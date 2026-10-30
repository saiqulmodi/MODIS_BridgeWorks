"""Chemistry high-yield: Class 11/12 NCERT numericals and structure tables, at JEE (NIT/IIT), BE and Expert level."""
import math

from . import facts, fmt, near, template, unit

S = "chemistry"
C11 = (11, 15, 13, 14, 16)
C12 = (12, 15, 13, 14, 16)
N = 60

MOLAR = {"H2O": 18, "CO2": 44, "NaCl": 58.5, "NaOH": 40, "HCl": 36.5, "H2SO4": 98, "CaCO3": 100, "NH3": 17,
         "CH4": 16, "C6H12O6": 180, "O2": 32, "N2": 28, "KMnO4": 158, "C2H5OH": 46, "Na2CO3": 106, "MgO": 40,
         "Fe2O3": 160, "Al2O3": 102, "HNO3": 63, "CH3COOH": 60}


@template(C11, S, N)
def mole_concept(rng, level):
    f, M = rng.choice(list(MOLAR.items()))
    kind = rng.randrange(3)
    if kind == 0:
        n = rng.choice([0.1, 0.2, 0.25, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
        m = n * M
        return (f"How many moles are there in {fmt(m)} g of {f}? (M = {M} g/mol)", fmt(n),
                [fmt(m * M), fmt(M / m), fmt(n * 2), fmt(n / 2)], f"n = mass / M = {fmt(m)} / {M} = {fmt(n)} mol.")
    if kind == 1:
        n = rng.choice([0.1, 0.2, 0.5, 1, 2, 3])
        N_ = n * 6.022e23
        return (f"How many molecules are in {fmt(n * M)} g of {f}? (M = {M} g/mol, NA = 6.022 x 10²³)", f"{N_:.3e}".replace("e+", " x 10^"),
                [f"{N_ * 2:.3e}".replace("e+", " x 10^"), f"{N_ / 10:.3e}".replace("e+", " x 10^"), f"{6.022e23 * M:.3e}".replace("e+", " x 10^"),
                 f"{N_ * 3:.3e}".replace("e+", " x 10^")], f"N = (m/M) x NA = {fmt(n)} x 6.022e23.")
    n = rng.choice([0.25, 0.5, 1, 2, 4])
    return (f"What volume does {fmt(n * M)} g of {f} gas occupy at STP? (M = {M}, molar volume 22.4 L)" if f in
            ("CO2", "NH3", "CH4", "O2", "N2", "HCl") else f"What volume would {fmt(n)} mol of an ideal gas occupy at STP?",
            unit(n * 22.4, "L"), [unit(n * 24.8, "L"), unit(22.4 / n, "L"), unit(n * 11.2, "L"), unit(n * 44.8, "L")],
            f"V = n x 22.4 L = {fmt(n * 22.4)} L.")


@template(C11, S, N)
def percent_composition(rng, level):
    comp = {"H2O": ("H", 2, 18), "CO2": ("C", 12, 44), "NH3": ("N", 14, 17), "CH4": ("C", 12, 16), "CaCO3": ("Ca", 40, 100),
            "NaCl": ("Na", 23, 58.5), "Fe2O3": ("Fe", 112, 160), "H2SO4": ("S", 32, 98), "C6H12O6": ("C", 72, 180),
            "MgO": ("Mg", 24, 40), "Al2O3": ("Al", 54, 102), "HNO3": ("N", 14, 63)}
    f, (el, m, M) = rng.choice(list(comp.items()))
    p = m / M * 100
    return (f"What is the mass percentage of {el} in {f}?", f"{fmt(p)}%",
            [f"{fmt(100 - p)}%", f"{fmt(p / 2)}%", f"{fmt(min(99, p * 1.5))}%", f"{fmt(M / m)}%"], f"%{el} = {m} / {M} x 100 = {fmt(p)}%.")


@template(C11, S, N)
def solutions_conc(rng, level):
    kind = rng.randrange(3)
    f, M = rng.choice([("NaOH", 40), ("NaCl", 58.5), ("HCl", 36.5), ("H2SO4", 98), ("C6H12O6", 180), ("KMnO4", 158)])
    if kind == 0:
        n = rng.choice([0.1, 0.2, 0.25, 0.5, 1])
        V = rng.choice([100, 200, 250, 500, 1000])
        Mo = n / (V / 1000)
        return (f"{fmt(n * M)} g of {f} (M = {M}) is dissolved to make {V} mL of solution. What is the molarity?", unit(Mo, "M"),
                [unit(n / V, "M"), unit(Mo * 2, "M"), unit(Mo / 2, "M"), unit(n * M / V, "M")], f"Molarity = moles / litres = {fmt(n)} / {V / 1000:g} = {fmt(Mo)} M.")
    if kind == 1:
        M1, V1 = rng.choice([0.5, 1, 2, 5, 10, 12]), rng.choice([10, 20, 25, 50, 100])
        V2 = rng.choice([100, 250, 500, 1000])
        M2 = M1 * V1 / V2
        return (f"{V1} mL of {M1} M {f} is diluted to {V2} mL. What is the new molarity?", unit(M2, "M"),
                [unit(M1 * V2 / V1, "M"), unit(M1 - M2, "M"), unit(M2 * 10, "M"), unit(M2 / 2, "M")], f"M1V1 = M2V2  ->  M2 = {M1} x {V1} / {V2} = {fmt(M2)} M.")
    n, kg = rng.choice([0.1, 0.2, 0.5, 1, 2]), rng.choice([0.1, 0.2, 0.25, 0.5, 1])
    m = n / kg
    return (f"{fmt(n * M)} g of {f} (M = {M}) dissolves in {fmt(kg * 1000)} g of water. What is the molality?", unit(m, "mol/kg"),
            [unit(n * kg, "mol/kg"), unit(m / 1000, "mol/kg"), unit(m * 2, "mol/kg"), unit(n * M / kg, "mol/kg")],
            f"Molality = moles of solute / kg of solvent = {fmt(n)} / {kg} = {fmt(m)} mol/kg.")


@template(C11, S, N)
def gas_laws(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        P1, V1, P2 = rng.choice([1, 2, 3, 4]), rng.choice([2, 5, 10, 12, 20]), rng.choice([1, 2, 5, 6, 8])
        if P2 == P1:
            P2 += 1
        V2 = P1 * V1 / P2
        return (f"A gas occupies {V1} L at {P1} atm. At constant temperature, what is its volume at {P2} atm?", unit(V2, "L"),
                [unit(P2 * V1 / P1, "L"), unit(V1, "L"), unit(V2 * 2, "L"), unit(P1 * P2 / V1, "L")], f"Boyle: P1V1 = P2V2  ->  V2 = {fmt(V2)} L.")
    if kind == 1:
        V1, T1, T2 = rng.choice([1, 2, 3, 5, 10]), rng.choice([273, 300, 250, 400]), rng.choice([300, 350, 546, 600, 450])
        V2 = V1 * T2 / T1
        return (f"A gas has volume {V1} L at {T1} K. At constant pressure, what is its volume at {T2} K?", unit(V2, "L"),
                [unit(V1 * T1 / T2, "L"), unit(V1 * (T2 - T1) / 100, "L"), unit(V2 * 2, "L"), unit(V1, "L")], f"Charles: V/T is constant -> V2 = {fmt(V2)} L.")
    M1, M2 = rng.sample([2, 4, 16, 17, 28, 32, 44, 64], 2)
    r = math.sqrt(M2 / M1)
    return (f"How many times faster does a gas of molar mass {M1} effuse than one of molar mass {M2}?", fmt(r),
            [fmt(M2 / M1), fmt(1 / r), fmt(r * r * r), fmt(r * 2)], f"Graham's law: r1/r2 = √(M2/M1) = √({M2}/{M1}) = {fmt(r)}.")


@template(C11, S, N)
def ph_values(rng, level):
    kind = rng.randrange(3 if level != 11 else 2)
    if kind == 0:
        e = rng.randrange(1, 6)
        c = rng.choice([1, 2, 5])
        conc = c * 10 ** -e
        pH = -math.log10(conc)
        return (f"What is the pH of {c} x 10⁻{e} M HCl (a strong acid)?", fmt(pH),
                [fmt(14 - pH), fmt(e + 1), fmt(pH / 2), fmt(-math.log(conc))], f"pH = -log[H⁺] = -log({conc:g}) = {fmt(pH)}.")
    if kind == 1:
        e = rng.randrange(1, 6)
        pH = 14 - e
        return (f"What is the pH of 10⁻{e} M NaOH (a strong base) at 25 °C?", str(pH),
                [str(e), str(pH - 1), str(pH + 1) if pH < 14 else "15", str(7 + e // 2)], f"pOH = {e}; pH = 14 - pOH = {pH}.")
    pKa, c = rng.choice([3.75, 4.2, 4.74, 4.76, 5.0, 9.25]), rng.choice([0.01, 0.1, 0.001, 1])
    pH = 0.5 * (pKa - math.log10(c))
    return (f"What is the pH of {c} M of a weak acid with pKa = {pKa}?", fmt(pH),
            [fmt(pKa - math.log10(c)), fmt(pKa), fmt(0.5 * pKa), fmt(14 - pH)], f"pH = ½(pKa - log C) = ½({pKa} - log {c}) = {fmt(pH)}.")


@template(C12, S, N)
def kinetics(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        k = rng.choice([0.001, 0.002, 0.005, 0.01, 0.0231, 0.0693, 0.1])
        t = 0.693 / k
        return (f"A first-order reaction has k = {k} s⁻¹. What is its half-life?", unit(t, "s"),
                [unit(1 / k, "s"), unit(k / 0.693, "s"), unit(2.303 / k, "s"), unit(t * 2, "s")], f"t½ = 0.693/k = {fmt(t)} s.")
    if kind == 1:
        n = rng.randrange(1, 6)
        pct = 100 / 2 ** n
        return (f"After {n} half-lives of a first-order reaction, what percentage of the reactant remains?", f"{fmt(pct)}%",
                [f"{fmt(100 - pct)}%", f"{fmt(100 / (2 * n))}%", f"{fmt(pct / 2)}%", f"{fmt(pct * 2)}%" if n > 1 else "75%"], f"(½)^{n} x 100 = {fmt(pct)}%.")
    r = rng.choice([2, 3, 4])
    order = rng.randrange(1, 3)
    return (f"For a reaction of order {order} in A, the concentration of A is multiplied by {r}. By what factor does the rate change?",
            str(r ** order), [str(r), str(r ** (order + 1)), str(r * order + 1), str(2 * r) if 2 * r != r ** order else str(r + 1)],
            f"Rate = k[A]^{order}, so the rate changes by {r}^{order} = {r ** order}.")


@template(C12, S, N)
def electrochem(rng, level):
    kind = rng.randrange(3)
    couples = {"Zn": -0.76, "Fe": -0.44, "Cu": 0.34, "Ag": 0.80, "Mg": -2.37, "Ni": -0.25, "Pb": -0.13, "Al": -1.66}
    if kind == 0:
        a, c = rng.sample(list(couples), 2)
        if couples[a] > couples[c]:
            a, c = c, a
        E = couples[c] - couples[a]
        return (f"Find E°cell for a cell with {a} as anode and {c} as cathode. (E°: {a} = {couples[a]} V, {c} = {couples[c]} V)",
                unit(E, "V"), [unit(couples[a] + couples[c], "V"), unit(-E, "V"), unit(E / 2, "V"), unit(abs(couples[a]), "V")],
                f"E°cell = E°cathode - E°anode = {couples[c]} - ({couples[a]}) = {fmt(E)} V.")
    if kind == 1:
        n, E = rng.choice([1, 2, 3]), rng.choice([0.34, 0.46, 1.1, 1.56, 2.0, 0.78])
        dG = -n * 96500 * E / 1000
        return (f"A cell reaction transfers {n} mol electrons with E°cell = {E} V. What is ΔG°? (F = 96,500 C/mol)", unit(dG, "kJ/mol"),
                [unit(-dG, "kJ/mol"), unit(dG / n, "kJ/mol"), unit(dG * 1000, "kJ/mol"), unit(-96.5 * E, "kJ/mol") if n != 1 else unit(dG * 2, "kJ/mol")],
                f"ΔG° = -nFE° = -{n} x 96500 x {E} = {fmt(dG)} kJ/mol.")
    metal, M, z = rng.choice([("Cu", 63.5, 2), ("Ag", 108, 1), ("Zn", 65.4, 2), ("Al", 27, 3), ("Ni", 58.7, 2)])
    I, t = rng.choice([1, 2, 2.5, 5, 10]), rng.choice([965, 1930, 3600, 9650])
    m = I * t * M / (z * 96500)
    return (f"A current of {I} A flows for {t} s through a {metal} salt solution ({metal}^{z}+, M = {M}). What mass of {metal} is deposited?",
            unit(m, "g"), [unit(I * t * M / 96500, "g") if z != 1 else unit(m * 2, "g"), unit(m * z * z, "g") if z != 1 else unit(m / 2, "g"),
                          unit(I * t / 96500, "g"), unit(m * 10, "g")], f"m = I t M / (z F) = {fmt(m)} g (Faraday's first law).")


@template(C12, S, N)
def colligative(rng, level):
    kind = rng.randrange(2)
    i = rng.choice([1, 2, 3]) if level != 12 or rng.random() < 0.5 else 1
    m = rng.choice([0.1, 0.2, 0.25, 0.5, 1])
    solute = {1: "glucose", 2: "NaCl", 3: "CaCl2"}[i]
    if kind == 0:
        Kf = 1.86
        dT = i * Kf * m
        return (f"What is the depression in freezing point of a {m} molal aqueous {solute} solution? (Kf = 1.86 K kg/mol, full dissociation)",
                unit(dT, "K"), [unit(Kf * m, "K") if i != 1 else unit(dT * 2, "K"), unit(dT / 2, "K"), unit(0.52 * i * m, "K"), unit(Kf * m * (i + 1), "K")],
                f"ΔTf = i Kf m = {i} x 1.86 x {m} = {fmt(dT)} K (van 't Hoff factor i = {i}).")
    Kb = 0.52
    dT = i * Kb * m
    return (f"What is the elevation in boiling point of a {m} molal aqueous {solute} solution? (Kb = 0.52 K kg/mol, full dissociation)",
            unit(dT, "K"), [unit(Kb * m, "K") if i != 1 else unit(dT * 2, "K"), unit(dT / 2, "K"), unit(1.86 * i * m, "K"), unit(Kb * m * (i + 1), "K")],
            f"ΔTb = i Kb m = {fmt(dT)} K.")


@template(C11, S, N)
def thermo_chem(rng, level):
    kind = rng.randrange(2)
    if kind == 0:
        dH, dS = rng.choice([-120, -90, -40, 30, 60, 178]), rng.choice([-200, -100, 50, 120, 160])
        T = rng.choice([200, 298, 500, 1000, 1200])
        dG = dH - T * dS / 1000
        sp = "spontaneous" if dG < 0 else "non-spontaneous"
        return (f"For a reaction ΔH = {dH} kJ/mol and ΔS = {dS} J/(mol K). At {T} K, ΔG is about:",
                f"{fmt(dG)} kJ/mol ({sp})", [f"{fmt(dH - T * dS)} kJ/mol", f"{fmt(-dG)} kJ/mol ({'non-spontaneous' if dG < 0 else 'spontaneous'})",
                                            f"{fmt(dH + T * dS / 1000)} kJ/mol", f"{fmt(dH)} kJ/mol"],
                f"ΔG = ΔH - TΔS = {dH} - {T} x {dS}/1000 = {fmt(dG)} kJ/mol; ΔG < 0 means spontaneous.")
    a, b = rng.choice([-394, -286, -242, -75, -110]), rng.choice([-283, -890, 52, -46, 90])
    return (f"Reaction 1 has ΔH = {a} kJ and reaction 2 has ΔH = {b} kJ. By Hess's law, what is ΔH for reaction 1 + reaction 2?",
            unit(a + b, "kJ"), [unit(a - b, "kJ"), unit(b - a, "kJ"), unit((a + b) / 2, "kJ"), unit(-(a + b), "kJ")],
            f"Enthalpy changes add: {a} + ({b}) = {a + b} kJ.")


HYB = {"CH4": ("sp³", "tetrahedral"), "NH3": ("sp³", "trigonal pyramidal"), "H2O": ("sp³", "bent"), "BF3": ("sp²", "trigonal planar"),
       "CO2": ("sp", "linear"), "C2H2": ("sp", "linear"), "C2H4": ("sp²", "trigonal planar"), "PCl5": ("sp³d", "trigonal bipyramidal"),
       "SF6": ("sp³d²", "octahedral"), "XeF4": ("sp³d²", "square planar"), "XeF2": ("sp³d", "linear"), "SF4": ("sp³d", "see-saw"),
       "ClF3": ("sp³d", "T-shaped"), "BeCl2": ("sp", "linear"), "SO3": ("sp²", "trigonal planar"), "NH4+": ("sp³", "tetrahedral"),
       "IF5": ("sp³d²", "square pyramidal"), "SO2": ("sp²", "bent"), "CCl4": ("sp³", "tetrahedral"), "IF7": ("sp³d³", "pentagonal bipyramidal")}


@template(C11, S, 25)
def hybridisation(rng, level):
    f, (h, shape) = rng.choice(list(HYB.items()))
    hs = sorted({v[0] for v in HYB.values()})
    shapes = sorted({v[1] for v in HYB.values()})
    if rng.random() < 0.5:
        return (f"What is the hybridisation of the central atom in {f}?", h, [x for x in hs if x != h],
                f"Count bond pairs + lone pairs on the central atom: {f} is {h} ({shape}).")
    return (f"What is the shape of {f}?", shape, [x for x in shapes if x != shape],
            f"VSEPR: {f} is {h}; lone pairs change the shape to {shape}.")


OXI = {"KMnO4": ("Mn", 7), "K2Cr2O7": ("Cr", 6), "H2SO4": ("S", 6), "HNO3": ("N", 5), "NH3": ("N", -3), "H2O2": ("O", -1),
       "Fe3O4": ("Fe", "8/3"), "Na2S2O3": ("S", 2), "CrO5": ("Cr", 6), "HClO4": ("Cl", 7), "SO2": ("S", 4), "NO2": ("N", 4),
       "K4[Fe(CN)6]": ("Fe", 2), "Ni(CO)4": ("Ni", 0), "OF2": ("O", 2), "N2O": ("N", 1), "H3PO4": ("P", 5), "NaH": ("H", -1)}


@template(C11, S, 25)
def oxidation_state(rng, level):
    f, (el, n) = rng.choice(list(OXI.items()))
    ans = n if isinstance(n, str) else (f"+{n}" if n > 0 else str(n))
    pool = ["+1", "+2", "+3", "+4", "+5", "+6", "+7", "-1", "-2", "-3", "0", "8/3"]
    rng.shuffle(pool)
    return (f"What is the oxidation state of {el} in {f}?", ans, [p for p in pool if p != ans],
            f"Sum of oxidation states = charge on the species; this gives {el} = {ans} in {f}.")


BO = {"H2": 1, "He2+": 0.5, "N2": 3, "O2": 2, "O2-": 1.5, "O2 2-": 1, "O2+": 2.5, "F2": 1, "C2": 2, "B2": 1, "NO": 2.5, "CO": 3, "Li2": 1, "N2+": 2.5}


@template(C11, S, 20)
def bond_order(rng, level):
    f, b = rng.choice(list(BO.items()))
    pool = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
    rng.shuffle(pool)
    return (f"By molecular orbital theory, what is the bond order of {f}?", fmt(b), [p for p in pool if p != fmt(b)],
            f"Bond order = (bonding - antibonding electrons)/2 = {fmt(b)} for {f}.")


@template(C11, S, 20)
def atomic_counts(rng, level):
    atoms = [("Na", 11, 23), ("Cl", 17, 35), ("Fe", 26, 56), ("Ca", 20, 40), ("U", 92, 238), ("C", 6, 14), ("K", 19, 39),
             ("Zn", 30, 65), ("Br", 35, 80), ("Ag", 47, 108), ("Al", 13, 27), ("P", 15, 31)]
    el, Z, A = rng.choice(atoms)
    q = rng.choice([0, 1, 2, -1])
    ion = el + ("" if q == 0 else (f"{q}+" if q > 0 else f"{-q}-"))
    if rng.random() < 0.5:
        return (f"How many neutrons are in {el}-{A} (Z = {Z})?", str(A - Z), [str(Z), str(A), str(A + Z), str(A - Z + 1)], f"Neutrons = A - Z = {A} - {Z} = {A - Z}.")
    e = Z - q
    return (f"How many electrons are in {ion} (Z = {Z})?", str(e), [str(Z + q) if q else str(Z + 1), str(Z - 2 * q) if q else str(Z - 1), str(A - Z), str(A)],
            f"Electrons = Z - charge = {Z} - ({q}) = {e}.")


facts((11, 12, 15, 13, 14, 16), S, [
    ("Which element has the highest electronegativity?", "Fluorine", ["Oxygen", "Chlorine", "Nitrogen"], "F = 4.0 on the Pauling scale."),
    ("Ionisation enthalpy generally ___ across a period.", "Increases", ["Decreases", "Stays the same", "Becomes zero"],
     "Nuclear charge rises while the shell stays the same."),
    ("Which quantum number describes the shape of an orbital?", "Azimuthal (l)", ["Principal (n)", "Magnetic (m)", "Spin (s)"],
     "l = 0, 1, 2, 3 for s, p, d, f."),
    ("The maximum number of electrons in a shell with n = 3 is:", "18", ["8", "32", "9"], "2n² = 18."),
    ("Aldol condensation needs a carbonyl compound with:", "An α-hydrogen", ["No α-hydrogen", "A benzene ring", "A halogen"],
     "The α-hydrogen is removed to form the enolate."),
    ("Cannizzaro reaction is given by aldehydes that have:", "No α-hydrogen", ["An α-hydrogen", "A nitro group", "A ketone group"],
     "e.g. HCHO and C6H5CHO disproportionate in strong base."),
    ("SN1 reactions go fastest with:", "Tertiary alkyl halides", ["Primary alkyl halides", "Methyl halides", "Vinyl halides"],
     "A stable tertiary carbocation forms."),
    ("SN2 reactions give:", "Inversion of configuration", ["Retention", "Racemisation", "No change"],
     "Backside attack (Walden inversion)."),
    ("Markovnikov's rule: in adding HBr to propene, Br goes to:", "The carbon with fewer hydrogens", ["The carbon with more hydrogens",
     "Both carbons equally", "Neither carbon"], "The more stable carbocation forms. With peroxide, the anti-Markovnikov product forms."),
    ("Which is the strongest acid?", "CF3COOH", ["CH3COOH", "HCOOH", "C2H5COOH"], "Three F atoms pull electron density and stabilise the anion."),
    ("Lucas test distinguishes:", "Primary, secondary and tertiary alcohols", ["Aldehydes and ketones", "Acids and bases",
     "Alkenes and alkynes"], "Tertiary alcohols turn cloudy at once with ZnCl2/HCl."),
    ("Tollens' reagent gives a silver mirror with:", "Aldehydes", ["Ketones", "Alcohols", "Ethers"], "Aldehydes reduce Ag⁺ to Ag."),
    ("The coordination number of Fe in [Fe(CN)6]4- is:", "6", ["4", "2", "3"], "Six CN⁻ ligands surround Fe."),
    ("Which has the highest boiling point?", "H2O", ["H2S", "H2Se", "H2Te"], "Strong hydrogen bonding in water."),
    ("Lanthanoid contraction makes Zr and Hf:", "Almost the same size", ["Very different in size", "Non-metals", "Radioactive"],
     "Poor shielding by 4f electrons."),
    ("Which gas causes the greenhouse effect most among these?", "CO2", ["N2", "O2", "Ar"], "CO2 absorbs infrared radiation."),
    ("Haber process makes ammonia using an iron catalyst at about:", "200 atm and 700 K", ["1 atm and 300 K", "1000 atm and 2000 K",
     "10 atm and 100 K"], "A compromise between yield and rate."),
    ("Which polymer is made by condensation?", "Nylon-6,6", ["Polythene", "PVC", "Teflon"], "Hexamethylenediamine + adipic acid lose water."),
    ("Glucose and fructose are:", "Functional isomers (C6H12O6)", ["Identical", "Polymers", "Enantiomers of each other"],
     "Glucose is an aldose; fructose is a ketose."),
    ("DNA contains the sugar:", "2-deoxyribose", ["Ribose", "Glucose", "Fructose"], "RNA contains ribose."),
])


@template(C12, S, N)
def solid_state(rng, level):
    lattice, Z = rng.choice([("simple cubic", 1), ("body-centred cubic", 2), ("face-centred cubic", 4)])
    if rng.random() < 0.4:
        return (f"How many atoms belong to one unit cell of a {lattice} lattice?", str(Z), [str(z) for z in (1, 2, 4, 6, 8) if z != Z],
                "Corners count 1/8, face centres 1/2, body centre 1: sc = 1, bcc = 2, fcc = 4.")
    M, a = rng.choice([27, 56, 63.5, 108, 23, 39, 197]), rng.choice([286, 300, 350, 361, 405, 408, 430, 500])
    d = Z * M / ((a * 1e-10) ** 3 * 6.022e23)
    return (f"A metal (M = {M} g/mol) forms a {lattice} lattice with edge {a} pm. What is its density?", unit(d, "g/cm³"),
            [unit(M / ((a * 1e-10) ** 3 * 6.022e23), "g/cm³") if Z != 1 else unit(d * 2, "g/cm³"), unit(d * 4, "g/cm³") if Z != 4 else unit(d / 2, "g/cm³"),
             unit(d / 10, "g/cm³"), unit(d * 1.5, "g/cm³")], f"ρ = Z M / (a³ NA) with Z = {Z}: {fmt(d)} g/cm³.")


IONS = {"Ti3+": 1, "V3+": 2, "Cr3+": 3, "Mn2+": 5, "Fe2+": 4, "Fe3+": 5, "Co2+": 3, "Ni2+": 2, "Cu2+": 1, "Zn2+": 0, "Sc3+": 0, "Mn3+": 4, "Co3+": 4}


@template(C12, S, 30)
def magnetic_moment(rng, level):
    ion, n = rng.choice(list(IONS.items()))
    mu = (n * (n + 2)) ** 0.5
    if rng.random() < 0.5:
        return (f"How many unpaired electrons does a free {ion} ion have?", str(n), [str(k) for k in range(6) if k != n],
                f"Write the 3d configuration of {ion} and fill singly first (Hund's rule): {n} unpaired.")
    return (f"What is the spin-only magnetic moment of a free {ion} ion?", f"{fmt(mu)} BM",
            [f"{fmt(((n + 1) * (n + 3)) ** 0.5)} BM", f"{fmt(((max(n - 1, 0)) * (n + 1)) ** 0.5)} BM", f"{n} BM", f"{fmt(mu * 2)} BM"],
            f"μ = √(n(n+2)) with n = {n} unpaired electrons = {fmt(mu)} BM.")
