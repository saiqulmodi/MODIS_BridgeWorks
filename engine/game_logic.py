import json
import random
import os

from engine import daily_limit

SAVE_FILE = "save.json"

def load_game_state():
    """Loads the player session and wallet state safely with defaults."""
    default_state = {
        "player_name": "Student",
        "wallet": 0,
        "phase": 1,
        "attempted_ids": []
    }
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                for k, v in default_state.items():
                    if k not in data:
                        data[k] = v
                return data
        except json.JSONDecodeError:
            pass
    return default_state

def save_game_state(state):
    """Saves the current session and wallet state to save.json."""
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def get_random_question(phase_number, all_questions_dict):
    """
    Fetches a random unattempted question for the given phase.
    all_questions_dict format: {phase_id: [ {id, question, options, answer}, ... ]}
    """
    state = load_game_state()
    attempted = set(state.get("attempted_ids", []))
    
    phase_pool = all_questions_dict.get(str(phase_number), [])
    available = [q for q in phase_pool if q["id"] not in attempted]
    
    if not available:
        return None  # All questions in this phase completed!
        
    return random.choice(available)

def submit_answer(question_id, user_choice, correct_choice, all_questions_dict=None):
    """
    Processes the answer submission:
    - Awards ₹10 for attempting.
    - Awards an extra ₹90 (+₹100 total) if correct.
    - Checks if phase is complete and automatically promotes player if true.
    - At most daily_limit.DAILY_ANSWER_LIMIT answers a day: past that nothing is paid or
      recorded and earned is None.
    """
    state = load_game_state()
    is_correct = (str(user_choice).strip().lower() == str(correct_choice).strip().lower())
    if not daily_limit.use_answer(state):
        return is_correct, None, state["wallet"], False
    
    # Track attempted question ID
    if question_id not in state["attempted_ids"]:
        state["attempted_ids"].append(question_id)
    
    earned = 10  # Base attempt reward
    
    if is_correct:
        earned += 90  # Correct answer bonus (Total ₹100)
        
    state["wallet"] += earned
    
    # Automatic Phase Promotion Check
    promoted = False
    if all_questions_dict:
        current_phase = str(state["phase"])
        phase_pool = all_questions_dict.get(current_phase, [])
        attempted = set(state["attempted_ids"])
        
        # Check if all questions in the current phase have been attempted
        remaining_in_phase = [q for q in phase_pool if q["id"] not in attempted]
        if not remaining_in_phase and state["phase"] < 5:
            state["phase"] += 1
            promoted = True

    save_game_state(state)
    
    return is_correct, earned, state["wallet"], promoted