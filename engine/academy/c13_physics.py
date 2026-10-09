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
]

ITEMS = tuple(NUMERIC + CONCEPTS)
