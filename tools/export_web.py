"""Export everything the web version (web/) needs as small JSON files.

    python tools/export_web.py

web/data/levels.json         one row per building: level code, name, project, question count, subjects
web/data/q/<level>.json      that level's questions only: {"s": [subjects], "q": [[subject, q, options, answer, explanation, bengali?]]}
                             (bengali = [question, options, explanation] where the Academy has it)
web/data/projects.json       the 5 bridge projects, materials, sizes, guided-build steps (checked with the Python solver)
web/data/handbook.json       the 200-question Engineering Handbook (English + Bengali)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from engine import materials as M                       # noqa: E402
from game.projects import (DECK_SIZE, PARTS_PER_CORRECT, PROJECTS, PYLON_AREA,  # noqa: E402
                           SIZE_COST, Design)
from game.question_bank import load_for_game           # noqa: E402
from game.world import LEVELS, SUBJECT_NAMES, tier_of  # noqa: E402

OUT = os.path.join(ROOT, "web", "data")
SC, ST, ST_C, CF = M.STEEL_CABLE, M.STEEL, M.CONCRETE, M.CARBON_CABLE

# Guided build: the steps of a design that passes, easiest idea first.
STEPS = {
    1: [("Hang a cable from the left mast top to road joint 1.", [(5, 1, SC, "S")]),
        ("Hang a cable from the left mast top to the middle road joint.", [(5, 2, SC, "S")]),
        ("Hang a cable from the right mast top to road joint 3.", [(6, 3, SC, "S")])],
    2: [("Build the top chord: join the five top joints in a line.", [(7, 8, ST, "M"), (8, 9, ST, "M"), (9, 10, ST, "M"), (10, 11, ST, "M")]),
        ("Add the two end posts from the supports up to the top. They carry the most, so use size L.", [(0, 7, ST, "L"), (6, 11, ST, "L")]),
        ("Add a vertical under every top joint.", [(1, 7, ST, "M"), (2, 8, ST, "M"), (3, 9, ST, "M"), (4, 10, ST, "M"), (5, 11, ST, "M")]),
        ("Add diagonals sloping down towards the middle, so every panel is a triangle.", [(7, 2, ST, "M"), (8, 3, ST, "M"), (10, 3, ST, "M"), (11, 4, ST, "M")])],
    3: [("Build the arch rib from bank to bank through the arch joints (steel, size L).",
         [(0, 9, ST, "L")] + [(k, k + 1, ST, "L") for k in range(9, 15)] + [(15, 8, ST, "L")]),
        ("Hang the road from the arch: a steel hanger from each arch joint straight down.", [(k, k - 8, ST, "S") for k in range(9, 16)]),
        ("Brace the arch with diagonals so it cannot change shape.", [(9, 2, ST, "L"), (10, 3, ST, "L"), (11, 4, ST, "L"), (13, 4, ST, "L"), (14, 5, ST, "L"), (15, 6, ST, "L")])],
    4: [("Anchor the pylon top with a backstay cable to each bank support.", [(14, 0, SC, "M"), (14, 12, SC, "M")]),
        ("Fan stays from the pylon top to the left half of the road.", [(14, k, SC, "M") for k in (1, 2, 3, 4, 5)]),
        ("Mirror the fan on the right half so the pulls balance.", [(14, k, SC, "M") for k in (7, 8, 9, 10, 11)])],
    5: [("Anchor each pylon top to its bank support.", [(18, 0, CF, "M"), (20, 16, CF, "M")]),
        ("Tie the two pylon tops together.", [(18, 20, SC, "M")]),
        ("Fan carbon stays from the left pylon over its side of the road.", [(18, k, CF, "M") for k in (1, 2, 3, 5, 6, 7, 8)]),
        ("Fan carbon stays from the right pylon; road joint 8 in the middle gets one from each pylon.", [(20, k, CF, "M") for k in (8, 9, 10, 11, 13, 14, 15)])],
}

HINTS = {
    1: ["Cables can only pull. Each road joint between the banks needs one cable pulling it up.",
        "Join a mast top (the joints high on the banks) to the road joints 1, 2 and 3.",
        "Size S is strong enough for a car - save your parts."],
    2: ["A frame of squares folds flat. Every panel needs a diagonal to make two triangles.",
        "Start with the top chord, then the end posts, verticals and diagonals.",
        "If an end post buckles, make it size L - long pushed members buckle first."],
    3: ["The arch must go from bank to bank through all the arch joints, and it is pushed (compression).",
        "Cable hangers can go slack when the truck lifts the arch - steel hangers push and pull.",
        "Brace the arch: diagonals between arch joints and the road joints next to them."],
    4: ["Without backstays the pylon top can sway: tie it to both bank supports first.",
        "Then give every road joint its own stay, balanced left and right.",
        "Flat stays near the banks pull hardest; use size M or bigger."],
    5: ["Each pylon top needs a backstay to its bank, and a tie to the other pylon top.",
        "Every road joint needs a stay; the middle joint can take one from each pylon.",
        "Carbon cable is stronger for the same size. Watch the stays near the banks."],
}


def mat_name(m):
    return m.name


def export_projects():
    mats = {m.name: {"E": m.E, "t": m.tensile_strength, "c": m.compressive_strength, "rho": m.density,
                     "colour": list(m.colour), "cable": m.cable_only} for m in M.ALL.values()}
    out = []
    for p in PROJECTS:
        d = Design(p)
        d.parts = 10_000
        steps = []
        for text, members in STEPS[p.id]:
            for i, j, mat, size in members:
                assert d.add(i, j, mat, size) == "", (p.id, i, j)
            steps.append({"text": text, "members": [[i, j, mat.name, size] for i, j, mat, size in members]})
        ok, msg, worst = d.full_test()
        assert ok, f"guided design for project {p.id} fails: {msg}"
        par = sum(SIZE_COST[s] for *_, s in d.members)
        out.append({
            "id": p.id, "name": p.name, "level": p.level, "span": p.span, "joints": p.joints, "n_deck": p.n_deck,
            "supports": {str(k): v for k, v in p.supports.items()},
            "prebuilt": [[i, j, mat.name, size, kind] for i, j, mat, size, kind in p.prebuilt],
            "materials": [m.name for m in p.materials], "sizes": p.sizes,
            "vehicle": {"name": p.vehicle.name, "mass": p.vehicle.mass_kg, "axles": list(p.vehicle.axles), "colour": list(p.vehicle.colour)},
            "dead_load": p.dead_load, "impact": p.impact, "goal": p.goal, "tip": p.tip, "lesson": p.lesson,
            "parts_per_correct": PARTS_PER_CORRECT[p.id], "steps": steps, "hints": HINTS[p.id],
            "par_parts": par, "ref_worst": round(worst, 6),
        })
        print(f"project {p.id}: guided design passes, worst ratio {worst:.2f}, {par} parts")
    return {"materials": mats, "shapes": {"solid": M.SOLID.factor, "ibeam": M.IBEAM.factor, "box": M.BOX.factor},
            "beam_sizes": M.BEAM_SIZES, "cable_sizes": M.CABLE_SIZES, "size_cost": SIZE_COST,
            "pylon_area": PYLON_AREA, "deck_size": DECK_SIZE, "projects": out}


def bengali_text():
    """(level, English question) -> [question, options, explanation] in Bengali, from the Academy."""
    from engine import academy_data
    out = {}
    for it in academy_data.all_items():
        if it.get("question_bn"):
            out[(it["class_level"], it["question"].strip())] = [it["question_bn"], list(it.get("options_bn") or it["options"]),
                                                                it.get("explanation_bn", "")]
    return out


def export_questions():
    qs = load_for_game()
    bn = bengali_text()
    os.makedirs(os.path.join(OUT, "q"), exist_ok=True)
    levels = []
    for level, name in LEVELS:
        mine = [q for q in qs if q["class_level"] == level]
        subjects = sorted({q["subject"] for q in mine}, key=lambda s: SUBJECT_NAMES.get(s, s))
        idx = {s: k for k, s in enumerate(subjects)}
        rows = []
        for q in mine:
            if q["correct_idx"] >= 4:
                continue
            row = [idx[q["subject"]], q["question"], q["options"][:4], q["correct_idx"], q["explanation"]]
            b = bn.get((level, q["question"].strip()))
            if b and len(b[1]) >= 4:
                row.append([b[0], b[1][:4], b[2]])
            rows.append(row)
        with open(os.path.join(OUT, "q", f"{level}.json"), "w", encoding="utf-8") as f:
            json.dump({"s": subjects, "q": rows}, f, ensure_ascii=False, separators=(",", ":"))
        counts = {s: sum(1 for r in rows if r[0] == idx[s]) for s in subjects}
        levels.append({"l": level, "name": name, "project": tier_of(level), "n": len(rows), "subjects": counts})
    return levels


def export_handbook():
    from game.guide import SECTIONS
    return [{"key": s.key, "title": s.title_en, "title_bn": s.title_bn, "first": s.first,
             "items": [[it.q_en, it.a_en, it.q_bn, it.a_bn] for it in s.items]}
            for s in SECTIONS if s.first > 0]


def main():
    os.makedirs(OUT, exist_ok=True)

    def dump(name, obj):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))

    dump("projects.json", export_projects())
    levels = export_questions()
    dump("levels.json", {"levels": levels, "subject_names": SUBJECT_NAMES})
    dump("handbook.json", export_handbook())
    print("questions:", sum(l["n"] for l in levels), "in", len(levels), "levels")


if __name__ == "__main__":
    main()
