"""Title screen and level select."""
import math

import pygame

from engine.levels import LEVELS

from .. import sound
from ..ui import (ACCENT, BG_DARK, CYAN, GOOD, HEIGHT, LINE, MUTED, PANEL, PANEL_EDGE, TEXT,
                  WIDTH, Button, WidgetGroup, blueprint_background, panel, text, text_block)

def language_button_label():
    from ..i18n import lang
    return "বাংলা / English" if lang() == "bn" else "English / বাংলা"


SCENE_LABEL = {"bridge": "Build a bridge", "rail": "Lay a railway", "cantilever": "Cast a cantilever",
               "signals": "Wire the signals", "traffic": "Tame the traffic",
               "logistics": "Plan the freight"}


class MenuScene:
    def __init__(self, app):
        self.app = app
        self.widgets = WidgetGroup()
        self.cards = []
        self.t = 0.0
        cw, ch, gap = 228, 200, 16
        x0 = (WIDTH - (5 * cw + 4 * gap)) // 2
        for k, lv in enumerate(LEVELS):
            r = pygame.Rect(x0 + (k % 5) * (cw + gap), 190 + (k // 5) * (ch + gap), cw, ch)
            self.cards.append((r, lv))
        self.widgets.add(Button((WIDTH - 140, HEIGHT - 56, 120, 40), "Quit", app.quit,
                                hotkey=pygame.K_ESCAPE))
        self.lang_btn = self.widgets.add(Button((40, 150, 170, 36), "", app.toggle_language,
                                                hotkey=pygame.K_F2, size=16,
                                                tooltip="English / Bengali (F2)"))
        self.lang_btn.label = language_button_label()
        self.hover = None

    def handle(self, event):
        if self.widgets.handle(event):
            return
        if event.type == pygame.MOUSEMOTION:
            self.hover = next((lv.num for r, lv in self.cards if r.collidepoint(event.pos)), None)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for r, lv in self.cards:
                if r.collidepoint(event.pos) and self.app.save.unlocked(lv.num):
                    sound.play("click")
                    self.app.start_level(lv.num)
                    return
        if event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_9:
            self.app.start_level(event.key - pygame.K_0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            self.app.start_level(10)

    def update(self, dt):
        self.t += dt
        self.lang_btn.label = language_button_label()

    def draw(self, s):
        blueprint_background(s)
        # a little animated truss as a logo
        for k in range(9):
            x = 120 + k * 46
            y = 92 + (0 if k % 2 == 0 else -36)
            if k:
                px = 120 + (k - 1) * 46
                py = 92 + (0 if (k - 1) % 2 == 0 else -36)
                pygame.draw.line(s, ACCENT, (px, py), (x, y), 4)
            if k % 2 == 0 and k >= 2:
                pygame.draw.line(s, LINE, (x - 92, 92), (x, 92), 4)
        bob = 4 * math.sin(self.t * 2)
        text(s, "MODIS BridgeWorks", (560, 40 + bob), 54, TEXT, bold=True)
        text(s, "Calculate. Construct. Route.  -  a hard-physics engineering sandbox", (564, 112), 18, CYAN)
        text(s, f"EXP {self.app.save.exp}", (WIDTH - 40, 150), 20, ACCENT, bold=True, anchor="topright")
        for r, lv in self.cards:
            prog = self.app.save.level(lv.num)
            unlocked = self.app.save.unlocked(lv.num)
            col = PANEL if self.hover != lv.num else (40, 70, 115)
            panel(s, r, col, ACCENT if self.hover == lv.num else PANEL_EDGE, 12)
            text(s, f"{lv.num}", (r.x + 14, r.y + 8), 34, ACCENT, bold=True)
            text(s, lv.tier.split(":")[0], (r.right - 12, r.y + 14), 13, MUTED, anchor="topright")
            text_block(s, lv.title, (r.x + 14, r.y + 56), r.w - 28, 19, TEXT, bold=True)
            text(s, SCENE_LABEL[lv.scene], (r.x + 14, r.y + 118), 15, CYAN)
            for k in range(3):
                c = ACCENT if k < prog["stars"] else (60, 70, 90)
                cx, cy = r.x + 26 + k * 30, r.bottom - 26
                pts = [(cx + (11 if j % 2 == 0 else 5) * math.cos(math.radians(-90 + 36 * j)),
                        cy + (11 if j % 2 == 0 else 5) * math.sin(math.radians(-90 + 36 * j)))
                       for j in range(10)]
                pygame.draw.polygon(s, c, pts)
            if prog["done"]:
                text(s, "DONE", (r.right - 14, r.bottom - 36), 14, GOOD, bold=True, anchor="topright")
            if not unlocked:
                veil = pygame.Surface(r.size, pygame.SRCALPHA)
                veil.fill((0, 0, 0, 150))
                s.blit(veil, r.topleft)
                text(s, "LOCKED", r.center, 20, MUTED, bold=True, anchor="center")
        text(s, "Click a level (or press 1-9, 0 for level 10).  Inside a level: C toggles the "
                "calculator, Esc returns here.", (40, HEIGHT - 44), 15, MUTED)
        self.widgets.draw(s)
