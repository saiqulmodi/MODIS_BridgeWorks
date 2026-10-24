"""IIT level - Physics (JEE Advanced standard): multi-step problems on projectiles on inclines,
constrained and frictional motion, circular motion, variable mass, centre of mass, rolling with
slipping, collisions with restitution, orbital energy, physical pendulums, fluid flow, heat
conduction, thermodynamic processes, fields of extended charges, dielectrics, transient circuits,
magnetic moments, LC oscillations, refraction by curved surfaces, wave optics, X-rays and nuclei.
g = 10 m/s² unless stated."""
import math

from . import mcq


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def _o(r, *alts):
    out = []
    for x in (r, *alts, r * 2, r + 1, r * 3, r + 10):
        x = _c(x)
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _f(x):
    return f"{x:,}" if isinstance(x, int) else f"{x:g}"


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    r = _c(r)
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [_f(x) + u_en for x in o], 0, ex_en, q_bn, [_f(x) + ub for x in o], ex_bn)


SIN = {30: 0.5, 37: 0.6, 45: 0.7071, 53: 0.8, 60: 0.866, 90: 1.0}
COS = {30: 0.866, 37: 0.8, 45: 0.7071, 53: 0.6, 60: 0.5}


# ---------------------------------------------------------------- mechanics
def incline_max_range(u, beta):
    r = u * u / (10 * (1 + SIN[beta]))
    return _n(f"A ball is projected at {u} m/s from the foot of a fixed incline of {beta}°. What is the maximum range it can have up the incline? (g = 10 m/s²)",
              f"{beta}° নতির একটা স্থির নত তলের পাদদেশ থেকে {u} m/s বেগে একটা বল ছোড়া হল। নত তল বরাবর উপরে এর সর্বোচ্চ পাল্লা কত হতে পারে? (g = 10 m/s²)", r,
              f"R_max (up the incline) = u² ÷ [g(1 + sin β)] = {u}² ÷ [10 x (1 + {SIN[beta]:g})] = {_f(_c(r))} m, at θ = 45° + β/2 from the horizontal.",
              f"নত তল বরাবর সর্বোচ্চ পাল্লা = u² ÷ [g(1 + sin β)] = {u}² ÷ [10 x (1 + {SIN[beta]:g})] = {_f(_c(r))} m, অনুভূমিক থেকে θ = 45° + β/2 কোণে।",
              (u * u / 10, u * u / (10 * (1 - SIN[beta])), r / 2), " m")


def table_hang(m1, m2, mu):
    a = (m2 - mu * m1) * 10 / (m1 + m2)
    return _n(f"A {m1} kg block on a horizontal table (friction coefficient {mu}) is tied over a light pulley to a hanging {m2} kg block. What is the acceleration? (g = 10 m/s²)",
              f"অনুভূমিক টেবিলে {m1} kg-এর একটা ব্লক (ঘর্ষণাঙ্ক {mu}) হালকা কপিকলের উপর দিয়ে ঝুলন্ত {m2} kg ব্লকের সঙ্গে বাঁধা। ত্বরণ কত? (g = 10 m/s²)", a,
              f"a = (m₂g - μm₁g) ÷ (m₁ + m₂) = ({m2 * 10} - {_f(_c(mu * m1 * 10))}) ÷ {m1 + m2} = {_f(_c(a))} m/s².",
              f"ত্বরণ = (m₂g - μm₁g) ÷ (m₁ + m₂) = ({m2 * 10} - {_f(_c(mu * m1 * 10))}) ÷ {m1 + m2} = {_f(_c(a))} m/s²।",
              (m2 * 10 / (m1 + m2), (m2 + mu * m1) * 10 / (m1 + m2), a * 2), " m/s²")


def two_block(m_top, m_bot, mu):
    f = mu * 10 * (m_top + m_bot)
    return _n(f"A {m_top} kg block rests on a {m_bot} kg plank on a frictionless floor; the friction coefficient between them is {mu}. What is the largest horizontal force on the PLANK for which they move together? (g = 10 m/s²)",
              f"ঘর্ষণহীন মেঝেতে {m_bot} kg-এর একটা তক্তার উপর {m_top} kg-এর একটা ব্লক; তাদের মধ্যে ঘর্ষণাঙ্ক {mu}। তক্তার উপর সর্বোচ্চ কত অনুভূমিক বলে দুটো একসঙ্গে চলবে? (g = 10 m/s²)", f,
              f"Friction can give the top block at most a = μg = {_f(_c(mu * 10))} m/s²; F = (m₁ + m₂) μg = {m_top + m_bot} x {_f(_c(mu * 10))} = {_f(_c(f))} N.",
              f"ঘর্ষণ উপরের ব্লককে সর্বোচ্চ a = μg = {_f(_c(mu * 10))} m/s² দিতে পারে; F = (m₁ + m₂) μg = {m_top + m_bot} x {_f(_c(mu * 10))} = {_f(_c(f))} N।",
              (mu * 10 * m_top, mu * 10 * m_bot, f / 2), " N")


def loop_speed(r):
    v = math.sqrt(5 * 10 * r)
    return _n(f"A bob on a string of length {r:g} m must just complete a vertical circle. What is the minimum speed needed at the lowest point? (g = 10 m/s²)",
              f"{r:g} m লম্বা সুতোয় বাঁধা একটা ববকে কোনোমতে একটা উল্লম্ব বৃত্ত সম্পূর্ণ করতে হবে। সর্বনিম্ন বিন্দুতে ন্যূনতম কত বেগ লাগবে? (g = 10 m/s²)", v,
              f"At the top tension can be zero, so v_top = √(gR); energy then gives v_bottom = √(5gR) = √(50 x {r:g}) = {_f(_c(v))} m/s.",
              f"শীর্ষে টান শূন্য হতে পারে, তাই v_শীর্ষ = √(gR); শক্তি-সংরক্ষণে v_নিম্ন = √(5gR) = √(50 x {r:g}) = {_f(_c(v))} m/s।",
              (math.sqrt(10 * r), math.sqrt(20 * r), math.sqrt(40 * r)), " m/s")


def loop_tension(m):
    t = 6 * m * 10
    return _n(f"A {m:g} kg bob just completes a vertical circle on a string. What is the string tension at the lowest point? (g = 10 m/s²)",
              f"{m:g} kg-এর একটা বব সুতোয় কোনোমতে উল্লম্ব বৃত্ত সম্পূর্ণ করে। সর্বনিম্ন বিন্দুতে সুতোর টান কত? (g = 10 m/s²)", t,
              f"T = mg + mv²/R with v² = 5gR, so T = 6mg = 6 x {m:g} x 10 = {_f(_c(t))} N - independent of the radius.",
              f"T = mg + mv²/R, যেখানে v² = 5gR, তাই T = 6mg = 6 x {m:g} x 10 = {_f(_c(t))} N - ব্যাসার্ধের উপর নির্ভর করে না।",
              (m * 10, 5 * m * 10, 2 * m * 10), " N")


def rocket(m, u, rate):
    a = (u * rate - m * 10) / m
    return _n(f"A {m:,} kg rocket ejects gas at {rate} kg/s with exhaust speed {u:,} m/s relative to it. What is its initial upward acceleration? (g = 10 m/s²)",
              f"{m:,} kg-এর একটা রকেট নিজের সাপেক্ষে {u:,} m/s বেগে সেকেন্ডে {rate} kg গ্যাস ছোড়ে। এর প্রাথমিক ঊর্ধ্বমুখী ত্বরণ কত? (g = 10 m/s²)", a,
              f"Thrust = u dm/dt = {u * rate:,} N; a = (thrust - mg) ÷ m = ({u * rate:,} - {m * 10:,}) ÷ {m:,} = {_f(_c(a))} m/s².",
              f"ধাক্কা = u dm/dt = {u * rate:,} N; ত্বরণ = (ধাক্কা - mg) ÷ m = ({u * rate:,} - {m * 10:,}) ÷ {m:,} = {_f(_c(a))} m/s²।",
              (u * rate / m, a + 10, a * 2), " m/s²")


def disc_hole(r):
    x = r / 6
    return _n(f"From a uniform disc of radius {r} cm, a circular hole of radius {r / 2:g} cm is cut so that it touches the rim. How far does the centre of mass move from the disc's centre?",
              f"{r} cm ব্যাসার্ধের একটা সুষম চাকতি থেকে {r / 2:g} cm ব্যাসার্ধের একটা বৃত্তাকার ছিদ্র এমনভাবে কাটা হল যে তা কিনারা ছোঁয়। ভরকেন্দ্র চাকতির কেন্দ্র থেকে কত সরে?", x,
              f"The hole has 1/4 of the mass at distance R/2: x = (1/4 x R/2) ÷ (1 - 1/4) = R/6 = {_f(_c(x))} cm, away from the hole.",
              f"ছিদ্রের ভর মোটের 1/4, দূরত্ব R/2: x = (1/4 x R/2) ÷ (1 - 1/4) = R/6 = {_f(_c(x))} cm, ছিদ্রের উল্টো দিকে।",
              (r / 4, r / 8, r / 2), " cm")


def skid_to_roll(v0, mu):
    t = 2 * v0 / (7 * mu * 10)
    return _n(f"A solid ball is launched sliding (not spinning) at {v0} m/s on a floor with friction coefficient {mu}. After how long does it start rolling without slipping? (g = 10 m/s²)",
              f"{mu} ঘর্ষণাঙ্কের মেঝেতে একটা নিরেট বল {v0} m/s বেগে পিছলে (না ঘুরে) ছাড়া হল। কত সময় পরে এটা না পিছলে গড়াতে শুরু করে? (g = 10 m/s²)", t,
              f"Friction slows v (a = μg) and spins it up (α = 5μg/2R); v = ωR when t = 2v₀ ÷ 7μg = {_f(_c(t))} s, when v = 5v₀/7.",
              f"ঘর্ষণ বেগ কমায় (a = μg) আর ঘোরায় (α = 5μg/2R); t = 2v₀ ÷ 7μg = {_f(_c(t))} s-এ v = ωR হয়, তখন v = 5v₀/7।",
              (v0 / (mu * 10), 2 * v0 / (5 * mu * 10), t * 2), " s")


def restitution(m1, m2, u, e):
    v2 = (1 + e) * m1 * u / (m1 + m2)
    return _n(f"A {m1} kg ball at {u} m/s hits a stationary {m2} kg ball head-on with coefficient of restitution {e}. What is the speed of the second ball after impact?",
              f"{u} m/s বেগের {m1} kg-এর একটা বল স্থির {m2} kg-এর বলকে মুখোমুখি ধাক্কা দেয়, প্রত্যাবর্তন-গুণাঙ্ক {e}। ধাক্কার পরে দ্বিতীয় বলের বেগ কত?", v2,
              f"Momentum and e = (v₂ - v₁)/u give v₂ = (1 + e)m₁u ÷ (m₁ + m₂) = {_f(_c(v2))} m/s.",
              f"ভরবেগ সংরক্ষণ আর e = (v₂ - v₁)/u থেকে v₂ = (1 + e)m₁u ÷ (m₁ + m₂) = {_f(_c(v2))} m/s।",
              (m1 * u / (m1 + m2), 2 * m1 * u / (m1 + m2), u), " m/s")


def rod_alpha(l):
    a = 3 * 10 / (2 * l)
    return _n(f"A uniform rod {l:g} m long is pivoted at one end and released from rest in a horizontal position. What is its initial angular acceleration? (g = 10 m/s²)",
              f"{l:g} m লম্বা একটা সুষম দণ্ড এক প্রান্তে কব্জাযুক্ত, অনুভূমিক অবস্থা থেকে স্থির ছাড়া হল। এর প্রাথমিক কৌণিক ত্বরণ কত? (g = 10 m/s²)", a,
              f"τ = mgL/2, I = mL²/3, so α = 3g ÷ 2L = 30 ÷ {_f(_c(2 * l))} = {_f(_c(a))} rad/s².",
              f"টর্ক = mgL/2, I = mL²/3, তাই α = 3g ÷ 2L = 30 ÷ {_f(_c(2 * l))} = {_f(_c(a))} rad/s²।",
              (10 / l, 3 * 10 / l, 10 / (2 * l)), " rad/s²", " রেডিয়ান/s²")


def phys_pendulum(l):
    t = 2 * math.pi * math.sqrt(2 * l / (3 * 10))
    return _n(f"A uniform rod {l:g} m long swings about a horizontal axis through one end. What is its period for small oscillations? (g = 10 m/s²)",
              f"{l:g} m লম্বা একটা সুষম দণ্ড এক প্রান্ত দিয়ে যাওয়া অনুভূমিক অক্ষে দোলে। ছোট দোলনে এর পর্যায়কাল কত? (g = 10 m/s²)", t,
              f"T = 2π√(I ÷ mgd) with I = mL²/3, d = L/2: T = 2π√(2L/3g) = {_f(_c(t))} s.",
              f"পর্যায়কাল T = 2π√(I ÷ mgd), I = mL²/3, d = L/2: T = 2π√(2L/3g) = {_f(_c(t))} s।",
              (2 * math.pi * math.sqrt(l / 10), 2 * math.pi * math.sqrt(l / 20), t * 2), " s")


def orbit_raise(m, r_km):
    e = m * 10 * r_km * 1000 / 4 / 1e9
    return _n(f"A {m:,} kg satellite orbits just above a planet of radius {r_km:,} km (surface g = 10 m/s²). How much energy is needed to move it to an orbit at height equal to the planet's radius?",
              f"{r_km:,} km ব্যাসার্ধের একটা গ্রহের (পৃষ্ঠে g = 10 m/s²) ঠিক উপরে {m:,} kg-এর একটা উপগ্রহ ঘোরে। গ্রহের ব্যাসার্ধের সমান উচ্চতার কক্ষপথে নিতে কত শক্তি লাগে?", e,
              f"E = -GMm/2r; from r = R to 2R: ΔE = GMm/4R = mgR/4 = {m:,} x 10 x {r_km * 1000:,} ÷ 4 J = {_f(_c(e))} x 10⁹ J.",
              f"শক্তি E = -GMm/2r; r = R থেকে 2R: ΔE = GMm/4R = mgR/4 = {m:,} x 10 x {r_km * 1000:,} ÷ 4 J = {_f(_c(e))} x 10⁹ J।",
              (e * 2, e * 4, e / 2), " x 10⁹ J")


def torricelli(h, H):
    x = 2 * math.sqrt(h * (H - h))
    return _n(f"Water stands {H} m deep in an open tank. A small hole is made {h} m below the surface. How far from the tank's base does the jet hit the ground?",
              f"একটা খোলা ট্যাঙ্কে {H} m গভীর জল। জলতলের {h} m নিচে একটা ছোট ছিদ্র করা হল। জলধারা ট্যাঙ্কের তলা থেকে কত দূরে মাটিতে পড়ে?", x,
              f"v = √(2gh), fall height H - h, so range = 2√(h(H - h)) = 2√({h} x {H - h}) = {_f(_c(x))} m.",
              f"বেগ = √(2gh), পতনের উচ্চতা H - h, তাই পাল্লা = 2√(h(H - h)) = 2√({h} x {H - h}) = {_f(_c(x))} m।",
              (math.sqrt(h * (H - h)), H, x / 2), " m")


def bubble(t, r_mm):
    p = 4 * t / (r_mm / 1000)
    return _n(f"A soap bubble of radius {r_mm} mm has surface tension {t} N/m. What is the excess pressure inside it?",
              f"{r_mm} mm ব্যাসার্ধের একটা সাবানের বুদবুদের পৃষ্ঠটান {t} N/m। এর ভেতরে বাড়তি চাপ কত?", p,
              f"A bubble has two surfaces: ΔP = 4T/r = 4 x {t} ÷ {r_mm / 1000:g} = {_f(_c(p))} Pa (a liquid drop has 2T/r).",
              f"বুদবুদের দুটো তল: বাড়তি চাপ = 4T/r = 4 x {t} ÷ {r_mm / 1000:g} = {_f(_c(p))} Pa (তরলের ফোঁটায় 2T/r)।",
              (p / 2, p / 4, p * 2), " Pa")


def wire_energy(f, dl_mm):
    u = 0.5 * f * dl_mm / 1000
    return _n(f"A wire stretched elastically by {dl_mm} mm carries a final load of {f} N. How much elastic energy is stored in it?",
              f"একটা তার {dl_mm} mm স্থিতিস্থাপকভাবে লম্বা হয়ে শেষে {f} N বোঝা বয়। এতে কত স্থিতিস্থাপক শক্তি জমা থাকে?", u,
              f"U = ½ F ΔL = ½ x {f} x {dl_mm / 1000:g} = {_f(_c(u))} J (the force grows from 0 to F).",
              f"শক্তি = ½ F ΔL = ½ x {f} x {dl_mm / 1000:g} = {_f(_c(u))} J (বল 0 থেকে F পর্যন্ত বাড়ে)।",
              (f * dl_mm / 1000, u / 2, u * 4), " J")


def banking_friction(r, mu):
    v = math.sqrt(r * 10 * (mu + 0.75) / (1 - mu * 0.75))
    return _n(f"A road of radius {r} m is banked at 37° (tan 37° = 0.75) and the friction coefficient is {mu}. What is the maximum safe speed? (g = 10 m/s²)",
              f"{r} m ব্যাসার্ধের একটা রাস্তা 37° ঢালু (tan 37° = 0.75), ঘর্ষণাঙ্ক {mu}। সর্বোচ্চ নিরাপদ বেগ কত? (g = 10 m/s²)", v,
              f"v²_max = rg(μ + tan θ) ÷ (1 - μ tan θ) = {r} x 10 x {_f(_c(mu + 0.75))} ÷ {_f(_c(1 - mu * 0.75))}, v = {_f(_c(v))} m/s.",
              f"সর্বোচ্চ বেগ² = rg(μ + tan θ) ÷ (1 - μ tan θ) = {r} x 10 x {_f(_c(mu + 0.75))} ÷ {_f(_c(1 - mu * 0.75))}, বেগ = {_f(_c(v))} m/s।",
              (math.sqrt(r * 10 * 0.75), math.sqrt(r * 10 * mu), v * 1.3), " m/s")


def rain_angle(v_rain, v_man):
    a = math.degrees(math.atan(v_man / v_rain))
    return _n(f"Rain falls vertically at {v_rain} m/s. A cyclist rides at {v_man} m/s. At what angle from the vertical should the cyclist hold an umbrella?",
              f"বৃষ্টি উল্লম্বভাবে {v_rain} m/s বেগে পড়ছে। একজন সাইকেল-আরোহী {v_man} m/s বেগে চলেন। ছাতা উল্লম্বের সঙ্গে কত কোণে ধরা উচিত?", a,
              f"Rain relative to the rider has components {v_man} (towards him) and {v_rain} (down): tan θ = {v_man}/{v_rain}, θ = {_f(_c(a))}°, tilted forward.",
              f"আরোহীর সাপেক্ষে বৃষ্টির উপাংশ {v_man} (তাঁর দিকে) আর {v_rain} (নিচে): tan θ = {v_man}/{v_rain}, θ = {_f(_c(a))}°, সামনের দিকে হেলানো।",
              (90 - a, a / 2, a + 15), "°")


# ---------------------------------------------------------------- heat and thermodynamics
def junction(k1, t1, k2, t2):
    t = (k1 * t1 + k2 * t2) / (k1 + k2)
    return _n(f"Two rods of equal length and cross-section, with conductivities {k1} and {k2} W/(m K), are joined end to end. The free ends are at {t1}°C and {t2}°C. What is the steady junction temperature?",
              f"সমান দৈর্ঘ্য আর প্রস্থচ্ছেদের দুটো দণ্ড, পরিবাহিতা {k1} আর {k2} W/(m K), প্রান্তে প্রান্তে জোড়া। মুক্ত প্রান্ত দুটো {t1}°C আর {t2}°C-এ। স্থিত অবস্থায় সংযোগের তাপমাত্রা কত?", t,
              f"Equal heat currents: k₁(T₁ - T) = k₂(T - T₂), so T = (k₁T₁ + k₂T₂) ÷ (k₁ + k₂) = {_f(_c(t))}°C.",
              f"সমান তাপ-প্রবাহ: k₁(T₁ - T) = k₂(T - T₂), তাই T = (k₁T₁ + k₂T₂) ÷ (k₁ + k₂) = {_f(_c(t))}°C।",
              ((t1 + t2) / 2, (k2 * t1 + k1 * t2) / (k1 + k2), t + 10), "°C")


def adiabatic_t(t1, ratio):
    t2 = t1 * ratio ** (2 / 3)
    return _n(f"A monatomic ideal gas at {t1} K is compressed adiabatically to 1/{ratio} of its volume. What is its final temperature?",
              f"{t1} K-এর একটা এক-পারমাণবিক আদর্শ গ্যাসকে রুদ্ধতাপে আয়তনের 1/{ratio} অংশে সংকুচিত করা হল। শেষ তাপমাত্রা কত?", t2,
              f"TV^(γ - 1) is constant with γ = 5/3: T₂ = {t1} x {ratio}^(2/3) = {_f(_c(t2))} K.",
              f"TV^(γ - 1) ধ্রুবক, γ = 5/3: শেষ তাপমাত্রা = {t1} x {ratio}^(2/3) = {_f(_c(t2))} K।",
              (t1 * ratio, t1 * ratio ** 0.4, t1), " K")


def cop_fridge(t_in, t_out):
    c = (t_in + 273) / (t_out - t_in)
    return _n(f"An ideal refrigerator keeps its inside at {t_in}°C in a room at {t_out}°C. What is its coefficient of performance?",
              f"একটা আদর্শ রেফ্রিজারেটর {t_out}°C ঘরে ভেতরটা {t_in}°C-এ রাখে। এর কার্যকারিতা-সহগ কত?", c,
              f"COP = T_cold ÷ (T_hot - T_cold) = {t_in + 273} ÷ {t_out - t_in} = {_f(_c(c))} (temperatures in kelvin).",
              f"কার্যকারিতা-সহগ = T_শীতল ÷ (T_উষ্ণ - T_শীতল) = {t_in + 273} ÷ {t_out - t_in} = {_f(_c(c))} (কেলভিনে তাপমাত্রা)।",
              ((t_out + 273) / (t_out - t_in), 1 - (t_in + 273) / (t_out + 273), c / 2))


def isothermal_w(n, t, ratio):
    w = n * 8.314 * t * math.log(ratio) / 1000
    return _n(f"{n} mol of an ideal gas expands isothermally at {t} K to {ratio} times its volume. How much work does it do? (R = 8.314 J/(mol K))",
              f"{n} মোল আদর্শ গ্যাস {t} K-এ সমোষ্ণভাবে আয়তনের {ratio} গুণে প্রসারিত হয়। এটা কত কাজ করে? (R = 8.314 J/(mol K))", w,
              f"W = nRT ln(V₂/V₁) = {n} x 8.314 x {t} x ln {ratio} = {_f(_c(w))} kJ; the same heat is absorbed.",
              f"কাজ = nRT ln(V₂/V₁) = {n} x 8.314 x {t} x ln {ratio} = {_f(_c(w))} kJ; একই পরিমাণ তাপ শোষিত হয়।",
              (n * 8.314 * t * ratio / 1000, n * 8.314 * t / 1000, w * 2), " kJ")


def cooling(t1, t2, room, minutes, t3):
    k = math.log((t1 - room) / (t2 - room)) / minutes
    t = math.log((t2 - room) / (t3 - room)) / k
    return _n(f"Tea cools from {t1}°C to {t2}°C in {minutes} minutes in a {room}°C room. Using Newton's law of cooling, how long does it take to cool further from {t2}°C to {t3}°C?",
              f"{room}°C ঘরে চা {minutes} মিনিটে {t1}°C থেকে {t2}°C-এ ঠান্ডা হয়। নিউটনের শীতলীকরণ সূত্রে {t2}°C থেকে {t3}°C-এ আরও ঠান্ডা হতে কত সময় লাগে?", t,
              f"(T - T₀) falls exponentially: k = ln({t1 - room}/{t2 - room}) ÷ {minutes}; t = ln({t2 - room}/{t3 - room}) ÷ k = {_f(_c(t))} min.",
              f"(T - T₀) সূচকীয়ভাবে কমে: k = ln({t1 - room}/{t2 - room}) ÷ {minutes}; সময় = ln({t2 - room}/{t3 - room}) ÷ k = {_f(_c(t))} মিনিট।",
              (minutes, minutes * (t2 - t3) / (t1 - t2), t * 1.5), " min", " মিনিট")


# ---------------------------------------------------------------- waves
def doppler_both(f, vs, vo):
    r = f * (340 + vo) / (340 - vs)
    return _n(f"A car horn of {f} Hz moves at {vs} m/s towards a cyclist who rides towards the car at {vo} m/s. What frequency does the cyclist hear? (speed of sound 340 m/s)",
              f"{f} Hz-এর একটা গাড়ির হর্ন {vs} m/s বেগে একজন সাইকেল-আরোহীর দিকে আসছে, যিনি গাড়ির দিকে {vo} m/s বেগে যাচ্ছেন। আরোহী কোন কম্পাঙ্ক শোনেন? (শব্দের বেগ 340 m/s)", r,
              f"f' = f (v + v_o) ÷ (v - v_s) = {f} x {340 + vo} ÷ {340 - vs} = {_f(_c(r))} Hz.",
              f"শ্রুত কম্পাঙ্ক = f (v + v_o) ÷ (v - v_s) = {f} x {340 + vo} ÷ {340 - vs} = {_f(_c(r))} Hz।",
              (f * (340 - vo) / (340 + vs), f * 340 / (340 - vs), f), " Hz")


def resonance_tube(f, l1, l2):
    v = 2 * f * (l2 - l1) / 100
    return _n(f"With a {f} Hz tuning fork, a resonance tube gives the first resonance at {l1} cm and the second at {l2} cm. What is the speed of sound?",
              f"{f} Hz স্বরশলাকা দিয়ে একটা অনুনাদ-নলে প্রথম অনুনাদ {l1} cm-এ আর দ্বিতীয়টা {l2} cm-এ। শব্দের বেগ কত?", v,
              f"Successive resonances are λ/2 apart, so the end correction cancels: v = 2f(l₂ - l₁) = 2 x {f} x {(l2 - l1) / 100:g} = {_f(_c(v))} m/s.",
              f"পরপর অনুনাদ λ/2 দূরে, তাই প্রান্ত-সংশোধন বাদ যায়: v = 2f(l₂ - l₁) = 2 x {f} x {(l2 - l1) / 100:g} = {_f(_c(v))} m/s।",
              (4 * f * l1 / 100, f * (l2 - l1) / 100, 4 * f * l2 / 100), " m/s")


# ---------------------------------------------------------------- electricity and magnetism
def field_inside(q, r_big, r):
    e = 9e9 * q * 1e-6 * r / r_big ** 3
    return _n(f"A non-conducting sphere of radius {r_big} m carries {q} μC spread uniformly through its volume. What is the field {r} m from its centre?",
              f"{r_big} m ব্যাসার্ধের একটা অপরিবাহী গোলকের আয়তনজুড়ে সুষমভাবে {q} μC আধান ছড়ানো। এর কেন্দ্র থেকে {r} m দূরে তড়িৎক্ষেত্র কত?", e,
              f"Inside, only the enclosed charge counts: E = kQr ÷ R³ = 9 x 10⁹ x {q} x 10⁻⁶ x {r} ÷ {r_big}³ = {_f(_c(e))} N/C.",
              f"ভেতরে কেবল আবদ্ধ আধান গোনা হয়: E = kQr ÷ R³ = 9 x 10⁹ x {q} x 10⁻⁶ x {r} ÷ {r_big}³ = {_f(_c(e))} N/C।",
              (9e9 * q * 1e-6 / r ** 2, 9e9 * q * 1e-6 / r_big ** 2, e * 2), " N/C")


def centre_potential(q, r):
    v = 1.5 * 9e9 * q * 1e-6 / r
    return _n(f"A uniformly charged solid (non-conducting) sphere of radius {r} m holds {q} μC. What is the potential at its centre?",
              f"{r} m ব্যাসার্ধের একটা সুষম আহিত নিরেট (অপরিবাহী) গোলকে {q} μC আধান। এর কেন্দ্রে বিভব কত?", v,
              f"V_centre = 3kQ ÷ 2R = 1.5 x 9 x 10⁹ x {q} x 10⁻⁶ ÷ {r} = {_f(_c(v))} V, 1.5 times the surface value.",
              f"কেন্দ্রে বিভব = 3kQ ÷ 2R = 1.5 x 9 x 10⁹ x {q} x 10⁻⁶ ÷ {r} = {_f(_c(v))} V, পৃষ্ঠের মানের 1.5 গুণ।",
              (v / 1.5, v * 2, 0.5 * v), " V")


def slab_cap(a, d_mm, t_mm, k):
    c = 8.85 * a / (d_mm - t_mm + t_mm / k)
    return _n(f"A parallel-plate capacitor (plate area {a} m², gap {d_mm} mm) has a dielectric slab {t_mm} mm thick with K = {k} inserted. What is its capacitance? (ε₀ = 8.85 x 10⁻¹² F/m)",
              f"একটা সমান্তরাল-পাত ধারকে (পাতের ক্ষেত্রফল {a} m², ফাঁক {d_mm} mm) K = {k}-এর {t_mm} mm পুরু একটা পরাবৈদ্যুতিক পাত ঢোকানো হল। এর ধারকত্ব কত? (ε₀ = 8.85 x 10⁻¹² F/m)", c,
              f"C = ε₀A ÷ (d - t + t/K) = 8.85 x 10⁻¹² x {a} ÷ ({d_mm} - {t_mm} + {t_mm}/{k}) mm = {_f(_c(c))} nF.",
              f"ধারকত্ব = ε₀A ÷ (d - t + t/K) = 8.85 x 10⁻¹² x {a} ÷ ({d_mm} - {t_mm} + {t_mm}/{k}) mm = {_f(_c(c))} nF।",
              (8.85 * a / d_mm, 8.85 * a * k / d_mm, c / 2), " nF")


def share_loss(c1, v1, c2, v2):
    u = c1 * c2 * (v1 - v2) ** 2 / (2 * (c1 + c2)) / 1000
    return _n(f"A {c1} μF capacitor at {v1} V is connected (like plates together) to a {c2} μF capacitor at {v2} V. How much energy is lost in the connecting wires?",
              f"{v1} V-এর একটা {c1} μF ধারককে {v2} V-এর একটা {c2} μF ধারকের সঙ্গে (সমধর্মী পাত একসঙ্গে) যুক্ত করা হল। সংযোগকারী তারে কত শক্তি হারায়?", u,
              f"ΔU = C₁C₂(V₁ - V₂)² ÷ 2(C₁ + C₂) = {c1} x {c2} x {v1 - v2}² ÷ (2 x {c1 + c2}) μJ = {_f(_c(u))} mJ - lost as heat and radiation, whatever the resistance.",
              f"শক্তিক্ষয় = C₁C₂(V₁ - V₂)² ÷ 2(C₁ + C₂) = {c1} x {c2} x {v1 - v2}² ÷ (2 x {c1 + c2}) μJ = {_f(_c(u))} mJ - রোধ যাই হোক, তাপ আর বিকিরণে হারায়।",
              (u * 2, (c1 * v1 * v1 + c2 * v2 * v2) / 2000, u / 2), " mJ")


def rc_half(r_k, c_u):
    t = r_k * 1000 * c_u * 1e-6 * math.log(2)
    return _n(f"A {c_u} μF capacitor charges through a {r_k} kΩ resistor from a battery. How long until its charge reaches half the final value?",
              f"একটা {c_u} μF ধারক একটা ব্যাটারি থেকে {r_k} kΩ রোধের মধ্য দিয়ে আহিত হয়। চূড়ান্ত আধানের অর্ধেক হতে কত সময় লাগে?", t,
              f"q = Q(1 - e^(-t/RC)) = Q/2 when t = RC ln 2 = {_f(_c(r_k * c_u / 1000))} x 0.693 = {_f(_c(t))} s.",
              f"q = Q(1 - e^(-t/RC)) = Q/2 হয় যখন t = RC ln 2 = {_f(_c(r_k * c_u / 1000))} x 0.693 = {_f(_c(t))} s।",
              (r_k * c_u / 1000, t * 2, r_k * c_u / 2000), " s")


def lr_current(e, r, l):
    i = e / r * (1 - math.exp(-1))
    return _n(f"A {l:g} H inductor and a {r} Ω resistor are connected in series to a {e} V battery. What is the current one time constant ({_f(_c(l / r))} s) after closing the switch?",
              f"একটা {l:g} H আবেশক আর {r} Ω রোধ শ্রেণিতে একটা {e} V ব্যাটারির সঙ্গে যুক্ত। সুইচ বন্ধের এক সময়-ধ্রুবক ({_f(_c(l / r))} s) পরে প্রবাহ কত?", i,
              f"I = (E/R)(1 - e⁻¹) = {_f(_c(e / r))} x 0.632 = {_f(_c(i))} A.",
              f"প্রবাহ = (E/R)(1 - e⁻¹) = {_f(_c(e / r))} x 0.632 = {_f(_c(i))} A।",
              (e / r, e / r * 0.368, e / r / 2), " A")


def lc_freq(l_mh, c_uf):
    f = 1 / (2 * math.pi * math.sqrt(l_mh * 1e-3 * c_uf * 1e-6))
    return _n(f"What is the natural frequency of an LC circuit with L = {l_mh} mH and C = {c_uf} μF?",
              f"L = {l_mh} mH আর C = {c_uf} μF-এর একটা LC বর্তনীর স্বাভাবিক কম্পাঙ্ক কত?", f,
              f"f = 1 ÷ 2π√(LC) = 1 ÷ (2π√({l_mh} x 10⁻³ x {c_uf} x 10⁻⁶)) = {_f(_c(f))} Hz; energy swaps between C and L.",
              f"কম্পাঙ্ক = 1 ÷ 2π√(LC) = 1 ÷ (2π√({l_mh} x 10⁻³ x {c_uf} x 10⁻⁶)) = {_f(_c(f))} Hz; শক্তি C আর L-এর মধ্যে অদলবদল হয়।",
              (f * 2 * math.pi, f * 2, f / 2), " Hz")


def loop_b(n, i, r_cm):
    b = n * 4 * math.pi * 1e-7 * i / (2 * r_cm / 100) * 1e6
    return _n(f"A flat circular coil of {n} turns and radius {r_cm} cm carries {i} A. What is the magnetic field at its centre?",
              f"{r_cm} cm ব্যাসার্ধের {n} পাকের একটা চ্যাপ্টা বৃত্তাকার কুণ্ডলীতে {i} A প্রবাহ। এর কেন্দ্রে চৌম্বকক্ষেত্র কত?", b,
              f"B = Nμ₀I ÷ 2R = {n} x 4π x 10⁻⁷ x {i} ÷ (2 x {r_cm / 100:g}) T = {_f(_c(b))} μT.",
              f"চৌম্বকক্ষেত্র = Nμ₀I ÷ 2R = {n} x 4π x 10⁻⁷ x {i} ÷ (2 x {r_cm / 100:g}) T = {_f(_c(b))} μT।",
              (b / 2, b * 2, b / n), " μT")


def coil_torque(n, i, a_cm2, b, th):
    t = n * i * a_cm2 * 1e-4 * b * SIN[th]
    return _n(f"A {n}-turn coil of area {a_cm2} cm² carries {i} A in a {b:g} T field, its normal at {th}° to the field. What torque acts on it?",
              f"{a_cm2} cm² ক্ষেত্রফলের {n} পাকের একটা কুণ্ডলীতে {i} A প্রবাহ, {b:g} T ক্ষেত্রে তার অভিলম্ব ক্ষেত্রের সঙ্গে {th}° কোণে। এর উপর কত টর্ক কাজ করে?", t,
              f"τ = NIAB sin θ = {n} x {i} x {a_cm2} x 10⁻⁴ x {b:g} x {SIN[th]:g} = {_f(_c(t))} N m.",
              f"টর্ক = NIAB sin θ = {n} x {i} x {a_cm2} x 10⁻⁴ x {b:g} x {SIN[th]:g} = {_f(_c(t))} N m।",
              (n * i * a_cm2 * 1e-4 * b, t * 2, t / 2), " N m")


def ac_power(vr, ir, pf):
    p = vr * ir * pf
    return _n(f"An AC motor draws {ir} A (rms) from a {vr} V (rms) supply at a power factor of {pf}. What average power does it take?",
              f"একটা এসি মোটর {vr} V (আরএমএস) সরবরাহ থেকে {pf} ক্ষমতা-গুণকে {ir} A (আরএমএস) প্রবাহ নেয়। এটা গড়ে কত ক্ষমতা নেয়?", p,
              f"P = V_rms I_rms cos φ = {vr} x {ir} x {pf} = {_f(_c(p))} W.",
              f"ক্ষমতা = V_rms I_rms cos φ = {vr} x {ir} x {pf} = {_f(_c(p))} W।",
              (vr * ir, vr * ir * 2, p / 2), " W")


# ---------------------------------------------------------------- optics and modern physics
def lens_maker(n, r1, r2):
    inv = (n - 1) * (1 / r1 - 1 / r2)
    f = 1 / inv
    return _n(f"A thin lens of glass (n = {n}) has radii of curvature R₁ = +{r1} cm and R₂ = {r2} cm. What is its focal length?",
              f"কাচের (n = {n}) একটা পাতলা লেন্সের বক্রতা-ব্যাসার্ধ R₁ = +{r1} cm আর R₂ = {r2} cm। এর ফোকাস দূরত্ব কত?", f,
              f"Lens maker's formula: 1/f = (n - 1)(1/R₁ - 1/R₂) = {n - 1:g} x (1/{r1} - 1/({r2})), f = {_f(_c(f))} cm.",
              f"লেন্স-প্রস্তুতকারকের সূত্র: 1/f = (n - 1)(1/R₁ - 1/R₂) = {n - 1:g} x (1/{r1} - 1/({r2})), ফোকাস দূরত্ব = {_f(_c(f))} cm।",
              (abs(r1), abs(r1 * r2) / (abs(r1) + abs(r2)), f * 2), " cm")


def lens_in_water(f_air, n, nw_txt, nw):
    f = f_air * (n - 1) / (n / nw - 1)
    return _n(f"A glass lens (n = {n}) has a focal length of {f_air} cm in air. What is its focal length in water (n = {nw_txt})?",
              f"কাচের (n = {n}) একটা লেন্সের বাতাসে ফোকাস দূরত্ব {f_air} cm। জলে (n = {nw_txt}) এর ফোকাস দূরত্ব কত?", f,
              f"1/f ∝ (n_lens/n_medium - 1): f_water = {f_air} x {n - 1:g} ÷ {_f(_c(n / nw - 1))} = {_f(_c(f))} cm - about four times longer.",
              f"1/f ∝ (n_লেন্স/n_মাধ্যম - 1): জলে ফোকাস দূরত্ব = {f_air} x {n - 1:g} ÷ {_f(_c(n / nw - 1))} = {_f(_c(f))} cm - প্রায় চার গুণ।",
              (f_air, f_air * nw, f_air * n), " cm")


def fringe_shift(mu, t_um, lam_nm):
    n = (mu - 1) * t_um * 1000 / lam_nm
    return _n(f"In Young's experiment with light of {lam_nm} nm, a thin film of thickness {t_um:g} μm and refractive index {mu} covers one slit. By how many fringes does the pattern shift?",
              f"{lam_nm} nm আলো দিয়ে ইয়ংয়ের পরীক্ষায় একটা ছিদ্র {t_um:g} μm পুরু আর {mu} প্রতিসরাঙ্কের পাতলা পর্দায় ঢাকা হল। নকশা কয়টি ঝালর সরে যায়?", n,
              f"Extra path = (μ - 1)t; shift = (μ - 1)t ÷ λ = {mu - 1:g} x {t_um:g} x 1000 ÷ {lam_nm} = {_f(_c(n))} fringes, towards the covered slit.",
              f"বাড়তি পথ = (μ - 1)t; সরণ = (μ - 1)t ÷ λ = {mu - 1:g} x {t_um:g} x 1000 ÷ {lam_nm} = {_f(_c(n))}টি ঝালর, ঢাকা ছিদ্রের দিকে।",
              (mu * t_um * 1000 / lam_nm, n / 2, n + 2))


def single_slit(lam_nm, a_um, d_m):
    w = 2 * lam_nm * 1e-9 * d_m / (a_um * 1e-6) * 1000
    return _n(f"Light of {lam_nm} nm passes through a slit {a_um} μm wide onto a screen {d_m} m away. How wide is the central bright band?",
              f"{lam_nm} nm আলো {a_um} μm চওড়া একটা ছিদ্র দিয়ে {d_m} m দূরের পর্দায় পড়ে। মাঝের উজ্জ্বল পটি কত চওড়া?", w,
              f"Width = 2λD ÷ a = 2 x {lam_nm} x 10⁻⁹ x {d_m} ÷ ({a_um} x 10⁻⁶) m = {_f(_c(w))} mm.",
              f"প্রস্থ = 2λD ÷ a = 2 x {lam_nm} x 10⁻⁹ x {d_m} ÷ ({a_um} x 10⁻⁶) m = {_f(_c(w))} mm।",
              (w / 2, w * 2, w * 1.22), " mm")


def resolve(lam_nm, d_m):
    th = 1.22 * lam_nm * 1e-9 / d_m * 1e6
    return _n(f"What is the smallest angle a telescope of aperture {d_m:g} m can resolve at {lam_nm} nm?",
              f"{d_m:g} m অ্যাপারচারের একটা দূরবিন {lam_nm} nm-এ ন্যূনতম কত কোণ পৃথক করতে পারে?", th,
              f"θ = 1.22λ ÷ D = 1.22 x {lam_nm} x 10⁻⁹ ÷ {d_m:g} rad = {_f(_c(th))} μrad - bigger mirrors see finer detail.",
              f"কোণ = 1.22λ ÷ D = 1.22 x {lam_nm} x 10⁻⁹ ÷ {d_m:g} রেডিয়ান = {_f(_c(th))} মাইক্রো-রেডিয়ান - বড় দর্পণ সূক্ষ্মতর খুঁটিনাটি দেখে।",
              (th / 1.22, th * 2, th * 10), " μrad", " মাইক্রো-রেডিয়ান")


def planck(f1, v1, f2, v2):
    h = (v2 - v1) * 1.6e-19 / ((f2 - f1) * 1e14) * 1e34
    return _n(f"In a photoelectric experiment the stopping potential is {v1} V at {f1} x 10¹⁴ Hz and {v2} V at {f2} x 10¹⁴ Hz. What value of Planck's constant does this give?",
              f"একটা আলোক-তড়িৎ পরীক্ষায় {f1} x 10¹⁴ Hz-এ নিবৃত্তি বিভব {v1} V আর {f2} x 10¹⁴ Hz-এ {v2} V। এতে প্ল্যাঙ্কের ধ্রুবকের মান কত পাওয়া যায়?", h,
              f"eV = hf - φ, so h = e ΔV ÷ Δf = 1.6 x 10⁻¹⁹ x {_f(_c(v2 - v1))} ÷ ({f2 - f1} x 10¹⁴) = {_f(_c(h))} x 10⁻³⁴ J s.",
              f"eV = hf - φ, তাই h = e ΔV ÷ Δf = 1.6 x 10⁻¹⁹ x {_f(_c(v2 - v1))} ÷ ({f2 - f1} x 10¹⁴) = {_f(_c(h))} x 10⁻³⁴ J s।",
              (h * 2, h / 2, h + 1.5), " x 10⁻³⁴ J s")


def xray_cutoff(kv):
    lam = 1240 / (kv * 1000) * 1000
    return _n(f"An X-ray tube runs at {kv} kV. What is the shortest wavelength in its spectrum?",
              f"একটা এক্স-রে নল {kv} kV-এ চলে। এর বর্ণালির ক্ষুদ্রতম তরঙ্গদৈর্ঘ্য কত?", lam,
              f"An electron's full energy {kv} keV becomes one photon: λ_min = 1240 ÷ {kv * 1000:,} nm = {_f(_c(lam))} pm (Duane-Hunt law).",
              f"ইলেকট্রনের পুরো শক্তি {kv} keV একটা ফোটনে যায়: λ_ন্যূনতম = 1240 ÷ {kv * 1000:,} nm = {_f(_c(lam))} pm (ডুয়েন-হান্ট সূত্র)।",
              (lam * 2, lam / 2, lam * 10), " pm")


def activity(n_e20, t_half_days):
    lam = 0.693 / (t_half_days * 86400)
    a = lam * n_e20 * 1e20 / 1e14
    return _n(f"A sample holds {n_e20:g} x 10²⁰ radioactive nuclei with a half-life of {t_half_days} days. What is its activity?",
              f"একটা নমুনায় {t_half_days} দিন অর্ধায়ুর {n_e20:g} x 10²⁰টি তেজস্ক্রিয় নিউক্লিয়াস আছে। এর সক্রিয়তা কত?", a,
              f"A = λN = (0.693 ÷ {t_half_days * 86400:,} s) x {n_e20:g} x 10²⁰ = {_f(_c(a))} x 10¹⁴ Bq.",
              f"সক্রিয়তা = λN = (0.693 ÷ {t_half_days * 86400:,} s) x {n_e20:g} x 10²⁰ = {_f(_c(a))} x 10¹⁴ Bq।",
              (a * 24, a / 0.693, a * 2), " x 10¹⁴ Bq")


def screw_gauge(pitch, divs):
    lc = pitch / divs * 1000
    return _n(f"A screw gauge has a pitch of {pitch} mm and {divs} divisions on its circular scale. What is its least count?",
              f"একটা স্ক্রু-গজের পিচ {pitch} mm আর বৃত্তাকার স্কেলে {divs}টি ভাগ। এর লঘিষ্ঠ ধ্রুবক কত?", lc,
              f"Least count = pitch ÷ divisions = {pitch} ÷ {divs} mm = {_f(_c(lc))} μm.",
              f"লঘিষ্ঠ ধ্রুবক = পিচ ÷ ভাগসংখ্যা = {pitch} ÷ {divs} mm = {_f(_c(lc))} μm।",
              (lc * 10, lc / 2, pitch * 1000), " μm")


NUMERIC = [
    incline_max_range(20, 30), incline_max_range(30, 37), incline_max_range(40, 53),
    table_hang(4, 2, 0.2), table_hang(3, 3, 0.25), table_hang(6, 4, 0.1),
    two_block(2, 3, 0.4), two_block(1, 4, 0.3), two_block(5, 5, 0.2),
    loop_speed(0.8), loop_speed(2), loop_speed(1.25), loop_tension(0.5), loop_tension(2),
    rocket(5000, 2000, 50), rocket(2000, 1500, 20), rocket(10000, 2500, 60),
    disc_hole(12), disc_hole(30), skid_to_roll(7, 0.2), skid_to_roll(14, 0.1),
    restitution(2, 3, 10, 0.5), restitution(1, 1, 8, 0.75), restitution(3, 2, 5, 0.4),
    rod_alpha(1.5), rod_alpha(3), phys_pendulum(1.5), phys_pendulum(0.6),
    orbit_raise(1000, 6400), orbit_raise(500, 3200),
    torricelli(5, 20), torricelli(3, 12), torricelli(2, 10),
    bubble(0.03, 5), bubble(0.025, 2), wire_energy(200, 2), wire_energy(500, 1.5),
    banking_friction(90, 0.2), banking_friction(40, 0.25),
    rain_angle(12, 5), rain_angle(8, 6),
    junction(400, 100, 100, 0), junction(200, 80, 50, 20), junction(300, 150, 100, 30),
    adiabatic_t(300, 8), adiabatic_t(250, 27),
    cop_fridge(-3, 27), cop_fridge(4, 34),
    isothermal_w(2, 300, 3), isothermal_w(1, 400, 2),
    cooling(80, 60, 20, 10, 45), cooling(90, 70, 30, 6, 50),
    doppler_both(500, 20, 10), doppler_both(400, 30, 15),
    resonance_tube(512, 16, 49), resonance_tube(480, 17, 52),
    field_inside(4, 0.2, 0.1), field_inside(10, 0.5, 0.25),
    centre_potential(2, 0.3), centre_potential(5, 0.5),
    slab_cap(1, 4, 2, 4), slab_cap(2, 5, 3, 3),
    share_loss(2, 100, 3, 50), share_loss(4, 200, 1, 0),
    rc_half(100, 20), rc_half(50, 100),
    lr_current(12, 4, 2), lr_current(20, 10, 0.5),
    lc_freq(10, 100), lc_freq(4, 25),
    loop_b(100, 2, 10), loop_b(50, 5, 5),
    coil_torque(100, 2, 50, 0.4, 30), coil_torque(200, 1.5, 20, 0.5, 90),
    ac_power(230, 5, 0.8), ac_power(220, 10, 0.6),
    lens_maker(1.5, 20, -20), lens_maker(1.5, 10, -30), lens_maker(1.6, 15, -15),
    lens_in_water(20, 1.5, "4/3", 4 / 3), lens_in_water(15, 1.5, "4/3", 4 / 3),
    fringe_shift(1.5, 6, 600), fringe_shift(1.6, 5, 500),
    single_slit(600, 100, 2), single_slit(500, 50, 1.5),
    resolve(550, 2.4), resolve(500, 10),
    planck(5, 0.5, 10, 2.5), planck(4.5, 0.2, 7.5, 1.45),
    xray_cutoff(40), xray_cutoff(100),
    activity(1, 8), activity(5, 30),
    screw_gauge(0.5, 50), screw_gauge(0.5, 100),
    incline_max_range(25, 45), table_hang(5, 5, 0.3), two_block(3, 2, 0.5), loop_speed(3.2), loop_tension(1),
    rocket(1000, 1200, 15), disc_hole(18), skid_to_roll(21, 0.3), restitution(4, 1, 10, 0.6), rod_alpha(0.75),
    phys_pendulum(2.4), orbit_raise(2000, 6400), torricelli(4, 16), bubble(0.04, 8), wire_energy(1000, 0.8),
    banking_friction(60, 0.3), rain_angle(10, 10), junction(100, 90, 300, 10), adiabatic_t(400, 8),
    cop_fridge(-13, 27), isothermal_w(3, 350, 4), cooling(70, 50, 20, 8, 35), doppler_both(600, 10, 20),
    resonance_tube(320, 25, 77), field_inside(8, 0.4, 0.3), slab_cap(3, 6, 4, 5), share_loss(5, 120, 5, 40),
    rc_half(150, 10), lr_current(9, 6, 1.5), lc_freq(16, 25), loop_b(200, 1, 20), ac_power(240, 8, 0.9),
    lens_maker(1.5, 30, -60), fringe_shift(1.4, 4.5, 450), single_slit(450, 90, 2), resolve(600, 5),
    xray_cutoff(62), activity(2, 1), screw_gauge(1, 50),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    _q("A block slides down a frictionless wedge that itself rests on a frictionless floor. Which quantity is conserved for the block + wedge system?", ["Horizontal momentum", "Vertical momentum", "Total momentum in every direction", "The block's speed"],
       "No external horizontal force acts; gravity and the floor's normal force are vertical.",
       "ঘর্ষণহীন মেঝেতে রাখা একটা ঘর্ষণহীন কীলকের গা বেয়ে একটা ব্লক নামছে। ব্লক + কীলক সংস্থায় কোন রাশি সংরক্ষিত?", ["অনুভূমিক ভরবেগ", "উল্লম্ব ভরবেগ", "সব দিকে মোট ভরবেগ", "ব্লকের দ্রুতি"],
       "কোনো বাহ্যিক অনুভূমিক বল নেই; অভিকর্ষ আর মেঝের অভিলম্ব বল উল্লম্ব।"),
    _q("In the frame of an accelerating lift, a pseudo force must be added. In which direction does it act on a body?", ["Opposite to the lift's acceleration", "Along the lift's acceleration", "Always downward", "Always zero"],
       "F_pseudo = -m a_frame; with it, Newton's laws work in the non-inertial frame.",
       "ত্বরিত লিফটের নির্দেশতন্ত্রে একটা ছদ্ম বল যোগ করতে হয়। কোনো বস্তুর উপর তা কোন দিকে কাজ করে?", ["লিফটের ত্বরণের বিপরীতে", "লিফটের ত্বরণের দিকে", "সবসময় নিচের দিকে", "সবসময় শূন্য"],
       "ছদ্ম বল = -m a_তন্ত্র; এটা যোগ করলে অজড় তন্ত্রেও নিউটনের সূত্র খাটে।"),
    _q("A disc rolls without slipping. Which point has zero instantaneous velocity, and what does that mean?", ["The contact point; the disc rotates about it at that instant", "The centre; the disc is at rest", "The top point; it moves backwards", "No point is ever at rest"],
       "The instantaneous axis of rotation passes through the contact point, so v = ωr from there.",
       "একটা চাকতি না পিছলে গড়ায়। কোন বিন্দুর তাৎক্ষণিক বেগ শূন্য, আর তার মানে কী?", ["স্পর্শবিন্দু; সেই মুহূর্তে চাকতি তার চারপাশে ঘোরে", "কেন্দ্র; চাকতি স্থির", "শীর্ষবিন্দু; সেটা পেছনে চলে", "কোনো বিন্দুই কখনো স্থির নয়"],
       "তাৎক্ষণিক ঘূর্ণন-অক্ষ স্পর্শবিন্দু দিয়ে যায়, তাই সেখান থেকে v = ωr।"),
    _q("Which body reaches the bottom of an incline first when all roll from rest without slipping?", ["The solid sphere", "The hollow sphere", "The ring", "They all arrive together"],
       "a = g sin θ ÷ (1 + k²/R²); the solid sphere has the smallest k²/R² (2/5), so the largest acceleration.",
       "সব স্থির অবস্থা থেকে না পিছলে গড়ালে কোন বস্তু নত তলের নিচে প্রথমে পৌঁছায়?", ["নিরেট গোলক", "ফাঁপা গোলক", "আংটি", "সবাই একসঙ্গে পৌঁছায়"],
       "ত্বরণ = g sin θ ÷ (1 + k²/R²); নিরেট গোলকের k²/R² সবচেয়ে কম (2/5), তাই ত্বরণ সবচেয়ে বেশি।"),
    _q("For a satellite in a circular orbit, how are its kinetic energy K and total energy E related?", ["E = -K", "E = K", "E = 2K", "E = 0"],
       "K = GMm/2r and U = -GMm/r, so E = -GMm/2r = -K; lowering E (by drag) speeds the satellite up.",
       "বৃত্তাকার কক্ষপথে একটা উপগ্রহের গতিশক্তি K আর মোট শক্তি E-এর সম্পর্ক কী?", ["E = -K", "E = K", "E = 2K", "E = 0"],
       "K = GMm/2r আর U = -GMm/r, তাই E = -GMm/2r = -K; বাধায় E কমলে উপগ্রহ আসলে দ্রুত চলে।"),
    _q("What is the gravitational field inside a uniform spherical shell?", ["Zero everywhere inside", "Largest at the centre", "Same as at the surface", "Infinite at the centre"],
       "Contributions from opposite parts of the shell cancel exactly (Newton's shell theorem).",
       "একটা সুষম গোলীয় খোলের ভেতরে মহাকর্ষীয় ক্ষেত্র কত?", ["ভেতরে সব জায়গায় শূন্য", "কেন্দ্রে সর্বোচ্চ", "পৃষ্ঠের সমান", "কেন্দ্রে অসীম"],
       "খোলের বিপরীত অংশের প্রভাব হুবহু কাটাকাটি হয় (নিউটনের খোল উপপাদ্য)।"),
    _q("A body is dropped into a tunnel through the Earth's centre. Ignoring air and rotation, how does it move?", ["Simple harmonic motion with a period of about 84 minutes", "It stops at the centre", "It accelerates forever", "Uniform motion"],
       "Inside a uniform Earth, g ∝ r, a restoring force like a spring; T = 2π√(R/g).",
       "পৃথিবীর কেন্দ্র দিয়ে যাওয়া একটা সুড়ঙ্গে একটা বস্তু ফেলা হল। বাতাস আর ঘূর্ণন বাদ দিলে এটা কীভাবে চলে?", ["প্রায় 84 মিনিট পর্যায়কালের সরল দোলগতিতে", "কেন্দ্রে থেমে যায়", "চিরকাল ত্বরিত হয়", "সুষম গতিতে"],
       "সুষম পৃথিবীর ভেতরে g ∝ r, স্প্রিংয়ের মতো প্রত্যানয়ক বল; T = 2π√(R/g)।"),
    _q("Why does a spinning top precess instead of falling over?", ["Gravity's torque changes the direction of its angular momentum, not its size", "Air pressure holds it up", "Friction lifts it", "It has no weight while spinning"],
       "dL/dt = τ is horizontal and perpendicular to L, so L sweeps round in a cone.",
       "ঘুরন্ত লাট্টু পড়ে না গিয়ে অয়নচলন (প্রিসেশন) করে কেন?", ["অভিকর্ষের টর্ক কৌণিক ভরবেগের দিক বদলায়, মান নয়", "বায়ুচাপ একে ধরে রাখে", "ঘর্ষণ একে তোলে", "ঘোরার সময় এর ওজন থাকে না"],
       "dL/dt = τ অনুভূমিক আর L-এর লম্ব, তাই L একটা শঙ্কু বরাবর ঘোরে।"),
    _q("Bernoulli's equation applies along a streamline only if the flow is…", ["Steady, incompressible and non-viscous", "Turbulent", "Highly viscous", "Compressible at any speed"],
       "Viscosity dissipates energy; turbulence breaks the idea of fixed streamlines.",
       "বার্নুলির সমীকরণ একটা প্রবাহরেখা বরাবর খাটে কেবল যদি প্রবাহ হয়…", ["স্থির, অসংনম্য আর অসান্দ্র", "বিক্ষুব্ধ", "অতি সান্দ্র", "যেকোনো বেগে সংনম্য"],
       "সান্দ্রতা শক্তি নষ্ট করে; বিক্ষুব্ধতা স্থির প্রবাহরেখার ধারণা ভেঙে দেয়।"),
    _q("When does flow through a pipe turn turbulent?", ["When the Reynolds number exceeds roughly 2,000-4,000", "When the pipe is very short", "When the liquid is very viscous", "Never in water"],
       "Re = ρvD/η compares inertia with viscosity; fast flow in wide pipes becomes turbulent.",
       "নলের মধ্য দিয়ে প্রবাহ কখন বিক্ষুব্ধ হয়?", ["যখন রেনল্ডস সংখ্যা মোটামুটি 2,000-4,000 ছাড়ায়", "যখন নল খুব ছোট", "যখন তরল খুব সান্দ্র", "জলে কখনো নয়"],
       "রেনল্ডস সংখ্যা = ρvD/η জড়তাকে সান্দ্রতার সঙ্গে তুলনা করে; চওড়া নলে দ্রুত প্রবাহ বিক্ষুব্ধ হয়।"),
    _q("In a free expansion of an ideal gas into a vacuum (insulated container), what happens to its temperature?", ["It stays the same", "It rises", "It falls", "It becomes zero"],
       "Q = 0 and W = 0 (nothing to push against), so ΔU = 0; for an ideal gas U depends only on T.",
       "তাপ-নিরোধী পাত্রে শূন্যস্থানে আদর্শ গ্যাসের মুক্ত প্রসারণে তাপমাত্রার কী হয়?", ["একই থাকে", "বাড়ে", "কমে", "শূন্য হয়"],
       "Q = 0 আর W = 0 (ঠেলার কিছু নেই), তাই ΔU = 0; আদর্শ গ্যাসে U কেবল T-এর উপর নির্ভর করে।"),
    _q("Which statement about entropy in an isolated system is correct?", ["It never decreases; it rises in irreversible processes", "It always stays exactly constant", "It always decreases", "It is unrelated to heat"],
       "This is the second law; reversible processes keep total entropy constant.",
       "বিচ্ছিন্ন সংস্থায় এনট্রপি সম্পর্কে কোন বিবৃতি সঠিক?", ["কখনো কমে না; অপ্রত্যাবর্তী প্রক্রিয়ায় বাড়ে", "সবসময় ঠিক একই থাকে", "সবসময় কমে", "তাপের সঙ্গে সম্পর্কহীন"],
       "এটাই দ্বিতীয় সূত্র; প্রত্যাবর্তী প্রক্রিয়ায় মোট এনট্রপি স্থির থাকে।"),
    _q("On a P-V diagram, the work done by a gas in a complete clockwise cycle equals…", ["The area enclosed by the cycle", "Zero always", "P x V at the start", "The area under the lowest curve"],
       "Clockwise cycles do net work (engines); anticlockwise cycles need work input (refrigerators).",
       "P-V লেখচিত্রে একটা সম্পূর্ণ দক্ষিণাবর্ত চক্রে গ্যাসের কৃতকাজ সমান…", ["চক্রে আবদ্ধ ক্ষেত্রফল", "সবসময় শূন্য", "শুরুতে P x V", "সবচেয়ে নিচের রেখার নিচের ক্ষেত্রফল"],
       "দক্ষিণাবর্ত চক্র নিট কাজ করে (ইঞ্জিন); বামাবর্ত চক্রে কাজ দিতে হয় (রেফ্রিজারেটর)।"),
    _q("Why is the adiabatic curve on a P-V diagram steeper than the isothermal through the same point?", ["Slope is -γP/V for adiabatic but -P/V for isothermal, and γ > 1", "The adiabatic has no pressure", "Isothermal curves are vertical", "They have equal slopes"],
       "In adiabatic compression the temperature also rises, so pressure climbs faster.",
       "P-V লেখচিত্রে একই বিন্দু দিয়ে যাওয়া রুদ্ধতাপ রেখা সমোষ্ণ রেখার চেয়ে খাড়া কেন?", ["রুদ্ধতাপে নতি -γP/V, সমোষ্ণে -P/V, আর γ > 1", "রুদ্ধতাপে চাপ নেই", "সমোষ্ণ রেখা উল্লম্ব", "দুটোর নতি সমান"],
       "রুদ্ধতাপ সংকোচনে তাপমাত্রাও বাড়ে, তাই চাপ দ্রুত চড়ে।"),
    _q("Two coherent waves of equal amplitude A meet with a phase difference φ. What is the resultant amplitude?", ["2A cos(φ/2)", "2A", "A cos φ", "A/2"],
       "It is 2A for φ = 0 (constructive) and 0 for φ = π (destructive).",
       "সমান বিস্তার A-এর দুটো সুসংগত তরঙ্গ φ দশা-পার্থক্যে মেলে। ফলস্বরূপ বিস্তার কত?", ["2A কোসাইন(φ/2)", "2A", "A কোসাইন φ", "A/2"],
       "φ = 0 হলে 2A (গঠনমূলক) আর φ = π হলে 0 (ধ্বংসাত্মক)।"),
    _q("A string fixed at both ends vibrates in its third harmonic. How many nodes (including the ends) are there?", ["4", "3", "2", "6"],
       "The nth harmonic has n loops and n + 1 nodes.",
       "দুই প্রান্তে আটকানো একটা তার তৃতীয় সমমেলে কাঁপছে। কয়টি নিস্পন্দ বিন্দু (প্রান্তসহ) আছে?", ["4", "3", "2", "6"],
       "n-তম সমমেলে n-টি লুপ আর n + 1টি নিস্পন্দ বিন্দু।"),
    _q("A pipe closed at one end can produce which harmonics?", ["Only odd harmonics (f, 3f, 5f, …)", "All harmonics", "Only even harmonics", "Only the fundamental"],
       "The closed end must be a node and the open end an antinode, allowing only odd quarter-wave patterns.",
       "এক প্রান্ত বন্ধ নল কোন সমমেলগুলো তৈরি করতে পারে?", ["কেবল বিজোড় সমমেল (f, 3f, 5f, …)", "সব সমমেল", "কেবল জোড় সমমেল", "কেবল মূল সুর"],
       "বন্ধ প্রান্তে নিস্পন্দ আর খোলা প্রান্তে সুস্পন্দ হতেই হবে, তাই কেবল বিজোড় চতুর্থাংশ-তরঙ্গ নকশা সম্ভব।"),
    _q("A charge q sits at the centre of a cube. What is the electric flux through one face?", ["q ÷ 6ε₀", "q ÷ ε₀", "q ÷ 4ε₀", "Zero"],
       "By symmetry the total flux q/ε₀ divides equally among the six faces.",
       "একটা ঘনকের কেন্দ্রে একটা আধান q আছে। একটা তলের মধ্য দিয়ে তড়িৎ-ফ্লাক্স কত?", ["q ÷ 6ε₀", "q ÷ ε₀", "q ÷ 4ε₀", "শূন্য"],
       "প্রতিসাম্যের জন্য মোট ফ্লাক্স q/ε₀ ছয়টি তলে সমানভাবে ভাগ হয়।"),
    _q("A point charge is placed near a large grounded conducting plate. The force on it is the same as that from…", ["An equal and opposite image charge at the mirror point behind the plate", "No charge at all", "An equal charge of the same sign", "A charge twice as large"],
       "The method of images: the plate's induced charge acts like the mirror charge -q.",
       "একটা বড় ভূ-সংযুক্ত পরিবাহী পাতের কাছে একটা বিন্দু-আধান রাখা হল। এর উপর বল সমান…", ["পাতের পেছনে দর্পণ-বিন্দুতে একটা সমান ও বিপরীত প্রতিবিম্ব-আধানের বলের", "কোনো আধানই নয়", "একই চিহ্নের সমান আধানের", "দ্বিগুণ বড় আধানের"],
       "প্রতিবিম্ব পদ্ধতি: পাতের আবিষ্ট আধান দর্পণ-আধান -q-এর মতো আচরণ করে।"),
    _q("Why does charge on an irregular conductor concentrate at sharp points?", ["Surface charge density is highest where curvature is greatest", "Sharp points are hotter", "Charge avoids flat parts by magnetism", "It does not - charge spreads evenly"],
       "High fields at points cause corona discharge; lightning conductors use this.",
       "অনিয়মিত আকারের পরিবাহীতে আধান তীক্ষ্ণ বিন্দুতে জমা হয় কেন?", ["যেখানে বক্রতা সবচেয়ে বেশি সেখানে পৃষ্ঠ-আধান ঘনত্ব সর্বোচ্চ", "তীক্ষ্ণ বিন্দু বেশি গরম", "চুম্বকত্বে আধান সমতল অংশ এড়ায়", "জমা হয় না - আধান সমানভাবে ছড়ায়"],
       "বিন্দুতে তীব্র ক্ষেত্র করোনা-মোক্ষণ ঘটায়; বজ্রনিরোধক এটা কাজে লাগায়।"),
    _q("In a charging RC circuit, what fraction of the energy drawn from the battery ends up stored in the capacitor?", ["Half", "All of it", "One quarter", "None"],
       "The battery supplies QV; the capacitor stores QV/2; the resistor dissipates the other half, whatever its value.",
       "আহিত হতে থাকা RC বর্তনীতে ব্যাটারি থেকে নেওয়া শক্তির কত অংশ শেষে ধারকে জমা থাকে?", ["অর্ধেক", "পুরোটা", "এক-চতুর্থাংশ", "কিছুই না"],
       "ব্যাটারি QV দেয়; ধারক QV/2 জমায়; বাকি অর্ধেক রোধে খরচ হয়, রোধের মান যাই হোক।"),
    _q("A current-carrying loop sits in a uniform magnetic field. What is the net force on it?", ["Zero, although there may be a torque", "Always maximum", "Along the field", "Perpendicular to the loop always"],
       "Forces on opposite sides cancel in a uniform field; a non-uniform field gives a net force.",
       "একটা প্রবাহবাহী লুপ সুষম চৌম্বকক্ষেত্রে আছে। এর উপর মোট বল কত?", ["শূন্য, যদিও টর্ক থাকতে পারে", "সবসময় সর্বোচ্চ", "ক্ষেত্র বরাবর", "সবসময় লুপের লম্ব"],
       "সুষম ক্ষেত্রে বিপরীত বাহুর বল কাটাকাটি হয়; অসম ক্ষেত্রে মোট বল থাকে।"),
    _q("Two long parallel wires carry currents in the same direction. The wires…", ["Attract each other", "Repel each other", "Do not interact", "Twist around each other"],
       "This is the basis of the old definition of the ampere: 2 x 10⁻⁷ N per metre for 1 A each, 1 m apart.",
       "দুটো লম্বা সমান্তরাল তারে একই দিকে প্রবাহ। তার দুটো…", ["পরস্পরকে আকর্ষণ করে", "পরস্পরকে বিকর্ষণ করে", "কোনো ক্রিয়া করে না", "একে অপরকে পাক খায়"],
       "এটাই অ্যাম্পিয়ারের পুরোনো সংজ্ঞার ভিত্তি: 1 m দূরে 1 A করে হলে মিটারপ্রতি 2 x 10⁻⁷ N।"),
    _q("A charged particle moves through crossed E and B fields undeflected. What is its speed?", ["v = E ÷ B", "v = B ÷ E", "v = EB", "Any speed"],
       "qE = qvB; this 'velocity selector' passes only particles of one speed.",
       "একটা আহিত কণা আড়াআড়ি E আর B ক্ষেত্রের মধ্য দিয়ে বিচ্যুত না হয়ে যায়। এর বেগ কত?", ["v = E ÷ B", "v = B ÷ E", "v = EB", "যেকোনো বেগ"],
       "qE = qvB; এই 'বেগ-বাছাইকারী' কেবল এক বেগের কণা পার হতে দেয়।"),
    _q("A cyclotron's frequency does not depend on the particle's speed (non-relativistically) because…", ["The orbit radius grows in proportion to speed, so the period stays qB-dependent only", "The field changes with speed", "The particles never speed up", "The dees rotate"],
       "f = qB ÷ 2πm; this fails at high speeds as relativistic mass grows.",
       "সাইক্লোট্রনের কম্পাঙ্ক কণার বেগের উপর (অনাপেক্ষিকভাবে) নির্ভর করে না কারণ…", ["কক্ষের ব্যাসার্ধ বেগের সমানুপাতে বাড়ে, তাই পর্যায়কাল কেবল qB-নির্ভর থাকে", "ক্ষেত্র বেগের সঙ্গে বদলায়", "কণা কখনো দ্রুত হয় না", "ডি-গুলো ঘোরে"],
       "কম্পাঙ্ক = qB ÷ 2πm; উচ্চ বেগে আপেক্ষিক ভর বাড়লে এটা আর খাটে না।"),
    _q("A magnet falls through a long copper tube. Compared with free fall, it…", ["Falls much more slowly because induced eddy currents oppose its motion", "Falls faster", "Falls at exactly g", "Stops completely forever"],
       "Lenz's law: the induced currents make magnetic fields that brake the magnet; it reaches a terminal speed.",
       "একটা চুম্বক একটা লম্বা তামার নলের মধ্য দিয়ে পড়ে। মুক্ত পতনের তুলনায় এটা…", ["অনেক ধীরে পড়ে কারণ আবিষ্ট ঘূর্ণি-প্রবাহ এর গতির বিরোধিতা করে", "দ্রুত পড়ে", "ঠিক g-তে পড়ে", "চিরকালের জন্য থেমে যায়"],
       "লেঞ্জের সূত্র: আবিষ্ট প্রবাহ এমন চৌম্বকক্ষেত্র তৈরি করে যা চুম্বককে ব্রেক করে; এটা একটা প্রান্তিক বেগে পৌঁছায়।"),
    _q("The mutual inductance of two coils depends on…", ["Their geometry, relative position and the core material", "Only the current in them", "The battery voltage", "Only the wire's colour"],
       "M = Φ₂/I₁; coils wound on the same iron core have a large M - as in a transformer.",
       "দুটো কুণ্ডলীর পারস্পরিক আবেশাঙ্ক নির্ভর করে…", ["তাদের জ্যামিতি, আপেক্ষিক অবস্থান আর কোরের পদার্থের উপর", "কেবল তাদের প্রবাহের উপর", "ব্যাটারির বিভবের উপর", "কেবল তারের রঙের উপর"],
       "M = Φ₂/I₁; একই লোহার কোরে জড়ানো কুণ্ডলীর M বড় - যেমন ট্রান্সফর্মারে।"),
    _q("At very high frequency, how do an ideal inductor and an ideal capacitor behave?", ["The inductor acts like an open circuit and the capacitor like a short circuit", "Both act like short circuits", "Both act like open circuits", "The inductor acts like a short circuit"],
       "X_L = ωL grows and X_C = 1/ωC shrinks as frequency rises; at DC the reverse holds.",
       "অতি উচ্চ কম্পাঙ্কে আদর্শ আবেশক আর আদর্শ ধারক কেমন আচরণ করে?", ["আবেশক খোলা বর্তনীর মতো আর ধারক শর্ট-সার্কিটের মতো", "দুটোই শর্ট-সার্কিটের মতো", "দুটোই খোলা বর্তনীর মতো", "আবেশক শর্ট-সার্কিটের মতো"],
       "কম্পাঙ্ক বাড়লে X_L = ωL বাড়ে আর X_C = 1/ωC কমে; ডিসি-তে উল্টোটা।"),
    _q("The quality factor Q of a series LCR circuit measures…", ["The sharpness of its resonance", "Its resistance only", "Its power factor at DC", "Its capacitance"],
       "Q = ω₀L/R = (1/R)√(L/C); a high Q gives a narrow, tall resonance peak - good for radio tuning.",
       "শ্রেণি LCR বর্তনীর গুণমান-গুণক Q কী মাপে?", ["অনুনাদের তীক্ষ্ণতা", "কেবল রোধ", "ডিসি-তে ক্ষমতা-গুণক", "ধারকত্ব"],
       "Q = ω₀L/R = (1/R)√(L/C); বেশি Q সরু, উঁচু অনুনাদ-শীর্ষ দেয় - রেডিও টিউনিংয়ে ভালো।"),
    _q("A plane EM wave travels in the +x direction with E along y. In which direction does B point?", ["Along z", "Along x", "Along y", "Opposite to x"],
       "E, B and the direction of travel form a right-handed set: E x B points along the propagation.",
       "একটা সমতল তড়িৎচুম্বকীয় তরঙ্গ +x দিকে চলে, E আছে y বরাবর। B কোন দিকে?", ["z বরাবর", "x বরাবর", "y বরাবর", "x-এর বিপরীতে"],
       "E, B আর গতির দিক ডানহাতি সেট গড়ে: E x B সঞ্চারণের দিকে।"),
    _q("What is the displacement current, introduced by Maxwell?", ["ε₀ dΦ_E/dt, a changing electric field that creates a magnetic field like a current", "Current in a superconductor", "The current in a short circuit", "Electrons moving through a vacuum"],
       "It completes Ampère's law between capacitor plates and predicts electromagnetic waves.",
       "ম্যাক্সওয়েলের প্রবর্তিত সরণ-প্রবাহ কী?", ["ε₀ dΦ_E/dt, পরিবর্তনশীল তড়িৎক্ষেত্র যা প্রবাহের মতো চৌম্বকক্ষেত্র তৈরি করে", "অতিপরিবাহীর প্রবাহ", "শর্ট-সার্কিটের প্রবাহ", "শূন্যস্থানে চলমান ইলেকট্রন"],
       "এটা ধারকের পাতের মাঝে অ্যাম্পিয়ারের সূত্র পূর্ণ করে আর তড়িৎচুম্বকীয় তরঙ্গের পূর্বাভাস দেয়।"),
    _q("At Brewster's angle, the reflected light is…", ["Completely plane-polarised", "Unpolarised", "Circularly polarised", "Absent"],
       "tan θ_B = n; the reflected and refracted rays are then perpendicular to each other.",
       "ব্রুস্টার কোণে প্রতিফলিত আলো…", ["সম্পূর্ণ সমতল-সমবর্তিত", "অসমবর্তিত", "বৃত্তীয়ভাবে সমবর্তিত", "অনুপস্থিত"],
       "tan θ_B = n; তখন প্রতিফলিত আর প্রতিসৃত রশ্মি পরস্পর লম্ব।"),
    _q("Why do thin oil films on water show colours?", ["Interference between light reflected from the top and bottom surfaces", "The oil is dyed", "Diffraction by water waves", "Total internal reflection"],
       "For each thickness some wavelengths interfere constructively; one reflection has an extra π phase change.",
       "জলের উপর পাতলা তেলের স্তরে রং দেখা যায় কেন?", ["উপরের আর নিচের তল থেকে প্রতিফলিত আলোর ব্যতিচার", "তেল রং করা", "জলতরঙ্গে অপবর্তন", "পূর্ণ অভ্যন্তরীণ প্রতিফলন"],
       "প্রতিটি পুরুত্বে কিছু তরঙ্গদৈর্ঘ্য গঠনমূলক ব্যতিচার করে; একটা প্রতিফলনে বাড়তি π দশা-পরিবর্তন হয়।"),
    _q("If the whole Young's double-slit apparatus is dipped in water, the fringe width…", ["Decreases by the factor n of water", "Increases", "Stays the same", "Becomes zero"],
       "The wavelength in water is λ/n, and β = λD/d.",
       "ইয়ংয়ের দ্বি-ছিদ্র যন্ত্রটা পুরোটা জলে ডোবালে ঝালরের প্রস্থ…", ["জলের প্রতিসরাঙ্ক n গুণ কমে", "বাড়ে", "একই থাকে", "শূন্য হয়"],
       "জলে তরঙ্গদৈর্ঘ্য λ/n, আর β = λD/d।"),
    _q("Why is a thin convex lens's focal length different for red and violet light?", ["The glass's refractive index varies with wavelength (chromatic aberration)", "Red light travels in a curve", "Violet light is not refracted", "The lens shape changes"],
       "Violet focuses closer; an achromatic doublet of two glasses cancels the difference.",
       "পাতলা উত্তল লেন্সের ফোকাস দূরত্ব লাল আর বেগুনি আলোর জন্য আলাদা কেন?", ["কাচের প্রতিসরাঙ্ক তরঙ্গদৈর্ঘ্যের সঙ্গে বদলায় (বর্ণ-বিপথন)", "লাল আলো বাঁকা পথে চলে", "বেগুনি আলো প্রতিসৃত হয় না", "লেন্সের আকার বদলায়"],
       "বেগুনি কাছে ফোকাস হয়; দুই কাচের অবর্ণ জোড়-লেন্স পার্থক্যটা বাতিল করে।"),
    _q("In Compton scattering of X-rays by electrons, the scattered X-rays have…", ["A longer wavelength, depending on the scattering angle", "The same wavelength", "A shorter wavelength", "No energy"],
       "Δλ = (h/mc)(1 - cos θ); it showed that photons carry momentum.",
       "ইলেকট্রন দিয়ে এক্স-রশ্মির কম্পটন বিক্ষেপে বিক্ষিপ্ত এক্স-রশ্মির…", ["তরঙ্গদৈর্ঘ্য বেশি, বিক্ষেপ-কোণের উপর নির্ভর করে", "তরঙ্গদৈর্ঘ্য একই", "তরঙ্গদৈর্ঘ্য কম", "কোনো শক্তি নেই"],
       "Δλ = (h/mc)(1 - cos θ); এটা দেখিয়েছিল যে ফোটন ভরবেগ বয়।"),
    _q("Moseley's law relates the frequency of characteristic X-rays to…", ["The square of (Z - b), the atomic number", "The mass number", "The temperature", "The tube current"],
       "√f ∝ (Z - b); it let Moseley order the periodic table by atomic number.",
       "মোজলের সূত্র বৈশিষ্ট্যমূলক এক্স-রশ্মির কম্পাঙ্ককে কীসের সঙ্গে যুক্ত করে?", ["পারমাণবিক সংখ্যা (Z - b)-এর বর্গের সঙ্গে", "ভরসংখ্যার সঙ্গে", "তাপমাত্রার সঙ্গে", "নলের প্রবাহের সঙ্গে"],
       "√f ∝ (Z - b); এটা দিয়ে মোজলে পারমাণবিক সংখ্যা অনুযায়ী পর্যায় সারণি সাজিয়েছিলেন।"),
    _q("In β⁻ decay, why is the electron's energy spread over a continuous range?", ["An antineutrino carries away a varying share of the energy", "Electrons collide inside the nucleus", "The nucleus emits light too", "The measurement is inaccurate"],
       "Pauli proposed the neutrino to save energy and momentum conservation.",
       "β⁻ ক্ষয়ে ইলেকট্রনের শক্তি অবিচ্ছিন্ন পাল্লায় ছড়ানো কেন?", ["একটা প্রতি-নিউট্রিনো শক্তির পরিবর্তনশীল অংশ নিয়ে যায়", "নিউক্লিয়াসের ভেতরে ইলেকট্রন ধাক্কা খায়", "নিউক্লিয়াস আলোও দেয়", "মাপ ভুল"],
       "শক্তি আর ভরবেগ সংরক্ষণ বাঁচাতে পাউলি নিউট্রিনোর প্রস্তাব দিয়েছিলেন।"),
    _q("What does a moderator do in a thermal nuclear reactor?", ["Slows fast neutrons so they can cause more fission", "Absorbs all neutrons", "Cools the turbine", "Speeds up the neutrons"],
       "Water, heavy water or graphite are used; control rods (cadmium, boron) absorb neutrons instead.",
       "তাপীয় নিউক্লীয় চুল্লিতে মন্দক (মডারেটর) কী করে?", ["দ্রুত নিউট্রনকে ধীর করে, যাতে আরও বিভাজন ঘটে", "সব নিউট্রন শোষণ করে", "টারবাইন ঠান্ডা করে", "নিউট্রনকে দ্রুত করে"],
       "জল, ভারী জল বা গ্রাফাইট ব্যবহৃত হয়; নিয়ন্ত্রক দণ্ড (ক্যাডমিয়াম, বোরন) বরং নিউট্রন শোষণ করে।"),
    _q("Why is a transistor's base made thin and lightly doped?", ["So most carriers from the emitter cross to the collector, giving current gain", "To increase its resistance to infinity", "To make it emit light", "To store charge"],
       "Only a few carriers recombine in the base, so a small base current controls a large collector current.",
       "ট্রানজিস্টরের বেস পাতলা আর হালকাভাবে মেশানো (ডোপড) কেন?", ["যাতে নিঃসারকের বেশিরভাগ বাহক সংগ্রাহকে পৌঁছায়, প্রবাহ-বিবর্ধন দেয়", "রোধ অসীমে বাড়াতে", "আলো দিতে", "আধান জমাতে"],
       "বেসে অল্প বাহকই পুনর্মিলিত হয়, তাই ছোট বেস-প্রবাহ বড় সংগ্রাহক-প্রবাহ নিয়ন্ত্রণ করে।"),
    _q("A body slides down a rough incline at constant velocity. What can you say about the coefficient of kinetic friction?", ["μ = tan θ", "μ = sin θ", "μ = cos θ", "μ = 0"],
       "Constant velocity means zero net force: mg sin θ = μ mg cos θ.",
       "একটা বস্তু খসখসে নত তল বেয়ে স্থির বেগে নামছে। গতীয় ঘর্ষণাঙ্ক সম্পর্কে কী বলা যায়?", ["μ = ট্যান θ", "μ = সাইন θ", "μ = কোসাইন θ", "μ = 0"],
       "স্থির বেগ মানে মোট বল শূন্য: mg sin θ = μ mg cos θ।"),
    _q("For a particle moving in a circle with increasing speed, the acceleration…", ["Has both a centripetal and a tangential component", "Points only to the centre", "Points only along the velocity", "Is zero"],
       "a = √(a_c² + a_t²), with a_c = v²/r and a_t = dv/dt.",
       "বাড়তে থাকা দ্রুতিতে বৃত্তে চলা কণার ত্বরণ…", ["কেন্দ্রমুখী আর স্পর্শকীয় দুটো উপাংশই আছে", "কেবল কেন্দ্রের দিকে", "কেবল বেগ বরাবর", "শূন্য"],
       "a = √(a_c² + a_t²), যেখানে a_c = v²/r আর a_t = dv/dt।"),
    _q("A heavy and a light body have the same kinetic energy. Which has more momentum?", ["The heavier one", "The lighter one", "Both the same", "Cannot be compared"],
       "p = √(2mK), so for equal K the larger mass has larger momentum.",
       "একটা ভারী আর একটা হালকা বস্তুর গতিশক্তি সমান। কোনটার ভরবেগ বেশি?", ["ভারীটার", "হালকাটার", "দুটোর সমান", "তুলনা করা যায় না"],
       "p = √(2mK), তাই K সমান হলে বেশি ভরের ভরবেগ বেশি।"),
    _q("The potential energy of a particle is U(x) = ax² - bx (a, b > 0). Where is it in stable equilibrium?", ["x = b ÷ 2a", "x = 0", "x = b ÷ a", "x = 2a ÷ b"],
       "dU/dx = 0 at x = b/2a, and d²U/dx² = 2a > 0, so it is a minimum - stable.",
       "একটা কণার স্থিতিশক্তি U(x) = ax² - bx (a, b > 0)। এটা কোথায় সুস্থির সাম্যে থাকে?", ["x = b ÷ 2a", "x = 0", "x = b ÷ a", "x = 2a ÷ b"],
       "x = b/2a-তে dU/dx = 0, আর d²U/dx² = 2a > 0, তাই এটা অবম - সুস্থির।"),
    _q("A uniform chain lies on a smooth table with part hanging over the edge. As it slides off, which is conserved?", ["Mechanical energy of the chain", "The hanging length", "The chain's momentum", "The table's height"],
       "The table is smooth, so only gravity does work; speeds follow from the drop in the centre of mass.",
       "মসৃণ টেবিলে একটা সুষম শিকলের কিছুটা কিনারা থেকে ঝুলছে। পিছলে পড়ার সময় কী সংরক্ষিত থাকে?", ["শিকলের যান্ত্রিক শক্তি", "ঝুলন্ত দৈর্ঘ্য", "শিকলের ভরবেগ", "টেবিলের উচ্চতা"],
       "টেবিল মসৃণ, তাই কেবল অভিকর্ষ কাজ করে; ভরকেন্দ্রের পতন থেকে বেগ পাওয়া যায়।"),
    _q("The escape speed from a planet doubles if, at the same density, its radius…", ["Doubles", "Halves", "Quadruples", "Stays the same"],
       "v_e = √(2GM/R) and M ∝ ρR³, so v_e ∝ R√ρ.",
       "একই ঘনত্বে একটা গ্রহের মুক্তিবেগ দ্বিগুণ হয় যদি তার ব্যাসার্ধ…", ["দ্বিগুণ হয়", "অর্ধেক হয়", "চার গুণ হয়", "একই থাকে"],
       "v_e = √(2GM/R) আর M ∝ ρR³, তাই v_e ∝ R√ρ।"),
    _q("A metal rod is heated but prevented from expanding by rigid walls. The thermal stress in it depends on…", ["Y α ΔT - not on its length", "Its length only", "Its cross-section only", "Nothing - there is no stress"],
       "Strain prevented = αΔT; stress = Y x strain. Bridge bearings let decks move to avoid this.",
       "একটা ধাতব দণ্ড গরম করা হল, কিন্তু শক্ত দেয়াল একে প্রসারিত হতে দেয় না। এতে তাপীয় পীড়ন নির্ভর করে…", ["Y α ΔT-এর উপর - দৈর্ঘ্যের উপর নয়", "কেবল দৈর্ঘ্যের উপর", "কেবল প্রস্থচ্ছেদের উপর", "কিছুরই উপর নয় - পীড়ন নেই"],
       "বাধাপ্রাপ্ত বিকৃতি = αΔT; পীড়ন = Y x বিকৃতি। এটা এড়াতে সেতুর বিয়ারিং পাটাতনকে সরতে দেয়।"),
    _q("Which is the correct relation between the specific heats and γ for an ideal gas?", ["Cv = R ÷ (γ - 1)", "Cv = R(γ - 1)", "Cp = R ÷ γ", "Cv = γR"],
       "From Cp - Cv = R and γ = Cp/Cv; then Cp = γR/(γ - 1).",
       "আদর্শ গ্যাসে আপেক্ষিক তাপ আর γ-এর সঠিক সম্পর্ক কোনটা?", ["Cv = R ÷ (γ - 1)", "Cv = R(γ - 1)", "Cp = R ÷ γ", "Cv = γR"],
       "Cp - Cv = R আর γ = Cp/Cv থেকে; তখন Cp = γR/(γ - 1)।"),
    _q("A capacitor is charged and then disconnected; its plates are pulled further apart. What happens?", ["Charge stays the same, voltage and stored energy increase", "Charge decreases", "Voltage decreases", "Energy decreases"],
       "C falls; with Q fixed, V = Q/C and U = Q²/2C rise - the work done pulling the plates supplies the energy.",
       "একটা ধারক আহিত করে বিচ্ছিন্ন করা হল; তারপর পাত দুটো আরও দূরে টানা হল। কী হয়?", ["আধান একই থাকে, বিভব আর জমা শক্তি বাড়ে", "আধান কমে", "বিভব কমে", "শক্তি কমে"],
       "C কমে; Q স্থির থাকায় V = Q/C আর U = Q²/2C বাড়ে - পাত টানার কাজ থেকে শক্তি আসে।"),
    _q("A long solenoid's self-inductance is proportional to…", ["The square of its number of turns per unit length", "The current in it", "Its resistance", "The battery's emf"],
       "L = μ₀n²Al; doubling the turns per metre quadruples L.",
       "একটা লম্বা সলিনয়েডের স্বাবেশাঙ্ক সমানুপাতিক…", ["একক দৈর্ঘ্যে পাকসংখ্যার বর্গের", "তার প্রবাহের", "তার রোধের", "ব্যাটারির তড়িচ্চালক বলের"],
       "L = μ₀n²Al; মিটারপ্রতি পাক দ্বিগুণ হলে L চার গুণ।"),
    _q("The work function of a metal is the minimum energy needed to…", ["Remove an electron from its surface", "Melt the metal", "Ionise the nucleus", "Excite a photon"],
       "Alkali metals have low work functions, so even visible light frees electrons from them.",
       "একটা ধাতুর কার্য-অপেক্ষক হলো ন্যূনতম শক্তি যা লাগে…", ["তার পৃষ্ঠ থেকে একটা ইলেকট্রন সরাতে", "ধাতু গলাতে", "নিউক্লিয়াস আয়নিত করতে", "একটা ফোটন উত্তেজিত করতে"],
       "ক্ষারধাতুর কার্য-অপেক্ষক কম, তাই দৃশ্যমান আলোও তাদের থেকে ইলেকট্রন মুক্ত করে।"),
    _q("In a Bohr atom, as the electron moves to higher orbits, its kinetic energy…", ["Decreases while total energy increases (becomes less negative)", "Increases", "Stays the same", "Becomes negative"],
       "K = -E and E = -13.6Z²/n² eV; outer electrons move more slowly.",
       "বোর পরমাণুতে ইলেকট্রন উচ্চতর কক্ষে গেলে তার গতিশক্তি…", ["কমে, অথচ মোট শক্তি বাড়ে (কম ঋণাত্মক হয়)", "বাড়ে", "একই থাকে", "ঋণাত্মক হয়"],
       "K = -E আর E = -13.6Z²/n² eV; বাইরের ইলেকট্রন ধীরে চলে।"),
    _q("Which property makes a p-n junction act as a rectifier?", ["It conducts easily in forward bias and hardly at all in reverse bias", "It has equal resistance both ways", "It stores charge like a battery", "It emits light in reverse bias"],
       "Only one half of each AC cycle passes, so the output is unidirectional.",
       "কোন বৈশিষ্ট্যের জন্য p-n সংযোগ একমুখীকারক হিসেবে কাজ করে?", ["সম্মুখ ঝোঁকে সহজে পরিবহন করে আর বিপরীত ঝোঁকে প্রায় করেই না", "দুই দিকে রোধ সমান", "ব্যাটারির মতো আধান জমায়", "বিপরীত ঝোঁকে আলো দেয়"],
       "প্রতি এসি চক্রের কেবল এক অর্ধ পার হয়, তাই আউটপুট একমুখী।"),
    _q("A ball is thrown horizontally from a moving train. Seen from the ground, its path is…", ["A parabola with horizontal speed equal to the train's speed plus the throw speed", "A straight vertical line", "A circle", "A straight horizontal line"],
       "Velocities add (Galilean relativity); gravity alone acts vertically.",
       "চলন্ত ট্রেন থেকে একটা বল অনুভূমিকভাবে ছোড়া হল। মাটি থেকে দেখলে এর পথ…", ["একটা অধিবৃত্ত, যার অনুভূমিক বেগ ট্রেনের বেগ যোগ ছোড়ার বেগ", "সোজা উল্লম্ব রেখা", "একটা বৃত্ত", "সোজা অনুভূমিক রেখা"],
       "বেগ যোগ হয় (গ্যালিলীয় আপেক্ষিকতা); কেবল অভিকর্ষ উল্লম্বভাবে কাজ করে।"),
    _q("Why can't a real heat engine reach the Carnot efficiency?", ["Real processes involve friction, finite-speed heat flow and other irreversibilities", "Carnot engines use magic fuel", "Real engines have no cold reservoir", "The Carnot limit is lower than real engines"],
       "Every irreversibility creates entropy, which lowers the work obtained from the same heat.",
       "প্রকৃত তাপ-ইঞ্জিন কার্নো দক্ষতায় পৌঁছাতে পারে না কেন?", ["প্রকৃত প্রক্রিয়ায় ঘর্ষণ, সসীম বেগে তাপপ্রবাহ আর অন্যান্য অপ্রত্যাবর্তিতা থাকে", "কার্নো ইঞ্জিন জাদু-জ্বালানি ব্যবহার করে", "প্রকৃত ইঞ্জিনের শীতল আধার নেই", "কার্নো সীমা প্রকৃত ইঞ্জিনের চেয়ে কম"],
       "প্রতিটি অপ্রত্যাবর্তিতা এনট্রপি তৈরি করে, যা একই তাপ থেকে পাওয়া কাজ কমায়।"),
    _q("A wave's equation is y = A sin(kx - ωt). What is its speed?", ["ω ÷ k", "k ÷ ω", "ωk", "A ω"],
       "A crest moves so that kx - ωt stays constant: dx/dt = ω/k = fλ.",
       "একটা তরঙ্গের সমীকরণ y = A sin(kx - ωt)। এর বেগ কত?", ["ω ÷ k", "k ÷ ω", "ωk", "A ω"],
       "শীর্ষ এমনভাবে চলে যে kx - ωt স্থির থাকে: dx/dt = ω/k = fλ।"),
    _q("A particle moves under a central force (always towards a fixed point). Which quantity is conserved about that point?", ["Angular momentum", "Linear momentum", "Speed", "Kinetic energy always"],
       "A central force has zero torque about the centre; this gives Kepler's law of equal areas.",
       "একটা কণা কেন্দ্রীয় বলের (সবসময় একটা স্থির বিন্দুর দিকে) অধীনে চলে। ওই বিন্দুর সাপেক্ষে কোন রাশি সংরক্ষিত?", ["কৌণিক ভরবেগ", "রৈখিক ভরবেগ", "দ্রুতি", "সবসময় গতিশক্তি"],
       "কেন্দ্রীয় বলের কেন্দ্রের সাপেক্ষে টর্ক শূন্য; এ থেকেই কেপলারের সমান ক্ষেত্রফলের সূত্র।"),
    _q("The moment of inertia of a body depends on…", ["Its mass distribution relative to the chosen axis", "Its angular velocity", "The torque applied", "Its temperature only"],
       "Mass far from the axis contributes more: I = Σ m r².",
       "একটা বস্তুর জড়তা-ভ্রামক নির্ভর করে…", ["বাছা অক্ষের সাপেক্ষে তার ভর-বণ্টনের উপর", "তার কৌণিক বেগের উপর", "প্রযুক্ত টর্কের উপর", "কেবল তার তাপমাত্রার উপর"],
       "অক্ষ থেকে দূরের ভর বেশি অবদান রাখে: I = Σ m r²।"),
    _q("Why does the time period of a simple pendulum increase slightly at large amplitudes?", ["The restoring force is proportional to sin θ, not θ, so the motion is not exactly SHM", "The string stretches", "Gravity weakens at the ends", "Air resistance vanishes"],
       "The small-angle formula T = 2π√(L/g) assumes sin θ ≈ θ.",
       "বড় বিস্তারে সরল দোলকের পর্যায়কাল সামান্য বাড়ে কেন?", ["প্রত্যানয়ক বল θ-এর নয়, sin θ-এর সমানুপাতিক, তাই গতি ঠিক সরল দোলগতি নয়", "সুতো প্রসারিত হয়", "প্রান্তে অভিকর্ষ দুর্বল হয়", "বায়ুর বাধা উধাও হয়"],
       "ছোট কোণের সূত্র T = 2π√(L/g) ধরে নেয় sin θ ≈ θ।"),
    _q("What happens to the resonant frequency of an LC circuit if the capacitance is made four times larger?", ["It halves", "It doubles", "It becomes four times", "It does not change"],
       "f = 1 ÷ 2π√(LC), so f ∝ 1/√C.",
       "ধারকত্ব চার গুণ করলে একটা LC বর্তনীর অনুনাদ-কম্পাঙ্কের কী হয়?", ["অর্ধেক হয়", "দ্বিগুণ হয়", "চার গুণ হয়", "বদলায় না"],
       "f = 1 ÷ 2π√(LC), তাই f ∝ 1/√C।"),
    _q("A convex lens is cut into two equal halves along its principal axis. What is the focal length of each half?", ["The same as the original", "Half", "Double", "Infinite"],
       "Each half keeps the same curved surfaces; only the light gathered (brightness) is halved.",
       "একটা উত্তল লেন্সকে তার প্রধান অক্ষ বরাবর দুটো সমান অর্ধে কাটা হল। প্রতিটি অর্ধের ফোকাস দূরত্ব কত?", ["মূল লেন্সের সমান", "অর্ধেক", "দ্বিগুণ", "অসীম"],
       "প্রতিটি অর্ধে একই বাঁকা তল থাকে; কেবল সংগৃহীত আলো (উজ্জ্বলতা) অর্ধেক হয়।"),
    _q("What is the de Broglie wavelength of a particle related to?", ["Its momentum, λ = h ÷ p", "Its charge only", "Its temperature only", "Its colour"],
       "Heavier or faster particles have shorter wavelengths, which is why everyday objects show no wave effects.",
       "একটা কণার দ্য ব্রয়লি তরঙ্গদৈর্ঘ্য কীসের সঙ্গে সম্পর্কিত?", ["তার ভরবেগের সঙ্গে, λ = h ÷ p", "কেবল তার আধানের সঙ্গে", "কেবল তার তাপমাত্রার সঙ্গে", "তার রঙের সঙ্গে"],
       "ভারী বা দ্রুত কণার তরঙ্গদৈর্ঘ্য ছোট, তাই দৈনন্দিন বস্তুতে তরঙ্গ-প্রভাব দেখা যায় না।"),
    _q("A metal sphere is given charge and then connected by a thin wire to a smaller uncharged metal sphere far away. After sharing, which sphere has the higher surface charge density?", ["The smaller sphere", "The larger sphere", "Both are equal", "Neither has any charge"],
       "Both end at the same potential kQ/R, so Q ∝ R and σ ∝ Q/R² ∝ 1/R.",
       "একটা ধাতব গোলককে আধান দিয়ে সরু তার দিয়ে দূরের একটা ছোট আধানহীন ধাতব গোলকের সঙ্গে যুক্ত করা হল। ভাগাভাগির পরে কোন গোলকের পৃষ্ঠ-আধান ঘনত্ব বেশি?", ["ছোট গোলকের", "বড় গোলকের", "দুটোর সমান", "কারো কোনো আধান নেই"],
       "দুটোই একই বিভব kQ/R-এ পৌঁছায়, তাই Q ∝ R আর σ ∝ Q/R² ∝ 1/R।"),
    _q("Why does a nucleus heavier than iron release energy when it splits?", ["The fragments have higher binding energy per nucleon than the original nucleus", "Splitting creates new protons", "Mass is not involved", "Electrons are released"],
       "The total mass of the fragments is a little less than the original; the difference appears as energy (E = Δmc²).",
       "লোহার চেয়ে ভারী নিউক্লিয়াস ভাঙলে শক্তি মুক্ত হয় কেন?", ["খণ্ডগুলোর নিউক্লিয়ন-প্রতি বন্ধনশক্তি মূল নিউক্লিয়াসের চেয়ে বেশি", "ভাঙলে নতুন প্রোটন তৈরি হয়", "ভরের কোনো ভূমিকা নেই", "ইলেকট্রন মুক্ত হয়"],
       "খণ্ডগুলোর মোট ভর মূলের চেয়ে সামান্য কম; পার্থক্যটা শক্তি হিসেবে দেখা দেয় (E = Δmc²)।"),
    _q("A ray enters a glass slab with parallel faces at an angle. How does it leave the slab?", ["Parallel to the incident ray but shifted sideways", "Along the normal", "Bent towards the base", "Reflected back"],
       "Refraction at the two parallel faces cancels in direction; the lateral shift grows with thickness and angle.",
       "একটা রশ্মি তির্যকভাবে সমান্তরাল তলের কাচ-ফলকে ঢোকে। ফলক থেকে এটা কীভাবে বেরোয়?", ["আপতিত রশ্মির সমান্তরালে, কিন্তু পাশে সরে", "অভিলম্ব বরাবর", "তলের দিকে বেঁকে", "পেছনে প্রতিফলিত হয়ে"],
       "দুই সমান্তরাল তলের প্রতিসরণ দিকের হিসেবে কাটাকাটি হয়; পার্শ্ব-সরণ পুরুত্ব আর কোণের সঙ্গে বাড়ে।"),
    _q("In a meter bridge, why is the balance point preferred near the middle of the wire?", ["It reduces the percentage error, including end-correction effects", "The wire is thicker there", "Current is zero at the ends", "The galvanometer works only there"],
       "Errors in reading l matter less when both l and 100 - l are large.",
       "মিটার-ব্রিজে সাম্যবিন্দু তারের মাঝামাঝি থাকা পছন্দনীয় কেন?", ["প্রান্ত-সংশোধনসহ শতকরা ত্রুটি কমে", "সেখানে তার মোটা", "প্রান্তে প্রবাহ শূন্য", "গ্যালভানোমিটার কেবল সেখানে কাজ করে"],
       "l আর 100 - l দুটোই বড় হলে l পড়ার ত্রুটি কম গুরুত্বপূর্ণ।"),
    _q("A block of mass M on a frictionless incline of angle θ is connected by a string over a pulley to a hanging mass m. The acceleration of the system is:", ["(mg − Mg sinθ)/(M + m)", "(M − m)g/(M + m)", "g sinθ", "(m + M sinθ)g/(M + m)"],
       "Net force = mg − Mg sinθ (if m drives the system); total inertia = M + m. If mg < Mg sinθ, system slides up the incline.",
       "ঘর্ষণহীন θ কোণের ঢালে M ভরের ব্লক একটা তারের মাধ্যমে ঝুলন্ত m ভরের সাথে সংযুক্ত। ব্যবস্থার ত্বরণ:", ["(mg − Mg sinθ)/(M + m)", "(M − m)g/(M + m)", "g sinθ", "(m + M sinθ)g/(M + m)"],
       "নেট বল = mg − Mg sinθ; মোট জড়তা = M + m।"),
    _q("A disc of radius R rolls without slipping on a flat surface. The speed of the topmost point is:", ["2v, where v is the speed of the centre (velocity = v + ωR = v + v = 2v at top)", "v", "√2 v", "Zero"],
       "Rolling: v_contact = 0, v_centre = v = ωR, v_top = 2v. The contact point is momentarily at rest.",
       "R ব্যাসার্ধের একটা ডিস্ক না-পিছলিয়ে সমতলে গড়ায়। সর্বোচ্চ বিন্দুর বেগ:", ["2v, যেখানে v কেন্দ্রের বেগ", "v", "√2 v", "শূন্য"],
       "গড়ানো: স্পর্শবিন্দু v = 0, কেন্দ্র v = ωR, উপরের বিন্দু 2v।"),
    _q("A particle moves in a circle with speed v. Its kinetic energy is constant, but its momentum is:", ["Changing (direction changes even though magnitude is constant — centripetal acceleration)", "Also constant", "Zero", "Increasing"],
       "p = mv: magnitude constant, but direction constantly changes. Rate of change of momentum = centripetal force = mv²/r.",
       "একটা কণা v বেগে বৃত্তাকারে চলে। গতিশক্তি ধ্রুবক, কিন্তু ভরবেগ:", ["পরিবর্তনশীল (মান ধ্রুবক হলেও দিক পরিবর্তিত হয় — অভিকেন্দ্র ত্বরণ)", "ধ্রুবক", "শূন্য", "বর্ধমান"],
       "p = mv: মান ধ্রুবক কিন্তু দিক ক্রমাগত পরিবর্তিত। ভরবেগের পরিবর্তনের হার = mv²/r।"),
    _q("A ball is thrown vertically upward from height h with velocity u. The total time to reach the ground (below launch point) is:", ["[u + √(u² + 2gh)] / g (using s = ut − ½gt²; take positive downward)", "[u − √(u² + 2gh)] / g", "u/g only", "2u/g"],
       "Take upward positive: 0 = h + ut − ½gt² → solve quadratic → larger root = total time.",
       "একটা বল উচ্চতা h থেকে u বেগে সরাসরি উপরে ছোড়া হয়। মাটিতে পৌঁছানোর মোট সময়:", ["[u + √(u² + 2gh)] / g", "[u − √(u² + 2gh)] / g", "শুধু u/g", "2u/g"],
       "উপরে ধনাত্মক: 0 = h + ut − ½gt² → দ্বিঘাত সমীকরণ → বড় মূল = মোট সময়।"),
    _q("Two identical springs each of spring constant k are connected in parallel to a mass m. The angular frequency of oscillation is:", ["√(2k/m) — parallel springs: k_eff = k + k = 2k", "√(k/m)", "√(k/2m)", "√(4k/m)"],
       "Parallel: k_eff = k₁ + k₂. Series: 1/k_eff = 1/k₁ + 1/k₂. Parallel is stiffer (higher ω).",
       "প্রতিটি k স্প্রিং ধ্রুবকের দুটো সমান স্প্রিং সমান্তরালে m ভরের সাথে সংযুক্ত। কৌণিক কম্পাঙ্ক:", ["√(2k/m) — সমান্তরালে: k_eff = 2k", "√(k/m)", "√(k/2m)", "√(4k/m)"],
       "সমান্তরালে: k_eff = k₁ + k₂। শ্রেণিতে: 1/k_eff = 1/k₁ + 1/k₂।"),
    _q("A solid cylinder of mass M and radius R rolls down an incline (angle θ) from rest through height h. The speed at the bottom is:", ["√(4gh/3) — KE_total = ½Mv² + ½Iω² = ½Mv² + ¼Mv² = ¾Mv² = Mgh → v = √(4gh/3)", "√(2gh)", "√(gh)", "√(2gh/3)"],
       "I_cyl = ½MR²; ω = v/R; total KE = ¾Mv². For a hoop: I = MR², total KE = Mv², v = √(gh) — slower than cylinder.",
       "M ভর R ব্যাসার্ধের একটা কঠিন সিলিন্ডার θ ঢাল দিয়ে h উচ্চতা থেকে গড়ায়। তলায় বেগ:", ["√(4gh/3) — মোট KE = ¾Mv² = Mgh → v = √(4gh/3)", "√(2gh)", "√(gh)", "√(2gh/3)"],
       "I_সিলিন্ডার = ½MR²; মোট KE = ¾Mv²।"),
    _q("The escape velocity from a planet of mass M and radius R is:", ["v_e = √(2GM/R) — set KE = GPE: ½mv² = GMm/R", "v_e = √(GM/R)", "v_e = 2GM/R", "v_e = √(gR)"],
       "At surface g = GM/R², so v_e = √(2gR). For Earth: v_e ≈ 11.2 km/s.",
       "M ভর R ব্যাসার্ধের গ্রহ থেকে মুক্তিবেগ:", ["v_e = √(2GM/R) — KE = GPE: ½mv² = GMm/R", "v_e = √(GM/R)", "v_e = 2GM/R", "v_e = √(gR)"],
       "ভূপৃষ্ঠে g = GM/R², তাই v_e = √(2gR)। পৃথিবীর জন্য v_e ≈ 11.2 km/s।"),
    _q("In a Carnot engine, heat Q₁ is absorbed at temperature T₁ and heat Q₂ is rejected at T₂ (T₁ > T₂). The efficiency η is:", ["η = 1 − T₂/T₁ = (T₁ − T₂)/T₁ (maximum possible efficiency for any engine between these temperatures)", "η = T₁/T₂", "η = Q₂/Q₁", "η = 1 − Q₁/Q₂"],
       "Carnot: Q₁/T₁ = Q₂/T₂ → η = 1 − Q₂/Q₁ = 1 − T₂/T₁. No real engine can exceed Carnot efficiency.",
       "কার্নো ইঞ্জিনে T₁ তাপমাত্রায় Q₁ তাপ শোষিত, T₂-তে Q₂ বর্জিত। দক্ষতা:", ["η = 1 − T₂/T₁ = (T₁ − T₂)/T₁ (এই তাপমাত্রার মধ্যে সর্বোচ্চ সম্ভব দক্ষতা)", "η = T₁/T₂", "η = Q₂/Q₁", "η = 1 − Q₁/Q₂"],
       "কার্নো: Q₁/T₁ = Q₂/T₂ → η = 1 − T₂/T₁। কোনো বাস্তব ইঞ্জিন কার্নো দক্ষতা অতিক্রম করতে পারে না।"),
    _q("For a monatomic ideal gas undergoing adiabatic process, PVγ = constant where γ = ?", ["5/3 (monatomic: f = 3 translational degrees; Cv = 3R/2; Cp = 5R/2; γ = Cp/Cv = 5/3)", "7/5", "4/3", "3/2"],
       "Diatomic: γ = 7/5 = 1.4 (5 degrees). Triatomic linear: γ = 9/7. Bridge material gas cylinders — adiabatic filling.",
       "একপরমাণুক আদর্শ গ্যাসের অ্যাডিয়াব্যাটিক প্রক্রিয়ায় PVγ = ধ্রুবক, γ = ?", ["5/3 (একপরমাণুক: f = 3; Cv = 3R/2; Cp = 5R/2; γ = 5/3)", "7/5", "4/3", "3/2"],
       "দ্বিপরমাণুক: γ = 7/5। ত্রিপরমাণুক রৈখিক: γ = 9/7।"),
    _q("A capillary tube of radius r is dipped in a liquid of surface tension T and contact angle θ. The height of rise is:", ["h = 2T cosθ / (ρgr)", "h = T / (ρgr)", "h = 2T / (ρgr²)", "h = T cosθ / (ρgr)"],
       "Excess pressure at meniscus = 2T cosθ/r; balancing: ρgh = 2T cosθ/r. Mercury (θ > 90°): h < 0 (depression).",
       "r ব্যাসার্ধের কৈশিক নলে T পৃষ্ঠ টান ও θ স্পর্শ কোণ বিশিষ্ট তরলে উচ্চতা:", ["h = 2T cosθ / (ρgr)", "h = T / (ρgr)", "h = 2T / (ρgr²)", "h = T cosθ / (ρgr)"],
       "মেনিস্কাসে অতিরিক্ত চাপ = 2T cosθ/r; সাম্যে ρgh = 2T cosθ/r। পারদে (θ > 90°): h < 0।"),
    _q("Two point charges Q and −Q are separated by distance d. The electric field at the midpoint between them is:", ["4kQ/d² directed from +Q to −Q (fields from both charges add in same direction at midpoint)", "Zero", "2kQ/d²", "kQ/d²"],
       "At midpoint: field from +Q points away (→), field from −Q also points toward −Q (→). Both in same direction.",
       "Q ও −Q আধান d দূরত্বে। মধ্যবিন্দুতে বৈদ্যুতিক ক্ষেত্র:", ["+Q থেকে −Q অভিমুখে 4kQ/d² (উভয় আধানের ক্ষেত্র একই দিকে যোগ হয়)", "শূন্য", "2kQ/d²", "kQ/d²"],
       "মধ্যবিন্দুতে: +Q থেকে ক্ষেত্র দূরে, −Q থেকেও সেদিকে। উভয় একই দিকে।"),
    _q("A parallel plate capacitor with plate area A and separation d is filled with dielectric constant K. Its capacitance is:", ["KAε₀/d (K times the vacuum capacitance)", "Aε₀/d", "KA/d", "ε₀A/(Kd)"],
       "Inserting a dielectric increases capacitance by K. Charge stored = KAε₀V/d. Energy = ½CV² = ½KAε₀V²/d.",
       "ক্ষেত্রফল A, ব্যবধান d, ডাইইলেকট্রিক ধ্রুবক K সহ সমান্তরাল পাত ধারকের ধারকত্ব:", ["KAε₀/d (শূন্যের ধারকত্বের K গুণ)", "Aε₀/d", "KA/d", "ε₀A/(Kd)"],
       "ডাইইলেকট্রিক প্রবেশে ধারকত্ব K গুণ বাড়ে।"),
    _q("In a series RLC circuit, the resonant frequency f₀ and the Q-factor are:", ["f₀ = 1/(2π√(LC)), Q = (1/R)√(L/C) — high Q means narrow, sharp resonance", "f₀ = 1/(2π√RC)", "Q = R/√(LC)", "f₀ = R/(2πL)"],
       "At resonance: Z = R (minimum impedance), current maximum. Bridge monitoring uses RLC resonant sensors.",
       "শ্রেণি RLC বর্তনীতে অনুনাদ কম্পাঙ্ক ও Q-ফ্যাক্টর:", ["f₀ = 1/(2π√(LC)), Q = (1/R)√(L/C) — উচ্চ Q মানে সরু, তীক্ষ্ণ অনুনাদ", "f₀ = 1/(2π√RC)", "Q = R/√(LC)", "f₀ = R/(2πL)"],
       "অনুনাদে: Z = R (সর্বনিম্ন impedance), প্রবাহ সর্বোচ্চ।"),
    _q("A solenoid of n turns/length carrying current I produces magnetic field B at its centre. If n is doubled and I is halved:", ["B stays the same (B = μ₀nI; 2n × I/2 = nI)", "B doubles", "B halves", "B quadruples"],
       "B = μ₀nI inside an ideal solenoid. B is uniform along axis and zero outside (in the ideal approximation).",
       "n মোড়/দৈর্ঘ্য I প্রবাহ বহনকারী সোলিনয়েডে B। n দ্বিগুণ ও I অর্ধেক করলে:", ["B অপরিবর্তিত (B = μ₀nI; 2n × I/2 = nI)", "B দ্বিগুণ", "B অর্ধেক", "B চারগুণ"],
       "আদর্শ সোলিনয়েডের ভেতর B = μ₀nI। বাইরে শূন্য।"),
    _q("Lenz's law is a consequence of:", ["Conservation of energy (induced EMF opposes the change causing it, preventing free energy generation)", "Faraday's law only", "Ampere's law", "Gauss's law for magnetism"],
       "If induced current aided the change, it would create more flux → more current → runaway: impossible.",
       "লেনজের সূত্র কিসের পরিণতি?", ["শক্তির সংরক্ষণ (আবিষ্ট EMF তার কারণ পরিবর্তনকে বাধা দেয়, বিনামূল্যে শক্তি উৎপাদন রোধ)", "শুধু ফ্যারাডের সূত্র", "অ্যাম্পিয়ারের সূত্র", "চুম্বকত্বের জন্য গাউসের সূত্র"],
       "আবিষ্ট প্রবাহ পরিবর্তন সাহায্য করলে আরও ফ্লাক্স → আরও প্রবাহ → অনিয়ন্ত্রিত: অসম্ভব।"),
    _q("The de Broglie wavelength of a particle with kinetic energy E is:", ["λ = h/√(2mE) — p = √(2mE), λ = h/p", "λ = h/E", "λ = h√(2mE)", "λ = E/h"],
       "For an electron accelerated through potential V: E = eV; λ = h/√(2meV). At 100 eV: λ ≈ 0.12 nm.",
       "গতিশক্তি E বিশিষ্ট কণার ডি ব্রগলি তরঙ্গদৈর্ঘ্য:", ["λ = h/√(2mE) — p = √(2mE)", "λ = h/E", "λ = h√(2mE)", "λ = E/h"],
       "V বিভব দিয়ে ত্বরিত ইলেকট্রনে E = eV; λ = h/√(2meV)।"),
    _q("In Young's double-slit experiment, the fringe width β = λD/d. If the experiment is done in water (refractive index n), the fringe width becomes:", ["β/n (wavelength in water = λ/n; fringe width decreases)", "nβ", "β unchanged", "β/n²"],
       "λ_medium = λ/n, so β_medium = λD/(nd) = β/n. The fringes shrink in a denser medium.",
       "ইয়ংয়ের দ্বি-চির পরীক্ষায় β = λD/d। জলে (প্রতিসরণাঙ্ক n) করলে ব্যান্ড প্রস্থ:", ["β/n (জলে তরঙ্গদৈর্ঘ্য = λ/n; ব্যান্ড প্রস্থ কমে)", "nβ", "অপরিবর্তিত β", "β/n²"],
       "λ_মাধ্যম = λ/n, তাই β_মাধ্যম = β/n। ঘন মাধ্যমে ব্যান্ড সংকুচিত।"),
    _q("For total internal reflection to occur when a ray travels from medium 1 (refractive index n₁) to medium 2 (n₂ < n₁), the angle of incidence must:", ["Exceed the critical angle θc = arcsin(n₂/n₁)", "Be less than θc", "Equal exactly 90°", "Be 45°"],
       "At θc, refracted ray grazes the interface (θr = 90°). Above θc: all light is reflected internally.",
       "n₁ থেকে n₂ < n₁ মাধ্যমে সম্পূর্ণ অভ্যন্তরীণ প্রতিফলনের জন্য আপতন কোণ:", ["সংকট কোণ θc = arcsin(n₂/n₁) অতিক্রম করতে হবে", "θc-এর চেয়ে কম", "ঠিক 90°", "45°"],
       "θc-তে প্রতিসৃত রশ্মি তল ঘেঁষে যায় (θr = 90°)। θc-এর উপরে সব আলো প্রতিফলিত।"),
    _q("The work function of a metal is 2 eV. The maximum KE of photoelectrons emitted when light of frequency f = 8×10¹⁴ Hz shines on it is:", ["1.31 eV ≈ 1.3 eV (hf = 6.626×10⁻³⁴ × 8×10¹⁴ ≈ 3.31 eV; KE = 3.31 − 2 = 1.31 eV)", "2 eV", "3.31 eV", "0 eV (below threshold)"],
       "Einstein: KE_max = hf − φ. Threshold: f₀ = φ/h = 2×1.6×10⁻¹⁹/(6.626×10⁻³⁴) ≈ 4.83×10¹⁴ Hz < 8×10¹⁴ Hz.",
       "কার্যফাংশন 2 eV। 8×10¹⁴ Hz আলোয় ফটোইলেকট্রনের সর্বোচ্চ KE:", ["≈ 1.3 eV (hf ≈ 3.31 eV; KE = 3.31 − 2 = 1.31 eV)", "2 eV", "3.31 eV", "0 eV (দহন কোণের নিচে)"],
       "আইনস্টাইন: KE_max = hf − φ। সীমা কম্পাঙ্ক ≈ 4.83×10¹⁴ Hz < 8×10¹⁴ Hz।"),
    _q("In the Bohr model, the radius of the nth orbit of hydrogen is:", ["rₙ = n²a₀ where a₀ = 0.529 Å (Bohr radius)", "rₙ = na₀", "rₙ = n²/a₀", "rₙ = a₀/n²"],
       "Energy: Eₙ = −13.6/n² eV. As n increases, radius grows as n² and energy increases (becomes less negative).",
       "বোর মডেলে হাইড্রোজেনের n-তম কক্ষপথের ব্যাসার্ধ:", ["rₙ = n²a₀ যেখানে a₀ = 0.529 Å (বোর ব্যাসার্ধ)", "rₙ = na₀", "rₙ = n²/a₀", "rₙ = a₀/n²"],
       "শক্তি: Eₙ = −13.6/n² eV। n বাড়লে ব্যাসার্ধ n² হারে বাড়ে।"),
    _q("A radioactive nucleus emits an α-particle. The mass number A and atomic number Z change by:", ["A decreases by 4, Z decreases by 2 (⁴₂He emitted)", "A decreases by 1, Z unchanged", "A unchanged, Z decreases by 1", "A decreases by 4, Z increases by 2"],
       "α: ⁴₂He. β⁻: A unchanged, Z +1 (n → p + e⁻ + ν̄). β⁺: A unchanged, Z −1. γ: neither changes.",
       "তেজস্ক্রিয় নিউক্লিয়াস α-কণা নির্গত করে। A ও Z-এর পরিবর্তন:", ["A 4 কমে, Z 2 কমে (⁴₂He নির্গত)", "A 1 কমে, Z অপরিবর্তিত", "A অপরিবর্তিত, Z 1 কমে", "A 4 কমে, Z 2 বাড়ে"],
       "α: ⁴₂He। β⁻: A অপরিবর্তিত, Z +1। β⁺: Z −1। γ: কোনো পরিবর্তন নেই।"),
    _q("The binding energy per nucleon is maximum for:", ["⁵⁶Fe (iron-56) — most stable nucleus; ~ 8.8 MeV/nucleon", "Hydrogen (1H)", "Uranium-235", "Helium-4"],
       "Light nuclei gain energy by fusion; heavy nuclei gain energy by fission — both move toward iron's maximum BE/nucleon.",
       "নিউক্লিয়ন-প্রতি বন্ধন শক্তি সর্বোচ্চ:", ["⁵⁶Fe (আয়রন-56) — সবচেয়ে স্থিতিশীল নিউক্লিয়াস; ~ 8.8 MeV/নিউক্লিয়ন", "হাইড্রোজেন", "ইউরেনিয়াম-235", "হিলিয়াম-4"],
       "হালকা নিউক্লিয়াস ফিউশনে; ভারী নিউক্লিয়াস ফিশনে — উভয় লোহার সর্বোচ্চ BE/নিউক্লিয়নের দিকে।"),
    _q("In the photoelectric effect, if the intensity of light is doubled (keeping frequency constant):", ["The number of photoelectrons doubles but their maximum KE remains the same", "Maximum KE doubles", "Both number and KE double", "No change in either"],
       "Intensity ∝ photon flux (number/sec). Each photon gives one electron with same energy hf − φ. More photons → more electrons.",
       "ফটোইলেকট্রিক প্রভাবে আলোর তীব্রতা দ্বিগুণ (কম্পাঙ্ক স্থির):", ["ফটোইলেকট্রনের সংখ্যা দ্বিগুণ কিন্তু সর্বোচ্চ KE অপরিবর্তিত", "সর্বোচ্চ KE দ্বিগুণ", "সংখ্যা ও KE উভয় দ্বিগুণ", "কোনো পরিবর্তন নেই"],
       "তীব্রতা ∝ ফোটন প্রবাহ। প্রতিটি ফোটন একটি ইলেকট্রন দেয় একই শক্তিতে।"),
    _q("The image formed by a convex mirror is always:", ["Virtual, erect, and diminished — used as rear-view mirrors", "Real, inverted, magnified", "Real, erect, same size", "Virtual, inverted, magnified"],
       "Convex mirror: f > 0; object always between F and infinity; image always between focus and pole — virtual.",
       "উত্তল দর্পণে সর্বদা প্রতিবিম্ব:", ["অভাসী, সোজা এবং ক্ষুদ্রীকৃত — রিয়ার-ভিউ দর্পণ হিসেবে ব্যবহার", "বাস্তব, উল্টো, বর্ধিত", "বাস্তব, সোজা, সমান আকার", "অভাসী, উল্টো, বর্ধিত"],
       "উত্তল দর্পণ: প্রতিবিম্ব সবসময় ফোকাস ও মেরুর মধ্যে — অভাসী।"),
    _q("A wire of resistance R is stretched to double its length. Its new resistance is:", ["4R (length doubles → resistance doubles; area halves → resistance doubles again: total ×4)", "2R", "R/2", "R/4"],
       "ρ = constant. R = ρL/A. Volume = LA = constant → A' = A/2. R' = ρ(2L)/(A/2) = 4R.",
       "R রোধের তার দ্বিগুণ দীর্ঘ করা হলে নতুন রোধ:", ["4R (দৈর্ঘ্য দ্বিগুণ → রোধ দ্বিগুণ; ক্ষেত্রফল অর্ধেক → আবার দ্বিগুণ: মোট ×4)", "2R", "R/2", "R/4"],
       "আয়তন ধ্রুবক। R = ρL/A; A' = A/2; R' = 4R।"),
    _q("An ideal transformer with 200 turns in the primary and 50 turns in the secondary is connected to a 240 V AC supply. The secondary voltage and the turns ratio are:", ["60 V; turns ratio = 200:50 = 4:1 (step-down transformer)", "960 V", "120 V", "480 V"],
       "Vs/Vp = Ns/Np → Vs = 240 × 50/200 = 60 V. Current: Is/Ip = Np/Ns = 4 (step-down increases current).",
       "200 প্রাথমিক ও 50 গৌণ মোড়ের আদর্শ ট্রান্সফর্মার 240 V AC-তে। গৌণ বিভব:", ["60 V; মোড় অনুপাত = 4:1 (অপনত ট্রান্সফর্মার)", "960 V", "120 V", "480 V"],
       "Vs = 240 × 50/200 = 60 V। প্রবাহ: Is/Ip = 4।"),
    _q("Two wires carry currents I₁ and I₂ in the same direction. They:", ["Attract each other (parallel currents attract; antiparallel repel)", "Repel each other", "Have no force between them", "Attract only if I₁ = I₂"],
       "Force per length: F/L = μ₀I₁I₂/(2πd). Same direction: attractive. This is the basis of the ampere definition.",
       "দুটো তার একই দিকে I₁ ও I₂ প্রবাহ বহন করে:", ["একে অপরকে আকর্ষণ করে (সমান্তরাল প্রবাহ আকর্ষণ; বিপরীত বিকর্ষণ)", "একে অপরকে বিকর্ষণ করে", "মধ্যে কোনো বল নেই", "শুধু I₁ = I₂ হলে আকর্ষণ"],
       "প্রতি দৈর্ঘ্যে বল: F/L = μ₀I₁I₂/(2πd)। সমান্তরাল: আকর্ষণ।"),
    _q("The displacement current was introduced by Maxwell to fix an inconsistency in Ampere's law. It equals:", ["ε₀ × dΦE/dt (rate of change of electric flux through any surface in a capacitor gap)", "μ₀ × dB/dt", "dq/dt (regular conduction current only)", "ε₀E"],
       "Maxwell: ∇×B = μ₀J + μ₀ε₀ ∂E/∂t. Displacement current ensures continuity between capacitor plates.",
       "ম্যাক্সওয়েল অ্যাম্পিয়ারের সূত্রের অসঙ্গতি দূর করতে সরণ প্রবাহ চালু করেন। এটা সমান:", ["ε₀ × dΦE/dt (ধারকের ফাঁকে যেকোনো তলের মধ্য দিয়ে বৈদ্যুতিক ফ্লাক্সের পরিবর্তনের হার)", "μ₀ × dB/dt", "শুধু dq/dt (নিয়মিত পরিবাহী প্রবাহ)", "ε₀E"],
       "ম্যাক্সওয়েল: ∇×B = μ₀J + μ₀ε₀ ∂E/∂t। সরণ প্রবাহ ধারকের পাতের মধ্যে ধারাবাহিকতা নিশ্চিত করে।"),
    _q("In Compton scattering of X-rays by free electrons, the wavelength of the scattered photon:", ["Increases (Δλ = h(1 − cosφ)/(mₑc) — photon loses energy to recoiling electron)", "Decreases", "Stays the same", "Depends only on the target material"],
       "Compton wavelength of electron λc = h/(mₑc) ≈ 2.43 pm. Maximum Δλ = 2λc (φ = 180° back-scatter).",
       "ইলেকট্রন দ্বারা X-রশ্মির কম্পটন বিক্ষেপণে বিক্ষিপ্ত ফোটনের তরঙ্গদৈর্ঘ্য:", ["বাড়ে (Δλ = h(1 − cosφ)/(mₑc) — ফোটন ইলেকট্রনে শক্তি হারায়)", "কমে", "একই থাকে", "শুধু লক্ষ্য উপাদানের উপর নির্ভর করে"],
       "ইলেকট্রনের কম্পটন তরঙ্গদৈর্ঘ্য λc ≈ 2.43 pm। সর্বোচ্চ Δλ = 2λc (180° পশ্চাৎ-বিক্ষেপণে)।"),
    _q("Standing waves form in a closed pipe of length L. The fundamental frequency and overtone sequence are:", ["f₁ = v/(4L); only odd harmonics (f₁, 3f₁, 5f₁, ...)", "f₁ = v/(2L); all harmonics", "f₁ = v/(4L); all harmonics", "f₁ = v/(8L)"],
       "Closed pipe: node at closed end, antinode at open end. Open pipe: f₁ = v/(2L), all harmonics.",
       "L দীর্ঘ বন্ধ পাইপে স্থির তরঙ্গ। মৌলিক কম্পাঙ্ক ও উপসুর ক্রম:", ["f₁ = v/(4L); শুধু বিজোড় হারমোনিক (f₁, 3f₁, 5f₁, ...)", "f₁ = v/(2L); সব হারমোনিক", "f₁ = v/(4L); সব হারমোনিক", "f₁ = v/(8L)"],
       "বন্ধ পাইপ: বন্ধ প্রান্তে নোড, খোলা প্রান্তে অ্যান্টিনোড। খোলা পাইপ: f₁ = v/(2L), সব হারমোনিক।"),
    _q("A charged particle enters a magnetic field B perpendicular to its velocity v. The radius of circular motion is:", ["r = mv/(qB) — from qvB = mv²/r → r = mv/(qB)", "r = qB/(mv)", "r = mv²/(qB)", "r = m/(qBv)"],
       "Time period T = 2πm/(qB) — independent of speed! Cyclotrons exploit this: same T for all speeds.",
       "চার্জিত কণা বেগের লম্বভাবে B চৌম্বক ক্ষেত্রে প্রবেশ করে। বৃত্তাকার গতির ব্যাসার্ধ:", ["r = mv/(qB) — qvB = mv²/r থেকে", "r = qB/(mv)", "r = mv²/(qB)", "r = m/(qBv)"],
       "পর্যায় T = 2πm/(qB) — বেগ থেকে স্বাধীন! সাইক্লোট্রন এটা কাজে লাগায়।"),
    _q("Gauss's law in electrostatics states that the total electric flux through a closed surface equals:", ["Q_enclosed/ε₀ (the net charge inside divided by permittivity of free space)", "Zero always", "Q_enclosed × ε₀", "E × surface area"],
       "∮E·dA = Q_enc/ε₀. Used to find E for symmetric charge distributions (spheres, cylinders, planes).",
       "স্থির বিদ্যুতে গাউসের সূত্র বলে বন্ধ তলের মধ্য দিয়ে মোট বৈদ্যুতিক ফ্লাক্স:", ["Q_ভেতরে/ε₀ (ভেতরের নেট আধান ভ্যাকুয়াম পার্মিটিভিটি দিয়ে ভাগ)", "সবসময় শূন্য", "Q_ভেতরে × ε₀", "E × তলের ক্ষেত্রফল"],
       "∮E·dA = Q_enc/ε₀। গোলক, সিলিন্ডার, সমতল বিতরণে E বের করতে ব্যবহার।"),
    _q("A ball thrown horizontally from height H hits the floor. The time of flight and horizontal range depend on:", ["Time = √(2H/g) (independent of horizontal speed); range = v₀√(2H/g)", "Both depend on v₀", "Neither depends on H", "Time depends on v₀"],
       "Horizontal and vertical motions are independent. Vertical: H = ½gt² → t = √(2H/g). Range = v₀ × t.",
       "H উচ্চতা থেকে অনুভূমিকভাবে ছোড়া বল মাটিতে পড়ে। ওড়ার সময় ও অনুভূমিক দূরত্ব:", ["সময় = √(2H/g) (অনুভূমিক বেগ থেকে স্বাধীন); দূরত্ব = v₀√(2H/g)", "উভয় v₀-এর উপর নির্ভর", "কোনোটাই H-এর উপর নির্ভর করে না", "সময় v₀-এর উপর নির্ভর করে"],
       "অনুভূমিক ও উল্লম্ব গতি স্বাধীন। উল্লম্ব: H = ½gt² → t = √(2H/g)।"),
    _q("A thin rod of length L and mass M pivoted at one end is released from horizontal. Its angular acceleration at the horizontal position is:", ["3g/(2L) (torque = Mg×L/2; I_end = ML²/3; α = τ/I = (MgL/2)/(ML²/3) = 3g/(2L))", "g/L", "g/(2L)", "2g/L"],
       "As the rod swings down, α decreases (moment arm decreases) but ω increases.",
       "L দীর্ঘ M ভরের সরু দণ্ড এক প্রান্তে কব্জায় অনুভূমিক থেকে ছাড়া হয়। কৌণিক ত্বরণ:", ["3g/(2L) (টর্ক = Mg×L/2; I_প্রান্ত = ML²/3; α = 3g/(2L))", "g/L", "g/(2L)", "2g/L"],
       "দণ্ড দুলতে থাকলে α কমে (মোমেন্ট আর্ম কমে) কিন্তু ω বাড়ে।"),
    _q("In a p-type semiconductor, the majority carriers are:", ["Holes (created by doping with acceptor atoms like boron into silicon)", "Electrons", "Protons", "Neutrons"],
       "n-type: donor impurity (P, As) → extra electrons. p-type: acceptor impurity (B, Al) → holes.",
       "p-টাইপ সেমিকন্ডাক্টরে সংখ্যাগরিষ্ঠ বাহক:", ["হোল (বোরনের মতো গ্রহণকারী অপদ্রব্য দোপিং থেকে তৈরি)", "ইলেকট্রন", "প্রোটন", "নিউট্রন"],
       "n-টাইপ: দাতা অপদ্রব্য (P, As) → অতিরিক্ত ইলেকট্রন। p-টাইপ: গ্রহণকারী (B, Al) → হোল।"),
    _q("The resolving power of a microscope is determined by the Rayleigh criterion. Two points are just resolved when the angular separation equals:", ["1.22λ/D (first diffraction minimum of one point falls on central maximum of the other)", "λ/D", "λ/(2D)", "2λ/D"],
       "Higher NA (numerical aperture) → better resolution. Oil-immersion lenses reduce λ effectively.",
       "মাইক্রোস্কোপের বিভেদ ক্ষমতা রেলিগ মানদণ্ড দ্বারা নির্ধারিত। দুটো বিন্দু ঠিক বিভেদ হয় যখন কৌণিক বিচ্ছেদ:", ["1.22λ/D (একটি বিন্দুর প্রথম বিচ্ছুরণ ন্যূনতম অন্যটির কেন্দ্রীয় সর্বোচ্চে পড়ে)", "λ/D", "λ/(2D)", "2λ/D"],
       "বেশি NA → ভালো রেজোলিউশন। তেল-নিমজ্জন লেন্স কার্যকরভাবে λ কমায়।"),
    _q("The Stefan-Boltzmann law states that the power radiated by a black body is:", ["P = σAT⁴ — proportional to the fourth power of absolute temperature T", "P = σAT²", "P = σT", "P = σA/T⁴"],
       "σ = 5.67×10⁻⁸ W/m²K⁴. If T doubles, power increases by 2⁴ = 16. Bridge surface temperature monitoring.",
       "স্টেফান-বোল্টজম্যান সূত্র: কৃষ্ণবস্তু থেকে বিকিরিত শক্তি:", ["P = σAT⁴ — পরম তাপমাত্রার চতুর্থ ঘাতের সমানুপাতিক", "P = σAT²", "P = σT", "P = σA/T⁴"],
       "T দ্বিগুণ হলে শক্তি 2⁴ = 16 গুণ। σ = 5.67×10⁻⁸ W/m²K⁴।"),
    _q("What is the physical significance of the area enclosed by the P-V diagram of a thermodynamic cycle?", ["It equals the net work done by the gas per cycle (W = ∮P dV)", "It equals the net heat absorbed", "It equals the internal energy change", "It has no physical significance"],
       "For clockwise cycle: net work > 0 (engine). Counter-clockwise: net work < 0 (refrigerator/pump).",
       "তাপগতিবিদ্যা চক্রের P-V রেখাচিত্রের অন্তর্ভুক্ত ক্ষেত্রফলের ভৌত তাৎপর্য:", ["প্রতি চক্রে গ্যাস দ্বারা নিট কার্য (W = ∮P dV)-এর সমান", "নিট শোষিত তাপের সমান", "অভ্যন্তরীণ শক্তি পরিবর্তনের সমান", "কোনো ভৌত তাৎপর্য নেই"],
       "ঘড়ির কাঁটার দিকে চক্র: নিট কার্য > 0 (ইঞ্জিন)। বিপরীত: < 0 (রেফ্রিজারেটর)।"),
    _q("A satellite in circular orbit of radius r around a planet (mass M) has speed:", ["v = √(GM/r) — derived from gravitational force = centripetal: GMm/r² = mv²/r", "v = √(2GM/r)", "v = √(GM/r²)", "v = GMm/r"],
       "Total energy = −GMm/(2r). PE = −GMm/r. KE = GMm/(2r). Energy increases (less negative) as r increases.",
       "M ভরের গ্রহকে r ব্যাসার্ধে বৃত্তাকার কক্ষপথে উপগ্রহের বেগ:", ["v = √(GM/r) — মাধ্যাকর্ষণ = অভিকেন্দ্র: GMm/r² = mv²/r", "v = √(2GM/r)", "v = √(GM/r²)", "v = GMm/r"],
       "মোট শক্তি = −GMm/(2r)।"),
    _q("A proton and an electron are placed between the plates of a capacitor (uniform field E). The ratio of their accelerations is:", ["aₑ/aₚ = mₚ/mₑ ≈ 1836 (electron accelerates 1836× faster since F = qE is equal but masses differ)", "1:1", "mₑ/mₚ", "They accelerate in the same direction"],
       "Both have charge e but mp/me ≈ 1836. F = eE for both; a = F/m. Electron is much lighter → much greater acceleration.",
       "ধারকের পাতের মধ্যে (সুষম ক্ষেত্র E) প্রোটন ও ইলেকট্রন। ত্বরণের অনুপাত:", ["aₑ/aₚ = mₚ/mₑ ≈ 1836 (ইলেকট্রন 1836 গুণ দ্রুত ত্বরান্বিত)", "1:1", "mₑ/mₚ", "একই দিকে ত্বরণ"],
       "উভয়ের চার্জ e কিন্তু mp/me ≈ 1836।"),
    _q("The refractive index of glass (n = 1.5) with respect to air. The critical angle for total internal reflection is:", ["θc = arcsin(1/1.5) = arcsin(0.667) ≈ 41.8°", "45°", "30°", "60°"],
       "sinθc = 1/n → θc = arcsin(2/3) ≈ 41.8°. Optical fibres use TIR: glass (n ≈ 1.5) + cladding (n ≈ 1.46).",
       "বায়ুর সাপেক্ষে কাচের প্রতিসরণাঙ্ক (n = 1.5)। সম্পূর্ণ অভ্যন্তরীণ প্রতিফলনের সংকট কোণ:", ["θc = arcsin(1/1.5) ≈ 41.8°", "45°", "30°", "60°"],
       "sinθc = 1/n → θc ≈ 41.8°। অপটিক্যাল ফাইবার TIR ব্যবহার করে।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
