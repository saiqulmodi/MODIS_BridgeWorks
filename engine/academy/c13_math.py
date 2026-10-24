"""NIT level - Mathematics (JEE Main standard): sets and functions, complex numbers, quadratic
equations, sequences and series, permutations and combinations, the binomial theorem, matrices and
determinants, limits, derivatives and their applications, integrals and areas, differential
equations, straight lines and conic sections, vectors and 3-D geometry, probability, statistics,
trigonometry and mathematical reasoning."""
import math
from fractions import Fraction as F

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


def _fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def _fr(q_en, q_bn, r, alts, ex_en, ex_bn):
    """A fraction answer such as 5/36, with distinct fraction distractors."""
    out = []
    for x in (r, *alts, r * 2, r / 2, 1 - r, r + F(1, 6)):
        x = F(x)
        if x > 0 and x not in out:
            out.append(x)
    opts = [_fs(x) for x in out[:4]]
    return mcq(q_en, opts, 0, ex_en, q_bn, opts, ex_bn)


def _s(q_en, opts, ex_en, q_bn, ex_bn, opts_bn=None):
    return mcq(q_en, opts, 0, ex_en, q_bn, opts_bn or opts, ex_bn)


# ---------------------------------------------------------------- algebra
def ap_term(a, d, n):
    t = a + (n - 1) * d
    return _n(f"An arithmetic progression starts {a}, {a + d}, {a + 2 * d}, ... What is its {n}th term?",
              f"একটা সমান্তর প্রগতি {a}, {a + d}, {a + 2 * d}, ... দিয়ে শুরু। এর {n}-তম পদ কত?", t,
              f"aₙ = a + (n - 1)d = {a} + {n - 1} x {d} = {t}.",
              f"n-তম পদ = a + (n - 1)d = {a} + {n - 1} x {d} = {t}।",
              (a + n * d, a * n, t - d))


def ap_sum(a, d, n):
    s = n * (2 * a + (n - 1) * d) // 2
    return _n(f"What is the sum of the first {n} terms of the AP {a}, {a + d}, {a + 2 * d}, ...?",
              f"সমান্তর প্রগতি {a}, {a + d}, {a + 2 * d}, ...-এর প্রথম {n}টি পদের যোগফল কত?", s,
              f"Sₙ = n/2 [2a + (n - 1)d] = {n}/2 x [{2 * a} + {(n - 1) * d}] = {s}.",
              f"যোগফল = n/2 [2a + (n - 1)d] = {n}/2 x [{2 * a} + {(n - 1) * d}] = {s}।",
              (n * (a + (n - 1) * d), s - a, s + d))


def gp_inf(a, num, den):
    r = F(num, den)
    s = F(a) / (1 - r)
    return _fr(f"What is the sum to infinity of the geometric series {a} + {_fs(a * r)} + {_fs(a * r * r)} + ...?",
               f"অসীম গুণোত্তর শ্রেণি {a} + {_fs(a * r)} + {_fs(a * r * r)} + ...-এর যোগফল কত?", s,
               (F(a) / (1 + r), F(a) * (1 + r), s + 1),
               f"r = {_fs(r)}, |r| < 1, so S∞ = a ÷ (1 - r) = {a} ÷ {_fs(1 - r)} = {_fs(s)}.",
               f"সাধারণ অনুপাত {_fs(r)}, |r| < 1, তাই অসীম যোগফল = a ÷ (1 - r) = {a} ÷ {_fs(1 - r)} = {_fs(s)}।")


def series_sum(kind, n):
    if kind == "sq":
        s = n * (n + 1) * (2 * n + 1) // 6
        en, bn, f_ = f"1² + 2² + ... + {n}²", f"1² + 2² + ... + {n}²", "n(n + 1)(2n + 1) ÷ 6"
        alts = (n * (n + 1) // 2, (n * (n + 1) // 2) ** 2, s + n)
    else:
        s = (n * (n + 1) // 2) ** 2
        en, bn, f_ = f"1³ + 2³ + ... + {n}³", f"1³ + 2³ + ... + {n}³", "[n(n + 1) ÷ 2]²"
        alts = (n * (n + 1) * (2 * n + 1) // 6, n ** 3, s - n)
    return _n(f"What is {en}?", f"{bn}-এর মান কত?", s,
              f"Use {f_} with n = {n}: {s}.", f"সূত্র {f_}, n = {n} বসিয়ে: {s}।", alts)


def roots_sq(b, c):
    s, p = -b, c
    r = s * s - 2 * p
    return _n(f"If α and β are the roots of x² {'+' if b >= 0 else '-'} {abs(b)}x + {c} = 0, what is α² + β²?",
              f"x² {'+' if b >= 0 else '-'} {abs(b)}x + {c} = 0 সমীকরণের বীজ α আর β হলে α² + β² কত?", r,
              f"α + β = {s}, αβ = {p}; α² + β² = (α + β)² - 2αβ = {s * s} - {2 * p} = {r}.",
              f"α + β = {s}, αβ = {p}; α² + β² = (α + β)² - 2αβ = {s * s} - {2 * p} = {r}।",
              (s * s + 2 * p, s * s, abs(s) + p))


def modulus(a, b):
    m = math.hypot(a, b)
    return _n(f"If z = {a} + {b}i, what is |z|, the distance of z from the origin in the Argand plane?",
              f"জটিল সংখ্যা {a} + {b}i-এর মডুলাস কত?", m,
              f"|z| = √(a² + b²) = √({a * a} + {b * b}) = {_f(_c(m))}.",
              f"মডুলাস = √(a² + b²) = √({a * a} + {b * b}) = {_f(_c(m))}।",
              (a + b, a * a + b * b, abs(a - b) + 1))


def one_plus_i(n):
    m = 2 ** (n / 2)
    return _n(f"What is the modulus of (1 + i)^{n}?",
              f"(1 + i)^{n}-এর মডুলাস কত?", m,
              f"|1 + i| = √2, and |zⁿ| = |z|ⁿ, so (√2)^{n} = {_f(_c(m))}.",
              f"|1 + i| = √2, আর |zⁿ| = |z|ⁿ, তাই (√2)^{n} = {_f(_c(m))}।",
              (2 ** n, n * 2, m * 2 if m * 2 != 2 ** n else m + 3))


def det3(m):
    (a, b, c), (d, e, f), (g, h, i) = m
    r = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    txt = "; ".join(" ".join(str(x) for x in row) for row in m)
    return _n(f"What is the determinant of the 3 x 3 matrix with rows [{txt}]?",
              f"সারি [{txt}]-যুক্ত 3 x 3 ম্যাট্রিক্সের নির্ণায়ক কত?", r,
              f"Expand along row 1: {a}({e * i - f * h}) - {b}({d * i - f * g}) + {c}({d * h - e * g}) = {r}.",
              f"প্রথম সারি ধরে বিস্তার: {a}({e * i - f * h}) - {b}({d * i - f * g}) + {c}({d * h - e * g}) = {r}।",
              (a * e * i, abs(r) + 4, a + e + i))


def det_scale(n, d, k):
    r = k ** n * d
    return _n(f"A is a {n} x {n} matrix with det A = {d}. What is det({k}A)?",
              f"A একটা {n} x {n} ম্যাট্রিক্স, det A = {d}। det({k}A) কত?", r,
              f"Each of the {n} rows is multiplied by {k}: det(kA) = kⁿ det A = {k}^{n} x {d} = {r}.",
              f"{n}টি সারির প্রতিটি {k} দিয়ে গুণ হয়: det(kA) = kⁿ det A = {k}^{n} x {d} = {r}।",
              (k * d, k * n * d, k ** (n - 1) * d))


def count_functions(m, n):
    r = n ** m
    return _n(f"Set A has {m} elements and set B has {n}. How many functions are there from A to B?",
              f"A সেটে {m}টি আর B সেটে {n}টি উপাদান। A থেকে B-তে কয়টি অপেক্ষক আছে?", r,
              f"Each of the {m} elements of A can go to any of {n} elements: {n}^{m} = {r:,}.",
              f"A-র {m}টি উপাদানের প্রত্যেকটি B-র {n}টির যেকোনোটিতে যেতে পারে: {n}^{m} = {r:,}।",
              (m ** n, m * n, 2 ** (m * n)))


def one_one(m, n):
    r = math.perm(n, m)
    return _n(f"How many one-one functions are there from a set of {m} elements to a set of {n} elements?",
              f"{m} উপাদানের একটা সেট থেকে {n} উপাদানের সেটে কয়টি এক-এক অপেক্ষক আছে?", r,
              f"ⁿPₘ = {n}! ÷ {n - m}! = {r:,}.",
              f"ⁿPₘ = {n}! ÷ {n - m}! = {r:,}।",
              (n ** m, math.comb(n, m), r // 2))


def relations(m, n):
    r = 2 ** (m * n)
    return _n(f"How many relations are there from a set with {m} elements to a set with {n} elements?",
              f"{m} উপাদানের সেট থেকে {n} উপাদানের সেটে কয়টি সম্বন্ধ আছে?", r,
              f"A relation is any subset of A x B, which has {m * n} pairs: 2^{m * n} = {r:,}.",
              f"সম্বন্ধ মানে A x B-র যেকোনো উপসেট, যাতে {m * n}টি জোড়: 2^{m * n} = {r:,}।",
              (m * n, n ** m, 2 ** (m + n)))


# ---------------------------------------------------------------- combinatorics
def word_arr(word, en_note, bn_note):
    from collections import Counter
    r = math.factorial(len(word))
    for c in Counter(word).values():
        r //= math.factorial(c)
    return _n(f"In how many distinct ways can the letters of the word {word} be arranged?",
              f"{word} শব্দের অক্ষরগুলো কত রকম ভিন্নভাবে সাজানো যায়?", r,
              f"{len(word)}! divided by the factorials of repeated letters ({en_note}) = {r:,}.",
              f"{len(word)}! কে পুনরাবৃত্ত অক্ষরের ফ্যাক্টোরিয়াল ({bn_note}) দিয়ে ভাগ = {r:,}।",
              (math.factorial(len(word)), r * 2, r // 2))


def committee(n_m, n_w, k_m, k_w):
    r = math.comb(n_m, k_m) * math.comb(n_w, k_w)
    return _n(f"A committee of {k_m} men and {k_w} women is chosen from {n_m} men and {n_w} women. In how many ways can this be done?",
              f"{n_m} জন পুরুষ আর {n_w} জন মহিলার মধ্যে থেকে {k_m} জন পুরুষ আর {k_w} জন মহিলার একটা কমিটি বাছা হবে। কত ভাবে করা যায়?", r,
              f"ᶜ({n_m},{k_m}) x ᶜ({n_w},{k_w}) = {math.comb(n_m, k_m)} x {math.comb(n_w, k_w)} = {r:,}.",
              f"ᶜ({n_m},{k_m}) x ᶜ({n_w},{k_w}) = {math.comb(n_m, k_m)} x {math.comb(n_w, k_w)} = {r:,}।",
              (math.comb(n_m + n_w, k_m + k_w), math.comb(n_m, k_m) + math.comb(n_w, k_w), r * 2))


def circular(n):
    r = math.factorial(n - 1)
    return _n(f"In how many ways can {n} people sit around a round table (rotations counted as the same)?",
              f"{n} জন মানুষ একটা গোল টেবিলে কত ভাবে বসতে পারে (ঘুরিয়ে একই হলে একটাই ধরা হবে)?", r,
              f"Fix one person and arrange the rest: ({n} - 1)! = {r:,}.",
              f"একজনকে স্থির রেখে বাকিদের সাজাও: ({n} - 1)! = {r:,}।",
              (math.factorial(n), r // 2, r * 2))


def diagonals(n):
    r = n * (n - 3) // 2
    return _n(f"How many diagonals does a convex polygon with {n} sides have?",
              f"{n} বাহুর একটা উত্তল বহুভুজের কয়টি কর্ণ আছে?", r,
              f"ⁿC₂ - n = {math.comb(n, 2)} - {n} = {r}: every pair of vertices minus the sides.",
              f"ⁿC₂ - n = {math.comb(n, 2)} - {n} = {r}: শীর্ষের সব জোড় থেকে বাহুগুলো বাদ।",
              (math.comb(n, 2), n * (n - 1), r + n))


def binom_coeff(n, k):
    r = math.comb(n, k)
    return _n(f"What is the coefficient of x^{k} in the expansion of (1 + x)^{n}?",
              f"(1 + x)^{n}-এর বিস্তারে x^{k}-এর সহগ কত?", r,
              f"The general term is ⁿCᵣ xʳ, so the coefficient is ᶜ({n},{k}) = {r:,}.",
              f"সাধারণ পদ ⁿCᵣ xʳ, তাই সহগ ᶜ({n},{k}) = {r:,}।",
              (math.comb(n, k - 1), math.perm(n, k), n * k))


def const_term(n):
    r = math.comb(n, n // 2)
    return _n(f"What is the term independent of x in the expansion of (x + 1/x)^{n}?",
              f"(x + 1/x)^{n}-এর বিস্তারে x-মুক্ত পদ কত?", r,
              f"Tᵣ₊₁ = ⁿCᵣ x^(n - 2r); x⁰ needs r = {n // 2}, giving ᶜ({n},{n // 2}) = {r:,}.",
              f"Tᵣ₊₁ = ⁿCᵣ x^(n - 2r); x⁰-এর জন্য r = {n // 2}, তাই ᶜ({n},{n // 2}) = {r:,}।",
              (math.comb(n, n // 2 - 1), 2 ** n, n))


def binom_sum(n):
    r = 2 ** n
    return _n(f"What is the sum of all the binomial coefficients in the expansion of (1 + x)^{n}?",
              f"(1 + x)^{n}-এর বিস্তারে সব দ্বিপদ সহগের যোগফল কত?", r,
              f"Put x = 1: (1 + 1)^{n} = 2^{n} = {r:,}.",
              f"x = 1 বসাও: (1 + 1)^{n} = 2^{n} = {r:,}।",
              (n * n, 2 ** (n - 1), n + 1))


# ---------------------------------------------------------------- calculus
def limit_power(n, a):
    r = n * a ** (n - 1)
    return _n(f"What is the limit of (x^{n} - {a ** n}) ÷ (x - {a}) as x → {a}?",
              f"x → {a} হলে (x^{n} - {a ** n}) ÷ (x - {a})-এর সীমা কত?", r,
              f"Standard limit: (xⁿ - aⁿ)/(x - a) → n aⁿ⁻¹ = {n} x {a}^{n - 1} = {r}.",
              f"প্রমাণ সীমা: (xⁿ - aⁿ)/(x - a) → n aⁿ⁻¹ = {n} x {a}^{n - 1} = {r}।",
              (a ** n, n * a, a ** (n - 1)))


def limit_sin(k, m):
    r = F(k, m)
    return _fr(f"What is the limit of sin({k}x) ÷ ({m}x) as x → 0?",
               f"x → 0 হলে sin({k}x) ÷ ({m}x)-এর সীমা কত?", r, (F(m, k), F(k * m), F(1)),
               f"sin({k}x)/({k}x) → 1, so the limit is {k}/{m} = {_fs(r)}.",
               f"sin({k}x)/({k}x) → 1, তাই সীমা {k}/{m} = {_fs(r)}।")


def limit_e(k):
    opts = [f"e^{k}", f"e^{-k}" if k > 0 else "e", f"e^{k * 2}", "1"]
    return _s(f"What is the limit of (1 + {k}/x)^x as x → ∞?", opts,
              f"(1 + k/x)^x → eᵏ, so the limit is e^{k}.",
              f"x → ∞ হলে (1 + {k}/x)^x-এর সীমা কত?",
              f"(1 + k/x)^x → eᵏ, তাই সীমা e^{k}।")


def deriv_at(n, c, a):
    r = c * n * a ** (n - 1)
    return _n(f"If f(x) = {c}x^{n}, what is f'({a})?",
              f"f(x) = {c}x^{n} হলে f'({a}) কত?", r,
              f"f'(x) = {c * n}x^{n - 1}, so f'({a}) = {c * n} x {a}^{n - 1} = {r}.",
              f"অবকলজ f'(x) = {c * n}x^{n - 1}, তাই f'({a}) = {c * n} x {a}^{n - 1} = {r}।",
              (c * a ** n, n * a ** (n - 1), c * n * a ** n))


def tangent_slope(a, b, x0):
    r = 2 * a * x0 + b
    return _n(f"What is the slope of the tangent to y = {a}x² + {b}x at x = {x0}?",
              f"x = {x0} বিন্দুতে y = {a}x² + {b}x বক্ররেখার স্পর্শকের নতি কত?", r,
              f"dy/dx = {2 * a}x + {b} = {2 * a} x {x0} + {b} = {r}.",
              f"অবকলজ dy/dx = {2 * a}x + {b} = {2 * a} x {x0} + {b} = {r}।",
              (a * x0 * x0 + b * x0, 2 * a * x0, r + b))


def quad_max(b, c):
    xm = F(b, 2)
    r = -xm * xm + b * xm + c
    return _fr(f"What is the maximum value of f(x) = -x² + {b}x + {c}?",
               f"f(x) = -x² + {b}x + {c}-এর সর্বোচ্চ মান কত?", r, (c, xm, r + b),
               f"f'(x) = -2x + {b} = 0 at x = {_fs(xm)}; f({_fs(xm)}) = {_fs(r)}.",
               f"f'(x) = -2x + {b} = 0 হয় x = {_fs(xm)}-এ; f({_fs(xm)}) = {_fs(r)}।")


def max_rect(p):
    r = F(p, 4) ** 2
    return _fr(f"A rectangle has a perimeter of {p} m. What is the largest area it can enclose (in m²)?",
               f"একটা আয়তক্ষেত্রের পরিসীমা {p} m। এটা সর্বোচ্চ কত ক্ষেত্রফল (m²) ঘিরতে পারে?", r,
               (F(p, 2) ** 2, F(p * p, 8), r - p),
               f"For fixed perimeter the square is best: side {_fs(F(p, 4))} m, area {_fs(r)} m².",
               f"নির্দিষ্ট পরিসীমায় বর্গই সেরা: বাহু {_fs(F(p, 4))} m, ক্ষেত্রফল {_fs(r)} m²।")


def integral_power(n, a):
    r = F(a ** (n + 1), n + 1)
    return _fr(f"What is the value of the integral of x^{n} from 0 to {a}?",
               f"0 থেকে {a} পর্যন্ত x^{n}-এর সমাকলের মান কত?", r,
               (F(a ** n, n), F(a ** (n + 1), n), F(n * a ** (n - 1))),
               f"∫ xⁿ dx = x^(n + 1) ÷ (n + 1): {a}^{n + 1} ÷ {n + 1} = {_fs(r)}.",
               f"সমাকল ∫ xⁿ dx = x^(n + 1) ÷ (n + 1): {a}^{n + 1} ÷ {n + 1} = {_fs(r)}।")


def area_curves(k):
    r = F(4, 3) * F(k) ** F(3, 2) if k in (1, 4, 9, 16) else None
    root = int(k ** 0.5)
    val = F(4, 3) * root ** 3
    return _fr(f"What is the area enclosed between the parabola y = x² and the line y = {k}?",
               f"অধিবৃত্ত y = x² আর রেখা y = {k}-এর মধ্যে আবদ্ধ ক্ষেত্রফল কত?", val,
               (F(2, 3) * root ** 3, F(2 * root * k), val + 1),
               f"Area = ∫ from -{root} to {root} of ({k} - x²) dx = 2[{k}x - x³/3] from 0 to {root} = {_fs(val)}.",
               f"ক্ষেত্রফল = -{root} থেকে {root} পর্যন্ত ({k} - x²)-এর সমাকল = 2[{k}x - x³/3], 0 থেকে {root} = {_fs(val)}।")


def de_growth(k, t):
    opts = [f"y = {k}e^({t}x)", f"y = e^({k * t}x)", f"y = {k}x + {t}", f"y = {t}e^({k}x)"]
    return _s(f"Which function solves dy/dx = {t}y with y(0) = {k}?", opts,
              f"Separating variables: dy/y = {t} dx, so ln y = {t}x + C; y(0) = {k} gives y = {k}e^({t}x).",
              f"কোন অপেক্ষক dy/dx = {t}y, y(0) = {k} সমীকরণের সমাধান?",
              f"চলরাশি পৃথক করে: dy/y = {t} dx, তাই ln y = {t}x + C; y(0) = {k} থেকে y = {k}e^({t}x)।")


# ---------------------------------------------------------------- coordinate geometry
def point_line(a, b, c, x, y):
    d = abs(a * x + b * y + c) / math.hypot(a, b)
    return _n(f"What is the perpendicular distance from the point ({x}, {y}) to the line {a}x + {b}y + {c} = 0?",
              f"বিন্দু ({x}, {y}) থেকে রেখা {a}x + {b}y + {c} = 0-এর লম্ব দূরত্ব কত?", d,
              f"d = |ax₁ + by₁ + c| ÷ √(a² + b²) = |{a * x + b * y + c}| ÷ {_f(_c(math.hypot(a, b)))} = {_f(_c(d))}.",
              f"দূরত্ব = |ax₁ + by₁ + c| ÷ √(a² + b²) = |{a * x + b * y + c}| ÷ {_f(_c(math.hypot(a, b)))} = {_f(_c(d))}।",
              (abs(a * x + b * y + c), d * 2, math.hypot(x, y)))


def parallel_lines(a, b, c1, c2):
    d = abs(c1 - c2) / math.hypot(a, b)
    return _n(f"What is the distance between the parallel lines {a}x + {b}y + {c1} = 0 and {a}x + {b}y + {c2} = 0?",
              f"সমান্তরাল রেখা {a}x + {b}y + {c1} = 0 আর {a}x + {b}y + {c2} = 0-এর মধ্যে দূরত্ব কত?", d,
              f"d = |c₁ - c₂| ÷ √(a² + b²) = {abs(c1 - c2)} ÷ {_f(_c(math.hypot(a, b)))} = {_f(_c(d))}.",
              f"দূরত্ব = |c₁ - c₂| ÷ √(a² + b²) = {abs(c1 - c2)} ÷ {_f(_c(math.hypot(a, b)))} = {_f(_c(d))}।",
              (abs(c1 - c2), abs(c1 + c2) / math.hypot(a, b), d + 1))


def circle_r(g, f, c):
    r = math.sqrt(g * g + f * f - c)
    return _n(f"What is the radius of the circle x² + y² {'+' if g >= 0 else '-'} {abs(2 * g)}x {'+' if f >= 0 else '-'} {abs(2 * f)}y {'+' if c >= 0 else '-'} {abs(c)} = 0?",
              f"বৃত্ত x² + y² {'+' if g >= 0 else '-'} {abs(2 * g)}x {'+' if f >= 0 else '-'} {abs(2 * f)}y {'+' if c >= 0 else '-'} {abs(c)} = 0-এর ব্যাসার্ধ কত?", r,
              f"Centre (-g, -f) = ({-g}, {-f}); r = √(g² + f² - c) = √({g * g} + {f * f} - ({c})) = {_f(_c(r))}.",
              f"কেন্দ্র (-g, -f) = ({-g}, {-f}); ব্যাসার্ধ = √(g² + f² - c) = √({g * g} + {f * f} - ({c})) = {_f(_c(r))}।",
              (g * g + f * f - c, math.sqrt(g * g + f * f), abs(c)))


def parabola_lr(a4):
    return _n(f"What is the length of the latus rectum of the parabola y² = {a4}x?",
              f"অধিবৃত্ত y² = {a4}x-এর নাভিলম্বের দৈর্ঘ্য কত?", a4,
              f"y² = 4ax with a = {_f(_c(a4 / 4))}; latus rectum = 4a = {a4}, and the focus is ({_f(_c(a4 / 4))}, 0).",
              f"y² = 4ax, a = {_f(_c(a4 / 4))}; নাভিলম্ব = 4a = {a4}, আর নাভি ({_f(_c(a4 / 4))}, 0)।",
              (a4 / 4, a4 / 2, a4 * 2))


def ellipse_e(a, b):
    e = math.sqrt(1 - b * b / (a * a))
    return _n(f"What is the eccentricity of the ellipse x²/{a * a} + y²/{b * b} = 1?",
              f"উপবৃত্ত x²/{a * a} + y²/{b * b} = 1-এর উৎকেন্দ্রিকতা কত?", e,
              f"e = √(1 - b²/a²) = √(1 - {b * b}/{a * a}) = {_f(_c(e))}; an ellipse always has e < 1.",
              f"উৎকেন্দ্রিকতা = √(1 - b²/a²) = √(1 - {b * b}/{a * a}) = {_f(_c(e))}; উপবৃত্তে সবসময় e < 1।",
              (b / a, math.sqrt(1 + b * b / (a * a)), 1 - b / a))


def hyperbola_e(a, b):
    e = math.sqrt(1 + b * b / (a * a))
    return _n(f"What is the eccentricity of the hyperbola x²/{a * a} - y²/{b * b} = 1?",
              f"পরাবৃত্ত x²/{a * a} - y²/{b * b} = 1-এর উৎকেন্দ্রিকতা কত?", e,
              f"e = √(1 + b²/a²) = √(1 + {b * b}/{a * a}) = {_f(_c(e))}; a hyperbola always has e > 1.",
              f"উৎকেন্দ্রিকতা = √(1 + b²/a²) = √(1 + {b * b}/{a * a}) = {_f(_c(e))}; পরাবৃত্তে সবসময় e > 1।",
              (b / a, math.sqrt(abs(1 - b * b / (a * a))) or 0.5, e + 1))


def dist3(p, q):
    d = math.dist(p, q)
    return _n(f"What is the distance between the points {p} and {q} in space?",
              f"মহাশূন্যে {p} আর {q} বিন্দুর মধ্যে দূরত্ব কত?", d,
              f"√(Δx² + Δy² + Δz²) = √({sum((a - b) ** 2 for a, b in zip(p, q))}) = {_f(_c(d))}.",
              f"দূরত্ব = √(Δx² + Δy² + Δz²) = √({sum((a - b) ** 2 for a, b in zip(p, q))}) = {_f(_c(d))}।",
              (sum(abs(a - b) for a, b in zip(p, q)), d * d, d + 2))


def cross_area(a, b):
    c = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    r = math.sqrt(sum(x * x for x in c))
    return _n(f"What is the area of the parallelogram with adjacent sides a = {a} and b = {b}?",
              f"সংলগ্ন বাহু a = {a} আর b = {b}-যুক্ত সামান্তরিকের ক্ষেত্রফল কত?", r,
              f"Area = |a x b|; a x b = {c}, |a x b| = {_f(_c(r))}.",
              f"ক্ষেত্রফল = |a x b|; a x b = {c}, তার মান {_f(_c(r))}।",
              (r / 2, abs(sum(x * y for x, y in zip(a, b))) + 1, r * 2))


def triple(a, b, c):
    v = (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
         + a[2] * (b[0] * c[1] - b[1] * c[0]))
    return _n(f"What is the volume of the parallelepiped with edges a = {a}, b = {b} and c = {c}?",
              f"a = {a}, b = {b} আর c = {c} ধারবিশিষ্ট সামান্তরিক ঘনবস্তুর আয়তন কত?", abs(v),
              f"Volume = |a · (b x c)| = |{v}| = {abs(v)}; zero would mean the three vectors are coplanar.",
              f"আয়তন = |a · (b x c)| = |{v}| = {abs(v)}; শূন্য হলে তিনটি ভেক্টর সমতলীয়।",
              (abs(v) * 2, sum(a) + sum(b) + sum(c), abs(v) + 6))


def projection(a, b):
    d = sum(x * y for x, y in zip(a, b))
    nb = math.sqrt(sum(x * x for x in b))
    r = d / nb
    return _n(f"What is the scalar projection of a = {a} on b = {b}?",
              f"b = {b}-এর উপর a = {a}-এর স্কেলার অভিক্ষেপ কত?", r,
              f"(a · b) ÷ |b| = {d} ÷ {_f(_c(nb))} = {_f(_c(r))}.",
              f"অভিক্ষেপ = (a · b) ÷ |b| = {d} ÷ {_f(_c(nb))} = {_f(_c(r))}।",
              (d, d / sum(x * x for x in b), r * 2))


# ---------------------------------------------------------------- probability, statistics, trigonometry
def dice_sum(s):
    ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s)
    r = F(ways, 36)
    return _fr(f"Two fair dice are thrown. What is the probability that the total is {s}?",
               f"দুটো নিরপেক্ষ লুডোর ছক্কা ছোড়া হল। মোট {s} হওয়ার সম্ভাবনা কত?", r, (F(1, 6), F(ways, 12), F(1, 36) if ways > 1 else F(1, 18)),
               f"{ways} of the 36 equally likely outcomes give {s}: {_fs(r)}.",
               f"36টি সমসম্ভাব্য ফলের মধ্যে {ways}টিতে {s} হয়: {_fs(r)}।")


def coins_at_least(n):
    r = 1 - F(1, 2 ** n)
    return _fr(f"{n} fair coins are tossed. What is the probability of getting at least one head?",
               f"{n}টি নিরপেক্ষ মুদ্রা ছোড়া হল। অন্তত একটা হেড পাওয়ার সম্ভাবনা কত?", r, (F(1, 2), F(n, 2 ** n), F(1, 2 ** n)),
               f"P(no head) = (1/2)^{n} = {_fs(F(1, 2 ** n))}, so P(at least one) = {_fs(r)}.",
               f"কোনো হেড না পাওয়ার সম্ভাবনা (1/2)^{n} = {_fs(F(1, 2 ** n))}, তাই অন্তত একটা = {_fs(r)}।")


def bayes(p_a, p_ba, p_bna):
    pa, pba, pbna = F(p_a), F(p_ba), F(p_bna)
    r = pa * pba / (pa * pba + (1 - pa) * pbna)
    return _fr(f"A test detects a disease with probability {_fs(pba)}; it wrongly flags a healthy person with probability {_fs(pbna)}. If {_fs(pa)} of people have the disease, what is P(disease | positive test)?",
               f"একটা পরীক্ষা {_fs(pba)} সম্ভাবনায় রোগ ধরে; সুস্থ মানুষকে ভুল করে {_fs(pbna)} সম্ভাবনায় রোগী বলে। {_fs(pa)} অংশ মানুষের রোগ থাকলে, পরীক্ষা পজিটিভ হলে রোগ থাকার সম্ভাবনা কত?", r,
               (pba, pa, pa * pba),
               f"Bayes: P = P(A)P(+|A) ÷ [P(A)P(+|A) + P(A')P(+|A')] = {_fs(pa * pba)} ÷ {_fs(pa * pba + (1 - pa) * pbna)} = {_fs(r)}.",
               f"বেইজের উপপাদ্য: সম্ভাবনা = {_fs(pa * pba)} ÷ {_fs(pa * pba + (1 - pa) * pbna)} = {_fs(r)}।")


def variance(xs):
    m = F(sum(xs), len(xs))
    v = sum((x - m) ** 2 for x in xs) / len(xs)
    txt = ", ".join(map(str, xs))
    return _fr(f"What is the variance of the data {txt}?",
               f"তথ্য {txt}-এর ভেদাঙ্ক কত?", v, (F(v) ** 2 if v < 5 else v / 2, m, v + 1),
               f"Mean = {_fs(m)}; variance = mean of squared deviations = {_fs(v)}.",
               f"গড় = {_fs(m)}; ভেদাঙ্ক = বিচ্যুতির বর্গের গড় = {_fs(v)}।")


def sd_scale(sd, k, c):
    r = sd * k
    return _n(f"A data set has standard deviation {sd}. Every value is multiplied by {k} and then {c} is added. What is the new standard deviation?",
              f"একটা তথ্যসারির পরিমিত ব্যবধান {sd}। প্রতিটি মান {k} দিয়ে গুণ করে {c} যোগ করা হল। নতুন পরিমিত ব্যবধান কত?", r,
              f"Adding a constant shifts every value equally (no change); multiplying by {k} scales the spread: {sd} x {k} = {r}.",
              f"ধ্রুবক যোগ করলে সব মান সমান সরে (পরিবর্তন নেই); {k} দিয়ে গুণ করলে বিস্তার বাড়ে: {sd} x {k} = {r}।",
              (sd * k + c, sd, sd * k * k))


def amp(a, b):
    r = math.hypot(a, b)
    return _n(f"What is the maximum value of {a} sin x + {b} cos x?",
              f"{a} sin x + {b} cos x-এর সর্বোচ্চ মান কত?", r,
              f"a sin x + b cos x = √(a² + b²) sin(x + φ), so the maximum is √({a * a} + {b * b}) = {_f(_c(r))}.",
              f"a sin x + b cos x = √(a² + b²) sin(x + φ), তাই সর্বোচ্চ মান √({a * a} + {b * b}) = {_f(_c(r))}।",
              (a + b, max(a, b), r * r))


def log_val(base, x):
    r = math.log(x, base)
    return _n(f"What is log base {base} of {x:,}?",
              f"{base} ভিত্তিতে {x:,}-এর লগারিদম কত?", round(r),
              f"{base}^{round(r)} = {x:,}, so the logarithm is {round(r)}.",
              f"{base}^{round(r)} = {x:,}, তাই লগারিদম {round(r)}।",
              (x / base, round(r) + 2, base))


NUMERIC = [
    ap_term(3, 4, 20), ap_term(7, 5, 15), ap_sum(2, 3, 20), ap_sum(5, 4, 12),
    gp_inf(12, 1, 3), gp_inf(8, 1, 2), gp_inf(9, 2, 3),
    series_sum("sq", 10), series_sum("cube", 10), series_sum("sq", 20),
    roots_sq(-5, 6), roots_sq(-7, 10), roots_sq(-3, 1),
    modulus(3, 4), modulus(5, 12), modulus(8, 15), one_plus_i(8), one_plus_i(6),
    det3(((1, 2, 3), (0, 1, 4), (5, 6, 0))), det3(((2, 0, 1), (1, 3, 2), (1, 1, 2))), det3(((3, 1, 2), (0, 2, 1), (1, 0, 4))),
    det_scale(3, 5, 2), det_scale(2, 7, 3), det_scale(4, 2, 2),
    count_functions(3, 4), count_functions(4, 2), one_one(3, 5), one_one(2, 6),
    relations(2, 3), relations(3, 3),
    word_arr("BANANA", "A three times, N twice", "A তিনবার, N দুবার"),
    word_arr("LEVEL", "L twice, E twice", "L দুবার, E দুবার"),
    word_arr("ENGINEER", "E three times, N twice", "E তিনবার, N দুবার"),
    word_arr("INDIA", "I twice", "I দুবার"),
    committee(6, 4, 3, 2), committee(7, 5, 2, 3), committee(5, 5, 2, 2),
    circular(6), circular(8), diagonals(10), diagonals(12),
    binom_coeff(8, 3), binom_coeff(10, 4), binom_coeff(12, 5),
    const_term(8), const_term(10), binom_sum(10), binom_sum(7),
    limit_power(3, 2), limit_power(5, 1), limit_power(4, 3),
    limit_sin(3, 2), limit_sin(5, 4), limit_sin(7, 3),
    limit_e(2), limit_e(3),
    deriv_at(3, 2, 2), deriv_at(4, 2, 3), deriv_at(5, 3, 1),
    tangent_slope(3, 2, 4), tangent_slope(2, 5, 3), tangent_slope(4, 6, 5),
    quad_max(6, 1), quad_max(5, 2), quad_max(8, 3),
    max_rect(40), max_rect(30), max_rect(100),
    integral_power(2, 3), integral_power(3, 2), integral_power(4, 1), integral_power(2, 6),
    area_curves(1), area_curves(4), area_curves(9),
    de_growth(3, 2), de_growth(5, 4),
    point_line(3, 4, -5, 2, 3), point_line(5, 12, 13, 1, 1), point_line(6, 8, 1, 3, 4),
    parallel_lines(3, 4, 5, -10), parallel_lines(5, 12, 4, -22),
    circle_r(-2, 3, -3), circle_r(1, -1, -7), circle_r(3, 4, -11),
    parabola_lr(12), parabola_lr(20),
    ellipse_e(5, 3), ellipse_e(13, 5), ellipse_e(5, 4),
    hyperbola_e(3, 4), hyperbola_e(5, 12),
    dist3((1, 2, 3), (4, 6, 15)), dist3((0, 0, 0), (2, 3, 6)), dist3((1, 1, 1), (3, 3, 2)),
    cross_area((1, 2, 0), (0, 1, 3)), cross_area((2, 0, 0), (0, 3, 0)), cross_area((1, 1, 1), (1, -1, 0)),
    triple((1, 0, 0), (0, 2, 0), (0, 0, 3)), triple((1, 2, 3), (0, 1, 4), (2, 1, 1)),
    projection((2, 3, 6), (1, 2, 2)), projection((4, 1, 2), (3, 0, 4)),
    dice_sum(7), dice_sum(8), dice_sum(10), dice_sum(4),
    coins_at_least(3), coins_at_least(4),
    bayes(F(1, 100), F(9, 10), F(1, 10)), bayes(F(1, 5), F(4, 5), F(1, 5)),
    variance([2, 4, 6, 8]), variance([1, 2, 3, 4, 5]), variance([5, 7, 9, 11, 13]),
    sd_scale(4, 3, 10), sd_scale(2.5, 2, 7),
    amp(3, 4), amp(5, 12), amp(8, 15),
    log_val(2, 1024), log_val(3, 729), log_val(5, 625),
    ap_term(100, -3, 25), ap_sum(1, 2, 50), gp_inf(20, 1, 4), series_sum("cube", 6), roots_sq(-9, 20),
    modulus(7, 24), det_scale(3, 4, 3), count_functions(2, 5),
    word_arr("COMMITTEE", "M, T and E twice each", "M, T আর E দুবার করে"), committee(8, 6, 3, 3),
    circular(5), diagonals(8), binom_coeff(9, 2), limit_power(6, 1), point_line(8, 15, -7, 2, 1), dice_sum(5),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    _q("If ω is a complex cube root of unity (ω ≠ 1), what is 1 + ω + ω²?", ["0", "1", "-1", "3"],
       "ω³ = 1 and ω ≠ 1, so 1 + ω + ω² = (ω³ - 1)/(ω - 1) = 0.",
       "ω যদি এককের একটা জটিল ঘনমূল হয় (ω ≠ 1), তবে 1 + ω + ω² কত?", ["0", "1", "-1", "3"],
       "ω³ = 1 আর ω ≠ 1, তাই 1 + ω + ω² = (ω³ - 1)/(ω - 1) = 0।"),
    _q("What is i^2026 (where i² = -1)?", ["-1", "1", "i", "-i"],
       "Powers of i repeat every 4; 2026 leaves remainder 2 when divided by 4, so i^2026 = i² = -1.",
       "i^2026-এর মান কত (যেখানে i² = -1)?", ["-1", "1", "i", "-i"],
       "i-এর ঘাত প্রতি 4-এ পুনরাবৃত্ত হয়; 2026-কে 4 দিয়ে ভাগ করলে ভাগশেষ 2, তাই i^2026 = i² = -1।"),
    _q("The argument of the product of two complex numbers equals…", ["The sum of their arguments", "The product of their arguments", "The difference of their arguments", "Always zero"],
       "In polar form r₁e^(iθ₁) x r₂e^(iθ₂) = r₁r₂e^(i(θ₁+θ₂)): moduli multiply, arguments add.",
       "দুটো জটিল সংখ্যার গুণফলের আর্গুমেন্ট সমান…", ["তাদের আর্গুমেন্টের যোগফল", "তাদের আর্গুমেন্টের গুণফল", "তাদের আর্গুমেন্টের পার্থক্য", "সবসময় শূন্য"],
       "ধ্রুবীয় রূপে r₁e^(iθ₁) x r₂e^(iθ₂) = r₁r₂e^(i(θ₁+θ₂)): মডুলাস গুণ হয়, আর্গুমেন্ট যোগ হয়।"),
    _q("For real a, b, c with a ≠ 0, the roots of ax² + bx + c = 0 are real and distinct when…", ["b² - 4ac > 0", "b² - 4ac = 0", "b² - 4ac < 0", "a + b + c = 0"],
       "The discriminant decides: positive gives two real roots, zero a repeated root, negative a complex pair.",
       "বাস্তব a, b, c আর a ≠ 0 হলে ax² + bx + c = 0-এর বীজ বাস্তব ও ভিন্ন হয় যখন…", ["b² - 4ac > 0", "b² - 4ac = 0", "b² - 4ac < 0", "a + b + c = 0"],
       "নিরূপক ঠিক করে: ধনাত্মক হলে দুটো বাস্তব বীজ, শূন্য হলে সমান বীজ, ঋণাত্মক হলে জটিল জোড়।"),
    _q("For positive numbers, how do the arithmetic mean (AM) and geometric mean (GM) compare?", ["AM ≥ GM, with equality only when all numbers are equal", "GM ≥ AM always", "They are always equal", "AM < GM always"],
       "The AM-GM inequality is a standard tool for finding minimum and maximum values.",
       "ধনাত্মক সংখ্যার ক্ষেত্রে সমান্তর গড় (AM) আর গুণোত্তর গড় (GM)-এর তুলনা কী?", ["AM ≥ GM, সমান কেবল সব সংখ্যা সমান হলে", "সবসময় GM ≥ AM", "সবসময় সমান", "সবসময় AM < GM"],
       "AM-GM অসমতা সর্বনিম্ন আর সর্বোচ্চ মান বের করার একটা প্রমাণ কৌশল।"),
    _q("A square matrix has an inverse exactly when…", ["Its determinant is non-zero", "It is symmetric", "Its trace is zero", "All entries are positive"],
       "A⁻¹ = adj(A) ÷ det(A), which needs det A ≠ 0; such a matrix is called non-singular.",
       "একটা বর্গ ম্যাট্রিক্সের বিপরীত থাকে ঠিক তখনই যখন…", ["তার নির্ণায়ক শূন্য নয়", "সেটা প্রতিসম", "তার ট্রেস শূন্য", "সব উপাদান ধনাত্মক"],
       "A⁻¹ = adj(A) ÷ det(A), এর জন্য det A ≠ 0 লাগে; এমন ম্যাট্রিক্সকে অব্যতিক্রমী বলে।"),
    _q("What is the determinant of any skew-symmetric matrix of odd order?", ["0", "1", "-1", "It cannot be found"],
       "det A = det(Aᵀ) = det(-A) = (-1)ⁿ det A; for odd n this forces det A = 0.",
       "বিজোড় ক্রমের যেকোনো বিপ্রতিসম ম্যাট্রিক্সের নির্ণায়ক কত?", ["0", "1", "-1", "নির্ণয় করা যায় না"],
       "det A = det(Aᵀ) = det(-A) = (-1)ⁿ det A; বিজোড় n হলে det A = 0 হতেই হবে।"),
    _q("If A and B are invertible matrices of the same order, what is (AB)⁻¹?", ["B⁻¹A⁻¹", "A⁻¹B⁻¹", "AB", "BA"],
       "(AB)(B⁻¹A⁻¹) = A(BB⁻¹)A⁻¹ = I - the order reverses, as with transposes.",
       "A আর B একই ক্রমের বিপরীতযোগ্য ম্যাট্রিক্স হলে (AB)⁻¹ কত?", ["B⁻¹A⁻¹", "A⁻¹B⁻¹", "AB", "BA"],
       "(AB)(B⁻¹A⁻¹) = A(BB⁻¹)A⁻¹ = I - ক্রম উল্টে যায়, ট্রান্সপোজের মতো।"),
    _q("A system of linear equations AX = B has a unique solution when…", ["det A ≠ 0", "det A = 0 and B = 0", "B = 0 only", "A is a zero matrix"],
       "Then X = A⁻¹B (Cramer's rule); with det A = 0 there are either no solutions or infinitely many.",
       "রৈখিক সমীকরণ-ব্যবস্থা AX = B-এর একক সমাধান থাকে যখন…", ["নির্ণায়ক A ≠ 0", "নির্ণায়ক A = 0 আর B = 0", "কেবল B = 0", "A শূন্য ম্যাট্রিক্স"],
       "তখন X = A⁻¹B (ক্র্যামারের নিয়ম); det A = 0 হলে হয় কোনো সমাধান নেই, নয় অসীম সংখ্যক।"),
    _q("At x = 0, the function f(x) = |x| is…", ["Continuous but not differentiable", "Differentiable but not continuous", "Neither continuous nor differentiable", "Both continuous and differentiable"],
       "The graph has a sharp corner: the left slope is -1 and the right slope is +1.",
       "x = 0-তে f(x) = |x| অপেক্ষকটি…", ["সন্তত কিন্তু অবকলনযোগ্য নয়", "অবকলনযোগ্য কিন্তু সন্তত নয়", "সন্তত বা অবকলনযোগ্য কোনোটাই নয়", "সন্তত আর অবকলনযোগ্য দুটোই"],
       "লেখচিত্রে একটা তীক্ষ্ণ কোণ: বাঁদিকের নতি -1 আর ডানদিকের +1।"),
    _q("Rolle's theorem needs f continuous on [a, b], differentiable on (a, b) and…", ["f(a) = f(b)", "f(a) = 0", "f'(a) = 0", "f increasing"],
       "Then some c in (a, b) has f'(c) = 0 - a horizontal tangent somewhere between.",
       "রোলের উপপাদ্যের জন্য f-কে [a, b]-তে সন্তত, (a, b)-তে অবকলনযোগ্য হতে হয়, আর…", ["f(a) = f(b)", "f(a) = 0", "f'(a) = 0", "f বর্ধমান"],
       "তখন (a, b)-র মধ্যে কোনো c-তে f'(c) = 0 - মাঝে কোথাও অনুভূমিক স্পর্শক।"),
    _q("The mean value theorem guarantees a point c in (a, b) where…", ["f'(c) = [f(b) - f(a)] ÷ (b - a)", "f(c) = 0", "f'(c) = 0 always", "f(c) = f(a) + f(b)"],
       "Somewhere the instantaneous slope equals the average slope of the chord.",
       "গড়মান উপপাদ্য (a, b)-তে এমন একটা বিন্দু c নিশ্চিত করে যেখানে…", ["f'(c) = [f(b) - f(a)] ÷ (b - a)", "f(c) = 0", "সবসময় f'(c) = 0", "f(c) = f(a) + f(b)"],
       "কোথাও তাৎক্ষণিক নতি জ্যা-এর গড় নতির সমান।"),
    _q("If f'(x) > 0 for every x in an interval, then on that interval f is…", ["Strictly increasing", "Strictly decreasing", "Constant", "Periodic"],
       "A positive derivative means the graph rises as x increases.",
       "কোনো অন্তরালের প্রতিটি x-এ f'(x) > 0 হলে ওই অন্তরালে f…", ["কঠোরভাবে বর্ধমান", "কঠোরভাবে হ্রাসমান", "ধ্রুবক", "পর্যাবৃত্ত"],
       "ধনাত্মক অবকলজ মানে x বাড়লে লেখচিত্র ওঠে।"),
    _q("At a point where f'(c) = 0 and f''(c) < 0, f has…", ["A local maximum", "A local minimum", "A point of inflection only", "No special feature"],
       "The second-derivative test: the curve is concave down at a stationary point, so it is a peak.",
       "যে বিন্দুতে f'(c) = 0 আর f''(c) < 0, সেখানে f-এর থাকে…", ["স্থানীয় চরম মান", "স্থানীয় অবম মান", "কেবল নতিবিন্দু", "বিশেষ কিছু নেই"],
       "দ্বিতীয় অবকলজ পরীক্ষা: স্থির বিন্দুতে বক্ররেখা নিচের দিকে অবতল, তাই চূড়া।"),
    _q("What is the integral of an odd function f from -a to a?", ["0", "2 x the integral from 0 to a", "f(a) - f(-a)", "a x f(a)"],
       "f(-x) = -f(x), so the areas on the two sides cancel; for an even function the integral doubles instead.",
       "-a থেকে a পর্যন্ত একটা অযুগ্ম অপেক্ষক f-এর সমাকল কত?", ["0", "0 থেকে a পর্যন্ত সমাকলের 2 গুণ", "f(a) - f(-a)", "a x f(a)"],
       "f(-x) = -f(x), তাই দুই পাশের ক্ষেত্রফল কাটাকাটি; যুগ্ম অপেক্ষকে বরং সমাকল দ্বিগুণ হয়।"),
    _q("What is the derivative of eˣ?", ["eˣ", "x eˣ⁻¹", "eˣ⁺¹", "1/x"],
       "eˣ is the only function (up to a constant multiple) equal to its own derivative.",
       "eˣ-এর অবকলজ কী?", ["eˣ", "x eˣ⁻¹", "eˣ⁺¹", "1/x"],
       "eˣ-ই একমাত্র অপেক্ষক (ধ্রুবক গুণিতক ছাড়া) যা নিজের অবকলজের সমান।"),
    _q("What is the integral of 1/x (for x > 0)?", ["ln x + C", "x⁻²/(-2) + C", "1/x² + C", "eˣ + C"],
       "The power rule fails for n = -1; d/dx (ln x) = 1/x fills that gap.",
       "1/x-এর সমাকল (x > 0-র জন্য) কী?", ["ln x + C", "x⁻²/(-2) + C", "1/x² + C", "eˣ + C"],
       "n = -1-এ ঘাত-নিয়ম খাটে না; d/dx (ln x) = 1/x সেই ফাঁক পূরণ করে।"),
    _q("What is the order and degree of the differential equation (d²y/dx²)³ + (dy/dx)² + y = 0?", ["Order 2, degree 3", "Order 3, degree 2", "Order 2, degree 2", "Order 1, degree 3"],
       "Order is the highest derivative (second); degree is the power of that derivative (3).",
       "অবকল সমীকরণ (d²y/dx²)³ + (dy/dx)² + y = 0-এর ক্রম আর মাত্রা কত?", ["ক্রম 2, মাত্রা 3", "ক্রম 3, মাত্রা 2", "ক্রম 2, মাত্রা 2", "ক্রম 1, মাত্রা 3"],
       "ক্রম হলো সর্বোচ্চ অবকলজ (দ্বিতীয়); মাত্রা হলো সেই অবকলজের ঘাত (3)।"),
    _q("Two lines with slopes m₁ and m₂ are perpendicular when…", ["m₁ x m₂ = -1", "m₁ = m₂", "m₁ + m₂ = 0", "m₁ x m₂ = 1"],
       "Parallel lines have equal slopes; perpendicular slopes are negative reciprocals (unless one line is vertical).",
       "m₁ আর m₂ নতির দুটো রেখা লম্ব হয় যখন…", ["m₁ x m₂ = -1", "m₁ = m₂", "m₁ + m₂ = 0", "m₁ x m₂ = 1"],
       "সমান্তরাল রেখার নতি সমান; লম্ব রেখার নতি পরস্পরের ঋণাত্মক অন্যোন্যক (যদি না একটা উল্লম্ব হয়)।"),
    _q("A tangent to a circle at a point is…", ["Perpendicular to the radius at that point", "Parallel to the radius", "Through the centre", "At 45° to the radius"],
       "So the tangent's slope is the negative reciprocal of the radius's slope.",
       "বৃত্তের কোনো বিন্দুতে স্পর্শক…", ["ওই বিন্দুতে ব্যাসার্ধের লম্ব", "ব্যাসার্ধের সমান্তরাল", "কেন্দ্র দিয়ে যায়", "ব্যাসার্ধের সঙ্গে 45° কোণে"],
       "তাই স্পর্শকের নতি ব্যাসার্ধের নতির ঋণাত্মক অন্যোন্যক।"),
    _q("What is the eccentricity of a parabola?", ["Exactly 1", "0", "Between 0 and 1", "Greater than 1"],
       "Every point is equally far from the focus and the directrix; a circle has e = 0, an ellipse 0 < e < 1, a hyperbola e > 1.",
       "অধিবৃত্তের উৎকেন্দ্রিকতা কত?", ["ঠিক 1", "0", "0 আর 1-এর মাঝে", "1-এর বেশি"],
       "প্রতিটি বিন্দু নাভি আর নিয়ামক থেকে সমান দূরে; বৃত্তে e = 0, উপবৃত্তে 0 < e < 1, পরাবৃত্তে e > 1।"),
    _q("For an ellipse, what is the sum of the distances from any point on it to the two foci?", ["2a, the length of the major axis", "2b", "a + b", "It varies from point to point"],
       "This constant sum is the gardener's-string definition of an ellipse.",
       "উপবৃত্তের যেকোনো বিন্দু থেকে দুই নাভির দূরত্বের যোগফল কত?", ["2a, পরাক্ষের দৈর্ঘ্য", "2b", "a + b", "বিন্দু অনুযায়ী বদলায়"],
       "এই ধ্রুবক যোগফলই উপবৃত্তের 'মালির সুতো' সংজ্ঞা।"),
    _q("Three vectors a, b and c are coplanar exactly when…", ["Their scalar triple product is zero", "Their cross products are equal", "They have the same length", "Each is perpendicular to the others"],
       "[a b c] is the volume of the box they span; zero volume means they lie in one plane.",
       "তিনটি ভেক্টর a, b আর c সমতলীয় হয় ঠিক তখনই যখন…", ["তাদের স্কেলার ত্রিগুণফল শূন্য", "তাদের ভেক্টর গুণফল সমান", "তাদের দৈর্ঘ্য সমান", "প্রত্যেকে অন্যদের লম্ব"],
       "[a b c] হলো তাদের গঠিত বাক্সের আয়তন; শূন্য আয়তন মানে তারা এক তলে।"),
    _q("If a · b = 0 for non-zero vectors a and b, then…", ["a and b are perpendicular", "a and b are parallel", "a = b", "a x b = 0"],
       "a · b = |a||b| cos θ, which vanishes only when θ = 90°.",
       "অশূন্য ভেক্টর a আর b-এর জন্য a · b = 0 হলে…", ["a আর b লম্ব", "a আর b সমান্তরাল", "a = b", "a x b = 0"],
       "a · b = |a||b| cos θ, যা কেবল θ = 90° হলে শূন্য।"),
    _q("What are the direction cosines of the z-axis?", ["(0, 0, 1)", "(1, 0, 0)", "(1, 1, 1)", "(0, 1, 0)"],
       "It makes angles 90°, 90° and 0° with the x-, y- and z-axes; l² + m² + n² = 1 always.",
       "z-অক্ষের দিক-কোসাইন কী?", ["(0, 0, 1)", "(1, 0, 0)", "(1, 1, 1)", "(0, 1, 0)"],
       "এটা x-, y- আর z-অক্ষের সঙ্গে 90°, 90° আর 0° কোণ করে; সবসময় l² + m² + n² = 1।"),
    _q("Two lines in space that are neither parallel nor intersecting are called…", ["Skew lines", "Coplanar lines", "Concurrent lines", "Collinear lines"],
       "Skew lines exist only in three dimensions; the shortest distance between them is along their common perpendicular.",
       "মহাশূন্যে যে দুটো রেখা সমান্তরালও নয়, ছেদও করে না, তাদের বলে…", ["নৈকতলীয় (স্কিউ) রেখা", "সমতলীয় রেখা", "সমবিন্দু রেখা", "সমরেখ রেখা"],
       "নৈকতলীয় রেখা কেবল ত্রিমাত্রায় থাকে; তাদের ন্যূনতম দূরত্ব সাধারণ লম্ব বরাবর।"),
    _q("Events A and B are independent when…", ["P(A ∩ B) = P(A) P(B)", "P(A ∩ B) = 0", "P(A) + P(B) = 1", "A is a subset of B"],
       "Knowing B happened does not change the chance of A. Mutually exclusive events (P(A ∩ B) = 0) are a different idea.",
       "ঘটনা A আর B স্বাধীন হয় যখন…", ["P(A ∩ B) = P(A) P(B)", "P(A ∩ B) = 0", "P(A) + P(B) = 1", "A, B-র উপসেট"],
       "B ঘটেছে জানলে A-র সম্ভাবনা বদলায় না। পরস্পর বর্জনশীল ঘটনা (P(A ∩ B) = 0) আলাদা ধারণা।"),
    _q("What is P(A | B), the probability of A given B?", ["P(A ∩ B) ÷ P(B)", "P(A) ÷ P(B)", "P(A) P(B)", "P(A ∪ B) ÷ P(A)"],
       "Restrict the sample space to B and see what share of it also lies in A.",
       "P(A | B), অর্থাৎ B দেওয়া থাকলে A-র সম্ভাবনা কী?", ["P(A ∩ B) ÷ P(B)", "P(A) ÷ P(B)", "P(A) P(B)", "P(A ∪ B) ÷ P(A)"],
       "নমুনাক্ষেত্রকে B-তে সীমিত করে দেখো তার কত অংশ A-তেও আছে।"),
    _q("For a binomial distribution with n trials and success probability p, what is the mean?", ["np", "np(1 - p)", "n/p", "p/n"],
       "The variance is np(1 - p); for 10 fair-coin tosses the mean number of heads is 5.",
       "n বার চেষ্টা আর সাফল্যের সম্ভাবনা p হলে দ্বিপদ বিন্যাসের গড় কত?", ["np", "np(1 - p)", "n/p", "p/n"],
       "ভেদাঙ্ক np(1 - p); 10 বার নিরপেক্ষ মুদ্রা ছুড়লে গড় হেডের সংখ্যা 5।"),
    _q("Adding the same constant to every value of a data set changes…", ["The mean, but not the variance", "The variance, but not the mean", "Both the mean and the variance", "Neither"],
       "Every value and the mean shift together, so all the deviations from the mean stay the same.",
       "একটা তথ্যসারির প্রতিটি মানে একই ধ্রুবক যোগ করলে কী বদলায়?", ["গড়, কিন্তু ভেদাঙ্ক নয়", "ভেদাঙ্ক, কিন্তু গড় নয়", "গড় আর ভেদাঙ্ক দুটোই", "কোনোটাই নয়"],
       "প্রতিটি মান আর গড় একসঙ্গে সরে, তাই গড় থেকে সব বিচ্যুতি একই থাকে।"),
    _q("What is the principal value of tan⁻¹(1)?", ["π/4", "π/2", "3π/4", "0"],
       "The principal range of tan⁻¹ is (-π/2, π/2), and tan(π/4) = 1.",
       "tan⁻¹(1)-এর মুখ্য মান কত?", ["π/4", "π/2", "3π/4", "0"],
       "tan⁻¹-এর মুখ্য পরিসর (-π/2, π/2), আর tan(π/4) = 1।"),
    _q("What is the principal range of sin⁻¹ x?", ["[-π/2, π/2]", "[0, π]", "(-π/2, π/2)", "[0, 2π]"],
       "Restricting sine to this interval makes it one-one, so it can be inverted; cos⁻¹ uses [0, π].",
       "sin⁻¹ x-এর মুখ্য পরিসর কী?", ["[-π/2, π/2]", "[0, π]", "(-π/2, π/2)", "[0, 2π]"],
       "এই অন্তরালে সাইনকে সীমিত করলে তা এক-এক হয়, তাই বিপরীত করা যায়; cos⁻¹-এর পরিসর [0, π]।"),
    _q("What is the general solution of sin x = 0?", ["x = nπ, n an integer", "x = 2nπ only", "x = nπ/2", "x = (2n + 1)π/2"],
       "Sine is zero at every multiple of π; cos x = 0 at odd multiples of π/2.",
       "sin x = 0 সমীকরণের সাধারণ সমাধান কী?", ["x = nπ, n পূর্ণসংখ্যা", "কেবল x = 2nπ", "x = nπ/2", "x = (2n + 1)π/2"],
       "π-এর প্রতিটি গুণিতকে সাইন শূন্য; cos x = 0 হয় π/2-এর বিজোড় গুণিতকে।"),
    _q("What is the value of sin²θ + cos²θ for every θ?", ["1", "0", "2", "It depends on θ"],
       "It is Pythagoras' theorem on the unit circle; dividing by cos²θ gives 1 + tan²θ = sec²θ.",
       "প্রতিটি θ-এর জন্য sin²θ + cos²θ-এর মান কত?", ["1", "0", "2", "θ-এর উপর নির্ভর করে"],
       "এটা একক বৃত্তে পিথাগোরাসের উপপাদ্য; cos²θ দিয়ে ভাগ করলে 1 + tan²θ = sec²θ।"),
    _q("What is the period of the function sin(2x)?", ["π", "2π", "π/2", "4π"],
       "sin(kx) has period 2π/k; here k = 2.",
       "sin(2x) অপেক্ষকের পর্যায় কত?", ["π", "2π", "π/2", "4π"],
       "sin(kx)-এর পর্যায় 2π/k; এখানে k = 2।"),
    _q("What is the contrapositive of 'If it rains, the ground is wet'?", ["If the ground is not wet, it did not rain", "If the ground is wet, it rained", "If it does not rain, the ground is not wet", "It rains and the ground is dry"],
       "The contrapositive of p → q is ~q → ~p, and it always has the same truth value as the original.",
       "'বৃষ্টি হলে মাটি ভেজে' বাক্যের বিপরীত-বিপরীতক (কন্ট্রাপজিটিভ) কী?", ["মাটি না ভিজলে বৃষ্টি হয়নি", "মাটি ভিজলে বৃষ্টি হয়েছে", "বৃষ্টি না হলে মাটি ভেজে না", "বৃষ্টি হচ্ছে আর মাটি শুকনো"],
       "p → q-এর বিপরীত-বিপরীতক ~q → ~p, আর মূল বাক্যের সঙ্গে এর সত্যমান সবসময় এক।"),
    _q("What is the negation of 'Every student passed'?", ["At least one student did not pass", "No student passed", "Every student failed", "Some students passed"],
       "The negation of 'for all x, P(x)' is 'there exists x with not P(x)'.",
       "'প্রত্যেক ছাত্র পাস করেছে'-এর নেতিকরণ কী?", ["অন্তত একজন ছাত্র পাস করেনি", "কোনো ছাত্র পাস করেনি", "প্রত্যেক ছাত্র ফেল করেছে", "কিছু ছাত্র পাস করেছে"],
       "'সব x-এর জন্য P(x)'-এর নেতিকরণ হলো 'এমন x আছে যার জন্য P(x) নয়'।"),
    _q("A compound statement that is true for every truth value of its parts is called…", ["A tautology", "A contradiction", "A contingency", "A converse"],
       "p ∨ ~p is a tautology; p ∧ ~p is a contradiction (always false).",
       "যে যৌগিক বাক্য তার অংশগুলোর প্রতিটি সত্যমানে সত্য, তাকে বলে…", ["স্বতঃসত্য (টটোলজি)", "স্ববিরোধ", "আকস্মিকতা", "বিপরীত"],
       "p ∨ ~p স্বতঃসত্য; p ∧ ~p স্ববিরোধ (সবসময় মিথ্যা)।"),
    _q("A relation that is reflexive, symmetric and transitive is called…", ["An equivalence relation", "A function", "A partial order", "An empty relation"],
       "It splits the set into equivalence classes, like 'has the same remainder when divided by 5'.",
       "যে সম্বন্ধ স্বসম, প্রতিসম আর সংক্রমণ, তাকে বলে…", ["সমতুল্যতা সম্বন্ধ", "অপেক্ষক", "আংশিক ক্রম", "শূন্য সম্বন্ধ"],
       "এটা সেটকে সমতুল্যতা-শ্রেণিতে ভাগ করে, যেমন '5 দিয়ে ভাগ করলে একই ভাগশেষ'।"),
    _q("A function f: A → B is a bijection when it is…", ["Both one-one and onto", "One-one only", "Onto only", "Constant"],
       "Only bijections have inverse functions; finite sets must then have the same number of elements.",
       "f: A → B অপেক্ষক দ্বিমুখী (বাইজেকশন) হয় যখন তা…", ["এক-এক আর উপরিচিত্রণ দুটোই", "কেবল এক-এক", "কেবল উপরিচিত্রণ", "ধ্রুবক"],
       "কেবল দ্বিমুখী অপেক্ষকেরই বিপরীত অপেক্ষক থাকে; সসীম সেট হলে উপাদান-সংখ্যা সমান হতেই হবে।"),
    _q("What is the domain of f(x) = √(4 - x²)?", ["[-2, 2]", "(-2, 2)", "All real numbers", "[0, 2]"],
       "The square root needs 4 - x² ≥ 0, so -2 ≤ x ≤ 2.",
       "f(x) = √(4 - x²)-এর সংজ্ঞার অঞ্চল কী?", ["[-2, 2]", "(-2, 2)", "সব বাস্তব সংখ্যা", "[0, 2]"],
       "বর্গমূলের জন্য 4 - x² ≥ 0 চাই, তাই -2 ≤ x ≤ 2।"),
    _q("A set has n elements. How many subsets does it have?", ["2ⁿ", "n²", "n!", "2n"],
       "Each element is either in or out of a subset: 2 choices, n times. That count includes the empty set and the set itself.",
       "একটা সেটে n উপাদান। এর কয়টি উপসেট আছে?", ["2ⁿ", "n²", "n!", "2n"],
       "প্রতিটি উপাদান উপসেটে থাকে বা থাকে না: 2টি পছন্দ, n বার। এতে শূন্য সেট আর সেটটা নিজেও আছে।"),
    _q("What does ⁿCᵣ + ⁿCᵣ₋₁ equal?", ["ⁿ⁺¹Cᵣ", "ⁿCᵣ₊₁", "ⁿ⁻¹Cᵣ", "2 ⁿCᵣ"],
       "Pascal's rule - each entry in Pascal's triangle is the sum of the two above it.",
       "ⁿCᵣ + ⁿCᵣ₋₁-এর মান কত?", ["ⁿ⁺¹Cᵣ", "ⁿCᵣ₊₁", "ⁿ⁻¹Cᵣ", "2 ⁿCᵣ"],
       "পাস্কালের নিয়ম - পাস্কালের ত্রিভুজের প্রতিটি সংখ্যা তার উপরের দুটোর যোগফল।"),
    _q("How many terms are there in the expansion of (a + b)ⁿ?", ["n + 1", "n", "2n", "n - 1"],
       "Powers of a run from n down to 0: that is n + 1 terms.",
       "(a + b)ⁿ-এর বিস্তারে কয়টি পদ থাকে?", ["n + 1", "n", "2n", "n - 1"],
       "a-এর ঘাত n থেকে 0 পর্যন্ত নামে: মোট n + 1টি পদ।"),
    _q("What is the limit of (eˣ - 1) ÷ x as x → 0?", ["1", "0", "e", "∞"],
       "It is the derivative of eˣ at x = 0, which is e⁰ = 1.",
       "x → 0 হলে (eˣ - 1) ÷ x-এর সীমা কত?", ["1", "0", "e", "∞"],
       "এটা x = 0-তে eˣ-এর অবকলজ, যা e⁰ = 1।"),
    _q("Which rule helps evaluate limits of the forms 0/0 or ∞/∞ using derivatives?", ["L'Hôpital's rule", "The chain rule", "Rolle's theorem", "Cramer's rule"],
       "Differentiate the top and bottom separately and take the limit again.",
       "কোন নিয়ম অবকলজ দিয়ে 0/0 বা ∞/∞ আকারের সীমা নির্ণয়ে সাহায্য করে?", ["ল'হসপিটালের নিয়ম", "শৃঙ্খল নিয়ম", "রোলের উপপাদ্য", "ক্র্যামারের নিয়ম"],
       "লব আর হরকে আলাদাভাবে অবকলন করে আবার সীমা নাও।"),
    _q("To integrate x eˣ, which method is used?", ["Integration by parts", "Substitution u = eˣ only", "Partial fractions", "It cannot be integrated"],
       "∫ u dv = uv - ∫ v du with u = x gives x eˣ - eˣ + C. The LIATE order helps choose u.",
       "x eˣ-এর সমাকলের জন্য কোন পদ্ধতি লাগে?", ["অংশায়ন পদ্ধতিতে সমাকলন", "কেবল u = eˣ প্রতিস্থাপন", "আংশিক ভগ্নাংশ", "সমাকলন করা যায় না"],
       "∫ u dv = uv - ∫ v du, u = x নিলে x eˣ - eˣ + C। LIATE ক্রম u বাছতে সাহায্য করে।"),
    _q("What happens at a point of inflection of a curve?", ["The second derivative changes sign there", "The first derivative is always zero there", "The function is undefined there", "The function has a maximum there"],
       "At an inflection point the curve switches between concave up and concave down.",
       "নতিবিন্দুতে কী ঘটে?", ["সেখানে দ্বিতীয় অবকলজের চিহ্ন বদলায়", "সেখানে প্রথম অবকলজ সবসময় শূন্য", "সেখানে অপেক্ষক অসংজ্ঞাত", "সেখানে অপেক্ষকের চরম মান"],
       "নতিবিন্দুতে বক্ররেখা উপরে-অবতল থেকে নিচে-অবতলে (বা উল্টো) বদলায়।"),
    _q("The rank of a 3 x 3 matrix whose determinant is non-zero is…", ["3", "0", "1", "2"],
       "All three rows are linearly independent, so the rank is full.",
       "যে 3 x 3 ম্যাট্রিক্সের নির্ণায়ক অশূন্য, তার র‍্যাঙ্ক কত?", ["3", "0", "1", "2"],
       "তিনটি সারিই রৈখিকভাবে স্বাধীন, তাই র‍্যাঙ্ক পূর্ণ।"),
    _q("A matrix A with Aᵀ = A is called…", ["Symmetric", "Skew-symmetric", "Orthogonal", "Singular"],
       "Its entries mirror across the main diagonal; every square matrix is the sum of a symmetric and a skew-symmetric part.",
       "যে ম্যাট্রিক্স A-তে Aᵀ = A, তাকে বলে…", ["প্রতিসম", "বিপ্রতিসম", "লম্ব (অর্থোগোনাল)", "ব্যতিক্রমী"],
       "এর উপাদান মুখ্য কর্ণ বরাবর প্রতিবিম্বিত; প্রতিটি বর্গ ম্যাট্রিক্স একটা প্রতিসম আর একটা বিপ্রতিসম অংশের যোগফল।"),
    _q("In how many ways can 5 different books be arranged on a shelf if two particular books must stay together?", ["48", "120", "24", "60"],
       "Glue the pair into one block: 4! arrangements, times 2! for the order inside the block = 48.",
       "দুটো নির্দিষ্ট বই সবসময় পাশাপাশি রাখতে হলে 5টি ভিন্ন বই তাকে কত ভাবে সাজানো যায়?", ["48", "120", "24", "60"],
       "জোড়াটাকে এক ব্লক ধরো: 4! বিন্যাস, ব্লকের ভেতরের ক্রমের জন্য 2! গুণ = 48।"),
    _q("How many 3-digit numbers with all digits different can be formed from 1, 2, 3, 4 and 5?", ["60", "125", "10", "120"],
       "Ordered choices without repetition: 5 x 4 x 3 = 60.",
       "1, 2, 3, 4 আর 5 দিয়ে সব অঙ্ক ভিন্ন রেখে কয়টি 3-অঙ্কের সংখ্যা তৈরি করা যায়?", ["60", "125", "10", "120"],
       "পুনরাবৃত্তি ছাড়া ক্রমযুক্ত বাছাই: 5 x 4 x 3 = 60।"),
    _q("A line makes intercepts 3 and 4 on the x- and y-axes. What is its equation?", ["x/3 + y/4 = 1", "3x + 4y = 1", "x/4 + y/3 = 1", "4x + 3y = 7"],
       "Intercept form x/a + y/b = 1, which is 4x + 3y = 12.",
       "একটা রেখা x- আর y-অক্ষে 3 আর 4 ছেদাংশ কাটে। এর সমীকরণ কী?", ["x/3 + y/4 = 1", "3x + 4y = 1", "x/4 + y/3 = 1", "4x + 3y = 7"],
       "ছেদাংশ রূপ x/a + y/b = 1, অর্থাৎ 4x + 3y = 12।"),
    _q("What is the angle between the lines y = x and y = -x?", ["90°", "45°", "60°", "0°"],
       "Their slopes are 1 and -1, whose product is -1.",
       "y = x আর y = -x রেখার মধ্যে কোণ কত?", ["90°", "45°", "60°", "0°"],
       "তাদের নতি 1 আর -1, গুণফল -1।"),
    _q("Which quadrant's points satisfy x < 0 and y > 0?", ["The second quadrant", "The first quadrant", "The third quadrant", "The fourth quadrant"],
       "Quadrants are numbered anticlockwise from (+, +); (-, +) is the second.",
       "x < 0 আর y > 0 শর্ত কোন পাদের বিন্দু মেনে চলে?", ["দ্বিতীয় পাদ", "প্রথম পাদ", "তৃতীয় পাদ", "চতুর্থ পাদ"],
       "(+, +) থেকে ঘড়ির কাঁটার বিপরীতে পাদ গোনা হয়; (-, +) দ্বিতীয়।"),
    _q("The median of the data 3, 9, 1, 7, 5 is…", ["5", "7", "3", "25"],
       "Sorted: 1, 3, 5, 7, 9 - the middle value is 5.",
       "তথ্য 3, 9, 1, 7, 5-এর মধ্যমা কত?", ["5", "7", "3", "25"],
       "সাজালে: 1, 3, 5, 7, 9 - মাঝের মান 5।"),
    _q("What is the probability of drawing an ace from a well-shuffled pack of 52 cards?", ["1/13", "1/52", "1/4", "4/13"],
       "There are 4 aces: 4/52 = 1/13.",
       "ভালো করে মেশানো 52 তাসের প্যাকেট থেকে একটা টেক্কা তোলার সম্ভাবনা কত?", ["1/13", "1/52", "1/4", "4/13"],
       "4টি টেক্কা আছে: 4/52 = 1/13।"),
    _q("Two events A and B are mutually exclusive. What is P(A ∪ B)?", ["P(A) + P(B)", "P(A) P(B)", "P(A) + P(B) - P(A) P(B)", "1"],
       "They cannot happen together, so P(A ∩ B) = 0 and nothing is double-counted.",
       "দুটো ঘটনা A আর B পরস্পর বর্জনশীল। P(A ∪ B) কত?", ["P(A) + P(B)", "P(A) P(B)", "P(A) + P(B) - P(A) P(B)", "1"],
       "তারা একসঙ্গে ঘটতে পারে না, তাই P(A ∩ B) = 0 আর কিছু দুবার গোনা হয় না।"),
    _q("What is the value of cos 0° + sin 90° + tan 45°?", ["3", "1", "2", "0"],
       "Each of the three terms equals 1.",
       "cos 0° + sin 90° + tan 45°-এর মান কত?", ["3", "1", "2", "0"],
       "তিনটি পদের প্রত্যেকটি 1।"),
    _q("What is sin(A + B)?", ["sin A cos B + cos A sin B", "sin A + sin B", "sin A sin B - cos A cos B", "cos A cos B + sin A sin B"],
       "The addition formula; cos(A + B) = cos A cos B - sin A sin B.",
       "sin(A + B) কত?", ["সাইন A কোসাইন B + কোসাইন A সাইন B", "সাইন A + সাইন B", "সাইন A সাইন B - কোসাইন A কোসাইন B", "কোসাইন A কোসাইন B + সাইন A সাইন B"],
       "যোগ-সূত্র; cos(A + B) = cos A cos B - sin A sin B।"),
    _q("In any triangle with sides a, b, c opposite angles A, B, C, which is the sine rule?", ["a/sin A = b/sin B = c/sin C", "a² = b² + c² always", "a sin A = b sin B", "a + b = c"],
       "Each ratio equals 2R, the diameter of the circumscribed circle.",
       "A, B, C কোণের বিপরীতে a, b, c বাহুযুক্ত যেকোনো ত্রিভুজে সাইন সূত্র কোনটা?", ["a/সাইন A = b/সাইন B = c/সাইন C", "সবসময় a² = b² + c²", "a সাইন A = b সাইন B", "a + b = c"],
       "প্রতিটি অনুপাত পরিবৃত্তের ব্যাস 2R-এর সমান।"),
    _q("Which function is its own inverse?", ["f(x) = 1/x (x ≠ 0)", "f(x) = x²", "f(x) = 2x", "f(x) = x + 1"],
       "f(f(x)) = 1/(1/x) = x; the graph is symmetric about the line y = x.",
       "কোন অপেক্ষক নিজেই নিজের বিপরীত?", ["f(x) = 1/x (x ≠ 0)", "f(x) = x²", "f(x) = 2x", "f(x) = x + 1"],
       "f(f(x)) = 1/(1/x) = x; লেখচিত্র y = x রেখার সাপেক্ষে প্রতিসম।"),
    _q("A vector of length 1 in the direction of a non-zero vector a is…", ["a ÷ |a|", "a x |a|", "|a| ÷ a", "a - |a|"],
       "Dividing by the magnitude keeps the direction and makes the length 1 - this is the unit vector â.",
       "অশূন্য ভেক্টর a-এর দিকে 1 দৈর্ঘ্যের ভেক্টর কোনটা?", ["a ÷ |a|", "a x |a|", "|a| ÷ a", "a - |a|"],
       "মান দিয়ে ভাগ করলে দিক একই থাকে আর দৈর্ঘ্য 1 হয় - এটাই একক ভেক্টর â।"),
    _q("The number of elements in the power set of a set with n elements is:", ["2ⁿ", "n²", "2n", "n!"],
       "Power set of {a,b,c} has 2³=8 subsets including ∅ and the full set.",
       "n উপাদানের একটা সেটের পাওয়ার সেটে উপাদান সংখ্যা:", ["2ⁿ", "n²", "2n", "n!"],
       "{a,b,c}-এর পাওয়ার সেটে ∅ ও পূর্ণ সেটসহ 2³=8 উপসেট আছে।"),
    _q("If A and B are two sets, then A ∪ B = A ∩ B if and only if:", ["A = B", "A ⊂ B", "B ⊂ A", "A and B are disjoint"],
       "A ∪ B = A ∩ B means every element in the union is also in the intersection, forcing A = B.",
       "যদি A ও B দুটো সেট হয়, তাহলে A ∪ B = A ∩ B হওয়ার শর্ত:", ["A = B", "A ⊂ B", "B ⊂ A", "A ও B পরস্পর-বিচ্ছিন্ন"],
       "A ∪ B = A ∩ B মানে মিলন সেটের প্রতিটা উপাদান ছেদেও আছে, তাই A = B বাধ্য।"),
    _q("The modulus of the complex number 3 + 4i is:", ["5", "7", "1", "12"],
       "|3+4i| = √(3²+4²) = √25 = 5 (3-4-5 Pythagorean triple).",
       "জটিল সংখ্যা 3 + 4i-এর মডুলাস:", ["5", "7", "1", "12"],
       "|3+4i| = √(3²+4²) = √25 = 5 (3-4-5 পিথাগোরিয়ান ত্রিক)।"),
    _q("The argument (angle) of the complex number −1 + i√3 is:", ["2π/3 (120°)", "π/3", "π/6", "5π/6"],
       "The point is in the second quadrant: r=2, tan α = √3 → α = π/3, angle = π − π/3 = 2π/3.",
       "জটিল সংখ্যা −1 + i√3-এর আর্গুমেন্ট (কোণ):", ["2π/3 (120°)", "π/3", "π/6", "5π/6"],
       "বিন্দুটি দ্বিতীয় চতুর্ভাগে: r=2, tan α = √3 → α = π/3, কোণ = π − π/3 = 2π/3।"),
    _q("The sum of the roots and the product of the roots of ax² + bx + c = 0 are:", ["Sum = −b/a, Product = c/a (Vieta's formulas)", "Sum = b/a, Product = −c/a", "Sum = c/a, Product = b/a", "Sum = −c/a, Product = b/a"],
       "Vieta: if roots are α, β then α+β = −b/a and αβ = c/a.",
       "ax² + bx + c = 0-এর মূলদ্বয়ের যোগফল ও গুণফল:", ["যোগ = −b/a, গুণ = c/a (ভিয়েটার সূত্র)", "যোগ = b/a, গুণ = −c/a", "যোগ = c/a, গুণ = b/a", "যোগ = −c/a, গুণ = b/a"],
       "ভিয়েটা: মূল α, β হলে α+β = −b/a আর αβ = c/a।"),
    _q("Discriminant D = b² − 4ac. The roots are real and equal when:", ["D = 0", "D > 0", "D < 0", "D > 1"],
       "D = 0: double root x = −b/2a. Example: x² − 6x + 9 = 0 has double root x = 3.",
       "বিভেদক D = b² − 4ac। মূলদ্বয় বাস্তব ও সমান হলে:", ["D = 0", "D > 0", "D < 0", "D > 1"],
       "D = 0: দ্বি-মূল x = −b/2a। উদাহরণ: x² − 6x + 9 = 0-এর দ্বি-মূল x = 3।"),
    _q("The 10th term of the arithmetic progression 5, 8, 11, … is:", ["32", "30", "35", "29"],
       "a=5, d=3, T₁₀ = 5 + 9×3 = 5 + 27 = 32.",
       "সমান্তর প্রগতি 5, 8, 11, …-এর 10তম পদ:", ["32", "30", "35", "29"],
       "a=5, d=3, T₁₀ = 5 + 9×3 = 5 + 27 = 32।"),
    _q("The sum of the first n terms of a GP with first term a and ratio r (r ≠ 1) is:", ["Sₙ = a(rⁿ−1)/(r−1)", "Sₙ = a(rⁿ+1)/(r+1)", "Sₙ = an/(r−1)", "Sₙ = a/(1−r)"],
       "For |r|<1 and n→∞: S_∞ = a/(1−r) (sum of infinite GP).",
       "প্রথম পদ a ও অনুপাত r (r ≠ 1) সহ GP-এর প্রথম n পদের যোগফল:", ["Sₙ = a(rⁿ−1)/(r−1)", "Sₙ = a(rⁿ+1)/(r+1)", "Sₙ = an/(r−1)", "Sₙ = a/(1−r)"],
       "|r|<1 ও n→∞ হলে: S_∞ = a/(1−r) (অসীম GP-এর যোগফল)।"),
    _q("The number of ways to arrange the letters of the word 'BRIDGE' is:", ["720 (6! = 720 since all letters are distinct)", "360", "120", "5040"],
       "6 distinct letters → 6! = 720. If repeated letters existed, we'd divide by their factorials.",
       "'BRIDGE' শব্দের অক্ষরগুলো সাজানোর উপায়:", ["720 (6! = 720, সব অক্ষর আলাদা)", "360", "120", "5040"],
       "6 আলাদা অক্ষর → 6! = 720। পুনরাবৃত্তি থাকলে সেগুলোর ফ্যাক্টরিয়াল দিয়ে ভাগ করতাম।"),
    _q("How many ways can a committee of 3 be chosen from 8 people?", ["56 (₈C₃ = 8!/(3!·5!) = 56)", "24", "336", "512"],
       "₈C₃ = (8×7×6)/(3×2×1) = 336/6 = 56.",
       "8 জনের মধ্যে থেকে 3 জনের কমিটি গঠনের উপায়:", ["56 (₈C₃ = 56)", "24", "336", "512"],
       "₈C₃ = (8×7×6)/(3×2×1) = 56।"),
    _q("In the expansion of (1 + x)ⁿ, the coefficient of xʳ is:", ["ⁿCᵣ = n!/[r!(n−r)!]", "ⁿPᵣ", "n!/(n−r)!", "rⁿ"],
       "Binomial theorem: (1+x)ⁿ = Σ ⁿCᵣ xʳ. Coefficient of x³ in (1+x)⁵ is ⁵C₃ = 10.",
       "(1 + x)ⁿ বিস্তারে xʳ-এর সহগ:", ["ⁿCᵣ = n!/[r!(n−r)!]", "ⁿPᵣ", "n!/(n−r)!", "rⁿ"],
       "দ্বিপদী উপপাদ্য: (1+x)ⁿ = Σ ⁿCᵣ xʳ। (1+x)⁵-এ x³-এর সহগ ⁵C₃ = 10।"),
    _q("The general term of (a + b)ⁿ is:", ["T_{r+1} = ⁿCᵣ aⁿ⁻ʳ bʳ", "T_r = ⁿCᵣ aʳ bⁿ⁻ʳ", "T_r = ⁿPᵣ aⁿ bʳ", "T_r = n!/r!"],
       "The middle term (n even) is T_{n/2 + 1} — useful for finding the term independent of x.",
       "(a + b)ⁿ-এর সাধারণ পদ:", ["T_{r+1} = ⁿCᵣ aⁿ⁻ʳ bʳ", "T_r = ⁿCᵣ aʳ bⁿ⁻ʳ", "T_r = ⁿPᵣ aⁿ bʳ", "T_r = n!/r!"],
       "মধ্যপদ (n জোড়) T_{n/2 + 1} — x-মুক্ত পদ খুঁজতে কাজে লাগে।"),
    _q("The limit lim(x→0) (eˣ − 1)/x = ?", ["1", "0", "e", "∞"],
       "By L'Hôpital or Taylor series: eˣ = 1 + x + x²/2 +… → (eˣ−1)/x → 1 as x→0.",
       "lim(x→0) (eˣ − 1)/x = ?", ["1", "0", "e", "∞"],
       "L'Hôpital বা টেলর শ্রেণি: eˣ = 1 + x + x²/2 +… → x→0-এ (eˣ−1)/x → 1।"),
    _q("lim(x→∞) (1 + 1/x)ˣ equals:", ["e ≈ 2.718", "1", "∞", "0"],
       "This is the definition of e. More generally lim(1 + k/x)ˣ = eᵏ.",
       "lim(x→∞) (1 + 1/x)ˣ =", ["e ≈ 2.718", "1", "∞", "0"],
       "এটাই e-এর সংজ্ঞা। আরও সাধারণভাবে lim(1 + k/x)ˣ = eᵏ।"),
    _q("The derivative of sin x is:", ["cos x", "−cos x", "−sin x", "sec²x"],
       "d/dx(sin x) = cos x; d/dx(cos x) = −sin x. Trigonometric derivatives appear in wave analysis for bridges.",
       "sin x-এর অবকল:", ["cos x", "−cos x", "−sin x", "sec²x"],
       "d/dx(sin x) = cos x; d/dx(cos x) = −sin x। ত্রিকোণমিতিক অবকল সেতুর তরঙ্গ বিশ্লেষণে দেখা দেয়।"),
    _q("If y = ln x, then dy/dx = ?", ["1/x", "x", "eˣ", "ln x / x"],
       "d/dx(ln x) = 1/x (x > 0). Appears in compound interest and exponential growth formulas.",
       "y = ln x হলে dy/dx = ?", ["1/x", "x", "eˣ", "ln x / x"],
       "d/dx(ln x) = 1/x (x > 0)। চক্রবৃদ্ধি সুদ ও সূচকীয় বৃদ্ধির সূত্রে দেখা যায়।"),
    _q("A function f has a local maximum at x = a if:", ["f'(a) = 0 and f''(a) < 0 (negative second derivative)", "f'(a) = 0 and f''(a) > 0", "f'(a) > 0", "f(a) = 0"],
       "f''(a) < 0: the function is concave down at a. f''(a) > 0 gives a local minimum.",
       "f অপেক্ষকের x = a-তে স্থানীয় সর্বোচ্চ থাকলে:", ["f'(a) = 0 আর f''(a) < 0 (ঋণাত্মক দ্বিতীয় অবকল)", "f'(a) = 0 আর f''(a) > 0", "f'(a) > 0", "f(a) = 0"],
       "f''(a) < 0: a-তে অপেক্ষক অবতল নিচে। f''(a) > 0 স্থানীয় সর্বনিম্ন দেয়।"),
    _q("The integral ∫ cos x dx = ?", ["sin x + C", "−sin x + C", "cos x + C", "tan x + C"],
       "Standard result: ∫cos x dx = sin x + C. Verify: d/dx(sin x) = cos x ✓",
       "∫ cos x dx = ?", ["sin x + C", "−sin x + C", "cos x + C", "tan x + C"],
       "প্রমিত ফলাফল: ∫cos x dx = sin x + C। যাচাই: d/dx(sin x) = cos x ✓"),
    _q("∫₀^(π/2) sin x dx = ?", ["1", "0", "π/2", "2"],
       "[−cos x]₀^(π/2) = −cos(π/2) − (−cos 0) = 0 − (−1) = 1.",
       "∫₀^(π/2) sin x dx = ?", ["1", "0", "π/2", "2"],
       "[−cos x]₀^(π/2) = −cos(π/2) − (−cos 0) = 0 − (−1) = 1।"),
    _q("The area between y = x² and y = x (where x² ≤ x, i.e. 0 ≤ x ≤ 1) is:", ["1/6", "1/2", "1/3", "1/4"],
       "∫₀¹(x − x²)dx = [x²/2 − x³/3]₀¹ = 1/2 − 1/3 = 1/6.",
       "y = x² ও y = x-এর মধ্যবর্তী ক্ষেত্রফল (0 ≤ x ≤ 1):", ["1/6", "1/2", "1/3", "1/4"],
       "∫₀¹(x − x²)dx = [x²/2 − x³/3]₀¹ = 1/2 − 1/3 = 1/6।"),
    _q("The general solution of dy/dx = y is:", ["y = Ceˣ (exponential growth)", "y = Cx", "y = C + eˣ", "y = Ce^(−x)"],
       "Separate: dy/y = dx → ln|y| = x + const → y = Ceˣ.",
       "dy/dx = y-এর সাধারণ সমাধান:", ["y = Ceˣ (সূচকীয় বৃদ্ধি)", "y = Cx", "y = C + eˣ", "y = Ce^(−x)"],
       "পৃথক করে: dy/y = dx → ln|y| = x + ধ্রুবক → y = Ceˣ।"),
    _q("The differential equation of simple harmonic motion d²x/dt² + ω²x = 0 has solution:", ["x = A cos(ωt + φ)", "x = Aeωt", "x = At + B", "x = A/t"],
       "The general solution combines sin and cos: x = A cos ωt + B sin ωt = R cos(ωt + φ).",
       "সরল ছন্দিত গতির অবকল সমীকরণ d²x/dt² + ω²x = 0-এর সমাধান:", ["x = A cos(ωt + φ)", "x = Aeωt", "x = At + B", "x = A/t"],
       "সাধারণ সমাধান sin ও cos মেলায়: x = A cos ωt + B sin ωt = R cos(ωt + φ)।"),
    _q("The equation of a circle with centre (h, k) and radius r is:", ["(x−h)² + (y−k)² = r²", "(x+h)² + (y+k)² = r²", "x² + y² = r²", "(x−h)/(y−k) = r"],
       "General form: x² + y² + 2gx + 2fy + c = 0 where centre = (−g, −f), r² = g²+f²−c.",
       "কেন্দ্র (h, k) ও ব্যাসার্ধ r-এর বৃত্তের সমীকরণ:", ["(x−h)² + (y−k)² = r²", "(x+h)² + (y+k)² = r²", "x² + y² = r²", "(x−h)/(y−k) = r"],
       "সাধারণ রূপ: x² + y² + 2gx + 2fy + c = 0 যেখানে কেন্দ্র = (−g, −f), r² = g²+f²−c।"),
    _q("The eccentricity of a parabola y² = 4ax is:", ["e = 1", "e = 0", "e > 1", "e < 1"],
       "Parabola: e=1 always. Ellipse: 0<e<1, circle: e=0, hyperbola: e>1.",
       "পরাবৃত্ত y² = 4ax-এর উৎকেন্দ্রিকতা:", ["e = 1", "e = 0", "e > 1", "e < 1"],
       "পরাবৃত্ত: e=1 সবসময়। উপবৃত্ত: 0<e<1, বৃত্ত: e=0, অতিবৃত্ত: e>1।"),
    _q("The point on the parabola y² = 4ax closest to the directrix x = −a is the vertex:", ["(0, 0)", "(a, 0)", "(2a, 0)", "(−a, 0)"],
       "The vertex is at the origin, equidistant from focus (a,0) and directrix x=−a.",
       "পরাবৃত্ত y² = 4ax-এ নির্দেশরেখা x = −a-এর সবচেয়ে কাছের বিন্দু:", ["(0, 0)", "(a, 0)", "(2a, 0)", "(−a, 0)"],
       "শীর্ষবিন্দু মূলবিন্দুতে, নাভি (a,0) ও নির্দেশরেখা x=−a থেকে সমদূরে।"),
    _q("For vectors a and b, |a × b| = ?", ["|a||b|sin θ (area of parallelogram spanned by a and b)", "|a||b|cos θ", "|a|+|b|", "|a|²|b|"],
       "Cross product magnitude = |a||b|sin θ. Direction: perpendicular to both (right-hand rule).",
       "ভেক্টর a ও b-এর জন্য |a × b| = ?", ["|a||b|sin θ (a ও b-দ্বারা বিস্তৃত সামান্তরিকের ক্ষেত্রফল)", "|a||b|cos θ", "|a|+|b|", "|a|²|b|"],
       "ক্রস গুণফলের মাত্রা = |a||b|sin θ। দিক: উভয়ের লম্ব (ডান-হাতের নিয়ম)।"),
    _q("The projection of vector a onto vector b is:", ["(a·b)/|b|", "(a·b)/|a|", "|a||b|/cos θ", "|a×b|/|b|"],
       "Scalar projection = a·b̂ = (a·b)/|b|; vector projection = [(a·b)/|b|²] b.",
       "ভেক্টর a-এর ভেক্টর b-এর উপর প্রক্ষেপ:", ["(a·b)/|b|", "(a·b)/|a|", "|a||b|/cos θ", "|a×b|/|b|"],
       "স্কেলার প্রক্ষেপ = a·b̂ = (a·b)/|b|; ভেক্টর প্রক্ষেপ = [(a·b)/|b|²] b।"),
    _q("The angle between two lines with direction cosines l₁,m₁,n₁ and l₂,m₂,n₂ satisfies:", ["cos θ = |l₁l₂ + m₁m₂ + n₁n₂|", "cos θ = l₁/l₂ + m₁/m₂", "sin θ = l₁l₂ + m₁m₂ + n₁n₂", "tan θ = (l₁−l₂)/(l₁+l₂)"],
       "For perpendicular lines: l₁l₂ + m₁m₂ + n₁n₂ = 0. Used in 3D bridge truss analysis.",
       "দিক-কোসাইন l₁,m₁,n₁ ও l₂,m₂,n₂ সহ দুই রেখার মধ্যবর্তী কোণ:", ["cos θ = |l₁l₂ + m₁m₂ + n₁n₂|", "cos θ = l₁/l₂ + m₁/m₂", "sin θ = l₁l₂ + m₁m₂ + n₁n₂", "tan θ = (l₁−l₂)/(l₁+l₂)"],
       "লম্ব রেখার জন্য: l₁l₂ + m₁m₂ + n₁n₂ = 0। 3D সেতু ট্রাস বিশ্লেষণে ব্যবহার।"),
    _q("The equation of a plane passing through (x₁,y₁,z₁) with normal n=(a,b,c) is:", ["a(x−x₁) + b(y−y₁) + c(z−z₁) = 0", "ax+by+cz = x₁+y₁+z₁", "a/x+b/y+c/z = 1", "a(x+x₁) + b(y+y₁) = 0"],
       "The intercept form x/p + y/q + z/r = 1 is used for planes cutting the coordinate axes.",
       "(x₁,y₁,z₁) দিয়ে যাওয়া অভিলম্ব n=(a,b,c) সহ সমতলের সমীকরণ:", ["a(x−x₁) + b(y−y₁) + c(z−z₁) = 0", "ax+by+cz = x₁+y₁+z₁", "a/x+b/y+c/z = 1", "a(x+x₁) + b(y+y₁) = 0"],
       "অন্তঃখণ্ড রূপ x/p + y/q + z/r = 1 অক্ষ কর্তনকারী সমতলে ব্যবহার।"),
    _q("In probability, P(A ∪ B) = P(A) + P(B) − P(A ∩ B). If P(A)=0.4, P(B)=0.5, P(A∩B)=0.2, then P(A∪B) = ?", ["0.7", "0.9", "0.6", "0.2"],
       "P(A∪B) = 0.4 + 0.5 − 0.2 = 0.7.",
       "P(A)=0.4, P(B)=0.5, P(A∩B)=0.2 হলে P(A∪B) = ?", ["0.7", "0.9", "0.6", "0.2"],
       "P(A∪B) = 0.4 + 0.5 − 0.2 = 0.7।"),
    _q("A bag has 4 red and 6 blue balls. A ball is drawn at random. P(red) = ?", ["0.4", "0.6", "0.25", "0.5"],
       "P(red) = 4/10 = 0.4.",
       "একটা থলিতে 4 লাল ও 6 নীল বল। এলোমেলোভাবে একটা বল তোলা হল। P(লাল) = ?", ["0.4", "0.6", "0.25", "0.5"],
       "P(লাল) = 4/10 = 0.4।"),
    _q("For mutually exclusive events A and B: P(A ∪ B) = ?", ["P(A) + P(B)", "P(A)·P(B)", "P(A) + P(B) − P(A)P(B)", "P(A)/P(B)"],
       "Mutually exclusive: P(A∩B) = 0, so P(A∪B) = P(A)+P(B) by inclusion-exclusion.",
       "পরস্পর-বিচ্ছিন্ন ঘটনা A ও B-এর জন্য: P(A ∪ B) = ?", ["P(A) + P(B)", "P(A)·P(B)", "P(A) + P(B) − P(A)P(B)", "P(A)/P(B)"],
       "পরস্পর-বিচ্ছিন্ন: P(A∩B) = 0, তাই P(A∪B) = P(A)+P(B)।"),
    _q("The mean of the data 2, 4, 6, 8, 10 is:", ["6", "5", "7", "30"],
       "Mean = (2+4+6+8+10)/5 = 30/5 = 6.",
       "তথ্য 2, 4, 6, 8, 10-এর গড়:", ["6", "5", "7", "30"],
       "গড় = (2+4+6+8+10)/5 = 30/5 = 6।"),
    _q("The standard deviation of 2, 4, 6, 8, 10 (mean = 6) is:", ["√8 ≈ 2.83", "√6", "4", "2"],
       "σ² = [(2−6)²+(4−6)²+(6−6)²+(8−6)²+(10−6)²]/5 = [16+4+0+4+16]/5 = 40/5 = 8; σ = √8.",
       "2, 4, 6, 8, 10 (গড় = 6)-এর প্রমাণ বিচ্যুতি:", ["√8 ≈ 2.83", "√6", "4", "2"],
       "σ² = [16+4+0+4+16]/5 = 8; σ = √8।"),
    _q("The value of cos 0° + cos 90° + cos 180° + cos 270° is:", ["0", "1", "−1", "2"],
       "1 + 0 + (−1) + 0 = 0.",
       "cos 0° + cos 90° + cos 180° + cos 270°-এর মান:", ["0", "1", "−1", "2"],
       "1 + 0 + (−1) + 0 = 0।"),
    _q("The principal value range of arccos is:", ["[0, π]", "[−π/2, π/2]", "(0, π)", "[0, 2π]"],
       "arccos is defined on [−1,1] with values in [0,π]. arcsin uses [−π/2, π/2].",
       "arccos-এর প্রধান মান পরিসর:", ["[0, π]", "[−π/2, π/2]", "(0, π)", "[0, 2π]"],
       "arccos [−1,1]-এ সংজ্ঞায়িত, মান [0,π]-এ। arcsin ব্যবহার করে [−π/2, π/2]।"),
    _q("sin²θ + cos²θ = ?", ["1 (Pythagorean identity)", "0", "sin 2θ", "2"],
       "Fundamental identity. Dividing by cos²θ: tan²θ + 1 = sec²θ. Dividing by sin²θ: 1 + cot²θ = csc²θ.",
       "sin²θ + cos²θ = ?", ["1 (পিথাগোরিয়ান অভেদ)", "0", "sin 2θ", "2"],
       "মৌলিক অভেদ। cos²θ দিয়ে ভাগ: tan²θ + 1 = sec²θ। sin²θ দিয়ে ভাগ: 1 + cot²θ = csc²θ।"),
    _q("The general solution of sin x = 0 is:", ["x = nπ, n ∈ ℤ", "x = 2nπ", "x = (2n+1)π/2", "x = nπ/2"],
       "sin nπ = 0 for all integers n. The solution is {0, ±π, ±2π, …}.",
       "sin x = 0-এর সাধারণ সমাধান:", ["x = nπ, n ∈ ℤ", "x = 2nπ", "x = (2n+1)π/2", "x = nπ/2"],
       "সব পূর্ণসংখ্যা n-এর জন্য sin nπ = 0। সমাধান {0, ±π, ±2π, …}।"),
    _q("A 2×2 matrix A has det(A) = ad − bc. Matrix A = [[2, 3],[1, 4]] has determinant:", ["5", "11", "−5", "8"],
       "det = 2×4 − 3×1 = 8 − 3 = 5.",
       "2×2 ম্যাট্রিক্স A-এর det(A) = ad − bc। A = [[2, 3],[1, 4]]-এর নির্ধারক:", ["5", "11", "−5", "8"],
       "det = 2×4 − 3×1 = 8 − 3 = 5।"),
    _q("The inverse of a 2×2 matrix [[a,b],[c,d]] (when ad−bc ≠ 0) is:", ["(1/det)×[[d,−b],[−c,a]]", "(1/det)×[[a,−c],[−b,d]]", "[[d,b],[c,a]]", "[[1/a,0],[0,1/d]]"],
       "A⁻¹ = (1/det(A)) × adjugate. Verify A·A⁻¹ = I.",
       "2×2 ম্যাট্রিক্স [[a,b],[c,d]] (যখন ad−bc ≠ 0)-এর বিপরীত:", ["(1/det)×[[d,−b],[−c,a]]", "(1/det)×[[a,−c],[−b,d]]", "[[d,b],[c,a]]", "[[1/a,0],[0,1/d]]"],
       "A⁻¹ = (1/det(A)) × অ্যাডজুগেট। A·A⁻¹ = I যাচাই করুন।"),
    _q("If A is a 2×3 matrix and B is a 3×4 matrix, the product AB has order:", ["2×4", "3×3", "2×3", "3×4"],
       "Matrix multiplication: (m×n)(n×p) = (m×p). Inner dimensions must match.",
       "A যদি 2×3 ম্যাট্রিক্স আর B 3×4 ম্যাট্রিক্স হয়, তাহলে AB-এর ক্রম:", ["2×4", "3×3", "2×3", "3×4"],
       "ম্যাট্রিক্স গুণ: (m×n)(n×p) = (m×p)। অভ্যন্তরীণ মাত্রা মিলতে হবে।"),
    _q("The slope of the tangent to the curve y = 2x³ − 3x at x = 1 is:", ["3", "−1", "6", "1"],
       "dy/dx = 6x² − 3; at x=1: 6(1)−3 = 3.",
       "y = 2x³ − 3x বক্ররেখায় x = 1-এ স্পর্শকের ঢাল:", ["3", "−1", "6", "1"],
       "dy/dx = 6x² − 3; x=1-এ: 6(1)−3 = 3।"),
    _q("The maximum value of f(x) = −x² + 4x − 3 is:", ["1 (at x = 2)", "3", "−3", "4"],
       "f'(x) = −2x+4 = 0 → x=2; f(2) = −4+8−3 = 1. f''(2)=−2 < 0 confirms maximum.",
       "f(x) = −x² + 4x − 3-এর সর্বোচ্চ মান:", ["1 (x = 2-এ)", "3", "−3", "4"],
       "f'(x) = −2x+4 = 0 → x=2; f(2) = −4+8−3 = 1। f''(2)=−2 < 0 সর্বোচ্চ নিশ্চিত।"),
    _q("The length of the latus rectum of the ellipse x²/a² + y²/b² = 1 (a > b) is:", ["2b²/a", "2a²/b", "2ab", "b²/a"],
       "Latus rectum = chord through focus perpendicular to major axis. Length = 2b²/a.",
       "উপবৃত্ত x²/a² + y²/b² = 1 (a > b)-এর লেটাস রেকটামের দৈর্ঘ্য:", ["2b²/a", "2a²/b", "2ab", "b²/a"],
       "লেটাস রেকটাম = নাভির মধ্য দিয়ে প্রধান অক্ষের লম্ব জ্যা। দৈর্ঘ্য = 2b²/a।"),
    _q("The equation of the tangent to the circle x² + y² = r² at point (x₁, y₁) on the circle is:", ["x·x₁ + y·y₁ = r²", "x/x₁ + y/y₁ = r", "x−x₁ = m(y−y₁)", "x²+y²=x₁²+y₁²"],
       "T = 0 rule for conics: substitute (x,x₁) → (x·x₁), etc.",
       "বৃত্ত x² + y² = r²-এর উপরিস্থ বিন্দু (x₁, y₁)-এ স্পর্শকের সমীকরণ:", ["x·x₁ + y·y₁ = r²", "x/x₁ + y/y₁ = r", "x−x₁ = m(y−y₁)", "x²+y²=x₁²+y₁²"],
       "কনিকে T = 0 নিয়ম: (x,x₁) → (x·x₁) ইত্যাদি প্রতিস্থাপন।"),
    _q("The value of i⁴ⁿ (where n is a positive integer) is:", ["1", "i", "−1", "−i"],
       "i¹=i, i²=−1, i³=−i, i⁴=1. The cycle repeats every 4: i⁴ⁿ = (i⁴)ⁿ = 1ⁿ = 1.",
       "i⁴ⁿ-এর মান (n ধনাত্মক পূর্ণসংখ্যা):", ["1", "i", "−1", "−i"],
       "i¹=i, i²=−1, i³=−i, i⁴=1। চক্র 4-এ পুনরাবৃত্তি: i⁴ⁿ = 1ⁿ = 1।"),
    _q("The number of terms in the expansion of (a + b)ⁿ is:", ["n + 1", "n", "2n", "n − 1"],
       "Expansion: T₁, T₂, …, T_{n+1} — one more than the exponent.",
       "(a + b)ⁿ বিস্তারে পদের সংখ্যা:", ["n + 1", "n", "2n", "n − 1"],
       "বিস্তার: T₁, T₂, …, T_{n+1} — ঘাতের চেয়ে একটা বেশি।"),
    _q("If P(A|B) = P(A∩B)/P(B), then for independent events A and B:", ["P(A|B) = P(A) (B gives no information about A)", "P(A|B) = P(B)", "P(A|B) = 0", "P(A|B) = P(A) + P(B)"],
       "Independence: P(A∩B) = P(A)P(B), so P(A|B) = P(A)P(B)/P(B) = P(A).",
       "P(A|B) = P(A∩B)/P(B) হলে স্বাধীন ঘটনা A ও B-এর জন্য:", ["P(A|B) = P(A) (B, A সম্পর্কে কোনো তথ্য দেয় না)", "P(A|B) = P(B)", "P(A|B) = 0", "P(A|B) = P(A) + P(B)"],
       "স্বাধীনতা: P(A∩B) = P(A)P(B), তাই P(A|B) = P(A)।"),
    _q("The scalar triple product a · (b × c) gives:", ["The volume of the parallelepiped formed by a, b, c", "Zero always", "The area of a triangle", "The sum of the three vectors"],
       "V = |a · (b × c)|. If the triple product is 0, the three vectors are coplanar.",
       "স্কেলার ত্রৈরাশিক গুণফল a · (b × c) দেয়:", ["a, b, c দ্বারা গঠিত সমান্তরষষ্ঠফলকের আয়তন", "সবসময় শূন্য", "ত্রিভুজের ক্ষেত্রফল", "তিনটি ভেক্টরের যোগফল"],
       "V = |a · (b × c)|। ত্রৈরাশিক গুণফল 0 হলে তিনটি ভেক্টর সমতলীয়।"),
    _q("The distance between the parallel lines ax + by + c₁ = 0 and ax + by + c₂ = 0 is:", ["|c₁ − c₂| / √(a² + b²)", "|c₁ − c₂| / (a + b)", "|c₁ + c₂| / √(a² + b²)", "√(a² + b²) / |c₁ − c₂|"],
       "Standard formula for distance between parallel lines. Used in railway track geometry on bridges.",
       "সমান্তরাল রেখা ax+by+c₁=0 ও ax+by+c₂=0-এর মধ্যবর্তী দূরত্ব:", ["|c₁ − c₂| / √(a² + b²)", "|c₁ − c₂| / (a + b)", "|c₁ + c₂| / √(a² + b²)", "√(a² + b²) / |c₁ − c₂|"],
       "সমান্তরাল রেখার দূরত্বের প্রমিত সূত্র। সেতুতে রেললাইন জ্যামিতিতে ব্যবহার।"),
    _q("The sum of an infinite geometric series |r| < 1 is:", ["a/(1−r)", "a/(1+r)", "ar/(1−r)", "a·r"],
       "S_∞ = a/(1−r). Example: 1 + 1/2 + 1/4 +… = 1/(1−1/2) = 2.",
       "অসীম গুণোত্তর শ্রেণির যোগফল |r| < 1 হলে:", ["a/(1−r)", "a/(1+r)", "ar/(1−r)", "a·r"],
       "S_∞ = a/(1−r)। উদাহরণ: 1 + 1/2 + 1/4 +… = 2।"),
    _q("The Harmonic Mean of two numbers a and b is:", ["2ab/(a+b)", "(a+b)/2", "√(ab)", "ab/(a+b)"],
       "HM = n / Σ(1/xᵢ). For two numbers: HM = 2/(1/a+1/b) = 2ab/(a+b). Always HM ≤ GM ≤ AM.",
       "দুটো সংখ্যা a ও b-এর হারমোনিক গড়:", ["2ab/(a+b)", "(a+b)/2", "√(ab)", "ab/(a+b)"],
       "HM = n / Σ(1/xᵢ)। দুটো সংখ্যার জন্য: HM = 2ab/(a+b)। সবসময় HM ≤ GM ≤ AM।"),
    _q("By the AM-GM inequality, for two positive numbers a and b:", ["(a+b)/2 ≥ √(ab), with equality iff a = b", "(a+b)/2 ≤ √(ab)", "AM = GM always", "AM > GM always (never equal)"],
       "AM ≥ GM. Useful in optimisation problems — minimum perimeter for fixed area uses AM-GM.",
       "দুটো ধনাত্মক সংখ্যা a ও b-এর জন্য AM-GM অসাম্য:", ["(a+b)/2 ≥ √(ab), সমতা iff a = b", "(a+b)/2 ≤ √(ab)", "সবসময় AM = GM", "সবসময় AM > GM (কখনো সমান নয়)"],
       "AM ≥ GM। অপ্টিমাইজেশনে কার্যকর — নির্দিষ্ট ক্ষেত্রফলে সর্বনিম্ন পরিসীমা AM-GM ব্যবহার করে।"),
    _q("The first-order linear ODE dy/dx + Py = Q has integrating factor:", ["e^(∫P dx)", "e^P", "∫P dx", "P/Q"],
       "Multiply both sides by e^(∫P dx) to make left side d/dx[y·e^(∫P dx)].",
       "প্রথম-ক্রম রৈখিক ODE dy/dx + Py = Q-এর সমাকলক গুণক:", ["e^(∫P dx)", "e^P", "∫P dx", "P/Q"],
       "উভয় পক্ষকে e^(∫P dx) দিয়ে গুণ করলে বাম পক্ষ d/dx[y·e^(∫P dx)] হয়।"),
    _q("The dot product of i and j (unit vectors along x and y axes) is:", ["0 (they are perpendicular)", "1", "−1", "√2"],
       "i·j = |i||j|cos 90° = 1×1×0 = 0. i·i = j·j = k·k = 1.",
       "i ও j (x ও y অক্ষ বরাবর একক ভেক্টর)-এর ডট গুণফল:", ["0 (তারা লম্ব)", "1", "−1", "√2"],
       "i·j = |i||j|cos 90° = 0। i·i = j·j = k·k = 1।"),
    _q("If two events have P(A) = 0.3 and P(B|A) = 0.5, then P(A ∩ B) = ?", ["0.15", "0.8", "0.6", "0.2"],
       "P(A∩B) = P(B|A)·P(A) = 0.5 × 0.3 = 0.15.",
       "P(A) = 0.3 ও P(B|A) = 0.5 হলে P(A ∩ B) = ?", ["0.15", "0.8", "0.6", "0.2"],
       "P(A∩B) = P(B|A)·P(A) = 0.5 × 0.3 = 0.15।"),
    _q("The value of ∑(r=1 to n) r² is:", ["n(n+1)(2n+1)/6", "n(n+1)/2", "n²(n+1)²/4", "[n(n+1)/2]²"],
       "∑r² = n(n+1)(2n+1)/6. For n=3: 1+4+9=14 = 3×4×7/6=14 ✓.",
       "∑(r=1 থেকে n) r²-এর মান:", ["n(n+1)(2n+1)/6", "n(n+1)/2", "n²(n+1)²/4", "[n(n+1)/2]²"],
       "∑r² = n(n+1)(2n+1)/6। n=3: 1+4+9=14 = 3×4×7/6=14 ✓।"),
    _q("The value of ∑(r=1 to n) r³ is:", ["[n(n+1)/2]²", "n(n+1)(2n+1)/6", "n²(n+1)/2", "n(n+1)²/2"],
       "∑r³ = [n(n+1)/2]². Note: (∑r)² = ∑r³ — a beautiful identity.",
       "∑(r=1 থেকে n) r³-এর মান:", ["[n(n+1)/2]²", "n(n+1)(2n+1)/6", "n²(n+1)/2", "n(n+1)²/2"],
       "∑r³ = [n(n+1)/2]²। লক্ষ্য: (∑r)² = ∑r³ — একটা সুন্দর অভেদ।"),
    _q("The number of solutions of the equation sin x = x in [0, 2π] is:", ["1 (only x = 0)", "2", "3", "infinitely many"],
       "y = sin x and y = x intersect only at the origin in [0, 2π] since sin x ≤ x for x ≥ 0.",
       "[0, 2π]-এ sin x = x সমীকরণের সমাধানের সংখ্যা:", ["1 (শুধু x = 0)", "2", "3", "অসংখ্য"],
       "y = sin x ও y = x শুধু মূলবিন্দুতে মেলে কারণ x ≥ 0-এ sin x ≤ x।"),
    _q("A relation R on a set A is called an equivalence relation if it is:", ["Reflexive, symmetric, AND transitive", "Reflexive and symmetric only", "Transitive only", "Symmetric and transitive only"],
       "All three properties needed. Example: congruence mod n on integers is an equivalence relation.",
       "সেট A-এ সম্পর্ক R সমতুল্যতা সম্পর্ক হয় যদি:", ["স্বতুল্য, প্রতিসম এবং তুল্যক্রমিক", "শুধু স্বতুল্য ও প্রতিসম", "শুধু তুল্যক্রমিক", "শুধু প্রতিসম ও তুল্যক্রমিক"],
       "তিনটি ধর্মই লাগবে। উদাহরণ: পূর্ণসংখ্যায় mod n সর্বাঙ্গ সমতুল্যতা সম্পর্ক।"),
    _q("The number of real roots of x⁴ − 5x² + 4 = 0 is:", ["4 (substitution u = x² gives u² − 5u + 4 = 0 → u = 1 or 4 → x = ±1, ±2)", "2", "0", "3"],
       "u² − 5u + 4 = (u−1)(u−4) = 0 → x² = 1 → x = ±1; x² = 4 → x = ±2. Four real roots.",
       "x⁴ − 5x² + 4 = 0-এর বাস্তব মূলের সংখ্যা:", ["4 (u = x² প্রতিস্থাপন: u=1 বা 4 → x = ±1, ±2)", "2", "0", "3"],
       "u² − 5u + 4 = (u−1)(u−4) = 0 → চারটি বাস্তব মূল ±1, ±2।"),
    _q("The angle subtended by an arc of length l in a circle of radius r (in radians) is:", ["θ = l/r", "θ = l·r", "θ = r/l", "θ = πl/r"],
       "Definition of radian measure: θ = arc/radius. Bridge arch geometry uses radian angles extensively.",
       "r ব্যাসার্ধের বৃত্তে l দৈর্ঘ্যের চাপ কর্তৃক কেন্দ্রীয় কোণ (রেডিয়ানে):", ["θ = l/r", "θ = l·r", "θ = r/l", "θ = πl/r"],
       "রেডিয়ান পরিমাপের সংজ্ঞা: θ = চাপ/ব্যাসার্ধ। সেতু খিলান জ্যামিতিতে রেডিয়ান কোণ ব্যাপকভাবে ব্যবহার।"),
    _q("Which of these series is convergent?", ["∑ 1/n² (p-series with p=2 > 1, converges)", "∑ 1/n (harmonic, diverges)", "∑ 1 (diverges)", "∑ n (diverges)"],
       "p-series: ∑1/nᵖ converges iff p > 1. ∑1/n (harmonic) diverges despite tending to 0.",
       "এই শ্রেণিগুলোর মধ্যে কোনটা অভিসারী?", ["∑ 1/n² (p-শ্রেণি, p=2 > 1, অভিসারী)", "∑ 1/n (হারমোনিক, অপসারী)", "∑ 1 (অপসারী)", "∑ n (অপসারী)"],
       "p-শ্রেণি: ∑1/nᵖ অভিসারী iff p > 1। ∑1/n (হারমোনিক) শূন্যের দিকে গেলেও অপসারী।"),
    _q("The graph of y = |x| (absolute value) is:", ["A V-shape with vertex at the origin, slopes ±1", "A straight line", "A parabola", "A circle"],
       "y = x for x ≥ 0, y = −x for x < 0. Non-differentiable at x = 0 (sharp corner).",
       "y = |x| (পরম মান)-এর লেখচিত্র:", ["মূলবিন্দুতে শীর্ষসহ V-আকৃতি, ঢাল ±1", "সরলরেখা", "পরাবৃত্ত", "বৃত্ত"],
       "x ≥ 0-এ y = x, x < 0-এ y = −x। x = 0-এ অ-অবকলনযোগ্য (ধারালো কোণ)।"),
    _q("The number of integers from 1 to 100 divisible by 3 or 5 is:", ["47 (by inclusion-exclusion: 33 + 20 − 6 = 47)", "53", "40", "33"],
       "⌊100/3⌋=33, ⌊100/5⌋=20, ⌊100/15⌋=6. Total = 33+20−6 = 47.",
       "1 থেকে 100 পর্যন্ত 3 বা 5 দ্বারা বিভাজ্য পূর্ণসংখ্যা:", ["47 (অন্তর্ভুক্তি-বর্জন: 33 + 20 − 6 = 47)", "53", "40", "33"],
       "⌊100/3⌋=33, ⌊100/5⌋=20, ⌊100/15⌋=6। মোট = 47।"),
    _q("In how many ways can 4 different objects be placed in 3 different boxes (repetition allowed)?", ["81 (3⁴ = 81)", "12", "64", "24"],
       "Each of 4 objects can go in 3 boxes independently: 3×3×3×3 = 3⁴ = 81.",
       "4 ভিন্ন বস্তু 3 ভিন্ন বাক্সে রাখার উপায় (পুনরাবৃত্তি অনুমোদিত):", ["81 (3⁴ = 81)", "12", "64", "24"],
       "প্রতিটি বস্তু 3 বাক্সে স্বতন্ত্রভাবে যেতে পারে: 3⁴ = 81।"),
    _q("The condition for lines y = m₁x + c₁ and y = m₂x + c₂ to be perpendicular is:", ["m₁m₂ = −1", "m₁ = m₂", "m₁ + m₂ = 0", "m₁m₂ = 1"],
       "Perpendicular slopes: product = −1. Parallel slopes: m₁ = m₂.",
       "y = m₁x + c₁ ও y = m₂x + c₂ রেখাদ্বয় লম্ব হওয়ার শর্ত:", ["m₁m₂ = −1", "m₁ = m₂", "m₁ + m₂ = 0", "m₁m₂ = 1"],
       "লম্ব ঢাল: গুণফল = −1। সমান্তরাল ঢাল: m₁ = m₂।"),
    _q("The formula for compound interest (principal P, rate r per annum, n years, compounded annually) is:", ["A = P(1 + r)ⁿ", "A = P(1 + nr)", "A = Perⁿ", "A = P + Prn"],
       "Compound vs simple interest: CI compounds the interest; SI is A = P(1+nr) — linear.",
       "চক্রবৃদ্ধি সুদের সূত্র (মূলধন P, বার্ষিক হার r, n বছর, বার্ষিক চক্রবৃদ্ধি):", ["A = P(1 + r)ⁿ", "A = P(1 + nr)", "A = Perⁿ", "A = P + Prn"],
       "চক্রবৃদ্ধি বনাম সরল সুদ: CI সুদ যোগ করে; SI = P(1+nr) — রৈখিক।"),
    _q("A function f: A → B is bijective if:", ["It is both injective (one-to-one) and surjective (onto)", "It is surjective only", "It is injective only", "f(a) = f(b) for all a, b"],
       "Bijection has a unique inverse. Example: f(x) = x³ from ℝ to ℝ is bijective.",
       "অপেক্ষক f: A → B দ্বিভেদী (bijective) হয় যদি:", ["এটা একমুখী (injective) এবং পরিব্যাপ্ত (surjective) উভয়ই", "শুধু পরিব্যাপ্ত", "শুধু একমুখী", "সব a, b-এর জন্য f(a) = f(b)"],
       "দ্বিভেদীর একটা অনন্য বিপরীত আছে। উদাহরণ: ℝ থেকে ℝ-তে f(x) = x³ দ্বিভেদী।"),
    _q("The smallest positive value of x satisfying tan x = 1 is:", ["π/4", "π/2", "π", "3π/4"],
       "tan(π/4) = 1. General solution: x = nπ + π/4. Smallest positive = π/4.",
       "tan x = 1 সন্তুষ্টকারী x-এর ক্ষুদ্রতম ধনাত্মক মান:", ["π/4", "π/2", "π", "3π/4"],
       "tan(π/4) = 1। সাধারণ সমাধান: x = nπ + π/4। ক্ষুদ্রতম ধনাত্মক = π/4।"),
    _q("The value of ⁿC₀ + ⁿC₁ + ⁿC₂ + … + ⁿCₙ is:", ["2ⁿ", "n!", "n²", "2n"],
       "Sum of all binomial coefficients = 2ⁿ (set x=1 in (1+x)ⁿ = Σ ⁿCᵣ xʳ).",
       "ⁿC₀ + ⁿC₁ + ⁿC₂ + … + ⁿCₙ-এর মান:", ["2ⁿ", "n!", "n²", "2n"],
       "সব দ্বিপদী সহগগুলোর যোগফল = 2ⁿ ((1+x)ⁿ-এ x=1 রাখুন)।"),
    _q("The maximum number of solutions of the equation cos θ = c (|c| ≤ 1) in [0, 2π] is:", ["2", "1", "4", "infinite"],
       "cos is symmetric about π: θ = arccos c and θ = 2π − arccos c give 2 solutions (1 if c = ±1).",
       "[0, 2π]-এ cos θ = c (|c| ≤ 1) সমীকরণের সর্বোচ্চ সমাধানের সংখ্যা:", ["2", "1", "4", "অসীম"],
       "cos π সম্পর্কে প্রতিসম: θ = arccos c ও θ = 2π − arccos c দুটো সমাধান দেয়।"),
    _q("The midpoint formula: the midpoint of the line segment joining (x₁,y₁) and (x₂,y₂) is:", ["((x₁+x₂)/2, (y₁+y₂)/2)", "((x₁−x₂)/2, (y₁−y₂)/2)", "((x₁x₂), (y₁y₂))", "(x₁+x₂, y₁+y₂)"],
       "Used to find the centre of a bridge span, the midpoint of a cable, or the centroid of a simple beam.",
       "মধ্যবিন্দু সূত্র: (x₁,y₁) ও (x₂,y₂) যোগকারী রেখাংশের মধ্যবিন্দু:", ["((x₁+x₂)/2, (y₁+y₂)/2)", "((x₁−x₂)/2, (y₁−y₂)/2)", "((x₁x₂), (y₁y₂))", "(x₁+x₂, y₁+y₂)"],
       "সেতু বিস্তারের কেন্দ্র, তারের মধ্যবিন্দু বা সরল মরীচির কেন্দ্রবিন্দু খুঁজতে ব্যবহার।"),
    _q("In a sample space with equally likely outcomes, the probability of event E is:", ["P(E) = (number of favourable outcomes) / (total outcomes)", "P(E) = total outcomes / favourable", "P(E) = 1 always", "P(E) = E / total"],
       "Classical definition. P(E) ∈ [0,1] always; P(∅)=0, P(Ω)=1.",
       "সমান সম্ভাবনার নমুনা পরিসরে ঘটনা E-এর সম্ভাবনা:", ["P(E) = (অনুকূল ঘটনার সংখ্যা) / (মোট ঘটনা)", "P(E) = মোট / অনুকূল", "P(E) = সবসময় 1", "P(E) = E / মোট"],
       "ধ্রুপদী সংজ্ঞা। P(E) ∈ [0,1] সবসময়; P(∅)=0, P(Ω)=1।"),
    _q("The sum of interior angles of a polygon with n sides is:", ["(n−2) × 180°", "n × 90°", "n × 180°", "(n−2) × 90°"],
       "Triangle (n=3): 180°; quadrilateral (n=4): 360°; pentagon (n=5): 540°.",
       "n বাহুর বহুভুজের অভ্যন্তরীণ কোণগুলোর যোগফল:", ["(n−2) × 180°", "n × 90°", "n × 180°", "(n−2) × 90°"],
       "ত্রিভুজ (n=3): 180°; চতুর্ভুজ (n=4): 360°; পঞ্চভুজ (n=5): 540°।"),
    _q("The contrapositive of 'If p then q' is:", ["If not q then not p (¬q → ¬p)", "If q then p", "If not p then not q", "If p then not q"],
       "Contrapositive is logically equivalent to the original. Converse (q→p) is NOT equivalent.",
       "'p হলে q' -এর বিপরীতধর্মী:", ["q না হলে p না (¬q → ¬p)", "q হলে p", "p না হলে q না", "p হলে q না"],
       "বিপরীতধর্মী মূল বিবৃতির সাথে যুক্তিগতভাবে সমতুল্য। বিপরীত (q→p) সমতুল্য নয়।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
