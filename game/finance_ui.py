"""Business Plan / Bank Loan screen: shown before an over-budget project is built, and on demand."""
import pygame

from engine import economy
from engine import finance as F

from . import sound
from .ui import (ACCENT, BAD, BG_DARK, CYAN, GOOD, HEIGHT, MUTED, PANEL, PANEL_EDGE, TEXT, WARN,
                 WIDTH, Button, Slider, WidgetGroup, mini_chart, panel, text, text_block)

rs = economy.format_rs


def plan_for(scene, cost=None):
    cost = scene.cost() if cost is None else cost
    return F.business_plan(scene.level.num, scene.budget, cost, scene.toll_factor,
                           getattr(scene, "toll_efficiency", 1.0), govt=scene.govt_loan)


class FinanceOverlay:
    """mode 'loan': the design costs more than the budget - offer a bank loan (if viable).
    mode 'view': just show the business plan."""
    blocks_world = True

    def __init__(self, scene, mode="view", on_accept=None):
        self.scene = scene
        self.mode = mode
        self.on_accept = on_accept
        self.rect = pygame.Rect(60, 52, WIDTH - 120, HEIGHT - 96)
        r = self.rect
        self.widgets = WidgetGroup()
        self.chart = pygame.Rect(r.x + 570, r.y + 56, r.w - 594, r.h - 270)
        cx = self.chart.x
        self.slider = self.widgets.add(Slider((cx, self.chart.bottom + 112, self.chart.w, 40),
                                              "Toll rate (x standard)", F.TOLL_RANGE[0], F.TOLL_RANGE[1],
                                              scene.toll_factor, self._set_toll, "{:.2f}", 0.05))
        self.govt_btn = self.widgets.add(Button((cx, self.chart.bottom + 36, self.chart.w, 34), "",
                                                self._toggle_govt, toggle=True, active=scene.govt_loan,
                                                size=14))
        if mode == "loan":
            self.take_btn = self.widgets.add(Button((r.x + 24, r.bottom - 60, 300, 44), "Take loan & build",
                                                    self.accept, size=16, colour=(40, 110, 70),
                                                    hotkey=pygame.K_RETURN))
            self.widgets.add(Button((r.x + 340, r.bottom - 60, 300, 44), "Go back and cut costs",
                                    self.close, size=16, hotkey=pygame.K_ESCAPE))
        else:
            self.take_btn = None
            self.widgets.add(Button((r.right - 224, r.bottom - 60, 200, 44), "Close", self.close, size=16,
                                    hotkey=pygame.K_ESCAPE))
        self.plan = plan_for(scene)

    def _toggle_govt(self):
        self.scene.govt_loan = self.govt_btn.active
        self.plan = plan_for(self.scene)

    def _set_toll(self, v):
        self.scene.toll_factor = v
        self.plan = plan_for(self.scene)

    def accept(self):
        if not self.plan.viable:
            sound.play("click")
            return
        self.scene.loan = self.plan.loan
        self.scene.overlay = None
        sound.play("kaching")
        if self.on_accept:
            self.on_accept()

    def close(self):
        self.scene.overlay = None

    def handle(self, event):
        return self.widgets.handle(event) or event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)

    def update(self, dt):
        self.govt_btn.label = ("Govt subsidised loan: ON (0.5%, 15 yr, up to half the budget)"
                               if self.scene.govt_loan else
                               "Govt subsidised loan: OFF - click to apply (0.5%, 15 yr)")
        if self.take_btn is not None:
            self.take_btn.enabled = self.plan.viable

    def draw(self, surface):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 160))
        surface.blit(veil, (0, 0))
        p = self.plan
        sc = self.scene
        r = panel(surface, self.rect, PANEL, ACCENT if self.mode == "loan" else CYAN, 14)
        title = "BANK LOAN NEEDED" if self.mode == "loan" and p.loan > 0 else "BUSINESS PLAN"
        text(surface, title, (r.x + 24, r.y + 14), 26, TEXT, bold=True)
        name, rate, unit = F.TOLLS[sc.level.num]
        x, y, w = r.x + 24, r.y + 56, 520
        rows = [("Build cost", rs(p.build_cost), None), ("Your budget", rs(sc.budget), None)]
        if p.loan:
            rows.append(("Shortfall = loans", rs(p.loan), WARN))
        for label, value, col in rows:
            text(surface, label, (x, y), 16, MUTED)
            text(surface, value, (x + 300, y), 16, col or TEXT, bold=True)
            y += 23
        y += 4
        if p.loan:
            y = text_block(surface, "A = P r / (1 - (1 + r)^-n)   (equal yearly payments)", (x, y),
                           w, 15, CYAN, mono=True)
            if p.govt_loan:
                y = text_block(surface, f"Govt loan {rs(p.govt_loan)} at 0.5% for 15 yr = "
                                        f"{rs(p.govt_payment)} a year", (x, y), w, 14, GOOD)
            if p.bank_loan:
                y = text_block(surface, f"Bank loan {rs(p.bank_loan)} at 2% for 10 yr = "
                                        f"{rs(p.bank_payment)} a year", (x, y), w, 14, TEXT)
            if p.govt_loan:
                y = text_block(surface, f"The subsidy saves {rs(p.subsidy_saving)} of interest",
                               (x, y), w, 14, GOOD)
            y += 6
        y = text_block(surface, f"{name}: {rs(rate * p.toll_factor)} per {unit}, about "
                                f"{p.users_day:,.0f} a day", (x, y), w, 15, TEXT)
        y = text_block(surface, f"Year-1 income = rate x users x 365 = {rs(p.income1)}; "
                                f"upkeep 3% of cost = {rs(p.upkeep1)} a year", (x, y), w, 15, TEXT)
        y += 6
        if p.loan:
            ok = p.coverage >= F.MIN_COVERAGE
            y = text_block(surface, f"Coverage = (income - upkeep) / A = {p.coverage:.2f}   "
                                    f"(the bank needs 1.50 = a 50% margin)", (x, y), w, 16,
                           GOOD if ok else BAD, bold=True)
            verdict = ("The bank approves: tolls cover the loan with a 50% margin." if ok else
                       "The bank refuses: tolls would not cover the loan with a 50% margin. "
                       "Cut the cost, or raise the toll.")
            y = text_block(surface, verdict, (x, y + 2), w, 15, GOOD if ok else BAD)
        y += 6
        rec = (f"Investment recovered in year {p.payback_year}" if p.payback_year
               else f"Not recovered within {F.HORIZON} years")
        y = text_block(surface, rec, (x, y), w, 16, GOOD if p.payback_year else BAD, bold=True)
        if p.loan:
            y = text_block(surface, f"Loan repaid in year {p.loan_repaid_year or F.LOAN_YEARS}; interest "
                                    f"paid {rs(p.total_interest)}", (x, y), w, 15, TEXT)
        text_block(surface, f"Profit after {F.HORIZON} years: {rs(p.profit_horizon)} - traffic grows "
                            f"6% a year, so the business keeps growing", (x, y + 2), w, 15, ACCENT)
        text_block(surface, "Higher tolls earn more per user, but some users stay away "
                            "(users fall as 1 / sqrt(toll)).", (self.chart.x, self.chart.bottom + 74),
                   self.chart.w, 12, MUTED)
        # chart
        chart = self.chart
        cum = [(row.year, row.cumulative / 1e5) for row in p.rows]
        bal = [(0, p.loan / 1e5)] + [(row.year, row.balance / 1e5) for row in p.rows]
        mini_chart(surface, chart, [cum, bal] if p.loan else [cum], [GOOD, BAD],
                   "Your cash (green) and loan still owed (red), Rs lakh, by year",
                   x_marker=p.payback_year or None)
        if p.payback_year:
            text(surface, f"recovered: year {p.payback_year}", (chart.x + 10, chart.bottom + 8), 14, GOOD)
        self.widgets.draw(surface)
