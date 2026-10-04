"""BridgeWorks Academy: pick a class and a subject (or the Daily 5), answer multiple-choice
questions and earn Civil Grants that pay for bridges instead of loans."""
import random

import pygame

from engine import economy
from engine.academy import CLASSES, SUBJECTS
from engine.academy_data import TARGET_PER_SUBJECT, items
from engine.academy_pass import has_access

from .. import i18n, sound
from ..academy_ui import QuizCard
from ..ui import (ACCENT, BG_DARK, CYAN, GOOD, HEIGHT, MUTED, PANEL, PANEL_EDGE, TEXT, WARN, WIDTH,
                  Button, WidgetGroup, blueprint_background, font_for, panel)
from ..help_screen import _wrap

rs = economy.format_rs

NAMES = {
    "physics": ("Physics", "পদার্থবিজ্ঞান"), "chemistry": ("Chemistry", "রসায়ন"),
    "math": ("Math", "গণিত"), "biology": ("Biology", "জীববিজ্ঞান"),
    "finance": ("Finance", "অর্থসংস্থান"), "commercials": ("Commercials", "বাণিজ্য"),
    "skills": ("Game skills (Help quiz)", "খেলার দক্ষতা (সাহায্য-কুইজ)"),
    "daily": ("Daily 5 (mixed)", "দৈনিক 5 (মিশ্র)"),
}
WORDS = {
    "title": ("BridgeWorks Academy", "ব্রিজওয়ার্কস একাডেমি"),
    "sub": ("Answer right on the first try to earn Civil Grants - free money for your bridges, "
            "used before any loan.",
            "প্রথম চেষ্টায় সঠিক উত্তরে সিভিল অনুদান পাও - তোমার সেতুর জন্য বিনামূল্যের টাকা, যেকোনো "
            "ঋণের আগে ব্যবহার হয়।"),
    "wallet": ("Civil Grants: {w}   (earned so far {e})", "সিভিল অনুদান: {w}   (এ পর্যন্ত অর্জিত {e})"),
    "class": ("Class", "শ্রেণি"),
    "subject": ("Subject", "বিষয়"),
    "menu": ("Menu (Esc)", "মেনু (Esc)"),
    "lang": ("বাংলা (F2)", "English (F2)"),
    "next": ("Next question (Enter)", "পরের প্রশ্ন (Enter)"),
    "give": ("Donation Camps", "দান-শিবির"),
    "reward": ("Class {c}: {g} for a right first answer, +{b} for reading the explanation.",
               "শ্রেণি {c}: প্রথম চেষ্টায় সঠিক উত্তরে {g}, ব্যাখ্যা পড়লে আরও {b}।"),
    "count": ("{a} of {n} answered", "{n}টির মধ্যে {a}টির উত্তর দেওয়া"),
    "empty": ("Class {c} {s} is still being written ({n} of 100 ready). Pick another subject or "
              "class.", "শ্রেণি {c} {s} এখনো লেখা হচ্ছে (100-এর মধ্যে {n}টি তৈরি)। অন্য বিষয় বা শ্রেণি বাছো।"),
    "done": ("Every question here is answered. Great work! Pick another subject - or keep "
             "practising (no new grants).", "এখানের সব প্রশ্নের উত্তর দেওয়া হয়েছে। দারুণ! অন্য বিষয় বাছো - "
             "অথবা অনুশীলন চালিয়ে যাও (নতুন অনুদান নেই)।"),
    "daily_left": ("Daily 5: question {k} of {n}", "দৈনিক 5: {n}টির মধ্যে {k} নম্বর প্রশ্ন"),
    "daily_end": ("Daily 5 finished: {r} of {n} right, {g} earned. Come back tomorrow!",
                  "দৈনিক 5 শেষ: {n}টির মধ্যে {r}টি সঠিক, {g} অর্জিত। কাল আবার এসো!"),
    "free": ("Scholarship Pass: free during the preview - every class is open.",
             "স্কলারশিপ পাস: প্রিভিউর সময় বিনামূল্যে - সব শ্রেণি খোলা।"),
    "locked": ("This class needs the Scholarship Pass.", "এই শ্রেণির জন্য স্কলারশিপ পাস লাগবে।"),
}


def w(key, **kw):
    en, bn = WORDS[key]
    return (bn if i18n.lang() == "bn" else en).format(**kw)


def name(key):
    en, bn = NAMES[key]
    return bn if i18n.lang() == "bn" else en


def skill_items():
    from engine.academy_skills import items as skills
    return skills()


class AcademyScene:
    def __init__(self, app):
        self.app = app
        self.save = app.save
        self.widgets = WidgetGroup()
        self.cls = self.save.academy["class"]
        self.subject = "physics"
        self.card = None
        self.daily = None             # list of records while a Daily 5 runs
        self.daily_k = 0
        self.daily_right = 0
        self.daily_paid = 0.0
        self.message = ""
        self.menu_btn = self.widgets.add(Button((WIDTH - 184, 16, 168, 36), "", app.to_menu, size=15,
                                                hotkey=pygame.K_ESCAPE))
        self.lang_btn = self.widgets.add(Button((WIDTH - 360, 16, 168, 36), "", app.toggle_language,
                                                size=15, hotkey=pygame.K_F2))
        self.class_btns = {}
        for k, c in enumerate(CLASSES):
            b = self.widgets.add(Button((24 + (k % 4) * 76, 142 + (k // 4) * 42, 70, 36), str(c),
                                        lambda c=c: self.pick_class(c), size=16))
            self.class_btns[c] = b
        self.subject_btns = {}
        y = 292
        for key in SUBJECTS + ("skills", "daily"):
            b = self.widgets.add(Button((24, y, 300, 40), "", lambda key=key: self.pick_subject(key),
                                        size=15))
            self.subject_btns[key] = b
            y += 46
        self.give_btn = self.widgets.add(Button((WIDTH - 536, 16, 168, 36), "", app.to_donations, size=15))
        self.next_btn = self.widgets.add(Button((WIDTH - 300, HEIGHT - 62, 280, 44), "", self.next_question,
                                                size=16, colour=(40, 110, 70), hotkey=pygame.K_RETURN))
        self.next_question()

    # --- choosing what to study ---------------------------------------------------------------
    def pick_class(self, c):
        sound.play("click")
        self.cls = c
        self.save.academy["class"] = c
        self.save.write()
        self.daily = None
        self.next_question()

    def pick_subject(self, key):
        sound.play("click")
        self.subject = key
        self.daily = None
        if key == "daily":
            self.start_daily()
        else:
            self.next_question()

    def pool(self, subject=None):
        subject = subject or self.subject
        if subject == "skills":
            return skill_items()
        return items(self.cls, subject)

    def start_daily(self, rng=random):
        answered = self.save.academy["answered"]
        pool = [r for s in SUBJECTS for r in items(self.cls, s) if str(r["id"]) not in answered]
        if len(pool) < 5:
            pool += [r for r in skill_items() if str(r["id"]) not in answered]
        self.daily = rng.sample(pool, min(5, len(pool)))
        self.daily_k, self.daily_right, self.daily_paid = 0, 0, 0.0
        self.message = ""
        self._show(self.daily[0] if self.daily else None)

    def next_question(self):
        self.message = ""
        if self.daily is not None:
            self.daily_k += 1
            if self.daily_k < len(self.daily):
                self._show(self.daily[self.daily_k])
            else:
                self.card = None
                self.message = w("daily_end", r=self.daily_right, n=len(self.daily), g=rs(self.daily_paid))
            return
        if self.subject != "skills" and not has_access(self.save, self.cls):
            self.card, self.message = None, w("locked")
            return
        pool = self.pool()
        if not pool:
            self.card = None
            self.message = w("empty", c=self.cls, s=name(self.subject), n=0)
            return
        answered = self.save.academy["answered"]
        current = self.card.r["id"] if self.card else None
        fresh = [r for r in pool if str(r["id"]) not in answered and r["id"] != current]
        if fresh:
            self._show(fresh[0])                 # in order: the bank goes from easy to harder
            return
        self.message = w("done")
        self._show(random.choice([r for r in pool if r["id"] != current] or pool))

    def _show(self, record):
        if record is None:
            self.card = None
            return
        self.card = QuizCard(self.save, record, (360, 120, WIDTH - 384, HEIGHT - 200), self._answered)

    def _answered(self, correct, paid):
        if self.daily is not None:
            self.daily_right += int(correct)
            self.daily_paid += paid

    # --- loop ---------------------------------------------------------------------------------
    def handle(self, event):
        if self.widgets.handle(event):
            return
        if self.card is not None:
            self.card.handle(event)

    def update(self, dt):
        if self.card is not None:
            before = self.save.wallet
            self.card.update(dt)
            if self.daily is not None and self.save.wallet > before:
                self.daily_paid += self.save.wallet - before
        self.menu_btn.label = w("menu")
        self.lang_btn.label = w("lang")
        self.next_btn.label = w("next")
        self.give_btn.label = w("give")
        self.next_btn.enabled = self.card is None or self.card.answered
        for c, b in self.class_btns.items():
            b.active = c == self.cls
        answered = self.save.academy["answered"]
        for key, b in self.subject_btns.items():
            b.active = (key == "daily") if self.daily is not None else (key == self.subject)
            if key == "daily":
                b.label = name(key)
                continue
            pool = self.pool(key)
            done = sum(1 for r in pool if str(r["id"]) in answered)
            total = 200 if key == "skills" else TARGET_PER_SUBJECT
            b.label = f"{name(key)}   {done}/{total}"

    def draw(self, s):
        blueprint_background(s)
        t = w("title")
        s.blit(font_for(t, 32, True).render(t, True, TEXT), (24, 12))
        sub = w("sub")
        fs = font_for(sub, 14)
        y = 56
        for line in _wrap(fs, sub, WIDTH - 420):
            s.blit(fs.render(line, True, MUTED), (26, y))
            y += fs.get_linesize()
        a = self.save.academy
        wl = w("wallet", w=rs(a["wallet"]), e=rs(a["earned"]))
        s.blit(font_for(wl, 18, True).render(wl, True, ACCENT), (360, 88))
        lab = w("class")
        s.blit(font_for(lab, 15, True).render(lab, True, ACCENT), (26, 118))
        lab = w("subject")
        s.blit(font_for(lab, 15, True).render(lab, True, ACCENT), (26, 270))
        panel(s, (348, 112, WIDTH - 360, HEIGHT - 186), BG_DARK, PANEL_EDGE, 12, alpha=235)
        if self.card is not None:
            self.card.draw(s)
        if self.message:
            fm = font_for(self.message, 17, True)
            my = HEIGHT - 120 if self.card is not None else 150
            for line in _wrap(fm, self.message, WIDTH - 420):
                s.blit(fm.render(line, True, GOOD if self.card is None else WARN), (372, my))
                my += fm.get_linesize()
        info = (w("daily_left", k=self.daily_k + 1, n=len(self.daily))
                if self.daily is not None and self.daily_k < len(self.daily)
                else w("reward", c=self.cls, g=rs(1000.0 * self.cls), b=rs(200.0)))
        s.blit(font_for(info, 14).render(info, True, CYAN), (360, HEIGHT - 58))
        free = w("free")
        s.blit(font_for(free, 13).render(free, True, MUTED), (360, HEIGHT - 34))
        self.widgets.draw(s)
