import re

# 1. Create engineer_profile.py
profile_code = '''"""Engineer progression and visual profiles."""
class EngineerTier:
    TIERS = [
        {
            "title": "Trainee Apprentice",
            "min_exp": 0,
            "scale": 1.05,
            "helmet_color": (245, 185, 20),
            "shirt_color": (220, 225, 230),
            "vest_color": (255, 110, 0),
            "pants_color": (45, 55, 75),
            "boots_color": (75, 45, 20),
            "accessory": "none"
        },
        {
            "title": "Junior Site Technician",
            "min_exp": 500,
            "scale": 1.18,
            "helmet_color": (245, 245, 245),
            "shirt_color": (25, 75, 150),
            "vest_color": (215, 250, 0),
            "pants_color": (25, 75, 150),
            "boots_color": (35, 35, 35),
            "accessory": "toolbelt"
        },
        {
            "title": "Graduate Structural Engineer",
            "min_exp": 1500,
            "scale": 1.32,
            "helmet_color": (255, 255, 255),
            "shirt_color": (30, 45, 70),
            "vest_color": (235, 235, 235),
            "pants_color": (90, 85, 80),
            "boots_color": (25, 25, 25),
            "accessory": "clipboard_goggles"
        },
        {
            "title": "Chief Project Director",
            "min_exp": 3500,
            "scale": 1.48,
            "helmet_color": (240, 195, 60),
            "shirt_color": (20, 30, 48),
            "vest_color": (220, 40, 30),
            "pants_color": (35, 40, 50),
            "boots_color": (20, 20, 20),
            "accessory": "blueprint_tube"
        }
    ]

    @classmethod
    def get_tier(cls, exp: int) -> dict:
        cur = cls.TIERS[0]
        for t in cls.TIERS:
            if exp >= t["min_exp"]:
                cur = t
            else:
                break
        return cur
'''
with open("game/engineer_profile.py", "w", encoding="utf-8") as f:
    f.write(profile_code)

# 2. Update game/scenes/campus.py
with open("game/scenes/campus.py", "r", encoding="utf-8") as f:
    campus = f.read()

if "from game.engineer_profile import EngineerTier" not in campus:
    campus = "from game.engineer_profile import EngineerTier\n" + campus

new_draw = '''    def draw_player(self, s):
        p = self.player
        cam = self.cam
        px, py, pz = p.pos
        sh = cam.project((px, self.floor_under() + 0.03, pz))
        if sh:
            r = max(3, int(cam.focal * 0.7 / sh[2]))
            shadow = pygame.Surface((2 * r, r), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
            s.blit(shadow, (sh[0] - r, sh[1] - r // 2))

        foot = cam.project((px, py, pz))
        if not foot:
            return

        exp = getattr(self, "exp", 0)
        tier = EngineerTier.get_tier(exp)
        sc = (cam.focal / foot[2]) * tier.get("scale", 1.0)

        def P(dx, dy, dz=0.0):
            hx, _, hz = p.heading
            rx, rz = hz, -hx
            q = cam.project((px + rx * dx + hx * dz, py + dy, pz + rz * dx + hz * dz))
            return q[:2] if q else foot[:2]

        swing = math.sin(p.walk_phase * 2.2) * (0.4 if p.grounded else 0.15)
        hip, neck, head = P(0, 0.95), P(0, 1.45), P(0, 1.70)
        lw = max(3, int(0.18 * sc))

        if p.gliding:
            pygame.draw.polygon(s, (140, 70, 210), [
                P(-0.25, 1.45, -0.1), P(0.25, 1.45, -0.1),
                P(0.9, 0.5, -0.8), P(-0.9, 0.5, -0.8)
            ])

        if tier.get("accessory") == "blueprint_tube":
            tube_top = P(-0.25, 1.75, -0.12)
            tube_bot = P(0.22, 1.05, -0.12)
            pygame.draw.line(s, (35, 40, 45), tube_top, tube_bot, max(4, int(0.14 * sc)))
            pygame.draw.circle(s, (220, 185, 45), tube_top, max(2, int(0.06 * sc)))

        pants_col = tier["pants_color"]
        boot_col = tier["boots_color"]
        l_foot = P(-0.16, 0.0, swing)
        r_foot = P(0.16, 0.0, -swing)
        pygame.draw.line(s, pants_col, hip, l_foot, lw)
        pygame.draw.line(s, pants_col, hip, r_foot, lw)
        pygame.draw.circle(s, boot_col, l_foot, max(3, int(0.11 * sc)))
        pygame.draw.circle(s, boot_col, r_foot, max(3, int(0.11 * sc)))

        torso_w = max(5, int(0.36 * sc))
        pygame.draw.line(s, tier["shirt_color"], hip, neck, torso_w)
        vest_w = max(4, int(0.34 * sc))
        mid_spine = P(0, 1.20)
        pygame.draw.line(s, tier["vest_color"], mid_spine, neck, vest_w)
        pygame.draw.line(s, (250, 250, 250), P(-0.16, 1.25), P(0.16, 1.25), max(2, int(0.06 * sc)))

        if tier.get("accessory") in ("toolbelt", "clipboard_goggles", "blueprint_tube"):
            pygame.draw.line(s, (45, 30, 15), P(-0.19, 0.96), P(0.19, 0.96), max(3, int(0.08 * sc)))
            pygame.draw.rect(s, (210, 190, 60), (hip[0] - 3, hip[1] - 3, 6, 6))

        shirt_col = tier["shirt_color"]
        if p.rope is not None:
            hand = P(0.1, 2.0)
            a = cam.project(p.rope[0])
            if a:
                pygame.draw.line(s, (255, 255, 255), hand, a[:2], 2)
                pygame.draw.circle(s, (255, 220, 60), a[:2], 5)
            pygame.draw.line(s, shirt_col, neck, hand, lw)
            pygame.draw.line(s, shirt_col, neck, P(-0.35, 1.0, 0.2), lw)
        elif p.zip is not None and len(p.zip) > 4:
            hand = P(0.1, 2.0)
            a = cam.project(p.zip[4])
            if a:
                pygame.draw.line(s, (255, 255, 255), hand, a[:2], 2)
                for k in range(6):
                    ang = k * 3.14159 / 3
                    pygame.draw.line(s, (255, 255, 255), a[:2],
                                     (a[0] + 9 * math.cos(ang), a[1] + 9 * math.sin(ang)), 1)
            pygame.draw.line(s, shirt_col, neck, hand, lw)
            pygame.draw.line(s, shirt_col, neck, P(-0.35, 1.0, 0.2), lw)
        elif p.zip is not None:
            pygame.draw.line(s, shirt_col, neck, P(-0.4, 1.9), lw)
            pygame.draw.line(s, shirt_col, neck, P(0.4, 1.9), lw)
        else:
            pygame.draw.line(s, shirt_col, neck, P(-0.32, 1.0, -swing), lw)
            pygame.draw.line(s, shirt_col, neck, P(0.32, 1.0, swing), lw)

        hr = max(3, int(0.20 * sc))
        pygame.draw.circle(s, (230, 185, 145), head, hr)
        helmet_col = tier["helmet_color"]
        pygame.draw.circle(s, helmet_col, (head[0], head[1] - hr * 0.35), int(hr * 1.08),
                           draw_top_right=True, draw_top_left=True)
        pygame.draw.line(s, helmet_col, (head[0] - hr * 1.35, head[1] - hr * 0.3),
                         (head[0] + hr * 1.35, head[1] - hr * 0.3), max(2, hr // 3))

        if p.splash > 0:
            for k in range(6):
                a = k / 6 * math.tau + self.t * 3
                q = P(math.cos(a) * 0.9, 0.3 + 0.8 * p.splash / 2.5, math.sin(a) * 0.9)
                pygame.draw.circle(s, (180, 220, 255), q, max(2, int(0.1 * sc)))'''

campus = re.sub(r'    def draw_player\(self, s\):.*?(?=\n    def draw_anchor)', new_draw, campus, flags=re.DOTALL)

with open("game/scenes/campus.py", "w", encoding="utf-8") as f:
    f.write(campus)

print("Applied cleanly!")