"""Class 8 - Math (Junior Cadet): solving quadratics by factorising, Pythagoras in 3D, spheres and
cylinders in terms of π, surds, laws of indices, geometric sequences, linear inequalities,
rearranging engineering formulae, quartiles and the interquartile range, mean from a frequency
table, upper and lower bounds, and finding angles with inverse tan - all from bridge sites."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r + 2, r * 2, r + 10):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + ub for x in o], ex_bn)


def _same(q_en, q_bn, opts, ex_en, ex_bn):
    """Options that read the same in both languages (numbers and symbols)."""
    return mcq(q_en, opts, 0, ex_en, q_bn, opts, ex_bn)


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def quad(r1, r2):
    b, c = -(r1 + r2), r1 * r2
    cx = lambda k: "x" if k == 1 else f"{k}x"
    eq = "x²" + (f" + {cx(b)}" if b > 0 else f" - {cx(-b)}" if b < 0 else "") + (f" + {c}" if c > 0 else f" - {-c}" if c < 0 else "")
    f1 = f"(x {'-' if r1 > 0 else '+'} {abs(r1)})"
    f2 = f"(x {'-' if r2 > 0 else '+'} {abs(r2)})"
    pair = lambda a, b_: f"x = {a} or x = {b_}"
    opts = [pair(r1, r2), pair(-r1, -r2), pair(r1, -r2) if r1 != -r2 else pair(r1 + 1, r2), pair(r1 * r2, r1 + r2)]
    seen = []
    for o in opts:
        if o not in seen:
            seen.append(o)
    while len(seen) < 4:
        seen.append(pair(r1 + len(seen), r2))
    return mcq(f"Solve {eq} = 0.", seen, 0,
               f"Factorise: {f1}{f2} = 0, so x = {r1} or x = {r2}. Check: {r1} x {r2} = {c} and {r1} + {r2} = {-b}.",
               f"সমাধান করো: {eq} = 0।", [o.replace(' or ', ' বা ') for o in seen],
               f"উৎপাদকে ভাঙো: {f1}{f2} = 0, তাই x = {r1} বা x = {r2}। যাচাই: {r1} x {r2} = {c} আর {r1} + {r2} = {-b}।")


def diag3d(a, b, c, what_en, what_bn):
    d = int(round((a * a + b * b + c * c) ** 0.5))
    return _n(f"{what_en} is {a} m x {b} m x {c} m. How long is the longest straight rod that fits from one corner to the opposite corner?",
              f"{what_bn} {a} m x {b} m x {c} m। এক কোণ থেকে বিপরীত কোণ পর্যন্ত সবচেয়ে লম্বা কত মিটারের সোজা রড আঁটবে?", d,
              f"d² = {a}² + {b}² + {c}² = {a * a} + {b * b} + {c * c} = {d * d}, so d = {d} m.",
              f"d² = {a}² + {b}² + {c}² = {a * a} + {b * b} + {c * c} = {d * d}, তাই d = {d} m।",
              (a + b + c, int(round((a * a + b * b) ** 0.5)) if int(round((a * a + b * b) ** 0.5)) != d else d + 3, d * d), " m")


def sphere(r, what_en, what_bn):
    k = _c(4 * r ** 3 / 3)
    f = lambda x: f"{x:g}π m³"
    opts = [f(k), f(_c(4 * r * r)), f(_c(r ** 3)), f(_c(4 * r ** 3))]
    seen = []
    for o in opts:
        if o not in seen:
            seen.append(o)
    while len(seen) < 4:
        seen.append(f(_c(k + len(seen) * 3)))
    return _same(f"{what_en} is a sphere of radius {r} m. What is its volume, in terms of π? (V = 4/3 πr³)",
                 f"{what_bn} {r} m ব্যাসার্ধের একটা গোলক। π-এর হিসেবে এর আয়তন কত? (V = 4/3 πr³)", seen,
                 f"V = 4/3 x π x {r}³ = 4/3 x {r ** 3} x π = {k:g}π m³.",
                 f"V = 4/3 x π x {r}³ = 4/3 x {r ** 3} x π = {k:g}π m³।")


def cylsa(r, h, what_en, what_bn):
    k = 2 * r * r + 2 * r * h
    f = lambda x: f"{x:g}π m²"
    opts = [f(k), f(2 * r * h), f(r * r * h), f(r * r + 2 * r * h)]
    seen = []
    for o in opts:
        if o not in seen:
            seen.append(o)
    while len(seen) < 4:
        seen.append(f(k + len(seen) * 4))
    return _same(f"{what_en} is a closed cylinder, radius {r} m and height {h} m. What is its total surface area, in terms of π?",
                 f"{what_bn} একটা বন্ধ চোঙ, ব্যাসার্ধ {r} m আর উচ্চতা {h} m। π-এর হিসেবে এর মোট পৃষ্ঠতল কত?", seen,
                 f"Two ends 2πr² = {2 * r * r}π, curved side 2πrh = {2 * r * h}π; total {k}π m² - useful for ordering paint.",
                 f"দুই প্রান্ত 2πr² = {2 * r * r}π, বাঁকা গা 2πrh = {2 * r * h}π; মোট {k}π m² - রং অর্ডারে কাজে লাগে।")


def surd(n, a, b):
    # √n = a√b
    opts = [f"{a}√{b}", f"{b}√{a}", f"{a * a}√{b}", f"{a}√{b * 2}"]
    return _same(f"Simplify √{n}.", f"সরল করো: √{n}।", opts,
                 f"√{n} = √({a * a} x {b}) = √{a * a} x √{b} = {a}√{b}.",
                 f"√{n} = √({a * a} x {b}) = √{a * a} x √{b} = {a}√{b}।")


def index(kind, a, b):
    if kind == "mul":
        r, q, ex = a + b, f"x^{a} x x^{b}", f"Add the powers: {a} + {b} = {a + b}."
        alts = [a * b, abs(a - b) if a != b else a + b + 2, a + b + 1]
    elif kind == "div":
        r, q, ex = a - b, f"x^{a} ÷ x^{b}", f"Subtract the powers: {a} - {b} = {a - b}."
        alts = [_c(a / b) if a % b == 0 and a // b != a - b else a + b, a + b if a + b != a - b else a * b, a * b]
    else:
        r, q, ex = a * b, f"(x^{a})^{b}", f"Multiply the powers: {a} x {b} = {a * b}."
        alts = [a + b, a ** b if a ** b != a * b else a * b + 2, a * b + 1]
    o = _o(r, *alts)
    opts = [f"x^{v:g}" for v in o]
    return _same(f"Simplify {q}.", f"সরল করো: {q}।", opts, ex,
                 ex.replace("Add the powers", "ঘাত যোগ করো").replace("Subtract the powers", "ঘাত বিয়োগ করো").replace("Multiply the powers", "ঘাত গুণ করো").rstrip(".") + "।")


def geo(a, r, n, what_en, what_bn):
    t = a * r ** (n - 1)
    return _n(f"{what_en} {a}, {a * r}, {a * r * r}, … is multiplied by {r} each time. What is term number {n}?",
              f"{what_bn} {a}, {a * r}, {a * r * r}, … প্রতিবার {r} দিয়ে গুণ হয়। {n}-তম পদ কত?", t,
              f"nth term = {a} x {r}^(n - 1) = {a} x {r}^{n - 1} = {t:,}.",
              f"n-তম পদ = {a} x {r}^(n - 1) = {a} x {r}^{n - 1} = {t:,}।",
              (a * r ** n, a + (n - 1) * r, a * r * n))


def ineq(a, b, c):
    # a x + b < c  ->  x < (c - b) / a
    r = _c((c - b) / a)
    rhs = f"+ {b}" if b > 0 else f"- {-b}"
    opts = [f"x < {r:g}", f"x > {r:g}", f"x < {_c((c + b) / a):g}" if _c((c + b) / a) != r else f"x < {r + 1:g}", f"x < {_c(c / a - b):g}" if _c(c / a - b) != r else f"x < {r + 2:g}"]
    return _same(f"Solve the inequality {a}x {rhs} < {c}.", f"অসমতার সমাধান করো: {a}x {rhs} < {c}।", opts,
                 f"{a}x < {c} {'-' if b > 0 else '+'} {abs(b)} = {c - b}, so x < {c - b} ÷ {a} = {r:g}.",
                 f"{a}x < {c} {'-' if b > 0 else '+'} {abs(b)} = {c - b}, তাই x < {c - b} ÷ {a} = {r:g}।")


def rearr(formula, subject, right, wrongs, what_en, what_bn):
    opts = [right, *wrongs]
    return _same(f"{what_en}: {formula}. Make {subject} the subject.",
                 f"{what_bn}: {formula}। {subject}-কে বিষয় করো।", opts,
                 f"Undo each operation in reverse order: {subject} = {right.split('= ', 1)[1]}.",
                 f"প্রতিটা ক্রিয়া উল্টো ক্রমে খোলো: {subject} = {right.split('= ', 1)[1]}।")


def iqr(data, what_en, what_bn):
    d = sorted(data)
    n = len(d)
    q1, q3 = d[(n + 1) // 4 - 1], d[3 * (n + 1) // 4 - 1]
    r = q3 - q1
    return _n(f"{what_en}: {', '.join(map(str, d))}. What is the interquartile range?",
              f"{what_bn}: {', '.join(map(str, d))}। আন্তঃচতুর্থক পরিসর কত?", r,
              f"With {n} values, Q1 is the {(n + 1) // 4}th = {q1} and Q3 is the {3 * (n + 1) // 4}th = {q3}; IQR = {q3} - {q1} = {r}.",
              f"{n}টি মানে Q1 হলো {(n + 1) // 4}-তম = {q1} আর Q3 হলো {3 * (n + 1) // 4}-তম = {q3}; পরিসর = {q3} - {q1} = {r}।",
              (d[-1] - d[0], q3, d[n // 2]))


def fmean(values, freqs, what_en, what_bn):
    tot = sum(v * f for v, f in zip(values, freqs))
    n = sum(freqs)
    m = _c(tot / n)
    table = ", ".join(f"{v} ({f})" for v, f in zip(values, freqs))
    return _n(f"{what_en}, shown as value (frequency): {table}. What is the mean?",
              f"{what_bn}, মান (পরিসংখ্যা) হিসেবে: {table}। গড় কত?", m,
              f"Σfx = {tot}, Σf = {n}; mean = {tot} ÷ {n} = {m:g}.",
              f"Σfx = {tot}, Σf = {n}; গড় = {tot} ÷ {n} = {m:g}।",
              (_c(sum(values) / len(values)), _c(tot / len(values)), max(values)))


def bounds(l, w, unit, acc):
    hi = _c((l + acc / 2) * (w + acc / 2))
    lo = _c((l - acc / 2) * (w - acc / 2))
    return _n(f"A deck panel measures {l} {unit} by {w} {unit}, each to the nearest {acc:g} {unit}. What is the upper bound of its area?",
              f"একটা পাটাতন-প্যানেল {l} {unit} x {w} {unit}, প্রতিটা নিকটতম {acc:g} {unit} পর্যন্ত। ক্ষেত্রফলের ঊর্ধ্বসীমা কত?", hi,
              f"Upper bounds: {l + acc / 2:g} and {w + acc / 2:g}; area ≤ {l + acc / 2:g} x {w + acc / 2:g} = {hi:g} {unit}².",
              f"ঊর্ধ্বসীমা: {l + acc / 2:g} আর {w + acc / 2:g}; ক্ষেত্রফল ≤ {l + acc / 2:g} x {w + acc / 2:g} = {hi:g} {unit}²।",
              (l * w, lo, _c((l + acc) * (w + acc))), f" {unit}²")


def atan(rise, run, ang):
    opts = [f"{ang}°", f"{90 - ang}°" if 90 - ang != ang else f"{ang + 15}°", f"{_c(rise / run * 45):g}°" if _c(rise / run * 45) not in (ang, 90 - ang) else f"{ang + 10}°", f"{ang + 20}°"]
    return _same(f"A ramp rises {rise:g} m over a horizontal distance of {run:g} m. Using tan⁻¹({_c(rise / run):g}) = {ang}°, what angle does it make with the ground?",
                 f"একটা ঢাল {run:g} m অনুভূমিক দূরত্বে {rise:g} m ওঠে। tan⁻¹({_c(rise / run):g}) = {ang}° ধরে, মাটির সঙ্গে কত কোণ করে?", opts,
                 f"tan θ = opposite ÷ adjacent = {rise:g} ÷ {run:g} = {_c(rise / run):g}, so θ = tan⁻¹({_c(rise / run):g}) = {ang}°.",
                 f"tan θ = বিপরীত ÷ সন্নিহিত = {rise:g} ÷ {run:g} = {_c(rise / run):g}, তাই θ = tan⁻¹({_c(rise / run):g}) = {ang}°।")


ITEMS = (
    quad(4, -1), quad(-2, -5), quad(6, -3), quad(1, 7), quad(-4, 5),
    diag3d(2, 3, 6, "A storage container", "একটা মালপত্রের কনটেনার"), diag3d(1, 4, 8, "A site cabin", "নির্মাণস্থলের একটা কেবিন"),
    diag3d(4, 4, 7, "A concrete mould", "একটা কংক্রিটের ছাঁচ"), diag3d(2, 6, 9, "A steel crate", "একটা ইস্পাতের বাক্স"),
    diag3d(6, 6, 7, "A bridge pier cap", "একটা সেতু-স্তম্ভের মাথা"),
    sphere(3, "A water tank", "একটা জলের ট্যাঙ্ক"), sphere(6, "A gas holder", "একটা গ্যাস-আধার"),
    cylsa(2, 5, "A pier column", "একটা স্তম্ভ-থাম"), cylsa(3, 10, "A storage silo", "একটা মজুত-সাইলো"), cylsa(1, 4, "A drainage pipe", "একটা নিকাশি-পাইপ"),
    surd(50, 5, 2), surd(72, 6, 2), surd(48, 4, 3), surd(75, 5, 3), surd(200, 10, 2),
    index("mul", 3, 4), index("div", 8, 3), index("div", 9, 6), index("pow", 3, 2), index("pow", 4, 3),
    geo(3, 2, 6, "The number of rivets in each row", "প্রতি সারিতে রিভেটের সংখ্যা"), geo(5, 3, 4, "A crack count", "ফাটলের সংখ্যা"),
    geo(2, 5, 4, "Cells in a mould sample", "ছত্রাকের নমুনায় কোষ"), geo(1, 4, 5, "Truss panel count", "ট্রাস-প্যানেলের সংখ্যা"),
    ineq(3, -4, 11), ineq(2, 5, 17), ineq(5, 3, 28), ineq(4, -6, 10),
    rearr("v = u + at", "t", "t = (v - u) / a", ["t = v - u - a", "t = (v + u) / a", "t = a(v - u)"], "Speed formula", "বেগের সূত্র"),
    rearr("F = ma", "a", "a = F / m", ["a = Fm", "a = m / F", "a = F - m"], "Newton's second law", "নিউটনের দ্বিতীয় সূত্র"),
    rearr("σ = F / A", "A", "A = F / σ", ["A = Fσ", "A = σ / F", "A = F - σ"], "Stress formula", "পীড়নের সূত্র"),
    rearr("P = 2(l + w)", "l", "l = P / 2 - w", ["l = P - 2w", "l = 2P - w", "l = (P - w) / 2"], "Perimeter of a site", "নির্মাণস্থলের পরিসীমা"),
    rearr("V = IR", "R", "R = V / I", ["R = VI", "R = I / V", "R = V - I"], "Ohm's law", "ওহমের সূত্র"),
    iqr([12, 15, 18, 20, 22, 25, 30], "Daily concrete pours (m³) for a week", "এক সপ্তাহের দৈনিক কংক্রিট-ঢালাই (m³)"),
    iqr([3, 5, 6, 8, 9, 11, 14, 15, 17, 20, 21], "Minutes late for 11 deliveries", "11টি ডেলিভারির দেরির মিনিট"),
    iqr([40, 42, 45, 47, 50, 55, 58], "Bolt tension readings (kN)", "বল্টুর টানের পাঠ (kN)"),
    fmean([1, 2, 3, 4], [5, 8, 4, 3], "Number of cracks found per girder", "প্রতি গার্ডারে পাওয়া ফাটলের সংখ্যা"),
    fmean([10, 20, 30], [2, 5, 3], "Trucks per hour over 10 hours", "10 ঘণ্টায় প্রতি ঘণ্টার ট্রাক"),
    fmean([0, 1, 2, 3], [6, 9, 3, 2], "Faulty welds per panel", "প্রতি প্যানেলে ত্রুটিপূর্ণ ঝালাই"),
    bounds(6, 4, "m", 1), bounds(12, 5, "m", 1), bounds(3.4, 2.1, "m", 0.1),
    atan(1, 1, 45), atan(3, 5.2, 30), atan(5.2, 3, 60),
    mcq("A product of two brackets equals zero: (x - 4)(x + 2) = 0. Why can we say x = 4 or x = -2?", ["If two numbers multiply to zero, at least one of them must be zero", "Because 4 and 2 are even", "Brackets always give two answers", "Because x is always positive"], 0,
        "This is why factorising solves quadratics.",
        "দুটো বন্ধনীর গুণফল শূন্য: (x - 4)(x + 2) = 0। কেন বলা যায় x = 4 বা x = -2?", ["দুটো সংখ্যার গুণফল শূন্য হলে অন্তত একটাকে শূন্য হতেই হবে", "কারণ 4 আর 2 জোড়", "বন্ধনী সবসময় দুটো উত্তর দেয়", "কারণ x সবসময় ধনাত্মক"],
        "তাই উৎপাদকে ভেঙে দ্বিঘাত সমীকরণের সমাধান হয়।"),
    mcq("Factorise x² - 25.", ["(x - 5)(x + 5)", "(x - 5)²", "(x + 25)(x - 1)", "x(x - 25)"], 0,
        "Difference of two squares: a² - b² = (a - b)(a + b).",
        "উৎপাদকে ভাঙো: x² - 25।", ["(x - 5)(x + 5)", "(x - 5)²", "(x + 25)(x - 1)", "x(x - 25)"],
        "দুই বর্গের অন্তর: a² - b² = (a - b)(a + b)।"),
    mcq("What is the quadratic formula used for?", ["Solving ax² + bx + c = 0 when it will not factorise neatly", "Finding the area of a circle", "Adding fractions", "Finding a percentage"], 0,
        "x = (-b ± √(b² - 4ac)) / 2a.",
        "দ্বিঘাত সূত্র কীসের জন্য ব্যবহার হয়?", ["ax² + bx + c = 0 যখন সহজে উৎপাদকে ভাঙে না, তখন সমাধান করতে", "বৃত্তের ক্ষেত্রফল বের করতে", "ভগ্নাংশ যোগ করতে", "শতাংশ বের করতে"],
        "x = (-b ± √(b² - 4ac)) / 2a।"),
    mcq("A projectile path y = 20x - 5x² hits the ground (y = 0) at x = 0 and where else?", ["x = 4", "x = 5", "x = 20", "x = 2"], 0,
        "5x(4 - x) = 0, so x = 0 or x = 4.",
        "একটা প্রক্ষিপ্ত বস্তুর পথ y = 20x - 5x² মাটিতে (y = 0) x = 0-তে আর আর কোথায় নামে?", ["x = 4", "x = 5", "x = 20", "x = 2"],
        "5x(4 - x) = 0, তাই x = 0 বা x = 4।"),
    mcq("What does the graph of y = x² look like?", ["A U-shaped curve (parabola) with its lowest point at (0, 0)", "A straight line", "A circle", "A zig-zag"], 0,
        "Many arch bridges are close to parabolas, but upside down.",
        "y = x²-এর লেখচিত্র দেখতে কেমন?", ["(0, 0)-তে সবচেয়ে নিচু বিন্দুওয়ালা U-আকারের বক্ররেখা (অধিবৃত্ত)", "সরলরেখা", "বৃত্ত", "আঁকাবাঁকা রেখা"],
        "অনেক খিলান-সেতু উল্টো অধিবৃত্তের কাছাকাছি।"),
    mcq("An arch follows y = 16 - x² (in metres). How high is the top of the arch?", ["16 m", "4 m", "8 m", "32 m"], 0,
        "The top is at x = 0, where y = 16 - 0 = 16.",
        "একটা খিলান y = 16 - x² (মিটারে) মেনে চলে। খিলানের মাথা কত উঁচু?", ["16 m", "4 m", "8 m", "32 m"],
        "মাথা x = 0-তে, যেখানে y = 16 - 0 = 16।"),
    mcq("The same arch y = 16 - x² meets the ground at x = -4 and x = 4. How wide is its span?", ["8 m", "4 m", "16 m", "32 m"], 0,
        "From -4 to 4 is 8 m.",
        "একই খিলান y = 16 - x² মাটিতে x = -4 আর x = 4-এ মেশে। এর বিস্তার কত চওড়া?", ["8 m", "4 m", "16 m", "32 m"],
        "-4 থেকে 4 পর্যন্ত 8 m।"),
    mcq("Why is √2 called an 'irrational' number?", ["Its decimal goes on forever without repeating, so it cannot be written as a fraction", "It is negative", "It is a whole number", "It is unreasonable"], 0,
        "The diagonal of a 1 m square is √2 ≈ 1.414 m.",
        "√2-কে 'অমূলদ' সংখ্যা বলে কেন?", ["এর দশমিক না থেমে, পুনরাবৃত্তি ছাড়া চলতেই থাকে, তাই ভগ্নাংশে লেখা যায় না", "এটা ঋণাত্মক", "এটা পূর্ণসংখ্যা", "এটা অযৌক্তিক"],
        "1 m বর্গের কর্ণ √2 ≈ 1.414 m।"),
    mcq("What is √3 x √12?", ["6", "√15", "36", "9"], 0,
        "√3 x √12 = √36 = 6.",
        "√3 x √12 কত?", ["6", "√15", "36", "9"],
        "√3 x √12 = √36 = 6।"),
    mcq("Why do engineers sometimes leave answers as surds like 5√2 instead of decimals?", ["Surds are exact; decimals are rounded", "Surds are always smaller", "Decimals are not allowed", "Surds are easier to measure with a tape"], 0,
        "Round only at the final step to avoid building up errors.",
        "প্রকৌশলীরা কখনো উত্তর দশমিকে না দিয়ে 5√2-এর মতো করণীতে রাখেন কেন?", ["করণী নিখুঁত; দশমিক আসন্ন", "করণী সবসময় ছোট", "দশমিক নিষিদ্ধ", "ফিতে দিয়ে করণী মাপা সহজ"],
        "ভুল জমে ওঠা এড়াতে শুধু শেষ ধাপে আসন্ন করো।"),
    mcq("What is 2⁻³?", ["1/8", "-8", "-6", "8"], 0,
        "A negative power means 'one over': 2⁻³ = 1/2³ = 1/8.",
        "2⁻³ কত?", ["1/8", "-8", "-6", "8"],
        "ঋণাত্মক ঘাত মানে 'এক ভাগ': 2⁻³ = 1/2³ = 1/8।"),
    mcq("What is 16^(1/2)?", ["4", "8", "256", "32"], 0,
        "A power of 1/2 means square root.",
        "16^(1/2) কত?", ["4", "8", "256", "32"],
        "1/2 ঘাত মানে বর্গমূল।"),
    mcq("What is 27^(1/3)?", ["3", "9", "81", "1/27"], 0,
        "A power of 1/3 means cube root: 3 x 3 x 3 = 27.",
        "27^(1/3) কত?", ["3", "9", "81", "1/27"],
        "1/3 ঘাত মানে ঘনমূল: 3 x 3 x 3 = 27।"),
    mcq("What is the difference between an arithmetic and a geometric sequence?", ["Arithmetic adds the same number each time; geometric multiplies by the same number", "They are the same", "Arithmetic multiplies; geometric adds", "Geometric sequences only use shapes"], 0,
        "Bridge tolls rising Rs 5 a year are arithmetic; costs rising 5% a year are geometric.",
        "সমান্তর আর গুণোত্তর অনুক্রমের পার্থক্য কী?", ["সমান্তরে প্রতিবার একই সংখ্যা যোগ হয়; গুণোত্তরে একই সংখ্যা দিয়ে গুণ হয়", "দুটো একই", "সমান্তরে গুণ; গুণোত্তরে যোগ", "গুণোত্তরে শুধু আকার থাকে"],
        "টোল বছরে 5 টাকা বাড়া সমান্তর; খরচ বছরে 5% বাড়া গুণোত্তর।"),
    mcq("A crack doubles in length every year. It is 2 mm now. How long will it be in 5 years if nothing is done?", ["64 mm", "12 mm", "10 mm", "32 mm"], 0,
        "2 x 2⁵ = 64 mm - exponential growth is why early repairs matter.",
        "একটা ফাটল প্রতি বছর দ্বিগুণ লম্বা হয়। এখন 2 mm। কিছু না করলে 5 বছরে কত হবে?", ["64 mm", "12 mm", "10 mm", "32 mm"],
        "2 x 2⁵ = 64 mm - সূচকীয় বৃদ্ধির জন্যই আগেভাগে মেরামত জরুরি।"),
    mcq("On a number line, what does 'x ≥ 3' look like?", ["A filled dot at 3 with an arrow to the right", "An open dot at 3 with an arrow to the left", "A filled dot at 3 with an arrow to the left", "Just a dot at 3"], 0,
        "Filled means 3 is included; the arrow shows all larger values.",
        "সংখ্যারেখায় 'x ≥ 3' দেখতে কেমন?", ["3-এ ভরাট বিন্দু আর ডানদিকে তির", "3-এ ফাঁকা বিন্দু আর বাঁদিকে তির", "3-এ ভরাট বিন্দু আর বাঁদিকে তির", "শুধু 3-এ একটা বিন্দু"],
        "ভরাট মানে 3 ধরা আছে; তির সব বড় মান দেখায়।"),
    mcq("When you multiply or divide both sides of an inequality by a negative number, what must you do?", ["Reverse the inequality sign", "Nothing special", "Add 1 to both sides", "Square both sides"], 0,
        "-2x < 6 becomes x > -3.",
        "অসমতার দুই দিককে ঋণাত্মক সংখ্যা দিয়ে গুণ বা ভাগ করলে কী করতে হবে?", ["অসমতার চিহ্ন উল্টে দিতে হবে", "বিশেষ কিছু না", "দুই দিকে 1 যোগ", "দুই দিকের বর্গ"],
        "-2x < 6 হয়ে যায় x > -3।"),
    mcq("A lorry may cross a bridge only if its mass m (tonnes) satisfies m ≤ 40. Which lorry may cross?", ["A 38-tonne lorry", "A 41-tonne lorry", "A 44-tonne lorry", "A 50-tonne lorry"], 0,
        "38 ≤ 40 is true; the others break the limit.",
        "একটা লরি সেতু পার হতে পারে শুধু যদি তার ভর m (টন) m ≤ 40 মানে। কোন লরি পার হতে পারে?", ["38 টনের লরি", "41 টনের লরি", "44 টনের লরি", "50 টনের লরি"],
        "38 ≤ 40 সত্য; বাকিগুলো সীমা ভাঙে।"),
    mcq("A quantity is 'inversely proportional to the square' of distance. If the distance doubles, the quantity…", ["Becomes a quarter", "Halves", "Doubles", "Stays the same"], 0,
        "1 ÷ 2² = 1/4 - like light or sound intensity spreading out.",
        "একটা রাশি দূরত্বের 'বর্গের ব্যস্তানুপাতিক'। দূরত্ব দ্বিগুণ হলে রাশিটা…", ["এক-চতুর্থাংশ হয়", "অর্ধেক হয়", "দ্বিগুণ হয়", "একই থাকে"],
        "1 ÷ 2² = 1/4 - আলো বা শব্দের তীব্রতা ছড়িয়ে পড়ার মতো।"),
    mcq("The wind force on a sign is proportional to the square of wind speed. If the wind speed triples, the force…", ["Becomes 9 times as big", "Triples", "Becomes 6 times as big", "Stays the same"], 0,
        "3² = 9 - why storms are so much more dangerous than breezes.",
        "একটা বোর্ডের উপর হাওয়ার বল হাওয়ার গতির বর্গের সমানুপাতিক। গতি তিনগুণ হলে বল…", ["9 গুণ হয়", "তিনগুণ হয়", "6 গুণ হয়", "একই থাকে"],
        "3² = 9 - তাই ঝড় হালকা হাওয়ার চেয়ে অনেক বেশি বিপজ্জনক।"),
    mcq("What is the median of a data set?", ["The middle value when the data are in order", "The most common value", "The total divided by the count", "The largest minus the smallest"], 0,
        "It is not pulled about by one extreme value, unlike the mean.",
        "তথ্যসমষ্টির মধ্যমা কী?", ["তথ্য ক্রমে সাজালে মাঝের মান", "সবচেয়ে বেশিবার আসা মান", "যোগফল ÷ সংখ্যা", "বৃহত্তম বিয়োগ ক্ষুদ্রতম"],
        "গড়ের মতো একটা চরম মানে এটা টানা খায় না।"),
    mcq("Why is the interquartile range often better than the range for describing spread?", ["It ignores extreme values and describes the middle half of the data", "It is always bigger", "It uses only the largest value", "It is easier to spell"], 0,
        "One faulty sensor reading can wreck the range but hardly moves the IQR.",
        "ছড়ানো বোঝাতে আন্তঃচতুর্থক পরিসর প্রায়ই পরিসরের চেয়ে ভালো কেন?", ["চরম মান বাদ দিয়ে তথ্যের মাঝের অর্ধেকটা বোঝায়", "সবসময় বড়", "শুধু বৃহত্তম মান ব্যবহার করে", "বানান সহজ"],
        "একটা ত্রুটিপূর্ণ সেন্সরের পাঠ পরিসর নষ্ট করতে পারে, কিন্তু আন্তঃচতুর্থক পরিসর প্রায় নড়ে না।"),
    mcq("What does a box plot show?", ["The minimum, lower quartile, median, upper quartile and maximum", "Only the mean", "The shape of a box girder", "Every single value"], 0,
        "Two box plots side by side make it easy to compare suppliers.",
        "বক্স-প্লট কী দেখায়?", ["ক্ষুদ্রতম, নিম্ন চতুর্থক, মধ্যমা, ঊর্ধ্ব চতুর্থক আর বৃহত্তম মান", "শুধু গড়", "বাক্স-গার্ডারের আকার", "প্রতিটা মান"],
        "পাশাপাশি দুটো বক্স-প্লটে সরবরাহকারীদের তুলনা সহজ হয়।"),
    mcq("Two concrete suppliers have the same median strength, but supplier A has a much smaller IQR. Which is more consistent?", ["Supplier A", "Supplier B", "They are equally consistent", "It cannot be compared"], 0,
        "A smaller spread means fewer surprises on site.",
        "দুই কংক্রিট-সরবরাহকারীর শক্তির মধ্যমা সমান, কিন্তু A-এর আন্তঃচতুর্থক পরিসর অনেক ছোট। কে বেশি স্থির মানের?", ["সরবরাহকারী A", "সরবরাহকারী B", "দুজনেই সমান", "তুলনা করা যায় না"],
        "কম ছড়ানো মানে নির্মাণস্থলে কম চমক।"),
    mcq("What does a cumulative frequency graph let you read off easily?", ["The median and quartiles", "The mode only", "The colour of data", "The mean exactly"], 0,
        "Read across at half the total for the median, a quarter and three-quarters for the quartiles.",
        "ক্রমযোজিত পরিসংখ্যার লেখচিত্র থেকে সহজে কী পড়া যায়?", ["মধ্যমা আর চতুর্থকগুলো", "শুধু ভূয়িষ্ঠক", "তথ্যের রং", "ঠিক গড়"],
        "মোটের অর্ধেকে আড়াআড়ি পড়লে মধ্যমা, এক-চতুর্থাংশ আর তিন-চতুর্থাংশে চতুর্থক।"),
    mcq("In a histogram with unequal class widths, what does the height of each bar show?", ["Frequency density (frequency ÷ class width)", "Frequency", "Class width", "The mean"], 0,
        "The area of each bar then shows the frequency.",
        "অসমান শ্রেণি-প্রস্থের হিস্টোগ্রামে প্রতিটা স্তম্ভের উচ্চতা কী দেখায়?", ["পরিসংখ্যা-ঘনত্ব (পরিসংখ্যা ÷ শ্রেণি-প্রস্থ)", "পরিসংখ্যা", "শ্রেণি-প্রস্থ", "গড়"],
        "তখন প্রতিটা স্তম্ভের ক্ষেত্রফল পরিসংখ্যা দেখায়।"),
    mcq("A class 10-30 m has a frequency of 40. What is its frequency density?", ["2", "40", "20", "800"], 0,
        "Class width = 20; 40 ÷ 20 = 2.",
        "10-30 m শ্রেণির পরিসংখ্যা 40। এর পরিসংখ্যা-ঘনত্ব কত?", ["2", "40", "20", "800"],
        "শ্রেণি-প্রস্থ = 20; 40 ÷ 20 = 2।"),
    mcq("A length is 8 m to the nearest metre. What is its lower bound?", ["7.5 m", "7 m", "8 m", "7.9 m"], 0,
        "Half of the 1 m accuracy below: 8 - 0.5 = 7.5 m.",
        "একটা দৈর্ঘ্য নিকটতম মিটারে 8 m। এর নিম্নসীমা কত?", ["7.5 m", "7 m", "8 m", "7.9 m"],
        "1 m নির্ভুলতার অর্ধেক নিচে: 8 - 0.5 = 7.5 m।"),
    mcq("A beam's load is 40 kN (nearest 10 kN) and its strength 50 kN (nearest 10 kN). What is the worst case - the smallest possible spare strength?", ["0 kN", "10 kN", "20 kN", "5 kN"], 0,
        "Lowest strength 45 - highest load 45 = 0. Rounding can hide a real risk!",
        "একটা কড়ির বোঝা 40 kN (নিকটতম 10 kN) আর শক্তি 50 kN (নিকটতম 10 kN)। সবচেয়ে খারাপ ক্ষেত্রে - সম্ভাব্য সবচেয়ে কম বাড়তি শক্তি কত?", ["0 kN", "10 kN", "20 kN", "5 kN"],
        "সবচেয়ে কম শক্তি 45 - সবচেয়ে বেশি বোঝা 45 = 0। আসন্ন করা আসল ঝুঁকি লুকোতে পারে!"),
    mcq("What is tan⁻¹ used for?", ["Finding an angle when you know the tangent ratio (opposite ÷ adjacent)", "Finding a side from an angle only", "Finding the area of a triangle", "Undoing a square"], 0,
        "On a calculator it is often SHIFT + tan.",
        "tan⁻¹ কীসের জন্য ব্যবহার হয়?", ["ট্যানজেন্ট অনুপাত (বিপরীত ÷ সন্নিহিত) জানা থাকলে কোণ বের করতে", "শুধু কোণ থেকে বাহু বের করতে", "ত্রিভুজের ক্ষেত্রফল বের করতে", "বর্গ খুলতে"],
        "ক্যালকুলেটরে প্রায়ই SHIFT + tan।"),
    mcq("A road gradient of 1 in 20 means…", ["It rises 1 m for every 20 m along", "It rises 20 m for every 1 m", "It is 20° steep", "It is flat"], 0,
        "As a percentage that is 5%.",
        "রাস্তার ঢাল '20-এ 1' মানে…", ["প্রতি 20 m এগোলে 1 m ওঠে", "প্রতি 1 m-এ 20 m ওঠে", "20° খাড়া", "সমতল"],
        "শতাংশে সেটা 5%।"),
    mcq("A ramp for wheelchairs should be no steeper than 1 in 12. A ramp must rise 0.5 m. What is the least horizontal length?", ["6 m", "12 m", "0.5 m", "24 m"], 0,
        "0.5 x 12 = 6 m.",
        "হুইলচেয়ারের ঢাল 12-এ 1-এর বেশি খাড়া হওয়া উচিত নয়। একটা ঢালকে 0.5 m উঠতে হবে। ন্যূনতম অনুভূমিক দৈর্ঘ্য কত?", ["6 m", "12 m", "0.5 m", "24 m"],
        "0.5 x 12 = 6 m।"),
    mcq("What is the volume of a cylinder of radius 2 m and height 10 m, in terms of π?", ["40π m³", "20π m³", "400π m³", "4π m³"], 0,
        "V = πr²h = π x 4 x 10 = 40π m³.",
        "2 m ব্যাসার্ধ আর 10 m উচ্চতার চোঙের আয়তন π-এর হিসেবে কত?", ["40π m³", "20π m³", "400π m³", "4π m³"],
        "V = πr²h = π x 4 x 10 = 40π m³।"),
    mcq("What is the curved surface area of a sphere of radius 5 m, in terms of π? (A = 4πr²)", ["100π m²", "25π m²", "20π m²", "500π m²"], 0,
        "4 x π x 25 = 100π m².",
        "5 m ব্যাসার্ধের গোলকের বাঁকা পৃষ্ঠতল π-এর হিসেবে কত? (A = 4πr²)", ["100π m²", "25π m²", "20π m²", "500π m²"],
        "4 x π x 25 = 100π m²।"),
    mcq("If you double the radius of a spherical tank, its volume becomes…", ["8 times as big", "2 times as big", "4 times as big", "the same"], 0,
        "Volume depends on r³, and 2³ = 8.",
        "গোলাকার ট্যাঙ্কের ব্যাসার্ধ দ্বিগুণ করলে আয়তন হয়…", ["8 গুণ", "2 গুণ", "4 গুণ", "একই"],
        "আয়তন r³-এর উপর নির্ভর করে, আর 2³ = 8।"),
    mcq("What is a 'vector'?", ["A quantity with both size and direction, like a force or a displacement", "Only a size, like mass", "A type of triangle", "A straight line graph"], 0,
        "Forces in a truss are vectors - they add head to tail.",
        "'ভেক্টর' কী?", ["মান আর দিক দুটোই আছে এমন রাশি, যেমন বল বা সরণ", "শুধু মান, যেমন ভর", "এক রকম ত্রিভুজ", "সরলরেখার লেখচিত্র"],
        "ট্রাসের বলগুলো ভেক্টর - মাথা থেকে লেজে জুড়ে যোগ হয়।"),
    mcq("Vector a = (3, 4) and vector b = (1, -2). What is a + b?", ["(4, 2)", "(2, 6)", "(3, -8)", "(4, 6)"], 0,
        "Add the parts: (3 + 1, 4 + (-2)) = (4, 2).",
        "ভেক্টর a = (3, 4) আর ভেক্টর b = (1, -2)। a + b কত?", ["(4, 2)", "(2, 6)", "(3, -8)", "(4, 6)"],
        "অংশগুলো যোগ করো: (3 + 1, 4 + (-2)) = (4, 2)।"),
    mcq("What is the length (magnitude) of the vector (6, 8)?", ["10", "14", "48", "2"], 0,
        "√(6² + 8²) = √100 = 10.",
        "ভেক্টর (6, 8)-এর দৈর্ঘ্য (মান) কত?", ["10", "14", "48", "2"],
        "√(6² + 8²) = √100 = 10।"),
    mcq("What does 'the angle in a semicircle is 90°' mean?", ["A triangle drawn from a diameter to any point on the circle has a right angle at that point", "All circles are 90°", "Semicircles have four corners", "Diameters are always 90 cm"], 0,
        "Builders once used this to set out right angles with a rope and a peg.",
        "'অর্ধবৃত্তস্থ কোণ 90°' মানে কী?", ["ব্যাস থেকে বৃত্তের যেকোনো বিন্দুতে আঁকা ত্রিভুজের সেই বিন্দুতে সমকোণ", "সব বৃত্ত 90°", "অর্ধবৃত্তের চারটে কোণ", "ব্যাস সবসময় 90 cm"],
        "নির্মাতারা একসময় দড়ি আর খুঁটি দিয়ে এভাবে সমকোণ চিহ্নিত করতেন।"),
    mcq("What is a 'tangent' to a circle?", ["A straight line that touches the circle at exactly one point", "A line through the centre", "Any chord", "The circle's area"], 0,
        "A tangent is at 90° to the radius at the point where it touches.",
        "বৃত্তের 'স্পর্শক' কী?", ["যে সরলরেখা বৃত্তকে ঠিক একটা বিন্দুতে ছোঁয়", "কেন্দ্র দিয়ে যাওয়া রেখা", "যেকোনো জ্যা", "বৃত্তের ক্ষেত্রফল"],
        "স্পর্শবিন্দুতে স্পর্শক ব্যাসার্ধের সঙ্গে 90° করে।"),
    mcq("A road curve is designed so the straight road meets it as a tangent. Why?", ["The change from straight to curve is smooth, with no sudden kink", "Tangents are cheaper", "Curves must cross the road", "It makes the road longer"], 0,
        "Smooth transitions keep vehicles stable.",
        "রাস্তার বাঁক এমনভাবে নকশা হয় যাতে সোজা রাস্তা তাকে স্পর্শক হিসেবে মেশে। কেন?", ["সোজা থেকে বাঁকে বদল মসৃণ হয়, হঠাৎ মোচড় থাকে না", "স্পর্শক সস্তা", "বাঁককে রাস্তা কাটতে হয়", "রাস্তা লম্বা হয়"],
        "মসৃণ বদলে গাড়ি স্থির থাকে।"),
    mcq("What is a 'function' such as f(x) = 2x + 3?", ["A rule that turns each input x into exactly one output", "A random number", "A type of graph paper", "A bridge part"], 0,
        "f(4) = 2 x 4 + 3 = 11.",
        "f(x) = 2x + 3-এর মতো 'অপেক্ষক' কী?", ["যে নিয়ম প্রতিটা ইনপুট x-কে ঠিক একটা আউটপুটে বদলায়", "এলোমেলো সংখ্যা", "এক রকম গ্রাফ-কাগজ", "সেতুর অংশ"],
        "f(4) = 2 x 4 + 3 = 11।"),
    mcq("If f(x) = 3x - 2, what is f(5)?", ["13", "15", "17", "1"], 0,
        "3 x 5 - 2 = 13.",
        "f(x) = 3x - 2 হলে f(5) কত?", ["13", "15", "17", "1"],
        "3 x 5 - 2 = 13।"),
    mcq("If f(x) = 2x + 6, what is the inverse function f⁻¹(x)?", ["(x - 6) / 2", "2x - 6", "(x + 6) / 2", "x / 2 + 6"], 0,
        "Undo in reverse: subtract 6, then divide by 2.",
        "f(x) = 2x + 6 হলে বিপরীত অপেক্ষক f⁻¹(x) কী?", ["(x - 6) / 2", "2x - 6", "(x + 6) / 2", "x / 2 + 6"],
        "উল্টো ক্রমে খোলো: 6 বিয়োগ, তারপর 2 দিয়ে ভাগ।"),
    mcq("A shape is enlarged by scale factor -1 about a point. What does it look like?", ["It is turned upside down through the point, same size (a half-turn)", "Twice as big", "Half the size", "It disappears"], 0,
        "A negative scale factor puts the image on the other side of the centre.",
        "একটা আকারকে একটা বিন্দুর সাপেক্ষে -1 স্কেল-গুণকে বড় করা হলো। দেখতে কেমন হয়?", ["বিন্দুটার মধ্যে দিয়ে উল্টো ঘুরে যায়, একই মাপ (অর্ধ-আবর্তন)", "দ্বিগুণ বড়", "অর্ধেক মাপ", "মিলিয়ে যায়"],
        "ঋণাত্মক স্কেল-গুণক প্রতিবিম্বকে কেন্দ্রের অন্য পাশে বসায়।"),
    mcq("What is the probability of NOT getting a faulty bolt if P(faulty) = 0.03?", ["0.97", "0.03", "0.7", "1.03"], 0,
        "P(not A) = 1 - P(A) = 1 - 0.03 = 0.97.",
        "P(ত্রুটিপূর্ণ) = 0.03 হলে ত্রুটিপূর্ণ বল্টু না পাওয়ার সম্ভাবনা কত?", ["0.97", "0.03", "0.7", "1.03"],
        "P(A নয়) = 1 - P(A) = 1 - 0.03 = 0.97।"),
    mcq("Two independent inspections each miss a crack with probability 0.1. What is the probability both miss it?", ["0.01", "0.2", "0.1", "0.9"], 0,
        "Independent events multiply: 0.1 x 0.1 = 0.01 - two checks are far safer than one.",
        "দুটো স্বাধীন পরিদর্শনের প্রত্যেকটা 0.1 সম্ভাবনায় একটা ফাটল এড়িয়ে যায়। দুটোই এড়ানোর সম্ভাবনা কত?", ["0.01", "0.2", "0.1", "0.9"],
        "স্বাধীন ঘটনা গুণ হয়: 0.1 x 0.1 = 0.01 - একটার চেয়ে দুটো যাচাই অনেক নিরাপদ।"),
    mcq("A Venn diagram shows 30 workers: 18 can weld, 12 can drive cranes and 5 can do both. How many can do neither?", ["5", "0", "7", "13"], 0,
        "Weld or crane = 18 + 12 - 5 = 25; neither = 30 - 25 = 5.",
        "একটা ভেন-চিত্রে 30 জন কর্মী: 18 জন ঝালাই পারেন, 12 জন ক্রেন চালান আর 5 জন দুটোই পারেন। কতজন কোনোটাই পারেন না?", ["5", "0", "7", "13"],
        "ঝালাই বা ক্রেন = 18 + 12 - 5 = 25; কোনোটাই না = 30 - 25 = 5।"),
    mcq("A survey of drivers picks every 10th car at the toll plaza. What kind of sample is this?", ["Systematic sampling", "Random sampling by lottery", "Asking only friends", "A census of all drivers"], 0,
        "It is quick and spreads the sample across the day.",
        "টোল-প্লাজায় প্রতি দশম গাড়ি বেছে চালকদের সমীক্ষা হয়। এটা কোন ধরনের নমুনা?", ["নিয়মমাফিক নমুনায়ন", "লটারিতে এলোমেলো নমুনা", "শুধু বন্ধুদের জিজ্ঞাসা", "সব চালকের শুমারি"],
        "দ্রুত হয় আর নমুনা সারাদিনে ছড়িয়ে থাকে।"),
    mcq("Why might asking only morning drivers about a new bridge give a biased result?", ["Morning drivers (often commuters) may not represent everyone who uses it", "Morning drivers always lie", "Biased means correct", "Surveys must be done at night"], 0,
        "A fair sample covers different times, days and types of user.",
        "নতুন সেতু নিয়ে শুধু সকালের চালকদের জিজ্ঞাসা করলে ফল পক্ষপাতদুষ্ট হতে পারে কেন?", ["সকালের চালকরা (প্রায়ই অফিসযাত্রী) সব ব্যবহারকারীর প্রতিনিধি নাও হতে পারেন", "সকালের চালকরা সবসময় মিথ্যা বলেন", "পক্ষপাত মানে সঠিক", "সমীক্ষা রাতে করতেই হবে"],
        "ন্যায্য নমুনা আলাদা সময়, দিন আর ধরনের ব্যবহারকারীকে ধরে।"),
)
