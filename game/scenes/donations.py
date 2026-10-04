"""Donation Camps: give Civil Grants to nation-building causes and watch them grow."""
import pygame

from engine import economy
from engine.donations import CAMPS, GIVE_STEPS, title

from .. import i18n, sound
from ..help_screen import _wrap
from ..ui import (ACCENT, BG_DARK, CYAN, GOOD, HEIGHT, MUTED, PANEL, PANEL_EDGE, TEXT, WARN, WIDTH,
                  Button, WidgetGroup, blueprint_background, font_for, panel)

rs = economy.format_rs

WORDS = {
    "title": ("Donation Camps", "দান-শিবির"),
    "sub": ("Give part of your Civil Grants to causes that build opportunities for people across "
            "the nation. Every gift is recorded; complete a camp to earn its badge.",
            "তোমার সিভিল অনুদানের একটা অংশ এমন কাজে দাও, যা দেশজুড়ে মানুষের জন্য সুযোগ তৈরি করে। "
            "প্রতিটি দান লেখা থাকে; একটা শিবির পূর্ণ করলে তার ব্যাজ পাবে।"),
    "wallet": ("Your Civil Grants: {w}    Given so far: {g}    Title: {t}",
               "তোমার সিভিল অনুদান: {w}    এ পর্যন্ত দান: {g}    উপাধি: {t}"),
    "collected": ("{c} of {t} collected", "{t}-এর মধ্যে {c} সংগৃহীত"),
    "done": ("COMPLETED - badge earned: {b}", "পূর্ণ হয়েছে - ব্যাজ অর্জিত: {b}"),
    "give": ("Give {a}", "দান করো {a}"),
    "give_all": ("Give all I can", "যতটা পারি দান করো"),
    "thanks": ("Thank you! You gave {a} to {c}. +{e} EXP", "ধন্যবাদ! তুমি {c}-এ {a} দান করলে। +{e} EXP"),
    "finished": ("Camp complete! {c} will be built. Badge: {b}", "শিবির পূর্ণ! {c} তৈরি হবে। ব্যাজ: {b}"),
    "empty": ("Your wallet is empty - earn Civil Grants in the Academy first.",
              "তোমার তহবিল খালি - আগে একাডেমিতে সিভিল অনুদান অর্জন করো।"),
    "full": ("This camp is already complete. Choose another cause.",
             "এই শিবির আগেই পূর্ণ হয়েছে। অন্য কোনো কাজ বাছো।"),
    "ledger": ("Your recent gifts", "তোমার সাম্প্রতিক দান"),
    "none": ("No gifts yet.", "এখনো কোনো দান নেই।"),
    "note": ("Only in-game Civil Grants are given here - no real money is collected.",
             "এখানে শুধু খেলার সিভিল অনুদান দান করা হয় - কোনো আসল টাকা নেওয়া হয় না।"),
    "academy": ("Earn grants: Academy", "অনুদান অর্জন: একাডেমি"),
    "menu": ("Menu (Esc)", "মেনু (Esc)"),
    "lang": ("বাংলা (F2)", "English (F2)"),
}


def w(key, **kw):
    en, bn = WORDS[key]
    return (bn if i18n.lang() == "bn" else en).format(**kw)


def blit_text(s, txt, pos, size, colour, bold=False):
    f = font_for(txt, size, bold)
    s.blit(f.render(txt, True, colour), pos)
    return f.get_linesize()


def bar(s, rect, frac, colour):
    rect = pygame.Rect(rect)
    pygame.draw.rect(s, BG_DARK, rect, border_radius=6)
    if frac > 0:
        pygame.draw.rect(s, colour, (rect.x, rect.y, max(6, rect.w * min(frac, 1.0)), rect.h), border_radius=6)
    pygame.draw.rect(s, PANEL_EDGE, rect, 1, border_radius=6)


class DonationScene:
    def __init__(self, app):
        self.app = app
        self.save = app.save
        self.widgets = WidgetGroup()
        self.selected = 0
        self.message, self.msg_good = None, True      # a function, so it follows the language
        self.cards = [pygame.Rect(24, 150 + k * 62, 330, 56) for k in range(len(CAMPS))]
        self.menu_btn = self.widgets.add(Button((WIDTH - 184, 16, 168, 36), "", app.to_menu, size=15,
                                                hotkey=pygame.K_ESCAPE))
        self.lang_btn = self.widgets.add(Button((WIDTH - 360, 16, 168, 36), "", app.toggle_language,
                                                size=15, hotkey=pygame.K_F2))
        self.give_btns = []
        x = 380
        for amount in GIVE_STEPS:
            self.give_btns.append(self.widgets.add(Button((x, 440, 160, 44), "", lambda a=amount: self.give(a),
                                                          size=15, colour=(40, 90, 70))))
            x += 170
        self.all_btn = self.widgets.add(Button((x, 440, 200, 44), "", lambda: self.give(None), size=15,
                                               colour=(90, 70, 30)))
        self.academy_btn = self.widgets.add(Button((WIDTH - 264, HEIGHT - 58, 240, 40), "", app.to_academy,
                                                   size=15))

    def give(self, amount):
        c = CAMPS[self.selected]
        if self.save.donations["given"].get(c.key, 0.0) >= c.target - 1e-6:
            self.message, self.msg_good = (lambda: w("full")), False
            return
        if self.save.wallet <= 0:
            self.message, self.msg_good = (lambda: w("empty")), False
            sound.play("click")
            return
        given, done, exp = self.save.donate(c.key, self.save.wallet if amount is None else amount)
        if done:
            self.message = lambda: w("finished", c=c.name(i18n.lang()), b=c.badge(i18n.lang()))
        else:
            self.message = lambda: w("thanks", a=rs(given), c=c.name(i18n.lang()), e=exp)
        self.msg_good = True
        sound.play("kaching")

    def handle(self, event):
        if self.widgets.handle(event):
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for k, r in enumerate(self.cards):
                if r.collidepoint(event.pos):
                    self.selected, self.message = k, None
                    sound.play("click")
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN):
            step = -1 if event.key == pygame.K_UP else 1
            self.selected = (self.selected + step) % len(CAMPS)
            self.message = None

    def update(self, dt):
        self.menu_btn.label, self.lang_btn.label = w("menu"), w("lang")
        for b, amount in zip(self.give_btns, GIVE_STEPS):
            b.label = w("give", a=rs(amount))
        self.all_btn.label = w("give_all")
        self.academy_btn.label = w("academy")

    def draw(self, s):
        blueprint_background(s)
        lang = i18n.lang()
        blit_text(s, w("title"), (24, 12), 32, TEXT, True)
        y = 56
        sub = w("sub")
        fs = font_for(sub, 14)
        for line in _wrap(fs, sub, WIDTH - 420):
            s.blit(fs.render(line, True, MUTED), (26, y))
            y += fs.get_linesize()
        given = self.save.donations["given"]
        blit_text(s, w("wallet", w=rs(self.save.wallet), g=rs(self.save.donated_total()),
                       t=title(self.save.donated_total(), lang)), (26, 112), 17, ACCENT, True)
        # camp list
        for k, (r, c) in enumerate(zip(self.cards, CAMPS)):
            got = given.get(c.key, 0.0)
            panel(s, r, (40, 70, 115) if k == self.selected else PANEL,
                  ACCENT if k == self.selected else PANEL_EDGE, 10)
            nm = c.name(lang)
            blit_text(s, nm, (r.x + 12, r.y + 6), 15, GOOD if got >= c.target else TEXT, True)
            bar(s, (r.x + 12, r.y + 34, r.w - 24, 12), got / c.target, GOOD if got >= c.target else CYAN)
        # selected camp
        c = CAMPS[self.selected]
        got = given.get(c.key, 0.0)
        box = pygame.Rect(368, 150, WIDTH - 392, 360)
        panel(s, box, BG_DARK, PANEL_EDGE, 12, alpha=235)
        x, y = box.x + 18, box.y + 14
        y += blit_text(s, c.name(lang), (x, y), 24, TEXT, True) + 6
        cause = c.cause(lang)
        fc = font_for(cause, 16)
        for line in _wrap(fc, cause, box.w - 36):
            s.blit(fc.render(line, True, CYAN), (x, y))
            y += fc.get_linesize()
        y += 12
        bar(s, (x, y, box.w - 36, 22), got / c.target, GOOD if got >= c.target else ACCENT)
        y += 30
        blit_text(s, w("collected", c=rs(got), t=rs(c.target)), (x, y), 16, TEXT, True)
        if got >= c.target:
            blit_text(s, w("done", b=c.badge(lang)), (x, y + 26), 16, GOOD, True)
        if self.message:
            msg = self.message()
            fm = font_for(msg, 16, True)
            my = box.y + 222
            for line in _wrap(fm, msg, box.w - 36):
                s.blit(fm.render(line, True, GOOD if self.msg_good else WARN), (x, my))
                my += fm.get_linesize()
        # ledger
        ly = 530
        blit_text(s, w("ledger"), (368, ly), 15, ACCENT, True)
        ly += 24
        rows = self.save.donations["ledger"][-4:][::-1]
        if not rows:
            blit_text(s, w("none"), (368, ly), 14, MUTED)
        for date, key, amount in rows:
            name = next((cc.name(lang) for cc in CAMPS if cc.key == key), key)
            ly += blit_text(s, f"{date}   {rs(amount)}   {name}", (368, ly), 14, TEXT)
        blit_text(s, w("note"), (26, HEIGHT - 34), 13, MUTED)
        self.widgets.draw(s)
