"""Class 10 - Chemistry (Bridge Engineer): finding concentrations by titration and dilution,
calorimetry and enthalpy change, electrolysis with the Faraday constant, oxidation states,
reacting gas volumes, pH from hydrogen-ion concentration, rates from concentration data, the
chemistry of setting concrete, carbonation and steel passivation, cells, batteries and fuel
cells, isomers and instrumental analysis - all tied to building and keeping bridges."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r * 2, r + 10, r + 2):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + ub for x in o], ex_bn)


def _c(x):
    x = round(x, 3)
    return int(x) if x == int(x) else x


def titre(c1, v1, v2, acid_en, acid_bn):
    c2 = _c(c1 * v1 / v2)
    return _n(f"{v1:g} cm³ of {c1:g} mol/dm³ sodium hydroxide exactly neutralises {v2:g} cm³ of {acid_en} (1 : 1 reaction). What is the acid's concentration?",
              f"{c1:g} mol/dm³ সোডিয়াম হাইড্রক্সাইডের {v1:g} cm³ ঠিক {v2:g} cm³ {acid_bn}-কে প্রশমিত করে (1 : 1 বিক্রিয়া)। অ্যাসিডের গাঢ়ত্ব কত?", c2,
              f"Moles of alkali = {c1:g} x {v1:g} ÷ 1000 = {_c(c1 * v1 / 1000):g}; same moles of acid in {v2:g} cm³, so c = {c2:g} mol/dm³.",
              f"ক্ষারের মোল = {c1:g} x {v1:g} ÷ 1000 = {_c(c1 * v1 / 1000):g}; {v2:g} cm³-এ অ্যাসিডের একই মোল, তাই গাঢ়ত্ব = {c2:g} মোল/dm³।",
              (_c(c1 * v2 / v1), _c(c1 * v1), _c(c2 / 2)), " mol/dm³", " মোল/dm³")


def dilute(c1, v1, v2):
    c2 = _c(c1 * v1 / v2)
    return _n(f"{v1:g} cm³ of {c1:g} mol/dm³ acid is diluted with water to make {v2:g} cm³. What is the new concentration?",
              f"{c1:g} mol/dm³ অ্যাসিডের {v1:g} cm³ জলে মিশিয়ে {v2:g} cm³ করা হলো। নতুন গাঢ়ত্ব কত?", c2,
              f"c1v1 = c2v2: {c1:g} x {v1:g} = c2 x {v2:g}, so c2 = {c2:g} mol/dm³. The moles stay the same; only the volume grows.",
              f"c1v1 = c2v2: {c1:g} x {v1:g} = c2 x {v2:g}, তাই c2 = {c2:g} মোল/dm³। মোল একই থাকে; শুধু আয়তন বাড়ে।",
              (_c(c1 * v2 / v1), _c(c1 - c2) if c1 - c2 > 0 else c2 + 1, _c(c2 * 10)), " mol/dm³", " মোল/dm³")


def calor(m, dt, what_en, what_bn):
    q = _c(m * 4.2 * dt / 1000)
    return _n(f"Burning {what_en} heats {m} g of water by {dt}°C. How much energy did the water gain? (c = 4.2 J/g°C)",
              f"{what_bn} পুড়িয়ে {m} g জল {dt}°C গরম হলো। জল কত শক্তি পেল? (c = 4.2 J/g°C)", q,
              f"Q = mcΔT = {m} x 4.2 x {dt} = {_c(m * 4.2 * dt):g} J = {q:g} kJ.",
              f"Q = mcΔT = {m} x 4.2 x {dt} = {_c(m * 4.2 * dt):g} J = {q:g} কিলোজুল।",
              (_c(m * dt / 1000), _c(m * 4.2 * dt), _c(q * 2)), " kJ", " কিলোজুল")


def dh(q, n, what_en, what_bn):
    r = _c(q / n)
    o = []
    for v in (-r, r, -_c(q * n), -_c(n / q * 1000)):
        if v not in o:
            o.append(v)
    o = o[:4]
    return mcq(f"{q:g} kJ of heat is given out when {n:g} mol of {what_en} burns. What is the enthalpy change per mole?",
               [f"{v:+g} kJ/mol" for v in o], 0,
               f"ΔH = -{q:g} ÷ {n:g} = {-r:g} kJ/mol. The minus sign shows an exothermic reaction.",
               f"{n:g} মোল {what_bn} পুড়ে {q:g} kJ তাপ বেরোয়। প্রতি মোলে এনথ্যালপির পরিবর্তন কত?",
               [f"{v:+g} kJ/মোল" for v in o],
               f"ΔH = -{q:g} ÷ {n:g} = {-r:g} kJ/মোল। ঋণচিহ্ন তাপমোচী বিক্রিয়া দেখায়।")


def faraday(i, t, ar, ch, sym, metal_en, metal_bn):
    mol_e = i * t / 96500
    mass = _c(mol_e / ch * ar)
    return _n(f"A current of {i} A is passed for {t:,} s to plate {metal_en} ({sym}{'⁺' if ch == 1 else '²⁺'} ions, Ar = {ar:g}). What mass is deposited? (1 mol of electrons = 96,500 C)",
              f"{metal_bn} প্রলেপ দিতে {t:,} s ধরে {i} A প্রবাহ চালানো হলো ({sym}{'⁺' if ch == 1 else '²⁺'} আয়ন, Ar = {ar:g})। কত ভর জমা হয়? (1 মোল ইলেকট্রন = 96,500 C)", mass,
              f"Charge = {i} x {t:,} = {i * t:,} C = {_c(mol_e):g} mol of electrons; {ch} electrons per atom gives {_c(mol_e / ch):g} mol x {ar:g} = {mass:g} g.",
              f"আধান = {i} x {t:,} = {i * t:,} C = {_c(mol_e):g} মোল ইলেকট্রন; পরমাণুপ্রতি {ch}টি ইলেকট্রনে {_c(mol_e / ch):g} মোল x {ar:g} = {mass:g} g।",
              (_c(mol_e * ar), _c(mass / 2) if ch == 1 else _c(mass * ch), _c(i * t / 1000)), " g")


def oxstate(formula_en, formula_bn, el, r, alts, why_en, why_bn):
    o = []
    for v in (r, *alts):
        if v not in o:
            o.append(v)
    fmt = lambda v: f"{v:+d}" if v else "0"
    return mcq(f"What is the oxidation state of {el} in {formula_en}?", [fmt(v) for v in o[:4]], 0, why_en,
               f"{formula_bn}-এ {el}-এর জারণ-সংখ্যা কত?", [fmt(v) for v in o[:4]], why_bn)


def gasv(v_known, ratio_need, ratio_known, known_en, known_bn, need_en, need_bn, eq):
    r = _c(v_known * ratio_need / ratio_known)
    return _n(f"{eq}. What volume of {need_en} reacts exactly with {v_known:g} cm³ of {known_en} (same temperature and pressure)?",
              f"{eq}। একই তাপমাত্রা আর চাপে {v_known:g} cm³ {known_bn}-এর সঙ্গে ঠিক কত আয়তন {need_bn} বিক্রিয়া করে?", r,
              f"Gas volumes react in the same ratio as moles: {ratio_known} : {ratio_need}, so {v_known:g} x {ratio_need} ÷ {ratio_known} = {r:g} cm³.",
              f"গ্যাসের আয়তন মোলের অনুপাতেই বিক্রিয়া করে: {ratio_known} : {ratio_need}, তাই {v_known:g} x {ratio_need} ÷ {ratio_known} = {r:g} cm³।",
              (_c(v_known * ratio_known / ratio_need), v_known, _c(r * 3)), " cm³")


def ph(power):
    o = []
    for v in (power, -power if power else 7, power + 1, 14 - power):
        if v not in o and v >= 0:
            o.append(v)
    while len(o) < 4:
        o.append(o[-1] + 2)
    return mcq(f"A sample of rainwater running off a bridge has a hydrogen-ion concentration of 10⁻{power} mol/dm³. What is its pH?" if power else "A solution has a hydrogen-ion concentration of 1 mol/dm³. What is its pH?",
               [str(v) for v in o], 0,
               f"pH = -log[H⁺] = -log(10⁻{power}) = {power}." if power else "pH = -log(1) = 0 - very strongly acidic.",
               f"সেতু থেকে গড়িয়ে আসা বৃষ্টির জলের নমুনায় হাইড্রোজেন-আয়নের গাঢ়ত্ব 10⁻{power} মোল/dm³। এর pH কত?" if power else "একটা দ্রবণে হাইড্রোজেন-আয়নের গাঢ়ত্ব 1 মোল/dm³। এর pH কত?",
               [str(v) for v in o],
               f"pH = -log[H⁺] = -log(10⁻{power}) = {power}। এখানে log মানে 10-ভিত্তিক লগারিদম।" if power else "pH = -log(1) = 0 - খুব তীব্র অম্লীয়।")


def o2need(n, what_en, what_bn, per, eq):
    r = _c(n * per)
    return _n(f"{eq}. How many moles of oxygen are needed to burn {n:g} mol of {what_en} completely?",
              f"{eq}। {n:g} মোল {what_bn} পুরো পোড়াতে কত মোল অক্সিজেন লাগে?", r,
              f"The equation shows {per:g} mol of O2 per mol of fuel: {n:g} x {per:g} = {r:g} mol.",
              f"সমীকরণে প্রতি মোল জ্বালানিতে {per:g} মোল O2: {n:g} x {per:g} = {r:g} মোল।",
              (_c(n / per), _c(n + per), _c(r * 2)), " mol", " মোল")


def crate(c1, c2, t):
    r = _c((c1 - c2) / t)
    return _n(f"In a cement-hydration study, the concentration of a reactant falls from {c1:g} to {c2:g} mol/dm³ in {t} s. What is the mean rate?",
              f"সিমেন্ট-জলযোজনের এক গবেষণায় একটা বিক্রিয়কের গাঢ়ত্ব {t} s-এ {c1:g} থেকে {c2:g} মোল/dm³-এ নামে। গড় হার কত?", r,
              f"Rate = change in concentration ÷ time = ({c1:g} - {c2:g}) ÷ {t} = {r:g} mol/dm³/s.",
              f"হার = গাঢ়ত্বের পরিবর্তন ÷ সময় = ({c1:g} - {c2:g}) ÷ {t} = {r:g} মোল/dm³/s।",
              (_c(c1 / t), _c((c1 + c2) / t), _c(r * 10)), " mol/dm³/s", " মোল/dm³/s")


ITEMS = (
    titre(0.1, 25, 20, "hydrochloric acid", "হাইড্রোক্লোরিক অ্যাসিড"), titre(0.2, 20, 25, "nitric acid", "নাইট্রিক অ্যাসিড"),
    titre(0.5, 10, 25, "an acid cleaner", "একটা অ্যাসিড-পরিষ্কারক"), titre(1, 15, 30, "a pickling acid", "একটা পিকলিং-অ্যাসিড"),
    titre(0.25, 40, 20, "hydrochloric acid", "হাইড্রোক্লোরিক অ্যাসিড"),
    dilute(2, 50, 500), dilute(1, 25, 250), dilute(0.5, 100, 200), dilute(6, 25, 500),
    calor(200, 25, "a sample of fuel", "এক নমুনা জ্বালানি"), calor(100, 40, "some ethanol", "কিছুটা ইথানল"),
    calor(500, 12, "a piece of timber", "এক টুকরো কাঠ"), calor(250, 30, "a candle", "একটা মোমবাতি"), calor(150, 20, "some kerosene", "কিছুটা কেরোসিন"),
    dh(89, 0.1, "methane", "মিথেন"), dh(68.4, 0.05, "ethanol", "ইথানল"), dh(110, 0.05, "propane", "প্রোপেন"), dh(28.6, 0.1, "hydrogen", "হাইড্রোজেন"),
    faraday(10, 9650, 63.5, 2, "Cu", "copper", "তামা"), faraday(5, 19300, 65, 2, "Zn", "zinc", "দস্তা"),
    faraday(2, 9650, 108, 1, "Ag", "silver", "রুপো"), faraday(20, 4825, 58.7, 2, "Ni", "nickel", "নিকেল"),
    oxstate("Fe2O3 (rust)", "Fe2O3 (মরচে)", "Fe", 3, [2, -3, 6], "Each O is -2: 3 x (-2) = -6, so 2 Fe = +6 and each Fe = +3.", "প্রতিটা O -2: 3 x (-2) = -6, তাই 2টি Fe = +6, প্রতিটা Fe = +3।"),
    oxstate("FeO", "FeO", "Fe", 2, [3, -2, 1], "O is -2, so Fe must be +2 for a neutral compound.", "O হলো -2, তাই নিরপেক্ষ যৌগে Fe-কে +2 হতে হবে।"),
    oxstate("CO2", "CO2", "C", 4, [2, -4, 0], "Two O at -2 each = -4, so C = +4.", "দুটো O-র প্রত্যেকটা -2 = -4, তাই C = +4।"),
    oxstate("H2SO4", "H2SO4", "S", 6, [4, 2, -2], "2 H = +2 and 4 O = -8, so S = +6.", "2টি H = +2 আর 4টি O = -8, তাই S = +6।"),
    oxstate("pure zinc metal", "বিশুদ্ধ দস্তা-ধাতু", "Zn", 0, [2, -2, 1], "Elements on their own always have an oxidation state of 0.", "একা মৌলের জারণ-সংখ্যা সবসময় 0।"),
    gasv(100, 1, 2, "hydrogen", "হাইড্রোজেন", "oxygen", "অক্সিজেন", "2H2 + O2 -> 2H2O"),
    gasv(50, 2, 1, "methane", "মিথেন", "oxygen", "অক্সিজেন", "CH4 + 2O2 -> CO2 + 2H2O"),
    gasv(30, 3, 1, "nitrogen", "নাইট্রোজেন", "hydrogen", "হাইড্রোজেন", "N2 + 3H2 -> 2NH3"),
    gasv(40, 5, 1, "propane", "প্রোপেন", "oxygen", "অক্সিজেন", "C3H8 + 5O2 -> 3CO2 + 4H2O"),
    ph(2), ph(4), ph(5), ph(1), ph(6),
    o2need(3, "methane", "মিথেন", 2, "CH4 + 2O2 -> CO2 + 2H2O"), o2need(2, "propane", "প্রোপেন", 5, "C3H8 + 5O2 -> 3CO2 + 4H2O"),
    o2need(4, "hydrogen", "হাইড্রোজেন", 0.5, "2H2 + O2 -> 2H2O"), o2need(1.5, "ethanol", "ইথানল", 3, "C2H5OH + 3O2 -> 2CO2 + 3H2O"),
    titre(0.2, 15, 12, "a descaling acid", "একটা আঁশ-তোলা অ্যাসিড"), calor(300, 15, "some diesel", "কিছুটা ডিজেল"),
    oxstate("Al2O3 (alumina)", "Al2O3 (অ্যালুমিনা)", "Al", 3, [2, -3, 6], "3 O = -6, so 2 Al = +6 and each Al = +3.", "3টি O = -6, তাই 2টি Al = +6, প্রতিটা Al = +3।"),
    gasv(60, 1, 2, "carbon monoxide", "কার্বন মনোক্সাইড", "oxygen", "অক্সিজেন", "2CO + O2 -> 2CO2"), ph(3),
    o2need(2, "butane", "বিউটেন", 6.5, "2C4H10 + 13O2 -> 8CO2 + 10H2O"),
    crate(0.8, 0.5, 60), crate(1.2, 0.4, 200), crate(0.5, 0.2, 30), crate(2, 1.1, 150),
    mcq("Why is a titration repeated until two results agree within 0.1 cm³?", ["Concordant results show the reading is reliable, not a one-off mistake", "To use up the acid", "Because the first result is always right", "To make the flask warmer"], 0,
        "The first 'rough' titration finds roughly where the end point is.",
        "দুটো ফল 0.1 cm³-এর মধ্যে না মেলা পর্যন্ত টাইট্রেশন বারবার করা হয় কেন?", ["মিলে যাওয়া ফল দেখায় পাঠটা ভরসার, একবারের ভুল নয়", "অ্যাসিড শেষ করতে", "কারণ প্রথম ফল সবসময় ঠিক", "ফ্লাস্ক গরম করতে"],
        "প্রথম 'মোটামুটি' টাইট্রেশন শেষবিন্দু আন্দাজে কোথায় তা খোঁজে।"),
    mcq("Why do chemists add acid drop by drop near the end point of a titration?", ["So they do not overshoot the exact point of neutralisation", "To save acid", "To make the reaction slower forever", "Because acid is dangerous only at the end"], 0,
        "Swirling the flask mixes each drop fully.",
        "টাইট্রেশনের শেষবিন্দুর কাছে রসায়নবিদরা ফোঁটা ফোঁটা অ্যাসিড দেন কেন?", ["যাতে প্রশমনের ঠিক বিন্দু পেরিয়ে না যান", "অ্যাসিড বাঁচাতে", "বিক্রিয়া চিরকাল ধীর করতে", "কারণ শুধু শেষে অ্যাসিড বিপজ্জনক"],
        "ফ্লাস্ক ঘোরালে প্রতিটা ফোঁটা পুরো মেশে।"),
    mcq("In calorimetry, why are measured enthalpy changes for burning fuels usually smaller than book values?", ["Heat is lost to the air and the apparatus, and some burning is incomplete", "Fuels get weaker in labs", "Thermometers add heat", "Water absorbs too little"], 0,
        "Insulating the calorimeter and shielding the flame reduce the error.",
        "ক্যালোরিমিতিতে জ্বালানি পোড়ার মাপা এনথ্যালপি-পরিবর্তন সাধারণত বইয়ের মানের চেয়ে কম হয় কেন?", ["বাতাস আর যন্ত্রে তাপ হারায়, আর কিছু দহন অপূর্ণ হয়", "ল্যাবে জ্বালানি দুর্বল হয়", "থার্মোমিটার তাপ যোগ করে", "জল খুব কম শোষে"],
        "ক্যালোরিমিটার অন্তরিত করে আর শিখা আড়াল করে ভুল কমে।"),
    mcq("What does the Faraday constant (about 96,500 C/mol) represent?", ["The charge carried by one mole of electrons", "The voltage of a battery", "The mass of one mole of copper", "The speed of electrons"], 0,
        "It links the current used in electroplating to the mass of metal deposited.",
        "ফ্যারাডে ধ্রুবক (প্রায় 96,500 C/মোল) কী বোঝায়?", ["এক মোল ইলেকট্রন যে আধান বয়", "ব্যাটারির ভোল্টেজ", "এক মোল তামার ভর", "ইলেকট্রনের গতি"],
        "তড়িৎলেপনে ব্যবহৃত প্রবাহকে জমা হওয়া ধাতুর ভরের সঙ্গে জোড়ে।"),
    mcq("Doubling the current in an electroplating bath for the same time does what to the mass of zinc deposited?", ["Doubles it", "Halves it", "Leaves it the same", "Quadruples it"], 0,
        "Mass deposited is proportional to the charge passed (current x time).",
        "একই সময়ে তড়িৎলেপন-পাত্রে প্রবাহ দ্বিগুণ করলে জমা দস্তার ভরের কী হয়?", ["দ্বিগুণ হয়", "অর্ধেক হয়", "একই থাকে", "চারগুণ হয়"],
        "জমা ভর প্রবাহিত আধানের (প্রবাহ x সময়) সমানুপাতিক।"),
    mcq("What is an 'oxidation state'?", ["A number showing how many electrons an atom has lost or gained (or shares unequally) in a compound", "The temperature of oxidation", "The amount of oxygen in air", "The colour of rust"], 0,
        "An increase in oxidation state means oxidation; a decrease means reduction.",
        "'জারণ-সংখ্যা' কী?", ["যৌগে একটা পরমাণু কতগুলো ইলেকট্রন হারিয়েছে বা পেয়েছে (বা অসমভাবে ভাগ করে) তার সংখ্যা", "জারণের তাপমাত্রা", "বাতাসে অক্সিজেনের পরিমাণ", "মরচের রং"],
        "জারণ-সংখ্যা বাড়া মানে জারণ; কমা মানে বিজারণ।"),
    mcq("When iron turns into rust (Fe2O3), what happens to iron's oxidation state?", ["It rises from 0 to +3 - iron is oxidised", "It falls from +3 to 0", "It stays at 0", "It becomes -2"], 0,
        "Oxygen is reduced at the same time, from 0 to -2.",
        "লোহা মরচে (Fe2O3) হলে লোহার জারণ-সংখ্যার কী হয়?", ["0 থেকে +3-এ বাড়ে - লোহা জারিত হয়", "+3 থেকে 0-তে নামে", "0-তেই থাকে", "-2 হয়"],
        "একই সময়ে অক্সিজেন 0 থেকে -2-এ বিজারিত হয়।"),
    mcq("What is a 'redox' reaction?", ["A reaction in which one substance is oxidised while another is reduced", "A reaction that only makes red products", "A reaction with no electrons", "A type of neutralisation only"], 0,
        "Rusting, combustion and batteries all involve redox.",
        "'জারণ-বিজারণ' বিক্রিয়া কী?", ["যে বিক্রিয়ায় একটা পদার্থ জারিত আর অন্যটা বিজারিত হয়", "যে বিক্রিয়ায় শুধু লাল উৎপাদ", "ইলেকট্রনহীন বিক্রিয়া", "শুধু এক রকম প্রশমন"],
        "মরচে, দহন আর ব্যাটারি সবেতেই জারণ-বিজারণ থাকে।"),
    mcq("Why can equal volumes of gases be used directly in reacting ratios?", ["At the same temperature and pressure, equal volumes contain equal numbers of molecules", "All gases have the same mass", "Gases do not react", "Gas volumes never change"], 0,
        "This is Avogadro's law.",
        "গ্যাসের সমান আয়তন সরাসরি বিক্রিয়ার অনুপাতে ব্যবহার করা যায় কেন?", ["একই তাপমাত্রা আর চাপে সমান আয়তনে সমান সংখ্যক অণু থাকে", "সব গ্যাসের ভর সমান", "গ্যাস বিক্রিয়া করে না", "গ্যাসের আয়তন কখনো বদলায় না"],
        "এটা অ্যাভোগাড্রোর সূত্র।"),
    mcq("By how much does pH change when the hydrogen-ion concentration rises 100 times?", ["It falls by 2", "It rises by 2", "It falls by 100", "It does not change"], 0,
        "Each factor of 10 changes pH by 1.",
        "হাইড্রোজেন-আয়নের গাঢ়ত্ব 100 গুণ বাড়লে pH কতটা বদলায়?", ["2 কমে", "2 বাড়ে", "100 কমে", "বদলায় না"],
        "প্রতি 10 গুণে pH 1 বদলায়।"),
    mcq("Why does fresh concrete have a pH of about 12.5?", ["Calcium hydroxide forms as cement hydrates, making the pore water strongly alkaline", "Cement contains acid", "Water is always alkaline", "Sand is alkaline"], 0,
        "This alkalinity is what protects the steel bars inside.",
        "টাটকা কংক্রিটের pH প্রায় 12.5 কেন?", ["সিমেন্টের জলযোজনে ক্যালসিয়াম হাইড্রক্সাইড তৈরি হয়, ছিদ্রের জলকে তীব্র ক্ষারীয় করে", "সিমেন্টে অ্যাসিড থাকে", "জল সবসময় ক্ষারীয়", "বালি ক্ষারীয়"],
        "এই ক্ষারত্বই ভেতরের ইস্পাতের রডকে রক্ষা করে।"),
    mcq("What is 'passivation' of steel bars in concrete?", ["A thin, stable oxide film forms on the steel in the alkaline concrete and stops corrosion", "The steel melting into the concrete", "Painting the bars", "The steel becoming magnetic"], 0,
        "Chlorides or carbonation can break this film down.",
        "কংক্রিটে ইস্পাতের রডের 'নিষ্ক্রিয়করণ' কী?", ["ক্ষারীয় কংক্রিটে ইস্পাতের উপর পাতলা, স্থায়ী অক্সাইড-স্তর তৈরি হয়ে ক্ষয় থামায়", "ইস্পাত কংক্রিটে গলে যাওয়া", "রডে রং করা", "ইস্পাত চৌম্বক হওয়া"],
        "ক্লোরাইড বা কার্বনেশন এই স্তর ভেঙে দিতে পারে।"),
    mcq("How does carbonation put reinforcement at risk?", ["CO2 from the air reacts with calcium hydroxide, lowering the pH near the steel so its protective film is lost", "CO2 makes concrete stronger only", "CO2 cools the steel", "CO2 dissolves sand"], 0,
        "Inspectors spray phenolphthalein on a fresh break: pink means still alkaline.",
        "কার্বনেশন কীভাবে রডকে ঝুঁকিতে ফেলে?", ["বাতাসের CO2 ক্যালসিয়াম হাইড্রক্সাইডের সঙ্গে বিক্রিয়া করে ইস্পাতের কাছে pH কমায়, তাই সুরক্ষা-স্তর হারায়", "CO2 শুধু কংক্রিট শক্ত করে", "CO2 ইস্পাত ঠান্ডা করে", "CO2 বালি গলায়"],
        "পরিদর্শকরা সদ্য-ভাঙা অংশে ফেনলফথ্যালিন ছেটান: গোলাপি মানে এখনো ক্ষারীয়।"),
    mcq("A phenolphthalein spray on a broken concrete core stays colourless for the outer 30 mm. The steel bars are at 25 mm. What does this suggest?", ["Carbonation has reached the steel, so corrosion may begin", "The concrete is perfectly protected", "The bars are made of plastic", "The test always fails"], 0,
        "The repair may involve re-alkalisation or adding more cover.",
        "একটা ভাঙা কংক্রিট-কোরে ফেনলফথ্যালিন ছেটালে বাইরের 30 mm বর্ণহীন থাকে। ইস্পাতের রড আছে 25 mm-এ। এতে কী বোঝা যায়?", ["কার্বনেশন ইস্পাত পর্যন্ত পৌঁছেছে, তাই ক্ষয় শুরু হতে পারে", "কংক্রিট পুরো সুরক্ষিত", "রড প্লাস্টিকের", "পরীক্ষা সবসময় ব্যর্থ"],
        "মেরামতে আবার-ক্ষারীকরণ বা বেশি আবরণ লাগতে পারে।"),
    mcq("What is 'C-S-H' in hardened concrete?", ["Calcium silicate hydrate - the gel that gives cement paste its strength", "A type of steel", "Carbon sulfur hydrogen gas", "A crack-sealing paint"], 0,
        "It grows as cement reacts with water over weeks and months.",
        "শক্ত কংক্রিটে 'সি-এস-এইচ' কী?", ["ক্যালসিয়াম সিলিকেট হাইড্রেট - যে জেল সিমেন্ট-মণ্ডকে শক্তি দেয়", "এক রকম ইস্পাত", "কার্বন-সালফার-হাইড্রোজেন গ্যাস", "ফাটল-বোজানো রং"],
        "সিমেন্ট সপ্তাহ-মাস ধরে জলের সঙ্গে বিক্রিয়া করতে করতে এটা বাড়ে।"),
    mcq("Why is concrete strength usually specified at 28 days?", ["Most strength has developed by then, although hydration continues slowly for years", "Concrete is weakest at 28 days", "It dissolves after 28 days", "28 is a lucky number"], 0,
        "Test cubes are crushed at 7 and 28 days to check the mix.",
        "কংক্রিটের শক্তি সাধারণত 28 দিনে নির্দিষ্ট করা হয় কেন?", ["ততদিনে বেশিরভাগ শক্তি তৈরি হয়ে যায়, যদিও জলযোজন বছরের পর বছর ধীরে চলে", "28 দিনে কংক্রিট সবচেয়ে দুর্বল", "28 দিন পরে গলে যায়", "28 শুভ সংখ্যা"],
        "মিশ্রণ যাচাইয়ে 7 আর 28 দিনে পরীক্ষা-ঘনক ভাঙা হয়।"),
    mcq("Why is cement hydration described as exothermic?", ["Cement reacting with water releases heat, which can warm large pours significantly", "It absorbs heat from the air", "It needs heating to work", "Water freezes when added"], 0,
        "Massive foundations may be cooled with embedded pipes.",
        "সিমেন্টের জলযোজনকে তাপমোচী বলা হয় কেন?", ["জলের সঙ্গে সিমেন্টের বিক্রিয়া তাপ ছাড়ে, যা বড় ঢালাইকে অনেক গরম করতে পারে", "বাতাস থেকে তাপ শোষে", "কাজ করতে গরম করতে হয়", "জল দিলে জমে যায়"],
        "বিশাল ভিতে ভেতরে পাইপ বসিয়ে ঠান্ডা করা হতে পারে।"),
    mcq("What is a 'simple cell' (battery)?", ["Two different metals in an electrolyte, producing a voltage from a redox reaction", "One metal in air", "A wire loop", "A magnet and coil"], 0,
        "The more reactive metal becomes the negative terminal.",
        "'সরল কোষ' (ব্যাটারি) কী?", ["তড়িৎবিশ্লেষ্যে দুটো আলাদা ধাতু, জারণ-বিজারণ বিক্রিয়া থেকে ভোল্টেজ দেয়", "বাতাসে একটা ধাতু", "তারের লুপ", "চুম্বক আর কুণ্ডলী"],
        "বেশি সক্রিয় ধাতুটা ঋণাত্মক প্রান্ত হয়।"),
    mcq("Why do non-rechargeable batteries eventually stop working?", ["The chemicals that react to make the voltage get used up", "The case melts", "Electrons leak out of the top", "They get too heavy"], 0,
        "Rechargeable cells reverse the reaction when charged.",
        "রিচার্জ-অযোগ্য ব্যাটারি শেষ পর্যন্ত কাজ বন্ধ করে কেন?", ["ভোল্টেজ দেওয়া বিক্রিয়ার রাসায়নিক খরচ হয়ে যায়", "খোল গলে যায়", "উপর দিয়ে ইলেকট্রন বেরিয়ে যায়", "খুব ভারী হয়"],
        "রিচার্জযোগ্য কোষ চার্জের সময় বিক্রিয়া উল্টে দেয়।"),
    mcq("Why are lithium-ion batteries used in cordless site tools?", ["They store a lot of energy for their weight and can be recharged many times", "They never need charging", "They are the cheapest batteries", "They work only in cold weather"], 0,
        "Damaged lithium batteries can catch fire - store and charge them safely.",
        "তারহীন নির্মাণ-যন্ত্রে লিথিয়াম-আয়ন ব্যাটারি ব্যবহার হয় কেন?", ["ওজনের তুলনায় অনেক শক্তি জমায় আর বহুবার রিচার্জ করা যায়", "কখনো চার্জ লাগে না", "সবচেয়ে সস্তা ব্যাটারি", "শুধু ঠান্ডায় কাজ করে"],
        "ক্ষতিগ্রস্ত লিথিয়াম ব্যাটারিতে আগুন ধরতে পারে - নিরাপদে রাখো আর চার্জ দাও।"),
    mcq("What is the overall reaction in a hydrogen fuel cell?", ["Hydrogen + oxygen -> water", "Water -> hydrogen + oxygen", "Carbon + oxygen -> carbon dioxide", "Iron + oxygen -> rust"], 0,
        "Unlike burning, the energy is released directly as electricity.",
        "হাইড্রোজেন জ্বালানি-কোষের সামগ্রিক বিক্রিয়া কী?", ["হাইড্রোজেন + অক্সিজেন -> জল", "জল -> হাইড্রোজেন + অক্সিজেন", "কার্বন + অক্সিজেন -> কার্বন ডাইঅক্সাইড", "লোহা + অক্সিজেন -> মরচে"],
        "দহনের মতো নয়, শক্তি সরাসরি বিদ্যুৎ হিসেবে বেরোয়।"),
    mcq("What are 'isomers'?", ["Compounds with the same molecular formula but different structures", "Atoms of the same element with different masses", "Two identical molecules", "Metals that do not rust"], 0,
        "Butane and methylpropane are both C4H10 but have different shapes.",
        "'সমাণু' (আইসোমার) কী?", ["একই আণবিক সংকেত কিন্তু আলাদা গঠনের যৌগ", "একই মৌলের আলাদা ভরের পরমাণু", "দুটো হুবহু একই অণু", "যে ধাতুতে মরচে ধরে না"],
        "বিউটেন আর মিথাইলপ্রোপেন দুটোই C4H10, কিন্তু আকার আলাদা।"),
    mcq("What is a 'homologous series' in organic chemistry?", ["A family of compounds with the same functional group, each differing by CH2", "A list of metals", "A series of bridges", "A set of identical molecules"], 0,
        "Alkanes, alkenes and alcohols are homologous series.",
        "জৈব রসায়নে 'সমগোত্রীয় শ্রেণি' কী?", ["একই কার্যকরী মূলকের যৌগের পরিবার, প্রত্যেকটা CH2-তে আলাদা", "ধাতুর তালিকা", "সেতুর সারি", "হুবহু একই অণুর দল"],
        "অ্যালকেন, অ্যালকিন আর অ্যালকোহল সমগোত্রীয় শ্রেণি।"),
    mcq("Why do larger alkanes have higher boiling points?", ["Bigger molecules have stronger forces between them", "They contain more oxygen", "They are ionic", "They are always solids"], 0,
        "This is why bitumen is solid and methane is a gas.",
        "বড় অ্যালকেনের স্ফুটনাঙ্ক বেশি কেন?", ["বড় অণুর মধ্যে বল বেশি", "এতে বেশি অক্সিজেন", "এরা আয়নীয়", "এরা সবসময় কঠিন"],
        "তাই বিটুমেন কঠিন আর মিথেন গ্যাস।"),
    mcq("What does 'viscosity' mean for a fuel or oil?", ["How thick and slow-flowing it is", "How hot it burns", "How much it costs", "Its colour"], 0,
        "Engine oils are chosen with the right viscosity for the climate.",
        "জ্বালানি বা তেলের ক্ষেত্রে 'সান্দ্রতা' মানে কী?", ["কতটা ঘন আর ধীরে গড়ায়", "কত গরমে পোড়ে", "কত দাম", "এর রং"],
        "জলবায়ু অনুযায়ী ঠিক সান্দ্রতার ইঞ্জিন-তেল বাছা হয়।"),
    mcq("What does infrared spectroscopy tell a chemist about a paint sample from a bridge?", ["Which bonds and functional groups are present, helping identify the paint type", "The paint's price", "The bridge's age", "The paint's weight only"], 0,
        "Instrumental methods are fast, accurate and need only tiny samples.",
        "সেতুর একটা রঙের নমুনা নিয়ে অবলোহিত বর্ণালিবীক্ষণ রসায়নবিদকে কী জানায়?", ["কোন বন্ধন আর কার্যকরী মূলক আছে, রঙের ধরন চিনতে সাহায্য করে", "রঙের দাম", "সেতুর বয়স", "শুধু রঙের ওজন"],
        "যন্ত্র-নির্ভর পদ্ধতি দ্রুত, নির্ভুল আর মাত্র খুদে নমুনা লাগে।"),
    mcq("Why might old bridge paint be tested for lead before blasting it off?", ["Lead dust is toxic, so workers need special protection and waste must be contained", "Lead makes paint shine", "Lead is valuable to sell", "Lead paint is always safe"], 0,
        "Many older steel bridges were painted with lead-based primers.",
        "সেতুর পুরোনো রং ব্লাস্ট করে তোলার আগে সিসার পরীক্ষা হতে পারে কেন?", ["সিসার ধুলো বিষাক্ত, তাই কর্মীদের বিশেষ সুরক্ষা লাগে আর বর্জ্য আটকে রাখতে হয়", "সিসা রং চকচকে করে", "সিসা বেচে লাভ", "সিসার রং সবসময় নিরাপদ"],
        "অনেক পুরোনো ইস্পাতের সেতুতে সিসা-ভিত্তিক প্রাইমার দেওয়া হয়েছিল।"),
    mcq("What is 'atomic absorption' or flame emission analysis used for?", ["Measuring small amounts of metals, such as lead or zinc, in a sample", "Measuring temperature", "Counting bacteria", "Weighing trucks"], 0,
        "Each metal absorbs or emits light at its own wavelengths.",
        "'পারমাণবিক শোষণ' বা শিখা-নিঃসরণ বিশ্লেষণ কীসের জন্য ব্যবহার হয়?", ["নমুনায় সিসা বা দস্তার মতো ধাতুর অল্প পরিমাণ মাপতে", "তাপমাত্রা মাপতে", "ব্যাকটেরিয়া গুনতে", "ট্রাক ওজন করতে"],
        "প্রতিটা ধাতু নিজস্ব তরঙ্গদৈর্ঘ্যে আলো শোষে বা ছাড়ে।"),
    mcq("What is the effect of increasing the concentration of an acid on its reaction rate with limestone?", ["The rate increases, because acid particles collide with the limestone more often", "The rate decreases", "No effect", "The reaction stops"], 0,
        "Polluted, more acidic rain weathers limestone bridges faster.",
        "অ্যাসিডের গাঢ়ত্ব বাড়ালে চুনাপাথরের সঙ্গে বিক্রিয়ার হারে কী প্রভাব পড়ে?", ["হার বাড়ে, কারণ অ্যাসিডের কণা বেশিবার চুনাপাথরে ধাক্কা মারে", "হার কমে", "কোনো প্রভাব নেই", "বিক্রিয়া থেমে যায়"],
        "দূষিত, বেশি অম্লীয় বৃষ্টি চুনাপাথরের সেতুকে দ্রুত ক্ষয় করে।"),
    mcq("On a graph of product made against time, what does a steep start that levels off show?", ["The reaction starts fast, slows as reactants are used up, then stops", "The reaction speeds up forever", "No reaction happened", "The reaction went backwards"], 0,
        "The gradient at any point gives the rate at that moment.",
        "উৎপাদ বনাম সময়ের লেখচিত্রে খাড়া শুরু তারপর সমান হয়ে যাওয়া কী দেখায়?", ["বিক্রিয়া দ্রুত শুরু হয়, বিক্রিয়ক খরচ হতে হতে ধীর হয়, তারপর থামে", "বিক্রিয়া চিরকাল দ্রুত হয়", "কোনো বিক্রিয়া হয়নি", "বিক্রিয়া উল্টো দিকে গেছে"],
        "যেকোনো বিন্দুর ঢাল সেই মুহূর্তের হার দেয়।"),
    mcq("For an exothermic reversible reaction, what does raising the temperature do to the equilibrium?", ["Shifts it towards the reactants, lowering the yield of product", "Shifts it towards the products", "Has no effect", "Stops the reaction"], 0,
        "That is the trade-off in processes like making ammonia.",
        "তাপমোচী উভমুখী বিক্রিয়ায় তাপমাত্রা বাড়ালে সাম্যাবস্থার কী হয়?", ["বিক্রিয়কের দিকে সরে, উৎপাদের ফলন কমে", "উৎপাদের দিকে সরে", "কোনো প্রভাব নেই", "বিক্রিয়া থামে"],
        "অ্যামোনিয়া তৈরির মতো প্রক্রিয়ায় এটাই আপস।"),
    mcq("What is the 'yield' versus 'rate' compromise in industry?", ["Conditions that give the most product at equilibrium may make the reaction too slow, so a middle choice is used", "Industry ignores both", "Rate and yield are always both maximised", "Yield is always 100%"], 0,
        "Cost of energy and equipment also affects the choice.",
        "শিল্পে 'ফলন' বনাম 'হার'-এর আপস কী?", ["যে অবস্থায় সাম্যে সবচেয়ে বেশি উৎপাদ হয়, তাতে বিক্রিয়া খুব ধীর হতে পারে, তাই মাঝামাঝি বাছাই", "শিল্প দুটোই উপেক্ষা করে", "হার আর ফলন সবসময় দুটোই সর্বোচ্চ", "ফলন সবসময় 100%"],
        "শক্তি আর যন্ত্রের খরচও বাছাইয়ে প্রভাব ফেলে।"),
    mcq("What is 'electrolytic refining' of copper for electrical cables?", ["Impure copper is the anode; pure copper deposits on the cathode, leaving impurities behind", "Copper is melted with coal", "Copper is painted", "Copper is dissolved in water only"], 0,
        "Very pure copper conducts electricity best.",
        "বৈদ্যুতিক তারের জন্য তামার 'তড়িৎবিশ্লেষণী শোধন' কী?", ["অশুদ্ধ তামা অ্যানোড; বিশুদ্ধ তামা ক্যাথোডে জমে, অপদ্রব্য পিছনে থাকে", "কয়লার সঙ্গে তামা গলানো", "তামায় রং", "শুধু জলে তামা গলানো"],
        "খুব বিশুদ্ধ তামা বিদ্যুৎ সবচেয়ে ভালো পরিবহন করে।"),
    mcq("Why is a sacrificial anode on a steel pier eventually replaced?", ["It slowly corrodes away as it protects the steel", "It grows too large", "It becomes radioactive", "It turns into steel"], 0,
        "Divers check and replace zinc or aluminium anodes on a schedule.",
        "ইস্পাতের স্তম্ভের আত্মত্যাগী অ্যানোড শেষ পর্যন্ত বদলাতে হয় কেন?", ["ইস্পাতকে রক্ষা করতে করতে ধীরে ক্ষয়ে যায়", "খুব বড় হয়ে যায়", "তেজস্ক্রিয় হয়", "ইস্পাত হয়ে যায়"],
        "ডুবুরিরা নির্দিষ্ট সময় অন্তর দস্তা বা অ্যালুমিনিয়ামের অ্যানোড দেখে বদলান।"),
    mcq("What is 'impressed current' cathodic protection?", ["A small DC power supply forces electrons onto the steel so it becomes the cathode and does not corrode", "Painting the steel with current", "Heating the steel", "Striking the steel with lightning"], 0,
        "It is used on large bridges and reinforced concrete decks.",
        "'আরোপিত প্রবাহ' ক্যাথোডিক সুরক্ষা কী?", ["একটা ছোট ডিসি বিদ্যুৎ-উৎস ইস্পাতে ইলেকট্রন ঠেলে দেয়, তাই এটা ক্যাথোড হয়ে ক্ষয় থেকে বাঁচে", "প্রবাহ দিয়ে ইস্পাতে রং", "ইস্পাত গরম করা", "বাজ দিয়ে ইস্পাতে আঘাত"],
        "বড় সেতু আর রিইনফোর্সড কংক্রিটের পাটাতনে ব্যবহার হয়।"),
    mcq("Why do chemists use 'mol/dm³' rather than 'g/dm³' when comparing acid strengths in reactions?", ["Reactions depend on numbers of particles, which moles count directly", "Grams are not accurate", "Moles are heavier", "It is just tradition"], 0,
        "Equal concentrations in mol/dm³ contain equal numbers of particles per litre.",
        "বিক্রিয়ায় অ্যাসিডের শক্তি তুলনায় রসায়নবিদরা 'g/dm³'-এর বদলে 'মোল/dm³' ব্যবহার করেন কেন?", ["বিক্রিয়া কণার সংখ্যার উপর নির্ভর করে, যা মোল সরাসরি গোনে", "গ্রাম সঠিক নয়", "মোল বেশি ভারী", "শুধু প্রথা"],
        "মোল/dm³-এ সমান গাঢ়ত্বে প্রতি লিটারে সমান সংখ্যক কণা থাকে।"),
    mcq("What is 'standard solution' in chemistry?", ["A solution whose concentration is known accurately", "Any solution in a lab", "Pure water", "A solution with no solute"], 0,
        "It is made by dissolving an exact mass in an exact volume.",
        "রসায়নে 'প্রমাণ দ্রবণ' কী?", ["যে দ্রবণের গাঢ়ত্ব নিখুঁতভাবে জানা", "ল্যাবের যেকোনো দ্রবণ", "বিশুদ্ধ জল", "দ্রবহীন দ্রবণ"],
        "নিখুঁত আয়তনে নিখুঁত ভর গুলে তৈরি।"),
    mcq("Why are safety data sheets (SDS) kept for every chemical on a bridge site?", ["They list hazards, safe handling, first aid and spill procedures", "They are price lists", "They are delivery notes", "They are optional decoration"], 0,
        "Workers must be able to find them quickly in an emergency.",
        "সেতু-নির্মাণস্থলে প্রতিটা রাসায়নিকের জন্য নিরাপত্তা-তথ্যপত্র (এসডিএস) রাখা হয় কেন?", ["এতে বিপদ, নিরাপদ ব্যবহার, প্রাথমিক চিকিৎসা আর ছড়িয়ে পড়লে করণীয় থাকে", "এগুলো দামের তালিকা", "ডেলিভারি-চালান", "ঐচ্ছিক সাজসজ্জা"],
        "জরুরি অবস্থায় কর্মীদের দ্রুত খুঁজে পেতে হবে।"),
    mcq("What is the danger of mixing bleach with acid-based cleaners in a site washroom?", ["They react to release toxic chlorine gas", "They make the floor slippery only", "They cancel each other harmlessly", "They make perfume"], 0,
        "Never mix cleaning chemicals.",
        "নির্মাণস্থলের শৌচাগারে ব্লিচ আর অ্যাসিড-ভিত্তিক পরিষ্কারক মেশালে বিপদ কী?", ["বিক্রিয়া করে বিষাক্ত ক্লোরিন গ্যাস ছাড়ে", "শুধু মেঝে পিছল করে", "নিরীহভাবে কাটাকাটি হয়", "সুগন্ধ তৈরি করে"],
        "কখনো পরিষ্কারের রাসায়নিক মেশাবে না।"),
    mcq("Why must cement powder never be handled with bare, wet skin for long periods?", ["Wet cement is strongly alkaline and can cause chemical burns and dermatitis", "Cement is radioactive", "Cement is magnetic", "It is completely harmless"], 0,
        "Wear gloves and wash skin promptly with clean water.",
        "খালি, ভেজা হাতে দীর্ঘক্ষণ সিমেন্টের গুঁড়ো ধরা কখনো উচিত নয় কেন?", ["ভেজা সিমেন্ট তীব্র ক্ষারীয়, রাসায়নিক পোড়া আর চর্মরোগ ঘটাতে পারে", "সিমেন্ট তেজস্ক্রিয়", "সিমেন্ট চৌম্বক", "পুরো নিরীহ"],
        "দস্তানা পরো আর তাড়াতাড়ি পরিষ্কার জলে চামড়া ধোও।"),
    mcq("What is the purpose of an 'air-entraining' admixture in concrete for cold regions?", ["It creates tiny bubbles that relieve pressure when water in the concrete freezes", "It makes concrete float", "It adds oxygen for rusting", "It makes concrete set instantly"], 0,
        "It greatly improves freeze-thaw durability of bridge decks.",
        "ঠান্ডা অঞ্চলের কংক্রিটে 'বায়ু-আবদ্ধকারী' সংযোজকের উদ্দেশ্য কী?", ["খুদে বুদবুদ তৈরি করে, কংক্রিটের জল জমলে চাপ কমায়", "কংক্রিট ভাসায়", "মরচের জন্য অক্সিজেন যোগ করে", "তখনই কংক্রিট জমায়"],
        "সেতুর পাটাতনের জমা-গলা টেকসইতা অনেক বাড়ায়।"),
    mcq("What is 'efflorescence' on new concrete or brick piers?", ["White salt deposits left when water carrying dissolved salts evaporates at the surface", "Green moss", "Rust stains", "Paint peeling"], 0,
        "It is usually harmless but shows water is moving through the material.",
        "নতুন কংক্রিট বা ইটের স্তম্ভে 'লবণ-ফোটা' কী?", ["দ্রবীভূত লবণ বয়ে আনা জল উপরিতলে বাষ্প হয়ে যে সাদা লবণ রেখে যায়", "সবুজ শ্যাওলা", "মরচের দাগ", "রং উঠে যাওয়া"],
        "সাধারণত নিরীহ, তবে দেখায় উপাদানের মধ্যে দিয়ে জল চলছে।"),
    mcq("Why must the rebar cover (concrete thickness over steel) be checked before pouring?", ["Too little cover lets carbonation and chlorides reach the steel much sooner", "Too much cover makes steel rust", "Cover affects only colour", "Cover does not matter"], 0,
        "Plastic spacers hold the bars at the correct distance from the formwork.",
        "ঢালাইয়ের আগে রডের আবরণ (ইস্পাতের উপর কংক্রিটের পুরুত্ব) যাচাই করতে হয় কেন?", ["খুব কম আবরণে কার্বনেশন আর ক্লোরাইড অনেক তাড়াতাড়ি ইস্পাতে পৌঁছায়", "বেশি আবরণে ইস্পাতে মরচে ধরে", "আবরণ শুধু রঙে প্রভাব ফেলে", "আবরণ গুরুত্বহীন"],
        "প্লাস্টিকের স্পেসার রডকে ছাঁচ থেকে ঠিক দূরত্বে রাখে।"),
    mcq("What is 'mill scale' on new hot-rolled steel?", ["A layer of iron oxides formed during rolling, which must be removed before painting", "A weighing scale in the mill", "A grade of steel", "A type of paint"], 0,
        "Paint over mill scale can flake off as the scale cracks.",
        "নতুন গরম-গড়ানো ইস্পাতে 'কারখানার আঁশ' কী?", ["গড়ানোর সময় তৈরি লোহার অক্সাইডের স্তর, রং করার আগে সরাতে হয়", "কারখানার দাঁড়িপাল্লা", "ইস্পাতের এক মান", "এক রকম রং"],
        "আঁশের উপর রং করলে আঁশ ফাটলে রং খসে পড়তে পারে।"),
    mcq("Which gas is produced at the cathode when acidified water is electrolysed?", ["Hydrogen", "Oxygen", "Chlorine", "Carbon dioxide"], 0,
        "Twice as much hydrogen as oxygen is made, by volume.",
        "অম্লীকৃত জলের তড়িৎবিশ্লেষণে ক্যাথোডে কোন গ্যাস তৈরি হয়?", ["হাইড্রোজেন", "অক্সিজেন", "ক্লোরিন", "কার্বন ডাইঅক্সাইড"],
        "আয়তনে অক্সিজেনের দ্বিগুণ হাইড্রোজেন তৈরি হয়।"),
    mcq("What is 'green hydrogen'?", ["Hydrogen made by electrolysing water using renewable electricity", "Hydrogen coloured green", "Hydrogen from burning coal", "Hydrogen found in plants"], 0,
        "It could one day power heavy construction machinery with no carbon emissions.",
        "'সবুজ হাইড্রোজেন' কী?", ["নবায়নযোগ্য বিদ্যুতে জলের তড়িৎবিশ্লেষণে তৈরি হাইড্রোজেন", "সবুজ রঙের হাইড্রোজেন", "কয়লা পোড়ানো থেকে হাইড্রোজেন", "উদ্ভিদে পাওয়া হাইড্রোজেন"],
        "একদিন হয়তো কার্বন-নির্গমন ছাড়াই ভারী নির্মাণ-যন্ত্র চালাবে।"),
    mcq("What is 'electrolysis of brine' used to make that is important for treating drinking water?", ["Chlorine", "Copper", "Nitrogen", "Methane"], 0,
        "Chlorine kills harmful microbes in water supplies.",
        "লবণজলের তড়িৎবিশ্লেষণে খাবার জল শোধনে জরুরি কী তৈরি হয়?", ["ক্লোরিন", "তামা", "নাইট্রোজেন", "মিথেন"],
        "ক্লোরিন জল-সরবরাহের ক্ষতিকর জীবাণু মারে।"),
    mcq("Why is the bitumen used for bridge deck waterproofing sometimes 'polymer-modified'?", ["Added polymers make it more elastic and resistant to cracking in cold and flowing in heat", "To make it smell better", "To make it cheaper", "To colour it red"], 0,
        "Decks flex under traffic, so the waterproofing must flex too.",
        "সেতুর পাটাতন জলরোধী করার বিটুমেন কখনো 'পলিমার-সংশোধিত' করা হয় কেন?", ["যুক্ত পলিমার একে বেশি স্থিতিস্থাপক করে, ঠান্ডায় ফাটা আর গরমে গড়ানো রোধ করে", "গন্ধ ভালো করতে", "সস্তা করতে", "লাল রং করতে"],
        "যানবাহনে পাটাতন বাঁকে, তাই জলরোধী স্তরকেও বাঁকতে হয়।"),
    mcq("What is 'zinc-rich primer' used for on steel bridges?", ["A paint loaded with zinc dust that gives sacrificial protection like galvanising", "A decorative top coat", "A paint remover", "A concrete sealer"], 0,
        "It is often the first coat in a multi-coat paint system.",
        "ইস্পাতের সেতুতে 'দস্তা-সমৃদ্ধ প্রাইমার' কীসের জন্য ব্যবহার হয়?", ["দস্তার গুঁড়োয় ভরা রং, যা গ্যালভানাইজিংয়ের মতো আত্মত্যাগী সুরক্ষা দেয়", "সাজানোর শেষ পোঁচ", "রং তোলার রাসায়নিক", "কংক্রিটের সিলার"],
        "বহুস্তর রং-ব্যবস্থায় প্রায়ই এটাই প্রথম পোঁচ।"),
    mcq("Why are steel bridges painted with several thin coats rather than one thick coat?", ["Thin coats cure properly and together block water and oxygen with fewer pinholes", "One coat is illegal", "Thin coats are heavier", "To use more paint brushes"], 0,
        "Each coat has a job: primer, intermediate barrier and weather-resistant top coat.",
        "ইস্পাতের সেতুতে এক পোঁচ মোটা রঙের বদলে কয়েক পোঁচ পাতলা রং দেওয়া হয় কেন?", ["পাতলা পোঁচ ঠিকমতো জমে আর একসঙ্গে কম ছিদ্রে জল আর অক্সিজেন আটকায়", "এক পোঁচ বেআইনি", "পাতলা পোঁচ ভারী", "বেশি তুলি ব্যবহার করতে"],
        "প্রতিটা পোঁচের কাজ আছে: প্রাইমার, মাঝের বাধা আর আবহাওয়া-রোধী শেষ পোঁচ।"),
)
