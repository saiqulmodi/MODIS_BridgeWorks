"""The Help screen: 200 numbered questions in English and Bengali, a walkthrough for every
level, and a screen that opens, scrolls, searches and closes without touching the level."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from game import i18n
from game.app import App
from game.guide import SECTIONS, level_walkthrough
from game.help_screen import UI, HelpOverlay
from game.save import Save


@pytest.fixture
def app(tmp_path):
    a = App(save=Save(str(tmp_path / "s.json")), headless=True, show_briefings=False)
    yield a
    i18n.set_lang("en")


def key(k, uni=""):
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode=uni)


def typed(s):
    return [pygame.event.Event(pygame.TEXTINPUT, text=c) for c in s]


def test_two_hundred_numbered_questions():
    numbered = [s for s in SECTIONS if s.first]
    assert [s.first for s in numbered] == [1, 51, 101, 151]
    assert [len(s.items) for s in numbered] == [50, 50, 50, 50]
    assert SECTIONS[0].first == 0 and len(SECTIONS[0].items) >= 20      # the start guide


def test_every_answer_is_in_both_languages():
    for sec in SECTIONS:
        assert i18n.has_bengali(sec.title_bn)
        for it in sec.items:
            assert it.q_en.strip() and it.a_en.strip()
            assert i18n.has_bengali(it.q_bn) and i18n.has_bengali(it.a_bn), it.q_en
            assert not i18n.has_bengali(it.q_en + it.a_en), it.q_en
    for en, bn in UI.values():
        assert en and i18n.has_bengali(bn) or i18n.has_bengali(en)


def test_no_question_is_asked_twice():
    qs = [it.q_en for sec in SECTIONS for it in sec.items]
    assert len(qs) == len(set(qs))


def test_every_level_has_a_walkthrough():
    for num in range(1, 11):
        s, k = level_walkthrough(num)
        assert SECTIONS[s].items[k].level == num
        assert f"Level {num}" in SECTIONS[s].items[k].q_en


def test_menu_help_opens_switches_language_and_closes(app):
    app.frame([key(pygame.K_h, "h")], 1 / 60)
    assert isinstance(app.scene.help, HelpOverlay)
    app.frame([key(pygame.K_F2)], 1 / 60)
    assert i18n.lang() == "bn"
    app.frame([key(pygame.K_ESCAPE)], 1 / 60)
    assert app.scene.help is None and app.running        # Esc closed Help, not the game
    app.frame([key(pygame.K_F2)], 1 / 60)
    assert i18n.lang() == "en"


def test_level_help_opens_on_the_walkthrough_and_keeps_keys_away_from_the_level(app):
    app.start_level(7)
    sc = app.scene
    app.frame([key(pygame.K_h, "h")], 1 / 60)
    ov = sc.overlay
    assert isinstance(ov, HelpOverlay)
    assert ov.highlight == level_walkthrough(7)
    # typing goes into the search box, not to the level's hotkeys (L = wind lab, Esc = menu)
    app.frame([key(pygame.K_l, "l")] + typed("resonance"), 1 / 60)
    assert ov.query == "resonance" and sc.overlay is ov
    hits = ov.matches()
    assert hits and all("resonan" in " ".join((SECTIONS[s].items[k].q_en, SECTIONS[s].items[k].a_en)).lower()
                        or "অনুনাদ" in SECTIONS[s].items[k].a_bn for s, k in hits)
    app.frame([key(pygame.K_ESCAPE)], 1 / 60)         # first Esc clears the search
    assert ov.query == "" and sc.overlay is ov
    app.frame([key(pygame.K_ESCAPE)], 1 / 60)         # second Esc closes Help
    assert sc.overlay is None and app.scene is sc     # still in the level


def test_help_returns_to_the_briefing_it_was_opened_from(tmp_path):
    app = App(save=Save(str(tmp_path / "s.json")), headless=True, show_briefings=True)
    app.start_level(1)
    briefing = app.scene.overlay
    app.scene.toggle_help()
    assert isinstance(app.scene.overlay, HelpOverlay)
    app.scene.toggle_help()
    assert app.scene.overlay is briefing


def test_number_search_finds_that_question_first(app):
    app.scene.open_help()
    ov = app.scene.help
    for q, n in (("Q37", 37), ("151", 151), ("প্রশ্ন 200", 200)):
        ov.query = q
        s, k = ov.matches()[0]
        assert SECTIONS[s].first + k == n


def test_scrolling_stays_inside_the_text(app):
    app.scene.open_help()
    ov = app.scene.help
    ov.show_section(1)
    app.frame([key(pygame.K_END)], 1 / 60)
    assert ov.scroll == ov.max_scroll > 0
    app.frame([pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=-100, flipped=False)], 1 / 60)
    assert ov.scroll == ov.max_scroll
    app.frame([key(pygame.K_HOME)], 1 / 60)
    assert ov.scroll == 0
    app.frame([key(pygame.K_PAGEDOWN)], 1 / 60)
    assert 0 < ov.scroll <= ov.max_scroll


def test_help_draws_every_section_in_both_languages(app):
    app.scene.open_help()
    ov = app.scene.help
    for lang in ("en", "bn"):
        i18n.set_lang(lang)
        for k in range(len(SECTIONS)):
            ov.show_section(k)
            ov.scroll = ov.max_scroll
            app.scene.draw(app.screen)
        ov.query = "zzzz"
        app.scene.draw(app.screen)
        ov.query = ""
