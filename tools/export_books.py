"""NCERT books tab for both web games: one small list per class of the current English-medium NCERT textbooks for
the game's own subjects (Science/Physics/Chemistry, Maths, Geography, Economics; no Biology book), each chapter
linking to NCERT's official free PDF (https://ncert.nic.in/textbook/pdf/<code><NN>.pdf). Nothing is copied: the
books stay on NCERT's site, so the game grows by a few KB only.

    python tools/export_books.py

Codes and chapter counts were read from https://ncert.nic.in/textbook.php and every chapter link was checked
(HTTP 200) on 08-Nov-2026. NIT and IIT (JEE) use the Class 11 and 12 books; BE and Expert have no NCERT book.
Writes web/data/books.json here and data/books.json in FAILSPAN.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTS = [os.path.join(ROOT, "web", "data", "books.json"),
        os.path.join(os.path.dirname(ROOT), "FAILSPAN", "data", "books.json")]

# (subject, title, code, chapters)
BOOKS = {
    8: [("science", "Curiosity (Science)", "hecu1", 13),
        ("math", "Ganita Prakash Part I (Maths)", "hegp1", 7),
        ("math", "Ganita Prakash Part II (Maths)", "hegp2", 7),
        ("geography", "Exploring Society: India and Beyond Part I", "hees1", 7),
        ("geography", "Exploring Society: India and Beyond Part II", "hees2", 8)],
    9: [("science", "Exploration (Science)", "iesc1", 13),
        ("math", "Ganita Manjari Part I (Maths)", "iemh1", 8),
        ("math", "Ganita Manjari Part II (Maths)", "iemh2", 6),
        ("geography", "Understanding Society: India and Beyond Part I", "iest1", 9),
        ("geography", "Understanding Society: India and Beyond Part II", "iest2", 6)],
    10: [("science", "Science", "jesc1", 13),
         ("math", "Mathematics", "jemh1", 14),
         ("geography", "Contemporary India (Geography)", "jess1", 7),
         ("economics", "Understanding Economic Development", "jess2", 5)],
    11: [("physics", "Physics Part I", "keph1", 7),
         ("physics", "Physics Part II", "keph2", 7),
         ("chemistry", "Chemistry Part I", "kech1", 6),
         ("chemistry", "Chemistry Part II", "kech2", 3),
         ("math", "Mathematics", "kemh1", 14),
         ("geography", "Fundamentals of Physical Geography", "kegy2", 14),
         ("geography", "India: Physical Environment", "kegy1", 6),
         ("economics", "Indian Economic Development", "keec1", 8),
         ("economics", "Statistics for Economics", "kest1", 8)],
    12: [("physics", "Physics Part I", "leph1", 8),
         ("physics", "Physics Part II", "leph2", 6),
         ("chemistry", "Chemistry Part I", "lech1", 5),
         ("chemistry", "Chemistry Part II", "lech2", 5),
         ("math", "Mathematics Part I", "lemh1", 6),
         ("math", "Mathematics Part II", "lemh2", 7),
         ("geography", "Fundamentals of Human Geography", "legy1", 8),
         ("geography", "India: People and Economy", "legy2", 9),
         ("economics", "Introductory Macroeconomics", "leec1", 6),
         ("economics", "Introductory Microeconomics", "leec2", 5)],
}
JEE = [b for lv in (11, 12) for b in BOOKS[lv] if b[0] in ("physics", "chemistry", "math")]


def rows(books, prefix=""):
    return [{"s": s, "t": prefix + t, "c": c, "n": n} for s, t, c, n in books]


def main():
    levels = {str(lv): rows(b) for lv, b in BOOKS.items()}
    jee = rows([b for b in JEE if b[2].startswith("k")], "Class 11 ") + rows([b for b in JEE if b[2].startswith("l")], "Class 12 ")
    levels["13"] = levels["14"] = jee
    out = {"base": "https://ncert.nic.in/textbook/pdf/", "levels": levels}
    for p in OUTS:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("books:", {k: len(v) for k, v in levels.items()}, "chapters:", sum(b["n"] for v in levels.values() for b in v))


if __name__ == "__main__":
    main()
