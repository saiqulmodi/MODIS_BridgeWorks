"""Engineer progression and visual profiles."""
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
