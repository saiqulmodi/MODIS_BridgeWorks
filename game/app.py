"""The application: window, main loop and switching between the menu and levels."""
import asyncio

import pygame

from engine.levels import LEVELS, get

from . import i18n, screen, sound
from .save import Save
from .ui import HEIGHT, WIDTH

TITLE = "MODIS BridgeWorks"
FPS = 60


def scene_for(app, level):
    from .scenes.bridge import BridgeScene
    from .scenes.cantilever import CantileverScene
    from .scenes.logistics import LogisticsScene
    from .scenes.rail import RailScene
    from .scenes.signals import SignalScene
    from .scenes.traffic import TrafficScene
    return {"bridge": BridgeScene, "rail": RailScene, "cantilever": CantileverScene,
            "signals": SignalScene, "traffic": TrafficScene,
            "logistics": LogisticsScene}[level.scene](app, level)


class App:
    def __init__(self, save=None, headless=False, show_briefings=True):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = screen.create_window(headless)
        self.clock = pygame.time.Clock()
        self.save = save or Save()
        i18n.set_lang(self.save.data.get("lang", "en"))
        self.headless = headless
        self.show_briefings = show_briefings
        if not headless:
            sound.init()
        self.running = True
        self.scene = None
        self.to_menu()

    def to_menu(self):
        from .scenes.menu import MenuScene
        self.scene = MenuScene(self)

    def start_level(self, num):
        self.scene = scene_for(self, get(num))

    def quit(self):
        self.running = False

    def toggle_language(self):
        self.save.data["lang"] = i18n.toggle()
        self.save.write()

    def frame(self, events, dt):
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                screen.toggle_fullscreen()
            else:
                self.scene.handle(e)
        self.scene.update(dt)
        self.scene.draw(self.screen)

    async def run(self):
        """Main loop. It is async so the same code runs in the browser (pygbag), where each
        frame must hand control back to the page with `await asyncio.sleep(0)`."""
        frames = 0
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 1 / 20)
            if frames % 30 == 0:
                screen.fit_browser()          # browser: keep the canvas filling the window
            frames += 1
            self.frame(pygame.event.get(), dt)
            pygame.display.flip()
            await asyncio.sleep(0)
        pygame.quit()


__all__ = ["App", "LEVELS"]
