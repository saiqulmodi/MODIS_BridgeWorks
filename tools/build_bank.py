"""Turn a big question file into a BridgeWorks question bank (banks/<id>/), see engine/question_bank.py.

    venv\\Scripts\\python.exe tools/build_bank.py --id school --title "School MCQ Bank" ^
        --title-bn "স্কুল প্রশ্নব্যাংক" --sqlite ..\\School_MCQ_Bank\\output\\mcq_bank.db --publish

Sources: --sqlite FILE [--table questions], --csv FILE, --json FILE (a list of rows, or {"questions": [...]}).
Columns are found by name (case does not matter):
    level      class_level | level | class | grade          (1-12, NIT/JEE Main = 13, IIT/JEE Advanced = 14)
    subject    subject
    question   question | q
    options    options (list or JSON text) | option_a..option_d | a..d
    answer     correct_idx (0-3) | correct_option (A-D or 1-4) | answer | correct_answer (the option text)
    explain    explanation | solution
    Bengali    question_bn, options_bn | option_a_bn..option_d_bn, explanation_bn   (optional)
New levels:   --new-level "15=International Olympiad|আন্তর্জাতিক অলিম্পিয়াড"  (the name may then be used as a level)
Subjects:     physics, chemistry, math, biology, finance, commercials are the Academy's own; others (EVS,
              Geography, English, ...) become new subjects. --subject-map "Accountancy=commercials" adds names.
Every row is checked: a question, four different non-empty options, one valid answer. Repeated questions,
and questions already in the built-in Academy, are skipped. --publish copies banks/ into docs/banks/ so
the website version can download it. --remove ID takes a bank out.
"""
import argparse
import csv
import json
import os
import re
import shutil
import sqlite3
import sys

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT)
os.environ["BRIDGEWORKS_NO_BANKS"] = "1"          # compare against the built-in Academy only

from engine.academy import SUBJECTS  # noqa: E402
from engine.academy_data import all_items  # noqa: E402

CHUNK = 1000
OWN = {s: s for s in SUBJECTS}
SUBJECT_NAMES = {      # key: (English, Bengali) for subjects the Academy does not have yet
    "evs": ("EVS", "পরিবেশ পরিচিতি"), "geography": ("Geography", "ভূগোল"),
    "general_safety": ("General Safety", "সাধারণ নিরাপত্তা"), "english": ("English", "ইংরেজি"),
    "computer_science": ("Computer Science", "কম্পিউটার বিজ্ঞান"), "history": ("History", "ইতিহাস"),
    "civics": ("Civics", "পৌরনীতি"), "economics": ("Economics", "অর্থনীতি"),
    "general_knowledge": ("General Knowledge", "সাধারণ জ্ঞান"), "astronomy": ("Astronomy", "জ্যোতির্বিজ্ঞান"),
}
SUBJECT_MAP = {
    "maths": "math", "mathematics": "math", "math": "math", "physics": "physics", "chemistry": "chemistry",
    "biology": "biology", "finance": "finance", "commercials": "commercials", "commerce": "commercials",
    "accountancy": "commercials", "business studies": "commercials", "evs": "evs",
    "environmental studies": "evs", "geography": "geography", "general safety": "general_safety",
    "safety": "general_safety", "english": "english", "computer science": "computer_science",
    "computers": "computer_science", "history": "history", "civics": "civics", "economics": "economics",
    "general knowledge": "general_knowledge", "gk": "general_knowledge", "astronomy": "astronomy",
}
LEVEL_MAP = {"nit": 13, "jee main": 13, "jee mains": 13, "iit": 14, "jee advanced": 14}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.strip().lower()).strip("_")


def load_rows(args):
    if args.sqlite:
        con = sqlite3.connect(args.sqlite)
        con.row_factory = sqlite3.Row
        return [dict(r) for r in con.execute(f"SELECT * FROM {args.table}")]
    if args.csv:
        with open(args.csv, encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    with open(args.json, encoding="utf-8") as f:
        data = json.load(f)
    return data["questions"] if isinstance(data, dict) else data


def pick(row, *names):
    for n in names:
        v = row.get(n)
        if v not in (None, ""):
            return v
    return None


def options_of(row, suffix=""):
    v = pick(row, "options" + suffix)
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except ValueError:
            v = None
    if isinstance(v, list):
        return [str(x).strip() for x in v]
    four = [pick(row, f"option_{x}{suffix}", f"{x}{suffix}") for x in "abcd"]
    return [str(x).strip() for x in four] if all(x is not None for x in four) else None


def answer_of(row, opts):
    v = pick(row, "correct_idx")
    if v is not None and str(v).strip().isdigit() and 0 <= int(v) <= 3:
        return int(v)
    v = pick(row, "correct_option", "answer", "correct")
    if v is not None:
        t = str(v).strip()
        if len(t) == 1 and t.upper() in "ABCD":
            return "ABCD".index(t.upper())
        if t in ("1", "2", "3", "4"):
            return int(t) - 1
        if t in opts:
            return opts.index(t)
    v = pick(row, "correct_answer")
    if v is not None and str(v).strip() in opts:
        return opts.index(str(v).strip())
    return None


def level_of(row, names):
    v = pick(row, "class_level", "level", "class", "grade")
    if v is None:
        return None
    t = str(v).strip().lower()
    if t.isdigit():
        return int(t)
    return names.get(t) or LEVEL_MAP.get(t)


def build(args):
    new_levels = {}
    level_names = dict(LEVEL_MAP)
    for spec in args.new_level:
        num, _, names = spec.partition("=")
        en, _, bn = names.partition("|")
        new_levels[int(num)] = [en.strip(), (bn or en).strip()]
        level_names[en.strip().lower()] = int(num)
    smap = dict(SUBJECT_MAP)
    for spec in args.subject_map.split(",") if args.subject_map else []:
        name, _, key = spec.partition("=")
        smap[name.strip().lower()] = slug(key)

    built_in = {r["question"].strip().lower() for r in all_items()}
    seen, chunks, extra_subjects, rejects = set(), {}, {}, {}
    rows = load_rows(args)
    for k, raw in enumerate(rows):
        row = {str(key).strip().lower(): val for key, val in raw.items()}
        q = pick(row, "question", "q")
        opts = options_of(row)
        why = None
        if not q or not str(q).strip():
            why = "no question"
        elif not opts or len(opts) != 4 or len(set(opts)) != 4 or not all(opts):
            why = "options are not 4 different answers"
        lvl = level_of(row, level_names)
        if why is None and (lvl is None or lvl < 1 or (lvl > 14 and lvl not in new_levels)):
            why = "unknown level (declare it with --new-level)"
        a = answer_of(row, opts) if why is None else None
        if why is None and a is None:
            why = "no valid answer"
        subj_raw = str(pick(row, "subject") or "").strip()
        subj = smap.get(subj_raw.lower()) or slug(subj_raw)
        if why is None and not subj:
            why = "no subject"
        q = str(q).strip() if q else ""
        if why is None and q.lower() in built_in:
            why = "already in the built-in Academy"
        if why is None and (lvl, subj, q.lower()) in seen:
            why = "repeated question"
        if why:
            rejects[why] = rejects.get(why, 0) + 1
            continue
        seen.add((lvl, subj, q.lower()))
        if subj not in OWN:
            extra_subjects[subj] = list(SUBJECT_NAMES.get(subj, (subj_raw.title(), subj_raw.title())))
        rec = {"id": pick(row, "id") or k + 1, "q": q, "o": opts, "a": a,
               "e": str(pick(row, "explanation", "solution") or "").strip()}
        qb, ob = pick(row, "question_bn"), options_of(row, "_bn")
        if qb and ob and len(ob) == 4 and len(set(ob)) == 4 and all(ob):
            rec.update(qb=str(qb).strip(), ob=ob, eb=str(pick(row, "explanation_bn") or "").strip())
        chunks.setdefault(f"{lvl}/{subj}", []).append(rec)

    out = os.path.join(args.out, args.id)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    meta = {"id": args.id, "title": args.title, "title_bn": args.title_bn or args.title,
            "source": os.path.basename(args.sqlite or args.csv or args.json),
            "levels": {str(k): v for k, v in sorted(new_levels.items())},
            "subjects": dict(sorted(extra_subjects.items())), "chunks": {}, "counts": {}, "total": 0}
    for key, recs in sorted(chunks.items()):
        lvl, subj = key.split("/")
        names = []
        for i in range(0, len(recs), CHUNK):
            name = f"{lvl}_{subj}_{i // CHUNK + 1}.json"
            with open(os.path.join(out, name), "w", encoding="utf-8") as f:
                json.dump(recs[i:i + CHUNK], f, ensure_ascii=False, separators=(",", ":"))
            names.append(name)
        meta["chunks"][key] = names
        meta["counts"][key] = len(recs)
        meta["total"] += len(recs)
    with open(os.path.join(out, "bank.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    set_index(args.out, add=args.id)

    with_bn = sum(1 for recs in chunks.values() for r in recs if "qb" in r)
    print(f"bank '{args.id}': {meta['total']:,} questions kept of {len(rows):,} rows "
          f"({with_bn:,} with Bengali), {sum(len(v) for v in meta['chunks'].values())} files")
    for why, n in sorted(rejects.items(), key=lambda x: -x[1]):
        print(f"  skipped {n:,}: {why}")
    if extra_subjects:
        print("  new subjects: " + ", ".join(f"{v[0]} ({k})" for k, v in extra_subjects.items()))
    return meta


def set_index(root, add=None, remove=None):
    path = os.path.join(root, "index.json")
    try:
        with open(path, encoding="utf-8") as f:
            ids = json.load(f).get("banks", [])
    except (OSError, ValueError):
        ids = []
    if add and add not in ids:
        ids.append(add)
    if remove:
        ids = [i for i in ids if i != remove]
        shutil.rmtree(os.path.join(root, remove), ignore_errors=True)
    os.makedirs(root, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"banks": ids}, f, indent=1)


def publish(root):
    """Copy the banks folder next to the web page (docs/banks) for the browser version."""
    dst = os.path.join(PROJECT, "docs", "banks")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(root, dst)
    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(dst) for f in fs)
    print(f"published to docs/banks ({size / 1024 / 1024:.1f} MB)")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--id", help="short bank name, letters and digits")
    p.add_argument("--title", help="name shown on each question")
    p.add_argument("--title-bn", default="")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--sqlite")
    src.add_argument("--csv")
    src.add_argument("--json")
    p.add_argument("--table", default="questions")
    p.add_argument("--new-level", action="append", default=[])
    p.add_argument("--subject-map", default="")
    p.add_argument("--out", default=os.path.join(PROJECT, "banks"))
    p.add_argument("--publish", action="store_true")
    p.add_argument("--remove", metavar="ID")
    args = p.parse_args(argv)
    if args.remove:
        set_index(args.out, remove=args.remove)
        print(f"removed bank '{args.remove}'")
    elif args.sqlite or args.csv or args.json:
        if not (args.id and re.fullmatch(r"[a-z0-9_-]+", args.id) and args.title):
            p.error("--id (lower-case letters, digits, - or _) and --title are needed")
        build(args)
    if args.publish:
        publish(args.out)


if __name__ == "__main__":
    main()
