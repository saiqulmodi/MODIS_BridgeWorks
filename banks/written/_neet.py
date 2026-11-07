"""Class 11/12 Physics and Chemistry questions from the NEET Data Hub (read-only), for BridgeWorks.

No Biology. Used by b053/b054; the shared Gate in the exports still drops anything already in a game or
near-same to a kept question (FAILSPAN already has these rows, so it keeps none of them twice)."""
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(os.path.dirname(ROOT), "NEET_Data_Hub", "output", "neet_hub.db")
SUBJ = {"Physics": "physics", "Chemistry": "chemistry"}
HEAD_MAX = 12                     # one opening (first five words) at most this many times per subject
SKIP = re.compile(r"\b(figure|fig\.|shown (below|above|in)|diagram|graph shown|given below)\b", re.I)


def items(level):
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import ncert_map
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        rows = db.execute("select q.subject, c.title, q.question, q.option_a, q.option_b, q.option_c, q.option_d, "
                          "q.correct_option, q.explanation from questions q left join chapters c on c.id = q.chapter_id "
                          "where q.class_level = ? and q.subject in ('Physics', 'Chemistry') and q.source != 'School MCQ Bank' "
                          "order by q.id", (level,)).fetchall()
    finally:
        db.close()
    out, heads = [], {}
    for subj, title, q, a, b, c, d, right, expl in rows:
        opts = [(o or "").strip() for o in (a, b, c, d)]
        if right not in ("A", "B", "C", "D") or len(set(opts)) < 4 or not all(opts) or SKIP.search(q):
            continue
        k = "ABCD".index(right)
        opts = [opts[k]] + opts[:k] + opts[k + 1:]
        raw = SUBJ[subj]
        subject, chapter, _ = ncert_map.classify(level, raw, title or "", q, expl or "")
        if chapter is None and ncert_map.chapter_order(level, subject):
            subject = raw + "_x"
            if ncert_map.chapter_order(level, subject):
                continue
        head = (subject, " ".join(re.findall(r"[a-z]+", q.lower())[:5]))
        if heads.get(head, 0) >= HEAD_MAX:
            continue
        heads[head] = heads.get(head, 0) + 1
        out.append((subject, chapter, q.strip(), opts, (expl or "").strip()))
    return out
