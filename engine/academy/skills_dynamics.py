"""Game skills, part 3: Help Q101-150 (wind, earthquakes and rail) as multiple-choice questions.

The question and the explanation are the Help screen's own text in both languages; only the
four options are written here, the right one first (the loader shuffles them)."""
from game.guide.dynamics import DYNAMICS

from . import mcq

_OPTS = (
    # Q101 natural frequency
    (("The rate at which it likes to swing: f_n = (1/2π)√(k/m), faster when stiffer, slower when heavier", "The number of vehicles per minute", "How often the bridge is inspected", "The frequency of the radio on site"),
     ("যে হারে এটি দুলতে চায়: f_n = (1/2π)√(k/m), দৃঢ় হলে দ্রুত, ভারী হলে ধীর", "প্রতি মিনিটে যানবাহনের সংখ্যা", "সেতু কতবার পরিদর্শন হয়", "সাইটের রেডিওর কম্পাঙ্ক")),
    # Q102 raise natural frequency
    (("Make it stiffer or lighter - a deeper truss is most effective", "Make it heavier", "Use more timber instead of steel", "Paint it a lighter colour"),
     ("দৃঢ় বা হালকা করো — গভীর ট্রাস সবচেয়ে কার্যকর", "ভারী করো", "ইস্পাতের বদলে বেশি কাঠ দাও", "হালকা রং করো")),
    # Q103 resonance
    (("Pushes in time with the natural swing add up, so the swing grows - as at Tacoma Narrows in 1940", "A very loud noise from the bridge", "Wind that blows only once", "A bridge that is too stiff"),
     ("স্বাভাবিক দোলার তালে ধাক্কা যোগ হতে থাকে, তাই দোলা বাড়ে — যেমন ১৯৪০-এ টাকোমা ন্যারোজে", "সেতু থেকে খুব জোর শব্দ", "একবার মাত্র বয়ে যাওয়া বাতাস", "খুব বেশি দৃঢ় সেতু")),
    # Q104 vortex shedding
    (("Swirls peel off the deck edges alternately, giving a rhythmic push at f_v = St U / D", "Rain falling on the deck", "Cars braking together", "Sunlight heating the deck"),
     ("ডেকের কিনারা থেকে পালা করে ঘূর্ণি ছিটকে যায়, f_v = St U / D হারে ছন্দে ধাক্কা দেয়", "ডেকে বৃষ্টি পড়া", "একসঙ্গে গাড়ির ব্রেক", "রোদে ডেক গরম হওয়া")),
    # Q105 U_crit
    (("The wind speed where the vortex rhythm equals f_n: U_crit = f_n D / St", "The top speed of the buses", "The speed limit on the bridge", "The wind that blows the bridge away instantly"),
     ("যে বায়ুগতিতে ঘূর্ণির ছন্দ f_n-এর সমান: U_crit = f_n D / St", "বাসের সর্বোচ্চ গতি", "সেতুর গতিসীমা", "যে বাতাস সঙ্গে সঙ্গে সেতু উড়িয়ে দেয়")),
    # Q106 lock-in
    (("No - vortices lock in whenever f_v is within 25% of f_n (about 0.75-1.25 x U_crit)", "Yes, only an exact match matters", "Wind never affects bridges", "Only above 100 m/s"),
     ("না — f_v যখনই f_n-এর ২৫%-এর মধ্যে (প্রায় ০.৭৫-১.২৫ x U_crit), ঘূর্ণি আটকে যায়", "হ্যাঁ, শুধু হুবহু মিললে", "বাতাস কখনো সেতুতে প্রভাব ফেলে না", "শুধু সেকেন্ডে ১০০ মিটারের বেশিতে")),
    # Q107 high wind resonance worse
    (("The vortex push grows with U², so at 30 m/s it is 9 times bigger than at 10 m/s", "High wind is always steady", "Low wind has bigger vortices", "There is no difference"),
     ("ঘূর্ণির ধাক্কা U²-এ বাড়ে, তাই সেকেন্ডে ৩০ মিটারে ১০ মিটারের ৯ গুণ", "জোরালো বাতাস সবসময় স্থির", "মৃদু বাতাসে ঘূর্ণি বড়", "কোনো তফাত নেই")),
    # Q108 fairings
    (("Streamlined edges cut the lift coefficient by 75%, so the push is four times weaker", "They raise f_n a lot", "They make the deck heavier to stop swinging", "They add lights to the bridge"),
     ("মসৃণ কিনারা উত্তোলন-সহগ ৭৫% কমায়, তাই ধাক্কা চার গুণ দুর্বল হয়", "এরা f_n অনেক বাড়ায়", "দোলা থামাতে ডেক ভারী করে", "সেতুতে আলো যোগ করে")),
    # Q109 dampers
    (("They raise damping from 0.5% to 2%, making the resonant swing about four times smaller", "They make the bridge longer", "They double f_n", "They remove the wind"),
     ("অবমন্দন ০.৫% থেকে ২% করে, তাই অনুনাদী দোলা প্রায় চার গুণ ছোট হয়", "সেতু লম্বা করে", "f_n দ্বিগুণ করে", "বাতাস সরিয়ে দেয়")),
    # Q110 TMD
    (("A heavy mass on springs under the deck, tuned to swing opposite to the bridge and soak up energy", "A large weight that holds the bridge down permanently", "A traffic light for trains", "A crane counterweight"),
     ("ডেকের নিচে স্প্রিংয়ে ঝোলানো ভারী ভর, সেতুর উল্টো দিকে দুলে শক্তি শুষে নেয়", "সেতু চিরকাল চেপে রাখা ভারী ওজন", "ট্রেনের ট্রাফিক-বাতি", "ক্রেনের পাল্টা-ওজন")),
    # Q111 TMD tuning
    (("Den Hartog's rule: tuning 1/(1+μ) and a matching damping - for μ = 0.02, about 0.98 and 0.08", "Always set both sliders to maximum", "Tuning does not matter", "Set tuning to 2.0"),
     ("ডেন হার্টগের নিয়ম: টিউনিং 1/(1+μ) আর মানানসই অবমন্দন — μ = 0.02-এ প্রায় ০.৯৮ আর ০.০৮", "দুটো স্লাইডারই সর্বোচ্চ করো", "টিউনিং জরুরি নয়", "টিউনিং ২.০ করো")),
    # Q112 heavier TMD
    (("It is more forgiving but costs more and adds deck weight - a tuned 0.02 is usually best value", "Always - heavier is free", "Heavier dampers stop working", "Only heavier ones can be tuned"),
     ("বেশি ক্ষমাশীল, কিন্তু দাম বেশি আর ডেকে ওজন যোগ করে — টিউন করা ০.০২ সাধারণত সেরা", "সবসময় — ভারী হলে বিনা পয়সায়", "ভারী ড্যাম্পার কাজ বন্ধ করে", "শুধু ভারীগুলো টিউন করা যায়")),
    # Q113 which wind fix
    (("Check the Wind lab and combine one fix - dampers, fairings or TMD - with a reasonably stiff truss", "Buy all three and the heaviest timber", "None - wind never matters", "Only make the deck longer"),
     ("বাতাস-ল্যাব দেখে একটা সমাধান — ড্যাম্পার, ফেয়ারিং বা টিএমডি — যথেষ্ট দৃঢ় ট্রাসের সঙ্গে মেলাও", "তিনটেই কেনো আর সবচেয়ে ভারী কাঠ দাও", "কিছুই না — বাতাস জরুরি নয়", "শুধু ডেক লম্বা করো")),
    # Q114 swing to forces
    (("The first swing mode is turned into equivalent deck loads at each instant and the truss solver checks every member", "Wind only changes the colours", "The swing is ignored by the solver", "Only cables feel the wind"),
     ("প্রথম দোলন-রূপকে প্রতি মুহূর্তে সমতুল্য ডেক-ভারে বদলে ট্রাস-সমাধানকারী প্রতিটি সদস্য যাচাই করে", "বাতাস শুধু রং বদলায়", "সমাধানকারী দোলা উপেক্ষা করে", "শুধু কেবল বাতাস টের পায়")),
    # Q115 Level 7 fails despite TEST
    (("TEST checks one still bus with no wind; the run adds four buses and a rising gale for 70 seconds", "TEST is always wrong", "Buses are heavier in RUN mode", "The wind only blows in TEST"),
     ("পরীক্ষা বাতাস ছাড়া একটা দাঁড়ানো বাস দেখে; চালানোয় চারটে বাস আর ৭০ সেকেন্ড বাড়তে থাকা ঝড়", "পরীক্ষা সবসময় ভুল", "চালানোয় বাস ভারী হয়", "বাতাস শুধু পরীক্ষায় বয়")),
    # Q116 Wind lab
    (("f_n, the vortex rhythm, U_crit against the level's strongest wind, and the best TMD tuning", "The price of steel", "The bus timetable", "Only the wind direction"),
     ("f_n, ঘূর্ণির ছন্দ, লেভেলের সবচেয়ে জোর বাতাসের তুলনায় U_crit, আর সেরা টিএমডি টিউনিং", "ইস্পাতের দাম", "বাসের সময়সূচি", "শুধু বাতাসের দিক")),
    # Q117 earthquake model
    (("A decaying sine shake peaking at 0.35 g and 1.5 Hz, starting as the truck is 35% across", "Random shaking for an hour", "A single jolt at the end of the level", "Shaking that grows forever"),
     ("ক্ষয়িষ্ণু সাইন-কাঁপুনি, শীর্ষে ০.৩৫ g আর ১.৫ হার্জ, ট্রাক ৩৫% পার হলে শুরু", "এক ঘণ্টা এলোমেলো কাঁপুনি", "লেভেলের শেষে একটা ঝাঁকুনি", "চিরকাল বাড়তে থাকা কাঁপুনি")),
    # Q118 base shear
    (("The total sideways force: mass x ground acceleration x response factor C", "The weight of the deck only", "The force of the truck's brakes", "The river's push on the piers"),
     ("মোট পাশের বল: ভর x ভূমি-ত্বরণ x সাড়া-গুণক C", "শুধু ডেকের ওজন", "ট্রাকের ব্রেকের বল", "স্তম্ভে নদীর ধাক্কা")),
    # Q119 natural period
    (("The time of one full sway, T = 2π√(M/k) = 1/f", "The time the truck takes to cross", "The age of the bridge", "The length of the earthquake"),
     ("একটা পূর্ণ দোলার সময়, T = 2π√(M/k) = 1/f", "ট্রাকের পার হওয়ার সময়", "সেতুর বয়স", "ভূমিকম্পের দৈর্ঘ্য")),
    # Q120 C vs T
    (("A plateau of 2.5 between 0.1 and 0.5 s, then falling as 2.5 x 0.5 / T", "C always equals 1", "C grows forever with T", "C is the cost per tonne"),
     ("০.১ থেকে ০.৫ সেকেন্ডে ২.৫-এর মালভূমি, তারপর 2.5 x 0.5 / T হারে কমে", "C সবসময় ১", "T-এর সঙ্গে C চিরকাল বাড়ে", "C হল টনপ্রতি দাম")),
    # Q121 stiffer worse
    (("A shorter period lands on the 2.5 plateau and added mass raises V = C M a_g", "Stiff bridges attract lightning", "Stiffness makes steel brittle", "It is never worse"),
     ("ছোট পর্যায়কাল ২.৫-এর মালভূমিতে পড়ে আর বাড়তি ভর V = C M a_g বাড়ায়", "দৃঢ় সেতু বাজ টানে", "দৃঢ়তা ইস্পাত ভঙ্গুর করে", "কখনো খারাপ হয় না")),
    # Q122 heavier feels more
    (("Force is mass x acceleration, so every extra tonne adds sideways force", "Heavier bridges float above the shaking", "Mass has no effect", "Lighter bridges feel more force"),
     ("বল = ভর x ত্বরণ, তাই প্রতি বাড়তি টন পাশের বল বাড়ায়", "ভারী সেতু কাঁপুনির উপরে ভাসে", "ভরের কোনো প্রভাব নেই", "হালকা সেতু বেশি বল টের পায়")),
    # Q123 isolation bearings
    (("They stretch the period to 2.5 s, cutting C from 2.5 to 0.5 - but the deck moves much further", "They glue the deck to the piers", "They make the bridge heavier", "They stop the ground moving"),
     ("পর্যায়কাল ২.৫ সেকেন্ডে টেনে C ২.৫ থেকে ০.৫ করে — কিন্তু ডেক অনেক বেশি সরে", "ডেককে স্তম্ভে আঠা দিয়ে আটকায়", "সেতু ভারী করে", "মাটি নড়া থামায়")),
    # Q124 pounding
    (("The isolated deck drifts about 0.27 m but a normal joint gap is 0.05 m - buy flexible joints too", "The truck braked too hard", "The bearings were too stiff", "Pounding is caused by rain"),
     ("বিচ্ছিন্ন ডেক প্রায় ০.২৭ মিটার সরে, অথচ সাধারণ জোড়ের ফাঁক ০.০৫ মিটার — নমনীয় জোড়ও কেনো", "ট্রাক খুব জোরে ব্রেক কষেছিল", "বিয়ারিং খুব দৃঢ় ছিল", "বৃষ্টিতে ধাক্কা লাগে")),
    # Q125 diagonals in every bay
    (("Bank rollers take no sideways push, so it must go down braced columns - a bay without a diagonal folds", "Diagonals are only decoration", "To carry the truck's weight only", "To hold the river back"),
     ("পাড়ের রোলার পাশের ধাক্কা নেয় না, তাই তা ঠেকনা-দেওয়া স্তম্ভ দিয়ে নামতে হয় — কর্ণহীন খোপ ভাঁজ হয়ে যায়", "কর্ণ শুধু সাজানোর জন্য", "শুধু ট্রাকের ওজন বইতে", "নদী আটকাতে")),
    # Q126 concrete braces
    (("Not for diagonals - shaking reverses, so a pushed brace is soon pulled and concrete fails in tension", "Yes, concrete is ideal for braces", "Only in wet weather", "Concrete is stronger when shaken"),
     ("কর্ণে নয় — কাঁপুনি দিক বদলায়, তাই চাপ-খাওয়া ঠেকনা শিগগিরই টান খায় আর কংক্রিট টানে ভাঙে", "হ্যাঁ, ঠেকনায় কংক্রিট আদর্শ", "শুধু ভেজা আবহাওয়ায়", "কাঁপলে কংক্রিট শক্ত হয়")),
    # Q127 robust way
    (("Massive X-braced steel piers resisting the full shaking - it works but is hard to keep under par", "Isolation bearings without joints", "No bracing at all", "A concrete-only viaduct"),
     ("পুরো কাঁপুনি সামলানো বিশাল এক্স-ঠেকনার ইস্পাত-স্তম্ভ — কাজ করে, কিন্তু সমমানের নিচে রাখা কঠিন", "জোড় ছাড়া বিচ্ছিন্নকারী বিয়ারিং", "কোনো ঠেকনাই নয়", "শুধু কংক্রিটের উড়ালপথ")),
    # Q128 Quake lab
    (("Period T, factor C with and without bearings, base shear, and isolated drift against the joint gap", "The truck's fuel level", "Only the price of bearings", "The weather forecast"),
     ("পর্যায়কাল T, বিয়ারিং-সহ ও ছাড়া C, ভিত্তি-কৃন্তন, আর জোড়ের ফাঁকের তুলনায় বিচ্ছিন্ন ডেকের সরণ", "ট্রাকের জ্বালানি", "শুধু বিয়ারিং-এর দাম", "আবহাওয়ার পূর্বাভাস")),
    # Q129 slope pull
    (("F = m g sin θ - a 1% grade pulls back about 1% of the train's weight", "Slopes have no effect on trains", "A 1% grade pulls back half the weight", "Only the engine's weight is pulled back"),
     ("F = m g sin θ — ১% ঢাল ট্রেনের ওজনের প্রায় ১% পিছনে টানে", "ঢালের ট্রেনে প্রভাব নেই", "১% ঢাল অর্ধেক ওজন পিছনে টানে", "শুধু ইঞ্জিনের ওজন পিছনে টানে")),
    # Q130 adhesion
    (("Grip = μ x weight on the driving wheels: 0.30 dry, 0.18 wet - only the locomotive's weight counts", "Grip depends only on engine power", "Wagons add grip too", "Wet rails grip better"),
     ("আঁকড় = μ x চালক-চাকার উপর ওজন: শুকনোয় ০.৩০, ভেজায় ০.১৮ — শুধু ইঞ্জিনের ওজন ধরা হয়", "আঁকড় শুধু ইঞ্জিনের শক্তির উপর নির্ভর করে", "ওয়াগনও আঁকড় বাড়ায়", "ভেজা লাইনে আঁকড় বেশি")),
    # Q131 tractive effort
    (("Grip limits pull at low speed; power limits it at higher speed, since pull = P / v", "Pull rises the faster you go", "Pull is always the same", "Pull depends only on wagon count"),
     ("কম গতিতে আঁকড় টান সীমিত করে; বেশি গতিতে শক্তি, কারণ টান = P / v", "যত দ্রুত, তত বেশি টান", "টান সবসময় সমান", "টান শুধু ওয়াগনের সংখ্যায় নির্ভর করে")),
    # Q132 steepest grade
    (("tan θ = μ x m_loco / m_train - C_rr: a shunter with 2 wagons manages 11.8%, with 4 only 7.3%", "Any grade, if the engine is loud", "Exactly 50% for every train", "Grades do not limit trains"),
     ("tan θ = μ x m_loco / m_train - C_rr: দুই ওয়াগনে শান্টার ১১.৮% পারে, চারটেয় মাত্র ৭.৩%", "ইঞ্জিন জোরে শব্দ করলে যেকোনো ঢাল", "প্রতিটি ট্রেনের জন্য ঠিক ৫০%", "ঢাল ট্রেনকে সীমিত করে না")),
    # Q133 even grade or follow hill
    (("Even grade usually pays: it removes the 13.3% stretch that stalls trains, for the cost of earthworks", "Follow hill is always best because it is free", "Both give the same steepest slope", "Neither can reach the station"),
     ("সমান ঢাল সাধারণত লাভজনক: মাটি-কাজের খরচে ট্রেন থামানো ১৩.৩% অংশ সরায়", "পাহাড় অনুসরণ সবসময় সেরা কারণ বিনা পয়সায়", "দুটোতেই একই সবচেয়ে খাড়া ঢাল", "কোনোটাই স্টেশনে পৌঁছায় না")),
    # Q134 track and earthworks
    (("Track Rs 3,000/m; cuttings and embankments cost per m² of cross-section, much more on rocky Eagle Pass", "Earthworks are free", "Track costs Rs 3 per metre", "Embankments cost more than cuttings everywhere"),
     ("লাইন মিটারে ৩,০০০ টাকা; কাটা আর বাঁধের দাম প্রস্থচ্ছেদের বর্গমিটারে, পাথুরে ঈগল পাসে অনেক বেশি", "মাটি-কাজ বিনা পয়সায়", "লাইন মিটারে ৩ টাকা", "সব জায়গায় বাঁধ কাটার চেয়ে দামি")),
    # Q135 which locomotive
    (("The cheapest one whose grip limit covers your train on the steepest bit - weight is grip", "Always the double-header", "Always the tank engine", "The one with the best colour"),
     ("সবচেয়ে সস্তা সেটা, যার আঁকড়-সীমা সবচেয়ে খাড়া অংশে তোমার ট্রেন সামলায় — ওজনই আঁকড়", "সবসময় দুই-ইঞ্জিন", "সবসময় ট্যাঙ্ক ইঞ্জিন", "যার রং সবচেয়ে সুন্দর")),
    # Q136 banker
    (("A pusher at the back adding 400 kW and about 147 kN more grip, for Rs 2.5 lakh", "A bank loan for the railway", "A brake van", "A signal at the summit"),
     ("পিছনে ঠেলা-ইঞ্জিন, ৪০০ কিলোওয়াট আর প্রায় ১৪৭ কিলোনিউটন বাড়তি আঁকড় যোগ করে, দাম ২.৫ লাখ", "রেলের জন্য ব্যাংক-ঋণ", "ব্রেক-ভ্যান", "চূড়ায় একটা সংকেত")),
    # Q137 wagons
    (("Level 2 log wagons: 30 t cargo, 15 t empty, Rs 20,000; Level 4 ore wagons: 60 t, 22 t empty, Rs 50,000", "All wagons weigh nothing when empty", "Every wagon carries 100 t", "Wagons are free"),
     ("লেভেল ২-এর কাঠ-ওয়াগন: ৩০ টন মাল, খালি ১৫ টন, ২০,০০০ টাকা; লেভেল ৪-এর আকরিক-ওয়াগন: ৬০ টন, খালি ২২ টন, ৫০,০০০ টাকা", "খালি ওয়াগনের ওজন নেই", "প্রতিটি ওয়াগন ১০০ টন বয়", "ওয়াগন বিনা পয়সায়")),
    # Q138 job time
    (("Trips (rounded up) x trip time + the empty runs back", "Only one trip is ever counted", "Trip time divided by wagons", "A fixed 2 minutes always"),
     ("যাত্রার সংখ্যা (উপরে তুলে) x যাত্রার সময় + খালি ফেরার সময়", "সবসময় শুধু একটা যাত্রা গোনা হয়", "যাত্রার সময় ভাগ ওয়াগন", "সবসময় স্থির ২ মিনিট")),
    # Q139 wheel slip
    (("Carry fewer wagons, flatten the steepest part, use a heavier engine or add the banker", "Add more power only", "Speed up", "Ignore it"),
     ("কম ওয়াগন নাও, সবচেয়ে খাড়া অংশ সমান করো, ভারী ইঞ্জিন বা ঠেলা-ইঞ্জিন নাও", "শুধু শক্তি বাড়াও", "গতি বাড়াও", "উপেক্ষা করো")),
    # Q140 tank engine Level 2
    (("Only one wagon at a time on the 8% grade, so four slow trips - check the 2-minute limit", "Yes, with all six wagons in one trip", "No, it cannot move at all", "Only downhill"),
     ("৮% ঢালে একবারে মাত্র এক ওয়াগন, তাই চারটে ধীর যাত্রা — ২ মিনিটের সীমা যাচাই করো", "হ্যাঁ, ছয় ওয়াগন নিয়ে এক যাত্রায়", "না, এটা নড়তেই পারে না", "শুধু উৎরাইয়ে")),
    # Q141 momentum
    (("A heavy moving train can coast over a short steep crest using its kinetic energy", "Momentum makes trains slower uphill", "Momentum removes the need for an engine", "It only matters for stopping"),
     ("চলন্ত ভারী ট্রেন গতিশক্তি খরচ করে ছোট খাড়া চূড়া গড়িয়ে পেরোতে পারে", "ভরবেগে চড়াইয়ে ট্রেন ধীর হয়", "ভরবেগে ইঞ্জিনের দরকার থাকে না", "এটা শুধু থামার সময় জরুরি")),
    # Q142 energy bars
    (("Kinetic energy ½mv² and potential energy mgh - climbing turns work into height, descending into speed", "Fuel and water levels", "The driver's tiredness", "Ticket sales"),
     ("গতিশক্তি ½mv² আর স্থিতিশক্তি mgh — চড়াইয়ে কাজ উচ্চতায়, উৎরাইয়ে গতিতে বদলায়", "জ্বালানি আর জলের মাত্রা", "চালকের ক্লান্তি", "টিকিট বিক্রি")),
    # Q143 stopping distance
    (("d = v² / (2(μ g cos θ - g sin θ)) - double the speed and the distance becomes four times longer", "It is the same at every speed", "Wet rails shorten it", "Downhill shortens it"),
     ("d = v² / (2(μ g cos θ - g sin θ)) — গতি দ্বিগুণ করলে দূরত্ব চার গুণ হয়", "সব গতিতে সমান", "ভেজা লাইনে কমে", "উৎরাইয়ে কমে")),
    # Q144 no brake can stop
    (("When the grade (tan θ) is bigger than μ - steeper than 30% dry or 18% wet", "Never - brakes always work", "Only on level track", "Whenever it is night"),
     ("যখন ঢাল (tan θ) μ-এর চেয়ে বেশি — শুকনোয় ৩০% বা ভেজায় ১৮%-এর বেশি খাড়া", "কখনো না — ব্রেক সবসময় কাজ করে", "শুধু সমতল লাইনে", "যখনই রাত")),
    # Q145 brake marker
    (("The allowed distance is stop line - marker; stop within 15 m of the line for the bonus star", "Put it right on the stop line", "Brake markers are only decoration", "Put it after the buffers"),
     ("অনুমোদিত দূরত্ব = থামার রেখা - চিহ্ন; বাড়তি তারার জন্য রেখার ১৫ মিটারের মধ্যে থামো", "ঠিক থামার রেখায় বসাও", "ব্রেক-চিহ্ন শুধু সাজানোর জন্য", "বাফারের পরে বসাও")),
    # Q146 signal spacing
    (("A train passing a YELLOW must be able to stop before the next RED, or it passes a signal at danger", "Signals must be close so drivers see more lights", "Spacing only affects cost", "Trains never need braking distance"),
     ("হলুদ পেরোনো ট্রেনকে পরের লালের আগে থামতে পারতে হবে, নইলে বিপদ-সংকেত পেরিয়ে যায়", "চালক বেশি আলো দেখতে কাছাকাছি সংকেত চাই", "ব্যবধান শুধু খরচে প্রভাব ফেলে", "ট্রেনের থামার দূরত্ব লাগে না")),
    # Q147 3 or 4 aspect
    (("4-aspect adds DOUBLE YELLOW so blocks need only half the braking distance, but each signal costs more", "3-aspect always lets trains follow closer", "They are identical", "4-aspect removes the need for red"),
     ("৪-দিকের সংকেতে জোড়া হলুদ যোগ হয়, তাই ব্লকে অর্ধেক থামার দূরত্ব লাগে, কিন্তু প্রতিটির দাম বেশি", "৩-দিকের সংকেতে ট্রেন সবসময় কাছে চলতে পারে", "দুটো হুবহু এক", "৪-দিকের সংকেতে লালের দরকার নেই")),
    # Q148 maglev
    (("Thrust-limited at 220 kN below about 13.6 m/s, then power-limited as F = P / v", "Its thrust grows with speed forever", "It is limited by wheel grip", "It has rolling resistance like a train"),
     ("সেকেন্ডে প্রায় ১৩.৬ মিটারের নিচে ২২০ কিলোনিউটনে ধাক্কা-সীমিত, তারপর F = P / v হারে শক্তি-সীমিত", "এর ধাক্কা গতির সঙ্গে চিরকাল বাড়ে", "এটা চাকার আঁকড়ে সীমিত", "ট্রেনের মতো এর ঘর্ষণ-বাধা আছে")),
    # Q149 smart grid MW
    (("About 3 MW for the pod plus the powered alloy's share - not 8", "As much as possible, 8 MW or more", "Zero - the pod needs no power", "Exactly 1 MW"),
     ("পডের জন্য প্রায় ৩ মেগাওয়াট আর চালু সংকরের ভাগ — ৮ নয়", "যত বেশি সম্ভব, ৮ মেগাওয়াট বা বেশি", "শূন্য — পডের শক্তি লাগে না", "ঠিক ১ মেগাওয়াট")),
    # Q150 power the alloy?
    (("Only if wind is the problem - it doubles stiffness but draws 50 kW per tonne from the pod's grid", "Always, it is free", "Never, it weakens the bridge", "Only when no pod is running"),
     ("শুধু বাতাস সমস্যা হলে — দৃঢ়তা দ্বিগুণ করে, কিন্তু পডের গ্রিড থেকে টনপ্রতি ৫০ কিলোওয়াট টানে", "সবসময়, বিনা পয়সায়", "কখনো না, সেতু দুর্বল করে", "শুধু পড না চললে")),
)

assert len(_OPTS) == len(DYNAMICS) == 50

ITEMS = tuple(mcq(it.q_en, en, 0, it.a_en, it.q_bn, bn, it.a_bn) for it, (en, bn) in zip(DYNAMICS, _OPTS))
