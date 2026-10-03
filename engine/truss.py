"""2D truss solver - the game's "smart calculator" core (Prompt 1).

Uses the Direct Stiffness Method: every member acts like a stiff spring
(k = E*A/L) along its own length. We add all the springs into one big
global stiffness matrix K, hold the supports still, and solve

    [K][U] = [F]

for how far every joint moves (U). From that movement we get each member's
pull or push (axial force N), its stress sigma = N/A and strain epsilon = sigma/E.

Sign convention: N > 0 is TENSION (being pulled), N < 0 is COMPRESSION (being pushed).
Units: metres, newtons, pascals.  +y is UP.
"""
import math
from dataclasses import dataclass, field

import numpy as np

from .materials import Material

G = 9.81

# Load-ratio bands for the colour-coded HUD
GREEN, YELLOW, RED, FAILED = "green", "yellow", "red", "failed"


class UnstableStructure(Exception):
    """The structure is a mechanism (it can move freely) - e.g. a square with no diagonal."""


@dataclass
class Node:
    x: float
    y: float
    fix_x: bool = False   # support stops sideways movement
    fix_y: bool = False   # support stops up/down movement
    fx: float = 0.0       # applied load, N (+x is right)
    fy: float = 0.0       # applied load, N (+y is UP)

    @classmethod
    def pinned(cls, x, y):
        """Pin support: cannot move in any direction (can still rotate)."""
        return cls(x, y, fix_x=True, fix_y=True)

    @classmethod
    def roller(cls, x, y):
        """Roller support: holds the joint up, but lets it slide sideways."""
        return cls(x, y, fix_x=False, fix_y=True)

    @property
    def is_support(self):
        return self.fix_x or self.fix_y


@dataclass
class Member:
    i: int                 # index of start node
    j: int                 # index of end node
    material: Material
    A: float               # cross-section area, m^2
    I: float               # second moment of area (bending stiffness of the shape), m^4
    K_eff: float = 1.0     # effective-length factor for buckling (1.0 = pinned both ends)
    tension_only: bool = None   # cables: can pull but go slack when pushed
    E_factor: float = 1.0       # e.g. smart alloy powered = 2.0
    strength_factor: float = 1.0  # e.g. wet timber = 0.7
    kind: str = "beam"     # "beam", "deck" or "cable" - used by the game layer

    def __post_init__(self):
        if self.tension_only is None:
            self.tension_only = self.material.cable_only

    @property
    def E(self):
        return self.material.E * self.E_factor


@dataclass
class MemberResult:
    N: float               # axial force, N (+ tension, - compression)
    stress: float          # sigma = N / A, Pa
    strain: float          # epsilon = sigma / E
    length: float          # m
    limit: float           # the force (N, positive) this member can carry in its current mode
    P_cr: float            # Euler buckling load, N
    ratio: float           # |N| / limit  (0 = relaxed, 1 = at the limit, >1 = failed)
    status: str            # green / yellow / red / failed
    failure_mode: str      # "" or "yield" (pulled apart / crushed) or "buckling"
    explanation: str       # human-readable formula with numbers, for the calculator panel
    slack: bool = False    # cable that went slack (cables cannot push)

    @property
    def in_tension(self):
        return self.N > 0

    @property
    def display_ratio(self):
        """Load ratio clamped to 0..1 for colour bars."""
        return min(self.ratio, 1.0)


@dataclass
class SolveResult:
    displacements: np.ndarray            # shape (n_nodes, 2), metres
    members: list                        # list[MemberResult]
    reactions: np.ndarray                # shape (n_nodes, 2), N, non-zero only at supports
    node_forces: list = field(default_factory=list)  # [(node, member, fx, fy)] action-reaction arrows
    loads: np.ndarray = None             # shape (n_nodes, 2), total applied loads used

    @property
    def failed_members(self):
        return [k for k, m in enumerate(self.members) if m.status == FAILED]

    @property
    def max_ratio(self):
        return max((m.ratio for m in self.members), default=0.0)

    @property
    def worst_member(self):
        if not self.members:
            return None
        return max(range(len(self.members)), key=lambda k: self.members[k].ratio)


def euler_buckling_load(E, I, K_eff, L):
    """P_cr = pi^2 * E * I / (K_eff * L)^2"""
    return math.pi ** 2 * E * I / (K_eff * L) ** 2


def status_for_ratio(ratio):
    if ratio > 1.0:
        return FAILED
    if ratio >= 0.8:
        return RED
    if ratio >= 0.5:
        return YELLOW
    return GREEN


def member_length(nodes, m):
    a, b = nodes[m.i], nodes[m.j]
    return math.hypot(b.x - a.x, b.y - a.y)


def member_mass(nodes, m):
    return m.material.density * m.A * member_length(nodes, m)


def self_weight_loads(nodes, members, extra_per_metre=None, g=G):
    """Gravity on every member, split half to each end joint.

    extra_per_metre(member) -> N/m of extra dead load (e.g. a road slab on deck members).
    Returns {node_index: (fx, fy)}.
    """
    loads = {}
    for m in members:
        L = member_length(nodes, m)
        w = member_mass(nodes, m) * g
        if extra_per_metre:
            w += extra_per_metre(m) * L
        for n in (m.i, m.j):
            fx, fy = loads.get(n, (0.0, 0.0))
            loads[n] = (fx, fy - w / 2)
    return loads


class TrussSolver:
    """Solves a pin-jointed truss. The stiffness matrix is cached, so calling solve()
    every frame with different extra_loads (moving vehicles, wind, quakes) is cheap."""

    def __init__(self, nodes, members):
        self.nodes = list(nodes)
        self.members = list(members)
        self._geom = [self._geometry(m) for m in self.members]
        self._cache = {}
        n = 2 * len(self.nodes)
        self._fixed = []
        for idx, nd in enumerate(self.nodes):
            if nd.fix_x:
                self._fixed.append(2 * idx)
            if nd.fix_y:
                self._fixed.append(2 * idx + 1)
        fixed_set = set(self._fixed)
        self._free = [d for d in range(n) if d not in fixed_set]

    def _geometry(self, m):
        a, b = self.nodes[m.i], self.nodes[m.j]
        dx, dy = b.x - a.x, b.y - a.y
        L = math.hypot(dx, dy)
        if L == 0:
            raise ValueError(f"Member {m.i}-{m.j} has zero length")
        return L, dx / L, dy / L   # length, cos(theta), sin(theta)

    def _element_matrix(self, idx):
        m = self.members[idx]
        L, c, s = self._geom[idx]
        k = m.E * m.A / L
        # Element stiffness in global axes = k * [T]^T [1 -1; -1 1] [T]
        cc, cs, ss = c * c, c * s, s * s
        return k * np.array([
            [cc, cs, -cc, -cs],
            [cs, ss, -cs, -ss],
            [-cc, -cs, cc, cs],
            [-cs, -ss, cs, ss],
        ])

    def stiffness_matrix(self, skip=frozenset()):
        """Assemble the global stiffness matrix K (2 rows/cols per node: x then y)."""
        n = 2 * len(self.nodes)
        K = np.zeros((n, n))
        for idx, m in enumerate(self.members):
            if idx in skip:
                continue
            dofs = [2 * m.i, 2 * m.i + 1, 2 * m.j, 2 * m.j + 1]
            K[np.ix_(dofs, dofs)] += self._element_matrix(idx)
        return K

    def _factor(self, slack):
        key = frozenset(slack)
        if key not in self._cache:
            K = self.stiffness_matrix(key)
            free = self._free
            if free:
                K_ff = K[np.ix_(free, free)]
                scale = np.abs(K_ff).max() if K_ff.size else 1.0
                if scale == 0 or np.linalg.matrix_rank(K_ff, tol=1e-9 * scale) < len(free):
                    raise UnstableStructure(
                        "The structure can wobble freely - add diagonal braces to make triangles"
                        " (and remember cables can only pull, never push).")
                K_inv = np.linalg.inv(K_ff)
            else:
                K_inv = np.zeros((0, 0))
            self._cache[key] = (K, K_inv)
            if len(self._cache) > 64:
                self._cache.pop(next(iter(self._cache)))
        return self._cache[key]

    def _elongation(self, idx, U):
        m = self.members[idx]
        _, c, s = self._geom[idx]
        return (c * (U[2 * m.j] - U[2 * m.i]) + s * (U[2 * m.j + 1] - U[2 * m.i + 1]))

    def solve(self, extra_loads=None):
        """Solve the truss.

        extra_loads: optional {node_index: (fx, fy)} added on top of each Node's own load
        (self weight, moving vehicles, wind, earthquakes...).
        """
        n_nodes = len(self.nodes)
        F = np.zeros(2 * n_nodes)
        for idx, nd in enumerate(self.nodes):
            F[2 * idx] += nd.fx
            F[2 * idx + 1] += nd.fy
        for idx, (fx, fy) in (extra_loads or {}).items():
            F[2 * idx] += fx
            F[2 * idx + 1] += fy

        cables = [k for k, m in enumerate(self.members) if m.tension_only]
        slack = set()
        free = self._free
        for _ in range(2 * len(cables) + 2):
            K, K_inv = self._factor(slack)
            U = np.zeros(2 * n_nodes)
            if free:
                U[free] = K_inv @ F[free]
            # Cables that are being pushed go slack; slack cables that are stretched re-tighten.
            new_slack = {k for k in cables if self._elongation(k, U) < -1e-12}
            if new_slack == slack:
                break
            # Release only the most-compressed cable at a time for a stable, unique answer.
            added = new_slack - slack
            if added:
                worst = min(added, key=lambda k: self._elongation(k, U))
                slack = (slack & new_slack) | {worst}
            else:
                slack = new_slack

        reactions_flat = K @ U - F
        reactions = np.zeros((n_nodes, 2))
        for d in self._fixed:
            reactions[d // 2, d % 2] = reactions_flat[d]

        results, node_forces = [], []
        for idx, m in enumerate(self.members):
            L, c, s = self._geom[idx]
            if idx in slack:
                N = 0.0
            else:
                N = m.E * m.A / L * self._elongation(idx, U)
            results.append(self._member_result(m, N, L, idx in slack))
            # Newton's third law: a member in tension pulls each end toward the other.
            node_forces.append((m.i, idx, N * c, N * s))
            node_forces.append((m.j, idx, -N * c, -N * s))

        return SolveResult(U.reshape(n_nodes, 2), results, reactions, node_forces,
                           F.reshape(n_nodes, 2))

    @staticmethod
    def _member_result(m, N, L, slack=False):
        mat = m.material
        stress = N / m.A
        strain = stress / m.E
        P_cr = euler_buckling_load(m.E, m.I, m.K_eff, L)
        tiny = 1e-6  # newtons; below this we treat the member as unloaded
        t_strength = mat.tensile_strength * m.strength_factor
        c_strength = mat.compressive_strength * m.strength_factor

        if slack:
            return MemberResult(0.0, 0.0, 0.0, L, t_strength * m.A, P_cr, 0.0, GREEN, "",
                                "Slack: cables can only pull, never push", slack=True)

        if N > tiny:  # tension
            limit = t_strength * m.A
            ratio = N / limit if limit > 0 else math.inf
            mode = "yield"
            explanation = (f"Tension: sigma = N/A = {N/1e3:.1f} kN / {m.A*1e4:.1f} cm^2 = "
                           f"{stress/1e6:.1f} MPa (limit {t_strength/1e6:.0f} MPa)")
        elif N < -tiny:  # compression: whichever is weaker, crushing or buckling
            crush = c_strength * m.A
            limit = min(crush, P_cr)
            ratio = -N / limit if limit > 0 else math.inf
            mode = "buckling" if P_cr < crush else "yield"
            if mode == "buckling":
                explanation = (f"Compression: {-N/1e3:.1f} kN vs Euler P_cr = pi^2*E*I/(K*L)^2 = "
                               f"{P_cr/1e3:.1f} kN")
            else:
                explanation = (f"Compression: sigma = {stress/1e6:.1f} MPa "
                               f"(crush limit {c_strength/1e6:.0f} MPa)")
        else:
            limit, ratio, mode = t_strength * m.A, 0.0, ""
            explanation = "Unloaded (zero-force member)"

        status = status_for_ratio(ratio)
        if status == FAILED:
            if mode == "buckling":
                explanation = (f"BUCKLED: compressive force {-N/1e3:.0f} kN exceeded "
                               f"P_cr {P_cr/1e3:.0f} kN")
            elif N > 0:
                explanation = (f"SNAPPED: tensile stress {stress/1e6:.1f} MPa exceeded "
                               f"{t_strength/1e6:.0f} MPa")
            else:
                explanation = (f"CRUSHED: compressive stress {-stress/1e6:.1f} MPa exceeded "
                               f"{c_strength/1e6:.0f} MPa")

        return MemberResult(N, stress, strain, L, limit, P_cr, ratio, status,
                            mode if status == FAILED else "", explanation)
