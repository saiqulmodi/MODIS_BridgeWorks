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
    _q("Mole fraction of a solute A in a solution is defined as:", ["nₐ / (nₐ + n_solvent)", "nₐ / n_solvent", "mass of A / total mass", "nₐ / Avogadro's number"],
       "Sum of all mole fractions in a solution = 1. Used in Raoult's law calculations.",
       "দ্রবণে দ্রাবক A-এর মোল ভগ্নাংশ:", ["nₐ / (nₐ + n_দ্রাবক)", "nₐ / n_দ্রাবক", "A-এর ভর / মোট ভর", "nₐ / অ্যাভোগাড্রো সংখ্যা"],
       "দ্রবণে সব মোল ভগ্নাংশের যোগফল = 1। রাউল্টের সূত্রে ব্যবহার।"),
    _q("Normality (N) is related to molarity (M) by:", ["N = M × n-factor (valency factor)", "N = M / n", "N = M", "N = M²"],
       "n-factor: acid = H⁺ furnished; base = OH⁻ furnished; oxidising agent = change in oxidation state per molecule.",
       "নর্মালিটি (N) ও মোলারিটি (M)-এর সম্পর্ক:", ["N = M × n-ফ্যাক্টর (যোজ্যতা ফ্যাক্টর)", "N = M / n", "N = M", "N = M²"],
       "n-ফ্যাক্টর: অ্যাসিড = H⁺ প্রদান; ক্ষার = OH⁻ প্রদান; জারক = অণু-প্রতি জারণ সংখ্যার পরিবর্তন।"),
    _q("How many grams of NaOH (M = 40 g/mol) are needed to make 500 mL of a 0.5 M solution?", ["10 g (moles = 0.5 × 0.5 = 0.25 mol; mass = 0.25 × 40 = 10 g)", "20 g", "5 g", "40 g"],
       "n = C × V = 0.5 M × 0.5 L = 0.25 mol; m = 0.25 × 40 = 10 g.",
       "0.5 M NaOH (M = 40 g/mol) 500 mL তৈরিতে কত গ্রাম NaOH লাগবে?", ["10 g (মোল = 0.25; ভর = 10 g)", "20 g", "5 g", "40 g"],
       "n = C × V = 0.5 × 0.5 = 0.25 mol; m = 0.25 × 40 = 10 g।"),
    _q("The van't Hoff factor i for a strong electrolyte like CaCl₂ (complete dissociation) is:", ["3 (Ca²⁺ + 2Cl⁻)", "2", "1", "4"],
       "CaCl₂ → Ca²⁺ + 2Cl⁻ gives 3 ions. Colligative properties are 3× larger than for a non-electrolyte.",
       "CaCl₂ (সম্পূর্ণ বিয়োজন) এর ভ্যান্ট হফ ফ্যাক্টর i:", ["3 (Ca²⁺ + 2Cl⁻)", "2", "1", "4"],
       "CaCl₂ → Ca²⁺ + 2Cl⁻ দেয় 3 আয়ন। সহ-সক্রিয় ধর্ম অ-তড়িৎবিশ্লেষ্যের 3 গুণ।"),
    _q("At equilibrium, the equilibrium constant Kc for A + B ⇌ C + D is:", ["Kc = [C][D]/[A][B] (products over reactants, each at equilibrium concentration)", "Kc = [A][B]/[C][D]", "Kc = [C]+[D]/[A]+[B]", "Kc = [C][D]"],
       "Kc depends only on temperature. Kp = Kc(RT)^Δn where Δn = moles gas product − reactant.",
       "A + B ⇌ C + D বিক্রিয়ায় সাম্যাবস্থায় Kc:", ["Kc = [C][D]/[A][B] (সাম্য ঘনত্বে উৎপাদ/বিক্রিয়ক)", "Kc = [A][B]/[C][D]", "Kc = [C]+[D]/[A]+[B]", "Kc = [C][D]"],
       "Kc শুধু তাপমাত্রার উপর নির্ভর করে। Kp = Kc(RT)^Δn যেখানে Δn = গ্যাস মোলের পার্থক্য।"),
    _q("In the Haber process N₂ + 3H₂ ⇌ 2NH₃, increasing pressure:", ["Shifts equilibrium to the right (fewer moles of gas on right), increasing NH₃ yield", "Shifts left", "Has no effect", "Decreases temperature"],
       "Le Chatelier: 4 moles gas → 2 moles gas; high pressure favours fewer moles.",
       "হেবার প্রক্রিয়া N₂ + 3H₂ ⇌ 2NH₃-এ চাপ বাড়ালে:", ["সাম্য ডানদিকে সরে (ডানে কম গ্যাস মোল), NH₃ বৃদ্ধি", "বামদিকে সরে", "কোনো প্রভাব নেই", "তাপমাত্রা কমে"],
       "লে শাটেলিয়ে: 4 মোল গ্যাস → 2 মোল গ্যাস; উচ্চ চাপ কম মোলকে অনুকূল।"),
    _q("A weak acid HA in water: Ka = [H⁺][A⁻]/[HA]. For a 0.1 M solution of HA with Ka = 10⁻⁵, [H⁺] ≈ ?", ["10⁻³ M (√(Ka × C) = √(10⁻⁵ × 0.1) = √10⁻⁶ = 10⁻³)", "10⁻⁵ M", "0.1 M", "10⁻⁷ M"],
       "[H⁺] = √(Ka·C) ≈ √(10⁻⁵ × 0.1) = 10⁻³ M; pH = 3.",
       "0.1 M দুর্বল অ্যাসিড HA-এ Ka = 10⁻⁵ হলে [H⁺] ≈ ?", ["10⁻³ M (√(Ka × C) = 10⁻³)", "10⁻⁵ M", "0.1 M", "10⁻⁷ M"],
       "[H⁺] = √(Ka·C) ≈ 10⁻³ M; pH = 3।"),
    _q("The solubility product Ksp of AgCl = [Ag⁺][Cl⁻] = 1.8×10⁻¹⁰. Solubility of AgCl in pure water is:", ["√Ksp ≈ 1.34×10⁻⁵ mol/L", "Ksp = 1.8×10⁻¹⁰ mol/L", "Ksp/2 mol/L", "2√Ksp mol/L"],
       "s = √Ksp = √(1.8×10⁻¹⁰) ≈ 1.34×10⁻⁵ M. Very low — AgCl barely dissolves.",
       "AgCl-এর Ksp = [Ag⁺][Cl⁻] = 1.8×10⁻¹⁰। বিশুদ্ধ জলে AgCl-এর দ্রাব্যতা:", ["√Ksp ≈ 1.34×10⁻⁵ mol/L", "Ksp = 1.8×10⁻¹⁰ mol/L", "Ksp/2 mol/L", "2√Ksp mol/L"],
       "s = √Ksp ≈ 1.34×10⁻⁵ M। অত্যন্ত কম — AgCl কমই দ্রবীভূত হয়।"),
    _q("The standard enthalpy of formation ΔH°f of an element in its standard state is:", ["Zero by definition (e.g., C(graphite), H₂(g), O₂(g))", "Positive always", "Equal to its atomisation enthalpy", "The same for all elements"],
       "ΔH°f = 0 for reference states. Enthalpy of formation gives the energy stored in compounds relative to elements.",
       "প্রমাণ অবস্থায় মৌলের গঠন-এনথালপি ΔH°f:", ["সংজ্ঞা অনুযায়ী শূন্য (যেমন C(গ্রাফাইট), H₂(g), O₂(g))", "সবসময় ধনাত্মক", "পারমাণবীকরণ এনথালপির সমান", "সব মৌলের একই"],
       "ΔH°f = 0 নির্দেশ অবস্থার জন্য। গঠন-এনথালপি মৌলের সাপেক্ষে যৌগে সঞ্চিত শক্তি দেয়।"),
    _q("Bond dissociation enthalpy is always:", ["Positive (endothermic) — breaking a bond requires energy", "Negative (exothermic)", "Zero for all bonds", "Depends on the product"],
       "Bond breaking: endothermic (+ΔH). Bond forming: exothermic (−ΔH). Net ΔH_rxn = Σ(bonds broken) − Σ(bonds formed).",
       "বন্ধন বিয়োজন এনথালপি সবসময়:", ["ধনাত্মক (এন্ডোথার্মিক) — বন্ধন ভাঙতে শক্তি লাগে", "ঋণাত্মক (এক্সোথার্মিক)", "সব বন্ধনে শূন্য", "উৎপাদের উপর নির্ভর করে"],
       "বন্ধন ভাঙা: এন্ডোথার্মিক (+ΔH)। বন্ধন তৈরি: এক্সোথার্মিক (−ΔH)।"),
    _q("Entropy (S) is a measure of:", ["Disorder or randomness of a system (S increases in spontaneous irreversible processes)", "Heat stored in a system", "Temperature", "Enthalpy change"],
       "Second law: ΔS_universe > 0 for spontaneous processes. Gases have higher entropy than liquids.",
       "এনট্রপি (S) পরিমাপ করে:", ["ব্যবস্থার বিশৃঙ্খলতা বা এলোমেলোত্ব (স্বতঃস্ফূর্ত অপরিবর্তনীয় প্রক্রিয়ায় S বাড়ে)", "ব্যবস্থায় সঞ্চিত তাপ", "তাপমাত্রা", "এনথালপি পরিবর্তন"],
       "দ্বিতীয় সূত্র: স্বতঃস্ফূর্ত প্রক্রিয়ায় ΔS_মহাবিশ্ব > 0। গ্যাসের এনট্রপি তরলের চেয়ে বেশি।"),
    _q("For a spontaneous process, Gibbs free energy ΔG = ΔH − TΔS must be:", ["Negative (ΔG < 0 means reaction proceeds spontaneously)", "Positive", "Zero", "Equal to ΔH"],
       "ΔG = ΔH − TΔS. If ΔH < 0 and ΔS > 0: always spontaneous. If ΔH > 0 and ΔS < 0: never spontaneous.",
       "স্বতঃস্ফূর্ত প্রক্রিয়ার জন্য গিবস মুক্ত শক্তি ΔG = ΔH − TΔS হতে হবে:", ["ঋণাত্মক (ΔG < 0 মানে বিক্রিয়া স্বতঃস্ফূর্তভাবে এগোয়)", "ধনাত্মক", "শূন্য", "ΔH-এর সমান"],
       "ΔG = ΔH − TΔS। ΔH < 0 ও ΔS > 0: সবসময় স্বতঃস্ফূর্ত। ΔH > 0 ও ΔS < 0: কখনো নয়।"),
    _q("The Arrhenius equation k = A e^(−Ea/RT). Increasing temperature:", ["Increases k (faster reaction) because more molecules have energy ≥ Ea", "Decreases k", "Has no effect on k", "Changes A"],
       "Each 10°C rise roughly doubles rate for many reactions (Ea ≈ 50 kJ/mol).",
       "অ্যারেনিয়াস সমীকরণ k = A e^(−Ea/RT)। তাপমাত্রা বাড়ালে:", ["k বাড়ে (বিক্রিয়া দ্রুত) কারণ বেশি অণুর শক্তি ≥ Ea", "k কমে", "k-তে কোনো প্রভাব নেই", "A পরিবর্তিত হয়"],
       "অনেক বিক্রিয়ায় প্রতি 10°C বৃদ্ধিতে হার প্রায় দ্বিগুণ (Ea ≈ 50 kJ/mol)।"),
    _q("A first-order reaction has half-life t₁/₂ = ln2/k ≈ 0.693/k. If k = 0.0693 min⁻¹, the half-life is:", ["10 min", "1 min", "0.693 min", "100 min"],
       "t₁/₂ = 0.693/0.0693 = 10 min. First-order: t₁/₂ is independent of initial concentration.",
       "k = 0.0693 min⁻¹ সহ প্রথম-ক্রম বিক্রিয়ার অর্ধজীবন:", ["10 min", "1 min", "0.693 min", "100 min"],
       "t₁/₂ = 0.693/0.0693 = 10 min। প্রথম-ক্রমে অর্ধজীবন প্রাথমিক ঘনত্বের উপর নির্ভরশীল নয়।"),
    _q("Electrolysis of dilute H₂SO₄: at the cathode (negative electrode) the product is:", ["H₂(g): 2H⁺ + 2e⁻ → H₂ (reduction)", "O₂(g)", "SO₄²⁻ discharged", "H₂SO₄ concentrated"],
       "At anode: 2H₂O → O₂ + 4H⁺ + 4e⁻. At cathode: H₂ is produced.",
       "পাতলা H₂SO₄-এর তড়িৎ বিশ্লেষণে ক্যাথোডে (ঋণ তড়িৎদ্বার) উৎপাদ:", ["H₂(g): 2H⁺ + 2e⁻ → H₂ (বিজারণ)", "O₂(g)", "SO₄²⁻ নির্গমন", "H₂SO₄ ঘনীভূত"],
       "অ্যানোডে: 2H₂O → O₂ + 4H⁺ + 4e⁻। ক্যাথোডে H₂ উৎপাদিত হয়।"),
    _q("The standard cell potential E°cell for the reaction Zn + Cu²⁺ → Zn²⁺ + Cu is:", ["1.10 V (E°Cu²⁺/Cu = +0.34 V, E°Zn²⁺/Zn = −0.76 V; E°cell = 0.34−(−0.76) = 1.10 V)", "0.76 V", "0.34 V", "−1.10 V"],
       "E°cell = E°cathode − E°anode. Spontaneous cell: E°cell > 0 → ΔG°< 0.",
       "Zn + Cu²⁺ → Zn²⁺ + Cu বিক্রিয়ার প্রমাণ কোষ বিভব E°cell:", ["1.10 V (0.34−(−0.76) = 1.10 V)", "0.76 V", "0.34 V", "−1.10 V"],
       "E°cell = E°ক্যাথোড − E°অ্যানোড। স্বতঃস্ফূর্ত কোষ: E°cell > 0 → ΔG°< 0।"),
    _q("In the periodic table, atomic radius generally decreases across a period because:", ["Increasing nuclear charge pulls electrons closer, while electrons are added to the same shell", "Atomic mass increases", "Number of shells increases", "Electron-electron repulsion increases more"],
       "More protons (+) attract same-shell electrons more. Shielding is roughly constant across a period.",
       "পর্যায় সারণিতে পর্যায় জুড়ে পারমাণবিক ব্যাসার্ধ সাধারণত কমে কারণ:", ["নিউক্লিয়ার চার্জ বাড়লে ইলেকট্রন কাছে টানে, একই কক্ষে ইলেকট্রন যোগ", "পারমাণবিক ভর বাড়ে", "কক্ষের সংখ্যা বাড়ে", "ইলেকট্রন-ইলেকট্রন বিকর্ষণ বেশি বাড়ে"],
       "বেশি প্রোটন (+) একই কক্ষের ইলেকট্রন বেশি আকর্ষণ করে। পর্দাকরণ পর্যায় জুড়ে প্রায় ধ্রুবক।"),
    _q("First ionisation energy generally increases across a period. An exception is the dip from N to O because:", ["O has a paired electron in 2p (repulsion lowers IE₁ compared to N's half-filled 2p)", "O is heavier", "N is more electronegative", "O has more protons"],
       "N: 2p↑2p↑2p↑ — half-filled stable. O: 2p↑↓2p↑2p↑ — paired electron easier to remove.",
       "প্রথম আয়নীকরণ শক্তি পর্যায়ে বাড়ে। N থেকে O-তে হ্রাসের ব্যতিক্রম:", ["O-তে 2p-তে যুগল ইলেকট্রন আছে (N-এর অর্ধ-পূর্ণ 2p-এর তুলনায় বিকর্ষণ IE₁ কমায়)", "O ভারী", "N বেশি তড়িৎ-ঋণাত্মক", "O-তে বেশি প্রোটন"],
       "N: 2p↑↑↑ — অর্ধ-পূর্ণ স্থিতিশীল। O: 2p↑↓↑↑ — যুগল ইলেকট্রন সহজে সরানো যায়।"),
    _q("Diagonal relationship exists between Li and Mg because:", ["Similar ionic size and charge density despite being in different groups and periods", "They are in the same group", "Both are transition metals", "Both dissolve in water similarly"],
       "Li⁺ (76 pm) ≈ Mg²⁺ (72 pm) in effective radius. Both form covalent organometallics.",
       "Li ও Mg-এর মধ্যে তির্যক সম্পর্ক:", ["ভিন্ন গ্রুপ ও পর্যায়ে থাকলেও অনুরূপ আয়নিক আকার ও চার্জ ঘনত্ব", "একই গ্রুপে", "উভয় রূপান্তর ধাতু", "উভয় একইভাবে জলে দ্রবীভূত"],
       "Li⁺ (76 pm) ≈ Mg²⁺ (72 pm)। উভয় সমযোজী অর্গানোমেটালিক তৈরি করে।"),
    _q("The hybridisation of the carbon atom in CO₂ is:", ["sp (linear: two double bonds, no lone pairs on C)", "sp²", "sp³", "dsp²"],
       "sp: linear geometry, two C=O double bonds at 180°. Compare with SO₂ (sp²: bent).",
       "CO₂-তে কার্বন পরমাণুর সংকরণ:", ["sp (রৈখিক: দুটো দ্বিবন্ধন, C-তে লোন পেয়ার নেই)", "sp²", "sp³", "dsp²"],
       "sp: রৈখিক জ্যামিতি, 180°-তে দুটো C=O দ্বিবন্ধন। তুলনা: SO₂ (sp²: বাঁকানো)।"),
    _q("The VSEPR shape of NH₃ is:", ["Trigonal pyramidal (3 bond pairs + 1 lone pair on N)", "Trigonal planar", "Tetrahedral", "Linear"],
       "4 electron pairs (3 bonds + 1 lone pair) give tetrahedral electron geometry but trigonal pyramidal shape; bond angle 107°.",
       "NH₃-এর VSEPR আকৃতি:", ["ত্রিকোণীয় পিরামিডাল (3 বন্ধন যুগল + N-তে 1 লোন পেয়ার)", "ত্রিকোণীয় সমতলীয়", "চতুষ্তলীয়", "রৈখিক"],
       "4 ইলেকট্রন যুগল চতুষ্তলীয় ইলেকট্রন জ্যামিতি কিন্তু ত্রিকোণীয় পিরামিডাল আকৃতি; বন্ধন কোণ 107°।"),
    _q("Which type of solid has the highest melting point, being held together by a 3D covalent network?", ["Covalent/network solid (e.g., diamond, SiO₂ — very hard, high MP)", "Ionic solid", "Metallic solid", "Molecular solid"],
       "Diamond: each C bonds to 4 others → very high MP (~3550°C). Bridge construction tools use diamond drill bits.",
       "3D সমযোজী নেটওয়ার্কে আবদ্ধ কোন ধরনের কঠিনের গলনাঙ্ক সর্বোচ্চ?", ["সমযোজী/নেটওয়ার্ক কঠিন (যেমন হীরা, SiO₂ — অত্যন্ত শক্ত, উচ্চ গলনাঙ্ক)", "আয়নিক কঠিন", "ধাতব কঠিন", "আণবিক কঠিন"],
       "হীরা: প্রতিটি C 4টার সাথে বন্ধন → অত্যন্ত উচ্চ গলনাঙ্ক (~3550°C)। সেতু নির্মাণ সরঞ্জামে হীরার ড্রিল বিট।"),
    _q("The octahedral complex [Co(NH₃)₆]³⁺ has how many d-electrons on Co³⁺?", ["6 (Co atomic number 27: [Ar]3d⁷4s²; Co³⁺ loses 2s+1d → [Ar]3d⁶)", "7", "5", "4"],
       "Co³⁺: 27−3 = 24 electrons → [Ar]3d⁶. NH₃ is a strong field ligand → low spin (all 6 paired).",
       "অষ্টতলীয় জটিল [Co(NH₃)₆]³⁺-এ Co³⁺-এ কয়টি d-ইলেকট্রন?", ["6 (Co পারমাণবিক সংখ্যা 27: [Ar]3d⁷4s²; Co³⁺ → [Ar]3d⁶)", "7", "5", "4"],
       "Co³⁺: 24 ইলেকট্রন → [Ar]3d⁶। NH₃ শক্তিশালী ক্ষেত্র লিগ্যান্ড → নিম্ন-স্পিন (সব 6 যুগল)।"),
    _q("The reaction of ethene (CH₂=CH₂) with HBr follows Markovnikov's rule. The product is:", ["CH₃CHBr (bromine adds to the more substituted carbon)", "BrCH₂CH₂Br", "CH₂=CHBr", "CH₃CH₂OH"],
       "Markovnikov: H adds to C with more H (CH₂), Br adds to the other C → CH₃CHBr (1-bromoethane? No: CH₃CH₂Br).",
       "ইথেন (CH₂=CH₂) + HBr বিক্রিয়ায় মার্কভনিকভ-এর নিয়মে উৎপাদ:", ["CH₃CH₂Br (ব্রোমিন বেশি-প্রতিস্থাপিত কার্বনে)", "BrCH₂CH₂Br", "CH₂=CHBr", "CH₃CH₂OH"],
       "মার্কভনিকভ: H বেশি-H কার্বনে (CH₂), Br অন্যটায় → CH₃CH₂Br।"),
    _q("In SN2 reactions, the rate = k[substrate][nucleophile] because:", ["Both substrate and nucleophile are involved in the rate-determining step (concerted single step)", "Only substrate determines rate", "The reaction goes via a carbocation intermediate", "Rate depends on solvent only"],
       "SN2: backside attack, inversion of configuration (Walden inversion), bimolecular.",
       "SN2 বিক্রিয়ায় হার = k[সাবস্ট্রেট][নিউক্লিওফাইল] কারণ:", ["সাবস্ট্রেট ও নিউক্লিওফাইল উভয় হার-নির্ধারণকারী পদক্ষেপে (একযোগী এক পদক্ষেপ)", "শুধু সাবস্ট্রেট নির্ধারণ করে", "কার্বোক্যাটায়ন মধ্যবর্তী হয়", "শুধু দ্রাবকের উপর"],
       "SN2: পেছনের আক্রমণ, বিন্যাসের উল্টানো (ওয়ালডেন উল্টানো), দ্বিআণবিক।"),
    _q("Lucas test (ZnCl₂/conc. HCl) distinguishes primary, secondary, and tertiary alcohols. Which reacts fastest?", ["Tertiary alcohol (fastest — stable 3° carbocation formed immediately, cloudy at once)", "Primary", "Secondary", "All react at same speed"],
       "3° > 2° > 1° in Lucas test. Primary needs heating or does not react. Tertiary reacts at room temperature instantly.",
       "লুকাস পরীক্ষা (ZnCl₂/conc. HCl) 1°, 2°, 3° অ্যালকোহলের পার্থক্য করে। কোনটা দ্রুততম বিক্রিয়া করে?", ["তৃতীয় অ্যালকোহল (দ্রুততম — স্থিতিশীল 3° কার্বোক্যাটায়ন তাৎক্ষণিক, সঙ্গে সঙ্গে ঘোলা)", "প্রথম", "দ্বিতীয়", "সবগুলো সমান"],
       "3° > 2° > 1° লুকাস পরীক্ষায়। প্রথম-ক্রমে গরম লাগে বা বিক্রিয়া হয় না।"),
    _q("The reaction of an alcohol with acetic acid in the presence of H₂SO₄ to form an ester is called:", ["Fischer esterification (RCO₂H + R'OH ⇌ RCO₂R' + H₂O)", "Saponification", "Transesterification", "Aldol condensation"],
       "Reversible equilibrium — excess of one reactant or removal of water shifts toward ester.",
       "H₂SO₄ উপস্থিতিতে অ্যালকোহল ও অ্যাসিটিক অ্যাসিড বিক্রিয়ায় এস্টার তৈরি:", ["ফিশার এস্টারীকরণ (RCO₂H + R'OH ⇌ RCO₂R' + H₂O)", "সাপোনিফিকেশন", "ট্রান্সএস্টারীকরণ", "অ্যালডোল ঘনীভবন"],
       "উভমুখী সাম্য — এক বিক্রিয়কের আধিক্য বা জল অপসারণ এস্টারের দিকে সরায়।"),
    _q("Aldehydes are more reactive towards nucleophilic addition than ketones because:", ["Aldehyde carbon is less hindered (only one alkyl group) and more electrophilic", "Ketones have no carbonyl group", "Aldehydes are stronger acids", "Ketones have more hydrogen"],
       "HCHO > RCHO > RCOR' in reactivity towards nucleophilic addition.",
       "কিটোনের চেয়ে অ্যালডিহাইড নিউক্লিওফিলিক যোগে বেশি ক্রিয়াশীল কারণ:", ["অ্যালডিহাইড কার্বন কম বাধাগ্রস্ত (শুধু একটা অ্যালকাইল গ্রুপ) এবং বেশি ইলেকট্রোফিলিক", "কিটোনে কার্বনাইল গ্রুপ নেই", "অ্যালডিহাইড শক্তিশালী অ্যাসিড", "কিটোনে বেশি হাইড্রোজেন"],
       "নিউক্লিওফিলিক যোগে ক্রিয়াশীলতা: HCHO > RCHO > RCOR'।"),
    _q("The Cannizzaro reaction is a disproportionation of aldehydes having no α-hydrogen. Under strong base:", ["One molecule is oxidised to acid and another reduced to alcohol", "Both aldehydes become acids", "Both become alcohols", "CO₂ is formed"],
       "Example: 2HCHO + OH⁻ → HCOO⁻ + CH₃OH. HCHO is oxidised (formate) and reduced (methanol).",
       "ক্যানিজারো বিক্রিয়া α-হাইড্রোজেনহীন অ্যালডিহাইডের অনুপাতান্তর। শক্তিশালী ক্ষারে:", ["একটা অণু জারিত হয় অ্যাসিডে, আরেকটা বিজারিত হয় অ্যালকোহলে", "উভয় অ্যাসিড হয়", "উভয় অ্যালকোহল হয়", "CO₂ তৈরি হয়"],
       "উদাহরণ: 2HCHO + OH⁻ → HCOO⁻ + CH₃OH।"),
    _q("Carboxylic acids react with Na₂CO₃ to give:", ["Salt + CO₂ + H₂O (2RCOOH + Na₂CO₃ → 2RCOONa + CO₂ + H₂O)", "Ester only", "Aldehyde", "No reaction"],
       "Stronger acid displaces weaker acid (CO₂ is a weaker acid than RCOOH here).",
       "কার্বক্সিলিক অ্যাসিড Na₂CO₃-এর সাথে বিক্রিয়া করে:", ["লবণ + CO₂ + H₂O", "শুধু এস্টার", "অ্যালডিহাইড", "কোনো বিক্রিয়া নেই"],
       "শক্তিশালী অ্যাসিড দুর্বল অ্যাসিড সরিয়ে দেয় (এখানে RCOOH, CO₂-এর চেয়ে শক্তিশালী)।"),
    _q("Amines are classified as primary, secondary, tertiary based on:", ["The number of alkyl/aryl groups attached to nitrogen (1, 2, or 3)", "Number of carbon atoms", "Number of lone pairs", "Boiling point"],
       "1° R-NH₂, 2° R₂NH, 3° R₃N. Basicity order: 2° > 1° > 3° > NH₃ in water (solvation effects).",
       "অ্যামাইনের প্রথম, দ্বিতীয়, তৃতীয় শ্রেণি বিভাগ:", ["নাইট্রোজেনে সংযুক্ত অ্যালকাইল/অ্যারাইল গ্রুপের সংখ্যায় (1, 2 বা 3)", "কার্বন পরমাণুর সংখ্যায়", "লোন পেয়ারের সংখ্যায়", "স্ফুটনাঙ্কে"],
       "1° R-NH₂, 2° R₂NH, 3° R₃N। ক্ষারকতা: জলে 2° > 1° > 3° > NH₃।"),
    _q("Aniline (C₆H₅NH₂) is less basic than aliphatic amines because:", ["The lone pair on N is delocalised into the benzene ring (less available for protonation)", "Phenyl group is electron-withdrawing by induction", "The nitrogen in aniline is sp² hybridised", "Benzene ring increases mass"],
       "Resonance delocalisation: aniline ↔ C₆H₄=NH₂⁺ structures. Lone pair participates in conjugation.",
       "অ্যানিলিন (C₆H₅NH₂) অ্যালিফ্যাটিক অ্যামাইনের চেয়ে কম ক্ষারিক কারণ:", ["N-এর লোন পেয়ার বেনজিন বলয়ে বিস্থানীকৃত (প্রোটোনেশনের জন্য কম উপলব্ধ)", "ফেনাইল গ্রুপ আবেশে ইলেকট্রন-প্রত্যাহারকারী", "N sp² সংকরিত", "বেনজিন ভর বাড়ায়"],
       "অনুনাদ বিস্থানীকরণ: লোন পেয়ার সংযুগনে অংশ নেয়।"),
    _q("The Hinsberg test uses benzenesulfonyl chloride to distinguish: primary amine (product soluble in NaOH), secondary amine (product insoluble), tertiary amine:", ["Does not react with benzenesulfonyl chloride", "Reacts fastest", "Produces precipitate soluble in HCl", "Gives a yellow product"],
       "1° amine → sulfonamide (has N-H, dissolves in NaOH). 2° → no N-H, insoluble. 3° → no reaction.",
       "হিনসবার্গ পরীক্ষা ব্যবহার করে বেনজিনসালফোনাইল ক্লোরাইড: তৃতীয় অ্যামাইন:", ["বেনজিনসালফোনাইল ক্লোরাইডের সাথে বিক্রিয়া করে না", "সবচেয়ে দ্রুত বিক্রিয়া করে", "HCl-তে দ্রাব্য অধঃক্ষেপ দেয়", "হলুদ উৎপাদ"],
       "1° অ্যামাইন → সালফোনামাইড (N-H আছে, NaOH-তে দ্রবীভূত)। 3° → বিক্রিয়া নেই।"),
    _q("The Diels-Alder reaction forms a 6-membered ring by reaction between:", ["A diene (4π electrons) and a dienophile (2π electrons) — [4+2] cycloaddition", "Two alkenes", "An alkyne and benzene", "A ketone and an amine"],
       "[4+2] cycloaddition: concerted, stereospecific, no catalyst needed. Used to make cyclohexene rings.",
       "ডিলস-আলডার বিক্রিয়ায় 6-সদস্যীয় বলয় তৈরি হয়:", ["ডাইন (4π ইলেকট্রন) ও ডাইনোফাইল (2π ইলেকট্রন)-এর মধ্যে — [4+2] সাইক্লো-সংযোজন", "দুটো অ্যালকিন", "অ্যালকাইন ও বেনজিন", "কিটোন ও অ্যামাইন"],
       "[4+2] সাইক্লো-সংযোজন: একযোগী, স্টেরিও-নির্দিষ্ট, অনুঘটকের প্রয়োজন নেই।"),
    _q("Grignard reagents (RMgX) react with CO₂ and then hydrolysis to give:", ["Carboxylic acids (RCOOH) — used to extend carbon chain by one C", "Alcohols", "Aldehydes", "Esters"],
       "RMgX + CO₂ → RCOOMgX →(H₃O⁺) RCOOH. Key carbon-carbon forming reaction.",
       "গ্রিনিয়ার বিকারক (RMgX) CO₂-এর সাথে বিক্রিয়া করে ও জলবিশ্লেষণে দেয়:", ["কার্বক্সিলিক অ্যাসিড (RCOOH) — কার্বন শৃঙ্খল এক C বাড়াতে", "অ্যালকোহল", "অ্যালডিহাইড", "এস্টার"],
       "RMgX + CO₂ → RCOOMgX →(H₃O⁺) RCOOH। মূল কার্বন-কার্বন গঠন বিক্রিয়া।"),
    _q("Reduction of an aldehyde with NaBH₄ gives:", ["A primary alcohol (RCHO → RCH₂OH)", "A secondary alcohol", "A carboxylic acid", "An ether"],
       "NaBH₄ is a mild reducing agent. LiAlH₄ reduces more substrates including carboxylic acids.",
       "NaBH₄ দিয়ে অ্যালডিহাইডের বিজারণে:", ["প্রথম-ক্রম অ্যালকোহল (RCHO → RCH₂OH)", "দ্বিতীয়-ক্রম অ্যালকোহল", "কার্বক্সিলিক অ্যাসিড", "ইথার"],
       "NaBH₄ মৃদু বিজারক। LiAlH₄ কার্বক্সিলিক অ্যাসিড সহ আরও সাবস্ট্রেট বিজারণ করে।"),
    _q("The Aldol condensation reaction involves:", ["A carbonyl compound with α-hydrogen reacting with itself under base/acid catalyst to give a β-hydroxy carbonyl, then dehydration", "Esterification of two aldehydes", "Oxidation of ketones", "Ring formation from amines"],
       "Aldol: α-carbon acts as nucleophile toward another carbonyl. Important in synthesis of complex carbon chains.",
       "অ্যালডোল ঘনীভবন বিক্রিয়ায়:", ["α-হাইড্রোজেনযুক্ত কার্বনাইল যৌগ ক্ষার/অ্যাসিড অনুঘটকে নিজের সাথে বিক্রিয়া করে β-হাইড্রক্সি কার্বনাইল দেয়", "দুটো অ্যালডিহাইডের এস্টারীকরণ", "কিটোনের জারণ", "অ্যামাইন থেকে বলয় গঠন"],
       "অ্যালডোল: α-কার্বন অন্য কার্বনাইলে নিউক্লিওফাইল হিসেবে কাজ করে।"),
    _q("Glucose (C₆H₁₂O₆) belongs to which class of carbohydrates?", ["Monosaccharide (cannot be hydrolysed to simpler sugars)", "Disaccharide", "Polysaccharide", "Oligosaccharide"],
       "Glucose: aldohexose. Fructose: ketohexose. Both are monosaccharides (C₆H₁₂O₆ isomers).",
       "গ্লুকোজ (C₆H₁₂O₆) কোন শ্রেণির শর্করা?", ["মনোস্যাকারাইড (সরল শর্করায় জলবিশ্লেষণ হয় না)", "ডাইস্যাকারাইড", "পলিস্যাকারাইড", "অলিগোস্যাকারাইড"],
       "গ্লুকোজ: অ্যালডোহেক্সোজ। ফ্রুক্টোজ: কিটোহেক্সোজ। উভয় মনোস্যাকারাইড।"),
    _q("Sucrose is a disaccharide formed by:", ["Glucose + Fructose joined by an α,β-1,2-glycosidic bond (non-reducing disaccharide)", "Glucose + Glucose (maltose)", "Glucose + Galactose (lactose)", "Fructose + Galactose"],
       "Sucrose hydrolysis (inversion) gives glucose + fructose — called invert sugar.",
       "সুক্রোজ ডাইস্যাকারাইড তৈরি হয়:", ["গ্লুকোজ + ফ্রুক্টোজ, α,β-1,2-গ্লাইকোসিডিক বন্ধনে (অ-বিজারক ডাইস্যাকারাইড)", "গ্লুকোজ + গ্লুকোজ (মলটোজ)", "গ্লুকোজ + গ্যালাকটোজ (ল্যাকটোজ)", "ফ্রুক্টোজ + গ্যালাকটোজ"],
       "সুক্রোজ জলবিশ্লেষণ গ্লুকোজ + ফ্রুক্টোজ দেয় — ইনভার্ট সুগার।"),
    _q("The structure of proteins is determined by the sequence of amino acids joined by peptide bonds. The secondary structure (α-helix) is stabilised by:", ["Intrachain hydrogen bonds between C=O and N-H groups", "Disulfide bridges", "Ionic bonds", "Covalent C-C bonds"],
       "α-helix: H-bonds between every 4th residue. β-pleated sheet: H-bonds between adjacent chains.",
       "প্রোটিনের কাঠামো পেপটাইড বন্ধনে সংযুক্ত অ্যামাইনো অ্যাসিডের ক্রম দ্বারা নির্ধারিত। দ্বিতীয় কাঠামো (α-হেলিক্স) স্থিতিশীল:", ["শৃঙ্খল-অভ্যন্তরীণ C=O ও N-H গ্রুপের হাইড্রোজেন বন্ধনে", "ডাইসালফাইড সেতু", "আয়নিক বন্ধন", "সমযোজী C-C বন্ধন"],
       "α-হেলিক্স: প্রতি 4র্থ অবশিষ্টের মধ্যে H-বন্ধন। β-প্লিটেড শিট: সন্নিহিত শৃঙ্খলের মধ্যে।"),
    _q("Addition polymers form without loss of small molecules. An example is:", ["Poly(ethene) from ethene CH₂=CH₂ — free radical chain reaction", "Nylon from diamine + diacid", "Dacron from glycol + terephthalic acid", "Bakelite from phenol + formaldehyde"],
       "Polyethylene (PE) pipes are used in bridge drainage because addition polymer — no by-products, easy to process.",
       "সংযোজন পলিমার ক্ষুদ্র অণু হারানো ছাড়াই তৈরি হয়। উদাহরণ:", ["ইথেন CH₂=CH₂ থেকে পলি(ইথেন) — মুক্তমূলক শৃঙ্খল বিক্রিয়া", "ডাইঅ্যামাইন + ডাইঅ্যাসিড থেকে নাইলন", "গ্লাইকোল + টেরেফথ্যালিক অ্যাসিড থেকে ড্যাক্রন", "ফেনল + ফর্মালডিহাইড থেকে বেকেলাইট"],
       "পলিইথিলিন (PE) পাইপ সেতু নিষ্কাশনে ব্যবহার কারণ সংযোজন পলিমার — কোনো উপজাত নেই।"),
    _q("The liquid crystal state exists between the solid and liquid phases and is characterised by:", ["Ordered molecular arrangement in one direction but fluidity in another (anisotropic liquid)", "Complete disorder like a liquid", "Perfect crystalline order like a solid", "Gaseous properties"],
       "LCD screens in bridge monitoring dashboards use liquid crystal displays.",
       "তরল স্ফটিক অবস্থা কঠিন ও তরলের মধ্যে বিদ্যমান এবং বৈশিষ্ট্য:", ["একদিকে সুশৃঙ্খল আণবিক বিন্যাস কিন্তু অন্যদিকে প্রবাহ (অ্যানিসোট্রপিক তরল)", "তরলের মতো সম্পূর্ণ বিশৃঙ্খলতা", "কঠিনের মতো নিখুঁত স্ফটিক শৃঙ্খলা", "গ্যাসীয় ধর্ম"],
       "সেতু পর্যবেক্ষণ ড্যাশবোর্ডের LCD স্ক্রিন তরল স্ফটিক ডিসপ্লে ব্যবহার করে।"),
    _q("Which gas is produced when steam is passed over red-hot coke (water gas reaction)?", ["CO + H₂ (water gas: C + H₂O → CO + H₂)", "CO₂ only", "CH₄", "H₂S"],
       "C + H₂O (steam) → CO + H₂. Water gas is used as industrial fuel and for hydrogen production.",
       "লাল-গরম কোকের উপর দিয়ে বাষ্প পাঠালে (ওয়াটার গ্যাস বিক্রিয়া) কোন গ্যাস উৎপন্ন হয়?", ["CO + H₂ (ওয়াটার গ্যাস: C + H₂O → CO + H₂)", "শুধু CO₂", "CH₄", "H₂S"],
       "C + H₂O (বাষ্প) → CO + H₂। ওয়াটার গ্যাস শিল্পে জ্বালানি ও হাইড্রোজেন উৎপাদনে ব্যবহার।"),
    _q("Hydrolysis of PCl₅ gives:", ["H₃PO₄ + 5HCl (PCl₅ + 4H₂O → H₃PO₄ + 5HCl)", "POCl₃ only", "PH₃", "P₂O₅"],
       "Partial hydrolysis: PCl₅ + H₂O → POCl₃ + 2HCl. Full hydrolysis → H₃PO₄.",
       "PCl₅-এর জলবিশ্লেষণে:", ["H₃PO₄ + 5HCl (PCl₅ + 4H₂O → H₃PO₄ + 5HCl)", "শুধু POCl₃", "PH₃", "P₂O₅"],
       "আংশিক জলবিশ্লেষণ: PCl₅ + H₂O → POCl₃ + 2HCl। সম্পূর্ণ → H₃PO₄।"),
    _q("The Baeyer-Villiger oxidation converts a ketone to:", ["An ester (cyclic ketones → lactones) using peroxy acids", "A carboxylic acid", "An aldehyde", "An alcohol"],
       "R-CO-R' + RCO₃H → R-CO₂-R'. Migration order: H > tert > sec > phen > prim.",
       "বায়ার-ভিলিগার জারণ কিটোনকে রূপান্তরিত করে:", ["এস্টারে (চক্রীয় কিটোন → ল্যাকটোন) পারক্সি অ্যাসিড ব্যবহার করে", "কার্বক্সিলিক অ্যাসিডে", "অ্যালডিহাইডে", "অ্যালকোহলে"],
       "R-CO-R' + RCO₃H → R-CO₂-R'। মাইগ্রেশন ক্রম: H > তৃতীয় > দ্বিতীয় > ফেনাইল > প্রথম।"),
    _q("Which reagent converts a primary alcohol to an aldehyde without over-oxidising to the carboxylic acid?", ["PCC (pyridinium chlorochromate) in CH₂Cl₂", "KMnO₄ in acidic medium", "Jones reagent (CrO₃/H₂SO₄)", "H₂O₂/Fe²⁺ (Fenton)"],
       "PCC is a mild oxidant that stops at aldehyde. KMnO₄ and Jones over-oxidise to acid.",
       "কোন বিকারক প্রথম-ক্রম অ্যালকোহলকে কার্বক্সিলিক অ্যাসিডে অতি-জারণ ছাড়া অ্যালডিহাইডে রূপান্তর করে?", ["PCC (পাইরিডিনিয়াম ক্লোরোক্রোমেট) CH₂Cl₂-এ", "অ্যাসিডিক KMnO₄", "জোনস বিকারক (CrO₃/H₂SO₄)", "H₂O₂/Fe²⁺ (ফেন্টন)"],
       "PCC মৃদু জারক যা অ্যালডিহাইডে থামে। KMnO₄ ও জোনস অ্যাসিডে অতি-জারণ করে।"),
    _q("The Hofmann rearrangement of a primary amide with Br₂/NaOH gives:", ["A primary amine with one fewer carbon (RCONH₂ → RNH₂)", "Carboxylic acid", "Nitrile", "Secondary amine"],
       "Carbon is lost as CO₂. Hofmann uses Br₂/NaOH; Curtius uses acyl azide; Lossen uses O-acylhydroxamate.",
       "Br₂/NaOH দিয়ে প্রথম-ক্রম অ্যামাইডের হফম্যান পুনর্বিন্যাসে:", ["এক কার্বন কম প্রথম-ক্রম অ্যামাইন (RCONH₂ → RNH₂)", "কার্বক্সিলিক অ্যাসিড", "নাইট্রাইল", "দ্বিতীয়-ক্রম অ্যামাইন"],
       "কার্বন CO₂ হিসেবে হারায়। হফম্যান Br₂/NaOH; কার্টিয়াস অ্যাসাইল অ্যাজাইড ব্যবহার করে।"),
    _q("Chlorobenzene is less reactive than chloroalkane in nucleophilic substitution because:", ["The C-Cl bond has partial double-bond character (resonance into ring), making C less electrophilic", "Benzene is a better leaving group", "Chlorine is a better nucleophile in aromatic systems", "C-Cl bond in benzene is longer"],
       "Benzene ring delocalises lone pair of Cl into ring (resonance contributor). Strong conditions or SNAr needed.",
       "ক্লোরোবেনজিন নিউক্লিওফিলিক প্রতিস্থাপনে ক্লোরোঅ্যালকেনের চেয়ে কম ক্রিয়াশীল:", ["C-Cl বন্ধনে আংশিক দ্বিবন্ধন বৈশিষ্ট্য আছে (বলয়ে অনুনাদ), C কম ইলেকট্রোফিলিক", "বেনজিন ভালো লিভিং গ্রুপ", "ক্লোরিন অ্যারোমেটিক ব্যবস্থায় ভালো নিউক্লিওফাইল", "বেনজিনে C-Cl বন্ধন দীর্ঘ"],
       "বেনজিন বলয় Cl-এর লোন পেয়ার বলয়ে বিস্থানীকৃত করে। SNAr প্রয়োজন।"),
    _q("The reagent used for converting a primary amine to a diazonium salt at 0–5°C is:", ["NaNO₂/HCl (HNO₂ in situ with ArNH₂ → ArN₂⁺Cl⁻)", "Br₂/NaOH", "Conc. H₂SO₄", "PCl₅"],
       "Diazonium salts are versatile intermediates: coupling → azo dyes (used in fabric of bridge site safety vests).",
       "0–5°C-এ প্রথম-ক্রম অ্যামাইনকে ডায়াজোনিয়াম লবণে পরিণত করার বিকারক:", ["NaNO₂/HCl (ঘটনাস্থলে HNO₂, ArNH₂ → ArN₂⁺Cl⁻)", "Br₂/NaOH", "ঘন H₂SO₄", "PCl₅"],
       "ডায়াজোনিয়াম লবণ বহুমুখী মধ্যবর্তী: যুগলকরণ → অ্যাজো রং।"),
    _q("Which statement about enzymes is correct?", ["They are biological catalysts (proteins) that lower activation energy and are highly specific", "They raise activation energy", "They are consumed in the reaction", "They only work at high temperature"],
       "Enzymes: lock-and-key and induced-fit models. Active site binds substrate specifically.",
       "এনজাইম সম্পর্কে কোনটা সঠিক?", ["এগুলো জৈবিক অনুঘটক (প্রোটিন) যা সক্রিয়করণ শক্তি কমায় এবং অত্যন্ত নির্দিষ্ট", "সক্রিয়করণ শক্তি বাড়ায়", "বিক্রিয়ায় ক্ষয় পায়", "শুধু উচ্চ তাপমাত্রায় কাজ করে"],
       "এনজাইম: লক-এন্ড-কি ও ইন্ডিউসড-ফিট মডেল। সক্রিয় স্থান নির্দিষ্টভাবে সাবস্ট্রেট বাঁধে।"),
    _q("The fehling test uses Cu²⁺ ions to detect:", ["Aldehydes (reduce Cu²⁺ to Cu₂O red precipitate) — ketones do not react (except α-hydroxy)", "Ketones only", "Alcohols", "Carboxylic acids"],
       "Fehling's A = CuSO₄, Fehling's B = NaOH + Na₂K-tartrate. Only aliphatic aldehydes react.",
       "ফেলিং পরীক্ষা Cu²⁺ আয়ন ব্যবহার করে শনাক্ত করে:", ["অ্যালডিহাইড (Cu²⁺ কে Cu₂O লাল অধঃক্ষেপে বিজারণ করে) — কিটোন বিক্রিয়া করে না", "শুধু কিটোন", "অ্যালকোহল", "কার্বক্সিলিক অ্যাসিড"],
       "ফেলিং A = CuSO₄, ফেলিং B = NaOH + Na₂K-টার্ট্রেট। শুধু অ্যালিফ্যাটিক অ্যালডিহাইড।"),
    _q("The de-polymerisation of rubber (natural rubber = cis-polyisoprene) by ozonolysis gives:", ["Levulinaldehyde (4-oxopentanal) fragments", "Acetylene", "Benzene", "Ethanol"],
       "Ozonolysis cleaves C=C bonds; the repeating unit C₅H₈ of isoprene gives aldehyde/ketone fragments.",
       "প্রাকৃতিক রাবারের (সিস-পলিআইসোপ্রিন) ওজোনোলাইসিসে ডি-পলিমারাইজেশনে:", ["লেভুলিনালডিহাইড টুকরো", "অ্যাসিটিলিন", "বেনজিন", "ইথানল"],
       "ওজোনোলাইসিস C=C বন্ধন ছাড়ে; আইসোপ্রিনের পুনরাবৃত্তি একক C₅H₈ অ্যালডিহাইড/কিটোন টুকরো দেয়।"),
    _q("The IUPAC name of CH₃-CH=CH-CHO is:", ["But-2-enal", "But-3-enal", "Propenal", "2-butenal"],
       "Chain: 4C aldehyde. Double bond at C2-C3 (from CHO end). Name: but-2-enal (or 2-butenal).",
       "CH₃-CH=CH-CHO-এর IUPAC নাম:", ["বিউট-2-এনাল", "বিউট-3-এনাল", "প্রোপেনাল", "2-বিউটেনাল"],
       "শৃঙ্খল: 4C অ্যালডিহাইড। দ্বিবন্ধন C2-C3-এ (CHO প্রান্ত থেকে)। নাম: বিউট-2-এনাল।"),
    _q("Ozone (O₃) absorbs which type of radiation in the stratosphere?", ["UV-B radiation (280–315 nm) — protecting life from DNA damage", "Visible light", "Infrared", "Radio waves"],
       "CFCs destroy ozone by producing Cl• radicals: Cl + O₃ → ClO + O₂. Each Cl destroys ~100,000 O₃ molecules.",
       "স্ট্র্যাটোস্ফিয়ারে ওজোন (O₃) কোন বিকিরণ শোষণ করে?", ["UV-B বিকিরণ (280–315 nm) — DNA ক্ষতি থেকে জীবন রক্ষা", "দৃশ্যমান আলো", "ইনফ্রারেড", "রেডিও তরঙ্গ"],
       "CFC ওজোন ধ্বংস করে Cl• মূলক উৎপন্ন করে। প্রতিটি Cl ~100,000 O₃ অণু ধ্বংস করে।"),
    _q("The solubility of gases in liquids (Henry's law) states:", ["Solubility ∝ partial pressure of gas above the solution: C = kH × P", "Solubility ∝ temperature", "Solubility is independent of pressure", "Solubility decreases with pressure"],
       "Henry's law: CO₂ in carbonated water is kept under pressure. When opened, CO₂ escapes.",
       "তরলে গ্যাসের দ্রাব্যতার হেনরির সূত্র:", ["দ্রাব্যতা ∝ দ্রবণের উপর গ্যাসের আংশিক চাপ: C = kH × P", "দ্রাব্যতা ∝ তাপমাত্রা", "দ্রাব্যতা চাপ থেকে স্বাধীন", "চাপে দ্রাব্যতা কমে"],
       "হেনরির সূত্র: কার্বনেটেড জলে CO₂ চাপে রাখা। খুললে CO₂ বের হয়।"),
    _q("Coloured transition metal compounds owe their colour mainly to:", ["d-d electronic transitions absorbing visible light (complementary colour observed)", "High molar mass", "Metallic lustre", "Ionic size"],
       "Crystal field splitting energy Δ determines which wavelength is absorbed. Larger Δ → higher energy absorbed → blue-shifted.",
       "রঙিন রূপান্তর ধাতু যৌগের রং প্রধানত:", ["d-d ইলেকট্রনিক রূপান্তর দৃশ্যমান আলো শোষণে (পরিপূরক রং পর্যবেক্ষিত)", "উচ্চ মোলার ভর", "ধাতব দীপ্তি", "আয়নিক আকার"],
       "ক্রিস্টাল ক্ষেত্র বিভাজন শক্তি Δ শোষিত তরঙ্গদৈর্ঘ্য নির্ধারণ করে।"),
    _q("The Werner theory of coordination compounds: the primary valence is:", ["Ionizable — the formal charge on the metal (e.g., +3 for Co³⁺)", "Non-ionizable", "Always zero", "Equal to the coordination number"],
       "Secondary (coordination) valence = coordination number (number of ligands bonded to metal).",
       "ওয়ার্নারের সমন্বয় যৌগের তত্ত্ব: প্রাথমিক যোজ্যতা:", ["আয়নীয় — ধাতুতে আনুষ্ঠানিক আধান (যেমন Co³⁺-এর জন্য +3)", "অ-আয়নীয়", "সবসময় শূন্য", "সমন্বয় সংখ্যার সমান"],
       "গৌণ (সমন্বয়) যোজ্যতা = সমন্বয় সংখ্যা (ধাতুতে বন্ধিত লিগ্যান্ড সংখ্যা)।"),
    _q("The bleaching action of SO₂ is due to:", ["Reduction (SO₂ + 2H → S + 2H₂O — absorbs oxygen from colouring matter)", "Oxidation by SO₂", "Chlorine gas production", "Acidic hydrolysis"],
       "SO₂ bleaching is temporary and reversible (cloth recoils on standing in air).",
       "SO₂-এর বিরঞ্জন ক্রিয়া কারণ:", ["বিজারণ (রঙ থেকে অক্সিজেন শোষণ)", "SO₂ দ্বারা জারণ", "ক্লোরিন গ্যাস উৎপাদন", "অ্যাসিডিক জলবিশ্লেষণ"],
       "SO₂ বিরঞ্জন অস্থায়ী ও বিপরীতমুখী (বাতাসে রাখলে কাপড় পুনরায় রঙ পায়)।"),
    _q("The Dow process manufactures chlorobenzene by:", ["Direct chlorination of benzene with Cl₂ in the presence of FeCl₃ (Lewis acid catalyst)", "Reaction of benzene with HCl", "Chlorination with NaOCl", "Electrophilic addition of Cl₂"],
       "FeCl₃ activates Cl₂: generates Cl⁺ electrophile. Benzene undergoes electrophilic aromatic substitution.",
       "ডাও প্রক্রিয়ায় ক্লোরোবেনজিন তৈরি:", ["FeCl₃ (লুইস অ্যাসিড অনুঘটক) উপস্থিতিতে Cl₂ দিয়ে বেনজিনের সরাসরি ক্লোরিনেশন", "HCl-এর সাথে বেনজিনের বিক্রিয়া", "NaOCl দিয়ে ক্লোরিনেশন", "Cl₂-এর ইলেকট্রোফিলিক সংযোজন"],
       "FeCl₃, Cl₂ সক্রিয় করে: Cl⁺ ইলেকট্রোফাইল তৈরি। বেনজিন ইলেকট্রোফিলিক অ্যারোমেটিক প্রতিস্থাপন করে।"),
    _q("Starch gives a blue-black colour with iodine because:", ["Iodine molecules fit into the helical coil of amylose (starch component), forming a charge-transfer complex", "Iodine oxidises glucose in starch", "Starch has a blue natural pigment", "Iodine reacts with glycoside bonds"],
       "Amylose helix: inner diameter fits I₂ molecules. Heating destroys the helix → colour disappears.",
       "আয়োডিনে স্টার্চ নীল-কালো রং দেয় কারণ:", ["আয়োডিন অণু অ্যামাইলোজের (স্টার্চ উপাদান) সর্পিল কুণ্ডলীতে ঢোকে, চার্জ-স্থানান্তর জটিল তৈরি", "আয়োডিন স্টার্চের গ্লুকোজ জারণ করে", "স্টার্চে প্রাকৃতিক নীল রঞ্জক", "আয়োডিন গ্লাইকোসিড বন্ধনে বিক্রিয়া করে"],
       "অ্যামাইলোজ কুণ্ডলী: অভ্যন্তরীণ ব্যাস I₂ অণু ধরে। গরম করলে কুণ্ডলী নষ্ট → রং চলে যায়।"),
    _q("In organic reactions, a carbene (:CH₂) is an example of:", ["An electrophile with only 6 electrons around carbon (can insert into C-H bonds)", "A nucleophile", "A free radical", "An anion"],
       "Carbenes are reactive intermediates with 2 non-bonding electrons. Used in Simmons-Smith cyclopropanation.",
       "জৈব বিক্রিয়ায় কার্বিন (:CH₂) উদাহরণ:", ["ইলেকট্রোফাইল যার কার্বনে মাত্র 6 ইলেকট্রন (C-H বন্ধনে ঢুকতে পারে)", "নিউক্লিওফাইল", "মুক্তমূলক", "অ্যানায়ন"],
       "কার্বিন 2 অ-বন্ধন ইলেকট্রন সহ ক্রিয়াশীল মধ্যবর্তী। সিমনস-স্মিথ সাইক্লোপ্রোপানেশনে ব্যবহার।"),
    _q("Which reaction converts a primary alcohol to an alkyl chloride with retention of configuration at a chiral centre?", ["SOCl₂ in pyridine (front-face attack via chlorosulfite intermediate → retention)", "HCl (inversion)", "PCl₅ (can give inversion)", "Cl₂ (radical)"],
       "SOCl₂/py gives retention because Cl⁻ attacks from the same face as the SOCl group departs.",
       "কোন বিক্রিয়া চিরাল কেন্দ্রে বিন্যাস ধরে রেখে প্রথম-ক্রম অ্যালকোহলকে অ্যালকাইল ক্লোরাইডে পরিণত করে?", ["পিরিডিনে SOCl₂ (ক্লোরোসালফাইট মধ্যবর্তী → ধারণ)", "HCl (উল্টানো)", "PCl₅ (উল্টানো হতে পারে)", "Cl₂ (মূলক)"],
       "SOCl₂/py ধারণ দেয় কারণ Cl⁻ একই দিক থেকে আক্রমণ করে যেখান থেকে SOCl চলে যায়।"),
    _q("Which of the following is the strongest acid?", ["HClO₄ (perchloric acid — the strongest common oxoacid, fully dissociates)", "H₂SO₄", "HNO₃", "HCl"],
       "Strength order for oxyacids increases with number of oxygen atoms and oxidation state of the central atom.",
       "নিচের কোনটি সবচেয়ে শক্তিশালী অ্যাসিড?", ["HClO₄ (পার্ক্লোরিক অ্যাসিড — সবচেয়ে শক্তিশালী সাধারণ অক্সো-অ্যাসিড)", "H₂SO₄", "HNO₃", "HCl"],
       "অক্সি-অ্যাসিডের শক্তি অক্সিজেন পরমাণু সংখ্যা ও কেন্দ্রীয় পরমাণুর জারণ অবস্থার সাথে বাড়ে।"),
    _q("The Aufbau principle states that electrons fill orbitals in order of:", ["Increasing energy: 1s < 2s < 2p < 3s < 3p < 4s < 3d …", "Decreasing energy", "Increasing principal quantum number only", "Random order"],
       "The (n+l) rule: lower (n+l) fills first; for equal (n+l), lower n fills first. So 4s (n+l=4) < 3d (n+l=5).",
       "আউফবাউ নীতি বলে ইলেকট্রন অরবিটাল পূরণ করে:", ["শক্তি বৃদ্ধির ক্রমে: 1s < 2s < 2p < 3s < 3p < 4s < 3d …", "শক্তি হ্রাসের ক্রমে", "শুধু প্রধান কোয়ান্টাম সংখ্যার বৃদ্ধির ক্রমে", "এলোমেলো ক্রমে"],
       "(n+l) নিয়ম: কম (n+l) আগে পূরণ হয়; সমান (n+l)-এ কম n আগে। তাই 4s (n+l=4) < 3d (n+l=5)।"),
    _q("The quantum number that specifies the orientation of an orbital in space is:", ["Magnetic quantum number (mₗ), ranging from −l to +l", "Principal quantum number (n)", "Azimuthal quantum number (l)", "Spin quantum number (ms)"],
       "For p (l=1): mₗ = −1, 0, +1 → three p-orbitals along x, y, z axes.",
       "মহাকাশে অরবিটালের অভিমুখ নির্দিষ্ট করে কোন কোয়ান্টাম সংখ্যা?", ["চৌম্বক কোয়ান্টাম সংখ্যা (mₗ), −l থেকে +l পর্যন্ত", "প্রধান কোয়ান্টাম সংখ্যা (n)", "আজিমুথাল কোয়ান্টাম সংখ্যা (l)", "স্পিন কোয়ান্টাম সংখ্যা (ms)"],
       "p (l=1)-এর জন্য: mₗ = −1, 0, +1 → x, y, z অক্ষ বরাবর তিনটি p-অরবিটাল।"),
    _q("The de Broglie wavelength of an electron is λ = h/mv. For an electron accelerated through 100 V, λ is approximately:", ["0.12 nm (λ = h/√(2meV))", "100 nm", "0.001 nm", "1 μm"],
       "λ = 1.23/√V nm for electrons. At 100 V: λ ≈ 1.23/10 = 0.123 nm — typical atomic spacings.",
       "100 V-এ ত্বরিত ইলেকট্রনের ডি ব্রগলি তরঙ্গদৈর্ঘ্য প্রায়:", ["0.12 nm (λ = h/√(2meV))", "100 nm", "0.001 nm", "1 μm"],
       "ইলেকট্রনের জন্য λ = 1.23/√V nm। 100 V-এ: λ ≈ 0.123 nm — স্বাভাবিক পারমাণবিক ব্যবধান।"),
    _q("Hess's law states that:", ["The total enthalpy change is the same regardless of the route, only depending on initial and final states", "Enthalpy change depends on the path taken", "Exothermic reactions are always spontaneous", "Enthalpy is not a state function"],
       "Hess's law is a consequence of enthalpy being a state function. Used to calculate ΔH for reactions hard to measure directly.",
       "হেসের সূত্র বলে:", ["মোট এনথালপি পরিবর্তন পথ নির্বিশেষে একই, শুধু প্রাথমিক ও চূড়ান্ত অবস্থার উপর নির্ভরশীল", "এনথালপি পরিবর্তন পথের উপর নির্ভরশীল", "তাপোৎপাদী বিক্রিয়া সবসময় স্বতঃস্ফূর্ত", "এনথালপি অবস্থা ফাংশন নয়"],
       "হেসের সূত্র এনথালপি অবস্থা ফাংশন হওয়ার পরিণতি। সরাসরি পরিমাপ কঠিন বিক্রিয়ার ΔH গণনায় ব্যবহার।"),
    _q("For a reaction with Kc = 1×10⁻³⁰ at 298 K, which statement is correct?", ["Reaction barely proceeds; reactants strongly favoured at equilibrium", "Products strongly favoured", "Kc is independent of concentration", "Equilibrium lies to the right"],
       "Kc << 1 means products are in tiny amount. Kc >> 1 means products favoured. Kc = 1 means both sides roughly equal.",
       "298 K-এ Kc = 1×10⁻³⁰ বিক্রিয়ায় কোনটা সঠিক?", ["বিক্রিয়া কমই এগোয়; সাম্যে বিক্রিয়ক অনুকূল", "উৎপাদ অনুকূল", "Kc ঘনত্বের উপর স্বাধীন", "সাম্য ডানদিকে"],
       "Kc << 1 মানে উৎপাদ নগণ্য। Kc >> 1 মানে উৎপাদ অনুকূল। Kc = 1 মানে উভয় পক্ষ মোটামুটি সমান।"),
    _q("The buffer capacity of an acetate buffer (CH₃COOH/CH₃COO⁻) is maximum when:", ["pH = pKa of acetic acid ≈ 4.74 (equal concentrations of acid and conjugate base)", "pH = 7", "pH = 0", "pH = 14"],
       "Henderson-Hasselbalch: pH = pKa + log([A⁻]/[HA]). At pH = pKa: [A⁻] = [HA], maximum buffering.",
       "অ্যাসিটেট বাফারের (CH₃COOH/CH₃COO⁻) বাফার ক্ষমতা সর্বোচ্চ:", ["pH = অ্যাসিটিক অ্যাসিডের pKa ≈ 4.74 (অ্যাসিড ও সংযুগ ক্ষারের সমান ঘনত্ব)", "pH = 7", "pH = 0", "pH = 14"],
       "হেন্ডারসন-হাসেলবালখ: pH = pKa + log([A⁻]/[HA])। pH = pKa-তে: [A⁻] = [HA], সর্বোচ্চ বাফারিং।"),
    _q("Which of the following is a colligative property?", ["Elevation of boiling point (ΔTb = Kb × molality × i)", "Viscosity", "Surface tension", "Optical activity"],
       "Colligative properties depend only on the number of solute particles, not their nature: ΔTf, ΔTb, osmotic pressure, vapour pressure lowering.",
       "নিচের কোনটি সহ-সক্রিয় ধর্ম?", ["স্ফুটনাঙ্ক বৃদ্ধি (ΔTb = Kb × মোললিটি × i)", "সান্দ্রতা", "পৃষ্ঠ টান", "আলোকীয় সক্রিয়তা"],
       "সহ-সক্রিয় ধর্ম দ্রাবক কণার সংখ্যার উপর নির্ভর করে, প্রকৃতির নয়: ΔTf, ΔTb, অসমোটিক চাপ, বাষ্পচাপ হ্রাস।"),
    _q("The rate constant of a zero-order reaction has units:", ["mol L⁻¹ s⁻¹ (rate = k, independent of concentration)", "s⁻¹", "L mol⁻¹ s⁻¹", "L² mol⁻² s⁻¹"],
       "For order n: units of k = (mol L⁻¹)^(1−n) s⁻¹. n=0: mol L⁻¹ s⁻¹; n=1: s⁻¹; n=2: L mol⁻¹ s⁻¹.",
       "শূন্য-ক্রম বিক্রিয়ার হার ধ্রুবকের একক:", ["mol L⁻¹ s⁻¹ (হার = k, ঘনত্ব থেকে স্বাধীন)", "s⁻¹", "L mol⁻¹ s⁻¹", "L² mol⁻² s⁻¹"],
       "n-ক্রম বিক্রিয়ায়: k-এর একক = (mol L⁻¹)^(1−n) s⁻¹। n=0: mol L⁻¹ s⁻¹; n=1: s⁻¹; n=2: L mol⁻¹ s⁻¹।"),
    _q("In the electrolysis of molten NaCl (not aqueous), the product at the anode is:", ["Cl₂(g): 2Cl⁻ → Cl₂ + 2e⁻ (oxidation)", "Na at anode", "O₂", "H₂"],
       "Cathode: Na⁺ + e⁻ → Na (liquid sodium). Anode: Cl₂. This is how sodium is produced industrially (Down's cell).",
       "গলিত NaCl তড়িৎ বিশ্লেষণে অ্যানোডে উৎপাদ:", ["Cl₂(g): 2Cl⁻ → Cl₂ + 2e⁻ (জারণ)", "অ্যানোডে Na", "O₂", "H₂"],
       "ক্যাথোড: Na⁺ + e⁻ → Na (তরল সোডিয়াম)। অ্যানোড: Cl₂। এভাবে শিল্পে সোডিয়াম তৈরি হয় (ডাউনস কোষ)।"),
    _q("The standard Gibbs free energy change is related to equilibrium constant by:", ["ΔG° = −RT ln Kc (spontaneous when Kc > 1)", "ΔG° = RT ln Kc", "ΔG° = −nFE°", "ΔG° = ΔH°"],
       "Both ΔG° = −RT ln Kc and ΔG° = −nFE° are correct; they give the same ΔG° from different measurements.",
       "প্রমাণ গিবস মুক্ত শক্তি পরিবর্তন ও সাম্য ধ্রুবকের সম্পর্ক:", ["ΔG° = −RT ln Kc (Kc > 1 হলে স্বতঃস্ফূর্ত)", "ΔG° = RT ln Kc", "ΔG° = −nFE°", "ΔG° = ΔH°"],
       "ΔG° = −RT ln Kc এবং ΔG° = −nFE° উভয়ই সঠিক; ভিন্ন পরিমাপ থেকে একই ΔG° দেয়।"),
    _q("In a galvanic (voltaic) cell, oxidation occurs at the:", ["Anode (negative terminal in a voltaic cell)", "Cathode", "Salt bridge", "External circuit"],
       "Mnemonic: OIL RIG — Oxidation Is Loss, Reduction Is Gain. Anode = oxidation in BOTH galvanic and electrolytic cells.",
       "গ্যালভানিক (ভোল্টাইক) কোষে জারণ ঘটে:", ["অ্যানোডে (ভোল্টাইক কোষে ঋণ টার্মিনাল)", "ক্যাথোডে", "লবণ সেতুতে", "বাহ্যিক বর্তনীতে"],
       "স্মৃতিসহায়ক: OIL RIG — Oxidation Is Loss, Reduction Is Gain। গ্যালভানিক ও তড়িৎ বিশ্লেষণ উভয় কোষে অ্যানোড = জারণ।"),
    _q("The molecular geometry of XeF₄ is:", ["Square planar (2 lone pairs + 4 bond pairs, octahedral electron geometry)", "Tetrahedral", "See-saw", "Square pyramidal"],
       "VSEPR: 6 electron pairs total (4 bonds + 2 lone pairs). 2 lone pairs go equatorial in octahedral arrangement → square planar.",
       "XeF₄-এর আণবিক জ্যামিতি:", ["বর্গ সমতলীয় (2 লোন পেয়ার + 4 বন্ধন যুগল, অষ্টতলীয় ইলেকট্রন জ্যামিতি)", "চতুষ্তলীয়", "সি-স", "বর্গাকার পিরামিডাল"],
       "VSEPR: 6 ইলেকট্রন যুগল (4 বন্ধন + 2 লোন পেয়ার)। 2 লোন পেয়ার বিষুবীয় অবস্থানে → বর্গ সমতলীয়।"),
    _q("The bond order in N₂ (according to MO theory) is:", ["3 (triple bond: (σ1s)²(σ*1s)²(σ2s)²(σ*2s)²(π2p)⁴(σ2p)² → BO = (10−4)/2 = 3)", "2", "1", "2.5"],
       "High bond order → short bond length (110 pm) → high bond dissociation energy (945 kJ/mol). Most stable diatomic.",
       "MO তত্ত্ব অনুযায়ী N₂-এর বন্ধন ক্রম:", ["3 (ত্রিবন্ধন: BO = (10−4)/2 = 3)", "2", "1", "2.5"],
       "উচ্চ বন্ধন ক্রম → ছোট বন্ধন দৈর্ঘ্য (110 pm) → উচ্চ বন্ধন বিয়োজন শক্তি (945 kJ/mol)।"),
    _q("The difference between physisorption and chemisorption is:", ["Physisorption: weak van der Waals forces, reversible, low heat; chemisorption: covalent/ionic bonds, irreversible, high heat", "Physisorption is irreversible", "Chemisorption occurs at low temperature only", "Physisorption changes the adsorbate chemically"],
       "Chemisorption is specific and monolayer; physisorption is non-specific and multilayer.",
       "ভৌত অধিশোষণ ও রাসায়নিক অধিশোষণের পার্থক্য:", ["ভৌত: দুর্বল ভ্যান্ডার ওয়ালস বল, বিপরীতমুখী, কম তাপ; রাসায়নিক: সমযোজী/আয়নিক বন্ধন, অপরিবর্তনীয়, বেশি তাপ", "ভৌত অধিশোষণ অপরিবর্তনীয়", "রাসায়নিক অধিশোষণ শুধু কম তাপমাত্রায়", "ভৌত অধিশোষণ অধিশোষিত পদার্থ রাসায়নিকভাবে পরিবর্তন করে"],
       "রাসায়নিক অধিশোষণ নির্দিষ্ট ও একস্তরীয়; ভৌত অধিশোষণ অনির্দিষ্ট ও বহুস্তরীয়।"),
    _q("Which of the following elements has the highest electronegativity?", ["Fluorine (F) — electronegativity 3.98 on Pauling scale, highest of all elements", "Oxygen (3.44)", "Chlorine (3.16)", "Nitrogen (3.04)"],
       "Trend: electronegativity increases across period and up a group. F is top-right of periodic table.",
       "কোন মৌলের তড়িৎ-ঋণাত্মকতা সর্বোচ্চ?", ["ফ্লোরিন (F) — পলিং স্কেলে 3.98, সব মৌলের মধ্যে সর্বোচ্চ", "অক্সিজেন (3.44)", "ক্লোরিন (3.16)", "নাইট্রোজেন (3.04)"],
       "প্রবণতা: পর্যায়ে বাম থেকে ডানে ও গ্রুপে নিচ থেকে উপরে তড়িৎ-ঋণাত্মকতা বাড়ে। F পর্যায় সারণির উপর-ডানে।"),
    _q("The chemical formula of rust (iron oxide formed in the presence of water and air) is:", ["Fe₂O₃·xH₂O (hydrated iron(III) oxide)", "FeO", "Fe₃O₄", "Fe(OH)₂"],
       "Rust = hydrated ferric oxide. Fe → Fe²⁺ → Fe³⁺. Cathodic area: O₂ + 2H₂O + 4e⁻ → 4OH⁻.",
       "মরিচার রাসায়নিক সংকেত (জল ও বায়ু উপস্থিতিতে তৈরি আয়রন অক্সাইড):", ["Fe₂O₃·xH₂O (হাইড্রেটেড আয়রন(III) অক্সাইড)", "FeO", "Fe₃O₄", "Fe(OH)₂"],
       "মরিচা = হাইড্রেটেড ফেরিক অক্সাইড। ক্যাথোডিক: O₂ + 2H₂O + 4e⁻ → 4OH⁻।"),
    _q("The Tyndall effect is observed in colloids because:", ["Colloidal particles (1–1000 nm) are large enough to scatter visible light", "Colloidal particles absorb all light", "True solutions also show this effect", "Colloidal particles are smaller than light wavelength"],
       "True solutions (< 1 nm) transmit light without scattering. Use to distinguish colloid from solution.",
       "কলয়েডে টাইন্ডাল প্রভাব দেখা যায় কারণ:", ["কলয়েড কণা (1–1000 nm) দৃশ্যমান আলো বিক্ষেপণ করার মতো বড়", "কলয়েড কণা সব আলো শোষণ করে", "সত্যিকারের দ্রবণও এই প্রভাব দেখায়", "কলয়েড কণা আলোর তরঙ্গদৈর্ঘ্যের চেয়ে ছোট"],
       "সত্যিকারের দ্রবণ (< 1 nm) বিক্ষেপণ ছাড়া আলো প্রেরণ করে। কলয়েড ও দ্রবণ পার্থক্য করতে ব্যবহার।"),
    _q("The Werner coordination number of [Fe(CN)₆]³⁻ is:", ["6 (six CN⁻ ligands each donate one lone pair to Fe³⁺)", "3", "4", "12"],
       "CN⁻ is a strong field ligand → low spin configuration for Fe³⁺ (d⁵). Used in blood-group testing and blue dyes (Prussian blue).",
       "[Fe(CN)₆]³⁻-এর ওয়ার্নার সমন্বয় সংখ্যা:", ["6 (ছয়টি CN⁻ লিগ্যান্ড প্রতিটি Fe³⁺-এ একটি লোন পেয়ার দেয়)", "3", "4", "12"],
       "CN⁻ শক্তিশালী ক্ষেত্র লিগ্যান্ড → Fe³⁺-এর নিম্ন-স্পিন বিন্যাস। প্রুশিয়ান ব্লু রঙে ব্যবহার।"),
    _q("In the reaction 2SO₂ + O₂ ⇌ 2SO₃ (used in H₂SO₄ manufacture), increasing temperature:", ["Decreases yield of SO₃ (exothermic reaction, Le Chatelier shifts left at high T)", "Increases yield", "Has no effect on yield", "Changes Kp and Kc equally"],
       "Contact process: moderate temperature (450°C) + V₂O₅ catalyst — balance between rate and yield.",
       "2SO₂ + O₂ ⇌ 2SO₃ বিক্রিয়ায় (H₂SO₄ উৎপাদনে) তাপমাত্রা বাড়ালে:", ["SO₃ উৎপাদ কমে (তাপোৎপাদী বিক্রিয়া, লে শাটেলিয়ে উচ্চ T-এ বামে সরে)", "উৎপাদ বাড়ে", "উৎপাদে কোনো প্রভাব নেই", "Kp ও Kc সমানভাবে পরিবর্তিত হয়"],
       "সম্পর্ক প্রক্রিয়া: মধ্যম তাপমাত্রা (450°C) + V₂O₅ অনুঘটক — হার ও উৎপাদের ভারসাম্য।"),
    _q("The phenomenon where a substance melts at lower temperature when a foreign particle is present on the surface is related to:", ["Freezing-point depression (ΔTf = Kf × m × i) — colligative property", "Raoult's law", "Henry's law", "Osmosis"],
       "ΔTf = Kf × molality × van't Hoff factor. Used to determine molar mass of unknown solutes.",
       "বাইরের কণার উপস্থিতিতে পদার্থ কম তাপমাত্রায় গলার ঘটনা সম্পর্কিত:", ["হিমাঙ্ক অবনমন (ΔTf = Kf × m × i) — সহ-সক্রিয় ধর্ম", "রাউল্টের সূত্র", "হেনরির সূত্র", "অসমোসিস"],
       "ΔTf = Kf × মোললিটি × ভ্যান্ট হফ ফ্যাক্টর। অজানা দ্রাবকের মোলার ভর নির্ধারণে ব্যবহার।"),
    _q("The unit cell of NaCl structure has how many formula units of NaCl?", ["4 (corner Na: 8×1/8=1; edge Na: 12×1/4=3? Actually: Na: corner+face=4; Cl: edge+body; net 4 NaCl)", "1", "2", "8"],
       "FCC NaCl: Na⁺ at face centres + corners = 4; Cl⁻ at edge centres + body centre = 4. Total: 4 NaCl.",
       "NaCl কাঠামোর একক কোষে কয়টি NaCl সূত্র একক?", ["4 (FCC: Na⁺ = 4; Cl⁻ = 4)", "1", "2", "8"],
       "FCC NaCl: Na⁺ মুখ কেন্দ্র + কোণে = 4; Cl⁻ প্রান্ত কেন্দ্র + দেহ কেন্দ্রে = 4।"),
    _q("Cryoscopic constant Kf for water is 1.86 K·kg/mol. Dissolving 18 g glucose (M=180) in 500 g water lowers freezing point by:", ["0.372 K (m = (18/180)/0.5 = 0.2 mol/kg; ΔTf = 1.86 × 0.2 = 0.372 K)", "0.186 K", "1.86 K", "0.744 K"],
       "m = moles solute / kg solvent = 0.1 mol / 0.5 kg = 0.2 mol/kg; ΔTf = Kf × m = 1.86 × 0.2 = 0.372 K.",
       "Kf (জল) = 1.86 K·kg/mol। 500 g জলে 18 g গ্লুকোজ (M=180) হিমাঙ্ক কমায়:", ["0.372 K (m = 0.2 mol/kg; ΔTf = 1.86 × 0.2 = 0.372 K)", "0.186 K", "1.86 K", "0.744 K"],
       "m = 0.1 mol / 0.5 kg = 0.2 mol/kg; ΔTf = 1.86 × 0.2 = 0.372 K।"),
    _q("The magnetic moment of a d-block complex is μ = √(n(n+2)) BM, where n is the number of unpaired electrons. For a d⁷ high-spin complex:", ["μ = √(3×5) = √15 ≈ 3.87 BM (3 unpaired electrons: t₂g⁵ eg²)", "0 BM (all paired)", "1.73 BM", "5.92 BM"],
       "d⁷ high spin: t₂g⁵ eg² → eg has 2 electrons both unpaired (↑↑), t₂g has 5 electrons: one doubly occupied → 3 unpaired.",
       "d⁷ উচ্চ-স্পিন জটিলের চৌম্বক ভরবেগ:", ["μ = √(3×5) ≈ 3.87 BM (3 অযুগল ইলেকট্রন)", "0 BM (সব যুগল)", "1.73 BM", "5.92 BM"],
       "d⁷ উচ্চ-স্পিন: t₂g⁵ eg² → 3 অযুগল ইলেকট্রন।"),
    _q("The Clemmensen reduction converts a ketone/aldehyde to an alkane using:", ["Zn-Hg amalgam / conc. HCl (acid conditions)", "LiAlH₄", "NaBH₄ / MeOH", "H₂ / Pd"],
       "C=O → CH₂ under acidic conditions. Wolff-Kishner reduction (NH₂NH₂ / KOH) works under basic conditions.",
       "ক্লেমেনসেন বিজারণ কিটোন/অ্যালডিহাইডকে অ্যালকেনে পরিণত করে:", ["Zn-Hg অ্যামালগাম / ঘন HCl (অম্ল পরিস্থিতি)", "LiAlH₄", "NaBH₄ / MeOH", "H₂ / Pd"],
       "C=O → CH₂ অম্ল পরিস্থিতিতে। ওলফ-কিশনার বিজারণ (NH₂NH₂/KOH) ক্ষার পরিস্থিতিতে।"),
    _q("Which test distinguishes an alkene from an alkane?", ["Bromine water test (alkene decolourises Br₂/H₂O; alkane does not under normal conditions)", "Combustion", "Density measurement", "Solubility in water"],
       "Alkene: Br₂ adds across C=C → dibromoalkane (colourless). Alkane: no reaction with Br₂ at room temperature in dark.",
       "অ্যালকিনকে অ্যালকেন থেকে আলাদা করার পরীক্ষা:", ["ব্রোমিন জল পরীক্ষা (অ্যালকিন Br₂/H₂O বর্ণহীন করে; অ্যালকেন সাধারণ পরিস্থিতিতে করে না)", "দহন", "ঘনত্ব পরিমাপ", "জলে দ্রাব্যতা"],
       "অ্যালকিন: Br₂ C=C জুড়ে যোগ → ডাইব্রোমোঅ্যালকেন (বর্ণহীন)। অ্যালকেন: অন্ধকারে Br₂-এর সাথে বিক্রিয়া নেই।"),
    _q("Benzene does not undergo addition reactions readily because:", ["Delocalised π electrons give extra stability (aromatic stabilisation energy ≈ 150 kJ/mol); addition would destroy aromaticity", "Benzene has no π bonds", "C–H bonds are too strong", "Benzene is very reactive"],
       "Electrophilic substitution preserves aromaticity. Addition gives cyclohexadiene — less stable than benzene.",
       "বেনজিন সহজে সংযোজন বিক্রিয়া করে না কারণ:", ["বিস্থানীকৃত π ইলেকট্রন অতিরিক্ত স্থিতিশীলতা দেয় (অ্যারোমেটিক স্থিতিশীলতা শক্তি ≈ 150 kJ/mol); সংযোজনে অ্যারোমেটিকতা নষ্ট হয়", "বেনজিনে π বন্ধন নেই", "C–H বন্ধন অত্যন্ত শক্তিশালী", "বেনজিন অত্যন্ক ক্রিয়াশীল"],
       "ইলেকট্রোফিলিক প্রতিস্থাপন অ্যারোমেটিকতা ধরে রাখে। সংযোজনে সাইক্লোহেক্সাডাইন — বেনজিনের চেয়ে কম স্থিতিশীল।"),
    _q("The Williamson synthesis is used to prepare:", ["Ethers: R–O⁻Na⁺ + R'–X → R–O–R' + NaX (SN2 reaction)", "Alcohols", "Aldehydes", "Carboxylic acids"],
       "Best for unsymmetrical ethers. The alkoxide is the nucleophile; the alkyl halide should be primary (SN2 favoured).",
       "উইলিয়ামসন সংশ্লেষণ তৈরিতে ব্যবহার:", ["ইথার: R–O⁻Na⁺ + R'–X → R–O–R' + NaX (SN2 বিক্রিয়া)", "অ্যালকোহল", "অ্যালডিহাইড", "কার্বক্সিলিক অ্যাসিড"],
       "অসমমিত ইথারের জন্য উত্তম। অ্যালকক্সাইড নিউক্লিওফাইল; অ্যালকাইল হ্যালাইড প্রথম-ক্রম হওয়া উচিত।"),
    _q("The dehydration of an alcohol to an alkene using H₂SO₄ follows:", ["Saytzeff's rule — the more substituted alkene is the major product", "Markovnikov's rule", "Anti-Markovnikov's rule", "Hofmann's rule"],
       "Saytzeff: remove H from the more substituted carbon → more stable alkene. Hofmann rule applies to elimination from ammonium salts.",
       "H₂SO₄ দিয়ে অ্যালকোহলের পানিচ্যুতিতে অ্যালকিন তৈরিতে:", ["সাইটসেভের নিয়ম — অধিক প্রতিস্থাপিত অ্যালকিন প্রধান উৎপাদ", "মার্কভনিকভের নিয়ম", "অ্যান্টি-মার্কভনিকভ নিয়ম", "হফম্যানের নিয়ম"],
       "সাইটসেভ: বেশি প্রতিস্থাপিত কার্বন থেকে H সরানো → অধিক স্থিতিশীল অ্যালকিন।"),
    _q("The Reimer-Tiemann reaction gives:", ["Salicylaldehyde from phenol + CHCl₃/NaOH — introduction of CHO at ortho position", "Benzaldehyde", "Phenol from benzene", "Phenol dimer"],
       "Phenol → salicylaldehyde (2-hydroxybenzaldehyde). Mechanism: dichlorocarbene (:CCl₂) is the intermediate.",
       "রাইমার-টাইমান বিক্রিয়ায় তৈরি হয়:", ["ফেনল + CHCl₃/NaOH থেকে স্যালিসাইলালডিহাইড — অর্থো অবস্থানে CHO প্রবেশ", "বেনজালডিহাইড", "বেনজিন থেকে ফেনল", "ফেনল ডাইমার"],
       "ফেনল → স্যালিসাইলালডিহাইড (2-হাইড্রক্সিবেনজালডিহাইড)। মধ্যবর্তী: ডাইক্লোরোকার্বিন (:CCl₂)।"),
    _q("The Kolbe-Schmitt reaction converts phenol (as sodium phenoxide) to:", ["Salicylic acid (aspirin precursor) using CO₂ under pressure", "Benzoic acid", "Cresol", "Catechol"],
       "C₆H₅ONa + CO₂ (4–7 atm, 125°C) → sodium salicylate → H⁺ → salicylic acid.",
       "কোলবে-শ্মিট বিক্রিয়ায় ফেনল (সোডিয়াম ফেনক্সাইড হিসেবে) রূপান্তরিত হয়:", ["স্যালিসাইলিক অ্যাসিডে (অ্যাসপিরিনের পূর্বসূরি) CO₂ চাপে", "বেনজোইক অ্যাসিডে", "ক্রেসলে", "ক্যাটেকলে"],
       "C₆H₅ONa + CO₂ (4–7 atm, 125°C) → সোডিয়াম স্যালিসাইলেট → H⁺ → স্যালিসাইলিক অ্যাসিড।"),
    _q("Addition of HX to alkenes — peroxide effect (anti-Markovnikov) applies to:", ["HBr only (not HCl or HI) — radical mechanism gives Br at less substituted C", "HCl", "HI", "HF"],
       "Kharasch effect: in presence of peroxides, HBr adds anti-Markovnikov via radical chain: Br• adds first to terminal carbon.",
       "অ্যালকিনে HX-এর পার-অক্সাইড প্রভাব (অ্যান্টি-মার্কভনিকভ) কার জন্য?", ["শুধু HBr (HCl বা HI নয়) — মূলক পদ্ধতিতে কম-প্রতিস্থাপিত C-তে Br", "HCl", "HI", "HF"],
       "খারাশ প্রভাব: পার-অক্সাইড উপস্থিতিতে HBr অ্যান্টি-মার্কভনিকভ যোগ করে মূলক শৃঙ্খলে।"),
    _q("Amino acids at their isoelectric point (pI) are:", ["Electrically neutral zwitterions (NH₃⁺ and COO⁻ both present, net charge = 0)", "Positively charged", "Negatively charged", "Non-ionised"],
       "pI = (pKa₁ + pKa₂)/2 for simple amino acids. At pI: minimum solubility, no migration in electric field.",
       "সমতড়িৎ বিন্দুতে (pI) অ্যামাইনো অ্যাসিড:", ["বৈদ্যুতিকভাবে নিরপেক্ষ জুইটেরিয়ন (NH₃⁺ ও COO⁻ উভয় বিদ্যমান, নিট চার্জ = 0)", "ধনাত্মক আধানযুক্ত", "ঋণাত্মক আধানযুক্ত", "অআয়নীয়"],
       "pI = (pKa₁ + pKa₂)/2 সরল অ্যামাইনো অ্যাসিডের জন্য। pI-তে: সর্বনিম্ন দ্রাব্যতা, বৈদ্যুতিক ক্ষেত্রে চলন নেই।"),
    _q("The catecholamine dopamine is a neurotransmitter that is a derivative of:", ["Tyrosine (amino acid) — dopamine = 3,4-dihydroxyphenethylamine", "Tryptophan", "Phenylalanine only", "Glycine"],
       "Dopamine deficiency is linked to Parkinson's disease. It is produced in the brain and peripheral nervous system.",
       "নিউরোট্রান্সমিটার ডোপামিন কোন অ্যামাইনো অ্যাসিডের ডেরিভেটিভ?", ["টাইরোসিন — ডোপামিন = 3,4-ডাইহাইড্রক্সিফেনিথাইলামিন", "ট্রিপটোফান", "শুধু ফেনাইলঅ্যালানিন", "গ্লাইসিন"],
       "ডোপামিনের অভাব পার্কিনসন রোগের সাথে সম্পর্কিত। মস্তিষ্কে উৎপাদিত হয়।"),
    _q("Cellulose is a structural polysaccharide in which glucose units are joined by:", ["β-1,4-glycosidic bonds (humans cannot digest — lack β-glucosidase enzyme)", "α-1,4-glycosidic bonds (like starch)", "α-1,6-glycosidic bonds", "Peptide bonds"],
       "Cotton/wood = cellulose. Termites and ruminants can digest cellulose via symbiotic bacteria.",
       "কাঠামোগত পলিস্যাকারাইড সেলুলোজে গ্লুকোজ একক যুক্ত:", ["β-1,4-গ্লাইকোসিডিক বন্ধনে (মানুষ হজম করতে পারে না — β-গ্লুকোসিডেজ এনজাইম নেই)", "α-1,4-গ্লাইকোসিডিক বন্ধনে (স্টার্চের মতো)", "α-1,6-গ্লাইকোসিডিক বন্ধনে", "পেপটাইড বন্ধনে"],
       "তুলা/কাঠ = সেলুলোজ। দিমক ও রুমিন্যান্ট সিম্বায়োটিক ব্যাকটেরিয়া দিয়ে সেলুলোজ হজম করে।"),
    _q("The Haworth projection of glucose shows it in which form?", ["Pyranose ring (6-membered ring with oxygen, α or β anomer depending on position of OH at C1)", "Open-chain form", "Fischer projection", "Newman projection"],
       "In aqueous solution, glucose exists mostly as a cyclic hemiacetal (pyranose). α-D-glucose ↔ β-D-glucose via mutarotation.",
       "গ্লুকোজের হাওয়ার্থ প্রজেকশন কোন রূপ দেখায়?", ["পাইরানোজ বলয় (O সহ 6-সদস্যীয় বলয়, C1-এ OH অবস্থানের উপর α বা β অ্যানোমার)", "খোলা শৃঙ্খল রূপ", "ফিশার প্রজেকশন", "নিউম্যান প্রজেকশন"],
       "জলীয় দ্রবণে গ্লুকোজ বেশিরভাগ চক্রীয় হেমিঅ্যাসিটাল (পাইরানোজ) হিসেবে থাকে।"),
    _q("The reaction of aniline with NaNO₂/HCl at 0–5°C followed by coupling with β-naphthol gives:", ["An azo dye (orange/red colour) — used in fabric dyeing", "Phenylamine hydrochloride only", "Benzene", "Aniline hydrochloride"],
       "Diazonium salt couples with activated aromatic compounds at para position. Azo group (−N=N−) gives vivid colours.",
       "0–5°C-এ অ্যানিলিন + NaNO₂/HCl, তারপর β-ন্যাফথলের সাথে যুগলকরণে:", ["একটি অ্যাজো রং (কমলা/লাল) — কাপড় রঙ করায় ব্যবহার", "শুধু ফেনাইলামিন হাইড্রোক্লোরাইড", "বেনজিন", "অ্যানিলিন হাইড্রোক্লোরাইড"],
       "ডায়াজোনিয়াম লবণ সক্রিয় অ্যারোমেটিক যৌগের প্যারা অবস্থানে যুগল করে। অ্যাজো গ্রুপ (−N=N−) উজ্জ্বল রং দেয়।"),
    _q("The Birch reduction of benzene using Na/liq. NH₃ + alcohol gives:", ["1,4-cyclohexadiene (non-conjugated diene) — unconjugated positions reduced", "Cyclohexane", "Cyclohexene", "Benzene remains unchanged"],
       "Dissolving metal reduction: electrons from Na add to aromatic ring. Electron-donating substituents: reduction at ipso; withdrawing: at ipso also, but pattern differs.",
       "Na/তরল NH₃ + অ্যালকোহল ব্যবহার করে বেনজিনের বার্চ বিজারণে:", ["1,4-সাইক্লোহেক্সাডাইন (অ-সংযুজিত ডাইন) — অ-সংযুজিত অবস্থান বিজারিত", "সাইক্লোহেক্সেন", "সাইক্লোহেক্সিন", "বেনজিন অপরিবর্তিত থাকে"],
       "দ্রবীভূত ধাতু বিজারণ: Na থেকে ইলেকট্রন অ্যারোমেটিক বলয়ে যোগ হয়।"),
    _q("The Fries rearrangement converts a phenyl ester to:", ["A hydroxy aryl ketone (ortho or para depending on temperature)", "A carboxylic acid", "A phenol only", "An ether"],
       "High T → ortho product; low T → para product. Lewis acid catalyst (AlCl₃) used. Important in synthesis of phenol-based drugs.",
       "ফ্রিস পুনর্বিন্যাস ফেনাইল এস্টারকে রূপান্তর করে:", ["হাইড্রক্সি অ্যারাইল কিটোনে (তাপমাত্রা অনুযায়ী অর্থো বা প্যারা)", "কার্বক্সিলিক অ্যাসিডে", "শুধু ফেনলে", "ইথারে"],
       "উচ্চ T → অর্থো; কম T → প্যারা। AlCl₃ অনুঘটক। ফেনল-ভিত্তিক ওষুধ সংশ্লেষণে গুরুত্বপূর্ণ।"),
    _q("In mass spectrometry, the base peak is:", ["The most abundant peak (highest intensity) in the spectrum, assigned relative intensity 100%", "The molecular ion peak (M⁺)", "The peak at m/z = 1", "The smallest m/z peak"],
       "Molecular ion peak M⁺ gives molar mass. Base peak = most stable fragment formed during electron ionisation.",
       "ভর বর্ণালিবিদ্যায় বেস পিক:", ["বর্ণালিতে সবচেয়ে প্রচুর পিক (সর্বোচ্চ তীব্রতা), আপেক্ষিক তীব্রতা 100%", "আণবিক আয়ন পিক (M⁺)", "m/z = 1-এর পিক", "সবচেয়ে ছোট m/z পিক"],
       "আণবিক আয়ন পিক M⁺ মোলার ভর দেয়। বেস পিক = ইলেকট্রন আয়নীকরণে তৈরি সবচেয়ে স্থিতিশীল টুকরো।"),
    _q("Infrared spectroscopy identifies functional groups. The N–H stretch of a primary amine appears near:", ["3300–3500 cm⁻¹ (two bands for R–NH₂: symmetric and antisymmetric N–H)", "1700 cm⁻¹", "2900 cm⁻¹", "1500 cm⁻¹"],
       "C=O (carbonyl): ~1700 cm⁻¹. O–H (alcohol): 2500–3300 cm⁻¹ (broad). C–H: ~2900–3100 cm⁻¹.",
       "ইনফ্রারেড বর্ণালিবিদ্যায় প্রাথমিক অ্যামাইনের N–H প্রসারণ কাছে:", ["3300–3500 cm⁻¹ (R–NH₂-এ দুটো ব্যান্ড: সিমেট্রিক ও অ্যান্টিসিমেট্রিক N–H)", "1700 cm⁻¹", "2900 cm⁻¹", "1500 cm⁻¹"],
       "C=O (কার্বনাইল): ~1700 cm⁻¹। O–H (অ্যালকোহল): 2500–3300 cm⁻¹ (চওড়া)। C–H: ~2900–3100 cm⁻¹।"),
    _q("Which of the following best describes a nucleophile?", ["An electron-pair donor that attacks electron-deficient centres (e.g., OH⁻, CN⁻, NH₃)", "An electron-pair acceptor", "A species that donates protons", "A free radical"],
       "Nucleophile (Nuc:) attacks electrophile (E⁺). Lewis base = nucleophile. Distinguish from Brønsted base (proton acceptor).",
       "নিউক্লিওফাইলকে সবচেয়ে ভালো বর্ণনা:", ["ইলেকট্রন-যুগল দাতা যা ইলেকট্রন-অভাব কেন্দ্রে আক্রমণ করে (যেমন OH⁻, CN⁻, NH₃)", "ইলেকট্রন-যুগল গ্রহীতা", "প্রোটন দাতা", "মুক্তমূলক"],
       "নিউক্লিওফাইল (Nuc:) ইলেকট্রোফাইলে (E⁺) আক্রমণ করে। লুইস ক্ষার = নিউক্লিওফাইল।"),
    _q("What is the product when propan-2-ol is oxidised with acidified K₂Cr₂O₇?", ["Propan-2-one (acetone), a ketone — secondary alcohol → ketone", "Propanal", "Propanoic acid", "No reaction"],
       "2° alcohol + [O] → ketone. Ketones resist further oxidation under mild conditions.",
       "অ্যাসিডিয়ুক্ত K₂Cr₂O₇ দিয়ে প্রোপান-2-অলের জারণে:", ["প্রোপান-2-ওন (অ্যাসিটোন), কিটোন — দ্বিতীয়-ক্রম অ্যালকোহল → কিটোন", "প্রোপানাল", "প্রোপানোয়িক অ্যাসিড", "কোনো বিক্রিয়া নেই"],
       "2° অ্যালকোহল + [O] → কিটোন। মৃদু পরিস্থিতিতে কিটোন আরও জারণ প্রতিরোধ করে।"),
    _q("The pinacol rearrangement involves:", ["A 1,2-diol treated with acid: loss of water + 1,2-shift to give a carbonyl compound (pinacolone)", "Oxidation of a diol", "Reduction of a diol", "Esterification"],
       "Pinacol (2,3-dimethyl-2,3-butanediol) → pinacolone (3,3-dimethyl-2-butanone) with H₂SO₄.",
       "পিনাকোল পুনর্বিন্যাসে:", ["অ্যাসিড দিয়ে 1,2-ডাইঅল: জল হারানো + 1,2-শিফটে কার্বনাইল যৌগ", "ডাইঅলের জারণ", "ডাইঅলের বিজারণ", "এস্টারীকরণ"],
       "পিনাকোল → পিনাকোলোন H₂SO₄ দিয়ে।"),
    _q("Which of these is an example of a condensation polymer?", ["Nylon-6,6 (from hexamethylene diamine + adipic acid; loses H₂O at each bond)", "Polyethylene", "Polypropylene", "Poly(vinyl chloride)"],
       "Condensation polymer loses small molecule (H₂O, HCl) per bond. Addition polymer loses nothing.",
       "কোনটি ঘনীভবন পলিমারের উদাহরণ?", ["নাইলন-6,6 (হেক্সামেথিলিন ডাইঅ্যামাইন + অ্যাডিপিক অ্যাসিড; প্রতিটি বন্ধনে H₂O বের হয়)", "পলিইথিলিন", "পলিপ্রোপিলিন", "পলি(ভিনাইল ক্লোরাইড)"],
       "ঘনীভবন পলিমার প্রতিটি বন্ধনে ছোট অণু (H₂O, HCl) হারায়। সংযোজন পলিমার কিছু হারায় না।"),
    _q("The pH of a 10⁻⁸ M HCl solution is:", ["≈ 6.98 (not 8 — must include water's contribution: [H⁺]total = 10⁻⁸ + 10⁻⁷ ≈ 1.1×10⁻⁷; pH ≈ 6.96)", "8", "7", "1"],
       "When [H⁺] from acid is comparable to 10⁻⁷ from water, you must add both contributions. pH is always < 7 for acid.",
       "10⁻⁸ M HCl দ্রবণের pH:", ["≈ 6.98 (8 নয় — জলের অবদান যোগ করতে হবে: [H⁺]মোট ≈ 1.1×10⁻⁷; pH ≈ 6.96)", "8", "7", "1"],
       "যখন অ্যাসিড থেকে [H⁺] জলের 10⁻⁷-এর তুলনায়, উভয় যোগ করতে হবে। অ্যাসিডের pH সবসময় 7 এর নিচে।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
