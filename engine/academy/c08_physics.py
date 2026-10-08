"""Class 8 - Physics (Junior Cadet): momentum and impulse, support reactions of a loaded beam,
Hooke's law, strain and Young's modulus, pressure in liquids (ρgh), specific heat capacity,
linear expansion of steel, electrical power, transformers, half-life, and the physics of
safe bridges - joints, cables, wind and vibration."""
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


def mom(m, v, what_en, what_bn):
    p = m * v
    return _n(f"{what_en} of mass {m:,} kg moves at {v} m/s. What is its momentum?",
              f"{m:,} kg ভরের {what_bn} {v} m/s বেগে চলে। তার ভরবেগ কত?", p,
              f"Momentum p = mv = {m:,} x {v} = {p:,} kg m/s.",
              f"ভরবেগ p = mv = {m:,} x {v} = {p:,} kg m/s।",
              (m * v * v // 2, m + v, p * 10), " kg m/s")


def impulse(m, dv, t):
    f = m * dv // t if (m * dv) % t == 0 else _c(m * dv / t)
    return _n(f"A {m:,} kg truck slows from {dv} m/s to rest in {t} s at a bridge barrier. What average force acts on it?",
              f"একটা {m:,} kg ট্রাক সেতুর বাধায় {t} s-এ {dv} m/s থেকে থেমে গেল। গড়ে কত বল কাজ করল?", f,
              f"F = change in momentum ÷ time = {m:,} x {dv} ÷ {t} = {f:,} N. A longer stopping time means a smaller force.",
              f"F = ভরবেগের পরিবর্তন ÷ সময় = {m:,} x {dv} ÷ {t} = {f:,} N। থামার সময় বেশি হলে বল কম হয়।",
              (m * dv, m * dv * t, _c(m * dv / (t * 10))), " N")


def react(span, load, x):
    rb = _c(load * x / span)
    ra = _c(load - rb)
    return _n(f"A {span} m beam rests on supports A and B at its ends. A {load} kN load sits {x} m from A. What is the reaction at B?",
              f"একটা {span} m কড়ি দুই প্রান্তে A আর B ঠেকনায় রাখা। A থেকে {x} m দূরে {load} kN বোঝা। B-তে প্রতিক্রিয়া কত?", rb,
              f"Moments about A: R_B x {span} = {load} x {x}, so R_B = {rb:g} kN (and R_A = {load} - {rb:g} = {ra:g} kN).",
              f"A-র সাপেক্ষে ভ্রামক: R_B x {span} = {load} x {x}, তাই R_B = {rb:g} kN (আর R_A = {load} - {rb:g} = {ra:g} kN)।",
              (ra if ra != rb else _c(rb + 5), _c(load / 2) if _c(load / 2) != rb else _c(rb + 3), load), " kN")


def hooke(k, f):
    e = _c(f / k)
    return _n(f"A spring in a bridge bearing has stiffness {k} N/mm. How far does it compress under {f:,} N?",
              f"সেতুর বিয়ারিংয়ের একটা স্প্রিংয়ের দৃঢ়তা {k} N/mm। {f:,} N বোঝায় কতটা সংকুচিত হয়?", e,
              f"Hooke's law: extension = F ÷ k = {f:,} ÷ {k} = {e:g} mm.",
              f"হুকের সূত্র: দৈর্ঘ্য-বদল = F ÷ k = {f:,} ÷ {k} = {e:g} mm।",
              (f * k, _c(k / f * 1000), _c(e * 10)), " mm")


def strain(dl, l):
    s = _c(dl / l * 1000)
    return mcq(f"A {l:,} mm steel hanger stretches by {dl} mm under load. What is its strain?",
               [f"{s:g} x 10⁻³", f"{_c(l / dl):g}", f"{_c(s * 10):g} x 10⁻³", f"{dl * l:,}"], 0,
               f"Strain = extension ÷ original length = {dl} ÷ {l:,} = {s:g} x 10⁻³ (no units).",
               f"{l:,} mm লম্বা একটা ইস্পাতের ঝুলন্ত দণ্ড বোঝায় {dl} mm বাড়ল। এর বিকৃতি কত?",
               [f"{s:g} x 10⁻³", f"{_c(l / dl):g}", f"{_c(s * 10):g} x 10⁻³", f"{dl * l:,}"],
               f"বিকৃতি = দৈর্ঘ্য-বৃদ্ধি ÷ আদি দৈর্ঘ্য = {dl} ÷ {l:,} = {s:g} x 10⁻³ (একক নেই)।")


def youngs(stress, strain_e3, mat_en, mat_bn):
    e = _c(stress / strain_e3)
    return _n(f"A {mat_en} test piece carries a stress of {stress} N/mm² at a strain of {strain_e3:g} x 10⁻³. What is its Young's modulus?",
              f"একটা {mat_bn}-নমুনায় {strain_e3:g} x 10⁻³ বিকৃতিতে পীড়ন {stress} N/mm²। এর ইয়ং-গুণাঙ্ক কত?", e,
              f"E = stress ÷ strain = {stress} ÷ {strain_e3:g} x 10⁻³ = {e:g} kN/mm².",
              f"E = পীড়ন ÷ বিকৃতি = {stress} ÷ {strain_e3:g} x 10⁻³ = {e:g} kN/mm²।",
              (_c(stress * strain_e3), _c(e * 10), _c(e / 2)), " kN/mm²")


def rgh(depth, rho, what_en, what_bn):
    p = rho * 10 * depth // 1000
    return _n(f"How much extra pressure does {what_en} (density {rho:,} kg/m³) exert at {depth} m deep on a pier? (g = 10 N/kg)",
              f"{what_bn} (ঘনত্ব {rho:,} kg/m³) {depth} m গভীরে একটা স্তম্ভে কত বাড়তি চাপ দেয়? (g = 10 N/kg)", p,
              f"p = ρgh = {rho:,} x 10 x {depth} = {rho * 10 * depth:,} Pa = {p:,} kPa.",
              f"p = ρgh = {rho:,} x 10 x {depth} = {rho * 10 * depth:,} Pa = {p:,} কিলোপ্যাসকেল।",
              (rho * depth // 1000 if rho * depth >= 1000 else p + 3, p * 10, p + depth), " kPa", " কিলোপ্যাসকেল")


def shc(m, c, dt, what_en, what_bn):
    q = m * c * dt // 1000
    return _n(f"How much energy heats {m} kg of {what_en} (c = {c} J/kg°C) by {dt}°C?",
              f"{m} kg {what_bn} (c = {c} J/kg°C) {dt}°C গরম করতে কত শক্তি লাগে?", q,
              f"Q = mcΔT = {m} x {c} x {dt} = {m * c * dt:,} J = {q:,} kJ.",
              f"Q = mcΔT = {m} x {c} x {dt} = {m * c * dt:,} J = {q:,} কিলোজুল।",
              (m * c // 1000 if m * c >= 1000 else q + 9, q * 10, m * dt), " kJ", " কিলোজুল")


def expand(l, dt):
    d = _c(l * 1000 * 12 * dt / 1_000_000)
    return _n(f"A {l} m steel girder warms by {dt}°C. Steel expands 12 millionths of its length per °C. How much longer does it get?",
              f"একটা {l} m ইস্পাতের গার্ডার {dt}°C গরম হলো। ইস্পাত প্রতি °C-এ দৈর্ঘ্যের 12 লক্ষভাগের এক ভাগ বাড়ে। কতটা লম্বা হয়?", d,
              f"ΔL = αLΔT = 12 x 10⁻⁶ x {l * 1000:,} mm x {dt} = {d:g} mm - expansion joints leave room for it.",
              f"ΔL = αLΔT = 12 x 10⁻⁶ x {l * 1000:,} mm x {dt} = {d:g} mm - প্রসারণ-জোড় এর জায়গা রাখে।",
              (_c(d * 10), _c(d / 10), _c(l * dt / 100)), " mm")


def power(v, i, what_en, what_bn):
    p = v * i
    return _n(f"{what_en} runs on {v} V and draws {i} A. What is its power?",
              f"{what_bn} {v} V-এ চলে আর {i} A টানে। এর ক্ষমতা কত?", p,
              f"P = VI = {v} x {i} = {p:,} W.",
              f"P = VI = {v} x {i} = {p:,} W।",
              (_c(v / i), v + i, p * 10), " W")


def transformer(vp, np, ns):
    vs = vp * ns // np
    return _n(f"A site transformer has {np:,} turns on the primary and {ns:,} on the secondary. The input is {vp:,} V. What is the output voltage?",
              f"নির্মাণস্থলের একটা ট্রান্সফর্মারের মুখ্য কুণ্ডলীতে {np:,} পাক আর গৌণে {ns:,} পাক। ইনপুট {vp:,} V। আউটপুট ভোল্টেজ কত?", vs,
              f"Vs ÷ Vp = Ns ÷ Np, so Vs = {vp:,} x {ns:,} ÷ {np:,} = {vs:,} V.",
              f"Vs ÷ Vp = Ns ÷ Np, তাই Vs = {vp:,} x {ns:,} ÷ {np:,} = {vs:,} V।",
              (vp * np // ns, vp - vs if vp > vs else vs + vp, vs * 2), " V")


def halflife(start, hl, t):
    n = start
    for _ in range(t // hl):
        n //= 2
    return _n(f"A radiography source used to check bridge welds has a half-life of {hl} days. Its activity starts at {start:,} units. What is it after {t} days?",
              f"সেতুর ঝালাই পরীক্ষার একটা রেডিওগ্রাফি-উৎসের অর্ধায়ু {hl} দিন। শুরুতে সক্রিয়তা {start:,} একক। {t} দিন পরে কত?", n,
              f"{t} ÷ {hl} = {t // hl} half-lives; halve {t // hl} times: {start:,} -> {n:,}.",
              f"{t} ÷ {hl} = {t // hl}টি অর্ধায়ু; {t // hl} বার অর্ধেক: {start:,} -> {n:,}।",
              (start // (t // hl * 2) if start // (t // hl * 2) != n else n * 3, start - start * t // (hl * 4), n * 2))


ITEMS = (
    mom(2000, 15, "A car", "একটা গাড়ি"), mom(12000, 10, "A loaded truck", "একটা বোঝাই ট্রাক"),
    mom(80, 6, "A cyclist and bike", "সাইকেলসহ একজন আরোহী"), mom(40000, 5, "A train wagon", "একটা ট্রেনের ওয়াগন"),
    impulse(1500, 20, 2), impulse(10000, 12, 4), impulse(3000, 15, 3), impulse(800, 10, 1),
    react(10, 60, 4), react(8, 40, 2), react(12, 90, 8), react(6, 30, 3), react(20, 100, 15),
    hooke(50, 2000), hooke(200, 9000), hooke(25, 600), hooke(400, 30000),
    strain(3, 2000), strain(6, 5000), strain(2, 4000), strain(9, 3000),
    youngs(200, 1, "steel", "ইস্পাত"), youngs(70, 1, "aluminium", "অ্যালুমিনিয়াম"),
    youngs(30, 1, "concrete", "কংক্রিট"), youngs(100, 0.5, "high-strength steel", "উচ্চ-শক্তির ইস্পাত"),
    rgh(10, 1000, "river water", "নদীর জল"), rgh(25, 1000, "lake water", "হ্রদের জল"),
    rgh(8, 1025, "sea water", "সমুদ্রের জল"), rgh(4, 1500, "wet mud", "ভেজা কাদা"),
    shc(2, 4200, 50, "water", "জল"), shc(10, 450, 40, "steel", "ইস্পাত"),
    shc(5, 900, 20, "aluminium", "অ্যালুমিনিয়াম"), shc(50, 880, 10, "concrete", "কংক্রিট"),
    expand(50, 30), expand(100, 40), expand(20, 25), expand(250, 20),
    power(230, 10, "A site heater", "নির্মাণস্থলের একটা হিটার"), power(230, 4, "A drill", "একটা ড্রিল"),
    power(12, 5, "A warning lamp", "একটা সতর্কতা-বাতি"), power(400, 30, "A crane motor", "একটা ক্রেনের মোটর"),
    transformer(11000, 5000, 200), transformer(230, 1000, 50), transformer(400, 200, 1000),
    halflife(800, 74, 148), halflife(1600, 30, 90), halflife(640, 5, 20),
    mcq("Two trucks have the same speed, but one is twice as heavy. Which is harder to stop?", ["The heavier one - it has twice the momentum", "The lighter one", "Both are equally hard", "Neither has momentum"], 0,
        "Momentum = mass x velocity, so doubling the mass doubles the momentum.",
        "দুটো ট্রাকের বেগ সমান, কিন্তু একটা দ্বিগুণ ভারী। কোনটা থামানো কঠিন?", ["ভারীটা - এর ভরবেগ দ্বিগুণ", "হালকাটা", "দুটোই সমান কঠিন", "কোনোটারই ভরবেগ নেই"],
        "ভরবেগ = ভর x বেগ, তাই ভর দ্বিগুণ হলে ভরবেগও দ্বিগুণ।"),
    mcq("Why do crash barriers on bridges crumple instead of staying perfectly rigid?", ["Crumpling makes the stop take longer, which lowers the force on the vehicle", "Crumpling looks nicer", "Rigid barriers are illegal", "To save paint"], 0,
        "Force = change in momentum ÷ time; more time, less force.",
        "সেতুর ধাক্কা-রোধক বেড়া একদম শক্ত না থেকে দুমড়ে যায় কেন?", ["দুমড়োলে থামতে বেশি সময় লাগে, তাতে গাড়ির উপর বল কমে", "দেখতে ভালো লাগে", "শক্ত বেড়া বেআইনি", "রং বাঁচাতে"],
        "বল = ভরবেগের পরিবর্তন ÷ সময়; সময় বেশি, বল কম।"),
    mcq("What is 'conservation of momentum'?", ["In a collision, total momentum before equals total momentum after, if no outside force acts", "Momentum is always lost", "Momentum only exists in water", "Heavy things have no momentum"], 0,
        "It lets investigators work out vehicle speeds after a crash.",
        "'ভরবেগের সংরক্ষণ' কী?", ["বাইরের বল না থাকলে সংঘর্ষের আগে আর পরে মোট ভরবেগ সমান", "ভরবেগ সবসময় হারায়", "ভরবেগ শুধু জলে থাকে", "ভারী জিনিসের ভরবেগ নেই"],
        "এতে তদন্তকারীরা দুর্ঘটনার পরে গাড়ির গতি হিসাব করতে পারেন।"),
    mcq("A loaded beam is in equilibrium. What must be true?", ["Upward forces equal downward forces, and clockwise moments equal anticlockwise moments", "Only the forces balance", "Only the moments balance", "The beam must be moving"], 0,
        "Both conditions together let engineers find unknown support reactions.",
        "একটা বোঝাই কড়ি সাম্যাবস্থায় আছে। কী সত্যি হতেই হবে?", ["ঊর্ধ্বমুখী বল = নিম্নমুখী বল, আর দক্ষিণাবর্ত ভ্রামক = বামাবর্ত ভ্রামক", "শুধু বল সমান", "শুধু ভ্রামক সমান", "কড়িটা চলতেই হবে"],
        "দুটো শর্ত একসঙ্গে ধরে প্রকৌশলীরা অজানা ঠেকনা-প্রতিক্রিয়া বের করেন।"),
    mcq("A load sits exactly in the middle of a simply supported beam. How do the two support reactions compare?", ["They are equal - each carries half", "The left one carries all of it", "The right one carries all of it", "Neither carries any"], 0,
        "Symmetry: moments about either end give the same answer.",
        "একটা সরল-ঠেকনার কড়ির ঠিক মাঝখানে বোঝা। দুই ঠেকনার প্রতিক্রিয়া কেমন?", ["সমান - প্রত্যেকে অর্ধেক বয়", "বাঁদিকেরটা সবটা বয়", "ডানদিকেরটা সবটা বয়", "কেউই কিছু বয় না"],
        "প্রতিসাম্য: যেকোনো প্রান্তের সাপেক্ষে ভ্রামক একই উত্তর দেয়।"),
    mcq("As a heavy truck drives from support A towards support B, what happens to the reaction at B?", ["It increases", "It decreases", "It stays the same", "It becomes negative"], 0,
        "The closer the load is to a support, the bigger the share that support carries.",
        "একটা ভারী ট্রাক ঠেকনা A থেকে B-এর দিকে গেলে B-এর প্রতিক্রিয়ার কী হয়?", ["বাড়ে", "কমে", "একই থাকে", "ঋণাত্মক হয়"],
        "বোঝা যে ঠেকনার যত কাছে, সেই ঠেকনা তত বেশি ভাগ বয়।"),
    mcq("A bearing spring obeys Hooke's law. If the force on it is tripled (still within its limit), what happens to its compression?", ["It triples", "It stays the same", "It doubles", "It falls to a third"], 0,
        "Extension or compression is proportional to force - until the limit of proportionality.",
        "বিয়ারিংয়ের একটা স্প্রিং হুকের সূত্র মানে। তার উপর বল তিনগুণ করলে (সীমার মধ্যেই) সংকোচনের কী হয়?", ["তিনগুণ হয়", "একই থাকে", "দ্বিগুণ হয়", "এক-তৃতীয়াংশ হয়"],
        "আনুপাতিক সীমা পর্যন্ত দৈর্ঘ্য-বদল বলের সমানুপাতিক।"),
    mcq("What is the 'elastic limit' of a steel bar?", ["The largest stress after which it no longer returns to its original length", "Its weight", "Its melting point", "The length of the bar"], 0,
        "Bridges are designed so steel stays well below this limit.",
        "ইস্পাতের দণ্ডের 'স্থিতিস্থাপক সীমা' কী?", ["সবচেয়ে বড় পীড়ন, যার পরে আর আদি দৈর্ঘ্যে ফেরে না", "এর ওজন", "এর গলনাঙ্ক", "দণ্ডের দৈর্ঘ্য"],
        "সেতুর নকশায় ইস্পাতকে এই সীমার অনেক নিচে রাখা হয়।"),
    mcq("What does 'plastic deformation' mean for a steel member?", ["It has been stretched so far that it stays permanently bent or longer", "It has turned into plastic", "It has become stronger forever", "It has melted"], 0,
        "A permanently bent member is a warning sign that inspectors look for.",
        "ইস্পাতের অংশের 'প্লাস্টিক বিকৃতি' মানে কী?", ["এত টানা হয়েছে যে স্থায়ীভাবে বেঁকে বা লম্বা হয়ে থাকে", "প্লাস্টিক হয়ে গেছে", "চিরকালের জন্য শক্ত হয়েছে", "গলে গেছে"],
        "স্থায়ীভাবে বাঁকা অংশ একটা বিপদসংকেত, পরিদর্শকরা যা খোঁজেন।"),
    mcq("What does a high Young's modulus tell you about a material?", ["It is stiff - it stretches very little under stress", "It is very heavy", "It is very cheap", "It melts easily"], 0,
        "Steel's modulus is about 3 times aluminium's and 7 times concrete's.",
        "উপাদানের ইয়ং-গুণাঙ্ক বেশি হলে কী বোঝায়?", ["এটা শক্ত-অনমনীয় - পীড়নে খুব কম লম্বা হয়", "খুব ভারী", "খুব সস্তা", "সহজে গলে"],
        "ইস্পাতের গুণাঙ্ক অ্যালুমিনিয়ামের প্রায় 3 গুণ আর কংক্রিটের 7 গুণ।"),
    mcq("Why does strain have no units?", ["It is a length divided by a length", "Scientists forgot to give it one", "It is always zero", "It is measured in newtons"], 0,
        "mm ÷ mm cancels out, leaving a pure number.",
        "বিকৃতির একক নেই কেন?", ["এটা দৈর্ঘ্যকে দৈর্ঘ্য দিয়ে ভাগ", "বিজ্ঞানীরা দিতে ভুলে গেছেন", "সবসময় শূন্য", "নিউটনে মাপা হয়"],
        "mm ÷ mm কেটে গিয়ে খাঁটি সংখ্যা থাকে।"),
    mcq("Why is the bottom of a dam or bridge pier built thicker than the top?", ["Water pressure increases with depth", "Water is lighter at the bottom", "Fish push harder at the top", "To look stronger"], 0,
        "p = ρgh: double the depth, double the pressure.",
        "বাঁধ বা সেতু-স্তম্ভের নিচটা উপরের চেয়ে মোটা করে বানানো হয় কেন?", ["গভীরতার সঙ্গে জলের চাপ বাড়ে", "নিচে জল হালকা", "উপরে মাছ জোরে ঠেলে", "শক্ত দেখাতে"],
        "p = ρgh: গভীরতা দ্বিগুণ, চাপ দ্বিগুণ।"),
    mcq("Does the pressure at the bottom of a river depend on how wide the river is?", ["No - only on the depth, the liquid's density and g", "Yes - wider rivers press harder", "Only on the river's length", "Only on the speed of boats"], 0,
        "A narrow deep channel and a wide lake of the same depth give the same pressure at the bottom.",
        "নদীর তলার চাপ কি নদী কত চওড়া তার উপর নির্ভর করে?", ["না - শুধু গভীরতা, তরলের ঘনত্ব আর g-এর উপর", "হ্যাঁ - চওড়া নদী বেশি চাপ দেয়", "শুধু নদীর দৈর্ঘ্যের উপর", "শুধু নৌকার গতির উপর"],
        "একই গভীরতার সরু খাল আর চওড়া হ্রদের তলায় চাপ সমান।"),
    mcq("Which needs more energy to warm by 10°C: 1 kg of river water or 1 kg of steel?", ["The water - its specific heat capacity is about 9 times steel's", "The steel", "Both need exactly the same", "Neither needs any energy"], 0,
        "Water 4,200 J/kg°C, steel about 450 J/kg°C - so steel railings feel hot in the sun while the river stays cool.",
        "10°C গরম করতে কোনটায় বেশি শক্তি লাগে: 1 kg নদীর জল না 1 kg ইস্পাত?", ["জল - এর আপেক্ষিক তাপধারকত্ব ইস্পাতের প্রায় 9 গুণ", "ইস্পাত", "দুটোয় হুবহু সমান", "কোনোটাতেই শক্তি লাগে না"],
        "জল 4,200 J/kg°C, ইস্পাত প্রায় 450 J/kg°C - তাই রোদে ইস্পাতের রেলিং গরম লাগে আর নদী ঠান্ডা থাকে।"),
    mcq("Why is concrete cured with water and sometimes cooled in very hot weather?", ["Setting cement gives off heat; too much heat causes cracks", "Cold concrete is heavier", "Water makes it set instantly", "Hot concrete changes colour"], 0,
        "Big pours like bridge foundations are watched with thermometers inside.",
        "খুব গরম আবহাওয়ায় কংক্রিট জল দিয়ে কিউর করা হয় আর কখনো ঠান্ডা রাখা হয় কেন?", ["জমাট বাঁধা সিমেন্ট তাপ ছাড়ে; বেশি তাপে ফাটল ধরে", "ঠান্ডা কংক্রিট ভারী", "জলে তখনই জমে যায়", "গরম কংক্রিটের রং বদলায়"],
        "সেতুর ভিতের মতো বড় ঢালাইয়ে ভেতরে থার্মোমিটার রেখে নজর রাখা হয়।"),
    mcq("Why do long bridges have expansion joints?", ["Steel and concrete lengthen in heat and shorten in cold; joints let them move without cracking", "To let rainwater in", "To make a noise when cars cross", "To save materials"], 0,
        "A 1 km steel deck can change length by about 50 cm between winter and summer.",
        "লম্বা সেতুতে প্রসারণ-জোড় থাকে কেন?", ["ইস্পাত আর কংক্রিট গরমে লম্বা, ঠান্ডায় ছোট হয়; জোড় ফাটল ছাড়াই নড়তে দেয়", "বৃষ্টির জল ঢোকাতে", "গাড়ি গেলে শব্দ করতে", "উপাদান বাঁচাতে"],
        "1 km ইস্পাতের পাটাতন শীত থেকে গ্রীষ্মে প্রায় 50 cm দৈর্ঘ্য বদলাতে পারে।"),
    mcq("Why can steel bars be used inside concrete without cracking it as temperature changes?", ["Steel and concrete expand by almost the same amount per °C", "Concrete does not expand at all", "Steel shrinks when heated", "The bars are painted"], 0,
        "This lucky match is one reason reinforced concrete works so well.",
        "তাপমাত্রা বদলালেও কংক্রিটের ভেতরে ইস্পাতের রড ফাটল ধরায় না কেন?", ["প্রতি °C-এ ইস্পাত আর কংক্রিট প্রায় সমান প্রসারিত হয়", "কংক্রিট মোটেই প্রসারিত হয় না", "গরমে ইস্পাত ছোট হয়", "রডে রং করা থাকে"],
        "এই সৌভাগ্যজনক মিলই রিইনফোর্সড কংক্রিট এত ভালো কাজ করার একটা কারণ।"),
    mcq("What does a power rating of 2 kW mean for a site heater?", ["It transfers 2,000 joules of energy every second", "It weighs 2 kg", "It runs for 2 hours", "It uses 2 volts"], 0,
        "1 W = 1 J/s, so 2 kW = 2,000 J/s.",
        "নির্মাণস্থলের হিটারের ক্ষমতা 2 kW মানে কী?", ["প্রতি সেকেন্ডে 2,000 জুল শক্তি স্থানান্তর করে", "ওজন 2 kg", "2 ঘণ্টা চলে", "2 ভোল্ট ব্যবহার করে"],
        "1 W = 1 J/s, তাই 2 kW = 2,000 J/s।"),
    mcq("Why is electricity sent across the country at very high voltage?", ["The current is smaller, so much less energy is wasted as heat in the cables", "High voltage travels faster", "Low voltage is illegal", "It makes cables lighter in colour"], 0,
        "Step-up transformers raise the voltage at power stations; step-down ones lower it near homes.",
        "বিদ্যুৎ দেশজুড়ে খুব উচ্চ ভোল্টেজে পাঠানো হয় কেন?", ["প্রবাহ ছোট হয়, তাই তারে তাপ হিসেবে অনেক কম শক্তি নষ্ট হয়", "উচ্চ ভোল্টেজ দ্রুত চলে", "নিম্ন ভোল্টেজ বেআইনি", "তারের রং হালকা হয়"],
        "বিদ্যুৎকেন্দ্রে স্টেপ-আপ ট্রান্সফর্মার ভোল্টেজ বাড়ায়; বাড়ির কাছে স্টেপ-ডাউন কমায়।"),
    mcq("A transformer has more turns on its secondary coil than on its primary. What kind is it?", ["Step-up - it increases the voltage", "Step-down", "It does not change the voltage", "It only works on batteries"], 0,
        "Voltage ratio equals turns ratio.",
        "একটা ট্রান্সফর্মারের গৌণ কুণ্ডলীতে মুখ্যের চেয়ে বেশি পাক। এটা কোন ধরনের?", ["স্টেপ-আপ - ভোল্টেজ বাড়ায়", "স্টেপ-ডাউন", "ভোল্টেজ বদলায় না", "শুধু ব্যাটারিতে চলে"],
        "ভোল্টেজের অনুপাত পাকের অনুপাতের সমান।"),
    mcq("Why does a transformer not work on steady direct current (DC)?", ["It needs a changing magnetic field, which only alternating current makes", "DC is too strong", "DC flows backwards", "Transformers only work at night"], 0,
        "A changing field in the core induces a voltage in the secondary coil.",
        "স্থির একমুখী প্রবাহে (ডিসি) ট্রান্সফর্মার কাজ করে না কেন?", ["এর পরিবর্তনশীল চৌম্বক ক্ষেত্র লাগে, যা শুধু পরিবর্তী প্রবাহ তৈরি করে", "ডিসি খুব শক্তিশালী", "ডিসি উল্টো দিকে চলে", "ট্রান্সফর্মার শুধু রাতে কাজ করে"],
        "কোরের পরিবর্তনশীল ক্ষেত্র গৌণ কুণ্ডলীতে ভোল্টেজ আবিষ্ট করে।"),
    mcq("What does an electric motor on a crane do?", ["Turns electrical energy into kinetic energy using magnetic forces on a current-carrying coil", "Turns heat into light", "Stores electricity", "Makes magnets from steel"], 0,
        "A current in a magnetic field feels a force - the motor effect.",
        "ক্রেনের বৈদ্যুতিক মোটর কী করে?", ["প্রবাহবাহী কুণ্ডলীর উপর চৌম্বক বলে বৈদ্যুতিক শক্তিকে গতিশক্তিতে বদলায়", "তাপকে আলোয় বদলায়", "বিদ্যুৎ জমিয়ে রাখে", "ইস্পাত থেকে চুম্বক বানায়"],
        "চৌম্বক ক্ষেত্রে প্রবাহ বল অনুভব করে - মোটর-প্রভাব।"),
    mcq("A magnet is pushed into a coil, first slowly and then quickly. What happens to the induced voltage when it moves quickly?", ["It is larger", "It is smaller", "It is the same", "It becomes zero"], 0,
        "A faster change in magnetic field induces a bigger voltage - the idea behind every generator.",
        "একটা চুম্বককে একটা কুণ্ডলীতে প্রথমে ধীরে, পরে দ্রুত ঠেলা হলো। দ্রুত ঠেললে আবিষ্ট ভোল্টেজের কী হয়?", ["বড় হয়", "ছোট হয়", "একই থাকে", "শূন্য হয়"],
        "চৌম্বক ক্ষেত্র দ্রুত বদলালে বেশি ভোল্টেজ আবিষ্ট হয় - প্রতিটা জেনারেটরের মূল ভাবনা।"),
    mcq("What is the 'half-life' of a radioactive source?", ["The time for its activity to fall to half", "Half the time it takes to make", "The time until it explodes", "Half its weight"], 0,
        "After two half-lives a quarter remains; after three, an eighth.",
        "তেজস্ক্রিয় উৎসের 'অর্ধায়ু' কী?", ["সক্রিয়তা অর্ধেক হতে যে সময় লাগে", "বানাতে যে সময় লাগে তার অর্ধেক", "বিস্ফোরণ পর্যন্ত সময়", "এর ওজনের অর্ধেক"],
        "দুই অর্ধায়ু পরে এক-চতুর্থাংশ থাকে; তিনটের পরে এক-অষ্টমাংশ।"),
    mcq("Why do inspectors use gamma or X-ray radiography on bridge welds?", ["The rays pass through steel and show hidden cracks or holes on film", "To make welds hotter", "To paint the welds", "To magnetise the steel"], 0,
        "Workers stay behind barriers and wear badges that measure their dose.",
        "পরিদর্শকরা সেতুর ঝালাইয়ে গামা বা এক্স-রে রেডিওগ্রাফি ব্যবহার করেন কেন?", ["রশ্মি ইস্পাত ভেদ করে ফিল্মে লুকোনো ফাটল বা ফুটো দেখায়", "ঝালাই গরম করতে", "ঝালাইয়ে রং করতে", "ইস্পাতকে চুম্বক করতে"],
        "কর্মীরা আড়ালে থাকেন আর মাত্রা-মাপার ব্যাজ পরেন।"),
    mcq("Which radiation is stopped by a sheet of paper?", ["Alpha", "Gamma", "X-rays", "Radio waves"], 0,
        "Beta needs a few mm of aluminium; gamma needs thick lead or concrete.",
        "কোন বিকিরণ এক পাতা কাগজে আটকে যায়?", ["আলফা", "গামা", "এক্স-রে", "বেতার-তরঙ্গ"],
        "বিটার জন্য কয়েক mm অ্যালুমিনিয়াম লাগে; গামার জন্য মোটা সিসা বা কংক্রিট।"),
    mcq("What is 'resonance' in a bridge?", ["Large vibrations when a regular push matches the bridge's natural frequency", "The bridge's echo", "A type of paint", "The colour of steel"], 0,
        "That is why soldiers break step when marching across a bridge.",
        "সেতুতে 'অনুনাদ' কী?", ["নিয়মিত ধাক্কা সেতুর স্বাভাবিক কম্পাঙ্কের সঙ্গে মিললে বড় কম্পন", "সেতুর প্রতিধ্বনি", "এক রকম রং", "ইস্পাতের রং"],
        "তাই সৈন্যরা সেতু পার হওয়ার সময় পা মিলিয়ে কুচকাওয়াজ থামায়।"),
    mcq("London's Millennium Bridge wobbled on opening day in 2000. What caused it?", ["Walkers fell into step with the sway, pushing it in time and making it worse", "A storm", "An earthquake", "A heavy truck"], 0,
        "Engineers added dampers - like shock absorbers - to fix it.",
        "2000 সালে উদ্বোধনের দিন লন্ডনের মিলেনিয়াম ব্রিজ দুলে উঠেছিল। কারণ কী?", ["পথচারীরা দোলার সঙ্গে পা মিলিয়ে ফেলেন, তালে তালে ঠেলে দোলা বাড়িয়ে দেন", "ঝড়", "ভূমিকম্প", "একটা ভারী ট্রাক"],
        "প্রকৌশলীরা ড্যাম্পার - শক অ্যাবজর্বারের মতো - বসিয়ে ঠিক করেন।"),
    mcq("What does a 'damper' on a cable-stayed bridge do?", ["Absorbs vibration energy so the cables stop swinging", "Keeps the cables wet", "Makes the bridge longer", "Lights the bridge at night"], 0,
        "Rain and wind together can make stay cables gallop without them.",
        "কেবল-স্টেড সেতুতে 'ড্যাম্পার' কী করে?", ["কম্পনের শক্তি শুষে নেয়, যাতে তার দোলা থামে", "তার ভেজা রাখে", "সেতু লম্বা করে", "রাতে সেতু আলো করে"],
        "এটা না থাকলে বৃষ্টি আর হাওয়া মিলে টানা-তারকে লাফাতে পারে।"),
    mcq("Why did the Tacoma Narrows Bridge collapse in 1940?", ["Wind made its thin, flexible deck twist more and more until it tore apart", "A ship hit it", "It was too heavy", "Termites ate it"], 0,
        "Since then, decks are tested in wind tunnels before they are built.",
        "1940 সালে ট্যাকোমা ন্যারোজ সেতু ভেঙে পড়েছিল কেন?", ["হাওয়ায় এর পাতলা, নমনীয় পাটাতন ক্রমশ বেশি মোচড় খেয়ে ছিঁড়ে যায়", "একটা জাহাজ ধাক্কা দেয়", "খুব ভারী ছিল", "উইপোকা খেয়ে ফেলে"],
        "তারপর থেকে পাটাতন বানানোর আগে বায়ু-সুড়ঙ্গে পরীক্ষা হয়।"),
    mcq("Heavy planters are added to a footbridge without making it any stiffer. What happens to its natural frequency?", ["It goes down", "It goes up", "It stays exactly the same", "It becomes zero"], 0,
        "More mass with the same stiffness vibrates more slowly - which may bring it closer to walking pace.",
        "একটা পায়ে-চলা সেতুতে ভারী টব বসানো হলো, কিন্তু সেতু একটুও শক্ত করা হলো না। এর স্বাভাবিক কম্পাঙ্কের কী হয়?", ["কমে", "বাড়ে", "হুবহু একই থাকে", "শূন্য হয়"],
        "একই দৃঢ়তায় ভর বাড়লে কম্পন ধীর হয় - যা হাঁটার তালের কাছাকাছি চলে আসতে পারে।"),
    mcq("Why are holes and sharp corners in a steel plate places where cracks often start?", ["Stress crowds around them and becomes much higher than in the rest of the plate", "Holes make steel softer everywhere", "Corners attract rust only", "Cracks only start in the middle of plates"], 0,
        "This is 'stress concentration' - designers round corners and smooth edges to avoid it.",
        "ইস্পাতের পাতের ফুটো আর ধারালো কোণ থেকে প্রায়ই ফাটল শুরু হয় কেন?", ["পীড়ন সেখানে ভিড় করে আর পাতের বাকি অংশের চেয়ে অনেক বেশি হয়", "ফুটো সব জায়গায় ইস্পাত নরম করে", "কোণ শুধু মরচে টানে", "ফাটল শুধু পাতের মাঝখানে শুরু হয়"],
        "একে 'পীড়ন-ঘনীভবন' বলে - নকশাকাররা কোণ গোল আর ধার মসৃণ করে এটা এড়ান।"),
    mcq("Why are suspension bridge main cables made of thousands of thin wires rather than one solid bar?", ["Thin wires can be made very strong and flexible, and one broken wire does not fail the cable", "Solid bars cannot carry tension", "Wires are cheaper to paint", "To make the bridge heavier"], 0,
        "Many small parallel paths for the load also make the cable easier to inspect and repair.",
        "ঝুলন্ত সেতুর মূল তার একটা নিরেট দণ্ডের বদলে হাজার হাজার সরু তার দিয়ে বানানো হয় কেন?", ["সরু তার খুব শক্ত আর নমনীয় করা যায়, আর একটা তার ছিঁড়লে গোটা তার ব্যর্থ হয় না", "নিরেট দণ্ড টান বইতে পারে না", "তারে রং করা সস্তা", "সেতু ভারী করতে"],
        "বোঝার জন্য অনেক ছোট সমান্তরাল পথ থাকায় পরীক্ষা আর মেরামতও সহজ।"),
    mcq("Why do engineers apply a 'factor of safety' of, say, 2 to a bridge member?", ["To allow for unknowns - the member is made twice as strong as the worst expected load needs", "To make it twice as heavy for no reason", "To halve the cost", "Because the law says use 2 for everything"], 0,
        "Material flaws, extra loads and wear are all covered by this margin.",
        "প্রকৌশলীরা সেতুর অংশে, ধরো, 2-এর 'নিরাপত্তা-গুণক' দেন কেন?", ["অজানার জন্য জায়গা রাখতে - সবচেয়ে খারাপ প্রত্যাশিত বোঝার চেয়ে অংশটা দ্বিগুণ শক্ত করা হয়", "অকারণে দ্বিগুণ ভারী করতে", "খরচ অর্ধেক করতে", "আইনে সবকিছুতে 2 বলা আছে"],
        "উপাদানের ত্রুটি, বাড়তি বোঝা আর ক্ষয় এই ফাঁকে ধরা থাকে।"),
    mcq("A steel tie can carry 300 kN before failing. With a factor of safety of 2, what is the most load it should carry in use?", ["150 kN", "600 kN", "300 kN", "302 kN"], 0,
        "Safe working load = failure load ÷ factor of safety = 300 ÷ 2 = 150 kN.",
        "একটা ইস্পাতের টানা-দণ্ড ভাঙার আগে 300 kN বইতে পারে। নিরাপত্তা-গুণক 2 হলে ব্যবহারে সর্বোচ্চ কত বোঝা বওয়া উচিত?", ["150 kN", "600 kN", "300 kN", "302 kN"],
        "নিরাপদ কার্যকর বোঝা = ভাঙার বোঝা ÷ নিরাপত্তা-গুণক = 300 ÷ 2 = 150 kN।"),
    mcq("What is 'metal fatigue'?", ["Cracks that grow slowly after millions of small repeated loads, even below the breaking stress", "Metal getting tired and sleeping", "Rust on the surface", "Metal melting in summer"], 0,
        "Every truck crossing is one small load cycle - inspectors look for fatigue cracks at welds.",
        "'ধাতুর ক্লান্তি' কী?", ["লক্ষ লক্ষ বার ছোট বোঝা বারবার পড়লে ধীরে বাড়া ফাটল, ভাঙার পীড়নের নিচেও", "ধাতু ক্লান্ত হয়ে ঘুমায়", "উপরিতলে মরচে", "গ্রীষ্মে ধাতু গলে"],
        "প্রতিটা ট্রাক পারাপার একটা ছোট বোঝা-চক্র - পরিদর্শকরা ঝালাইয়ে ক্লান্তি-ফাটল খোঁজেন।"),
    mcq("What is 'creep' in a concrete bridge?", ["Slow, continuing deformation under a constant load over years", "Insects crawling on it", "Traffic moving slowly", "Paint peeling"], 0,
        "Long concrete spans can sag a few centimetres over decades because of creep.",
        "কংক্রিটের সেতুতে 'ক্রিপ' কী?", ["স্থির বোঝার নিচে বছরের পর বছর ধীরে চলতে থাকা বিকৃতি", "পোকা হেঁটে বেড়ানো", "ধীরে চলা যানবাহন", "রং উঠে যাওয়া"],
        "ক্রিপের জন্য লম্বা কংক্রিট-স্প্যান কয়েক দশকে কয়েক সেন্টিমিটার ঝুলে পড়তে পারে।"),
    mcq("Why are bridge decks often given a slight upward curve (camber) when built?", ["So that after the deck settles under its own weight and traffic, it ends up level", "To make cars jump", "To collect rainwater in the middle", "For decoration only"], 0,
        "It also helps rainwater drain to the sides.",
        "বানানোর সময় সেতুর পাটাতনে প্রায়ই সামান্য উপরের দিকে বাঁক (ক্যাম্বার) দেওয়া হয় কেন?", ["নিজের ওজন আর যানবাহনে বসে যাওয়ার পরে যাতে সমতল হয়", "গাড়ি লাফাতে", "মাঝখানে বৃষ্টির জল জমাতে", "শুধু সাজাতে"],
        "এতে বৃষ্টির জলও দুপাশে গড়িয়ে যায়।"),
    mcq("What is 'deflection' of a beam?", ["How far it bends down under load", "How shiny it is", "Its length", "Its weight"], 0,
        "Codes limit deflection so decks feel solid and finishes do not crack.",
        "কড়ির 'বিক্ষেপ' কী?", ["বোঝায় কতটা নিচে বাঁকে", "কতটা চকচকে", "এর দৈর্ঘ্য", "এর ওজন"],
        "নিয়মে বিক্ষেপ সীমিত রাখা হয়, যাতে পাটাতন মজবুত লাগে আর উপরের স্তরে ফাটল না ধরে।"),
    mcq("Doubling a beam's depth (keeping the same width) does what to its stiffness?", ["Makes it about 8 times stiffer", "Makes it 2 times stiffer", "Halves it", "No change"], 0,
        "Bending stiffness grows with depth cubed: 2³ = 8. That is why beams are deep, not wide.",
        "একটা কড়ির গভীরতা দ্বিগুণ করলে (প্রস্থ একই রেখে) দৃঢ়তার কী হয়?", ["প্রায় 8 গুণ শক্ত হয়", "2 গুণ শক্ত হয়", "অর্ধেক হয়", "বদলায় না"],
        "বাঁকার দৃঢ়তা গভীরতার ঘনফলের সঙ্গে বাড়ে: 2³ = 8। তাই কড়ি চওড়া নয়, গভীর হয়।"),
    mcq("Why is an I-shaped steel beam so efficient?", ["Most of its material sits in the flanges, far from the middle, where bending stress is largest", "It is shaped like a letter for decoration", "It is hollow and full of air", "It has no flanges"], 0,
        "The thin web joins the flanges and carries shear.",
        "I-আকারের ইস্পাতের কড়ি এত দক্ষ কেন?", ["বেশিরভাগ উপাদান মাঝখান থেকে দূরে ফ্ল্যাঞ্জে থাকে, যেখানে বাঁকার পীড়ন সবচেয়ে বেশি", "সাজাতে অক্ষরের আকার", "ফাঁপা আর হাওয়ায় ভরা", "এর ফ্ল্যাঞ্জ নেই"],
        "সরু ওয়েব ফ্ল্যাঞ্জ দুটোকে জোড়ে আর কর্তন-বল বয়।"),
    mcq("When a beam sags under load, which part is in tension?", ["The bottom", "The top", "Neither", "Only the ends"], 0,
        "The top is squeezed (compression); the bottom is stretched (tension) - so steel bars go in the bottom of concrete beams.",
        "বোঝায় কড়ি নিচে ঝুলে পড়লে কোন অংশে টান?", ["নিচের দিক", "উপরের দিক", "কোনোটাই না", "শুধু প্রান্ত"],
        "উপরটা চাপে (সংনমন); নিচটা টানে (প্রসারণ) - তাই কংক্রিটের কড়ির নিচে ইস্পাতের রড থাকে।"),
    mcq("What is 'shear force' in a beam?", ["The force trying to slide one part of the beam past the next", "The force that paints it", "The beam's weight only", "A force that cools it"], 0,
        "Shear is largest near the supports, so stirrups are packed closer there.",
        "কড়িতে 'কর্তন-বল' কী?", ["যে বল কড়ির এক অংশকে পাশের অংশের পাশ দিয়ে পিছলে দিতে চায়", "যে বল রং করে", "শুধু কড়ির ওজন", "যে বল ঠান্ডা করে"],
        "ঠেকনার কাছে কর্তন সবচেয়ে বেশি, তাই সেখানে স্টিরাপ ঘন করে বসানো হয়।"),
    mcq("A crane's counterweight helps it lift heavy loads safely. Why?", ["It provides an opposite moment so the crane does not topple", "It makes the hook heavier", "It powers the motor", "It stops rain"], 0,
        "Total clockwise moment must not exceed the anticlockwise moment about the tipping edge.",
        "ক্রেনের পাল্টা-ওজন ভারী বোঝা নিরাপদে তুলতে সাহায্য করে কেন?", ["উল্টো ভ্রামক দেয়, যাতে ক্রেন উল্টে না পড়ে", "হুক ভারী করে", "মোটর চালায়", "বৃষ্টি থামায়"],
        "উল্টানোর ধারের সাপেক্ষে মোট দক্ষিণাবর্ত ভ্রামক বামাবর্তকে ছাড়াতে পারবে না।"),
    mcq("What is 'terminal velocity' for an object falling from a bridge?", ["The steady speed reached when air resistance equals its weight", "The speed at the moment it is dropped", "The speed of sound", "Zero"], 0,
        "After that, forces are balanced, so it stops accelerating.",
        "সেতু থেকে পড়া বস্তুর 'প্রান্তিক বেগ' কী?", ["বায়ুর বাধা ওজনের সমান হলে যে স্থির বেগে পৌঁছায়", "ফেলার মুহূর্তের বেগ", "শব্দের বেগ", "শূন্য"],
        "তারপর বল সাম্যে থাকে, তাই ত্বরণ থেমে যায়।"),
    mcq("Why do workers on high bridges use tool lanyards?", ["A dropped spanner gains a lot of kinetic energy and can kill someone below", "Tools get lonely", "To make tools heavier", "To stop rust"], 0,
        "A 1 kg spanner falling 45 m hits at about 30 m/s.",
        "উঁচু সেতুতে কর্মীরা যন্ত্রে দড়ি বেঁধে রাখেন কেন?", ["পড়ে যাওয়া স্প্যানার অনেক গতিশক্তি পায় আর নিচে কাউকে মেরে ফেলতে পারে", "যন্ত্র একা বোধ করে", "যন্ত্র ভারী করতে", "মরচে আটকাতে"],
        "1 kg-এর স্প্যানার 45 m পড়লে প্রায় 30 m/s বেগে আঘাত করে।"),
    mcq("What is 'centripetal force' on a car going round a curved bridge ramp?", ["The inward force (from tyre grip) that keeps it turning", "An outward force that throws it off", "The car's engine force", "Gravity pulling it forward"], 0,
        "Ramps are banked so part of the road's push helps turn the car.",
        "বাঁকা সেতু-ঢালে ঘোরা গাড়ির উপর 'কেন্দ্রমুখী বল' কী?", ["ভেতরের দিকে বল (টায়ারের আঁকড়ে ধরা থেকে) যা গাড়িকে বাঁকে রাখে", "বাইরের দিকে ছুড়ে ফেলার বল", "গাড়ির ইঞ্জিনের বল", "সামনে টানা মাধ্যাকর্ষণ"],
        "ঢালগুলো হেলানো থাকে, যাতে রাস্তার ঠেলার একটা অংশ গাড়ি ঘোরাতে সাহায্য করে।"),
    mcq("A worker's ear protectors are rated to cut noise by 30 dB. Why is this important near a pile-driver?", ["Loud noise over time permanently damages hearing", "Noise makes steel weaker", "Ear protectors keep heads warm only", "Pile-drivers are silent"], 0,
        "Hearing damage cannot be repaired - prevention is the only cure.",
        "একজন কর্মীর কানের সুরক্ষা 30 dB শব্দ কমায়। পাইল-ড্রাইভারের কাছে এটা জরুরি কেন?", ["দীর্ঘ সময় জোরালো শব্দ শ্রবণশক্তির স্থায়ী ক্ষতি করে", "শব্দ ইস্পাত দুর্বল করে", "কানের সুরক্ষা শুধু মাথা গরম রাখে", "পাইল-ড্রাইভার নিঃশব্দ"],
        "শ্রবণের ক্ষতি সারানো যায় না - প্রতিরোধই একমাত্র উপায়।"),
    mcq("How do ultrasonic testers find flaws inside a steel plate?", ["High-frequency sound echoes back early from a crack inside", "They heat the plate until it glows", "They listen to the plate sing", "They count the bolts"], 0,
        "The echo's timing tells how deep the flaw is.",
        "আল্ট্রাসোনিক পরীক্ষক ইস্পাতের পাতের ভেতরের ত্রুটি কীভাবে খোঁজেন?", ["উচ্চ-কম্পাঙ্কের শব্দ ভেতরের ফাটল থেকে আগে প্রতিধ্বনি হয়ে ফেরে", "পাত গনগনে লাল হওয়া পর্যন্ত গরম করেন", "পাতের গান শোনেন", "বল্টু গোনেন"],
        "প্রতিধ্বনির সময় বলে দেয় ত্রুটি কত গভীরে।"),
    mcq("Why is a lightning conductor fitted to the top of a tall bridge tower?", ["It gives lightning a safe, low-resistance path to earth", "It attracts rain", "It makes the tower taller for photos", "It charges phones"], 0,
        "Without it, a strike could damage cables, electronics or concrete.",
        "উঁচু সেতু-মিনারের মাথায় বজ্রনিরোধক বসানো হয় কেন?", ["বাজকে মাটিতে যাওয়ার নিরাপদ, কম-রোধের পথ দেয়", "বৃষ্টি টানে", "ছবির জন্য মিনার লম্বা করে", "ফোন চার্জ করে"],
        "এটা না থাকলে বাজ পড়ে তার, ইলেকট্রনিক্স বা কংক্রিটের ক্ষতি হতে পারে।"),
    mcq("What is 'cathodic protection' on a steel bridge pier in the sea?", ["A small electric current or sacrificial metal makes the steel the cathode so it does not corrode", "A coat of paint only", "A fence around the pier", "Cooling the steel"], 0,
        "Zinc or aluminium blocks corrode instead of the steel.",
        "সমুদ্রে ইস্পাতের সেতু-স্তম্ভে 'ক্যাথোডিক সুরক্ষা' কী?", ["ছোট বৈদ্যুতিক প্রবাহ বা আত্মত্যাগী ধাতু ইস্পাতকে ক্যাথোড বানায়, তাই ক্ষয় হয় না", "শুধু এক পোঁচ রং", "স্তম্ভের চারপাশে বেড়া", "ইস্পাত ঠান্ডা রাখা"],
        "ইস্পাতের বদলে দস্তা বা অ্যালুমিনিয়ামের খণ্ড ক্ষয়ে যায়।"),
    mcq("What does an anemometer on a bridge measure?", ["Wind speed - the bridge may close to high-sided vehicles in strong wind", "Traffic speed", "Rainfall", "Temperature only"], 0,
        "Strong side winds can blow over empty trucks on exposed bridges.",
        "সেতুর অ্যানিমোমিটার কী মাপে?", ["হাওয়ার গতি - জোর হাওয়ায় উঁচু-পাশের গাড়ির জন্য সেতু বন্ধ হতে পারে", "যানবাহনের গতি", "বৃষ্টিপাত", "শুধু তাপমাত্রা"],
        "খোলা সেতুতে জোরালো পাশের হাওয়া খালি ট্রাক উল্টে দিতে পারে।"),
    mcq("What is a 'strain gauge' on a bridge used for?", ["Measuring tiny stretches in a member to work out the stress it carries", "Measuring rainfall", "Counting vehicles", "Measuring paint thickness"], 0,
        "Its electrical resistance changes as it stretches.",
        "সেতুতে 'বিকৃতি-মাপক' কীসের জন্য ব্যবহার হয়?", ["অংশের খুব ছোট টান মেপে তার পীড়ন হিসাব করতে", "বৃষ্টি মাপতে", "গাড়ি গুনতে", "রঙের পুরুত্ব মাপতে"],
        "টান লাগলে এর বৈদ্যুতিক রোধ বদলায়।"),
)
