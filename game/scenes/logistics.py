"""Level 9 - Heavy Industrial Corridor: split 6000 t between road, rail and barge, size the
fleets, and find a plan on the Pareto frontier of cost, time and safety."""
import math

import pygame

from engine import economy
from engine.failure import FailureReport
from engine.logistics import (BARGE_T, RAIL_GRADE, RAIL_KM, RIVER_KM, ROAD_KM, TRUCK_T, Plan,
                              evaluate, search_frontier, train_grade_speed, train_spec,
                              truck_speed_kmh)
from engine.vehicles import G, max_climbable_grade

from .. import sound
from ..common import Card, LevelScene
from ..ui import (ACCENT, BAD, BG_DARK, BOTTOM_BAR, CYAN, GOOD, HEIGHT, LINE, MUTED, PANEL_EDGE,
                  TEXT, TOP_BAR, WARN, WIDTH, Button, Slider, WidgetGroup, blueprint_background,
                  panel, text)

MAP_X0, MAP_X1 = 110, 800
Y_ROAD, Y_RAIL, Y_RIVER = TOP_BAR + 70, TOP_BAR + 150, TOP_BAR + 230


class LogisticsScene(LevelScene):
    CONTROLS = ("Use the sliders to share the 6000 t between road, rail and barge and to hire "
                "fleets. The calculator shows each mode's physics. 'Optimizer' plots every "
                "feasible plan so you can see the Pareto frontier. RUN ships it.")

    def __init__(self, app, level):
        super().__init__(app, level)
        self.cfg = level.cfg
        self.total = self.cfg["total"]
        self.plan = Plan(road_t=self.total, rail_t=0, barge_t=0, trucks=60, rakes=1, wagons=30, barges=1)
        self.frontier = None
        self.state = "edit"
        self.t = 0.0
        self.panel_widgets = WidgetGroup()
        self._build()
        y = HEIGHT - BOTTOM_BAR + 9
        self.widgets.add(Button((10, y, 200, 40), "Optimizer: show all plans", self.optimize, size=14,
                                tooltip="Brute-force search (a stand-in for linear programming) over "
                                        "every split and fleet size."))
        self.run_btn = self.widgets.add(Button((216, y, WIDTH - 226, 40), "SHIP IT", self.toggle_run,
                                               hotkey=pygame.K_SPACE, colour=(40, 110, 70)))
        self.result = evaluate(self.plan)
        self.show_panel()

    def _build(self):
        p = self.plan
        x1, x2, y = 24, 300, TOP_BAR + 304
        def sl(x, yy, label, lo, hi, val, attr, fmt, step):
            self.panel_widgets.add(Slider((x, yy, 250, 40), label, lo, hi, val,
                                          lambda v, a=attr: self._set(a, v), fmt, step))
        sl(x1, y, "Rail share (t)", 0, self.total, p.rail_t, "rail_t", "{:.0f}", 250)
        sl(x1, y + 48, "Barge share (t)", 0, self.total, p.barge_t, "barge_t", "{:.0f}", 250)
        sl(x1, y + 96, "Trucks hired", 0, 200, p.trucks, "trucks", "{:.0f}", 5)
        sl(x2, y, "Trains (rakes)", 0, 4, p.rakes, "rakes", "{:.0f}", 1)
        sl(x2, y + 48, "Wagons per train", 10, 50, p.wagons, "wagons", "{:.0f}", 1)
        sl(x2, y + 96, "Barges", 0, 5, p.barges, "barges", "{:.0f}", 1)

    def _set(self, attr, v):
        if self.state != "edit":
            return
        p = self.plan
        if attr in ("rail_t", "barge_t"):
            setattr(p, attr, v)
            other = "barge_t" if attr == "rail_t" else "rail_t"
            if p.rail_t + p.barge_t > self.total:
                setattr(p, other, self.total - v)
            p.road_t = self.total - p.rail_t - p.barge_t
            for w in self.panel_widgets.items:
                if w.label.startswith("Rail share"):
                    w.value = p.rail_t
                if w.label.startswith("Barge share"):
                    w.value = p.barge_t
        else:
            setattr(p, attr, int(round(v)))
        self.result = evaluate(p)
        self.drawer.update_cards(self.cards())

    def cost(self):
        return self.result.cost

    def optimize(self):
        self.frontier = search_frontier(self.total)
        sound.play("click")
        ok = [x for x in self.frontier if x[1].hours <= self.cfg["deadline"]]
        if ok:
            best = min(ok, key=lambda x: x[1].cost)
            self.say(f"Cheapest plan meeting the deadline costs {economy.format_rs(best[1].cost)} - "
                     f"can you find it?", 5)

    # --- calculator -----------------------------------------------------------------------
    def show_panel(self):
        self.drawer.show("Freight plan", self.cards())

    def cards(self):
        p, r = self.plan, self.result
        sp = train_spec(p.wagons)
        cards = [
            Card("Road: truck speed (Greenshields)", "v = v_max (1 - k / k_jam)",
                 f"{p.trucks} trucks add density; v_max 70 km/h, k_jam 120 veh/km",
                 f"v = {truck_speed_kmh(p.trucks):.0f} km/h,  {math.ceil(p.road_t / TRUCK_T)} truck trips"),
            Card("Rail: speed on the 1.2% grade", "P / v = m g (sin(theta) + C_rr cos(theta))",
                 f"m = {sp.mass/1e6:.2f} kt, P = {sp.power/1e6:.1f} MW",
                 f"v = {train_grade_speed(p.wagons)*3.6:.0f} km/h"),
            Card("Rail: can it climb at all?", "mu m_loco g cos(theta) >= m g sin(theta) + C_rr m g",
                 f"grip {sp.mu_dry*sp.driven_mass*G/1e3:.0f} kN vs needed "
                 f"{sp.mass*G*(math.sin(RAIL_GRADE)+sp.C_rr)/1e3:.0f} kN",
                 "OK" if max_climbable_grade(sp) >= RAIL_GRADE else "STALLS - fewer wagons!",
                 GOOD if max_climbable_grade(sp) >= RAIL_GRADE else BAD),
            Card("Barge: speed over ground", "v = v_water +/- current", "3.0 m/s through water, 1.0 m/s current",
                 "14.4 km/h down to the port, 7.2 km/h back"),
        ]
        for m in r.modes:
            cards.append(Card(f"{m.name}: {m.tonnes:.0f} t", f"{m.trips} trips, round trip {m.round_h:.1f} h",
                              m.note, f"done in {m.hours:.1f} h, {economy.format_rs(m.cost)}"))
        toll = economy.toll(self.total, (ROAD_KM + RAIL_KM + RIVER_KM) / 3, max(r.hours, 0.1), max(r.fuel_l, 1))
        cards.append(Card("Plan totals", "time = slowest mode;  Toll = (t x km)/(h x L)",
                          f"{r.hours:.1f} h of {self.cfg['deadline']:.0f} h, fuel {r.fuel_l:,.0f} L, "
                          f"safety index {r.safety:.1f}",
                          f"cost {economy.format_rs(r.cost)};  toll score {toll:,.0f}",
                          GOOD if r.feasible and r.hours <= self.cfg["deadline"] else BAD))
        if r.problem:
            cards.append(Card("Problem", r.problem[:160], "", "", BAD))
        return cards

    # --- run -------------------------------------------------------------------------------
    def handle_world(self, event):
        if self.state == "edit":
            self.panel_widgets.handle(event)

    def toggle_run(self):
        if self.overlay is not None:
            return
        if self.state == "edit":
            self.state = "run"
            self.t = 0.0
            self.run_btn.label = "STOP"
            sound.play("whoosh")
        else:
            self.reset_after_failure()

    def reset_after_failure(self):
        self.state = "edit"
        self.run_btn.label = "SHIP IT"

    def update_world(self, dt):
        if self.state != "run":
            return
        r = self.result
        end = min(r.hours if math.isfinite(r.hours) else 1e9, self.cfg["deadline"] * 1.2)
        self.t += dt * max(end, 1.0) / 10.0          # play the whole job in ~10 seconds
        if r.problem and r.problem_kind == "stall" and self.t > 1.0:
            self.state = "frozen"
            self.fail(FailureReport("stall", "FREIGHT TRAIN STALLED ON THE GRADE", r.problem,
                                    ["One locomotive can only haul about 30 of these wagons up 1.2%."],
                                    self.t, build_cost=r.cost))
            return
        if self.t >= end:
            self.state = "frozen"
            self.run_btn.label = "EDIT"
            if not r.feasible or r.hours > self.cfg["deadline"]:
                self.fail(FailureReport("timeout", "MISSED THE 24-HOUR DEADLINE",
                                        f"The slowest mode finishes at {r.hours:.1f} h > {self.cfg['deadline']:.0f} h"
                                        if math.isfinite(r.hours) else r.problem or "A mode has freight but no vehicles",
                                        [f"{m.name}: {m.hours:.1f} h" for m in r.modes], self.t, build_cost=r.cost))
                return
            extra = r.safety >= self.cfg["safety_bonus"]
            lines = [(m.name, f"{m.tonnes:.0f} t in {m.hours:.1f} h, {economy.format_rs(m.cost)}", None)
                     for m in r.modes]
            lines += [("Safety index", f"{r.safety:.1f}", GOOD if extra else WARN),
                      ("Fuel", f"{r.fuel_l:,.0f} L", None)]
            self.succeed(r.cost, r.safety, r.hours * 3600, extra_goal=extra, lines=lines)

    # --- drawing ---------------------------------------------------------------------------
    def draw_world(self, s):
        blueprint_background(s, (0, TOP_BAR, WIDTH, HEIGHT - TOP_BAR - BOTTOM_BAR))
        p, r = self.plan, self.result
        # places
        for x, label in ((MAP_X0 - 60, "BHILWARA\nMINE"), (MAP_X1 + 10, "KANDLA\nPORT")):
            pygame.draw.rect(s, (60, 80, 110), (x, TOP_BAR + 40, 56, 220), border_radius=6)
            for k, line in enumerate(label.split("\n")):
                text(s, line, (x + 28, TOP_BAR + 130 + 16 * k), 12, TEXT, bold=True, anchor="center")
        # corridors
        pygame.draw.line(s, (90, 90, 100), (MAP_X0, Y_ROAD), (MAP_X1, Y_ROAD), 10)
        pygame.draw.line(s, LINE, (MAP_X0, Y_RAIL), (MAP_X1, Y_RAIL), 3)
        for x in range(MAP_X0, MAP_X1, 12):
            pygame.draw.line(s, LINE, (x, Y_RAIL - 5), (x, Y_RAIL + 5), 1)
        pts = [(x, Y_RIVER + 6 * math.sin(x / 30)) for x in range(MAP_X0, MAP_X1, 6)]
        pygame.draw.lines(s, (40, 110, 190), False, pts, 14)
        text(s, f"ROAD {ROAD_KM:.0f} km", (MAP_X0, Y_ROAD - 28), 14, MUTED)
        text(s, f"RAIL {RAIL_KM:.0f} km, 1.2% ruling grade", (MAP_X0, Y_RAIL - 28), 14, MUTED)
        text(s, f"RIVER {RIVER_KM:.0f} km, current 1 m/s toward the port", (MAP_X0, Y_RIVER - 30), 14, MUTED)
        # moving vehicles
        if self.state in ("run", "frozen"):
            for m in r.modes:
                y = {"Road": Y_ROAD, "Rail": Y_RAIL, "Barge": Y_RIVER}[m.name]
                fleet = {"Road": p.trucks, "Rail": p.rakes, "Barge": p.barges}[m.name]
                shown = min(fleet, 30)
                for k in range(shown):
                    if m.round_h <= 0:
                        continue
                    phase = ((self.t + k * m.round_h / max(shown, 1)) % m.round_h) / m.round_h
                    if self.t > m.hours:
                        continue
                    f = phase * 2 if phase < 0.5 else 2 - phase * 2
                    x = MAP_X0 + f * (MAP_X1 - MAP_X0)
                    col = {"Road": (240, 160, 60), "Rail": (230, 120, 50), "Barge": (220, 220, 230)}[m.name]
                    size = {"Road": (8, 6), "Rail": (26, 8), "Barge": (22, 10)}[m.name]
                    pygame.draw.rect(s, col, (x - size[0] / 2, y - size[1] / 2, *size))
            text(s, f"hour {min(self.t, r.hours if math.isfinite(r.hours) else self.t):.1f}",
                 (MAP_X0, TOP_BAR + 8), 18, ACCENT, bold=True)
        # plan panel
        panel(s, (12, TOP_BAR + 296, 548, 178), BG_DARK, PANEL_EDGE, 8)
        text(s, f"Road share: {p.road_t:.0f} t (the rest)", (24, TOP_BAR + 450), 14, TEXT)
        self.panel_widgets.draw(s)
        status = (f"{r.hours:.1f} h  |  {economy.format_rs(r.cost)}  |  safety {r.safety:.1f}"
                  if math.isfinite(r.hours) else "a mode has freight but no vehicles")
        col = GOOD if r.feasible and r.hours <= self.cfg["deadline"] else BAD
        text(s, status, (300, TOP_BAR + 450), 14, col, bold=True)
        self.draw_pareto(s)

    def draw_pareto(self, s):
        rect = panel(s, (12, TOP_BAR + 478, 860, HEIGHT - BOTTOM_BAR - TOP_BAR - 488), BG_DARK, PANEL_EDGE, 8)
        text(s, "Cost (left = cheap) vs time (down = fast). Gold = Pareto frontier, white ring = your plan, "
                "red line = deadline", (rect.x + 8, rect.y + 4), 13, MUTED)
        inner = rect.inflate(-40, -34).move(10, 8)
        pts = [(pl, rs) for pl, rs in (self.frontier or [])]
        if self.result.feasible:
            pts_all = pts + [(self.plan, self.result)]
        else:
            pts_all = pts
        if not pts_all:
            text(s, "Press 'Optimizer' to plot every feasible plan.", inner.center, 15, MUTED, anchor="center")
            return
        c0 = min(x[1].cost for x in pts_all)
        c1 = max(x[1].cost for x in pts_all)
        h0 = 0
        h1 = max(min(x[1].hours, 80) for x in pts_all)
        c1 = c1 if c1 > c0 else c0 + 1
        def to(res):
            return (inner.x + (res.cost - c0) / (c1 - c0) * inner.w,
                    inner.y + min(res.hours, 80) / max(h1, 1) * inner.h)
        dl = inner.y + self.cfg["deadline"] / max(h1, 1) * inner.h
        pygame.draw.line(s, BAD, (inner.x, dl), (inner.right, dl), 1)
        if pts:
            front = set(economy.pareto_front([{"safety": rs.safety, "cost": rs.cost, "time": rs.hours}
                                              for _, rs in pts]))
            for k, (_, rs) in enumerate(pts):
                x, y = to(rs)
                pygame.draw.circle(s, ACCENT if k in front else (70, 90, 120), (int(x), int(y)), 3 if k in front else 2)
        if self.result.feasible:
            x, y = to(self.result)
            pygame.draw.circle(s, TEXT, (int(x), int(y)), 8, 2)
