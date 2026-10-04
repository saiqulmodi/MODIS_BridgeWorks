"""3D view: the camera maths, and building / selecting / deleting by clicking in 3D."""
import math
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from engine.levels import get
from game import view3d
from game.app import App
from game.reference import level1_good
from game.save import Save


@pytest.fixture
def scene(tmp_path):
    app = App(save=Save(str(tmp_path / "s.json")), headless=True, show_briefings=False)
    app.start_level(1)
    sc = app.scene
    sc.toggle_view3d()
    yield app, sc
    app.view3d = False


def click(app, pos, button=1):
    app.frame([pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(0, 0), buttons=(0, 0, 0)),
               pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=button),
               pygame.event.Event(pygame.MOUSEBUTTONUP, pos=pos, button=button)], 1 / 60)


def test_mouse_ray_lands_back_on_the_projected_point():
    cam = view3d.Camera3D(get(1).cfg)
    for yaw, pitch in ((0.55, 0.3), (-0.9, 0.6), (2.8, 0.2)):
        cam.yaw, cam.pitch = yaw, pitch
        cam._update()
        z = 2.5 if cam.pos[2] > 0 else -2.5
        sx, sy, _ = cam.project((17.0, 3.0, z))
        x, y = cam.on_plane((sx, sy), z)
        assert abs(x - 17.0) < 1e-6 and abs(y - 3.0) < 1e-6


def test_edge_on_view_refuses_to_build():
    cam = view3d.Camera3D(get(1).cfg)
    cam.yaw = math.pi / 2           # looking along the road from the side bank
    cam._update()
    assert cam.on_plane((cam.cx, cam.cy), 2.5) is None


def test_build_a_deck_beam_by_clicking_in_3d(scene):
    app, sc = scene
    sc.set_tool("deck")
    z = sc.build_z()
    a = sc.cam3.project((12.0, 0.0, z))
    b = sc.cam3.project((16.0, 0.0, z))
    click(app, (int(round(a[0])), int(round(a[1]))))
    click(app, (int(round(b[0])), int(round(b[1]))))
    assert len(sc.design.beams) == 1
    bm = sc.design.beams[0]
    ends = {sc.design.joints[bm.a], sc.design.joints[bm.b]}
    assert ends == {(12.0, 0.0), (16.0, 0.0)} and bm.kind == "deck"


def test_building_from_behind_uses_the_near_side(scene):
    app, sc = scene
    sc.cam3.rotate(math.pi, 0)       # now looking from the other side of the road
    assert sc.build_z() < 0
    sc.set_tool("beam")
    z = sc.build_z()
    a, b = sc.cam3.project((14.0, 0.0, z)), sc.cam3.project((16.0, 2.0, z))
    click(app, (int(a[0]), int(a[1])))
    click(app, (int(b[0]), int(b[1])))
    bm = sc.design.beams[0]
    assert {sc.design.joints[bm.a], sc.design.joints[bm.b]} == {(14.0, 0.0), (16.0, 2.0)}


def test_select_and_delete_in_3d(scene):
    app, sc = scene
    sc.design = level1_good()
    sc.dirty = True
    sc.update(1 / 60)
    bm = sc.design.beams[3]
    (ax, ay), (bx, by) = sc.design.joints[bm.a], sc.design.joints[bm.b]
    # the far side truss works too
    z = -sc.build_z()
    m = sc.cam3.project(((ax + bx) / 2, (ay + by) / 2, z))
    sc.set_tool("select")
    click(app, (int(m[0]), int(m[1])))
    assert sc.selected and sc.selected[0] in ("beam", "joint")
    n = len(sc.design.beams)
    click(app, (int(m[0]), int(m[1])), button=3)
    assert len(sc.design.beams) == n - 1


def test_camera_controls_and_drawing(scene):
    app, sc = scene
    sc.design = level1_good()
    sc.dirty = True
    sc.update(1 / 60)
    yaw, dist = sc.cam3.yaw, sc.cam3.dist
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0, unicode="")], 1 / 60)
    app.frame([pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=1, flipped=False)], 1 / 60)
    assert sc.cam3.yaw != yaw and sc.cam3.dist < dist
    for b in sc.view_controls:
        b.click()
    sc.cam3.reset()
    assert sc.cam3.yaw == yaw
    sc.start_run()
    for _ in range(30):
        sc.update(1 / 30)
    sc.draw(app.screen)               # vehicles, stress colours, HUD in 3D
    sc.toggle_view3d()
    assert not sc.view3d and not any(b.visible for b in sc.view_controls)
    sc.draw(app.screen)
