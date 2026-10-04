"""BridgeWorks Academy: the question bank in its public record format, rewards and export.

Record format (one dict per question):
    {"id": int, "class_level": 1-12, "subject": "physics"|"chemistry"|"math"|"biology"|
     "finance"|"commercials", "question": str, "options": [4 str], "correct_idx": 0-3,
     "explanation": str, "grant_reward": float,
     "question_bn": str, "options_bn": [4 str], "explanation_bn": str}

ids are class_level * 10000 + subject number * 1000 + position (1-based), so they never
change when more questions are added. `python -m engine.academy_data out.json` exports the
whole bank as JSON for an external quiz engine or a SQLite import.
"""
import importlib
import json
import sys

from .academy import CLASSES, SUBJECTS

GRANT_PER_CLASS = 1000.0       # a correct first answer in Class n earns Rs 1000 x n
READING_BONUS = 200.0          # reading the explanation to the end (right or wrong)
HELP_READ_REWARD = 500.0       # reading one Help answer to the end, once
TARGET_PER_SUBJECT = 100

_cache = {}


def grant_reward(class_level):
    return GRANT_PER_CLASS * class_level


def record(qid, class_level, subject, m, reward):
    """One question in the public format. The options are rotated by the id so the right
    answer sits in every position equally often (the screen also shuffles them each time)."""
    turn = qid % 4
    order = [(i + turn) % 4 for i in range(4)]
    return dict(id=qid, class_level=class_level, subject=subject, question=m.question,
                options=[m.options[i] for i in order], correct_idx=order.index(m.correct_idx),
                explanation=m.explanation, grant_reward=reward, question_bn=m.question_bn,
                options_bn=[m.options_bn[i] for i in order], explanation_bn=m.explanation_bn)


def module_name(class_level, subject):
    return f"engine.academy.c{class_level:02d}_{subject}"


def items(class_level, subject):
    """Records for one class and subject ([] when that batch is not written yet)."""
    key = (class_level, subject)
    if key not in _cache:
        try:
            mod = importlib.import_module(module_name(class_level, subject))
            raw = mod.ITEMS
        except ModuleNotFoundError:
            raw = ()
        s = SUBJECTS.index(subject) + 1
        _cache[key] = [record(class_level * 10000 + s * 1000 + k + 1, class_level, subject, m,
                              grant_reward(class_level)) for k, m in enumerate(raw)]
    return _cache[key]


def all_items():
    return [r for c in CLASSES for s in SUBJECTS for r in items(c, s)]


def by_id(qid):
    c, rest = divmod(qid, 10000)
    s = rest // 1000
    if not (1 <= c <= 12 and 1 <= s <= len(SUBJECTS)):
        return None
    for r in items(c, SUBJECTS[s - 1]):
        if r["id"] == qid:
            return r
    return None


def coverage():
    """{(class, subject): number of questions written} - progress towards 7,200."""
    return {(c, s): len(items(c, s)) for c in CLASSES for s in SUBJECTS}


def export_json(path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_items(), f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    export_json(sys.argv[1] if len(sys.argv) > 1 else "academy.json")
