"""Class 11 - Math (Senior Engineer): differentiation and stationary points, optimisation,
integration for areas under curves, logarithms and exponentials, permutations and combinations,
binomial coefficients, geometric series, parabolic cable profiles, standard deviation, complex
numbers and limits - the mathematics engineers use to design and check bridges."""
from math import comb, perm
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


def _poly(a, b, c):
    parts = []
    for coef, term in ((a, "x³"), (b, "x²"), (c, "x")):
        if coef:
            mag = "" if abs(coef) == 1 else str(abs(coef))
            parts.append(("- " if coef < 0 else "+ ") + mag + term)
    s = " ".join(parts)
    return s[2:] if s.startswith("+ ") else "-" + s[2:]


def deriv(a, b, c, x0):
    d = 3 * a * x0 * x0 + 2 * b * x0 + c
    return _n(f"If y = {_poly(a, b, c)}, what is dy/dx when x = {x0}?",
              f"y = {_poly(a, b, c)} হলে x = {x0}-এ dy/dx কত?", d,
              f"dy/dx = {3 * a}x² + {2 * b}x + {c}; at x = {x0}: {3 * a * x0 * x0} + {2 * b * x0} + {c} = {d}.",
              f"dy/dx = {3 * a}x² + {2 * b}x + {c}; x = {x0}-এ: {3 * a * x0 * x0} + {2 * b * x0} + {c} = {d}।",
              (a * x0 ** 3 + b * x0 ** 2 + c * x0, a * x0 * x0 + b * x0 + c, d + 3 * a))


def statpt(a, b, c):
    x = _c(-b / (2 * a))
    y = _c(a * x * x + b * x + c)
    kind_en = "minimum" if a > 0 else "maximum"
    kind_bn = "সর্বনিম্ন" if a > 0 else "সর্বোচ্চ"
    sgn = lambda v, t: (f"+ {v}{t}" if v > 0 else f"- {-v}{t}") if v else ""
    lead = "x²" if a == 1 else "-x²" if a == -1 else f"{a}x²"
    expr = f"{lead} {sgn(b, 'x')} {sgn(c, '')}".replace("  ", " ").strip()
    return _n(f"The curve y = {expr} has a stationary point. At what value of x?",
              f"বক্ররেখা y = {expr}-এর একটা স্থির বিন্দু আছে। x-এর কোন মানে?", abs(x) if x != 0 else 0.5,
              f"dy/dx = {2 * a}x {sgn(b, '')} = 0 gives x = {x:g}; it is a {kind_en} with y = {y:g}.",
              f"dy/dx = {2 * a}x {sgn(b, '')} = 0 থেকে x = {x:g}; এটা {kind_bn}, y = {y:g}।",
              (_c(abs(b / a)), abs(c) if abs(c) != abs(x) else abs(x) + 3, _c(abs(x) * 2))) if x > 0 else None


def maxarea(p):
    s = _c(p / 4)
    a = _c(s * s)
    return _n(f"A site compound is fenced with {p} m of fencing in a rectangle. What is the largest area it can enclose?",
              f"একটা নির্মাণস্থলের ঘের {p} m বেড়ায় আয়তাকারে ঘেরা হবে। সবচেয়ে বেশি কত ক্ষেত্রফল ঘেরা যায়?", a,
              f"Area A = x(P/2 - x); dA/dx = 0 gives x = P/4 = {s:g} m, a square: area = {s:g}² = {a:g} m².",
              f"ক্ষেত্রফল A = x(P/2 - x); dA/dx = 0 থেকে x = P/4 = {s:g} m, একটা বর্গ: ক্ষেত্রফল = {s:g}² = {a:g} m²।",
              (_c(p * p / 8), _c(p / 2 * p / 4), _c(a / 2)), " m²")


def integ(k, a):
    r = _c(k * a ** 3 / 3)
    kx = "x²" if k == 1 else f"{k}x²"
    return _n(f"What is the area under the curve y = {kx} between x = 0 and x = {a}?",
              f"x = 0 থেকে x = {a}-এর মধ্যে বক্ররেখা y = {kx}-এর নিচের ক্ষেত্রফল কত?", r,
              f"∫{k}x² dx = {k}x³/3; from 0 to {a}: {k} x {a ** 3} ÷ 3 = {r:g}.",
              f"∫{k}x² dx = {k}x³/3; 0 থেকে {a}: {k} x {a ** 3} ÷ 3 = {r:g}।",
              (k * a * a, _c(k * a ** 3), _c(2 * k * a)))


def logq(base, val, ans):
    o = _o(ans, val // base if val // base != ans else ans + 3, base * ans, ans - 1 if ans > 1 else ans + 4)
    return mcq(f"What is log base {base} of {val:,}?", [str(v) for v in o], 0,
               f"{base}^{ans} = {val:,}, so log_{base}({val:,}) = {ans}.",
               f"{base} ভিত্তিতে {val:,}-এর লগারিদম কত?", [str(v) for v in o],
               f"{base}^{ans} = {val:,}, তাই log_{base}({val:,}) = {ans}।")


def expq(base, val, ans):
    o = _o(ans, val // base, ans * 2, ans + 1)
    return mcq(f"Solve {base}^x = {val:,}.", [f"x = {v}" for v in o], 0,
               f"{base} multiplied by itself {ans} times is {val:,}, so x = {ans}.",
               f"সমাধান করো: {base}^x = {val:,}।", [f"x = {v}" for v in o],
               f"{base}-কে নিজের সঙ্গে {ans} বার গুণ করলে {val:,}, তাই x = {ans}।")


def choose(n, r, what_en, what_bn):
    c = comb(n, r)
    return _n(f"A team of {r} inspectors is chosen from {n} {what_en}. How many different teams are possible? (order does not matter)",
              f"{n} জন {what_bn} থেকে {r} জনের একটা পরিদর্শক-দল বাছা হবে। কত আলাদা দল সম্ভব? (ক্রম গুরুত্বহীন)", c,
              f"ⁿCᵣ = {n}! ÷ ({r}! x {n - r}!) = {c:,}.",
              f"ⁿCᵣ = {n}! ÷ ({r}! x {n - r}!) = {c:,}।",
              (perm(n, r), n * r, c + n))


def arrange(n, r, what_en, what_bn):
    p = perm(n, r)
    return _n(f"{r} different {what_en} are to be placed in order in {r} of {n} numbered bays. How many arrangements are possible? (order matters)",
              f"{r}টি আলাদা {what_bn} {n}টি নম্বর-দেওয়া খোপের {r}টিতে ক্রম মেনে রাখা হবে। কতভাবে সাজানো যায়? (ক্রম গুরুত্বপূর্ণ)", p,
              f"ⁿPᵣ = {n}! ÷ {n - r}! = {p:,}.",
              f"ⁿPᵣ = {n}! ÷ {n - r}! = {p:,}।",
              (comb(n, r), n ** r if n ** r != p else p + n, n * r))


def gsum(a, r, n, what_en, what_bn):
    s = a * (r ** n - 1) // (r - 1)
    return _n(f"{what_en}: {a} in the first week, then {r} times as many each week. What is the total over {n} weeks?",
              f"{what_bn}: প্রথম সপ্তাহে {a}, তারপর প্রতি সপ্তাহে {r} গুণ। {n} সপ্তাহে মোট কত?", s,
              f"Geometric series: S = a(rⁿ - 1) ÷ (r - 1) = {a}({r}^{n} - 1) ÷ {r - 1} = {s:,}.",
              f"গুণোত্তর শ্রেণি: S = a(rⁿ - 1) ÷ (r - 1) = {a}({r}^{n} - 1) ÷ {r - 1} = {s:,}।",
              (a * r ** (n - 1), a * r ** n, a * n * r))


def cable(span, sag):
    a = _c(sag / (span / 2) ** 2)
    return _n(f"A suspension cable spans {span} m and sags {sag} m at the middle. Modelling it as y = ax² with the lowest point at the origin, what is a?",
              f"একটা ঝুলন্ত তার {span} m বিস্তৃত আর মাঝখানে {sag} m ঝুলে আছে। সবচেয়ে নিচু বিন্দু মূলবিন্দুতে ধরে y = ax² মডেলে a কত?", a,
              f"At x = {span // 2} (half the span), y = {sag}: a = {sag} ÷ {span // 2}² = {a:g}.",
              f"x = {span // 2} (অর্ধেক বিস্তার)-এ y = {sag}: a = {sag} ÷ {span // 2}² = {a:g}।",
              (_c(sag / span), _c(sag / span ** 2), _c(a * 2)))


def sd(vals, what_en, what_bn):
    m = sum(vals) / len(vals)
    var = _c(sum((v - m) ** 2 for v in vals) / len(vals))
    s = _c(var ** 0.5)
    return _n(f"{what_en}: {', '.join(map(str, vals))}. What is the standard deviation? (divide by n)",
              f"{what_bn}: {', '.join(map(str, vals))}। প্রমিত বিচ্যুতি কত? (n দিয়ে ভাগ)", s,
              f"Mean = {_c(m):g}; mean of squared deviations = {var:g}; σ = √{var:g} = {s:g}.",
              f"গড় = {_c(m):g}; বিচ্যুতির বর্গের গড় = {var:g}; σ = √{var:g} = {s:g}।",
              (var, max(vals) - min(vals), _c(m)))


def modz(a, b):
    r = _c((a * a + b * b) ** 0.5)
    return _n(f"What is the modulus of the complex number {a} + {b}i?",
              f"জটিল সংখ্যা {a} + {b}i-এর মডিউলাস কত?", r,
              f"|z| = √({a}² + {b}²) = √{a * a + b * b} = {r:g}.",
              f"|z| = √({a}² + {b}²) = √{a * a + b * b} = {r:g}।",
              (a + b, a * a + b * b, abs(a - b) if a != b else r + 1))


ITEMS = tuple(q for q in (
    deriv(1, 0, 0, 2), deriv(2, -3, 4, 1), deriv(0, 5, -2, 3), deriv(1, 2, 1, 2), deriv(0, 3, 6, 4),
    statpt(1, -6, 10), statpt(2, -8, 3), statpt(-1, 10, 5), statpt(3, -24, 2),
    maxarea(40), maxarea(100), maxarea(64), maxarea(200),
    integ(3, 2), integ(6, 3), integ(1, 6), integ(9, 2),
    logq(10, 1000, 3), logq(2, 32, 5), logq(10, 100000, 5), logq(3, 81, 4),
    expq(2, 64, 6), expq(3, 243, 5), expq(5, 125, 3), expq(10, 10000, 4),
    choose(6, 2, "engineers", "প্রকৌশলী"), choose(8, 3, "engineers", "প্রকৌশলী"), choose(10, 4, "technicians", "প্রযুক্তিবিদ"),
    arrange(5, 3, "girders", "গার্ডার"), arrange(6, 2, "crane jobs", "ক্রেন-কাজ"), arrange(7, 3, "test cubes", "পরীক্ষা-ঘনক"),
    gsum(2, 3, 4, "Defects found by a new sensor", "নতুন সেন্সরে পাওয়া ত্রুটি"), gsum(5, 2, 6, "Downloads of a bridge-inspection app", "সেতু-পরিদর্শন অ্যাপের ডাউনলোড"),
    gsum(1, 4, 4, "Cracks mapped by drone", "ড্রোনে মানচিত্রিত ফাটল"),
    cable(200, 20), cable(100, 10), cable(400, 40), cable(60, 9),
    sd([2, 4, 4, 4, 5, 5, 7, 9], "Daily delays (minutes)", "দৈনিক দেরি (মিনিট)"), sd([10, 12, 14, 16, 18], "Cube strengths (N/mm² above 30)", "ঘনকের শক্তি (30-এর উপরে N/mm²)"),
    sd([5, 5, 5, 5], "Bolt torques (units)", "বল্টুর টর্ক (একক)") if False else None,
    modz(3, 4), modz(5, 12), modz(8, 6), modz(7, 24), modz(9, 12),
    deriv(2, 0, -5, 3), statpt(1, -14, 40), maxarea(120), integ(2, 3), choose(12, 2, "welders", "ঝালাইকার"),
    arrange(8, 2, "inspection visits", "পরিদর্শন-সফর"), gsum(3, 2, 5, "Sensor alerts", "সেন্সরের সতর্কবার্তা"),
    sd([20, 24, 28, 32, 36], "Hourly truck counts", "ঘণ্টায় ট্রাকের সংখ্যা"),
    mcq("What does dy/dx represent?", ["The rate of change of y with respect to x - the gradient of the curve", "The area under the curve", "The value of y when x = 0", "The average of x and y"], 0,
        "Engineers use it to find slopes of curves, rates and maximum values.",
        "dy/dx কী বোঝায়?", ["x-এর সাপেক্ষে y-এর পরিবর্তনের হার - বক্ররেখার ঢাল", "বক্ররেখার নিচের ক্ষেত্রফল", "x = 0-তে y-এর মান", "x আর y-এর গড়"],
        "প্রকৌশলীরা বক্ররেখার ঢাল, হার আর সর্বোচ্চ মান বের করতে এটা ব্যবহার করেন।"),
    mcq("What is the derivative of xⁿ?", ["nxⁿ⁻¹", "xⁿ⁺¹ ÷ (n + 1)", "nxⁿ", "xⁿ⁻¹"], 0,
        "Bring the power down and reduce it by one.",
        "xⁿ-এর অবকলজ কী?", ["nxⁿ⁻¹", "xⁿ⁺¹ ÷ (n + 1)", "nxⁿ", "xⁿ⁻¹"],
        "ঘাতকে নামিয়ে আনো আর ঘাত এক কমাও।"),
    mcq("How do you find a stationary point on a curve?", ["Set dy/dx = 0 and solve for x", "Set y = 0", "Set x = 0", "Find the area"], 0,
        "At a stationary point the tangent is horizontal.",
        "বক্ররেখার স্থির বিন্দু কীভাবে বের করো?", ["dy/dx = 0 ধরে x-এর সমাধান করো", "y = 0 ধরো", "x = 0 ধরো", "ক্ষেত্রফল বের করো"],
        "স্থির বিন্দুতে স্পর্শক অনুভূমিক।"),
    mcq("How can you tell whether a stationary point is a maximum or a minimum?", ["Check the second derivative: negative means maximum, positive means minimum", "Look at the colour of the graph", "It is always a maximum", "Check the y-intercept"], 0,
        "d²y/dx² shows whether the gradient is increasing or decreasing.",
        "স্থির বিন্দু সর্বোচ্চ না সর্বনিম্ন কীভাবে বোঝা যায়?", ["দ্বিতীয় অবকলজ দেখো: ঋণাত্মক মানে সর্বোচ্চ, ধনাত্মক মানে সর্বনিম্ন", "লেখচিত্রের রং দেখো", "সবসময় সর্বোচ্চ", "y-ছেদক দেখো"],
        "d²y/dx² দেখায় ঢাল বাড়ছে না কমছে।"),
    mcq("A beam's deflection is y(x). Where is the deflection greatest?", ["Where dy/dx = 0 - the slope of the deflected shape is zero", "Always at the supports", "Where y = 0", "Nowhere"], 0,
        "For a symmetric simply supported beam, that is mid-span.",
        "একটা কড়ির বিক্ষেপ y(x)। বিক্ষেপ কোথায় সবচেয়ে বেশি?", ["যেখানে dy/dx = 0 - বাঁকা আকারের ঢাল শূন্য", "সবসময় ঠেকনায়", "যেখানে y = 0", "কোথাও না"],
        "প্রতিসম সরল-ঠেকনার কড়িতে সেটা মাঝ-স্প্যান।"),
    mcq("What does integration find?", ["The area under a curve, or the total from a rate of change", "The gradient", "The maximum point", "The intercept"], 0,
        "Integration is the reverse of differentiation.",
        "সমাকলন কী বের করে?", ["বক্ররেখার নিচের ক্ষেত্রফল, বা পরিবর্তনের হার থেকে মোট", "ঢাল", "সর্বোচ্চ বিন্দু", "ছেদক"],
        "সমাকলন হলো অবকলনের উল্টো।"),
    mcq("What is ∫xⁿ dx (for n ≠ -1)?", ["xⁿ⁺¹ ÷ (n + 1) + c", "nxⁿ⁻¹", "xⁿ + c", "(n + 1)xⁿ"], 0,
        "Add one to the power and divide by the new power; add a constant.",
        "∫xⁿ dx (n ≠ -1-এর জন্য) কী?", ["xⁿ⁺¹ ÷ (n + 1) + c", "nxⁿ⁻¹", "xⁿ + c", "(n + 1)xⁿ"],
        "ঘাতে এক যোগ করে নতুন ঘাত দিয়ে ভাগ করো; একটা ধ্রুবক যোগ করো।"),
    mcq("If a crane's speed is v(t), what does the area under the v-t graph between two times give?", ["The distance moved in that time", "The acceleration", "The force", "The power"], 0,
        "Integrating speed over time gives distance.",
        "ক্রেনের বেগ v(t) হলে দুই সময়ের মধ্যে v-t লেখচিত্রের নিচের ক্ষেত্রফল কী দেয়?", ["সেই সময়ে সরে যাওয়া দূরত্ব", "ত্বরণ", "বল", "ক্ষমতা"],
        "সময় ধরে বেগের সমাকলন দূরত্ব দেয়।"),
    mcq("What is a 'limit' as x tends to a value?", ["The value a function gets closer and closer to as x approaches that value", "The largest x allowed", "A speed limit", "The value at x = 0 always"], 0,
        "Derivatives are defined using limits of tiny changes.",
        "x কোনো মানের দিকে গেলে 'সীমা' কী?", ["x সেই মানের কাছে গেলে অপেক্ষক যে মানের ক্রমশ কাছে যায়", "অনুমোদিত সবচেয়ে বড় x", "গতিসীমা", "সবসময় x = 0-এর মান"],
        "অবকলজের সংজ্ঞা খুদে বদলের সীমা দিয়ে।"),
    mcq("Given log 2 ≈ 0.301 and log 3 ≈ 0.477, what is log 6?", ["0.778", "0.144", "0.176", "1.431"], 0,
        "log 6 = log(2 x 3) = log 2 + log 3 = 0.778 - logs turn multiplication into addition.",
        "log 2 ≈ 0.301 আর log 3 ≈ 0.477 হলে log 6 কত?", ["0.778", "0.144", "0.176", "1.431"],
        "log 6 = log(2 x 3) = log 2 + log 3 = 0.778 - লগারিদম গুণকে যোগে বদলায়।"),
    mcq("Given log 2 ≈ 0.301, what is log 8?", ["0.903", "2.408", "0.602", "0.090"], 0,
        "log 8 = log 2³ = 3 log 2 = 0.903.",
        "log 2 ≈ 0.301 হলে log 8 কত?", ["0.903", "2.408", "0.602", "0.090"],
        "log 8 = log 2³ = 3 log 2 = 0.903 - ঘাত সামনে গুণক হয়ে আসে।"),
    mcq("Why are decibels (dB) a logarithmic scale?", ["Sound intensities range over many powers of ten, and logs compress them into a usable scale", "Logs make sounds louder", "dB are not logarithmic", "To confuse workers"], 0,
        "+10 dB means ten times the intensity.",
        "ডেসিবেল (dB) লগারিদমিক মাপকাঠি কেন?", ["শব্দের তীব্রতা দশের অনেক ঘাত জুড়ে ছড়ানো, আর লগ তাদের ব্যবহারযোগ্য মাপকাঠিতে গুটিয়ে আনে", "লগ শব্দ জোরালো করে", "dB লগারিদমিক নয়", "কর্মীদের গুলিয়ে দিতে"],
        "+10 dB মানে দশগুণ তীব্রতা।"),
    mcq("What is the number e (about 2.718) important for?", ["Continuous growth and decay, such as compound interest compounded continuously or cooling", "Counting bridges", "Measuring angles", "Writing names"], 0,
        "eˣ is the only function equal to its own derivative.",
        "সংখ্যা e (প্রায় 2.718) কীসের জন্য জরুরি?", ["অবিরাম বৃদ্ধি আর ক্ষয়, যেমন অবিরাম চক্রবৃদ্ধি সুদ বা ঠান্ডা হওয়া", "সেতু গোনা", "কোণ মাপা", "নাম লেখা"],
        "eˣ একমাত্র অপেক্ষক যা নিজের অবকলজের সমান।"),
    mcq("What is the difference between a permutation and a combination?", ["In a permutation order matters; in a combination it does not", "They are the same", "Combinations always give more", "Permutations ignore order"], 0,
        "Choosing a team is a combination; ranking winners is a permutation.",
        "বিন্যাস (পারমুটেশন) আর সমবায় (কম্বিনেশন)-এর পার্থক্য কী?", ["বিন্যাসে ক্রম গুরুত্বপূর্ণ; সমবায়ে নয়", "দুটো একই", "সমবায় সবসময় বেশি দেয়", "বিন্যাস ক্রম উপেক্ষা করে"],
        "দল বাছাই সমবায়; বিজয়ীদের ক্রম সাজানো বিন্যাস।"),
    mcq("What is 5! (5 factorial)?", ["120", "25", "15", "60"], 0,
        "5 x 4 x 3 x 2 x 1 = 120.",
        "5! (5 ফ্যাক্টোরিয়াল) কত?", ["120", "25", "15", "60"],
        "5 x 4 x 3 x 2 x 1 = 120।"),
    mcq("A 4-digit site padlock code uses digits 0-9 with repeats allowed. How many codes are possible?", ["10,000", "5,040", "40", "9,999"], 0,
        "10 x 10 x 10 x 10 = 10,000.",
        "নির্মাণস্থলের একটা 4-অঙ্কের তালার সংকেতে 0-9 অঙ্ক, পুনরাবৃত্তি চলে। কতগুলো সংকেত সম্ভব?", ["10,000", "5,040", "40", "9,999"],
        "10 x 10 x 10 x 10 = 10,000।"),
    mcq("What is the binomial expansion of (1 + x)² ?", ["1 + 2x + x²", "1 + x²", "1 + x + x²", "2 + 2x"], 0,
        "The coefficients 1, 2, 1 come from Pascal's triangle.",
        "(1 + x)²-এর দ্বিপদ বিস্তৃতি কী?", ["1 + 2x + x²", "1 + x²", "1 + x + x²", "2 + 2x"],
        "সহগ 1, 2, 1 প্যাসকেলের ত্রিভুজ থেকে আসে।"),
    mcq("For small x, (1 + x)ⁿ ≈ 1 + nx. Roughly what is 1.02¹⁰?", ["About 1.2", "About 1.02", "About 2", "About 10"], 0,
        "1 + 10 x 0.02 = 1.2 (the exact value is about 1.219).",
        "ছোট x-এর জন্য (1 + x)ⁿ ≈ 1 + nx। 1.02¹⁰ মোটামুটি কত?", ["প্রায় 1.2", "প্রায় 1.02", "প্রায় 2", "প্রায় 10"],
        "1 + 10 x 0.02 = 1.2 (আসল মান প্রায় 1.219)।"),
    mcq("What is the sum to infinity of a geometric series with first term a and ratio r (|r| < 1)?", ["a ÷ (1 - r)", "a x r", "a ÷ r", "Infinite always"], 0,
        "1 + ½ + ¼ + … adds up to 2.",
        "প্রথম পদ a আর অনুপাত r (|r| < 1) গুণোত্তর শ্রেণির অসীম পর্যন্ত যোগফল কত?", ["a ÷ (1 - r)", "a x r", "a ÷ r", "সবসময় অসীম"],
        "1 + ½ + ¼ + … যোগ হয়ে 2।"),
    mcq("A bouncing tool rises 50% as high on each bounce, starting at 4 m. What total height does it rise on all the bounces after the first drop?", ["4 m", "8 m", "2 m", "Infinite"], 0,
        "Rises: 2 + 1 + 0.5 + … = 2 ÷ (1 - 0.5) = 4 m.",
        "একটা লাফানো যন্ত্র প্রতি লাফে আগের অর্ধেক উচ্চতায় ওঠে, শুরু 4 m থেকে। প্রথম পতনের পরের সব লাফে মোট কত উঁচুতে ওঠে?", ["4 m", "8 m", "2 m", "অসীম"],
        "ওঠা: 2 + 1 + 0.5 + … = 2 ÷ (1 - 0.5) = 4 m।"),
    mcq("What shape does a uniformly loaded suspension cable take?", ["A parabola", "A circle", "A straight line", "A zig-zag"], 0,
        "A cable hanging under its own weight alone forms a slightly different curve - a catenary.",
        "সমভাবে বোঝাই ঝুলন্ত তার কোন আকার নেয়?", ["অধিবৃত্ত", "বৃত্ত", "সরলরেখা", "আঁকাবাঁকা রেখা"],
        "শুধু নিজের ওজনে ঝোলা তার একটু আলাদা বক্ররেখা - ক্যাটেনারি - তৈরি করে।"),
    mcq("What is a 'catenary'?", ["The curve a flexible chain or cable makes hanging under its own weight", "A type of arch made of brick", "A train", "A circle"], 0,
        "Turned upside down, a catenary is the ideal shape for a pure-compression arch.",
        "'ক্যাটেনারি' কী?", ["নমনীয় শিকল বা তার নিজের ওজনে ঝুললে যে বক্ররেখা হয়", "ইটের এক রকম খিলান", "একটা ট্রেন", "একটা বৃত্ত"],
        "উল্টে দিলে ক্যাটেনারি খাঁটি সংনমনের খিলানের আদর্শ আকার।"),
    mcq("What is an ellipse used for in bridge design?", ["Some arch shapes, giving a flatter crown and more headroom near the springing", "Measuring traffic", "Writing equations only", "Drawing circles"], 0,
        "Elliptical arches suit wide, low openings.",
        "সেতুর নকশায় উপবৃত্ত কীসের জন্য ব্যবহার হয়?", ["কিছু খিলানের আকার, মাথা চ্যাপ্টা আর পাদদেশের কাছে বেশি ফাঁক দেয়", "যানবাহন মাপা", "শুধু সমীকরণ লেখা", "বৃত্ত আঁকা"],
        "উপবৃত্তাকার খিলান চওড়া, নিচু ফাঁকের জন্য মানানসই।"),
    mcq("What does standard deviation measure?", ["How spread out the data are around the mean", "The middle value", "The most common value", "The total"], 0,
        "Concrete suppliers with a smaller standard deviation are more consistent.",
        "প্রমিত বিচ্যুতি কী মাপে?", ["তথ্য গড়ের চারপাশে কতটা ছড়ানো", "মাঝের মান", "সবচেয়ে সাধারণ মান", "যোগফল"],
        "যে কংক্রিট-সরবরাহকারীর প্রমিত বিচ্যুতি কম, তারা বেশি স্থির মানের।"),
    mcq("Why do concrete specifications use a 'characteristic strength' below the mean test strength?", ["To make sure only a small percentage (often 5%) of results fall below it", "To make concrete weaker", "Because tests always lie", "It is the same as the mean"], 0,
        "Target mean = characteristic strength + about 1.64 standard deviations.",
        "কংক্রিটের নির্দেশিকায় গড় পরীক্ষা-শক্তির নিচে 'বৈশিষ্ট্যসূচক শক্তি' ব্যবহার হয় কেন?", ["নিশ্চিত করতে যে মাত্র ছোট শতাংশ (প্রায়ই 5%) ফল এর নিচে পড়ে", "কংক্রিট দুর্বল করতে", "কারণ পরীক্ষা সবসময় মিথ্যা বলে", "এটা গড়ের সমান"],
        "লক্ষ্য-গড় = বৈশিষ্ট্যসূচক শক্তি + প্রায় 1.64 প্রমিত বিচ্যুতি।"),
    mcq("What is the 'normal distribution'?", ["A symmetric bell-shaped spread of data around the mean", "A list of normal people", "A straight line", "A type of bar chart only"], 0,
        "About 95% of values lie within 2 standard deviations of the mean.",
        "'স্বাভাবিক বণ্টন' কী?", ["গড়ের চারপাশে প্রতিসম ঘণ্টা-আকারের তথ্য-বিস্তার", "স্বাভাবিক মানুষের তালিকা", "একটা সরলরেখা", "শুধু এক রকম বার-চার্ট"],
        "প্রায় 95% মান গড়ের 2 প্রমিত বিচ্যুতির মধ্যে থাকে।"),
    mcq("What is i in complex numbers?", ["The square root of -1", "The number 1", "Infinity", "The letter for current only"], 0,
        "Electrical engineers often write j instead of i.",
        "জটিল সংখ্যায় i কী?", ["-1-এর বর্গমূল", "সংখ্যা 1", "অসীম", "শুধু প্রবাহের অক্ষর"],
        "বৈদ্যুতিক প্রকৌশলীরা প্রায়ই i-এর বদলে j লেখেন।"),
    mcq("What is i²?", ["-1", "1", "i", "0"], 0,
        "By definition, i x i = -1.",
        "i² কত?", ["-1", "1", "i", "0"],
        "সংজ্ঞা অনুযায়ী i x i = -1।"),
    mcq("Where are complex numbers used in engineering?", ["Analysing AC circuits and vibrations, where quantities have both size and phase", "Counting bolts", "Measuring length with a tape", "They have no use"], 0,
        "They make oscillation maths much simpler.",
        "প্রকৌশলে জটিল সংখ্যা কোথায় ব্যবহার হয়?", ["এসি বর্তনী আর কম্পন বিশ্লেষণে, যেখানে রাশির মান আর দশা দুটোই থাকে", "বল্টু গোনা", "ফিতে দিয়ে দৈর্ঘ্য মাপা", "কোনো ব্যবহার নেই"],
        "দোলনের অঙ্ক অনেক সহজ করে।"),
    mcq("What is (2 + 3i) + (4 - i)?", ["6 + 2i", "8 + 3i", "6 + 4i", "2 + 2i"], 0,
        "Add real parts and imaginary parts separately.",
        "(2 + 3i) + (4 - i) কত?", ["6 + 2i", "8 + 3i", "6 + 4i", "2 + 2i"],
        "বাস্তব অংশ আর কাল্পনিক অংশ আলাদা করে যোগ করো।"),
    mcq("What is a 'set' in mathematics?", ["A well-defined collection of distinct objects", "A group of tools", "A TV", "A number line"], 0,
        "For example, the set of prime numbers below 10 is {2, 3, 5, 7}.",
        "গণিতে 'সেট' কী?", ["সুনির্দিষ্ট আলাদা আলাদা বস্তুর সংগ্রহ", "এক দল যন্ত্র", "একটা টিভি", "একটা সংখ্যারেখা"],
        "যেমন 10-এর নিচের মৌলিক সংখ্যার সেট {2, 3, 5, 7}।"),
    mcq("If A = {1, 2, 3} and B = {2, 3, 4}, what is A ∩ B?", ["{2, 3}", "{1, 2, 3, 4}", "{1, 4}", "{}"], 0,
        "The intersection holds elements in both sets.",
        "A = {1, 2, 3} আর B = {2, 3, 4} হলে A ∩ B কী?", ["{2, 3}", "{1, 2, 3, 4}", "{1, 4}", "{}"],
        "ছেদ-সেটে দুটো সেটেরই উপাদান থাকে।"),
    mcq("What is a 'function' in terms of mapping?", ["A rule that gives exactly one output for each input in its domain", "A rule that gives many outputs for one input", "A random list", "A graph that is always straight"], 0,
        "y = x² is a function; x = y² is not (one x gives two y).",
        "মানচিত্রণের দিক থেকে 'অপেক্ষক' কী?", ["যে নিয়ম ডোমেনের প্রতিটা ইনপুটে ঠিক একটা আউটপুট দেয়", "যে নিয়ম একটা ইনপুটে অনেক আউটপুট দেয়", "এলোমেলো তালিকা", "সবসময় সোজা লেখচিত্র"],
        "y = x² অপেক্ষক; x = y² নয় (একটা x দুটো y দেয়)।"),
    mcq("In radians, what is 180°?", ["π", "2π", "π/2", "1"], 0,
        "Radians are the natural unit for angles in calculus.",
        "রেডিয়ানে 180° কত?", ["π", "2π", "π/2", "1"],
        "ক্যালকুলাসে কোণের স্বাভাবিক একক রেডিয়ান।"),
    mcq("What is the arc length of a curve of radius r through an angle θ in radians?", ["rθ", "r ÷ θ", "θ ÷ r", "r²θ"], 0,
        "A 50 m radius curve through 0.5 rad is 25 m long.",
        "r ব্যাসার্ধ আর রেডিয়ানে θ কোণের বক্ররেখার চাপের দৈর্ঘ্য কত?", ["rθ", "r ÷ θ", "θ ÷ r", "r²θ"],
        "50 m ব্যাসার্ধের বাঁক 0.5 রেডিয়ানে 25 m লম্বা।"),
    mcq("What is the period of y = sin(2x)?", ["π (180°)", "2π (360°)", "π/2 (90°)", "4π"], 0,
        "The 2 squeezes the graph horizontally by half.",
        "y = sin(2x)-এর পর্যায় কত?", ["π (180°)", "2π (360°)", "π/2 (90°)", "4π"],
        "2 লেখচিত্রকে অনুভূমিকভাবে অর্ধেক চেপে দেয়।"),
    mcq("What is the equation of a straight line with gradient m through the point (x₁, y₁)?", ["y - y₁ = m(x - x₁)", "y = mx₁", "x = my", "y = m + x₁"], 0,
        "Useful for setting out a road alignment from a known point.",
        "(x₁, y₁) বিন্দু দিয়ে যাওয়া m ঢালের সরলরেখার সমীকরণ কী?", ["y - y₁ = m(x - x₁)", "y = mx₁", "x = my", "y = m + x₁"],
        "জানা বিন্দু থেকে রাস্তার সারিবদ্ধতা চিহ্নিত করতে কাজের।"),
    mcq("What is the perpendicular distance idea used for in surveying?", ["Finding the shortest distance from a point to a line, such as from a pier to a road centreline", "Measuring height only", "Counting traffic", "Measuring temperature"], 0,
        "The shortest path to a line meets it at a right angle.",
        "জরিপে লম্ব-দূরত্বের ভাবনা কীসের জন্য ব্যবহার হয়?", ["একটা বিন্দু থেকে রেখার সবচেয়ে কম দূরত্ব বের করতে, যেমন স্তম্ভ থেকে রাস্তার মধ্যরেখা", "শুধু উচ্চতা মাপা", "যান গোনা", "তাপমাত্রা মাপা"],
        "রেখার দিকে সবচেয়ে ছোট পথ সমকোণে মেশে।"),
    mcq("What is 'mathematical modelling' in engineering?", ["Describing a real situation with equations, then testing and improving them against real data", "Building a plastic model only", "Drawing pictures", "Guessing"], 0,
        "All models simplify reality - engineers check their assumptions.",
        "প্রকৌশলে 'গাণিতিক মডেল-নির্মাণ' কী?", ["সমীকরণ দিয়ে বাস্তব পরিস্থিতি বর্ণনা করা, তারপর আসল তথ্যের সঙ্গে যাচাই আর উন্নত করা", "শুধু প্লাস্টিকের মডেল বানানো", "ছবি আঁকা", "আন্দাজ"],
        "সব মডেল বাস্তবকে সরল করে - প্রকৌশলীরা অনুমান যাচাই করেন।"),
    mcq("What is 'numerical integration' used for when no formula exists?", ["Estimating areas or totals from measured data, for example with the trapezium or Simpson's rule", "Counting integers", "Drawing bar charts", "Finding derivatives only"], 0,
        "River flows and earthwork volumes are often found this way.",
        "সূত্র না থাকলে 'সাংখ্যিক সমাকলন' কীসের জন্য ব্যবহার হয়?", ["মাপা তথ্য থেকে ক্ষেত্রফল বা মোট আন্দাজ, যেমন ট্রাপিজিয়াম বা সিম্পসনের নিয়মে", "পূর্ণসংখ্যা গোনা", "বার-চার্ট আঁকা", "শুধু অবকলজ বের করা"],
        "নদীর প্রবাহ আর মাটি-কাটার আয়তন প্রায়ই এভাবে বের হয়।"),
    mcq("What is a 'matrix' used for in structural analysis?", ["Organising many simultaneous equations so computers can solve for forces and displacements", "Drawing the bridge", "Mixing concrete", "A film"], 0,
        "The stiffness method builds a large matrix for the whole structure.",
        "কাঠামো-বিশ্লেষণে 'ম্যাট্রিক্স' কীসের জন্য ব্যবহার হয়?", ["অনেক যুগপৎ সমীকরণ সাজাতে, যাতে কম্পিউটার বল আর সরণের সমাধান করতে পারে", "সেতু আঁকা", "কংক্রিট মেশানো", "একটা সিনেমা"],
        "দৃঢ়তা-পদ্ধতি পুরো কাঠামোর জন্য একটা বড় ম্যাট্রিক্স গড়ে।"),
    mcq("What is the 'mean' of a probability distribution also called?", ["The expected value", "The mode", "The range", "The variance"], 0,
        "It is the long-run average outcome.",
        "সম্ভাবনা-বণ্টনের 'গড়'-কে আর কী বলে?", ["প্রত্যাশিত মান", "ভূয়িষ্ঠক", "পরিসর", "ভেদাঙ্ক"],
        "দীর্ঘমেয়াদে গড় ফল।"),
    mcq("A test of 10 welds each has a 10% chance of a defect, independently. What is the expected number of defective welds?", ["1", "10", "0.1", "5"], 0,
        "Expected value = n x p = 10 x 0.1 = 1.",
        "10টি ঝালাইয়ের প্রত্যেকটায় স্বাধীনভাবে 10% ত্রুটির সম্ভাবনা। ত্রুটিপূর্ণ ঝালাইয়ের প্রত্যাশিত সংখ্যা কত?", ["1", "10", "0.1", "5"],
        "প্রত্যাশিত মান = n x p = 10 x 0.1 = 1।"),
    mcq("What is the probability that none of 3 independent welds is defective if each has a 10% defect chance?", ["0.729", "0.7", "0.001", "0.3"], 0,
        "0.9 x 0.9 x 0.9 = 0.729.",
        "প্রত্যেকটায় 10% ত্রুটির সম্ভাবনা থাকলে 3টি স্বাধীন ঝালাইয়ের একটাও ত্রুটিপূর্ণ না হওয়ার সম্ভাবনা কত?", ["0.729", "0.7", "0.001", "0.3"],
        "0.9 x 0.9 x 0.9 = 0.729।"),
    mcq("What is the 'binomial distribution' used for?", ["The number of successes in a fixed number of independent trials with the same probability", "Measuring lengths", "Continuous data like heights only", "Drawing circles"], 0,
        "Counting defective bolts in a batch sample fits this model.",
        "'দ্বিপদ বণ্টন' কীসের জন্য ব্যবহার হয়?", ["একই সম্ভাবনার নির্দিষ্ট সংখ্যক স্বাধীন চেষ্টায় সাফল্যের সংখ্যা", "দৈর্ঘ্য মাপা", "শুধু উচ্চতার মতো নিরবচ্ছিন্ন তথ্য", "বৃত্ত আঁকা"],
        "একটা ব্যাচের নমুনায় ত্রুটিপূর্ণ বল্টু গোনা এই মডেলে মেলে।"),
    mcq("What does a 'scatter graph' with points close to a rising line suggest?", ["A strong positive correlation between the two variables", "No relationship", "A negative correlation", "That one causes the other for certain"], 0,
        "Correlation does not prove causation.",
        "একটা বিক্ষেপ-লেখচিত্রে বিন্দুগুলো ঊর্ধ্বমুখী রেখার কাছাকাছি থাকলে কী বোঝা যায়?", ["দুই চলরাশির মধ্যে জোরালো ধনাত্মক সহসম্পর্ক", "কোনো সম্পর্ক নেই", "ঋণাত্মক সহসম্পর্ক", "নিশ্চিতভাবে একটা অন্যটা ঘটায়"],
        "সহসম্পর্ক কার্যকারণ প্রমাণ করে না।"),
    mcq("Why must engineers be careful extrapolating a trend line far beyond the data?", ["The relationship may change outside the measured range", "Lines always continue forever", "Extrapolation is always exact", "Data never ends"], 0,
        "A material may behave linearly only up to its yield point.",
        "প্রকৌশলীদের তথ্যের অনেক বাইরে প্রবণতা-রেখা টেনে বাড়ানোয় সাবধান হতে হয় কেন?", ["মাপা পরিসরের বাইরে সম্পর্ক বদলাতে পারে", "রেখা সবসময় চিরকাল চলে", "বহির্বেশন সবসময় নিখুঁত", "তথ্য কখনো শেষ হয় না"],
        "একটা উপাদান শুধু নতি-বিন্দু পর্যন্ত সরলরৈখিক আচরণ করতে পারে।"),
) if q is not None)
