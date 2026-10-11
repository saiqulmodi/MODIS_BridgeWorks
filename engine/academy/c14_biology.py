"""IIT level - Biology (advanced entrance standard, NEET-advanced depth): molecular genetics and gene
regulation, epistasis and linkage maps, chromosomal disorders, biotechnology tools, evolution,
cell cycle control, bioenergetics, plant physiology and hormones, human physiology (respiration,
circulation, excretion, nerves, hormones), reproduction and development, immunology, ecology and
microbes. Numerical items cover map distances, epistatic ratios, DNA labelling, physiology and
population calculations."""
import math
from fractions import Fraction as F

from . import mcq


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def _o(r, *alts):
    out = []
    for x in (r, *alts, r * 2, r + 1, r * 3, r + 10):
        x = _c(x)
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _f(x):
    return f"{x:,}" if isinstance(x, int) else f"{x:g}"


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    o = _o(_c(r), *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [_f(x) + u_en for x in o], 0, ex_en, q_bn, [_f(x) + ub for x in o], ex_bn)


def _fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def _fr(q_en, q_bn, r, alts, ex_en, ex_bn):
    out = []
    for x in (r, *alts, r * 2, r / 2, r + F(1, 16), r * 3):
        x = F(x)
        if 0 < x <= 1 and x not in out:
            out.append(x)
    opts = [_fs(x) for x in out[:4]]
    return mcq(q_en, opts, 0, ex_en, q_bn, opts, ex_bn)


# ---------------------------------------------------------------- genetics
def trihybrid(k):
    r = math.comb(3, k) * F(3, 4) ** k * F(1, 4) ** (3 - k)
    words = {3: ("all three", "তিনটিই"), 1: ("exactly one", "ঠিক একটি"), 0: ("none", "একটিও না")}[k]
    return _fr(f"AaBbCc is self-crossed (three unlinked genes, complete dominance). What fraction of the offspring show {words[0]} of the dominant traits?",
               f"AaBbCc-এর স্ব-সংকরণ (তিনটি অসংলগ্ন জিন, সম্পূর্ণ প্রকটতা)। অপত্যের কত ভাগ প্রকট বৈশিষ্ট্যের {words[1]} দেখায়?", r,
               (F(3, 4) ** k, F(27, 64) if k != 3 else F(9, 64), F(1, 8)),
               f"Each trait is dominant with probability 3/4: ³C{k} x (3/4)^{k} x (1/4)^{3 - k} = {_fs(r)}.",
               f"প্রতিটি বৈশিষ্ট্য প্রকট হওয়ার সম্ভাবনা 3/4: ³C{k} x (3/4)^{k} x (1/4)^{3 - k} = {_fs(r)}।")


def map_distance(rec, total):
    r = rec / total * 100
    return _n(f"A test cross gives {rec} recombinant offspring out of {total}. How far apart are the two genes on the chromosome map?",
              f"একটা পরীক্ষামূলক সংকরণে {total}টি অপত্যের মধ্যে {rec}টি পুনর্যোজিত। ক্রোমোজোম-মানচিত্রে জিন দুটির দূরত্ব কত?", r,
              f"Recombination frequency = {rec} ÷ {total} x 100 = {_f(_c(r))}%, and 1% = 1 map unit (centimorgan).",
              f"পুনর্যোজন হার = {rec} ÷ {total} x 100 = {_f(_c(r))}%, আর 1% = 1 মানচিত্র-একক (সেন্টিমর্গান)।",
              (100 - r, r / 2, rec / (total - rec) * 100), " cM", " সেন্টিমর্গান")


EPISTASIS = {
    "9:7": (F(9, 16), "coloured (purple) flowers in sweet pea, where two genes are both needed (9 : 7)",
            "মিষ্টি মটরে রঙিন (বেগুনি) ফুল, যেখানে দুটি জিনই লাগে (9 : 7)"),
    "12:3:1": (F(12, 16), "white fruits in summer squash, where a dominant gene masks colour (12 : 3 : 1)",
               "গ্রীষ্মকালীন স্কোয়াশে সাদা ফল, যেখানে একটা প্রকট জিন রং ঢেকে দেয় (12 : 3 : 1)"),
    "15:1": (F(15, 16), "triangular capsules in shepherd's purse, where either gene alone is enough (15 : 1)",
             "শেফার্ডস পার্সে ত্রিকোণ ফলত্বক, যেখানে যেকোনো একটা জিনই যথেষ্ট (15 : 1)"),
    "9:3:4": (F(4, 16), "albino mice, where the recessive cc hides the coat-colour gene (9 : 3 : 4)",
              "অ্যালবিনো ইঁদুর, যেখানে প্রচ্ছন্ন cc লোমের রঙের জিনকে ঢেকে দেয় (9 : 3 : 4)"),
}


def epistasis(key):
    r, en, bn = EPISTASIS[key]
    return _fr(f"In the F₂ of a dihybrid cross showing epistasis, what fraction are {en}?",
               f"এপিস্টাসিস দেখানো একটা দ্বিসংকর সংকরণের F₂-তে কত ভাগ {bn}?", r,
               (F(9, 16), F(3, 16), F(1, 16), F(7, 16)),
               f"The ratio {key} out of 16 gives {_fs(r)}; epistasis merges the classes of the 9 : 3 : 3 : 1 ratio.",
               f"16-এর মধ্যে {key} অনুপাত থেকে {_fs(r)}; এপিস্টাসিস 9 : 3 : 3 : 1-এর শ্রেণিগুলো মিলিয়ে দেয়।")


def polygene(n):
    r = 2 * n + 1
    return _n(f"A height trait is controlled by {n} gene pairs with equal, additive effects. How many phenotypic classes appear in the F₂?",
              f"একটা উচ্চতার বৈশিষ্ট্য সমান ও যোগাত্মক প্রভাবের {n} জোড়া জিন নিয়ন্ত্রণ করে। F₂-তে কয়টি ফিনোটাইপ-শ্রেণি দেখা যায়?", r,
              f"The number of dominant alleles can be 0 to {2 * n}, giving {r} classes (a bell-shaped spread).",
              f"প্রকট অ্যালিলের সংখ্যা 0 থেকে {2 * n} হতে পারে, তাই {r}টি শ্রেণি (ঘণ্টাকৃতি বিস্তার)।",
              (2 * n, 3 ** n, 2 ** n))


def meselson(n):
    r = F(2, 2 ** n)
    return _fr(f"E. coli grown in ¹⁵N is moved to ¹⁴N medium. After {n} generations, what fraction of the DNA molecules are hybrid (¹⁵N-¹⁴N)?",
               f"¹⁵N-এ বাড়া ই. কোলাই ¹⁴N মাধ্যমে আনা হল। {n} প্রজন্ম পরে ডিএনএ অণুর কত ভাগ সংকর (¹⁵N-¹⁴N)?", r,
               (F(1, 2 ** n), 1 - r if r < 1 else F(1, 3), F(1, n)),
               f"Semi-conservative replication keeps the 2 original strands in 2 of the 2^{n} = {2 ** n} molecules: 2/{2 ** n} = {_fs(r)}.",
               f"অর্ধ-সংরক্ষণশীল প্রতিলিপনে মূল 2টি সূত্র 2^{n} = {2 ** n}টি অণুর 2টিতে থাকে: 2/{2 ** n} = {_fs(r)}।")


def h_bonds(bp, a_pct):
    at = round(2 * bp * a_pct / 100)
    gc = bp - at
    r = 2 * at + 3 * gc
    return _n(f"A double-stranded DNA of {bp:,} base pairs has {a_pct}% adenine. How many hydrogen bonds hold its two strands together?",
              f"{bp:,} ক্ষারক-জোড়ার একটা দ্বিসূত্রক ডিএনএ-তে {a_pct}% অ্যাডেনিন। কয়টি হাইড্রোজেন বন্ধন দুটি সূত্রকে ধরে রাখে?", r,
              f"A = {a_pct}% of {2 * bp:,} bases = {at} A-T pairs (2 bonds each); the other {gc} pairs are G-C (3 each): {2 * at} + {3 * gc} = {r:,}.",
              f"{2 * bp:,}টি ক্ষারকের {a_pct}% = {at}টি A-T জোড়া (প্রতিটিতে 2টি বন্ধন); বাকি {gc}টি G-C (প্রতিটিতে 3টি): {2 * at} + {3 * gc} = {r:,}।",
              (3 * at + 2 * gc, 2 * bp, 3 * bp))


def mrna_length(aa):
    r = 3 * aa + 3
    return _n(f"A polypeptide has {aa} amino acids. What is the minimum length of the mRNA coding region, counting the stop codon?",
              f"একটা পলিপেপটাইডে {aa}টি অ্যামিনো অ্যাসিড। থামার কোডনসহ এমআরএনএ-র সংকেত-অংশের ন্যূনতম দৈর্ঘ্য কত?", r,
              f"{aa} codons x 3 = {3 * aa}, plus 3 for the stop codon (which codes no amino acid) = {r} nucleotides.",
              f"{aa}টি কোডন x 3 = {3 * aa}, আর থামার কোডনের 3 (যা কোনো অ্যামিনো অ্যাসিড দেয় না) = {r}টি নিউক্লিওটাইড।",
              (3 * aa, aa + 3, 3 * aa - 3))


def heterozygotes(q):
    r = 2 * q * (1 - q) * 100
    return _n(f"The recessive allele of a gene has frequency {q} in a population in Hardy-Weinberg equilibrium. What percentage of people are heterozygous?",
              f"হার্ডি-ভাইনবার্গ সাম্যে থাকা জনগোষ্ঠীতে একটা জিনের প্রচ্ছন্ন অ্যালিলের হার {q}। কত শতাংশ মানুষ বিষমযুগ্মী?", r,
              f"p = {_f(_c(1 - q))}, so 2pq = 2 x {_f(_c(1 - q))} x {q} = {_f(_c(r / 100))} = {_f(_c(r))}%.",
              f"p = {_f(_c(1 - q))}, তাই 2pq = 2 x {_f(_c(1 - q))} x {q} = {_f(_c(r / 100))} = {_f(_c(r))}%।",
              (q * q * 100, (1 - q) ** 2 * 100, q * 100), "%")


def x_linked_females(m_pct):
    r = (m_pct / 100) ** 2 * 100
    return _n(f"{m_pct}% of the men in a population are red-green colour-blind (X-linked recessive). What percentage of the women are expected to be colour-blind?",
              f"একটা জনগোষ্ঠীর {m_pct}% পুরুষ লাল-সবুজ বর্ণান্ধ (X-সংযুক্ত প্রচ্ছন্ন)। কত শতাংশ নারী বর্ণান্ধ হবেন বলে আশা করা যায়?", r,
              f"In men the trait frequency equals q = {m_pct / 100:g}; women need two copies, q² = {(m_pct / 100) ** 2:g} = {_f(_c(r))}%.",
              f"পুরুষে বৈশিষ্ট্যের হার q = {m_pct / 100:g}; নারীর দুটি প্রতিলিপি লাগে, q² = {_f(_c(r))}%।",
              (m_pct, m_pct / 2, 2 * m_pct / 100 * (1 - m_pct / 100) * 100), "%")


# ---------------------------------------------------------------- physiology
def alveolar(tv, dead, rate):
    r = (tv - dead) * rate
    return _n(f"A person breathes {rate} times a minute with a tidal volume of {tv} mL; the anatomical dead space is {dead} mL. What is the alveolar ventilation?",
              f"একজন মিনিটে {rate} বার শ্বাস নেন, জোয়ার-আয়তন {tv} mL; শারীরস্থানিক মৃত-স্থান {dead} mL। বায়ুথলির বায়ুচলাচল কত?", r,
              f"Only air beyond the dead space reaches the alveoli: ({tv} - {dead}) x {rate} = {r:,} mL/min.",
              f"কেবল মৃত-স্থানের বাইরের বায়ু বায়ুথলিতে পৌঁছয়: ({tv} - {dead}) x {rate} = {r:,} mL/মিনিট।",
              (tv * rate, dead * rate, r + dead), " mL/min", " mL/মিনিট")


def o2_capacity(hb, sat):
    r = hb * 1.34 * sat / 100
    return _n(f"Blood has {hb} g of haemoglobin per 100 mL and is {sat}% saturated. Each gram binds 1.34 mL of O₂. How much oxygen is bound per 100 mL of blood?",
              f"রক্তে প্রতি 100 mL-এ {hb} g হিমোগ্লোবিন, সম্পৃক্ততা {sat}%। প্রতি গ্রাম 1.34 mL অক্সিজেন বাঁধে। প্রতি 100 mL রক্তে কত অক্সিজেন বাঁধা থাকে?", r,
              f"{hb} x 1.34 x {sat / 100:g} = {_f(_c(r))} mL O₂ per 100 mL.",
              f"{hb} x 1.34 x {sat / 100:g} = {_f(_c(r))} mL অক্সিজেন প্রতি 100 mL-এ।",
              (hb * 1.34, hb * sat / 100, r / 2), " mL")


def mean_pressure(sys_, dia):
    r = dia + (sys_ - dia) / 3
    return _n(f"A person's blood pressure is {sys_}/{dia} mm Hg. What is the mean arterial pressure?",
              f"একজনের রক্তচাপ {sys_}/{dia} mm Hg। গড় ধমনী-চাপ কত?", r,
              f"The heart spends about two-thirds of each beat in diastole: MAP ≈ {dia} + ({sys_} - {dia}) ÷ 3 = {_f(_c(r))} mm Hg.",
              f"হৃৎপিণ্ড প্রতি স্পন্দনের প্রায় দুই-তৃতীয়াংশ সময় প্রসারণে থাকে: গড় চাপ ≈ {dia} + ({sys_} - {dia}) ÷ 3 = {_f(_c(r))} mm Hg।",
              ((sys_ + dia) / 2, sys_ - dia, r + 10), " mm Hg")


def clearance(u, v, p):
    r = u * v / p
    return _n(f"Inulin is infused into the blood. Its plasma level is {p} mg/mL, its urine level {u} mg/mL and urine flows at {v} mL/min. What is the inulin clearance (= GFR)?",
              f"রক্তে ইনুলিন দেওয়া হল। রক্তরসে তার মাত্রা {p} mg/mL, মূত্রে {u} mg/mL, আর মূত্র প্রবাহ {v} mL/মিনিট। ইনুলিন ক্লিয়ারেন্স (= পরিস্রাবণ হার) কত?", r,
              f"C = U x V ÷ P = {u} x {v} ÷ {p} = {_f(_c(r))} mL/min; inulin is filtered but neither reabsorbed nor secreted.",
              f"ক্লিয়ারেন্স = U x V ÷ P = {u} x {v} ÷ {p} = {_f(_c(r))} mL/মিনিট; ইনুলিন পরিস্রুত হয়, কিন্তু পুনঃশোষিত বা ক্ষরিত হয় না।",
              (u * p / v, u / p, r / 2), " mL/min", " mL/মিনিট")


def ejection(sv, edv):
    r = sv / edv * 100
    return _n(f"A ventricle holds {edv} mL at the end of diastole and pumps out {sv} mL per beat. What is its ejection fraction?",
              f"একটা নিলয় প্রসারণের শেষে {edv} mL ধরে রাখে আর প্রতি স্পন্দনে {sv} mL পাম্প করে। এর নিক্ষেপণ-ভগ্নাংশ কত?", r,
              f"EF = stroke volume ÷ end-diastolic volume = {sv} ÷ {edv} = {_f(_c(r))}% (healthy hearts: about 55-70%).",
              f"নিক্ষেপণ-ভগ্নাংশ = স্পন্দন-আয়তন ÷ প্রসারণ-শেষ আয়তন = {sv} ÷ {edv} = {_f(_c(r))}% (সুস্থ হৃৎপিণ্ডে প্রায় 55-70%)।",
              (100 - r, (edv - sv) / sv * 100, r / 2), "%")


def beta_ox(c, what):
    if what == "cycles":
        r = c // 2 - 1
        en, bn = "β-oxidation cycles", "বিটা-জারণ চক্র"
        alts = (c // 2, c - 1, c // 4)
    else:
        r = c // 2
        en, bn = "acetyl-CoA molecules", "অ্যাসিটাইল-কোএ অণু"
        alts = (c // 2 - 1, c, c // 3)
    return _n(f"How many {en} does the complete breakdown of a saturated fatty acid with {c} carbons give?",
              f"{c} কার্বনের একটা সম্পৃক্ত ফ্যাটি অ্যাসিড সম্পূর্ণ ভাঙলে কয়টি {bn} হয়?", r,
              f"Each cycle removes 2 carbons: {c // 2 - 1} cycles make {c // 2} acetyl-CoA (the last cycle leaves two).",
              f"প্রতিটি চক্র 2টি কার্বন সরায়: {c // 2 - 1}টি চক্রে {c // 2}টি অ্যাসিটাইল-কোএ (শেষ চক্র দুটি রেখে যায়)।",
              alts)


# ---------------------------------------------------------------- plants and ecology
def water_potential(psi_s, psi_p):
    r = round(psi_s + psi_p, 2)
    vals = [r, round(psi_s - psi_p, 2), psi_s, round(-r, 2) if r != 0 else 0.1]
    opts = []
    for v in vals:
        s = f"{v:g} MPa"
        if s not in opts:
            opts.append(s)
    while len(opts) < 4:
        opts.append(f"{round(r - 0.1 * len(opts), 2):g} MPa")
    bn_opts = [o.replace("MPa", "মেগাপ্যাসকেল") for o in opts]
    return mcq(f"A plant cell has a solute potential of {psi_s:g} MPa and a pressure potential of {psi_p:g} MPa. What is its water potential?",
               opts, 0,
               f"Ψw = Ψs + Ψp = {psi_s:g} + {psi_p:g} = {r:g} MPa; water moves towards the more negative water potential.",
               f"একটা উদ্ভিদকোষের দ্রাব-বিভব {psi_s:g} মেগাপ্যাসকেল আর চাপ-বিভব {psi_p:g} মেগাপ্যাসকেল। এর জল-বিভব কত?",
               bn_opts,
               f"জল-বিভব = দ্রাব-বিভব + চাপ-বিভব = {psi_s:g} + {psi_p:g} = {r:g} মেগাপ্যাসকেল; জল বেশি ঋণাত্মক জল-বিভবের দিকে যায়।")


def logistic(r_, n, k):
    g = r_ * n * (1 - n / k)
    return _n(f"A population of {n} grows logistically with r = {r_} per year and carrying capacity K = {k:,}. How fast is it growing now?",
              f"{n} সদস্যের একটা জনগোষ্ঠী লজিস্টিকভাবে বাড়ে, r = {r_} প্রতি বছর, ধারণক্ষমতা K = {k:,}। এখন বৃদ্ধির হার কত?", g,
              f"dN/dt = rN(1 - N/K) = {r_} x {n} x (1 - {n}/{k:,}) = {_f(_c(g))} individuals per year.",
              f"dN/dt = rN(1 - N/K) = {r_} x {n} x (1 - {n}/{k:,}) = প্রতি বছর {_f(_c(g))}টি সদস্য।",
              (r_ * n, r_ * k, g / 2))


def calvin(n, what):
    if what == "atp":
        r, en, bn, ex, exb = 18 * n, "ATP molecules", "এটিপি অণু", "18 ATP per glucose", "প্রতি গ্লুকোজে 18টি এটিপি"
        alts = (12 * n, 6 * n, 36 * n)
    elif what == "nadph":
        r, en, bn, ex, exb = 12 * n, "NADPH molecules", "এনএডিপিএইচ অণু", "12 NADPH per glucose", "প্রতি গ্লুকোজে 12টি এনএডিপিএইচ"
        alts = (18 * n, 6 * n, 24 * n)
    else:
        r, en, bn, ex, exb = 6 * n, "turns of the Calvin cycle", "ক্যালভিন চক্রের আবর্তন", "6 turns (one CO₂ each) per glucose", "প্রতি গ্লুকোজে 6টি আবর্তন (প্রতিটিতে একটি CO₂)"
        alts = (3 * n, 12 * n, n)
    return _n(f"How many {en} are needed to make {n} molecules of glucose in the Calvin cycle?",
              f"ক্যালভিন চক্রে {n} অণু গ্লুকোজ তৈরি করতে কয়টি {bn} লাগে?", r,
              f"Each CO₂ fixed uses 3 ATP and 2 NADPH, and glucose has 6 carbons: {ex}, so {r} for {n}.",
              f"প্রতিটি CO₂ বাঁধতে 3টি এটিপি আর 2টি এনএডিপিএইচ লাগে, আর গ্লুকোজে 6টি কার্বন: {exb}, তাই {n}টির জন্য {r}।",
              alts)


def seed_meiosis(seeds):
    r = seeds + seeds // 4
    return _n(f"How many meiotic divisions are needed to form {seeds} seeds in a flowering plant?",
              f"একটা সপুষ্পক উদ্ভিদে {seeds}টি বীজ তৈরি করতে কয়টি মিয়োসিস বিভাজন লাগে?", r,
              f"Each seed needs one megaspore mother cell ({seeds} meioses) and one pollen grain; each microspore mother cell gives 4 pollen ({seeds // 4} meioses): {r}.",
              f"প্রতিটি বীজে একটা গুরুরেণু-মাতৃকোষ ({seeds}টি মিয়োসিস) আর একটা পরাগরেণু লাগে; প্রতিটি লঘুরেণু-মাতৃকোষ 4টি পরাগ দেয় ({seeds // 4}টি মিয়োসিস): {r}।",
              (seeds, 2 * seeds, seeds // 4))


def endosperm(two_n, plant_en, plant_bn):
    r = 3 * two_n // 2
    return _n(f"The leaf cells of {plant_en} have {two_n} chromosomes. How many chromosomes are in its endosperm cells?",
              f"{plant_bn}-এর পাতার কোষে {two_n}টি ক্রোমোজোম। এর শস্যকোষে (এন্ডোস্পার্ম) কয়টি ক্রোমোজোম?", r,
              f"Endosperm is triploid (two polar nuclei + one sperm): 3 x {two_n // 2} = {r}.",
              f"শস্য ত্রিপ্লয়েড (দুটি মেরু-নিউক্লিয়াস + একটি শুক্রাণু): 3 x {two_n // 2} = {r}।",
              (two_n, two_n // 2, 2 * two_n))


NUMERIC = [
    trihybrid(3), trihybrid(1), trihybrid(0),
    map_distance(18, 200), map_distance(45, 300), map_distance(12, 400), map_distance(66, 600), map_distance(35, 500),
    epistasis("9:7"), epistasis("12:3:1"), epistasis("15:1"), epistasis("9:3:4"),
    polygene(3), polygene(4), polygene(5),
    meselson(2), meselson(3), meselson(4), meselson(5),
    h_bonds(1000, 20), h_bonds(500, 30), h_bonds(2000, 15),
    mrna_length(100), mrna_length(250), mrna_length(60),
    heterozygotes(0.3), heterozygotes(0.1), heterozygotes(0.4),
    x_linked_females(8), x_linked_females(10), x_linked_females(5),
    alveolar(500, 150, 12), alveolar(600, 150, 15), alveolar(400, 150, 20),
    o2_capacity(15, 98), o2_capacity(12, 98), o2_capacity(15, 75),
    mean_pressure(120, 80), mean_pressure(140, 90), mean_pressure(110, 70),
    clearance(30, 1, 0.25), clearance(25, 1, 0.25), clearance(62.5, 0.5, 0.25),
    ejection(70, 120), ejection(80, 130), ejection(50, 150),
    beta_ox(16, "cycles"), beta_ox(18, "cycles"), beta_ox(16, "acetyl"), beta_ox(20, "acetyl"),
    water_potential(-0.8, 0.3), water_potential(-1.2, 0.5), water_potential(-0.6, 0.6),
    logistic(0.2, 500, 1000), logistic(0.1, 200, 1000), logistic(0.5, 900, 1000),
    calvin(2, "atp"), calvin(3, "nadph"), calvin(5, "turns"),
    seed_meiosis(100), seed_meiosis(200), seed_meiosis(40),
    endosperm(24, "rice", "ধান"), endosperm(14, "garden pea", "মটর"), endosperm(16, "onion", "পেঁয়াজ"),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = []
CONCEPTS += [
    # ---------------------------------------------------------------- molecular genetics
    _q("What does telomerase do?", ["It adds repeats to chromosome ends, using its own RNA as a template", "It joins Okazaki fragments", "It unwinds the double helix", "It removes RNA primers"],
       "Linear chromosomes shorten at each replication; telomerase (a reverse transcriptase) is active in germ cells, stem cells and most cancers.",
       "টেলোমারেজ কী করে?", ["নিজের আরএনএ ছাঁচ ব্যবহার করে ক্রোমোজোমের প্রান্তে পুনরাবৃত্ত অংশ যোগ করে", "ওকাজাকি খণ্ড জোড়ে", "দ্বিকুণ্ডলী খোলে", "আরএনএ প্রাইমার সরায়"],
       "রৈখিক ক্রোমোজোম প্রতিলিপনে ছোট হয়; টেলোমারেজ (একটা বিপরীত ট্রান্সক্রিপটেজ) জননকোষ, স্টেম কোষ আর বেশির ভাগ ক্যানসারে সক্রিয়।"),
    _q("Which RNA polymerase transcribes mRNA precursors in eukaryotes?", ["RNA polymerase II", "RNA polymerase I", "RNA polymerase III", "Primase"],
       "Pol I makes most rRNA, Pol II makes hnRNA (pre-mRNA), Pol III makes tRNA, 5S rRNA and snRNAs.",
       "সুকেন্দ্রিকে কোন আরএনএ পলিমারেজ এমআরএনএ-র পূর্বসূরি প্রতিলিপি করে?", ["আরএনএ পলিমারেজ II", "আরএনএ পলিমারেজ I", "আরএনএ পলিমারেজ III", "প্রাইমেজ"],
       "Pol I বেশির ভাগ আরআরএনএ, Pol II এইচএনআরএনএ (প্রাক-এমআরএনএ), Pol III টিআরএনএ, 5S আরআরএনএ আর এসএনআরএনএ তৈরি করে।"),
    _q("In bacteria, the sigma (σ) factor of RNA polymerase…", ["Recognises the promoter and starts transcription", "Ends transcription at the terminator", "Adds the poly-A tail", "Splices out introns"],
       "σ joins the core enzyme to form the holoenzyme for initiation; ρ (rho) helps terminate some genes.",
       "ব্যাকটেরিয়ায় আরএনএ পলিমারেজের সিগমা (σ) উপাদান…", ["প্রোমোটার চেনে আর প্রতিলিপন শুরু করে", "টার্মিনেটরে প্রতিলিপন শেষ করে", "পলি-A লেজ যোগ করে", "ইনট্রন কেটে বাদ দেয়"],
       "σ মূল উৎসেচকের সঙ্গে মিলে সূচনার জন্য হোলোএনজাইম গড়ে; ρ (রো) কিছু জিনে সমাপ্তিতে সাহায্য করে।"),
    _q("The Shine-Dalgarno sequence on a bacterial mRNA…", ["Pairs with 16S rRNA to position the ribosome at the start codon", "Codes for the first amino acid", "Signals transcription to stop", "Is removed by splicing"],
       "It lies just upstream of AUG; eukaryotic ribosomes instead scan from the 5' cap.",
       "ব্যাকটেরিয়ার এমআরএনএ-তে শাইন-ডালগার্নো অনুক্রম…", ["16S আরআরএনএ-র সঙ্গে জোড় বেঁধে রাইবোজোমকে শুরুর কোডনে বসায়", "প্রথম অ্যামিনো অ্যাসিডের সংকেত দেয়", "প্রতিলিপন থামার সংকেত দেয়", "স্প্লাইসিংয়ে বাদ যায়"],
       "এটা AUG-এর ঠিক আগে থাকে; সুকেন্দ্রিক রাইবোজোম বরং 5' টুপি থেকে খুঁজে এগোয়।"),
    _q("Crick's wobble hypothesis explains why…", ["One tRNA can read more than one codon, through loose pairing at the third base", "Mutations are always harmful", "Start codons differ between species", "Ribosomes have two subunits"],
       "The 5' base of the anticodon (often inosine) can pair with several bases, so about 45 tRNAs serve 61 codons.",
       "ক্রিকের ওয়াবল প্রকল্প ব্যাখ্যা করে কেন…", ["তৃতীয় ক্ষারকে শিথিল জোড়ের ফলে একটা টিআরএনএ একাধিক কোডন পড়তে পারে", "মিউটেশন সবসময় ক্ষতিকর", "শুরুর কোডন প্রজাতিভেদে আলাদা", "রাইবোজোমের দুটি উপ-একক থাকে"],
       "অ্যান্টিকোডনের 5' ক্ষারক (প্রায়ই ইনোসিন) কয়েকটি ক্ষারকের সঙ্গে জোড় বাঁধে, তাই প্রায় 45টি টিআরএনএ 61টি কোডন সামলায়।"),
    _q("Which molecule catalyses peptide bond formation in the ribosome?", ["The large-subunit rRNA (a ribozyme)", "A protein called peptidase", "tRNA", "mRNA"],
       "Peptidyl transferase activity lies in 23S rRNA (28S in eukaryotes) - strong support for an early 'RNA world'.",
       "রাইবোজোমে কোন অণু পেপটাইড বন্ধন গঠনে অনুঘটক?", ["বড় উপ-এককের আরআরএনএ (একটা রাইবোজাইম)", "পেপটিডেজ নামের প্রোটিন", "টিআরএনএ", "এমআরএনএ"],
       "পেপটিডাইল ট্রান্সফারেজ ক্ষমতা 23S আরআরএনএ-তে (সুকেন্দ্রিকে 28S) - প্রাচীন 'আরএনএ জগৎ'-এর জোরালো সমর্থন।"),
    _q("The trp operon of E. coli is an example of…", ["A repressible operon, switched off when tryptophan is plentiful", "An inducible operon switched on by lactose", "A constitutive gene", "A eukaryotic enhancer"],
       "Tryptophan acts as a co-repressor: it activates the repressor, which then binds the operator.",
       "ই. কোলাইয়ের trp অপেরন কীসের উদাহরণ?", ["অবদমনযোগ্য অপেরন, ট্রিপটোফ্যান প্রচুর হলে বন্ধ হয়", "ল্যাকটোজে চালু হওয়া আবেশযোগ্য অপেরন", "সর্বদা-সক্রিয় জিন", "সুকেন্দ্রিক এনহ্যান্সার"],
       "ট্রিপটোফ্যান সহ-অবদমক: এটা অবদমককে সক্রিয় করে, যা তখন অপারেটরে বসে।"),
    _q("A deletion of one base in the middle of a gene usually…", ["Shifts the reading frame and changes every codon after it", "Changes only one amino acid", "Has no effect", "Converts the gene into an intron"],
       "Frameshifts scramble the downstream protein and often create an early stop codon; deleting three bases removes one amino acid.",
       "একটা জিনের মাঝখানে একটা ক্ষারক মুছে গেলে সাধারণত…", ["পাঠ-কাঠামো সরে যায় আর পরের সব কোডন বদলায়", "কেবল একটা অ্যামিনো অ্যাসিড বদলায়", "কোনো প্রভাব হয় না", "জিনটি ইনট্রন হয়ে যায়"],
       "কাঠামো-সরণ পরবর্তী প্রোটিনকে এলোমেলো করে, প্রায়ই আগাম থামার কোডন তৈরি করে; তিনটি ক্ষারক মুছলে একটা অ্যামিনো অ্যাসিড বাদ যায়।"),
    _q("Transposons ('jumping genes') were first discovered by…", ["Barbara McClintock, in maize", "Gregor Mendel, in peas", "Watson and Crick, in phage", "Thomas Morgan, in fruit flies"],
       "She explained the patchy colours of maize kernels by elements that move within the genome (Nobel 1983).",
       "ট্রান্সপোজন ('লাফানো জিন') প্রথম আবিষ্কার করেন…", ["বারবারা ম্যাকক্লিনটক, ভুট্টায়", "গ্রেগর মেন্ডেল, মটরে", "ওয়াটসন আর ক্রিক, ফাজে", "টমাস মর্গান, ফলের মাছিতে"],
       "ভুট্টার দানার ছোপ ছোপ রঙ তিনি জিনোমের ভেতরে সরে যাওয়া উপাদান দিয়ে ব্যাখ্যা করেন (নোবেল 1983)।"),
    _q("In Sanger sequencing, chain termination happens because dideoxynucleotides…", ["Lack the 3'-OH group needed to add the next nucleotide", "Bind the DNA polymerase permanently", "Cut the DNA strand", "Pair with every base"],
       "Fragments ending at each base are separated by size, and the sequence is read from the order.",
       "স্যাঙ্গার অনুক্রম-নির্ণয়ে শৃঙ্খল থামে কারণ ডাইডিঅক্সিনিউক্লিওটাইডে…", ["পরের নিউক্লিওটাইড যোগ করার জন্য দরকারি 3'-OH গ্রুপ নেই", "ডিএনএ পলিমারেজ স্থায়ীভাবে আটকে যায়", "ডিএনএ সূত্র কেটে যায়", "সব ক্ষারকের সঙ্গে জোড় বাঁধে"],
       "প্রতিটি ক্ষারকে শেষ হওয়া খণ্ডগুলো মাপ অনুযায়ী আলাদা করে ক্রম থেকে অনুক্রম পড়া হয়।"),
    _q("In CRISPR-Cas9 genome editing, what guides Cas9 to the target DNA?", ["A short guide RNA complementary to the target", "A restriction site", "A plasmid origin of replication", "A ribosome-binding site"],
       "Cas9 cuts where the guide RNA pairs next to a PAM sequence; the cell's repair then disables or edits the gene.",
       "ক্রিসপার-ক্যাস9 জিনোম সম্পাদনায় ক্যাস9-কে লক্ষ্য ডিএনএ-তে কী নিয়ে যায়?", ["লক্ষ্যের পরিপূরক একটা ছোট পথপ্রদর্শক আরএনএ", "একটা রেস্ট্রিকশন স্থান", "প্লাজমিডের প্রতিলিপন-সূচনাস্থল", "রাইবোজোম-বন্ধন স্থান"],
       "পথপ্রদর্শক আরএনএ যেখানে PAM অনুক্রমের পাশে জোড় বাঁধে, ক্যাস9 সেখানে কাটে; তারপর কোষের মেরামতি জিনটি অকেজো বা সম্পাদিত করে।"),
    _q("In blue-white screening, recombinant colonies are white because…", ["The insert disrupts the lacZ gene, so no β-galactosidase is made (insertional inactivation)", "They have lost the plasmid", "They are dead", "X-gal cannot enter them"],
       "Colonies whose plasmid has no insert keep a working lacZ and turn X-gal blue.",
       "নীল-সাদা বাছাইয়ে পুনর্যোজিত কলোনি সাদা হয় কারণ…", ["সন্নিবিষ্ট ডিএনএ lacZ জিনকে ভেঙে দেয়, তাই বিটা-গ্যালাক্টোসিডেজ তৈরি হয় না (সন্নিবেশ-নিষ্ক্রিয়করণ)", "তারা প্লাজমিড হারিয়েছে", "তারা মৃত", "তাদের ভেতরে এক্স-গ্যাল ঢুকতে পারে না"],
       "যে কলোনির প্লাজমিডে কিছু ঢোকেনি, তাদের lacZ কাজ করে আর এক্স-গ্যালকে নীল করে।"),
    _q("Agrobacterium tumefaciens is used to make transgenic plants because…", ["Its Ti plasmid naturally transfers a DNA segment (T-DNA) into plant chromosomes", "It fixes nitrogen", "It kills insects", "It makes plants grow faster"],
       "Scientists replace the tumour genes in T-DNA with useful genes - a 'natural genetic engineer'.",
       "জিন-পরিবর্তিত উদ্ভিদ তৈরিতে অ্যাগ্রোব্যাকটেরিয়াম টিউমিফেসিয়েন্স ব্যবহৃত হয় কারণ…", ["এর টিআই প্লাজমিড স্বাভাবিকভাবে একটা ডিএনএ অংশ (টি-ডিএনএ) উদ্ভিদের ক্রোমোজোমে পাঠায়", "এটা নাইট্রোজেন বাঁধে", "এটা পোকা মারে", "এটা উদ্ভিদকে দ্রুত বাড়ায়"],
       "বিজ্ঞানীরা টি-ডিএনএ-র টিউমার জিন সরিয়ে দরকারি জিন বসান - এক 'প্রাকৃতিক জিন প্রকৌশলী'।"),
    _q("Tobacco plants protected from the nematode Meloidogyne incognita use…", ["RNA interference: double-stranded RNA silences an essential nematode gene", "A Bt toxin gene", "A gene for herbicide resistance", "Extra chlorophyll"],
       "Nematode-specific genes were introduced so the plant makes dsRNA; the parasite feeding on it cannot survive.",
       "নিমাটোড মেলোইডোগাইন ইনকগনিটা থেকে সুরক্ষিত তামাক গাছ ব্যবহার করে…", ["আরএনএ ইন্টারফারেন্স: দ্বিসূত্রক আরএনএ নিমাটোডের একটা অপরিহার্য জিন স্তব্ধ করে", "বিটি বিষের জিন", "আগাছানাশক-প্রতিরোধের জিন", "বাড়তি ক্লোরোফিল"],
       "নিমাটোড-নির্দিষ্ট জিন ঢোকানো হয়, তাই গাছ দ্বিসূত্রক আরএনএ বানায়; তা খাওয়া পরজীবী বাঁচে না।"),
    _q("The first clinical gene therapy (1990) treated a child with…", ["Adenosine deaminase (ADA) deficiency, a severe immune disorder", "Diabetes", "Sickle-cell anaemia", "Haemophilia"],
       "Her lymphocytes were given a working ADA gene and returned; periodic infusions were needed because the cells die.",
       "প্রথম ক্লিনিক্যাল জিন-চিকিৎসা (1990) একটি শিশুর কোন রোগে করা হয়?", ["অ্যাডেনোসিন ডিঅ্যামিনেজ ঘাটতি, একটা গুরুতর অনাক্রম্যতা-রোগ", "ডায়াবেটিস", "সিকল-সেল রক্তাল্পতা", "হিমোফিলিয়া"],
       "তার লিম্ফোসাইটে কার্যকর জিন দিয়ে ফেরত দেওয়া হয়; কোষ মরে যায় বলে মাঝে মাঝে আবার দিতে হত।"),
    _q("Which Indian body approves the release of genetically modified organisms?", ["GEAC (Genetic Engineering Appraisal Committee)", "ISRO", "ICAR alone", "The Election Commission"],
       "GEAC under the environment ministry judges the safety of GM research and field release, such as Bt cotton.",
       "জিন-পরিবর্তিত জীব ছাড়ার অনুমতি দেয় ভারতের কোন সংস্থা?", ["জিন প্রকৌশল মূল্যায়ন কমিটি (জিইএসি)", "ইসরো", "কেবল আইসিএআর", "নির্বাচন কমিশন"],
       "পরিবেশ মন্ত্রকের অধীনে এই কমিটি জিন-পরিবর্তিত গবেষণা আর মাঠে ছাড়ার নিরাপত্তা বিচার করে, যেমন বিটি তুলো।"),
    _q("Why are bacterial cells treated with calcium chloride before transformation?", ["To make their membranes permeable so plasmid DNA can enter (competence)", "To kill them", "To cut the plasmid", "To feed them"],
       "Divalent Ca²⁺ ions and a brief heat shock at 42 °C help the negatively charged DNA cross the cell envelope.",
       "রূপান্তরের আগে ব্যাকটেরিয়া কোষকে ক্যালসিয়াম ক্লোরাইডে রাখা হয় কেন?", ["প্লাজমিড ডিএনএ ঢোকার জন্য পর্দাকে ভেদ্য করতে (সক্ষমতা)", "তাদের মারতে", "প্লাজমিড কাটতে", "তাদের খাওয়াতে"],
       "দ্বিযোজী Ca²⁺ আয়ন আর 42 °C-এ ক্ষণিক তাপ-আঘাত ঋণাত্মক ডিএনএ-কে কোষের আবরণ পার হতে সাহায্য করে।"),
    _q("In a cloning vector, the 'ori' sequence…", ["Is where replication starts, and it controls the copy number", "Gives antibiotic resistance", "Is the site cut by restriction enzymes", "Codes for the inserted protein"],
       "Any DNA linked to ori is copied along with the vector; selectable markers and cloning sites are other parts.",
       "ক্লোনিং ভেক্টরে 'ori' অনুক্রম…", ["প্রতিলিপন শুরুর জায়গা, আর প্রতিলিপির সংখ্যা নিয়ন্ত্রণ করে", "অ্যান্টিবায়োটিক প্রতিরোধ দেয়", "রেস্ট্রিকশন উৎসেচকের কাটার জায়গা", "সন্নিবিষ্ট প্রোটিনের সংকেত দেয়"],
       "ori-র সঙ্গে যুক্ত যেকোনো ডিএনএ ভেক্টরের সঙ্গে প্রতিলিপি হয়; বাছাই-চিহ্ন আর ক্লোনিং স্থান অন্য অংশ।"),
    _q("The steps after fermentation that purify a biotech product (separation, purification, formulation) are called…", ["Downstream processing", "Upstream processing", "Transformation", "Electrophoresis"],
       "The product must pass quality-control tests before it can be sold as a medicine.",
       "জৈবপ্রযুক্তি পণ্যকে গাঁজনের পরে বিশুদ্ধ করার ধাপগুলোকে (পৃথকীকরণ, বিশুদ্ধকরণ, প্রস্তুতকরণ) বলে…", ["নিম্নপ্রবাহ প্রক্রিয়াকরণ", "ঊর্ধ্বপ্রবাহ প্রক্রিয়াকরণ", "রূপান্তর", "তড়িৎ-কণা সঞ্চালন"],
       "ওষুধ হিসেবে বিক্রির আগে পণ্যকে মান-নিয়ন্ত্রণ পরীক্ষা পেরোতে হয়।"),
    # ---------------------------------------------------------------- inheritance
    _q("Which F₂ ratio shows complementary gene action?", ["9 : 7", "12 : 3 : 1", "15 : 1", "9 : 3 : 4"],
       "Both dominant genes are needed for the trait, so only the 9 class shows it.",
       "কোন F₂ অনুপাত পরিপূরক জিন-ক্রিয়া দেখায়?", ["9 : 7", "12 : 3 : 1", "15 : 1", "9 : 3 : 4"],
       "বৈশিষ্ট্যের জন্য দুটি প্রকট জিনই লাগে, তাই কেবল 9 শ্রেণি তা দেখায়।"),
    _q("A single gene affecting several unrelated traits (as in phenylketonuria) shows…", ["Pleiotropy", "Polygenic inheritance", "Codominance", "Linkage"],
       "In PKU one faulty enzyme causes mental retardation, pale skin and hair, and eczema.",
       "একটা জিন যখন কয়েকটি আলাদা বৈশিষ্ট্যে প্রভাব ফেলে (যেমন ফিনাইলকিটোনিউরিয়ায়), তখন দেখা যায়…", ["প্লিওট্রপি", "বহুজিনীয় উত্তরাধিকার", "সহপ্রকটতা", "সংযোগ"],
       "পিকেইউ-তে একটা ত্রুটিপূর্ণ উৎসেচক মানসিক প্রতিবন্ধকতা, ফ্যাকাশে ত্বক-চুল আর একজিমা ঘটায়।"),
    _q("Klinefelter's syndrome has which karyotype?", ["47, XXY", "45, XO", "47, XX + 21", "47, XYY"],
       "An extra X in a male causes tall stature, small testes, sterility and sometimes breast development.",
       "ক্লাইনফেল্টার সিনড্রোমের ক্যারিওটাইপ কী?", ["47, XXY ক্যারিওটাইপ", "45, XO ক্যারিওটাইপ", "47, XX + 21 ক্যারিওটাইপ", "47, XYY ক্যারিওটাইপ"],
       "পুরুষে একটা বাড়তি X লম্বা গড়ন, ছোট শুক্রাশয়, বন্ধ্যাত্ব আর কখনো স্তনবৃদ্ধি ঘটায়।"),
    _q("Turner's syndrome (45, XO) affects…", ["Females, who are short and have underdeveloped ovaries", "Males, who are very tall", "Both sexes equally, with an extra chromosome 21", "Only plants"],
       "Monosomy of the X chromosome; it arises from non-disjunction in a parent's meiosis.",
       "টার্নার সিনড্রোম (45, XO) কাদের হয়?", ["নারীদের, যারা খর্বকায় আর ডিম্বাশয় অপরিণত", "পুরুষদের, যারা খুব লম্বা", "উভয় লিঙ্গের, বাড়তি 21 নম্বর ক্রোমোজোম নিয়ে", "কেবল উদ্ভিদের"],
       "X ক্রোমোজোমের একসূত্রতা; মা-বাবার মিয়োসিসে অ-বিযোজন থেকে ঘটে।"),
    _q("Thalassemia differs from sickle-cell anaemia because thalassemia is…", ["A quantitative problem - too little of a globin chain is made", "A qualitative problem - one amino acid is wrong", "Caused by a virus", "X-linked"],
       "Sickle-cell is a single substitution (Glu → Val at position 6 of β-globin); thalassemia reduces α or β chain synthesis.",
       "থ্যালাসেমিয়া সিকল-সেল রক্তাল্পতা থেকে আলাদা কারণ থ্যালাসেমিয়া…", ["পরিমাণগত সমস্যা - একটা গ্লোবিন শৃঙ্খল খুব কম তৈরি হয়", "গুণগত সমস্যা - একটা অ্যামিনো অ্যাসিড ভুল", "ভাইরাস-ঘটিত", "X-সংযুক্ত"],
       "সিকল-সেল একটা প্রতিস্থাপন (বিটা-গ্লোবিনের 6 নম্বরে গ্লু → ভ্যাল); থ্যালাসেমিয়ায় আলফা বা বিটা শৃঙ্খল কম তৈরি হয়।"),
    _q("A trait passed by an affected mother to all her children, but never by an affected father, suggests…", ["Mitochondrial inheritance", "Autosomal dominant inheritance", "Y-linked inheritance", "X-linked recessive inheritance"],
       "Mitochondria come from the egg's cytoplasm; sperm contribute essentially none.",
       "আক্রান্ত মা থেকে সব সন্তানে যায়, কিন্তু আক্রান্ত বাবা থেকে কখনো নয় - এমন বৈশিষ্ট্য ইঙ্গিত করে…", ["মাইটোকন্ড্রিয়ার উত্তরাধিকার", "অটোজোমীয় প্রকট উত্তরাধিকার", "Y-সংযুক্ত উত্তরাধিকার", "X-সংযুক্ত প্রচ্ছন্ন উত্তরাধিকার"],
       "মাইটোকন্ড্রিয়া আসে ডিম্বাণুর সাইটোপ্লাজম থেকে; শুক্রাণু প্রায় কিছুই দেয় না।"),
    _q("A Barr body seen in the nucleus of a female cell is…", ["An inactivated, condensed X chromosome", "An extra nucleolus", "A Y chromosome", "A virus particle"],
       "One X is silenced in each female cell (dosage compensation); the number of Barr bodies = number of X - 1.",
       "নারীকোষের নিউক্লিয়াসে দেখা বার বডি হল…", ["একটা নিষ্ক্রিয়, ঘনীভূত X ক্রোমোজোম", "একটা বাড়তি নিউক্লিওলাস", "একটা Y ক্রোমোজোম", "একটা ভাইরাস কণা"],
       "প্রতিটি নারীকোষে একটা X নীরব থাকে (মাত্রা-ক্ষতিপূরণ); বার বডির সংখ্যা = X-এর সংখ্যা - 1।"),
    _q("In birds, the sex of the offspring is decided by…", ["The mother, since females are ZW and males ZZ", "The father, since males are XY", "Temperature only", "The number of chromosome sets"],
       "The female is the heterogametic sex in birds; in honeybees, unfertilised eggs become males (haplodiploidy).",
       "পাখিতে অপত্যের লিঙ্গ নির্ধারণ করে…", ["মা, কারণ স্ত্রী ZW আর পুরুষ ZZ", "বাবা, কারণ পুরুষ XY", "কেবল তাপমাত্রা", "ক্রোমোজোম-সেটের সংখ্যা"],
       "পাখিতে স্ত্রী বিষমজননকোষী লিঙ্গ; মৌমাছিতে অনিষিক্ত ডিম পুরুষ হয় (হ্যাপ্লো-ডিপ্লয়েডি)।"),
    _q("A male honeybee (drone) develops from…", ["An unfertilised egg, so it is haploid", "A fertilised egg fed royal jelly", "A fertilised egg fed honey", "Two fused eggs"],
       "Drones have 16 chromosomes and make sperm by mitosis; queens and workers are diploid with 32.",
       "পুরুষ মৌমাছি (ড্রোন) জন্মায়…", ["অনিষিক্ত ডিম থেকে, তাই এটা হ্যাপ্লয়েড", "রাজকীয় জেলি খাওয়া নিষিক্ত ডিম থেকে", "মধু খাওয়া নিষিক্ত ডিম থেকে", "দুটি মিলিত ডিম থেকে"],
       "ড্রোনে 16টি ক্রোমোজোম, মাইটোসিসে শুক্রাণু তৈরি করে; রানি আর কর্মী ডিপ্লয়েড, 32টি।"),
    _q("Genes A and B are 10 map units apart, B and C 15, and A and C 25. The gene order is…", ["A - B - C", "B - A - C", "A - C - B", "Cannot be told"],
       "The two shorter distances add up to the longest (10 + 15 = 25), so B lies in the middle.",
       "জিন A আর B-এর দূরত্ব 10 মানচিত্র-একক, B আর C-এর 15, A আর C-এর 25। জিনগুলোর ক্রম…", ["A - B - C", "B - A - C", "A - C - B", "বলা যায় না"],
       "ছোট দুটি দূরত্ব মিলে সবচেয়ে বড়টি (10 + 15 = 25), তাই B মাঝখানে।"),
    _q("A woman with blood group O marries a man with AB. Which blood group can their child NOT have?", ["O or AB", "A only", "B only", "A or B"],
       "ii x IᴬIᴮ gives only Iᴬi (A) and Iᴮi (B) children.",
       "রক্তগ্রুপ O-এর একজন নারী AB-এর একজন পুরুষকে বিয়ে করেন। তাঁদের সন্তানের কোন রক্তগ্রুপ হতে পারে না?", ["O বা AB", "কেবল A", "কেবল B", "A বা B"],
       "ii x IᴬIᴮ থেকে কেবল Iᴬi (A) আর Iᴮi (B) সন্তান হয়।"),
    _q("Genomic imprinting means that…", ["Some genes are expressed only from the copy inherited from one particular parent", "All genes are copied twice", "Genes move between chromosomes", "Mutations are repaired"],
       "Methylation marks the silent copy; Prader-Willi and Angelman syndromes come from the same region depending on the parent.",
       "জিনোমিক ইমপ্রিন্টিং মানে…", ["কিছু জিন কেবল একজন নির্দিষ্ট অভিভাবক থেকে পাওয়া প্রতিলিপি থেকে প্রকাশিত হয়", "সব জিন দুবার প্রতিলিপি হয়", "জিন ক্রোমোজোমের মধ্যে সরে যায়", "মিউটেশন মেরামত হয়"],
       "মিথাইলেশন নীরব প্রতিলিপিকে চিহ্নিত করে; প্রাডার-উইলি আর অ্যাঞ্জেলম্যান সিনড্রোম একই অঞ্চল থেকে, অভিভাবক অনুযায়ী।"),
    # ---------------------------------------------------------------- evolution
    _q("A small group of settlers founds a new population whose allele frequencies differ by chance from the parent population. This is…", ["The founder effect", "Natural selection", "Gene flow", "Mutation pressure"],
       "A form of genetic drift; a sudden crash in numbers (a bottleneck) has a similar effect.",
       "একদল অল্প বসতিস্থাপক নতুন জনগোষ্ঠী গড়ে, যার অ্যালিল-হার দৈবাৎ মূল জনগোষ্ঠী থেকে আলাদা। এটা…", ["প্রতিষ্ঠাতা প্রভাব", "প্রাকৃতিক নির্বাচন", "জিন-প্রবাহ", "মিউটেশন-চাপ"],
       "এটা জিনগত প্রবাহের এক রূপ; সংখ্যায় হঠাৎ ধস (বোতলের গলা) একই রকম প্রভাব ফেলে।"),
    _q("Australian marsupials evolving into many forms that resemble placental mammals elsewhere show…", ["Adaptive radiation within the group and convergent evolution with placentals", "Only divergent evolution", "Genetic drift alone", "Lamarck's inheritance of acquired characters"],
       "From one ancestor they spread into many niches; the marsupial mole and placental mole look alike because they live alike.",
       "অস্ট্রেলিয়ার মারসুপিয়ালরা নানা রূপে বিবর্তিত হয়ে অন্যত্রের অমরাযুক্ত স্তন্যপায়ীদের মতো দেখতে হয়েছে - এটা দেখায়…", ["গোষ্ঠীর মধ্যে অভিযোজনমূলক বিকিরণ আর অমরাযুক্তদের সঙ্গে অভিসারী বিবর্তন", "কেবল অপসারী বিবর্তন", "কেবল জিনগত প্রবাহ", "ল্যামার্কের অর্জিত বৈশিষ্ট্যের উত্তরাধিকার"],
       "এক পূর্বপুরুষ থেকে তারা নানা আবাসে ছড়ায়; মারসুপিয়াল ছুঁচো আর অমরাযুক্ত ছুঁচো একই জীবনযাত্রায় একই রকম দেখতে।"),
    _q("Miller and Urey's 1953 experiment showed that…", ["Amino acids can form from simple gases (CH₄, NH₃, H₂, H₂O) with electric sparks", "Life arises from non-living matter every day", "DNA was the first genetic material", "Cells come only from cells"],
       "It supported the Oparin-Haldane idea of chemical evolution in the early Earth's reducing atmosphere.",
       "মিলার আর ইউরির 1953 সালের পরীক্ষা দেখায় যে…", ["সরল গ্যাস (CH₄, NH₃, H₂, H₂O) থেকে বৈদ্যুতিক স্ফুলিঙ্গে অ্যামিনো অ্যাসিড তৈরি হতে পারে", "প্রতিদিন জড় থেকে প্রাণ জন্মায়", "ডিএনএ প্রথম জিনগত উপাদান ছিল", "কোষ কেবল কোষ থেকেই আসে"],
       "এটা আদি পৃথিবীর বিজারক বায়ুমণ্ডলে রাসায়নিক বিবর্তনের ওপারিন-হ্যালডেন ধারণাকে সমর্থন করে।"),
    _q("Selection that favours both extremes of a trait over the average is called…", ["Disruptive selection", "Stabilising selection", "Directional selection", "Artificial selection"],
       "It can split a population into two forms; stabilising selection favours the average (e.g. human birth weight).",
       "যে নির্বাচন কোনো বৈশিষ্ট্যের গড়ের চেয়ে দুই প্রান্তকে বেশি সুবিধা দেয়, তাকে বলে…", ["বিভাজনমূলক নির্বাচন", "স্থিতিশীল নির্বাচন", "দিকনির্দেশক নির্বাচন", "কৃত্রিম নির্বাচন"],
       "এটা জনগোষ্ঠীকে দুটি রূপে ভাগ করতে পারে; স্থিতিশীল নির্বাচন গড়কে সুবিধা দেয় (যেমন মানুষের জন্ম-ওজন)।"),
    _q("Speciation that happens when a population is split by a geographical barrier is…", ["Allopatric speciation", "Sympatric speciation", "Polyploidy only", "Convergent evolution"],
       "Separated groups accumulate different mutations and selection until they can no longer interbreed.",
       "ভৌগোলিক বাধায় জনগোষ্ঠী ভাগ হয়ে যে প্রজাতি-সৃষ্টি হয়, তা হল…", ["বিচ্ছিন্নভূমি (অ্যালোপ্যাট্রিক) প্রজাতি-সৃষ্টি", "সহভূমি (সিমপ্যাট্রিক) প্রজাতি-সৃষ্টি", "কেবল বহুপ্লয়েডি", "অভিসারী বিবর্তন"],
       "আলাদা দলগুলোতে ভিন্ন মিউটেশন আর নির্বাচন জমে, শেষে তারা আর আন্তঃপ্রজনন করতে পারে না।"),
    _q("Archaeopteryx is called a connecting link between…", ["Reptiles and birds", "Fish and amphibians", "Apes and humans", "Plants and animals"],
       "It had feathers and wings like a bird, but teeth, clawed fingers and a long bony tail like a reptile.",
       "আর্কিওপটেরিক্সকে কাদের মধ্যে সংযোগকারী বলা হয়?", ["সরীসৃপ আর পাখি", "মাছ আর উভচর", "বনমানুষ আর মানুষ", "উদ্ভিদ আর প্রাণী"],
       "এর পাখির মতো পালক আর ডানা, কিন্তু সরীসৃপের মতো দাঁত, নখরযুক্ত আঙুল আর লম্বা হাড়ের লেজ ছিল।"),
    _q("Homologous organs are evidence for…", ["Divergent evolution from a common ancestor", "Convergent evolution", "Spontaneous generation", "Inheritance of acquired characters"],
       "Same basic structure, different uses (e.g. forelimbs of whale, bat, cheetah and human).",
       "সমসংস্থ অঙ্গ কীসের প্রমাণ?", ["সাধারণ পূর্বপুরুষ থেকে অপসারী বিবর্তনের", "অভিসারী বিবর্তনের", "স্বতঃস্ফূর্ত উৎপত্তির", "অর্জিত বৈশিষ্ট্যের উত্তরাধিকারের"],
       "মূল গঠন এক, কাজ আলাদা (যেমন তিমি, বাদুড়, চিতা আর মানুষের অগ্রপদ)।"),
    # ---------------------------------------------------------------- cells
    _q("Cells that leave the cell cycle and stop dividing, such as mature neurons, are in…", ["G₀ phase", "S phase", "G₂ phase", "M phase"],
       "G₀ is a quiescent state; some cells (like liver cells) can re-enter G₁ when needed.",
       "যে কোষ কোষচক্র ছেড়ে বিভাজন থামায়, যেমন পরিণত নিউরন, তারা থাকে…", ["G₀ দশায়", "S দশায়", "G₂ দশায়", "M দশায়"],
       "G₀ একটা নিষ্ক্রিয় অবস্থা; কিছু কোষ (যেমন যকৃৎ কোষ) দরকারে আবার G₁-এ ফেরে।"),
    _q("The cell cycle is driven forward mainly by…", ["Cyclins binding cyclin-dependent kinases (CDKs)", "Ribosomes", "Lysosomes", "The cell wall"],
       "Cyclin levels rise and fall; active cyclin-CDK complexes phosphorylate targets at checkpoints such as G₁/S and G₂/M.",
       "কোষচক্রকে মূলত এগিয়ে নিয়ে যায়…", ["সাইক্লিন-নির্ভর কাইনেজের (সিডিকে) সঙ্গে যুক্ত সাইক্লিন", "রাইবোজোম", "লাইসোজোম", "কোষপ্রাচীর"],
       "সাইক্লিনের মাত্রা ওঠানামা করে; সক্রিয় সাইক্লিন-সিডিকে জোট G₁/S আর G₂/M-এর মতো নিয়ন্ত্রণ-বিন্দুতে লক্ষ্যকে ফসফরিলেট করে।"),
    _q("Colchicine is used to make polyploid plants because it…", ["Stops spindle formation, so duplicated chromosomes stay in one nucleus", "Breaks DNA", "Kills the cell wall", "Speeds up meiosis"],
       "It binds tubulin; the chromosome number doubles because the cell skips division.",
       "বহুপ্লয়েড উদ্ভিদ তৈরিতে কলচিসিন ব্যবহৃত হয় কারণ এটা…", ["তন্তু-যন্ত্র গঠন থামায়, তাই দ্বিগুণ ক্রোমোজোম একই নিউক্লিয়াসে থাকে", "ডিএনএ ভাঙে", "কোষপ্রাচীর নষ্ট করে", "মিয়োসিস দ্রুত করে"],
       "এটা টিউবিউলিনে বাঁধে; কোষ বিভাজন এড়ায় বলে ক্রোমোজোম-সংখ্যা দ্বিগুণ হয়।"),
    _q("In which sub-stage of prophase I does the synaptonemal complex form as homologues pair?", ["Zygotene", "Leptotene", "Diplotene", "Diakinesis"],
       "Leptotene: threads condense; zygotene: synapsis; pachytene: crossing over; diplotene: chiasmata visible; diakinesis: terminalisation.",
       "প্রথম প্রোফেজের কোন উপদশায় সমসংস্থ ক্রোমোজোম জোড় বাঁধলে সিন্যাপটোনিমাল জটিল তৈরি হয়?", ["জাইগোটিন", "লেপ্টোটিন", "ডিপ্লোটিন", "ডায়াকাইনেসিস"],
       "লেপ্টোটিন: সুতো ঘন হয়; জাইগোটিন: জোড় বাঁধা; প্যাকিটিন: ক্রসিং ওভার; ডিপ্লোটিন: কায়াজমা দেখা যায়; ডায়াকাইনেসিস: প্রান্তসরণ।"),
    _q("Cilia and flagella of eukaryotic cells have which arrangement of microtubules?", ["9 + 2", "9 + 0", "9 x 3 triplets with no centre", "2 + 2"],
       "Nine outer doublets surround two central singlets; the basal body (like a centriole) has 9 triplets and no centre.",
       "সুকেন্দ্রিক কোষের সিলিয়া আর ফ্ল্যাজেলায় অণুনালিকার বিন্যাস কেমন?", ["9 + 2", "9 + 0", "কেন্দ্রহীন 9টি ত্রয়ী", "2 + 2"],
       "বাইরের নয়টি জোড় দুটি কেন্দ্রীয় একক ঘিরে থাকে; মূলদেহে (সেন্ট্রিওলের মতো) 9টি ত্রয়ী, কেন্দ্র নেই।"),
    _q("Which organelle is the main site of lipid and steroid synthesis and drug detoxification in liver cells?", ["Smooth endoplasmic reticulum", "Rough endoplasmic reticulum", "Golgi apparatus", "Nucleolus"],
       "SER lacks ribosomes; RER makes proteins for secretion and membranes.",
       "যকৃৎ কোষে লিপিড ও স্টেরয়েড সংশ্লেষ আর ওষুধ বিষমুক্ত করার প্রধান অঙ্গাণু কোনটি?", ["মসৃণ অন্তঃপ্লাজমীয় জালিকা", "অমসৃণ অন্তঃপ্লাজমীয় জালিকা", "গলগি বস্তু", "নিউক্লিওলাস"],
       "মসৃণ জালিকায় রাইবোজোম নেই; অমসৃণটি ক্ষরণ আর পর্দার জন্য প্রোটিন বানায়।"),
    _q("Glyoxysomes in germinating oily seeds…", ["Convert stored fats into sugars through the glyoxylate cycle", "Make chlorophyll", "Store starch", "Digest the cell wall"],
       "Animals lack this pathway, so they cannot turn fat into glucose.",
       "অঙ্কুরিত তৈলবীজে গ্লাইঅক্সিজোম…", ["গ্লাইঅক্সিলেট চক্রে সঞ্চিত চর্বিকে শর্করায় বদলায়", "ক্লোরোফিল তৈরি করে", "শ্বেতসার জমায়", "কোষপ্রাচীর পরিপাক করে"],
       "প্রাণীর এই পথ নেই, তাই তারা চর্বিকে গ্লুকোজে বদলাতে পারে না।"),
    _q("Prions, which cause mad cow disease, are…", ["Misfolded proteins that make normal proteins misfold too", "Viruses with RNA genomes", "Bacteria without walls", "Viroids of free RNA"],
       "They contain no nucleic acid; viroids (potato spindle tuber) are naked RNA without a protein coat.",
       "পাগলা গরু রোগ ঘটানো প্রিয়ন হল…", ["ভুলভাবে ভাঁজ হওয়া প্রোটিন, যা স্বাভাবিক প্রোটিনকেও ভুল ভাঁজে ফেলে", "আরএনএ জিনোমের ভাইরাস", "প্রাচীরহীন ব্যাকটেরিয়া", "মুক্ত আরএনএ-র ভাইরয়েড"],
       "এতে কোনো নিউক্লিক অ্যাসিড নেই; ভাইরয়েড (আলুর স্পিন্ডল টিউবার) প্রোটিন-আবরণহীন খালি আরএনএ।"),
    _q("A ribosome of a eukaryotic cell (80S) is made of which subunits?", ["60S and 40S", "50S and 30S", "40S and 40S", "70S and 10S"],
       "Svedberg units measure sedimentation, so they do not simply add; bacterial 70S = 50S + 30S.",
       "সুকেন্দ্রিক কোষের রাইবোজোম (80S) কোন উপ-একক দিয়ে তৈরি?", ["60S আর 40S", "50S আর 30S", "40S আর 40S", "70S আর 10S"],
       "স্ভেডবার্গ একক থিতিয়ে পড়ার হার মাপে, তাই সরাসরি যোগ হয় না; ব্যাকটেরিয়ার 70S = 50S + 30S।"),
    _q("Which enzyme property does a competitive inhibitor change?", ["It raises the apparent Km but leaves Vmax unchanged", "It lowers Vmax but leaves Km unchanged", "It destroys the enzyme", "It changes the enzyme's amino acids"],
       "Enough substrate can out-compete the inhibitor; malonate inhibiting succinate dehydrogenase is the classic case.",
       "প্রতিযোগী নিরোধক উৎসেচকের কোন ধর্ম বদলায়?", ["আপাত Km বাড়ায় কিন্তু Vmax একই রাখে", "Vmax কমায় কিন্তু Km একই রাখে", "উৎসেচক ধ্বংস করে", "উৎসেচকের অ্যামিনো অ্যাসিড বদলায়"],
       "যথেষ্ট সাবস্ট্রেট নিরোধককে হারাতে পারে; সাক্সিনেট ডিহাইড্রোজিনেজকে ম্যালোনেটের নিরোধন চিরাচরিত উদাহরণ।"),
    _q("A non-protein organic group tightly bound to an enzyme, like haem in catalase, is a…", ["Prosthetic group", "Substrate", "Competitive inhibitor", "Isozyme"],
       "Loosely bound organic cofactors (NAD⁺, FAD) are coenzymes; metal ions such as Zn²⁺ are also cofactors.",
       "উৎসেচকে শক্তভাবে যুক্ত একটা অ-প্রোটিন জৈব অংশ, যেমন ক্যাটালেজে হিম, হল…", ["প্রস্থেটিক গ্রুপ", "সাবস্ট্রেট", "প্রতিযোগী নিরোধক", "আইসোজাইম"],
       "শিথিলভাবে যুক্ত জৈব সহ-উপাদান (NAD⁺, FAD) হল কো-এনজাইম; Zn²⁺-এর মতো ধাতব আয়নও সহ-উপাদান।"),
    _q("The two strands of DNA are antiparallel. This means…", ["One runs 5' → 3' and the other 3' → 5'", "They are identical in sequence", "They never separate", "They are made of different sugars"],
       "That is why the lagging strand must be made in pieces: polymerase only adds to a 3' end.",
       "ডিএনএ-র দুটি সূত্র প্রতিসমান্তরাল। এর মানে…", ["একটি 5' → 3' আর অন্যটি 3' → 5' দিকে চলে", "অনুক্রমে দুটি অভিন্ন", "এরা কখনো আলাদা হয় না", "এরা আলাদা শর্করায় তৈরি"],
       "তাই পশ্চাদ্গামী সূত্র খণ্ডে খণ্ডে তৈরি করতে হয়: পলিমারেজ কেবল 3' প্রান্তে যোগ করে।"),
    _q("In eukaryotes, DNA is packed around histone octamers into…", ["Nucleosomes, about 200 base pairs each with linker DNA", "Plasmids", "Ribosomes", "Operons"],
       "Positively charged histones (rich in lysine and arginine) bind negatively charged DNA - 'beads on a string'.",
       "সুকেন্দ্রিকে ডিএনএ হিস্টোন অক্টামারের চারপাশে প্যাঁচিয়ে তৈরি করে…", ["নিউক্লিওজোম, সংযোগকারী ডিএনএ-সহ প্রতিটি প্রায় 200 ক্ষারক-জোড়া", "প্লাজমিড", "রাইবোজোম", "অপেরন"],
       "ধনাত্মক হিস্টোন (লাইসিন আর আর্জিনিনে সমৃদ্ধ) ঋণাত্মক ডিএনএ-কে বাঁধে - 'সুতোয় গাঁথা পুঁতি'।"),
    _q("Which statement about introns and exons is correct?", ["Exons are kept in mature mRNA; introns are removed", "Introns are kept in mature mRNA", "Bacteria have many introns", "Exons never code for protein"],
       "Alternative splicing joins exons in different combinations, so one gene can make several proteins.",
       "ইনট্রন আর এক্সন সম্পর্কে কোন বিবৃতি সঠিক?", ["পরিণত এমআরএনএ-তে এক্সন থাকে; ইনট্রন বাদ যায়", "পরিণত এমআরএনএ-তে ইনট্রন থাকে", "ব্যাকটেরিয়ায় অনেক ইনট্রন", "এক্সন কখনো প্রোটিনের সংকেত দেয় না"],
       "বিকল্প স্প্লাইসিং এক্সনগুলোকে নানা সংমিশ্রণে জোড়ে, তাই একটা জিন কয়েকটি প্রোটিন বানাতে পারে।"),
    _q("Which technique amplifies a specific DNA segment millions of times in a few hours?", ["The polymerase chain reaction (PCR)", "Southern blotting", "Gel electrophoresis", "Microinjection"],
       "Cycles of denaturation (94 °C), primer annealing and extension double the target each round.",
       "কোন কৌশল কয়েক ঘণ্টায় একটা নির্দিষ্ট ডিএনএ অংশকে লক্ষ লক্ষ গুণ বাড়ায়?", ["পলিমারেজ শৃঙ্খল বিক্রিয়া (পিসিআর)", "সাদার্ন ব্লটিং", "জেল তড়িৎ-কণা সঞ্চালন", "অণু-ইনজেকশন"],
       "বিভাজন (94 °C), প্রাইমার সংযুক্তি আর প্রসারণের প্রতিটি চক্রে লক্ষ্য দ্বিগুণ হয়।"),
    _q("A probe that reveals a specific DNA fragment on a membrane after electrophoresis is used in…", ["Southern blotting", "Northern blotting (for RNA)", "Western blotting (for protein)", "ELISA"],
       "Named after Edwin Southern; Northern and Western blots were named in fun for RNA and proteins.",
       "তড়িৎ-কণা সঞ্চালনের পরে একটা পর্দায় নির্দিষ্ট ডিএনএ খণ্ড দেখাতে প্রোব ব্যবহার হয়…", ["সাদার্ন ব্লটিংয়ে", "নর্দার্ন ব্লটিংয়ে (আরএনএ-র জন্য)", "ওয়েস্টার্ন ব্লটিংয়ে (প্রোটিনের জন্য)", "এলাইজায়"],
       "এডউইন সাদার্নের নামে; আরএনএ আর প্রোটিনের জন্য মজা করে নর্দার্ন আর ওয়েস্টার্ন নাম দেওয়া হয়।"),
    _q("Which statement about the human genome is correct?", ["Less than 2% of it codes for proteins", "Every base codes for a protein", "It has about 100,000 genes", "Men and women differ in most genes"],
       "About 20,000-25,000 genes; much of the rest is regulatory, repetitive or of unknown function.",
       "মানব জিনোম সম্পর্কে কোন বিবৃতি সঠিক?", ["এর 2%-এরও কম প্রোটিনের সংকেত দেয়", "প্রতিটি ক্ষারক প্রোটিনের সংকেত দেয়", "এতে প্রায় 1,00,000 জিন", "নারী-পুরুষে বেশির ভাগ জিন আলাদা"],
       "প্রায় 20,000-25,000 জিন; বাকির বেশির ভাগ নিয়ন্ত্রক, পুনরাবৃত্ত বা অজানা কাজের।"),
    _q("Single nucleotide polymorphisms (SNPs) are…", ["Single-base differences between individuals at the same position", "Whole extra chromosomes", "Viruses inside the genome", "Changes in ribosome number"],
       "Millions exist in each person; they help trace ancestry, disease risk and drug response.",
       "সিঙ্গল নিউক্লিওটাইড পলিমরফিজম (এসএনপি) হল…", ["একই অবস্থানে ব্যক্তিভেদে একটা ক্ষারকের পার্থক্য", "গোটা বাড়তি ক্রোমোজোম", "জিনোমের ভেতরের ভাইরাস", "রাইবোজোম-সংখ্যার পরিবর্তন"],
       "প্রত্যেকের লক্ষ লক্ষ আছে; বংশধারা, রোগের ঝুঁকি আর ওষুধে সাড়া খুঁজতে সাহায্য করে।"),
    _q("Which statement about the lac operon is true when both glucose and lactose are present?", ["Transcription stays low, because low cAMP leaves CAP inactive (catabolite repression)", "Transcription is at its maximum", "The repressor binds lactose and the operator together", "The operon is deleted"],
       "Cells use glucose first; only when glucose falls does cAMP-CAP boost lac transcription.",
       "গ্লুকোজ আর ল্যাকটোজ দুটোই থাকলে ল্যাক অপেরন সম্পর্কে কোন বিবৃতি সত্য?", ["প্রতিলিপন কম থাকে, কারণ কম সিএএমপি-তে ক্যাপ নিষ্ক্রিয় (ক্যাটাবোলাইট অবদমন)", "প্রতিলিপন সর্বোচ্চ", "অবদমক ল্যাকটোজ আর অপারেটরে একসঙ্গে বাঁধে", "অপেরন মুছে যায়"],
       "কোষ আগে গ্লুকোজ ব্যবহার করে; গ্লুকোজ কমলে তবেই সিএএমপি-ক্যাপ ল্যাক প্রতিলিপন বাড়ায়।"),
    _q("A plasmid carrying genes for resistance to two antibiotics (such as pBR322) helps in…", ["Selecting transformed cells and spotting recombinants by insertional inactivation", "Making the bacteria grow faster", "Killing viruses", "Measuring DNA length"],
       "Cells growing on ampicillin but not on tetracycline carry a plasmid with an insert in the tet gene.",
       "দুটি অ্যান্টিবায়োটিক-প্রতিরোধী জিনযুক্ত প্লাজমিড (যেমন pBR322) কাজে লাগে…", ["রূপান্তরিত কোষ বাছতে আর সন্নিবেশ-নিষ্ক্রিয়করণে পুনর্যোজিত চিনতে", "ব্যাকটেরিয়াকে দ্রুত বাড়াতে", "ভাইরাস মারতে", "ডিএনএ-র দৈর্ঘ্য মাপতে"],
       "যে কোষ অ্যাম্পিসিলিনে বাড়ে কিন্তু টেট্রাসাইক্লিনে নয়, তার প্লাজমিডে টেট জিনের মধ্যে কিছু ঢুকেছে।"),
    _q("Which enzyme is used to dissolve the cell wall when isolating DNA from a fungus?", ["Chitinase", "Cellulase", "Lysozyme", "Ribonuclease"],
       "Fungal walls are chitin; plant walls need cellulase and bacterial walls lysozyme.",
       "ছত্রাক থেকে ডিএনএ বের করতে কোষপ্রাচীর গলাতে কোন উৎসেচক ব্যবহৃত হয়?", ["কাইটিনেজ", "সেলুলেজ", "লাইসোজাইম", "রাইবোনিউক্লিয়েজ"],
       "ছত্রাকের প্রাচীর কাইটিনের; উদ্ভিদে সেলুলেজ আর ব্যাকটেরিয়ায় লাইসোজাইম লাগে।"),
    _q("Polyploids that combine the chromosome sets of two different species, like Triticale, are…", ["Allopolyploids", "Autopolyploids", "Aneuploids", "Haploids"],
       "Triticale = wheat x rye with doubled chromosomes; an autopolyploid multiplies one species' own set.",
       "দুটি ভিন্ন প্রজাতির ক্রোমোজোম-সেট মেলানো বহুপ্লয়েড, যেমন ট্রিটিকেল, হল…", ["অ্যালোপলিপ্লয়েড", "অটোপলিপ্লয়েড", "অ্যানিউপ্লয়েড", "হ্যাপ্লয়েড"],
       "ট্রিটিকেল = গম x রাই, ক্রোমোজোম দ্বিগুণ করে; অটোপলিপ্লয়েড একই প্রজাতির নিজের সেট বাড়ায়।"),
    _q("In human evolution, which species first used stone tools and is called 'handy man'?", ["Homo habilis", "Homo erectus", "Homo neanderthalensis", "Ramapithecus"],
       "About 2 million years ago, with a brain of 650-800 cc; Homo erectus (about 900 cc) probably used fire.",
       "মানব বিবর্তনে কোন প্রজাতি প্রথম পাথরের হাতিয়ার ব্যবহার করে, যাকে 'দক্ষ মানুষ' বলা হয়?", ["হোমো হ্যাবিলিস", "হোমো ইরেক্টাস", "হোমো নিয়ান্ডারথালেনসিস", "রামাপিথেকাস"],
       "প্রায় 20 লক্ষ বছর আগে, মস্তিষ্ক 650-800 cc; হোমো ইরেক্টাস (প্রায় 900 cc) সম্ভবত আগুন ব্যবহার করত।"),
]
CONCEPTS += [
    # ---------------------------------------------------------------- bioenergetics and photosynthesis
    _q("According to Mitchell's chemiosmotic theory, ATP synthase makes ATP using…", ["The flow of protons back down their gradient across the membrane", "Direct transfer of electrons to ADP", "Heat from respiration", "Light energy directly"],
       "Electron transport pumps H⁺ out (into the intermembrane space or thylakoid lumen); H⁺ returning through F₀ turns the F₁ head.",
       "মিচেলের রসায়ন-অভিস্রবণ তত্ত্ব অনুযায়ী এটিপি সিন্থেজ এটিপি তৈরি করে…", ["পর্দার ওপারে প্রোটনের নতিপথে ফিরে আসা প্রবাহ দিয়ে", "সরাসরি ADP-তে ইলেকট্রন দিয়ে", "শ্বসনের তাপ দিয়ে", "সরাসরি আলোক শক্তি দিয়ে"],
       "ইলেকট্রন পরিবহন H⁺ বাইরে পাম্প করে (আন্তঃপর্দা স্থানে বা থাইলাকয়েড গহ্বরে); F₀ দিয়ে ফেরা H⁺ F₁ মাথা ঘোরায়।"),
    _q("Cyanide is deadly because it blocks…", ["Cytochrome c oxidase (complex IV), stopping the electron transport chain", "Glycolysis only", "Haemoglobin synthesis", "DNA replication"],
       "With complex IV blocked, oxygen cannot accept electrons and ATP production by oxidative phosphorylation stops.",
       "সায়ানাইড মারাত্মক কারণ এটা আটকায়…", ["সাইটোক্রোম সি অক্সিডেজ (চতুর্থ জটিল), ইলেকট্রন পরিবহন শৃঙ্খল থামিয়ে", "কেবল গ্লাইকোলাইসিস", "হিমোগ্লোবিন সংশ্লেষ", "ডিএনএ প্রতিলিপন"],
       "চতুর্থ জটিল আটকালে অক্সিজেন ইলেকট্রন নিতে পারে না, জারণমূলক ফসফোরাইলেশনে এটিপি তৈরি থেমে যায়।"),
    _q("What is the final electron acceptor in aerobic respiration?", ["Oxygen, which becomes water", "NAD⁺", "Carbon dioxide", "Pyruvate"],
       "Without O₂ the chain backs up; in fermentation pyruvate (or acetaldehyde) accepts electrons from NADH instead.",
       "সবাত শ্বসনে শেষ ইলেকট্রন গ্রাহক কী?", ["অক্সিজেন, যা জলে পরিণত হয়", "এনএডি⁺", "কার্বন ডাইঅক্সাইড", "পাইরুভেট"],
       "অক্সিজেন না থাকলে শৃঙ্খল আটকে যায়; গাঁজনে বরং পাইরুভেট (বা অ্যাসিট্যালডিহাইড) NADH থেকে ইলেকট্রন নেয়।"),
    _q("The reaction centre of photosystem II absorbs best at…", ["680 nm (P680)", "700 nm (P700)", "450 nm", "550 nm"],
       "PS II splits water and passes electrons to PS I (P700), which reduces NADP⁺.",
       "দ্বিতীয় ফটোসিস্টেমের প্রতিক্রিয়া-কেন্দ্র সবচেয়ে ভালো শোষণ করে…", ["680 nm-এ (P680)", "700 nm-এ (P700)", "450 nm-এ", "550 nm-এ"],
       "দ্বিতীয় ফটোসিস্টেম জল ভাঙে আর প্রথম ফটোসিস্টেমে (P700) ইলেকট্রন দেয়, যা NADP⁺ বিজারিত করে।"),
    _q("Cyclic photophosphorylation produces…", ["ATP only, using photosystem I alone", "ATP, NADPH and O₂", "NADPH only", "Glucose directly"],
       "Electrons from P700 return to it via cytochromes; no water is split, so no O₂ or NADPH forms.",
       "চক্রীয় ফটোফসফোরাইলেশনে তৈরি হয়…", ["কেবল এটিপি, শুধু প্রথম ফটোসিস্টেম ব্যবহার করে", "এটিপি, এনএডিপিএইচ আর অক্সিজেন", "কেবল এনএডিপিএইচ", "সরাসরি গ্লুকোজ"],
       "P700-এর ইলেকট্রন সাইটোক্রোম ঘুরে তাতেই ফেরে; জল ভাঙে না, তাই অক্সিজেন বা এনএডিপিএইচ হয় না।"),
    _q("Emerson's enhancement effect showed that…", ["Two photosystems work together, since red plus far-red light gives more photosynthesis than either alone", "Plants need only blue light", "Chlorophyll absorbs green light best", "Oxygen comes from CO₂"],
       "Above 680 nm the yield drops (red drop); adding shorter red light restores it - evidence for PS I and PS II.",
       "এমারসনের বর্ধন-প্রভাব দেখায় যে…", ["দুটি ফটোসিস্টেম একসঙ্গে কাজ করে, কারণ লাল আর দূর-লাল আলো একসঙ্গে আলাদাভাবের চেয়ে বেশি সালোকসংশ্লেষ ঘটায়", "উদ্ভিদের কেবল নীল আলো লাগে", "ক্লোরোফিল সবুজ আলো সবচেয়ে ভালো শোষে", "অক্সিজেন আসে CO₂ থেকে"],
       "680 nm-এর ওপরে ফলন কমে (লাল পতন); ছোট তরঙ্গের লাল আলো যোগ করলে আবার বাড়ে - দুটি ফটোসিস্টেমের প্রমাণ।"),
    _q("C₄ plants have Kranz anatomy, in which…", ["Bundle-sheath cells with many chloroplasts surround the veins and run the Calvin cycle", "There are no stomata", "Leaves have no veins", "Mesophyll cells run the Calvin cycle alone"],
       "Mesophyll fixes CO₂ with PEP carboxylase into C₄ acids, which release CO₂ in the bundle sheath, keeping RuBisCO away from O₂.",
       "C₄ উদ্ভিদে ক্র্যাঞ্জ গঠন থাকে, যেখানে…", ["অনেক ক্লোরোপ্লাস্টযুক্ত আবরণী-কলার কোষ শিরা ঘিরে ক্যালভিন চক্র চালায়", "কোনো পত্ররন্ধ্র নেই", "পাতায় শিরা নেই", "কেবল মেসোফিল কোষ ক্যালভিন চক্র চালায়"],
       "মেসোফিল PEP কার্বক্সিলেজ দিয়ে CO₂-কে C₄ অ্যাসিডে বাঁধে, যা আবরণী-কলায় CO₂ ছাড়ে, রুবিস্কোকে অক্সিজেন থেকে দূরে রাখে।"),
    _q("CAM plants such as pineapple and cacti save water by…", ["Opening stomata at night to take in CO₂ and closing them by day", "Having no stomata", "Absorbing CO₂ through roots", "Never doing photosynthesis"],
       "CO₂ is stored as malic acid overnight and released for the Calvin cycle during the day - a separation in time, not space.",
       "আনারস আর ক্যাকটাসের মতো ক্যাম উদ্ভিদ জল বাঁচায়…", ["রাতে পত্ররন্ধ্র খুলে CO₂ নিয়ে আর দিনে বন্ধ রেখে", "কোনো পত্ররন্ধ্র না রেখে", "মূল দিয়ে CO₂ শোষণ করে", "কখনো সালোকসংশ্লেষ না করে"],
       "রাতে CO₂ ম্যালিক অ্যাসিড হিসেবে জমা থাকে, দিনে ক্যালভিন চক্রের জন্য ছাড়া হয় - স্থানে নয়, সময়ে আলাদা।"),
    _q("Gluconeogenesis is…", ["Making glucose from non-carbohydrate sources such as lactate, amino acids and glycerol", "Breaking glucose into pyruvate", "Storing glucose as glycogen", "Absorbing glucose in the gut"],
       "It happens mainly in the liver (and kidneys) during fasting, partly reversing glycolysis.",
       "গ্লুকোনিওজেনেসিস হল…", ["ল্যাকটেট, অ্যামিনো অ্যাসিড আর গ্লিসারলের মতো অ-শর্করা উৎস থেকে গ্লুকোজ তৈরি", "গ্লুকোজকে পাইরুভেটে ভাঙা", "গ্লুকোজকে গ্লাইকোজেন হিসেবে জমানো", "অন্ত্রে গ্লুকোজ শোষণ"],
       "উপবাসে মূলত যকৃতে (আর বৃক্কে) ঘটে, গ্লাইকোলাইসিসকে আংশিক উল্টে।"),
    _q("Which step links glycolysis to the Krebs cycle?", ["Oxidative decarboxylation of pyruvate to acetyl-CoA in the mitochondrial matrix", "Splitting fructose-1,6-bisphosphate", "The electron transport chain", "Photolysis of water"],
       "Pyruvate dehydrogenase releases one CO₂ and makes one NADH per pyruvate.",
       "কোন ধাপ গ্লাইকোলাইসিসকে ক্রেবস চক্রের সঙ্গে যুক্ত করে?", ["মাইটোকন্ড্রিয়ার ধাত্রে পাইরুভেটের জারণমূলক ডিকার্বক্সিলেশনে অ্যাসিটাইল-কোএ তৈরি", "ফ্রুক্টোজ-1,6-বিসফসফেট ভাঙা", "ইলেকট্রন পরিবহন শৃঙ্খল", "জলের আলোক-বিশ্লেষণ"],
       "পাইরুভেট ডিহাইড্রোজিনেজ প্রতি পাইরুভেটে একটা CO₂ ছাড়ে আর একটা NADH তৈরি করে।"),
    # ---------------------------------------------------------------- plant physiology
    _q("Pure water at atmospheric pressure has a water potential of…", ["Zero, the highest possible value", "-1 MPa", "+1 MPa", "Infinity"],
       "Adding solutes lowers it (makes it negative); water always moves from higher to lower water potential.",
       "বায়ুমণ্ডলীয় চাপে বিশুদ্ধ জলের জল-বিভব…", ["শূন্য, সম্ভাব্য সর্বোচ্চ মান", "-1 মেগাপ্যাসকেল", "+1 মেগাপ্যাসকেল", "অসীম"],
       "দ্রাব যোগ করলে কমে (ঋণাত্মক হয়); জল সবসময় বেশি থেকে কম জল-বিভবের দিকে যায়।"),
    _q("The Casparian strip in the root endodermis…", ["Blocks the apoplast path, forcing water and minerals through cell membranes", "Stores starch", "Makes root hairs", "Carries sugars upward"],
       "It is a band of suberin; the plant can thus choose which minerals enter the xylem.",
       "মূলের অন্তঃত্বকে ক্যাসপেরিয়ান স্ট্রিপ…", ["অ্যাপোপ্লাস্ট পথ আটকে জল আর খনিজকে কোষপর্দা দিয়ে যেতে বাধ্য করে", "শ্বেতসার জমায়", "মূলরোম তৈরি করে", "শর্করা ওপরে নিয়ে যায়"],
       "এটা সুবেরিনের একটা ফিতে; ফলে কোন খনিজ জাইলেমে ঢুকবে, উদ্ভিদ তা বেছে নিতে পারে।"),
    _q("Water drops seen at leaf margins early in the morning come out through hydathodes because of…", ["Root pressure (guttation)", "Transpiration pull", "Dew condensation only", "Photosynthesis"],
       "At night transpiration is low, so root pressure pushes xylem sap out of the leaf tips.",
       "ভোরে পাতার কিনারায় দেখা জলের ফোঁটা জলরন্ধ্র দিয়ে বেরোয় কারণ…", ["মূলজ চাপ (বিন্দুস্রাব)", "প্রস্বেদন টান", "কেবল শিশির জমা", "সালোকসংশ্লেষ"],
       "রাতে প্রস্বেদন কম, তাই মূলজ চাপ জাইলেম রসকে পাতার ডগা দিয়ে বের করে দেয়।"),
    _q("Münch's pressure-flow hypothesis explains…", ["Movement of sugars in the phloem from source to sink", "Rise of water in the xylem", "Opening of stomata", "Absorption of minerals"],
       "Sugar loading at the source draws in water, raising pressure that pushes sap towards sinks where sugar is unloaded.",
       "মুঞ্চের চাপ-প্রবাহ প্রকল্প ব্যাখ্যা করে…", ["ফ্লোয়েমে উৎস থেকে গ্রাহকে শর্করার চলাচল", "জাইলেমে জলের ওঠা", "পত্ররন্ধ্রের খোলা", "খনিজ শোষণ"],
       "উৎসে শর্করা ভরলে জল টানে, চাপ বাড়ে, যা রসকে সেই গ্রাহকের দিকে ঠেলে যেখানে শর্করা নামানো হয়।"),
    _q("Phytochrome switches to its active Pfr form when it absorbs…", ["Red light (about 660 nm)", "Far-red light (about 730 nm)", "Green light", "Ultraviolet only"],
       "Far-red light turns Pfr back to Pr; this switch controls germination of lettuce seeds and flowering.",
       "ফাইটোক্রোম কোন আলো শোষণ করলে সক্রিয় Pfr রূপে বদলায়?", ["লাল আলো (প্রায় 660 nm)", "দূর-লাল আলো (প্রায় 730 nm)", "সবুজ আলো", "কেবল অতিবেগুনি"],
       "দূর-লাল আলো Pfr-কে আবার Pr করে; এই সুইচ লেটুস বীজের অঙ্কুরোদ্গম আর ফুল ফোটা নিয়ন্ত্রণ করে।"),
    _q("Vernalisation means…", ["Promoting flowering by a period of low temperature", "Ripening fruits with ethylene", "Breaking dormancy with light", "Bending towards light"],
       "Winter varieties of wheat and rye flower only after chilling; it stops plants flowering too early in the season.",
       "বসন্তীকরণ মানে…", ["নিম্ন তাপমাত্রার একটা সময় দিয়ে ফুল ফোটানো ত্বরান্বিত করা", "ইথিলিন দিয়ে ফল পাকানো", "আলো দিয়ে সুপ্তি ভাঙা", "আলোর দিকে বাঁকা"],
       "শীতের জাতের গম আর রাই ঠান্ডা পাওয়ার পরেই ফুল দেয়; মরসুমের খুব আগে ফুল ফোটা আটকায়।"),
    _q("Which plant hormone delays leaf senescence (the Richmond-Lang effect)?", ["Cytokinin", "Abscisic acid", "Ethylene", "Gibberellin"],
       "Cytokinins promote cell division and nutrient mobilisation; ABA and ethylene speed up ageing and abscission.",
       "কোন উদ্ভিদ-হরমোন পাতার বার্ধক্য দেরি করায় (রিচমন্ড-ল্যাং প্রভাব)?", ["সাইটোকাইনিন", "অ্যাবসিসিক অ্যাসিড", "ইথিলিন", "জিবেরেলিন"],
       "সাইটোকাইনিন কোষ বিভাজন আর পুষ্টি চলাচল বাড়ায়; এবিএ আর ইথিলিন বার্ধক্য আর মোচন দ্রুত করে।"),
    _q("Which gaseous hormone causes the 'triple response' in seedlings and speeds fruit ripening?", ["Ethylene", "Auxin", "Cytokinin", "Abscisic acid"],
       "Triple response: shorter, thicker stems and horizontal growth; ethephon releases ethylene in farming.",
       "কোন গ্যাসীয় হরমোন চারায় 'ত্রয়ী সাড়া' ঘটায় আর ফল পাকা দ্রুত করে?", ["ইথিলিন", "অক্সিন", "সাইটোকাইনিন", "অ্যাবসিসিক অ্যাসিড"],
       "ত্রয়ী সাড়া: ছোট, মোটা কাণ্ড আর আনুভূমিক বৃদ্ধি; চাষে ইথেফন ইথিলিন ছাড়ে।"),
    _q("Auxin moves in a stem mainly…", ["Polarly, from the shoot tip downwards", "Equally in all directions", "Only upwards in xylem", "Only in phloem towards the leaves"],
       "Polar transport by carrier proteins sets up gradients behind phototropism and apical dominance.",
       "কাণ্ডে অক্সিন প্রধানত চলে…", ["মেরুমুখীভাবে, বিটপ-ডগা থেকে নিচের দিকে", "সব দিকে সমানভাবে", "কেবল জাইলেমে ওপরে", "কেবল ফ্লোয়েমে পাতার দিকে"],
       "বাহক প্রোটিনের মেরুমুখী পরিবহন আলোকবর্তন আর অগ্রস্থ প্রকটতার পেছনের ঢাল তৈরি করে।"),
    _q("Which hormone keeps seeds dormant and is antagonistic to gibberellins?", ["Abscisic acid", "Auxin", "Cytokinin", "Florigen"],
       "GA triggers α-amylase in cereal aleurone to mobilise starch; ABA blocks it.",
       "কোন হরমোন বীজকে সুপ্ত রাখে আর জিবেরেলিনের বিরোধী?", ["অ্যাবসিসিক অ্যাসিড", "অক্সিন", "সাইটোকাইনিন", "ফ্লোরিজেন"],
       "জিবেরেলিন দানাশস্যের অ্যালিউরোনে আলফা-অ্যামাইলেজ চালু করে শ্বেতসার কাজে লাগায়; এবিএ তা আটকায়।"),
    _q("Which mineral deficiency first shows yellowing (chlorosis) of older leaves?", ["Nitrogen", "Calcium", "Iron", "Boron"],
       "Mobile elements (N, P, K, Mg) move to young leaves, so old leaves suffer first; immobile ones (Ca, Fe) affect young leaves first.",
       "কোন খনিজের অভাবে প্রথমে পুরোনো পাতা হলুদ হয় (ক্লোরোসিস)?", ["নাইট্রোজেন", "ক্যালসিয়াম", "লোহা", "বোরন"],
       "চলমান মৌল (N, P, K, Mg) কচি পাতায় সরে যায়, তাই পুরোনো পাতা আগে ভোগে; অচল মৌল (Ca, Fe) আগে কচি পাতায় প্রভাব ফেলে।"),
    # ---------------------------------------------------------------- human physiology
    _q("The Bohr effect means that haemoglobin releases more oxygen where…", ["CO₂ and H⁺ are high, as in active tissues", "Oxygen is high, as in the lungs", "Temperature is low", "pH is high"],
       "Acid and CO₂ shift the dissociation curve right, unloading O₂ exactly where it is needed.",
       "বোর প্রভাব মানে হিমোগ্লোবিন বেশি অক্সিজেন ছাড়ে যেখানে…", ["CO₂ আর H⁺ বেশি, যেমন সক্রিয় কলায়", "অক্সিজেন বেশি, যেমন ফুসফুসে", "তাপমাত্রা কম", "pH বেশি"],
       "অম্ল আর CO₂ বিয়োজন-বক্ররেখাকে ডানে সরায়, ঠিক যেখানে দরকার সেখানে অক্সিজেন নামায়।"),
    _q("As bicarbonate leaves red blood cells into plasma, chloride ions move in. This is…", ["The chloride (Hamburger) shift", "The Bohr effect", "The Haldane effect", "Osmosis"],
       "It keeps the cell electrically neutral while CO₂ travels as HCO₃⁻ made by carbonic anhydrase.",
       "লোহিত কণিকা থেকে বাইকার্বনেট রক্তরসে বেরোলে ক্লোরাইড আয়ন ভেতরে ঢোকে। এটা…", ["ক্লোরাইড (হ্যামবার্গার) সরণ", "বোর প্রভাব", "হ্যালডেন প্রভাব", "অভিস্রবণ"],
       "কার্বনিক অ্যানহাইড্রেজের তৈরি HCO₃⁻ রূপে CO₂ চলার সময় এটা কোষকে বৈদ্যুতিকভাবে নিরপেক্ষ রাখে।"),
    _q("Lung surfactant, made by type II alveolar cells, is important because it…", ["Lowers surface tension and stops alveoli collapsing", "Kills bacteria", "Carries oxygen", "Makes mucus"],
       "Premature babies lacking it develop respiratory distress syndrome.",
       "দ্বিতীয় ধরনের বায়ুথলি-কোষের তৈরি ফুসফুসের সারফ্যাক্ট্যান্ট গুরুত্বপূর্ণ কারণ এটা…", ["পৃষ্ঠটান কমিয়ে বায়ুথলিকে চুপসে যেতে দেয় না", "ব্যাকটেরিয়া মারে", "অক্সিজেন বহন করে", "শ্লেষ্মা তৈরি করে"],
       "যে অপরিণত শিশুর এর অভাব, তাদের শ্বাসকষ্ট সিনড্রোম হয়।"),
    _q("The Frank-Starling law of the heart states that…", ["The more the ventricle is filled (stretched), the more forcefully it contracts", "Heart rate always stays constant", "The left and right sides pump different volumes", "Valves open by nerve signals"],
       "This matches output to venous return beat by beat, without nerves or hormones.",
       "হৃৎপিণ্ডের ফ্র্যাঙ্ক-স্টারলিং সূত্র বলে…", ["নিলয় যত বেশি ভরে (প্রসারিত হয়), তত জোরে সংকুচিত হয়", "হৃৎস্পন্দন সবসময় স্থির থাকে", "বাম আর ডান দিক আলাদা আয়তন পাম্প করে", "কপাটিকা স্নায়ু-সংকেতে খোলে"],
       "স্নায়ু বা হরমোন ছাড়াই প্রতি স্পন্দনে নির্গমনকে শিরা থেকে ফেরা রক্তের সঙ্গে মেলায়।"),
    _q("When blood pressure in the kidney falls, the juxtaglomerular cells release…", ["Renin, starting the renin-angiotensin-aldosterone system", "ADH", "Insulin", "Atrial natriuretic factor"],
       "Angiotensin II constricts vessels and aldosterone retains Na⁺ and water; ANF from the atria does the opposite.",
       "বৃক্কে রক্তচাপ কমলে জাক্সটাগ্লোমেরুলার কোষ ছাড়ে…", ["রেনিন, রেনিন-অ্যানজিওটেনসিন-অ্যালডোস্টেরন তন্ত্র শুরু করে", "এডিএইচ", "ইনসুলিন", "অ্যাট্রিয়াল ন্যাট্রিইউরেটিক ফ্যাক্টর"],
       "অ্যানজিওটেনসিন II নালি সংকুচিত করে আর অ্যালডোস্টেরন Na⁺ ও জল ধরে রাখে; অলিন্দের এএনএফ উল্টো কাজ করে।"),
    _q("The loop of Henle concentrates urine by…", ["A countercurrent multiplier that builds a salt gradient in the medulla", "Filtering blood", "Secreting glucose", "Producing hormones"],
       "The descending limb lets water out, the ascending limb pumps salt out but holds water; the vasa recta preserve the gradient.",
       "হেনলির লুপ মূত্রকে ঘন করে…", ["প্রতিস্রোত গুণক দিয়ে, যা মেডুলায় লবণের ঢাল গড়ে", "রক্ত পরিস্রুত করে", "গ্লুকোজ ক্ষরণ করে", "হরমোন তৈরি করে"],
       "অবরোহী বাহু জল ছাড়ে, আরোহী বাহু লবণ পাম্প করে কিন্তু জল ধরে রাখে; ভাসা রেক্টা ঢালটি রক্ষা করে।"),
    _q("Diabetes insipidus is caused by a lack of…", ["Antidiuretic hormone (ADH), leading to large volumes of dilute urine", "Insulin", "Glucagon", "Thyroxine"],
       "Unlike diabetes mellitus, the urine contains no sugar - 'insipid' means tasteless.",
       "ডায়াবেটিস ইনসিপিডাস হয় কীসের অভাবে?", ["অ্যান্টিডাইইউরেটিক হরমোন (এডিএইচ), ফলে প্রচুর লঘু মূত্র", "ইনসুলিন", "গ্লুকাগন", "থাইরক্সিন"],
       "ডায়াবেটিস মেলাইটাসের মতো নয়, মূত্রে শর্করা থাকে না - 'ইনসিপিড' মানে স্বাদহীন।"),
    _q("At a cholinergic synapse, the neurotransmitter is removed from the cleft by…", ["Acetylcholinesterase, which breaks acetylcholine down", "Reuptake into the muscle", "Diffusion into the blood only", "Binding to haemoglobin"],
       "Nerve gases and some insecticides block this enzyme, causing continuous stimulation.",
       "কোলিনার্জিক সাইন্যাপসে নিউরোট্রান্সমিটার ফাঁক থেকে সরায়…", ["অ্যাসিটাইলকোলিনেস্টারেজ, যা অ্যাসিটাইলকোলিন ভাঙে", "পেশিতে পুনঃগ্রহণ", "কেবল রক্তে ব্যাপন", "হিমোগ্লোবিনে বন্ধন"],
       "স্নায়ু-গ্যাস আর কিছু কীটনাশক এই উৎসেচক আটকায়, ফলে অবিরাম উদ্দীপনা হয়।"),
    _q("During the refractory period after an action potential, a nerve fibre…", ["Cannot fire another impulse (absolute) or needs a stronger stimulus (relative)", "Fires impulses continuously", "Reverses the direction of conduction", "Loses its myelin"],
       "Inactivated Na⁺ channels make impulses travel one way and limit their frequency.",
       "সক্রিয়-বিভবের পরের অবাধ্য সময়ে একটা স্নায়ুতন্তু…", ["আর একটা আবেগ ছুড়তে পারে না (পরম) বা জোরালো উদ্দীপনা লাগে (আপেক্ষিক)", "অবিরাম আবেগ ছোড়ে", "পরিবহনের দিক উল্টে দেয়", "মায়েলিন হারায়"],
       "নিষ্ক্রিয় Na⁺ চ্যানেল আবেগকে একমুখী করে আর তার কম্পাঙ্ক সীমিত রাখে।"),
    _q("The resting membrane potential of a neuron (about -70 mV) is maintained mainly by…", ["The Na⁺-K⁺ pump and the membrane's greater permeability to K⁺", "Calcium entering the cell", "Chloride pumps only", "ATP synthase"],
       "The pump moves 3 Na⁺ out for 2 K⁺ in; K⁺ leaking out leaves the inside negative.",
       "নিউরনের বিশ্রাম-বিভব (প্রায় -70 mV) প্রধানত বজায় রাখে…", ["Na⁺-K⁺ পাম্প আর পর্দার K⁺-এর প্রতি বেশি ভেদ্যতা", "কোষে ক্যালসিয়ামের প্রবেশ", "কেবল ক্লোরাইড পাম্প", "এটিপি সিন্থেজ"],
       "পাম্প 2টি K⁺ ভেতরে আনার বিনিময়ে 3টি Na⁺ বের করে; K⁺ বাইরে চুঁইয়ে ভেতরটা ঋণাত্মক রাখে।"),
    _q("Which structure in the inner ear contains the hair cells for hearing?", ["The organ of Corti in the cochlea", "The semicircular canals", "The utricle", "The Eustachian tube"],
       "The semicircular canals sense rotation and the utricle and saccule sense gravity and linear motion.",
       "অন্তঃকর্ণের কোন অংশে শোনার রোমকোষ থাকে?", ["কক্লিয়ার কর্টি-অঙ্গ", "অর্ধবৃত্তাকার নালি", "ইউট্রিকল", "ইউস্টেশিয়ান নালি"],
       "অর্ধবৃত্তাকার নালি ঘূর্ণন আর ইউট্রিকল-স্যাকিউল মাধ্যাকর্ষণ ও সরল গতি বোঝে।"),
    _q("Parathyroid hormone raises blood calcium by…", ["Releasing calcium from bone and increasing its reabsorption in the kidney", "Storing calcium in bone", "Reducing calcium absorption", "Breaking down glucose"],
       "Calcitonin from the thyroid lowers blood calcium; the two balance each other.",
       "প্যারাথাইরয়েড হরমোন রক্তে ক্যালসিয়াম বাড়ায়…", ["হাড় থেকে ক্যালসিয়াম ছেড়ে আর বৃক্কে তার পুনঃশোষণ বাড়িয়ে", "হাড়ে ক্যালসিয়াম জমিয়ে", "ক্যালসিয়াম শোষণ কমিয়ে", "গ্লুকোজ ভেঙে"],
       "থাইরয়েডের ক্যালসিটোনিন রক্তের ক্যালসিয়াম কমায়; দুটি পরস্পরের ভারসাম্য রাখে।"),
    _q("Addison's disease results from…", ["Too little cortisol and aldosterone from the adrenal cortex", "Too much thyroxine", "Too much growth hormone", "Too little insulin"],
       "Symptoms include weakness, low blood pressure and darkened skin; too much cortisol causes Cushing's syndrome.",
       "অ্যাডিসন রোগ হয়…", ["অ্যাড্রিনাল কর্টেক্স থেকে খুব কম কর্টিসল আর অ্যালডোস্টেরনে", "খুব বেশি থাইরক্সিনে", "খুব বেশি বৃদ্ধি-হরমোনে", "খুব কম ইনসুলিনে"],
       "লক্ষণ: দুর্বলতা, নিম্ন রক্তচাপ আর গাঢ় ত্বক; বেশি কর্টিসলে কুশিং সিনড্রোম হয়।"),
    _q("Excess growth hormone in an adult, after the growth plates have closed, causes…", ["Acromegaly - enlarged hands, feet and jaw", "Gigantism", "Dwarfism", "Cretinism"],
       "Before puberty the same excess causes gigantism; too little causes pituitary dwarfism.",
       "বৃদ্ধি-তল বন্ধ হওয়ার পরে প্রাপ্তবয়স্কে বাড়তি বৃদ্ধি-হরমোন ঘটায়…", ["অ্যাক্রোমেগালি - হাত, পা আর চোয়াল বড় হয়", "অতিকায়ত্ব", "বামনত্ব", "ক্রেটিনিজম"],
       "বয়ঃসন্ধির আগে একই আধিক্যে অতিকায়ত্ব; কম হলে পিটুইটারি বামনত্ব।"),
    _q("Insulin lowers blood glucose mainly by…", ["Moving GLUT4 transporters to muscle and fat cell membranes and promoting glycogen synthesis", "Breaking down glycogen", "Making glucose in the liver", "Increasing glucose loss in urine"],
       "Glucagon from α-cells has the opposite effects; type 1 diabetes lacks insulin, type 2 resists it.",
       "ইনসুলিন রক্তের গ্লুকোজ কমায় প্রধানত…", ["পেশি আর চর্বি-কোষের পর্দায় গ্লুট4 বাহক এনে আর গ্লাইকোজেন সংশ্লেষ বাড়িয়ে", "গ্লাইকোজেন ভেঙে", "যকৃতে গ্লুকোজ তৈরি করে", "মূত্রে গ্লুকোজ ক্ষয় বাড়িয়ে"],
       "আলফা-কোষের গ্লুকাগন উল্টো কাজ করে; টাইপ 1 ডায়াবেটিসে ইনসুলিন নেই, টাইপ 2-এ ইনসুলিনে সাড়া কম।"),
    _q("Which hormone is a classic example of positive feedback during childbirth?", ["Oxytocin", "Progesterone", "Thyroxine", "Cortisol"],
       "Contractions push the baby on the cervix, which releases more oxytocin, which strengthens contractions until birth.",
       "প্রসবের সময় ধনাত্মক প্রতিক্রিয়ার চিরাচরিত উদাহরণ কোন হরমোন?", ["অক্সিটোসিন", "প্রোজেস্টেরন", "থাইরক্সিন", "কর্টিসল"],
       "সংকোচন শিশুকে জরায়ুমুখে ঠেলে, যা আরও অক্সিটোসিন ছাড়ায়, যা জন্ম পর্যন্ত সংকোচন জোরালো করে।"),
    _q("Graves' disease, with bulging eyes and a fast heartbeat, is…", ["An autoimmune overactivity of the thyroid", "Iodine deficiency goitre", "A lack of growth hormone", "A pancreatic tumour"],
       "Antibodies mimic TSH and keep stimulating the thyroid (hyperthyroidism).",
       "চোখ ঠেলে বেরোনো আর দ্রুত হৃৎস্পন্দনযুক্ত গ্রেভস রোগ হল…", ["থাইরয়েডের অটোইমিউন অতিসক্রিয়তা", "আয়োডিন-ঘাটতির গলগণ্ড", "বৃদ্ধি-হরমোনের অভাব", "অগ্ন্যাশয়ের টিউমার"],
       "অ্যান্টিবডি টিএসএইচ-এর মতো আচরণ করে থাইরয়েডকে উদ্দীপিত করতে থাকে (হাইপারথাইরয়েডিজম)।"),
    # ---------------------------------------------------------------- reproduction and development
    _q("Which cells in the testes nourish developing sperm and secrete inhibin?", ["Sertoli cells", "Leydig cells", "Spermatogonia", "Oocytes"],
       "Leydig (interstitial) cells make testosterone; inhibin from Sertoli cells reduces FSH.",
       "শুক্রাশয়ের কোন কোষ বিকাশমান শুক্রাণুকে পুষ্টি দেয় আর ইনহিবিন ক্ষরণ করে?", ["সারটোলি কোষ", "লেডিগ কোষ", "স্পার্মাটোগোনিয়া", "উসাইট"],
       "লেডিগ (অন্তর্বর্তী) কোষ টেস্টোস্টেরন বানায়; সারটোলি কোষের ইনহিবিন এফএসএইচ কমায়।"),
    _q("Capacitation of sperm happens…", ["In the female reproductive tract, making sperm able to fertilise", "In the testes", "In the epididymis only", "After fertilisation"],
       "It changes the sperm membrane so the acrosome reaction can release enzymes that cross the zona pellucida.",
       "শুক্রাণুর সক্ষমায়ন ঘটে…", ["স্ত্রী জননপথে, শুক্রাণুকে নিষেকে সক্ষম করে", "শুক্রাশয়ে", "কেবল এপিডিডাইমিসে", "নিষেকের পরে"],
       "এটা শুক্রাণুর পর্দা বদলায়, যাতে অ্যাক্রোজোম বিক্রিয়ায় উৎসেচক বেরিয়ে জোনা পেলুসিডা পেরোতে পারে।"),
    _q("At what stage does the human embryo implant in the uterine wall?", ["Blastocyst", "Morula", "Zygote", "Gastrula"],
       "About 7 days after fertilisation; the trophoblast attaches and the inner cell mass becomes the embryo.",
       "মানব ভ্রূণ কোন দশায় জরায়ু-প্রাচীরে প্রোথিত হয়?", ["ব্লাস্টোসিস্ট", "মরুলা", "জাইগোট", "গ্যাস্ট্রুলা"],
       "নিষেকের প্রায় 7 দিন পরে; ট্রফোব্লাস্ট লেগে যায় আর অন্তঃকোষপুঞ্জ ভ্রূণ হয়।"),
    _q("The first milk after childbirth, colostrum, is especially valuable because it is rich in…", ["IgA antibodies that protect the newborn", "Sugar only", "Iron only", "Vitamin C only"],
       "This is natural passive immunity given by the mother.",
       "প্রসবের পরের প্রথম দুধ, কোলোস্ট্রাম, বিশেষ মূল্যবান কারণ এতে প্রচুর…", ["আইজিএ অ্যান্টিবডি, যা নবজাতককে রক্ষা করে", "কেবল শর্করা", "কেবল লোহা", "কেবল ভিটামিন সি"],
       "এটা মায়ের দেওয়া প্রাকৃতিক নিষ্ক্রিয় অনাক্রম্যতা।"),
    _q("Amniocentesis is used to…", ["Check foetal cells in the amniotic fluid for chromosomal disorders", "Increase fertility", "Stop labour", "Measure blood sugar"],
       "Its misuse for sex determination is banned in India.",
       "অ্যামনিওসেন্টেসিস ব্যবহার করা হয়…", ["অ্যামনিয়ন তরলের ভ্রূণকোষে ক্রোমোজোম-ত্রুটি পরীক্ষা করতে", "উর্বরতা বাড়াতে", "প্রসব থামাতে", "রক্তের শর্করা মাপতে"],
       "লিঙ্গ নির্ধারণে এর অপব্যবহার ভারতে নিষিদ্ধ।"),
    _q("In flowering plants, apomixis means…", ["Forming seeds without fertilisation", "Self-pollination", "Cross-pollination by insects", "Vegetative propagation by cuttings"],
       "The seed is a clone of the mother; it could keep hybrid vigour in crops year after year.",
       "সপুষ্পক উদ্ভিদে অ্যাপোমিক্সিস মানে…", ["নিষেক ছাড়াই বীজ তৈরি", "স্বপরাগযোগ", "পোকার মাধ্যমে ইতর-পরাগযোগ", "কাটিং দিয়ে অঙ্গজ জনন"],
       "বীজটি মায়ের ক্লোন; ফসলে বছরের পর বছর সংকর-ওজ ধরে রাখতে পারত।"),
    _q("Which part of a mature embryo sac has three cells at the micropylar end?", ["The egg apparatus (egg cell + two synergids)", "The antipodals", "The central cell", "The nucellus"],
       "The 7-celled, 8-nucleate embryo sac: egg apparatus, 3 antipodals and a central cell with 2 polar nuclei.",
       "পরিণত ভ্রূণস্থলীর ডিম্বকরন্ধ্র প্রান্তে কোন অংশে তিনটি কোষ?", ["ডিম্বাণু-যন্ত্র (ডিম্বাণু + দুটি সহকারী কোষ)", "প্রতিপাদ কোষ", "কেন্দ্রীয় কোষ", "ন্যুসেলাস"],
       "7 কোষ, 8 নিউক্লিয়াসের ভ্রূণস্থলী: ডিম্বাণু-যন্ত্র, 3টি প্রতিপাদ কোষ আর 2টি মেরু-নিউক্লিয়াসযুক্ত কেন্দ্রীয় কোষ।"),
    _q("Which hormone level stays high during pregnancy to keep the uterine lining and stop new ovulation?", ["Progesterone", "LH", "FSH", "Oxytocin"],
       "First from the corpus luteum (kept alive by hCG), later from the placenta.",
       "গর্ভাবস্থায় জরায়ুর আস্তরণ ধরে রাখতে আর নতুন ডিম্বস্ফোটন থামাতে কোন হরমোনের মাত্রা উঁচু থাকে?", ["প্রোজেস্টেরন", "এলএইচ", "এফএসএইচ", "অক্সিটোসিন"],
       "প্রথমে পীতগ্রন্থি থেকে (এইচসিজি তাকে বাঁচিয়ে রাখে), পরে অমরা থেকে।"),
    # ---------------------------------------------------------------- immunology
    _q("Which cells are destroyed by HIV, crippling both antibody and cell-mediated immunity?", ["Helper T cells (CD4⁺)", "B cells only", "Red blood cells", "Platelets"],
       "Helper T cells activate B cells and cytotoxic T cells; their loss leads to AIDS and opportunistic infections.",
       "এইচআইভি কোন কোষ ধ্বংস করে অ্যান্টিবডি আর কোষ-মধ্যস্থ দুই অনাক্রম্যতাই পঙ্গু করে?", ["সাহায্যকারী টি কোষ (সিডি4⁺)", "কেবল বি কোষ", "লোহিত রক্তকণিকা", "অণুচক্রিকা"],
       "সাহায্যকারী টি কোষ বি কোষ আর সাইটোটক্সিক টি কোষকে সক্রিয় করে; তাদের ক্ষয়ে এইডস আর সুযোগসন্ধানী সংক্রমণ হয়।"),
    _q("Monoclonal antibodies are produced by…", ["Hybridoma cells - B cells fused with myeloma (cancer) cells", "Red blood cells", "Plants", "Bacteria alone"],
       "The hybrid makes one specific antibody and divides endlessly; used in diagnosis and cancer therapy.",
       "মনোক্লোনাল অ্যান্টিবডি তৈরি হয়…", ["হাইব্রিডোমা কোষে - মায়েলোমা (ক্যানসার) কোষের সঙ্গে মিলিত বি কোষে", "লোহিত রক্তকণিকায়", "উদ্ভিদে", "কেবল ব্যাকটেরিয়ায়"],
       "সংকরটি একটা নির্দিষ্ট অ্যান্টিবডি বানায় আর অবিরাম বিভাজিত হয়; রোগনির্ণয় আর ক্যানসার চিকিৎসায় ব্যবহৃত।"),
    _q("Why is the secondary immune response faster and stronger than the primary?", ["Memory B and T cells formed during the first exposure respond quickly", "The antigen becomes weaker", "Antibodies are made by red cells", "Vaccines contain antibodies"],
       "This is why booster doses work: the IgG response rises sooner and higher.",
       "গৌণ অনাক্রম্য সাড়া মুখ্য সাড়ার চেয়ে দ্রুত আর জোরালো কেন?", ["প্রথম সংস্পর্শে তৈরি স্মৃতি বি আর টি কোষ দ্রুত সাড়া দেয়", "অ্যান্টিজেন দুর্বল হয়ে যায়", "লোহিত কণিকা অ্যান্টিবডি বানায়", "টিকায় অ্যান্টিবডি থাকে"],
       "তাই বুস্টার ডোজ কাজ করে: আইজিজি সাড়া আগে আর উঁচুতে ওঠে।"),
    _q("In an allergic reaction, which antibody triggers mast cells to release histamine?", ["IgE", "IgG", "IgM", "IgA"],
       "Antihistamines and steroids reduce the symptoms; adrenaline treats severe anaphylaxis.",
       "অ্যালার্জি প্রতিক্রিয়ায় কোন অ্যান্টিবডি মাস্ট কোষকে হিস্টামিন ছাড়তে প্ররোচিত করে?", ["আইজিই", "আইজিজি", "আইজিএম", "আইজিএ"],
       "অ্যান্টিহিস্টামিন আর স্টেরয়েড লক্ষণ কমায়; গুরুতর অ্যানাফাইল্যাক্সিসে অ্যাড্রিনালিন দেওয়া হয়।"),
    _q("Rheumatoid arthritis is an example of…", ["An autoimmune disease, where the body attacks its own tissues", "An allergy", "A bacterial infection", "A nutritional deficiency"],
       "Failure to tell self from non-self; type 1 diabetes and multiple sclerosis are other examples.",
       "রিউমাটয়েড আর্থ্রাইটিস কীসের উদাহরণ?", ["অটোইমিউন রোগের, যেখানে দেহ নিজের কলাকে আক্রমণ করে", "অ্যালার্জির", "ব্যাকটেরিয়া সংক্রমণের", "পুষ্টির অভাবের"],
       "নিজ আর পরকে চিনতে ব্যর্থতা; টাইপ 1 ডায়াবেটিস আর মাল্টিপল স্ক্লেরোসিস অন্য উদাহরণ।"),
    _q("Interferons are proteins released by virus-infected cells that…", ["Protect neighbouring cells from viral infection", "Kill bacteria directly", "Carry oxygen", "Clot blood"],
       "They are part of innate (non-specific) immunity and are used as drugs against some viral diseases and cancers.",
       "ইন্টারফেরন হল ভাইরাস-আক্রান্ত কোষের ছাড়া প্রোটিন, যা…", ["পাশের কোষকে ভাইরাস সংক্রমণ থেকে রক্ষা করে", "সরাসরি ব্যাকটেরিয়া মারে", "অক্সিজেন বহন করে", "রক্ত জমাট বাঁধায়"],
       "এরা সহজাত (অনির্দিষ্ট) অনাক্রম্যতার অংশ, কিছু ভাইরাস রোগ আর ক্যানসারে ওষুধ হিসেবে ব্যবহৃত।"),
    _q("Graft rejection after an organ transplant is mainly due to…", ["Differences in MHC (HLA) proteins recognised by T cells", "Blood sugar levels", "The size of the organ", "Antibiotics"],
       "Tissue matching and immunosuppressants such as cyclosporin A reduce rejection.",
       "অঙ্গ প্রতিস্থাপনের পরে গ্রাফট প্রত্যাখ্যান মূলত হয়…", ["টি কোষের চেনা এমএইচসি (এইচএলএ) প্রোটিনের পার্থক্যের কারণে", "রক্তের শর্করার মাত্রায়", "অঙ্গের আকারে", "অ্যান্টিবায়োটিকে"],
       "কলা মেলানো আর সাইক্লোস্পোরিন এ-র মতো অনাক্রম্যতা-দমনকারী প্রত্যাখ্যান কমায়।"),
    # ---------------------------------------------------------------- ecology and environment
    _q("Species with many offspring, little parental care and rapid growth are…", ["r-selected", "K-selected", "Keystone species", "Endemic species"],
       "They thrive in unstable habitats (insects, weeds); K-selected species (elephants, whales) have few young and long care.",
       "যে প্রজাতির অনেক সন্তান, অল্প যত্ন আর দ্রুত বৃদ্ধি, তারা…", ["আর-নির্বাচিত", "কে-নির্বাচিত", "মূল প্রজাতি (কি-স্টোন)", "স্থানিক প্রজাতি"],
       "অস্থির আবাসে এরা বাড়ে (পোকা, আগাছা); কে-নির্বাচিত প্রজাতির (হাতি, তিমি) সন্তান কম আর দীর্ঘ যত্ন।"),
    _q("Allen's rule states that animals of colder climates tend to have…", ["Shorter ears and limbs, to reduce heat loss", "Longer ears and tails", "Thinner fur", "Larger surface area for their size"],
       "Bergmann's rule adds that they also tend to have larger bodies (lower surface area to volume ratio).",
       "অ্যালেনের নিয়ম বলে শীতল জলবায়ুর প্রাণীর থাকে…", ["তাপক্ষয় কমাতে ছোট কান আর অঙ্গ", "লম্বা কান আর লেজ", "পাতলা লোম", "আকারের তুলনায় বেশি পৃষ্ঠতল"],
       "বার্গম্যানের নিয়ম যোগ করে, তাদের দেহও বড় হয় (পৃষ্ঠতল-আয়তন অনুপাত কম)।"),
    _q("In the species-area relationship log S = log C + Z log A, the slope Z for whole continents is about…", ["0.6 to 1.2", "0.1 to 0.2", "Exactly 0", "Exactly 5"],
       "Small regions within a continent give Z ≈ 0.1-0.2; very large areas give steeper slopes, as Humboldt observed.",
       "প্রজাতি-ক্ষেত্রফল সম্পর্ক log S = log C + Z log A-তে গোটা মহাদেশের জন্য নতি Z প্রায়…", ["0.6 থেকে 1.2", "0.1 থেকে 0.2", "ঠিক 0", "ঠিক 5"],
       "মহাদেশের মধ্যে ছোট অঞ্চলে Z ≈ 0.1-0.2; খুব বড় এলাকায় নতি বেশি, যা হামবোল্ট লক্ষ করেন।"),
    _q("A species whose removal changes the whole community far more than its numbers suggest is a…", ["Keystone species", "Pioneer species", "Exotic species", "Dominant producer"],
       "For example sea otters keep sea urchins in check and so protect kelp forests.",
       "যে প্রজাতি সরালে তার সংখ্যার তুলনায় অনেক বেশি পুরো সম্প্রদায় বদলে যায়, তা হল…", ["মূল প্রজাতি (কি-স্টোন)", "পথিকৃৎ প্রজাতি", "বহিরাগত প্রজাতি", "প্রধান উৎপাদক"],
       "যেমন সামুদ্রিক ভোঁদড় সমুদ্র-সজারু নিয়ন্ত্রণে রেখে কেল্প বন রক্ষা করে।"),
    _q("A high BOD (biochemical oxygen demand) in river water indicates…", ["Heavy pollution by organic matter, such as sewage", "Very clean water", "High salt content", "Low temperature"],
       "Microbes use up dissolved oxygen as they decompose organic waste, and fish suffocate.",
       "নদীর জলে বেশি বিওডি (জৈব-রাসায়নিক অক্সিজেন চাহিদা) ইঙ্গিত করে…", ["নর্দমার মতো জৈব পদার্থে ভারী দূষণ", "খুব পরিষ্কার জল", "বেশি লবণ", "নিম্ন তাপমাত্রা"],
       "জীবাণু জৈব বর্জ্য পচানোর সময় দ্রবীভূত অক্সিজেন খরচ করে, মাছ দম বন্ধ হয়ে মরে।"),
    _q("The Montreal Protocol (1987) aimed to…", ["Phase out ozone-depleting substances such as CFCs", "Cut greenhouse gases from vehicles", "Protect wetlands", "Ban plastic bags"],
       "CFCs release chlorine in the stratosphere, which destroys ozone catalytically; wetlands are covered by the Ramsar Convention.",
       "মন্ট্রিল প্রোটোকলের (1987) লক্ষ্য ছিল…", ["সিএফসি-র মতো ওজোন-ক্ষয়কারী পদার্থ ধীরে ধীরে বন্ধ করা", "যানবাহনের গ্রিনহাউস গ্যাস কমানো", "জলাভূমি রক্ষা", "প্লাস্টিক ব্যাগ নিষেধ"],
       "সিএফসি স্ট্র্যাটোস্ফিয়ারে ক্লোরিন ছাড়ে, যা অনুঘটকভাবে ওজোন ধ্বংস করে; জলাভূমি রামসার চুক্তির আওতায়।"),
    _q("An age pyramid with a broad base and narrow top shows a population that is…", ["Growing rapidly", "Stable", "Declining", "Made only of old people"],
       "Many pre-reproductive individuals will soon reproduce; a bell shape is stable and an urn shape declining.",
       "চওড়া ভিত্তি আর সরু মাথার বয়স-পিরামিড দেখায় জনগোষ্ঠী…", ["দ্রুত বাড়ছে", "স্থিতিশীল", "কমছে", "কেবল বৃদ্ধদের নিয়ে"],
       "অনেক প্রাক-প্রজননক্ষম সদস্য শিগগির প্রজনন করবে; ঘণ্টাকৃতি স্থিতিশীল আর কলসি-আকৃতি ক্ষয়িষ্ণু।"),
    _q("The Chipko movement of the 1970s in the Himalaya is known for…", ["Villagers, especially women, hugging trees to stop them being felled", "Cleaning the Ganga", "Protecting tigers", "Building dams"],
       "It inspired later community forest protection; the Bishnoi community's sacrifice of 1731 is an older example.",
       "1970-এর দশকে হিমালয়ের চিপকো আন্দোলন বিখ্যাত…", ["গ্রামবাসী, বিশেষত নারীদের গাছ জড়িয়ে ধরে কাটা আটকানোর জন্য", "গঙ্গা পরিষ্কারের জন্য", "বাঘ রক্ষার জন্য", "বাঁধ তৈরির জন্য"],
       "এটা পরে সম্প্রদায়ভিত্তিক বন রক্ষাকে অনুপ্রাণিত করে; 1731-এ বিশনোই সম্প্রদায়ের আত্মত্যাগ আরও পুরোনো উদাহরণ।"),
    _q("Paul Ehrlich's 'rivet popper' hypothesis compares species in an ecosystem to…", ["Rivets in an aeroplane - losing a few may seem harmless, but losing key ones causes collapse", "Bricks in a wall that can all be removed", "Coins in a bank", "Leaves on a tree"],
       "It argues for conserving biodiversity because we cannot know which loss will be critical.",
       "পল এরলিকের 'রিভেট খোলা' প্রকল্প বাস্তুতন্ত্রের প্রজাতিকে তুলনা করে…", ["বিমানের রিভেটের সঙ্গে - কয়েকটি খুললে ক্ষতিহীন মনে হয়, কিন্তু গুরুত্বপূর্ণগুলো খুললে ভেঙে পড়ে", "দেয়ালের ইটের সঙ্গে, যার সবই খোলা যায়", "ব্যাংকের মুদ্রার সঙ্গে", "গাছের পাতার সঙ্গে"],
       "কোন ক্ষতি মারাত্মক হবে জানা যায় না, তাই জীববৈচিত্র্য সংরক্ষণের পক্ষে যুক্তি।"),
    _q("In a lake, the zone where light is enough for photosynthesis is the…", ["Photic (euphotic) zone", "Profundal zone", "Benthic zone", "Aphotic zone"],
       "Below the compensation point, respiration exceeds photosynthesis and only consumers and decomposers live.",
       "হ্রদে যে অঞ্চলে সালোকসংশ্লেষের মতো যথেষ্ট আলো থাকে, তা হল…", ["আলোকিত (ইউফোটিক) অঞ্চল", "গভীর (প্রোফান্ডাল) অঞ্চল", "তলদেশীয় অঞ্চল", "আলোহীন অঞ্চল"],
       "ক্ষতিপূরণ-বিন্দুর নিচে শ্বসন সালোকসংশ্লেষকে ছাড়িয়ে যায়, কেবল খাদক আর বিয়োজক বাঁচে।"),
    # ---------------------------------------------------------------- microbes
    _q("Which microbe produces the clot-buster streptokinase, used after heart attacks?", ["Streptococcus", "Trichoderma polysporum", "Monascus purpureus", "Lactobacillus"],
       "Trichoderma gives cyclosporin A (an immunosuppressant) and Monascus gives statins (cholesterol-lowering).",
       "হার্ট অ্যাটাকের পরে ব্যবহৃত জমাট-ভাঙানো স্ট্রেপটোকাইনেজ কোন জীবাণু তৈরি করে?", ["স্ট্রেপটোকক্কাস", "ট্রাইকোডার্মা পলিস্পোরাম", "মোনাস্কাস পারপিউরিয়াস", "ল্যাকটোব্যাসিলাস"],
       "ট্রাইকোডার্মা দেয় সাইক্লোস্পোরিন এ (অনাক্রম্যতা-দমনকারী) আর মোনাস্কাস দেয় স্ট্যাটিন (কোলেস্টেরল কমায়)।"),
    _q("The large holes in Swiss cheese are made by…", ["Carbon dioxide from Propionibacterium shermanii", "Air bubbles beaten in", "Yeast making alcohol", "Lactobacillus making acid"],
       "The bacterium ferments lactate and releases CO₂ during ripening.",
       "সুইস চিজের বড় গর্তগুলো তৈরি করে…", ["প্রোপিওনিব্যাকটেরিয়াম শারমানির কার্বন ডাইঅক্সাইড", "ফেটিয়ে ঢোকানো বাতাসের বুদ্বুদ", "অ্যালকোহল বানানো ইস্ট", "অম্ল বানানো ল্যাকটোব্যাসিলাস"],
       "পাকার সময় ব্যাকটেরিয়াটি ল্যাকটেট গাঁজিয়ে CO₂ ছাড়ে।"),
    _q("Methanogens such as Methanobacterium, found in cattle rumen and sewage, are…", ["Archaea that produce methane from CO₂ and H₂ in the absence of oxygen", "Fungi that digest wood", "Algae that fix nitrogen", "Viruses of cattle"],
       "Their work makes biogas; cattle dung contains them, which is why gobar gas plants work.",
       "গবাদিপশুর পাকস্থলী আর নর্দমায় থাকা মিথানোব্যাকটেরিয়ামের মতো মিথানোজেন হল…", ["অক্সিজেনহীন অবস্থায় CO₂ আর H₂ থেকে মিথেন তৈরি করা আর্কিয়া", "কাঠ হজম করা ছত্রাক", "নাইট্রোজেন বাঁধা শৈবাল", "গবাদিপশুর ভাইরাস"],
       "এদের কাজে বায়োগ্যাস হয়; গোবরে এরা থাকে, তাই গোবর-গ্যাস কেন্দ্র চলে।"),
    _q("Trichoderma is used in organic farming as…", ["A biocontrol agent against fungal plant diseases", "A nitrogen fixer", "An insecticide against caterpillars", "A source of insulin"],
       "It grows in the root zone and attacks pathogenic fungi; Baculoviruses are used against insects.",
       "জৈব চাষে ট্রাইকোডার্মা ব্যবহৃত হয়…", ["ছত্রাকঘটিত উদ্ভিদ-রোগের বিরুদ্ধে জৈব নিয়ন্ত্রক হিসেবে", "নাইট্রোজেন-বন্ধক হিসেবে", "শুঁয়োপোকার বিরুদ্ধে কীটনাশক হিসেবে", "ইনসুলিনের উৎস হিসেবে"],
       "এটা মূল-অঞ্চলে বাড়ে আর রোগজীবাণু ছত্রাককে আক্রমণ করে; পোকার বিরুদ্ধে ব্যাকুলোভাইরাস ব্যবহৃত হয়।"),
    _q("Mycorrhizal fungi such as Glomus help plants mainly by…", ["Absorbing phosphorus from the soil and passing it to the roots", "Fixing nitrogen gas", "Making plants taller with hormones", "Killing insects"],
       "In return they get sugars from the plant - a mutualism; they also improve drought and pathogen resistance.",
       "গ্লোমাসের মতো মাইকোরাইজা ছত্রাক উদ্ভিদকে প্রধানত সাহায্য করে…", ["মাটি থেকে ফসফরাস শোষণ করে মূলে দিয়ে", "নাইট্রোজেন গ্যাস বেঁধে", "হরমোন দিয়ে গাছ লম্বা করে", "পোকা মেরে"],
       "বিনিময়ে তারা উদ্ভিদ থেকে শর্করা পায় - পারস্পরিক উপকার; খরা আর রোগ সহনশীলতাও বাড়ায়।"),
    _q("In sewage treatment, the flocs in the secondary (biological) stage are…", ["Masses of bacteria and fungal filaments that digest organic matter", "Grains of sand", "Chemical coagulants only", "Plastic beads"],
       "Aeration lets them reduce BOD; part of the sludge returns as inoculum and the rest goes to anaerobic digesters.",
       "নর্দমা শোধনে গৌণ (জৈব) পর্যায়ের ফ্লক হল…", ["জৈব পদার্থ পরিপাককারী ব্যাকটেরিয়া আর ছত্রাক-সুতোর পিণ্ড", "বালির দানা", "কেবল রাসায়নিক জমাটকারী", "প্লাস্টিকের পুঁতি"],
       "বায়ু-চালনায় এরা বিওডি কমায়; কাদার কিছু অংশ বীজ হিসেবে ফেরে, বাকিটা অবাত পাচকে যায়।"),
    _q("Which part of the nephron is almost impermeable to water?", ["The ascending limb of the loop of Henle", "The descending limb of the loop of Henle", "The proximal convoluted tubule", "The collecting duct with ADH present"],
       "It pumps salt out but keeps water in, so the filtrate becomes dilute as it climbs - the heart of the countercurrent system.",
       "নেফ্রনের কোন অংশ জলের প্রতি প্রায় অভেদ্য?", ["হেনলির লুপের আরোহী বাহু", "হেনলির লুপের অবরোহী বাহু", "নিকটবর্তী সংবর্ত নালিকা", "এডিএইচ থাকা অবস্থায় সংগ্রাহী নালি"],
       "এটা লবণ বের করে কিন্তু জল ধরে রাখে, তাই ওঠার পথে পরিস্রুত লঘু হয় - প্রতিস্রোত তন্ত্রের মূল।"),
    _q("Which organ secretes erythropoietin, the hormone that boosts red blood cell production?", ["The kidney", "The liver", "The spleen", "The thyroid"],
       "Low oxygen in the kidney triggers its release - why people living at high altitude make more red cells.",
       "লোহিত রক্তকণিকা তৈরি বাড়ানো হরমোন এরিথ্রোপোয়েটিন কোন অঙ্গ ক্ষরণ করে?", ["বৃক্ক", "যকৃৎ", "প্লীহা", "থাইরয়েড"],
       "বৃক্কে অক্সিজেন কমলে এটা ছাড়া হয় - তাই উঁচু পাহাড়ে থাকা মানুষের লোহিত কণিকা বেশি।"),
    _q("Which metal ion sits at the centre of the chlorophyll molecule?", ["Magnesium", "Iron", "Copper", "Zinc"],
       "Chlorophyll's porphyrin ring holds Mg²⁺; the similar haem ring of haemoglobin holds Fe²⁺.",
       "ক্লোরোফিল অণুর কেন্দ্রে কোন ধাতব আয়ন থাকে?", ["ম্যাগনেসিয়াম", "লোহা", "তামা", "দস্তা"],
       "ক্লোরোফিলের পরফাইরিন বলয়ে Mg²⁺ থাকে; হিমোগ্লোবিনের একই রকম হিম বলয়ে Fe²⁺।"),
    _q("Plant tissue culture is possible because plant cells show…", ["Totipotency - a single cell can regenerate a whole plant", "Apical dominance", "Photoperiodism", "Senescence"],
       "With the right auxin-cytokinin balance, callus forms shoots or roots; meristem culture gives virus-free plants.",
       "উদ্ভিদ কলা-কর্ষণ সম্ভব কারণ উদ্ভিদকোষ দেখায়…", ["পূর্ণক্ষমতা - একটা কোষ থেকে গোটা উদ্ভিদ জন্মাতে পারে", "অগ্রস্থ প্রকটতা", "দীপ্তিকালবাদ", "বার্ধক্য"],
       "সঠিক অক্সিন-সাইটোকাইনিন অনুপাতে ক্যালাস থেকে বিটপ বা মূল হয়; ভাজক-কলা কর্ষণে ভাইরাসমুক্ত উদ্ভিদ পাওয়া যায়।"),
    _q("Lactobacillus turning milk into curd also improves its nutritional value by…", ["Increasing vitamin B₁₂", "Adding iron", "Removing all protein", "Adding vitamin C"],
       "The acid it makes coagulates milk proteins; in the stomach it also checks disease-causing microbes.",
       "ল্যাকটোব্যাসিলাস দুধকে দই করার সময় পুষ্টিমানও বাড়ায়…", ["ভিটামিন বি₁₂ বাড়িয়ে", "লোহা যোগ করে", "সব প্রোটিন সরিয়ে", "ভিটামিন সি যোগ করে"],
       "এর তৈরি অম্ল দুধের প্রোটিন জমাট বাঁধায়; পাকস্থলীতে রোগজীবাণুও নিয়ন্ত্রণে রাখে।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
