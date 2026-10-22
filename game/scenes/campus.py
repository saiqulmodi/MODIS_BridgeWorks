from game.engineer_profile import EngineerTier
"""Campus World - the 3D front door of BridgeWorks.

Walk, jump and bridge-swing across a sunny campus. Every building is a part of the game:
the Primary/Middle/High schools, the College, NIT and IIT open the Academy at their classes,
the ten yellow pylons by the river are the bridge-building levels, the Help Library, the
Registration Office, the NCERT Archive, the Donation Camp and the Daily 5 Clock Tower open
their screens. The classic level menu stays one key (M) away.

Drawing is plain pygame (works in the browser through pygbag): engine/campus3d.py projects
the world, this file paints it far-to-near.
"""
import math

import pygame

from engine import campus3d as world
from engine import economy
from engine import magic
from engine.academy import SUBJECTS
from engine.academy_data import items as academy_items
from engine.levels import get as get_level

from .. import i18n, sound
from ..ui import HEIGHT, WEB, WIDTH, Button, WidgetGroup, measure, panel, text, wrap

SKY_TOP = (74, 140, 222)
SKY_LOW = (255, 214, 170)
FOG = (206, 222, 236)
GRASS_NEAR = (92, 170, 84)
GRASS_FAR = (150, 196, 120)
AVENUE = (176, 170, 158)
RIVER = (52, 132, 206)
DECK = (120, 112, 104)
PLAYER_SUIT = (40, 110, 220)
HAT = (255, 200, 40)
LIGHT = (0.45, 0.80, -0.40)
MAP = pygame.Rect(WIDTH - 196, 58, 182, 214)
# the browser runs Python more slowly, so it draws a little less fine detail far away
WINDOW_DIST = 85 if WEB else 140
TREE_DIST = 170 if WEB else 240
_FOG_CACHE = {}

WORDS = {
    "title": ("BridgeWorks Campus", "ব্রিজওয়ার্কস ক্যাম্পাস"),
    "levels": ("All levels (M)", "সব লেভেল (M)"),
    "help": ("Help (H)", "সাহায্য (H)"),
    "full": ("Full screen (F11)", "পূর্ণ পর্দা (F11)"),
    "tour": ("Guide me (T)", "পথ দেখাও (T)"),
    "lang": ("বাংলা (F2)", "English (F2)"),
    "zip": ("Zip there (Z)", "ওখানে উড়ে যাও (Z)"),
    "enter": ("Press E or tap ENTER:  {n}", "E চাপো বা ENTER ছোঁও:  {n}"),
    "wallet": ("Grants {g}   EXP {x}", "অনুদান {g}   অভিজ্ঞতা {x}"),
    "to": ("{n}  {d} m", "{n}  {d} মি"),
    "splash": ("Splash! Swing across on the river pylons or use the bridge.",
               "ঝপাং! নদীর খুঁটিতে দড়ি ঝুলিয়ে পার হও বা সেতু দিয়ে যাও।"),
    "locked": ("Bridge site {n} is locked - finish site {p} first.",
               "সেতু-ক্ষেত্র {n} বন্ধ - আগে {p} নম্বর শেষ করো।"),
    "pick_class": ("Which class?", "কোন শ্রেণি?"),
    "class_n": ("Class {c}", "শ্রেণি {c}"),
    "grant_note": ("A right first answer earns a Civil Grant for your bridges.",
                   "প্রথম চেষ্টায় সঠিক উত্তরে তোমার সেতুর জন্য সিভিল অনুদান।"),
    "read_help": ("Read: how to play", "পড়ো: কীভাবে খেলবে"),
    "skills": ("Game-skills quiz", "খেলার দক্ষতা কুইজ"),
    "close": ("Close (Esc)", "বন্ধ (Esc)"),
    "jump": ("JUMP", "লাফ"),
    "swing": ("SWING", "দোল"),
    "go_in": ("ENTER", "ঢোকো"),
    "tip_title": ("Welcome to the campus!", "ক্যাম্পাসে স্বাগতম!"),
    "tip1": ("Walk: arrow keys / W A S D (or the arrow pads).",
             "হাঁটো: তীর-চাবি / W A S D (বা তীর-বোতাম)।"),
    "tip2": ("Jump: SPACE. In the air, HOLD SPACE to swing from the glowing anchor.",
             "লাফ: SPACE। শূন্যে SPACE ধরে রাখো - জ্বলজ্বলে বিন্দু থেকে দোল খাও।"),
    "tip3": ("Walk up to a building and press E to go in.", "কোনো ভবনের কাছে গিয়ে E চাপো, ভেতরে ঢোকো।"),
    "tip4": ("Click a building or the map to choose it, then Zip there.",
             "কোনো ভবন বা মানচিত্রে ক্লিক করো, তারপর উড়ে যাও।"),
    "got_it": ("Let's go!", "চলো যাই!"),
    "tip5": ("Class 1-7: answer Academy questions to earn magic tools - ZIP onto roofs, BOOTS to jump high, "
             "CAPE to float (keys Q, B, hold G).",
             "শ্রেণি ১-৭: একাডেমির প্রশ্নের উত্তর দিয়ে জাদুর সরঞ্জাম জেতো - জিপে ছাদে ওঠো, বুটে উঁচু লাফ, "
             "কেপে ভাসো (Q, B, G ধরে রাখো)।"),
    "locked_tool": ("{t} is locked: answer {n} Class {c} Academy questions right ({h}/{n}). Go to the school!",
                    "{t} বন্ধ: একাডেমিতে শ্রেণি {c}-এর {n}টি প্রশ্নের সঠিক উত্তর দাও ({h}/{n})। স্কুলে যাও!"),
    "new_tool": ("New magic tool: {t} - {d}!", "নতুন জাদুর সরঞ্জাম: {t} - {d}!"),
    "no_roof": ("Face a building to zip onto its roof!", "ছাদে উঠতে একটা ভবনের দিকে মুখ করো!"),
    "ready": ("{r} of {n} subjects ready", "{n}টির মধ্যে {r}টি বিষয় তৈরি"),
}

TOUR = ["primary", "library", "site1", "middle", "high", "college", "nit", "iit", "archive", "camp",
        "tower", "registry"]


def w(key, **kw):
    en, bn = WORDS[key]
    return (bn if i18n.lang() == "bn" else en).format(**kw)


def pair(p):
    return p[1] if i18n.lang() == "bn" and p[1] else p[0]


def _mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def _shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c)


def _inside(pt, poly):
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-9) + x1:
            inside = not inside
    return inside


ARROWS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


class HoldPad:
    """An on-screen button that counts while it is held (for touch screens)."""

    def __init__(self, rect, label, colour=(30, 60, 100)):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.colour = colour
        self.held = False
        self.visible = True
        self.locked = None          # "2/5" while a magic tool is still being earned

    def draw(self, s):
        surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        col = (*_shade(self.colour, 1.5 if self.held else (0.45 if self.locked else 1.0)), 190)
        pygame.draw.rect(surf, col, surf.get_rect(), border_radius=14)
        pygame.draw.rect(surf, (255, 255, 255, 120), surf.get_rect(), 2, border_radius=14)
        s.blit(surf, self.rect.topleft)
        if self.label in ARROWS:
            c, k = self.rect.center, self.rect.w * 0.22
            dx, dy = ARROWS[self.label]
            tip = (c[0] + dx * k, c[1] + dy * k)
            side = ((-dy) * k * 0.9, dx * k * 0.9)
            back = (c[0] - dx * k * 0.7, c[1] - dy * k * 0.7)
            pygame.draw.polygon(s, (255, 255, 255), [tip, (back[0] + side[0], back[1] + side[1]),
                                                     (back[0] - side[0], back[1] - side[1])])
            return
        if self.locked:
            c = self.rect.center
            lk = pygame.Rect(0, 0, 18, 14)
            lk.midtop = (c[0], c[1] - 18)
            pygame.draw.arc(s, (255, 255, 255), (lk.x + 3, lk.y - 9, 12, 18), 0, math.pi, 3)
            pygame.draw.rect(s, (255, 255, 255), lk, border_radius=3)
            text(s, self.label, (c[0], c[1] + 8), 14, (220, 225, 235), bold=True, anchor="center", raw=True)
            text(s, self.locked, (c[0], c[1] + 26), 13, (255, 220, 120), bold=True, anchor="center", raw=True)
            return
        text(s, self.label, self.rect.center, 15, (255, 255, 255), bold=True, anchor="center", raw=True)


class Picker:
    """A small panel of choices shown on top of the campus (e.g. which class)."""

    def __init__(self, title, sub, choices, on_close):
        self.title, self.sub = title, sub
        self.widgets = WidgetGroup()
        n = len(choices)
        cols = min(4, n)
        rows = -(-n // cols)
        bw = 200
        self.rect = pygame.Rect(0, 0, max(460, cols * (bw + 12) + 40), 170 + rows * 58)
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        x0 = self.rect.centerx - (cols * (bw + 12) - 12) // 2
        for k, (label, fn, colour) in enumerate(choices):
            r = (x0 + (k % cols) * (bw + 12), self.rect.y + 96 + (k // cols) * 58, bw, 48)
            self.widgets.add(Button(r, label, fn, size=18, colour=colour))
        self.widgets.add(Button((self.rect.centerx - 80, self.rect.bottom - 54, 160, 38), w("close"),
                                on_close, size=15, hotkey=pygame.K_ESCAPE))

    def handle(self, e):
        self.widgets.handle(e)

    def draw(self, s):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((8, 16, 30, 140))
        s.blit(veil, (0, 0))
        panel(s, self.rect, (24, 46, 80), (255, 196, 64), 16)
        text(s, self.title, (self.rect.centerx, self.rect.y + 18), 28, (255, 214, 120), bold=True,
             anchor="midtop", raw=True)
        text(s, self.sub, (self.rect.centerx, self.rect.y + 58), 16, (200, 220, 245), anchor="midtop",
             raw=True)
        self.widgets.draw(s)


class CampusScene:
    def __init__(self, app):
        self.app = app
        self.boxes = world.build_world()
        self.by_key = {b.key: b for b in self.boxes}
        self.trees, self.lamps = world.trees_and_lamps()
        state = getattr(app, "campus_state", None)
        if state:
            self.player = world.Player(state[0], state[1])
        else:
            self.player = world.Player()
        self.cam = world.Camera(WIDTH, HEIGHT)
        self.cam.follow(self.player.pos, self.player.yaw)
        self.t = 0.0
        self.target = None
        self.tour_k = 0
        self.toast = ("", 0.0)
        self.picker = None
        self.help = None
        self.register_overlay = None
        self.ncert_overlay = None
        self.space_held = False
        self.drag = None
        self.hit_polys = {}
        self.anchor = None
        self.show_tips = not app.save.data.get("campus_seen")
        self._ready = {}
        self.widgets = WidgetGroup()
        self.lang_btn = self.widgets.add(Button((14, 10, 120, 34), "", app.toggle_language,
                                                hotkey=pygame.K_F2, size=15))
        self.levels_btn = self.widgets.add(Button((142, 10, 160, 34), "", app.to_classic_menu,
                                                  hotkey=pygame.K_m, size=15, colour=(40, 90, 70)))
        self.help_btn = self.widgets.add(Button((310, 10, 120, 34), "", self.open_help,
                                                hotkey=pygame.K_h, size=15))
        self.tour_btn = self.widgets.add(Button((438, 10, 150, 34), "", self.next_tour,
                                                hotkey=pygame.K_t, size=15, colour=(110, 70, 140)))
        from .. import screen
        self.full_btn = self.widgets.add(Button((596, 10, 170, 34), "", screen.toggle_fullscreen, size=15))
        self.zip_btn = self.widgets.add(Button((WIDTH // 2 - 100, 96, 200, 38), "", self.zip_to_target,
                                               hotkey=pygame.K_z, size=16, colour=(200, 120, 30)))
        self.got_it = Button((40, 380, 180, 40), "", self.close_tips, size=16, colour=(40, 120, 70))
        pad, gap = 70, 8
        bx, by = 26, HEIGHT - 26 - 2 * pad - gap
        self.pads = {
            "up": HoldPad((bx + pad + gap, by, pad, pad), "up"),
            "left": HoldPad((bx, by + pad + gap, pad, pad), "left"),
            "down": HoldPad((bx + pad + gap, by + pad + gap, pad, pad), "down"),
            "right": HoldPad((bx + 2 * (pad + gap), by + pad + gap, pad, pad), "right"),
            "jump": HoldPad((WIDTH - 26 - 3 * 96 - 16, HEIGHT - 26 - 80, 96, 80), "", (40, 120, 70)),
            "swing": HoldPad((WIDTH - 26 - 2 * 96 - 8, HEIGHT - 26 - 80, 96, 80), "", (200, 120, 30)),
            "enter": HoldPad((WIDTH - 26 - 96, HEIGHT - 26 - 80, 96, 80), "", (150, 60, 120)),
            # magic tools for Class 1-7 players, earned in the Academy (engine/magic.py)
            "zip": HoldPad((WIDTH - 26 - 3 * 96 - 16, HEIGHT - 26 - 168, 96, 80), "", (230, 110, 40)),
            "boots": HoldPad((WIDTH - 26 - 2 * 96 - 8, HEIGHT - 26 - 168, 96, 80), "", (50, 120, 220)),
            "cape": HoldPad((WIDTH - 26 - 96, HEIGHT - 26 - 168, 96, 80), "", (140, 70, 210)),
        }
        self.cape_hold = False
        self.web_flash = None         # (anchor, until): the web line of a web-zip
        self._magic_key = None
        self.sky = self._sky_surface()
        self.hills = self._hills_surface()
        self._labels()
        self.refresh_magic()

    # --- pre-rendered backdrop ----------------------------------------------------------
    def _sky_surface(self):
        hy = int(self.cam.horizon_y())
        s = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            if y <= hy:
                col = _mix(SKY_TOP, SKY_LOW, (y / max(1, hy)) ** 1.6)
            else:
                k = ((y - hy) / max(1, HEIGHT - hy)) ** 0.7
                col = _mix(GRASS_FAR, GRASS_NEAR, k)
            pygame.draw.line(s, col, (0, y), (WIDTH, y))
        return s

    def _hills_surface(self):
        """A wide strip of distant hills and a city skyline that scrolls as you turn."""
        bw = int(self.cam.focal * 2 * math.pi)
        s = pygame.Surface((bw, 120), pygame.SRCALPHA)
        pts = [(0, 120)]
        for x in range(0, bw + 1, 12):
            y = 70 - 26 * math.sin(x * 0.004) - 14 * math.sin(x * 0.011 + 1.3) - 6 * math.sin(x * 0.031)
            pts.append((x, y))
        pts.append((bw, 120))
        pygame.draw.polygon(s, (150, 176, 196), pts)
        for k in range(60):                      # a far skyline, in the haze
            x = (k * 97) % bw
            h = 18 + (k * 37) % 40
            ww = 10 + (k * 13) % 18
            pygame.draw.rect(s, (168, 190, 208), (x, 120 - h - 10, ww, h + 10))
        pts = [(0, 120)]
        for x in range(0, bw + 1, 10):
            y = 96 - 12 * math.sin(x * 0.007 + 0.4) - 7 * math.sin(x * 0.019)
            pts.append((x, y))
        pts.append((bw, 120))
        pygame.draw.polygon(s, (118, 160, 120), pts)
        return s

    def _labels(self):
        self.lang_btn.label = w("lang")
        self.levels_btn.label = w("levels")
        self.help_btn.label = w("help")
        self.tour_btn.label = w("tour")
        self.full_btn.label = w("full")
        self.zip_btn.label = w("zip")
        self.got_it.label = w("got_it")
        self.pads["jump"].label = w("jump")
        for key, _classes, name, _does in magic.TOOLS:
            self.pads[key].label = pair(name)
        self.pads["swing"].label = w("swing")
        self.pads["enter"].label = w("go_in")

    # --- helpers ------------------------------------------------------------------------
    def box_name(self, b):
        if b.kind == "level":
            return pair(b.label)
        return pair(b.label)

    def box_sub(self, b):
        if b.kind == "level":
            return i18n.tr(get_level(b.payload).title)
        if b.kind == "school" and b.payload[0] >= 13:   # NIT / IIT: say how much is ready
            ready = self.ready_subjects(b.payload[0])
            return f"{pair(b.sub)} - {w('ready', r=ready, n=len(SUBJECTS))}"
        return pair(b.sub)

    def ready_subjects(self, c):
        if c not in self._ready:
            self._ready[c] = sum(1 for subj in SUBJECTS if academy_items(c, subj))
        return self._ready[c]

    def say(self, msg, secs=3.5):
        self.toast = (msg, secs)

    def close_tips(self):
        self.show_tips = False
        self.app.save.data["campus_seen"] = True
        self.app.save.write()

    def next_tour(self):
        sound.play("click")
        self.target = self.by_key[TOUR[self.tour_k % len(TOUR)]]
        self.tour_k += 1
        self.say(f"{self.box_name(self.target)} - {self.box_sub(self.target)}", 4.0)

    def zip_to_target(self):
        if self.target is None or self.player.zip is not None:
            return
        sound.play("whoosh")
        self.player.zip_to(self.target.door())

    def remember_spot(self, b):
        """Come back to this door after the screen you open is closed."""
        door = b.door()
        self.app.campus_state = (door, self.player.yaw)
        self.app.home = "campus"

    # --- entering buildings -------------------------------------------------------------
    def enter(self, b):
        sound.play("click")
        kind = b.kind
        if kind == "school":
            if len(b.payload) == 1:
                self.go_class(b, b.payload[0])
                return
            choices = [(w("class_n", c=c), lambda c=c: self.go_class(b, c), (40, 90, 140)) for c in b.payload]
            self.picker = Picker(f"{pair(b.label)} - {w('pick_class')}", w("grant_note"), choices,
                                 self.close_picker)
        elif kind == "library":
            choices = [(w("read_help"), self.open_help, (40, 90, 140)),
                       (w("skills"), lambda: self.go_academy(b, subject="skills"), (40, 110, 70))]
            self.picker = Picker(pair(b.label), pair(b.sub), choices, self.close_picker)
        elif kind == "register":
            from .register import RegisterOverlay
            self.register_overlay = RegisterOverlay(self.app, self.on_register_success)
        elif kind == "ncert":
            from .ncert_overlay import NCERTBrowserOverlay
            self.ncert_overlay = NCERTBrowserOverlay(self.app, self.close_ncert)
        elif kind == "donate":
            self.remember_spot(b)
            self.app.to_donations()
        elif kind == "daily":
            self.go_academy(b, subject="daily")
        elif kind == "level":
            n = b.payload
            if not self.app.save.unlocked(n):
                self.say(w("locked", n=n, p=n - 1))
                return
            self.remember_spot(b)
            self.app.start_level(n)

    def go_class(self, b, c):
        self.app.save.academy["class"] = c
        self.app.save.write()
        self.go_academy(b)

    def go_academy(self, b, subject=None):
        self.picker = None
        self.remember_spot(b)
        self.app.to_academy()
        if subject:
            self.app.scene.pick_subject(subject)

    def close_picker(self):
        self.picker = None

    def open_help(self):
        from ..help_screen import HelpOverlay
        self.picker = None
        sound.play("click")
        self.help = HelpOverlay(self.app, self.close_help)

    def close_help(self):
        self.help = None

    def close_ncert(self):
        self.ncert_overlay = None

    def on_register_success(self, name, phone, email):
        from ..player_economy import PlayerProfile
        self.app.player_profile = PlayerProfile(name, phone, email, data=self.app.save.data,
                                                on_change=self.app.save.write)
        self.register_overlay = None

    # --- input --------------------------------------------------------------------------
    def overlay(self):
        return self.ncert_overlay or self.register_overlay or self.help or self.picker

    def pick_box_at(self, pos):
        if MAP.collidepoint(pos):
            best, best_d = None, 14.0
            for b in self.boxes:
                if b.kind is None:
                    continue
                r = self.map_rect(b)
                d = math.hypot(r.centerx - pos[0], r.centery - pos[1]) if not r.collidepoint(pos) else 0
                if d < best_d:
                    best, best_d = b, d
            return best
        for key in reversed(list(self.hit_polys)):          # nearest drawn last
            for poly in self.hit_polys[key]:
                if _inside(pos, poly):
                    return self.by_key[key]
        return None

    def handle(self, e):
        ov = self.overlay()
        if ov is not None:
            ov.handle(e)
            return
        if self.show_tips and self.got_it.handle(e):
            return
        if self.widgets.handle(e):
            return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for name, p in self.pads.items():
                if p.visible and p.rect.collidepoint(e.pos):
                    p.held = True
                    if name in ("zip", "boots", "cape"):
                        self.use_tool(name)
                    elif name == "jump":
                        self.jump_or_swing(True)
                    elif name == "swing":
                        self.swing(True)
                    elif name == "enter":
                        self.try_enter()
                    return
            b = self.pick_box_at(e.pos)
            if b is not None and b.kind is not None:
                if self.target is b:
                    self.zip_to_target()
                else:
                    sound.play("click")
                    self.target = b
                    self.say(f"{self.box_name(b)} - {self.box_sub(b)}", 4.0)
                return
            self.drag = e.pos[0]
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
            self.swing(True)
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 3:
            self.swing(False)
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            for name, p in self.pads.items():
                if p.held and name in ("jump", "swing"):
                    self.swing(False)
                p.held = False
            self.cape_hold = False
            self.drag = None
        elif e.type == pygame.MOUSEMOTION and self.drag is not None:
            self.player.yaw += (e.pos[0] - self.drag) * 0.006
            self.drag = e.pos[0]
        elif e.type == pygame.MOUSEWHEEL:
            self.cam.dist = max(8.0, min(32.0, self.cam.dist - e.y * 1.5))
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                self.jump_or_swing(True)
            elif e.key in (pygame.K_e, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.try_enter()
            elif e.key == pygame.K_q:
                self.use_tool("zip")
            elif e.key == pygame.K_b:
                self.use_tool("boots")
            elif e.key == pygame.K_ESCAPE:
                self.target = None
        elif e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
            self.swing(False)

    def jump_or_swing(self, down):
        if self.player.zip is not None:
            return
        if self.player.grounded:
            if self.player.jump():
                sound.play("click")
            self.space_held = True
        else:
            self.swing(True)

    def swing(self, down):
        if down:
            self.space_held = True
            if self.player.rope is None and self.player.zip is None:
                if self.player.grounded:
                    self.player.jump()
                if self.player.attach(self.boxes):
                    sound.play("whoosh")
        else:
            self.space_held = False
            if self.player.rope is not None:
                self.player.release()

    # --- magic tools ------------------------------------------------------------------------
    def refresh_magic(self):
        """Show the tool belt to Class 1-7 players and lock tools not yet earned; announce a
        tool the moment it is earned."""
        save = self.app.save
        a = save.academy
        key = (a.get("class"), len(a["answered"]), i18n.lang())
        if key == self._magic_key:
            return
        self._magic_key = key
        show = magic.eligible(save)
        seen = save.data.setdefault("magic_seen", [])
        for tool, _classes, name, does in magic.TOOLS:
            pad = self.pads[tool]
            pad.visible = show
            have, need = magic.progress(save, tool)
            pad.locked = None if have >= need else f"{have}/{need}"
            if show and pad.locked is None and tool not in seen:
                seen.append(tool)
                save.write()
                sound.play("kaching")
                self.say(w("new_tool", t=pair(name), d=pair(does)), 5.0)

    def tool_ready(self, tool):
        pad = self.pads[tool]
        if not pad.visible:
            return False
        if pad.locked:
            have, need = magic.progress(self.app.save, tool)
            self.say(w("locked_tool", t=pad.label, c=magic.class_range(tool), h=have, n=need), 5.0)
            school = "primary" if magic.BY_KEY[tool][1][-1] <= 4 else "middle"
            self.target = self.by_key[school]
            return False
        return True

    def use_tool(self, tool):
        p = self.player
        if p.zip is not None or not self.tool_ready(tool):
            return
        if tool == "zip":
            anchor = p.web_pull(self.boxes)
            if anchor is None:
                self.say(w("no_roof"))
                return
            sound.play("whoosh")
            self.web_flash = (anchor, self.t + 1.6)
        elif tool == "boots":
            if p.super_jump():
                sound.play("whoosh")
        else:
            self.cape_hold = True
            if p.grounded:
                if self.pads["boots"].locked is None:
                    p.super_jump()
                else:
                    p.jump()

    def try_enter(self):
        b = world.nearest_entrance(self.boxes, self.player.pos)
        if b is not None:
            self.enter(b)

    # --- update -------------------------------------------------------------------------
    def update(self, dt):
        self.t += dt
        self._labels()
        if self.help is not None:
            self.help.update(dt)
        if self.ncert_overlay is not None:
            self.ncert_overlay.update(dt)
        msg, ttl = self.toast
        self.toast = (msg, max(0.0, ttl - dt))
        self.refresh_magic()
        if self.overlay() is not None:
            return
        try:
            keys = pygame.key.get_pressed()
        except pygame.error:
            keys = None

        def k(*codes):
            return bool(keys) and any(keys[c] for c in codes)

        fwd = (1.0 if (k(pygame.K_UP, pygame.K_w) or self.pads["up"].held) else 0.0) - \
              (1.0 if (k(pygame.K_DOWN, pygame.K_s) or self.pads["down"].held) else 0.0)
        turn = (1.0 if (k(pygame.K_RIGHT, pygame.K_d) or self.pads["right"].held) else 0.0) - \
               (1.0 if (k(pygame.K_LEFT, pygame.K_a) or self.pads["left"].held) else 0.0)
        if fwd or turn:
            if self.show_tips and self.t > 6:
                self.close_tips()
        if self.player.rope is None and not self.player.grounded and self.space_held \
                and self.player.zip is None and self.player.vel[1] < 2:
            if self.player.attach(self.boxes):         # holding SPACE through the jump
                sound.play("whoosh")
        cape = self.pads["cape"]
        self.player.glide(cape.visible and cape.locked is None and (self.cape_hold or k(pygame.K_g)))
        event = self.player.update(dt, self.boxes, fwd, turn)
        if event == "splash":
            sound.play("snap")
            self.say(w("splash"), 4.0)
        elif event == "arrived":
            sound.play("kaching")
        self.anchor = None if (self.player.rope or self.player.zip) else self.player.best_anchor(self.boxes)
        self.cam.follow(self.player.pos, self.player.yaw, dt)

    # --- drawing ------------------------------------------------------------------------
    def fog(self, col, depth):
        """Blend a colour into the haze with distance (cached in 4 m steps)."""
        key = (col, int(depth) >> 2)
        out = _FOG_CACHE.get(key)
        if out is None:
            if len(_FOG_CACHE) > 4000:
                _FOG_CACHE.clear()
            out = _FOG_CACHE[key] = _mix(col, FOG, min(0.8, max(0.0, ((key[1] << 2) - 50.0) / 260.0)))
        return out

    def draw(self, s):
        cam = self.cam
        s.blit(self.sky, (0, 0))
        hy = int(cam.horizon_y())
        # the sun, low in the north-east
        sun_yaw = 0.7
        d = (sun_yaw - cam.yaw + math.pi) % (2 * math.pi) - math.pi
        if abs(d) < 1.2:
            sx = cam.cx + cam.focal * math.tan(d)
            for r, a in ((70, 40), (46, 80), (30, 255)):
                glow = pygame.Surface((2 * r, 2 * r), pygame.SRCALPHA)
                pygame.draw.circle(glow, (255, 240, 190, a), (r, r), r)
                s.blit(glow, (sx - r, hy - 150 - r))
        bw = self.hills.get_width()
        off = int(-cam.yaw * cam.focal + cam.cx) % bw
        s.blit(self.hills, (off - bw, hy - 118))
        s.blit(self.hills, (off, hy - 118))
        self.draw_ground(s)
        items = []
        self.hit_polys = {}
        cp = cam.pos
        for b in self.boxes:
            cx, cy, cz = b.centre
            dist = math.dist((cx, cy, cz), cp)
            if dist > 300:
                continue
            items.append((dist, "box", b))
        for (x, z, h) in self.trees:
            dist = math.dist((x, h / 2, z), cp)
            if dist < TREE_DIST:
                items.append((dist, "tree", (x, z, h)))
        for (x, z) in self.lamps:
            dist = math.dist((x, 3, z), cp)
            if dist < 160:
                items.append((dist, "lamp", (x, z)))
        items.append((math.dist(self.player.pos, cp), "player", None))
        items.sort(key=lambda it: -it[0])
        labels = self.place_labels()
        for dist, kind, obj in items:
            if kind == "box":
                self.draw_box(s, obj, dist)
                if obj.key in labels:
                    self.draw_label(s, obj, *labels[obj.key])
            elif kind == "tree":
                self.draw_tree(s, obj, dist)
            elif kind == "lamp":
                self.draw_lamp(s, obj, dist)
            else:
                self.draw_player(s)
        self.draw_anchor(s)
        self.draw_hud(s)

    def ground_poly(self, s, pts, col):
        pr = self.cam.project_poly([(x, 0.0, z) for x, z in pts])
        if pr is None:
            return None
        poly, depth = pr
        if len(poly) >= 3:
            pygame.draw.polygon(s, self.fog(col, depth * 0.6), poly)
        return poly

    def draw_ground(self, s):
        x0, x1, z0, z1 = world.BOUNDS
        rz0, rz1 = world.RIVER_Z
        # avenue (in pieces so the far part fades nicely)
        for za in range(int(z0), int(z1), 30):
            zb = min(z1, za + 30)
            self.ground_poly(s, [(-6, za), (6, za), (6, zb), (-6, zb)], AVENUE)
        # side paths to every door
        for b in self.boxes:
            if b.kind in ("school", "library", "register", "ncert", "donate"):
                dx, _, dz = b.door()
                xa, xb = sorted((dx, 0.0))
                self.ground_poly(s, [(xa, dz - 2), (xb, dz - 2), (xb, dz + 2), (xa, dz + 2)], AVENUE)
        # a round plaza at the gate
        plaza = [(14 * math.cos(a / 12 * math.tau), 8 + 14 * math.sin(a / 12 * math.tau)) for a in range(12)]
        self.ground_poly(s, plaza, (196, 186, 170))
        # the river with moving ripples, then the avenue bridge over it
        self.ground_poly(s, [(x0, rz0), (x1, rz0), (x1, rz1), (x0, rz1)], RIVER)
        for k in range(8):
            z = rz0 + 2 + ((k * 2.1 + self.t * 1.2) % (rz1 - rz0 - 4))
            a = self.cam.project((x0 + 20, 0.02, z))
            b = self.cam.project((x1 - 20, 0.02, z))
            if a and b:
                pygame.draw.line(s, (120, 186, 236), a[:2], b[:2], 1)
        self.ground_poly(s, [(-7, rz0 - 2), (7, rz0 - 2), (7, rz1 + 2), (-7, rz1 + 2)], DECK)
        # building-site sand along the south bank
        self.ground_poly(s, [(x0, 82), (-12, 82), (-12, 93), (x0, 93)], (214, 190, 140))
        self.ground_poly(s, [(12, 82), (x1, 82), (x1, 93), (12, 93)], (214, 190, 140))
        # the target ring on the ground
        if self.target is not None:
            dx, _, dz = self.target.door()
            r = 2.6 + 0.4 * math.sin(self.t * 5)
            ring = [(dx + r * math.cos(a / 16 * math.tau), dz + r * math.sin(a / 16 * math.tau))
                    for a in range(16)]
            pr = self.cam.project_poly([(x, 0.05, z) for x, z in ring])
            if pr:
                pygame.draw.polygon(s, (255, 220, 60), pr[0], 4)

    def draw_box(self, s, b, dist):
        cam = self.cam
        x0, x1, z0, z1, y0, y1 = b.x0, b.x1, b.z0, b.z1, b.y0, b.h
        cp = cam.pos
        faces = []
        if cp[2] < z0:
            faces.append(((0, 0, -1), [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)]))
        if cp[2] > z1:
            faces.append(((0, 0, 1), [(x1, y0, z1), (x0, y0, z1), (x0, y1, z1), (x1, y1, z1)]))
        if cp[0] < x0:
            faces.append(((-1, 0, 0), [(x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, y1, z1)]))
        if cp[0] > x1:
            faces.append(((1, 0, 0), [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)]))
        if cp[1] > y1:
            faces.append(((0, 1, 0), [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]))
        if cp[1] < y0:
            faces.append(((0, -1, 0), [(x0, y0, z0), (x0, y0, z1), (x1, y0, z1), (x1, y0, z0)]))
        polys = []
        lit = self.target is b
        for n, pts in faces:
            pr = cam.project_poly(pts)
            if pr is None:
                continue
            poly, depth = pr
            k = 0.62 + 0.45 * max(0.0, n[0] * LIGHT[0] + n[1] * LIGHT[1] + n[2] * LIGHT[2])
            base = b.roof if n[1] > 0 else b.colour
            col = self.fog(_shade(base, k), dist)
            pygame.draw.polygon(s, col, poly)
            pygame.draw.polygon(s, self.fog(_shade(base, k * 0.7), dist), poly, 1)
            polys.append(poly)
            if n[1] == 0 and b.windows and dist < WINDOW_DIST:
                self.draw_windows(s, b, n, pts, dist)
            if n[1] == 0 and b.kind == "level":
                self.draw_stripes(s, b, pts, dist)
        if lit and polys:
            for poly in polys:
                pygame.draw.polygon(s, (255, 236, 120), poly, 3)
        if b.kind is not None and polys:
            self.hit_polys[b.key] = polys

    def draw_windows(self, s, b, n, pts, dist):
        cam = self.cam
        p0, p1, _, p3 = pts                     # bottom-left, bottom-right, top-left
        width = math.dist(p0, p1)
        height = b.h - b.y0
        cols = max(1, min(7, int(width / 3.6)))
        rows = max(1, min(9, int(height / 4.2)))
        door_face = False
        dx, _, dz = b.door()
        mid = ((p0[0] + p1[0]) / 2, (p0[2] + p1[2]) / 2)
        if math.hypot(mid[0] - dx, mid[1] - dz) < 4.0:
            door_face = True

        def at(u, v):
            return tuple(p0[i] + (p1[i] - p0[i]) * u + (p3[i] - p0[i]) * v for i in range(3))

        # the camera transform is linear, so the window grid is worked out in camera space from
        # the wall's corners once, instead of projecting every window corner from the world
        c0, c1, c3 = cam.to_cam(p0), cam.to_cam(p1), cam.to_cam(p3)
        near = min(c0[2], c1[2], c3[2], c1[2] + c3[2] - c0[2])
        win_px = cam.focal * (width / cols) * 0.5 / max(near, 0.6)
        if win_px >= 2.5:
            colours = {True: self.fog((255, 226, 140), dist), False: self.fog((60, 92, 130), dist)}
            us = [(c + f) / cols for c in range(cols) for f in (0.25, 0.75)]
            vs = [(r + f) / rows for r in range(rows) for f in (0.3, 0.75)]
            grid = None
            if near >= cam.NEAR:
                e1 = [c1[i] - c0[i] for i in range(3)]
                e3 = [c3[i] - c0[i] for i in range(3)]
                fx, cx, cy = cam.focal, cam.cx, cam.cy
                grid = []
                for v in vs:
                    row = []
                    for u in us:
                        x = c0[0] + e1[0] * u + e3[0] * v
                        y = c0[1] + e1[1] * u + e3[1] * v
                        z = c0[2] + e1[2] * u + e3[2] * v
                        row.append((cx + fx * x / z, cy - fx * y / z))
                    grid.append(row)
            for r in range(rows):
                for c in range(cols):
                    if door_face and r == 0 and abs((c + 0.5) / cols - 0.5) < 0.6 / cols:
                        continue
                    col = colours[(r * 7 + c * 3 + len(b.key)) % 5 == 0]
                    if grid is not None:
                        g0, g1 = grid[2 * r], grid[2 * r + 1]
                        poly = (g0[2 * c], g0[2 * c + 1], g1[2 * c + 1], g1[2 * c])
                    else:                       # wall reaches behind the camera: clip each one
                        pr = cam.project_poly([at(us[2 * c], vs[2 * r]), at(us[2 * c + 1], vs[2 * r]),
                                               at(us[2 * c + 1], vs[2 * r + 1]), at(us[2 * c], vs[2 * r + 1])])
                        if pr is None:
                            continue
                        poly = pr[0]
                    pygame.draw.polygon(s, col, poly)
        if door_face:
            dw = min(0.3, 3.0 / max(width, 1.0))
            pr = cam.project_poly([at(0.5 - dw / 2, 0), at(0.5 + dw / 2, 0),
                                   at(0.5 + dw / 2, min(0.9, 4.0 / height)),
                                   at(0.5 - dw / 2, min(0.9, 4.0 / height))])
            if pr:
                pygame.draw.polygon(s, self.fog((70, 46, 30), dist), pr[0])
                pygame.draw.polygon(s, self.fog((255, 220, 120), dist), pr[0], 2)

    def draw_stripes(self, s, b, pts, dist):
        """Hazard stripes and the big number on a bridge-site pylon."""
        p0, p1, _, p3 = pts
        for k in range(1, 5):
            v = k / 5
            a = self.cam.project(tuple(p0[i] + (p3[i] - p0[i]) * v for i in range(3)))
            c = self.cam.project(tuple(p1[i] + (p3[i] - p0[i]) * v for i in range(3)))
            if a and c:
                pygame.draw.line(s, self.fog((40, 40, 50), dist), a[:2], c[:2], max(1, int(400 / max(dist, 1))))

    def draw_tree(self, s, t, dist):
        x, z, h = t
        base = self.cam.project((x, 0.0, z))
        top = self.cam.project((x, h, z))
        if not base or not top:
            return
        scale = self.cam.focal / base[2]
        pygame.draw.line(s, self.fog((110, 76, 50), dist), base[:2], top[:2], max(1, int(0.5 * scale)))
        for k, (fy, fr, col) in enumerate(((0.55, 0.42, (58, 140, 70)), (0.8, 0.32, (76, 166, 84)))):
            c = self.cam.project((x, h * fy, z))
            if c:
                pygame.draw.circle(s, self.fog(col, dist), c[:2], max(2, int(h * fr * scale)))

    def draw_lamp(self, s, lp, dist):
        x, z = lp
        a = self.cam.project((x, 0.0, z))
        b = self.cam.project((x, 5.0, z))
        if a and b:
            pygame.draw.line(s, self.fog((60, 70, 86), dist), a[:2], b[:2], max(1, int(self.cam.focal * 0.18 / a[2])))
            pygame.draw.circle(s, self.fog((255, 236, 170), dist), b[:2], max(2, int(self.cam.focal * 0.4 / b[2])))

    def floor_under(self):
        px, _, pz = self.player.pos
        floor = 0.0
        for b in self.boxes:
            if b.contains_xz(px, pz) and b.h <= self.player.pos[1] + 0.1:
                floor = max(floor, b.h)
        return floor

    def draw_player(self, s):
        p = self.player
        cam = self.cam
        px, py, pz = p.pos
        sh = cam.project((px, self.floor_under() + 0.03, pz))
        if sh:
            r = max(3, int(cam.focal * 0.7 / sh[2]))
            shadow = pygame.Surface((2 * r, r), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
            s.blit(shadow, (sh[0] - r, sh[1] - r // 2))

        foot = cam.project((px, py, pz))
        if not foot:
            return

        exp = getattr(self, "exp", 0)
        tier = EngineerTier.get_tier(exp)
        sc = (cam.focal / foot[2]) * tier.get("scale", 1.0)

        def P(dx, dy, dz=0.0):
            hx, _, hz = p.heading
            rx, rz = hz, -hx
            q = cam.project((px + rx * dx + hx * dz, py + dy, pz + rz * dx + hz * dz))
            return q[:2] if q else foot[:2]

        swing = math.sin(p.walk_phase * 2.2) * (0.4 if p.grounded else 0.15)
        hip, neck, head = P(0, 0.95), P(0, 1.45), P(0, 1.70)
        lw = max(3, int(0.18 * sc))

        if p.gliding:
            pygame.draw.polygon(s, (140, 70, 210), [
                P(-0.25, 1.45, -0.1), P(0.25, 1.45, -0.1),
                P(0.9, 0.5, -0.8), P(-0.9, 0.5, -0.8)
            ])

        if tier.get("accessory") == "blueprint_tube":
            tube_top = P(-0.25, 1.75, -0.12)
            tube_bot = P(0.22, 1.05, -0.12)
            pygame.draw.line(s, (35, 40, 45), tube_top, tube_bot, max(4, int(0.14 * sc)))
            pygame.draw.circle(s, (220, 185, 45), tube_top, max(2, int(0.06 * sc)))

        pants_col = tier["pants_color"]
        boot_col = tier["boots_color"]
        l_foot = P(-0.16, 0.0, swing)
        r_foot = P(0.16, 0.0, -swing)
        pygame.draw.line(s, pants_col, hip, l_foot, lw)
        pygame.draw.line(s, pants_col, hip, r_foot, lw)
        pygame.draw.circle(s, boot_col, l_foot, max(3, int(0.11 * sc)))
        pygame.draw.circle(s, boot_col, r_foot, max(3, int(0.11 * sc)))

        torso_w = max(5, int(0.36 * sc))
        pygame.draw.line(s, tier["shirt_color"], hip, neck, torso_w)
        vest_w = max(4, int(0.34 * sc))
        mid_spine = P(0, 1.20)
        pygame.draw.line(s, tier["vest_color"], mid_spine, neck, vest_w)
        pygame.draw.line(s, (250, 250, 250), P(-0.16, 1.25), P(0.16, 1.25), max(2, int(0.06 * sc)))

        if tier.get("accessory") in ("toolbelt", "clipboard_goggles", "blueprint_tube"):
            pygame.draw.line(s, (45, 30, 15), P(-0.19, 0.96), P(0.19, 0.96), max(3, int(0.08 * sc)))
            pygame.draw.rect(s, (210, 190, 60), (hip[0] - 3, hip[1] - 3, 6, 6))

        shirt_col = tier["shirt_color"]
        if p.rope is not None:
            hand = P(0.1, 2.0)
            a = cam.project(p.rope[0])
            if a:
                pygame.draw.line(s, (255, 255, 255), hand, a[:2], 2)
                pygame.draw.circle(s, (255, 220, 60), a[:2], 5)
            pygame.draw.line(s, shirt_col, neck, hand, lw)
            pygame.draw.line(s, shirt_col, neck, P(-0.35, 1.0, 0.2), lw)
        elif p.zip is not None and len(p.zip) > 4:
            hand = P(0.1, 2.0)
            a = cam.project(p.zip[4])
            if a:
                pygame.draw.line(s, (255, 255, 255), hand, a[:2], 2)
                for k in range(6):
                    ang = k * 3.14159 / 3
                    pygame.draw.line(s, (255, 255, 255), a[:2],
                                     (a[0] + 9 * math.cos(ang), a[1] + 9 * math.sin(ang)), 1)
            pygame.draw.line(s, shirt_col, neck, hand, lw)
            pygame.draw.line(s, shirt_col, neck, P(-0.35, 1.0, 0.2), lw)
        elif p.zip is not None:
            pygame.draw.line(s, shirt_col, neck, P(-0.4, 1.9), lw)
            pygame.draw.line(s, shirt_col, neck, P(0.4, 1.9), lw)
        else:
            pygame.draw.line(s, shirt_col, neck, P(-0.32, 1.0, -swing), lw)
            pygame.draw.line(s, shirt_col, neck, P(0.32, 1.0, swing), lw)

        hr = max(3, int(0.20 * sc))
        pygame.draw.circle(s, (230, 185, 145), head, hr)
        helmet_col = tier["helmet_color"]
        pygame.draw.circle(s, helmet_col, (head[0], head[1] - hr * 0.35), int(hr * 1.08),
                           draw_top_right=True, draw_top_left=True)
        pygame.draw.line(s, helmet_col, (head[0] - hr * 1.35, head[1] - hr * 0.3),
                         (head[0] + hr * 1.35, head[1] - hr * 0.3), max(2, hr // 3))

        if p.splash > 0:
            for k in range(6):
                a = k / 6 * math.tau + self.t * 3
                q = P(math.cos(a) * 0.9, 0.3 + 0.8 * p.splash / 2.5, math.sin(a) * 0.9)
                pygame.draw.circle(s, (180, 220, 255), q, max(2, int(0.1 * sc)))
    def draw_anchor(self, s):
        if self.anchor is None or self.overlay() is not None:
            return
        a = self.cam.project(self.anchor)
        if not a:
            return
        r = 8 + 3 * math.sin(self.t * 8)
        pygame.draw.circle(s, (255, 255, 255), a[:2], int(r) + 3, 2)
        pygame.draw.circle(s, (255, 220, 60), a[:2], int(r))

    def place_labels(self):
        """Which name signs to show this frame: nearest first, and a sign that would overlap a
        nearer one is left out, so the view never turns into a pile of labels."""
        cam = self.cam
        cands = []
        for b in self.boxes:
            if b.kind is None:
                continue
            cx, _, cz = b.centre
            p = cam.project((cx, b.h + 2.5, cz))
            limit = 75 if b.kind == "level" else 230
            if not p or p[2] > limit or not (-60 < p[0] < WIDTH + 60):
                continue
            size = int(max(13, min(28, 1500 / p[2])))
            r = pygame.Rect(0, 0, measure(self.box_name(b), size, True)[0] + 22, size + 14)
            r.midbottom = (int(p[0]), int(p[1]))
            if r.top < 62:
                # a tall building's roof is above the screen: keep its sign just under the top bar
                base = cam.project((cx, b.y0, cz))
                if base is None or base[1] < 62 + r.h:
                    continue
                r.top = 62
            show_sub = p[2] < 60
            area = r.inflate(0, 2 * (size + 2)).move(0, size + 2) if show_sub else r
            cands.append((p[2], b, r, size, show_sub, area))
        cands.sort(key=lambda c: c[0])
        kept, taken = {}, []
        for depth, b, r, size, show_sub, area in cands:
            if area.top < 58 or any(area.colliderect(t) for t in taken):
                continue
            taken.append(area.inflate(8, 6))
            kept[b.key] = (r, size, show_sub, depth)
        return kept

    def draw_label(self, s, b, r, size, show_sub, depth):
        pill = pygame.Surface(r.size, pygame.SRCALPHA)
        pygame.draw.rect(pill, (20, 30, 50, 210), pill.get_rect(), border_radius=r.h // 2)
        pygame.draw.rect(pill, (*b.colour, 255), pill.get_rect(), 3, border_radius=r.h // 2)
        s.blit(pill, r.topleft)
        text(s, self.box_name(b), r.center, size, (255, 255, 255), bold=True, anchor="center", raw=True)
        if show_sub:
            sub = self.box_sub(b)
            ss = max(12, size - 6)
            sr = pygame.Rect(0, 0, measure(sub, ss, True)[0] + 16, ss + 8)
            sr.midtop = (r.centerx, r.bottom + 2)
            panel(s, sr, (20, 30, 50), None, sr.h // 2, alpha=170)
            text(s, sub, sr.center, ss, (255, 244, 210), bold=True, anchor="center", raw=True)
        if b.kind == "level" and not self.app.save.unlocked(b.payload):
            # a small padlock: this site opens after the one before it
            lk = pygame.Rect(r.right + 6, r.y + r.h // 2 - 2, size, size * 0.8)
            pygame.draw.arc(s, (255, 255, 255), (lk.x + lk.w * 0.2, lk.y - lk.h * 0.6, lk.w * 0.6, lk.h),
                            0, math.pi, 3)
            pygame.draw.rect(s, (230, 90, 70), lk, border_radius=3)

    def map_rect(self, b):
        x0, x1, z0, z1 = world.BOUNDS
        sx = MAP.w / (x1 - x0)
        sz = MAP.h / (z1 - z0)
        return pygame.Rect(MAP.x + (b.x0 - x0) * sx, MAP.bottom - (b.z1 - z0) * sz,
                           max(3, (b.x1 - b.x0) * sx), max(3, (b.z1 - b.z0) * sz))

    def map_point(self, x, z):
        x0, x1, z0, z1 = world.BOUNDS
        return (MAP.x + (x - x0) * MAP.w / (x1 - x0), MAP.bottom - (z - z0) * MAP.h / (z1 - z0))

    def draw_map(self, s):
        panel(s, MAP.inflate(8, 8), (22, 42, 72), (255, 255, 255), 10, alpha=210)
        pygame.draw.rect(s, (96, 160, 90), MAP)
        a = self.map_point(-6, world.BOUNDS[2])
        b = self.map_point(6, world.BOUNDS[3])
        pygame.draw.rect(s, AVENUE, pygame.Rect(a[0], b[1], b[0] - a[0], a[1] - b[1]))
        r0 = self.map_point(world.BOUNDS[0], world.RIVER_Z[1])
        r1 = self.map_point(world.BOUNDS[1], world.RIVER_Z[0])
        pygame.draw.rect(s, RIVER, pygame.Rect(r0[0], r0[1], r1[0] - r0[0], r1[1] - r0[1]))
        for bx in self.boxes:
            if bx.kind is None:
                continue
            r = self.map_rect(bx)
            pygame.draw.rect(s, bx.colour, r)
            if bx is self.target:
                pygame.draw.rect(s, (255, 255, 255), r.inflate(6, 6), 2)
        p = self.player
        c = self.map_point(p.pos[0], p.pos[2])
        hx, _, hz = p.heading
        tip = (c[0] + hx * 9, c[1] - hz * 9)
        left = (c[0] - hz * 5 - hx * 4, c[1] - hx * 5 + hz * 4)
        right = (c[0] + hz * 5 - hx * 4, c[1] + hx * 5 + hz * 4)
        pygame.draw.polygon(s, (255, 255, 255), [tip, left, right])
        pygame.draw.polygon(s, (220, 40, 40), [tip, left, right], 2)
        text(s, "N", (MAP.centerx, MAP.y + 2), 13, (255, 255, 255), bold=True, anchor="midtop", raw=True)

    def draw_hud(self, s):
        bar = pygame.Surface((WIDTH, 54), pygame.SRCALPHA)
        bar.fill((12, 24, 44, 170))
        s.blit(bar, (0, 0))
        text(s, w("title"), (WIDTH - 214, 27), 22, (255, 214, 120), bold=True, anchor="midright", raw=True)
        save = self.app.save
        text(s, w("wallet", g=economy.format_rs(save.wallet), x=save.exp), (WIDTH - 20, 296), 15,
             (255, 255, 255), bold=True, anchor="topright", raw=True)
        self.draw_map(s)
        # where you are heading
        if self.target is not None:
            p = self.player
            dx, _, dz = self.target.door()
            dist = math.hypot(dx - p.pos[0], dz - p.pos[2])
            ang = math.atan2(dx - p.pos[0], dz - p.pos[2]) - self.cam.yaw
            c = (WIDTH // 2, 74)
            label = w("to", n=self.box_name(self.target), d=int(dist))
            tw = measure(label, 18, True)[0]
            panel(s, pygame.Rect(c[0] - tw // 2 - 40, 58, tw + 80, 34), (20, 36, 64), (255, 220, 60), 17,
                  alpha=220)
            tip = (c[0] - tw // 2 - 22 + 11 * math.sin(ang), c[1] + 1 - 11 * math.cos(ang))
            base = (c[0] - tw // 2 - 22 - 7 * math.sin(ang), c[1] + 1 + 7 * math.cos(ang))
            pygame.draw.line(s, (255, 220, 60), base, tip, 4)
            pygame.draw.circle(s, (255, 220, 60), tip, 4)
            text(s, label, (c[0] + 10, c[1] + 1), 18, (255, 255, 255), bold=True, anchor="center", raw=True)
            self.zip_btn.visible = dist > 8 and self.player.zip is None
        else:
            self.zip_btn.visible = False
        self.widgets.draw(s)
        # the door you are standing at
        b = world.nearest_entrance(self.boxes, self.player.pos)
        for name, pad in self.pads.items():
            if (name == "enter" and b is None) or not pad.visible:
                continue
            pad.draw(s)
        if b is not None and self.overlay() is None:
            label = w("enter", n=self.box_name(b))
            tw = measure(label, 22, True)[0]
            r = pygame.Rect(0, 0, tw + 50, 50)
            r.midbottom = (WIDTH // 2, HEIGHT - 120)
            pulse = int(30 * (1 + math.sin(self.t * 6)))
            panel(s, r, (150 + pulse // 2, 60, 120), (255, 255, 255), 25, alpha=235)
            text(s, label, r.center, 22, (255, 255, 255), bold=True, anchor="center", raw=True)
        msg, ttl = self.toast
        if ttl > 0 and msg:
            tw = measure(msg, 18, True)[0]
            r = pygame.Rect(0, 0, min(WIDTH - 40, tw + 40), 44)
            r.midtop = (WIDTH // 2, 140)
            panel(s, r, (20, 36, 64), (90, 210, 240), 14, alpha=int(min(1.0, ttl) * 230))
            text(s, msg, r.center, 18, (255, 255, 255), bold=True, anchor="center", raw=True)
        if self.show_tips and self.overlay() is None:
            r = pygame.Rect(26, 70, 440, 380)
            panel(s, r, (20, 40, 70), (255, 196, 64), 16, alpha=235)
            text(s, w("tip_title"), (r.x + 20, r.y + 16), 24, (255, 214, 120), bold=True, raw=True)
            y = r.y + 60
            for key, col in (("tip1", (90, 210, 240)), ("tip2", (255, 220, 60)), ("tip3", (255, 150, 200)),
                             ("tip4", (140, 230, 140)), ("tip5", (255, 140, 60))):
                pygame.draw.circle(s, col, (r.x + 26, y + 11), 6)
                for line in wrap(w(key), r.w - 64, 16):
                    text(s, line, (r.x + 42, y), 16, (240, 245, 255), raw=True)
                    y += 24
                y += 8
            self.got_it.rect.topleft = (r.x + 20, r.bottom - 54)
            self.got_it.draw(s)
        ov = self.overlay()
        if ov is not None:
            ov.draw(s)
