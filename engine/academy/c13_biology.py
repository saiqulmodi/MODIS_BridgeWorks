"""NIT level - Biology (entrance-exam standard, NEET-style): cell biology and biomolecules, genetics
and molecular biology, evolution, plant physiology, human physiology, reproduction, health and
disease, microbes, biotechnology, ecology and the environment. Numerical items cover genetic ratios,
population genetics, ecology and physiology calculations."""
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
    r = _c(r)
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [_f(x) + u_en for x in o], 0, ex_en, q_bn, [_f(x) + ub for x in o], ex_bn)


def _fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def _fr(q_en, q_bn, r, alts, ex_en, ex_bn):
    out = []
    for x in (r, *alts, r * 2, r / 2, 1 - r, F(1, 16)):
        x = F(x)
        if 0 < x <= 1 and x not in out:
            out.append(x)
    opts = [_fs(x) for x in out[:4]]
    return mcq(q_en, opts, 0, ex_en, q_bn, opts, ex_bn)


# ---------------------------------------------------------------- genetics
DIHYBRID = {
    "both dominant traits": ("দুটো প্রকট বৈশিষ্ট্যই", F(9, 16)),
    "the first dominant and the second recessive trait": ("প্রথমটা প্রকট আর দ্বিতীয়টা প্রচ্ছন্ন বৈশিষ্ট্য", F(3, 16)),
    "both recessive traits": ("দুটো প্রচ্ছন্ন বৈশিষ্ট্যই", F(1, 16)),
}


def dihybrid(which):
    bn, r = DIHYBRID[which]
    return _fr(f"Two plants heterozygous for two unlinked genes (AaBb x AaBb) are crossed. What fraction of the offspring show {which}?",
               f"দুটো অসংযুক্ত জিনের জন্য বিষমযুগ্মী দুটো উদ্ভিদের (AaBb x AaBb) সংকরায়ণ হল। অপত্যের কত অংশ {bn} দেখায়?", r,
               (F(3, 4), F(1, 4), F(9, 16) if r != F(9, 16) else F(1, 16)),
               f"Each gene gives 3/4 dominant and 1/4 recessive; multiply: {_fs(r)} (the 9:3:3:1 ratio).",
               f"প্রতিটি জিনে 3/4 প্রকট আর 1/4 প্রচ্ছন্ন; গুণ করলে {_fs(r)} (9:3:3:1 অনুপাত)।")


def mono(cross, bn_cross, want_en, want_bn, r, how_en, how_bn):
    return _fr(f"In the cross {cross}, what fraction of the offspring are {want_en}?",
               f"{bn_cross} সংকরায়ণে অপত্যের কত অংশ {want_bn}?", r, (F(1, 4), F(3, 4), F(1, 2)), how_en, how_bn)


def genotypes(n):
    r = n * (n + 1) // 2
    return _n(f"A gene has {n} alleles in a population. How many different genotypes are possible in a diploid organism?",
              f"একটা জনগোষ্ঠীতে একটা জিনের {n}টি অ্যালিল আছে। দ্বিপ্লয়েড জীবে কয়টি ভিন্ন জিনোটাইপ সম্ভব?", r,
              f"n(n + 1) ÷ 2 = {n} x {n + 1} ÷ 2 = {r}: {n} homozygous and {r - n} heterozygous. The ABO system (3 alleles) gives 6.",
              f"n(n + 1) ÷ 2 = {n} x {n + 1} ÷ 2 = {r}: {n}টি সমযুগ্মী আর {r - n}টি বিষমযুগ্মী। ABO ব্যবস্থায় (3 অ্যালিল) 6টি।",
              (n * n, 2 ** n, n * 2))


def gametes(n):
    r = 2 ** n
    return _n(f"How many genetically different gametes can an individual heterozygous at {n} independent gene loci produce?",
              f"{n}টি স্বাধীন জিন-লোকাসে বিষমযুগ্মী একটা জীব কয় রকম জিনগতভাবে ভিন্ন গ্যামেট তৈরি করতে পারে?", r,
              f"Each locus contributes 2 choices: 2^{n} = {r}.",
              f"প্রতিটি লোকাস 2টি করে বিকল্প দেয়: 2^{n} = {r}টি।",
              (n * 2, 3 ** n, n * n))


def hardy(q2_pct):
    q = (q2_pct / 100) ** 0.5
    het = 2 * q * (1 - q) * 100
    return _n(f"In a population in Hardy-Weinberg equilibrium, {q2_pct:g}% of people show a recessive trait. What percentage are carriers (heterozygous)?",
              f"হার্ডি-ওয়াইনবার্গ সাম্যে থাকা একটা জনগোষ্ঠীর {q2_pct:g}% মানুষ একটা প্রচ্ছন্ন বৈশিষ্ট্য দেখায়। কত শতাংশ বাহক (বিষমযুগ্মী)?", het,
              f"q² = {q2_pct / 100:g}, so q = {_f(_c(q))} and p = {_f(_c(1 - q))}; 2pq = {_f(_c(het))}%.",
              f"q² = {q2_pct / 100:g}, তাই q = {_f(_c(q))} আর p = {_f(_c(1 - q))}; 2pq = {_f(_c(het))}%।",
              (q2_pct * 2, q * 100, (1 - q) ** 2 * 100), "%")


def chargaff(a):
    g = (100 - 2 * a) / 2
    return _n(f"A double-stranded DNA sample contains {a}% adenine. What percentage of its bases are guanine?",
              f"একটা দ্বিতন্ত্রী ডিএনএ নমুনায় {a}% অ্যাডেনিন আছে। এর কত শতাংশ ক্ষারক গুয়ানিন?", g,
              f"A = T = {a}%, so G + C = {100 - 2 * a}% and G = C = {_f(_c(g))}% (Chargaff's rule).",
              f"A = T = {a}%, তাই G + C = {100 - 2 * a}% আর G = C = {_f(_c(g))}% (শারগাফের নিয়ম)।",
              (a, 100 - a, 50 - a / 2), "%")


def dna_length(bp_txt, bp):
    m = bp * 0.34e-9
    if m < 0.1:                        # bacterial genomes: answer in millimetres
        mm = m * 1000
        return _n(f"The distance between adjacent base pairs in B-DNA is 0.34 nm. How long is a DNA molecule of {bp_txt} base pairs?",
                  f"বি-ডিএনএ-তে পাশাপাশি দুটো ক্ষারকজোড়ের দূরত্ব 0.34 nm। {bp_txt} ক্ষারকজোড়ের একটা ডিএনএ অণু কত লম্বা?", mm,
                  f"{bp_txt} x 0.34 x 10⁻⁹ m = {_f(_c(mm))} mm - about 1,000 times the length of the cell that packs it.",
                  f"দৈর্ঘ্য = {bp_txt} x 0.34 x 10⁻⁹ m = {_f(_c(mm))} mm - যে কোষে তা ভাঁজ হয়ে থাকে তার প্রায় 1,000 গুণ।",
                  (mm / 2, mm * 10, mm * 3.4), " mm")
    return _n(f"The distance between adjacent base pairs in B-DNA is 0.34 nm. How long is a DNA molecule of {bp_txt} base pairs?",
              f"বি-ডিএনএ-তে পাশাপাশি দুটো ক্ষারকজোড়ের দূরত্ব 0.34 nm। {bp_txt} ক্ষারকজোড়ের একটা ডিএনএ অণু কত লম্বা?", m,
              f"{bp_txt} x 0.34 x 10⁻⁹ m = {_f(_c(m))} m.",
              f"দৈর্ঘ্য = {bp_txt} x 0.34 x 10⁻⁹ m = {_f(_c(m))} m।",
              (m / 2, m * 10, m * 3.4), " m")


def amino(n_codons):
    nt = n_codons * 3 + 3
    return _n(f"An mRNA coding region, from start codon to stop codon inclusive, is {nt} nucleotides long. How many amino acids are in the polypeptide?",
              f"একটা এম-আরএনএ-র সংকেত অংশ, সূচনা থেকে সমাপ্তি কোডন পর্যন্ত, {nt} নিউক্লিওটাইড লম্বা। পলিপেপটাইডে কয়টি অ্যামিনো অ্যাসিড থাকে?", n_codons,
              f"{nt} ÷ 3 = {nt // 3} codons; the stop codon codes for no amino acid, leaving {n_codons}.",
              f"{nt} ÷ 3 = {nt // 3}টি কোডন; সমাপ্তি কোডন কোনো অ্যামিনো অ্যাসিড দেয় না, তাই {n_codons}টি।",
              (nt // 3, nt, n_codons - 1))


def mitosis_cells(n):
    r = 2 ** n
    return _n(f"A single cell divides by mitosis {n} times in a row, with every daughter cell dividing each time. How many cells result?",
              f"একটা কোষ পরপর {n} বার মাইটোসিসে বিভাজিত হয়, প্রতিবার প্রতিটি অপত্য কোষ বিভাজিত হয়। কয়টি কোষ তৈরি হয়?", r,
              f"The number doubles each round: 2^{n} = {r}.",
              f"প্রতি দফায় সংখ্যা দ্বিগুণ হয়: 2^{n} = {r}টি।",
              (2 * n, n * n, r - 1))


def meiosis(n2, organism_en, organism_bn):
    return _n(f"{organism_en} has {n2} chromosomes in its body cells. How many chromosomes are in each of its gametes?",
              f"{organism_bn}-এর দেহকোষে {n2}টি ক্রোমোজোম আছে। এর প্রতিটি গ্যামেটে কয়টি ক্রোমোজোম থাকে?", n2 // 2,
              f"Meiosis halves the number (2n → n): {n2} ÷ 2 = {n2 // 2}; fertilisation restores {n2}.",
              f"মিয়োসিস সংখ্যা অর্ধেক করে (2n → n): {n2} ÷ 2 = {n2 // 2}; নিষেক আবার {n2} ফিরিয়ে আনে।",
              (n2, n2 * 2, n2 // 4 if n2 % 4 == 0 else n2 // 2 + 1))


def blood_cross(p1_en, p2_en, p_bn, want_en, want_bn, r, how_en, how_bn):
    return _fr(f"Parents with genotypes {p1_en} and {p2_en} have a child. What is the probability that the child has blood group {want_en}?",
               f"{p_bn} জিনোটাইপের বাবা-মায়ের একটা সন্তান হল। সন্তানের রক্তের গ্রুপ {want_bn} হওয়ার সম্ভাবনা কত?", r,
               (F(1, 2), F(3, 4), F(1, 4) if r != F(1, 4) else F(1, 8)), how_en, how_bn)


def x_linked(want_en, want_bn, r, how_en, how_bn):
    return _fr(f"A woman who carries the recessive X-linked colour-blindness allele marries a man with normal vision. What is the probability that {want_en}?",
               f"বর্ণান্ধতার প্রচ্ছন্ন এক্স-সংযুক্ত অ্যালিলের বাহক এক মহিলা স্বাভাবিক দৃষ্টির এক পুরুষকে বিয়ে করলেন। {want_bn} সম্ভাবনা কত?", r,
               (F(1, 2), F(1, 4), F(0) + F(3, 4)), how_en, how_bn)


# ---------------------------------------------------------------- physiology and ecology
def cardiac_output(hr, sv):
    co = hr * sv / 1000
    return _n(f"A person's heart beats {hr} times a minute with a stroke volume of {sv} mL. What is the cardiac output?",
              f"একজনের হৃৎপিণ্ড মিনিটে {hr} বার স্পন্দিত হয়, প্রতি স্পন্দনে {sv} mL রক্ত পাম্প করে। হৃৎ-উৎপাদ কত?", co,
              f"Cardiac output = heart rate x stroke volume = {hr} x {sv} mL = {_f(_c(co))} L/min.",
              f"হৃৎ-উৎপাদ = হৃৎস্পন্দন হার x স্ট্রোক আয়তন = {hr} x {sv} mL = {_f(_c(co))} L/মিনিট।",
              (hr * sv / 100, co / 2, hr / sv), " L/min", " L/মিনিট")


def ventilation(tv, rate):
    v = tv * rate / 1000
    return _n(f"A person breathes {rate} times a minute with a tidal volume of {tv} mL. What is the minute ventilation?",
              f"একজন মিনিটে {rate} বার শ্বাস নেন, প্রতিবার {tv} mL (জোয়ার আয়তন)। মিনিট-প্রশ্বাস কত?", v,
              f"Tidal volume x rate = {tv} x {rate} mL = {_f(_c(v))} L/min.",
              f"জোয়ার আয়তন x হার = {tv} x {rate} mL = {_f(_c(v))} L/মিনিট।",
              (tv * rate / 100, v / 2, tv / rate), " L/min", " L/মিনিট")


def gfr(rate):
    v = rate * 60 * 24 / 1000
    return _n(f"The kidneys filter blood at {rate} mL per minute (the glomerular filtration rate). How much filtrate forms in a day?",
              f"বৃক্ক মিনিটে {rate} mL হারে রক্ত ছাঁকে (গ্লোমেরুলার পরিস্রাবণ হার)। দিনে কত পরিস্রুত তরল তৈরি হয়?", v,
              f"{rate} mL x 60 x 24 = {_f(_c(v))} L; about 99% is reabsorbed, leaving 1-2 L of urine.",
              f"{rate} mL x 60 x 24 = {_f(_c(v))} L; প্রায় 99% পুনঃশোষিত হয়, থাকে 1-2 L মূত্র।",
              (v / 60, v / 10, rate * 24 / 1000), " L")


def ten_percent(e, levels, top_en, top_bn):
    r = e * 0.1 ** levels
    return _n(f"Producers in a food chain fix {e:,} kJ of energy. About how much reaches the {top_en}, {levels} trophic level{'s' if levels > 1 else ''} higher? (10% law)",
              f"একটা খাদ্যশৃঙ্খলে উৎপাদকেরা {e:,} kJ শক্তি আবদ্ধ করে। {levels}টি পুষ্টিস্তর উপরে {top_bn} মোটামুটি কত শক্তি পৌঁছায়? (10% সূত্র)", r,
              f"Lindeman's 10% law: {e:,} x 0.1^{levels} = {_f(_c(r))} kJ.",
              f"লিন্ডেম্যানের 10% সূত্র: {e:,} x 0.1^{levels} = {_f(_c(r))} kJ।",
              (e * 0.1 ** (levels - 1), r / 10, e * 0.9 ** levels), " kJ")


def npp(gpp, resp):
    r = gpp - resp
    return _n(f"An ecosystem has a gross primary productivity of {gpp:,} kcal/m²/yr and its plants respire {resp:,} kcal/m²/yr. What is the net primary productivity?",
              f"একটা বাস্তুতন্ত্রের মোট প্রাথমিক উৎপাদনশীলতা {gpp:,} kcal/m²/বছর, আর উদ্ভিদের শ্বসনে খরচ {resp:,} kcal/m²/বছর। নিট প্রাথমিক উৎপাদনশীলতা কত?", r,
              f"NPP = GPP - respiration = {gpp:,} - {resp:,} = {r:,} kcal/m²/yr, the energy available to consumers.",
              f"নিট উৎপাদনশীলতা = মোট - শ্বসন = {gpp:,} - {resp:,} = {r:,} kcal/m²/বছর, যা খাদকদের জন্য প্রাপ্য।",
              (gpp + resp, resp, gpp), "")


def lincoln(m, c, r):
    n = m * c // r
    return _n(f"Ecologists mark {m} fish and release them. Later they catch {c} fish, of which {r} are marked. Estimate the population.",
              f"বাস্তুবিদরা {m}টি মাছ চিহ্নিত করে ছেড়ে দিলেন। পরে {c}টি মাছ ধরলেন, তার {r}টি চিহ্নিত। জনসংখ্যা কত অনুমান করা যায়?", n,
              f"Lincoln-Petersen index: N = M x C ÷ R = {m} x {c} ÷ {r} = {n:,}.",
              f"লিংকন-পিটারসেন সূচক: N = M x C ÷ R = {m} x {c} ÷ {r} = {n:,}।",
              (m + c, m * r // c if m * r // c > 0 else m, c * r))


def doubling(n0, t, td):
    n = n0 * 2 ** (t // td)
    return _n(f"A bacterial culture starts with {n0:,} cells and doubles every {td} minutes with unlimited food. How many cells are there after {t} minutes?",
              f"একটা ব্যাকটেরিয়া-কালচার {n0:,}টি কোষ দিয়ে শুরু হয় আর অফুরন্ত খাদ্যে প্রতি {td} মিনিটে দ্বিগুণ হয়। {t} মিনিট পরে কয়টি কোষ থাকে?", n,
              f"{t} ÷ {td} = {t // td} doublings: {n0:,} x 2^{t // td} = {n:,} - exponential (J-shaped) growth.",
              f"{t} ÷ {td} = {t // td}টি দ্বিগুণন: {n0:,} x 2^{t // td} = {n:,} - সূচকীয় (J-আকৃতির) বৃদ্ধি।",
              (n0 * (t // td) * 2, n // 2, n0 * t // td))


def growth_rate(b, d, n):
    r = (b - d) * n // 1000
    return _n(f"A town of {n:,} people has a birth rate of {b} and a death rate of {d} per 1,000 per year. Ignoring migration, by how many people does it grow in a year?",
              f"{n:,} জনের একটা শহরে বছরে প্রতি 1,000-এ জন্মহার {b} আর মৃত্যুহার {d}। অভিবাসন বাদ দিলে বছরে জনসংখ্যা কতজন বাড়ে?", r,
              f"Net rate = {b} - {d} = {b - d} per 1,000; {n:,} x {b - d} ÷ 1,000 = {r:,}.",
              f"নিট হার = {b} - {d} = প্রতি 1,000-এ {b - d}; {n:,} x {b - d} ÷ 1,000 = {r:,}জন।",
              (b * n // 1000, (b + d) * n // 1000, r // 10))


def rq(co2, o2, food_en, food_bn):
    r = co2 / o2
    return _n(f"When {food_en} is respired, {co2} molecules of CO₂ are released for every {o2} molecules of O₂ used. What is the respiratory quotient?",
              f"{food_bn} শ্বসনে প্রতি {o2}টি O₂ অণু খরচে {co2}টি CO₂ অণু নির্গত হয়। শ্বসন-অনুপাত (আরকিউ) কত?", r,
              f"RQ = CO₂ released ÷ O₂ used = {co2} ÷ {o2} = {_f(_c(r))}. Carbohydrates give 1, fats about 0.7, proteins about 0.9.",
              f"শ্বসন-অনুপাত = নির্গত CO₂ ÷ খরচ O₂ = {co2} ÷ {o2} = {_f(_c(r))}। শর্করায় 1, চর্বিতে প্রায় 0.7, প্রোটিনে প্রায় 0.9।",
              (o2 / co2, 1 if abs(r - 1) > 0.05 else 0.7, r + 0.3))


def magnification(img_mm, real_um):
    m = img_mm * 1000 / real_um
    return _n(f"A cell {real_um} μm across appears {img_mm} mm wide in a micrograph. What is the magnification?",
              f"{real_um} μm চওড়া একটা কোষ অণুবীক্ষণ-ছবিতে {img_mm} mm চওড়া দেখায়। বিবর্ধন কত?", m,
              f"Magnification = image size ÷ real size = {img_mm * 1000:,} μm ÷ {real_um} μm = {_f(_c(m))} times.",
              f"বিবর্ধন = প্রতিবিম্বের মাপ ÷ প্রকৃত মাপ = {img_mm * 1000:,} μm ÷ {real_um} μm = {_f(_c(m))} গুণ।",
              (img_mm / real_um, m * 10, m / 10), " x", " গুণ")


def density(n, area):
    d = n / area
    return _n(f"A survey counts {n:,} neem trees in {area} hectares of forest. What is the population density?",
              f"একটা সমীক্ষায় {area} হেক্টর বনে {n:,}টি নিমগাছ গোনা হল। জনঘনত্ব কত?", d,
              f"Density = number ÷ area = {n:,} ÷ {area} = {_f(_c(d))} trees per hectare.",
              f"ঘনত্ব = সংখ্যা ÷ ক্ষেত্রফল = {n:,} ÷ {area} = হেক্টরপ্রতি {_f(_c(d))}টি গাছ।",
              (n * area, d * 10, d / 2), " per ha", " প্রতি হেক্টরে")


NUMERIC = [
    dihybrid("both dominant traits"), dihybrid("the first dominant and the second recessive trait"),
    dihybrid("both recessive traits"),
    mono("Aa x aa (a test cross)", "Aa x aa (পরীক্ষা-সংকর)", "homozygous recessive", "সমযুগ্মী প্রচ্ছন্ন", F(1, 2),
         "Aa gives A or a equally; aa gives only a: half the offspring are aa.", "Aa সমানভাবে A বা a দেয়; aa কেবল a: অর্ধেক অপত্য aa।"),
    mono("Aa x Aa", "Aa x Aa", "heterozygous", "বিষমযুগ্মী", F(1, 2),
         "AA : Aa : aa = 1 : 2 : 1, so 2/4 = 1/2 are Aa.", "AA : Aa : aa = 1 : 2 : 1, তাই 2/4 = 1/2 অংশ Aa।"),
    mono("Aa x Aa", "Aa x Aa", "of the dominant phenotype", "প্রকট ফিনোটাইপের", F(3, 4),
         "AA and Aa both show the dominant trait: 1/4 + 2/4 = 3/4.", "AA আর Aa দুটোই প্রকট বৈশিষ্ট্য দেখায়: 1/4 + 2/4 = 3/4।"),
    mono("AaBbCc x AaBbCc", "AaBbCc x AaBbCc", "homozygous recessive for all three genes (aabbcc)", "তিনটি জিনেই সমযুগ্মী প্রচ্ছন্ন (aabbcc)", F(1, 64),
         "Each gene gives 1/4 recessive homozygotes: (1/4)³ = 1/64.", "প্রতিটি জিনে 1/4 সমযুগ্মী প্রচ্ছন্ন: (1/4)³ = 1/64।"),
    genotypes(3), genotypes(4), genotypes(5),
    gametes(3), gametes(4), gametes(6),
    hardy(16), hardy(4), hardy(1), hardy(9),
    chargaff(30), chargaff(18), chargaff(35),
    dna_length("6.6 x 10⁹", 6.6e9), dna_length("4.6 x 10⁶ (E. coli)", 4.6e6),
    amino(150), amino(299), amino(64),
    mitosis_cells(5), mitosis_cells(8), mitosis_cells(10),
    meiosis(46, "A human", "মানুষ"), meiosis(14, "A garden pea", "মটরগাছ"), meiosis(24, "Rice", "ধান"),
    meiosis(8, "The fruit fly Drosophila", "ফলের মাছি ড্রসোফিলা"),
    blood_cross("IᴬIᴬ", "IᴮIᴮ", "IᴬIᴬ আর IᴮIᴮ", "AB", "AB", F(1),
                "Every child gets Iᴬ from one parent and Iᴮ from the other: all are IᴬIᴮ.", "প্রতিটি সন্তান একজনের কাছে Iᴬ, অন্যজনের কাছে Iᴮ পায়: সবাই IᴬIᴮ।"),
    blood_cross("Iᴬi", "Iᴮi", "Iᴬi আর Iᴮi", "O", "O", F(1, 4),
                "Each parent passes i with probability 1/2: 1/2 x 1/2 = 1/4 are ii (group O).", "প্রত্যেক বাবা-মা 1/2 সম্ভাবনায় i দেন: 1/2 x 1/2 = 1/4 হয় ii (গ্রুপ O)।"),
    blood_cross("Iᴬi", "ii", "Iᴬi আর ii", "A", "A", F(1, 2),
                "Half the children get Iᴬ from the first parent and i from the second: Iᴬi, group A.", "অর্ধেক সন্তান প্রথমজনের কাছে Iᴬ আর দ্বিতীয়জনের কাছে i পায়: Iᴬi, গ্রুপ A।"),
    x_linked("their next child is a colour-blind son", "পরের সন্তানটি বর্ণান্ধ ছেলে হওয়ার", F(1, 4),
             "A son (1/2) who receives the mother's affected X (1/2): 1/4. No daughter is colour-blind, but half are carriers.",
             "ছেলে (1/2), যে মায়ের আক্রান্ত X পায় (1/2): 1/4। কোনো মেয়ে বর্ণান্ধ নয়, কিন্তু অর্ধেক বাহক।"),
    x_linked("a son of theirs is colour-blind", "তাদের একটা ছেলে বর্ণান্ধ হওয়ার", F(1, 2),
             "Every son gets his X from his mother, who passes the affected X half the time.",
             "প্রতিটি ছেলে তার X মায়ের কাছে পায়, আর মা অর্ধেক সময় আক্রান্ত X দেন।"),
    cardiac_output(72, 70), cardiac_output(60, 80), cardiac_output(150, 120),
    ventilation(500, 12), ventilation(600, 15),
    gfr(125), gfr(100),
    ten_percent(10000, 3, "tertiary consumers", "তৃতীয় খাদকে"), ten_percent(50000, 2, "secondary consumers", "দ্বিতীয় খাদকে"),
    ten_percent(200000, 4, "top carnivores", "শীর্ষ মাংসাশীতে"),
    npp(20000, 12000), npp(8000, 3500),
    lincoln(120, 150, 30), lincoln(80, 100, 16), lincoln(200, 250, 40),
    doubling(1000, 120, 20), doubling(500, 90, 30), doubling(100, 200, 20),
    growth_rate(28, 8, 50000), growth_rate(20, 12, 200000),
    rq(6, 6, "glucose (C₆H₁₂O₆)", "গ্লুকোজ (C₆H₁₂O₆)"), rq(102, 145, "the fat tripalmitin", "চর্বি ট্রাইপামিটিন"),
    rq(4, 1, "oxalic acid", "অক্সালিক অ্যাসিড"),
    magnification(30, 10), magnification(12, 20), magnification(45, 9),
    density(360, 12), density(1500, 25),
    mono("Aa x Aa", "Aa x Aa", "homozygous recessive", "সমযুগ্মী প্রচ্ছন্ন", F(1, 4),
         "Only aa shows the recessive trait: 1/2 x 1/2 = 1/4.", "কেবল aa প্রচ্ছন্ন বৈশিষ্ট্য দেখায়: 1/2 x 1/2 = 1/4।"),
    mono("AaBb x aabb (a dihybrid test cross)", "AaBb x aabb (দ্বিসংকর পরীক্ষা-সংকর)", "of genotype AaBb", "AaBb জিনোটাইপের", F(1, 4),
         "AaBb makes four gamete types equally (AB, Ab, aB, ab); only AB gives AaBb: 1/4, the 1:1:1:1 ratio.",
         "AaBb সমানভাবে চার রকম গ্যামেট দেয় (AB, Ab, aB, ab); কেবল AB থেকে AaBb: 1/4, 1:1:1:1 অনুপাত।"),
    gametes(5), genotypes(6), hardy(25), hardy(0.25), chargaff(22), amino(100), mitosis_cells(6),
    meiosis(48, "A potato plant", "আলুগাছ"), meiosis(16, "An onion", "পেঁয়াজ"),
    cardiac_output(80, 75), ventilation(450, 16), ten_percent(1000, 1, "herbivores", "তৃণভোজীতে"),
    npp(15000, 9000), lincoln(60, 90, 15), doubling(200, 60, 15), growth_rate(30, 10, 10000),
    magnification(8, 40), density(900, 20),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    _q("Which experiment proved that DNA replication is semi-conservative?", ["Meselson and Stahl's ¹⁵N experiment", "Griffith's transformation experiment", "Hershey and Chase's blender experiment", "Miller and Urey's spark experiment"],
       "After one generation in ¹⁴N, all DNA had intermediate density: each new double helix kept one old strand.",
       "কোন পরীক্ষা প্রমাণ করেছিল যে ডিএনএ প্রতিলিপিকরণ অর্ধ-সংরক্ষণশীল?", ["মেসেলসন আর স্টালের ¹⁵N পরীক্ষা", "গ্রিফিথের রূপান্তর পরীক্ষা", "হার্শে আর চেজের ব্লেন্ডার পরীক্ষা", "মিলার আর উরের স্ফুলিঙ্গ পরীক্ষা"],
       "¹⁴N-এ এক প্রজন্ম পরে সব ডিএনএ-র ঘনত্ব মাঝামাঝি: প্রতিটি নতুন দ্বিসূত্রক একটা পুরোনো সূত্র রেখেছিল।"),
    _q("Hershey and Chase used ³²P and ³⁵S-labelled bacteriophages to show that…", ["DNA, not protein, is the genetic material", "Protein is the genetic material", "RNA carries the code in bacteria", "Viruses have no genetic material"],
       "Only the ³²P (in DNA) entered the bacteria and turned up in the new phages.",
       "হার্শে আর চেজ ³²P আর ³⁵S-চিহ্নিত ব্যাকটেরিওফাজ দিয়ে দেখিয়েছিলেন যে…", ["প্রোটিন নয়, ডিএনএ-ই জিনগত বস্তু", "প্রোটিনই জিনগত বস্তু", "ব্যাকটেরিয়ায় আরএনএ সংকেত বয়", "ভাইরাসের কোনো জিনগত বস্তু নেই"],
       "কেবল ³²P (ডিএনএ-তে) ব্যাকটেরিয়ায় ঢুকেছিল আর নতুন ফাজে পাওয়া গিয়েছিল।"),
    _q("In the lac operon of E. coli, what does lactose (allolactose) do?", ["Binds the repressor so the genes can be transcribed", "Binds the operator directly to stop transcription", "Acts as the RNA polymerase", "Destroys the lac genes"],
       "The repressor can no longer sit on the operator, so the enzymes that digest lactose are made - an inducible system.",
       "ই. কোলাইয়ের ল্যাক অপেরনে ল্যাকটোজ (অ্যালোল্যাকটোজ) কী করে?", ["রিপ্রেসরের সঙ্গে যুক্ত হয়, ফলে জিনগুলোর প্রতিলিপন হয়", "সরাসরি অপারেটরে যুক্ত হয়ে প্রতিলিপন থামায়", "আরএনএ পলিমারেজ হিসেবে কাজ করে", "ল্যাক জিনগুলো ধ্বংস করে"],
       "রিপ্রেসর আর অপারেটরে বসতে পারে না, তাই ল্যাকটোজ-পাচক এনজাইম তৈরি হয় - একটা আবেশযোগ্য ব্যবস্থা।"),
    _q("Why is the genetic code called 'degenerate'?", ["Most amino acids are coded by more than one codon", "One codon codes for several amino acids", "The code changes between species", "Codons overlap"],
       "61 sense codons code for only 20 amino acids; leucine, for example, has six codons.",
       "জিনগত সংকেতকে 'অপজাত' (ডিজেনারেট) বলা হয় কেন?", ["বেশিরভাগ অ্যামিনো অ্যাসিডের একাধিক কোডন আছে", "একটা কোডন কয়েকটা অ্যামিনো অ্যাসিডের সংকেত দেয়", "প্রজাতিভেদে সংকেত বদলায়", "কোডনগুলো একটার উপর আরেকটা পড়ে"],
       "61টি অর্থবোধক কোডন মাত্র 20টি অ্যামিনো অ্যাসিডের সংকেত দেয়; যেমন লিউসিনের ছয়টি কোডন।"),
    _q("Which codon starts translation and also codes for methionine?", ["AUG", "UAA", "UGA", "UAG"],
       "UAA, UAG and UGA are stop codons with no matching tRNA.",
       "কোন কোডন অনুবাদ শুরু করে আর মেথিওনিনেরও সংকেত দেয়?", ["AUG কোডন", "UAA কোডন", "UGA কোডন", "UAG কোডন"],
       "UAA, UAG আর UGA সমাপ্তি কোডন, তাদের মেলানো কোনো টি-আরএনএ নেই।"),
    _q("Which enzyme joins Okazaki fragments on the lagging strand?", ["DNA ligase", "Helicase", "Primase", "Topoisomerase"],
       "DNA polymerase can only build 5' → 3', so the lagging strand is made in pieces that ligase seals.",
       "পশ্চাদ্গামী সূত্রে ওকাজাকি খণ্ডগুলো কোন এনজাইম জোড়ে?", ["ডিএনএ লাইগেজ", "হেলিকেজ", "প্রাইমেজ", "টোপোআইসোমারেজ"],
       "ডিএনএ পলিমারেজ কেবল 5' → 3' দিকে গড়তে পারে, তাই পশ্চাদ্গামী সূত্র খণ্ডে খণ্ডে তৈরি হয়, লাইগেজ সেগুলো জোড়ে।"),
    _q("In eukaryotic RNA processing, what is splicing?", ["Removing introns and joining exons", "Adding a poly-A tail", "Adding the 5' cap", "Translating mRNA into protein"],
       "The mature mRNA keeps only the exons; alternative splicing lets one gene make several proteins.",
       "প্রকৃতকোষী আরএনএ প্রক্রিয়াকরণে স্প্লাইসিং কী?", ["ইন্ট্রন বাদ দিয়ে এক্সনগুলো জোড়া", "পলি-A লেজ যোগ করা", "5' ক্যাপ যোগ করা", "এম-আরএনএ থেকে প্রোটিন অনুবাদ"],
       "পরিণত এম-আরএনএ-তে কেবল এক্সন থাকে; বিকল্প স্প্লাইসিংয়ে একটা জিন কয়েকটা প্রোটিন তৈরি করতে পারে।"),
    _q("A cross between red and white snapdragons gives all pink flowers. This is an example of…", ["Incomplete dominance", "Codominance", "Complete dominance", "Epistasis"],
       "The heterozygote is intermediate; F₂ shows 1 red : 2 pink : 1 white, the phenotype ratio matching the genotype ratio.",
       "লাল আর সাদা স্ন্যাপড্রাগনের সংকরায়ণে সব গোলাপি ফুল হয়। এটা কীসের উদাহরণ?", ["অসম্পূর্ণ প্রকটতা", "সহপ্রকটতা", "সম্পূর্ণ প্রকটতা", "এপিস্ট্যাসিস"],
       "বিষমযুগ্মী মাঝামাঝি; F₂-তে 1 লাল : 2 গোলাপি : 1 সাদা, ফিনোটাইপ অনুপাত জিনোটাইপ অনুপাতের সমান।"),
    _q("Blood group AB shows both A and B antigens on red cells. This is…", ["Codominance", "Incomplete dominance", "Polygenic inheritance", "Linkage"],
       "Both alleles Iᴬ and Iᴮ are fully expressed together in the heterozygote.",
       "AB রক্তের গ্রুপে লোহিত কণিকায় A আর B দুটো অ্যান্টিজেনই থাকে। এটা…", ["সহপ্রকটতা", "অসম্পূর্ণ প্রকটতা", "বহুজিনীয় উত্তরাধিকার", "সংযোগ (লিংকেজ)"],
       "বিষমযুগ্মীতে Iᴬ আর Iᴮ দুটো অ্যালিলই একসঙ্গে পুরোপুরি প্রকাশিত হয়।"),
    _q("Human skin colour varies continuously because it is controlled by…", ["Several genes with additive effects (polygenic inheritance)", "A single gene with two alleles", "Only the environment", "Mitochondrial DNA"],
       "Many genes each add a little pigment, giving a bell-shaped spread of phenotypes.",
       "মানুষের ত্বকের রং অবিচ্ছিন্নভাবে বদলায় কারণ তা নিয়ন্ত্রিত হয়…", ["যোগাত্মক প্রভাবের কয়েকটা জিন দিয়ে (বহুজিনীয় উত্তরাধিকার)", "দুই অ্যালিলের একটা জিন দিয়ে", "কেবল পরিবেশ দিয়ে", "মাইটোকন্ড্রিয়ার ডিএনএ দিয়ে"],
       "অনেক জিন প্রত্যেকে একটু করে রঞ্জক যোগ করে, ফলে ফিনোটাইপ ঘণ্টা-আকৃতিতে ছড়ায়।"),
    _q("Why do linked genes often fail to assort independently?", ["They lie close together on the same chromosome", "They are on different chromosomes", "They are always recessive", "They are in mitochondria"],
       "Crossing over rarely separates genes that are close; recombination frequency measures the distance between them.",
       "সংযুক্ত জিন প্রায়ই স্বাধীনভাবে বিন্যস্ত হয় না কেন?", ["তারা একই ক্রোমোজোমে কাছাকাছি থাকে", "তারা ভিন্ন ক্রোমোজোমে থাকে", "তারা সবসময় প্রচ্ছন্ন", "তারা মাইটোকন্ড্রিয়ায় থাকে"],
       "কাছাকাছি জিনকে ক্রসিং ওভার কদাচিৎ আলাদা করে; পুনঃসংযোজন-হার তাদের দূরত্ব মাপে।"),
    _q("Down's syndrome is caused by…", ["An extra copy of chromosome 21 (trisomy 21)", "A missing X chromosome", "A point mutation in haemoglobin", "An extra Y chromosome"],
       "It usually arises from non-disjunction in meiosis; Turner's syndrome is 45,X0 and Klinefelter's is 47,XXY.",
       "ডাউন সিনড্রোমের কারণ…", ["21 নম্বর ক্রোমোজোমের একটা বাড়তি কপি (ট্রাইসোমি 21)", "একটা X ক্রোমোজোমের অভাব", "হিমোগ্লোবিনে বিন্দু-পরিব্যক্তি", "একটা বাড়তি Y ক্রোমোজোম"],
       "সাধারণত মিয়োসিসে অ-বিচ্ছেদ থেকে ঘটে; টার্নার সিনড্রোম 45,X0 আর ক্লাইনফেল্টার 47,XXY।"),
    _q("Sickle-cell anaemia results from…", ["A single base substitution changing glutamic acid to valine in β-globin", "An extra chromosome", "A deletion of a whole gene", "A vitamin deficiency"],
       "GAG → GTG at codon 6; heterozygotes resist malaria, which keeps the allele common in some regions.",
       "সিকল-সেল রক্তাল্পতার কারণ…", ["β-গ্লোবিনে একটা ক্ষারক প্রতিস্থাপনে গ্লুটামিক অ্যাসিড বদলে ভ্যালিন", "একটা বাড়তি ক্রোমোজোম", "পুরো একটা জিন মুছে যাওয়া", "ভিটামিনের অভাব"],
       "6 নম্বর কোডনে GAG → GTG; বিষমযুগ্মীরা ম্যালেরিয়া প্রতিরোধ করে, তাই কিছু অঞ্চলে অ্যালিলটা সাধারণ থাকে।"),
    _q("In humans, the sex of a child is determined by…", ["Whether the sperm carries an X or a Y chromosome", "The mother's egg", "The temperature during pregnancy", "The father's age"],
       "All eggs carry X; an X sperm gives XX (girl), a Y sperm gives XY (boy).",
       "মানুষে সন্তানের লিঙ্গ নির্ধারিত হয়…", ["শুক্রাণু X না Y ক্রোমোজোম বয় তা দিয়ে", "মায়ের ডিম্বাণু দিয়ে", "গর্ভাবস্থার তাপমাত্রা দিয়ে", "বাবার বয়স দিয়ে"],
       "সব ডিম্বাণু X বয়; X শুক্রাণু XX (মেয়ে), Y শুক্রাণু XY (ছেলে) দেয়।"),
    _q("Which statement fits the Hardy-Weinberg principle?", ["Allele frequencies stay constant without mutation, migration, selection, drift or non-random mating", "Allele frequencies always change each generation", "Dominant alleles always become more common", "It applies only to small populations"],
       "Any change in allele frequencies signals that evolution is happening.",
       "কোন বিবৃতি হার্ডি-ওয়াইনবার্গ নীতির সঙ্গে মেলে?", ["পরিব্যক্তি, অভিপ্রয়াণ, নির্বাচন, প্রবাহ বা অ-এলোমেলো মিলন না থাকলে অ্যালিল-হার স্থির থাকে", "প্রতি প্রজন্মে অ্যালিল-হার সবসময় বদলায়", "প্রকট অ্যালিল সবসময় বেশি সাধারণ হয়", "কেবল ছোট জনগোষ্ঠীতে খাটে"],
       "অ্যালিল-হারে যেকোনো পরিবর্তন মানে বিবর্তন ঘটছে।"),
    _q("The wing of a bat and the arm of a human are…", ["Homologous organs: same origin, different function", "Analogous organs: same function, different origin", "Vestigial organs", "Unrelated structures"],
       "Both share the same pentadactyl bone plan - evidence of common ancestry (divergent evolution).",
       "বাদুড়ের ডানা আর মানুষের হাত…", ["সমসংস্থ অঙ্গ: একই উৎপত্তি, ভিন্ন কাজ", "সমবৃত্তীয় অঙ্গ: একই কাজ, ভিন্ন উৎপত্তি", "নিষ্ক্রিয় অঙ্গ", "সম্পর্কহীন গঠন"],
       "দুটোরই একই পঞ্চাঙ্গুলি হাড়ের নকশা - সাধারণ পূর্বপুরুষের প্রমাণ (অপসারী বিবর্তন)।"),
    _q("The wings of a butterfly and a bird are…", ["Analogous organs (convergent evolution)", "Homologous organs", "Vestigial organs", "Atavistic organs"],
       "They do the same job but are built from completely different tissues.",
       "প্রজাপতি আর পাখির ডানা…", ["সমবৃত্তীয় অঙ্গ (অভিসারী বিবর্তন)", "সমসংস্থ অঙ্গ", "নিষ্ক্রিয় অঙ্গ", "পূর্বপুরুষ-অনুরূপ অঙ্গ"],
       "একই কাজ করে কিন্তু সম্পূর্ণ ভিন্ন কলা দিয়ে তৈরি।"),
    _q("Darwin's finches on the Galapagos Islands illustrate…", ["Adaptive radiation from a common ancestor", "Inheritance of acquired characters", "Spontaneous generation", "Convergent evolution only"],
       "One ancestral finch species gave rise to many species with beaks suited to different foods.",
       "গালাপাগোস দ্বীপের ডারউইনের ফিঞ্চ পাখি কী দেখায়?", ["একই পূর্বপুরুষ থেকে অভিযোজিত বিকিরণ", "অর্জিত বৈশিষ্ট্যের উত্তরাধিকার", "স্বতঃস্ফূর্ত জীবনোৎপত্তি", "কেবল অভিসারী বিবর্তন"],
       "একটা পূর্বপুরুষ ফিঞ্চ প্রজাতি থেকে বিভিন্ন খাদ্যের উপযোগী ঠোঁটের অনেক প্রজাতি তৈরি হয়েছে।"),
    _q("Industrial melanism in the peppered moth is an example of…", ["Natural selection", "Mutation pressure only", "Lamarckism", "Genetic drift only"],
       "Dark moths survived better on soot-darkened trees; when pollution fell, pale moths became common again.",
       "পেপার্ড মথে শিল্পজাত মেলানিজম কীসের উদাহরণ?", ["প্রাকৃতিক নির্বাচন", "কেবল পরিব্যক্তির চাপ", "ল্যামার্কবাদ", "কেবল জিনগত প্রবাহ"],
       "ঝুলকালো গাছে কালো মথ বেশি বাঁচত; দূষণ কমলে আবার ফ্যাকাশে মথ বেড়েছে।"),
    _q("In C₄ plants such as maize, the first stable product of CO₂ fixation is…", ["Oxaloacetic acid, a 4-carbon compound", "3-phosphoglyceric acid", "Glucose", "Ribulose bisphosphate"],
       "PEP carboxylase fixes CO₂ in mesophyll cells; Kranz anatomy concentrates it around RuBisCO, cutting photorespiration.",
       "ভুট্টার মতো C₄ উদ্ভিদে CO₂ আবদ্ধকরণের প্রথম স্থায়ী উৎপাদ…", ["অক্সালোঅ্যাসিটিক অ্যাসিড, একটা 4-কার্বন যৌগ", "3-ফসফোগ্লিসারিক অ্যাসিড", "গ্লুকোজ", "রাইবুলোজ বিসফসফেট"],
       "মেসোফিল কোষে পিইপি কার্বক্সিলেজ CO₂ আবদ্ধ করে; ক্রাঞ্জ গঠন রুবিস্কোর চারপাশে তা ঘনীভূত করে, আলোক-শ্বসন কমায়।"),
    _q("Photorespiration occurs because RuBisCO can also…", ["Bind O₂ instead of CO₂", "Split water", "Make ATP directly", "Fix nitrogen"],
       "At high temperature and low CO₂ the oxygenase reaction wastes fixed carbon; C₄ and CAM plants avoid it.",
       "আলোক-শ্বসন ঘটে কারণ রুবিস্কো…", ["CO₂-এর বদলে O₂-এর সঙ্গে যুক্ত হতে পারে", "জল ভাঙতে পারে", "সরাসরি এটিপি তৈরি করতে পারে", "নাইট্রোজেন আবদ্ধ করতে পারে"],
       "বেশি তাপমাত্রা আর কম CO₂-তে অক্সিজিনেজ বিক্রিয়া আবদ্ধ কার্বন নষ্ট করে; C₄ আর CAM উদ্ভিদ তা এড়ায়।"),
    _q("In the light reactions of photosynthesis, oxygen comes from…", ["The splitting of water (photolysis)", "Carbon dioxide", "Glucose", "Chlorophyll"],
       "Experiments with ¹⁸O-labelled water confirmed it; the electrons from water reduce NADP⁺.",
       "সালোকসংশ্লেষের আলোক-দশায় অক্সিজেন আসে…", ["জলের বিভাজন (ফটোলাইসিস) থেকে", "কার্বন ডাইঅক্সাইড থেকে", "গ্লুকোজ থেকে", "ক্লোরোফিল থেকে"],
       "¹⁸O-চিহ্নিত জল দিয়ে পরীক্ষা তা নিশ্চিত করেছে; জলের ইলেকট্রন NADP⁺-কে বিজারিত করে।"),
    _q("What is the net gain of ATP from glycolysis of one glucose molecule?", ["2 ATP", "36 ATP", "4 ATP", "0 ATP"],
       "4 ATP are made but 2 are used in the first steps; 2 NADH are also produced.",
       "একটা গ্লুকোজ অণুর গ্লাইকোলাইসিসে নিট কয়টি এটিপি লাভ হয়?", ["2টি এটিপি", "36টি এটিপি", "4টি এটিপি", "0টি এটিপি"],
       "4টি এটিপি তৈরি হয় কিন্তু প্রথম ধাপে 2টি খরচ হয়; 2টি এনএডিএইচ-ও তৈরি হয়।"),
    _q("Where does the Krebs (citric acid) cycle take place in a eukaryotic cell?", ["The mitochondrial matrix", "The cytoplasm", "The inner thylakoid space", "The nucleus"],
       "Glycolysis happens in the cytoplasm; the electron transport chain sits on the inner mitochondrial membrane.",
       "প্রকৃতকোষে ক্রেবস (সাইট্রিক অ্যাসিড) চক্র কোথায় ঘটে?", ["মাইটোকন্ড্রিয়ার ধাত্র", "সাইটোপ্লাজম", "থাইলাকয়েডের ভেতরের স্থান", "নিউক্লিয়াস"],
       "গ্লাইকোলাইসিস সাইটোপ্লাজমে; ইলেকট্রন পরিবহন শৃঙ্খল মাইটোকন্ড্রিয়ার ভেতরের পর্দায়।"),
    _q("Which plant hormone promotes stem elongation and is used to make seedless grapes bigger?", ["Gibberellin", "Abscisic acid", "Ethylene", "Cytokinin"],
       "Gibberellins lengthen internodes and fruit; abscisic acid closes stomata, ethylene ripens fruit, cytokinins promote cell division.",
       "কোন উদ্ভিদ-হরমোন কাণ্ডের দৈর্ঘ্যবৃদ্ধি ঘটায় আর বীজহীন আঙুরকে বড় করতে লাগে?", ["জিব্বেরেলিন", "অ্যাবসিসিক অ্যাসিড", "ইথিলিন", "সাইটোকাইনিন"],
       "জিব্বেরেলিন পর্বমধ্য আর ফল লম্বা করে; অ্যাবসিসিক অ্যাসিড পত্ররন্ধ্র বন্ধ করে, ইথিলিন ফল পাকায়, সাইটোকাইনিন কোষবিভাজন ঘটায়।"),
    _q("Which hormone is called the 'stress hormone' of plants because it closes stomata during drought?", ["Abscisic acid", "Auxin", "Gibberellin", "Florigen"],
       "ABA also keeps seeds and buds dormant until conditions improve.",
       "খরার সময় পত্ররন্ধ্র বন্ধ করে বলে কোন হরমোনকে উদ্ভিদের 'চাপ-হরমোন' বলা হয়?", ["অ্যাবসিসিক অ্যাসিড", "অক্সিন", "জিব্বেরেলিন", "ফ্লোরিজেন"],
       "অ্যাবসিসিক অ্যাসিড অবস্থা ভালো না হওয়া পর্যন্ত বীজ আর মুকুলকে সুপ্ত রাখে।"),
    _q("Apical dominance, where the main shoot tip suppresses side buds, is caused by…", ["Auxin", "Ethylene", "Abscisic acid", "Gibberellin"],
       "Gardeners pinch off the tip to make a bushier plant; cytokinins counteract the effect.",
       "শীর্ষ-প্রকটতা, যেখানে প্রধান বিটপের অগ্রভাগ পার্শ্বমুকুল দমিয়ে রাখে, কীসের কারণে?", ["অক্সিন", "ইথিলিন", "অ্যাবসিসিক অ্যাসিড", "জিব্বেরেলিন"],
       "মালিরা অগ্রভাগ ছেঁটে গাছকে ঝোপালো করেন; সাইটোকাইনিন এই প্রভাবের বিরোধিতা করে।"),
    _q("A plant that flowers only when nights are longer than a critical length is…", ["A short-day plant", "A long-day plant", "A day-neutral plant", "A C₄ plant"],
       "It is really the length of uninterrupted darkness that matters; a flash of light at night can stop flowering.",
       "যে উদ্ভিদ কেবল রাত একটা নির্দিষ্ট দৈর্ঘ্যের বেশি হলে ফুল ফোটায়, সেটা…", ["স্বল্প-দিবা উদ্ভিদ", "দীর্ঘ-দিবা উদ্ভিদ", "দিবা-নিরপেক্ষ উদ্ভিদ", "C₄ উদ্ভিদ"],
       "আসলে নিরবচ্ছিন্ন অন্ধকারের দৈর্ঘ্যই গুরুত্বপূর্ণ; রাতে এক ঝলক আলোয় ফুল ফোটা বন্ধ হতে পারে।"),
    _q("Water rises in tall trees mainly because of…", ["Transpiration pull with cohesion of water molecules", "Root pressure alone", "Capillarity alone", "Active pumping by phloem"],
       "Evaporation from leaves pulls a continuous water column up the xylem; hydrogen bonds keep it from breaking.",
       "লম্বা গাছে জল ওঠে প্রধানত…", ["জলের অণুর সংসক্তিসহ প্রস্বেদন-টানে", "কেবল মূলজ চাপে", "কেবল কৈশিকতায়", "ফ্লোয়েমের সক্রিয় পাম্পিংয়ে"],
       "পাতা থেকে বাষ্পীভবন জাইলেম বরাবর অবিচ্ছিন্ন জলস্তম্ভকে উপরে টানে; হাইড্রোজেন বন্ধন তা ভাঙতে দেয় না।"),
    _q("Which tissue transports sugars from leaves to the rest of the plant?", ["Phloem", "Xylem", "Cork", "Sclerenchyma"],
       "Sugar moves by mass flow from 'sources' to 'sinks' (pressure-flow hypothesis).",
       "কোন কলা পাতা থেকে গাছের বাকি অংশে শর্করা পরিবহন করে?", ["ফ্লোয়েম", "জাইলেম", "কর্ক", "স্ক্লেরেনকাইমা"],
       "শর্করা 'উৎস' থেকে 'গন্তব্যে' গণ-প্রবাহে চলে (চাপ-প্রবাহ প্রকল্প)।"),
    _q("Leghaemoglobin in the root nodules of legumes…", ["Keeps oxygen low so nitrogenase can work", "Fixes nitrogen itself", "Makes the nodules green", "Stores starch"],
       "Nitrogenase is destroyed by oxygen; leghaemoglobin mops it up and turns the nodules pink.",
       "শিম্বগোত্রীয় উদ্ভিদের মূলের অর্বুদে লেগহিমোগ্লোবিন…", ["অক্সিজেন কম রাখে যাতে নাইট্রোজিনেজ কাজ করতে পারে", "নিজেই নাইট্রোজেন আবদ্ধ করে", "অর্বুদকে সবুজ করে", "শ্বেতসার জমায়"],
       "অক্সিজেন নাইট্রোজিনেজকে নষ্ট করে; লেগহিমোগ্লোবিন তা শুষে নেয় আর অর্বুদকে গোলাপি করে।"),
    _q("A shift of the oxygen-haemoglobin dissociation curve to the right means…", ["Haemoglobin releases oxygen more easily to tissues", "Haemoglobin binds oxygen more tightly", "Less CO₂ in the blood", "Lower body temperature"],
       "More CO₂, acid, heat or 2,3-BPG (the Bohr effect) shift it right - just what active muscles need.",
       "অক্সিজেন-হিমোগ্লোবিন বিয়োজন রেখা ডানে সরা মানে…", ["হিমোগ্লোবিন কলায় সহজে অক্সিজেন ছাড়ে", "হিমোগ্লোবিন অক্সিজেনকে আরও শক্তভাবে বাঁধে", "রক্তে কম CO₂", "দেহের তাপমাত্রা কম"],
       "বেশি CO₂, অম্লতা, তাপ বা 2,3-বিপিজি (বোর প্রভাব) একে ডানে সরায় - সক্রিয় পেশির ঠিক যা দরকার।"),
    _q("Most carbon dioxide is carried in the blood as…", ["Bicarbonate ions in the plasma", "Dissolved CO₂ gas", "Carbaminohaemoglobin only", "Carbon monoxide"],
       "About 70% travels as HCO₃⁻, formed quickly in red cells by carbonic anhydrase.",
       "রক্তে বেশিরভাগ কার্বন ডাইঅক্সাইড বাহিত হয়…", ["প্লাজমায় বাইকার্বনেট আয়ন হিসেবে", "দ্রবীভূত CO₂ গ্যাস হিসেবে", "কেবল কার্বামিনোহিমোগ্লোবিন হিসেবে", "কার্বন মনোক্সাইড হিসেবে"],
       "প্রায় 70% HCO₃⁻ হিসেবে চলে, যা লোহিত কণিকায় কার্বনিক অ্যানহাইড্রেজ দ্রুত তৈরি করে।"),
    _q("Which structure is the natural pacemaker of the human heart?", ["The sino-atrial (SA) node", "The atrio-ventricular (AV) node", "The bundle of His", "The mitral valve"],
       "The SA node in the right atrium sets the rhythm; the AV node delays the impulse so atria empty first.",
       "মানুষের হৃৎপিণ্ডের প্রাকৃতিক পেসমেকার কোনটা?", ["সাইনো-অ্যাট্রিয়াল (এসএ) নোড", "অ্যাট্রিও-ভেন্ট্রিকুলার (এভি) নোড", "হিজের বান্ডল", "মাইট্রাল কপাটিকা"],
       "ডান অলিন্দের এসএ নোড ছন্দ ঠিক করে; এভি নোড আবেগকে দেরি করায় যাতে অলিন্দ আগে খালি হয়।"),
    _q("In an ECG, the QRS complex represents…", ["Ventricular depolarisation", "Atrial depolarisation", "Ventricular repolarisation", "Closing of the valves"],
       "The P wave is atrial depolarisation and the T wave is ventricular repolarisation.",
       "ইসিজি-তে QRS জটিলাংশ বোঝায়…", ["নিলয়ের বিমেরুকরণ", "অলিন্দের বিমেরুকরণ", "নিলয়ের পুনর্মেরুকরণ", "কপাটিকা বন্ধ হওয়া"],
       "P তরঙ্গ অলিন্দের বিমেরুকরণ আর T তরঙ্গ নিলয়ের পুনর্মেরুকরণ।"),
    _q("Which hormone makes the kidney collecting ducts reabsorb more water?", ["Antidiuretic hormone (vasopressin)", "Aldosterone", "Insulin", "Thyroxine"],
       "ADH from the posterior pituitary inserts water channels; without it, large volumes of dilute urine form (diabetes insipidus).",
       "কোন হরমোন বৃক্কের সংগ্রাহক নালিকে বেশি জল পুনঃশোষণ করায়?", ["অ্যান্টিডাইইউরেটিক হরমোন (ভেসোপ্রেসিন)", "অ্যালডোস্টেরন", "ইনসুলিন", "থাইরক্সিন"],
       "পশ্চাৎ পিটুইটারির এই হরমোন জল-চ্যানেল বসায়; এটা না থাকলে প্রচুর পাতলা মূত্র হয় (ডায়াবেটিস ইনসিপিডাস)।"),
    _q("Where is most of the glomerular filtrate reabsorbed?", ["The proximal convoluted tubule", "The loop of Henle", "The collecting duct", "The urinary bladder"],
       "About 65-70% of water and nearly all glucose and amino acids are taken back there.",
       "গ্লোমেরুলার পরিস্রুতের বেশিরভাগ কোথায় পুনঃশোষিত হয়?", ["নিকটবর্তী সংবর্তিত নালিকায়", "হেনলির লুপে", "সংগ্রাহক নালিতে", "মূত্রথলিতে"],
       "প্রায় 65-70% জল আর প্রায় সব গ্লুকোজ ও অ্যামিনো অ্যাসিড সেখানে ফেরত নেওয়া হয়।"),
    _q("In a nerve fibre at rest, the inside of the membrane is…", ["Negative relative to the outside, about -70 mV", "Positive relative to the outside", "At zero potential", "Full of sodium ions"],
       "The Na⁺/K⁺ pump and leaky K⁺ channels keep the inside negative; an action potential briefly reverses it.",
       "বিশ্রামে থাকা স্নায়ুতন্তুর পর্দার ভেতরের দিক…", ["বাইরের তুলনায় ঋণাত্মক, প্রায় -70 mV", "বাইরের তুলনায় ধনাত্মক", "শূন্য বিভবে", "সোডিয়াম আয়নে ভরা"],
       "Na⁺/K⁺ পাম্প আর ছিদ্রযুক্ত K⁺ চ্যানেল ভেতরকে ঋণাত্মক রাখে; কর্মবিভব একে ক্ষণিকের জন্য উল্টে দেয়।"),
    _q("Why does impulse conduction speed up in myelinated nerve fibres?", ["The impulse jumps from one node of Ranvier to the next (saltatory conduction)", "Myelin carries electricity", "There are no synapses", "The fibre is thinner"],
       "Myelin insulates the axon, so the action potential is regenerated only at the gaps.",
       "মায়েলিনযুক্ত স্নায়ুতন্তুতে আবেগ-পরিবহন দ্রুত হয় কেন?", ["আবেগ এক র‍্যানভিয়ারের পর্ব থেকে পরেরটায় লাফিয়ে চলে (লম্ফন পরিবহন)", "মায়েলিন তড়িৎ বহন করে", "কোনো সিন্যাপস নেই", "তন্তু সরু"],
       "মায়েলিন অ্যাক্সনকে অন্তরিত করে, তাই কর্মবিভব কেবল ফাঁকগুলোয় নতুন করে তৈরি হয়।"),
    _q("During muscle contraction, what happens according to the sliding filament theory?", ["Actin filaments slide over myosin, shortening the sarcomere", "Myosin filaments shorten", "Actin filaments shorten", "The A band shortens"],
       "Myosin heads pull actin inward using ATP; the I band and H zone shrink while the A band stays the same.",
       "পেশি-সংকোচনের সময় সরণশীল তন্তু তত্ত্ব অনুযায়ী কী ঘটে?", ["অ্যাক্টিন তন্তু মায়োসিনের উপর দিয়ে সরে সারকোমিয়ার ছোট করে", "মায়োসিন তন্তু ছোট হয়", "অ্যাক্টিন তন্তু ছোট হয়", "A ব্যান্ড ছোট হয়"],
       "মায়োসিনের মাথা এটিপি খরচ করে অ্যাক্টিনকে ভেতরে টানে; I ব্যান্ড আর H অঞ্চল ছোট হয়, A ব্যান্ড একই থাকে।"),
    _q("Which ion released from the sarcoplasmic reticulum triggers muscle contraction?", ["Calcium (Ca²⁺)", "Sodium (Na⁺)", "Chloride (Cl⁻)", "Iron (Fe²⁺)"],
       "Ca²⁺ binds troponin, which moves tropomyosin off actin's binding sites.",
       "সারকোপ্লাজমীয় জালিকা থেকে মুক্ত কোন আয়ন পেশি-সংকোচন শুরু করে?", ["ক্যালসিয়াম (Ca²⁺)", "সোডিয়াম (Na⁺)", "ক্লোরাইড (Cl⁻)", "লোহা (Fe²⁺)"],
       "Ca²⁺ ট্রোপোনিনে যুক্ত হয়, যা ট্রোপোমায়োসিনকে অ্যাক্টিনের বন্ধনস্থল থেকে সরিয়ে দেয়।"),
    _q("Which hormone surge triggers ovulation in the menstrual cycle?", ["Luteinising hormone (LH)", "Progesterone", "Oxytocin", "Prolactin"],
       "The LH surge around day 14 ruptures the Graafian follicle, which then becomes the corpus luteum.",
       "ঋতুচক্রে কোন হরমোনের হঠাৎ বৃদ্ধি ডিম্বস্ফোটন ঘটায়?", ["লিউটিনাইজিং হরমোন (এলএইচ)", "প্রোজেস্টেরন", "অক্সিটোসিন", "প্রোল্যাকটিন"],
       "প্রায় 14 নম্বর দিনে এলএইচ-এর হঠাৎ বৃদ্ধি গ্রাফিয়ান ফলিকল ফাটায়, যা পরে কর্পাস লুটিয়াম হয়।"),
    _q("Which hormone, made by the embryo, keeps the corpus luteum active in early pregnancy?", ["Human chorionic gonadotropin (hCG)", "FSH", "Testosterone", "Thyroxine"],
       "Pregnancy tests detect hCG in urine; the corpus luteum keeps making progesterone to maintain the uterine lining.",
       "ভ্রূণের তৈরি কোন হরমোন গর্ভাবস্থার শুরুতে কর্পাস লুটিয়ামকে সক্রিয় রাখে?", ["হিউম্যান কোরিওনিক গোনাডোট্রপিন (এইচসিজি)", "এফএসএইচ", "টেস্টোস্টেরন", "থাইরক্সিন"],
       "গর্ভ-পরীক্ষা মূত্রে এইচসিজি শনাক্ত করে; কর্পাস লুটিয়াম জরায়ুর আস্তরণ বজায় রাখতে প্রোজেস্টেরন তৈরি করে চলে।"),
    _q("In human spermatogenesis, one primary spermatocyte finally gives…", ["Four sperm", "One sperm and three polar bodies", "Two sperm", "Eight sperm"],
       "In oogenesis, by contrast, one primary oocyte gives one ovum and polar bodies.",
       "মানুষের শুক্রাণুজননে একটা প্রাথমিক স্পার্মাটোসাইট শেষে দেয়…", ["চারটি শুক্রাণু", "একটা শুক্রাণু আর তিনটি পোলার বডি", "দুটো শুক্রাণু", "আটটি শুক্রাণু"],
       "উল্টো দিকে ডিম্বাণুজননে একটা প্রাথমিক উসাইট একটা ডিম্বাণু আর পোলার বডি দেয়।"),
    _q("Double fertilisation, unique to flowering plants, produces…", ["A diploid zygote and a triploid endosperm", "Two embryos", "A haploid embryo", "Two seeds"],
       "One male gamete fuses with the egg; the other fuses with the two polar nuclei to form the food-storing endosperm.",
       "সপুষ্পক উদ্ভিদের বিশেষ দ্বি-নিষেক তৈরি করে…", ["একটা দ্বিপ্লয়েড জাইগোট আর একটা ত্রিপ্লয়েড সস্য", "দুটো ভ্রূণ", "একটা একপ্লয়েড ভ্রূণ", "দুটো বীজ"],
       "একটা পুং-গ্যামেট ডিম্বাণুর সঙ্গে মেলে; অন্যটা দুটো মেরু-নিউক্লিয়াসের সঙ্গে মিলে খাদ্য-সঞ্চয়ী সস্য গড়ে।"),
    _q("Which is a barrier method of contraception that also protects against sexually transmitted infections?", ["Condoms", "Oral contraceptive pills", "A copper IUD", "Vasectomy"],
       "Pills, IUDs and sterilisation prevent pregnancy but not infections such as HIV.",
       "কোনটা জন্মনিয়ন্ত্রণের বাধা-পদ্ধতি, যা যৌনবাহিত সংক্রমণ থেকেও রক্ষা করে?", ["কনডম", "মুখে খাওয়ার গর্ভনিরোধক বড়ি", "তামার আইইউডি", "ভ্যাসেকটমি"],
       "বড়ি, আইইউডি আর বন্ধ্যাকরণ গর্ভ রোধ করে কিন্তু এইচআইভির মতো সংক্রমণ নয়।"),
    _q("Which cells does HIV mainly attack?", ["Helper T cells (CD4⁺)", "Red blood cells", "Platelets", "B cells only"],
       "Loss of helper T cells cripples both antibody and cell-mediated immunity, leading to AIDS.",
       "এইচআইভি প্রধানত কোন কোষ আক্রমণ করে?", ["সাহায্যকারী টি কোষ (CD4⁺)", "লোহিত রক্তকণিকা", "অণুচক্রিকা", "কেবল বি কোষ"],
       "সাহায্যকারী টি কোষ হারালে অ্যান্টিবডি আর কোষ-মাধ্যমিক দুই অনাক্রম্যতাই ভেঙে পড়ে, পরিণতি এইডস।"),
    _q("Vaccination gives protection mainly by producing…", ["Memory B and T cells", "Instant antibodies from another person", "Antibiotics", "Interferon only"],
       "This is active immunity; injecting ready-made antibodies (as for snakebite) is passive immunity.",
       "টিকা প্রধানত কী তৈরি করে সুরক্ষা দেয়?", ["স্মৃতি বি আর টি কোষ", "অন্য মানুষের তৈরি তাৎক্ষণিক অ্যান্টিবডি", "অ্যান্টিবায়োটিক", "কেবল ইন্টারফেরন"],
       "এটা সক্রিয় অনাক্রম্যতা; তৈরি অ্যান্টিবডি ইনজেকশন দেওয়া (যেমন সাপের কামড়ে) নিষ্ক্রিয় অনাক্রম্যতা।"),
    _q("Which antibody crosses the placenta to protect the foetus?", ["IgG", "IgM", "IgA", "IgE"],
       "IgA protects the newborn through colostrum; IgE is involved in allergies.",
       "কোন অ্যান্টিবডি অমরা পেরিয়ে ভ্রূণকে রক্ষা করে?", ["আইজিজি", "আইজিএম", "আইজিএ", "আইজিই"],
       "আইজিএ শালদুধের মাধ্যমে নবজাতককে রক্ষা করে; আইজিই অ্যালার্জিতে জড়িত।"),
    _q("Malaria is caused by…", ["The protozoan Plasmodium, spread by female Anopheles mosquitoes", "A virus spread by Aedes mosquitoes", "A bacterium in contaminated water", "A fungus on the skin"],
       "Plasmodium multiplies in the liver and red blood cells; the rupture of red cells causes the cycles of fever.",
       "ম্যালেরিয়ার কারণ…", ["প্রোটোজোয়া প্লাজমোডিয়াম, স্ত্রী অ্যানোফিলিস মশা দিয়ে ছড়ায়", "এডিস মশাবাহিত একটা ভাইরাস", "দূষিত জলের একটা ব্যাকটেরিয়া", "ত্বকের একটা ছত্রাক"],
       "প্লাজমোডিয়াম যকৃৎ আর লোহিত কণিকায় বংশবৃদ্ধি করে; লোহিত কণিকা ফাটলে পর্যায়ক্রমে জ্বর আসে।"),
    _q("Cancer cells differ from normal cells because they…", ["Lose contact inhibition and divide without control", "Never divide", "Have no DNA", "Always come from viruses"],
       "Mutations in oncogenes and tumour-suppressor genes remove the normal brakes on division.",
       "ক্যান্সার কোষ স্বাভাবিক কোষ থেকে আলাদা কারণ তারা…", ["স্পর্শ-নিরোধ হারিয়ে অনিয়ন্ত্রিতভাবে বিভাজিত হয়", "কখনো বিভাজিত হয় না", "তাদের ডিএনএ নেই", "সবসময় ভাইরাস থেকে আসে"],
       "অনকোজিন আর টিউমার-দমনকারী জিনে পরিব্যক্তি বিভাজনের স্বাভাবিক ব্রেক সরিয়ে দেয়।"),
    _q("Restriction enzymes such as EcoRI are used in genetic engineering to…", ["Cut DNA at specific recognition sequences", "Join DNA fragments", "Copy DNA many times", "Translate genes into protein"],
       "Many leave 'sticky ends' that pair with any DNA cut by the same enzyme; DNA ligase then seals the joint.",
       "জিন প্রকৌশলে ইকোআরআই-এর মতো রেস্ট্রিকশন এনজাইম ব্যবহার হয়…", ["নির্দিষ্ট শনাক্তকরণ-ক্রমে ডিএনএ কাটতে", "ডিএনএ খণ্ড জুড়তে", "ডিএনএ বহুবার প্রতিলিপি করতে", "জিনকে প্রোটিনে অনুবাদ করতে"],
       "অনেকে 'আঠালো প্রান্ত' রাখে, যা একই এনজাইমে কাটা যেকোনো ডিএনএ-র সঙ্গে জোড় বাঁধে; তারপর ডিএনএ লাইগেজ জোড়টা আটকায়।"),
    _q("Why is Taq polymerase used in PCR?", ["It survives the high temperatures used to separate DNA strands", "It cuts DNA", "It works only at room temperature", "It makes RNA"],
       "It comes from Thermus aquaticus, a bacterium of hot springs, and is not destroyed at about 94°C.",
       "পিসিআর-এ ট্যাক পলিমারেজ কেন ব্যবহার হয়?", ["ডিএনএ সূত্র আলাদা করার উচ্চ তাপমাত্রায় এটা টিকে থাকে", "এটা ডিএনএ কাটে", "এটা কেবল ঘরের তাপমাত্রায় কাজ করে", "এটা আরএনএ তৈরি করে"],
       "এটা উষ্ণপ্রস্রবণের ব্যাকটেরিয়া থার্মাস অ্যাকোয়াটিকাস থেকে আসে, প্রায় 94°C-এও নষ্ট হয় না।"),
    _q("Bt cotton resists bollworms because it carries a gene from Bacillus thuringiensis that makes…", ["A Cry protein toxic to insect larvae", "An antibiotic", "A plant hormone", "A fungicide"],
       "The protoxin becomes active only in the alkaline gut of certain insects, so it is harmless to humans.",
       "বিটি তুলা বোলওয়ার্ম প্রতিরোধ করে কারণ এতে ব্যাসিলাস থুরিঞ্জিয়েনসিসের একটা জিন আছে, যা তৈরি করে…", ["পতঙ্গের লার্ভার পক্ষে বিষাক্ত ক্রাই প্রোটিন", "একটা অ্যান্টিবায়োটিক", "একটা উদ্ভিদ-হরমোন", "একটা ছত্রাকনাশক"],
       "প্রোটক্সিন কেবল কিছু পতঙ্গের ক্ষারীয় অন্ত্রে সক্রিয় হয়, তাই মানুষের ক্ষতি করে না।"),
    _q("Human insulin is now produced mainly by…", ["Recombinant DNA technology in bacteria or yeast", "Extracting it from pig pancreas only", "Chemical synthesis from glucose", "Plant extracts"],
       "Eli Lilly made the A and B chains in E. coli in 1983 and joined them by disulphide bonds.",
       "মানব ইনসুলিন এখন প্রধানত তৈরি হয়…", ["ব্যাকটেরিয়া বা ইস্টে রিকম্বিন্যান্ট ডিএনএ প্রযুক্তিতে", "কেবল শূকরের অগ্ন্যাশয় থেকে নিষ্কাশন করে", "গ্লুকোজ থেকে রাসায়নিক সংশ্লেষে", "উদ্ভিদের নির্যাস থেকে"],
       "1983-এ এলি লিলি ই. কোলাইতে A আর B শৃঙ্খল তৈরি করে ডাইসালফাইড বন্ধনে জুড়েছিল।"),
    _q("DNA fingerprinting is based on differences between people in…", ["Variable number tandem repeats (VNTRs)", "The genetic code", "The number of chromosomes", "The structure of ribosomes"],
       "These short repeated sequences vary in length from person to person, giving a unique band pattern.",
       "ডিএনএ ফিঙ্গারপ্রিন্টিং মানুষের মধ্যে কোন পার্থক্যের উপর ভিত্তি করে?", ["পরিবর্তনশীল সংখ্যার পরপর পুনরাবৃত্তি (ভিএনটিআর)", "জিনগত সংকেত", "ক্রোমোজোমের সংখ্যা", "রাইবোজোমের গঠন"],
       "এই ছোট পুনরাবৃত্ত ক্রমগুলোর দৈর্ঘ্য মানুষভেদে বদলায়, ফলে অনন্য পটি-নকশা তৈরি হয়।"),
    _q("In gel electrophoresis, DNA fragments move towards the anode because…", ["DNA is negatively charged", "DNA is positively charged", "Gravity pulls them", "They are attracted by the gel"],
       "The phosphate backbone carries negative charge; smaller fragments move faster through the gel.",
       "জেল ইলেকট্রোফোরেসিসে ডিএনএ খণ্ড অ্যানোডের দিকে যায় কারণ…", ["ডিএনএ ঋণাত্মক আধানযুক্ত", "ডিএনএ ধনাত্মক আধানযুক্ত", "অভিকর্ষ টানে", "জেল আকর্ষণ করে"],
       "ফসফেট মেরুদণ্ড ঋণাত্মক আধান বয়; ছোট খণ্ড জেলের মধ্য দিয়ে দ্রুত চলে।"),
    _q("Which gas is the main component of biogas?", ["Methane", "Hydrogen", "Carbon monoxide", "Oxygen"],
       "Methanogenic archaea in cattle dung digest organic matter without oxygen, giving 50-70% methane.",
       "বায়োগ্যাসের প্রধান উপাদান কোন গ্যাস?", ["মিথেন", "হাইড্রোজেন", "কার্বন মনোক্সাইড", "অক্সিজেন"],
       "গোবরের মিথেনোজেন আর্কিয়া অক্সিজেন ছাড়া জৈব পদার্থ পচিয়ে 50-70% মিথেন দেয়।"),
    _q("Penicillin was discovered from…", ["The mould Penicillium notatum", "A soil bacterium Streptomyces", "Human blood", "A virus"],
       "Fleming noticed in 1928 that the mould killed Staphylococcus colonies; Florey and Chain made it a medicine.",
       "পেনিসিলিন আবিষ্কৃত হয়েছিল…", ["ছত্রাক পেনিসিলিয়াম নোটাটাম থেকে", "মাটির ব্যাকটেরিয়া স্ট্রেপ্টোমাইসিস থেকে", "মানুষের রক্ত থেকে", "একটা ভাইরাস থেকে"],
       "1928-এ ফ্লেমিং দেখেন ছত্রাকটা স্ট্যাফাইলোকক্কাস কলোনি মেরে ফেলছে; ফ্লোরি আর চেইন একে ওষুধ বানান।"),
    _q("Ecological succession that starts on bare rock with no soil is called…", ["Primary succession", "Secondary succession", "Climax community", "Retrogression"],
       "Lichens are the pioneers; secondary succession starts where soil remains, such as on abandoned farmland.",
       "মাটিহীন খালি পাথরে শুরু হওয়া বাস্তুতান্ত্রিক অনুক্রমকে বলে…", ["প্রাথমিক অনুক্রম", "গৌণ অনুক্রম", "চূড়ান্ত সম্প্রদায়", "পশ্চাদ্গমন"],
       "লাইকেন পথিকৃৎ; গৌণ অনুক্রম শুরু হয় যেখানে মাটি থেকে যায়, যেমন পরিত্যক্ত খেতে।"),
    _q("Which ecological pyramid can never be inverted?", ["The pyramid of energy", "The pyramid of numbers", "The pyramid of biomass", "All of them can be inverted"],
       "Energy is lost at every transfer; a single tree with many insects inverts the number pyramid, and oceans invert biomass.",
       "কোন বাস্তুতান্ত্রিক পিরামিড কখনো উল্টো হতে পারে না?", ["শক্তির পিরামিড", "সংখ্যার পিরামিড", "জৈবভরের পিরামিড", "সবগুলোই উল্টো হতে পারে"],
       "প্রতিটি স্থানান্তরে শক্তি হারায়; একটা গাছে অনেক পোকা সংখ্যার পিরামিড উল্টায়, আর সমুদ্রে জৈবভরের পিরামিড উল্টো।"),
    _q("Which region of India is one of the world's biodiversity hotspots?", ["The Western Ghats", "The Thar Desert", "The Deccan plateau's centre", "The Gangetic plain"],
       "India shares four hotspots: the Western Ghats-Sri Lanka, the Himalaya, Indo-Burma and Sundaland.",
       "ভারতের কোন অঞ্চল বিশ্বের জীববৈচিত্র্য-হটস্পটগুলোর একটা?", ["পশ্চিমঘাট", "থর মরুভূমি", "দাক্ষিণাত্য মালভূমির কেন্দ্র", "গাঙ্গেয় সমভূমি"],
       "ভারতে চারটি হটস্পট আছে: পশ্চিমঘাট-শ্রীলঙ্কা, হিমালয়, ইন্দো-বর্মা আর সুন্দাল্যান্ড।"),
    _q("Excess nitrates and phosphates from farms entering a lake cause…", ["Eutrophication and algal blooms that use up oxygen", "Cleaner water", "Lower algal growth", "Higher dissolved oxygen at night"],
       "Dead algae decompose, raising the BOD; fish can die from lack of oxygen.",
       "খেত থেকে অতিরিক্ত নাইট্রেট আর ফসফেট হ্রদে ঢুকলে ঘটে…", ["সুপুষ্টিভবন আর শৈবাল-বিস্ফোরণ, যা অক্সিজেন ফুরিয়ে দেয়", "পরিষ্কার জল", "শৈবালের বৃদ্ধি কম", "রাতে দ্রবীভূত অক্সিজেন বেশি"],
       "মরা শৈবাল পচে জৈব-রাসায়নিক অক্সিজেন চাহিদা বাড়ায়; অক্সিজেনের অভাবে মাছ মরতে পারে।"),
    _q("Which kind of interaction benefits one species and leaves the other unaffected?", ["Commensalism", "Mutualism", "Parasitism", "Competition"],
       "An orchid growing on a mango branch gets light and support; the tree is neither helped nor harmed.",
       "কোন ধরনের পারস্পরিক ক্রিয়ায় একটা প্রজাতি উপকৃত হয় আর অন্যটা অপ্রভাবিত থাকে?", ["সহভোজিতা (কমেনসালিজম)", "মিথোজীবিতা", "পরজীবিতা", "প্রতিযোগিতা"],
       "আমের ডালে জন্মানো অর্কিড আলো আর আশ্রয় পায়; গাছটা উপকৃত বা ক্ষতিগ্রস্ত হয় না।"),
    _q("Gause's competitive exclusion principle states that…", ["Two species competing for exactly the same resources cannot coexist indefinitely", "All species can share any niche", "Predators always win", "Competition increases both populations"],
       "One species eventually wins unless they divide the resource (resource partitioning).",
       "গসের প্রতিযোগিতামূলক বর্জন নীতি বলে যে…", ["ঠিক একই সম্পদের জন্য প্রতিযোগী দুটো প্রজাতি অনির্দিষ্টকাল সহাবস্থান করতে পারে না", "সব প্রজাতি যেকোনো নিশ ভাগ করতে পারে", "শিকারি সবসময় জেতে", "প্রতিযোগিতা দুই জনসংখ্যাই বাড়ায়"],
       "সম্পদ ভাগাভাগি (রিসোর্স পার্টিশনিং) না করলে শেষে একটা প্রজাতি জেতে।"),
    _q("A population growing with limited resources follows which curve?", ["Logistic, S-shaped, levelling off at the carrying capacity K", "Exponential, J-shaped forever", "A straight falling line", "A random zig-zag"],
       "dN/dt = rN(K - N)/K: growth slows as N approaches K.",
       "সীমিত সম্পদে বাড়তে থাকা জনসংখ্যা কোন রেখা অনুসরণ করে?", ["লজিস্টিক, S-আকৃতি, ধারণক্ষমতা K-তে গিয়ে স্থির", "সূচকীয়, চিরকাল J-আকৃতি", "সোজা নেমে যাওয়া রেখা", "এলোমেলো আঁকাবাঁকা"],
       "dN/dt = rN(K - N)/K: N যত K-এর কাছে যায়, বৃদ্ধি তত কমে।"),
    _q("Which enzyme in saliva begins the digestion of starch?", ["Salivary amylase (ptyalin)", "Pepsin", "Lipase", "Trypsin"],
       "It breaks starch into maltose at a near-neutral pH; stomach acid stops it.",
       "লালার কোন এনজাইম শ্বেতসারের পরিপাক শুরু করে?", ["লালা-অ্যামাইলেজ (টায়ালিন)", "পেপসিন", "লাইপেজ", "ট্রিপসিন"],
       "প্রায় নিরপেক্ষ pH-এ এটা শ্বেতসারকে মলটোজে ভাঙে; পাকস্থলীর অ্যাসিড তা থামায়।"),
    _q("Bile from the liver helps digestion by…", ["Emulsifying fats into small droplets", "Digesting proteins", "Absorbing glucose", "Killing all bacteria"],
       "Bile salts increase the surface area for pancreatic lipase; bile contains no digestive enzymes.",
       "যকৃতের পিত্ত পরিপাকে সাহায্য করে…", ["চর্বিকে ছোট ফোঁটায় অবদ্রবণ করে", "প্রোটিন পরিপাক করে", "গ্লুকোজ শোষণ করে", "সব ব্যাকটেরিয়া মেরে"],
       "পিত্ত-লবণ অগ্ন্যাশয়ের লাইপেজের জন্য তলের ক্ষেত্রফল বাড়ায়; পিত্তে কোনো পাচক এনজাইম নেই।"),
    _q("Which vitamin deficiency causes night blindness?", ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin K"],
       "Vitamin A forms retinal, part of the rod pigment rhodopsin needed for dim-light vision.",
       "কোন ভিটামিনের অভাবে রাতকানা হয়?", ["ভিটামিন A", "ভিটামিন C", "ভিটামিন D", "ভিটামিন K"],
       "ভিটামিন A থেকে রেটিনাল তৈরি হয়, যা ক্ষীণ আলোয় দেখার জন্য রড-রঞ্জক রোডপসিনের অংশ।"),
    _q("An enzyme's activity drops when a molecule resembling its substrate occupies the active site. This is…", ["Competitive inhibition", "Non-competitive inhibition", "Denaturation", "Allosteric activation"],
       "Adding more substrate can overcome it; malonate inhibiting succinate dehydrogenase is the classic case.",
       "সাবস্ট্রেটের মতো দেখতে একটা অণু সক্রিয় স্থান দখল করলে এনজাইমের কার্যকারিতা কমে। এটা…", ["প্রতিযোগিতামূলক বাধা", "অপ্রতিযোগিতামূলক বাধা", "বিকৃতকরণ", "অ্যালোস্টেরিক সক্রিয়করণ"],
       "বেশি সাবস্ট্রেট দিলে এটা কাটানো যায়; ম্যালোনেট দিয়ে সাকসিনেট ডিহাইড্রোজিনেজের বাধা প্রমাণ উদাহরণ।"),
    _q("At which stage of mitosis do chromosomes line up at the cell's equator?", ["Metaphase", "Prophase", "Anaphase", "Telophase"],
       "Spindle fibres attach to kinetochores; chromosomes are easiest to count at this stage.",
       "মাইটোসিসের কোন দশায় ক্রোমোজোমগুলো কোষের বিষুবীয় তলে সারিবদ্ধ হয়?", ["মেটাফেজ", "প্রোফেজ", "অ্যানাফেজ", "টেলোফেজ"],
       "বেম-তন্তু কাইনেটোকোরে যুক্ত হয়; এই দশায় ক্রোমোজোম গোনা সবচেয়ে সহজ।"),
    _q("Crossing over between homologous chromosomes happens during…", ["Pachytene of prophase I of meiosis", "Metaphase of mitosis", "Anaphase II of meiosis", "Interphase"],
       "Paired homologues exchange segments at chiasmata, creating new allele combinations.",
       "সমসংস্থ ক্রোমোজোমের মধ্যে ক্রসিং ওভার ঘটে…", ["মিয়োসিসের প্রোফেজ I-এর প্যাকাইটিন দশায়", "মাইটোসিসের মেটাফেজে", "মিয়োসিসের অ্যানাফেজ II-তে", "ইন্টারফেজে"],
       "জোড়বদ্ধ সমসংস্থরা কায়াজমায় অংশ বিনিময় করে, নতুন অ্যালিল-সমন্বয় তৈরি হয়।"),
    _q("Which organelle is called the 'suicide bag' of the cell?", ["Lysosome", "Golgi body", "Ribosome", "Centriole"],
       "It holds hydrolytic enzymes that can digest worn-out parts - or the whole cell if it bursts.",
       "কোন অঙ্গাণুকে কোষের 'আত্মঘাতী থলি' বলা হয়?", ["লাইসোজোম", "গলগি বস্তু", "রাইবোজোম", "সেন্ট্রিওল"],
       "এতে আর্দ্রবিশ্লেষী এনজাইম থাকে, যা জীর্ণ অংশ - বা ফেটে গেলে পুরো কোষ - পরিপাক করতে পারে।"),
    _q("Which organelles contain their own circular DNA and 70S ribosomes, supporting the endosymbiotic theory?", ["Mitochondria and chloroplasts", "Golgi bodies and lysosomes", "Nucleus and nucleolus", "Vacuoles and peroxisomes"],
       "They resemble bacteria and divide by fission, suggesting they were once free-living prokaryotes.",
       "কোন অঙ্গাণুগুলোর নিজস্ব বৃত্তাকার ডিএনএ আর 70S রাইবোজোম আছে, যা অন্তঃমিথোজীবী তত্ত্বকে সমর্থন করে?", ["মাইটোকন্ড্রিয়া আর ক্লোরোপ্লাস্ট", "গলগি বস্তু আর লাইসোজোম", "নিউক্লিয়াস আর নিউক্লিওলাস", "কোষগহ্বর আর পারঅক্সিজোম"],
       "এরা ব্যাকটেরিয়ার মতো আর বিভাজনে সংখ্যা বাড়ায়, অর্থাৎ একসময় মুক্তজীবী আদিকোষী ছিল।"),
    _q("The fluid mosaic model describes the cell membrane as…", ["A phospholipid bilayer with proteins that can move within it", "A rigid protein sheet", "A single layer of cholesterol", "A layer of cellulose"],
       "Singer and Nicolson (1972): proteins float like icebergs in a sea of lipid.",
       "তরল মোজাইক মডেল কোষপর্দাকে বর্ণনা করে…", ["ফসফোলিপিডের দ্বিস্তর হিসেবে, যার মধ্যে প্রোটিন চলাফেরা করতে পারে", "শক্ত প্রোটিন পাত হিসেবে", "কোলেস্টেরলের একক স্তর হিসেবে", "সেলুলোজের স্তর হিসেবে"],
       "সিঙ্গার আর নিকলসন (1972): লিপিডের সমুদ্রে প্রোটিন হিমশৈলের মতো ভাসে।"),
    _q("Glucose enters many cells down its concentration gradient through carrier proteins without using ATP. This is…", ["Facilitated diffusion", "Active transport", "Osmosis", "Endocytosis"],
       "Carriers speed up diffusion; active transport, such as the Na⁺/K⁺ pump, moves substances against the gradient using ATP.",
       "অনেক কোষে গ্লুকোজ এটিপি ছাড়াই বাহক প্রোটিন দিয়ে ঘনত্ব-ঢাল বরাবর ঢোকে। এটা…", ["সহজ ব্যাপন", "সক্রিয় পরিবহন", "অভিস্রবণ", "এন্ডোসাইটোসিস"],
       "বাহক ব্যাপনকে দ্রুত করে; Na⁺/K⁺ পাম্পের মতো সক্রিয় পরিবহন এটিপি খরচ করে ঢালের বিপরীতে বস্তু সরায়।"),
    _q("Which class of animals has a four-chambered heart and is warm-blooded but lays eggs?", ["Birds", "Reptiles", "Amphibians", "Fishes"],
       "Birds and mammals are endothermic with fully separated circulations; crocodiles also have four chambers but are cold-blooded.",
       "কোন শ্রেণির প্রাণীর চার-প্রকোষ্ঠ হৃৎপিণ্ড, উষ্ণশোণিত অথচ ডিম পাড়ে?", ["পাখি", "সরীসৃপ", "উভচর", "মাছ"],
       "পাখি আর স্তন্যপায়ী সম্পূর্ণ পৃথক সংবহনসহ উষ্ণশোণিত; কুমিরেরও চার প্রকোষ্ঠ, কিন্তু শীতলশোণিত।"),
    _q("Which kingdom in Whittaker's five-kingdom system contains unicellular eukaryotes such as Amoeba and Euglena?", ["Protista", "Monera", "Fungi", "Plantae"],
       "Monera holds the prokaryotes (bacteria); Fungi, Plantae and Animalia are multicellular eukaryotes.",
       "হুইটেকারের পাঁচ-রাজ্য ব্যবস্থায় অ্যামিবা আর ইউগ্লিনার মতো এককোষী প্রকৃতকোষীরা কোন রাজ্যে?", ["প্রোটিস্টা", "মনেরা", "ছত্রাক", "উদ্ভিদ"],
       "মনেরায় আদিকোষীরা (ব্যাকটেরিয়া); ছত্রাক, উদ্ভিদ আর প্রাণী রাজ্য বহুকোষী প্রকৃতকোষী।"),
    _q("Which statement about viruses is correct?", ["They can reproduce only inside living host cells", "They have both DNA and RNA always", "They respire like bacteria", "They are killed by antibiotics"],
       "Outside a cell a virus is an inert particle; antibiotics target bacterial structures that viruses lack.",
       "ভাইরাস সম্পর্কে কোন বিবৃতি সঠিক?", ["তারা কেবল জীবিত পোষক কোষের ভেতরে বংশবৃদ্ধি করতে পারে", "তাদের সবসময় ডিএনএ আর আরএনএ দুটোই থাকে", "তারা ব্যাকটেরিয়ার মতো শ্বসন করে", "অ্যান্টিবায়োটিক তাদের মারে"],
       "কোষের বাইরে ভাইরাস একটা নিষ্ক্রিয় কণা; অ্যান্টিবায়োটিক ব্যাকটেরিয়ার যে গঠনকে লক্ষ্য করে, ভাইরাসে তা নেই।"),
    _q("In-vitro fertilisation (IVF) means…", ["Fertilisation outside the body, followed by embryo transfer", "Artificial insemination into the uterus", "Cloning from a body cell", "Gene therapy of the egg"],
       "The embryo is placed in the uterus (or the zygote in the fallopian tube, ZIFT) to develop normally.",
       "ইন-ভিট্রো নিষেক (আইভিএফ) মানে…", ["দেহের বাইরে নিষেক, তারপর ভ্রূণ স্থানান্তর", "জরায়ুতে কৃত্রিম গর্ভাধান", "দেহকোষ থেকে ক্লোনিং", "ডিম্বাণুর জিন থেরাপি"],
       "ভ্রূণকে জরায়ুতে (বা জাইগোটকে ডিম্বনালিতে, জিআইএফটি) রাখা হয় যাতে স্বাভাবিকভাবে বাড়ে।"),
    _q("Which hormone from the pancreas raises blood glucose between meals?", ["Glucagon", "Insulin", "Somatostatin only", "Secretin"],
       "Glucagon from α cells makes the liver break down glycogen; insulin from β cells lowers blood glucose.",
       "অগ্ন্যাশয়ের কোন হরমোন দুই খাবারের মাঝে রক্তে গ্লুকোজ বাড়ায়?", ["গ্লুকাগন", "ইনসুলিন", "কেবল সোমাটোস্ট্যাটিন", "সিক্রেটিন"],
       "α কোষের গ্লুকাগন যকৃৎকে গ্লাইকোজেন ভাঙায়; β কোষের ইনসুলিন রক্তে গ্লুকোজ কমায়।"),
    _q("Which gland is called the 'master gland' because it controls several other endocrine glands?", ["The pituitary", "The thyroid", "The adrenal", "The pineal"],
       "Its own secretion is in turn controlled by releasing hormones from the hypothalamus.",
       "কোন গ্রন্থি অন্য কয়েকটা অন্তঃক্ষরা গ্রন্থিকে নিয়ন্ত্রণ করে বলে 'প্রধান গ্রন্থি' নামে পরিচিত?", ["পিটুইটারি", "থাইরয়েড", "অ্যাড্রিনাল", "পিনিয়াল"],
       "এর নিজের ক্ষরণ আবার হাইপোথ্যালামাসের রিলিজিং হরমোন দিয়ে নিয়ন্ত্রিত।"),
    _q("Iodine deficiency in the diet commonly causes…", ["Goitre, an enlarged thyroid", "Rickets", "Scurvy", "Night blindness"],
       "Without iodine the thyroid cannot make thyroxine; TSH keeps stimulating it and it swells. Iodised salt prevents it.",
       "খাদ্যে আয়োডিনের অভাবে সাধারণত হয়…", ["গলগণ্ড, থাইরয়েড বড় হয়ে যাওয়া", "রিকেটস", "স্কার্ভি", "রাতকানা"],
       "আয়োডিন ছাড়া থাইরয়েড থাইরক্সিন তৈরি করতে পারে না; টিএসএইচ উদ্দীপিত করতে থাকে আর গ্রন্থি ফোলে। আয়োডিনযুক্ত লবণ এটা আটকায়।"),
    _q("What is the main role of the ozone layer in the stratosphere?", ["It absorbs harmful ultraviolet-B radiation", "It traps heat to warm the Earth", "It produces oxygen for breathing", "It blocks visible light"],
       "Thinning ozone raises the risk of skin cancer and cataracts; the Montreal Protocol phased out CFCs.",
       "স্ট্র্যাটোস্ফিয়ারে ওজোন স্তরের প্রধান ভূমিকা কী?", ["ক্ষতিকর অতিবেগুনি-বি বিকিরণ শোষণ করা", "তাপ আটকে পৃথিবীকে গরম রাখা", "শ্বাসের জন্য অক্সিজেন তৈরি করা", "দৃশ্যমান আলো আটকানো"],
       "ওজোন পাতলা হলে ত্বকের ক্যান্সার আর ছানির ঝুঁকি বাড়ে; মন্ট্রিয়াল প্রোটোকল সিএফসি তুলে দিয়েছে।"),
    _q("Which group of organisms fixes atmospheric nitrogen in rice paddies?", ["Cyanobacteria such as Anabaena", "Mushrooms", "Mosses", "Protozoa"],
       "They are used as biofertilisers; Anabaena also lives inside the water fern Azolla.",
       "ধানখেতে কোন জীবগোষ্ঠী বায়ুর নাইট্রোজেন আবদ্ধ করে?", ["অ্যানাবিনার মতো সায়ানোব্যাকটেরিয়া", "ব্যাঙের ছাতা", "মস", "প্রোটোজোয়া"],
       "এরা জৈবসার হিসেবে ব্যবহৃত হয়; অ্যানাবিনা জলজ ফার্ন অ্যাজোলার ভেতরেও থাকে।"),
    _q("Which blood cells are the first to arrive at a site of infection and engulf bacteria?", ["Neutrophils", "Red blood cells", "Platelets", "Basophils"],
       "Neutrophils are the most common white cells; pus is largely dead neutrophils and bacteria.",
       "কোন রক্তকোষ সংক্রমণের জায়গায় প্রথমে পৌঁছে ব্যাকটেরিয়া গ্রাস করে?", ["নিউট্রোফিল", "লোহিত রক্তকণিকা", "অণুচক্রিকা", "বেসোফিল"],
       "নিউট্রোফিল সবচেয়ে সাধারণ শ্বেতকণিকা; পুঁজ প্রধানত মরা নিউট্রোফিল আর ব্যাকটেরিয়া।"),
    _q("A person of blood group O is called a 'universal donor' because their red cells…", ["Carry neither A nor B antigens", "Carry both A and B antigens", "Have no haemoglobin", "Have extra antibodies"],
       "Recipients' anti-A and anti-B antibodies have nothing to attack; AB people are universal recipients.",
       "O রক্তের গ্রুপের মানুষকে 'সর্বজনীন দাতা' বলা হয় কারণ তাদের লোহিত কণিকায়…", ["A বা B কোনো অ্যান্টিজেন নেই", "A আর B দুটো অ্যান্টিজেনই আছে", "হিমোগ্লোবিন নেই", "বাড়তি অ্যান্টিবডি আছে"],
       "গ্রহীতার অ্যান্টি-A আর অ্যান্টি-B অ্যান্টিবডির আক্রমণ করার কিছু থাকে না; AB মানুষ সর্বজনীন গ্রহীতা।"),
    _q("Erythroblastosis foetalis can occur when…", ["An Rh-negative mother carries a second Rh-positive baby", "Both parents are Rh-negative", "The mother is Rh-positive", "The baby is Rh-negative"],
       "Antibodies made after the first birth cross the placenta and destroy the baby's red cells; anti-D injections prevent it.",
       "এরিথ্রোব্লাস্টোসিস ফিটালিস ঘটতে পারে যখন…", ["আরএইচ-নেগেটিভ মা দ্বিতীয়বার আরএইচ-পজিটিভ শিশু গর্ভে ধারণ করেন", "বাবা-মা দুজনেই আরএইচ-নেগেটিভ", "মা আরএইচ-পজিটিভ", "শিশু আরএইচ-নেগেটিভ"],
       "প্রথম প্রসবের পর তৈরি অ্যান্টিবডি অমরা পেরিয়ে শিশুর লোহিত কণিকা ধ্বংস করে; অ্যান্টি-ডি ইনজেকশন তা আটকায়।"),
    _q("Which part of the brain coordinates balance and fine movements?", ["Cerebellum", "Medulla oblongata", "Hypothalamus", "Corpus callosum"],
       "The medulla controls breathing and heartbeat; the hypothalamus controls temperature, hunger and thirst.",
       "মস্তিষ্কের কোন অংশ ভারসাম্য আর সূক্ষ্ম নড়াচড়া সমন্বয় করে?", ["লঘুমস্তিষ্ক (সেরিবেলাম)", "সুষুম্নাশীর্ষক (মেডুলা)", "হাইপোথ্যালামাস", "কর্পাস ক্যালোসাম"],
       "মেডুলা শ্বাস আর হৃৎস্পন্দন নিয়ন্ত্রণ করে; হাইপোথ্যালামাস তাপমাত্রা, খিদে আর তেষ্টা নিয়ন্ত্রণ করে।"),
    _q("In the eye, which cells are responsible for colour vision?", ["Cones", "Rods", "Bipolar cells only", "Iris cells"],
       "Three kinds of cones respond to red, green and blue light; rods work in dim light and see only shades of grey.",
       "চোখে কোন কোষ রঙিন দৃষ্টির জন্য দায়ী?", ["কোন (শঙ্কু) কোষ", "রড (দণ্ড) কোষ", "কেবল বাইপোলার কোষ", "আইরিস কোষ"],
       "তিন রকম শঙ্কু কোষ লাল, সবুজ আর নীল আলোয় সাড়া দেয়; দণ্ড কোষ ক্ষীণ আলোয় কাজ করে, কেবল ধূসর দেখে।"),
    _q("Which part of a flower develops into the fruit after fertilisation?", ["The ovary", "The ovule", "The anther", "The petal"],
       "The ovules become seeds; fruits that develop without fertilisation (parthenocarpy) are seedless, like bananas.",
       "নিষেকের পর ফুলের কোন অংশ ফলে পরিণত হয়?", ["গর্ভাশয়", "ডিম্বক", "পরাগধানী", "পাপড়ি"],
       "ডিম্বকগুলো বীজ হয়; নিষেক ছাড়া তৈরি ফল (পার্থেনোকার্পি) বীজহীন, যেমন কলা।"),
    _q("Which part of a neuron receives signals from other neurons?", ["Dendrites", "The axon terminal", "The myelin sheath", "The node of Ranvier"],
       "Signals travel dendrites → cell body → axon → axon terminals, where neurotransmitters cross the synapse.",
       "নিউরনের কোন অংশ অন্য নিউরনের সংকেত গ্রহণ করে?", ["ডেনড্রাইট", "অ্যাক্সন প্রান্ত", "মায়েলিন আবরণ", "র‍্যানভিয়ারের পর্ব"],
       "সংকেত চলে ডেনড্রাইট → কোষদেহ → অ্যাক্সন → অ্যাক্সন প্রান্ত, যেখানে নিউরোট্রান্সমিটার সিন্যাপস পেরোয়।"),
    _q("A reflex action such as pulling a hand away from a flame is coordinated by…", ["The spinal cord", "The cerebrum alone", "The cerebellum", "The pituitary gland"],
       "The reflex arc (receptor → sensory neuron → spinal cord → motor neuron → muscle) skips the brain for speed.",
       "আগুন থেকে হাত সরিয়ে নেওয়ার মতো প্রতিবর্ত ক্রিয়া কে সমন্বয় করে?", ["সুষুম্নাকাণ্ড", "কেবল গুরুমস্তিষ্ক", "লঘুমস্তিষ্ক", "পিটুইটারি গ্রন্থি"],
       "প্রতিবর্ত চাপ (গ্রাহক → সংবেদী নিউরন → সুষুম্নাকাণ্ড → আজ্ঞাবহ নিউরন → পেশি) দ্রুততার জন্য মস্তিষ্ককে এড়িয়ে যায়।"),
    _q("Which hormone from the adrenal medulla prepares the body for 'fight or flight'?", ["Adrenaline", "Cortisol", "Aldosterone", "Melatonin"],
       "It raises heart rate, blood glucose and blood flow to muscles within seconds.",
       "অ্যাড্রিনাল মেডুলার কোন হরমোন দেহকে 'লড়াই বা পালাও'-এর জন্য তৈরি করে?", ["অ্যাড্রিনালিন", "কর্টিসল", "অ্যালডোস্টেরন", "মেলাটোনিন"],
       "এটা কয়েক সেকেন্ডে হৃৎস্পন্দন, রক্তে গ্লুকোজ আর পেশিতে রক্তপ্রবাহ বাড়ায়।"),
    _q("Which hormone keeps the uterine lining ready for pregnancy after ovulation?", ["Progesterone", "FSH", "Oxytocin", "Relaxin only"],
       "It is made by the corpus luteum; when it falls, the lining breaks down and menstruation begins.",
       "ডিম্বস্ফোটনের পর কোন হরমোন জরায়ুর আস্তরণকে গর্ভধারণের জন্য প্রস্তুত রাখে?", ["প্রোজেস্টেরন", "এফএসএইচ", "অক্সিটোসিন", "কেবল রিলাক্সিন"],
       "কর্পাস লুটিয়াম এটা তৈরি করে; এর মাত্রা কমলে আস্তরণ ভেঙে ঋতুস্রাব শুরু হয়।"),
    _q("Which structure in the testes secretes testosterone?", ["Leydig (interstitial) cells", "Sertoli cells", "The epididymis", "The vas deferens"],
       "Sertoli cells nourish developing sperm; the epididymis stores and matures them.",
       "শুক্রাশয়ের কোন গঠন টেস্টোস্টেরন ক্ষরণ করে?", ["লেডিগ (অন্তর্বর্তী) কোষ", "সার্টোলি কোষ", "এপিডিডাইমিস", "শুক্রনালি"],
       "সার্টোলি কোষ বিকাশমান শুক্রাণুকে পুষ্টি দেয়; এপিডিডাইমিস তাদের জমিয়ে পরিণত করে।"),
    _q("Which type of RNA carries amino acids to the ribosome?", ["Transfer RNA (tRNA)", "Messenger RNA (mRNA)", "Ribosomal RNA (rRNA)", "Small nuclear RNA"],
       "Each tRNA has an anticodon that pairs with a codon on the mRNA.",
       "কোন ধরনের আরএনএ রাইবোজোমে অ্যামিনো অ্যাসিড বয়ে আনে?", ["ট্রান্সফার আরএনএ (টি-আরএনএ)", "মেসেঞ্জার আরএনএ (এম-আরএনএ)", "রাইবোজোমাল আরএনএ (আর-আরএনএ)", "ক্ষুদ্র নিউক্লীয় আরএনএ"],
       "প্রতিটি টি-আরএনএ-র একটা অ্যান্টিকোডন থাকে, যা এম-আরএনএ-র কোডনের সঙ্গে জোড় বাঁধে।"),
    _q("Reverse transcriptase, found in retroviruses such as HIV, makes…", ["DNA from an RNA template", "RNA from a DNA template", "Protein from RNA", "RNA from protein"],
       "It reverses the usual flow of the central dogma; scientists use it to make cDNA from mRNA.",
       "এইচআইভির মতো রেট্রোভাইরাসে থাকা রিভার্স ট্রান্সক্রিপটেজ তৈরি করে…", ["আরএনএ ছাঁচ থেকে ডিএনএ", "ডিএনএ ছাঁচ থেকে আরএনএ", "আরএনএ থেকে প্রোটিন", "প্রোটিন থেকে আরএনএ"],
       "এটা কেন্দ্রীয় মতবাদের স্বাভাবিক প্রবাহ উল্টে দেয়; বিজ্ঞানীরা এম-আরএনএ থেকে সি-ডিএনএ তৈরিতে এটা ব্যবহার করেন।"),
    _q("Plasmids are useful vectors in genetic engineering because they…", ["Replicate independently inside bacteria and can carry foreign genes", "Are found only in the nucleus of plants", "Cannot be cut by enzymes", "Never enter bacteria"],
       "Good vectors also have an origin of replication, selectable markers such as antibiotic-resistance genes, and cloning sites.",
       "জিন প্রকৌশলে প্লাজমিড কার্যকর বাহক কারণ তারা…", ["ব্যাকটেরিয়ার ভেতরে স্বাধীনভাবে প্রতিলিপি হয় আর বাইরের জিন বইতে পারে", "কেবল উদ্ভিদের নিউক্লিয়াসে থাকে", "এনজাইম দিয়ে কাটা যায় না", "কখনো ব্যাকটেরিয়ায় ঢোকে না"],
       "ভালো বাহকে প্রতিলিপি-সূচনাস্থল, অ্যান্টিবায়োটিক-প্রতিরোধী জিনের মতো নির্বাচনী চিহ্নক আর ক্লোনিং-স্থান থাকে।"),
    _q("Golden rice was engineered to fight…", ["Vitamin A deficiency", "Iron deficiency anaemia", "Protein deficiency", "Iodine deficiency"],
       "It makes β-carotene, the precursor of vitamin A, in its grain.",
       "গোল্ডেন রাইস কীসের বিরুদ্ধে লড়তে তৈরি করা হয়েছিল?", ["ভিটামিন A-র অভাব", "লোহার অভাবজনিত রক্তাল্পতা", "প্রোটিনের অভাব", "আয়োডিনের অভাব"],
       "এর দানায় β-ক্যারোটিন তৈরি হয়, যা ভিটামিন A-র পূর্বসূরি।"),
    _q("ELISA tests detect infections by using…", ["Antigen-antibody reactions linked to an enzyme colour change", "DNA sequencing only", "Light microscopy", "Blood pressure readings"],
       "It can detect HIV antibodies or viral antigens even before symptoms appear.",
       "এলাইজা পরীক্ষা কী ব্যবহার করে সংক্রমণ শনাক্ত করে?", ["এনজাইমজনিত রং-পরিবর্তনের সঙ্গে যুক্ত অ্যান্টিজেন-অ্যান্টিবডি বিক্রিয়া", "কেবল ডিএনএ ক্রম নির্ণয়", "আলোক অণুবীক্ষণ", "রক্তচাপের পাঠ"],
       "উপসর্গ দেখা দেওয়ার আগেই এটা এইচআইভি অ্যান্টিবডি বা ভাইরাসের অ্যান্টিজেন ধরতে পারে।"),
    _q("Which of these is an example of ex-situ conservation?", ["A seed bank or botanical garden", "A national park", "A biosphere reserve", "A sacred grove"],
       "Ex-situ means outside the natural habitat; national parks and sanctuaries protect species in place (in-situ).",
       "এগুলোর মধ্যে কোনটা বহিঃস্থানিক (এক্স-সিটু) সংরক্ষণের উদাহরণ?", ["বীজভান্ডার বা উদ্ভিদ-উদ্যান", "জাতীয় উদ্যান", "জীবমণ্ডল সংরক্ষিত অঞ্চল", "পবিত্র বন"],
       "বহিঃস্থানিক মানে প্রাকৃতিক আবাসের বাইরে; জাতীয় উদ্যান আর অভয়ারণ্য প্রজাতিকে নিজের জায়গায় রক্ষা করে।"),
    _q("The 'evil quartet' of causes of biodiversity loss includes habitat loss, over-exploitation, alien species invasion and…", ["Co-extinction", "Afforestation", "Seed banking", "Crop rotation"],
       "When a host goes extinct, its specialised parasites and partners vanish with it.",
       "জীববৈচিত্র্য হ্রাসের 'চার খলনায়ক'-এর মধ্যে আছে আবাস হারানো, অতি-আহরণ, বহিরাগত প্রজাতির আগ্রাসন আর…", ["সহ-বিলুপ্তি", "বনসৃজন", "বীজ সংরক্ষণ", "শস্যাবর্তন"],
       "একটা পোষক বিলুপ্ত হলে তার বিশেষায়িত পরজীবী আর সঙ্গীরাও হারিয়ে যায়।"),
    _q("Which greenhouse gas is released in large amounts by rice paddies and cattle?", ["Methane", "Nitrogen", "Oxygen", "Argon"],
       "Methane traps much more heat per molecule than CO₂, though it stays in the air for less time.",
       "ধানখেত আর গবাদি পশু কোন গ্রিনহাউস গ্যাস প্রচুর পরিমাণে ছাড়ে?", ["মিথেন", "নাইট্রোজেন", "অক্সিজেন", "আর্গন"],
       "অণুপ্রতি মিথেন CO₂-এর চেয়ে অনেক বেশি তাপ আটকায়, যদিও বাতাসে কম সময় থাকে।"),
    _q("Biomagnification means that a persistent pollutant such as DDT…", ["Becomes more concentrated at each higher trophic level", "Breaks down quickly in water", "Is found only in plants", "Becomes less toxic over time"],
       "Fish-eating birds had DDT levels millions of times higher than the water, making their eggshells thin.",
       "জৈব-বিবর্ধন মানে ডিডিটির মতো একটা স্থায়ী দূষক…", ["প্রতিটি উচ্চতর পুষ্টিস্তরে আরও ঘনীভূত হয়", "জলে দ্রুত ভেঙে যায়", "কেবল উদ্ভিদে পাওয়া যায়", "সময়ের সঙ্গে কম বিষাক্ত হয়"],
       "মাছখেকো পাখিতে ডিডিটির মাত্রা জলের চেয়ে লক্ষ লক্ষ গুণ বেশি ছিল, তাদের ডিমের খোলা পাতলা হয়েছিল।"),
    _q("Which tissue is responsible for increasing the girth (secondary growth) of a dicot stem?", ["The vascular cambium", "The apical meristem", "The epidermis", "The pith"],
       "Cambium adds xylem inside and phloem outside; the yearly layers of xylem form annual rings.",
       "দ্বিবীজপত্রী কাণ্ডের বেড় বৃদ্ধির (গৌণ বৃদ্ধি) জন্য কোন কলা দায়ী?", ["সংবহন ক্যাম্বিয়াম", "অগ্রস্থ ভাজক কলা", "ত্বক", "মজ্জা"],
       "ক্যাম্বিয়াম ভেতরে জাইলেম আর বাইরে ফ্লোয়েম যোগ করে; জাইলেমের বার্ষিক স্তর বর্ষবলয় তৈরি করে।"),
    _q("Stomata open when guard cells…", ["Take in water and become turgid", "Lose water and become flaccid", "Die", "Fill with starch"],
       "K⁺ ions flow in, water follows by osmosis, and the thick inner walls make the cells curve apart.",
       "পত্ররন্ধ্র খোলে যখন রক্ষীকোষ…", ["জল নিয়ে স্ফীত হয়", "জল হারিয়ে শিথিল হয়", "মরে যায়", "শ্বেতসারে ভরে যায়"],
       "K⁺ আয়ন ঢোকে, অভিস্রবণে জল আসে, আর পুরু ভেতরের প্রাচীর কোষ দুটোকে বাঁকিয়ে আলাদা করে।"),
    _q("Which pigment is the main photosynthetic pigment in green plants?", ["Chlorophyll a", "Carotene", "Xanthophyll", "Anthocyanin"],
       "Chlorophyll a forms the reaction centres of both photosystems; the others are accessory pigments.",
       "সবুজ উদ্ভিদের প্রধান সালোকসংশ্লেষী রঞ্জক কোনটা?", ["ক্লোরোফিল a", "ক্যারোটিন", "জ্যান্থোফিল", "অ্যান্থোসায়ানিন"],
       "ক্লোরোফিল a দুই ফটোসিস্টেমেরই বিক্রিয়াকেন্দ্র গড়ে; বাকিরা সহায়ক রঞ্জক।"),
    _q("Which statement about anaerobic respiration in human muscles is correct?", ["Pyruvate is turned into lactic acid when oxygen runs short", "It produces ethanol", "It gives more ATP than aerobic respiration", "It happens in the mitochondria"],
       "It gives only 2 ATP per glucose; yeast instead makes ethanol and CO₂.",
       "মানুষের পেশিতে অবাত শ্বসন সম্পর্কে কোন বিবৃতি সঠিক?", ["অক্সিজেন কম পড়লে পাইরুভেট ল্যাকটিক অ্যাসিডে পরিণত হয়", "এতে ইথানল তৈরি হয়", "এটা সবাত শ্বসনের চেয়ে বেশি এটিপি দেয়", "এটা মাইটোকন্ড্রিয়ায় ঘটে"],
       "এতে গ্লুকোজপ্রতি মাত্র 2টি এটিপি; ইস্ট বরং ইথানল আর CO₂ তৈরি করে।"),
    _q("Which component of blood is mainly responsible for clotting?", ["Platelets with fibrinogen", "Red blood cells", "Lymphocytes", "Albumin only"],
       "Platelets release factors that turn prothrombin into thrombin, which turns fibrinogen into a fibrin mesh.",
       "রক্তের কোন উপাদান প্রধানত রক্ত তঞ্চনের জন্য দায়ী?", ["ফাইব্রিনোজেনসহ অণুচক্রিকা", "লোহিত রক্তকণিকা", "লিম্ফোসাইট", "কেবল অ্যালবুমিন"],
       "অণুচক্রিকা এমন উপাদান ছাড়ে যা প্রোথ্রম্বিনকে থ্রম্বিনে, আর থ্রম্বিন ফাইব্রিনোজেনকে ফাইব্রিন-জালে পরিণত করে।"),
    _q("Which organ produces bile?", ["The liver", "The gall bladder", "The pancreas", "The stomach"],
       "The gall bladder only stores and concentrates bile made by the liver.",
       "কোন অঙ্গ পিত্ত তৈরি করে?", ["যকৃৎ", "পিত্তথলি", "অগ্ন্যাশয়", "পাকস্থলী"],
       "পিত্তথলি কেবল যকৃতের তৈরি পিত্ত জমিয়ে গাঢ় করে।"),
    _q("Which vitamin is made by the skin in sunlight and helps absorb calcium?", ["Vitamin D", "Vitamin C", "Vitamin B12", "Vitamin E"],
       "Its lack causes rickets in children and osteomalacia in adults.",
       "কোন ভিটামিন সূর্যালোকে ত্বকে তৈরি হয় আর ক্যালসিয়াম শোষণে সাহায্য করে?", ["ভিটামিন D", "ভিটামিন C", "ভিটামিন B12", "ভিটামিন E"],
       "এর অভাবে শিশুদের রিকেটস আর বড়দের অস্টিওম্যালাসিয়া হয়।"),
    _q("Which statement describes a test cross?", ["Crossing an individual of dominant phenotype with a homozygous recessive", "Crossing two homozygous dominants", "Crossing two heterozygotes", "Self-pollinating a recessive plant"],
       "If any offspring show the recessive trait, the tested parent must be heterozygous.",
       "কোন বিবৃতি পরীক্ষা-সংকরকে বর্ণনা করে?", ["প্রকট ফিনোটাইপের একটা জীবকে সমযুগ্মী প্রচ্ছন্নের সঙ্গে সংকরায়ণ", "দুটো সমযুগ্মী প্রকটের সংকরায়ণ", "দুটো বিষমযুগ্মীর সংকরায়ণ", "একটা প্রচ্ছন্ন উদ্ভিদের স্বপরাগযোগ"],
       "কোনো অপত্য প্রচ্ছন্ন বৈশিষ্ট্য দেখালে পরীক্ষিত জনক নিশ্চয়ই বিষমযুগ্মী।"),
    _q("Which statement about Mendel's law of independent assortment is correct?", ["Alleles of different genes separate independently during gamete formation", "All genes are always inherited together", "Dominant alleles always pair with dominant alleles", "It applies to genes close together on the same chromosome"],
       "It holds for genes on different chromosomes (or far apart on one), giving the 9:3:3:1 ratio.",
       "মেন্ডেলের স্বাধীন বিন্যাস সূত্র সম্পর্কে কোন বিবৃতি সঠিক?", ["গ্যামেট তৈরির সময় ভিন্ন জিনের অ্যালিল স্বাধীনভাবে পৃথক হয়", "সব জিন সবসময় একসঙ্গে বাহিত হয়", "প্রকট অ্যালিল সবসময় প্রকটের সঙ্গে জোড় বাঁধে", "একই ক্রোমোজোমে কাছাকাছি থাকা জিনে খাটে"],
       "এটা ভিন্ন ক্রোমোজোমের (বা একই ক্রোমোজোমে দূরে থাকা) জিনে খাটে, ফলে 9:3:3:1 অনুপাত।"),
    _q("Which statement about the human genome project's findings is correct?", ["Less than 2% of the genome codes for proteins", "Humans have over 100,000 genes", "All human DNA codes for proteins", "Every person's genome is identical"],
       "There are about 20,000-25,000 genes; much of the rest is regulatory or repetitive DNA.",
       "হিউম্যান জিনোম প্রকল্পের ফলাফল সম্পর্কে কোন বিবৃতি সঠিক?", ["জিনোমের 2%-এরও কম অংশ প্রোটিনের সংকেত দেয়", "মানুষের 1,00,000-এর বেশি জিন আছে", "মানুষের সব ডিএনএ প্রোটিনের সংকেত দেয়", "প্রত্যেক মানুষের জিনোম হুবহু এক"],
       "জিন প্রায় 20,000-25,000টি; বাকি অনেকটা নিয়ন্ত্রক বা পুনরাবৃত্ত ডিএনএ।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
