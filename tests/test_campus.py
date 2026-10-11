"""Campus World: the 3D front door - physics, swinging, entering every building, coming back."""
import math
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from engine import campus3d as world
from game import i18n
from game.app import App
from game.save import Save


@pytest.fixture
def app(tmp_path):
    a = App(save=Save(str(tmp_path / "s.json")), headless=True, show_briefings=False)
    yield a
    i18n.set_lang("en")


def run(player, boxes, secs, fwd=0.0, turn=0.0):
    for _ in range(int(secs * 60)):
        player.update(1 / 60, boxes, fwd, turn)


def test_game_opens_in_campus_world(app):
    assert type(app.scene).__name__ == "CampusScene"


def test_world_has_every_part_of_the_game():
    boxes = world.build_world()
    kinds = {b.kind for b in boxes}
    assert {"school", "library", "register", "ncert", "donate", "daily", "level"} <= kinds
    classes = sorted(c for b in boxes if b.kind == "school" for c in b.payload)
    assert classes == list(range(1, 15))                 # Class 1-12, NIT, IIT
    assert sorted(b.payload for b in boxes if b.kind == "level") == list(range(1, 11))
    for b in boxes:                                       # nothing blocks the avenue
        if b.kind is not None:
            assert b.x1 <= -world.BRIDGE_HALF or b.x0 >= world.BRIDGE_HALF or b.z0 > 200


def test_walk_jump_and_walls():
    boxes = world.build_world()
    p = world.Player((0, 0, 0), 0.0)
    run(p, boxes, 1.0, fwd=1.0)
    assert p.pos[2] > 8 and p.grounded and abs(p.pos[0]) < 0.01
    assert p.jump() and not p.grounded
    run(p, boxes, 1.5)
    assert p.grounded and p.pos[1] == 0.0
    # walk west into the Primary School: the wall stops you
    school = next(b for b in boxes if b.key == "primary")
    p = world.Player((-8, 0, school.centre[2]), -math.pi / 2)
    run(p, boxes, 2.0, fwd=1.0)
    assert p.pos[0] >= school.x1 + world.RADIUS - 1e-6


def test_swing_keeps_rope_length_and_carries_you_forward():
    boxes = world.build_world()
    p = world.Player((0, 0, 20), 0.0)
    p.jump()
    run(p, boxes, 0.25)
    assert p.attach(boxes)
    anchor, length, longest = p.rope
    assert longest == anchor[1] - 2.5               # reels in to clear the ground
    assert anchor[1] > p.pos[1]
    z0 = p.pos[2]
    for _ in range(40):
        p.update(1 / 60, boxes, 1.0)
        if p.rope is None:
            break
        assert math.dist(p.pos, p.rope[0]) <= p.rope[1] + 1e-6
    assert p.pos[2] > z0
    p.release()
    assert p.rope is None


def test_falling_in_the_river_puts_you_on_the_bank():
    boxes = world.build_world()
    p = world.Player((-40, 3, 105), 0.0)
    ev = None
    for _ in range(120):
        ev = p.update(1 / 60, boxes) or ev
    assert ev == "splash" and not world.in_river(p.pos[0], p.pos[2])
    q = world.Player((0, 0, 90), 0.0)                    # the avenue bridge is dry
    run(q, boxes, 2.5, fwd=1.0)
    assert q.pos[2] > world.RIVER_Z[1] and q.splash == 0.0


def test_zip_line_lands_at_the_door():
    boxes = world.build_world()
    iit = next(b for b in boxes if b.key == "iit")
    p = world.Player()
    p.zip_to(iit.door())
    ev = None
    for _ in range(400):
        ev = p.update(1 / 60, boxes) or ev
        if p.zip is None:
            break
    assert ev == "arrived"
    assert world.nearest_entrance(boxes, p.pos) is iit


def test_camera_clips_walls_next_to_it():
    cam = world.Camera(1280, 720)
    cam.follow((0, 0, 0), 0.0)
    pr = cam.project_poly([(-5, 0, cam.pos[2] - 2), (5, 0, cam.pos[2] - 2), (5, 0, 30), (-5, 0, 30)])
    assert pr is not None and len(pr[0]) >= 3            # half behind the camera, still drawn
    assert cam.project((0, 0, cam.pos[2] - 5)) is None


def enter(app, key):
    sc = app.scene
    b = sc.by_key[key]
    sc.player = world.Player(b.door(), 0.0)
    sc.update(1 / 60)
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e, mod=0, unicode="e")], 1 / 60)
    return b


def test_entering_schools_opens_the_academy_and_returns_to_the_door(app):
    b = enter(app, "middle")
    sc = app.scene
    assert sc.picker is not None
    sc.picker.widgets.items[2].click()                   # Class 7
    assert type(app.scene).__name__ == "AcademyScene" and app.scene.cls == 7
    app.frame([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")], 1 / 60)
    assert type(app.scene).__name__ == "CampusScene"
    assert math.dist(app.scene.player.pos, b.door()) < 0.01
    enter(app, "iit")                                    # one level only: straight in
    assert type(app.scene).__name__ == "AcademyScene" and app.scene.cls == 14


def test_every_building_opens_its_screen(app):
    enter(app, "tower")
    assert type(app.scene).__name__ == "AcademyScene" and app.scene.daily
    app.to_menu()
    enter(app, "library")
    assert app.scene.picker is not None
    app.scene.picker.widgets.items[1].click()
    assert type(app.scene).__name__ == "AcademyScene" and app.scene.subject == "skills"
    app.to_menu()
    enter(app, "registry")
    assert app.scene.register_overlay is not None
    app.scene.register_overlay = None
    enter(app, "archive")
    assert app.scene.ncert_overlay is not None
    app.scene.ncert_overlay = None
    enter(app, "camp")
    assert type(app.scene).__name__ == "DonationScene"
    app.to_menu()
    app.save.unlocked = lambda n: n == 1                 # as if only site 1 were open
    enter(app, "site2")
    assert type(app.scene).__name__ == "CampusScene" and "locked" in app.scene.toast[0]
    del app.save.unlocked
    enter(app, "site1")
    assert type(app.scene).__name__ == "BridgeScene"
    app.to_menu()
    assert type(app.scene).__name__ == "CampusScene"
    app.scene.levels_btn.click()
    assert type(app.scene).__name__ == "MenuScene"
    app.to_academy()
    app.to_menu()                                        # opened from the menu: back to the menu
    assert type(app.scene).__name__ == "MenuScene"


def test_campus_draws_in_both_languages_from_everywhere(app):
    sc = app.scene
    for lang in ("en", "bn"):
        i18n.set_lang(lang)
        for spot in [(0, 0, -18), (0, 0, 100), (-50, 20, 105), (0, 0, 200), (90, 0, 60)]:
            for yaw in (0.0, 1.6, 3.1, -1.6):
                sc.player = world.Player(spot, yaw)
                sc.cam.follow(sc.player.pos, yaw)
                sc.update(1 / 60)
                sc.draw(app.screen)
        sc.next_tour()
        sc.zip_to_target()
        for _ in range(30):
            sc.update(1 / 30)
        sc.draw(app.screen)
        sc.enter(sc.by_key["primary"])
        sc.draw(app.screen)
        sc.picker = None


def test_clicking_the_map_targets_a_building(app):
    sc = app.scene
    from game.scenes.campus import MAP
    sc.close_tips()
    iit = sc.by_key["iit"]
    pos = sc.map_rect(iit).center
    app.frame([pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)], 1 / 60)
    assert sc.target is iit and MAP.collidepoint(pos)
    app.frame([pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)], 1 / 60)
    assert sc.player.zip is not None                     # second click: zip there


def test_signs_and_academy_show_what_is_ready(app):
    from engine.academy import SUBJECTS
    from engine.academy_data import items
    sc = app.scene
    ready = sum(1 for s in SUBJECTS if items(14, s))
    assert f"{ready} of {len(SUBJECTS)} subjects ready" in sc.box_sub(sc.by_key["iit"])
    assert len(items(14, "chemistry")) == 200                       # IIT chemistry is complete
    app.to_academy()
    ac = app.scene
    ac.pick_class(14)
    ac.update(1 / 60)
    from game.scenes.academy import READY, SOON
    assert ac.ready["chemistry"] == READY and "/200" in ac.subject_btns["chemistry"].label
    for s in SUBJECTS:
        if not items(14, s):
            assert ac.ready[s] == SOON and "coming soon" in ac.subject_btns[s].label
    ac.draw(app.screen)
