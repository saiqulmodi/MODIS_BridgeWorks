"""Engineering core (BE and Expert): mechanics of materials, structures, fluids, thermal, electrical, civil."""
import math

from . import facts, fmt, template, unit

S = "engineering"
BE = (15, 16)
N = 60


@template(BE, S, N)
def stress_strain(rng, level):
    kind = rng.randrange(3)
    P = rng.randrange(10, 500, 10)            # kN
    A = rng.choice([100, 200, 250, 400, 500, 1000, 2000])   # mm²
    if kind == 0:
        s = P * 1000 / A
        return (f"An axial load of {P} kN acts on a bar of cross-section {A} mm². What is the normal stress?", unit(s, "MPa"),
                [unit(P / A, "MPa"), unit(s * 2, "MPa"), unit(s / 2, "MPa"), unit(P * A / 1000, "MPa")], f"σ = P/A = {P}e3 N / {A} mm² = {fmt(s)} MPa.")
    if kind == 1:
        L, E = rng.choice([1, 2, 3, 4, 5]), rng.choice([200, 70, 100, 210])
        d = P * 1000 * L * 1000 / (A * E * 1000)
        return (f"A {L} m bar of area {A} mm² and E = {E} GPa carries {P} kN. What is its elongation?", unit(d, "mm"),
                [unit(d * 10, "mm"), unit(d / 10, "mm"), unit(d * 2, "mm"), unit(P * L / (A * E), "mm")], f"δ = PL/(AE) = {fmt(d)} mm.")
    E, nu = rng.choice([200, 210, 70, 100]), rng.choice([0.25, 0.3, 0.33])
    G = E / (2 * (1 + nu))
    return (f"For a material with E = {E} GPa and Poisson's ratio {nu}, what is the shear modulus G?", unit(G, "GPa"),
            [unit(E / (3 * (1 - 2 * nu)), "GPa"), unit(E / 2, "GPa"), unit(E * (1 + nu), "GPa"), unit(E / (1 + nu), "GPa")],
            f"G = E / (2(1 + ν)) = {fmt(G)} GPa.")


@template(BE, S, N)
def beams(rng, level):
    L = rng.choice([2, 3, 4, 5, 6, 8, 10])
    kind = rng.randrange(4)
    if kind == 0:
        w = rng.randrange(2, 40)
        M = w * L * L / 8
        return (f"A simply supported beam of span {L} m carries a uniform load of {w} kN/m. What is the maximum bending moment?",
                unit(M, "kN m"), [unit(w * L * L / 2, "kN m"), unit(w * L * L / 12, "kN m"), unit(w * L / 4, "kN m"), unit(w * L * L / 4, "kN m")],
                f"M_max = wL²/8 = {w} x {L}² / 8 = {fmt(M)} kN m (at mid-span).")
    if kind == 1:
        P = rng.randrange(5, 200, 5)
        M = P * L / 4
        return (f"A simply supported beam of span {L} m carries a point load of {P} kN at mid-span. What is the maximum bending moment?",
                unit(M, "kN m"), [unit(P * L / 8, "kN m"), unit(P * L / 2, "kN m"), unit(P * L, "kN m"), unit(P * L * L / 8, "kN m")],
                f"M_max = PL/4 = {fmt(M)} kN m.")
    if kind == 2:
        P = rng.randrange(5, 100, 5)
        return (f"A cantilever of length {L} m carries {P} kN at its free end. What is the bending moment at the fixed end?", unit(P * L, "kN m"),
                [unit(P * L / 2, "kN m"), unit(P * L / 4, "kN m"), unit(P * L * L / 2, "kN m"), unit(P / L, "kN m")], f"M = P x L = {fmt(P * L)} kN m.")
    b, d = rng.choice([100, 150, 200, 230, 300]), rng.choice([200, 300, 400, 450, 500, 600])
    M = rng.randrange(10, 200, 5)
    Z = b * d * d / 6
    s = M * 1e6 / Z
    return (f"A rectangular beam {b} mm wide and {d} mm deep resists a moment of {M} kN m. What is the maximum bending stress?",
            unit(s, "MPa"), [unit(M * 1e6 / (b * d * d / 12), "MPa"), unit(M * 1e6 / (b * d), "MPa"), unit(s * 2, "MPa"), unit(M * 1e6 / (b * b * d / 6), "MPa")],
            f"σ = M/Z with Z = bd²/6 = {fmt(Z)} mm³: σ = {fmt(s)} MPa.")


@template(BE, S, N)
def deflection_buckling(rng, level):
    kind = rng.randrange(2)
    E = rng.choice([200e3, 210e3, 70e3])      # MPa = N/mm²
    I = rng.choice([1e6, 5e6, 1e7, 5e7, 1e8])  # mm⁴
    L = rng.choice([2000, 3000, 4000, 5000, 6000])  # mm
    if kind == 0:
        P = rng.choice([5e3, 10e3, 20e3, 50e3])
        d = P * L ** 3 / (48 * E * I)
        return (f"A simply supported beam (L = {L / 1000:g} m, E = {E / 1000:g} GPa, I = {I:g} mm⁴) carries {P / 1000:g} kN at mid-span. "
                f"What is the mid-span deflection?", unit(d, "mm"),
                [unit(P * L ** 3 / (3 * E * I), "mm"), unit(5 * P * L ** 3 / (384 * E * I), "mm"), unit(d * 2, "mm"), unit(P * L ** 2 / (48 * E * I), "mm")],
                f"δ = PL³/(48EI) = {fmt(d)} mm.")
    K = rng.choice([(1.0, "pinned at both ends"), (0.5, "fixed at both ends"), (2.0, "fixed at one end, free at the other"), (0.7, "fixed at one end, pinned at the other")])
    Pcr = math.pi ** 2 * E * I / (K[0] * L) ** 2
    return (f"A column {L / 1000:g} m long ({K[1]}) has E = {E / 1000:g} GPa and I = {I:g} mm⁴. What is its Euler buckling load?",
            unit(Pcr / 1000, "kN", 4), [unit(math.pi ** 2 * E * I / L ** 2 / 1000, "kN", 4) if K[0] != 1 else unit(Pcr / 4000, "kN", 4),
                                        unit(Pcr / 2000, "kN", 4), unit(Pcr / 250, "kN", 4), unit(math.pi * E * I / (K[0] * L) ** 2 / 1000, "kN", 4)],
            f"P_cr = π²EI/(KL)² with K = {K[0]}: {fmt(Pcr / 1000, 4)} kN.")


@template(BE, S, N)
def fluids(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        v, D = rng.choice([0.5, 1, 1.5, 2, 3]), rng.choice([0.01, 0.02, 0.05, 0.1, 0.2])
        nu = rng.choice([1e-6, 1.5e-6, 1e-5])
        Re = v * D / nu
        regime = "laminar" if Re < 2000 else "turbulent" if Re > 4000 else "transitional"
        return (f"Water-like fluid (ν = {nu:g} m²/s) flows at {v} m/s in a {D * 1000:g} mm pipe. What is the Reynolds number and flow type?",
                f"{fmt(Re)} ({regime})", [f"{fmt(Re / 10)} ({'laminar' if Re / 10 < 2000 else 'turbulent'})", f"{fmt(Re * 10)} (turbulent)",
                                           f"{fmt(Re)} ({'turbulent' if regime != 'turbulent' else 'laminar'})", f"{fmt(v * D)} (laminar)"],
                f"Re = vD/ν = {fmt(Re)}: below 2000 laminar, above 4000 turbulent.")
    if kind == 1:
        D, v = rng.choice([0.1, 0.2, 0.3, 0.5]), rng.choice([0.5, 1, 1.5, 2, 2.5])
        Q = math.pi * D * D / 4 * v
        return (f"Water flows at {v} m/s in a pipe of diameter {D} m. What is the discharge?", unit(Q * 1000, "L/s"),
                [unit(math.pi * D * D * v * 1000, "L/s"), unit(Q * 100, "L/s"), unit(math.pi * D * v * 1000, "L/s"), unit(Q * 2000, "L/s")],
                f"Q = (π D²/4) v = {fmt(Q, 4)} m³/s = {fmt(Q * 1000)} L/s.")
    h = rng.randrange(1, 30)
    v = math.sqrt(2 * 9.81 * h)
    return (f"Water discharges from an orifice {h} m below the free surface of a large tank. What is the ideal jet speed?", unit(v, "m/s"),
            [unit(9.81 * h, "m/s"), unit(math.sqrt(9.81 * h), "m/s"), unit(2 * 9.81 * h, "m/s"), unit(v / 2, "m/s")], f"Torricelli: v = √(2gh) = {fmt(v)} m/s.")


@template(BE, S, N)
def thermal_eng(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        Tl, Th = rng.choice([253, 263, 268, 273]), rng.choice([303, 308, 313, 318])
        cop = Tl / (Th - Tl)
        return (f"What is the Carnot COP of a refrigerator working between {Tl} K and {Th} K?", fmt(cop),
                [fmt(Th / (Th - Tl)), fmt((Th - Tl) / Th), fmt(cop / 2), fmt(Tl / Th)], f"COP_R = TL/(TH - TL) = {Tl}/{Th - Tl} = {fmt(cop)}.")
    if kind == 1:
        k, A, dT, L = rng.choice([0.04, 0.6, 1.4, 45, 200, 385]), rng.choice([1, 2, 5, 10]), rng.randrange(5, 80), rng.choice([0.01, 0.05, 0.1, 0.2, 0.25])
        q = k * A * dT / L
        return (f"Heat conducts through a wall of k = {k} W/(m K), area {A} m², thickness {L} m, with a {dT} K temperature difference. Heat rate?",
                unit(q, "W"), [unit(k * A * dT * L, "W"), unit(k * dT / L, "W"), unit(q * 2, "W"), unit(A * dT / (k * L), "W")], f"Fourier's law: q = kAΔT/L = {fmt(q)} W.")
    r = rng.choice([6, 8, 9, 10, 12])
    g = 1.4
    eta = 1 - 1 / r ** (g - 1)
    return (f"What is the air-standard Otto cycle efficiency for a compression ratio of {r}? (γ = 1.4)", f"{fmt(eta * 100)}%",
            [f"{fmt((1 - 1 / r) * 100)}%", f"{fmt((1 - 1 / r ** g) * 100)}%", f"{fmt(eta * 80)}%", f"{fmt(min(99, eta * 120))}%"],
            f"η = 1 - 1/r^(γ-1) = 1 - 1/{r}^0.4 = {fmt(eta * 100)}%.")


@template(BE, S, N)
def electrical(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        V, I, pf = rng.choice([400, 415, 440, 11000]), rng.randrange(10, 200, 5), rng.choice([0.8, 0.85, 0.9, 0.95, 1.0])
        P = math.sqrt(3) * V * I * pf / 1000
        return (f"A balanced 3-phase load draws {I} A at {V} V line voltage with power factor {pf}. What real power does it take?",
                unit(P, "kW", 4), [unit(V * I * pf / 1000, "kW", 4), unit(3 * V * I * pf / 1000, "kW", 4), unit(math.sqrt(3) * V * I / 1000, "kW", 4) if pf != 1 else unit(P / 2, "kW", 4),
                                   unit(P / math.sqrt(3), "kW", 4)], f"P = √3 V_L I_L cos φ = {fmt(P, 4)} kW.")
    if kind == 1:
        Vp, Np, Ns = rng.choice([230, 11000, 400, 33000]), rng.choice([500, 1000, 2000, 1500]), rng.choice([50, 100, 200, 250, 4000])
        Vs = Vp * Ns / Np
        return (f"An ideal transformer has {Np} primary and {Ns} secondary turns. With {Vp} V on the primary, what is the secondary voltage?",
                unit(Vs, "V"), [unit(Vp * Np / Ns, "V"), unit(Vp, "V"), unit(Vs * 2, "V"), unit(Vs / 2, "V")], f"Vs/Vp = Ns/Np  ->  Vs = {fmt(Vs)} V.")
    R, X = rng.randrange(3, 40), rng.randrange(3, 40)
    Z = math.hypot(R, X)
    return (f"A series circuit has R = {R} Ω and net reactance X = {X} Ω. What is its power factor?", fmt(R / Z),
            [fmt(X / Z), fmt(R / X) if R < X else fmt(X / R), fmt(R / (R + X)), "1"], f"Z = √(R² + X²) = {fmt(Z)} Ω; pf = R/Z = {fmt(R / Z)}.")


@template(BE, S, 25)
def civil(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        L, B, D = rng.choice([3, 4, 5, 6, 10]), rng.choice([3, 4, 5, 6]), rng.choice([0.1, 0.12, 0.15, 0.2, 0.25])
        V = L * B * D
        return (f"How much concrete is needed for a {L} m x {B} m slab {D * 1000:g} mm thick?", unit(V, "m³"),
                [unit(L * B * D * 10, "m³"), unit(L * B, "m³"), unit(V * 1.54, "m³"), unit(V / 2, "m³")],
                f"V = L x B x D = {fmt(V)} m³ (wet concrete; dry material is about 1.54 x this).")
    if kind == 1:
        rise, run = rng.randrange(1, 30), rng.choice([100, 200, 250, 500, 1000])
        g = rise / run * 100
        return (f"A road rises {rise} m over {run} m horizontally. What is its gradient?", f"{fmt(g)}%",
                [f"{fmt(run / rise)}%", f"{fmt(g * 10)}%", f"{fmt(math.degrees(math.atan(rise / run)))}%", f"{fmt(g / 2)}%"], f"Gradient = rise/run x 100 = {fmt(g)}%.")
    fck = rng.choice([20, 25, 30, 35, 40])
    return (f"For M{fck} concrete, what does {fck} mean?", f"Characteristic cube strength {fck} MPa at 28 days",
            [f"{fck} kg cement per bag", f"{fck}% water", f"{fck} days curing time"], f"M{fck}: characteristic compressive strength of 150 mm cubes at 28 days (IS 456).")


facts(BE, S, [
    ("In a truss, members carry only:", "Axial forces (tension or compression)", ["Bending moments", "Torsion", "Shear only"],
     "Pin joints and loads at joints mean no bending in ideal truss members."),
    ("A structure is statically determinate when:", "Equilibrium equations alone give all forces", ["It has no supports",
     "It is made of steel", "It has more unknowns than equations"], "For a plane truss, m + r = 2j."),
    ("The factor of safety is:", "Failure load / working load", ["Working load / failure load", "Stress x strain", "Yield / Young's modulus"],
     "It gives a margin against uncertainty."),
    ("Shear force diagrams change slope where:", "There is a distributed load", ["There is a point load only", "There is no load",
     "The beam is fixed"], "dV/dx = -w."),
    ("Maximum bending moment occurs where shear force is:", "Zero (changes sign)", ["Maximum", "Equal to the load", "Infinite"],
     "dM/dx = V."),
    ("The neutral axis of a beam has:", "Zero bending stress", ["Maximum bending stress", "Maximum shear only at the top", "Infinite strain"],
     "Stress varies linearly from it: σ = My/I."),
    ("Prestressed concrete applies:", "Compression before service loads act", ["Tension to concrete", "Heat to steel only",
     "No force"], "It cancels the tension that loads would cause."),
    ("Pascal's law says pressure in a fluid at rest is:", "Equal in all directions at a point", ["Highest at the top", "Zero",
     "Only vertical"], "This is how hydraulic jacks work."),
    ("The Bernoulli equation assumes flow that is:", "Steady, incompressible and frictionless along a streamline", ["Turbulent and viscous",
     "Unsteady", "Compressible only"], "Real flows need head-loss terms."),
    ("Second law of thermodynamics: no heat engine can be:", "100% efficient", ["Reversible", "Cyclic", "Used at all"],
     "Kelvin-Planck statement."),
    ("Kirchhoff's voltage law: around any closed loop the sum of voltages is:", "Zero", ["Equal to current", "Maximum", "Infinite"],
     "Energy is conserved."),
    ("An induction motor's rotor runs at a speed slightly ___ synchronous speed.", "Below", ["Above", "Equal to", "Twice"],
     "Slip is needed to induce rotor current."),
    ("The bearing capacity of soil is:", "The load per unit area it can carry safely", ["Its water content", "Its colour",
     "Its density only"], "Foundations are sized from it."),
    ("Slump test measures concrete's:", "Workability", ["Strength", "Density", "Curing time"], "Higher slump = more workable mix."),
    ("Fatigue failure happens under:", "Repeated cyclic loading below the static strength", ["A single huge load", "No load",
     "Constant temperature only"], "S-N curves give the cycles to failure."),
    ("Resonance in a bridge is dangerous because:", "Small periodic forces build up large oscillations", ["It cools the deck",
     "It lowers traffic", "It removes damping"], "Tacoma Narrows (1940) failed by aeroelastic flutter; dampers add energy loss."),
    ("A tuned mass damper reduces vibration by:", "Oscillating out of phase with the structure", ["Adding stiffness only",
     "Heating the structure", "Removing mass"], "It absorbs energy near the structure's natural frequency."),
    ("Moment of inertia of a rectangle about its centroidal axis is:", "bd³/12", ["bd²/6", "bd³/3", "b³d/36"], "I-beams move area away from this axis."),
])
