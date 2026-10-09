"""Player profile and economy tracker for rewards.

Rules:
  - Reading an item pays 1 Rs, once per item.
  - Every answer attempt pays 2 Rs.
  - The first correct answer to an item pays 100 Rs (once per item, so repeats cannot farm it).
"""

READ_REWARD = 1
ATTEMPT_REWARD = 2
CORRECT_REWARD = 100


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
        self.attempted_items.add(content_id)
        if is_correct and content_id not in self.completed_questions:
            earned += CORRECT_REWARD
            self.completed_questions.add(content_id)
        self.balance_rupees += earned
        return earned
