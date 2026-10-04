"""In-game Help: a guide for new players and 200 questions & answers, in English and Bengali.

Every answer uses the game's real numbers (engine/ and game/), so what the Help says is
what the simulation does. Text is stored in both languages side by side and shown raw in
the current language, so it never goes through the string-by-string translator.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    q_en: str
    a_en: str
    q_bn: str
    a_bn: str
    level: int = 0          # the level this answer walks through (0 = general)

    def q(self, lang):
        return self.q_bn if lang == "bn" else self.q_en

    def a(self, lang):
        return self.a_bn if lang == "bn" else self.a_en


def qa(q_en, a_en, q_bn, a_bn, level=0):
    return Item(q_en, a_en, q_bn, a_bn, level)


@dataclass(frozen=True)
class Section:
    key: str
    title_en: str
    title_bn: str
    first: int              # number of the first question (0 = the unnumbered start guide)
    items: tuple

    def title(self, lang):
        return self.title_bn if lang == "bn" else self.title_en

    def tag(self, k, lang):
        """Label shown before item k: 'Q12' / 'প্রশ্ন 12', or 'Start 3' / 'শুরু 3'."""
        if self.first == 0:
            return f"শুরু {k + 1}" if lang == "bn" else f"Start {k + 1}"
        n = self.first + k
        return f"প্রশ্ন {n}" if lang == "bn" else f"Q{n}"


from .start import START          # noqa: E402
from .truss import TRUSS          # noqa: E402
from .beams import BEAMS          # noqa: E402
from .dynamics import DYNAMICS    # noqa: E402
from .money import MONEY          # noqa: E402

SECTIONS = (
    Section("start", "Start here: how to play", "এখান থেকে শুরু: কীভাবে খেলবে", 0, START),
    Section("truss", "Q1-50  Trusses & materials", "প্রশ্ন 1-50  ট্রাস ও উপাদান", 1, TRUSS),
    Section("beams", "Q51-100  Beams & cantilevers", "প্রশ্ন 51-100  বিম ও ক্যান্টিলিভার", 51, BEAMS),
    Section("dynamics", "Q101-150  Wind, quakes & rail", "প্রশ্ন 101-150  বাতাস, ভূমিকম্প ও রেল", 101,
            DYNAMICS),
    Section("money", "Q151-200  Money & every level", "প্রশ্ন 151-200  টাকা ও প্রতিটি লেভেল", 151, MONEY),
)


def level_walkthrough(num):
    """(section index, item index) of the 'How do I win Level N?' answer."""
    for s, sec in enumerate(SECTIONS):
        for k, it in enumerate(sec.items):
            if it.level == num:
                return s, k
    return 0, 0
