"""Bridge quiz: questions about each class's own bridge project (subject "bridge").

Project 1 Tension Fibers   - Class 1-7     cables, pulling, sharing a load
Project 2 Coplanar Trusses - Class 8-10    triangles, reactions, stress, buckling
Project 3 Parabolic Thrust - Class 11-12   arch thrust, parabola, hangers
Project 4 Stay Dynamics    - BE, NIT       stay tension, angles, backstays, impact
Project 5 Matrix Dissipation - IIT, Expert stiffness sharing, vibration, resonance
"""
import math

from . import facts, fmt, template, unit

S = "bridge"
T1, T2, T3, T4, T5 = tuple(range(1, 8)), (8, 9, 10), (11, 12), (15, 13), (14, 16)

# ---------------- Project 1: Tension Fibers ----------------
facts(T1, S, [
    ("A cable can only:", "Pull", ["Push", "Push and pull", "Bend like a beam"], "Cables and ropes go slack if you push them; they only pull (tension)."),
    ("What holds the road up in the Tension Fibers bridge?", "Cables hanging from the masts", ["Balloons", "Water", "Nothing"],
     "Each cable pulls the road joint up towards the mast top."),
    ("If one road joint has no cable, the road there will:", "Sag and fall", ["Float", "Get stronger", "Turn into a cable"],
     "Every road joint in the middle needs something holding it up."),
    ("Which is stronger for a bridge cable?", "Steel cable", ["Cotton thread", "Paper string", "Wool"], "Steel can pull very hard without breaking."),
    ("The tall posts on the banks that hold the cables are called:", "Masts (towers)", ["Wheels", "Roads", "Rivers"],
     "Masts give the cables a high point to pull from."),
    ("A pulled cable is in:", "Tension", ["Compression", "Rest", "Water"], "Pulling = tension; pushing = compression."),
    ("A heavier vehicle on the bridge makes the cables pull:", "Harder", ["Less", "Not at all", "Backwards"], "More weight needs more pull."),
    ("Why do we test the bridge with a car?", "To check it holds a real load", ["To paint it", "To make noise", "To wash it"],
     "A test shows if every part is strong enough."),
    ("A cable that is very flat (almost lying down) must pull:", "Much harder", ["Less", "The same", "Not at all"],
     "Only the up-part of its pull holds the road; a flat cable has a small up-part."),
    ("Weight is the pull of:", "Gravity", ["Wind", "Magnets", "Light"], "Earth's gravity pulls every mass down; 1 kg weighs about 10 N."),
    ("In the game, parts are earned by:", "Answering questions right", ["Waiting", "Breaking the bridge", "Closing the game"],
     "Each right answer gives parts to build with."),
    ("Bigger cable sizes (M instead of S) are:", "Stronger but cost more parts", ["Weaker", "Free", "Invisible"],
     "Engineers balance strength against cost."),
    ("A support that holds a joint still in every direction is a:", "Pin", ["Roller", "Cable", "Car"], "A roller lets the joint slide sideways."),
    ("The Howrah Bridge in Kolkata is mainly made of:", "Steel", ["Wood", "Glass", "Paper"], "It opened in 1943 and carries over 1 lakh vehicles a day."),
])


@template(T1, S, 30)
def share_load(rng, level):
    n = rng.choice([2, 2, 4] if level <= 3 else [2, 3, 4, 5])
    each = rng.randrange(2, 6 + level * 3)
    w = each * n
    u = "kg" if level <= 3 else "N"
    return (f"{n} cables share a load of {w} {u} equally. How much does each cable hold?", f"{each} {u}",
            [f"{w} {u}", f"{each + 1} {u}", f"{w * n} {u}", f"{max(1, each - 1)} {u}"], f"{w} ÷ {n} = {each} {u} each.")


@template(T1, S, 30)
def parts_budget(rng, level):
    c = rng.choice([1, 2] if level <= 3 else [1, 2, 3, 4])
    p = rng.randrange(c * 2, c * (6 + level))
    return (f"You have {p} parts. Each cable costs {c} part{'s' if c > 1 else ''}. How many cables can you build?", str(p // c),
            [str(p // c + 1), str(p * c), str(max(0, p // c - 1)), str(p)], f"{p} ÷ {c} = {p // c} (a part left over cannot make a cable).")


@template(range(4, 8), S, 30)
def weight_of(rng, level):
    m = rng.randrange(5, 200) * (10 if level >= 6 else 1)
    return (f"A load has a mass of {m} kg. About how much does it weigh? (1 kg weighs about 10 N)", f"{m * 10} N",
            [f"{m} N", f"{m * 100} N", f"{m // 10 or 1} N", f"{m * 10 + 10} N"], f"Weight = mass x g ≈ {m} x 10 = {m * 10} N.")


@template((6, 7), S, 30)
def two_cables_angle(rng, level):
    W = rng.randrange(2, 40) * 100
    th = rng.choice([30, 90])
    T = W / (2 * math.sin(math.radians(th)))
    return (f"A {W} N sign hangs from two equal cables, each at {th}° to the horizontal. What is the pull in each cable?", unit(T, "N"),
            [unit(W / 2 if th != 90 else W, "N"), unit(W * 2, "N"), unit(W / 4, "N"), unit(T * 2 if th != 90 else W * 1.5, "N")],
            f"Up-parts must add to W: 2 T sin {th}° = {W}, so T = {fmt(T)} N. Flatter cables pull harder.")


# ---------------- Project 2: Coplanar Trusses ----------------
facts(T2, S, [
    ("Why does a truss use triangles?", "A triangle cannot change shape without a side changing length", ["Triangles look nice",
     "Triangles are lighter than any beam", "Squares are not allowed"], "A square can fold flat; a triangle cannot."),
    ("In a truss, the top chord of a simply supported bridge is mostly in:", "Compression", ["Tension", "No force", "Torsion"],
     "The bridge bends downward, squeezing the top and stretching the bottom."),
    ("The bottom chord (the road deck) of a simple truss bridge is mostly in:", "Tension", ["Compression", "No force", "Shear only"],
     "It is stretched as the bridge sags."),
    ("Which member is most likely to buckle?", "A long, thin member being pushed", ["A short member being pulled", "A cable",
     "A member with no force"], "Buckling load P_cr = π²EI/L² falls fast as L grows."),
    ("End posts carry the most force because:", "They bring the whole load down to the supports", ["They are the shortest",
     "They are painted", "They have no angle"], "All the load must reach the supports through them."),
    ("A member with zero force in a truss is called a:", "Zero-force member", ["Mechanism", "Pin", "Roller"],
     "It still helps by bracing other members against buckling."),
    ("If the solver says 'the structure can wobble freely', you should:", "Add diagonals to make triangles", ["Remove members",
     "Use a heavier car", "Delete the supports"], "A mechanism needs more members, not stronger ones."),
    ("Steel is a good truss material because it is:", "Strong in both tension and compression", ["Weak but cheap", "Only strong when pulled",
     "Lighter than air"], "Timber is cheaper and lighter but weaker."),
    ("A Pratt truss has diagonals that are mostly in:", "Tension", ["Compression", "No force", "Torsion"],
     "Long diagonals in tension cannot buckle; the short verticals take compression."),
    ("Stress in a member is:", "Force divided by area", ["Force times length", "Mass times speed", "Area divided by force"],
     "σ = F/A, measured in pascals (N/m²) or MPa."),
])


@template(T2, S, 60)
def diagonal_length(rng, level):
    w, h = rng.choice([3, 4, 5, 6, 8]), rng.choice([3, 4, 5, 6])
    d = math.hypot(w, h)
    return (f"A truss panel is {w} m wide and {h} m tall. How long is its diagonal?", unit(d, "m"),
            [unit(w + h, "m"), unit(d * 1.2, "m"), unit(abs(w - h) or 1, "m"), unit(w * h / 2, "m")],
            f"Pythagoras: √({w}² + {h}²) = {fmt(d)} m.")


@template(T2, S, 60)
def reactions(rng, level):
    L = rng.choice([10, 20, 30, 40])
    W = rng.randrange(10, 200, 10)
    a = rng.randrange(1, L)
    Rr = W * a / L
    if level == 8 or rng.random() < 0.3:
        return (f"A {L} m bridge carries a {W} kN load exactly in the middle. How much does each support carry?", unit(W / 2, "kN"),
                [unit(W, "kN"), unit(W / 4, "kN"), unit(W * 2, "kN"), unit(W / 3, "kN")], f"By symmetry each support takes half: {fmt(W / 2)} kN.")
    return (f"A {L} m bridge carries a {W} kN load {a} m from the left support. How much does the RIGHT support carry?", unit(Rr, "kN"),
            [unit(W - Rr, "kN") if a * 2 != L else unit(W, "kN"), unit(W / 2, "kN") if a * 2 != L else unit(W / 4, "kN"), unit(W * L / a, "kN"), unit(W * a / (2 * L), "kN")],
            f"Moments about the left support: R_right x {L} = {W} x {a}, so R_right = {fmt(Rr)} kN.")


@template(T2, S, 60)
def member_stress(rng, level):
    F, A = rng.randrange(10, 400, 10), rng.choice([10, 20, 40, 50, 80, 100])
    s = F * 1000 / (A * 100)
    return (f"A truss member carries {F} kN and has a cross-section of {A} cm². What is its stress?", unit(s, "MPa"),
            [unit(s * 10, "MPa"), unit(s / 10, "MPa"), unit(F / A, "MPa"), unit(s * 2, "MPa")],
            f"σ = F/A = {F}e3 N / {A}e-4 m² = {fmt(s)} MPa.")


@template(T2, S, 60)
def buckling_scale(rng, level):
    k = rng.choice([2, 3, 4, 0.5])
    f = 1 / k ** 2
    return (f"A strut's length is multiplied by {fmt(k)} (same material and shape). Its buckling load is multiplied by:", fmt(f),
            [fmt(1 / k), fmt(k), fmt(k * k), fmt(1 / k ** 3)], f"P_cr ∝ 1/L², so (1/{fmt(k)})² = {fmt(f)}.")


@template(T2, S, 60)
def end_post(rng, level):
    R, th = rng.randrange(20, 200, 10), rng.choice([30, 45, 60])
    F = R / math.sin(math.radians(th))
    return (f"An end post at {th}° to the deck must carry a support reaction of {R} kN up. What is the force in the post?", unit(F, "kN"),
            [unit(R, "kN"), unit(R * math.sin(math.radians(th)), "kN"), unit(R / math.cos(math.radians(th)), "kN") if th != 45 else unit(F * 2, "kN"), unit(F / 2, "kN")],
            f"Only its vertical part lifts: F sin {th}° = {R}, so F = {fmt(F)} kN (in compression).")


# ---------------- Project 3: Parabolic Thrust ----------------
facts(T3, S, [
    ("Under an even load, the ideal arch shape is a:", "Parabola", ["Square", "Straight line", "Zig-zag"], "A parabolic arch carries a uniform load in pure compression."),
    ("An arch pushes outward on its supports. This push is called:", "Thrust", ["Lift", "Drag", "Torque only"], "H = wL²/(8h) for a parabolic arch."),
    ("A taller (deeper) arch has ___ thrust for the same load and span.", "Less", ["More", "The same", "Zero"], "H ∝ 1/h."),
    ("Why must both arch supports be pins, not rollers?", "A roller cannot resist the outward thrust", ["Pins are cheaper",
     "Rollers are too heavy", "It does not matter"], "The arch would spread and fall."),
    ("Hangers in an arch bridge carry the road load:", "Up to the arch", ["Down to the river", "Sideways", "Nowhere"],
     "They are in tension when they work."),
    ("A cable hanger can go slack when:", "A moving load lifts part of the arch", ["The bridge is painted", "It is made of steel",
     "There is no load at all"], "Then it carries nothing; a steel hanger can both push and pull."),
    ("Concrete is good for arches because it is:", "Strong in compression", ["Strong in tension", "Very light", "Flexible like rope"],
     "Plain concrete cracks when pulled."),
    ("Diagonal braces in a pin-jointed arch:", "Stop it changing shape under moving loads", ["Make it heavier for no reason",
     "Carry only wind", "Are never needed"], "Without them the arch joints form a mechanism."),
    ("The Chenab Rail Bridge (J&K) is famous as:", "The world's highest railway arch bridge", ["The longest suspension bridge",
     "A wooden bridge", "An underwater tunnel"], "Its steel arch spans 467 m, 359 m above the river."),
])


@template(T3, S, 90)
def arch_thrust(rng, level):
    w, L, h = rng.randrange(5, 60, 5), rng.choice([20, 30, 40, 50, 60]), rng.choice([5, 6, 8, 10, 12])
    H = w * L * L / (8 * h)
    return (f"A parabolic arch of span {L} m and rise {h} m carries {w} kN/m. What is the horizontal thrust?", unit(H, "kN"),
            [unit(w * L * L / (4 * h), "kN"), unit(w * L / 2, "kN"), unit(w * L * L / (8 * h * h), "kN"), unit(H * 2, "kN")],
            f"H = wL²/(8h) = {w} x {L}² / (8 x {h}) = {fmt(H)} kN.")


@template(T3, S, 90)
def parabola_height(rng, level):
    L, h = rng.choice([20, 40, 60, 80]), rng.choice([6, 8, 10, 12, 16])
    x = rng.randrange(1, L)
    y = 4 * h * x * (L - x) / L ** 2
    return (f"A parabolic arch spans {L} m with rise {h} m. How high is it {x} m from the left support?", unit(y, "m"),
            [unit(h * x / L, "m"), unit(h, "m") if abs(y - h) > 0.01 else unit(h / 2, "m"), unit(y * 2, "m"), unit(4 * h * x / L, "m")],
            f"y = 4h x (L - x) / L² = {fmt(y)} m.")


@template(T3, S, 90)
def arch_support(rng, level):
    w, L, h = rng.randrange(5, 60, 5), rng.choice([20, 30, 40, 50]), rng.choice([5, 8, 10])
    H, V = w * L * L / (8 * h), w * L / 2
    R = math.hypot(H, V)
    if rng.random() < 0.5:
        return (f"A parabolic arch (span {L} m) carries {w} kN/m. What vertical reaction does each support give?", unit(V, "kN"),
                [unit(w * L, "kN"), unit(w * L / 4, "kN"), unit(H, "kN"), unit(V * 1.5, "kN")], f"V = wL/2 = {fmt(V)} kN.")
    return (f"Span {L} m, rise {h} m, load {w} kN/m. What is the total force at each arch support (thrust and vertical combined)?",
            unit(R, "kN"), [unit(H + V, "kN"), unit(H, "kN"), unit(V, "kN"), unit(R * 2, "kN")],
            f"H = {fmt(H)} kN, V = {fmt(V)} kN; R = √(H² + V²) = {fmt(R)} kN.")


@template(T3, S, 90)
def hanger_force(rng, level):
    w, s = rng.randrange(5, 80, 5), rng.choice([2, 3, 4, 5, 6])
    return (f"Hangers are {s} m apart and the road weighs {w} kN/m. How much does each hanger carry?", unit(w * s, "kN"),
            [unit(w / s, "kN"), unit(w, "kN"), unit(w * s * 2, "kN"), unit(w * s / 2, "kN")], f"Each hanger carries the road between it and its neighbours: {w} x {s} = {w * s} kN.")


# ---------------- Project 4: Stay Dynamics ----------------
facts(T4, S, [
    ("In a cable-stayed bridge, the road is held by cables running:", "Straight from the pylon to the deck", ["From a main curved cable",
     "Under the river", "Between two boats"], "In a suspension bridge, hangers drop from a main curved cable."),
    ("Backstay cables to the banks are needed because:", "They stop the pylon top swaying sideways", ["They hold the river",
     "They look nice", "They carry traffic"], "Without them the fan of stays plus the deck forms a mechanism."),
    ("A flatter stay (smaller angle) needs:", "More tension for the same lift", ["Less tension", "No tension", "Compression"],
     "T = W / sin θ."),
    ("The pylon of a cable-stayed bridge is mainly in:", "Compression", ["Tension", "No force", "Torsion only"],
     "The stays pull it down from both sides."),
    ("The horizontal pulls of the stays squeeze the deck. So the deck is in:", "Compression", ["Tension", "Nothing", "Shear only"],
     "This is why long cable-stayed decks must resist buckling."),
    ("Bandra-Worli Sea Link (Mumbai) is a:", "Cable-stayed bridge", ["Suspension bridge", "Truss bridge", "Floating bridge"],
     "Its main spans hang from stays on tall concrete pylons."),
    ("An impact factor of 1.15 means the design load is:", "15% more than the static load", ["15% less", "1.15 kg", "The same"],
     "Bumps and braking add dynamic load."),
])


@template(T4, S, 90)
def stay_tension(rng, level):
    W, h, d = rng.randrange(50, 600, 25), rng.choice([15, 20, 22, 25, 30]), rng.choice([5, 10, 15, 20, 25, 30])
    th = math.atan2(h, d)
    T = W / math.sin(th)
    return (f"A stay runs from a pylon top {h} m high to a deck point {d} m away and lifts {W} kN. What is its tension?", unit(T, "kN"),
            [unit(W, "kN"), unit(W / math.cos(th), "kN"), unit(W * math.sin(th), "kN"), unit(T * 2, "kN")],
            f"θ = atan({h}/{d}) = {fmt(math.degrees(th))}°; T = W / sin θ = {fmt(T)} kN.")


@template(T4, S, 90)
def stay_horizontal(rng, level):
    W, h, d = rng.randrange(50, 600, 25), rng.choice([15, 20, 25, 30]), rng.choice([5, 10, 15, 20, 30])
    H = W * d / h
    return (f"A stay lifts {W} kN at a deck point {d} m from the pylon; the pylon top is {h} m high. How hard does it pull the deck towards the pylon?",
            unit(H, "kN"), [unit(W * h / d, "kN"), unit(W, "kN"), unit(H / 2, "kN"), unit(math.hypot(W, H), "kN")],
            f"Horizontal / vertical = d / h, so H = {W} x {d}/{h} = {fmt(H)} kN.")


@template(T4, S, 90)
def cable_area(rng, level):
    T, s = rng.randrange(100, 3000, 50), rng.choice([500, 600, 750, 1000])
    A = T * 1000 / s
    return (f"A stay must carry {T} kN with an allowed stress of {s} MPa. What cross-section area is needed?", unit(A, "mm²"),
            [unit(T / s, "mm²"), unit(A * 10, "mm²"), unit(A / 10, "mm²"), unit(s / T * 1000, "mm²")],
            f"A = T / σ = {T}e3 N / {s} N/mm² = {fmt(A)} mm².")


@template(T4, S, 90)
def backstay(rng, level):
    hs = [rng.randrange(50, 400, 10) for _ in range(rng.randrange(2, 5))]
    total = sum(hs)
    return (f"The front stays pull the pylon top towards the river with horizontal forces of {', '.join(map(str, hs))} kN. "
            f"What horizontal pull must the backstays give to keep it still?", unit(total, "kN"),
            [unit(total / 2, "kN"), unit(max(hs), "kN"), unit(total * 2, "kN"), unit(total / len(hs), "kN")],
            f"ΣFx = 0 at the pylon top: backstays must pull {total} kN the other way.")


@template(T4, S, 60)
def impact_load(rng, level):
    m, f = rng.randrange(10, 200, 5), rng.choice([1.1, 1.15, 1.2, 1.25, 1.3])
    W = m * 9.81 * f
    return (f"A {m} t vehicle crosses with an impact factor of {f}. What design load should the bridge take? (g = 9.81)", unit(W, "kN"),
            [unit(m * 9.81, "kN"), unit(m * f, "kN"), unit(W * 1.5, "kN"), unit(m * 9.81 / f, "kN")], f"{m} x 9.81 x {f} = {fmt(W)} kN.")


# ---------------- Project 5: Matrix Dissipation ----------------
facts(T5, S, [
    ("Two members joined side by side share a load in proportion to their:", "Stiffness (EA/L)", ["Colour", "Age", "Length only"],
     "The stiffer one takes more: F1 = F k1/(k1 + k2)."),
    ("Resonance is dangerous when the forcing frequency is:", "Close to a natural frequency", ["Much lower than all natural frequencies",
     "Zero", "Exactly double the damping"], "The response can grow huge without damping."),
    ("Dampers make a bridge safer by:", "Turning vibration energy into heat", ["Adding traffic", "Making it lighter", "Removing cables"],
     "Tuned mass and viscous dampers absorb energy."),
    ("The London Millennium Bridge wobbled in 2000 because:", "People walking in step matched its sideways sway", ["Wind broke a cable",
     "A boat hit it", "It was too heavy"], "It was fixed with 91 dampers."),
    ("Carbon-fibre cable compared with steel cable of the same size is:", "Stronger and lighter", ["Weaker and heavier",
     "The same", "Unable to pull"], "But it costs much more."),
    ("In [K]{u} = {F}, K is the:", "Stiffness matrix", ["Force vector", "Displacement vector", "Mass"], "The game solves this for every test."),
    ("A tie between two pylon tops helps by:", "Sharing the pull between both pylons", ["Making traffic faster", "Adding weight only",
     "Lowering the deck"], "It balances the middle-span stays."),
])


@template(T5, S, 90)
def stiffness_share(rng, level):
    k1, k2, F = rng.randrange(10, 100, 5), rng.randrange(10, 100, 5), rng.randrange(100, 2000, 50)
    f1 = F * k1 / (k1 + k2)
    return (f"Two parallel members with stiffness {k1} and {k2} kN/mm share a {F} kN load. How much does the first carry?", unit(f1, "kN"),
            [unit(F / 2, "kN") if k1 != k2 else unit(F * 0.75, "kN"), unit(F * k2 / (k1 + k2), "kN") if k1 != k2 else unit(F / 4, "kN"), unit(F, "kN"), unit(f1 * 2, "kN")],
            f"F1 = F k1/(k1 + k2) = {F} x {k1}/{k1 + k2} = {fmt(f1)} kN.")


@template(T5, S, 90)
def natural_frequency(rng, level):
    k, m = rng.choice([1e5, 2e5, 5e5, 1e6, 4e6]), rng.choice([1e3, 2e3, 5e3, 1e4, 2e4])
    f = math.sqrt(k / m) / (2 * math.pi)
    return (f"A bridge mode has stiffness {k:g} N/m and mass {m:g} kg. What is its natural frequency?", unit(f, "Hz"),
            [unit(math.sqrt(k / m), "Hz"), unit(k / m / (2 * math.pi), "Hz"), unit(f * 2, "Hz"), unit(math.sqrt(m / k) / (2 * math.pi), "Hz")],
            f"f = (1/2π)√(k/m) = {fmt(f)} Hz.")


@template(T5, S, 90)
def amplification(rng, level):
    r = rng.choice([0.2, 0.4, 0.5, 0.6, 0.8, 0.9, 1.5, 2])
    A = 1 / abs(1 - r * r)
    return (f"An undamped bridge is shaken at {fmt(r)} times its natural frequency. By what factor is the static deflection amplified?", fmt(A),
            [fmt(1 / (1 + r * r)), fmt(1 - r * r) if r < 1 else fmt(r * r - 1), fmt(r), fmt(A * 2)],
            f"Dynamic amplification = 1/|1 - r²| = {fmt(A)}; near r = 1 it explodes (resonance).")


@template(T5, S, 90)
def carbon_vs_steel(rng, level):
    T = rng.randrange(500, 5000, 100)
    As, Ac = T * 1000 / 1500, T * 1000 / 2400
    return (f"A stay carries {T} kN. Using strengths of 1500 MPa (steel) and 2400 MPa (carbon fibre), how much less area does carbon need?",
            unit(As - Ac, "mm²"), [unit(As, "mm²"), unit(Ac, "mm²"), unit((As - Ac) * 2, "mm²"), unit(As + Ac, "mm²")],
            f"Steel {fmt(As)} mm², carbon {fmt(Ac)} mm²; difference {fmt(As - Ac)} mm².")


@template(T5, S, 60)
def convoy_impact(rng, level):
    n, m, f = rng.randrange(2, 8), rng.randrange(20, 60, 5), rng.choice([1.2, 1.25, 1.3])
    W = n * m * 9.81 * f
    return (f"A convoy of {n} trucks of {m} t each crosses with impact factor {f}. What total design load? (g = 9.81)", unit(W, "kN", 4),
            [unit(n * m * 9.81, "kN", 4), unit(m * 9.81 * f, "kN", 4), unit(W * f, "kN", 4), unit(n * m * f, "kN", 4)],
            f"{n} x {m} x 9.81 x {f} = {fmt(W, 4)} kN.")
