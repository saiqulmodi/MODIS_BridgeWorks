"""The Help screen: the new-player guide and 200 questions & answers, English or Bengali.

Opened with H or the '?' button inside a level, and with H or the Help button on the menu.
Inside a level it opens on that level's walkthrough. Scroll with the mouse wheel, the arrow
keys, Page Up / Page Down or the scrollbar; type to search both languages at once.
"""
import re

import pygame

from . import i18n, sound
from .guide import SECTIONS, level_walkthrough
from .ui import (ACCENT, BG_DARK, CYAN, HEIGHT, LINE, MUTED, PANEL, PANEL_EDGE, TEXT, WIDTH,
                 Button, WidgetGroup, font_for, panel)

# Fixed words of the Help screen itself: (English, Bengali)
UI = {
    "title": ("Help: how to play and build", "সাহায্য: কীভাবে খেলবে আর বানাবে"),
    "sub": ("A guide for new players and 200 questions & answers, with the game's real numbers.",
            "নতুন খেলোয়াড়ের জন্য নির্দেশিকা আর 200টি প্রশ্নোত্তর, খেলার আসল সংখ্যা দিয়ে।"),
    "close": ("Close (Esc)", "বন্ধ করো (Esc)"),
    "lang": ("বাংলা (F2)", "English (F2)"),
    "level": ("This level: walkthrough", "এই লেভেল: পথনির্দেশ"),
    "search": ("Search:", "খোঁজো:"),
    "type": ("type a word or a number", "একটি শব্দ বা সংখ্যা লেখো"),
    "found": ("{n} answers for '{q}'", "'{q}'-এর জন্য {n}টি উত্তর"),
    "none": ("Nothing found for '{q}'. Try a shorter word.",
             "'{q}'-এর জন্য কিছু পাওয়া যায়নি। ছোট শব্দ চেষ্টা করো।"),
    "keys": ("Mouse wheel, arrow keys or Page Up / Down to scroll. Type to search, Backspace to "
             "delete, Esc to clear the search or close.",
             "স্ক্রল করতে মাউসের চাকা, তীর-চাবি বা Page Up / Down। খুঁজতে লেখো, মুছতে Backspace, "
             "খোঁজা মুছতে বা বন্ধ করতে Esc।"),
}

# Remembered while the game runs, so Help reopens where you left it
STATE = {"section": 0, "scroll": 0, "query": ""}

CAPTURE = (pygame.KEYDOWN, pygame.KEYUP, pygame.TEXTINPUT, pygame.MOUSEWHEEL)


def ui(key):
    en, bn = UI[key]
    return bn if i18n.lang() == "bn" else en


def _wrap(f, s, width):
    lines = []
    for para in s.split("\n"):
        cur = ""
        for w in para.split(" "):
            trial = (cur + " " + w).strip()
            if f.size(trial)[0] <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


class HelpOverlay:
    blocks_world = True

    def __init__(self, app, on_close, level_num=None):
        self.app = app
        self.on_close = on_close
        self.level_num = level_num
        self.rect = pygame.Rect(24, 50, WIDTH - 48, HEIGHT - 64)
        r = self.rect
        self.content = pygame.Rect(r.x + 336, r.y + 78, r.right - 30 - (r.x + 336), r.bottom - 16 - (r.y + 78))
        self.track = pygame.Rect(self.content.right + 8, self.content.y, 8, self.content.h)
        self.search_rect = pygame.Rect(r.x + 16, 0, 300, 40)
        self.widgets = WidgetGroup()
        self.widgets.add(Button((r.right - 180, r.y + 14, 164, 36), "", self.close, size=15))
        self.widgets.add(Button((r.right - 344, r.y + 14, 156, 36), "", self.toggle_language, size=15))
        self.section_btns = []
        y = r.y + 78
        for k in range(len(SECTIONS)):
            b = self.widgets.add(Button((r.x + 16, y, 300, 44), "", lambda k=k: self.show_section(k),
                                        toggle=False, size=15))
            self.section_btns.append(b)
            y += 50
        self.level_btn = None
        if level_num:
            self.level_btn = self.widgets.add(Button((r.x + 16, y, 300, 44), "", self.show_walkthrough,
                                                     size=15, colour=(40, 90, 70)))
            y += 50
        self.search_rect.y = y + 10
        self.layout = []
        self.total_h = 0
        self.anchors = {}
        self.highlight = None
        self.drag = False
        self._key = None
        self.section = STATE["section"]
        self.query = STATE["query"]
        self.scroll = STATE["scroll"]
        if level_num:
            self.show_walkthrough(play=False)
        try:
            pygame.key.start_text_input()
            pygame.key.set_text_input_rect(self.search_rect)
        except (AttributeError, pygame.error):
            pass
        self._labels()

    # --- actions ---------------------------------------------------------------------------
    def close(self):
        STATE.update(section=self.section, scroll=self.scroll, query=self.query)
        sound.play("click")
        self.on_close()

    def toggle_language(self):
        self.app.toggle_language()
        self._labels()

    def show_section(self, k):
        sound.play("click")
        self.section, self.query, self.scroll, self.highlight = k, "", 0, None

    def show_walkthrough(self, play=True):
        if play:
            sound.play("click")
        s, k = level_walkthrough(self.level_num)
        self.section, self.query, self.highlight = s, "", (s, k)
        self._build()
        self.scroll = max(0, self.anchors.get((s, k), 0) - 8)

    # --- layout ------------------------------------------------------------------------------
    def _labels(self):
        lang = i18n.lang()
        self.widgets.items[0].label = ui("close")
        self.widgets.items[1].label = ui("lang")
        for k, (b, sec) in enumerate(zip(self.section_btns, SECTIONS)):
            b.label = sec.title(lang)
        if self.level_btn:
            self.level_btn.label = ui("level")

    def matches(self):
        """(section index, item index) of every answer to show."""
        q = self.query.strip().lower()
        if not q:
            sec = SECTIONS[self.section]
            return [(self.section, k) for k in range(len(sec.items))]
        num = re.fullmatch(r"(?:q|প্রশ্ন)?\s*(\d{1,3})", q)
        out = []
        if num:
            n = int(num.group(1))
            for s, sec in enumerate(SECTIONS):
                if sec.first and sec.first <= n < sec.first + len(sec.items):
                    out.append((s, n - sec.first))
        for s, sec in enumerate(SECTIONS):
            for k, it in enumerate(sec.items):
                if (s, k) in out:
                    continue
                blob = " ".join((it.q_en, it.a_en, it.q_bn, it.a_bn)).lower()
                if q in blob:
                    out.append((s, k))
        return out

    def _build(self):
        lang = i18n.lang()
        key = (lang, self.section, self.query)
        if key == self._key:
            return
        self._key = key
        w = self.content.w - 16
        rows, y, anchors = [], 0, {}
        hits = self.matches()
        if self.query.strip():
            msg = ui("found" if hits else "none").format(n=len(hits), q=self.query.strip())
            f = font_for(msg, 16, True)
            rows.append((y, f, msg, ACCENT, 0))
            y += f.get_linesize() + 12
        last_sec = None
        for s, k in hits:
            sec = SECTIONS[s]
            it = sec.items[k]
            if self.query.strip() and s != last_sec:
                title = sec.title(lang)
                f = font_for(title, 14, True)
                rows.append((y, f, title.upper() if lang == "en" else title, MUTED, 0))
                y += f.get_linesize() + 4
                last_sec = s
            anchors[(s, k)] = y
            tag = sec.tag(k, lang)
            ft = font_for(tag, 16, True)
            tag_w = max(ft.size(tag)[0] + 12, 74)
            rows.append((y, ft, tag, ACCENT, 0))
            q = it.q(lang)
            fq = font_for(q, 18, True)
            for line in _wrap(fq, q, w - tag_w):
                rows.append((y, fq, line, CYAN, tag_w))
                y += fq.get_linesize()
            y += 4
            a = it.a(lang)
            fa = font_for(a, 16)
            for line in _wrap(fa, a, w - tag_w):
                rows.append((y, fa, line, TEXT, tag_w))
                y += fa.get_linesize() + 1
            y += 18
            rows.append((y - 10, None, "", PANEL_EDGE, 0))       # separator
        self.layout = [[ry, f, s, c, x, None] for ry, f, s, c, x in rows]
        self.total_h = y
        self.anchors = anchors

    @property
    def max_scroll(self):
        return max(0, self.total_h - self.content.h)

    def _clamp(self):
        self.scroll = max(0, min(self.scroll, self.max_scroll))

    def _thumb(self):
        if self.total_h <= self.content.h:
            return None
        h = max(30, self.track.h * self.content.h / self.total_h)
        y = self.track.y + (self.track.h - h) * self.scroll / max(1, self.max_scroll)
        return pygame.Rect(self.track.x - 2, y, self.track.w + 4, h)

    def _scroll_to_mouse(self, my):
        f = (my - self.track.y) / max(1, self.track.h)
        self.scroll = f * self.max_scroll
        self._clamp()

    # --- events --------------------------------------------------------------------------------
    def handle(self, event):
        self._build()
        if self.widgets.handle(event):
            return True
        page = self.content.h - 40
        if event.type == pygame.MOUSEWHEEL:
            self.scroll -= event.y * 60
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hit = self.track.inflate(16, 0)
            if hit.collidepoint(event.pos):
                self.drag = True
                self._scroll_to_mouse(event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.drag = False
        elif event.type == pygame.MOUSEMOTION and self.drag:
            self._scroll_to_mouse(event.pos[1])
        elif event.type == pygame.TEXTINPUT:
            ch = "".join(c for c in event.text if c.isprintable())
            if ch and len(self.query) < 40:
                self.query += ch
                self.scroll, self.highlight = 0, None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.query:
                    self.query, self.scroll = "", 0
                else:
                    self.close()
                    return True
            elif event.key == pygame.K_F2:
                self.toggle_language()
            elif event.key == pygame.K_BACKSPACE:
                self.query = self.query[:-1]
                self.scroll = 0
            elif event.key == pygame.K_UP:
                self.scroll -= 40
            elif event.key == pygame.K_DOWN:
                self.scroll += 40
            elif event.key == pygame.K_PAGEUP:
                self.scroll -= page
            elif event.key == pygame.K_PAGEDOWN:
                self.scroll += page
            elif event.key == pygame.K_HOME:
                self.scroll = 0
            elif event.key == pygame.K_END:
                self.scroll = self.max_scroll
        self._build()
        self._clamp()
        return True

    def update(self, dt):
        pass

    # --- drawing -------------------------------------------------------------------------------
    def draw(self, surface):
        self._build()
        self._clamp()
        lang = i18n.lang()
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 170))
        surface.blit(veil, (0, 0))
        r = panel(surface, self.rect, PANEL, ACCENT, 14)
        title, sub = ui("title"), ui("sub")
        surface.blit(font_for(title, 26, True).render(title, True, TEXT), (r.x + 20, r.y + 10))
        surface.blit(font_for(sub, 15).render(sub, True, MUTED), (r.x + 22, r.y + 48))
        for k, b in enumerate(self.section_btns):
            b.active = not self.query.strip() and k == self.section
        # search box
        sr = self.search_rect
        pygame.draw.rect(surface, BG_DARK, sr, border_radius=8)
        pygame.draw.rect(surface, ACCENT if self.query else PANEL_EDGE, sr, 1, border_radius=8)
        label = ui("search")
        fl = font_for(label, 15, True)
        surface.blit(fl.render(label, True, ACCENT), (sr.x + 10, sr.y + (sr.h - fl.get_linesize()) // 2))
        x = sr.x + 16 + fl.size(label)[0]
        shown = self.query if self.query else ui("type")
        fs = font_for(shown, 15)
        while fs.size(shown)[0] > sr.right - x - 14 and len(shown) > 1:
            shown = shown[1:]
        surface.blit(fs.render(shown, True, TEXT if self.query else MUTED),
                     (x, sr.y + (sr.h - fs.get_linesize()) // 2))
        if self.query and (pygame.time.get_ticks() // 500) % 2 == 0:
            cx = x + fs.size(shown)[0] + 2
            pygame.draw.line(surface, ACCENT, (cx, sr.y + 9), (cx, sr.bottom - 9), 2)
        # key help under the search box
        keys = ui("keys")
        fk = font_for(keys, 13)
        ky = sr.bottom + 12
        for line in _wrap(fk, keys, sr.w):
            surface.blit(fk.render(line, True, MUTED), (sr.x + 2, ky))
            ky += fk.get_linesize()
        # content
        c = self.content
        pygame.draw.rect(surface, BG_DARK, c.inflate(12, 8), border_radius=10)
        surface.set_clip(c)
        if self.highlight in self.anchors:
            hy = c.y + self.anchors[self.highlight] - self.scroll - 6
            nxt = [y for key, y in self.anchors.items() if y > self.anchors[self.highlight]]
            hb = (min(nxt) if nxt else self.total_h) - self.anchors[self.highlight] - 4
            pygame.draw.rect(surface, (34, 66, 60), (c.x - 4, hy, c.w + 8, hb), border_radius=8)
        for row in self.layout:
            y, f, s, col, x, img = row
            sy = c.y + y - self.scroll
            if sy > c.bottom or sy < c.y - 40:
                continue
            if f is None:
                pygame.draw.line(surface, col, (c.x, sy), (c.right - 8, sy), 1)
                continue
            if img is None:
                img = row[5] = f.render(s, True, col)
            surface.blit(img, (c.x + x, sy))
        surface.set_clip(None)
        thumb = self._thumb()
        if thumb:
            pygame.draw.rect(surface, PANEL_EDGE, self.track, border_radius=4)
            pygame.draw.rect(surface, ACCENT if self.drag else LINE, thumb, border_radius=4)
        self.widgets.draw(surface)
