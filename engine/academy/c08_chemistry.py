"""Class 8 - Chemistry (Junior Cadet): reacting masses from equations, limiting reactants,
titration sums, bond energies, rates from measurements, equilibrium and the Haber process,
formulae of ionic compounds, electrolysis products, chromatography (Rf), alkanes, alkenes and
cracking, and the chemistry that attacks concrete and steel in bridges."""
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
    x = round(x, 2)
    return int(x) if x == int(x) else x


# (equation, reactant en, reactant bn, Mr in x moles, product en, product bn, Mr out x moles)
REACT = {
    "lime": ("CaCO3 -> CaO + CO2", "calcium carbonate", "ক্যালসিয়াম কার্বনেট", 100, "calcium oxide", "ক্যালসিয়াম অক্সাইড", 56),
    "iron": ("Fe2O3 + 3CO -> 2Fe + 3CO2", "iron(III) oxide", "আয়রন(III) অক্সাইড", 160, "iron", "লোহা", 112),
    "mgo": ("2Mg + O2 -> 2MgO", "magnesium", "ম্যাগনেসিয়াম", 48, "magnesium oxide", "ম্যাগনেসিয়াম অক্সাইড", 80),
    "co2": ("CaCO3 -> CaO + CO2", "calcium carbonate", "ক্যালসিয়াম কার্বনেট", 100, "carbon dioxide", "কার্বন ডাইঅক্সাইড", 44),
    "zno": ("2Zn + O2 -> 2ZnO", "zinc", "দস্তা", 130, "zinc oxide", "জিঙ্ক অক্সাইড", 162),
}


def rmass(key, m):
    eq, a_en, a_bn, mi, b_en, b_bn, mo = REACT[key]
    r = _c(m * mo / mi)
    return _n(f"{eq}. What mass of {b_en} can be made from {m:g} g of {a_en}? (Mr totals: {a_en} {mi}, {b_en} {mo})",
              f"{eq}। {m:g} g {a_bn} থেকে কত {b_bn} তৈরি হতে পারে? (মোট Mr: {a_bn} {mi}, {b_bn} {mo})", r,
              f"Mass = {m:g} x {mo} ÷ {mi} = {r:g} g. The ratio of masses follows the ratio of Mr totals.",
              f"ভর = {m:g} x {mo} ÷ {mi} = {r:g} g। ভরের অনুপাত মোট Mr-এর অনুপাত মেনে চলে।",
              (_c(m * mi / mo), m, _c(r / 2)), " g")


def titr(vol_ml, conc, acid_en, acid_bn):
    mol = _c(vol_ml * conc / 1000)
    return _n(f"In a titration, {vol_ml} cm³ of {conc:g} mol/dm³ {acid_en} is used. How many moles of acid is that?",
              f"একটা টাইট্রেশনে {conc:g} mol/dm³ {acid_bn}-এর {vol_ml} cm³ লাগল। সেটা কত মোল অ্যাসিড?", mol,
              f"Moles = concentration x volume in dm³ = {conc:g} x {vol_ml} ÷ 1,000 = {mol:g} mol.",
              f"মোল = গাঢ়ত্ব x আয়তন (dm³-এ) = {conc:g} x {vol_ml} ÷ 1,000 = {mol:g} mol।",
              (_c(vol_ml * conc), _c(vol_ml / conc / 1000), _c(mol * 10)), " mol", " মোল")


def bonds(broken, made, what_en, what_bn):
    dh = broken - made
    sign = "exothermic" if dh < 0 else "endothermic"
    sign_bn = "তাপমোচী" if dh < 0 else "তাপগ্রাহী"
    o = []
    for v in (dh, -dh, broken + made, made):
        if v not in o:
            o.append(v)
    return mcq(f"For {what_en}, bonds broken total {broken:,} kJ and bonds made total {made:,} kJ. What is the energy change?",
               [f"{v:+,} kJ" for v in o[:4]], 0,
               f"ΔH = broken - made = {broken:,} - {made:,} = {dh:+,} kJ, so the reaction is {sign}.",
               f"{what_bn}-তে ভাঙা বন্ধনের মোট শক্তি {broken:,} kJ আর গড়া বন্ধনের {made:,} kJ। শক্তির পরিবর্তন কত?",
               [f"{v:+,} kJ" for v in o[:4]],
               f"ΔH = ভাঙা - গড়া = {broken:,} - {made:,} = {dh:+,} kJ, তাই বিক্রিয়াটা {sign_bn}।")


def rate(amount, secs, unit_en, unit_bn, what_en, what_bn):
    r = _c(amount / secs)
    return _n(f"{what_en} gives off {amount:g} {unit_en} of gas in {secs} s. What is the mean rate of reaction?",
              f"{what_bn} {secs} s-এ {amount:g} {unit_bn} গ্যাস ছাড়ে। বিক্রিয়ার গড় হার কত?", r,
              f"Mean rate = amount ÷ time = {amount:g} ÷ {secs} = {r:g} {unit_en}/s.",
              f"গড় হার = পরিমাণ ÷ সময় = {amount:g} ÷ {secs} = {r:g} {unit_bn}/s।",
              (_c(secs / amount), _c(amount * secs), _c(r * 10)), f" {unit_en}/s", f" {unit_bn}/s")


def rf(spot, front, dye_en, dye_bn):
    r = _c(spot / front)
    o = []
    for v in (r, _c(front / spot), _c(1 - r) if _c(1 - r) != r else _c(r + 0.1), _c(spot / 100)):
        if v not in o:
            o.append(v)
    while len(o) < 4:
        o.append(_c(o[-1] + 0.05))
    return mcq(f"In a chromatogram of {dye_en}, a spot moves {spot:g} cm while the solvent moves {front:g} cm. What is the Rf value?",
               [f"{v:g}" for v in o], 0,
               f"Rf = distance moved by spot ÷ distance moved by solvent = {spot:g} ÷ {front:g} = {r:g}. It is always less than 1.",
               f"{dye_bn}-এর একটা ক্রোমাটোগ্রামে একটা দাগ {spot:g} cm যায়, দ্রাবক যায় {front:g} cm। Rf মান কত?",
               [f"{v:g}" for v in o],
               f"Rf = দাগের সরণ ÷ দ্রাবকের সরণ = {spot:g} ÷ {front:g} = {r:g}। এটা সবসময় 1-এর কম।")


SUP = {1: "⁺", 2: "²⁺", 3: "³⁺"}
SUPN = {1: "⁻", 2: "²⁻", 3: "³⁻"}


def formula(cat, cc, an, ac, right, wrongs, name_en, name_bn):
    """Ionic compound: which ratio of ions makes the charges cancel? right/wrongs are (n_cat, n_an)."""
    show = lambda r: f"{r[0]} {cat}{SUP[cc]} : {r[1]} {an}{SUPN[ac]}"
    sym = f"{cat}{right[0] if right[0] > 1 else ''}{an}{right[1] if right[1] > 1 else ''}"
    opts = [show(r) for r in (right, *wrongs)]
    return mcq(f"{name_en[0].upper() + name_en[1:]} is made of {cat}{SUP[cc]} and {an}{SUPN[ac]} ions. In what ratio do they combine?",
               opts, 0,
               f"Charges must cancel: {right[0]} x (+{cc}) + {right[1]} x (-{ac}) = 0, giving the formula {sym}.",
               f"{name_bn} {cat}{SUP[cc]} আর {an}{SUPN[ac]} আয়নে তৈরি। এরা কোন অনুপাতে যুক্ত হয়?",
               opts,
               f"আধান কাটাকাটি হতে হবে: {right[0]} x (+{cc}) + {right[1]} x (-{ac}) = 0, তাই সংকেত {sym}।")


def electro(salt_en, salt_bn, cath_en, cath_bn, an_en, an_bn, wrong_en, wrong_bn):
    return mcq(f"Molten {salt_en} is electrolysed. What forms at the negative electrode (cathode)?",
               [cath_en, an_en, wrong_en[0], wrong_en[1]], 0,
               f"Positive metal ions gain electrons at the cathode and become {cath_en}; {an_en} forms at the anode.",
               f"গলিত {salt_bn}-এর তড়িৎবিশ্লেষণ করা হলো। ঋণাত্মক তড়িদ্বারে (ক্যাথোড) কী তৈরি হয়?",
               [cath_bn, an_bn, wrong_bn[0], wrong_bn[1]],
               f"ধনাত্মক ধাতব আয়ন ক্যাথোডে ইলেকট্রন নিয়ে {cath_bn} হয়; অ্যানোডে {an_bn} তৈরি হয়।")


def limiting(a_mol, b_mol, ratio_b, a_en, a_bn, b_en, b_bn, eq):
    need_b = a_mol * ratio_b
    lim_en, lim_bn = (a_en, a_bn) if b_mol >= need_b else (b_en, b_bn)
    oth_en, oth_bn = (b_en, b_bn) if lim_en == a_en else (a_en, a_bn)
    return mcq(f"{eq}. {a_mol:g} mol of {a_en} is mixed with {b_mol:g} mol of {b_en}. Which is the limiting reactant?",
               [lim_en.capitalize(), oth_en.capitalize(), "Neither - both run out together", "Water"], 0,
               f"{a_mol:g} mol of {a_en} needs {need_b:g} mol of {b_en}; there is {b_mol:g} mol, so {lim_en} runs out first.",
               f"{eq}। {a_mol:g} mol {a_bn} {b_mol:g} mol {b_bn}-এর সঙ্গে মেশানো হলো। সীমাবদ্ধ বিক্রিয়ক কোনটা?",
               [lim_bn, oth_bn, "কোনোটা না - দুটোই একসঙ্গে ফুরোয়", "জল"],
               f"{a_mol:g} mol {a_bn}-এর জন্য {need_b:g} mol {b_bn} লাগে; আছে {b_mol:g} mol, তাই {lim_bn} আগে ফুরোয়।")


ITEMS = (
    rmass("lime", 50), rmass("lime", 250), rmass("iron", 80), rmass("iron", 400), rmass("mgo", 12),
    rmass("mgo", 6), rmass("co2", 25), rmass("co2", 1000), rmass("zno", 13), rmass("zno", 65),
    titr(25, 0.1, "hydrochloric acid", "হাইড্রোক্লোরিক অ্যাসিড"), titr(20, 0.5, "sulphuric acid", "সালফিউরিক অ্যাসিড"),
    titr(50, 0.2, "nitric acid", "নাইট্রিক অ্যাসিড"), titr(12.5, 2, "hydrochloric acid", "হাইড্রোক্লোরিক অ্যাসিড"),
    titr(40, 0.25, "ethanoic acid", "ইথানোয়িক অ্যাসিড"),
    bonds(2648, 3466, "burning methane", "মিথেন পোড়ানো"), bonds(1370, 1856, "burning hydrogen", "হাইড্রোজেন পোড়ানো"),
    bonds(2238, 2346, "making ammonia", "অ্যামোনিয়া তৈরি"), bonds(1840, 1600, "a decomposition", "একটা বিয়োজন"),
    bonds(945, 860, "splitting a compound", "একটা যৌগ ভাঙা"),
    rate(60, 30, "cm³", "cm³", "Marble chips in acid", "অ্যাসিডে মার্বেলের টুকরো"),
    rate(90, 45, "cm³", "cm³", "Zinc in acid", "অ্যাসিডে দস্তা"), rate(2.4, 60, "g", "g", "A fizzing tablet", "একটা বুদবুদ-ওঠা বড়ি"),
    rate(150, 50, "cm³", "cm³", "Magnesium ribbon in acid", "অ্যাসিডে ম্যাগনেসিয়ামের ফিতে"),
    rate(1.5, 30, "g", "g", "Limestone powder in acid", "অ্যাসিডে চুনাপাথরের গুঁড়ো"),
    rf(3, 6, "red ink", "লাল কালি"), rf(2, 8, "a food dye", "একটা খাদ্য-রং"), rf(4.5, 9, "blue marker ink", "নীল মার্কারের কালি"),
    rf(6, 8, "a paint pigment", "একটা রঙের রঞ্জক"), rf(1.2, 6, "green ink", "সবুজ কালি"),
    formula("Ca", 2, "Cl", 1, (1, 2), [(1, 1), (2, 1), (2, 3)], "calcium chloride", "ক্যালসিয়াম ক্লোরাইড"),
    formula("Al", 3, "O", 2, (2, 3), [(1, 1), (3, 2), (1, 3)], "aluminium oxide", "অ্যালুমিনিয়াম অক্সাইড"),
    formula("Na", 1, "O", 2, (2, 1), [(1, 1), (1, 2), (2, 3)], "sodium oxide", "সোডিয়াম অক্সাইড"),
    formula("Fe", 3, "Cl", 1, (1, 3), [(1, 1), (3, 1), (1, 2)], "iron(III) chloride", "আয়রন(III) ক্লোরাইড"),
    formula("Mg", 2, "O", 2, (1, 1), [(2, 1), (1, 2), (2, 3)], "magnesium oxide", "ম্যাগনেসিয়াম অক্সাইড"),
    formula("Zn", 2, "Cl", 1, (1, 2), [(1, 1), (2, 1), (1, 3)], "zinc chloride", "জিঙ্ক ক্লোরাইড"),
    electro("lead bromide", "লেড ব্রোমাইড", "Lead", "সিসা", "Bromine", "ব্রোমিন", ["Hydrogen", "Oxygen"], ["হাইড্রোজেন", "অক্সিজেন"]),
    electro("sodium chloride", "সোডিয়াম ক্লোরাইড", "Sodium", "সোডিয়াম", "Chlorine", "ক্লোরিন", ["Oxygen", "Hydrogen"], ["অক্সিজেন", "হাইড্রোজেন"]),
    electro("aluminium oxide (in cryolite)", "অ্যালুমিনিয়াম অক্সাইড (ক্রায়োলাইটে)", "Aluminium", "অ্যালুমিনিয়াম", "Oxygen", "অক্সিজেন", ["Carbon", "Hydrogen"], ["কার্বন", "হাইড্রোজেন"]),
    electro("zinc chloride", "জিঙ্ক ক্লোরাইড", "Zinc", "দস্তা", "Chlorine", "ক্লোরিন", ["Hydrogen", "Oxygen"], ["হাইড্রোজেন", "অক্সিজেন"]),
    limiting(2, 3, 2, "magnesium", "ম্যাগনেসিয়াম", "hydrochloric acid", "হাইড্রোক্লোরিক অ্যাসিড", "Mg + 2HCl -> MgCl2 + H2"),
    limiting(4, 1, 0.5, "hydrogen", "হাইড্রোজেন", "oxygen", "অক্সিজেন", "2H2 + O2 -> 2H2O"),
    limiting(1, 5, 3, "nitrogen", "নাইট্রোজেন", "hydrogen", "হাইড্রোজেন", "N2 + 3H2 -> 2NH3"),
    limiting(4, 2, 0.75, "iron", "লোহা", "oxygen", "অক্সিজেন", "4Fe + 3O2 -> 2Fe2O3"),
    mcq("What is the 'limiting reactant'?", ["The reactant that is used up first, so it decides how much product forms", "The reactant in excess", "The catalyst", "The product"], 0,
        "Extra of the other reactant is simply left over.",
        "'সীমাবদ্ধ বিক্রিয়ক' কী?", ["যে বিক্রিয়ক আগে ফুরিয়ে যায়, তাই কতটা উৎপাদ হবে তা ঠিক করে", "যে বিক্রিয়ক বেশি আছে", "অনুঘটক", "উৎপাদ"],
        "অন্য বিক্রিয়কের বাড়তিটা শুধু পড়ে থাকে।"),
    mcq("What is a titration used for?", ["Finding the exact volume of one solution that reacts with another, to work out a concentration", "Heating a liquid until it boils", "Separating inks", "Weighing solids"], 0,
        "Labs titrate to check the strength of acids used to clean steel before painting.",
        "টাইট্রেশন কীসের জন্য ব্যবহার হয়?", ["একটা দ্রবণের ঠিক কত আয়তন অন্যটার সঙ্গে বিক্রিয়া করে তা বের করে গাঢ়ত্ব হিসাব করতে", "তরল ফোটা পর্যন্ত গরম করতে", "কালি আলাদা করতে", "কঠিন ওজন করতে"],
        "রঙের আগে ইস্পাত পরিষ্কারের অ্যাসিড কত কড়া, ল্যাব টাইট্রেশনে তা যাচাই করে।"),
    mcq("In a titration, why is an indicator added?", ["Its colour change shows the exact moment the acid and alkali have neutralised", "To make the reaction faster", "To add more acid", "To cool the flask"], 0,
        "Phenolphthalein turns from pink to colourless at the end point.",
        "টাইট্রেশনে নির্দেশক যোগ করা হয় কেন?", ["এর রং-বদল দেখায় ঠিক কোন মুহূর্তে অ্যাসিড আর ক্ষার প্রশমিত হলো", "বিক্রিয়া দ্রুত করতে", "আরও অ্যাসিড যোগ করতে", "ফ্লাস্ক ঠান্ডা করতে"],
        "শেষ বিন্দুতে ফেনলফথ্যালিন গোলাপি থেকে বর্ণহীন হয়।"),
    mcq("What piece of equipment delivers the acid drop by drop in a titration?", ["A burette", "A beaker", "A test tube", "A funnel"], 0,
        "A pipette measures the fixed volume of alkali in the flask.",
        "টাইট্রেশনে কোন যন্ত্র ফোঁটা ফোঁটা অ্যাসিড দেয়?", ["বুরেট", "বিকার", "টেস্ট-টিউব", "ফানেল"],
        "ফ্লাস্কে ক্ষারের নির্দিষ্ট আয়তন মাপে পিপেট।"),
    mcq("In terms of bonds, why is a reaction exothermic?", ["More energy is released making new bonds than is taken in breaking old ones", "No bonds are broken", "Bonds break but none form", "It absorbs heat from the room"], 0,
        "Breaking bonds takes energy in; making bonds gives energy out.",
        "বন্ধনের দিক থেকে একটা বিক্রিয়া তাপমোচী হয় কেন?", ["নতুন বন্ধন গড়তে যত শক্তি বেরোয়, পুরোনো ভাঙতে তার চেয়ে কম লাগে", "কোনো বন্ধন ভাঙে না", "বন্ধন ভাঙে কিন্তু গড়ে না", "ঘর থেকে তাপ শোষে"],
        "বন্ধন ভাঙতে শক্তি ঢোকে; গড়তে শক্তি বেরোয়।"),
    mcq("Why doesn't propane from a site heater's cylinder burn until a spark is applied?", ["The molecules need a minimum energy - the activation energy - before they can react", "Propane cannot burn", "The spark adds the oxygen", "Propane only burns underwater"], 0,
        "Once started, the heat given out supplies the activation energy for the next molecules.",
        "নির্মাণস্থলের হিটারের সিলিন্ডারের প্রোপেন স্ফুলিঙ্গ না দেওয়া পর্যন্ত জ্বলে না কেন?", ["বিক্রিয়ার আগে অণুদের ন্যূনতম শক্তি - সক্রিয়করণ শক্তি - লাগে", "প্রোপেন জ্বলতে পারে না", "স্ফুলিঙ্গ অক্সিজেন যোগ করে", "প্রোপেন শুধু জলের নিচে জ্বলে"],
        "একবার শুরু হলে বেরোনো তাপই পরের অণুদের সক্রিয়করণ শক্তি জোগায়।"),
    mcq("A catalyst is added to a reversible reaction. What does it change?", ["Equilibrium is reached faster, but the amounts at equilibrium stay the same", "More product forms at equilibrium", "Less product forms", "The reaction stops"], 0,
        "A catalyst speeds up the forward and backward reactions equally.",
        "একটা উভমুখী বিক্রিয়ায় অনুঘটক যোগ করা হলো। এটা কী বদলায়?", ["সাম্যাবস্থায় দ্রুত পৌঁছায়, কিন্তু সাম্যে পরিমাণ একই থাকে", "সাম্যে বেশি উৎপাদ হয়", "কম উৎপাদ হয়", "বিক্রিয়া থেমে যায়"],
        "অনুঘটক সম্মুখ আর পশ্চাৎ বিক্রিয়াকে সমানভাবে দ্রুত করে।"),
    mcq("Why does powdered limestone react with acid faster than lumps of the same mass?", ["Powder has a much larger surface area, so collisions happen more often", "Powder is a different chemical", "Lumps are heavier", "Acid prefers powder's colour"], 0,
        "Fine dust can even burn explosively for the same reason.",
        "একই ভরের চুনাপাথরের ডেলার চেয়ে গুঁড়ো অ্যাসিডের সঙ্গে দ্রুত বিক্রিয়া করে কেন?", ["গুঁড়োর উপরিতলের ক্ষেত্রফল অনেক বেশি, তাই ধাক্কা বেশি ঘন ঘন হয়", "গুঁড়ো আলাদা রাসায়নিক", "ডেলা ভারী", "অ্যাসিড গুঁড়োর রং পছন্দ করে"],
        "একই কারণে সূক্ষ্ম ধুলো বিস্ফোরণের মতো জ্বলতেও পারে।"),
    mcq("What does a 'dynamic equilibrium' mean in a reversible reaction?", ["Forward and backward reactions go at the same rate, so amounts stay constant", "Both reactions have stopped", "Only the forward reaction happens", "The reaction explodes"], 0,
        "It is busy on the inside but looks still from the outside.",
        "উভমুখী বিক্রিয়ায় 'গতিশীল সাম্যাবস্থা' মানে কী?", ["সম্মুখ আর পশ্চাৎ বিক্রিয়া সমান হারে চলে, তাই পরিমাণ স্থির থাকে", "দুটো বিক্রিয়াই থেমে গেছে", "শুধু সম্মুখ বিক্রিয়া চলে", "বিক্রিয়া বিস্ফোরিত হয়"],
        "ভেতরে ব্যস্ত, বাইরে থেকে স্থির দেখায়।"),
    mcq("What does Le Chatelier's principle say?", ["If conditions change, an equilibrium shifts to oppose the change", "Equilibrium never moves", "Reactions always go to completion", "Catalysts shift equilibrium"], 0,
        "Add more reactant and the equilibrium shifts to use it up.",
        "লা শাতেলিয়ের নীতি কী বলে?", ["অবস্থা বদলালে সাম্যাবস্থা বদলের বিরোধিতা করতে সরে যায়", "সাম্যাবস্থা কখনো নড়ে না", "বিক্রিয়া সবসময় শেষ পর্যন্ত যায়", "অনুঘটক সাম্যাবস্থা সরায়"],
        "বেশি বিক্রিয়ক দিলে সাম্যাবস্থা তা খরচ করার দিকে সরে।"),
    mcq("In the Haber process N2 + 3H2 ⇌ 2NH3, why does high pressure give more ammonia?", ["The right side has fewer gas molecules, so equilibrium shifts that way to reduce pressure", "Pressure heats the gas", "Ammonia is heavier", "Pressure removes the catalyst"], 0,
        "4 molecules on the left, 2 on the right.",
        "হেবার প্রক্রিয়ায় N2 + 3H2 ⇌ 2NH3-এ উচ্চ চাপে বেশি অ্যামোনিয়া হয় কেন?", ["ডানদিকে গ্যাস-অণু কম, তাই চাপ কমাতে সাম্যাবস্থা সেদিকে সরে", "চাপ গ্যাস গরম করে", "অ্যামোনিয়া ভারী", "চাপ অনুঘটক সরায়"],
        "বাঁদিকে 4টি অণু, ডানদিকে 2টি।"),
    mcq("Why is ammonia from the Haber process important?", ["It is used to make fertilisers that feed billions of people", "It is used to make concrete set", "It is a fuel for trucks only", "It paints bridges"], 0,
        "It is also used to make explosives used in quarrying and tunnelling.",
        "হেবার প্রক্রিয়ার অ্যামোনিয়া জরুরি কেন?", ["এ দিয়ে সার বানানো হয় যা কোটি কোটি মানুষের খাদ্য জোগায়", "কংক্রিট জমাতে লাগে", "শুধু ট্রাকের জ্বালানি", "সেতু রং করে"],
        "খাদান আর সুড়ঙ্গ-খোঁড়ার বিস্ফোরক বানাতেও লাগে।"),
    mcq("A magnesium atom loses 2 electrons. What does it become?", ["A magnesium ion, Mg²⁺", "A magnesium ion, Mg²⁻", "A neutral magnesium atom", "An oxygen atom"], 0,
        "Losing negative electrons leaves more protons than electrons, so the charge is 2+.",
        "একটা ম্যাগনেসিয়াম পরমাণু 2টি ইলেকট্রন হারাল। এটা কী হয়?", ["ম্যাগনেসিয়াম আয়ন, Mg²⁺", "ম্যাগনেসিয়াম আয়ন, Mg²⁻", "নিরপেক্ষ ম্যাগনেসিয়াম পরমাণু", "অক্সিজেন পরমাণু"],
        "ঋণাত্মক ইলেকট্রন হারালে প্রোটন ইলেকট্রনের চেয়ে বেশি থাকে, তাই আধান 2+।"),
    mcq("Why does solid salt not conduct electricity, but molten salt does?", ["In the solid, ions are fixed in place; when molten they can move and carry charge", "Solid salt has no ions", "Molten salt contains metal wires", "Heat creates electrons"], 0,
        "That is why electrolysis needs the compound molten or dissolved.",
        "কঠিন নুন বিদ্যুৎ পরিবহন করে না, কিন্তু গলিত নুন করে কেন?", ["কঠিনে আয়ন এক জায়গায় আটকে থাকে; গললে চলতে পারে আর আধান বয়", "কঠিন নুনে আয়ন নেই", "গলিত নুনে ধাতুর তার থাকে", "তাপ ইলেকট্রন বানায়"],
        "তাই তড়িৎবিশ্লেষণে যৌগকে গলিত বা দ্রবীভূত রাখতে হয়।"),
    mcq("At which electrode does oxidation happen during electrolysis?", ["The anode (positive electrode)", "The cathode (negative electrode)", "Both equally", "Neither"], 0,
        "Remember OIL RIG: oxidation is loss of electrons - negative ions lose them at the anode.",
        "তড়িৎবিশ্লেষণে কোন তড়িদ্বারে জারণ হয়?", ["অ্যানোড (ধনাত্মক তড়িদ্বার)", "ক্যাথোড (ঋণাত্মক তড়িদ্বার)", "দুটোয় সমান", "কোনোটাতেই না"],
        "মনে রাখো: জারণ মানে ইলেকট্রন হারানো - ঋণাত্মক আয়ন অ্যানোডে তা হারায়।"),
    mcq("Why is aluminium oxide dissolved in molten cryolite before electrolysis?", ["It lowers the melting temperature, saving a lot of energy", "Cryolite is the aluminium ore itself", "To make the aluminium coloured", "To stop electricity flowing"], 0,
        "Aluminium oxide alone melts above 2,000°C.",
        "তড়িৎবিশ্লেষণের আগে অ্যালুমিনিয়াম অক্সাইড গলিত ক্রায়োলাইটে দ্রবীভূত করা হয় কেন?", ["গলনের তাপমাত্রা কমায়, অনেক শক্তি বাঁচে", "ক্রায়োলাইটই অ্যালুমিনিয়ামের আকরিক", "অ্যালুমিনিয়াম রঙিন করতে", "বিদ্যুৎ বন্ধ করতে"],
        "শুধু অ্যালুমিনিয়াম অক্সাইড 2,000°C-এর বেশিতে গলে।"),
    mcq("Why do the carbon anodes in aluminium smelting need replacing often?", ["Oxygen made at the anode reacts with the carbon and burns it away as CO2", "They melt into aluminium", "They are stolen", "They turn into gold"], 0,
        "This is one reason aluminium production releases carbon dioxide.",
        "অ্যালুমিনিয়াম নিষ্কাশনে কার্বনের অ্যানোড প্রায়ই বদলাতে হয় কেন?", ["অ্যানোডে তৈরি অক্সিজেন কার্বনের সঙ্গে বিক্রিয়া করে তাকে CO2 হিসেবে পুড়িয়ে ফেলে", "অ্যালুমিনিয়ামে গলে যায়", "চুরি হয়", "সোনা হয়ে যায়"],
        "অ্যালুমিনিয়াম উৎপাদনে কার্বন ডাইঅক্সাইড বেরোনোর এটা একটা কারণ।"),
    mcq("What does chromatography do?", ["Separates a mixture of dissolved substances, such as the dyes in an ink", "Makes new compounds", "Measures temperature", "Hardens concrete"], 0,
        "Different substances travel at different speeds with the solvent.",
        "ক্রোমাটোগ্রাফি কী করে?", ["দ্রবীভূত পদার্থের মিশ্রণ আলাদা করে, যেমন কালির রংগুলো", "নতুন যৌগ বানায়", "তাপমাত্রা মাপে", "কংক্রিট শক্ত করে"],
        "দ্রাবকের সঙ্গে বিভিন্ন পদার্থ বিভিন্ন গতিতে চলে।"),
    mcq("A sample gives a single spot in several different solvents. What does that suggest?", ["It is probably a pure substance", "It is a mixture of many dyes", "The paper is broken", "The solvent is wrong"], 0,
        "A mixture usually splits into more than one spot.",
        "একটা নমুনা কয়েকটা আলাদা দ্রাবকে একটাই দাগ দেয়। এতে কী বোঝা যায়?", ["সম্ভবত এটা বিশুদ্ধ পদার্থ", "এটা অনেক রঙের মিশ্রণ", "কাগজ ছেঁড়া", "দ্রাবক ভুল"],
        "মিশ্রণ সাধারণত একাধিক দাগে ভাগ হয়।"),
    mcq("Why is the start line on chromatography paper drawn in pencil, not ink?", ["Pencil (graphite) does not dissolve and run in the solvent", "Pencil is cheaper", "Ink is too dark", "Pencil glows in the dark"], 0,
        "Ink would separate too and spoil the result.",
        "ক্রোমাটোগ্রাফি-কাগজের শুরুর রেখা কালিতে নয়, পেনসিলে আঁকা হয় কেন?", ["পেনসিলের গ্রাফাইট দ্রাবকে গলে ছড়ায় না", "পেনসিল সস্তা", "কালি খুব গাঢ়", "পেনসিল অন্ধকারে জ্বলে"],
        "কালিও আলাদা হয়ে ফলাফল নষ্ট করত।"),
    mcq("What are alkanes?", ["Saturated hydrocarbons with only single C-C bonds, like methane and propane", "Hydrocarbons with a C=C double bond", "Metals in group 1", "Acids in vinegar"], 0,
        "General formula CnH2n+2.",
        "অ্যালকেন কী?", ["শুধু একক C-C বন্ধনযুক্ত সম্পৃক্ত হাইড্রোকার্বন, যেমন মিথেন আর প্রোপেন", "C=C দ্বিবন্ধনযুক্ত হাইড্রোকার্বন", "গ্রুপ 1-এর ধাতু", "ভিনিগারের অ্যাসিড"],
        "সাধারণ সংকেত CnH2n+2।"),
    mcq("What is the formula of the alkane with 3 carbon atoms (propane)?", ["C3H8", "C3H6", "C3H4", "C3H3"], 0,
        "CnH2n+2 with n = 3 gives C3H8 - the gas in many site heaters.",
        "3টি কার্বন-পরমাণুর অ্যালকেনের (প্রোপেন) সংকেত কী?", ["C3H8", "C3H6", "C3H4", "C3H3"],
        "CnH2n+2-এ n = 3 দিলে C3H8 - অনেক নির্মাণস্থলের হিটারের গ্যাস।"),
    mcq("How can you tell an alkene from an alkane in the lab?", ["Bromine water turns from orange to colourless with an alkene", "Alkenes smell of roses", "Alkanes are always solid", "Limewater turns milky"], 0,
        "The C=C double bond adds bromine across it.",
        "ল্যাবে অ্যালকিন আর অ্যালকেন কীভাবে চেনা যায়?", ["অ্যালকিনের সঙ্গে ব্রোমিন-জল কমলা থেকে বর্ণহীন হয়", "অ্যালকিনে গোলাপের গন্ধ", "অ্যালকেন সবসময় কঠিন", "চুনজল দুধের মতো হয়"],
        "C=C দ্বিবন্ধনে ব্রোমিন যুক্ত হয়ে যায়।"),
    mcq("What is 'cracking' in an oil refinery?", ["Breaking long hydrocarbon molecules into shorter, more useful ones", "Cracking open oil barrels", "Mixing oil and water", "Freezing oil"], 0,
        "It turns heavy fractions into petrol and alkenes for making plastics.",
        "তেল-শোধনাগারে 'ক্র্যাকিং' কী?", ["লম্বা হাইড্রোকার্বন-অণুকে ছোট, বেশি কাজের অণুতে ভাঙা", "তেলের পিপে ফাটানো", "তেল আর জল মেশানো", "তেল জমানো"],
        "ভারী অংশকে পেট্রোল আর প্লাস্টিক বানানোর অ্যালকিনে বদলায়।"),
    mcq("Which fraction of crude oil is used to surface roads and waterproof bridge decks?", ["Bitumen", "Petrol", "Kerosene", "Refinery gas"], 0,
        "Bitumen has very long molecules, so it is thick and sticky.",
        "অশোধিত তেলের কোন অংশ দিয়ে রাস্তা বাঁধানো আর সেতুর পাটাতন জলরোধী করা হয়?", ["বিটুমেন", "পেট্রোল", "কেরোসিন", "শোধনাগারের গ্যাস"],
        "বিটুমেনের অণু খুব লম্বা, তাই এটা ঘন আর আঠালো।"),
    mcq("Why do long-chain hydrocarbons like bitumen have high boiling points?", ["Stronger forces between their long molecules need more energy to overcome", "They contain metal", "They are already gases", "They have no molecules"], 0,
        "Short chains like methane boil far below 0°C.",
        "বিটুমেনের মতো লম্বা-শৃঙ্খল হাইড্রোকার্বনের স্ফুটনাঙ্ক বেশি কেন?", ["লম্বা অণুর মধ্যে বল বেশি, কাটাতে বেশি শক্তি লাগে", "এতে ধাতু আছে", "এরা আগেই গ্যাস", "এদের অণু নেই"],
        "মিথেনের মতো ছোট শৃঙ্খল 0°C-এর অনেক নিচে ফোটে।"),
    mcq("What is an 'addition polymer' like poly(ethene)?", ["A long chain made by joining many small alkene molecules by opening their double bonds", "A mixture of metals", "A type of salt", "A single small molecule"], 0,
        "Thousands of ethene units link into one chain.",
        "পলি(ইথিন)-এর মতো 'যুত পলিমার' কী?", ["অনেক ছোট অ্যালকিন-অণুর দ্বিবন্ধন খুলে জুড়ে তৈরি লম্বা শৃঙ্খল", "ধাতুর মিশ্রণ", "এক রকম লবণ", "একটা ছোট অণু"],
        "হাজার হাজার ইথিন-একক জুড়ে একটা শৃঙ্খল হয়।"),
    mcq("Why are polymer bearing pads (such as neoprene) used under bridge beams?", ["They are flexible and tough, letting the beam move slightly while spreading its load", "They are the cheapest metal", "They conduct electricity", "They dissolve in rain"], 0,
        "Steel plates are often bonded inside to stop them bulging.",
        "সেতুর কড়ির নিচে পলিমারের বিয়ারিং-প্যাড (যেমন নিওপ্রিন) ব্যবহার হয় কেন?", ["নমনীয় আর মজবুত, কড়িকে সামান্য নড়তে দেয় আর বোঝা ছড়িয়ে দেয়", "সবচেয়ে সস্তা ধাতু", "বিদ্যুৎ পরিবহন করে", "বৃষ্টিতে গলে যায়"],
        "ফুলে ওঠা আটকাতে প্রায়ই ভেতরে ইস্পাতের পাত জোড়া থাকে।"),
    mcq("What is 'sulfate attack' on concrete?", ["Sulfates in soil or water react with hardened cement, forming crystals that swell and crack it", "Concrete turning sweet", "Painting concrete yellow", "Rain washing away sand"], 0,
        "Sulfate-resisting cement is used for foundations in such ground.",
        "কংক্রিটে 'সালফেট-আক্রমণ' কী?", ["মাটি বা জলের সালফেট শক্ত সিমেন্টের সঙ্গে বিক্রিয়া করে ফুলে-ওঠা কেলাস বানায় আর ফাটল ধরায়", "কংক্রিট মিষ্টি হয়ে যাওয়া", "কংক্রিটে হলুদ রং", "বৃষ্টিতে বালি ধুয়ে যাওয়া"],
        "এমন মাটিতে ভিতের জন্য সালফেট-রোধী সিমেন্ট ব্যবহার হয়।"),
    mcq("Why are bridges near the sea or on salted winter roads at risk of rebar corrosion?", ["Chloride ions soak into the concrete and break down the protective layer on the steel", "Salt makes concrete heavier", "Salt freezes the steel", "Sea air is pure oxygen"], 0,
        "Extra concrete cover and low-permeability mixes slow chlorides down.",
        "সমুদ্রের কাছের বা শীতে নুন-ছড়ানো রাস্তার সেতুর রডে মরচের ঝুঁকি কেন?", ["ক্লোরাইড আয়ন কংক্রিটে চুঁইয়ে ঢুকে ইস্পাতের সুরক্ষা-স্তর ভেঙে দেয়", "নুন কংক্রিট ভারী করে", "নুন ইস্পাত জমিয়ে দেয়", "সমুদ্রের বাতাস বিশুদ্ধ অক্সিজেন"],
        "বেশি কংক্রিট-আবরণ আর কম-ভেদ্য মিশ্রণ ক্লোরাইডকে ধীর করে।"),
    mcq("Why does rust cause concrete to crack and break off (spalling)?", ["Rust takes up several times the volume of the steel, pushing the concrete apart", "Rust is very hot", "Rust dissolves concrete instantly", "Rust is magnetic"], 0,
        "Brown stains and cracks along the line of a bar are a warning sign.",
        "মরচে কংক্রিটে ফাটল ধরিয়ে টুকরো খসিয়ে দেয় (স্প্যালিং) কেন?", ["মরচে ইস্পাতের কয়েক গুণ জায়গা নেয়, কংক্রিটকে ঠেলে ফাটায়", "মরচে খুব গরম", "মরচে তখনই কংক্রিট গলায়", "মরচে চৌম্বক"],
        "রডের লাইন বরাবর বাদামি দাগ আর ফাটল বিপদসংকেত।"),
    mcq("What is 'alkali-silica reaction' (ASR) in concrete?", ["Alkalis in cement react with some silica in aggregates, forming a gel that swells and cracks the concrete", "Concrete reacting with sunlight", "Sand turning into glass", "Rain making concrete stronger"], 0,
        "It shows as map-like cracking; engineers test aggregates to avoid it.",
        "কংক্রিটে 'ক্ষার-সিলিকা বিক্রিয়া' (এএসআর) কী?", ["সিমেন্টের ক্ষার কিছু খোয়ার সিলিকার সঙ্গে বিক্রিয়া করে জেল বানায়, যা ফুলে কংক্রিট ফাটায়", "সূর্যালোকের সঙ্গে কংক্রিটের বিক্রিয়া", "বালি কাচ হয়ে যাওয়া", "বৃষ্টিতে কংক্রিট শক্ত হওয়া"],
        "মানচিত্রের মতো ফাটল দেখা যায়; এড়াতে প্রকৌশলীরা খোয়া পরীক্ষা করেন।"),
    mcq("Why is fly ash (from power stations) often added to concrete for bridges?", ["It reacts slowly with lime in cement, making concrete denser, more durable and lower in CO2", "It makes concrete set in seconds", "It colours concrete black", "It is a type of steel"], 0,
        "It also reduces heat in big pours and resists chlorides better.",
        "সেতুর কংক্রিটে প্রায়ই ফ্লাই-অ্যাশ (বিদ্যুৎকেন্দ্রের ছাই) মেশানো হয় কেন?", ["সিমেন্টের চুনের সঙ্গে ধীরে বিক্রিয়া করে কংক্রিটকে ঘন, টেকসই আর কম কার্বন ডাইঅক্সাইডের করে", "সেকেন্ডে কংক্রিট জমায়", "কংক্রিট কালো করে", "এক রকম ইস্পাত"],
        "বড় ঢালাইয়ে তাপও কমায় আর ক্লোরাইড ভালো রোধ করে।"),
    mcq("In a rusting cell on a steel girder, what is the role of water?", ["It acts as the electrolyte that lets ions move between areas of the steel", "It cools the steel so it cannot rust", "It is a catalyst that is not needed", "It turns into iron"], 0,
        "Dry steel in dry air hardly rusts at all.",
        "ইস্পাতের গার্ডারে মরচে-কোষে জলের ভূমিকা কী?", ["তড়িৎবিশ্লেষ্য হিসেবে কাজ করে, ইস্পাতের এক জায়গা থেকে আরেক জায়গায় আয়ন চলতে দেয়", "ইস্পাত ঠান্ডা রাখে, তাই মরচে ধরে না", "অনাবশ্যক অনুঘটক", "লোহা হয়ে যায়"],
        "শুকনো বাতাসে শুকনো ইস্পাতে প্রায় মরচে ধরে না।"),
    mcq("Why does galvanised steel still resist rust even when the zinc coating is scratched?", ["Zinc is more reactive, so it corrodes instead of the exposed iron (sacrificial protection)", "Scratches heal by themselves", "Zinc turns into paint", "Iron stops being metal"], 0,
        "Paint alone protects only while it is unbroken.",
        "দস্তার আবরণে আঁচড় লাগলেও গ্যালভানাইজড ইস্পাত মরচে রোধ করে কেন?", ["দস্তা বেশি সক্রিয়, তাই খোলা লোহার বদলে নিজে ক্ষয়ে যায় (আত্মত্যাগী সুরক্ষা)", "আঁচড় নিজে সেরে যায়", "দস্তা রং হয়ে যায়", "লোহা আর ধাতু থাকে না"],
        "শুধু রং ততক্ষণই রক্ষা করে যতক্ষণ অটুট থাকে।"),
    mcq("What is 'potable' water?", ["Water that is safe to drink", "Water stored in pots", "Sea water", "Water used only for concrete"], 0,
        "Site drinking water must be potable; concrete also needs clean water.",
        "'পানযোগ্য' জল কী?", ["যে জল খাওয়া নিরাপদ", "হাঁড়িতে রাখা জল", "সমুদ্রের জল", "শুধু কংক্রিটের জল"],
        "নির্মাণস্থলের খাবার জল পানযোগ্য হতে হবে; কংক্রিটেও পরিষ্কার জল লাগে।"),
    mcq("What are the main steps in treating river water for drinking?", ["Filtering out solids, then killing microbes with chlorine or UV light", "Adding salt and sugar", "Boiling it into steam only", "Adding cement"], 0,
        "Sedimentation and filtration remove dirt; disinfection makes it safe.",
        "নদীর জল খাওয়ার উপযোগী করার প্রধান ধাপগুলো কী?", ["কঠিন কণা ছেঁকে, তারপর ক্লোরিন বা অতিবেগুনি আলোয় জীবাণু মারা", "নুন আর চিনি মেশানো", "শুধু ফুটিয়ে বাষ্প করা", "সিমেন্ট মেশানো"],
        "থিতানো আর ছাঁকা ময়লা সরায়; জীবাণুমুক্তি নিরাপদ করে।"),
    mcq("Why shouldn't sea water be used to mix reinforced concrete?", ["Its chlorides would corrode the steel bars", "It is too cold", "It makes concrete too strong", "Fish would get trapped"], 0,
        "Only clean, low-chloride water is allowed for reinforced concrete.",
        "রিইনফোর্সড কংক্রিট মাখতে সমুদ্রের জল ব্যবহার করা উচিত নয় কেন?", ["এর ক্লোরাইড ইস্পাতের রডে মরচে ধরাবে", "খুব ঠান্ডা", "কংক্রিট বেশি শক্ত করে", "মাছ আটকে যাবে"],
        "রিইনফোর্সড কংক্রিটে শুধু পরিষ্কার, কম-ক্লোরাইডের জল অনুমোদিত।"),
    mcq("What is a 'nanoparticle'?", ["A particle 1-100 nanometres across, with a huge surface area for its size", "A particle as big as a grain of sand", "A tiny animal", "A type of atom nucleus"], 0,
        "Nano-silica can make concrete denser; nano-coatings can repel water.",
        "'ন্যানো-কণা' কী?", ["1-100 ন্যানোমিটার মাপের কণা, মাপের তুলনায় বিশাল উপরিতল", "বালির দানার মতো বড় কণা", "খুব ছোট প্রাণী", "এক রকম পরমাণু-কেন্দ্রক"],
        "ন্যানো-সিলিকা কংক্রিট ঘন করতে পারে; ন্যানো-আবরণ জল তাড়াতে পারে।"),
    mcq("Why is the air inside a steel box girder sometimes kept dry with a dehumidifier?", ["Rusting needs water; dry air stops corrosion inside where painting is hard", "To keep workers cool", "To make the girder lighter", "To stop sound"], 0,
        "The Great Belt and Forth Road bridges protect cables and girders this way.",
        "ইস্পাতের বাক্স-গার্ডারের ভেতরের বাতাস কখনো ডিহিউমিডিফায়ার দিয়ে শুকনো রাখা হয় কেন?", ["মরচের জন্য জল লাগে; শুকনো বাতাস ভেতরে ক্ষয় থামায়, যেখানে রং করা কঠিন", "কর্মীদের ঠান্ডা রাখতে", "গার্ডার হালকা করতে", "শব্দ থামাতে"],
        "গ্রেট বেল্ট আর ফোর্থ রোড সেতু এভাবে তার আর গার্ডার রক্ষা করে।"),
    mcq("Why is a weathering steel bridge left unpainted?", ["Its alloy forms a dense, stable rust layer that protects the steel underneath", "Paint is not allowed on bridges", "It never touches air", "It is made of gold"], 0,
        "Its brown colour is the protective layer, not a sign of failure.",
        "আবহ-সহ ইস্পাতের সেতু রং ছাড়া রাখা হয় কেন?", ["এর সংকর ঘন, স্থায়ী মরচের স্তর বানায়, যা নিচের ইস্পাতকে রক্ষা করে", "সেতুতে রং নিষিদ্ধ", "কখনো বাতাস লাগে না", "সোনা দিয়ে তৈরি"],
        "এর বাদামি রংটাই সুরক্ষা-স্তর, ব্যর্থতার চিহ্ন নয়।"),
    mcq("What does a 'half equation' such as Fe -> Fe²⁺ + 2e⁻ show?", ["Iron atoms losing electrons - oxidation - at the corroding area", "Iron gaining electrons", "Iron turning into a gas", "Iron becoming a neutron"], 0,
        "The electrons travel through the steel to where oxygen is reduced.",
        "Fe -> Fe²⁺ + 2e⁻-এর মতো 'অর্ধ-সমীকরণ' কী দেখায়?", ["ক্ষয়-হওয়া জায়গায় লোহার পরমাণুর ইলেকট্রন হারানো - জারণ", "লোহার ইলেকট্রন পাওয়া", "লোহা গ্যাস হয়ে যাওয়া", "লোহা নিউট্রন হয়ে যাওয়া"],
        "ইলেকট্রনগুলো ইস্পাত দিয়ে সেখানে যায় যেখানে অক্সিজেন বিজারিত হয়।"),
    mcq("Which pair of metals would give the biggest voltage in a simple cell?", ["Magnesium and copper - they are far apart in the reactivity series", "Copper and copper", "Zinc and zinc", "Iron and iron"], 0,
        "The further apart the metals in reactivity, the bigger the voltage - and the faster the more reactive one corrodes.",
        "একটা সরল কোষে কোন জোড়া ধাতু সবচেয়ে বেশি ভোল্টেজ দেবে?", ["ম্যাগনেসিয়াম আর তামা - সক্রিয়তা-শ্রেণিতে অনেক দূরে", "তামা আর তামা", "দস্তা আর দস্তা", "লোহা আর লোহা"],
        "সক্রিয়তায় ধাতু যত দূরে, ভোল্টেজ তত বেশি - আর বেশি সক্রিয়টা তত দ্রুত ক্ষয়ে যায়।"),
    mcq("Why should copper pipes not be fixed directly to galvanised steel?", ["The two metals form a cell in wet conditions and the zinc and steel corrode fast", "Copper is too heavy", "They are different colours", "Copper is magnetic"], 0,
        "Engineers use insulating washers to separate different metals.",
        "তামার পাইপ সরাসরি গ্যালভানাইজড ইস্পাতে লাগানো উচিত নয় কেন?", ["ভেজা অবস্থায় দুই ধাতু কোষ তৈরি করে আর দস্তা ও ইস্পাত দ্রুত ক্ষয়ে যায়", "তামা খুব ভারী", "রং আলাদা", "তামা চৌম্বক"],
        "প্রকৌশলীরা আলাদা ধাতু আলাদা রাখতে অন্তরক ওয়াশার ব্যবহার করেন।"),
    mcq("Why does hard water 'fur up' the boiler of a site canteen?", ["Heating breaks down dissolved calcium hydrogencarbonate into insoluble calcium carbonate scale", "Hard water contains sand", "Boilers make their own chalk", "Soft water contains more calcium"], 0,
        "Scale wastes energy because it insulates the heating element.",
        "খর জল নির্মাণস্থলের ক্যান্টিনের বয়লারে স্তর জমায় কেন?", ["গরম করলে দ্রবীভূত ক্যালসিয়াম হাইড্রোজেনকার্বনেট ভেঙে অদ্রাব্য ক্যালসিয়াম কার্বনেটের স্তর হয়", "খর জলে বালি থাকে", "বয়লার নিজে চক বানায়", "মৃদু জলে বেশি ক্যালসিয়াম"],
        "স্তর তাপ-উপাদানকে ঢেকে শক্তি নষ্ট করে।"),
    mcq("Which observation shows that a reaction is endothermic?", ["The temperature of the mixture falls", "The mixture gets hot", "A flame appears", "Nothing happens"], 0,
        "Instant cold packs for sprains use an endothermic reaction.",
        "কোন পর্যবেক্ষণ দেখায় যে বিক্রিয়াটা তাপগ্রাহী?", ["মিশ্রণের তাপমাত্রা কমে", "মিশ্রণ গরম হয়", "শিখা দেখা যায়", "কিছুই হয় না"],
        "মচকানোর জন্য তাৎক্ষণিক ঠান্ডা-প্যাক তাপগ্রাহী বিক্রিয়া ব্যবহার করে।"),
    mcq("Why can a reversible reaction only reach equilibrium in a closed system?", ["In an open system, products such as gases escape, so the backward reaction cannot keep pace", "Open systems have no reactants", "Air stops all reactions", "Closed systems are always hotter"], 0,
        "Limestone heated in an open kiln decomposes completely because CO2 escapes.",
        "একটা উভমুখী বিক্রিয়া কেবল বন্ধ ব্যবস্থায় সাম্যে পৌঁছায় কেন?", ["খোলা ব্যবস্থায় গ্যাসের মতো উৎপাদ বেরিয়ে যায়, তাই পশ্চাৎ বিক্রিয়া তাল রাখতে পারে না", "খোলা ব্যবস্থায় বিক্রিয়ক থাকে না", "বাতাস সব বিক্রিয়া থামায়", "বন্ধ ব্যবস্থা সবসময় গরম"],
        "খোলা চুল্লিতে চুনাপাথর গরম করলে CO2 বেরিয়ে যায়, তাই পুরোটা বিয়োজিত হয়।"),
    mcq("The Haber process makes more ammonia at low temperature, yet it runs at about 450°C. Why?", ["It is a compromise: at low temperature the reaction is far too slow", "Ammonia only forms when hot", "The catalyst melts below 450°C", "It saves fuel to run hot"], 0,
        "A reasonable yield, produced quickly, makes more ammonia per day.",
        "কম তাপমাত্রায় হেবার প্রক্রিয়ায় বেশি অ্যামোনিয়া হয়, তবু এটা প্রায় 450°C-এ চালানো হয়। কেন?", ["এটা আপস: কম তাপমাত্রায় বিক্রিয়া খুব বেশি ধীর", "অ্যামোনিয়া শুধু গরমে তৈরি হয়", "450°C-এর নিচে অনুঘটক গলে যায়", "গরমে চালালে জ্বালানি বাঁচে"],
        "দ্রুত তৈরি যুক্তিসঙ্গত ফলনে দিনে বেশি অ্যামোনিয়া হয়।"),
    mcq("A lab tests crushed concrete from an old seaside bridge for chloride. Which result shows chloride ions are present?", ["A white precipitate forms with acidified silver nitrate", "Limewater turns milky", "A squeaky pop with a lighted splint", "Bromine water turns colourless"], 0,
        "Silver chloride is white and insoluble - high chloride warns of rebar corrosion.",
        "একটা ল্যাব সমুদ্রতীরের পুরোনো সেতুর গুঁড়ো কংক্রিটে ক্লোরাইড পরীক্ষা করে। কোন ফলাফল ক্লোরাইড আয়নের উপস্থিতি দেখায়?", ["অম্লীকৃত সিলভার নাইট্রেটে সাদা অধঃক্ষেপ পড়ে", "চুনজল দুধের মতো হয়", "জ্বলন্ত কাঠিতে চিঁ শব্দ", "ব্রোমিন-জল বর্ণহীন হয়"],
        "সিলভার ক্লোরাইড সাদা আর অদ্রাব্য - বেশি ক্লোরাইড রডে মরচের সতর্কবার্তা।"),
    mcq("Why does a bridge's concrete drainage pipe sometimes get white crusty deposits at its outlet?", ["Water dissolves calcium compounds from the concrete, then they react with CO2 in air and deposit as calcium carbonate", "Birds leave salt there", "Snow never melts there", "The pipe is made of chalk"], 0,
        "This 'efflorescence' or calcite growth shows water is moving through the concrete.",
        "সেতুর কংক্রিটের নালার মুখে কখনো সাদা খসখসে স্তর জমে কেন?", ["জল কংক্রিট থেকে ক্যালসিয়াম যৌগ গলায়, তারপর বাতাসের CO2-এর সঙ্গে বিক্রিয়া করে ক্যালসিয়াম কার্বনেট হয়ে জমে", "পাখি সেখানে নুন রাখে", "সেখানে বরফ গলে না", "পাইপটা চক দিয়ে তৈরি"],
        "এই 'লবণ-ফোটা' দেখায় কংক্রিটের মধ্যে দিয়ে জল চলছে।"),
    mcq("Why is the welding of stainless steel railings done with an argon gas shield?", ["Argon is unreactive and keeps oxygen away from the hot metal", "Argon makes the weld glow", "Argon is cheaper than air", "Argon cools the weld instantly"], 0,
        "Without the shield, the hot metal would oxidise and the weld would be weak and porous.",
        "স্টেইনলেস স্টিলের রেলিং ঝালাইয়ে আর্গন-গ্যাসের আবরণ দেওয়া হয় কেন?", ["আর্গন নিষ্ক্রিয়, তাই গরম ধাতু থেকে অক্সিজেন দূরে রাখে", "আর্গন ঝালাই উজ্জ্বল করে", "আর্গন বাতাসের চেয়ে সস্তা", "আর্গন তখনই ঝালাই ঠান্ডা করে"],
        "আবরণ না থাকলে গরম ধাতু জারিত হয়ে ঝালাই দুর্বল আর ঝাঁঝরা হতো।"),
    mcq("What makes stainless steel 'stainless'?", ["Chromium in the alloy forms a thin, self-healing oxide layer", "It is painted silver", "It contains no iron", "It is kept in oil"], 0,
        "At least about 10.5% chromium is needed.",
        "স্টেইনলেস স্টিলকে কী 'মরচেহীন' করে?", ["সংকরের ক্রোমিয়াম একটা পাতলা, নিজে-সেরে-ওঠা অক্সাইড-স্তর বানায়", "রুপোলি রং করা", "এতে লোহা নেই", "তেলে রাখা হয়"],
        "অন্তত প্রায় 10.5% ক্রোমিয়াম লাগে।"),
    mcq("Why is glass fibre reinforced polymer (GFRP) sometimes used instead of steel bars in bridge decks?", ["It does not rust, so it suits salty or wet places", "It is magnetic", "It is heavier and stronger in every way", "It melts in sunlight"], 0,
        "It is less stiff than steel, so designs must allow for more bending.",
        "সেতুর পাটাতনে কখনো ইস্পাতের রডের বদলে কাচতন্তু-পলিমার (জিএফআরপি) ব্যবহার হয় কেন?", ["মরচে ধরে না, তাই নোনা বা ভেজা জায়গায় মানানসই", "চৌম্বক", "সব দিক থেকে ভারী আর শক্ত", "রোদে গলে"],
        "এটা ইস্পাতের চেয়ে কম অনমনীয়, তাই নকশায় বেশি বাঁকার জায়গা রাখতে হয়।"),
    mcq("What does a fire risk assessment say about storing gas cylinders on a bridge site?", ["Store them upright, chained, ventilated and away from heat and oil", "Lay them flat in the sun", "Keep them next to the welding bay", "Store them in a closed cabin with heaters"], 0,
        "Oxygen with oil or grease can ignite violently.",
        "নির্মাণস্থলে গ্যাস-সিলিন্ডার রাখা নিয়ে অগ্নি-ঝুঁকি মূল্যায়ন কী বলে?", ["খাড়া করে, শিকলে বেঁধে, হাওয়া-চলাচলে, তাপ আর তেল থেকে দূরে রাখো", "রোদে শুইয়ে রাখো", "ঝালাইয়ের জায়গার পাশে রাখো", "হিটারসহ বন্ধ কেবিনে রাখো"],
        "তেল বা গ্রিজের সঙ্গে অক্সিজেন প্রচণ্ডভাবে জ্বলে উঠতে পারে।"),
    mcq("What does a hazard symbol showing a flame over a circle mean?", ["Oxidising - it can make other materials burn more fiercely", "Flammable gas only", "Toxic", "Corrosive"], 0,
        "Oxygen cylinders and some cleaning chemicals carry it.",
        "বৃত্তের উপর শিখা আঁকা বিপদ-চিহ্ন কী বোঝায়?", ["জারক - অন্য জিনিসকে আরও জোরে জ্বালাতে পারে", "শুধু দাহ্য গ্যাস", "বিষাক্ত", "ক্ষয়কারী"],
        "অক্সিজেন-সিলিন্ডার আর কিছু পরিষ্কারের রাসায়নিকে এটা থাকে।"),
    mcq("A worker spills strong acid on their skin. What is the first thing to do?", ["Rinse with plenty of cool running water for a long time and get help", "Rub it with a dry cloth", "Add alkali powder to it", "Ignore it if it does not hurt"], 0,
        "Water dilutes and washes away the acid; then follow the safety data sheet.",
        "একজন কর্মীর চামড়ায় কড়া অ্যাসিড পড়ল। প্রথমে কী করতে হবে?", ["অনেকক্ষণ ধরে প্রচুর ঠান্ডা চলমান জলে ধুয়ে সাহায্য ডাকো", "শুকনো কাপড়ে ঘষো", "উপরে ক্ষারের গুঁড়ো দাও", "ব্যথা না করলে উপেক্ষা করো"],
        "জল অ্যাসিড পাতলা করে ধুয়ে দেয়; তারপর নিরাপত্তা-তথ্যপত্র মেনে চলো।"),
)
