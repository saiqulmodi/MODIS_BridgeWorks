"""BridgeWorks Academy question bank: Class 1-12 x 6 subjects, then the NIT level (13, JEE Main
standard) and the IIT level (14, JEE Advanced standard), English and Bengali.

Each file cNN_<subject>.py holds up to target_per_subject(NN) multiple-choice questions written with
mcq(): 100 for Classes 1-12, 200 for NIT and IIT.
engine/academy_data.py turns them into the public record format (and exports JSON).
"""
from dataclasses import dataclass

SUBJECTS = ("physics", "chemistry", "math", "biology", "finance", "commercials")
CLASSES = tuple(range(1, 15))
NIT, IIT = 13, 14
LEVEL_NAMES = {NIT: ("NIT", "NIT"), IIT: ("IIT", "IIT")}   # shown instead of a class number


def target_per_subject(class_level):
    return 200 if class_level >= NIT else 100


def class_label(class_level, lang="en"):
    """'7' for Class 7, 'NIT' / 'IIT' for the two entrance-exam levels."""
    if class_level in LEVEL_NAMES:
        return LEVEL_NAMES[class_level][1 if lang == "bn" else 0]
    return str(class_level)


@dataclass(frozen=True)
class MCQ:
    question: str
    options: tuple          # 4 options, English
    correct_idx: int        # 0..3
    explanation: str
    question_bn: str
    options_bn: tuple       # the same 4 options in Bengali, same order
    explanation_bn: str


def mcq(question, options, correct_idx, explanation, question_bn, options_bn, explanation_bn):
    return MCQ(question, tuple(options), correct_idx, explanation, question_bn, tuple(options_bn),
               explanation_bn)
