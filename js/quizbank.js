// Graded Curriculum Bank: Class 1-7 through JEE/IIT Mechanics
const QuizBank = [
    {
        id: "PHYS_01_RIGID_01",
        stage: 1,
        tier: "Class 1–7",
        category: "Geometric Rigidity & Levers",
        question: "Why does a triangular structural frame resist deformation under a point load better than a square frame?",
        options: [
            "A) Triangles have higher density",
            "B) Triangle angles are geometrically locked by fixed side lengths",
            "C) Triangles have zero gravity acting on them",
            "D) Square frames have lower friction at pin joints"
        ],
        correct: 1,
        explanation: "Side-Side-Side (SSS) congruence locks a triangle's interior angles without allowing hinge shearing.",
        subsidy: 50000
    },
    {
        id: "PHYS_02_TRUSS_02",
        stage: 2,
        tier: "Class 8–10",
        category: "Coplanar Trusses & Equilibrium",
        "question": "For a statically determinate pin-jointed bridge truss in coplanar equilibrium, which pair of equations must be satisfied at every joint?",
        options: [
            "A) ΣFx = 0 and ΣFy = 0",
            "B) ΣF = m·a and Στ = I·α",
            "C) W = F·d and P = W/t",
            "D) F_net = constant"
        ],
        correct: 0,
        explanation: "Static translational equilibrium requires zero net force vectors along both orthogonal axes.",
        subsidy: 150000
    },
    {
        id: "PHYS_03_SOLID_03",
        stage: 3,
        tier: "Class 11–12",
        category: "Mechanical Properties of Solids",
        question: "A steel stay cable experiences an axial tensile stress σ within its elastic limit. What defines its Young's Modulus Y?",
        options: [
            "A) Shear stress / Lateral strain",
            "B) Tensile stress / Longitudinal strain (σ / ε)",
            "C) Hydraulic pressure / Volume strain",
            "D) Fracture load / Cross-sectional area"
        ],
        correct: 1,
        explanation: "Hooke's Law states that within proportional elastic limits, longitudinal stress is directly proportional to longitudinal strain.",
        subsidy: 250000
    },
    {
        id: "PHYS_04_BUCKLE_04",
        stage: 4,
        tier: "JEE Advanced",
        category: "Compressive Stability & Torsion",
        question: "According to Euler's buckling theory, pinning both ends of an axial compressive column causes its critical buckling load P_cr to depend on length as:",
        options: [
            "A) Inversely proportional to L² (P_cr ∝ 1/L²)",
            "B) Directly proportional to L²",
            "C) Linearly proportional to L",
            "D) Independent of column length"
        ],
        correct: 0,
        explanation: "Euler critical buckling formula: P_cr = (π²·E·I) / (K·L)². For pinned ends (K=1), P_cr scales inversely with L².",
        subsidy: 400000
    },
    {
        id: "PHYS_05_FEM_05",
        stage: 5,
        tier: "IIT / NIT Mechanics",
        category: "Finite Element Method & Dynamics",
        question: "In computational finite element analysis (FEM) of large bridge spans, how is the global stiffness equation formulated?",
        options: [
            "A) [K]{u} = {F}",
            "B) [M]{a} = 0",
            "C) [C]{v} = {F}",
            "D) {u} = [K]⁻¹"
        ],
        correct: 0,
        explanation: "The fundamental matrix equilibrium relation connects the global stiffness matrix [K] and nodal displacements {u} with applied forces {F}.",
        subsidy: 750000
    }
];
if (typeof module !== "undefined") module.exports = QuizBank;
