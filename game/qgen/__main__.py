"""Write banks/core/<level>_<subject>_<n>.json from the generators, then rebuild the game files."""
import collections
import glob
import json
import os

from . import build
from game import question_bank

CHUNK = 400
OUT_DIR = os.path.join(question_bank.ROOT, "banks", "core")


def main():
    records = build()
    os.makedirs(OUT_DIR, exist_ok=True)
    for old in glob.glob(os.path.join(OUT_DIR, "*.json")):
        os.remove(old)
    groups = collections.defaultdict(list)
    for r in records:
        groups[(r["class_level"], r["subject"])].append(r)
    for (level, subject), items in sorted(groups.items()):
        for k in range(0, len(items), CHUNK):
            path = os.path.join(OUT_DIR, f"{level}_{subject}_{k // CHUNK + 1}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(items[k:k + CHUNK], f, ensure_ascii=False)
    by_level = collections.Counter(r["class_level"] for r in records)
    print(f"Core bank: {len(records)} questions in {len(groups)} level/subject groups")
    print(dict(sorted(by_level.items())))
    phases = question_bank.build()
    question_bank.write_files(phases)
    print("Game files:", {k: len(v) for k, v in phases.items()})


if __name__ == "__main__":
    main()
