"""Class 7 - Math (Junior Cadet): simultaneous equations, expanding and factorising, trigonometry
(SOH CAH TOA) for truss members and ramps, similar shapes and scale factors, gradients between
points, arcs and sectors, error intervals, probability trees and standard form - all with bridges."""
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


def _c(x):
    return int(x) if x == int(x) else round(x, 2)


def _lin(a, b):
    t1 = "x" if a == 1 else f"{a}x"
    t2 = ("+ y" if b == 1 else "- y" if b == -1 else f"+ {b}y" if b > 0 else f"- {-b}y")
    return f"{t1} {t2}"


def simul(x, y, a, b, c, d):
    e1, e2 = a * x + b * y, c * x + d * y
    L1, L2 = _lin(a, b), _lin(c, d)
    o = [f"x = {x}, y = {y}", f"x = {y}, y = {x}", f"x = {x + 1}, y = {y - 1}", f"x = {x - 1}, y = {y + 2}"]
    return mcq(f"Solve together: {L1} = {e1} and {L2} = {e2}.", o, 0,
               f"Eliminate one letter, solve for the other, then substitute back: x = {x}, y = {y}. Check the first: {a} x {x} + ({b}) x {y} = {e1}.",
               f"একসঙ্গে সমাধান করো: {L1} = {e1} আর {L2} = {e2}।", o,
               f"একটা অক্ষর বাদ দাও, অন্যটা বের করো, তারপর বসাও: x = {x}, y = {y}। প্রথমটা যাচাই: {a} x {x} + ({b}) x {y} = {e1}।")


def trig_opp(hyp, angle, what_en, what_bn):
    s = {30: 0.5, 90: 1}[angle]
    r = _c(hyp * s)
    return _n(f"{what_en} is {hyp} m long and makes {angle}° with the ground. How high does its top reach? (sin {angle}° = {s:g})",
              f"{what_bn} {hyp} m লম্বা আর মাটির সঙ্গে {angle}° কোণ করে। মাথা কত উঁচুতে পৌঁছায়? (sin {angle}° = {s:g})", r,
              f"Opposite = hypotenuse x sin θ = {hyp} x {s:g} = {r:g} m.",
              f"বিপরীত বাহু = অতিভুজ x sin θ = {hyp} x {s:g} = {r:g} m।",
              (hyp, _c(hyp * 0.87), _c(hyp * 2)), " m")


def trig_adj(hyp, angle, what_en, what_bn):
    c = {60: 0.5}[angle]
    r = _c(hyp * c)
    return _n(f"{what_en} is {hyp} m long at {angle}° to the horizontal. How far does it reach horizontally? (cos {angle}° = {c:g})",
              f"{what_bn} {hyp} m লম্বা, অনুভূমিকের সঙ্গে {angle}°। অনুভূমিকভাবে কত দূর পৌঁছায়? (cos {angle}° = {c:g})", r,
              f"Adjacent = hypotenuse x cos θ = {hyp} x {c:g} = {r:g} m.",
              f"সন্নিহিত বাহু = অতিভুজ x cos θ = {hyp} x {c:g} = {r:g} m।",
              (hyp, _c(hyp * 0.87), _c(hyp / 0.5 if hyp < 50 else hyp + 5)), " m")


def trig_tan(adj, what_en, what_bn):
    r = adj  # tan 45 = 1
    return _n(f"{what_en}: you stand {adj} m from its base and look up to the top at 45°. How tall is it? (tan 45° = 1)",
              f"{what_bn}: তুমি গোড়া থেকে {adj} m দূরে দাঁড়িয়ে 45°-এ মাথার দিকে তাকাও। কত উঁচু? (tan 45° = 1)", r,
              f"Opposite = adjacent x tan θ = {adj} x 1 = {adj} m.",
              f"বিপরীত বাহু = সন্নিহিত x tan θ = {adj} x 1 = {adj} m।",
              (adj * 2, _c(adj * 0.71), adj + 45), " m")


def similar(k, a1, what_en, what_bn):
    a2 = a1 * k * k
    return _n(f"A bridge model is scaled up by a length factor of {k}. A panel on the model has an area of {a1} m². What is the area on the real bridge?",
              f"একটা সেতুর মডেল দৈর্ঘ্যে {k} গুণ বড় করা হলো। মডেলের একটা প্যানেলের ক্ষেত্রফল {a1} m²। আসল সেতুতে ক্ষেত্রফল কত?", a2,
              f"Area scales by k² = {k}² = {k * k}: {a1} x {k * k} = {a2} m². (Length factor alone gives the wrong {a1 * k}.)",
              f"ক্ষেত্রফল k² = {k}² = {k * k} গুণ বাড়ে: {a1} x {k * k} = {a2} m²। (শুধু দৈর্ঘ্যের গুণক দিলে ভুল {a1 * k} হয়।)",
              (a1 * k, a1 * k ** 3, a1 + k), " m²")


def grad(x1, y1, x2, y2):
    g = _c((y2 - y1) / (x2 - x1))
    alts = [g, -g, _c((x2 - x1) / (y2 - y1)), y2 - y1, g + 1]
    o = []
    for v in alts:
        if v not in o:
            o.append(v)
    o = [f"{v:g}" for v in o[:4]]
    return mcq(f"What is the gradient of the line through ({x1}, {y1}) and ({x2}, {y2})?", o, 0,
               f"Gradient = change in y ÷ change in x = ({y2} - {y1}) ÷ ({x2} - {x1}) = {g:g}." + (" A negative gradient slopes downhill." if g < 0 else ""),
               f"({x1}, {y1}) আর ({x2}, {y2}) বিন্দুগামী রেখার নতি কত?", o,
               f"নতি = y-এর পরিবর্তন ÷ x-এর পরিবর্তন = ({y2} - {y1}) ÷ ({x2} - {x1}) = {g:g}।" + (" ঋণাত্মক নতি নিচের দিকে ঢালু।" if g < 0 else ""))


def arc(r_, ang, what_en, what_bn):
    L = _c(2 * 22 * r_ * ang / (7 * 360))
    return _n(f"{what_en} is an arc of a circle of radius {r_} m with angle {ang}°. Using π = 22/7, how long is the arc?",
              f"{what_bn} {r_} m ব্যাসার্ধের বৃত্তের {ang}° কোণের একটা বৃত্তচাপ। π = 22/7 ধরে চাপের দৈর্ঘ্য কত?", L,
              f"Arc = (θ ÷ 360) x 2πr = ({ang} ÷ 360) x 2 x 22/7 x {r_} = {L:g} m.",
              f"চাপ = (θ ÷ 360) x 2πr = ({ang} ÷ 360) x 2 x 22/7 x {r_} = {L:g} m।",
              (_c(L * 2), _c(22 * r_ * r_ * ang / (7 * 360)), _c(2 * 22 * r_ / 7)), " m")


ITEMS = (
    simul(3, 2, 2, 1, 1, 1), simul(5, 1, 1, 2, 2, 1), simul(4, 3, 3, 2, 1, -1), simul(2, 6, 4, 1, 1, 3), simul(7, 2, 1, 1, 2, -3),
    trig_opp(10, 30, "A ramp", "একটা ঢাল"), trig_opp(24, 30, "A crane jib", "একটা ক্রেনের বাহু"),
    trig_opp(16, 30, "A truss diagonal", "একটা ট্রাসের কর্ণ"), trig_opp(50, 30, "A cable-stay", "একটা ঝোলানো তার"),
    trig_adj(20, 60, "A sloping strut", "একটা হেলানো ঠেকনা"), trig_adj(12, 60, "A ladder", "একটা মই"), trig_adj(30, 60, "A cable", "একটা তার"),
    trig_tan(25, "A bridge tower", "একটা সেতুর টাওয়ার"), trig_tan(40, "A pylon", "একটা খুঁটি-স্তম্ভ"), trig_tan(12, "A lamp post", "একটা ল্যাম্পপোস্ট"),
    similar(2, 3, "", ""), similar(3, 4, "", ""), similar(5, 2, "", ""), similar(10, 1, "", ""),
    grad(1, 2, 3, 8), grad(0, 5, 4, 7), grad(2, 10, 6, 2), grad(-1, 1, 3, 9), grad(0, 0, 50, 2),
    arc(7, 90, "A curved footbridge edge", "একটা বাঁকা হাঁটার সেতুর কিনারা"),
    arc(14, 180, "A semicircular arch", "একটা অর্ধবৃত্তাকার খিলান"),
    arc(21, 60, "A curved road on a bridge approach", "সেতুর সংযোগপথের একটা বাঁকা রাস্তা"),
    mcq("Expand (x + 3)(x + 5).", ["x² + 8x + 15", "x² + 15x + 8", "x² + 8", "2x + 8"], 0,
        "x x x + 5x + 3x + 15 = x² + 8x + 15.",
        "বিস্তার করো: (x + 3)(x + 5)।", ["x² + 8x + 15", "x² + 15x + 8", "x² + 8", "2x + 8"],
        "x x x + 5x + 3x + 15 = x² + 8x + 15।"),
    mcq("Expand (x - 4)(x + 2).", ["x² - 2x - 8", "x² + 2x - 8", "x² - 6x + 8", "x² - 8"], 0,
        "x² + 2x - 4x - 8 = x² - 2x - 8.",
        "বিস্তার করো: (x - 4)(x + 2)।", ["x² - 2x - 8", "x² + 2x - 8", "x² - 6x + 8", "x² - 8"],
        "x² + 2x - 4x - 8 = x² - 2x - 8।"),
    mcq("Factorise x² + 7x + 12.", ["(x + 3)(x + 4)", "(x + 2)(x + 6)", "(x + 12)(x + 1)", "(x - 3)(x - 4)"], 0,
        "Find two numbers that multiply to 12 and add to 7: 3 and 4.",
        "উৎপাদকে বিশ্লেষণ করো: x² + 7x + 12।", ["(x + 3)(x + 4)", "(x + 2)(x + 6)", "(x + 12)(x + 1)", "(x - 3)(x - 4)"],
        "এমন দুটি সংখ্যা খোঁজো যাদের গুণফল 12 আর যোগফল 7: 3 আর 4।"),
    mcq("Solve x² - 9 = 0.", ["x = 3 or x = -3", "x = 9", "x = 3 only", "x = 81"], 0,
        "x² = 9, so x = ±3.",
        "সমাধান করো: x² - 9 = 0।", ["x = 3 বা x = -3", "x = 9", "শুধু x = 3", "x = 81"],
        "x² = 9, তাই x = ±3।"),
    mcq("Solve x² - 5x + 6 = 0.", ["x = 2 or x = 3", "x = -2 or x = -3", "x = 6", "x = 5"], 0,
        "(x - 2)(x - 3) = 0.",
        "সমাধান করো: x² - 5x + 6 = 0।", ["x = 2 বা x = 3", "x = -2 বা x = -3", "x = 6", "x = 5"],
        "(x - 2)(x - 3) = 0।"),
    mcq("A rectangular deck is x m wide and (x + 4) m long with area 60 m². What is x?", ["6", "10", "4", "15"], 0,
        "x(x + 4) = 60 -> x² + 4x - 60 = 0 -> (x + 10)(x - 6) = 0; width is positive, so x = 6.",
        "একটা আয়তাকার পাটাতন x m চওড়া আর (x + 4) m লম্বা, ক্ষেত্রফল 60 m²। x কত?", ["6", "10", "4", "15"],
        "x(x + 4) = 60 -> x² + 4x - 60 = 0 -> (x + 10)(x - 6) = 0; প্রস্থ ধনাত্মক, তাই x = 6।"),
    mcq("What does SOH CAH TOA help you remember?", ["sin = opp/hyp, cos = adj/hyp, tan = opp/adj", "Order of operations", "Area formulas", "Angles in a circle"], 0,
        "Trigonometry links angles and side lengths in right-angled triangles.",
        "SOH CAH TOA কী মনে রাখতে সাহায্য করে?", ["sin = বিপরীত/অতিভুজ, cos = সন্নিহিত/অতিভুজ, tan = বিপরীত/সন্নিহিত", "গণনার ক্রম", "ক্ষেত্রফলের সূত্র", "বৃত্তের কোণ"],
        "ত্রিকোণমিতি সমকোণী ত্রিভুজে কোণ আর বাহুর দৈর্ঘ্য জোড়ে।"),
    mcq("In a right-angled triangle the side opposite the right angle is called the...", ["Hypotenuse", "Adjacent", "Opposite", "Base only"], 0,
        "It is always the longest side.",
        "সমকোণী ত্রিভুজে সমকোণের বিপরীত বাহুকে বলে...", ["অতিভুজ", "সন্নিহিত", "বিপরীত", "শুধু ভূমি"],
        "এটা সবসময় সবচেয়ে লম্বা বাহু।"),
    mcq("What is tan 45°?", ["1", "0.5", "0.71", "0"], 0,
        "In a 45° right triangle, opposite = adjacent.",
        "tan 45° কত?", ["1", "0.5", "0.71", "0"],
        "45°-এর সমকোণী ত্রিভুজে বিপরীত = সন্নিহিত।"),
    mcq("A ramp rises 3 m over a horizontal 4 m. Its sloping length is...", ["5 m", "7 m", "1 m", "12 m"], 0,
        "3-4-5 triangle.",
        "একটা ঢাল অনুভূমিক 4 m-এ 3 m ওঠে। ঢালু দৈর্ঘ্য...", ["5 m", "7 m", "1 m", "12 m"],
        "3-4-5 ত্রিভুজ।"),
    mcq("If sin θ = 0.5, what is θ?", ["30°", "45°", "60°", "90°"], 0,
        "sin 30° = 0.5.",
        "sin θ = 0.5 হলে θ কত?", ["30°", "45°", "60°", "90°"],
        "sin 30° = 0.5, তাই θ = 30°।"),
    mcq("Two shapes are 'similar'. What does that mean?", ["Same shape, possibly different size, with equal angles", "Same size exactly", "Same colour", "Any two triangles"], 0,
        "Models of bridges are similar to the real bridges.",
        "দুটি আকার 'সদৃশ'। এর মানে কী?", ["একই আকার, মাপ আলাদা হতে পারে, কোণগুলো সমান", "একদম একই মাপ", "একই রং", "যেকোনো দুটি ত্রিভুজ"],
        "সেতুর মডেল আসল সেতুর সদৃশ।"),
    mcq("A model is 1/50 of real size. A real beam is 25 m. How long is it on the model?", ["0.5 m", "1,250 m", "2 m", "50 m"], 0,
        "25 ÷ 50 = 0.5 m.",
        "একটা মডেল আসলের 1/50। আসল বিম 25 m। মডেলে কত লম্বা?", ["0.5 m", "1,250 m", "2 m", "50 m"],
        "25 ÷ 50 = 0.5 m।"),
    mcq("If a model's lengths are scaled up by 4, by what factor does volume (and so weight of the same material) grow?", ["64", "16", "4", "12"], 0,
        "Volume scales by k³ = 4³ = 64 - big bridges get heavy fast!",
        "মডেলের দৈর্ঘ্য 4 গুণ বাড়ালে আয়তন (আর একই উপাদানে ওজন) কত গুণ বাড়ে?", ["64", "16", "4", "12"],
        "আয়তন k³ = 4³ = 64 গুণ - বড় সেতু দ্রুত ভারী হয়!"),
    mcq("Why can't you just build a giant version of a working model bridge?", ["Weight grows with length cubed but strength only with length squared", "Models are always wrong", "Giant bridges are illegal", "You always can"], 0,
        "The square-cube law - bigger structures need proportionally stronger designs.",
        "কাজ করা মডেল সেতুর হুবহু বিশাল সংস্করণ বানানো যায় না কেন?", ["ওজন দৈর্ঘ্যের ঘনের সঙ্গে বাড়ে কিন্তু শক্তি শুধু দৈর্ঘ্যের বর্গের সঙ্গে", "মডেল সবসময় ভুল", "বিশাল সেতু বেআইনি", "সবসময় যায়"],
        "বর্গ-ঘন সূত্র - বড় কাঠামোয় আনুপাতিক হারে শক্ত নকশা লাগে।"),
    mcq("A length is 6.4 m to 1 decimal place. What is the error interval?", ["6.35 ≤ L < 6.45", "6.3 ≤ L < 6.5", "6.4 ≤ L < 6.5", "6 ≤ L < 7"], 0,
        "Half a unit of the last place either side.",
        "একটা দৈর্ঘ্য 1 দশমিক স্থানে 6.4 m। ত্রুটির ব্যবধান কত?", ["6.35 ≤ L < 6.45", "6.3 ≤ L < 6.5", "6.4 ≤ L < 6.5", "6 ≤ L < 7"],
        "শেষ স্থানের অর্ধেক একক দুই দিকে।"),
    mcq("Why do engineers care about 'tolerances'?", ["Parts made slightly too big or small may not fit or carry load", "To be tolerant of mistakes", "To slow work", "Tolerances do not matter"], 0,
        "Steel parts might be specified as 3,000 mm ± 2 mm.",
        "প্রকৌশলীরা 'সহনসীমা' নিয়ে ভাবেন কেন?", ["সামান্য বড় বা ছোট অংশ না আঁটতে বা বোঝা না বইতে পারে", "ভুল সহ্য করতে", "কাজ ধীর করতে", "সহনসীমা জরুরি নয়"],
        "ইস্পাতের অংশ 3,000 mm ± 2 mm বলে নির্দিষ্ট করা হতে পারে।"),
    mcq("Write 0.00045 in standard form.", ["4.5 x 10^-4", "4.5 x 10^4", "45 x 10^-5", "0.45 x 10^-3"], 0,
        "Move the point 4 places right.",
        "0.00045-কে আদর্শ রূপে লেখো।", ["4.5 x 10^-4", "4.5 x 10^4", "45 x 10^-5", "0.45 x 10^-3"],
        "দশমিক বিন্দু 4 ঘর ডানে সরাও।"),
    mcq("What is (3 x 10^5) x (2 x 10^3)?", ["6 x 10^8", "6 x 10^15", "5 x 10^8", "6 x 10^2"], 0,
        "Multiply the numbers, add the powers.",
        "(3 x 10^5) x (2 x 10^3) কত?", ["6 x 10^8", "6 x 10^15", "5 x 10^8", "6 x 10^2"],
        "সংখ্যা গুণ করো, ঘাত যোগ করো।"),
    mcq("Simplify a³ x a⁴.", ["a⁷", "a¹²", "2a⁷", "a"], 0,
        "Add powers when multiplying the same base.",
        "সরল করো: a³ x a⁴।", ["a⁷", "a¹²", "2a⁷", "a"],
        "একই ভিত্তি গুণ করলে ঘাত যোগ হয়।"),
    mcq("What is 2⁰?", ["1", "0", "2", "20"], 0,
        "Any non-zero number to the power 0 is 1.",
        "2⁰ কত?", ["1", "0", "2", "20"],
        "শূন্য ছাড়া যেকোনো সংখ্যার ঘাত 0 হলে মান 1।"),
    mcq("A bag has 4 good and 1 faulty bolt. Two are taken without replacement. Probability both are good?", ["3/5", "16/25", "4/5", "1/5"], 0,
        "4/5 x 3/4 = 12/20 = 3/5.",
        "একটা ব্যাগে 4টি ভালো আর 1টি ত্রুটিপূর্ণ বল্টু। ফেরত না দিয়ে দুটো তোলা হলো। দুটোই ভালো হওয়ার সম্ভাবনা?", ["3/5", "16/25", "4/5", "1/5"],
        "4/5 x 3/4 = 12/20 = 3/5।"),
    mcq("The chance a delivery is late is 0.2 each day, independently. What is the chance two days in a row are both late?", ["0.04", "0.4", "0.2", "0.02"], 0,
        "Multiply for independent events: 0.2 x 0.2.",
        "প্রতিদিন ডেলিভারি দেরি হওয়ার সম্ভাবনা 0.2, স্বাধীনভাবে। পরপর দুদিনই দেরির সম্ভাবনা কত?", ["0.04", "0.4", "0.2", "0.02"],
        "স্বাধীন ঘটনায় গুণ করো: 0.2 x 0.2।"),
    mcq("What is the sum of exterior angles of any polygon?", ["360°", "180°", "540°", "It depends on sides"], 0,
        "Walk around any shape and you turn once.",
        "যেকোনো বহুভুজের বহিঃকোণগুলোর যোগফল কত?", ["360°", "180°", "540°", "বাহুর উপর নির্ভর করে"],
        "যেকোনো আকারের চারপাশে হাঁটলে একবার পুরো ঘোরো।"),
    mcq("A regular polygon has exterior angles of 45°. How many sides?", ["8", "6", "45", "4"], 0,
        "360 ÷ 45 = 8 - an octagon.",
        "একটা সুষম বহুভুজের বহিঃকোণ 45°। কয়টি বাহু?", ["8", "6", "45", "4"],
        "360 ÷ 45 = 8 - অষ্টভুজ।"),
    mcq("A bearing from A to B is 060°. What is the bearing from B back to A?", ["240°", "060°", "300°", "120°"], 0,
        "Add 180°: 60 + 180 = 240°.",
        "A থেকে B-র দিগংশ 060°। B থেকে A-তে ফেরার দিগংশ কত?", ["240°", "060°", "300°", "120°"],
        "180° যোগ করো: 60 + 180 = 240°।"),
    mcq("A sector has radius 6 m and angle 60°. Using π ≈ 3.14, what is its area?", ["18.84 m²", "37.68 m²", "6.28 m²", "113.04 m²"], 0,
        "(60 ÷ 360) x 3.14 x 36 = 18.84 m².",
        "একটা বৃত্তকলার ব্যাসার্ধ 6 m আর কোণ 60°। π ≈ 3.14 ধরে ক্ষেত্রফল কত?", ["18.84 m²", "37.68 m²", "6.28 m²", "113.04 m²"],
        "(60 ÷ 360) x 3.14 x 36 = 18.84 m²।"),
    mcq("What is the volume of a cone with base area 30 m² and height 9 m?", ["90 m³", "270 m³", "39 m³", "30 m³"], 0,
        "Cone = ⅓ x base area x height = ⅓ x 30 x 9 = 90 m³ - like a pile of sand.",
        "ভূমির ক্ষেত্রফল 30 m² আর উচ্চতা 9 m-এর শঙ্কুর আয়তন কত?", ["90 m³", "270 m³", "39 m³", "30 m³"],
        "শঙ্কু = ⅓ x ভূমির ক্ষেত্রফল x উচ্চতা = ⅓ x 30 x 9 = 90 m³ - বালির ঢিবির মতো।"),
    mcq("A sand pile is a cone with base area 12 m² and height 3 m. Sand weighs 1.6 t per m³. About how heavy is it?", ["19.2 tonnes", "57.6 tonnes", "12 tonnes", "6.4 tonnes"], 0,
        "Volume = ⅓ x 12 x 3 = 12 m³; x 1.6 = 19.2 t.",
        "একটা বালির ঢিবি শঙ্কু-আকারের, ভূমি 12 m² আর উচ্চতা 3 m। বালির ওজন m³-প্রতি 1.6 টন। মোটামুটি কত ভারী?", ["19.2 টন", "57.6 টন", "12 টন", "6.4 টন"],
        "আয়তন = ⅓ x 12 x 3 = 12 m³; x 1.6 = 19.2 টন।"),
    mcq("y is directly proportional to x. When x = 4, y = 20. What is y when x = 7?", ["35", "23", "28", "140"], 0,
        "y = 5x, so y = 35.",
        "y, x-এর সমানুপাতিক। x = 4 হলে y = 20। x = 7 হলে y কত?", ["35", "23", "28", "140"],
        "y = 5x, তাই y = 35।"),
    mcq("Time to build is inversely proportional to the number of workers. 10 workers take 18 days. How long for 15?", ["12 days", "27 days", "15 days", "8 days"], 0,
        "workers x days = 180, so 180 ÷ 15 = 12.",
        "নির্মাণের সময় কর্মী-সংখ্যার ব্যস্তানুপাতিক। 10 জনে 18 দিন লাগে। 15 জনে কত?", ["12 দিন", "27 দিন", "15 দিন", "8 দিন"],
        "কর্মী x দিন = 180, তাই 180 ÷ 15 = 12।"),
    mcq("Which is the equation of a line with gradient 2 passing through (0, -3)?", ["y = 2x - 3", "y = -3x + 2", "y = 2x + 3", "y = x - 3"], 0,
        "y = mx + c with m = 2, c = -3.",
        "নতি 2 আর (0, -3) বিন্দুগামী রেখার সমীকরণ কোনটা?", ["y = 2x - 3", "y = -3x + 2", "y = 2x + 3", "y = x - 3"],
        "y = mx + c, যেখানে m = 2, c = -3।"),
    mcq("Two lines are parallel. What do their equations have in common?", ["The same gradient", "The same y-intercept", "They cross at (0, 0)", "Nothing"], 0,
        "y = 3x + 1 and y = 3x - 5 are parallel.",
        "দুটি রেখা সমান্তরাল। তাদের সমীকরণে কী মিল?", ["একই নতি", "একই y-ছেদক", "(0, 0)-তে ছেদ করে", "কিছুই না"],
        "y = 3x + 1 আর y = 3x - 5 সমান্তরাল।"),
    mcq("A cable hangs in a curve shaped like y = x² / 100. How high is it at x = 20 m from the lowest point?", ["4 m", "40 m", "0.4 m", "2 m"], 0,
        "20² ÷ 100 = 400 ÷ 100 = 4 m - suspension cables are close to this shape (a parabola).",
        "একটা তার y = x² / 100 আকারের বাঁকে ঝোলে। সবচেয়ে নিচু বিন্দু থেকে x = 20 m-এ কত উঁচু?", ["4 m", "40 m", "0.4 m", "2 m"],
        "20² ÷ 100 = 400 ÷ 100 = 4 m - ঝুলন্ত সেতুর তার প্রায় এই আকারের (অধিবৃত্ত)।"),
    mcq("What shape does a suspension bridge's main cable make under an evenly spread deck load?", ["A parabola", "A circle", "A straight line", "A zig-zag"], 0,
        "A freely hanging chain alone makes a catenary; a uniform deck load makes it a parabola.",
        "সমানভাবে ছড়ানো পাটাতনের বোঝায় ঝুলন্ত সেতুর মূল তার কী আকার নেয়?", ["অধিবৃত্ত", "বৃত্ত", "সরলরেখা", "আঁকাবাঁকা"],
        "একা মুক্তভাবে ঝোলা শিকল ক্যাটেনারি হয়; সমান পাটাতন-বোঝায় অধিবৃত্ত হয়।"),
    simul(6, 4, 1, 1, 1, -1), simul(3, 5, 2, 3, 1, 2), simul(8, 3, 1, -2, 2, 1), simul(1, 4, 5, 2, 3, -1),
    trig_opp(30, 30, "A conveyor belt", "একটা কনভেয়ার বেল্ট"), trig_opp(8, 30, "A wheelchair ramp", "একটা হুইলচেয়ারের ঢাল"),
    trig_adj(40, 60, "A tower guy-rope", "টাওয়ারের একটা টানা দড়ি"), trig_adj(16, 60, "A roof rafter", "ছাদের একটা কড়িকাঠ"),
    trig_tan(60, "A cliff above the river", "নদীর ধারের একটা খাড়া পাহাড়"), trig_tan(18, "A crane mast", "একটা ক্রেনের মাস্তুল"),
    similar(4, 2, "", ""), similar(6, 1, "", ""),
    grad(0, 10, 5, 0), grad(-3, 2, 1, 14), grad(-2, -4, 2, 4),
    arc(28, 45, "A curved railing", "একটা বাঁকা রেলিং"), arc(35, 72, "A curved viaduct section", "একটা বাঁকা ভায়াডাক্ট-অংশ"),
    mcq("Expand and simplify (x + 6)².", ["x² + 12x + 36", "x² + 36", "x² + 6x + 36", "2x + 12"], 0,
        "(x + 6)(x + 6) = x² + 6x + 6x + 36.",
        "বিস্তার করে সরল করো: (x + 6)²।", ["x² + 12x + 36", "x² + 36", "x² + 6x + 36", "2x + 12"],
        "(x + 6)(x + 6) = x² + 6x + 6x + 36।"),
    mcq("Factorise x² - 16.", ["(x - 4)(x + 4)", "(x - 4)²", "(x - 8)(x + 2)", "(x - 16)(x + 1)"], 0,
        "Difference of two squares: a² - b² = (a - b)(a + b).",
        "উৎপাদকে বিশ্লেষণ করো: x² - 16।", ["(x - 4)(x + 4)", "(x - 4)²", "(x - 8)(x + 2)", "(x - 16)(x + 1)"],
        "দুই বর্গের অন্তর: a² - b² = (a - b)(a + b)।"),
    mcq("Factorise x² + x - 12.", ["(x + 4)(x - 3)", "(x - 4)(x + 3)", "(x + 6)(x - 2)", "(x + 12)(x - 1)"], 0,
        "Numbers that multiply to -12 and add to +1: 4 and -3.",
        "উৎপাদকে বিশ্লেষণ করো: x² + x - 12।", ["(x + 4)(x - 3)", "(x - 4)(x + 3)", "(x + 6)(x - 2)", "(x + 12)(x - 1)"],
        "যাদের গুণফল -12 আর যোগফল +1: 4 আর -3।"),
    mcq("A tower is 30 m tall. From a point on level ground, the angle up to its top is 45°. How far away is the point?", ["30 m", "60 m", "15 m", "42 m"], 0,
        "tan 45° = 1, so distance = height.",
        "একটা টাওয়ার 30 m উঁচু। সমতল মাটির একটা বিন্দু থেকে মাথার দিকে কোণ 45°। বিন্দুটা কত দূরে?", ["30 m", "60 m", "15 m", "42 m"],
        "tan 45° = 1, তাই দূরত্ব = উচ্চতা।"),
    mcq("What is cos 0°?", ["1", "0", "0.5", "-1"], 0,
        "At 0° the adjacent side equals the hypotenuse.",
        "cos 0° কত?", ["1", "0", "0.5", "-1"],
        "0°-এ সন্নিহিত বাহু অতিভুজের সমান।"),
    mcq("Which ratio would you use to find a ramp's angle from its height and sloping length?", ["sin = opposite ÷ hypotenuse", "tan = adjacent ÷ opposite", "cos = opposite ÷ adjacent", "None"], 0,
        "Height is opposite; sloping length is the hypotenuse.",
        "উচ্চতা আর ঢালু দৈর্ঘ্য থেকে ঢালের কোণ বের করতে কোন অনুপাত ব্যবহার করবে?", ["sin = বিপরীত ÷ অতিভুজ", "tan = সন্নিহিত ÷ বিপরীত", "cos = বিপরীত ÷ সন্নিহিত", "কোনোটাই না"],
        "উচ্চতা বিপরীত বাহু; ঢালু দৈর্ঘ্য অতিভুজ।"),
    mcq("A map shows two piers 4 cm apart at a scale of 1 : 2,500. How far apart are they really?", ["100 m", "10 m", "1,000 m", "625 m"], 0,
        "4 x 2,500 = 10,000 cm = 100 m.",
        "1 : 2,500 মাপের মানচিত্রে দুটো থাম 4 cm দূরে। বাস্তবে কত দূরে?", ["100 m", "10 m", "1,000 m", "625 m"],
        "4 x 2,500 = 10,000 cm = 100 m।"),
    mcq("What is the 'upper bound' of 50 m measured to the nearest 10 m?", ["55 m", "60 m", "50 m", "51 m"], 0,
        "The true value is in 45 ≤ L < 55.",
        "নিকটতম 10 m-এ মাপা 50 m-এর 'ঊর্ধ্বসীমা' কত?", ["55 m", "60 m", "50 m", "51 m"],
        "আসল মান 45 ≤ L < 55-এর মধ্যে।"),
    mcq("Why do engineers design using the 'worst case' bound of measurements?", ["To make sure the structure is safe even if measurements are off", "To waste material", "To make drawings messy", "It is never done"], 0,
        "Safety first: use the smallest strength and largest load.",
        "প্রকৌশলীরা মাপের 'সবচেয়ে খারাপ' সীমা ধরে নকশা করেন কেন?", ["মাপে গোলমাল থাকলেও কাঠামো যাতে নিরাপদ থাকে", "উপাদান নষ্ট করতে", "নকশা অগোছালো করতে", "কখনো করা হয় না"],
        "নিরাপত্তা আগে: সবচেয়ে কম শক্তি আর সবচেয়ে বেশি বোঝা ধরো।"),
    mcq("What is (2 x 10^6) ÷ (4 x 10^2)?", ["5 x 10^3", "0.5 x 10^3", "8 x 10^8", "5 x 10^4"], 0,
        "2 ÷ 4 = 0.5; 10^6 ÷ 10^2 = 10^4; 0.5 x 10^4 = 5 x 10^3.",
        "(2 x 10^6) ÷ (4 x 10^2) কত?", ["5 x 10^3", "0.5 x 10^3", "8 x 10^8", "5 x 10^4"],
        "2 ÷ 4 = 0.5; 10^6 ÷ 10^2 = 10^4; 0.5 x 10^4 = 5 x 10^3।"),
    mcq("Simplify (x⁵)².", ["x¹⁰", "x⁷", "2x⁵", "x²⁵"], 0,
        "Multiply powers when raising a power to a power.",
        "সরল করো: (x⁵)²।", ["x¹⁰", "x⁷", "2x⁵", "x²⁵"],
        "ঘাতের ঘাতে ঘাত গুণ করো।"),
    mcq("What is 5^-1?", ["1/5", "-5", "5", "0"], 0,
        "A negative power means the reciprocal.",
        "5^-1 কত?", ["1/5", "-5", "5", "0"],
        "ঋণাত্মক ঘাত মানে অন্যোন্যক।"),
    mcq("A survey of 200 drivers found 50 would pay a Rs 30 toll. Estimate how many of 8,000 daily drivers would pay.", ["2,000", "1,600", "4,000", "50"], 0,
        "50/200 = 1/4; 1/4 of 8,000 = 2,000.",
        "200 জন চালকের সমীক্ষায় 50 জন 30 টাকা টোল দিতে রাজি। দৈনিক 8,000 চালকের কতজন দেবেন আন্দাজ করো।", ["2,000", "1,600", "4,000", "50"],
        "50/200 = 1/4; 8,000-এর 1/4 = 2,000।"),
    mcq("A spinner lands on red with probability 0.35 and blue 0.4. What is P(neither red nor blue)?", ["0.25", "0.75", "0.14", "0.05"], 0,
        "1 - 0.35 - 0.4 = 0.25.",
        "একটা চাকতি লালে পড়ার সম্ভাবনা 0.35 আর নীলে 0.4। লালও নয় নীলও নয়, এমন সম্ভাবনা কত?", ["0.25", "0.75", "0.14", "0.05"],
        "1 - 0.35 - 0.4 = 0.25।"),
    mcq("What is the interior angle of a regular octagon?", ["135°", "120°", "45°", "108°"], 0,
        "180 - exterior 45 = 135°.",
        "সুষম অষ্টভুজের অন্তঃকোণ কত?", ["135°", "120°", "45°", "108°"],
        "180 - বহিঃকোণ 45 = 135°।"),
    mcq("A cylinder pile has radius 0.5 m and depth 20 m. Using π ≈ 3.14, how much concrete fills it?", ["15.7 m³", "31.4 m³", "62.8 m³", "10 m³"], 0,
        "πr²h = 3.14 x 0.25 x 20 = 15.7 m³.",
        "একটা চোঙাকার পাইলের ব্যাসার্ধ 0.5 m আর গভীরতা 20 m। π ≈ 3.14 ধরে কত কংক্রিট লাগবে?", ["15.7 m³", "31.4 m³", "62.8 m³", "10 m³"],
        "πr²h = 3.14 x 0.25 x 20 = 15.7 m³।"),
    mcq("What is the volume of a sphere of radius 3 m? (V = 4/3 πr³, π ≈ 3.14)", ["113.04 m³", "37.68 m³", "28.26 m³", "339.12 m³"], 0,
        "4/3 x 3.14 x 27 = 113.04 m³.",
        "3 m ব্যাসার্ধের গোলকের আয়তন কত? (V = 4/3 πr³, π ≈ 3.14)", ["113.04 m³", "37.68 m³", "28.26 m³", "339.12 m³"],
        "4/3 x 3.14 x 27 = 113.04 m³।"),
    mcq("If y = 3x², what is y when x = 4?", ["48", "144", "24", "36"], 0,
        "x² = 16; 3 x 16 = 48.",
        "y = 3x² হলে x = 4-এ y কত?", ["48", "144", "24", "36"],
        "x² = 16; 3 x 16 = 48।"),
    mcq("What is the nth term of 7, 12, 17, 22, ...?", ["5n + 2", "5n + 7", "7n + 5", "n + 5"], 0,
        "Goes up by 5; 5 x 1 + 2 = 7.",
        "7, 12, 17, 22, ...-এর n-তম পদ কী?", ["5n + 2", "5n + 7", "7n + 5", "n + 5"],
        "5 করে বাড়ে; 5 x 1 + 2 = 7।"),
    mcq("A deck's length L and width W satisfy L = 3W and L + W = 48. What is W?", ["12 m", "16 m", "36 m", "9 m"], 0,
        "3W + W = 48 -> 4W = 48 -> W = 12; L = 36.",
        "একটা পাটাতনের দৈর্ঘ্য L আর প্রস্থ W-এ L = 3W আর L + W = 48। W কত?", ["12 m", "16 m", "36 m", "9 m"],
        "3W + W = 48 -> 4W = 48 -> W = 12; L = 36।"),
    mcq("A cable is 1.5 km long. What is that in standard form, in metres?", ["1.5 x 10^3 m", "15 x 10^2 m", "1.5 x 10^2 m", "0.15 x 10^4 m"], 0,
        "1,500 m = 1.5 x 10^3.",
        "একটা তার 1.5 km লম্বা। মিটারে আদর্শ রূপে কত?", ["1.5 x 10^3 m", "15 x 10^2 m", "1.5 x 10^2 m", "0.15 x 10^4 m"],
        "1,500 m = 1.5 x 10^3।"),
)
