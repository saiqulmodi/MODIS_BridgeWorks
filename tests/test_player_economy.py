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




def test_login_limit_25_answers_and_relogin_gives_25_more():
    save = {}
    player = PlayerProfile(name="Student Player", data=save)
    for i in range(25):
        assert player.submit_answer(f"p{i % 5}_{i}", is_correct=True) == 102
    assert player.balance_rupees == 25 * 102
    assert player.answers_left() == 0
    # The 26th answer in the same login pays nothing, in any phase
    assert player.submit_answer("p4_99", is_correct=True) is None
    assert player.balance_rupees == 2550

    # Logging in again with the same name on the same device: wallet kept, 25 fresh answers
    again = PlayerProfile(name="Student Player", data=save)
    assert again.balance_rupees == 2550
    assert again.answers_left() == 25
    assert again.submit_answer("p1_50", is_correct=True) == 102
    assert again.balance_rupees == 2652
    # A question already paid its 100 pays only the 2 for trying
    assert again.submit_answer("p0_0", is_correct=True) == 2


def test_console_game_login_limit(tmp_path, monkeypatch):
    from engine import game_logic, login_limit
    monkeypatch.setattr(game_logic, "SAVE_FILE", str(tmp_path / "save.json"))
    for i in range(25):
        ok, earned, wallet, _ = game_logic.submit_answer(f"q{i}", "12", "12")
        assert ok and earned == 100
    ok, earned, wallet, promoted = game_logic.submit_answer("q99", "12", "12")
    assert earned is None and wallet == 2500 and not promoted
    # Log in again: 25 more
    state = game_logic.load_game_state()
    login_limit.start_login(state)
    game_logic.save_game_state(state)
    ok, earned, wallet, _ = game_logic.submit_answer("q100", "12", "12")
    assert earned == 100 and wallet == 2600
