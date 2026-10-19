"""Random question order that keeps look-alike questions apart.

Questions written together often share a template ("A beam of 4 m..." / "A beam of 6 m..."), so showing
them in bank order (or plain random order) can put near-twins back to back. Two questions count as
look-alikes when they start with the same five words, or share at least half of their words; numbers
are ignored, so changing only the numbers does not make a question new. The last few questions shown
(on any screen) are remembered for this session.
"""
import random
import re
from collections import deque

WINDOW = 6                      # a new question must not look like any of the last 6 shown
_RECENT = deque(maxlen=WINDOW)
_WORD = re.compile(r"[^\W\d_]+")


def text_of(record):
    """The English question text of a record (dict with "question"), or the string itself."""
    return record.get("question", "") if isinstance(record, dict) else str(record)


def signature(text):
    words = _WORD.findall(text.lower())
    return frozenset(words), tuple(words[:5])


def look_alike(a, b):
    (wa, sa), (wb, sb) = a, b
    if sa and sa == sb:
        return True
    if not wa or not wb:
        return False
    return len(wa & wb) / len(wa | wb) >= 0.5


def remember(record):
    """Note a question as shown so the next picks keep away from it."""
    _RECENT.append(signature(text_of(record)))


def recent():
    return list(_RECENT)


def pick(candidates, rng=random, avoid=None):
    """A random candidate that looks like none of the recently shown questions (or of `avoid`).

    Falls back to the candidate that looks like the fewest of them, so a pick is always made."""
    cands = list(candidates)
    if not cands:
        return None
    rng.shuffle(cands)
    seen = list(_RECENT) + [signature(text_of(r)) for r in (avoid or [])]
    best, best_hits = None, None
    for c in cands[:400]:
        sig = signature(text_of(c))
        hits = sum(look_alike(sig, s) for s in seen)
        if hits == 0:
            return c
        if best_hits is None or hits < best_hits:
            best, best_hits = c, hits
    return best


def order(items, rng=random, window=WINDOW):
    """A whole sequence in random order with look-alikes at least `window` places apart where possible."""
    rest = list(items)
    rng.shuffle(rest)
    out, sigs = [], []
    while rest:
        last = sigs[-window:]
        k = next((i for i, r in enumerate(rest[:400]) if not any(look_alike(signature(text_of(r)), s) for s in last)), 0)
        r = rest.pop(k)
        out.append(r)
        sigs.append(signature(text_of(r)))
    return out
