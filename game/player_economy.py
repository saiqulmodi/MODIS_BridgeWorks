"""Player profile management and scoring economy rules:
- Reading content: 1 mark/rupee
- Answering/Attempting: 2 marks/rupees
- First-attempt correct answer bonus: 10 marks/rupees
- Registration: Name only mandatory; phone and email optional.
"""

class PlayerProfile:
    def __init__(self, name, phone="", email=""):
        self.name = name.strip()
        self.phone = phone.strip()
        self.email = email.strip()
        self.balance_rupees = 0
        self.read_items = set()          # Track read items for 1 rupee each
        self.attempted_questions = set()  # Track attempted questions

    def read_content(self, content_id):
        """Rule 1: Earn 1 mark/rupee for reading content (once per item)."""
        if content_id not in self.read_items:
            self.read_items.add(content_id)
            self.balance_rupees += 1

    def submit_answer(self, q_id, is_correct):
        """Rule 2 & 3: Answering grants 2 marks/rupees. First-attempt correct adds 10 bonus marks/rupees."""
        # 2 marks/rupees for answering/attempting
        self.balance_rupees += 2
        
        is_first_attempt = q_id not in self.attempted_questions
        if is_first_attempt:
            self.attempted_questions.add(q_id)
            if is_correct:
                self.balance_rupees += 10  # First-attempt correct bonus

