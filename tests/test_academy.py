"""BridgeWorks Academy: the question bank is well formed in both languages, grants are paid
once, they cover a shortfall before any loan, reading pays, and the Black Box challenge
raises salvage to 75%."""
import collections
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from engine import finance as F
from engine.academy import CLASSES, SUBJECTS
from engine.academy_data import all_items, by_id, export_json, grant_reward, items
from engine.academy_skills import items as skill_items
from engine.failure import FailureReport
from game import i18n
from game.app import App
from game.save import Save

BANK = all_items() + skill_items()


@pytest.fixture
def app(tmp_path):
    a = App(save=Save(str(tmp_path / "s.json")), headless=True, show_briefings=False)
    yield a
    i18n.set_lang("en")


def key(k):
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_every_question_is_complete_in_both_languages():
    assert BANK, "no questions written yet"
    for r in BANK:
        assert r["question"].strip() and r["explanation"].strip(), r["id"]
        assert len(r["options"]) == 4 and len(r["options_bn"]) == 4, r["id"]
        assert all(o.strip() for o in r["options"] + r["options_bn"]), r["id"]
        assert len(set(r["options"])) == 4 and len(set(r["options_bn"])) == 4, r["question"]
        assert 0 <= r["correct_idx"] <= 3
        for k in ("question_bn", "explanation_bn"):
            assert i18n.has_bengali(r[k]), (r["id"], k)
        for k in ("question", "explanation"):
            assert not i18n.has_bengali(r[k]), (r["id"], k)


def test_batches_hold_at_most_100_and_no_question_repeats():
    for c in CLASSES:
        for s in SUBJECTS:
            assert len(items(c, s)) <= 100, (c, s)
    for group in (all_items(), skill_items()):
        qs = collections.Counter(r["question"] for r in group)
        assert not [q for q, n in qs.items() if n > 1]


def test_right_answers_are_spread_over_all_four_positions():
    counts = collections.Counter(r["correct_idx"] for r in BANK)
    assert min(counts[k] for k in range(4)) > 0.15 * len(BANK)


def test_ids_are_stable_and_findable(tmp_path):
    for r in all_items()[:50]:
        assert by_id(r["id"]) == r
    export_json(str(tmp_path / "bank.json"))
    assert (tmp_path / "bank.json").stat().st_size > 1000


def test_grant_is_paid_once_on_a_right_first_answer(tmp_path):
    save = Save(str(tmp_path / "s.json"))
    r, r2 = all_items()[:2]
    assert save.answer_question(r["id"], True, r["grant_reward"]) == grant_reward(r["class_level"])
    assert save.answer_question(r["id"], True, r["grant_reward"]) == 0.0      # no farming
    assert save.answer_question(r2["id"], False, r2["grant_reward"]) == 0.0
    assert save.answer_question(r2["id"], True, r2["grant_reward"]) == 0.0    # the first try decides
    assert save.explanation_read(r2["id"], 200.0) == 200.0
    assert save.explanation_read(r2["id"], 200.0) == 0.0
    assert save.wallet == grant_reward(r["class_level"]) + 200.0


def test_grant_covers_the_shortfall_before_any_loan():
    p = F.business_plan(1, 250000, 300000, grant=20000)
    assert p.grant_used == 20000 and p.loan == pytest.approx(30000)
    p = F.business_plan(1, 250000, 300000, grant=80000)
    assert p.grant_used == 50000 and p.loan == 0 and p.viable


def test_over_budget_bridge_uses_the_grant_and_gets_it_back_for_a_new_attempt(app):
    from engine.levels import get
    from game.reference import warren
    start = 2_000_000.0
    app.save.add_grant(start)
    app.start_level(1)
    sc = app.scene
    sc.design = warren(get(1).cfg, 8, 3.0, mat="Steel", A=0.02, shape="Hollow box")
    sc.dirty = True
    sc.update(1 / 60)
    shortfall = sc.cost() - sc.budget
    assert shortfall > 0
    sc.toggle_run()
    ov = sc.overlay
    assert ov.plan.grant_used == pytest.approx(shortfall) and ov.plan.loan == 0
    ov.accept()
    assert app.save.wallet == pytest.approx(start - shortfall)
    if sc.mode != "edit":
        sc.stop_run()
    sc.overlay = None
    sc.finance_gate(lambda: None)        # a new attempt first gives the unspent grant back
    assert app.save.wallet == pytest.approx(start)


def test_academy_challenge_raises_salvage_to_75_percent():
    rep = FailureReport("yield", "x", "y", build_cost=100000)
    assert rep.salvage == pytest.approx(30000)
    rep.academy_bonus = True
    assert rep.salvage == pytest.approx(75000)


def test_black_box_offers_the_academy_challenge(app):
    from game.academy_ui import AcademyChallenge
    from game.common import BlackBox
    app.start_level(1)
    sc = app.scene
    sc.fail(FailureReport("yield", "BEAM SNAPPED", "sigma > limit", build_cost=100000))
    bb = sc.overlay
    assert isinstance(bb, BlackBox) and bb.challenge_btn.visible
    bb.challenge()
    ch = sc.overlay
    assert isinstance(ch, AcademyChallenge)
    card = ch.card
    ch.handle(key(pygame.K_1 + card.order.index(card.r["correct_idx"])))
    assert bb.report.academy_bonus and bb.report.salvage == pytest.approx(75000)
    ch.back()
    assert sc.overlay is bb
    bb.update(0)
    assert "75" in bb.retry_btn.label or "0.75" in bb.retry_btn.label


def test_academy_screen_answers_reads_and_pays(app):
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, mod=0, unicode="a")], 1 / 60)
    sc = app.scene
    sc.pick_class(1)
    sc.pick_subject("physics")
    card = sc.card
    assert card is not None
    app.frame([key(pygame.K_1 + card.order.index(card.r["correct_idx"]))], 1 / 60)
    assert card.answered and card.correct
    assert app.save.wallet == grant_reward(1)
    for _ in range(40 * 30):
        app.frame([], 1 / 30)
    assert app.save.wallet == grant_reward(1) + 200.0       # reading bonus after the explanation
    app.frame([key(pygame.K_RETURN)], 1 / 60)
    assert sc.card is not card
    for lang in ("en", "bn"):
        i18n.set_lang(lang)
        sc.update(1 / 60)
        sc.draw(app.screen)
    sc.pick_subject("daily")
    assert sc.daily and len(sc.daily) <= 5
    sc.draw(app.screen)
    app.frame([key(pygame.K_ESCAPE)], 1 / 60)
    assert type(app.scene).__name__ == "MenuScene"


def test_help_pays_for_reading_an_answer(app):
    from game.help_screen import STATE
    STATE.update(section=0, scroll=0, query="")      # Help remembers its last view
    app.scene.open_help()
    for _ in range(60 * 30):
        app.scene.update(1 / 30)
    assert app.save.wallet >= 500.0
    assert app.save.academy["read_help"]
