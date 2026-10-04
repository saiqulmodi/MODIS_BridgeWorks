"""Level 3 - The Deep Canyon Pier: balanced cantilever construction, see-saw balance,
haunched girders and the mid-span stitch."""
import math

import numpy as np
import pygame

from engine import economy
from engine.beams import rect_I
from engine.cantilever import (CantileverBridge, PT_RS, TIE_DOWN_RS, construction_cost)
from engine.failure import FailureReport

from .. import sound
from ..common import Card, LevelScene
from ..ui import (ACCENT, BAD, BG_DARK, BOTTOM_BAR, CYAN, GOOD, HEIGHT, LINE, MUTED, PANEL_EDGE,
                  TEXT, TOP_BAR, WARN, WIDTH, Button, Slider, blueprint_background, mini_chart,
                  panel, text)
from ..help_texts import HELP
from .bridge import ROCK, ROCK_EDGE, Camera

FLOOR = -44.0
PT_NAMES = ("none", "light", "heavy")


class CantileverScene(LevelScene):
    CONTROLS = ("Cast segments one at a time with the four CAST buttons. Watch each pier's "
                "see-saw meter. Tie-downs add resistance. Set the haunch depths in the "
                "calculator before the first cast. When all arms are complete, STITCH, then "
                "run the TRUCK TEST.")

    DEMO_STATE = ("bridge", "history", "last_check", "tilt", "balance_hist", "girder", "bundle",
                  "truck", "truck_worst")

    def __init__(self, app, level):
        super().__init__(app, level)
        self.demo_queue = []
        self.demo_timer = 0.0
        self.cam = Camera(level.cfg["view"])
        self.bridge = CantileverBridge()
        self.history = []              # (pier, side) cast order for undo
        self.balance_hist = {"pier A MN*m": [(0, 0.0)], "pier B MN*m": [(0, 0.0)]}
        self.last_check = [None, None]
        self.tilt = [0.0, 0.0]
        self.truck = None
        self.truck_worst = 0.0
        self.girder = None
        self.bundle = None
        self.tick = 0
        self._build_toolbar()
        self.show_girder_panel()

    def _build_toolbar(self):
        y = HEIGHT - BOTTOM_BAR + 9
        x = 10
        self.cast_btns = {}
        for pier, name in ((0, "A"), (1, "B")):
            for side, arrow_ in ((-1, "<"), (1, ">")):
                label = f"{arrow_} Cast {name}" if side < 0 else f"Cast {name} {arrow_}"
                b = self.widgets.add(Button((x, y, 104, 40), label,
                                            lambda p=pier, s=side: self.cast(p, s), size=15,
                                            help=HELP["cast"]))
                self.cast_btns[(pier, side)] = b
                x += 108
        x += 6
        for pier, name in ((0, "A"), (1, "B")):
            self.widgets.add(Button((x, y, 116, 40), f"Tie-down {name}", lambda p=pier: self.tie(p),
                                    size=14, help=HELP["tie"]))
            x += 120
        self.widgets.add(Button((x, y, 80, 40), "Undo", self.undo, size=14, help=HELP["undo_cast"]))
        x += 86
        self.stitch_btn = self.widgets.add(Button((x, y, 190, 40), "STITCH & POST-TENSION",
                                                  self.stitch, size=14, help=HELP["stitch"]))
        x += 196
        self.truck_btn = self.widgets.add(Button((x, y, WIDTH - x - 10, 40), "TRUCK TEST",
                                                 self.start_truck, colour=(40, 110, 70),
                                                 hotkey=pygame.K_SPACE, help=HELP["truck_test"]))

    def cost(self):
        return construction_cost(self.bridge)

    # --- demonstration: cast the whole bridge step by step ---------------------------------
    def demo_prepare(self):
        self.truck = None
        self.demo_queue = []

    def load_demo(self):
        self.bridge = CantileverBridge(d_pier=3.5, d_tip=2.5)
        self.history = []
        self.last_check = [None, None]
        self.tilt = [0.0, 0.0]
        self.balance_hist = {"pier A MN*m": [(0, 0.0)], "pier B MN*m": [(0, 0.0)]}
        self.girder = self.bundle = None
        self.show_girder_panel()

    def run_demo(self):
        b = self.bridge
        q = [("tie", 0), ("tie", 1)]
        for k in range(6):
            for p in (0, 1):
                for s in (-1, 1):
                    if k < b.arm_segments_needed(p, s):
                        q.append(("cast", p, s))
        q += [("pt", 1), ("stitch",), ("truck",)]
        self.demo_queue = q
        self.demo_timer = 0.0

    def after_demo(self):
        self.show_girder_panel()

    def _demo_step(self, dt):
        self.demo_timer += dt
        if self.demo_timer < 0.3:
            return
        self.demo_timer = 0.0
        act = self.demo_queue.pop(0)
        if act[0] == "tie":
            self.tie(act[1])
        elif act[0] == "cast":
            self.cast(act[1], act[2])
        elif act[0] == "pt":
            self._set_pt(act[1])
            self.show_girder_panel()
        elif act[0] == "stitch":
            self.stitch()
        elif act[0] == "truck":
            self.start_truck()

    # --- calculator panel ------------------------------------------------------------------
    def show_girder_panel(self):
        b = self.bridge
        sliders = []
        if b.can_change_haunch():
            sliders.append(Slider((0, 0, 10, 40), "Haunch depth at piers d_pier (m)", 2.5, 6.5,
                                  b.d_pier, self._set_dpier, "{:.1f}", 0.1))
            sliders.append(Slider((0, 0, 10, 40), "Depth at tips / mid-span d_tip (m)", 1.5, 3.5,
                                  b.d_tip, self._set_dtip, "{:.1f}", 0.1))
        if not b.stitched:
            sliders.append(Slider((0, 0, 10, 40), "Post-tensioning level (0 none, 1 light, 2 heavy)",
                                  0, 2, b.pt_level, self._set_pt, "{:.0f}", 1))
        self.drawer.show("Girder & piers", self.cards(), sliders)

    def _set_dpier(self, v):
        self.bridge.d_pier = v

    def _set_dtip(self, v):
        self.bridge.d_tip = v

    def _set_pt(self, v):
        self.bridge.pt_level = int(round(v))

    def cards(self):
        b = self.bridge
        c = b.cfg
        I_p, I_t = rect_I(c.width, b.d_pier), rect_I(c.width, b.d_tip)
        cards = [Card("Second moment of area", "I = b d^3 / 12",
                      f"pier: {c.width} x {b.d_pier:.1f}^3 / 12 = {I_p:.2f} m^4;  tip: {I_t:.2f} m^4",
                      f"deep haunch is {I_p/I_t:.1f}x stiffer than the tip")]
        for p, name in ((0, "A"), (1, "B")):
            chk = self.last_check[p] or b.check_pier(p)
            cards.append(Card(f"Pier {name}: see-saw balance",
                              "Sum M = Sum W_right x - Sum W_left x",
                              f"right arm {b.arm_moment(p, 1)/1e6:.1f}, left arm {b.arm_moment(p, -1)/1e6:.1f} MN*m",
                              f"unbalance {chk.overturning/1e6:+.1f} of +/-{b.capacity(p)/1e6:.0f} MN*m"
                              + ("  (landed on abutment)" if b.propped(p) else ""),
                              GOOD if abs(chk.overturning) < 0.7 * b.capacity(p) else WARN))
            cards.append(Card(f"Pier {name}: root bending", "sigma = M y / I",
                              f"M = {chk.root_moment/1e6:.1f} MN*m, y = {b.d_pier/2:.2f} m, I = {I_p:.2f} m^4",
                              f"sigma = {chk.root_stress/1e6:.1f} MPa (limit {c.allow_tension_build/1e6:.0f})",
                              GOOD if chk.root_stress < 0.8 * c.allow_tension_build else WARN))
        if b.stitched and self.girder:
            ratio, x, _, info = self.girder
            cards.append(Card("Continuous girder (after stitch)", "sigma = M y / I,  tau = V Q / (I t)",
                              info, f"worst {ratio*100:.0f}% at x = {x:.0f} m",
                              GOOD if ratio < 0.8 else (WARN if ratio <= 1 else BAD)))
        cards.append(Card("Post-tensioning", "allowed tension = f_t + sigma_pt",
                          f"{c.concrete_tension/1e6:.0f} + {c.pt_levels[b.pt_level]/1e6:.0f} MPa",
                          f"level: {PT_NAMES[b.pt_level]} ({economy.format_rs(PT_RS[b.pt_level])})"))
        return cards

    # --- actions ----------------------------------------------------------------------------
    def cast(self, pier, side):
        b = self.bridge
        if self.truck or b.stitched or self.overlay:
            return
        if b.arm_complete(pier, side):
            self.say("That arm is complete")
            return
        chk = b.add_segment(pier, side)
        self.history.append((pier, side))
        self.last_check[pier] = chk
        t = len(self.history)
        self.balance_hist[f"pier {'AB'[pier]} MN*m"].append((t, chk.overturning / 1e6))
        sound.play("click")
        if not chk.ok:
            self.tilt[pier] = math.copysign(0.06, chk.overturning) if chk.failure == "overturn" else 0.0
            rep = FailureReport(chk.failure, chk.message.split(":")[0], chk.message,
                                [f"Segments cast so far: {t}. Capacity = {b.cfg.base_capacity/1e6:.0f} "
                                 f"+ {b.tie_downs[pier]} tie-down(s) x {b.cfg.tie_down_capacity/1e6:.0f} MN*m"],
                                t, ("pier", pier), dict(self.balance_hist), build_cost=self.cost())
            self.fail(rep)
        self.show_girder_panel()

    def tie(self, pier):
        if self.bridge.stitched or self.truck:
            return
        self.bridge.tie_downs[pier] += 1
        sound.play("click")
        self.show_girder_panel()

    def undo(self):
        if self.truck or self.bridge.stitched:
            if self.bridge.stitched and not self.truck:
                self.bridge.stitched = False
                self.girder = None
                self.show_girder_panel()
            return
        if self.history:
            p, s = self.history.pop()
            self.bridge.segments[(p, s)] -= 1
            self.last_check[p] = None
            self.tilt[p] = 0.0
            self.show_girder_panel()

    def reset_after_failure(self):
        if self.truck:
            self.truck = None
            return
        self.undo()

    def stitch(self):
        b = self.bridge
        if not b.ready_to_stitch():
            missing = [f"{'AB'[p]}{'<' if s < 0 else '>'}" for p in range(2) for s in (-1, 1)
                       if not b.arm_complete(p, s)]
            self.say("Finish every arm first: " + ", ".join(missing))
            return
        b.stitched = True
        self.bundle = b.beam_model()
        self.girder = b.girder_check(None, self.bundle)
        sound.play("kaching")
        self.say("Stitched! The two T-frames are now one continuous beam.")
        self.show_girder_panel()

    def start_truck(self):
        if not self.bridge.stitched:
            self.say("Stitch the girder before the truck test")
            return
        if self.truck is None and self.overlay is None:
            def go():
                self.truck = -12.0
                self.truck_worst = 0.0
                self.truck_hist = {"girder %": []}
            self.finance_gate(go)

    def update_world(self, dt):
        self.tick += 1
        if self.demo_active and self.demo_queue:
            self._demo_step(dt)
        b = self.bridge
        for (p, s), btn in self.cast_btns.items():
            btn.enabled = not b.arm_complete(p, s) and not b.stitched
        self.stitch_btn.enabled = b.ready_to_stitch() and not b.stitched
        if self.truck is not None:
            self.truck += 10.0 * dt
            self.girder = b.girder_check(self.truck, self.bundle)
            ratio = self.girder[0]
            self.truck_worst = max(self.truck_worst, ratio)
            self.truck_hist["girder %"].append((self.truck, 100 * ratio))
            self.drawer.update_cards(self.cards())
            if ratio > 1.0:
                rep = FailureReport("girder", "GIRDER CRACKED under the truck", self.girder[3],
                                    ["More post-tensioning raises the allowed tension; a deeper "
                                     "tip raises I."], self.truck, ("girder", self.girder[1]),
                                    self.truck_hist, build_cost=self.cost())
                self.fail(rep)
                return
            if self.truck > b.cfg.abutments[1] + 14:
                self.truck = None
                worst = self.truck_worst
                fs = 1 / worst if worst else 9.9
                lines = [("Concrete", f"{b.concrete_volume():.0f} m^3", None),
                         ("Tie-downs", f"{sum(b.tie_downs)}", None),
                         ("Post-tensioning", PT_NAMES[b.pt_level], None),
                         ("Worst girder stress", f"{worst*100:.0f}% of allowed", None)]
                self.succeed(self.cost(), min(100, 50 * fs), 0.0, fs=fs, lines=lines)

    # --- drawing ---------------------------------------------------------------------------
    def draw_world(self, s):
        blueprint_background(s, (0, TOP_BAR, WIDTH, HEIGHT - TOP_BAR - BOTTOM_BAR))
        cam, b = self.cam, self.bridge
        a0, a1 = b.cfg.abutments
        v = self.level.cfg["view"]
        # canyon walls and floor
        for rect in ((v[0], v[1], a0, 0), (a1, v[1], v[2], 0), (a0, v[1], a1, FLOOR)):
            p, q = cam.to_screen(rect[0], rect[3]), cam.to_screen(rect[2], rect[1])
            r = pygame.Rect(p, (q[0] - p[0], q[1] - p[1]))
            pygame.draw.rect(s, ROCK, r)
            pygame.draw.rect(s, ROCK_EDGE, r, 1)
        # piers (tilted if failed)
        for p, x in enumerate(b.cfg.piers):
            tilt = self.tilt[p]
            top = (x, -b.d_pier)
            base = (x, FLOOR)
            def rot(pt, x=x, tilt=tilt):
                dx, dy = pt[0] - base[0], pt[1] - base[1]
                return cam.to_screen(base[0] + dx * math.cos(tilt) + dy * math.sin(tilt),
                                     base[1] - dx * math.sin(tilt) + dy * math.cos(tilt))
            poly = [rot((x - 1.5, FLOOR)), rot((x + 1.5, FLOOR)), rot((x + 1.5, top[1])), rot((x - 1.5, top[1]))]
            pygame.draw.polygon(s, (150, 150, 140), poly)
            pygame.draw.polygon(s, LINE, poly, 1)
            text(s, f"PIER {'AB'[p]}", cam.to_screen(x - 2.5, FLOOR + 3), 14, TEXT, bold=True)
            for k in range(b.tie_downs[p]):
                for sgn in (-1, 1):
                    pygame.draw.line(s, CYAN, cam.to_screen(x + sgn * 1.5, -b.d_pier),
                                     cam.to_screen(x + sgn * (6 + 2 * k), FLOOR), 2)
        # segments
        ratio_at = None
        if self.girder:
            _, _, res, _ = self.girder
            ratio_at = (res, b)
        for (p, side), count in b.segments.items():
            for k in range(count):
                xa, xb = b.segment_span(p, side, k)
                pts_top, pts_bot = [], []
                for i in range(7):
                    xx = xa + (xb - xa) * i / 6
                    pts_top.append((xx, 0.0))
                    pts_bot.append((xx, -b.depth_at(xx)))
                tilt = self.tilt[p]
                def tr(pt, x0=b.cfg.piers[p], tilt=tilt):
                    dx, dy = pt[0] - x0, pt[1] - FLOOR
                    return cam.to_screen(x0 + dx * math.cos(tilt) + dy * math.sin(tilt),
                                         FLOOR - dx * math.sin(tilt) + dy * math.cos(tilt))
                poly = [tr(q) for q in pts_top] + [tr(q) for q in reversed(pts_bot)]
                col = (185, 185, 172) if k % 2 == 0 else (170, 170, 160)
                if b.stitched and self.girder:
                    col = self._girder_colour((xa + xb) / 2)
                pygame.draw.polygon(s, col, poly)
                pygame.draw.polygon(s, (90, 90, 90), poly, 1)
            # traveller
            if count and not b.arm_complete(p, side) and not b.stitched:
                tip = b.cfg.piers[p] + side * count * b.cfg.seg_len
                q = cam.to_screen(tip, 0)
                pygame.draw.rect(s, ACCENT, (q[0] - (24 if side > 0 else 0), q[1] - 18, 24, 18), 2)
                pygame.draw.line(s, ACCENT, (q[0], q[1] - 18), (q[0] + side * 10, q[1] + 22), 2)
        # stitch marker
        mid = (b.cfg.piers[0] + b.cfg.piers[1]) / 2
        if b.stitched:
            p = cam.to_screen(mid, 0)
            pygame.draw.line(s, GOOD, (p[0], p[1] - 4), (p[0], p[1] + int(b.d_tip * cam.scale) + 4), 4)
        else:
            text(s, "close here", cam.to_screen(mid - 2.5, 2.2), 13, MUTED)
        # truck
        if self.truck is not None:
            for k, P in enumerate(b.cfg.truck_axles):
                xx = self.truck - k * b.cfg.truck_axle_gap
                pygame.draw.circle(s, (20, 20, 25), cam.to_screen(xx, 0.5), 5)
            q0, q1 = cam.to_screen(self.truck - 5, 3), cam.to_screen(self.truck + 1, 0.8)
            pygame.draw.rect(s, (200, 90, 70), (q0[0], q0[1], q1[0] - q0[0], q1[1] - q0[1]))
        # moment diagram strip
        self.draw_moments(s)
        self.draw_meters(s)

    def _girder_colour(self, x):
        b = self.bridge
        _, _, res, _ = self.girder
        k = int(np.argmin(np.abs(res.x - x)))
        d = b.depth_at(x)
        sigma = abs(res.M[k]) * (d / 2) / rect_I(b.cfg.width, d)
        r = sigma / b.allowable_tension()
        if r > 1:
            return (255, 40, 40)
        if r >= 0.8:
            return (235, 70, 60)
        if r >= 0.5:
            return (245, 200, 50)
        return (110, 200, 120)

    def draw_moments(self, s):
        b = self.bridge
        area = pygame.Rect(16, HEIGHT - BOTTOM_BAR - 104, WIDTH - 450, 96)
        panel(s, area, BG_DARK, PANEL_EDGE, 6)
        a0, a1 = b.cfg.abutments
        if b.stitched and self.girder:
            res = self.girder[2]
            xs, Ms = res.x, res.M
            title = "Bending moment M(x) of the continuous girder (sagging up, hogging down)"
        else:
            xs, Ms = [], []
            for i in range(0, 133):
                x = a0 + (a1 - a0) * i / 132
                M = 0.0
                for p, xp in enumerate(b.cfg.piers):
                    side = 1 if x > xp else -1
                    dist = abs(x - xp)
                    n = b.segments[(p, side)]
                    if dist <= n * b.cfg.seg_len and dist <= b.arm_target(p, side) + 1e-6:
                        # hogging moment from the part of the arm beyond x
                        for k in range(n):
                            xa, xb = b.segment_span(p, side, k)
                            xm = (xa + xb) / 2
                            if abs(xm - xp) > dist:
                                M -= b.segment_weight(p, side, k) * (abs(xm - xp) - dist)
                xs.append(x)
                Ms.append(M)
            title = "Cantilever moments while building (all hogging: the top is pulled)"
        text(s, title, (area.x + 8, area.y + 4), 13, MUTED)
        if len(xs) > 1:
            mmax = max(1.0, max(abs(m) for m in Ms))
            mid = area.y + 56
            pts = [(area.x + 10 + (x - a0) / (a1 - a0) * (area.w - 20), mid - m / mmax * 34) for x, m in zip(xs, Ms)]
            pygame.draw.line(s, MUTED, (area.x + 10, mid), (area.right - 10, mid), 1)
            pygame.draw.lines(s, CYAN, False, pts, 2)
            text(s, f"max |M| = {mmax/1e6:.1f} MN*m", (area.right - 10, area.y + 4), 13, CYAN, anchor="topright")

    def draw_meters(self, s):
        b = self.bridge
        for p in range(2):
            r = panel(s, (16 + p * 250, TOP_BAR + 10, 236, 96), BG_DARK, PANEL_EDGE, 8)
            chk = self.last_check[p] or b.check_pier(p)
            cap = b.capacity(p)
            frac = max(-1.2, min(1.2, chk.overturning / cap))
            text(s, f"PIER {'AB'[p]} see-saw", (r.x + 10, r.y + 6), 14, TEXT, bold=True)
            cx, cy = r.x + 118, r.y + 82
            pygame.draw.arc(s, MUTED, (cx - 60, cy - 60, 120, 120), math.radians(20), math.radians(160), 3)
            for lim, col in ((1, BAD), (-1, BAD)):
                ang = math.radians(90 - 60 * lim)
                pygame.draw.line(s, col, (cx + 50 * math.cos(ang), cy - 50 * math.sin(ang)),
                                 (cx + 62 * math.cos(ang), cy - 62 * math.sin(ang)), 3)
            ang = math.radians(90 - 60 * frac)
            col = GOOD if abs(frac) < 0.7 else (WARN if abs(frac) <= 1 else BAD)
            pygame.draw.line(s, col, (cx, cy), (cx + 52 * math.cos(ang), cy - 52 * math.sin(ang)), 4)
            text(s, f"{chk.overturning/1e6:+.1f} / {cap/1e6:.0f} MN*m", (r.x + 10, r.y + 24), 13, col)
            if b.propped(p):
                text(s, "landed", (r.right - 10, r.y + 6), 13, GOOD, anchor="topright")
        if self.truck is not None or (self.bridge.stitched and getattr(self, "truck_hist", None)):
            hist = getattr(self, "truck_hist", {}).get("girder %", [])
            if hist:
                mini_chart(s, (520, TOP_BAR + 10, 300, 96), [hist], [BAD], "girder % vs truck x", limit=100)
