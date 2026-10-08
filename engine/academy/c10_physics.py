"""Class 10 - Physics (Bridge Engineer): conservation of momentum in collisions, centripetal force
on curved ramps, projectiles, elastic potential energy, pulley systems and efficiency, the
pressure law, specific latent heat, resistivity, power lost in cables, the motor effect
(F = BIL), uniformly loaded beams, refraction and fibre-optic sensing - with real bridges."""
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


def stick(m1, u1, m2):
    v = _c(m1 * u1 / (m1 + m2))
    return _n(f"A {m1:,} kg truck at {u1} m/s runs into a stationary {m2:,} kg car on a bridge and they move off together. What is their speed just after the crash?",
              f"সেতুর উপর {u1} m/s বেগের একটা {m1:,} kg ট্রাক দাঁড়ানো {m2:,} kg গাড়িকে ধাক্কা মারল আর দুটো একসঙ্গে চলল। ধাক্কার ঠিক পরে বেগ কত?", v,
              f"Momentum before = {m1:,} x {u1} = {m1 * u1:,}; after = ({m1:,} + {m2:,})v, so v = {v:g} m/s.",
              f"আগে ভরবেগ = {m1:,} x {u1} = {m1 * u1:,}; পরে = ({m1:,} + {m2:,})v, তাই v = {v:g} m/s।",
              (u1, _c(m2 * u1 / (m1 + m2)), _c(u1 / 2) if _c(u1 / 2) != v else _c(v + 3)), " m/s")


def centri(m, v, r):
    f = _c(m * v * v / r)
    return _n(f"A {m:,} kg car takes a curved bridge ramp of radius {r} m at {v} m/s. What centripetal force is needed to keep it on the curve?",
              f"একটা {m:,} kg গাড়ি {r} m ব্যাসার্ধের বাঁকা সেতু-ঢালে {v} m/s বেগে ঘোরে। বাঁকে রাখতে কত কেন্দ্রমুখী বল লাগে?", f,
              f"F = mv² ÷ r = {m:,} x {v}² ÷ {r} = {f:,} N. Double the speed and the force is four times as big.",
              f"F = mv² ÷ r = {m:,} x {v}² ÷ {r} = {f:,} N। বেগ দ্বিগুণ হলে বল চারগুণ।",
              (_c(m * v / r), _c(m * v * v), _c(f / 2)), " N")


def proj(h, u):
    t = _c((2 * h / 10) ** 0.5)
    x = _c(u * t)
    return _n(f"A stone is thrown horizontally at {u} m/s from a bridge {h} m above the water. How far from the bridge does it land? (g = 10 m/s², no air resistance)",
              f"জল থেকে {h} m উঁচু একটা সেতু থেকে {u} m/s বেগে একটা পাথর অনুভূমিকভাবে ছোড়া হলো। সেতু থেকে কত দূরে পড়ে? (g = 10 m/s², বায়ুর বাধা নেই)", x,
              f"Fall time t = √(2h ÷ g) = √({2 * h} ÷ 10) = {t:g} s; distance = {u} x {t:g} = {x:g} m.",
              f"পড়ার সময় t = √(2h ÷ g) = √({2 * h} ÷ 10) = {t:g} s; দূরত্ব = {u} x {t:g} = {x:g} m।",
              (_c(u * h / 10), _c(u * t * t), _c(h + u)), " m")


def elastic(k, x):
    e = _c(0.5 * k * x * x)
    return _n(f"A bridge bearing spring has a spring constant of {k:,} N/m. How much elastic energy does it store when compressed by {x:g} m?",
              f"সেতুর একটা বিয়ারিং-স্প্রিংয়ের স্প্রিং-ধ্রুবক {k:,} N/m। {x:g} m সংকুচিত হলে কত স্থিতিস্থাপক শক্তি জমা থাকে?", e,
              f"E = ½kx² = ½ x {k:,} x {x:g}² = {e:,} J.",
              f"E = ½kx² = ½ x {k:,} x {x:g}² = {e:,} J।",
              (_c(k * x), _c(k * x * x), _c(0.5 * k * x)), " J")


def pulley(load, effort, ropes):
    ma = _c(load / effort)
    eff = _c(ma / ropes * 100)
    return _n(f"A pulley system with {ropes} supporting ropes lifts a {load:,} N girder section with an effort of {effort:,} N. What is its efficiency?",
              f"{ropes}টি ধারক-দড়ির একটা কপিকল-ব্যবস্থা {effort:,} N প্রয়াসে {load:,} N-এর গার্ডার-খণ্ড তোলে। দক্ষতা কত?", eff,
              f"Mechanical advantage = {load:,} ÷ {effort:,} = {ma:g}; velocity ratio = {ropes}; efficiency = {ma:g} ÷ {ropes} x 100 = {eff:g}%.",
              f"যান্ত্রিক সুবিধা = {load:,} ÷ {effort:,} = {ma:g}; বেগ-অনুপাত = {ropes}; দক্ষতা = {ma:g} ÷ {ropes} x 100 = {eff:g}%।",
              (_c(ma * 100 / (ropes + 1)), _c(ropes / ma * 100), _c(100 - eff) if 100 - eff > 0 else _c(eff / 2)), "%")


def plaw(p1, t1, t2):
    p2 = _c(p1 * (t2 + 273) / (t1 + 273))
    return _n(f"A sealed gas cylinder on site is at {p1:,} kPa at {t1}°C. In the sun it warms to {t2}°C. What is the new pressure?",
              f"নির্মাণস্থলের একটা বন্ধ গ্যাস-সিলিন্ডারের চাপ {t1}°C-এ {p1:,} কিলোপ্যাসকেল। রোদে তা {t2}°C-এ গরম হলো। নতুন চাপ কত?", p2,
              f"Pressure law: p ÷ T is constant, with T in kelvin: p2 = {p1:,} x {t2 + 273} ÷ {t1 + 273} = {p2:g} kPa. Keep cylinders out of the sun!",
              f"চাপের সূত্র: p ÷ T ধ্রুবক, T কেলভিনে: p2 = {p1:,} x {t2 + 273} ÷ {t1 + 273} = {p2:g} কিলোপ্যাসকেল। সিলিন্ডার রোদ থেকে দূরে রাখো!",
              (_c(p1 * t2 / t1), _c(p1 + t2 - t1) if _c(p1 + t2 - t1) != p2 else _c(p2 + 40), _c(p2 * 2)), " kPa", " কিলোপ্যাসকেল")


def latent(m, L, what_en, what_bn, kind_en, kind_bn):
    q = m * L
    return _n(f"How much energy is needed to {what_en} {m} kg of {kind_en}? (specific latent heat = {L:,} kJ/kg)",
              f"{m} kg {kind_bn} {what_bn} কত শক্তি লাগে? (আপেক্ষিক লীনতাপ = {L:,} kJ/kg)", q,
              f"Q = mL = {m} x {L:,} = {q:,} kJ. The temperature stays the same while the state changes.",
              f"Q = mL = {m} x {L:,} = {q:,} kJ। অবস্থা বদলের সময় তাপমাত্রা একই থাকে।",
              (_c(L / m), m + L, q * 10), " kJ")


def resist(rho_e8, L, a_mm2, metal_en, metal_bn):
    r = _c(rho_e8 * 1e-8 * L / (a_mm2 * 1e-6))
    return _n(f"A {metal_en} cable is {L:,} m long with a cross-section of {a_mm2:g} mm². Its resistivity is {rho_e8:g} x 10⁻⁸ Ωm. What is its resistance?",
              f"একটা {metal_bn}-তার {L:,} m লম্বা, প্রস্থচ্ছেদ {a_mm2:g} mm²। এর রোধাঙ্ক {rho_e8:g} x 10⁻⁸ Ωm। রোধ কত?", r,
              f"R = ρL ÷ A = {rho_e8:g} x 10⁻⁸ x {L:,} ÷ ({a_mm2:g} x 10⁻⁶) = {r:g} Ω.",
              f"R = ρL ÷ A = {rho_e8:g} x 10⁻⁸ x {L:,} ÷ ({a_mm2:g} x 10⁻⁶) = {r:g} Ω।",
              (_c(r * 10), _c(r / 10), _c(r * 2) if _c(r * 2) != r else r + 1), " Ω")


def i2r(i, r):
    p = _c(i * i * r)
    return _n(f"A current of {i} A flows through site cabling with a resistance of {r:g} Ω. How much power is wasted as heat?",
              f"{r:g} Ω রোধের নির্মাণস্থলের তারে {i} A প্রবাহ চলে। কত ক্ষমতা তাপ হিসেবে নষ্ট হয়?", p,
              f"P = I²R = {i}² x {r:g} = {p:g} W. Halving the current cuts this loss to a quarter.",
              f"P = I²R = {i}² x {r:g} = {p:g} W। প্রবাহ অর্ধেক করলে এই ক্ষতি এক-চতুর্থাংশ হয়।",
              (_c(i * r), _c(i * r * r), _c(p / 2)), " W")


def bil(b, i, l):
    f = _c(b * i * l)
    return _n(f"A {l:g} m wire carrying {i} A sits at right angles to a {b:g} T magnetic field inside a crane motor. What force acts on it?",
              f"একটা ক্রেন-মোটরের ভেতরে {i} A প্রবাহবাহী {l:g} m তার {b:g} T চৌম্বক ক্ষেত্রের সঙ্গে সমকোণে আছে। এর উপর কত বল কাজ করে?", f,
              f"F = BIL = {b:g} x {i} x {l:g} = {f:g} N.",
              f"বল F = BIL = {b:g} x {i} x {l:g} = {f:g} N।",
              (_c(b * i), _c(i * l), _c(f * 10)), " N")


def udl(w, span):
    r = _c(w * span / 2)
    return _n(f"A simply supported footbridge beam of span {span} m carries a uniform load of {w} kN/m along its whole length. What is the reaction at each support?",
              f"{span} m স্প্যানের একটা সরল-ঠেকনার পায়ে-চলা সেতুর কড়ি পুরো দৈর্ঘ্যে {w} kN/m সুষম বোঝা বয়। প্রতিটা ঠেকনায় প্রতিক্রিয়া কত?", r,
              f"Total load = {w} x {span} = {w * span} kN, shared equally: {r:g} kN at each end.",
              f"মোট বোঝা = {w} x {span} = {w * span} kN, সমান ভাগে: প্রতি প্রান্তে {r:g} kN।",
              (w * span, _c(w * span / 4), _c(w * span * span / 8)), " kN")


def glass_speed(n):
    v = _c(300000 / n)
    return _n(f"Light travels at 300,000 km/s in air. In an optical fibre with refractive index {n:g}, how fast does it travel?",
              f"বাতাসে আলোর বেগ 300,000 km/s। {n:g} প্রতিসরাঙ্কের অপটিক্যাল ফাইবারে আলো কত দ্রুত চলে?", v,
              f"v = c ÷ n = 300,000 ÷ {n:g} = {v:,} km/s.",
              f"v = c ÷ n = 300,000 ÷ {n:g} = {v:,} km/s।",
              (_c(300000 * n), _c(300000 - n * 1000), _c(v / 2)), " km/s")


ITEMS = (
    stick(10000, 12, 2000), stick(8000, 18, 4000), stick(15000, 10, 5000), stick(3000, 20, 1000), stick(20000, 9, 10000),
    centri(1000, 10, 50), centri(1500, 20, 100), centri(12000, 15, 75), centri(800, 25, 125),
    proj(20, 5), proj(45, 4), proj(5, 15), proj(80, 5),
    elastic(200000, 0.01), elastic(50000, 0.04), elastic(1000, 0.1), elastic(400000, 0.01),
    pulley(1200, 400, 4), pulley(3000, 800, 4), pulley(6000, 1250, 6), pulley(900, 500, 2),
    plaw(300, 27, 57), plaw(600, 7, 77), plaw(400, 27, 102),
    latent(2, 334, "melt", "গলাতে", "ice at 0°C", "0°C-এর বরফ"), latent(5, 2260, "boil away", "বাষ্প করে ওড়াতে", "water at 100°C", "100°C-এর জল"),
    latent(10, 270, "melt", "গলাতে", "iron at its melting point", "গলনাঙ্কে লোহা"), latent(3, 400, "melt", "গলাতে", "aluminium at its melting point", "গলনাঙ্কে অ্যালুমিনিয়াম"),
    resist(1.7, 100, 2.5, "copper", "তামার"), resist(2.8, 200, 4, "aluminium", "অ্যালুমিনিয়ামের"), resist(1.7, 500, 10, "copper", "তামার"),
    i2r(10, 0.5), i2r(20, 0.2), i2r(5, 3), i2r(30, 0.1),
    bil(0.5, 10, 0.2), bil(1.2, 5, 0.5), bil(0.8, 20, 0.1),
    udl(5, 12), udl(8, 20), udl(12, 15), udl(3, 30),
    glass_speed(1.5), glass_speed(1.2), glass_speed(2), glass_speed(1.6),
    stick(6000, 14, 1000), centri(2000, 12, 40), proj(125, 6), elastic(80000, 0.05), pulley(2400, 750, 4),
    plaw(250, 17, 75), latent(4, 205, "melt", "গলাতে", "copper at its melting point", "গলনাঙ্কে তামা"),
    resist(2.8, 1000, 25, "aluminium", "অ্যালুমিনিয়ামের"), i2r(40, 0.05), bil(0.6, 25, 0.4), udl(6, 25),
    stick(7000, 16, 1000), centri(5000, 8, 64), proj(20, 9), udl(7, 14),
    mcq("In a collision where no outside forces act, what is always conserved?", ["Total momentum", "Total kinetic energy, always", "The speed of each vehicle", "The colour of the vehicles"], 0,
        "Kinetic energy is only conserved in perfectly elastic collisions; crashes turn much of it into heat and damage.",
        "বাইরের বল কাজ না করলে সংঘর্ষে কী সবসময় সংরক্ষিত থাকে?", ["মোট ভরবেগ", "মোট গতিশক্তি, সবসময়", "প্রতিটা গাড়ির বেগ", "গাড়ির রং"],
        "গতিশক্তি সংরক্ষিত থাকে শুধু পূর্ণ স্থিতিস্থাপক সংঘর্ষে; দুর্ঘটনায় এর অনেকটা তাপ আর ক্ষতিতে বদলায়।"),
    mcq("Why do crash investigators measure skid marks on a bridge?", ["The length and friction let them estimate the vehicle's speed before braking", "To repaint the lines", "To check the bridge's age", "Skid marks show the driver's name"], 0,
        "v² = 2as links speed, deceleration and distance.",
        "দুর্ঘটনা-তদন্তকারীরা সেতুতে চাকার ঘষার দাগ মাপেন কেন?", ["দৈর্ঘ্য আর ঘর্ষণ থেকে ব্রেকের আগে গাড়ির বেগ আন্দাজ করা যায়", "লাইন আবার রং করতে", "সেতুর বয়স দেখতে", "দাগে চালকের নাম থাকে"],
        "v² = 2as বেগ, মন্দন আর দূরত্বকে জোড়ে।"),
    mcq("Why are curved bridge ramps 'banked' (tilted inwards)?", ["Part of the road's push then points towards the centre, helping provide the centripetal force", "To drain rain faster only", "To make the ramp look interesting", "To slow cars down"], 0,
        "Less reliance on tyre friction means safer turns, especially in rain.",
        "বাঁকা সেতু-ঢাল ভেতরের দিকে হেলিয়ে বানানো হয় কেন?", ["রাস্তার ঠেলার একটা অংশ তখন কেন্দ্রের দিকে থাকে, কেন্দ্রমুখী বল জোগাতে সাহায্য করে", "শুধু বৃষ্টির জল দ্রুত সরাতে", "ঢালটা আকর্ষণীয় দেখাতে", "গাড়ি ধীর করতে"],
        "টায়ারের ঘর্ষণের উপর কম নির্ভরতা মানে নিরাপদ বাঁক, বিশেষত বৃষ্টিতে।"),
    mcq("A car goes round a curve at constant speed. Is it accelerating?", ["Yes - its direction, and so its velocity, is changing", "No - its speed is constant", "Only if it brakes", "Only uphill"], 0,
        "Any change in velocity, including direction, is an acceleration.",
        "একটা গাড়ি স্থির দ্রুতিতে বাঁক ঘোরে। এর কি ত্বরণ হচ্ছে?", ["হ্যাঁ - এর দিক, তাই বেগ, বদলাচ্ছে", "না - দ্রুতি স্থির", "শুধু ব্রেক কষলে", "শুধু চড়াইয়ে"],
        "দিকসহ বেগের যেকোনো বদলই ত্বরণ।"),
    mcq("For a projectile launched at 45° on level ground (no air resistance), what is special?", ["It gives the greatest range for a given launch speed", "It goes highest", "It never lands", "It travels in a straight line"], 0,
        "Water cannons and shot-put throwers use this.",
        "সমতল মাটিতে 45°-এ ছোড়া প্রক্ষিপ্ত বস্তুর (বায়ুর বাধা নেই) বিশেষত্ব কী?", ["একই ছোড়ার বেগে সবচেয়ে বেশি পাল্লা দেয়", "সবচেয়ে উঁচুতে যায়", "কখনো নামে না", "সরলরেখায় চলে"],
        "জলকামান আর গোলক-নিক্ষেপকারীরা এটা কাজে লাগান।"),
    mcq("What is the velocity ratio of a pulley system?", ["Distance moved by the effort ÷ distance moved by the load", "Load ÷ effort", "Effort x load", "The speed of the rope"], 0,
        "For a simple block and tackle it equals the number of supporting ropes.",
        "কপিকল-ব্যবস্থার বেগ-অনুপাত কী?", ["প্রয়াসের সরণ ÷ বোঝার সরণ", "বোঝা ÷ প্রয়াস", "প্রয়াস x বোঝা", "দড়ির গতি"],
        "সাধারণ ব্লক-ও-ট্যাকলে এটা ধারক-দড়ির সংখ্যার সমান।"),
    mcq("Why is a real pulley system never 100% efficient?", ["Friction in the wheels and the weight of the lower block waste some of the effort", "Ropes create energy", "Gravity switches off", "It is always 100%"], 0,
        "Well-greased, light pulleys waste less.",
        "আসল কপিকল-ব্যবস্থা কখনো 100% দক্ষ হয় না কেন?", ["চাকার ঘর্ষণ আর নিচের ব্লকের ওজন প্রয়াসের কিছুটা নষ্ট করে", "দড়ি শক্তি তৈরি করে", "মাধ্যাকর্ষণ বন্ধ হয়", "সবসময় 100%"],
        "ভালো গ্রিজ-দেওয়া, হালকা কপিকল কম নষ্ট করে।"),
    mcq("What is 'specific latent heat'?", ["The energy needed to change the state of 1 kg of a substance without changing its temperature", "The energy to warm 1 kg by 1°C", "Heat hidden in the ground", "The temperature of steam"], 0,
        "Melting ice and boiling water both need large amounts of energy.",
        "'আপেক্ষিক লীনতাপ' কী?", ["তাপমাত্রা না বদলে 1 kg পদার্থের অবস্থা বদলাতে লাগা শক্তি", "1 kg-কে 1°C গরম করার শক্তি", "মাটিতে লুকোনো তাপ", "বাষ্পের তাপমাত্রা"],
        "বরফ গলানো আর জল ফোটানো দুটোতেই প্রচুর শক্তি লাগে।"),
    mcq("Why does sweating cool a worker down?", ["Evaporating sweat takes latent heat from the skin", "Sweat is cold when made", "Sweat reflects sunlight", "It does not cool"], 0,
        "In humid weather sweat evaporates slowly, so cooling is poor.",
        "ঘাম কীভাবে কর্মীকে ঠান্ডা করে?", ["ঘাম বাষ্প হতে চামড়া থেকে লীনতাপ নেয়", "তৈরির সময় ঘাম ঠান্ডা", "ঘাম সূর্যালোক প্রতিফলিত করে", "ঠান্ডা করে না"],
        "আর্দ্র আবহাওয়ায় ঘাম ধীরে ওড়ে, তাই ঠান্ডা কম হয়।"),
    mcq("Why does water expanding as it freezes damage concrete bridge decks?", ["Ice takes up about 9% more volume, forcing cracks open in saturated concrete", "Ice is heavier than water", "Ice melts concrete", "It does not damage concrete"], 0,
        "Air-entrained concrete has tiny bubbles that give the ice room to expand.",
        "জমে যাওয়ার সময় জল প্রসারিত হয়ে কংক্রিটের সেতু-পাটাতনের ক্ষতি করে কেন?", ["বরফ প্রায় 9% বেশি জায়গা নেয়, ভেজা কংক্রিটের ফাটল জোর করে খোলে", "বরফ জলের চেয়ে ভারী", "বরফ কংক্রিট গলায়", "ক্ষতি করে না"],
        "বায়ু-মেশানো কংক্রিটে খুদে বুদবুদ বরফকে প্রসারিত হওয়ার জায়গা দেয়।"),
    mcq("What does 'resistivity' depend on?", ["The material and its temperature, not its length or thickness", "Only the length of the wire", "Only the current", "The colour of the insulation"], 0,
        "Resistance depends on resistivity, length and cross-section together.",
        "'রোধাঙ্ক' কীসের উপর নির্ভর করে?", ["উপাদান আর তাপমাত্রার উপর, দৈর্ঘ্য বা পুরুত্বের উপর নয়", "শুধু তারের দৈর্ঘ্য", "শুধু প্রবাহ", "অন্তরকের রং"],
        "রোধ নির্ভর করে রোধাঙ্ক, দৈর্ঘ্য আর প্রস্থচ্ছেদ একসঙ্গে।"),
    mcq("Why are long site extension cables made thicker for power tools?", ["A thicker cable has less resistance, so less voltage is lost and it heats less", "Thick cables look professional", "Thin cables carry no current", "To make them heavier"], 0,
        "Coiled-up cables also trap heat - unwind them fully.",
        "পাওয়ার-যন্ত্রের জন্য নির্মাণস্থলের লম্বা এক্সটেনশন-তার মোটা করা হয় কেন?", ["মোটা তারের রোধ কম, তাই কম ভোল্টেজ হারায় আর কম গরম হয়", "মোটা তার পেশাদার দেখায়", "সরু তারে প্রবাহ চলে না", "ভারী করতে"],
        "গোটানো তারও তাপ আটকায় - পুরো খুলে নাও।"),
    mcq("Why does the National Grid transmit power at very high voltage?", ["For the same power, a higher voltage means a smaller current, and I²R losses fall sharply", "High voltage travels faster", "It is cheaper to make", "Low voltage is unsafe at home"], 0,
        "Halving the current cuts cable losses to one quarter.",
        "জাতীয় গ্রিড খুব উচ্চ ভোল্টেজে বিদ্যুৎ পাঠায় কেন?", ["একই ক্ষমতায় বেশি ভোল্টেজ মানে কম প্রবাহ, আর I²R ক্ষতি তীব্রভাবে কমে", "উচ্চ ভোল্টেজ দ্রুত চলে", "বানানো সস্তা", "বাড়িতে কম ভোল্টেজ অনিরাপদ"],
        "প্রবাহ অর্ধেক করলে তারের ক্ষতি এক-চতুর্থাংশ হয়।"),
    mcq("What does Fleming's left-hand rule help you find?", ["The direction of the force on a current-carrying wire in a magnetic field", "The direction of north", "The resistance of a wire", "The voltage of a battery"], 0,
        "First finger = field, second finger = current, thumb = motion.",
        "ফ্লেমিংয়ের বাম-হাতি নিয়ম কী বের করতে সাহায্য করে?", ["চৌম্বক ক্ষেত্রে প্রবাহবাহী তারের উপর বলের দিক", "উত্তরের দিক", "তারের রোধ", "ব্যাটারির ভোল্টেজ"],
        "তর্জনী = ক্ষেত্র, মধ্যমা = প্রবাহ, বুড়ো আঙুল = গতি।"),
    mcq("How can the force on a motor's coil be increased?", ["Increase the current, use a stronger magnet or add more turns of wire", "Use a weaker magnet", "Reduce the current", "Paint the coil"], 0,
        "Crane motors are designed with strong magnets and many turns.",
        "মোটরের কুণ্ডলীর উপর বল কীভাবে বাড়ানো যায়?", ["প্রবাহ বাড়িয়ে, জোরালো চুম্বক দিয়ে বা তারের পাক বাড়িয়ে", "দুর্বল চুম্বক দিয়ে", "প্রবাহ কমিয়ে", "কুণ্ডলীতে রং করে"],
        "ক্রেন-মোটর জোরালো চুম্বক আর অনেক পাক দিয়ে নকশা করা হয়।"),
    mcq("A magnet is held perfectly still inside a coil connected to a meter. Is a voltage induced?", ["No - a voltage is induced only while the magnetic field through the coil is changing", "Yes - a large one", "Yes - but only at night", "Only if the coil is copper"], 0,
        "Move the magnet, or switch the field on and off, and the meter flicks.",
        "একটা মিটারে যুক্ত কুণ্ডলীর ভেতরে একটা চুম্বক একদম স্থির ধরে রাখা হলো। ভোল্টেজ কি আবিষ্ট হয়?", ["না - কুণ্ডলীর মধ্যে চৌম্বক ক্ষেত্র বদলাতে থাকলেই শুধু ভোল্টেজ আবিষ্ট হয়", "হ্যাঁ - বড়", "হ্যাঁ - কিন্তু শুধু রাতে", "শুধু কুণ্ডলী তামার হলে"],
        "চুম্বক নাড়াও, বা ক্ষেত্র চালু-বন্ধ করো, মিটারের কাঁটা নড়বে।"),
    mcq("Why do the main cables of a suspension bridge hang in a smooth curve?", ["That shape lets the cable carry the deck's weight in pure tension", "Cables are too long", "To look decorative", "Wind pushes them into a curve"], 0,
        "Under an evenly spread deck load the curve is close to a parabola.",
        "ঝুলন্ত সেতুর মূল তার মসৃণ বাঁকে ঝোলে কেন?", ["এই আকারে তার পাটাতনের ওজন শুধু টানে বইতে পারে", "তার খুব লম্বা", "সাজানোর জন্য", "হাওয়া বাঁকিয়ে দেয়"],
        "সমভাবে ছড়ানো পাটাতনের বোঝায় বাঁকটা অধিবৃত্তের কাছাকাছি।"),
    mcq("Why does glass shatter suddenly while structural steel bends a lot before breaking?", ["Glass is brittle; steel is ductile and deforms plastically, giving warning", "Glass is heavier", "Steel is softer than glass in every way", "Glass contains water"], 0,
        "Bridge designers prefer materials and joints that fail gradually, with warning.",
        "কাচ হঠাৎ চুরমার হয়, অথচ কাঠামো-ইস্পাত ভাঙার আগে অনেক বাঁকে কেন?", ["কাচ ভঙ্গুর; ইস্পাত নমনীয় আর প্লাস্টিক বিকৃতিতে সতর্ক করে", "কাচ ভারী", "ইস্পাত সব দিক থেকে কাচের চেয়ে নরম", "কাচে জল থাকে"],
        "সেতু-নকশাকাররা এমন উপাদান আর জোড় চান যা ধীরে, সতর্ক করে ভাঙে।"),
    mcq("On a stress-strain graph for steel, what does the gradient of the first straight part give?", ["The Young's modulus (stiffness) of the steel", "Its breaking strength", "Its density", "Its melting point"], 0,
        "In this region the steel obeys Hooke's law and springs back when unloaded.",
        "ইস্পাতের পীড়ন-বিকৃতি লেখচিত্রে প্রথম সরল অংশের ঢাল কী দেয়?", ["ইস্পাতের ইয়ং-গুণাঙ্ক (দৃঢ়তা)", "এর ভাঙার শক্তি", "এর ঘনত্ব", "এর গলনাঙ্ক"],
        "এই অংশে ইস্পাত হুকের সূত্র মানে আর বোঝা সরালে ফিরে আসে।"),
    mcq("What is the 'yield point' of steel?", ["The stress at which it starts to deform permanently (plastically)", "The point where it melts", "The price per tonne", "The stress at which it is first loaded"], 0,
        "Designers keep working stresses safely below the yield point.",
        "ইস্পাতের 'নতি-বিন্দু' কী?", ["যে পীড়নে এটা স্থায়ীভাবে (প্লাস্টিকভাবে) বিকৃত হতে শুরু করে", "যে বিন্দুতে গলে", "টনপ্রতি দাম", "যে পীড়নে প্রথম বোঝা পড়ে"],
        "নকশাকাররা কার্যকর পীড়ন নতি-বিন্দুর নিরাপদ নিচে রাখেন।"),
    mcq("How is the maximum bending moment of a simply supported beam with a uniform load w over span L calculated?", ["wL² ÷ 8, at mid-span", "wL ÷ 2, at the ends", "wL, everywhere", "Zero everywhere"], 0,
        "That is why beams are often deepest in the middle.",
        "সুষম বোঝা w আর স্প্যান L-এর সরল-ঠেকনার কড়ির সর্বোচ্চ বাঁকানো ভ্রামক কীভাবে হিসাব হয়?", ["wL² ÷ 8, মাঝ-স্প্যানে", "wL ÷ 2, প্রান্তে", "wL, সব জায়গায়", "সব জায়গায় শূন্য"],
        "তাই কড়ি প্রায়ই মাঝখানে সবচেয়ে গভীর হয়।"),
    mcq("A 10 m beam carries 4 kN/m along its length. What is the maximum bending moment? (M = wL² ÷ 8)", ["50 kN·m", "20 kN·m", "40 kN·m", "400 kN·m"], 0,
        "4 x 10² ÷ 8 = 400 ÷ 8 = 50 kN·m.",
        "একটা 10 m কড়ি দৈর্ঘ্য বরাবর 4 kN/m বয়। সর্বোচ্চ বাঁকানো ভ্রামক কত? (M = wL² ÷ 8)", ["50 kN·m", "20 kN·m", "40 kN·m", "400 kN·m"],
        "4 x 10² ÷ 8 = 400 ÷ 8 = 50 কিলোনিউটন-মিটার।"),
    mcq("What is a 'cantilever'?", ["A beam fixed at one end and free at the other", "A beam supported at both ends", "A type of cable", "A floating bridge"], 0,
        "Balconies, diving boards and many bridge arms are cantilevers.",
        "'ক্যান্টিলিভার' কী?", ["এক প্রান্তে আটকানো আর অন্য প্রান্ত মুক্ত কড়ি", "দুই প্রান্তে ঠেকনা দেওয়া কড়ি", "এক রকম তার", "ভাসমান সেতু"],
        "বারান্দা, ডাইভিং-বোর্ড আর অনেক সেতুর বাহু ক্যান্টিলিভার।"),
    mcq("Where is the bending moment largest in a cantilever carrying a load at its tip?", ["At the fixed end", "At the free tip", "In the exact middle", "It is the same everywhere"], 0,
        "So cantilevers are made deepest at the support.",
        "মাথায় বোঝা নিয়ে থাকা ক্যান্টিলিভারে বাঁকানো ভ্রামক কোথায় সবচেয়ে বেশি?", ["আটকানো প্রান্তে", "মুক্ত মাথায়", "ঠিক মাঝখানে", "সব জায়গায় সমান"],
        "তাই ক্যান্টিলিভার ঠেকনার কাছে সবচেয়ে গভীর করে বানানো হয়।"),
    mcq("The Forth Bridge in Scotland is a famous example of which design?", ["A cantilever bridge", "A suspension bridge", "A floating bridge", "A clapper bridge"], 0,
        "Its huge balanced cantilevers carry trains across the firth.",
        "স্কটল্যান্ডের ফোর্থ সেতু কোন নকশার বিখ্যাত উদাহরণ?", ["ক্যান্টিলিভার সেতু", "ঝুলন্ত সেতু", "ভাসমান সেতু", "পাথরের পাটা-সেতু"],
        "এর বিশাল ভারসাম্যপূর্ণ ক্যান্টিলিভার খাঁড়ি পেরিয়ে ট্রেন বয়।"),
    mcq("What happens to light when it passes from air into glass at an angle?", ["It slows down and bends towards the normal (refraction)", "It speeds up", "It stops", "It turns into heat only"], 0,
        "The amount of bending depends on the refractive index.",
        "বাতাস থেকে কাচে কোণ করে ঢুকলে আলোর কী হয়?", ["ধীর হয়ে অভিলম্বের দিকে বাঁকে (প্রতিসরণ)", "দ্রুত হয়", "থেমে যায়", "শুধু তাপ হয়ে যায়"],
        "কতটা বাঁকবে তা প্রতিসরাঙ্কের উপর নির্ভর করে।"),
    mcq("What is 'total internal reflection'?", ["When light inside a denser material hits the boundary above the critical angle and all reflects back", "Light passing straight through glass", "Light absorbed by black paint", "A mirror breaking"], 0,
        "It keeps light trapped inside optical fibres.",
        "'পূর্ণ অভ্যন্তরীণ প্রতিফলন' কী?", ["ঘন মাধ্যমের ভেতরের আলো সংকট-কোণের বেশিতে সীমানায় পড়লে পুরোটা ফিরে আসে", "কাচ দিয়ে সোজা আলো যাওয়া", "কালো রঙে আলো শোষণ", "আয়না ভাঙা"],
        "এটা অপটিক্যাল ফাইবারের ভেতরে আলো আটকে রাখে।"),
    mcq("How are optical fibres used to monitor modern bridges?", ["Fibres along the structure detect tiny strains and temperature changes from how light travels in them", "They light the bridge at night only", "They hold the bridge up", "They carry water"], 0,
        "One fibre can act as thousands of sensors along its length.",
        "আধুনিক সেতুর নজরদারিতে অপটিক্যাল ফাইবার কীভাবে ব্যবহার হয়?", ["কাঠামো বরাবর ফাইবার তার ভেতরে আলোর চলন থেকে খুদে বিকৃতি আর তাপমাত্রার বদল ধরে", "শুধু রাতে সেতু আলোকিত করে", "সেতুকে ধরে রাখে", "জল বয়"],
        "একটা ফাইবার তার দৈর্ঘ্য বরাবর হাজারটা সেন্সরের কাজ করতে পারে।"),
    mcq("What is the 'Doppler effect'?", ["The change in frequency heard when a source of sound moves towards or away from you", "Echoes in a tunnel", "Sound getting louder in water", "Light bending in glass"], 0,
        "A truck's horn sounds higher as it approaches and lower as it leaves.",
        "'ডপলার প্রভাব' কী?", ["শব্দের উৎস কাছে এলে বা দূরে গেলে শোনা কম্পাঙ্কের বদল", "সুড়ঙ্গে প্রতিধ্বনি", "জলে শব্দ জোরালো হওয়া", "কাচে আলো বাঁকা"],
        "ট্রাকের হর্ন কাছে আসার সময় তীক্ষ্ণ আর চলে যাওয়ার সময় মোটা শোনায়।"),
    mcq("How do radar speed guns on bridge approaches use the Doppler effect?", ["Reflected microwaves change frequency in proportion to the vehicle's speed", "They time the car with a stopwatch", "They weigh the car", "They listen to the engine"], 0,
        "The bigger the frequency shift, the faster the vehicle.",
        "সেতুর সংযোগ-রাস্তায় রাডার-গতিমাপক কীভাবে ডপলার প্রভাব কাজে লাগায়?", ["প্রতিফলিত মাইক্রোতরঙ্গের কম্পাঙ্ক গাড়ির গতির অনুপাতে বদলায়", "স্টপওয়াচে গাড়ির সময় মাপে", "গাড়ি ওজন করে", "ইঞ্জিনের শব্দ শোনে"],
        "কম্পাঙ্কের সরণ যত বড়, গাড়ি তত দ্রুত।"),
    mcq("In the nuclear equation for alpha decay, what does the nucleus lose?", ["2 protons and 2 neutrons (a helium nucleus)", "One electron", "Only energy", "One neutron"], 0,
        "Its mass number falls by 4 and its atomic number by 2.",
        "আলফা-ক্ষয়ের নিউক্লীয় সমীকরণে কেন্দ্রক কী হারায়?", ["2টি প্রোটন আর 2টি নিউট্রন (একটা হিলিয়াম-কেন্দ্রক)", "একটা ইলেকট্রন", "শুধু শক্তি", "একটা নিউট্রন"],
        "ভরসংখ্যা 4 আর পারমাণবিক সংখ্যা 2 কমে।"),
    mcq("What is 'background radiation'?", ["Low-level radiation always around us from rocks, space and the air", "Radiation from mobile phones only", "Light from the Sun only", "Sound from traffic"], 0,
        "Granite and some building stones give slightly more than average.",
        "'পটভূমি-বিকিরণ' কী?", ["পাথর, মহাকাশ আর বাতাস থেকে সবসময় আমাদের চারপাশে থাকা নিম্নমাত্রার বিকিরণ", "শুধু মোবাইল ফোনের বিকিরণ", "শুধু সূর্যের আলো", "যানবাহনের শব্দ"],
        "গ্রানাইট আর কিছু নির্মাণ-পাথর গড়ের চেয়ে একটু বেশি দেয়।"),
    mcq("What is 'irradiation' compared with 'contamination'?", ["Irradiation is exposure to radiation from outside; contamination is radioactive material getting onto or into something", "They are the same", "Irradiation makes things radioactive forever", "Contamination is always harmless"], 0,
        "Radiography crews use shielding and distance to limit irradiation.",
        "'বিকিরণ-সংস্পর্শ' আর 'দূষণ'-এর পার্থক্য কী?", ["সংস্পর্শ মানে বাইরে থেকে বিকিরণ পড়া; দূষণ মানে তেজস্ক্রিয় পদার্থ কিছুর উপরে বা ভেতরে ঢোকা", "দুটো একই", "সংস্পর্শ চিরকাল তেজস্ক্রিয় করে", "দূষণ সবসময় নিরীহ"],
        "রেডিওগ্রাফি-দল সংস্পর্শ কমাতে আড়াল আর দূরত্ব ব্যবহার করে।"),
    mcq("What does the 'work-energy principle' say?", ["The work done on an object equals its change in kinetic energy", "Work and energy are unrelated", "Energy is created by work", "Work is always zero"], 0,
        "Braking force x stopping distance = the kinetic energy removed.",
        "'কার্য-শক্তি নীতি' কী বলে?", ["বস্তুর উপর করা কার্য তার গতিশক্তির পরিবর্তনের সমান", "কার্য আর শক্তি সম্পর্কহীন", "কার্য শক্তি তৈরি করে", "কার্য সবসময় শূন্য"],
        "ব্রেক-বল x থামার দূরত্ব = সরানো গতিশক্তি।"),
    mcq("A 1,000 kg car at 20 m/s brakes with a constant force of 5,000 N. How far does it travel before stopping?", ["40 m", "20 m", "4 m", "200 m"], 0,
        "KE = ½ x 1,000 x 20² = 200,000 J; distance = 200,000 ÷ 5,000 = 40 m.",
        "20 m/s বেগের 1,000 kg গাড়ি 5,000 N স্থির বলে ব্রেক কষে। থামার আগে কত দূর যায়?", ["40 m", "20 m", "4 m", "200 m"],
        "গতিশক্তি = ½ x 1,000 x 20² = 200,000 J; দূরত্ব = 200,000 ÷ 5,000 = 40 m।"),
    mcq("Why do escape lanes on steep bridge approaches use deep loose gravel?", ["The gravel does a lot of work on a runaway truck, removing its kinetic energy quickly", "Gravel is cheaper than asphalt", "To grow plants", "To drain rain only"], 0,
        "A large stopping force over a short distance removes the energy safely.",
        "খাড়া সেতু-সংযোগে পালানোর লেনে গভীর আলগা কাঁকর থাকে কেন?", ["কাঁকর লাগামছাড়া ট্রাকের উপর অনেক কার্য করে, দ্রুত তার গতিশক্তি সরায়", "কাঁকর পিচের চেয়ে সস্তা", "গাছ জন্মাতে", "শুধু বৃষ্টির জল সরাতে"],
        "অল্প দূরত্বে বড় থামানোর বল শক্তি নিরাপদে সরায়।"),
    mcq("A 2 kg spanner falls and hits the deck at 10 m/s, stopping in 0.01 s. What average force does it exert?", ["2,000 N", "20 N", "200 N", "0.2 N"], 0,
        "F = change in momentum ÷ time = (2 x 10) ÷ 0.01 = 2,000 N - like a 200 kg weight landing on someone.",
        "2 kg-এর একটা স্প্যানার পড়ে 10 m/s বেগে পাটাতনে লেগে 0.01 s-এ থামল। গড়ে কত বল দেয়?", ["2,000 N", "20 N", "200 N", "0.2 N"],
        "F = ভরবেগের পরিবর্তন ÷ সময় = (2 x 10) ÷ 0.01 = 2,000 N - কারও উপর 200 kg ওজন পড়ার মতো।"),
    mcq("On the Moon, g is about 1.6 N/kg. What would a 50 kg bag of cement weigh there?", ["80 N", "500 N", "50 N", "31 N"], 0,
        "W = mg = 50 x 1.6 = 80 N - its mass is still 50 kg.",
        "চাঁদে g প্রায় 1.6 N/kg। সেখানে 50 kg-এর এক বস্তা সিমেন্টের ওজন কত হতো?", ["80 N", "500 N", "50 N", "31 N"],
        "W = mg = 50 x 1.6 = 80 N - ভর এখনো 50 kg।"),
    mcq("Why is the pressure under a heavy crane's outrigger pads reduced by placing large timber mats beneath them?", ["The same force spread over a larger area gives lower pressure, so the ground does not sink", "Timber makes the crane lighter", "Mats push the crane up", "It increases the pressure"], 0,
        "p = F ÷ A - doubling the area halves the pressure.",
        "ভারী ক্রেনের আউটরিগার-প্যাডের নিচে বড় কাঠের মাদুর দিলে চাপ কমে কেন?", ["একই বল বড় ক্ষেত্রে ছড়ালে চাপ কম হয়, তাই মাটি বসে যায় না", "কাঠ ক্রেন হালকা করে", "মাদুর ক্রেনকে উপরে ঠেলে", "চাপ বাড়ায়"],
        "p = F ÷ A - ক্ষেত্রফল দ্বিগুণ করলে চাপ অর্ধেক।"),
)
