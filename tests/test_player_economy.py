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

