"""Road traffic flow (Prompt 5): macroscopic LWR theory + microscopic car-following.

Macroscopic (whole-road) view - Greenshields:
    v(k) = v_max (1 - k / k_jam)          k = density (vehicles per km)
    q = k v                                q = flow (vehicles per hour)
    k_crit = k_jam / 2,  q_max = v_max k_jam / 4
    shockwave speed  w = (q2 - q1) / (k2 - k1)   (negative = jam grows backwards)

Microscopic (one car at a time) view - Intelligent Driver Model (IDM):
    a = a_max [ 1 - (v / v0)^4 - (s* / s)^2 ],   s* = s0 + v T + v dv / (2 sqrt(a_max b))
"""
import math
import random
from dataclasses import dataclass, field

# --- macroscopic -----------------------------------------------------------------------


def greenshields_speed(k, v_max, k_jam):
    return max(0.0, v_max * (1 - k / k_jam))


def greenshields_flow(k, v_max, k_jam):
    return k * greenshields_speed(k, v_max, k_jam)


def critical_density(k_jam):
    return k_jam / 2


def max_flow(v_max, k_jam):
    return v_max * k_jam / 4


def greenberg_speed(k, v0, k_jam):
    """Greenberg: v = v0 ln(k_jam / k) (good for heavy, congested traffic)."""
    if k <= 0:
        return math.inf
    return max(0.0, v0 * math.log(k_jam / k))


def shockwave_speed(q1, k1, q2, k2):
    """Speed of the boundary between two traffic states (km/h if q in veh/h and k in veh/km)."""
    if k2 == k1:
        return 0.0
    return (q2 - q1) / (k2 - k1)


def ctm_step(k, dx, dt, v_max, k_jam, inflow, out_capacity=None, w=None):
    """One Cell-Transmission-Model step of the LWR equation (Godunov scheme).

    k: list of cell densities (veh/m); dx: cell length (m); dt: s; v_max: m/s;
    inflow: veh/s offered at the upstream end; out_capacity: veh/s the downstream end accepts.
    Returns (new densities, actual inflow, outflow)."""
    q_max = v_max * k_jam / 4
    w = w if w is not None else v_max          # backward wave speed (Greenshields: = v_max)
    k_c = k_jam / 2

    def demand(kk):
        return greenshields_flow(min(kk, k_c), v_max, k_jam) if kk < k_c else q_max

    def supply(kk):
        return q_max if kk <= k_c else max(0.0, min(q_max, w * (k_jam - kk)))

    n = len(k)
    flux = [0.0] * (n + 1)
    flux[0] = min(inflow, supply(k[0]))
    for i in range(1, n):
        flux[i] = min(demand(k[i - 1]), supply(k[i]))
    cap = q_max if out_capacity is None else out_capacity
    flux[n] = min(demand(k[-1]), cap)
    new = [k[i] + dt / dx * (flux[i] - flux[i + 1]) for i in range(n)]
    return new, flux[0], flux[n]


# --- microscopic ------------------------------------------------------------------------


@dataclass(frozen=True)
class IDMParams:
    v0: float = 13.9          # desired speed (m/s) = 50 km/h
    T: float = 1.2            # safe time headway (s)
    a_max: float = 1.4        # comfortable acceleration (m/s^2)
    b: float = 1.5            # comfortable braking (m/s^2)
    s0: float = 2.0           # minimum gap (m)
    delta: float = 4.0
    length: float = 5.0


def idm_accel(v, gap, dv, p):
    """IDM acceleration. gap: bumper-to-bumper distance to the leader (inf if none);
    dv = v - v_leader (positive when closing in)."""
    free = 1 - (v / p.v0) ** p.delta
    if gap == math.inf:
        return p.a_max * free
    s_star = p.s0 + max(0.0, v * p.T + v * dv / (2 * math.sqrt(p.a_max * p.b)))
    return p.a_max * (free - (s_star / max(gap, 0.1)) ** 2)


@dataclass
class Car:
    cid: int
    road: str
    x: float
    v: float
    t_spawn: float           # when it wanted to enter (includes time queued off-map)
    t_enter: float = 0.0
    idle: float = 0.0
    waiting_since: float = None


@dataclass
class RoadDef:
    name: str
    length: float
    conflict: tuple          # (start, end) of the junction box along this road
    peak_demand: float       # veh/h


@dataclass
class TrafficConfig:
    duration: float = 720.0          # 12 rush-hour minutes
    main: RoadDef = field(default_factory=lambda: RoadDef("MAIN", 700.0, (300.0, 320.0), 1100.0))
    cross: RoadDef = field(default_factory=lambda: RoadDef("CROSS", 500.0, (250.0, 270.0), 400.0))
    gridlock_queue: int = 15
    cell: float = 20.0               # heat-map cell length, m
    seed: int = 7


def demand_factor(t, duration):
    """Rush-hour shape: 50% -> 100% over the first 30%, hold, then ease off in the last 20%."""
    r = t / duration
    if r < 0.3:
        return 0.5 + 0.5 * r / 0.3
    if r < 0.8:
        return 1.0
    return max(0.5, 1.0 - 0.5 * (r - 0.8) / 0.2)


class TrafficSim:
    MODES = ("signals", "roundabout", "overpass")
    MERGE_GAP = 2.0     # s between two cars merging at a roundabout

    def __init__(self, mode="signals", cycle=60.0, main_split=0.5, speed_kmh=50.0, cfg=None):
        if mode not in self.MODES:
            raise ValueError(mode)
        self.cfg = cfg or TrafficConfig()
        self.mode = mode
        self.cycle = cycle
        self.main_split = main_split
        self.params = IDMParams(v0=speed_kmh / 3.6)
        self.roads = {"MAIN": self.cfg.main, "CROSS": self.cfg.cross}
        self.cars = {"MAIN": [], "CROSS": []}
        self.queue = {"MAIN": [], "CROSS": []}      # off-map spawn times waiting to enter
        self.next_spawn = {"MAIN": 0.0, "CROSS": 1.3}
        self.rng = random.Random(self.cfg.seed)
        self.time = 0.0
        self.next_id = 1
        self.exited = []          # (road, travel_time, exit_time)
        self.idle_time = 0.0
        self.fuel = 0.0           # litres
        self.failure = None
        self.history = []         # (t, throughput veh/min, avg travel time s)
        self.detector = []        # (k veh/km, q veh/h) samples upstream of the junction
        self._last_hist = 0.0
        self.lost_time = 5.0      # amber + all-red per phase change

    # --- junction control -------------------------------------------------------------------
    def signal_state(self, road, t=None):
        """'G', 'A' (amber/all-red), or 'R' for this road at time t."""
        t = self.time if t is None else t
        c = t % self.cycle
        g_main = max(5.0, self.main_split * self.cycle - self.lost_time)
        g_cross = max(5.0, self.cycle - g_main - 2 * self.lost_time)
        if c < g_main:
            main, cross = "G", "R"
        elif c < g_main + self.lost_time:
            main, cross = "A", "R"
        elif c < g_main + self.lost_time + g_cross:
            main, cross = "R", "G"
        else:
            main, cross = "R", "A"
        return main if road == "MAIN" else cross

    def capacity(self, road, sat_flow=1800.0):
        """Theoretical signal capacity = s * g / C (veh/h)."""
        if self.mode != "signals":
            return None
        g_main = max(5.0, self.main_split * self.cycle - self.lost_time)
        g_cross = max(5.0, self.cycle - g_main - 2 * self.lost_time)
        g = g_main if road == "MAIN" else g_cross
        return sat_flow * g / self.cycle

    def box(self, road):
        """The stretch of `road` shared with the other road. A roundabout's merge point is
        much shorter than a crossroads box, because cars only cut across one lane."""
        a, b = self.roads[road].conflict
        return (a, a + 8.0) if self.mode == "roundabout" else (a, b)

    def _box_busy(self, road, ignore=None):
        other = "CROSS" if road == "MAIN" else "MAIN"
        a, b = self.box(other)
        return any(a - 2 < c.x < b + self.params.length for c in self.cars[other] if c is not ignore)

    def _other_arrives_soon(self, road, horizon):
        other = "CROSS" if road == "MAIN" else "MAIN"
        a, _ = self.roads[other].conflict
        for c in self.cars[other]:
            d = a - c.x
            if 0 <= d and d / max(c.v, 0.5) < horizon and c.waiting_since is None:
                return True
        return False

    def _must_stop(self, car, road):
        """Does this car have to stop at the junction stop line?"""
        a, _ = self.roads[road].conflict
        dist = a - car.x
        if dist < 0:
            return False
        if self.mode == "overpass":
            return False
        if self.mode == "signals":
            st = self.signal_state(road)
            if st == "G":
                return False
            if st == "A" and car.waiting_since is None:
                # amber dilemma zone: too close to stop (firm 3 m/s^2 braking) -> keep going
                return dist > car.v * car.v / (2 * 3.0) + 1.0
            return True
        # Roundabout: cars merge in turn. Whoever reaches the merge point first goes; the
        # other car must arrive at least GAP seconds later or wait (gap acceptance).
        if dist > 50:
            return False
        if self._box_busy(road):
            return True
        other = "CROSS" if road == "MAIN" else "MAIN"
        a_other = self.roads[other].conflict[0]
        rivals = [c for c in self.cars[other] if 0 <= a_other - c.x <= 50]
        if not rivals:
            return False
        lead = max(rivals, key=lambda c: c.x)
        my_eta = dist / max(car.v, 1.0)
        their_eta = (a_other - lead.x) / max(lead.v, 1.0)
        they_first = their_eta < my_eta or (their_eta == my_eta and road == "CROSS")
        return they_first and my_eta - their_eta < self.MERGE_GAP

    # --- simulation ---------------------------------------------------------------------
    def _spawn(self, dt):
        for road in ("MAIN", "CROSS"):
            rd = self.roads[road]
            rate = rd.peak_demand * demand_factor(self.time, self.cfg.duration) / 3600.0
            while self.next_spawn[road] <= self.time:
                self.queue[road].append(self.next_spawn[road])
                gap = 1.0 / rate if rate > 0 else math.inf
                self.next_spawn[road] += gap * self.rng.uniform(0.7, 1.3)
            cars = self.cars[road]
            if self.queue[road]:
                last = cars[-1] if cars else None
                if last is None or last.x > self.params.length + self.params.s0 + 4:
                    t_want = self.queue[road].pop(0)
                    v_in = min(self.params.v0, last.v if last else self.params.v0)
                    cars.append(Car(self.next_id, road, 0.0, v_in, t_want, self.time))
                    self.next_id += 1
            if len(self.queue[road]) > self.cfg.gridlock_queue and not self.failure:
                cap = self.capacity(road)
                demand = rd.peak_demand
                if cap is not None:
                    formula = (f"Demand {demand:.0f} veh/h > capacity s*g/C = 1800 x "
                               f"{cap/1800*self.cycle:.0f}/{self.cycle:.0f} = {cap:.0f} veh/h")
                else:
                    formula = (f"Demand {demand:.0f} veh/h exceeded what the junction could pass; "
                               f"q = k v collapses once k > k_crit")
                self.failure = (f"GRIDLOCK on {road}: {len(self.queue[road])} cars queued back "
                                f"past the city edge", formula)

    def step(self, dt):
        if self.failure:
            return
        self.time += dt
        self._spawn(dt)
        p = self.params
        for road in ("MAIN", "CROSS"):
            rd = self.roads[road]
            cars = self.cars[road]          # ordered: index 0 is furthest along
            cars.sort(key=lambda c: -c.x)
            new_v = []
            for idx, car in enumerate(cars):
                gap, dv = math.inf, 0.0
                if idx > 0:
                    lead = cars[idx - 1]
                    gap = lead.x - car.x - p.length
                    dv = car.v - lead.v
                a_box, _ = rd.conflict
                v_cap = None
                if self.mode == "roundabout" and a_box - 40 < car.x < rd.conflict[1] + 20:
                    v_cap = 8.0
                if self._must_stop(car, road):
                    stop_gap = a_box - 1.0 - car.x
                    if stop_gap < gap:
                        gap, dv = stop_gap, car.v
                    if car.waiting_since is None and stop_gap < 30:
                        car.waiting_since = self.time
                else:
                    if car.x > a_box:
                        car.waiting_since = None
                acc = idm_accel(car.v, gap, dv, p)
                if v_cap is not None and car.v > v_cap:
                    acc = min(acc, -1.5)
                new_v.append(max(0.0, car.v + acc * dt))
            for car, v in zip(cars, new_v):
                car.x += 0.5 * (car.v + v) * dt
                car.v = v
                if v < 1.0:
                    car.idle += dt
                    self.idle_time += dt
                    self.fuel += 0.6 / 3600 * dt          # idling: ~0.6 L/h
                else:
                    self.fuel += 0.08 / 1000 * v * dt     # moving: ~8 L/100 km
            for car in [c for c in cars if c.x > rd.length]:
                cars.remove(car)
                self.exited.append((road, self.time - car.t_spawn, self.time))
        # junction safety check (should never trigger; guards against logic bugs)
        if self.mode != "overpass":
            in_main = [c for c in self.cars["MAIN"] if self.box("MAIN")[0] < c.x < self.box("MAIN")[1]]
            in_cross = [c for c in self.cars["CROSS"] if self.box("CROSS")[0] < c.x < self.box("CROSS")[1]]
            if in_main and in_cross:
                self.near_misses = getattr(self, "near_misses", 0) + 1
        self._record()

    def _record(self):
        if self.time - self._last_hist >= 10.0:
            self._last_hist = self.time
            recent = [e for e in self.exited if e[2] > self.time - 60]
            tput = len(recent)
            avg_tt = sum(e[1] for e in recent) / len(recent) if recent else 0.0
            self.history.append((self.time, tput, avg_tt))
            # detector: 200 m stretch of MAIN just upstream of the junction
            a = self.roads["MAIN"].conflict[0]
            seg = [c for c in self.cars["MAIN"] if a - 220 < c.x < a - 20]
            k = len(seg) / 0.2                      # veh/km
            v = (sum(c.v for c in seg) / len(seg)) * 3.6 if seg else self.params.v0 * 3.6
            self.detector.append((k, k * v))

    def heatmap(self, road):
        """Average speed (m/s) per cell, or None for empty cells."""
        rd = self.roads[road]
        n = int(math.ceil(rd.length / self.cfg.cell))
        sums, counts = [0.0] * n, [0] * n
        for c in self.cars[road]:
            i = min(n - 1, max(0, int(c.x / self.cfg.cell)))
            sums[i] += c.v
            counts[i] += 1
        return [sums[i] / counts[i] if counts[i] else None for i in range(n)]

    # --- results ----------------------------------------------------------------------
    def free_flow_time(self, road):
        return self.roads[road].length / self.params.v0

    def stats(self):
        n = len(self.exited)
        tt = [e[1] for e in self.exited]
        main_tt = [e[1] for e in self.exited if e[0] == "MAIN"]
        demand = sum(rd.peak_demand for rd in self.roads.values())
        return {
            "exited": n,
            "throughput_per_min": n / (self.time / 60) if self.time else 0.0,
            "avg_travel_time": sum(tt) / n if n else 0.0,
            "main_delay_ratio": (sum(main_tt) / len(main_tt)) / self.free_flow_time("MAIN") if main_tt else 0.0,
            "idle_time": self.idle_time,
            "fuel_l": self.fuel,
            "queued": sum(len(q) for q in self.queue.values()),
            "peak_demand_vph": demand,
        }

    def run(self, dt=0.25, until=None):
        until = until or self.cfg.duration
        while not self.failure and self.time < until:
            self.step(dt)
        return self
