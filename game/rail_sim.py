"""Railway levels (2, 4): track profile design, earthworks cost and the train run."""
import math
from dataclasses import dataclass, field

from engine.failure import FailureReport
from engine.vehicles import G, TrackPath, VehicleEngine, VehicleSpec, braking_distance, max_climbable_grade

LOCOS = {
    "Tank engine": VehicleSpec("Tank engine", mass=30e3, power=250e3, driven_mass=30e3, length=9,
                               axles=3, C_rr=0.002, mu_dry=0.30, mu_wet=0.18, max_speed=12, cost=150000),
    "Diesel shunter": VehicleSpec("Diesel shunter", mass=60e3, power=500e3, driven_mass=60e3,
                                  length=12, axles=4, C_rr=0.002, mu_dry=0.30, mu_wet=0.18,
                                  max_speed=14, cost=350000),
    "Mainline diesel": VehicleSpec("Mainline diesel", mass=120e3, power=2.2e6, driven_mass=120e3,
                                   length=20, axles=6, C_rr=0.002, mu_dry=0.30, mu_wet=0.18,
                                   max_speed=20, cost=1000000),
    "Double-header": VehicleSpec("Double-header", mass=240e3, power=4.4e6, driven_mass=240e3,
                                 length=40, axles=12, C_rr=0.002, mu_dry=0.30, mu_wet=0.18,
                                 max_speed=20, cost=1800000),
}
BANKER = dict(power=400e3, mass=50e3, cost=250000)
WAGON_HIRE = {False: 20000.0, True: 50000.0}     # small / heavy wagons


@dataclass
class RailDesign:
    heights: list                 # track height at each station
    loco: str = "Diesel shunter"
    wagons: int = 2
    banker: bool = False
    brake_x: float = None         # where the driver starts braking (L4)


def ground_height(cfg, x):
    pts = cfg["ground"]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1] if x > pts[-1][0] else pts[0][1]


def default_design(cfg):
    hs = [ground_height(cfg, x) for x in cfg["stations"]]
    brake = None
    if cfg.get("brake_marker"):
        brake = cfg["stop_x"] - 120
    return RailDesign(hs, cfg["locos"][0], 2, False, brake)


def fixed_station(cfg, i):
    x = cfg["stations"][i]
    (a0, a1), (b0, b1) = cfg["fixed_ends"]
    return a0 <= x <= a1 or b0 <= x <= b1


def train_spec(cfg, d):
    base = LOCOS[d.loco]
    if d.banker:
        base = VehicleSpec(base.name + " + banker", mass=base.mass + BANKER["mass"],
                           power=base.power + BANKER["power"],
                           driven_mass=base.driven_mass + BANKER["mass"],
                           length=base.length + 12, axles=base.axles + 4, C_rr=base.C_rr,
                           mu_dry=base.mu_dry, mu_wet=base.mu_wet, max_speed=base.max_speed,
                           cost=base.cost + BANKER["cost"])
    return base.with_cargo(d.wagons, wagon_tare=cfg["wagon_tare"], wagon_load=cfg["wagon_load"])


def track_points(cfg, d):
    return list(zip(cfg["stations"], d.heights))


def grades(cfg, d):
    pts = track_points(cfg, d)
    return [math.degrees(math.atan2(y1 - y0, x1 - x0)) for (x0, y0), (x1, y1) in zip(pts, pts[1:])]


@dataclass
class CostInfo:
    track: float
    cut: float
    fill: float
    loco: float
    wagons: float
    cut_m2: float
    fill_m2: float

    @property
    def total(self):
        return self.track + self.cut + self.fill + self.loco + self.wagons


def cost(cfg, d):
    pts = track_points(cfg, d)
    length = sum(math.hypot(x1 - x0, y1 - y0) for (x0, y0), (x1, y1) in zip(pts, pts[1:]))
    cut = fill = 0.0
    x_start, x_end = pts[0][0], pts[-1][0]
    x = x_start
    while x < x_end:
        xm = x + 0.5
        # track height by linear interpolation
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            if xa <= xm <= xb:
                h = ya + (yb - ya) * (xm - xa) / (xb - xa)
                break
        dh = h - ground_height(cfg, xm)
        if dh > 0:
            fill += dh          # m^2 per metre: embankment / trestle
        else:
            cut += -dh
        x += 1.0
    spec = train_spec(cfg, d)
    heavy = cfg["wagon_load"] > 40000
    return CostInfo(track=length * cfg["track_rs_m"], cut=cut * cfg["cut_rs_m2"],
                    fill=fill * cfg["fill_rs_m2"], loco=spec.cost,
                    wagons=d.wagons * WAGON_HIRE[heavy], cut_m2=cut, fill_m2=fill)


class RailSim:
    """One loaded trip; the total job time is extrapolated from it."""

    def __init__(self, cfg, d):
        self.cfg = cfg
        self.design = d
        self.spec = train_spec(cfg, d)
        self.path = TrackPath(track_points(cfg, d))
        start = cfg["start_x"]
        self.engine = VehicleEngine(self.spec, self.path, s=start + 0.0, v=0.0,
                                    speed_limit=self.spec.max_speed)
        self.engine.s = start
        self.engine.s_start = self.engine.s
        self.engine.h0 = self.engine.centre_height()
        self.time = 0.0
        self.failure = None
        self.done = False
        self.phase = "drive"         # drive / brake / creep / stopped
        self.history = {"speed m/s": [], "PE MJ": [], "KE MJ": []}
        self.stop_error = None
        cargo = d.wagons * cfg["wagon_load"] / 1000
        self.cargo_per_trip = cargo
        self.trips = math.ceil(cfg["cargo_target"] / cargo) if cargo > 0 else 0
        self.events = []

    @property
    def front_x(self):
        return self.path.point_at(self.engine.s)[0]

    def wet(self):
        w = self.cfg.get("wet_after_x")
        return w is not None and self.path.point_at(self.engine.centre_s())[0] > w

    def step(self, dt):
        if self.failure or self.done:
            return
        e = self.engine
        cfg = self.cfg
        self.time += dt
        e.wet = self.wet()
        if cfg.get("brake_marker"):
            if self.phase == "drive" and self.front_x >= self.design.brake_x:
                self.phase = "brake"
                self.events.append("brake")
            if self.phase == "brake":
                e.throttle, e.brake = 0.0, 1.0
                if e.v <= 0.05:
                    e.v = 0.0
                    if self.front_x < cfg["stop_x"] - 30:
                        self.phase = "creep"
                    else:
                        self._arrive()
                        return
            elif self.phase == "creep":
                # stopped short: crawl up to the stop line at walking pace
                e.throttle = 0.3 if e.v < 2.0 else 0.0
                e.brake = 0.6 if e.v > 3.0 else 0.0
                if self.front_x >= cfg["stop_x"] - 5:
                    self.phase = "brake"
                    e.throttle, e.brake = 0.0, 1.0
        else:
            if self.front_x >= cfg["end_x"]:
                self._arrive()
                return
        f = e.step(dt)
        if self.time - (self.history["speed m/s"][-1][0] if self.history["speed m/s"] else -1) >= 0.25:
            self.history["speed m/s"].append((self.time, e.v))
            self.history["PE MJ"].append((self.time, e.potential_energy / 1e6))
            self.history["KE MJ"].append((self.time, e.kinetic_energy / 1e6))
        # failures
        self._stuck = getattr(self, "_stuck", 0.0) + dt if (e.v <= 0.01 and e.throttle > 0
                                                             and self.phase != "brake") else 0.0
        if e.runaway or self._stuck > 3.0:
            self.failure = FailureReport(
                "stall", "STALLED AND ROLLED BACK", e.stall_explanation(),
                [f"Max grade this train can climb: "
                 f"{math.degrees(max_climbable_grade(self.spec, e.wet)):.1f} deg "
                 f"(tan = mu m_loco / m - C_rr)", f"Steepest grade on your track: "
                 f"{max(grades(cfg, self.design)):.1f} deg"], self.time, None, self.history)
            return
        if self.phase == "brake" and e.brake >= 1.0 and f.net > 0 and e.v > 1.0:
            theta = -f.theta
            mu = self.spec.mu_wet if e.wet else self.spec.mu_dry
            self.failure = FailureReport(
                "runaway", "RUNAWAY: brakes cannot hold the train",
                f"g sin(theta) = {G*math.sin(theta):.2f} > mu g cos(theta) = "
                f"{mu*G*math.cos(theta):.2f} m/s^2 on a {math.degrees(theta):.1f} deg descent",
                ["Wet rails: mu fell from 0.30 to 0.18." if e.wet else ""], self.time, None, self.history)
            return
        if e.v > 1.6 * self.spec.max_speed:
            self.failure = FailureReport(
                "runaway", f"OVERSPEED: {e.v*3.6:.0f} km/h on the descent",
                f"Going downhill gravity adds g sin(theta) = {G*math.sin(max(-f.theta, 0)):.2f} m/s^2 "
                f"every second. The line limit is {self.spec.max_speed*3.6:.0f} km/h.",
                ["Make the descent gentler, or start braking before the train runs away."],
                self.time, None, self.history)
            return
        if cfg.get("buffer_x") is not None and self.front_x >= cfg["buffer_x"]:
            mu = self.spec.mu_wet if e.wet else self.spec.mu_dry
            self.failure = FailureReport(
                "overrun", f"HIT THE BUFFERS at {e.v*3.6:.0f} km/h",
                f"d_stop = v^2 / (2 (mu g cos - g sin)): from {self._brake_speed:.1f} m/s needed "
                f"{braking_distance(self._brake_speed, mu, self._brake_theta):.0f} m, you allowed "
                f"{cfg['stop_x'] - self.design.brake_x:.0f} m", [], self.time, None, self.history)
            return
        if self.phase == "brake" and not hasattr(self, "_brake_speed_set"):
            self._brake_speed_set = True
            self._brake_speed = e.v
            self._brake_theta = -f.theta
        if self.time > 400:
            self.failure = FailureReport("timeout", "THE TRIP NEVER FINISHED",
                                         "The train got stuck", time=self.time, history=self.history)

    def _arrive(self):
        self.done = True
        if self.cfg.get("brake_marker"):
            self.stop_error = self.front_x - self.cfg["stop_x"]

    @property
    def trip_time(self):
        return self.time

    def total_time(self):
        """Loaded trips plus the empty return runs in between (returns are ~70% as long)."""
        return self.trips * self.trip_time + max(self.trips - 1, 0) * 0.7 * self.trip_time

    def predicted_brake_distance(self, v=None):
        e = self.engine
        mu = self.spec.mu_wet if self.cfg.get("wet_after_x") is not None else self.spec.mu_dry
        x = self.design.brake_x or self.cfg["stop_x"]
        theta = 0.0
        for (x0, y0), (x1, y1) in zip(self.path.points, self.path.points[1:]):
            if x0 <= x <= x1:
                theta = -math.atan2(y1 - y0, x1 - x0)
        v = v if v is not None else self.spec.max_speed
        return braking_distance(v, mu, theta), mu, theta
