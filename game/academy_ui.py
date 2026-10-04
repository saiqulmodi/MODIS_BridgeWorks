"""BridgeWorks Academy: the multiple-choice question card, and the Black Box challenge.

A QuizCard shows one question in the current language with four options (shuffled each
time, keys 1-4 or a click). After an answer it shows right/wrong and the explanation; if the
student stays on the explanation for its reading time, a reading bonus is paid once.
"""
import random

import pygame

from engine import economy
from engine.academy_data import READING_BONUS

from . import i18n, sound
from .help_screen import _wrap
from .ui import (ACCENT, BAD, BG_DARK, BUTTON, BUTTON_HOVER, CYAN, GOOD, MUTED, PANEL, PANEL_EDGE,
                 TEXT, WARN, Button, WidgetGroup, font_for, panel)

rs = economy.format_rs

WORDS = {
    "right": ("Correct!", "সঠিক!"),
    "wrong": ("Not quite.", "পুরোপুরি ঠিক হয়নি।"),
    "answer": ("Answer: {a}", "উত্তর: {a}"),
    "grant": ("+{g} Civil Grant", "+{g} সিভিল অনুদান"),
    "practice": ("Already answered before - practice only, no grant.",
                 "আগেই উত্তর দেওয়া - শুধু অনুশীলন, অনুদান নেই।"),
    "reading": ("Keep reading: +{g} reading bonus in {s} s", "পড়তে থাকো: {s} সেকেন্ডে +{g} পড়ার বোনাস"),
    "read_paid": ("Reading bonus +{g} paid. Well read!", "পড়ার বোনাস +{g} দেওয়া হয়েছে। ভালো পড়েছ!"),
    "read_done": ("Explanation read.", "ব্যাখ্যা পড়া হয়েছে।"),
    "keys": ("Press 1-4 or click an answer.", "1-4 চাপো বা একটি উত্তরে ক্লিক করো।"),
}


def word(key, **kw):
    en, bn = WORDS[key]
    return (bn if i18n.lang() == "bn" else en).format(**kw)


def reading_seconds(text):
    """Time a young reader needs: about 3 words a second, at least 4 seconds."""
    return max(4.0, len(text.split()) / 3.0)


class QuizCard:
    def __init__(self, save, record, rect, on_answer=None):
        self.save = save
        self.r = record
        self.rect = pygame.Rect(rect)
        self.on_answer = on_answer
        self.order = list(range(4))
        random.shuffle(self.order)
        self.chosen = None             # original option index picked
        self.paid = 0.0
        self.first_try = str(record["id"]) not in save.academy["answered"]
        self.read_t = 0.0
        self.read_paid = 0.0
        self.boxes = []
        self.hover = None

    @property
    def answered(self):
        return self.chosen is not None

    @property
    def correct(self):
        return self.chosen == self.r["correct_idx"]

    def _t(self, key):
        bn = i18n.lang() == "bn"
        return self.r[key + "_bn"] if bn else self.r[key]

    def choose(self, original_idx):
        if self.answered:
            return
        self.chosen = original_idx
        self.paid = self.save.answer_question(self.r["id"], self.correct, self.r["grant_reward"])
        sound.play("kaching" if self.correct else "click")
        if self.on_answer:
            self.on_answer(self.correct, self.paid)

    def handle(self, event):
        if event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_4 and not self.answered:
            self.choose(self.order[event.key - pygame.K_1])
            return True
        if event.type == pygame.MOUSEMOTION:
            self.hover = next((k for k, b in enumerate(self.boxes) if b.collidepoint(event.pos)), None)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.answered:
            for k, b in enumerate(self.boxes):
                if b.collidepoint(event.pos):
                    self.choose(self.order[k])
                    return True
        return False

    def update(self, dt):
        if not self.answered or self.read_paid or str(self.r["id"]) in self._explained():
            return
        self.read_t += dt
        if self.read_t >= reading_seconds(self._t("explanation")):
            self.read_paid = self.save.explanation_read(self.r["id"], READING_BONUS)
            if self.read_paid:
                sound.play("kaching")

    def _explained(self):
        return {str(q) for q in self.save.academy["explained"]}

    def draw(self, surface):
        r = self.rect
        x, y, w = r.x, r.y, r.w
        q = self._t("question")
        fq = font_for(q, 21, True)
        for line in _wrap(fq, q, w):
            surface.blit(fq.render(line, True, TEXT), (x, y))
            y += fq.get_linesize()
        y += 12
        opts = self._t("options")
        self.boxes = []
        for k, oi in enumerate(self.order):
            s = opts[oi]
            fo = font_for(s, 17)
            lines = _wrap(fo, s, w - 64)
            h = max(44, len(lines) * fo.get_linesize() + 16)
            box = pygame.Rect(x, y, w, h)
            self.boxes.append(box)
            if self.answered and oi == self.r["correct_idx"]:
                col, edge = (34, 96, 60), GOOD
            elif self.answered and oi == self.chosen:
                col, edge = (100, 40, 40), BAD
            else:
                col = BUTTON_HOVER if (self.hover == k and not self.answered) else BUTTON
                edge = PANEL_EDGE
            pygame.draw.rect(surface, col, box, border_radius=8)
            pygame.draw.rect(surface, edge, box, 2 if edge != PANEL_EDGE else 1, border_radius=8)
            fk = font_for("1", 18, True)
            surface.blit(fk.render(str(k + 1), True, ACCENT), (x + 16, y + (h - fk.get_linesize()) // 2))
            ly = y + (h - len(lines) * fo.get_linesize()) // 2
            for line in lines:
                surface.blit(fo.render(line, True, TEXT), (x + 48, ly))
                ly += fo.get_linesize()
            y += h + 8
        y += 6
        if not self.answered:
            s = word("keys")
            surface.blit(font_for(s, 14).render(s, True, MUTED), (x, y))
            return
        head = word("right") if self.correct else word("wrong")
        if self.paid:
            head += "   " + word("grant", g=rs(self.paid))
        fh = font_for(head, 19, True)
        surface.blit(fh.render(head, True, GOOD if self.correct else WARN), (x, y))
        y += fh.get_linesize() + 2
        if not self.first_try:
            s = word("practice")
            surface.blit(font_for(s, 14).render(s, True, MUTED), (x, y))
            y += 20
        ex = self._t("explanation")
        fe = font_for(ex, 16)
        for line in _wrap(fe, ex, w):
            surface.blit(fe.render(line, True, CYAN), (x, y))
            y += fe.get_linesize()
        y += 6
        if self.read_paid:
            s = word("read_paid", g=rs(self.read_paid))
        elif str(self.r["id"]) in self._explained():
            s = word("read_done")
        else:
            left = max(0, int(reading_seconds(ex) - self.read_t + 0.99))
            s = word("reading", g=rs(READING_BONUS), s=left)
        surface.blit(font_for(s, 14, True).render(s, True, ACCENT), (x, y))


# --- Black Box: answer one Academy question to raise salvage from 30% to 75% ---------------------
CHALLENGE = {
    "title": ("ACADEMY CHALLENGE: answer correctly to recover 75% instead of 30%",
              "একাডেমি চ্যালেঞ্জ: সঠিক উত্তরে 30%-এর বদলে 75% ফেরত"),
    "won": ("Salvage raised to 75%: {s}. Press 'Back to the Black Box'.",
            "উদ্ধার-মূল্য বেড়ে 75%: {s}। 'ব্ল্যাক বক্সে ফেরো' চাপো।"),
    "lost": ("Salvage stays at 30%. Read the explanation - the next failure brings a new question.",
             "উদ্ধার-মূল্য 30%-ই থাকল। ব্যাখ্যাটি পড়ো - পরের ব্যর্থতায় নতুন প্রশ্ন আসবে।"),
    "back": ("Back to the Black Box", "ব্ল্যাক বক্সে ফেরো"),
}


def challenge_word(key, **kw):
    en, bn = CHALLENGE[key]
    return (bn if i18n.lang() == "bn" else en).format(**kw)


def pick_question(save, rng=random):
    """A question from the student's class (unanswered first), else from any written class."""
    from engine.academy import CLASSES, SUBJECTS
    from engine.academy_data import items
    answered = save.academy["answered"]
    cls = save.academy["class"]
    order = [cls] + sorted((c for c in CLASSES if c != cls), key=lambda c: abs(c - cls))
    for c in order:
        pool = [r for s in SUBJECTS for r in items(c, s)]
        if pool:
            fresh = [r for r in pool if str(r["id"]) not in answered]
            return rng.choice(fresh or pool)
    return None


class AcademyChallenge:
    blocks_world = True

    def __init__(self, scene, blackbox, record):
        from .ui import HEIGHT, WIDTH
        self.scene = scene
        self.blackbox = blackbox
        self.rect = pygame.Rect(140, 60, WIDTH - 280, HEIGHT - 110)
        r = self.rect
        self.card = QuizCard(scene.app.save, record, (r.x + 24, r.y + 60, r.w - 48, r.h - 130),
                             self._answered)
        self.widgets = WidgetGroup()
        self.back_btn = self.widgets.add(Button((r.right - 284, r.bottom - 58, 260, 42), "", self.back,
                                                size=16, hotkey=pygame.K_ESCAPE))
        self.back_btn.visible = False

    def _answered(self, correct, paid):
        self.blackbox.report.academy_bonus = correct
        self.blackbox.challenge_done = True
        self.back_btn.visible = True

    def back(self):
        self.scene.overlay = self.blackbox

    def handle(self, event):
        if self.widgets.handle(event) or self.card.handle(event):
            return True
        return event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)

    def update(self, dt):
        self.back_btn.label = challenge_word("back")
        self.card.update(dt)

    def draw(self, surface):
        from .ui import HEIGHT, WIDTH
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 170))
        surface.blit(veil, (0, 0))
        r = panel(surface, self.rect, PANEL, ACCENT, 14)
        t = challenge_word("title")
        surface.blit(font_for(t, 18, True).render(t, True, ACCENT), (r.x + 24, r.y + 18))
        self.card.draw(surface)
        if self.card.answered:
            rep = self.blackbox.report
            s = (challenge_word("won", s=rs(rep.salvage)) if rep.academy_bonus else challenge_word("lost"))
            surface.blit(font_for(s, 15, True).render(s, True, GOOD if rep.academy_bonus else WARN),
                         (r.x + 24, r.bottom - 50))
        self.widgets.draw(surface)
