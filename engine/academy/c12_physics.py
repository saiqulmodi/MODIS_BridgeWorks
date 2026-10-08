"""Class 12 - Physics (Chief Engineer): beam deflection formulas, cable and arch thrust, vortex
shedding (Strouhal), fatigue cycle counts, prestress, hydrodynamic forces on piers, span-depth
ratios, natural-frequency scaling, fracture mechanics, seismic response and the physics of
monitoring - the analysis behind world-class bridges."""
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


def defl_point(p_kn, l_m, i_e6):
    d = _c(p_kn * 1e3 * (l_m * 1e3) ** 3 / (48 * 200000 * i_e6 * 1e6))
    return _n(f"A steel beam (E = 200 GPa, I = {i_e6:g} x 10⁶ mm⁴) spans {l_m} m with a {p_kn} kN load at mid-span. What is the mid-span deflection? (δ = PL³ ÷ 48EI)",
              f"একটা ইস্পাতের কড়ি (E = 200 GPa, I = {i_e6:g} x 10⁶ mm⁴) {l_m} m বিস্তৃত, মাঝে {p_kn} kN বোঝা। মাঝের বিক্ষেপ কত? (δ = PL³ ÷ 48EI)", d,
              f"δ = {p_kn * 1000:,} N x ({l_m * 1000:,} mm)³ ÷ (48 x 200,000 x {i_e6:g} x 10⁶) = {d:g} mm. Deflection grows with span cubed.",
              f"δ = {p_kn * 1000:,} N x ({l_m * 1000:,} mm)³ ÷ (48 x 200,000 x {i_e6:g} x 10⁶) = {d:g} mm। বিক্ষেপ স্প্যানের ঘনের সঙ্গে বাড়ে।",
              (_c(d * 2), _c(d / 2), _c(d * 8)), " mm")


def defl_udl(w, l_m, i_e6):
    d = _c(5 * w * (l_m * 1e3) ** 4 / (384 * 200000 * i_e6 * 1e6))
    return _n(f"A steel girder (E = 200 GPa, I = {i_e6:g} x 10⁶ mm⁴) spans {l_m} m carrying a uniform load of {w} kN/m. What is the maximum deflection? (δ = 5wL⁴ ÷ 384EI)",
              f"একটা ইস্পাতের গার্ডার (E = 200 GPa, I = {i_e6:g} x 10⁶ mm⁴) {l_m} m বিস্তৃত, {w} kN/m সুষম বোঝা বয়। সর্বোচ্চ বিক্ষেপ কত? (δ = 5wL⁴ ÷ 384EI)", d,
              f"w = {w} N/mm; δ = 5 x {w} x ({l_m * 1000:,})⁴ ÷ (384 x 200,000 x {i_e6:g} x 10⁶) = {d:g} mm.",
              f"w = {w} N/mm; δ = 5 x {w} x ({l_m * 1000:,})⁴ ÷ (384 x 200,000 x {i_e6:g} x 10⁶) = {d:g} mm।",
              (_c(d * 16), _c(d / 5), _c(d * 2)), " mm")


def defl_cant(p_kn, l_m, i_e6):
    d = _c(p_kn * 1e3 * (l_m * 1e3) ** 3 / (3 * 200000 * i_e6 * 1e6))
    return _n(f"A steel cantilever (E = 200 GPa, I = {i_e6:g} x 10⁶ mm⁴) projects {l_m} m with a {p_kn} kN load at its tip. What is the tip deflection? (δ = PL³ ÷ 3EI)",
              f"একটা ইস্পাতের ক্যান্টিলিভার (E = 200 GPa, I = {i_e6:g} x 10⁶ mm⁴) {l_m} m বেরিয়ে আছে, মাথায় {p_kn} kN বোঝা। মাথার বিক্ষেপ কত? (δ = PL³ ÷ 3EI)", d,
              f"δ = {p_kn * 1000:,} x ({l_m * 1000:,})³ ÷ (3 x 200,000 x {i_e6:g} x 10⁶) = {d:g} mm - 16 times a simply supported beam of the same span.",
              f"δ = {p_kn * 1000:,} x ({l_m * 1000:,})³ ÷ (3 x 200,000 x {i_e6:g} x 10⁶) = {d:g} mm - একই স্প্যানের সরল-ঠেকনার কড়ির 16 গুণ।",
              (_c(d / 16), _c(d * 3), _c(d / 2)), " mm")


def cableh(w, span, sag):
    h = _c(w * span * span / (8 * sag))
    return _n(f"A suspension cable carries a uniform deck load of {w} kN/m over a {span} m span with a sag of {sag} m. What is the horizontal cable tension? (H = wL² ÷ 8d)",
              f"একটা ঝুলন্ত তার {span} m স্প্যানে {w} kN/m সুষম পাটাতন-বোঝা বয়, ঝোল {sag} m। তারের অনুভূমিক টান কত? (H = wL² ÷ 8d)", h,
              f"H = {w} x {span}² ÷ (8 x {sag}) = {h:,} kN. Halving the sag doubles the tension - a deep sag is cheaper on cable.",
              f"H = {w} x {span}² ÷ (8 x {sag}) = {h:,} kN। ঝোল অর্ধেক করলে টান দ্বিগুণ - বেশি ঝোলে তার কম লাগে।",
              (_c(w * span / 2), _c(h * 2), _c(w * span * span / sag)), " kN")


def strouhal(v, d):
    f = _c(0.2 * v / d)
    return _n(f"Wind at {v} m/s flows past a round bridge hanger {d} m in diameter. Taking a Strouhal number of 0.2, at what frequency are vortices shed? (f = St v ÷ D)",
              f"{v} m/s বেগের হাওয়া {d} m ব্যাসের একটা গোল সেতু-ঝুলন্ত দণ্ডের পাশ দিয়ে বয়। স্ট্রুহাল সংখ্যা 0.2 ধরে কোন কম্পাঙ্কে ঘূর্ণি নিক্ষিপ্ত হয়? (f = St v ÷ D)", f,
              f"f = 0.2 x {v} ÷ {d} = {f:g} Hz. If this matches the hanger's natural frequency, it may vibrate strongly.",
              f"f = 0.2 x {v} ÷ {d} = {f:g} Hz। এটা দণ্ডের স্বাভাবিক কম্পাঙ্কের সঙ্গে মিললে জোরে কাঁপতে পারে।",
              (_c(v / d), _c(0.2 * v * d), _c(f * 2)), " Hz")


def cycles(trucks, years):
    r = trucks * 365 * years
    return _n(f"A bridge detail sees {trucks:,} heavy trucks a day. How many load cycles does it experience over {years} years?",
              f"একটা সেতুর একটা অংশের উপর দিয়ে দিনে {trucks:,}টি ভারী ট্রাক যায়। {years} বছরে এটা কত বোঝা-চক্র সহ্য করে?", r,
              f"{trucks:,} x 365 x {years} = {r:,} cycles - fatigue design must allow for tens of millions.",
              f"{trucks:,} x 365 x {years} = {r:,} চক্র - ক্লান্তি-নকশায় কোটি কোটি চক্র ধরতে হয়।",
              (trucks * years, trucks * 365, r // 10))


def prestress(p_kn, a_mm2):
    s = _c(p_kn * 1000 / a_mm2)
    return _n(f"A post-tensioned girder of cross-section {a_mm2:,} mm² is stressed with a tendon force of {p_kn:,} kN through its centroid. What uniform compressive stress results?",
              f"{a_mm2:,} mm² প্রস্থচ্ছেদের একটা পরে-টানের গার্ডারে ভরকেন্দ্র দিয়ে {p_kn:,} kN তারের বল দেওয়া হলো। কত সুষম সংনমন-পীড়ন হয়?", s,
              f"σ = P ÷ A = {p_kn * 1000:,} N ÷ {a_mm2:,} mm² = {s:g} N/mm². Loads must pull it back towards zero, never into large tension.",
              f"σ = P ÷ A = {p_kn * 1000:,} N ÷ {a_mm2:,} mm² = {s:g} N/mm²। বোঝা একে শূন্যের দিকে টানবে, কখনো বড় টানে নয়।",
              (_c(p_kn / a_mm2 * 100), _c(s * 10), _c(s / 2)), " N/mm²")


def hydro(v, cd, area):
    f = _c(0.5 * 1000 * v * v * cd * area / 1000)
    return _n(f"Floodwater flows at {v} m/s past a bridge pier presenting {area} m² to the flow, with a drag coefficient of {cd:g}. What force does the water exert? (F = ½ρv²C_dA, ρ = 1,000 kg/m³)",
              f"বন্যার জল {v} m/s বেগে একটা সেতু-স্তম্ভের পাশ দিয়ে বয়, প্রবাহের সামনে {area} m², বাধা-গুণাঙ্ক {cd:g}। জল কত বল দেয়? (F = ½ρv²C_dA, ρ = 1,000 kg/m³)", f,
              f"F = 0.5 x 1,000 x {v}² x {cd:g} x {area} = {f:g} kN - water is about 800 times denser than air, so floods push hard.",
              f"F = 0.5 x 1,000 x {v}² x {cd:g} x {area} = {f:g} kN - জল বাতাসের প্রায় 800 গুণ ঘন, তাই বন্যা জোরে ঠেলে।",
              (_c(f / 2), _c(f * 2), _c(500 * v * cd * area / 1000)), " kN")


def spandepth(span, ratio):
    d = _c(span / ratio)
    return _n(f"A designer uses a span-to-depth ratio of {ratio} for a continuous girder bridge. For a {span} m span, about how deep should the girder be?",
              f"একজন নকশাকার একটানা গার্ডার-সেতুর জন্য স্প্যান-গভীরতা অনুপাত {ratio} ধরেন। {span} m স্প্যানে গার্ডার মোটামুটি কত গভীর হওয়া উচিত?", d,
              f"Depth ≈ span ÷ ratio = {span} ÷ {ratio} = {d:g} m - a quick first check before detailed analysis.",
              f"গভীরতা ≈ স্প্যান ÷ অনুপাত = {span} ÷ {ratio} = {d:g} m - বিস্তারিত বিশ্লেষণের আগে দ্রুত প্রাথমিক যাচাই।",
              (_c(span * ratio / 100), ratio, _c(d * 2)), " m")


def fscale(f1, k_mult, m_mult):
    f2 = _c(f1 * (k_mult / m_mult) ** 0.5)
    return _n(f"A footbridge has a natural frequency of {f1:g} Hz. A retrofit multiplies its stiffness by {k_mult:g} and its mass by {m_mult:g}. What is the new natural frequency? (f ∝ √(k/m))",
              f"একটা পায়ে-চলা সেতুর স্বাভাবিক কম্পাঙ্ক {f1:g} Hz। সংস্কারে দৃঢ়তা {k_mult:g} গুণ আর ভর {m_mult:g} গুণ হলো। নতুন স্বাভাবিক কম্পাঙ্ক কত? (f ∝ √(k/m))", f2,
              f"f2 = {f1:g} x √({k_mult:g} ÷ {m_mult:g}) = {f2:g} Hz.",
              f"f2 = {f1:g} x √({k_mult:g} ÷ {m_mult:g}) = {f2:g} Hz।",
              (_c(f1 * k_mult / m_mult), _c(f1 * k_mult), _c(f1 / 2)), " Hz")


ITEMS = (
    defl_point(100, 10, 400), defl_point(50, 8, 200), defl_point(200, 12, 1000), defl_point(80, 6, 100),
    defl_udl(20, 20, 4000), defl_udl(10, 15, 1500), defl_udl(30, 25, 8000), defl_udl(5, 10, 300),
    defl_cant(10, 3, 100), defl_cant(20, 4, 400), defl_cant(5, 2, 50),
    cableh(100, 500, 50), cableh(80, 300, 30), cableh(150, 1000, 100), cableh(60, 200, 20),
    strouhal(20, 0.2), strouhal(15, 0.3), strouhal(30, 0.5), strouhal(10, 0.25),
    cycles(2000, 50), cycles(5000, 100), cycles(800, 75),
    prestress(5000, 500000), prestress(12000, 800000), prestress(4000, 250000),
    hydro(3, 1.0, 20), hydro(2, 1.2, 30), hydro(4, 0.8, 15),
    spandepth(60, 20), spandepth(120, 25), spandepth(40, 18),
    fscale(4, 2, 1), fscale(3, 1, 4), fscale(2.5, 4, 1), fscale(6, 1, 2.25), fscale(5, 9, 4),
    defl_point(150, 15, 2000), defl_point(30, 5, 80), defl_udl(15, 30, 20000), defl_cant(15, 2.5, 150), defl_cant(8, 5, 600),
    cableh(120, 800, 80), strouhal(25, 0.4), cycles(10000, 120), prestress(8000, 400000), hydro(5, 1.0, 12),
    spandepth(90, 22), spandepth(200, 30),
    mcq("Why do engineers limit bridge deflection under traffic, typically to about span ÷ 800?", ["To keep the deck comfortable, protect surfacing and joints, and avoid alarming users", "Deflection is always dangerous at any size", "To save paint", "Codes require zero deflection"], 0,
        "Strength and stiffness are separate checks - a strong beam can still be too bouncy.",
        "প্রকৌশলীরা যান-বোঝায় সেতুর বিক্ষেপ সাধারণত প্রায় স্প্যান ÷ 800-এ সীমিত রাখেন কেন?", ["পাটাতন আরামদায়ক রাখতে, উপরের স্তর আর জোড় রক্ষা করতে আর ব্যবহারকারীদের ভয় না দিতে", "যেকোনো মাপের বিক্ষেপ সবসময় বিপজ্জনক", "রং বাঁচাতে", "নিয়মে শূন্য বিক্ষেপ চাই"],
        "শক্তি আর দৃঢ়তা আলাদা যাচাই - শক্ত কড়িও বেশি লাফাতে পারে।"),
    mcq("By how much does a simply supported beam's deflection grow if its span doubles under the same uniform load per metre?", ["16 times", "2 times", "4 times", "8 times"], 0,
        "δ ∝ L⁴ for a uniform load: 2⁴ = 16.",
        "প্রতি মিটারে একই সুষম বোঝায় সরল-ঠেকনার কড়ির স্প্যান দ্বিগুণ হলে বিক্ষেপ কত বাড়ে?", ["16 গুণ", "2 গুণ", "4 গুণ", "8 গুণ"],
        "সুষম বোঝায় δ ∝ L⁴: 2⁴ = 16।"),
    mcq("Why does a deeper sag reduce the tension in a suspension cable?", ["The cable then carries the load at a steeper angle, needing less horizontal pull", "Sag makes the deck lighter", "Tension is unrelated to sag", "Deeper sag adds more steel"], 0,
        "But very deep sags need taller, costlier towers - designers balance the two.",
        "বেশি ঝোল ঝুলন্ত তারের টান কমায় কেন?", ["তখন তার খাড়া কোণে বোঝা বয়, কম অনুভূমিক টান লাগে", "ঝোল পাটাতন হালকা করে", "টান ঝোলের সঙ্গে সম্পর্কহীন", "বেশি ঝোলে বেশি ইস্পাত"],
        "তবে খুব বেশি ঝোলে উঁচু, দামি মিনার লাগে - নকশাকাররা দুটোর ভারসাম্য রাখেন।"),
    mcq("What carries the horizontal cable pull at each end of a suspension bridge?", ["Massive anchorages that resist it with their weight and the ground", "The deck alone", "The wind", "Nothing - it cancels out automatically"], 0,
        "Self-anchored suspension bridges tie the cable into the deck instead.",
        "ঝুলন্ত সেতুর প্রতি প্রান্তে তারের অনুভূমিক টান কী বয়?", ["বিশাল নোঙর-কাঠামো, যা নিজের ওজন আর মাটি দিয়ে রোধ করে", "শুধু পাটাতন", "হাওয়া", "কিছুই না - নিজে থেকে কেটে যায়"],
        "স্ব-নোঙর ঝুলন্ত সেতু তার বদলে তারকে পাটাতনে বাঁধে।"),
    mcq("Why does an arch push outwards at its supports?", ["Its curved shape carries load in compression, which has a horizontal component - the thrust", "Arches are in tension", "Arches have no supports", "The keystone pulls inwards only"], 0,
        "Tied arches use a tie beam to carry the thrust instead of the ground.",
        "খিলান তার ঠেকনায় বাইরের দিকে ঠেলে কেন?", ["বাঁকা আকার সংনমনে বোঝা বয়, যার একটা অনুভূমিক উপাংশ আছে - ঠেলা", "খিলান টানে থাকে", "খিলানের ঠেকনা নেই", "চাবিপাথর শুধু ভেতরে টানে"],
        "বাঁধা-খিলান মাটির বদলে একটা টানা-কড়ি দিয়ে ঠেলা বয়।"),
    mcq("What is the 'Strouhal number'?", ["A dimensionless number linking vortex-shedding frequency to flow speed and object size", "The number of bridge cables", "A type of bolt", "The speed of sound"], 0,
        "For a circular cylinder it is about 0.2 over a wide range of speeds.",
        "'স্ট্রুহাল সংখ্যা' কী?", ["মাত্রাহীন সংখ্যা, যা ঘূর্ণি-নিক্ষেপের কম্পাঙ্ককে প্রবাহের বেগ আর বস্তুর মাপের সঙ্গে জোড়ে", "সেতুর তারের সংখ্যা", "এক রকম বল্টু", "শব্দের বেগ"],
        "বৃত্তাকার চোঙে অনেক গতির পরিসরে এটা প্রায় 0.2।"),
    mcq("What is 'lock-in' in vortex-induced vibration?", ["When shedding frequency latches onto the structure's natural frequency over a range of wind speeds, causing sustained vibration", "Locking the bridge gates", "A type of bearing", "A computer error"], 0,
        "Dampers or shape changes break the lock-in.",
        "ঘূর্ণি-জনিত কম্পনে 'আটকে-যাওয়া' (লক-ইন) কী?", ["হাওয়ার একটা গতির পরিসরে নিক্ষেপের কম্পাঙ্ক কাঠামোর স্বাভাবিক কম্পাঙ্কে আটকে যায়, টানা কম্পন ঘটায়", "সেতুর ফটক বন্ধ", "এক রকম বিয়ারিং", "কম্পিউটারের ভুল"],
        "ড্যাম্পার বা আকারের বদল আটকে-যাওয়া ভাঙে।"),
    mcq("What is 'flutter' of a bridge deck?", ["A self-exciting aeroelastic instability where wind feeds energy into twisting and bending motions", "Flags moving on the bridge", "Birds landing", "Paint peeling"], 0,
        "It destroyed the Tacoma Narrows Bridge; decks are wind-tunnel tested to avoid it.",
        "সেতুর পাটাতনের 'ফ্লাটার' কী?", ["নিজে-উত্তেজিত বায়ু-স্থিতিস্থাপক অস্থিরতা, যেখানে হাওয়া মোচড় আর বাঁকার গতিতে শক্তি জোগায়", "সেতুতে পতাকা দোলা", "পাখি বসা", "রং ওঠা"],
        "এটাই ট্যাকোমা ন্যারোজ সেতু ধ্বংস করেছিল; এড়াতে পাটাতন বায়ু-সুড়ঙ্গে পরীক্ষা হয়।"),
    mcq("What is 'rain-wind induced vibration' of stay cables?", ["Rivulets of rain on the cable change its shape in the wind, causing large oscillations", "Rain making cables heavier only", "Lightning strikes", "Cables rusting in rain"], 0,
        "Helical ribs or dimples on the cable sheath help prevent it.",
        "টানা-তারে 'বৃষ্টি-হাওয়া জনিত কম্পন' কী?", ["তারের উপর বৃষ্টির ধারা হাওয়ায় এর আকার বদলায়, বড় দোলন ঘটায়", "বৃষ্টি শুধু তার ভারী করে", "বাজ পড়া", "বৃষ্টিতে তারে মরচে"],
        "তারের আবরণে পেঁচানো খাঁজ বা গর্ত এটা ঠেকাতে সাহায্য করে।"),
    mcq("What does an 'S-N curve' show for a bridge steel detail?", ["The stress range it can withstand for a given number of load cycles before fatigue cracking", "Speed against noise", "Stress against nothing", "Snow against nitrogen"], 0,
        "Lower stress ranges allow many more cycles.",
        "সেতুর ইস্পাতের একটা অংশের জন্য 'এস-এন বক্ররেখা' কী দেখায়?", ["ক্লান্তি-ফাটলের আগে নির্দিষ্ট সংখ্যক বোঝা-চক্রে এটা কত পীড়ন-পরিসর সহ্য করে", "গতি বনাম শব্দ", "পীড়ন বনাম কিছুই না", "তুষার বনাম নাইট্রোজেন"],
        "কম পীড়ন-পরিসরে অনেক বেশি চক্র চলে।"),
    mcq("Why are welded details often the weak points for fatigue?", ["Welds create stress concentrations and tiny flaws where cracks can start", "Welds are always stronger than steel", "Welds never carry load", "Fatigue only happens in bolts"], 0,
        "Smooth weld profiles and good detailing improve fatigue life.",
        "ঝালাই-করা অংশ প্রায়ই ক্লান্তির দুর্বল জায়গা কেন?", ["ঝালাই পীড়ন-ঘনীভবন আর খুদে ত্রুটি তৈরি করে, যেখান থেকে ফাটল শুরু হতে পারে", "ঝালাই সবসময় ইস্পাতের চেয়ে শক্ত", "ঝালাই কখনো বোঝা বয় না", "ক্লান্তি শুধু বল্টুতে হয়"],
        "মসৃণ ঝালাই-আকার আর ভালো নকশা ক্লান্তি-আয়ু বাড়ায়।"),
    mcq("What is 'fracture toughness'?", ["A material's resistance to the growth of an existing crack", "Its hardness", "Its melting point", "Its colour"], 0,
        "It decides how long a crack can grow before sudden failure.",
        "'ভাঙন-দৃঢ়তা' কী?", ["বিদ্যমান ফাটল বাড়ার বিরুদ্ধে উপাদানের প্রতিরোধ", "এর কাঠিন্য", "এর গলনাঙ্ক", "এর রং"],
        "হঠাৎ ব্যর্থতার আগে একটা ফাটল কত বড় হতে পারে, তা ঠিক করে।"),
    mcq("Why do inspectors measure crack lengths in steel bridges over time?", ["Crack growth rate shows how long until the crack becomes critical, so repairs can be scheduled", "To decorate reports", "Cracks never grow", "To count bolts"], 0,
        "This 'damage-tolerant' approach keeps bridges safe despite small flaws.",
        "পরিদর্শকরা ইস্পাতের সেতুতে সময়ের সঙ্গে ফাটলের দৈর্ঘ্য মাপেন কেন?", ["ফাটল বাড়ার হার দেখায় কতদিনে সংকটজনক হবে, তাই মেরামত সময়মতো করা যায়", "প্রতিবেদন সাজাতে", "ফাটল কখনো বাড়ে না", "বল্টু গুনতে"],
        "এই 'ক্ষতি-সহনশীল' পদ্ধতি ছোট ত্রুটি সত্ত্বেও সেতু নিরাপদ রাখে।"),
    mcq("What is the purpose of drilling a 'crack-stop hole' at the tip of a fatigue crack?", ["It blunts the sharp crack tip, reducing the stress concentration so the crack stops growing for a while", "To drain water", "To insert a sensor only", "To weaken the steel"], 0,
        "It is a temporary measure until a permanent repair.",
        "ক্লান্তি-ফাটলের মাথায় 'ফাটল-থামানো গর্ত' করার উদ্দেশ্য কী?", ["ধারালো ফাটলের মাথা ভোঁতা করে পীড়ন-ঘনীভবন কমায়, তাই কিছুদিন ফাটল বাড়া থামে", "জল বার করতে", "শুধু সেন্সর বসাতে", "ইস্পাত দুর্বল করতে"],
        "স্থায়ী মেরামতের আগে পর্যন্ত এটা অস্থায়ী ব্যবস্থা।"),
    mcq("Why is prestressed concrete efficient for long-span girders?", ["Pre-compression cancels much of the tension from loads, so the whole section works and cracks are avoided", "It uses no steel", "It is lighter than air", "It never deflects"], 0,
        "Draped tendons can also push upwards to counter the load.",
        "লম্বা-স্প্যানের গার্ডারে আগাম-পীড়িত কংক্রিট দক্ষ কেন?", ["আগাম-সংনমন বোঝার টানের অনেকটা কাটিয়ে দেয়, তাই পুরো প্রস্থচ্ছেদ কাজ করে আর ফাটল এড়ানো যায়", "এতে ইস্পাত লাগে না", "বাতাসের চেয়ে হালকা", "কখনো বাঁকে না"],
        "বাঁকা পথে বসানো তার বোঝার বিরুদ্ধে উপরের দিকেও ঠেলতে পারে।"),
    mcq("What are 'prestress losses'?", ["Reductions in tendon force over time from creep, shrinkage, steel relaxation and friction", "Money lost on a project", "Cables falling off", "Concrete washing away"], 0,
        "Designers allow for them so enough prestress remains for the bridge's life.",
        "'আগাম-পীড়ন হ্রাস' কী?", ["ক্রিপ, সংকোচন, ইস্পাতের শিথিলতা আর ঘর্ষণে সময়ের সঙ্গে তারের বল কমা", "প্রকল্পে টাকা হারানো", "তার খুলে পড়া", "কংক্রিট ধুয়ে যাওয়া"],
        "নকশাকাররা এগুলো ধরেন, যাতে সেতুর আয়ু জুড়ে যথেষ্ট আগাম-পীড়ন থাকে।"),
    mcq("Why does water exert so much more force on a pier than wind of the same speed?", ["Water is about 800 times denser than air, and drag force is proportional to density", "Water is always faster", "Wind has no force", "Piers attract water"], 0,
        "Debris and ice can add even more load in floods.",
        "একই বেগের হাওয়ার চেয়ে জল স্তম্ভে এত বেশি বল দেয় কেন?", ["জল বাতাসের প্রায় 800 গুণ ঘন, আর টানা-বল ঘনত্বের সমানুপাতিক", "জল সবসময় দ্রুত", "হাওয়ার বল নেই", "স্তম্ভ জল টানে"],
        "বন্যায় ভেসে-আসা জিনিস আর বরফ আরও বোঝা যোগ করতে পারে।"),
    mcq("What is 'ship impact' design for river and sea bridges?", ["Designing piers and protective fenders or islands to survive or deflect collisions from vessels", "Painting ships", "Allowing ships to hit freely", "Building only on land"], 0,
        "The Sunshine Skyway (USA) was rebuilt with protection after a ship strike.",
        "নদী আর সমুদ্র-সেতুর 'জাহাজ-ধাক্কা' নকশা কী?", ["স্তম্ভ আর সুরক্ষা-বেড়া বা দ্বীপ এমনভাবে নকশা যাতে জাহাজের ধাক্কা সয় বা ঘুরিয়ে দেয়", "জাহাজ রং করা", "জাহাজকে ইচ্ছেমতো ধাক্কা দিতে দেওয়া", "শুধু ডাঙায় নির্মাণ"],
        "জাহাজের ধাক্কার পরে সানশাইন স্কাইওয়ে (আমেরিকা) সুরক্ষাসহ আবার বানানো হয়।"),
    mcq("What is a 'response spectrum' in earthquake engineering?", ["A graph showing the peak response of structures of different natural periods to a given earthquake", "A rainbow", "A list of earthquakes", "A type of seismometer"], 0,
        "Engineers read off the design force for their bridge's period.",
        "ভূমিকম্প-প্রকৌশলে 'সাড়া-বর্ণালি' কী?", ["লেখচিত্র, যা দেখায় আলাদা স্বাভাবিক পর্যায়কালের কাঠামো একটা ভূমিকম্পে কতটা সর্বোচ্চ সাড়া দেয়", "রামধনু", "ভূমিকম্পের তালিকা", "এক রকম ভূকম্পমাপক"],
        "প্রকৌশলীরা তাঁদের সেতুর পর্যায়কাল দেখে নকশা-বল পড়েন।"),
    mcq("Why does base isolation lengthen a bridge's natural period?", ["Flexible bearings make the structure 'softer' sideways, moving its period away from the strongest earthquake shaking", "It makes the bridge heavier", "It shortens the period", "It has no effect on period"], 0,
        "Longer periods attract smaller accelerations, though displacements grow.",
        "ভিত-বিচ্ছিন্নকরণ সেতুর স্বাভাবিক পর্যায়কাল লম্বা করে কেন?", ["নমনীয় বিয়ারিং কাঠামোকে পাশের দিকে 'নরম' করে, পর্যায়কাল ভূমিকম্পের সবচেয়ে জোরালো কাঁপুনি থেকে সরায়", "সেতু ভারী করে", "পর্যায়কাল ছোট করে", "পর্যায়কালে প্রভাব নেই"],
        "লম্বা পর্যায়কালে ত্বরণ কম আসে, যদিও সরণ বাড়ে।"),
    mcq("What is 'ductile design' for earthquake-resistant piers?", ["Detailing piers so they can bend and yield in a controlled way without collapsing, absorbing energy", "Making piers brittle", "Using no steel", "Making piers as stiff as possible only"], 0,
        "Closely spaced confining links keep the concrete core intact.",
        "ভূমিকম্প-সহ স্তম্ভের 'নমনীয় নকশা' কী?", ["স্তম্ভকে এমনভাবে গড়া যাতে না ভেঙে নিয়ন্ত্রিতভাবে বাঁকতে আর নতি স্বীকার করতে পারে, শক্তি শোষে", "স্তম্ভ ভঙ্গুর করা", "ইস্পাত না ব্যবহার", "শুধু স্তম্ভ যত সম্ভব শক্ত করা"],
        "ঘন করে বসানো বাঁধন-রিং কংক্রিটের মজ্জা অটুট রাখে।"),
    mcq("What is 'liquefaction' and why does it threaten bridge foundations?", ["Shaking turns saturated loose sand into a fluid-like state, so it loses strength and foundations can sink or tilt", "Melting of steel", "Concrete turning to water", "Rain filling a river"], 0,
        "Deep piles to firm layers or ground improvement reduce the risk.",
        "'তরলীভবন' কী আর সেতুর ভিতকে কেন বিপদে ফেলে?", ["কাঁপুনিতে জলে-ভেজা আলগা বালি তরলের মতো হয়ে শক্তি হারায়, ভিত বসে বা হেলে যেতে পারে", "ইস্পাত গলা", "কংক্রিট জল হওয়া", "বৃষ্টিতে নদী ভরা"],
        "শক্ত স্তর পর্যন্ত গভীর পাইল বা মাটি-উন্নয়ন ঝুঁকি কমায়।"),
    mcq("What is 'P-delta effect'?", ["Extra bending caused when a vertical load acts on a structure that has already deflected sideways", "A type of bolt", "Price changes", "A wave in water"], 0,
        "Tall slender piers and towers must check it.",
        "'পি-ডেল্টা প্রভাব' কী?", ["পাশে আগেই সরে-যাওয়া কাঠামোয় উল্লম্ব বোঝা কাজ করলে বাড়তি বাঁকানো", "এক রকম বল্টু", "দামের বদল", "জলের ঢেউ"],
        "উঁচু সরু স্তম্ভ আর মিনারে এটা যাচাই করতে হয়।"),
    mcq("What is 'structural health monitoring' (SHM)?", ["Permanent sensors that measure strains, movements, vibrations and temperatures to track a bridge's condition", "A doctor's check-up for workers", "Painting the bridge", "Counting toll money"], 0,
        "Changes in natural frequency can reveal hidden damage.",
        "'কাঠামোগত স্বাস্থ্য-নজরদারি' (এসএইচএম) কী?", ["স্থায়ী সেন্সর, যা বিকৃতি, নড়াচড়া, কম্পন আর তাপমাত্রা মেপে সেতুর অবস্থা নজরে রাখে", "কর্মীদের ডাক্তারি পরীক্ষা", "সেতু রং করা", "টোলের টাকা গোনা"],
        "স্বাভাবিক কম্পাঙ্কের বদল লুকোনো ক্ষতি প্রকাশ করতে পারে।"),
    mcq("Why can a drop in a bridge's natural frequency signal damage?", ["Cracks or loosened connections reduce stiffness, and frequency falls with lower stiffness", "Frequency rises with damage", "Temperature never affects frequency", "It cannot signal anything"], 0,
        "Engineers correct for temperature, which also changes stiffness slightly.",
        "সেতুর স্বাভাবিক কম্পাঙ্ক কমে যাওয়া কেন ক্ষতির সংকেত হতে পারে?", ["ফাটল বা ঢিলে জোড় দৃঢ়তা কমায়, আর কম দৃঢ়তায় কম্পাঙ্ক কমে", "ক্ষতিতে কম্পাঙ্ক বাড়ে", "তাপমাত্রা কখনো কম্পাঙ্কে প্রভাব ফেলে না", "কিছুরই সংকেত হতে পারে না"],
        "প্রকৌশলীরা তাপমাত্রার জন্য সংশোধন করেন, যা দৃঢ়তাও একটু বদলায়।"),
    mcq("How does GNSS (GPS) monitoring help on long-span bridges?", ["Receivers on towers and deck measure movements to millimetres in real time", "It guides traffic only", "It measures rainfall", "It replaces all inspections"], 0,
        "It tracks deck sway in wind and tower movements with temperature.",
        "লম্বা-স্প্যানের সেতুতে জিএনএসএস (জিপিএস) নজরদারি কীভাবে সাহায্য করে?", ["মিনার আর পাটাতনের গ্রাহক যন্ত্র বাস্তব সময়ে মিলিমিটার পর্যন্ত নড়াচড়া মাপে", "শুধু যান চালায়", "বৃষ্টি মাপে", "সব পরিদর্শনের বদলি"],
        "হাওয়ায় পাটাতনের দোলা আর তাপমাত্রায় মিনারের নড়াচড়া নজরে রাখে।"),
    mcq("What does an accelerometer on a bridge deck measure?", ["Accelerations from vibrations, used to find natural frequencies and comfort levels", "Vehicle speeds", "Temperature", "Cable tension directly"], 0,
        "Footbridge comfort limits are often set in terms of acceleration.",
        "সেতুর পাটাতনে অ্যাক্সিলেরোমিটার কী মাপে?", ["কম্পন থেকে ত্বরণ, যা দিয়ে স্বাভাবিক কম্পাঙ্ক আর আরামের মাত্রা বের হয়", "গাড়ির গতি", "তাপমাত্রা", "সরাসরি তারের টান"],
        "পায়ে-চলা সেতুর আরামের সীমা প্রায়ই ত্বরণের হিসেবে ঠিক হয়।"),
    mcq("How can stay-cable tension be measured without cutting the cable?", ["By measuring its vibration frequency - like a guitar string, tension sets the pitch", "By weighing the bridge", "By painting it", "It cannot be measured"], 0,
        "T ≈ 4mL²f² for a taut string of mass per length m and length L.",
        "তার না কেটে টানা-তারের টান কীভাবে মাপা যায়?", ["কম্পনের কম্পাঙ্ক মেপে - গিটারের তারের মতো টানই সুর ঠিক করে", "সেতু ওজন করে", "রং করে", "মাপা যায় না"],
        "দৈর্ঘ্যপ্রতি ভর m আর দৈর্ঘ্য L-এর টানটান তারে T ≈ 4mL²f²।"),
    mcq("What is 'acoustic emission' monitoring of bridge cables?", ["Sensors listen for the tiny sound of wires snapping inside a cable, revealing hidden corrosion", "Playing music to cables", "Measuring traffic noise", "A loudspeaker system"], 0,
        "It is used on suspension cables where wires cannot be seen.",
        "সেতুর তারের 'শব্দ-নিঃসরণ' নজরদারি কী?", ["সেন্সর তারের ভেতরে সরু তার ছেঁড়ার খুদে শব্দ শোনে, লুকোনো ক্ষয় প্রকাশ করে", "তারকে গান শোনানো", "যানবাহনের শব্দ মাপা", "মাইক-ব্যবস্থা"],
        "ঝুলন্ত তারে ব্যবহার হয়, যেখানে ভেতরের তার দেখা যায় না।"),
    mcq("What is 'ground-penetrating radar' (GPR) used for on bridge decks?", ["Sending radio waves into concrete to locate rebar, voids and deterioration without drilling", "Detecting aircraft", "Measuring wind", "Finding underground water only"], 0,
        "Reflections from different materials build a picture of the inside.",
        "সেতুর পাটাতনে 'ভূ-ভেদী রাডার' (জিপিআর) কীসের জন্য ব্যবহার হয়?", ["কংক্রিটে বেতার-তরঙ্গ পাঠিয়ে না খুঁড়েই রড, ফাঁক আর অবনতি খোঁজা", "বিমান ধরা", "হাওয়া মাপা", "শুধু মাটির নিচের জল খোঁজা"],
        "আলাদা উপাদানের প্রতিফলন ভেতরের ছবি গড়ে।"),
    mcq("What is 'infrared thermography' used for in bridge inspection?", ["Spotting delaminations, which heat and cool differently from sound concrete", "Taking holiday photos", "Measuring traffic", "Heating the deck"], 0,
        "It works best when the sun is warming or cooling the deck.",
        "সেতু-পরিদর্শনে 'অবলোহিত তাপচিত্র' কীসের জন্য ব্যবহার হয়?", ["স্তর-আলগা জায়গা ধরা, যা অক্ষত কংক্রিটের থেকে আলাদাভাবে গরম আর ঠান্ডা হয়", "ছুটির ছবি তোলা", "যান মাপা", "পাটাতন গরম করা"],
        "রোদ যখন পাটাতন গরম বা ঠান্ডা করছে তখন সবচেয়ে ভালো কাজ করে।"),
    mcq("How does a 'half-cell potential' survey find corroding rebar?", ["It measures the electrical potential of the steel; more negative readings suggest active corrosion", "It counts half the cells in concrete", "It weighs the steel", "It measures rainfall"], 0,
        "Readings are mapped to target repairs.",
        "'অর্ধকোষ-বিভব' জরিপ কীভাবে ক্ষয়ে-যাওয়া রড খোঁজে?", ["ইস্পাতের বৈদ্যুতিক বিভব মাপে; বেশি ঋণাত্মক পাঠ সক্রিয় ক্ষয় বোঝায়", "কংক্রিটের অর্ধেক কোষ গোনে", "ইস্পাত ওজন করে", "বৃষ্টি মাপে"],
        "মেরামতের লক্ষ্য ঠিক করতে পাঠগুলোর মানচিত্র বানানো হয়।"),
    mcq("Why do laser scanners and photogrammetry help bridge engineers?", ["They capture millions of accurate 3D points to compare shapes over time and build digital models", "They cut steel", "They replace concrete", "They count vehicles only"], 0,
        "Small changes in shape can reveal settlement or damage.",
        "লেজার-স্ক্যানার আর ফটোগ্রামেট্রি সেতু-প্রকৌশলীদের কীভাবে সাহায্য করে?", ["লক্ষ লক্ষ নিখুঁত ত্রিমাত্রিক বিন্দু ধরে সময়ের সঙ্গে আকার তুলনা আর ডিজিটাল মডেল গড়ে", "ইস্পাত কাটে", "কংক্রিটের বদলি", "শুধু যান গোনে"],
        "আকারের ছোট বদল বসে-যাওয়া বা ক্ষতি প্রকাশ করতে পারে।"),
    mcq("Why do the longest bridges have to consider the curvature of the Earth?", ["Over kilometres, vertical towers are not quite parallel - the Humber Bridge towers are about 36 mm further apart at the top", "The Earth is flat", "Curvature only matters for ships", "It never matters"], 0,
        "At long spans, small geometric effects become measurable.",
        "সবচেয়ে লম্বা সেতুতে পৃথিবীর বক্রতা কেন ধরতে হয়?", ["কয়েক কিলোমিটারে খাড়া মিনারগুলো পুরো সমান্তরাল নয় - হাম্বার সেতুর মিনার মাথায় প্রায় 36 mm বেশি দূরে", "পৃথিবী সমতল", "বক্রতা শুধু জাহাজের জন্য গুরুত্বপূর্ণ", "কখনো গুরুত্বপূর্ণ নয়"],
        "লম্বা স্প্যানে ছোট জ্যামিতিক প্রভাবও মাপা যায়।"),
    mcq("What is 'creep' and why must long concrete bridges allow for it over decades?", ["Concrete slowly keeps deforming under sustained stress, changing deflections and prestress", "Concrete shrinking only in fire", "Insects crawling", "Steel melting"], 0,
        "Builders pre-camber spans to end up at the right level.",
        "'ক্রিপ' কী আর লম্বা কংক্রিট-সেতুকে কয়েক দশক ধরে কেন এটা ধরতে হয়?", ["টানা পীড়নে কংক্রিট ধীরে বিকৃত হতে থাকে, বিক্ষেপ আর আগাম-পীড়ন বদলায়", "শুধু আগুনে কংক্রিট ছোট হওয়া", "পোকা হেঁটে বেড়ানো", "ইস্পাত গলা"],
        "নির্মাতারা স্প্যান আগে থেকে বাঁকিয়ে রাখেন, যাতে শেষে ঠিক উচ্চতায় থাকে।"),
    mcq("What is 'shrinkage' of concrete?", ["Volume reduction as concrete dries and as cement reacts, which can cause cracking if restrained", "Concrete getting stronger", "Concrete expanding in heat only", "Washing away of sand"], 0,
        "Good curing and joints control shrinkage cracking.",
        "কংক্রিটের 'সংকোচন' কী?", ["কংক্রিট শুকোনো আর সিমেন্টের বিক্রিয়ায় আয়তন কমা, আটকানো থাকলে ফাটল ধরাতে পারে", "কংক্রিট শক্ত হওয়া", "শুধু গরমে প্রসারণ", "বালি ধুয়ে যাওয়া"],
        "ভালো কিউরিং আর জোড় সংকোচন-ফাটল নিয়ন্ত্রণ করে।"),
    mcq("What is the 'limit state' design approach?", ["Checking that a bridge stays safe (ultimate limit state) and usable (serviceability limit state) with suitable safety factors", "Designing with no safety factors", "Limiting the bridge's length", "A speed limit"], 0,
        "Loads are increased and strengths reduced by partial factors.",
        "'সীমা-অবস্থা' নকশা-পদ্ধতি কী?", ["উপযুক্ত নিরাপত্তা-গুণকসহ সেতু নিরাপদ (চূড়ান্ত সীমা) আর ব্যবহারযোগ্য (সেবা-সীমা) থাকে কিনা যাচাই", "নিরাপত্তা-গুণক ছাড়া নকশা", "সেতুর দৈর্ঘ্য সীমিত করা", "গতিসীমা"],
        "আংশিক গুণকে বোঝা বাড়ানো আর শক্তি কমানো হয়।"),
    mcq("What is 'redundancy' in a bridge structure?", ["Having alternative load paths so the failure of one member does not cause collapse", "Having unnecessary parts", "Firing workers", "Using only one cable"], 0,
        "Many cable-stayed bridges are designed to survive the loss of any single cable.",
        "সেতু-কাঠামোয় 'অতিরিক্ততা' (রিডান্ড্যান্সি) কী?", ["বিকল্প বোঝা-পথ থাকা, যাতে একটা অংশ ব্যর্থ হলে ধস না হয়", "অপ্রয়োজনীয় অংশ থাকা", "কর্মী ছাঁটাই", "শুধু একটা তার ব্যবহার"],
        "অনেক কেবল-স্টেড সেতু যেকোনো একটা তার হারালেও টিকে থাকতে নকশা হয়।"),
    mcq("What is a 'fracture-critical member'?", ["A tension member whose failure would cause collapse because no alternative load path exists", "A member that is already broken", "A compression strut only", "A decorative rail"], 0,
        "Such members receive extra-close inspection.",
        "'ভাঙন-সংকটজনক অংশ' কী?", ["একটা টান-অংশ, যার ব্যর্থতায় ধস হবে, কারণ বিকল্প বোঝা-পথ নেই", "আগেই ভাঙা অংশ", "শুধু সংনমন-ঠেকনা", "সাজানোর রেলিং"],
        "এমন অংশ বাড়তি কাছ থেকে পরিদর্শন পায়।"),
    mcq("What lesson did the 2018 Morandi Bridge collapse in Genoa reinforce?", ["Corrosion of hidden prestressing tendons in non-redundant stays can be catastrophic - inspection access and redundancy matter", "Bridges never need inspection", "Concrete never corrodes", "Wind caused it alone"], 0,
        "Many countries reviewed their inspection of similar bridges afterwards.",
        "2018 সালে জেনোয়ার মোরান্ডি সেতুর ধস কোন শিক্ষা জোরালো করে?", ["অতিরিক্ততাহীন টানা-অংশে লুকোনো আগাম-টানের তারের ক্ষয় বিপর্যয়কর হতে পারে - পরিদর্শনের নাগাল আর অতিরিক্ততা জরুরি", "সেতুর পরিদর্শন লাগে না", "কংক্রিট কখনো ক্ষয়ে না", "শুধু হাওয়ায় হয়েছিল"],
        "পরে অনেক দেশ একই রকম সেতুর পরিদর্শন পর্যালোচনা করে।"),
    mcq("What is 'robustness' in bridge design?", ["The ability to withstand unforeseen events like impacts or local failures without disproportionate collapse", "Being very heavy", "Being cheap", "Having bright paint"], 0,
        "Ties, continuity and redundancy all improve robustness.",
        "সেতু-নকশায় 'মজবুতি' (রোবাস্টনেস) কী?", ["ধাক্কা বা স্থানীয় ব্যর্থতার মতো অপ্রত্যাশিত ঘটনায় অসমানুপাতিক ধস ছাড়া টিকে থাকার ক্ষমতা", "খুব ভারী হওয়া", "সস্তা হওয়া", "উজ্জ্বল রং থাকা"],
        "বাঁধন, একটানা হওয়া আর অতিরিক্ততা মজবুতি বাড়ায়।"),
    mcq("Why are bridge bearings designed to be replaceable?", ["They wear out long before the bridge does, so jacking points and access are planned for swapping them", "They never wear", "They are decorative", "Bearings are glued forever"], 0,
        "A bridge may need new bearings two or three times in its life.",
        "সেতুর বিয়ারিং বদলযোগ্য করে নকশা হয় কেন?", ["সেতুর অনেক আগে এগুলো ক্ষয়ে যায়, তাই বদলানোর জন্য জ্যাক বসানোর জায়গা আর নাগাল পরিকল্পনা করা হয়", "কখনো ক্ষয়ে না", "সাজানোর জিনিস", "বিয়ারিং চিরকাল আঠায় আটকানো"],
        "সেতুর জীবনে দু-তিনবার নতুন বিয়ারিং লাগতে পারে।"),
    mcq("What is 'dynamic amplification' of vehicle loads?", ["Moving, bouncing vehicles produce larger effects than the same weight standing still", "Vehicles getting heavier at night", "Loads shrinking when moving", "Amplifiers on bridges"], 0,
        "Codes add an impact allowance, especially for rough joints and short spans.",
        "যানবাহনের বোঝার 'গতিশীল বর্ধন' কী?", ["চলন্ত, লাফানো গাড়ি একই ওজন দাঁড়িয়ে থাকার চেয়ে বড় প্রভাব ফেলে", "রাতে গাড়ি ভারী হওয়া", "চলার সময় বোঝা কমা", "সেতুতে লাউডস্পিকার"],
        "নিয়মে ধাক্কার বাড়তি ধরা হয়, বিশেষত এবড়োখেবড়ো জোড় আর ছোট স্প্যানে।"),
    mcq("Why are high-speed rail bridges checked for resonance from trains?", ["Regularly spaced axles at high speed can pump energy into the deck at its natural frequency", "Trains are silent", "Rails never vibrate", "Speed has no effect"], 0,
        "Excess deck acceleration can destabilise ballast and affect safety.",
        "উচ্চগতির রেলসেতু ট্রেন থেকে অনুনাদের জন্য যাচাই করা হয় কেন?", ["উচ্চগতিতে নিয়মিত দূরত্বের অক্ষ পাটাতনের স্বাভাবিক কম্পাঙ্কে শক্তি জোগাতে পারে", "ট্রেন নিঃশব্দ", "রেল কখনো কাঁপে না", "গতির প্রভাব নেই"],
        "অতিরিক্ত পাটাতন-ত্বরণ পাথরকুচি অস্থির করে নিরাপত্তায় প্রভাব ফেলতে পারে।"),
    mcq("What is the purpose of a 'load test' on a new bridge?", ["Placing known heavy loads and measuring deflections to confirm the bridge behaves as designed", "Testing how many people fit", "Testing the paint", "Testing the toll booths only"], 0,
        "Measured and predicted deflections are compared.",
        "নতুন সেতুতে 'বোঝা-পরীক্ষার' উদ্দেশ্য কী?", ["জানা ভারী বোঝা রেখে বিক্ষেপ মেপে নিশ্চিত হওয়া যে সেতু নকশা মতো আচরণ করছে", "কতজন আঁটে পরীক্ষা", "রং পরীক্ষা", "শুধু টোল-বুথ পরীক্ষা"],
        "মাপা আর পূর্বাভাসিত বিক্ষেপ তুলনা করা হয়।"),
    mcq("What is 'finite element analysis' (FEA)?", ["A computer method that divides a structure into many small elements to calculate stresses and deflections", "A list of chemical elements", "Analysing a bridge by eye", "Counting bolts"], 0,
        "Engineers still check results with hand calculations for sense.",
        "'সসীম উপাদান বিশ্লেষণ' (এফইএ) কী?", ["কম্পিউটার-পদ্ধতি, যা কাঠামোকে অনেক ছোট উপাদানে ভাগ করে পীড়ন আর বিক্ষেপ হিসাব করে", "রাসায়নিক মৌলের তালিকা", "চোখে দেখে সেতু-বিশ্লেষণ", "বল্টু গোনা"],
        "প্রকৌশলীরা তবু যুক্তিসঙ্গততার জন্য হাতে-হিসাবে ফল যাচাই করেন।"),
    mcq("Why must engineers check computer results with simple hand calculations?", ["Input errors or wrong assumptions can give convincing but wrong results", "Computers are always wrong", "Hand calculations are always exact", "It is a tradition only"], 0,
        "'Garbage in, garbage out.'",
        "প্রকৌশলীদের কম্পিউটারের ফল সরল হাতে-হিসাবে যাচাই করতে হয় কেন?", ["ইনপুটের ভুল বা ভুল অনুমান বিশ্বাসযোগ্য কিন্তু ভুল ফল দিতে পারে", "কম্পিউটার সবসময় ভুল", "হাতে-হিসাব সবসময় নিখুঁত", "শুধু প্রথা"],
        "'যেমন ঢোকাবে, তেমনই বেরোবে।'"),
    mcq("How does a cable-stayed bridge carry its deck differently from a suspension bridge?", ["Straight cables run directly from towers to the deck, rather than hanging from main cables", "It has no towers", "It floats on water", "It uses no cables"], 0,
        "Cable-stayed bridges suit spans of roughly 200-1,100 m and need no massive anchorages.",
        "কেবল-স্টেড সেতু ঝুলন্ত সেতুর থেকে আলাদাভাবে পাটাতন কীভাবে বয়?", ["সোজা তার মিনার থেকে সরাসরি পাটাতনে যায়, মূল তার থেকে ঝোলে না", "এর মিনার নেই", "জলে ভাসে", "তার ব্যবহার করে না"],
        "কেবল-স্টেড সেতু মোটামুটি 200-1,100 m স্প্যানে মানানসই আর বিশাল নোঙর লাগে না।"),
    mcq("What is an 'extradosed' bridge?", ["A hybrid between a girder bridge and a cable-stayed bridge, with short towers and shallow cables", "A bridge with no deck", "A floating bridge", "A stone arch"], 0,
        "The stiff girder does much of the work; cables help like external prestress.",
        "'এক্সট্রাডোজড' সেতু কী?", ["গার্ডার-সেতু আর কেবল-স্টেড সেতুর মিশ্রণ, বেঁটে মিনার আর অগভীর তারসহ", "পাটাতনহীন সেতু", "ভাসমান সেতু", "পাথরের খিলান"],
        "শক্ত গার্ডার বেশিরভাগ কাজ করে; তার বাইরের আগাম-পীড়নের মতো সাহায্য করে।"),
    mcq("Why are box girders popular for long, curved bridge decks?", ["Their closed shape gives very high torsional stiffness, resisting twisting from off-centre loads and curves", "They are open at the top", "They cannot twist at all ever", "They are lighter than air"], 0,
        "Open I-girders twist much more easily.",
        "লম্বা, বাঁকা সেতু-পাটাতনে বাক্স-গার্ডার জনপ্রিয় কেন?", ["বন্ধ আকার খুব বেশি মোচড়-দৃঢ়তা দেয়, কেন্দ্রের বাইরের বোঝা আর বাঁকের মোচড় রোধ করে", "উপরে খোলা", "কখনো মোচড় খায় না", "বাতাসের চেয়ে হালকা"],
        "খোলা I-গার্ডার অনেক সহজে মোচড় খায়।"),
    mcq("What is an 'orthotropic' steel deck?", ["A steel plate stiffened by ribs and cross-beams, giving a light, strong deck for long spans", "A deck made of timber only", "A glass deck", "A deck with no steel"], 0,
        "Its many welds need careful fatigue design.",
        "'অর্থোট্রপিক' ইস্পাতের পাটাতন কী?", ["পাঁজর আর আড়-কড়িতে শক্ত-করা ইস্পাতের পাত, লম্বা স্প্যানে হালকা, শক্ত পাটাতন দেয়", "শুধু কাঠের পাটাতন", "কাচের পাটাতন", "ইস্পাতহীন পাটাতন"],
        "এর অনেক ঝালাইয়ে যত্নশীল ক্লান্তি-নকশা লাগে।"),
    mcq("What is an 'integral bridge'?", ["A bridge with no expansion joints or bearings at the abutments - the deck is built into them", "A bridge made of one piece of stone", "A bridge with integrated toll booths", "A bridge that floats"], 0,
        "Removing joints removes a common source of leaks and corrosion.",
        "'অখণ্ড সেতু' (ইন্টিগ্রাল ব্রিজ) কী?", ["প্রান্ত-ঠেকনায় প্রসারণ-জোড় বা বিয়ারিংহীন সেতু - পাটাতন তাদের মধ্যে গেঁথে বানানো", "এক টুকরো পাথরের সেতু", "টোল-বুথ-যুক্ত সেতু", "ভাসমান সেতু"],
        "জোড় সরালে চুঁইয়ে পড়া আর ক্ষয়ের এক সাধারণ উৎস দূর হয়।"),
)
