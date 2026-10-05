"""NCERT and Engineering Question Bank Browser and Practice Overlay for Phase 1 to Phase 5."""
import pygame
from ..ui import ACCENT, BG_DARK, CYAN, GOOD, HEIGHT, LINE, MUTED, PANEL, PANEL_EDGE, TEXT, WIDTH, Button, WidgetGroup, font_for, panel, text

class NCERTBrowserOverlay:
    def __init__(self, app, on_close):
        self.app = app
        self.on_close = on_close
        self.rect = pygame.Rect(100, 50, WIDTH - 200, HEIGHT - 100)
        
        # Load questions from all phases (Phase 1 through Phase 5)
        self.questions = []
        
        try:
            from ..ncert_bank.phase1_foundation import FOUNDATION_QUESTIONS
            for q in FOUNDATION_QUESTIONS:
                self.questions.append(("Phase 1: Foundation (Classes 1-7)", q))
        except ImportError:
            pass

        try:
            from ..ncert_bank.phase2_advanced import ADVANCED_QUESTIONS
            for q in ADVANCED_QUESTIONS:
                self.questions.append(("Phase 2: Advanced (Classes 8-12)", q))
        except ImportError:
            pass

        try:
            from ..ncert_bank.phase3_engineering import PHASE3_QUESTIONS
            for q in PHASE3_QUESTIONS:
                self.questions.append(("Phase 3: Higher Secondary Eng. (11-12)", q))
        except ImportError:
            pass

        try:
            from ..ncert_bank.phase4_nit import PHASE4_NIT_QUESTIONS
            for q in PHASE4_NIT_QUESTIONS:
                self.questions.append(("Phase 4: NIT Level Rigor (11-12)", q))
        except ImportError:
            pass

        try:
            from ..ncert_bank.phase5_iit import PHASE5_IIT_QUESTIONS
            for q in PHASE5_IIT_QUESTIONS:
                self.questions.append(("Phase 5: IIT Advanced JEE Level", q))
        except ImportError:
            pass
        
        self.scroll = 0
        self.selected_idx = 0
        
        self.widgets = WidgetGroup()
        r = self.rect
        self.widgets.add(Button((r.right - 140, r.y + 16, 120, 36), "Close (Esc)", self.close, size=15))
        
    def close(self):
        from .. import sound
        sound.play("click")
        self.on_close()

    def handle(self, event):
        if self.widgets.handle(event):
            return True
            
        if event.type == pygame.MOUSEWHEEL:
            self.scroll -= event.y * 40
            max_s = max(0, len(self.questions) * 110 - (self.rect.h - 120))
            self.scroll = max(0, min(self.scroll, max_s))
            return True
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rx = self.rect.x + 30
            ry = self.rect.y + 80 - self.scroll
            for i, (phase_name, q_data) in enumerate(self.questions):
                item_rect = pygame.Rect(rx, ry + i * 110, self.rect.w - 60, 100)
                if item_rect.collidepoint(event.pos):
                    self.selected_idx = i
                    # Trigger Economy Reward: Reading / Exploring content
                    if hasattr(self.app, "player_profile") and self.app.player_profile:
                        self.app.player_profile.read_content(f"ncert_{i}")
                    return True
        return False

    def update(self, dt):
        pass

    def draw(self, surface):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 180))
        surface.blit(veil, (0, 0))
        
        r = panel(surface, self.rect, PANEL, ACCENT, 14)
        
        title = "Question Bank Browser (NCERT Foundation to IIT/NIT Engineering)"
        surface.blit(font_for(title, 20, True).render(title, True, TEXT), (r.x + 30, r.y + 20))
        
        content_rect = pygame.Rect(r.x + 20, r.y + 70, r.w - 40, r.h - 90)
        surface.set_clip(content_rect)
        
        rx = content_rect.x + 10
        ry = content_rect.y - self.scroll
        
        for i, (phase_name, q_data) in enumerate(self.questions):
            cls_lvl, subject, question_text, correct_ans, options = q_data
            item_rect = pygame.Rect(rx, ry + i * 110, content_rect.w - 20, 100)
            
            bg_col = (45, 75, 115) if i == self.selected_idx else BG_DARK
            pygame.draw.rect(surface, bg_col, item_rect, border_radius=8)
            pygame.draw.rect(surface, ACCENT if i == self.selected_idx else PANEL_EDGE, item_rect, 1, border_radius=8)
            
            tag = f"[{phase_name}] Class {cls_lvl} - {subject}"
            surface.blit(font_for(tag, 12, True).render(tag, True, CYAN), (item_rect.x + 12, item_rect.y + 10))
            
            surface.blit(font_for(question_text, 14, True).render(question_text, True, TEXT), (item_rect.x + 12, item_rect.y + 32))
            
            ans_str = f"Answer: {correct_ans}"
            surface.blit(font_for(ans_str, 13).render(ans_str, True, GOOD), (item_rect.x + 12, item_rect.y + 68))
            
        surface.set_clip(None)
        self.widgets.draw(surface)