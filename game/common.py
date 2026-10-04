"""Pieces every level shares: the scientific-calculator drawer, the Black Box investigation,
the results screen, the mission briefing, and the LevelScene base class."""
import math

import pygame

from engine import economy
from engine.failure import EXP_ALTERNATE, EXP_AUTOPSY, FailureReport

from . import sound
from .fx import Confetti
from .ui import (HINT, ACCENT, BAD, BG_DARK, BOTTOM_BAR, CYAN, DRAWER_W, GOOD, HEIGHT, LINE, MUTED,
                 PANEL, PANEL_EDGE, TEXT, TOP_BAR, WARN, WIDTH, Button, Slider, WidgetGroup,
                 line_height, measure, mini_chart, panel, text, text_block, wrap)


# --------------------------------------------------------------------------------------------
# Scientific calculator drawer (Prompt 10)
# --------------------------------------------------------------------------------------------
class Card:
    def __init__(self, title, formula, worked="", result="", colour=TEXT):
        self.title = title
        self.formula = formula
        self.worked = worked
        self.result = result
        self.colour = colour


class CalculatorDrawer:
    def __init__(self):
        self.open = True
        self.subject = "Calculator"
        self.hint = "Click a beam, joint, vehicle or track to see its maths."
        self.cards = []
        self.sliders = WidgetGroup()
        self.tape = []
        self.tab = pygame.Rect(WIDTH - 26, TOP_BAR + 70, 26, 110)

    @property
    def rect(self):
        return pygame.Rect(WIDTH - DRAWER_W, TOP_BAR, DRAWER_W, HEIGHT - TOP_BAR - BOTTOM_BAR)

    def covers(self, pos):
        return (self.open and self.rect.collidepoint(pos)) or self.tab_rect().collidepoint(pos)

    def tab_rect(self):
        if self.open:
            return pygame.Rect(WIDTH - DRAWER_W - 26, TOP_BAR + 70, 26, 110)
        return pygame.Rect(WIDTH - 26, TOP_BAR + 70, 26, 110)

    def show(self, subject, cards, sliders=None, tape=None, hint=""):
        """sliders: Slider and/or Button widgets stacked at the top of the drawer."""
        self.subject = subject
        self.cards = cards
        self.hint = hint
        self.sliders = WidgetGroup()
        y = self._sliders_top()
        for s in sliders or []:
            h = 40 if isinstance(s, Slider) else 32
            s.rect = pygame.Rect(self.rect.x + 16, y, DRAWER_W - 40, h)
            self.sliders.add(s)
            y += h + 6
        self._widgets_bottom = y
        if tape:
            self.tape.append(tape)
            self.tape = self.tape[-8:]

    def update_cards(self, cards):
        self.cards = cards

    def _sliders_top(self):
        return self.rect.y + 44

    @staticmethod
    def _card_height(c):
        w = DRAWER_W - 30
        h = 24 + len(wrap(c.formula, w, 16, mono=True)) * (line_height(c.formula, 16, mono=True) + 2)
        if c.worked:
            h += len(wrap(c.worked, w, 14, mono=True)) * (line_height(c.worked, 14, mono=True) + 2)
        if c.result:
            h += len(wrap(c.result, w, 16, True)) * (line_height(c.result, 16, True) + 2)
        return h + 4

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.tab_rect().collidepoint(event.pos):
            self.open = not self.open
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            self.open = not self.open
            return True
        if self.open and self.sliders.handle(event):
            return True
        if self.open and event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP) \
                and self.rect.collidepoint(event.pos):
            return True
        return False

    def draw(self, surface):
        tab = self.tab_rect()
        pygame.draw.rect(surface, ACCENT, tab, border_radius=6)
        for k, ch in enumerate("CALC"):
            text(surface, ch, (tab.centerx, tab.y + 14 + k * 22), 16, (20, 20, 30), bold=True,
                 anchor="center")
        if not self.open:
            return
        r = self.rect
        panel(surface, r, BG_DARK, PANEL_EDGE, 0, alpha=238)
        text(surface, "SCIENTIFIC CALCULATOR", (r.x + 14, r.y + 8), 14, ACCENT, bold=True)
        text(surface, self.subject, (r.x + 14, r.y + 24), 16, TEXT, bold=True)
        y = getattr(self, "_widgets_bottom", self._sliders_top())
        self.sliders.draw(surface)
        if not self.cards and self.hint:
            y = text_block(surface, self.hint, (r.x + 14, y + 6), DRAWER_W - 30, 15, MUTED)
        tape_top = r.bottom - 22 - 18 * min(len(self.tape), 5)
        for c in self.cards:
            if y + self._card_height(c) > tape_top - 6:
                text(surface, "(more cards below - pick a smaller selection)", (r.x + 14, y + 4), 13, MUTED)
                break
            pygame.draw.line(surface, PANEL_EDGE, (r.x + 10, y + 2), (r.right - 10, y + 2))
            text(surface, c.title, (r.x + 14, y + 6), 14, MUTED)
            y += 24
            y = text_block(surface, c.formula, (r.x + 14, y), DRAWER_W - 30, 16, CYAN, mono=True)
            if c.worked:
                y = text_block(surface, c.worked, (r.x + 14, y), DRAWER_W - 30, 14, TEXT, mono=True)
            if c.result:
                y = text_block(surface, c.result, (r.x + 14, y), DRAWER_W - 30, 16, c.colour, bold=True)
            y += 4
        if self.tape:
            pygame.draw.line(surface, PANEL_EDGE, (r.x + 10, tape_top - 4), (r.right - 10, tape_top - 4))
            text(surface, "TAPE", (r.x + 14, tape_top - 2), 12, MUTED)
            for k, line in enumerate(self.tape[-5:]):
                text(surface, line[:52], (r.x + 14, tape_top + 14 + 18 * k), 13, MUTED, mono=True)


# --------------------------------------------------------------------------------------------
# Overlays
# --------------------------------------------------------------------------------------------
class Overlay:
    blocks_world = True

    def __init__(self, scene):
        self.scene = scene
        self.widgets = WidgetGroup()

    def handle(self, event):
        return self.widgets.handle(event) or (
            self.blocks_world and event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP))

    def update(self, dt):
        pass

    def draw(self, surface):
        self.widgets.draw(surface)


class Briefing(Overlay):
    def __init__(self, scene):
        super().__init__(scene)
        lv = scene.level
        self.rect = pygame.Rect(90, 60, WIDTH - 180, HEIGHT - 110)
        self.widgets.add(Button((self.rect.right - 250, self.rect.bottom - 56, 230, 42),
                                "Start building", self.close, hotkey=pygame.K_RETURN))
        self.lv = lv

    def close(self):
        sound.play("click")
        self.scene.overlay = None

    def draw(self, surface):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        surface.blit(s, (0, 0))
        r = panel(surface, self.rect, PANEL, ACCENT, 14)
        lv = self.lv
        text(surface, f"LEVEL {lv.num}  -  {lv.tier}", (r.x + 24, r.y + 16), 16, ACCENT, bold=True)
        text(surface, lv.title, (r.x + 24, r.y + 38), 32, TEXT, bold=True)
        col_w = (r.w - 72) // 2
        y = text_block(surface, lv.mission, (r.x + 24, r.y + 86), col_w, 17, TEXT)
        y = text_block(surface, lv.context, (r.x + 24, y + 8), col_w, 15, MUTED)
        y += 10
        text(surface, f"Budget: {economy.format_rs(lv.budget)}    Par (bonus star): "
                      f"{economy.format_rs(lv.par_cost)}", (r.x + 24, y), 16, ACCENT, bold=True)
        y += 26
        if lv.materials:
            y = text_block(surface, "Materials: " + ", ".join(lv.materials), (r.x + 24, y), col_w, 15)
        y += 8
        text(surface, "TWO PATHS FORWARD", (r.x + 24, y), 14, ACCENT, bold=True)
        y += 22
        for name, desc in lv.paths:
            y = text_block(surface, f"- {name}: {desc}", (r.x + 24, y), col_w, 15)
        y += 8
        text(surface, "SUCCESS", (r.x + 24, y), 14, GOOD, bold=True)
        y = text_block(surface, lv.success, (r.x + 24, y + 20), col_w, 15)
        text(surface, "BONUS STAR", (r.x + 24, y + 4), 14, GOOD, bold=True)
        text_block(surface, lv.bonus, (r.x + 24, y + 24), col_w, 15)
        x2 = r.x + 48 + col_w
        text(surface, "MATHS YOU WILL DISCOVER", (x2, r.y + 86), 14, ACCENT, bold=True)
        y2 = r.y + 110
        for formula, how in lv.formulas:
            y2 = text_block(surface, formula, (x2, y2), col_w, 16, CYAN, mono=True)
            y2 = text_block(surface, how, (x2 + 12, y2), col_w - 12, 14, MUTED) + 8
        controls = getattr(self.scene, "CONTROLS", "")
        if controls:
            text(surface, "CONTROLS", (x2, y2 + 4), 14, ACCENT, bold=True)
            text_block(surface, controls, (x2, y2 + 24), col_w, 14, TEXT)
        super().draw(surface)


class BlackBox(Overlay):
    """Black Box Investigation Mode (Prompt 6)."""

    def __init__(self, scene, report: FailureReport):
        super().__init__(scene)
        self.report = report
        self.feedback = ""
        self.rect = pygame.Rect(16, HEIGHT - BOTTOM_BAR - 300, WIDTH - 32, 292)
        r = self.rect
        scene.app.save.add_exp(EXP_AUTOPSY)
        self.exp_earned = EXP_AUTOPSY
        opts = report.diagnosis_options()
        for k, o in enumerate(opts):
            self.widgets.add(Button((r.x + 16, r.y + 150 + k * 34, 470, 30), o,
                                    lambda o=o: self.answer(o), size=14))
        bx = r.right - 250
        self.widgets.add(Button((bx, r.bottom - 132, 234, 36),
                                f"Edit & retry (+{economy.format_rs(report.salvage)})",
                                self.retry, size=15, hotkey=pygame.K_r))
        alt = scene.level.alternate
        if alt:
            self.widgets.add(Button((bx, r.bottom - 90, 234, 36), f"Alternate: {alt['name']}",
                                    self.alternate, size=15,
                                    tooltip=alt["text"]))
        self.widgets.add(Button((bx, r.bottom - 48, 234, 36), "Level menu", scene.to_menu, size=15))

    def answer(self, option):
        if self.report.diagnosed:
            return
        gained = self.report.diagnose(option)
        if option == self.report.correct_cause:
            self.feedback = f"Correct! +{gained} EXP. " + self.report.lesson
            if gained:
                self.scene.app.save.add_exp(gained)
                self.exp_earned += gained
            sound.play("kaching")
        else:
            self.feedback = "Not quite - look at the formula and the chart again."
            sound.play("click")

    def retry(self):
        self.scene.add_salvage(self.report.salvage)
        self.scene.overlay = None
        self.scene.reset_after_failure()

    def alternate(self):
        self.scene.take_alternate(self.report)

    def draw(self, surface):
        r = panel(surface, self.rect, BG_DARK, BAD, 12, alpha=240)
        text(surface, "BLACK BOX INVESTIGATION", (r.x + 16, r.y + 10), 14, BAD, bold=True)
        text(surface, f"t = {self.report.time:.1f} s", (r.x + 230, r.y + 10), 14, MUTED)
        text(surface, self.report.title[:90], (r.x + 16, r.y + 30), 18, TEXT, bold=True)
        y = text_block(surface, self.report.formula, (r.x + 16, r.y + 56), 480, 14, CYAN, mono=True)
        for d in self.report.details[:2]:
            if d and y < r.y + 108:
                y = text_block(surface, d, (r.x + 16, y + 2), 480, 13, MUTED)
        text(surface, "Diagnose it - what went wrong?", (r.x + 16, r.y + 128), 14, ACCENT, bold=True)
        if self.feedback:
            text_block(surface, self.feedback, (r.x + 500, r.y + 30), r.w - 770, 14,
                       GOOD if self.report.diagnosed else WARN)
        hist = self.report.history
        if hist:
            names = list(hist)[:3]
            cols = [BAD, ACCENT, CYAN]
            chart = pygame.Rect(r.x + 500, r.y + 150, r.w - 770, 130)
            if self.feedback:
                chart = pygame.Rect(r.x + 500, r.y + 170, r.w - 770, 110)
            mini_chart(surface, chart, [hist[n] for n in names], cols, " / ".join(names),
                       limit=self.report.__dict__.get("limit"))
        text(surface, f"EXP earned here: {self.exp_earned}", (r.right - 250, r.y + 12), 14, GOOD)
        super().draw(surface)


class Results(Overlay):
    def __init__(self, scene, info):
        super().__init__(scene)
        self.info = info
        self.rect = pygame.Rect(150, 70, WIDTH - 300, HEIGHT - 130)
        r = self.rect
        self.confetti = Confetti()
        if info.get("celebrate"):
            self.confetti.burst(WIDTH // 2, 200)
            sound.play("kaching")
        nxt = scene.level.num + 1
        if nxt <= 10:
            self.widgets.add(Button((r.right - 200, r.bottom - 56, 180, 40), "Next level",
                                    lambda: scene.app.start_level(nxt), hotkey=pygame.K_RETURN))
        self.widgets.add(Button((r.right - 390, r.bottom - 56, 180, 40), "Improve design",
                                self.improve))
        self.widgets.add(Button((r.right - 580, r.bottom - 56, 180, 40), "Level menu", scene.to_menu))

    def improve(self):
        self.scene.overlay = None
        self.scene.reset_after_failure()

    def update(self, dt):
        self.confetti.update(dt)

    def draw(self, surface):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 140))
        surface.blit(s, (0, 0))
        r = panel(surface, self.rect, PANEL, GOOD, 14)
        i = self.info
        text(surface, i.get("headline", "MISSION COMPLETE"), (r.x + 24, r.y + 16), 30, GOOD, bold=True)
        stars = i.get("stars", 0)
        for k in range(3):
            c = ACCENT if k < stars else (60, 70, 90)
            cx, cy = r.right - 150 + k * 46, r.y + 36
            pts = [(cx + (18 if j % 2 == 0 else 8) * math.cos(math.radians(-90 + 36 * j)),
                    cy + (18 if j % 2 == 0 else 8) * math.sin(math.radians(-90 + 36 * j)))
                   for j in range(10)]
            pygame.draw.polygon(surface, c, pts)
        y = r.y + 64
        for label, value, col in i.get("lines", []):
            text(surface, label, (r.x + 24, y), 16, MUTED)
            text(surface, value, (r.x + 300, y), 16, col or TEXT, bold=True)
            y += 24
        if i.get("verdict"):
            y = text_block(surface, i["verdict"], (r.x + 24, y + 6), 520, 15, ACCENT)
        text(surface, f"+{i.get('exp', 0)} EXP   (total {self.scene.app.save.exp})",
             (r.x + 24, r.bottom - 48), 18, GOOD, bold=True)
        # Pareto chart of attempts
        att = i.get("attempts", [])
        if att:
            chart = pygame.Rect(r.x + 600, r.y + 70, r.w - 630, r.h - 150)
            panel(surface, chart, BG_DARK, PANEL_EDGE, 6)
            text(surface, "Your designs: cost vs safety (Pareto frontier in gold)", (chart.x + 8, chart.y + 4), 13, MUTED)
            pts = [a for a in att if a.get("ok")]
            if pts:
                c0 = min(a["cost"] for a in pts)
                c1 = max(a["cost"] for a in pts)
                s0 = min(a["safety"] for a in pts)
                s1 = max(a["safety"] for a in pts)
                c1 = c1 if c1 > c0 else c0 + 1
                s1 = s1 if s1 > s0 else s0 + 1
                inner = chart.inflate(-50, -50).move(10, 6)
                front = set(economy.pareto_front(pts))
                for k, a in enumerate(pts):
                    x = inner.x + (a["cost"] - c0) / (c1 - c0) * inner.w
                    y_ = inner.bottom - (a["safety"] - s0) / (s1 - s0) * inner.h
                    col = ACCENT if k in front else MUTED
                    pygame.draw.circle(surface, col, (int(x), int(y_)), 7 if k == len(pts) - 1 else 5)
                text(surface, "cost ->", (inner.right - 40, inner.bottom + 8), 12, MUTED)
                text(surface, "safety", (chart.x + 6, inner.y), 12, MUTED)
        super().draw(surface)
        self.confetti.draw(surface)


# --------------------------------------------------------------------------------------------
# Base class for the 10 levels
# --------------------------------------------------------------------------------------------
class LevelScene:
    CONTROLS = ""

    def __init__(self, app, level):
        self.app = app
        self.level = level
        self.widgets = WidgetGroup()
        self.drawer = CalculatorDrawer()
        self.overlay = Briefing(self) if app.show_briefings else None
        self.toast = ""
        self.toast_t = 0.0
        self.top_buttons = WidgetGroup()
        self.lang_btn = self.top_buttons.add(Button((WIDTH - 292, 6, 76, 32), "", app.toggle_language,
                                                    size=14, hotkey=pygame.K_F2,
                                                    tooltip="English / Bengali (F2)"))
        self.top_buttons.add(Button((WIDTH - 210, 6, 96, 32), "Briefing", self.show_briefing,
                                    size=14, hotkey=pygame.K_F1))
        self.top_buttons.add(Button((WIDTH - 108, 6, 96, 32), "Menu", self.to_menu, size=14,
                                    hotkey=pygame.K_ESCAPE))

    # --- money ------------------------------------------------------------------------
    @property
    def salvage(self):
        return self.app.save.level(self.level.num).get("salvage", 0.0)

    def add_salvage(self, amount):
        lv = self.app.save.level(self.level.num)
        lv["salvage"] = lv.get("salvage", 0.0) + amount
        self.app.save.write()

    @property
    def budget(self):
        return self.level.budget + self.salvage

    def cost(self):
        return 0.0

    # --- flow -----------------------------------------------------------------------
    def show_briefing(self):
        self.overlay = Briefing(self)

    def to_menu(self):
        self.app.to_menu()

    def say(self, msg, t=3.0):
        self.toast, self.toast_t = msg, t

    def fail(self, report: FailureReport):
        report.build_cost = report.build_cost or self.cost()
        self.app.save.record(self.level.num, 0, report.build_cost, 0, report.time, False)
        sound.play("snap")
        self.overlay = BlackBox(self, report)

    def reset_after_failure(self):
        """Back to editing with the same design."""

    def take_alternate(self, report):
        alt = self.level.alternate
        cost = alt["cost_factor"] * max(report.build_cost, self.level.par_cost * 0.5)
        self.app.save.add_exp(EXP_ALTERNATE)
        self.app.save.record(self.level.num, 1, cost, 50.0, report.time, True)
        lines = [("Route", alt["name"], ACCENT), ("Cost", economy.format_rs(cost), None),
                 ("Lesson kept", report.correct_cause, None)]
        self.overlay = Results(self, dict(headline="ALTERNATE ROUTE OPEN", stars=1, lines=lines,
                                          exp=EXP_ALTERNATE, verdict=alt["text"],
                                          attempts=self.app.save.level(self.level.num)["attempts"]))

    def succeed(self, cost, safety, time_s, fs=None, extra_goal=True, lines=None, verdict="",
                revenue=None):
        stars = economy.star_rating(True, cost, self.level.par_cost, self.budget, fs, extra_goal)
        if cost > self.budget:
            report = FailureReport("budget", "OVER BUDGET", f"Cost {economy.format_rs(cost)} > budget "
                                   f"{economy.format_rs(self.budget)}", time=time_s, build_cost=cost)
            self.fail(report)
            return
        exp = 100 + 50 * stars
        self.app.save.add_exp(exp)
        self.app.save.record(self.level.num, stars, cost, safety, time_s, True)
        all_lines = [("Build cost", f"{economy.format_rs(cost)}  of  {economy.format_rs(self.budget)}",
                      GOOD if cost <= self.level.par_cost else None)]
        if fs is not None:
            grade, why = economy.fs_grade(fs)
            all_lines.append(("Factor of safety", f"{fs:.2f}  ({grade})",
                              GOOD if grade == "OPTIMAL" else WARN))
            verdict = verdict or why
        if revenue is not None:
            prof, penalty = economy.profit(revenue, cost, fs or 2.0, self.level.budget)
            all_lines.append(("Toll revenue (5 yr)", economy.format_rs(revenue), None))
            all_lines.append(("Profit", economy.format_rs(prof), GOOD if prof > 0 else BAD))
            if penalty:
                all_lines.append(("Over-engineering penalty", economy.format_rs(penalty), BAD))
        all_lines += lines or []
        self.overlay = Results(self, dict(stars=stars, lines=all_lines, exp=exp, verdict=verdict,
                                          celebrate=cost <= self.level.par_cost,
                                          attempts=self.app.save.level(self.level.num)["attempts"]))

    # --- event plumbing ------------------------------------------------------------------
    def handle(self, event):
        if self.overlay is not None:
            if self.top_buttons.handle(event):
                return
            self.overlay.handle(event)
            return
        if self.top_buttons.handle(event):
            return
        if self.drawer.handle(event):
            return
        if self.widgets.handle(event):
            return
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION) \
                and self.drawer.covers(event.pos):
            return
        self.handle_world(event)

    def handle_world(self, event):
        pass

    def update(self, dt):
        if HINT["ttl"] > 0:
            HINT["ttl"] -= dt
        if self.toast_t > 0:
            self.toast_t -= dt
        if self.overlay is not None:
            self.overlay.update(dt)
            if getattr(self.overlay, "blocks_world", True) and not getattr(self, "run_under_overlay", False):
                return
        self.update_world(dt)

    def update_world(self, dt):
        pass

    def draw(self, surface):
        surface.set_clip(pygame.Rect(0, TOP_BAR, WIDTH, HEIGHT - TOP_BAR - BOTTOM_BAR))
        self.draw_world(surface)
        surface.set_clip(None)
        self.draw_top_bar(surface)
        self.draw_bottom_bar(surface)
        self.widgets.draw(surface)
        self.drawer.draw(surface)
        if self.toast_t > 0 and self.toast:
            w = measure(self.toast, 17)[0] + 30
            r = panel(surface, (WIDTH // 2 - w // 2 - 150, TOP_BAR + 10, w, 34), BG_DARK, ACCENT, 8)
            text(surface, self.toast, r.center, 17, ACCENT, anchor="center")
        if self.overlay is None:
            self.draw_hint(surface)
        if self.overlay is not None:
            self.overlay.draw(surface)
        self.top_buttons.draw(surface)

    def draw_hint(self, surface):
        """'IDEA' box: for the bottom-bar button under the mouse, else the one last clicked."""
        title, body = "", ""
        for w in self.widgets.items:
            if isinstance(w, Button) and w.visible and w.hover and w.help_text():
                title, body = w.label, w.help_text()
                break
        if not body and HINT["ttl"] > 0:
            title, body = HINT["title"], HINT["text"]
        if not body:
            return
        width = WIDTH - DRAWER_W - 40
        lines = wrap(body, width - 30, 15)
        h = 36 + 21 * len(lines)
        r = panel(surface, (16, HEIGHT - BOTTOM_BAR - h - 8, width, h), BG_DARK, ACCENT, 10, alpha=240)
        x = text(surface, "IDEA", (r.x + 12, r.y + 7), 15, ACCENT, bold=True).right
        text(surface, title, (x + 10, r.y + 7), 15, TEXT, bold=True)
        y = r.y + 30
        for line in lines:
            text(surface, line, (r.x + 12, y), 15, TEXT, raw=True)
            y += 21

    def draw_world(self, surface):
        pass

    def status_text(self):
        return ""

    def draw_top_bar(self, surface):
        pygame.draw.rect(surface, BG_DARK, (0, 0, WIDTH, TOP_BAR))
        pygame.draw.line(surface, PANEL_EDGE, (0, TOP_BAR), (WIDTH, TOP_BAR))
        text(surface, f"L{self.level.num}  {self.level.title}", (14, 10), 20, TEXT, bold=True)
        c = self.cost()
        col = GOOD if c <= self.level.par_cost else (WARN if c <= self.budget else BAD)
        money = f"Cost {economy.format_rs(c)} / {economy.format_rs(self.budget)}"
        if self.salvage:
            money += f" (+salvage {economy.format_rs(self.salvage)})"
        text(surface, money, (390, 12), 17, col, bold=True)
        text(surface, f"EXP {self.app.save.exp}", (720, 12), 17, ACCENT, bold=True)
        from .i18n import lang
        self.lang_btn.label = "English" if lang() == "bn" else "বাংলা"

    def draw_bottom_bar(self, surface):
        pygame.draw.rect(surface, BG_DARK, (0, HEIGHT - BOTTOM_BAR, WIDTH, BOTTOM_BAR))
        pygame.draw.line(surface, PANEL_EDGE, (0, HEIGHT - BOTTOM_BAR), (WIDTH, HEIGHT - BOTTOM_BAR))
        st = self.status_text()
        if st:
            text(surface, st, (WIDTH - DRAWER_W - 12, HEIGHT - BOTTOM_BAR + 18), 15, MUTED,
                 anchor="topright")
