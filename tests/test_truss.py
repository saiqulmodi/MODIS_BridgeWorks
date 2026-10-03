"""Checks the truss solver against hand-worked textbook answers."""
import math

import pytest

from engine.materials import CONCRETE, STEEL
from engine.truss import (FAILED, GREEN, RED, YELLOW, Member, Node, TrussSolver,
                          UnstableStructure, euler_buckling_load, status_for_ratio)

P = 10_000.0          # 10 kN test load
A = 0.002             # 20 cm^2
I_STOCKY = 1e-5       # stiff section - no buckling at these loads
REL = 1e-6


def steel(i, j, A=A, I=I_STOCKY):
    return Member(i, j, STEEL, A, I)


def test_single_bar_stretch_matches_PL_over_EA():
    L = 3.0
    nodes = [Node.pinned(0, 0), Node(L, 0, fix_y=True, fx=P)]
    res = TrussSolver(nodes, [steel(0, 1)]).solve()
    assert res.displacements[1, 0] == pytest.approx(P * L / (STEEL.E * A), rel=REL)
    m = res.members[0]
    assert m.N == pytest.approx(P, rel=REL)
    assert m.stress == pytest.approx(P / A, rel=REL)
    assert m.strain == pytest.approx(P / A / STEEL.E, rel=REL)
    assert res.reactions[0, 0] == pytest.approx(-P, rel=REL)


def test_wall_cantilever_truss():
    # Wall at x=0 with two pins (bottom A, top B). Free tip C at (1, 0) carries P downward.
    # Method of joints at C: diagonal BC = +P*sqrt(2) (tension), bottom AC = -P (compression).
    nodes = [Node.pinned(0, 0), Node.pinned(0, 1), Node(1, 0, fy=-P)]
    res = TrussSolver(nodes, [steel(0, 2), steel(1, 2)]).solve()
    assert res.members[0].N == pytest.approx(-P, rel=REL)
    assert res.members[1].N == pytest.approx(P * math.sqrt(2), rel=REL)
    # Reactions balance the load: sum Fy = 0 and sum Fx = 0
    assert res.reactions[:, 1].sum() == pytest.approx(P, rel=REL)
    assert res.reactions[:, 0].sum() == pytest.approx(0, abs=1e-6)


def test_warren_truss_midspan_load():
    # Two equilateral triangles plus a top chord, side 2 m. P at the bottom middle joint.
    h = math.sqrt(3)
    nodes = [Node.pinned(0, 0), Node(2, 0, fy=-P), Node.roller(4, 0),
             Node(1, h), Node(3, h)]
    members = [steel(0, 1), steel(1, 2),             # bottom chord
               steel(0, 3), steel(3, 1),             # left triangle sides
               steel(1, 4), steel(4, 2),             # right triangle sides
               steel(3, 4)]                          # top chord
    res = TrussSolver(nodes, members).solve()
    N = [m.N for m in res.members]
    s3 = math.sqrt(3)
    assert N[0] == pytest.approx(P / (2 * s3), rel=REL)   # bottom chord tension
    assert N[1] == pytest.approx(P / (2 * s3), rel=REL)
    assert N[2] == pytest.approx(-P / s3, rel=REL)        # end diagonals compression
    assert N[5] == pytest.approx(-P / s3, rel=REL)
    assert N[3] == pytest.approx(P / s3, rel=REL)         # inner diagonals tension
    assert N[4] == pytest.approx(P / s3, rel=REL)
    assert N[6] == pytest.approx(-P / s3, rel=REL)        # top chord compression
    assert res.reactions[0, 1] == pytest.approx(P / 2, rel=REL)
    assert res.reactions[2, 1] == pytest.approx(P / 2, rel=REL)


def test_newtons_third_law_pairs_cancel():
    nodes = [Node.pinned(0, 0), Node.pinned(0, 1), Node(1, 0, fy=-P)]
    res = TrussSolver(nodes, [steel(0, 2), steel(1, 2)]).solve()
    for k in range(0, len(res.node_forces), 2):
        _, _, fx1, fy1 = res.node_forces[k]
        _, _, fx2, fy2 = res.node_forces[k + 1]
        assert fx1 + fx2 == pytest.approx(0, abs=1e-9)
        assert fy1 + fy2 == pytest.approx(0, abs=1e-9)


def test_euler_buckling_formula():
    E, I, K, L = 200e9, 1e-8, 1.0, 2.0
    assert euler_buckling_load(E, I, K, L) == pytest.approx(math.pi ** 2 * E * I / 4)
    # Fixed-free column (K = 2) is four times weaker than pinned-pinned
    assert euler_buckling_load(E, I, 2.0, L) == pytest.approx(euler_buckling_load(E, I, 1.0, L) / 4)


def test_slender_strut_buckles_before_crushing():
    I_thin = 1e-9   # P_cr = pi^2*200e9*1e-9/1^2 ~ 1.97 kN, far below the 500 kN crush limit
    nodes = [Node.pinned(0, 0), Node(1, 0, fix_y=True, fx=-P)]
    res = TrussSolver(nodes, [steel(0, 1, I=I_thin)]).solve()
    m = res.members[0]
    assert m.N == pytest.approx(-P, rel=REL)
    assert m.status == FAILED
    assert m.failure_mode == "buckling"
    assert "P_cr" in m.explanation


def test_overloaded_tie_snaps():
    big = STEEL.tensile_strength * A * 1.1
    nodes = [Node.pinned(0, 0), Node(1, 0, fix_y=True, fx=big)]
    m = TrussSolver(nodes, [steel(0, 1)]).solve().members[0]
    assert m.status == FAILED and m.failure_mode == "yield"
    assert m.explanation.startswith("SNAPPED")


def test_concrete_cannot_take_tension():
    nodes = [Node.pinned(0, 0), Node(1, 0, fix_y=True, fx=100.0)]
    m = TrussSolver(nodes, [Member(0, 1, CONCRETE, 0.04, 1e-4)]).solve().members[0]
    assert m.status == FAILED


def test_square_without_diagonal_is_unstable():
    nodes = [Node.pinned(0, 0), Node.roller(1, 0), Node(1, 1), Node(0, 1, fx=P)]
    members = [steel(0, 1), steel(1, 2), steel(2, 3), steel(3, 0)]
    with pytest.raises(UnstableStructure):
        TrussSolver(nodes, members).solve()
    # Adding one diagonal makes triangles, and it stands.
    TrussSolver(nodes, members + [steel(0, 2)]).solve()


def test_extra_loads_from_vehicles():
    nodes = [Node.pinned(0, 0), Node.pinned(0, 1), Node(1, 0)]
    res = TrussSolver(nodes, [steel(0, 2), steel(1, 2)]).solve(extra_loads={2: (0, -P)})
    assert res.members[1].N == pytest.approx(P * math.sqrt(2), rel=REL)


@pytest.mark.parametrize("ratio,expected", [
    (0.0, GREEN), (0.49, GREEN), (0.5, YELLOW), (0.79, YELLOW),
    (0.8, RED), (1.0, RED), (1.01, FAILED)])
def test_colour_bands(ratio, expected):
    assert status_for_ratio(ratio) == expected
