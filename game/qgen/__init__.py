"""
Question generators for the core bank (banks/core/).

Numerical questions are built from templates: the numbers are drawn at random
(fixed seed, so the bank is the same every build) and the answer is computed,
so it is always right. Wrong options come from the usual mistakes (forgetting a
factor, mixing up a formula) where possible. Concept questions are written out
by hand as (question, answer, three wrong options, explanation).

Levels: 1-12 = Class 1-12, 13 = NIT (JEE Main), 14 = IIT (JEE Advanced /
Olympiad), 15 = BE (engineering degree), 16 = Expert Engineer.

    python -m game.qgen        # write banks/core/*.json, then rebuild data/questions.json
"""
import math
import random

TEMPLATES = []          # (levels, subject, count, func)
FACTS = []              # (levels, subject, rows)
BALANCE = {"computer": 120}     # subjects given the same number of questions at every level


def template(levels, subject, count=20):
    """Register func(rng, level) -> (question, answer, [wrong...], explanation)."""
    def deco(func):
        TEMPLATES.append((tuple(levels), subject, count, func))
        return func
    return deco


def facts(levels, subject, rows):
    """rows: [(question, answer, [wrong, wrong, wrong], explanation)], easiest first.

    Each row goes to ONE level: the rows are split in order across the levels given,
    so the earlier (easier) rows land in the lower class."""
    levels = tuple(levels)
    for k, row in enumerate(rows):
        FACTS.append(((levels[k * len(levels) // len(rows)],), subject, [row]))


def fmt(x, sig=3):
    """Readable number: whole numbers stay whole, others get `sig` significant figures."""
    if isinstance(x, str):
        return x
    if x == 0:
        return "0"
    if abs(x - round(x)) < 1e-9 and abs(x) < 1e12:
        n = int(round(x))
        return f"{n:,}" if abs(n) >= 10000 else str(n)
    digits = max(0, sig - 1 - int(math.floor(math.log10(abs(x)))))
    s = f"{x:.{digits}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def unit(x, u, sig=3):
    return f"{fmt(x, sig)} {u}".strip()


def near(x, rng, u="", factors=(2, 0.5, 1.5, 0.75, 1.25, 4, 0.25, 3, 10, 0.1), sig=3):
    """Plausible wrong numbers around x (as formatted strings)."""
    out = []
    fs = list(factors)
    rng.shuffle(fs)
    for f in fs:
        out.append(unit(x * f, u, sig))
    return out


def options(answer, wrong, rng):
    """Four distinct options with the answer at a random place, or None."""
    seen, opts = {answer}, [answer]
    for w in wrong:
        if w not in seen and w.strip():
            seen.add(w)
            opts.append(w)
        if len(opts) == 4:
            break
    if len(opts) < 4:
        return None, None
    rng.shuffle(opts)
    return opts, opts.index(answer)


def build():
    """All core questions as bank records."""
    from . import (computer, economics, physics, chemistry, maths,  # noqa: F401  (registers)
                   engineering, expert, bridge)
    out, seen = [], set()
    rng = random.Random(20261029)
    for levels, subject, count, func in TEMPLATES:
        for level in levels:
            made, tries = 0, 0
            while made < count and tries < count * 6:
                tries += 1
                q, ans, wrong, e = func(rng, level)
                key = (level, q)
                if key in seen:
                    continue
                opts, a = options(ans, wrong, rng)
                if opts is None:
                    continue
                seen.add(key)
                out.append({"class_level": level, "subject": subject, "q": q, "o": opts, "a": a, "e": e,
                            "kind": func.__name__})
                made += 1
    for levels, subject, rows in FACTS:
        for level in levels:
            for q, ans, wrong, e in rows:
                key = (level, q)
                if key in seen:
                    continue
                opts, a = options(ans, list(wrong), rng)
                if opts is None:
                    raise ValueError(f"Fact needs 3 distinct wrong options: {q}")
                seen.add(key)
                out.append({"class_level": level, "subject": subject, "q": q, "o": opts, "a": a, "e": e,
                            "kind": "fact"})
    out = balance(out)
    for n, rec in enumerate(out, 1):
        rec["id"] = f"core{n}"
    return out


def balance(records):
    """Same count per level for BALANCE subjects: concept rows first, then templates taken in turn."""
    keep, pools = [], {}
    for r in records:
        if r["subject"] in BALANCE:
            pools.setdefault((r["class_level"], r["subject"]), []).append(r)
        else:
            keep.append(r)
    for (level, subject), items in sorted(pools.items()):
        target = BALANCE[subject]
        fact_rows = [r for r in items if r.get("kind") == "fact"]
        by_tpl = {}
        for r in items:
            if r.get("kind") != "fact":
                by_tpl.setdefault(r["kind"], []).append(r)
        chosen, queues = fact_rows[:target], list(by_tpl.values())
        while len(chosen) < target and any(queues):
            for q in queues:
                if q and len(chosen) < target:
                    chosen.append(q.pop(0))
        if len(chosen) < target:
            print(f"warning: {subject} level {level} has only {len(chosen)} of {target}")
        keep.extend(chosen)
    for r in keep:
        r.pop("kind", None)
    return keep
