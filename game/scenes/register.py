"""Player registration overlay script with active text input handling."""
import pygame
from ..ui import ACCENT, BG_DARK, CYAN, PANEL, PANEL_EDGE, TEXT, WIDTH, HEIGHT, Button, font_for, panel, text

class RegisterOverlay:
    def __init__(self, app, on_success):
        self.app = app
        self.on_success = on_success
        self.rect = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 - 200, 440, 380)
        
        # Form fields: (label, active_bool, text_value)
        self.fields = [
            {"label": "Name (Required):", "val": "", "active": True},
            {"label": "Phone (Optional):", "val": "", "active": False},
            {"label": "Email (Optional):", "val": "", "active": False},
        ]
        self.active_idx = 0
        
        self.widgets = WidgetGroup()
        # Start Playing button
        self.widgets.add(Button((self.rect.centerx - 90, self.rect.bottom - 60, 180, 40), "Start Playing", self.submit, size=16))
        
        try:
            pygame.key.start_text_input()
        except (AttributeError, pygame.error):
            pass

    def submit(self):
        name = self.fields[0]["val"].strip()
        if not name:
            return  # Name is mandatory
        phone = self.fields[1]["val"].strip()
        email = self.fields[2]["val"].strip()
        try:
            pygame.key.stop_text_input()
        except (AttributeError, pygame.error):
            pass
        self.on_success(name, phone, email)

    def handle(self, event):
        if self.widgets.handle(event):
            return True
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check clicks on input boxes
            rx = self.rect.x + 30
            ry = self.rect.y + 70
            for i, f in enumerate(self.fields):
                box_rect = pygame.Rect(rx, ry + i * 90, self.rect.w - 60, 36)
                if box_rect.collidepoint(event.pos):
                    self.active_idx = i
                    for j, field in enumerate(self.fields):
                        field["active"] = (j == i)
                    return True

        elif event.type == pygame.TEXTINPUT:
            ch = "".join(c for c in event.text if c.isprintable())
            if ch:
                f = self.fields[self.active_idx]
                if len(f["val"]) < 40:
                    f["val"] += ch
            return True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active_idx = (self.active_idx + 1) % len(self.fields)
                for j, f in enumerate(self.fields):
                    f["active"] = (j == self.active_idx)
                return True
            elif event.key == pygame.K_BACKSPACE:
                f = self.fields[self.active_idx]
                f["val"] = f["val"][:-1]
                return True
            elif event.key == pygame.K_RETURN:
                if self.active_idx < len(self.fields) - 1:
                    self.active_idx += 1
                    for j, f in enumerate(self.fields):
                        f["active"] = (j == self.active_idx)
                else:
                    self.submit()
                return True
        return False

    def update(self, dt):
        pass

    def draw(self, surface):
        # Dim background
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 180))
        surface.blit(veil, (0, 0))
        
        # Panel box
        r = panel(surface, self.rect, PANEL, ACCENT, 14)
        
        # Title
        title = "Player Registration"
        surface.blit(font_for(title, 22, True).render(title, True, TEXT), (r.x + 30, r.y + 20))
        
        rx = r.x + 30
        ry = r.y + 65
        for i, f in enumerate(self.fields):
            # Label
            surface.blit(font_for(f["label"], 14).render(f["label"], True, CYAN), (rx, ry + i * 90))
            
            # Input Box
            box_rect = pygame.Rect(rx, ry + i * 90 + 22, r.w - 60, 36)
            pygame.draw.rect(surface, BG_DARK, box_rect, border_radius=6)
            border_col = ACCENT if f["active"] else PANEL_EDGE
            pygame.draw.rect(surface, border_col, box_rect, 1, border_radius=6)
            
            # Text Value
            val = f["val"] if f["val"] else ("Enter your name" if i == 0 else "Optional")
            col = TEXT if f["val"] else (100, 110, 130)
            txt_surface = font_for(val, 14).render(val, True, col)
            surface.blit(txt_surface, (box_rect.x + 10, box_rect.y + 8))
            
            # Blinking cursor for active box
            if f["active"] and (pygame.time.get_ticks() // 500) % 2 == 0:
                cx = box_rect.x + 10 + font_for(f["val"], 14).size(f["val"])[0] + 2
                pygame.draw.line(surface, ACCENT, (cx, box_rect.y + 8), (cx, box_rect.bottom - 8), 2)

        self.widgets.draw(surface)

# Import WidgetGroup helper locally to prevent circular imports if needed
from ..ui import WidgetGroup