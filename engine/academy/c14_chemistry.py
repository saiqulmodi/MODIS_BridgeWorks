"""IIT level - Chemistry (JEE Advanced standard): equivalents and redox stoichiometry, real gases,
thermochemical cycles, Kp and Kc, hydrolysis and buffers, integrated rate laws and activation
energy, concentration cells and the link between ΔG and K, crystal geometry, abnormal colligative
behaviour, atomic spectra and uncertainty, crystal field theory, VSEPR of hypervalent molecules,
named reactions and reaction mechanisms, and industrial inorganic chemistry."""
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
    ub = (u_en if u_bn is None else u_bn).replace("mol", "মোল")    # Bengali options: units in Bengali
    return mcq(q_en, [_f(x) + u_en for x in o], 0, ex_en, q_bn, [_f(x) + ub for x in o], ex_bn)


# ---------------------------------------------------------------- stoichiometry and gases
def redox_titration(m_kmno4, v_fe):
    v = v_fe * 0.1 / (5 * m_kmno4)
    return _n(f"What volume of {m_kmno4:g} M KMnO₄ is needed in acid to oxidise {v_fe} mL of 0.1 M Fe²⁺ to Fe³⁺?",
              f"অম্লীয় মাধ্যমে 0.1 M Fe²⁺-এর {v_fe} mL-কে Fe³⁺-এ জারিত করতে {m_kmno4:g} M পটাশিয়াম পারম্যাঙ্গানেটের কত আয়তন লাগে?", v,
              f"MnO₄⁻ takes 5 e⁻ and each Fe²⁺ gives 1: 5 x {m_kmno4:g} x V = 1 x 0.1 x {v_fe}, V = {_f(_c(v))} mL.",
              f"MnO₄⁻ 5টি ইলেকট্রন নেয় আর প্রতিটি Fe²⁺ 1টি দেয়: 5 x {m_kmno4:g} x V = 1 x 0.1 x {v_fe}, আয়তন = {_f(_c(v))} mL।",
              (v * 5, v_fe * 0.1 / m_kmno4 / 3, v * 2), " mL")


def normality(m, mm, n_factor, ml):
    nn = m / (mm / n_factor) / (ml / 1000)
    return _n(f"{m:g} g of oxalic acid dihydrate (molar mass {mm}, n-factor {n_factor} as an acid) is dissolved to {ml} mL. What is the normality?",
              f"{m:g} g অক্সালিক অ্যাসিড ডাইহাইড্রেট (মোলার ভর {mm}, অ্যাসিড হিসেবে n-গুণক {n_factor}) গুলে {ml} mL করা হল। নর্মালিটি কত?", nn,
              f"Equivalent mass = {mm} ÷ {n_factor} = {_f(_c(mm / n_factor))}; N = ({m:g} ÷ {_f(_c(mm / n_factor))}) ÷ {ml / 1000:g} = {_f(_c(nn))} N.",
              f"তুল্যাঙ্ক ভর = {mm} ÷ {n_factor} = {_f(_c(mm / n_factor))}; নর্মালিটি = ({m:g} ÷ {_f(_c(mm / n_factor))}) ÷ {ml / 1000:g} = {_f(_c(nn))} N।",
              (nn / n_factor, m / mm, nn * n_factor), " N")


def vdw_pressure(n, v, t, a, b):
    p = n * 0.0821 * t / (v - n * b) - a * n * n / (v * v)
    ideal = n * 0.0821 * t / v
    return _n(f"Using the van der Waals equation (a = {a} L² atm/mol², b = {b} L/mol), what pressure does {n} mol of gas exert in {v} L at {t} K?",
              f"ভ্যান ডার ওয়ালস সমীকরণ (a = {a} L² atm/mol², b = {b} L/mol) ব্যবহার করে {t} K-এ {v} L-এ {n} মোল গ্যাস কত চাপ দেয়?", p,
              f"P = nRT ÷ (V - nb) - an²/V² = {_f(_c(n * 0.0821 * t / (v - n * b)))} - {_f(_c(a * n * n / (v * v)))} = {_f(_c(p))} atm (ideal: {_f(_c(ideal))} atm).",
              f"চাপ = nRT ÷ (V - nb) - an²/V² = {_f(_c(n * 0.0821 * t / (v - n * b)))} - {_f(_c(a * n * n / (v * v)))} = {_f(_c(p))} atm (আদর্শ: {_f(_c(ideal))} atm)।",
              (ideal, ideal + a * n * n / (v * v), p * 1.2), " atm", " atm (বায়ুমণ্ডল)")


def vapour_density_alpha(m_theory, d_obs):
    m_obs = 2 * d_obs
    alpha = (m_theory - m_obs) / m_obs
    return _n(f"PCl₅ (molar mass {m_theory}) dissociates as PCl₅ ⇌ PCl₃ + Cl₂. At some temperature its vapour density is {d_obs}. What is the degree of dissociation?",
              f"PCl₅ (মোলার ভর {m_theory}) PCl₅ ⇌ PCl₃ + Cl₂ অনুযায়ী বিয়োজিত হয়। কোনো তাপমাত্রায় এর বাষ্পঘনত্ব {d_obs}। বিয়োজন-মাত্রা কত?", alpha,
              f"Observed molar mass = 2 x {d_obs} = {m_obs}; one molecule gives two, so α = (M_theory - M_obs) ÷ M_obs = {_f(_c(alpha))}.",
              f"পরীক্ষিত মোলার ভর = 2 x {d_obs} = {m_obs}; একটা অণু থেকে দুটো, তাই α = (M_তাত্ত্বিক - M_পরীক্ষিত) ÷ M_পরীক্ষিত = {_f(_c(alpha))}।",
              ((m_theory - m_obs) / m_theory, m_obs / m_theory, alpha + 0.3))


# ---------------------------------------------------------------- thermodynamics and equilibrium
def born_haber(sub, ie, half_bond, ea, formation):
    u = formation + sub + ie + half_bond - ea          # -ΔHf = +formation
    return _n(f"For NaCl: sublimation of Na = {sub}, ionisation energy of Na = {ie}, ½ bond energy of Cl₂ = {half_bond}, electron affinity of Cl = {ea}, and ΔHf of NaCl = -{formation} kJ/mol. What is the lattice energy (magnitude)?",
              f"NaCl-এর জন্য: Na-এর ঊর্ধ্বপাতন = {sub}, Na-এর আয়নীভবন শক্তি = {ie}, Cl₂-এর ½ বন্ধনশক্তি = {half_bond}, Cl-এর ইলেকট্রন আসক্তি = {ea} আর NaCl-এর ΔHf = -{formation} kJ/mol। কেলাস-শক্তির মান কত?", u,
              f"Born-Haber cycle: U = -ΔHf + S + IE + ½D - EA = {formation} + {sub} + {ie} + {half_bond} - {ea} = {u} kJ/mol.",
              f"বর্ন-হেবার চক্র: কেলাস-শক্তি = -ΔHf + S + IE + ½D - EA = {formation} + {sub} + {ie} + {half_bond} - {ea} = {u} kJ/mol।",
              (u - 2 * ea, sub + ie + half_bond, formation), " kJ/mol")


def kp_kc(kc, t, dn):
    kp = kc * (0.0821 * t) ** dn
    return _n(f"For a gas reaction with Δn(gas) = {dn}, Kc = {kc:g} at {t} K. What is Kp? (R = 0.0821 L atm/(mol K))",
              f"গ্যাস-মোলের পরিবর্তন Δn = {dn}-এর একটা বিক্রিয়ায় {t} K-এ Kc = {kc:g}। Kp কত? (R = 0.0821 L atm/(mol K))", kp,
              f"Kp = Kc(RT)^Δn = {kc:g} x ({_f(_c(0.0821 * t))})^{dn} = {_f(_c(kp))}.",
              f"Kp = Kc(RT)^Δn = {kc:g} x ({_f(_c(0.0821 * t))})^{dn} = {_f(_c(kp))}।",
              (kc, kc * 0.0821 * t * (dn if dn > 0 else 1) * 2, kp * 2))


def dg_from_k(k_exp, t):
    g = 2.303 * 8.314 * t * k_exp / 1000
    return _n(f"A reaction has an equilibrium constant of 10^{k_exp} at {t} K. What is the magnitude of ΔG°?",
              f"একটা বিক্রিয়ার {t} K-এ সাম্য-ধ্রুবক 10^{k_exp}। ΔG°-এর মান কত?", g,
              f"ΔG° = -2.303 RT log K = -2.303 x 8.314 x {t} x {k_exp} J = -{_f(_c(g))} kJ/mol: K > 1 means ΔG° < 0.",
              f"ΔG° = -2.303 RT log K = -2.303 x 8.314 x {t} x {k_exp} J = -{_f(_c(g))} kJ/mol: K > 1 মানে ΔG° < 0।",
              (8.314 * t * k_exp / 1000, g * 2.303, g / 2), " kJ/mol")


def salt_hydrolysis(pka, c_exp):
    ph = 7 + pka / 2 - c_exp / 2
    return _n(f"What is the pH of a 10⁻{c_exp} M solution of sodium acetate? (pKa of acetic acid = {pka})",
              f"সোডিয়াম অ্যাসিটেটের 10⁻{c_exp} M দ্রবণের pH কত? (অ্যাসিটিক অ্যাসিডের pKa = {pka})", ph,
              f"Salt of a weak acid and strong base: pH = 7 + ½pKa + ½log C = 7 + {pka / 2:g} - {c_exp / 2:g} = {_f(_c(ph))}.",
              f"দুর্বল অ্যাসিড আর তীব্র ক্ষারের লবণ: pH = 7 + ½pKa + ½log C = 7 + {pka / 2:g} - {c_exp / 2:g} = {_f(_c(ph))}।",
              (7, 7 - pka / 2 + c_exp / 2, ph + 1))


def common_ion(ksp_exp, c):
    s = 10 ** (-ksp_exp) / c
    return mcq(f"The Ksp of AgCl is 1 x 10⁻{ksp_exp}. What is its solubility in a {c:g} M NaCl solution?",
               [f"{_sci(s)} M", f"{_sci(math.sqrt(10 ** -ksp_exp))} M", f"{_sci(s * 10)} M", f"{_sci(10 ** -ksp_exp)} M"], 0,
               f"[Cl⁻] ≈ {c:g} M from NaCl, so s = Ksp ÷ [Cl⁻] = 10⁻{ksp_exp} ÷ {c:g} = {_sci(s)} M - far less than in pure water.",
               f"সোডিয়াম ক্লোরাইডের দ্রবণে AgCl-এর Ksp 1 x 10⁻{ksp_exp}। {c:g} M দ্রবণে এর দ্রাব্যতা কত?",
               [f"{_sci(s)} M", f"{_sci(math.sqrt(10 ** -ksp_exp))} M", f"{_sci(s * 10)} M", f"{_sci(10 ** -ksp_exp)} M"],
               f"সোডিয়াম ক্লোরাইড থেকে [Cl⁻] ≈ {c:g} M, তাই দ্রাব্যতা = Ksp ÷ [Cl⁻] = 10⁻{ksp_exp} ÷ {c:g} = {_sci(s)} M - বিশুদ্ধ জলের চেয়ে অনেক কম।")


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _sci(x):
    e = math.floor(math.log10(x))
    m = x / 10 ** e
    return f"{m:.3g} x 10{str(e).translate(SUP)}"


# ---------------------------------------------------------------- kinetics and electrochemistry
def ea_two_t(k_ratio, t1, t2):
    ea = 2.303 * 8.314 * math.log10(k_ratio) * t1 * t2 / (t2 - t1) / 1000
    return _n(f"A reaction's rate constant rises {k_ratio} times when the temperature goes from {t1} K to {t2} K. What is its activation energy?",
              f"তাপমাত্রা {t1} K থেকে {t2} K হলে একটা বিক্রিয়ার হার-ধ্রুবক {k_ratio} গুণ বাড়ে। এর সক্রিয়ন-শক্তি কত?", ea,
              f"log(k₂/k₁) = Ea ÷ 2.303R x (T₂ - T₁) ÷ T₁T₂, so Ea = 2.303 x 8.314 x log {k_ratio} x {t1} x {t2} ÷ {t2 - t1} = {_f(_c(ea))} kJ/mol.",
              f"log(k₂/k₁) = Ea ÷ 2.303R x (T₂ - T₁) ÷ T₁T₂, তাই সক্রিয়ন-শক্তি = 2.303 x 8.314 x log {k_ratio} x {t1} x {t2} ÷ {t2 - t1} = {_f(_c(ea))} kJ/mol।",
              (ea / 2.303, ea * 2, 8.314 * k_ratio / 10), " kJ/mol")


def first_order_time(k, pct_left):
    t = 2.303 / k * math.log10(100 / pct_left)
    return _n(f"A first-order reaction has k = {k:g} per minute. How long until only {pct_left}% of the reactant remains?",
              f"একটা প্রথম-ক্রমের বিক্রিয়ার k = প্রতি মিনিটে {k:g}। কত সময় পরে বিক্রিয়কের মাত্র {pct_left}% বাকি থাকে?", t,
              f"t = (2.303 ÷ k) log([A]₀/[A]) = (2.303 ÷ {k:g}) x log({100 / pct_left:g}) = {_f(_c(t))} min.",
              f"সময় = (2.303 ÷ k) log([A]₀/[A]) = (2.303 ÷ {k:g}) x log({100 / pct_left:g}) = {_f(_c(t))} মিনিট।",
              (0.693 / k, (100 - pct_left) / (k * 100), t * 2), " min", " মিনিট")


def second_order_half(k, a0):
    t = 1 / (k * a0)
    return _n(f"A second-order reaction (rate = k[A]²) has k = {k:g} L/(mol min) and [A]₀ = {a0:g} M. What is its first half-life?",
              f"একটা দ্বিতীয়-ক্রমের বিক্রিয়ার (হার = k[A]²) k = {k:g} L/(mol min) আর [A]₀ = {a0:g} M। এর প্রথম অর্ধায়ু কত?", t,
              f"For second order t½ = 1 ÷ (k[A]₀) = 1 ÷ ({k:g} x {a0:g}) = {_f(_c(t))} min - it doubles each successive half-life.",
              f"দ্বিতীয় ক্রমে অর্ধায়ু = 1 ÷ (k[A]₀) = 1 ÷ ({k:g} x {a0:g}) = {_f(_c(t))} মিনিট - প্রতি পরের অর্ধায়ু দ্বিগুণ হয়।",
              (0.693 / k, a0 / k, t * 2), " min", " মিনিট")


def conc_cell(c1, c2, n):
    e = 0.059 / n * math.log10(c2 / c1) * 1000
    return _n(f"A concentration cell uses Cu electrodes in {c1:g} M and {c2:g} M CuSO₄ (n = {n}). What is its emf at 25°C?",
              f"একটা ঘনমাত্রা-কোষে {c1:g} M আর {c2:g} M কপার সালফেটে তামার তড়িদ্দ্বার (n = {n})। 25°C-এ এর তড়িচ্চালক বল কত?", e,
              f"E° = 0, so E = (0.059 ÷ n) log(c₂/c₁) = (0.059 ÷ {n}) x log {c2 / c1:g} = {_f(_c(e))} mV.",
              f"E° = 0, তাই তড়িচ্চালক বল = (0.059 ÷ n) log(c₂/c₁) = (0.059 ÷ {n}) x log {c2 / c1:g} = {_f(_c(e))} mV।",
              (e * n if n > 1 else e / 2, e / 2 if n > 1 else e * 2, e * 3), " mV")

def k_from_e(n, e):
    logk = n * e / 0.059
    return _n(f"A cell reaction transfers {n} electrons and has E° = {e:g} V. What is log K at 25°C?",
              f"একটা কোষ-বিক্রিয়ায় {n}টি ইলেকট্রন স্থানান্তরিত হয়, E° = {e:g} V। 25°C-এ log K কত?", logk,
              f"log K = nE° ÷ 0.059 = {n} x {e:g} ÷ 0.059 = {_f(_c(logk))}: a large positive E° means the reaction goes almost to completion.",
              f"log K = nE° ÷ 0.059 = {n} x {e:g} ÷ 0.059 = {_f(_c(logk))}: বড় ধনাত্মক E° মানে বিক্রিয়া প্রায় সম্পূর্ণ হয়।",
              (e / 0.059, n * e, logk * 2.303))


def kohlrausch(l1, l2, l3):
    r = l1 + l2 - l3
    return _n(f"Limiting molar conductivities (S cm²/mol) are HCl {l1}, CH₃COONa {l2} and NaCl {l3}. What is Λ° for acetic acid?",
              f"সীমাস্থ মোলার পরিবাহিতা (S cm²/mol): HCl {l1}, সোডিয়াম অ্যাসিটেট {l2} আর NaCl {l3}। অ্যাসিটিক অ্যাসিডের Λ° কত?", r,
              f"Kohlrausch's law: Λ°(CH₃COOH) = Λ°(HCl) + Λ°(CH₃COONa) - Λ°(NaCl) = {l1} + {l2} - {l3} = {_f(_c(r))}.",
              f"কোলরাউশের সূত্র: অ্যাসিটিক অ্যাসিডের Λ° = HCl + সোডিয়াম অ্যাসিটেট - NaCl = {l1} + {l2} - {l3} = {_f(_c(r))}।",
              (l1 + l2 + l3, l1 - l2 + l3, l2), " S cm²/mol", " S cm²/মোল")


def degree_ionisation(lam, lam0):
    a = lam / lam0
    return _n(f"A weak acid solution has molar conductivity {lam} S cm²/mol; its limiting value is {lam0}. What is the degree of ionisation?",
              f"একটা দুর্বল অ্যাসিডের দ্রবণের মোলার পরিবাহিতা {lam} S cm²/mol; এর সীমাস্থ মান {lam0}। আয়নীভবন-মাত্রা কত?", a,
              f"α = Λm ÷ Λ°m = {lam} ÷ {lam0} = {_f(_c(a))}.",
              f"আয়নীভবন-মাত্রা = Λm ÷ Λ°m = {lam} ÷ {lam0} = {_f(_c(a))}।",
              (lam0 / lam / 100, a * a, a + 0.1))


# ---------------------------------------------------------------- structure and solid state
def radius_ratio(r_plus, r_minus):
    rr = r_plus / r_minus
    cn, shape_en, shape_bn = (8, "cubic", "ঘনকাকার") if rr >= 0.732 else ((6, "octahedral", "অষ্টতলকীয়") if rr >= 0.414 else (4, "tetrahedral", "চতুস্তলকীয়"))
    return _n(f"A cation of radius {r_plus} pm fits among anions of radius {r_minus} pm. Using the radius-ratio rule, what coordination number is expected?",
              f"{r_plus} pm ব্যাসার্ধের একটা ক্যাটায়ন {r_minus} pm ব্যাসার্ধের অ্যানায়নদের মধ্যে বসে। ব্যাসার্ধ-অনুপাত নিয়মে কোন সন্নিবেশ-সংখ্যা প্রত্যাশিত?", cn,
              f"r⁺/r⁻ = {_f(_c(rr))}: 0.414-0.732 gives 6 (octahedral), above 0.732 gives 8, 0.225-0.414 gives 4 - here {cn} ({shape_en}).",
              f"r⁺/r⁻ = {_f(_c(rr))}: 0.414-0.732-এ 6 (অষ্টতলকীয়), 0.732-এর বেশিতে 8, 0.225-0.414-এ 4 - এখানে {cn} ({shape_bn})।",
              (12, 3, 2))


def voids(n_atoms):
    return _n(f"A crystal has {n_atoms} atoms in cubic close packing. How many tetrahedral voids are there?",
              f"একটা কেলাসে ঘনকীয় ঘন-সজ্জায় {n_atoms}টি পরমাণু। কয়টি চতুস্তলকীয় ফাঁক আছে?", 2 * n_atoms,
              f"Close packing of N spheres gives 2N tetrahedral and N octahedral voids: 2 x {n_atoms} = {2 * n_atoms}.",
              f"N গোলকের ঘন-সজ্জায় 2N চতুস্তলকীয় আর N অষ্টতলকীয় ফাঁক: 2 x {n_atoms} = {2 * n_atoms}।",
              (n_atoms, n_atoms // 2, 4 * n_atoms))


def edge_from_radius(r, kind):
    a = 2 * math.sqrt(2) * r if kind == "fcc" else 4 * r / math.sqrt(3)
    en = "face-centred cubic" if kind == "fcc" else "body-centred cubic"
    bn = "মুখকেন্দ্রিক ঘনকাকার" if kind == "fcc" else "দেহকেন্দ্রিক ঘনকাকার"
    rel = "a = 2√2 r (atoms touch along the face diagonal)" if kind == "fcc" else "a = 4r/√3 (atoms touch along the body diagonal)"
    rel_bn = "a = 2√2 r (মুখ-কর্ণ বরাবর পরমাণু ছোঁয়)" if kind == "fcc" else "a = 4r/√3 (দেহ-কর্ণ বরাবর পরমাণু ছোঁয়)"
    return _n(f"A metal with atomic radius {r} pm crystallises in a {en} lattice. What is the edge length of the unit cell?",
              f"{r} pm পারমাণবিক ব্যাসার্ধের একটা ধাতু {bn} জালকে কেলাসিত হয়। একক-কোষের ধারের দৈর্ঘ্য কত?", a,
              f"{rel} = {_f(_c(a))} pm.", f"{rel_bn} = {_f(_c(a))} pm।",
              (2 * r, 4 * r / math.sqrt(3) if kind == "fcc" else 2 * math.sqrt(2) * r, 4 * r), " pm")


def vant_hoff_assoc(alpha, n):
    i = 1 - alpha + alpha / n
    return _n(f"Acetic acid dimerises in benzene. If {alpha * 100:g}% of the molecules associate into dimers, what is the van 't Hoff factor i?",
              f"বেঞ্জিনে অ্যাসিটিক অ্যাসিড দ্বিতয় (ডাইমার) গঠন করে। {alpha * 100:g}% অণু ডাইমারে যুক্ত হলে ভ্যান্ট হফ গুণক i কত?", i,
              f"i = 1 - α + α/n = 1 - {alpha:g} + {alpha:g}/{n} = {_f(_c(i))}: association lowers the particle count.",
              f"i = 1 - α + α/n = 1 - {alpha:g} + {alpha:g}/{n} = {_f(_c(i))}: সংযুক্তি কণার সংখ্যা কমায়।",
              (1 + alpha, 1 - alpha, i + 0.5))


def vant_hoff_dissoc(alpha, ions):
    i = 1 + (ions - 1) * alpha
    return _n(f"A salt that gives {ions} ions per formula unit is {alpha * 100:g}% dissociated in water. What is its van 't Hoff factor?",
              f"সূত্র-এককপ্রতি {ions}টি আয়ন দেওয়া একটা লবণ জলে {alpha * 100:g}% বিয়োজিত। এর ভ্যান্ট হফ গুণক কত?", i,
              f"i = 1 + (n - 1)α = 1 + {ions - 1} x {alpha:g} = {_f(_c(i))}.",
              f"i = 1 + (n - 1)α = 1 + {ions - 1} x {alpha:g} = {_f(_c(i))}।",
              (ions, 1 + ions * alpha, i - 0.5 if i > 1.5 else i + 1))


def rydberg(n1, n2, series_en, series_bn):
    inv = 1.097e7 * (1 / n1 ** 2 - 1 / n2 ** 2)
    lam = 1 / inv * 1e9
    return _n(f"What is the wavelength of the {series_en} line for an electron dropping from n = {n2} to n = {n1} in hydrogen? (R = 1.097 x 10⁷ m⁻¹)",
              f"হাইড্রোজেনে ইলেকট্রন n = {n2} থেকে n = {n1}-এ নামলে {series_bn} রেখার তরঙ্গদৈর্ঘ্য কত? (R = 1.097 x 10⁷ m⁻¹)", lam,
              f"1/λ = R(1/{n1}² - 1/{n2}²) = {_f(_c(inv / 1e6))} x 10⁶ m⁻¹, so λ = {_f(_c(lam))} nm.",
              f"1/λ = R(1/{n1}² - 1/{n2}²) = {_f(_c(inv / 1e6))} x 10⁶ m⁻¹, তাই তরঙ্গদৈর্ঘ্য = {_f(_c(lam))} nm।",
              (lam / 2, lam * 1.5, 1 / (1.097e7 / n1 ** 2) * 1e9), " nm")


def spectral_lines(n):
    r = n * (n - 1) // 2
    return _n(f"Electrons in a sample of hydrogen atoms are excited to n = {n}. How many different spectral lines can appear as they return to the ground state?",
              f"একগুচ্ছ হাইড্রোজেন পরমাণুর ইলেকট্রন n = {n}-এ উত্তেজিত। ভূমি-অবস্থায় ফেরার সময় কয়টি ভিন্ন বর্ণালি-রেখা দেখা যেতে পারে?", r,
              f"Any pair of the {n} levels can give a line: n(n - 1)/2 = {r}.",
              f"{n}টি স্তরের যেকোনো জোড় থেকে একটা রেখা: n(n - 1)/2 = {r}টি।",
              (n - 1, n * n, r + n))


def uncertainty(dx_pm):
    dv = 6.626e-34 / (4 * math.pi * 9.11e-31 * dx_pm * 1e-12) / 1e6
    return _n(f"An electron's position is known within {dx_pm} pm. What is the minimum uncertainty in its velocity? (h = 6.626 x 10⁻³⁴ J s, m = 9.11 x 10⁻³¹ kg)",
              f"একটা ইলেকট্রনের অবস্থান {dx_pm} pm-এর মধ্যে জানা। তার বেগে ন্যূনতম অনিশ্চয়তা কত? (h = 6.626 x 10⁻³⁴ J s, m = 9.11 x 10⁻³¹ kg)", dv,
              f"Δx·mΔv ≥ h/4π: Δv = h ÷ (4π m Δx) = {_f(_c(dv))} x 10⁶ m/s - comparable to the electron's speed in an atom.",
              f"Δx·mΔv ≥ h/4π: Δv = h ÷ (4π m Δx) = {_f(_c(dv))} x 10⁶ m/s - পরমাণুতে ইলেকট্রনের বেগের সঙ্গে তুলনীয়।",
              (dv * 4 * math.pi, dv / 2, dv * 2), " x 10⁶ m/s")


HIGH = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0), 4: (3, 1), 5: (3, 2), 6: (4, 2), 7: (5, 2), 8: (6, 2), 9: (6, 3), 10: (6, 4)}
LOW = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0), 4: (4, 0), 5: (5, 0), 6: (6, 0), 7: (6, 1), 8: (6, 2), 9: (6, 3), 10: (6, 4)}


def cfse(d, low_spin, label_en, label_bn):
    t2g, eg = (LOW if low_spin else HIGH)[d]
    e = -0.4 * t2g + 0.6 * eg
    return _n(f"What is the crystal field stabilisation energy of {label_en} in an octahedral field (in units of Δo, ignoring pairing energy)?",
              f"অষ্টতলকীয় ক্ষেত্রে {label_bn}-এর কেলাস-ক্ষেত্র স্থিতিশীলতা শক্তি কত (Δo এককে, জোড়-শক্তি বাদে)?", abs(e),
              f"t₂g^{t2g} e_g^{eg}: CFSE = (-0.4 x {t2g} + 0.6 x {eg})Δo = {_f(_c(e))}Δo; magnitude {_f(_c(abs(e)))}Δo.",
              f"t₂g^{t2g} e_g^{eg}: স্থিতিশীলতা শক্তি = (-0.4 x {t2g} + 0.6 x {eg})Δo = {_f(_c(e))}Δo; মান {_f(_c(abs(e)))}Δo।",
              (0.4 * d, abs(e) + 0.4, 0.6 * d), " Δo")

def ean(z, ox, cn):
    r = z - ox + 2 * cn
    return _n(f"A metal of atomic number {z} in the +{ox} state is bonded to {cn} ligands, each donating a pair of electrons. What is its effective atomic number (EAN)?",
              f"{z} পারমাণবিক সংখ্যার একটা ধাতু +{ox} অবস্থায় {cn}টি লিগ্যান্ডের সঙ্গে যুক্ত, প্রত্যেকে এক জোড়া ইলেকট্রন দেয়। এর কার্যকর পারমাণবিক সংখ্যা কত?", r,
              f"EAN = Z - oxidation state + 2 x ligands = {z} - {ox} + {2 * cn} = {r}; 36 matches krypton.",
              f"কার্যকর পারমাণবিক সংখ্যা = Z - জারণ-অবস্থা + 2 x লিগ্যান্ড = {z} - {ox} + {2 * cn} = {r}; 36 মানে ক্রিপটনের সমান।",
              (z + 2 * cn, z - ox + cn, r + 2))


def isomers_alkane(c, n, name_en, name_bn):
    return _n(f"How many structural (chain) isomers does {name_en} (C{c}H{2 * c + 2}) have?",
              f"{name_bn}-এর (C{c}H{2 * c + 2}) কয়টি গাঠনিক (শৃঙ্খল) সমাণু আছে?", n,
              f"Drawing every distinct carbon skeleton gives {n} isomers for C{c}H{2 * c + 2}.",
              f"প্রতিটি ভিন্ন কার্বন-কাঠামো আঁকলে C{c}H{2 * c + 2}-এর {n}টি সমাণু পাওয়া যায়।",
              (n + 1, n - 1 if n > 2 else n + 2, c))


def combustion_c(m_co2, m_sample):
    p = m_co2 * 12 / 44 / m_sample * 100
    return _n(f"Burning {m_sample} g of an organic compound gives {m_co2} g of CO₂. What is the percentage of carbon in the compound?",
              f"{m_sample} g একটা জৈব যৌগ পোড়ালে {m_co2} g CO₂ পাওয়া যায়। যৌগে কার্বনের শতাংশ কত?", p,
              f"Mass of C = {m_co2} x 12/44 = {_f(_c(m_co2 * 12 / 44))} g; % C = {_f(_c(m_co2 * 12 / 44))} ÷ {m_sample} x 100 = {_f(_c(p))}%.",
              f"কার্বনের ভর = {m_co2} x 12/44 = {_f(_c(m_co2 * 12 / 44))} g; কার্বনের শতাংশ = {_f(_c(m_co2 * 12 / 44))} ÷ {m_sample} x 100 = {_f(_c(p))}%।",
              (m_co2 / m_sample * 100, p * 44 / 12 / 10, p + 8), "%")


def kjeldahl(v_acid, m_acid, m_sample):
    p = 1.4 * v_acid * m_acid / m_sample
    return _n(f"In Kjeldahl's method, the ammonia from {m_sample} g of a compound neutralises {v_acid} mL of {m_acid:g} M H₂SO₄. What is the percentage of nitrogen? (each mol H₂SO₄ takes 2 mol NH₃)",
              f"কেলডালের পদ্ধতিতে {m_sample} g যৌগের অ্যামোনিয়া {m_acid:g} M সালফিউরিক অ্যাসিডের {v_acid} mL প্রশমিত করে। নাইট্রোজেনের শতাংশ কত? (প্রতি মোল অ্যাসিড 2 মোল NH₃ নেয়)", p * 2,
              f"% N = 1.4 x normality x volume ÷ mass = 1.4 x {2 * m_acid:g} x {v_acid} ÷ {m_sample} = {_f(_c(p * 2))}%.",
              f"নাইট্রোজেনের শতাংশ = 1.4 x নর্মালিটি x আয়তন ÷ ভর = 1.4 x {2 * m_acid:g} x {v_acid} ÷ {m_sample} = {_f(_c(p * 2))}%।",
              (p, p * 4, p * 2 + 5), "%")


NUMERIC = [
    redox_titration(0.02, 20), redox_titration(0.01, 25), redox_titration(0.05, 50),
    normality(6.3, 126, 2, 500), normality(12.6, 126, 2, 250), normality(3.15, 126, 2, 100),
    vdw_pressure(1, 10, 300, 3.59, 0.0427), vdw_pressure(2, 5, 400, 1.39, 0.0391),
    vapour_density_alpha(208.5, 80), vapour_density_alpha(208.5, 62.5),
    born_haber(108, 496, 121, 349, 411), born_haber(89, 419, 121, 349, 437),
    kp_kc(0.5, 500, 1), kp_kc(2, 400, -1), kp_kc(4, 300, 2),
    dg_from_k(2, 298), dg_from_k(5, 300), dg_from_k(10, 298),
    salt_hydrolysis(4.74, 1), salt_hydrolysis(4.74, 2), salt_hydrolysis(4.2, 1),
    common_ion(10, 0.1), common_ion(10, 0.01),
    ea_two_t(2, 300, 310), ea_two_t(4, 300, 320), ea_two_t(10, 300, 350),
    first_order_time(0.1, 10), first_order_time(0.05, 1), first_order_time(0.2303, 50),
    second_order_half(0.5, 0.1), second_order_half(2, 0.25),
    conc_cell(0.01, 1, 2), conc_cell(0.001, 0.1, 2), conc_cell(0.01, 0.1, 1),
    k_from_e(2, 1.1), k_from_e(1, 0.59), k_from_e(2, 0.295),
    kohlrausch(426, 91, 126), kohlrausch(425.9, 91, 126.4),
    degree_ionisation(39, 390), degree_ionisation(16, 400),
    radius_ratio(102, 181), radius_ratio(169, 181), radius_ratio(74, 184),
    voids(6), voids(12),
    edge_from_radius(128, "fcc"), edge_from_radius(124, "bcc"), edge_from_radius(144, "fcc"),
    vant_hoff_assoc(0.8, 2), vant_hoff_assoc(0.6, 2), vant_hoff_dissoc(0.9, 2), vant_hoff_dissoc(0.8, 3),
    rydberg(1, 2, "Lyman", "লাইম্যান"), rydberg(2, 3, "Balmer (H-α)", "বামার (H-α)"), rydberg(3, 4, "Paschen", "পাশেন"),
    spectral_lines(4), spectral_lines(5), spectral_lines(6),
    uncertainty(100), uncertainty(50),
    cfse(3, False, "Cr³⁺ (d³)", "Cr³⁺ (d³)"), cfse(6, True, "low-spin Co³⁺ (d⁶)", "নিম্ন-স্পিন Co³⁺ (d⁶)"),
    cfse(8, False, "Ni²⁺ (d⁸)", "Ni²⁺ (d⁸)"), cfse(4, False, "high-spin Mn³⁺ (d⁴)", "উচ্চ-স্পিন Mn³⁺ (d⁴)"),
    ean(26, 2, 6), ean(27, 3, 6), ean(28, 0, 4), ean(24, 0, 6),
    isomers_alkane(5, 3, "pentane", "পেন্টেন"), isomers_alkane(6, 5, "hexane", "হেক্সেন"), isomers_alkane(7, 9, "heptane", "হেপ্টেন"),
    combustion_c(0.88, 0.3), combustion_c(1.32, 0.6),
    kjeldahl(25, 0.5, 1.4), kjeldahl(20, 0.25, 0.7),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    _q("What is the shape of ClF₃?", ["T-shaped", "Trigonal planar", "Trigonal pyramidal", "Tetrahedral"],
       "Five electron pairs (3 bonds, 2 lone pairs in equatorial positions) leave a T shape.",
       "ক্লোরিন ট্রাইফ্লুওরাইডের আকৃতি কী?", ["T-আকৃতি", "ত্রিকোণী সমতলীয়", "ত্রিকোণী পিরামিডীয়", "চতুস্তলকীয়"],
       "পাঁচ জোড়া ইলেকট্রন (3টি বন্ধন, নিরক্ষীয় অবস্থানে 2টি নিঃসঙ্গ জোড়) T আকার রাখে।"),
    _q("What is the shape of the I₃⁻ ion?", ["Linear", "Bent", "Trigonal planar", "T-shaped"],
       "The central iodine has 3 lone pairs in the equatorial plane of a trigonal bipyramid, leaving the two bonds opposite each other.",
       "I₃⁻ আয়নের আকৃতি কী?", ["রৈখিক", "বাঁকা", "ত্রিকোণী সমতলীয়", "T-আকৃতি"],
       "কেন্দ্রীয় আয়োডিনের 3টি নিঃসঙ্গ জোড় ত্রিকোণী দ্বিপিরামিডের নিরক্ষীয় তলে, তাই দুটো বন্ধন মুখোমুখি।"),
    _q("What is the shape of BrF₅?", ["Square pyramidal", "Trigonal bipyramidal", "Octahedral", "Pentagonal planar"],
       "Six electron pairs with one lone pair: the five F atoms form a square pyramid.",
       "ব্রোমিন পেন্টাফ্লুওরাইডের আকৃতি কী?", ["বর্গ-পিরামিডীয়", "ত্রিকোণী দ্বিপিরামিডীয়", "অষ্টতলকীয়", "পঞ্চভুজ সমতলীয়"],
       "ছয় জোড়া ইলেকট্রন, একটা নিঃসঙ্গ জোড়: পাঁচটি F পরমাণু বর্গ-পিরামিড গড়ে।"),
    _q("Which order of bond angles is correct?", ["NH₃ > H₂O", "H₂O > NH₃", "They are equal", "Both are exactly 109.5°"],
       "NH₃ (107°) has one lone pair; H₂O (104.5°) has two, which squeeze the bonds more.",
       "বন্ধন-কোণের কোন ক্রম সঠিক?", ["NH₃ > H₂O", "H₂O > NH₃", "দুটো সমান", "দুটোই ঠিক 109.5°"],
       "NH₃ (107°)-এ একটা নিঃসঙ্গ জোড়; H₂O (104.5°)-এ দুটো, যা বন্ধনগুলোকে বেশি চাপে।"),
    _q("Why does a real gas deviate most from ideal behaviour at high pressure and low temperature?", ["Molecular volume and intermolecular attractions become significant", "Molecules move faster", "The gas becomes lighter", "Collisions stop"],
       "The compressibility factor Z = PV/nRT then departs from 1.",
       "উচ্চ চাপ আর নিম্ন তাপমাত্রায় প্রকৃত গ্যাস আদর্শ আচরণ থেকে সবচেয়ে বেশি বিচ্যুত হয় কেন?", ["অণুর আয়তন আর আন্তঃআণবিক আকর্ষণ গুরুত্বপূর্ণ হয়ে ওঠে", "অণুগুলো দ্রুত চলে", "গ্যাস হালকা হয়", "সংঘর্ষ থেমে যায়"],
       "তখন সংনম্যতা-গুণক Z = PV/nRT 1 থেকে সরে যায়।"),
    _q("Above its critical temperature, a gas…", ["Cannot be liquefied by pressure alone", "Liquefies easily", "Becomes a solid", "Has no pressure"],
       "Supercritical CO₂ is used to decaffeinate coffee for this reason.",
       "সংকট তাপমাত্রার উপরে একটা গ্যাস…", ["কেবল চাপ দিয়ে তরলিত হয় না", "সহজে তরলিত হয়", "কঠিন হয়ে যায়", "এর কোনো চাপ নেই"],
       "এই কারণে অতিসংকট CO₂ দিয়ে কফি থেকে ক্যাফেইন বাদ দেওয়া হয়।"),
    _q("A solution shows a positive deviation from Raoult's law. What can you say?", ["A-B attractions are weaker than A-A and B-B, and it may form a minimum-boiling azeotrope", "It obeys Raoult's law exactly", "A-B attractions are stronger", "It cannot boil"],
       "Ethanol-water is an example; its azeotrope (95.6% ethanol) boils below either pure liquid.",
       "একটা দ্রবণ রাউল্টের সূত্র থেকে ধনাত্মক বিচ্যুতি দেখায়। কী বলা যায়?", ["A-B আকর্ষণ A-A আর B-B-এর চেয়ে দুর্বল, আর এটা ন্যূনতম-স্ফুটনাঙ্কের অ্যাজিওট্রপ গড়তে পারে", "এটা হুবহু রাউল্টের সূত্র মানে", "A-B আকর্ষণ বেশি শক্তিশালী", "এটা ফুটতে পারে না"],
       "ইথানল-জল এর উদাহরণ; এর অ্যাজিওট্রপ (95.6% ইথানল) দুটো বিশুদ্ধ তরলের চেয়ে কম তাপমাত্রায় ফোটে।"),
    _q("Which statement about the Freundlich adsorption isotherm is correct?", ["x/m = k P^(1/n), with n > 1, so adsorption rises less than proportionally with pressure", "Adsorption falls with pressure", "Adsorption is independent of pressure", "It applies only to liquids"],
       "A log-log plot of x/m against P gives a straight line of slope 1/n.",
       "ফ্রয়েন্ডলিখ অধিশোষণ সমোষ্ণরেখা সম্পর্কে কোন বিবৃতি সঠিক?", ["x/m = k P^(1/n), n > 1, তাই চাপের সমানুপাতের চেয়ে কম হারে অধিশোষণ বাড়ে", "চাপ বাড়লে অধিশোষণ কমে", "অধিশোষণ চাপ-নিরপেক্ষ", "এটা কেবল তরলে খাটে"],
       "x/m বনাম P-এর লগ-লগ লেখচিত্র 1/n নতির সরলরেখা দেয়।"),
    _q("How does a catalyst work in terms of the energy profile?", ["It provides an alternative path with a lower activation energy", "It raises the energy of the products", "It changes ΔH of the reaction", "It shifts the equilibrium"],
       "Both forward and reverse barriers drop by the same amount.",
       "শক্তি-লেখচিত্রের দিক থেকে অনুঘটক কীভাবে কাজ করে?", ["কম সক্রিয়ন-শক্তির একটা বিকল্প পথ দেয়", "উৎপাদের শক্তি বাড়ায়", "বিক্রিয়ার ΔH বদলায়", "সাম্য সরিয়ে দেয়"],
       "সম্মুখ আর বিপরীত দুই বাধাই সমান পরিমাণে কমে।"),
    _q("What does the Michaelis constant Km of an enzyme represent?", ["The substrate concentration at which the rate is half of Vmax", "The maximum rate", "The enzyme's molar mass", "The temperature optimum"],
       "A low Km means the enzyme binds its substrate tightly.",
       "একটা এনজাইমের মাইকেলিস ধ্রুবক Km কী বোঝায়?", ["যে সাবস্ট্রেট ঘনমাত্রায় হার Vmax-এর অর্ধেক", "সর্বোচ্চ হার", "এনজাইমের মোলার ভর", "অনুকূলতম তাপমাত্রা"],
       "কম Km মানে এনজাইম সাবস্ট্রেটকে শক্তভাবে বাঁধে।"),
    _q("What is the order of a reaction whose half-life is independent of the starting concentration?", ["First order", "Zero order", "Second order", "Third order"],
       "Radioactive decay is the classic first-order process.",
       "যে বিক্রিয়ার অর্ধায়ু শুরুর ঘনমাত্রার উপর নির্ভর করে না, তার ক্রম কত?", ["প্রথম ক্রম", "শূন্য ক্রম", "দ্বিতীয় ক্রম", "তৃতীয় ক্রম"],
       "তেজস্ক্রিয় ক্ষয় প্রথম-ক্রমের প্রমাণ উদাহরণ।"),
    _q("Why are pseudo-first-order reactions so called?", ["One reactant is in such large excess that its concentration is effectively constant", "They have no rate law", "They are always slow", "They involve only one molecule"],
       "The acid hydrolysis of an ester in water is a typical example.",
       "ছদ্ম-প্রথম-ক্রমের বিক্রিয়াকে এই নাম দেওয়া হয় কেন?", ["একটা বিক্রিয়ক এত বেশি পরিমাণে থাকে যে তার ঘনমাত্রা কার্যত স্থির", "তাদের কোনো হার-সূত্র নেই", "তারা সবসময় ধীর", "তাতে কেবল একটা অণু জড়িত"],
       "জলে এস্টারের অম্লীয় আর্দ্রবিশ্লেষণ একটা সাধারণ উদাহরণ।"),
    _q("A cell reaction has a positive E°cell. What follows?", ["ΔG° is negative and K is greater than 1", "ΔG° is positive", "K is less than 1", "The reaction cannot happen"],
       "ΔG° = -nFE° = -RT ln K link all three quantities.",
       "একটা কোষ-বিক্রিয়ার E°কোষ ধনাত্মক। এ থেকে কী বোঝা যায়?", ["ΔG° ঋণাত্মক আর K 1-এর বেশি", "ΔG° ধনাত্মক", "K 1-এর কম", "বিক্রিয়া ঘটতে পারে না"],
       "ΔG° = -nFE° = -RT ln K তিনটি রাশিকে যুক্ত করে।"),
    _q("In the electrolysis of aqueous NaCl with inert electrodes, what forms at the cathode?", ["Hydrogen gas", "Sodium metal", "Chlorine gas", "Oxygen gas"],
       "Water is reduced more easily than Na⁺; chlorine forms at the anode and NaOH stays in solution.",
       "নিষ্ক্রিয় তড়িদ্দ্বার দিয়ে জলীয় NaCl-এর তড়িৎবিশ্লেষণে ক্যাথোডে কী তৈরি হয়?", ["হাইড্রোজেন গ্যাস", "সোডিয়াম ধাতু", "ক্লোরিন গ্যাস", "অক্সিজেন গ্যাস"],
       "Na⁺-এর চেয়ে জল সহজে বিজারিত হয়; অ্যানোডে ক্লোরিন তৈরি হয় আর NaOH দ্রবণে থাকে।"),
    _q("What kind of defect is created when Na⁺ ions are missing and their charge is balanced by electrons in the vacancies (F-centres)?", ["A metal-excess defect giving colour", "A Frenkel defect", "A Schottky defect only", "An impurity defect"],
       "Heating NaCl in sodium vapour makes it yellow because trapped electrons absorb light.",
       "অ্যানায়নের শূন্যস্থানে ইলেকট্রন আটকে থাকলে (এফ-কেন্দ্র) কোন ধরনের ত্রুটি তৈরি হয়?", ["ধাতু-আধিক্য ত্রুটি, যা রং দেয়", "ফ্রেঙ্কেল ত্রুটি", "কেবল শটকি ত্রুটি", "অপদ্রব্য ত্রুটি"],
       "সোডিয়াম বাষ্পে NaCl গরম করলে আটকে থাকা ইলেকট্রন আলো শোষণ করে, তাই এটা হলুদ হয়।"),
    _q("A Frenkel defect differs from a Schottky defect because…", ["An ion moves to an interstitial site, so density does not change", "Equal numbers of cations and anions are missing", "It increases the density", "It only occurs in metals"],
       "AgCl and AgBr show Frenkel defects (small cations); NaCl and KCl show Schottky defects.",
       "ফ্রেঙ্কেল ত্রুটি শটকি ত্রুটি থেকে আলাদা কারণ…", ["একটা আয়ন অন্তর্বর্তী স্থানে সরে যায়, তাই ঘনত্ব বদলায় না", "সমান সংখ্যক ক্যাটায়ন আর অ্যানায়ন অনুপস্থিত", "এটা ঘনত্ব বাড়ায়", "এটা কেবল ধাতুতে ঘটে"],
       "AgCl আর AgBr ফ্রেঙ্কেল ত্রুটি দেখায় (ছোট ক্যাটায়ন); NaCl আর KCl দেখায় শটকি ত্রুটি।"),
    _q("Which reagent pair converts a carbonyl group (C=O) into CH₂ under strongly basic conditions?", ["Hydrazine and KOH (Wolff-Kishner reduction)", "Zn-Hg and HCl", "LiAlH₄ only", "NaBH₄ only"],
       "Clemmensen reduction (Zn-Hg, HCl) does the same job in acid; LiAlH₄ and NaBH₄ give alcohols.",
       "কোন বিকারক-জোড় তীব্র ক্ষারীয় অবস্থায় কার্বনিল গ্রুপকে (C=O) CH₂-তে পরিণত করে?", ["হাইড্রাজিন আর পটাশিয়াম হাইড্রক্সাইড (উলফ-কিশনার বিজারণ)", "Zn-Hg আর হাইড্রোক্লোরিক অ্যাসিড", "কেবল লিথিয়াম অ্যালুমিনিয়াম হাইড্রাইড", "কেবল সোডিয়াম বোরোহাইড্রাইড"],
       "ক্লেমেনসেন বিজারণ (Zn-Hg, HCl) অম্লে একই কাজ করে; লিথিয়াম অ্যালুমিনিয়াম হাইড্রাইড আর সোডিয়াম বোরোহাইড্রাইড অ্যালকোহল দেয়।"),
    _q("Phenol with chloroform and aqueous NaOH gives salicylaldehyde. This is the…", ["Reimer-Tiemann reaction", "Kolbe reaction", "Gattermann-Koch reaction", "Sandmeyer reaction"],
       "Dichlorocarbene is the electrophile and attacks mainly the ortho position.",
       "ক্লোরোফর্ম আর জলীয় NaOH-এর সঙ্গে ফেনল স্যালিসাইলালডিহাইড দেয়। এটা…", ["রাইমার-টাইম্যান বিক্রিয়া", "কোলবে বিক্রিয়া", "গ্যাটারম্যান-কখ বিক্রিয়া", "স্যান্ডমেয়ার বিক্রিয়া"],
       "ডাইক্লোরোকার্বিন ইলেকট্রোফাইল, প্রধানত অর্থো অবস্থানে আক্রমণ করে।"),
    _q("Sodium phenoxide heated with CO₂ under pressure, then acidified, gives…", ["Salicylic acid (Kolbe's reaction)", "Benzoic acid", "Phenyl acetate", "Benzaldehyde"],
       "Salicylic acid is then acetylated to make aspirin.",
       "চাপে CO₂-এর সঙ্গে সোডিয়াম ফিনক্সাইড গরম করে অম্লীকরণ করলে পাওয়া যায়…", ["স্যালিসাইলিক অ্যাসিড (কোলবের বিক্রিয়া)", "বেঞ্জোয়িক অ্যাসিড", "ফিনাইল অ্যাসিটেট", "বেঞ্জালডিহাইড"],
       "স্যালিসাইলিক অ্যাসিডকে তারপর অ্যাসিটাইলেশন করে অ্যাসপিরিন তৈরি হয়।"),
    _q("A benzenediazonium salt treated with CuCl gives chlorobenzene. This is the…", ["Sandmeyer reaction", "Gattermann reaction with copper powder only", "Wurtz-Fittig reaction", "Friedel-Crafts reaction"],
       "Diazonium salts are versatile: CuBr gives bromobenzene, CuCN benzonitrile, and warming in water phenol.",
       "বেঞ্জিনডায়াজোনিয়াম লবণকে কিউপ্রাস ক্লোরাইড দিয়ে বিক্রিয়া করালে ক্লোরোবেঞ্জিন পাওয়া যায়। এটা…", ["স্যান্ডমেয়ার বিক্রিয়া", "কেবল তামার গুঁড়োসহ গ্যাটারম্যান বিক্রিয়া", "উর্টজ-ফিটিগ বিক্রিয়া", "ফ্রিডেল-ক্রাফটস বিক্রিয়া"],
       "ডায়াজোনিয়াম লবণ বহুমুখী: কিউপ্রাস ব্রোমাইড ব্রোমোবেঞ্জিন, কিউপ্রাস সায়ানাইড বেঞ্জোনাইট্রাইল, আর জলে গরম করলে ফেনল দেয়।"),
    _q("A diene reacts with an alkene to form a six-membered ring in one step. This is the…", ["Diels-Alder reaction", "Aldol condensation", "Wittig reaction", "Cannizzaro reaction"],
       "It is a concerted [4+2] cycloaddition; the diene must be able to adopt the s-cis form.",
       "একটা ডাইইন একটা অ্যালকিনের সঙ্গে এক ধাপে ছয়-সদস্যের বলয় গড়ে। এটা…", ["ডিলস-অ্যাল্ডার বিক্রিয়া", "অ্যালডল ঘনীভবন", "উইটিগ বিক্রিয়া", "ক্যানিজারো বিক্রিয়া"],
       "এটা একসঙ্গে ঘটা [4+2] বলয়-সংযোজন; ডাইইনকে এস-সিস রূপ নিতে পারতে হয়।"),
    _q("A ketone oxime rearranges in acid to give an amide. This is the…", ["Beckmann rearrangement", "Hofmann degradation", "Curtius reaction", "Baeyer-Villiger oxidation"],
       "Cyclohexanone oxime gives caprolactam this way - the monomer for nylon-6.",
       "অম্লে একটা কিটোন অক্সিম পুনর্বিন্যস্ত হয়ে অ্যামাইড দেয়। এটা…", ["বেকম্যান পুনর্বিন্যাস", "হফম্যান অবক্ষয়", "কার্টিয়াস বিক্রিয়া", "বেয়ার-ভিলিগার জারণ"],
       "সাইক্লোহেক্সানোন অক্সিম থেকে এভাবে ক্যাপ্রোল্যাকটাম হয় - নাইলন-6-এর মনোমার।"),
    _q("Which reagent converts a ketone into an ester by inserting an oxygen atom?", ["A peroxyacid (Baeyer-Villiger oxidation)", "Hydrazine", "Sodium borohydride", "Grignard reagent"],
       "The group better able to carry positive charge migrates to oxygen.",
       "কোন বিকারক একটা অক্সিজেন পরমাণু ঢুকিয়ে কিটোনকে এস্টারে পরিণত করে?", ["একটা পারঅক্সি-অ্যাসিড (বেয়ার-ভিলিগার জারণ)", "হাইড্রাজিন", "সোডিয়াম বোরোহাইড্রাইড", "গ্রিনিয়ার বিকারক"],
       "যে গ্রুপ ধনাত্মক আধান ভালো বইতে পারে, সেটা অক্সিজেনে সরে যায়।"),
    _q("A phosphorus ylide converts an aldehyde into an alkene. This is the…", ["Wittig reaction", "Perkin reaction", "Claisen condensation", "Michael addition"],
       "It fixes the position of the new C=C exactly where the C=O was.",
       "একটা ফসফরাস ইলাইড অ্যালডিহাইডকে অ্যালকিনে পরিণত করে। এটা…", ["উইটিগ বিক্রিয়া", "পার্কিন বিক্রিয়া", "ক্লাইজেন ঘনীভবন", "মাইকেল সংযোজন"],
       "এটা নতুন C=C-কে ঠিক সেখানে বসায় যেখানে C=O ছিল।"),
    _q("Benzene reduced by sodium in liquid ammonia with an alcohol gives…", ["1,4-cyclohexadiene (Birch reduction)", "Cyclohexane", "Benzyl alcohol", "Toluene"],
       "Solvated electrons add one at a time; the ring is not fully reduced.",
       "অ্যালকোহলসহ তরল অ্যামোনিয়ায় সোডিয়াম দিয়ে বেঞ্জিন বিজারিত করলে পাওয়া যায়…", ["1,4-সাইক্লোহেক্সাডাইইন (বার্চ বিজারণ)", "সাইক্লোহেক্সেন", "বেঞ্জাইল অ্যালকোহল", "টলুইন"],
       "দ্রাবকযুক্ত ইলেকট্রন একে একে যুক্ত হয়; বলয় পুরো বিজারিত হয় না।"),
    _q("In an E2 elimination with a bulky base such as tert-butoxide, the major alkene is usually…", ["The less substituted (Hofmann) alkene", "The more substituted (Saytzeff) alkene", "No alkene forms", "An alcohol"],
       "The bulky base removes the most accessible hydrogen; small bases favour the more stable Saytzeff product.",
       "টারশিয়ারি-বিউটক্সাইডের মতো ভারী ক্ষার দিয়ে E2 অপসারণে প্রধান অ্যালকিন সাধারণত…", ["কম প্রতিস্থাপিত (হফম্যান) অ্যালকিন", "বেশি প্রতিস্থাপিত (সেজফ) অ্যালকিন", "কোনো অ্যালকিন হয় না", "একটা অ্যালকোহল"],
       "ভারী ক্ষার সবচেয়ে সহজলভ্য হাইড্রোজেন সরায়; ছোট ক্ষার বেশি স্থিতিশীল সেজফ উৎপাদ দেয়।"),
    _q("E2 elimination requires the leaving group and the β-hydrogen to be…", ["Anti-periplanar (180° apart)", "Syn and 0° apart always", "On the same carbon", "Far apart on different rings"],
       "In cyclohexanes both must be axial for E2 to occur.",
       "E2 অপসারণে বিদায়ী গ্রুপ আর β-হাইড্রোজেনকে থাকতে হয়…", ["প্রতি-সমতলীয় (180° দূরে)", "সবসময় একই দিকে 0°-তে", "একই কার্বনে", "ভিন্ন বলয়ে দূরে"],
       "সাইক্লোহেক্সেনে E2 ঘটতে হলে দুটোকেই অক্ষীয় হতে হয়।"),
    _q("Why is cyclobutadiene very unstable?", ["It is antiaromatic, with 4n π electrons in a planar ring", "It is aromatic", "It has no π electrons", "It is ionic"],
       "Planar cyclic 4n π systems are destabilised; cyclooctatetraene avoids this by puckering into a tub.",
       "সাইক্লোবিউটাডাইয়িন এত অস্থিতিশীল কেন?", ["এটা প্রতি-অ্যারোমেটিক, সমতলীয় বলয়ে 4n π ইলেকট্রন", "এটা অ্যারোমেটিক", "এর কোনো π ইলেকট্রন নেই", "এটা আয়নীয়"],
       "সমতলীয় চক্রীয় 4n π ব্যবস্থা অস্থিতিশীল; সাইক্লোঅক্টাটেট্রাইন টব-আকারে বেঁকে এটা এড়ায়।"),
    _q("Keto-enol tautomerism involves…", ["Movement of a hydrogen atom and a double bond between carbon and oxygen", "Movement of a carbon atom", "Breaking of the ring", "A change in molecular formula"],
       "Tautomers are distinct, interconverting isomers; the keto form usually dominates for simple ketones.",
       "কিটো-এনল চলাবয়বতায় ঘটে…", ["কার্বন আর অক্সিজেনের মধ্যে একটা হাইড্রোজেন পরমাণু আর একটা দ্বিবন্ধনের সরণ", "একটা কার্বন পরমাণুর সরণ", "বলয় ভাঙা", "আণবিক সংকেতের পরিবর্তন"],
       "চলাবয়বেরা আলাদা, পরস্পরে রূপান্তরিত সমাণু; সরল কিটোনে সাধারণত কিটো রূপই প্রধান।"),
    _q("Which is the strongest base in water?", ["Dimethylamine", "Ammonia", "Aniline", "Trimethylamine"],
       "Alkyl groups push electrons onto N, but in water solvation favours secondary amines; aniline's lone pair is delocalised into the ring.",
       "জলে কোনটা সবচেয়ে তীব্র ক্ষার?", ["ডাইমিথাইলঅ্যামিন", "অ্যামোনিয়া", "অ্যানিলিন", "ট্রাইমিথাইলঅ্যামিন"],
       "অ্যালকাইল গ্রুপ নাইট্রোজেনে ইলেকট্রন ঠেলে, কিন্তু জলে দ্রাবকীকরণ দ্বিতীয়ক অ্যামিনকে সুবিধা দেয়; অ্যানিলিনের নিঃসঙ্গ জোড় বলয়ে ছড়ানো।"),
    _q("Which is the correct order of SN1 reactivity?", ["Benzyl chloride > tert-butyl chloride > isopropyl chloride > ethyl chloride", "Ethyl > isopropyl > tert-butyl > benzyl", "All react equally", "Isopropyl > benzyl > ethyl"],
       "SN1 rate follows carbocation stability; the benzyl cation is stabilised by resonance.",
       "SN1 সক্রিয়তার সঠিক ক্রম কোনটা?", ["বেঞ্জাইল ক্লোরাইড > টারশিয়ারি-বিউটাইল ক্লোরাইড > আইসোপ্রোপাইল ক্লোরাইড > ইথাইল ক্লোরাইড", "ইথাইল > আইসোপ্রোপাইল > টারশিয়ারি-বিউটাইল > বেঞ্জাইল", "সবাই সমানভাবে বিক্রিয়া করে", "আইসোপ্রোপাইল > বেঞ্জাইল > ইথাইল"],
       "SN1-এর হার কার্বোক্যাটায়নের স্থিতিশীলতা অনুসরণ করে; বেঞ্জাইল ক্যাটায়ন অনুনাদে স্থিতিশীল।"),
    _q("Why is fluoride a poor leaving group in SN2 reactions in protic solvents although fluorine is very electronegative?", ["The C-F bond is very strong and F⁻ is strongly solvated, a relatively strong base", "Fluorine is too large", "F⁻ is a weak base", "C-F bonds are weak"],
       "Good leaving groups are weak bases: I⁻ > Br⁻ > Cl⁻ > F⁻.",
       "প্রোটিক দ্রাবকে SN2 বিক্রিয়ায় ফ্লুওরাইড খারাপ বিদায়ী গ্রুপ কেন, যদিও ফ্লুওরিন খুব তড়িৎ-ঋণাত্মক?", ["C-F বন্ধন খুব শক্ত আর F⁻ তুলনায় তীব্র ক্ষার, বেশি দ্রাবকযুক্ত", "ফ্লুওরিন খুব বড়", "F⁻ দুর্বল ক্ষার", "C-F বন্ধন দুর্বল"],
       "ভালো বিদায়ী গ্রুপ দুর্বল ক্ষার: I⁻ > Br⁻ > Cl⁻ > F⁻।"),
    _q("Which statement about the chelate effect is true?", ["Complexes with multidentate ligands are more stable than similar ones with monodentate ligands", "Chelates are always less stable", "Chelation decreases entropy", "Only cations can chelate"],
       "Replacing several monodentate ligands with one chelate releases molecules, increasing entropy - EDTA binds metals very strongly.",
       "কিলেট প্রভাব সম্পর্কে কোন বিবৃতি সত্য?", ["বহুদন্তী লিগ্যান্ডের জটিল একদন্তী লিগ্যান্ডের অনুরূপ জটিলের চেয়ে বেশি স্থিতিশীল", "কিলেট সবসময় কম স্থিতিশীল", "কিলেশন এনট্রপি কমায়", "কেবল ক্যাটায়ন কিলেট গড়তে পারে"],
       "কয়েকটা একদন্তী লিগ্যান্ডের বদলে একটা কিলেট এলে অণু মুক্ত হয়, এনট্রপি বাড়ে - ইডিটিএ ধাতুকে খুব শক্তভাবে বাঁধে।"),
    _q("[Co(NH₃)₅Br]SO₄ and [Co(NH₃)₅SO₄]Br are examples of…", ["Ionisation isomers", "Linkage isomers", "Geometrical isomers", "Optical isomers"],
       "They give different ions in solution: one precipitates with BaCl₂, the other with AgNO₃.",
       "[Co(NH₃)₅Br]SO₄ আর [Co(NH₃)₅SO₄]Br কীসের উদাহরণ?", ["আয়নীভবন সমাবয়ব", "সংযোগ সমাবয়ব", "জ্যামিতিক সমাবয়ব", "আলোক সমাবয়ব"],
       "দ্রবণে এরা ভিন্ন আয়ন দেয়: একটা বেরিয়াম ক্লোরাইডে, অন্যটা সিলভার নাইট্রেটে অধঃক্ষেপ দেয়।"),
    _q("NO₂⁻ binding through N in one complex and through O in another is an example of…", ["Linkage isomerism", "Ionisation isomerism", "Hydrate isomerism", "Coordination isomerism"],
       "Ambidentate ligands such as NO₂⁻ and SCN⁻ can bond through different atoms.",
       "একটা জটিলে NO₂⁻ নাইট্রোজেন দিয়ে আর অন্যটায় অক্সিজেন দিয়ে যুক্ত হওয়া কীসের উদাহরণ?", ["সংযোগ সমাবয়বতা", "আয়নীভবন সমাবয়বতা", "হাইড্রেট সমাবয়বতা", "সন্নিবেশ সমাবয়বতা"],
       "NO₂⁻ আর SCN⁻-এর মতো উভদন্তী লিগ্যান্ড ভিন্ন পরমাণু দিয়ে বন্ধন গড়তে পারে।"),
    _q("Why are tetrahedral complexes almost always high-spin?", ["The splitting Δt is small (about 4/9 Δo), less than the pairing energy", "They have no d electrons", "Ligands are always strong-field", "They are always diamagnetic"],
       "With small splitting it costs less to put electrons in higher orbitals than to pair them.",
       "চতুস্তলকীয় জটিল প্রায় সবসময় উচ্চ-স্পিন কেন?", ["বিভাজন Δt ছোট (প্রায় 4/9 Δo), জোড়-শক্তির চেয়ে কম", "এদের d ইলেকট্রন নেই", "লিগ্যান্ড সবসময় তীব্র-ক্ষেত্র", "এরা সবসময় তিরশ্চৌম্বক"],
       "বিভাজন ছোট হলে ইলেকট্রন জোড় না বেঁধে উঁচু কক্ষকে বসাতে কম শক্তি লাগে।"),
    _q("Which metal is purified by Mond's process via its volatile carbonyl?", ["Nickel", "Zirconium", "Silicon", "Copper"],
       "Ni + 4CO → Ni(CO)₄ at about 330 K, which decomposes back to pure Ni at about 450 K.",
       "কোন ধাতু উদ্বায়ী কার্বনিলের মাধ্যমে মন্ডের পদ্ধতিতে বিশুদ্ধ করা হয়?", ["নিকেল", "জিরকোনিয়াম", "সিলিকন", "তামা"],
       "প্রায় 330 K-এ Ni + 4CO → Ni(CO)₄, যা প্রায় 450 K-এ ভেঙে আবার বিশুদ্ধ Ni দেয়।"),
    _q("Zone refining is used to obtain ultra-pure…", ["Silicon and germanium for semiconductors", "Iron for steel", "Aluminium foil", "Mercury"],
       "Impurities are more soluble in the melt, so a moving molten zone sweeps them to one end.",
       "অতি-বিশুদ্ধ কী পেতে জোন রিফাইনিং ব্যবহৃত হয়?", ["অর্ধপরিবাহীর জন্য সিলিকন আর জার্মেনিয়াম", "ইস্পাতের জন্য লোহা", "অ্যালুমিনিয়াম ফয়েল", "পারদ"],
       "অপদ্রব্য গলিত অংশে বেশি দ্রাব্য, তাই চলমান গলিত অঞ্চল সেগুলোকে এক প্রান্তে ঠেলে নেয়।"),
    _q("In the Hall-Héroult process, why is cryolite added to alumina?", ["To lower the melting point and improve conductivity", "To oxidise aluminium", "To make the metal magnetic", "To remove carbon"],
       "Alumina melts above 2,000°C; dissolved in molten cryolite it can be electrolysed near 950°C.",
       "হল-হেরো পদ্ধতিতে অ্যালুমিনায় ক্রায়োলাইট যোগ করা হয় কেন?", ["গলনাঙ্ক কমাতে আর পরিবাহিতা বাড়াতে", "অ্যালুমিনিয়াম জারিত করতে", "ধাতুকে চৌম্বক করতে", "কার্বন সরাতে"],
       "অ্যালুমিনা 2,000°C-এর বেশিতে গলে; গলিত ক্রায়োলাইটে দ্রবীভূত করলে প্রায় 950°C-এ তড়িৎবিশ্লেষণ করা যায়।"),
    _q("In the Ostwald process, ammonia is first oxidised over which catalyst?", ["Platinum-rhodium gauze", "Iron", "Vanadium pentoxide", "Nickel"],
       "4NH₃ + 5O₂ → 4NO + 6H₂O; the NO is then oxidised and absorbed in water to give nitric acid.",
       "অস্টওয়াল্ড পদ্ধতিতে অ্যামোনিয়া প্রথমে কোন অনুঘটকের উপর জারিত হয়?", ["প্ল্যাটিনাম-রোডিয়াম জাল", "লোহা", "ভ্যানাডিয়াম পেন্টক্সাইড", "নিকেল"],
       "4NH₃ + 5O₂ → 4NO + 6H₂O; তারপর NO জারিত হয়ে জলে শোষিত হয়ে নাইট্রিক অ্যাসিড দেয়।"),
    _q("What forms when XeF₆ is completely hydrolysed?", ["XeO₃", "Xe and O₂ only", "XeF₂", "XeO₄"],
       "XeF₆ + 3H₂O → XeO₃ + 6HF; XeO₃ is a dangerously explosive solid.",
       "XeF₆ সম্পূর্ণ আর্দ্রবিশ্লেষিত হলে কী তৈরি হয়?", ["জেনন ট্রাইঅক্সাইড (XeO₃)", "কেবল জেনন আর অক্সিজেন", "জেনন ডাইফ্লুওরাইড (XeF₂)", "জেনন টেট্রাঅক্সাইড (XeO₄)"],
       "XeF₆ + 3H₂O → XeO₃ + 6HF; XeO₃ একটা বিপজ্জনক বিস্ফোরক কঠিন।"),
    _q("Why do silicones have water-repellent, heat-stable properties?", ["They have a strong Si-O-Si backbone with organic groups on the outside", "They contain metal atoms", "They are ionic solids", "They are unsaturated hydrocarbons"],
       "They are made by hydrolysing alkylchlorosilanes and polymerising the silanols.",
       "সিলিকোন জল-বিকর্ষী আর তাপ-স্থিতিশীল কেন?", ["এদের শক্ত Si-O-Si মেরুদণ্ড, বাইরের দিকে জৈব গ্রুপ", "এতে ধাতব পরমাণু আছে", "এরা আয়নীয় কঠিন", "এরা অসম্পৃক্ত হাইড্রোকার্বন"],
       "অ্যালকাইলক্লোরোসাইলেন আর্দ্রবিশ্লেষণ করে সাইলানলগুলোর পলিমারকরণে এরা তৈরি হয়।"),
    _q("Which interhalogen compound is the most reactive?", ["ClF₃", "ICl", "BrCl", "IBr"],
       "Interhalogens are generally more reactive than halogens (except F₂); ClF₃ is so reactive it was considered as a rocket oxidiser.",
       "কোন আন্তঃহ্যালোজেন যৌগ সবচেয়ে সক্রিয়?", ["ক্লোরিন ট্রাইফ্লুওরাইড", "আয়োডিন মনোক্লোরাইড", "ব্রোমিন মনোক্লোরাইড", "আয়োডিন মনোব্রোমাইড"],
       "আন্তঃহ্যালোজেন সাধারণত হ্যালোজেনের চেয়ে (ফ্লুওরিন ছাড়া) বেশি সক্রিয়; ক্লোরিন ট্রাইফ্লুওরাইড এত সক্রিয় যে রকেটের জারক হিসেবে ভাবা হয়েছিল।"),
    _q("Which of these is the strongest acid?", ["HClO₄", "HClO₃", "HClO₂", "HOCl"],
       "More oxygen atoms on chlorine spread the negative charge of the conjugate base more widely.",
       "এগুলোর মধ্যে কোনটা সবচেয়ে তীব্র অ্যাসিড?", ["পারক্লোরিক অ্যাসিড", "ক্লোরিক অ্যাসিড", "ক্লোরাস অ্যাসিড", "হাইপোক্লোরাস অ্যাসিড"],
       "ক্লোরিনে বেশি অক্সিজেন থাকলে অনুবন্ধী ক্ষারের ঋণাত্মক আধান বেশি ছড়িয়ে পড়ে।"),
    _q("Why is H₃PO₃ dibasic, not tribasic?", ["Only two of its hydrogens are attached to oxygen; one is bonded directly to phosphorus", "It has only two hydrogens", "Phosphorus is in the +5 state", "It is a strong base"],
       "Only O-H hydrogens are acidic; H₃PO₂ is monobasic for the same reason.",
       "H₃PO₃ ত্রিক্ষারীয় না হয়ে দ্বিক্ষারীয় কেন?", ["এর মাত্র দুটো হাইড্রোজেন অক্সিজেনে যুক্ত; একটা সরাসরি ফসফরাসে", "এতে মাত্র দুটো হাইড্রোজেন", "ফসফরাস +5 অবস্থায়", "এটা তীব্র ক্ষার"],
       "কেবল O-H হাইড্রোজেনই অম্লীয়; একই কারণে H₃PO₂ একক্ষারীয়।"),
    _q("Which oxide of nitrogen is a brown, paramagnetic gas?", ["NO₂", "N₂O", "N₂O₅", "N₂O₃ solid"],
       "NO₂ has an odd electron; it dimerises to colourless N₂O₄ on cooling.",
       "নাইট্রোজেনের কোন অক্সাইড বাদামি, অনুচৌম্বক গ্যাস?", ["নাইট্রোজেন ডাইঅক্সাইড", "নাইট্রাস অক্সাইড", "নাইট্রোজেন পেন্টক্সাইড", "কঠিন নাইট্রোজেন ট্রাইঅক্সাইড"],
       "NO₂-তে একটা বিজোড় ইলেকট্রন; ঠান্ডা করলে এটা দ্বিতয় হয়ে বর্ণহীন N₂O₄ হয়।"),
    _q("Why is the second ionisation energy of sodium much larger than its first?", ["The second electron comes from a stable, inner noble-gas core", "Sodium has no second electron", "The nucleus becomes smaller", "It is the same"],
       "Na⁺ has the neon configuration; removing from it breaks a filled shell close to the nucleus.",
       "সোডিয়ামের দ্বিতীয় আয়নীভবন শক্তি প্রথমটার চেয়ে অনেক বেশি কেন?", ["দ্বিতীয় ইলেকট্রন আসে স্থিতিশীল, ভেতরের নিষ্ক্রিয়-গ্যাস কোর থেকে", "সোডিয়ামের দ্বিতীয় ইলেকট্রন নেই", "নিউক্লিয়াস ছোট হয়ে যায়", "এটা একই"],
       "Na⁺-এর নিয়ন বিন্যাস; তা থেকে সরালে নিউক্লিয়াসের কাছের একটা পূর্ণ কক্ষ ভাঙে।"),
    _q("Why does the electron gain enthalpy of chlorine exceed that of fluorine?", ["Fluorine's small 2p shell is crowded, so an added electron is repelled more", "Fluorine is not a halogen", "Chlorine is smaller", "Fluorine has no vacancy"],
       "Similarly, sulphur has a more negative electron gain enthalpy than oxygen.",
       "ক্লোরিনের ইলেকট্রন-গ্রহণ এনথালপি ফ্লুওরিনের চেয়ে বেশি কেন?", ["ফ্লুওরিনের ছোট 2p কক্ষ ঘিঞ্জি, তাই যোগ হওয়া ইলেকট্রন বেশি বিকর্ষিত হয়", "ফ্লুওরিন হ্যালোজেন নয়", "ক্লোরিন ছোট", "ফ্লুওরিনে কোনো শূন্যস্থান নেই"],
       "একইভাবে অক্সিজেনের চেয়ে সালফারের ইলেকট্রন-গ্রহণ এনথালপি বেশি ঋণাত্মক।"),
    _q("Which is used as the borax bead test?", ["Coloured metaborate glasses identify transition-metal ions", "It detects halides", "It measures pH", "It detects organic nitrogen"],
       "For example, cobalt gives a blue bead and chromium a green one.",
       "বোরাক্স বিড পরীক্ষা কী কাজে লাগে?", ["রঙিন মেটাবোরেট কাচ দিয়ে অবস্থান্তর-ধাতুর আয়ন শনাক্ত করতে", "হ্যালাইড শনাক্ত করতে", "pH মাপতে", "জৈব নাইট্রোজেন শনাক্ত করতে"],
       "যেমন কোবাল্ট নীল আর ক্রোমিয়াম সবুজ বিড দেয়।"),
    _q("What is the role of a nucleophile in neighbouring-group participation?", ["An internal group assists departure of the leaving group, often giving retention of configuration", "It always causes inversion", "It slows every reaction", "It removes a proton"],
       "Two inversions (internal then external attack) give overall retention and often a faster rate.",
       "প্রতিবেশী গ্রুপের অংশগ্রহণে একটা অভ্যন্তরীণ নিউক্লিওফাইলের ভূমিকা কী?", ["একটা অভ্যন্তরীণ গ্রুপ বিদায়ী গ্রুপকে সরাতে সাহায্য করে, প্রায়ই বিন্যাস অপরিবর্তিত রাখে", "সবসময় বিন্যাস উল্টে দেয়", "প্রতিটি বিক্রিয়া ধীর করে", "একটা প্রোটন সরায়"],
       "দুটো উল্টে যাওয়া (প্রথমে অভ্যন্তরীণ, পরে বাহ্যিক আক্রমণ) মিলে বিন্যাস অপরিবর্তিত থাকে, আর হার প্রায়ই বেশি হয়।"),
    _q("Which compound undergoes the Cannizzaro reaction?", ["Benzaldehyde", "Acetaldehyde", "Acetone", "Propanal"],
       "Only aldehydes with no α-hydrogen do so; acetaldehyde gives an aldol instead.",
       "কোন যৌগ ক্যানিজারো বিক্রিয়া দেয়?", ["বেঞ্জালডিহাইড", "অ্যাসিট্যালডিহাইড", "অ্যাসিটোন", "প্রোপানাল"],
       "কেবল α-হাইড্রোজেনহীন অ্যালডিহাইড এটা দেয়; অ্যাসিট্যালডিহাইড বরং অ্যালডল দেয়।"),
    _q("Glucose reacts with excess phenylhydrazine to form…", ["An osazone, the same one as fructose gives", "A cyclic ester", "Sorbitol", "Gluconic acid only"],
       "C-1 and C-2 both react, so glucose, fructose and mannose give the same osazone.",
       "অতিরিক্ত ফিনাইলহাইড্রাজিনের সঙ্গে গ্লুকোজ তৈরি করে…", ["একটা ওসাজোন, যা ফ্রুক্টোজও একই দেয়", "একটা চক্রীয় এস্টার", "সরবিটল", "কেবল গ্লুকোনিক অ্যাসিড"],
       "C-1 আর C-2 দুটোই বিক্রিয়া করে, তাই গ্লুকোজ, ফ্রুক্টোজ আর ম্যানোজ একই ওসাজোন দেয়।"),
    _q("What are anomers?", ["Cyclic sugar isomers that differ only at the new chiral carbon formed by ring closure", "Mirror-image amino acids", "Different sugars entirely", "Isotopes of carbon"],
       "α- and β-D-glucose differ at C-1; they interconvert in water (mutarotation).",
       "অ্যানোমার কী?", ["চক্রীয় শর্করার সমাণু, যারা কেবল বলয়-গঠনে তৈরি নতুন কাইরাল কার্বনে আলাদা", "দর্পণ-প্রতিবিম্ব অ্যামিনো অ্যাসিড", "সম্পূর্ণ ভিন্ন শর্করা", "কার্বনের আইসোটোপ"],
       "α- আর β-D-গ্লুকোজ C-1-এ আলাদা; জলে তারা পরস্পরে বদলায় (মিউটারোটেশন)।"),
    _q("Which polymer is made by addition polymerisation using a Ziegler-Natta catalyst?", ["High-density polythene", "Nylon-6,6", "Terylene", "Bakelite"],
       "Ziegler-Natta catalysts (TiCl₄ + Al(C₂H₅)₃) make linear, stereoregular chains.",
       "জিগলার-নাট্টা অনুঘটক দিয়ে যুত-পলিমারকরণে কোন পলিমার তৈরি হয়?", ["উচ্চ-ঘনত্বের পলিথিন", "নাইলন-6,6", "টেরিলিন", "ব্যাকেলাইট"],
       "জিগলার-নাট্টা অনুঘটক (TiCl₄ + Al(C₂H₅)₃) রৈখিক, নিয়মিত-বিন্যাসের শৃঙ্খল তৈরি করে।"),
    _q("Why does a 0.1 M solution of a weak acid conduct electricity less than 0.1 M HCl?", ["The weak acid is only partly ionised, giving fewer ions", "Weak acids have larger ions", "HCl is a weak electrolyte", "Weak acids are not soluble"],
       "Molar conductivity of a weak electrolyte rises steeply on dilution as ionisation increases.",
       "দুর্বল অ্যাসিডের 0.1 M দ্রবণ 0.1 M হাইড্রোক্লোরিক অ্যাসিডের চেয়ে কম তড়িৎ পরিবহন করে কেন?", ["দুর্বল অ্যাসিড আংশিক আয়নিত, তাই আয়ন কম", "দুর্বল অ্যাসিডের আয়ন বড়", "হাইড্রোক্লোরিক অ্যাসিড দুর্বল তড়িৎবিশ্লেষ্য", "দুর্বল অ্যাসিড দ্রাব্য নয়"],
       "লঘুকরণে আয়নীভবন বাড়ে, তাই দুর্বল তড়িৎবিশ্লেষ্যের মোলার পরিবাহিতা খুব বাড়ে।"),
    _q("Which law explains why the pressure of a gas in a closed container rises with temperature at constant volume?", ["Gay-Lussac's (pressure) law", "Boyle's law", "Graham's law", "Avogadro's law"],
       "P ∝ T (in kelvin) at constant V and n - why pressure cookers and gas cylinders need safety valves.",
       "স্থির আয়তনে বন্ধ পাত্রে তাপমাত্রার সঙ্গে গ্যাসের চাপ বাড়ে কেন, কোন সূত্র তা ব্যাখ্যা করে?", ["গে-লুসাকের (চাপ) সূত্র", "বয়েলের সূত্র", "গ্রাহামের সূত্র", "অ্যাভোগাড্রোর সূত্র"],
       "স্থির V আর n-এ P ∝ T (কেলভিনে) - তাই প্রেশার কুকার আর গ্যাস সিলিন্ডারে নিরাপত্তা-ভাল্ভ লাগে।"),
]


# ---------------------------------------------------------------- more calculations
def buffer_ph(pka, salt, acid, name_en, name_bn):
    ph = pka + math.log10(salt / acid)
    return _n(f"A buffer holds {salt:g} M of the sodium salt and {acid:g} M of {name_en} (pKa = {pka}). What is its pH?",
              f"একটা বাফারে {salt:g} M সোডিয়াম লবণ আর {acid:g} M {name_bn} (pKa = {pka}) আছে। এর pH কত?", ph,
              f"Henderson-Hasselbalch: pH = pKa + log([salt] ÷ [acid]) = {pka} + log({salt:g} ÷ {acid:g}) = {_f(_c(ph))}.",
              f"হেন্ডারসন-হ্যাসেলবাখ: pH = pKa + log([লবণ] ÷ [অ্যাসিড]) = {pka} + log({salt:g} ÷ {acid:g}) = {_f(_c(ph))}।",
              (pka - math.log10(salt / acid), pka + salt / acid, 7.5))


def faraday_mass(amps, minutes, molar, n, metal_en, metal_bn):
    m = amps * minutes * 60 * molar / (n * 96500)
    return _n(f"A current of {amps} A flows for {minutes} minutes through a solution of {metal_en} ions (M{'⁺' if n == 1 else str(n).translate(SUP) + '⁺'}, molar mass {molar}). What mass of {metal_en} is deposited?",
              f"{metal_bn}-আয়নের (M{'⁺' if n == 1 else str(n).translate(SUP) + '⁺'}, মোলার ভর {molar}) দ্রবণে {minutes} মিনিট ধরে {amps} A তড়িৎ চলে। কত ভর {metal_bn} জমা হয়?", m,
              f"Faraday: m = I t M ÷ (n F) = {amps} x {minutes * 60} x {molar} ÷ ({n} x 96500) = {_f(_c(m))} g.",
              f"ফ্যারাডে: ভর = I t M ÷ (n F) = {amps} x {minutes * 60} x {molar} ÷ ({n} x 96500) = {_f(_c(m))} g।",
              (m * n, m / 2, amps * minutes * molar / (n * 96500)), " g")


def osmotic(g, molar, litres, t, solute_en, solute_bn):
    pi = g / molar / litres * 0.0821 * t
    return _n(f"{g:g} g of {solute_en} (molar mass {molar}) is dissolved to make {litres:g} L of solution at {t} K. What is its osmotic pressure?",
              f"{t} K-এ {g:g} g {solute_bn} (মোলার ভর {molar}) গুলে {litres:g} লিটার দ্রবণ তৈরি হল। এর অভিস্রবণ চাপ কত?", pi,
              f"π = CRT = ({g:g} ÷ {molar} ÷ {litres:g}) x 0.0821 x {t} = {_f(_c(pi))} atm.",
              f"অভিস্রবণ চাপ = CRT = ({g:g} ÷ {molar} ÷ {litres:g}) x 0.0821 x {t} = {_f(_c(pi))} বায়ুমণ্ডলীয় চাপ।",
              (pi / 2, g / molar * 0.0821 * t * 1.5, pi + 3), " atm", " বায়ুমণ্ডলীয় চাপ")


def cell_density(z, molar, a_pm, name_en, name_bn, lattice_en, lattice_bn):
    rho = z * molar / (6.022e23 * (a_pm * 1e-10) ** 3)
    return _n(f"{name_en} has a {lattice_en} unit cell (Z = {z}) with edge {a_pm} pm and molar mass {molar}. What is its density?",
              f"{name_bn}-এর {lattice_bn} একক কোষ (Z = {z}), ধার {a_pm} pm, মোলার ভর {molar}। এর ঘনত্ব কত?", rho,
              f"ρ = Z M ÷ (N_A a³) = {z} x {molar} ÷ (6.022 x 10²³ x ({a_pm} x 10⁻¹⁰ cm)³) = {_f(_c(rho))} g/cm³.",
              f"ঘনত্ব = Z M ÷ (N_A a³) = {z} x {molar} ÷ (6.022 x 10²³ x ({a_pm} x 10⁻¹⁰ cm)³) = {_f(_c(rho))} g/cm³।",
              (rho / 2, rho * 1.5, rho / 4), " g/cm³")


def decay_left(half, t, unit_en, unit_bn, what_en, what_bn):
    left = 100 * 0.5 ** (t / half)
    return _n(f"{what_en} has a half-life of {half:,} {unit_en}. What percentage of it is left after {t:,} {unit_en}?",
              f"{what_bn}-এর অর্ধায়ু {half:,} {unit_bn}। {t:,} {unit_bn} পরে এর কত শতাংশ থাকে?", left,
              f"{t:,} ÷ {half:,} = {_f(_c(t / half))} half-lives, so 100 x (½)^{_f(_c(t / half))} = {_f(_c(left))}% is left.",
              f"{t:,} ÷ {half:,} = {_f(_c(t / half))}টি অর্ধায়ু, তাই 100 x (½)^{_f(_c(t / half))} = {_f(_c(left))}% থাকে।",
              (100 - left, 100 * half / t / 2, left + 15), "%")


def transition_entropy(dh, t, change_en, change_bn):
    ds = dh * 1000 / t
    return _n(f"The enthalpy of {change_en} is {dh} kJ/mol at {t} K. What is the entropy change for it?",
              f"{t} K-এ {change_bn}-এর এনথালপি {dh} kJ/mol। এর এনট্রপি পরিবর্তন কত?", ds,
              f"At a phase change ΔG = 0, so ΔS = ΔH ÷ T = {dh * 1000:g} J/mol ÷ {t} K = {_f(_c(ds))} J/(K mol).",
              f"দশা পরিবর্তনে ΔG = 0, তাই ΔS = ΔH ÷ T = {dh * 1000:g} J/mol ÷ {t} K = {_f(_c(ds))} J/(K mol)।",
              (ds / 10, ds * 1.5, ds + 50), " J/(K mol)")


def bp_elevation(kb, g, molar, kg, solute_en, solute_bn, solvent_en, solvent_bn):
    dt = kb * (g / molar) / kg
    return _n(f"{g:g} g of {solute_en} (molar mass {molar}) is dissolved in {kg:g} kg of {solvent_en} (Kb = {kb} K kg/mol). By how much does the boiling point rise?",
              f"{kg:g} কেজি {solvent_bn}-এ (Kb = {kb} K kg/mol) {g:g} g {solute_bn} (মোলার ভর {molar}) গোলানো হল। স্ফুটনাঙ্ক কত বাড়ে?", dt,
              f"ΔTb = Kb x m = {kb} x ({g:g} ÷ {molar} ÷ {kg:g}) = {_f(_c(dt))} K.",
              f"স্ফুটনাঙ্কের বৃদ্ধি = Kb x মোলালিটি = {kb} x ({g:g} ÷ {molar} ÷ {kg:g}) = {_f(_c(dt))} K।",
              (dt / 2, kb * g / molar, dt * 3), " K")


def electron_wavelength(volts):
    lam = 1227 / math.sqrt(volts)
    return _n(f"An electron at rest is accelerated through {volts} V. What is its de Broglie wavelength?",
              f"স্থির একটা ইলেকট্রনকে {volts} V দিয়ে ত্বরিত করা হল। এর দ্য ব্রয় তরঙ্গদৈর্ঘ্য কত?", lam,
              f"λ = h ÷ √(2 m e V) ≈ 1227 ÷ √V pm = 1227 ÷ √{volts} = {_f(_c(lam))} pm - about the size of atoms, which is why electrons diffract from crystals.",
              f"λ = h ÷ √(2 m e V) ≈ 1227 ÷ √V pm = 1227 ÷ √{volts} = {_f(_c(lam))} pm - পরমাণুর মাপের, তাই কেলাসে ইলেকট্রনের অপবর্তন হয়।",
              (1227 / volts, lam / 2, lam * 1.41), " pm")


NUMERIC += [
    buffer_ph(4.74, 0.2, 0.1, "acetic acid", "অ্যাসিটিক অ্যাসিড"),
    buffer_ph(4.74, 0.1, 0.2, "acetic acid", "অ্যাসিটিক অ্যাসিড"),
    buffer_ph(3.75, 0.5, 0.05, "formic acid", "ফরমিক অ্যাসিড"),
    faraday_mass(2, 30, 63.5, 2, "copper", "তামা"),
    faraday_mass(5, 20, 108, 1, "silver", "রুপো"),
    faraday_mass(3, 60, 27, 3, "aluminium", "অ্যালুমিনিয়াম"),
    osmotic(18, 180, 1, 300, "glucose", "গ্লুকোজ"),
    osmotic(34.2, 342, 0.5, 300, "sucrose", "সুক্রোজ"),
    cell_density(4, 63.5, 361, "Copper", "তামা", "face-centred cubic", "মুখকেন্দ্রিক ঘনকীয়"),
    cell_density(2, 55.85, 287, "Iron", "লোহা", "body-centred cubic", "দেহকেন্দ্রিক ঘনকীয়"),
    cell_density(4, 58.5, 564, "Rock salt (NaCl)", "সাধারণ লবণ (NaCl)", "face-centred cubic", "মুখকেন্দ্রিক ঘনকীয়"),
    decay_left(5730, 11460, "years", "বছর", "Carbon-14", "কার্বন-14"),
    decay_left(8, 24, "days", "দিন", "Iodine-131 (used in thyroid treatment)", "আয়োডিন-131 (থাইরয়েড চিকিৎসায় ব্যবহৃত)"),
    transition_entropy(40.7, 373, "vaporisation of water", "জলের বাষ্পীভবন"),
    transition_entropy(6.01, 273, "fusion of ice", "বরফের গলন"),
    bp_elevation(0.52, 6, 60, 0.25, "urea", "ইউরিয়া", "water", "জল"),
    bp_elevation(2.53, 12.8, 128, 0.2, "naphthalene", "ন্যাপথালিন", "benzene", "বেঞ্জিন"),
    electron_wavelength(100), electron_wavelength(150), electron_wavelength(400),
]


CONCEPTS += [
    # ---------------------------------------------------------------- bonding and periodicity
    _q("What are the hybridisation of xenon and the shape of XeF₄?", ["sp³d², square planar", "sp³, tetrahedral", "sp³d, see-saw", "dsp², tetrahedral"],
       "Six electron pairs (4 bonds + 2 lone pairs) sit octahedrally; the lone pairs take opposite positions, leaving a square plane.",
       "জেনন টেট্রাফ্লুওরাইডে জেননের সংকরায়ণ আর অণুর আকৃতি কী?", ["sp³d², বর্গ-সমতলীয়", "sp³, চতুস্তলকীয়", "sp³d, ঢেঁকি-আকৃতি", "dsp², চতুস্তলকীয়"],
       "ছয় জোড়া ইলেকট্রন (4টি বন্ধন + 2টি নিঃসঙ্গ জোড়া) অষ্টতলকীয়ভাবে থাকে; নিঃসঙ্গ জোড়া দুটো বিপরীত দিকে, তাই বর্গ-সমতল থাকে।"),
    _q("According to molecular orbital theory, what is the bond order of O₂⁺?", ["2.5", "2", "1.5", "3"],
       "O₂ has bond order 2; removing one electron from an antibonding π* orbital raises it to (10 - 5) ÷ 2 = 2.5.",
       "আণবিক কক্ষক তত্ত্ব অনুযায়ী O₂⁺-এর বন্ধনক্রম কত?", ["2.5", "2", "1.5", "3"],
       "O₂-এর বন্ধনক্রম 2; একটা বন্ধনবিরোধী π* কক্ষক থেকে একটা ইলেকট্রন সরালে তা হয় (10 - 5) ÷ 2 = 2.5।"),
    _q("Which of these species is diamagnetic?", ["N₂", "O₂", "O₂⁻", "B₂"],
       "N₂ has all electrons paired; O₂, O₂⁻ and B₂ each keep unpaired electrons in degenerate π orbitals.",
       "এদের মধ্যে কোনটি তিরশ্চুম্বকীয়?", ["N₂", "O₂", "O₂⁻", "B₂"],
       "N₂-এর সব ইলেকট্রন জোড়বদ্ধ; O₂, O₂⁻ আর B₂-এর সমশক্তির π কক্ষকে অযুগ্ম ইলেকট্রন থাকে।"),
    _q("Which molecule has zero dipole moment even though its bonds are polar?", ["BF₃", "NH₃", "H₂O", "NF₃"],
       "In trigonal planar BF₃ the three B-F bond dipoles cancel; the pyramidal and bent molecules keep a net dipole.",
       "কোন অণুর বন্ধনগুলো পোলার হলেও দ্বিমেরু ভ্রামক শূন্য?", ["BF₃", "NH₃", "H₂O", "NF₃"],
       "ত্রিকোণী সমতলীয় BF₃-এ তিনটি B-F বন্ধনের দ্বিমেরু পরস্পরকে বাতিল করে; পিরামিডীয় আর বাঁকা অণুতে মোট দ্বিমেরু থাকে।"),
    _q("Why is BF₃ a weaker Lewis acid than BCl₃?", ["Strong pπ-pπ back-donation from fluorine eases boron's electron deficiency", "Fluorine is less electronegative than chlorine", "BF₃ is not planar", "B-F bonds are longer than B-Cl bonds"],
       "The small 2p orbitals of F overlap well with boron's empty 2p orbital; Cl's 3p overlaps poorly, so BCl₃ stays hungrier for electrons.",
       "BF₃ কেন BCl₃-এর চেয়ে দুর্বল লুইস অ্যাসিড?", ["ফ্লুওরিন থেকে জোরালো pπ-pπ পশ্চাৎ-দান বোরনের ইলেকট্রন-ঘাটতি কমায়", "ফ্লুওরিন ক্লোরিনের চেয়ে কম তড়িৎ-ঋণাত্মক", "BF₃ সমতলীয় নয়", "B-F বন্ধন B-Cl বন্ধনের চেয়ে লম্বা"],
       "F-এর ছোট 2p কক্ষক বোরনের খালি 2p কক্ষকের সঙ্গে ভালো মেলে; Cl-এর 3p ভালো মেলে না, তাই BCl₃ বেশি ইলেকট্রন-ক্ষুধার্ত থাকে।"),
    _q("Why is o-nitrophenol steam-volatile while p-nitrophenol is not?", ["o-Nitrophenol forms an intramolecular hydrogen bond, so its molecules do not associate", "o-Nitrophenol has a lower molar mass", "p-Nitrophenol is ionic", "o-Nitrophenol has no hydrogen bonds at all"],
       "The ortho -OH bonds to its own -NO₂ group; the para isomer links to neighbouring molecules, raising its boiling point.",
       "অর্থো-নাইট্রোফেনল বাষ্প-উদ্বায়ী কিন্তু প্যারা-নাইট্রোফেনল নয় কেন?", ["অর্থো যৌগে অন্তঃআণবিক হাইড্রোজেন বন্ধন হয়, তাই অণুগুলো জোট বাঁধে না", "অর্থো যৌগের মোলার ভর কম", "প্যারা যৌগ আয়নীয়", "অর্থো যৌগে কোনো হাইড্রোজেন বন্ধনই নেই"],
       "অর্থো -OH নিজের -NO₂ গ্রুপের সঙ্গেই বন্ধন করে; প্যারা সমাণু পাশের অণুর সঙ্গে যুক্ত হয়, তাই তার স্ফুটনাঙ্ক বেশি।"),
    _q("Why do zirconium and hafnium have almost the same atomic radius?", ["The lanthanoid contraction cancels the expected increase down the group", "They have the same number of electrons", "Both are noble gases", "Hafnium has fewer shells"],
       "The poorly shielding 4f electrons filled before Hf pull its outer shell in, so Zr (160 pm) and Hf (159 pm) are twins - and hard to separate.",
       "জারকোনিয়াম আর হাফনিয়ামের পারমাণবিক ব্যাসার্ধ প্রায় সমান কেন?", ["ল্যান্থানয়েড সংকোচন গ্রুপে নামার প্রত্যাশিত বৃদ্ধি বাতিল করে", "তাদের ইলেকট্রন-সংখ্যা সমান", "দুটোই নিষ্ক্রিয় গ্যাস", "হাফনিয়ামের কক্ষপথ কম"],
       "হাফনিয়ামের আগে ভরা 4f ইলেকট্রন ভালো আড়াল করে না, তাই বাইরের স্তর ভেতরে টানে; জারকোনিয়াম (160 pm) আর হাফনিয়াম (159 pm) প্রায় যমজ - আলাদা করাও কঠিন।"),
    _q("Why is Tl⁺ more stable than Tl³⁺?", ["The inert pair effect: the 6s² electrons resist taking part in bonding", "Thallium is a non-metal", "Tl³⁺ has a noble-gas configuration", "Thallium has no s electrons"],
       "Down group 13 the ns² pair is held tightly (poor d/f shielding), so the oxidation state two below the group value becomes more stable.",
       "Tl³⁺-এর চেয়ে Tl⁺ বেশি স্থায়ী কেন?", ["নিষ্ক্রিয় জোড় প্রভাব: 6s² ইলেকট্রন বন্ধনে অংশ নিতে চায় না", "থ্যালিয়াম অধাতু", "Tl³⁺-এর নিষ্ক্রিয় গ্যাসের বিন্যাস", "থ্যালিয়ামের কোনো s ইলেকট্রন নেই"],
       "গ্রুপ 13-এ নামলে ns² জোড়া শক্তভাবে ধরা থাকে (d/f-এর দুর্বল আড়াল), তাই গ্রুপ-মানের দুই কম জারণ অবস্থা বেশি স্থায়ী হয়।"),
    _q("Lithium resembles magnesium more than sodium in many properties. This is called…", ["The diagonal relationship", "The inert pair effect", "The lanthanoid contraction", "Isomorphism of alkali metals"],
       "Li⁺ and Mg²⁺ have similar charge-to-radius ratios: both form nitrides, covalent organometallics and carbonates that decompose on heating.",
       "অনেক ধর্মে লিথিয়াম সোডিয়ামের চেয়ে ম্যাগনেসিয়ামের মতো বেশি। একে বলে…", ["কর্ণ-সম্পর্ক", "নিষ্ক্রিয় জোড় প্রভাব", "ল্যান্থানয়েড সংকোচন", "ক্ষারধাতুর সমরূপতা"],
       "Li⁺ আর Mg²⁺-এর আধান-ব্যাসার্ধ অনুপাত কাছাকাছি: দুটোই নাইট্রাইড, সমযোজী জৈব-ধাতব যৌগ আর তাপে ভাঙা কার্বনেট তৈরি করে।"),
    _q("Why is water a liquid at room temperature while hydrogen sulphide, a heavier molecule, is a gas?", ["Water molecules are linked by strong hydrogen bonds", "H₂S is ionic", "Water has a higher molar mass", "Sulphur is more electronegative than oxygen"],
       "Small, very electronegative oxygen makes strong O-H···O hydrogen bonds; sulphur cannot, so H₂S boils at -60 °C.",
       "ঘরের তাপমাত্রায় জল তরল অথচ ভারী অণু হাইড্রোজেন সালফাইড গ্যাস কেন?", ["জলের অণুগুলো জোরালো হাইড্রোজেন বন্ধনে যুক্ত", "H₂S আয়নীয়", "জলের মোলার ভর বেশি", "সালফার অক্সিজেনের চেয়ে বেশি তড়িৎ-ঋণাত্মক"],
       "ছোট আর খুব তড়িৎ-ঋণাত্মক অক্সিজেন জোরালো O-H···O হাইড্রোজেন বন্ধন গড়ে; সালফার পারে না, তাই H₂S -60 °C-এ ফোটে।"),
    # ---------------------------------------------------------------- thermodynamics and equilibrium
    _q("A process is spontaneous at every temperature when…", ["ΔH is negative and ΔS is positive", "ΔH is positive and ΔS is negative", "Both ΔH and ΔS are positive", "Both ΔH and ΔS are negative"],
       "ΔG = ΔH - TΔS is then negative for every T; the mixed-sign cases depend on temperature.",
       "একটা প্রক্রিয়া সব তাপমাত্রায় স্বতঃস্ফূর্ত হয় যখন…", ["ΔH ঋণাত্মক আর ΔS ধনাত্মক", "ΔH ধনাত্মক আর ΔS ঋণাত্মক", "ΔH আর ΔS দুটোই ধনাত্মক", "ΔH আর ΔS দুটোই ঋণাত্মক"],
       "তখন ΔG = ΔH - TΔS প্রতিটি তাপমাত্রায় ঋণাত্মক; মিশ্র চিহ্নের ক্ষেত্রে ফল তাপমাত্রার ওপর নির্ভর করে।"),
    _q("For the isothermal expansion of an ideal gas, which quantity is zero?", ["ΔU (change in internal energy)", "Work done", "Heat absorbed", "ΔS (change in entropy)"],
       "The internal energy of an ideal gas depends only on temperature; with T fixed, q = -w and ΔU = 0.",
       "আদর্শ গ্যাসের সমোষ্ণ প্রসারণে কোন রাশি শূন্য?", ["ΔU (অন্তঃস্থ শক্তির পরিবর্তন)", "কৃতকার্য", "শোষিত তাপ", "ΔS (এনট্রপির পরিবর্তন)"],
       "আদর্শ গ্যাসের অন্তঃস্থ শক্তি কেবল তাপমাত্রার ওপর নির্ভর করে; তাপমাত্রা স্থির থাকলে q = -w আর ΔU = 0।"),
    _q("For N₂ + 3H₂ ⇌ 2NH₃ (exothermic), which change increases the yield of ammonia at equilibrium?", ["Raising the pressure", "Raising the temperature", "Adding a catalyst", "Removing nitrogen"],
       "Four moles of gas become two, so higher pressure pushes the equilibrium right; heat pushes it left, and a catalyst only speeds the approach.",
       "N₂ + 3H₂ ⇌ 2NH₃ (তাপমোচী) বিক্রিয়ায় কোন পরিবর্তন সাম্যে অ্যামোনিয়ার উৎপাদন বাড়ায়?", ["চাপ বাড়ানো", "তাপমাত্রা বাড়ানো", "অনুঘটক যোগ", "নাইট্রোজেন সরানো"],
       "চার মোল গ্যাস দুই মোল হয়, তাই বেশি চাপ সাম্যকে ডানে ঠেলে; তাপ বাঁয়ে ঠেলে, আর অনুঘটক কেবল সাম্যে পৌঁছনো দ্রুত করে।"),
    _q("An inert gas is added to an equilibrium mixture at constant volume. What happens?", ["Nothing: the partial pressures, and so the equilibrium, are unchanged", "It shifts towards fewer gas moles", "It shifts towards more gas moles", "The equilibrium constant doubles"],
       "Total pressure rises, but each reacting gas keeps the same concentration; at constant pressure, by contrast, the mixture would dilute.",
       "স্থির আয়তনে সাম্য-মিশ্রণে একটা নিষ্ক্রিয় গ্যাস যোগ করা হল। কী ঘটে?", ["কিছুই না: আংশিক চাপ, তাই সাম্যও অপরিবর্তিত", "কম গ্যাস-মোলের দিকে সরে", "বেশি গ্যাস-মোলের দিকে সরে", "সাম্য-ধ্রুবক দ্বিগুণ হয়"],
       "মোট চাপ বাড়ে, কিন্তু প্রতিটি বিক্রিয়ক গ্যাসের ঘনত্ব একই থাকে; স্থির চাপে হলে অবশ্য মিশ্রণ লঘু হত।"),
    # ---------------------------------------------------------------- kinetics and electrochemistry
    _q("The molecularity of an elementary reaction can never be…", ["Zero or a fraction", "One", "Two", "Three"],
       "Molecularity counts the molecules colliding in one step, so it is a small whole number; order, found by experiment, can be 0 or fractional.",
       "একটা প্রাথমিক বিক্রিয়ার আণবিকতা কখনো হতে পারে না…", ["শূন্য বা ভগ্নাংশ", "এক", "দুই", "তিন"],
       "আণবিকতা এক ধাপে সংঘর্ষে যাওয়া অণুর সংখ্যা, তাই ছোট পূর্ণসংখ্যা; পরীক্ষায় পাওয়া ক্রম অবশ্য 0 বা ভগ্নাংশ হতে পারে।"),
    _q("What are the units of the rate constant of a second-order reaction?", ["L mol⁻¹ s⁻¹", "s⁻¹", "mol L⁻¹ s⁻¹", "L² mol⁻² s⁻¹"],
       "Rate = k[A]², so k = (mol L⁻¹ s⁻¹) ÷ (mol L⁻¹)² = L mol⁻¹ s⁻¹.",
       "দ্বিতীয় ক্রমের বিক্রিয়ার হার-ধ্রুবকের একক কী?", ["L মোল⁻¹ s⁻¹", "s⁻¹", "মোল L⁻¹ s⁻¹", "L² মোল⁻² s⁻¹"],
       "হার = k[A]², তাই k = (মোল L⁻¹ s⁻¹) ÷ (মোল L⁻¹)² = L মোল⁻¹ s⁻¹।"),
    _q("Which electrode is assigned a standard potential of exactly 0 V?", ["The standard hydrogen electrode", "The calomel electrode", "The silver-silver chloride electrode", "The glass electrode"],
       "Pt | H₂ (1 bar) | H⁺ (1 M) is the agreed zero against which every other E° is measured.",
       "কোন তড়িৎদ্বারের প্রমাণ বিভব ঠিক 0 V ধরা হয়?", ["প্রমাণ হাইড্রোজেন তড়িৎদ্বার", "ক্যালোমেল তড়িৎদ্বার", "সিলভার-সিলভার ক্লোরাইড তড়িৎদ্বার", "কাচ তড়িৎদ্বার"],
       "Pt | H₂ (1 বার) | H⁺ (1 M) হল সর্বসম্মত শূন্য, যার সাপেক্ষে বাকি সব প্রমাণ বিভব মাপা হয়।"),
    _q("A zinc block bolted to a steel ship's hull protects it from rusting because…", ["Zinc is more easily oxidised and corrodes in place of iron (sacrificial protection)", "Zinc makes the hull waterproof", "Zinc reduces the water", "Zinc is less reactive than iron"],
       "Zinc (E° = -0.76 V) becomes the anode and iron the cathode, so the zinc is eaten and the hull is spared - the blocks are replaced at docking.",
       "ইস্পাতের জাহাজের খোলে লাগানো দস্তার ব্লক মরচে থেকে রক্ষা করে কারণ…", ["দস্তা সহজে জারিত হয় আর লোহার বদলে নিজে ক্ষয় হয় (আত্মত্যাগী সুরক্ষা)", "দস্তা খোলকে জলরোধী করে", "দস্তা জলকে বিজারিত করে", "দস্তা লোহার চেয়ে কম সক্রিয়"],
       "দস্তা (E° = -0.76 V) অ্যানোড আর লোহা ক্যাথোড হয়, তাই দস্তা ক্ষয় হয় আর খোল বাঁচে - বন্দরে ব্লক বদলানো হয়।"),
    _q("What is the only product of a hydrogen-oxygen fuel cell?", ["Water", "Carbon dioxide", "Hydrogen peroxide", "Ozone"],
       "2H₂ + O₂ → 2H₂O; the energy comes out directly as electricity, at about 60-70% efficiency - used in spacecraft.",
       "হাইড্রোজেন-অক্সিজেন জ্বালানি কোষের একমাত্র উৎপাদ কী?", ["জল", "কার্বন ডাইঅক্সাইড", "হাইড্রোজেন পারক্সাইড", "ওজোন"],
       "2H₂ + O₂ → 2H₂O; শক্তি সরাসরি বিদ্যুৎ হিসেবে বেরোয়, প্রায় 60-70% দক্ষতায় - মহাকাশযানে ব্যবহৃত।"),
    # ---------------------------------------------------------------- solids, solutions and surfaces
    _q("What is the coordination number of each ion in the caesium chloride structure?", ["8", "6", "4", "12"],
       "Cs⁺ sits at the body centre of a cube of 8 Cl⁻ ions (and vice versa), possible because the radius ratio exceeds 0.732.",
       "সিজিয়াম ক্লোরাইড গঠনে প্রতিটি আয়নের সন্নিবেশ সংখ্যা কত?", ["8", "6", "4", "12"],
       "Cs⁺ আটটি Cl⁻ আয়নের ঘনকের দেহকেন্দ্রে বসে (আর উল্টোটাও), কারণ ব্যাসার্ধ-অনুপাত 0.732-এর বেশি।"),
    _q("What fraction of space is filled in a cubic close-packed (fcc) lattice?", ["74%", "68%", "52%", "100%"],
       "Four atoms of radius r in a cube of edge 2√2 r fill π ÷ (3√2) ≈ 0.74 of it; bcc fills 68% and simple cubic 52%.",
       "ঘনকীয় ঘন-সংকুলিত (মুখকেন্দ্রিক) জালিকায় কত অংশ স্থান ভরা থাকে?", ["74%", "68%", "52%", "100%"],
       "2√2 r ধারের ঘনকে r ব্যাসার্ধের চারটি পরমাণু π ÷ (3√2) ≈ 0.74 অংশ ভরায়; দেহকেন্দ্রিক 68% আর সরল ঘনক 52% ভরায়।"),
    _q("Which 0.1 molal aqueous solution has the highest boiling point?", ["Aluminium sulphate", "Sodium chloride", "Glucose", "Urea"],
       "Al₂(SO₄)₃ gives up to 5 ions per formula unit (i ≈ 5), NaCl 2, and the two molecular solutes 1.",
       "কোন 0.1 মোলাল জলীয় দ্রবণের স্ফুটনাঙ্ক সবচেয়ে বেশি?", ["অ্যালুমিনিয়াম সালফেট", "সোডিয়াম ক্লোরাইড", "গ্লুকোজ", "ইউরিয়া"],
       "Al₂(SO₄)₃ প্রতি সংকেত-এককে 5টি পর্যন্ত আয়ন দেয় (i ≈ 5), NaCl 2টি, আর আণবিক দ্রাব দুটো 1টি।"),
    _q("What is an azeotrope?", ["A liquid mixture that boils at constant temperature with vapour of the same composition", "A solution that obeys Raoult's law exactly", "A mixture of two solids", "A colloid of gas in liquid"],
       "95.6% ethanol-water is one: distillation cannot purify it further, so absolute alcohol needs other methods.",
       "অ্যাজিওট্রোপ কী?", ["এমন তরল মিশ্রণ যা স্থির তাপমাত্রায় ফোটে আর বাষ্পের গঠন তরলের সমান", "যে দ্রবণ রাউল্টের সূত্র হুবহু মানে", "দুটি কঠিনের মিশ্রণ", "তরলে গ্যাসের কলয়েড"],
       "95.6% ইথানল-জল এমন মিশ্রণ: পাতনে আর বিশুদ্ধ হয় না, তাই নির্জল অ্যালকোহলের জন্য অন্য পদ্ধতি লাগে।"),
    _q("A beam of light becomes visible as it passes through a colloid but not through a true solution. This is the…", ["Tyndall effect", "Brownian motion", "Electrophoresis", "Peptisation"],
       "Colloidal particles (1-1000 nm) scatter light; dissolved ions and molecules are too small - the same reason sunbeams show in dusty air.",
       "আলোর রশ্মি কলয়েডের মধ্য দিয়ে গেলে দেখা যায়, প্রকৃত দ্রবণে যায় না। এটা হল…", ["টিন্ডাল প্রভাব", "ব্রাউনীয় গতি", "তড়িৎ-কণা সঞ্চালন", "পেপটাইজেশন"],
       "কলয়েড কণা (1-1000 nm) আলো বিক্ষিপ্ত করে; দ্রবীভূত আয়ন আর অণু খুব ছোট - ধুলোভরা বাতাসে সূর্যরশ্মি দেখা যাওয়ার একই কারণ।"),
    _q("Which ion coagulates a negatively charged arsenic sulphide sol most effectively?", ["Al³⁺", "Ba²⁺", "Na⁺", "Cl⁻"],
       "Hardy-Schulze rule: the higher the charge of the oppositely charged ion, the greater its coagulating power.",
       "ঋণাত্মক আধানের আর্সেনিক সালফাইড সলকে কোন আয়ন সবচেয়ে কার্যকরভাবে তঞ্চিত করে?", ["Al³⁺", "Ba²⁺", "Na⁺", "Cl⁻"],
       "হার্ডি-শুলৎজ নিয়ম: বিপরীত আধানের আয়নের আধান যত বেশি, তঞ্চন-ক্ষমতা তত বেশি।"),
    # ---------------------------------------------------------------- atomic structure
    _q("How many orbitals are there in the shell with principal quantum number n = 3?", ["9", "3", "18", "6"],
       "n² orbitals: one 3s, three 3p and five 3d = 9, holding up to 18 electrons.",
       "মুখ্য কোয়ান্টাম সংখ্যা n = 3 স্তরে কয়টি কক্ষক আছে?", ["9", "3", "18", "6"],
       "n²টি কক্ষক: একটি 3s, তিনটি 3p আর পাঁচটি 3d = 9, যাতে 18টি পর্যন্ত ইলেকট্রন থাকে।"),
    _q("What is the ground-state electron configuration of chromium (Z = 24)?", ["[Ar] 3d⁵ 4s¹", "[Ar] 3d⁴ 4s²", "[Ar] 3d⁶", "[Ar] 4s² 4p⁴"],
       "A half-filled d subshell has extra exchange stability, so one 4s electron moves to 3d (copper does the same: 3d¹⁰ 4s¹).",
       "ক্রোমিয়ামের (Z = 24) ভূমি-অবস্থার ইলেকট্রন বিন্যাস কী?", ["[Ar] 3d⁵ 4s¹", "[Ar] 3d⁴ 4s²", "[Ar] 3d⁶", "[Ar] 4s² 4p⁴"],
       "অর্ধপূর্ণ d উপস্তরের বিনিময়-স্থায়িত্ব বেশি, তাই একটা 4s ইলেকট্রন 3d-তে যায় (তামাও তাই করে: 3d¹⁰ 4s¹)।"),
    _q("In the photoelectric effect, the maximum kinetic energy of the ejected electrons depends on…", ["The frequency of the light, not its intensity", "The intensity of the light only", "The area of the metal plate", "How long the light shines"],
       "KE = hν - φ: brighter light ejects more electrons, but only higher frequency makes them faster - Einstein's evidence for photons.",
       "আলোক-তড়িৎ ক্রিয়ায় নির্গত ইলেকট্রনের সর্বোচ্চ গতিশক্তি নির্ভর করে…", ["আলোর কম্পাঙ্কের ওপর, তীব্রতার ওপর নয়", "কেবল আলোর তীব্রতার ওপর", "ধাতব পাতের ক্ষেত্রফলের ওপর", "কতক্ষণ আলো পড়ে তার ওপর"],
       "গতিশক্তি = hν - φ: উজ্জ্বল আলো বেশি ইলেকট্রন বের করে, কিন্তু কেবল বেশি কম্পাঙ্ক তাদের দ্রুততর করে - ফোটনের পক্ষে আইনস্টাইনের প্রমাণ।"),
    # ---------------------------------------------------------------- coordination chemistry
    _q("What is the IUPAC name of K₃[Fe(CN)₆]?", ["Potassium hexacyanidoferrate(III)", "Potassium hexacyanidoiron(II)", "Tripotassium iron cyanide", "Potassium ferrocyanide(II)"],
       "Ligands first (hexacyanido), then the metal with -ate because the complex is an anion (ferrate), then its oxidation state: 3 K⁺ balance [Fe(CN)₆]³⁻, so Fe is +3.",
       "K₃[Fe(CN)₆]-এর আইইউপিএসি নাম কী?", ["পটাশিয়াম হেক্সাসায়ানিডোফেরেট(III)", "পটাশিয়াম হেক্সাসায়ানিডোআয়রন(II)", "ট্রাইপটাশিয়াম আয়রন সায়ানাইড", "পটাশিয়াম ফেরোসায়ানাইড(II)"],
       "আগে লিগ্যান্ড (হেক্সাসায়ানিডো), তারপর ধাতু - জটিল আয়নটি ঋণাত্মক বলে -এট (ফেরেট), তারপর জারণ অবস্থা: 3টি K⁺ [Fe(CN)₆]³⁻-কে প্রশমিত করে, তাই Fe-এর +3।"),
    _q("How many geometrical isomers does square-planar [Pt(NH₃)₂Cl₂] have?", ["2 (cis and trans)", "1", "3", "4"],
       "The two Cl can be neighbours (cis - the anticancer drug cisplatin) or opposite (trans); a tetrahedral complex would have none.",
       "বর্গ-সমতলীয় [Pt(NH₃)₂Cl₂]-এর কয়টি জ্যামিতিক সমাণু আছে?", ["2টি (সিস আর ট্রান্স)", "1টি", "3টি", "4টি"],
       "দুটি Cl পাশাপাশি (সিস - ক্যানসার-রোধী ওষুধ সিসপ্ল্যাটিন) বা বিপরীতে (ট্রান্স) থাকতে পারে; চতুস্তলকীয় জটিলের কোনো সমাণু হত না।"),
    _q("What is the spin-only magnetic moment of [Fe(CN)₆]³⁻?", ["About 1.73 BM (one unpaired electron)", "About 5.92 BM", "Zero", "About 3.87 BM"],
       "Fe³⁺ is d⁵; strong-field CN⁻ pairs four of them in t₂g, leaving one unpaired: μ = √(n(n+2)) = √3 ≈ 1.73 BM.",
       "[Fe(CN)₆]³⁻-এর কেবল-স্পিন চৌম্বক ভ্রামক কত?", ["প্রায় 1.73 বোর ম্যাগনেটন (একটি অযুগ্ম ইলেকট্রন)", "প্রায় 5.92 বোর ম্যাগনেটন", "শূন্য", "প্রায় 3.87 বোর ম্যাগনেটন"],
       "Fe³⁺ হল d⁵; প্রবল-ক্ষেত্রের CN⁻ t₂g-তে চারটিকে জোড়বদ্ধ করে, একটি অযুগ্ম থাকে: μ = √(n(n+2)) = √3 ≈ 1.73।"),
    _q("Which ligand produces the largest crystal field splitting?", ["CO", "I⁻", "Cl⁻", "H₂O"],
       "Spectrochemical series: I⁻ < Br⁻ < Cl⁻ < F⁻ < H₂O < NH₃ < en < CN⁻ < CO; π-acceptor CO splits the d orbitals most.",
       "কোন লিগ্যান্ড সবচেয়ে বড় কেলাস-ক্ষেত্র বিভাজন ঘটায়?", ["কার্বন মনোক্সাইড (CO)", "I⁻", "Cl⁻", "H₂O"],
       "বর্ণালি-রাসায়নিক শ্রেণি: I⁻ < Br⁻ < Cl⁻ < F⁻ < H₂O < NH₃ < en < CN⁻ < CO; π-গ্রাহক CO সবচেয়ে বেশি বিভাজন ঘটায়।"),
    # ---------------------------------------------------------------- organic chemistry
    _q("Propene reacts with HBr in the presence of a peroxide. What is the main product?", ["1-Bromopropane (anti-Markovnikov)", "2-Bromopropane", "1,2-Dibromopropane", "Propane"],
       "Peroxides start a free-radical chain; Br· adds to the end carbon to give the more stable secondary radical. Only HBr shows this effect.",
       "পারক্সাইডের উপস্থিতিতে প্রোপিন HBr-এর সঙ্গে বিক্রিয়া করে। প্রধান উৎপাদ কী?", ["1-ব্রোমোপ্রোপেন (মারকনিকভ-বিরোধী)", "2-ব্রোমোপ্রোপেন", "1,2-ডাইব্রোমোপ্রোপেন", "প্রোপেন"],
       "পারক্সাইড মুক্ত-মূলক শৃঙ্খল শুরু করে; Br· প্রান্তের কার্বনে যুক্ত হয়ে বেশি স্থায়ী দ্বিতীয়ক মূলক দেয়। কেবল HBr-এ এই প্রভাব দেখা যায়।"),
    _q("What does ozonolysis of but-2-ene (followed by Zn and water) give?", ["Two molecules of acetaldehyde", "One molecule of acetone", "Formaldehyde and propanal", "Butanoic acid"],
       "The C=C is cut in two and each half becomes C=O: CH₃CH=CHCH₃ → 2 CH₃CHO. Ozonolysis locates double bonds.",
       "বিউট-2-ইনের ওজোনবিশ্লেষণ (পরে Zn আর জল) কী দেয়?", ["দুই অণু অ্যাসিট্যালডিহাইড", "এক অণু অ্যাসিটোন", "ফরমালডিহাইড আর প্রোপানাল", "বিউটানোয়িক অ্যাসিড"],
       "C=C দুই ভাগ হয় আর প্রতিটি অর্ধেক C=O হয়: CH₃CH=CHCH₃ → 2 CH₃CHO। ওজোনবিশ্লেষণ দ্বিবন্ধনের অবস্থান জানায়।"),
    _q("Which species is aromatic?", ["The cyclopentadienyl anion", "Cyclooctatetraene (tub-shaped)", "The cyclopentadienyl cation", "Cyclohexene"],
       "It is cyclic, planar and fully conjugated with 6 π electrons (4n + 2, n = 1); the cation has 4 and is antiaromatic.",
       "কোনটি অ্যারোমেটিক?", ["সাইক্লোপেন্টাডাইইনাইল অ্যানায়ন", "সাইক্লোঅক্টাটেট্রাইন (টব-আকৃতি)", "সাইক্লোপেন্টাডাইইনাইল ক্যাটায়ন", "সাইক্লোহেক্সিন"],
       "এটা চক্রীয়, সমতলীয়, সম্পূর্ণ সংযুগ্মিত আর এতে 6টি π ইলেকট্রন (4n + 2, n = 1); ক্যাটায়নে 4টি, তাই সেটা অ্যান্টিঅ্যারোমেটিক।"),
    _q("Why is meso-tartaric acid optically inactive although it has two chiral carbons?", ["An internal plane of symmetry makes it superimposable on its mirror image", "It has no chiral carbons", "It is a racemic mixture", "It does not dissolve in water"],
       "The two halves rotate light equally in opposite directions within one molecule; a racemic mixture, by contrast, is two different molecules.",
       "দুটি কাইরাল কার্বন থাকলেও মেসো-টারটারিক অ্যাসিড আলোক-নিষ্ক্রিয় কেন?", ["অভ্যন্তরীণ প্রতিসাম্য-তল একে দর্পণ-প্রতিবিম্বের সঙ্গে মিলিয়ে দেয়", "এতে কোনো কাইরাল কার্বন নেই", "এটা রেসেমিক মিশ্রণ", "এটা জলে দ্রবীভূত হয় না"],
       "একই অণুর দুই অর্ধেক আলোকে সমান কিন্তু বিপরীত দিকে ঘোরায়; রেসেমিক মিশ্রণ অবশ্য দুটি আলাদা অণু।"),
    _q("How many stereoisomers does 2,3-dibromobutane have?", ["3 (a pair of enantiomers and one meso form)", "4", "2", "1"],
       "Two chiral centres would allow 2² = 4, but the identical ends make the (2R,3S) form meso, so only 3 exist.",
       "2,3-ডাইব্রোমোবিউটেনের কয়টি ত্রিমাত্রিক সমাণু আছে?", ["3টি (এক জোড়া এনানশিওমার আর একটি মেসো রূপ)", "4টি", "2টি", "1টি"],
       "দুটি কাইরাল কেন্দ্রে 2² = 4টি হতে পারত, কিন্তু দুই প্রান্ত একই বলে (2R,3S) রূপটি মেসো, তাই কেবল 3টি।"),
    _q("Treating an amide with bromine and aqueous NaOH gives…", ["A primary amine with one carbon fewer (Hofmann bromamide degradation)", "A nitrile", "An amine with one carbon more", "A carboxylic acid with the same carbons"],
       "RCONH₂ → RNH₂ via an isocyanate; e.g. acetamide gives methylamine.",
       "একটা অ্যামাইডকে ব্রোমিন আর জলীয় NaOH দিয়ে বিক্রিয়া করালে পাওয়া যায়…", ["এক কার্বন কম মুখ্য অ্যামিন (হফম্যান ব্রোমাইড অবক্ষয়)", "একটা নাইট্রাইল", "এক কার্বন বেশি অ্যামিন", "একই কার্বনের কার্বক্সিলিক অ্যাসিড"],
       "RCONH₂ → RNH₂, একটা আইসোসায়ানেটের মধ্য দিয়ে; যেমন অ্যাসিটামাইড থেকে মিথাইলঅ্যামিন।"),
    _q("A primary amine warmed with chloroform and alcoholic KOH gives an offensive smell. Which test is this?", ["The carbylamine (isocyanide) test", "The Lucas test", "Tollens' test", "The iodoform test"],
       "RNH₂ + CHCl₃ + 3KOH → RNC (isocyanide); secondary and tertiary amines do not respond.",
       "মুখ্য অ্যামিনকে ক্লোরোফর্ম আর অ্যালকোহলীয় KOH-এর সঙ্গে গরম করলে বিশ্রী গন্ধ বেরোয়। এটা কোন পরীক্ষা?", ["কার্বিলঅ্যামিন (আইসোসায়ানাইড) পরীক্ষা", "লুকাস পরীক্ষা", "টলেন্সের পরীক্ষা", "আয়োডোফর্ম পরীক্ষা"],
       "RNH₂ + CHCl₃ + 3KOH → RNC (আইসোসায়ানাইড); গৌণ আর প্রগৌণ অ্যামিন সাড়া দেয় না।"),
    _q("Which reagent is used to tell primary, secondary and tertiary amines apart?", ["Benzenesulphonyl chloride (Hinsberg's reagent)", "Fehling's solution", "Bromine water", "Baeyer's reagent"],
       "Primary amines give a sulphonamide soluble in alkali, secondary give an insoluble one, tertiary do not react.",
       "মুখ্য, গৌণ আর প্রগৌণ অ্যামিন আলাদা করতে কোন বিকারক ব্যবহার হয়?", ["বেঞ্জিনসালফোনাইল ক্লোরাইড (হিন্সবার্গের বিকারক)", "ফেলিংয়ের দ্রবণ", "ব্রোমিন জল", "বেয়ারের বিকারক"],
       "মুখ্য অ্যামিন ক্ষারে দ্রাব্য সালফোনামাইড দেয়, গৌণ অদ্রাব্য দেয়, প্রগৌণ বিক্রিয়া করে না।"),
    _q("Why does nitrobenzene not undergo Friedel-Crafts alkylation?", ["The -NO₂ group strongly deactivates the ring towards electrophiles", "Nitrobenzene is not aromatic", "AlCl₃ does not dissolve in it", "It is too reactive and explodes"],
       "The nitro group pulls electron density out of the ring, so the weak carbocation electrophile cannot attack - nitrobenzene is even used as a solvent for these reactions.",
       "নাইট্রোবেঞ্জিনে ফ্রিডেল-ক্রাফটস অ্যালকিলেশন হয় না কেন?", ["-NO₂ গ্রুপ বলয়কে ইলেকট্রনাকর্ষীদের প্রতি খুব নিষ্ক্রিয় করে", "নাইট্রোবেঞ্জিন অ্যারোমেটিক নয়", "এতে AlCl₃ গলে না", "এটা অতিসক্রিয় আর বিস্ফোরণ ঘটায়"],
       "নাইট্রো গ্রুপ বলয় থেকে ইলেকট্রন টেনে নেয়, তাই দুর্বল কার্বোক্যাটায়ন আক্রমণ করতে পারে না - এমনকি এই বিক্রিয়ার দ্রাবক হিসেবেও নাইট্রোবেঞ্জিন ব্যবহৃত হয়।"),
    _q("Nitration of nitrobenzene mainly gives which dinitrobenzene?", ["The meta isomer", "The ortho isomer", "The para isomer", "Equal amounts of all three"],
       "-NO₂ withdraws electrons by resonance most strongly from the ortho and para positions, leaving meta the least deactivated.",
       "নাইট্রোবেঞ্জিনের নাইট্রেশনে প্রধানত কোন ডাইনাইট্রোবেঞ্জিন পাওয়া যায়?", ["মেটা সমাণু", "অর্থো সমাণু", "প্যারা সমাণু", "তিনটিই সমান পরিমাণে"],
       "-NO₂ অনুরণনে অর্থো আর প্যারা অবস্থান থেকে সবচেয়ে বেশি ইলেকট্রন টানে, তাই মেটা সবচেয়ে কম নিষ্ক্রিয় থাকে।"),
    _q("Which carbonyl compound cannot undergo aldol condensation?", ["Formaldehyde", "Acetaldehyde", "Acetone", "Propanal"],
       "Aldol needs an α-hydrogen to form the enolate; HCHO has no α-carbon at all.",
       "কোন কার্বনিল যৌগে অ্যালডল ঘনীভবন হয় না?", ["ফরমালডিহাইড", "অ্যাসিট্যালডিহাইড", "অ্যাসিটোন", "প্রোপানাল"],
       "অ্যালডলের জন্য এনোলেট গড়তে α-হাইড্রোজেন লাগে; ফরমালডিহাইডে কোনো α-কার্বনই নেই।"),
    _q("Which reagent reduces a ketone's C=O to CH₂ under acidic conditions?", ["Zinc amalgam and concentrated HCl (Clemmensen reduction)", "LiAlH₄ in ether", "NaBH₄ in methanol", "Hydrazine and KOH"],
       "Clemmensen works in acid; Wolff-Kishner (hydrazine/KOH) does the same job in base. LiAlH₄ and NaBH₄ stop at the alcohol.",
       "অম্লীয় অবস্থায় কোন বিকারক কিটোনের C=O-কে CH₂-তে বিজারিত করে?", ["জিঙ্ক অ্যামালগাম আর গাঢ় HCl (ক্লেমেনসেন বিজারণ)", "ইথারে LiAlH₄", "মিথানলে NaBH₄", "হাইড্রাজিন আর KOH"],
       "ক্লেমেনসেন অম্লে কাজ করে; উলফ-কিশনার (হাইড্রাজিন/KOH) একই কাজ করে ক্ষারে। LiAlH₄ আর NaBH₄ অ্যালকোহলে থেমে যায়।"),
    # ---------------------------------------------------------------- biomolecules and polymers
    _q("How many hydrogen bonds join a guanine-cytosine base pair in DNA?", ["3", "2", "1", "4"],
       "G≡C has three, A=T two - so GC-rich DNA needs a higher temperature to separate its strands.",
       "ডিএনএ-তে গুয়ানিন-সাইটোসিন ক্ষারক-জোড়া কয়টি হাইড্রোজেন বন্ধনে যুক্ত?", ["3", "2", "1", "4"],
       "G≡C-তে তিনটি, A=T-তে দুটি - তাই বেশি GC-যুক্ত ডিএনএ-র সূত্র আলাদা করতে বেশি তাপমাত্রা লাগে।"),
    _q("Which vitamin is fat-soluble and can be stored in the body?", ["Vitamin D", "Vitamin C", "Vitamin B₁", "Vitamin B₁₂"],
       "Vitamins A, D, E and K dissolve in fat and are stored in the liver and fatty tissue; B and C dissolve in water and are excreted.",
       "কোন ভিটামিন চর্বিতে দ্রাব্য আর দেহে জমা থাকতে পারে?", ["ভিটামিন ডি", "ভিটামিন সি", "ভিটামিন বি₁", "ভিটামিন বি₁₂"],
       "ভিটামিন এ, ডি, ই আর কে চর্বিতে গলে, যকৃৎ আর চর্বি-কলায় জমে; বি আর সি জলে গলে, প্রস্রাবে বেরিয়ে যায়।"),
    _q("Which two monomers condense, losing water, to form the amide links of nylon-6,6?", ["Hexamethylenediamine and adipic acid", "Caprolactam alone", "Ethylene glycol and terephthalic acid", "Phenol and formaldehyde"],
       "Each monomer has 6 carbons, hence '6,6'; they join by condensation, losing water to form amide links.",
       "কোন দুটি মনোমার জল বের করে ঘনীভূত হয়ে নাইলন-6,6-এর অ্যামাইড বন্ধন গড়ে?", ["হেক্সামিথিলিনডাইঅ্যামিন আর অ্যাডিপিক অ্যাসিড", "কেবল ক্যাপ্রোল্যাকটাম", "ইথিলিন গ্লাইকল আর টেরেফথ্যালিক অ্যাসিড", "ফেনল আর ফরমালডিহাইড"],
       "প্রতিটি মনোমারে 6টি কার্বন, তাই '6,6'; জল বের করে ঘনীভবনে অ্যামাইড বন্ধনে যুক্ত হয়।"),
    _q("Why is natural rubber vulcanised with sulphur?", ["Sulphur cross-links the cis-polyisoprene chains, making rubber stronger and less sticky", "To make it dissolve in water", "To turn it into a thermosetting plastic powder", "To remove its double bonds completely"],
       "S-S bridges between chains stop them sliding past each other: tyres keep their shape from cold winters to hot roads.",
       "প্রাকৃতিক রাবারকে সালফার দিয়ে ভালকানাইজ করা হয় কেন?", ["সালফার সিস-পলিআইসোপ্রিন শৃঙ্খলগুলোকে আড়াআড়ি জোড়ে, তাই রাবার শক্ত আর কম চটচটে হয়", "জলে দ্রবীভূত করতে", "তাপ-দৃঢ় প্লাস্টিকের গুঁড়ো বানাতে", "সব দ্বিবন্ধন পুরোপুরি সরাতে"],
       "শৃঙ্খলের মাঝে S-S সেতু তাদের একে অপরের ওপর পিছলে যেতে দেয় না: শীতের ঠান্ডা থেকে গরম রাস্তায় টায়ার আকার ধরে রাখে।"),
]


ITEMS = tuple(NUMERIC + CONCEPTS)
