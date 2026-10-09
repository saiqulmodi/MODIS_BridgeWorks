"""Big question banks: very large MCQ collections kept outside the game code (user, 2026-10-09).

The built-in Academy (Classes 1-12, NIT, IIT) lives in engine/academy/*.py. A big bank is a folder of
plain JSON files that tools/build_bank.py makes from SQLite, CSV or JSON. It can add questions to the
existing classes and subjects, and also bring new levels (e.g. 15 = International Olympiad) and new
subjects (e.g. EVS, Geography). Only the piece the student opens is read, so a bank can hold hundreds
of thousands of questions without slowing the game.

Layout (desktop: <project>/banks/, browser: banks/ next to the web page):
    banks/index.json                 {"banks": ["school", ...]}
    banks/<bank>/bank.json           {"id", "title", "levels": {"15": [en, bn]}, "subjects": {"evs": [en, bn]},
                                      "chunks": {"7/physics": ["7_physics_1.json", ...]},
                                      "counts": {"7/physics": 300}, "total": n}
    banks/<bank>/<chunk>.json        [{"id", "q", "o": [4], "a": 0-3, "e", "qb", "ob": [4], "eb"}, ...]

Record ids are "<bank>:<id>" so they never clash with the built-in integer ids. A question without
Bengali shows its English text in Bengali mode (bn_missing = True). Anything missing or broken is
skipped and logged; the game never crashes because of a bank.
"""
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "banks")
WEB = sys.platform == "emscripten"

_root = ROOT
_meta = None                # {bank_id: bank.json dict}
_chunks = {}                # (bank_id, chunk file) -> list of raw rows
_records = {}               # (level, subject) -> list of game records
errors = []                 # human-readable problems, for the log and tests


def disabled():
    return os.environ.get("BRIDGEWORKS_NO_BANKS") == "1"


def set_root(path):
    """Point at another banks folder (tests, tools) and forget everything loaded so far."""
    global _root, _meta
    _root = path
    _meta = None
    _chunks.clear()
    _records.clear()
    errors.clear()


def _read(rel):
    """Parse one JSON file of the banks folder; None when it is missing or broken."""
    try:
        if WEB:
            import platform
            import urllib.request
            page = str(platform.window.location.href).split("?")[0].split("#")[0]
            url = page.rsplit("/", 1)[0] + "/banks/" + rel
            path, _ = urllib.request.urlretrieve(url, "/tmp/bank_" + rel.replace("/", "_"))
        else:
            path = os.path.join(_root, *rel.split("/"))
            if not os.path.exists(path):
                return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:              # a bank must never stop the game
        errors.append(f"{rel}: {exc}")
        return None


def banks():
    """{bank_id: bank.json} for every bank listed in banks/index.json."""
    global _meta
    if _meta is None:
        _meta = {}
        if not disabled():
            index = _read("index.json") or {}
            for bid in index.get("banks", []):
                meta = _read(f"{bid}/bank.json")
                if isinstance(meta, dict) and isinstance(meta.get("chunks"), dict):
                    _meta[bid] = meta
                elif meta is not None:
                    errors.append(f"{bid}/bank.json: no chunk list")
    return _meta


def extra_levels():
    """{level: (english name, bengali name)} for levels a bank adds beyond the built-in ones."""
    out = {}
    for meta in banks().values():
        for lv, names in (meta.get("levels") or {}).items():
            try:
                out[int(lv)] = (str(names[0]), str(names[1] if len(names) > 1 else names[0]))
            except (ValueError, TypeError, IndexError):
                errors.append(f"{meta.get('id')}: bad level {lv!r}")
    return out


def extra_subjects():
    """{subject key: (english name, bengali name)} for subjects a bank adds."""
    out = {}
    for meta in banks().values():
        for key, names in (meta.get("subjects") or {}).items():
            try:
                out[str(key)] = (str(names[0]), str(names[1] if len(names) > 1 else names[0]))
            except (TypeError, IndexError):
                errors.append(f"{meta.get('id')}: bad subject {key!r}")
    return out


def levels_with_questions():
    out = set()
    for meta in banks().values():
        for key in meta.get("chunks", {}):
            try:
                out.add(int(key.split("/")[0]))
            except ValueError:
                pass
    return out


def count(level, subject):
    """How many bank questions exist for this level and subject (without loading them)."""
    key = f"{level}/{subject}"
    return sum(int((m.get("counts") or {}).get(key, 0)) for m in banks().values())


def total():
    return sum(int(m.get("total", 0)) for m in banks().values())


def _record(bid, title, title_bn, level, subject, row, grant):
    q, o, a = row.get("q"), row.get("o"), row.get("a")
    if not (isinstance(q, str) and q.strip() and isinstance(o, list) and len(o) == 4
            and isinstance(a, int) and 0 <= a <= 3 and len({str(x) for x in o}) == 4):
        return None
    ob = row.get("ob")
    has_bn = bool(row.get("qb")) and isinstance(ob, list) and len(ob) == 4 and len(set(ob)) == 4
    e = row.get("e") or ""
    return dict(id=f"{bid}:{row.get('id')}", class_level=level, subject=subject, question=q,
                options=[str(x) for x in o], correct_idx=a, explanation=e, grant_reward=grant,
                question_bn=row["qb"] if has_bn else q, options_bn=[str(x) for x in ob] if has_bn else [str(x) for x in o],
                explanation_bn=(row.get("eb") or e) if has_bn else e, bn_missing=not has_bn, bank=title,
                bank_bn=title_bn)


def items(level, subject, grant=0.0):
    """Every bank question for one level and subject, in the Academy record format."""
    key = (level, subject)
    if key not in _records:
        out = []
        for bid, meta in banks().items():
            title = str(meta.get("title") or bid)
            title_bn = str(meta.get("title_bn") or title)
            for name in meta["chunks"].get(f"{level}/{subject}", []):
                ck = (bid, name)
                if ck not in _chunks:
                    rows = _read(f"{bid}/{name}")
                    _chunks[ck] = rows if isinstance(rows, list) else []
                for row in _chunks[ck]:
                    rec = _record(bid, title, title_bn, level, subject, row, grant) if isinstance(row, dict) else None
                    if rec is not None:
                        out.append(rec)
        _records[key] = out
    return _records[key]
