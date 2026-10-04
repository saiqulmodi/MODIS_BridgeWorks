"""Donation Camps: Civil Grants go to a cause, never more than the wallet holds or the camp
still needs; completing a camp gives its badge and EXP; the screen works in both languages."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from engine import donations as D
from game import i18n
from game.app import App
from game.save import Save


@pytest.fixture
def app(tmp_path):
    a = App(save=Save(str(tmp_path / "s.json")), headless=True, show_briefings=False)
    yield a
    i18n.set_lang("en")


def test_no_real_money_is_collected():
    assert D.REAL_DONATIONS_ENABLED is False


def test_every_camp_is_bilingual_and_unique():
    keys = [c.key for c in D.CAMPS]
    assert len(keys) == len(set(keys)) and len(keys) >= 6
    for c in D.CAMPS:
        assert c.target > 0
        for text in (c.name_bn, c.cause_bn, c.badge_bn):
            assert i18n.has_bengali(text)


def test_giving_is_limited_by_wallet_and_target(tmp_path):
    save = Save(str(tmp_path / "s.json"))
    trees = D.camp("riverbank_trees")
    assert save.donate(trees.key, 1000) == (0.0, False, 0)          # empty wallet
    save.add_grant(100000)
    given, done, exp = save.donate(trees.key, 5000)
    assert given == 5000 and not done and exp == 25
    given, done, exp = save.donate(trees.key, 99999)                # only what is still needed
    assert given == trees.target - 5000 and done and exp >= D.EXP_CAMP_COMPLETE
    assert save.donate(trees.key, 1000) == (0.0, False, 0)          # already complete
    assert trees.key in save.donations["badges"]
    assert save.wallet == 100000 - trees.target
    assert save.donated_total() == trees.target
    assert len(save.donations["ledger"]) == 2
    assert Save(str(tmp_path / "s.json")).donated_total() == trees.target     # saved to disk


def test_titles_grow_with_giving():
    assert D.title(0, "en") == "Friend of the Nation"
    assert D.title(30000, "en") == "Citizen Engineer"
    assert i18n.has_bengali(D.title(200000, "bn"))


def test_donation_screen_from_menu_and_academy(app):
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d, mod=0, unicode="d")], 1 / 60)
    sc = app.scene
    assert type(sc).__name__ == "DonationScene"
    sc.give(500)                                    # nothing to give yet: a friendly message
    assert sc.message and not sc.msg_good
    app.save.add_grant(10000)
    sc.give(1000)
    assert app.save.donated_total() == 1000 and sc.msg_good
    for lang in ("en", "bn"):
        i18n.set_lang(lang)
        sc.update(1 / 60)
        sc.draw(app.screen)
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")], 1 / 60)
    assert type(app.scene).__name__ == "MenuScene"
    app.to_academy()
    app.scene.give_btn.click()
    assert type(app.scene).__name__ == "DonationScene"
