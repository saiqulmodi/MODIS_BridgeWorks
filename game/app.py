"""
MODIS BridgeWorks - Desktop App with Fixed ₹5,000 Award + ₹500 Attendance
"""
import asyncio
import json
import os
import pygame
from engine.landmarks import BandraWorliSeaLink
from game.economy import CivicEconomy

STAGES = [
    {"id": 1, "name": "Tension Fibers", "class": "Class 1-7"},
    {"id": 2, "name": "Coplanar Trusses", "class": "Class 8-10"},
    {"id": 3, "name": "Parabolic Thrust", "class": "Class 11-12"},
    {"id": 4, "name": "Stay Dynamics", "class": "JEE Advanced"},
    {"id": 5, "name": "Matrix Dissipation", "class": "IIT Mechanics"}
]

class App:
    def __init__(self):
        pygame.init()
        self.w = 1040
        self.h = 680
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("MODIS BridgeWorks: Structural Mechanics & NCERT Physics")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Segoe UI", 15, bold=True)
        self.font_sm = pygame.font.SysFont("Segoe UI", 12)
        
        self.economy = CivicEconomy(project_name="BridgeWorks", initial_grant=50000000)
        self.sea_link = BandraWorliSeaLink(self.w, self.h)
        self.current_stage = 1
        self.tick = 0
        self.score = 0
        self.running = True
        
        self.questions = []
        q_path = os.path.join("data", "questions.json")
        if os.path.exists(q_path):
            with open(q_path, "r", encoding="utf-8") as f:
                self.questions = json.load(f)
        self.current_q_idx = 0
        self.deck_nodes = [(x, int(self.h * 0.78) - 55) for x in range(160, self.w - 160, 45)]

    def draw_hud(self):
        pygame.draw.rect(self.screen, (30, 41, 59), (0, 0, self.w, 42))
        pygame.draw.line(self.screen, (51, 65, 85), (0, 42), (self.w, 42), 2)
        st = self.economy.get_status()
        hud_str = f"Score: {self.score}  |  Treasury: {st['Treasury']}  |  Subsidies: {st['Subsidies']}  |  Vehicles: {st['Vehicles Passed']}"
        self.screen.blit(self.font.render(hud_str, True, (248, 250, 252)), (20, 10))

        tab_w = (self.w - 40) // 5
        for i, s in enumerate(STAGES):
            x = 20 + i * tab_w
            is_active = (s["id"] == self.current_stage)
            bg_col = (2, 132, 199) if is_active else (30, 41, 59)
            border_col = (56, 189, 248) if is_active else (71, 85, 105)
            
            pygame.draw.rect(self.screen, bg_col, (x, 48, tab_w - 6, 40), border_radius=6)
            pygame.draw.rect(self.screen, border_col, (x, 48, tab_w - 6, 40), 2, border_radius=6)
            
            self.screen.blit(self.font.render(s["name"], True, (255, 255, 255)), (x + 8, 52))
            self.screen.blit(self.font_sm.render(s["class"], True, (203, 213, 225)), (x + 8, 70))

        if self.questions:
            q = self.questions[self.current_q_idx % len(self.questions)]
            card_rect = pygame.Rect(20, self.h - 110, self.w - 40, 95)
            pygame.draw.rect(self.screen, (30, 41, 59), card_rect, border_radius=8)
            pygame.draw.rect(self.screen, (2, 132, 199), card_rect, 2, border_radius=8)
            
            q_header = self.font.render(f"Curriculum Checkpoint ({q['tier']}) - Attending: +₹500 | Correct: +₹5,000 (+4 Pts)", True, (56, 189, 248))
            q_text = self.font.render(q['question'][:120] + "...", True, (255, 255, 255))
            self.screen.blit(q_header, (32, self.h - 104))
            self.screen.blit(q_text, (32, self.h - 84))
            
            opts_str = f"[1] {q['options'][0]}    [2] {q['options'][1]}"
            self.screen.blit(self.font_sm.render(opts_str, True, (226, 232, 240)), (32, self.h - 58))
            opts_str2 = f"[3] {q['options'][2]}    [4] {q['options'][3]}    |  [SPACE] Run Load Convoy"
            self.screen.blit(self.font_sm.render(opts_str2, True, (226, 232, 240)), (32, self.h - 38))

    async def run(self):
        while self.running:
            self.tick += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if 48 <= my <= 88:
                        tab_w = (self.w - 40) // 5
                        idx = (mx - 20) // tab_w + 1
                        if 1 <= idx <= 5:
                            self.current_stage = idx
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.economy.collect_toll_revenue(25)
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        ans_idx = event.key - pygame.K_1
                        q = self.questions[self.current_q_idx % len(self.questions)]
                        if ans_idx == q["correct"]:
                            self.score += 4
                            self.economy.treasury += 5500  # 5000 bonus + 500 attendance
                            self.economy.subsidies_earned += 5500
                        else:
                            self.score = max(0, self.score - 1)
                            self.economy.treasury += 500   # 500 attendance incentive
                            self.economy.subsidies_earned += 500
                        self.current_q_idx += 1

            self.screen.fill((15, 23, 42))
            self.sea_link.render_sea(self.screen, self.tick)
            if self.current_stage >= 4:
                self.sea_link.render_diamond_pylon(self.screen)
                self.sea_link.render_stay_cables(self.screen, self.deck_nodes)
            
            pygame.draw.line(self.screen, (245, 158, 11), self.deck_nodes[0], self.deck_nodes[-1], 4)
            for pt in self.deck_nodes:
                pygame.draw.circle(self.screen, (226, 232, 240), pt, 4)

            self.draw_hud()
            pygame.display.flip()
            self.clock.tick(60)
            await asyncio.sleep(0)

        pygame.quit()
