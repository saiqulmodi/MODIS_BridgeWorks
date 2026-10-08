"""Class 11 - Biology (Senior Engineer): bone and joint biomechanics, muscles as levers, the
cardiac cycle and ECG, incidence rates of workplace illness, PCR, respiratory quotient,
Hardy-Weinberg genetics, membrane structure, the biochemistry of respiration and photosynthesis,
wood and bone as natural composites, toxicology, ergonomics and biomimetic design."""
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


def bone_stress(force, area, what_en, what_bn):
    s = _c(force / area)
    return _n(f"During a jump, {what_en} carries a compressive force of {force:,} N over a cross-section of {area} mm². What is the stress?",
              f"লাফের সময় {what_bn} {area} mm² প্রস্থচ্ছেদে {force:,} N সংনমন-বল বয়। পীড়ন কত?", s,
              f"σ = F ÷ A = {force:,} ÷ {area} = {s:g} N/mm² - well below bone's compressive strength of about 170 N/mm².",
              f"σ = F ÷ A = {force:,} ÷ {area} = {s:g} N/mm² - হাড়ের প্রায় 170 N/mm² সংনমন-শক্তির অনেক নিচে।",
              (_c(force * area / 1000), _c(area / force * 100), _c(s * 2)), " N/mm²")


def hipforce(mass, mult):
    f = mass * 10 * mult
    return _n(f"When walking, the hip joint carries about {mult} times body weight. What force acts on the hip of a {mass} kg worker? (g = 10 N/kg)",
              f"হাঁটার সময় নিতম্ব-সন্ধি দেহের ওজনের প্রায় {mult} গুণ বয়। {mass} kg-এর একজন কর্মীর নিতম্বে কত বল কাজ করে? (g = 10 N/kg)", f,
              f"Weight = {mass} x 10 = {mass * 10:,} N; x {mult} = {f:,} N. Carrying loads raises this further.",
              f"ওজন = {mass} x 10 = {mass * 10:,} N; x {mult} = {f:,} N। বোঝা বইলে এটা আরও বাড়ে।",
              (mass * 10, mass * mult, f * 2), " N")


def biceps(w, d_load, d_muscle):
    f = _c(w * d_load / d_muscle)
    return _n(f"A worker holds a {w} N tool in the hand, {d_load} cm from the elbow. The biceps attaches {d_muscle} cm from the elbow. What force must the biceps provide? (ignore the arm's own weight)",
              f"একজন কর্মী কনুই থেকে {d_load} cm দূরে হাতে {w} N-এর একটা যন্ত্র ধরে আছেন। বাইসেপ কনুই থেকে {d_muscle} cm দূরে যুক্ত। বাইসেপকে কত বল দিতে হবে? (বাহুর নিজের ওজন বাদ)", f,
              f"Moments about the elbow: F x {d_muscle} = {w} x {d_load}, so F = {f:g} N - the arm is a third-class lever that trades force for speed.",
              f"কনুইয়ের সাপেক্ষে ভ্রামক: F x {d_muscle} = {w} x {d_load}, তাই F = {f:g} N - বাহু তৃতীয় শ্রেণির লিভার, গতির বিনিময়ে বল দেয়।",
              (w, _c(w * d_muscle / d_load), _c(w + d_load)), " N")


def ecg(rr):
    r = _c(60 / rr)
    return _n(f"On a worker's ECG, the time between two R peaks is {rr:g} s. What is the heart rate?",
              f"একজন কর্মীর ইসিজি-তে দুটো R-চূড়ার মধ্যে সময় {rr:g} s। হৃৎস্পন্দন কত?", r,
              f"Heart rate = 60 ÷ {rr:g} = {r:g} beats per minute.",
              f"হৃৎস্পন্দন = 60 ÷ {rr:g} = মিনিটে {r:g}টি স্পন্দন।",
              (_c(rr * 60), _c(100 * rr), _c(r / 2)), " bpm", " স্পন্দন/মিনিট")


def incidence(cases, workers, what_en, what_bn):
    r = _c(cases * 1000 / workers)
    return _n(f"In a year, {cases} cases of {what_en} were reported among {workers:,} construction workers. What is the incidence rate per 1,000 workers?",
              f"এক বছরে {workers:,} জন নির্মাণ-শ্রমিকের মধ্যে {what_bn}-এর {cases}টি ঘটনা জানা গেল। প্রতি 1,000 শ্রমিকে ঘটনার হার কত?", r,
              f"{cases} ÷ {workers:,} x 1,000 = {r:g} per 1,000 workers per year.",
              f"{cases} ÷ {workers:,} x 1,000 = প্রতি বছর প্রতি 1,000 শ্রমিকে {r:g}।",
              (_c(cases * 100 / workers), _c(workers / cases), _c(r * 10)))


def pcr(start, cycles):
    r = start * 2 ** cycles
    return _n(f"PCR doubles a DNA sample each cycle. Starting with {start} cop{'y' if start == 1 else 'ies'}, how many are there after {cycles} cycles?",
              f"পিসিআর প্রতি চক্রে ডিএনএ নমুনা দ্বিগুণ করে। {start}টি কপি থেকে শুরু করে {cycles}টি চক্রের পরে কতগুলো?", r,
              f"{start} x 2^{cycles} = {r:,}. Tiny traces of DNA can be multiplied enough to test.",
              f"{start} x 2^{cycles} = {r:,}। ডিএনএ-র খুদে চিহ্নও পরীক্ষার মতো যথেষ্ট বাড়ানো যায়।",
              (start * 2 * cycles, start + 2 ** cycles if start + 2 ** cycles != r else r + 8, r // 2))


def rq(co2, o2):
    r = _c(co2 / o2)
    fuel_en = "carbohydrate" if abs(r - 1) < 0.05 else "fat" if r < 0.8 else "a mixture, mostly protein or mixed fuels"
    fuel_bn = "কার্বোহাইড্রেট" if abs(r - 1) < 0.05 else "চর্বি" if r < 0.8 else "মিশ্রণ, প্রধানত প্রোটিন বা মিশ্র জ্বালানি"
    return _n(f"A resting worker produces {co2:g} dm³ of CO2 while using {o2:g} dm³ of O2. What is the respiratory quotient (RQ)?",
              f"বিশ্রামরত একজন কর্মী {o2:g} dm³ O2 খরচ করে {co2:g} dm³ CO2 তৈরি করেন। শ্বসন-ভাগফল (আরকিউ) কত?", r,
              f"RQ = CO2 produced ÷ O2 used = {co2:g} ÷ {o2:g} = {r:g}, suggesting the main fuel is {fuel_en}.",
              f"আরকিউ = তৈরি CO2 ÷ খরচ O2 = {co2:g} ÷ {o2:g} = {r:g}, বোঝায় প্রধান জ্বালানি {fuel_bn}।",
              (_c(o2 / co2), _c(co2 * o2), _c(r + 0.3)))


def hw(q2_pct):
    q = _c((q2_pct / 100) ** 0.5)
    p = _c(1 - q)
    het = _c(2 * p * q * 100)
    return _n(f"In a population, {q2_pct:g}% of people show a recessive condition (aa). Using Hardy-Weinberg, what percentage are carriers (Aa)?",
              f"একটা জনগোষ্ঠীতে {q2_pct:g}% মানুষের একটা প্রচ্ছন্ন অবস্থা (aa)। হার্ডি-ভাইনবার্গ ধরে কত শতাংশ বাহক (Aa)?", het,
              f"q² = {q2_pct / 100:g}, so q = {q:g} and p = {p:g}; carriers = 2pq = {het:g}%.",
              f"q² = {q2_pct / 100:g}, তাই q = {q:g} আর p = {p:g}; বাহক = 2pq = {het:g}%।",
              (_c(q * 100), _c(p * 100), _c(q2_pct * 2)), "%")


ITEMS = (
    bone_stress(3000, 300, "a shin bone (tibia)", "পায়ের নলার হাড় (টিবিয়া)"), bone_stress(5000, 400, "a thigh bone (femur)", "উরুর হাড় (ফিমার)"),
    bone_stress(1200, 150, "a forearm bone", "বাহুর নিচের হাড়"), bone_stress(4500, 500, "a spinal vertebra", "মেরুদণ্ডের একটা কশেরুকা"),
    hipforce(70, 3), hipforce(60, 4), hipforce(80, 4), hipforce(55, 5),
    biceps(50, 35, 5), biceps(30, 30, 4), biceps(100, 40, 5), biceps(20, 36, 4),
    ecg(0.8), ecg(0.6), ecg(1.0), ecg(0.5), ecg(0.75),
    incidence(12, 4000, "occupational asthma", "পেশাগত হাঁপানি"), incidence(60, 15000, "back injuries", "পিঠের আঘাত"),
    incidence(6, 2400, "noise-induced hearing loss", "শব্দজনিত শ্রবণক্ষতি"), incidence(30, 6000, "dermatitis from cement", "সিমেন্টে চর্মরোগ"),
    pcr(1, 10), pcr(10, 20), pcr(5, 8), pcr(2, 15),
    rq(10, 10), rq(7, 10), rq(5.4, 6), rq(16, 20),
    hw(1), hw(4), hw(9), hw(16), hw(25),
    bone_stress(2400, 200, "a collarbone", "কণ্ঠার হাড়"), biceps(40, 32, 4), ecg(0.4), pcr(3, 12),
    incidence(9, 1800, "heat illness", "তাপজনিত অসুস্থতা"), hipforce(65, 6),
    mcq("What is bone mainly made of that gives it both strength and toughness?", ["A composite of collagen fibres (tough) and calcium phosphate mineral (stiff and hard)", "Pure calcium only", "Keratin like hair", "Fat and water"], 0,
        "Like reinforced concrete: stiff mineral plus tough fibres.",
        "হাড় প্রধানত কী দিয়ে তৈরি, যা একে শক্তি আর দৃঢ়তা-সহনশীলতা দুটোই দেয়?", ["কোলাজেন-তন্তু (মজবুত) আর ক্যালসিয়াম ফসফেট খনিজের (শক্ত আর কঠিন) যৌগিক উপাদান", "শুধু বিশুদ্ধ ক্যালসিয়াম", "চুলের মতো কেরাটিন", "চর্বি আর জল"],
        "রিইনফোর্সড কংক্রিটের মতো: শক্ত খনিজ আর মজবুত তন্তু।"),
    mcq("Why is bone stronger in compression than in tension?", ["Its mineral crystals resist crushing well, while cracks open more easily under tension", "Bone has no strength in compression", "Tension makes bone grow", "It is equally strong both ways"], 0,
        "Most fractures start on the tension side of a bent bone.",
        "হাড় টানের চেয়ে সংনমনে শক্ত কেন?", ["এর খনিজ কেলাস চূর্ণ হওয়া ভালো রোধ করে, আর টানে ফাটল সহজে খোলে", "সংনমনে হাড়ের শক্তি নেই", "টানে হাড় বাড়ে", "দুদিকেই সমান শক্ত"],
        "বেশিরভাগ ফাটল বাঁকা হাড়ের টানের দিকে শুরু হয়।"),
    mcq("What does 'Wolff's law' say about bone?", ["Bone remodels to become stronger where it is loaded and weaker where it is not", "Bones never change after childhood", "Bones get weaker with exercise", "Wolves have the strongest bones"], 0,
        "Astronauts lose bone mass in weightlessness; weight-bearing exercise builds it.",
        "'উলফের সূত্র' হাড় নিয়ে কী বলে?", ["যেখানে বোঝা পড়ে সেখানে হাড় নতুন করে গড়ে শক্ত হয়, যেখানে পড়ে না সেখানে দুর্বল হয়", "শৈশবের পরে হাড় বদলায় না", "ব্যায়ামে হাড় দুর্বল হয়", "নেকড়ের হাড় সবচেয়ে শক্ত"],
        "ওজনহীনতায় মহাকাশচারীরা হাড়ের ভর হারান; ভার-বহনকারী ব্যায়াম তা গড়ে।"),
    mcq("What is 'osteoporosis'?", ["A condition where bones lose mass and become porous and fragile", "A bone infection", "A type of joint", "Extra-strong bone"], 0,
        "Calcium, vitamin D and exercise help prevent it.",
        "'অস্টিওপোরোসিস' কী?", ["যে অবস্থায় হাড় ভর হারিয়ে ছিদ্রময় আর ভঙ্গুর হয়", "হাড়ের সংক্রমণ", "এক রকম অস্থিসন্ধি", "অতি-শক্ত হাড়"],
        "ক্যালসিয়াম, ভিটামিন ডি আর ব্যায়াম এটা ঠেকাতে সাহায্য করে।"),
    mcq("Why is the inside of the femur's head filled with a lattice of spongy bone?", ["The struts line up with stress paths, giving strength with little weight - like a truss", "To store fat only", "To make blood cells only", "It has no purpose"], 0,
        "Engineers have compared it to a crane's lattice jib.",
        "উরুর হাড়ের মাথার ভেতরটা স্পঞ্জের মতো জাফরি-হাড়ে ভরা কেন?", ["খুঁটিগুলো পীড়নের পথ বরাবর সাজানো, অল্প ওজনে শক্তি দেয় - ট্রাসের মতো", "শুধু চর্বি জমাতে", "শুধু রক্তকণিকা বানাতে", "কোনো উদ্দেশ্য নেই"],
        "প্রকৌশলীরা একে ক্রেনের জাফরি-বাহুর সঙ্গে তুলনা করেছেন।"),
    mcq("What does cartilage in a joint do?", ["Provides a smooth, low-friction, shock-absorbing surface between bones", "Joins muscle to bone", "Makes red blood cells", "Stores calcium"], 0,
        "Synovial fluid lubricates it - nature's bearing.",
        "অস্থিসন্ধির তরুণাস্থি কী করে?", ["হাড়ের মধ্যে মসৃণ, কম-ঘর্ষণের, ধাক্কা-শোষক তল দেয়", "পেশিকে হাড়ে জোড়ে", "লোহিতকণিকা বানায়", "ক্যালসিয়াম জমায়"],
        "সাইনোভিয়াল তরল একে পিচ্ছিল রাখে - প্রকৃতির বিয়ারিং।"),
    mcq("How is a knee joint like a bridge bearing?", ["Both allow controlled movement while transferring large loads with low friction", "Both are made of steel", "Both never wear out", "Neither carries load"], 0,
        "Both wear over decades and may need replacement.",
        "হাঁটুর সন্ধি কীভাবে সেতুর বিয়ারিংয়ের মতো?", ["দুটোই কম ঘর্ষণে বড় বোঝা স্থানান্তর করতে করতে নিয়ন্ত্রিত নড়াচড়া করতে দেয়", "দুটোই ইস্পাতের", "দুটোই কখনো ক্ষয়ে না", "কোনোটাই বোঝা বয় না"],
        "দুটোই কয়েক দশকে ক্ষয়ে যায় আর বদলাতে হতে পারে।"),
    mcq("Why is the human arm a 'third-class lever'?", ["The effort (muscle) is between the pivot (elbow) and the load (hand)", "The pivot is in the middle", "The load is in the middle", "It is not a lever"], 0,
        "It needs a large muscle force but moves the hand quickly over a big range.",
        "মানুষের বাহু 'তৃতীয় শ্রেণির লিভার' কেন?", ["প্রয়াস (পেশি) পিভট (কনুই) আর বোঝা (হাত)-এর মাঝখানে", "পিভট মাঝখানে", "বোঝা মাঝখানে", "এটা লিভার নয়"],
        "বড় পেশি-বল লাগে, কিন্তু হাতকে বড় পরিসরে দ্রুত নাড়ায়।"),
    mcq("What is the 'sliding filament' model of muscle contraction?", ["Actin and myosin filaments slide past each other, using ATP, shortening the muscle", "Muscles stretch to contract", "Bones push muscles", "Muscles fill with air"], 0,
        "Calcium ions trigger the process.",
        "পেশি-সংকোচনের 'পিছল-তন্তু' মডেল কী?", ["অ্যাকটিন আর মায়োসিন তন্তু এটিপি খরচ করে পরস্পরের পাশ দিয়ে পিছলায়, পেশি ছোট হয়", "সংকুচিত হতে পেশি টানটান হয়", "হাড় পেশিকে ঠেলে", "পেশি বাতাসে ভরে"],
        "ক্যালসিয়াম আয়ন প্রক্রিয়াটা শুরু করে।"),
    mcq("Why do muscles 'fatigue' during long repetitive work?", ["ATP supply falls behind demand and waste products build up, reducing force", "Muscles run out of bones", "Muscles turn to fat instantly", "Fatigue is imaginary"], 0,
        "Job rotation and breaks reduce fatigue-related injuries.",
        "দীর্ঘ পুনরাবৃত্ত কাজে পেশি 'ক্লান্ত' হয় কেন?", ["এটিপি-র জোগান চাহিদার পিছনে পড়ে আর বর্জ্য জমে, বল কমে", "পেশির হাড় ফুরিয়ে যায়", "পেশি তখনই চর্বি হয়", "ক্লান্তি কাল্পনিক"],
        "কাজ বদলাবদলি আর বিরতি ক্লান্তিজনিত আঘাত কমায়।"),
    mcq("What is the 'cardiac cycle'?", ["The sequence of contraction (systole) and relaxation (diastole) of the heart in one beat", "A bicycle for heart patients", "The route of blood to the lungs only", "A type of exercise"], 0,
        "Valves open and close in order to keep blood moving one way.",
        "'হৃৎচক্র' কী?", ["এক স্পন্দনে হৃৎপিণ্ডের সংকোচন (সিস্টোল) আর প্রসারণ (ডায়াস্টোল)-এর ক্রম", "হৃদরোগীর সাইকেল", "শুধু ফুসফুসে রক্তের পথ", "এক রকম ব্যায়াম"],
        "রক্ত একদিকে চালাতে ভালভ ক্রমে খোলে আর বন্ধ হয়।"),
    mcq("What does an ECG measure?", ["The electrical activity of the heart", "Blood sugar", "Lung volume", "Bone density"], 0,
        "The QRS complex shows the ventricles contracting.",
        "ইসিজি কী মাপে?", ["হৃৎপিণ্ডের বৈদ্যুতিক ক্রিয়া", "রক্তে শর্করা", "ফুসফুসের আয়তন", "হাড়ের ঘনত্ব"],
        "কিউআরএস জটিল দেখায় নিলয় সংকুচিত হচ্ছে।"),
    mcq("What does the sinoatrial node (SAN) do?", ["Acts as the heart's natural pacemaker, starting each beat", "Pumps blood to the lungs", "Filters blood", "Stores oxygen"], 0,
        "Artificial pacemakers take over if it fails.",
        "সাইনোঅ্যাট্রিয়াল নোড (এসএএন) কী করে?", ["হৃৎপিণ্ডের প্রাকৃতিক ছন্দ-নির্ধারক হিসেবে প্রতিটা স্পন্দন শুরু করে", "ফুসফুসে রক্ত পাম্প করে", "রক্ত ছাঁকে", "অক্সিজেন জমায়"],
        "এটা ব্যর্থ হলে কৃত্রিম পেসমেকার কাজ নেয়।"),
    mcq("What is an AED, and why do large bridge sites keep one?", ["An automated external defibrillator that can restart a heart in cardiac arrest - every minute counts", "A type of crane", "A fire extinguisher", "A noise meter"], 0,
        "It talks the user through each step; CPR plus early defibrillation saves lives.",
        "এইডি কী, আর বড় সেতু-নির্মাণস্থলে কেন রাখা হয়?", ["স্বয়ংক্রিয় বাহ্যিক ডিফিব্রিলেটর, যা হৃৎস্পন্দন থেমে গেলে আবার চালু করতে পারে - প্রতিটা মিনিট জরুরি", "এক রকম ক্রেন", "অগ্নিনির্বাপক", "শব্দ-মাপক"],
        "প্রতিটা ধাপে ব্যবহারকারীকে বলে দেয়; সিপিআর আর তাড়াতাড়ি ডিফিব্রিলেশন প্রাণ বাঁচায়।"),
    mcq("What is the 'fluid mosaic' model of the cell membrane?", ["A phospholipid bilayer with proteins floating in it like tiles in a moving mosaic", "A rigid wall of cellulose", "A layer of fat only", "A sheet of DNA"], 0,
        "Membrane proteins act as channels, carriers and receptors.",
        "কোষপর্দার 'তরল মোজাইক' মডেল কী?", ["ফসফোলিপিডের দ্বিস্তর, যাতে প্রোটিন চলমান মোজাইকের টুকরোর মতো ভাসে", "সেলুলোজের শক্ত দেয়াল", "শুধু চর্বির স্তর", "ডিএনএ-র চাদর"],
        "পর্দার প্রোটিন নালি, বাহক আর গ্রাহকের কাজ করে।"),
    mcq("What is 'facilitated diffusion'?", ["Diffusion of molecules down a concentration gradient through protein channels or carriers, without using ATP", "Movement using ATP", "Water moving through a membrane only", "Breathing"], 0,
        "Glucose enters many cells this way.",
        "'সহায়ক ব্যাপন' কী?", ["এটিপি ছাড়াই প্রোটিন-নালি বা বাহকের মধ্য দিয়ে গাঢ়ত্বের ঢাল বেয়ে অণুর ব্যাপন", "এটিপি খরচ করে চলাচল", "শুধু পর্দা দিয়ে জলের চলাচল", "শ্বাস নেওয়া"],
        "অনেক কোষে গ্লুকোজ এভাবে ঢোকে।"),
    mcq("What are the main stages of aerobic respiration?", ["Glycolysis, the link reaction, the Krebs cycle and oxidative phosphorylation", "Only glycolysis", "Photosynthesis and digestion", "Fermentation only"], 0,
        "Most ATP is made in the final stage in the mitochondria.",
        "সবাত শ্বসনের প্রধান ধাপগুলো কী?", ["গ্লাইকোলাইসিস, সংযোগ-বিক্রিয়া, ক্রেবস চক্র আর জারণ-ফসফোরাইলেশন", "শুধু গ্লাইকোলাইসিস", "সালোকসংশ্লেষ আর হজম", "শুধু সন্ধান"],
        "বেশিরভাগ এটিপি মাইটোকন্ড্রিয়ার শেষ ধাপে তৈরি হয়।"),
    mcq("Where does glycolysis take place?", ["In the cytoplasm", "In the nucleus", "In the chloroplast", "In the cell wall"], 0,
        "It splits glucose into pyruvate and makes a little ATP without oxygen.",
        "গ্লাইকোলাইসিস কোথায় ঘটে?", ["সাইটোপ্লাজমে", "নিউক্লিয়াসে", "ক্লোরোপ্লাস্টে", "কোষপ্রাচীরে"],
        "অক্সিজেন ছাড়াই গ্লুকোজকে পাইরুভেটে ভেঙে অল্প এটিপি বানায়।"),
    mcq("What is the role of oxygen at the end of the electron transport chain?", ["It is the final electron acceptor, forming water", "It makes glucose", "It breaks down fat directly", "It carries ATP"], 0,
        "Without oxygen the chain stops - which is why cyanide and carbon monoxide are so dangerous.",
        "ইলেকট্রন-পরিবহন শৃঙ্খলের শেষে অক্সিজেনের ভূমিকা কী?", ["শেষ ইলেকট্রন-গ্রাহক, জল তৈরি করে", "গ্লুকোজ বানায়", "সরাসরি চর্বি ভাঙে", "এটিপি বয়"],
        "অক্সিজেন না থাকলে শৃঙ্খল থামে - তাই সায়ানাইড আর কার্বন মনোক্সাইড এত বিপজ্জনক।"),
    mcq("What are the two main stages of photosynthesis?", ["The light-dependent reactions and the light-independent (Calvin) cycle", "Glycolysis and Krebs", "Osmosis and diffusion", "Germination and growth"], 0,
        "Light reactions make ATP and reduced NADP; the Calvin cycle fixes CO2 into sugar.",
        "সালোকসংশ্লেষের দুটো প্রধান ধাপ কী?", ["আলোক-নির্ভর বিক্রিয়া আর আলোক-নিরপেক্ষ (ক্যালভিন) চক্র", "গ্লাইকোলাইসিস আর ক্রেবস", "অভিস্রবণ আর ব্যাপন", "অঙ্কুরোদ্গম আর বৃদ্ধি"],
        "আলোক-বিক্রিয়া এটিপি আর বিজারিত এনএডিপি বানায়; ক্যালভিন চক্র CO2-কে শর্করায় আবদ্ধ করে।"),
    mcq("What is the enzyme RuBisCO famous for?", ["Fixing CO2 in the Calvin cycle - it may be the most abundant protein on Earth", "Digesting fat", "Copying DNA", "Making bone"], 0,
        "Scientists study it to help crops grow faster.",
        "রুবিসকো এনজাইম কীসের জন্য বিখ্যাত?", ["ক্যালভিন চক্রে CO2 আবদ্ধ করা - সম্ভবত পৃথিবীর সবচেয়ে প্রচুর প্রোটিন", "চর্বি হজম", "ডিএনএ নকল", "হাড় তৈরি"],
        "ফসল দ্রুত বাড়াতে বিজ্ঞানীরা এটা নিয়ে গবেষণা করেন।"),
    mcq("Why is wood described as a natural composite material?", ["Strong cellulose fibres are held in a matrix of lignin, much like fibre-reinforced polymer", "Wood is pure cellulose", "Wood is a metal", "Wood has no structure"], 0,
        "That is why wood is much stronger along the grain than across it.",
        "কাঠকে প্রাকৃতিক যৌগিক উপাদান বলা হয় কেন?", ["শক্ত সেলুলোজ-তন্তু লিগনিনের আধারে আটকানো, অনেকটা তন্তু-শক্ত পলিমারের মতো", "কাঠ বিশুদ্ধ সেলুলোজ", "কাঠ একটা ধাতু", "কাঠের গঠন নেই"],
        "তাই কাঠ আঁশ বরাবর আড়াআড়ির চেয়ে অনেক বেশি শক্ত।"),
    mcq("What is 'glulam' and why is it used for timber footbridges?", ["Glued laminated timber - thin layers glued together into large, strong, reliable beams", "Glass and aluminium", "Glue only", "A type of concrete"], 0,
        "Gluing spreads out natural defects, making strength more predictable.",
        "'গ্লুল্যাম' কী আর কাঠের পায়ে-চলা সেতুতে কেন ব্যবহার হয়?", ["আঠা-দেওয়া স্তরিত কাঠ - পাতলা স্তর আঠা দিয়ে জুড়ে বড়, শক্ত, ভরসার কড়ি", "কাচ আর অ্যালুমিনিয়াম", "শুধু আঠা", "এক রকম কংক্রিট"],
        "আঠায় জোড়ায় প্রাকৃতিক ত্রুটি ছড়িয়ে যায়, শক্তি বেশি অনুমানযোগ্য হয়।"),
    mcq("What is PCR used for?", ["Making millions of copies of a DNA sequence so it can be studied or identified", "Measuring blood pressure", "Building proteins", "Counting cells"], 0,
        "It is used in disease testing and forensics.",
        "পিসিআর কীসের জন্য ব্যবহার হয়?", ["একটা ডিএনএ-ক্রমের লক্ষ লক্ষ কপি বানাতে, যাতে গবেষণা বা শনাক্ত করা যায়", "রক্তচাপ মাপা", "প্রোটিন তৈরি", "কোষ গোনা"],
        "রোগ-পরীক্ষা আর ফরেনসিকে ব্যবহার হয়।"),
    mcq("What is 'gel electrophoresis'?", ["Separating DNA fragments by size using an electric field through a gel", "Freezing DNA", "Painting DNA", "Making gels for hair"], 0,
        "Smaller fragments travel further through the gel.",
        "'জেল-তড়িৎসঞ্চালন' কী?", ["জেলের মধ্য দিয়ে বৈদ্যুতিক ক্ষেত্রে মাপ অনুযায়ী ডিএনএ-র টুকরো আলাদা করা", "ডিএনএ জমানো", "ডিএনএ রং করা", "চুলের জেল বানানো"],
        "ছোট টুকরো জেলের মধ্য দিয়ে বেশি দূর যায়।"),
    mcq("What does the Hardy-Weinberg principle assume about a population?", ["No mutation, no selection, no migration, random mating and a large size, so allele frequencies stay constant", "Constant change", "Only one allele exists", "Populations always shrink"], 0,
        "Departures from it show that evolution is happening.",
        "হার্ডি-ভাইনবার্গ নীতি জনগোষ্ঠী নিয়ে কী ধরে নেয়?", ["মিউটেশন, নির্বাচন, অভিবাসন নেই, এলোমেলো মিলন আর বড় আকার, তাই অ্যালিলের হার স্থির থাকে", "সবসময় বদল", "শুধু একটা অ্যালিল আছে", "জনগোষ্ঠী সবসময় ছোট হয়"],
        "এর থেকে বিচ্যুতি দেখায় বিবর্তন ঘটছে।"),
    mcq("What is 'genetic drift'?", ["Random changes in allele frequencies, strongest in small populations", "Genes moving between cells", "Mutation caused by radiation", "Selective breeding"], 0,
        "Small isolated populations, such as on islands, are most affected.",
        "'জিনগত সরণ' কী?", ["অ্যালিলের হারে এলোমেলো বদল, ছোট জনগোষ্ঠীতে সবচেয়ে জোরালো", "কোষের মধ্যে জিনের চলাচল", "বিকিরণে মিউটেশন", "নির্বাচিত প্রজনন"],
        "দ্বীপের মতো ছোট বিচ্ছিন্ন জনগোষ্ঠী সবচেয়ে প্রভাবিত।"),
    mcq("Why can a highway that splits a habitat lead to genetic problems in small animals?", ["Isolated groups become small, increasing inbreeding and genetic drift", "Highways create new species instantly", "Animals become larger", "Genes are destroyed by traffic noise"], 0,
        "Green bridges and underpasses restore gene flow.",
        "বাসস্থান ভাগ-করা মহাসড়ক ছোট প্রাণীদের জিনগত সমস্যায় ফেলতে পারে কেন?", ["বিচ্ছিন্ন দলগুলো ছোট হয়, অন্তঃপ্রজনন আর জিনগত সরণ বাড়ে", "মহাসড়ক তখনই নতুন প্রজাতি বানায়", "প্রাণীরা বড় হয়", "যানবাহনের শব্দে জিন নষ্ট হয়"],
        "সবুজ সেতু আর সুড়ঙ্গপথ জিন-প্রবাহ ফেরায়।"),
    mcq("What is 'ecological succession'?", ["The gradual change in species in an area over time, for example from bare ground to woodland", "A list of animals in order of size", "A food chain", "Animals moving each season"], 0,
        "Bare embankments go through succession unless managed.",
        "'বাস্তুতান্ত্রিক উত্তরাধিকার' কী?", ["সময়ের সঙ্গে একটা জায়গায় প্রজাতির ধীর বদল, যেমন খালি মাটি থেকে বনভূমি", "আকারের ক্রমে প্রাণীর তালিকা", "খাদ্যশৃঙ্খল", "প্রতি মরসুমে প্রাণীর সরে যাওয়া"],
        "দেখভাল না করলে খালি বাঁধে উত্তরাধিকার চলে।"),
    mcq("What are 'pioneer species'?", ["The first organisms to colonise bare ground, such as lichens and mosses", "The largest trees", "Animals that hunt at night", "Species brought by humans only"], 0,
        "They start building soil for later species.",
        "'অগ্রণী প্রজাতি' কী?", ["খালি মাটিতে প্রথম বসতি গড়া জীব, যেমন লাইকেন আর শ্যাওলা", "সবচেয়ে বড় গাছ", "রাতে শিকার করা প্রাণী", "শুধু মানুষের আনা প্রজাতি"],
        "পরের প্রজাতির জন্য মাটি গড়া শুরু করে।"),
    mcq("What does 'LD50' mean in toxicology?", ["The dose that kills 50% of a test population - a measure of how toxic a substance is", "A light-duty truck", "The legal driving limit", "A type of concrete"], 0,
        "A lower LD50 means a more toxic substance.",
        "বিষবিজ্ঞানে 'এলডি50' মানে কী?", ["যে মাত্রায় পরীক্ষার জনগোষ্ঠীর 50% মারা যায় - পদার্থ কতটা বিষাক্ত তার মাপ", "হালকা ট্রাক", "আইনি গাড়ি-চালানোর সীমা", "এক রকম কংক্রিট"],
        "এলডি50 কম মানে বেশি বিষাক্ত পদার্থ।"),
    mcq("What is a 'workplace exposure limit' (WEL)?", ["The maximum average concentration of a hazardous substance a worker may breathe over a set time", "The longest shift allowed", "The noise from a radio", "The weight limit of a crane"], 0,
        "Silica dust and welding fumes have strict limits.",
        "'কর্মস্থলে সংস্পর্শের সীমা' কী?", ["নির্দিষ্ট সময়ে একজন কর্মী শ্বাসে একটা বিপজ্জনক পদার্থের সর্বোচ্চ যে গড় গাঢ়ত্ব নিতে পারেন", "অনুমোদিত সবচেয়ে লম্বা পালা", "রেডিওর শব্দ", "ক্রেনের ওজন-সীমা"],
        "সিলিকা-ধুলো আর ঝালাইয়ের ধোঁয়ার কড়া সীমা আছে।"),
    mcq("What is the 'hierarchy of controls' for a health hazard on site?", ["Eliminate, substitute, engineer it out, use admin controls, and only then rely on PPE", "PPE first, then nothing else", "Ignore it unless someone is hurt", "Only training"], 0,
        "For silica dust: wet cutting and extraction come before masks.",
        "নির্মাণস্থলে স্বাস্থ্য-বিপদের জন্য 'নিয়ন্ত্রণের ক্রমতালিকা' কী?", ["দূর করো, বদলাও, প্রকৌশলে সরাও, প্রশাসনিক নিয়ন্ত্রণ দাও, তবেই সুরক্ষা-পোশাকের উপর নির্ভর করো", "আগে সুরক্ষা-পোশাক, তারপর কিছু না", "কেউ আহত না হলে উপেক্ষা", "শুধু প্রশিক্ষণ"],
        "সিলিকা-ধুলোর জন্য: মুখোশের আগে ভেজা কাটা আর নিষ্কাশন।"),
    mcq("What does 'ergonomics' aim to do?", ["Design tasks, tools and workplaces to fit people, reducing strain and injury", "Make machines faster only", "Reduce wages", "Paint offices"], 0,
        "Adjustable crane cab seats and good tool handles are ergonomic design.",
        "'এরগোনমিক্স' কী করতে চায়?", ["মানুষের উপযোগী করে কাজ, যন্ত্র আর কর্মস্থলের নকশা, চাপ আর আঘাত কমাতে", "শুধু যন্ত্র দ্রুত করতে", "মজুরি কমাতে", "অফিস রং করতে"],
        "সামঞ্জস্যযোগ্য ক্রেন-কেবিনের আসন আর ভালো যন্ত্রের হাতল এরগোনমিক নকশা।"),
    mcq("What is a 'musculoskeletal disorder' (MSD)?", ["An injury or pain in muscles, tendons, joints or the back, often from repetitive or awkward work", "A broken machine", "A skin rash", "A lung disease"], 0,
        "MSDs are among the most common work-related illnesses in construction.",
        "'পেশি-কঙ্কালের ব্যাধি' (এমএসডি) কী?", ["পেশি, কণ্ডরা, অস্থিসন্ধি বা পিঠে আঘাত বা ব্যথা, প্রায়ই পুনরাবৃত্ত বা বেখাপ্পা কাজ থেকে", "ভাঙা যন্ত্র", "চামড়ার ফুসকুড়ি", "ফুসফুসের রোগ"],
        "নির্মাণে এমএসডি সবচেয়ে সাধারণ কাজ-সংক্রান্ত অসুখগুলোর একটা।"),
    mcq("What is 'hand-arm vibration syndrome' (HAVS)?", ["Damage to nerves, blood vessels and joints from long use of vibrating tools like breakers", "A dance move", "A type of glove", "A noise problem only"], 0,
        "Low-vibration tools and limiting trigger time prevent it.",
        "'হাত-বাহু কম্পন রোগ' (এইচএভিএস) কী?", ["ব্রেকারের মতো কম্পনশীল যন্ত্র দীর্ঘ ব্যবহারে স্নায়ু, রক্তনালী আর অস্থিসন্ধির ক্ষতি", "এক রকম নাচ", "এক রকম দস্তানা", "শুধু শব্দের সমস্যা"],
        "কম-কম্পনের যন্ত্র আর ট্রিগার-সময় সীমিত রাখলে ঠেকানো যায়।"),
    mcq("What is 'epidemiology'?", ["The study of how often diseases occur in populations and what causes them", "The study of skin", "The study of epidemics in plants only", "The study of bridges"], 0,
        "It revealed the link between asbestos and lung cancer.",
        "'মহামারীবিদ্যা' কী?", ["জনগোষ্ঠীতে রোগ কত ঘন ঘন হয় আর কী কারণে, তার পাঠ", "চামড়ার পাঠ", "শুধু উদ্ভিদের মহামারীর পাঠ", "সেতুর পাঠ"],
        "এটাই অ্যাসবেস্টস আর ফুসফুসের ক্যান্সারের সম্পর্ক প্রকাশ করেছিল।"),
    mcq("What is the difference between 'incidence' and 'prevalence' of a disease?", ["Incidence counts new cases in a period; prevalence counts all existing cases at a time", "They are the same", "Prevalence counts only deaths", "Incidence counts only children"], 0,
        "Both help plan health services for workforces.",
        "রোগের 'আপতন' আর 'ব্যাপকতা'-র পার্থক্য কী?", ["আপতন একটা সময়ে নতুন ঘটনা গোনে; ব্যাপকতা এক সময়ে বিদ্যমান সব ঘটনা", "দুটো একই", "ব্যাপকতা শুধু মৃত্যু গোনে", "আপতন শুধু শিশু গোনে"],
        "দুটোই কর্মীবাহিনীর স্বাস্থ্য-পরিষেবা পরিকল্পনায় সাহায্য করে।"),
    mcq("What is 'biomimetics' (biomimicry) in engineering?", ["Copying designs and processes from nature to solve human problems", "Painting animals on bridges", "Using live animals in buildings", "Studying biology only"], 0,
        "Velcro, bird-inspired bridge shapes and termite-mound ventilation are examples.",
        "প্রকৌশলে 'জৈব-অনুকরণ' কী?", ["মানুষের সমস্যা সমাধানে প্রকৃতির নকশা আর প্রক্রিয়া নকল করা", "সেতুতে প্রাণী আঁকা", "বাড়িতে জীবন্ত প্রাণী ব্যবহার", "শুধু জীববিদ্যার পাঠ"],
        "ভেলক্রো, পাখি-অনুপ্রাণিত সেতুর আকার আর উইঢিবির বায়ুচলাচল এর উদাহরণ।"),
    mcq("How do termite mounds inspire building ventilation?", ["Their tunnels use natural air currents to keep a steady temperature without machines", "Termites install fans", "Mounds are air-conditioned by people", "They do not inspire anything"], 0,
        "Some buildings use similar passive cooling to save energy.",
        "উইঢিবি কীভাবে বাড়ির বায়ুচলাচলে অনুপ্রেরণা দেয়?", ["এর সুড়ঙ্গ প্রাকৃতিক বায়ুপ্রবাহে যন্ত্র ছাড়াই স্থির তাপমাত্রা রাখে", "উইপোকা পাখা বসায়", "মানুষ ঢিবি শীতাতপ করে", "কিছুতে অনুপ্রেরণা দেয় না"],
        "কিছু বাড়ি শক্তি বাঁচাতে একই রকম নিষ্ক্রিয় শীতলীকরণ ব্যবহার করে।"),
    mcq("What makes spider dragline silk remarkable for engineers?", ["It combines high strength with great stretch, absorbing a lot of energy before breaking", "It is magnetic", "It is heavier than steel", "It never stretches"], 0,
        "Scientists are trying to make synthetic versions for ropes and medical uses.",
        "মাকড়সার টানা-রেশম প্রকৌশলীদের কাছে আশ্চর্য কেন?", ["উচ্চ শক্তির সঙ্গে প্রচুর টান মেশায়, ভাঙার আগে অনেক শক্তি শোষে", "এটা চৌম্বক", "ইস্পাতের চেয়ে ভারী", "কখনো টানে না"],
        "দড়ি আর চিকিৎসার জন্য বিজ্ঞানীরা কৃত্রিম রূপ বানানোর চেষ্টা করছেন।"),
    mcq("What is 'bioremediation'?", ["Using microbes or plants to clean up polluted soil or water", "Repairing bones", "Building with bamboo", "Medical surgery"], 0,
        "Oil-contaminated ground at old industrial bridge sites can be treated this way.",
        "'জৈব-প্রতিকার' কী?", ["দূষিত মাটি বা জল পরিষ্কারে জীবাণু বা উদ্ভিদ ব্যবহার", "হাড় মেরামত", "বাঁশ দিয়ে নির্মাণ", "চিকিৎসা-শল্য"],
        "পুরোনো শিল্প-এলাকার সেতুর জমিতে তেল-দূষণ এভাবে শোধন করা যায়।"),
    mcq("What is 'bio-concrete' (self-healing concrete)?", ["Concrete containing dormant bacteria that make limestone to seal cracks when water gets in", "Concrete made of bones", "Concrete that grows plants", "Concrete that dissolves"], 0,
        "It could reduce maintenance on hard-to-reach structures.",
        "'জৈব-কংক্রিট' (নিজে-সেরে-ওঠা কংক্রিট) কী?", ["সুপ্ত ব্যাকটেরিয়াযুক্ত কংক্রিট, যা জল ঢুকলে চুনাপাথর বানিয়ে ফাটল বোজায়", "হাড় দিয়ে তৈরি কংক্রিট", "গাছ জন্মানো কংক্রিট", "গলে যাওয়া কংক্রিট"],
        "দুর্গম কাঠামোয় রক্ষণাবেক্ষণ কমাতে পারে।"),
    mcq("What is 'microbially induced corrosion' (MIC)?", ["Corrosion speeded up by bacteria, for example sulfate-reducing bacteria in mud around piles", "Corrosion by sunlight", "Rusting in dry air", "Corrosion of plastics"], 0,
        "It can cause surprisingly fast pitting of buried steel.",
        "'জীবাণুজনিত ক্ষয়' (এমআইসি) কী?", ["ব্যাকটেরিয়ায় দ্রুত হওয়া ক্ষয়, যেমন পাইলের চারপাশের কাদায় সালফেট-বিজারক ব্যাকটেরিয়া", "সূর্যালোকে ক্ষয়", "শুকনো বাতাসে মরচে", "প্লাস্টিকের ক্ষয়"],
        "মাটিতে পোঁতা ইস্পাতে আশ্চর্য দ্রুত গর্ত-ক্ষয় ঘটাতে পারে।"),
    mcq("What is 'biofouling' on underwater bridge piers?", ["The build-up of organisms like barnacles, mussels and algae on submerged surfaces", "Fish swimming nearby", "Rust only", "Paint drying"], 0,
        "It adds weight and drag and can hide damage from inspectors.",
        "জলের নিচের সেতু-স্তম্ভে 'জৈব-আবরণ' কী?", ["ডুবন্ত তলে বার্নাকল, ঝিনুক আর শৈবালের মতো জীবের জমে ওঠা", "কাছে মাছের সাঁতার", "শুধু মরচে", "রং শুকোনো"],
        "ওজন আর টান বাড়ায়, আর পরিদর্শকদের থেকে ক্ষতি লুকোতে পারে।"),
    mcq("What does a 'risk assessment' for Weil's disease (leptospirosis) recommend for river workers?", ["Cover cuts, wear gloves and waterproofs, wash before eating, and carry a card describing the risk", "Swim in the river daily", "Drink river water", "Ignore symptoms"], 0,
        "Early treatment with antibiotics is effective, so doctors must know the risk.",
        "নদী-কর্মীদের জন্য ওয়েইলের রোগের (লেপটোস্পাইরোসিস) ঝুঁকি মূল্যায়ন কী সুপারিশ করে?", ["কাটা জায়গা ঢাকো, দস্তানা আর জলরোধী পোশাক পরো, খাওয়ার আগে ধোও, আর ঝুঁকির বিবরণসহ কার্ড রাখো", "রোজ নদীতে সাঁতার", "নদীর জল খাওয়া", "লক্ষণ উপেক্ষা"],
        "তাড়াতাড়ি অ্যান্টিবায়োটিক কার্যকর, তাই ডাক্তারদের ঝুঁকি জানা দরকার।"),
    mcq("What does 'acclimatisation' to heat involve for new site workers?", ["Gradually increasing work in the heat over about a week so the body adapts, for example by sweating sooner", "Working the hardest on day one", "Drinking less water", "Wearing more clothes"], 0,
        "New workers are at highest risk of heat illness in their first days.",
        "নতুন নির্মাণ-কর্মীদের গরমে 'অভিযোজন'-এ কী থাকে?", ["প্রায় এক সপ্তাহ ধরে গরমে কাজ ধীরে বাড়ানো, যাতে শরীর মানিয়ে নেয়, যেমন আগে ঘাম ঝরায়", "প্রথম দিনেই সবচেয়ে কঠোর কাজ", "কম জল খাওয়া", "বেশি পোশাক পরা"],
        "প্রথম কয়েক দিনে নতুন কর্মীদের তাপজনিত অসুস্থতার ঝুঁকি সবচেয়ে বেশি।"),
    mcq("What is 'circadian rhythm' and why does it matter for night-shift bridge crews?", ["The body's roughly 24-hour clock; working against it lowers alertness, especially in the early morning", "A type of music", "The tide timetable", "A heart rhythm only"], 0,
        "Scheduling the riskiest tasks away from 3-5 a.m. improves safety.",
        "'সার্কাডিয়ান ছন্দ' কী আর রাতের পালার সেতু-দলের জন্য কেন জরুরি?", ["শরীরের মোটামুটি 24 ঘণ্টার ঘড়ি; এর বিরুদ্ধে কাজ করলে সতর্কতা কমে, বিশেষত ভোরে", "এক রকম গান", "জোয়ারের সময়সূচি", "শুধু হৃৎছন্দ"],
        "সবচেয়ে ঝুঁকির কাজ ভোর 3-5টা থেকে সরালে নিরাপত্তা বাড়ে।"),
    mcq("What is 'melatonin'?", ["A hormone released in darkness that promotes sleep", "A skin pigment", "A digestive enzyme", "A muscle protein"], 0,
        "Bright light at night suppresses it, disturbing sleep.",
        "'মেলাটোনিন' কী?", ["অন্ধকারে ছাড়া এক হরমোন, যা ঘুম আনে", "চামড়ার রঞ্জক", "পাচক এনজাইম", "পেশির প্রোটিন"],
        "রাতে উজ্জ্বল আলো এটা দমন করে ঘুম ব্যাহত করে।"),
    mcq("Why do hospitals use bone-like titanium lattices made by 3D printing for implants?", ["The porous lattice matches bone stiffness better and lets bone grow into it", "Titanium is cheap", "To make implants heavy", "Lattices dissolve in the body"], 0,
        "Matching stiffness avoids 'stress shielding', where bone weakens beside a stiff implant.",
        "হাসপাতালে ইমপ্ল্যান্টে 3D-প্রিন্টে তৈরি হাড়ের মতো টাইটানিয়াম-জাফরি ব্যবহার হয় কেন?", ["ছিদ্রময় জাফরি হাড়ের দৃঢ়তার সঙ্গে ভালো মেলে আর হাড়কে ভেতরে বাড়তে দেয়", "টাইটানিয়াম সস্তা", "ইমপ্ল্যান্ট ভারী করতে", "জাফরি শরীরে গলে যায়"],
        "দৃঢ়তা মেলালে 'পীড়ন-আড়াল' এড়ায়, যেখানে শক্ত ইমপ্ল্যান্টের পাশে হাড় দুর্বল হয়।"),
    mcq("What is 'stress shielding' around a metal hip implant?", ["The stiff implant carries most of the load, so nearby bone is under-loaded and weakens", "A shield against stress at work", "Extra-strong bone", "A type of armour"], 0,
        "It is Wolff's law in action.",
        "ধাতব নিতম্ব-ইমপ্ল্যান্টের চারপাশে 'পীড়ন-আড়াল' কী?", ["শক্ত ইমপ্ল্যান্ট বেশিরভাগ বোঝা বয়, তাই কাছের হাড়ে কম বোঝা পড়ে আর দুর্বল হয়", "কাজের চাপের বিরুদ্ধে ঢাল", "অতি-শক্ত হাড়", "এক রকম বর্ম"],
        "এটা উলফের সূত্রের বাস্তব রূপ।"),
    mcq("Why is the human spine S-shaped rather than straight?", ["The curves act like a spring, absorbing shocks and balancing the head over the hips", "It is a mistake of nature", "To make people shorter", "Straight spines are stronger"], 0,
        "Good lifting technique keeps these natural curves.",
        "মানুষের মেরুদণ্ড সোজা না হয়ে S-আকারের কেন?", ["বাঁকগুলো স্প্রিংয়ের মতো কাজ করে, ধাক্কা শোষে আর নিতম্বের উপর মাথার ভারসাম্য রাখে", "প্রকৃতির ভুল", "মানুষকে বেঁটে করতে", "সোজা মেরুদণ্ড বেশি শক্ত"],
        "ভালো তোলার কৌশল এই প্রাকৃতিক বাঁক বজায় রাখে।"),
    mcq("What is the main structural job of tendons, compared with bridge cables?", ["Both carry tension, transferring pulling forces between parts", "Both carry compression", "Neither carries force", "Tendons carry blood"], 0,
        "Tendons are made of aligned collagen fibres, like parallel wires in a cable.",
        "সেতুর তারের তুলনায় কণ্ডরার প্রধান কাঠামোগত কাজ কী?", ["দুটোই টান বয়, অংশগুলোর মধ্যে টানার বল স্থানান্তর করে", "দুটোই সংনমন বয়", "কোনোটাই বল বয় না", "কণ্ডরা রক্ত বয়"],
        "কণ্ডরা সারিবদ্ধ কোলাজেন-তন্তুতে তৈরি, তারের সমান্তরাল সুতোর মতো।"),
    mcq("Why are sterile techniques important when treating a worker's open wound on site?", ["They prevent bacteria such as Staphylococcus and tetanus from entering and causing infection", "To make the wound heal slower", "They are only for hospitals", "They cool the wound"], 0,
        "Clean gloves, clean water and sterile dressings are basic first aid.",
        "নির্মাণস্থলে কর্মীর খোলা ক্ষতের চিকিৎসায় জীবাণুমুক্ত কৌশল জরুরি কেন?", ["স্ট্যাফাইলোকক্কাস আর ধনুষ্টংকারের মতো ব্যাকটেরিয়া ঢুকে সংক্রমণ আটকায়", "ক্ষত ধীরে সারাতে", "শুধু হাসপাতালের জন্য", "ক্ষত ঠান্ডা করে"],
        "পরিষ্কার দস্তানা, পরিষ্কার জল আর জীবাণুমুক্ত পট্টি মৌলিক প্রাথমিক চিকিৎসা।"),
    mcq("What is the purpose of 'health surveillance' for workers exposed to hazards?", ["Regular checks to detect early signs of work-related ill health so action can be taken", "Watching workers with cameras", "Checking their phones", "A one-time medical at retirement"], 0,
        "Hearing tests, lung tests and skin checks are common examples.",
        "বিপদের সংস্পর্শে থাকা কর্মীদের 'স্বাস্থ্য-নজরদারির' উদ্দেশ্য কী?", ["কাজজনিত অসুস্থতার প্রাথমিক লক্ষণ ধরতে নিয়মিত পরীক্ষা, যাতে ব্যবস্থা নেওয়া যায়", "ক্যামেরায় কর্মীদের নজর", "তাদের ফোন দেখা", "অবসরে একবার পরীক্ষা"],
        "শ্রবণ, ফুসফুস আর চামড়ার পরীক্ষা সাধারণ উদাহরণ।"),
    mcq("What does 'audiometry' test?", ["Hearing ability across different frequencies", "Eyesight", "Lung capacity", "Blood pressure"], 0,
        "Noise damage usually shows first as a dip around 4,000 Hz.",
        "'অডিওমেট্রি' কী পরীক্ষা করে?", ["বিভিন্ন কম্পাঙ্কে শোনার ক্ষমতা", "দৃষ্টি", "ফুসফুসের ক্ষমতা", "রক্তচাপ"],
        "শব্দজনিত ক্ষতি সাধারণত প্রথমে প্রায় 4,000 Hz-এ খাদ হিসেবে দেখা যায়।"),
    mcq("What is 'spirometry' used to measure?", ["How much air a person can breathe out and how fast - a test of lung function", "Blood sugar", "Body temperature", "Muscle strength"], 0,
        "It tracks lung damage from dust and fumes over time.",
        "'স্পাইরোমেট্রি' কী মাপতে ব্যবহার হয়?", ["মানুষ কতটা বাতাস আর কত দ্রুত ছাড়তে পারে - ফুসফুসের কার্যক্ষমতার পরীক্ষা", "রক্তে শর্করা", "শরীরের তাপমাত্রা", "পেশির শক্তি"],
        "সময়ের সঙ্গে ধুলো আর ধোঁয়ায় ফুসফুসের ক্ষতি নজরে রাখে।"),
    mcq("Why are pre-employment medicals done for crane operators?", ["To check vision, hearing, heart health and fitness that safe operation depends on", "To lower their wages", "To choose uniforms", "They are never done"], 0,
        "A sudden illness at the controls could endanger many people.",
        "ক্রেন-চালকদের নিয়োগের আগে স্বাস্থ্য-পরীক্ষা হয় কেন?", ["দৃষ্টি, শ্রবণ, হৃদ্‌স্বাস্থ্য আর সুস্থতা যাচাই করতে, নিরাপদ চালনা যার উপর নির্ভর করে", "মজুরি কমাতে", "পোশাক বাছতে", "কখনো হয় না"],
        "চালকের আসনে হঠাৎ অসুস্থতা অনেক মানুষকে বিপদে ফেলতে পারে।"),
    mcq("What is the 'blood-alcohol' risk the morning after heavy drinking for a site driver?", ["Alcohol may still be in the blood, impairing reactions even after sleep", "Sleep removes all alcohol instantly", "Coffee removes alcohol", "There is no risk"], 0,
        "The liver removes roughly one unit an hour - nothing speeds it up.",
        "রাতে অনেক মদ্যপানের পরের সকালে নির্মাণস্থলের চালকের 'রক্তে মদ'-এর ঝুঁকি কী?", ["ঘুমের পরেও রক্তে মদ থাকতে পারে, প্রতিক্রিয়া দুর্বল করে", "ঘুম তখনই সব মদ সরায়", "কফি মদ সরায়", "কোনো ঝুঁকি নেই"],
        "যকৃৎ মোটামুটি ঘণ্টায় এক একক সরায় - কিছুই একে দ্রুত করে না।"),
    mcq("What is the main function of the cerebellum, relevant to steel erectors?", ["Coordinating balance and precise movement", "Controlling hunger", "Producing hormones", "Filtering blood"], 0,
        "Fatigue, alcohol and some medicines impair it.",
        "ইস্পাত-খাড়াকারীদের জন্য প্রাসঙ্গিক সেরিবেলামের প্রধান কাজ কী?", ["ভারসাম্য আর নিখুঁত নড়াচড়ার সমন্বয়", "খিদে নিয়ন্ত্রণ", "হরমোন তৈরি", "রক্ত ছাঁকা"],
        "ক্লান্তি, মদ আর কিছু ওষুধ এটা দুর্বল করে।"),
)
