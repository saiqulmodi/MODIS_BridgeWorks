"""'Game skills': the Help screen's 200 answers as multiple-choice questions (Academy track).

Each part of engine/academy/skills_*.py lists MCQs in the order of the Help questions they
test. Records use the Academy format with class_level 0 and subject "skills".
"""
import importlib

from .academy_data import record

SKILL_GRANT = 2000.0
PARTS = ("skills_truss", "skills_beams", "skills_dynamics", "skills_money")

_cache = []


def items():
    if not _cache:
        for p, part in enumerate(PARTS):
            try:
                raw = importlib.import_module(f"engine.academy.{part}").ITEMS
            except ModuleNotFoundError:
                raw = ()
            for k, m in enumerate(raw):       # ids stay fixed: 900000 + part x 1000 + position
                _cache.append(record(900000 + (p + 1) * 1000 + k + 1, 0, "skills", m, SKILL_GRANT))
    return _cache
