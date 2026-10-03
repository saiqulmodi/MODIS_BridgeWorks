"""Funds & Fun: costs, revenue, factor of safety and Pareto ranking (Prompt 8).

    Total Construction Cost = materials + labour/scaffolding + maintenance overhead
    Toll = (tonnes delivered x distance) / (time taken x fuel burned)   (x a payout scale)
    Factor of Safety FS = capacity / demand = 1 / (worst load ratio)
    Best practice: FS between 1.5 and 2.0 - not so low it collapses, not so high it bankrupts.
"""
import math
from dataclasses import dataclass

LABOUR_PER_JOINT = 4000.0       # Rs per joint (bolting, welding)
LABOUR_PER_MEMBER = 2500.0      # Rs per member placed
SCAFFOLD_PER_METRE_HEIGHT = 1500.0  # Rs per metre of height above ground per member


@dataclass
class CostBreakdown:
    materials: float = 0.0
    labour: float = 0.0
    maintenance: float = 0.0
    extras: float = 0.0
    carbon_kg: float = 0.0

    @property
    def total(self):
        return self.materials + self.labour + self.maintenance + self.extras

    def lines(self):
        return [("Materials", self.materials), ("Labour & scaffolding", self.labour),
                ("Maintenance (5 yr)", self.maintenance), ("Equipment & extras", self.extras)]


def member_material_cost(material, A, L, shape_fabrication=1.0):
    mass = material.density * A * L
    return mass * material.cost_per_kg * shape_fabrication, mass


def structure_cost(nodes, members, shape_fab=None, ground_y=None, extras=0.0, maintenance_years=5):
    """Cost of a truss design. shape_fab(member) -> fabrication multiplier.
    ground_y: height of the ground for scaffolding (members higher up cost more to place)."""
    cb = CostBreakdown(extras=extras)
    used = set()
    for m in members:
        a, b = nodes[m.i], nodes[m.j]
        L = math.hypot(b.x - a.x, b.y - a.y)
        fab = shape_fab(m) if shape_fab else 1.0
        cost, mass = member_material_cost(m.material, m.A, L, fab)
        cb.materials += cost
        cb.carbon_kg += mass * m.material.carbon_per_kg
        cb.maintenance += cost * m.material.maintenance_rate * maintenance_years / 5
        cb.labour += LABOUR_PER_MEMBER
        if ground_y is not None:
            h = max(0.0, (a.y + b.y) / 2 - ground_y)
            cb.labour += SCAFFOLD_PER_METRE_HEIGHT * h
        used.update((m.i, m.j))
    cb.labour += LABOUR_PER_JOINT * len(used)
    return cb


def toll(tonnes, distance_km, time_h, fuel_l, scale=1000.0):
    """Toll = (Tons x Distance) / (Time x Fuel) x scale  (Rs)."""
    if time_h <= 0 or fuel_l <= 0:
        return 0.0
    return scale * tonnes * distance_km / (time_h * fuel_l)


def factor_of_safety(max_ratio):
    return math.inf if max_ratio <= 0 else 1.0 / max_ratio


def fs_grade(fs):
    """Plain-language verdict on a factor of safety."""
    if fs < 1.0:
        return "FAILED", "Under-designed: it broke."
    if fs < 1.5:
        return "RISKY", "Stands, but with too little margin for surprises."
    if fs <= 2.0:
        return "OPTIMAL", "Just right: safe without wasting money."
    if fs <= 4.0:
        return "CONSERVATIVE", "Safe, but you paid for strength you don't need."
    return "OVER-ENGINEERED", "Far too heavy: profits are eaten by the extra steel."


def profit(revenue, build_cost, fs, budget):
    """Revenue minus cost, with an over-engineering penalty when FS > 4."""
    penalty = 0.0
    if fs > 4.0 and math.isfinite(fs):
        penalty = 0.05 * budget * min(fs - 4.0, 6.0)
    return revenue - build_cost - penalty, penalty


def pareto_front(points):
    """points: list of dicts with 'safety' (higher better), 'cost' and 'time' (lower better).
    Returns the indices of designs nobody beats on all three at once."""
    front = []
    for i, p in enumerate(points):
        dominated = False
        for j, q in enumerate(points):
            if i == j:
                continue
            no_worse = q["safety"] >= p["safety"] and q["cost"] <= p["cost"] and q["time"] <= p["time"]
            better = q["safety"] > p["safety"] or q["cost"] < p["cost"] or q["time"] < p["time"]
            if no_worse and better:
                dominated = True
                break
        if not dominated:
            front.append(i)
    return front


def star_rating(success, cost, par_cost, budget, fs=None, extra_goal=True):
    """1 star = mission done within budget; 2 = also under par cost; 3 = also extra goal met
    (optimal factor of safety for structures, or the level's own bonus goal)."""
    if not success or cost > budget:
        return 0
    stars = 1
    if cost <= par_cost:
        stars += 1
    if extra_goal and (fs is None or 1.5 <= fs <= 4.0):
        stars += 1
    return stars


def format_rs(x):
    """Indian-style rupee formatting: lakh and crore."""
    if x is None or not math.isfinite(x):
        return "-"
    sign = "-" if x < 0 else ""
    x = abs(x)
    if x >= 1e7:
        return f"{sign}Rs {x/1e7:.2f} Cr"
    if x >= 1e5:
        return f"{sign}Rs {x/1e5:.2f} L"
    return f"{sign}Rs {x:,.0f}"
