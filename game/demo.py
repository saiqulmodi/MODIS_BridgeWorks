"""Paid demonstrations: watch a working solution, paid for out of the level's budget.

The player is warned - with the exact old and new budget - before anything is charged.
Paying once unlocks free replays of that level's demonstration. Demonstrations never
earn stars or EXP.
"""
import pygame

from engine import economy

from . import sound
from .ui import (ACCENT, BAD, CYAN, GOOD, HEIGHT, MUTED, PANEL, TEXT, WARN, WIDTH, Button,
                 panel, text, text_block)

DEMO_FRACTION = 0.01        # share of the level's base budget a demonstration costs (1%)

# Why each level's demonstration design works (shown in the demo banner and at the end)
DEMO_TEXT = {
    1: "A light timber Warren truss: two big triangles of hollow-box timber. Hollow boxes resist "
       "buckling, and triangles cannot fold.",
    2: "The diesel shunter with only 2 wagons stays under its grip limit on the hill, so it "
       "makes two quick trips instead of stalling with four wagons.",
    3: "Slim haunch, tie-downs on both piers, segments cast left-right in turn, light "
       "post-tensioning after the stitch.",
    4: "One mainline diesel with 5 wagons (two trips), braking 80 m before the stop line so the "
       "wet descent still leaves enough stopping distance.",
    5: "A distant signal 400 m out on each side, the bridge locked to one direction at a time, "
       "the switch following CARGO_AT_JE and the barrier triggered by XING_APPR.",
    6: "A roundabout: cars merge in turn, so nobody waits for a red light and the queue never "
       "reaches the city edge.",
    7: "A deep steel Warren truss with aerodynamic fairings: the fairings weaken the vortices "
       "so the swing never builds up when the wind matches f_n.",
    8: "Slender braced piers on isolation bearings plus flexible joints: forces drop to C = 0.5 "
       "and the joints leave room for the bigger movement.",
    9: "5000 t by rail (one 30-wagon train, under the grip limit) and 1000 t by barge: cheap, "
       "safe and inside 24 hours.",
    10: "A steel deck truss propped by V-piers on both rock islands, with enough grid power for "
        "the maglev pod to cross in time.",
}


def demo_cost(level):
    return DEMO_FRACTION * level.budget


class ConfirmDemo:
    """Warning before paying: shows the cost and the budget before and after."""
    blocks_world = True

    def __init__(self, scene):
        from .ui import WidgetGroup
        self.scene = scene
        self.widgets = WidgetGroup()
        self.rect = pygame.Rect(WIDTH // 2 - 330, 150, 660, 330)
        r = self.rect
        cost = demo_cost(scene.level)
        self.widgets.add(Button((r.x + 30, r.bottom - 64, 290, 44), f"Yes, pay {economy.format_rs(cost)}",
                                scene.pay_and_start_demo, size=16, colour=(120, 70, 30)))
        self.widgets.add(Button((r.right - 320, r.bottom - 64, 290, 44), "No, keep my budget",
                                self.close, size=16, hotkey=pygame.K_ESCAPE))

    def close(self):
        sound.play("click")
        self.scene.overlay = None

    def handle(self, event):
        return self.widgets.handle(event) or event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)

    def update(self, dt):
        pass

    def draw(self, surface):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 160))
        surface.blit(veil, (0, 0))
        r = panel(surface, self.rect, PANEL, WARN, 14)
        sc = self.scene
        cost = demo_cost(sc.level)
        old, new = sc.budget, sc.budget - cost
        text(surface, "WATCH A DEMONSTRATION?", (r.x + 30, r.y + 22), 26, TEXT, bold=True)
        y = text_block(surface, "A demonstration shows one design that solves this level.",
                       (r.x + 30, r.y + 70), r.w - 60, 17, TEXT)
        y = text_block(surface, f"It costs {economy.format_rs(cost)} "
                                f"({DEMO_FRACTION * 100:.0f}% of this level's budget).",
                       (r.x + 30, y + 6), r.w - 60, 17, ACCENT)
        y = text_block(surface, f"WARNING: your total budget for this level will drop from "
                                f"{economy.format_rs(old)} to {economy.format_rs(new)}. "
                                f"This cannot be undone.", (r.x + 30, y + 10), r.w - 60, 18, BAD, bold=True)
        text_block(surface, "After paying, you can replay the demonstration for free. "
                            "A demonstration earns no stars or EXP.",
                   (r.x + 30, y + 10), r.w - 60, 15, MUTED)
        self.widgets.draw(surface)


class DemoDone:
    """End of a demonstration: go back to your own design, or keep the demo design."""
    blocks_world = True

    def __init__(self, scene, worked=True):
        from .ui import WidgetGroup
        self.scene = scene
        self.worked = worked
        self.widgets = WidgetGroup()
        self.rect = pygame.Rect(WIDTH // 2 - 340, 160, 680, 300)
        r = self.rect
        self.widgets.add(Button((r.x + 30, r.bottom - 64, 300, 44), "Back to my design",
                                lambda: scene.end_demo(restore=True), size=16, hotkey=pygame.K_RETURN))
        self.widgets.add(Button((r.right - 330, r.bottom - 64, 300, 44), "Start from this design",
                                lambda: scene.end_demo(restore=False), size=16))

    def handle(self, event):
        return self.widgets.handle(event) or event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)

    def update(self, dt):
        pass

    def draw(self, surface):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 140))
        surface.blit(veil, (0, 0))
        r = panel(surface, self.rect, PANEL, CYAN, 14)
        text(surface, "DEMONSTRATION FINISHED", (r.x + 30, r.y + 22), 26, GOOD if self.worked else WARN,
             bold=True)
        y = text_block(surface, DEMO_TEXT.get(self.scene.level.num, ""), (r.x + 30, r.y + 70),
                       r.w - 60, 17, TEXT)
        text_block(surface, "Demonstrations earn no stars or EXP - now build your own version and "
                            "try to beat its cost!", (r.x + 30, y + 12), r.w - 60, 16, ACCENT)
        self.widgets.draw(surface)
