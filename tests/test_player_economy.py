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

    # Rule 2 & 3: Answering grants 2 marks/rupees + 10 bonus if correct on first attempt
    player.submit_answer("q1", is_correct=True)
    # Total: 1 (read) + 2 (attempt) + 10 (first attempt correct bonus) = 13
    assert player.balance_rupees == 13

    # Subsequent attempt on same question: grants 2 marks/rupees for trying, but NO first-attempt bonus
    player.submit_answer("q1", is_correct=True)
    # Total: 13 + 2 = 15
    assert player.balance_rupees == 15

