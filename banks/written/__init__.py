"""Questions written fresh for BridgeWorks and FAILSPAN (not generated from templates).

Each batch file bNNN_*.py has LEVEL, SUBJECT and ITEMS = [(chapter, question, [right, wrong, wrong, wrong], explanation)].
The right answer is written first; load() places it at a fixed but mixed position (seeded by the question text),
so the answer letter does not follow a pattern. Batches load in file-name order and new batches only ever come
after older ones, so the games can append them without moving saved-progress row numbers.

Both exports (tools/export_web.py here, FAILSPAN tools/export_bank.py) drop a written question that is already in
the game or near-same to one kept in that class and subject, the same quality rule as the rest of the bank.
"""
import hashlib
import importlib
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
NEAR = 0.8                                   # same near-same line as game/question_bank.quality()
_WORDS = re.compile(r"[^\W\d_]+")


class Gate:
    """Keeps a written question only if nothing like it is in the game yet.

    seen: lower-case texts of every question in the game (any class); kept: (class, subject) -> texts kept there."""

    def __init__(self, seen, kept):
        self.seen = set(seen)
        self.kinds, self.words = {}, {}
        for key, texts in kept.items():
            for t in texts:
                self._add(key, t)

    def _add(self, key, text):
        self.kinds.setdefault(key, set()).add(" ".join(_WORDS.findall(text.lower())))
        self.words.setdefault(key, []).append(frozenset(_WORDS.findall(text.lower())))

    def ok(self, level, subject, text):
        key, low = (level, subject), text.strip().lower()
        kind, words = " ".join(_WORDS.findall(low)), frozenset(_WORDS.findall(low))
        if low in self.seen or kind in self.kinds.get(key, ()):
            return False
        if words and any(len(words & w) / len(words | w) >= NEAR for w in self.words.get(key, [])):
            return False
        self.seen.add(low)
        self._add(key, text)
        return True


def _mix(question, options):
    rnd = random.Random(int(hashlib.md5(question.encode("utf-8")).hexdigest()[:8], 16))
    order = list(range(4))
    rnd.shuffle(order)
    return [options[k] for k in order], order.index(0)


def load():
    """-> list of dicts: class_level, subject, chapter, question, options, correct_idx, explanation (batch order)."""
    out = []
    for name in sorted(f[:-3] for f in os.listdir(HERE) if f.startswith("b") and f.endswith(".py")):
        mod = importlib.import_module(f"banks.written.{name}")
        for chapter, q, opts, expl in mod.ITEMS:
            assert len(opts) == 4 and len(set(opts)) == 4, (name, q)
            options, right = _mix(q, opts)
            out.append({"class_level": mod.LEVEL, "subject": mod.SUBJECT, "chapter": chapter, "question": q,
                        "options": options, "correct_idx": right, "explanation": expl, "batch": name})
    return out
