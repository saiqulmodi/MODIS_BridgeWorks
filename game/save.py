"""Progress file: stars, EXP and the last few designs per level (for the Pareto chart)."""
import json
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "save.json")
UNLOCK_ALL = True      # every level open, so the whole game can be reviewed in any order


class Save:
    def __init__(self, path=PATH):
        self.path = path
        self.data = {"exp": 0, "levels": {}, "lang": "en"}
        try:
            with open(path, encoding="utf-8") as f:
                self.data.update(json.load(f))
        except (OSError, ValueError):
            pass

    def level(self, num):
        return self.data["levels"].setdefault(str(num), {"stars": 0, "attempts": [],
                                                          "salvage": 0.0, "done": False})

    @property
    def exp(self):
        return self.data["exp"]

    def add_exp(self, n):
        self.data["exp"] += int(n)
        self.write()

    def record(self, num, stars, cost, safety, time_s, success):
        lv = self.level(num)
        lv["stars"] = max(lv["stars"], stars)
        lv["done"] = lv["done"] or success
        lv["attempts"].append({"cost": cost, "safety": safety, "time": time_s, "ok": success})
        lv["attempts"] = lv["attempts"][-20:]
        self.write()

    def unlocked(self, num):
        if UNLOCK_ALL or num == 1:
            return True
        return self.level(num - 1)["done"]

    def write(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=1)
        except OSError:
            pass
