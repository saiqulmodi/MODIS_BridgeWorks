"""Questions come in random order without look-alikes back to back (engine/spread.py)."""
import random

from engine import spread
from engine.academy_data import pool


def test_numbers_only_change_is_a_look_alike():
    a = spread.signature("A beam 4 m long carries 10 kN at its centre. Find the reaction.")
    b = spread.signature("A beam 6 m long carries 25 kN at its centre. Find the reaction.")
    c = spread.signature("Which gas do plants take in for photosynthesis?")
    assert spread.look_alike(a, b)
    assert not spread.look_alike(a, c)


def test_order_keeps_look_alikes_apart_in_a_real_pool():
    rng = random.Random(1)
    for cls, subject in ((3, "math"), (9, "physics"), (12, "finance")):
        qs = pool(cls, subject)
        seq = spread.order(qs, rng)
        assert sorted(r["id"] for r in seq) == sorted(r["id"] for r in qs)
        sigs = [spread.signature(r["question"]) for r in seq]
        adjacent = sum(spread.look_alike(sigs[i], sigs[i + 1]) for i in range(len(sigs) - 1))
        bank = [spread.signature(r["question"]) for r in qs]
        in_bank_order = sum(spread.look_alike(bank[i], bank[i + 1]) for i in range(len(bank) - 1))
        assert adjacent <= max(1, in_bank_order // 5)


def test_pick_avoids_recently_shown():
    rng = random.Random(2)
    qs = pool(9, "physics")
    shown = []
    for _ in range(30):
        q = spread.pick([r for r in qs if r not in shown], rng)
        assert q is not None
        shown.append(q)
        spread.remember(q)
    sigs = [spread.signature(r["question"]) for r in shown]
    assert sum(spread.look_alike(sigs[i], sigs[i + 1]) for i in range(len(sigs) - 1)) <= 1
