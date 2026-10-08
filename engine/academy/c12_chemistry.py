"""Class 12 - Chemistry (Chief Engineer): carbon equivalent and weldability, zinc coating
thickness, corrosion rate from mass loss, the Nernst equation, cement clinker phases and heat of
hydration, pozzolans and low-carbon cements, first-order kinetics, temperature and rate,
steelmaking and heat treatment, welding metallurgy, polymers for bridges and green steel."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r * 2, r + 10, r + 2):
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


def ce(c, mn, cr, mo, v, ni, cu):
    r = _c(c + mn / 6 + (cr + mo + v) / 5 + (ni + cu) / 15)
    return _n(f"A bridge steel contains C {c:g}%, Mn {mn:g}%, Cr {cr:g}%, Mo {mo:g}%, V {v:g}%, Ni {ni:g}%, Cu {cu:g}%. What is its carbon equivalent? (CE = C + Mn/6 + (Cr + Mo + V)/5 + (Ni + Cu)/15)",
              f"একটা সেতু-ইস্পাতে C {c:g}%, Mn {mn:g}%, Cr {cr:g}%, Mo {mo:g}%, V {v:g}%, Ni {ni:g}%, Cu {cu:g}%। এর কার্বন-সমতুল্য কত? (CE = C + Mn/6 + (Cr + Mo + V)/5 + (Ni + Cu)/15)", r,
              f"CE = {c:g} + {_c(mn / 6):g} + {_c((cr + mo + v) / 5):g} + {_c((ni + cu) / 15):g} = {r:g}. Above about 0.45, preheating is usually needed to avoid weld cracking.",
              f"CE = {c:g} + {_c(mn / 6):g} + {_c((cr + mo + v) / 5):g} + {_c((ni + cu) / 15):g} = {r:g}। প্রায় 0.45-এর উপরে ঝালাই-ফাটল এড়াতে সাধারণত আগে গরম করতে হয়।",
              (_c(c + mn + cr + mo + v + ni + cu), _c(c + mn / 6), c))


def zinc(g_m2):
    t = round(g_m2 / 7.14, 1)
    return _n(f"A galvanised bridge railing has a zinc coating of {g_m2} g/m². Zinc's density is 7.14 g/cm³. How thick is the coating in micrometres?",
              f"একটা গ্যালভানাইজড সেতু-রেলিংয়ে দস্তার আবরণ {g_m2} g/m²। দস্তার ঘনত্ব 7.14 g/cm³। আবরণ কত মাইক্রোমিটার পুরু?", t,
              f"Thickness (µm) = mass per area (g/m²) ÷ density (g/cm³) = {g_m2} ÷ 7.14 ≈ {t:g} µm.",
              f"পুরুত্ব (µm) = ক্ষেত্রফলপ্রতি ভর (g/m²) ÷ ঘনত্ব (g/cm³) = {g_m2} ÷ 7.14 ≈ {t:g} µm।",
              (round(g_m2 * 7.14 / 100, 1), round(g_m2 / 71.4, 1), round(t * 2, 1)), " µm")


def corrate(loss_g, area_cm2, years):
    r = _c(loss_g / (7.85 * area_cm2) * 10 / years)
    return _n(f"A steel test coupon of {area_cm2} cm² exposed under a bridge loses {loss_g:g} g in {years} years. Steel's density is 7.85 g/cm³. What is the average corrosion rate in mm per year?",
              f"সেতুর নিচে রাখা {area_cm2} cm²-এর একটা ইস্পাতের পরীক্ষা-টুকরো {years} বছরে {loss_g:g} g হারাল। ইস্পাতের ঘনত্ব 7.85 g/cm³। গড় ক্ষয়ের হার বছরে কত mm?", r,
              f"Thickness lost = {loss_g:g} ÷ (7.85 x {area_cm2}) cm = {_c(loss_g / (7.85 * area_cm2) * 10):g} mm; ÷ {years} years = {r:g} mm/year.",
              f"হারানো পুরুত্ব = {loss_g:g} ÷ (7.85 x {area_cm2}) cm = {_c(loss_g / (7.85 * area_cm2) * 10):g} mm; ÷ {years} বছর = বছরে {r:g} mm।",
              (_c(loss_g / (7.85 * area_cm2) * 10), _c(r * 10), _c(loss_g / area_cm2)), " mm/yr", " mm/বছর")


def nernst(e0, n, q_pow):
    e = _c(e0 - 0.059 / n * q_pow)
    return _n(f"For a half-reaction with E° = {e0:+.2f} V and n = {n} electrons, the reaction quotient Q = 10^{q_pow}. Using E = E° - (0.059/n) log Q, what is E?",
              f"E° = {e0:+.2f} V আর n = {n}টি ইলেকট্রনের একটা অর্ধ-বিক্রিয়ায় বিক্রিয়া-ভাগফল Q = 10^{q_pow}। E = E° - (0.059/n) log Q ধরে E কত?", e,
              f"E = {e0:g} - (0.059 ÷ {n}) x {q_pow} = {e:g} V. Concentration differences shift electrode potentials and drive corrosion cells.",
              f"E = {e0:g} - (0.059 ÷ {n}) x {q_pow} = {e:g} V। গাঢ়ত্বের পার্থক্য তড়িদ্বার-বিভব সরায় আর ক্ষয়-কোষ চালায়।",
              (_c(e0 + 0.059 / n * q_pow) if e0 + 0.059 / n * q_pow > 0 else _c(abs(e) + 0.2), _c(abs(e0)), _c(abs(e) + 0.1)), " V") if e > 0 else None


def hydheat(mass_t, j_per_g):
    r = _c(mass_t * 1e6 * j_per_g / 1e9)
    return _n(f"A massive pier footing contains {mass_t:,} tonnes of cement, which releases about {j_per_g} J/g as it hydrates. How much heat is released in total, in gigajoules?",
              f"একটা বিশাল স্তম্ভ-ভিতে {mass_t:,} টন সিমেন্ট, যা জলযোজনে প্রায় {j_per_g} J/g তাপ ছাড়ে। মোট কত তাপ বেরোয়, গিগাজুলে?", r,
              f"{mass_t:,} t = {mass_t * 1e6:,.0f} g; x {j_per_g} J/g = {_c(mass_t * 1e6 * j_per_g):,.0f} J = {r:g} GJ. Cooling pipes or low-heat cement may be needed.",
              f"{mass_t:,} টন = {mass_t * 1e6:,.0f} g; x {j_per_g} J/g = {_c(mass_t * 1e6 * j_per_g):,.0f} J = {r:g} গিগাজুল। শীতলীকরণ-পাইপ বা কম-তাপের সিমেন্ট লাগতে পারে।",
              (_c(r * 1000), _c(r / 1000), _c(mass_t * j_per_g)), " GJ", " গিগাজুল")


def co2save(cement_t, repl, co2_per_t):
    r = _c(cement_t * repl / 100 * co2_per_t)
    return _n(f"A bridge needs {cement_t:,} tonnes of cement. Replacing {repl}% with GGBS saves about {co2_per_t:g} t of CO2 per tonne replaced. How much CO2 is saved?",
              f"একটা সেতুতে {cement_t:,} টন সিমেন্ট লাগে। {repl}% জিজিবিএস দিয়ে বদলালে প্রতি টন বদলে প্রায় {co2_per_t:g} টন CO2 বাঁচে। কত CO2 বাঁচে?", r,
              f"Replaced = {cement_t:,} x {repl}% = {_c(cement_t * repl / 100):g} t; x {co2_per_t:g} = {r:g} t of CO2.",
              f"বদলানো = {cement_t:,} x {repl}% = {_c(cement_t * repl / 100):g} টন; x {co2_per_t:g} = {r:g} টন CO2।",
              (_c(cement_t * co2_per_t), _c(cement_t * repl / 100), _c(r / 2)), " t", " টন")


def halflife1(k):
    t = _c(0.693 / k)
    return _n(f"A curing compound breaks down by first-order kinetics with rate constant k = {k:g} per day. What is its half-life? (t½ = 0.693 ÷ k)",
              f"একটা কিউরিং-যৌগ প্রথম-ক্রমের গতিবিদ্যায় ভাঙে, হার-ধ্রুবক k = দিনে {k:g}। এর অর্ধায়ু কত? (t½ = 0.693 ÷ k)", t,
              f"t½ = 0.693 ÷ {k:g} = {t:g} days - and it does not depend on the starting amount.",
              f"t½ = 0.693 ÷ {k:g} = {t:g} দিন - আর এটা শুরুর পরিমাণের উপর নির্ভর করে না।",
              (_c(k * 0.693), _c(1 / k), _c(t * 2)), " days", " দিন")


def q10(rate, dt):
    r = _c(rate * 2 ** (dt / 10))
    return _n(f"A corrosion reaction runs at {rate:g} units at 20°C and roughly doubles for every 10°C rise. What rate would you expect at {20 + dt}°C?",
              f"একটা ক্ষয়-বিক্রিয়া 20°C-এ {rate:g} একক হারে চলে আর প্রতি 10°C বাড়লে মোটামুটি দ্বিগুণ হয়। {20 + dt}°C-এ কত হার আশা করবে?", r,
              f"{dt}°C rise = {dt / 10:g} doublings: {rate:g} x 2^{dt / 10:g} = {r:g}.",
              f"{dt}°C বৃদ্ধি = {dt / 10:g} বার দ্বিগুণ: {rate:g} x 2^{dt / 10:g} = {r:g}।",
              (_c(rate * (1 + dt / 10)), _c(rate * dt), _c(rate * 2)))


def ppm(mg, litres, what_en, what_bn):
    r = _c(mg / litres)
    return _n(f"A {litres:g} L sample of mixing water contains {mg:g} mg of {what_en}. What is the concentration in ppm (mg/L)?",
              f"মেশানোর জলের {litres:g} L নমুনায় {mg:g} mg {what_bn}। পিপিএম-এ (mg/L) গাঢ়ত্ব কত?", r,
              f"{mg:g} ÷ {litres:g} = {r:g} mg/L = {r:g} ppm. Specifications limit chlorides and sulfates in concrete water.",
              f"{mg:g} ÷ {litres:g} = {r:g} mg/L = {r:g} পিপিএম। নির্দেশিকা কংক্রিটের জলে ক্লোরাইড আর সালফেট সীমিত রাখে।",
              (_c(mg * litres), _c(litres / mg * 1000), _c(r * 10)), " ppm", " পিপিএম")


ITEMS = tuple(q for q in (
    ce(0.18, 1.4, 0.1, 0.0, 0.05, 0.1, 0.2), ce(0.12, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0), ce(0.20, 1.2, 0.3, 0.2, 0.0, 0.3, 0.3),
    ce(0.15, 0.9, 0.5, 0.0, 0.0, 0.15, 0.3),
    zinc(610), zinc(500), zinc(714), zinc(1000),
    corrate(62.8, 100, 4), corrate(11.775, 50, 2), corrate(47.1, 200, 3),
    nernst(0.34, 2, -2), nernst(0.80, 1, 2), nernst(0.34, 2, 2), nernst(1.23, 4, 4),
    hydheat(500, 400), hydheat(1200, 350), hydheat(250, 450),
    co2save(5000, 50, 0.8), co2save(12000, 30, 0.85), co2save(2000, 70, 0.8),
    halflife1(0.1), halflife1(0.231), halflife1(0.0693), halflife1(0.35),
    q10(2, 10), q10(3, 20), q10(5, 30), q10(1.5, 15),
    ce(0.16, 1.2, 0.2, 0.1, 0.03, 0.2, 0.15), zinc(850), corrate(37.68, 80, 2), nernst(0.80, 1, 1), hydheat(800, 380),
    co2save(8000, 40, 0.82), halflife1(0.0462), q10(4, 25), ppm(120, 3, "nitrate", "নাইট্রেট"),
    ppm(500, 2, "chloride", "ক্লোরাইড"), ppm(1500, 5, "sulfate", "সালফেট"), ppm(30, 0.5, "sugar", "চিনি"), ppm(200, 4, "suspended solids", "ভাসমান কঠিন"),
    mcq("What does a high 'carbon equivalent' (CE) warn a welding engineer about?", ["The steel is more hardenable and prone to cracking near welds, so preheat and controlled procedures are needed", "The steel cannot be welded at all", "The steel is softer", "The steel is stainless"], 0,
        "CE combines the hardening effects of carbon and alloying elements.",
        "উচ্চ 'কার্বন-সমতুল্য' (সিই) ঝালাই-প্রকৌশলীকে কী নিয়ে সতর্ক করে?", ["ইস্পাত বেশি শক্ত-হওয়ার প্রবণ আর ঝালাইয়ের কাছে ফাটতে পারে, তাই আগে গরম আর নিয়ন্ত্রিত পদ্ধতি লাগে", "ইস্পাত ঝালাই করাই যায় না", "ইস্পাত নরম", "ইস্পাত স্টেইনলেস"],
        "সিই কার্বন আর সংকর-মৌলের শক্ত-করার প্রভাব মেশায়।"),
    mcq("What is the 'heat-affected zone' (HAZ) in welding?", ["The region of base metal next to a weld whose structure has been changed by heat without melting", "The flame itself", "The welder's mask", "The cooling water"], 0,
        "It can become hard and brittle if cooled too fast.",
        "ঝালাইয়ে 'তাপ-প্রভাবিত অঞ্চল' (এইচএজেড) কী?", ["ঝালাইয়ের পাশের মূল ধাতুর অঞ্চল, যার গঠন না গলে তাপে বদলে গেছে", "শিখা নিজেই", "ঝালাইকারের মুখোশ", "শীতলীকরণের জল"],
        "খুব দ্রুত ঠান্ডা হলে শক্ত আর ভঙ্গুর হতে পারে।"),
    mcq("What causes 'hydrogen cracking' in welded bridge steel?", ["Hydrogen from moisture in consumables diffuses into a hard HAZ under stress, causing delayed cracks", "Too much paint", "Cold rain after welding only", "Oxygen in the air"], 0,
        "Dry electrodes, preheat and controlled cooling prevent it.",
        "ঝালাই-করা সেতু-ইস্পাতে 'হাইড্রোজেন-ফাটল' কী থেকে হয়?", ["সরঞ্জামের আর্দ্রতার হাইড্রোজেন পীড়নে থাকা শক্ত এইচএজেড-এ ঢুকে দেরিতে ফাটল ঘটায়", "বেশি রং", "শুধু ঝালাইয়ের পরে ঠান্ডা বৃষ্টি", "বাতাসের অক্সিজেন"],
        "শুকনো ইলেকট্রোড, আগে গরম আর নিয়ন্ত্রিত ঠান্ডা এটা ঠেকায়।"),
    mcq("Why are welding electrodes stored in heated ovens on site?", ["To keep their flux coatings dry, preventing hydrogen from moisture entering the weld", "To make them glow", "To save space", "To sterilise them"], 0,
        "Low-hydrogen electrodes lose their benefit if they absorb water.",
        "নির্মাণস্থলে ঝালাইয়ের ইলেকট্রোড গরম চুল্লিতে রাখা হয় কেন?", ["ফ্লাক্স-আবরণ শুকনো রাখতে, যাতে আর্দ্রতার হাইড্রোজেন ঝালাইয়ে না ঢোকে", "জ্বলজ্বলে করতে", "জায়গা বাঁচাতে", "জীবাণুমুক্ত করতে"],
        "কম-হাইড্রোজেন ইলেকট্রোড জল শুষলে সুবিধা হারায়।"),
    mcq("What happens to steel when it is 'quenched' from red heat?", ["Rapid cooling forms hard martensite, which is strong but brittle until tempered", "It becomes soft and ductile", "It melts", "It turns into iron oxide only"], 0,
        "Tempering then trades some hardness for toughness.",
        "লাল-গরম থেকে ইস্পাতকে 'হঠাৎ ঠান্ডা' (কুয়েঞ্চ) করলে কী হয়?", ["দ্রুত ঠান্ডায় শক্ত মার্টেনসাইট তৈরি হয়, যা টেম্পার না করা পর্যন্ত শক্ত কিন্তু ভঙ্গুর", "নরম আর নমনীয় হয়", "গলে যায়", "শুধু আয়রন অক্সাইড হয়"],
        "তারপর টেম্পারিং কিছু কাঠিন্যের বদলে দৃঢ়তা-সহনশীলতা দেয়।"),
    mcq("What is 'tempering' of quenched steel?", ["Reheating to a moderate temperature to reduce brittleness and improve toughness", "Cooling it further in ice", "Painting it", "Melting it again"], 0,
        "High-strength bolts for bridges are quenched and tempered.",
        "কুয়েঞ্চ-করা ইস্পাতের 'টেম্পারিং' কী?", ["মাঝারি তাপমাত্রায় আবার গরম করে ভঙ্গুরতা কমানো আর দৃঢ়তা-সহনশীলতা বাড়ানো", "বরফে আরও ঠান্ডা করা", "রং করা", "আবার গলানো"],
        "সেতুর উচ্চ-শক্তির বল্টু কুয়েঞ্চ আর টেম্পার করা হয়।"),
    mcq("What is 'normalising' steel?", ["Heating above a critical temperature and cooling in air to refine the grain and make properties uniform", "Painting it normally", "Cooling it in water", "Rolling it cold"], 0,
        "Fine grains improve toughness.",
        "ইস্পাতের 'স্বাভাবিকীকরণ' (নরমালাইজিং) কী?", ["একটা সংকট-তাপমাত্রার উপরে গরম করে বাতাসে ঠান্ডা করা, যাতে দানা সূক্ষ্ম আর ধর্ম সমান হয়", "স্বাভাবিক রং করা", "জলে ঠান্ডা করা", "ঠান্ডা অবস্থায় গড়ানো"],
        "সূক্ষ্ম দানা দৃঢ়তা-সহনশীলতা বাড়ায়।"),
    mcq("What is 'micro-alloying' with niobium or vanadium in bridge steels?", ["Adding tiny amounts that form fine precipitates, raising strength and toughness while keeping weldability", "Adding large amounts of gold", "Removing all carbon", "Adding plastic"], 0,
        "Thermo-mechanical rolling with micro-alloying gives strong, tough plates.",
        "সেতুর ইস্পাতে নিওবিয়াম বা ভ্যানাডিয়ামের 'অণু-সংকরায়ন' কী?", ["খুদে পরিমাণ যোগ করা, যা সূক্ষ্ম অধঃক্ষেপ গড়ে ঝালাইযোগ্যতা রেখে শক্তি আর দৃঢ়তা বাড়ায়", "প্রচুর সোনা যোগ", "সব কার্বন সরানো", "প্লাস্টিক যোগ"],
        "অণু-সংকরায়নসহ তাপ-যান্ত্রিক গড়ানো শক্ত, মজবুত পাত দেয়।"),
    mcq("How does the basic oxygen furnace (BOF) turn pig iron into steel?", ["Blowing pure oxygen through molten iron oxidises excess carbon and impurities", "Adding more coal", "Freezing the iron", "Electrolysing the iron"], 0,
        "Carbon leaves as carbon monoxide; other impurities form slag.",
        "মৌলিক অক্সিজেন-চুল্লি (বিওএফ) কীভাবে কাঁচা লোহাকে ইস্পাতে বদলায়?", ["গলিত লোহার মধ্য দিয়ে বিশুদ্ধ অক্সিজেন বইয়ে বাড়তি কার্বন আর অপদ্রব্য জারিত করে", "আরও কয়লা যোগ করে", "লোহা জমিয়ে", "লোহার তড়িৎবিশ্লেষণ করে"],
        "কার্বন কার্বন মনোক্সাইড হয়ে বেরোয়; অন্য অপদ্রব্য ধাতুমল হয়।"),
    mcq("What is 'green steel' made by hydrogen direct reduction?", ["Iron ore reduced by hydrogen instead of coke, releasing water instead of CO2", "Steel painted green", "Steel made from plants", "Steel with no iron"], 0,
        "With renewable electricity for the hydrogen, emissions fall sharply.",
        "হাইড্রোজেন-প্রত্যক্ষ-বিজারণে তৈরি 'সবুজ ইস্পাত' কী?", ["কোকের বদলে হাইড্রোজেনে বিজারিত লোহার আকরিক, CO2-এর বদলে জল ছাড়ে", "সবুজ রং-করা ইস্পাত", "উদ্ভিদ থেকে তৈরি ইস্পাত", "লোহাহীন ইস্পাত"],
        "হাইড্রোজেনের জন্য নবায়নযোগ্য বিদ্যুৎ হলে নির্গমন তীব্রভাবে কমে।"),
    mcq("What are the main clinker phases in Portland cement?", ["C3S (alite), C2S (belite), C3A (aluminate) and C4AF (ferrite)", "Iron, copper and zinc", "Sand, gravel and water", "Sugar and salt"], 0,
        "Cement chemists use C = CaO, S = SiO2, A = Al2O3, F = Fe2O3.",
        "পোর্টল্যান্ড সিমেন্টের প্রধান ক্লিংকার-দশা কী?", ["C3S (অ্যালাইট), C2S (বেলাইট), C3A (অ্যালুমিনেট) আর C4AF (ফেরাইট)", "লোহা, তামা আর দস্তা", "বালি, খোয়া আর জল", "চিনি আর লবণ"],
        "সিমেন্ট-রসায়নবিদরা C = CaO, S = SiO2, A = Al2O3, F = Fe2O3 লেখেন।"),
    mcq("Which clinker phase gives most of cement's early strength?", ["C3S (alite)", "C2S (belite)", "C4AF (ferrite)", "Gypsum"], 0,
        "C2S hydrates more slowly and adds strength over months.",
        "কোন ক্লিংকার-দশা সিমেন্টের প্রথম দিকের বেশিরভাগ শক্তি দেয়?", ["C3S (অ্যালাইট)", "C2S (বেলাইট)", "C4AF (ফেরাইট)", "জিপসাম"],
        "C2S ধীরে জলযোজিত হয়ে কয়েক মাস ধরে শক্তি যোগ করে।"),
    mcq("Why is gypsum ground into Portland cement?", ["It controls the very fast reaction of C3A, preventing a 'flash set'", "To colour it white", "To make it heavier", "To add strength only"], 0,
        "Without it, cement could stiffen within minutes.",
        "পোর্টল্যান্ড সিমেন্টে জিপসাম গুঁড়িয়ে মেশানো হয় কেন?", ["C3A-র খুব দ্রুত বিক্রিয়া নিয়ন্ত্রণ করে, 'ঝটিতি-জমাট' আটকায়", "সাদা রং দিতে", "ভারী করতে", "শুধু শক্তি যোগ করতে"],
        "এটা না থাকলে সিমেন্ট কয়েক মিনিটে শক্ত হয়ে যেতে পারত।"),
    mcq("Why is low-C3A, sulfate-resisting cement chosen for foundations in sulfate-rich ground?", ["C3A reacts with sulfates to form expansive ettringite, so less C3A means less damage", "C3A makes concrete waterproof", "It is cheaper", "C3A has no effect"], 0,
        "Supplementary materials like GGBS also improve sulfate resistance.",
        "সালফেট-সমৃদ্ধ মাটিতে ভিতের জন্য কম-C3A সালফেট-রোধী সিমেন্ট বাছা হয় কেন?", ["C3A সালফেটের সঙ্গে বিক্রিয়ায় ফুলে-ওঠা এট্রিঞ্জাইট বানায়, তাই কম C3A মানে কম ক্ষতি", "C3A কংক্রিট জলরোধী করে", "সস্তা", "C3A-র প্রভাব নেই"],
        "জিজিবিএস-এর মতো পরিপূরক উপাদানও সালফেট-রোধ বাড়ায়।"),
    mcq("What is a 'pozzolanic reaction'?", ["Silica in materials like fly ash reacts with calcium hydroxide from cement to form extra strength-giving C-S-H", "Cement reacting with sugar", "Steel rusting", "Sand melting"], 0,
        "It makes concrete denser and more durable over time.",
        "'পোজোলানিক বিক্রিয়া' কী?", ["ফ্লাই-অ্যাশের মতো উপাদানের সিলিকা সিমেন্টের ক্যালসিয়াম হাইড্রক্সাইডের সঙ্গে বিক্রিয়া করে বাড়তি শক্তিদায়ী সি-এস-এইচ বানায়", "চিনির সঙ্গে সিমেন্টের বিক্রিয়া", "ইস্পাতে মরচে", "বালি গলা"],
        "সময়ের সঙ্গে কংক্রিট ঘন আর টেকসই করে।"),
    mcq("What is 'silica fume' and why is it used in high-performance bridge concrete?", ["Ultra-fine silica from silicon production that fills tiny gaps and reacts, giving very strong, low-permeability concrete", "Smoke from a fire", "A type of paint", "Crushed glass bottles"], 0,
        "It greatly slows chloride penetration.",
        "'সিলিকা-ধোঁয়া' কী আর উচ্চ-ক্ষমতার সেতু-কংক্রিটে কেন ব্যবহার হয়?", ["সিলিকন-উৎপাদনের অতি-সূক্ষ্ম সিলিকা, যা খুদে ফাঁক ভরে আর বিক্রিয়া করে খুব শক্ত, কম-ভেদ্য কংক্রিট দেয়", "আগুনের ধোঁয়া", "এক রকম রং", "গুঁড়ো কাচের বোতল"],
        "ক্লোরাইড ঢোকা অনেক ধীর করে।"),
    mcq("What are 'geopolymer' cements?", ["Binders made by activating aluminosilicates like fly ash or slag with alkalis, often with much lower CO2 than Portland cement", "Cements made from plastic", "Cements made of rock salt", "Paints for bridges"], 0,
        "They are being trialled for precast bridge elements.",
        "'জিওপলিমার' সিমেন্ট কী?", ["ফ্লাই-অ্যাশ বা ধাতুমলের মতো অ্যালুমিনোসিলিকেটকে ক্ষার দিয়ে সক্রিয় করে বানানো বন্ধক, প্রায়ই পোর্টল্যান্ড সিমেন্টের চেয়ে অনেক কম CO2", "প্লাস্টিকের সিমেন্ট", "পাথুরে নুনের সিমেন্ট", "সেতুর রং"],
        "প্রিকাস্ট সেতু-অংশে পরীক্ষা চলছে।"),
    mcq("What is 'LC3' (limestone calcined clay cement)?", ["A blend replacing much clinker with calcined clay and limestone, cutting CO2 by up to about 40%", "A type of steel", "A brand of paint", "A clay brick"], 0,
        "It was developed with major input from Indian researchers.",
        "'এলসি3' (চুনাপাথর-ভস্মীভূত কাদামাটি সিমেন্ট) কী?", ["মিশ্রণ, যা অনেকটা ক্লিংকারের বদলে ভস্মীভূত কাদামাটি আর চুনাপাথর দেয়, CO2 প্রায় 40% পর্যন্ত কমায়", "এক রকম ইস্পাত", "রঙের ব্র্যান্ড", "কাদামাটির ইট"],
        "ভারতীয় গবেষকদের বড় অবদানে তৈরি।"),
    mcq("Why does mass concrete in a big foundation need its temperature controlled?", ["Hydration heat makes the core much hotter than the surface; the difference can crack it", "Cold concrete never sets", "Heat makes concrete stronger always", "It does not need control"], 0,
        "Limits are often set on peak temperature and core-to-surface difference.",
        "বড় ভিতের বিশাল কংক্রিটের তাপমাত্রা নিয়ন্ত্রণ করতে হয় কেন?", ["জলযোজনের তাপে মাঝখান উপরিতলের চেয়ে অনেক গরম হয়; পার্থক্য ফাটল ধরাতে পারে", "ঠান্ডা কংক্রিট কখনো জমে না", "তাপ সবসময় কংক্রিট শক্ত করে", "নিয়ন্ত্রণ লাগে না"],
        "প্রায়ই সর্বোচ্চ তাপমাত্রা আর মাঝখান-উপরিতলের পার্থক্যে সীমা থাকে।"),
    mcq("What is 'delayed ettringite formation' (DEF)?", ["Expansive crystals forming months or years later in concrete that got too hot while curing, causing cracking", "Fast setting of cement", "Rust on steel", "Paint peeling"], 0,
        "It is why peak curing temperatures are limited to about 65-70°C.",
        "'বিলম্বিত এট্রিঞ্জাইট গঠন' (ডিইএফ) কী?", ["কিউরিংয়ের সময় খুব গরম হওয়া কংক্রিটে কয়েক মাস বা বছর পরে ফুলে-ওঠা কেলাস তৈরি, ফাটল ঘটায়", "সিমেন্টের দ্রুত জমা", "ইস্পাতে মরচে", "রং ওঠা"],
        "তাই কিউরিংয়ের সর্বোচ্চ তাপমাত্রা প্রায় 65-70°C-এ সীমিত।"),
    mcq("What does the Nernst equation describe?", ["How an electrode potential changes with the concentrations of the species involved", "The speed of light", "The strength of steel", "The boiling point of water"], 0,
        "It explains concentration cells that drive pitting and crevice corrosion.",
        "নার্নস্ট সমীকরণ কী বর্ণনা করে?", ["যুক্ত পদার্থের গাঢ়ত্বের সঙ্গে তড়িদ্বার-বিভব কীভাবে বদলায়", "আলোর বেগ", "ইস্পাতের শক্তি", "জলের স্ফুটনাঙ্ক"],
        "গর্ত আর ফাঁক-ক্ষয় চালানো গাঢ়ত্ব-কোষ ব্যাখ্যা করে।"),
    mcq("What is a 'Pourbaix diagram'?", ["A map of potential against pH showing where a metal corrodes, is immune or is passive", "A recipe for paint", "A bridge drawing", "A weather map"], 0,
        "It shows why steel is passive in alkaline concrete but corrodes when pH drops.",
        "'পুরবে-চিত্র' কী?", ["বিভব বনাম pH-এর মানচিত্র, যা দেখায় কোথায় ধাতু ক্ষয়ে যায়, অপ্রভাবিত থাকে বা নিষ্ক্রিয় হয়", "রঙের রেসিপি", "সেতুর নকশা", "আবহাওয়ার মানচিত্র"],
        "দেখায় কেন ক্ষারীয় কংক্রিটে ইস্পাত নিষ্ক্রিয়, কিন্তু pH কমলে ক্ষয়ে যায়।"),
    mcq("Why does the corrosion rate of steel in a marine splash zone tend to be the highest?", ["Constant wetting and drying with plenty of oxygen and salt gives ideal corrosion conditions", "There is no oxygen there", "Splash zones are always dry", "Salt protects steel"], 0,
        "Extra coating thickness or sacrificial steel allowance is used there.",
        "সমুদ্রের ছিটে-অঞ্চলে ইস্পাতের ক্ষয়ের হার সবচেয়ে বেশি হয় কেন?", ["প্রচুর অক্সিজেন আর লবণসহ অবিরাম ভেজা-শুকনো ক্ষয়ের আদর্শ অবস্থা দেয়", "সেখানে অক্সিজেন নেই", "ছিটে-অঞ্চল সবসময় শুকনো", "লবণ ইস্পাত রক্ষা করে"],
        "সেখানে বাড়তি আবরণ-পুরুত্ব বা ক্ষয়ের জন্য বাড়তি ইস্পাত রাখা হয়।"),
    mcq("What is a 'corrosion allowance' in steel pile design?", ["Extra steel thickness added so the pile is still strong enough after expected corrosion over its life", "A discount on steel", "Permission to let piles rust away", "A paint layer only"], 0,
        "It is based on measured corrosion rates for the environment.",
        "ইস্পাতের পাইলের নকশায় 'ক্ষয়-ছাড়' (করোশন অ্যালাওয়েন্স) কী?", ["বাড়তি ইস্পাত-পুরুত্ব, যাতে জীবনভর প্রত্যাশিত ক্ষয়ের পরেও পাইল যথেষ্ট শক্ত থাকে", "ইস্পাতে ছাড়", "পাইলকে মরচে ধরতে দেওয়ার অনুমতি", "শুধু রঙের স্তর"],
        "পরিবেশের মাপা ক্ষয়-হারের ভিত্তিতে ঠিক হয়।"),
    mcq("What does the glass transition temperature (Tg) of a polymer mean for bridge bearings and sealants?", ["Below Tg the polymer becomes hard and brittle; materials are chosen so Tg is below the coldest service temperature", "The polymer melts at Tg", "Tg is the price", "Tg has no effect"], 0,
        "Elastomeric bearings must stay flexible in winter.",
        "পলিমারের কাচ-রূপান্তর তাপমাত্রা (Tg) সেতুর বিয়ারিং আর সিল্যান্টের জন্য কী বোঝায়?", ["Tg-র নিচে পলিমার শক্ত আর ভঙ্গুর হয়; উপাদান বাছা হয় যাতে Tg সবচেয়ে ঠান্ডা কার্যকালের তাপমাত্রার নিচে থাকে", "Tg-তে পলিমার গলে", "Tg হলো দাম", "Tg-র প্রভাব নেই"],
        "স্থিতিস্থাপক বিয়ারিংকে শীতেও নমনীয় থাকতে হয়।"),
    mcq("What does 'cross-link density' control in an epoxy coating?", ["Higher cross-linking gives harder, more chemical-resistant but more brittle coatings", "The coating's colour only", "The coating's smell", "Nothing"], 0,
        "Formulators balance toughness against resistance.",
        "ইপক্সি-আবরণে 'আড়াআড়ি-সংযোগের ঘনত্ব' কী নিয়ন্ত্রণ করে?", ["বেশি আড়াআড়ি-সংযোগে আবরণ শক্ত, বেশি রাসায়নিক-রোধী কিন্তু বেশি ভঙ্গুর", "শুধু আবরণের রং", "আবরণের গন্ধ", "কিছুই না"],
        "প্রস্তুতকারকরা দৃঢ়তা আর প্রতিরোধের ভারসাম্য রাখেন।"),
    mcq("Why does UV light degrade many polymers, such as old cable sheaths?", ["UV photons break polymer bonds, causing chalking, cracking and loss of strength", "UV adds strength", "UV only affects metals", "UV cools polymers"], 0,
        "Carbon black and UV stabilisers protect outdoor plastics.",
        "অতিবেগুনি আলো পুরোনো তারের খাপের মতো অনেক পলিমারের অবনতি ঘটায় কেন?", ["অতিবেগুনি ফোটন পলিমারের বন্ধন ভাঙে, খড়ি-পড়া, ফাটল আর শক্তি-হ্রাস ঘটায়", "অতিবেগুনি শক্তি যোগ করে", "অতিবেগুনি শুধু ধাতুতে প্রভাব ফেলে", "অতিবেগুনি পলিমার ঠান্ডা করে"],
        "কার্বন-ব্ল্যাক আর অতিবেগুনি-স্থিতিকারক বাইরের প্লাস্টিক রক্ষা করে।"),
    mcq("Why is HDPE used to sheath stay cables?", ["It is tough, flexible, waterproof and resists UV when stabilised, protecting the steel strands", "It conducts electricity", "It is heavier than steel", "It dissolves in rain"], 0,
        "Strands inside are often also greased or waxed.",
        "টানা-তারের খাপে এইচডিপিই ব্যবহার হয় কেন?", ["মজবুত, নমনীয়, জলরোধী আর স্থিতিকারকসহ অতিবেগুনি-রোধী, ইস্পাতের তার রক্ষা করে", "বিদ্যুৎ পরিবহন করে", "ইস্পাতের চেয়ে ভারী", "বৃষ্টিতে গলে"],
        "ভেতরের তারে প্রায়ই গ্রিজ বা মোমও থাকে।"),
    mcq("What is the first-order half-life's key property?", ["It is constant - each half-life halves whatever amount remains", "It doubles each time", "It depends on the starting amount", "It is always one day"], 0,
        "Radioactive decay and many breakdown reactions follow it.",
        "প্রথম-ক্রমের অর্ধায়ুর মূল বৈশিষ্ট্য কী?", ["স্থির - প্রতিটা অর্ধায়ু যা বাকি আছে তার অর্ধেক করে", "প্রতিবার দ্বিগুণ হয়", "শুরুর পরিমাণের উপর নির্ভর করে", "সবসময় এক দিন"],
        "তেজস্ক্রিয় ক্ষয় আর অনেক ভাঙন-বিক্রিয়া এটা মানে।"),
    mcq("What does the Arrhenius equation relate?", ["The rate constant of a reaction to temperature and activation energy", "Pressure to volume", "Force to mass", "Current to voltage"], 0,
        "It explains why corrosion and curing speed up in hot climates.",
        "আরেনিয়াস সমীকরণ কীসের সম্পর্ক দেখায়?", ["বিক্রিয়ার হার-ধ্রুবকের সঙ্গে তাপমাত্রা আর সক্রিয়করণ শক্তি", "চাপের সঙ্গে আয়তন", "বলের সঙ্গে ভর", "প্রবাহের সঙ্গে ভোল্টেজ"],
        "গরম জলবায়ুতে ক্ষয় আর জমাট কেন দ্রুত হয়, ব্যাখ্যা করে।"),
    mcq("What is 'maturity' of concrete used for?", ["Estimating in-place strength from its temperature history, to decide when to strip formwork or stress tendons", "Its age in years only", "Its colour", "Its price"], 0,
        "Sensors embedded in the pour record temperature continuously.",
        "কংক্রিটের 'পরিপক্বতা' কীসের জন্য ব্যবহার হয়?", ["তাপমাত্রার ইতিহাস থেকে জায়গায় থাকা শক্তি আন্দাজ করে কখন ছাঁচ খোলা বা তার টানা যাবে ঠিক করা", "শুধু বছরে বয়স", "এর রং", "এর দাম"],
        "ঢালাইয়ে বসানো সেন্সর অবিরাম তাপমাত্রা লেখে।"),
    mcq("What does X-ray fluorescence (XRF) analysis tell a materials engineer?", ["The elemental composition of a sample, such as the alloy content of steel or lead in old paint", "The sample's temperature", "The crystal size only", "The colour of the sample"], 0,
        "Handheld XRF guns give results on site in seconds.",
        "এক্স-রে প্রতিপ্রভা (এক্সআরএফ) বিশ্লেষণ উপাদান-প্রকৌশলীকে কী জানায়?", ["নমুনার মৌলিক গঠন, যেমন ইস্পাতের সংকর-উপাদান বা পুরোনো রঙে সিসা", "নমুনার তাপমাত্রা", "শুধু কেলাসের মাপ", "নমুনার রং"],
        "হাতে-ধরা এক্সআরএফ যন্ত্র নির্মাণস্থলে কয়েক সেকেন্ডে ফল দেয়।"),
    mcq("What does X-ray diffraction (XRD) identify?", ["The crystalline phases present, such as ettringite or rust minerals", "The chemical price", "The sample's mass only", "Temperature"], 0,
        "It helps diagnose sulfate attack and other concrete problems.",
        "এক্স-রে অপবর্তন (এক্সআরডি) কী শনাক্ত করে?", ["উপস্থিত কেলাসীয় দশা, যেমন এট্রিঞ্জাইট বা মরচের খনিজ", "রাসায়নিকের দাম", "শুধু নমুনার ভর", "তাপমাত্রা"],
        "সালফেট-আক্রমণ আর অন্য কংক্রিট-সমস্যা নির্ণয়ে সাহায্য করে।"),
    mcq("What is 'petrography' of concrete?", ["Examining thin slices under a microscope to diagnose causes of deterioration like ASR or freeze-thaw damage", "Drawing pictures of concrete", "Measuring concrete weight", "A type of paint test"], 0,
        "It reads the concrete's history like a geologist reads a rock.",
        "কংক্রিটের 'শিলাবিদ্যা-পরীক্ষা' (পেট্রোগ্রাফি) কী?", ["অণুবীক্ষণে পাতলা টুকরো দেখে এএসআর বা জমা-গলা ক্ষতির মতো অবনতির কারণ নির্ণয়", "কংক্রিটের ছবি আঁকা", "কংক্রিটের ওজন মাপা", "এক রকম রং-পরীক্ষা"],
        "ভূতত্ত্ববিদ যেমন পাথর পড়েন, তেমনি কংক্রিটের ইতিহাস পড়ে।"),
    mcq("What is 'electrochemical chloride extraction' for a contaminated bridge pier?", ["A temporary anode and current draw chloride ions out of the concrete towards the surface", "Washing the pier with water only", "Painting over chlorides", "Adding more salt"], 0,
        "It can restore protection to rebar without breaking out sound concrete.",
        "দূষিত সেতু-স্তম্ভের জন্য 'তড়িৎ-রাসায়নিক ক্লোরাইড-নিষ্কাশন' কী?", ["একটা অস্থায়ী অ্যানোড আর প্রবাহ কংক্রিট থেকে ক্লোরাইড আয়নকে উপরিতলের দিকে টেনে আনে", "শুধু জলে স্তম্ভ ধোয়া", "ক্লোরাইডের উপর রং", "আরও নুন যোগ"],
        "অক্ষত কংক্রিট না ভেঙেই রডের সুরক্ষা ফেরাতে পারে।"),
    mcq("What is 're-alkalisation' of carbonated concrete?", ["Using a temporary current and alkaline electrolyte to raise the pH around the steel again", "Painting the concrete white", "Adding acid", "Heating the concrete"], 0,
        "It restores the passive film on the reinforcement.",
        "কার্বনেশন-হওয়া কংক্রিটের 'পুনঃক্ষারীকরণ' কী?", ["অস্থায়ী প্রবাহ আর ক্ষারীয় তড়িৎবিশ্লেষ্য দিয়ে ইস্পাতের চারপাশে আবার pH বাড়ানো", "কংক্রিট সাদা রং করা", "অ্যাসিড যোগ", "কংক্রিট গরম করা"],
        "রডের নিষ্ক্রিয় স্তর ফিরিয়ে আনে।"),
    mcq("Why are zinc and aluminium thermally sprayed onto some steel bridges?", ["The metal spray gives long-lasting sacrificial and barrier protection, often sealed with a coating", "To make the steel shiny for photos", "To heat the steel", "To weaken the steel"], 0,
        "It is used where very long life between maintenance is needed.",
        "কিছু ইস্পাতের সেতুতে দস্তা আর অ্যালুমিনিয়াম তাপে স্প্রে করা হয় কেন?", ["ধাতব স্প্রে দীর্ঘস্থায়ী আত্মত্যাগী আর বাধা-সুরক্ষা দেয়, প্রায়ই আবরণে সিল করা", "ছবির জন্য ইস্পাত চকচকে করতে", "ইস্পাত গরম করতে", "ইস্পাত দুর্বল করতে"],
        "রক্ষণাবেক্ষণের মধ্যে খুব লম্বা সময় চাইলে ব্যবহার হয়।"),
    mcq("What is 'duplex' protection on steel?", ["Galvanising plus paint, which together last far longer than either alone", "Two layers of rust", "Two bridges side by side", "Painting twice the same day"], 0,
        "The paint protects the zinc; the zinc protects the steel at scratches.",
        "ইস্পাতে 'দ্বৈত' (ডুপ্লেক্স) সুরক্ষা কী?", ["গ্যালভানাইজিং যোগ রং, যা একসঙ্গে যেকোনো একটার চেয়ে অনেক বেশি টেকে", "দুই স্তর মরচে", "পাশাপাশি দুটো সেতু", "একই দিনে দুবার রং"],
        "রং দস্তাকে রক্ষা করে; আঁচড়ে দস্তা ইস্পাতকে রক্ষা করে।"),
    mcq("Why must paint be applied within a dew-point limit on bridges?", ["If the steel surface is near the dew point, invisible moisture condenses and ruins adhesion", "Dew makes paint dry faster", "Paint needs wet steel", "It does not matter"], 0,
        "Steel should be at least 3°C above the dew point.",
        "সেতুতে শিশিরাঙ্কের সীমার মধ্যে রং করতে হয় কেন?", ["ইস্পাতের তল শিশিরাঙ্কের কাছে থাকলে অদৃশ্য আর্দ্রতা জমে আঁকড়ে-ধরা নষ্ট করে", "শিশির রং দ্রুত শুকোয়", "রঙের জন্য ভেজা ইস্পাত লাগে", "কিছু যায় আসে না"],
        "ইস্পাত শিশিরাঙ্কের অন্তত 3°C উপরে থাকা উচিত।"),
    mcq("What does a 'pull-off adhesion test' check on a bridge coating?", ["The force needed to pull a glued dolly off the coating, showing how well it is bonded", "The coating's colour", "The coating's thickness only", "The steel's strength"], 0,
        "Low values point to poor surface preparation or contamination.",
        "সেতুর আবরণে 'টেনে-তোলা আঁকড়ে-ধরা পরীক্ষা' কী যাচাই করে?", ["আঠা দিয়ে লাগানো একটা ডলি আবরণ থেকে টেনে তুলতে লাগা বল, যা দেখায় কতটা ভালো জুড়ে আছে", "আবরণের রং", "শুধু আবরণের পুরুত্ব", "ইস্পাতের শক্তি"],
        "কম মান খারাপ তল-প্রস্তুতি বা দূষণ নির্দেশ করে।"),
    mcq("What is 'soluble salt' testing before painting steel?", ["Measuring salts left on the blasted surface, because they draw moisture through paint and cause blistering", "Testing food salt", "Measuring rainfall", "Testing the paint tin"], 0,
        "Water washing may be needed in coastal sites.",
        "ইস্পাতে রঙের আগে 'দ্রবণীয় লবণ'-এর পরীক্ষা কী?", ["ব্লাস্ট-করা তলে থেকে যাওয়া লবণ মাপা, কারণ এগুলো রঙের মধ্য দিয়ে আর্দ্রতা টেনে ফোস্কা ঘটায়", "খাবারের নুন পরীক্ষা", "বৃষ্টি মাপা", "রঙের টিন পরীক্ষা"],
        "উপকূলের নির্মাণস্থলে জলে ধোয়া লাগতে পারে।"),
    mcq("Why do steelmakers add aluminium to 'kill' molten steel?", ["Aluminium removes dissolved oxygen, preventing gas bubbles and giving a sound, fine-grained steel", "To make the steel lighter", "To colour it", "To raise its melting point"], 0,
        "'Fully killed' steels are specified for bridges.",
        "ইস্পাত-নির্মাতারা গলিত ইস্পাতকে 'শান্ত' করতে অ্যালুমিনিয়াম যোগ করেন কেন?", ["অ্যালুমিনিয়াম দ্রবীভূত অক্সিজেন সরায়, গ্যাসের বুদবুদ আটকে নিখুঁত, সূক্ষ্ম-দানার ইস্পাত দেয়", "ইস্পাত হালকা করতে", "রং দিতে", "গলনাঙ্ক বাড়াতে"],
        "সেতুর জন্য 'পুরো শান্ত' ইস্পাত নির্দিষ্ট করা হয়।"),
    mcq("What is 'lamellar tearing' in thick steel plates?", ["Step-like cracks parallel to the surface caused by through-thickness weld stresses acting on non-metallic inclusions", "Paint peeling in layers", "Rust flakes", "Cuts from a saw"], 0,
        "'Z-grade' steels with good through-thickness ductility resist it.",
        "পুরু ইস্পাতের পাতে 'স্তরীয় ছেঁড়া' কী?", ["অধাতব অন্তর্ভুক্তির উপর পুরুত্ব-বরাবর ঝালাই-পীড়নে উপরিতলের সমান্তরালে সিঁড়ির মতো ফাটল", "স্তরে স্তরে রং ওঠা", "মরচের চাকলা", "করাতের কাটা"],
        "পুরুত্ব-বরাবর ভালো নমনীয়তার 'জেড-গ্রেড' ইস্পাত এটা রোধ করে।"),
    mcq("What is 'embodied carbon' per tonne roughly for virgin steel versus recycled electric-arc steel?", ["Virgin blast-furnace steel emits much more - often around two to three times recycled EAF steel", "They are always identical", "Recycled steel emits far more", "Steel has no embodied carbon"], 0,
        "Specifying recycled content cuts a bridge's footprint.",
        "নতুন ইস্পাত আর পুনর্ব্যবহৃত বৈদ্যুতিক-আর্ক ইস্পাতের টনপ্রতি 'অন্তর্নিহিত কার্বন' মোটামুটি কেমন?", ["নতুন ব্লাস্ট-ফার্নেস ইস্পাত অনেক বেশি ছাড়ে - প্রায়ই পুনর্ব্যবহৃত ইএএফ ইস্পাতের দুই-তিনগুণ", "সবসময় হুবহু সমান", "পুনর্ব্যবহৃত ইস্পাত অনেক বেশি ছাড়ে", "ইস্পাতের অন্তর্নিহিত কার্বন নেই"],
        "পুনর্ব্যবহৃত অংশ নির্দিষ্ট করলে সেতুর পদচিহ্ন কমে।"),
    mcq("Why does concrete slowly absorb some CO2 over its life?", ["Carbonation converts calcium hydroxide back into calcium carbonate, taking CO2 from the air", "Concrete breathes like a plant", "It never absorbs CO2", "Steel absorbs it"], 0,
        "This partly offsets cement emissions, though it can threaten rebar.",
        "জীবনভর কংক্রিট ধীরে কিছু CO2 শোষে কেন?", ["কার্বনেশন ক্যালসিয়াম হাইড্রক্সাইডকে আবার ক্যালসিয়াম কার্বনেটে বদলায়, বাতাস থেকে CO2 নেয়", "উদ্ভিদের মতো কংক্রিট শ্বাস নেয়", "কখনো CO2 শোষে না", "ইস্পাত শোষে"],
        "এটা সিমেন্টের নির্গমন আংশিক পূরণ করে, যদিও রডের জন্য বিপদ হতে পারে।"),
    mcq("What are 'environmental product declarations' (EPDs)?", ["Verified documents stating a product's environmental impacts, such as embodied carbon per tonne", "Advertising leaflets", "Safety data sheets only", "Import licences"], 0,
        "Designers use them to compare materials fairly.",
        "'পরিবেশগত পণ্য-ঘোষণা' (ইপিডি) কী?", ["যাচাই-করা নথি, যা পণ্যের পরিবেশগত প্রভাব, যেমন টনপ্রতি অন্তর্নিহিত কার্বন, জানায়", "বিজ্ঞাপনের প্রচারপত্র", "শুধু নিরাপত্তা-তথ্যপত্র", "আমদানি-লাইসেন্স"],
        "নকশাকাররা ন্যায্যভাবে উপাদান তুলনায় এগুলো ব্যবহার করেন।"),
    mcq("Why are VOC limits set for bridge coatings?", ["Volatile organic compounds contribute to smog and harm health, so low-VOC products are required", "VOCs make paint stronger", "VOCs are minerals", "There are no limits"], 0,
        "High-solids and water-borne coatings meet the limits.",
        "সেতুর আবরণে ভিওসি-সীমা বাঁধা হয় কেন?", ["উদ্বায়ী জৈব যৌগ ধোঁয়াশা বাড়ায় আর স্বাস্থ্যের ক্ষতি করে, তাই কম-ভিওসি পণ্য বাধ্যতামূলক", "ভিওসি রং শক্ত করে", "ভিওসি খনিজ", "কোনো সীমা নেই"],
        "উচ্চ-কঠিন আর জল-বাহিত আবরণ সীমা মানে।"),
    mcq("What does 'ppm' mean in water quality testing?", ["Parts per million - about milligrams per litre in water", "Pieces per minute", "Pounds per metre", "Percentage per month"], 0,
        "Concrete mixing water often has limits like 500 ppm chloride.",
        "জলের মান পরীক্ষায় 'পিপিএম' মানে কী?", ["প্রতি দশ লক্ষে অংশ - জলে মোটামুটি লিটারপ্রতি মিলিগ্রাম", "মিনিটপ্রতি টুকরো", "মিটারপ্রতি পাউন্ড", "মাসপ্রতি শতাংশ"],
        "কংক্রিট মেশানোর জলে প্রায়ই 500 পিপিএম ক্লোরাইডের মতো সীমা থাকে।"),
    mcq("Why can sugar contamination in mixing water be a problem for concrete?", ["Sugar strongly retards cement hydration and can stop concrete setting", "Sugar makes concrete sweet and stronger", "It has no effect", "It speeds setting to seconds"], 0,
        "Even small amounts can delay setting dramatically.",
        "মেশানোর জলে চিনির দূষণ কংক্রিটের জন্য সমস্যা কেন?", ["চিনি সিমেন্টের জলযোজন তীব্রভাবে ধীর করে, কংক্রিট জমা থামিয়েও দিতে পারে", "চিনি কংক্রিট মিষ্টি আর শক্ত করে", "প্রভাব নেই", "সেকেন্ডে জমায়"],
        "অল্প পরিমাণও জমা নাটকীয়ভাবে পিছিয়ে দিতে পারে।"),
    mcq("What is the role of a 'chain extender' or 'curing agent' in polyurethane bridge-deck waterproofing?", ["It reacts with the prepolymer to build long, cross-linked chains, giving a tough elastic membrane", "It colours the membrane", "It dissolves the membrane", "It has no role"], 0,
        "Correct mixing ratios are vital for full cure.",
        "পলিইউরিথেনের সেতু-পাটাতন জলরোধীকরণে 'শৃঙ্খল-বর্ধক' বা 'জমাট-কারক'-এর ভূমিকা কী?", ["প্রি-পলিমারের সঙ্গে বিক্রিয়া করে লম্বা, আড়াআড়ি-যুক্ত শৃঙ্খল গড়ে, মজবুত স্থিতিস্থাপক পর্দা দেয়", "পর্দা রঙিন করে", "পর্দা গলায়", "কোনো ভূমিকা নেই"],
        "পুরো জমাটের জন্য ঠিক মেশানোর অনুপাত জরুরি।"),
    mcq("What is the danger of mixing two-part epoxy in the wrong ratio?", ["It may never fully cure, leaving a soft, weak, chemically unstable coating", "It becomes stronger", "It changes colour only", "Nothing"], 0,
        "Always follow the manufacturer's ratio and pot life.",
        "দুই-অংশের ইপক্সি ভুল অনুপাতে মেশালে বিপদ কী?", ["কখনো পুরো জমবে না, নরম, দুর্বল, রাসায়নিকভাবে অস্থির আবরণ থাকবে", "আরও শক্ত হয়", "শুধু রং বদলায়", "কিছুই না"],
        "সবসময় প্রস্তুতকারকের অনুপাত আর ব্যবহার-সময় মানো।"),
    mcq("What is 'pot life' of a two-part coating?", ["The time after mixing during which it can still be applied properly", "The time it lasts on the bridge", "The life of the tin", "How long the pot is guaranteed"], 0,
        "Hot weather shortens pot life.",
        "দুই-অংশের আবরণের 'পাত্র-আয়ু' কী?", ["মেশানোর পরে যে সময়ের মধ্যে এখনো ঠিকঠাক লাগানো যায়", "সেতুতে কতদিন টেকে", "টিনের আয়ু", "পাত্রের কতদিনের নিশ্চয়তা"],
        "গরম আবহাওয়ায় পাত্র-আয়ু কমে।"),
    mcq("What is 'chemical admixture compatibility' testing?", ["Checking that superplasticisers, retarders and air-entrainers work properly together with the chosen cement", "Testing whether chemicals are friendly", "Mixing paint colours", "Weighing bags"], 0,
        "Some combinations cause rapid slump loss or poor air content.",
        "'রাসায়নিক সংযোজকের সামঞ্জস্য' পরীক্ষা কী?", ["বাছা সিমেন্টের সঙ্গে সুপারপ্লাস্টিসাইজার, মন্দক আর বায়ু-আবদ্ধকারী একসঙ্গে ঠিক কাজ করে কিনা যাচাই", "রাসায়নিক বন্ধুত্বপূর্ণ কিনা পরীক্ষা", "রঙ মেশানো", "বস্তা ওজন"],
        "কিছু মিশ্রণে দ্রুত গড়ানো-ক্ষমতা হারায় বা বায়ুর পরিমাণ কম হয়।"),
    mcq("Why do concrete technologists measure the 'water-binder ratio' rather than just water-cement?", ["Modern mixes include fly ash, slag and silica fume that also react, so all binders count", "Binders are not used", "Water does not matter", "It is a translation error"], 0,
        "Lower ratios generally mean stronger, more durable concrete.",
        "কংক্রিট-প্রযুক্তিবিদরা শুধু জল-সিমেন্ট নয়, 'জল-বন্ধক অনুপাত' মাপেন কেন?", ["আধুনিক মিশ্রণে ফ্লাই-অ্যাশ, ধাতুমল আর সিলিকা-ধোঁয়াও বিক্রিয়া করে, তাই সব বন্ধক গোনা হয়", "বন্ধক ব্যবহার হয় না", "জল গুরুত্বহীন", "অনুবাদের ভুল"],
        "কম অনুপাতে সাধারণত শক্ত, টেকসই কংক্রিট।"),
    mcq("What is 'ultra-high-performance concrete' (UHPC)?", ["Concrete with very fine particles, low water and steel fibres, reaching compressive strengths above about 150 N/mm²", "Ordinary concrete painted grey", "Concrete with no cement", "Foam concrete"], 0,
        "It allows thin, light, very durable bridge elements.",
        "'অতি-উচ্চ-ক্ষমতার কংক্রিট' (ইউএইচপিসি) কী?", ["খুব সূক্ষ্ম কণা, কম জল আর ইস্পাত-তন্তুর কংক্রিট, যার সংনমন-শক্তি প্রায় 150 N/mm²-এর বেশি", "ধূসর রং-করা সাধারণ কংক্রিট", "সিমেন্টহীন কংক্রিট", "ফেনা-কংক্রিট"],
        "পাতলা, হালকা, খুব টেকসই সেতু-অংশ সম্ভব করে।"),
    mcq("Why is the 'alkali content' of cement limited when aggregates may be reactive?", ["High alkali drives alkali-silica reaction, forming an expansive gel that cracks concrete", "Alkali makes concrete weak in fire only", "Alkali has no effect", "Low alkali causes ASR"], 0,
        "Low-alkali cement or pozzolans help control ASR.",
        "খোয়া প্রতিক্রিয়াশীল হতে পারলে সিমেন্টের 'ক্ষার-পরিমাণ' সীমিত করা হয় কেন?", ["বেশি ক্ষার ক্ষার-সিলিকা বিক্রিয়া চালায়, ফুলে-ওঠা জেল কংক্রিট ফাটায়", "ক্ষার শুধু আগুনে কংক্রিট দুর্বল করে", "ক্ষারের প্রভাব নেই", "কম ক্ষারে এএসআর হয়"],
        "কম-ক্ষারের সিমেন্ট বা পোজোলান এএসআর নিয়ন্ত্রণে সাহায্য করে।"),
    mcq("Why are stainless steel bars sometimes used in marine bridge decks despite costing several times more?", ["They resist chloride corrosion for the bridge's life, saving far more in future repairs and closures", "They are lighter than concrete", "They need no concrete cover at all", "They are cheaper"], 0,
        "Whole-life cost, not purchase price, justifies them in aggressive environments.",
        "কয়েকগুণ দামি হলেও সমুদ্রতীরের সেতু-পাটাতনে কখনো স্টেইনলেস স্টিলের রড ব্যবহার হয় কেন?", ["সেতুর জীবনভর ক্লোরাইড-ক্ষয় রোধ করে, ভবিষ্যৎ মেরামত আর বন্ধে অনেক বেশি বাঁচায়", "কংক্রিটের চেয়ে হালকা", "কংক্রিট-আবরণ মোটেই লাগে না", "সস্তা"],
        "ক্ষয়কারী পরিবেশে কেনার দাম নয়, পূর্ণ-জীবন খরচই এর যৌক্তিকতা।"),
    mcq("What is the 'incipient anode' (ring anode) problem after patch-repairing chloride-damaged concrete?", ["Steel just outside the new alkaline patch can start corroding faster, because the patch steel becomes cathodic", "The patch turns blue", "The patch melts", "There is no such problem"], 0,
        "Small zinc anodes embedded at the patch edge prevent it.",
        "ক্লোরাইডে ক্ষতিগ্রস্ত কংক্রিটে তালি-মেরামতের পরে 'আসন্ন অ্যানোড' (বলয়-অ্যানোড) সমস্যা কী?", ["নতুন ক্ষারীয় তালির ঠিক বাইরের ইস্পাত দ্রুত ক্ষয়ে যেতে পারে, কারণ তালির ইস্পাত ক্যাথোডিক হয়ে যায়", "তালি নীল হয়ে যায়", "তালি গলে যায়", "এমন সমস্যা নেই"],
        "তালির কিনারায় বসানো ছোট দস্তা-অ্যানোড এটা ঠেকায়।"),
) if q is not None)
