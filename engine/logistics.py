"""Multi-modal freight planning: road + rail + barge (Level 9, Prompts 2, 5 and 8 together).

Each mode's speed comes from the physics built earlier:
  road  - truck speed from Greenshields: v = v_max (1 - k / k_jam), more trucks = more density
  rail  - balancing speed on the ruling grade: P / v = m g (sin(theta) + C_rr); too many wagons
          and the adhesion limit mu m_loco g cos(theta) < m g sin(theta) stalls the train
  barge - speed through water +/- river current
"""
import math
from dataclasses import dataclass

from .traffic import greenshields_speed
from .vehicles import G, VehicleSpec, max_climbable_grade

# Corridor data
ROAD_KM, RAIL_KM, RIVER_KM = 80.0, 95.0, 120.0
TRUCK_T = 25.0
TRUCK_DAY = 9000.0
TRUCK_VMAX_KMH, ROAD_KJAM, ROAD_BG_DENSITY = 70.0, 120.0, 20.0
TRUCK_FUEL_LOADED, TRUCK_FUEL_EMPTY = 0.35, 0.25   # L per km
TRUCK_LOAD_H = 0.5

RAIL_GRADE = math.atan(0.012)          # 1.2% ruling grade
RAKE_DAY = 120000.0
WAGON_T, WAGON_TARE = 60.0, 22.0
RAIL_TRANSFER_RS_T = 60.0
RAIL_TERMINAL_H = 3.0
RAIL_FUEL_L_PER_GROSS_TKM = 0.004
LOCO = VehicleSpec("Freight loco", mass=130e3, power=3.2e6, driven_mass=130e3, length=22,
                   axles=6, C_rr=0.002, mu_dry=0.30, max_speed=22.0)

BARGE_T = 1000.0
BARGE_DAY = 60000.0
BARGE_WATER_SPEED = 3.0               # m/s through the water
RIVER_CURRENT = 1.0                   # m/s, helps on the way to the port
BARGE_TERMINAL_H = 6.0
BARGE_TRANSFER_RS_T = 100.0
BARGE_FUEL_L_PER_TKM = 0.004

DIESEL_RS_L = 100.0
TRUCK_RISK_PER_KM = 4e-4
RAIL_RISK_PER_KM = 5e-4
BARGE_RISK_PER_KM = 3e-4


@dataclass
class Plan:
    road_t: float = 6000.0
    rail_t: float = 0.0
    barge_t: float = 0.0
    trucks: int = 60
    rakes: int = 1
    wagons: int = 30
    barges: int = 1


@dataclass
class ModeResult:
    name: str
    tonnes: float
    trips: int
    one_way_h: float
    round_h: float
    hours: float
    cost: float
    fuel_l: float
    risk: float
    note: str = ""


@dataclass
class PlanResult:
    modes: list
    hours: float
    cost: float
    fuel_l: float
    safety: float
    feasible: bool
    problem: str = ""
    problem_kind: str = ""


def _finish_time(trips, fleet, one_way_h, round_h, load_h):
    if trips <= 0:
        return 0.0
    rounds = math.ceil(trips / max(fleet, 1))
    return (rounds - 1) * round_h + load_h + one_way_h


def truck_speed_kmh(trucks):
    """Trucks spread over both directions of the 80 km road add to background density."""
    k = ROAD_BG_DENSITY + trucks / (2 * ROAD_KM) * 2.5   # a truck counts as 2.5 cars
    return max(5.0, greenshields_speed(k, TRUCK_VMAX_KMH, ROAD_KJAM))


def train_spec(wagons):
    return LOCO.with_cargo(wagons, wagon_tare=WAGON_TARE * 1000, wagon_load=WAGON_T * 1000,
                           wagon_len=15)


def train_grade_speed(wagons):
    """Balancing speed on the ruling grade: P / v = m g (sin(theta) + C_rr cos(theta))."""
    sp = train_spec(wagons)
    resist = sp.mass * G * (math.sin(RAIL_GRADE) + sp.C_rr * math.cos(RAIL_GRADE))
    return min(sp.max_speed, sp.power / resist)


def evaluate(plan: Plan):
    modes, problem, kind = [], "", ""
    # --- road ---
    if plan.road_t > 0:
        n = max(plan.trucks, 0)
        v = truck_speed_kmh(n)
        trips = math.ceil(plan.road_t / TRUCK_T)
        one = ROAD_KM / v
        rnd = 2 * one + 2 * TRUCK_LOAD_H
        hours = _finish_time(trips, n, one, rnd, TRUCK_LOAD_H) if n else math.inf
        days = math.ceil(max(hours, 1) / 24) if math.isfinite(hours) else 0
        fuel = trips * ROAD_KM * (TRUCK_FUEL_LOADED + TRUCK_FUEL_EMPTY)
        cost = n * days * TRUCK_DAY + fuel * DIESEL_RS_L
        risk = trips * 2 * ROAD_KM * TRUCK_RISK_PER_KM
        modes.append(ModeResult("Road", plan.road_t, trips, one, rnd, hours, cost, fuel, risk,
                                f"{n} trucks at {v:.0f} km/h (Greenshields)"))
        if n == 0:
            problem, kind = "Road freight assigned but no trucks hired", "timeout"
    # --- rail ---
    if plan.rail_t > 0:
        sp = train_spec(plan.wagons)
        if max_climbable_grade(sp) < RAIL_GRADE:
            problem = (f"STALL: {plan.wagons} wagons weigh {sp.mass/1e6:.2f} kt - the 1.2% grade "
                       f"pulls back m g sin(theta) = {sp.mass*G*math.sin(RAIL_GRADE)/1e3:.0f} kN but "
                       f"adhesion allows only mu m_loco g = {sp.mu_dry*sp.driven_mass*G/1e3:.0f} kN")
            kind = "stall"
        v_grade = train_grade_speed(plan.wagons)
        v_avg = 0.4 * v_grade + 0.6 * sp.max_speed
        per_train = plan.wagons * WAGON_T
        trips = math.ceil(plan.rail_t / per_train)
        one = RAIL_KM / (v_avg * 3.6)
        rnd = 2 * one + 2 * RAIL_TERMINAL_H
        hours = _finish_time(trips, plan.rakes, one, rnd, RAIL_TERMINAL_H) if plan.rakes else math.inf
        days = math.ceil(max(hours, 1) / 24) if math.isfinite(hours) else 0
        fuel = trips * RAIL_KM * sp.mass / 1000 * RAIL_FUEL_L_PER_GROSS_TKM * 1.6
        cost = plan.rakes * days * RAKE_DAY + fuel * DIESEL_RS_L + plan.rail_t * RAIL_TRANSFER_RS_T
        risk = trips * 2 * RAIL_KM * RAIL_RISK_PER_KM
        modes.append(ModeResult("Rail", plan.rail_t, trips, one, rnd, hours, cost, fuel, risk,
                                f"{plan.rakes} train(s) x {plan.wagons} wagons, "
                                f"{v_grade*3.6:.0f} km/h on the grade"))
    # --- barge ---
    if plan.barge_t > 0:
        down = BARGE_WATER_SPEED + RIVER_CURRENT
        up = BARGE_WATER_SPEED - RIVER_CURRENT
        trips = math.ceil(plan.barge_t / BARGE_T)
        one = RIVER_KM / (down * 3.6)
        rnd = one + RIVER_KM / (up * 3.6) + 2 * BARGE_TERMINAL_H
        hours = _finish_time(trips, plan.barges, one, rnd, BARGE_TERMINAL_H) if plan.barges else math.inf
        days = math.ceil(max(hours, 1) / 24) if math.isfinite(hours) else 0
        fuel = trips * RIVER_KM * BARGE_T * BARGE_FUEL_L_PER_TKM * 1.4
        cost = plan.barges * days * BARGE_DAY + fuel * DIESEL_RS_L + plan.barge_t * BARGE_TRANSFER_RS_T
        risk = trips * 2 * RIVER_KM * BARGE_RISK_PER_KM
        modes.append(ModeResult("Barge", plan.barge_t, trips, one, rnd, hours, cost, fuel, risk,
                                f"{plan.barges} barge(s): {down*3.6:.1f} km/h down, "
                                f"{up*3.6:.1f} km/h back"))
    hours = max((m.hours for m in modes), default=0.0)
    cost = sum(m.cost for m in modes)
    fuel = sum(m.fuel_l for m in modes)
    risk = sum(m.risk for m in modes)
    safety = max(0.0, 100.0 - risk)
    feasible = not problem and math.isfinite(hours)
    return PlanResult(modes, hours, cost, fuel, safety, feasible, problem, kind)


def search_frontier(total_t, step=500.0, fleets=None):
    """Brute-force 'optimizer' over allocations and fleet sizes (small linear-programming
    stand-in). Returns [(plan, result)] for every feasible plan."""
    fleets = fleets or dict(trucks=(20, 40, 80, 120), rakes=(1, 2), wagons=(30, 40), barges=(1, 2, 3))
    out = []
    n = int(total_t / step)
    for i in range(n + 1):
        for j in range(n + 1 - i):
            road, rail = i * step, j * step
            barge = total_t - road - rail
            for tr in (fleets["trucks"] if road else (0,)):
                for rk in (fleets["rakes"] if rail else (0,)):
                    for wg in (fleets["wagons"] if rail else (30,)):
                        for bg in (fleets["barges"] if barge else (0,)):
                            p = Plan(road, rail, barge, tr, rk, wg, bg)
                            r = evaluate(p)
                            if r.feasible:
                                out.append((p, r))
    return out
