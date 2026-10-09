import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engine.game_logic import load_game_state, save_game_state, get_random_question, submit_answer
from engine import daily_limit

QUESTIONS_FILE = "questions.txt"

def load_questions_from_file():
    default_db = {
        "1": [
            {"id": "p1_q1", "question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "answer": "12"},
            {"id": "p1_q2", "question": "Which shape has 3 straight sides?", "options": ["Square", "Triangle", "Circle", "Rectangle"], "answer": "Triangle"}
        ]
    }
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    parsed_data = json.loads(content)
                    if isinstance(parsed_data, dict) and len(parsed_data) > 0:
                        return parsed_data
        except (json.JSONDecodeError, Exception):
            pass
    return default_db

def main():
    questions_db = load_questions_from_file()
    
    while True:
        state = load_game_state()
        
        print("\n" + "=" * 60)
        print("       MODIS BRIDGEWORKS - NATIONAL FOUNDATION SYSTEM       ")
        print("=" * 60)
        print(f"Player: {state.get('player_name', 'Student')} | Current Phase: {state.get('phase', 1)} | Wallet: ₹{state.get('wallet', 0)}")
        print(f"Answers left today: {daily_limit.answers_left(state)}/{daily_limit.DAILY_ANSWER_LIMIT} (any phase)")
        print("-" * 60)
        print("1. Play & Earn (Answer Questions)")
        print("2. Change Phase (1 to 5)")
        print("3. View Wallet & Progress")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            if daily_limit.answers_left(state) == 0:
                print(f"\nDaily limit reached: {daily_limit.DAILY_ANSWER_LIMIT} answers today. "
                      "Logging in again does not reset it. Come back tomorrow!")
                continue
            phase = str(state.get("phase", 1))
            question = get_random_question(phase, questions_db)
            
            if not question:
                print(f"\n🎉 Amazing! You have completed all questions in Phase {phase}.")
                if int(phase) < 5:
                    state["phase"] = int(phase) + 1
                    save_game_state(state)
                    print(f"🚀 Automatic Promotion! You have been advanced to Phase {state['phase']}.")
                continue
                
            print(f"\n[Phase {phase} Question]")
            print(f"Q: {question['question']}")
            for idx, opt in enumerate(question['options']):
                print(f"  {idx + 1}. {opt}")
                
            ans_choice = input("\nEnter your option (1-4) or type the exact answer: ").strip()
            
            selected_answer = ans_choice
            if ans_choice.isdigit() and 1 <= int(ans_choice) <= len(question['options']):
                selected_answer = question['options'][int(ans_choice) - 1]
                
            is_correct, earned, total_wallet, promoted = submit_answer(question['id'], selected_answer, question['answer'], questions_db)
            
            print("\n" + ("-" * 40))
            if is_correct:
                print("Result: CORRECT! 🎉")
                print(f"Earned: ₹{earned} (₹10 Attempt + ₹90 Correct Answer Bonus)")
            else:
                print(f"Result: Incorrect. (Correct Answer was: {question['answer']})")
                print(f"Earned: ₹{earned} (₹10 Attempt Reward)")
            print(f"Updated Wallet Balance: ₹{total_wallet}")
            
            if promoted:
                print(f"\n🚀 CONGRATULATIONS! Phase cleared! You've been automatically promoted to Phase {load_game_state()['phase']}!")
            print("-" * 40)
            
        elif choice == "2":
            print("\nSelect Phase:")
            print("  Phase 1: Classes 1-3 (Early Foundation)")
            print("  Phase 2: Classes 4-6 (Core Concepts)")
            print("  Phase 3: Classes 7-9 (Pre-Engineering Bridge)")
            print("  Phase 4: Classes 10-12 / NIT Target")
            print("  Phase 5: IIT / Elite Engineering & Business")
            new_phase = input("\nEnter phase number (1-5): ").strip()
            if new_phase in ["1", "2", "3", "4", "5"]:
                state["phase"] = int(new_phase)
                save_game_state(state)
                print(f"Phase successfully updated to Phase {new_phase}!")
            else:
                print("Invalid phase selection. Choose between 1 and 5.")
                
        elif choice == "3":
            print(f"\n--- Player Status ---")
            print(f"Name: {state.get('player_name', 'Student')}")
            print(f"Current Phase: {state.get('phase', 1)}")
            print(f"Total Wallet Balance: ₹{state.get('wallet', 0)}")
            print(f"Total Questions Attempted: {len(state.get('attempted_ids', []))}")
            
        elif choice == "4":
            print("\nKeep building your foundation! Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select a number between 1 and 4.")

if __name__ == "__main__":
    main()