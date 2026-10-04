"""Bank loans: offered before building when over budget, approved only with a 50% margin."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

from engine.levels import get
from engine.logistics import Plan, evaluate
from game.app import App
from game.common import Results
from game.finance_ui import FinanceOverlay
from game.reference import warren
from game.save import Save


@pytest.fixture
def app(tmp_path):
    return App(save=Save(str(tmp_path / "save.json")), headless=True, show_briefings=False)


def play(app, n=6000):
    sc = app.scene
    for k in range(n):
        sc.update(1 / 30)
        if sc.overlay is not None:
            sc.draw(app.screen)
            return sc.overlay
    raise AssertionError("never finished")


def level1_with(app, A, panels, h):
    app.start_level(1)
    sc = app.scene
    sc.design = warren(get(1).cfg, panels, h, mat="Steel", A=A, shape="Hollow box")
    sc.dirty = True
    sc.update(1 / 60)
    return sc


def test_inside_budget_builds_without_asking(app):
    sc = level1_with(app, 0.001, 4, 3.0)
    assert sc.cost() <= sc.budget
    sc.toggle_run()
    assert sc.overlay is None and sc.mode == "run" and sc.loan == 0


def test_over_budget_shows_business_plan_before_building(app):
    sc = level1_with(app, 0.008, 8, 2.0)
    budget = sc.budget
    assert sc.cost() > budget
    sc.toggle_run()
    ov = sc.overlay
    assert isinstance(ov, FinanceOverlay) and ov.mode == "loan"
    assert sc.mode == "edit" and sc.loan == 0            # nothing built or borrowed yet
    sc.draw(app.screen)
    assert ov.plan.viable and ov.plan.coverage >= 1.5
    ov.accept()
    assert sc.loan == pytest.approx(sc.cost() - budget)
    assert sc.mode == "run"
    res = play(app)
    assert isinstance(res, Results)
    labels = [l for l, _, _ in res.info["lines"]]
    assert "Bank loan (2%, 10 yr)" in labels and "Investment recovered" in labels
    assert res.info["stars"] <= 2                      # a loan-financed build is over par


def test_bank_refuses_without_a_50_percent_margin(app):
    sc = level1_with(app, 0.02, 8, 3.0)
    sc.toggle_run()
    ov = sc.overlay
    ov.update(0)
    assert not ov.plan.viable and not ov.take_btn.enabled
    ov.accept()                                        # pressing anyway does nothing
    assert sc.overlay is ov and sc.mode == "edit" and sc.loan == 0
    ov.close()
    assert sc.overlay is None and sc.mode == "edit"


def test_higher_toll_improves_coverage(app):
    sc = level1_with(app, 0.008, 8, 2.0)
    sc.toggle_run()
    ov = sc.overlay
    c1 = ov.plan.coverage
    ov._set_toll(1.5)
    assert ov.plan.coverage > c1 and ov.plan.users_day < FinanceOverlay(sc, "view").plan.users_day * 1.0001


def test_government_subsidised_loan(app):
    sc = level1_with(app, 0.008, 8, 2.0)
    sc.toggle_run()
    ov = sc.overlay
    bank_only = ov.plan.payment
    ov.govt_btn.click()
    assert sc.govt_loan and ov.plan.govt_loan > 0 and ov.plan.payment < bank_only
    ov.update(0)
    sc.draw(app.screen)
    ov.accept()
    res = play(app)
    labels = [l for l, _, _ in res.info["lines"]]
    assert "Govt loan (0.5%, 15 yr)" in labels


def test_logistics_loan_for_a_truck_fleet(app):
    app.start_level(9)
    sc = app.scene
    sc.plan = Plan(6000, 0, 0, 200)
    sc.result = evaluate(sc.plan)
    assert sc.cost() > sc.budget
    sc.toggle_run()
    assert isinstance(sc.overlay, FinanceOverlay)
    sc.overlay.accept()
    assert isinstance(play(app), Results)


def test_finance_button_opens_the_plan_in_every_level(app):
    for n in range(1, 11):
        app.start_level(n)
        sc = app.scene
        sc.show_finance()
        assert isinstance(sc.overlay, FinanceOverlay) and sc.overlay.mode == "view"
        sc.draw(app.screen)
