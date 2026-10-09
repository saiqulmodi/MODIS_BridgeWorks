"""NIT level - Chemistry (JEE Main standard): mole concept and stoichiometry, gases, solutions and
colligative properties, chemical and ionic equilibrium, thermodynamics, kinetics, electrochemistry,
atomic structure and bonding, solid state, the periodic table, s-, p- and d-block chemistry,
coordination compounds, organic reaction mechanisms, named reactions, polymers and biomolecules."""
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


def _sup(n):
    """10⁻⁵ style exponents."""
    return str(n).translate(str.maketrans("0123456789.-", "⁰¹²³⁴⁵⁶⁷⁸⁹·⁻"))


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    r = _c(r)
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [_f(x) + u_en for x in o], 0, ex_en, q_bn, [_f(x) + ub for x in o], ex_bn)


# ---------------------------------------------------------------- mole concept and stoichiometry
def moles(name_en, name_bn, m, mm):
    n = m / mm
    return _n(f"How many moles are there in {m:g} g of {name_en} (molar mass {mm} g/mol)?",
              f"{m:g} g {name_bn}-এ (মোলার ভর {mm} g/mol) কত মোল আছে?", n,
              f"n = mass ÷ molar mass = {m:g} ÷ {mm} = {_f(_c(n))} mol.",
              f"মোল-সংখ্যা = ভর ÷ মোলার ভর = {m:g} ÷ {mm} = {_f(_c(n))}।",
              (mm / m, m * mm / 100, n / 2), " mol", "")


def molecules(name_en, name_bn, m, mm):
    n = m / mm * 6.022
    return _n(f"How many molecules are present in {m:g} g of {name_en} (molar mass {mm} g/mol)? (N_A = 6.022 x 10²³)",
              f"{m:g} g {name_bn}-এ (মোলার ভর {mm} g/mol) কতগুলো অণু আছে? (N_A = 6.022 x 10²³)", n,
              f"{m:g} ÷ {mm} = {_f(_c(m / mm))} mol; x 6.022 x 10²³ = {_f(_c(n))} x 10²³ molecules.",
              f"{m:g} ÷ {mm} = {_f(_c(m / mm))} মোল; x 6.022 x 10²³ = {_f(_c(n))} x 10²³টি অণু।",
              (6.022, n / 2, n * 3), " x 10²³", " x 10²³টি")


def molarity(m, mm, ml, solute_en, solute_bn):
    c = m / mm / (ml / 1000)
    return _n(f"{m:g} g of {solute_en} (molar mass {mm} g/mol) is dissolved to make {ml} mL of solution. What is its molarity?",
              f"{m:g} g {solute_bn} (মোলার ভর {mm} g/mol) গুলে {ml} mL দ্রবণ তৈরি করা হল। এর মোলারিটি কত?", c,
              f"M = moles ÷ litres = ({m:g} ÷ {mm}) ÷ {ml / 1000:g} = {_f(_c(c))} M.",
              f"মোলারিটি = মোল ÷ লিটার = ({m:g} ÷ {mm}) ÷ {ml / 1000:g} = {_f(_c(c))} M।",
              (m / mm, c / 2, m / ml), " M")


def dilution(m1, v1, v2):
    m2 = m1 * v1 / v2
    return _n(f"{v1} mL of {m1:g} M acid is diluted with water to {v2} mL. What is the new molarity?",
              f"{m1:g} M অ্যাসিডের {v1} mL জল দিয়ে পাতলা করে {v2} mL করা হল। নতুন মোলারিটি কত?", m2,
              f"M₁V₁ = M₂V₂: M₂ = {m1:g} x {v1} ÷ {v2} = {_f(_c(m2))} M.",
              f"M₁V₁ = M₂V₂ সূত্রে নতুন মোলারিটি = {m1:g} x {v1} ÷ {v2} = {_f(_c(m2))} M।",
              (m1 * v2 / v1, m1, m2 * 2), " M")


def molality(m, mm, kg):
    b = m / mm / kg
    return _n(f"{m:g} g of glucose (molar mass {mm} g/mol) is dissolved in {kg:g} kg of water. What is the molality?",
              f"{kg:g} kg জলে {m:g} g গ্লুকোজ (মোলার ভর {mm} g/mol) গোলা হল। মোলালিটি কত?", b,
              f"m = moles of solute ÷ kg of solvent = ({m:g} ÷ {mm}) ÷ {kg:g} = {_f(_c(b))} mol/kg.",
              f"মোলালিটি = দ্রাবের মোল ÷ দ্রাবকের kg = ({m:g} ÷ {mm}) ÷ {kg:g} = {_f(_c(b))} m।",
              (m / mm, b * 2, m / kg / 100), " mol/kg", " m")


def titration(m_acid, v_acid, basicity, m_base):
    v = m_acid * v_acid * basicity / m_base
    acid_en, acid_bn = ("H₂SO₄", "সালফিউরিক অ্যাসিড (H₂SO₄)") if basicity == 2 else ("HCl", "হাইড্রোক্লোরিক অ্যাসিড")
    return _n(f"What volume of {m_base:g} M NaOH neutralises {v_acid} mL of {m_acid:g} M {acid_en}?",
              f"{m_acid:g} M {acid_bn}-এর {v_acid} mL প্রশমিত করতে {m_base:g} M সোডিয়াম হাইড্রক্সাইডের কত আয়তন লাগে?", v,
              f"Moles of H⁺ = {m_acid:g} x {v_acid} x {basicity} = moles of OH⁻ = {m_base:g} x V, so V = {_f(_c(v))} mL.",
              f"H⁺-এর মোল = {m_acid:g} x {v_acid} x {basicity} = OH⁻-এর মোল = {m_base:g} x V, তাই আয়তন = {_f(_c(v))} mL।",
              (m_acid * v_acid / m_base, v / 2, v * 2), " mL")


def limiting(h2):
    nh3 = h2 / 6 * 2 * 17
    return _n(f"28 g of N₂ reacts with {h2} g of H₂ to form ammonia (N₂ + 3H₂ → 2NH₃). What mass of NH₃ forms at most?",
              f"28 g N₂, {h2} g H₂-এর সঙ্গে বিক্রিয়া করে অ্যামোনিয়া তৈরি করে (N₂ + 3H₂ → 2NH₃)। সর্বোচ্চ কত ভর NH₃ তৈরি হয়?", nh3,
              f"1 mol N₂ needs 3 mol H₂ = 6 g; only {h2} g H₂ = {_f(_c(h2 / 2))} mol, so H₂ limits: NH₃ = {_f(_c(h2 / 2))} x 2/3 mol x 17 = {_f(_c(nh3))} g.",
              f"1 মোল N₂-এর জন্য 3 মোল H₂ = 6 g লাগে; আছে মাত্র {h2} g H₂ = {_f(_c(h2 / 2))} মোল, তাই H₂ সীমাবদ্ধকারী: NH₃ = {_f(_c(h2 / 2))} x 2/3 মোল x 17 = {_f(_c(nh3))} g।",
              (34, 28 + h2, h2 * 17 / 2), " g")


def percent_mass(el_en, el_bn, part, total, comp):
    p = part / total * 100
    return _n(f"What is the percentage by mass of {el_en} in {comp} (molar mass {total} g/mol, containing {part} g of {el_en} per mole)?",
              f"{comp}-এ (মোলার ভর {total} g/mol, প্রতি মোলে {part} g {el_bn}) {el_bn}-এর ভর-শতাংশ কত?", p,
              f"% = {part} ÷ {total} x 100 = {_f(_c(p))}%.",
              f"শতাংশ = {part} ÷ {total} x 100 = {_f(_c(p))}%।",
              (100 - p, part, p / 2), "%")


# ---------------------------------------------------------------- gases
def stp_volume(m, mm, gas_en, gas_bn):
    v = m / mm * 22.4
    return _n(f"What volume does {m:g} g of {gas_en} (molar mass {mm} g/mol) occupy at STP? (Molar volume 22.4 L)",
              f"প্রমাণ উষ্ণতা ও চাপে {m:g} g {gas_bn} (মোলার ভর {mm} g/mol) কত আয়তন দখল করে? (মোলার আয়তন 22.4 L)", v,
              f"{m:g} ÷ {mm} = {_f(_c(m / mm))} mol x 22.4 L = {_f(_c(v))} L.",
              f"{m:g} ÷ {mm} = {_f(_c(m / mm))} মোল x 22.4 L = {_f(_c(v))} L।",
              (22.4, m * 22.4 / 100, v * 2), " L")


def graham(m1, m2, g1_en, g1_bn, g2_en, g2_bn):
    r = math.sqrt(m2 / m1)
    return _n(f"How many times faster does {g1_en} (M = {m1}) diffuse than {g2_en} (M = {m2}) under the same conditions?",
              f"একই অবস্থায় {g1_bn} (M = {m1}), {g2_bn} (M = {m2})-এর চেয়ে কত গুণ দ্রুত ব্যাপিত হয়?", r,
              f"Graham's law: rate ∝ 1/√M, so the ratio is √({m2}/{m1}) = {_f(_c(r))}.",
              f"গ্রাহামের সূত্র: হার ∝ 1/√M, তাই অনুপাত √({m2}/{m1}) = {_f(_c(r))}।",
              (m2 / m1, math.sqrt(m1 / m2), r + 0.5), " times", " গুণ")


def partial(x_txt, x, p):
    pp = x * p
    return _n(f"A gas mixture at {p} atm contains a gas with mole fraction {x_txt}. What is that gas's partial pressure?",
              f"{p} atm চাপের একটা গ্যাস-মিশ্রণে একটা গ্যাসের মোল-ভগ্নাংশ {x_txt}। ওই গ্যাসের আংশিক চাপ কত?", pp,
              f"Dalton's law: p = x P = {x_txt} x {p} = {_f(_c(pp))} atm.",
              f"ডাল্টনের সূত্র: আংশিক চাপ = x P = {x_txt} x {p} = {_f(_c(pp))} atm।",
              (p - pp, p, pp * 2), " atm", " atm (বায়ুমণ্ডল)")


# ---------------------------------------------------------------- solutions
def boiling(kb, m, i, solute_en, solute_bn):
    d = i * kb * m
    return _n(f"By how much does a {m:g} molal aqueous solution of {solute_en} raise the boiling point of water? (K_b = {kb} K kg/mol, van 't Hoff factor i = {i})",
              f"{solute_bn}-এর {m:g} মোলাল জলীয় দ্রবণ জলের স্ফুটনাঙ্ক কতটা বাড়ায়? (K_b = {kb} K kg/mol, ভ্যান্ট হফ গুণক i = {i})", d,
              f"ΔT_b = i K_b m = {i} x {kb} x {m:g} = {_f(_c(d))} K.",
              f"স্ফুটনাঙ্কের বৃদ্ধি = i K_b m = {i} x {kb} x {m:g} = {_f(_c(d))} K।",
              (kb * m, d / 2 if i > 1 else d * 2, kb * m * 3), " K")


def freezing(m, i, solute_en, solute_bn):
    d = i * 1.86 * m
    return _n(f"What is the depression in freezing point of a {m:g} molal aqueous solution of {solute_en}? (K_f = 1.86 K kg/mol, i = {i})",
              f"{solute_bn}-এর {m:g} মোলাল জলীয় দ্রবণে হিমাঙ্কের অবনমন কত? (K_f = 1.86 K kg/mol, i = {i})", d,
              f"ΔT_f = i K_f m = {i} x 1.86 x {m:g} = {_f(_c(d))} K.",
              f"হিমাঙ্কের অবনমন = i K_f m = {i} x 1.86 x {m:g} = {_f(_c(d))} K।",
              (1.86 * m, d / 2 if i > 1 else d * 2, 1.86 * m * 3), " K")


def osmotic(c, t):
    p = c * 0.0821 * t
    return _n(f"What is the osmotic pressure of a {c:g} M glucose solution at {t} K? (R = 0.0821 L atm/(mol K))",
              f"{t} K-এ {c:g} M গ্লুকোজ দ্রবণের অভিস্রবণ চাপ কত? (R = 0.0821 L atm/(mol K))", p,
              f"π = CRT = {c:g} x 0.0821 x {t} = {_f(_c(p))} atm.",
              f"অভিস্রবণ চাপ = CRT = {c:g} x 0.0821 x {t} = {_f(_c(p))} atm।",
              (c * t / 100, p * 2, c * 0.0821), " atm", " atm (বায়ুমণ্ডল)")


def raoult(p0, x):
    p = p0 * (1 - x)
    return _n(f"Pure water has a vapour pressure of {p0} mm Hg. What is the vapour pressure of a solution in which the non-volatile solute's mole fraction is {x:g}?",
              f"বিশুদ্ধ জলের বাষ্পচাপ {p0} mm Hg। যে দ্রবণে অনুদ্বায়ী দ্রাবের মোল-ভগ্নাংশ {x:g}, তার বাষ্পচাপ কত?", p,
              f"Raoult's law: p = p⁰ x_solvent = {p0} x {_f(_c(1 - x))} = {_f(_c(p))} mm Hg.",
              f"রাউল্টের সূত্র: বাষ্পচাপ = p⁰ x দ্রাবকের মোল-ভগ্নাংশ = {p0} x {_f(_c(1 - x))} = {_f(_c(p))} mm Hg।",
              (p0 * x, p0, p0 - x * 10), " mm Hg", " mm পারদ")


# ---------------------------------------------------------------- ionic equilibrium
def ph_strong(c_txt, h_exp, what_en, what_bn, base):
    ph = 14 - h_exp if base else h_exp
    return _n(f"What is the pH of {c_txt} {what_en} at 25°C?",
              f"25°C-এ {c_txt} {what_bn}-এর pH কত?", ph,
              (f"[OH⁻] = 10⁻{_sup(h_exp)}, pOH = {h_exp}, pH = 14 - {h_exp} = {ph}." if base else
               f"Full ionisation gives [H⁺] = 10⁻{_sup(h_exp)} M, so pH = {ph}."),
              (f"[OH⁻] = 10⁻{_sup(h_exp)}, pOH = {h_exp}, তাই pH = 14 - {h_exp} = {ph}।" if base else
               f"সম্পূর্ণ আয়নীভবনে [H⁺] = 10⁻{_sup(h_exp)} M, তাই pH = {ph}।"),
              (14 - ph, ph + 2, ph + 1))


def ph_weak(ka_exp, c_exp):
    ph = (ka_exp + c_exp) / 2
    return _n(f"A weak acid with Ka = 10⁻{_sup(ka_exp)} is present at 10⁻{_sup(c_exp)} M. What is the pH of the solution?",
              f"Ka = 10⁻{_sup(ka_exp)}-এর একটা দুর্বল অ্যাসিড 10⁻{_sup(c_exp)} M ঘনমাত্রায় আছে। দ্রবণের pH কত?", ph,
              f"[H⁺] = √(Ka C) = √(10⁻{_sup(ka_exp)} x 10⁻{_sup(c_exp)}) = 10⁻{_sup(_f(_c(ph)))}, so pH = {_f(_c(ph))}.",
              f"[H⁺] = √(Ka C) = √(10⁻{_sup(ka_exp)} x 10⁻{_sup(c_exp)}) = 10⁻{_sup(_f(_c(ph)))}, তাই pH = {_f(_c(ph))}।",
              (c_exp, ka_exp, ph + 1))


def buffer(pka, ratio_txt, ratio):
    ph = pka + math.log10(ratio)
    return _n(f"A buffer contains acetate and acetic acid (pKa = {pka}) in the ratio [salt]/[acid] = {ratio_txt}. What is its pH?",
              f"একটা বাফারে অ্যাসিটেট আর অ্যাসিটিক অ্যাসিড (pKa = {pka}) [লবণ]/[অ্যাসিড] = {ratio_txt} অনুপাতে আছে। এর pH কত?", ph,
              f"Henderson equation: pH = pKa + log({ratio_txt}) = {pka} + ({_f(_c(math.log10(ratio)))}) = {_f(_c(ph))}.",
              f"হেন্ডারসনের সমীকরণ: pH = pKa + log({ratio_txt}) = {pka} + ({_f(_c(math.log10(ratio)))}) = {_f(_c(ph))}।",
              (pka, pka - math.log10(ratio) if ratio != 1 else pka + 1, 7))


def ksp(k_exp, salt_en, salt_bn):
    s = k_exp / 2
    return mcq(f"The solubility product of {salt_en} is 1 x 10⁻{_sup(k_exp)}. What is its molar solubility in pure water?",
               [f"1 x 10⁻{_sup(f"{s:g}")} M", f"1 x 10⁻{_sup(k_exp)} M", f"2 x 10⁻{_sup(f"{s:g}")} M", f"1 x 10⁻{_sup(k_exp * 2)} M"], 0,
               f"For an AB salt Ksp = s², so s = √(10⁻{_sup(k_exp)}) = 10⁻{_sup(f"{s:g}")} M.",
               f"{salt_bn}-এর দ্রাব্যতা-গুণফল 1 x 10⁻{_sup(k_exp)}। বিশুদ্ধ জলে এর মোলার দ্রাব্যতা কত?",
               [f"1 x 10⁻{_sup(f"{s:g}")} M", f"1 x 10⁻{_sup(k_exp)} M", f"2 x 10⁻{_sup(f"{s:g}")} M", f"1 x 10⁻{_sup(k_exp * 2)} M"],
               f"AB ধরনের লবণে Ksp = s², তাই দ্রাব্যতা = √(10⁻{_sup(k_exp)}) = 10⁻{_sup(f"{s:g}")} M।")


def kc(a, b, c):
    k = c / (a * b)
    return _n(f"For A + B ⇌ C at equilibrium, [A] = {a:g} M, [B] = {b:g} M and [C] = {c:g} M. What is Kc?",
              f"A + B ⇌ C সাম্যাবস্থায় [A] = {a:g} M, [B] = {b:g} M আর [C] = {c:g} M। Kc কত?", k,
              f"Kc = [C] ÷ ([A][B]) = {c:g} ÷ ({a:g} x {b:g}) = {_f(_c(k))}.",
              f"সাম্য-ধ্রুবক Kc = [C] ÷ ([A][B]) = {c:g} ÷ ({a:g} x {b:g}) = {_f(_c(k))}।",
              (a * b / c, c / (a + b), k * 2))


# ---------------------------------------------------------------- thermodynamics and kinetics
def bond_energy(hh, xx, hx, name_en, name_bn):
    q = 2 * hx - hh - xx
    return _n(f"Using bond energies H-H = {hh}, {name_en} = {xx} and H-X = {hx} kJ/mol, how much heat is released when 1 mol of H₂ reacts with 1 mol of the halogen to give 2 mol of HX?",
              f"বন্ধনশক্তি H-H = {hh}, {name_bn} = {xx} আর H-X = {hx} kJ/mol ধরে, 1 মোল H₂ আর 1 মোল হ্যালোজেন বিক্রিয়া করে 2 মোল HX দিলে কত তাপ মুক্ত হয়?", q,
              f"ΔH = bonds broken - bonds formed = ({hh} + {xx}) - 2 x {hx} = -{q} kJ, so {q} kJ is released.",
              f"ΔH = ভাঙা বন্ধন - গঠিত বন্ধন = ({hh} + {xx}) - 2 x {hx} = -{q} kJ, তাই {q} kJ তাপ মুক্ত হয়।",
              (hx - hh, hh + xx - hx, q * 2), " kJ")


def hess(a, b):
    r = a - b
    return _n(f"C + O₂ → CO₂ releases {a} kJ and CO + ½O₂ → CO₂ releases {b} kJ. How much heat is released by C + ½O₂ → CO?",
              f"C + O₂ → CO₂ বিক্রিয়ায় {a} kJ আর CO + ½O₂ → CO₂ বিক্রিয়ায় {b} kJ তাপ মুক্ত হয়। C + ½O₂ → CO বিক্রিয়ায় কত তাপ মুক্ত হয়?", r,
              f"Hess's law: subtract the second equation from the first: {a} - {b} = {r} kJ.",
              f"হেসের সূত্র: প্রথম সমীকরণ থেকে দ্বিতীয়টা বিয়োগ: {a} - {b} = {r} kJ।",
              (a + b, b, a), " kJ")


def gibbs_t(dh, ds):
    t = dh * 1000 / ds
    return _n(f"A reaction has ΔH = +{dh} kJ/mol and ΔS = +{ds} J/(mol K). Above what temperature does it become spontaneous?",
              f"একটা বিক্রিয়ার ΔH = +{dh} kJ/mol আর ΔS = +{ds} J/(mol K)। কোন তাপমাত্রার উপরে এটা স্বতঃস্ফূর্ত হয়?", t,
              f"ΔG = ΔH - TΔS < 0 when T > ΔH ÷ ΔS = {dh * 1000:,} ÷ {ds} = {_f(_c(t))} K.",
              f"ΔG = ΔH - TΔS < 0 হয় যখন তাপমাত্রা > ΔH ÷ ΔS = {dh * 1000:,} ÷ {ds} = {_f(_c(t))} K।",
              (dh / ds, t / 2, t + 273), " K")


def first_order_half(k):
    t = 0.693 / k
    return _n(f"A first-order reaction has a rate constant of {k:g} per minute. What is its half-life?",
              f"একটা প্রথম-ক্রমের বিক্রিয়ার হার-ধ্রুবক প্রতি মিনিটে {k:g}। এর অর্ধায়ু কত?", t,
              f"t½ = 0.693 ÷ k = 0.693 ÷ {k:g} = {_f(_c(t))} min - independent of the starting concentration.",
              f"অর্ধায়ু = 0.693 ÷ k = 0.693 ÷ {k:g} = {_f(_c(t))} মিনিট - শুরুর ঘনমাত্রার উপর নির্ভর করে না।",
              (1 / k, t * 2, k * 0.693 * 100), " min", " মিনিট")


def completion(t_half, pct, n):
    t = t_half * n
    return _n(f"A first-order reaction has a half-life of {t_half} min. How long does it take to reach {pct}% completion?",
              f"একটা প্রথম-ক্রমের বিক্রিয়ার অর্ধায়ু {t_half} মিনিট। {pct}% সম্পূর্ণ হতে কত সময় লাগে?", t,
              f"{pct}% done leaves {100 - pct:g}% = (1/2)^{n}, i.e. {n} half-lives: {n} x {t_half} = {t} min.",
              f"{pct}% সম্পূর্ণ মানে {100 - pct:g}% বাকি = (1/2)^{n}, অর্থাৎ {n}টি অর্ধায়ু: {n} x {t_half} = {t} মিনিট।",
              (t_half * pct / 50, t_half, t + t_half), " min", " মিনিট")


def temp_rate(rise):
    f = 2 ** (rise / 10)
    return _n(f"A reaction's rate doubles for every 10°C rise. By what factor does it increase when the temperature rises by {rise}°C?",
              f"একটা বিক্রিয়ার হার প্রতি 10°C বৃদ্ধিতে দ্বিগুণ হয়। তাপমাত্রা {rise}°C বাড়লে হার কত গুণ বাড়ে?", f,
              f"{rise}°C is {rise // 10} steps of 10°C: 2^{rise // 10} = {_f(_c(f))} times.",
              f"{rise}°C মানে 10°C-এর {rise // 10}টি ধাপ: 2^{rise // 10} = {_f(_c(f))} গুণ।",
              (rise / 10 * 2, rise / 10, f * 2), " times", " গুণ")


def order(factor_c, factor_r):
    n = math.log(factor_r) / math.log(factor_c)
    return _n(f"Raising the concentration of a reactant {factor_c} times raises the rate {factor_r} times. What is the order with respect to that reactant?",
              f"একটা বিক্রিয়কের ঘনমাত্রা {factor_c} গুণ করলে হার {factor_r} গুণ হয়। ওই বিক্রিয়কের সাপেক্ষে ক্রম কত?", n,
              f"rate ∝ [A]ⁿ: {factor_c}ⁿ = {factor_r}, so n = {_f(_c(n))}.",
              f"হার ∝ [A]ⁿ: {factor_c}ⁿ = {factor_r}, তাই ক্রম = {_f(_c(n))}।",
              (factor_r / factor_c, factor_r, n + 2))


# ---------------------------------------------------------------- electrochemistry
def ecell(c_en, c_bn, ec, a_en, a_bn, ea):
    e = ec - ea
    return _n(f"What is the standard emf of a cell with a {c_en} cathode (E° = {ec:+g} V) and a {a_en} anode (E° = {ea:+g} V)?",
              f"{c_bn} ক্যাথোড (E° = {ec:+g} V) আর {a_bn} অ্যানোডের (E° = {ea:+g} V) একটা কোষের প্রমাণ তড়িচ্চালক বল কত?", e,
              f"E°cell = E°cathode - E°anode = {ec:+g} - ({ea:+g}) = {_f(_c(e))} V.",
              f"কোষের E° = ক্যাথোডের E° - অ্যানোডের E° = {ec:+g} - ({ea:+g}) = {_f(_c(e))} V।",
              (abs(ec + ea), abs(ec), abs(ea)), " V")


def nernst(e0, n, logq):
    e = e0 - 0.059 / n * logq
    return _n(f"A cell has E° = {e0:g} V with n = {n} electrons transferred. What is its emf at 25°C when log Q = {logq}?",
              f"একটা কোষের E° = {e0:g} V, n = {n}টি ইলেকট্রন স্থানান্তরিত হয়। 25°C-এ log Q = {logq} হলে এর তড়িচ্চালক বল কত?", e,
              f"Nernst equation: E = E° - (0.059/n) log Q = {e0:g} - (0.059/{n}) x {logq} = {_f(_c(e))} V.",
              f"নার্নস্টের সমীকরণ: E = E° - (0.059/n) log Q = {e0:g} - (0.059/{n}) x {logq} = {_f(_c(e))} V।",
              (e0, e0 + 0.059 / n * logq, e0 - 0.059 * logq), " V")


def electrolysis(metal_en, metal_bn, mm, z, i, t):
    m = mm * i * t / (z * 96500)
    return _n(f"A current of {i} A is passed for {t:,} s through a solution of {metal_en} ions (charge {z}+, molar mass {mm}). What mass of metal is deposited? (F = 96,500 C/mol)",
              f"{metal_bn} আয়নের ({z}+ আধান, মোলার ভর {mm}) দ্রবণে {t:,} s ধরে {i} A প্রবাহ পাঠানো হল। কত ভর ধাতু জমা হয়? (F = 96,500 C/mol)", m,
              f"Charge = {i} x {t:,} = {i * t:,} C = {_f(_c(i * t / 96500))} mol e⁻; metal = that ÷ {z} mol x {mm} = {_f(_c(m))} g.",
              f"আধান = {i} x {t:,} = {i * t:,} C = {_f(_c(i * t / 96500))} মোল ইলেকট্রন; ধাতু = তা ÷ {z} মোল x {mm} = {_f(_c(m))} g।",
              (m * z, m / 2 if z == 1 else m * 2 / z * 3, mm * i * t / 96500 / 10), " g")


def gibbs_cell(n, e):
    g = n * 96500 * e / 1000
    return _n(f"A cell reaction transfers {n} mol of electrons and has E°cell = {e:g} V. What is the magnitude of ΔG°?",
              f"একটা কোষ-বিক্রিয়ায় {n} মোল ইলেকট্রন স্থানান্তরিত হয়, E°কোষ = {e:g} V। ΔG°-এর মান কত?", g,
              f"ΔG° = -nFE° = -{n} x 96,500 x {e:g} J = -{_f(_c(g))} kJ: negative, so the reaction is spontaneous.",
              f"ΔG° = -nFE° = -{n} x 96,500 x {e:g} J = -{_f(_c(g))} kJ: ঋণাত্মক, তাই বিক্রিয়া স্বতঃস্ফূর্ত।",
              (g / n, g * 2, 96.5 * e / n), " kJ")


def molar_cond(kappa, c):
    lam = kappa * 1000 / c
    return _n(f"A {c:g} M solution has a conductivity of {kappa:g} S/cm. What is its molar conductivity?",
              f"{c:g} M দ্রবণের পরিবাহিতা {kappa:g} S/cm। এর মোলার পরিবাহিতা কত?", lam,
              f"Λm = κ x 1000 ÷ C = {kappa:g} x 1000 ÷ {c:g} = {_f(_c(lam))} S cm²/mol.",
              f"মোলার পরিবাহিতা = κ x 1000 ÷ C = {kappa:g} x 1000 ÷ {c:g} = {_f(_c(lam))} S cm²/mol।",
              (kappa / c, lam / 10, lam * 10), " S cm²/mol", " S cm²/মোল")


# ---------------------------------------------------------------- structure
def spin_moment(ion_en, ion_bn, n):
    mu = math.sqrt(n * (n + 2))
    return _n(f"What is the spin-only magnetic moment of {ion_en}, which has {n} unpaired electron{'s' if n > 1 else ''}?",
              f"{ion_bn}-এ {n}টি অযুগ্ম ইলেকট্রন আছে। এর কেবল-স্পিন চৌম্বক ভ্রামক কত?", mu,
              f"μ = √(n(n + 2)) = √({n} x {n + 2}) = {_f(_c(mu))} BM.",
              f"চৌম্বক ভ্রামক = √(n(n + 2)) = √({n} x {n + 2}) = {_f(_c(mu))} BM।",
              (n, math.sqrt(n * (n + 1)), n * 2), " BM")


def radial_nodes(orb, n, l):
    r = n - l - 1
    return _n(f"How many radial nodes does a {orb} orbital have?",
              f"একটা {orb} কক্ষকের কয়টি ব্যাসার্ধীয় নোড আছে?", r if r > 0 else 0,
              f"Radial nodes = n - l - 1 = {n} - {l} - 1 = {r}; angular nodes = l = {l}.",
              f"ব্যাসার্ধীয় নোড = n - l - 1 = {n} - {l} - 1 = {r}; কৌণিক নোড = l = {l}।",
              (n - 1, l, n), "", "") if r > 0 else None


def bond_order(sp_en, sp_bn, bo, how_en, how_bn):
    return _n(f"What is the bond order of {sp_en} according to molecular orbital theory?",
              f"আণবিক কক্ষক তত্ত্ব অনুযায়ী {sp_bn}-এর বন্ধন-ক্রম কত?", bo, how_en, how_bn,
              (bo + 0.5, bo - 0.5 if bo > 1 else 3, bo + 1))


def dbe(formula, c, h):
    d = (2 * c + 2 - h) // 2
    return _n(f"What is the degree of unsaturation (double-bond equivalent) of {formula}?",
              f"{formula}-এর অসম্পৃক্ততার মাত্রা (দ্বিবন্ধন-তুল্য) কত?", d,
              f"DBE = (2C + 2 - H) ÷ 2 = (2 x {c} + 2 - {h}) ÷ 2 = {d}: rings plus π bonds.",
              f"দ্বিবন্ধন-তুল্য = (2C + 2 - H) ÷ 2 = (2 x {c} + 2 - {h}) ÷ 2 = {d}: বলয় আর π বন্ধনের যোগফল।",
              (d + 1, c - d if c - d > 0 else d + 2, d * 2))


def cell_density(z, mm, a_pm, kind_en, kind_bn):
    rho = z * mm / (6.022e23 * (a_pm * 1e-10) ** 3)
    return _n(f"A metal (molar mass {mm} g/mol) has a {kind_en} unit cell of edge {a_pm} pm. What is its density?",
              f"একটা ধাতুর (মোলার ভর {mm} g/mol) {kind_bn} একক-কোষের ধার {a_pm} pm। এর ঘনত্ব কত?", rho,
              f"Z = {z}; ρ = ZM ÷ (a³ N_A) = {z} x {mm} ÷ (({a_pm} x 10⁻¹⁰ cm)³ x 6.022 x 10²³) = {_f(_c(rho))} g/cm³.",
              f"Z = {z}; ঘনত্ব = ZM ÷ (a³ N_A) = {z} x {mm} ÷ (({a_pm} x 10⁻¹⁰ cm)³ x 6.022 x 10²³) = {_f(_c(rho))} g/cm³।",
              (rho / z, rho * 2, rho + 2), " g/cm³")


def isomers_chiral(n):
    r = 2 ** n
    return _n(f"A compound has {n} different chiral centres and no internal symmetry. How many stereoisomers can it have?",
              f"একটা যৌগে {n}টি ভিন্ন কাইরাল কেন্দ্র আছে আর কোনো অভ্যন্তরীণ প্রতিসাম্য নেই। এর কয়টি স্টেরিও-সমাণু হতে পারে?", r,
              f"Each centre can be R or S: 2^{n} = {r}.",
              f"প্রতিটি কেন্দ্র R বা S হতে পারে: 2^{n} = {r}টি।",
              (n * 2, r // 2, r + 2))


NUMERIC = [
    moles("carbon dioxide", "কার্বন ডাইঅক্সাইড", 88, 44), moles("calcium carbonate", "ক্যালসিয়াম কার্বনেট", 25, 100),
    moles("glucose", "গ্লুকোজ", 45, 180),
    molecules("water", "জল", 36, 18), molecules("methane", "মিথেন", 8, 16),
    molarity(4, 40, 250, "sodium hydroxide", "সোডিয়াম হাইড্রক্সাইড"), molarity(5.85, 58.5, 500, "sodium chloride", "সোডিয়াম ক্লোরাইড"),
    molarity(9.8, 98, 200, "sulphuric acid", "সালফিউরিক অ্যাসিড"),
    dilution(2, 50, 500), dilution(0.5, 100, 250), dilution(6, 25, 300),
    molality(18, 180, 0.5), molality(90, 180, 2),
    titration(0.1, 25, 2, 0.1), titration(0.2, 20, 1, 0.1), titration(0.05, 40, 2, 0.2),
    limiting(3), limiting(4),
    percent_mass("carbon", "কার্বন", 12, 44, "CO₂"), percent_mass("nitrogen", "নাইট্রোজেন", 28, 60, "urea, CO(NH₂)₂"),
    percent_mass("oxygen", "অক্সিজেন", 48, 100, "CaCO₃"),
    stp_volume(32, 16, "methane", "মিথেন"), stp_volume(11, 44, "carbon dioxide", "কার্বন ডাইঅক্সাইড"),
    stp_volume(7, 28, "nitrogen", "নাইট্রোজেন"),
    graham(2, 32, "hydrogen", "হাইড্রোজেন", "oxygen", "অক্সিজেন"), graham(16, 64, "methane", "মিথেন", "sulphur dioxide", "সালফার ডাইঅক্সাইড"),
    graham(4, 16, "helium", "হিলিয়াম", "methane", "মিথেন"),
    partial("0.25", 0.25, 4), partial("0.6", 0.6, 5),
    boiling(0.52, 0.5, 1, "glucose", "গ্লুকোজ"), boiling(0.52, 0.1, 2, "sodium chloride", "সোডিয়াম ক্লোরাইড"),
    freezing(0.2, 1, "urea", "ইউরিয়া"), freezing(0.1, 3, "calcium chloride", "ক্যালসিয়াম ক্লোরাইড"),
    osmotic(0.1, 300), osmotic(0.2, 310),
    raoult(760, 0.1), raoult(30, 0.2),
    ph_strong("0.01 M", 2, "hydrochloric acid", "হাইড্রোক্লোরিক অ্যাসিড", False),
    ph_strong("0.001 M", 3, "sodium hydroxide", "সোডিয়াম হাইড্রক্সাইড", True),
    ph_strong("0.0001 M", 4, "nitric acid", "নাইট্রিক অ্যাসিড", False),
    ph_strong("0.01 M", 2, "potassium hydroxide", "পটাশিয়াম হাইড্রক্সাইড", True),
    ph_weak(5, 1), ph_weak(6, 2), ph_weak(4, 2),
    buffer(4.74, "10", 10), buffer(4.74, "1", 1), buffer(4.74, "0.1", 0.1),
    ksp(10, "silver chloride", "সিলভার ক্লোরাইড"), ksp(8, "barium sulphate", "বেরিয়াম সালফেট"),
    kc(0.5, 0.2, 0.4), kc(0.1, 0.4, 0.8), kc(0.2, 0.2, 0.2),
    bond_energy(436, 243, 432, "Cl-Cl", "Cl-Cl"), bond_energy(436, 193, 366, "Br-Br", "Br-Br"),
    hess(394, 283), hess(393, 285),
    gibbs_t(40, 100), gibbs_t(60, 200), gibbs_t(30, 120),
    first_order_half(0.0693), first_order_half(0.231), first_order_half(0.01386),
    completion(10, 75, 2), completion(20, 87.5, 3), completion(5, 93.75, 4),
    temp_rate(30), temp_rate(40),
    order(2, 4), order(3, 3), order(2, 8),
    ecell("copper", "তামার", 0.34, "zinc", "দস্তার", -0.76), ecell("silver", "রুপোর", 0.80, "copper", "তামার", 0.34),
    ecell("silver", "রুপোর", 0.80, "zinc", "দস্তার", -0.76),
    nernst(1.1, 2, 2), nernst(0.46, 2, 1),
    electrolysis("copper", "তামা (Cu²⁺)", 63.5, 2, 2, 965), electrolysis("silver", "রুপো (Ag⁺)", 108, 1, 1, 9650),
    electrolysis("copper", "তামা (Cu²⁺)", 63.5, 2, 5, 1930),
    gibbs_cell(2, 1.1), gibbs_cell(1, 0.46),
    molar_cond(0.0129, 0.1), molar_cond(0.0025, 0.02),
    spin_moment("Fe³⁺", "Fe³⁺", 5), spin_moment("Cr³⁺", "Cr³⁺", 3), spin_moment("Ni²⁺", "Ni²⁺", 2),
    spin_moment("Cu²⁺", "Cu²⁺", 1), spin_moment("Fe²⁺ (high spin)", "Fe²⁺ (উচ্চ-স্পিন)", 4),
    radial_nodes("4s", 4, 0), radial_nodes("3p", 3, 1), radial_nodes("5d", 5, 2),
    bond_order("O₂", "O₂", 2, "(8 bonding - 4 antibonding) ÷ 2 = 2; its two unpaired π* electrons make it paramagnetic.",
               "(8 বন্ধনী - 4 বন্ধনবিরোধী) ÷ 2 = 2; দুটো অযুগ্ম π* ইলেকট্রন একে অনুচৌম্বক করে।"),
    bond_order("N₂", "N₂", 3, "(10 - 4) ÷ 2 = 3: a triple bond, which is why N₂ is so unreactive.",
               "(10 - 4) ÷ 2 = 3: ত্রিবন্ধন, তাই N₂ এত নিষ্ক্রিয়।"),
    bond_order("the superoxide ion O₂⁻", "সুপারঅক্সাইড আয়ন O₂⁻", 1.5, "One more antibonding electron than O₂: (8 - 5) ÷ 2 = 1.5.",
               "O₂-এর চেয়ে একটা বেশি বন্ধনবিরোধী ইলেকট্রন: (8 - 5) ÷ 2 = 1.5।"),
    bond_order("nitric oxide, NO", "নাইট্রিক অক্সাইড (NO)", 2.5, "15 electrons: (10 - 5) ÷ 2 = 2.5, with one unpaired electron.",
               "15টি ইলেকট্রন: (10 - 5) ÷ 2 = 2.5, একটা অযুগ্ম ইলেকট্রন সহ।"),
    dbe("benzene, C₆H₆", 6, 6), dbe("C₅H₈", 5, 8), dbe("C₄H₈", 4, 8), dbe("naphthalene, C₁₀H₈", 10, 8),
    cell_density(4, 63.5, 361, "face-centred cubic", "মুখকেন্দ্রিক ঘনকাকার"),
    cell_density(2, 56, 287, "body-centred cubic", "দেহকেন্দ্রিক ঘনকাকার"),
    isomers_chiral(2), isomers_chiral(3), isomers_chiral(4),
    moles("ammonia", "অ্যামোনিয়া", 51, 17), molecules("carbon dioxide", "কার্বন ডাইঅক্সাইড", 22, 44),
    molarity(5.6, 56, 500, "potassium hydroxide", "পটাশিয়াম হাইড্রক্সাইড"), dilution(1, 40, 200),
    titration(0.1, 10, 2, 0.05), limiting(2), stp_volume(4, 2, "hydrogen", "হাইড্রোজেন"),
    graham(2, 16, "hydrogen", "হাইড্রোজেন", "methane", "মিথেন"), boiling(0.52, 1, 1, "sucrose", "সুক্রোজ"),
    freezing(0.5, 2, "potassium chloride", "পটাশিয়াম ক্লোরাইড"), osmotic(0.05, 300), raoult(100, 0.05),
    kc(0.3, 0.5, 0.6), gibbs_t(50, 250), first_order_half(0.1386), completion(15, 75, 2),
    ecell("silver", "রুপোর", 0.80, "nickel", "নিকেলের", -0.25),
    electrolysis("aluminium", "অ্যালুমিনিয়াম (Al³⁺)", 27, 3, 10, 2895), temp_rate(20),
]
NUMERIC = [q for q in NUMERIC if q is not None]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    _q("Which shape does VSEPR theory predict for SF₄?", ["See-saw", "Tetrahedral", "Square planar", "Trigonal pyramidal"],
       "Four bonding pairs and one lone pair (sp³d) - the lone pair sits in an equatorial position.",
       "VSEPR তত্ত্ব অনুযায়ী SF₄-এর আকৃতি কী?", ["ঢেঁকি (সি-স)", "চতুস্তলকীয়", "বর্গ-সমতলীয়", "ত্রিকোণী পিরামিডীয়"],
       "চারটি বন্ধন-জোড় আর একটা নিঃসঙ্গ জোড় (sp³d) - নিঃসঙ্গ জোড় নিরক্ষীয় অবস্থানে থাকে।"),
    _q("What is the shape of XeF₄?", ["Square planar", "Tetrahedral", "Octahedral", "See-saw"],
       "Six electron pairs (sp³d²), two of them lone pairs opposite each other, leave the four F atoms in a square.",
       "XeF₄-এর আকৃতি কী?", ["বর্গ-সমতলীয়", "চতুস্তলকীয়", "অষ্টতলকীয়", "ঢেঁকি (সি-স)"],
       "ছয় জোড়া ইলেকট্রন (sp³d²), তার দুটো নিঃসঙ্গ জোড় মুখোমুখি, চারটি F পরমাণু বর্গাকারে থাকে।"),
    _q("What is the hybridisation of the carbon atoms in ethyne (C₂H₂)?", ["sp", "sp²", "sp³", "sp³d"],
       "Each carbon forms two σ bonds in a straight line plus two π bonds, so the molecule is linear.",
       "ইথাইনে (C₂H₂) কার্বন পরমাণুর সংকরায়ণ কী?", ["sp", "sp²", "sp³", "sp³d"],
       "প্রতিটি কার্বন এক সরলরেখায় দুটো σ বন্ধন আর দুটো π বন্ধন গঠন করে, তাই অণুটা রৈখিক।"),
    _q("Why does water have an unusually high boiling point for its small molar mass?", ["Extensive hydrogen bonding between molecules", "Its covalent bonds are very strong", "It is an ionic compound", "Its molecules are linear"],
       "Each H₂O can form up to four hydrogen bonds; breaking them needs far more energy than for H₂S, which boils at -60°C.",
       "ছোট মোলার ভর সত্ত্বেও জলের স্ফুটনাঙ্ক অস্বাভাবিক বেশি কেন?", ["অণুগুলোর মধ্যে ব্যাপক হাইড্রোজেন বন্ধন", "এর সমযোজী বন্ধন খুব শক্ত", "এটা আয়নীয় যৌগ", "এর অণু রৈখিক"],
       "প্রতিটি H₂O চারটি পর্যন্ত হাইড্রোজেন বন্ধন গড়ে; সেগুলো ভাঙতে H₂S-এর চেয়ে অনেক বেশি শক্তি লাগে, যা -60°C-এ ফোটে।"),
    _q("Which molecule has a zero dipole moment despite having polar bonds?", ["CO₂", "H₂O", "NH₃", "SO₂"],
       "CO₂ is linear, so its two C=O dipoles point in opposite directions and cancel.",
       "কোন অণুতে ধ্রুবীয় বন্ধন থাকা সত্ত্বেও দ্বিমেরু-ভ্রামক শূন্য?", ["CO₂", "H₂O", "NH₃", "SO₂"],
       "CO₂ রৈখিক, তাই তার দুটো C=O দ্বিমেরু বিপরীত দিকে মুখ করে কাটাকাটি হয়।"),
    _q("Across a period from left to right, the atomic radius generally…", ["Decreases", "Increases", "Stays the same", "First rises then falls sharply"],
       "Nuclear charge grows while electrons enter the same shell, pulling the shell in.",
       "পর্যায় বরাবর বাঁ থেকে ডানে পারমাণবিক ব্যাসার্ধ সাধারণত…", ["কমে", "বাড়ে", "একই থাকে", "প্রথমে বাড়ে পরে খুব কমে"],
       "নিউক্লীয় আধান বাড়ে অথচ ইলেকট্রন একই কক্ষে ঢোকে, তাই কক্ষটা ভেতরে টান খায়।"),
    _q("Which element has the highest first ionisation energy?", ["Helium", "Fluorine", "Neon", "Hydrogen"],
       "Helium's two electrons sit in the first shell close to the nucleus with no shielding: 2,372 kJ/mol.",
       "কোন মৌলের প্রথম আয়নীভবন শক্তি সবচেয়ে বেশি?", ["হিলিয়াম", "ফ্লুওরিন", "নিয়ন", "হাইড্রোজেন"],
       "হিলিয়ামের দুটো ইলেকট্রন নিউক্লিয়াসের কাছে প্রথম কক্ষে, কোনো আবরণ ছাড়া: 2,372 kJ/mol।"),
    _q("Why is the first ionisation energy of nitrogen higher than that of oxygen?", ["Nitrogen's half-filled 2p subshell is extra stable", "Nitrogen has more protons", "Oxygen is a noble gas", "Nitrogen's atom is larger"],
       "Oxygen's fourth 2p electron is paired and repelled, so it is easier to remove.",
       "নাইট্রোজেনের প্রথম আয়নীভবন শক্তি অক্সিজেনের চেয়ে বেশি কেন?", ["নাইট্রোজেনের অর্ধপূর্ণ 2p উপকক্ষ বিশেষ স্থিতিশীল", "নাইট্রোজেনে প্রোটন বেশি", "অক্সিজেন নিষ্ক্রিয় গ্যাস", "নাইট্রোজেনের পরমাণু বড়"],
       "অক্সিজেনের চতুর্থ 2p ইলেকট্রন জোড়বদ্ধ ও বিকর্ষিত, তাই সরানো সহজ।"),
    _q("Which element is the most electronegative?", ["Fluorine", "Oxygen", "Chlorine", "Nitrogen"],
       "Fluorine tops the Pauling scale at 4.0: small size and high nuclear pull on bonding electrons.",
       "কোন মৌল সবচেয়ে বেশি তড়িৎ-ঋণাত্মক?", ["ফ্লুওরিন", "অক্সিজেন", "ক্লোরিন", "নাইট্রোজেন"],
       "পলিং স্কেলে ফ্লুওরিন 4.0 নিয়ে শীর্ষে: ছোট আকার আর বন্ধন-ইলেকট্রনের উপর জোরালো নিউক্লীয় টান।"),
    _q("Le Chatelier's principle: for N₂ + 3H₂ ⇌ 2NH₃ (exothermic), which change raises the equilibrium yield of ammonia?", ["Increasing the pressure", "Raising the temperature", "Adding a catalyst", "Removing nitrogen"],
       "4 moles of gas become 2, so higher pressure shifts the equilibrium to the right. A catalyst only speeds up the approach.",
       "লা শাতেলিয়ের নীতি: N₂ + 3H₂ ⇌ 2NH₃ (তাপমোচী) বিক্রিয়ায় কোন পরিবর্তন অ্যামোনিয়ার সাম্য-উৎপাদন বাড়ায়?", ["চাপ বাড়ানো", "তাপমাত্রা বাড়ানো", "অনুঘটক যোগ করা", "নাইট্রোজেন সরিয়ে নেওয়া"],
       "4 মোল গ্যাস 2 মোল হয়, তাই বেশি চাপে সাম্য ডানে সরে। অনুঘটক কেবল সাম্যে পৌঁছানো দ্রুত করে।"),
    _q("What does a catalyst change in a reversible reaction?", ["The rates of both forward and backward reactions, not the equilibrium constant", "The equilibrium constant", "The enthalpy change", "The equilibrium position only"],
       "It lowers the activation energy for both directions equally, so equilibrium is reached sooner but sits in the same place.",
       "উভমুখী বিক্রিয়ায় অনুঘটক কী বদলায়?", ["সম্মুখ আর বিপরীত দুই বিক্রিয়ার হার, সাম্য-ধ্রুবক নয়", "সাম্য-ধ্রুবক", "এনথালপির পরিবর্তন", "কেবল সাম্যের অবস্থান"],
       "এটা দুই দিকের সক্রিয়ন-শক্তি সমানভাবে কমায়, তাই সাম্যে আগে পৌঁছায় কিন্তু একই জায়গায় থাকে।"),
    _q("According to Lewis, an acid is a substance that…", ["Accepts an electron pair", "Donates a proton", "Donates an electron pair", "Releases OH⁻ in water"],
       "BF₃ and AlCl₃ are Lewis acids with no protons at all; NH₃ is a Lewis base.",
       "লুইসের মতে অ্যাসিড এমন পদার্থ যা…", ["ইলেকট্রন-জোড় গ্রহণ করে", "প্রোটন দান করে", "ইলেকট্রন-জোড় দান করে", "জলে OH⁻ ছাড়ে"],
       "BF₃ আর AlCl₃ লুইস অ্যাসিড, অথচ কোনো প্রোটনই নেই; NH₃ লুইস ক্ষার।"),
    _q("What is the conjugate base of HCO₃⁻?", ["CO₃²⁻", "H₂CO₃", "CO₂", "OH⁻"],
       "Removing a proton from HCO₃⁻ gives CO₃²⁻; adding one gives its conjugate acid H₂CO₃.",
       "HCO₃⁻-এর অনুবন্ধী ক্ষার কোনটা?", ["CO₃²⁻", "H₂CO₃", "CO₂", "OH⁻"],
       "HCO₃⁻ থেকে একটা প্রোটন সরালে CO₃²⁻; একটা যোগ করলে অনুবন্ধী অ্যাসিড H₂CO₃।"),
    _q("Adding NaCl to a saturated AgCl solution lowers the solubility of AgCl. This is called…", ["The common ion effect", "Hydrolysis", "The buffer action", "Le Chatelier's failure"],
       "Extra Cl⁻ pushes AgCl ⇌ Ag⁺ + Cl⁻ to the left, so less AgCl stays dissolved.",
       "সম্পৃক্ত AgCl দ্রবণে সোডিয়াম ক্লোরাইড যোগ করলে AgCl-এর দ্রাব্যতা কমে। একে বলে…", ["সম-আয়ন প্রভাব", "আর্দ্রবিশ্লেষণ", "বাফার ক্রিয়া", "লা শাতেলিয়েরের ব্যর্থতা"],
       "অতিরিক্ত Cl⁻ AgCl ⇌ Ag⁺ + Cl⁻ সাম্যকে বাঁয়ে ঠেলে, তাই কম AgCl দ্রবীভূত থাকে।"),
    _q("A process is always spontaneous when…", ["ΔH is negative and ΔS is positive", "ΔH is positive and ΔS is negative", "Both ΔH and ΔS are positive", "Both are negative"],
       "Then ΔG = ΔH - TΔS is negative at every temperature.",
       "কোন ক্ষেত্রে একটা প্রক্রিয়া সবসময় স্বতঃস্ফূর্ত?", ["ΔH ঋণাত্মক আর ΔS ধনাত্মক", "ΔH ধনাত্মক আর ΔS ঋণাত্মক", "ΔH আর ΔS দুটোই ধনাত্মক", "দুটোই ঋণাত্মক"],
       "তখন ΔG = ΔH - TΔS সব তাপমাত্রায় ঋণাত্মক।"),
    _q("Which of these is an intensive property?", ["Temperature", "Volume", "Mass", "Enthalpy"],
       "Intensive properties do not depend on the amount of substance; temperature, density and pressure are examples.",
       "এগুলোর মধ্যে কোনটা প্রগাঢ় (ইনটেনসিভ) ধর্ম?", ["তাপমাত্রা", "আয়তন", "ভর", "এনথালপি"],
       "প্রগাঢ় ধর্ম পদার্থের পরিমাণের উপর নির্ভর করে না; তাপমাত্রা, ঘনত্ব আর চাপ এর উদাহরণ।"),
    _q("The half-life of a zero-order reaction…", ["Is proportional to the initial concentration", "Is independent of concentration", "Is inversely proportional to the initial concentration", "Is always 0.693/k"],
       "For zero order, t½ = [A]₀ ÷ 2k; only first-order half-lives are constant.",
       "শূন্য-ক্রম বিক্রিয়ার অর্ধায়ু…", ["প্রাথমিক ঘনমাত্রার সমানুপাতিক", "ঘনমাত্রা-নিরপেক্ষ", "প্রাথমিক ঘনমাত্রার ব্যস্তানুপাতিক", "সবসময় 0.693/k"],
       "শূন্য ক্রমে অর্ধায়ু = [A]₀ ÷ 2k; কেবল প্রথম-ক্রমের অর্ধায়ু স্থির।"),
    _q("What does the Arrhenius equation k = A e^(-Ea/RT) predict?", ["The rate constant rises exponentially as temperature rises", "The rate constant falls as temperature rises", "Activation energy depends on concentration", "Catalysts raise Ea"],
       "A plot of ln k against 1/T is a straight line of slope -Ea/R.",
       "আরহেনিয়াস সমীকরণ k = A e^(-Ea/RT) কী বলে?", ["তাপমাত্রা বাড়লে হার-ধ্রুবক সূচকীয়ভাবে বাড়ে", "তাপমাত্রা বাড়লে হার-ধ্রুবক কমে", "সক্রিয়ন-শক্তি ঘনমাত্রার উপর নির্ভর করে", "অনুঘটক Ea বাড়ায়"],
       "ln k বনাম 1/T লেখচিত্র -Ea/R নতির সরলরেখা।"),
    _q("In a galvanic cell, oxidation takes place at the…", ["Anode, which is the negative electrode", "Cathode", "Salt bridge", "Anode, which is the positive electrode"],
       "Electrons leave the anode through the wire; in an electrolytic cell the anode is positive instead.",
       "গ্যালভানীয় কোষে জারণ ঘটে…", ["অ্যানোডে, যা ঋণাত্মক তড়িদ্দ্বার", "ক্যাথোডে", "লবণ-সেতুতে", "অ্যানোডে, যা ধনাত্মক তড়িদ্দ্বার"],
       "ইলেকট্রন তার দিয়ে অ্যানোড ছেড়ে যায়; তড়িৎবিশ্লেষ্য কোষে বরং অ্যানোড ধনাত্মক।"),
    _q("What is the job of the salt bridge in a Daniell cell?", ["To keep both solutions electrically neutral and complete the circuit", "To supply electrons", "To act as the cathode", "To stop the reaction"],
       "Ions migrate through it; without it charge builds up and the current stops almost at once.",
       "ড্যানিয়েল কোষে লবণ-সেতুর কাজ কী?", ["দুই দ্রবণকে তড়িৎ-নিরপেক্ষ রেখে বর্তনী পূর্ণ করা", "ইলেকট্রন সরবরাহ করা", "ক্যাথোড হিসেবে কাজ করা", "বিক্রিয়া থামানো"],
       "এর মধ্য দিয়ে আয়ন চলে; এটা না থাকলে আধান জমে আর প্রবাহ প্রায় সঙ্গে সঙ্গে থেমে যায়।"),
    _q("How does molar conductivity change when a strong electrolyte solution is diluted?", ["It increases slightly", "It decreases sharply", "It stays exactly constant", "It becomes zero"],
       "Ions are less crowded and move more freely; Kohlrausch extrapolated this to infinite dilution, Λ°m.",
       "তীব্র তড়িৎবিশ্লেষ্যের দ্রবণ পাতলা করলে মোলার পরিবাহিতা কীভাবে বদলায়?", ["সামান্য বাড়ে", "খুব কমে", "ঠিক একই থাকে", "শূন্য হয়ে যায়"],
       "আয়নগুলো কম ঘিঞ্জি হয়ে স্বাধীনভাবে চলে; কোলরাউশ একে অসীম লঘুতা Λ°m পর্যন্ত বাড়িয়ে দেখিয়েছিলেন।"),
    _q("Why is iron galvanised with zinc?", ["Zinc is more reactive and corrodes first, protecting the iron", "Zinc is less reactive than iron", "Zinc makes iron magnetic", "Zinc stops oxygen dissolving in water"],
       "Even when scratched, zinc acts as a sacrificial anode - the same idea protects ship hulls and pipelines.",
       "লোহাকে দস্তা দিয়ে গ্যালভানাইজ করা হয় কেন?", ["দস্তা বেশি সক্রিয়, আগে ক্ষয় হয়ে লোহাকে বাঁচায়", "দস্তা লোহার চেয়ে কম সক্রিয়", "দস্তা লোহাকে চৌম্বক করে", "দস্তা জলে অক্সিজেন গলতে দেয় না"],
       "আঁচড় লাগলেও দস্তা উৎসর্গী অ্যানোড হিসেবে কাজ করে - জাহাজের খোল আর পাইপলাইন একইভাবে রক্ষা করা হয়।"),
    _q("Which set of quantum numbers is NOT allowed?", ["n = 2, l = 2, m = 0", "n = 3, l = 2, m = -2", "n = 1, l = 0, m = 0", "n = 4, l = 3, m = 3"],
       "l can only run from 0 to n - 1, so l = 2 is impossible when n = 2.",
       "কোন কোয়ান্টাম সংখ্যার সেট অনুমোদিত নয়?", ["n = 2, l = 2, m = 0", "n = 3, l = 2, m = -2", "n = 1, l = 0, m = 0", "n = 4, l = 3, m = 3"],
       "l কেবল 0 থেকে n - 1 পর্যন্ত হতে পারে, তাই n = 2 হলে l = 2 অসম্ভব।"),
    _q("Why does chromium have the configuration [Ar] 3d⁵ 4s¹ rather than 3d⁴ 4s²?", ["A half-filled d subshell is extra stable", "4s is higher in energy than 4p", "Chromium is a noble metal", "It breaks Hund's rule"],
       "Exchange energy favours five parallel d electrons; copper's 3d¹⁰ 4s¹ is the same idea.",
       "ক্রোমিয়ামের বিন্যাস 3d⁴ 4s²-এর বদলে [Ar] 3d⁵ 4s¹ কেন?", ["অর্ধপূর্ণ d উপকক্ষ বিশেষ স্থিতিশীল", "4s-এর শক্তি 4p-এর চেয়ে বেশি", "ক্রোমিয়াম মহৎ ধাতু", "এটা হুন্ডের নিয়ম ভাঙে"],
       "বিনিময়-শক্তি পাঁচটা সমান্তরাল d ইলেকট্রনকে সুবিধা দেয়; তামার 3d¹⁰ 4s¹-ও একই কারণে।"),
    _q("What is the coordination number of each ion in a rock-salt (NaCl) crystal?", ["6", "4", "8", "12"],
       "Each Na⁺ is surrounded octahedrally by six Cl⁻, and vice versa; in CsCl it is 8.",
       "শিলা-লবণ (NaCl) কেলাসে প্রতিটি আয়নের সন্নিবেশ-সংখ্যা কত?", ["6", "4", "8", "12"],
       "প্রতিটি Na⁺-কে ছয়টি Cl⁻ অষ্টতলকীয়ভাবে ঘিরে থাকে, আর উল্টোটাও; CsCl-এ এটা 8।"),
    _q("What fraction of space is filled in a face-centred cubic (cubic close-packed) lattice?", ["74%", "68%", "52%", "90%"],
       "fcc and hcp are the densest packings of equal spheres; bcc fills 68% and simple cubic 52%.",
       "মুখকেন্দ্রিক ঘনকাকার (ঘনকীয় ঘন-সজ্জিত) কেলাসে কত শতাংশ জায়গা ভরা থাকে?", ["74%", "68%", "52%", "90%"],
       "সমান গোলকের সবচেয়ে ঘন সজ্জা fcc আর hcp; bcc 68% আর সরল ঘনক 52% ভরায়।"),
    _q("Which alkali metal reacts most violently with water?", ["Caesium", "Lithium", "Sodium", "Potassium"],
       "Reactivity rises down group 1 as the outer electron is held more loosely.",
       "কোন ক্ষারধাতু জলের সঙ্গে সবচেয়ে প্রচণ্ডভাবে বিক্রিয়া করে?", ["সিজিয়াম", "লিথিয়াম", "সোডিয়াম", "পটাশিয়াম"],
       "গ্রুপ 1-এ নিচের দিকে বাইরের ইলেকট্রন আলগাভাবে আবদ্ধ, তাই সক্রিয়তা বাড়ে।"),
    _q("Lithium resembles magnesium in many properties. This is called…", ["A diagonal relationship", "The inert pair effect", "Lanthanide contraction", "Isomorphism"],
       "Similar charge-to-size ratios make Li and Mg (and Be and Al) behave alike across the diagonal.",
       "লিথিয়াম অনেক ধর্মে ম্যাগনেসিয়ামের মতো। একে বলে…", ["কর্ণ-সম্পর্ক", "নিষ্ক্রিয় জোড় প্রভাব", "ল্যান্থানাইড সংকোচন", "সমাকৃতিতা"],
       "সমান আধান-আকার অনুপাতের জন্য Li আর Mg (এবং Be আর Al) কর্ণ বরাবর একই রকম আচরণ করে।"),
    _q("Why is lead more stable in the +2 oxidation state than +4?", ["The inert pair effect: the 6s² electrons resist bonding", "Lead has no d electrons", "Lead is an alkali metal", "Pb⁴⁺ is too small"],
       "Down group 14 the s pair is held more tightly, so PbO₂ is a strong oxidising agent.",
       "সিসা +4-এর চেয়ে +2 জারণ-অবস্থায় বেশি স্থিতিশীল কেন?", ["নিষ্ক্রিয় জোড় প্রভাব: 6s² ইলেকট্রন বন্ধনে অংশ নিতে চায় না", "সিসার কোনো d ইলেকট্রন নেই", "সিসা ক্ষারধাতু", "Pb⁴⁺ খুব ছোট"],
       "গ্রুপ 14-এ নিচের দিকে s জোড় আরও শক্তভাবে আবদ্ধ, তাই PbO₂ শক্তিশালী জারক।"),
    _q("What special bonding holds diborane (B₂H₆) together?", ["Two three-centre two-electron (banana) bonds", "A boron-boron triple bond", "Ionic bonds", "Hydrogen bonds between molecules"],
       "Boron is electron-deficient; two bridging H atoms each share one electron pair between both borons.",
       "ডাইবোরেন (B₂H₆) কোন বিশেষ বন্ধনে আবদ্ধ?", ["দুটো ত্রি-কেন্দ্র দ্বি-ইলেকট্রন (কলা) বন্ধন", "বোরন-বোরন ত্রিবন্ধন", "আয়নীয় বন্ধন", "অণুগুলোর মধ্যে হাইড্রোজেন বন্ধন"],
       "বোরন ইলেকট্রন-ঘাটতিযুক্ত; দুটো সেতু-H পরমাণু প্রতিটি দুই বোরনের মধ্যে এক জোড়া ইলেকট্রন ভাগ করে।"),
    _q("Why are most transition-metal compounds coloured?", ["d-d electron transitions absorb visible light", "They contain unpaired s electrons", "They are all ionic", "They reflect all wavelengths"],
       "Ligands split the d orbitals; electrons jump across the gap, absorbing one colour and showing its complement.",
       "বেশিরভাগ অবস্থান্তর ধাতুর যৌগ রঙিন কেন?", ["d-d ইলেকট্রন স্থানান্তর দৃশ্যমান আলো শোষণ করে", "এতে অযুগ্ম s ইলেকট্রন আছে", "সবই আয়নীয়", "সব তরঙ্গদৈর্ঘ্য প্রতিফলিত করে"],
       "লিগ্যান্ড d কক্ষকগুলোকে ভাগ করে; ইলেকট্রন ফাঁক পেরিয়ে লাফায়, একটা রং শোষণ করে, তার পরিপূরক রং দেখায়।"),
    _q("What causes the lanthanide contraction?", ["Poor shielding by 4f electrons", "Extra stability of 4f⁷", "High electronegativity of lanthanides", "Relativistic expansion"],
       "4f electrons shield the growing nuclear charge badly, so radii shrink - making Zr and Hf almost the same size.",
       "ল্যান্থানাইড সংকোচনের কারণ কী?", ["4f ইলেকট্রনের দুর্বল আবরণ-ক্ষমতা", "4f⁷-এর বাড়তি স্থিতিশীলতা", "ল্যান্থানাইডের উচ্চ তড়িৎ-ঋণাত্মকতা", "আপেক্ষিকতাজনিত প্রসারণ"],
       "4f ইলেকট্রন বাড়তে থাকা নিউক্লীয় আধানকে খারাপভাবে ঢাকে, তাই ব্যাসার্ধ কমে - ফলে Zr আর Hf প্রায় সমান মাপের।"),
    _q("Why is potassium permanganate a strong oxidising agent in acid?", ["Mn goes from +7 to +2, accepting five electrons", "It releases chlorine", "Mn goes from +2 to +7", "It forms hydrogen gas"],
       "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O; the purple colour vanishing marks the titration end point.",
       "অম্লীয় মাধ্যমে পটাশিয়াম পারম্যাঙ্গানেট শক্তিশালী জারক কেন?", ["Mn +7 থেকে +2-এ নামে, পাঁচটা ইলেকট্রন নেয়", "এটা ক্লোরিন ছাড়ে", "Mn +2 থেকে +7-এ ওঠে", "হাইড্রোজেন গ্যাস তৈরি করে"],
       "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O; বেগুনি রং মিলিয়ে যাওয়া টাইট্রেশনের শেষবিন্দু।"),
    _q("What is the oxidation state of iron in K₄[Fe(CN)₆]?", ["+2", "+3", "+4", "+6"],
       "4 x (+1) + x + 6 x (-1) = 0 gives x = +2; the complex is potassium hexacyanoferrate(II).",
       "K₄[Fe(CN)₆]-এ লোহার জারণ-অবস্থা কত?", ["+2", "+3", "+4", "+6"],
       "4 x (+1) + x + 6 x (-1) = 0 থেকে x = +2; জটিলটা পটাশিয়াম হেক্সাসায়ানোফেরেট(II)।"),
    _q("What is the coordination number of cobalt in [Co(en)₃]³⁺ (en = ethylenediamine)?", ["6", "3", "4", "9"],
       "Each en is bidentate, binding through two nitrogen atoms: 3 x 2 = 6.",
       "[Co(en)₃]³⁺-এ (en = ইথিলিনডায়ামিন) কোবাল্টের সন্নিবেশ-সংখ্যা কত?", ["6", "3", "4", "9"],
       "প্রতিটি en দ্বিদন্তী, দুটো নাইট্রোজেন দিয়ে যুক্ত: 3 x 2 = 6।"),
    _q("Which complex shows geometrical (cis-trans) isomerism?", ["[Pt(NH₃)₂Cl₂] (square planar)", "[Ni(CO)₄] (tetrahedral)", "[Co(NH₃)₆]³⁺", "[Fe(CN)₆]⁴⁻"],
       "In square-planar MA₂B₂ the two Cl can be adjacent (cis, the anticancer drug cisplatin) or opposite (trans).",
       "কোন জটিল যৌগ জ্যামিতিক (সিস-ট্রান্স) সমাবয়বতা দেখায়?", ["[Pt(NH₃)₂Cl₂] (বর্গ-সমতলীয়)", "[Ni(CO)₄] (চতুস্তলকীয়)", "[Co(NH₃)₆]³⁺", "[Fe(CN)₆]⁴⁻"],
       "বর্গ-সমতলীয় MA₂B₂-তে দুটো Cl পাশাপাশি (সিস, ক্যান্সার-রোধী ওষুধ সিসপ্ল্যাটিন) বা মুখোমুখি (ট্রান্স) হতে পারে।"),
    _q("In the spectrochemical series, which ligand produces the largest crystal-field splitting?", ["CN⁻", "I⁻", "H₂O", "F⁻"],
       "Strong-field ligands like CN⁻ and CO pair electrons up (low spin); halides are weak-field.",
       "বর্ণালি-রাসায়নিক শ্রেণিতে কোন লিগ্যান্ড সবচেয়ে বেশি কেলাস-ক্ষেত্র বিভাজন ঘটায়?", ["CN⁻", "I⁻", "H₂O", "F⁻"],
       "CN⁻ আর CO-র মতো তীব্র-ক্ষেত্র লিগ্যান্ড ইলেকট্রন জোড় বাঁধায় (নিম্ন-স্পিন); হ্যালাইড দুর্বল-ক্ষেত্র।"),
    _q("Froth flotation is used to concentrate which kind of ore?", ["Sulphide ores", "Oxide ores", "Carbonate ores", "Native metals"],
       "Pine oil wets sulphide particles, which ride up on the froth while earthy gangue sinks.",
       "ফেনা-ভাসমান পদ্ধতি কোন ধরনের আকরিক গাঢ় করতে লাগে?", ["সালফাইড আকরিক", "অক্সাইড আকরিক", "কার্বনেট আকরিক", "মুক্ত ধাতু"],
       "পাইন তেল সালফাইড কণাকে ভেজায়, সেগুলো ফেনায় ভেসে ওঠে আর মাটির খনিজমল ডুবে যায়।"),
    _q("What does an Ellingham diagram show?", ["ΔG° of oxide formation against temperature, to choose a reducing agent", "Melting points of metals", "Electrode potentials", "Rate of corrosion"],
       "A metal whose line lies lower can reduce the oxide of a metal above it; carbon's line falls with temperature.",
       "এলিংহাম চিত্র কী দেখায়?", ["তাপমাত্রার সাপেক্ষে অক্সাইড গঠনের ΔG°, বিজারক বাছতে", "ধাতুর গলনাঙ্ক", "তড়িদ্দ্বার বিভব", "ক্ষয়ের হার"],
       "যে ধাতুর রেখা নিচে, সে উপরের ধাতুর অক্সাইডকে বিজারিত করতে পারে; তাপমাত্রার সঙ্গে কার্বনের রেখা নামে।"),
    _q("Which carbocation is the most stable?", ["Tertiary (CH₃)₃C⁺", "Primary CH₃CH₂⁺", "Methyl CH₃⁺", "Secondary (CH₃)₂CH⁺"],
       "More alkyl groups give more hyperconjugation and +I donation to the positive carbon.",
       "কোন কার্বোক্যাটায়ন সবচেয়ে স্থিতিশীল?", ["তৃতীয়ক (CH₃)₃C⁺", "প্রাথমিক CH₃CH₂⁺", "মিথাইল CH₃⁺", "দ্বিতীয়ক (CH₃)₂CH⁺"],
       "বেশি অ্যালকাইল গ্রুপ মানে ধনাত্মক কার্বনে বেশি অতিসংযুক্তি আর +I দান।"),
    _q("Which acid is the strongest?", ["Trichloroacetic acid", "Acetic acid", "Chloroacetic acid", "Propanoic acid"],
       "Three electron-withdrawing Cl atoms (-I effect) stabilise the carboxylate ion most.",
       "কোন অ্যাসিড সবচেয়ে তীব্র?", ["ট্রাইক্লোরোঅ্যাসিটিক অ্যাসিড", "অ্যাসিটিক অ্যাসিড", "ক্লোরোঅ্যাসিটিক অ্যাসিড", "প্রোপানোয়িক অ্যাসিড"],
       "তিনটি ইলেকট্রন-আকর্ষী Cl পরমাণু (-I প্রভাব) কার্বক্সিলেট আয়নকে সবচেয়ে বেশি স্থিতিশীল করে।"),
    _q("Why is phenol more acidic than ethanol?", ["The phenoxide ion is stabilised by resonance with the ring", "Phenol has more hydrogen atoms", "Ethanol is an aromatic compound", "Phenol is a gas"],
       "The negative charge spreads over the ring's ortho and para carbons; ethoxide has no such delocalisation.",
       "ফেনল ইথানলের চেয়ে বেশি অম্লীয় কেন?", ["ফিনক্সাইড আয়ন বলয়ের সঙ্গে অনুনাদে স্থিতিশীল", "ফেনলে হাইড্রোজেন বেশি", "ইথানল অ্যারোমেটিক যৌগ", "ফেনল গ্যাস"],
       "ঋণাত্মক আধান বলয়ের অর্থো আর প্যারা কার্বনে ছড়িয়ে পড়ে; ইথক্সাইডে এমন বিস্তার নেই।"),
    _q("Which statement describes an SN2 reaction?", ["One step, backside attack, inversion of configuration", "Two steps through a carbocation", "Fastest for tertiary halides", "Gives a racemic mixture"],
       "Rate = k[substrate][nucleophile]; methyl and primary halides react fastest because there is little crowding.",
       "কোন বিবৃতি SN2 বিক্রিয়াকে বোঝায়?", ["এক ধাপ, পেছন দিক থেকে আক্রমণ, বিন্যাসের উল্টে যাওয়া", "কার্বোক্যাটায়নের মধ্য দিয়ে দুই ধাপ", "তৃতীয়ক হ্যালাইডে সবচেয়ে দ্রুত", "রেসিমিক মিশ্রণ দেয়"],
       "হার = k[সাবস্ট্রেট][নিউক্লিওফাইল]; মিথাইল আর প্রাথমিক হ্যালাইড ভিড় কম বলে সবচেয়ে দ্রুত বিক্রিয়া করে।"),
    _q("Tertiary butyl bromide in water mainly reacts by which mechanism?", ["SN1", "SN2", "E2 only", "Free radical substitution"],
       "A stable tertiary carbocation forms first; a polar protic solvent helps it form.",
       "জলে টারশিয়ারি বিউটাইল ব্রোমাইড প্রধানত কোন কৌশলে বিক্রিয়া করে?", ["SN1", "SN2", "কেবল E2", "মুক্ত-মূলক প্রতিস্থাপন"],
       "আগে একটা স্থিতিশীল তৃতীয়ক কার্বোক্যাটায়ন তৈরি হয়; ধ্রুবীয় প্রোটিক দ্রাবক তা তৈরিতে সাহায্য করে।"),
    _q("HBr adds to propene in the presence of a peroxide. Which product forms mainly?", ["1-bromopropane (anti-Markovnikov)", "2-bromopropane", "1,2-dibromopropane", "Propanol"],
       "The peroxide effect (Kharasch) works by a free-radical chain and applies to HBr only.",
       "পারঅক্সাইডের উপস্থিতিতে প্রোপিনে HBr যুক্ত হয়। প্রধানত কোন উৎপাদ তৈরি হয়?", ["1-ব্রোমোপ্রোপেন (মারকোভনিকভ-বিরোধী)", "2-ব্রোমোপ্রোপেন", "1,2-ডাইব্রোমোপ্রোপেন", "প্রোপানল"],
       "পারঅক্সাইড প্রভাব (খারাশ) মুক্ত-মূলক শৃঙ্খলে কাজ করে, আর কেবল HBr-এর ক্ষেত্রে খাটে।"),
    _q("Without a peroxide, HCl adds to propene to give mainly…", ["2-chloropropane", "1-chloropropane", "Propane", "Allyl chloride"],
       "Markovnikov's rule: H goes to the carbon that already has more H, through the more stable secondary carbocation.",
       "পারঅক্সাইড ছাড়া প্রোপিনে HCl যুক্ত হয়ে প্রধানত দেয়…", ["2-ক্লোরোপ্রোপেন", "1-ক্লোরোপ্রোপেন", "প্রোপেন", "অ্যালাইল ক্লোরাইড"],
       "মারকোভনিকভের নিয়ম: H যায় সেই কার্বনে যাতে আগেই বেশি H আছে, বেশি স্থিতিশীল দ্বিতীয়ক কার্বোক্যাটায়নের মাধ্যমে।"),
    _q("Which reagent is used in the Friedel-Crafts alkylation of benzene?", ["An alkyl halide with anhydrous AlCl₃", "Concentrated HNO₃ and H₂SO₄", "Zn-Hg and HCl", "NaOH and I₂"],
       "AlCl₃ pulls the halide away, making a carbocation electrophile that attacks the ring.",
       "বেঞ্জিনের ফ্রিডেল-ক্রাফটস অ্যালকাইলেশনে কোন বিকারক লাগে?", ["অনার্দ্র AlCl₃-সহ অ্যালকাইল হ্যালাইড", "গাঢ় HNO₃ আর H₂SO₄", "Zn-Hg আর HCl", "NaOH আর I₂"],
       "AlCl₃ হ্যালাইডকে টেনে নেয়, একটা কার্বোক্যাটায়ন ইলেকট্রোফাইল তৈরি হয় যা বলয়কে আক্রমণ করে।"),
    _q("Which group directs an incoming electrophile to the meta position of a benzene ring?", ["-NO₂", "-OH", "-CH₃", "-NH₂"],
       "Electron-withdrawing groups deactivate the ring most at ortho and para, leaving meta as the least bad site.",
       "কোন গ্রুপ বেঞ্জিন বলয়ে আগত ইলেকট্রোফাইলকে মেটা অবস্থানে পাঠায়?", ["-NO₂", "-OH", "-CH₃", "-NH₂"],
       "ইলেকট্রন-আকর্ষী গ্রুপ অর্থো আর প্যারায় বলয়কে সবচেয়ে নিষ্ক্রিয় করে, মেটা সবচেয়ে কম খারাপ জায়গা থাকে।"),
    _q("Which compounds undergo the aldol condensation?", ["Aldehydes or ketones with at least one α-hydrogen", "Aldehydes with no α-hydrogen", "Carboxylic acids only", "Alkanes"],
       "A base removes an α-H to make an enolate, which attacks another carbonyl group.",
       "কোন যৌগ অ্যালডল ঘনীভবনে অংশ নেয়?", ["অন্তত একটা α-হাইড্রোজেনযুক্ত অ্যালডিহাইড বা কিটোন", "α-হাইড্রোজেনহীন অ্যালডিহাইড", "কেবল কার্বক্সিলিক অ্যাসিড", "অ্যালকেন"],
       "ক্ষার একটা α-H সরিয়ে এনোলেট তৈরি করে, যা আরেকটা কার্বনিল গ্রুপকে আক্রমণ করে।"),
    _q("Formaldehyde with concentrated NaOH gives methanol and sodium formate. This is the…", ["Cannizzaro reaction", "Aldol condensation", "Wurtz reaction", "Clemmensen reduction"],
       "Aldehydes without α-hydrogen disproportionate: one molecule is oxidised, the other reduced.",
       "গাঢ় NaOH-এর সঙ্গে ফরম্যালডিহাইড মিথানল আর সোডিয়াম ফরমেট দেয়। এটা…", ["ক্যানিজারো বিক্রিয়া", "অ্যালডল ঘনীভবন", "উর্টজ বিক্রিয়া", "ক্লেমেনসেন বিজারণ"],
       "α-হাইড্রোজেনহীন অ্যালডিহাইড অসমঞ্জস বিক্রিয়া করে: একটা অণু জারিত, অন্যটা বিজারিত হয়।"),
    _q("An amide treated with Br₂ and NaOH gives an amine with one carbon fewer. This is the…", ["Hofmann bromamide degradation", "Gabriel synthesis", "Sandmeyer reaction", "Reimer-Tiemann reaction"],
       "RCONH₂ → RNH₂: the carbonyl carbon leaves as carbonate, so the chain shortens by one.",
       "Br₂ আর NaOH দিয়ে একটা অ্যামাইড থেকে একটা কম কার্বনের অ্যামিন পাওয়া যায়। এটা…", ["হফম্যান ব্রোমামাইড অবক্ষয়", "গ্যাব্রিয়েল সংশ্লেষণ", "স্যান্ডমেয়ার বিক্রিয়া", "রাইমার-টাইম্যান বিক্রিয়া"],
       "RCONH₂ → RNH₂: কার্বনিল কার্বন কার্বনেট হয়ে বেরিয়ে যায়, তাই শৃঙ্খল এক কার্বন ছোট হয়।"),
    _q("In the Lucas test, which alcohol gives turbidity immediately?", ["A tertiary alcohol", "A primary alcohol", "Methanol", "A secondary alcohol, only after heating for an hour"],
       "ZnCl₂/HCl forms an insoluble alkyl chloride fastest from the most stable (tertiary) carbocation.",
       "লুকাস পরীক্ষায় কোন অ্যালকোহল সঙ্গে সঙ্গে ঘোলা হয়?", ["তৃতীয়ক অ্যালকোহল", "প্রাথমিক অ্যালকোহল", "মিথানল", "দ্বিতীয়ক অ্যালকোহল, কেবল এক ঘণ্টা গরম করার পর"],
       "ZnCl₂/HCl সবচেয়ে স্থিতিশীল (তৃতীয়ক) কার্বোক্যাটায়ন থেকে সবচেয়ে দ্রুত অদ্রাব্য অ্যালকাইল ক্লোরাইড তৈরি করে।"),
    _q("Which compound gives a silver mirror with Tollens' reagent?", ["Acetaldehyde", "Acetone", "Ethanol", "Acetic acid"],
       "Aldehydes reduce [Ag(NH₃)₂]⁺ to metallic silver; ketones (apart from α-hydroxy ones) do not.",
       "কোন যৌগ টলেন্সের বিকারকের সঙ্গে রুপোর আয়না দেয়?", ["অ্যাসিট্যালডিহাইড", "অ্যাসিটোন", "ইথানল", "অ্যাসিটিক অ্যাসিড"],
       "অ্যালডিহাইড [Ag(NH₃)₂]⁺-কে ধাতব রুপোয় বিজারিত করে; কিটোন (α-হাইড্রক্সি ছাড়া) করে না।"),
    _q("Which compound gives a yellow precipitate in the iodoform test?", ["Acetone", "Methanol", "Benzaldehyde", "Formaldehyde"],
       "Compounds with a CH₃CO- group (or CH₃CH(OH)-) give yellow CHI₃ with I₂ and NaOH.",
       "আয়োডোফর্ম পরীক্ষায় কোন যৌগ হলুদ অধঃক্ষেপ দেয়?", ["অ্যাসিটোন", "মিথানল", "বেঞ্জালডিহাইড", "ফরম্যালডিহাইড"],
       "CH₃CO- (বা CH₃CH(OH)-) গ্রুপযুক্ত যৌগ I₂ আর NaOH-এর সঙ্গে হলুদ CHI₃ দেয়।"),
    _q("A Grignard reagent reacts with formaldehyde, and the product is hydrolysed. What forms?", ["A primary alcohol", "A tertiary alcohol", "A ketone", "A carboxylic acid"],
       "R-MgX adds to H₂C=O giving RCH₂OH; other aldehydes give secondary and ketones tertiary alcohols.",
       "গ্রিনিয়ার বিকারক ফরম্যালডিহাইডের সঙ্গে বিক্রিয়া করে, তারপর উৎপাদ আর্দ্রবিশ্লেষিত হয়। কী তৈরি হয়?", ["প্রাথমিক অ্যালকোহল", "তৃতীয়ক অ্যালকোহল", "কিটোন", "কার্বক্সিলিক অ্যাসিড"],
       "R-MgX, H₂C=O-তে যুক্ত হয়ে RCH₂OH দেয়; অন্য অ্যালডিহাইড দ্বিতীয়ক আর কিটোন তৃতীয়ক অ্যালকোহল দেয়।"),
    _q("Which amine does not react with benzenesulphonyl chloride (Hinsberg test)?", ["A tertiary amine", "A primary amine", "A secondary amine", "Aniline"],
       "Tertiary amines have no N-H to replace; primary give an alkali-soluble product, secondary an insoluble one.",
       "কোন অ্যামিন বেঞ্জিনসালফোনাইল ক্লোরাইডের সঙ্গে বিক্রিয়া করে না (হিন্সবার্গ পরীক্ষা)?", ["তৃতীয়ক অ্যামিন", "প্রাথমিক অ্যামিন", "দ্বিতীয়ক অ্যামিন", "অ্যানিলিন"],
       "তৃতীয়ক অ্যামিনে প্রতিস্থাপনযোগ্য N-H নেই; প্রাথমিক ক্ষারে দ্রাব্য, দ্বিতীয়ক অদ্রাব্য উৎপাদ দেয়।"),
    _q("Which compound is aromatic by Hückel's rule?", ["The cyclopentadienyl anion", "Cyclobutadiene", "Cyclooctatetraene (planar)", "Cyclohexene"],
       "Aromatic rings are planar, fully conjugated and hold 4n + 2 π electrons; C₅H₅⁻ has 6.",
       "হুকেলের নিয়ম অনুযায়ী কোন যৌগ অ্যারোমেটিক?", ["সাইক্লোপেন্টাডাইয়েনাইল অ্যানায়ন", "সাইক্লোবিউটাডাইয়িন", "সাইক্লোঅক্টাটেট্রাইন (সমতলীয়)", "সাইক্লোহেক্সিন"],
       "অ্যারোমেটিক বলয় সমতলীয়, পুরো সংযুগ্মিত আর 4n + 2টি π ইলেকট্রন ধারণ করে; C₅H₅⁻-এ আছে 6টি।"),
    _q("A molecule cannot be superimposed on its mirror image. It is described as…", ["Chiral", "Achiral", "Meso", "Planar"],
       "Like left and right hands; chiral molecules rotate plane-polarised light.",
       "একটা অণুকে তার দর্পণ-প্রতিবিম্বের উপর মেলানো যায় না। একে বলা হয়…", ["কাইরাল", "অ্যাকাইরাল", "মেসো", "সমতলীয়"],
       "ডান আর বাঁ হাতের মতো; কাইরাল অণু সমতল-সমবর্তিত আলোকে ঘোরায়।"),
    _q("Why is meso-tartaric acid optically inactive although it has two chiral centres?", ["An internal plane of symmetry cancels the rotation", "It has no chiral carbon", "It is a racemic mixture", "It does not absorb light"],
       "The two halves rotate light equally in opposite senses within the same molecule.",
       "দুটো কাইরাল কেন্দ্র থাকা সত্ত্বেও মেসো-টারটারিক অ্যাসিড আলোক-নিষ্ক্রিয় কেন?", ["অভ্যন্তরীণ প্রতিসাম্য-তল ঘূর্ণন বাতিল করে", "এতে কোনো কাইরাল কার্বন নেই", "এটা রেসিমিক মিশ্রণ", "এটা আলো শোষণ করে না"],
       "একই অণুর দুই অর্ধ আলোকে সমান পরিমাণে উল্টো দিকে ঘোরায়।"),
    _q("Nylon-6,6 is made from which pair of monomers?", ["Hexamethylenediamine and adipic acid", "Caprolactam only", "Phenol and formaldehyde", "Ethylene glycol and terephthalic acid"],
       "Each monomer has six carbons; they join by condensation, losing water to form amide links.",
       "নাইলন-6,6 কোন দুটো মনোমার থেকে তৈরি?", ["হেক্সামিথিলিনডায়ামিন আর অ্যাডিপিক অ্যাসিড", "কেবল ক্যাপ্রোল্যাকটাম", "ফেনল আর ফরম্যালডিহাইড", "ইথিলিন গ্লাইকল আর টেরেফথ্যালিক অ্যাসিড"],
       "প্রতিটি মনোমারে ছয়টি কার্বন; ঘনীভবনে জল হারিয়ে অ্যামাইড বন্ধনে যুক্ত হয়।"),
    _q("Which polymer is a thermosetting resin?", ["Bakelite", "Polythene", "PVC", "Nylon-6"],
       "Phenol-formaldehyde cross-links into a rigid 3-D network that cannot be remelted.",
       "কোন পলিমার তাপে-কঠিন (থার্মোসেটিং) রেজিন?", ["ব্যাকেলাইট", "পলিথিন", "পিভিসি", "নাইলন-6"],
       "ফেনল-ফরম্যালডিহাইড আড়াআড়ি যুক্ত হয়ে শক্ত ত্রিমাত্রিক জাল গড়ে, যা আর গলানো যায় না।"),
    _q("Natural rubber is a polymer of which monomer?", ["Isoprene (cis-1,4)", "Chloroprene", "Styrene", "Ethylene"],
       "Vulcanisation with sulphur cross-links the chains, making rubber tougher and less sticky.",
       "প্রাকৃতিক রবার কোন মনোমারের পলিমার?", ["আইসোপ্রিন (সিস-1,4)", "ক্লোরোপ্রিন", "স্টাইরিন", "ইথিলিন"],
       "সালফার দিয়ে ভালকানাইজেশন শৃঙ্খলগুলোকে আড়াআড়ি যুক্ত করে, রবারকে শক্ত আর কম আঠালো করে।"),
    _q("What links amino acids in a protein?", ["Peptide (amide) bonds", "Glycosidic bonds", "Phosphodiester bonds", "Ester bonds"],
       "The -COOH of one amino acid condenses with the -NH₂ of the next, releasing water.",
       "প্রোটিনে অ্যামিনো অ্যাসিডগুলোকে কী জুড়ে রাখে?", ["পেপটাইড (অ্যামাইড) বন্ধন", "গ্লাইকোসাইডিক বন্ধন", "ফসফোডাইএস্টার বন্ধন", "এস্টার বন্ধন"],
       "একটা অ্যামিনো অ্যাসিডের -COOH পরেরটার -NH₂-এর সঙ্গে ঘনীভূত হয়, জল বেরিয়ে যায়।"),
    _q("Glucose is a reducing sugar. Which test shows this?", ["It reduces Fehling's solution to red Cu₂O", "It turns starch-iodide blue", "It gives a violet colour with biuret", "It burns with a green flame"],
       "Its open-chain form has a free aldehyde group; sucrose, with no free carbonyl, is non-reducing.",
       "গ্লুকোজ একটা বিজারক শর্করা। কোন পরীক্ষা তা দেখায়?", ["এটা ফেলিং দ্রবণকে লাল Cu₂O-তে বিজারিত করে", "স্টার্চ-আয়োডাইডকে নীল করে", "বাইউরেটের সঙ্গে বেগুনি রং দেয়", "সবুজ শিখায় পোড়ে"],
       "এর খোলা-শৃঙ্খল রূপে মুক্ত অ্যালডিহাইড গ্রুপ আছে; সুক্রোজে মুক্ত কার্বনিল নেই, তাই বিজারক নয়।"),
    _q("Which base is found in RNA but not in DNA?", ["Uracil", "Thymine", "Adenine", "Cytosine"],
       "RNA uses uracil where DNA uses thymine; both pair with adenine.",
       "কোন ক্ষারক RNA-তে আছে কিন্তু DNA-তে নেই?", ["ইউরাসিল", "থায়ামিন", "অ্যাডেনিন", "সাইটোসিন"],
       "DNA যেখানে থায়ামিন ব্যবহার করে, RNA সেখানে ইউরাসিল; দুটোই অ্যাডেনিনের সঙ্গে জোড় বাঁধে।"),
    _q("Which gases are mainly responsible for stratospheric ozone depletion?", ["Chlorofluorocarbons (CFCs)", "Carbon dioxide", "Methane", "Nitrogen"],
       "UV light frees Cl atoms from CFCs; each Cl destroys thousands of O₃ molecules in a catalytic cycle.",
       "স্ট্র্যাটোস্ফিয়ারে ওজোন ক্ষয়ের জন্য প্রধানত কোন গ্যাস দায়ী?", ["ক্লোরোফ্লুরোকার্বন (সিএফসি)", "কার্বন ডাইঅক্সাইড", "মিথেন", "নাইট্রোজেন"],
       "অতিবেগুনি আলো সিএফসি থেকে Cl পরমাণু মুক্ত করে; প্রতিটি Cl অনুঘটন-চক্রে হাজার হাজার O₃ অণু ধ্বংস করে।"),
    _q("A high biochemical oxygen demand (BOD) in river water indicates…", ["Heavy organic pollution", "Very pure water", "High dissolved oxygen", "Hard water"],
       "Microbes use up oxygen decomposing organic waste; clean water has a BOD below about 5 ppm.",
       "নদীর জলে বেশি জৈব-রাসায়নিক অক্সিজেন চাহিদা (বিওডি) কী বোঝায়?", ["ভারী জৈব দূষণ", "খুব বিশুদ্ধ জল", "বেশি দ্রবীভূত অক্সিজেন", "খর জল"],
       "জৈব বর্জ্য পচাতে জীবাণু অক্সিজেন খরচ করে; পরিষ্কার জলের বিওডি প্রায় 5 ppm-এর কম।"),
    _q("Why does a beam of light become visible when passed through a colloid but not a true solution?", ["Colloidal particles scatter light (Tyndall effect)", "Colloids absorb all light", "True solutions are opaque", "Colloids emit light"],
       "Particles of 1-1,000 nm are big enough to scatter visible light; dissolved ions are too small.",
       "কলয়েডের মধ্য দিয়ে আলোকরশ্মি পাঠালে দেখা যায়, প্রকৃত দ্রবণে যায় না কেন?", ["কলয়েড কণা আলো বিক্ষিপ্ত করে (টিন্ডাল প্রভাব)", "কলয়েড সব আলো শোষণ করে", "প্রকৃত দ্রবণ অস্বচ্ছ", "কলয়েড আলো বিকিরণ করে"],
       "1-1,000 nm-এর কণা দৃশ্যমান আলো বিক্ষিপ্ত করার মতো বড়; দ্রবীভূত আয়ন খুব ছোট।"),
    _q("By the Hardy-Schulze rule, which ion coagulates a negative sol (such as As₂S₃) most effectively?", ["Al³⁺", "Na⁺", "Ba²⁺", "Cl⁻"],
       "The opposite-charged ion with the highest charge has the greatest coagulating power.",
       "হার্ডি-শুলজের নিয়ম অনুযায়ী কোন আয়ন একটা ঋণাত্মক সলকে (যেমন As₂S₃) সবচেয়ে কার্যকরভাবে তঞ্চিত করে?", ["Al³⁺", "Na⁺", "Ba²⁺", "Cl⁻"],
       "বিপরীত আধানের যে আয়নের আধান সবচেয়ে বেশি, তার তঞ্চন-ক্ষমতা সবচেয়ে বেশি।"),
    _q("Physical adsorption (physisorption) is…", ["Weak, reversible and decreases as temperature rises", "Strong and irreversible", "Highly specific to one gas", "Increases with temperature always"],
       "It is held by van der Waals forces; chemisorption involves real chemical bonds and needs activation energy.",
       "ভৌত অধিশোষণ…", ["দুর্বল, উভমুখী আর তাপমাত্রা বাড়লে কমে", "শক্তিশালী আর একমুখী", "একটা গ্যাসের জন্য অত্যন্ত নির্দিষ্ট", "তাপমাত্রার সঙ্গে সবসময় বাড়ে"],
       "এটা ভ্যান ডার ওয়ালস বলে আবদ্ধ; রাসায়নিক অধিশোষণে আসল রাসায়নিক বন্ধন থাকে আর সক্রিয়ন-শক্তি লাগে।"),
    _q("Which oxide is amphoteric?", ["Aluminium oxide", "Sodium oxide", "Sulphur trioxide", "Calcium oxide"],
       "Al₂O₃ dissolves in both acids and alkalis, as do ZnO and BeO.",
       "কোন অক্সাইড উভধর্মী?", ["অ্যালুমিনিয়াম অক্সাইড", "সোডিয়াম অক্সাইড", "সালফার ট্রাইঅক্সাইড", "ক্যালসিয়াম অক্সাইড"],
       "Al₂O₃ অ্যাসিড আর ক্ষার দুটোতেই দ্রবীভূত হয়, যেমন ZnO আর BeO।"),
    _q("What causes the temporary hardness of water, and how is it removed?", ["Calcium and magnesium bicarbonates; removed by boiling", "Calcium sulphate; removed by boiling", "Sodium chloride; removed by filtering", "Dissolved oxygen; removed by cooling"],
       "Boiling turns soluble bicarbonates into insoluble carbonates; permanent hardness (sulphates, chlorides) needs ion exchange.",
       "জলের অস্থায়ী খরতার কারণ কী, আর তা কীভাবে দূর করা হয়?", ["ক্যালসিয়াম আর ম্যাগনেসিয়াম বাইকার্বনেট; ফুটিয়ে দূর হয়", "ক্যালসিয়াম সালফেট; ফুটিয়ে দূর হয়", "সোডিয়াম ক্লোরাইড; ছেঁকে দূর হয়", "দ্রবীভূত অক্সিজেন; ঠান্ডা করে দূর হয়"],
       "ফোটালে দ্রাব্য বাইকার্বনেট অদ্রাব্য কার্বনেটে পরিণত হয়; স্থায়ী খরতা (সালফেট, ক্লোরাইড) দূর করতে আয়ন-বিনিময় লাগে।"),
    _q("Which noble gas forms the most compounds?", ["Xenon", "Helium", "Neon", "Argon"],
       "Xenon's large, loosely held outer electrons let it bond with fluorine and oxygen (XeF₂, XeF₄, XeO₃).",
       "কোন নিষ্ক্রিয় গ্যাস সবচেয়ে বেশি যৌগ তৈরি করে?", ["জেনন", "হিলিয়াম", "নিয়ন", "আর্গন"],
       "জেননের বড়, আলগাভাবে আবদ্ধ বাইরের ইলেকট্রন একে ফ্লুওরিন আর অক্সিজেনের সঙ্গে বন্ধন গড়তে দেয় (XeF₂, XeF₄, XeO₃)।"),
    _q("In the contact process for sulphuric acid, which catalyst oxidises SO₂ to SO₃?", ["Vanadium pentoxide (V₂O₅)", "Iron", "Platinum-free nickel", "Manganese dioxide"],
       "SO₃ is then absorbed in concentrated H₂SO₄ to give oleum, which is diluted to the acid.",
       "সালফিউরিক অ্যাসিড তৈরির স্পর্শ-পদ্ধতিতে কোন অনুঘটক SO₂-কে SO₃-তে জারিত করে?", ["ভ্যানাডিয়াম পেন্টক্সাইড (V₂O₅)", "লোহা", "প্ল্যাটিনাম-মুক্ত নিকেল", "ম্যাঙ্গানিজ ডাইঅক্সাইড"],
       "তারপর SO₃ গাঢ় H₂SO₄-এ শোষিত হয়ে ওলিয়াম হয়, যা পাতলা করে অ্যাসিড পাওয়া যায়।"),
    _q("Which statement about an ideal solution is true?", ["ΔH_mix = 0 and ΔV_mix = 0, and it obeys Raoult's law", "It always forms an azeotrope", "Its components react", "ΔH_mix is large and negative"],
       "Benzene and toluene behave almost ideally because A-B forces equal A-A and B-B forces.",
       "আদর্শ দ্রবণ সম্পর্কে কোন কথা সত্য?", ["ΔH_মিশ্রণ = 0 আর ΔV_মিশ্রণ = 0, আর এটা রাউল্টের সূত্র মানে", "এটা সবসময় অ্যাজিওট্রপ তৈরি করে", "এর উপাদানগুলো বিক্রিয়া করে", "ΔH_মিশ্রণ বড় আর ঋণাত্মক"],
       "বেঞ্জিন আর টলুইন প্রায় আদর্শ আচরণ করে, কারণ A-B বল A-A আর B-B বলের সমান।"),
    _q("Why does a 0.1 molal NaCl solution freeze lower than a 0.1 molal glucose solution?", ["NaCl dissociates into two ions, doubling the particle count", "NaCl has a higher molar mass", "Glucose raises the freezing point", "NaCl reacts with water"],
       "Colligative properties depend on the number of solute particles; i ≈ 2 for NaCl.",
       "0.1 মোলাল সোডিয়াম ক্লোরাইড দ্রবণ 0.1 মোলাল গ্লুকোজ দ্রবণের চেয়ে নিচে জমে কেন?", ["সোডিয়াম ক্লোরাইড দুটো আয়নে বিয়োজিত হয়ে কণার সংখ্যা দ্বিগুণ করে", "সোডিয়াম ক্লোরাইডের মোলার ভর বেশি", "গ্লুকোজ হিমাঙ্ক বাড়ায়", "সোডিয়াম ক্লোরাইড জলের সঙ্গে বিক্রিয়া করে"],
       "সংখ্যাগত ধর্ম দ্রাব-কণার সংখ্যার উপর নির্ভর করে; সোডিয়াম ক্লোরাইডের i ≈ 2।"),
    _q("What is the IUPAC name of CH₃-CH(CH₃)-CH₂-OH?", ["2-methylpropan-1-ol", "Butan-2-ol", "2-methylpropan-2-ol", "Butan-1-ol"],
       "The longest chain holding -OH has three carbons; the methyl sits on carbon 2, the -OH on carbon 1.",
       "CH₃-CH(CH₃)-CH₂-OH-এর IUPAC নাম কী?", ["2-মিথাইলপ্রোপান-1-অল", "বিউটান-2-অল", "2-মিথাইলপ্রোপান-2-অল", "বিউটান-1-অল"],
       "-OH-যুক্ত দীর্ঘতম শৃঙ্খলে তিনটি কার্বন; মিথাইল কার্বন 2-এ, -OH কার্বন 1-এ।"),
    _q("Which of these molecules shows hydrogen bonding within a single molecule (intramolecular)?", ["o-Nitrophenol", "p-Nitrophenol", "Ethanol", "Water"],
       "In the ortho isomer -OH and -NO₂ are close enough to bond to each other, which lowers its boiling point and makes it steam-volatile.",
       "এগুলোর মধ্যে কোন অণু একই অণুর ভেতরে (অন্তঃআণবিক) হাইড্রোজেন বন্ধন দেখায়?", ["অর্থো-নাইট্রোফেনল", "প্যারা-নাইট্রোফেনল", "ইথানল", "জল"],
       "অর্থো সমাণুতে -OH আর -NO₂ নিজেদের মধ্যে বন্ধন গড়ার মতো কাছে, তাই স্ফুটনাঙ্ক কম আর স্টিম-উদ্বায়ী।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
