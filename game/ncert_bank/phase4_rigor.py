"""Phase Four: NIT-Level Rigor Curriculum Bank (Advanced Mechanics & Structures)"""

RIGOR_QUESTIONS = [
    # --- Advanced Structural Analysis ---
    (11, "Structures", "What theorem determines structural determinacy in pin-jointed plane trusses?", "m + r = 2j", ["m = r", "m + r = 2j", "j = r + 2", "m = 2j"]),
    (11, "Structures", "What is the degree of static indeterminacy for a fixed-fixed beam in a 2D plane?", "3", ["1", "2", "3", "6"]),
    (12, "Structures", "In moment distribution method, what is the distribution factor for a fixed support?", "0", ["0", "0.5", "1.0", "Infinity"]),
    (12, "Structures", "What is the carry-over factor for a prismatic beam with a far end fixed?", "1/2", ["1", "1/2", "1/4", "0"]),

    # --- Advanced Mechanics & Shafts ---
    (11, "Mechanics", "What is the polar moment of inertia for a solid circular shaft of diameter d?", "pi * d^4 / 32", ["pi * d^4 / 64", "pi * d^4 / 32", "pi * d^4 / 16", "pi * d^4 / 12"]),
    (12, "Mechanics", "What represents the maximum shear stress theory for yielding (Guest's theory)?", "Tau_max = (sigma_1 - sigma_2) / 2", ["Tau_max = sigma_1 / 2", "Tau_max = (sigma_1 - sigma_2) / 2", "Tau_max = sqrt(sigma_1^2 + sigma_2^2)", "Tau_max = sigma_1 - sigma_2"]),
    (12, "Mechanics", "What is the natural frequency of a simple mass-spring system with mass m and stiffness k?", "sqrt(k/m) / (2*pi)", ["sqrt(k/m)", "sqrt(k/m) / (2*pi)", "2 * pi * sqrt(m/k)", "sqrt(m/k)"]),
]