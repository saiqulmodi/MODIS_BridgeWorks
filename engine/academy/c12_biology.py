"""Class 12 - Biology (Chief Engineer): biodiversity indices, logistic population growth, noise
dose, biochemical oxygen demand, the Q10 rule, enzyme kinetics, epidemiology and screening tests,
bioaccumulation, biotechnology, bio-deterioration of bridges, self-healing concrete and the
ecological management of large infrastructure projects."""
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


def _f(r, *alts):
    o = []
    for v in (r, *alts):
        v = round(v, 2)
        if v not in o and 0 <= v <= 1:
            o.append(v)
    k = 0.1
    while len(o) < 4:
        v = round(r + k if r + k <= 1 else r - k, 2)
        if v not in o:
            o.append(v)
        k += 0.1
    return [f"{v:.2f}" for v in o[:4]]


def simpson(counts, site_en, site_bn):
    n = sum(counts)
    d = round(1 - sum(c * (c - 1) for c in counts) / (n * (n - 1)), 2)
    o = _f(d, 1 - d, len(counts) / 10, d / 2)
    return mcq(f"A survey of {site_en} finds species counts {', '.join(map(str, counts))}. What is Simpson's diversity index, 1 - Σn(n-1) ÷ N(N-1)?", o, 0,
               f"N = {n}; Σn(n-1) = {sum(c * (c - 1) for c in counts)}; D = 1 - {sum(c * (c - 1) for c in counts)} ÷ {n * (n - 1)} = {d:.2f}. Closer to 1 means more diverse.",
               f"{site_bn} জরিপে প্রজাতির সংখ্যা {', '.join(map(str, counts))}। সিম্পসনের বৈচিত্র্য-সূচক 1 - Σn(n-1) ÷ N(N-1) কত?", o,
               f"N = {n}; Σn(n-1) = {sum(c * (c - 1) for c in counts)}; D = 1 - {sum(c * (c - 1) for c in counts)} ÷ {n * (n - 1)} = {d:.2f}। 1-এর যত কাছে, বৈচিত্র্য তত বেশি।")


def logistic(r, n, k, what_en, what_bn):
    g = _c(r * n * (1 - n / k))
    return _n(f"A {what_en} population grows logistically with r = {r:g} per year and carrying capacity K = {k:,}. At N = {n:,}, what is the growth rate dN/dt per year?",
              f"একটা {what_bn}-জনসংখ্যা লজিস্টিকভাবে বাড়ে, r = বছরে {r:g} আর ধারণক্ষমতা K = {k:,}। N = {n:,} হলে বৃদ্ধির হার dN/dt বছরে কত?", g,
              f"dN/dt = rN(1 - N/K) = {r:g} x {n:,} x (1 - {n:,}/{k:,}) = {g:g}. Growth slows as N nears K.",
              f"dN/dt = rN(1 - N/K) = {r:g} x {n:,} x (1 - {n:,}/{k:,}) = {g:g}। N, K-এর কাছে গেলে বৃদ্ধি কমে।",
              (_c(r * n), _c(r * k), _c(r * (k - n))))


def noise(level):
    t = _c(8 / 2 ** ((level - 85) / 3))
    o = [f"{t:g} h"] + [f"{v:g} h" for v in dict.fromkeys((8, _c(t * 2), _c(t * 4), _c(t / 2), _c(8 - (level - 85) / 3))) if v != t and v > 0][:3]
    ob = [f"{t:g} ঘণ্টা"] + [x.replace(" h", " ঘণ্টা") for x in o[1:]]
    return mcq(f"The noise limit is 85 dB(A) for 8 hours, and the allowed time halves for every 3 dB extra. How long may a worker stay unprotected beside a {level} dB(A) pile hammer?", o, 0,
               f"{level} - 85 = {level - 85} dB = {_c((level - 85) / 3):g} halvings, so 8 ÷ 2^{_c((level - 85) / 3):g} = {t:g} h.",
               f"শব্দের সীমা 8 ঘণ্টার জন্য 85 dB(A), আর প্রতি বাড়তি 3 dB-তে অনুমোদিত সময় অর্ধেক হয়। {level} dB(A) পাইল-হাতুড়ির পাশে একজন কর্মী সুরক্ষা ছাড়া কতক্ষণ থাকতে পারেন?", ob,
               f"{level} - 85 = {level - 85} dB = {_c((level - 85) / 3):g}বার অর্ধেক, তাই 8 ÷ 2^{_c((level - 85) / 3):g} = {t:g} ঘণ্টা।")


def bod(d1, d2, p):
    b = _c((d1 - d2) / p)
    return _n(f"A river sample near a site outfall is diluted to {p:g} of its strength. Dissolved oxygen falls from {d1} to {d2} mg/L over 5 days. What is the BOD₅ of the river water?",
              f"নির্মাণস্থলের নিকাশি-মুখের কাছের নদী-নমুনা {p:g} শক্তিতে লঘু করা হল। 5 দিনে দ্রবীভূত অক্সিজেন {d1} থেকে {d2} mg/L-এ নামে। নদী-জলের BOD₅ কত?", b,
              f"BOD = (D₁ - D₂) ÷ P = ({d1} - {d2}) ÷ {p:g} = {b:g} mg/L. Higher BOD means more organic pollution.",
              f"BOD = (D₁ - D₂) ÷ P = ({d1} - {d2}) ÷ {p:g} = {b:g} mg/L। বেশি BOD মানে বেশি জৈব দূষণ।",
              (_c(d1 - d2), _c((d1 - d2) * p), _c(d1 / p)), " mg/L")


def q10(r1, q, dt, what_en, what_bn):
    r2 = _c(r1 * q ** (dt / 10))
    return _n(f"{what_en} has a rate of {r1} at one temperature and Q₁₀ = {q}. What is the rate {dt}°C warmer?",
              f"{what_bn}-এর হার এক তাপমাত্রায় {r1} আর Q₁₀ = {q}। {dt}°C বেশি গরমে হার কত?", r2,
              f"Rate x Q₁₀^(ΔT/10) = {r1} x {q}^{_c(dt / 10):g} = {r2:g}. Biological rates roughly double for each 10°C.",
              f"হার x Q₁₀^(ΔT/10) = {r1} x {q}^{_c(dt / 10):g} = {r2:g}। জৈব হার প্রতি 10°C-এ মোটামুটি দ্বিগুণ হয়।",
              (_c(r1 * q * dt / 10 + r1 if r1 * q * dt / 10 + r1 != r2 else r2 + 5), _c(r1 + q * dt), _c(r1 * q)))


def mm(vmax, km, s):
    v = _c(vmax * s / (km + s))
    return _n(f"A cement-degrading bacterial enzyme has Vmax = {vmax} units and Km = {km} mM. What is its rate at a substrate concentration of {s} mM?",
              f"সিমেন্ট-ক্ষয়কারী একটা ব্যাকটেরিয়া-উৎসেচকের Vmax = {vmax} একক আর Km = {km} mM। {s} mM ভিত্তিবস্তু-ঘনত্বে এর হার কত?", v,
              f"v = Vmax x S ÷ (Km + S) = {vmax} x {s} ÷ ({km} + {s}) = {v:g}. At S = Km the rate is half of Vmax.",
              f"v = Vmax x S ÷ (Km + S) = {vmax} x {s} ÷ ({km} + {s}) = {v:g}। S = Km হলে হার Vmax-এর অর্ধেক।",
              (_c(vmax / 2) if _c(vmax / 2) != v else vmax, _c(vmax * s / km), _c(vmax * km / (km + s))))


def rrisk(a, n1, b, n2, what_en, what_bn):
    rr = _c((a / n1) / (b / n2))
    return _n(f"In a study of {what_en}, {a} of {n1:,} exposed workers and {b} of {n2:,} unexposed workers developed the disease. What is the relative risk?",
              f"{what_bn} নিয়ে একটা গবেষণায় উন্মুক্ত {n1:,} জন কর্মীর {a} জন আর অনুন্মুক্ত {n2:,} জনের {b} জন রোগে আক্রান্ত হলেন। আপেক্ষিক ঝুঁকি কত?", rr,
              f"RR = ({a}/{n1:,}) ÷ ({b}/{n2:,}) = {rr:g}. RR > 1 means exposure raises the risk.",
              f"RR = ({a}/{n1:,}) ÷ ({b}/{n2:,}) = {rr:g}। RR > 1 মানে সংস্পর্শে ঝুঁকি বাড়ে।",
              (_c(a / b), _c(a - b), _c(rr / 2)))


def sens(tp, fn, fp, tn):
    s = _c(100 * tp / (tp + fn))
    return _n(f"A site screening test for hearing loss finds {tp} true positives, {fn} false negatives, {fp} false positives and {tn} true negatives. What is its sensitivity?",
              f"শ্রবণ-ক্ষতির একটা পরীক্ষায় {tp}টি সত্য-ধনাত্মক, {fn}টি মিথ্যা-ঋণাত্মক, {fp}টি মিথ্যা-ধনাত্মক আর {tn}টি সত্য-ঋণাত্মক মেলে। এর সংবেদনশীলতা কত?", s,
              f"Sensitivity = TP ÷ (TP + FN) = {tp} ÷ {tp + fn} = {s:g}% - the share of real cases the test catches.",
              f"সংবেদনশীলতা = TP ÷ (TP + FN) = {tp} ÷ {tp + fn} = {s:g}% - আসল রোগীদের যত অংশ পরীক্ষা ধরে।",
              (_c(100 * tn / (tn + fp)), _c(100 * tp / (tp + fp)), _c(100 * (tp + tn) / (tp + fn + fp + tn))), "%")


def bcf(cw, f, what_en, what_bn):
    c = _c(cw * f)
    return _n(f"River water below an old paint-stripping site holds {cw:g} µg/L of a pollutant. If {what_en} concentrate it with a bioconcentration factor of {f:,}, what is the level in their tissue (µg/kg)?",
              f"পুরোনো রং-তোলার জায়গার নিচের নদী-জলে একটা দূষকের {cw:g} µg/L আছে। {what_bn} যদি 1:{f:,} জৈব-ঘনীভবন গুণকে এটা জমায়, তাদের দেহকলায় মাত্রা কত (µg/kg)?", c,
              f"Tissue = water x BCF = {cw:g} x {f:,} = {c:,}. Predators eating them concentrate it further.",
              f"দেহকলা = জল x গুণক = {cw:g} x {f:,} = {c:,}। এদের খাওয়া শিকারিরা আরও বেশি জমায়।",
              (_c(cw + f), _c(f / cw) if _c(f / cw) != c else c + 7, _c(cw * f / 10)))


ITEMS = (
    simpson((10, 10, 10, 10), "a riverbank meadow", "নদীতীরের একটা তৃণভূমির"),
    simpson((30, 5, 5), "a sprayed verge", "ওষুধ-ছেটানো রাস্তার ধারের"),
    simpson((8, 6, 4, 2), "a restored wetland", "পুনরুদ্ধার-করা একটা জলাভূমির"),
    simpson((20, 10, 5, 5), "a pier-side mudflat", "স্তম্ভের পাশের কাদা-চরের"),
    simpson((12, 12, 6), "a mangrove plot", "একটা ম্যানগ্রোভ-খণ্ডের"),
    logistic(0.4, 500, 1000, "otter", "ভোঁদড়"), logistic(0.5, 200, 1000, "heron", "বক"),
    logistic(0.3, 800, 1000, "turtle", "কচ্ছপ"), logistic(0.6, 2000, 5000, "mudskipper", "মাডস্কিপার-মাছ"),
    noise(88), noise(91), noise(94), noise(97), noise(100),
    bod(8, 6, 0.02), bod(9, 4, 0.05), bod(8.5, 5.5, 0.1), bod(7.5, 3.5, 0.04),
    q10(10, 2, 10, "A rot fungus decaying a timber pile", "কাঠের খুঁটি-পচানো একটা ছত্রাক"),
    q10(6, 2, 20, "Bacterial growth in a damp bearing shelf", "স্যাঁতসেঁতে বিয়ারিং-তাকের ব্যাকটেরিয়া-বৃদ্ধি"),
    q10(5, 3, 10, "A marine borer's feeding", "একটা সামুদ্রিক ছিদ্রকারীর খাওয়া"),
    q10(12, 2, 30, "Sulphate-reducing bacteria in pier mud", "স্তম্ভের কাদার সালফেট-বিজারক ব্যাকটেরিয়া"),
    mm(100, 4, 4), mm(60, 2, 6), mm(90, 5, 10), mm(80, 3, 1),
    rrisk(30, 1000, 10, 1000, "silica dust and lung disease", "সিলিকা-ধুলো আর ফুসফুসের রোগ"),
    rrisk(24, 400, 12, 800, "night shifts and injuries", "রাতের পালা আর আঘাত"),
    rrisk(18, 600, 6, 600, "vibrating tools and hand damage", "কম্পন-যন্ত্র আর হাতের ক্ষতি"),
    sens(45, 5, 10, 140), sens(72, 8, 20, 100), sens(36, 12, 6, 146),
    bcf(0.5, 2000, "oysters on the piers", "স্তম্ভের ঝিনুকেরা"), bcf(0.2, 5000, "mussels", "শামুক-ঝিনুকেরা"), bcf(1.5, 400, "river prawns", "নদীর চিংড়িরা"),
    mcq("What does a low Simpson's diversity index in a habitat beside a new road suggest?", ["One or two species dominate, often a sign of disturbance", "The habitat is extremely rich", "No species live there", "The survey was too large"], 0,
        "Engineers use such indices to measure the before-and-after impact of a project.",
        "নতুন রাস্তার পাশের আবাসস্থলে সিম্পসনের বৈচিত্র্য-সূচক কম হলে কী বোঝায়?", ["এক-দুটো প্রজাতি প্রাধান্য পাচ্ছে, প্রায়ই বিঘ্নের লক্ষণ", "আবাসস্থল খুবই সমৃদ্ধ", "সেখানে কোনো প্রজাতি থাকে না", "জরিপ খুব বড় ছিল"],
        "প্রকল্পের আগে-পরের প্রভাব মাপতে প্রকৌশলীরা এমন সূচক ব্যবহার করেন।"),
    mcq("What is the 'carrying capacity' (K) of a habitat?", ["The largest population the habitat can support long term", "The weight a bridge can carry", "The number of species present", "The birth rate"], 0,
        "Food, space and shelter set the limit.",
        "আবাসস্থলের 'ধারণক্ষমতা' (K) কী?", ["আবাসস্থল দীর্ঘমেয়াদে যত বড় জনসংখ্যা টিকিয়ে রাখতে পারে", "সেতু কত ওজন বইতে পারে", "উপস্থিত প্রজাতির সংখ্যা", "জন্মহার"],
        "খাদ্য, জায়গা আর আশ্রয় সীমা ঠিক করে।"),
    mcq("At what population size is logistic growth fastest?", ["At half the carrying capacity, K/2", "At zero", "At K", "At twice K"], 0,
        "There N is large but crowding has not yet slowed growth much.",
        "জনসংখ্যা কত হলে লজিস্টিক বৃদ্ধি সবচেয়ে দ্রুত?", ["ধারণক্ষমতার অর্ধেকে, K/2", "শূন্যে", "K-তে", "K-এর দ্বিগুণে"],
        "সেখানে N বড় কিন্তু ভিড় এখনো বৃদ্ধি বেশি কমায়নি।"),
    mcq("What does 'habitat fragmentation' by a new highway embankment mean for wildlife?", ["Breaking a large habitat into small isolated patches, for example by roads and embankments", "Planting new forests", "Animals changing colour", "A type of rock"], 0,
        "Small patches support fewer species and smaller, vulnerable populations.",
        "নতুন মহাসড়ক-বাঁধের কারণে 'আবাসস্থল খণ্ডীকরণ' বন্যপ্রাণীর জন্য কী বোঝায়?", ["বড় আবাসস্থলকে ছোট বিচ্ছিন্ন টুকরোয় ভাঙা, যেমন রাস্তা আর বাঁধ দিয়ে", "নতুন বন লাগানো", "প্রাণীর রং বদল", "এক রকম পাথর"],
        "ছোট টুকরো কম প্রজাতি আর ছোট, ঝুঁকিপূর্ণ জনসংখ্যা টেকায়।"),
    mcq("Why might long viaducts be chosen over embankments across a wetland, despite the higher cost?", ["They keep water flow and animal movement connected beneath the road", "They are always cheaper", "Embankments cannot be built on land", "Viaducts need no foundations"], 0,
        "Embankments act like dams and barriers.",
        "বেশি খরচ সত্ত্বেও জলাভূমি পেরোতে বাঁধের বদলে লম্বা ভায়াডাক্ট বাছা হতে পারে কেন?", ["রাস্তার নিচে জলের প্রবাহ আর প্রাণীর চলাচল জোড়া রাখে", "এরা সবসময় সস্তা", "জমিতে বাঁধ বানানো যায় না", "ভায়াডাক্টে ভিত লাগে না"],
        "বাঁধ জলাধার আর বাধার মতো কাজ করে।"),
    mcq("What is the 'mitigation hierarchy' in environmental planning?", ["Avoid harm first, then minimise it, then restore, and offset only what remains", "Offset first, then build anything", "Ignore small impacts", "Plant trees after damage only"], 0,
        "Avoiding damage is almost always cheaper and better than repairing it.",
        "পরিবেশ-পরিকল্পনায় 'প্রশমন-ক্রম' কী?", ["আগে ক্ষতি এড়াও, তারপর কমাও, তারপর পুনরুদ্ধার করো, আর শুধু বাকিটা পূরণ করো", "আগে পূরণ, তারপর যা খুশি বানাও", "ছোট প্রভাব উপেক্ষা করো", "শুধু ক্ষতির পরে গাছ লাগাও"],
        "ক্ষতি এড়ানো প্রায় সবসময় মেরামতের চেয়ে সস্তা আর ভালো।"),
    mcq("Why are piling works in rivers often restricted during fish spawning seasons?", ["Underwater noise and silt can kill eggs and drive fish away from breeding grounds", "Fish damage the piles", "Water is too cold", "Piles cannot be driven in summer"], 0,
        "Work windows are agreed with ecologists in advance.",
        "নদীতে পাইলের কাজ মাছের ডিম পাড়ার মরসুমে প্রায়ই সীমিত করা হয় কেন?", ["জলের নিচের শব্দ আর পলি ডিম মারতে পারে আর প্রজনন-ক্ষেত্র থেকে মাছ তাড়ায়", "মাছ পাইল নষ্ট করে", "জল খুব ঠান্ডা", "গ্রীষ্মে পাইল বসানো যায় না"],
        "কাজের সময়সীমা আগেই বাস্তুবিদদের সঙ্গে ঠিক করা হয়।"),
    mcq("What is a 'bubble curtain' used for during marine piling?", ["A ring of rising air bubbles around the pile that absorbs underwater sound to protect dolphins and fish", "Cleaning the pile", "Cooling the hammer", "Lifting the pile"], 0,
        "It can cut underwater noise substantially.",
        "সমুদ্রে পাইল বসানোর সময় 'বুদবুদ-পর্দা' কীসের জন্য ব্যবহার হয়?", ["পাইলের চারপাশে উঠতি বাতাসের বুদবুদের বলয়, যা জলের নিচের শব্দ শুষে ডলফিন আর মাছ রক্ষা করে", "পাইল পরিষ্কার", "হাতুড়ি ঠান্ডা করা", "পাইল তোলা"],
        "জলের নিচের শব্দ অনেকটাই কমাতে পারে।"),
    mcq("Why can bright lighting on a coastal bridge harm sea turtles?", ["Hatchlings use the brighter sea horizon to find the water, and artificial light leads them inland", "Turtles eat light bulbs", "Light heats the sand too much", "It has no effect"], 0,
        "Shielded, low, amber lighting reduces the problem.",
        "উপকূলের সেতুর উজ্জ্বল আলো সামুদ্রিক কচ্ছপের ক্ষতি করতে পারে কেন?", ["বাচ্চারা জল খুঁজতে সমুদ্রের উজ্জ্বল দিগন্ত ব্যবহার করে, আর কৃত্রিম আলো তাদের ডাঙার দিকে নিয়ে যায়", "কচ্ছপ বাল্ব খায়", "আলো বালি খুব গরম করে", "কোনো প্রভাব নেই"],
        "ঢাকা, নিচু, হলদে-কমলা আলো সমস্যা কমায়।"),
    mcq("Why are the cables of some cable-stayed bridges fitted with markers in bird migration areas?", ["To make the thin cables visible so birds avoid colliding with them", "To measure wind", "To hold lamps", "To scare away tourists"], 0,
        "Collision risk is assessed in the environmental study.",
        "পাখির পরিযান-এলাকায় কিছু কেবল-স্টেড সেতুর তারে চিহ্ন লাগানো হয় কেন?", ["সরু তার দৃশ্যমান করতে, যাতে পাখি ধাক্কা এড়ায়", "বাতাস মাপতে", "বাতি ধরতে", "পর্যটক তাড়াতে"],
        "পরিবেশ-গবেষণায় ধাক্কার ঝুঁকি মূল্যায়ন করা হয়।"),
    mcq("What is 'biochemical oxygen demand' (BOD)?", ["The oxygen used by microbes to break down organic matter in water over a set time", "The oxygen needed by fish to swim", "The oxygen in air", "The oxygen in concrete"], 0,
        "Clean rivers have a BOD below about 3 mg/L.",
        "'জৈব-রাসায়নিক অক্সিজেন চাহিদা' (BOD) কী?", ["নির্দিষ্ট সময়ে জলের জৈব পদার্থ ভাঙতে জীবাণুরা যত অক্সিজেন ব্যবহার করে", "মাছের সাঁতারে লাগা অক্সিজেন", "বাতাসের অক্সিজেন", "কংক্রিটের অক্সিজেন"],
        "পরিষ্কার নদীর BOD প্রায় 3 mg/L-এর নিচে।"),
    mcq("Why must site welfare cabins never discharge untreated sewage into a river?", ["The high BOD strips dissolved oxygen from the water, suffocating fish and spreading disease", "It makes the river warmer", "It is only a smell problem", "It strengthens the river bed"], 0,
        "Septic tanks or tankers are used instead.",
        "নির্মাণস্থলের কর্মী-কেবিন কখনো অপরিশোধিত বর্জ্য নদীতে ফেলবে না কেন?", ["বেশি BOD জলের দ্রবীভূত অক্সিজেন কেড়ে নেয়, মাছের দম আটকায় আর রোগ ছড়ায়", "নদী গরম হয়", "শুধু গন্ধের সমস্যা", "নদীর তলা শক্ত হয়"],
        "বদলে সেপটিক ট্যাঙ্ক বা ট্যাঙ্কার ব্যবহার হয়।"),
    mcq("Why does fresh concrete washout harm aquatic life if it reaches a stream?", ["It is strongly alkaline (pH around 12), burning gills and killing invertebrates", "It is acidic", "It feeds fish", "It has no effect once diluted at all"], 0,
        "Washout is collected in lined pits and neutralised.",
        "তাজা কংক্রিট-ধোয়া জল নালায় পৌঁছলে জলজ প্রাণীর ক্ষতি করে কেন?", ["এটা খুব ক্ষারীয় (pH প্রায় 12), কানকো পোড়ায় আর অমেরুদণ্ডীদের মারে", "এটা আম্লিক", "মাছকে খাওয়ায়", "লঘু হলেই কোনো প্রভাব নেই"],
        "ধোয়া জল আস্তরণ-দেওয়া গর্তে জমিয়ে নিরপেক্ষ করা হয়।"),
    mcq("What does the Q₁₀ value describe?", ["How many times a biological rate increases for a 10°C rise in temperature", "The quality of water", "The tenth enzyme", "The ten-year growth of trees"], 0,
        "For most enzymes it is about 2-3 within their working range.",
        "Q₁₀ মান কী বর্ণনা করে?", ["তাপমাত্রা 10°C বাড়লে জৈব হার কতগুণ বাড়ে", "জলের গুণমান", "দশম উৎসেচক", "গাছের দশ বছরের বৃদ্ধি"],
        "বেশিরভাগ উৎসেচকের কাজের পরিসরে এটা প্রায় 2-3।"),
    mcq("Why does timber decay faster in warm, humid coastal regions?", ["Fungi and insects are more active at higher temperature and moisture, following the Q₁₀ effect", "Salt makes wood grow", "Cold air carries fungi", "Timber never decays at the coast"], 0,
        "Preservative treatment and good drainage slow it down.",
        "উষ্ণ, আর্দ্র উপকূলে কাঠ দ্রুত পচে কেন?", ["বেশি তাপমাত্রা আর আর্দ্রতায় ছত্রাক আর পোকা বেশি সক্রিয়, Q₁₀ প্রভাব মেনে", "লবণে কাঠ বাড়ে", "ঠান্ডা বাতাস ছত্রাক বয়", "উপকূলে কাঠ কখনো পচে না"],
        "সংরক্ষক-প্রক্রিয়া আর ভালো নিকাশি এটা ধীর করে।"),
    mcq("In enzyme kinetics, what does Km (the Michaelis constant) represent?", ["The substrate concentration at which the rate is half its maximum", "The maximum rate", "The enzyme's mass", "The temperature limit"], 0,
        "A low Km means the enzyme grabs its substrate easily.",
        "উৎসেচক-গতিবিদ্যায় Km (মিকেলিস ধ্রুবক) কী বোঝায়?", ["যে ভিত্তিবস্তু-ঘনত্বে হার সর্বোচ্চের অর্ধেক", "সর্বোচ্চ হার", "উৎসেচকের ভর", "তাপমাত্রার সীমা"],
        "কম Km মানে উৎসেচক ভিত্তিবস্তু সহজে ধরে।"),
    mcq("Why does adding more substrate eventually stop increasing an enzyme's rate?", ["All the active sites become occupied, so the enzyme is saturated at Vmax", "The substrate becomes poisonous", "The enzyme melts", "Rate always increases forever"], 0,
        "Only adding more enzyme can then speed things up.",
        "আরও ভিত্তিবস্তু যোগ করলে শেষ পর্যন্ত উৎসেচকের হার আর বাড়ে না কেন?", ["সব সক্রিয় স্থান দখল হয়ে যায়, তাই উৎসেচক Vmax-এ সম্পৃক্ত", "ভিত্তিবস্তু বিষাক্ত হয়ে যায়", "উৎসেচক গলে যায়", "হার চিরকাল বাড়ে"],
        "তখন শুধু বেশি উৎসেচক যোগ করলেই গতি বাড়ে।"),
    mcq("What is 'relative risk' in occupational health?", ["The risk of disease in exposed workers divided by the risk in unexposed workers", "The risk to relatives", "The risk of a bridge collapsing", "The total number of sick workers"], 0,
        "RR = 3 means exposed workers are three times as likely to fall ill.",
        "পেশাগত স্বাস্থ্যে 'আপেক্ষিক ঝুঁকি' কী?", ["উন্মুক্ত কর্মীদের রোগের ঝুঁকিকে অনুন্মুক্ত কর্মীদের ঝুঁকি দিয়ে ভাগ", "আত্মীয়দের ঝুঁকি", "সেতু ভেঙে পড়ার ঝুঁকি", "অসুস্থ কর্মীর মোট সংখ্যা"],
        "RR = 3 মানে উন্মুক্ত কর্মীদের অসুস্থ হওয়ার সম্ভাবনা তিনগুণ।"),
    mcq("Why does a link between an exposure and a disease not prove that one causes the other?", ["Other factors, such as smoking or age, may explain the link - correlation is not causation", "Links are always causes", "Diseases have no causes", "Statistics are never useful"], 0,
        "Good studies control for such confounding factors.",
        "সংস্পর্শ আর রোগের মধ্যে যোগ থাকলেই একটা অন্যটার কারণ প্রমাণ হয় না কেন?", ["ধূমপান বা বয়সের মতো অন্য কারণ যোগটা ব্যাখ্যা করতে পারে - সহসম্পর্ক কারণ নয়", "যোগ সবসময় কারণ", "রোগের কারণ নেই", "পরিসংখ্যান কখনো কাজের নয়"],
        "ভালো গবেষণা এমন বিভ্রান্তিকর কারণ নিয়ন্ত্রণ করে।"),
    mcq("What is the 'specificity' of a screening test?", ["The share of healthy people correctly identified as negative", "The share of sick people found", "The test's price", "How fast it works"], 0,
        "Low specificity gives many false alarms.",
        "একটা পরীক্ষার 'নির্দিষ্টতা' কী?", ["সুস্থ মানুষের যত অংশ ঠিকভাবে ঋণাত্মক ধরা পড়ে", "অসুস্থদের যত অংশ ধরা পড়ে", "পরীক্ষার দাম", "কত দ্রুত কাজ করে"],
        "কম নির্দিষ্টতায় অনেক মিথ্যা সতর্কতা আসে।"),
    mcq("Why is a highly sensitive test chosen for screening workers for an early disease?", ["It misses very few real cases, and positives can be confirmed by a more specific test", "It is always cheaper", "It never gives false alarms", "Sensitivity does not matter"], 0,
        "Screening then confirmation is the usual two-step approach.",
        "প্রাথমিক রোগে কর্মীদের পরীক্ষায় খুব সংবেদনশীল পরীক্ষা বাছা হয় কেন?", ["খুব কম আসল রোগী বাদ পড়ে, আর ধনাত্মকদের আরও নির্দিষ্ট পরীক্ষায় নিশ্চিত করা যায়", "সবসময় সস্তা", "কখনো মিথ্যা সতর্কতা দেয় না", "সংবেদনশীলতার গুরুত্ব নেই"],
        "আগে বাছাই, তারপর নিশ্চিতকরণ - সাধারণ দুই-ধাপ পদ্ধতি।"),
    mcq("What is 'biomagnification'?", ["The rise in concentration of a persistent pollutant at each higher level of a food chain", "Using a microscope", "Animals growing larger", "Bacteria multiplying"], 0,
        "Top predators like otters and eagles carry the highest loads.",
        "'জৈব-বিবর্ধন' কী?", ["খাদ্যশৃঙ্খলের প্রতিটা উঁচু স্তরে স্থায়ী দূষকের ঘনত্ব বাড়া", "অণুবীক্ষণ ব্যবহার", "প্রাণী বড় হওয়া", "ব্যাকটেরিয়া বাড়া"],
        "ভোঁদড় আর ঈগলের মতো শীর্ষ শিকারিরা সবচেয়ে বেশি বয়।"),
    mcq("Why is old lead-based bridge paint removed inside sealed enclosures?", ["Lead dust is toxic, accumulates in the body and food chain, and harms the nervous system", "Lead paint is very valuable", "To keep the paint dry", "To make the work faster"], 0,
        "Workers also have their blood lead levels monitored.",
        "সেতুর পুরোনো সীসা-ভিত্তিক রং বন্ধ ঘেরাটোপের মধ্যে তোলা হয় কেন?", ["সীসার ধুলো বিষাক্ত, দেহ আর খাদ্যশৃঙ্খলে জমে আর স্নায়ুতন্ত্রের ক্ষতি করে", "সীসার রং খুব দামি", "রং শুকনো রাখতে", "কাজ দ্রুত করতে"],
        "কর্মীদের রক্তে সীসার মাত্রাও নজরে রাখা হয়।"),
    mcq("What is 'biological monitoring' of workers?", ["Measuring a chemical or its breakdown products in blood or urine to check actual exposure", "Watching birds on site", "Checking workers' attendance", "Testing soil for worms"], 0,
        "It shows what really entered the body, not just what was in the air.",
        "কর্মীদের 'জৈব নজরদারি' কী?", ["আসল সংস্পর্শ যাচাইয়ে রক্ত বা প্রস্রাবে রাসায়নিক বা তার ভাঙা অংশ মাপা", "নির্মাণস্থলে পাখি দেখা", "কর্মীদের হাজিরা যাচাই", "মাটিতে কেঁচো পরীক্ষা"],
        "বাতাসে কী ছিল শুধু তা নয়, দেহে আসলে কী ঢুকেছে তা দেখায়।"),
    mcq("What is the 'dose-response' relationship in toxicology?", ["The link between how much of a substance is received and the size of its effect", "The price of medicine", "The speed of a reaction", "A reply to a letter"], 0,
        "'The dose makes the poison.'",
        "বিষবিদ্যায় 'মাত্রা-সাড়া' সম্পর্ক কী?", ["কতটা পদার্থ পাওয়া গেল আর তার প্রভাব কত বড়, তার সম্পর্ক", "ওষুধের দাম", "বিক্রিয়ার গতি", "চিঠির উত্তর"],
        "'মাত্রাই বিষ তৈরি করে।'"),
    mcq("What is a 'latency period' for diseases such as mesothelioma from asbestos?", ["The long gap, often decades, between exposure and the appearance of disease", "The time to cure it", "A short holiday", "The time for a test result"], 0,
        "This is why old exposures still cause illness today.",
        "অ্যাসবেস্টস থেকে মেসোথেলিওমার মতো রোগের 'সুপ্তিকাল' কী?", ["সংস্পর্শ আর রোগ দেখা দেওয়ার মধ্যে দীর্ঘ ফাঁক, প্রায়ই কয়েক দশক", "সারানোর সময়", "ছোট ছুটি", "পরীক্ষার ফলের সময়"],
        "এই কারণেই পুরোনো সংস্পর্শ আজও অসুখ ঘটায়।"),
    mcq("Why must asbestos be surveyed for before demolishing an old bridge or building?", ["Disturbing it releases fibres that can cause fatal lung diseases years later", "It is valuable to sell", "It explodes", "It is always harmless"], 0,
        "Licensed specialists remove it first.",
        "পুরোনো সেতু বা বাড়ি ভাঙার আগে অ্যাসবেস্টস জরিপ করতে হয় কেন?", ["নাড়া দিলে আঁশ বেরোয় যা বছর পরে প্রাণঘাতী ফুসফুসের রোগ ঘটাতে পারে", "বিক্রি করলে দামি", "এটা বিস্ফোরিত হয়", "সবসময় নিরীহ"],
        "লাইসেন্সপ্রাপ্ত বিশেষজ্ঞরা আগে এটা সরান।"),
    mcq("How does 'self-healing' bacterial concrete work?", ["Dormant bacterial spores in the mix wake when water enters a crack and produce limestone that seals it", "Bacteria eat the concrete", "Concrete grows new steel", "Workers spray glue daily"], 0,
        "Bacillus species and calcium lactate food are typical ingredients.",
        "'নিজে-সারা' ব্যাকটেরিয়া-কংক্রিট কীভাবে কাজ করে?", ["মিশ্রণের সুপ্ত ব্যাকটেরিয়া-রেণু ফাটলে জল ঢুকলে জেগে চুনাপাথর তৈরি করে ফাটল বন্ধ করে", "ব্যাকটেরিয়া কংক্রিট খায়", "কংক্রিটে নতুন ইস্পাত গজায়", "কর্মীরা রোজ আঠা ছেটান"],
        "ব্যাসিলাস প্রজাতি আর খাবার হিসেবে ক্যালসিয়াম ল্যাকটেট সাধারণ উপাদান।"),
    mcq("Why must self-healing bacteria survive the very alkaline conditions inside concrete?", ["Concrete's pH is about 12-13, which kills most microbes, so only hardy spore-formers can be used", "Concrete is acidic", "Bacteria prefer pH 7 only and never survive", "pH does not matter"], 0,
        "Their spores can lie dormant for many years.",
        "নিজে-সারা ব্যাকটেরিয়াকে কংক্রিটের ভেতরের খুব ক্ষারীয় অবস্থায় টিকতে হয় কেন?", ["কংক্রিটের pH প্রায় 12-13, যা বেশিরভাগ জীবাণু মারে, তাই শুধু কঠিন রেণু-গঠনকারীরাই চলে", "কংক্রিট আম্লিক", "ব্যাকটেরিয়া শুধু pH 7 পছন্দ করে আর কখনো টেকে না", "pH-এর গুরুত্ব নেই"],
        "এদের রেণু বহু বছর সুপ্ত থাকতে পারে।"),
    mcq("What is 'microbially influenced corrosion' (MIC) of steel piles?", ["Corrosion speeded up by bacteria, such as sulphate-reducing bacteria in low-oxygen mud", "Rust caused by sunlight", "Corrosion from paint", "Steel dissolving in air"], 0,
        "It can cause unexpectedly fast, deep pitting near the mud line.",
        "ইস্পাতের পাইলের 'জীবাণু-প্রভাবিত ক্ষয়' (MIC) কী?", ["ব্যাকটেরিয়ায়, যেমন কম-অক্সিজেনের কাদায় সালফেট-বিজারক ব্যাকটেরিয়ায়, দ্রুত হওয়া ক্ষয়", "সূর্যালোকে মরচে", "রং থেকে ক্ষয়", "বাতাসে ইস্পাত গলে যাওয়া"],
        "কাদার রেখার কাছে অপ্রত্যাশিত দ্রুত, গভীর গর্ত তৈরি করতে পারে।"),
    mcq("What is 'accelerated low water corrosion' (ALWC) on harbour piles?", ["Rapid, bacteria-driven corrosion of steel just below the low-tide level", "Corrosion only above the high tide", "Slow corrosion inside concrete", "A type of paint"], 0,
        "Bright orange deposits over black, pitted steel are a warning sign.",
        "বন্দরের পাইলে 'ত্বরান্বিত নিম্ন-জল ক্ষয়' (ALWC) কী?", ["ভাটার নিচু জলের ঠিক নিচে ইস্পাতের দ্রুত, ব্যাকটেরিয়া-চালিত ক্ষয়", "শুধু জোয়ারের উপরে ক্ষয়", "কংক্রিটের ভেতরে ধীর ক্ষয়", "এক রকম রং"],
        "কালো, গর্তওয়ালা ইস্পাতের উপরে উজ্জ্বল কমলা জমা সতর্কতার লক্ষণ।"),
    mcq("What is 'biofouling' on marine bridge piers?", ["The growth of barnacles, mussels and seaweed that adds weight and wave load to the piers", "Bird droppings on the deck", "Mould in offices", "Polluting the water"], 0,
        "Engineers allow for the extra thickness in wave-force calculations.",
        "সমুদ্রের সেতু-স্তম্ভে 'জৈব-আবরণ' (বায়োফাউলিং) কী?", ["বার্নাকল, ঝিনুক আর সামুদ্রিক শৈবালের বৃদ্ধি, যা স্তম্ভে ওজন আর ঢেউয়ের বোঝা বাড়ায়", "পাটাতনে পাখির বিষ্ঠা", "অফিসে ছাতা", "জল দূষণ"],
        "ঢেউয়ের বল হিসাবে প্রকৌশলীরা বাড়তি পুরুত্ব ধরেন।"),
    mcq("What are 'shipworms', and why do they matter for timber piles?", ["Wood-boring marine molluscs that tunnel inside timber, hollowing it out unseen", "Worms that live on ships' decks", "A type of fish", "Harmless sea snails"], 0,
        "Timber in seawater needs treatment or wrapping against them.",
        "'শিপওয়ার্ম' কী, আর কাঠের খুঁটিতে এর গুরুত্ব কেন?", ["কাঠ-ছিদ্রকারী সামুদ্রিক কম্বোজ, যা কাঠের ভেতরে সুড়ঙ্গ কেটে অদৃশ্যে ফাঁপা করে দেয়", "জাহাজের পাটাতনে থাকা কৃমি", "এক রকম মাছ", "নিরীহ সামুদ্রিক শামুক"],
        "সমুদ্র-জলের কাঠে এদের বিরুদ্ধে প্রক্রিয়া বা মোড়ক লাগে।"),
    mcq("Why are termite barriers used under bridge-side buildings and timber structures in India?", ["Subterranean termites eat cellulose in timber and can travel through cracks to reach it", "Termites strengthen wood", "Termites only live in deserts", "They help concrete set"], 0,
        "Physical mesh barriers or treated soil block their route.",
        "ভারতে সেতুর পাশের বাড়ি আর কাঠের কাঠামোর নিচে উই-প্রতিরোধক বাধা ব্যবহার হয় কেন?", ["মাটির নিচের উই কাঠের সেলুলোজ খায় আর ফাটল দিয়ে পৌঁছে যেতে পারে", "উই কাঠ শক্ত করে", "উই শুধু মরুভূমিতে থাকে", "এরা কংক্রিট জমাতে সাহায্য করে"],
        "ভৌত জাল-বাধা বা প্রক্রিয়াজাত মাটি তাদের পথ আটকায়।"),
    mcq("What is 'bioremediation' of contaminated land?", ["Using microbes or plants to break down or remove pollutants from soil or water", "Digging up soil and dumping it in the sea", "Paving over contamination", "Burning the land"], 0,
        "It is often cheaper and gentler than excavation.",
        "দূষিত জমির 'জৈব-প্রতিকার' কী?", ["মাটি বা জল থেকে দূষক ভাঙতে বা সরাতে জীবাণু বা উদ্ভিদ ব্যবহার", "মাটি খুঁড়ে সমুদ্রে ফেলা", "দূষণের উপর পাকা করা", "জমি পোড়ানো"],
        "প্রায়ই খোঁড়ার চেয়ে সস্তা আর কোমল।"),
    mcq("What is 'phytoremediation'?", ["Using plants that absorb heavy metals or break down pollutants to clean soil", "Taking photographs of pollution", "Spraying weedkiller", "Removing all plants from a site"], 0,
        "Sunflowers and some grasses take up metals; the plants are then harvested.",
        "'উদ্ভিদ-প্রতিকার' কী?", ["ভারী ধাতু শোষণকারী বা দূষক-ভাঙা উদ্ভিদ দিয়ে মাটি পরিষ্কার", "দূষণের ছবি তোলা", "আগাছানাশক ছেটানো", "জায়গা থেকে সব গাছ সরানো"],
        "সূর্যমুখী আর কিছু ঘাস ধাতু টানে; তারপর গাছ কেটে সরানো হয়।"),
    mcq("How does a 'constructed wetland' treat road run-off from a bridge?", ["Plants, gravel and microbes slow the water, trap sediment and break down oil and metals", "It heats the water", "It pumps water uphill", "It adds chemicals only"], 0,
        "It also creates habitat.",
        "একটা 'নির্মিত জলাভূমি' সেতুর রাস্তা-ধোয়া জল কীভাবে পরিশোধন করে?", ["উদ্ভিদ, নুড়ি আর জীবাণু জল ধীর করে, পলি আটকায় আর তেল ও ধাতু ভাঙে", "জল গরম করে", "জল উপরে পাম্প করে", "শুধু রাসায়নিক যোগ করে"],
        "এটা আবাসস্থলও তৈরি করে।"),
    mcq("What is 'recombinant DNA' technology?", ["Joining DNA from different sources, such as putting a human gene into bacteria to make insulin", "Copying a whole animal", "Reading DNA aloud", "Mixing blood types"], 0,
        "Restriction enzymes cut DNA and ligase joins it.",
        "'পুনঃসংযোজিত ডিএনএ' প্রযুক্তি কী?", ["আলাদা উৎসের ডিএনএ জোড়া, যেমন ইনসুলিন বানাতে মানুষের জিন ব্যাকটেরিয়ায় বসানো", "গোটা প্রাণী নকল করা", "ডিএনএ জোরে পড়া", "রক্তের গ্রুপ মেশানো"],
        "সীমাবদ্ধকারী উৎসেচক ডিএনএ কাটে আর লাইগেজ জোড়ে।"),
    mcq("What is CRISPR-Cas9?", ["A precise gene-editing tool that cuts DNA at a chosen sequence", "A crisp snack", "A type of microscope", "A vaccine"], 0,
        "It was adapted from a bacterial defence system against viruses.",
        "ক্রিসপার-ক্যাস9 কী?", ["নির্বাচিত ক্রমে ডিএনএ কাটা নিখুঁত জিন-সম্পাদনার যন্ত্র", "এক রকম মুচমুচে খাবার", "এক রকম অণুবীক্ষণ", "একটা টিকা"],
        "ভাইরাসের বিরুদ্ধে ব্যাকটেরিয়ার প্রতিরক্ষা-ব্যবস্থা থেকে নেওয়া।"),
    mcq("What is 'environmental DNA' (eDNA) sampling?", ["Detecting species from traces of DNA they leave in water or soil, without catching them", "Testing workers' DNA", "Adding DNA to rivers", "Building with DNA"], 0,
        "One water sample can reveal rare fish or otters near a bridge site.",
        "'পরিবেশগত ডিএনএ' (ইডিএনএ) নমুনা কী?", ["প্রাণী না ধরে জল বা মাটিতে রেখে যাওয়া ডিএনএ-চিহ্ন থেকে প্রজাতি শনাক্ত", "কর্মীদের ডিএনএ পরীক্ষা", "নদীতে ডিএনএ যোগ", "ডিএনএ দিয়ে নির্মাণ"],
        "একটা জল-নমুনাই সেতু-স্থলের কাছে বিরল মাছ বা ভোঁদড় প্রকাশ করতে পারে।"),
    mcq("What is the role of 'stem cells' in medicine?", ["Unspecialised cells that can develop into many cell types, used to repair damaged tissue", "Cells from plant stems only", "Dead cells", "Cells that only make bone"], 0,
        "Bone marrow transplants rely on blood stem cells.",
        "চিকিৎসায় 'স্টেম কোষ'-এর ভূমিকা কী?", ["অবিশেষায়িত কোষ যা অনেক রকম কোষে পরিণত হতে পারে, ক্ষতিগ্রস্ত কলা সারাতে ব্যবহৃত", "শুধু উদ্ভিদের কাণ্ডের কোষ", "মৃত কোষ", "শুধু হাড় তৈরির কোষ"],
        "অস্থিমজ্জা প্রতিস্থাপন রক্তের স্টেম কোষের উপর নির্ভর করে।"),
    mcq("What happens in transcription?", ["A gene's DNA sequence is copied into messenger RNA in the nucleus", "Proteins are digested", "Cells divide", "DNA is destroyed"], 0,
        "Translation at the ribosome then builds the protein.",
        "প্রতিলিপিকরণে (ট্রান্সক্রিপশন) কী ঘটে?", ["নিউক্লিয়াসে একটা জিনের ডিএনএ-ক্রম বার্তাবাহী আরএনএ-তে নকল হয়", "প্রোটিন হজম হয়", "কোষ বিভাজিত হয়", "ডিএনএ ধ্বংস হয়"],
        "তারপর রাইবোজোমে অনুবাদ প্রোটিন গড়ে।"),
    mcq("What is a 'codon'?", ["A sequence of three mRNA bases that codes for one amino acid", "A whole gene", "A type of cell", "A protein shape"], 0,
        "There are 64 codons for 20 amino acids plus stop signals.",
        "'কোডন' কী?", ["তিনটি এমআরএনএ-ক্ষারকের ক্রম যা একটা অ্যামিনো অ্যাসিডের সংকেত দেয়", "গোটা জিন", "এক রকম কোষ", "প্রোটিনের আকার"],
        "20টি অ্যামিনো অ্যাসিড আর থামার সংকেতের জন্য 64টি কোডন।"),
    mcq("Why are night-shift workers on bridge projects at higher risk of accidents in the early morning hours?", ["The body clock's circadian low around 3-5 am reduces alertness and reaction speed", "It is always darker at midnight", "Machines run slower at night", "There is no extra risk"], 0,
        "Shift planning places critical tasks away from this window.",
        "সেতু-প্রকল্পে রাতের পালার কর্মীদের ভোরের দিকে দুর্ঘটনার ঝুঁকি বেশি কেন?", ["রাত 3-5টার দিকে দেহ-ঘড়ির দৈনিক ছন্দের নিম্নবিন্দু সতর্কতা আর প্রতিক্রিয়ার গতি কমায়", "মাঝরাতে সবসময় বেশি অন্ধকার", "রাতে যন্ত্র ধীরে চলে", "বাড়তি ঝুঁকি নেই"],
        "পালা-পরিকল্পনা জরুরি কাজ এই সময় থেকে দূরে রাখে।"),
    mcq("What does the hormone melatonin do?", ["It signals night-time to the body and promotes sleep, released in darkness", "It digests food", "It builds muscle", "It raises blood sugar"], 0,
        "Bright light at night suppresses it, disturbing sleep.",
        "মেলাটোনিন হরমোন কী করে?", ["দেহকে রাতের সংকেত দেয় আর ঘুম আনে, অন্ধকারে নিঃসৃত হয়", "খাবার হজম করে", "পেশি গড়ে", "রক্তে শর্করা বাড়ায়"],
        "রাতে উজ্জ্বল আলো একে দমায়, ঘুম বিঘ্নিত করে।"),
    mcq("Why is 'whole-body vibration' from driving heavy plant a health concern?", ["Long exposure can damage the lower back and spine", "It improves posture", "It cures back pain", "It only affects the plant"], 0,
        "Good seats, smooth haul roads and time limits reduce it.",
        "ভারী যন্ত্র চালানোর 'পুরো-দেহ কম্পন' স্বাস্থ্যের চিন্তা কেন?", ["দীর্ঘ সংস্পর্শে কোমর আর মেরুদণ্ডের ক্ষতি হতে পারে", "অঙ্গভঙ্গি ভালো করে", "পিঠের ব্যথা সারায়", "শুধু যন্ত্রকে প্রভাবিত করে"],
        "ভালো আসন, মসৃণ রাস্তা আর সময়সীমা এটা কমায়।"),
    mcq("What is the 'wet-bulb globe temperature' (WBGT) used for on construction sites?", ["Setting safe work-rest cycles in hot conditions by combining temperature, humidity, sun and wind", "Measuring concrete temperature", "Weather forecasting only", "Checking water supply"], 0,
        "Above certain WBGT values, heavy work is limited.",
        "নির্মাণস্থলে 'আর্দ্র-বাল্ব গ্লোব তাপমাত্রা' (WBGT) কীসের জন্য ব্যবহার হয়?", ["তাপমাত্রা, আর্দ্রতা, রোদ আর বাতাস মিলিয়ে গরমে নিরাপদ কাজ-বিশ্রাম চক্র ঠিক করা", "কংক্রিটের তাপমাত্রা মাপা", "শুধু আবহাওয়ার পূর্বাভাস", "জলসরবরাহ যাচাই"],
        "নির্দিষ্ট WBGT মানের উপরে ভারী কাজ সীমিত।"),
    mcq("Why is humid heat more dangerous to workers than dry heat at the same temperature?", ["Sweat cannot evaporate well in humid air, so the body loses its main cooling method", "Humid air has less oxygen", "Dry heat is always hotter", "Humidity cools the body"], 0,
        "Coastal and monsoon sites need extra heat precautions.",
        "একই তাপমাত্রায় শুকনো গরমের চেয়ে আর্দ্র গরম কর্মীদের জন্য বেশি বিপজ্জনক কেন?", ["আর্দ্র বাতাসে ঘাম ভালোভাবে বাষ্প হয় না, তাই দেহ ঠান্ডা হওয়ার প্রধান উপায় হারায়", "আর্দ্র বাতাসে অক্সিজেন কম", "শুকনো গরম সবসময় বেশি গরম", "আর্দ্রতা দেহ ঠান্ডা করে"],
        "উপকূল আর বর্ষার নির্মাণস্থলে বাড়তি তাপ-সতর্কতা লাগে।"),
    mcq("Why is dengue a particular risk on construction sites in the monsoon?", ["Water collecting in tyres, drums and formwork breeds Aedes mosquitoes", "Concrete attracts mosquitoes", "Dengue spreads through dust", "Rain kills all mosquitoes"], 0,
        "Removing standing water every week breaks the breeding cycle.",
        "বর্ষায় নির্মাণস্থলে ডেঙ্গু বিশেষ ঝুঁকি কেন?", ["টায়ার, ড্রাম আর ছাঁচে জমা জলে এডিস মশা জন্মায়", "কংক্রিট মশা টানে", "ডেঙ্গু ধুলো দিয়ে ছড়ায়", "বৃষ্টি সব মশা মারে"],
        "প্রতি সপ্তাহে জমা জল সরালে প্রজনন-চক্র ভাঙে।"),
    mcq("What is 'ecological succession' on a disturbed site beside a new bridge?", ["The gradual change of plant and animal communities over years, from pioneer species to a stable community", "Building in stages", "Animals queueing", "Trees cut in order"], 0,
        "Engineers can speed it with native seeding and planting.",
        "নতুন সেতুর পাশের বিঘ্নিত জমিতে 'বাস্তুতান্ত্রিক অনুক্রম' কী?", ["বছর ধরে উদ্ভিদ আর প্রাণী-গোষ্ঠীর ধীরে বদল, পথিকৃৎ প্রজাতি থেকে স্থিতিশীল গোষ্ঠী পর্যন্ত", "ধাপে ধাপে নির্মাণ", "প্রাণীর সারি", "ক্রমে গাছ কাটা"],
        "দেশি বীজ আর চারা লাগিয়ে প্রকৌশলীরা এটা দ্রুত করতে পারেন।"),
    mcq("Why should landscaping around a new bridge use native plant species?", ["They suit local soil and climate, need less care and support local insects and birds", "They are always bigger", "Foreign plants never grow", "Native plants are free of all pests"], 0,
        "Some exotic plants can become invasive.",
        "নতুন সেতুর চারপাশের বাগান-সজ্জায় দেশি উদ্ভিদ ব্যবহার করা উচিত কেন?", ["স্থানীয় মাটি আর জলবায়ুতে মানায়, কম যত্ন লাগে আর স্থানীয় পোকা ও পাখিকে সাহায্য করে", "সবসময় বড় হয়", "বিদেশি গাছ কখনো জন্মায় না", "দেশি গাছে কোনো কীট নেই"],
        "কিছু বিদেশি গাছ আগ্রাসী হয়ে উঠতে পারে।"),
    mcq("What are 'ecosystem services'?", ["Benefits people get from nature, such as flood control, clean water and pollination", "Repair services for zoos", "Cleaning companies", "Government offices"], 0,
        "Mangroves, for example, reduce storm surge on coastal bridges.",
        "'বাস্তুতন্ত্র-পরিষেবা' কী?", ["প্রকৃতি থেকে মানুষ যে উপকার পায়, যেমন বন্যা-নিয়ন্ত্রণ, পরিষ্কার জল আর পরাগমিলন", "চিড়িয়াখানার মেরামত-পরিষেবা", "পরিষ্কারক সংস্থা", "সরকারি অফিস"],
        "যেমন ম্যানগ্রোভ উপকূলের সেতুতে ঝড়ের জলোচ্ছ্বাস কমায়।"),
    mcq("Why do environmental surveys for a bridge often cover a full year?", ["Many species are present or active only in certain seasons, such as migrants and breeding animals", "Surveyors need a holiday", "Plants never change", "One day is always enough"], 0,
        "Missing a season can miss a protected species.",
        "সেতুর পরিবেশ-জরিপ প্রায়ই পুরো এক বছর ধরে চলে কেন?", ["অনেক প্রজাতি শুধু নির্দিষ্ট ঋতুতে থাকে বা সক্রিয়, যেমন পরিযায়ী আর প্রজননকারী প্রাণী", "জরিপকারীদের ছুটি লাগে", "উদ্ভিদ কখনো বদলায় না", "এক দিনই সবসময় যথেষ্ট"],
        "একটা ঋতু বাদ পড়লে সংরক্ষিত প্রজাতি বাদ পড়তে পারে।"),
    mcq("What does 'sample size' affect in an ecological or health study?", ["The precision of the results - larger samples give narrower confidence intervals", "Nothing at all", "Only the cost of paper", "The species' colour"], 0,
        "Too small a sample can miss real effects.",
        "বাস্তু বা স্বাস্থ্য-গবেষণায় 'নমুনার আকার' কী প্রভাবিত করে?", ["ফলের নির্ভুলতা - বড় নমুনা সরু আস্থা-ব্যবধান দেয়", "কিছুই না", "শুধু কাগজের দাম", "প্রজাতির রং"],
        "খুব ছোট নমুনা আসল প্রভাব হারাতে পারে।"),
    mcq("What is a 'control group' in a field trial of a new erosion-control planting?", ["Plots left untreated, so changes caused by the planting can be told apart from natural changes", "The group in charge", "The best-performing plots only", "Plots that are fenced off from scientists"], 0,
        "Without controls, weather alone might explain the results.",
        "নতুন ভূমিক্ষয়-রোধী রোপণের মাঠ-পরীক্ষায় 'নিয়ন্ত্রণ-গোষ্ঠী' কী?", ["অপরিবর্তিত রাখা খণ্ড, যাতে রোপণের কারণে বদল প্রাকৃতিক বদল থেকে আলাদা করা যায়", "দায়িত্বে থাকা দল", "শুধু সবচেয়ে ভালো খণ্ড", "বিজ্ঞানীদের থেকে বেড়া-ঘেরা খণ্ড"],
        "নিয়ন্ত্রণ ছাড়া শুধু আবহাওয়াই ফল ব্যাখ্যা করতে পারে।"),
    mcq("What is 'antimicrobial resistance' and why does it concern public health planners?", ["Microbes evolving to survive drugs, making infections harder to treat", "Microbes becoming friendly", "Drugs becoming cheaper", "A new vaccine"], 0,
        "Overuse of antibiotics speeds it up.",
        "'জীবাণুনাশক-প্রতিরোধ' কী আর জনস্বাস্থ্য-পরিকল্পকরা কেন চিন্তিত?", ["জীবাণুরা ওষুধে টিকে থাকতে বিবর্তিত হয়, সংক্রমণের চিকিৎসা কঠিন করে", "জীবাণু বন্ধুত্বপূর্ণ হয়", "ওষুধ সস্তা হয়", "নতুন টিকা"],
        "অ্যান্টিবায়োটিকের অতিব্যবহার একে দ্রুত করে।"),
    mcq("Why do large bridge projects set up on-site medical centres and health records for workers?", ["Early treatment of injuries and illness saves lives, and records reveal patterns such as heat or dust problems", "To slow the work", "Only for paperwork", "Workers never get ill"], 0,
        "Occupational health is part of project management.",
        "বড় সেতু-প্রকল্প নির্মাণস্থলে চিকিৎসা-কেন্দ্র আর কর্মীদের স্বাস্থ্য-নথি রাখে কেন?", ["আঘাত আর অসুখের দ্রুত চিকিৎসা জীবন বাঁচায়, আর নথি তাপ বা ধুলোর মতো সমস্যার ধরন দেখায়", "কাজ ধীর করতে", "শুধু কাগজপত্রের জন্য", "কর্মীরা কখনো অসুস্থ হন না"],
        "পেশাগত স্বাস্থ্য প্রকল্প-ব্যবস্থাপনার অংশ।"),
    mcq("What is 'biomimicry' in bridge design?", ["Learning from natural forms and systems, such as spider webs, bones or tree branching, to design efficient structures", "Painting bridges green", "Building bridges for animals only", "Copying another engineer's drawings"], 0,
        "Nature's designs have been refined by evolution over millions of years.",
        "সেতু-নকশায় 'জৈব-অনুকরণ' কী?", ["মাকড়সার জাল, হাড় বা গাছের শাখার মতো প্রাকৃতিক রূপ আর ব্যবস্থা থেকে শিখে দক্ষ কাঠামো নকশা", "সেতু সবুজ রং করা", "শুধু প্রাণীর জন্য সেতু বানানো", "অন্য প্রকৌশলীর নকশা নকল"],
        "প্রকৃতির নকশা লক্ষ লক্ষ বছরের বিবর্তনে নিখুঁত হয়েছে।"),
    mcq("In a quarry village, 4% of people show a recessive inherited trait. Assuming Hardy-Weinberg equilibrium, what share of people are unaffected carriers?", ["32%", "16%", "64%", "4%"], 0,
        "q² = 0.04 so q = 0.2 and p = 0.8. Carriers = 2pq = 2 × 0.8 × 0.2 = 0.32, i.e. 32%. Far more people carry the allele than show it!",
        "এক খাদান-গ্রামে ৪% মানুষের মধ্যে একটি প্রচ্ছন্ন বংশগত বৈশিষ্ট্য দেখা যায়। হার্ডি-ওয়াইনবার্গ সাম্য ধরে নিলে কত শতাংশ মানুষ উপসর্গহীন বাহক?", ["৩২%", "১৬%", "৬৪%", "৪%"],
        "q² = ০.০৪, তাই q = ০.২ আর p = ০.৮। বাহক = 2pq = ২ × ০.৮ × ০.২ = ০.৩২, অর্থাৎ ৩২%। বৈশিষ্ট্য যত জনের দেখা যায়, তার চেয়ে অনেক বেশি মানুষ অ্যালিলটি বহন করে!"),
    mcq("Plankton under a harbour pier fix 50,000 kJ of energy. If about 10% passes to each next feeding level, how much reaches the secondary consumers (small fish-eating fish)?", ["500 kJ", "5,000 kJ", "50 kJ", "5 kJ"], 0,
        "Producers 50,000 → primary consumers 5,000 → secondary consumers 500 kJ. That is why top predators are always few.",
        "বন্দরের জেটির নিচে প্ল্যাঙ্কটন ৫০,০০০ কিলোজুল শক্তি আবদ্ধ করে। প্রতিটি পরের খাদ্যস্তরে প্রায় ১০% গেলে গৌণ খাদকদের (ছোট মাছ-খেকো মাছ) কাছে কত পৌঁছায়?", ["৫০০ কিলোজুল", "৫,০০০ কিলোজুল", "৫০ কিলোজুল", "৫ কিলোজুল"],
        "উৎপাদক ৫০,০০০ → প্রথম স্তরের খাদক ৫,০০০ → গৌণ খাদক ৫০০ কিলোজুল। তাই শীর্ষ শিকারি সবসময় সংখ্যায় কম।"),
    mcq("Ten 1 m² frames thrown at random on a 500 m² approach embankment contain 60 plants of an invasive weed in total. Estimate the weed population on the whole embankment.", ["3,000", "600", "30,000", "6,000"], 0,
        "Mean density = 60 ÷ 10 m² = 6 per m². Population ≈ 6 × 500 = 3,000 plants - time to plan the weeding crew.",
        "৫০০ বর্গমিটারের সংযোগ-বাঁধে এলোমেলোভাবে ফেলা দশটি ১ বর্গমিটারের ফ্রেমে মোট ৬০টি আগ্রাসী আগাছা পাওয়া গেল। পুরো বাঁধে আগাছার সংখ্যা আনুমানিক কত?", ["৩,০০০", "৬০০", "৩০,০০০", "৬,০০০"],
        "গড় ঘনত্ব = ৬০ ÷ ১০ বর্গমিটার = প্রতি বর্গমিটারে ৬টি। মোট ≈ ৬ × ৫০০ = ৩,০০০টি — আগাছা-সাফাই দল পাঠানোর সময়!"),
    mcq("Ecologists tag 40 mud crabs near a new pier and release them. A week later they catch 50 crabs, of which 10 carry tags. Using the Lincoln-Petersen estimate, how many crabs live there?", ["200", "100", "400", "2,000"], 0,
        "N = (first catch × second catch) ÷ tagged recaptures = (40 × 50) ÷ 10 = 200 crabs.",
        "নতুন জেটির কাছে পরিবেশবিদরা ৪০টি কাদা-কাঁকড়াকে চিহ্ন দিয়ে ছেড়ে দেন। এক সপ্তাহ পরে ৫০টি ধরা হলে তার ১০টিতে চিহ্ন পাওয়া যায়। লিঙ্কন-পিটারসেন হিসাবে সেখানে কতগুলি কাঁকড়া থাকে?", ["২০০", "১০০", "৪০০", "২,০০০"],
        "N = (প্রথম ধরা × দ্বিতীয় ধরা) ÷ চিহ্নিত পুনরায় ধরা = (৪০ × ৫০) ÷ ১০ = ২০০টি কাঁকড়া।"),
    mcq("Among 2,000 grit-blasting workers, 50 develop a lung condition in five years, against 10 of 2,000 office staff. What is the attributable risk (extra cases caused per 100 exposed workers)?", ["2 per 100", "5 per 100", "2.5 per 100", "0.5 per 100"], 0,
        "Risk in exposed = 50/2,000 = 2.5%; in unexposed = 10/2,000 = 0.5%. Attributable risk = 2.5 - 0.5 = 2 extra cases per 100 workers - cases that better dust control could prevent.",
        "২,০০০ জন বালি-ব্লাস্টিং কর্মীর মধ্যে পাঁচ বছরে ৫০ জনের ফুসফুসের রোগ হয়, আর ২,০০০ জন অফিসকর্মীর মধ্যে ১০ জনের। আরোপযোগ্য ঝুঁকি (প্রতি ১০০ জন সংস্পর্শে আসা কর্মীতে বাড়তি রোগী) কত?", ["প্রতি ১০০-এ ২", "প্রতি ১০০-এ ৫", "প্রতি ১০০-এ ২.৫", "প্রতি ১০০-এ ০.৫"],
        "সংস্পর্শে থাকা দলে ঝুঁকি = ৫০/২,০০০ = ২.৫%; অন্য দলে = ১০/২,০০০ = ০.৫%। আরোপযোগ্য ঝুঁকি = ২.৫ - ০.৫ = প্রতি ১০০ জনে ২ জন বাড়তি — ভালো ধুলো-নিয়ন্ত্রণে যাদের রোগ ঠেকানো যেত।"),
    mcq("Bacteria in a biofilm on a wet pier cap double every 20 minutes. Starting from 1,000 cells, how many are there after 2 hours of ideal growth?", ["64,000", "6,000", "12,000", "32,000"], 0,
        "2 hours = 6 doublings, so 1,000 × 2⁶ = 1,000 × 64 = 64,000 cells. Exponential growth is why biofilms appear 'overnight'.",
        "ভেজা স্তম্ভ-মাথার জৈব-আস্তরণে ব্যাকটেরিয়া প্রতি ২০ মিনিটে দ্বিগুণ হয়। ১,০০০টি কোষ থেকে শুরু করলে আদর্শ বৃদ্ধিতে ২ ঘণ্টা পরে কতগুলি হবে?", ["৬৪,০০০", "৬,০০০", "১২,০০০", "৩২,০০০"],
        "২ ঘণ্টা = ৬ বার দ্বিগুণ, তাই ১,০০০ × ২⁶ = ১,০০০ × ৬৪ = ৬৪,০০০টি কোষ। সূচকীয় বৃদ্ধির জন্যই জৈব-আস্তরণ যেন 'রাতারাতি' গজিয়ে ওঠে।"),
    mcq("Why do environmental rules often forbid in-river excavation for a bridge during hot, low-flow summer weeks?", ["Warm, slow water already holds little dissolved oxygen, so extra silt and organic matter can suffocate fish", "Excavators overheat in summer", "Fish migrate to the sea every summer", "River water is too clear to see the work"], 0,
        "Oxygen dissolves less in warm water, and low flow means less mixing. Stirred-up sediment raises oxygen demand just when supply is lowest.",
        "গরম, কম-প্রবাহের গ্রীষ্মের সপ্তাহগুলিতে সেতুর জন্য নদীর ভিতরে খননে পরিবেশ-বিধি প্রায়ই নিষেধ করে কেন?", ["গরম, ধীর জলে এমনিতেই দ্রবীভূত অক্সিজেন কম থাকে, তাই বাড়তি পলি আর জৈব পদার্থ মাছের দম বন্ধ করে দিতে পারে", "গ্রীষ্মে খননযন্ত্র অতিরিক্ত গরম হয়", "প্রতি গ্রীষ্মে মাছ সমুদ্রে চলে যায়", "নদীর জল এত স্বচ্ছ যে কাজ দেখা যায় না"],
        "গরম জলে অক্সিজেন কম দ্রবীভূত হয়, আর কম প্রবাহে মেশাও কম হয়। ঘোলা পলি ঠিক তখনই অক্সিজেনের চাহিদা বাড়ায় যখন জোগান সবচেয়ে কম।"),
)
