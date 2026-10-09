"""Tests for Player Profile registration and rupee scoring economy rules."""
import pytest
from game.player_economy import PlayerProfile

def test_player_registration_and_scoring():
    # Registration: Name mandatory, phone/email optional
    player = PlayerProfile(name="Student Player", phone="", email="")
    assert player.name == "Student Player"
    assert player.balance_rupees == 0

    # Rule 1: Reading grants 1 mark/rupee (only once per item)
    player.read_content("q1")
    player.read_content("q1") # Duplicate read should not re-add
    assert player.balance_rupees == 1

    # Rule 2 & 3: every attempt grants 2 rupees; the first correct answer grants 100
    player.submit_answer("q1", is_correct=True)
    # Total: 1 (read) + 2 (attempt) + 100 (correct answer) = 103
    assert player.balance_rupees == 103

    # Answering the same question again: 2 rupees for trying, but NO second 100
    player.submit_answer("q1", is_correct=True)
    # Total: 103 + 2 = 105
    assert player.balance_rupees == 105

    # A wrong attempt still pays for trying; getting it right later still earns the 100 once
    player.read_content("q2")
    player.submit_answer("q2", is_correct=False)
    assert player.balance_rupees == 105 + 1 + 2
    player.submit_answer("q2", is_correct=True)
    assert player.balance_rupees == 108 + 2 + 100



def test_daily_limit_25_answers_survives_relogin():
    import datetime
    day = datetime.date(2026, 10, 9)
    save = {}
    player = PlayerProfile(name="Student Player", data=save, today=day)
    for i in range(25):
        assert player.submit_answer(f"p{i % 5}_{i}", is_correct=True) == 102
    assert player.balance_rupees == 25 * 102
    assert player.answers_left() == 0
    # The 26th answer pays nothing, in any phase
    assert player.submit_answer("p4_99", is_correct=True) is None
    assert player.balance_rupees == 2550

    # Logging in again (same or a new name) on the same save does not give another 25
    again = PlayerProfile(name="student player", data=save, today=day)
    assert again.balance_rupees == 2550
    assert again.submit_answer("p1_50", is_correct=True) is None
    other = PlayerProfile(name="New Name", data=save, today=day)
    assert other.submit_answer("p1_51", is_correct=True) is None

    # Already-paid questions stay paid after a new login
    tomorrow = PlayerProfile(name="Student Player", data=save, today=day + datetime.timedelta(days=1))
    assert tomorrow.answers_left() == 25
    assert tomorrow.submit_answer("p0_0", is_correct=True) == 2


def test_console_game_daily_limit(tmp_path, monkeypatch):
    from engine import game_logic
    monkeypatch.setattr(game_logic, "SAVE_FILE", str(tmp_path / "save.json"))
    for i in range(25):
        ok, earned, wallet, _ = game_logic.submit_answer(f"q{i}", "12", "12")
        assert ok and earned == 100
    ok, earned, wallet, promoted = game_logic.submit_answer("q99", "12", "12")
    assert earned is None and wallet == 2500 and not promoted
