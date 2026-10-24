"""Class 10 - Math (Bridge Engineer): arithmetic progressions (nth term and sums), the section
formula, area of a triangle from coordinates, heights and distances with angles of elevation and
depression, tangent lengths, frustums, cones and combined solids, mean and modal class of
grouped data, trigonometric identities and probability - all from bridge sites."""
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


def ap_n(a, d, n, what_en, what_bn):
    t = a + (n - 1) * d
    return _n(f"{what_en}: {a}, {a + d}, {a + 2 * d}, … (adding {d} each time). What is term number {n}?",
              f"{what_bn}: {a}, {a + d}, {a + 2 * d}, … (প্রতিবার {d} যোগ)। {n}-তম পদ কত?", t,
              f"aₙ = a + (n - 1)d = {a} + {n - 1} x {d} = {t}.",
              f"aₙ = a + (n - 1)d = {a} + {n - 1} x {d} = {t}।",
              (a + n * d, a * n, n * d))


def ap_sum(a, d, n, what_en, what_bn):
    s = n * (2 * a + (n - 1) * d) // 2
    last = a + (n - 1) * d
    return _n(f"{what_en}: the first is {a}, and each one is {d} more than the last. What is the total for {n} of them?",
              f"{what_bn}: প্রথমটা {a}, আর প্রতিটা আগেরটার চেয়ে {d} বেশি। {n}টির মোট কত?", s,
              f"Sₙ = n/2 x (first + last) = {n}/2 x ({a} + {last}) = {s:,}.",
              f"Sₙ = n/2 x (প্রথম + শেষ) = {n}/2 x ({a} + {last}) = {s:,}।",
              (n * last, n * a, s + last))


def section(x1, y1, x2, y2, m, n):
    x = _c((m * x2 + n * x1) / (m + n))
    y = _c((m * y2 + n * y1) / (m + n))
    opts = [f"({x:g}, {y:g})", f"({_c((x1 + x2) / 2):g}, {_c((y1 + y2) / 2):g})" if (_c((x1 + x2) / 2), _c((y1 + y2) / 2)) != (x, y) else f"({x + 1:g}, {y:g})",
            f"({_c((n * x2 + m * x1) / (m + n)):g}, {_c((n * y2 + m * y1) / (m + n)):g})", f"({x2 - x1}, {y2 - y1})"]
    seen = []
    for o in opts:
        if o not in seen:
            seen.append(o)
    while len(seen) < 4:
        seen.append(f"({x + len(seen):g}, {y + 1:g})")
    return _same(f"A survey peg divides the line from A({x1}, {y1}) to B({x2}, {y2}) in the ratio {m} : {n}. Where is it?",
                 f"একটা জরিপ-খুঁটি A({x1}, {y1}) থেকে B({x2}, {y2}) রেখাকে {m} : {n} অনুপাতে ভাগ করে। খুঁটিটা কোথায়?", seen,
                 f"Section formula: x = ({m} x {x2} + {n} x {x1}) ÷ {m + n} = {x:g}, y = ({m} x {y2} + {n} x {y1}) ÷ {m + n} = {y:g}.",
                 f"বিভাজন-সূত্র: x = ({m} x {x2} + {n} x {x1}) ÷ {m + n} = {x:g}, y = ({m} x {y2} + {n} x {y1}) ÷ {m + n} = {y:g}।")


def tri_area(p, q, r):
    (x1, y1), (x2, y2), (x3, y3) = p, q, r
    a = _c(abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)
    return _n(f"A triangular plot for a bridge abutment has corners at ({x1}, {y1}), ({x2}, {y2}) and ({x3}, {y3}) metres. What is its area?",
              f"সেতুর প্রান্ত-ঠেকনার একটা ত্রিভুজাকার জমির কোণগুলো ({x1}, {y1}), ({x2}, {y2}) আর ({x3}, {y3}) মিটারে। ক্ষেত্রফল কত?", a,
              f"Area = ½ |x1(y2 - y3) + x2(y3 - y1) + x3(y1 - y2)| = {a:g} m².",
              f"ক্ষেত্রফল = ½ |x1(y2 - y3) + x2(y3 - y1) + x3(y1 - y2)| = {a:g} m²।",
              (_c(a * 2), _c(a / 2), _c(a + 6)), " m²")


def elev(d, ang, tanv, what_en, what_bn):
    h = _c(d * tanv)
    return _n(f"From a point {d} m from the foot of {what_en}, the angle of elevation of the top is {ang}°. How tall is it? (tan {ang}° = {tanv:g})",
              f"{what_bn}-এর পাদদেশ থেকে {d} m দূরের একটা বিন্দু থেকে চূড়ার উন্নতি-কোণ {ang}°। এটা কত উঁচু? (tan {ang}° = {tanv:g})", h,
              f"tan θ = height ÷ distance, so height = {d} x {tanv:g} = {h:g} m.",
              f"tan θ = উচ্চতা ÷ দূরত্ব, তাই উচ্চতা = {d} x {tanv:g} = {h:g} m।",
              (_c(d / tanv), d, _c(h * 2)), " m")


def depress(h, ang, tanv):
    d = _c(h / tanv)
    return _n(f"From a bridge deck {h} m above the water, the angle of depression of a boat is {ang}°. How far is the boat from the foot of the bridge? (tan {ang}° = {tanv:g})",
              f"জল থেকে {h} m উঁচু একটা সেতুর পাটাতন থেকে একটা নৌকার অবনতি-কোণ {ang}°। সেতুর পাদদেশ থেকে নৌকা কত দূরে? (tan {ang}° = {tanv:g})", d,
              f"The angle of depression equals the angle of elevation from the boat, so distance = {h} ÷ {tanv:g} = {d:g} m.",
              f"অবনতি-কোণ নৌকা থেকে উন্নতি-কোণের সমান, তাই দূরত্ব = {h} ÷ {tanv:g} = {d:g} m।",
              (_c(h * tanv), h, _c(d * 2)), " m")


def tangent(d, r):
    t = _c((d * d - r * r) ** 0.5)
    return _n(f"A survey point is {d} m from the centre of a circular roundabout of radius {r} m. How long is the tangent from the point to the circle?",
              f"একটা জরিপ-বিন্দু {r} m ব্যাসার্ধের বৃত্তাকার গোলচক্করের কেন্দ্র থেকে {d} m দূরে। বিন্দু থেকে বৃত্তে স্পর্শকের দৈর্ঘ্য কত?", t,
              f"The tangent meets the radius at 90°: t = √({d}² - {r}²) = √{d * d - r * r} = {t:g} m.",
              f"স্পর্শক ব্যাসার্ধের সঙ্গে 90° করে: t = √({d}² - {r}²) = √{d * d - r * r} = {t:g} m।",
              (d - r, _c((d * d + r * r) ** 0.5), d + r), " m")


def frustum(R, r, h, what_en, what_bn):
    k = _c(h * (R * R + r * r + R * r) / 3)
    f = lambda x: f"{x:g}π m³"
    opts = [f(k), f(_c(h * (R * R + r * r) / 3)), f(_c(h * (R * R + r * r + R * r))), f(_c(h * R * R / 3))]
    return _same(f"{what_en} is a frustum of a cone: top radius {r} m, bottom radius {R} m, height {h} m. What is its volume? (V = ⅓πh(R² + r² + Rr))",
                 f"{what_bn} শঙ্কুর একটা ছিন্নক: উপরের ব্যাসার্ধ {r} m, নিচের {R} m, উচ্চতা {h} m। আয়তন কত? (V = ⅓πh(R² + r² + Rr))", opts,
                 f"V = ⅓ x π x {h} x ({R * R} + {r * r} + {R * r}) = {k:g}π m³.",
                 f"V = ⅓ x π x {h} x ({R * R} + {r * r} + {R * r}) = {k:g}π m³।")


def capsule(r, h, what_en, what_bn):
    k = _c(r * r * h + 2 * r ** 3 / 3)
    f = lambda x: f"{x:g}π m³"
    opts = [f(k), f(_c(r * r * h)), f(_c(r * r * h + 4 * r ** 3 / 3)), f(_c(r * r * h + r ** 3 / 3))]
    return _same(f"{what_en} is a cylinder of radius {r} m and height {h} m topped by a hemisphere of the same radius. What is its volume?",
                 f"{what_bn} হলো {r} m ব্যাসার্ধ আর {h} m উচ্চতার একটা চোঙ, মাথায় একই ব্যাসার্ধের অর্ধগোলক। আয়তন কত?", opts,
                 f"Cylinder πr²h = {r * r * h}π; hemisphere ⅔πr³ = {_c(2 * r ** 3 / 3):g}π; total {k:g}π m³.",
                 f"চোঙ πr²h = {r * r * h}π; অর্ধগোলক ⅔πr³ = {_c(2 * r ** 3 / 3):g}π; মোট {k:g}π m³।")


def gmean(mids, freqs, what_en, what_bn):
    tot = sum(m * f for m, f in zip(mids, freqs))
    n = sum(freqs)
    r = _c(tot / n)
    table = ", ".join(f"{m} ({f})" for m, f in zip(mids, freqs))
    return _n(f"{what_en}, shown as class mid-point (frequency): {table}. Estimate the mean.",
              f"{what_bn}, শ্রেণি-মধ্যবিন্দু (পরিসংখ্যা) হিসেবে: {table}। গড় আন্দাজ করো।", r,
              f"Σfx = {tot:,}, Σf = {n}; mean ≈ {tot:,} ÷ {n} = {r:g}. It is an estimate because we use mid-points.",
              f"Σfx = {tot:,}, Σf = {n}; গড় ≈ {tot:,} ÷ {n} = {r:g}। মধ্যবিন্দু ব্যবহারে এটা আন্দাজ।",
              (_c(sum(mids) / len(mids)), _c(tot / len(mids)), max(mids)))


def slant(r, h):
    l = _c((r * r + h * h) ** 0.5)
    return _n(f"A conical spoil heap has base radius {r} m and height {h} m. What is its slant height?",
              f"একটা শঙ্কু-আকারের মাটির স্তূপের ভূমির ব্যাসার্ধ {r} m আর উচ্চতা {h} m। হেলানো উচ্চতা কত?", l,
              f"l = √(r² + h²) = √({r * r} + {h * h}) = {l:g} m.",
              f"l = √(r² + h²) = √({r * r} + {h * h}) = {l:g} m।",
              (r + h, _c(abs(h - r)) if h != r else l + 2, _c(l * 2)), " m")


def simul(a1, b1, c1, a2, b2, c2, x, y, what_en, what_bn):
    opts = [f"{x} and {y}", f"{y} and {x}" if x != y else f"{x + 1} and {y}", f"{x + 1} and {y - 1}", f"{x * 2} and {y * 2}"]
    opts_bn = [o.replace(" and ", " আর ") for o in opts]
    return mcq(f"{what_en}: {a1} cars and {b1} trucks pay Rs {c1:,} in tolls; {a2} cars and {b2} trucks pay Rs {c2:,}. What are the car and truck tolls (in Rs)?",
               opts, 0,
               f"Solve {a1}c + {b1}t = {c1} and {a2}c + {b2}t = {c2}: c = {x}, t = {y}. Check: {a1} x {x} + {b1} x {y} = {c1}.",
               f"{what_bn}: {a1}টি গাড়ি আর {b1}টি ট্রাক টোল দেয় {c1:,} টাকা; {a2}টি গাড়ি আর {b2}টি ট্রাক দেয় {c2:,} টাকা। গাড়ি আর ট্রাকের টোল (টাকায়) কত?",
               opts_bn,
               f"সমাধান করো {a1}c + {b1}t = {c1} আর {a2}c + {b2}t = {c2}: c = {x}, t = {y}। যাচাই: {a1} x {x} + {b1} x {y} = {c1}।")


ITEMS = (
    ap_n(5, 3, 20, "Bolt spacings along a girder (cm)", "গার্ডার বরাবর বল্টুর দূরত্ব (cm)"), ap_n(100, 15, 12, "Daily metres of deck laid", "রোজ বসানো পাটাতনের মিটার"),
    ap_n(2, 4, 30, "Rows of stones in a pier", "স্তম্ভে পাথরের সারি"), ap_n(50, -2, 10, "Litres left in a curing tank each hour", "প্রতি ঘণ্টায় কিউরিং-ট্যাঙ্কে বাকি লিটার"),
    ap_n(12, 6, 15, "Toll queue lengths each minute", "প্রতি মিনিটে টোলের লাইনের দৈর্ঘ্য"),
    ap_sum(10, 5, 10, "Truckloads delivered each day", "রোজ পৌঁছানো ট্রাক-বোঝাই"), ap_sum(1, 1, 50, "Cables in each row of a stack", "স্তূপের প্রতি সারিতে তার"),
    ap_sum(20, 10, 8, "Metres of piling driven each day", "রোজ বসানো পাইলের মিটার"), ap_sum(3, 2, 20, "Bricks in each course of a pier", "স্তম্ভের প্রতি স্তরে ইট"),
    ap_sum(100, 50, 6, "Monthly savings for a welding course (Rs)", "ঝালাই-কোর্সের মাসিক সঞ্চয় (টাকা)"),
    section(0, 0, 12, 6, 1, 2), section(2, 4, 10, 12, 3, 1), section(-4, 2, 8, 8, 1, 1), section(0, 10, 15, 0, 2, 3),
    tri_area((0, 0), (8, 0), (0, 6)), tri_area((1, 2), (7, 2), (4, 8)), tri_area((0, 0), (10, 4), (2, 8)), tri_area((-2, 0), (6, 0), (2, 7)),
    elev(30, 45, 1, "a bridge pylon", "একটা সেতু-মিনার"), elev(50, 30, 0.58, "a tower crane", "একটা টাওয়ার-ক্রেন"),
    elev(20, 60, 1.73, "a lighting mast", "একটা আলোর খুঁটি"), elev(100, 10, 0.18, "a cable-stay tower", "একটা কেবল-স্টে মিনার"),
    elev(40, 45, 1, "a concrete pier", "একটা কংক্রিট-স্তম্ভ"),
    depress(30, 45, 1), depress(20, 30, 0.58), depress(60, 60, 1.73),
    tangent(13, 5), tangent(10, 6), tangent(25, 7), tangent(17, 8),
    frustum(3, 1, 6, "A concrete pier footing", "একটা কংক্রিট-স্তম্ভের ভিত"), frustum(4, 2, 3, "A bridge-pier cap", "একটা সেতু-স্তম্ভের মাথা"),
    frustum(5, 2, 9, "A cooling tower section", "একটা শীতলীকরণ-মিনারের অংশ"),
    capsule(2, 6, "A water storage tank", "একটা জল-মজুতের ট্যাঙ্ক"), capsule(3, 10, "A cement silo", "একটা সিমেন্ট-সাইলো"), capsule(1, 4, "A buoy", "একটা বয়া"),
    gmean([5, 15, 25, 35], [4, 6, 8, 2], "Minutes waited by trucks at a site gate", "নির্মাণস্থলের ফটকে ট্রাকের অপেক্ষার মিনিট"),
    gmean([10, 30, 50], [5, 10, 5], "Daily concrete delivered (m³)", "রোজ পৌঁছানো কংক্রিট (m³)"),
    gmean([25, 35, 45, 55], [2, 5, 9, 4], "Ages of crane drivers", "ক্রেন-চালকদের বয়স"),
    gmean([150, 250, 350], [3, 4, 3], "Daily vehicle counts (hundreds)", "দৈনিক যানবাহন-গণনা (শতে)"),
    slant(3, 4), slant(6, 8), slant(5, 12), slant(8, 15),
    simul(2, 1, 250, 1, 2, 350, 50, 150, "A toll plaza check", "একটা টোল-প্লাজার হিসাব"), simul(3, 2, 420, 1, 1, 180, 60, 120, "Weekend tolls", "সপ্তাহান্তের টোল"),
    simul(4, 1, 380, 2, 3, 640, 50, 180, "Night tolls", "রাতের টোল"), simul(5, 2, 700, 2, 1, 320, 60, 200, "Festival tolls", "উৎসবের টোল"),
    ap_n(7, 5, 25, "Fence posts numbered along an approach", "সংযোগ-পথ বরাবর নম্বর দেওয়া বেড়ার খুঁটি"), ap_n(40, 8, 18, "Cars per minute as a jam clears", "জট কাটার সময় মিনিটে গাড়ি"),
    ap_sum(5, 3, 15, "Rungs fitted on a ladder each hour", "প্রতি ঘণ্টায় মইয়ে লাগানো ধাপ"), section(-6, -3, 9, 12, 2, 1), tri_area((3, 1), (9, 1), (5, 11)),
    elev(25, 60, 1.73, "a signal mast", "একটা সংকেত-খুঁটি"), depress(45, 45, 1), tangent(15, 9), frustum(6, 3, 4, "A pier base", "একটা স্তম্ভের ভিত্তি"),
    capsule(2, 9, "A grout tank", "একটা গ্রাউট-ট্যাঙ্ক"), slant(7, 24),
    gmean([2, 6, 10, 14], [3, 7, 6, 4], "Hours of overtime per worker", "কর্মীপ্রতি ওভারটাইমের ঘণ্টা"),
    mcq("What is an 'arithmetic progression'?", ["A sequence where each term is found by adding the same number to the one before", "A sequence where each term is doubled", "A list of random numbers", "A sequence that never changes"], 0,
        "That fixed number is the common difference d.",
        "'সমান্তর প্রগতি' কী?", ["যে অনুক্রমে প্রতিটা পদ আগেরটায় একই সংখ্যা যোগ করে পাওয়া যায়", "যে অনুক্রমে প্রতিটা পদ দ্বিগুণ", "এলোমেলো সংখ্যার তালিকা", "যে অনুক্রম কখনো বদলায় না"],
        "সেই নির্দিষ্ট সংখ্যা হলো সাধারণ অন্তর d।"),
    mcq("A young Gauss added 1 + 2 + … + 100 in seconds. What is the sum?", ["5,050", "5,000", "10,100", "100"], 0,
        "Pair the ends: 50 pairs each adding to 101, so 50 x 101 = 5,050.",
        "ছোটবেলায় গাউস কয়েক সেকেন্ডে 1 + 2 + … + 100 যোগ করেছিলেন। যোগফল কত?", ["5,050", "5,000", "10,100", "100"],
        "প্রান্ত জোড়া করো: প্রতিটার যোগফল 101-এর 50টি জোড়া, তাই 50 x 101 = 5,050।"),
    mcq("What is the 'angle of elevation'?", ["The angle between the horizontal and your line of sight when looking up at an object", "The angle when looking down", "The angle of a slope only", "The angle between two walls"], 0,
        "Surveyors measure it with a clinometer or total station.",
        "'উন্নতি-কোণ' কী?", ["কোনো বস্তুর দিকে উপরে তাকালে অনুভূমিক আর দৃষ্টিরেখার মধ্যের কোণ", "নিচে তাকানোর কোণ", "শুধু ঢালের কোণ", "দুই দেয়ালের মধ্যের কোণ"],
        "জরিপকারীরা ক্লিনোমিটার বা টোটাল-স্টেশন দিয়ে মাপেন।"),
    mcq("Why does the angle of depression from a bridge to a boat equal the angle of elevation from the boat to the bridge?", ["They are alternate angles between parallel horizontal lines", "Boats are always level", "By coincidence", "They are not equal"], 0,
        "This lets surveyors use whichever angle is easier to measure.",
        "সেতু থেকে নৌকার অবনতি-কোণ নৌকা থেকে সেতুর উন্নতি-কোণের সমান কেন?", ["সমান্তরাল অনুভূমিক রেখার মধ্যে এরা একান্তর কোণ", "নৌকা সবসময় সমতল", "কাকতালীয়", "সমান নয়"],
        "জরিপকারীরা যেটা মাপা সহজ সেটা ব্যবহার করতে পারেন।"),
    mcq("For an angle θ, sin θ = 0.6 and cos θ = 0.8. What is tan θ?", ["0.75", "1.33", "0.48", "1.4"], 0,
        "tan θ = sin θ ÷ cos θ = 0.6 ÷ 0.8 = 0.75.",
        "একটা কোণ θ-এর জন্য sin θ = 0.6 আর cos θ = 0.8। tan θ কত?", ["0.75", "1.33", "0.48", "1.4"],
        "সূত্র: tan θ = sin θ ÷ cos θ = 0.6 ÷ 0.8 = 0.75।"),
    mcq("If tan θ = 3/4, what is 1 + tan²θ?", ["25/16", "7/4", "9/16", "5/4"], 0,
        "1 + 9/16 = 25/16 - which also equals sec²θ.",
        "tan θ = 3/4 হলে 1 + tan²θ কত?", ["25/16", "7/4", "9/16", "5/4"],
        "1 + 9/16 = 25/16 - যা sec²θ-এর সমানও।"),
    mcq("If sin θ = 3/5 for an acute angle, what is cos θ?", ["4/5", "3/4", "5/3", "2/5"], 0,
        "A 3-4-5 triangle: cos θ = adjacent ÷ hypotenuse = 4/5.",
        "সূক্ষ্মকোণের জন্য sin θ = 3/5 হলে cos θ কত?", ["4/5", "3/4", "5/3", "2/5"],
        "একটা 3-4-5 ত্রিভুজ: cos θ = সন্নিহিত ÷ অতিভুজ = 4/5।"),
    mcq("Given cos 30° ≈ 0.87, what is sin 60°?", ["About 0.87", "About 0.5", "About 1.73", "About 0.13"], 0,
        "sin(90° - θ) = cos θ, and 90° - 30° = 60°.",
        "cos 30° ≈ 0.87 হলে sin 60° কত?", ["প্রায় 0.87", "প্রায় 0.5", "প্রায় 1.73", "প্রায় 0.13"],
        "sin(90° - θ) = cos θ, আর 90° - 30° = 60°।"),
    mcq("How many tangents can be drawn to a circle from a point outside it?", ["Two, of equal length", "One", "None", "Infinitely many"], 0,
        "The two tangent lengths from an external point are always equal.",
        "বৃত্তের বাইরের একটা বিন্দু থেকে বৃত্তে কতগুলো স্পর্শক আঁকা যায়?", ["দুটো, সমান দৈর্ঘ্যের", "একটা", "একটাও না", "অসীম"],
        "বাইরের বিন্দু থেকে দুটো স্পর্শকের দৈর্ঘ্য সবসময় সমান।"),
    mcq("What is a 'frustum'?", ["The part of a cone or pyramid left after cutting off the top with a cut parallel to the base", "A whole cone", "A sphere cut in half", "A type of beam"], 0,
        "Many pier footings and buckets are frustum-shaped.",
        "'ছিন্নক' (ফ্রাস্টাম) কী?", ["ভূমির সমান্তরাল কেটে মাথা বাদ দেওয়ার পর শঙ্কু বা পিরামিডের বাকি অংশ", "পুরো শঙ্কু", "অর্ধেক কাটা গোলক", "এক রকম কড়ি"],
        "অনেক স্তম্ভের ভিত আর বালতি ছিন্নক-আকারের।"),
    mcq("What is the 'modal class' of grouped data?", ["The class with the highest frequency", "The middle class", "The class with the largest values", "The first class"], 0,
        "It tells you the most common range of values.",
        "শ্রেণিবদ্ধ তথ্যের 'ভূয়িষ্ঠক শ্রেণি' কী?", ["সবচেয়ে বেশি পরিসংখ্যার শ্রেণি", "মাঝের শ্রেণি", "সবচেয়ে বড় মানের শ্রেণি", "প্রথম শ্রেণি"],
        "সবচেয়ে সাধারণ মানের পরিসর জানায়।"),
    mcq("Why is the mean of grouped data only an estimate?", ["We use class mid-points instead of the exact values", "Grouped data has no mean", "The frequencies are guessed", "It is always exact"], 0,
        "The narrower the classes, the better the estimate.",
        "শ্রেণিবদ্ধ তথ্যের গড় শুধু আন্দাজ কেন?", ["আসল মানের বদলে শ্রেণি-মধ্যবিন্দু ব্যবহার করা হয়", "শ্রেণিবদ্ধ তথ্যের গড় নেই", "পরিসংখ্যা আন্দাজে ধরা", "সবসময় নিখুঁত"],
        "শ্রেণি যত সরু, আন্দাজ তত ভালো।"),
    mcq("What is the probability of an event that is certain to happen?", ["1", "0", "0.5", "100"], 0,
        "Probabilities run from 0 (impossible) to 1 (certain).",
        "যে ঘটনা নিশ্চিত ঘটবে তার সম্ভাবনা কত?", ["1", "0", "0.5", "100"],
        "সম্ভাবনা 0 (অসম্ভব) থেকে 1 (নিশ্চিত) পর্যন্ত।"),
    mcq("A fair dice is rolled. What is the probability of a number greater than 4?", ["1/3", "1/2", "2/3", "1/6"], 0,
        "5 and 6: 2 out of 6 = 1/3.",
        "একটা নিরপেক্ষ ছক্কা গড়ানো হলো। 4-এর বেশি সংখ্যা পড়ার সম্ভাবনা কত?", ["1/3", "1/2", "2/3", "1/6"],
        "5 আর 6: 6-এর মধ্যে 2 = 1/3।"),
    mcq("A box of 50 bolts has 3 faulty ones. One bolt is picked at random. What is the probability it is good?", ["47/50", "3/50", "1/50", "50/47"], 0,
        "47 good out of 50.",
        "50টি বল্টুর একটা বাক্সে 3টি ত্রুটিপূর্ণ। এলোমেলোভাবে একটা তোলা হলো। ভালো হওয়ার সম্ভাবনা কত?", ["47/50", "3/50", "1/50", "50/47"],
        "50-এর মধ্যে 47টি ভালো।"),
    mcq("Two coins are tossed. What is the probability of getting at least one head?", ["3/4", "1/2", "1/4", "1"], 0,
        "Only TT has no head: 1 - 1/4 = 3/4.",
        "দুটো মুদ্রা ছোড়া হলো। অন্তত একটা হেড পাওয়ার সম্ভাবনা কত?", ["3/4", "1/2", "1/4", "1"],
        "শুধু টিটি-তে হেড নেই: 1 - 1/4 = 3/4।"),
    mcq("What is the distance between points (2, 3) and (5, 7)?", ["5", "7", "25", "3"], 0,
        "√(3² + 4²) = √25 = 5.",
        "বিন্দু (2, 3) আর (5, 7)-এর দূরত্ব কত?", ["5", "7", "25", "3"],
        "√(3² + 4²) = √25 = 5।"),
    mcq("Points A, B and C are collinear (on one straight line). What is the area of triangle ABC?", ["Zero", "One", "It cannot be found", "Always 90"], 0,
        "Surveyors use this to check if three pegs are in a straight line.",
        "বিন্দু A, B আর C সমরেখ (একই সরলরেখায়)। ত্রিভুজ ABC-র ক্ষেত্রফল কত?", ["শূন্য", "এক", "বের করা যায় না", "সবসময় 90"],
        "তিনটে খুঁটি এক সরলরেখায় কিনা জরিপকারীরা এভাবে যাচাই করেন।"),
    mcq("What does the discriminant tell you about x² + 4x + 4 = 0?", ["b² - 4ac = 0, so there is exactly one (repeated) root, x = -2", "Two different roots", "No real roots", "Infinitely many roots"], 0,
        "It factorises as (x + 2)².",
        "x² + 4x + 4 = 0 সম্পর্কে নিরূপক কী জানায়?", ["b² - 4ac = 0, তাই ঠিক একটা (পুনরাবৃত্ত) বীজ, x = -2", "দুটো আলাদা বীজ", "কোনো বাস্তব বীজ নেই", "অসীম বীজ"],
        "এটা (x + 2)²-এ উৎপাদকে ভাঙে।"),
    mcq("The product of two consecutive positive integers is 132. What are they?", ["11 and 12", "10 and 13", "12 and 13", "6 and 22"], 0,
        "n(n + 1) = 132 gives n² + n - 132 = 0, (n - 11)(n + 12) = 0.",
        "দুটো পরপর ধনাত্মক পূর্ণসংখ্যার গুণফল 132। সংখ্যা দুটো কী?", ["11 আর 12", "10 আর 13", "12 আর 13", "6 আর 22"],
        "n(n + 1) = 132 থেকে n² + n - 132 = 0, (n - 11)(n + 12) = 0।"),
    mcq("A rectangular site office has an area of 60 m² and its length is 4 m more than its width. What is the width?", ["6 m", "10 m", "4 m", "15 m"], 0,
        "w(w + 4) = 60 gives w² + 4w - 60 = 0, (w - 6)(w + 10) = 0, so w = 6.",
        "একটা আয়তাকার নির্মাণস্থল-অফিসের ক্ষেত্রফল 60 m² আর দৈর্ঘ্য প্রস্থের চেয়ে 4 m বেশি। প্রস্থ কত?", ["6 m", "10 m", "4 m", "15 m"],
        "w(w + 4) = 60 থেকে w² + 4w - 60 = 0, (w - 6)(w + 10) = 0, তাই w = 6।"),
    mcq("What is the HCF of 84 and 126, used to cut two steel bars into the longest equal pieces with no waste?", ["42", "21", "14", "252"], 0,
        "84 = 2 x 42, 126 = 3 x 42.",
        "84 আর 126-এর গসাগু কত, যা দিয়ে দুটো ইস্পাতের রড কোনো অপচয় ছাড়া সবচেয়ে লম্বা সমান টুকরোয় কাটা যায়?", ["42", "21", "14", "252"],
        "84 = 2 x 42, 126 = 3 x 42।"),
    mcq("Two signal lights flash every 12 s and 18 s. They flash together now. After how many seconds will they next flash together?", ["36 s", "6 s", "30 s", "216 s"], 0,
        "The LCM of 12 and 18 is 36.",
        "দুটো সংকেত-বাতি প্রতি 12 s আর 18 s-এ জ্বলে। এখন একসঙ্গে জ্বলল। কত সেকেন্ড পরে আবার একসঙ্গে জ্বলবে?", ["36 s", "6 s", "30 s", "216 s"],
        "12 আর 18-এর লসাগু 36।"),
    mcq("Why is √2 irrational, according to the classic proof?", ["Assuming √2 = p/q in lowest terms leads to both p and q being even - a contradiction", "Because 2 is even", "Because it is less than 2", "It is rational"], 0,
        "Proof by contradiction is a powerful tool.",
        "ধ্রুপদী প্রমাণ অনুযায়ী √2 অমূলদ কেন?", ["√2 = p/q লঘিষ্ঠ আকারে ধরলে p আর q দুটোই জোড় হয় - স্ববিরোধ", "কারণ 2 জোড়", "কারণ এটা 2-এর কম", "এটা মূলদ"],
        "বিরোধের মাধ্যমে প্রমাণ এক শক্তিশালী হাতিয়ার।"),
    mcq("What is the sum of the zeroes of the polynomial x² - 7x + 10?", ["7", "10", "-7", "3"], 0,
        "For ax² + bx + c, the zeroes add to -b/a = 7 (they are 2 and 5).",
        "বহুপদী x² - 7x + 10-এর শূন্যগুলোর যোগফল কত?", ["7", "10", "-7", "3"],
        "ax² + bx + c-এর শূন্যগুলোর যোগফল -b/a = 7 (এরা 2 আর 5)।"),
    mcq("What is the product of the zeroes of x² - 7x + 10?", ["10", "7", "-10", "2"], 0,
        "Product = c/a = 10: 2 x 5 = 10.",
        "x² - 7x + 10-এর শূন্যগুলোর গুণফল কত?", ["10", "7", "-10", "2"],
        "গুণফল = c/a = 10: 2 x 5 = 10।"),
    mcq("How many solutions does a pair of parallel lines (like y = 2x + 1 and y = 2x + 5) have?", ["None - parallel lines never meet", "One", "Two", "Infinitely many"], 0,
        "Same gradient, different intercepts: inconsistent equations.",
        "সমান্তরাল দুটো রেখার (যেমন y = 2x + 1 আর y = 2x + 5) কতগুলো সমাধান?", ["একটাও না - সমান্তরাল রেখা কখনো মেশে না", "একটা", "দুটো", "অসীম"],
        "একই ঢাল, আলাদা ছেদক: অসংগত সমীকরণ।"),
    mcq("A road and a railway are drawn as lines on a map. When do they have exactly one crossing point?", ["When their gradients are different", "When they are parallel", "When they are the same line", "Never"], 0,
        "That crossing point is where a bridge or level crossing is needed.",
        "মানচিত্রে একটা রাস্তা আর একটা রেলপথ রেখা হিসেবে আঁকা। কখন এদের ঠিক একটা ছেদবিন্দু থাকে?", ["যখন ঢাল আলাদা", "যখন সমান্তরাল", "যখন একই রেখা", "কখনো না"],
        "সেই ছেদবিন্দুতে সেতু বা লেভেল-ক্রসিং লাগে।"),
    mcq("What does 'similar triangles' mean?", ["Triangles with the same angles, so their sides are in the same ratio", "Triangles with the same area", "Triangles with the same colour", "Triangles that are identical"], 0,
        "Surveyors use similar triangles to find heights from shadows.",
        "'সদৃশ ত্রিভুজ' মানে কী?", ["একই কোণের ত্রিভুজ, তাই বাহুগুলো একই অনুপাতে", "একই ক্ষেত্রফলের ত্রিভুজ", "একই রঙের ত্রিভুজ", "হুবহু এক ত্রিভুজ"],
        "জরিপকারীরা ছায়া থেকে উচ্চতা বের করতে সদৃশ ত্রিভুজ ব্যবহার করেন।"),
    mcq("A 2 m pole casts a 3 m shadow while a pylon casts a 60 m shadow at the same time. How tall is the pylon?", ["40 m", "90 m", "30 m", "120 m"], 0,
        "Similar triangles: height ÷ shadow is the same, so 2/3 x 60 = 40 m.",
        "একই সময়ে একটা 2 m খুঁটির ছায়া 3 m আর একটা মিনারের ছায়া 60 m। মিনার কত উঁচু?", ["40 m", "90 m", "30 m", "120 m"],
        "সদৃশ ত্রিভুজ: উচ্চতা ÷ ছায়া সমান, তাই 2/3 x 60 = 40 m।"),
    mcq("What does the Basic Proportionality Theorem (Thales) say?", ["A line parallel to one side of a triangle divides the other two sides in the same ratio", "All triangles are equal", "Angles add to 360°", "The longest side is opposite the right angle"], 0,
        "It is the basis of many scale and proportion methods in drawing.",
        "মৌলিক সমানুপাতিকতা উপপাদ্য (থেলিস) কী বলে?", ["ত্রিভুজের এক বাহুর সমান্তরাল রেখা অন্য দুটো বাহুকে একই অনুপাতে ভাগ করে", "সব ত্রিভুজ সমান", "কোণের যোগফল 360°", "দীর্ঘতম বাহু সমকোণের বিপরীতে"],
        "নকশায় অনেক মাপ আর অনুপাতের পদ্ধতির ভিত্তি।"),
    mcq("What is the area of a sector of radius 14 m with angle 90°? (π = 22/7)", ["154 m²", "616 m²", "44 m²", "22 m²"], 0,
        "90/360 x 22/7 x 14² = ¼ x 616 = 154 m².",
        "14 m ব্যাসার্ধ আর 90° কোণের বৃত্তকলার ক্ষেত্রফল কত? (π = 22/7)", ["154 m²", "616 m²", "44 m²", "22 m²"],
        "90/360 x 22/7 x 14² = ¼ x 616 = 154 m²।"),
    mcq("What is the curved surface area of a cylinder with radius 7 m and height 10 m? (π = 22/7)", ["440 m²", "154 m²", "1,540 m²", "220 m²"], 0,
        "2πrh = 2 x 22/7 x 7 x 10 = 440 m² - the area to paint on a round pier.",
        "7 m ব্যাসার্ধ আর 10 m উচ্চতার চোঙের বাঁকা পৃষ্ঠতল কত? (π = 22/7)", ["440 m²", "154 m²", "1,540 m²", "220 m²"],
        "2πrh = 2 x 22/7 x 7 x 10 = 440 m² - গোল স্তম্ভে রং করার ক্ষেত্রফল।"),
    mcq("A cylindrical pier of radius 1 m and height 7 m is cast. How much concrete is needed? (π = 22/7)", ["22 m³", "44 m³", "154 m³", "7 m³"], 0,
        "πr²h = 22/7 x 1 x 7 = 22 m³.",
        "1 m ব্যাসার্ধ আর 7 m উচ্চতার একটা চোঙাকার স্তম্ভ ঢালাই হবে। কত কংক্রিট লাগবে? (π = 22/7)", ["22 m³", "44 m³", "154 m³", "7 m³"],
        "πr²h = 22/7 x 1 x 7 = 22 m³।"),
    mcq("A cone of soil has radius 3 m and height 7 m. What is its volume? (π = 22/7)", ["66 m³", "198 m³", "22 m³", "132 m³"], 0,
        "⅓πr²h = ⅓ x 22/7 x 9 x 7 = 66 m³.",
        "একটা মাটির শঙ্কুর ব্যাসার্ধ 3 m আর উচ্চতা 7 m। আয়তন কত? (π = 22/7)", ["66 m³", "198 m³", "22 m³", "132 m³"],
        "⅓πr²h = ⅓ x 22/7 x 9 x 7 = 66 m³।"),
    mcq("When a solid is melted and recast into a new shape, what stays the same?", ["Its volume", "Its surface area", "Its shape", "Its height"], 0,
        "Equate the volumes to find the new dimensions.",
        "একটা ঘনবস্তু গলিয়ে নতুন আকারে ঢাললে কী একই থাকে?", ["এর আয়তন", "এর পৃষ্ঠতল", "এর আকার", "এর উচ্চতা"],
        "নতুন মাপ বের করতে আয়তন সমান ধরো।"),
    mcq("A 1 m³ block of steel is rolled into a plate 10 mm thick. What area does the plate cover?", ["100 m²", "10 m²", "1,000 m²", "1 m²"], 0,
        "Area = volume ÷ thickness = 1 ÷ 0.01 = 100 m².",
        "1 m³ ইস্পাতের ব্লক গড়িয়ে 10 mm পুরু পাত বানানো হলো। পাতটা কত ক্ষেত্রফল ঢাকে?", ["100 m²", "10 m²", "1,000 m²", "1 m²"],
        "ক্ষেত্রফল = আয়তন ÷ পুরুত্ব = 1 ÷ 0.01 = 100 m²।"),
    mcq("What is the median of grouped data used for?", ["Finding the middle value when data are in classes, using cumulative frequency", "Finding the largest value", "Finding the sum", "Finding the mode only"], 0,
        "Median = L + ((n/2 - cf) ÷ f) x h.",
        "শ্রেণিবদ্ধ তথ্যের মধ্যমা কীসের জন্য ব্যবহার হয়?", ["তথ্য শ্রেণিতে থাকলে ক্রমযোজিত পরিসংখ্যা দিয়ে মাঝের মান বের করতে", "সবচেয়ে বড় মান বের করতে", "যোগফল বের করতে", "শুধু ভূয়িষ্ঠক বের করতে"],
        "মধ্যমা = L + ((n/2 - cf) ÷ f) x h।"),
    mcq("Which average is best for 'the most common crack width' found in an inspection?", ["The mode", "The mean", "The range", "The median"], 0,
        "The mode is the value that appears most often.",
        "পরিদর্শনে পাওয়া 'সবচেয়ে সাধারণ ফাটলের চওড়া'-র জন্য কোন গড় সেরা?", ["ভূয়িষ্ঠক", "গড়", "পরিসর", "মধ্যমা"],
        "ভূয়িষ্ঠক হলো যে মান সবচেয়ে বেশিবার আসে।"),
    mcq("What is the empirical relationship between mean, median and mode for moderately skewed data?", ["Mode ≈ 3 median - 2 mean", "Mode = mean + median", "Mean = 2 x mode", "They are always equal"], 0,
        "It lets you estimate one average from the other two.",
        "মাঝারি বিষম তথ্যে গড়, মধ্যমা আর ভূয়িষ্ঠকের অভিজ্ঞতালব্ধ সম্পর্ক কী?", ["ভূয়িষ্ঠক ≈ 3 মধ্যমা - 2 গড়", "ভূয়িষ্ঠক = গড় + মধ্যমা", "গড় = 2 x ভূয়িষ্ঠক", "সবসময় সমান"],
        "অন্য দুটো থেকে একটা গড় আন্দাজ করতে দেয়।"),
    mcq("Euclid's division lemma: for positive integers a, b, there exist unique q, r with a = bq + r and:", ["0 ≤ r < b", "r > 0", "r ≥ b", "r = b"], 0,
        "HCF(96,72): 96=72×1+24, 72=24×3+0 → HCF=24. Used to find common cable cut-lengths.",
        "ইউক্লিডের বিভাজন উপপাদ্য: ধনাত্মক পূর্ণসংখ্যা a, b-এর জন্য a = bq + r আর:", ["0 ≤ r < b", "r > 0", "r ≥ b", "r = b"],
        "HCF(96,72): 96=72×1+24, 72=24×3+0 → HCF=24। সাধারণ কেবল-কাটার দৈর্ঘ্যে ব্যবহার।"),
    mcq("√2 is irrational because:", ["Its decimal expansion is non-terminating and non-repeating", "It is negative", "It has two values", "It is less than 1"], 0,
        "Proof by contradiction: assume √2 = p/q in lowest terms → p² = 2q² → p even → q even → contradiction.",
        "√2 অমূলদ কারণ:", ["এর দশমিক প্রকাশ অসান্ত ও অনাবৃত্ত", "এটা ঋণাত্মক", "এর দুটো মান আছে", "এটা 1-এর কম"],
        "বিরোধ প্রমাণ: √2 = p/q সরলতম আকারে ধরলে → p² = 2q² → p জোড় → q জোড় → বিরোধ।"),
    mcq("LCM(12, 18) × HCF(12, 18) equals:", ["216", "30", "6", "36"], 0,
        "LCM = 36, HCF = 6. Product = 36 × 6 = 216 = 12 × 18. LCM × HCF = product of the two numbers.",
        "LCM(12, 18) × HCF(12, 18) সমান:", ["216", "30", "6", "36"],
        "LCM = 36, HCF = 6। গুণফল = 36 × 6 = 216 = 12 × 18। LCM × HCF = দুটো সংখ্যার গুণফল।"),
    mcq("The decimal expansion 7/8 terminates because the denominator 8 equals:", ["2³ (only prime factor is 2)", "2 × 4", "A prime number", "3 × 2"], 0,
        "A fraction p/q terminates iff q = 2ᵐ × 5ⁿ. 7/8 = 0.875.",
        "7/8-এর দশমিক সান্ত কারণ হর 8 = ", ["2³ (একমাত্র মৌলিক গুণনীয়ক 2)", "2 × 4", "একটা মৌলিক সংখ্যা", "3 × 2"],
        "p/q সান্ত তখনই যখন q = 2ᵐ × 5ⁿ। 7/8 = 0.875।"),
    mcq("A quadratic polynomial has zeroes α and β. Which expression gives the polynomial?", ["x² - (α+β)x + αβ", "x² + (α+β)x - αβ", "x² - αβx + (α+β)", "(x-α) only"], 0,
        "Sum of zeroes = α+β = -b/a; product = αβ = c/a for ax²+bx+c.",
        "দ্বিঘাত বহুপদর শূন্য α ও β। কোন রাশি বহুপদটা দেয়?", ["x² - (α+β)x + αβ", "x² + (α+β)x - αβ", "x² - αβx + (α+β)", "শুধু (x-α)"],
        "শূন্যের যোগফল = α+β = -b/a; গুণফল = αβ = c/a, যেখানে ax²+bx+c।"),
    mcq("Solve 2x + 3y = 13 and 3x - y = 3 by elimination:", ["x = 2, y = 3", "x = 3, y = 2", "x = 1, y = 4", "x = 4, y = 0"], 0,
        "Multiply 2nd by 3: 9x-3y=9. Add to 1st: 11x=22→x=2; y=(13-4)/3=3.",
        "বিলোপ দ্বারা 2x + 3y = 13 ও 3x - y = 3 সমাধান:", ["x = 2, y = 3", "x = 3, y = 2", "x = 1, y = 4", "x = 4, y = 0"],
        "২য়কে 3 দিয়ে গুণ: 9x-3y=9। ১মের সাথে যোগ: 11x=22→x=2; y=3।"),
    mcq("The discriminant of x² - 4x + 5 = 0 is:", ["-4 (no real roots)", "36", "0", "4"], 0,
        "D = b²-4ac = 16-20 = -4 < 0 → no real roots. The bridge arch equation has no real crossing point with this line.",
        "x² - 4x + 5 = 0-এর বিভেদক:", ["-4 (কোনো বাস্তব মূল নেই)", "36", "0", "4"],
        "D = b²-4ac = 16-20 = -4 < 0 → কোনো বাস্তব মূল নেই।"),
    mcq("Solve 2x² - 5x - 3 = 0 by the quadratic formula:", ["x = 3 or x = -1/2", "x = 5 or x = -3", "x = 1 or x = 3", "x = -3 or x = 1/2"], 0,
        "D = 25+24 = 49; x = (5±7)/4 → x = 12/4 = 3 or x = -2/4 = -1/2.",
        "দ্বিঘাত সূত্রে 2x² - 5x - 3 = 0 সমাধান:", ["x = 3 অথবা x = -1/2", "x = 5 অথবা x = -3", "x = 1 অথবা x = 3", "x = -3 অথবা x = 1/2"],
        "D = 25+24 = 49; x = (5±7)/4 → x = 3 অথবা x = -1/2।"),
    mcq("By the Basic Proportionality Theorem, if DE ∥ BC in △ABC and AD = 3, DB = 6, then AE : EC =", ["1:2", "2:1", "3:6", "1:1"], 0,
        "AD/DB = AE/EC → 3/6 = AE/EC → AE:EC = 1:2.",
        "মৌলিক সমানুপাত উপপাদ্য: △ABC-এ DE ∥ BC, AD = 3, DB = 6 হলে AE : EC =", ["1:2", "2:1", "3:6", "1:1"],
        "AD/DB = AE/EC → 3/6 = AE/EC → AE:EC = 1:2।"),
    mcq("Two similar triangles have sides in ratio 3:5. What is the ratio of their areas?", ["9:25", "3:5", "6:10", "27:125"], 0,
        "Area ratio = (side ratio)² = (3/5)² = 9/25. Volume ratio would be (3/5)³ = 27/125.",
        "দুটো সদৃশ ত্রিভুজের বাহু 3:5 অনুপাতে। ক্ষেত্রফলের অনুপাত:", ["9:25", "3:5", "6:10", "27:125"],
        "ক্ষেত্রফলের অনুপাত = (বাহুর অনুপাত)² = (3/5)² = 9/25। আয়তনের অনুপাত (3/5)³ = 27/125।"),
    mcq("From an external point P, tangents PA = 8 cm and PB touch a circle. If the radius is 6 cm, how far is P from the centre O?", ["10 cm", "14 cm", "√28 cm", "6 cm"], 0,
        "OA ⊥ PA (radius⊥tangent); OA=6, PA=8; OP = √(6²+8²) = √100 = 10 cm (3-4-5 scaled).",
        "বাইরের বিন্দু P থেকে স্পর্শক PA = 8 cm, ব্যাসার্ধ 6 cm। কেন্দ্র O থেকে P কত দূরে?", ["10 cm", "14 cm", "√28 cm", "6 cm"],
        "OA ⊥ PA (ব্যাসার্ধ⊥স্পর্শক); OA=6, PA=8; OP = √(36+64) = 10 cm।"),
    mcq("sin 60° equals:", ["√3/2", "1/2", "1/√2", "1"], 0,
        "sin 60° = √3/2 ≈ 0.866. In a 30-60-90 triangle: sides 1:√3:2 (shortest:middle:hypotenuse).",
        "sin 60° সমান:", ["√3/2", "1/2", "1/√2", "1"],
        "sin 60° = √3/2 ≈ 0.866। 30-60-90 ত্রিভুজে বাহু 1:√3:2 (ক্ষুদ্রতম:মধ্য:অতিভুজ)।"),
    mcq("sin(90°-θ) = cosθ is called a:", ["Complementary angle identity", "Pythagorean identity", "Sum identity", "Double angle formula"], 0,
        "Complementary identities: sin(90°-θ)=cosθ, cos(90°-θ)=sinθ, tan(90°-θ)=cotθ.",
        "sin(90°-θ) = cosθ কে বলা হয়:", ["পূরক কোণের অভেদ", "পিথাগোরিয়ান অভেদ", "যোগফল অভেদ", "দ্বিগুণ কোণ সূত্র"],
        "পূরক অভেদ: sin(90°-θ)=cosθ, cos(90°-θ)=sinθ, tan(90°-θ)=cotθ।"),
    mcq("A tower casts a shadow 40 m long when the sun's angle of elevation is 30°. Height of tower?", ["40/√3 ≈ 23.1 m", "40√3 ≈ 69.3 m", "40 m", "20 m"], 0,
        "tan 30° = h/40 → h = 40 × (1/√3) = 40/√3 ≈ 23.1 m.",
        "সূর্যের উন্নতি কোণ 30° হলে টাওয়ার 40 m ছায়া ফেলে। টাওয়ারের উচ্চতা?", ["40/√3 ≈ 23.1 m", "40√3 ≈ 69.3 m", "40 m", "20 m"],
        "tan 30° = h/40 → h = 40/√3 ≈ 23.1 m।"),
    mcq("Volume of a frustum with radii r₁, r₂ and height h:", ["(πh/3)(r₁² + r₂² + r₁r₂)", "π(r₁+r₂)h", "(π/3)(r₁² + r₂²)h", "πr₁r₂h/3"], 0,
        "Used for tapered concrete pile heads (frustum) - difference between the two cone volumes.",
        "r₁, r₂ ব্যাসার্ধ ও h উচ্চতার ছিন্নশঙ্কুর আয়তন:", ["(πh/3)(r₁² + r₂² + r₁r₂)", "π(r₁+r₂)h", "(π/3)(r₁² + r₂²)h", "πr₁r₂h/3"],
        "শঙ্কু-আকৃতির কংক্রিট পাইল হেডে ব্যবহার হয় - দুটো শঙ্কুর আয়তনের পার্থক্য।"),
    mcq("What is the probability that a card drawn at random from a standard 52-card deck is a king?", ["4/52 = 1/13", "4/13", "1/4", "1/52"], 0,
        "4 kings in 52 cards. P = 4/52 = 1/13. Risk assessment in engineering uses similar ratio calculations.",
        "52-তাসের প্যাকেট থেকে এলোমেলো তোলা তাস রাজা হওয়ার সম্ভাবনা:", ["4/52 = 1/13", "4/13", "1/4", "1/52"],
        "52 তাসে 4 রাজা। P = 4/52 = 1/13। প্রকৌশলে ঝুঁকি মূল্যায়নেও এমন অনুপাত গণনা হয়।"),
    mcq("A bag has 5 white and 3 black balls. A ball is drawn and NOT replaced, then a second is drawn. P(both white) =", ["5/14", "25/64", "10/56", "8/21"], 0,
        "P = (5/8) × (4/7) = 20/56 = 5/14. Without replacement changes the second probability.",
        "থলিতে 5 সাদা ও 3 কালো বল। একটা তুলে না রেখে দ্বিতীয়টা তোলা হল। P(দুটোই সাদা) =", ["5/14", "25/64", "10/56", "8/21"],
        "P = (5/8) × (4/7) = 20/56 = 5/14। না রাখলে দ্বিতীয় সম্ভাবনা বদলায়।"),
    mcq("The nth term of the GP 2, 6, 18, 54,... is:", ["2 × 3^(n-1)", "3 × 2^(n-1)", "2n × 3", "6^(n-1)"], 0,
        "First term a=2, ratio r=3. Tₙ = ar^(n-1) = 2×3^(n-1).",
        "2, 6, 18, 54,... গুণোত্তর প্রগতির n-তম পদ:", ["2 × 3^(n-1)", "3 × 2^(n-1)", "2n × 3", "6^(n-1)"],
        "প্রথম পদ a=2, অনুপাত r=3। Tₙ = ar^(n-1) = 2×3^(n-1)।"),
    mcq("Find the sum of first 10 terms of AP: 3, 7, 11,...", ["210", "120", "185", "143"], 0,
        "a=3, d=4. S₁₀ = (10/2)(2×3 + 9×4) = 5(6+36) = 5×42 = 210.",
        "3, 7, 11,... AP-এর প্রথম 10 পদের যোগফল:", ["210", "120", "185", "143"],
        "a=3, d=4। S₁₀ = (10/2)(2×3 + 9×4) = 5×42 = 210।"),
    mcq("The 10th term of an AP is 52 and the 3rd term is 17. Find the common difference:", ["5", "7", "4", "3"], 0,
        "T₁₀ - T₃ = 7d = 52-17 = 35 → d = 5.",
        "AP-এর 10ম পদ 52 ও 3য় পদ 17। সাধারণ অন্তর:", ["5", "7", "4", "3"],
        "T₁₀ - T₃ = 7d = 52-17 = 35 → d = 5।"),
    mcq("The area of a triangle with vertices at (1,0), (6,0) and (4,3) using coordinates is:", ["7.5 sq units", "15 sq units", "10 sq units", "6 sq units"], 0,
        "Area = ½|1(0-3)+6(3-0)+4(0-0)| = ½|−3+18+0| = ½×15 = 7.5.",
        "(1,0), (6,0) ও (4,3) শীর্ষের ত্রিভুজের ক্ষেত্রফল:", ["7.5 বর্গ একক", "15 বর্গ একক", "10 বর্গ একক", "6 বর্গ একক"],
        "ক্ষেত্রফল = ½|1(0-3)+6(3-0)+4(0-0)| = ½×15 = 7.5।"),
    mcq("P divides AB in ratio 2:3 where A = (1,2) and B = (6,7). Coordinates of P?", ["(3, 4)", "(4, 5)", "(2, 3)", "(5, 6)"], 0,
        "Section formula: P = ((2×6+3×1)/(2+3), (2×7+3×2)/(2+3)) = (15/5, 20/5) = (3,4).",
        "A = (1,2) ও B = (6,7) সংযোজক রেখাকে P 2:3 অনুপাতে বিভক্ত করে। P-এর স্থানাঙ্ক?", ["(3, 4)", "(4, 5)", "(2, 3)", "(5, 6)"],
        "বিভাজন সূত্র: P = ((2×6+3×1)/5, (2×7+3×2)/5) = (15/5, 20/5) = (3,4)।"),
    mcq("The equation of a line with slope 2 passing through (1, 3) is:", ["y = 2x + 1", "y = 2x + 3", "y = 3x + 1", "y = 2x - 1"], 0,
        "y - y₁ = m(x - x₁) → y - 3 = 2(x-1) → y = 2x + 1.",
        "ঢাল 2 এবং (1, 3) দিয়ে যাওয়া রেখার সমীকরণ:", ["y = 2x + 1", "y = 2x + 3", "y = 3x + 1", "y = 2x - 1"],
        "y - y₁ = m(x - x₁) → y - 3 = 2(x-1) → y = 2x + 1।"),
    mcq("The volume of a sphere of radius 7 cm is: (π = 22/7)", ["1437.3 cm³ ≈ (4/3)×(22/7)×343", "308 cm³", "616 cm³", "2156 cm³"], 0,
        "V = (4/3)πr³ = (4/3)×(22/7)×343 = 4×22×49/3 = 4312/3 ≈ 1437.3 cm³.",
        "7 cm ব্যাসার্ধের গোলকের আয়তন: (π = 22/7)", ["1437.3 cm³ ≈ (4/3)×(22/7)×343", "308 cm³", "616 cm³", "2156 cm³"],
        "V = (4/3)×(22/7)×343 = 4312/3 ≈ 1437.3 cm³।"),
    mcq("Curved surface area of a cylinder (radius r, height h):", ["2πrh", "2πr(r+h)", "πr²h", "πrh²"], 0,
        "CSA = 2πrh (label area only); Total SA = 2πr(r+h). A cylindrical pier of r=1m, h=5m: CSA = 2π×1×5 ≈ 31.4 m².",
        "সিলিন্ডারের পার্শ্বতল ক্ষেত্রফল (ব্যাসার্ধ r, উচ্চতা h):", ["2πrh", "2πr(r+h)", "πr²h", "πrh²"],
        "পার্শ্বতল = 2πrh; মোট তল ক্ষেত্র = 2πr(r+h)। r=1m, h=5m স্তম্ভ: পার্শ্বতল ≈ 31.4 m²।"),
    mcq("In a class of 30 students, the probability of randomly choosing a girl is 2/5. How many boys?", ["18", "12", "15", "20"], 0,
        "Girls = 30 × 2/5 = 12. Boys = 30 - 12 = 18.",
        "30 জনের ক্লাসে এলোমেলো মেয়ে বেছে নেওয়ার সম্ভাবনা 2/5। ছেলে কতজন?", ["18", "12", "15", "20"],
        "মেয়ে = 30 × 2/5 = 12। ছেলে = 30 - 12 = 18।"),
    mcq("P(A ∪ B) = P(A) + P(B) - P(A ∩ B). If P(A)=0.5, P(B)=0.4, P(A∩B)=0.2, find P(A∪B):", ["0.7", "0.9", "0.3", "1.1"], 0,
        "P(A∪B) = 0.5+0.4-0.2 = 0.7. Addition rule of probability for non-mutually exclusive events.",
        "P(A)=0.5, P(B)=0.4, P(A∩B)=0.2 হলে P(A∪B):", ["0.7", "0.9", "0.3", "1.1"],
        "P(A∪B) = 0.5+0.4-0.2 = 0.7। পরস্পর-বর্জনীয় নয় এমন ঘটনার যোগ নিয়ম।"),
    mcq("The perimeter of a sector with radius 10 cm and angle 60° is: (π ≈ 3.14)", ["30.47 cm", "20 cm", "62.8 cm", "10.47 cm"], 0,
        "Arc length = (60/360)×2π×10 = (1/6)×62.8 ≈ 10.47; Perimeter = 10+10+10.47 = 30.47 cm.",
        "ব্যাসার্ধ 10 cm ও কোণ 60°-এর বৃত্তকলার পরিসীমা: (π ≈ 3.14)", ["30.47 cm", "20 cm", "62.8 cm", "10.47 cm"],
        "চাপ = (60/360)×2π×10 ≈ 10.47; পরিসীমা = 10+10+10.47 = 30.47 cm।"),
    mcq("What is (1+tan²θ) equal to (Pythagorean identity)?", ["sec²θ", "cosec²θ", "1", "cot²θ + 1"], 0,
        "1+tan²θ = sec²θ. Also: 1+cot²θ = cosec²θ. Derived from sin²θ+cos²θ=1 by dividing.",
        "(1+tan²θ) কীসের সমান?", ["sec²θ", "cosec²θ", "1", "cot²θ + 1"],
        "1+tan²θ = sec²θ। এছাড়া 1+cot²θ = cosec²θ। sin²θ+cos²θ=1 থেকে ভাগ করে পাওয়া।"),
    mcq("The slope of a line that makes an angle of 45° with the positive x-axis is:", ["1", "0", "∞ (undefined)", "√3"], 0,
        "m = tan θ = tan 45° = 1. A 45° ramp has a gradient of 1 (1 unit rise per 1 unit run).",
        "ধনাত্মক x-অক্ষের সাথে 45° কোণ করা রেখার ঢাল:", ["1", "0", "∞ (অনির্ধারিত)", "√3"],
        "m = tan θ = tan 45° = 1। 45° র‍্যাম্পের গ্রেডিয়েন্ট 1 (1 একক বৃদ্ধিতে 1 একক দৌড়)।"),
    mcq("The coordinates of the centroid of △ with vertices A(1,2), B(3,4) and C(5,0) are:", ["(3, 2)", "(4, 3)", "(2, 2)", "(3, 3)"], 0,
        "Centroid = ((x₁+x₂+x₃)/3, (y₁+y₂+y₃)/3) = ((1+3+5)/3, (2+4+0)/3) = (3, 2).",
        "A(1,2), B(3,4) ও C(5,0) শীর্ষের ত্রিভুজের ভরকেন্দ্র:", ["(3, 2)", "(4, 3)", "(2, 2)", "(3, 3)"],
        "ভরকেন্দ্র = ((x₁+x₂+x₃)/3, (y₁+y₂+y₃)/3) = ((1+3+5)/3, (2+4+0)/3) = (3, 2)।"),
    mcq("If 3x - 4y + 12 = 0 is a line, what are its x and y intercepts?", ["x-intercept = -4, y-intercept = 3", "x-intercept = 4, y-intercept = -3", "x-intercept = 3, y-intercept = -4", "Both intercepts = 12"], 0,
        "x-intercept (y=0): 3x=−12→x=−4; y-intercept (x=0): −4y=−12→y=3.",
        "3x - 4y + 12 = 0 রেখার x ও y অন্তখণ্ড কত?", ["x-অন্তখণ্ড = -4, y-অন্তখণ্ড = 3", "x-অন্তখণ্ড = 4, y-অন্তখণ্ড = -3", "x-অন্তখণ্ড = 3, y-অন্তখণ্ড = -4", "দুটো অন্তখণ্ড = 12"],
        "x-অন্তখণ্ড (y=0): 3x=−12→x=−4; y-অন্তখণ্ড (x=0): −4y=−12→y=3।"),
    mcq("A rectangle is 3 times as long as it is wide. If the diagonal is 10 cm, find the width:", ["√10 cm", "3 cm", "√(10/10) cm", "5 cm"], 0,
        "Let width=w, length=3w. w²+(3w)²=100 → 10w²=100 → w²=10 → w=√10 cm.",
        "আয়তক্ষেত্রের দৈর্ঘ্য প্রস্থের 3 গুণ। কর্ণ 10 cm হলে প্রস্থ:", ["√10 cm", "3 cm", "√(10/10) cm", "5 cm"],
        "প্রস্থ=w, দৈর্ঘ্য=3w। w²+(3w)²=100 → 10w²=100 → w=√10 cm।"),
)
