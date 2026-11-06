import pygame

TAB_BRIDGE = "BRIDGE_VIEW"
TAB_NCERT = "NCERT_VIEW"

class NCERTOverlay:
    def __init__(self, q_manager):
        self.qm = q_manager
        self.active_tab = TAB_NCERT
        self.classes = self.qm.get_classes() or [f"Class {i}" for i in range(1, 13)]
        self.selected_class_idx = 0
        self.subjects = []
        self.selected_subject_idx = 0
        self.current_q = None
        self.selected_option = None
        self.result_message = ""
        self.update_subject_pool()

    def update_subject_pool(self):
        cls_name = self.classes[self.selected_class_idx]
        self.subjects = self.qm.get_subjects(cls_name)
        if not self.subjects:
            self.subjects = ["General", "Physics", "Mathematics", "Science"]
        self.selected_subject_idx = 0
        self.next_question()

    def next_question(self):
        cls_name = self.classes[self.selected_class_idx]
        subj = self.subjects[self.selected_subject_idx] if self.subjects else None
        self.current_q = self.qm.get_next_question(cls_name, subj)
        self.selected_option = None
        self.result_message = ""

    def handle_click(self, pos, app_state):
        x, y = pos
        # Top Global Tab Clicks
        if 40 <= x <= 260 and 8 <= y <= 48:
            self.active_tab = TAB_BRIDGE
            return
        if 280 <= x <= 560 and 8 <= y <= 48:
            self.active_tab = TAB_NCERT
            return

        if self.active_tab != TAB_NCERT:
            return

        # Class Ribbon Clicks
        for i, _ in enumerate(self.classes[:12]):
            bx = 40 + (i * 98)
            if bx <= x <= bx + 90 and 65 <= y <= 95:
                self.selected_class_idx = i
                self.update_subject_pool()
                return

        # Subject Selector Clicks
        for j, _ in enumerate(self.subjects):
            sx = 40 + (j * 140)
            if sx <= x <= sx + 130 and 105 <= y <= 135:
                self.selected_subject_idx = j
                self.next_question()
                return

        # MCQ Option Clicks
        if self.current_q and "options" in self.current_q:
            for opt_idx, _ in enumerate(self.current_q["options"]):
                oy = 240 + (opt_idx * 60)
                if 40 <= x <= 800 and oy <= y <= oy + 48:
                    correct = self.current_q.get("answer")
                    if opt_idx == correct:
                        app_state["balance"] = app_state.get("balance", 0) + 100
                        self.result_message = "Correct! +Rs 100 Grant Earned."
                    else:
                        self.result_message = "Incorrect. Try next question."
                    self.selected_option = opt_idx
                    return

        # Next Button Click
        if 40 <= x <= 200 and 520 <= y <= 565:
            self.next_question()

    def render(self, screen, font, app_state):
        # 1. Permanent Top HUD Bar
        pygame.draw.rect(screen, (24, 28, 38), (0, 0, 1280, 56))
        pygame.draw.line(screen, (45, 55, 72), (0, 55), (1280, 55), 2)

        col_b = (59, 130, 246) if self.active_tab == TAB_BRIDGE else (40, 48, 64)
        col_q = (16, 185, 129) if self.active_tab == TAB_NCERT else (40, 48, 64)
        pygame.draw.rect(screen, col_b, (40, 8, 220, 40), border_radius=6)
        pygame.draw.rect(screen, col_q, (280, 8, 280, 40), border_radius=6)

        t_br = font.render("Bridge Sandbox", True, (255, 255, 255))
        t_nc = font.render(f"NCERT Bank ({self.classes[self.selected_class_idx]})", True, (255, 255, 255))
        screen.blit(t_br, t_br.get_rect(center=(150, 28)))
        screen.blit(t_nc, t_nc.get_rect(center=(420, 28)))

        grants = font.render(f"Civil Grants: Rs {app_state.get('balance', 0):,}", True, (250, 204, 21))
        screen.blit(grants, (1030, 18))

        if self.active_tab != TAB_NCERT:
            return

        # 2. NCERT Class Selector Ribbon
        for i, cls in enumerate(self.classes[:12]):
            bx = 40 + (i * 98)
            col = (37, 99, 235) if i == self.selected_class_idx else (30, 36, 48)
            pygame.draw.rect(screen, col, (bx, 65, 90, 30), border_radius=4)
            lbl = font.render(cls, True, (255, 255, 255))
            screen.blit(lbl, lbl.get_rect(center=(bx + 45, 80)))

        # 3. Subject Filter Ribbon
        for j, subj in enumerate(self.subjects):
            sx = 40 + (j * 140)
            col_s = (13, 148, 136) if j == self.selected_subject_idx else (25, 30, 42)
            pygame.draw.rect(screen, col_s, (sx, 105, 130, 30), border_radius=4)
            slbl = font.render(subj, True, (230, 240, 255))
            screen.blit(slbl, slbl.get_rect(center=(sx + 65, 120)))

        # 4. Question & Options Card
        if self.current_q:
            # Metadata banner
            subtopic = self.current_q.get("subtopic", "General")
            qtype = self.current_q.get("question_type", "Conceptual")
            meta_str = f"Syllabus Subtopic: {subtopic}  |  Type: {qtype}"
            screen.blit(font.render(meta_str, True, (148, 163, 184)), (40, 150))

            q_txt = font.render(self.current_q.get("question", ""), True, (255, 255, 255))
            screen.blit(q_txt, (40, 185))

            for idx, opt in enumerate(self.current_q.get("options", [])):
                oy = 240 + (idx * 60)
                box_col = (33, 41, 54)
                if self.selected_option is not None:
                    if idx == self.current_q.get("answer"):
                        box_col = (22, 101, 52)
                    elif idx == self.selected_option:
                        box_col = (153, 27, 27)
                pygame.draw.rect(screen, box_col, (40, oy, 760, 48), border_radius=6)
                pygame.draw.rect(screen, (71, 85, 105), (40, oy, 760, 48), 1, border_radius=6)
                screen.blit(font.render(f"{chr(65+idx)}. {opt}", True, (240, 240, 240)), (55, oy + 12))

        # 5. Next Question & Feedback
        if self.result_message:
            res = font.render(self.result_message, True, (250, 204, 21))
            screen.blit(res, (220, 532))

        pygame.draw.rect(screen, (79, 70, 229), (40, 520, 160, 45), border_radius=6)
        btn_next = font.render("Next Question", True, (255, 255, 255))
        screen.blit(btn_next, btn_next.get_rect(center=(120, 542)))
