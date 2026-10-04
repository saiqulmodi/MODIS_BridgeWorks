"""Drives every screen through its main states (edit, run, failure, success, labs,
selections). Used to collect displayed text and to check translation coverage."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import tempfile

import pygame

from engine.failure import CAUSES
from engine.levels import LEVELS, get
from engine.logistics import Plan, evaluate
from engine.railnet import reference_logic
from game.app import App
from game.rail_sim import RailDesign, ground_height
from game.reference import level1_bad, level1_good, megastructure, viaduct, warren
from game.save import Save
from game.ui import Button


def _draw(app):
    app.scene.draw(app.screen)
    for group in (getattr(app.scene, "widgets", None), getattr(app.scene, "top_buttons", None)):
        if group:
            for w in group.items:
                if isinstance(w, Button) and w.tooltip:
                    from game.i18n import tr
                    tr(w.tooltip)


def _until_overlay(app, n=4000, dt=1 / 30):
    for k in range(n):
        app.scene.update(dt)
        if k % 150 == 0:
            _draw(app)
        if app.scene.overlay is not None:
            break
    _draw(app)
    ov = app.scene.overlay
    if ov is not None:
        for w in ov.widgets.items:
            if isinstance(w, Button) and w.tooltip:
                from game.i18n import tr
                tr(w.tooltip)
    return ov


def _diagnose_and_close(app):
    ov = app.scene.overlay
    if ov is not None and hasattr(ov, "answer"):
        ov.answer(ov.report.correct_cause)
        _draw(app)
    app.scene.overlay = None


def run_all_flows():
    app = App(save=Save(os.path.join(tempfile.mkdtemp(), "s.json")), headless=True, show_briefings=True)
    _draw(app)
    from game.i18n import tr
    for lv in LEVELS:
        for s in (lv.title, lv.tier, lv.mission, lv.context, lv.success, lv.bonus):
            tr(s)
        if lv.alternate:
            tr(lv.alternate["name"])
            tr(lv.alternate["text"])
    for cause, lesson in CAUSES.values():
        tr(cause)
        tr(lesson)

    # --- bridge levels -------------------------------------------------------------------
    designs = {1: [level1_good(), level1_bad()],
               7: [warren(get(7).cfg, 8, 6, mat="Steel", A=0.008, shape="Hollow box")],
               8: [viaduct(get(8).cfg, A_col=0.004, A_diag=0.002, A_deck=0.002)],
               10: [megastructure(get(10).cfg)]}
    for num, ds in designs.items():
        app.start_level(num)
        _draw(app)                       # briefing
        app.scene.overlay = None
        sc = app.scene
        _draw(app)
        for d in ds:
            sc.design = d
            sc.dirty = True
            sc.update(1 / 60)
            _draw(app)
            sc.select(("beam", 1))
            _draw(app)
            sc.select(("joint", 1))
            _draw(app)
            if sc.cfg.get("wind") or sc.cfg.get("quake") or sc.cfg.get("grid_power"):
                sc.toggle_lab()
                sc.update(1 / 60)
                _draw(app)
            sc.vectors = True
            sc.speed = 4
            sc.start_run()
            for _ in range(60):
                sc.update(1 / 30)
            sc.select(("vehicle", 0))
            sc.update(1 / 30)
            _draw(app)
            _until_overlay(app)
            _diagnose_and_close(app)
            sc.reset_after_failure()
            _draw(app)
        # a failure with the alternate route
        if num == 1:
            sc.design = level1_bad()
            sc.start_run()
            _draw(app)
            sc.take_alternate(sc.overlay.report)
            _draw(app)
            app.scene.overlay = None
        if num == 8:
            d = viaduct(get(8).cfg, A_col=0.004, A_diag=0.002, A_deck=0.002)
            d.isolation = True
            sc.design = d
            sc.start_run()
            sc.speed = 4
            _until_overlay(app)
            _diagnose_and_close(app)
            sc.reset_after_failure()
        sc.say("Too long: 9.0 m (max 8 m for this tool)")
        _draw(app)
        sc.say("You can't build inside the rock")
        _draw(app)
        sc.design = level1_bad() if num == 1 else sc.design
        sc.dirty = True
        sc.update(1 / 60)
        _draw(app)

    # --- rail -------------------------------------------------------------------------------
    for num, runs in ((2, [RailDesign(None, "Diesel shunter", 2), RailDesign(None, "Diesel shunter", 4)]),
                      (4, [RailDesign(None, "Mainline diesel", 5, False, 340),
                           RailDesign(None, "Mainline diesel", 5, False, 380)])):
        app.start_level(num)
        _draw(app)
        app.scene.overlay = None
        sc = app.scene
        cfg = get(num).cfg
        for d in runs:
            d.heights = [ground_height(cfg, x) for x in cfg["stations"]]
            sc.design = d
            sc.select_train()
            _draw(app)
            sc.selected_seg = 3
            sc.drawer.show("Track", sc.segment_cards(3))
            _draw(app)
            sc.speed = 4
            sc.toggle_run()
            for _ in range(60):
                sc.update(1 / 30)
            _draw(app)
            _until_overlay(app, 20000)
            _diagnose_and_close(app)
            sc.reset_after_failure()
            _draw(app)

    # --- cantilever ---------------------------------------------------------------------------
    app.start_level(3)
    _draw(app)
    app.scene.overlay = None
    sc = app.scene
    _draw(app)
    sc.cast(0, -1)
    sc.cast(0, -1)
    sc.cast(0, -1)
    sc.cast(0, -1)
    _draw(app)
    _diagnose_and_close(app)
    sc.reset_after_failure()
    sc.stitch()
    _draw(app)
    sc.tie(0)
    sc.tie(1)
    b = sc.bridge
    for k in range(6):
        for p in (0, 1):
            for s in (-1, 1):
                if not b.arm_complete(p, s) and k < b.arm_segments_needed(p, s):
                    sc.cast(p, s)
    sc._set_pt(1)
    sc.stitch()
    _draw(app)
    sc.start_truck()
    for _ in range(30):
        sc.update(1 / 30)
    _draw(app)
    _until_overlay(app)
    app.scene.overlay = None

    # --- signals --------------------------------------------------------------------------------
    for logic, slots in ((None, set()), (reference_logic(), {400.0})):
        app.start_level(5)
        _draw(app)
        app.scene.overlay = None
        sc = app.scene
        if logic:
            sc.logic = logic
            sc._build_logic()
        sc.eb_slots, sc.wb_slots = set(slots), set(slots)
        sc.show_info()
        _draw(app)
        sc.toggle_aspect()
        _draw(app)
        sc.toggle_aspect()
        sc.speed = 16
        sc.toggle_run()
        for _ in range(100):
            sc.update(1 / 30)
        _draw(app)
        _until_overlay(app, 20000)
        _diagnose_and_close(app)

    # --- traffic --------------------------------------------------------------------------------
    for mode, cyc, split in (("signals", 60, 0.5), ("roundabout", 60, 0.5), ("overpass", 60, 0.5)):
        app.start_level(6)
        _draw(app)
        app.scene.overlay = None
        sc = app.scene
        sc.mode_name, sc.cycle, sc.split = mode, cyc, split
        sc.show_panel()
        _draw(app)
        sc.mode_cycler._next()
        _draw(app)
        sc.mode_name = mode
        sc.speed = 16
        sc.toggle_run()
        for _ in range(200):
            sc.update(1 / 30)
        _draw(app)
        _until_overlay(app, 20000)
        _diagnose_and_close(app)

    # --- logistics ------------------------------------------------------------------------------
    for plan in (Plan(0, 5000, 1000, 0, 1, 30, 1), Plan(0, 6000, 0, 0, 2, 40, 0), Plan(0, 0, 6000, 0, 0, 30, 2)):
        app.start_level(9)
        _draw(app)
        app.scene.overlay = None
        sc = app.scene
        sc.plan = plan
        sc.result = evaluate(plan)
        sc.drawer.update_cards(sc.cards())
        sc.optimize()
        _draw(app)
        sc.toggle_run()
        for _ in range(30):
            sc.update(1 / 30)
        _draw(app)
        _until_overlay(app, 5000)
        _diagnose_and_close(app)
    app.to_menu()
    _draw(app)
    return app
