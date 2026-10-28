"""
Compiles Class 1-12 & JEE/IIT Engineering Mechanics Question Bank.
Extracts questions from School_MCQ_Bank SQLite database if available,
and combines them with core static mechanics questions.
"""
import os, json, sqlite3, glob

BANK_DEST = os.path.join("data", "questions.json")
SCHOOL_BANK_DIR = os.path.abspath(os.path.join("..", "School_MCQ_Bank"))

core_curriculum = [
    {
        "id": "ENG_11_SOLIDS_001",
        "tier": "Class_11",
        "category": "Mechanical Properties of Solids",
        "question": "In the Bandra-Worli Sea Link stay cables, which property must be maximized to prevent structural sagging under dead and live loads?",
        "options": ["A) Bulk Modulus", "B) Young's Modulus", "C) Shear Modulus", "D) Poisson's Ratio"],
        "correct": 1,
        "explanation": "Young's modulus (Y = longitudinal stress / longitudinal strain) directly governs tensile resistance against axial elongation.",
        "subsidy": 150000
    },
    {
        "id": "ENG_JEE_EQUILIB_002",
        "tier": "JEE_Advanced",
        "category": "Statics & Rotational Equilibrium",
        "question": "For a bridge pylon in static equilibrium subjected to concurrent asymmetric vehicle loads, which condition is mandatory?",
        "options": ["A) ΣFx = 0 only", "B) ΣFy = 0 only", "C) Both ΣF = 0 and Στ = 0 about all axes", "D) Moment of Inertia is zero"],
        "correct": 2,
        "explanation": "Static equilibrium in 3D/2D space mandates zero net translational force (ΣF = 0) and zero net rotational torque (Στ = 0).",
        "subsidy": 300000
    },
    {
        "id": "ENG_11_THERMAL_003",
        "tier": "Class_11",
        "category": "Thermal Expansion",
        "question": "Why are finger-type expansion joints installed every 500m along modern steel bridge spans?",
        "options": [
            "A) To dampen acoustic traffic noise",
            "B) To allow linear expansion (ΔL = α·L·ΔT) without buckling",
            "C) To increase concrete curing speed",
            "D) To ground lightning strikes"
        ],
        "correct": 1,
        "explanation": "Thermal expansion causes continuous length changes. Constrained members experience destructive thermal stress F = Y·A·α·ΔT.",
        "subsidy": 175000
    },
    {
        "id": "ENG_09_NEWTON_004",
        "tier": "Class_09",
        "category": "Forces and Laws of Motion",
        "question": "When a heavy multi-axle freight convoy brakes sharply on a deck, what force does the bridge foundation absorb?",
        "options": ["A) Normal vertical reaction", "B) Horizontal shear friction", "C) Centripetal force", "D) Archimedes buoyant lift"],
        "correct": 1,
        "explanation": "Decelerating freight transmits horizontal shear force to the deck through tyre-surface friction.",
        "subsidy": 75000
    },
    {
        "id": "ENG_JEE_BUCKLE_005",
        "tier": "JEE_Advanced",
        "category": "Structural Mechanics",
        "question": "According to Euler's formula, the critical compressive buckling load P_cr of a slender bridge strut is inversely proportional to:",
        "options": ["A) Young's Modulus E", "B) Moment of Inertia I", "C) Square of the effective length (L_eff²)", "D) Material Density"],
        "correct": 2,
        "explanation": "P_cr = (π² · E · I) / (K · L)². Doubling the length reduces buckling capacity to one-fourth.",
        "subsidy": 350000
    }
]

# Ingest from School_MCQ_Bank databases if found
if os.path.exists(SCHOOL_BANK_DIR):
    db_files = glob.glob(os.path.join(SCHOOL_BANK_DIR, "**", "*.db"), recursive=True)
    print(f"Found {len(db_files)} databases in School_MCQ_Bank.")
    for db in db_files:
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall()]
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                cols = [c[1].lower() for c in cursor.fetchall()]
                if 'question' in cols and 'option_a' in cols:
                    cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_option FROM {table} LIMIT 25;")
                    for row in cursor.fetchall():
                        q_text, oa, ob, oc, od, ans = row
                        c_idx = 0
                        if str(ans).strip().upper() in ['B', '2']: c_idx = 1
                        elif str(ans).strip().upper() in ['C', '3']: c_idx = 2
                        elif str(ans).strip().upper() in ['D', '4']: c_idx = 3
                        core_curriculum.append({
                            "id": f"SCH_{len(core_curriculum)+1}",
                            "tier": "Class_10_12",
                            "category": "Physics & Engineering Foundations",
                            "question": q_text,
                            "options": [f"A) {oa}", f"B) {ob}", f"C) {oc}", f"D) {od}"],
                            "correct": c_idx,
                            "explanation": "Fundamental mechanics and properties of matter concept from NCERT curriculum.",
                            "subsidy": 100000
                        })
            conn.close()
        except Exception as e:
            pass

os.makedirs("data", exist_ok=True)
with open(BANK_DEST, "w", encoding="utf-8") as f:
    json.dump(core_curriculum, f, indent=2)

print(f"Total compiled questions: {len(core_curriculum)} saved to {BANK_DEST}")
