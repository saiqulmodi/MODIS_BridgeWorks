"""Class 10 - Biology (Bridge Engineer): codominance and blood groups, sex-linked inheritance,
expected numbers from crosses, bacterial counts from dilutions, decomposition rates, energy
budgets of animals, dosing by body mass, protein synthesis, monoclonal antibodies, kidney
dialysis, plant disease, classification, human impact on ecosystems, and occupational health
for bridge crews - vibration, noise, dust, heat and mental well-being."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r + 2, r * 2, r + 10):
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


def expected(total, frac_num, frac_den, trait_en, trait_bn, cross):
    r = total * frac_num // frac_den
    return _n(f"In a {cross} cross, {frac_num}/{frac_den} of the offspring are expected to show {trait_en}. Out of {total:,} seedlings, how many would you expect to show it?",
              f"একটা {cross} সংকরে প্রত্যাশিত {frac_num}/{frac_den} সন্তান {trait_bn} দেখাবে। {total:,}টি চারার মধ্যে কতগুলো দেখাবে বলে আশা?", r,
              f"{total:,} x {frac_num}/{frac_den} = {r:,}. Real counts vary a little because fertilisation is random.",
              f"{total:,} x {frac_num}/{frac_den} = {r:,}। নিষেক এলোমেলো বলে আসল সংখ্যা একটু আলাদা হয়।",
              (total - r if total - r != r else r // 2 * 3, total * frac_num // (frac_den * 2), total))


ABO = {
    ("AO", "BO"): ("AB", 25, "AB, AO, BO, OO - one in four is AB", "AB, AO, BO, OO - চারে একটা AB"),
    ("AA", "BB"): ("AB", 100, "every child gets A from one parent and B from the other", "প্রতিটা সন্তান এক অভিভাবক থেকে A আর অন্যজন থেকে B পায়"),
    ("AO", "OO"): ("O", 50, "AO, AO, OO, OO - half are group O", "AO, AO, OO, OO - অর্ধেক গ্রুপ O"),
    ("BO", "BO"): ("O", 25, "BB, BO, BO, OO - one in four is group O", "BB, BO, BO, OO - চারে একটা গ্রুপ O"),
}


def abo(p1, p2):
    grp, pct, why_en, why_bn = ABO[(p1, p2)]
    o = []
    for v in (pct, 25, 50, 75, 100, 0):
        if v not in o:
            o.append(v)
    return mcq(f"Blood group alleles A and B are codominant; O is recessive. Parents are {p1} and {p2}. What is the chance a child has blood group {grp}?",
               [f"{v}%" for v in o[:4]], 0, f"Punnett square: {why_en}, so {pct}%.",
               f"রক্তের গ্রুপের অ্যালিল A আর B সহ-প্রকট; O প্রচ্ছন্ন। বাবা-মা {p1} আর {p2}। সন্তানের রক্তের গ্রুপ {grp} হওয়ার সম্ভাবনা কত?",
               [f"{v}%" for v in o[:4]], f"পানেট-বর্গ: {why_bn}, তাই {pct}%।")


def colonies(count, dilution, vol_ml):
    r = count * dilution // vol_ml if vol_ml else count * dilution
    return _n(f"Water from a site tank is diluted {dilution:,} times; {vol_ml} ml of the diluted sample grows {count} colonies on an agar plate. How many bacteria were in each ml of the original water?",
              f"নির্মাণস্থলের ট্যাঙ্কের জল {dilution:,} গুণ পাতলা করা হলো; পাতলা নমুনার {vol_ml} ml আগার-প্লেটে {count}টি উপনিবেশ জন্মাল। আসল জলের প্রতি ml-এ কতগুলো ব্যাকটেরিয়া ছিল?", r,
              f"Each colony grew from one bacterium: {count} ÷ {vol_ml} ml x {dilution:,} = {r:,} per ml. That water needs treating before drinking!",
              f"প্রতিটা উপনিবেশ একটা ব্যাকটেরিয়া থেকে: {count} ÷ {vol_ml} ml x {dilution:,} = প্রতি ml-এ {r:,}। এই জল খাওয়ার আগে শোধন লাগবে!",
              (count * vol_ml, count + dilution, r // 10), " per ml", " প্রতি ml")


def decay(before, after, weeks, what_en, what_bn):
    r = _c((before - after) * 100 / before / weeks)
    return _n(f"A bag of {what_en} in a compost bin goes from {before:g} g to {after:g} g in {weeks} weeks. What is the mean percentage mass lost per week?",
              f"কম্পোস্ট-বাক্সে এক ব্যাগ {what_bn} {weeks} সপ্তাহে {before:g} g থেকে {after:g} g হলো। সপ্তাহে গড়ে কত শতাংশ ভর কমল?", r,
              f"Loss = {_c(before - after):g} g = {_c((before - after) * 100 / before):g}% of the start; ÷ {weeks} = {r:g}% per week.",
              f"কমেছে {_c(before - after):g} g = শুরুর {_c((before - after) * 100 / before):g}%; ÷ {weeks} = সপ্তাহে {r:g}%।",
              (_c((before - after) * 100 / before), _c((before - after) / weeks), _c(r * 2)), "%")


def budget(eaten, resp, waste, animal_en, animal_bn):
    growth = eaten - resp - waste
    r = _c(growth * 100 / eaten)
    return _n(f"A {animal_en} eats food containing {eaten:,} kJ. It uses {resp:,} kJ in respiration and loses {waste:,} kJ in waste. What percentage goes into new growth?",
              f"একটা {animal_bn} {eaten:,} kJ-এর খাবার খায়। শ্বসনে {resp:,} kJ খরচ করে আর বর্জ্যে {waste:,} kJ হারায়। কত শতাংশ নতুন বৃদ্ধিতে যায়?", r,
              f"Growth = {eaten:,} - {resp:,} - {waste:,} = {growth:,} kJ; {growth:,} ÷ {eaten:,} x 100 = {r:g}%.",
              f"বৃদ্ধি = {eaten:,} - {resp:,} - {waste:,} = {growth:,} kJ; {growth:,} ÷ {eaten:,} x 100 = {r:g}%।",
              (_c(resp * 100 / eaten), _c(waste * 100 / eaten), _c(100 - r)), "%")


def dose(mg_per_kg, mass):
    r = mg_per_kg * mass
    return _n(f"A medicine is given at {mg_per_kg} mg per kg of body mass. What dose does a {mass} kg worker need?",
              f"একটা ওষুধ দেহের ভরের প্রতি kg-এ {mg_per_kg} mg দেওয়া হয়। {mass} kg-এর একজন কর্মীর কত মাত্রা লাগবে?", r,
              f"{mg_per_kg} x {mass} = {r:,} mg. Doses must always be checked by a doctor or pharmacist.",
              f"{mg_per_kg} x {mass} = {r:,} mg। মাত্রা সবসময় ডাক্তার বা ফার্মাসিস্টকে দিয়ে যাচাই করাতে হবে।",
              (mg_per_kg + mass, _c(mass / mg_per_kg), r * 10), " mg")


def sexlinked():
    return mcq("Red-green colour blindness is caused by a recessive allele on the X chromosome. A carrier mother (XᴮXᵇ) and an unaffected father (XᴮY) have a son. What is the chance the son is colour-blind?",
               ["50%", "25%", "0%", "100%"], 0,
               "A son gets Y from his father and one X from his mother - half her X chromosomes carry b.",
               "লাল-সবুজ বর্ণান্ধতা X ক্রোমোজোমের এক প্রচ্ছন্ন অ্যালিলের জন্য হয়। বাহক মা (XᴮXᵇ) আর সুস্থ বাবার (XᴮY) একটা ছেলে হলো। ছেলেটার বর্ণান্ধ হওয়ার সম্ভাবনা কত?",
               ["50%", "25%", "0%", "100%"],
               "ছেলে বাবার থেকে Y আর মায়ের থেকে একটা X পায় - মায়ের X-এর অর্ধেকে b থাকে।")


def popdensity(n, area_km2, what_en, what_bn):
    r = _c(n / area_km2)
    return _n(f"A survey finds {n:,} {what_en} in a {area_km2:g} km² wetland beside a planned bridge. What is the population density?",
              f"পরিকল্পিত সেতুর পাশে {area_km2:g} km² জলাভূমিতে জরিপে {n:,}টি {what_bn} পাওয়া গেল। জনসংখ্যার ঘনত্ব কত?", r,
              f"Density = number ÷ area = {n:,} ÷ {area_km2:g} = {r:g} per km².",
              f"ঘনত্ব = সংখ্যা ÷ ক্ষেত্রফল = {n:,} ÷ {area_km2:g} = km²-প্রতি {r:g}।",
              (_c(n * area_km2), _c(area_km2 / n * 1000), _c(r * 2)), " per km²", " প্রতি km²")


ITEMS = (
    expected(400, 3, 4, "the dominant tall form", "প্রকট লম্বা রূপ", "Tt x Tt"), expected(200, 1, 4, "the recessive white colour", "প্রচ্ছন্ন সাদা রং", "Ww x Ww"),
    expected(600, 1, 2, "the recessive short form", "প্রচ্ছন্ন খাটো রূপ", "Tt x tt"), expected(1000, 3, 4, "purple flowers", "বেগুনি ফুল", "Pp x Pp"),
    expected(320, 1, 4, "the recessive wrinkled seeds", "প্রচ্ছন্ন কোঁচকানো বীজ", "Rr x Rr"),
    abo("AO", "BO"), abo("AA", "BB"), abo("AO", "OO"), abo("BO", "BO"),
    sexlinked(),
    colonies(40, 1000, 1), colonies(25, 10000, 1), colonies(60, 100, 2), colonies(15, 100000, 1),
    decay(500, 380, 4, "leaf litter", "ঝরা পাতা"), decay(200, 140, 6, "straw", "খড়"), decay(1000, 700, 5, "food scraps", "খাবারের উচ্ছিষ্ট"),
    decay(300, 255, 3, "sawdust", "করাতের গুঁড়ো"),
    budget(1000, 600, 300, "cow grazing on an embankment", "বাঁধে চরা গরু"), budget(500, 150, 200, "fish in a river", "নদীর মাছ"),
    budget(2000, 1400, 400, "bat living under a bridge", "সেতুর নিচে থাকা বাদুড়"), budget(800, 500, 220, "rabbit", "খরগোশ"),
    dose(10, 60), dose(5, 80), dose(15, 50), dose(2, 75),
    popdensity(1200, 4, "frogs", "ব্যাঙ"), popdensity(56, 0.8, "kingfishers", "মাছরাঙা"),
    expected(800, 1, 4, "the recessive albino form", "প্রচ্ছন্ন অ্যালবিনো রূপ", "Aa x Aa"), expected(240, 1, 2, "the dominant red flowers", "প্রকট লাল ফুল", "Rr x rr"),
    colonies(80, 1000, 2), colonies(32, 10000, 4), decay(400, 260, 7, "grass cuttings", "ঘাসের কুচি"), decay(250, 225, 2, "bark chips", "বাকলের টুকরো"),
    budget(1200, 700, 380, "goat", "ছাগল"), budget(300, 120, 135, "frog", "ব্যাঙ"), dose(20, 45), dose(8, 90), colonies(12, 100000, 3), popdensity(450, 2.5, "water birds", "জলচর পাখি"), popdensity(90, 0.6, "otters", "ভোঁদড়"),
    mcq("What does 'codominance' mean?", ["Both alleles are fully expressed in the phenotype", "One allele hides the other", "Neither allele is expressed", "Alleles change each generation"], 0,
        "Blood group AB shows both A and B antigens.",
        "'সহ-প্রকটতা' মানে কী?", ["দুটো অ্যালিলই ফিনোটাইপে পুরো প্রকাশ পায়", "একটা অ্যালিল অন্যটাকে ঢাকে", "কোনো অ্যালিলই প্রকাশ পায় না", "প্রতি প্রজন্মে অ্যালিল বদলায়"],
        "রক্তের গ্রুপ AB-তে A আর B দুটো অ্যান্টিজেনই থাকে।"),
    mcq("Why must blood groups be matched before a transfusion after a site accident?", ["Antibodies in the patient's plasma would attack donated red cells with foreign antigens, causing clumping", "Blood groups affect hair colour", "Any blood can be given safely", "To match the hospital's records only"], 0,
        "Group O negative is often used in emergencies as a 'universal donor'.",
        "নির্মাণস্থলের দুর্ঘটনার পরে রক্ত দেওয়ার আগে রক্তের গ্রুপ মেলাতে হয় কেন?", ["রোগীর রক্তরসের অ্যান্টিবডি দান-করা লোহিতকণিকার বিদেশি অ্যান্টিজেনকে আক্রমণ করে দলা পাকাবে", "রক্তের গ্রুপ চুলের রঙে প্রভাব ফেলে", "যেকোনো রক্ত নিরাপদে দেওয়া যায়", "শুধু হাসপাতালের নথি মেলাতে"],
        "জরুরি অবস্থায় প্রায়ই ও-নেগেটিভ 'সর্বজনীন দাতা' হিসেবে ব্যবহার হয়।"),
    mcq("Why are sex-linked conditions like haemophilia more common in males?", ["Males have only one X chromosome, so a single recessive allele is expressed", "Males have two X chromosomes", "Females cannot inherit X chromosomes", "It is caused by diet"], 0,
        "Females need two copies of the recessive allele to be affected.",
        "হিমোফিলিয়ার মতো লিঙ্গ-সংযুক্ত অবস্থা পুরুষদের মধ্যে বেশি দেখা যায় কেন?", ["পুরুষদের মাত্র একটা X ক্রোমোজোম, তাই একটা প্রচ্ছন্ন অ্যালিলই প্রকাশ পায়", "পুরুষদের দুটো X ক্রোমোজোম", "মহিলারা X ক্রোমোজোম পান না", "খাদ্যের জন্য হয়"],
        "মহিলাদের আক্রান্ত হতে প্রচ্ছন্ন অ্যালিলের দুটো কপি লাগে।"),
    mcq("Which pair of sex chromosomes does a human male have?", ["XY", "XX", "YY", "X only"], 0,
        "The father's sperm decides the sex of the child.",
        "মানব পুরুষের লিঙ্গ-ক্রোমোজোমের জোড়া কোনটা?", ["XY", "XX", "YY", "শুধু X"],
        "বাবার শুক্রাণু সন্তানের লিঙ্গ ঠিক করে।"),
    mcq("In protein synthesis, what does mRNA do?", ["Carries a copy of a gene's code from the nucleus to the ribosomes", "Digests proteins", "Stores energy", "Makes the cell wall"], 0,
        "Ribosomes read the code three bases at a time.",
        "প্রোটিন-সংশ্লেষে এমআরএনএ কী করে?", ["নিউক্লিয়াস থেকে রাইবোজোমে জিনের সংকেতের কপি বয়ে নেয়", "প্রোটিন হজম করে", "শক্তি জমায়", "কোষপ্রাচীর বানায়"],
        "রাইবোজোম একবারে তিনটে করে ক্ষারক পড়ে।"),
    mcq("How many bases code for one amino acid?", ["Three (a triplet)", "One", "Two", "Ten"], 0,
        "Four bases in groups of three give 64 possible codes - enough for 20 amino acids.",
        "কতগুলো ক্ষারক একটা অ্যামিনো অ্যাসিডের সংকেত দেয়?", ["তিনটে (একটা ত্রয়ী)", "একটা", "দুটো", "দশটা"],
        "চারটে ক্ষারক তিনটে করে দলে 64টি সম্ভাব্য সংকেত দেয় - 20টি অ্যামিনো অ্যাসিডের জন্য যথেষ্ট।"),
    mcq("Why can a mutation in one base change a protein's function?", ["It can change one amino acid, altering the protein's shape - such as an enzyme's active site", "Bases have no effect on proteins", "It always makes the protein bigger", "Mutations only affect hair"], 0,
        "Many mutations have no effect; a few are harmful and very few helpful.",
        "একটা ক্ষারকের মিউটেশন কেন প্রোটিনের কাজ বদলাতে পারে?", ["একটা অ্যামিনো অ্যাসিড বদলে প্রোটিনের আকার বদলাতে পারে - যেমন এনজাইমের সক্রিয় স্থান", "ক্ষারক প্রোটিনে প্রভাব ফেলে না", "সবসময় প্রোটিন বড় করে", "মিউটেশন শুধু চুলে প্রভাব ফেলে"],
        "অনেক মিউটেশনের প্রভাব নেই; কয়েকটা ক্ষতিকর আর খুব কম উপকারী।"),
    mcq("What are monoclonal antibodies?", ["Identical antibodies made by clones of one type of cell, all targeting one specific antigen", "Antibodies from many different cells", "Antibiotics", "Vaccines made of bacteria"], 0,
        "They are used in pregnancy tests and to treat some cancers.",
        "মনোক্লোনাল অ্যান্টিবডি কী?", ["এক ধরনের কোষের ক্লোন থেকে তৈরি হুবহু এক অ্যান্টিবডি, সবাই একটা নির্দিষ্ট অ্যান্টিজেনকে লক্ষ্য করে", "অনেক আলাদা কোষের অ্যান্টিবডি", "অ্যান্টিবায়োটিক", "ব্যাকটেরিয়ার তৈরি টিকা"],
        "গর্ভাবস্থার পরীক্ষা আর কিছু ক্যান্সারের চিকিৎসায় ব্যবহার হয়।"),
    mcq("How do rapid lateral-flow tests detect an infection?", ["Monoclonal antibodies on a strip bind the target antigen and show a coloured line", "They measure body temperature", "They count white cells", "They grow bacteria for a week"], 0,
        "A control line shows the test itself worked.",
        "দ্রুত ল্যাটারাল-ফ্লো পরীক্ষা কীভাবে সংক্রমণ ধরে?", ["ফালিতে মনোক্লোনাল অ্যান্টিবডি লক্ষ্য-অ্যান্টিজেনে বেঁধে রঙিন রেখা দেখায়", "শরীরের তাপমাত্রা মাপে", "শ্বেতকণিকা গোনে", "এক সপ্তাহ ব্যাকটেরিয়া জন্মায়"],
        "নিয়ন্ত্রণ-রেখা দেখায় পরীক্ষাটা নিজে কাজ করেছে।"),
    mcq("What does a kidney dialysis machine do?", ["Filters urea and excess salts from the blood through a partially permeable membrane", "Pumps blood like a heart", "Adds oxygen to blood", "Digests food"], 0,
        "Patients often need dialysis several times a week until a transplant.",
        "বৃক্কের ডায়ালিসিস-যন্ত্র কী করে?", ["আংশিক-ভেদ্য পর্দার মধ্যে দিয়ে রক্ত থেকে ইউরিয়া আর অতিরিক্ত লবণ ছেঁকে বার করে", "হৃৎপিণ্ডের মতো রক্ত পাম্প করে", "রক্তে অক্সিজেন যোগ করে", "খাবার হজম করে"],
        "প্রতিস্থাপনের আগে পর্যন্ত রোগীদের প্রায়ই সপ্তাহে কয়েকবার ডায়ালিসিস লাগে।"),
    mcq("Why might a transplanted kidney be rejected?", ["The immune system recognises its antigens as foreign and attacks it", "Kidneys are too heavy", "The blood is too thin", "Kidneys cannot be moved"], 0,
        "Tissue matching and immunosuppressant drugs reduce the risk.",
        "প্রতিস্থাপিত বৃক্ক কেন প্রত্যাখ্যাত হতে পারে?", ["প্রতিরোধ-ব্যবস্থা এর অ্যান্টিজেনকে বিদেশি চিনে আক্রমণ করে", "বৃক্ক খুব ভারী", "রক্ত খুব পাতলা", "বৃক্ক সরানো যায় না"],
        "কলা মিলিয়ে আর প্রতিরোধ-দমনকারী ওষুধে ঝুঁকি কমে।"),
    mcq("How can farmers and foresters detect plant disease early?", ["Look for stunted growth, spots, decay, abnormal growths, discolouration or pests - then test", "Wait until the plant dies", "Only by the plant's height", "Plants never get diseases"], 0,
        "Early action stops a disease spreading through a whole plantation.",
        "চাষি আর বনকর্মীরা কীভাবে আগেভাগে উদ্ভিদের রোগ ধরতে পারেন?", ["খর্ব বৃদ্ধি, দাগ, পচন, অস্বাভাবিক বৃদ্ধি, বিবর্ণতা বা পোকা দেখো - তারপর পরীক্ষা করো", "গাছ মরা পর্যন্ত অপেক্ষা", "শুধু গাছের উচ্চতা দেখে", "গাছের রোগ হয় না"],
        "আগেভাগে ব্যবস্থা নিলে রোগ গোটা বাগানে ছড়ায় না।"),
    mcq("Why can timber in a footbridge suffer from 'wet rot' fungi?", ["Fungi feed on wood cellulose when it stays damp", "Wood attracts lightning", "Dry wood is always rotten", "Fungi only live in deserts"], 0,
        "Good drainage and ventilation keep timber below the moisture level fungi need.",
        "পায়ে-চলা সেতুর কাঠে 'ভেজা পচন' ছত্রাক কেন ধরতে পারে?", ["কাঠ ভেজা থাকলে ছত্রাক তার সেলুলোজ খায়", "কাঠ বাজ টানে", "শুকনো কাঠ সবসময় পচা", "ছত্রাক শুধু মরুভূমিতে থাকে"],
        "ভালো জলনিকাশ আর বায়ুচলাচল কাঠকে ছত্রাকের দরকারি আর্দ্রতার নিচে রাখে।"),
    mcq("In the three-domain system, what are the three domains?", ["Archaea, Bacteria and Eukaryota", "Plants, animals and fungi", "Fish, birds and mammals", "Viruses, cells and tissues"], 0,
        "Carl Woese proposed it after studying genetic material.",
        "তিন-অধিজগৎ ব্যবস্থায় তিনটে অধিজগৎ কী?", ["আর্কিয়া, ব্যাকটেরিয়া আর ইউক্যারিওটা", "উদ্ভিদ, প্রাণী আর ছত্রাক", "মাছ, পাখি আর স্তন্যপায়ী", "ভাইরাস, কোষ আর কলা"],
        "জিনগত উপাদান গবেষণার পরে কার্ল উজ এটা প্রস্তাব করেন।"),
    mcq("Why do scientists now classify organisms using DNA as well as appearance?", ["DNA shows how closely related species really are, even when they look different", "Appearance never matters", "DNA is easier to see", "It is required by law"], 0,
        "Some look-alike species turn out to be distant relatives.",
        "বিজ্ঞানীরা এখন চেহারার পাশাপাশি ডিএনএ দিয়েও জীব শ্রেণিবিভাগ করেন কেন?", ["ডিএনএ দেখায় প্রজাতিগুলো আসলে কতটা ঘনিষ্ঠ, দেখতে আলাদা হলেও", "চেহারা কখনো গুরুত্বপূর্ণ নয়", "ডিএনএ দেখা সহজ", "আইনে বাধ্যতামূলক"],
        "কিছু একরকম-দেখতে প্রজাতি আসলে দূরের আত্মীয় বেরোয়।"),
    mcq("What is an 'evolutionary tree'?", ["A diagram showing how species are thought to be related through common ancestors", "A very old tree", "A family photo album", "A list of extinct animals only"], 0,
        "Branch points show where lineages split.",
        "'বিবর্তনীয় বৃক্ষ' কী?", ["সাধারণ পূর্বপুরুষের মাধ্যমে প্রজাতিগুলো কীভাবে সম্পর্কিত বলে মনে করা হয় তার চিত্র", "খুব পুরোনো গাছ", "পারিবারিক অ্যালবাম", "শুধু বিলুপ্ত প্রাণীর তালিকা"],
        "শাখার বিন্দু দেখায় কোথায় বংশধারা আলাদা হয়েছে।"),
    mcq("Why does draining or burning peat bogs add to climate change?", ["Peat stores huge amounts of carbon, released as CO2 when it decays or burns", "Peat absorbs oxygen", "Peat is a metal", "It cools the planet"], 0,
        "Peat-free compost helps protect these carbon stores.",
        "পিট-জলাভূমি শুকোলে বা পোড়ালে জলবায়ু-পরিবর্তন বাড়ে কেন?", ["পিটে বিপুল কার্বন জমা থাকে, যা পচলে বা পুড়লে CO2 হিসেবে বেরোয়", "পিট অক্সিজেন শোষে", "পিট একটা ধাতু", "এটা গ্রহকে ঠান্ডা করে"],
        "পিট-মুক্ত কম্পোস্ট এই কার্বন-ভান্ডার রক্ষায় সাহায্য করে।"),
    mcq("What is 'deforestation' doing to the global carbon cycle?", ["Fewer trees absorb CO2, and burning or rotting them releases more", "It removes CO2 from the air", "It has no effect", "It creates oxygen"], 0,
        "Bridge projects often replant more trees than they remove.",
        "বিশ্ব কার্বন-চক্রে 'বন উজাড়' কী করছে?", ["কম গাছ CO2 শোষে, আর পোড়ানো বা পচানো আরও ছাড়ে", "বাতাস থেকে CO2 সরায়", "কোনো প্রভাব নেই", "অক্সিজেন তৈরি করে"],
        "সেতু-প্রকল্প প্রায়ই যত গাছ কাটে তার বেশি লাগায়।"),
    mcq("What does 'land use' change around a new bridge often include?", ["New roads, housing and businesses replacing farms and natural habitats", "Only more trees", "Nothing changes", "Rivers disappearing"], 0,
        "Planners try to balance development with protecting habitats.",
        "নতুন সেতুর আশপাশে 'জমি-ব্যবহারের' বদলে প্রায়ই কী থাকে?", ["খেত আর প্রাকৃতিক বাসস্থানের জায়গায় নতুন রাস্তা, বাড়ি আর ব্যবসা", "শুধু বেশি গাছ", "কিছুই বদলায় না", "নদী উধাও হওয়া"],
        "পরিকল্পনাকারীরা উন্নয়ন আর বাসস্থান-রক্ষার ভারসাম্য খোঁজেন।"),
    mcq("Why are wildlife underpasses and green bridges built across busy highways?", ["They reconnect habitats so animals can cross safely, reducing road deaths and isolation", "To decorate the road", "To slow traffic", "To grow crops"], 0,
        "Isolated populations can lose genetic variety.",
        "ব্যস্ত মহাসড়কের উপর দিয়ে বন্যপ্রাণীর সুড়ঙ্গপথ আর সবুজ সেতু বানানো হয় কেন?", ["বাসস্থান আবার জোড়ে, যাতে প্রাণীরা নিরাপদে পার হয়, রাস্তায় মৃত্যু আর বিচ্ছিন্নতা কমে", "রাস্তা সাজাতে", "যানবাহন ধীর করতে", "ফসল ফলাতে"],
        "বিচ্ছিন্ন জনগোষ্ঠী জিনগত বৈচিত্র্য হারাতে পারে।"),
    mcq("What is a 'protected area' or nature reserve?", ["Land or water managed to conserve wildlife and habitats, with limits on development", "A military base", "A private garden", "A toll plaza"], 0,
        "New routes often avoid them or use viaducts to reduce harm.",
        "'সংরক্ষিত এলাকা' বা প্রকৃতি-অভয়ারণ্য কী?", ["বন্যপ্রাণী আর বাসস্থান রক্ষায় পরিচালিত জমি বা জল, উন্নয়নে বিধিনিষেধসহ", "সামরিক ঘাঁটি", "ব্যক্তিগত বাগান", "টোল-প্লাজা"],
        "নতুন পথ প্রায়ই এগুলো এড়ায় বা ক্ষতি কমাতে উড়ালপথ ব্যবহার করে।"),
    mcq("What is 'whole-body vibration' and who is at risk?", ["Shaking transmitted through the seat or feet, affecting drivers of dumpers, rollers and excavators", "Shaking hands", "Vibration of bridge cables only", "A type of exercise"], 0,
        "It can cause back pain; good seats and shorter exposure help.",
        "'সারা-শরীরের কম্পন' কী আর কারা ঝুঁকিতে?", ["আসন বা পায়ের মধ্য দিয়ে আসা ঝাঁকুনি, যা ডাম্পার, রোলার আর খননযন্ত্রের চালকদের প্রভাবিত করে", "হাত মেলানো", "শুধু সেতুর তারের কম্পন", "এক রকম ব্যায়াম"],
        "এতে পিঠে ব্যথা হতে পারে; ভালো আসন আর কম সময় সাহায্য করে।"),
    mcq("What is 'tinnitus', which some workers develop after years of loud noise?", ["A constant ringing or buzzing in the ears", "An eye disease", "A skin rash", "A broken bone"], 0,
        "Ear protection prevents it - it often cannot be cured.",
        "বছরের পর বছর জোরালো শব্দের পরে কিছু কর্মীর যে 'টিনিটাস' হয়, তা কী?", ["কানে অবিরাম ঝিঁঝিঁ বা গুঞ্জন", "চোখের রোগ", "চামড়ার ফুসকুড়ি", "ভাঙা হাড়"],
        "কানের সুরক্ষা এটা আটকায় - প্রায়ই সারানো যায় না।"),
    mcq("Why is mental health support important for bridge construction workers?", ["Long hours, time away from family and dangerous work raise stress, and construction has high suicide rates in many countries", "Construction is never stressful", "Mental health does not affect safety", "Only managers get stressed"], 0,
        "Talking openly and offering support saves lives.",
        "সেতু-নির্মাণ কর্মীদের মানসিক স্বাস্থ্যের সহায়তা জরুরি কেন?", ["দীর্ঘ সময়, পরিবার থেকে দূরে থাকা আর বিপজ্জনক কাজ চাপ বাড়ায়, আর অনেক দেশে নির্মাণশিল্পে আত্মহত্যার হার বেশি", "নির্মাণ কখনো চাপের নয়", "মানসিক স্বাস্থ্য নিরাপত্তায় প্রভাব ফেলে না", "শুধু ম্যানেজারদের চাপ হয়"],
        "খোলাখুলি কথা বলা আর সহায়তা দেওয়া প্রাণ বাঁচায়।"),
    mcq("How does chronic stress affect the body?", ["Long-term high stress hormones can raise blood pressure, weaken immunity and disturb sleep", "It makes bones stronger", "It has no physical effect", "It only affects hair colour"], 0,
        "Rest, exercise, sleep and talking to someone all help.",
        "দীর্ঘস্থায়ী চাপ শরীরে কী প্রভাব ফেলে?", ["দীর্ঘদিন বেশি চাপ-হরমোন রক্তচাপ বাড়াতে, প্রতিরোধ দুর্বল করতে আর ঘুম ব্যাহত করতে পারে", "হাড় শক্ত করে", "শারীরিক প্রভাব নেই", "শুধু চুলের রঙে প্রভাব"],
        "বিশ্রাম, ব্যায়াম, ঘুম আর কারও সঙ্গে কথা বলা সবই সাহায্য করে।"),
    mcq("What is 'heat exhaustion' compared with heat stroke?", ["Heat exhaustion is an earlier stage - heavy sweating, weakness, nausea; untreated it can become heat stroke", "They are exactly the same", "Heat exhaustion is more dangerous", "Heat exhaustion happens only in cold weather"], 0,
        "Move to shade, cool down, sip water and rest - get help if it worsens.",
        "হিটস্ট্রোকের তুলনায় 'তাপজনিত অবসাদ' কী?", ["আগের ধাপ - প্রচুর ঘাম, দুর্বলতা, বমিভাব; চিকিৎসা না হলে হিটস্ট্রোক হতে পারে", "হুবহু এক", "তাপজনিত অবসাদ বেশি বিপজ্জনক", "শুধু ঠান্ডায় হয়"],
        "ছায়ায় যাও, ঠান্ডা হও, অল্প অল্প জল খাও আর বিশ্রাম নাও - খারাপ হলে সাহায্য নাও।"),
    mcq("Why are work-rest schedules used in very hot weather on bridge sites?", ["Regular breaks in shade let the body lose heat before core temperature rises dangerously", "To reduce wages", "To slow the project on purpose", "Heat does not affect people"], 0,
        "Heavy work in the hottest hours is often moved to early morning.",
        "খুব গরম আবহাওয়ায় সেতু-নির্মাণস্থলে কাজ-বিশ্রামের সূচি কেন মানা হয়?", ["ছায়ায় নিয়মিত বিরতিতে শরীরের ভেতরের তাপমাত্রা বিপজ্জনকভাবে বাড়ার আগে তাপ বেরোতে পারে", "মজুরি কমাতে", "ইচ্ছে করে প্রকল্প ধীর করতে", "তাপ মানুষকে প্রভাবিত করে না"],
        "সবচেয়ে গরম ঘণ্টার ভারী কাজ প্রায়ই ভোরে সরানো হয়।"),
    mcq("What is 'occupational asthma'?", ["Asthma caused by breathing substances at work, such as some dusts, fumes or isocyanate paints", "Asthma from playing sports", "A type of broken rib", "Asthma that only children get"], 0,
        "Good ventilation and the right respirator protect workers.",
        "'পেশাগত হাঁপানি' কী?", ["কাজের জায়গায় কিছু ধুলো, ধোঁয়া বা আইসোসায়ানেট রঙের মতো পদার্থ শ্বাসে নিয়ে হাঁপানি", "খেলাধুলা থেকে হাঁপানি", "এক রকম ভাঙা পাঁজর", "শুধু শিশুদের হাঁপানি"],
        "ভালো বায়ুচলাচল আর ঠিক রেসপিরেটর কর্মীদের রক্ষা করে।"),
    mcq("Why must a dust mask fit closely to the face to work?", ["Air takes the easiest path - gaps let dusty air in around the filter", "Masks only work when loose", "Tight masks filter sound", "Fit does not matter"], 0,
        "Workers with beards may need hood-type respirators instead.",
        "ধুলো-মুখোশ কাজ করতে মুখে ঠিকঠাক এঁটে বসতে হয় কেন?", ["বাতাস সহজতম পথে যায় - ফাঁক থাকলে ছাঁকনির পাশ দিয়ে ধুলোভরা বাতাস ঢোকে", "ঢিলে হলেই মুখোশ কাজ করে", "আঁটোসাঁটো মুখোশ শব্দ ছাঁকে", "এঁটে বসা গুরুত্বহীন"],
        "দাড়িওয়ালা কর্মীদের বদলে হুডের মতো রেসপিরেটর লাগতে পারে।"),
    mcq("What is 'mesothelioma'?", ["A cancer of the lining around the lungs, strongly linked to past asbestos exposure", "A bone infection", "A skin burn", "A type of flu"], 0,
        "It can appear 20-50 years after exposure.",
        "'মেসোথেলিওমা' কী?", ["ফুসফুসের চারপাশের আস্তরণের ক্যান্সার, অতীতে অ্যাসবেস্টসের সংস্পর্শের সঙ্গে জোরালোভাবে যুক্ত", "হাড়ের সংক্রমণ", "চামড়া পোড়া", "এক রকম ফ্লু"],
        "সংস্পর্শের 20-50 বছর পরে দেখা দিতে পারে।"),
    mcq("Why do health checks for workers include lung function tests?", ["To spot early damage from dust or fumes so exposure can be reduced", "To measure height", "To check eyesight", "To test hearing"], 0,
        "A spirometer measures how much air and how fast a person can breathe out.",
        "কর্মীদের স্বাস্থ্য-পরীক্ষায় ফুসফুসের কার্যক্ষমতার পরীক্ষা থাকে কেন?", ["ধুলো বা ধোঁয়ায় হওয়া প্রাথমিক ক্ষতি ধরতে, যাতে সংস্পর্শ কমানো যায়", "উচ্চতা মাপতে", "দৃষ্টি পরীক্ষা করতে", "শ্রবণ পরীক্ষা করতে"],
        "স্পাইরোমিটার মাপে মানুষ কতটা বাতাস আর কত দ্রুত ছাড়তে পারে।"),
    mcq("What is the role of the lymphatic system in fighting infection?", ["It carries lymph and contains lymph nodes where white blood cells gather to attack pathogens", "It pumps blood", "It digests fat only", "It controls breathing"], 0,
        "Swollen 'glands' in the neck are lymph nodes working hard.",
        "সংক্রমণের বিরুদ্ধে লড়াইয়ে লসিকাতন্ত্রের ভূমিকা কী?", ["লসিকা বয় আর এতে লসিকাগ্রন্থি থাকে, যেখানে শ্বেতকণিকা জড়ো হয়ে জীবাণুকে আক্রমণ করে", "রক্ত পাম্প করে", "শুধু চর্বি হজম করে", "শ্বাস নিয়ন্ত্রণ করে"],
        "গলায় ফোলা 'গ্রন্থি' মানে লসিকাগ্রন্থি কঠোর কাজ করছে।"),
    mcq("Why are 'memory cells' important after an infection or vaccination?", ["They remember the antigen and make antibodies quickly if it returns", "They store food", "They improve eyesight", "They carry oxygen"], 0,
        "That is why some diseases are caught only once.",
        "সংক্রমণ বা টিকার পরে 'স্মৃতি-কোষ' জরুরি কেন?", ["অ্যান্টিজেন মনে রাখে আর ফিরে এলে দ্রুত অ্যান্টিবডি বানায়", "খাবার জমায়", "দৃষ্টি বাড়ায়", "অক্সিজেন বয়"],
        "তাই কিছু রোগ একবারই হয়।"),
    mcq("What are 'antigens'?", ["Molecules on the surface of cells or pathogens that the immune system recognises", "A type of antibiotic", "Red blood cells", "Hormones"], 0,
        "Each antibody fits one specific antigen.",
        "'অ্যান্টিজেন' কী?", ["কোষ বা জীবাণুর উপরিতলের অণু, যা প্রতিরোধ-ব্যবস্থা চেনে", "এক রকম অ্যান্টিবায়োটিক", "লোহিতকণিকা", "হরমোন"],
        "প্রতিটা অ্যান্টিবডি একটা নির্দিষ্ট অ্যান্টিজেনে খাপ খায়।"),
    mcq("How are new medicines tested before they are approved?", ["Lab and cell tests, then animal tests where required, then clinical trials on people in increasing numbers", "Sold straight to the public", "Tested only on computers", "Tested once on one volunteer"], 0,
        "Trials check safety, the right dose and whether the drug works.",
        "অনুমোদনের আগে নতুন ওষুধ কীভাবে পরীক্ষা হয়?", ["ল্যাব আর কোষে পরীক্ষা, দরকারে প্রাণীর উপর পরীক্ষা, তারপর ক্রমশ বেশি মানুষের উপর চিকিৎসা-পরীক্ষা", "সরাসরি জনসাধারণকে বেচা", "শুধু কম্পিউটারে পরীক্ষা", "একজন স্বেচ্ছাসেবকের উপর একবার"],
        "পরীক্ষা নিরাপত্তা, ঠিক মাত্রা আর ওষুধ কাজ করে কিনা দেখে।"),
    mcq("Why do doctors prescribe medicine doses by body mass?", ["The same dose has a stronger effect in a smaller body", "Heavier people never need medicine", "Doses are random", "To save medicine"], 0,
        "Children's doses are much smaller than adults'.",
        "ডাক্তাররা দেহের ভর অনুযায়ী ওষুধের মাত্রা দেন কেন?", ["একই মাত্রা ছোট শরীরে বেশি জোরালো প্রভাব ফেলে", "ভারী মানুষের ওষুধ লাগে না", "মাত্রা এলোমেলো", "ওষুধ বাঁচাতে"],
        "শিশুদের মাত্রা বড়দের চেয়ে অনেক কম।"),
    mcq("What is an 'aseptic technique' when growing bacteria in a lab?", ["Steps such as sterilising loops and working near a flame to stop unwanted microbes contaminating the culture", "Growing bacteria in open air", "Using dirty equipment", "Heating bacteria until they die"], 0,
        "Plates are incubated at 25°C in schools to avoid growing human pathogens.",
        "ল্যাবে ব্যাকটেরিয়া জন্মানোর সময় 'জীবাণুমুক্ত কৌশল' কী?", ["লুপ জীবাণুমুক্ত করা আর শিখার কাছে কাজের মতো ধাপ, যাতে অনাকাঙ্ক্ষিত জীবাণু কালচার দূষিত না করে", "খোলা বাতাসে ব্যাকটেরিয়া জন্মানো", "নোংরা যন্ত্র ব্যবহার", "ব্যাকটেরিয়া মরা পর্যন্ত গরম করা"],
        "মানুষের রোগজীবাণু না জন্মাতে স্কুলে প্লেট 25°C-এ রাখা হয়।"),
    mcq("Why does a clear zone appear around an antibiotic disc on a bacterial lawn?", ["The antibiotic has killed or stopped bacteria growing there", "Light bleached the bacteria", "Bacteria moved away for fun", "The agar dried out"], 0,
        "A bigger clear zone usually means a more effective antibiotic.",
        "ব্যাকটেরিয়ার আস্তরণে একটা অ্যান্টিবায়োটিক-চাকতির চারপাশে স্বচ্ছ অঞ্চল দেখা যায় কেন?", ["অ্যান্টিবায়োটিক সেখানে ব্যাকটেরিয়া মেরেছে বা বাড়তে দেয়নি", "আলো ব্যাকটেরিয়া সাদা করেছে", "ব্যাকটেরিয়া মজা করে সরে গেছে", "আগার শুকিয়ে গেছে"],
        "বড় স্বচ্ছ অঞ্চল সাধারণত বেশি কার্যকর অ্যান্টিবায়োটিক বোঝায়।"),
    mcq("Why is drinking water on remote bridge sites often chlorinated or boiled?", ["To kill pathogens such as cholera and typhoid bacteria", "To improve the taste only", "To add minerals", "To make it cold"], 0,
        "Safe water is one of the most important health measures in any work camp.",
        "দূরের সেতু-নির্মাণস্থলে খাবার জল প্রায়ই ক্লোরিন দেওয়া বা ফোটানো হয় কেন?", ["কলেরা আর টাইফয়েডের মতো রোগজীবাণু মারতে", "শুধু স্বাদ ভালো করতে", "খনিজ যোগ করতে", "ঠান্ডা করতে"],
        "যেকোনো শ্রমিক-শিবিরে নিরাপদ জল সবচেয়ে জরুরি স্বাস্থ্য-ব্যবস্থাগুলোর একটা।"),
    mcq("What is 'selective breeding' of trees used for in forestry?", ["Choosing parent trees with useful features, such as fast, straight growth, to produce better timber", "Breeding animals in forests", "Cutting down all trees", "Genetic engineering in a lab"], 0,
        "Straight, strong timber suits construction.",
        "বনবিদ্যায় গাছের 'নির্বাচিত প্রজনন' কীসের জন্য ব্যবহার হয়?", ["দ্রুত, সোজা বৃদ্ধির মতো কাজের বৈশিষ্ট্যের মাতৃ-পিতৃ গাছ বেছে ভালো কাঠ পাওয়া", "বনে প্রাণীর প্রজনন", "সব গাছ কাটা", "ল্যাবে জিন-প্রযুক্তি"],
        "সোজা, শক্ত কাঠ নির্মাণের উপযোগী।"),
    mcq("What is a 'tissue culture' of plants?", ["Growing many identical plants from small pieces of tissue in sterile nutrient jelly", "Growing plants in tissue paper", "A type of compost", "Planting seeds in rows"], 0,
        "It quickly produces many plants for re-greening embankments.",
        "উদ্ভিদের 'কলা-কর্ষণ' কী?", ["জীবাণুমুক্ত পুষ্টি-জেলিতে কলার ছোট টুকরো থেকে অনেক হুবহু এক গাছ জন্মানো", "টিস্যু-কাগজে গাছ জন্মানো", "এক রকম কম্পোস্ট", "সারি করে বীজ বোনা"],
        "বাঁধ আবার সবুজ করতে দ্রুত অনেক গাছ দেয়।"),
    mcq("Why can cloned plants all be wiped out by one disease?", ["They are genetically identical, so none has natural resistance the others lack", "Clones are always weak", "Diseases prefer clones' colour", "Clones cannot photosynthesise"], 0,
        "Genetic variety is a population's insurance policy.",
        "একটা রোগে ক্লোন-করা সব গাছ কেন শেষ হয়ে যেতে পারে?", ["জিনগতভাবে হুবহু এক, তাই কারও এমন প্রাকৃতিক প্রতিরোধ নেই যা অন্যদের নেই", "ক্লোন সবসময় দুর্বল", "রোগ ক্লোনের রং পছন্দ করে", "ক্লোন সালোকসংশ্লেষ করতে পারে না"],
        "জিনগত বৈচিত্র্য জনগোষ্ঠীর বিমার মতো।"),
    mcq("What is 'extinction', and what is one human cause near rivers?", ["The permanent loss of a species; dams and pollution can destroy the only habitat of some fish", "A species moving to a new home", "A species growing larger", "A bridge closing"], 0,
        "Careful design and fish passes help river species survive.",
        "'বিলুপ্তি' কী, আর নদীর কাছে এর একটা মানবিক কারণ কী?", ["একটা প্রজাতির চিরতরে হারিয়ে যাওয়া; বাঁধ আর দূষণ কিছু মাছের একমাত্র বাসস্থান ধ্বংস করতে পারে", "প্রজাতির নতুন বাসায় যাওয়া", "প্রজাতির বড় হওয়া", "সেতু বন্ধ হওয়া"],
        "যত্নশীল নকশা আর মাছের সিঁড়ি নদীর প্রজাতিকে বাঁচতে সাহায্য করে।"),
    mcq("What is the 'water potential' idea used to explain in plants?", ["Why water moves by osmosis from where it is more available to where it is less available", "Why plants are green", "How fast plants grow", "Why flowers smell"], 0,
        "Water moves from soil into roots and up to the leaves along this gradient.",
        "উদ্ভিদে 'জল-বিভব' ধারণা কী ব্যাখ্যা করতে ব্যবহার হয়?", ["অভিস্রবণে জল কেন বেশি-প্রাপ্য জায়গা থেকে কম-প্রাপ্য জায়গায় যায়", "উদ্ভিদ কেন সবুজ", "উদ্ভিদ কত দ্রুত বাড়ে", "ফুলের গন্ধ কেন"],
        "এই ঢাল বরাবর জল মাটি থেকে শিকড়ে আর উপরে পাতায় যায়।"),
    mcq("What do the xylem and phloem each carry?", ["Xylem carries water and minerals up; phloem carries sugars to where they are needed", "Both carry only water", "Xylem carries sugar; phloem carries air", "Both carry blood"], 0,
        "Phloem moves sugar both up and down the plant (translocation).",
        "জাইলেম আর ফ্লোয়েম প্রত্যেকে কী বয়?", ["জাইলেম জল আর খনিজ উপরে নেয়; ফ্লোয়েম শর্করা দরকারি জায়গায় নেয়", "দুটোই শুধু জল বয়", "জাইলেম শর্করা; ফ্লোয়েম বাতাস", "দুটোই রক্ত বয়"],
        "ফ্লোয়েম শর্করা গাছের উপরে-নিচে দুদিকেই নেয় (স্থানান্তর)।"),
    mcq("Why does ringing the bark of a tree (removing a strip all round) eventually kill it?", ["It cuts the phloem, so sugars cannot reach the roots", "It lets in too much air", "It stops the leaves photosynthesising directly", "Bark holds the tree up"], 0,
        "That is why young trees on sites are protected with guards.",
        "গাছের চারপাশ জুড়ে বাকলের একটা ফালি তুলে দিলে শেষ পর্যন্ত গাছ মরে যায় কেন?", ["ফ্লোয়েম কেটে যায়, তাই শর্করা শিকড়ে পৌঁছায় না", "বেশি বাতাস ঢোকে", "সরাসরি পাতার সালোকসংশ্লেষ থামায়", "বাকল গাছকে খাড়া রাখে"],
        "তাই নির্মাণস্থলের চারাগাছ রক্ষাকবচে ঘিরে রাখা হয়।"),
    mcq("Why are 'root protection zones' fenced off around trees near construction?", ["Heavy machines compact soil and cut roots, which can kill trees years later", "Roots are dangerous to workers", "To hide the trees", "Trees need sunlight on roots"], 0,
        "Most tree roots lie in the top 60 cm of soil.",
        "নির্মাণের কাছে গাছের চারপাশে 'শিকড়-সুরক্ষা অঞ্চল' বেড়া দিয়ে ঘেরা হয় কেন?", ["ভারী যন্ত্র মাটি চেপে দেয় আর শিকড় কাটে, যা বছর পরে গাছ মেরে ফেলতে পারে", "শিকড় কর্মীদের জন্য বিপজ্জনক", "গাছ লুকোতে", "শিকড়ে রোদ লাগে"],
        "বেশিরভাগ শিকড় মাটির উপরের 60 cm-এ থাকে।"),
    mcq("What are 'quadrats' and 'transects' together useful for at a bridge site?", ["Measuring how plant species change along a line, such as from riverbank to dry land", "Counting cars", "Measuring rainfall", "Weighing soil"], 0,
        "Repeat surveys show recovery after construction.",
        "সেতুর নির্মাণস্থলে কোয়াড্র্যাট আর ট্রানসেক্ট একসঙ্গে কীসের জন্য কাজের?", ["একটা রেখা বরাবর উদ্ভিদ-প্রজাতি কীভাবে বদলায় মাপতে, যেমন নদীপাড় থেকে শুকনো জমি", "গাড়ি গুনতে", "বৃষ্টি মাপতে", "মাটি ওজন করতে"],
        "বারবার জরিপ নির্মাণের পরে পুনরুদ্ধার দেখায়।"),
    mcq("What does 'abiotic factor' mean? Give one affecting riverbank plants.", ["A non-living factor, such as light level under a bridge deck", "A predator", "A disease", "A competing plant"], 0,
        "Biotic factors are living ones, like grazing animals.",
        "'অজৈব উপাদান' মানে কী? নদীপাড়ের উদ্ভিদে প্রভাব ফেলে এমন একটা বলো।", ["একটা অজীব উপাদান, যেমন সেতুর পাটাতনের নিচে আলোর মাত্রা", "একটা শিকারি", "একটা রোগ", "প্রতিযোগী উদ্ভিদ"],
        "জৈব উপাদান জীবিত, যেমন চরে-খাওয়া প্রাণী।"),
    mcq("What do denitrifying bacteria do in waterlogged soil?", ["Turn nitrates back into nitrogen gas, making the soil less fertile", "Fix nitrogen into the soil", "Make oxygen", "Digest wood"], 0,
        "Good drainage around new embankments keeps soil fertile for planting.",
        "জল-জমা মাটিতে বিনাইট্রীকরণ ব্যাকটেরিয়া কী করে?", ["নাইট্রেটকে আবার নাইট্রোজেন গ্যাসে বদলায়, মাটির উর্বরতা কমে", "মাটিতে নাইট্রোজেন আবদ্ধ করে", "অক্সিজেন বানায়", "কাঠ হজম করে"],
        "নতুন বাঁধের চারপাশে ভালো জলনিকাশ গাছ লাগানোর জন্য মাটি উর্বর রাখে।"),
    mcq("What is 'sustainable development'?", ["Meeting today's needs without stopping future generations meeting theirs", "Building as fast as possible", "Never building anything", "Using up resources quickly"], 0,
        "Long-lasting, low-carbon bridges are part of it.",
        "'টেকসই উন্নয়ন' কী?", ["ভবিষ্যৎ প্রজন্মের প্রয়োজন মেটানোয় বাধা না দিয়ে আজকের প্রয়োজন মেটানো", "যত দ্রুত সম্ভব নির্মাণ", "কখনো কিছু না বানানো", "দ্রুত সম্পদ শেষ করা"],
        "দীর্ঘস্থায়ী, কম-কার্বন সেতু এর অংশ।"),
    mcq("What is the 'carrying capacity' of a habitat?", ["The largest population of a species it can support long-term", "The weight a bridge can carry", "The number of trucks per day", "The size of a nest"], 0,
        "Food, water, space and shelter all set the limit.",
        "একটা বাসস্থানের 'ধারণক্ষমতা' কী?", ["দীর্ঘমেয়াদে একটা প্রজাতির সবচেয়ে বড় যে জনসংখ্যা টিকিয়ে রাখতে পারে", "সেতু কত ওজন বইতে পারে", "দিনে ট্রাকের সংখ্যা", "বাসার মাপ"],
        "খাদ্য, জল, জায়গা আর আশ্রয় সবই সীমা ঠিক করে।"),
    mcq("What does 'interdependence' mean in an ecosystem?", ["Species depend on each other for food, shelter, pollination and more", "Each species lives alone", "Only plants matter", "Animals never interact"], 0,
        "Removing one species can affect many others.",
        "বাস্তুতন্ত্রে 'পারস্পরিক নির্ভরতা' মানে কী?", ["খাদ্য, আশ্রয়, পরাগায়ন আর আরও অনেক কিছুর জন্য প্রজাতিরা পরস্পরের উপর নির্ভর করে", "প্রতিটা প্রজাতি একা থাকে", "শুধু উদ্ভিদই গুরুত্বপূর্ণ", "প্রাণীরা কখনো মেলামেশা করে না"],
        "একটা প্রজাতি সরালে আরও অনেকের উপর প্রভাব পড়তে পারে।"),
    mcq("How do selective weedkillers made from plant hormones work?", ["They are auxin-like chemicals that make broad-leaved weeds grow too fast and die, sparing grasses", "They poison all plants equally", "They block sunlight", "They feed the weeds"], 0,
        "They must be used carefully near rivers to protect wildlife.",
        "উদ্ভিদ-হরমোন থেকে তৈরি বাছাই-আগাছানাশক কীভাবে কাজ করে?", ["অক্সিনের মতো রাসায়নিক, যা চওড়া-পাতার আগাছাকে খুব দ্রুত বাড়িয়ে মেরে ফেলে, ঘাস বাঁচে", "সব গাছকে সমান বিষ দেয়", "সূর্যালোক আটকায়", "আগাছাকে খাওয়ায়"],
        "বন্যপ্রাণী রক্ষায় নদীর কাছে সাবধানে ব্যবহার করতে হয়।"),
    mcq("Why is ethene gas used when fruit is transported long distances?", ["Fruit is picked unripe and ethene ripens it on arrival, reducing damage in transit", "Ethene keeps fruit cold", "Ethene adds vitamins", "Ethene makes fruit heavier"], 0,
        "Good bridges and roads shorten journeys so less fruit spoils.",
        "দূরে ফল পাঠানোর সময় ইথিন গ্যাস ব্যবহার হয় কেন?", ["ফল কাঁচা অবস্থায় তোলা হয় আর পৌঁছানোর পরে ইথিন পাকায়, পথে ক্ষতি কমে", "ইথিন ফল ঠান্ডা রাখে", "ইথিন ভিটামিন যোগ করে", "ইথিন ফল ভারী করে"],
        "ভালো সেতু আর রাস্তা যাত্রা ছোট করে, তাই কম ফল নষ্ট হয়।"),
    mcq("What are gibberellins used for in agriculture?", ["Plant hormones that help seeds germinate and can increase fruit size", "Killing insects", "Making fertiliser", "Stopping plant growth completely"], 0,
        "Brewers also use them to speed up the germination of barley.",
        "কৃষিতে জিবেরেলিন কীসের জন্য ব্যবহার হয়?", ["উদ্ভিদ-হরমোন, যা বীজের অঙ্কুরোদ্গমে সাহায্য করে আর ফলের মাপ বাড়াতে পারে", "পোকা মারতে", "সার বানাতে", "গাছের বৃদ্ধি পুরো থামাতে"],
        "মদ্য-প্রস্তুতকারীরাও যবের অঙ্কুরোদ্গম দ্রুত করতে এটা ব্যবহার করেন।"),
    mcq("What is long-sightedness (hyperopia) and how is it corrected?", ["Near objects look blurred; corrected with a converging (convex) lens", "Far objects look blurred; corrected with a concave lens", "Seeing colours wrongly", "It cannot be corrected"], 0,
        "Many older workers need reading glasses to check drawings.",
        "দূরদৃষ্টি (হাইপারোপিয়া) কী আর কীভাবে সংশোধন হয়?", ["কাছের জিনিস ঝাপসা দেখায়; অভিসারী (উত্তল) লেন্সে সংশোধন", "দূরের জিনিস ঝাপসা; অবতল লেন্সে সংশোধন", "রং ভুল দেখা", "সংশোধন করা যায় না"],
        "অনেক বয়স্ক কর্মীর নকশা দেখতে পড়ার চশমা লাগে।"),
    mcq("What does the cornea do?", ["It is the clear front of the eye that bends (refracts) most of the incoming light", "It controls pupil size", "It turns light into nerve signals", "It makes tears"], 0,
        "Eye protection stops grit from scratching it.",
        "কর্নিয়া কী করে?", ["চোখের সামনের স্বচ্ছ অংশ, যা আসা আলোর বেশিরভাগ বাঁকায় (প্রতিসরণ)", "তারারন্ধ্রের মাপ নিয়ন্ত্রণ করে", "আলোকে স্নায়ু-সংকেতে বদলায়", "চোখের জল বানায়"],
        "চোখের সুরক্ষা কাঁকর থেকে একে আঁচড় লাগা আটকায়।"),
    mcq("What should you do first if cement dust or grit gets into a worker's eye?", ["Rinse the eye with plenty of clean water for at least 10-15 minutes and get help", "Rub the eye hard", "Ignore it", "Put oil in the eye"], 0,
        "Cement is alkaline and can burn the eye - eyewash stations save sight.",
        "একজন কর্মীর চোখে সিমেন্টের ধুলো বা কাঁকর ঢুকলে প্রথমে কী করা উচিত?", ["অন্তত 10-15 মিনিট প্রচুর পরিষ্কার জলে চোখ ধুয়ে সাহায্য নাও", "জোরে চোখ ঘষো", "উপেক্ষা করো", "চোখে তেল দাও"],
        "সিমেন্ট ক্ষারীয় আর চোখ পুড়িয়ে দিতে পারে - চোখ-ধোয়ার জায়গা দৃষ্টি বাঁচায়।"),
)
