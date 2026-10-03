"""Railway signalling maths and logic gates (Prompt 4).

Safe braking distance on a slope (theta > 0 = downhill):

    d_stop = v^2 / (2 (mu g cos(theta) - g sin(theta)))

A caution (yellow) signal must stand at least d_stop before the red it warns about,
otherwise a train at line speed cannot stop in time.

Block signalling (3-aspect):  RED = my block is occupied
                              YELLOW = next signal is red (slow down, be ready to stop)
                              GREEN = at least two blocks ahead are clear
4-aspect adds DOUBLE YELLOW = the signal after next is red (lets blocks be shorter).
"""
import math
from dataclasses import dataclass, field

from .vehicles import braking_distance

G = 9.81
RED, YELLOW, DOUBLE_YELLOW, GREEN = "R", "Y", "YY", "G"


def safe_braking_distance(v, mu, theta_down=0.0):
    return braking_distance(v, mu, theta_down)


def deceleration(mu, theta_down=0.0, g=G):
    return g * (mu * math.cos(theta_down) - math.sin(theta_down))


def aspect_for(block_occupied, next_aspect, four_aspect=False, permitted=True):
    """Aspect of a signal from its own block and the aspect of the next signal ahead."""
    if block_occupied or not permitted:
        return RED
    if next_aspect is None:
        return GREEN
    if next_aspect == RED:
        return YELLOW
    if four_aspect and next_aspect == YELLOW:
        return DOUBLE_YELLOW
    return GREEN


def min_block_length(v, mu, four_aspect=False, theta_down=0.0, margin=20.0):
    """Shortest safe block: a train passing a YELLOW (or DOUBLE YELLOW for 4-aspect) must be
    able to stop at the red. 4-aspect warning spans two blocks, so each can be half as long."""
    d = safe_braking_distance(v, mu, theta_down) + margin
    return d / 2 if four_aspect else d


# --- Logic gates ---------------------------------------------------------------------------

@dataclass
class LogicRow:
    """OUTPUT = [NOT] A  op1  [NOT] B  op2  [NOT] C   (evaluated left to right)."""
    output: str
    inputs: list = field(default_factory=lambda: [None, None, None])
    negate: list = field(default_factory=lambda: [False, False, False])
    ops: list = field(default_factory=lambda: ["AND", "AND"])

    def evaluate(self, values):
        result = None
        for k in range(3):
            name = self.inputs[k]
            if name is None:
                continue
            v = bool(values.get(name, False))
            if self.negate[k]:
                v = not v
            if result is None:
                result = v
            else:
                op = self.ops[k - 1]
                result = (result and v) if op == "AND" else (result or v)
        return bool(result) if result is not None else False

    def text(self):
        parts = []
        for k in range(3):
            name = self.inputs[k]
            if name is None:
                continue
            term = ("NOT " if self.negate[k] else "") + name
            if parts:
                parts.append(self.ops[k - 1])
            parts.append(term)
        return f"{self.output} = " + (" ".join(parts) if parts else "FALSE")

    def term_count(self):
        return sum(1 for n in self.inputs if n is not None)


def evaluate_logic(rows, inputs):
    """Evaluate rows in order. Each output becomes an input for the rows after it
    (and for the next tick), so outputs can lock each other out."""
    values = dict(inputs)
    out = {}
    for row in rows:
        out[row.output] = row.evaluate(values)
        values[row.output] = out[row.output]
    return out


def gate(op, a, b=None):
    """Plain logic gates for the HUD / tests."""
    if op == "AND":
        return a and b
    if op == "OR":
        return a or b
    if op == "NOT":
        return not a
    raise ValueError(op)
