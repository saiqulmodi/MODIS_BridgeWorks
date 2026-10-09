"""NCERT Curriculum Bank and Interactive Practice Overlay"""
import pygame
from .. import sound
from ..ui import (ACCENT, BG_DARK, CYAN, GOOD, HEIGHT, LINE, MUTED, PANEL, PANEL_EDGE, TEXT,
                  WARN, WIDTH, Button, WidgetGroup, font_for, panel)

class NCERTBrowserOverlay:
    def __init__(self, app, on_close):
        self.app = app
        self.on_close = on_close
        self.rect = pygame.Rect(40, 40, WIDTH - 80, HEIGHT - 80)
        self.widgets = WidgetGroup()
        self.current_tab = 0  # 0 to 4 for Phases 1 to 5
        self.scroll = 0
        self.selected_idx = 0
        self.selected_option = None
        self.feedback_msg = ""
        
        # Close button
        r = self.rect
        self.widgets.add(Button((r.right - 140, r.y + 14, 120, 36), "Close (Esc)", self.close, size=15))
        
        # Load phase question banks dynamically
        self.phases = []
        self._load_phases()


    def _load_phases(self):
        # Phase 1: Foundation (Classes 1-7)
        p1_qs = []
        try:
            from ..ncert_bank.phase1_foundation import FOUNDATION_QUESTIONS
            p1_qs = FOUNDATION_QUESTIONS
        except ImportError:
            p1_qs = []

        # Phase 2: Advanced (Classes 8-12)
        p2_qs = []
        try:
            from ..ncert_bank.phase2_advanced import ADVANCED_QUESTIONS
            p2_qs = ADVANCED_QUESTIONS
        except ImportError:
            p2_qs = []

        # Phase 3: Core Engineering
        p3_qs = []
        try:
            from ..ncert_bank.phase3_engineering import ENGINEERING_QUESTIONS
            p3_qs = ENGINEERING_QUESTIONS
        except ImportError:
            p3_qs = []

        # Phase 4: NIT-Level Rigor
        p4_qs = []
        try:
            from ..ncert_bank.phase4_rigor import RIGOR_QUESTIONS
            p4_qs = RIGOR_QUESTIONS
        except ImportError:
            p4_qs = []

        # Phase 5: IIT Advanced JEE
        p5_qs = []
        try:
            from ..ncert_bank.phase5_jee import JEE_QUESTIONS
            p5_qs = JEE_QUESTIONS
        except ImportError:
            p5_qs = []

        self.phases = [
            {"title": "Phase 1", "questions": p1_qs},
            {"title": "Phase 2", "questions": p2_qs},
            {"title": "Phase 3", "questions": p3_qs},
            {"title": "Phase 4", "questions": p4_qs},
            {"title": "Phase 5", "questions": p5_qs},
        ]
    def close(self):
        sound.play("click")
        self.on_close()

    def is_phase_unlocked(self, tab_idx):
        return True  # All phases permanently unlocked for browsing and building

    def handle(self, event):
        if self.widgets.handle(event):
            return True
            
        r = self.rect
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Tab selection click handler
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
            
            # Question card & option click handler
            content_rect = pygame.Rect(r.x + 20, r.y + 105, r.w - 40, r.h - 125)
            if content_rect.collidepoint(event.pos):
                current_q_list = self.phases[self.current_tab]["questions"]
                rx = content_rect.x + 10
                ry = content_rect.y + 10 - self.scroll
                
                for i, q_data in enumerate(current_q_list):
                    cls_lvl, subject, q_text, correct_ans, options = q_data
                    item_rect = pygame.Rect(rx, ry + i * 140, content_rect.w - 20, 130)
                    
                    if item_rect.collidepoint(event.pos):
                        self.selected_idx = i
                        self.selected_option = None
                        self.feedback_msg = ""
                        q_id = f"p{self.current_tab}_{i}"
                        
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
                                earned = None
                                if hasattr(self.app, "player_profile") and self.app.player_profile:
                                    profile = self.app.player_profile
                                    if hasattr(profile, "submit_answer"):
                                        earned = profile.submit_answer(q_id, is_correct)
                                paid = f" +{earned} Rs" if earned else ""
                                if is_correct:
                                    self.feedback_msg = "Correct!" + paid
                                else:
                                    self.feedback_msg = f"Incorrect{paid}. Right answer: {correct_ans}"
                                return True
                        return True

        elif event.type == pygame.MOUSEWHEEL:
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
        
        title_str = "Curriculum Bank & Interactive Practice [+1 Rs Read, +10 Rs Correct]"
        surface.blit(font_for(title_str, 20, True).render(title_str, True, TEXT), (r.x + 20, r.y + 16))
        
        tab_w = (r.w - 160) // 5
        for idx, phase in enumerate(self.phases):
            tab_rect = pygame.Rect(r.x + 20 + idx * (tab_w + 5), r.y + 60, tab_w, 30)
            is_active = (idx == self.current_tab)
            col = (40, 90, 130) if is_active else (30, 45, 65)
            pygame.draw.rect(surface, col, tab_rect, border_radius=6)
            pygame.draw.rect(surface, ACCENT if is_active else PANEL_EDGE, tab_rect, 1, border_radius=6)
            
            lbl = phase["title"]
            ft = font_for(lbl, 14, True)
            surface.blit(ft.render(lbl, True, TEXT if is_active else MUTED), 
                         (tab_rect.centerx - ft.size(lbl)[0] // 2, tab_rect.centery - ft.size(lbl)[1] // 2))

        content_rect = pygame.Rect(r.x + 20, r.y + 105, r.w - 40, r.h - 125)
        surface.set_clip(content_rect)
        
        current_q_list = self.phases[self.current_tab]["questions"]
        rx = content_rect.x + 10
        ry = content_rect.y + 10 - self.scroll
        
        for i, q_data in enumerate(current_q_list):
            cls_lvl, subject, question_text, correct_ans, options = q_data
            item_rect = pygame.Rect(rx, ry + i * 140, content_rect.w - 20, 130)
            
            pygame.draw.rect(surface, BG_DARK, item_rect, border_radius=8)
            pygame.draw.rect(surface, ACCENT if i == self.selected_idx else PANEL_EDGE, item_rect, 1, border_radius=8)
            
            hdr = f"Class {cls_lvl} | {subject}"
            surface.blit(font_for(hdr, 13, True).render(hdr, True, CYAN), (item_rect.x + 12, item_rect.y + 8))
            
            surface.blit(font_for(question_text, 15, True).render(question_text, True, TEXT), (item_rect.x + 12, item_rect.y + 26))
            
            opt_y = item_rect.y + 50
            opt_w = (item_rect.w - 30) // 2
            for opt_idx, opt_text in enumerate(options):
                col_idx = opt_idx % 2
                row_idx = opt_idx // 2
                box = pygame.Rect(item_rect.x + 12 + col_idx * (opt_w + 10), opt_y + row_idx * 26, opt_w, 24)
                
                is_selected = (i == self.selected_idx and self.selected_option == opt_idx)
                is_right = (opt_text.strip().lower() == correct_ans.strip().lower())
                
                box_col = (50, 90, 70) if is_selected and is_right else ((90, 50, 50) if is_selected else (35, 50, 75))
                pygame.draw.rect(surface, box_col, box, border_radius=4)
                pygame.draw.rect(surface, LINE, box, 1, border_radius=4)
                
                opt_lbl = f"{chr(65+opt_idx)}. {opt_text}"
                surface.blit(font_for(opt_lbl, 13).render(opt_lbl, True, TEXT), (box.x + 8, box.y + 3))

            if i == self.selected_idx and self.feedback_msg:
                fb_col = GOOD if self.feedback_msg.startswith("Correct") else WARN
                surface.blit(font_for(self.feedback_msg, 13, True).render(self.feedback_msg, True, fb_col), 
                             (item_rect.right - 240, item_rect.y + 8))

        surface.set_clip(None)
        self.widgets.draw(surface)