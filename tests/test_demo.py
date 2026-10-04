"""Paid demonstrations: warning first, budget cut only after 'Yes', demo wins, design restored,
replays are free, and demos never award stars."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import copy

import pytest

from game.app import App
from game.demo import DEMO_FRACTION, ConfirmDemo, DemoDone
from game.save import Save


@pytest.fixture
def app(tmp_path):
    return App(save=Save(str(tmp_path / "save.json")), headless=True, show_briefings=False)


def play_until_overlay(app, n=30000):
    sc = app.scene
    for k in range(n):
        sc.update(1 / 30)
        if k % 300 == 0:
            sc.draw(app.screen)
        if sc.overlay is not None:
            sc.draw(app.screen)
            return sc.overlay
    raise AssertionError("demo never finished")


@pytest.mark.parametrize("num", range(1, 11))
def test_demo_warns_charges_wins_and_restores(app, num):
    app.start_level(num)
    sc = app.scene
    full = sc.budget
    before = copy.deepcopy({a: getattr(sc, a) for a in sc.DEMO_STATE})

    # 1. clicking Demo only shows the warning - nothing is charged yet
    sc.demo_clicked()
    assert isinstance(sc.overlay, ConfirmDemo)
    sc.draw(app.screen)
    assert sc.budget == full

    # 2. "No, keep my budget" leaves everything alone
    sc.overlay.close()
    assert sc.overlay is None and sc.budget == full and not sc.demo_active

    # 3. pay: budget drops by exactly the advertised amount, and it is saved
    sc.demo_clicked()
    sc.pay_and_start_demo()
    assert sc.budget == pytest.approx(full - DEMO_FRACTION * sc.level.budget)
    assert app.save.level(num)["demo_paid"]
    assert sc.demo_active
    assert sc.cost() <= sc.budget, "the demo design must fit the reduced budget"
    sc.draw(app.screen)

    # 4. the demonstration wins, with no stars or EXP
    exp = app.save.exp
    ov = play_until_overlay(app)
    assert isinstance(ov, DemoDone) and ov.worked
    assert app.save.exp == exp and app.save.level(num)["stars"] == 0

    # 5. back to my design
    sc.end_demo(restore=True)
    assert not sc.demo_active and sc.overlay is None
    for k, v in before.items():
        assert type(getattr(sc, k)) is type(v)
    sc.draw(app.screen)

    # 6. replay is free - no second warning, no second charge
    cut = sc.budget
    sc.demo_clicked()
    assert not isinstance(sc.overlay, ConfirmDemo)
    assert sc.demo_active and sc.budget == cut
    sc.end_demo(restore=False)


def test_budget_cut_survives_restart(tmp_path):
    path = str(tmp_path / "save.json")
    app = App(save=Save(path), headless=True, show_briefings=False)
    app.start_level(1)
    full = app.scene.budget
    app.scene.demo_clicked()
    app.scene.pay_and_start_demo()
    app2 = App(save=Save(path), headless=True, show_briefings=False)
    app2.start_level(1)
    assert app2.scene.budget == pytest.approx(full * (1 - DEMO_FRACTION))
