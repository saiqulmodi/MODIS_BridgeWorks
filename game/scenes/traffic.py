"""Level 6 - Urban Bottleneck: a crossroads at rush hour. Choose signals, a roundabout or an
overpass, tune it, and watch the fundamental diagram q = k v come alive."""
import math

import pygame

from engine import economy
from engine.failure import FailureReport
from engine.traffic import (TrafficSim, critical_density, greenshields_flow, max_flow,
                            shockwave_speed)

from .. import sound
from ..common import Card, LevelScene
from ..help_texts import HELP, JUNCTION
from ..ui import (ACCENT, BAD, BG_DARK, BOTTOM_BAR, CYAN, GOOD, HEIGHT, LINE, MUTED, PANEL_EDGE,
                  TEXT, TOP_BAR, WARN, WIDTH, Button, Cycler, Slider, blueprint_background,
                  mini_chart, panel, text)

X0 = 30
Y_MAIN = TOP_BAR + 262
K_JAM = 1000 / 7.0          # veh/km: 5 m car + 2 m gap
MODES = ["signals", "roundabout", "overpass"]


def speed_colour(v, vmax):
    r = max(0.0, min(1.0, v / vmax))
    if r > 0.6:
        return (70, 200, 110)
    if r > 0.3:
        return (240, 200, 60)
    return (235, 70, 60)


class TrafficScene(LevelScene):
    CONTROLS = ("Choose the junction type at the bottom left. Signal timing and the speed limit "
                "are sliders in the calculator. RUN plays 12 minutes of rush hour; the road is "
                "coloured by speed so you can watch jams travel backwards.")

    DEMO_STATE = ("mode_name", "cycle", "split", "speed_kmh")

    def __init__(self, app, level):
        super().__init__(app, level)
        self.cfg = level.cfg
        self.mode_name = "signals"
        self.cycle = 60.0
        self.split = 0.5
        self.speed_kmh = 50.0
        self.sim = None
        self.state = "edit"
        self.speed = 8
        self.tick = 0
        self._acc = 0.0
        y = HEIGHT - BOTTOM_BAR + 9
        self.mode_cycler = self.widgets.add(Cycler((10, y, 300, 40), "Junction: ",
                                                   [self._label(m) for m in MODES],
                                                   on_change=self._mode, size=15,
                                                   help=lambda: JUNCTION[MODES[self.mode_cycler.index]]))
        self.speed_btn = self.widgets.add(Button((316, y, 60, 40), "x8", self.cycle_speed, size=15,
                                                 help=HELP["speed"]))
        self.run_btn = self.widgets.add(Button((382, y, WIDTH - 392, 40), "RUN RUSH HOUR",
                                               self.toggle_run, hotkey=pygame.K_SPACE, colour=(40, 110, 70),
                                               help=HELP["run_traffic"]))
        self.show_panel()

    # --- demonstration --------------------------------------------------------------------
    def demo_prepare(self):
        if self.state != "edit":
            self.reset_after_failure()

    def load_demo(self):
        self.mode_name = "roundabout"
        self.after_demo()

    def run_demo(self):
        self.toggle_run()

    def after_demo(self):
        self.mode_cycler.index = MODES.index(self.mode_name)
        self.mode_cycler.label = self.mode_cycler._label()
        self.show_panel()

    def _label(self, m):
        return f"{m.title()} ({economy.format_rs(self.cfg['cost'][m])})"

    def _mode(self, label):
        if self.state != "edit":
            return
        self.mode_name = MODES[[self._label(m) for m in MODES].index(label)]
        self.show_panel()

    def cycle_speed(self):
        self.speed = {2: 4, 4: 8, 8: 16, 16: 2}[self.speed]
        self.speed_btn.label = f"x{self.speed}"

    def cost(self):
        return self.cfg["cost"][self.mode_name]

    def make_sim(self):
        return TrafficSim(self.mode_name, self.cycle, self.split, self.speed_kmh)

    # --- calculator -----------------------------------------------------------------------
    def show_panel(self):
        sliders = []
        if self.state == "edit":
            if self.mode_name == "signals":
                sliders.append(Slider((0, 0, 10, 40), "Signal cycle C (s)", 40, 140, self.cycle,
                                      self._set("cycle"), "{:.0f}", 5))
                sliders.append(Slider((0, 0, 10, 40), "Main-road share of green", 0.3, 0.85, self.split,
                                      self._set("split"), "{:.2f}", 0.01))
            sliders.append(Slider((0, 0, 10, 40), "Speed limit (km/h)", 30, 70, self.speed_kmh,
                                  self._set("speed_kmh"), "{:.0f}", 5))
        self.drawer.show("Traffic flow", self.cards(), sliders)

    def _set(self, attr):
        def f(v):
            setattr(self, attr, v)
            self.drawer.update_cards(self.cards())
        return f

    def cards(self):
        sim = self.sim or self.make_sim()
        vmax = self.speed_kmh
        kc = critical_density(K_JAM)
        cards = [Card("Greenshields model", "v = v_max (1 - k / k_jam),  q = k v",
                      f"v_max = {vmax:.0f} km/h, k_jam = {K_JAM:.0f} veh/km",
                      f"k_crit = k_jam/2 = {kc:.0f} veh/km,  q_max = v_max k_jam / 4 = {max_flow(vmax, K_JAM):.0f} veh/h")]
        if self.mode_name == "signals":
            cm = sim.capacity("MAIN")
            cc = sim.capacity("CROSS")
            dm, dc = sim.roads["MAIN"].peak_demand, sim.roads["CROSS"].peak_demand
            cards.append(Card("Signal capacity", "c = s g / C   (s = 1800 veh/h of green)",
                              f"main {cm:.0f} vs demand {dm:.0f};  cross {cc:.0f} vs demand {dc:.0f} veh/h",
                              "OK" if cm >= dm and cc >= dc else "Demand exceeds capacity: queues will grow",
                              GOOD if cm >= dm and cc >= dc else BAD))
        elif self.mode_name == "roundabout":
            cards.append(Card("Roundabout", "cars merge in turn, gap >= 2 s",
                              "Slower (8 m/s in the circle) but nobody waits for a red light."))
        else:
            cards.append(Card("Overpass", "no conflict point", "Each road flows at its own capacity."))
        q1 = sim.roads["MAIN"].peak_demand
        k1 = q1 / vmax
        cards.append(Card("Shockwave when a queue forms", "w = (q2 - q1) / (k2 - k1)",
                          f"free: q1 = {q1:.0f} veh/h, k1 = {k1:.0f} veh/km;  jam: q2 = 0, k2 = {K_JAM:.0f}",
                          f"w = {shockwave_speed(q1, k1, 0, K_JAM):.1f} km/h (negative = travels backwards)"))
        if self.sim:
            st = self.sim.stats()
            k, q = self.sim.detector[-1] if self.sim.detector else (0, 0)
            cards.append(Card("Detector (200 m before the junction)", "q = k v",
                              f"k = {k:.0f} veh/km, q = {q:.0f} veh/h",
                              "congested (k > k_crit)" if k > kc else "free flow", BAD if k > kc else GOOD))
            cards.append(Card("Results so far", "throughput, travel time, idling",
                              f"{st['throughput_per_min']:.1f} veh/min, trips {st['avg_travel_time']:.0f} s "
                              f"(main {st['main_delay_ratio']:.2f}x free-flow)",
                              f"idling {st['idle_time']:.0f} car-s, fuel {st['fuel_l']:.1f} L, queued {st['queued']}"))
        return cards

    # --- run -------------------------------------------------------------------------------
    def toggle_run(self):
        if self.overlay is not None:
            return
        if self.state == "edit":
            def go():
                self.sim = self.make_sim()
                self.state = "run"
                self.run_btn.label = "STOP"
                self.show_panel()
            self.finance_gate(go)
        else:
            self.reset_after_failure()

    def reset_after_failure(self):
        self.state = "edit"
        self.sim = None
        self.run_btn.label = "RUN RUSH HOUR"
        self.show_panel()

    def update_world(self, dt):
        self.tick += 1
        if self.state != "run":
            return
        self._acc += self.speed * 2 * dt            # x1 = 2 simulated seconds per real second
        while self._acc >= 0.25:
            self._acc -= 0.25
            self.sim.step(0.25)
            if self.sim.failure or self.sim.time >= self.sim.cfg.duration:
                self._acc = 0.0
                break
        if self.tick % 20 == 0:
            self.drawer.update_cards(self.cards())
        if self.sim.failure:
            self.state = "frozen"
            self.run_btn.label = "EDIT"
            title, formula = self.sim.failure
            self.fail(FailureReport("gridlock", title, formula,
                                    ["The red band in the heat map is the jam; it grows backwards at the "
                                     "shockwave speed w."], self.sim.time, None, self._history(),
                                    build_cost=self.cost()))
        elif self.sim.time >= self.sim.cfg.duration:
            self.state = "frozen"
            self.run_btn.label = "EDIT"
            self._finish()

    def _history(self):
        h = self.sim.history
        return {"veh/min": [(t, q) for t, q, _ in h], "trip s": [(t, tt) for t, _, tt in h]}

    def _finish(self):
        st = self.sim.stats()
        if st["main_delay_ratio"] > self.cfg["max_delay"]:
            self.fail(FailureReport("gridlock", "CITY TOO SLOW: main-road trips took too long",
                                    f"Trips took {st['main_delay_ratio']:.2f}x the free-flow time "
                                    f"(limit {self.cfg['max_delay']}x)", [], self.sim.time, None,
                                    self._history(), build_cost=self.cost()))
            return
        extra = st["idle_time"] <= self.cfg["idle_bonus"]
        lines = [("Cars through", f"{st['exited']}  ({st['throughput_per_min']:.1f} per min)", None),
                 ("Main-road trip vs free flow", f"{st['main_delay_ratio']:.2f}x", None),
                 ("Idling (pollution)", f"{st['idle_time']:.0f} car-seconds", GOOD if extra else WARN),
                 ("Fuel burned", f"{st['fuel_l']:.1f} L", None)]
        self.succeed(self.cost(), 100 - 20 * (st["main_delay_ratio"] - 1), self.sim.time,
                     extra_goal=extra, lines=lines)

    # --- drawing ---------------------------------------------------------------------------
    def draw_world(self, s):
        blueprint_background(s, (0, TOP_BAR, WIDTH, HEIGHT - TOP_BAR - BOTTOM_BAR))
        sim = self.sim or self.make_sim()
        main, cross = sim.roads["MAIN"], sim.roads["CROSS"]
        jx = X0 + main.conflict[0] + 10
        y_top = Y_MAIN - cross.conflict[0] - 10
        vmax = sim.params.v0
        # roads, coloured by speed in each 20 m cell (heat map)
        hm = sim.heatmap("MAIN")
        for i, v in enumerate(hm):
            col = (60, 64, 74) if v is None else speed_colour(v, vmax)
            pygame.draw.rect(s, col, (X0 + i * sim.cfg.cell, Y_MAIN - 8, sim.cfg.cell, 16))
        hc = sim.heatmap("CROSS")
        for i, v in enumerate(hc):
            col = (60, 64, 74) if v is None else speed_colour(v, vmax)
            pygame.draw.rect(s, col, (jx - 8, y_top + i * sim.cfg.cell, 16, sim.cfg.cell))
        text(s, "MAIN ROAD  ->", (X0, Y_MAIN - 30), 14, MUTED)
        text(s, "MARKET STREET", (jx + 14, y_top), 14, MUTED)
        # junction furniture
        if self.mode_name == "roundabout":
            pygame.draw.circle(s, (60, 64, 74), (jx, Y_MAIN), 26, 10)
            pygame.draw.circle(s, (70, 130, 80), (jx, Y_MAIN), 14)
        elif self.mode_name == "overpass":
            pygame.draw.rect(s, (20, 20, 26), (jx - 14, Y_MAIN - 30, 28, 60))
            pygame.draw.rect(s, (110, 110, 120), (jx - 10, Y_MAIN - 34, 20, 68), 2)
            text(s, "overpass", (jx + 16, Y_MAIN + 14), 13, MUTED)
        else:
            for road, pos in (("MAIN", (jx - 24, Y_MAIN - 22)), ("CROSS", (jx + 14, Y_MAIN - 36))):
                st = sim.signal_state(road)
                col = {"G": GOOD, "A": WARN, "R": BAD}[st]
                pygame.draw.rect(s, (15, 15, 20), (pos[0] - 6, pos[1] - 6, 12, 12))
                pygame.draw.circle(s, col, pos, 5)
        # cars
        for c in sim.cars["MAIN"]:
            pygame.draw.rect(s, (230, 235, 245), (X0 + c.x - 5, Y_MAIN - 3, 5, 6))
        for c in sim.cars["CROSS"]:
            pygame.draw.rect(s, (230, 235, 245), (jx - 3, y_top + c.x - 5, 6, 5))
        # queues off the map
        for road, pos in (("MAIN", (X0 - 4, Y_MAIN + 12)), ("CROSS", (jx + 12, y_top - 4))):
            n = len(sim.queue[road])
            if n:
                text(s, f"+{n} waiting", pos, 13, BAD if n > 5 else WARN)
        # charts
        self.draw_fundamental(s, sim)
        if self.sim:
            h = self.sim.history
            mini_chart(s, (440, TOP_BAR + 300, 430, 120), [[(t, q) for t, q, _ in h]], [GOOD],
                       "throughput (veh per min)")
            text(s, f"t = {self.sim.time:.0f} / {self.sim.cfg.duration:.0f} s", (440, TOP_BAR + 280), 15, TEXT, bold=True)
        else:
            text(s, f"Rush-hour demand: main {main.peak_demand:.0f} veh/h, market street "
                    f"{cross.peak_demand:.0f} veh/h", (440, TOP_BAR + 280), 14, MUTED)

    def draw_fundamental(self, s, sim):
        r = panel(s, (440, TOP_BAR + 430, 430, 168), BG_DARK, PANEL_EDGE, 6)
        text(s, "Fundamental diagram  q = k v  (curve = Greenshields, dots = detector)", (r.x + 8, r.y + 4), 13, MUTED)
        vmax = self.speed_kmh
        qmax = max_flow(vmax, K_JAM)
        inner = pygame.Rect(r.x + 30, r.y + 24, r.w - 44, r.h - 44)
        pts = []
        for i in range(41):
            k = K_JAM * i / 40
            q = greenshields_flow(k, vmax, K_JAM)
            pts.append((inner.x + k / K_JAM * inner.w, inner.bottom - q / (qmax * 1.15) * inner.h))
        pygame.draw.lines(s, CYAN, False, pts, 2)
        kc = critical_density(K_JAM)
        xk = inner.x + kc / K_JAM * inner.w
        pygame.draw.line(s, WARN, (xk, inner.y), (xk, inner.bottom), 1)
        text(s, "k_crit", (xk + 3, inner.y), 12, WARN)
        for k, q in (sim.detector[-40:] if self.sim else []):
            x = inner.x + min(k, K_JAM) / K_JAM * inner.w
            y = inner.bottom - min(q, qmax * 1.15) / (qmax * 1.15) * inner.h
            pygame.draw.circle(s, ACCENT if k <= kc else BAD, (int(x), int(y)), 3)
        text(s, "k (veh/km) ->", (inner.right - 80, inner.bottom + 4), 12, MUTED)
        text(s, "q", (r.x + 10, inner.y), 12, MUTED)
