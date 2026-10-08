"""Class 11 - Chemistry (Senior Engineer): electron configuration, periodic trends, shapes of
molecules and bond angles, bond polarity and intermolecular forces, the ideal gas equation,
Hess's law, equilibrium constants, pH of strong bases, standard electrode potentials and cell
voltages, and the electrochemistry of corrosion, galvanising and cathodic protection."""
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


def _same(q_en, q_bn, opts, ex_en, ex_bn):
    return mcq(q_en, opts, 0, ex_en, q_bn, opts, ex_bn)


def _c(x):
    x = round(x, 3)
    return int(x) if x == int(x) else x


def pvnrt(p_kpa, v_dm3, t_k, what_en, what_bn):
    n = _c(p_kpa * 1000 * v_dm3 / 1000 / (8.31 * t_k))
    return _n(f"A cylinder of {what_en} holds {v_dm3:g} dm³ at {p_kpa:,} kPa and {t_k} K. How many moles of gas does it contain? (pV = nRT, R = 8.31 J/mol/K)",
              f"একটা {what_bn}-সিলিন্ডারে {t_k} K-এ {p_kpa:,} কিলোপ্যাসকেল চাপে {v_dm3:g} dm³ গ্যাস। কত মোল গ্যাস আছে? (pV = nRT, R = 8.31 J/mol/K)", n,
              f"n = pV ÷ RT = ({p_kpa * 1000:,} Pa x {v_dm3 / 1000:g} m³) ÷ (8.31 x {t_k}) = {n:g} mol. Remember to use pascals and cubic metres.",
              f"n = pV ÷ RT = ({p_kpa * 1000:,} Pa x {v_dm3 / 1000:g} m³) ÷ (8.31 x {t_k}) = {n:g} মোল। প্যাসকেল আর ঘনমিটার ব্যবহার করতে ভুলো না।",
              (_c(n * 1000), _c(n / 10), _c(p_kpa * v_dm3 / t_k)), " mol", " মোল")


def config(el_en, el_bn, z, right, wrongs):
    return _same(f"What is the electron arrangement (by shells) of {el_en}, atomic number {z}?",
                 f"পারমাণবিক সংখ্যা {z}-এর {el_bn}-এর ইলেকট্রন-বিন্যাস (কক্ষ অনুযায়ী) কী?", [right, *wrongs],
                 f"Fill shells in order (2, then 8, then 8 for these elements): {right}, adding to {z}.",
                 f"ক্রমে কক্ষ ভরো (এই মৌলগুলোর জন্য 2, তারপর 8, তারপর 8): {right}, যোগফল {z}।")


POT = {"Zn": -0.76, "Fe": -0.44, "Cu": 0.34, "Mg": -2.37, "Al": -1.66, "Ag": 0.80, "Ni": -0.25}
NAMES = {"Zn": ("zinc", "দস্তা"), "Fe": ("iron", "লোহা"), "Cu": ("copper", "তামা"), "Mg": ("magnesium", "ম্যাগনেসিয়াম"),
         "Al": ("aluminium", "অ্যালুমিনিয়াম"), "Ag": ("silver", "রুপো"), "Ni": ("nickel", "নিকেল")}


def ecell(a, b):
    lo, hi = sorted((a, b), key=lambda m: POT[m])
    e = _c(POT[hi] - POT[lo])
    return _n(f"A cell is made from {NAMES[a][0]} (E° = {POT[a]:+.2f} V) and {NAMES[b][0]} (E° = {POT[b]:+.2f} V) half-cells. What is the standard cell voltage?",
              f"{NAMES[a][1]} (E° = {POT[a]:+.2f} V) আর {NAMES[b][1]} (E° = {POT[b]:+.2f} V) অর্ধকোষ দিয়ে একটা কোষ তৈরি। প্রমাণ কোষ-ভোল্টেজ কত?", e,
              f"E°cell = E°(more positive) - E°(more negative) = {POT[hi]:+.2f} - ({POT[lo]:+.2f}) = {e:g} V. {NAMES[lo][0].capitalize()} is the negative electrode and corrodes.",
              f"E°কোষ = E°(বেশি ধনাত্মক) - E°(বেশি ঋণাত্মক) = {POT[hi]:+.2f} - ({POT[lo]:+.2f}) = {e:g} V। {NAMES[lo][1]} ঋণাত্মক তড়িদ্বার আর ক্ষয়ে যায়।",
              (_c(abs(POT[a] + POT[b])) if _c(abs(POT[a] + POT[b])) != e else _c(e + 0.5), _c(abs(POT[hi])) if _c(abs(POT[hi])) != e else _c(e / 2), _c(e * 2)), " V")


def kc(a, b, c):
    k = _c(c * c / (a * b))
    return _n(f"For A + B ⇌ 2C at equilibrium, [A] = {a:g}, [B] = {b:g} and [C] = {c:g} mol/dm³. What is Kc?",
              f"A + B ⇌ 2C সাম্যাবস্থায় [A] = {a:g}, [B] = {b:g} আর [C] = {c:g} মোল/dm³। Kc কত?", k,
              f"Kc = [C]² ÷ ([A][B]) = {c:g}² ÷ ({a:g} x {b:g}) = {k:g}. A large Kc means products are favoured.",
              f"Kc = [C]² ÷ ([A][B]) = {c:g}² ÷ ({a:g} x {b:g}) = {k:g}। বড় Kc মানে উৎপাদের দিকে ঝোঁক।",
              (_c(c / (a * b)), _c(a * b / (c * c)), _c(k * 2)))


def hess(h1, h2, what_en, what_bn):
    r = h1 + h2
    o = []
    for v in (r, h1 - h2, h2 - h1, -r):
        if v not in o:
            o.append(v)
    while len(o) < 4:
        o.append(o[-1] + 50)
    return mcq(f"{what_en} can happen in two steps with ΔH = {h1:+,} kJ/mol and ΔH = {h2:+,} kJ/mol. What is the overall enthalpy change?",
               [f"{v:+,} kJ/mol" for v in o], 0,
               f"Hess's law: the total enthalpy change is the same by any route, so ΔH = {h1:+,} + ({h2:+,}) = {r:+,} kJ/mol.",
               f"{what_bn} দুই ধাপে ঘটতে পারে, ΔH = {h1:+,} kJ/মোল আর ΔH = {h2:+,} kJ/মোল। সামগ্রিক এনথ্যালপি-পরিবর্তন কত?",
               [f"{v:+,} kJ/মোল" for v in o],
               f"হেসের সূত্র: যেকোনো পথে মোট এনথ্যালপি-পরিবর্তন একই, তাই ΔH = {h1:+,} + ({h2:+,}) = {r:+,} kJ/মোল।")


def phbase(power):
    ph = 14 - power
    o = [str(ph), str(power), str(14 + power), str(ph - 1)]
    return mcq(f"A sodium hydroxide cleaner has [OH⁻] = 10⁻{power} mol/dm³. What is its pH? (pH + pOH = 14)", o, 0,
               f"pOH = {power}, so pH = 14 - {power} = {ph}.",
               f"একটা সোডিয়াম হাইড্রক্সাইড-পরিষ্কারকে [OH⁻] = 10⁻{power} মোল/dm³। এর pH কত? (pH + pOH = 14)", o,
               f"pOH = {power}, তাই pH = 14 - {power} = {ph}। ক্ষার যত তীব্র, pH তত বেশি।")


SHAPES = {
    "CH4": ("methane", "মিথেন", "109.5°", ["90°", "120°", "180°"], "4 bonding pairs repel equally: tetrahedral.", "4টি বন্ধন-জোড় সমান বিকর্ষণ করে: চতুস্তলক।"),
    "NH3": ("ammonia", "অ্যামোনিয়া", "107°", ["109.5°", "90°", "120°"], "3 bonding pairs and 1 lone pair; the lone pair repels more, squeezing the angle.", "3টি বন্ধন-জোড় আর 1টি নিঃসঙ্গ জোড়; নিঃসঙ্গ জোড় বেশি বিকর্ষণ করে কোণ চাপে।"),
    "H2O": ("water", "জল", "104.5°", ["109.5°", "180°", "120°"], "2 bonding pairs and 2 lone pairs: a bent shape.", "2টি বন্ধন-জোড় আর 2টি নিঃসঙ্গ জোড়: বাঁকা আকার।"),
    "CO2": ("carbon dioxide", "কার্বন ডাইঅক্সাইড", "180°", ["120°", "109.5°", "90°"], "Two double bonds as far apart as possible: linear.", "দুটো দ্বিবন্ধন যত দূরে সম্ভব: রৈখিক।"),
}


def angle(f):
    name_en, name_bn, right, wrongs, why_en, why_bn = SHAPES[f]
    return _same(f"What is the bond angle in a molecule of {name_en} ({f})?", f"{name_bn} ({f}) অণুর বন্ধন-কোণ কত?",
                 [right, *wrongs], why_en, why_bn)


ITEMS = (
    pvnrt(200, 10, 300, "argon shielding gas", "আর্গন আবরণ-গ্যাস"), pvnrt(1000, 50, 300, "oxygen", "অক্সিজেন"),
    pvnrt(500, 20, 290, "nitrogen", "নাইট্রোজেন"), pvnrt(800, 40, 320, "acetylene", "অ্যাসিটিলিন"),
    config("calcium", "ক্যালসিয়াম", 20, "2, 8, 8, 2", ["2, 8, 10", "2, 18", "8, 8, 4"]),
    config("chlorine", "ক্লোরিন", 17, "2, 8, 7", ["2, 7, 8", "8, 8, 1", "2, 15"]),
    config("aluminium", "অ্যালুমিনিয়াম", 13, "2, 8, 3", ["2, 11", "8, 5", "3, 8, 2"]),
    config("sodium", "সোডিয়াম", 11, "2, 8, 1", ["2, 9", "1, 8, 2", "8, 3"]),
    ecell("Zn", "Cu"), ecell("Fe", "Cu"), ecell("Zn", "Fe"), ecell("Mg", "Fe"), ecell("Al", "Fe"), ecell("Fe", "Ag"),
    kc(0.2, 0.5, 1.0), kc(0.1, 0.4, 0.6), kc(1, 2, 4), kc(0.5, 0.5, 0.25),
    hess(-110, -283, "Burning carbon to carbon dioxide", "কার্বন পুড়িয়ে কার্বন ডাইঅক্সাইড"), hess(+178, -64, "Making slaked lime from limestone", "চুনাপাথর থেকে কলিচুন"),
    hess(-286, +44, "Forming water vapour from hydrogen", "হাইড্রোজেন থেকে জলীয় বাষ্প"), hess(-824, +200, "A two-step iron oxide reduction", "দুই ধাপে আয়রন অক্সাইড বিজারণ"),
    phbase(1), phbase(2), phbase(3), phbase(4),
    angle("CH4"), angle("NH3"), angle("H2O"), angle("CO2"),
    pvnrt(300, 25, 310, "carbon dioxide", "কার্বন ডাইঅক্সাইড"), pvnrt(1500, 10, 300, "compressed air", "চাপা বাতাস"),
    ecell("Ni", "Cu"), ecell("Mg", "Cu"), kc(0.4, 0.4, 0.8), kc(0.3, 0.6, 0.9),
    hess(-394, +283, "Making carbon monoxide by a two-step route", "দুই ধাপে কার্বন মনোক্সাইড তৈরি"), hess(+92, -46, "A two-step ammonia route", "দুই ধাপে অ্যামোনিয়ার পথ"),
    phbase(5), ecell("Al", "Cu"), kc(0.2, 0.2, 0.6), config("magnesium", "ম্যাগনেসিয়াম", 12, "2, 8, 2", ["2, 10", "8, 4", "2, 2, 8"]),
    config("argon", "আর্গন", 18, "2, 8, 8", ["2, 16", "8, 8, 2", "2, 8, 6, 2"]),
    config("potassium", "পটাশিয়াম", 19, "2, 8, 8, 1", ["2, 8, 9", "2, 17", "1, 8, 8, 2"]),
    mcq("What is an 'orbital'?", ["A region around the nucleus where an electron is likely to be found, holding up to 2 electrons", "The path of a planet", "A type of bond", "The nucleus itself"], 0,
        "s, p and d orbitals have different shapes and energies.",
        "'কক্ষক' (অরবিটাল) কী?", ["কেন্দ্রকের চারপাশের যে অঞ্চলে ইলেকট্রন পাওয়ার সম্ভাবনা বেশি, সর্বোচ্চ 2টি ইলেকট্রন ধরে", "গ্রহের পথ", "এক রকম বন্ধন", "কেন্দ্রক নিজেই"],
        "s, p আর d কক্ষকের আকার আর শক্তি আলাদা।"),
    mcq("What is the electron configuration of iron (Z = 26) in s, p, d notation?", ["1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁶", "1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁸", "2, 8, 16", "1s² 2s² 2p¹⁰ 3s¹²"], 0,
        "4s fills before 3d; iron's partly filled d sub-shell explains its colours and catalytic activity.",
        "s, p, d চিহ্নে লোহার (Z = 26) ইলেকট্রন-বিন্যাস কী?", ["1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁶", "1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁸", "2, 8, 16", "1s² 2s² 2p¹⁰ 3s¹²"],
        "3d-এর আগে 4s ভরে; লোহার আংশিক ভরা d উপকক্ষ এর রং আর অনুঘটক-ক্ষমতা ব্যাখ্যা করে।"),
    mcq("What is 'first ionisation energy'?", ["The energy needed to remove one electron from each atom in a mole of gaseous atoms", "The energy released when a bond forms", "The energy of a photon", "The energy to melt a metal"], 0,
        "It generally rises across a period and falls down a group.",
        "'প্রথম আয়নন-শক্তি' কী?", ["এক মোল গ্যাসীয় পরমাণুর প্রতিটা থেকে একটা ইলেকট্রন সরাতে লাগা শক্তি", "বন্ধন গড়ার সময় বেরোনো শক্তি", "ফোটনের শক্তি", "ধাতু গলানোর শক্তি"],
        "সাধারণত পর্যায়ে ডানে বাড়ে আর শ্রেণিতে নিচে কমে।"),
    mcq("Why do reactive metals like sodium have low ionisation energies?", ["Their outer electron is far from the nucleus and well shielded, so it is easily removed", "They have no electrons", "Their nucleus is very large and attractive", "They are liquids"], 0,
        "Easily lost electrons mean high reactivity - and fast corrosion.",
        "সোডিয়ামের মতো সক্রিয় ধাতুর আয়নন-শক্তি কম কেন?", ["বাইরের ইলেকট্রন কেন্দ্রক থেকে দূরে আর ভালোভাবে আড়ালে, তাই সহজে সরানো যায়", "এদের ইলেকট্রন নেই", "কেন্দ্রক খুব বড় আর আকর্ষক", "এরা তরল"],
        "সহজে ইলেকট্রন হারানো মানে বেশি সক্রিয়তা - আর দ্রুত ক্ষয়।"),
    mcq("What is 'electronegativity'?", ["The ability of an atom to attract the shared electrons in a covalent bond", "The charge on an electron", "The number of neutrons", "The energy to boil a liquid"], 0,
        "Fluorine is the most electronegative element.",
        "'তড়িৎঋণাত্মকতা' কী?", ["সমযোজী বন্ধনে ভাগ-করা ইলেকট্রনকে আকর্ষণের পরমাণুর ক্ষমতা", "ইলেকট্রনের আধান", "নিউট্রনের সংখ্যা", "তরল ফোটানোর শক্তি"],
        "ফ্লুরিন সবচেয়ে বেশি তড়িৎঋণাত্মক মৌল।"),
    mcq("Which bond is the most polar?", ["O-H", "C-H", "H-H", "C-C"], 0,
        "Oxygen is much more electronegative than hydrogen, so the electrons are pulled towards O.",
        "কোন বন্ধন সবচেয়ে বেশি পোলার?", ["O-H", "C-H", "H-H", "C-C"],
        "অক্সিজেন হাইড্রোজেনের চেয়ে অনেক বেশি তড়িৎঋণাত্মক, তাই ইলেকট্রন O-এর দিকে টানে।"),
    mcq("What is 'hydrogen bonding'?", ["A strong intermolecular attraction between H on N, O or F and a lone pair on another N, O or F", "A covalent bond in H2", "An ionic bond", "Bonding in metals"], 0,
        "It gives water its high boiling point and helps cement paste hold together.",
        "'হাইড্রোজেন-বন্ধন' কী?", ["N, O বা F-এর সঙ্গে যুক্ত H আর অন্য N, O বা F-এর নিঃসঙ্গ জোড়ের মধ্যে জোরালো আন্তঃআণবিক আকর্ষণ", "H2-এর সমযোজী বন্ধন", "আয়নীয় বন্ধন", "ধাতুর বন্ধন"],
        "এটা জলকে বেশি স্ফুটনাঙ্ক দেয় আর সিমেন্ট-মণ্ডকে জুড়ে থাকতে সাহায্য করে।"),
    mcq("Why does water have a much higher boiling point than methane, although both are small molecules?", ["Water molecules are held by hydrogen bonds, which need more energy to break", "Water is heavier than methane by far", "Methane has hydrogen bonds", "Water is ionic"], 0,
        "Methane has only weak London (van der Waals) forces.",
        "দুটোই ছোট অণু হলেও মিথেনের চেয়ে জলের স্ফুটনাঙ্ক অনেক বেশি কেন?", ["জলের অণু হাইড্রোজেন-বন্ধনে আটকে থাকে, যা ভাঙতে বেশি শক্তি লাগে", "জল মিথেনের চেয়ে অনেক ভারী", "মিথেনে হাইড্রোজেন-বন্ধন আছে", "জল আয়নীয়"],
        "মিথেনে শুধু দুর্বল লন্ডন (ভ্যান ডার ওয়ালস) বল।"),
    mcq("What are London (van der Waals) forces?", ["Weak attractions between temporary dipoles in all molecules", "Strong ionic bonds", "Bonds in metals only", "Magnetic forces"], 0,
        "They grow with the size of the molecule - so bitumen is solid while methane is a gas.",
        "লন্ডন (ভ্যান ডার ওয়ালস) বল কী?", ["সব অণুতে অস্থায়ী দ্বিমেরুর মধ্যে দুর্বল আকর্ষণ", "জোরালো আয়নীয় বন্ধন", "শুধু ধাতুর বন্ধন", "চৌম্বক বল"],
        "অণুর মাপের সঙ্গে বাড়ে - তাই বিটুমেন কঠিন আর মিথেন গ্যাস।"),
    mcq("What does VSEPR theory say about electron pairs around a central atom?", ["They repel each other and arrange themselves as far apart as possible", "They attract each other", "They always lie in a straight line", "They have no effect on shape"], 0,
        "Lone pairs repel more strongly than bonding pairs.",
        "কেন্দ্রীয় পরমাণুর চারপাশের ইলেকট্রন-জোড় নিয়ে ভিএসইপিআর তত্ত্ব কী বলে?", ["পরস্পরকে বিকর্ষণ করে যত দূরে সম্ভব সাজে", "পরস্পরকে আকর্ষণ করে", "সবসময় সরলরেখায় থাকে", "আকারে প্রভাব নেই"],
        "নিঃসঙ্গ জোড় বন্ধন-জোড়ের চেয়ে বেশি বিকর্ষণ করে।"),
    mcq("When using the ideal gas equation, in which unit must temperature be entered?", ["Kelvin", "Degrees Celsius", "Degrees Fahrenheit", "Any unit works"], 0,
        "Gas behaviour depends on absolute temperature; 0°C is 273 K, not zero.",
        "আদর্শ গ্যাসের সমীকরণ ব্যবহারের সময় তাপমাত্রা কোন এককে দিতে হয়?", ["কেলভিন", "ডিগ্রি সেলসিয়াস", "ডিগ্রি ফারেনহাইট", "যেকোনো একক চলে"],
        "গ্যাসের আচরণ পরম তাপমাত্রার উপর নির্ভর করে; 0°C মানে 273 K, শূন্য নয়।"),
    mcq("What is the 'partial pressure' of a gas in a mixture?", ["The pressure it would exert if it alone filled the container", "The total pressure", "Half the total pressure always", "The pressure of the container walls"], 0,
        "Dalton's law: partial pressures add up to the total pressure.",
        "মিশ্রণে একটা গ্যাসের 'আংশিক চাপ' কী?", ["পাত্র একা ভরালে সেই গ্যাস যে চাপ দিত", "মোট চাপ", "সবসময় মোট চাপের অর্ধেক", "পাত্রের দেয়ালের চাপ"],
        "ডাল্টনের সূত্র: আংশিক চাপগুলো যোগ করলে মোট চাপ।"),
    mcq("Why do many steel-welding shielding gases mix argon with a little carbon dioxide?", ["The CO2 improves arc stability and weld penetration while argon protects the weld pool", "CO2 makes the weld colourful", "Argon alone is illegal", "CO2 cools the welder"], 0,
        "Pure argon is used for aluminium and stainless steel.",
        "ইস্পাত-ঝালাইয়ের অনেক আবরণ-গ্যাসে আর্গনের সঙ্গে অল্প কার্বন ডাইঅক্সাইড মেশানো হয় কেন?", ["CO2 আর্কের স্থিতি আর ঝালাইয়ের গভীরতা বাড়ায়, আর আর্গন গলিত ধাতু রক্ষা করে", "CO2 ঝালাই রঙিন করে", "শুধু আর্গন বেআইনি", "CO2 ঝালাইকারকে ঠান্ডা করে"],
        "অ্যালুমিনিয়াম আর স্টেইনলেস স্টিলে বিশুদ্ধ আর্গন ব্যবহার হয়।"),
    mcq("What is the 'chloride threshold' for steel in concrete?", ["The chloride level at the steel above which the passive film breaks down and corrosion starts", "The maximum salt in drinking water", "The temperature at which salt melts", "The strength of concrete"], 0,
        "Engineers measure chloride profiles in cores to predict when corrosion will begin.",
        "কংক্রিটে ইস্পাতের 'ক্লোরাইড-সীমা' কী?", ["ইস্পাতের কাছে ক্লোরাইডের যে মাত্রার উপরে নিষ্ক্রিয় স্তর ভেঙে ক্ষয় শুরু হয়", "খাবার জলে সর্বোচ্চ লবণ", "যে তাপমাত্রায় লবণ গলে", "কংক্রিটের শক্তি"],
        "ক্ষয় কবে শুরু হবে আন্দাজ করতে প্রকৌশলীরা কোরে ক্লোরাইডের বিন্যাস মাপেন।"),
    mcq("What does a 'corrosion inhibitor' such as calcium nitrite do in bridge concrete?", ["It helps keep the passive film on the steel stable even when some chloride arrives", "It makes concrete set faster only", "It colours the concrete", "It removes all water"], 0,
        "It is added to the mix for structures exposed to sea spray or de-icing salt.",
        "সেতুর কংক্রিটে ক্যালসিয়াম নাইট্রাইটের মতো 'ক্ষয়-রোধক' কী করে?", ["কিছু ক্লোরাইড এলেও ইস্পাতের নিষ্ক্রিয় স্তর স্থির রাখতে সাহায্য করে", "শুধু কংক্রিট দ্রুত জমায়", "কংক্রিট রঙিন করে", "সব জল সরায়"],
        "সমুদ্রের ছিটে বা বরফ-গলানো নুনের সংস্পর্শে থাকা কাঠামোর মিশ্রণে যোগ করা হয়।"),
    mcq("Why are concrete bridge decks sometimes treated with silane?", ["Silane soaks in and makes the pores water-repellent, slowing chloride entry while letting vapour out", "To make the deck shiny", "To glue the asphalt", "To colour the concrete"], 0,
        "It is a cheap way to extend the life of decks and parapets.",
        "কংক্রিটের সেতু-পাটাতনে কখনো সাইলেন দেওয়া হয় কেন?", ["সাইলেন ভেতরে ঢুকে ছিদ্রকে জল-বিকর্ষী করে, বাষ্প বেরোতে দেয় অথচ ক্লোরাইডের প্রবেশ ধীর করে", "পাটাতন চকচকে করতে", "পিচ আঠা দিয়ে জুড়তে", "কংক্রিট রঙিন করতে"],
        "পাটাতন আর রেলিংয়ের আয়ু বাড়ানোর সস্তা উপায়।"),
    mcq("Why are fluoropolymer top coats used on some landmark steel bridges?", ["Very strong C-F bonds resist breakdown by sunlight, so colour and gloss last for decades", "They are the cheapest paints", "They conduct electricity", "They dissolve in rain"], 0,
        "Longer repainting cycles save money and disruption.",
        "কিছু বিখ্যাত ইস্পাতের সেতুতে ফ্লুরোপলিমারের শেষ পোঁচ ব্যবহার হয় কেন?", ["খুব শক্ত C-F বন্ধন সূর্যালোকে ভাঙন রোধ করে, তাই রং আর ঔজ্জ্বল্য কয়েক দশক টেকে", "সবচেয়ে সস্তা রং", "বিদ্যুৎ পরিবহন করে", "বৃষ্টিতে গলে"],
        "লম্বা সময় অন্তর রং করায় টাকা আর ব্যাঘাত বাঁচে।"),
    mcq("What is the electrolyte in the corrosion of steel bars inside concrete?", ["The alkaline pore water in the concrete", "The steel itself", "Dry air", "The asphalt surface"], 0,
        "Dry concrete corrodes reinforcement very slowly because ions cannot move easily.",
        "কংক্রিটের ভেতরে ইস্পাতের রডের ক্ষয়ে তড়িৎবিশ্লেষ্য কী?", ["কংক্রিটের ক্ষারীয় ছিদ্র-জল", "ইস্পাত নিজেই", "শুকনো বাতাস", "পিচের তল"],
        "শুকনো কংক্রিটে আয়ন সহজে চলতে পারে না, তাই রড খুব ধীরে ক্ষয়ে যায়।"),
    mcq("Why do real gases depart from ideal behaviour at very high pressure?", ["Molecules are squeezed close, so their own volume and attractions matter", "They become liquids instantly", "Temperature drops to zero", "They stop moving"], 0,
        "High-pressure gas cylinders are designed with this in mind.",
        "খুব উচ্চ চাপে আসল গ্যাস আদর্শ আচরণ থেকে সরে কেন?", ["অণুরা কাছাকাছি চাপা পড়ে, তাই তাদের নিজের আয়তন আর আকর্ষণ গুরুত্বপূর্ণ হয়", "তখনই তরল হয়ে যায়", "তাপমাত্রা শূন্যে নামে", "চলা বন্ধ করে"],
        "উচ্চচাপের গ্যাস-সিলিন্ডার এটা মাথায় রেখে নকশা হয়।"),
    mcq("What does Hess's law state?", ["The total enthalpy change of a reaction is the same whichever route is taken", "Energy can be created", "Reactions always release heat", "Enthalpy depends on speed"], 0,
        "It lets chemists find enthalpy changes that cannot be measured directly.",
        "হেসের সূত্র কী বলে?", ["যে পথেই হোক বিক্রিয়ার মোট এনথ্যালপি-পরিবর্তন একই", "শক্তি তৈরি করা যায়", "বিক্রিয়া সবসময় তাপ ছাড়ে", "এনথ্যালপি গতির উপর নির্ভর করে"],
        "সরাসরি মাপা যায় না এমন এনথ্যালপি-পরিবর্তন বের করতে সাহায্য করে।"),
    mcq("What is the 'standard enthalpy of formation'?", ["The enthalpy change when 1 mole of a compound forms from its elements in their standard states", "The energy to melt a solid", "The energy of a photon", "The heat from burning any fuel"], 0,
        "For elements in their standard states it is zero by definition.",
        "'প্রমাণ গঠন-এনথ্যালপি' কী?", ["প্রমাণ অবস্থায় মৌল থেকে 1 মোল যৌগ তৈরিতে এনথ্যালপি-পরিবর্তন", "কঠিন গলানোর শক্তি", "ফোটনের শক্তি", "যেকোনো জ্বালানি পোড়ানোর তাপ"],
        "প্রমাণ অবস্থার মৌলের জন্য সংজ্ঞা অনুযায়ী এটা শূন্য।"),
    mcq("What does a very large equilibrium constant (Kc) tell you?", ["The equilibrium lies far to the right - mostly products", "Mostly reactants remain", "The reaction is very fast", "The reaction cannot happen"], 0,
        "Kc says how far, not how fast.",
        "খুব বড় সাম্য-ধ্রুবক (Kc) কী জানায়?", ["সাম্যাবস্থা অনেক ডানদিকে - বেশিরভাগ উৎপাদ", "বেশিরভাগ বিক্রিয়ক থেকে যায়", "বিক্রিয়া খুব দ্রুত", "বিক্রিয়া ঘটতেই পারে না"],
        "Kc বলে কতদূর, কত দ্রুত নয়।"),
    mcq("Which change alters the value of Kc for a reaction?", ["Changing the temperature", "Adding a catalyst", "Changing the concentration of a reactant", "Changing the pressure of the container only"], 0,
        "Concentration and pressure shift the position, but only temperature changes Kc.",
        "কোন বদল বিক্রিয়ার Kc-এর মান বদলায়?", ["তাপমাত্রা বদলানো", "অনুঘটক যোগ করা", "বিক্রিয়কের গাঢ়ত্ব বদলানো", "শুধু পাত্রের চাপ বদলানো"],
        "গাঢ়ত্ব আর চাপ অবস্থান সরায়, কিন্তু শুধু তাপমাত্রা Kc বদলায়।"),
    mcq("What is a 'Brønsted-Lowry acid'?", ["A proton (H⁺) donor", "A proton acceptor", "An electron donor", "Any salt"], 0,
        "A base is a proton acceptor.",
        "'ব্রনস্টেড-লাউরি অ্যাসিড' কী?", ["প্রোটন (H⁺) দাতা", "প্রোটন গ্রহীতা", "ইলেকট্রন দাতা", "যেকোনো লবণ"],
        "ক্ষার হলো প্রোটন গ্রহীতা।"),
    mcq("What does the 'standard electrode potential' (E°) of a metal tell you?", ["How readily it loses electrons compared with hydrogen - more negative means more easily oxidised", "Its melting point", "Its density", "Its price"], 0,
        "Zinc (-0.76 V) corrodes before iron (-0.44 V) - the basis of galvanising.",
        "কোনো ধাতুর 'প্রমাণ তড়িদ্বার-বিভব' (E°) কী জানায়?", ["হাইড্রোজেনের তুলনায় কত সহজে ইলেকট্রন হারায় - বেশি ঋণাত্মক মানে সহজে জারিত হয়", "এর গলনাঙ্ক", "এর ঘনত্ব", "এর দাম"],
        "দস্তা (-0.76 V) লোহার (-0.44 V) আগে ক্ষয়ে যায় - গ্যালভানাইজিংয়ের ভিত্তি।"),
    mcq("What is the reference electrode for standard electrode potentials?", ["The standard hydrogen electrode, defined as 0.00 V", "A copper electrode", "A zinc electrode", "A battery"], 0,
        "All other potentials are measured against it.",
        "প্রমাণ তড়িদ্বার-বিভবের নির্দেশক তড়িদ্বার কোনটা?", ["প্রমাণ হাইড্রোজেন-তড়িদ্বার, সংজ্ঞায় 0.00 V", "একটা তামার তড়িদ্বার", "একটা দস্তার তড়িদ্বার", "একটা ব্যাটারি"],
        "অন্য সব বিভব এর সাপেক্ষে মাপা হয়।"),
    mcq("In a corrosion cell on a steel girder, what happens at the anodic areas?", ["Iron is oxidised: Fe -> Fe²⁺ + 2e⁻", "Oxygen is reduced", "Hydrogen is made", "Nothing happens"], 0,
        "Rust forms where these iron ions meet hydroxide ions and oxygen.",
        "ইস্পাতের গার্ডারের ক্ষয়-কোষে অ্যানোড অঞ্চলে কী ঘটে?", ["লোহা জারিত হয়: Fe -> Fe²⁺ + 2e⁻", "অক্সিজেন বিজারিত হয়", "হাইড্রোজেন তৈরি হয়", "কিছুই না"],
        "এই লোহার আয়ন হাইড্রক্সাইড আয়ন আর অক্সিজেনের সঙ্গে মিলে মরচে হয়।"),
    mcq("What happens at the cathodic areas of a corrosion cell in neutral water?", ["Oxygen and water gain electrons: O2 + 2H2O + 4e⁻ -> 4OH⁻", "Iron dissolves", "Zinc forms", "Chlorine is released"], 0,
        "That is why oxygen and water are both needed for rusting.",
        "নিরপেক্ষ জলে ক্ষয়-কোষের ক্যাথোড অঞ্চলে কী ঘটে?", ["অক্সিজেন আর জল ইলেকট্রন নেয়: O2 + 2H2O + 4e⁻ -> 4OH⁻", "লোহা গলে", "দস্তা তৈরি হয়", "ক্লোরিন বেরোয়"],
        "তাই মরচের জন্য অক্সিজেন আর জল দুটোই লাগে।"),
    mcq("Why does rust often form under the edge of a water droplet rather than at its centre?", ["The edge gets more oxygen and acts as the cathode; the oxygen-poor centre becomes the anode and pits", "The centre is hotter", "Rust avoids water", "It is random"], 0,
        "This 'differential aeration' explains pitting in crevices and under dirt.",
        "মরচে প্রায়ই জলবিন্দুর মাঝখানে নয়, কিনারার নিচে ধরে কেন?", ["কিনারা বেশি অক্সিজেন পায় আর ক্যাথোড হয়; কম-অক্সিজেনের মাঝখান অ্যানোড হয়ে গর্ত হয়", "মাঝখান বেশি গরম", "মরচে জল এড়ায়", "এলোমেলো"],
        "এই 'অসম বায়ুপ্রবাহ' ফাটলে আর ময়লার নিচে গর্ত-ক্ষয় ব্যাখ্যা করে।"),
    mcq("Why are crevices and bolted joints on bridges hot spots for corrosion?", ["Trapped water there is low in oxygen, making those spots anodic so they corrode", "Bolts are made of gold", "Crevices are always dry", "Paint is thicker there"], 0,
        "Sealing joints and good drainage prevent crevice corrosion.",
        "সেতুর ফাঁক আর বল্টু-জোড় ক্ষয়ের বিশেষ জায়গা কেন?", ["সেখানে আটকে থাকা জলে অক্সিজেন কম, তাই জায়গাগুলো অ্যানোডিক হয়ে ক্ষয়ে যায়", "বল্টু সোনার", "ফাঁক সবসময় শুকনো", "সেখানে রং বেশি পুরু"],
        "জোড় সিল করা আর ভালো জলনিকাশ ফাঁক-ক্ষয় আটকায়।"),
    mcq("What is 'galvanic corrosion'?", ["When two different metals touch in an electrolyte, the more reactive one corrodes faster", "Corrosion caused by lightning", "Rust on galvanised steel only", "Corrosion in dry air"], 0,
        "Steel bolts in aluminium parapets need insulating washers.",
        "'গ্যালভানিক ক্ষয়' কী?", ["তড়িৎবিশ্লেষ্যে দুটো আলাদা ধাতু ছুঁলে বেশি সক্রিয়টা দ্রুত ক্ষয়ে যায়", "বাজ থেকে ক্ষয়", "শুধু গ্যালভানাইজড ইস্পাতে মরচে", "শুকনো বাতাসে ক্ষয়"],
        "অ্যালুমিনিয়ামের রেলিংয়ে ইস্পাতের বল্টুতে অন্তরক ওয়াশার লাগে।"),
    mcq("Why is hot-dip galvanising better than a thin zinc electroplate for a bridge in the open air?", ["The thick zinc layer, bonded as zinc-iron alloy layers, lasts decades and protects cut edges", "Electroplate is thicker", "Galvanising uses gold", "It is always cheaper by far"], 0,
        "Hot-dip coatings are typically 85 µm or more thick.",
        "খোলা বাতাসে সেতুর জন্য পাতলা দস্তা-তড়িৎলেপের চেয়ে গরম-ডুবানো গ্যালভানাইজিং ভালো কেন?", ["দস্তা-লোহার সংকর-স্তরে আটকানো পুরু দস্তার স্তর কয়েক দশক টেকে আর কাটা ধারও রক্ষা করে", "তড়িৎলেপ বেশি পুরু", "গ্যালভানাইজিংয়ে সোনা লাগে", "সবসময় অনেক সস্তা"],
        "গরম-ডুবানো আবরণ সাধারণত 85 µm বা বেশি পুরু।"),
    mcq("What is a 'passive' metal surface, such as on stainless steel?", ["A thin, stable oxide film that stops further corrosion and repairs itself", "A surface with no atoms", "A painted surface", "A rusty surface"], 0,
        "Chlorides can break the film locally, causing pitting.",
        "স্টেইনলেস স্টিলের মতো 'নিষ্ক্রিয়' ধাতব তল কী?", ["পাতলা, স্থায়ী অক্সাইড-স্তর যা আরও ক্ষয় থামায় আর নিজে সেরে ওঠে", "পরমাণুহীন তল", "রং-করা তল", "মরচে-ধরা তল"],
        "ক্লোরাইড স্থানীয়ভাবে স্তর ভেঙে গর্ত-ক্ষয় ঘটাতে পারে।"),
    mcq("Which grade of stainless steel resists chloride pitting better near the sea?", ["Grade 316, which contains molybdenum", "Grade 304 without molybdenum", "Mild steel", "Cast iron"], 0,
        "Molybdenum strengthens the passive film against chlorides.",
        "সমুদ্রের কাছে কোন মানের স্টেইনলেস স্টিল ক্লোরাইডের গর্ত-ক্ষয় ভালো রোধ করে?", ["গ্রেড 316, যাতে মলিবডেনাম আছে", "মলিবডেনাম ছাড়া গ্রেড 304", "মৃদু ইস্পাত", "ঢালাই লোহা"],
        "মলিবডেনাম ক্লোরাইডের বিরুদ্ধে নিষ্ক্রিয় স্তর শক্ত করে।"),
    mcq("In impressed-current cathodic protection of a bridge deck, what is connected to the negative terminal of the power supply?", ["The steel reinforcement", "The anode mesh", "The asphalt", "The bridge lights"], 0,
        "Electrons are pushed onto the steel, making it the cathode so it does not corrode.",
        "সেতুর পাটাতনের আরোপিত-প্রবাহ ক্যাথোডিক সুরক্ষায় বিদ্যুৎ-উৎসের ঋণাত্মক প্রান্তে কী যুক্ত থাকে?", ["ইস্পাতের রড", "অ্যানোড-জাল", "পিচ", "সেতুর আলো"],
        "ইস্পাতে ইলেকট্রন ঠেলে দেওয়া হয়, তাই এটা ক্যাথোড হয়ে ক্ষয় থেকে বাঁচে।"),
    mcq("What is 'pitting corrosion' and why is it dangerous for cables and rebar?", ["Deep, narrow attack at small spots that can cut through a wire while the surface looks mostly fine", "Even rusting over a large area", "Corrosion of fruit pits", "Corrosion only on paint"], 0,
        "A few deep pits can cut a member's strength far more than general rusting.",
        "'গর্ত-ক্ষয়' কী আর তার আর রডের জন্য কেন বিপজ্জনক?", ["ছোট জায়গায় গভীর, সরু আক্রমণ, যা তল প্রায় ঠিক দেখালেও তার কেটে দিতে পারে", "বড় জায়গা জুড়ে সমান মরচে", "ফলের আঁটির ক্ষয়", "শুধু রঙে ক্ষয়"],
        "কয়েকটা গভীর গর্ত সাধারণ মরচের চেয়ে অংশের শক্তি অনেক বেশি কমাতে পারে।"),
    mcq("What is 'stress corrosion cracking'?", ["Cracks that grow when a metal is under tensile stress in a corrosive environment", "Cracks from hammering", "Paint cracking in sunlight", "Concrete cracking in frost"], 0,
        "High-strength prestressing wires must be protected from it.",
        "'পীড়ন-ক্ষয় ফাটল' কী?", ["ক্ষয়কারী পরিবেশে টান-পীড়নে থাকা ধাতুতে বাড়তে থাকা ফাটল", "হাতুড়ি পেটার ফাটল", "রোদে রঙের ফাটল", "তুষারে কংক্রিটের ফাটল"],
        "উচ্চ-শক্তির আগাম-টানের তারকে এর থেকে রক্ষা করতে হয়।"),
    mcq("Why are post-tensioning ducts in bridges filled completely with grout?", ["The alkaline grout protects the steel tendons and keeps out water and air", "To make the bridge heavier", "Grout is decorative", "To let water flow through"], 0,
        "Voids left in ducts have caused serious tendon corrosion in some bridges.",
        "সেতুর পরে-টানের নালি পুরোপুরি গ্রাউটে ভরা হয় কেন?", ["ক্ষারীয় গ্রাউট ইস্পাতের তার রক্ষা করে আর জল ও বাতাস ঢুকতে দেয় না", "সেতু ভারী করতে", "গ্রাউট সাজসজ্জা", "জল বইতে দিতে"],
        "নালিতে ফাঁকা থেকে যাওয়ায় কিছু সেতুতে তারের গুরুতর ক্ষয় হয়েছে।"),
    mcq("What is 'hydrogen embrittlement' of high-strength steel?", ["Hydrogen atoms enter the steel and make it brittle, so it can crack suddenly", "Steel becoming softer in water", "Steel turning into hydrogen", "A type of paint"], 0,
        "It is a risk when high-strength bolts are acid-cleaned or electroplated carelessly.",
        "উচ্চ-শক্তির ইস্পাতের 'হাইড্রোজেন-ভঙ্গুরতা' কী?", ["হাইড্রোজেন পরমাণু ইস্পাতে ঢুকে তাকে ভঙ্গুর করে, তাই হঠাৎ ফাটতে পারে", "জলে ইস্পাত নরম হওয়া", "ইস্পাত হাইড্রোজেন হয়ে যাওয়া", "এক রকম রং"],
        "উচ্চ-শক্তির বল্টু অসাবধানে অ্যাসিডে পরিষ্কার বা তড়িৎলেপন করলে এই ঝুঁকি।"),
    mcq("What does the Nernst idea tell us about a corrosion cell in salty water?", ["Electrode potentials depend on concentrations, so local differences in salt or oxygen drive corrosion", "Salt has no effect", "Potentials never change", "Only temperature matters"], 0,
        "Concentration cells form wherever conditions differ across a surface.",
        "নোনা জলে ক্ষয়-কোষ নিয়ে নার্নস্টের ভাবনা কী বলে?", ["তড়িদ্বার-বিভব গাঢ়ত্বের উপর নির্ভর করে, তাই লবণ বা অক্সিজেনের স্থানীয় পার্থক্য ক্ষয় চালায়", "লবণের প্রভাব নেই", "বিভব কখনো বদলায় না", "শুধু তাপমাত্রা গুরুত্বপূর্ণ"],
        "তলের এক জায়গা থেকে আরেক জায়গায় অবস্থা আলাদা হলেই গাঢ়ত্ব-কোষ তৈরি হয়।"),
    mcq("What is a 'transition element'?", ["A d-block metal that forms at least one ion with a partly filled d sub-shell", "Any metal", "A noble gas", "A non-metal"], 0,
        "Iron, chromium, nickel and copper are transition elements used in steels.",
        "'অবস্থান্তর মৌল' কী?", ["d-ব্লকের ধাতু, যা অন্তত একটা আংশিক-ভরা d উপকক্ষের আয়ন তৈরি করে", "যেকোনো ধাতু", "নিষ্ক্রিয় গ্যাস", "অধাতু"],
        "লোহা, ক্রোমিয়াম, নিকেল আর তামা ইস্পাতে ব্যবহৃত অবস্থান্তর মৌল।"),
    mcq("Why can transition metals show several oxidation states, like iron(II) and iron(III)?", ["Their 4s and 3d electrons have similar energies, so different numbers can be lost", "They have no electrons", "They are radioactive", "They are always +1"], 0,
        "Rust contains iron(III); green rust and some ores contain iron(II).",
        "লোহা(II) আর লোহা(III)-এর মতো অবস্থান্তর ধাতু কয়েকটা জারণ-অবস্থা দেখায় কেন?", ["এদের 4s আর 3d ইলেকট্রনের শক্তি কাছাকাছি, তাই আলাদা সংখ্যায় হারানো যায়", "এদের ইলেকট্রন নেই", "এরা তেজস্ক্রিয়", "সবসময় +1"],
        "মরচেতে লোহা(III); সবুজ মরচে আর কিছু আকরিকে লোহা(II)।"),
    mcq("What is a 'ligand' in a complex ion?", ["A molecule or ion that donates a lone pair to a central metal ion", "A type of bond in metals", "A neutron", "An acid"], 0,
        "Water molecules are ligands around Cu²⁺, giving its blue colour.",
        "জটিল আয়নে 'লিগ্যান্ড' কী?", ["কেন্দ্রীয় ধাতব আয়নকে নিঃসঙ্গ জোড় দান করা অণু বা আয়ন", "ধাতুর এক রকম বন্ধন", "একটা নিউট্রন", "একটা অ্যাসিড"],
        "Cu²⁺-এর চারপাশে জলের অণু লিগ্যান্ড, যা নীল রং দেয়।"),
    mcq("What does 'rate-determining step' mean in a reaction mechanism?", ["The slowest step, which controls the overall rate", "The fastest step", "The final step always", "A step with no reactants"], 0,
        "Like the slowest crew on a production line.",
        "বিক্রিয়ার প্রক্রিয়ায় 'হার-নির্ধারক ধাপ' মানে কী?", ["সবচেয়ে ধীর ধাপ, যা সামগ্রিক হার নিয়ন্ত্রণ করে", "সবচেয়ে দ্রুত ধাপ", "সবসময় শেষ ধাপ", "বিক্রিয়কহীন ধাপ"],
        "উৎপাদন-লাইনের সবচেয়ে ধীর দলের মতো।"),
    mcq("What does the Maxwell-Boltzmann distribution show?", ["How the energies of gas molecules are spread, and why only some exceed the activation energy", "The speed of light", "The density of steel", "The shape of a molecule"], 0,
        "Raising temperature shifts the curve so many more molecules can react.",
        "ম্যাক্সওয়েল-বোলৎসমান বণ্টন কী দেখায়?", ["গ্যাসের অণুদের শক্তি কীভাবে ছড়ানো, আর কেন শুধু কয়েকটা সক্রিয়করণ শক্তি ছাড়ায়", "আলোর বেগ", "ইস্পাতের ঘনত্ব", "অণুর আকার"],
        "তাপমাত্রা বাড়ালে বক্ররেখা সরে, তাই অনেক বেশি অণু বিক্রিয়া করতে পারে।"),
    mcq("Why does a 10°C rise often roughly double the rate of corrosion or cement hydration?", ["Many more particles then have energy above the activation energy", "Particles become heavier", "The reaction changes completely", "It has no effect"], 0,
        "Hot climates speed up both curing and corrosion.",
        "10°C বাড়লে প্রায়ই ক্ষয় বা সিমেন্ট-জলযোজনের হার মোটামুটি দ্বিগুণ হয় কেন?", ["তখন অনেক বেশি কণার শক্তি সক্রিয়করণ শক্তির উপরে থাকে", "কণা ভারী হয়", "বিক্রিয়া পুরো বদলে যায়", "প্রভাব নেই"],
        "গরম জলবায়ু জমাট আর ক্ষয় দুটোই দ্রুত করে।"),
    mcq("What is 'entropy' in simple terms?", ["A measure of disorder - the number of ways energy and particles can be arranged", "The heat in a reaction", "A type of bond", "The speed of a reaction"], 0,
        "Spontaneous changes tend to increase total entropy.",
        "সহজ কথায় 'এনট্রপি' কী?", ["বিশৃঙ্খলার মাপ - শক্তি আর কণা কত উপায়ে সাজানো যায়", "বিক্রিয়ার তাপ", "এক রকম বন্ধন", "বিক্রিয়ার গতি"],
        "স্বতঃস্ফূর্ত বদল মোট এনট্রপি বাড়ানোর দিকে ঝোঁকে।"),
    mcq("Why is rusting of iron spontaneous at room temperature even though it is slow?", ["It has a negative overall free-energy change - it is thermodynamically favoured, but kinetically slow", "It needs a spark", "It is endothermic", "Iron never rusts"], 0,
        "Protection works by slowing or blocking the reaction, not by making it impossible.",
        "ঘরের তাপমাত্রায় লোহার মরচে ধীর হলেও স্বতঃস্ফূর্ত কেন?", ["এর সামগ্রিক মুক্ত-শক্তির পরিবর্তন ঋণাত্মক - তাপগতীয়ভাবে অনুকূল, কিন্তু গতিগতভাবে ধীর", "স্ফুলিঙ্গ লাগে", "তাপগ্রাহী", "লোহায় মরচে ধরে না"],
        "সুরক্ষা বিক্রিয়াকে ধীর বা বন্ধ করে কাজ করে, অসম্ভব করে নয়।"),
    mcq("What is 'IUPAC naming' for?", ["A systematic way to name compounds so every chemist understands exactly which substance is meant", "Naming bridges", "Naming companies", "A brand of paint"], 0,
        "Ethanoic acid is the IUPAC name for acetic acid in vinegar.",
        "'আইইউপ্যাক নামকরণ' কীসের জন্য?", ["যৌগের নামের এক নিয়মবদ্ধ উপায়, যাতে প্রত্যেক রসায়নবিদ ঠিক কোন পদার্থ বোঝানো হচ্ছে বোঝেন", "সেতুর নাম", "কোম্পানির নাম", "রঙের ব্র্যান্ড"],
        "ভিনিগারের অ্যাসেটিক অ্যাসিডের আইইউপ্যাক নাম ইথানোয়িক অ্যাসিড।"),
    mcq("What does the prefix 'but-' mean in an organic name like butane?", ["4 carbon atoms in the main chain", "1 carbon", "2 carbons", "6 carbons"], 0,
        "meth = 1, eth = 2, prop = 3, but = 4.",
        "বিউটেনের মতো জৈব নামে 'বিউট-' উপসর্গ মানে কী?", ["মূল শৃঙ্খলে 4টি কার্বন-পরমাণু", "1টি কার্বন", "2টি কার্বন", "6টি কার্বন"],
        "মিথ = 1, ইথ = 2, প্রপ = 3, বিউট = 4।"),
    mcq("What are 'structural isomers'?", ["Compounds with the same molecular formula but atoms joined in a different order", "Identical molecules", "Atoms with different neutrons", "Two different elements"], 0,
        "Butane and methylpropane are structural isomers of C4H10.",
        "'গঠনগত সমাণু' কী?", ["একই আণবিক সংকেত কিন্তু পরমাণুগুলো আলাদা ক্রমে যুক্ত এমন যৌগ", "হুবহু এক অণু", "আলাদা নিউট্রনের পরমাণু", "দুটো আলাদা মৌল"],
        "বিউটেন আর মিথাইলপ্রোপেন C4H10-এর গঠনগত সমাণু।"),
    mcq("What is an 'epoxide' group, as used in epoxy resins?", ["A three-membered ring of two carbons and one oxygen that opens to form strong cross-links", "A double bond between carbons", "A metal ion", "A type of sugar"], 0,
        "Epoxy coatings and adhesives are used to bond and protect bridge steel.",
        "ইপক্সি রজনে ব্যবহৃত 'ইপক্সাইড' মূলক কী?", ["দুটো কার্বন আর একটা অক্সিজেনের তিন-সদস্যের বলয়, যা খুলে শক্ত আড়াআড়ি-সংযোগ গড়ে", "কার্বনের মধ্যে দ্বিবন্ধন", "ধাতব আয়ন", "এক রকম শর্করা"],
        "ইপক্সি আবরণ আর আঠা সেতুর ইস্পাত জোড়া আর রক্ষায় ব্যবহার হয়।"),
    mcq("Why does polyurethane foam sealant expand and harden in a joint?", ["Isocyanates react with moisture, releasing CO2 that foams the polymer as it cross-links", "It absorbs sand", "Air dries it like paint only", "It melts"], 0,
        "Isocyanates are hazardous - use proper ventilation and protection.",
        "পলিইউরিথেন-ফোম সিল্যান্ট জোড়ে ফুলে কেন শক্ত হয়?", ["আইসোসায়ানেট আর্দ্রতার সঙ্গে বিক্রিয়া করে CO2 ছাড়ে, যা আড়াআড়ি-যুক্ত হওয়ার সময় পলিমারকে ফেনায়", "বালি শোষে", "শুধু রঙের মতো বাতাসে শুকোয়", "গলে যায়"],
        "আইসোসায়ানেট বিপজ্জনক - ঠিকঠাক বায়ুচলাচল আর সুরক্ষা নাও।"),
    mcq("What is 'atom economy' used to compare?", ["How much of the reactants' mass ends up in the useful product", "The speed of reactions", "The price of atoms", "The colour of products"], 0,
        "High atom economy means less waste - greener chemistry.",
        "'পরমাণু-সাশ্রয়' কী তুলনায় ব্যবহার হয়?", ["বিক্রিয়কের ভরের কত অংশ কাজের উৎপাদে যায়", "বিক্রিয়ার গতি", "পরমাণুর দাম", "উৎপাদের রং"],
        "বেশি পরমাণু-সাশ্রয় মানে কম বর্জ্য - সবুজ রসায়ন।"),
    mcq("What is 'green chemistry'?", ["Designing processes to reduce waste, energy use and hazardous substances", "Chemistry with green chemicals only", "Painting labs green", "Chemistry of plants only"], 0,
        "Water-based coatings and low-carbon cements are green chemistry in construction.",
        "'সবুজ রসায়ন' কী?", ["বর্জ্য, শক্তি-ব্যবহার আর বিপজ্জনক পদার্থ কমাতে প্রক্রিয়ার নকশা", "শুধু সবুজ রাসায়নিক নিয়ে রসায়ন", "ল্যাব সবুজ রং করা", "শুধু উদ্ভিদের রসায়ন"],
        "নির্মাণে জল-ভিত্তিক আবরণ আর কম-কার্বন সিমেন্ট সবুজ রসায়নের উদাহরণ।"),
    mcq("What does a 'buffer solution' do?", ["Resists changes in pH when small amounts of acid or alkali are added", "Changes pH rapidly", "Removes all ions", "Makes water boil faster"], 0,
        "Concrete pore water is buffered by solid calcium hydroxide, holding its pH high.",
        "'বাফার দ্রবণ' কী করে?", ["অল্প অ্যাসিড বা ক্ষার যোগ করলে pH-এর বদল রোধ করে", "দ্রুত pH বদলায়", "সব আয়ন সরায়", "জল দ্রুত ফোটায়"],
        "কঠিন ক্যালসিয়াম হাইড্রক্সাইড কংক্রিটের ছিদ্র-জলকে বাফার করে উঁচু pH ধরে রাখে।"),
)
