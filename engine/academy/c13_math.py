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
]

ITEMS = tuple(NUMERIC + CONCEPTS)
