import json
import os
from engine.game_logic import GameLogic

class BridgeWorksAutoSolver:
    def __init__(self, save_path="data/save.json"):
        self.save_path = save_path
        self.game = GameLogic()

    def run_auto_win(self):
        """Simulates answering all questions correctly across all 5 phases."""
        total_earnings = 0
        solved_count = 0

        # Loop through all 5 phases
        for phase in range(1, 6):
            self.game.current_phase = phase
            while True:
                q = self.game.get_next_question()
                if not q:
                    break
                
                # ₹10 attempt + ₹90 correct answer bonus = ₹100 per question
                total_earnings += 100
                q_id = q.get("id")
                if q_id and q_id not in self.game.completed_questions:
                    self.game.completed_questions.append(q_id)
                solved_count += 1

        self.game.wallet += total_earnings
        self.save_progress(solved_count)

    def save_progress(self, solved_count):
        """Persists updated state directly to data/save.json"""
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        state = {
            "wallet": self.game.wallet,
            "completed_questions": self.game.completed_questions,
            "current_phase": 5
        }
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
        
        print(f"[✔] Successfully auto-solved {solved_count} questions across all phases.")
        print(f"[💰] Total Earnings Credited: ₹{self.game.wallet} | Updated Wallet Balance: ₹{self.game.wallet}")

if __name__ == "__main__":
    solver = BridgeWorksAutoSolver()
    solver.run_auto_win()