"""Known-good (and known-bad) designs for every level.

Used by the automated tests to prove each level can be won within budget and that bad
ideas fail for the right reason. They are not shown to the player.
"""
from engine.levels import get
from game.bridge_sim import new_design


def warren(cfg, panels, height, mat="Steel", A=0.002, shape="I-beam", deck_mat=None, deck_A=None,
           below=False, design=None):
    """Classic Warren truss across the gap: deck along the bottom, triangles above
    (or below the deck when below=True)."""
    d = design or new_design(cfg)
    x0, x1, y = cfg["left_x"], cfg["right_x"], cfg["deck_y"]
    w = (x1 - x0) / panels
    deck_mat = deck_mat or mat
    deck_A = deck_A or A
    h = -height if below else height
    for k in range(panels):
        a = (x0 + k * w, y)
        b = (x0 + (k + 1) * w, y)
        top = (x0 + (k + 0.5) * w, y + h)
        d.add_beam(a, b, deck_mat, deck_A, shape, "deck")
        d.add_beam(a, top, mat, A, shape)
        d.add_beam(top, b, mat, A, shape)
        if k < panels - 1:
            d.add_beam(top, (x0 + (k + 1.5) * w, y + h), mat, A, shape)
    return d


def pratt(cfg, panels, height, mat="Steel", A=0.002, shape="I-beam", chord_A=None, design=None):
    """Pratt truss: verticals plus diagonals, top chord between the end posts."""
    d = design or new_design(cfg)
    x0, x1, y = cfg["left_x"], cfg["right_x"], cfg["deck_y"]
    w = (x1 - x0) / panels
    chord_A = chord_A or A
    for k in range(panels):
        a, b = (x0 + k * w, y), (x0 + (k + 1) * w, y)
        d.add_beam(a, b, mat, chord_A, shape, "deck")
        ta, tb = (x0 + k * w, y + height), (x0 + (k + 1) * w, y + height)
        d.add_beam(ta, tb, mat, chord_A, shape)
        d.add_beam(a, ta, mat, A, shape)
        if k < panels / 2:
            d.add_beam(a, tb, mat, A, shape)
        else:
            d.add_beam(ta, b, mat, A, shape)
    d.add_beam((x1, y), (x1, y + height), mat, A, shape)
    return d


def viaduct(cfg, A_col=0.008, A_diag=0.004, A_deck=0.004, mat="Steel", shape="Hollow box",
            x_braced=False):
    """Deck on columns every 4 m, each bay braced by a diagonal (or an X)."""
    d = new_design(cfg)
    x0, x1, y = cfg["left_x"], cfg["right_x"], cfg["deck_y"]
    gy = cfg["extra_anchor_y"]
    xs = list(range(int(x0), int(x1) + 1, 4))
    for a, b in zip(xs, xs[1:]):
        d.add_beam((a, y), (b, y), mat, A_deck, shape, "deck")
    cols = cfg["extra_anchor_xs"]
    for x in cols:
        d.add_beam((x, y), (x, gy), mat, A_col, shape)
    for a, b in zip(cols, cols[1:]):
        d.add_beam((a, y), (b, gy), mat, A_diag, shape)
        if x_braced:
            d.add_beam((b, y), (a, gy), mat, A_diag, shape)
    return d


def megastructure(cfg, A=0.004, A_pier=0.008, mat="Steel", height=6.0, cables=None, A_cable=0.002):
    """Deck truss over the strait, propped by V-piers on both rock islands, optionally with
    cable stays from tower tops."""
    d = warren(cfg, 16, height, mat=mat, A=A, shape="Hollow box")
    gy = cfg["extra_anchor_y"]
    for xa, xb in ((26, 28), (52, 54)):
        # deck joints over the islands are at x = 24, 28, 52, 56 (4 m grid)
        top = 28 if xa == 26 else 52
        d.add_beam((top, 0), (xa, gy), mat, A_pier, "Hollow box")
        d.add_beam((top, 0), (xb, gy), mat, A_pier, "Hollow box")
        d.add_beam((xa, gy), (top - 4 if xa == 26 else top + 4, 0), mat, A_pier, "Hollow box")
    if cables:
        for (x0, y0), (x1, y1) in cables:
            d.add_beam((x0, y0), (x1, y1), cables_material(cables), A_cable, "Solid square", "cable")
    return d


def cables_material(_):
    return "Carbon-fibre cable"


def demo_bridge_design(num):
    """The design each bridge level's demonstration shows."""
    cfg = get(num).cfg
    if num == 1:
        return warren(cfg, 2, 3.0, mat="Timber", A=0.008, shape="Hollow box")
    if num == 7:
        d = warren(cfg, 8, 6, mat="Steel", A=0.008, shape="Hollow box")
        d.fairing = True
        return d
    if num == 8:
        d = viaduct(cfg, A_col=0.004, A_diag=0.002, A_deck=0.002)
        d.isolation = d.flex_joints = True
        return d
    if num == 10:
        return megastructure(cfg)
    raise ValueError(num)


def level1_good():
    cfg = get(1).cfg
    return warren(cfg, 4, 3.0, mat="Steel", A=0.001, shape="I-beam")


def level1_bad():
    """Only a flat road - no triangles."""
    cfg = get(1).cfg
    d = new_design(cfg)
    for k in range(4):
        d.add_beam((12 + 4 * k, 0), (16 + 4 * k, 0), "Timber", 0.004, "Solid square", "deck")
    return d


def level1_weak():
    """Triangles, but thin solid timber: the top chord buckles."""
    cfg = get(1).cfg
    return warren(cfg, 2, 2.0, mat="Timber", A=0.001, shape="Solid square")
