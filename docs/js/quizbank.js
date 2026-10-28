// Comprehensive National (NCERT) & International Standards Question Bank
const QuizBank = [
    // --- TENSION FIBERS: CLASS 1 TO 7 SYLLABUS ---
    {
        id: "TF_C17_01",
        stage: 1,
        tier: "Class 1–7 (NCERT / STEM)",
        category: "Geometric Rigidity & Shapes",
        question: "Why do engineers use triangles instead of squares when lashing bamboo or timber frames?",
        options: [
            "A) Triangles are lighter in weight",
            "B) Triangle angles cannot deform without changing side lengths (SSS Rule)",
            "C) Square frames attract more moisture and rot faster",
            "D) Triangles eliminate the force of gravity"
        ],
        correct: 1,
        explanation: "By the Side-Side-Side (SSS) geometric rule, a triangle cannot change its shape without bending or breaking its sides, providing structural rigidity.",
        clue: "Think about diagonal bracing: squares need a diagonal to lock their corners into two triangles."
    },
    {
        id: "TF_C17_02",
        stage: 1,
        tier: "Class 1–7 (NCERT / STEM)",
        category: "Forces, Tension & Gravity",
        question: "When a person walks across a natural fiber rope bridge, where does the greatest tensile pulling force occur?",
        options: [
            "A) In the main upper cables near the riverbank anchorages",
            "B) In the vertical safety handrail nets",
            "C) Only on the wooden footpath planks",
            "D) Air pressure carries the load"
        ],
        correct: 0,
        explanation: "The entire weight of the deck and crossing loads is transferred upward along the catenary curve to the anchorages on the solid banks.",
        clue: "The anchors absorb both the downward weight (vertical reaction) and the inward pull (horizontal tension)."
    },
    {
        id: "TF_C17_03",
        stage: 1,
        tier: "Class 1–7 (International STEM)",
        category: "Catenary Curves & Cable Sag",
        question: "Why can a rope bridge NEVER be pulled into a perfectly straight horizontal line across a gorge?",
        options: [
            "A) The ropes are too heavy to stretch",
            "B) A zero-sag cable requires infinite tension to balance downward gravity (T = W / 2·sin θ)",
            "C) Air resistance pushes the center downward",
            "D) Earth's magnetic field curves all long fibers"
        ],
        correct: 1,
        explanation: "As the sag angle approaches zero, sin(θ) approaches 0. To support even 1 kg vertically, the horizontal tension would have to be infinitely large.",
        clue: "Every suspension cable must sag slightly so the angled tension vector has a vertical upward component."
    },
    {
        id: "TF_C17_04",
        stage: 1,
        tier: "Class 1–7 (NCERT Materials)",
        category: "Natural Fiber Properties",
        question: "Why are living Ficus elastica tree roots in Meghalaya twisted into bundles rather than using single thick branches?",
        options: [
            "A) Bundled fibers share tensile strain and continue growing stronger together over decades",
            "B) Single roots cannot conduct water across rivers",
            "C) Twisted roots become lighter than air",
            "D) Bundling prevents leaves from growing"
        ],
        correct: 0,
        explanation: "Bundling multiple roots allows individual fibers to intertwine, self-reinforce via secondary growth, and prevent catastrophic single-point failures.",
        clue: "Living root bridges are dynamic bio-engineering structures that gain load capacity with age."
    },

    // --- COPLANAR TRUSSES: CLASS 8 TO 10 ---
    {
        id: "CT_C810_01",
        stage: 2,
        tier: "Class 8–10",
        category: "Method of Joints & Vectors",
        question: "In a pin-jointed truss under static equilibrium, what must be true for the concurrent forces at any joint?",
        options: ["A) ΣFx = 0 and ΣFy = 0", "B) ΣF = m·a", "C) Kinetic energy is maximized", "D) All members must be in tension"],
        correct: 0,
        explanation: "Static equilibrium requires translational balance along both horizontal and vertical axes.",
        clue: "Break every member force into its cosine and sine components."
    },

    // --- PARABOLIC THRUST: CLASS 11 TO 12 ---
    {
        id: "PT_C1112_01",
        stage: 3,
        tier: "Class 11–12",
        category: "Elasticity & Hooke's Law",
        question: "A steel cable of length L and cross-section A is under tension F. What is its elastic elongation?",
        options: ["A) ΔL = (F·L)/(A·Y)", "B) ΔL = (F·A)/(L·Y)", "C) ΔL = (Y·L)/(F·A)", "D) ΔL = (F·Y)/(A·L)"],
        correct: 0,
        explanation: "From Hooke's law: stress = Y × strain => F/A = Y × (ΔL/L) => ΔL = (F·L)/(A·Y).",
        clue: "Young's modulus Y relates stress directly to elongation strain."
    },

    // --- STAY DYNAMICS & MATRIX: JEE & IIT ---
    {
        id: "SD_JEE_01",
        stage: 4,
        tier: "JEE Advanced",
        category: "Euler Buckling",
        question: "Euler critical buckling load P_cr for a pinned compressive strut scales with length L as:",
        options: ["A) P_cr ∝ 1 / L²", "B) P_cr ∝ L²", "C) P_cr ∝ 1 / L", "D) P_cr ∝ L"],
        correct: 0,
        explanation: "Euler's formula: P_cr = (π²·E·I)/(K·L)². For pinned ends (K=1), capacity drops with the square of length.",
        clue: "Doubling the strut length reduces its buckling limit by a factor of 4."
    }
];
if (typeof module !== "undefined") module.exports = QuizBank;
