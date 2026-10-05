"""Tabbed and Phase-Gated Question Bank Browser & Practice Overlay."""
import pygame
from ..ui import ACCENT, BG_DARK, CYAN, GOOD, BAD, HEIGHT, LINE, MUTED, PANEL, PANEL_EDGE, TEXT, WIDTH, Button, WidgetGroup, font_for, panel, text

class NCERTBrowserOverlay:
    def __init__(self, app, on_close):
        self.app = app
        self.on_close = on_close
        self.rect = pygame.Rect(100, 50, WIDTH - 200, HEIGHT - 100)
        
        # Load all phase modules dynamically
        self.phases = []
        
        def load_phase_module(name, path, attr):
            try:
                mod = __import__(path, fromlist=[attr])
                return {"name": name, "questions": getattr(mod, attr)}
            except (ImportError, AttributeError):
                return {"name": name, "questions": []}

        self.phases = [
            load_phase_module("Phase 1: Foundation", "..ncert_bank.phase1_foundation", "FOUNDATION_QUESTIONS"),
            load_phase_module("Phase 2: Advanced", "..ncert_bank.phase2_advanced", "ADVANCED_QUESTIONS"),
            load_phase_module("Phase 3: Engineering", "..ncert_bank.phase3_engineering", "PHASE3_QUESTIONS"),
            load_phase_module("Phase 4: NIT Rigor", "..ncert_bank.phase4_nit", "PHASE4_NIT_QUESTIONS"),
            load_phase_module("Phase 5: IIT Advanced", "..ncert_bank.phase5_iit", "PHASE5_IIT_QUESTIONS"),
        ]
        
        self.current_tab = 0  # Default to Phase 1 tab
        self.scroll = 0
        self.selected_idx = 0
        self.selected_option = None
        self.feedback_msg = ""
        
        self.widgets = WidgetGroup()
        r = self.rect
        self.widgets.add(Button((r.right - 140, r.y + 16, 120, 36), "Close (Esc)", self.close, size=15))
        
    def close(self):
        from .. import sound
        sound.play("click")
        self.on_close()

    def is_phase_unlocked(self, tab_idx):
        if tab_idx == 0:
            return True  # Phase 1 is always unlocked
            
        # Check if all questions in the previous phase are completed
        profile = getattr(self.app, "player_profile", None)
        if not profile:
            return False
            
        prev_questions = self.phases[tab_idx - 1]["questions"]
        prev_ids = [f"p{tab_idx-1}_{idx}" for idx in range(len(prev_questions))]
        return profile.is_phase_complete(prev_ids)

    def handle(self, event):
        if self.widgets.handle(event):
            return True
            
        r = self.rect
        
        # Handle tab clicks at the top
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            tab_w = (r.w - 160) // 5
            for idx in range(5):
                tab_rect = pygame.Rect(r.x + 20 + idx * (tab_w + 5), r.y + 60, tab_w, 30)
                if tab_rect.collidepoint(event.pos):
                    self.current_tab = idx
                    self.scroll = 0
                    self.selected_idx = 0
                    self.selected_option = None
                    self.feedback_msg = ""
                    sound.play("click")
                    return True
            
            # Handle question card interactions if tab is unlocked
            if self.is_phase_unlocked(self.current_tab):
                current_q_list = self.phases[self.current_tab]["questions"]
                rx = r.x + 30
                ry = r.y + 110 - self.scroll
                
                for i, q_data in enumerate(current_q_list):
                    cls_lvl, subject, q_text, correct_ans, options = q_data
                    item_rect = pygame.Rect(rx, ry + i * 140, r.w - 60, 130)
                    
                    if item_rect.collidepoint(event.pos):
                        self.selected_idx = i
                        self.selected_option = None
                        self.feedback_msg = ""
                        q_id = f"p{self.current_tab}_{i}"
                        
                        # Award +1 Rs for exploring
                        if hasattr(self.app, "player_profile") and self.app.player_profile:
                            self.app.player_profile.read_content(q_id)
                        
                        opt_y = item_rect.y + 50
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
                                        profile = self.app.player_profile
                                        profile.completed_questions.add(q_id)
                                        profile.submit_answer(q_id, True)
                                else:
                                    self.feedback_msg = f"Incorrect. Correct answer was: {correct_ans}"
                                return True
                        return True

        elif event.type == pygame.MOUSEWHEEL and self.is_phase_unlocked(self.current_tab):
            current_len = len(self.phases[self.current_tab]["questions"])
            self.scroll -= event.y * 40
            max_scroll = max(0, current_len * 140 - (self.rect.h - 140))
            self.scroll = max(0, min(self.scroll, max_scroll))
            return True
            
        return False

    def update(self, dt):
        pass

    def draw(self, surface):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 180))
        surface.blit(veil, (0, 0))
        
        r = panel(surface, self.rect, PANEL, ACCENT, 14)
        
        title = "Curriculum Bank & Interactive Practice [+1 Rs Read, +10 Rs Correct]"
        surface.blit(font_for(title, 16, True).render(title, True, TEXT), (r.x + 30, r.y + 18))
        
        if hasattr(self.app, "player_profile") and self.app.player_profile:
            rs_text = f"Earnings: ₹{self.app.player_profile.rupees:.1f}"
            surface.blit(font_for(rs_text, 16, True).render(rs_text, True, GOOD), (r.right - 280, r.y + 20))

        # Draw Phase Tabs
        tab_w = (r.w - 160) // 5
        for idx, phase_info in enumerate(self.phases):
            tab_rect = pygame.Rect(r.x + 20 + idx * (tab_w + 5), r.y + 60, tab_w, 30)
            is_active = (idx == self.current_tab)
            is_unlocked = self.is_phase_unlocked(idx)
            
            tab_bg = (45, 75, 115) if is_active else (BG_DARK if is_unlocked else (30, 30, 35))
            tab_border = ACCENT if is_active else (PANEL_EDGE if is_unlocked else (70, 70, 75))
            
            pygame.draw.rect(surface, tab_bg, tab_rect, border_radius=6)
            pygame.draw.rect(surface, tab_border, tab_rect, 1, border_radius=6)
            
            short_name = f"Phase {idx+1}"
            label_color = TEXT if is_unlocked else MUTED
            surface.blit(font_for(short_name, 12, True).render(short_name, True, label_color), (tab_rect.x + 8, tab_rect.y + 8))

        # Content Area
        content_rect = pygame.Rect(r.x + 20, r.y + 100, r.w - 40, r.h - 120)
        surface.set_clip(content_rect)
        
        if not self.is_phase_unlocked(self.current_tab):
            locked_msg = "LOCKED PHASE: Complete all questions in the previous phase to unlock!"
            surface.blit(font_for(locked_msg, 15, True).render(locked_msg, True, BAD), (content_rect.x + 40, content_rect.centery - 20))
        else:
            current_q_list = self.phases[self.current_tab]["questions"]
            rx = content_rect.x + 10
            ry = content_rect.y - self.scroll
            
            for i, q_data in enumerate(current_q_list):
                cls_lvl, subject, question_text, correct_ans, options = q_data
                item_rect = pygame.Rect(rx, ry + i * 140, content_rect.w - 20, 130)
                
                bg_col = (45, 75, 115) if i == self.selected_idx else BG_DARK
                pygame.draw.rect(surface, bg_col, item_rect, border_radius=8)
                pygame.draw.rect(surface, ACCENT if i == self.selected_idx else PANEL_EDGE, item_rect, 1, border_radius=8)
                
                tag = f"[Class {cls_lvl} - {subject}]"
                surface.blit(font_for(tag, 11, True).render(tag, True, CYAN), (item_rect.x + 12, item_rect.y + 8))
                surface.blit(font_for(question_text, 13, True).render(question_text, True, TEXT), (item_rect.x + 12, item_rect.y + 26))
                
                opt_y = item_rect.y + 50
                opt_w = (item_rect.w - 30) // 2
                for opt_idx, opt_text in enumerate(options):
                    col_idx = opt_idx % 2
                    row_idx = opt_idx // 2
                    box = pygame.Rect(item_rect.x + 12 + col_idx * (opt_w + 10), opt_y + row_idx * 26, opt_w, 24)
                    
                    opt_bg = BG_DARK
                    opt_border = PANEL_EDGE
                    if i == self.selected_idx and self.selected_option == opt_idx:
                        is_correct = (opt_text.strip().lower() == correct_ans.strip().lower())
                        opt_bg = (40, 120, 70) if is_correct else (130, 50, 50)
                        opt_border = GOOD if is_correct else BAD
                        
                    pygame.draw.rect(surface, opt_bg, box, border_radius=4)
                    pygame.draw.rect(surface, opt_border, box, 1, border_radius=4)
                    
                    choice_label = f"{chr(65+opt_idx)}. {opt_text}"
                    surface.blit(font_for(choice_label, 12).render(choice_label, True, TEXT), (box.x + 8, box.y + 4))
                
                if i == self.selected_idx and self.feedback_msg:
                    f_col = GOOD if "Correct" in self.feedback_msg else BAD
                    surface.blit(font_for(self.feedback_msg, 12, True).render(self.feedback_msg, True, f_col), (item_rect.x + 12, item_rect.bottom - 20))
            
        surface.set_clip(None)
        self.widgets.draw(surface)