"""
MODIS BridgeWorks - Structural Mechanics & NCERT Physics Sandbox
A Campus World with one building per level (Class 1-12, BE, NIT, IIT, Expert
Engineer). Each building has only its own question bank and a bridge project
matched to its level (5 projects, easy to tough). The student answers that
level's questions to earn parts, builds the bridge joint by joint, and tests it:
a vehicle drives across and the real truss solver checks every member. Live
score card with government merit subsidies, and an in-game Q&A Bank browser.
"""
import asyncio
import math
import pygame

from engine import spread
from engine.truss import FAILED, RED, YELLOW, UnstableStructure
from game.projects import PARTS_PER_CORRECT, PROJECTS, SIZE_COST, Design
from game.question_bank import load_for_game
from game.world import LEVEL_NAMES, LEVELS, World, subject_name, tier_of

STAGES = [
    {"id": 1, "name": "Tension Fibers", "class": "Class 1-7", "min_cls": 1, "max_cls": 7},
    {"id": 2, "name": "Coplanar Trusses", "class": "Class 8-10", "min_cls": 8, "max_cls": 10},
    {"id": 3, "name": "Parabolic Thrust", "class": "Class 11-12", "min_cls": 11, "max_cls": 12},
    {"id": 4, "name": "Stay Dynamics", "class": "JEE Main / NEET", "min_cls": 13, "max_cls": 13},
    {"id": 5, "name": "Matrix Dissipation", "class": "IIT / NIT Olympiad", "min_cls": 14, "max_cls": 20},
]

CORRECT_CASH, CORRECT_PTS = 10000.0, 4
WRONG_CASH, WRONG_PTS = 1000.0, 1
SUBSIDY_PER_POINT = 2500.0
PER_PAGE = 5

TAB_Y, TAB_H = 44, 38            # tabs and bank button: 44 <= y <= 82
BANK_BTN_W = 130
BACK_BTN_W = 96
TOOL_Y, TOOL_H = 88, 24          # build toolbar
CANVAS_TOP = TOOL_Y + TOOL_H + 4
TEST_SECONDS = 5.0               # time for the vehicle to cross

SHORT_NAMES = {"Steel cable": "Steel cable", "Carbon-fibre cable": "Carbon cable",
               "Steel": "Steel beam", "Timber": "Timber beam", "Concrete": "Concrete beam"}
STATUS_COLOURS = {FAILED: (127, 29, 29), RED: (239, 68, 68), YELLOW: (250, 204, 21)}
SAFE = (34, 197, 94)
SIZE_WIDTH = {"S": 2, "M": 3, "L": 4, "XL": 6}


class App:
    def __init__(self):
        pygame.init()
        self.w, self.h = 1080, 600
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("MODIS BridgeWorks: Structural Mechanics & NCERT Physics")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Segoe UI", 14, bold=True)
        self.font_sm = pygame.font.SysFont("Segoe UI", 12)
        self.font_lg = pygame.font.SysFont("Segoe UI", 17, bold=True)
        self.font_icon = pygame.font.SysFont("Segoe UI Emoji", 14)

        self.stages = STAGES
        self.mode = "world"              # "world" or "class"
        self.level = 1
        self.subject = None              # subject filter inside a class, None = all
        self.score = 0
        self.treasury = 50000000.0
        self.vehicles_passed = 0
        self.running = True
        self.show_bank_view = False
        self.bank_page = 0
        self.feedback_msg = ""
        self.feedback_color = (56, 189, 248)

        self.designs = {level: Design(PROJECTS[tier_of(level) - 1]) for level, _ in LEVELS}
        self.material = {p.id: p.materials[0] for p in PROJECTS}
        self.size = {p.id: p.sizes[1] if len(p.sizes) > 1 else p.sizes[0] for p in PROJECTS}
        self.selected = None             # joint index waiting for its second end
        self.test = None                 # {"x", "status", "result", "msg"}
        self.build_msg = ""

        self.raw_questions = load_for_game()
        self.level_stats = {}
        for level, _ in LEVELS:
            qs = [q for q in self.raw_questions if q["class_level"] == level]
            self.level_stats[level] = (len(qs), len({q["subject"] for q in qs}))
        self.world = World(self)
        self.filter_stage_questions()

    # ---------- data ----------
    @property
    def subsidies(self):
        # Merit subsidy: high-scoring students receive proportional government funding
        return max(0.0, self.score * SUBSIDY_PER_POINT)

    @property
    def bank_pages(self):
        return max(1, (len(self.bank_questions) + PER_PAGE - 1) // PER_PAGE)

    @property
    def current_stage(self):
        """Bridge project (1-5) of the class being played."""
        return tier_of(self.level)

    @property
    def level_name(self):
        return LEVEL_NAMES[self.level]

    @property
    def subjects(self):
        return sorted({q["subject"] for q in self.raw_questions if q["class_level"] == self.level},
                      key=subject_name)

    @property
    def design(self):
        return self.designs[self.level]

    @property
    def project(self):
        return PROJECTS[self.current_stage - 1]

    def filter_stage_questions(self):
        self.bank_questions = [q for q in self.raw_questions if q["class_level"] == self.level
                               and (self.subject is None or q["subject"] == self.subject)]
        self.bank_questions.sort(key=lambda q: subject_name(q["subject"]))
        # random order with look-alike questions (same template, new numbers) kept apart
        self.active_questions = spread.order(self.bank_questions)
        self.current_q_idx = 0
        self.bank_page = 0
        self.feedback_msg = ""

    def enter_level(self, level):
        self.mode = "class"
        self.level = level
        self.subject = None
        self.show_bank_view = False
        self.selected = None
        self.test = None
        self.build_msg = ""
        self.filter_stage_questions()

    def to_world(self):
        self.mode = "world"
        self.show_bank_view = False
        self.selected = None
        self.test = None
        self.world.focus(self.level)

    def set_subject(self, subject):
        self.subject = subject
        self.filter_stage_questions()

    def current_question(self):
        if not self.active_questions:
            return None
        return self.active_questions[self.current_q_idx % len(self.active_questions)]

    def next_question(self):
        if self.active_questions:
            self.current_q_idx = (self.current_q_idx + 1) % len(self.active_questions)

    def submit_answer(self, chosen_idx):
        q = self.current_question()
        if q is None or not (0 <= chosen_idx < len(q["options"])):
            return
        if chosen_idx == q["correct_idx"]:
            parts = PARTS_PER_CORRECT[self.current_stage]
            self.score += CORRECT_PTS
            self.treasury += CORRECT_CASH
            self.design.parts += parts
            self.feedback_msg = f"Correct! +₹{CORRECT_CASH:,.0f} | +{CORRECT_PTS} Pts | +{parts} parts"
            self.feedback_color = (34, 197, 94)
        else:
            self.score = max(0, self.score - WRONG_PTS)
            self.treasury = max(0.0, self.treasury - WRONG_CASH)
            self.feedback_msg = f"Wrong! -₹{WRONG_CASH:,.0f} | -{WRONG_PTS} Pt | Answer: {q['answer']}"
            self.feedback_color = (239, 68, 68)
        self.next_question()

    # ---------- building ----------
    def view(self):
        """(scale px/m, origin x px, origin y px) that fits the project in the canvas."""
        p = self.project
        ys = [y for _, y in p.joints]
        top, bottom = CANVAS_TOP + 78, self.h - 150 - 26
        s = min((self.w - 200) / p.span, (bottom - top) / (max(ys) - min(ys)))
        return s, (self.w - p.span * s) / 2, top + max(ys) * s

    def to_px(self, x, y):
        s, ox, oy = self.view()
        return ox + x * s, oy - y * s

    def joint_at(self, mx, my):
        best, best_d = None, 13
        for k, (x, y) in enumerate(self.project.joints):
            px, py = self.to_px(x, y)
            d = math.hypot(px - mx, py - my)
            if d < best_d:
                best, best_d = k, d
        return best

    def member_at(self, mx, my, player_only=False):
        """Index into design.all_members() of the member under the mouse."""
        best, best_d = None, 7
        for k, (i, j, *_rest, pk) in enumerate(self.design.all_members()):
            if player_only and pk is None:
                continue
            (x1, y1), (x2, y2) = self.to_px(*self.project.joints[i]), self.to_px(*self.project.joints[j])
            dx, dy = x2 - x1, y2 - y1
            t = max(0.0, min(1.0, ((mx - x1) * dx + (my - y1) * dy) / max(dx * dx + dy * dy, 1e-9)))
            d = math.hypot(x1 + t * dx - mx, y1 + t * dy - my)
            if d < best_d:
                best, best_d = k, d
        return best

    def edited(self):
        self.test = None

    def click_joint(self, k):
        if self.selected is None:
            self.selected = k
            self.build_msg = "Now click the joint at the other end (Esc cancels)."
            return
        if k == self.selected:
            self.selected = None
            self.build_msg = ""
            return
        pid = self.current_stage
        msg = self.design.add(self.selected, k, self.material[pid], self.size[pid])
        if msg:
            self.build_msg = msg
        else:
            self.build_msg = f"Built: {SHORT_NAMES[self.material[pid].name]} {self.size[pid]}."
            self.edited()
        self.selected = k if msg == "" else self.selected

    def remove_member_at(self, mx, my):
        k = self.member_at(mx, my, player_only=True)
        if k is not None:
            self.design.remove(self.design.all_members()[k][5])
            self.build_msg = "Removed - parts returned."
            self.edited()

    def undo(self):
        if self.design.members:
            self.design.remove(len(self.design.members) - 1)
            self.build_msg = "Undone - parts returned."
            self.edited()

    def clear(self):
        self.design.clear()
        self.selected = None
        self.build_msg = "Cleared - all parts returned."
        self.edited()

    def start_test(self):
        self.selected = None
        self.test = {"x": 0.0, "status": "running", "result": None, "msg": "", "worst": 0.0}
        self.step_test(0.0)

    def step_test(self, dt):
        t = self.test
        if not t or t["status"] != "running":
            return
        p = self.project
        t["x"] += (p.span + p.vehicle.length) / TEST_SECONDS * dt
        try:
            r = self.design.solve_at(t["x"])
        except UnstableStructure as e:
            t.update(status="failed", result=None,
                     msg=f"Collapsed: {e} Every road joint must be held up, and every joint "
                         f"needs at least two members that are not in one straight line.")
            return
        t["result"] = r
        t["worst"] = max(t["worst"], r.max_ratio)
        if r.failed_members:
            worst = r.members[r.worst_member]
            t.update(status="failed", msg=f"{worst.explanation}. Strengthen the dark red member: "
                                          f"bigger size, stronger material or a shorter, braced member.")
        elif t["x"] >= p.span + p.vehicle.length:
            self.design.complete = True
            self.vehicles_passed += 1
            t.update(status="passed", msg=f"Bridge passed! The {p.vehicle.name} crossed safely. "
                                          f"Highest load ratio {t['worst']:.0%} (100% = breaking).")

    # ---------- drawing helpers ----------
    def fit(self, text, font, max_w):
        """Cut text to fit max_w pixels, ending with an ellipsis."""
        text = str(text).replace("\n", " ")
        if font.size(text)[0] <= max_w:
            return text
        while text and font.size(text + "…")[0] > max_w:
            text = text[:-1]
        return text + "…"

    def wrap(self, text, font, max_w, max_lines):
        words, lines, cur = str(text).replace("\n", " ").split(), [], ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if font.size(trial)[0] <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
        if len(lines) > max_lines:
            lines = lines[:max_lines - 1] + [self.fit(" ".join(lines[max_lines - 1:]), font, max_w)]
        return lines

    def bank_btn_rect(self):
        return pygame.Rect(self.w - BANK_BTN_W - 16, TAB_Y, BANK_BTN_W, TAB_H)

    def back_btn_rect(self):
        return pygame.Rect(16, TAB_Y, BACK_BTN_W, TAB_H)

    def subject_chips(self):
        """[(rect, subject or None)] - "All" then each subject of this class."""
        left, right = 16 + BACK_BTN_W + 8 + 170, self.bank_btn_rect().x - 6
        x, row, out = left, 0, []
        for subj in [None] + self.subjects:
            label = "All" if subj is None else subject_name(subj)
            w = self.font_sm.size(label)[0] + 12
            if x + w > right:
                if row == 1:
                    break
                x, row = left, 1
            r = pygame.Rect(x, TAB_Y + row * 20, w, 18)
            out.append((r, subj, label))
            x = r.right + 4
        return out

    def option_rects(self):
        top = self.h - 150
        col_w = (self.w - 64) // 2
        return [pygame.Rect(32 + (i % 2) * (col_w + 8), top + 68 + (i // 2) * 26, col_w - 8, 23)
                for i in range(4)]

    def page_btn_rects(self):
        y = self.h - 46
        return (pygame.Rect(self.w // 2 - 230, y, 110, 28), pygame.Rect(self.w // 2 + 120, y, 110, 28))

    def tool_buttons(self):
        """[(rect, action, label, active)] for the build toolbar."""
        p, pid = self.project, self.current_stage
        out, x = [], 16
        for mat in p.materials:
            label = SHORT_NAMES[mat.name]
            r = pygame.Rect(x, TOOL_Y, self.font_sm.size(label)[0] + 18, TOOL_H)
            out.append((r, ("mat", mat), label, self.material[pid] is mat))
            x = r.right + 4
        x += 10
        for size in p.sizes:
            label = f"{size} ({SIZE_COST[size]})"
            r = pygame.Rect(x, TOOL_Y, self.font_sm.size(label)[0] + 14, TOOL_H)
            out.append((r, ("size", size), label, self.size[pid] == size))
            x = r.right + 4
        right = self.w - 16
        for action, label in (("test", "Test bridge [T]"), ("clear", "Clear"), ("undo", "Undo [U]")):
            wdt = self.font_sm.size(label)[0] + 18
            r = pygame.Rect(right - wdt, TOOL_Y, wdt, TOOL_H)
            out.append((r, (action, None), label, action == "test"))
            right = r.x - 4
        return out

    # ---------- drawing ----------
    def draw_hud(self):
        pygame.draw.rect(self.screen, (30, 41, 59), (0, 0, self.w, 40))
        pygame.draw.line(self.screen, (51, 65, 85), (0, 40), (self.w, 40), 2)
        hud_str = (f"Score: {self.score} | Treasury: ₹{self.treasury:,.2f} | "
                   f"Govt Subsidies: ₹{self.subsidies:,.2f} | Vehicles: {self.vehicles_passed}")
        self.screen.blit(self.font.render(hud_str, True, (248, 250, 252)), (20, 11))

        if self.mode == "world":
            title = "Campus World: every class is a building on the road - click one to enter"
            self.screen.blit(self.font_lg.render(title, True, (226, 232, 240)), (16, TAB_Y + 8))
            return
        back = self.back_btn_rect()
        pygame.draw.rect(self.screen, (51, 65, 85), back, border_radius=6)
        pygame.draw.rect(self.screen, (148, 163, 184), back, 2, border_radius=6)
        label = self.font.render("< World", True, (255, 255, 255))
        self.screen.blit(label, label.get_rect(center=back.center))
        st = STAGES[self.current_stage - 1]
        tx = back.right + 12
        self.screen.blit(self.font_lg.render(self.level_name, True, (255, 255, 255)), (tx, TAB_Y + 1))
        sub = f"Project {st['id']}: {st['name']}" + ("  ·  BUILT" if self.design.complete else "")
        self.screen.blit(self.font_sm.render(sub, True, (110, 231, 183) if self.design.complete
                                             else (203, 213, 225)), (tx, TAB_Y + 22))
        for r, subj, label in self.subject_chips():
            on = subj == self.subject
            pygame.draw.rect(self.screen, (2, 132, 199) if on else (30, 41, 59), r, border_radius=5)
            pygame.draw.rect(self.screen, (71, 85, 105), r, 1, border_radius=5)
            t = self.font_sm.render(label, True, (255, 255, 255))
            self.screen.blit(t, t.get_rect(center=r.center))

        rect = self.bank_btn_rect()
        pygame.draw.rect(self.screen, (16, 185, 129) if self.show_bank_view else (51, 65, 85), rect, border_radius=6)
        pygame.draw.rect(self.screen, (52, 211, 153), rect, 2, border_radius=6)
        if self.show_bank_view:
            label = self.font.render("X  Close Bank", True, (255, 255, 255))
            self.screen.blit(label, label.get_rect(center=rect.center))
        else:
            icon = self.font_icon.render("📋", True, (255, 255, 255))
            label = self.font.render("Q&A Bank", True, (255, 255, 255))
            x = rect.centerx - (icon.get_width() + 4 + label.get_width()) // 2
            self.screen.blit(icon, icon.get_rect(midleft=(x, rect.centery)))
            self.screen.blit(label, label.get_rect(midleft=(x + icon.get_width() + 4, rect.centery)))

    def draw_toolbar(self):
        testing = self.test and self.test["status"] == "running"
        for r, (action, _), label, active in self.tool_buttons():
            if action == "test":
                bg = (22, 163, 74) if not testing else (51, 65, 85)
            else:
                bg = (2, 132, 199) if active else (30, 41, 59)
            pygame.draw.rect(self.screen, bg, r, border_radius=5)
            pygame.draw.rect(self.screen, (71, 85, 105), r, 1, border_radius=5)
            s = self.font_sm.render(label, True, (255, 255, 255))
            self.screen.blit(s, s.get_rect(center=r.center))

    def member_colour(self, k, mat, size):
        t = self.test
        if t and t["result"] is not None:
            res = t["result"].members[k]
            if res.slack:
                return (100, 116, 139)
            return STATUS_COLOURS.get(res.status, SAFE)
        return mat.colour

    def draw_build(self):
        p, d = self.project, self.design
        s, ox, oy = self.view()
        bottom = self.h - 150 - 4
        pygame.draw.rect(self.screen, (11, 17, 32), (0, CANVAS_TOP, self.w, 76))
        pygame.draw.rect(self.screen, (8, 47, 73), (ox, oy + 6, p.span * s, bottom - oy - 6))      # river
        for x0, x1 in ((0, ox), (ox + p.span * s, self.w)):
            pygame.draw.rect(self.screen, (63, 49, 36), (x0, oy, x1 - x0, bottom - oy))           # banks
            pygame.draw.line(self.screen, (101, 163, 13), (x0, oy), (x1, oy), 3)

        mouse = pygame.mouse.get_pos()
        hover_member = None if self.show_bank_view else self.member_at(*mouse)
        for k, (i, j, mat, size, kind, pk) in enumerate(d.all_members()):
            a, b = self.to_px(*p.joints[i]), self.to_px(*p.joints[j])
            col = self.member_colour(k, mat, size)
            width = 8 if kind == "pylon" else SIZE_WIDTH[size] + (1 if kind == "deck" else 0)
            if kind == "cable" and not (self.test and self.test["result"]):
                width = max(1, width - 1)
            pygame.draw.line(self.screen, col, a, b, width)
            if k == hover_member:
                pygame.draw.line(self.screen, (255, 255, 255), a, b, 1)

        if self.selected is not None and not self.show_bank_view:
            pygame.draw.line(self.screen, (250, 204, 21), self.to_px(*p.joints[self.selected]), mouse, 1)

        hover_joint = None if self.show_bank_view else self.joint_at(*mouse)
        for k, (x, y) in enumerate(p.joints):
            px, py = self.to_px(x, y)
            sup = p.supports.get(k)
            if sup:
                pts = [(px, py + 4), (px - 9, py + 16), (px + 9, py + 16)]
                pygame.draw.polygon(self.screen, (148, 163, 184), pts)
                if sup == "roller":
                    pygame.draw.circle(self.screen, (148, 163, 184), (int(px - 5), int(py + 19)), 3)
                    pygame.draw.circle(self.screen, (148, 163, 184), (int(px + 5), int(py + 19)), 3)
            r = 7 if k in (hover_joint, self.selected) else 5
            pygame.draw.circle(self.screen, (250, 204, 21) if k == self.selected else (241, 245, 249),
                               (int(px), int(py)), r)
            pygame.draw.circle(self.screen, (15, 23, 42), (int(px), int(py)), r, 1)

        t = self.test
        if t:
            v = p.vehicle
            for off in v.axles:
                ax = t["x"] - off
                if 0 <= ax <= p.span:
                    px, py = self.to_px(ax, 0)
                    pygame.draw.rect(self.screen, v.colour, (px - 9, py - 15, 18, 11), border_radius=3)
                    pygame.draw.circle(self.screen, (30, 41, 59), (int(px - 5), int(py - 3)), 3)
                    pygame.draw.circle(self.screen, (30, 41, 59), (int(px + 5), int(py - 3)), 3)

        # text: goal, tip, status and hover details
        x0, y0 = 16, CANVAS_TOP + 2
        head = f"Project {p.id}: {p.name} ({p.level}) - {p.goal}"
        self.screen.blit(self.font.render(self.fit(head, self.font, self.w - 32), True, (226, 232, 240)), (x0, y0))
        info = (f"Parts: {d.parts}  (+{PARTS_PER_CORRECT[p.id]} per right answer)  |  "
                f"Load: {p.vehicle.name} {p.vehicle.mass_kg / 1000:g} t"
                + (f" x {p.impact:g} impact" if p.impact != 1 else "") + f"  |  Span {p.span:g} m")
        self.screen.blit(self.font_sm.render(info, True, (250, 204, 21)), (x0, y0 + 19))
        tip = f"Tip: {p.tip}"
        self.screen.blit(self.font_sm.render(self.fit(tip, self.font_sm, self.w - 32), True, (148, 163, 184)),
                         (x0, y0 + 34))

        line, colour = "", (203, 213, 225)
        if t and t["status"] != "running":
            line, colour = t["msg"], (34, 197, 94) if t["status"] == "passed" else (248, 113, 113)
        elif self.build_msg:
            line = self.build_msg
        if hover_member is not None:
            i, j, mat, size, kind, pk = d.all_members()[hover_member]
            desc = f"{SHORT_NAMES.get(mat.name, mat.name)} {size if kind != 'pylon' else ''}, {d.length(i, j):.1f} m"
            if t and t["result"] is not None:
                desc += f": {t['result'].members[hover_member].explanation}"
            elif pk is not None:
                desc += "  (right-click to remove)"
            line, colour = desc, (226, 232, 240)
        if not line:
            line, colour = f"Physics: {p.lesson}", (125, 211, 252)
        for n, ln in enumerate(self.wrap(line, self.font_sm, self.w - 32, 2)):
            self.screen.blit(self.font_sm.render(ln, True, colour), (x0, y0 + 49 + n * 14))

    def draw_checkpoint_card(self):
        top = self.h - 150
        card = pygame.Rect(16, top, self.w - 32, 142)
        pygame.draw.rect(self.screen, (30, 41, 59), card, border_radius=8)
        pygame.draw.rect(self.screen, (2, 132, 199), card, 2, border_radius=8)

        st = STAGES[self.current_stage - 1]
        q = self.current_question()
        if q is None:
            msg = f"No questions in {self.level_name} yet. Run: python -m game.question_bank"
            self.screen.blit(self.font.render(msg, True, (251, 191, 36)), (32, top + 10))
            return

        header = (f"{self.level_name} · {subject_name(q['subject'])}  |  Project {st['id']}: {st['name']}"
                  f"  |  Right +₹10,000 (+4) +{PARTS_PER_CORRECT[self.current_stage]} parts"
                  f"  Wrong -₹1,000 (-1)")
        self.screen.blit(self.font_sm.render(self.fit(header, self.font_sm, self.w - 470), True, (56, 189, 248)),
                         (32, top + 8))
        if self.feedback_msg:
            fb = self.font_sm.render(self.fit(self.feedback_msg, self.font_sm, 420), True, self.feedback_color)
            self.screen.blit(fb, (self.w - 32 - fb.get_width(), top + 8))

        for i, line in enumerate(self.wrap(q["question"], self.font, self.w - 64, 2)):
            self.screen.blit(self.font.render(line, True, (255, 255, 255)), (32, top + 28 + i * 19))

        mouse = pygame.mouse.get_pos()
        for i, rect in enumerate(self.option_rects()):
            hover = rect.collidepoint(mouse) and not self.show_bank_view
            pygame.draw.rect(self.screen, (71, 85, 105) if hover else (51, 65, 85), rect, border_radius=4)
            label = self.fit(f"[{i + 1}] {q['options'][i]}", self.font_sm, rect.w - 16)
            self.screen.blit(self.font_sm.render(label, True, (241, 245, 249)), (rect.x + 8, rect.y + 4))

        hint = ("Press [1-4] or click an option  |  [SPACE] Skip  |  [Q] Q&A Bank  |  "
                "Build: click two joints  ·  right-click a member to remove  ·  [T] Test")
        self.screen.blit(self.font_sm.render(self.fit(hint, self.font_sm, self.w - 64), True, (148, 163, 184)),
                         (32, top + 122))

    def draw_bank_overlay(self):
        rect = pygame.Rect(16, TAB_Y + TAB_H + 6, self.w - 32, self.h - (TAB_Y + TAB_H + 6) - 8)
        pygame.draw.rect(self.screen, (15, 23, 42), rect, border_radius=8)
        pygame.draw.rect(self.screen, (56, 189, 248), rect, 2, border_radius=8)
        x0, y = rect.x + 20, rect.y + 10
        text_w = rect.w - 40

        st = STAGES[self.current_stage - 1]
        subj = "All subjects" if self.subject is None else subject_name(self.subject)
        title = f"Q&A Bank: {self.level_name} - {subj}  ({len(self.bank_questions):,} questions)"
        self.screen.blit(self.font_lg.render(title, True, (56, 189, 248)), (x0, y))
        help_txt = ("[Left/Right] page  ·  [PgUp/PgDn] 50 pages  ·  [Home/End]  ·  click a subject above to filter  ·  "
                    "[Q] or [Esc] close")
        self.screen.blit(self.font_sm.render(help_txt, True, (148, 163, 184)), (x0, y + 24))
        y += 46

        start = self.bank_page * PER_PAGE
        half = text_w // 2
        for n, item in enumerate(self.bank_questions[start:start + PER_PAGE], start + 1):
            head = f"{n}. [{subject_name(item['subject'])}] {item['question']}"
            self.screen.blit(self.font.render(self.fit(head, self.font, text_w), True, (248, 250, 252)), (x0, y))
            for i, opt in enumerate(item["options"][:4]):
                ox, oy = x0 + 16 + (i % 2) * half, y + 19 + (i // 2) * 16
                right = i == item["correct_idx"]
                label = self.fit(f"{'ABCD'[i]}: {opt}", self.font_sm, half - 28)
                surf = self.font_sm.render(label, True, (15, 23, 42) if right else (203, 213, 225))
                if right:
                    pygame.draw.rect(self.screen, (52, 211, 153),
                                     (ox - 4, oy, surf.get_width() + 8, surf.get_height()), border_radius=3)
                self.screen.blit(surf, (ox, oy))
            exp = item["explanation"] or "-"
            exp = self.fit(f"Answer: {item['answer']}  ·  Explanation: {exp}", self.font_sm, text_w - 16)
            self.screen.blit(self.font_sm.render(exp, True, (110, 231, 183)), (x0 + 16, y + 53))
            y += 76

        prev_r, next_r = self.page_btn_rects()
        for r, label, on in ((prev_r, "< Prev", self.bank_page > 0),
                             (next_r, "Next >", self.bank_page < self.bank_pages - 1)):
            pygame.draw.rect(self.screen, (2, 132, 199) if on else (51, 65, 85), r, border_radius=6)
            s = self.font.render(label, True, (255, 255, 255) if on else (148, 163, 184))
            self.screen.blit(s, s.get_rect(center=r.center))
        page = self.font.render(f"Page {self.bank_page + 1:,} of {self.bank_pages:,}", True, (255, 255, 255))
        self.screen.blit(page, page.get_rect(center=(self.w // 2, prev_r.centery)))

    # ---------- input ----------
    def set_page(self, page):
        self.bank_page = max(0, min(self.bank_pages - 1, page))

    def tool_action(self, action, value):
        pid = self.current_stage
        if action == "mat":
            self.material[pid] = value
        elif action == "size":
            self.size[pid] = value
        elif action == "test":
            self.start_test()
        elif action == "clear":
            self.clear()
        elif action == "undo":
            self.undo()

    def on_click(self, mx, my, button=1):
        if button == 1 and self.bank_btn_rect().collidepoint(mx, my):
            self.show_bank_view = not self.show_bank_view
            return
        if button == 1 and self.back_btn_rect().collidepoint(mx, my):
            self.to_world()
            return
        if button == 1 and TAB_Y <= my <= TAB_Y + TAB_H:
            for r, subj, _ in self.subject_chips():
                if r.collidepoint(mx, my):
                    self.set_subject(subj)
            return
        if self.show_bank_view:
            prev_r, next_r = self.page_btn_rects()
            if prev_r.collidepoint(mx, my):
                self.set_page(self.bank_page - 1)
            elif next_r.collidepoint(mx, my):
                self.set_page(self.bank_page + 1)
            return
        if button == 1:
            for i, rect in enumerate(self.option_rects()):
                if rect.collidepoint(mx, my):
                    self.submit_answer(i)
                    return
        if self.test and self.test["status"] == "running":
            return
        if button == 1:
            for r, (action, value), *_ in self.tool_buttons():
                if r.collidepoint(mx, my):
                    self.tool_action(action, value)
                    return
        if CANVAS_TOP <= my < self.h - 150:
            if button == 3:
                self.remove_member_at(mx, my)
            elif button == 1:
                k = self.joint_at(mx, my)
                if k is not None:
                    self.click_joint(k)
                else:
                    self.selected = None

    def on_key(self, key):
        if key == pygame.K_q:
            self.show_bank_view = not self.show_bank_view
        elif key == pygame.K_ESCAPE:
            if self.show_bank_view:
                self.show_bank_view = False
            elif self.selected is not None:
                self.selected = None
            else:
                self.to_world()
        elif self.show_bank_view:
            step = {pygame.K_RIGHT: 1, pygame.K_LEFT: -1, pygame.K_PAGEDOWN: 50, pygame.K_PAGEUP: -50}
            if key in step:
                self.set_page(self.bank_page + step[key])
            elif key == pygame.K_HOME:
                self.set_page(0)
            elif key == pygame.K_END:
                self.set_page(self.bank_pages - 1)
        else:
            answers = {pygame.K_1: 0, pygame.K_KP1: 0, pygame.K_2: 1, pygame.K_KP2: 1,
                       pygame.K_3: 2, pygame.K_KP3: 2, pygame.K_4: 3, pygame.K_KP4: 3}
            running = self.test and self.test["status"] == "running"
            if key in answers:
                self.submit_answer(answers[key])
            elif key == pygame.K_SPACE:
                self.next_question()
                self.feedback_msg = ""
            elif key == pygame.K_t and not running:
                self.start_test()
            elif key == pygame.K_u and not running:
                self.undo()

    def world_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.world.on_down(*event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.world.on_motion(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.world.on_up(*event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            self.world.scroll(-(event.y or event.x) * 120)
        elif event.type == pygame.KEYDOWN:
            self.world.on_key(event.key)

    def draw_frame(self, dt):
        self.screen.fill((11, 17, 32))
        if self.mode == "world":
            self.world.draw()
            self.draw_hud()
            return
        self.step_test(dt)
        self.draw_build()
        self.draw_toolbar()
        self.draw_checkpoint_card()
        if self.show_bank_view:
            self.draw_bank_overlay()
        self.draw_hud()

    async def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.mode == "world":
                    self.world_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                    self.on_click(*event.pos, button=event.button)
                elif event.type == pygame.MOUSEWHEEL and self.show_bank_view:
                    self.set_page(self.bank_page - event.y)
                elif event.type == pygame.KEYDOWN:
                    self.on_key(event.key)

            self.draw_frame(dt)
            pygame.display.flip()
            await asyncio.sleep(0)         # lets pygbag's browser loop breathe


if __name__ == "__main__":
    asyncio.run(App().run())
