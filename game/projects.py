"""
The 5 build projects, easiest to toughest. Pure logic, no drawing.

Each project gives fixed joints over a gap, a road deck that is already built,
and supports. The student joins joints with members (beams or cables), paying
"parts" earned by answering that project's questions, then tests the bridge:
a vehicle drives across and the real truss solver (engine/truss.py) checks
every member for snapping, crushing and buckling at every position.
"""
import math
from dataclasses import dataclass, field

from engine import materials as M
from engine.truss import FAILED, Member, Node, TrussSolver, UnstableStructure, self_weight_loads, G

SIZE_COST = {"S": 1, "M": 2, "L": 3, "XL": 4}     # parts per member
PARTS_PER_CORRECT = {1: 4, 2: 6, 3: 8, 4: 6, 5: 8}   # parts earned per right answer, by project
DECK_SIZE = "L"
PYLON_AREA = 0.25                # m^2 of concrete in a pylon segment


@dataclass
class Vehicle:
    name: str
    mass_kg: float
    axles: tuple            # axle offsets behind the front, m; weight shared equally
    colour: tuple = (250, 204, 21)

    @property
    def length(self):
        return max(self.axles) + 2.0


@dataclass
class Project:
    id: int
    name: str
    level: str
    span: float
    joints: list            # [(x, y)] in metres, y up; deck joints first, left to right
    n_deck: int
    supports: dict          # joint -> "pin" or "roller"
    prebuilt: list          # [(i, j, material, size, kind)]
    materials: list         # materials the student may use
    sizes: list
    vehicle: Vehicle
    dead_load: float        # road slab, N per metre of deck
    impact: float = 1.0     # dynamic factor on the vehicle (bumps, braking)
    goal: str = ""
    tip: str = ""
    lesson: str = ""
    deck_material: M.Material = M.STEEL
    deck_joints: list = field(default_factory=list)

    def __post_init__(self):
        self.deck_joints = list(range(self.n_deck))


def _deck(span, panels):
    step = span / panels
    return [(round(k * step, 3), 0.0) for k in range(panels + 1)]


def _p1():
    deck = _deck(20, 4)
    masts = [(0.0, 9.0), (20.0, 9.0)]
    return Project(
        1, "Tension Fibers", "Class 1-7", 20, deck + masts, len(deck),
        {0: "pin", 4: "roller", 5: "pin", 6: "pin"},
        [(i, i + 1, M.TIMBER, "XL", "deck") for i in range(4)],
        [M.STEEL_CABLE], ["S", "M"],
        Vehicle("Car", 1200, (0.0, 2.6)), dead_load=1500, deck_material=M.TIMBER,
        goal="Hold up the 3 middle road joints with cables from the two masts.",
        tip="Click a mast top, then a road joint, to hang a cable. Cables can only pull.",
        lesson="A cable is pulled tight (tension). Its pull T holds the road up: T sin(angle) = load.")


def _p2():
    deck = _deck(30, 6)
    top = [(5.0 * k, 5.0) for k in range(1, 6)]
    return Project(
        2, "Coplanar Trusses", "Class 8-10", 30, deck + top, len(deck),
        {0: "pin", 6: "roller"},
        [(i, i + 1, M.STEEL, DECK_SIZE, "deck") for i in range(6)],
        [M.STEEL, M.TIMBER], ["S", "M", "L"],
        Vehicle("Minibus", 6000, (0.0, 4.5)), dead_load=1000,
        goal="Build a truss: a top chord and diagonals so every panel is a triangle.",
        tip="A square can fold flat; a triangle cannot. Join every top joint so it makes triangles.",
        lesson="Triangles keep their shape. Members are pulled (tension) or pushed (compression); "
               "pushed long thin members buckle: P_cr = pi^2 E I / L^2.")


def _p3():
    deck = _deck(40, 8)
    arch = [(5.0 * k, round(12.0 * (1 - ((5.0 * k - 20) / 20) ** 2), 3)) for k in range(1, 8)]
    return Project(
        3, "Parabolic Thrust", "Class 11-12", 40, deck + arch, len(deck),
        {0: "pin", 8: "pin"},
        [(i, i + 1, M.STEEL, DECK_SIZE, "deck") for i in range(8)],
        [M.CONCRETE, M.STEEL, M.STEEL_CABLE], ["S", "M", "L", "XL"],
        Vehicle("Truck", 12000, (0.0, 4.0, 8.0)), dead_load=3000,
        goal="Build the arch rib from bank to bank, hang the road from it, and brace it.",
        tip="Arches are pushed (compression): steel or concrete. A moving truck can make a cable "
            "hanger go slack - steel hangers can push and pull. Add a few diagonal braces.",
        lesson="A parabolic arch carries an even load in pure compression; it pushes outward "
               "on both banks (thrust H = w L^2 / 8h), so both supports must be pinned.")


def _p4():
    deck = _deck(60, 12)
    pylon = [(30.0, -8.0), (30.0, 22.0)]
    base, top = len(deck), len(deck) + 1
    return Project(
        4, "Stay Dynamics", "JEE Main / NEET", 60, deck + pylon, len(deck),
        {0: "pin", 12: "roller", base: "pin"},
        [(i, i + 1, M.STEEL, "XL", "deck") for i in range(12)]
        + [(base, 6, M.CONCRETE, "XL", "pylon"), (6, top, M.CONCRETE, "XL", "pylon")],
        [M.STEEL_CABLE, M.STEEL], ["S", "M", "L", "XL"],
        Vehicle("Heavy-haul trailer", 70000, (0.0, 3.5, 7.0, 10.5)), dead_load=12000, impact=1.15,
        goal="Cable-stay the road from one tall pylon. Balance the cables on both sides.",
        tip="Anchor the pylon top with a backstay cable to each bank support, then put matching "
            "cables left and right. Flat cables need a bigger size.",
        lesson="A flat cable needs a bigger pull for the same lift: T = W / sin(angle). "
               "The horizontal parts of the stays must balance at the pylon top.")


def _p5():
    deck = _deck(80, 16)
    n = len(deck)
    pylons = [(20.0, -8.0), (20.0, 20.0), (60.0, -8.0), (60.0, 20.0)]
    b1, t1, b2, t2 = n, n + 1, n + 2, n + 3
    return Project(
        5, "Matrix Dissipation", "IIT / NIT Olympiad", 80, deck + pylons, n,
        {0: "pin", 16: "roller", b1: "pin", b2: "pin"},
        [(i, i + 1, M.STEEL, "XL", "deck") for i in range(16)]
        + [(b1, 4, M.CONCRETE, "XL", "pylon"), (4, t1, M.CONCRETE, "XL", "pylon"),
           (b2, 12, M.CONCRETE, "XL", "pylon"), (12, t2, M.CONCRETE, "XL", "pylon")],
        [M.STEEL_CABLE, M.CARBON_CABLE, M.STEEL], ["S", "M", "L", "XL"],
        Vehicle("Freight convoy", 160000, (0.0, 4.0, 8.0, 14.0, 18.0, 22.0), (244, 114, 182)),
        dead_load=15000, impact=1.3,
        goal="Two pylons, a long span and a heavy convoy with 30% impact. Use parts wisely.",
        tip="Anchor each pylon top to its bank, tie the two tops together, and share the middle "
            "span between both pylons. Carbon cable is stronger for the same size.",
        lesson="Impact (dynamic) load = 1.3 x static. The stiffness matrix [K][U] = [F] shares "
               "the load between all members in proportion to their stiffness E A / L.")


PROJECTS = [_p1(), _p2(), _p3(), _p4(), _p5()]


def make_member(i, j, material, size, kind):
    if kind == "pylon":                   # a massive tower, not a build-menu beam
        A = PYLON_AREA
        I = M.second_moment(M.BOX, A)
    elif material.cable_only:
        A = M.CABLE_SIZES[size]
        I = M.second_moment(M.SOLID, A)
        kind = "cable"
    else:
        A = M.BEAM_SIZES[size]
        I = M.second_moment(M.IBEAM, A)
    return Member(i, j, material, A, I, kind=kind)


class Design:
    """The student's bridge for one project."""

    def __init__(self, project):
        self.p = project
        self.members = []           # [(i, j, material, size)]
        self.parts = 0
        self.complete = False
        self._solver = None

    def length(self, i, j):
        (x1, y1), (x2, y2) = self.p.joints[i], self.p.joints[j]
        return math.hypot(x2 - x1, y2 - y1)

    def taken(self, i, j):
        pairs = {frozenset((a, b)) for a, b, *_ in self.p.prebuilt}
        pairs |= {frozenset((a, b)) for a, b, *_ in self.members}
        return frozenset((i, j)) in pairs

    def can_add(self, i, j, size):
        if i == j:
            return "Pick two different joints."
        if self.taken(i, j):
            return "Those joints are already joined."
        if self.parts < SIZE_COST[size]:
            return f"Need {SIZE_COST[size]} parts for size {size} - answer questions to earn parts."
        return ""

    def add(self, i, j, material, size):
        msg = self.can_add(i, j, size)
        if not msg:
            self.members.append((i, j, material, size))
            self.parts -= SIZE_COST[size]
            self._solver = None
        return msg

    def remove(self, k):
        i, j, material, size = self.members.pop(k)
        self.parts += SIZE_COST[size]
        self._solver = None

    def clear(self):
        while self.members:
            self.remove(len(self.members) - 1)

    def all_members(self):
        """[(i, j, material, size, kind, player_index or None)] - prebuilt first."""
        out = [(i, j, mat, size, kind, None) for i, j, mat, size, kind in self.p.prebuilt]
        out += [(i, j, mat, size, "beam", k) for k, (i, j, mat, size) in enumerate(self.members)]
        return out

    def _build(self):
        nodes = []
        for k, (x, y) in enumerate(self.p.joints):
            kind = self.p.supports.get(k)
            nodes.append(Node.pinned(x, y) if kind == "pin" else Node.roller(x, y) if kind == "roller"
                         else Node(x, y))
        members = [make_member(i, j, mat, size, kind) for i, j, mat, size, kind, _ in self.all_members()]
        solver = TrussSolver(nodes, members)
        dead = self.p.dead_load
        base = self_weight_loads(nodes, members, lambda m: dead if m.kind == "deck" else 0.0)
        return solver, base

    def vehicle_loads(self, front_x):
        """Axle loads at deck joints (lever rule) for a vehicle whose front is at front_x."""
        v, deck = self.p.vehicle, self.p.joints[:self.p.n_deck]
        w = v.mass_kg * G * self.p.impact / len(v.axles)
        loads = {}
        for off in v.axles:
            x = front_x - off
            if not 0.0 <= x <= self.p.span:
                continue
            for k in range(self.p.n_deck - 1):
                x0, x1 = deck[k][0], deck[k + 1][0]
                if x0 <= x <= x1:
                    t = (x - x0) / (x1 - x0)
                    loads[k] = (0.0, loads.get(k, (0, 0))[1] - w * (1 - t))
                    loads[k + 1] = (0.0, loads.get(k + 1, (0, 0))[1] - w * t)
                    break
        return loads

    def solve_at(self, front_x):
        """SolveResult with the vehicle front at front_x. Raises UnstableStructure."""
        if self._solver is None:
            self._solver = self._build()
        solver, base = self._solver
        loads = dict(base)
        for k, (fx, fy) in self.vehicle_loads(front_x).items():
            bx, by = loads.get(k, (0.0, 0.0))
            loads[k] = (bx + fx, by + fy)
        return solver.solve(loads)

    def test_positions(self, step=0.5):
        x, end = 0.0, self.p.span + self.p.vehicle.length
        while x <= end:
            yield x
            x += step

    def full_test(self):
        """(passed, message, worst_ratio). Used by the tests and for quick checks."""
        worst = 0.0
        try:
            for x in self.test_positions():
                r = self.solve_at(x)
                worst = max(worst, r.max_ratio)
                if r.failed_members:
                    return False, r.members[r.worst_member].explanation, worst
        except UnstableStructure as e:
            return False, str(e), worst
        return True, "", worst


def is_failed(result):
    return any(m.status == FAILED for m in result.members)
