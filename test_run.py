from engine.game_logic import load_game_state, save_game_state, get_random_question, submit_answer
from engine import login_limit
import os

# Load player session (each run is a login: 25 fresh answers)
state = load_game_state()
login_limit.start_login(state)
save_game_state(state)
print(f"Welcome back, {state.get('player_name', 'Student')}! Current Phase: {state.get('phase', 1)} | Current Wallet: ₹{state.get('wallet', 0)}")

# Comprehensive multi-phase question database (covering Phases 1 to 5)
# You can expand these arrays or link them to your questions.txt loader
questions_db = {
    "1": [
        {"id": "p1_q1", "question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "answer": "12"},
        {"id": "p1_q2", "question": "Which shape has 3 sides?", "options": ["Square", "Triangle", "Circle", "Rectangle"], "answer": "Triangle"}
    ],
    "2": [
        {"id": "p2_q1", "question": "What is 1/2 expressed as a percentage?", "options": ["25%", "50%", "75%", "100%"], "answer": "50%"}
    ],
    "3": [
        {"id": "p3_q1", "question": "What is the chemical symbol for Water?", "options": ["O2", "H2O", "CO2", "NaCl"], "answer": "H2O"}
    ],
    "4": [
        {"id": "p4_q1", "question": "What is the derivative of x^2 with respect to x?", "options": ["x", "2x", "x^2", "2"], "answer": "2x"},
        {"id": "p4_q2", "question": "Which law states that pressure is inversely proportional to volume at constant temperature?", "options": ["Boyle's Law", "Charles's Law", "Gay-Lussac's Law", "Avogadro's Law"], "answer": "Boyle's Law"}
    ],
    "5": [
        {"id": "p5_q1", "question": "What is the quantum number that describes the orientation of an orbital in space?", "options": ["Principal", "Azimuthal", "Magnetic", "Spin"], "answer": "Magnetic"}
    ]
}

# More questions: the whole BridgeWorks Academy bank (English), sorted into the 5 phases.
#   Phase 1: Classes 1-3   Phase 2: Classes 4-6   Phase 3: Classes 7-9
#   Phase 4: Classes 10-12 + NIT level (JEE Main)
#   Phase 5: IIT level (JEE Advanced) + Game skills (bridge engineering, from the Help screen)
from engine.academy_data import all_items
from engine.academy_skills import items as skill_items


def _phase_of(class_level):
    if class_level in (0, 14):          # Game skills, IIT
        return "5"
    if class_level == 13:               # NIT
        return "4"
    return str((class_level - 1) // 3 + 1)


for _r in all_items() + skill_items():
    questions_db[_phase_of(_r["class_level"])].append({
        "id": f"a{_r['id']}", "question": _r["question"], "options": _r["options"],
        "answer": _r["options"][_r["correct_idx"]]})

print("Question bank: " + ", ".join(f"Phase {k}: {len(v)}" for k, v in sorted(questions_db.items())))

# Fetch a random question for the player's current phase
current_q = get_random_question(state.get("phase", 1), questions_db)

if current_q:
    print(f"\n[Phase {state.get('phase', 1)}] {current_q['question']}")
    for idx, opt in enumerate(current_q['options']):
        print(f"  {idx+1}. {opt}")
        
    # Simulate answering correctly
    user_answer = current_q['answer']
    is_correct, earned, total_wallet, promoted = submit_answer(current_q["id"], user_answer, current_q["answer"], questions_db)
    
    if earned is None:
        print("\n25 answers used for this login. Nothing paid. Log in again for 25 more.")
    else:
        print(f"\nResult: {'Correct! 🎉' if is_correct else 'Incorrect.'}")
        print(f"Earned this round: ₹{earned} (₹10 attempt + ₹90 correct bonus)")
    print(f"Updated Wallet Balance: ₹{total_wallet}")
    if promoted:
        print("Phase complete! You have been promoted to the next phase.")
else:
    print(f"All questions completed for Phase {state.get('phase', 1)}! Ready to advance or reset attempted IDs.")