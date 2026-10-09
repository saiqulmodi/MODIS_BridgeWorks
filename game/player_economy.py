"""Player profile and economy tracker for rewards.

Rules:
  - Reading an item pays 1 Rs, once per item.
  - Every answer attempt pays 2 Rs.
  - The first correct answer to an item pays 100 Rs (once per item, so repeats cannot farm it).
  - At most 25 answers a day, in any phase (engine.daily_limit). The count is kept in the save
    file, so logging in again does not give another 25.

With save data (the game's save.json dict) the profile is stored under "ncert_players" by name,
so the balance and the already-paid questions survive a restart or a new login.
"""
from engine import daily_limit

READ_REWARD = 1
ATTEMPT_REWARD = 2
CORRECT_REWARD = 100


class PlayerProfile:
    def __init__(self, name, phone="", email="", data=None, on_change=None, today=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.data = {} if data is None else data
        self.on_change = on_change
        self.today = today
        rec = self.data.setdefault("ncert_players", {}).setdefault(name.strip().lower(), {})
        rec.update(name=name, phone=phone or rec.get("phone", ""), email=email or rec.get("email", ""))
        rec.setdefault("balance", 0)
        self.rec = rec
        self.read_items = set(rec.get("read", []))
        self.attempted_items = set(rec.get("attempted", []))
        self.completed_questions = set(rec.get("completed", []))

    @property
    def balance_rupees(self):
        return self.rec["balance"]

    @property
    def rupees(self):
        return self.balance_rupees

    def answers_left(self):
        return daily_limit.answers_left(self.data, self.today)

    def _store(self):
        self.rec["read"] = sorted(self.read_items)
        self.rec["attempted"] = sorted(self.attempted_items)
        self.rec["completed"] = sorted(self.completed_questions)
        if self.on_change:
            self.on_change()

    def read_content(self, content_id):
        if content_id in self.read_items:
            return 0
        self.read_items.add(content_id)
        self.rec["balance"] += READ_REWARD
        self._store()
        return READ_REWARD

    def submit_answer(self, content_id, is_correct):
        """Pay for one answer. Returns the rupees paid, or None when today's 25 are used up."""
        if not daily_limit.use_answer(self.data, self.today):
            return None
        earned = ATTEMPT_REWARD
        self.attempted_items.add(content_id)
        if is_correct and content_id not in self.completed_questions:
            earned += CORRECT_REWARD
            self.completed_questions.add(content_id)
        self.rec["balance"] += earned
        self._store()
        return earned
