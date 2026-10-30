"""
Question bank loader for the 5-project sandbox.

Reads banks/*/*.json - school/ and the generated core/ (compact keys q/o/a/e, class from the key or the
file name prefix) plus every Academy question (Class 1-12, NIT 13, IIT 14),
skipping repeats of the same question in the same class, and writes
data/questions.json and questions.txt as {"1".."5": [questions]} - the phase
layout quiz_console.py reads (Phase 1 = Class 1-3, 2 = 4-7, 3 = 8-10,
4 = 11-12, 5 = 13+).

    python -m game.question_bank      # rebuild both files
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK_GLOB = os.path.join(ROOT, "banks", "*", "*.json")     # school/, core/ ...
OUT_FILES = (os.path.join(ROOT, "data", "questions.json"), os.path.join(ROOT, "questions.txt"))
FILE_RE = re.compile(r"^(\d+)_(.+?)(?:_\d+)?\.json$")


def _first(d, *keys, default=None):
    for k in keys:
        v = d.get(k)
        if v not in (None, "", []):
            return v
    return default


def _to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _correct_index(raw, opts):
    """Answer may be an index, a digit string, a letter A-D or the option text."""
    if isinstance(raw, bool):
        return 0
    if isinstance(raw, int):
        return raw if 0 <= raw < len(opts) else 0
    s = str(raw if raw is not None else "").strip()
    if s.isdigit() and int(s) < len(opts):
        return int(s)
    if len(s) == 1 and s.upper() in "ABCD" and "ABCD".index(s.upper()) < len(opts):
        return "ABCD".index(s.upper())
    for i, o in enumerate(opts):
        if o.strip() == s:
            return i
    return 0


def normalise(q, file_cls=1, file_subject="general"):
    """One raw question -> the standard dict, or None if it has no text."""
    if not isinstance(q, dict):
        return None
    text = str(_first(q, "q", "question", default="")).strip()
    if not text:
        return None
    opts = _first(q, "o", "options", default=[])
    opts = [str(o) for o in opts] if isinstance(opts, list) else []
    real = len(opts)
    while len(opts) < 4:
        opts.append("-")
    idx = _correct_index(_first(q, "a", "correct_idx", "answer", default=0), opts[:max(real, 1)])
    cls = _to_int(_first(q, "class_level", "level", "class", "l", default=file_cls), file_cls)
    return {
        "id": str(q.get("id", "")),
        "class_level": cls,
        "subject": str(q.get("subject") or q.get("s") or file_subject),
        "question": text,
        "options": opts[:4] if idx < 4 else opts,
        "correct_idx": idx,
        "answer": opts[idx],
        "explanation": str(_first(q, "e", "explanation", default="")),
    }


def load_school_bank():
    out = []
    for path in sorted(glob.glob(BANK_GLOB)):
        m = FILE_RE.match(os.path.basename(path))
        if not m:
            continue                      # bank.json and other metadata
        file_cls, file_subject = int(m.group(1)), m.group(2)
        try:
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
        except (OSError, ValueError) as e:
            print(f"Skipping {path}: {e}")
            continue
        if isinstance(items, dict):
            items = items.get("questions", [])
        for q in items if isinstance(items, list) else []:
            n = normalise(q, file_cls, file_subject)
            if n:
                out.append(n)
    return out


def load_academy_bank():
    """Academy questions, Class 1-12 plus NIT (13) and IIT (14)."""
    try:
        from engine import academy_data
    except Exception as e:                # missing engine must not stop the game
        print(f"Academy questions not loaded: {e}")
        return []
    out = []
    for q in academy_data.all_items():
        n = normalise(q, q.get("class_level", 1), q.get("subject", "general"))
        if n:
            out.append(n)
    return out


def merge(*banks):
    seen, out = set(), []
    for bank in banks:
        for q in bank:
            key = (q["class_level"], q["question"].strip().lower())
            if key not in seen:
                seen.add(key)
                out.append(q)
    return out


def phase_of(cls):
    return "1" if cls <= 3 else "2" if cls <= 7 else "3" if cls <= 10 else "4" if cls <= 12 else "5"


def build():
    phases = {str(p): [] for p in range(1, 6)}
    for q in merge(load_school_bank(), load_academy_bank()):
        phases[phase_of(q["class_level"])].append(q)
    return phases


def write_files(phases):
    """data/questions.json is compact (the game and the web build read it); questions.txt stays readable."""
    for path in OUT_FILES:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            if path == OUT_FILES[0]:
                short = {k: [compact(q) for q in v] for k, v in phases.items()}
                json.dump(short, f, ensure_ascii=False, separators=(",", ":"))
            else:
                json.dump(phases, f, indent=2, ensure_ascii=False)


def compact(q):
    """Short keys for data/questions.json; normalise() reads them back."""
    return {"l": q["class_level"], "s": q["subject"], "q": q["question"], "o": q["options"],
            "a": q["correct_idx"], "e": q["explanation"]}


def flatten(data):
    """questions.json may be the phase dict or a plain list."""
    if isinstance(data, dict):
        return [q for k in sorted(data, key=str) for q in (data[k] if isinstance(data[k], list) else [])]
    return data if isinstance(data, list) else []


def load_for_game():
    """All questions, normalised. Reads data/questions.json, else builds from the banks."""
    try:
        with open(OUT_FILES[0], "r", encoding="utf-8") as f:
            qs = [n for n in (normalise(q, _to_int(q.get("class_level", q.get("l")), 1)) for q in flatten(json.load(f))) if n]
        if qs:
            return qs
    except (OSError, ValueError):
        pass
    return flatten(build())


if __name__ == "__main__":
    ph = build()
    write_files(ph)
    print(f"Wrote {sum(len(v) for v in ph.values())} questions:", {k: len(v) for k, v in ph.items()})
