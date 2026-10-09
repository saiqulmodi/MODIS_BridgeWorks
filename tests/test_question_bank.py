"""Big question banks (engine/question_bank.py, tools/build_bank.py): build a small bank, load it lazily,
show it in the Academy and pay grants, and never crash on a missing or broken bank."""
import csv
import json
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools"))

import build_bank  # noqa: E402
from engine import academy_data, question_bank  # noqa: E402
from engine.academy import class_label  # noqa: E402

FIELDS = ["id", "class_level", "subject", "question", "option_a", "option_b", "option_c", "option_d",
          "correct_option", "explanation", "question_bn", "option_a_bn", "option_b_bn", "option_c_bn",
          "option_d_bn", "explanation_bn"]


def _row(i, level, subject, q, opts, ans, bn=None):
    r = dict(id=i, class_level=level, subject=subject, question=q, option_a=opts[0], option_b=opts[1],
             option_c=opts[2], option_d=opts[3], correct_option=ans, explanation=f"Because {i}.")
    if bn:
        r.update(question_bn=bn[0], option_a_bn=bn[1][0], option_b_bn=bn[1][1], option_c_bn=bn[1][2],
                 option_d_bn=bn[1][3], explanation_bn=bn[2])
    return r


@pytest.fixture
def bank(tmp_path, monkeypatch):
    rows = [_row(i, 15, "Physics", f"Olympiad question {i}?", [f"a{i}", f"b{i}", f"c{i}", f"d{i}"], "B")
            for i in range(1, 2501)]
    rows += [_row(3001, 7, "EVS", "Which gas do plants take in?", ["Carbon dioxide", "Oxygen", "Helium", "Neon"], "A",
                  ("উদ্ভিদ কোন গ্যাস গ্রহণ করে?", ["কার্বন ডাইঅক্সাইড", "অক্সিজেন", "হিলিয়াম", "নিয়ন"], "সালোকসংশ্লেষে।")),
             _row(3002, 7, "Mathematics", "What is 7 x 8 in this bank?", ["56", "54", "64", "48"], "1"),
             _row(3003, 7, "Mathematics", "What is 7 x 8 in this bank?", ["56", "54", "64", "48"], "A"),  # repeat
             _row(3004, 7, "Physics", "Broken?", ["x", "x", "y", "z"], "A"),                              # bad options
             _row(3005, 99, "Physics", "Unknown level?", ["p", "q", "r", "s"], "A")]                      # bad level
    src = tmp_path / "src.csv"
    with open(src, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    out = tmp_path / "banks"
    build_bank.main(["--id", "olymp", "--title", "Test Olympiad Bank", "--title-bn", "পরীক্ষার অলিম্পিয়াড",
                     "--csv", str(src), "--out", str(out),
                     "--new-level", "15=International Olympiad|আন্তর্জাতিক অলিম্পিয়াড"])
    monkeypatch.delenv("BRIDGEWORKS_NO_BANKS", raising=False)
    question_bank.set_root(str(out))
    yield out
    question_bank.set_root(question_bank.ROOT)


def test_converter_checks_rows_and_splits_into_chunks(bank):
    meta = json.loads((bank / "olymp" / "bank.json").read_text(encoding="utf-8"))
    assert meta["total"] == 2502                       # 2,500 olympiad + EVS + one maths (repeat and bad rows dropped)
    assert meta["chunks"]["15/physics"] == ["15_physics_1.json", "15_physics_2.json", "15_physics_3.json"]
    assert meta["subjects"]["evs"] == ["EVS", "পরিবেশ পরিচিতি"]
    assert json.loads((bank / "index.json").read_text())["banks"] == ["olymp"]


def test_levels_subjects_and_pools(bank):
    assert academy_data.levels()[-1] == 15
    assert class_label(15) == "International Olympiad" and class_label(15, "bn") == "আন্তর্জাতিক অলিম্পিয়াড"
    assert "evs" in academy_data.subjects()
    pool = academy_data.pool(15, "physics")
    assert len(pool) == 2500 and pool[0]["id"] == "olymp:1" and pool[0]["correct_idx"] == 1
    assert pool[0]["grant_reward"] == academy_data.grant_reward(15)
    maths = academy_data.pool(7, "math")
    assert len(maths) == 100 + 1                       # built-in Class 7 maths plus the bank's one
    evs = academy_data.pool(7, "evs")[0]
    assert evs["question_bn"].startswith("উদ্ভিদ") and not evs["bn_missing"]
    assert academy_data.pool(15, "physics")[5]["bn_missing"]          # English shown in Bengali mode


def test_only_the_opened_piece_is_read(bank):
    academy_data.pool(7, "evs")
    assert not any(k[1].startswith("15_") for k in question_bank._chunks)


def test_broken_or_missing_banks_never_crash(bank, tmp_path):
    (bank / "olymp" / "15_physics_2.json").write_text("{not json", encoding="utf-8")
    question_bank.set_root(str(bank))
    assert len(academy_data.pool(15, "physics")) == 1500     # the 1,000 in the broken piece are skipped
    assert question_bank.errors
    question_bank.set_root(str(tmp_path / "nowhere"))
    assert academy_data.levels()[-1] == 14 and academy_data.pool(15, "physics") == []


def test_academy_screen_shows_bank_levels_and_pays_grants(bank, tmp_path):
    from game.app import App
    from game.save import Save
    from game.scenes.academy import AcademyScene
    app = App(save=Save(str(tmp_path / "s.json")), headless=True)
    scene = AcademyScene(app)
    assert 15 in scene.class_btns and "evs" in scene.subject_btns
    scene.pick_class(15)
    scene.pick_subject("physics")
    scene.update(0.016)
    assert scene.subject_btns["physics"].label.endswith("0/2500")
    card = scene.card
    assert card.r["id"].startswith("olymp:")
    card.choose(card.r["correct_idx"])
    assert app.save.wallet == academy_data.grant_reward(15)
    app.frame([], 1 / 30)
