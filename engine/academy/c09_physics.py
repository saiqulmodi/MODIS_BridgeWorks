"""Class 9 - Physics (Bridge Engineer cadet): Newton's three laws in depth, the equations of
motion (suvat), free fall and impact speed, friction (F = μN), forces on slopes, Boyle's law and
the kelvin scale, upthrust on pontoons, charge and energy in circuits, choosing fuses, sonar
depth, earthquake waves and seismic design - all tied to real bridges."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r * 2, r + 10, r + 2):
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


def vuat(u, a, t, what_en, what_bn):
    v = u + a * t
    return _n(f"{what_en} starts at {u} m/s and accelerates at {a} m/s² for {t} s. What is its final speed?",
              f"{what_bn} {u} m/s থেকে শুরু করে {t} s ধরে {a} m/s² ত্বরণে চলে। শেষ বেগ কত?", v,
              f"v = u + at = {u} + {a} x {t} = {v} m/s.",
              f"v = u + at = {u} + {a} x {t} = {v} m/s।",
              (a * t, u * t + a, u + a + t), " m/s")


def suat(u, a, t, what_en, what_bn):
    s = _c(u * t + 0.5 * a * t * t)
    return _n(f"{what_en} starts at {u} m/s and accelerates at {a} m/s² for {t} s. How far does it travel?",
              f"{what_bn} {u} m/s থেকে শুরু করে {t} s ধরে {a} m/s² ত্বরণে চলে। কত দূর যায়?", s,
              f"s = ut + ½at² = {u} x {t} + ½ x {a} x {t}² = {s:g} m.",
              f"s = ut + ½at² = {u} x {t} + ½ x {a} x {t}² = {s:g} m।",
              (_c(u * t + a * t * t), _c((u + a * t) * t), _c(u * t)), " m")


def brake(u, a):
    s = _c(u * u / (2 * a))
    return _n(f"A truck at {u} m/s brakes with a deceleration of {a} m/s². How far does it travel before stopping? (v² = u² + 2as)",
              f"{u} m/s বেগের একটা ট্রাক {a} m/s² মন্দনে ব্রেক কষে। থামার আগে কত দূর যায়? (v² = u² + 2as)", s,
              f"0 = {u}² - 2 x {a} x s, so s = {u * u} ÷ {2 * a} = {s:g} m. Double the speed and the distance becomes four times as long!",
              f"0 = {u}² - 2 x {a} x s, তাই s = {u * u} ÷ {2 * a} = {s:g} m। বেগ দ্বিগুণ হলে দূরত্ব চারগুণ!",
              (_c(u / a), _c(u * u / a), _c(s / 2)), " m")


def fall_t(h):
    t = _c((2 * h / 10) ** 0.5)
    return _n(f"A bolt is dropped from a bridge deck {h} m above the water. Ignoring air resistance, how long does it take to hit the water? (g = 10 m/s²)",
              f"জল থেকে {h} m উঁচু সেতুর পাটাতন থেকে একটা বল্টু পড়ল। বায়ুর বাধা বাদ দিলে জলে পড়তে কত সময়? (g = 10 m/s²)", t,
              f"h = ½gt², so t = √(2h ÷ g) = √({2 * h} ÷ 10) = {t:g} s.",
              f"h = ½gt², তাই t = √(2h ÷ g) = √({2 * h} ÷ 10) = {t:g} s।",
              (_c(h / 10), _c(2 * h / 10), _c(t + 0.5)), " s")


def fall_v(h):
    v = _c((2 * 10 * h) ** 0.5)
    return _n(f"A tool falls {h} m from a tower crane. Ignoring air resistance, how fast is it moving when it lands? (g = 10 m/s²)",
              f"একটা টাওয়ার-ক্রেন থেকে একটা যন্ত্র {h} m পড়ল। বায়ুর বাধা বাদ দিলে মাটিতে পড়ার সময় বেগ কত? (g = 10 m/s²)", v,
              f"v² = 2gh = 2 x 10 x {h} = {20 * h}, so v = {v:g} m/s (about {_c(v * 3.6):g} km/h).",
              f"v² = 2gh = 2 x 10 x {h} = {20 * h}, তাই v = {v:g} m/s (প্রায় {_c(v * 3.6):g} km/h)।",
              (_c(10 * h), _c(20 * h), _c(v / 2)), " m/s")


def friction(mu, m, what_en, what_bn):
    f = _c(mu * m * 10)
    return _n(f"{what_en} of mass {m:,} kg rests on a flat surface. The coefficient of friction is {mu:g}. What horizontal force is needed to start it sliding? (g = 10 N/kg)",
              f"{m:,} kg ভরের {what_bn} সমতলে রাখা। ঘর্ষণ-গুণাঙ্ক {mu:g}। পিছলে চালু করতে কত অনুভূমিক বল লাগে? (g = 10 N/kg)", f,
              f"Normal force N = mg = {m * 10:,} N; F = μN = {mu:g} x {m * 10:,} = {f:,} N.",
              f"অভিলম্ব বল N = mg = {m * 10:,} N; F = μN = {mu:g} x {m * 10:,} = {f:,} N।",
              (m * 10, _c(mu * m), _c(f * 2)), " N")


def slope(m, ang, sinv):
    f = _c(m * 10 * sinv)
    return _n(f"A {m:,} kg trolley stands on a ramp at {ang}° (sin {ang}° = {sinv:g}). What component of its weight acts down the slope? (g = 10 N/kg)",
              f"{m:,} kg-এর একটা ট্রলি {ang}° ঢালে দাঁড়িয়ে (sin {ang}° = {sinv:g})। এর ওজনের কোন উপাংশ ঢাল বেয়ে নিচে কাজ করে? (g = 10 N/kg)", f,
              f"Down-slope force = mg sin θ = {m * 10:,} x {sinv:g} = {f:,} N - the brakes or a winch must hold this.",
              f"ঢাল-বরাবর বল = mg sin θ = {m * 10:,} x {sinv:g} = {f:,} N - ব্রেক বা উইঞ্চকে এটা ধরে রাখতে হবে।",
              (m * 10, _c(m * sinv), _c(f / 2)), " N")


def boyle(p1, v1, v2):
    p2 = _c(p1 * v1 / v2)
    return _n(f"Air in a pneumatic tool's cylinder is at {p1:g} kPa in a volume of {v1:g} cm³. It is squeezed to {v2:g} cm³ at the same temperature. What is the new pressure?",
              f"একটা বায়ুচালিত যন্ত্রের সিলিন্ডারে {v1:g} cm³ আয়তনে বাতাসের চাপ {p1:g} কিলোপ্যাসকেল। একই তাপমাত্রায় একে {v2:g} cm³-এ চাপা হলো। নতুন চাপ কত?", p2,
              f"Boyle's law: p1V1 = p2V2, so p2 = {p1:g} x {v1:g} ÷ {v2:g} = {p2:g} kPa.",
              f"বয়েলের সূত্র: p1V1 = p2V2, তাই p2 = {p1:g} x {v1:g} ÷ {v2:g} = {p2:g} কিলোপ্যাসকেল।",
              (_c(p1 * v2 / v1), _c(p1 + v1 - v2) if p1 + v1 - v2 > 0 else _c(p2 + 50), _c(p2 / 2)), " kPa", " কিলোপ্যাসকেল")


def kelvin(c):
    k = c + 273
    return _n(f"Steel in a bridge is at {c}°C. What is that temperature in kelvin?",
              f"সেতুর ইস্পাতের তাপমাত্রা {c}°C। কেলভিনে সেটা কত?", k,
              f"K = °C + 273 = {c} + 273 = {k} K.",
              f"K = °C + 273 = {c} + 273 = {k} K।",
              (c - 273 if c - 273 > 0 else k + 100, c + 100, k - 30), " K")


def upthrust(vol, what_en, what_bn):
    f = vol * 1000 * 10 // 1000
    return _n(f"{what_en} pushes {vol} m³ of river water aside. What upthrust does the water give? (water 1,000 kg/m³, g = 10 N/kg)",
              f"{what_bn} {vol} m³ নদীর জল সরায়। জল কত ঊর্ধ্বঘাত দেয়? (জল 1,000 kg/m³, g = 10 N/kg)", f,
              f"Upthrust = weight of water displaced = {vol} x 1,000 x 10 = {vol * 10000:,} N = {f:,} kN.",
              f"ঊর্ধ্বঘাত = সরানো জলের ওজন = {vol} x 1,000 x 10 = {vol * 10000:,} N = {f:,} kN।",
              (vol * 10, vol * 1000, f * 10), " kN")


def charge(i, t, what_en, what_bn):
    q = i * t
    return _n(f"{what_en} draws {i} A for {t:,} s. How much charge flows?",
              f"{what_bn} {t:,} s ধরে {i} A টানে। কত আধান প্রবাহিত হয়?", q,
              f"Q = It = {i} x {t:,} = {q:,} C.",
              f"Q = It = {i} x {t:,} = {q:,} C।",
              (_c(t / i), i + t, q * 60), " C")


def energy_qv(q, v):
    e = q * v
    return _n(f"{q:,} C of charge passes through a site lamp on a {v} V supply. How much energy is transferred?",
              f"{v} V সরবরাহে নির্মাণস্থলের একটা বাতির মধ্যে দিয়ে {q:,} C আধান যায়। কত শক্তি স্থানান্তরিত হয়?", e,
              f"E = QV = {q:,} x {v} = {e:,} J.",
              f"E = QV = {q:,} x {v} = {e:,} J।",
              (_c(q / v), q + v, e * 10), " J")


def fuse(p, v, what_en, what_bn):
    i = p / v
    choice = 3 if i < 3 else 5 if i < 5 else 13
    o = [f"{choice} A"] + [f"{x} A" for x in (3, 5, 13, 30) if x != choice][:3]
    return mcq(f"{what_en} is rated {p:,} W on a {v} V supply. Fuses come in 3 A, 5 A, 13 A and 30 A. Which fuse should be fitted?",
               o, 0,
               f"I = P ÷ V = {p:,} ÷ {v} ≈ {i:.1f} A. Choose the smallest fuse just above this: {choice} A.",
               f"{v} V সরবরাহে {what_bn}-এর ক্ষমতা {p:,} W। ফিউজ আছে 3 A, 5 A, 13 A আর 30 A। কোনটা লাগানো উচিত?",
               o,
               f"I = P ÷ V = {p:,} ÷ {v} ≈ {i:.1f} A। এর ঠিক উপরের সবচেয়ে ছোট ফিউজ বাছো: {choice} A।")


def sonar(t, v, what_en, what_bn):
    d = _c(v * t / 2)
    return _n(f"A sonar pulse from a survey boat reflects off {what_en} and returns after {t:g} s. Sound travels {v:,} m/s in water. How deep is it?",
              f"জরিপ-নৌকার একটা সোনার-স্পন্দন {what_bn}-এ প্রতিফলিত হয়ে {t:g} s পরে ফিরল। জলে শব্দের বেগ {v:,} m/s। কত গভীর?", d,
              f"Distance there and back = {v:,} x {t:g} = {_c(v * t):g} m; depth = half = {d:g} m.",
              f"যাওয়া-আসার দূরত্ব = {v:,} x {t:g} = {_c(v * t):g} m; গভীরতা = অর্ধেক = {d:g} m।",
              (_c(v * t), _c(v / t), _c(d * 3)), " m")


def workdone(f, d, what_en, what_bn):
    w = f * d
    return _n(f"A winch pulls {what_en} with a force of {f:,} N through {d} m. How much work is done?",
              f"একটা উইঞ্চ {f:,} N বলে {what_bn}কে {d} m টানে। কত কার্য হয়?", w,
              f"W = Fd = {f:,} x {d} = {w:,} J.",
              f"W = Fd = {f:,} x {d} = {w:,} J।",
              (_c(f / d), f + d, w * 10), " J")


ITEMS = (
    vuat(0, 2, 10, "A car leaving a toll plaza", "টোল-প্লাজা ছাড়া একটা গাড়ি"), vuat(5, 3, 4, "A cyclist on a ramp", "ঢালে একজন সাইকেল-আরোহী"),
    vuat(10, 1, 15, "A train on a viaduct", "উড়ালপথে একটা ট্রেন"), vuat(0, 4, 6, "A launched girder trolley", "ছাড়া-হওয়া গার্ডারের ট্রলি"),
    suat(0, 2, 10, "A truck from rest", "স্থির থেকে একটা ট্রাক"), suat(4, 2, 5, "A van", "একটা ভ্যান"),
    suat(10, 1, 4, "A bus on a bridge", "সেতুর উপর একটা বাস"), suat(0, 6, 3, "A test sled", "একটা পরীক্ষামূলক স্লেজ"),
    brake(20, 5), brake(30, 6), brake(10, 4), brake(25, 5),
    fall_t(5), fall_t(20), fall_t(45), fall_t(80),
    fall_v(5), fall_v(20), fall_v(45), fall_v(80),
    friction(0.4, 500, "A steel crate", "একটা ইস্পাতের বাক্স"), friction(0.6, 200, "A concrete block", "একটা কংক্রিটের ব্লক"),
    friction(0.1, 20000, "A bridge segment on PTFE sliding bearings", "পিটিএফই পিছল-বিয়ারিংয়ে একটা সেতু-খণ্ড"), friction(0.5, 80, "A toolbox", "একটা যন্ত্রের বাক্স"),
    slope(200, 30, 0.5), slope(1000, 10, 0.17), slope(800, 20, 0.34), slope(60, 30, 0.5),
    boyle(100, 300, 100), boyle(200, 50, 20), boyle(150, 400, 300), boyle(120, 90, 30),
    kelvin(20), kelvin(45), kelvin(-10), kelvin(0),
    upthrust(30, "A steel pontoon", "একটা ইস্পাতের পন্টুন"), upthrust(120, "A floating crane barge", "একটা ভাসমান ক্রেন-বজরা"),
    upthrust(8, "A small work boat", "একটা ছোট কাজের নৌকা"),
    charge(5, 600, "A drill", "একটা ড্রিল"), charge(2, 3600, "A floodlight", "একটা ফ্লাডলাইট"), charge(10, 120, "A welder's fan", "ঝালাইকারের পাখা"),
    energy_qv(500, 230), energy_qv(1200, 12), energy_qv(60, 230),
    fuse(2300, 230, "A kettle in the site canteen", "ক্যান্টিনের একটা কেটলি"), fuse(460, 230, "A drill", "একটা ড্রিল"),
    fuse(60, 230, "A desk lamp", "একটা টেবিল-বাতি"), fuse(1000, 230, "A heater", "একটা হিটার"),
    sonar(0.02, 1500, "the riverbed beside a pier", "স্তম্ভের পাশের নদীর তল"), sonar(0.04, 1500, "the seabed", "সমুদ্রের তল"),
    sonar(0.1, 1500, "a deep channel", "একটা গভীর খাত"),
    workdone(2000, 15, "a girder", "একটা গার্ডার"), workdone(500, 40, "a cable", "একটা তার"),
    mcq("What does Newton's first law say?", ["An object stays at rest or keeps moving at constant velocity unless a resultant force acts on it", "Force equals mass times acceleration", "Every action has an equal and opposite reaction", "Objects always slow down by themselves"], 0,
        "Things slow down in everyday life only because friction and drag are forces.",
        "নিউটনের প্রথম সূত্র কী বলে?", ["লব্ধি বল কাজ না করলে বস্তু স্থির থাকে বা সমবেগে চলতে থাকে", "বল = ভর x ত্বরণ", "প্রতিটা ক্রিয়ার সমান ও বিপরীত প্রতিক্রিয়া আছে", "বস্তু সবসময় নিজে থেকে ধীর হয়"],
        "রোজকার জীবনে জিনিস ধীর হয় শুধু ঘর্ষণ আর টান বল বলে।"),
    mcq("Why do unsecured loads slide forward off a truck that brakes suddenly?", ["The load keeps moving forward (inertia) when the truck slows", "Brakes push loads forward", "Gravity pulls them forward", "Wind blows them"], 0,
        "Straps provide the force needed to slow the load with the truck.",
        "হঠাৎ ব্রেক কষা ট্রাক থেকে না-বাঁধা বোঝা সামনে পিছলে পড়ে কেন?", ["ট্রাক ধীর হলেও বোঝা সামনে চলতে থাকে (জড়তা)", "ব্রেক বোঝাকে সামনে ঠেলে", "মাধ্যাকর্ষণ সামনে টানে", "হাওয়া উড়িয়ে নেয়"],
        "বেল্টই বোঝাকে ট্রাকের সঙ্গে ধীর করার বল জোগায়।"),
    mcq("What does Newton's third law say about a truck resting on a bridge deck?", ["The truck pushes down on the deck and the deck pushes up on the truck with an equal force", "Only the truck pushes", "Only the deck pushes", "The forces cancel to zero on the truck from Newton's third law alone"], 0,
        "Third-law pairs act on different objects - one on the deck, one on the truck.",
        "সেতুর পাটাতনে দাঁড়ানো ট্রাক নিয়ে নিউটনের তৃতীয় সূত্র কী বলে?", ["ট্রাক পাটাতনকে নিচে ঠেলে আর পাটাতন সমান বলে ট্রাককে উপরে ঠেলে", "শুধু ট্রাক ঠেলে", "শুধু পাটাতন ঠেলে", "শুধু তৃতীয় সূত্র থেকেই ট্রাকের উপর বল শূন্য হয়ে কাটে"],
        "তৃতীয় সূত্রের জোড়া আলাদা বস্তুর উপর কাজ করে - একটা পাটাতনে, একটা ট্রাকে।"),
    mcq("How does a jet of water from a fire hose push the firefighter backwards?", ["The hose pushes water forward, so the water pushes the hose back (Newton's third law)", "Water is heavier than the firefighter", "Gravity acts sideways", "It does not push back"], 0,
        "Rockets and jet engines work the same way.",
        "দমকলের পাইপের জলের ধারা কীভাবে দমকলকর্মীকে পিছনে ঠেলে?", ["পাইপ জলকে সামনে ঠেলে, তাই জল পাইপকে পিছনে ঠেলে (নিউটনের তৃতীয় সূত্র)", "জল দমকলকর্মীর চেয়ে ভারী", "মাধ্যাকর্ষণ পাশে কাজ করে", "পিছনে ঠেলে না"],
        "রকেট আর জেট-ইঞ্জিন একইভাবে কাজ করে।"),
    mcq("A 1,000 kg survey rover is sent to the Moon, where g = 1.6 N/kg. What is its weight there?", ["1,600 N", "10,000 N", "1,000 N", "625 N"], 0,
        "W = mg = 1,000 x 1.6 = 1,600 N. Its mass is still 1,000 kg - only the weight changes.",
        "1,000 kg-এর একটা জরিপ-রোভার চাঁদে পাঠানো হলো, যেখানে g = 1.6 N/kg। সেখানে এর ওজন কত?", ["1,600 N", "10,000 N", "1,000 N", "625 N"],
        "W = mg = 1,000 x 1.6 = 1,600 N। ভর এখনো 1,000 kg - শুধু ওজন বদলায়।"),
    mcq("What does a free-body diagram show?", ["All the forces acting on one object, drawn as arrows from it", "The route of a truck", "A bridge's paint colours", "The forces an object exerts on everything else"], 0,
        "Engineers draw one for every joint in a truss.",
        "মুক্ত-বস্তু চিত্র কী দেখায়?", ["একটা বস্তুর উপর কাজ করা সব বল, তার থেকে তির দিয়ে আঁকা", "ট্রাকের পথ", "সেতুর রং", "বস্তুটা অন্য সবকিছুর উপর যে বল দেয়"],
        "প্রকৌশলীরা ট্রাসের প্রতিটা জোড়ের জন্য একটা আঁকেন।"),
    mcq("A 2,000 kg car accelerates at 3 m/s² while friction and drag total 1,000 N. What driving force does the engine provide?", ["7,000 N", "6,000 N", "5,000 N", "1,000 N"], 0,
        "Resultant = ma = 6,000 N; driving force = 6,000 + 1,000 = 7,000 N.",
        "2,000 kg-এর একটা গাড়ি 3 m/s² ত্বরণে চলে, ঘর্ষণ আর বায়ুর টান মিলিয়ে 1,000 N। ইঞ্জিন কত চালক-বল দেয়?", ["7,000 N", "6,000 N", "5,000 N", "1,000 N"],
        "লব্ধি = ma = 6,000 N; চালক-বল = 6,000 + 1,000 = 7,000 N।"),
    mcq("A displacement-time graph for a train curves upwards, getting steeper. What is the train doing?", ["Speeding up (accelerating)", "Moving at constant speed", "Standing still", "Slowing down"], 0,
        "The gradient is the velocity - a steeper gradient means a higher velocity.",
        "একটা ট্রেনের সরণ-সময় লেখচিত্র উপরের দিকে বেঁকে ক্রমশ খাড়া হচ্ছে। ট্রেনটা কী করছে?", ["গতি বাড়াচ্ছে (ত্বরণ)", "সমদ্রুতিতে চলছে", "দাঁড়িয়ে আছে", "ধীর হচ্ছে"],
        "ঢালই বেগ - খাড়া ঢাল মানে বেশি বেগ।"),
    mcq("Why are the decks of long suspension bridges often shaped like a streamlined box (an aerofoil)?", ["Air flows smoothly around them, reducing wind forces and dangerous vortices", "To hold more cars", "To look like aeroplanes", "To collect rainwater"], 0,
        "Wind-tunnel tests on scale models decide the final shape.",
        "লম্বা ঝুলন্ত সেতুর পাটাতন প্রায়ই প্রবাহরেখ বাক্সের (এয়ারোফয়েল) আকারের হয় কেন?", ["বাতাস চারপাশে মসৃণভাবে বয়, হাওয়ার বল আর বিপজ্জনক ঘূর্ণি কমে", "বেশি গাড়ি ধরতে", "বিমানের মতো দেখাতে", "বৃষ্টির জল জমাতে"],
        "মাপমতো মডেলে বায়ু-সুড়ঙ্গ পরীক্ষা শেষ আকার ঠিক করে।"),
    mcq("Why does river water speed up as it flows past a bridge pier?", ["The pier narrows the channel, so the same flow must pass through a smaller gap faster", "Piers pump the water", "Water is attracted to concrete", "It slows down, not speeds up"], 0,
        "Faster water can scour away the riverbed around the pier.",
        "সেতু-স্তম্ভের পাশ দিয়ে যাওয়ার সময় নদীর জল দ্রুত হয় কেন?", ["স্তম্ভ খাতকে সরু করে, তাই একই প্রবাহ ছোট ফাঁক দিয়ে দ্রুত যেতে হয়", "স্তম্ভ জল পাম্প করে", "জল কংক্রিটের প্রতি আকৃষ্ট", "দ্রুত নয়, ধীর হয়"],
        "দ্রুত জল স্তম্ভের চারপাশের নদীতল ক্ষইয়ে দিতে পারে।"),
    mcq("After a flood, divers find a deep hole in the riverbed around a pier. What caused it?", ["Scour - fast-flowing water carried the riverbed sediment away", "Rust on the railings", "Fish digging nests", "The pier sinking under its own weight only"], 0,
        "Scour is one of the most common causes of bridge collapse worldwide.",
        "বন্যার পরে ডুবুরিরা একটা স্তম্ভের চারপাশে নদীতলে গভীর গর্ত পেলেন। এর কারণ কী?", ["ক্ষয়-খনন - দ্রুত স্রোত নদীতলের পলি বয়ে নিয়ে গেছে", "রেলিংয়ে মরচে", "মাছের বাসা খোঁড়া", "শুধু নিজের ওজনে স্তম্ভ বসে যাওয়া"],
        "বিশ্বজুড়ে সেতু ভেঙে পড়ার সবচেয়ে সাধারণ কারণগুলোর একটা।"),
    mcq("What causes the pressure of the air inside a sealed gas cylinder?", ["Gas particles colliding with the cylinder walls", "The weight of the cylinder", "The colour of the gas", "Electric charge"], 0,
        "More particles, or faster particles, mean more frequent and harder collisions - higher pressure.",
        "বন্ধ গ্যাস-সিলিন্ডারের ভেতরের চাপ কীসের জন্য হয়?", ["গ্যাসের কণা সিলিন্ডারের দেয়ালে ধাক্কা মারায়", "সিলিন্ডারের ওজন", "গ্যাসের রং", "বৈদ্যুতিক আধান"],
        "বেশি কণা বা দ্রুত কণা মানে আরও ঘন ঘন আর জোরে ধাক্কা - বেশি চাপ।"),
    mcq("With the same braking force, why does a loaded truck take longer to stop than an empty one?", ["Its greater mass gives a smaller deceleration (a = F ÷ m)", "Loaded trucks have weaker brakes", "Loads push the truck forward", "Empty trucks are faster"], 0,
        "Drivers of heavy vehicles must leave much bigger gaps.",
        "একই ব্রেক-বলে বোঝাই ট্রাক খালি ট্রাকের চেয়ে থামতে বেশি সময় নেয় কেন?", ["বেশি ভরে মন্দন কম হয় (a = F ÷ m)", "বোঝাই ট্রাকের ব্রেক দুর্বল", "বোঝা ট্রাককে সামনে ঠেলে", "খালি ট্রাক দ্রুত"],
        "ভারী গাড়ির চালকদের অনেক বেশি দূরত্ব রাখতে হয়।"),
    mcq("A crane lifts a load at a steady speed. What is the resultant force on the load?", ["Zero - the cable tension equals the weight", "Equal to the weight, upwards", "Twice the weight", "Equal to the cable tension, downwards"], 0,
        "Constant velocity means balanced forces (Newton's first law).",
        "একটা ক্রেন স্থির বেগে বোঝা তোলে। বোঝার উপর লব্ধি বল কত?", ["শূন্য - তারের টান ওজনের সমান", "ওজনের সমান, উপরের দিকে", "ওজনের দ্বিগুণ", "তারের টানের সমান, নিচের দিকে"],
        "সমবেগ মানে সাম্যে থাকা বল (নিউটনের প্রথম সূত্র)।"),
    mcq("Why is the cable tension greater than the load's weight as a crane starts lifting?", ["An extra upward force is needed to accelerate the load upwards", "The load gets heavier", "Cables shrink", "Gravity is stronger at the start"], 0,
        "T - mg = ma, so T = m(g + a). Jerky lifts overload cables.",
        "ক্রেন তোলা শুরু করার সময় তারের টান বোঝার ওজনের চেয়ে বেশি কেন?", ["বোঝাকে উপরে ত্বরান্বিত করতে বাড়তি ঊর্ধ্বমুখী বল লাগে", "বোঝা ভারী হয়", "তার ছোট হয়ে যায়", "শুরুতে মাধ্যাকর্ষণ জোরালো"],
        "T - mg = ma, তাই T = m(g + a)। ঝাঁকুনি দিয়ে তুললে তারে অতিরিক্ত বোঝা পড়ে।"),
    mcq("A velocity-time graph is a straight line sloping upwards. What does its gradient show?", ["The acceleration", "The distance", "The mass", "The force"], 0,
        "The area under a velocity-time graph shows the distance travelled.",
        "বেগ-সময় লেখচিত্র উপরের দিকে ঢালু সরলরেখা। এর ঢাল কী দেখায়?", ["ত্বরণ", "দূরত্ব", "ভর", "বল"],
        "বেগ-সময় লেখচিত্রের নিচের ক্ষেত্রফল অতিক্রান্ত দূরত্ব দেখায়।"),
    mcq("What does the area under a velocity-time graph represent?", ["The distance travelled", "The acceleration", "The time taken only", "The speed limit"], 0,
        "For constant acceleration from rest, it is a triangle: ½ x base x height.",
        "বেগ-সময় লেখচিত্রের নিচের ক্ষেত্রফল কী বোঝায়?", ["অতিক্রান্ত দূরত্ব", "ত্বরণ", "শুধু লাগা সময়", "গতিসীমা"],
        "স্থির থেকে সম-ত্বরণে এটা ত্রিভুজ: ½ x ভূমি x উচ্চতা।"),
    mcq("What is the difference between speed and velocity?", ["Velocity has a direction as well as a size; speed has only size", "They are always equal", "Speed has direction", "Velocity is always bigger"], 0,
        "A car going round a curved ramp at steady speed has a changing velocity.",
        "দ্রুতি আর বেগের পার্থক্য কী?", ["বেগের মানের সঙ্গে দিকও আছে; দ্রুতির শুধু মান", "সবসময় সমান", "দ্রুতির দিক আছে", "বেগ সবসময় বড়"],
        "বাঁকা ঢালে স্থির দ্রুতিতে ঘোরা গাড়ির বেগ বদলাতে থাকে।"),
    mcq("What is the 'thinking distance' when a driver brakes?", ["The distance travelled during the driver's reaction time, before the brakes act", "The distance after the brakes act", "The length of the car", "The distance to the next junction"], 0,
        "Tiredness, alcohol and phones all increase thinking distance.",
        "চালক ব্রেক কষার সময় 'ভাবনার দূরত্ব' কী?", ["ব্রেক কাজ করার আগে চালকের প্রতিক্রিয়া-সময়ে অতিক্রান্ত দূরত্ব", "ব্রেক কাজ করার পরের দূরত্ব", "গাড়ির দৈর্ঘ্য", "পরের মোড় পর্যন্ত দূরত্ব"],
        "ক্লান্তি, মদ আর ফোন সবই ভাবনার দূরত্ব বাড়ায়।"),
    mcq("Why are bridge decks in cold places sometimes fitted with heating or treated with grit?", ["Ice greatly reduces friction, so braking distances become much longer", "To keep the steel warm for workers", "Heating makes the bridge lighter", "To melt the paint"], 0,
        "Bridges freeze before roads because cold air flows above and below them.",
        "ঠান্ডা জায়গায় সেতুর পাটাতনে কখনো তাপ-ব্যবস্থা বসানো বা কাঁকর ছড়ানো হয় কেন?", ["বরফ ঘর্ষণ অনেক কমায়, তাই ব্রেকের দূরত্ব অনেক লম্বা হয়", "কর্মীদের জন্য ইস্পাত গরম রাখতে", "তাপে সেতু হালকা হয়", "রং গলাতে"],
        "সেতু রাস্তার আগে জমে, কারণ উপরে-নিচে দুদিকেই ঠান্ডা হাওয়া বয়।"),
    mcq("What is the 'coefficient of friction'?", ["A number comparing the friction force with the force pressing two surfaces together", "The weight of an object", "The speed of sliding", "A type of lubricant"], 0,
        "Rubber on dry road is about 0.7; on ice it can drop below 0.1.",
        "'ঘর্ষণ-গুণাঙ্ক' কী?", ["ঘর্ষণ বলকে দুই তল চেপে ধরা বলের সঙ্গে তুলনা করা একটা সংখ্যা", "বস্তুর ওজন", "পিছলানোর গতি", "এক রকম পিচ্ছিলকারক"],
        "শুকনো রাস্তায় রবারের প্রায় 0.7; বরফে 0.1-এর নিচে নামতে পারে।"),
    mcq("Why are PTFE (Teflon) sliding bearings used under some bridge decks?", ["Their very low friction lets the deck expand and contract without pushing hard on the piers", "They are magnetic", "They stop the deck moving at all", "They are the heaviest option"], 0,
        "Polished stainless steel slides on PTFE with a coefficient of friction of only a few hundredths.",
        "কিছু সেতুর পাটাতনের নিচে পিটিএফই (টেফলন) পিছল-বিয়ারিং ব্যবহার হয় কেন?", ["খুব কম ঘর্ষণে পাটাতন স্তম্ভকে জোরে না ঠেলেই প্রসারিত-সংকুচিত হতে পারে", "চৌম্বক", "পাটাতনের নড়াচড়া পুরো থামায়", "সবচেয়ে ভারী বিকল্প"],
        "পালিশ করা স্টেইনলেস স্টিল পিটিএফই-র উপর মাত্র কয়েক শতাংশ ঘর্ষণ-গুণাঙ্কে পিছলায়।"),
    mcq("A heavy load sits on a ramp without sliding. Which force stops it sliding down?", ["Static friction acting up the slope", "Air resistance", "Magnetism", "Upthrust"], 0,
        "If the slope gets steeper, the down-slope force may exceed the maximum friction.",
        "একটা ভারী বোঝা না পিছলে ঢালে বসে আছে। কোন বল একে নিচে পিছলাতে দেয় না?", ["ঢাল বরাবর উপরে কাজ করা স্থিতি-ঘর্ষণ", "বায়ুর বাধা", "চৌম্বকত্ব", "ঊর্ধ্বঘাত"],
        "ঢাল বেশি খাড়া হলে নিচের দিকের বল সর্বোচ্চ ঘর্ষণ ছাড়াতে পারে।"),
    mcq("What does Boyle's law say about a gas at constant temperature?", ["Pressure and volume are inversely proportional: halve the volume, double the pressure", "Pressure and volume rise together", "Volume never changes", "Temperature doubles"], 0,
        "pV = constant. Pneumatic tools and air brakes rely on compressed air.",
        "স্থির তাপমাত্রায় গ্যাস নিয়ে বয়েলের সূত্র কী বলে?", ["চাপ আর আয়তন ব্যস্তানুপাতিক: আয়তন অর্ধেক, চাপ দ্বিগুণ", "চাপ আর আয়তন একসঙ্গে বাড়ে", "আয়তন বদলায় না", "তাপমাত্রা দ্বিগুণ হয়"],
        "pV = ধ্রুবক। বায়ুচালিত যন্ত্র আর এয়ার-ব্রেক চাপা বাতাসের উপর চলে।"),
    mcq("Why does a truck's tyre pressure rise after a long drive on a hot day?", ["The air inside warms up, its particles move faster and hit the walls harder and more often", "Air leaks in", "Rubber shrinks", "The tyre gets heavier"], 0,
        "Check tyre pressures when cold for an accurate reading.",
        "গরম দিনে লম্বা যাত্রার পরে ট্রাকের টায়ারের চাপ বাড়ে কেন?", ["ভেতরের বাতাস গরম হয়, কণাগুলো দ্রুত চলে আর দেয়ালে জোরে ও বেশিবার ধাক্কা মারে", "বাতাস ঢুকে যায়", "রবার ছোট হয়", "টায়ার ভারী হয়"],
        "সঠিক পাঠের জন্য ঠান্ডা অবস্থায় টায়ারের চাপ দেখো।"),
    mcq("What is 'absolute zero'?", ["0 K or -273°C, the lowest possible temperature, where particles have the least energy", "0°C, where water freezes", "The temperature of space stations", "100°C"], 0,
        "Gas laws only work properly with temperatures in kelvin.",
        "'পরম শূন্য' কী?", ["0 K বা -273°C, সম্ভাব্য সর্বনিম্ন তাপমাত্রা, যেখানে কণার শক্তি সবচেয়ে কম", "0°C, যেখানে জল জমে", "মহাকাশ-স্টেশনের তাপমাত্রা", "100°C"],
        "গ্যাসের সূত্র ঠিকমতো খাটে শুধু কেলভিনের তাপমাত্রায়।"),
    mcq("What does Archimedes' principle say?", ["An object in a fluid feels an upthrust equal to the weight of fluid it displaces", "Objects always sink", "Heavy things always float", "Water has no weight"], 0,
        "Steel ships and pontoons float because their hollow shape displaces a lot of water.",
        "আর্কিমিডিসের নীতি কী বলে?", ["তরলে কোনো বস্তু যত তরল সরায়, তার ওজনের সমান ঊর্ধ্বঘাত পায়", "বস্তু সবসময় ডোবে", "ভারী জিনিস সবসময় ভাসে", "জলের ওজন নেই"],
        "ইস্পাতের জাহাজ আর পন্টুন ভাসে কারণ ফাঁপা আকার অনেক জল সরায়।"),
    mcq("Why can a pontoon bridge carry trucks across a river?", ["Its floating units displace enough water for upthrust to support the bridge and the trucks", "The trucks are lighter on water", "The river pushes sideways", "Pontoons are filled with helium"], 0,
        "Each extra truck pushes the pontoons a little deeper until the upthrust balances.",
        "ভাসমান পন্টুন-সেতু কীভাবে নদী পার করে ট্রাক বইতে পারে?", ["ভাসমান খণ্ডগুলো যথেষ্ট জল সরায়, তাই ঊর্ধ্বঘাত সেতু আর ট্রাক দুটোই বয়", "জলে ট্রাক হালকা হয়", "নদী পাশ থেকে ঠেলে", "পন্টুনে হিলিয়াম ভরা"],
        "প্রতিটা বাড়তি ট্রাক পন্টুনকে একটু গভীরে ঠেলে, যতক্ষণ না ঊর্ধ্বঘাত সমান হয়।"),
    mcq("Why does a loaded barge float lower in fresh river water than in sea water?", ["Fresh water is less dense, so more must be displaced for the same upthrust", "Sea water is warmer", "Rivers are deeper", "Fresh water has no upthrust"], 0,
        "Ships carry 'load lines' marking safe depths for fresh and salt water.",
        "বোঝাই বজরা সমুদ্রের জলের চেয়ে নদীর মিঠে জলে বেশি ডুবে ভাসে কেন?", ["মিঠে জলের ঘনত্ব কম, তাই একই ঊর্ধ্বঘাতের জন্য বেশি জল সরাতে হয়", "সমুদ্রের জল গরম", "নদী গভীর", "মিঠে জলে ঊর্ধ্বঘাত নেই"],
        "জাহাজের গায়ে মিঠে আর নোনা জলের নিরাপদ গভীরতার 'বোঝাই-রেখা' আঁকা থাকে।"),
    mcq("What is electric current?", ["The rate of flow of electric charge", "The amount of energy in a battery", "The push of a battery", "The resistance of a wire"], 0,
        "1 ampere = 1 coulomb per second.",
        "বিদ্যুৎ-প্রবাহ কী?", ["বৈদ্যুতিক আধান প্রবাহের হার", "ব্যাটারির শক্তির পরিমাণ", "ব্যাটারির ঠেলা", "তারের রোধ"],
        "1 অ্যাম্পিয়ার = সেকেন্ডে 1 কুলম্ব।"),
    mcq("What is potential difference (voltage)?", ["The energy transferred per unit of charge between two points", "The current in a wire", "The speed of electrons", "The thickness of a wire"], 0,
        "1 volt = 1 joule per coulomb.",
        "বিভব-পার্থক্য (ভোল্টেজ) কী?", ["দুই বিন্দুর মধ্যে প্রতি একক আধানে স্থানান্তরিত শক্তি", "তারের প্রবাহ", "ইলেকট্রনের গতি", "তারের পুরুত্ব"],
        "1 ভোল্ট = কুলম্বপ্রতি 1 জুল।"),
    mcq("What is the job of a fuse?", ["It melts and breaks the circuit if the current gets dangerously high", "It makes appliances work faster", "It stores charge", "It increases the voltage"], 0,
        "A fuse protects the wiring from overheating and starting a fire.",
        "ফিউজের কাজ কী?", ["প্রবাহ বিপজ্জনকভাবে বাড়লে গলে গিয়ে বর্তনী ছিন্ন করে", "যন্ত্র দ্রুত চালায়", "আধান জমায়", "ভোল্টেজ বাড়ায়"],
        "ফিউজ তারকে অতিরিক্ত গরম হয়ে আগুন লাগা থেকে রক্ষা করে।"),
    mcq("Why is a metal-cased site heater connected to an earth wire?", ["If a live wire touches the case, current flows safely to earth and blows the fuse instead of through a person", "To make it heat faster", "To save electricity", "Earth wires carry the main current"], 0,
        "Never use tools with damaged plugs or missing earth connections.",
        "ধাতব খোলের নির্মাণস্থলের হিটার আর্থ-তারে যুক্ত থাকে কেন?", ["জীবন্ত তার খোলে লাগলে প্রবাহ মানুষের বদলে নিরাপদে মাটিতে যায় আর ফিউজ উড়িয়ে দেয়", "দ্রুত গরম করতে", "বিদ্যুৎ বাঁচাতে", "আর্থ-তার মূল প্রবাহ বয়"],
        "ভাঙা প্লাগ বা আর্থ-সংযোগ নেই এমন যন্ত্র কখনো ব্যবহার কোরো না।"),
    mcq("Why do building sites often use 110 V tools instead of 230 V?", ["A shock from 110 V (centre-tapped to earth) is far less dangerous in wet, rough conditions", "110 V tools are more powerful", "230 V is illegal everywhere", "110 V uses no current"], 0,
        "Site transformers step the mains down to 110 V.",
        "নির্মাণস্থলে প্রায়ই 230 V-এর বদলে 110 V যন্ত্র ব্যবহার হয় কেন?", ["ভেজা, রুক্ষ পরিবেশে 110 V (মাঝখান থেকে মাটিতে যুক্ত) থেকে শক অনেক কম বিপজ্জনক", "110 V যন্ত্র বেশি শক্তিশালী", "230 V সব জায়গায় বেআইনি", "110 V-এ প্রবাহ লাগে না"],
        "নির্মাণস্থলের ট্রান্সফর্মার মেইন সরবরাহকে 110 V-এ নামায়।"),
    mcq("What does an RCD (residual current device) do?", ["Cuts the power within milliseconds if current leaks to earth, for example through a person", "Increases the voltage", "Measures temperature", "Stores electricity"], 0,
        "It reacts far faster than a fuse and can save lives.",
        "আরসিডি (অবশিষ্ট-প্রবাহ যন্ত্র) কী করে?", ["প্রবাহ মাটিতে চুঁইয়ে গেলে, যেমন কোনো মানুষের মধ্যে দিয়ে, কয়েক মিলিসেকেন্ডে বিদ্যুৎ কেটে দেয়", "ভোল্টেজ বাড়ায়", "তাপমাত্রা মাপে", "বিদ্যুৎ জমায়"],
        "ফিউজের চেয়ে অনেক দ্রুত সাড়া দেয় আর প্রাণ বাঁচাতে পারে।"),
    mcq("Why does sound travel faster in steel than in air?", ["Steel's particles are tightly bonded, passing vibrations on very quickly", "Steel is hotter", "Air has no particles", "Sound cannot travel in air"], 0,
        "Sound travels about 5,000 m/s in steel but only about 340 m/s in air.",
        "শব্দ বাতাসের চেয়ে ইস্পাতে দ্রুত চলে কেন?", ["ইস্পাতের কণাগুলো শক্ত করে যুক্ত, তাই কম্পন খুব দ্রুত পরের কণায় যায়", "ইস্পাত গরম", "বাতাসে কণা নেই", "বাতাসে শব্দ চলে না"],
        "ইস্পাতে শব্দ প্রায় 5,000 m/s চলে, বাতাসে মাত্র প্রায় 340 m/s।"),
    mcq("Why is sonar used to check around underwater bridge piers?", ["It maps the riverbed by echoes, showing scour holes that could undermine the foundations", "To scare fish away", "To heat the water", "To paint the piers"], 0,
        "Floods can scour away sand around piers in a single night.",
        "জলের নিচে সেতু-স্তম্ভের চারপাশ পরীক্ষায় সোনার ব্যবহার হয় কেন?", ["প্রতিধ্বনিতে নদীর তল মানচিত্র করে, ভিত দুর্বল করতে পারে এমন ক্ষয়-গর্ত দেখায়", "মাছ তাড়াতে", "জল গরম করতে", "স্তম্ভ রং করতে"],
        "বন্যায় এক রাতেই স্তম্ভের চারপাশের বালি ধুয়ে যেতে পারে।"),
    mcq("What are P-waves and S-waves in an earthquake?", ["P-waves are faster longitudinal waves; S-waves are slower transverse waves that shake side to side", "Both are sound waves in air", "P-waves are light, S-waves are heat", "They are types of ocean wave only"], 0,
        "Warning systems detect P-waves to give a few seconds' notice before stronger shaking.",
        "ভূমিকম্পে পি-তরঙ্গ আর এস-তরঙ্গ কী?", ["পি-তরঙ্গ দ্রুত অনুদৈর্ঘ্য তরঙ্গ; এস-তরঙ্গ ধীর অনুপ্রস্থ তরঙ্গ যা পাশাপাশি নাড়ায়", "দুটোই বাতাসে শব্দ-তরঙ্গ", "পি আলো, এস তাপ", "শুধু সমুদ্রের ঢেউ"],
        "সতর্কতা-ব্যবস্থা পি-তরঙ্গ ধরে জোরালো কাঁপুনির কয়েক সেকেন্ড আগে খবর দেয়।"),
    mcq("How do 'base isolation' bearings protect a bridge in an earthquake?", ["Flexible bearings let the ground move under the bridge while the deck moves much less", "They glue the bridge to the ground", "They make the bridge heavier", "They stop all ground movement"], 0,
        "Rubber and lead layers absorb energy and lengthen the bridge's natural period.",
        "ভূমিকম্পে 'ভিত-বিচ্ছিন্নকারী' বিয়ারিং কীভাবে সেতু রক্ষা করে?", ["নমনীয় বিয়ারিং সেতুর নিচে মাটিকে নড়তে দেয়, অথচ পাটাতন অনেক কম নড়ে", "সেতুকে মাটিতে আঠা দিয়ে আটকায়", "সেতু ভারী করে", "মাটির সব নড়াচড়া থামায়"],
        "রবার আর সিসার স্তর শক্তি শোষে আর সেতুর স্বাভাবিক পর্যায়কাল লম্বা করে।"),
    mcq("What is 'power' in physics?", ["The rate of doing work or transferring energy", "The total energy used", "The force applied", "The mass of a machine"], 0,
        "P = W ÷ t; 1 watt = 1 joule per second.",
        "পদার্থবিদ্যায় 'ক্ষমতা' কী?", ["কার্য করার বা শক্তি স্থানান্তরের হার", "মোট ব্যবহৃত শক্তি", "প্রযুক্ত বল", "যন্ত্রের ভর"],
        "P = W ÷ t; 1 ওয়াট = সেকেন্ডে 1 জুল।"),
    mcq("Two winches lift the same girder to the same height. Winch A takes 20 s, winch B 40 s. Which is true?", ["Both do the same work, but A has twice the power", "A does twice the work", "B has more power", "They have the same power"], 0,
        "Same force and distance means same work; less time means more power.",
        "দুটো উইঞ্চ একই গার্ডার একই উচ্চতায় তোলে। A নেয় 20 s, B 40 s। কোনটা সত্যি?", ["দুটো একই কার্য করে, কিন্তু A-র ক্ষমতা দ্বিগুণ", "A দ্বিগুণ কার্য করে", "B-র ক্ষমতা বেশি", "দুটোর ক্ষমতা সমান"],
        "একই বল আর দূরত্ব মানে একই কার্য; কম সময় মানে বেশি ক্ষমতা।"),
    mcq("Where does the kinetic energy of a braking truck go?", ["Mostly into heat in the brakes and tyres", "It disappears", "Into the driver's muscles", "It turns into mass"], 0,
        "Energy is conserved - long downhill braking can overheat brakes.",
        "ব্রেক-কষা ট্রাকের গতিশক্তি কোথায় যায়?", ["বেশিরভাগই ব্রেক আর টায়ারে তাপ হয়", "মিলিয়ে যায়", "চালকের পেশিতে", "ভরে পরিণত হয়"],
        "শক্তি সংরক্ষিত থাকে - লম্বা ঢালে ব্রেক কষলে ব্রেক অতিরিক্ত গরম হতে পারে।"),
    mcq("What is 'regenerative braking' on electric trains crossing long viaducts?", ["The motors act as generators, turning kinetic energy back into electricity", "Brakes that grow back", "Braking with sand", "Braking that uses more fuel"], 0,
        "It saves energy and reduces brake wear.",
        "লম্বা উড়ালপথ পেরোনো বৈদ্যুতিক ট্রেনে 'পুনরুৎপাদী ব্রেক' কী?", ["মোটর জেনারেটর হয়ে গতিশক্তিকে আবার বিদ্যুতে বদলায়", "যে ব্রেক আবার গজায়", "বালি দিয়ে ব্রেক", "যে ব্রেকে বেশি জ্বালানি লাগে"],
        "শক্তি বাঁচায় আর ব্রেকের ক্ষয় কমায়।"),
    mcq("What does a 'Sankey diagram' show for a machine?", ["How input energy is split into useful and wasted outputs, with arrow widths to scale", "The machine's wiring", "The machine's price", "A map of the site"], 0,
        "It makes efficiency easy to see at a glance.",
        "যন্ত্রের 'স্যাংকি-চিত্র' কী দেখায়?", ["প্রবেশ করা শক্তি কীভাবে কাজের আর অপচয়ের অংশে ভাগ হয়, তিরের প্রস্থ মাপমতো", "যন্ত্রের তারের নকশা", "যন্ত্রের দাম", "নির্মাণস্থলের মানচিত্র"],
        "এক নজরে দক্ষতা বোঝা যায়।"),
    mcq("Why does a dropped hammer fall at the same rate as a dropped bolt (ignoring air resistance)?", ["All objects fall with the same acceleration, g, whatever their mass", "Heavy things fall slower", "Light things fall faster", "Bolts are magnetic"], 0,
        "Galileo showed this; on the Moon, a hammer and feather land together.",
        "পড়ে-যাওয়া হাতুড়ি আর বল্টু একই হারে পড়ে কেন (বায়ুর বাধা বাদ দিলে)?", ["ভর যা-ই হোক সব বস্তু একই ত্বরণ g নিয়ে পড়ে", "ভারী জিনিস ধীরে পড়ে", "হালকা জিনিস দ্রুত পড়ে", "বল্টু চৌম্বক"],
        "গ্যালিলিও এটা দেখান; চাঁদে হাতুড়ি আর পালক একসঙ্গে নামে।"),
    mcq("A tool is thrown horizontally off a bridge. How does its horizontal speed change as it falls (ignoring air)?", ["It stays the same; only the vertical speed increases", "It increases", "It drops to zero at once", "It becomes vertical"], 0,
        "Horizontal and vertical motions are independent - the path is a parabola.",
        "সেতু থেকে একটা যন্ত্র অনুভূমিকভাবে ছোড়া হলো। পড়ার সময় এর অনুভূমিক বেগ কীভাবে বদলায় (বাতাস বাদে)?", ["একই থাকে; শুধু উল্লম্ব বেগ বাড়ে", "বাড়ে", "তখনই শূন্য হয়", "উল্লম্ব হয়ে যায়"],
        "অনুভূমিক আর উল্লম্ব গতি স্বাধীন - পথটা অধিবৃত্ত।"),
)
