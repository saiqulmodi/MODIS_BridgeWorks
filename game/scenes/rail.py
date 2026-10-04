"""Railway levels (2 Timber Incline, 4 Freight Mountain Pass): shape the track, pick the
train, and watch gravity, friction, power and momentum fight it out."""
import math

import pygame

from engine import economy
from engine.failure import FailureReport
from engine.vehicles import G, braking_distance, max_climbable_grade, tractive_effort

from .. import sound
from ..common import Card, LevelScene
from ..rail_sim import (LOCOS, RailDesign, RailSim, cost, default_design, fixed_station, grades,
                        ground_height, train_spec)
from ..help_texts import HELP, LOCO
from ..ui import (ACCENT, BAD, BG_DARK, BOTTOM_BAR, CYAN, DRAWER_W, GOOD, HEIGHT, LINE, MUTED,
                  PANEL_EDGE, TEXT, TOP_BAR, WARN, WIDTH, Button, Cycler, blueprint_background,
                  mini_chart, panel, text)

EARTH = (92, 74, 56)
EARTH_EDGE = (150, 120, 90)


class ProfileCamera:
    """Separate horizontal and vertical scales: hills are drawn taller than life so the
    slopes are easy to see (the HUD always shows the true angle)."""

    def __init__(self, view):
        x0, y0, x1, y1 = view
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.area = pygame.Rect(16, TOP_BAR + 150, WIDTH - DRAWER_W - 60, HEIGHT - TOP_BAR - BOTTOM_BAR - 180)
        self.sx = self.area.w / (x1 - x0)
        self.sy = self.area.h / (y1 - y0)
        self.exaggeration = self.sy / self.sx

    def to_screen(self, x, y):
        return (int(self.area.x + (x - self.x0) * self.sx), int(self.area.bottom - (y - self.y0) * self.sy))

    def to_world(self, px, py):
        return ((px - self.area.x) / self.sx + self.x0, (self.area.bottom - py) / self.sy + self.y0)


class RailScene(LevelScene):
    CONTROLS = ("Drag the round handles up/down to shape the track (cuttings and embankments "
                "cost money). Pick a locomotive and the number of wagons. Click a track segment "
                "to see the slope maths. SPACE runs the train.")

    DEMO_STATE = ("design",)

    def __init__(self, app, level):
        super().__init__(app, level)
        self.cfg = level.cfg
        self.cam = ProfileCamera(self.cfg["view"])
        self.design = default_design(self.cfg)
        self.drag = None
        self.drag_brake = False
        self.sim = None
        self.mode = "edit"
        self.selected_seg = None
        self.speed = 1
        self.tick = 0
        self.rain = [(i * 37 % 997, i * 53 % 613) for i in range(90)]
        self._build_toolbar()
        self.select_train()

    def _build_toolbar(self):
        y = HEIGHT - BOTTOM_BAR + 9
        x = 10
        self.loco_cycler = self.widgets.add(Cycler((x, y, 210, 40), "", self.cfg["locos"],
                                                   on_change=self._loco, size=15, hotkey=pygame.K_l,
                                                   help=lambda: LOCO.get(self.loco_cycler.value, "")))
        x += 216
        self.widgets.add(Button((x, y, 40, 40), "-", lambda: self._wagons(-1), size=20,
                                help=HELP["wagon_minus"]))
        x += 44
        self.wagon_label_x = x
        x += 110
        self.widgets.add(Button((x, y, 40, 40), "+", lambda: self._wagons(1), size=20,
                                help=HELP["wagon_plus"]))
        x += 50
        if self.cfg.get("banker"):
            self.banker_btn = self.widgets.add(Button((x, y, 170, 40),
                                                      f"Banker engine (+{economy.format_rs(250000)})",
                                                      self._banker, toggle=True, size=13,
                                                      help=HELP["banker"]))
            x += 176
        self.widgets.add(Button((x, y, 120, 40), "Even grade", self.even_grade, size=14,
                                help=HELP["even_grade"]))
        x += 126
        self.widgets.add(Button((x, y, 110, 40), "Follow hill", self.follow_ground, size=14,
                                help=HELP["follow_hill"]))
        x += 116
        self.speed_btn = self.widgets.add(Button((x, y, 52, 40), "x1", self.cycle_speed, size=14,
                                                 help=HELP["speed"]))
        x += 56
        self.run_btn = self.widgets.add(Button((x, y, WIDTH - x - 10, 40), "RUN", self.toggle_run,
                                               hotkey=pygame.K_SPACE, colour=(40, 110, 70),
                                               help=HELP["run_rail"]))

    # --- demonstration ----------------------------------------------------------------------
    def demo_prepare(self):
        if self.mode != "edit":
            self.reset_after_failure()

    def load_demo(self):
        hs = [ground_height(self.cfg, x) for x in self.cfg["stations"]]
        if self.level.num == 2:
            self.design = RailDesign(hs, "Diesel shunter", 2)
        else:
            self.design = RailDesign(hs, "Mainline diesel", 5, False, 340)
        self.after_demo()

    def run_demo(self):
        self.toggle_run()

    def after_demo(self):
        self.loco_cycler.set(self.design.loco)
        if getattr(self, "banker_btn", None):
            self.banker_btn.active = self.design.banker
        self.select_train()

    # --- design changes ---------------------------------------------------------------------
    def _loco(self, name):
        self.design.loco = name
        self.select_train()

    def _wagons(self, dv):
        if self.mode != "edit":
            return
        self.design.wagons = max(1, min(self.cfg["max_wagons"], self.design.wagons + dv))
        self.select_train()

    def _banker(self):
        self.design.banker = self.banker_btn.active
        self.select_train()

    def even_grade(self):
        if self.mode != "edit":
            return
        st = self.cfg["stations"]
        (a0, a1), (b0, b1) = self.cfg["fixed_ends"]
        ia, ib = st.index(a1), st.index(b0)
        ha, hb = self.design.heights[ia], self.design.heights[ib]
        for i in range(ia + 1, ib):
            self.design.heights[i] = round((ha + (hb - ha) * (st[i] - st[ia]) / (st[ib] - st[ia])) * 2) / 2
        self.select_train()

    def follow_ground(self):
        if self.mode != "edit":
            return
        self.design.heights = [ground_height(self.cfg, x) for x in self.cfg["stations"]]
        self.select_train()

    def cycle_speed(self):
        self.speed = {1: 2, 2: 4, 4: 1}[self.speed]
        self.speed_btn.label = f"x{self.speed}"

    def cost(self):
        return cost(self.cfg, self.design).total

    # --- calculator ------------------------------------------------------------------------
    def select_train(self):
        self.selected_seg = None
        self.drawer.show(f"Train: {train_spec(self.cfg, self.design).name}", self.train_cards())

    def train_cards(self):
        sp = train_spec(self.cfg, self.design)
        mt = max_climbable_grade(sp)
        mt_wet = max_climbable_grade(sp, wet=True)
        steep = max(grades(self.cfg, self.design))
        cards = [
            Card("Train", f"m = {sp.mass/1e3:.0f} t  (loco {sp.driven_mass/1e3:.0f} t drives)",
                 f"P = {sp.power/1e3:.0f} kW, cargo {sp.cargo:.0f} t per trip"),
            Card("Steepest slope it can climb", "mu m_loco g cos(theta) = m g sin(theta) + C_rr m g",
                 f"tan(theta) = {sp.mu_dry} x {sp.driven_mass/1e3:.0f} / {sp.mass/1e3:.0f} - {sp.C_rr}",
                 f"theta_max = {math.degrees(mt):.1f} deg dry, {math.degrees(mt_wet):.1f} deg wet; "
                 f"your steepest = {steep:.1f} deg",
                 GOOD if math.radians(steep) < mt * 0.95 else (WARN if math.radians(steep) <= mt else BAD)),
        ]
        trips = math.ceil(self.cfg["cargo_target"] / sp.cargo) if sp.cargo else 0
        cards.append(Card("Trips needed", f"ceil({self.cfg['cargo_target']:.0f} t / {sp.cargo:.0f} t)", "",
                          f"{trips} trip(s), time limit {self.cfg['time_limit']/60:.0f} min"))
        c = cost(self.cfg, self.design)
        cards.append(Card("Cost", "track + cuttings + embankments + hire",
                          f"track {economy.format_rs(c.track)}, cut {c.cut_m2:.0f} m^2 = "
                          f"{economy.format_rs(c.cut)}, fill {c.fill_m2:.0f} m^2 = {economy.format_rs(c.fill)}",
                          f"loco {economy.format_rs(c.loco)}, wagons {economy.format_rs(c.wagons)}"))
        if self.cfg.get("brake_marker"):
            d, mu, th = RailSim(self.cfg, self.design).predicted_brake_distance()
            room = self.cfg["stop_x"] - self.design.brake_x
            cards.append(Card("Braking distance (wet rails)", "d = v^2 / (2 (mu g cos(theta) - g sin(theta)))",
                              f"v = {sp.max_speed:.0f} m/s, mu = {mu:.2f}, theta = {math.degrees(th):.1f} deg down",
                              f"d = {d:.0f} m needed;  your marker gives {room:.0f} m",
                              GOOD if room >= d else BAD))
        return cards

    def segment_cards(self, i):
        st, hs = self.cfg["stations"], self.design.heights
        th = math.atan2(hs[i + 1] - hs[i], st[i + 1] - st[i])
        sp = train_spec(self.cfg, self.design)
        mg = sp.mass * G
        v = sp.max_speed * 0.4
        T = tractive_effort(sp.power, v, sp.mu_dry, sp.driven_mass * G * math.cos(th))
        need = mg * math.sin(th) + sp.C_rr * mg * math.cos(th)
        return [
            Card("Slope", "theta = atan(rise / run)", f"= atan({hs[i+1]-hs[i]:+.1f} / {st[i+1]-st[i]:.0f})",
                 f"theta = {math.degrees(th):+.2f} deg ({100*math.tan(th):+.1f}%)"),
            Card("Gravity along the track", "F = m g sin(theta)", f"= {mg/1e3:.0f} kN x {math.sin(th):.3f}",
                 f"{mg*math.sin(th)/1e3:+.1f} kN pulling back"),
            Card("Normal force & grip", "N = m g cos(theta);  F_grip = mu N_loco",
                 f"N_loco = {sp.driven_mass*G*math.cos(th)/1e3:.0f} kN",
                 f"grip limit = {sp.mu_dry*sp.driven_mass*G*math.cos(th)/1e3:.0f} kN (dry)"),
            Card(f"Engine pull at {v:.1f} m/s", "T = min(P / v, mu N)", f"P / v = {sp.power/v/1e3:.0f} kN",
                 f"T = {T/1e3:.0f} kN vs needed {need/1e3:.0f} kN", GOOD if T > need else BAD),
            Card("Balancing speed (power-limited)", "P = F v  ->  v = P / (m g (sin + C_rr cos))", "",
                 f"v = {sp.power/max(need, 1):.1f} m/s" if need > 0 else "downhill: speeds up"),
        ]

    def live_cards(self):
        e = self.sim.engine
        f = e.forces
        sp = self.sim.spec
        return [
            Card("Speed & momentum", "p = m v", f"v = {e.v:.1f} m/s ({e.v*3.6:.0f} km/h)",
                 f"p = {e.momentum/1e3:.0f} kN s"),
            Card("Forces right now", "m a = T - F_rr - F_drag - F_brake - m g sin(theta)",
                 f"T {f.traction/1e3:.0f}, rr {f.rolling/1e3:.1f}, drag {f.drag/1e3:.1f}, brake "
                 f"{f.brake/1e3:.0f}, gravity {f.gravity/1e3:+.0f} kN",
                 f"a = {e.acceleration:+.3f} m/s^2" + ("   WHEEL SLIP" if f.wheel_slip else "")),
            Card("Energy", "PE = m g h,  KE = 1/2 m v^2", f"engine work {e.engine_work/1e6:.2f} MJ",
                 f"PE {e.potential_energy/1e6:.2f} MJ, KE {e.kinetic_energy/1e6:.2f} MJ, heat {e.heat/1e6:.2f} MJ"),
            Card("Rails", "mu = 0.30 dry, 0.18 wet", "", "WET (rain)" if e.wet else "dry", CYAN if e.wet else TEXT),
        ]

    # --- input ---------------------------------------------------------------------------
    def handle_world(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.mode != "edit":
                return
            if self.cfg.get("brake_marker"):
                bx, by = self.cam.to_screen(self.design.brake_x, self._track_h(self.design.brake_x))
                if abs(event.pos[0] - bx) < 12 and by - 60 < event.pos[1] < by + 10:
                    self.drag_brake = True
                    return
            for i, x in enumerate(self.cfg["stations"]):
                px, py = self.cam.to_screen(x, self.design.heights[i])
                if math.hypot(px - event.pos[0], py - event.pos[1]) < 12 and not fixed_station(self.cfg, i):
                    self.drag = i
                    return
            # click on a segment -> slope maths
            wx, _ = self.cam.to_world(*event.pos)
            st = self.cfg["stations"]
            for i in range(len(st) - 1):
                if st[i] <= wx <= st[i + 1]:
                    self.selected_seg = i
                    self.drawer.show(f"Track {st[i]}-{st[i+1]} m", self.segment_cards(i))
                    return
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.drag is not None or self.drag_brake:
                self.drag = None
                self.drag_brake = False
                self.select_train()
        elif event.type == pygame.MOUSEMOTION:
            if self.drag is not None:
                _, wy = self.cam.to_world(*event.pos)
                v = self.cfg["view"]
                self.design.heights[self.drag] = max(v[1] + 1, min(v[3] - 1, round(wy * 2) / 2))
            elif self.drag_brake:
                wx, _ = self.cam.to_world(*event.pos)
                self.design.brake_x = max(self.cfg["stations"][1], min(self.cfg["stop_x"] - 5, round(wx)))

    def _track_h(self, x):
        st, hs = self.cfg["stations"], self.design.heights
        for i in range(len(st) - 1):
            if st[i] <= x <= st[i + 1]:
                return hs[i] + (hs[i + 1] - hs[i]) * (x - st[i]) / (st[i + 1] - st[i])
        return hs[-1]

    # --- run -------------------------------------------------------------------------------
    def toggle_run(self):
        if self.overlay is not None:
            return
        if self.mode == "edit":
            def go():
                self.sim = RailSim(self.cfg, self.design)
                self.mode = "run"
                self.run_btn.label = "STOP"
                sound.play("whoosh")
            self.finance_gate(go)
        else:
            self.reset_after_failure()

    def reset_after_failure(self):
        self.mode = "edit"
        self.sim = None
        self.run_btn.label = "RUN"
        self.select_train()

    def update_world(self, dt):
        self.tick += 1
        if self.mode != "run":
            return
        for _ in range(self.speed):
            self.sim.step(min(dt, 1 / 30))
            if self.sim.failure or self.sim.done:
                break
        if "brake" in self.sim.events:
            sound.play("groan")
        self.sim.events.clear()
        self.drawer.subject = f"Train: {self.sim.spec.name}"
        self.drawer.update_cards(self.live_cards())
        if self.sim.failure:
            self.mode = "frozen"
            self.run_btn.label = "EDIT"
            self.fail(self.sim.failure)
        elif self.sim.done:
            self.mode = "frozen"
            self.run_btn.label = "EDIT"
            self._finish()

    def _finish(self):
        s = self.sim
        total = s.total_time()
        c = self.cost()
        if total > self.cfg["time_limit"]:
            self.fail(FailureReport("timeout", "TOO SLOW: the job missed its deadline",
                                    f"{s.trips} trips x {s.trip_time:.0f} s + returns = {total:.0f} s > "
                                    f"{self.cfg['time_limit']:.0f} s",
                                    ["Carry more per trip (more power or gentler grades) or move faster."],
                                    s.time, None, s.history, build_cost=c))
            return
        extra = True
        lines = [("Trips x cargo", f"{s.trips} x {s.cargo_per_trip:.0f} t", None),
                 ("Job time", f"{total:.0f} s of {self.cfg['time_limit']:.0f} s", None),
                 ("Energy: engine work", f"{s.engine.engine_work/1e6:.1f} MJ per trip", None),
                 ("Heat lost to friction/brakes", f"{s.engine.heat/1e6:.1f} MJ", None)]
        if s.stop_error is not None:
            extra = abs(s.stop_error) <= 15
            lines.append(("Stopping accuracy", f"{s.stop_error:+.1f} m from the stop line",
                          GOOD if extra else WARN))
        safety = 100 - 2 * max(0.0, max(grades(self.cfg, self.design)))
        self.succeed(c, safety, total, extra_goal=extra, lines=lines)

    # --- drawing ---------------------------------------------------------------------------
    def draw_world(self, s):
        blueprint_background(s, (0, TOP_BAR, WIDTH, HEIGHT - TOP_BAR - BOTTOM_BAR))
        cam, cfg = self.cam, self.cfg
        # ground
        pts = [cam.to_screen(x, y) for x, y in cfg["ground"]]
        poly = [cam.to_screen(cfg["ground"][0][0], cfg["view"][1])] + pts + \
               [cam.to_screen(cfg["ground"][-1][0], cfg["view"][1])]
        pygame.draw.polygon(s, EARTH, poly)
        pygame.draw.lines(s, EARTH_EDGE, False, pts, 2)
        # rain zone
        if cfg.get("wet_after_x") is not None:
            x0 = cam.to_screen(cfg["wet_after_x"], 0)[0]
            for (rx, ry) in self.rain:
                px = x0 + rx % max(1, cam.area.right - x0)
                py = cam.area.y + (ry + self.tick * 6) % cam.area.h
                pygame.draw.line(s, (120, 170, 230), (px, py), (px - 3, py + 9), 1)
            text(s, "RAIN: wet rails, mu = 0.18", (x0 + 6, cam.area.y + 4), 14, CYAN)
        # track: earthworks shading then rails
        st, hs = cfg["stations"], self.design.heights
        tp = [cam.to_screen(x, h) for x, h in zip(st, hs)]
        for i in range(len(st) - 1):
            for x in range(int(st[i]), int(st[i + 1]), 2):
                h = self._track_h(x + 1)
                g = ground_height(cfg, x + 1)
                a, b = cam.to_screen(x + 1, h), cam.to_screen(x + 1, g)
                pygame.draw.line(s, (150, 110, 70) if h > g else (60, 44, 32), a, b, max(1, int(cam.sx * 2)))
        pygame.draw.lines(s, (30, 30, 34), False, tp, 7)
        pygame.draw.lines(s, LINE, False, tp, 3)
        sp = train_spec(cfg, self.design)
        mt = math.degrees(max_climbable_grade(sp))
        for i, gdeg in enumerate(grades(cfg, self.design)):
            mx = (tp[i][0] + tp[i + 1][0]) // 2
            my = min(tp[i][1], tp[i + 1][1]) - 18
            col = BAD if gdeg > mt else (WARN if gdeg > 0.8 * mt else MUTED)
            if gdeg < -1:
                col = CYAN
            text(s, f"{gdeg:+.1f}", (mx, my), 13, col, anchor="center")
            if self.selected_seg == i:
                pygame.draw.line(s, ACCENT, tp[i], tp[i + 1], 5)
        for i, p in enumerate(tp):
            fixed = fixed_station(cfg, i)
            pygame.draw.circle(s, MUTED if fixed else ACCENT, p, 6 if fixed else 8)
            if self.drag == i:
                pygame.draw.circle(s, LINE, p, 12, 2)
        # stations, stop line, buffers, brake marker
        for x, label in ((cfg["start_x"], "START"), (cfg.get("end_x"), "YARD")):
            if x is not None and not cfg.get("brake_marker") or label == "START":
                p = cam.to_screen(x, self._track_h(x))
                pygame.draw.line(s, GOOD, p, (p[0], p[1] - 40), 2)
                text(s, label, (p[0] + 4, p[1] - 44), 13, GOOD)
        if cfg.get("brake_marker"):
            p = cam.to_screen(cfg["stop_x"], self._track_h(cfg["stop_x"]))
            pygame.draw.line(s, GOOD, p, (p[0], p[1] - 40), 3)
            text(s, "STOP", (p[0] + 4, p[1] - 44), 13, GOOD)
            q = cam.to_screen(cfg["buffer_x"], self._track_h(cfg["buffer_x"]))
            pygame.draw.rect(s, BAD, (q[0] - 4, q[1] - 16, 8, 16))
            text(s, "BUFFER", (q[0] - 20, q[1] - 34), 12, BAD)
            b = cam.to_screen(self.design.brake_x, self._track_h(self.design.brake_x))
            pygame.draw.line(s, WARN, b, (b[0], b[1] - 50), 3)
            pygame.draw.polygon(s, WARN, [(b[0], b[1] - 50), (b[0] + 18, b[1] - 44), (b[0], b[1] - 38)])
            text(s, "BRAKE", (b[0] + 4, b[1] - 66), 13, WARN)
            d, _, _ = RailSim(cfg, self.design).predicted_brake_distance()
            if math.isfinite(d):
                e = cam.to_screen(min(self.design.brake_x + d, cfg["view"][2]),
                                  self._track_h(min(self.design.brake_x + d, cfg["view"][2])))
                pygame.draw.line(s, WARN, (b[0], b[1] + 10), (e[0], e[1] + 10), 2)
                text(s, f"d_stop ~ {d:.0f} m", (b[0], b[1] + 14), 12, WARN)
        text(s, f"vertical scale x{cam.exaggeration:.1f}", (cam.area.x, cam.area.bottom + 4), 12, MUTED)
        if self.sim:
            self.draw_train(s)
            self.draw_energy(s)
        else:
            text(s, f"Train: {sp.name}  -  {sp.mass/1e3:.0f} t, {sp.power/1e3:.0f} kW, can climb "
                    f"{mt:.1f} deg", (20, TOP_BAR + 12), 17, TEXT, bold=True)
            text(s, "Grade labels: red = too steep for this train, yellow = close, blue = downhill",
                 (20, TOP_BAR + 36), 14, MUTED)

    def draw_bottom_bar(self, surface):
        super().draw_bottom_bar(surface)
        text(surface, f"Wagons: {self.design.wagons}", (self.wagon_label_x + 8, HEIGHT - BOTTOM_BAR + 20),
             16, TEXT, bold=True)

    def draw_train(self, s):
        e = self.sim.engine
        sp = self.sim.spec
        loco_len = sp.length - self.design.wagons * 14
        cars = [(0, loco_len, (230, 120, 50))]
        pos = loco_len
        for _ in range(self.design.wagons):
            cars.append((pos + 1, pos + 14, (120, 160, 90)))
            pos += 14
        for a, b, col in cars:
            p = self.cam.to_screen(*e.path.point_at(e.s - a))
            q = self.cam.to_screen(*e.path.point_at(e.s - b))
            pygame.draw.line(s, (20, 20, 25), p, q, 16)
            pygame.draw.line(s, col, (p[0], p[1] - 4), (q[0], q[1] - 4), 12)
        if self.sim.phase == "brake" and e.v > 0.5 and self.tick % 4 < 2:
            p = self.cam.to_screen(*e.path.point_at(e.s - 3))
            pygame.draw.circle(s, ACCENT, (p[0], p[1] + 4), 4)

    def draw_energy(self, s):
        e = self.sim.engine
        r = panel(s, (16, TOP_BAR + 8, 420, 130), BG_DARK, PANEL_EDGE, 8)
        text(s, f"v = {e.v*3.6:5.1f} km/h   a = {e.acceleration:+.2f} m/s^2   p = {e.momentum/1e3:,.0f} kN s",
             (r.x + 10, r.y + 6), 15, TEXT, bold=True)
        total = max(e.engine_work, abs(e.potential_energy) + e.kinetic_energy + e.heat, 1.0)
        bars = [("PE m g h", e.potential_energy, CYAN), ("KE 1/2 m v^2", e.kinetic_energy, GOOD),
                ("Heat (friction)", e.heat, BAD), ("Engine work", e.engine_work, ACCENT)]
        for k, (label, val, col) in enumerate(bars):
            y = r.y + 32 + k * 23
            text(s, label, (r.x + 10, y), 13, MUTED)
            w = int(200 * max(val, 0) / total)
            pygame.draw.rect(s, col, (r.x + 130, y + 3, w, 13))
            text(s, f"{val/1e6:.2f} MJ", (r.x + 410, y), 13, TEXT, anchor="topright")
        mini_chart(s, (450, TOP_BAR + 8, 300, 130), [self.sim.history["speed m/s"]], [GOOD], "speed m/s")
