"""Headless smoke tests: every screen opens, draws and survives clicks, keys and runs."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from game.app import App
from game.save import Save
from game.ui import BOTTOM_BAR, HEIGHT, WIDTH


@pytest.fixture
def app(tmp_path):
    a = App(save=Save(str(tmp_path / "save.json")), headless=True, show_briefings=True)
    yield a


def click(app, pos, button=1):
    app.frame([pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=button),
               pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=button)], 1 / 60)


def key(app, k, mod=0):
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=k, mod=mod, unicode="")], 1 / 60)


def frames(app, n, dt=1 / 60):
    for _ in range(n):
        app.frame([], dt)


def test_menu_draws(app):
    frames(app, 3)
    app.frame([pygame.event.Event(pygame.MOUSEMOTION, pos=(300, 300), rel=(0, 0), buttons=(0, 0, 0))], 1 / 60)


@pytest.mark.parametrize("num", range(1, 11))
def test_every_level_opens_and_runs(app, num):
    app.start_level(num)
    frames(app, 2)
    key(app, pygame.K_RETURN)            # close the briefing
    assert app.scene.overlay is None
    frames(app, 2)
    # click across the play area and the toolbar to shake out crashes
    for x in range(40, WIDTH - 40, 97):
        for y in (120, 260, 420, 560):
            click(app, (x, y))
            app.frame([pygame.event.Event(pygame.MOUSEMOTION, pos=(x + 5, y + 5), rel=(1, 1),
                                          buttons=(0, 0, 0))], 1 / 60)
            if app.scene.overlay is not None:          # a click may start a run that fails
                app.scene.overlay = None
            if app.scene.__class__.__name__ == "MenuScene":
                app.start_level(num)
                app.scene.overlay = None
    key(app, pygame.K_SPACE)                          # run / stop
    frames(app, 120)
    key(app, pygame.K_c)                              # toggle calculator
    frames(app, 2)
    key(app, pygame.K_F1)                             # briefing again
    frames(app, 1)
    key(app, pygame.K_ESCAPE)                         # back to menu
    frames(app, 1)


def drag(app, a, b):
    app.frame([pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=a, button=1)], 1 / 60)
    app.frame([pygame.event.Event(pygame.MOUSEMOTION, pos=b, rel=(1, 1), buttons=(1, 0, 0))], 1 / 60)
    app.frame([pygame.event.Event(pygame.MOUSEBUTTONUP, pos=b, button=1)], 1 / 60)


def test_build_a_bridge_with_the_mouse(app):
    app.start_level(1)
    sc = app.scene
    sc.overlay = None
    cam = sc.cam
    # deck: drag from bank to bank in 4 m pieces, then triangles above
    sc.set_tool("deck")
    xs = [12, 16, 20, 24, 28]
    for a, b in zip(xs, xs[1:]):
        drag(app, cam.to_screen(a, 0), cam.to_screen(b, 0))
    sc.set_tool("beam")
    for k in range(4):
        top = (14 + 4 * k, 3)
        click(app, cam.to_screen(xs[k], 0))            # click-click style
        click(app, cam.to_screen(*top))
        drag(app, cam.to_screen(*top), cam.to_screen(xs[k + 1], 0))
        if k < 3:
            drag(app, cam.to_screen(*top), cam.to_screen(18 + 4 * k, 3))
    assert len(sc.design.beams) == 4 + 8 + 3
    frames(app, 2)
    assert sc.preview is not None and sc.preview_error == ""
    # select a beam and change its area with the drawer slider
    sc.set_tool("select")
    a, b = cam.to_screen(14, 3), cam.to_screen(18, 3)
    click(app, ((a[0] + b[0]) // 2, a[1]))
    assert sc.selected and sc.selected[0] == "beam"
    slider = sc.drawer.sliders.items[0]
    click(app, (slider.track.right - 2, slider.track.centery))
    assert sc.design.beams[sc.selected[1]].A > 0.01
    # right-click delete then undo
    n = len(sc.design.beams)
    click(app, ((a[0] + b[0]) // 2, a[1]), button=3)
    assert len(sc.design.beams) == n - 1
    key(app, pygame.K_z, pygame.KMOD_CTRL)
    assert len(sc.design.beams) == n
    # run it to the end
    key(app, pygame.K_SPACE)
    for _ in range(1200):
        app.frame([], 1 / 60)
        if sc.overlay is not None:
            break
    assert sc.overlay is not None


def test_rail_handle_drag_changes_the_grade(app):
    app.start_level(2)
    sc = app.scene
    sc.overlay = None
    i = sc.cfg["stations"].index(50)
    before = sc.design.heights[i]
    p = sc.cam.to_screen(50, before)
    drag(app, p, (p[0], p[1] - 60))
    assert sc.design.heights[i] > before
