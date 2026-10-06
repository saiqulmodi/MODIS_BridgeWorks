"""Phase Three: Core Engineering Curriculum Bank (Strength of Materials & Structures)"""

ENGINEERING_QUESTIONS = [
    # --- Mechanics of Materials & Stress-Strain ---
    (8, "Engineering", "What is the ratio of lateral strain to longitudinal strain known as?", "Poisson's ratio", ["Young's modulus", "Poisson's ratio", "Bulk modulus", "Rigidity modulus"]),
    (8, "Engineering", "Hooke's law states that within elastic limits, stress is directly proportional to:", "Strain", ["Strain", "Pressure", "Temperature", "Load"]),
    (9, "Engineering", "What type of stress is induced when a member is subjected to equal and opposite pull forces?", "Tensile stress", ["Compressive stress", "Tensile stress", "Shear stress", "Torsional stress"]),
    (9, "Engineering", "The ability of a material to absorb energy up to the elastic limit is called:", "Resilience", ["Toughness", "Resilience", "Plasticity", "Ductility"]),
    (9, "Engineering", "What is the unit of Young's modulus of elasticity?", "Pascal (Pa)", ["Newton", "Pascal (Pa)", "Joule", "Watt"]),

    # --- Beams, Bending & Shear Forces ---
    (10, "Engineering", "In a simply supported beam carrying a central point load, where does the maximum bending moment occur?", "At the center", ["At the supports", "At the center", "At the quarter points", "At the inflection point"]),
    (10, "Engineering", "What represents the point where the bending moment changes sign (from positive to negative or vice versa)?", "Point of contraflexure", ["Neutral axis", "Point of contraflexure", "Center of gravity", "Shear center"]),
    (11, "Engineering", "What is the bending equation for beams expressed as?", "M/I = sigma/y = E/R", ["M/I = sigma/y = E/R", "F = ma", "PV = nRT", "sigma = P/A"]),
    (11, "Engineering", "What property of a cross-section measures its resistance to bending?", "Moment of inertia", ["Cross-sectional area", "Moment of inertia", "Radius of gyration", "Section modulus"]),
    (10, "Engineering", "What is the shear force at the free end of a cantilever beam carrying a point load at the free end?", "Equal to the load", ["Zero", "Equal to the load", "Half the load", "Double the load"]),

    # --- Trusses, Determinacy & Structures ---
    (12, "Engineering", "For a plane pin-jointed truss, what is the condition for a perfect and statically determinate structure?", "m = 2j - 3", ["m = j - 3", "m = 2j - 3", "m = 3j - 6", "m = j + 2"]),
    (12, "Engineering", "Which structural member is designed primarily to carry axial compressive loads?", "Column / Strut", ["Beam", "Tie", "Column / Strut", "Shaft"]),
    (12, "Engineering", "What is the critical load for a long column hinged at both ends given by Euler's formula?", "pi^2 EI / L^2", ["pi^2 EI / L^2", "4 pi^2 EI / L^2", "pi^2 EI / 4L^2", "EI / L^2"]),
    
    # --- Fluid Mechanics & Dynamics Basics ---
    (11, "Engineering", "What principle states that an increase in fluid speed occurs simultaneously with a decrease in static pressure?", "Bernoulli's principle", ["Pascal's law", "Archimedes' principle", "Bernoulli's principle", "Newton's law of viscosity"]),
    (12, "Engineering", "What dimensionless number represents the ratio of inertial forces to viscous forces in fluid flow?", "Reynolds number", ["Froude number", "Mach number", "Reynolds number", "Nusselt number"]),
]