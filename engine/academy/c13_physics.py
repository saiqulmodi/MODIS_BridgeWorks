"""NIT level - Physics (JEE Main standard): units and errors, kinematics, laws of motion, work and
energy, rotation, gravitation, properties of matter, heat and thermodynamics, oscillations and
waves, electrostatics, current electricity, magnetism, induction and AC, optics, modern physics and
semiconductors. Numerical items show the formula and the working; g = 10 m/s² unless stated."""
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


SIN = {120: 0.866, 150: 0.5, 15: 0.2588, 30: 0.5, 37: 0.6, 45: 0.7071, 53: 0.8, 60: 0.866, 75: 0.9659, 90: 1.0}


# ---------------------------------------------------------------- kinematics and laws of motion
def proj_range(u, th):
    r = u * u * SIN[2 * th] / 10
    return _n(f"A ball is projected at {u} m/s at {th}° above the horizontal. Taking g = 10 m/s², what is its horizontal range on level ground?",
              f"একটা বলকে অনুভূমিকের সঙ্গে {th}° কোণে {u} m/s বেগে ছোড়া হল। g = 10 m/s² ধরে সমতল মাটিতে এর অনুভূমিক পাল্লা কত?", r,
              f"R = u² sin 2θ ÷ g = {u}² x sin {2 * th}° ÷ 10 = {_f(_c(r))} m. Angles θ and 90° - θ give the same range.",
              f"R = u² sin 2θ ÷ g = {u}² x sin {2 * th}° ÷ 10 = {_f(_c(r))} m। θ আর 90° - θ কোণে পাল্লা একই হয়।",
              (u * u * SIN[th] / 10, r / 2, u * u / 10), " m")


def proj_h(u, th):
    h = (u * SIN[th]) ** 2 / 20
    return _n(f"A stone is thrown at {u} m/s at {th}° to the horizontal. Taking g = 10 m/s², what maximum height does it reach?",
              f"একটা পাথর অনুভূমিকের সঙ্গে {th}° কোণে {u} m/s বেগে ছোড়া হল। g = 10 m/s² ধরে এটা সর্বোচ্চ কত উচ্চতায় ওঠে?", h,
              f"H = u² sin²θ ÷ 2g = ({u} x {SIN[th]:g})² ÷ 20 = {_f(_c(h))} m.",
              f"সর্বোচ্চ উচ্চতা H = u² sin²θ ÷ 2g = ({u} x {SIN[th]:g})² ÷ 20 = {_f(_c(h))} m।",
              (u * u * SIN[th] / 20, h * 2, u * u / 20), " m")


def proj_t(u, th):
    t = 2 * u * SIN[th] / 10
    return _n(f"A projectile is launched at {u} m/s at {th}° above level ground. Taking g = 10 m/s², how long is it in the air?",
              f"সমতল মাটি থেকে {th}° কোণে {u} m/s বেগে একটা প্রক্ষিপ্ত বস্তু ছোড়া হল। g = 10 m/s² ধরে এটা কতক্ষণ বাতাসে থাকে?", t,
              f"T = 2u sin θ ÷ g = 2 x {u} x {SIN[th]:g} ÷ 10 = {_f(_c(t))} s.",
              f"উড্ডয়নকাল T = 2u sin θ ÷ g = 2 x {u} x {SIN[th]:g} ÷ 10 = {_f(_c(t))} s।",
              (u * SIN[th] / 10, 2 * u / 10, t * 2), " s")


def river(d, v, u):
    x = u * d / v
    return _n(f"A river {d} m wide flows at {u} m/s. A swimmer who swims at {v} m/s in still water heads straight across, perpendicular to the bank. How far downstream does the swimmer land?",
              f"{d} m চওড়া একটা নদী {u} m/s বেগে বইছে। স্থির জলে {v} m/s বেগে সাঁতার কাটা একজন পাড়ের লম্বভাবে সোজা পার হতে চায়। স্রোতের দিকে সে কত দূরে গিয়ে পৌঁছায়?", x,
              f"Crossing time t = d ÷ v = {d} ÷ {v} = {_f(_c(d / v))} s; drift = u t = {u} x {_f(_c(d / v))} = {_f(_c(x))} m.",
              f"পার হওয়ার সময় t = d ÷ v = {d} ÷ {v} = {_f(_c(d / v))} s; সরণ = u t = {u} x {_f(_c(d / v))} = {_f(_c(x))} m।",
              (d * v / u, d, x / 2), " m")


def atwood_a(m1, m2):
    a = (m1 - m2) * 10 / (m1 + m2)
    return _n(f"Blocks of {m1} kg and {m2} kg hang from a light string over a frictionless pulley. Taking g = 10 m/s², what is their acceleration?",
              f"হালকা সুতোয় বাঁধা {m1} kg ও {m2} kg-এর দুটো ব্লক একটা ঘর্ষণহীন কপিকলের উপর দিয়ে ঝুলছে। g = 10 m/s² ধরে তাদের ত্বরণ কত?", a,
              f"a = (m₁ - m₂)g ÷ (m₁ + m₂) = ({m1} - {m2}) x 10 ÷ {m1 + m2} = {_f(_c(a))} m/s².",
              f"a = (m₁ - m₂)g ÷ (m₁ + m₂) = ({m1} - {m2}) x 10 ÷ {m1 + m2} = {_f(_c(a))} m/s²।",
              ((m1 - m2) * 10 / m1, 10, (m1 - m2) * 10 / m2), " m/s²")


def atwood_t(m1, m2):
    t = 2 * m1 * m2 * 10 / (m1 + m2)
    return _n(f"In an Atwood machine with masses {m1} kg and {m2} kg on a light string, what is the string tension? (g = 10 m/s²)",
              f"হালকা সুতোয় {m1} kg ও {m2} kg ভরের একটা অ্যাটউড যন্ত্রে সুতোর টান কত? (g = 10 m/s²)", t,
              f"T = 2m₁m₂g ÷ (m₁ + m₂) = 2 x {m1} x {m2} x 10 ÷ {m1 + m2} = {_f(_c(t))} N - between the two weights.",
              f"T = 2m₁m₂g ÷ (m₁ + m₂) = 2 x {m1} x {m2} x 10 ÷ {m1 + m2} = {_f(_c(t))} N - দুই ওজনের মাঝামাঝি।",
              (m1 * 10, m2 * 10, (m1 + m2) * 10), " N")


def incline(mu):
    a = 10 * (0.6 - 0.8 * mu)
    return _n(f"A block slides down a rough 37° incline (sin 37° = 0.6, cos 37° = 0.8) with kinetic friction coefficient {mu}. Taking g = 10 m/s², what is its acceleration?",
              f"একটা ব্লক 37° খসখসে নত তল বেয়ে নামছে (sin 37° = 0.6, cos 37° = 0.8), গতীয় ঘর্ষণাঙ্ক {mu}। g = 10 m/s² ধরে এর ত্বরণ কত?", a,
              f"a = g(sin θ - μ cos θ) = 10 x (0.6 - {mu} x 0.8) = {_f(_c(a))} m/s².",
              f"ত্বরণ a = g(sin θ - μ cos θ) = 10 x (0.6 - {mu} x 0.8) = {_f(_c(a))} m/s²।",
              (6, 10 * (0.8 - 0.6 * mu), 10 * (0.6 + 0.8 * mu)), " m/s²")


def banking(r, th, tan_txt, tan):
    v = math.sqrt(r * 10 * tan)
    return _n(f"A curve of radius {r} m is banked at {th}° (tan θ = {tan_txt}). At what speed can a car take it with no friction needed? (g = 10 m/s²)",
              f"{r} m ব্যাসার্ধের একটা বাঁক {th}° কোণে ঢালু করা (tan θ = {tan_txt})। ঘর্ষণ ছাড়াই গাড়ি কোন বেগে বাঁকটা নিতে পারে? (g = 10 m/s²)", v,
              f"tan θ = v² ÷ rg, so v = √(rg tan θ) = √({r} x 10 x {tan_txt}) = {_f(_c(v))} m/s.",
              f"tan θ = v² ÷ rg, তাই v = √(rg tan θ) = √({r} x 10 x {tan_txt}) = {_f(_c(v))} m/s।",
              (math.sqrt(r * 10), r * 10 * tan / 10, v / 2), " m/s")


def spring_x(m, v, k):
    x = v * math.sqrt(m / k)
    return _n(f"A {m} kg block moving at {v} m/s on a smooth floor hits a spring of stiffness {k} N/m. What is the maximum compression?",
              f"মসৃণ মেঝেতে {v} m/s বেগে চলা {m} kg-এর একটা ব্লক {k} N/m দৃঢ়তার একটা স্প্রিংয়ে ধাক্কা দিল। সর্বোচ্চ সংকোচন কত?", x,
              f"½mv² = ½kx², so x = v√(m ÷ k) = {v} x √({m} ÷ {k}) = {_f(_c(x))} m.",
              f"½mv² = ½kx², তাই x = v√(m ÷ k) = {v} x √({m} ÷ {k}) = {_f(_c(x))} m।",
              (m * v * v / k, v * m / k, x / 2), " m")


def perfectly_inelastic(m1, u1, m2, ask_loss):
    v = m1 * u1 / (m1 + m2)
    loss = 0.5 * m1 * u1 * u1 - 0.5 * (m1 + m2) * v * v
    if not ask_loss:
        return _n(f"A {m1} kg trolley moving at {u1} m/s hits and sticks to a stationary {m2} kg trolley. What is their common velocity?",
                  f"{u1} m/s বেগে চলা {m1} kg-এর একটা ট্রলি স্থির {m2} kg-এর ট্রলিতে ধাক্কা দিয়ে আটকে গেল। তাদের সাধারণ বেগ কত?", v,
                  f"Momentum is conserved: v = m₁u₁ ÷ (m₁ + m₂) = {m1} x {u1} ÷ {m1 + m2} = {_f(_c(v))} m/s.",
                  f"ভরবেগ সংরক্ষিত: v = m₁u₁ ÷ (m₁ + m₂) = {m1} x {u1} ÷ {m1 + m2} = {_f(_c(v))} m/s।",
                  (u1 / 2, m2 * u1 / (m1 + m2), u1), " m/s")
    return _n(f"A {m1} kg ball at {u1} m/s collides with a stationary {m2} kg ball and they stick together. How much kinetic energy is lost?",
              f"{u1} m/s বেগের {m1} kg-এর একটা বল স্থির {m2} kg-এর বলে ধাক্কা দিয়ে জুড়ে গেল। কত গতিশক্তি হারায়?", loss,
              f"v = {m1} x {u1} ÷ {m1 + m2} = {_f(_c(v))} m/s; loss = ½ x {m1} x {u1}² - ½ x {m1 + m2} x {_f(_c(v))}² = {_f(_c(loss))} J.",
              f"v = {m1} x {u1} ÷ {m1 + m2} = {_f(_c(v))} m/s; ক্ষতি = ½ x {m1} x {u1}² - ½ x {m1 + m2} x {_f(_c(v))}² = {_f(_c(loss))} J।",
              (0.5 * m1 * u1 * u1, 0.5 * (m1 + m2) * v * v, loss / 2), " J")


SHAPES = {"ring": ("a thin ring", "একটা পাতলা আংটি", 1.0), "disc": ("a solid disc", "একটা নিরেট চাকতি", 0.5),
          "sphere": ("a solid sphere", "একটা নিরেট গোলক", 0.4)}


def rolling(shape, h):
    en, bn, k = SHAPES[shape]
    v = math.sqrt(2 * 10 * h / (1 + k))
    return _n(f"{en[0].upper() + en[1:]} rolls without slipping from rest down a slope of vertical height {h} m. What is its speed at the bottom? (g = 10 m/s²)",
              f"{bn} স্থির অবস্থা থেকে না পিছলে {h} m খাড়া উচ্চতার ঢাল বেয়ে গড়িয়ে নামে। নিচে এর বেগ কত? (g = 10 m/s²)", v,
              f"mgh = ½mv²(1 + k²/R²) with k²/R² = {k:g}: v = √(2gh ÷ {1 + k:g}) = {_f(_c(v))} m/s - slower than sliding, √(2gh) = {_f(_c(math.sqrt(20 * h)))} m/s.",
              f"mgh = ½mv²(1 + k²/R²), k²/R² = {k:g}: v = √(2gh ÷ {1 + k:g}) = {_f(_c(v))} m/s - পিছলে নামার √(2gh) = {_f(_c(math.sqrt(20 * h)))} m/s-এর চেয়ে কম।",
              (math.sqrt(20 * h), math.sqrt(10 * h), v / 2), " m/s")


def skater(i1, w1, i2):
    w2 = i1 * w1 / i2
    return _n(f"A skater spins at {w1:g} rev/s with moment of inertia {i1} kg m². Pulling the arms in cuts it to {i2} kg m². What is the new spin rate?",
              f"একজন স্কেটার {w1:g} ঘূর্ণন/s হারে ঘুরছে, জড়তা-ভ্রামক {i1} kg m²। হাত গুটিয়ে নিলে তা কমে {i2} kg m² হয়। নতুন ঘূর্ণন-হার কত?", w2,
              f"No outside torque, so I₁ω₁ = I₂ω₂: ω₂ = {i1} x {w1:g} ÷ {i2} = {_f(_c(w2))} rev/s.",
              f"বাইরের টর্ক নেই, তাই I₁ω₁ = I₂ω₂: ω₂ = {i1} x {w1:g} ÷ {i2} = {_f(_c(w2))} ঘূর্ণন/s।",
              (w1 * i2 / i1, w1, w2 * w2 / w1), " rev/s", " ঘূর্ণন/s")


# ---------------------------------------------------------------- gravitation and matter
def g_height(en, bn, factor, how_en, how_bn):
    g = 10 * factor
    return _n(f"Taking g = 10 m/s² at the surface, what is g {en}?",
              f"পৃষ্ঠে g = 10 m/s² ধরলে {bn} g কত?", g, how_en, how_bn,
              (10 * (1 - (1 - factor) / 2), 10, 5), " m/s²")


def kepler(t, k):
    t2 = t * k ** 1.5
    return _n(f"A satellite orbits a planet with period {t} h. Another satellite orbits the same planet at {k} times the orbital radius. What is its period?",
              f"একটা উপগ্রহ একটা গ্রহকে {t} ঘণ্টা পর্যায়কালে প্রদক্ষিণ করে। একই গ্রহকে {k} গুণ কক্ষ-ব্যাসার্ধে আরেকটা উপগ্রহ ঘোরে। তার পর্যায়কাল কত?", t2,
              f"Kepler's third law T² ∝ r³: T₂ = {t} x {k}^1.5 = {_f(_c(t2))} h.",
              f"কেপলারের তৃতীয় সূত্র T² ∝ r³: T₂ = {t} x {k}^1.5 = {_f(_c(t2))} ঘণ্টা।",
              (t * k, t * k * k, t * math.sqrt(k)), " h", " ঘণ্টা")


def escape(v_orb):
    v = v_orb * math.sqrt(2)
    return _n(f"A satellite skimming just above a planet's surface orbits at {v_orb} km/s. What is the escape speed from that surface?",
              f"একটা গ্রহের পৃষ্ঠের ঠিক উপর দিয়ে একটা উপগ্রহ {v_orb} km/s বেগে ঘোরে। ওই পৃষ্ঠ থেকে মুক্তিবেগ কত?", v,
              f"v_orbit = √(GM/R), v_escape = √(2GM/R) = √2 x {v_orb} = {_f(_c(v))} km/s.",
              f"কক্ষবেগ = √(GM/R), মুক্তিবেগ = √(2GM/R) = √2 x {v_orb} = {_f(_c(v))} km/s।",
              (v_orb * 2, v_orb, v_orb * 1.5), " km/s")


def stretch(f, l, a):
    d = f * l / (a * 200)
    return _n(f"A steel wire (Y = 2 x 10¹¹ Pa) {l} m long with cross-section {a} mm² carries a load of {f} N. By how much does it stretch?",
              f"{l} m লম্বা, {a} mm² প্রস্থচ্ছেদের একটা ইস্পাতের তার (Y = 2 x 10¹¹ Pa) {f} N বোঝা বয়। এটা কতটা লম্বা হয়?", d,
              f"ΔL = FL ÷ AY = {f} x {l} ÷ ({a} x 10⁻⁶ x 2 x 10¹¹) m = {_f(_c(d))} mm.",
              f"ΔL = FL ÷ AY = {f} x {l} ÷ ({a} x 10⁻⁶ x 2 x 10¹¹) m = {_f(_c(d))} mm।",
              (d * 10, d / 2, f * l / a / 100), " mm")


def depth_p(h):
    p = 1 + h / 10
    return _n(f"What is the total pressure {h} m below the surface of a lake? (Atmospheric pressure 1 atm = 10⁵ Pa, water density 1000 kg/m³, g = 10 m/s²)",
              f"একটা হ্রদের জলতলের {h} m নিচে মোট চাপ কত? (বায়ুমণ্ডলীয় চাপ 1 atm = 10⁵ Pa, জলের ঘনত্ব 1000 kg/m³, g = 10 m/s²)", p,
              f"P = P₀ + ρgh = 10⁵ + 1000 x 10 x {h} = {_f(_c(p))} x 10⁵ Pa = {_f(_c(p))} atm. Every 10 m of water adds 1 atm.",
              f"P = P₀ + ρgh = 10⁵ + 1000 x 10 x {h} = {_f(_c(p))} x 10⁵ Pa = {_f(_c(p))} atm। প্রতি 10 m জল 1 atm যোগ করে।",
              (h / 10, p * 10, 1 + h), " atm", " atm (বায়ুমণ্ডল)")


def terminal(v, k):
    r = v * k * k
    return _n(f"A tiny oil drop falls through air at a terminal speed of {v:g} mm/s. What is the terminal speed of a drop of the same oil with {k} times the radius? (Stokes' law)",
              f"একটা ছোট্ট তেলের ফোঁটা বাতাসে {v:g} mm/s প্রান্তিক বেগে পড়ে। একই তেলের {k} গুণ ব্যাসার্ধের ফোঁটার প্রান্তিক বেগ কত? (স্টোকসের সূত্র)", r,
              f"Terminal speed ∝ r²: {v:g} x {k}² = {_f(_c(r))} mm/s.",
              f"প্রান্তিক বেগ ∝ r²: {v:g} x {k}² = {_f(_c(r))} mm/s।",
              (v * k, v * k ** 3, v * math.sqrt(k)), " mm/s")


def pipe(v, k):
    r = v * k * k
    return _n(f"Water flows at {v:g} m/s in a pipe that narrows to 1/{k} of its diameter. What is the speed in the narrow part?",
              f"একটা নলে জল {v:g} m/s বেগে বইছে, নলটা সরু হয়ে ব্যাসের 1/{k} হয়ে যায়। সরু অংশে বেগ কত?", r,
              f"A₁v₁ = A₂v₂ and area ∝ d², so v₂ = {v:g} x {k}² = {_f(_c(r))} m/s.",
              f"A₁v₁ = A₂v₂ আর ক্ষেত্রফল ∝ d², তাই v₂ = {v:g} x {k}² = {_f(_c(r))} m/s।",
              (v * k, v / k, v * k ** 3), " m/s")


# ---------------------------------------------------------------- heat and thermodynamics
def mixing(m1, t1, m2, t2):
    t = (m1 * t1 + m2 * t2) / (m1 + m2)
    return _n(f"{m1} kg of water at {t1}°C is mixed with {m2} kg of water at {t2}°C in an insulated vessel. What is the final temperature?",
              f"তাপ-নিরোধী পাত্রে {t1}°C-এর {m1} kg জল {t2}°C-এর {m2} kg জলের সঙ্গে মেশানো হল। শেষ তাপমাত্রা কত?", t,
              f"Heat lost = heat gained: T = ({m1} x {t1} + {m2} x {t2}) ÷ {m1 + m2} = {_f(_c(t))}°C.",
              f"হারানো তাপ = পাওয়া তাপ: T = ({m1} x {t1} + {m2} x {t2}) ÷ {m1 + m2} = {_f(_c(t))}°C।",
              ((t1 + t2) / 2, t1 - t2, t + 5), "°C")


def melt(m):
    q = 336 * m
    return _n(f"How much heat is needed to melt {m:g} kg of ice already at 0°C? (Latent heat of fusion 336 kJ/kg)",
              f"0°C-এ থাকা {m:g} kg বরফ গলাতে কত তাপ লাগে? (গলনের লীন তাপ 336 kJ/kg)", q,
              f"Q = mL = {m:g} x 336 = {_f(_c(q))} kJ; the temperature stays at 0°C while it melts.",
              f"Q = mL = {m:g} x 336 = {_f(_c(q))} kJ; গলার সময় তাপমাত্রা 0°C-এই থাকে।",
              (4.2 * m, q / 2, 336 / m), " kJ")


def expand(l, dt):
    d = l * 12e-6 * dt * 1000
    return _n(f"A steel bridge deck {l} m long warms by {dt}°C. By how much does it lengthen? (α for steel = 12 x 10⁻⁶ /°C)",
              f"{l} m লম্বা একটা ইস্পাতের সেতু-পাটাতন {dt}°C গরম হল। এটা কতটা লম্বা হয়? (ইস্পাতের α = 12 x 10⁻⁶ /°C)", d,
              f"ΔL = LαΔT = {l} x 12 x 10⁻⁶ x {dt} m = {_f(_c(d))} mm - expansion joints must allow this.",
              f"ΔL = LαΔT = {l} x 12 x 10⁻⁶ x {dt} m = {_f(_c(d))} mm - প্রসারণ-জোড়কে এটুকু জায়গা দিতে হয়।",
              (d / 10, d * 3, d * 10), " mm")


def carnot(t1, t2):
    e = (1 - t2 / t1) * 100
    return _n(f"A Carnot engine works between {t1} K and {t2} K. What is its efficiency?",
              f"একটা কার্নো ইঞ্জিন {t1} K আর {t2} K-এর মধ্যে চলে। এর দক্ষতা কত?", e,
              f"η = 1 - T₂/T₁ = 1 - {t2}/{t1} = {_f(_c(e))}%. No engine between these temperatures can do better.",
              f"η = 1 - T₂/T₁ = 1 - {t2}/{t1} = {_f(_c(e))}%। এই দুই তাপমাত্রার মধ্যে কোনো ইঞ্জিন এর চেয়ে ভালো হতে পারে না।",
              (t2 / t1 * 100, (1 - t1 / (t1 + t2)) * 100, e / 2), "%")


def isobaric(p, v1, v2):
    w = p * (v2 - v1)
    return _n(f"A gas at a constant {p} kPa expands from {v1} L to {v2} L. How much work does it do?",
              f"স্থির {p} kPa চাপে একটা গ্যাস {v1} L থেকে {v2} L-এ প্রসারিত হল। এটা কত কাজ করে?", w,
              f"W = PΔV = {p} x 10³ Pa x ({v2} - {v1}) x 10⁻³ m³ = {_f(w)} J.",
              f"W = PΔV = {p} x 10³ Pa x ({v2} - {v1}) x 10⁻³ m³ = {_f(w)} J।",
              (p * v2, p * (v2 + v1), w * 1000), " J")


def vrms(v, t1, t2):
    r = v * math.sqrt(t2 / t1)
    return _n(f"The rms speed of a gas's molecules is {v} m/s at {t1} K. What is it at {t2} K?",
              f"{t1} K-এ একটা গ্যাসের অণুর গড়-বর্গমূল বেগ {v} m/s। {t2} K-এ এটা কত?", r,
              f"v_rms ∝ √T: {v} x √({t2}/{t1}) = {_f(_c(r))} m/s.",
              f"গড়-বর্গমূল বেগ ∝ √T: {v} x √({t2}/{t1}) = {_f(_c(r))} m/s।",
              (v * t2 / t1, v * (t2 / t1) ** 2, v + t2 - t1), " m/s")


def vrms_gas(v):
    r = v / 4
    return _n(f"Hydrogen molecules (M = 2 g/mol) have an rms speed of {v:,} m/s at some temperature. What is the rms speed of oxygen molecules (M = 32 g/mol) at the same temperature?",
              f"কোনো তাপমাত্রায় হাইড্রোজেন অণুর (M = 2 g/mol) গড়-বর্গমূল বেগ {v:,} m/s। একই তাপমাত্রায় অক্সিজেন অণুর (M = 32 g/mol) গড়-বর্গমূল বেগ কত?", r,
              f"v_rms ∝ 1/√M: {v:,} ÷ √16 = {_f(_c(r))} m/s.",
              f"গড়-বর্গমূল বেগ ∝ 1/√M: {v:,} ÷ √16 = {_f(_c(r))} m/s।",
              (v / 16, v / 2, v / 8), " m/s")


# ---------------------------------------------------------------- oscillations and waves
def shm_mass(t, k):
    r = t * math.sqrt(k)
    return _n(f"A mass on a spring oscillates with period {t:g} s. If the mass is made {k:g} times larger, what is the new period?",
              f"স্প্রিংয়ে ঝোলানো একটা ভর {t:g} s পর্যায়কালে দোলে। ভর {k:g} গুণ করলে নতুন পর্যায়কাল কত?", r,
              f"T = 2π√(m/k) ∝ √m: {t:g} x √{k:g} = {_f(_c(r))} s.",
              f"T = 2π√(m/k) ∝ √m: {t:g} x √{k:g} = {_f(_c(r))} s।",
              (t * k, t / math.sqrt(k), t), " s")


def pendulum(t):
    l = t * t / 4
    return _n(f"What length of simple pendulum has a period of {t:g} s? (Take g = 10 m/s² and π² = 10)",
              f"কত দৈর্ঘ্যের সরল দোলকের পর্যায়কাল {t:g} s? (g = 10 m/s² আর π² = 10 ধরো)", l,
              f"T = 2π√(L/g), so L = gT² ÷ 4π² = 10 x {t:g}² ÷ 40 = {_f(_c(l))} m.",
              f"T = 2π√(L/g), তাই L = gT² ÷ 4π² = 10 x {t:g}² ÷ 40 = {_f(_c(l))} m।",
              (t / 4, t * t, t * t / 2), " m")


def shm_v(a, w):
    v = a * w
    return _n(f"A particle in SHM has amplitude {a:g} m and angular frequency {w} rad/s. What is its maximum speed?",
              f"সরল দোলগতিতে একটা কণার বিস্তার {a:g} m আর কৌণিক কম্পাঙ্ক {w} rad/s। এর সর্বোচ্চ বেগ কত?", v,
              f"v_max = Aω = {a:g} x {w} = {_f(_c(v))} m/s, reached at the centre.",
              f"v_max = Aω = {a:g} x {w} = {_f(_c(v))} m/s, কেন্দ্রে পৌঁছায়।",
              (a * w * w, a / w, v / 2), " m/s")


def shm_a(a, w):
    acc = a * w * w
    return _n(f"A particle in SHM has amplitude {a:g} m and angular frequency {w} rad/s. What is its maximum acceleration?",
              f"সরল দোলগতিতে একটা কণার বিস্তার {a:g} m আর কৌণিক কম্পাঙ্ক {w} rad/s। এর সর্বোচ্চ ত্বরণ কত?", acc,
              f"a_max = Aω² = {a:g} x {w}² = {_f(_c(acc))} m/s², reached at the extreme positions.",
              f"a_max = Aω² = {a:g} x {w}² = {_f(_c(acc))} m/s², প্রান্তবিন্দুতে পৌঁছায়।",
              (a * w, acc / 2, a * w ** 3), " m/s²")


def string_v(t, mu):
    v = math.sqrt(t / mu)
    return _n(f"A string with linear mass density {mu:g} kg/m is stretched with a tension of {t} N. What is the speed of transverse waves on it?",
              f"{mu:g} kg/m রৈখিক ভর-ঘনত্বের একটা তার {t} N টানে টানটান। এর উপর তির্যক তরঙ্গের বেগ কত?", v,
              f"v = √(T/μ) = √({t} ÷ {mu:g}) = {_f(_c(v))} m/s.",
              f"v = √(T/μ) = √({t} ÷ {mu:g}) = {_f(_c(v))} m/s।",
              (t / mu, t * mu, v * 2), " m/s")


def string_f(v, l):
    f = v / (2 * l)
    return _n(f"Waves travel at {v} m/s on a guitar string {l:g} m long fixed at both ends. What is its fundamental frequency?",
              f"দুই প্রান্তে আটকানো {l:g} m লম্বা গিটারের তারে তরঙ্গ {v} m/s বেগে চলে। এর মূল কম্পাঙ্ক কত?", f,
              f"f = v ÷ 2L = {v} ÷ {_f(_c(2 * l))} = {_f(_c(f))} Hz.",
              f"f = v ÷ 2L = {v} ÷ {_f(_c(2 * l))} = {_f(_c(f))} Hz।",
              (v / l, v / (4 * l), f * 3), " Hz")


def organ(l, closed):
    f = 340 / ((4 if closed else 2) * l)
    kind_en, kind_bn = ("closed at one end", "এক প্রান্ত বন্ধ") if closed else ("open at both ends", "দুই প্রান্ত খোলা")
    return _n(f"What is the fundamental frequency of an organ pipe {l:g} m long, {kind_en}? (Speed of sound 340 m/s)",
              f"{l:g} m লম্বা, {kind_bn} একটা অর্গান-নলের মূল কম্পাঙ্ক কত? (শব্দের বেগ 340 m/s)", f,
              f"f = v ÷ {'4L' if closed else '2L'} = 340 ÷ {_f(_c((4 if closed else 2) * l))} = {_f(_c(f))} Hz.",
              f"f = v ÷ {'4L' if closed else '2L'} = 340 ÷ {_f(_c((4 if closed else 2) * l))} = {_f(_c(f))} Hz।",
              (340 / ((2 if closed else 4) * l), 340 / l, f * 3), " Hz")


def beats(fa, b1, b2):
    fb = fa - b1
    return _n(f"Fork A of {fa} Hz gives {b1} beats/s with fork B. Loading B with a little wax makes it {b2} beats/s. What was B's frequency?",
              f"{fa} Hz-এর স্বরশলাকা A, স্বরশলাকা B-এর সঙ্গে সেকেন্ডে {b1}টি স্বরকম্প দেয়। B-তে একটু মোম লাগালে তা সেকেন্ডে {b2}টি হয়। B-এর কম্পাঙ্ক কত ছিল?", fb,
              f"B is {fa} ± {b1}. Wax lowers B's frequency; the beats rose, so B was below A: {fa} - {b1} = {fb} Hz.",
              f"B হয় {fa} ± {b1}। মোম B-এর কম্পাঙ্ক কমায়; স্বরকম্প বেড়েছে, তাই B ছিল A-র নিচে: {fa} - {b1} = {fb} Hz।",
              (fa + b1, fa - b2, fa + b2), " Hz")


def doppler(f, vs):
    r = f * 340 / (340 - vs)
    return _n(f"An ambulance siren of {f} Hz approaches a standing listener at {vs} m/s. What frequency is heard? (Speed of sound 340 m/s)",
              f"{f} Hz-এর অ্যাম্বুলেন্সের সাইরেন {vs} m/s বেগে দাঁড়িয়ে থাকা শ্রোতার দিকে আসছে। শ্রোতা কোন কম্পাঙ্ক শোনে? (শব্দের বেগ 340 m/s)", r,
              f"f' = f v ÷ (v - vs) = {f} x 340 ÷ {340 - vs} = {_f(_c(r))} Hz - higher while approaching.",
              f"f' = f v ÷ (v - vs) = {f} x 340 ÷ {340 - vs} = {_f(_c(r))} Hz - কাছে আসার সময় বেশি।",
              (f * (340 - vs) / 340, f * 340 / (340 + vs), f + vs), " Hz")


# ---------------------------------------------------------------- electrostatics
def coulomb(q1, q2, r):
    f = 9e9 * q1 * q2 * 1e-12 / (r * r)
    return _n(f"What is the force between charges of {q1} μC and {q2} μC placed {r:g} m apart in air? (k = 9 x 10⁹ N m²/C²)",
              f"বাতাসে {r:g} m দূরে রাখা {q1} μC আর {q2} μC আধানের মধ্যে বল কত? (k = 9 x 10⁹ N m²/C²)", f,
              f"F = kq₁q₂ ÷ r² = 9 x 10⁹ x {q1} x 10⁻⁶ x {q2} x 10⁻⁶ ÷ {r:g}² = {_f(_c(f))} N.",
              f"F = kq₁q₂ ÷ r² = 9 x 10⁹ x {q1} x 10⁻⁶ x {q2} x 10⁻⁶ ÷ {r:g}² = {_f(_c(f))} N।",
              (f * r, f / 2, f * 4), " N")


def efield(q, r):
    e = int(round(9e9 * q * 1e-6 / (r * r)))
    return _n(f"What is the electric field {r:g} m from a point charge of {q} μC?",
              f"{q} μC বিন্দু-আধান থেকে {r:g} m দূরে তড়িৎক্ষেত্র কত?", e,
              f"E = kq ÷ r² = 9 x 10⁹ x {q} x 10⁻⁶ ÷ {r:g}² = {e:,} N/C.",
              f"E = kq ÷ r² = 9 x 10⁹ x {q} x 10⁻⁶ ÷ {r:g}² = {e:,} N/C।",
              (int(round(e * r)), e * 2, e // 2), " N/C")


def epot(q, r):
    v = int(round(9e9 * q * 1e-6 / r))
    return _n(f"What is the electric potential {r:g} m from a point charge of {q} μC?",
              f"{q} μC বিন্দু-আধান থেকে {r:g} m দূরে তড়িৎ-বিভব কত?", v,
              f"V = kq ÷ r = 9 x 10⁹ x {q} x 10⁻⁶ ÷ {r:g} = {v:,} V.",
              f"V = kq ÷ r = 9 x 10⁹ x {q} x 10⁻⁶ ÷ {r:g} = {v:,} V।",
              (int(round(v / r)), v * 2, v // 2), " V")


def plate_cap(a, d):
    c = 8.85 * a / d
    return _n(f"A parallel-plate capacitor has plates of area {a:g} m² separated by {d:g} mm of air. What is its capacitance? (ε₀ = 8.85 x 10⁻¹² F/m)",
              f"একটা সমান্তরাল-পাত ধারকের পাতের ক্ষেত্রফল {a:g} m², মাঝে {d:g} mm বাতাস। এর ধারকত্ব কত? (ε₀ = 8.85 x 10⁻¹² F/m)", c,
              f"C = ε₀A ÷ d = 8.85 x 10⁻¹² x {a:g} ÷ ({d:g} x 10⁻³) F = {_f(_c(c))} nF.",
              f"C = ε₀A ÷ d = 8.85 x 10⁻¹² x {a:g} ÷ ({d:g} x 10⁻³) F = {_f(_c(c))} nF।",
              (8.85 * a * d, c * 10, c / 2), " nF")


def cap_series(c1, c2):
    c = c1 * c2 / (c1 + c2)
    return _n(f"Capacitors of {c1} μF and {c2} μF are joined in series. What is the equivalent capacitance?",
              f"{c1} μF আর {c2} μF-এর দুটো ধারক শ্রেণিতে যুক্ত। তুল্য ধারকত্ব কত?", c,
              f"1/C = 1/{c1} + 1/{c2}, so C = {c1} x {c2} ÷ {c1 + c2} = {_f(_c(c))} μF - less than either.",
              f"1/C = 1/{c1} + 1/{c2}, তাই C = {c1} x {c2} ÷ {c1 + c2} = {_f(_c(c))} μF - যেকোনোটার চেয়ে কম।",
              (c1 + c2, (c1 + c2) / 2, abs(c1 - c2) + 0.5), " μF")


def cap_energy(c, v):
    u = 0.5 * c * 1e-6 * v * v
    return _n(f"How much energy is stored in a {c} μF capacitor charged to {v} V?",
              f"{v} V পর্যন্ত আহিত {c} μF ধারকে কত শক্তি জমা থাকে?", u,
              f"U = ½CV² = ½ x {c} x 10⁻⁶ x {v}² = {_f(_c(u))} J.",
              f"U = ½CV² = ½ x {c} x 10⁻⁶ x {v}² = {_f(_c(u))} J।",
              (c * 1e-6 * v * v, u * 4, c * 1e-6 * v), " J")


def cap_share(c1, v1, c2):
    v = c1 * v1 / (c1 + c2)
    return _n(f"A {c1} μF capacitor charged to {v1} V is connected across an uncharged {c2} μF capacitor. What is the common voltage?",
              f"{v1} V-এ আহিত একটা {c1} μF ধারককে একটা আধানহীন {c2} μF ধারকের সঙ্গে যুক্ত করা হল। সাধারণ বিভব কত?", v,
              f"Charge is shared, not lost: V = C₁V₁ ÷ (C₁ + C₂) = {c1} x {v1} ÷ {c1 + c2} = {_f(_c(v))} V.",
              f"আধান ভাগ হয়, হারায় না: V = C₁V₁ ÷ (C₁ + C₂) = {c1} x {v1} ÷ {c1 + c2} = {_f(_c(v))} V।",
              (v1 / 2, c2 * v1 / (c1 + c2), v1), " V")


# ---------------------------------------------------------------- current electricity
def cell_i(e, r, big_r):
    i = e / (big_r + r)
    return _n(f"A cell of emf {e} V and internal resistance {r:g} Ω drives current through a {big_r:g} Ω resistor. What is the current?",
              f"{e} V তড়িচ্চালক বল আর {r:g} Ω অভ্যন্তরীণ রোধের একটা কোষ {big_r:g} Ω রোধের মধ্য দিয়ে প্রবাহ পাঠায়। প্রবাহ কত?", i,
              f"I = E ÷ (R + r) = {e} ÷ ({big_r:g} + {r:g}) = {_f(_c(i))} A.",
              f"I = E ÷ (R + r) = {e} ÷ ({big_r:g} + {r:g}) = {_f(_c(i))} A।",
              (e / big_r, e / r, i / 2), " A")


def cell_v(e, r, big_r):
    v = e * big_r / (big_r + r)
    return _n(f"A battery of emf {e} V and internal resistance {r:g} Ω is connected to a {big_r:g} Ω load. What is the terminal voltage?",
              f"{e} V তড়িচ্চালক বল আর {r:g} Ω অভ্যন্তরীণ রোধের একটা ব্যাটারি {big_r:g} Ω বোঝার সঙ্গে যুক্ত। প্রান্তীয় বিভব কত?", v,
              f"I = {e} ÷ {_f(_c(big_r + r))} = {_f(_c(e / (big_r + r)))} A; V = E - Ir = {_f(_c(v))} V.",
              f"I = {e} ÷ {_f(_c(big_r + r))} = {_f(_c(e / (big_r + r)))} A; V = E - Ir = {_f(_c(v))} V।",
              (e, e - r, v / 2), " V")


def parallel(*rs):
    r = 1 / sum(1 / x for x in rs)
    txt = ", ".join(f"{x} Ω" for x in rs)
    return _n(f"Resistors of {txt} are connected in parallel. What is the equivalent resistance?",
              f"{txt} রোধগুলো সমান্তরালে যুক্ত। তুল্য রোধ কত?", r,
              f"1/R = {' + '.join(f'1/{x}' for x in rs)}, so R = {_f(_c(r))} Ω - smaller than the smallest.",
              f"1/R = {' + '.join(f'1/{x}' for x in rs)}, তাই R = {_f(_c(r))} Ω - সবচেয়ে ছোটটার চেয়েও কম।",
              (sum(rs), sum(rs) / len(rs), min(rs) + 1), " Ω")


def bulb(p, v_rated, v):
    r = p * (v / v_rated) ** 2
    return _n(f"A bulb rated {p} W at {v_rated} V is run on {v} V. What power does it now draw (resistance unchanged)?",
              f"{v_rated} V-এ {p} W চিহ্নিত একটা বাল্ব {v} V-এ চালানো হল। এখন এটা কত ক্ষমতা নেয় (রোধ অপরিবর্তিত)?", r,
              f"R = V² ÷ P stays fixed, so P' = P(V'/V)² = {p} x ({v}/{v_rated})² = {_f(_c(r))} W.",
              f"R = V² ÷ P স্থির থাকে, তাই P' = P(V'/V)² = {p} x ({v}/{v_rated})² = {_f(_c(r))} W।",
              (p * v / v_rated, p, p * (v / v_rated) ** 3), " W")


def meter_bridge(r, l):
    x = r * l / (100 - l)
    return _n(f"In a metre bridge, the balance point is {l} cm from the end of the unknown resistance X, with a {r} Ω standard resistor in the other gap. What is X?",
              f"একটা মিটার-ব্রিজে অজানা রোধ X-এর প্রান্ত থেকে {l} cm দূরে সাম্যবিন্দু, অন্য ফাঁকে {r} Ω প্রমাণ রোধ। X কত?", x,
              f"X ÷ R = l ÷ (100 - l): X = {r} x {l} ÷ {100 - l} = {_f(_c(x))} Ω.",
              f"X ÷ R = l ÷ (100 - l): X = {r} x {l} ÷ {100 - l} = {_f(_c(x))} Ω।",
              (r * (100 - l) / l, r * l / 100, r), " Ω")


def potentiometer(e1, l1, l2):
    e2 = e1 * l2 / l1
    return _n(f"On a potentiometer, a {e1:g} V cell balances at {l1} cm and a second cell balances at {l2} cm. What is the second cell's emf?",
              f"একটা বিভবমাপকে {e1:g} V-এর কোষ {l1} cm-এ আর দ্বিতীয় কোষ {l2} cm-এ সাম্য দেয়। দ্বিতীয় কোষের তড়িচ্চালক বল কত?", e2,
              f"E ∝ balancing length: E₂ = {e1:g} x {l2} ÷ {l1} = {_f(_c(e2))} V.",
              f"E ∝ সাম্য-দৈর্ঘ্য: E₂ = {e1:g} x {l2} ÷ {l1} = {_f(_c(e2))} V।",
              (e1 * l1 / l2, e1, e1 + (l2 - l1) / 100), " V")


def joule(i, r, t):
    h = i * i * r * t
    return _n(f"A current of {i:g} A flows through a {r} Ω heater for {t} s. How much heat is produced?",
              f"{r} Ω-এর একটা হিটারের মধ্য দিয়ে {t} s ধরে {i:g} A প্রবাহ চলে। কত তাপ উৎপন্ন হয়?", h,
              f"H = I²Rt = {i:g}² x {r} x {t} = {_f(_c(h))} J.",
              f"H = I²Rt = {i:g}² x {r} x {t} = {_f(_c(h))} J।",
              (i * r * t, h / 2, i * r * r * t), " J")


def rc(r_txt, r, c_txt, c):
    t = r * c
    return _n(f"What is the time constant of a {r_txt} resistor in series with a {c_txt} capacitor?",
              f"{c_txt} ধারকের সঙ্গে শ্রেণিতে যুক্ত {r_txt} রোধের সময়-ধ্রুবক কত?", t,
              f"τ = RC = {r:g} Ω x {c:g} F = {_f(_c(t))} s; the capacitor reaches about 63% charge in one τ.",
              f"τ = RC = {r:g} Ω x {c:g} F = {_f(_c(t))} s; এক τ-তে ধারক প্রায় 63% আহিত হয়।",
              (t * 10, t / 10, t * 2), " s")


# ---------------------------------------------------------------- magnetism, induction and AC
def wire_force(b, i, l, th):
    f = b * i * l * SIN[th]
    return _n(f"A {l:g} m wire carrying {i} A lies at {th}° to a uniform magnetic field of {b:g} T. What force acts on it?",
              f"{i} A প্রবাহবাহী {l:g} m লম্বা একটা তার {b:g} T সুষম চৌম্বকক্ষেত্রের সঙ্গে {th}° কোণে আছে। এর উপর কত বল কাজ করে?", f,
              f"F = BIL sin θ = {b:g} x {i} x {l:g} x sin {th}° = {_f(_c(f))} N.",
              f"তারের উপর বল F = BIL sin θ = {b:g} x {i} x {l:g} x sin {th}° = {_f(_c(f))} N।",
              (b * i * l, f * 2, b * i / l), " N")


def ion_radius(m, v, b):
    r = m * v / (1.6 * b)
    return _n(f"An ion of mass {m:g} x 10⁻²⁶ kg and charge 1.6 x 10⁻¹⁹ C moves at {v:g} x 10⁵ m/s perpendicular to a {b:g} T magnetic field. What is the radius of its circle?",
              f"{m:g} x 10⁻²⁶ kg ভর আর 1.6 x 10⁻¹⁹ C আধানের একটা আয়ন {b:g} T চৌম্বকক্ষেত্রের লম্বভাবে {v:g} x 10⁵ m/s বেগে চলে। এর বৃত্তপথের ব্যাসার্ধ কত?", r,
              f"r = mv ÷ qB = {m:g} x 10⁻²⁶ x {v:g} x 10⁵ ÷ (1.6 x 10⁻¹⁹ x {b:g}) m = {_f(_c(r))} cm.",
              f"r = mv ÷ qB = {m:g} x 10⁻²⁶ x {v:g} x 10⁵ ÷ (1.6 x 10⁻¹⁹ x {b:g}) m = {_f(_c(r))} cm।",
              (r * 10, r / 2, m * b / (1.6 * v)), " cm")


def wire_b(i, r):
    b = 0.2 * i / r
    return _n(f"What magnetic field does a long straight wire carrying {i} A produce {r:g} m away?",
              f"{i} A প্রবাহবাহী একটা লম্বা সোজা তার {r:g} m দূরে কত চৌম্বকক্ষেত্র তৈরি করে?", b,
              f"B = μ₀I ÷ 2πr = 2 x 10⁻⁷ x {i} ÷ {r:g} T = {_f(_c(b))} μT.",
              f"B = μ₀I ÷ 2πr = 2 x 10⁻⁷ x {i} ÷ {r:g} T = {_f(_c(b))} μT।",
              (b * 2, b / r, 0.2 * i * r), " μT")


def solenoid(n, i):
    b = 4 * math.pi * 1e-4 * n * i
    return _n(f"A long solenoid has {n:,} turns per metre and carries {i} A. What is the field inside it?",
              f"একটা লম্বা সলিনয়েডে প্রতি মিটারে {n:,} পাক, প্রবাহ {i} A। এর ভেতরের চৌম্বকক্ষেত্র কত?", b,
              f"B = μ₀nI = 4π x 10⁻⁷ x {n:,} x {i} T = {_f(_c(b))} mT.",
              f"B = μ₀nI = 4π x 10⁻⁷ x {n:,} x {i} T = {_f(_c(b))} mT।",
              (b / 2, b * 2, n * i / 1000), " mT")


def shunt(g, ig_ma, i):
    s = g * ig_ma * 1e-3 / (i - ig_ma * 1e-3)
    return _n(f"A galvanometer of resistance {g} Ω gives full-scale deflection at {ig_ma} mA. What shunt converts it into an ammeter reading up to {i:g} A?",
              f"{g} Ω রোধের একটা গ্যালভানোমিটার {ig_ma} mA-এ পূর্ণ বিক্ষেপ দেয়। কত শান্ট লাগালে এটা {i:g} A পর্যন্ত মাপা অ্যামমিটার হবে?", s,
              f"S = I_g G ÷ (I - I_g) = {ig_ma} x 10⁻³ x {g} ÷ ({i:g} - {ig_ma * 1e-3:g}) = {_f(_c(s))} Ω, joined in parallel.",
              f"S = I_g G ÷ (I - I_g) = {ig_ma} x 10⁻³ x {g} ÷ ({i:g} - {ig_ma * 1e-3:g}) = {_f(_c(s))} Ω, সমান্তরালে যুক্ত।",
              (s * 10, g / i, s + 1), " Ω")


def voltmeter(g, ig_ma, v):
    r = int(round(v / (ig_ma * 1e-3) - g))
    return _n(f"A galvanometer of {g} Ω gives full-scale deflection at {ig_ma} mA. What series resistance makes it a voltmeter of range {v} V?",
              f"{g} Ω-এর একটা গ্যালভানোমিটার {ig_ma} mA-এ পূর্ণ বিক্ষেপ দেয়। কত শ্রেণি-রোধ লাগালে এটা {v} V পাল্লার ভোল্টমিটার হবে?", r,
              f"R = V ÷ I_g - G = {v} ÷ ({ig_ma} x 10⁻³) - {g} = {r:,} Ω.",
              f"R = V ÷ I_g - G = {v} ÷ ({ig_ma} x 10⁻³) - {g} = {r:,} Ω।",
              (r + 2 * g, int(round(v / (ig_ma * 1e-3)))+ g + 1, r // 10), " Ω")


def motional(b, l, v):
    e = b * l * v
    return _n(f"A {l:g} m rod moves at {v} m/s perpendicular to a {b:g} T magnetic field. What emf is induced across it?",
              f"{l:g} m লম্বা একটা দণ্ড {b:g} T চৌম্বকক্ষেত্রের লম্বভাবে {v} m/s বেগে চলে। এর দুই প্রান্তে কত তড়িচ্চালক বল আবিষ্ট হয়?", e,
              f"ε = BLv = {b:g} x {l:g} x {v} = {_f(_c(e))} V.",
              f"আবিষ্ট তড়িচ্চালক বল ε = BLv = {b:g} x {l:g} x {v} = {_f(_c(e))} V।",
              (b * v / l, e / 2, e * 2), " V")


def faraday(n, dphi, dt):
    e = n * dphi / dt
    return _n(f"The flux through a {n}-turn coil changes by {dphi:g} Wb in {dt:g} s. What average emf is induced?",
              f"{n} পাকের একটা কুণ্ডলীর মধ্য দিয়ে ফ্লাক্স {dt:g} s-এ {dphi:g} Wb বদলায়। গড়ে কত তড়িচ্চালক বল আবিষ্ট হয়?", e,
              f"ε = N ΔΦ ÷ Δt = {n} x {dphi:g} ÷ {dt:g} = {_f(_c(e))} V.",
              f"ε = N ΔΦ ÷ Δt = {n} x {dphi:g} ÷ {dt:g} = {_f(_c(e))} V।",
              (dphi / dt, n * dphi * dt, e / 2), " V")


def inductor_u(l, i):
    u = 0.5 * l * i * i
    return _n(f"How much energy is stored in a {l:g} H inductor carrying {i} A?",
              f"{i} A প্রবাহবাহী {l:g} H আবেশকে কত শক্তি জমা থাকে?", u,
              f"U = ½LI² = ½ x {l:g} x {i}² = {_f(_c(u))} J.",
              f"U = ½LI² = ½ x {l:g} x {i}² = {_f(_c(u))} J।",
              (l * i * i, l * i, u / 2), " J")


def transformer(vp, np_, ns):
    vs = vp * ns / np_
    return _n(f"A transformer has {np_:,} primary turns and {ns:,} secondary turns. If {vp} V AC is applied to the primary, what is the secondary voltage?",
              f"একটা ট্রান্সফর্মারের মুখ্য কুণ্ডলীতে {np_:,} পাক আর গৌণ কুণ্ডলীতে {ns:,} পাক। মুখ্যতে {vp} V পরিবর্তী বিভব দিলে গৌণ বিভব কত?", vs,
              f"Vs ÷ Vp = Ns ÷ Np: Vs = {vp} x {ns:,} ÷ {np_:,} = {_f(_c(vs))} V.",
              f"Vs ÷ Vp = Ns ÷ Np: Vs = {vp} x {ns:,} ÷ {np_:,} = {_f(_c(vs))} V।",
              (vp * np_ / ns, vp, vs * 2), " V")


def impedance(r, x):
    z = math.hypot(r, x)
    return _n(f"A series AC circuit has resistance {r} Ω and net reactance {x} Ω. What is its impedance?",
              f"একটা শ্রেণি পরিবর্তী-প্রবাহ বর্তনীর রোধ {r} Ω আর মোট প্রতিঘাত {x} Ω। এর প্রতিবাধা কত?", z,
              f"Z = √(R² + X²) = √({r}² + {x}²) = {_f(_c(z))} Ω.",
              f"Z = √(R² + X²) = √({r}² + {x}²) = {_f(_c(z))} Ω।",
              (r + x, abs(x - r) + 1, z * 2), " Ω")


def power_factor(r, x):
    pf = r / math.hypot(r, x)
    return _n(f"A series circuit has R = {r} Ω and net reactance {x} Ω. What is its power factor?",
              f"একটা শ্রেণি বর্তনীতে R = {r} Ω আর মোট প্রতিঘাত {x} Ω। এর ক্ষমতা-গুণক কত?", pf,
              f"cos φ = R ÷ Z = {r} ÷ {_f(_c(math.hypot(r, x)))} = {_f(_c(pf))}.",
              f"ক্ষমতা-গুণক cos φ = R ÷ Z = {r} ÷ {_f(_c(math.hypot(r, x)))} = {_f(_c(pf))}।",
              (x / math.hypot(r, x), r / (r + x), 1))


def xl(f, l):
    x = 2 * math.pi * f * l
    return _n(f"What is the reactance of a {l:g} H inductor at {f} Hz?",
              f"{f} Hz-এ {l:g} H আবেশকের প্রতিঘাত কত?", x,
              f"X_L = 2πfL = 2π x {f} x {l:g} = {_f(_c(x))} Ω - it rises with frequency.",
              f"X_L = 2πfL = 2π x {f} x {l:g} = {_f(_c(x))} Ω - কম্পাঙ্কের সঙ্গে বাড়ে।",
              (f * l, x / 2, x * 2), " Ω")


def xc(f, c):
    x = 1 / (2 * math.pi * f * c * 1e-6)
    return _n(f"What is the reactance of a {c} μF capacitor at {f} Hz?",
              f"{f} Hz-এ {c} μF ধারকের প্রতিঘাত কত?", x,
              f"X_C = 1 ÷ 2πfC = 1 ÷ (2π x {f} x {c} x 10⁻⁶) = {_f(_c(x))} Ω - it falls as frequency rises.",
              f"X_C = 1 ÷ 2πfC = 1 ÷ (2π x {f} x {c} x 10⁻⁶) = {_f(_c(x))} Ω - কম্পাঙ্ক বাড়লে কমে।",
              (x * 2, x / 2, 2 * math.pi * f * c), " Ω")


# ---------------------------------------------------------------- optics
def mirror(f, u):
    v = u * f / (u - f)
    return _n(f"An object stands {u} cm in front of a concave mirror of focal length {f} cm. How far from the mirror is the image?",
              f"{f} cm ফোকাস দূরত্বের একটা অবতল দর্পণের সামনে {u} cm দূরে একটা বস্তু আছে। প্রতিবিম্ব দর্পণ থেকে কত দূরে?", v,
              f"1/v + 1/u = 1/f with real-is-positive distances: 1/v = 1/{f} - 1/{u}, so v = {_f(_c(v))} cm, in front of the mirror.",
              f"বাস্তব দূরত্ব ধনাত্মক ধরে 1/v + 1/u = 1/f: 1/v = 1/{f} - 1/{u}, তাই v = {_f(_c(v))} cm, দর্পণের সামনে।",
              (u * f / (u + f), u - f, u + f), " cm")


def lens(f, u):
    v = u * f / (u - f)
    return _n(f"An object is {u} cm from a convex lens of focal length {f} cm. How far from the lens is the real image?",
              f"{f} cm ফোকাস দূরত্বের একটা উত্তল লেন্স থেকে {u} cm দূরে একটা বস্তু। বাস্তব প্রতিবিম্ব লেন্স থেকে কত দূরে?", v,
              f"1/v - 1/u = 1/f with u = -{u}: 1/v = 1/{f} - 1/{u}, so v = {_f(_c(v))} cm on the other side.",
              f"u = -{u} নিয়ে 1/v - 1/u = 1/f: 1/v = 1/{f} - 1/{u}, তাই v = {_f(_c(v))} cm অন্য পাশে।",
              (u * f / (u + f), u + f, u - f), " cm")


def lens_m(f, u):
    v = u * f / (u - f)
    m = v / u
    return _n(f"An object {u} cm from a convex lens of focal length {f} cm forms a real image. What is the size of the magnification?",
              f"{f} cm ফোকাস দূরত্বের উত্তল লেন্স থেকে {u} cm দূরের একটা বস্তু বাস্তব প্রতিবিম্ব গঠন করে। বিবর্ধনের মান কত?", m,
              f"v = uf ÷ (u - f) = {_f(_c(v))} cm; |m| = v ÷ u = {_f(_c(v))} ÷ {u} = {_f(_c(m))}.",
              f"v = uf ÷ (u - f) = {_f(_c(v))} cm; |m| = v ÷ u = {_f(_c(v))} ÷ {u} = {_f(_c(m))}।",
              (u / v, m + 1, f / u))


def lens_power(f1, f2):
    p = 100 / f1 + 100 / f2
    t2 = f"{f2} cm" if f2 > 0 else f"{-f2} cm (diverging)"
    t2b = f"{f2} cm" if f2 > 0 else f"{-f2} cm (অপসারী)"
    return _n(f"A converging lens of focal length {f1} cm is placed in contact with a lens of focal length {t2}. What is the power of the combination?",
              f"{f1} cm ফোকাস দূরত্বের একটা অভিসারী লেন্স {t2b} ফোকাস দূরত্বের একটা লেন্সের সঙ্গে লাগানো। সমবায়ের ক্ষমতা কত?", p,
              f"P = 100/f (cm) dioptres, and powers add: {_f(_c(100 / f1))} + ({_f(_c(100 / f2))}) = {_f(_c(p))} D.",
              f"P = 100/f (cm) ডায়প্টার, আর ক্ষমতা যোগ হয়: {_f(_c(100 / f1))} + ({_f(_c(100 / f2))}) = {_f(_c(p))} D।",
              (100 / f1 - 100 / f2, abs(f1 + f2) / 10, p * 2), " D")


def critical(n_txt, n, deg):
    return _n(f"Light goes from glass of refractive index {n_txt} towards air. What is the critical angle?",
              f"আলো {n_txt} প্রতিসরাঙ্কের কাচ থেকে বাতাসের দিকে যায়। সংকট কোণ কত?", deg,
              f"sin C = 1/n = 1/{n_txt} = {_f(_c(1 / n))}, so C = {deg}°. Beyond it the light is totally reflected.",
              f"sin C = 1/n = 1/{n_txt} = {_f(_c(1 / n))}, তাই C = {deg}°। এর বেশি কোণে আলো পূর্ণ প্রতিফলিত হয়।",
              (90 - deg, deg / 2, deg + 15), "°")


def apparent(h, n_txt, n):
    a = h / n
    return _n(f"A pool is {h:g} m deep. Looking straight down, how deep does it appear? (Refractive index of water {n_txt})",
              f"একটা পুকুর {h:g} m গভীর। সোজা উপর থেকে দেখলে কত গভীর মনে হয়? (জলের প্রতিসরাঙ্ক {n_txt})", a,
              f"Apparent depth = real depth ÷ n = {h:g} ÷ {n_txt} = {_f(_c(a))} m - water looks shallower than it is.",
              f"আপাত গভীরতা = প্রকৃত গভীরতা ÷ n = {h:g} ÷ {n_txt} = {_f(_c(a))} m - জল যত গভীর তার চেয়ে অগভীর দেখায়।",
              (h * n, h - n, a / 2), " m")


def ydse(lam, d_m, d_mm):
    b = lam * d_m / d_mm / 1000
    return _n(f"In Young's double-slit experiment, light of wavelength {lam} nm falls on slits {d_mm:g} mm apart and the screen is {d_m:g} m away. What is the fringe width?",
              f"ইয়ংয়ের দ্বি-রেখাছিদ্র পরীক্ষায় {lam} nm তরঙ্গদৈর্ঘ্যের আলো {d_mm:g} mm দূরত্বের ছিদ্রে পড়ে, পর্দা {d_m:g} m দূরে। ঝালরের প্রস্থ কত?", b,
              f"β = λD ÷ d = {lam} x 10⁻⁹ x {d_m:g} ÷ ({d_mm:g} x 10⁻³) m = {_f(_c(b))} mm.",
              f"β = λD ÷ d = {lam} x 10⁻⁹ x {d_m:g} ÷ ({d_mm:g} x 10⁻³) m = {_f(_c(b))} mm।",
              (b * 2, b / 2, lam * d_mm / d_m / 1000), " mm")


def prism(a, d, n):
    return _n(f"A prism of angle {a}° gives a minimum deviation of {d}°. What is its refractive index?",
              f"{a}° কোণের একটা প্রিজমে ন্যূনতম বিচ্যুতি {d}°। এর প্রতিসরাঙ্ক কত?", n,
              f"n = sin((A + D)/2) ÷ sin(A/2) = sin {(a + d) // 2}° ÷ sin {a // 2}° = {_f(_c(n))}.",
              f"প্রতিসরাঙ্ক n = sin((A + D)/2) ÷ sin(A/2) = sin {(a + d) // 2}° ÷ sin {a // 2}° = {_f(_c(n))}।",
              (d / a + 1, 1.5, n + 0.3))


def telescope(fo, fe):
    m = fo / fe
    return _n(f"An astronomical telescope has an objective of focal length {fo} cm and an eyepiece of {fe} cm. What is its magnifying power in normal adjustment?",
              f"একটা জ্যোতির্বিজ্ঞান দূরবিনের অভিলক্ষ্যের ফোকাস দূরত্ব {fo} cm, অভিনেত্রের {fe} cm। স্বাভাবিক সমন্বয়ে এর বিবর্ধন-ক্ষমতা কত?", m,
              f"M = f_o ÷ f_e = {fo} ÷ {fe} = {_f(_c(m))}; the tube length is f_o + f_e = {fo + fe} cm.",
              f"M = f_o ÷ f_e = {fo} ÷ {fe} = {_f(_c(m))}; নলের দৈর্ঘ্য f_o + f_e = {fo + fe} cm।",
              (fo * fe / 100, fe / fo * 100, fo + fe))


def malus(i0, th):
    i = i0 * SIN[90 - th] ** 2
    return _n(f"Polarised light of intensity {i0} W/m² passes through an analyser whose axis is at {th}° to the light's plane of polarisation. What intensity comes out?",
              f"{i0} W/m² তীব্রতার সমবর্তিত আলো একটা বিশ্লেষকের মধ্য দিয়ে যায়, যার অক্ষ আলোর সমবর্তন-তলের সঙ্গে {th}° কোণে। কত তীব্রতা বেরোয়?", i,
              f"Malus's law I = I₀ cos²θ = {i0} x cos² {th}° = {_f(_c(i))} W/m².",
              f"মালুসের সূত্র I = I₀ cos²θ = {i0} x cos² {th}° = {_f(_c(i))} W/m²।",
              (i0 * SIN[90 - th], i0 / 2, i0 * SIN[th] ** 2), " W/m²")


# ---------------------------------------------------------------- modern physics
def photon(lam):
    e = 1240 / lam
    return _n(f"What is the energy of a photon of wavelength {lam} nm? (hc = 1240 eV nm)",
              f"{lam} nm তরঙ্গদৈর্ঘ্যের একটা ফোটনের শক্তি কত? (hc = 1240 eV nm)", e,
              f"E = hc ÷ λ = 1240 ÷ {lam} = {_f(_c(e))} eV.",
              f"E = hc ÷ λ = 1240 ÷ {lam} = {_f(_c(e))} eV।",
              (lam / 1240 * 100, e * 2, e + 1.5), " eV")


def photoelectric(lam, phi):
    k = 1240 / lam - phi
    return _n(f"Light of wavelength {lam} nm falls on a metal with work function {phi:g} eV. What is the maximum kinetic energy of the photoelectrons? (hc = 1240 eV nm)",
              f"{phi:g} eV কার্য-অপেক্ষকের একটা ধাতুতে {lam} nm তরঙ্গদৈর্ঘ্যের আলো পড়ে। ফটো-ইলেকট্রনের সর্বোচ্চ গতিশক্তি কত? (hc = 1240 eV nm)", k,
              f"K_max = hc/λ - φ = {_f(_c(1240 / lam))} - {phi:g} = {_f(_c(k))} eV; the stopping potential is {_f(_c(k))} V.",
              f"K_max = hc/λ - φ = {_f(_c(1240 / lam))} - {phi:g} = {_f(_c(k))} eV; নিবৃত্তি বিভব {_f(_c(k))} V।",
              (1240 / lam, 1240 / lam + phi, phi), " eV")


def threshold(phi):
    lam = 1240 / phi
    return _n(f"A metal has a work function of {phi:g} eV. What is its threshold wavelength for photoemission? (hc = 1240 eV nm)",
              f"একটা ধাতুর কার্য-অপেক্ষক {phi:g} eV। আলোক-নিঃসরণের জন্য এর সূচন-তরঙ্গদৈর্ঘ্য কত? (hc = 1240 eV nm)", lam,
              f"λ₀ = hc ÷ φ = 1240 ÷ {phi:g} = {_f(_c(lam))} nm; longer wavelengths free no electrons at all.",
              f"λ₀ = hc ÷ φ = 1240 ÷ {phi:g} = {_f(_c(lam))} nm; এর চেয়ে দীর্ঘ তরঙ্গদৈর্ঘ্য কোনো ইলেকট্রন মুক্ত করে না।",
              (lam / 2, lam * 2, 1240 * phi / 10), " nm")


def debroglie(v):
    lam = 1227 / math.sqrt(v)
    return _n(f"An electron is accelerated from rest through {v:,} V. What is its de Broglie wavelength? (λ = 1.227/√V nm)",
              f"একটা ইলেকট্রনকে স্থির অবস্থা থেকে {v:,} V বিভবের মধ্য দিয়ে ত্বরিত করা হল। এর দ্য ব্রয়লি তরঙ্গদৈর্ঘ্য কত? (λ = 1.227/√V nm)", lam,
              f"λ = 1.227 ÷ √{v:,} nm = {_f(_c(lam))} pm - comparable to atomic spacings, which is why electron diffraction works.",
              f"λ = 1.227 ÷ √{v:,} nm = {_f(_c(lam))} pm - পরমাণুর দূরত্বের কাছাকাছি, তাই ইলেকট্রন-অপবর্তন হয়।",
              (1227 / v, lam * 2, lam / 2), " pm")


def bohr_ion(n):
    e = 13.6 / (n * n)
    return _n(f"How much energy is needed to ionise a hydrogen atom from its n = {n} state?",
              f"n = {n} অবস্থা থেকে একটা হাইড্রোজেন পরমাণুকে আয়নিত করতে কত শক্তি লাগে?", e,
              f"E_n = -13.6 ÷ n² eV = -{_f(_c(e))} eV, so {_f(_c(e))} eV frees the electron.",
              f"E_n = -13.6 ÷ n² eV = -{_f(_c(e))} eV, তাই {_f(_c(e))} eV দিলে ইলেকট্রন মুক্ত হয়।",
              (13.6 / n, 13.6, 13.6 - e), " eV")


def bohr_line(n1, n2):
    e = 13.6 * (1 / (n1 * n1) - 1 / (n2 * n2))
    return _n(f"What is the energy of the photon emitted when a hydrogen electron drops from n = {n2} to n = {n1}?",
              f"হাইড্রোজেনের ইলেকট্রন n = {n2} থেকে n = {n1}-এ নামলে নির্গত ফোটনের শক্তি কত?", e,
              f"ΔE = 13.6(1/{n1}² - 1/{n2}²) = {_f(_c(e))} eV.",
              f"ΔE = 13.6(1/{n1}² - 1/{n2}²) = {_f(_c(e))} eV।",
              (13.6 / (n2 * n2), 13.6 / (n1 * n1), e / 2), " eV")


def bohr_r(n):
    r = 0.53 * n * n
    return _n(f"The Bohr radius of hydrogen's ground state is 0.53 Å. What is the orbit radius for n = {n}?",
              f"হাইড্রোজেনের ভূমি-অবস্থার বোর ব্যাসার্ধ 0.53 Å। n = {n}-এর কক্ষ-ব্যাসার্ধ কত?", r,
              f"r ∝ n²: 0.53 x {n}² = {_f(_c(r))} Å.",
              f"r ∝ n²: 0.53 x {n}² = {_f(_c(r))} Å।",
              (0.53 * n, 0.53 / n, r * 2), " Å")


def halflife(m, t_half, t, unit_en, unit_bn, mu_en, mu_bn):
    r = m / 2 ** (t / t_half)
    return _n(f"A sample holds {m:g} {mu_en} of a radioisotope with a half-life of {t_half:g} {unit_en}. How much is left after {t:g} {unit_en}?",
              f"একটা নমুনায় {t_half:g} {unit_bn} অর্ধায়ুর তেজস্ক্রিয় আইসোটোপ {m:g} {mu_bn} আছে। {t:g} {unit_bn} পরে কতটা থাকে?", r,
              f"{_f(_c(t / t_half))} half-lives: {m:g} ÷ 2^{_f(_c(t / t_half))} = {_f(_c(r))} {mu_en}.",
              f"{_f(_c(t / t_half))}টি অর্ধায়ু: {m:g} ÷ 2^{_f(_c(t / t_half))} = {_f(_c(r))} {mu_bn}।",
              (m * (1 - t / t_half / 4), m / (t / t_half), m / 2), f" {mu_en}", f" {mu_bn}")


def mass_energy(dm):
    e = dm * 931.5
    return _n(f"A nuclear reaction has a mass defect of {dm:g} u. How much energy is released? (1 u = 931.5 MeV)",
              f"একটা নিউক্লীয় বিক্রিয়ায় ভর-ত্রুটি {dm:g} u। কত শক্তি মুক্ত হয়? (1 u = 931.5 মেগা-ইলেকট্রন ভোল্ট)", e,
              f"E = Δm x 931.5 = {dm:g} x 931.5 = {_f(_c(e))} MeV.",
              f"E = Δm x 931.5 = {dm:g} x 931.5 = {_f(_c(e))} মেগা-ইলেকট্রন ভোল্ট।",
              (e / 2, dm * 9, e * 10), " MeV", " মেগা-ইলেকট্রন ভোল্ট")


# ---------------------------------------------------------------- measurement
def density_error(em, el):
    e = em + 3 * el
    return _n(f"The density of a cube is found from its mass (error {em:g}%) and its side length (error {el:g}%). What is the maximum percentage error in the density?",
              f"একটা ঘনকের ঘনত্ব নির্ণয় করা হয় তার ভর (ত্রুটি {em:g}%) আর বাহুর দৈর্ঘ্য (ত্রুটি {el:g}%) থেকে। ঘনত্বে সর্বোচ্চ শতকরা ত্রুটি কত?", e,
              f"ρ = m ÷ L³, so Δρ/ρ = Δm/m + 3ΔL/L = {em:g} + 3 x {el:g} = {_f(_c(e))}%.",
              f"ρ = m ÷ L³, তাই Δρ/ρ = Δm/m + 3ΔL/L = {em:g} + 3 x {el:g} = {_f(_c(e))}%।",
              (em + el, em * el * 3, abs(3 * el - em) + 0.5), "%")


def vernier(n_v, n_m):
    lc = 1 / n_v
    return _n(f"On a vernier caliper, 1 main-scale division is 1 mm and {n_v} vernier divisions match {n_m} main-scale divisions. What is the least count?",
              f"একটা ভার্নিয়ার ক্যালিপারে প্রধান স্কেলের 1 ভাগ = 1 mm, আর ভার্নিয়ারের {n_v} ভাগ প্রধান স্কেলের {n_m} ভাগের সমান। লঘিষ্ঠ ধ্রুবক কত?", lc,
              f"LC = 1 MSD - 1 VSD = 1 - {n_m}/{n_v} = {_f(_c(lc))} mm.",
              f"লঘিষ্ঠ ধ্রুবক = 1 MSD - 1 VSD = 1 - {n_m}/{n_v} = {_f(_c(lc))} mm।",
              (n_m / n_v, lc * 10, 1), " mm")


NUMERIC = [
    proj_range(20, 45), proj_range(30, 15), proj_h(20, 30), proj_h(20, 60), proj_t(30, 60),
    river(100, 5, 3), atwood_a(7, 3), atwood_t(3, 2), incline(0.25), incline(0.5),
    banking(40, 45, "1", 1.0), banking(120, 37, "0.75", 0.75), spring_x(2, 4, 800),
    perfectly_inelastic(2, 6, 1, False), perfectly_inelastic(3, 4, 1, True),
    rolling("ring", 10), rolling("disc", 30), rolling("sphere", 7), skater(6, 2, 4),
    g_height("at a height equal to Earth's radius", "পৃথিবীর ব্যাসার্ধের সমান উচ্চতায়", 0.25,
             "g' = g(R/(R + h))² = 10 x (1/2)² = 2.5 m/s².", "g' = g(R/(R + h))² = 10 x (1/2)² = 2.5 m/s²।"),
    g_height("at a depth of half Earth's radius", "পৃথিবীর অর্ধেক ব্যাসার্ধ গভীরে", 0.5,
             "g' = g(1 - d/R) = 10 x (1 - 1/2) = 5 m/s².", "g' = g(1 - d/R) = 10 x (1 - 1/2) = 5 m/s²।"),
    g_height("at a height of twice Earth's radius", "পৃথিবীর ব্যাসার্ধের দ্বিগুণ উচ্চতায়", 1 / 9,
             "g' = g(R/(R + 2R))² = 10 ÷ 9 = 1.11 m/s².", "g' = g(R/(R + 2R))² = 10 ÷ 9 = 1.11 m/s²।"),
    kepler(2, 4), kepler(3, 9), escape(7.9),
    stretch(1000, 2, 1), stretch(2000, 3, 2), depth_p(20), terminal(2, 3), pipe(2, 2),
    mixing(1, 80, 3, 20), melt(2), expand(100, 40), carnot(500, 300), carnot(800, 200),
    isobaric(100, 2, 5), vrms(500, 300, 1200), vrms_gas(1600),
    shm_mass(2, 4), pendulum(2), pendulum(3), shm_v(0.2, 15), shm_a(0.1, 10),
    string_v(360, 0.1), string_f(100, 0.5), organ(0.85, True), organ(0.5, False),
    beats(256, 4, 6), doppler(640, 20), doppler(500, 40),
    coulomb(2, 3, 0.3), coulomb(4, 5, 0.6), efield(1, 0.3), epot(1, 0.1),
    plate_cap(1, 1), cap_series(6, 3), cap_series(12, 4), cap_energy(10, 100), cap_share(2, 100, 3),
    cell_i(24, 2, 6), cell_v(12, 1, 5), parallel(6, 3), parallel(12, 6, 4), parallel(20, 30, 60),
    bulb(100, 220, 110), bulb(200, 240, 120), meter_bridge(6, 40), meter_bridge(15, 60),
    potentiometer(1.5, 60, 80), joule(2, 5, 60), rc("10 kΩ", 1e4, "100 μF", 1e-4),
    wire_force(0.5, 4, 2, 90), wire_force(0.2, 5, 3, 30), ion_radius(3.2, 2, 0.4),
    wire_b(10, 0.02), solenoid(1000, 2), shunt(100, 1, 1), voltmeter(100, 1, 10),
    motional(0.5, 2, 10), faraday(100, 0.02, 0.1), faraday(200, 0.005, 0.01), inductor_u(2, 3),
    transformer(220, 100, 500), transformer(240, 600, 30), impedance(3, 4), impedance(5, 12),
    power_factor(6, 8), xl(50, 0.1), xc(50, 100),
    mirror(10, 30), mirror(20, 30), lens(10, 25), lens(20, 30), lens_m(10, 15),
    lens_power(20, 25), lens_power(10, -25), critical("2", 2, 30), critical("√2", math.sqrt(2), 45),
    apparent(2, "4/3", 4 / 3), ydse(600, 1, 0.5), ydse(500, 1.5, 0.3),
    prism(60, 60, math.sqrt(3)), prism(60, 30, math.sqrt(2)), telescope(100, 5), malus(100, 60),
    photon(620), photon(248), photoelectric(310, 2), photoelectric(155, 5), threshold(2),
    debroglie(100), debroglie(900), bohr_ion(2), bohr_line(1, 2), bohr_line(2, 3), bohr_r(3),
    halflife(64, 2, 6, "days", "দিন", "g", "g"), halflife(80, 5, 15, "years", "বছর", "mg", "mg"),
    mass_energy(0.1), density_error(1, 2), vernier(10, 9), vernier(20, 19),
    atwood_a(3, 2), river(120, 6, 4), spring_x(1, 10, 400), perfectly_inelastic(4, 5, 1, True),
    carnot(400, 300), mixing(2, 90, 3, 40), efield(2, 0.2),
]


CONCEPTS = [
    mcq("Which pair of quantities has the same dimensions?", ["Planck's constant and angular momentum", "Force and power", "Work and momentum", "Pressure and force"], 0,
        "Both h and L = mvr have dimensions [M L² T⁻¹].",
        "কোন জোড়া রাশির মাত্রা একই?", ["প্ল্যাঙ্কের ধ্রুবক আর কৌণিক ভরবেগ", "বল আর ক্ষমতা", "কাজ আর ভরবেগ", "চাপ আর বল"],
        "h আর L = mvr দুটোরই মাত্রা [M L² T⁻¹]।"),
    mcq("A ball is thrown straight up. At the very top of its flight, what is its acceleration?", ["g, directed downward", "Zero", "g, directed upward", "It depends on the throw speed"], 0,
        "Velocity is momentarily zero, but gravity still acts, so acceleration stays g downward throughout.",
        "একটা বল সোজা উপরে ছোড়া হল। উড়ানের একেবারে শীর্ষবিন্দুতে এর ত্বরণ কত?", ["g, নিচের দিকে", "শূন্য", "g, উপরের দিকে", "ছোড়ার বেগের উপর নির্ভর করে"],
        "বেগ ক্ষণিকের জন্য শূন্য, কিন্তু অভিকর্ষ কাজ করেই চলে, তাই ত্বরণ সারাক্ষণ g নিচের দিকে।"),
    mcq("What does the area under a velocity-time graph give?", ["Displacement", "Acceleration", "Jerk", "Average force"], 0,
        "Area = ∫v dt = displacement; the slope of the same graph gives acceleration.",
        "বেগ-সময় লেখচিত্রের নিচের ক্ষেত্রফল কী দেয়?", ["সরণ", "ত্বরণ", "ঝাঁকুনি (জার্ক)", "গড় বল"],
        "ক্ষেত্রফল = ∫v dt = সরণ; একই লেখচিত্রের নতি দেয় ত্বরণ।"),
    mcq("Impulse acting on a body equals which of these?", ["Its change in momentum", "Its change in kinetic energy", "Force divided by time", "Mass times acceleration"], 0,
        "J = ∫F dt = Δp. Airbags lengthen the time so the same Δp needs a smaller force.",
        "কোনো বস্তুর উপর ঘাত-বল কোনটার সমান?", ["তার ভরবেগের পরিবর্তন", "তার গতিশক্তির পরিবর্তন", "বল ভাগ সময়", "ভর গুণ ত্বরণ"],
        "J = ∫F dt = Δp। এয়ারব্যাগ সময় বাড়ায়, তাই একই Δp-তে কম বল লাগে।"),
    mcq("For a conservative force, the work done moving between two points…", ["Depends only on the end points, not the path", "Is always zero", "Depends on the speed of motion", "Is always positive"], 0,
        "Gravity and spring forces are conservative: a potential energy can be defined, and work round any closed loop is zero.",
        "সংরক্ষী বলের ক্ষেত্রে দুই বিন্দুর মধ্যে সরাতে কৃতকাজ…", ["শুধু প্রান্তবিন্দুর উপর নির্ভর করে, পথের উপর নয়", "সবসময় শূন্য", "গতির বেগের উপর নির্ভর করে", "সবসময় ধনাত্মক"],
        "অভিকর্ষ আর স্প্রিং-বল সংরক্ষী: স্থিতিশক্তি সংজ্ঞায়িত করা যায়, আর যেকোনো বদ্ধ পথে কাজ শূন্য।"),
    mcq("Two equal masses collide head-on elastically, one initially at rest. What happens?", ["They exchange velocities", "Both stop", "They stick together", "Both move on at half speed"], 0,
        "With equal masses, momentum and kinetic energy are both conserved only if the velocities swap - as in Newton's cradle.",
        "দুটো সমান ভর মুখোমুখি স্থিতিস্থাপক সংঘর্ষে আসে, একটা শুরুতে স্থির। কী হয়?", ["তারা বেগ বিনিময় করে", "দুটোই থেমে যায়", "তারা জুড়ে যায়", "দুটোই অর্ধেক বেগে চলে"],
        "সমান ভরে ভরবেগ আর গতিশক্তি দুটোই সংরক্ষিত থাকে কেবল বেগ অদলবদল হলে - যেমন নিউটনের দোলনায়।"),
    mcq("When is the angular momentum of a system conserved?", ["When the net external torque on it is zero", "When the net external force is zero", "When it rotates at constant speed only", "Always, in every case"], 0,
        "dL/dt = τ_ext, so L stays constant when the external torque vanishes - even if forces act through the axis.",
        "কখন কোনো সংস্থার কৌণিক ভরবেগ সংরক্ষিত থাকে?", ["যখন তার উপর মোট বাহ্যিক টর্ক শূন্য", "যখন মোট বাহ্যিক বল শূন্য", "কেবল স্থির বেগে ঘুরলে", "সবসময়, সব ক্ষেত্রে"],
        "dL/dt = τ_বাহ্যিক, তাই বাহ্যিক টর্ক না থাকলে L স্থির থাকে - অক্ষ দিয়ে বল কাজ করলেও।"),
    mcq("For a wheel rolling without slipping, what is the velocity of the point touching the ground?", ["Zero", "Equal to the centre's velocity", "Twice the centre's velocity", "Equal to ωR backwards"], 0,
        "The contact point has v_centre - ωR = 0; the top point moves at 2v_centre.",
        "পিছলে না গিয়ে গড়ানো চাকার মাটি-ছোঁয়া বিন্দুর বেগ কত?", ["শূন্য", "কেন্দ্রের বেগের সমান", "কেন্দ্রের বেগের দ্বিগুণ", "পেছনের দিকে ωR"],
        "স্পর্শবিন্দুর বেগ v_কেন্দ্র - ωR = 0; শীর্ষবিন্দু চলে 2v_কেন্দ্র বেগে।"),
    mcq("How does escape speed from Earth depend on the mass of the object launched?", ["It does not depend on it", "It rises with the mass", "It falls as the mass rises", "It rises with the square root of the mass"], 0,
        "v_e = √(2GM/R) uses Earth's mass M only - a pebble and a rocket need the same 11.2 km/s.",
        "পৃথিবী থেকে মুক্তিবেগ উৎক্ষিপ্ত বস্তুর ভরের উপর কীভাবে নির্ভর করে?", ["নির্ভর করে না", "ভর বাড়লে বাড়ে", "ভর বাড়লে কমে", "ভরের বর্গমূলের সঙ্গে বাড়ে"],
        "v_e = √(2GM/R)-এ কেবল পৃথিবীর ভর M আছে - নুড়ি আর রকেট দুটোরই 11.2 km/s লাগে।"),
    mcq("What is special about a geostationary satellite's orbit?", ["Period 24 h, equatorial, about 36,000 km up", "Period 90 min over the poles", "It never moves at all", "Period 24 h over the poles"], 0,
        "Moving with Earth's rotation above the equator, it stays over one spot - ideal for TV and weather satellites.",
        "ভূস্থির উপগ্রহের কক্ষপথের বিশেষত্ব কী?", ["পর্যায়কাল 24 ঘণ্টা, নিরক্ষীয়, প্রায় 36,000 km উঁচুতে", "মেরুর উপর দিয়ে 90 মিনিট পর্যায়কাল", "এটা একদম নড়ে না", "মেরুর উপর দিয়ে 24 ঘণ্টা পর্যায়কাল"],
        "নিরক্ষরেখার উপরে পৃথিবীর ঘূর্ণনের সঙ্গে চলে, তাই এক জায়গার উপরেই থাকে - টিভি আর আবহাওয়া উপগ্রহের জন্য আদর্শ।"),
    mcq("Why do astronauts in an orbiting station feel weightless?", ["They and the station are in free fall together", "There is no gravity in orbit", "The station's engines cancel gravity", "Air pressure pushes them up"], 0,
        "Gravity there is still about 90% of surface g; everything falls together, so nothing presses on the floor.",
        "কক্ষপথে ঘোরা স্টেশনে মহাকাশচারীরা ভারহীন বোধ করেন কেন?", ["তাঁরা আর স্টেশন একসঙ্গে মুক্তভাবে পড়ছেন", "কক্ষপথে অভিকর্ষ নেই", "স্টেশনের ইঞ্জিন অভিকর্ষ বাতিল করে", "বায়ুচাপ তাঁদের উপরে ঠেলে"],
        "সেখানে অভিকর্ষ পৃষ্ঠের g-এর প্রায় 90%; সবকিছু একসঙ্গে পড়ে, তাই কিছু মেঝেতে চাপ দেয় না।"),
    mcq("Why does water rise higher in a narrower capillary tube?", ["Rise h = 2T cos θ ÷ ρgr, so h ∝ 1/r", "Narrow tubes hold less air", "Gravity is weaker in narrow tubes", "Viscosity is larger there"], 0,
        "Surface tension pulls along a circumference ∝ r while the lifted weight ∝ r²h, giving h ∝ 1/r (Jurin's law).",
        "সরু কৈশিক নলে জল বেশি উঁচুতে ওঠে কেন?", ["উচ্চতা h = 2T cos θ ÷ ρgr, তাই h ∝ 1/r", "সরু নলে বাতাস কম থাকে", "সরু নলে অভিকর্ষ দুর্বল", "সেখানে সান্দ্রতা বেশি"],
        "পৃষ্ঠটান পরিধি বরাবর টানে (∝ r), আর তোলা ওজন ∝ r²h, তাই h ∝ 1/r (জুরিনের সূত্র)।"),
    mcq("How does the viscosity of a liquid and of a gas change on heating?", ["Liquid's falls, gas's rises", "Both fall", "Both rise", "Liquid's rises, gas's falls"], 0,
        "Heat loosens a liquid's intermolecular bonds; in a gas faster molecules carry more momentum between layers.",
        "গরম করলে তরল আর গ্যাসের সান্দ্রতা কীভাবে বদলায়?", ["তরলের কমে, গ্যাসের বাড়ে", "দুটোরই কমে", "দুটোরই বাড়ে", "তরলের বাড়ে, গ্যাসের কমে"],
        "তাপ তরলের আন্তঃআণবিক বন্ধন আলগা করে; গ্যাসে দ্রুত অণু স্তরগুলোর মধ্যে বেশি ভরবেগ বয়ে নেয়।"),
    mcq("Wien's displacement law says that for a black body…", ["λ_max x T is constant", "Total power ∝ T⁴", "Emissivity equals absorptivity", "λ_max ∝ T"], 0,
        "Hotter bodies peak at shorter wavelengths: λ_max T ≈ 2.9 x 10⁻³ m K, which is why hot steel glows red, then white.",
        "উইনের সরণ-সূত্র অনুযায়ী কৃষ্ণবস্তুর ক্ষেত্রে…", ["λ_শীর্ষ x T ধ্রুবক", "মোট ক্ষমতা ∝ T⁴", "নিঃসরণ-ক্ষমতা = শোষণ-ক্ষমতা", "λ_শীর্ষ ∝ T"],
        "বেশি গরম বস্তুর শীর্ষ ছোট তরঙ্গদৈর্ঘ্যে: λ_max T ≈ 2.9 x 10⁻³ m K, তাই গরম ইস্পাত প্রথমে লাল, পরে সাদা জ্বলে।"),
    mcq("By what factor does the power radiated by a black body grow if its absolute temperature doubles?", ["16", "2", "4", "8"], 0,
        "Stefan-Boltzmann law P = σAT⁴: 2⁴ = 16.",
        "কৃষ্ণবস্তুর পরম তাপমাত্রা দ্বিগুণ হলে বিকিরিত ক্ষমতা কত গুণ বাড়ে?", ["16", "2", "4", "8"],
        "স্টেফান-বোলৎজমানের সূত্র P = σAT⁴: 2⁴ = 16।"),
    mcq("In an adiabatic process…", ["No heat enters or leaves the system", "The temperature stays constant", "The pressure stays constant", "The volume stays constant"], 0,
        "Q = 0, so ΔU = -W; for an ideal gas PV^γ stays constant. Quick compressions, like in a diesel engine, are nearly adiabatic.",
        "রুদ্ধতাপ প্রক্রিয়ায়…", ["সংস্থায় কোনো তাপ ঢোকে বা বেরোয় না", "তাপমাত্রা স্থির থাকে", "চাপ স্থির থাকে", "আয়তন স্থির থাকে"],
        "Q = 0, তাই ΔU = -W; আদর্শ গ্যাসে PV^γ স্থির থাকে। ডিজেল ইঞ্জিনের মতো দ্রুত সংকোচন প্রায় রুদ্ধতাপ।"),
    mcq("In an isothermal expansion of an ideal gas, what is the change in internal energy?", ["Zero - all the heat absorbed becomes work", "Equal to the work done", "Equal to the heat absorbed", "Negative"], 0,
        "An ideal gas's internal energy depends only on temperature; with T fixed, ΔU = 0 and Q = W.",
        "আদর্শ গ্যাসের সমোষ্ণ প্রসারণে অন্তর্নিহিত শক্তির পরিবর্তন কত?", ["শূন্য - শোষিত সব তাপ কাজে পরিণত হয়", "কৃতকাজের সমান", "শোষিত তাপের সমান", "ঋণাত্মক"],
        "আদর্শ গ্যাসের অন্তর্নিহিত শক্তি কেবল তাপমাত্রার উপর নির্ভর করে; T স্থির হলে ΔU = 0 আর Q = W।"),
    mcq("For one mole of an ideal gas, Cp - Cv equals…", ["R", "Zero", "γ", "3R/2"], 0,
        "Mayer's relation: at constant pressure the gas also does work PΔV = RΔT, so Cp exceeds Cv by R.",
        "এক মোল আদর্শ গ্যাসের Cp - Cv কত?", ["R", "শূন্য", "γ", "3R/2"],
        "মেয়ারের সম্পর্ক: স্থির চাপে গ্যাস PΔV = RΔT কাজও করে, তাই Cp, Cv-এর চেয়ে R বেশি।"),
    mcq("What is the molar heat capacity at constant volume of a monatomic ideal gas?", ["3R/2", "5R/2", "R/2", "3R"], 0,
        "Three translational degrees of freedom, each ½RT per mole by equipartition: U = 3RT/2.",
        "এক-পারমাণবিক আদর্শ গ্যাসের স্থির আয়তনে মোলার তাপধারকত্ব কত?", ["3R/2", "5R/2", "R/2", "3R"],
        "তিনটি চলন-স্বাতন্ত্র্য মাত্রা, সমবিভাজন অনুযায়ী প্রতিটিতে মোলপ্রতি ½RT: U = 3RT/2।"),
    mcq("What defines simple harmonic motion?", ["Acceleration proportional to displacement and opposite to it", "Constant acceleration", "Constant speed in a circle", "Acceleration proportional to velocity"], 0,
        "a = -ω²x. Its projection is uniform circular motion, and the period does not depend on amplitude.",
        "সরল দোলগতির সংজ্ঞা কী?", ["ত্বরণ সরণের সমানুপাতিক আর বিপরীতমুখী", "স্থির ত্বরণ", "বৃত্তে স্থির দ্রুতি", "ত্বরণ বেগের সমানুপাতিক"],
        "a = -ω²x। এটা সুষম বৃত্তীয় গতির অভিক্ষেপ, আর পর্যায়কাল বিস্তারের উপর নির্ভর করে না।"),
    mcq("How does the speed of sound in an ideal gas depend on its absolute temperature?", ["v ∝ √T", "v ∝ T", "v ∝ 1/T", "It does not depend on T"], 0,
        "v = √(γRT/M); air at 4 times the absolute temperature carries sound twice as fast.",
        "আদর্শ গ্যাসে শব্দের বেগ পরম তাপমাত্রার উপর কীভাবে নির্ভর করে?", ["v ∝ √T", "v ∝ T", "v ∝ 1/T", "T-এর উপর নির্ভর করে না"],
        "v = √(γRT/M); পরম তাপমাত্রা 4 গুণ হলে বাতাসে শব্দ দ্বিগুণ বেগে চলে।"),
    mcq("What happens to standing waves on a string at a node?", ["The displacement is always zero", "The displacement is always maximum", "The energy flows fastest", "The tension is zero"], 0,
        "Nodes are half a wavelength apart; antinodes, midway between them, swing the most.",
        "তারে স্থির তরঙ্গের নিস্পন্দ বিন্দুতে কী হয়?", ["সরণ সবসময় শূন্য", "সরণ সবসময় সর্বোচ্চ", "শক্তি সবচেয়ে দ্রুত বয়", "টান শূন্য"],
        "নিস্পন্দ বিন্দুগুলো অর্ধ-তরঙ্গদৈর্ঘ্য দূরে; মাঝের সুস্পন্দ বিন্দু সবচেয়ে বেশি দোলে।"),
    mcq("Gauss's law states that the electric flux through a closed surface equals…", ["The enclosed charge divided by ε₀", "Zero always", "The field times the volume", "The charge outside divided by ε₀"], 0,
        "Φ = q_enclosed ÷ ε₀. Charges outside contribute as much flux in as out.",
        "গাউসের সূত্র অনুযায়ী কোনো বদ্ধ তলের মধ্য দিয়ে তড়িৎ-ফ্লাক্স সমান…", ["আবদ্ধ আধান ভাগ ε₀", "সবসময় শূন্য", "ক্ষেত্র গুণ আয়তন", "বাইরের আধান ভাগ ε₀"],
        "Φ = q_আবদ্ধ ÷ ε₀। বাইরের আধান যতটা ফ্লাক্স ঢোকায় ততটাই বের করে।"),
    mcq("What is the electric field inside a charged hollow metal sphere?", ["Zero", "Maximum at the centre", "Uniform and non-zero", "Equal to that at the surface"], 0,
        "Charges sit on the outer surface of a conductor; the field inside vanishes - the basis of electrostatic shielding.",
        "আহিত ফাঁপা ধাতব গোলকের ভেতরে তড়িৎক্ষেত্র কত?", ["শূন্য", "কেন্দ্রে সর্বোচ্চ", "সুষম আর অশূন্য", "পৃষ্ঠের সমান"],
        "পরিবাহীর আধান বাইরের পৃষ্ঠে থাকে; ভেতরে ক্ষেত্র শূন্য - তড়িৎস্থিতীয় আবরণের ভিত্তি।"),
    mcq("How are equipotential surfaces related to electric field lines?", ["They are always perpendicular", "They are always parallel", "They meet at 45°", "They are unrelated"], 0,
        "No work is done moving along an equipotential, so the field can have no component along it.",
        "সমবিভব তল আর তড়িৎ-বলরেখার সম্পর্ক কী?", ["সবসময় লম্ব", "সবসময় সমান্তরাল", "45° কোণে মেলে", "সম্পর্কহীন"],
        "সমবিভব তল বরাবর সরাতে কাজ হয় না, তাই ক্ষেত্রের তার বরাবর কোনো উপাংশ থাকতে পারে না।"),
    mcq("A dielectric slab of constant K fills the gap of an isolated charged capacitor. What happens?", ["Capacitance rises K times and voltage falls K times", "Capacitance falls K times", "Charge rises K times", "Nothing changes"], 0,
        "With the battery removed the charge is fixed; C = Kε₀A/d grows, so V = Q/C drops.",
        "একটা বিচ্ছিন্ন আহিত ধারকের ফাঁক K ধ্রুবকের পরাবৈদ্যুতিক পাত দিয়ে ভরা হল। কী হয়?", ["ধারকত্ব K গুণ বাড়ে আর বিভব K গুণ কমে", "ধারকত্ব K গুণ কমে", "আধান K গুণ বাড়ে", "কিছুই বদলায় না"],
        "ব্যাটারি নেই বলে আধান স্থির; C = Kε₀A/d বাড়ে, তাই V = Q/C কমে।"),
    mcq("Kirchhoff's junction rule is a statement of which conservation law?", ["Conservation of charge", "Conservation of energy", "Conservation of momentum", "Conservation of mass"], 0,
        "Charge cannot pile up at a junction, so current in equals current out. The loop rule expresses energy conservation.",
        "কির্শফের সংযোগ-সূত্র কোন সংরক্ষণ-সূত্রের প্রকাশ?", ["আধানের সংরক্ষণ", "শক্তির সংরক্ষণ", "ভরবেগের সংরক্ষণ", "ভরের সংরক্ষণ"],
        "সংযোগবিন্দুতে আধান জমতে পারে না, তাই ঢোকা প্রবাহ = বেরোনো প্রবাহ। লুপ-সূত্র শক্তির সংরক্ষণ বোঝায়।"),
    mcq("Electron drift speed in a copper wire is only about a millimetre per second. Why does a bulb light at once?", ["The electric field travels along the wire almost at light speed", "Electrons jump from the switch to the bulb", "The bulb stores charge", "Copper has no resistance"], 0,
        "Electrons are already everywhere in the wire; the field that pushes them all is set up nearly instantly.",
        "তামার তারে ইলেকট্রনের সঞ্চরণ-বেগ সেকেন্ডে মাত্র এক মিলিমিটারের মতো। তবু বাল্ব সঙ্গে সঙ্গে জ্বলে কেন?", ["তড়িৎক্ষেত্র তার বরাবর প্রায় আলোর বেগে ছড়ায়", "ইলেকট্রন সুইচ থেকে লাফিয়ে বাল্বে যায়", "বাল্ব আধান জমিয়ে রাখে", "তামার কোনো রোধ নেই"],
        "তারের সর্বত্র আগে থেকেই ইলেকট্রন আছে; যে ক্ষেত্র সবাইকে ঠেলে তা প্রায় সঙ্গে সঙ্গে তৈরি হয়।"),
    mcq("How does resistance change with temperature for a metal and for a pure semiconductor?", ["Metal's rises, semiconductor's falls", "Both rise", "Both fall", "Metal's falls, semiconductor's rises"], 0,
        "Hotter metal lattices scatter electrons more; in semiconductors heat frees many more charge carriers.",
        "তাপমাত্রার সঙ্গে ধাতু আর বিশুদ্ধ অর্ধপরিবাহীর রোধ কীভাবে বদলায়?", ["ধাতুর বাড়ে, অর্ধপরিবাহীর কমে", "দুটোরই বাড়ে", "দুটোরই কমে", "ধাতুর কমে, অর্ধপরিবাহীর বাড়ে"],
        "গরম ধাতব কেলাস ইলেকট্রনকে বেশি বিক্ষিপ্ত করে; অর্ধপরিবাহীতে তাপ অনেক বেশি আধান-বাহক মুক্ত করে।"),
    mcq("How much work does a steady magnetic field do on a moving charge?", ["None - the force is always perpendicular to the velocity", "qvB per metre", "It doubles its kinetic energy", "It depends on the charge's sign"], 0,
        "F = qv x B is perpendicular to v, so speed and kinetic energy stay constant; only the direction changes.",
        "স্থির চৌম্বকক্ষেত্র একটা চলমান আধানের উপর কত কাজ করে?", ["কোনো কাজ নয় - বল সবসময় বেগের লম্ব", "প্রতি মিটারে qvB", "গতিশক্তি দ্বিগুণ করে", "আধানের চিহ্নের উপর নির্ভর করে"],
        "F = qv x B বেগের লম্ব, তাই দ্রুতি আর গতিশক্তি স্থির থাকে; কেবল দিক বদলায়।"),
    mcq("Above its Curie temperature, a ferromagnet becomes…", ["Paramagnetic", "Diamagnetic", "A superconductor", "More strongly magnetic"], 0,
        "Thermal agitation destroys the aligned domains; for iron this happens near 770°C.",
        "কুরি তাপমাত্রার উপরে একটা ফেরোচৌম্বক পদার্থ হয়ে যায়…", ["অনুচৌম্বক", "তিরশ্চৌম্বক", "অতিপরিবাহী", "আরও শক্তিশালী চুম্বক"],
        "তাপীয় আলোড়ন সাজানো ডোমেনগুলো ভেঙে দেয়; লোহার ক্ষেত্রে এটা প্রায় 770°C-এ ঘটে।"),
    mcq("Lenz's law, that an induced current opposes the change causing it, follows from…", ["Conservation of energy", "Conservation of charge", "Coulomb's law", "Ohm's law"], 0,
        "If the induced current aided the change, it would create energy from nothing.",
        "লেঞ্জের সূত্র - আবিষ্ট প্রবাহ তার কারণের পরিবর্তনকে বাধা দেয় - কোনটা থেকে আসে?", ["শক্তির সংরক্ষণ", "আধানের সংরক্ষণ", "কুলম্বের সূত্র", "ওহমের সূত্র"],
        "আবিষ্ট প্রবাহ পরিবর্তনকে সাহায্য করলে শূন্য থেকে শক্তি তৈরি হত।"),
    mcq("Why are transformer cores made of thin insulated laminations?", ["To cut eddy-current losses", "To increase the flux leakage", "To make the core lighter only", "To raise the resistance of the windings"], 0,
        "Laminations break up the large loops in which eddy currents would circulate and heat the core.",
        "ট্রান্সফর্মারের কোর পাতলা অন্তরিত পাত দিয়ে বানানো হয় কেন?", ["ঘূর্ণি-প্রবাহজনিত ক্ষতি কমাতে", "ফ্লাক্স-ক্ষরণ বাড়াতে", "কেবল কোর হালকা করতে", "কুণ্ডলীর রোধ বাড়াতে"],
        "পাতগুলো সেই বড় লুপগুলো ভেঙে দেয় যেখানে ঘূর্ণি-প্রবাহ ঘুরে কোর গরম করত।"),
    mcq("In a purely inductive AC circuit, how is the current related to the voltage?", ["Current lags voltage by 90°", "Current leads voltage by 90°", "They are in phase", "Current lags by 180°"], 0,
        "The inductor's back-emf L dI/dt equals V, so I peaks a quarter-cycle after V; no average power is used.",
        "বিশুদ্ধ আবেশী পরিবর্তী-প্রবাহ বর্তনীতে প্রবাহ বিভবের সঙ্গে কীভাবে সম্পর্কিত?", ["প্রবাহ বিভবের চেয়ে 90° পিছিয়ে", "প্রবাহ বিভবের চেয়ে 90° এগিয়ে", "দুটো একই দশায়", "প্রবাহ 180° পিছিয়ে"],
        "আবেশকের বিপরীত তড়িচ্চালক বল L dI/dt = V, তাই I শীর্ষে পৌঁছায় V-এর এক-চতুর্থাংশ চক্র পরে; গড় ক্ষমতা খরচ হয় না।"),
    mcq("At resonance in a series LCR circuit…", ["Impedance is minimum and equals R", "Impedance is maximum", "Current is zero", "Power factor is zero"], 0,
        "X_L = X_C, so they cancel: Z = R, the current peaks and the power factor is 1. Radio tuning uses this.",
        "শ্রেণি LCR বর্তনীর অনুনাদে…", ["প্রতিবাধা ন্যূনতম আর R-এর সমান", "প্রতিবাধা সর্বোচ্চ", "প্রবাহ শূন্য", "ক্ষমতা-গুণক শূন্য"],
        "X_L = X_C, তাই কাটাকাটি হয়: Z = R, প্রবাহ সর্বোচ্চ আর ক্ষমতা-গুণক 1। রেডিও টিউনিং এটা কাজে লাগায়।"),
    mcq("Why can't a transformer step up a steady DC voltage?", ["Induction needs a changing flux; steady DC gives none", "DC damages the iron core instantly", "DC flows only in the secondary", "Transformers have no primary coil"], 0,
        "With constant current the flux is constant, so no emf is induced in the secondary.",
        "ট্রান্সফর্মার স্থির সমপ্রবাহ বিভব বাড়াতে পারে না কেন?", ["আবেশের জন্য পরিবর্তনশীল ফ্লাক্স চাই; স্থির সমপ্রবাহ তা দেয় না", "সমপ্রবাহ সঙ্গে সঙ্গে লোহার কোর নষ্ট করে", "সমপ্রবাহ কেবল গৌণে চলে", "ট্রান্সফর্মারে মুখ্য কুণ্ডলী নেই"],
        "প্রবাহ স্থির হলে ফ্লাক্সও স্থির, তাই গৌণ কুণ্ডলীতে কোনো তড়িচ্চালক বল আবিষ্ট হয় না।"),
    mcq("Which list puts electromagnetic waves in order of increasing frequency?", ["Radio, microwave, infrared, visible, ultraviolet, X-ray, gamma", "Gamma, X-ray, visible, radio", "Visible, radio, X-ray, infrared", "Microwave, radio, gamma, visible"], 0,
        "All travel at c in vacuum; frequency rises (and wavelength falls) from radio to gamma rays.",
        "কোন তালিকায় তড়িৎচুম্বকীয় তরঙ্গ কম্পাঙ্ক বাড়ার ক্রমে সাজানো?", ["রেডিও, মাইক্রোতরঙ্গ, অবলোহিত, দৃশ্যমান, অতিবেগুনি, এক্স-রশ্মি, গামা", "গামা, এক্স-রশ্মি, দৃশ্যমান, রেডিও", "দৃশ্যমান, রেডিও, এক্স-রশ্মি, অবলোহিত", "মাইক্রোতরঙ্গ, রেডিও, গামা, দৃশ্যমান"],
        "শূন্যে সবাই c বেগে চলে; রেডিও থেকে গামার দিকে কম্পাঙ্ক বাড়ে (তরঙ্গদৈর্ঘ্য কমে)।"),
    mcq("Why is the clear daytime sky blue?", ["Air scatters short wavelengths far more strongly (∝ 1/λ⁴)", "The ocean reflects onto the sky", "Blue light is absorbed by ozone", "The Sun emits mostly blue light"], 0,
        "Rayleigh scattering favours blue; at sunset the long path leaves mostly red light.",
        "পরিষ্কার দিনের আকাশ নীল কেন?", ["বাতাস ছোট তরঙ্গদৈর্ঘ্য অনেক বেশি বিক্ষিপ্ত করে (∝ 1/λ⁴)", "সমুদ্র আকাশে প্রতিফলিত হয়", "ওজোন নীল আলো শোষণ করে", "সূর্য প্রধানত নীল আলো দেয়"],
        "র‍্যালে বিক্ষেপ নীলকে বেশি ছড়ায়; সূর্যাস্তে লম্বা পথ পেরিয়ে প্রধানত লাল আলো থাকে।"),
    mcq("Which colour is deviated most by a glass prism?", ["Violet", "Red", "Yellow", "Green"], 0,
        "Glass's refractive index is largest for short wavelengths, so violet bends most - this is dispersion.",
        "কাচের প্রিজমে কোন রং সবচেয়ে বেশি বিচ্যুত হয়?", ["বেগুনি", "লাল", "হলুদ", "সবুজ"],
        "ছোট তরঙ্গদৈর্ঘ্যে কাচের প্রতিসরাঙ্ক সবচেয়ে বেশি, তাই বেগুনি সবচেয়ে বেশি বাঁকে - এটাই বিচ্ছুরণ।"),
    mcq("What is needed to see a steady interference pattern?", ["Two coherent sources with a constant phase difference", "Two independent bulbs", "Any two sources of different colours", "A single very bright source only"], 0,
        "Independent sources change phase randomly; Young split one source into two slits to make them coherent.",
        "স্থির ব্যতিচার-নকশা দেখতে কী লাগে?", ["স্থির দশা-পার্থক্যের দুটো সুসংগত উৎস", "দুটো স্বাধীন বাল্ব", "ভিন্ন রঙের যেকোনো দুটো উৎস", "কেবল একটা খুব উজ্জ্বল উৎস"],
        "স্বাধীন উৎসের দশা এলোমেলো বদলায়; ইয়ং একটা উৎসকে দুটো ছিদ্রে ভাগ করে সুসংগত করেছিলেন।"),
    mcq("In single-slit diffraction, how wide is the central bright band compared with the others?", ["Twice as wide", "The same width", "Half as wide", "Four times as wide"], 0,
        "The central maximum spans from -λ/a to +λ/a in angle; each secondary maximum spans only λ/a.",
        "একক-ছিদ্র অপবর্তনে মাঝের উজ্জ্বল পটি অন্যগুলোর তুলনায় কতটা চওড়া?", ["দ্বিগুণ চওড়া", "একই চওড়া", "অর্ধেক চওড়া", "চার গুণ চওড়া"],
        "কেন্দ্রীয় চরম কোণে -λ/a থেকে +λ/a পর্যন্ত; প্রতিটি গৌণ চরম কেবল λ/a।"),
    mcq("What does the polarisation of light prove?", ["Light is a transverse wave", "Light is a longitudinal wave", "Light is made of particles only", "Light needs a medium"], 0,
        "Only transverse vibrations can be confined to one plane; sound in air cannot be polarised.",
        "আলোর সমবর্তন কী প্রমাণ করে?", ["আলো তির্যক তরঙ্গ", "আলো অনুদৈর্ঘ্য তরঙ্গ", "আলো কেবল কণা দিয়ে তৈরি", "আলোর মাধ্যম লাগে"],
        "কেবল তির্যক কম্পনকেই একটা তলে সীমাবদ্ধ করা যায়; বাতাসে শব্দকে সমবর্তিত করা যায় না।"),
    mcq("In the photoelectric effect, increasing the light's intensity (same frequency) increases…", ["The number of electrons emitted, not their maximum energy", "The maximum kinetic energy", "The work function", "The threshold frequency"], 0,
        "Each photon frees at most one electron with energy hf - φ; more photons mean more electrons.",
        "আলোক-তড়িৎ ক্রিয়ায় আলোর তীব্রতা বাড়ালে (একই কম্পাঙ্ক) কী বাড়ে?", ["নির্গত ইলেকট্রনের সংখ্যা, তাদের সর্বোচ্চ শক্তি নয়", "সর্বোচ্চ গতিশক্তি", "কার্য-অপেক্ষক", "সূচন-কম্পাঙ্ক"],
        "প্রতিটি ফোটন সর্বোচ্চ একটা ইলেকট্রন hf - φ শক্তিতে মুক্ত করে; বেশি ফোটন মানে বেশি ইলেকট্রন।"),
    mcq("What did the Davisson-Germer experiment demonstrate?", ["The wave nature of electrons", "The particle nature of light", "The existence of the nucleus", "The charge of the electron"], 0,
        "Electrons scattered from a nickel crystal gave diffraction peaks matching λ = h/p.",
        "ডেভিসন-জার্মার পরীক্ষা কী দেখিয়েছিল?", ["ইলেকট্রনের তরঙ্গ-প্রকৃতি", "আলোর কণা-প্রকৃতি", "নিউক্লিয়াসের অস্তিত্ব", "ইলেকট্রনের আধান"],
        "নিকেল কেলাস থেকে বিক্ষিপ্ত ইলেকট্রন λ = h/p-এর সঙ্গে মেলা অপবর্তন-শীর্ষ দিয়েছিল।"),
    mcq("Which nucleus has about the highest binding energy per nucleon?", ["Iron-56", "Uranium-235", "Helium-4", "Hydrogen-2"], 0,
        "Near iron nuclei are most tightly bound, so fusing light nuclei or splitting heavy ones both release energy.",
        "কোন নিউক্লিয়াসের নিউক্লিয়ন-প্রতি বন্ধনশক্তি প্রায় সবচেয়ে বেশি?", ["লোহা-56", "ইউরেনিয়াম-235", "হিলিয়াম-4", "হাইড্রোজেন-2"],
        "লোহার কাছাকাছি নিউক্লিয়াস সবচেয়ে দৃঢ়ভাবে আবদ্ধ, তাই হালকা নিউক্লিয়াস জোড়া বা ভারী নিউক্লিয়াস ভাঙা দুটোতেই শক্তি মুক্ত হয়।"),
    mcq("Which statement about nuclear forces is true?", ["They are short-range and nearly charge-independent", "They act over kilometres", "They act only between protons", "They are weaker than gravity"], 0,
        "They bind protons and neutrons alike within about 2-3 fm, and are the strongest force at that range.",
        "নিউক্লীয় বল সম্পর্কে কোন কথাটা সত্য?", ["স্বল্প-পাল্লার আর প্রায় আধান-নিরপেক্ষ", "কিলোমিটার জুড়ে কাজ করে", "কেবল প্রোটনের মধ্যে কাজ করে", "অভিকর্ষের চেয়ে দুর্বল"],
        "প্রায় 2-3 fm-এর মধ্যে এটা প্রোটন আর নিউট্রনকে সমানভাবে বাঁধে, ওই দূরত্বে সবচেয়ে শক্তিশালী বল।"),
    mcq("Doping pure silicon with a pentavalent element such as phosphorus produces…", ["An n-type semiconductor", "A p-type semiconductor", "An insulator", "A superconductor"], 0,
        "The fifth valence electron is loosely bound and becomes a free carrier; electrons are the majority carriers.",
        "বিশুদ্ধ সিলিকনে ফসফরাসের মতো পঞ্চযোজী মৌল মেশালে কী তৈরি হয়?", ["n-টাইপ অর্ধপরিবাহী", "p-টাইপ অর্ধপরিবাহী", "অন্তরক", "অতিপরিবাহী"],
        "পঞ্চম যোজ্যতা-ইলেকট্রন আলগাভাবে আবদ্ধ থাকে আর মুক্ত বাহক হয়; ইলেকট্রনই সংখ্যাগুরু বাহক।"),
    mcq("What happens to the depletion layer of a p-n junction under reverse bias?", ["It widens", "It disappears", "It narrows", "It stays the same"], 0,
        "The applied field pulls carriers away from the junction, so only a tiny leakage current flows.",
        "বিপরীত ঝোঁকে p-n সংযোগের নিঃশেষিত স্তরের কী হয়?", ["চওড়া হয়", "মিলিয়ে যায়", "সরু হয়", "একই থাকে"],
        "প্রযুক্ত ক্ষেত্র বাহকদের সংযোগ থেকে দূরে টানে, তাই কেবল সামান্য ক্ষরণ-প্রবাহ চলে।"),
    mcq("What is a Zener diode mainly used for?", ["Voltage regulation", "Amplifying signals", "Emitting light", "Rectifying high power AC"], 0,
        "In reverse breakdown its voltage stays nearly fixed over a wide current range.",
        "জেনার ডায়োড প্রধানত কী কাজে লাগে?", ["বিভব নিয়ন্ত্রণে", "সংকেত বিবর্ধনে", "আলো দিতে", "উচ্চ-ক্ষমতার পরিবর্তী প্রবাহ একমুখী করতে"],
        "বিপরীত ভাঙনে বিস্তৃত প্রবাহ-পাল্লায় এর বিভব প্রায় স্থির থাকে।"),
    mcq("Which logic gate is called 'universal' because any circuit can be built from it alone?", ["NAND", "OR", "XOR", "NOT"], 0,
        "NAND (like NOR) can make NOT, AND and OR, so it can build any digital circuit.",
        "কোন লজিক গেটকে 'সর্বজনীন' বলা হয়, কারণ শুধু তা দিয়েই যেকোনো বর্তনী বানানো যায়?", ["NAND গেট", "OR গেট", "XOR গেট", "NOT গেট"],
        "NAND (NOR-এর মতো) দিয়ে NOT, AND আর OR বানানো যায়, তাই যেকোনো ডিজিটাল বর্তনী তৈরি হয়।"),
    mcq("A full-wave rectifier is fed 50 Hz AC. What is the main ripple frequency of its output?", ["100 Hz", "50 Hz", "25 Hz", "0 Hz"], 0,
        "Both half-cycles give a pulse, so the output repeats twice per input cycle.",
        "একটা পূর্ণ-তরঙ্গ একমুখীকারককে 50 Hz পরিবর্তী প্রবাহ দেওয়া হল। আউটপুটের প্রধান উর্মি-কম্পাঙ্ক কত?", ["100 Hz", "50 Hz", "25 Hz", "0 Hz"],
        "দুই অর্ধচক্রই একটা করে স্পন্দন দেয়, তাই প্রতি ইনপুট-চক্রে আউটপুট দুবার পুনরাবৃত্ত হয়।"),
    mcq("A wire is stretched to twice its length (volume unchanged). What happens to its resistance?", ["It becomes 4 times", "It doubles", "It halves", "It is unchanged"], 0,
        "Length doubles and area halves, so R = ρL/A rises by 2 x 2 = 4.",
        "একটা তারকে টেনে দ্বিগুণ লম্বা করা হল (আয়তন অপরিবর্তিত)। এর রোধের কী হয়?", ["4 গুণ হয়", "দ্বিগুণ হয়", "অর্ধেক হয়", "অপরিবর্তিত থাকে"],
        "দৈর্ঘ্য দ্বিগুণ আর প্রস্থচ্ছেদ অর্ধেক, তাই R = ρL/A বাড়ে 2 x 2 = 4 গুণ।"),
    mcq("Two springs of stiffness k each are joined in series. What is the combined stiffness?", ["k/2", "2k", "k", "k²"], 0,
        "In series the extensions add: 1/k_eq = 1/k + 1/k. In parallel the stiffnesses add to 2k.",
        "k দৃঢ়তার দুটো স্প্রিং শ্রেণিতে জোড়া হল। মিলিত দৃঢ়তা কত?", ["k/2", "2k", "k", "k²"],
        "শ্রেণিতে প্রসারণ যোগ হয়: 1/k_eq = 1/k + 1/k। সমান্তরালে দৃঢ়তা যোগ হয়ে 2k হয়।"),
    mcq("A man in a lift weighs himself while the lift accelerates upward at a. What does the scale read?", ["m(g + a)", "m(g - a)", "mg", "Zero"], 0,
        "The floor must supply mg plus the extra force ma to accelerate him upward.",
        "উপরের দিকে a ত্বরণে চলা লিফটে একজন নিজের ওজন মাপছেন। যন্ত্রে কী পাঠ দেখায়?", ["m(g + a)", "m(g - a)", "mg", "শূন্য"],
        "মেঝেকে mg-র সঙ্গে তাঁকে উপরে ত্বরিত করার অতিরিক্ত ma বলও দিতে হয়।"),
    mcq("A body moves in a circle at constant speed. Which statement is true?", ["Its velocity changes, so it accelerates towards the centre", "Its acceleration is zero", "No net force acts on it", "Its velocity is constant"], 0,
        "Direction keeps changing; the centripetal acceleration v²/r needs a net inward force.",
        "একটা বস্তু স্থির দ্রুতিতে বৃত্তপথে চলছে। কোন কথাটা সত্য?", ["বেগ বদলাচ্ছে, তাই কেন্দ্রের দিকে ত্বরণ আছে", "ত্বরণ শূন্য", "কোনো মোট বল কাজ করে না", "বেগ স্থির"],
        "দিক বদলাতে থাকে; কেন্দ্রমুখী ত্বরণ v²/r-এর জন্য ভেতরমুখী মোট বল লাগে।"),
    mcq("What is the moment of inertia of a thin rod of mass M and length L about an axis through one end, perpendicular to it?", ["ML²/3", "ML²/12", "ML²/2", "ML²"], 0,
        "About the centre it is ML²/12; the parallel-axis theorem adds M(L/2)² = ML²/4, giving ML²/3.",
        "M ভর আর L দৈর্ঘ্যের একটা সরু দণ্ডের এক প্রান্ত দিয়ে লম্বভাবে যাওয়া অক্ষের সাপেক্ষে জড়তা-ভ্রামক কত?", ["ML²/3", "ML²/12", "ML²/2", "ML²"],
        "কেন্দ্রের সাপেক্ষে ML²/12; সমান্তরাল-অক্ষ উপপাদ্য M(L/2)² = ML²/4 যোগ করে, তাই ML²/3।"),
    mcq("An object is placed between the focus and the pole of a concave mirror. What kind of image forms?", ["Virtual, erect and magnified", "Real, inverted and diminished", "Real and the same size", "No image at all"], 0,
        "The reflected rays diverge; extended back they meet behind the mirror - the principle of a shaving mirror.",
        "অবতল দর্পণের ফোকাস আর মেরুর মাঝে একটা বস্তু রাখা হল। কেমন প্রতিবিম্ব হয়?", ["অসদ, সোজা আর বিবর্ধিত", "সদ, উল্টো আর ক্ষুদ্রতর", "সদ আর সমান মাপের", "কোনো প্রতিবিম্বই নয়"],
        "প্রতিফলিত রশ্মি অপসারী; পেছনে বাড়ালে দর্পণের পেছনে মেলে - দাড়ি কামানোর আয়নার নীতি।"),
    mcq("Optical fibres carry light over long distances by…", ["Repeated total internal reflection", "Diffraction at the core", "Absorption and re-emission", "Polarisation"], 0,
        "The core's refractive index is higher than the cladding's, so rays hitting the wall beyond the critical angle stay inside.",
        "আলোকতন্তু দীর্ঘ পথে আলো বয়ে নেয় কীভাবে?", ["বারবার পূর্ণ অভ্যন্তরীণ প্রতিফলনে", "কোরে অপবর্তনে", "শোষণ আর পুনঃনিঃসরণে", "সমবর্তনে"],
        "কোরের প্রতিসরাঙ্ক আবরণের চেয়ে বেশি, তাই সংকট কোণের বেশি কোণে দেয়ালে পড়া রশ্মি ভেতরেই থাকে।"),
    mcq("Why is a carrier wave modulated for radio broadcasting instead of sending audio directly?", ["Antennas for audio frequencies would be kilometres long", "Audio waves travel faster than light", "Audio cannot be amplified", "Modulation removes all noise"], 0,
        "An antenna should be about λ/4; a 10 kHz signal has λ = 30 km. High-frequency carriers allow small antennas and many channels.",
        "রেডিও সম্প্রচারে সরাসরি শব্দ-সংকেত না পাঠিয়ে বাহক-তরঙ্গকে মডুলেট করা হয় কেন?", ["শব্দ-কম্পাঙ্কের অ্যান্টেনা কয়েক কিলোমিটার লম্বা হত", "শব্দ-তরঙ্গ আলোর চেয়ে দ্রুত চলে", "শব্দ-সংকেত বিবর্ধন করা যায় না", "মডুলেশন সব শব্দদূষণ দূর করে"],
        "অ্যান্টেনা প্রায় λ/4 হওয়া উচিত; 10 kHz সংকেতের λ = 30 km। উচ্চ-কম্পাঙ্কের বাহক ছোট অ্যান্টেনা আর অনেক চ্যানেল সম্ভব করে।"),
    mcq("Which quantity is dimensionless?", ["Strain", "Stress", "Young's modulus", "Pressure"], 0,
        "Strain is a length divided by a length; stress, modulus and pressure all have units of N/m².",
        "কোন রাশিটা মাত্রাহীন?", ["বিকৃতি", "পীড়ন", "ইয়ং গুণাঙ্ক", "চাপ"],
        "বিকৃতি হলো দৈর্ঘ্য ভাগ দৈর্ঘ্য; পীড়ন, গুণাঙ্ক আর চাপ সবার একক N/m²।"),
    mcq("A force F = -kx acts on a particle. What is its potential energy?", ["½kx²", "-kx", "kx²", "-½kx²"], 0,
        "F = -dU/dx, so U = ½kx² (taking U = 0 at x = 0) - the spring's stored energy.",
        "একটা কণার উপর F = -kx বল কাজ করে। এর স্থিতিশক্তি কত?", ["½kx²", "-kx", "kx²", "-½kx²"],
        "F = -dU/dx, তাই U = ½kx² (x = 0-তে U = 0 ধরে) - স্প্রিংয়ে জমা শক্তি।"),
    mcq("What is the work done by the tension in a string that keeps a stone moving in a horizontal circle?", ["Zero", "T x 2πr per turn", "mv² per turn", "Negative"], 0,
        "Tension points to the centre, perpendicular to the motion at every instant.",
        "অনুভূমিক বৃত্তে একটা পাথর ঘোরানো সুতোর টান কত কাজ করে?", ["শূন্য", "প্রতি পাকে T x 2πr", "প্রতি পাকে mv²", "ঋণাত্মক"],
        "টান কেন্দ্রমুখী, প্রতি মুহূর্তে গতির লম্ব।"),
    mcq("Bernoulli's principle explains the lift on an aircraft wing because…", ["Faster air above the wing has lower pressure than the air below", "The wing is lighter than air", "Air below the wing moves faster", "Engines push the wing up"], 0,
        "Along a streamline P + ½ρv² + ρgh is constant; the pressure difference times wing area gives lift.",
        "বার্নুলির নীতি বিমানের ডানার উত্থান-বল ব্যাখ্যা করে কারণ…", ["ডানার উপরের দ্রুত বাতাসের চাপ নিচের বাতাসের চেয়ে কম", "ডানা বাতাসের চেয়ে হালকা", "ডানার নিচের বাতাস দ্রুত চলে", "ইঞ্জিন ডানাকে উপরে ঠেলে"],
        "প্রবাহরেখা বরাবর P + ½ρv² + ρgh স্থির; চাপের পার্থক্য গুণ ডানার ক্ষেত্রফল = উত্থান-বল।"),
    mcq("Two waves of the same frequency meet in phase. What is the resulting intensity compared with one wave alone?", ["4 times", "2 times", "The same", "Zero"], 0,
        "Amplitudes add to 2A, and intensity ∝ amplitude², so it becomes 4I; energy is redistributed, dark fringes get none.",
        "একই কম্পাঙ্কের দুটো তরঙ্গ একই দশায় মেলে। একটা তরঙ্গের তুলনায় ফলস্বরূপ তীব্রতা কত?", ["4 গুণ", "2 গুণ", "একই", "শূন্য"],
        "বিস্তার যোগ হয়ে 2A, আর তীব্রতা ∝ বিস্তার², তাই 4I; শক্তি পুনর্বণ্টিত হয়, অন্ধকার ঝালর কিছুই পায় না।"),
    mcq("A charged particle enters a uniform magnetic field at an angle (not 0° or 90°). What path does it follow?", ["A helix", "A straight line", "A circle", "A parabola"], 0,
        "The velocity component along B is unchanged while the perpendicular part circles - together, a helix.",
        "একটা আহিত কণা কোণে (0° বা 90° নয়) সুষম চৌম্বকক্ষেত্রে প্রবেশ করে। এটা কোন পথে চলে?", ["কুণ্ডলী (হেলিক্স)", "সরলরেখা", "বৃত্ত", "অধিবৃত্ত"],
        "B বরাবর বেগের উপাংশ অপরিবর্তিত থাকে আর লম্ব অংশ বৃত্তে ঘোরে - মিলে কুণ্ডলী।"),
    mcq("What is the SI unit of magnetic flux?", ["Weber", "Tesla", "Henry", "Gauss"], 0,
        "1 Wb = 1 T m². The tesla measures flux density, the henry measures inductance.",
        "চৌম্বক ফ্লাক্সের SI একক কী?", ["ওয়েবার", "টেসলা", "হেনরি", "গাউস"],
        "1 Wb = 1 T m²। টেসলা ফ্লাক্স-ঘনত্ব মাপে, হেনরি আবেশাঙ্ক মাপে।"),
    mcq("If the distance between two point charges is halved, the force between them…", ["Becomes 4 times", "Doubles", "Halves", "Becomes a quarter"], 0,
        "Coulomb's force ∝ 1/r², so halving r multiplies it by 4.",
        "দুটো বিন্দু-আধানের দূরত্ব অর্ধেক করলে তাদের মধ্যে বল…", ["4 গুণ হয়", "দ্বিগুণ হয়", "অর্ধেক হয়", "এক-চতুর্থাংশ হয়"],
        "কুলম্ব বল ∝ 1/r², তাই r অর্ধেক হলে বল 4 গুণ।"),
    mcq("Which law of thermodynamics rules out an engine that turns all absorbed heat into work in a cycle?", ["The second law", "The first law", "The zeroth law", "The third law"], 0,
        "Kelvin-Planck statement: some heat must be rejected to a colder reservoir, so efficiency is always below 100%.",
        "তাপগতিবিদ্যার কোন সূত্র এমন ইঞ্জিন অসম্ভব বলে, যা এক চক্রে শোষিত সব তাপকে কাজে পরিণত করে?", ["দ্বিতীয় সূত্র", "প্রথম সূত্র", "শূন্যতম সূত্র", "তৃতীয় সূত্র"],
        "কেলভিন-প্ল্যাঙ্ক বিবৃতি: কিছু তাপ শীতলতর আধারে ছাড়তেই হবে, তাই দক্ষতা সবসময় 100%-এর কম।"),
    mcq("A satellite's orbit radius is increased. What happens to its orbital speed?", ["It decreases", "It increases", "It stays the same", "It becomes zero"], 0,
        "v = √(GM/r): farther satellites move more slowly and take longer per orbit.",
        "একটা উপগ্রহের কক্ষ-ব্যাসার্ধ বাড়ানো হল। এর কক্ষীয় বেগের কী হয়?", ["কমে", "বাড়ে", "একই থাকে", "শূন্য হয়"],
        "v = √(GM/r): দূরের উপগ্রহ ধীরে চলে আর প্রতি পাকে বেশি সময় নেয়।"),
    mcq("A ray of light passes through the optical centre of a thin lens. What happens to it?", ["It goes straight through, undeviated", "It is bent towards the focus", "It is reflected back", "It is split into colours"], 0,
        "Near the centre the two lens faces are almost parallel, like a thin glass slab, so the ray is not deviated.",
        "পাতলা লেন্সের আলোককেন্দ্র দিয়ে একটা আলোকরশ্মি যায়। এর কী হয়?", ["বিচ্যুত না হয়ে সোজা চলে যায়", "ফোকাসের দিকে বাঁকে", "পেছনে প্রতিফলিত হয়", "রঙে ভাগ হয়ে যায়"],
        "কেন্দ্রের কাছে লেন্সের দুই তল প্রায় সমান্তরাল, পাতলা কাচের পাতের মতো, তাই রশ্মি বিচ্যুত হয় না।"),
    mcq("What is the resistance of an ideal ammeter and of an ideal voltmeter?", ["Ammeter zero, voltmeter infinite", "Both zero", "Both infinite", "Ammeter infinite, voltmeter zero"], 0,
        "An ammeter in series must not add resistance; a voltmeter in parallel must draw no current.",
        "আদর্শ অ্যামমিটার আর আদর্শ ভোল্টমিটারের রোধ কত?", ["অ্যামমিটার শূন্য, ভোল্টমিটার অসীম", "দুটোই শূন্য", "দুটোই অসীম", "অ্যামমিটার অসীম, ভোল্টমিটার শূন্য"],
        "শ্রেণিতে বসা অ্যামমিটার রোধ যোগ করবে না; সমান্তরালে বসা ভোল্টমিটার কোনো প্রবাহ টানবে না।"),
    mcq("A particle moves in a circle of radius r with speed v. Its centripetal acceleration is:", ["v²/r directed toward the centre", "v²r directed outward", "vr toward the centre", "v/r²"], 0,
        "a_c = v²/r = ω²r. Bridge cable bands maintain centripetal forces on curved spans.",
        "একটা কণা r ব্যাসার্ধের বৃত্তে v বেগে চলছে। কেন্দ্রমুখী ত্বরণ:", ["v²/r কেন্দ্রের দিকে", "v²r বাইরের দিকে", "vr কেন্দ্রের দিকে", "v/r²"],
        "a_c = v²/r = ω²r। বাঁকা বিস্তারে সেতু তারের বন্ধনী কেন্দ্রমুখী বল বজায় রাখে।"),
    mcq("Newton's second law for rotation is τ = Iα. What does I represent?", ["Moment of inertia — the rotational analogue of mass (I = Σmᵢrᵢ²)", "Angular impulse", "Rotational kinetic energy", "Torque per radian"], 0,
        "Hollow cylinders have larger I than solid ones of same mass. Bridge cable drums use solid cores to ease starting.",
        "ঘূর্ণনের নিউটনের দ্বিতীয় সূত্র τ = Iα। I কী?", ["জড়তার ভ্রামক — ভরের ঘূর্ণন সমতুল্য (I = Σmᵢrᵢ²)", "কৌণিক ঘাত-বল", "ঘূর্ণন গতিশক্তি", "রেডিয়ান-প্রতি টর্ক"],
        "ফাঁপা সিলিন্ডারের I বেশি একই ভরের কঠিনের চেয়ে। সেতু তারের ড্রামে ঘূর্ণন শুরু সহজ করতে কঠিন কোর।"),
    mcq("Conservation of angular momentum explains why a spinning figure skater speeds up when they pull in their arms because:", ["Reducing r decreases I, so ω increases to keep Iω constant", "They gain energy from the air", "Friction pushes them faster", "Mass is lost"], 0,
        "Same principle: a bridge cable reel speeds up as radius decreases during unwinding.",
        "ঘূর্ণায়মান স্কেটার হাত গুটিয়ে নিলে কৌণিক ভরবেগের সংরক্ষণ দ্রুততার ব্যাখ্যা:", ["r কমলে I কমে, তাই Iω ধ্রুবক রাখতে ω বাড়ে", "বায়ু থেকে শক্তি পান", "ঘর্ষণ দ্রুত করে", "ভর হারায়"],
        "একই নীতি: সেতু তারের রিল খোলার সময় ব্যাসার্ধ কমলে দ্রুততা বাড়ে।"),
    mcq("At what angle θ to the horizontal should a projectile be launched for maximum range on level ground?", ["45°", "60°", "30°", "90°"], 0,
        "R = u² sin2θ/g is maximum when sin2θ = 1, i.e. θ = 45°.",
        "সমতল মাটিতে সর্বোচ্চ পরিসীমার জন্য প্রক্ষেপ কোণ:", ["45°", "60°", "30°", "90°"],
        "R = u² sin2θ/g সর্বোচ্চ যখন sin2θ = 1, অর্থাৎ θ = 45°।"),
    mcq("The work-energy theorem states:", ["Net work done on an object equals its change in kinetic energy (W_net = ΔKE)", "Work done equals change in potential energy", "Kinetic energy is always conserved", "Power equals work done"], 0,
        "A vehicle braking on a bridge does negative work, reducing KE to zero.",
        "কাজ-শক্তি উপপাদ্য:", ["বস্তুতে কৃত মোট কাজ = গতিশক্তির পরিবর্তন (W_নেট = ΔKE)", "কৃতকাজ = স্থিতিশক্তির পরিবর্তন", "গতিশক্তি সবসময় সংরক্ষিত", "ক্ষমতা = কৃতকাজ"],
        "সেতুতে গাড়ি ব্রেক করলে ঋণাত্মক কাজ হয়, গতিশক্তি শূন্যে নামে।"),
    mcq("A perfectly inelastic collision is one where:", ["The bodies stick together after collision — kinetic energy is not conserved but momentum is", "Both KE and momentum are conserved", "Energy is conserved but momentum is not", "The bodies pass through each other"], 0,
        "Impact of a mass dropped on a bridge deck is nearly perfectly inelastic.",
        "পূর্ণ-অস্থিতিস্থাপক সংঘর্ষ কোনটা:", ["সংঘর্ষের পর বস্তুগুলো এক হয়ে যায় — গতিশক্তি সংরক্ষিত নয়, ভরবেগ সংরক্ষিত", "KE ও ভরবেগ উভয় সংরক্ষিত", "শক্তি সংরক্ষিত, ভরবেগ নয়", "বস্তু একে অপরকে ভেদ করে"],
        "সেতুর পাটাতনে পড়া ভরের আঘাত প্রায় পূর্ণ-অস্থিতিস্থাপক।"),
    mcq("Bernoulli's principle states that for streamline flow of an ideal fluid:", ["Where speed is high, pressure is low (P + ½ρv² + ρgh = const)", "Where speed is high, pressure is high", "Pressure does not vary with speed", "Density changes with pressure"], 0,
        "Bridge wind loads use Bernoulli: high wind speed over the deck creates low pressure above, causing lift.",
        "বার্নোলির নীতি আদর্শ তরলের ধারাপ্রবাহে:", ["যেখানে বেগ বেশি, চাপ কম (P + ½ρv² + ρgh = ধ্রুবক)", "যেখানে বেগ বেশি, চাপ বেশি", "চাপ বেগের সঙ্গে পরিবর্তিত নয়", "ঘনত্ব চাপের সঙ্গে পরিবর্তিত"],
        "বায়ু ভার বার্নোলি: সেতু পাটাতনের উপর দ্রুত বায়ু কম চাপ তৈরি করে, উত্থান ঘটায়।"),
    mcq("The specific heat capacity of water (4200 J/kg·K) is much higher than steel (~500 J/kg·K). This means:", ["For the same heat added, water temperature rises much less than steel (Q = mcΔT)", "Water is a better conductor of heat", "Steel stores more heat per kilogram", "Water and steel have the same specific heat"], 0,
        "Large bridges near water bodies show less temperature variation due to water's thermal buffering.",
        "জলের আপেক্ষিক তাপ (4200 J/kg·K) ইস্পাতের (~500 J/kg·K) চেয়ে অনেক বেশি:", ["একই তাপে জলের তাপমাত্রা ইস্পাতের চেয়ে অনেক কম বাড়ে (Q = mcΔT)", "জল তাপের ভালো পরিবাহক", "ইস্পাত কেজি-প্রতি বেশি তাপ সঞ্চয় করে", "উভয়ের আপেক্ষিক তাপ একই"],
        "জলাশয়ের পাশের বড় সেতু জলের তাপ-বাফারিং-এর কারণে কম তাপমাত্রা পরিবর্তন দেখায়।"),
    mcq("Latent heat is the heat needed to change the state of a substance without changing its:", ["Temperature (e.g. L_f for melting, L_v for vaporisation)", "Mass", "Volume", "Density"], 0,
        "De-icing salt on a bridge absorbs latent heat from ice to melt it.",
        "লুক্কায়িত তাপ হল পদার্থের অবস্থা পরিবর্তনে দরকারি তাপ যা পরিবর্তন না করে:", ["তাপমাত্রা (যেমন গলনের L_f, বাষ্পায়নের L_v)", "ভর", "আয়তন", "ঘনত্ব"],
        "সেতুতে বরফ গলানোর লবণ বরফ থেকে লুক্কায়িত তাপ শুষে নেয়।"),
    mcq("Which process in the Carnot cycle is both isothermal and involves heat exchange?", ["Both the two isothermal steps (heat absorbed from hot reservoir and rejected to cold)", "Both adiabatic steps", "Only the compression step", "The cycle has no isothermal step"], 0,
        "Carnot efficiency = 1 - T_cold/T_hot. No engine working between two temperatures can exceed this.",
        "কার্নো চক্রে কোন প্রক্রিয়া সমতাপীয় এবং তাপ বিনিময় করে?", ["দুটো সমতাপীয় পদক্ষেপ (গরম উৎস থেকে তাপ শোষণ ও শীতল উৎসে তাপ ত্যাগ)", "দুটো রুদ্ধতাপীয় পদক্ষেপ", "শুধু সংকোচন পদক্ষেপ", "চক্রে সমতাপীয় পদক্ষেপ নেই"],
        "কার্নো দক্ষতা = 1 - T_ঠান্ডা/T_গরম। দুই তাপমাত্রার মধ্যে কাজ করা কোনো ইঞ্জিন এটা অতিক্রম করতে পারে না।"),
    mcq("The speed of a transverse wave on a stretched string is v = √(T/μ). If the tension is quadrupled:", ["Speed doubles (v ∝ √T)", "Speed quadruples", "Speed halves", "Speed is unchanged"], 0,
        "Bridge hanger cables are tuned — measured vibration frequency ↔ tension via this relationship.",
        "টানা সুতোয় তির্যক তরঙ্গের বেগ v = √(T/μ)। টান চারগুণ হলে:", ["বেগ দ্বিগুণ (v ∝ √T)", "বেগ চারগুণ", "বেগ অর্ধেক", "বেগ অপরিবর্তিত"],
        "সেতুর হ্যাঙ্গার তার সুর করা — পরিমাপ করা কম্পনের কম্পাঙ্ক ↔ এই সম্পর্কে টান।"),
    mcq("Resonance occurs when the frequency of the driving force equals:", ["The natural frequency of the system", "Twice the natural frequency", "Half the natural frequency", "Any frequency"], 0,
        "Tacoma Narrows Bridge (1940) collapsed because wind drove it near its torsional resonance frequency.",
        "অনুরণন ঘটে যখন চালক বলের কম্পাঙ্ক সমান হয়:", ["ব্যবস্থার স্বাভাবিক কম্পাঙ্কের", "স্বাভাবিক কম্পাঙ্কের দ্বিগুণ", "স্বাভাবিক কম্পাঙ্কের অর্ধেক", "যেকোনো কম্পাঙ্ক"],
        "ট্যাকোমা ন্যারোস ব্রিজ (1940) ধ্বংস হয় কারণ বায়ু এটাকে মোচড়ীয় অনুরণন কম্পাঙ্কের কাছে চালিত করে।"),
    mcq("Huygens' principle states that every point on a wavefront acts as:", ["A source of secondary spherical wavelets — the new wavefront is tangent to these wavelets", "A receiver of light only", "A reflector", "A point of zero amplitude"], 0,
        "Diffraction of ocean waves around bridge piers follows Huygens' principle.",
        "হাইগেন্সের নীতি: তরঙ্গ-সম্মুখের প্রতিটা বিন্দু:", ["মাধ্যমিক গোলকীয় তরঙ্গিকার উৎস হিসেবে কাজ করে — নতুন তরঙ্গ-সম্মুখ এই তরঙ্গিকাগুলোর স্পর্শক", "শুধু আলোর গ্রাহক", "প্রতিফলক", "শূন্য বিস্তারের বিন্দু"],
        "সেতুর স্তম্ভের চারপাশে সমুদ্র তরঙ্গের অপবর্তন হাইগেন্সের নীতি মেনে চলে।"),
    mcq("In thin-film interference (e.g. oil on water), the condition for constructive interference with one phase-reversal is:", ["2nt = (m + ½)λ (m = 0,1,2…), where n is refractive index, t is film thickness", "2nt = mλ", "nt = mλ", "t = mλ/n"], 0,
        "Anti-reflection coatings on bridge traffic sensors use destructive interference at design wavelength.",
        "পাতলা-ফিল্ম ব্যতিচার (যেমন জলে তেল)। একটা দশা-বিপরীতনে গঠনমূলক ব্যতিচারের শর্ত:", ["2nt = (m + ½)λ (m = 0,1,2…), n = প্রতিসরণাঙ্ক, t = ফিল্ম পুরুত্ব", "2nt = mλ", "nt = mλ", "t = mλ/n"],
        "সেতু ট্র্যাফিক সেন্সরে বিধ্বংসী ব্যতিচার ব্যবহার করে নকশা তরঙ্গদৈর্ঘ্যে আলো-বিরোধী আবরণ।"),
    mcq("The angular magnification of a simple microscope using a lens of focal length f is (for near-point viewing):", ["M = 1 + D/f, where D = 25 cm", "M = D/f", "M = f/D", "M = 1 - D/f"], 0,
        "Optical instruments inspect bridge welds and cracks; magnification formula guides lens selection.",
        "f ফোকাস-দূরত্বের লেন্সে সরল অণুবীক্ষণের কৌণিক বিবর্ধন:", ["M = 1 + D/f, D = 25 cm", "M = D/f", "M = f/D", "M = 1 - D/f"],
        "অপটিক্যাল যন্ত্র সেতুর ঝালাই ও ফাটল পরীক্ষা করে; বিবর্ধন সূত্র লেন্স নির্বাচন গাইড করে।"),
    mcq("The photoelectric threshold frequency f₀ satisfies:", ["hf₀ = φ (work function of the metal) — photons below f₀ cannot eject electrons", "hf₀ = KE_max", "f₀ = √(φ/h)", "f₀ depends only on light intensity"], 0,
        "h = 6.63×10⁻³⁴ J·s. Below f₀, no electrons regardless of intensity — a key quantum result.",
        "আলোতড়িৎ ক্রান্তি কম্পাঙ্ক f₀:", ["hf₀ = φ (ধাতুর কাজ-অপেক্ষা) — f₀-এর নিচে ফোটন ইলেকট্রন বের করতে পারে না", "hf₀ = KE_সর্বোচ্চ", "f₀ = √(φ/h)", "f₀ শুধু আলোর তীব্রতার উপর নির্ভর করে"],
        "h = 6.63×10⁻³⁴ J·s। f₀-এর নিচে তীব্রতা নির্বিশেষে কোনো ইলেকট্রন নেই — কোয়ান্টামের মূল ফলাফল।"),
    mcq("In a nuclear fission chain reaction, what is a 'critical mass'?", ["The minimum mass of fissile material at which the chain reaction is self-sustaining (k = 1)", "The mass that makes the highest explosion", "The mass needed for fusion", "The mass at which radiation stops"], 0,
        "Nuclear plants provide baseload power for electrically operated bridge lifts and locks.",
        "নিউক্লিয়ার ফিশন শৃঙ্খল বিক্রিয়ায় 'ক্রান্তিক ভর' কী?", ["সর্বনিম্ন ভর যেখানে শৃঙ্খল বিক্রিয়া স্বনির্বাহী (k = 1)", "সর্বোচ্চ বিস্ফোরণের ভর", "ফিউশনের প্রয়োজনীয় ভর", "যে ভরে বিকিরণ থামে"],
        "পারমাণবিক কেন্দ্র বৈদ্যুতিকভাবে পরিচালিত সেতু লিফট ও লকে বেসলোড বিদ্যুৎ দেয়।"),
    mcq("Zener diode is used as a voltage regulator because:", ["It maintains constant voltage across it within its reverse breakdown region", "It amplifies current", "It generates AC", "It stores charge"], 0,
        "Zener diodes protect bridge sensor electronics from voltage spikes.",
        "জেনার ডায়োড ভোল্টেজ নিয়ন্ত্রক হিসেবে ব্যবহার:", ["বিপরীত ভাঙন অঞ্চলে এর জুড়ে ধ্রুবক ভোল্টেজ বজায় রাখে", "প্রবাহ বিবর্ধন করে", "AC তৈরি করে", "চার্জ সঞ্চয় করে"],
        "জেনার ডায়োড সেতু সেন্সর ইলেকট্রনিক্সকে ভোল্টেজ স্পাইক থেকে রক্ষা করে।"),
    mcq("An n-p-n transistor in common-emitter configuration: current gain β = I_C/I_B. If β = 100 and I_B = 20 μA then I_C is:", ["2 mA", "200 μA", "0.2 mA", "20 mA"], 0,
        "β = I_C/I_B = 100. I_C = 100 × 20 μA = 2000 μA = 2 mA.",
        "সাধারণ-নিঃসারক n-p-n ট্রানজিস্টর: প্রবাহ লাভ β = I_C/I_B। β = 100, I_B = 20 μA হলে I_C:", ["2 mA", "200 μA", "0.2 mA", "20 mA"],
        "β = I_C/I_B = 100। I_C = 100 × 20 μA = 2000 μA = 2 mA।"),
    mcq("What is the function of the depletion layer in a p-n junction?", ["It creates a built-in electric field that opposes further diffusion of majority carriers", "It allows current in both directions equally", "It stores charge permanently", "It has maximum conductivity"], 0,
        "Reverse biasing widens the depletion layer — used in bridge displacement sensors (varactor diodes).",
        "p-n সংযোগে অবক্ষয় স্তরের কাজ:", ["অন্তর্নির্মিত তড়িৎক্ষেত্র তৈরি যা সংখ্যাগরিষ্ঠ বাহকের আরও বিস্তার রোধ করে", "উভয় দিকে সমান প্রবাহ", "স্থায়ীভাবে চার্জ সঞ্চয়", "সর্বোচ্চ পরিবাহিতা"],
        "বিপরীত পক্ষপাত অবক্ষয় স্তর প্রশস্ত করে — সেতু সরণ সেন্সরে (ভ্যারেক্টর ডায়োড) ব্যবহার।"),
    mcq("The electric potential at a distance r from a point charge Q is:", ["V = kQ/r (where k = 9×10⁹ N·m²/C²)", "V = kQ/r²", "V = kQ²/r", "V = k/Qr"], 0,
        "Unlike field E = kQ/r², potential V = kQ/r drops more slowly with distance.",
        "বিন্দু আধান Q থেকে r দূরত্বে তড়িৎ বিভব:", ["V = kQ/r (k = 9×10⁹ N·m²/C²)", "V = kQ/r²", "V = kQ²/r", "V = k/Qr"],
        "ক্ষেত্র E = kQ/r² এর বিপরীতে, বিভব V = kQ/r দূরত্বের সাথে ধীরে কমে।"),
    mcq("A capacitor of capacitance C is charged to voltage V. Energy stored is:", ["½CV²", "CV²", "CV", "C²V"], 0,
        "E = ½CV² = ½QV = Q²/2C. Bridge expansion joint sensors use capacitive measurements.",
        "C ধারকত্বের একটি ধারিত্রক V ভোল্টেজে চার্জ। সঞ্চিত শক্তি:", ["½CV²", "CV²", "CV", "C²V"],
        "E = ½CV² = ½QV = Q²/2C। সেতু প্রসারণ সংযোগ সেন্সর ধারকীয় পরিমাপ ব্যবহার করে।"),
    mcq("Kirchhoff's Current Law (KCL) states that at any junction:", ["The sum of currents entering equals the sum leaving (charge conservation)", "Voltage is equal at all junctions", "Current divides by resistance at each branch", "Current is maximum at junctions"], 0,
        "KCL and KVL together solve any resistive network — used in bridge strain-gauge Wheatstone bridge circuits.",
        "কিরশফের প্রবাহ সূত্র (KCL) যেকোনো সংযোগ-বিন্দুতে:", ["প্রবেশকারী প্রবাহের সমষ্টি = বহির্গামী (আধান সংরক্ষণ)", "সব সংযোগে ভোল্টেজ সমান", "প্রবাহ প্রতিটা শাখায় রোধ দ্বারা ভাগ হয়", "সংযোগে প্রবাহ সর্বোচ্চ"],
        "KCL ও KVL একসাথে যেকোনো রোধী নেটওয়ার্ক সমাধান করে — সেতু স্ট্রেন-গজ হুইটস্টোন সার্কিটে ব্যবহার।"),
    mcq("A long straight wire carries current I. The magnetic field at distance r is:", ["B = μ₀I/(2πr), circular field lines around the wire", "B = μ₀I/r", "B = μ₀I/(4πr²)", "B = μ₀I·r"], 0,
        "μ₀ = 4π×10⁻⁷ T·m/A. Induced fields from bridge power cables can interfere with compasses.",
        "লম্বা সোজা তার প্রবাহ I বহন করে। r দূরত্বে চৌম্বক ক্ষেত্র:", ["B = μ₀I/(2πr), তারের চারপাশে বৃত্তাকার ক্ষেত্র রেখা", "B = μ₀I/r", "B = μ₀I/(4πr²)", "B = μ₀I·r"],
        "μ₀ = 4π×10⁻⁷ T·m/A। সেতু বিদ্যুৎ তার থেকে প্ররোচিত ক্ষেত্র কম্পাসে ব্যতিচার করতে পারে।"),
    mcq("Lenz's law states that the induced EMF always opposes the cause that produces it. This is a statement of:", ["Conservation of energy", "Conservation of charge", "Newton's third law", "Gauss's law"], 0,
        "If it aided the cause, energy would be created from nothing — violating conservation.",
        "লেঞ্জের সূত্র: প্ররোচিত EMF সবসময় কারণকে বিরোধ করে। এটা কোন সংরক্ষণ সূত্রের বিবৃতি:", ["শক্তি সংরক্ষণ", "আধান সংরক্ষণ", "নিউটনের তৃতীয় সূত্র", "গাউসের সূত্র"],
        "যদি কারণকে সহায়তা করত, শূন্য থেকে শক্তি তৈরি হত — সংরক্ষণ লঙ্ঘন করত।"),
    mcq("Self-inductance L of a coil is defined by the relation:", ["EMF = -L dI/dt (opposition to change in current)", "EMF = L × I", "EMF = I/L", "EMF = L × I²"], 0,
        "Inductors in bridge power-factor correction circuits store energy as magnetic fields.",
        "কুণ্ডলীর স্ব-আবেশাঙ্ক L সংজ্ঞায়িত:", ["EMF = -L dI/dt (প্রবাহ পরিবর্তনে বাধা)", "EMF = L × I", "EMF = I/L", "EMF = L × I²"],
        "সেতু পাওয়ার-ফ্যাক্টর সংশোধন সার্কিটে আবেশক চৌম্বক ক্ষেত্রে শক্তি সঞ্চয় করে।"),
    mcq("In an LC circuit with no resistance, energy oscillates between electric (½CV²) and magnetic (½LI²) forms. The resonant frequency is:", ["f = 1/(2π√(LC))", "f = 2π√(LC)", "f = √(LC)/2π", "f = 1/√(LC)"], 0,
        "LC tank circuits in bridge toll-plaza RFID readers operate at precise resonant frequencies.",
        "রোধহীন LC সার্কিটে শক্তি তড়িৎ (½CV²) ও চৌম্বক (½LI²) রূপে দোদুল্যমান। অনুরণন কম্পাঙ্ক:", ["f = 1/(2π√(LC))", "f = 2π√(LC)", "f = √(LC)/2π", "f = 1/√(LC)"],
        "সেতু টোল-প্লাজা RFID রিডারে LC ট্যাংক সার্কিট সুনির্দিষ্ট অনুরণন কম্পাঙ্কে কাজ করে।"),
    mcq("The RMS value of an AC voltage V₀ sin(ωt) is:", ["V_rms = V₀/√2 ≈ 0.707 V₀", "V_rms = V₀", "V_rms = V₀/2", "V_rms = V₀√2"], 0,
        "Mains supply: 230 V_rms means V₀ ≈ 325 V peak. Bridge lighting systems are designed for 230 V rms.",
        "AC ভোল্টেজ V₀ sin(ωt)-এর RMS মান:", ["V_rms = V₀/√2 ≈ 0.707 V₀", "V_rms = V₀", "V_rms = V₀/2", "V_rms = V₀√2"],
        "মেইন সরবরাহ: 230 V_rms মানে V₀ ≈ 325 V শীর্ষ। সেতু আলোক ব্যবস্থা 230 V rms-এর জন্য ডিজাইন।"),
    mcq("In a transformer, the voltage ratio equals the turns ratio: V_s/V_p = N_s/N_p. Energy conservation means:", ["V_p I_p = V_s I_s (ideal transformer: no energy loss)", "V_p I_p > V_s I_s", "Current ratio equals turns ratio", "Power increases through a transformer"], 0,
        "Step-up transformer raises voltage for long-distance transmission — used to power bridge construction sites.",
        "ট্রান্সফর্মারে ভোল্টেজ অনুপাত = পাক অনুপাত: V_s/V_p = N_s/N_p। শক্তি সংরক্ষণ:", ["V_p I_p = V_s I_s (আদর্শ ট্রান্সফর্মার: শক্তিক্ষতি নেই)", "V_p I_p > V_s I_s", "প্রবাহ অনুপাত = পাক অনুপাত", "ট্রান্সফর্মারে ক্ষমতা বাড়ে"],
        "স্টেপ-আপ ট্রান্সফর্মার দীর্ঘ-দূরত্ব সঞ্চালনে ভোল্টেজ বাড়ায় — সেতু নির্মাণ সাইট বিদ্যুৎ দিতে ব্যবহার।"),
    mcq("The Bohr model of hydrogen gives energy levels Eₙ = -13.6/n² eV. The ionisation energy of hydrogen (removing the electron from n=1) is:", ["13.6 eV", "1.51 eV", "3.4 eV", "0 eV"], 0,
        "E_ionise = E_∞ - E₁ = 0 - (-13.6) = 13.6 eV. UV photons ionise hydrogen in the upper atmosphere.",
        "হাইড্রোজেনের বোর মডেল শক্তি স্তর Eₙ = -13.6/n² eV। হাইড্রোজেনের আয়নীকরণ শক্তি (n=1 থেকে ইলেকট্রন সরানো):", ["13.6 eV", "1.51 eV", "3.4 eV", "0 eV"],
        "E_আয়ন = 0 - (-13.6) = 13.6 eV। UV ফোটন উপরের বায়ুমণ্ডলে হাইড্রোজেন আয়নিত করে।"),
    mcq("Radioactive decay law: N(t) = N₀ e^(-λt). The half-life T₁/₂ is related to the decay constant λ by:", ["T₁/₂ = ln 2 / λ ≈ 0.693/λ", "T₁/₂ = λ/ln 2", "T₁/₂ = 1/λ", "T₁/₂ = λ²"], 0,
        "Carbon-14 (T₁/₂ = 5730 yr) dates ancient wood — used to verify ages of timber found in bridge foundations.",
        "তেজস্ক্রিয় ক্ষয় সূত্র: N(t) = N₀ e^(-λt)। অর্ধজীবন T₁/₂ ক্ষয় ধ্রুবক λ-এর সাথে:", ["T₁/₂ = ln 2 / λ ≈ 0.693/λ", "T₁/₂ = λ/ln 2", "T₁/₂ = 1/λ", "T₁/₂ = λ²"],
        "কার্বন-14 (T₁/₂ = 5730 বছর) প্রাচীন কাঠ তারিখ দেয় — সেতু ভিত্তিতে পাওয়া কাঠের বয়স যাচাইয়ে ব্যবহার।"),
    mcq("Dimensional analysis can be used to:", ["Derive relationships between physical quantities and check equation homogeneity, but not to find dimensionless constants", "Solve all physics problems", "Replace experiments", "Find numerical values of constants"], 0,
        "Checking dimensions before submitting a bridge load-calculation is standard engineering practice.",
        "মাত্রা বিশ্লেষণ ব্যবহার করা যায়:", ["ভৌত রাশির সম্পর্ক বের করতে ও সমীকরণ সমঘাতীয়তা পরীক্ষায়, কিন্তু মাত্রাহীন ধ্রুবক পেতে নয়", "সব পদার্থবিজ্ঞান সমস্যা সমাধানে", "পরীক্ষা-নিরীক্ষার বিকল্পে", "ধ্রুবকের সংখ্যাগত মান পেতে"],
        "সেতু লোড-গণনা জমার আগে মাত্রা পরীক্ষা প্রমিত প্রকৌশল অনুশীলন।"),
    mcq("The escape velocity from Earth's surface is about 11.2 km/s. At double the radius from Earth's centre, escape velocity is:", ["√2 times smaller ≈ 7.9 km/s (v_escape ∝ 1/√r)", "The same", "Twice as large", "Zero"], 0,
        "v_e = √(2GM/r): doubling r → v_e = √(2GM/2r) = v_e_surface/√2.",
        "পৃথিবীর পৃষ্ঠ থেকে মুক্তি বেগ ~11.2 km/s। কেন্দ্র থেকে দ্বিগুণ ব্যাসার্ধে মুক্তি বেগ:", ["√2 গুণ কম ≈ 7.9 km/s (v_মুক্তি ∝ 1/√r)", "একই", "দ্বিগুণ", "শূন্য"],
        "v_e = √(2GM/r): r দ্বিগুণ → v_e = v_পৃষ্ঠ/√2।"),
    mcq("The pressure inside a soap bubble of radius r and surface tension T is:", ["P = P₀ + 4T/r (two surfaces contribute)", "P = P₀ + 2T/r (one surface)", "P = P₀ - 4T/r", "P = 4T/r only"], 0,
        "Concrete air entrainment creates billions of micro-bubbles (two-surface spheres) that absorb freeze-thaw stress.",
        "r ব্যাসার্ধ ও T পৃষ্ঠটান সহ সাবান-বুদবুদের ভেতরের চাপ:", ["P = P₀ + 4T/r (দুটো তল অবদান)", "P = P₀ + 2T/r (একটা তল)", "P = P₀ - 4T/r", "P = 4T/r শুধু"],
        "কংক্রিট বায়ু-অন্তর্ভূক্তি কোটি কোটি মাইক্রো-বুদবুদ (দুই-তলীয় গোলক) তৈরি করে হিমায়ন-গলন চাপ শুষে নেয়।"),
    mcq("If the length of a simple pendulum is increased by 21%, the period changes by approximately:", ["+10% (T ∝ √L; √1.21 = 1.10)", "+21%", "+4.5%", "-10%"], 0,
        "T = 2π√(L/g). Bridge cable stayed sag alters natural sway period similarly.",
        "সরল দোলকের দৈর্ঘ্য 21% বাড়লে পর্যায়কাল পরিবর্তন:", ["+10% (T ∝ √L; √1.21 = 1.10)", "+21%", "+4.5%", "-10%"],
        "T = 2π√(L/g)। সেতুর ক্যাবল স্টেড ঝুলে পড়া একইভাবে স্বাভাবিক দুলন পর্যায়কাল পরিবর্তন করে।"),
    mcq("A body in simple harmonic motion has maximum velocity when displacement is zero, and zero velocity when:", ["Displacement is at maximum (amplitude A) — all energy is potential there", "Displacement is at equilibrium", "Time equals period", "Frequency is maximum"], 0,
        "At max displacement: KE = 0, PE = ½kA². Bridge deck oscillation stores energy as bending PE at extremes.",
        "SHM-এ সরণ শূন্যে বেগ সর্বোচ্চ, আর বেগ শূন্য হয় যখন:", ["সরণ সর্বোচ্চে (বিস্তার A) — সেখানে সব শক্তি স্থিতিশক্তি", "সরণ ভারসাম্যে", "সময় পর্যায়ের সমান", "কম্পাঙ্ক সর্বোচ্চ"],
        "সর্বোচ্চ সরণে: KE = 0, PE = ½kA²। সেতু পাটাতন দোলায় চরমে বাঁকানো PE হিসেবে শক্তি সঞ্চয়।"),
    mcq("Beats are produced when two waves of slightly different frequencies f₁ and f₂ superpose. The beat frequency is:", ["|f₁ - f₂| (absolute difference)", "f₁ + f₂", "(f₁ + f₂)/2", "f₁ × f₂"], 0,
        "Beat frequency is used to tune musical instruments and to detect slight frequency shifts in bridge vibration monitoring.",
        "সামান্য ভিন্ন কম্পাঙ্কের দুটো তরঙ্গের উপরিপাতনে বীট উৎপন্ন। বীট কম্পাঙ্ক:", ["|f₁ - f₂| (পরম পার্থক্য)", "f₁ + f₂", "(f₁ + f₂)/2", "f₁ × f₂"],
        "বীট কম্পাঙ্ক বাদ্যযন্ত্র সুর করতে ও সেতু কম্পন পর্যবেক্ষণে সামান্য কম্পাঙ্ক পরিবর্তন শনাক্তে ব্যবহার।"),
    mcq("Total internal reflection occurs only when light travels from a denser to a rarer medium and the angle of incidence exceeds:", ["The critical angle θ_c = arcsin(n₂/n₁)", "The Brewster angle", "45°", "90°"], 0,
        "Optical fibres in bridge sensor networks use total internal reflection to transmit data without loss.",
        "সম্পূর্ণ আভ্যন্তরীণ প্রতিফলন ঘটে যখন আলো ঘন থেকে হালকা মাধ্যমে যায় আর আপাতন কোণ অতিক্রম করে:", ["ক্রান্তিক কোণ θ_c = arcsin(n₂/n₁)", "ব্রুস্টার কোণ", "45°", "90°"],
        "সেতু সেন্সর নেটওয়ার্কে অপটিক্যাল ফাইবার ক্ষতিমুক্ত ডেটা পাঠাতে সম্পূর্ণ আভ্যন্তরীণ প্রতিফলন ব্যবহার করে।"),
    mcq("The magnetic force on a current-carrying conductor in a field B is F = BIL sin θ. The force is maximum when:", ["θ = 90° (conductor perpendicular to B)", "θ = 0°", "θ = 45°", "θ = 180°"], 0,
        "DC electric motors on bridge draw-spans use this force. F = BIL when wire is perpendicular to field.",
        "চৌম্বক ক্ষেত্র B-তে প্রবাহ-বাহী পরিবাহকের বল F = BIL sin θ। বল সর্বোচ্চ যখন:", ["θ = 90° (পরিবাহক B-এর লম্ব)", "θ = 0°", "θ = 45°", "θ = 180°"],
        "সেতু ড্রসপ্যানে DC মোটর এই বল ব্যবহার করে। তার ক্ষেত্রের লম্ব হলে F = BIL।"),
    mcq("Gauss's law for electricity states: ∮E·dA = Q_enc/ε₀. For a spherical conductor with charge Q:", ["The electric field inside the conductor is zero; all charge resides on the surface", "The field is uniform throughout", "Charge distributes throughout the volume", "Field is maximum at the centre"], 0,
        "Bridge earth-grounding systems use conductor shielding — zero field inside metallic enclosures.",
        "তড়িতের গাউসের সূত্র: ∮E·dA = Q_enc/ε₀। আধান Q সহ গোলাকার পরিবাহক:", ["পরিবাহকের ভেতরে তড়িৎ ক্ষেত্র শূন্য; সব আধান পৃষ্ঠে", "সর্বত্র একসমান ক্ষেত্র", "আধান সমগ্র আয়তনে বিতরিত", "কেন্দ্রে ক্ষেত্র সর্বোচ্চ"],
        "সেতু ভূ-সংযোগ ব্যবস্থা পরিবাহক পর্দাবরণ ব্যবহার করে — ধাতব আবরণের ভেতরে শূন্য ক্ষেত্র।"),
    mcq("Two identical bulbs are connected first in series and then in parallel to the same supply. In which case is the total power dissipated more?", ["Parallel — total resistance is halved so power is doubled", "Series — current is same through both", "Equal in both cases", "Series dissipates more since resistance is higher"], 0,
        "P = V²/R_total. In parallel R_total halves, so power doubles. Bridge lighting panels use parallel wiring.",
        "দুটো একই বাল্ব প্রথমে শ্রেণিতে, তারপর সমান্তরালে একই সরবরাহে সংযুক্ত। কোনটায় মোট ক্ষয় বেশি?", ["সমান্তরাল — মোট রোধ অর্ধেক, শক্তি দ্বিগুণ", "শ্রেণি — উভয়ে প্রবাহ একই", "উভয়ে সমান", "শ্রেণিতে বেশি কারণ রোধ বেশি"],
        "P = V²/R_মোট। সমান্তরালে R_মোট অর্ধেক, তাই শক্তি দ্বিগুণ। সেতু আলোর প্যানেল সমান্তরাল তার ব্যবহার করে।"),
    mcq("The Stefan-Boltzmann law states that the total power radiated per unit area is P = σT⁴. If a body's absolute temperature doubles:", ["Power emitted per unit area increases 16 times", "Power doubles", "Power quadruples", "Power increases 8 times"], 0,
        "2⁴ = 16. Hot steel during welding on bridge joints radiates at much higher rate than cooled steel.",
        "স্টেফান-বোলৎজম্যান সূত্র: একক ক্ষেত্রে বিকীর্ণ মোট শক্তি P = σT⁴। বস্তুর পরম তাপমাত্রা দ্বিগুণ হলে:", ["একক ক্ষেত্রে বিকীর্ণ শক্তি 16 গুণ বাড়ে", "শক্তি দ্বিগুণ", "শক্তি চারগুণ", "শক্তি 8 গুণ বাড়ে"],
        "2⁴ = 16। সেতু সংযোগে ঝালাইয়ের সময় গরম ইস্পাত শীতল ইস্পাতের চেয়ে অনেক বেশি হারে বিকিরণ করে।"),
    mcq("Kepler's third law: T² ∝ r³ for orbits around the same body. If a satellite's orbital radius increases by a factor of 4:", ["Period increases by a factor of 8 (4^(3/2) = 8)", "Period doubles", "Period quadruples", "Period stays the same"], 0,
        "T²/r³ = constant. GPS satellites at ~26,600 km radius take ~12 hours per orbit.",
        "কেপলারের তৃতীয় সূত্র: T² ∝ r³। উপগ্রহের কক্ষ-ব্যাসার্ধ 4 গুণ বাড়লে:", ["পর্যায়কাল 8 গুণ বাড়ে (4^(3/2) = 8)", "পর্যায়কাল দ্বিগুণ", "পর্যায়কাল চারগুণ", "পর্যায়কাল একই"],
        "T²/r³ = ধ্রুবক। GPS উপগ্রহ ~26,600 km ব্যাসার্ধে ~12 ঘণ্টায় এক পাক দেয়।"),
    mcq("Which material property ensures that a steel rod regains its original length after the load is removed (provided stress < yield stress)?", ["Elasticity — Hooke's law applies within the elastic limit: σ = Eε", "Plasticity", "Brittleness", "Creep"], 0,
        "E_steel ≈ 200 GPa. Bridge steel is designed to stay in elastic range under service loads.",
        "কোন পদার্থের ধর্ম নিশ্চিত করে যে লোড সরানোর পর ইস্পাত দণ্ড মূল দৈর্ঘ্যে ফেরে (স্থিতিসীমার মধ্যে)?", ["স্থিতিস্থাপকতা — হুকের সূত্র স্থিতিসীমায় প্রযোজ্য: σ = Eε", "সুঘট্যতা", "ভঙ্গুরতা", "ক্রিপ"],
        "E_ইস্পাত ≈ 200 GPa। সেতু ইস্পাত সার্ভিস লোডে স্থিতিস্থাপক পরিসরে থাকতে ডিজাইন।"),
    mcq("Viscosity η of a fluid is the property that resists:", ["Relative motion between adjacent fluid layers (Newton's law: F/A = η × dv/dy)", "Compression", "Heating", "Evaporation"], 0,
        "High-viscosity bitumen (asphalt) on bridge road surfaces resists flow and deformation in summer heat.",
        "তরলের সান্দ্রতা η পার্শ্ববর্তী তরল স্তরের মধ্যে বাধা দেয়:", ["পার্শ্ববর্তী স্তরের মধ্যে আপেক্ষিক গতিকে (নিউটনের সূত্র: F/A = η × dv/dy)", "সংকোচন", "উত্তাপ", "বাষ্পীভবন"],
        "সেতু রাস্তার পৃষ্ঠে উচ্চ-সান্দ্র বিটুমিন (অ্যাসফাল্ট) গ্রীষ্মের তাপে প্রবাহ ও বিরূপণ রোধ করে।"),
    mcq("Polarisation of light is only possible for:", ["Transverse waves (light) — longitudinal waves like sound cannot be polarised", "All waves equally", "Longitudinal waves only", "Radio waves only"], 0,
        "Polarised light microscopy detects stress in transparent bridge bearing pads (photoelasticity).",
        "আলোর মেরুকরণ সম্ভব শুধুমাত্র:", ["তির্যক তরঙ্গে (আলো) — শব্দের মতো অনুদৈর্ঘ্য তরঙ্গ মেরুকৃত হয় না", "সমস্ত তরঙ্গে সমানভাবে", "শুধু অনুদৈর্ঘ্য তরঙ্গ", "শুধু রেডিও তরঙ্গ"],
        "মেরুকৃত আলো অণুবীক্ষণ স্বচ্ছ সেতু বিয়ারিং প্যাডে চাপ শনাক্ত করে (আলোস্থিতিস্থাপকতা)।"),
    mcq("The uncertainty principle (Heisenberg) states: Δx · Δp ≥ ℏ/2. This means:", ["Position and momentum cannot both be measured precisely at the same time", "Momentum can always be measured exactly", "All particles are at rest", "Uncertainty comes from instrument error only"], 0,
        "ℏ = h/(2π). Quantum tunnelling (based on uncertainty) is used in tunnel diode sensors on smart bridges.",
        "অনিশ্চয়তার নীতি (হাইজেনবার্গ): Δx · Δp ≥ ℏ/2। এর অর্থ:", ["অবস্থান ও ভরবেগ একই সাথে সুনির্দিষ্টভাবে পরিমাপ সম্ভব নয়", "ভরবেগ সবসময় সুনির্দিষ্টভাবে পরিমাপযোগ্য", "সব কণা স্থির", "অনিশ্চয়তা শুধু যন্ত্রের ত্রুটি"],
        "ℏ = h/(2π)। কোয়ান্টাম টানেলিং (অনিশ্চয়তার উপর ভিত্তি) স্মার্ট সেতুতে টানেল ডায়োড সেন্সরে ব্যবহার।"),
    mcq("A body of mass m is on a frictionless inclined plane of angle θ. Its acceleration along the plane is:", ["g sin θ (component of gravity along the incline)", "g cos θ", "g tan θ", "g"], 0,
        "Steel girders on sloped bridge ramps experience component forces that must be resolved correctly.",
        "ভর m বস্তু θ কোণের ঘর্ষণহীন ঢালু তলে। ঢাল বরাবর ত্বরণ:", ["g sin θ (অভিকর্ষের ঢাল-বরাবর উপাংশ)", "g cos θ", "g tan θ", "g"],
        "ঢালু সেতু র‍্যাম্পে ইস্পাত গার্ডারে উপাংশ বল সঠিকভাবে বিশ্লেষণ করতে হয়।"),
    mcq("When a spring of spring constant k is cut into two equal halves, the spring constant of each piece is:", ["2k (shorter spring is stiffer)", "k/2", "k", "k²"], 0,
        "Spring constant ∝ 1/natural length (k ∝ 1/L). Bridge bearing pads act as springs: smaller pad → stiffer.",
        "স্প্রিং ধ্রুবক k-এর স্প্রিং দুই সমান অংশে কাটলে প্রতিটার স্প্রিং ধ্রুবক:", ["2k (ছোট স্প্রিং বেশি শক্ত)", "k/2", "k", "k²"],
        "স্প্রিং ধ্রুবক ∝ 1/স্বাভাবিক দৈর্ঘ্য। সেতু বিয়ারিং প্যাড স্প্রিং হিসেবে কাজ করে: ছোট প্যাড → বেশি শক্ত।"),
    mcq("Power dissipated in a resistor R carrying current I is:", ["P = I²R = V²/R = VI (all equivalent)", "P = IR²", "P = I/R", "P = R/V"], 0,
        "I²R heating in bridge grounding cables must be managed to avoid insulation damage.",
        "প্রবাহ I বহনকারী রোধ R-এ ক্ষয় ক্ষমতা:", ["P = I²R = V²/R = VI (সবগুলো সমতুল্য)", "P = IR²", "P = I/R", "P = R/V"],
        "সেতু আর্থিং তারে I²R তাপ নিরোধক ক্ষতি এড়াতে নিয়ন্ত্রণ করতে হয়।"),
    mcq("The angle of deviation δ through a prism is minimum when the ray passes symmetrically. At minimum deviation, Snell's law gives:", ["n = sin[(A + δ_m)/2] / sin(A/2), where A is the apex angle", "n = sin(A)/sin(δ_m)", "n = δ_m/A", "n = A/δ_m"], 0,
        "Prism equation used in spectrometers that measure refractive index of bridge glass elements.",
        "প্রিজমে বিচ্যুতি কোণ δ ন্যূনতম যখন রশ্মি প্রতিসম পথে যায়। ন্যূনতম বিচ্যুতিতে স্নেলের সূত্র:", ["n = sin[(A + δ_m)/2] / sin(A/2), A = শীর্ষ কোণ", "n = sin(A)/sin(δ_m)", "n = δ_m/A", "n = A/δ_m"],
        "সেতু কাচ উপাদানের প্রতিসরণাঙ্ক পরিমাপের স্পেক্ট্রোমিটারে প্রিজম সমীকরণ ব্যবহার।"),
    mcq("The Doppler effect: when a source of sound frequency f moves towards a stationary observer at speed v_s, the observed frequency is:", ["f' = f(v + v_o)/(v - v_s) with both approaching; for source approaching stationary observer: f' = fv/(v-v_s) > f", "f' = f(v - v_s)/v", "f' = f/v_s", "f' = f × v_s"], 0,
        "Bridge traffic speed monitoring uses radar Doppler effect. Sound Doppler helps detect crack vibrations.",
        "ডপলার প্রভাব: কম্পাঙ্ক f উৎস বেগ v_s-এ স্থির পর্যবেক্ষকের দিকে এলে পর্যবেক্ষিত কম্পাঙ্ক:", ["উভয় এগিয়ে আসলে f' = f(v + v_o)/(v - v_s); শুধু উৎস এগিয়ে আসলে: f' = fv/(v-v_s) > f", "f' = f(v - v_s)/v", "f' = f/v_s", "f' = f × v_s"],
        "সেতু ট্র্যাফিক গতি পর্যবেক্ষণে রাডার ডপলার প্রভাব। শব্দ ডপলার ফাটল কম্পন শনাক্তে সাহায্য করে।"),
    mcq("A gyroscope resists changes to its axis of rotation because of:", ["Conservation of angular momentum — a large L requires a large torque to change its direction", "Friction", "Magnetic force", "Gravity"], 0,
        "Bridge alignment lasers and inertial measurement units use gyroscopic sensors.",
        "জাইরোস্কোপ ঘূর্ণন অক্ষের পরিবর্তন রোধ করে কারণ:", ["কৌণিক ভরবেগ সংরক্ষণ — বড় L-এর দিক পরিবর্তনে বড় টর্ক লাগে", "ঘর্ষণ", "চৌম্বক বল", "অভিকর্ষ"],
        "সেতু সারিবদ্ধকরণ লেজার ও জড়তা পরিমাপ ইউনিট জাইরোস্কোপিক সেন্সর ব্যবহার করে।"),
    mcq("Thermal expansion: a rod of length L₀ at temperature T₀ has length L = L₀(1 + αΔT). If α for steel is 12×10⁻⁶/°C, a 100 m bridge span expands by how much for a 50°C rise?", ["6 cm (L₀αΔT = 100 × 12×10⁻⁶ × 50 = 0.06 m)", "12 cm", "3 cm", "0.6 cm"], 0,
        "Expansion joints on bridges accommodate exactly this: up to ~6 cm over 100 m for India's climate range.",
        "তাপ প্রসারণ: তাপমাত্রা বৃদ্ধি 50°C-তে α = 12×10⁻⁶/°C ইস্পাতের 100 m সেতু বিস্তার কতটুকু প্রসারিত?", ["6 cm (L₀αΔT = 100 × 12×10⁻⁶ × 50 = 0.06 m)", "12 cm", "3 cm", "0.6 cm"],
        "সেতুর প্রসারণ সংযোগ ঠিক এটা মেটায়: ভারতের জলবায়ু পরিসরে 100 m-এ ~6 cm পর্যন্ত।"),
    mcq("Two identical positive charges Q are held a distance d apart. The electric potential at the midpoint between them is:", ["2kQ/(d/2) = 4kQ/d (potentials add, don't cancel)", "Zero", "kQ/d", "2kQ/d"], 0,
        "Unlike electric field (zero at midpoint by symmetry), potential adds — a useful distinction in bridge sensor design.",
        "দুটো একই Q ধনাত্মক আধান d দূরত্বে। মাঝবিন্দুতে তড়িৎ বিভব:", ["2kQ/(d/2) = 4kQ/d (বিভব যোগ হয়, বাতিল নয়)", "শূন্য", "kQ/d", "2kQ/d"],
        "তড়িৎ ক্ষেত্রের বিপরীতে (প্রতিসাম্যে মাঝে শূন্য), বিভব যোগ হয় — সেতু সেন্সর ডিজাইনে উপকারী পার্থক্য।"),
    mcq("In photoelectric effect, if frequency is above threshold, the stopping potential V_s (needed to stop all emitted electrons) is related to maximum KE by:", ["eV_s = hf - φ = KE_max (charge × stopping voltage = max KE)", "eV_s = hf + φ", "eV_s = φ/hf", "eV_s = hf²"], 0,
        "Millikan's oil-drop and photoelectric experiments confirmed fundamental charge e = 1.6×10⁻¹⁹ C.",
        "আলোতড়িৎ প্রভাবে কম্পাঙ্ক ক্রান্তির উপরে থাকলে থামানো বিভব V_s (সব ইলেকট্রন থামাতে) সর্বোচ্চ KE-এর সাথে:", ["eV_s = hf - φ = KE_সর্বোচ্চ (আধান × থামানো ভোল্টেজ = সর্বোচ্চ KE)", "eV_s = hf + φ", "eV_s = φ/hf", "eV_s = hf²"],
        "মিলিকানের তেলের ফোঁটা ও আলোতড়িৎ পরীক্ষা মৌলিক আধান e = 1.6×10⁻¹⁹ C নিশ্চিত করে।"),
    mcq("Which process converts AC to DC in a power supply?", ["Rectification using diodes (half-wave or full-wave bridge rectifier)", "Amplification", "Modulation", "Induction"], 0,
        "Bridge rectifier circuits (four diodes) convert AC mains to smooth DC for bridge monitoring electronics.",
        "পাওয়ার সাপ্লাইতে AC থেকে DC রূপান্তর:", ["ডায়োড দিয়ে রেকটিফিকেশন (হাফ-ওয়েভ বা ফুল-ওয়েভ ব্রিজ রেকটিফায়ার)", "বিবর্ধন", "মড্যুলেশন", "আবেশন"],
        "ব্রিজ রেকটিফায়ার সার্কিট (চার ডায়োড) সেতু পর্যবেক্ষণ ইলেকট্রনিক্সের জন্য AC মেইন থেকে মসৃণ DC রূপান্তর করে।"),
    mcq("What does the area under a force-displacement graph represent?", ["Work done by the force", "Power", "Impulse", "Acceleration"], 0,
        "Load-deflection curves for bridge bearings are used to calculate elastic strain energy stored.",
        "বল-সরণ লেখচিত্রের নিচের ক্ষেত্রফল:", ["বলের কৃতকাজ", "ক্ষমতা", "ঘাত-বল", "ত্বরণ"],
        "সেতু বিয়ারিংয়ের লোড-বিচ্যুতি বক্ররেখা সঞ্চিত স্থিতিস্থাপক বিকৃতি শক্তি হিসাব করতে ব্যবহার।"),
    mcq("A uniform rod of mass M and length L is pivoted at one end. Its moment of inertia about the pivot is:", ["ML²/3", "ML²/12", "ML²/2", "ML²"], 0,
        "I = ML²/3 (end pivot) vs ML²/12 (centre). Drawbridge arm — calculating raising torque uses this.",
        "ভর M, দৈর্ঘ্য L সুষম দণ্ড এক প্রান্তে কীলক-সংযুক্ত। কীলক সম্পর্কে জড়তার ভ্রামক:", ["ML²/3", "ML²/12", "ML²/2", "ML²"],
        "I = ML²/3 (প্রান্ত কীলক) বনাম ML²/12 (কেন্দ্র)। ড্রব্রিজ বাহু উত্তোলন টর্ক গণনায় এটা ব্যবহার।"),
    mcq("The terminal velocity of a sphere falling through a viscous fluid is reached when:", ["Drag force + buoyancy = weight (no net force → constant velocity)", "Gravity becomes zero", "Density of sphere equals fluid", "Drag force exceeds weight"], 0,
        "Pile driving through soft soil uses terminal velocity concept — pile velocity stabilises when resistance equals driving force.",
        "সান্দ্র তরলে পড়ন্ত গোলকের প্রান্তিক বেগ পৌঁছায় যখন:", ["টান বল + উচ্ছ্বাস = ওজন (কোনো নেট বল নেই → স্থির বেগ)", "অভিকর্ষ শূন্য", "গোলকের ঘনত্ব = তরল", "টান বল ওজন ছাড়িয়ে যায়"],
        "নরম মাটিতে পাইল চালানোয় প্রান্তিক বেগ ধারণা ব্যবহার — প্রতিরোধ = চালক বলে পাইলের বেগ স্থিতিশীল।"),
    mcq("Young's experiment: the fringe width β = λD/d. If the slit separation d is halved, fringes become:", ["Twice as wide (β ∝ 1/d)", "Half as wide", "Same width", "Disappear"], 0,
        "Optical strain sensors on bridge steel use interference patterns that shift with nano-scale deformation.",
        "ইয়ং-এর পরীক্ষায় ডোরার প্রস্থ β = λD/d। চির-ব্যবধান d অর্ধেক হলে ডোরা:", ["দ্বিগুণ চওড়া (β ∝ 1/d)", "অর্ধেক চওড়া", "একই প্রস্থ", "অদৃশ্য"],
        "সেতু ইস্পাতে অপটিক্যাল স্ট্রেন সেন্সর ব্যতিচার প্যাটার্ন ব্যবহার করে ন্যানো-স্কেল বিরূপণ পরিমাপ।"),
    mcq("A satellite is at height h above Earth's surface. If R is Earth's radius, its orbital speed is:", ["v = √[GM/(R+h)] (lower orbit → faster speed)", "v = √[GMh/R]", "v = √[GM/R]", "v = √[GM·h]"], 0,
        "Low Earth orbit (~400 km) satellites used for bridge inspection imagery travel at ~7.7 km/s.",
        "পৃথিবীর পৃষ্ঠ থেকে h উচ্চতায় উপগ্রহ। R = পৃথিবীর ব্যাসার্ধ, কক্ষীয় বেগ:", ["v = √[GM/(R+h)] (নিচের কক্ষ → বেশি বেগ)", "v = √[GMh/R]", "v = √[GM/R]", "v = √[GM·h]"],
        "নিম্ন পৃথিবী কক্ষপথে (~400 km) সেতু পরিদর্শন চিত্রের উপগ্রহ ~7.7 km/s বেগে চলে।"),
    mcq("For a concave mirror, if an object is at the centre of curvature (u = 2f), the image forms at:", ["Also at 2f — same size, real, inverted (m = -1)", "At infinity", "At the focus f", "Behind the mirror"], 0,
        "Used in alignment tools on bridge construction sites — matching image to object checks measurement accuracy.",
        "অবতল দর্পণে বস্তু বক্রতার কেন্দ্রে (u = 2f)। প্রতিবিম্ব:", ["2f-এও — সমান আকার, বাস্তব, উল্টো (m = -1)", "অসীমে", "ফোকাস f-এ", "দর্পণের পেছনে"],
        "সেতু নির্মাণ সাইটে সারিবদ্ধকরণ সরঞ্জামে ব্যবহার — প্রতিবিম্ব বস্তুর সাথে মেলালে পরিমাপের নির্ভুলতা পরীক্ষা।"),
    mcq("The electric field between two parallel plates (area A, separation d, charge Q) is approximately:", ["E = Q/(ε₀A) = σ/ε₀ (uniform, from positive to negative plate)", "E = Q/(ε₀d)", "E = Q·d/ε₀", "E = ε₀Q/A"], 0,
        "Capacitive displacement sensors on bridge expansion joints use this uniform field principle.",
        "দুটো সমান্তরাল পাত (ক্ষেত্রফল A, ব্যবধান d, আধান Q) মধ্যে তড়িৎ ক্ষেত্র:", ["E = Q/(ε₀A) = σ/ε₀ (সুষম, ধনাত্মক থেকে ঋণাত্মক পাতে)", "E = Q/(ε₀d)", "E = Q·d/ε₀", "E = ε₀Q/A"],
        "সেতু প্রসারণ সংযোগে ধারকীয় সরণ সেন্সর এই সুষম ক্ষেত্র নীতি ব্যবহার করে।"),
    mcq("An α-particle (mass 4u, charge +2e) and a β-particle (mass ≈ 0, charge -e) are produced in nuclear decay. Which is deflected more in a magnetic field?", ["β-particle (much larger charge-to-mass ratio)", "α-particle (heavier)", "Both deflect equally", "Neither deflects"], 0,
        "Magnetic spectroscopy of charged particles — used to identify decay products in nuclear physics.",
        "α-কণা (ভর 4u, আধান +2e) ও β-কণা (ভর ≈ 0, আধান -e) নিউক্লিয়ার ক্ষয়ে উৎপন্ন। চৌম্বক ক্ষেত্রে কোনটা বেশি বিক্ষিপ্ত?", ["β-কণা (অনেক বেশি আধান-থেকে-ভর অনুপাত)", "α-কণা (ভারী)", "উভয় সমান", "কোনোটাই নয়"],
        "আধানযুক্ত কণার চৌম্বক বর্ণালীবিক্ষণ — নিউক্লিয়ার পদার্থবিজ্ঞানে ক্ষয় পণ্য সনাক্তে ব্যবহার।"),
    mcq("The phenomenon of diffraction is most noticeable when the wavelength of the wave is:", ["Comparable to or larger than the size of the obstacle or opening", "Much smaller than the obstacle", "Equal to the amplitude", "Much larger than the medium"], 0,
        "Sound (λ ≈ 1 m) diffracts around bridge pillars; light (λ ≈ 500 nm) barely diffracts around them.",
        "অপবর্তনের ঘটনা সবচেয়ে লক্ষণীয় যখন তরঙ্গদৈর্ঘ্য:", ["বাধা বা ছিদ্রের আকারের সমতুল্য বা বড়", "বাধার চেয়ে অনেক ছোট", "বিস্তারের সমান", "মাধ্যমের চেয়ে অনেক বড়"],
        "শব্দ (λ ≈ 1 m) সেতু স্তম্ভের চারপাশে অপবর্তিত হয়; আলো (λ ≈ 500 nm) খুব কমই হয়।"),
    mcq("The Hall effect: a conductor carrying current I in a magnetic field B perpendicular to current develops:", ["A transverse voltage V_H = IBd/(nqt) across its width — used to measure B or carrier density n", "An increase in resistance", "A decrease in current", "Extra heating only"], 0,
        "Hall-effect sensors measure bridge cable tension without cutting the cable (non-destructive testing).",
        "হল প্রভাব: প্রবাহ I বহনকারী পরিবাহকে লম্ব চৌম্বক ক্ষেত্র B তৈরি করে:", ["প্রস্থ জুড়ে আড়াআড়ি ভোল্টেজ V_H = IBd/(nqt) — B বা বাহক ঘনত্ব n পরিমাপে ব্যবহার", "রোধ বাড়ে", "প্রবাহ কমে", "শুধু অতিরিক্ত তাপ"],
        "হল-প্রভাব সেন্সর তার না কেটে সেতু তারের টান পরিমাপ করে (অ-ধ্বংসাত্মক পরীক্ষা)।"),
    mcq("The work done by a gas in an isothermal expansion from volume V₁ to V₂ is:", ["W = nRT ln(V₂/V₁) (ideal gas)", "W = nR(V₂-V₁)", "W = P(V₂-V₁) with constant P", "W = nRT(V₂-V₁)"], 0,
        "Pneumatic bridge jacks use gas expansion for lifting heavy spans during maintenance.",
        "আদর্শ গ্যাসের সমতাপীয় প্রসারণে আয়তন V₁ থেকে V₂ তে কৃতকাজ:", ["W = nRT ln(V₂/V₁) (আদর্শ গ্যাস)", "W = nR(V₂-V₁)", "ধ্রুবক P-তে W = P(V₂-V₁)", "W = nRT(V₂-V₁)"],
        "নিউমেটিক সেতু জ্যাক রক্ষণাবেক্ষণের সময় ভারী বিস্তার উত্তোলনে গ্যাস প্রসারণ ব্যবহার করে।"),
    mcq("When a battery of EMF ε and internal resistance r supplies current I to an external resistance R, the terminal voltage is:", ["V = ε - Ir (terminal voltage drops below EMF due to internal resistance)", "V = ε + Ir", "V = εR/(R+r)", "V = ε/R"], 0,
        "Bridge monitoring systems use battery backups: under load, terminal voltage drops, affecting sensor accuracy.",
        "EMF ε ও অভ্যন্তরীণ রোধ r-এর ব্যাটারি প্রবাহ I সরবরাহ করে। পটি ভোল্টেজ:", ["V = ε - Ir (অভ্যন্তরীণ রোধের কারণে EMF-এর নিচে পড়ে)", "V = ε + Ir", "V = εR/(R+r)", "V = ε/R"],
        "সেতু পর্যবেক্ষণ ব্যবস্থা ব্যাটারি ব্যাকআপ ব্যবহার করে: লোডের সময় পটি ভোল্টেজ কমে, সেন্সর নির্ভুলতায় প্রভাব।"),
    mcq("For a convex lens forming a real image, if object distance u = -2f, the image distance v is:", ["v = +2f (by lens formula 1/v - 1/u = 1/f → 1/v = 1/f - 1/2f = 1/2f)", "v = -f", "v = +f", "v = ∞"], 0,
        "1/v - 1/(-2f) = 1/f → 1/v = 1/f - 1/2f = 1/2f → v = 2f (real, same size).",
        "উত্তল লেন্সে বাস্তব প্রতিবিম্বে u = -2f হলে প্রতিবিম্ব দূরত্ব v:", ["v = +2f (লেন্স সূত্রে 1/v - 1/u = 1/f → v = 2f)", "v = -f", "v = +f", "v = ∞"],
        "1/v + 1/2f = 1/f → v = 2f (বাস্তব, একই আকার)।"),
    mcq("Energy stored per unit volume in an electric field E is:", ["u = ½ε₀E² (electrostatic energy density)", "u = ε₀E", "u = ε₀E²", "u = E²/ε₀"], 0,
        "Parallel to magnetic energy density u = B²/2μ₀. Both matter for bridge sensor power budgets.",
        "তড়িৎ ক্ষেত্র E-তে প্রতি একক আয়তনে সঞ্চিত শক্তি:", ["u = ½ε₀E² (তড়িৎস্থিত শক্তি ঘনত্ব)", "u = ε₀E", "u = ε₀E²", "u = E²/ε₀"],
        "চৌম্বক শক্তি ঘনত্ব u = B²/2μ₀-এর সমান্তরাল। উভয়ই সেতু সেন্সর বিদ্যুৎ বাজেটে গুরুত্বপূর্ণ।"),
    mcq("Compton scattering occurs when an X-ray photon collides with a nearly-free electron. The scattered photon has:", ["Longer wavelength (less energy) — energy is transferred to the electron: Δλ = (h/m_ec)(1 - cos θ)", "Shorter wavelength", "Same wavelength", "Zero wavelength"], 0,
        "X-ray inspection of bridge welds relies on Compton scattering and photoelectric absorption for contrast.",
        "কম্পটন বিচ্ছুরণে X-রশ্মি ফোটন প্রায়-মুক্ত ইলেকট্রনে ধাক্কা লাগে। বিচ্ছুরিত ফোটনের:", ["দীর্ঘতর তরঙ্গদৈর্ঘ্য (কম শক্তি) — শক্তি ইলেকট্রনে স্থানান্তরিত: Δλ = (h/m_ec)(1 - cos θ)", "ছোটতর তরঙ্গদৈর্ঘ্য", "একই তরঙ্গদৈর্ঘ্য", "শূন্য তরঙ্গদৈর্ঘ্য"],
        "সেতু ঝালাই X-রশ্মি পরিদর্শনে কম্পটন বিচ্ছুরণ ও আলোতড়িৎ শোষণ কনট্রাস্টের জন্য।"),
    mcq("A current-carrying circular loop in a uniform magnetic field experiences:", ["A torque (τ = NIAB sin θ), but no net translational force if B is uniform", "A net translational force", "Zero torque always", "A force toward the field source"], 0,
        "NIAB sin θ = τ. Motors powering bridge moveable spans use this torque.",
        "সুষম চৌম্বক ক্ষেত্রে প্রবাহ-বাহী বৃত্তাকার বলয়:", ["টর্ক অনুভব করে (τ = NIAB sin θ), কিন্তু B সুষম হলে নেট বলানুবর্তী বল নেই", "নেট বলানুবর্তী বল", "সবসময় শূন্য টর্ক", "ক্ষেত্র উৎসের দিকে বল"],
        "NIAB sin θ = τ। সেতু চলন্ত বিস্তার পরিচালনাকারী মোটর এই টর্ক ব্যবহার করে।"),
    mcq("The work function of a metal is 2 eV. What is the minimum frequency of light needed to eject electrons?", ["f₀ = φ/h = (2 × 1.6×10⁻¹⁹)/(6.63×10⁻³⁴) ≈ 4.8×10¹⁴ Hz (near visible)", "2×10¹⁴ Hz", "10¹⁵ Hz", "10¹² Hz"], 0,
        "f₀ = eφ_eV / h ≈ (2 × 1.6×10⁻¹⁹)/(6.63×10⁻³⁴) ≈ 4.8×10¹⁴ Hz — near visible light.",
        "ধাতুর কাজ-অপেক্ষা 2 eV। ইলেকট্রন বের করতে আলোর ন্যূনতম কম্পাঙ্ক:", ["f₀ = φ/h = (2 × 1.6×10⁻¹⁹)/(6.63×10⁻³⁴) ≈ 4.8×10¹⁴ Hz (দৃশ্যমানের কাছে)", "2×10¹⁴ Hz", "10¹⁵ Hz", "10¹² Hz"],
        "f₀ = eφ_eV / h ≈ 4.8×10¹⁴ Hz — দৃশ্যমান আলোর কাছাকাছি।"),
    mcq("If a rigid body is in static equilibrium, the conditions are:", ["(1) ΣF = 0 (zero net force) AND (2) Στ = 0 (zero net torque about any point)", "Only ΣF = 0", "Only Στ = 0", "Net kinetic energy = 0"], 0,
        "Both conditions must hold for bridge structures: no resultant force and no tendency to rotate.",
        "দৃঢ় বস্তু স্থির সাম্যে থাকলে শর্ত:", ["(1) ΣF = 0 (নেট বল শূন্য) এবং (2) Στ = 0 (যেকোনো বিন্দু সম্পর্কে নেট টর্ক শূন্য)", "শুধু ΣF = 0", "শুধু Στ = 0", "নেট গতিশক্তি = 0"],
        "সেতু কাঠামোতে উভয় শর্ত পূরণ করতে হবে: কোনো লব্ধি বল নেই, ঘোরার প্রবণতা নেই।"),
    mcq("The Bohr radius (most probable distance of electron from nucleus in H ground state) is:", ["a₀ ≈ 0.53 Å = 0.053 nm (calculated from quantum mechanics)", "0.1 nm", "1 Å exactly", "0.01 nm"], 0,
        "a₀ = 4πε₀ℏ²/(m_e e²) ≈ 0.529 Å. Used as a scale for atomic dimensions in material science.",
        "বোর ব্যাসার্ধ (H ভূমি-অবস্থায় নিউক্লিয়াস থেকে ইলেকট্রনের সর্বাধিক সম্ভাব্য দূরত্ব):", ["a₀ ≈ 0.53 Å = 0.053 nm (কোয়ান্টাম বলবিদ্যা থেকে গণনা)", "0.1 nm", "ঠিক 1 Å", "0.01 nm"],
        "a₀ = 4πε₀ℏ²/(m_e e²) ≈ 0.529 Å। বস্তু বিজ্ঞানে পারমাণবিক মাত্রার স্কেল হিসেবে ব্যবহার।"),
    mcq("A mass-spring system oscillates. If the spring is replaced by one twice as stiff (k → 2k), the period:", ["Decreases by factor √2 (T = 2π√(m/k) ∝ 1/√k)", "Doubles", "Halves", "Stays the same"], 0,
        "Stiffer springs (bearings) on a bridge deck lower its natural frequency and change resonance behaviour.",
        "ভর-স্প্রিং ব্যবস্থা দোলছে। স্প্রিং দ্বিগুণ শক্ত (k → 2k) হলে পর্যায়কাল:", ["√2 গুণ কমে (T = 2π√(m/k) ∝ 1/√k)", "দ্বিগুণ", "অর্ধেক", "একই থাকে"],
        "শক্তিশালী স্প্রিং (বিয়ারিং) সেতু পাটাতনের স্বাভাবিক কম্পাঙ্ক কমায় ও অনুরণন আচরণ পরিবর্তন করে।"),
    mcq("In forced oscillations, the amplitude at resonance is limited (not infinite) due to:", ["Damping — friction or resistance dissipates energy", "Gravity", "Amplitude can be infinite ideally", "Frequency matching is impossible"], 0,
        "Bridge designers add dampers to limit resonance amplitude. Tuned mass dampers in tall bridge towers.",
        "জোরপূর্বক দোলায় অনুরণনে বিস্তার সীমিত (অসীম নয়) কারণ:", ["অবমন্দন — ঘর্ষণ বা রোধ শক্তি ক্ষয় করে", "অভিকর্ষ", "আদর্শভাবে অসীম হতে পারে", "কম্পাঙ্ক মেলানো অসম্ভব"],
        "সেতু ডিজাইনাররা অনুরণন বিস্তার সীমিত করতে অবমন্দক যোগ করেন। লম্বা সেতু টাওয়ারে সুর-করা ভর অবমন্দক।"),
    mcq("Sound travels fastest in:", ["Solids (highest bulk modulus and density combination gives highest v = √(E/ρ))", "Liquids", "Gases", "Vacuum"], 0,
        "v_steel ≈ 5000 m/s vs v_air ≈ 340 m/s. Ultrasonic testing of bridge steel exploits high speed in solids.",
        "শব্দ সবচেয়ে দ্রুত চলে:", ["কঠিনে (উচ্চ স্থিতিস্থাপকাঙ্ক ও ঘনত্বের সমন্বয়ে v = √(E/ρ) সর্বোচ্চ)", "তরলে", "গ্যাসে", "শূন্যে"],
        "v_ইস্পাত ≈ 5000 m/s বনাম v_বায়ু ≈ 340 m/s। সেতু ইস্পাতের আল্ট্রাসনিক পরীক্ষা কঠিনে উচ্চ বেগ ব্যবহার করে।"),
    mcq("The frequency of a closed organ pipe (one end closed) of length L is:", ["f_n = (2n-1)v/(4L) for n = 1,2,3… (only odd harmonics)", "f_n = nv/(2L)", "f_n = nv/(4L)", "f_n = v/(2L)"], 0,
        "Closed-end resonance: only odd harmonics (1st, 3rd, 5th…). Structural cavities in bridges can act as closed pipes.",
        "L দৈর্ঘ্যের বদ্ধ অর্গান পাইপের (এক প্রান্ত বন্ধ) কম্পাঙ্ক:", ["f_n = (2n-1)v/(4L) n = 1,2,3… (শুধু বিজোড় সুরঝংকার)", "f_n = nv/(2L)", "f_n = nv/(4L)", "f_n = v/(2L)"],
        "বদ্ধ প্রান্ত অনুরণন: শুধু বিজোড় সুরঝংকার। সেতুর কাঠামোগত গহ্বর বদ্ধ পাইপ হিসেবে কাজ করতে পারে।"),
    mcq("The coefficient of restitution e = (relative speed after)/(relative speed before). For a perfectly elastic collision:", ["e = 1 (no loss of kinetic energy)", "e = 0", "e > 1", "e = 0.5"], 0,
        "Real impact between a vehicle and a bridge barrier has e ≈ 0.1–0.3 (mostly inelastic).",
        "পুনরুজ্জীবন সহগ e = (পরে আপেক্ষিক বেগ)/(আগে আপেক্ষিক বেগ)। পূর্ণ স্থিতিস্থাপক সংঘর্ষে:", ["e = 1 (গতিশক্তির কোনো ক্ষতি নেই)", "e = 0", "e > 1", "e = 0.5"],
        "গাড়ি ও সেতু বাধার মধ্যে বাস্তব আঘাতে e ≈ 0.1–0.3 (বেশিরভাগ অস্থিতিস্থাপক)।"),
    mcq("Bulk modulus K is defined as K = -V(dP/dV). For water (K ≈ 2 GPa) vs air (K ≈ 0.14 MPa), water is:", ["About 14,000 times less compressible (harder to compress by pressure)", "More compressible", "About the same", "More compressible at high pressure only"], 0,
        "Water's high bulk modulus allows hydraulic jacks on bridges to transmit force with negligible fluid compression.",
        "স্থূল গুণাঙ্ক K = -V(dP/dV)। জল (K ≈ 2 GPa) বনাম বায়ু (K ≈ 0.14 MPa):", ["প্রায় 14,000 গুণ কম সংকোচনযোগ্য (চাপে সংকোচন কঠিন)", "বেশি সংকোচনযোগ্য", "প্রায় একই", "উচ্চ চাপে বেশি সংকোচনযোগ্য"],
        "জলের উচ্চ স্থূল গুণাঙ্ক সেতুতে হাইড্রোলিক জ্যাককে নগণ্য তরল সংকোচনে বল সঞ্চালন করতে দেয়।"),
    mcq("An electron in a hydrogen atom transitions from n=3 to n=2 (Balmer series). The energy of the emitted photon is:", ["E = 13.6(1/4 - 1/9) = 13.6 × 5/36 ≈ 1.89 eV (red light, Hα line)", "3.4 eV", "1.51 eV", "13.6 eV"], 0,
        "E = 13.6(1/n₁² - 1/n₂²). Balmer series is in visible range — used in spectroscopic material identification.",
        "হাইড্রোজেন পরমাণুতে n=3 থেকে n=2 (বামার শ্রেণি) রূপান্তরে নির্গত ফোটনের শক্তি:", ["E = 13.6(1/4 - 1/9) = 13.6 × 5/36 ≈ 1.89 eV (লাল আলো, Hα রেখা)", "3.4 eV", "1.51 eV", "13.6 eV"],
        "E = 13.6(1/n₁² - 1/n₂²)। বামার শ্রেণি দৃশ্যমান পরিসরে — বর্ণালীবিক্ষণ বস্তু সনাক্তে ব্যবহার।"),
    mcq("Modulation of a carrier wave is needed in radio communication because:", ["Audio frequencies (20 Hz–20 kHz) cannot propagate efficiently as radio waves without being superimposed on a high-frequency carrier", "Audio waves travel faster than radio", "Carriers lose information", "Antennas cannot detect audio frequencies directly"], 0,
        "AM/FM radio helps guide bridge construction teams — long-range communication via modulated radio waves.",
        "রেডিও যোগাযোগে বাহক তরঙ্গ মড্যুলেশন দরকার কারণ:", ["অডিও কম্পাঙ্ক (20 Hz–20 kHz) উচ্চ-কম্পাঙ্ক বাহকে না চাপালে দক্ষভাবে বিকিরণ হয় না", "অডিও তরঙ্গ দ্রুততর", "বাহক তথ্য হারায়", "অ্যান্টেনা সরাসরি অডিও কম্পাঙ্ক শনাক্ত করতে পারে না"],
        "AM/FM রেডিও সেতু নির্মাণ দলকে গাইড করে — মড্যুলেটেড রেডিও তরঙ্গে দূর-পাল্লার যোগাযোগ।"),
    mcq("A proton and an electron are placed in the same electric field E. Their accelerations are:", ["Different — a = qE/m; proton 1836 times heavier so 1836 times less acceleration", "Equal (same charge magnitude)", "Proton faster", "Electron has zero acceleration"], 0,
        "Mass spectrometers separate ions by charge-to-mass ratio — identifying bridge steel alloy composition.",
        "একই তড়িৎ ক্ষেত্র E-তে প্রোটন ও ইলেকট্রন। তাদের ত্বরণ:", ["ভিন্ন — a = qE/m; প্রোটন 1836 গুণ ভারী তাই 1836 গুণ কম ত্বরণ", "সমান (একই আধানের মাত্রা)", "প্রোটন দ্রুততর", "ইলেকট্রনের শূন্য ত্বরণ"],
        "ভর বর্ণালীমাপক আধান-থেকে-ভর অনুপাতে আয়ন আলাদা করে — সেতু ইস্পাত সংকর গঠন সনাক্ত করে।"),
    mcq("Two objects of masses 3 kg and 5 kg collide and stick together. If 3 kg was moving at 8 m/s and 5 kg was stationary, their common velocity after collision is:", ["3 m/s (3×8 + 5×0 = 8×v → v = 24/8 = 3 m/s)", "4.8 m/s", "5 m/s", "8 m/s"], 0,
        "Conservation of momentum: p_before = 3×8 = 24 kg·m/s = (3+5)v → v = 3 m/s.",
        "3 kg ও 5 kg বস্তু সংঘর্ষ করে এক হয়। 3 kg 8 m/s বেগে, 5 kg স্থির। সংঘর্ষের পর সাধারণ বেগ:", ["3 m/s (3×8 + 5×0 = 8×v → v = 3 m/s)", "4.8 m/s", "5 m/s", "8 m/s"],
        "ভরবেগ সংরক্ষণ: p_আগে = 3×8 = 24 kg·m/s = (3+5)v → v = 3 m/s।"),
    mcq("Pressure at depth h in a fluid of density ρ is P = P₀ + ρgh. At 10 m depth in water (ρ = 1000 kg/m³, g = 10), gauge pressure is:", ["100,000 Pa = 1 atm (1000 × 10 × 10 = 100,000 Pa)", "10,000 Pa", "1,000,000 Pa", "10 Pa"], 0,
        "Bridge pier foundations submerged 10 m experience ~1 atm extra pressure from water column alone.",
        "ঘনত্ব ρ তরলে h গভীরতায় চাপ P = P₀ + ρgh। জলে 10 m গভীরতায় গেজ চাপ:", ["100,000 Pa = 1 atm (1000 × 10 × 10 = 100,000 Pa)", "10,000 Pa", "1,000,000 Pa", "10 Pa"],
        "10 m নিমজ্জিত সেতু পিলার ভিত্তি শুধু জল কলাম থেকে ~1 atm অতিরিক্ত চাপ অনুভব করে।"),
    mcq("The SI unit of electric charge is the coulomb. One coulomb = one ampere × one second. The charge of one electron is:", ["e = 1.6×10⁻¹⁹ C (very small — current of 1 A ≈ 6.24×10¹⁸ electrons per second)", "1.6×10⁻²³ C", "9.1×10⁻³¹ C", "1 C"], 0,
        "One mole of electrons = Avogadro's number × e = 96,485 C (one Faraday).",
        "তড়িৎ আধানের SI একক কুলম্ব। এক কুলম্ব = এক অ্যাম্পিয়ার × এক সেকেন্ড। একটি ইলেকট্রনের আধান:", ["e = 1.6×10⁻¹⁹ C (অতি ক্ষুদ্র — 1 A ≈ প্রতি সেকেন্ডে 6.24×10¹⁸ ইলেকট্রন)", "1.6×10⁻²³ C", "9.1×10⁻³¹ C", "1 C"],
        "এক মোল ইলেকট্রন = অ্যাভোগাড্রো সংখ্যা × e = 96,485 C (এক ফ্যারাডে)।"),
    mcq("A transformer has 200 primary turns and 50 secondary turns. If input voltage is 240 V, the output voltage is:", ["60 V (V_s/V_p = N_s/N_p → V_s = 240 × 50/200 = 60 V)", "960 V", "120 V", "30 V"], 0,
        "Step-down transformer: 240V → 60V. Bridge instrument panels often use step-down transformers for safety.",
        "ট্রান্সফর্মারে 200 প্রাথমিক পাক ও 50 গৌণ পাক। ইনপুট ভোল্টেজ 240 V হলে আউটপুট:", ["60 V (V_s/V_p = N_s/N_p → V_s = 240 × 50/200 = 60 V)", "960 V", "120 V", "30 V"],
        "স্টেপ-ডাউন ট্রান্সফর্মার: 240V → 60V। সেতু যন্ত্র প্যানেলে নিরাপত্তার জন্য প্রায়ই স্টেপ-ডাউন ব্যবহার।"),
    mcq("The energy stored in a magnetic field of an inductor L carrying current I is:", ["E = ½LI²", "E = LI²", "E = LI", "E = L²I"], 0,
        "E = ½LI². Large inductors in bridge power-factor-correction equipment store energy during each AC cycle.",
        "প্রবাহ I বহনকারী আবেশক L-এর চৌম্বক ক্ষেত্রে সঞ্চিত শক্তি:", ["E = ½LI²", "E = LI²", "E = LI", "E = L²I"],
        "E = ½LI²। সেতু পাওয়ার-ফ্যাক্টর-সংশোধন সরঞ্জামে বড় আবেশক প্রতিটা AC চক্রে শক্তি সঞ্চয় করে।"),
    mcq("Which electromagnetic waves have the highest frequency (and energy per photon)?", ["Gamma rays (>10¹⁹ Hz, used in nuclear processes and radiography)", "X-rays", "UV light", "Radio waves"], 0,
        "Gamma radiography is the most penetrating NDT method for thick bridge steel welds.",
        "কোন তড়িৎচুম্বকীয় তরঙ্গের কম্পাঙ্ক (এবং ফোটন-প্রতি শক্তি) সর্বোচ্চ?", ["গামা রশ্মি (>10¹⁹ Hz, নিউক্লিয়ার প্রক্রিয়া ও রেডিওগ্রাফিতে)", "X-রশ্মি", "UV আলো", "রেডিও তরঙ্গ"],
        "গামা রেডিওগ্রাফি মোটা সেতু ইস্পাত ঝালাইয়ের সবচেয়ে ভেদনকারী NDT পদ্ধতি।"),
    mcq("If the distance between two charges is halved, the Coulomb force becomes:", ["4 times larger (F ∝ 1/r²: r halved → F × (2)² = 4)", "2 times larger", "Halved", "Unchanged"], 0,
        "F = kQ₁Q₂/r². Short-range electrostatic forces in concrete microstructure scale with r⁻².",
        "দুটো আধানের মধ্যে দূরত্ব অর্ধেক হলে কুলম্ব বল:", ["4 গুণ বড় (F ∝ 1/r²: r অর্ধেক → F × (2)² = 4)", "2 গুণ বড়", "অর্ধেক", "অপরিবর্তিত"],
        "F = kQ₁Q₂/r²। কংক্রিট মাইক্রোস্ট্রাকচারে স্বল্প-পাল্লার তড়িৎস্থিত বল r⁻² এ স্কেল হয়।"),
    mcq("A wire of resistance R is stretched to double its length (volume stays constant). The new resistance is:", ["4R (length doubles → R ∝ L²/volume → R × 4)", "2R", "R/2", "R/4"], 0,
        "When L doubles, cross-section halves: R = ρL/A → ρ(2L)/(A/2) = 4ρL/A = 4R.",
        "রোধ R-এর তার দ্বিগুণ দৈর্ঘ্যে প্রসারিত (আয়তন স্থির)। নতুন রোধ:", ["4R (দৈর্ঘ্য দ্বিগুণ → R ∝ L²/আয়তন → R × 4)", "2R", "R/2", "R/4"],
        "L দ্বিগুণ হলে প্রস্থচ্ছেদ অর্ধেক: R = ρL/A → ρ(2L)/(A/2) = 4ρL/A = 4R।"),
    mcq("What is the relation between electric field E and electric potential V?", ["E = -dV/dr (field is the negative gradient of potential)", "E = V/r", "E = V²/r", "V = E²/r"], 0,
        "E = -∇V. Mapping potential on bridge structures identifies corrosion current pathways.",
        "তড়িৎ ক্ষেত্র E ও তড়িৎ বিভব V-এর সম্পর্ক:", ["E = -dV/dr (ক্ষেত্র হল বিভবের ঋণাত্মক গ্রেডিয়েন্ট)", "E = V/r", "E = V²/r", "V = E²/r"],
        "E = -∇V। সেতু কাঠামোতে বিভব ম্যাপিং ক্ষয়ের প্রবাহ পথ সনাক্ত করে।"),
    mcq("A photon has zero rest mass but carries momentum p = h/λ. This was verified by:", ["Compton scattering (1923) — X-rays colliding with electrons showed measurable momentum transfer", "Double-slit experiment", "Photoelectric effect", "Rutherford scattering"], 0,
        "Radiation pressure (photon momentum) is negligible on bridges but relevant in solar-sail spacecraft.",
        "ফোটনের বিশ্রাম ভর শূন্য কিন্তু ভরবেগ p = h/λ আছে। এটা যাচাই করা হয়:", ["কম্পটন বিচ্ছুরণে (1923) — ইলেকট্রনে X-রশ্মির সংঘর্ষে পরিমাপযোগ্য ভরবেগ স্থানান্তর", "দ্বি-চির পরীক্ষা", "আলোতড়িৎ প্রভাব", "রাদারফোর্ড বিচ্ছুরণ"],
        "বিকিরণ চাপ (ফোটন ভরবেগ) সেতুতে নগণ্য কিন্তু সোলার-সেল মহাকাশযানে প্রাসঙ্গিক।"),
    mcq("In a common-base transistor configuration, the current gain α = I_C/I_E is:", ["Slightly less than 1 (approximately 0.95 to 0.99 for typical transistors)", "Greater than 1", "Exactly 1", "Equal to β"], 0,
        "α = β/(1+β). For β = 99, α = 99/100 = 0.99. Bridge sensor signal amplifiers use transistor circuits.",
        "সাধারণ-ভূমি ট্রানজিস্টর বিন্যাসে প্রবাহ লাভ α = I_C/I_E:", ["1-এর সামান্য কম (সাধারণত 0.95 থেকে 0.99)", "1-এর বেশি", "ঠিক 1", "β-এর সমান"],
        "α = β/(1+β)। β = 99 হলে α = 0.99। সেতু সেন্সর সংকেত বিবর্ধকে ট্রানজিস্টর সার্কিট।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
