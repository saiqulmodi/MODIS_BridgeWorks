"""Level 5 - The Harbor Switchyard: block signals, braking distances and interlocking logic."""
import pygame

from engine import economy
from engine.failure import FailureReport
from engine.railnet import (BRIDGE, CARGO, CROSSING, HARBOR_END, INPUTS, OUTPUTS, PASSENGER,
                            SIGNAL_SLOTS, X_END, RailNet, default_logic)
from engine.signals import DOUBLE_YELLOW, GREEN, RED, YELLOW, LogicRow, min_block_length, safe_braking_distance

from .. import sound
from ..common import Card, LevelScene
from ..help_texts import HELP
from ..ui import (ACCENT, BAD, BG_DARK, BOTTOM_BAR, CYAN, GOOD, HEIGHT, LINE, MUTED, PANEL,
                  PANEL_EDGE, TEXT, TOP_BAR, WARN, WIDTH, Button, Cycler, WidgetGroup,
                  blueprint_background, panel, text)

ASPECT_COL = {RED: (235, 60, 50), YELLOW: (245, 200, 50), DOUBLE_YELLOW: (255, 150, 40), GREEN: (70, 210, 110)}
X0, X1 = 24, 866
Y_EB, Y_WB, Y_BR, Y_HB = TOP_BAR + 120, TOP_BAR + 170, TOP_BAR + 145, TOP_BAR + 80
INPUT_CHOICES = [None] + INPUTS


def sx(x):
    return int(X0 + x / X_END * (X1 - X0))


class SignalScene(LevelScene):
    CONTROLS = ("Click the small dots beside the eastbound (top) and westbound (bottom) approach "
                "tracks to add or remove signals. Edit the interlocking rows below: click an input "
                "to cycle it, NOT to invert it, AND/OR to switch. RUN plays 12 minutes of traffic.")

    DEMO_STATE = ("eb_slots", "wb_slots", "four", "logic")

    def __init__(self, app, level):
        super().__init__(app, level)
        self.cfg = level.cfg
        self.eb_slots = set()
        self.wb_slots = set()
        self.four = False
        self.logic = default_logic()
        self.net = None
        self.mode = "edit"
        self.speed = 8
        self.tick = 0
        self.logic_widgets = WidgetGroup()
        self._build_toolbar()
        self._build_logic()
        self.show_info()

    def _build_toolbar(self):
        y = HEIGHT - BOTTOM_BAR + 9
        self.aspect_btn = self.widgets.add(Button((10, y, 180, 40), "3-aspect signals", self.toggle_aspect,
                                                  size=15, help=HELP["aspect"]))
        self.widgets.add(Button((196, y, 170, 40), "Starter logic", self.reset_logic, size=15,
                                help=HELP["starter_logic"]))
        self.speed_btn = self.widgets.add(Button((372, y, 70, 40), "x8", self.cycle_speed, size=15,
                                                 help=HELP["speed"]))
        self.run_btn = self.widgets.add(Button((448, y, WIDTH - 458, 40), "RUN 12 MINUTES",
                                               self.toggle_run, hotkey=pygame.K_SPACE, colour=(40, 110, 70),
                                               help=HELP["run_signals"]))

    def _build_logic(self):
        self.logic_widgets.clear()
        y0 = TOP_BAR + 262
        for r, row in enumerate(self.logic):
            y = y0 + r * 46
            x = 160
            for k in range(3):
                self.logic_widgets.add(Button((x, y, 46, 34), "NOT", lambda r=r, k=k: self._neg(r, k),
                                              toggle=True, active=row.negate[k], size=12))
                x += 48
                c = Cycler((x, y, 150, 34), "", [n or "-" for n in INPUT_CHOICES],
                           INPUT_CHOICES.index(row.inputs[k]), lambda v, r=r, k=k: self._inp(r, k, v), size=13)
                self.logic_widgets.add(c)
                x += 154
                if k < 2:
                    self.logic_widgets.add(Cycler((x, y, 52, 34), "", ["AND", "OR"],
                                                  ["AND", "OR"].index(row.ops[k]),
                                                  lambda v, r=r, k=k: self._op(r, k, v), size=13))
                    x += 56

    # --- demonstration --------------------------------------------------------------------
    def demo_prepare(self):
        if self.mode != "edit":
            self.reset_after_failure()

    def load_demo(self):
        from engine.railnet import reference_logic
        self.logic = reference_logic()
        self.eb_slots, self.wb_slots, self.four = {400.0}, {400.0}, False
        self.after_demo()

    def run_demo(self):
        self.toggle_run()

    def after_demo(self):
        self._build_logic()
        self.aspect_btn.label = "4-aspect signals" if self.four else "3-aspect signals"
        self.show_info()

    def _neg(self, r, k):
        if self.mode == "edit":
            self.logic[r].negate[k] = not self.logic[r].negate[k]
        self.show_info()

    def _inp(self, r, k, v):
        self.logic[r].inputs[k] = None if v == "-" else v
        self.show_info()

    def _op(self, r, k, v):
        self.logic[r].ops[k] = v
        self.show_info()

    def reset_logic(self):
        if self.mode == "edit":
            self.logic = default_logic()
            self._build_logic()
            self.show_info()

    def toggle_aspect(self):
        if self.mode == "edit":
            self.four = not self.four
            self.aspect_btn.label = "4-aspect signals" if self.four else "3-aspect signals"
            self.show_info()

    def cycle_speed(self):
        self.speed = {2: 4, 4: 8, 8: 16, 16: 2}[self.speed]
        self.speed_btn.label = f"x{self.speed}"

    def cost(self):
        per = self.cfg["signal_cost_4"] if self.four else self.cfg["signal_cost"]
        terms = sum(r.term_count() for r in self.logic)
        return per * (len(self.eb_slots) + len(self.wb_slots) + 2) + terms * self.cfg["term_cost"]

    def make_net(self):
        return RailNet(sorted(self.eb_slots), sorted(self.wb_slots), self.four,
                       [LogicRow(r.output, list(r.inputs), list(r.negate), list(r.ops)) for r in self.logic])

    # --- calculator -------------------------------------------------------------------------
    def show_info(self):
        net = self.net or self.make_net()
        cards = []
        for tt in (PASSENGER, CARGO):
            d = safe_braking_distance(tt.max_speed, tt.brake_mu)
            cards.append(Card(f"{tt.kind.title()} braking distance", "d_stop = v^2 / (2 mu g)",
                              f"= {tt.max_speed:.0f}^2 / (2 x {tt.brake_mu} x 9.81)", f"d_stop = {d:.0f} m"))
        need = max(min_block_length(PASSENGER.max_speed, PASSENGER.brake_mu, self.four),
                   min_block_length(CARGO.max_speed, CARGO.brake_mu, self.four))
        warn = net.block_warnings()
        cards.append(Card("Minimum warning distance", "caution signal >= d_stop before the red" +
                          (" (halved: 4-aspect)" if self.four else ""), "",
                          f"{need:.0f} m;  short blocks: " + (", ".join(f"{n} {l:.0f} m" for n, l, _ in warn) or "none"),
                          BAD if warn else GOOD))
        cards.append(Card("Interlocking (evaluated top to bottom)", "\n".join(r.text() for r in self.logic)))
        if self.net:
            n = self.net
            cards.append(Card("Live", "delivered / SPADs / waiting",
                              f"t = {n.time:.0f} s of {n.cfg.duration:.0f}",
                              f"{n.delivered} trains, {n.spads} SPAD, {n.idle_time + n.queue_time:.0f} s waiting, "
                              f"{n.misroutes} misroutes"))
            cards.append(Card("Inputs now", " ".join(f"{k}={'1' if v else '0'}" for k, v in n.inputs.items() if k != "TRUE")))
        self.drawer.show("Signals & interlocking", cards)

    # --- input -----------------------------------------------------------------------------
    def handle_world(self, event):
        if self.mode == "edit" and self.logic_widgets.handle(event):
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mode == "edit":
            for s in SIGNAL_SLOTS:
                if abs(event.pos[0] - sx(s)) < 8 and abs(event.pos[1] - (Y_EB - 18)) < 12:
                    self.eb_slots ^= {s}
                    sound.play("click")
                    self.show_info()
                    return
                if abs(event.pos[0] - sx(X_END - s)) < 8 and abs(event.pos[1] - (Y_WB + 18)) < 12:
                    self.wb_slots ^= {s}
                    sound.play("click")
                    self.show_info()
                    return

    def toggle_run(self):
        if self.overlay is not None:
            return
        if self.mode == "edit":
            self.net = self.make_net()
            self.mode = "run"
            self.run_btn.label = "STOP"
        else:
            self.reset_after_failure()

    def reset_after_failure(self):
        self.mode = "edit"
        self.net = None
        self.run_btn.label = "RUN 12 MINUTES"
        self.show_info()

    def update_world(self, dt):
        self.tick += 1
        if self.mode != "run":
            return
        sim_dt = 0.1          # x1 = 3 simulated seconds per real second
        steps = max(1, round(self.speed * 3 * dt / sim_dt))
        spads = self.net.spads
        for _ in range(steps):
            self.net.step(sim_dt)
            if self.net.finished:
                break
        if self.net.spads > spads:
            sound.play("alarm")
        if self.tick % 15 == 0:
            self.show_info()
        n = self.net
        if n.failure:
            self.mode = "frozen"
            self.run_btn.label = "EDIT"
            f = n.failure
            kind = {"collision": "collision", "derail": "derail", "crossing": "crossing"}[f.kind]
            self.fail(FailureReport(kind, f.message, f.formula,
                                    [e[1] for e in n.events[-2:]], f.time, f.trains, build_cost=self.cost()))
        elif n.time >= n.cfg.duration:
            self.mode = "frozen"
            self.run_btn.label = "EDIT"
            self._finish()

    def _finish(self):
        n = self.net
        if n.misroutes:
            self.fail(FailureReport("misroute", f"{n.misroutes} TRAIN(S) MISROUTED",
                                    "SWITCH_HARBOR must be TRUE for cargo trains and FALSE for passengers",
                                    [e[1] for e in n.events if "Misroute" in e[1]][:2], n.time,
                                    build_cost=self.cost()))
            return
        if n.delivered < self.cfg["target"]:
            self.fail(FailureReport("timeout", f"ONLY {n.delivered} TRAINS GOT THROUGH",
                                    f"Target {self.cfg['target']}: waiting {n.idle_time + n.queue_time:.0f} "
                                    f"train-seconds. Shorter (but still safe) blocks raise capacity.",
                                    time=n.time, build_cost=self.cost()))
            return
        wait = n.idle_time + n.queue_time
        extra = n.spads == 0 and wait <= 1000
        lines = [("Trains delivered", f"{n.delivered} (cargo to harbor: {n.delivered_cargo_harbor})", None),
                 ("SPADs (signals passed at danger)", f"{n.spads}", GOOD if n.spads == 0 else BAD),
                 ("Waiting (idle + queued)", f"{wait:.0f} train-seconds", GOOD if wait <= 1000 else WARN),
                 ("Barrier down time", f"{n.barrier_down_time:.0f} s", None)]
        self.succeed(self.cost(), 100 - 10 * n.spads, n.time, extra_goal=extra, lines=lines)

    # --- drawing ---------------------------------------------------------------------------
    def draw_world(self, s):
        blueprint_background(s, (0, TOP_BAR, WIDTH, HEIGHT - TOP_BAR - BOTTOM_BAR))
        b0, b1 = sx(BRIDGE[0]), sx(BRIDGE[1])
        # water under the bridge
        pygame.draw.rect(s, (30, 80, 140), (b0 + 6, TOP_BAR + 60, b1 - b0 - 12, 150))
        text(s, "PORT KAVI BAY", ((b0 + b1) // 2, TOP_BAR + 196), 13, (150, 190, 230), anchor="center")
        tracks = [((X0, Y_EB), (b0 - 20, Y_EB)), ((b0 - 20, Y_EB), (b0, Y_BR)),
                  ((X0, Y_WB), (b0 - 20, Y_WB)), ((b0 - 20, Y_WB), (b0, Y_BR)),
                  ((b0, Y_BR), (b1, Y_BR)),
                  ((b1, Y_BR), (b1 + 20, Y_EB)), ((b1 + 20, Y_EB), (X1, Y_EB)),
                  ((b1, Y_BR), (b1 + 20, Y_WB)), ((b1 + 20, Y_WB), (X1, Y_WB)),
                  ((b1 + 20, Y_EB), (b1 + 50, Y_HB)), ((b1 + 50, Y_HB), (sx(HARBOR_END), Y_HB))]
        for a, b in tracks:
            pygame.draw.line(s, (30, 30, 36), a, b, 7)
            pygame.draw.line(s, LINE, a, b, 2)
        text(s, "HARBOR", (sx(HARBOR_END) + 6, Y_HB - 9), 14, ACCENT, bold=True)
        text(s, "EASTBOUND ->", (X0, Y_EB - 44), 13, MUTED)
        text(s, "<- WESTBOUND", (X0, Y_WB + 30), 13, MUTED)
        text(s, "single-track bridge", ((b0 + b1) // 2, Y_BR - 22), 13, MUTED, anchor="center")
        # level crossing
        cx0, cx1 = sx(CROSSING[0]), sx(CROSSING[1])
        pygame.draw.rect(s, (70, 70, 80), (cx0, TOP_BAR + 60, cx1 - cx0, 150))
        barrier = self.net.barrier if self.net else 0.0
        for y in (Y_EB - 30, Y_WB + 30):
            length = 40 * (1 - barrier) + 4
            pygame.draw.line(s, (240, 60, 60), (cx0 - 4, y), (cx0 - 4, y - length if y < Y_BR else y + length), 4)
        text(s, "road", ((cx0 + cx1) // 2, TOP_BAR + 64), 12, MUTED, anchor="center")
        # switch S1
        sw = self.net.switch_pos if self.net else 0.0
        text(s, f"S1: {'HARBOR' if sw >= 1 else ('moving' if sw > 0 else 'MAIN')}", (b1 + 24, Y_HB + 14), 13, ACCENT)
        # signal slots and signals
        net = self.net
        for slot in SIGNAL_SLOTS:
            for d, x, y in (("EB", sx(slot), Y_EB - 18), ("WB", sx(X_END - slot), Y_WB + 18)):
                placed = slot in (self.eb_slots if d == "EB" else self.wb_slots)
                if not placed and self.mode == "edit":
                    pygame.draw.circle(s, (80, 110, 160), (x, y), 3)
        sigs = net.signals if net else self.make_net().signals
        for d, lst in sigs.items():
            for g in lst:
                if g.name.endswith("FRINGE"):
                    continue
                x = sx(g.s if d == "EB" else X_END - g.s)
                y = Y_EB - 18 if d == "EB" else Y_WB + 18
                col = ASPECT_COL[g.aspect] if net else (200, 200, 210)
                pygame.draw.line(s, MUTED, (x, y), (x, Y_EB if d == "EB" else Y_WB), 1)
                pygame.draw.circle(s, (15, 15, 20), (x, y), 8)
                pygame.draw.circle(s, col, (x, y), 6)
                if g.aspect == DOUBLE_YELLOW and net:
                    pygame.draw.circle(s, col, (x, y - 14 if d == "EB" else y + 14), 5)
        # block warnings
        if not net:
            for name, length, need in self.make_net().block_warnings():
                text(s, f"{name}: warning {length:.0f} m < {need:.0f} m", (X0, TOP_BAR + 8 + 18 * 0), 13, WARN)
                break
        # trains
        if net:
            for t in net.trains:
                for track, a, b in t.pieces():
                    y = {"EB_W": Y_EB, "EB_E": Y_EB, "WB_W": Y_WB, "WB_E": Y_WB, "BRIDGE": Y_BR,
                         "HARBOR": Y_HB}[track]
                    col = (230, 120, 50) if t.ttype.kind == "cargo" else (90, 200, 240)
                    pygame.draw.line(s, col, (sx(a), y), (sx(b), y), 10)
                fx = sx(t.front_x)
                yy = Y_EB if t.direction == "EB" else Y_WB
                text(s, f"{t.tid}", (fx, yy - 26 if t.direction == "EB" else yy + 12), 12, TEXT, anchor="center")
                if t.emergency:
                    pygame.draw.circle(s, BAD, (fx, yy), 12, 2)
            text(s, f"t = {net.time:5.0f} s   delivered {net.delivered}   SPAD {net.spads}   "
                    f"waiting {net.idle_time + net.queue_time:.0f} s", (X0, TOP_BAR + 8), 15, TEXT, bold=True)
        else:
            text(s, f"Passenger: {PASSENGER.max_speed*3.6:.0f} km/h, {PASSENGER.length:.0f} m   "
                    f"Cargo: {CARGO.max_speed*3.6:.0f} km/h, {CARGO.length:.0f} m", (X0, TOP_BAR + 30), 14, MUTED)
        # logic editor
        r = panel(s, (12, TOP_BAR + 230, 866, 46 * 4 + 44), BG_DARK, PANEL_EDGE, 8)
        text(s, "INTERLOCKING LOGIC  -  each output = [NOT] A  AND/OR  [NOT] B  AND/OR  [NOT] C",
             (r.x + 10, r.y + 8), 14, ACCENT, bold=True)
        for k, row in enumerate(self.logic):
            y = TOP_BAR + 262 + k * 46
            on = net.outputs.get(row.output) if net else None
            col = GOOD if on else (MUTED if on is None else BAD)
            text(s, row.output, (r.x + 10, y + 8), 15, col, bold=True)
        self.logic_widgets.draw(s)
