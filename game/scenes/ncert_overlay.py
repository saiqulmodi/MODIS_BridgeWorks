"""NCERT Question Bank Browser and Interactive Practice Overlay."""
import pygame
from ..ui import ACCENT, BG_DARK, CYAN, GOOD, BAD, HEIGHT, LINE, MUTED, PANEL, PANEL_EDGE, TEXT, WIDTH, Button, WidgetGroup, font_for, panel, text

class NCERTBrowserOverlay:
    def __init__(self, app, on_close):
        self.app = app
        self.on_close = on_close
        self.rect = pygame.Rect(100, 50, WIDTH - 200, HEIGHT - 100)
        
        # Load questions from Phase 1 foundation bank
        try:
            from ..ncert_bank.phase1_foundation import FOUNDATION_QUESTIONS
            self.questions = [("Phase 1: Foundation", q) for q in FOUNDATION_QUESTIONS]
        except ImportError:
            self.questions = []
            
        self.scroll = 0
        self.selected_idx = 0
        self.selected_option = None  # Tracks which option index the player clicked for the active question
        self.feedback_msg = ""
        
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
            max_scroll = max(0, len(self.questions) * 140 - (self.rect.h - 120))
            self.scroll = max(0, min(self.scroll, max_scroll))
            return True
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rx = self.rect.x + 30
            ry = self.rect.y + 80 - self.scroll
            
            for i, (phase_name, q_data) in enumerate(self.questions):
                cls_lvl, subject, q_text, correct_ans, options = q_data
                item_rect = pygame.Rect(rx, ry + i * 140, self.rect.w - 60, 130)
                
                if item_rect.collidepoint(event.pos):
                    self.selected_idx = i
                    self.selected_option = None
                    self.feedback_msg = ""
                    
                    # Award 1 Rs for attending / exploring the question
                    if hasattr(self.app, "player_profile") and self.app.player_profile:
                        self.app.player_profile.read_content(f"ncert_{i}")
                    
                    # Check if click landed on one of the 4 choice option buttons inside this card
                    opt_y = item_rect.y + 75
                    opt_w = (item_rect.w - 30) // 2
                    for opt_idx, opt_text in enumerate(options):
                        col_idx = opt_idx % 2
                        row_idx = opt_idx // 2
                        box = pygame.Rect(item_rect.x + 12 + col_idx * (opt_w + 10), opt_y + row_idx * 26, opt_w, 24)
                        if box.collidepoint(event.pos):
                            self.selected_option = opt_idx
                            is_correct = (opt_text.strip().lower() == correct_ans.strip().lower())
                            if is_correct:
                                self.feedback_msg = "Correct! +10 Rs"
                                if hasattr(self.app, "player_profile") and self.app.player_profile:
                                    self.app.player_profile.submit_answer(f"ncert_{i}", True)
                            else:
                                self.feedback_msg = f"Incorrect. Correct answer was: {correct_ans}"
                    return True
        return False

    def update(self, dt):
        pass

    def draw(self, surface):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 180))
        surface.blit(veil, (0, 0))
        
        r = panel(surface, self.rect, PANEL, ACCENT, 14)
        
        title = "Phase 1 Question Bank & Interactive Practice (+1 Rs Read, +10 Rs Correct)"
        surface.blit(font_for(title, 18, True).render(title, True, TEXT), (r.x + 30, r.y + 20))
        
        # Display current player earnings if registered
        if hasattr(self.app, "player_profile") and self.app.player_profile:
            rs_text = f"Earnings: ₹{self.app.player_profile.rupees:.1f}"
            surface.blit(font_for(rs_text, 16, True).render(rs_text, True, GOOD), (r.right - 280, r.y + 22))

        content_rect = pygame.Rect(r.x + 20, r.y + 70, r.w - 40, r.h - 90)
        surface.set_clip(content_rect)
        
        rx = content_rect.x + 10
        ry = content_rect.y - self.scroll
        
        for i, (phase_name, q_data) in enumerate(self.questions):
            cls_lvl, subject, question_text, correct_ans, options = q_data
            item_rect = pygame.Rect(rx, ry + i * 140, content_rect.w - 20, 130)
            
            bg_col = (45, 75, 115) if i == self.selected_idx else BG_DARK
            pygame.draw.rect(surface, bg_col, item_rect, border_radius=8)
            pygame.draw.rect(surface, ACCENT if i == self.selected_idx else PANEL_EDGE, item_rect, 1, border_radius=8)
            
            # Tag & Question
            tag = f"[Class {cls_lvl} - {subject}]"
            surface.blit(font_for(tag, 11, True).render(tag, True, CYAN), (item_rect.x + 12, item_rect.y + 8))
            surface.blit(font_for(question_text, 13, True).render(question_text, True, TEXT), (item_rect.x + 12, item_rect.y + 26))
            
            # Draw 4 Options as clickable choice buttons
            opt_y = item_rect.y + 50
            opt_w = (item_rect.w - 30) // 2
            for opt_idx, opt_text in enumerate(options):
                col_idx = opt_idx % 2
                row_idx = opt_idx // 2
                box = pygame.Rect(item_rect.x + 12 + col_idx * (opt_w + 10), opt_y + row_idx * 26, opt_w, 24)
                
                # Highlight selection color
                opt_bg = BG_DARK
                border_col = PANEL_EDGE
                if i == self.selected_idx and self.selected_option == opt_idx:
                    is_correct = (opt_text.strip().lower() == correct_ans.strip().lower())
                    opt_bg = (40, 120, 70) if is_correct else (130, 50, 50)
                    border_col = GOOD if is_correct else BAD
                    
                pygame.draw.rect(surface, opt_bg, box, border_radius=4)
                pygame.draw.rect(surface, border_col, box, 1, border_radius=4)
                
                choice_label = f"{chr(65+opt_idx)}. {opt_text}"
                surface.blit(font_for(choice_label, 12).render(choice_label, True, TEXT), (box.x + 8, box.y + 4))
            
            # Feedback message for the selected question
            if i == self.selected_idx and self.feedback_msg:
                f_col = GOOD if "Correct" in self.feedback_msg else BAD
                surface.blit(font_for(self.feedback_msg, 12, True).render(self.feedback_msg, True, f_col), (item_rect.x + 12, item_rect.bottom - 20))
            
        surface.set_clip(None)
        self.widgets.draw(surface)