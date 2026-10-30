"""Each build project can be won with a sensible design, and weak designs fail."""
from engine import materials as M
from game.projects import PROJECTS, SIZE_COST, Design


def build(pid, members):
    d = Design(PROJECTS[pid - 1])
    d.parts = 10_000
    for i, j, mat, size in members:
        assert d.add(i, j, mat, size) == ""
    return d


def p1(size):
    return [(5, 1, M.STEEL_CABLE, size), (5, 2, M.STEEL_CABLE, size), (6, 3, M.STEEL_CABLE, size)]


def p2(mat, size, post_size=None):
    top = [(7, 8), (8, 9), (9, 10), (10, 11)]
    ends = [(0, 7), (6, 11)]
    verts = [(1, 7), (2, 8), (3, 9), (4, 10), (5, 11)]
    diags = [(7, 2), (8, 3), (10, 3), (11, 4)]
    return ([(i, j, mat, post_size or size) for i, j in ends]
            + [(i, j, mat, size) for i, j in top + verts + diags])


def p3(arch_mat, arch_size, hanger_size, hanger_mat=M.STEEL):
    arch = [(0, 9)] + [(k, k + 1) for k in range(9, 15)] + [(15, 8)]
    hangers = [(k, k - 8) for k in range(9, 16)]
    braces = [(9, 2), (10, 3), (11, 4), (13, 4), (14, 5), (15, 6)]
    return ([(i, j, arch_mat, arch_size) for i, j in arch]
            + [(i, j, hanger_mat, hanger_size) for i, j in hangers]
            + [(i, j, M.STEEL, "L") for i, j in braces])


def p4(size):
    top = 14
    return [(top, k, M.STEEL_CABLE, size) for k in (0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12)]


def p5(size, mat=M.CARBON_CABLE):
    t1, t2 = 18, 20
    stays = [(t1, k) for k in (0, 1, 2, 3, 5, 6, 7, 8)] + [(t2, k) for k in (8, 9, 10, 11, 13, 14, 15, 16)]
    return [(i, j, mat, size) for i, j in stays] + [(t1, t2, M.STEEL_CABLE, "M")]


CASES = {
    1: (p1("S"), None),
    2: (p2(M.STEEL, "M", post_size="L"), p2(M.STEEL, "M")),
    3: (p3(M.STEEL, "L", "S"), p3(M.CONCRETE, "L", "S")),
    4: (p4("M"), p4("S")),
    5: (p5("M"), p5("S", M.STEEL_CABLE)),
}


def test_good_designs_pass_and_weak_fail():
    for pid, (good, weak) in CASES.items():
        ok, msg, worst = build(pid, good).full_test()
        assert ok, (pid, msg, worst)
        if weak:
            ok, msg, worst = build(pid, weak).full_test()
            assert not ok, (pid, "weak design should fail", worst)


def test_empty_bridge_is_unstable_and_parts_are_spent():
    for p in PROJECTS:
        ok, msg, _ = Design(p).full_test()
        assert not ok
    d = Design(PROJECTS[0])
    assert d.add(5, 1, M.STEEL_CABLE, "M") != ""      # no parts yet
    d.parts = 4
    assert d.add(5, 1, M.STEEL_CABLE, "M") == "" and d.parts == 4 - SIZE_COST["M"]
    d.remove(0)
    assert d.parts == 4
