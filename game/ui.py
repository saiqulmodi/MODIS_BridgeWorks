"""Shared look and simple widgets (Prompt 10): blueprint style, big touch-friendly targets."""
import math

import pygame

WIDTH, HEIGHT = 1280, 720
TOP_BAR = 44
BOTTOM_BAR = 58
DRAWER_W = 390

# Blueprint palette
BG = (14, 30, 54)
BG_DARK = (9, 20, 38)
GRID = (30, 58, 96)
GRID_MAJOR = (44, 80, 128)
LINE = (210, 228, 255)
TEXT = (230, 238, 250)
MUTED = (140, 160, 190)
ACCENT = (255, 196, 64)
PANEL = (22, 42, 72)
PANEL_EDGE = (70, 110, 165)
BUTTON = (34, 62, 104)
BUTTON_HOVER = (48, 86, 140)
BUTTON_ACTIVE = (232, 168, 40)
GOOD = (70, 210, 110)
WARN = (245, 200, 50)
BAD = (235, 70, 60)
CYAN = (90, 210, 240)
STATUS = {"green": GOOD, "yellow": WARN, "red": BAD, "failed": (255, 40, 40)}

_fonts = {}


def font(size=18, bold=False, mono=False):
    key = (size, bold, mono)
    if key not in _fonts:
        name = "consolas" if mono else "segoeui"
        _fonts[key] = pygame.font.SysFont(name, size, bold=bold)
    return _fonts[key]


def text(surface, s, pos, size=18, colour=TEXT, bold=False, mono=False, anchor="topleft"):
    img = font(size, bold, mono).render(str(s), True, colour)
    r = img.get_rect(**{anchor: pos})
    surface.blit(img, r)
    return r


def wrap(s, width, size=18, bold=False, mono=False):
    f = font(size, bold, mono)
    lines = []
    for para in str(s).split("\n"):
        words, cur = para.split(" "), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if f.size(trial)[0] <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(surface, s, pos, width, size=18, colour=TEXT, bold=False, mono=False, gap=2):
    x, y = pos
    for line in wrap(s, width, size, bold, mono):
        text(surface, line, (x, y), size, colour, bold, mono)
        y += font(size, bold, mono).get_linesize() + gap
    return y


def panel(surface, rect, colour=PANEL, edge=PANEL_EDGE, radius=10, alpha=None):
    rect = pygame.Rect(rect)
    if alpha is not None:
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(s, (*colour, alpha), s.get_rect(), border_radius=radius)
        surface.blit(s, rect.topleft)
    else:
        pygame.draw.rect(surface, colour, rect, border_radius=radius)
    if edge:
        pygame.draw.rect(surface, edge, rect, 1, border_radius=radius)
    return rect


def arrow(surface, colour, start, end, width=3, head=10):
    sx, sy = start
    ex, ey = end
    dx, dy = ex - sx, ey - sy
    L = math.hypot(dx, dy)
    if L < 2:
        return
    pygame.draw.line(surface, colour, start, end, width)
    ux, uy = dx / L, dy / L
    h = min(head, L * 0.6)
    left = (ex - ux * h - uy * h * 0.55, ey - uy * h + ux * h * 0.55)
    right = (ex - ux * h + uy * h * 0.55, ey - uy * h - ux * h * 0.55)
    pygame.draw.polygon(surface, colour, [end, left, right])


def blueprint_background(surface, rect=None, step=32):
    rect = pygame.Rect(rect or surface.get_rect())
    surface.fill(BG, rect)
    for i, x in enumerate(range(rect.left, rect.right, step)):
        pygame.draw.line(surface, GRID_MAJOR if i % 5 == 0 else GRID, (x, rect.top), (x, rect.bottom))
    for i, y in enumerate(range(rect.top, rect.bottom, step)):
        pygame.draw.line(surface, GRID_MAJOR if i % 5 == 0 else GRID, (rect.left, y), (rect.right, y))


class Widget:
    visible = True
    enabled = True

    def handle(self, event):
        return False

    def draw(self, surface):
        pass


class Button(Widget):
    def __init__(self, rect, label, on_click=None, toggle=False, active=False, hotkey=None,
                 tooltip="", size=17, colour=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.toggle = toggle
        self.active = active
        self.hotkey = hotkey
        self.tooltip = tooltip
        self.size = size
        self.colour = colour
        self.visible = True
        self.enabled = True
        self.hover = False

    def handle(self, event):
        if not (self.visible and self.enabled):
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.click()
            return True
        elif event.type == pygame.KEYDOWN and self.hotkey is not None and event.key == self.hotkey:
            self.click()
            return True
        return False

    def click(self):
        if self.toggle:
            self.active = not self.active
        if self.on_click:
            self.on_click()

    def draw(self, surface):
        if not self.visible:
            return
        if not self.enabled:
            col = (40, 50, 66)
        elif self.active:
            col = BUTTON_ACTIVE
        elif self.hover:
            col = BUTTON_HOVER
        else:
            col = self.colour or BUTTON
        pygame.draw.rect(surface, col, self.rect, border_radius=8)
        pygame.draw.rect(surface, PANEL_EDGE, self.rect, 1, border_radius=8)
        tc = (20, 20, 30) if self.active else (TEXT if self.enabled else MUTED)
        text(surface, self.label, self.rect.center, self.size, tc, bold=True, anchor="center")


class Slider(Widget):
    def __init__(self, rect, label, lo, hi, value, on_change=None, fmt="{:.2f}", step=None,
                 log=False):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.lo, self.hi = lo, hi
        self.value = value
        self.on_change = on_change
        self.fmt = fmt
        self.step = step
        self.log = log
        self.drag = False
        self.visible = True
        self.enabled = True

    @property
    def track(self):
        return pygame.Rect(self.rect.x, self.rect.y + 24, self.rect.w, 10)

    def _frac(self, v):
        if self.log:
            return (math.log(v) - math.log(self.lo)) / (math.log(self.hi) - math.log(self.lo))
        return (v - self.lo) / (self.hi - self.lo)

    def _value(self, f):
        f = min(1.0, max(0.0, f))
        if self.log:
            v = math.exp(math.log(self.lo) + f * (math.log(self.hi) - math.log(self.lo)))
        else:
            v = self.lo + f * (self.hi - self.lo)
        if self.step:
            v = round(v / self.step) * self.step
        return min(self.hi, max(self.lo, v))

    def set_from_x(self, x):
        v = self._value((x - self.track.x) / self.track.w)
        if v != self.value:
            self.value = v
            if self.on_change:
                self.on_change(v)

    def handle(self, event):
        if not (self.visible and self.enabled):
            return False
        hit = self.track.inflate(0, 20)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hit.collidepoint(event.pos):
            self.drag = True
            self.set_from_x(event.pos[0])
            return True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.drag:
            self.drag = False
            return True
        if event.type == pygame.MOUSEMOTION and self.drag:
            self.set_from_x(event.pos[0])
            return True
        return False

    def draw(self, surface):
        if not self.visible:
            return
        text(surface, f"{self.label}: {self.fmt.format(self.value)}", (self.rect.x, self.rect.y), 15,
             TEXT if self.enabled else MUTED)
        t = self.track
        pygame.draw.rect(surface, BG_DARK, t, border_radius=5)
        f = self._frac(self.value)
        pygame.draw.rect(surface, ACCENT if self.enabled else MUTED,
                         (t.x, t.y, int(t.w * f), t.h), border_radius=5)
        pygame.draw.circle(surface, LINE, (t.x + int(t.w * f), t.centery), 9)


class Cycler(Button):
    """A button that steps through a list of options."""

    def __init__(self, rect, prefix, options, index=0, on_change=None, size=16, hotkey=None):
        self.prefix = prefix
        self.options = list(options)
        self.index = index
        self.on_change = on_change
        super().__init__(rect, self._label(), self._next, size=size, hotkey=hotkey)

    def _label(self):
        return f"{self.prefix}{self.options[self.index]}" if self.options else self.prefix

    @property
    def value(self):
        return self.options[self.index]

    def set(self, value):
        if value in self.options:
            self.index = self.options.index(value)
            self.label = self._label()

    def _next(self):
        if not self.options:
            return
        self.index = (self.index + 1) % len(self.options)
        self.label = self._label()
        if self.on_change:
            self.on_change(self.value)


class WidgetGroup:
    def __init__(self):
        self.items = []

    def add(self, w):
        self.items.append(w)
        return w

    def clear(self):
        self.items = []

    def handle(self, event):
        for w in reversed(self.items):
            if w.visible and w.handle(event):
                return True
        return False

    def draw(self, surface):
        for w in self.items:
            w.draw(surface)
        # tooltips last so they sit on top
        for w in self.items:
            if isinstance(w, Button) and w.visible and w.hover and w.tooltip:
                tip = wrap(w.tooltip, 300, 14)
                h = 20 * len(tip) + 10
                x = min(w.rect.x, WIDTH - 320)
                y = w.rect.y - h - 6 if w.rect.y > 200 else w.rect.bottom + 6
                panel(surface, (x, y, 316, h), BG_DARK)
                for k, line in enumerate(tip):
                    text(surface, line, (x + 8, y + 5 + 20 * k), 14, TEXT)


def mini_chart(surface, rect, series, colours, title="", y_label="", limit=None, x_marker=None):
    """Small line chart. series: list of [(x, y)] lists."""
    rect = pygame.Rect(rect)
    panel(surface, rect, BG_DARK, PANEL_EDGE, 6)
    if title:
        text(surface, title, (rect.x + 8, rect.y + 4), 14, MUTED)
    pts_all = [p for s in series for p in s]
    if not pts_all:
        return
    x0 = min(p[0] for p in pts_all)
    x1 = max(p[0] for p in pts_all)
    y0 = min(0.0, min(p[1] for p in pts_all))
    y1 = max(p[1] for p in pts_all)
    if limit is not None:
        y1 = max(y1, limit * 1.1)
    if x1 - x0 < 1e-9:
        x1 = x0 + 1
    if y1 - y0 < 1e-9:
        y1 = y0 + 1
    inner = rect.inflate(-20, -30).move(4, 8)

    def to(p):
        return (inner.x + (p[0] - x0) / (x1 - x0) * inner.w,
                inner.bottom - (p[1] - y0) / (y1 - y0) * inner.h)
    if limit is not None:
        ly = to((x0, limit))[1]
        pygame.draw.line(surface, BAD, (inner.x, ly), (inner.right, ly), 1)
        text(surface, "limit", (inner.right - 30, ly - 16), 12, BAD)
    for s, c in zip(series, colours):
        if len(s) >= 2:
            pygame.draw.lines(surface, c, False, [to(p) for p in s], 2)
    if x_marker is not None:
        mx = to((x_marker, y0))[0]
        pygame.draw.line(surface, ACCENT, (mx, inner.y), (mx, inner.bottom), 1)
    if y_label:
        text(surface, y_label, (rect.right - 8, rect.y + 4), 12, MUTED, anchor="topright")
