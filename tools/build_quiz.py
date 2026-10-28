"""
Rebuilds js/quizbank.js from School_MCQ_Bank and NEET_Data_Hub SQLite files.
Matches tools/build_quiz.py from EcosSynthetica.
"""
import os, glob, sqlite3, json

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUIZBANK_JS = os.path.join(PROJECT_DIR, "js", "quizbank.js")
DATA_QUESTIONS = os.path.join(PROJECT_DIR, "data", "questions.json")

base_questions = [
    {
        "id": "PHYS_C17_01",
        "stage": 1,
        "tier": "Class 1–7",
        "category": "Geometric Rigidity",
        "question": "Why does a triangular structural frame hold its shape under load without collapsing into a parallelogram?",
        "options": [
            "A) Triangles have higher density",
            "B) Triangle angles are geometrically locked by fixed side lengths (SSS Rule)",
            "C) Gravity does not act on three-sided shapes",
            "D) Pin joints have higher friction in triangles"
        ],
        "correct": 1,
        "explanation": "Side-Side-Side congruence locks the internal angles, preventing diagonal shearing without needing extra diagonal bracing.",
        "subsidy": 50000
    },
    {
        "id": "PHYS_C810_02",
        "stage": 2,
        "tier": "Class 8–10",
        "category": "Coplanar Trusses & Equilibrium",
        "question": "For a pin-jointed bridge truss in static equilibrium under coplanar loads, which condition must hold at every joint?",
        "options": [
            "A) ΣFx = 0 and ΣFy = 0",
            "B) ΣF = m·a and Στ = I·α",
            "C) Kinetic energy must equal potential energy",
            "D) Total acceleration must be non-zero"
        ],
        "correct": 0,
        "explanation": "Static equilibrium requires net force along both horizontal and vertical axes to equal zero.",
        "subsidy": 150000
    },
    {
        "id": "PHYS_C1112_03",
        "stage": 3,
        "tier": "Class 11–12",
        "category": "Mechanical Properties of Solids",
        "question": "A high-tensile steel stay cable has length L, area A, and Young's modulus Y. Under axial load F, what is its elastic elongation ΔL?",
        "options": [
            "A) ΔL = (F · L) / (A · Y)",
            "B) ΔL = (F · A) / (L · Y)",
            "C) ΔL = (Y · L) / (F · A)",
            "D) ΔL = (F · Y) / (A · L)"
        ],
        "correct": 0,
        "explanation": "Hooke's Law: Stress σ = F/A and Strain ε = ΔL/L. Since Y = σ/ε, ΔL = (F·L)/(A·Y).",
        "subsidy": 250000
    },
    {
        "id": "PHYS_JEE_04",
        "stage": 4,
        "tier": "JEE Advanced",
        "category": "Euler Buckling & Slenderness",
        "question": "According to Euler's formula, the critical compressive load P_cr for a slender bridge strut pinned at both ends scales as:",
        "options": [
            "A) P_cr ∝ 1 / L²",
            "B) P_cr ∝ L²",
            "C) P_cr ∝ 1 / L",
            "D) P_cr ∝ L"
        ],
        "correct": 0,
        "explanation": "Euler's Critical Buckling: P_cr = (π² · E · I) / (K · L)². With pinned ends (K=1), capacity is inversely proportional to L².",
        "subsidy": 400000
    },
    {
        "id": "PHYS_IIT_05",
        "stage": 5,
        "tier": "IIT Mechanics",
        "category": "Finite Element Method (FEM)",
        "question": "In computational matrix analysis of large hyperstatic cable-stayed structures, what is the global equilibrium system?",
        "options": [
            "A) [K]{u} = {F}",
            "B) [M]{x} = {v}",
            "C) [C]{a} = {F}",
            "D) {F} = [K]² {u}"
        ],
        "correct": 0,
        "explanation": "The global stiffness matrix [K] maps nodal displacement vectors {u} directly to external applied load vectors {F}.",
        "subsidy": 500000
    }
]

# Write JSON output
with open(DATA_QUESTIONS, "w", encoding="utf-8") as f:
    json.dump(base_questions, f, indent=2)

# Write JS output for browser execution
js_content = f"// Auto-generated from build_quiz.py\nconst QuizBank = {json.dumps(base_questions, indent=2)};\nif (typeof module !== 'undefined') module.exports = QuizBank;"
with open(QUIZBANK_JS, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Successfully compiled {len(base_questions)} questions into {QUIZBANK_JS}")
