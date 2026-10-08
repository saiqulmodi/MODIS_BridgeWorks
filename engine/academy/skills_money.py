"""Game skills, part 4: Help Q151-200 (money and every level) as multiple-choice questions.

The question and the explanation are the Help screen's own text in both languages; only the
four options are written here, the right one first (the loader shuffles them)."""
from game.guide.money import MONEY

from . import mcq

_OPTS = (
    # Q151 budget, par, cost
    (("Cost is your design's price, budget is the money you have, par is the expert target for the second star", "All three mean the same", "Par is the maximum loan", "Budget is the toll income"),
     ("খরচ তোমার নকশার দাম, বাজেট তোমার হাতের টাকা, সমমান দ্বিতীয় তারার জন্য বিশেষজ্ঞের লক্ষ্য", "তিনটের মানে একই", "সমমান হল সর্বোচ্চ ঋণ", "বাজেট হল টোল-আয়")),
    # Q152 cost lines
    (("Materials, labour & scaffolding, five years of maintenance, and equipment & extras", "Only materials", "Materials and tax only", "Labour and fuel only"),
     ("উপাদান, শ্রম ও ভারা, পাঁচ বছরের রক্ষণাবেক্ষণ, আর যন্ত্র ও বাড়তি জিনিস", "শুধু উপাদান", "শুধু উপাদান আর কর", "শুধু শ্রম আর জ্বালানি")),
    # Q153 labour vs materials Level 1
    (("Timber is so cheap that work dominates: in the demo labour is 72% of the cost", "Workers are paid extra in Level 1", "Timber is the most expensive material", "Materials are free in Level 1"),
     ("কাঠ এত সস্তা যে কাজই প্রধান: ডেমোতে খরচের ৭২% শ্রম", "লেভেল ১-এ কর্মীরা বাড়তি পান", "কাঠ সবচেয়ে দামি উপাদান", "লেভেল ১-এ উপাদান বিনা পয়সায়")),
    # Q154 stars
    (("1 star: success within funds; 2: also at or under par; 3: also the extra goal such as FS 1.5-4", "Stars are random", "3 stars for any bridge that stands", "2 stars need a loan"),
     ("১ তারা: তহবিলের মধ্যে সাফল্য; ২: সঙ্গে সমমান বা কম; ৩: সঙ্গে বাড়তি লক্ষ্য, যেমন গুণক ১.৫-৪", "তারা এলোমেলো", "যেকোনো দাঁড়িয়ে থাকা সেতুতে ৩ তারা", "২ তারার জন্য ঋণ লাগে")),
    # Q155 EXP
    (("Success gives 100 + 50 x stars; a Black Box and a correct first diagnosis after failure give 60", "Only demonstrations give EXP", "EXP is bought with money", "Failures remove EXP"),
     ("সাফল্যে ১০০ + ৫০ x তারা; ব্যর্থতার পরে ব্ল্যাক বক্স আর প্রথমবারে সঠিক নির্ণয়ে ৬০", "শুধু প্রদর্শনী অভিজ্ঞতা দেয়", "অভিজ্ঞতা টাকায় কেনা হয়", "ব্যর্থতায় অভিজ্ঞতা কাটা যায়")),
    # Q156 salvage
    (("30% of a failed design's build cost comes back and is added to that level's budget for good", "A fine paid after failure", "Money lost forever", "A bonus only for three stars"),
     ("ব্যর্থ নকশার নির্মাণ-খরচের ৩০% ফেরত এসে সেই লেভেলের বাজেটে চিরকালের জন্য যোগ হয়", "ব্যর্থতার পরে জরিমানা", "চিরকালের জন্য হারানো টাকা", "শুধু তিন তারার বোনাস")),
    # Q157 demo cost
    (("0.5% of the level's base budget, once, taken from that level's budget permanently", "Demos are always free", "Half of the budget each time", "Rs 1 lakh in every level"),
     ("লেভেলের মূল বাজেটের ০.৫%, একবারই, সেই লেভেলের বাজেট থেকে চিরকালের জন্য কাটা", "ডেমো সবসময় বিনা পয়সায়", "প্রতিবার বাজেটের অর্ধেক", "প্রতিটি লেভেলে ১ লাখ টাকা")),
    # Q158 over-engineering penalty
    (("Above FS 4, 5% of the budget is subtracted per point, up to 30%", "A reward for very strong bridges", "A fee for using steel", "A penalty for finishing early"),
     ("গুণক ৪-এর বেশি হলে প্রতি পয়েন্টে বাজেটের ৫% কাটা হয়, সর্বোচ্চ ৩০%", "খুব শক্ত সেতুর পুরস্কার", "ইস্পাত ব্যবহারের মাশুল", "আগে শেষ করার জরিমানা")),
    # Q159 alternate route cost
    (("The level's cost factor (0.4-0.8) x the failed build cost, finishing with one star and 30 EXP", "It is always free", "It costs the whole budget and gives three stars", "It ends the game"),
     ("লেভেলের খরচ-গুণক (০.৪-০.৮) x ব্যর্থ নির্মাণ-খরচ, এক তারা আর ৩০ অভিজ্ঞতায় শেষ", "সবসময় বিনা পয়সায়", "পুরো বাজেট লাগে আর তিন তারা দেয়", "খেলা শেষ করে দেয়")),
    # Q160 tolls per level
    (("Each level has its own toll, such as Rs 10 per vehicle in Level 1 and Rs 200 per passenger on the maglev", "Every level charges Rs 100 per vehicle", "There are no tolls", "Only Level 10 earns money"),
     ("প্রতিটি লেভেলের নিজস্ব টোল, যেমন লেভেল ১-এ প্রতি যানে ১০ টাকা আর ম্যাগলেভে যাত্রীপ্রতি ২০০ টাকা", "প্রতিটি লেভেলে প্রতি যানে ১০০ টাকা", "কোনো টোল নেই", "শুধু লেভেল ১০ আয় করে")),
    # Q161 first-year income
    (("45% of the level's budget at the standard toll, then growing 6% a year", "Exactly the par cost", "Zero in the first year", "Double the budget"),
     ("সাধারণ টোলে লেভেলের বাজেটের ৪৫%, তারপর বছরে ৬% বাড়ে", "ঠিক সমমানের সমান", "প্রথম বছরে শূন্য", "বাজেটের দ্বিগুণ")),
    # Q162 raise toll
    (("Higher tolls keep some users away, so income grows only with the square root of the factor", "Income grows exactly with the toll", "Raising tolls always loses income", "Users never react to the toll"),
     ("বেশি টোলে কিছু ব্যবহারকারী সরে যায়, তাই আয় গুণকের শুধু বর্গমূলে বাড়ে", "আয় টোলের সঙ্গে হুবহু বাড়ে", "টোল বাড়ালে সবসময় আয় কমে", "ব্যবহারকারী টোলে সাড়া দেন না")),
    # Q163 loan payment
    (("An annuity A = P r / (1 - (1 + r)^-n) - about Rs 11,133 a year per lakh from the bank", "The whole loan is paid in year 1", "Interest only, never the principal", "A random amount each year"),
     ("বার্ষিকী A = P r / (1 - (1 + r)^-n) — ব্যাংক থেকে প্রতি লাখে বছরে প্রায় ১১,১৩৩ টাকা", "পুরো ঋণ প্রথম বছরেই শোধ", "শুধু সুদ, আসল কখনো নয়", "প্রতি বছর এলোমেলো অঙ্ক")),
    # Q164 DSCR 1.5
    (("(Toll income - upkeep) ÷ yearly loan payments must be at least 1.5 for the bank to lend", "The bridge's FS must be 1.5", "The loan must be 1.5 times the budget", "Tolls must rise 1.5% a year"),
     ("(টোল-আয় - রক্ষণাবেক্ষণ) ÷ বার্ষিক ঋণ-কিস্তি অন্তত ১.৫ হলে তবেই ব্যাংক ঋণ দেয়", "সেতুর গুণক ১.৫ হতে হবে", "ঋণ বাজেটের ১.৫ গুণ হতে হবে", "টোল বছরে ১.৫% বাড়তে হবে")),
    # Q165 upkeep and growth
    (("Upkeep is 3% of the build cost each year, and traffic and income grow 6% a year over 20 years", "Upkeep is free and traffic never grows", "Upkeep is 50% of income", "Traffic falls 6% a year"),
     ("রক্ষণাবেক্ষণ প্রতি বছর নির্মাণ-খরচের ৩%, আর ২০ বছর ধরে যানবাহন ও আয় বছরে ৬% বাড়ে", "রক্ষণাবেক্ষণ বিনা পয়সায়, যানবাহন বাড়ে না", "রক্ষণাবেক্ষণ আয়ের ৫০%", "যানবাহন বছরে ৬% কমে")),
    # Q166 investment recovered and profit
    (("The first year your running cash total turns positive, and where it ends after 20 years", "The bridge's age and height", "The number of stars and EXP", "The loan's interest rate"),
     ("যে বছরে তোমার চলতি নগদ-মোট প্রথম ধনাত্মক হয়, আর ২০ বছর পরে তা কোথায় শেষ হয়", "সেতুর বয়স আর উচ্চতা", "তারা আর অভিজ্ঞতার সংখ্যা", "ঋণের সুদের হার")),
    # Q167 bank or government
    (("The government loan first: 0.5% over 15 years gives about 38% lower yearly payments", "Always the bank loan", "Neither - loans are illegal", "Whichever has the longer name"),
     ("আগে সরকারি ঋণ: ১৫ বছরে ০.৫% সুদে বার্ষিক কিস্তি প্রায় ৩৮% কম", "সবসময় ব্যাংক-ঋণ", "কোনোটাই নয় — ঋণ বেআইনি", "যার নাম লম্বা")),
    # Q168 bank loan size
    (("The largest loan keeping DSCR at exactly 1.5 - about Rs 5.3 L in Level 1 at the standard toll", "Any amount you ask for", "Always exactly the budget", "Nothing above Rs 1,000"),
     ("যে সবচেয়ে বড় ঋণে অনুপাত ঠিক ১.৫ থাকে — সাধারণ টোলে লেভেল ১-এ প্রায় ৫.৩ লাখ", "যত চাও তত", "সবসময় ঠিক বাজেটের সমান", "১,০০০ টাকার বেশি নয়")),
    # Q169 loan example
    (("A Rs 50,000 shortfall costs about Rs 5,566 a year from the bank; DSCR about 18.6 - approved, but over par", "The loan is rejected", "The bridge earns three stars because of the loan", "The shortfall is Rs 3 lakh"),
     ("৫০,০০০ টাকার ঘাটতিতে ব্যাংকে বছরে প্রায় ৫,৫৬৬ টাকা; অনুপাত প্রায় ১৮.৬ — মঞ্জুর, কিন্তু সমমানের বেশি", "ঋণ বাতিল হয়", "ঋণের জন্য সেতু তিন তারা পায়", "ঘাটতি ৩ লাখ টাকা")),
    # Q170 loan screen
    (("It opens by itself when a design costs more than the budget; the Finance button shows it any time", "Only after three failures", "Never - loans are automatic", "Only in Level 10"),
     ("নকশার খরচ বাজেট ছাড়ালে নিজে থেকেই খোলে; অর্থ-বোতাম যেকোনো সময় দেখায়", "শুধু তিনবার ব্যর্থ হলে", "কখনো না — ঋণ আপনা থেকে হয়", "শুধু লেভেল ১০-এ")),
    # Q171 demo results
    (("They run the real simulation; Levels 1, 7 and 8 get 3 stars but Level 10's demo is over par", "Every demo is perfect and free", "Demos never pass", "Demos skip the simulation"),
     ("এরা আসল অনুকরণ চালায়; লেভেল ১, ৭ আর ৮ তিন তারা পায়, কিন্তু লেভেল ১০-এর ডেমো সমমানের বেশি", "প্রতিটি ডেমো নিখুঁত আর বিনা পয়সায়", "ডেমো কখনো পাস করে না", "ডেমো অনুকরণ বাদ দেয়")),
    # Q172 Level 10 under par
    (("Buy 3 MW of grid instead of 4 - the pod still crosses in time and the cost drops under par", "Buy 8 MW", "Remove the guideway", "Use timber for the towers"),
     ("৪-এর বদলে ৩ মেগাওয়াট গ্রিড কেনো — পড তবুও সময়ে পার হয় আর খরচ সমমানের নিচে নামে", "৮ মেগাওয়াট কেনো", "গাইডওয়ে সরিয়ে দাও", "টাওয়ারে কাঠ দাও")),
    # Q173 Level 7 under par
    (("Steel with as few panels as needed, one wind fix such as fairings, and shrink green members", "Buy every wind fix and use XL everywhere", "Use concrete cables", "Skip the wind fix entirely"),
     ("যতটুকু দরকার ততগুলো প্যানেলে ইস্পাত, ফেয়ারিং-এর মতো একটা বাতাস-সমাধান, আর সবুজ সদস্য ছোট করো", "সব বাতাস-সমাধান কেনো আর সব জায়গায় XL", "কংক্রিটের কেবল দাও", "বাতাস-সমাধান একদম বাদ দাও")),
    # Q174 Level 8 under par
    (("Isolation plus flexible joints cut the quake force five times, so slim steel columns suffice", "Heavy X-braced concrete piers", "No bracing and no bearings", "Double the deck weight"),
     ("বিচ্ছিন্নকারী বিয়ারিং আর নমনীয় জোড় কম্পন-বল পাঁচ গুণ কমায়, তাই সরু ইস্পাত-স্তম্ভই যথেষ্ট", "ভারী এক্স-ঠেকনার কংক্রিট-স্তম্ভ", "ঠেকনা বা বিয়ারিং কিছুই নয়", "ডেকের ওজন দ্বিগুণ")),
    # Q175 Levels 2 and 4 money
    (("Track, earthworks, the locomotive and wagon hire - pick the cheapest engine that copes with your steepest grade", "Only tickets", "Only the station buildings", "Bridges and tolls"),
     ("লাইন, মাটি-কাজ, ইঞ্জিন আর ওয়াগন-ভাড়া — সবচেয়ে খাড়া ঢাল সামলানো সবচেয়ে সস্তা ইঞ্জিন বাছো", "শুধু টিকিট", "শুধু স্টেশন-ভবন", "সেতু আর টোল")),
    # Q176 mainline or double-header
    (("A single mainline diesel with 5 wagons, spending the savings on smoothing the worst grade", "Always the double-header", "The tank engine with 12 wagons", "No engine at all"),
     ("৫ ওয়াগনসহ একটা মেইনলাইন ডিজেল, আর বাঁচানো টাকা সবচেয়ে খারাপ ঢাল মসৃণ করতে", "সবসময় দুই-ইঞ্জিন", "১২ ওয়াগনসহ ট্যাঙ্ক ইঞ্জিন", "কোনো ইঞ্জিনই নয়")),
    # Q177 Level 5 pricing
    (("Signal price x (placed + 2 fixed signals) + Rs 50,000 per logic term", "A fixed Rs 15 L", "Per train delivered", "Per metre of track"),
     ("সংকেতের দাম x (বসানো + ২টি স্থির সংকেত) + প্রতি যুক্তি-পদে ৫০,০০০ টাকা", "স্থির ১৫ লাখ টাকা", "প্রতি পৌঁছানো ট্রেনে", "লাইনের প্রতি মিটারে")),
    # Q178 cheapest Level 5 plan
    (("Fix the three logic bugs and place no extra signals - Rs 10 L, 0 SPADs, about 764 train-seconds", "Place ten extra signals", "Leave the bugs and add signals", "Use 4-aspect signals everywhere"),
     ("যুক্তির তিনটে ত্রুটি সারাও আর কোনো বাড়তি সংকেত বসিয়ো না — ১০ লাখ, শূন্য বিপদ-অতিক্রম, প্রায় ৭৬৪ ট্রেন-সেকেন্ড", "দশটা বাড়তি সংকেত বসাও", "ত্রুটি রেখে সংকেত বাড়াও", "সব জায়গায় ৪-দিকের সংকেত")),
    # Q179 three bugs
    (("Missing NOT PERMIT for the other direction, the switch using CARGO_APPR_JE, and an empty BARRIER_DOWN", "Wrong signal colours, slow trains and rain", "Too many signals, too few wagons, no driver", "There are no bugs"),
     ("অন্য দিকের NOT PERMIT নেই, সুইচ CARGO_APPR_JE ব্যবহার করে, আর BARRIER_DOWN ফাঁকা", "ভুল সংকেত-রং, ধীর ট্রেন আর বৃষ্টি", "বেশি সংকেত, কম ওয়াগন, চালক নেই", "কোনো ত্রুটি নেই")),
    # Q180 editing rows
    (("Click input boxes to cycle inputs, NOT to invert, and AND/OR to switch; rows run top to bottom", "Type code in a text editor", "Rows cannot be edited", "Drag signals onto the rows"),
     ("ইনপুট-বাক্সে ক্লিক করে ইনপুট বদলাও, NOT দিয়ে উল্টাও, AND/OR দিয়ে জোড়-শব্দ বদলাও; সারি উপর থেকে নিচে চলে", "টেক্সট এডিটরে কোড লেখো", "সারি বদলানো যায় না", "সংকেত টেনে সারিতে বসাও")),
    # Q181 inputs
    (("Track sensors and permits, such as BRIDGE_OCC for a train on the bridge and XING_APPR for one nearing the crossing", "Weather readings", "Ticket counts", "Driver names"),
     ("লাইনের সেন্সর আর অনুমতি, যেমন সেতুতে ট্রেন থাকলে BRIDGE_OCC, আর লেভেল-ক্রসিংয়ের কাছে এলে XING_APPR", "আবহাওয়ার পাঠ", "টিকিটের সংখ্যা", "চালকদের নাম")),
    # Q182 350 m signal
    (("At 350 m the block was shorter than a train's braking distance, so a train passed a red", "350 m signals are a different colour", "Trains are faster near 350 m", "It was a random accident"),
     ("৩৫০ মিটারে ব্লক ট্রেনের থামার দূরত্বের চেয়ে ছোট ছিল, তাই একটা ট্রেন লাল পেরিয়ে গেল", "৩৫০ মিটারের সংকেত অন্য রঙের", "৩৫০ মিটারের কাছে ট্রেন দ্রুত চলে", "এলোমেলো দুর্ঘটনা")),
    # Q183 Level 5 bonus
    (("Zero SPADs and 1000 train-seconds of waiting or less - extra signals add waiting without adding capacity", "Delivering 100 trains", "Using every signal type", "Finishing in under one minute"),
     ("শূন্য বিপদ-অতিক্রম আর ১০০০ ট্রেন-সেকেন্ড বা কম অপেক্ষা — বাড়তি সংকেত ক্ষমতা না বাড়িয়ে অপেক্ষা বাড়ায়", "১০০টি ট্রেন পৌঁছানো", "সব রকম সংকেত ব্যবহার", "এক মিনিটের মধ্যে শেষ")),
    # Q184 fundamental diagram
    (("Flow = density x speed; flow peaks at half the jam density, then speed collapses", "Flow always rises with density", "Speed rises as density rises", "Flow is constant"),
     ("প্রবাহ = ঘনত্ব x গতি; জট-ঘনত্বের অর্ধেকে প্রবাহ সর্বোচ্চ, তারপর গতি ভেঙে পড়ে", "ঘনত্বের সঙ্গে প্রবাহ সবসময় বাড়ে", "ঘনত্ব বাড়লে গতি বাড়ে", "প্রবাহ স্থির")),
    # Q185 jams travel backwards
    (("The boundary moves at w = (q2 - q1)/(k2 - k1), which is negative, so the jam creeps upstream", "Cars drive backwards", "The road tilts", "Detectors are placed backwards"),
     ("সীমানা w = (q2 - q1)/(k2 - k1) গতিতে সরে, যা ঋণাত্মক, তাই জট উজানে পিছোয়", "গাড়ি পিছন দিকে চলে", "রাস্তা হেলে যায়", "সেন্সর উল্টো বসানো")),
    # Q186 signal tuning
    (("Capacity ≈ s x g / C; a 90 s cycle with 0.7 green to the main road passes, but idling stays high", "A 60 s cycle with 0.5 split is ideal", "Shorter green for the busy road", "Signals cannot be tuned"),
     ("ক্ষমতা ≈ s x g / C; ৯০ সেকেন্ডের চক্রে মূল রাস্তায় ০.৭ সবুজে পাস, কিন্তু অলস-সময় বেশি থাকে", "৬০ সেকেন্ডের চক্রে ০.৫ ভাগ আদর্শ", "ব্যস্ত রাস্তায় ছোট সবুজ", "সংকেত টিউন করা যায় না")),
    # Q187 roundabout or overpass
    (("The roundabout: no gridlock, idling under the bonus limit and under par - three stars", "The overpass, because zero idling always wins", "Signals, because they are cheapest", "None of them work"),
     ("গোলচত্বর: জট নেই, অলস-সময় বোনাস-সীমার নিচে আর সমমানের নিচে — তিন তারা", "উড়ালপুল, কারণ শূন্য অলস-সময় সবসময় জেতে", "সংকেত, কারণ সবচেয়ে সস্তা", "কোনোটাই কাজ করে না")),
    # Q188 IDM
    (("The Intelligent Driver Model: accelerate to the limit but keep a 1.2 s gap and brake smoothly", "Cars move at a fixed speed", "Cars ignore the car ahead", "Cars teleport between junctions"),
     ("বুদ্ধিমান চালক মডেল: সীমা পর্যন্ত গতি বাড়াও কিন্তু ১.২ সেকেন্ডের ফাঁক রাখো আর মসৃণভাবে ব্রেক করো", "গাড়ি স্থির গতিতে চলে", "গাড়ি সামনের গাড়ি উপেক্ষা করে", "গাড়ি এক মোড় থেকে আরেক মোড়ে লাফিয়ে যায়")),
    # Q189 three modes Level 9
    (("Road trucks, rail trains and river barges, each with its own cost, speed and transfer time", "Bicycles, buses and planes", "Only trucks", "Pipelines, drones and ships"),
     ("সড়কে ট্রাক, রেলে ট্রেন আর নদীতে বজরা — প্রতিটির নিজস্ব খরচ, গতি আর বদলের সময়", "সাইকেল, বাস আর বিমান", "শুধু ট্রাক", "পাইপলাইন, ড্রোন আর জাহাজ")),
    # Q190 safety index
    (("Risk grows per vehicle trip and kilometre, so hundreds of truck trips score low while rail and barge score high", "Safety depends only on the weather", "Trucks are always the safest", "The index is fixed at 95"),
     ("প্রতি যান-যাত্রা আর কিলোমিটারে ঝুঁকি বাড়ে, তাই শত শত ট্রাক-যাত্রায় কম নম্বর আর রেল-বজরায় বেশি", "নিরাপত্তা শুধু আবহাওয়ার উপর নির্ভর করে", "ট্রাক সবসময় সবচেয়ে নিরাপদ", "সূচক ৯৫-এ স্থির")),
    # Q191 working plans
    (("One 30-wagon train plus one barge, or two trains all by rail, both earn three stars", "All by 60 trucks earns three stars", "All by one train is fastest", "All by 6 barges is cheapest"),
     ("৩০ ওয়াগনের এক ট্রেন আর এক বজরা, অথবা দুই ট্রেনে সব রেলে — দুটোই তিন তারা", "৬০ ট্রাকে সব নিলে তিন তারা", "এক ট্রেনে সব নেওয়া সবচেয়ে দ্রুত", "৬ বজরায় সব নেওয়া সবচেয়ে সস্তা")),
    # Q192 30 wagons
    (("The 130 t loco's grip (about 383 kN) just covers 30 loaded wagons on the 1.2% grade; 33 slip", "The station is only 30 wagons long", "The law limits trains to 30 wagons", "More wagons make the train lighter"),
     ("১৩০ টনের ইঞ্জিনের আঁকড় (প্রায় ৩৮৩ কিলোনিউটন) ১.২% ঢালে ৩০টি বোঝাই ওয়াগন কোনোমতে সামলায়; ৩৩টিতে পিছলায়", "স্টেশন মাত্র ৩০ ওয়াগন লম্বা", "আইন ট্রেনকে ৩০ ওয়াগনে বেঁধেছে", "বেশি ওয়াগনে ট্রেন হালকা হয়")),
    # Q193 Pareto frontier
    (("The plans that no other plan beats on cost, time and safety all at once", "The cheapest plan only", "The border of the map", "Plans that use only trucks"),
     ("যে পরিকল্পনাগুলিকে অন্য কোনো পরিকল্পনা খরচ, সময় আর নিরাপত্তা তিনটেতেই একসঙ্গে হারায় না", "শুধু সবচেয়ে সস্তা পরিকল্পনা", "মানচিত্রের সীমানা", "শুধু ট্রাক ব্যবহার করা পরিকল্পনা")),
    # Q194 toll formula
    (("(tonnes x km) ÷ (hours x litres of fuel) x a payout scale - it rewards far, fast, fuel-light freight", "A fixed Rs 10 per truck", "Hours x litres", "Tonnes only"),
     ("(টন x কিলোমিটার) ÷ (ঘণ্টা x লিটার জ্বালানি) x প্রদান-মাপ — দূরে, দ্রুত, কম জ্বালানিতে মাল নিলে পুরস্কার", "প্রতি ট্রাকে স্থির ১০ টাকা", "ঘণ্টা x লিটার", "শুধু টন")),
    # Q195 budgets and pars
    (("Each level has its own, from Rs 2.50 L / Rs 1.00 L in Level 1 to Rs 1.00 Cr / Rs 70 L in Level 10", "Every level has the same budget", "Par is always higher than budget", "Budgets are secret"),
     ("প্রতিটি লেভেলের নিজস্ব, লেভেল ১-এ ২.৫০ লাখ / ১.০০ লাখ থেকে লেভেল ১০-এ ১.০০ কোটি / ৭০ লাখ", "সব লেভেলের বাজেট এক", "সমমান সবসময় বাজেটের বেশি", "বাজেট গোপন")),
    # Q196 two paths
    (("'Low cost, high skill' and 'High cost, robust' - try robust if stuck, then trim towards skilful", "Left bank and right bank", "Day and night modes", "Easy and impossible"),
     ("'কম খরচ, বেশি দক্ষতা' আর 'বেশি খরচ, মজবুত' — আটকে গেলে মজবুতটা চেষ্টা করো, তারপর দক্ষতার দিকে ছাঁটো", "বাঁ পাড় আর ডান পাড়", "দিন আর রাতের মোড", "সহজ আর অসম্ভব")),
    # Q197 stuck
    (("Read the Black Box, open the calculator on the failed part, read the walkthrough, try the robust path, then the Demo", "Quit the game", "Delete your save", "Keep pressing RUN without changes"),
     ("ব্ল্যাক বক্স পড়ো, ব্যর্থ অংশে ক্যালকুলেটর খোলো, নির্দেশিকা পড়ো, মজবুত পথ চেষ্টা করো, তারপর ডেমো", "খেলা ছেড়ে দাও", "সংরক্ষণ মুছে দাও", "কিছু না বদলে বারবার চালাও")),
    # Q198 failing cost
    (("Very little: you keep the design, earn EXP and get 30% back as salvage", "You lose all your money", "The level is locked forever", "You lose all your stars"),
     ("খুবই কম: নকশা থাকে, অভিজ্ঞতা মেলে আর ৩০% উদ্ধার-মূল্য ফেরত আসে", "সব টাকা হারাও", "লেভেল চিরকাল বন্ধ হয়", "সব তারা হারাও")),
    # Q199 browser / phone
    (("Yes - the browser version is the same game; click once to start and the first load takes 10-20 seconds", "No, only on a desktop", "Only on a games console", "Only offline in print"),
     ("হ্যাঁ — ব্রাউজার-সংস্করণ একই খেলা; শুরু করতে একবার ক্লিক করো, প্রথম লোডে ১০-২০ সেকেন্ড লাগে", "না, শুধু ডেস্কটপে", "শুধু গেম-কনসোলে", "শুধু ছাপা কাগজে")),
    # Q200 one rule
    (("Make it safe, then make it lean", "Make it as strong as possible", "Make it as cheap as possible", "Make it as tall as possible"),
     ("আগে নিরাপদ করো, তারপর ছিপছিপে করো", "যত শক্ত সম্ভব করো", "যত সস্তা সম্ভব করো", "যত উঁচু সম্ভব করো")),
)

assert len(_OPTS) == len(MONEY) == 50

ITEMS = tuple(mcq(it.q_en, en, 0, it.a_en, it.q_bn, bn, it.a_bn) for it, (en, bn) in zip(MONEY, _OPTS))
