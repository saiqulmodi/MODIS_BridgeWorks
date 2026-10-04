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

    # --- BridgeWorks Academy: Civil Grant wallet and what has been answered / read -------------
    @property
    def academy(self):
        a = self.data.setdefault("academy", {})
        a.setdefault("wallet", 0.0)          # Civil Grants not yet spent, Rs
        a.setdefault("earned", 0.0)          # all grants ever earned, Rs
        a.setdefault("class", 5)             # the class the student studies in
        a.setdefault("answered", {})         # question id -> True if right on the first try
        a.setdefault("explained", [])        # ids whose explanation earned the reading bonus
        a.setdefault("read_help", [])        # Help answers read to the end ("start:3", "truss:12")
        return a

    @property
    def wallet(self):
        return self.academy["wallet"]

    def add_grant(self, amount):
        a = self.academy
        a["wallet"] += amount
        a["earned"] += amount
        self.write()

    def spend_grant(self, amount):
        a = self.academy
        used = max(0.0, min(amount, a["wallet"]))
        a["wallet"] -= used
        self.write()
        return used

    def refund_grant(self, amount):
        """A grant committed to a build that did not succeed goes back to the wallet."""
        self.academy["wallet"] += amount
        self.write()

    def answer_question(self, qid, correct, reward):
        """First attempt at a question decides its grant; later attempts are practice.
        Returns the grant paid now."""
        a = self.academy
        key = str(qid)
        if key in a["answered"]:
            return 0.0
        a["answered"][key] = bool(correct)
        paid = reward if correct else 0.0
        if paid:
            self.add_grant(paid)
        else:
            self.write()
        return paid

    def explanation_read(self, qid, bonus):
        a = self.academy
        if qid in a["explained"]:
            return 0.0
        a["explained"].append(qid)
        self.add_grant(bonus)
        return bonus

    def help_read(self, key, reward):
        a = self.academy
        if key in a["read_help"]:
            return 0.0
        a["read_help"].append(key)
        self.add_grant(reward)
        return reward

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
