"""Class 12 - Math (Chief Engineer): vectors and the dot product, determinants and Cramer's rule,
linear programming, the normal distribution and z-scores, differential equations for growth and
decay, Newton-Raphson iteration, regression, the chain rule, definite integrals and the
mathematical thinking behind safe, economical bridge design."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r + 2, r * 2, r + 10):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _c(x):
    x = round(x, 3)
    return int(x) if x == int(x) else x


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + ub for x in o], ex_bn)


def dot(a, b):
    d = sum(x * y for x, y in zip(a, b))
    return _n(f"Two truss members have direction vectors a = {a} and b = {b}. What is a · b?",
              f"দুটো ট্রাস-অংশের দিক-ভেক্টর a = {a} আর b = {b}। a · b কত?", d,
              f"a · b = {' + '.join(f'{x} x {y}' for x, y in zip(a, b))} = {d}.",
              f"a · b = {' + '.join(f'{x} x {y}' for x, y in zip(a, b))} = {d}।",
              (sum(a) + sum(b), abs(d) + 5, sum(x * x for x in a)))


def angle(a, b, ans):
    o = [f"{ans}°"] + [f"{v}°" for v in (90, 60, 45, 30, 0, 180) if v != ans][:3]
    na = _c(sum(x * x for x in a) ** 0.5)
    nb = _c(sum(x * x for x in b) ** 0.5)
    d = sum(x * y for x, y in zip(a, b))
    return mcq(f"What is the angle between the members along a = {a} and b = {b}?", o, 0,
               f"cos θ = (a · b) ÷ (|a||b|) = {d} ÷ ({na:g} x {nb:g}) = {_c(d / (na * nb)):g}, so θ = {ans}°.",
               f"a = {a} আর b = {b} বরাবর অংশ দুটোর মধ্যে কোণ কত?", o,
               f"cos θ = (a · b) ÷ (|a||b|) = {d} ÷ ({na:g} x {nb:g}) = {_c(d / (na * nb)):g}, তাই θ = {ans}°।")


def det2(a, b, c, d):
    r = a * d - b * c
    return _n(f"What is the determinant of the matrix [[{a}, {b}], [{c}, {d}]]?",
              f"ম্যাট্রিক্স [[{a}, {b}], [{c}, {d}]]-এর নির্ণায়ক কত?", r,
              f"det = ad - bc = {a} x {d} - {b} x {c} = {r}. A zero determinant means the system has no unique solution.",
              f"নির্ণায়ক = ad - bc = {a} x {d} - {b} x {c} = {r}। শূন্য নির্ণায়ক মানে ব্যবস্থার একক সমাধান নেই।",
              (a * d + b * c, a + d, abs(a * b - c * d) if a * b - c * d != r else r + 3)) if r > 0 else None


def cramer(a, b, e, c, d, f):
    det = a * d - b * c
    x = _c((e * d - b * f) / det)
    y = _c((a * f - e * c) / det)
    return _n(f"Solve for the support reaction x using Cramer's rule: {a}x + {b}y = {e}, {c}x + {d}y = {f}.",
              f"ক্র্যামারের নিয়মে ঠেকনা-প্রতিক্রিয়া x-এর সমাধান করো: {a}x + {b}y = {e}, {c}x + {d}y = {f}।", x,
              f"det = {det}; x = ({e} x {d} - {b} x {f}) ÷ {det} = {x:g} (and y = {y:g}).",
              f"নির্ণায়ক = {det}; x = ({e} x {d} - {b} x {f}) ÷ {det} = {x:g} (আর y = {y:g})।",
              (y if y > 0 and y != x else _c(x + 3), _c(e / a), _c(f / d))) if x > 0 else None


def lp(corners, px, py, what_en, what_bn):
    vals = [(px * x + py * y, (x, y)) for x, y in corners]
    best = max(vals)
    r = best[0]
    return _n(f"A precast yard makes beams (x) and slabs (y) with profit P = {px}x + {py}y. The feasible region's corners are {', '.join(str(c) for c in corners)}. What is the maximum profit (Rs thousand)?",
              f"একটা প্রিকাস্ট-উঠান কড়ি (x) আর স্ল্যাব (y) বানায়, লাভ P = {px}x + {py}y। সম্ভাব্য অঞ্চলের কোণ {', '.join(str(c) for c in corners)}। সর্বোচ্চ লাভ কত (হাজার টাকা)?", r,
              f"Check every corner: {', '.join(f'{c} -> {v}' for v, c in vals)}. The best is {best[1]} with P = {r}.",
              f"প্রতিটা কোণ যাচাই: {', '.join(f'{c} -> {v}' for v, c in vals)}। সেরা {best[1]}, P = {r}।",
              tuple(v for v, _ in vals if v != r)[:3] or (r // 2,))


def zscore(x, mu, sd, what_en, what_bn):
    z = _c((x - mu) / sd)
    o = []
    for v in (z, -z, _c((x - mu) / sd * 2), _c(x / mu)):
        if v not in o:
            o.append(v)
    while len(o) < 4:
        o.append(_c(o[-1] + 0.5))
    return mcq(f"{what_en} has mean {mu} and standard deviation {sd}. What is the z-score of a result of {x}?", [f"{v:g}" for v in o], 0,
               f"z = (x - μ) ÷ σ = ({x} - {mu}) ÷ {sd} = {z:g}.",
               f"{what_bn}-এর গড় {mu} আর প্রমিত বিচ্যুতি {sd}। {x} ফলের জেড-স্কোর কত?", [f"{v:g}" for v in o],
               f"z = (x - μ) ÷ σ = ({x} - {mu}) ÷ {sd} = {z:g}।")


def decay(n0, k, t):
    # use k*t = ln 2 multiples for clean answers
    n = _c(n0 * 2 ** (-k * t / 0.693))
    return _n(f"Paint thickness decays as dP/dt = -kP with k = {k:g} per year, starting at {n0} µm. What is the thickness after {t} years? (ln 2 ≈ 0.693)",
              f"রঙের পুরুত্ব dP/dt = -kP মেনে কমে, k = বছরে {k:g}, শুরু {n0} µm। {t} বছর পরে পুরুত্ব কত? (ln 2 ≈ 0.693)", n,
              f"P = P₀e^(-kt); k x t = {_c(k * t):g} = {_c(k * t / 0.693):g} half-lives, so P = {n0} x ½^{_c(k * t / 0.693):g} = {n:g} µm.",
              f"P = P₀e^(-kt); k x t = {_c(k * t):g} = {_c(k * t / 0.693):g}টি অর্ধায়ু, তাই P = {n0} x ½^{_c(k * t / 0.693):g} = {n:g} µm।",
              (_c(n0 - k * t * n0), _c(n0 / 2), _c(n * 2) if _c(n * 2) != _c(n0 / 2) else _c(n * 3)), " µm")


def newton(a, x0):
    # f(x) = x² - a, f'(x) = 2x
    x1 = _c(x0 - (x0 * x0 - a) / (2 * x0))
    return _n(f"Use one step of Newton-Raphson on f(x) = x² - {a}, starting at x₀ = {x0}. What is x₁?",
              f"f(x) = x² - {a}-এ নিউটন-র‍্যাফসনের এক ধাপ চালাও, শুরু x₀ = {x0}। x₁ কত?", x1,
              f"x₁ = x₀ - f(x₀) ÷ f'(x₀) = {x0} - ({x0 * x0} - {a}) ÷ {2 * x0} = {x1:g}, already close to √{a}.",
              f"x₁ = x₀ - f(x₀) ÷ f'(x₀) = {x0} - ({x0 * x0} - {a}) ÷ {2 * x0} = {x1:g}, ইতিমধ্যে √{a}-এর কাছাকাছি।",
              (_c(x0 + (x0 * x0 - a) / (2 * x0)), _c(a / x0), x0))


def regress(a, b, x, what_en, what_bn):
    y = _c(a + b * x)
    return _n(f"A regression line for {what_en} is y = {a} + {b}x. What does it predict when x = {x}?",
              f"{what_bn}-এর প্রতিক্রমণ-রেখা y = {a} + {b}x। x = {x} হলে এটা কী পূর্বাভাস দেয়?", y,
              f"y = {a} + {b} x {x} = {y:g}. Predictions are most reliable inside the range of the data used.",
              f"y = {a} + {b} x {x} = {y:g}। ব্যবহৃত তথ্যের পরিসরের মধ্যেই পূর্বাভাস সবচেয়ে ভরসার।",
              (_c(a * b * x), _c(b * x), _c(a + x)))


def chain(a, b, n, x0):
    d = n * a * (a * x0 + b) ** (n - 1)
    return _n(f"If y = ({a}x + {b})^{n}, what is dy/dx at x = {x0}?",
              f"y = ({a}x + {b})^{n} হলে x = {x0}-এ dy/dx কত?", d,
              f"Chain rule: dy/dx = {n} x {a} x ({a}x + {b})^{n - 1} = {n * a} x {a * x0 + b}^{n - 1} = {d:,}.",
              f"শৃঙ্খল-নিয়ম: dy/dx = {n} x {a} x ({a}x + {b})^{n - 1} = {n * a} x {a * x0 + b}^{n - 1} = {d:,}।",
              (n * (a * x0 + b) ** (n - 1), (a * x0 + b) ** n, d + n))


def defint(a, b, c):
    r = _c(a * c * c / 2 + b * c)
    return _n(f"Evaluate the integral of ({a}x + {b}) dx from x = 0 to x = {c}.",
              f"x = 0 থেকে x = {c} পর্যন্ত ({a}x + {b}) dx-এর সমাকলন করো।", r,
              f"[{_c(a / 2):g}x² + {b}x] from 0 to {c} = {_c(a / 2):g} x {c * c} + {b} x {c} = {r:g}.",
              f"0 থেকে {c} পর্যন্ত [{_c(a / 2):g}x² + {b}x] = {_c(a / 2):g} x {c * c} + {b} x {c} = {r:g}।",
              (a * c + b, _c(a * c * c + b * c), _c(r / 2)))


ITEMS = tuple(q for q in (
    dot((1, 2, 3), (4, 5, 6)), dot((2, 0, 1), (3, 4, 2)), dot((5, 1, 2), (1, 3, 4)), dot((2, 3, 1), (4, 1, 5)),
    dot((3, 2, 2), (2, 2, 3)), dot((6, 1, 1), (1, 2, 7)),
    angle((1, 0, 0), (0, 1, 0), 90), angle((1, 1, 0), (1, 0, 0), 45), angle((1, 0, 0), (2, 0, 0), 0), angle((1, 1, 0), (0, 1, 1), 60),
    det2(4, 2, 1, 3), det2(5, 1, 2, 4), det2(6, 2, 3, 5), det2(7, 3, 2, 4), det2(8, 3, 2, 5), det2(9, 4, 1, 3),
    cramer(2, 1, 10, 1, 3, 15), cramer(3, 2, 18, 1, 4, 16), cramer(1, 1, 50, 2, 1, 70), cramer(4, 1, 24, 1, 2, 20),
    lp([(0, 0), (0, 8), (4, 6), (7, 0)], 5, 4, "", ""), lp([(0, 0), (0, 10), (6, 4), (8, 0)], 3, 5, "", ""), lp([(0, 0), (0, 5), (5, 5), (9, 0)], 6, 7, "", ""),
    lp([(0, 0), (0, 12), (5, 9), (10, 0)], 4, 3, "", ""),
    zscore(45, 40, 2.5, "Concrete cube strength (N/mm²)", "কংক্রিট-ঘনকের শক্তি (N/mm²)"), zscore(36, 40, 2, "Concrete cube strength (N/mm²)", "কংক্রিট-ঘনকের শক্তি (N/mm²)"),
    zscore(520, 500, 10, "Bolt tensile strength (N/mm²)", "বল্টুর টান-শক্তি (N/mm²)"), zscore(31, 25, 4, "Deck temperature (°C)", "পাটাতনের তাপমাত্রা (°C)"),
    zscore(88, 100, 8, "Daily cement delivery (tonnes)", "প্রতিদিনের সিমেন্ট-সরবরাহ (টন)"),
    decay(240, 0.0693, 10), decay(300, 0.1386, 10), decay(200, 0.03465, 20),
    newton(10, 3), newton(20, 4), newton(50, 7), newton(30, 5), newton(70, 8),
    regress(12, 0.8, 50, "toll income (Rs lakh) against traffic (thousand vehicles)", "যান (হাজার) বনাম টোল-আয় (লাখ টাকা)"),
    regress(5, 2.5, 12, "crack width (0.01 mm) against age (years)", "বয়স (বছর) বনাম ফাটলের চওড়া (0.01 mm)"),
    regress(20, 1.5, 30, "concrete strength against curing days", "কিউরিং-দিন বনাম কংক্রিটের শক্তি"),
    regress(3, 0.25, 40, "deck deflection (mm) against load (tonnes)", "বোঝা (টন) বনাম পাটাতনের বিক্ষেপ (mm)"),
    chain(2, 1, 3, 1), chain(3, 1, 2, 2), chain(2, 3, 2, 1), chain(4, 1, 2, 3), chain(5, 2, 3, 1),
    defint(2, 3, 4), defint(6, 1, 2), defint(4, 6, 5), defint(10, 2, 3), defint(8, 5, 2),
    mcq("What does a dot product of zero tell you about two vectors?", ["They are perpendicular", "They are parallel", "They are equal", "One is zero length always"], 0,
        "cos 90° = 0, so a · b = 0.",
        "দুটো ভেক্টরের ডট-গুণফল শূন্য হলে কী বোঝায়?", ["এরা লম্ব", "এরা সমান্তরাল", "এরা সমান", "একটা সবসময় শূন্য দৈর্ঘ্যের"],
        "cos 90° = 0, তাই a · b = 0।"),
    mcq("What is the 'cross product' of two vectors used for in statics?", ["Finding the moment of a force about a point in 3D (r x F)", "Adding forces", "Finding a length", "Measuring temperature"], 0,
        "Its direction gives the axis of rotation.",
        "স্থিতিবিদ্যায় দুটো ভেক্টরের 'ক্রস-গুণফল' কীসের জন্য ব্যবহার হয়?", ["ত্রিমাত্রায় একটা বিন্দুর সাপেক্ষে বলের ভ্রামক বের করতে (r x F)", "বল যোগ করতে", "দৈর্ঘ্য বের করতে", "তাপমাত্রা মাপতে"],
        "এর দিক ঘূর্ণনের অক্ষ দেয়।"),
    mcq("What is the inverse of a 2 x 2 matrix used for?", ["Solving a system of linear equations Ax = b by x = A⁻¹b", "Doubling a matrix", "Finding its colour", "Drawing graphs only"], 0,
        "It exists only if the determinant is not zero.",
        "2 x 2 ম্যাট্রিক্সের বিপরীত কীসের জন্য ব্যবহার হয়?", ["রৈখিক সমীকরণ-ব্যবস্থা Ax = b-কে x = A⁻¹b দিয়ে সমাধান করতে", "ম্যাট্রিক্স দ্বিগুণ করতে", "রং বের করতে", "শুধু লেখচিত্র আঁকতে"],
        "নির্ণায়ক শূন্য না হলেই এটা থাকে।"),
    mcq("Why do structural engineers rely on matrix methods?", ["Large structures give hundreds of simultaneous equations, which matrices organise for computers", "Matrices make drawings prettier", "Hand methods are forbidden", "Matrices are only for finance"], 0,
        "The stiffness matrix links forces and displacements at every joint.",
        "কাঠামো-প্রকৌশলীরা ম্যাট্রিক্স-পদ্ধতির উপর নির্ভর করেন কেন?", ["বড় কাঠামোয় শত শত যুগপৎ সমীকরণ হয়, যা ম্যাট্রিক্স কম্পিউটারের জন্য সাজায়", "ম্যাট্রিক্স নকশা সুন্দর করে", "হাতের পদ্ধতি নিষিদ্ধ", "ম্যাট্রিক্স শুধু অর্থের জন্য"],
        "দৃঢ়তা-ম্যাট্রিক্স প্রতিটা জোড়ে বল আর সরণ জোড়ে।"),
    mcq("What is 'linear programming'?", ["Finding the best value of a linear objective, like profit or cost, subject to linear constraints", "Writing computer code in a line", "Drawing straight roads", "A TV schedule"], 0,
        "The optimum lies at a corner of the feasible region.",
        "'রৈখিক প্রোগ্রামিং' কী?", ["রৈখিক শর্ত মেনে লাভ বা খরচের মতো রৈখিক লক্ষ্যের সেরা মান খোঁজা", "এক লাইনে কম্পিউটার-কোড লেখা", "সোজা রাস্তা আঁকা", "টিভির সময়সূচি"],
        "সর্বোত্তম মান সম্ভাব্য অঞ্চলের কোনো কোণে থাকে।"),
    mcq("Why does the optimum of a linear programme lie at a corner of the feasible region?", ["A linear objective increases steadily in one direction, so it is maximised at an extreme point", "Corners are lucky", "The middle is always best", "It never does"], 0,
        "So only the corner points need checking.",
        "রৈখিক প্রোগ্রামের সর্বোত্তম মান সম্ভাব্য অঞ্চলের কোণে থাকে কেন?", ["রৈখিক লক্ষ্য একদিকে স্থিরভাবে বাড়ে, তাই চরম বিন্দুতে সর্বোচ্চ হয়", "কোণ শুভ", "মাঝখান সবসময় সেরা", "কখনো থাকে না"],
        "তাই শুধু কোণবিন্দুগুলো যাচাই করলেই চলে।"),
    mcq("A transport problem asks how to send cement from 3 plants to 4 sites at least cost. What technique fits?", ["Linear programming (a transportation model)", "Pythagoras only", "Random guessing", "The quadratic formula"], 0,
        "Supply and demand limits are the constraints.",
        "একটা পরিবহন-সমস্যা জানতে চায় 3টি কারখানা থেকে 4টি নির্মাণস্থলে সবচেয়ে কম খরচে সিমেন্ট কীভাবে পাঠানো যায়। কোন কৌশল মানানসই?", ["রৈখিক প্রোগ্রামিং (পরিবহন-মডেল)", "শুধু পিথাগোরাস", "এলোমেলো আন্দাজ", "দ্বিঘাত সূত্র"],
        "জোগান আর চাহিদার সীমাই শর্ত।"),
    mcq("What does a z-score of -2 mean?", ["The value is 2 standard deviations below the mean", "It is 2 above the mean", "It equals the mean", "It is impossible"], 0,
        "Only about 2.3% of normal results lie below z = -2.",
        "-2-এর জেড-স্কোর মানে কী?", ["মানটা গড়ের 2 প্রমিত বিচ্যুতি নিচে", "গড়ের 2 উপরে", "গড়ের সমান", "অসম্ভব"],
        "স্বাভাবিক ফলের মাত্র প্রায় 2.3% z = -2-এর নিচে থাকে।"),
    mcq("In a normal distribution, about what percentage of values lie within one standard deviation of the mean?", ["68%", "50%", "95%", "99.7%"], 0,
        "About 95% lie within two, and 99.7% within three.",
        "স্বাভাবিক বণ্টনে মোটামুটি কত শতাংশ মান গড়ের এক প্রমিত বিচ্যুতির মধ্যে থাকে?", ["68%", "50%", "95%", "99.7%"],
        "প্রায় 95% দুইয়ের মধ্যে, আর 99.7% তিনের মধ্যে।"),
    mcq("Why are concrete strength specifications based on the lower tail of a normal distribution?", ["Safety depends on the weak results, so engineers control the proportion that falls below the specified value", "Average strength is all that matters", "Strong results are dangerous", "Distributions are ignored"], 0,
        "Characteristic strength is typically the 5% lower fractile.",
        "কংক্রিট-শক্তির নির্দেশিকা স্বাভাবিক বণ্টনের নিচের লেজের উপর নির্ভর করে কেন?", ["নিরাপত্তা দুর্বল ফলের উপর নির্ভর করে, তাই প্রকৌশলীরা নির্দিষ্ট মানের নিচে পড়া অংশ নিয়ন্ত্রণ করেন", "শুধু গড় শক্তি গুরুত্বপূর্ণ", "শক্ত ফল বিপজ্জনক", "বণ্টন উপেক্ষা করা হয়"],
        "বৈশিষ্ট্যসূচক শক্তি সাধারণত নিচের 5% ভাগ।"),
    mcq("What is the solution of dN/dt = -kN?", ["N = N₀e^(-kt), exponential decay", "N = N₀ + kt", "N = kt²", "N is constant"], 0,
        "The rate of loss is proportional to what remains.",
        "dN/dt = -kN-এর সমাধান কী?", ["N = N₀e^(-kt), সূচকীয় ক্ষয়", "N = N₀ + kt", "N = kt²", "N স্থির"],
        "যা বাকি আছে তার সমানুপাতে কমে।"),
    mcq("What is a 'differential equation'?", ["An equation relating a function to its rates of change (derivatives)", "An equation with two unknowns only", "A difference between two numbers", "A table of values"], 0,
        "Beam deflection, vibration and cooling are all described by differential equations.",
        "'অবকল সমীকরণ' কী?", ["যে সমীকরণ একটা অপেক্ষককে তার পরিবর্তনের হারের (অবকলজের) সঙ্গে জোড়ে", "শুধু দুটো অজানার সমীকরণ", "দুটো সংখ্যার পার্থক্য", "মানের তালিকা"],
        "কড়ির বিক্ষেপ, কম্পন আর ঠান্ডা হওয়া সবই অবকল সমীকরণে বর্ণিত।"),
    mcq("The beam equation EI d²y/dx² = M(x) links what?", ["The curvature of the deflected beam to the bending moment along it", "Temperature to time", "Cost to profit", "Speed to distance"], 0,
        "Integrating twice gives the deflected shape.",
        "কড়ির সমীকরণ EI d²y/dx² = M(x) কীসের সম্পর্ক দেখায়?", ["বাঁকা কড়ির বক্রতার সঙ্গে তার বরাবর বাঁকানো ভ্রামক", "তাপমাত্রার সঙ্গে সময়", "খরচের সঙ্গে লাভ", "গতির সঙ্গে দূরত্ব"],
        "দুবার সমাকলন করলে বাঁকা আকার মেলে।"),
    mcq("What does Newton-Raphson iteration do?", ["Uses the tangent at a guess to find a better approximation to a root, repeating until it settles", "Adds numbers in a series", "Draws circles", "Finds averages"], 0,
        "It usually converges very quickly when started near the root.",
        "নিউটন-র‍্যাফসন পুনরাবৃত্তি কী করে?", ["একটা আন্দাজে স্পর্শক ব্যবহার করে বীজের আরও ভালো আসন্ন মান খোঁজে, থিতু না হওয়া পর্যন্ত বারবার", "শ্রেণির সংখ্যা যোগ করে", "বৃত্ত আঁকে", "গড় বের করে"],
        "বীজের কাছ থেকে শুরু করলে সাধারণত খুব দ্রুত মিলে যায়।"),
    mcq("When can Newton-Raphson fail?", ["When the derivative is near zero at a guess, sending the next estimate far away", "Never", "When the function is linear", "When the root is positive"], 0,
        "A good starting value matters.",
        "নিউটন-র‍্যাফসন কখন ব্যর্থ হতে পারে?", ["যখন আন্দাজে অবকলজ শূন্যের কাছে, পরের আন্দাজ অনেক দূরে পাঠায়", "কখনো না", "অপেক্ষক রৈখিক হলে", "বীজ ধনাত্মক হলে"],
        "ভালো শুরুর মান জরুরি।"),
    mcq("What does the correlation coefficient r = 0.95 suggest?", ["A strong positive linear relationship", "No relationship", "A strong negative relationship", "That x causes y for certain"], 0,
        "r ranges from -1 to +1.",
        "সহসম্পর্ক-গুণাঙ্ক r = 0.95 কী বোঝায়?", ["জোরালো ধনাত্মক রৈখিক সম্পর্ক", "কোনো সম্পর্ক নেই", "জোরালো ঋণাত্মক সম্পর্ক", "নিশ্চিতভাবে x, y-এর কারণ"],
        "r -1 থেকে +1 পর্যন্ত।"),
    mcq("What is the 'least squares' method for a regression line?", ["Choosing the line that minimises the sum of squared vertical distances from the points", "Drawing a line through the first two points", "Using the largest values only", "Guessing a line"], 0,
        "It gives the best-fit straight line.",
        "প্রতিক্রমণ-রেখার 'ন্যূনতম বর্গ' পদ্ধতি কী?", ["যে রেখা বিন্দুগুলো থেকে উল্লম্ব দূরত্বের বর্গের যোগফল সবচেয়ে কম করে সেটা বাছা", "প্রথম দুটো বিন্দু দিয়ে রেখা টানা", "শুধু বড় মান ব্যবহার", "রেখা আন্দাজ করা"],
        "সবচেয়ে ভালো-মেলা সরলরেখা দেয়।"),
    mcq("What is the chain rule for differentiation?", ["dy/dx = dy/du x du/dx for a function of a function", "dy/dx = dy + dx", "dy/dx = u + v", "Derivatives cannot be combined"], 0,
        "It is used whenever one quantity depends on another that changes.",
        "অবকলনের শৃঙ্খল-নিয়ম কী?", ["অপেক্ষকের অপেক্ষকের জন্য dy/dx = dy/du x du/dx", "dy/dx = dy + dx", "dy/dx = u + v", "অবকলজ মেশানো যায় না"],
        "একটা রাশি পরিবর্তনশীল আরেকটার উপর নির্ভর করলেই ব্যবহার হয়।"),
    mcq("What is the product rule?", ["d(uv)/dx = u dv/dx + v du/dx", "d(uv)/dx = du/dx x dv/dx", "d(uv)/dx = u + v", "d(uv)/dx = 0"], 0,
        "Use it when differentiating a product of two functions.",
        "গুণফল-নিয়ম কী?", ["d(uv)/dx = u dv/dx + v du/dx", "d(uv)/dx = du/dx x dv/dx", "d(uv)/dx = u + v", "d(uv)/dx = 0"],
        "দুটো অপেক্ষকের গুণফলের অবকলনে ব্যবহার করো।"),
    mcq("What does a definite integral of a load intensity w(x) along a beam give?", ["The total load on that length of beam", "The beam's colour", "The maximum stress directly", "The beam's temperature"], 0,
        "Integrating once more gives the moment.",
        "কড়ি বরাবর বোঝা-তীব্রতা w(x)-এর নির্দিষ্ট সমাকলন কী দেয়?", ["কড়ির সেই দৈর্ঘ্যে মোট বোঝা", "কড়ির রং", "সরাসরি সর্বোচ্চ পীড়ন", "কড়ির তাপমাত্রা"],
        "আরও একবার সমাকলন করলে ভ্রামক মেলে।"),
    mcq("What does 'volume of revolution' calculate?", ["The volume formed when a curve is rotated about an axis, like a turned pier or tank", "The speed of a wheel", "The number of turns", "The area of a circle only"], 0,
        "V = π∫y² dx about the x-axis.",
        "'আবর্তনের আয়তন' কী হিসাব করে?", ["একটা বক্ররেখা অক্ষের চারপাশে ঘোরালে তৈরি আয়তন, যেমন কুঁদে-তোলা স্তম্ভ বা ট্যাঙ্ক", "চাকার গতি", "পাকের সংখ্যা", "শুধু বৃত্তের ক্ষেত্রফল"],
        "x-অক্ষের চারপাশে V = π∫y² dx।"),
    mcq("What is the length of a shallow parabolic cable of span L and sag d approximately?", ["L + 8d² ÷ (3L)", "L only", "2L", "L + d"], 0,
        "A small sag adds only a little length - useful for ordering cable.",
        "স্প্যান L আর ঝোল d-এর অগভীর অধিবৃত্তাকার তারের দৈর্ঘ্য মোটামুটি কত?", ["L + 8d² ÷ (3L)", "শুধু L", "2L", "L + d"],
        "ছোট ঝোল অল্পই দৈর্ঘ্য যোগ করে - তার অর্ডারে কাজের।"),
    mcq("Using L + 8d²/(3L), how long is a cable spanning 300 m with a 30 m sag?", ["About 308 m", "About 330 m", "About 300 m", "About 360 m"], 0,
        "8 x 900 ÷ 900 = 8, so about 308 m.",
        "L + 8d²/(3L) ধরে 30 m ঝোলে 300 m বিস্তৃত তার কত লম্বা?", ["প্রায় 308 m", "প্রায় 330 m", "প্রায় 300 m", "প্রায় 360 m"],
        "8 x 900 ÷ 900 = 8, তাই প্রায় 308 m।"),
    mcq("What is 'optimisation' in structural design?", ["Finding the design that minimises cost or weight while meeting all strength and deflection limits", "Making a bridge as big as possible", "Using the most steel", "Ignoring the limits"], 0,
        "Calculus and computer search methods both help.",
        "কাঠামো-নকশায় 'সর্বোত্তমকরণ' কী?", ["সব শক্তি আর বিক্ষেপের সীমা মেনে যে নকশা খরচ বা ওজন সবচেয়ে কম করে, তা খোঁজা", "সেতু যত বড় সম্ভব করা", "সবচেয়ে বেশি ইস্পাত ব্যবহার", "সীমা উপেক্ষা"],
        "ক্যালকুলাস আর কম্পিউটার-অনুসন্ধান দুটোই সাহায্য করে।"),
    mcq("A beam's strength is proportional to bd². For a fixed area bd, why is a deeper, narrower beam stronger?", ["Strength grows with the square of depth, so putting area into depth gains more than width", "Width matters more", "Shape never matters", "Narrow beams are always weak"], 0,
        "But very thin beams can buckle sideways, so limits apply.",
        "কড়ির শক্তি bd²-এর সমানুপাতিক। নির্দিষ্ট ক্ষেত্রফল bd-তে গভীর, সরু কড়ি বেশি শক্ত কেন?", ["শক্তি গভীরতার বর্গের সঙ্গে বাড়ে, তাই ক্ষেত্রফল গভীরতায় দিলে চওড়ার চেয়ে বেশি লাভ", "চওড়া বেশি গুরুত্বপূর্ণ", "আকার কখনো গুরুত্বপূর্ণ নয়", "সরু কড়ি সবসময় দুর্বল"],
        "তবে খুব পাতলা কড়ি পাশে বেঁকে যেতে পারে, তাই সীমা আছে।"),
    mcq("What does 'convergence' mean in an iterative calculation?", ["Successive results get closer and closer to a final value", "Results jump about randomly", "The calculation stops at once", "The answer is always zero"], 0,
        "Engineers stop when the change is below a set tolerance.",
        "পুনরাবৃত্তিমূলক হিসাবে 'অভিসরণ' মানে কী?", ["পরপর ফল ক্রমশ একটা শেষ মানের কাছে আসে", "ফল এলোমেলো লাফায়", "হিসাব তখনই থামে", "উত্তর সবসময় শূন্য"],
        "বদল একটা নির্দিষ্ট সহনশীলতার নিচে নামলে প্রকৌশলীরা থামেন।"),
    mcq("What is a 'probability density function' (PDF)?", ["A curve whose area over an interval gives the probability of a value in that interval", "A list of probabilities that add to 100", "A type of file", "A bar chart only"], 0,
        "The total area under it is 1.",
        "'সম্ভাবনা-ঘনত্ব অপেক্ষক' (পিডিএফ) কী?", ["যে বক্ররেখার একটা পরিসরের ক্ষেত্রফল সেই পরিসরে মান পড়ার সম্ভাবনা দেয়", "100-তে যোগ হওয়া সম্ভাবনার তালিকা", "এক রকম ফাইল", "শুধু বার-চার্ট"],
        "এর নিচে মোট ক্ষেত্রফল 1।"),
    mcq("What is the 'expected value' of a random variable?", ["Its long-run average, found by weighting each value by its probability", "Its largest value", "Its most likely value only", "Its smallest value"], 0,
        "Risk assessments use expected losses to rank hazards.",
        "দৈব চলরাশির 'প্রত্যাশিত মান' কী?", ["দীর্ঘমেয়াদি গড়, প্রতিটা মানকে তার সম্ভাবনায় ভারযুক্ত করে পাওয়া", "সবচেয়ে বড় মান", "শুধু সবচেয়ে সম্ভাব্য মান", "সবচেয়ে ছোট মান"],
        "ঝুঁকি-মূল্যায়ন বিপদের ক্রম ঠিক করতে প্রত্যাশিত ক্ষতি ব্যবহার করে।"),
    mcq("What is a 'return period' of 100 years for a flood?", ["A flood with a 1% chance of being exceeded in any one year", "A flood that happens exactly every 100 years", "The last flood was 100 years ago", "A flood that lasts 100 years"], 0,
        "Over a 100-year bridge life, there is about a 63% chance of at least one such flood.",
        "বন্যার '100 বছরের প্রত্যাবর্তন-কাল' কী?", ["যে বন্যা যেকোনো এক বছরে ছাড়ানোর সম্ভাবনা 1%", "ঠিক প্রতি 100 বছরে হওয়া বন্যা", "শেষ বন্যা 100 বছর আগে", "100 বছর স্থায়ী বন্যা"],
        "100 বছরের সেতু-জীবনে অন্তত একবার এমন বন্যার সম্ভাবনা প্রায় 63%।"),
    mcq("What is the chance of at least one '100-year flood' during a 100-year bridge life?", ["About 63%", "Exactly 100%", "1%", "About 37%"], 0,
        "1 - 0.99¹⁰⁰ ≈ 0.63.",
        "100 বছরের সেতু-জীবনে অন্তত একটা '100 বছরের বন্যা'-র সম্ভাবনা কত?", ["প্রায় 63%", "ঠিক 100%", "1%", "প্রায় 37%"],
        "1 - 0.99¹⁰⁰ ≈ 0.63।"),
    mcq("What is 'Monte Carlo simulation' used for in project planning?", ["Running thousands of random scenarios to estimate the range and likelihood of costs or durations", "Gambling", "Designing cars", "Counting bolts"], 0,
        "It produces outcomes like 'a 90% chance of finishing by June'.",
        "প্রকল্প-পরিকল্পনায় 'মন্টে কার্লো অনুকরণ' কীসের জন্য ব্যবহার হয়?", ["খরচ বা সময়ের পরিসর আর সম্ভাবনা আন্দাজে হাজার হাজার দৈব পরিস্থিতি চালানো", "জুয়া", "গাড়ির নকশা", "বল্টু গোনা"],
        "'জুনের মধ্যে শেষ হওয়ার 90% সম্ভাবনা'-র মতো ফল দেয়।"),
    mcq("What is 'reliability index' (β) in structural design?", ["A measure of how many standard deviations the safety margin is above failure", "The number of inspectors", "A bridge's age", "A price index"], 0,
        "Higher β means a lower probability of failure.",
        "কাঠামো-নকশায় 'নির্ভরযোগ্যতা-সূচক' (β) কী?", ["নিরাপত্তা-ফাঁক ব্যর্থতার উপরে কত প্রমিত বিচ্যুতি, তার মাপ", "পরিদর্শকের সংখ্যা", "সেতুর বয়স", "মূল্যসূচক"],
        "বেশি β মানে ব্যর্থতার কম সম্ভাবনা।"),
    mcq("What does 'sensitivity' of a design result to an input mean?", ["How much the result changes when that input changes slightly", "How easily the design is offended", "The colour of the result", "The input's cost"], 0,
        "Engineers focus checking effort on the most sensitive inputs.",
        "নকশার ফলের কোনো ইনপুটের প্রতি 'সংবেদনশীলতা' মানে কী?", ["সেই ইনপুট একটু বদলালে ফল কতটা বদলায়", "নকশা কত সহজে আহত হয়", "ফলের রং", "ইনপুটের দাম"],
        "প্রকৌশলীরা সবচেয়ে সংবেদনশীল ইনপুট যাচাইয়ে বেশি মনোযোগ দেন।"),
    mcq("What is a 'Fourier series' used for in bridge vibration analysis?", ["Breaking a complex vibration into a sum of simple sine waves of different frequencies", "Counting bridge cables", "Finding areas", "Adding money"], 0,
        "It reveals which frequencies dominate a measured response.",
        "সেতুর কম্পন-বিশ্লেষণে 'ফুরিয়ে শ্রেণি' কীসের জন্য ব্যবহার হয়?", ["জটিল কম্পনকে আলাদা কম্পাঙ্কের সরল সাইন-তরঙ্গের যোগফলে ভাঙা", "সেতুর তার গোনা", "ক্ষেত্রফল বের করা", "টাকা যোগ করা"],
        "মাপা সাড়ায় কোন কম্পাঙ্ক প্রধান তা প্রকাশ করে।"),
    mcq("What is an 'eigenvalue' in structural dynamics?", ["A value linked to a natural frequency of the structure, found from its stiffness and mass matrices", "A type of steel", "The price of a beam", "A random number"], 0,
        "Each eigenvector gives the matching mode shape.",
        "কাঠামো-গতিবিদ্যায় 'আইগেন-মান' কী?", ["কাঠামোর একটা স্বাভাবিক কম্পাঙ্কের সঙ্গে যুক্ত মান, যা দৃঢ়তা আর ভর-ম্যাট্রিক্স থেকে বের হয়", "এক রকম ইস্পাত", "কড়ির দাম", "দৈব সংখ্যা"],
        "প্রতিটা আইগেন-ভেক্টর মিলিয়ে কম্পন-রূপ দেয়।"),
    mcq("What is 'interpolation' in an engineering table?", ["Estimating a value between two known table values", "Guessing far beyond the table", "Deleting a value", "Rounding to zero"], 0,
        "Linear interpolation assumes a straight line between the points.",
        "প্রকৌশল-তালিকায় 'অন্তর্বেশন' কী?", ["তালিকার দুটো জানা মানের মধ্যের মান আন্দাজ", "তালিকার অনেক বাইরে আন্দাজ", "একটা মান মুছে ফেলা", "শূন্যে আসন্ন করা"],
        "রৈখিক অন্তর্বেশন বিন্দুগুলোর মধ্যে সরলরেখা ধরে নেয়।"),
    mcq("A table gives a factor of 1.20 at 20 m and 1.40 at 30 m. Using linear interpolation, what is it at 25 m?", ["1.30", "1.25", "1.35", "1.20"], 0,
        "Halfway between 20 and 30, so halfway between 1.20 and 1.40.",
        "একটা তালিকায় 20 m-এ গুণক 1.20 আর 30 m-এ 1.40। রৈখিক অন্তর্বেশনে 25 m-এ কত?", ["1.30", "1.25", "1.35", "1.20"],
        "20 আর 30-এর ঠিক মাঝখানে, তাই 1.20 আর 1.40-এর মাঝখানে।"),
    mcq("What is 'significant figures' discipline in final design answers?", ["Reporting answers to a precision that matches the input data, not every calculator digit", "Using as many digits as possible", "Rounding everything to zero", "Writing answers in words"], 0,
        "False precision can mislead.",
        "শেষ নকশা-উত্তরে 'সার্থক অঙ্কের' শৃঙ্খলা কী?", ["ইনপুট তথ্যের সঙ্গে মানানসই নির্ভুলতায় উত্তর দেওয়া, ক্যালকুলেটরের সব অঙ্ক নয়", "যত বেশি অঙ্ক সম্ভব ব্যবহার", "সব শূন্যে আসন্ন করা", "কথায় উত্তর লেখা"],
        "মিথ্যা নির্ভুলতা বিভ্রান্ত করতে পারে।"),
    mcq("What is the purpose of a 'mathematical proof' that a design method is safe in all cases?", ["It guarantees the method's rule holds generally, not just for the examples tried", "To make reports longer", "Proofs are never used in engineering", "To replace all testing"], 0,
        "Theory and testing together build confidence.",
        "একটা নকশা-পদ্ধতি সব ক্ষেত্রে নিরাপদ এমন 'গাণিতিক প্রমাণ'-এর উদ্দেশ্য কী?", ["নিশ্চিত করে যে পদ্ধতির নিয়ম শুধু চেষ্টা-করা উদাহরণে নয়, সাধারণভাবে খাটে", "প্রতিবেদন লম্বা করতে", "প্রকৌশলে প্রমাণ কখনো ব্যবহার হয় না", "সব পরীক্ষার বদলি হতে"],
        "তত্ত্ব আর পরীক্ষা মিলে আস্থা গড়ে।"),
    mcq("What is 'dimensional homogeneity'?", ["Every term in a valid physical equation has the same units", "All numbers are equal", "All dimensions are in metres", "Using only one unit"], 0,
        "A quick check that catches many algebra errors.",
        "'মাত্রিক সমতা' কী?", ["বৈধ ভৌত সমীকরণের প্রতিটা পদের একক একই", "সব সংখ্যা সমান", "সব মাপ মিটারে", "শুধু একটা একক ব্যবহার"],
        "দ্রুত যাচাই, যা অনেক বীজগণিতের ভুল ধরে।"),
    mcq("What is the 'mean value theorem' idea in simple terms?", ["Somewhere between two points the instantaneous rate equals the average rate", "The mean is always zero", "Values never change", "Averages are meaningless"], 0,
        "If a truck averaged 60 km/h, at some moment it was doing exactly 60.",
        "সহজ কথায় 'গড়-মান উপপাদ্য'-র ভাবনা কী?", ["দুই বিন্দুর মধ্যে কোথাও তাৎক্ষণিক হার গড় হারের সমান", "গড় সবসময় শূন্য", "মান কখনো বদলায় না", "গড় অর্থহীন"],
        "একটা ট্রাক গড়ে 60 km/h চললে কোনো মুহূর্তে ঠিক 60-তে ছিল।"),
    mcq("What is a 'logistic growth' curve?", ["Growth that is fast at first then levels off as it approaches a maximum capacity", "Straight-line growth", "Endless exponential growth", "Decay to zero"], 0,
        "Traffic on a new bridge often follows such an S-curve to its capacity.",
        "'লজিস্টিক বৃদ্ধি' বক্ররেখা কী?", ["প্রথমে দ্রুত, তারপর সর্বোচ্চ ক্ষমতার কাছে গিয়ে সমতল হয়ে যাওয়া বৃদ্ধি", "সরলরৈখিক বৃদ্ধি", "অন্তহীন সূচকীয় বৃদ্ধি", "শূন্যে ক্ষয়"],
        "নতুন সেতুর যান প্রায়ই এমন S-বক্ররেখায় ক্ষমতার দিকে যায়।"),
    mcq("Why do engineers prefer 'well-conditioned' equations in computer analysis?", ["Small rounding errors in the input then cause only small errors in the answer", "They are easier to spell", "They need no computer", "They always give zero"], 0,
        "Ill-conditioned systems, like nearly unstable structures, amplify errors.",
        "কম্পিউটার-বিশ্লেষণে প্রকৌশলীরা 'সুগঠিত' সমীকরণ পছন্দ করেন কেন?", ["ইনপুটের ছোট আসন্ন-ভুলে উত্তরে শুধু ছোট ভুল হয়", "বানান সহজ", "কম্পিউটার লাগে না", "সবসময় শূন্য দেয়"],
        "প্রায়-অস্থির কাঠামোর মতো দুর্গঠিত ব্যবস্থা ভুল বাড়িয়ে দেয়।"),
    mcq("What is the magnitude of the vector (3, 4, 12)?", ["13", "19", "12", "169"], 0,
        "√(9 + 16 + 144) = √169 = 13.",
        "ভেক্টর (3, 4, 12)-এর মান কত?", ["13", "19", "12", "169"],
        "√(9 + 16 + 144) = √169 = 13।"),
    mcq("Why do engineers convert a member's direction into a unit vector before resolving forces?", ["A unit vector has length 1, so multiplying it by the force gives the force's components directly", "It makes the force twice as big", "Unit vectors remove the need for any force", "It changes the member's length"], 0,
        "Divide a direction vector by its magnitude to get one.",
        "বল বিভাজনের আগে প্রকৌশলীরা অংশের দিককে একক ভেক্টরে বদলান কেন?", ["একক ভেক্টরের দৈর্ঘ্য 1, তাই একে বল দিয়ে গুণ করলে সরাসরি বলের উপাংশ মেলে", "এতে বল দ্বিগুণ হয়", "একক ভেক্টরে বলের দরকারই থাকে না", "এতে অংশের দৈর্ঘ্য বদলায়"],
        "দিক-ভেক্টরকে তার মান দিয়ে ভাগ করলেই মেলে।"),
    mcq("A cable force of 26 kN acts along the direction (5, 0, 12). What is its component along the 12 direction?", ["24 kN", "10 kN", "26 kN", "12 kN"], 0,
        "|direction| = 13, so the component = 26 x 12 ÷ 13 = 24 kN.",
        "26 kN-এর একটা তারের বল (5, 0, 12) দিক বরাবর কাজ করে। 12-এর দিকে এর উপাংশ কত?", ["24 kN", "10 kN", "26 kN", "12 kN"],
        "দিকের মান = 13, তাই উপাংশ = 26 x 12 ÷ 13 = 24 kN।"),
    mcq("What does it mean if the determinant of a structure's stiffness matrix is zero?", ["The structure is a mechanism - it can move without resistance and is unstable", "It is extra strong", "It weighs nothing", "It has no loads"], 0,
        "A missing support or member often causes this.",
        "কাঠামোর দৃঢ়তা-ম্যাট্রিক্সের নির্ণায়ক শূন্য হলে মানে কী?", ["কাঠামোটা একটা যন্ত্রকৌশল - বাধা ছাড়াই নড়তে পারে, অস্থির", "অতিরিক্ত শক্ত", "ওজন নেই", "কোনো বোঝা নেই"],
        "কোনো ঠেকনা বা অংশ না থাকলে প্রায়ই এমন হয়।"),
    mcq("What is the derivative of e^(kx)?", ["k e^(kx)", "e^(kx)", "kx e^(kx-1)", "e^k"], 0,
        "This is why exponentials solve dy/dx = ky.",
        "e^(kx)-এর অবকলজ কী?", ["k e^(kx)", "e^(kx)", "kx e^(kx-1)", "e^k"],
        "এই কারণেই সূচকীয় অপেক্ষক dy/dx = ky-এর সমাধান।"),
    mcq("A function has dy/dx = 0 and d²y/dx² > 0 at a point. What is the point?", ["A local minimum", "A local maximum", "A point of inflection always", "Undefined"], 0,
        "A positive second derivative means the curve bends upward there.",
        "একটা অপেক্ষকের কোনো বিন্দুতে dy/dx = 0 আর d²y/dx² > 0। বিন্দুটা কী?", ["স্থানীয় সর্বনিম্ন", "স্থানীয় সর্বোচ্চ", "সবসময় নতি-পরিবর্তন বিন্দু", "অসংজ্ঞাত"],
        "ধনাত্মক দ্বিতীয় অবকলজ মানে বক্ররেখা সেখানে উপরে বাঁকে।"),
) if q is not None)
