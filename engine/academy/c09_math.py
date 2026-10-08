"""Class 9 - Math (Bridge Engineer cadet): the sine and cosine rules for truss triangles, area
= ½ab sin C, the quadratic formula, completing the square, similar solids (volume scale factor),
the trapezium rule for areas under curves, composite functions, y ∝ x², rationalising surds,
conditional probability, graph transformations and simple proof - all with bridge examples."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r + 2, r * 2, r + 10):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + ub for x in o], ex_bn)


def _same(q_en, q_bn, opts, ex_en, ex_bn):
    return mcq(q_en, opts, 0, ex_en, q_bn, opts, ex_bn)


def sine_rule(b, A, sA, B, sB):
    a = _c(b * sA / sB)
    return _n(f"In a truss triangle, side b = {b} m is opposite angle B = {B}°, and angle A = {A}°. How long is side a? (sin {A}° = {sA:g}, sin {B}° = {sB:g})",
              f"একটা ট্রাস-ত্রিভুজে বাহু b = {b} m কোণ B = {B}°-এর বিপরীতে, আর কোণ A = {A}°। বাহু a কত লম্বা? (sin {A}° = {sA:g}, sin {B}° = {sB:g})", a,
              f"Sine rule: a ÷ sin A = b ÷ sin B, so a = {b} x {sA:g} ÷ {sB:g} = {a:g} m.",
              f"সাইন-সূত্র: a ÷ sin A = b ÷ sin B, তাই a = {b} x {sA:g} ÷ {sB:g} = {a:g} m।",
              (_c(b * sB / sA), _c(b * sA), _c(a + 2)), " m")


def cos_rule(a, b, C, cC):
    c2 = a * a + b * b - 2 * a * b * cC
    c = _c(c2 ** 0.5)
    return _n(f"Two members of a truss are {a} m and {b} m long with an angle of {C}° between them. How long is the third side? (cos {C}° = {cC:g})",
              f"একটা ট্রাসের দুটো অংশ {a} m আর {b} m লম্বা, মাঝে {C}° কোণ। তৃতীয় বাহু কত লম্বা? (cos {C}° = {cC:g})", c,
              f"Cosine rule: c² = {a}² + {b}² - 2 x {a} x {b} x {cC:g} = {_c(c2):g}, so c = {c:g} m.",
              f"কোসাইন-সূত্র: c² = {a}² + {b}² - 2 x {a} x {b} x {cC:g} = {_c(c2):g}, তাই c = {c:g} m।",
              (a + b, _c((a * a + b * b) ** 0.5) if _c((a * a + b * b) ** 0.5) != c else c + 3, _c(c2)), " m")


def area_sin(a, b, C, sC, what_en, what_bn):
    r = _c(0.5 * a * b * sC)
    return _n(f"{what_en} is a triangle with sides {a} m and {b} m and an included angle of {C}°. What is its area? (sin {C}° = {sC:g})",
              f"{what_bn} একটা ত্রিভুজ, বাহু {a} m আর {b} m, অন্তর্ভুক্ত কোণ {C}°। ক্ষেত্রফল কত? (sin {C}° = {sC:g})", r,
              f"Area = ½ab sin C = ½ x {a} x {b} x {sC:g} = {r:g} m².",
              f"ক্ষেত্রফল = ½ab sin C = ½ x {a} x {b} x {sC:g} = {r:g} m²।",
              (a * b, _c(0.5 * a * b), _c(a * b * sC)), " m²")


def qformula(a, b, c):
    d = b * b - 4 * a * c
    sq = int(round(d ** 0.5))
    r1, r2 = _c((-b + sq) / (2 * a)), _c((-b - sq) / (2 * a))
    eq = f"{a if a != 1 else ''}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0"
    pair = lambda p, q: f"x = {p:g} or x = {q:g}"
    opts = [pair(r1, r2), pair(-r1, -r2), pair(_c((-b + sq) / a), _c((-b - sq) / a)), pair(_c(b + sq), _c(b - sq))]
    seen = []
    for o in opts:
        if o not in seen:
            seen.append(o)
    while len(seen) < 4:
        seen.append(pair(r1 + len(seen), r2))
    return mcq(f"Use the quadratic formula to solve {eq}.", seen, 0,
               f"b² - 4ac = {b * b} - {4 * a * c} = {d}, √{d} = {sq}; x = ({-b} ± {sq}) ÷ {2 * a}, so x = {r1:g} or {r2:g}.",
               f"দ্বিঘাত সূত্র দিয়ে সমাধান করো: {eq}।", [o.replace(' or ', ' বা ') for o in seen],
               f"b² - 4ac = {b * b} - {4 * a * c} = {d}, √{d} = {sq}; x = ({-b} ± {sq}) ÷ {2 * a}, তাই x = {r1:g} বা {r2:g}।")


def csq(p, q):
    h = p // 2
    k = q - h * h
    sgn = lambda v: f"+ {v}" if v >= 0 else f"- {-v}"
    right = f"(x {sgn(h)})² {sgn(k)}"
    opts = [right, f"(x {sgn(h)})² {sgn(q)}", f"(x {sgn(p)})² {sgn(k)}", f"(x {sgn(-h)})² {sgn(k)}"]
    return _same(f"Write x² {sgn(p)}x {sgn(q)} in completed-square form.", f"x² {sgn(p)}x {sgn(q)}-কে পূর্ণবর্গ আকারে লেখো।", opts,
                 f"Halve the x-coefficient: (x {sgn(h)})² = x² {sgn(p)}x + {h * h}; then {q} - {h * h} = {k}. Answer: {right}. The turning point is ({-h}, {k}).",
                 f"x-এর সহগ অর্ধেক করো: (x {sgn(h)})² = x² {sgn(p)}x + {h * h}; তারপর {q} - {h * h} = {k}। উত্তর: {right}। বাঁক-বিন্দু ({-h}, {k})।")


def simvol(k, vol, what_en, what_bn):
    r = vol * k ** 3
    return _n(f"A {what_en} model has a volume of {vol:,} cm³. The real one is {k} times as long in every direction. What is the real volume?",
              f"একটা {what_bn}-মডেলের আয়তন {vol:,} cm³। আসলটা প্রতি দিকে {k} গুণ লম্বা। আসলটার আয়তন কত?", r,
              f"Volume scale factor = {k}³ = {k ** 3}; {vol:,} x {k ** 3} = {r:,} cm³.",
              f"আয়তনের স্কেল-গুণক = {k}³ = {k ** 3}; {vol:,} x {k ** 3} = {r:,} cm³।",
              (vol * k, vol * k * k, vol * k ** 4), " cm³")


def trap(h, ys, what_en, what_bn):
    a = _c(h / 2 * (ys[0] + ys[-1] + 2 * sum(ys[1:-1])))
    return _n(f"{what_en} is measured every {h} m: heights {', '.join(map(str, ys))} m. Use the trapezium rule to estimate the cross-section area.",
              f"{what_bn} প্রতি {h} m অন্তর মাপা হলো: উচ্চতা {', '.join(map(str, ys))} m। ট্রাপিজিয়াম-নিয়মে প্রস্থচ্ছেদের ক্ষেত্রফল আন্দাজ করো।", a,
              f"Area ≈ h/2 x (first + last + 2 x middle ones) = {h}/2 x ({ys[0]} + {ys[-1]} + 2 x {sum(ys[1:-1])}) = {a:g} m².",
              f"ক্ষেত্রফল ≈ h/2 x (প্রথম + শেষ + 2 x মাঝেরগুলো) = {h}/2 x ({ys[0]} + {ys[-1]} + 2 x {sum(ys[1:-1])}) = {a:g} m²।",
              (_c(h * sum(ys)), _c(h * (len(ys) - 1) * max(ys)), _c(a / 2)), " m²")


def _lin(m, k):
    mx = "x" if m == 1 else "-x" if m == -1 else f"{m}x"
    return mx if k == 0 else f"{mx} + {k}" if k > 0 else f"{mx} - {-k}"


def comp(a, b, c, d, x):
    gx = c * x + d
    r = a * gx + b
    return _same(f"f(x) = {_lin(a, b)} and g(x) = {_lin(c, d)}. What is f(g({x}))?", f"f(x) = {_lin(a, b)} আর g(x) = {_lin(c, d)}। f(g({x})) কত?",
                 [str(v) for v in _o(r, c * (a * x + b) + d if c * (a * x + b) + d != r else r + 3, a * x + b + c * x + d, gx)],
                 f"First g({x}) = {c} x {x} + {d} = {gx}; then f({gx}) = {a} x {gx} + {b} = {r}.",
                 f"আগে g({x}) = {c} x {x} + {d} = {gx}; তারপর f({gx}) = {a} x {gx} + {b} = {r}।")


def sqprop(x1, y1, x2, what_en, what_bn):
    k = _c(y1 / (x1 * x1))
    y2 = _c(k * x2 * x2)
    return _n(f"{what_en} is proportional to the square of the span. A {x1} m span needs {y1:g}. How much does a {x2} m span need?",
              f"{what_bn} স্প্যানের বর্গের সমানুপাতিক। {x1} m স্প্যানে লাগে {y1:g}। {x2} m স্প্যানে কত লাগবে?", y2,
              f"y = kx²: k = {y1:g} ÷ {x1}² = {k:g}; y = {k:g} x {x2}² = {y2:g}.",
              f"y = kx²: k = {y1:g} ÷ {x1}² = {k:g}; y = {k:g} x {x2}² = {y2:g}।",
              (_c(y1 * x2 / x1), _c(y1 + (x2 - x1) ** 2), _c(y2 * 2)))


def rationalise(n):
    opts = [f"√{n} / {n}", f"{n} / √{n}", f"√{n}", f"1 / {n}"]
    return _same(f"Rationalise the denominator of 1 / √{n}.", f"1 / √{n}-এর হরকে মূলদ করো।", opts,
                 f"Multiply top and bottom by √{n}: 1/√{n} x √{n}/√{n} = √{n} / {n}.",
                 f"লব আর হরকে √{n} দিয়ে গুণ করো: 1/√{n} x √{n}/√{n} = √{n} / {n}।")


def condp(a, b, total, what_en, what_bn):
    r = f"{a}/{b}"
    from math import gcd
    g = gcd(a, b)
    simp = f"{a // g}/{b // g}"
    opts = [simp, f"{a}/{total}" if f"{a}/{total}" != simp else f"{b}/{total}", f"{b}/{total}" if f"{b}/{total}" != simp else f"{a + 1}/{b}", f"{b - a}/{b}" if f"{b - a}/{b}" != simp else f"{a}/{total + 1}"]
    seen = []
    for o in opts:
        if o not in seen:
            seen.append(o)
    while len(seen) < 4:
        seen.append(f"{a + len(seen)}/{b}")
    return _same(f"Of {total} welds inspected, {b} were made in winter, and {a} of those winter welds had defects. A winter weld is picked. What is the probability it has a defect?",
                 f"{total}টি পরীক্ষিত ঝালাইয়ের {b}টি শীতে করা, আর সেই শীতের ঝালাইয়ের {a}টিতে ত্রুটি। একটা শীতের ঝালাই বাছা হলো। ত্রুটি থাকার সম্ভাবনা কত?", seen,
                 f"We already know it is a winter weld, so only those {b} count: P = {r} = {simp}.",
                 f"জানা আছে এটা শীতের ঝালাই, তাই শুধু ওই {b}টি গোনা হয়: P = {r} = {simp}।")


ITEMS = (
    sine_rule(10, 30, 0.5, 90, 1), sine_rule(8, 90, 1, 30, 0.5), sine_rule(12, 45, 0.71, 60, 0.87), sine_rule(20, 60, 0.87, 45, 0.71),
    cos_rule(5, 8, 60, 0.5), cos_rule(3, 4, 90, 0), cos_rule(7, 8, 60, 0.5), cos_rule(6, 10, 60, 0.5),
    area_sin(8, 10, 30, 0.5, "A triangular gusset plate", "একটা ত্রিভুজাকার গাসেট-পাত"), area_sin(12, 15, 30, 0.5, "A sloping embankment panel", "একটা ঢালু বাঁধ-প্যানেল"),
    area_sin(6, 10, 90, 1, "A bracing panel", "একটা ব্রেসিং-প্যানেল"), area_sin(20, 14, 60, 0.87, "A triangular plot by the abutment", "প্রান্ত-ঠেকনার পাশে একটা ত্রিভুজাকার জমি"),
    qformula(2, -7, 3), qformula(1, -2, -15), qformula(3, 5, -2), qformula(2, 3, -2),
    csq(6, 2), csq(-8, 20), csq(4, -1), csq(-10, 30),
    simvol(2, 500, "bridge pier", "সেতু-স্তম্ভের"), simvol(10, 40, "concrete block", "কংক্রিট-ব্লকের"),
    simvol(3, 200, "tower top", "মিনার-চূড়ার"), simvol(5, 12, "bearing", "বিয়ারিংয়ের"),
    trap(2, [0, 3, 4, 3, 0], "A river channel", "একটা নদীখাত"), trap(5, [2, 6, 8, 6, 2], "An embankment", "একটা বাঁধ"),
    trap(1, [1, 2, 4, 2], "A culvert opening", "একটা কালভার্টের মুখ"),
    comp(2, 1, 3, -1, 2), comp(3, -4, 2, 5, 1), comp(5, 0, 1, 2, 3), comp(-1, 10, 4, 0, 2),
    sqprop(10, 4, 20, "The bending moment in a beam", "কড়ির বাঁকানো ভ্রামক"), sqprop(5, 3, 15, "The concrete needed for a slab of fixed shape", "নির্দিষ্ট আকারের স্ল্যাবের কংক্রিট"),
    sqprop(8, 16, 12, "The paint for a square deck panel", "একটা বর্গাকার পাটাতন-প্যানেলের রং"),
    rationalise(2), rationalise(3), rationalise(5), rationalise(7),
    qformula(1, -5, 4), cos_rule(8, 5, 90, 0), simvol(4, 25, "deck segment", "পাটাতন-খণ্ডের"), trap(3, [0, 2, 5, 2, 0], "A drainage ditch", "একটা নিকাশি-নালা"),
    comp(4, -3, 2, 1, 3), comp(1, 5, 3, -2, 4), sqprop(6, 9, 18, "The wind force on a square sign", "একটা বর্গাকার বোর্ডে হাওয়ার বল"),
    condp(6, 20, 50, "", ""), condp(3, 12, 40, "", ""), condp(5, 15, 60, "", ""), condp(9, 24, 80, "", ""),
    mcq("When do you use the sine rule rather than the cosine rule?", ["When you know a side and its opposite angle, plus one more side or angle", "Only for right-angled triangles", "When you know all three sides only", "Never in real life"], 0,
        "The cosine rule suits two sides and the angle between them, or all three sides.",
        "কোসাইন-সূত্রের বদলে কখন সাইন-সূত্র ব্যবহার করো?", ["যখন একটা বাহু আর তার বিপরীত কোণ জানা, সঙ্গে আরও একটা বাহু বা কোণ", "শুধু সমকোণী ত্রিভুজে", "শুধু তিন বাহু জানা থাকলে", "বাস্তবে কখনো না"],
        "দুই বাহু আর তাদের মাঝের কোণ, বা তিন বাহু জানা থাকলে কোসাইন-সূত্র মানানসই।"),
    mcq("What does the cosine rule become when the angle C is 90°?", ["Pythagoras' theorem, since cos 90° = 0", "The sine rule", "The area formula", "Nothing useful"], 0,
        "c² = a² + b² - 2ab x 0 = a² + b².",
        "কোণ C = 90° হলে কোসাইন-সূত্র কী হয়ে যায়?", ["পিথাগোরাসের উপপাদ্য, কারণ cos 90° = 0", "সাইন-সূত্র", "ক্ষেত্রফলের সূত্র", "কাজের কিছু না"],
        "c² = a² + b² - 2ab x 0 = a² + b²।"),
    mcq("A surveyor cannot measure across a river directly. How can trigonometry help?", ["Measure a baseline and two angles on one bank, then use the sine rule to find the width", "Guess the width", "Swim across with a tape", "Use only a compass"], 0,
        "This is triangulation - used for centuries to map land and set out bridges.",
        "একজন জরিপকারী সরাসরি নদীর এপার-ওপার মাপতে পারছেন না। ত্রিকোণমিতি কীভাবে সাহায্য করে?", ["এক পাড়ে একটা ভূমিরেখা আর দুটো কোণ মেপে সাইন-সূত্রে চওড়া বের করা", "চওড়া আন্দাজ করা", "ফিতে নিয়ে সাঁতরে পার হওয়া", "শুধু কম্পাস ব্যবহার"],
        "একে ত্রিভুজায়ন বলে - শতাব্দী ধরে জমি মাপা আর সেতু চিহ্নিত করতে ব্যবহার হয়।"),
    mcq("What is the exact value of sin 30°?", ["1/2", "√3/2", "1", "√2/2"], 0,
        "From an equilateral triangle cut in half: opposite 1, hypotenuse 2.",
        "sin 30°-এর নিখুঁত মান কত?", ["1/2", "√3/2", "1", "√2/2"],
        "অর্ধেক করা সমবাহু ত্রিভুজ থেকে: বিপরীত 1, অতিভুজ 2।"),
    mcq("What is the exact value of tan 45°?", ["1", "0", "√3", "1/2"], 0,
        "In a right-angled isosceles triangle the opposite and adjacent sides are equal.",
        "tan 45°-এর নিখুঁত মান কত?", ["1", "0", "√3", "1/2"],
        "সমকোণী সমদ্বিবাহু ত্রিভুজে বিপরীত আর সন্নিহিত বাহু সমান।"),
    mcq("What is the exact value of cos 60°?", ["1/2", "√3/2", "0", "1"], 0,
        "cos 60° = sin 30°.",
        "cos 60°-এর নিখুঁত মান কত?", ["1/2", "√3/2", "0", "1"],
        "cos 60° আর sin 30° সমান।"),
    mcq("What does the discriminant b² - 4ac tell you about a quadratic equation?", ["How many real solutions it has: two if positive, one if zero, none if negative", "The largest solution", "The y-intercept", "The gradient"], 0,
        "A negative discriminant means the curve never crosses the x-axis.",
        "নিরূপক b² - 4ac দ্বিঘাত সমীকরণ সম্পর্কে কী বলে?", ["কতগুলো বাস্তব সমাধান: ধনাত্মক হলে দুটো, শূন্য হলে একটা, ঋণাত্মক হলে নেই", "বড় সমাধানটা", "y-ছেদক", "ঢাল"],
        "ঋণাত্মক নিরূপক মানে বক্ররেখা x-অক্ষ ছেদ করে না।"),
    mcq("What does completing the square show you about the graph of y = (x - 3)² + 2?", ["Its lowest point (turning point) is at (3, 2)", "It crosses the y-axis at 3", "It has no turning point", "It is a straight line"], 0,
        "The square is never negative, so the smallest y is 2, when x = 3.",
        "y = (x - 3)² + 2-এর লেখচিত্র সম্পর্কে পূর্ণবর্গ কী দেখায়?", ["সবচেয়ে নিচু বিন্দু (বাঁক-বিন্দু) (3, 2)-এ", "y-অক্ষ 3-এ ছেদ করে", "বাঁক-বিন্দু নেই", "এটা সরলরেখা"],
        "বর্গ কখনো ঋণাত্মক নয়, তাই x = 3 হলে y সবচেয়ে কম, 2।"),
    mcq("If two similar shapes have lengths in the ratio 1 : 3, what is the ratio of their areas?", ["1 : 9", "1 : 3", "1 : 27", "1 : 6"], 0,
        "Area scale factor = (length scale factor)².",
        "দুটো সদৃশ আকারের দৈর্ঘ্যের অনুপাত 1 : 3 হলে ক্ষেত্রফলের অনুপাত কত?", ["1 : 9", "1 : 3", "1 : 27", "1 : 6"],
        "ক্ষেত্রফলের স্কেল-গুণক = (দৈর্ঘ্যের স্কেল-গুণক)²।"),
    mcq("A 1:10 model of a steel bridge weighs 15 kg. Roughly what would the full bridge weigh if made of the same material?", ["15,000 kg", "150 kg", "1,500 kg", "150,000 kg"], 0,
        "Mass follows volume: 10³ = 1,000, so 15 x 1,000 = 15,000 kg.",
        "একটা ইস্পাতের সেতুর 1:10 মডেলের ওজন 15 kg। একই উপাদানে পুরো সেতুর ওজন মোটামুটি কত হতো?", ["15,000 kg", "150 kg", "1,500 kg", "150,000 kg"],
        "ভর আয়তন মেনে চলে: 10³ = 1,000, তাই 15 x 1,000 = 15,000 kg।"),
    mcq("Why can't a bridge simply be scaled up 10 times from a model that works?", ["Weight grows 1,000 times but cross-section strength only 100 times, so it may fail under its own weight", "Big bridges are illegal", "Models use different gravity", "It can always be scaled up safely"], 0,
        "This 'square-cube law' is why huge structures need thicker members.",
        "কাজ-করা একটা মডেল থেকে সেতুকে সোজাসুজি 10 গুণ বড় করা যায় না কেন?", ["ওজন 1,000 গুণ বাড়ে, কিন্তু প্রস্থচ্ছেদের শক্তি মাত্র 100 গুণ, তাই নিজের ওজনেই ভেঙে পড়তে পারে", "বড় সেতু বেআইনি", "মডেলে মাধ্যাকর্ষণ আলাদা", "সবসময় নিরাপদে বড় করা যায়"],
        "এই 'বর্গ-ঘন সূত্রের' জন্যই বিশাল কাঠামোয় মোটা অংশ লাগে।"),
    mcq("What does the trapezium rule estimate?", ["The area under a curve, using strips shaped like trapeziums", "The gradient of a line", "The volume of a sphere", "The median of data"], 0,
        "More, narrower strips give a better estimate.",
        "ট্রাপিজিয়াম-নিয়ম কী আন্দাজ করে?", ["ট্রাপিজিয়াম-আকারের ফালি দিয়ে বক্ররেখার নিচের ক্ষেত্রফল", "সরলরেখার ঢাল", "গোলকের আয়তন", "তথ্যের মধ্যমা"],
        "বেশি, সরু ফালিতে আন্দাজ ভালো হয়।"),
    mcq("Engineers estimate a river's flow by multiplying cross-section area by average water speed. Why measure the area with many depth readings?", ["The riverbed is uneven, so more readings give a more accurate area", "To make the job longer", "Depth does not matter", "One reading is always exact"], 0,
        "Flow (m³/s) = area (m²) x speed (m/s) - vital for designing bridge openings.",
        "প্রকৌশলীরা প্রস্থচ্ছেদের ক্ষেত্রফলকে গড় জলবেগ দিয়ে গুণ করে নদীর প্রবাহ আন্দাজ করেন। অনেক গভীরতা মেপে ক্ষেত্রফল বের করা হয় কেন?", ["নদীর তল অসমান, তাই বেশি পাঠে ক্ষেত্রফল বেশি সঠিক", "কাজ লম্বা করতে", "গভীরতা গুরুত্বহীন", "একটা পাঠই সবসময় নিখুঁত"],
        "প্রবাহ (m³/s) = ক্ষেত্রফল (m²) x বেগ (m/s) - সেতুর ফাঁকের নকশায় জরুরি।"),
    mcq("What is the gradient of a curve at a point?", ["The gradient of the tangent drawn at that point", "The average of all y-values", "The area under the curve", "The y-intercept"], 0,
        "On a distance-time curve, it gives the speed at that instant.",
        "কোনো বিন্দুতে বক্ররেখার ঢাল কী?", ["সেই বিন্দুতে আঁকা স্পর্শকের ঢাল", "সব y-মানের গড়", "বক্ররেখার নিচের ক্ষেত্রফল", "y-ছেদক"],
        "দূরত্ব-সময় বক্ররেখায় এটা সেই মুহূর্তের দ্রুতি দেয়।"),
    mcq("How is the graph of y = f(x) + 4 related to y = f(x)?", ["It is moved up by 4", "It is moved right by 4", "It is stretched 4 times", "It is reflected"], 0,
        "Adding outside the function moves the graph vertically.",
        "y = f(x) + 4-এর লেখচিত্র y = f(x)-এর সঙ্গে কীভাবে সম্পর্কিত?", ["4 একক উপরে সরে", "4 একক ডানে সরে", "4 গুণ টানা হয়", "প্রতিফলিত হয়"],
        "অপেক্ষকের বাইরে যোগ করলে লেখচিত্র উল্লম্বভাবে সরে।"),
    mcq("How is the graph of y = f(x - 2) related to y = f(x)?", ["It is moved right by 2", "It is moved left by 2", "It is moved down by 2", "It is moved up by 2"], 0,
        "Changes inside the brackets move the graph horizontally - the 'opposite' way to the sign.",
        "y = f(x - 2)-এর লেখচিত্র y = f(x)-এর সঙ্গে কীভাবে সম্পর্কিত?", ["2 একক ডানে সরে", "2 একক বাঁয়ে সরে", "2 একক নিচে সরে", "2 একক উপরে সরে"],
        "বন্ধনীর ভেতরের বদল লেখচিত্রকে অনুভূমিকভাবে সরায় - চিহ্নের 'উল্টো' দিকে।"),
    mcq("What does y = -f(x) do to a graph?", ["Reflects it in the x-axis", "Reflects it in the y-axis", "Moves it left", "Doubles it"], 0,
        "An arch y = 16 - x² reflected becomes a valley y = x² - 16.",
        "y = -f(x) লেখচিত্রের কী করে?", ["x-অক্ষে প্রতিফলিত করে", "y-অক্ষে প্রতিফলিত করে", "বাঁয়ে সরায়", "দ্বিগুণ করে"],
        "খিলান y = 16 - x² প্রতিফলিত হয়ে উপত্যকা y = x² - 16 হয়।"),
    mcq("What is an 'iterative' method for solving an equation?", ["Repeating a formula, feeding each answer back in, until the answers settle", "Guessing once", "Drawing a picture only", "Using a ruler"], 0,
        "Computers solve many engineering equations this way.",
        "সমীকরণ সমাধানের 'পুনরাবৃত্তিমূলক' পদ্ধতি কী?", ["একটা সূত্র বারবার চালানো, প্রতিটা উত্তর আবার ঢুকিয়ে, যতক্ষণ না উত্তর থিতু হয়", "একবার আন্দাজ", "শুধু ছবি আঁকা", "রুলার ব্যবহার"],
        "কম্পিউটার অনেক প্রকৌশল-সমীকরণ এভাবে সমাধান করে।"),
    mcq("Using xₙ₊₁ = √(xₙ + 6) with x₀ = 2, what is x₁?", ["√8 ≈ 2.83", "8", "√6 ≈ 2.45", "3"], 0,
        "x₁ = √(2 + 6) = √8. Repeating approaches the solution x = 3.",
        "xₙ₊₁ = √(xₙ + 6) আর x₀ = 2 ধরে x₁ কত?", ["√8 ≈ 2.83", "8", "√6 ≈ 2.45", "3"],
        "x₁ = √(2 + 6) = √8। বারবার করলে সমাধান x = 3-এর দিকে যায়।"),
    mcq("What is an 'algebraic proof'?", ["A step-by-step argument using algebra that shows a statement is always true", "Checking one example", "A drawing", "A guess that seems right"], 0,
        "One example can disprove a claim, but only a proof shows it is always true.",
        "'বীজগাণিতিক প্রমাণ' কী?", ["বীজগণিত দিয়ে ধাপে ধাপে যুক্তি, যা দেখায় একটা উক্তি সবসময় সত্য", "একটা উদাহরণ যাচাই", "একটা ছবি", "সঠিক মনে হওয়া আন্দাজ"],
        "একটা উদাহরণ দাবি ভুল প্রমাণ করতে পারে, কিন্তু শুধু প্রমাণই দেখায় তা সবসময় সত্য।"),
    mcq("Why is 2n always even for any whole number n?", ["It is 2 times a whole number, so it divides exactly by 2", "Because n is even", "Because 2 is odd", "It is not always even"], 0,
        "Similarly, 2n + 1 is always odd.",
        "যেকোনো পূর্ণসংখ্যা n-এর জন্য 2n সবসময় জোড় কেন?", ["এটা কোনো পূর্ণসংখ্যার 2 গুণ, তাই 2 দিয়ে ঠিক ভাগ যায়", "কারণ n জোড়", "কারণ 2 বিজোড়", "সবসময় জোড় নয়"],
        "একইভাবে 2n + 1 সবসময় বিজোড়।"),
    mcq("A claim says 'all prime numbers are odd'. How can you disprove it?", ["Find one counter-example: 2 is prime and even", "Check 3, 5 and 7", "Draw a graph", "It cannot be disproved"], 0,
        "A single counter-example is enough to disprove an 'all' statement.",
        "একটা দাবি বলে 'সব মৌলিক সংখ্যা বিজোড়'। কীভাবে ভুল প্রমাণ করবে?", ["একটা বিপরীত-উদাহরণ খোঁজো: 2 মৌলিক আর জোড়", "3, 5 আর 7 যাচাই", "লেখচিত্র আঁকা", "ভুল প্রমাণ করা যায় না"],
        "'সব'-বলা উক্তি ভুল প্রমাণে একটা বিপরীত-উদাহরণই যথেষ্ট।"),
    mcq("What is the composite function f(g(x)) if f(x) = x² and g(x) = x + 1?", ["(x + 1)²", "x² + 1", "x³ + 1", "2x + 1"], 0,
        "Apply g first, then f.",
        "f(x) = x² আর g(x) = x + 1 হলে যৌগিক অপেক্ষক f(g(x)) কী?", ["(x + 1)²", "x² + 1", "x³ + 1", "2x + 1"],
        "আগে g, তারপর f প্রয়োগ করো।"),
    mcq("What does 'conditional probability' mean?", ["The probability of an event given that another event has already happened", "A probability that is always 1", "A guess", "The probability of two things never happening"], 0,
        "Knowing extra information changes which outcomes are possible.",
        "'শর্তাধীন সম্ভাবনা' মানে কী?", ["অন্য একটা ঘটনা আগেই ঘটেছে জেনে একটা ঘটনার সম্ভাবনা", "সবসময় 1 হওয়া সম্ভাবনা", "আন্দাজ", "দুটো জিনিস কখনো না ঘটার সম্ভাবনা"],
        "বাড়তি তথ্য জানলে কোন ফল সম্ভব তা বদলায়।"),
    mcq("Two bolts are taken from a bag of 5 good and 5 faulty bolts without replacement. What is P(both faulty)?", ["2/9", "1/4", "1/2", "5/18"], 0,
        "5/10 x 4/9 = 20/90 = 2/9.",
        "5টা ভালো আর 5টা ত্রুটিপূর্ণ বল্টুর ব্যাগ থেকে না ফিরিয়ে দুটো তোলা হলো। P(দুটোই ত্রুটিপূর্ণ) কত?", ["2/9", "1/4", "1/2", "5/18"],
        "5/10 x 4/9 = 20/90 = 2/9।"),
    mcq("Events A and B are 'mutually exclusive'. What does that mean?", ["They cannot both happen at the same time", "They always happen together", "One causes the other", "They are independent"], 0,
        "For mutually exclusive events, P(A or B) = P(A) + P(B).",
        "ঘটনা A আর B 'পরস্পর-বর্জিত'। এর মানে কী?", ["দুটো একসঙ্গে ঘটতে পারে না", "সবসময় একসঙ্গে ঘটে", "একটা অন্যটা ঘটায়", "এরা স্বাধীন"],
        "পরস্পর-বর্জিত ঘটনায় P(A বা B) = P(A) + P(B)।"),
    mcq("What is the equation of a circle with centre (0, 0) and radius 5?", ["x² + y² = 25", "x² + y² = 5", "x + y = 5", "y = 5x²"], 0,
        "Every point on it is 5 from the centre: x² + y² = r².",
        "কেন্দ্র (0, 0) আর ব্যাসার্ধ 5-এর বৃত্তের সমীকরণ কী?", ["x² + y² = 25", "x² + y² = 5", "x + y = 5", "y = 5x²"],
        "এর প্রতিটা বিন্দু কেন্দ্র থেকে 5 দূরে: x² + y² = r²।"),
    mcq("Is the point (3, 4) on the circle x² + y² = 25?", ["Yes, because 9 + 16 = 25", "No, because 3 + 4 = 7", "No, because 25 is odd", "Only if the radius is 7"], 0,
        "Substitute and check: 3² + 4² = 25.",
        "বিন্দু (3, 4) কি বৃত্ত x² + y² = 25-এর উপর?", ["হ্যাঁ, কারণ 9 + 16 = 25", "না, কারণ 3 + 4 = 7", "না, কারণ 25 বিজোড়", "শুধু ব্যাসার্ধ 7 হলে"],
        "বসিয়ে যাচাই করো: 3² + 4² = 25।"),
    mcq("A circular arch has its centre 3 m below the road and a radius of 5 m. How high is the top of the arch above the centre?", ["5 m", "3 m", "8 m", "2 m"], 0,
        "The top is one radius above the centre - so 2 m above road level.",
        "একটা বৃত্তাকার খিলানের কেন্দ্র রাস্তার 3 m নিচে আর ব্যাসার্ধ 5 m। খিলানের মাথা কেন্দ্র থেকে কত উঁচুতে?", ["5 m", "3 m", "8 m", "2 m"],
        "মাথা কেন্দ্র থেকে এক ব্যাসার্ধ উপরে - তাই রাস্তা থেকে 2 m উপরে।"),
    mcq("What does the circle theorem 'angles in the same segment are equal' allow a surveyor to do?", ["Find points on a circular curve by keeping the same angle to two fixed marks", "Measure a river's depth", "Weigh steel", "Count traffic"], 0,
        "Classic geometry is still used to set out curved roads and bridges.",
        "বৃত্তের উপপাদ্য 'একই বৃত্তাংশের কোণ সমান' জরিপকারীকে কী করতে দেয়?", ["দুটো স্থির চিহ্নের সঙ্গে একই কোণ রেখে বৃত্তাকার বাঁকের বিন্দু খুঁজে পাওয়া", "নদীর গভীরতা মাপা", "ইস্পাত ওজন", "যানবাহন গোনা"],
        "ধ্রুপদী জ্যামিতি এখনো বাঁকা রাস্তা আর সেতু চিহ্নিত করতে ব্যবহার হয়।"),
    mcq("What is the angle at the centre of a circle compared with the angle at the circumference from the same arc?", ["Twice as big", "Half as big", "The same", "90° more"], 0,
        "This theorem underlies many setting-out tricks.",
        "একই চাপ থেকে বৃত্তের কেন্দ্রস্থ কোণ পরিধিস্থ কোণের তুলনায় কেমন?", ["দ্বিগুণ", "অর্ধেক", "সমান", "90° বেশি"],
        "এই উপপাদ্য অনেক চিহ্নিতকরণ-কৌশলের ভিত্তি।"),
    mcq("Opposite angles of a cyclic quadrilateral (all corners on a circle) add up to…", ["180°", "360°", "90°", "270°"], 0,
        "One is 70°, so the opposite one is 110°.",
        "বৃত্তস্থ চতুর্ভুজের (সব কোণ বৃত্তের উপর) বিপরীত কোণের যোগফল…", ["180°", "360°", "90°", "270°"],
        "একটা 70° হলে বিপরীতটা 110°।"),
    mcq("What is a 'unit vector'?", ["A vector of length 1, used to show a direction", "A vector of zero length", "Any vector with units", "A vector pointing down"], 0,
        "Forces are often written as size x unit vector.",
        "'একক ভেক্টর' কী?", ["দৈর্ঘ্য 1-এর ভেক্টর, যা দিক বোঝাতে ব্যবহার হয়", "শূন্য দৈর্ঘ্যের ভেক্টর", "একক-যুক্ত যেকোনো ভেক্টর", "নিচমুখী ভেক্টর"],
        "বল প্রায়ই মান x একক ভেক্টর হিসেবে লেখা হয়।"),
    mcq("Two cable forces act on a pylon top: (30, -40) kN and (-30, -40) kN. What is the resultant?", ["(0, -80) kN, straight down", "(60, 0) kN", "(0, 0) kN", "(-60, -80) kN"], 0,
        "Horizontal parts cancel; vertical parts add - a balanced cable-stayed tower.",
        "একটা মিনারের মাথায় দুটো তারের বল: (30, -40) kN আর (-30, -40) kN। লব্ধি কত?", ["(0, -80) kN, সোজা নিচে", "(60, 0) kN", "(0, 0) kN", "(-60, -80) kN"],
        "অনুভূমিক অংশ কাটাকাটি; উল্লম্ব অংশ যোগ হয় - ভারসাম্যপূর্ণ কেবল-স্টেড মিনার।"),
    mcq("A rope pulls a crate with force 50 N at 60° above the horizontal (cos 60° = 0.5). What is the horizontal component?", ["25 N", "50 N", "43 N", "100 N"], 0,
        "Horizontal component = 50 x cos 60° = 25 N.",
        "একটা দড়ি অনুভূমিকের 60° উপরে 50 N বলে একটা বাক্স টানে (cos 60° = 0.5)। অনুভূমিক উপাংশ কত?", ["25 N", "50 N", "43 N", "100 N"],
        "অনুভূমিক উপাংশ = 50 x cos 60° = 25 N।"),
    mcq("Why do engineers write large calculations with 'significant figures' rather than all calculator digits?", ["The answer cannot be more precise than the measurements used", "Calculators are wrong", "Long numbers are illegal", "To make answers bigger"], 0,
        "A length measured to 3 significant figures gives answers to about 3 significant figures.",
        "প্রকৌশলীরা বড় হিসাব ক্যালকুলেটরের সব অঙ্ক না দিয়ে 'সার্থক অঙ্কে' লেখেন কেন?", ["ব্যবহৃত মাপের চেয়ে উত্তর বেশি নিখুঁত হতে পারে না", "ক্যালকুলেটর ভুল", "লম্বা সংখ্যা বেআইনি", "উত্তর বড় করতে"],
        "3 সার্থক অঙ্কে মাপা দৈর্ঘ্য প্রায় 3 সার্থক অঙ্কের উত্তর দেয়।"),
    mcq("For any angle θ, what is sin²θ + cos²θ?", ["1", "0", "2", "-1"], 0,
        "From Pythagoras in a right-angled triangle with hypotenuse 1.",
        "যেকোনো কোণ θ-এর জন্য sin²θ + cos²θ কত?", ["1", "0", "2", "-1"],
        "অতিভুজ 1 এমন সমকোণী ত্রিভুজে পিথাগোরাস থেকে আসে।"),
    mcq("The graph of y = sin x repeats itself every…", ["360°", "180°", "90°", "45°"], 0,
        "Repeating patterns like this model vibrations and tides.",
        "y = sin x-এর লেখচিত্র প্রতি কত অন্তর নিজেকে পুনরাবৃত্তি করে?", ["360°", "180°", "90°", "45°"],
        "এমন পুনরাবৃত্ত নকশা কম্পন আর জোয়ারের মডেল বানায়।"),
    mcq("Traffic on a bridge is 10,000 vehicles a day and grows 4% a year. Which expression gives the daily traffic after n years?", ["10,000 x 1.04ⁿ", "10,000 + 4n", "10,000 x 0.96ⁿ", "10,000 x 4ⁿ"], 0,
        "Each year multiplies by 1.04 - exponential growth.",
        "একটা সেতুতে দিনে 10,000টি যান চলে আর বছরে 4% বাড়ে। n বছর পরে দৈনিক যান কোন রাশিতে মেলে?", ["10,000 x 1.04ⁿ", "10,000 + 4n", "10,000 x 0.96ⁿ", "10,000 x 4ⁿ"],
        "প্রতি বছর 1.04 দিয়ে গুণ - সূচকীয় বৃদ্ধি।"),
    mcq("A line has gradient 3 and passes through (0, 2). What is its equation?", ["y = 3x + 2", "y = 2x + 3", "y = 3x - 2", "y = x + 5"], 0,
        "y = mx + c with m = 3 and c = 2.",
        "একটা রেখার ঢাল 3 আর (0, 2) দিয়ে যায়। এর সমীকরণ কী?", ["y = 3x + 2", "y = 2x + 3", "y = 3x - 2", "y = x + 5"],
        "y = mx + c, যেখানে m = 3 আর c = 2।"),
    mcq("What is the gradient of a line perpendicular to y = 2x + 1?", ["-1/2", "2", "-2", "1/2"], 0,
        "Perpendicular gradients multiply to -1: 2 x (-1/2) = -1.",
        "y = 2x + 1-এর লম্ব রেখার ঢাল কত?", ["-1/2", "2", "-2", "1/2"],
        "লম্ব রেখার ঢালের গুণফল -1: 2 x (-1/2) = -1।"),
    mcq("A survey peg is halfway between (4, 6) and (10, 14). Where is it?", ["(7, 10)", "(14, 20)", "(6, 8)", "(3, 4)"], 0,
        "Average the coordinates: ((4 + 10) ÷ 2, (6 + 14) ÷ 2).",
        "একটা জরিপ-খুঁটি (4, 6) আর (10, 14)-এর ঠিক মাঝখানে। কোথায়?", ["(7, 10)", "(14, 20)", "(6, 8)", "(3, 4)"],
        "স্থানাঙ্কের গড় নাও: ((4 + 10) ÷ 2, (6 + 14) ÷ 2)।"),
    mcq("How far apart are survey points (1, 2) and (7, 10)?", ["10", "14", "8", "6"], 0,
        "√(6² + 8²) = √100 = 10.",
        "জরিপ-বিন্দু (1, 2) আর (7, 10)-এর দূরত্ব কত?", ["10", "14", "8", "6"],
        "√(6² + 8²) = √100 = 10।"),
    mcq("Round 0.004567 to 2 significant figures.", ["0.0046", "0.0045", "0.00457", "0.005"], 0,
        "The first significant figure is 4; the next is 5, and the following 6 rounds it up to 6.",
        "0.004567-কে 2 সার্থক অঙ্কে আসন্ন করো।", ["0.0046", "0.0045", "0.00457", "0.005"],
        "প্রথম সার্থক অঙ্ক 4; পরেরটা 5, তার পরের 6 তাকে 6-এ তোলে।"),
    mcq("What is the exponential decay formula used for a bridge's paint thickness that falls 5% a year from 300 µm?", ["300 x 0.95ⁿ", "300 - 5n", "300 x 1.05ⁿ", "300 ÷ 5n"], 0,
        "Each year keeps 95% of the year before.",
        "সেতুর রঙের পুরুত্ব 300 µm থেকে বছরে 5% কমলে কোন সূচকীয় হ্রাসের সূত্র ব্যবহার হয়?", ["300 x 0.95ⁿ", "300 - 5n", "300 x 1.05ⁿ", "300 ÷ 5n"],
        "প্রতি বছর আগের বছরের 95% থাকে।"),
    mcq("What does an 'asymptote' on a graph mean?", ["A line the curve gets closer and closer to but never reaches", "The highest point", "A straight-line graph", "Where the graph crosses the y-axis"], 0,
        "y = 1/x has asymptotes along both axes.",
        "লেখচিত্রে 'অসীমতট' (অ্যাসিম্পটোট) মানে কী?", ["যে রেখার কাছে বক্ররেখা ক্রমশ এগোয়, কিন্তু কখনো পৌঁছায় না", "সর্বোচ্চ বিন্দু", "সরলরেখার লেখচিত্র", "যেখানে লেখচিত্র y-অক্ষ ছেদ করে"],
        "y = 1/x-এর দুই অক্ষ বরাবর অসীমতট।"),
    mcq("Which graph shape fits 'time to finish is inversely proportional to the number of crews'?", ["A curve like y = k/x that falls steeply then flattens", "A straight line through the origin", "A U-shaped parabola", "A horizontal line"], 0,
        "Doubling crews halves the time - but never reaches zero.",
        "'শেষ করার সময় দলের সংখ্যার ব্যস্তানুপাতিক' - কোন লেখচিত্র মানানসই?", ["y = k/x-এর মতো বক্ররেখা, যা খাড়া নেমে পরে চ্যাপ্টা হয়", "মূলবিন্দু দিয়ে সরলরেখা", "U-আকারের অধিবৃত্ত", "অনুভূমিক রেখা"],
        "দল দ্বিগুণ করলে সময় অর্ধেক - কিন্তু কখনো শূন্যে পৌঁছায় না।"),
    mcq("Solve together: y = x + 1 and y = x² - 1. Which points are solutions?", ["(2, 3) and (-1, 0)", "(1, 2) and (0, 1)", "(3, 4) only", "(0, -1) only"], 0,
        "x + 1 = x² - 1, so x² - x - 2 = 0, (x - 2)(x + 1) = 0.",
        "একসঙ্গে সমাধান করো: y = x + 1 আর y = x² - 1। কোন বিন্দুগুলো সমাধান?", ["(2, 3) আর (-1, 0)", "(1, 2) আর (0, 1)", "শুধু (3, 4)", "শুধু (0, -1)"],
        "x + 1 = x² - 1, তাই x² - x - 2 = 0, (x - 2)(x + 1) = 0।"),
    mcq("Simplify (x² - 9) / (x + 3).", ["x - 3", "x + 3", "x - 9", "x² - 3"], 0,
        "x² - 9 = (x - 3)(x + 3); cancel the (x + 3).",
        "সরল করো: (x² - 9) / (x + 3)।", ["x - 3", "x + 3", "x - 9", "x² - 3"],
        "x² - 9 = (x - 3)(x + 3); (x + 3) কেটে দাও।"),
    mcq("Simplify 1/x + 1/(2x).", ["3/(2x)", "2/(3x)", "1/(3x)", "2/x"], 0,
        "Common denominator 2x: 2/(2x) + 1/(2x) = 3/(2x).",
        "সরল করো: 1/x + 1/(2x)।", ["3/(2x)", "2/(3x)", "1/(3x)", "2/x"],
        "সাধারণ হর 2x: 2/(2x) + 1/(2x) = 3/(2x)।"),
    mcq("A crane's reach R (m) and safe load L (t) follow L = 120 / R. What is the safe load at 30 m?", ["4 t", "40 t", "0.25 t", "3,600 t"], 0,
        "120 ÷ 30 = 4 tonnes - always check the load chart for the actual radius.",
        "একটা ক্রেনের নাগাল R (m) আর নিরাপদ বোঝা L (t) মানে L = 120 / R। 30 m-এ নিরাপদ বোঝা কত?", ["4 t", "40 t", "0.25 t", "3,600 t"],
        "120 ÷ 30 = 4 টন - আসল ব্যাসার্ধে সবসময় বোঝা-তালিকা যাচাই করো।"),
)
