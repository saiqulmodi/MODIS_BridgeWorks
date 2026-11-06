import json
import random
from collections import deque
from pathlib import Path

class QuestionManager:
    def __init__(self, data_file="data/questions.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
        self.recent_subtopics = deque(maxlen=10)
        self.recent_types = deque(maxlen=3)
        self.served_ids = set()

    def _load_data(self):
        if not self.data_file.exists():
            return {}
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def get_classes(self):
        return list(self.data.keys())

    def get_subjects(self, class_name):
        questions = self.data.get(class_name, [])
        return sorted(list({q.get("subject", "General") for q in questions if "subject" in q}))

    def get_next_question(self, class_name, subject=None):
        pool = self.data.get(class_name, [])
        if subject:
            pool = [q for q in pool if q.get("subject") == subject]
        if not pool:
            return None

        available = [q for q in pool if q.get("id") not in self.served_ids]
        if not available:
            self.served_ids.clear()
            available = pool

        diverse_pool = [
            q for q in available
            if q.get("subtopic") not in self.recent_subtopics
            and q.get("question_type") not in self.recent_types
        ]

        if not diverse_pool:
            diverse_pool = [
                q for q in available
                if q.get("subtopic") not in self.recent_subtopics
            ]

        selected = random.choice(diverse_pool if diverse_pool else available)

        self.served_ids.add(selected.get("id"))
        if "subtopic" in selected:
            self.recent_subtopics.append(selected["subtopic"])
        if "question_type" in selected:
            self.recent_types.append(selected["question_type"])

        return selected
