"""The application: window, main loop and switching between the menu and levels."""
import asyncio
import pygame

from engine.levels import LEVELS, get

from . import i18n, screen, sound
from .save import Save
from .ui import HEIGHT, WIDTH

TITLE = "MODIS BridgeWorks"
FPS = 60

QUIT_BTN_RECT = pygame.Rect(WIDTH - 75, 10, 65, 26)


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
        self.home = "menu"
        self.campus_state = None
        self.font = pygame.font.SysFont(None, 20)
        self.to_campus()

    def to_menu(self):
        if self.home == "campus":
            self.to_campus()
            return
        from .scenes.menu import MenuScene
        self.scene = MenuScene(self)

    def to_classic_menu(self):
        self.home = "menu"
        from .scenes.menu import MenuScene
        self.scene = MenuScene(self)

    def to_campus(self):
        from .scenes.campus import CampusScene
        self.home = "menu"
        self.scene = CampusScene(self)

    def to_academy(self):
        from .scenes.academy import AcademyScene
        self.scene = AcademyScene(self)

    def to_donations(self):
        from .scenes.donations import DonationScene
        self.scene = DonationScene(self)

    def start_level(self, num):
        self.scene = scene_for(self, get(num))

    def quit(self):
        self.running = False

    def toggle_language(self):
        self.save.data["lang"] = i18n.toggle()
        self.save.write()

    def _draw_quit_button(self):
        mouse_pos = pygame.mouse.get_pos()
        hover = QUIT_BTN_RECT.collidepoint(mouse_pos)
        color = (190, 40, 40) if hover else (120, 30, 30)

        pygame.draw.rect(self.screen, color, QUIT_BTN_RECT, border_radius=4)
        pygame.draw.rect(self.screen, (220, 220, 220), QUIT_BTN_RECT, width=1, border_radius=4)

        text = self.font.render("Quit", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=QUIT_BTN_RECT.center))

    def frame(self, events, dt):
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if QUIT_BTN_RECT.collidepoint(e.pos):
                    self.quit()
                    return
                self.scene.handle(e)
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                screen.toggle_fullscreen()
            else:
                self.scene.handle(e)
        self.scene.update(dt)
        self.scene.draw(self.screen)
        self._draw_quit_button()

    async def run(self):
        frames = 0
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 1 / 20)
            if frames % 30 == 0:
                screen.fit_browser()
            frames += 1
            self.frame(pygame.event.get(), dt)
            pygame.display.flip()
            await asyncio.sleep(0)
        pygame.quit()


__all__ = ["App", "LEVELS"]
