"""End-to-end level tests: a good design wins (within budget), bad designs fail for the
right reason - played through the real level screens, headless."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

from engine.levels import get
from engine.railnet import reference_logic
from engine.logistics import Plan, evaluate
from game.app import App
from game.common import BlackBox, Results
from game.rail_sim import RailDesign, ground_height
from game.reference import level1_bad, level1_good, level1_weak, megastructure, viaduct, warren
from game.save import Save


@pytest.fixture
def app(tmp_path):
    return App(save=Save(str(tmp_path / "save.json")), headless=True, show_briefings=False)


def play(app, max_updates=6000, dt=1 / 30):
    """Advance the scene until an overlay (results or black box) appears."""
    sc = app.scene
    for k in range(max_updates):
        sc.update(dt)
        if k % 200 == 0:
            sc.draw(app.screen)
        if sc.overlay is not None:
            sc.draw(app.screen)
            return sc.overlay
    raise AssertionError("level never finished")


def bridge(app, num, design):
    app.start_level(num)
    sc = app.scene
    sc.design = design
    sc.speed = 4
    sc.start_run()
    return play(app)


def assert_win(ov, min_stars=1):
    assert isinstance(ov, Results), getattr(ov, "report", None) and ov.report.title
    assert ov.info["stars"] >= min_stars


def assert_fail(ov, *kinds):
    assert isinstance(ov, BlackBox), "expected a failure"
    assert ov.report.kind in kinds, (ov.report.kind, ov.report.title)


# --- Level 1 ---------------------------------------------------------------------------------
def test_l1_good_bridge_wins(app):
    assert_win(bridge(app, 1, level1_good()))


def test_l1_flat_road_folds(app):
    assert_fail(bridge(app, 1, level1_bad()), "unstable")


def test_l1_thin_timber_buckles(app):
    assert_fail(bridge(app, 1, level1_weak()), "buckling", "yield")


def test_l1_cheap_timber_box_gets_three_stars(app):
    d = warren(get(1).cfg, 2, 3.0, mat="Timber", A=0.008, shape="Hollow box")
    assert_win(bridge(app, 1, d), 3)


# --- Level 7 ---------------------------------------------------------------------------------
def test_l7_plain_bridge_resonates(app):
    d = warren(get(7).cfg, 8, 6, mat="Steel", A=0.008, shape="Hollow box")
    assert_fail(bridge(app, 7, d), "resonance", "buckling", "yield")


def test_l7_fairings_save_it(app):
    d = warren(get(7).cfg, 8, 6, mat="Steel", A=0.008, shape="Hollow box")
    d.fairing = True
    assert_win(bridge(app, 7, d), 2)


def test_l7_tuned_mass_damper_saves_it(app):
    d = warren(get(7).cfg, 8, 6, mat="Steel", A=0.008, shape="Hollow box")
    d.tmd = True
    assert_win(bridge(app, 7, d))


# --- Level 8 ---------------------------------------------------------------------------------
def test_l8_light_viaduct_fails_in_quake(app):
    d = viaduct(get(8).cfg, A_col=0.004, A_diag=0.002, A_deck=0.002)
    assert_fail(bridge(app, 8, d), "buckling", "seismic", "yield")


def test_l8_isolation_without_joints_pounds(app):
    d = viaduct(get(8).cfg, A_col=0.004, A_diag=0.002, A_deck=0.002)
    d.isolation = True
    assert_fail(bridge(app, 8, d), "pounding")


def test_l8_isolation_with_joints_wins(app):
    d = viaduct(get(8).cfg, A_col=0.004, A_diag=0.002, A_deck=0.002)
    d.isolation = d.flex_joints = True
    assert_win(bridge(app, 8, d), 3)


def test_l8_braced_viaduct_wins(app):
    assert_win(bridge(app, 8, viaduct(get(8).cfg)))


# --- Level 10 --------------------------------------------------------------------------------
def test_l10_megastructure_wins(app):
    assert_win(bridge(app, 10, megastructure(get(10).cfg)))


def test_l10_weak_grid_is_too_slow(app):
    d = megastructure(get(10).cfg)
    d.grid_mw = 0.5
    assert_fail(bridge(app, 10, d), "timeout", "brownout")


def test_l10_unpropped_truss_fails(app):
    d = warren(get(10).cfg, 16, 6, mat="Steel", A=0.004, shape="Hollow box")
    assert_fail(bridge(app, 10, d), "buckling", "yield")


# --- Levels 2 and 4 (rail) ---------------------------------------------------------------------
def rail(app, num, design):
    app.start_level(num)
    sc = app.scene
    sc.design = design
    sc.speed = 4
    sc.toggle_run()
    return play(app, 20000)


def ground(num):
    cfg = get(num).cfg
    return [ground_height(cfg, x) for x in cfg["stations"]]


def test_l2_shunter_two_wagons_wins(app):
    assert_win(rail(app, 2, RailDesign(ground(2), "Diesel shunter", 2)), 2)


def test_l2_overloaded_shunter_stalls(app):
    assert_fail(rail(app, 2, RailDesign(ground(2), "Diesel shunter", 4)), "stall")


def test_l2_banker_hauls_everything(app):
    assert_win(rail(app, 2, RailDesign(ground(2), "Diesel shunter", 4, banker=True)))


def test_l4_good_braking_point_wins(app):
    assert_win(rail(app, 4, RailDesign(ground(4), "Mainline diesel", 5, False, 340)), 2)


def test_l4_late_braking_hits_buffers(app):
    assert_fail(rail(app, 4, RailDesign(ground(4), "Mainline diesel", 5, False, 380)), "overrun")


def test_l4_heavy_train_stalls_on_single_loco(app):
    assert_fail(rail(app, 4, RailDesign(ground(4), "Mainline diesel", 10, False, 340)), "stall")


# --- Level 3 (cantilever) ----------------------------------------------------------------------
def build_cantilever(sc, ties=True, d_tip=2.0):
    b = sc.bridge
    b.d_pier, b.d_tip = 3.5, d_tip
    if ties:
        sc.tie(0)
        sc.tie(1)
    for k in range(6):
        for p in (0, 1):
            for s in (-1, 1):
                if k < b.arm_segments_needed(p, s):
                    sc.cast(p, s)
                    if sc.overlay is not None:
                        return False
    return True


def test_l3_slim_tip_wins_two_stars(app):
    app.start_level(3)
    sc = app.scene
    assert build_cantilever(sc)
    sc._set_pt(1)
    sc.stitch()
    sc.start_truck()
    assert_win(play(app), 2)


def test_l3_deeper_tip_wins_three_stars(app):
    app.start_level(3)
    sc = app.scene
    assert build_cantilever(sc, d_tip=2.5)
    sc._set_pt(1)
    sc.stitch()
    sc.start_truck()
    assert_win(play(app), 3)


def test_l3_no_tie_downs_tips_over(app):
    app.start_level(3)
    sc = app.scene
    assert not build_cantilever(sc, ties=False)
    assert_fail(sc.overlay, "overturn")


def test_l3_no_post_tensioning_cracks(app):
    app.start_level(3)
    sc = app.scene
    assert build_cantilever(sc)
    sc._set_pt(0)
    sc.stitch()
    sc.start_truck()
    assert_fail(play(app), "girder")


# --- Level 5 (signals) -------------------------------------------------------------------------
def test_l5_reference_interlocking_wins(app):
    app.start_level(5)
    sc = app.scene
    sc.logic = reference_logic()
    sc.eb_slots, sc.wb_slots = {400.0}, {400.0}
    sc.speed = 16
    sc.toggle_run()
    assert_win(play(app, 20000))


def test_l5_starter_logic_fails(app):
    app.start_level(5)
    sc = app.scene
    sc.speed = 16
    sc.toggle_run()
    assert_fail(play(app, 20000), "crossing", "collision", "derail")


def test_l5_short_blocks_cause_a_crash(app):
    app.start_level(5)
    sc = app.scene
    sc.logic = reference_logic()
    sc.eb_slots, sc.wb_slots = {200.0, 400.0, 600.0}, {200.0, 400.0, 600.0}
    sc.speed = 16
    sc.toggle_run()
    assert_fail(play(app, 20000), "collision")


# --- Level 6 (traffic) -------------------------------------------------------------------------
def traffic(app, mode, cycle=60, split=0.5):
    app.start_level(6)
    sc = app.scene
    sc.mode_name, sc.cycle, sc.split = mode, cycle, split
    sc.speed = 16
    sc.toggle_run()
    return play(app, 20000)


def test_l6_even_split_gridlocks(app):
    assert_fail(traffic(app, "signals"), "gridlock")


def test_l6_tuned_signals_win(app):
    assert_win(traffic(app, "signals", 90, 0.7))


def test_l6_roundabout_wins(app):
    assert_win(traffic(app, "roundabout"))


def test_l6_overpass_wins(app):
    assert_win(traffic(app, "overpass"))


# --- Level 9 (logistics) -----------------------------------------------------------------------
def logistics(app, plan):
    app.start_level(9)
    sc = app.scene
    sc.plan = plan
    sc.result = evaluate(plan)
    sc.toggle_run()
    return play(app, 5000)


def test_l9_rail_and_barge_mix_wins_three_stars(app):
    assert_win(logistics(app, Plan(0, 5000, 1000, 0, 1, 30, 1)), 3)


def test_l9_all_road_wins_but_scores_lower(app):
    ov = logistics(app, Plan(6000, 0, 0, 60, 0, 30, 0))
    assert_win(ov)
    assert ov.info["stars"] < 3


def test_l9_too_many_wagons_stall(app):
    assert_fail(logistics(app, Plan(0, 6000, 0, 0, 2, 40, 0)), "stall")


def test_l9_slow_barges_miss_deadline(app):
    assert_fail(logistics(app, Plan(0, 0, 6000, 0, 0, 30, 2)), "timeout")
