"""3D view of a bridge level.

The design itself stays a flat (2D) truss - that is what the physics solves. In 3D it is
built as a real bridge: the same truss on both sides of the road, a road deck between them
and cross beams at every joint, so both side trusses share the load. The view can be
rotated and zoomed, and you can keep building in it: clicks land on the side truss nearest
to you, and every beam you draw appears on both sides.

Drawing is plain pygame: points are projected with a perspective camera and everything is
painted far-to-near.
"""
import math

import pygame

from engine.materials import ALL as MATERIALS
from engine.truss import FAILED

from .ui import (ACCENT, BAD, BOTTOM_BAR, CYAN, DRAWER_W, HEIGHT, STATUS, TOP_BAR, WIDTH, arrow,
                 text)

DECK_WIDTH = {"van": 5.0, "bus": 7.0, "truck": 7.0, "maglev": 6.0}
ROCK = (58, 76, 104)
WATER = (34, 96, 168)
ROAD = (58, 60, 68)
DECK = (44, 46, 54)
CROSS = (120, 136, 162)
LIGHT = (0.35, 0.85, 0.40)


def deck_width(cfg):
    return cfg.get("deck_width", DECK_WIDTH.get(cfg.get("vehicle", {}).get("kind"), 6.0))


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _norm(a):
    L = math.sqrt(_dot(a, a)) or 1.0
    return (a[0] / L, a[1] / L, a[2] / L)


def _shade(colour, k):
    return tuple(max(0, min(255, int(c * k))) for c in colour)


class Camera3D:
    """Orbit camera around the middle of the level."""
    FOV = math.radians(48)

    def __init__(self, cfg):
        x0, y0, x1, y1 = cfg["view"]
        self.area = pygame.Rect(10, TOP_BAR + 10, WIDTH - DRAWER_W - 46,
                                HEIGHT - TOP_BAR - BOTTOM_BAR - 20)
        # frame the gap you are bridging, not the whole map
        lx, rx = cfg.get("left_x", x0), cfg.get("right_x", x1)
        gy = cfg.get("ground_y", y0)
        self.target = ((lx + rx) / 2, (gy + y1) / 2, 0.0)
        aspect = self.area.w / self.area.h
        t = math.tan(self.FOV / 2)
        w = min(x1 - x0, (rx - lx) * 1.35 + 6)
        self.home = max(w / 2 / (t * aspect), (y1 - gy) / 2 / t) * 1.1
        self.shake = 0.0
        self.reset()

    def reset(self):
        self.yaw, self.pitch, self.dist = 0.55, 0.30, self.home
        self._update()

    def rotate(self, dyaw, dpitch):
        self.yaw = (self.yaw + dyaw + math.pi) % (2 * math.pi) - math.pi
        self.pitch = max(-0.30, min(1.45, self.pitch + dpitch))
        self._update()

    def zoom(self, factor):
        self.dist = max(0.45 * self.home, min(2.5 * self.home, self.dist * factor))
        self._update()

    def _update(self):
        cp = math.cos(self.pitch)
        off = (cp * math.sin(self.yaw), math.sin(self.pitch), cp * math.cos(self.yaw))
        self.pos = tuple(self.target[i] + self.dist * off[i] for i in range(3))
        self.f = _norm(_sub(self.target, self.pos))
        self.r = _norm(_cross(self.f, (0.0, 1.0, 0.0)))
        self.u = _cross(self.r, self.f)
        self.focal = (self.area.h / 2) / math.tan(self.FOV / 2)
        self.cx, self.cy = self.area.centerx, self.area.centery

    def depth(self, p):
        return _dot(_sub((p[0] + self.shake, p[1], p[2]), self.pos), self.f)

    def project(self, p):
        """(screen x, screen y, depth), or None if the point is behind the camera."""
        d = _sub((p[0] + self.shake, p[1], p[2]), self.pos)
        zc = _dot(d, self.f)
        if zc < 0.5:
            return None
        return (self.cx + self.focal * _dot(d, self.r) / zc,
                self.cy - self.focal * _dot(d, self.u) / zc, zc)

    def on_plane(self, pos, z0):
        """World (x, y) where the mouse ray meets the vertical plane z = z0, or None."""
        sx, sy = pos
        a, b = (sx - self.cx) / self.focal, (self.cy - sy) / self.focal
        ray = tuple(self.f[i] + self.r[i] * a + self.u[i] * b for i in range(3))
        if abs(ray[2]) < 0.12 * math.sqrt(_dot(ray, ray)):
            return None               # looking along the plane: too ambiguous to build
        t = (z0 - self.pos[2]) / ray[2]
        if t <= 0:
            return None
        return (self.pos[0] + ray[0] * t - self.shake, self.pos[1] + ray[1] * t)

    def facing(self, z):
        """Is the plane z seen from the front (camera on the same side as z)?"""
        return self.pos[2] * z > 0


class Painter:
    """Collects shapes with their depth, then paints far-to-near."""

    def __init__(self, cam):
        self.cam = cam
        self.items = []

    def poly(self, pts3, colour, edge=None, bias=0.0):
        pr = [self.cam.project(p) for p in pts3]
        if any(p is None for p in pr):
            return
        depth = sum(p[2] for p in pr) / len(pr) + bias
        self.items.append((depth, 0, [(p[0], p[1]) for p in pr], colour, edge))

    def line(self, a3, b3, colour, width_m, min_px=1, bias=0.0):
        a, b = self.cam.project(a3), self.cam.project(b3)
        if a is None or b is None:
            return
        depth = (a[2] + b[2]) / 2 + bias
        w = max(min_px, int(round(width_m * self.cam.focal / depth)))
        self.items.append((depth, 1, ((a[0], a[1]), (b[0], b[1])), colour, w))

    def dot(self, p3, colour, radius_m, min_px=2, width=0, bias=0.0):
        p = self.cam.project(p3)
        if p is None:
            return
        r = max(min_px, int(round(radius_m * self.cam.focal / p[2])))
        self.items.append((p[2] + bias, 2, (p[0], p[1]), colour, (r, width)))

    def box(self, x0, x1, y0, y1, z0, z1, colour, edge=None):
        self.solid([(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], colour, edge)

    def solid(self, c, colour, edge=None):
        """A hexahedron from 8 corners ordered (x0/x1) x (y0/y1) x (z0/z1); back faces culled."""
        centre = tuple(sum(p[i] for p in c) / 8 for i in range(3))
        for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
            pts = [c[k] for k in f]
            n = _norm(_cross(_sub(pts[1], pts[0]), _sub(pts[3], pts[0])))
            fc = tuple(sum(p[i] for p in pts) / 4 for i in range(3))
            if _dot(n, _sub(fc, centre)) < 0:
                n = (-n[0], -n[1], -n[2])
            if _dot(n, _sub(self.cam.pos, fc)) <= 0:
                continue
            k = 0.55 + 0.45 * max(0.0, _dot(n, _norm(LIGHT)))
            self.poly(pts, _shade(colour, k), edge)

    def paint(self, s):
        self.items.sort(key=lambda it: -it[0])
        for _, kind, geo, colour, extra in self.items:
            if kind == 0:
                pygame.draw.polygon(s, colour, geo)
                if extra:
                    pygame.draw.polygon(s, extra, geo, 1)
            elif kind == 1:
                pygame.draw.line(s, colour, geo[0], geo[1], extra)
            else:
                pygame.draw.circle(s, colour, (int(geo[0]), int(geo[1])), extra[0], extra[1])
        self.items = []


_SKY = {}


def _sky(rect):
    key = (rect.w, rect.h)
    if key not in _SKY:
        surf = pygame.Surface(key)
        for y in range(rect.h):
            t = y / max(1, rect.h - 1)
            surf.fill((int(10 + 22 * t), int(18 + 30 * t), int(34 + 40 * t)), (0, y, rect.w, 1))
        _SKY[key] = surf
    return _SKY[key]


def draw(scene, s, res):
    """Draw the whole bridge scene in 3D (everything but the HUD)."""
    cam, cfg, d = scene.cam3, scene.cfg, scene.design
    area = pygame.Rect(0, TOP_BAR, WIDTH, HEIGHT - TOP_BAR - BOTTOM_BAR)
    s.blit(_sky(area), area.topleft)
    W = deck_width(cfg)
    half = W / 2
    Wt = half + max(6.0, W)
    v = cfg["view"]
    cam.shake = scene.sim.ground_x * 6 if (scene.sim and scene.sim.quake and scene.mode == "run") else 0.0

    # --- terrain (always behind the bridge, painted first)
    p = Painter(cam)
    p.box(v[0], cfg["left_x"], v[1], cfg["deck_y"], -Wt, Wt, ROCK)
    p.box(cfg["right_x"], v[2], v[1], cfg["deck_y"], -Wt, Wt, ROCK)
    p.box(cfg["left_x"], cfg["right_x"], v[1], cfg["ground_y"], -Wt, Wt, ROCK)
    for a, b in cfg.get("islands", []):
        p.box(a, b, cfg["ground_y"], cfg.get("extra_anchor_y", cfg["ground_y"]), -half - 1.5, half + 1.5,
              (78, 94, 120))
    p.paint(s)
    if cfg.get("water_y") is not None:
        y = cfg["water_y"]
        p.poly([(cfg["left_x"], y, -Wt), (cfg["right_x"], y, -Wt), (cfg["right_x"], y, Wt),
                (cfg["left_x"], y, Wt)], WATER, (90, 150, 220))
        p.paint(s)
    y = cfg["deck_y"] + 0.02
    for x0, x1 in ((v[0], cfg["left_x"]), (cfg["right_x"], v[2])):
        p.poly([(x0, y, -half), (x1, y, -half), (x1, y, half), (x0, y, half)], ROAD)
    p.paint(s)

    # --- build grid on the side you are building on
    zb = scene.build_z()
    if scene.mode == "edit":
        g = cfg["grid"]
        x = v[0]
        while x <= v[2] + 1e-6:
            yy = v[1]
            while yy <= v[3] + 1e-6:
                if not scene.solid(x, yy):
                    q = cam.project((x, yy, zb))
                    if q:
                        s.set_at((int(q[0]), int(q[1])), (90, 125, 180))
                yy += g
            x += g

    # --- the bridge
    span = v[2] - v[0]
    joints = [scene.world_joint(k, res) for k in range(len(d.joints))]
    used = {b.a for b in d.beams} | {b.b for b in d.beams}
    deck_joints = {k for b in d.beams if b.kind == "deck" for k in (b.a, b.b)}
    flash = (scene.tick // 8) % 2
    for k, bm in enumerate(d.beams):
        (ax, ay), (bx, by) = joints[bm.a], joints[bm.b]
        mat = MATERIALS[bm.material]
        w_px = max(2, min(11, int(3 + 2 * math.log2(max(bm.A, 1e-4) / 0.001))))
        if bm.kind == "cable":
            w_px = max(2, w_px - 2)
        thick = w_px / scene.cam.scale
        col = mat.colour
        if res is not None and k < len(res.members):
            mr = res.members[k]
            col = STATUS[mr.status]
            if mr.slack:
                col = (110, 120, 135)
            if mr.status == FAILED and flash:
                col = (255, 255, 255)
        if bm.kind == "deck":
            p.poly([(ax, ay, -half), (bx, by, -half), (bx, by, half), (ax, ay, half)], DECK, (30, 30, 36),
                   bias=0.3)
            p.line((ax, ay + 0.03, 0), (bx, by + 0.03, 0), (230, 200, 90), 0.08, bias=0.2)
        for z in (half, -half):
            if scene.selected == ("beam", k):
                p.line((ax, ay, z), (bx, by, z), ACCENT, thick * 2.2, 3, bias=0.01)
            p.line((ax, ay, z), (bx, by, z), col, thick, 2)
    for k in used:
        x, y = joints[k]
        col = CROSS
        p.line((x, y, -half), (x, y, half), col, 0.12 if k in deck_joints else 0.09, 1, bias=0.05)
        for z in (half, -half):
            p.dot((x, y, z), (235, 240, 250), span / 400)
            if scene.selected == ("joint", k):
                p.dot((x, y, z), ACCENT, span / 160, 6, 2, bias=-0.01)
    a = span / 90                      # bearing blocks under the supports, across the road
    for k, kind in d.anchors.items():
        x, y = d.joints[k]
        p.box(x - a, x + a, y - 1.4 * a, y, -half - 0.3, half + 0.3,
              ACCENT if kind == "pin" else (150, 120, 60), (60, 50, 20))
    if scene.debris:
        for (a, b) in scene.debris:
            p.line((a[0], a[1], 0), (b[0], b[1], 0), (150, 150, 150), 0.3)
    if scene.sim and scene.mode in ("run", "frozen"):
        _vehicles(scene, p, half)
    p.paint(s)

    if scene.sim and scene.mode in ("run", "frozen") and scene.sim.wind:
        _wind(scene, s, Wt)
    if scene.vectors and res is not None:
        _vectors(scene, s, res, joints, zb)
    _pending(scene, s, zb)


def _vehicles(scene, p, half):
    colour = {"van": (240, 140, 60), "bus": (240, 200, 60), "truck": (200, 90, 70),
              "maglev": (230, 240, 255)}.get(scene.cfg["vehicle"]["kind"], ACCENT)
    for veh in scene.sim.vehicles:
        fx, fy = veh.path.point_at(veh.s)
        rx, ry = veh.path.point_at(veh.s - veh.spec.length)
        dx, dy = fx - rx, fy - ry
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        lift = 0.5 if veh.spec.maglev else 0.6
        h = 1.8 if veh.spec.maglev else 2.4
        hw = min(1.3, half * 0.5)
        corners = []
        for (bx, by) in ((rx, ry), (fx, fy)):
            for up in (lift, lift + h):
                for z in (-hw, hw):
                    corners.append((bx + nx * up, by + ny * up, z))
        p.solid(corners, colour, (20, 20, 30))
        if not veh.spec.maglev:
            for (ax, ay) in veh.axle_points():
                for z in (-hw, hw):
                    p.dot((ax + nx * 0.45, ay + ny * 0.45, z), (20, 20, 25), 0.45)


def _wind(scene, s, Wt):
    sim, v, cam = scene.sim, scene.cfg["view"], scene.cam3
    for k in range(18):
        y = v[1] + (k + 0.5) * (v[3] - v[1]) / 18
        z = -Wt + (k * 5.3) % (2 * Wt)
        x = v[0] + (scene.tick * sim.wind_U * 0.05 + k * 7.3) % (v[2] - v[0])
        a, b = cam.project((x, y, z)), cam.project((x + sim.wind_U * 0.15, y, z))
        if a and b:
            pygame.draw.line(s, (150, 190, 230), a[:2], b[:2], 1)


def _vectors(scene, s, res, joints, z):
    cam, d = scene.cam3, scene.design
    span = scene.cfg["view"][2] - scene.cfg["view"][0]
    big = max(1.0, max((abs(r) for r in res.reactions.flatten()), default=1.0))
    k_m = span / 12 / big                    # the biggest reaction is drawn span/12 long

    def arr(col, x, y, fx, fy, w=3):
        a, b = cam.project((x, y, z)), cam.project((x + fx * k_m, y + fy * k_m, z))
        if a and b:
            arrow(s, col, a[:2], b[:2], w)
        return a
    for k in range(len(d.joints)):
        x, y = joints[k]
        rx, ry = res.reactions[k]
        if rx or ry:
            a = arr(CYAN, x, y, rx, ry)
            if a:
                text(s, f"{math.hypot(rx, ry)/1e3:.0f} kN", (a[0] + 6, a[1] + 16), 13, CYAN)
        lx, ly = res.loads[k]
        if scene.sim and (abs(ly) > 1 or abs(lx) > 1) and k not in d.anchors:
            arr(BAD, x, y, lx, ly, 2)
    if scene.selected and scene.selected[0] in ("joint", "beam"):
        kind, i = scene.selected
        for (n, mi, fx, fy) in res.node_forces:
            if (kind == "joint" and n == i) or (kind == "beam" and mi == i):
                x, y = joints[n]
                arr(ACCENT, x, y, fx, fy)


def _pending(scene, s, z):
    if scene.mode != "edit" or not scene.pending or scene.mouse_pos is None:
        return
    q = scene.pick_point(scene.mouse_pos)
    if q is None:
        return
    a, b = scene.cam3.project((*scene.pending, z)), scene.cam3.project((*q, z))
    if a and b:
        ok, label = scene.pending_info(q)
        pygame.draw.line(s, ACCENT if ok else BAD, a[:2], b[:2], 3)
        text(s, label, (b[0] + 12, b[1] - 22), 14, ACCENT if ok else BAD)
