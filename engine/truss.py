"""2D truss solver - the game's "smart calculator" core (Prompt 1).

Uses the Direct Stiffness Method: every member acts like a stiff spring
(k = E*A/L) along its own length. We add all the springs into one big
global stiffness matrix K, hold the supports still, and solve

    [K][U] = [F]

for how far every joint moves (U). From that movement we get each member's
pull or push (axial force N), its stress sigma = N/A and strain epsilon = sigma/E.

Sign convention: N > 0 is TENSION (being pulled), N < 0 is COMPRESSION (being pushed).
Units: metres, newtons, pascals.
"""
import math
from dataclasses import dataclass, field

import numpy as np

from .materials import Material

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


@dataclass
class Member:
    i: int                 # index of start node
    j: int                 # index of end node
    material: Material
    A: float               # cross-section area, m^2
    I: float               # second moment of area (bending stiffness of the shape), m^4
    K_eff: float = 1.0     # effective-length factor for buckling (1.0 = pinned both ends)


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

    @property
    def failed_members(self):
        return [k for k, m in enumerate(self.members) if m.status == FAILED]


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


class TrussSolver:
    def __init__(self, nodes, members):
        self.nodes = list(nodes)
        self.members = list(members)

    def _geometry(self, m):
        a, b = self.nodes[m.i], self.nodes[m.j]
        dx, dy = b.x - a.x, b.y - a.y
        L = math.hypot(dx, dy)
        if L == 0:
            raise ValueError(f"Member {m.i}-{m.j} has zero length")
        return L, dx / L, dy / L   # length, cos(theta), sin(theta)

    def stiffness_matrix(self):
        """Assemble the global stiffness matrix K (2 rows/cols per node: x then y)."""
        n = 2 * len(self.nodes)
        K = np.zeros((n, n))
        for m in self.members:
            L, c, s = self._geometry(m)
            k = m.material.E * m.A / L
            # Element stiffness in global axes = k * [T]^T [1 -1; -1 1] [T]
            t = np.array([c * c, c * s, s * s])
            ke = k * np.array([
                [t[0], t[1], -t[0], -t[1]],
                [t[1], t[2], -t[1], -t[2]],
                [-t[0], -t[1], t[0], t[1]],
                [-t[1], -t[2], t[1], t[2]],
            ])
            dofs = [2 * m.i, 2 * m.i + 1, 2 * m.j, 2 * m.j + 1]
            K[np.ix_(dofs, dofs)] += ke
        return K

    def solve(self, extra_loads=None):
        """Solve the truss.

        extra_loads: optional {node_index: (fx, fy)} added on top of each Node's own load
        (used later for moving vehicles passing axle loads onto the bridge).
        """
        n_nodes = len(self.nodes)
        K = self.stiffness_matrix()
        F = np.zeros(2 * n_nodes)
        fixed = []
        for idx, nd in enumerate(self.nodes):
            F[2 * idx] += nd.fx
            F[2 * idx + 1] += nd.fy
            if nd.fix_x:
                fixed.append(2 * idx)
            if nd.fix_y:
                fixed.append(2 * idx + 1)
        for idx, (fx, fy) in (extra_loads or {}).items():
            F[2 * idx] += fx
            F[2 * idx + 1] += fy

        free = [d for d in range(2 * n_nodes) if d not in set(fixed)]
        U = np.zeros(2 * n_nodes)
        if free:
            K_ff = K[np.ix_(free, free)]
            # A free-to-move structure has a singular K. Check with a scale-aware rank test.
            if np.linalg.matrix_rank(K_ff, tol=1e-9 * np.abs(K_ff).max()) < len(free):
                raise UnstableStructure(
                    "The structure can wobble freely - add diagonal braces to make triangles.")
            U[free] = np.linalg.solve(K_ff, F[free])

        reactions_flat = K @ U - F
        reactions = np.zeros((n_nodes, 2))
        for d in fixed:
            reactions[d // 2, d % 2] = reactions_flat[d]

        results, node_forces = [], []
        for idx, m in enumerate(self.members):
            L, c, s = self._geometry(m)
            ui, vi = U[2 * m.i], U[2 * m.i + 1]
            uj, vj = U[2 * m.j], U[2 * m.j + 1]
            elongation = c * (uj - ui) + s * (vj - vi)
            N = m.material.E * m.A / L * elongation
            results.append(self._member_result(m, N, L))
            # Newton's third law: a member in tension pulls each end toward the other.
            node_forces.append((m.i, idx, N * c, N * s))
            node_forces.append((m.j, idx, -N * c, -N * s))

        return SolveResult(U.reshape(n_nodes, 2), results, reactions, node_forces)

    @staticmethod
    def _member_result(m, N, L):
        mat = m.material
        stress = N / m.A
        strain = stress / mat.E
        P_cr = euler_buckling_load(mat.E, m.I, m.K_eff, L)
        tiny = 1e-6  # newtons; below this we treat the member as unloaded

        if N > tiny:  # tension
            limit = mat.tensile_strength * m.A
            ratio = N / limit if limit > 0 else math.inf
            mode = "yield"
            explanation = (f"Tension: sigma = N/A = {N/1e3:.1f} kN / {m.A*1e4:.1f} cm^2 = "
                           f"{stress/1e6:.1f} MPa (limit {mat.tensile_strength/1e6:.0f} MPa)")
        elif N < -tiny:  # compression: whichever is weaker, crushing or buckling
            crush = mat.compressive_strength * m.A
            limit = min(crush, P_cr)
            ratio = -N / limit
            mode = "buckling" if P_cr < crush else "yield"
            if mode == "buckling":
                explanation = (f"Compression: {-N/1e3:.1f} kN vs Euler P_cr = pi^2*E*I/(K*L)^2 = "
                               f"{P_cr/1e3:.1f} kN")
            else:
                explanation = (f"Compression: sigma = {stress/1e6:.1f} MPa "
                               f"(crush limit {mat.compressive_strength/1e6:.0f} MPa)")
        else:
            limit, ratio, mode = mat.tensile_strength * m.A, 0.0, ""
            explanation = "Unloaded (zero-force member)"

        status = status_for_ratio(ratio)
        if status == FAILED:
            if mode == "buckling":
                explanation = (f"BUCKLED: compressive force {-N/1e3:.0f} kN exceeded "
                               f"P_cr {P_cr/1e3:.0f} kN")
            elif N > 0:
                explanation = (f"SNAPPED: tensile stress {stress/1e6:.1f} MPa exceeded "
                               f"{mat.tensile_strength/1e6:.0f} MPa")
            else:
                explanation = (f"CRUSHED: compressive stress {-stress/1e6:.1f} MPa exceeded "
                               f"{mat.compressive_strength/1e6:.0f} MPa")

        return MemberResult(N, stress, strain, L, limit, P_cr, ratio, status,
                            mode if status == FAILED else "", explanation)
