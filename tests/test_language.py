"""English / Bengali: every screen is fully translated, and the switch works and is remembered."""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

sys.path.insert(0, os.path.dirname(__file__))

from game import i18n
from game.app import App
from game.save import Save


@pytest.fixture(autouse=True)
def back_to_english():
    yield
    i18n.set_lang("en")


def test_every_displayed_string_is_translated_to_bengali(monkeypatch):
    import flows
    import game.app
    real = i18n.set_lang
    monkeypatch.setattr(game.app.i18n, "set_lang", lambda code: real("bn"))
    real("bn")
    i18n.start_recording()
    flows.run_all_flows()
    shown = i18n.stop_recording()
    real("bn")
    missing = sorted(s for s in shown if i18n.untranslated(s))
    assert not missing, "Untranslated in Bengali mode:\n" + "\n".join(missing[:40])
    assert len(shown) > 800          # the flows really visited the whole game


def test_every_help_idea_has_bengali():
    from game.help_texts import all_texts
    i18n.set_lang("bn")
    missing = [t for t in all_texts() + ["IDEA"] if not i18n.has_bengali(i18n.tr(t))]
    assert not missing, missing


def test_bottom_buttons_explain_themselves(tmp_path):
    """Every bottom-bar button in every level has an IDEA; clicking one shows it."""
    from game.ui import HINT, Button
    app = App(save=Save(str(tmp_path / "s.json")), headless=True, show_briefings=False)
    for num in range(1, 11):
        app.start_level(num)
        sc = app.scene
        for w in sc.widgets.items:
            if isinstance(w, Button):
                assert w.help_text(), f"level {num}: '{w.label}' has no help"
        btn = next(w for w in sc.widgets.items if isinstance(w, Button) and w.label != "RUN")
        HINT["ttl"] = 0
        app.frame([pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=btn.rect.center, button=1)], 1 / 60)
        assert HINT["ttl"] > 0 and HINT["text"] == btn.help_text()
        # hovering also shows it (drawn without errors)
        app.frame([pygame.event.Event(pygame.MOUSEMOTION, pos=btn.rect.center, rel=(0, 0),
                                      buttons=(0, 0, 0))], 1 / 60)
        if sc.overlay is not None:
            sc.overlay = None


def test_patterns_keep_numbers_and_formulas():
    i18n.set_lang("bn")
    assert i18n.tr("Cost Rs 1.50 L / Rs 2.50 L") == "খরচ Rs 1.50 L / Rs 2.50 L"
    assert i18n.tr("N = -36.3 kN  COMPRESSION (pushed)") == "N = -36.3 kN  চাপ (ঠেলা হচ্ছে)"
    assert i18n.tr("sigma = N / A") == "sigma = N / A"
    assert i18n.tr("Train: Diesel shunter + banker + 4 wagons").startswith("ট্রেন: ডিজেল শান্টার + ব্যাংকার + 4টি")
    i18n.set_lang("en")
    assert i18n.tr("Cost Rs 1.50 L / Rs 2.50 L") == "Cost Rs 1.50 L / Rs 2.50 L"


def test_bengali_font_shapes_text():
    from game.ui import font
    pygame.init()
    f = font(20, bengali=True)
    w, h = f.size("খাঁড়ির সেতু")
    assert w > 40 and h > 10


def test_f2_switches_language_and_it_is_remembered(tmp_path):
    path = str(tmp_path / "save.json")
    app = App(save=Save(path), headless=True, show_briefings=False)
    assert i18n.lang() == "en"
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2, mod=0, unicode="")], 1 / 60)
    assert i18n.lang() == "bn"
    app.start_level(1)
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2, mod=0, unicode="")], 1 / 60)
    assert i18n.lang() == "en"
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2, mod=0, unicode="")], 1 / 60)
    i18n.set_lang("en")
    App(save=Save(path), headless=True, show_briefings=False)
    assert i18n.lang() == "bn"            # restored from save.json
