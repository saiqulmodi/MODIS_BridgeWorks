"""
The Campus World: one building per level along a long road, wide apart, in
five zones (one per bridge project). Click a building to enter that class -
its own question bank, its own subjects and its own bridge to build.
"""
import pygame

# (level code, building name). Codes 13/14 match the Academy (NIT/IIT); 15/16 are new levels.
LEVELS = [(n, f"Class {n}") for n in range(1, 13)] + [(15, "BE"), (13, "NIT"), (14, "IIT"),
                                                       (16, "Expert Engineer")]
LEVEL_NAMES = dict(LEVELS)
SHORT = {15: "BE", 13: "NIT", 14: "IIT", 16: "EXP"}

SUBJECT_NAMES = {"math": "Math", "physics": "Physics", "chemistry": "Chemistry", "biology": "Biology",
                 "evs": "EVS", "commercials": "Commerce", "economics": "Economics", "finance": "Finance",
                 "geography": "Geography", "general_safety": "Safety", "civil": "Civil Engg",
                 "engineering": "Engineering", "computer": "Computer", "bridge": "Bridge"}

ZONE_COLOURS = [(20, 54, 44), (24, 44, 72), (52, 34, 70), (70, 44, 28), (72, 28, 40)]
SPACING, BLD_W, MARGIN, RIVER_W = 300, 170, 200, 120


def tier_of(level):
    """Bridge project (1-5) for a level."""
    if level <= 7:
        return 1
    if level <= 10:
        return 2
    if level <= 12:
        return 3
    return 4 if level in (13, 15) else 5


def subject_name(s):
    return SUBJECT_NAMES.get(s, s.replace("_", " ").title())


class World:
    def __init__(self, app):
        self.app = app
        self.cam_x = 0.0
        self.drag = None             # (mouse x at press, cam_x at press, moved?)
        self.slots = self._layout()

    def _layout(self):
        """[(level, world x of the building's left edge)] with a river between zones."""
        x, out, last_tier = MARGIN, [], tier_of(LEVELS[0][0])
        for level, _ in LEVELS:
            if tier_of(level) != last_tier:
                x += RIVER_W
                last_tier = tier_of(level)
            out.append((level, x))
            x += SPACING
        self.width = x + MARGIN
        return out

    @property
    def road_y(self):
        return self.app.h - 96

    def clamp(self):
        self.cam_x = max(0.0, min(self.width - self.app.w, self.cam_x))

    def scroll(self, dx):
        self.cam_x += dx
        self.clamp()

    def focus(self, level):
        for lv, x in self.slots:
            if lv == level:
                self.cam_x = x + BLD_W / 2 - self.app.w / 2
        self.clamp()

    def building_rect(self, level, x):
        rank = [lv for lv, _ in LEVELS].index(level)
        h = 120 + rank * 9
        return pygame.Rect(int(x - self.cam_x), self.road_y - 14 - h, BLD_W, h)

    def building_at(self, mx, my):
        for level, x in self.slots:
            if self.building_rect(level, x).inflate(0, 40).collidepoint(mx, my):
                return level
        return None

    def minimap_rects(self):
        n = len(LEVELS)
        w = (self.app.w - 32) // n
        return [(level, pygame.Rect(16 + k * w, self.app.h - 30, w - 4, 22)) for k, (level, _) in enumerate(LEVELS)]

    # ---------- input ----------
    def on_down(self, mx, my):
        self.drag = (mx, self.cam_x, False)

    def on_motion(self, mx):
        if self.drag:
            x0, cam0, moved = self.drag
            if abs(mx - x0) > 5 or moved:
                self.drag = (x0, cam0, True)
                self.cam_x = cam0 - (mx - x0)
                self.clamp()

    def on_up(self, mx, my):
        moved = self.drag and self.drag[2]
        self.drag = None
        if moved:
            return
        for level, r in self.minimap_rects():
            if r.collidepoint(mx, my):
                self.app.enter_level(level)
                return
        level = self.building_at(mx, my)
        if level is not None:
            self.app.enter_level(level)

    def on_key(self, key):
        step = {pygame.K_LEFT: -SPACING, pygame.K_a: -SPACING, pygame.K_RIGHT: SPACING, pygame.K_d: SPACING}
        if key in step:
            self.scroll(step[key])
        elif key == pygame.K_HOME:
            self.cam_x = 0
        elif key == pygame.K_END:
            self.cam_x = self.width
            self.clamp()

    # ---------- drawing ----------
    def draw(self):
        app, scr = self.app, self.app.screen
        top, ry = 88, self.road_y
        # sky and zone bands
        pygame.draw.rect(scr, (12, 20, 38), (0, top, app.w, ry - top))
        zones = {}
        for level, x in self.slots:
            t = tier_of(level)
            x0, x1 = zones.get(t, (x, x))
            zones[t] = (min(x0, x), max(x1, x + BLD_W))
        for t, (x0, x1) in zones.items():
            r = pygame.Rect(int(x0 - 60 - self.cam_x), top, int(x1 - x0 + 120), ry - top)
            pygame.draw.rect(scr, ZONE_COLOURS[t - 1], r)
            st = app.stages[t - 1]
            label = app.font.render(f"Project {t}: {st['name']}  ·  {st['class']}", True, (226, 232, 240))
            scr.blit(label, (r.x + 14, top + 8))

        # ground, road and rivers with a bridge of the next zone's type
        pygame.draw.rect(scr, (40, 32, 24), (0, ry, app.w, app.h - ry))
        pygame.draw.rect(scr, (51, 65, 85), (0, ry - 8, app.w, 26))
        for k in range(-1, app.w // 40 + 2):
            dx = int(k * 40 - self.cam_x % 40)
            pygame.draw.line(scr, (250, 204, 21), (dx, ry + 5), (dx + 20, ry + 5), 2)
        prev = None
        for level, x in self.slots:
            t = tier_of(level)
            if prev is not None and t != prev[0]:
                rx = int(prev[1] + SPACING - (SPACING - BLD_W) / 2 - self.cam_x) + 10
                rw = RIVER_W + (SPACING - BLD_W) - 20
                pygame.draw.rect(scr, (8, 47, 73), (rx, ry + 18, rw, app.h - ry))
                pygame.draw.rect(scr, (8, 47, 73), (rx + 10, ry - 8, rw - 20, 26))
                self._mini_bridge(rx + 10, rw - 20, ry - 8, t)
            prev = (t, x)

        # buildings
        mouse = pygame.mouse.get_pos()
        hover = self.building_at(*mouse)
        for level, x in self.slots:
            r = self.building_rect(level, x)
            if r.right < -20 or r.x > app.w + 20:
                continue
            self._building(r, level, level == hover)

        # minimap
        for level, r in self.minimap_rects():
            d = app.designs[level]
            pygame.draw.rect(scr, (22, 163, 74) if d.complete else (30, 41, 59), r, border_radius=4)
            pygame.draw.rect(scr, ZONE_COLOURS[tier_of(level) - 1], r, 2, border_radius=4)
            s = app.font_sm.render(SHORT.get(level, str(level)), True, (241, 245, 249))
            scr.blit(s, s.get_rect(center=r.center))
        hint = "Drag, wheel or Left/Right to move along the road  ·  click a building (or a box below) to enter"
        s = app.font_sm.render(hint, True, (148, 163, 184))
        scr.blit(s, (16, app.h - 50))

    def _mini_bridge(self, x, w, y, tier):
        scr, col = self.app.screen, (203, 213, 225)
        pygame.draw.line(scr, col, (x, y), (x + w, y), 3)
        mid = x + w // 2
        if tier in (1, 4, 5):
            pygame.draw.line(scr, col, (mid, y + 14), (mid, y - 46), 3)
            for k in range(1, 6):
                pygame.draw.line(scr, col, (mid, y - 44), (x + k * w // 6, y), 1)
        elif tier == 2:
            for k in range(6):
                pygame.draw.line(scr, col, (x + k * w // 6, y), (x + (k + 1) * w // 6, y - 20 if k % 2 == 0 else y), 2)
            pygame.draw.line(scr, col, (x + w // 6, y - 20), (x + 5 * w // 6, y - 20), 2)
        else:
            pts = [(x + k * w // 10, y - int(36 * (1 - ((k - 5) / 5) ** 2))) for k in range(11)]
            pygame.draw.lines(scr, col, False, pts, 2)

    def _building(self, r, level, hover):
        app, scr = self.app, self.app.screen
        t = tier_of(level)
        body = tuple(min(255, c + 70) for c in ZONE_COLOURS[t - 1])
        pygame.draw.rect(scr, body, r, border_radius=4)
        pygame.draw.rect(scr, (250, 204, 21) if hover else (15, 23, 42), r, 3 if hover else 2, border_radius=4)
        pygame.draw.polygon(scr, tuple(c // 2 for c in body), [(r.x - 8, r.y), (r.centerx, r.y - 26), (r.right + 8, r.y)])
        for wy in range(r.y + 46, r.bottom - 34, 22):
            for wx in range(r.x + 16, r.right - 20, 30):
                pygame.draw.rect(scr, (253, 224, 71), (wx, wy, 14, 12))
        pygame.draw.rect(scr, (15, 23, 42), (r.centerx - 12, r.bottom - 30, 24, 30))      # door
        sign = pygame.Rect(r.x + 10, r.y + 8, r.w - 20, 30)
        pygame.draw.rect(scr, (15, 23, 42), sign, border_radius=4)
        name = app.font.render(LEVEL_NAMES[level], True, (255, 255, 255))
        scr.blit(name, name.get_rect(center=sign.center))

        count, subjects = app.level_stats.get(level, (0, 0))
        info = f"{count:,} Q  ·  {subjects} subjects" if count else "Questions coming"
        s = app.font_sm.render(info, True, (226, 232, 240))
        scr.blit(s, s.get_rect(midtop=(r.centerx, r.bottom + 20)))
        if app.designs[level].complete:
            s = app.font_sm.render("BRIDGE BUILT", True, (74, 222, 128))
            scr.blit(s, s.get_rect(midtop=(r.centerx, r.bottom + 34)))
        elif hover:
            s = app.font_sm.render("Click to enter", True, (250, 204, 21))
            scr.blit(s, s.get_rect(midtop=(r.centerx, r.bottom + 34)))
