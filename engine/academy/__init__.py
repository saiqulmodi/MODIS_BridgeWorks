"""BridgeWorks Academy question bank: Class 1-12 x 6 subjects, English and Bengali.

Each file cNN_<subject>.py holds up to 100 multiple-choice questions written with mcq().
engine/academy_data.py turns them into the public record format (and exports JSON).
"""
from dataclasses import dataclass

SUBJECTS = ("physics", "chemistry", "math", "biology", "finance", "commercials")
CLASSES = tuple(range(1, 13))


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
