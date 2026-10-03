"""Vehicle kinematics and rail/road dynamics (Prompt 2).

A vehicle (train, truck or maglev pod) moves along a TrackPath. Every step we add up:

    gravity along the slope   F_parallel = m g sin(theta)
    normal force              N = m g cos(theta)
    rolling resistance        F_rr = C_rr * N
    aerodynamic drag          F_drag = 0.5 * rho * C_d * A * v^2
    engine pull               T_e = min(P / v, mu * N_driven)     (adhesion limit)
    brakes                    F_b = brake * mu_brake * N

and use Newton's second law a = F_net / m. Energy is tracked so the HUD can show
potential (m g h), kinetic (1/2 m v^2) and heat lost to friction.
"""
import bisect
import math
from dataclasses import dataclass, field

G = 9.81
RHO_AIR = 1.225
V_MIN_POWER = 0.5   # m/s; below this the engine is limited by adhesion, not P/v


@dataclass(frozen=True)
class VehicleSpec:
    name: str
    mass: float            # total mass incl. cargo, kg
    power: float           # engine power at the wheels, W
    driven_mass: float     # mass resting on driven wheels (the locomotive), kg
    length: float          # m
    axles: int = 4
    C_rr: float = 0.002    # rolling resistance (steel wheel on rail ~0.002, tyre ~0.012)
    C_d: float = 1.0
    frontal_area: float = 9.0
    mu_dry: float = 0.30   # wheel-rail adhesion
    mu_wet: float = 0.18
    max_speed: float = 25.0
    cost: float = 0.0      # hire/purchase cost, Rs
    maglev: bool = False   # no wheels: no rolling resistance, thrust from linear motor
    max_thrust: float = 0.0  # maglev thrust limit, N
    cargo: float = 0.0     # tonnes of cargo carried (for delivery goals)

    def with_cargo(self, wagons, wagon_tare=15000.0, wagon_load=30000.0, wagon_len=14.0):
        """A new spec with `wagons` loaded wagons coupled behind."""
        return VehicleSpec(
            name=f"{self.name} + {wagons} wagons",
            mass=self.mass + wagons * (wagon_tare + wagon_load),
            power=self.power, driven_mass=self.driven_mass,
            length=self.length + wagons * wagon_len, axles=self.axles + 4 * wagons,
            C_rr=self.C_rr, C_d=self.C_d, frontal_area=self.frontal_area,
            mu_dry=self.mu_dry, mu_wet=self.mu_wet, max_speed=self.max_speed,
            cost=self.cost, maglev=self.maglev, max_thrust=self.max_thrust,
            cargo=self.cargo + wagons * wagon_load / 1000.0)


class TrackPath:
    """A polyline track. Distance s runs from 0 at the first point to `length` at the last."""

    def __init__(self, points):
        if len(points) < 2:
            raise ValueError("A track needs at least two points")
        self.points = [(float(x), float(y)) for x, y in points]
        self.cum = [0.0]
        for (x0, y0), (x1, y1) in zip(self.points, self.points[1:]):
            self.cum.append(self.cum[-1] + math.hypot(x1 - x0, y1 - y0))
        self.length = self.cum[-1]

    def segment_at(self, s):
        s = min(max(s, 0.0), self.length)
        k = bisect.bisect_right(self.cum, s) - 1
        return min(max(k, 0), len(self.points) - 2)

    def point_at(self, s):
        k = self.segment_at(s)
        seg = self.cum[k + 1] - self.cum[k]
        t = 0.0 if seg == 0 else (min(max(s, 0.0), self.length) - self.cum[k]) / seg
        (x0, y0), (x1, y1) = self.points[k], self.points[k + 1]
        # Extend straight beyond the ends so long trains hanging off the end still have a position
        if s < 0:
            t = s / seg if seg else 0.0
        elif s > self.length:
            t = 1 + (s - self.length) / seg if seg else 1.0
        return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t

    def angle_at(self, s):
        """Slope angle (radians) at distance s; positive = uphill in the direction of travel."""
        k = self.segment_at(s)
        (x0, y0), (x1, y1) = self.points[k], self.points[k + 1]
        return math.atan2(y1 - y0, x1 - x0)

    def height_at(self, s):
        return self.point_at(s)[1]


def tractive_effort(power, v, mu, normal_driven, max_thrust=0.0, maglev=False):
    """T_e = min(P / v, mu * N_driven). Maglev pods have no wheels: thrust is capped instead."""
    power_limited = power / max(abs(v), V_MIN_POWER)
    if maglev:
        return min(power_limited, max_thrust) if max_thrust else power_limited
    return min(power_limited, mu * normal_driven)


def braking_distance(v, mu, theta_down=0.0, g=G):
    """d_stop = v^2 / (2 (mu g cos(theta) - g sin(theta)))   - theta_down > 0 means going downhill.
    Returns math.inf when gravity beats the brakes (the train cannot stop)."""
    decel = g * (mu * math.cos(theta_down) - math.sin(theta_down))
    if decel <= 0:
        return math.inf
    return v * v / (2 * decel)


def max_climbable_grade(spec, wet=False):
    """Steepest slope (radians) the train can hold at crawling speed:
    mu * m_driven * g cos(theta) >= m g sin(theta) + C_rr m g cos(theta)."""
    mu = spec.mu_wet if wet else spec.mu_dry
    if spec.maglev:
        ratio = (spec.max_thrust or spec.power / V_MIN_POWER) / (spec.mass * G)
        return math.asin(min(1.0, ratio))
    tan_max = mu * spec.driven_mass / spec.mass - spec.C_rr
    return math.atan(max(tan_max, 0.0))


@dataclass
class ForceBreakdown:
    gravity: float = 0.0      # along track, + forward
    normal: float = 0.0
    rolling: float = 0.0      # always resists motion (sign applied)
    drag: float = 0.0
    traction: float = 0.0
    brake: float = 0.0
    adhesion_limit: float = 0.0
    power_limit: float = 0.0
    net: float = 0.0
    theta: float = 0.0

    @property
    def wheel_slip(self):
        return self.traction > 0 and self.power_limit > self.adhesion_limit


@dataclass
class VehicleEngine:
    spec: VehicleSpec
    path: TrackPath
    s: float = 0.0             # position of the FRONT of the vehicle along the path, m
    v: float = 0.0             # m/s, + forward
    throttle: float = 1.0      # 0..1
    brake: float = 0.0         # 0..1
    wet: bool = False
    speed_limit: float = None  # cruise control target, m/s
    power_factor: float = 1.0  # e.g. smart-grid brownout scales this down
    time: float = 0.0
    heat: float = 0.0          # J lost to friction, drag and brakes
    engine_work: float = 0.0   # J delivered by the engine
    stalled: bool = False
    runaway: bool = False
    max_back_slide: float = 0.0
    forces: ForceBreakdown = field(default_factory=ForceBreakdown)

    def __post_init__(self):
        self.h0 = self.centre_height()
        self.s_start = self.s

    # --- geometry helpers --------------------------------------------------
    def axle_positions(self):
        """Distances along the path of each axle (front to back)."""
        n = max(self.spec.axles, 1)
        if n == 1:
            return [self.s - self.spec.length / 2]
        step = self.spec.length / (n - 1)
        return [self.s - k * step for k in range(n)]

    def axle_points(self):
        """(x, y) of each axle."""
        return [self.path.point_at(a) for a in self.axle_positions()]

    def axle_load(self):
        """Weight carried by each axle, N."""
        return self.spec.mass * G / max(self.spec.axles, 1)

    def centre_s(self):
        return self.s - self.spec.length / 2

    def centre_height(self):
        return self.path.height_at(self.centre_s())

    def mean_slope(self):
        """Average sin/cos of the slope under all axles (a long train can straddle a crest)."""
        sins, coss = 0.0, 0.0
        axles = self.axle_positions()
        for a in axles:
            th = self.path.angle_at(a)
            sins += math.sin(th)
            coss += math.cos(th)
        return sins / len(axles), coss / len(axles)

    # --- energy ---------------------------------------------------------------
    @property
    def potential_energy(self):
        return self.spec.mass * G * (self.centre_height() - self.h0)

    @property
    def kinetic_energy(self):
        return 0.5 * self.spec.mass * self.v * self.v

    @property
    def momentum(self):
        return self.spec.mass * self.v

    @property
    def acceleration(self):
        return self.forces.net / self.spec.mass

    @property
    def finished(self):
        return self.s - self.spec.length >= self.path.length

    # --- physics step -----------------------------------------------------------
    def compute_forces(self):
        sp = self.spec
        sin_t, cos_t = self.mean_slope()
        f = ForceBreakdown(theta=math.atan2(sin_t, cos_t))
        f.gravity = -sp.mass * G * sin_t
        f.normal = sp.mass * G * cos_t
        mu = sp.mu_wet if self.wet else sp.mu_dry
        f.adhesion_limit = math.inf if sp.maglev else mu * sp.driven_mass * G * cos_t
        throttle = self.throttle
        if self.speed_limit is not None and self.v >= self.speed_limit:
            throttle = 0.0
        f.power_limit = sp.power * self.power_factor / max(abs(self.v), V_MIN_POWER)
        if throttle > 0:
            f.traction = throttle * tractive_effort(sp.power * self.power_factor, self.v, mu,
                                                    sp.driven_mass * G * cos_t,
                                                    sp.max_thrust, sp.maglev)
        rr = 0.0 if sp.maglev else sp.C_rr * f.normal
        brake = self.brake * (mu if not sp.maglev else 0.25) * f.normal
        drag = 0.5 * RHO_AIR * sp.C_d * sp.frontal_area * self.v * self.v
        direction = math.copysign(1.0, self.v) if abs(self.v) > 1e-6 else 0.0
        f.drag = -direction * drag
        if direction != 0:
            f.rolling = -direction * rr
            f.brake = -direction * brake
        else:
            # Standing still: static friction/brakes hold up to their limit
            push = f.gravity + f.traction
            hold = rr + brake
            if abs(push) <= hold:
                f.rolling, f.brake = -push, 0.0
            else:
                f.rolling = -math.copysign(hold, push)
        f.net = f.gravity + f.traction + f.rolling + f.drag + f.brake
        self.forces = f
        return f

    def step(self, dt):
        f = self.compute_forces()
        a = f.net / self.spec.mass
        v_new = self.v + a * dt
        # Resistive forces can bring us to rest, never push us backwards on their own
        if self.v > 0 > v_new and f.gravity + f.traction >= 0:
            v_new = 0.0
        if self.v < 0 < v_new and f.gravity + f.traction <= 0:
            v_new = 0.0
        ds = 0.5 * (self.v + v_new) * dt
        self.s += ds
        self.engine_work += f.traction * ds
        self.v = v_new
        self.time += dt
        # Work done against friction, drag and brakes turns into heat
        self.heat += abs(f.rolling * ds) + abs(f.drag * ds) + abs(f.brake * ds)
        # Stall / runaway detection
        if self.throttle > 0 and self.v <= 0 and f.gravity + f.traction < 0:
            self.stalled = True
        if self.v < -0.5:
            self.runaway = True
        self.max_back_slide = max(self.max_back_slide, self.s_start - self.s)
        return f

    def stall_explanation(self):
        f = self.forces
        mg_sin = -f.gravity
        return (f"Stall: m g sin(theta) = {mg_sin/1e3:.0f} kN pulled back harder than the engine's "
                f"best pull min(P/v, mu N) = {min(f.power_limit, f.adhesion_limit)/1e3:.0f} kN")
