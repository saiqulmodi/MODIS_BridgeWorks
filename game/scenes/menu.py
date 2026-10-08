"""Title screen and level select."""
import math

import pygame

from engine.levels import LEVELS

from .. import sound
from ..ui import (ACCENT, BG_DARK, CYAN, GOOD, HEIGHT, LINE, MUTED, PANEL, PANEL_EDGE, TEXT,
                  WARN, WIDTH, Button, WidgetGroup, blueprint_background, panel, text, text_block)

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
        from .. import screen
        self.widgets.add(Button((WIDTH - 230, 150 - 2, 190, 36), "Full screen (F11)",
                                screen.toggle_fullscreen, size=15,
                                tooltip="Fill the whole screen; press F11 again to leave"))
        self.widgets.add(Button((222, 150, 210, 36), "Help: how to play (H)", self.open_help,
                                hotkey=pygame.K_h, size=16,
                                tooltip="A guide for new players and 200 questions & answers"))
        self.widgets.add(Button((444, 150, 250, 36), "BridgeWorks Academy (A)", app.to_academy,
                                hotkey=pygame.K_a, size=16, colour=(40, 90, 70),
                                tooltip="Class 1-12 quizzes in 6 subjects: earn Civil Grants for your bridges"))
        self.widgets.add(Button((WIDTH - 404, HEIGHT - 56, 250, 40), "Donation Camps (D)", app.to_donations,
                                hotkey=pygame.K_d, size=16, colour=(90, 70, 30),
                                tooltip="Give Civil Grants to causes that build opportunities"))

        # Register ID button
        self.widgets.add(Button((706, 150, 130, 36), "Register ID", self.open_register,
                                size=15, tooltip="Register with Name to unlock earnings"))

        # NCERT Bank button right next to Register ID
        self.widgets.add(Button((846, 150, 130, 36), "NCERT Bank", self.open_ncert_bank,
                                size=15, tooltip="Browse Phase 1 & 2 Question Bank"))

        self.help = None
        self.register_overlay = None
        self.ncert_overlay = None
        self.hover = None

    def open_help(self):
        from ..help_screen import HelpOverlay
        sound.play("click")
        self.help = HelpOverlay(self.app, self.close_help)

    def close_help(self):
        self.help = None

    def open_register(self):
        from .register import RegisterOverlay
        sound.play("click")
        self.register_overlay = RegisterOverlay(self.app, self.on_register_success)

    def on_register_success(self, name, phone, email):
        from ..player_economy import PlayerProfile
        self.app.player_profile = PlayerProfile(name, phone, email)
        self.register_overlay = None

    def open_ncert_bank(self):
        from .ncert_overlay import NCERTBrowserOverlay
        sound.play("click")
        self.ncert_overlay = NCERTBrowserOverlay(self.app, self.close_ncert_bank)

    def close_ncert_bank(self):
        self.ncert_overlay = None

    def handle(self, event):
        if self.ncert_overlay is not None:
            self.ncert_overlay.handle(event)
            return
        if self.register_overlay is not None:
            self.register_overlay.handle(event)
            return
        if self.help is not None:
            self.help.handle(event)
            return
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
        if self.help is not None:
            self.help.update(dt)
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
        
        # Player Profile status check on top bar
        has_profile = hasattr(self.app, "player_profile") and self.app.player_profile is not None
        profile_text = f"Player: {self.app.player_profile.name}" if has_profile else "Not Registered"
        text(s, profile_text, (WIDTH - 320, 154), 16, GOOD if has_profile else WARN, bold=True, anchor="topright")
        text(s, f"EXP {self.app.save.exp}", (WIDTH - 250, 194), 20, ACCENT, bold=True, anchor="topright")

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
                "calculator, H opens Help, Esc returns here.", (40, HEIGHT - 44), 15, MUTED)
        self.widgets.draw(s)
        if self.help is not None:
            self.help.draw(s)
        if self.register_overlay is not None:
            self.register_overlay.draw(s)
        if self.ncert_overlay is not None:
            self.ncert_overlay.draw(s)