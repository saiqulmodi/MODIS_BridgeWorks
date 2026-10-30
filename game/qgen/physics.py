"""Physics high-yield numericals: Class 11 and 12 NCERT topics, at JEE Main (NIT), JEE Advanced (IIT), BE and Expert level."""
import math

from . import facts, fmt, near, template, unit

S = "physics"
G = 9.8
C11 = (11, 15, 13, 14, 16)        # Class 11 topics: Class 11, BE, NIT, IIT, Expert
C12 = (12, 15, 13, 14, 16)        # Class 12 topics
N = 60                            # questions per template per level


def pick(rng, *vals):
    return rng.choice(vals)


# ---------------- Class 11 ----------------
@template(C11, S, N)
def kinematics(rng, level):
    u = rng.randrange(0, 25)
    a = pick(rng, 1, 1.5, 2, 2.5, 3, 4, 5)
    t = rng.randrange(2, 12)
    kind = rng.randrange(3)
    if kind == 0:
        v = u + a * t
        return (f"A car starts at {u} m/s and accelerates uniformly at {a} m/s² for {t} s. What is its final speed?",
                unit(v, "m/s"), [unit(u + a * t * 2, "m/s"), unit(a * t, "m/s"), unit(u + a * t / 2, "m/s"), unit(u * a * t, "m/s")],
                f"v = u + at = {u} + {a} x {t} = {fmt(v)} m/s.")
    if kind == 1:
        s = u * t + 0.5 * a * t * t
        return (f"A body moving at {u} m/s accelerates at {a} m/s² for {t} s. How far does it go?", unit(s, "m"),
                [unit(u * t + a * t * t, "m"), unit(u * t, "m"), unit(0.5 * a * t * t, "m"), unit((u + a * t) * t, "m")],
                f"s = ut + ½at² = {u} x {t} + ½ x {a} x {t}² = {fmt(s)} m.")
    v = rng.randrange(10, 40)
    d = v * v / (2 * a)
    return (f"A vehicle moving at {v} m/s brakes with a deceleration of {a} m/s². What is its stopping distance?", unit(d, "m"),
            [unit(v * v / a, "m"), unit(v / (2 * a), "m"), unit(v * a, "m"), unit(v * v / (4 * a), "m")],
            f"v² = u² - 2as  ->  s = u²/(2a) = {v}²/(2 x {a}) = {fmt(d)} m.")


@template(C11, S, N)
def projectile(rng, level):
    u = rng.randrange(10, 50)
    th = pick(rng, 15, 30, 37, 45, 53, 60, 75)
    r = math.radians(th)
    kind = rng.randrange(3)
    if kind == 0:
        R = u * u * math.sin(2 * r) / G
        return (f"A ball is thrown at {u} m/s at {th}° above the horizontal (g = 9.8 m/s²). What is its horizontal range?",
                unit(R, "m"), [unit(u * u / G, "m"), unit(u * u * math.sin(r) / G, "m"), unit(R / 2, "m"), unit(R * 2, "m")],
                f"R = u² sin 2θ / g = {u}² x sin {2 * th}° / 9.8 = {fmt(R)} m.")
    if kind == 1:
        H = (u * math.sin(r)) ** 2 / (2 * G)
        return (f"A stone is projected at {u} m/s at {th}° to the horizontal (g = 9.8 m/s²). What is its maximum height?",
                unit(H, "m"), [unit(u * u / (2 * G), "m"), unit(2 * H, "m"), unit((u * math.cos(r)) ** 2 / (2 * G), "m"), unit(H / 2, "m")],
                f"H = u² sin²θ / 2g = {fmt(H)} m.")
    T = 2 * u * math.sin(r) / G
    return (f"A projectile is fired at {u} m/s at {th}° (g = 9.8 m/s²). What is its time of flight?", unit(T, "s"),
            [unit(T / 2, "s"), unit(2 * u / G, "s"), unit(u * math.sin(r) / (2 * G), "s"), unit(2 * u * math.cos(r) / G, "s")],
            f"T = 2u sin θ / g = 2 x {u} x sin {th}° / 9.8 = {fmt(T)} s.")


@template(C11, S, N)
def newton_laws(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        m1, m2 = rng.randrange(2, 12), rng.randrange(1, 10)
        if m1 == m2:
            m1 += 1
        a = abs(m1 - m2) * G / (m1 + m2)
        T = 2 * m1 * m2 * G / (m1 + m2)
        if rng.random() < 0.5:
            return (f"Masses of {m1} kg and {m2} kg hang over a light frictionless pulley (Atwood machine, g = 9.8 m/s²). "
                    f"What is their acceleration?", unit(a, "m/s²"),
                    [unit(G, "m/s²"), unit(abs(m1 - m2) * G / max(m1, m2), "m/s²"), unit(a * 2, "m/s²"), unit((m1 + m2) * G / abs(m1 - m2), "m/s²")],
                    f"a = (m1 - m2) g / (m1 + m2) = {abs(m1 - m2)} x 9.8 / {m1 + m2} = {fmt(a)} m/s².")
        return (f"In an Atwood machine with {m1} kg and {m2} kg (g = 9.8 m/s²), what is the string tension?", unit(T, "N"),
                [unit(m1 * G, "N"), unit(m2 * G, "N"), unit((m1 + m2) * G, "N"), unit(T / 2, "N")],
                f"T = 2 m1 m2 g / (m1 + m2) = {fmt(T)} N.")
    if kind == 1:
        m = rng.randrange(2, 30)
        F = rng.randrange(20, 200, 5)
        mu = pick(rng, 0.1, 0.2, 0.25, 0.3, 0.4)
        fr = mu * m * G
        if F <= fr:
            F = int(fr) + 20
        a = (F - fr) / m
        return (f"A {m} kg block on a rough floor (μk = {mu}) is pulled horizontally with {F} N. What is its acceleration? (g = 9.8 m/s²)",
                unit(a, "m/s²"), [unit(F / m, "m/s²"), unit((F + fr) / m, "m/s²"), unit(a / 2, "m/s²"), unit(fr / m, "m/s²")],
                f"a = (F - μmg)/m = ({F} - {fmt(fr)}) / {m} = {fmt(a)} m/s².")
    th = pick(rng, 30, 37, 45, 53, 60)
    a = G * math.sin(math.radians(th))
    return (f"A block slides down a smooth incline of {th}° (g = 9.8 m/s²). What is its acceleration?", unit(a, "m/s²"),
            [unit(G * math.cos(math.radians(th)), "m/s²"), unit(G, "m/s²"), unit(G * math.tan(math.radians(th)), "m/s²"), unit(a / 2, "m/s²")],
            f"a = g sin θ = 9.8 x sin {th}° = {fmt(a)} m/s².")


@template(C11, S, N)
def work_energy(rng, level):
    kind = rng.randrange(3)
    m = rng.randrange(1, 60)
    if kind == 0:
        v = rng.randrange(2, 30)
        ke = 0.5 * m * v * v
        return (f"What is the kinetic energy of a {m} kg body moving at {v} m/s?", unit(ke, "J"),
                [unit(m * v * v, "J"), unit(m * v, "J"), unit(0.5 * m * v, "J"), unit(ke * 2, "J")], f"KE = ½mv² = ½ x {m} x {v}² = {fmt(ke)} J.")
    if kind == 1:
        h = rng.randrange(2, 50)
        v = math.sqrt(2 * G * h)
        return (f"A body falls freely from {h} m (g = 9.8 m/s²). With what speed does it hit the ground?", unit(v, "m/s"),
                [unit(G * h, "m/s"), unit(math.sqrt(G * h), "m/s"), unit(2 * G * h, "m/s"), unit(v / 2, "m/s")],
                f"mgh = ½mv²  ->  v = √(2gh) = √(2 x 9.8 x {h}) = {fmt(v)} m/s.")
    h = rng.randrange(5, 40)
    t = rng.randrange(5, 60)
    P = m * G * h / t
    return (f"A pump lifts {m * 10} kg of water through {h} m in {t} s (g = 9.8 m/s²). What is its power?", unit(P * 10, "W"),
            [unit(P, "W"), unit(m * 10 * h / t, "W"), unit(P * 10 * t, "W"), unit(P * 5, "W")],
            f"P = mgh/t = {m * 10} x 9.8 x {h} / {t} = {fmt(P * 10)} W.")


@template(C11, S, N)
def circular(rng, level):
    kind = rng.randrange(2)
    if kind == 0:
        m, v, r = rng.randrange(1, 2000, 50), rng.randrange(5, 30), rng.randrange(10, 200, 5)
        F = m * v * v / r
        return (f"A {m} kg car goes round a curve of radius {r} m at {v} m/s. What centripetal force is needed?", unit(F, "N"),
                [unit(m * v / r, "N"), unit(m * v * v * r, "N"), unit(F * 2, "N"), unit(m * v * v / (2 * r), "N")],
                f"F = mv²/r = {m} x {v}² / {r} = {fmt(F)} N.")
    mu, r = pick(rng, 0.2, 0.3, 0.4, 0.5, 0.6), rng.randrange(20, 300, 10)
    v = math.sqrt(mu * r * G)
    return (f"What is the maximum safe speed on a flat circular road of radius {r} m if μs = {mu}? (g = 9.8 m/s²)", unit(v, "m/s"),
            [unit(mu * r * G, "m/s"), unit(math.sqrt(r * G), "m/s"), unit(v * 2, "m/s"), unit(math.sqrt(mu * r), "m/s")],
            f"μmg = mv²/r  ->  v = √(μrg) = {fmt(v)} m/s.")


@template(C11, S, N)
def momentum(rng, level):
    m1, m2 = rng.randrange(1, 20), rng.randrange(1, 20)
    u1, u2 = rng.randrange(2, 20), rng.randrange(-10, 10)
    v = (m1 * u1 + m2 * u2) / (m1 + m2)
    loss = 0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2 - 0.5 * (m1 + m2) * v * v
    if rng.random() < 0.6 or level in (11, 15):
        return (f"A {m1} kg body at {u1} m/s collides with a {m2} kg body at {u2} m/s (same line) and they stick together. "
                f"What is their common velocity?", unit(v, "m/s"),
                [unit((m1 * u1 - m2 * u2) / (m1 + m2), "m/s"), unit((u1 + u2) / 2, "m/s"), unit(m1 * u1 / m2, "m/s"), unit(v * 2, "m/s")],
                f"Momentum is conserved: v = (m1u1 + m2u2)/(m1 + m2) = {fmt(v)} m/s.")
    return (f"A {m1} kg body at {u1} m/s hits a {m2} kg body at {u2} m/s head-on and they stick. How much kinetic energy is lost?",
            unit(loss, "J"), [unit(0.5 * m1 * u1 ** 2, "J"), unit(loss / 2, "J"), unit(loss * 2, "J"), "0 J"],
            f"v = {fmt(v)} m/s; KE before - KE after = {fmt(loss)} J (lost to heat and sound).")


@template(C11, S, N)
def gravitation(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        k = pick(rng, 0.5, 1, 2, 3)
        g = G / (1 + k) ** 2
        return (f"At a height equal to {fmt(k)} x Earth's radius, what is g? (g on the surface = 9.8 m/s²)", unit(g, "m/s²"),
                [unit(G / (1 + k), "m/s²"), unit(G / k ** 2 if k != 1 else G / 3, "m/s²"), unit(G * (1 - 2 * k) if k < 0.5 else G / (2 + k) ** 2, "m/s²"), unit(g * 2, "m/s²")],
                f"g_h = g R²/(R + h)² = 9.8 / {fmt(1 + k)}² = {fmt(g)} m/s².")
    if kind == 1:
        Mf, Rf = pick(rng, 2, 4, 8, 9, 16), pick(rng, 2, 3, 4, 0.5)
        ve = 11.2 * math.sqrt(Mf / Rf)
        return (f"A planet has {Mf} times Earth's mass and {fmt(Rf)} times its radius. What is its escape speed? (Earth: 11.2 km/s)",
                unit(ve, "km/s"), [unit(11.2 * Mf / Rf, "km/s"), unit(11.2 * math.sqrt(Rf / Mf), "km/s"), unit(11.2 * Mf, "km/s"), unit(ve / 2, "km/s")],
                f"v_e = √(2GM/R), so it scales as √(M/R) = √({Mf}/{fmt(Rf)}); 11.2 x {fmt(math.sqrt(Mf / Rf))} = {fmt(ve)} km/s.")
    k = pick(rng, 2, 3, 4, 9, 16)
    T = k ** 1.5
    return (f"Satellite B orbits at {k} times the orbital radius of satellite A. How many times A's period is B's period?",
            fmt(T), [str(k), fmt(k * k), fmt(math.sqrt(k)), fmt(k ** 3)], f"Kepler's third law: T² ∝ r³, so T ∝ r^1.5 = {k}^1.5 = {fmt(T)}.")


@template(C11, S, N)
def rotation(rng, level):
    kind = rng.randrange(3)
    M, L = rng.randrange(1, 12), pick(rng, 0.5, 1, 1.2, 1.5, 2, 3)
    if kind == 0:
        I = M * L * L / 12
        return (f"What is the moment of inertia of a uniform {M} kg rod of length {L} m about an axis through its centre, perpendicular to it?",
                unit(I, "kg m²"), [unit(M * L * L / 3, "kg m²"), unit(M * L * L, "kg m²"), unit(M * L * L / 2, "kg m²"), unit(M * L / 12, "kg m²")],
                f"I = ML²/12 = {M} x {L}² / 12 = {fmt(I)} kg m² (about one end it is ML²/3).")
    if kind == 1:
        R = L / 2
        I = 0.5 * M * R * R
        return (f"A uniform disc of mass {M} kg and radius {fmt(R)} m spins about its axis. What is its moment of inertia?",
                unit(I, "kg m²"), [unit(M * R * R, "kg m²"), unit(0.4 * M * R * R, "kg m²"), unit(0.25 * M * R * R, "kg m²"), unit(M * R / 2, "kg m²")],
                f"Disc: I = ½MR² = {fmt(I)} kg m² (ring: MR²; solid sphere: 2/5 MR²).")
    I1, w1 = rng.randrange(2, 10), rng.randrange(2, 12)
    f = pick(rng, 2, 3, 4)
    return (f"A skater with moment of inertia {I1} kg m² spins at {w1} rad/s and pulls their arms in, making I {f} times smaller. "
            f"What is the new angular speed?", unit(w1 * f, "rad/s"),
            [unit(w1 / f, "rad/s"), unit(w1, "rad/s"), unit(w1 * f * f, "rad/s"), unit(w1 * math.sqrt(f), "rad/s")],
            f"L = Iω is conserved: ω2 = ω1 x I1/I2 = {w1} x {f} = {w1 * f} rad/s.")


@template(C11, S, N)
def shm(rng, level):
    if rng.random() < 0.5:
        m, k = pick(rng, 0.1, 0.2, 0.25, 0.5, 1, 2, 4), rng.randrange(10, 400, 10)
        T = 2 * math.pi * math.sqrt(m / k)
        return (f"A {m} kg mass on a spring of stiffness {k} N/m oscillates. What is its period?", unit(T, "s"),
                [unit(2 * math.pi * math.sqrt(k / m), "s"), unit(math.sqrt(m / k), "s"), unit(T * 2, "s"), unit(2 * math.pi * m / k, "s")],
                f"T = 2π√(m/k) = 2π√({m}/{k}) = {fmt(T)} s.")
    Lp = pick(rng, 0.25, 0.5, 1, 1.5, 2, 2.45, 4, 9.8)
    T = 2 * math.pi * math.sqrt(Lp / G)
    return (f"What is the period of a simple pendulum of length {Lp} m? (g = 9.8 m/s²)", unit(T, "s"),
            [unit(2 * math.pi * math.sqrt(G / Lp), "s"), unit(math.sqrt(Lp / G), "s"), unit(T / 2, "s"), unit(2 * math.pi * Lp / G, "s")],
            f"T = 2π√(L/g) = {fmt(T)} s (it does not depend on the mass).")


@template(C11, S, N)
def waves(rng, level):
    kind = rng.randrange(3) if level in (13, 14, 16) else rng.randrange(2)
    if kind == 0:
        f, lam = rng.randrange(100, 2000, 50), pick(rng, 0.17, 0.25, 0.34, 0.5, 0.68, 1, 1.5)
        return (f"A wave of frequency {f} Hz has wavelength {lam} m. What is its speed?", unit(f * lam, "m/s"),
                [unit(f / lam, "m/s"), unit(lam / f, "m/s"), unit(f * lam * 2, "m/s"), unit(f * lam / 2, "m/s")], f"v = fλ = {f} x {lam} = {fmt(f * lam)} m/s.")
    if kind == 1:
        T, mu = rng.randrange(10, 400, 10), pick(rng, 0.001, 0.004, 0.01, 0.025, 0.1)
        v = math.sqrt(T / mu)
        return (f"A string under {T} N tension has linear mass density {mu} kg/m. What is the wave speed on it?", unit(v, "m/s"),
                [unit(T / mu, "m/s"), unit(math.sqrt(mu / T), "m/s"), unit(v * 2, "m/s"), unit(math.sqrt(T * mu), "m/s")], f"v = √(T/μ) = {fmt(v)} m/s.")
    f0, vs = rng.randrange(300, 1000, 20), rng.randrange(10, 60, 5)
    f = f0 * 340 / (340 - vs)
    return (f"An ambulance siren of {f0} Hz approaches a still listener at {vs} m/s (sound speed 340 m/s). What frequency is heard?",
            unit(f, "Hz", 4), [unit(f0 * 340 / (340 + vs), "Hz", 4), unit(f0 * (340 + vs) / 340, "Hz", 4), unit(f0, "Hz"), unit(f0 + vs, "Hz")],
            f"f' = f v/(v - vs) = {f0} x 340 / {340 - vs} = {fmt(f, 4)} Hz.")


@template(C11, S, N)
def thermal(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        m, dT = pick(rng, 0.2, 0.5, 1, 2, 5), rng.randrange(5, 80)
        c = pick(rng, 4200, 900, 390, 130, 2100)
        Q = m * c * dT
        return (f"How much heat raises {m} kg of a substance with specific heat {c} J/(kg K) by {dT} K?", unit(Q, "J"),
                [unit(c * dT, "J"), unit(m * c, "J"), unit(Q / 2, "J"), unit(m * dT, "J")], f"Q = mcΔT = {m} x {c} x {dT} = {fmt(Q)} J.")
    if kind == 1:
        Th, Tc = rng.randrange(400, 900, 25), rng.randrange(250, 380, 10)
        eta = 1 - Tc / Th
        return (f"A Carnot engine works between {Th} K and {Tc} K. What is its efficiency?", f"{fmt(eta * 100)}%",
                [f"{fmt(Tc / Th * 100)}%", f"{fmt((Th - Tc) / Tc * 100)}%", f"{fmt(eta * 50)}%", "100%"], f"η = 1 - Tc/Th = 1 - {Tc}/{Th} = {fmt(eta * 100)}%.")
    n, T, V = pick(rng, 0.5, 1, 2, 3), rng.randrange(250, 600, 10), pick(rng, 0.01, 0.02, 0.0224, 0.05)
    P = n * 8.314 * T / V
    return (f"{n} mol of an ideal gas at {T} K fills {V} m³. What is its pressure? (R = 8.314 J/mol K)", unit(P, "Pa"),
            [unit(n * T / V, "Pa"), unit(P / 2, "Pa"), unit(n * 8.314 * V / T, "Pa"), unit(P * 2, "Pa")], f"P = nRT/V = {fmt(P)} Pa.")


@template(C11, S, N)
def fluids_elasticity(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        h, rho = rng.randrange(2, 100), pick(rng, 1000, 1030, 800, 13600)
        p = rho * G * h
        return (f"What is the gauge pressure at a depth of {h} m in a liquid of density {rho} kg/m³? (g = 9.8 m/s²)", unit(p, "Pa"),
                [unit(rho * h, "Pa"), unit(p + 101325, "Pa"), unit(p / 2, "Pa"), unit(rho * G / h, "Pa")], f"p = ρgh = {fmt(p)} Pa.")
    if kind == 1:
        F, L = rng.randrange(100, 5000, 100), pick(rng, 1, 2, 3, 5)
        A, Y = pick(rng, 1e-6, 2e-6, 5e-6, 1e-5), pick(rng, 2e11, 1e11, 7e10)
        dL = F * L / (A * Y)
        return (f"A wire of length {L} m and area {A:g} m² (Y = {Y:g} Pa) carries a load of {F} N. By how many mm does it stretch?",
                unit(dL * 1000, "mm"), [unit(dL * 100, "mm"), unit(dL * 2000, "mm"), unit(F / (A * Y) * 1000, "mm"), unit(dL * 10000, "mm")],
                f"ΔL = FL/(AY) = {fmt(dL * 1000)} mm.")
    A1, v1 = pick(rng, 0.02, 0.05, 0.1), rng.randrange(1, 6)
    A2 = A1 / pick(rng, 2, 4, 5)
    v2 = A1 * v1 / A2
    return (f"Water flows at {v1} m/s in a pipe of area {A1} m² that narrows to {fmt(A2)} m². What is its speed in the narrow part?",
            unit(v2, "m/s"), [unit(v1 * A2 / A1, "m/s"), unit(v1, "m/s"), unit(v2 * 2, "m/s"), unit(v2 / 2, "m/s")],
            f"Continuity: A1v1 = A2v2  ->  v2 = {fmt(v2)} m/s.")


# ---------------- Class 12 ----------------
K = 9e9


@template(C12, S, N)
def electrostatics(rng, level):
    kind = rng.randrange(3)
    q1, q2 = rng.randrange(1, 10), rng.randrange(1, 10)
    r = pick(rng, 0.1, 0.2, 0.3, 0.5, 1)
    if kind == 0:
        F = K * q1 * q2 * 1e-12 / r ** 2
        return (f"Two charges of {q1} μC and {q2} μC are {r} m apart in air. What is the force between them? (k = 9 x 10⁹)",
                unit(F, "N"), [unit(F * r, "N"), unit(F / 2, "N"), unit(K * q1 * q2 * 1e-12 / r, "N"), unit(F * 4, "N")],
                f"F = k q1 q2 / r² = 9e9 x {q1}e-6 x {q2}e-6 / {r}² = {fmt(F)} N.")
    if kind == 1:
        E = K * q1 * 1e-6 / r ** 2
        return (f"What is the electric field {r} m from a {q1} μC point charge? (k = 9 x 10⁹)", unit(E, "N/C"),
                [unit(K * q1 * 1e-6 / r, "N/C"), unit(E / 2, "N/C"), unit(E * 2, "N/C"), unit(K * q1 * 1e-6 * r, "N/C")],
                f"E = kq/r² = {fmt(E)} N/C.")
    V = K * q1 * 1e-6 / r
    return (f"What is the electric potential {r} m from a {q1} μC point charge? (k = 9 x 10⁹)", unit(V, "V"),
            [unit(V / r, "V"), unit(V * r, "V"), unit(V / 2, "V"), unit(V * 2, "V")], f"V = kq/r = {fmt(V)} V.")


@template(C12, S, N)
def capacitors(rng, level):
    kind = rng.randrange(3)
    c1, c2 = rng.randrange(1, 12), rng.randrange(1, 12)
    if kind == 0:
        cs = c1 * c2 / (c1 + c2)
        return (f"Capacitors of {c1} μF and {c2} μF are joined in series. What is the total capacitance?", unit(cs, "μF"),
                [unit(c1 + c2, "μF"), unit((c1 + c2) / 2, "μF"), unit(c1 * c2, "μF"), unit(cs * 2, "μF")], f"1/C = 1/{c1} + 1/{c2}  ->  C = {fmt(cs)} μF.")
    if kind == 1:
        V = rng.randrange(5, 500, 5)
        U = 0.5 * c1 * 1e-6 * V * V
        return (f"How much energy is stored in a {c1} μF capacitor charged to {V} V?", unit(U, "J"),
                [unit(c1 * 1e-6 * V * V, "J"), unit(0.5 * c1 * 1e-6 * V, "J"), unit(U / 2, "J"), unit(U * 4, "J")], f"U = ½CV² = {fmt(U)} J.")
    A, d = pick(rng, 0.01, 0.02, 0.05, 0.1, 0.5), pick(rng, 0.001, 0.002, 0.005, 0.0001)
    k = pick(rng, 1, 2, 4, 5)
    C = k * 8.85e-12 * A / d
    return (f"A parallel-plate capacitor has plates of area {A} m², {d * 1000:g} mm apart, with a dielectric of K = {k}. "
            f"What is its capacitance? (ε0 = 8.85 x 10⁻¹² F/m)", unit(C * 1e12, "pF"),
            [unit(C * 1e12 / k, "pF"), unit(C * 1e12 * 2, "pF"), unit(k * 8.85 * d / A, "pF"), unit(C * 1e12 / 10, "pF")],
            f"C = Kε0A/d = {fmt(C * 1e12)} pF.")


@template(C12, S, N)
def current_electricity(rng, level):
    kind = rng.randrange(3)
    r1, r2 = rng.randrange(1, 30), rng.randrange(1, 30)
    if kind == 0:
        rp = r1 * r2 / (r1 + r2)
        return (f"Resistors of {r1} Ω and {r2} Ω are in parallel. What is the equivalent resistance?", unit(rp, "Ω"),
                [unit(r1 + r2, "Ω"), unit((r1 + r2) / 2, "Ω"), unit(abs(r1 - r2) or 1, "Ω"), unit(rp * 2, "Ω")], f"R = r1 r2 / (r1 + r2) = {fmt(rp)} Ω.")
    if kind == 1:
        E, r = rng.randrange(2, 24), pick(rng, 0.2, 0.5, 1, 2)
        I = E / (r1 + r)
        return (f"A cell of emf {E} V and internal resistance {r} Ω drives a {r1} Ω resistor. What is the current?", unit(I, "A"),
                [unit(E / r1, "A"), unit(E / r, "A"), unit(E / (r1 - r) if r1 > r else E * 2, "A"), unit(I * 2, "A")],
                f"I = E/(R + r) = {E}/({r1} + {r}) = {fmt(I)} A.")
    V = pick(rng, 110, 220, 230, 12, 24)
    P = rng.randrange(20, 2000, 20)
    R = V * V / P
    return (f"A device is rated {P} W at {V} V. What is its resistance?", unit(R, "Ω"),
            [unit(P / V, "Ω"), unit(V / P, "Ω"), unit(P * P / V, "Ω"), unit(R / 2, "Ω")], f"P = V²/R  ->  R = V²/P = {V}² / {P} = {fmt(R)} Ω.")


MU0 = 4 * math.pi * 1e-7


@template(C12, S, N)
def magnetism(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        I, r = rng.randrange(1, 50), pick(rng, 0.01, 0.02, 0.05, 0.1, 0.2)
        B = MU0 * I / (2 * math.pi * r)
        return (f"What is the magnetic field {r} m from a long straight wire carrying {I} A? (μ0 = 4π x 10⁻⁷)", unit(B * 1e6, "μT"),
                [unit(B * 1e6 * 2, "μT"), unit(B * 1e6 / 2, "μT"), unit(MU0 * I / (2 * r) * 1e6, "μT"), unit(B * 1e6 * math.pi, "μT")],
                f"B = μ0 I / (2πr) = 2 x 10⁻⁷ x {I} / {r} = {fmt(B * 1e6)} μT.")
    if kind == 1:
        v, B = pick(rng, 1e5, 2e5, 5e5, 1e6), pick(rng, 0.01, 0.05, 0.1, 0.5)
        r = 9.11e-31 * v / (1.6e-19 * B)
        return (f"An electron moves at {v:g} m/s at right angles to a {B} T field. What is the radius of its circle? (m = 9.11e-31 kg, e = 1.6e-19 C)",
                unit(r * 1e6, "μm"), [unit(r * 2e6, "μm"), unit(r * 0.5e6, "μm"), unit(1.6e-19 * B / (9.11e-31 * v) * 1e6, "μm"), unit(r * 1e7, "μm")],
                f"r = mv/(qB) = {fmt(r * 1e6)} μm.")
    I, L, B = rng.randrange(1, 20), pick(rng, 0.1, 0.2, 0.5, 1), pick(rng, 0.1, 0.2, 0.5, 1)
    th = pick(rng, 30, 90, 60)
    F = B * I * L * math.sin(math.radians(th))
    return (f"A {L} m wire carrying {I} A lies at {th}° to a {B} T field. What force acts on it?", unit(F, "N"),
            [unit(B * I * L, "N") if th != 90 else unit(F / 2, "N"), unit(B * I * L * math.cos(math.radians(th)), "N") if th != 90 else unit(F * 2, "N"),
             unit(F * 3, "N"), unit(B * I / L, "N")], f"F = BIL sin θ = {fmt(F)} N.")


@template(C12, S, N)
def emi_ac(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        B, L, v = pick(rng, 0.1, 0.2, 0.5, 1), pick(rng, 0.1, 0.2, 0.5, 1, 2), rng.randrange(1, 20)
        e = B * L * v
        return (f"A {L} m rod moves at {v} m/s perpendicular to a {B} T field. What emf is induced across it?", unit(e, "V"),
                [unit(B * v / L, "V"), unit(B * L / v, "V"), unit(e * 2, "V"), unit(0.5 * B * L * v, "V")], f"e = BLv = {fmt(e)} V.")
    if kind == 1:
        Vp = rng.randrange(10, 400, 10)
        return (f"An AC voltage has a peak value of {Vp} V. What is its rms value?", unit(Vp / math.sqrt(2), "V"),
                [unit(Vp * math.sqrt(2), "V"), unit(Vp / 2, "V"), unit(Vp, "V"), unit(Vp * 0.637, "V")], f"V_rms = V0/√2 = {fmt(Vp / math.sqrt(2))} V.")
    Lh, Cf = pick(rng, 0.01, 0.05, 0.1, 0.5, 1), pick(rng, 1e-6, 2e-6, 10e-6, 100e-9, 50e-6)
    f = 1 / (2 * math.pi * math.sqrt(Lh * Cf))
    return (f"What is the resonant frequency of an LC circuit with L = {Lh} H and C = {Cf * 1e6:g} μF?", unit(f, "Hz", 4),
            [unit(1 / math.sqrt(Lh * Cf), "Hz", 4), unit(f * 2, "Hz", 4), unit(2 * math.pi * math.sqrt(Lh * Cf), "Hz", 4), unit(f / 2, "Hz", 4)],
            f"f = 1/(2π√(LC)) = {fmt(f, 4)} Hz.")


@template(C12, S, N)
def optics(rng, level):
    kind = rng.randrange(4)
    if kind == 0:
        u, f = -rng.randrange(15, 60, 5), rng.choice([10, 12, 15, 20, 25])
        if abs(u) == f:
            u -= 5
        v = 1 / (1 / f + 1 / u)
        return (f"An object is {abs(u)} cm in front of a convex lens of focal length {f} cm. Where is the image?",
                f"{fmt(abs(v))} cm on the {'other' if v > 0 else 'same'} side",
                [f"{fmt(abs(1 / (1 / f - 1 / u)))} cm on the other side", f"{fmt(abs(u) + f)} cm on the other side",
                 f"{fmt(abs(v) * 2)} cm on the other side", f"{fmt(abs(v))} cm on the {'same' if v > 0 else 'other'} side"],
                f"1/v - 1/u = 1/f with u = {u}: v = {fmt(v)} cm.")
    if kind == 1:
        n = pick(rng, 1.33, 1.5, 1.6, 2.42, 1.7)
        c = math.degrees(math.asin(1 / n))
        return (f"What is the critical angle for light going from a medium of refractive index {n} into air?", f"{fmt(c)}°",
                [f"{fmt(90 - c)}°", f"{fmt(math.degrees(math.atan(1 / n)))}°", f"{fmt(c / 2)}°", f"{fmt(math.degrees(math.asin(1 / n ** 2)))}°"],
                f"sin C = 1/n = {fmt(1 / n)}  ->  C = {fmt(c)}°.")
    if kind == 2:
        lam, D, d = pick(rng, 400, 500, 550, 600, 650, 700), pick(rng, 0.5, 1, 1.5, 2), pick(rng, 0.1, 0.2, 0.25, 0.5, 1)
        beta = lam * 1e-9 * D / (d * 1e-3)
        return (f"In Young's double slit, λ = {lam} nm, slit gap = {d} mm and screen distance = {D} m. What is the fringe width?",
                unit(beta * 1000, "mm"), [unit(beta * 2000, "mm"), unit(beta * 500, "mm"), unit(lam * 1e-9 * d / D * 1e6, "mm"), unit(beta * 10000, "mm")],
                f"β = λD/d = {fmt(beta * 1000)} mm.")
    f1, f2 = pick(rng, 10, 20, 25, 40, 50), pick(rng, 10, 20, -25, 40, -50)
    P = 100 / f1 + 100 / f2
    return (f"Two thin lenses of focal lengths {f1} cm and {f2} cm are in contact. What is the power of the combination?", unit(P, "D"),
            [unit(1 / f1 + 1 / f2, "D"), unit(100 / (f1 + f2) if f1 + f2 else 5, "D"), unit(-P, "D") if P else "1 D", unit(P * 2, "D") if P else "2 D"],
            f"P = 100/f1 + 100/f2 (f in cm) = {fmt(P)} D.")


@template(C12, S, N)
def modern(rng, level):
    kind = rng.randrange(4)
    if kind == 0:
        lam = rng.randrange(200, 700, 10)
        E = 1240 / lam
        return (f"What is the energy of a photon of wavelength {lam} nm? (hc = 1240 eV nm)", unit(E, "eV"),
                [unit(lam / 1240, "eV"), unit(E * 2, "eV"), unit(E / 2, "eV"), unit(1240 * lam / 1e3, "eV")], f"E = hc/λ = 1240/{lam} = {fmt(E)} eV.")
    if kind == 1:
        lam, W = rng.randrange(150, 450, 10), pick(rng, 2.0, 2.3, 2.5, 3.0, 4.2)
        if 1240 / lam <= W:
            lam = 200
        K_ = 1240 / lam - W
        return (f"Light of {lam} nm falls on a metal of work function {W} eV. What is the maximum kinetic energy of the photoelectrons?",
                unit(K_, "eV"), [unit(1240 / lam + W, "eV"), unit(1240 / lam, "eV"), unit(W, "eV"), unit(K_ * 2, "eV")],
                f"K_max = hc/λ - φ = {fmt(1240 / lam)} - {W} = {fmt(K_)} eV.")
    if kind == 2:
        n1, n2 = sorted(rng.sample(range(1, 6), 2))
        dE = 13.6 * (1 / n1 ** 2 - 1 / n2 ** 2)
        return (f"What energy is emitted when a hydrogen electron falls from n = {n2} to n = {n1}?", unit(dE, "eV"),
                [unit(13.6 / n2 ** 2, "eV"), unit(13.6 / n1 ** 2, "eV"), unit(13.6 * (1 / n1 - 1 / n2), "eV"), unit(dE * 2, "eV")],
                f"ΔE = 13.6 (1/{n1}² - 1/{n2}²) = {fmt(dE)} eV.")
    T = rng.randrange(2, 30)
    n = rng.randrange(2, 6)
    frac = 1 / 2 ** n
    return (f"A radioactive sample has a half-life of {T} days. What fraction remains after {T * n} days?", f"1/{2 ** n}",
            [f"1/{2 * n}", f"1/{2 ** (n - 1)}", f"1/{2 ** (n + 1)}", f"1/{n}"], f"{n} half-lives: (½)^{n} = 1/{2 ** n} = {fmt(frac)}.")


# ---------------- concepts ----------------
facts((11, 12, 15, 13, 14, 16), S, [
    ("The dimensional formula of Planck's constant is:", "[M L² T⁻¹]", ["[M L T⁻²]", "[M L² T⁻²]", "[M⁰ L T⁻¹]"],
     "h = E/f: [ML²T⁻²]/[T⁻¹] = [ML²T⁻¹], same as angular momentum."),
    ("Which quantity is a vector?", "Impulse", ["Work", "Power", "Energy"], "Impulse = change in momentum, which has direction."),
    ("A body moves in a circle at constant speed. Its acceleration is:", "Towards the centre", ["Zero", "Along the tangent",
     "Away from the centre"], "Centripetal acceleration v²/r points to the centre."),
    ("For a projectile, maximum range on level ground is at:", "45°", ["30°", "60°", "90°"], "sin 2θ is largest at θ = 45°."),
    ("The work done by a centripetal force is:", "Zero", ["Positive", "Negative", "mv²"], "Force is perpendicular to displacement."),
    ("Escape speed from Earth depends on:", "Earth's mass and radius, not the body's mass", ["The body's mass", "Angle of launch only",
     "The body's shape"], "v_e = √(2GM/R)."),
    ("In an adiabatic process:", "No heat enters or leaves", ["Temperature is constant", "Pressure is constant", "Volume is constant"],
     "Q = 0; PV^γ is constant for an ideal gas."),
    ("The SI unit of magnetic flux is the:", "Weber", ["Tesla", "Henry", "Gauss"], "1 Wb = 1 T m²."),
    ("Lenz's law follows from conservation of:", "Energy", ["Charge", "Momentum", "Mass"], "The induced current opposes the change that makes it."),
    ("The stopping potential in the photoelectric effect depends on:", "Frequency of light", ["Intensity of light", "Area of the plate",
     "Time of exposure"], "eV0 = hf - φ; intensity changes the current, not V0."),
    ("A p-n junction diode in forward bias has:", "A thin depletion layer and low resistance", ["A wide depletion layer",
     "Infinite resistance", "No current"], "Forward bias pushes carriers across the junction."),
    ("Which colour of light bends the most in a glass prism?", "Violet", ["Red", "Yellow", "Green"], "Refractive index is highest for violet (shortest λ)."),
    ("The power factor of a pure inductor circuit is:", "0", ["1", "0.5", "√2"], "Current lags voltage by 90°, so cos 90° = 0."),
    ("Nuclear binding energy per nucleon is highest near:", "Iron-56", ["Uranium-235", "Hydrogen-1", "Helium-4"],
     "This is why fusion of light and fission of heavy nuclei both release energy."),
    ("Bernoulli's principle is a statement of conservation of:", "Energy", ["Mass", "Momentum", "Charge"],
     "P + ½ρv² + ρgh is constant along a streamline."),
    ("The speed of sound in a gas is proportional to:", "√T (absolute temperature)", ["T", "1/T", "T²"],
     "v = √(γRT/M)."),
    ("Which of these is NOT an electromagnetic wave?", "Sound", ["X-rays", "Radio waves", "Gamma rays"], "Sound is a mechanical wave."),
    ("The unit of self-inductance is the:", "Henry", ["Weber", "Tesla", "Farad"], "1 H = 1 V s / A."),
    ("de Broglie wavelength of a particle is:", "h / p", ["p / h", "hc / E", "h p"], "λ = h/(mv)."),
    ("Kirchhoff's current law is based on conservation of:", "Charge", ["Energy", "Momentum", "Mass"],
     "The current into a junction equals the current out."),
])
