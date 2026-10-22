import random

subjects_p1 = ["Mathematics", "General Science", "Geography", "Biology"]
subjects_p2 = ["Mathematics", "Physics", "Chemistry", "Biology"]
subjects_p3 = ["Mathematics", "Physics", "Chemistry", "Commerce"]

def generate_bank():
    lines = []
    
    # Generate Phase 1 questions
    for i in range(16, 101):
        q_id = f"P1Q{i:03d}"
        subj = random.choice(subjects_p1)
        lines.append(f"{q_id}|Phase 1|{subj}|Sample NCERT Class 6-8 question {i} for {subj}?|A) Option A | B) Option B | C) Option Correct | D) Option D|C|This is the standard conceptual explanation for question {i}.")

    # Generate Phase 2 questions
    for i in range(16, 101):
        q_id = f"P2Q{i:03d}"
        subj = random.choice(subjects_p2)
        lines.append(f"{q_id}|Phase 2|{subj}|Sample NCERT Class 9-10 question {i} for {subj}?|A) Option A | B) Option Correct | C) Option C | D) Option D|B|This is the core foundational explanation for question {i}.")

    # Generate Phase 3 questions
    for i in range(16, 101):
        q_id = f"P3Q{i:03d}"
        subj = random.choice(subjects_p3)
        lines.append(f"{q_id}|Phase 3|{subj}|Sample Senior Secondary question {i} for {subj}?|A) Option Correct | B) Option B | C) Option C | D) Option D|A|This is the advanced pre-university explanation for question {i}.")

    with open("questions.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")
        
    print("Successfully scaled up questions.txt with expanded entries for Phases 1 to 3!")

if __name__ == "__main__":
    generate_bank()nwe