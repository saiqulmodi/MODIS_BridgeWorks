"""Player profile and economy tracker for rewards.

Rules:
  - Reading an item pays 1 Rs, once per item.
  - Every answer attempt pays 2 Rs.
  - A correct answer on the first attempt at an item pays a 10 Rs bonus.
"""

READ_REWARD = 1
ATTEMPT_REWARD = 2
FIRST_TRY_BONUS = 10


class PlayerProfile:
    def __init__(self, name, phone="", email=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.balance_rupees = 0
        self.read_items = set()
        self.attempted_items = set()
        self.completed_questions = set()

    @property
    def rupees(self):
        return self.balance_rupees

    def read_content(self, content_id):
        if content_id in self.read_items:
            return 0
        self.read_items.add(content_id)
        self.balance_rupees += READ_REWARD
        return READ_REWARD

    def submit_answer(self, content_id, is_correct):
        earned = ATTEMPT_REWARD
        if is_correct and content_id not in self.attempted_items:
            earned += FIRST_TRY_BONUS
        self.attempted_items.add(content_id)
        if is_correct:
            self.completed_questions.add(content_id)
        self.balance_rupees += earned
        return earned
