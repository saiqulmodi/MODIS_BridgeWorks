"""বাংলা অনুবাদ - Bengali translations for everything the game shows.

EXACT: whole strings.  PATTERNS: strings with changing numbers (regular expressions).
Formulas, numbers and units are left as they are, so the maths reads the same in both
languages. KEEP lists the technical words that may stay in Latin letters.
"""
import re

# --- vocabulary used inside other strings ------------------------------------------------------
VOCAB = {
    # materials, shapes, member kinds
    "Timber": "কাঠ", "Steel": "ইস্পাত", "Concrete": "কংক্রিট", "Steel cable": "ইস্পাতের তার",
    "Carbon-fibre cable": "কার্বন-ফাইবার তার", "Nanotube cable": "ন্যানোটিউব তার",
    "Smart alloy": "স্মার্ট সংকর ধাতু", "Solid square": "নিরেট বর্গ", "I-beam": "আই-বিম",
    "Hollow box": "ফাঁপা বাক্স", "beam": "বিম", "deck": "ডেক", "cable": "তার",
    # trains
    "Tank engine": "ট্যাংক ইঞ্জিন", "Diesel shunter": "ডিজেল শান্টার",
    "Mainline diesel": "মেইনলাইন ডিজেল", "Double-header": "জোড়া ইঞ্জিন",
    "Freight loco": "মালবাহী ইঞ্জিন",
    # modes, roads, misc
    "Road": "সড়ক", "Rail": "রেল", "Barge": "বার্জ", "MAIN": "প্রধান সড়ক", "CROSS": "বাজার রাস্তা",
    "Signals": "ট্রাফিক সিগন্যাল", "Roundabout": "গোলচত্বর", "Overpass": "উড়ালসেতু",
    "none": "নেই", "light": "হালকা", "heavy": "ভারী", "dry": "শুকনো", "wet": "ভেজা",
    "left": "বাঁয়ে", "right": "ডানে", "cargo": "মালগাড়ি", "passenger": "যাত্রীবাহী",
    "main": "মূল লাইন", "harbor": "বন্দর",
}

FS_GRADES = {"FAILED": "ব্যর্থ", "RISKY": "ঝুঁকিপূর্ণ", "OPTIMAL": "সর্বোত্তম",
             "CONSERVATIVE": "বেশি সাবধানী", "OVER-ENGINEERED": "অতিরিক্ত মজবুত"}


def v(word):
    return VOCAB.get(word, EXACT.get(word, word))


EXACT = {
    # ---------------------------------------------------------------- menu & common
    "Calculate. Construct. Route.  -  a hard-physics engineering sandbox":
        "হিসাব করো। নির্মাণ করো। পথ গড়ো।  -  আসল পদার্থবিজ্ঞানের প্রকৌশল খেলা",
    "Click a level (or press 1-9, 0 for level 10).  Inside a level: C toggles the calculator, Esc returns here.":
        "একটি লেভেলে ক্লিক করো (বা 1-9 চাপো, লেভেল 10-এর জন্য 0)।  লেভেলের ভিতরে: C চাপলে ক্যালকুলেটর খোলে/বন্ধ হয়, Esc চাপলে এখানে ফেরো।",
    "Quit": "বন্ধ করো", "LOCKED": "তালাবদ্ধ", "DONE": "সম্পন্ন",
    "English / Bengali (F2)": "ইংরেজি / বাংলা (F2)",
    "Build a bridge": "সেতু বানাও", "Lay a railway": "রেললাইন পাতো",
    "Cast a cantilever": "ক্যান্টিলিভার ঢালাই করো", "Wire the signals": "সিগন্যালের তার জোড়ো",
    "Tame the traffic": "যানজট সামলাও", "Plan the freight": "মাল পরিবহনের পরিকল্পনা করো",
    "Tier 1": "স্তর 1", "Tier 2": "স্তর 2", "Tier 3": "স্তর 3", "Tier 4": "স্তর 4",
    "Tier 1: Foundations": "স্তর 1: ভিত্তি", "Tier 2: Rail & Gradients": "স্তর 2: রেল ও ঢাল",
    "Tier 3: Flow & Signalling": "স্তর 3: প্রবাহ ও সিগন্যাল",
    "Tier 4: Dynamic Systems": "স্তর 4: গতিশীল ব্যবস্থা",
    "Briefing": "নির্দেশনা", "Menu": "মেনু",
    "SCIENTIFIC CALCULATOR": "বৈজ্ঞানিক ক্যালকুলেটর", "Calculator": "ক্যালকুলেটর",
    "Click a beam, joint, vehicle or track to see its maths.":
        "কোনো বিম, জোড়, গাড়ি বা লাইনে ক্লিক করো - তার গণিত দেখো।",
    "TAPE": "হিসাবের খাতা",
    "(more cards below - pick a smaller selection)": "(আরও কার্ড আছে - ছোট কিছু বেছে নাও)",
    # briefing
    "Start building": "নির্মাণ শুরু করো", "TWO PATHS FORWARD": "সামনে এগোনোর দুই পথ",
    "SUCCESS": "সাফল্য", "BONUS STAR": "বোনাস তারা", "MATHS YOU WILL DISCOVER": "যে গণিত তুমি আবিষ্কার করবে",
    "CONTROLS": "নিয়ন্ত্রণ",
    # black box
    "BLACK BOX INVESTIGATION": "ব্ল্যাক বক্স তদন্ত", "Diagnose it - what went wrong?": "নির্ণয় করো - কী ভুল হয়েছিল?",
    "Level menu": "লেভেল মেনু",
    "Not quite - look at the formula and the chart again.": "ঠিক হয়নি - সূত্র আর চার্টটা আবার দেখো।",
    # results
    "MISSION COMPLETE": "মিশন সফল", "ALTERNATE ROUTE OPEN": "বিকল্প পথ খুলে গেছে",
    "Next level": "পরের লেভেল", "Improve design": "নকশা আরও ভালো করো",
    "Your designs: cost vs safety (Pareto frontier in gold)": "তোমার নকশাগুলো: খরচ বনাম নিরাপত্তা (সোনালি = প্যারেটো সীমান্ত)",
    "cost ->": "খরচ ->", "safety": "নিরাপত্তা", "Build cost": "নির্মাণ খরচ",
    "Factor of safety": "নিরাপত্তা গুণক", "Toll revenue (5 yr)": "টোল আয় (5 বছর)", "Profit": "লাভ",
    "Over-engineering penalty": "অতিরিক্ত মজবুতের জরিমানা", "Carbon footprint": "কার্বন পদচিহ্ন",
    "Worst member load": "সবচেয়ে বেশি ভার পাওয়া সদস্য", "Time": "সময়", "Route": "পথ", "Cost": "খরচ",
    "Lesson kept": "যা শিখলে", "Toll = (t x km)/(h x L)": "টোল = (t x km)/(h x L)",
    "Wind: f_n / U_crit": "বাতাস: f_n / U_crit", "Quake: T / C": "ভূমিকম্প: T / C",
    "Under-designed: it broke.": "দুর্বল নকশা: ভেঙে গেছে।",
    "Stands, but with too little margin for surprises.": "দাঁড়িয়ে আছে, কিন্তু হঠাৎ বিপদের জন্য যথেষ্ট ফাঁক নেই।",
    "Just right: safe without wasting money.": "একদম ঠিক: নিরাপদ, টাকাও নষ্ট হয়নি।",
    "Safe, but you paid for strength you don't need.": "নিরাপদ, কিন্তু অপ্রয়োজনীয় শক্তির জন্য বেশি টাকা খরচ হয়েছে।",
    "Far too heavy: profits are eaten by the extra steel.": "অনেক বেশি ভারী: বাড়তি ইস্পাত লাভ খেয়ে ফেলছে।",
    "OVER BUDGET": "বাজেট ছাড়িয়ে গেছে",
    "Use the calculator: aim for FS 1.5-2.0, not 5.": "ক্যালকুলেটর ব্যবহার করো: FS 1.5-2.0 লক্ষ্য রাখো, 5 নয়।",
    "load % (red) over time": "সময়ের সাথে ভার % (লাল)", "limit": "সীমা",

    # ---------------------------------------------------------------- level texts
    "The Creek Crossing": "খাঁড়ির সেতু", "The Timber Incline": "কাঠের ঢাল",
    "The Deep Canyon Pier": "গভীর গিরিখাতের স্তম্ভ", "Freight Mountain Pass": "মালবাহী পাহাড়ি গিরিপথ",
    "The Harbor Switchyard": "বন্দরের সুইচইয়ার্ড", "Urban Bottleneck": "শহরের যানজট-মোড়",
    "Gale-Force Gorge": "ঝড়ো হাওয়ার খাদ", "Earthquake Fault Viaduct": "ভূমিকম্প-ফাটলের উঁচু সেতু",
    "Heavy Industrial Corridor": "ভারী শিল্প করিডর", "The Continental Megastructure": "মহাদেশ-জোড়া মহাসেতু",
    # level 1
    "The bakery van must reach the village across Pebble Creek every morning. Build a road bridge across the 16 m gap.":
        "রুটির ভ্যানকে প্রতিদিন সকালে নুড়ি খাঁড়ির ওপারের গ্রামে পৌঁছাতে হয়। 16 m ফাঁকের উপর একটি সড়ক সেতু বানাও।",
    "Truss bridges like the old railway crossings of the 1800s use triangles because a triangle cannot change shape without changing the length of a side.":
        "1800-এর দশকের পুরনো রেল সেতুর মতো ট্রাস সেতুতে ত্রিভুজ ব্যবহার হয়, কারণ কোনো বাহুর দৈর্ঘ্য না বদলে ত্রিভুজের আকার বদলানো যায় না।",
    "Click any joint: all the arrows pulling on it always add up to zero, or it would move.":
        "যেকোনো জোড়ে ক্লিক করো: তার উপর সব তীরের যোগফল সবসময় শূন্য, নইলে জোড়টা নড়ে যেত।",
    "Click a beam and slide its area A: the stress drops as A grows.":
        "একটি বিমে ক্লিক করে তার ক্ষেত্রফল A স্লাইড করো: A বাড়লে পীড়ন কমে।",
    "Tension vs compression": "টান বনাম চাপ",
    "Top chords go blue-ish (pushed), bottom chords pull. Swap them and watch which ones buckle.":
        "উপরের কর্ড ঠেলা খায়, নিচের কর্ড টান খায়। জায়গা বদলে দেখো কোনগুলো বেঁকে যায়।",
    "Centre of mass": "ভরকেন্দ্র",
    "The van's weight moves along the deck - the worst moment is when it is in the middle.":
        "ভ্যানের ওজন ডেক বরাবর সরে - মাঝখানে থাকার সময়টাই সবচেয়ে কঠিন।",
    "Low cost, high skill": "কম খরচ, বেশি দক্ষতা", "High cost, robust": "বেশি খরচ, মজবুত",
    "A light timber Warren truss of perfect triangles.": "নিখুঁত ত্রিভুজের হালকা কাঠের ওয়ারেন ট্রাস।",
    "Chunky steel members everywhere - safe but pricey.": "সবখানে মোটা ইস্পাত - নিরাপদ কিন্তু দামি।",
    "The van (3.5 t) crosses and the bridge stands.": "ভ্যান (3.5 t) পার হয় এবং সেতু দাঁড়িয়ে থাকে।",
    "Factor of safety between 1.5 and 4 (not wasteful).": "নিরাপত্তা গুণক 1.5 থেকে 4-এর মধ্যে (অপচয় নয়)।",
    "Debris ford": "ধ্বংসাবশেষের অগভীর পারাপার",
    "Pile the fallen pieces into a low ford across the creek. Vans splash across slowly - half price, but it floods in the rains.":
        "ভেঙে পড়া টুকরো জড়ো করে খাঁড়িতে নিচু পারাপার বানাও। ভ্যান ধীরে জল ছিটিয়ে পার হয় - অর্ধেক দাম, কিন্তু বর্ষায় ডুবে যায়।",
    # level 2
    "Haul 120 t of logs from the valley sawmill up to the ridge-top timber yard on a narrow-gauge railway.":
        "উপত্যকার করাতকল থেকে 120 t কাঠের গুঁড়ি সরু-গেজ রেলে পাহাড়-চূড়ার কাঠের গুদামে তুলে নাও।",
    "Mountain railways are limited by adhesion: steel wheels on steel rails grip only about 30% of the weight resting on the driving wheels.":
        "পাহাড়ি রেলের সীমা আটকে ধরার শক্তি: ইস্পাতের লাইনে ইস্পাতের চাকা চালক-চাকার উপর থাকা ওজনের মাত্র প্রায় 30% আঁকড়ে ধরতে পারে।",
    "Drag a track handle steeper: the red gravity arrow grows.": "লাইনের একটি হ্যান্ডেল টেনে খাড়া করো: লাল মাধ্যাকর্ষণ তীর বড় হয়।",
    "The grip (adhesion) depends on the weight pressing down.": "আঁকড়ে ধরা (আসঞ্জন) নির্ভর করে নিচে চাপ দেওয়া ওজনের উপর।",
    "Too many wagons and the wheels spin: the engine cannot pull more than mu times its own weight.":
        "ওয়াগন বেশি হলে চাকা পিছলে ঘোরে: ইঞ্জিন নিজের ওজনের mu গুণের বেশি টানতে পারে না।",
    "Tractive effort T = min(P/v, mu N)": "টানার বল T = min(P/v, mu N)",
    "Watch the engine's pull fall as speed rises.": "দেখো, গতি বাড়লে ইঞ্জিনের টান কমে যায়।",
    "Small engine, fewer wagons per trip, more trips.": "ছোট ইঞ্জিন, প্রতি ট্রিপে কম ওয়াগন, বেশি ট্রিপ।",
    "Hire a banker (pusher) engine and haul everything at once.": "পিছন থেকে ঠেলার (ব্যাংকার) ইঞ্জিন ভাড়া করে সব একবারে নিয়ে যাও।",
    "Deliver 120 t to the ridge yard within 2 minutes without stalling.": "না থেমে 2 মিনিটের মধ্যে 120 t চূড়ার গুদামে পৌঁছে দাও।",
    "Spend less than the par cost.": "প্যার খরচের চেয়ে কম খরচ করো।",
    "Cable winch": "তারের উইঞ্চ",
    "Rig a winch at the top and drag wagons up the slope one at a time - slow, but it never stalls.":
        "উপরে একটি উইঞ্চ বসিয়ে একটা একটা করে ওয়াগন ঢাল বেয়ে টেনে তোলো - ধীর, কিন্তু কখনো আটকায় না।",
    # level 3
    "Span the 66 m Raven Canyon with a concrete girder built outward from two tall piers - no scaffolding can reach the canyon floor.":
        "দুটি উঁচু স্তম্ভ থেকে বাইরের দিকে কংক্রিট গার্ডার বানিয়ে 66 m চওড়া রেভেন গিরিখাত পার হও - কোনো ভারা গিরিখাতের তলা পর্যন্ত পৌঁছায় না।",
    "Balanced-cantilever bridges grow like a see-saw: a segment on one side must be matched on the other, or the pier tips over.":
        "ভারসাম্য-ক্যান্টিলিভার সেতু ঢেঁকির মতো বাড়ে: এক পাশে একটি অংশ দিলে অন্য পাশেও দিতে হয়, নইলে স্তম্ভ উল্টে যায়।",
    "Sum M_pier = Sum W_right x - Sum W_left x": "Sum M_pier = Sum W_right x - Sum W_left x",
    "The see-saw meter swings each time you cast a segment.": "প্রতিবার একটি অংশ ঢালাই করলে ঢেঁকি-মিটার দোলে।",
    "The pier root feels the biggest bending moment.": "স্তম্ভের গোড়ায় সবচেয়ে বড় বাঁকানো ভ্রামক পড়ে।",
    "Double the haunch depth d and the girder gets 8x stiffer.": "হঞ্চের গভীরতা d দ্বিগুণ করলে গার্ডার 8 গুণ শক্ত হয়।",
    "Shear is largest next to the supports.": "সাপোর্টের পাশেই কর্তন বল সবচেয়ে বেশি।",
    "Continuous beam": "অবিচ্ছিন্ন বিম",
    "Stitching the middle changes cantilevers into one beam: watch the moment diagram flip.":
        "মাঝখান জুড়ে দিলে ক্যান্টিলিভারগুলো একটি বিম হয়ে যায়: ভ্রামকের ছবি উল্টে যেতে দেখো।",
    "Perfectly alternate segments, slim haunch, light post-tensioning.": "নিখুঁতভাবে পালাক্রমে অংশ, সরু হঞ্চ, হালকা পোস্ট-টেনশনিং।",
    "Deep haunch, tie-downs on both piers, heavy post-tensioning.": "গভীর হঞ্চ, দুই স্তম্ভেই বাঁধন-তার, ভারী পোস্ট-টেনশনিং।",
    "Both piers stand, the stitch is closed, and a 40 t truck crosses.": "দুই স্তম্ভ দাঁড়িয়ে থাকে, মাঝখান জোড়া হয়, এবং 40 t ট্রাক পার হয়।",
    "Girder factor of safety between 1.5 and 4 under the truck.": "ট্রাকের নিচে গার্ডারের নিরাপত্তা গুণক 1.5 থেকে 4-এর মধ্যে।",
    "Steel launch girder": "ইস্পাতের লঞ্চিং গার্ডার",
    "Re-use the formwork travellers as a temporary steel launching truss to finish the span the slow way.":
        "ফর্মওয়ার্ক ট্রাভেলারগুলোকে অস্থায়ী ইস্পাতের লঞ্চিং ট্রাস বানিয়ে ধীরে ধীরে বাকি অংশ শেষ করো।",
    # level 4
    "Move 600 t of copper ore over Eagle Pass to the smelter terminal. Rain is forecast on the far side of the summit.":
        "600 t তামার আকরিক ঈগল গিরিপথ পেরিয়ে গলানোর কারখানার টার্মিনালে নিয়ে যাও। চূড়ার ওপারে বৃষ্টির পূর্বাভাস আছে।",
    "Heavy trains carry enormous momentum p = m v. Climbing turns it into height; descending, the brakes must turn it all into heat.":
        "ভারী ট্রেনের ভরবেগ p = m v বিশাল। উঠতে গেলে তা উচ্চতায় বদলায়; নামতে গেলে ব্রেককে সবটা তাপে বদলাতে হয়।",
    "Momentum carries the train over a short steep crest.": "ভরবেগ ট্রেনকে ছোট খাড়া চূড়া পার করিয়ে দেয়।",
    "The energy bars swap as the train climbs and descends.": "ট্রেন ওঠা-নামার সাথে শক্তির বারগুলো জায়গা বদলায়।",
    "Move the brake marker: too late on wet rails and you hit the buffers.": "ব্রেক-চিহ্ন সরাও: ভেজা লাইনে দেরি হলে বাফারে ধাক্কা লাগবে।",
    "Runaway when g sin(theta) > mu g cos(theta)": "g sin(theta) > mu g cos(theta) হলে ট্রেন নিয়ন্ত্রণ হারায়",
    "Make a descent too steep and no brake can hold the train.": "নামার ঢাল খুব খাড়া হলে কোনো ব্রেকই ট্রেন ধরে রাখতে পারে না।",
    "One locomotive, smart grades, careful braking point.": "একটি ইঞ্জিন, বুদ্ধিমান ঢাল, সাবধানী ব্রেক-বিন্দু।",
    "Double-header locomotives and expensive gentle earthworks.": "জোড়া ইঞ্জিন আর দামি মৃদু মাটির কাজ।",
    "Deliver 600 t to the terminal within 8 minutes and stop before the buffers.":
        "8 মিনিটের মধ্যে 600 t টার্মিনালে পৌঁছাও এবং বাফারের আগে থামো।",
    "Stop within 15 m of the stop line.": "থামার দাগের 15 m-এর মধ্যে থামো।",
    "Bypass spur": "বিকল্প শাখা লাইন",
    "Lay a short spur at the bottom of the descent so a runaway train can coast safely uphill to a stop.":
        "নামার নিচে একটি ছোট শাখা লাইন পাতো, যাতে নিয়ন্ত্রণহারা ট্রেন নিরাপদে চড়াই বেয়ে থেমে যায়।",
    # level 5
    "Passenger and cargo trains share one single-track bridge into Port Kavi. Cargo must go to the harbor siding, passengers to the main line - and nobody may meet head-on.":
        "যাত্রী আর মালবাহী ট্রেন পোর্ট কাভির এক-লাইনের সেতু ভাগ করে নেয়। মালগাড়ি যাবে বন্দরের সাইডিংয়ে, যাত্রী ট্রেন মূল লাইনে - আর কেউ মুখোমুখি হবে না।",
    "Real railways divide track into blocks with signals; interlocking logic stops two trains ever being given conflicting routes.":
        "আসল রেলপথ সিগন্যাল দিয়ে লাইনকে ব্লকে ভাগ করে; ইন্টারলকিং লজিক দুটি ট্রেনকে কখনো সংঘর্ষের পথ দেয় না।",
    "Place a signal too close to the next one and a fast train sails past the red (SPAD).":
        "পরের সিগন্যালের খুব কাছে সিগন্যাল দিলে দ্রুত ট্রেন লাল পেরিয়ে চলে যায় (SPAD)।",
    "3-aspect: RED / YELLOW / GREEN": "3-আলোর সিগন্যাল: লাল / হলুদ / সবুজ",
    "Watch aspects ripple back behind every train.": "দেখো, প্রতিটি ট্রেনের পিছনে সিগন্যালের রং ঢেউয়ের মতো পিছিয়ে যায়।",
    "Logic gates AND / OR / NOT": "লজিক গেট AND / OR / NOT",
    "Wire PERMIT_EB = APPR_EB AND NOT BRIDGE_OCC AND NOT PERMIT_WB to lock out head-on moves.":
        "মুখোমুখি চলা আটকাতে PERMIT_EB = APPR_EB AND NOT BRIDGE_OCC AND NOT PERMIT_WB জোড়ো।",
    "Headway": "দুই ট্রেনের ব্যবধান",
    "More, shorter blocks let trains follow closer - if they can still stop.":
        "বেশি আর ছোট ব্লক থাকলে ট্রেন কাছাকাছি চলতে পারে - যদি তবুও থামতে পারে।",
    "Few, well-spaced 3-aspect signals and tight logic.": "অল্প কিছু, ঠিক দূরত্বে 3-আলোর সিগন্যাল আর নিখুঁত লজিক।",
    "Many 4-aspect signals for short blocks and high capacity.": "ছোট ব্লক আর বেশি ক্ষমতার জন্য অনেক 4-আলোর সিগন্যাল।",
    "Run 12 minutes with no collision, derailment or crossing incident, deliver at least 10 trains and send every cargo train to the harbor.":
        "12 মিনিট চালাও কোনো সংঘর্ষ, লাইনচ্যুতি বা ক্রসিং দুর্ঘটনা ছাড়া, কমপক্ষে 10টি ট্রেন পৌঁছাও এবং প্রতিটি মালগাড়ি বন্দরে পাঠাও।",
    "Zero SPADs and total waiting under 1000 train-seconds.": "শূন্য SPAD এবং মোট অপেক্ষা 1000 ট্রেন-সেকেন্ডের কম।",
    "Cable ferry": "তারের ফেরি",
    "Run cargo wagons across the bay on a cable ferry instead of the bridge - slower, but it frees the single track for passengers.":
        "সেতুর বদলে তারের ফেরিতে মালবাহী ওয়াগন উপসাগর পার করাও - ধীর, কিন্তু এক-লাইনের সেতু যাত্রীদের জন্য খালি থাকে।",
    # level 6
    "Rush hour at Gandhi Chowk: the main road and the market street cross at one junction. Keep the city moving.":
        "গান্ধী চকে ভিড়ের সময়: প্রধান সড়ক আর বাজার রাস্তা একটি মোড়ে মেলে। শহরকে চলমান রাখো।",
    "Traffic behaves like a fluid: flow q = k v rises with density k until a critical point, then collapses into a jam that travels backwards.":
        "যানবাহন তরলের মতো আচরণ করে: প্রবাহ q = k v ঘনত্ব k-এর সাথে একটি সংকট-বিন্দু পর্যন্ত বাড়ে, তারপর ভেঙে জ্যাম হয়ে পিছনের দিকে ছড়ায়।",
    "The fundamental diagram plots every detector reading live.": "মৌলিক চিত্রে প্রতিটি সেন্সরের পাঠ সরাসরি আঁকা হয়।",
    "Greenshields: speed falls as cars pack closer.": "গ্রিনশিল্ডস: গাড়ি কাছাকাছি হলে গতি কমে।",
    "Push demand past q_max and a queue is born.": "চাহিদা q_max ছাড়ালেই লাইন তৈরি হয়।",
    "Watch the red shockwave crawl backwards in the heat map.": "তাপ-মানচিত্রে লাল শকওয়েভকে পিছনে হামাগুড়ি দিতে দেখো।",
    "IDM car-following": "IDM গাড়ি-অনুসরণ মডেল",
    "Each car keeps a safe time gap T = 1.2 s to the one ahead.": "প্রতিটি গাড়ি সামনের গাড়ি থেকে T = 1.2 s নিরাপদ সময়ের ফাঁক রাখে।",
    "Tune signal cycle and green split, or merge with a roundabout.": "সিগন্যালের চক্র আর সবুজের ভাগ ঠিক করো, বা গোলচত্বরে মিলিয়ে দাও।",
    "Build a grade-separated overpass: no conflict at all.": "আলাদা উচ্চতার উড়ালসেতু বানাও: কোনো সংঘাতই নেই।",
    "12 minutes of rush hour without gridlock, main-road trips no more than 1.8x the free-flow time.":
        "12 মিনিটের ভিড়ে কোনো অচল জট নেই, প্রধান সড়কের যাত্রা মুক্ত-প্রবাহের সময়ের 1.8 গুণের বেশি নয়।",
    "Idling under 4000 car-seconds (less pollution).": "অলস দাঁড়িয়ে থাকা 4000 গাড়ি-সেকেন্ডের কম (কম দূষণ)।",
    "Bypass lane": "বিকল্প লেন",
    "Open a temporary bypass through the bus depot to drain the queue.": "লাইন খালি করতে বাস ডিপোর ভিতর দিয়ে একটি অস্থায়ী বিকল্প পথ খোলো।",
    # level 7
    "Build a 48 m bus bridge across Whistling Gorge, where the wind builds from a breeze to a 36 m/s gale every afternoon.":
        "শিস-দেওয়া খাদের উপর 48 m বাস সেতু বানাও, যেখানে প্রতি বিকেলে বাতাস মৃদু হাওয়া থেকে 36 m/s ঝড়ে পরিণত হয়।",
    "In 1940 the Tacoma Narrows Bridge twisted itself apart in a 19 m/s wind because the wind pushed it in time with its own natural swing.":
        "1940 সালে ট্যাকোমা ন্যারোস সেতু মাত্র 19 m/s বাতাসে মুচড়ে ভেঙে পড়েছিল, কারণ বাতাস সেতুর নিজের স্বাভাবিক দোলনের তালে তালে ধাক্কা দিচ্ছিল।",
    "Stiffer (bigger k) or lighter (smaller m) raises the natural frequency.": "বেশি শক্ত (বড় k) বা হালকা (ছোট m) হলে স্বাভাবিক কম্পাঙ্ক বাড়ে।",
    "Vortices peel off the deck faster as the wind speeds up.": "বাতাসের গতি বাড়লে ডেক থেকে ঘূর্ণি আরও দ্রুত খসে পড়ে।",
    "The calculator predicts the wind speed where they match.": "ক্যালকুলেটর বলে দেয় কোন বাতাসের গতিতে দুটো মিলে যাবে।",
    "Tuned mass damper": "টিউনড মাস ড্যাম্পার",
    "Slide its mass and tuning until the swing dies away.": "দোলন থেমে না যাওয়া পর্যন্ত এর ভর আর টিউনিং স্লাইড করো।",
    "A light bridge plus a well-tuned mass damper or fairings.": "হালকা সেতু আর ভালোভাবে টিউন করা মাস ড্যাম্পার বা ফেয়ারিং।",
    "A deep, stiff truss whose natural frequency stays above anything the wind can excite.":
        "গভীর, শক্ত ট্রাস যার স্বাভাবিক কম্পাঙ্ক বাতাস যা নাড়াতে পারে তার চেয়ে বেশি থাকে।",
    "Four buses cross while the wind sweeps from 4 to 36 m/s, and the bridge survives.":
        "বাতাস 4 থেকে 36 m/s-এ ওঠার সময় চারটি বাস পার হয় এবং সেতু টিকে থাকে।",
    "Factor of safety between 1.5 and 4.": "নিরাপত্তা গুণক 1.5 থেকে 4-এর মধ্যে।",
    "Cable car": "রোপওয়ে কেবল কার",
    "String a cable car across the gorge from the surviving towers.": "টিকে থাকা টাওয়ার থেকে খাদের উপর দিয়ে একটি কেবল কার টানো।",
    # level 8
    "A highway viaduct must cross the Kutch fault valley. A magnitude-7 tremor is expected while traffic is on the bridge.":
        "একটি মহাসড়কের উঁচু সেতুকে কচ্ছের ফাটল-উপত্যকা পার হতে হবে। সেতুতে গাড়ি থাকার সময় মাত্রা-7 ভূমিকম্প আশা করা হচ্ছে।",
    "Modern bridges in earthquake zones often sit on rubber-and-lead isolation bearings that let the ground move underneath while the deck glides.":
        "ভূমিকম্প-প্রবণ এলাকার আধুনিক সেতু প্রায়ই রাবার-সীসার আইসোলেশন বিয়ারিংয়ের উপর বসানো থাকে, যাতে নিচে মাটি নড়লেও ডেক মসৃণভাবে ভেসে থাকে।",
    "The seismograph trace shows the pulse.": "সিসমোগ্রাফের রেখায় কম্পন দেখা যায়।",
    "Heavier bridges and stiff (short-period) bridges feel more force.": "ভারী সেতু আর শক্ত (ছোট পর্যায়কালের) সেতু বেশি বল অনুভব করে।",
    "Isolation bearings lengthen T and drop C from 2.5 to 0.5.": "আইসোলেশন বিয়ারিং T লম্বা করে এবং C-কে 2.5 থেকে 0.5-এ নামায়।",
    "...but the deck now swings further - add flexible joints.": "...কিন্তু এখন ডেক বেশি দূর দোলে - নমনীয় জোড় যোগ করো।",
    "Slender piers on isolation bearings with flexible joints.": "আইসোলেশন বিয়ারিং ও নমনীয় জোড়সহ সরু স্তম্ভ।",
    "Massive X-braced steel piers that resist the full shaking.": "পুরো কাঁপুনি সামলানো বিশাল X-বন্ধনীর ইস্পাতের স্তম্ভ।",
    "A 20 t truck crosses during the earthquake and the viaduct stands.": "ভূমিকম্পের সময় 20 t ট্রাক পার হয় এবং উঁচু সেতু দাঁড়িয়ে থাকে।",
    "Ground-level road": "মাটির স্তরের রাস্তা",
    "Grade a winding road down into the valley across the debris.": "ধ্বংসাবশেষের উপর দিয়ে উপত্যকায় নামার একটি আঁকাবাঁকা রাস্তা বানাও।",
    # level 9
    "The Bhilwara mine must ship 6000 t of ore to Kandla port within 24 hours. Road, rail and river barge are all available - choose the mix.":
        "ভিলওয়াড়া খনিকে 24 ঘণ্টার মধ্যে 6000 t আকরিক কান্ডলা বন্দরে পাঠাতে হবে। সড়ক, রেল আর নদীর বার্জ - সবই আছে, মিশ্রণ তুমি বেছে নাও।",
    "Real logistics planners solve exactly this with linear programming: the cheapest mix that still meets the deadline and the safety target.":
        "আসল পরিবহন-পরিকল্পনাকারীরা ঠিক এটাই লিনিয়ার প্রোগ্রামিং দিয়ে সমাধান করেন: সবচেয়ে সস্তা মিশ্রণ যা সময়সীমা আর নিরাপত্তার লক্ষ্য পূরণ করে।",
    "Hire too many trucks and they slow each other down.": "বেশি ট্রাক ভাড়া করলে তারা একে অপরকে ধীর করে দেয়।",
    "The train's speed on the 1.2% grade.": "1.2% ঢালে ট্রেনের গতি।",
    "Over 30 wagons and one loco stalls on the grade.": "30টির বেশি ওয়াগন হলে একটি ইঞ্জিন ঢালে আটকে যায়।",
    "Fast, fuel-light deliveries earn the best payout.": "দ্রুত, কম জ্বালানির ডেলিভারিতে সবচেয়ে বেশি টাকা মেলে।",
    "Pareto frontier": "প্যারেটো সীমান্ত",
    "No plan on the frontier can be beaten on cost, time and safety all at once.":
        "সীমান্তের কোনো পরিকল্পনাকে খরচ, সময় আর নিরাপত্তা - তিনটিতেই একসাথে হারানো যায় না।",
    "A rail-and-barge mix tuned to the deadline.": "সময়সীমা অনুযায়ী সাজানো রেল আর বার্জের মিশ্রণ।",
    "Flood the road with trucks - fast but costly and less safe.": "রাস্তা ট্রাকে ভরে দাও - দ্রুত কিন্তু দামি আর কম নিরাপদ।",
    "All 6000 t delivered within 24 h and within budget.": "24 h-এর মধ্যে এবং বাজেটের মধ্যে সব 6000 t পৌঁছানো।",
    "Safety index of 95 or more.": "নিরাপত্তা সূচক 95 বা তার বেশি।",
    "Split shipment": "ভাগ করা চালান",
    "Ship the urgent half now and the rest next week at a penalty.": "জরুরি অর্ধেক এখন পাঠাও, বাকিটা পরের সপ্তাহে জরিমানা দিয়ে।",
    # level 10
    "Link two continents across the 64 m Sapphire Strait with a maglev crossing powered by the new smart grid - in a rising wind.":
        "নতুন স্মার্ট গ্রিডে চলা ম্যাগলেভ পারাপার দিয়ে 64 m চওড়া স্যাফায়ার প্রণালীর দুই পাড়ের মহাদেশ জোড়ো - বাড়তে থাকা বাতাসের মধ্যে।",
    "Everything you have learned at once: cables, towers, resonance, power budgets and materials from the future.":
        "যা কিছু শিখেছ সব একসাথে: তার, টাওয়ার, অনুনাদ, বিদ্যুতের বাজেট আর ভবিষ্যতের উপকরণ।",
    "Cables: tension only": "তার: শুধু টান",
    "Cables go slack (grey) if you ask them to push.": "তারকে ঠেলতে বললে তা ঢিলা (ধূসর) হয়ে যায়।",
    "Cable-stayed towers": "তার-ঝোলানো টাওয়ার",
    "Tall towers turn the deck load into cable tension and tower compression.": "উঁচু টাওয়ার ডেকের ভারকে তারের টান আর টাওয়ারের চাপে বদলে দেয়।",
    "The maglev pod's thrust needs power from the smart grid.": "ম্যাগলেভ পডের ধাক্কার জন্য স্মার্ট গ্রিড থেকে বিদ্যুৎ লাগে।",
    "Smart alloy: E x 2 when powered": "স্মার্ট সংকর: বিদ্যুৎ পেলে E x 2",
    "Stiffen the bridge by spending grid power.": "গ্রিডের বিদ্যুৎ খরচ করে সেতু শক্ত করো।",
    "The wind still wants to make it dance.": "বাতাস এখনও একে নাচাতে চায়।",
    "Steel deck truss with a few carbon stays and a TMD.": "কয়েকটি কার্বন তার আর একটি TMD-সহ ইস্পাতের ডেক ট্রাস।",
    "Nanotube cables, smart-alloy towers and a big grid.": "ন্যানোটিউব তার, স্মার্ট-সংকরের টাওয়ার আর বড় গ্রিড।",
    "The maglev pod train crosses in under 9.5 s while the wind rises to 22 m/s.":
        "বাতাস 22 m/s-এ ওঠার সময় ম্যাগলেভ পড ট্রেন 9.5 s-এর কম সময়ে পার হয়।",
    "Hyperloop ferry": "হাইপারলুপ ফেরি",
    "Float the maglev pods across in a sealed ferry tube.": "সিল করা ফেরি টিউবে ম্যাগলেভ পডগুলো ভাসিয়ে পার করাও।",

    # ---------------------------------------------------------------- failure causes & lessons
    "A member in compression buckled (P > P_cr)": "চাপে থাকা একটি সদস্য বেঁকে ভেঙেছে (P > P_cr)",
    "Long thin struts bow sideways. Shorten them, brace them, or use a shape with a bigger I (I-beam, hollow box): P_cr = pi^2 E I / (K L)^2.":
        "লম্বা সরু দণ্ড পাশে বেঁকে যায়। ছোট করো, বন্ধনী দাও, বা বড় I-এর আকার নাও (আই-বিম, ফাঁপা বাক্স): P_cr = pi^2 E I / (K L)^2।",
    "A member was over-stressed (sigma = N/A too big)": "একটি সদস্যের উপর অতিরিক্ত পীড়ন (sigma = N/A খুব বড়)",
    "Give the member more area A, a stronger material, or share the load with more triangles.":
        "সদস্যকে বেশি ক্ষেত্রফল A দাও, শক্ত উপকরণ দাও, বা আরও ত্রিভুজে ভার ভাগ করো।",
    "The frame was a mechanism - not enough triangles": "কাঠামোটা নড়বড়ে যন্ত্রের মতো ছিল - ত্রিভুজ যথেষ্ট নয়",
    "Squares fold up. Every panel needs a diagonal so the joints cannot slide.":
        "বর্গক্ষেত্র ভাঁজ হয়ে যায়। প্রতিটি খোপে একটি কর্ণ লাগে যাতে জোড় পিছলে না যায়।",
    "The slope pulled back harder than the engine could pull": "ঢাল ইঞ্জিনের টানার চেয়ে জোরে পিছনে টেনেছে",
    "m g sin(theta) grows with steepness. Flatten the grade, add power, or carry less.":
        "খাড়াই বাড়লে m g sin(theta) বাড়ে। ঢাল কমাও, শক্তি বাড়াও, বা কম মাল নাও।",
    "The train could not stop in the distance it had": "ট্রেন হাতে থাকা দূরত্বে থামতে পারেনি",
    "d_stop = v^2 / (2 (mu g cos(theta) - g sin(theta))). Brake earlier or approach slower.":
        "d_stop = v^2 / (2 (mu g cos(theta) - g sin(theta)))। আগে ব্রেক করো বা ধীরে এগোও।",
    "Gravity beat the brakes on the descent": "নামার পথে মাধ্যাকর্ষণ ব্রেককে হারিয়ে দিয়েছে",
    "If g sin(theta) > mu g cos(theta) no brake can stop you. Make the descent gentler.":
        "g sin(theta) > mu g cos(theta) হলে কোনো ব্রেক থামাতে পারবে না। নামার ঢাল মৃদু করো।",
    "Two trains were allowed into the same block": "দুটি ট্রেনকে একই ব্লকে ঢুকতে দেওয়া হয়েছে",
    "Signals must warn at least d_stop ahead, and the single track needs an interlock.":
        "সিগন্যালকে অন্তত d_stop আগে সতর্ক করতে হবে, আর এক-লাইনের পথে ইন্টারলক লাগে।",
    "A switch moved under (or just before) a train": "ট্রেনের নিচে (বা ঠিক আগে) পয়েন্ট সরে গেছে",
    "Lock switches while their track circuit is occupied.": "লাইনে ট্রেন থাকার সময় পয়েন্ট তালাবদ্ধ রাখো।",
    "Trains were sent down the wrong route": "ট্রেন ভুল পথে পাঠানো হয়েছে",
    "Switches must follow the train type: cargo to the harbor, passengers to the main line.":
        "পয়েন্ট ট্রেনের ধরন মেনে চলবে: মালগাড়ি বন্দরে, যাত্রী ট্রেন মূল লাইনে।",
    "The level-crossing barrier was not down in time": "লেভেল-ক্রসিংয়ের গেট সময়মতো নামেনি",
    "Barriers take seconds to fall; trigger them from far enough out.": "গেট নামতে কয়েক সেকেন্ড লাগে; যথেষ্ট দূর থেকে চালু করো।",
    "Demand was higher than the junction's capacity": "চাহিদা মোড়ের ক্ষমতার চেয়ে বেশি ছিল",
    "q = k v peaks at k_crit. Above it, queues grow and shockwaves travel backwards.":
        "q = k v সর্বোচ্চ হয় k_crit-এ। তার বেশি হলে লাইন বাড়ে আর শকওয়েভ পিছনে ছড়ায়।",
    "The pier tipped: the see-saw was out of balance": "স্তম্ভ উল্টে গেছে: ঢেঁকির ভারসাম্য ছিল না",
    "sum(W x) on one side must stay within the foundation's resistance. Alternate sides or add tie-downs.":
        "এক পাশের sum(W x) ভিত্তির সহ্যক্ষমতার মধ্যে থাকতে হবে। পালাক্রমে দুই পাশে দাও বা বাঁধন-তার যোগ করো।",
    "The girder cracked at the pier: bending stress too high": "স্তম্ভের কাছে গার্ডার ফেটেছে: বাঁকানো পীড়ন খুব বেশি",
    "sigma = M y / I and I = b d^3 / 12: a deeper haunch at the pier helps a lot.":
        "sigma = M y / I এবং I = b d^3 / 12: স্তম্ভের কাছে গভীর হঞ্চ অনেক সাহায্য করে।",
    "The finished girder was over-stressed by the truck": "তৈরি গার্ডারে ট্রাক অতিরিক্ত পীড়ন দিয়েছে",
    "Post-tensioning adds pre-compression; a deeper mid-span section raises I.":
        "পোস্ট-টেনশনিং আগে থেকে চাপ যোগ করে; মাঝখানের গভীর অংশ I বাড়ায়।",
    "Wind vortices pushed in step with the bridge's natural swing": "বাতাসের ঘূর্ণি সেতুর স্বাভাবিক দোলনের তালে ধাক্কা দিয়েছে",
    "When f_v = St U / D matches f_n the swing grows. Detune (stiffen), add damping, a tuned mass damper, or fairings.":
        "f_v = St U / D যখন f_n-এর সমান হয় দোলন বাড়ে। কম্পাঙ্ক সরাও (শক্ত করো), অবমন্দন দাও, টিউনড মাস ড্যাম্পার বা ফেয়ারিং দাও।",
    "The isolated deck swung into the abutment": "বিচ্ছিন্ন ডেক দুলে পাড়ের দেয়ালে ধাক্কা খেয়েছে",
    "Seismic isolation lowers forces but increases movement: add flexible joints.":
        "ভূমিকম্প-বিচ্ছিন্নতা বল কমায় কিন্তু নড়াচড়া বাড়ায়: নমনীয় জোড় যোগ করো।",
    "Earthquake base shear broke the supports": "ভূমিকম্পের ভিত্তি-কর্তন বল সাপোর্ট ভেঙে দিয়েছে",
    "V = C M a_g. Brace the piers, or isolate the deck to lengthen the period and cut C.":
        "V = C M a_g। স্তম্ভে বন্ধনী দাও, বা পর্যায়কাল লম্বা করে C কমাতে ডেক বিচ্ছিন্ন করো।",
    "The job took longer than the deadline": "কাজ সময়সীমার চেয়ে বেশি সময় নিয়েছে",
    "Speed comes from power, gentle grades and fewer bottlenecks.": "গতি আসে শক্তি, মৃদু ঢাল আর কম বাধা থেকে।",
    "The smart grid ran out of power": "স্মার্ট গ্রিডের বিদ্যুৎ ফুরিয়ে গেছে",
    "Maglev thrust and smart-alloy stiffening share one power budget.": "ম্যাগলেভের ধাক্কা আর স্মার্ট-সংকরের শক্ত হওয়া একই বিদ্যুৎ-বাজেট ভাগ করে।",
    "The design cost more than the budget": "নকশার খরচ বাজেটের চেয়ে বেশি",

    # ---------------------------------------------------------------- bridge screens
    "Select": "বাছাই", "Deck": "ডেক", "Beam": "বিম", "Cable": "তার", "Delete": "মুছো",
    "Undo": "ফেরাও", "Clear": "সব মুছো", "TEST": "পরীক্ষা", "Vectors": "বল-তীর",
    "RUN": "চালাও", "STOP": "থামাও", "EDIT": "সম্পাদনা",
    "Steel": "ইস্পাত", "Timber": "কাঠ", "Concrete": "কংক্রিট", "Steel cable": "ইস্পাতের তার",
    "Carbon-fibre cable": "কার্বন-ফাইবার তার", "Nanotube cable": "ন্যানোটিউব তার",
    "Smart alloy": "স্মার্ট সংকর ধাতু", "I-beam": "আই-বিম", "Hollow box": "ফাঁপা বাক্স",
    "Solid square": "নিরেট বর্গ",
    "Pick a tool, then click a start point and an end point (or drag). Deck = road the vehicle drives on. Right-click deletes. Ctrl+Z undo. Select tool + click a beam/joint/vehicle shows its maths. SPACE runs the test.":
        "একটি টুল বেছে নাও, তারপর শুরুর আর শেষের বিন্দুতে ক্লিক করো (বা টেনে আনো)। ডেক = যে রাস্তায় গাড়ি চলে। ডান-ক্লিকে মোছে। Ctrl+Z আগের অবস্থা। বাছাই টুল দিয়ে বিম/জোড়/গাড়িতে ক্লিক করলে তার গণিত দেখায়। SPACE চাপলে পরীক্ষা চলে।",
    "Live stress colours with the vehicle at its worst position.": "গাড়ি সবচেয়ে কঠিন জায়গায় থাকলে পীড়নের রং সরাসরি দেখাও।",
    "Show force arrows (length = kN).": "বলের তীর দেখাও (দৈর্ঘ্য = kN)।",
    "Exaggerate deflection 10x / 50x so you can see the sag and bulge.": "বাঁকা হওয়াকে 10x / 50x বাড়িয়ে দেখাও, যাতে ঝুলে পড়া আর ফুলে ওঠা দেখা যায়।",
    "Build with the tools below. Turn on TEST to see live stress colours while you draw.":
        "নিচের টুল দিয়ে বানাও। আঁকার সময় পীড়নের রং দেখতে 'পরীক্ষা' চালু করো।",
    "Build DECK across the gap, then add triangles above or below.": "ফাঁকের উপর ডেক বানাও, তারপর উপরে বা নিচে ত্রিভুজ যোগ করো।",
    "Road not connected yet (build DECK from bank to bank)": "রাস্তা এখনও জোড়া হয়নি (এক পাড় থেকে অন্য পাড় পর্যন্ত ডেক বানাও)",
    "Wobbly! Add triangles (diagonals) so it cannot fold": "নড়বড়ে! ত্রিভুজ (কর্ণ) যোগ করো যাতে ভাঁজ না হয়",
    "You can't build inside the rock": "পাথরের ভিতরে বানানো যায় না",
    "Stop the run to change the bridge": "সেতু বদলাতে আগে চালানো থামাও",
    "The road is not connected: build DECK beams from the left bank to the right bank.":
        "রাস্তা জোড়া নেই: বাঁ পাড় থেকে ডান পাড় পর্যন্ত ডেক বিম বানাও।",
    "The structure can wobble freely - add diagonal braces to make triangles (and remember cables can only pull, never push).":
        "কাঠামো স্বাধীনভাবে নড়তে পারে - ত্রিভুজ বানাতে কর্ণ বন্ধনী দাও (মনে রেখো, তার শুধু টানতে পারে, ঠেলতে পারে না)।",
    "THE FRAME FOLDS UP": "কাঠামো ভাঁজ হয়ে যাচ্ছে",
    "STRUCTURE FOLDED UP": "কাঠামো ভাঁজ হয়ে গেছে",
    "A pin-jointed square can lean over like a parallelogram. Triangles cannot.":
        "পিন-জোড়া বর্গ সামান্তরিকের মতো হেলে যেতে পারে। ত্রিভুজ পারে না।",
    "VEHICLE ROLLED BACK": "গাড়ি পিছনে গড়িয়ে গেছে",
    "TOO SLOW: the pod train missed its slot": "খুব ধীর: পড ট্রেন তার সময় হারিয়েছে",
    "Wind lab": "বাতাসের ল্যাব", "Quake lab": "ভূমিকম্পের ল্যাব", "Grid & wind lab": "গ্রিড ও বাতাসের ল্যাব",
    "Hazard lab": "বিপদ-ল্যাব",
    "A heavy pendulum mass under the deck, tuned to swing against the bridge.": "ডেকের নিচে ভারী দোলক-ভর, সেতুর উল্টো দিকে দোলার জন্য টিউন করা।",
    "Streamlined edges break up the vortices: lift coefficient drops by 75%.": "মসৃণ কিনারা ঘূর্ণি ভেঙে দেয়: উত্তোলন সহগ 75% কমে।",
    "Raise structural damping from 0.5% to 2%.": "কাঠামোর অবমন্দন 0.5% থেকে 2%-এ বাড়াও।",
    "Rubber-lead bearings stretch the period to 2.5 s: C drops to 0.5.": "রাবার-সীসার বিয়ারিং পর্যায়কাল 2.5 s-এ টানে: C কমে 0.5 হয়।",
    "Let the deck move 0.40 m instead of 0.05 m before it hits the abutment.": "পাড়ের দেয়ালে ধাক্কার আগে ডেককে 0.05 m-এর বদলে 0.40 m নড়তে দাও।",
    "Power the smart alloy (E x2)": "স্মার্ট সংকরে বিদ্যুৎ দাও (E x2)",
    "Smart-alloy members double their stiffness but draw 50 kW per tonne.": "স্মার্ট-সংকরের সদস্য দ্বিগুণ শক্ত হয় কিন্তু প্রতি টনে 50 kW নেয়।",
    "Member": "সদস্য", "Forces": "বল", "Turn on TEST or RUN to see forces": "বল দেখতে 'পরীক্ষা' বা 'চালাও' চালু করো",
    "Axial force from the stiffness solve": "দৃঢ়তা-সমাধান থেকে অক্ষীয় বল",
    "Axial stress": "অক্ষীয় পীড়ন", "Strain": "বিকৃতি",
    "Euler buckling (only matters when pushed)": "অয়লার বাকলিং (শুধু ঠেলা খেলে গুরুত্বপূর্ণ)",
    "Load ratio": "ভারের অনুপাত", "unloaded": "ভার নেই",
    "Method of joints": "জোড়ের পদ্ধতি", "Why it balances": "কেন ভারসাম্য থাকে",
    "Newton's 3rd law": "নিউটনের তৃতীয় সূত্র",
    "Each beam pulls/pushes this joint exactly as hard as the joint pulls/pushes the beam. If the sum were not zero the joint would accelerate.":
        "প্রতিটি বিম এই জোড়কে ঠিক ততটাই টানে/ঠেলে যতটা জোড় বিমকে টানে/ঠেলে। যোগফল শূন্য না হলে জোড়টি ত্বরিত হতো।",
    "Joint": "জোড়", "Vehicle": "গাড়ি", "Motion": "গতি", "Forces along the road": "রাস্তা বরাবর বল",
    "Momentum & energy": "ভরবেগ ও শক্তি", "Axle loads on the deck": "ডেকের উপর অ্যাক্সেলের ভার",
    "Natural frequency (Rayleigh)": "স্বাভাবিক কম্পাঙ্ক (র‍্যালে)", "Vortex shedding": "ঘূর্ণি খসে পড়া",
    "Danger wind speed": "বিপজ্জনক বাতাসের গতি", "Best TMD tuning (Den Hartog)": "সেরা TMD টিউনিং (ডেন হার্টগ)",
    "Swing right now": "এই মুহূর্তের দোলন", "Lateral period (Rayleigh)": "পাশের দিকে পর্যায়কাল (র‍্যালে)",
    "Spectral coefficient": "বর্ণালী সহগ", "Base shear at peak": "সর্বোচ্চ ভিত্তি-কর্তন বল",
    "Deck drift if isolated": "বিচ্ছিন্ন হলে ডেকের সরণ",
    "C(T): 2.5 for stiff, 2.5 x 0.5/T for long periods": "C(T): শক্তের জন্য 2.5, লম্বা পর্যায়কালে 2.5 x 0.5/T",
    "Smart grid budget": "স্মার্ট গ্রিডের বাজেট", "Maglev thrust": "ম্যাগলেভের ধাক্কা",
    "no wheels: no rolling resistance": "চাকা নেই: গড়ানোর বাধা নেই",
    "Hazard lab ": "বিপদ-ল্যাব",
    "Finish a connected, stable bridge first": "আগে একটি জোড়া, স্থির সেতু শেষ করো",
    "Build a deck from bank to bank with triangles.": "ত্রিভুজসহ এক পাড় থেকে অন্য পাড় পর্যন্ত ডেক বানাও।",
    "Debris": "ধ্বংসাবশেষ",

    # ---------------------------------------------------------------- rail screens
    "Even grade": "সমান ঢাল", "Follow hill": "পাহাড় বরাবর",
    "Re-shape the track to one steady slope between the stations (costs earthworks).": "স্টেশনের মধ্যে লাইনকে একটি সমান ঢালে বদলাও (মাটির কাজের খরচ লাগে)।",
    "Lay the track straight on the ground: no earthworks.": "লাইন সরাসরি মাটির উপর পাতো: মাটির কাজ নেই।",
    "Drag the round handles up/down to shape the track (cuttings and embankments cost money). Pick a locomotive and the number of wagons. Click a track segment to see the slope maths. SPACE runs the train.":
        "গোল হ্যান্ডেল উপরে/নিচে টেনে লাইনের আকার দাও (কাটা আর বাঁধে টাকা লাগে)। ইঞ্জিন আর ওয়াগনের সংখ্যা বেছে নাও। ঢালের গণিত দেখতে লাইনের একটি অংশে ক্লিক করো। SPACE চাপলে ট্রেন চলে।",
    "Grade labels: red = too steep for this train, yellow = close, blue = downhill":
        "ঢালের লেবেল: লাল = এই ট্রেনের জন্য খুব খাড়া, হলুদ = কাছাকাছি, নীল = নিচের দিকে",
    "Train": "ট্রেন", "Steepest slope it can climb": "সবচেয়ে খাড়া যে ঢাল উঠতে পারে",
    "Trips needed": "কত ট্রিপ লাগবে", "track + cuttings + embankments + hire": "লাইন + কাটা + বাঁধ + ভাড়া",
    "Braking distance (wet rails)": "থামার দূরত্ব (ভেজা লাইন)", "Slope": "ঢাল",
    "theta = atan(rise / run)": "theta = atan(উচ্চতা / দূরত্ব)",
    "Gravity along the track": "লাইন বরাবর মাধ্যাকর্ষণ", "Normal force & grip": "লম্ব বল ও আঁকড়ে ধরা",
    "Balancing speed (power-limited)": "ভারসাম্যের গতি (শক্তি-সীমিত)", "Speed & momentum": "গতি ও ভরবেগ",
    "Forces right now": "এই মুহূর্তের বল", "Energy": "শক্তি", "Rails": "লাইন",
    "mu = 0.30 dry, 0.18 wet": "mu = 0.30 শুকনো, 0.18 ভেজা", "WET (rain)": "ভেজা (বৃষ্টি)", "dry": "শুকনো",
    "Engine work": "ইঞ্জিনের কাজ", "Heat (friction)": "তাপ (ঘর্ষণ)", "speed m/s": "গতি m/s",
    "RAIN: wet rails, mu = 0.18": "বৃষ্টি: ভেজা লাইন, mu = 0.18", "START": "শুরু", "YARD": "গুদাম",
    "STOP ": "থামো", "BUFFER": "বাফার", "BRAKE": "ব্রেক",
    "STALLED AND ROLLED BACK": "আটকে গিয়ে পিছনে গড়িয়েছে", "RUNAWAY: brakes cannot hold the train": "নিয়ন্ত্রণহারা: ব্রেক ট্রেন ধরে রাখতে পারছে না",
    "Wet rails: mu fell from 0.30 to 0.18.": "ভেজা লাইন: mu 0.30 থেকে কমে 0.18।",
    "Make the descent gentler, or start braking before the train runs away.": "নামার ঢাল মৃদু করো, বা ট্রেন নিয়ন্ত্রণ হারানোর আগে ব্রেক শুরু করো।",
    "THE TRIP NEVER FINISHED": "যাত্রা কখনো শেষ হয়নি", "The train got stuck": "ট্রেন আটকে গেছে",
    "TOO SLOW: the job missed its deadline": "খুব ধীর: কাজ সময়সীমা পেরিয়ে গেছে",
    "Carry more per trip (more power or gentler grades) or move faster.": "প্রতি ট্রিপে বেশি নাও (বেশি শক্তি বা মৃদু ঢাল) বা দ্রুত চলো।",
    "Trips x cargo": "ট্রিপ x মাল", "Job time": "কাজের সময়", "Energy: engine work": "শক্তি: ইঞ্জিনের কাজ",
    "Heat lost to friction/brakes": "ঘর্ষণ/ব্রেকে হারানো তাপ", "Stopping accuracy": "থামার নির্ভুলতা",
    "Banker engine (+Rs 2.50 L)": "ব্যাংকার ইঞ্জিন (+Rs 2.50 L)", "WHEEL SLIP": "চাকা পিছলাচ্ছে",

    # ---------------------------------------------------------------- cantilever screens
    "< Cast A": "< ঢালাই A", "Cast A >": "ঢালাই A >", "< Cast B": "< ঢালাই B", "Cast B >": "ঢালাই B >",
    "Tie-down A": "বাঁধন-তার A", "Tie-down B": "বাঁধন-তার B",
    "STITCH & POST-TENSION": "জোড়া দাও ও পোস্ট-টেনশন", "TRUCK TEST": "ট্রাক পরীক্ষা",
    "Cast segments one at a time with the four CAST buttons. Watch each pier's see-saw meter. Tie-downs add resistance. Set the haunch depths in the calculator before the first cast. When all arms are complete, STITCH, then run the TRUCK TEST.":
        "চারটি ঢালাই বোতাম দিয়ে একটা একটা করে অংশ ঢালাই করো। প্রতিটি স্তম্ভের ঢেঁকি-মিটার দেখো। বাঁধন-তার সহ্যক্ষমতা বাড়ায়। প্রথম ঢালাইয়ের আগে ক্যালকুলেটরে হঞ্চের গভীরতা ঠিক করো। সব বাহু শেষ হলে জোড়া দাও, তারপর ট্রাক পরীক্ষা চালাও।",
    "Girder & piers": "গার্ডার ও স্তম্ভ", "Second moment of area": "ক্ষেত্রফলের দ্বিতীয় ভ্রামক",
    "Pier A: see-saw balance": "স্তম্ভ A: ঢেঁকির ভারসাম্য", "Pier B: see-saw balance": "স্তম্ভ B: ঢেঁকির ভারসাম্য",
    "Pier A: root bending": "স্তম্ভ A: গোড়ার বাঁকানো", "Pier B: root bending": "স্তম্ভ B: গোড়ার বাঁকানো",
    "Post-tensioning": "পোস্ট-টেনশনিং", "allowed tension = f_t + sigma_pt": "অনুমোদিত টান = f_t + sigma_pt",
    "Continuous girder (after stitch)": "অবিচ্ছিন্ন গার্ডার (জোড়ার পরে)",
    "That arm is complete": "ওই বাহু শেষ হয়ে গেছে", "Stitch the girder before the truck test": "ট্রাক পরীক্ষার আগে গার্ডার জোড়া দাও",
    "Stitched! The two T-frames are now one continuous beam.": "জোড়া হয়েছে! দুটি T-কাঠামো এখন একটি অবিচ্ছিন্ন বিম।",
    "GIRDER CRACKED under the truck": "ট্রাকের নিচে গার্ডার ফেটে গেছে",
    "More post-tensioning raises the allowed tension; a deeper tip raises I.": "বেশি পোস্ট-টেনশনিং অনুমোদিত টান বাড়ায়; গভীর ডগা I বাড়ায়।",
    "PIER A": "স্তম্ভ A", "PIER B": "স্তম্ভ B", "PIER A see-saw": "স্তম্ভ A ঢেঁকি", "PIER B see-saw": "স্তম্ভ B ঢেঁকি",
    "landed": "পাড়ে বসেছে", "close here": "এখানে জোড়া হবে", "PIER TILT": "স্তম্ভ হেলে পড়েছে", "ROOT CRACK": "গোড়ায় ফাটল",
    "Cantilever moments while building (all hogging: the top is pulled)": "নির্মাণের সময় ক্যান্টিলিভারের ভ্রামক (সবই উপরে টান)",
    "Bending moment M(x) of the continuous girder (sagging up, hogging down)": "অবিচ্ছিন্ন গার্ডারের বাঁকানো ভ্রামক M(x) (ঝুলে পড়া উপরে, উঁচু হওয়া নিচে)",
    "girder % vs truck x": "গার্ডার % বনাম ট্রাকের অবস্থান x", "Concrete": "কংক্রিট", "Tie-downs": "বাঁধন-তার",
    "Worst girder stress": "গার্ডারের সর্বোচ্চ পীড়ন",

    # ---------------------------------------------------------------- signals
    "3-aspect signals": "3-আলোর সিগন্যাল", "4-aspect signals": "4-আলোর সিগন্যাল",
    "4-aspect adds DOUBLE YELLOW so each block only needs half the braking distance.":
        "4-আলোর সিগন্যালে জোড়া হলুদ যোগ হয়, তাই প্রতিটি ব্লকে অর্ধেক থামার দূরত্ব লাগে।",
    "Starter logic": "শুরুর লজিক", "RUN 12 MINUTES": "12 মিনিট চালাও",
    "Click the small dots beside the eastbound (top) and westbound (bottom) approach tracks to add or remove signals. Edit the interlocking rows below: click an input to cycle it, NOT to invert it, AND/OR to switch. RUN plays 12 minutes of traffic.":
        "পূর্বমুখী (উপরে) আর পশ্চিমমুখী (নিচে) লাইনের পাশের ছোট বিন্দুতে ক্লিক করে সিগন্যাল যোগ বা সরাও। নিচের ইন্টারলকিং সারি বদলাও: ইনপুটে ক্লিক করলে বদলায়, NOT উল্টায়, AND/OR বদলায়। 'চালাও' চাপলে 12 মিনিটের ট্রেন চলাচল হয়।",
    "Passenger braking distance": "যাত্রী ট্রেনের থামার দূরত্ব", "Cargo braking distance": "মালগাড়ির থামার দূরত্ব",
    "Minimum warning distance": "ন্যূনতম সতর্কতার দূরত্ব",
    "caution signal >= d_stop before the red": "সতর্ক সিগন্যাল লালের অন্তত d_stop আগে",
    "caution signal >= d_stop before the red (halved: 4-aspect)": "সতর্ক সিগন্যাল লালের অন্তত d_stop আগে (অর্ধেক: 4-আলো)",
    "Interlocking (evaluated top to bottom)": "ইন্টারলকিং (উপর থেকে নিচে হিসাব হয়)", "Live": "সরাসরি",
    "delivered / SPADs / waiting": "পৌঁছেছে / SPAD / অপেক্ষা", "Inputs now": "এখনকার ইনপুট",
    "PORT KAVI BAY": "পোর্ট কাভি উপসাগর", "HARBOR": "বন্দর", "EASTBOUND ->": "পূর্বমুখী ->",
    "<- WESTBOUND": "<- পশ্চিমমুখী", "single-track bridge": "এক-লাইনের সেতু", "road": "রাস্তা",
    "INTERLOCKING LOGIC  -  each output = [NOT] A  AND/OR  [NOT] B  AND/OR  [NOT] C":
        "ইন্টারলকিং লজিক  -  প্রতিটি আউটপুট = [NOT] A  AND/OR  [NOT] B  AND/OR  [NOT] C",
    "Trains delivered": "পৌঁছানো ট্রেন", "SPADs (signals passed at danger)": "SPAD (লাল সিগন্যাল পেরোনো)",
    "Waiting (idle + queued)": "অপেক্ষা (দাঁড়িয়ে + লাইনে)", "Barrier down time": "গেট নামানো থাকার সময়",
    "Interlocking rule: a switch may only move when its track circuit is clear -> add 'AND NOT JE_OCC' style locking (use CARGO_AT_JE)":
        "ইন্টারলকিং নিয়ম: লাইন খালি থাকলেই শুধু পয়েন্ট সরতে পারে -> 'AND NOT JE_OCC' ধরনের তালা দাও (CARGO_AT_JE ব্যবহার করো)",
    "Set the switch early and hold it while JE is occupied": "পয়েন্ট আগে থেকে ঠিক করো এবং JE-তে ট্রেন থাকলে ধরে রাখো",
    "d_stop = v^2 / (2 mu g) - every red must be warned at least d_stop earlier, and the bridge must only be given to one direction at a time (PERMIT_EB / PERMIT_WB interlock)":
        "d_stop = v^2 / (2 mu g) - প্রতিটি লালের অন্তত d_stop আগে সতর্ক করতে হবে, আর সেতু একবারে শুধু এক দিককে দেওয়া যাবে (PERMIT_EB / PERMIT_WB ইন্টারলক)",
    "SWITCH_HARBOR must be TRUE for cargo trains and FALSE for passengers": "মালগাড়ির জন্য SWITCH_HARBOR হবে TRUE আর যাত্রী ট্রেনের জন্য FALSE",

    # ---------------------------------------------------------------- traffic
    "RUN RUSH HOUR": "ভিড়ের সময় চালাও", "Traffic flow": "যান প্রবাহ", "Greenshields model": "গ্রিনশিল্ডস মডেল",
    "Choose the junction type at the bottom left. Signal timing and the speed limit are sliders in the calculator. RUN plays 12 minutes of rush hour; the road is coloured by speed so you can watch jams travel backwards.":
        "নিচে বাঁয়ে মোড়ের ধরন বেছে নাও। সিগন্যালের সময় আর গতিসীমা ক্যালকুলেটরের স্লাইডারে। 'চালাও' চাপলে 12 মিনিটের ভিড় চলে; রাস্তা গতি অনুযায়ী রঙিন, তাই জ্যাম পিছনে সরতে দেখা যায়।",
    "Signal capacity": "সিগন্যালের ক্ষমতা", "Demand exceeds capacity: queues will grow": "চাহিদা ক্ষমতার বেশি: লাইন বাড়বে",
    "Roundabout": "গোলচত্বর", "cars merge in turn, gap >= 2 s": "গাড়ি পালা করে মেশে, ফাঁক >= 2 s",
    "Slower (8 m/s in the circle) but nobody waits for a red light.": "ধীর (চত্বরে 8 m/s) কিন্তু কাউকে লাল বাতির জন্য অপেক্ষা করতে হয় না।",
    "Overpass": "উড়ালসেতু", "no conflict point": "কোনো সংঘাত-বিন্দু নেই", "Each road flows at its own capacity.": "প্রতিটি রাস্তা নিজের ক্ষমতায় চলে।",
    "Shockwave when a queue forms": "লাইন তৈরি হলে শকওয়েভ", "Detector (200 m before the junction)": "সেন্সর (মোড়ের 200 m আগে)",
    "congested (k > k_crit)": "জ্যাম (k > k_crit)", "free flow": "মুক্ত প্রবাহ", "Results so far": "এ পর্যন্ত ফলাফল",
    "throughput, travel time, idling": "প্রবাহ, যাত্রার সময়, অলস দাঁড়ানো", "MAIN ROAD  ->": "প্রধান সড়ক  ->",
    "MARKET STREET": "বাজার রাস্তা", "overpass": "উড়ালসেতু", "throughput (veh per min)": "প্রবাহ (প্রতি মিনিটে গাড়ি)",
    "Fundamental diagram  q = k v  (curve = Greenshields, dots = detector)": "মৌলিক চিত্র  q = k v  (বক্ররেখা = গ্রিনশিল্ডস, বিন্দু = সেন্সর)",
    "k (veh/km) ->": "k (veh/km) ->", "k_crit": "k_crit",
    "The red band in the heat map is the jam; it grows backwards at the shockwave speed w.":
        "তাপ-মানচিত্রের লাল অংশই জ্যাম; এটি শকওয়েভের গতি w-তে পিছনের দিকে বাড়ে।",
    "CITY TOO SLOW: main-road trips took too long": "শহর খুব ধীর: প্রধান সড়কের যাত্রায় অনেক সময় লেগেছে",
    "Cars through": "পার হওয়া গাড়ি", "Main-road trip vs free flow": "প্রধান সড়কের যাত্রা বনাম মুক্ত প্রবাহ",
    "Idling (pollution)": "অলস দাঁড়ানো (দূষণ)", "Fuel burned": "পোড়া জ্বালানি",

    # ---------------------------------------------------------------- logistics
    "Optimizer: show all plans": "অপ্টিমাইজার: সব পরিকল্পনা দেখাও", "SHIP IT": "পাঠাও",
    "Brute-force search (a stand-in for linear programming) over every split and fleet size.":
        "প্রতিটি ভাগ আর বহরের আকারে পূর্ণ অনুসন্ধান (লিনিয়ার প্রোগ্রামিংয়ের বিকল্প)।",
    "Use the sliders to share the 6000 t between road, rail and barge and to hire fleets. The calculator shows each mode's physics. 'Optimizer' plots every feasible plan so you can see the Pareto frontier. RUN ships it.":
        "স্লাইডার দিয়ে 6000 t সড়ক, রেল আর বার্জে ভাগ করো এবং যানবাহন ভাড়া করো। ক্যালকুলেটর প্রতিটি পথের পদার্থবিজ্ঞান দেখায়। 'অপ্টিমাইজার' সব সম্ভব পরিকল্পনা আঁকে, যাতে প্যারেটো সীমান্ত দেখা যায়। 'পাঠাও' চাপলে চালান যায়।",
    "Freight plan": "মাল পরিবহন পরিকল্পনা", "Road: truck speed (Greenshields)": "সড়ক: ট্রাকের গতি (গ্রিনশিল্ডস)",
    "Rail: speed on the 1.2% grade": "রেল: 1.2% ঢালে গতি", "Rail: can it climb at all?": "রেল: আদৌ উঠতে পারবে?",
    "Barge: speed over ground": "বার্জ: মাটির সাপেক্ষে গতি", "v = v_water +/- current": "v = v_পানি +/- স্রোত",
    "3.0 m/s through water, 1.0 m/s current": "পানিতে 3.0 m/s, স্রোত 1.0 m/s",
    "14.4 km/h down to the port, 7.2 km/h back": "বন্দরের দিকে 14.4 km/h, ফেরার পথে 7.2 km/h",
    "STALLS - fewer wagons!": "আটকে যায় - ওয়াগন কমাও!", "Problem": "সমস্যা",
    "time = slowest mode;  Toll = (t x km)/(h x L)": "সময় = সবচেয়ে ধীর পথ;  টোল = (t x km)/(h x L)",
    "ROAD 80 km": "সড়ক 80 km", "RAIL 95 km, 1.2% ruling grade": "রেল 95 km, সর্বোচ্চ ঢাল 1.2%",
    "RIVER 120 km, current 1 m/s toward the port": "নদী 120 km, বন্দরের দিকে স্রোত 1 m/s",
    "BHILWARA": "ভিলওয়াড়া", "MINE": "খনি", "KANDLA": "কান্ডলা", "PORT": "বন্দর",
    "Press 'Optimizer' to plot every feasible plan.": "সব সম্ভব পরিকল্পনা আঁকতে 'অপ্টিমাইজার' চাপো।",
    "Cost (left = cheap) vs time (down = fast). Gold = Pareto frontier, white ring = your plan, red line = deadline":
        "খরচ (বাঁয়ে = সস্তা) বনাম সময় (নিচে = দ্রুত)। সোনালি = প্যারেটো সীমান্ত, সাদা বৃত্ত = তোমার পরিকল্পনা, লাল রেখা = সময়সীমা",
    "FREIGHT TRAIN STALLED ON THE GRADE": "মালবাহী ট্রেন ঢালে আটকে গেছে",
    "One locomotive can only haul about 30 of these wagons up 1.2%.": "একটি ইঞ্জিন 1.2% ঢালে এমন প্রায় 30টি ওয়াগনই টানতে পারে।",
    "MISSED THE 24-HOUR DEADLINE": "24 ঘণ্টার সময়সীমা পেরিয়ে গেছে",
    "Road freight assigned but no trucks hired": "সড়কে মাল দেওয়া হয়েছে কিন্তু ট্রাক ভাড়া হয়নি",
    "A mode has freight but no vehicles": "একটি পথে মাল আছে কিন্তু কোনো যান নেই",
    "a mode has freight but no vehicles": "একটি পথে মাল আছে কিন্তু কোনো যান নেই",
    "Safety index": "নিরাপত্তা সূচক", "Fuel": "জ্বালানি",
    "Road": "সড়ক", "Rail": "রেল", "Barge": "বার্জ",

    # chart series names (joined with " / " in the black box)
    "max load %": "সর্বোচ্চ ভার %", "wind m/s": "বাতাস m/s", "ground a (m/s2)": "ভূমির ত্বরণ (m/s2)",
    "pier A MN*m": "স্তম্ভ A MN*m", "pier B MN*m": "স্তম্ভ B MN*m", "PE MJ": "PE MJ", "KE MJ": "KE MJ",
    "veh/min": "গাড়ি/মিনিট", "trip s": "যাত্রা s", "girder %": "গার্ডার %",
}

# Formula cards that are pure maths stay as they are; listing them documents that on purpose.
for _f in ("Sum Fx = 0, Sum Fy = 0", "Sum Fx = 0,  Sum Fy = 0", "sigma = N / A", "epsilon = sigma / E",
           "N = (E A / L) x stretch", "ratio = |N| / N_limit", "P_cr = pi^2 E I / (K L)^2",
           "F_net = m a", "F = T - F_rr - F_drag - m g sin(theta)", "p = m v,  KE = 1/2 m v^2",
           "P = m g / axles", "F = m g sin(theta)", "N = m g cos(theta)", "F_grip = mu N",
           "T = min(P / v, mu N)", "f_n = (1/2 pi) sqrt(k / m)", "f_v = St U / D", "U_crit = f_n D / St",
           "f_tmd/f_n = 1/(1+mu), zeta = sqrt(3mu/8(1+mu)^3)", "F_eq = k* x"):
    EXACT.setdefault(_f, _f)
EXACT.update({
    "N = (E A / L) x stretch": "N = (E A / L) x প্রসারণ",
    "P = m g / axles": "P = m g / অ্যাক্সেল সংখ্যা",
    "N = m g cos(theta);  F_grip = mu N_loco": "N = m g cos(theta);  F_আঁকড়ে = mu N_ইঞ্জিন",
    "P = F v  ->  v = P / (m g (sin + C_rr cos))": "P = F v  ->  v = P / (m g (sin + C_rr cos))",
    "T = min(P / v, T_max)": "T = min(P / v, T_max)",
    "P_total = P_pod + P_alloy": "P_মোট = P_পড + P_সংকর",
    "T = 2 pi sqrt(sum m u^2 / sum F u)": "T = 2 pi sqrt(sum m u^2 / sum F u)",
    "d = C a / omega^2": "d = C a / omega^2",
    "Displacement = C a / omega^2": "সরণ = C a / omega^2",
    "c = s g / C   (s = 1800 veh/h of green)": "c = s g / C   (সবুজের সময় s = 1800 veh/h)",
    "w = (q2 - q1) / (k2 - k1)": "w = (q2 - q1) / (k2 - k1)",
    "m a = T - F_rr - F_drag - F_brake - m g sin(theta)": "m a = T - F_rr - F_drag - F_brake - m g sin(theta)",
    "PE = m g h,  KE = 1/2 m v^2": "PE = m g h,  KE = 1/2 m v^2",
    "Sum M = Sum W_right x - Sum W_left x": "Sum M = Sum W_ডান x - Sum W_বাম x",
    "Sum M_pier = Sum W_right x - Sum W_left x": "Sum M_স্তম্ভ = Sum W_ডান x - Sum W_বাম x",
    "tau = V Q / (I t)": "tau = V Q / (I t)", "sigma = M y / I": "sigma = M y / I", "I = b d^3 / 12": "I = b d^3 / 12",
    "mu m_loco g cos(theta) = m g sin(theta) + C_rr m g": "mu m_ইঞ্জিন g cos(theta) = m g sin(theta) + C_rr m g",
    "mu m_loco g cos(theta) >= m g sin(theta) + C_rr m g": "mu m_ইঞ্জিন g cos(theta) >= m g sin(theta) + C_rr m g",
    "mu m_loco g >= m g sin(theta)": "mu m_ইঞ্জিন g >= m g sin(theta)",
    "Toll = (t x km) / (h x L)": "টোল = (t x km) / (h x L)",
    "F_grip = mu N": "F_আঁকড়ে = mu N", "F_net = m a": "F_নিট = m a",
    "ratio = |N| / N_limit": "অনুপাত = |N| / N_সীমা",
    "Tank engine": "ট্যাংক ইঞ্জিন", "Diesel shunter": "ডিজেল শান্টার",
    "Mainline diesel": "মেইনলাইন ডিজেল", "Double-header": "জোড়া ইঞ্জিন",
    "Signals & interlocking": "সিগন্যাল ও ইন্টারলকিং", "Track": "লাইন",
    "Smart grid capacity (MW)": "স্মার্ট গ্রিডের ক্ষমতা (MW)",
})

from .lang_bn_help import HELP_BN  # noqa: E402  (bottom-bar IDEA help)
EXACT.update(HELP_BN)
from .lang_bn_demo import DEMO_BN, DEMO_PATTERNS  # noqa: E402  (paid demonstrations)
EXACT.update(DEMO_BN)

# Slider and value labels ("Label: 12")
LABELS = {
    "Cross-section area A (cm^2)": "প্রস্থচ্ছেদের ক্ষেত্রফল A (cm^2)", "TMD mass ratio mu": "TMD ভরের অনুপাত mu",
    "TMD tuning f_tmd/f_n": "TMD টিউনিং f_tmd/f_n", "TMD damping zeta": "TMD অবমন্দন zeta",
    "Smart grid capacity (MW)": "স্মার্ট গ্রিডের ক্ষমতা (MW)", "Haunch depth at piers d_pier (m)": "স্তম্ভের কাছে হঞ্চের গভীরতা d_pier (m)",
    "Depth at tips / mid-span d_tip (m)": "ডগা / মাঝখানের গভীরতা d_tip (m)",
    "Post-tensioning level (0 none, 1 light, 2 heavy)": "পোস্ট-টেনশনিং মাত্রা (0 নেই, 1 হালকা, 2 ভারী)",
    "Signal cycle C (s)": "সিগন্যাল চক্র C (s)", "Main-road share of green": "সবুজে প্রধান সড়কের ভাগ",
    "Speed limit (km/h)": "গতিসীমা (km/h)", "Rail share (t)": "রেলের ভাগ (t)", "Barge share (t)": "বার্জের ভাগ (t)",
    "Trucks hired": "ভাড়া করা ট্রাক", "Trains (rakes)": "ট্রেন (র‍্যাক)", "Wagons per train": "প্রতি ট্রেনে ওয়াগন",
    "Barges": "বার্জ", "Wagons": "ওয়াগন",
}

SIGNS = {"BUCKLED": "বাকলিং", "SNAPPED": "ছিঁড়ে গেছে", "CRUSHED": "চূর্ণ হয়েছে", "Tension": "টান",
         "Compression": "চাপ", "Unloaded (zero-force member)": "ভারহীন (শূন্য-বল সদস্য)",
         "Slack": "ঢিলা"}

STATES = {"TENSION (pulled)": "টান (টানা হচ্ছে)", "COMPRESSION (pushed)": "চাপ (ঠেলা হচ্ছে)",
          "no load": "ভার নেই", "SLACK (cable cannot push)": "ঢিলা (তার ঠেলতে পারে না)"}


def _train_name(name):
    """'Diesel shunter + banker + 2 wagons' -> Bengali."""
    parts = [p.strip() for p in name.split("+")]
    out = []
    for p in parts:
        m = re.fullmatch(r"(\d+) wagons", p)
        if m:
            out.append(f"{m.group(1)}টি ওয়াগন")
        elif p == "banker":
            out.append("ব্যাংকার")
        else:
            out.append(v(p))
    return " + ".join(out)


def _grade(g):
    return FS_GRADES.get(g, g)


def _list(s):
    return ", ".join(v(x.strip()) for x in s.split(","))


PATTERNS = [
    # --- top bar, menus, money
    (r"Cost (Rs [^/]+) / (Rs [^(]+?)( \(\+salvage ([^)]+)\))?( \(demo -([^)]+)\))?",
     lambda m: f"খরচ {m.group(1)} / {m.group(2)}" + (f" (+উদ্ধার {m.group(4)})" if m.group(3) else "")
     + (f" (ডেমো -{m.group(6)})" if m.group(5) else "")),
    (r"Budget: (.+?)    Par \(bonus star\): (.+)", r"বাজেট: \1    প্যার (বোনাস তারা): \2"),
    (r"Materials: (.+)", lambda m: "উপকরণ: " + _list(m.group(1))),
    (r"L(\d+)  (.+)", lambda m: f"L{m.group(1)}  {EXACT.get(m.group(2), m.group(2))}"),
    (r"LEVEL (\d+)  -  (.+)", lambda m: f"লেভেল {m.group(1)}  -  {EXACT.get(m.group(2), m.group(2))}"),
    (r"- (Low cost, high skill|High cost, robust): (.+)",
     lambda m: f"- {EXACT[m.group(1)]}: {EXACT.get(m.group(2), m.group(2))}"),
    (r"\+(\d+) EXP   \(total (\d+)\)", r"+\1 EXP   (মোট \2)"),
    (r"EXP earned here: (\d+)", r"এখানে অর্জিত EXP: \1"),
    (r"Correct! \+(\d+) EXP\. (.+)", lambda m: f"সঠিক! +{m.group(1)} EXP। {EXACT.get(m.group(2), m.group(2))}"),
    (r"Edit & retry \((.+)\)", r"আবার চেষ্টা করো (\1)"),
    (r"Alternate: (.+)", lambda m: "বিকল্প: " + EXACT.get(m.group(1), m.group(1))),
    (r"([\d.]+)  \(([A-Z-]+)\)", lambda m: f"{m.group(1)}  ({_grade(m.group(2))})"),
    (r"(\d+)% of an ideal flat, full-speed crossing", r"আদর্শ সমতল, পূর্ণ-গতির পারাপারের \1%"),
    (r"(.+)  of  (.+)", r"\1  (মোট \2)"),
    (r"Cost (Rs .+) > budget (Rs .+)", r"খরচ \1 > বাজেট \2"),
    # --- bridge editor & calculator
    (r"TEST: worst member (\d+)% -> FS ([\d.inf]+) \(([A-Z-]+)\)",
     lambda m: f"পরীক্ষা: সবচেয়ে বেশি ভারের সদস্য {m.group(1)}% -> FS {m.group(2)} ({_grade(m.group(3))})"),
    (r"Too long: ([\d.]+) m \(max (\d+) m for this tool\)", r"খুব লম্বা: \1 m (এই টুলে সর্বোচ্চ \2 m)"),
    (r"Beam #(\d+)", r"বিম #\1"), (r"Joint #(\d+)", r"জোড় #\1"),
    (r"(.+?) (beam|deck|cable), (.+)", lambda m: f"{v(m.group(1))} {v(m.group(2))}, {v(m.group(3))}"),
    (r"N = (\S+) kN  (.+)", lambda m: f"N = {m.group(1)} kN  {STATES.get(m.group(2), m.group(2))}"),
    (r"stretch = (.+)", r"প্রসারণ = \1"),
    (r"epsilon = (\S+) microstrain", r"epsilon = \1 মাইক্রোস্ট্রেন"),
    (r"(\d+)% of limit  ->  FS = (.+)", r"সীমার \1%  ->  FS = \2"),
    (r"Tension: sigma = N/A = (.+) \(limit (.+)\)", r"টান: sigma = N/A = \1 (সীমা \2)"),
    (r"Compression: (\S+) kN vs Euler (.+)", r"চাপ: \1 kN বনাম অয়লার \2"),
    (r"Compression: sigma = (.+) \(crush limit (.+)\)", r"চাপ: sigma = \1 (চূর্ণ সীমা \2)"),
    (r"BUCKLED: compressive force (\S+) kN exceeded P_cr (\S+) kN",
     r"বাকলিং: চাপ বল \1 kN, P_cr \2 kN ছাড়িয়ে গেছে"),
    (r"SNAPPED: tensile stress (\S+) MPa exceeded (\S+) MPa", r"ছিঁড়ে গেছে: টানের পীড়ন \1 MPa, সীমা \2 MPa ছাড়িয়েছে"),
    (r"CRUSHED: compressive stress (\S+) MPa exceeded (\S+) MPa", r"চূর্ণ: চাপের পীড়ন \1 MPa, সীমা \2 MPa ছাড়িয়েছে"),
    (r"(BUCKLED|SNAPPED|CRUSHED|Tension|Compression) - member (\d+)",
     lambda m: f"{SIGNS[m.group(1)]} - সদস্য {m.group(2)}"),
    (r"Member (\d+): (.+?), L = (.+)", lambda m: f"সদস্য {m.group(1)}: {v(m.group(2))}, L = {m.group(3)}"),
    (r"beam (\d+): (.+)", r"বিম \1: \2"), (r"loads: (.+)", r"ভার: \1"), (r"support: (.+)", r"সাপোর্ট: \1"),
    (r"(\S+) kN on each of (\d+) axles", r"প্রতিটি \2টি অ্যাক্সেলে \1 kN"),
    (r"v = (\S+) m/s \((\d+) km/h\), a = (.+)", r"v = \1 m/s (\2 km/h), a = \3"),
    (r"T = (\S+) kN, F_rr = (\S+) kN, drag = (\S+) kN, gravity = (\S+) kN",
     r"T = \1 kN, F_rr = \2 kN, বাতাসের বাধা = \3 kN, মাধ্যাকর্ষণ = \4 kN"),
    (r"t = +([\d.]+) s   worst member now +(\d+)%   max so far (\d+)%",
     r"t = \1 s   এখন সবচেয়ে বেশি ভার \2%   এ পর্যন্ত সর্বোচ্চ \3%"),
    (r"wind U = +([\d.]+) m/s   f_v = (\S+) Hz   f_n = (\S+) Hz   swing load (\d+) kN",
     r"বাতাস U = \1 m/s   f_v = \2 Hz   f_n = \3 Hz   দোলনের ভার \4 kN"),
    (r"ground a = (\S+) m/s\^2   C = (\S+)   V_base = (\S+) kN", r"ভূমির ত্বরণ a = \1 m/s^2   C = \2   V_base = \3 kN"),
    (r"grid ([\d.]+) MW: pod power (\d+)%   limit ([\d.]+) s", r"গ্রিড \1 MW: পডের শক্তি \2%   সীমা \3 s"),
    (r"deck drift (\S+) cm", r"ডেকের সরণ \1 cm"),
    (r"k\* = (.+), m\* = (.+)", r"k* = \1, m* = \2"),
    (r"St = 0\.12, D = ([\d.]+) m \(deck\)", r"St = 0.12, D = \1 m (ডেক)"),
    (r"now: U = (\S+) m/s -> f_v = (\S+) Hz", r"এখন: U = \1 m/s -> f_v = \2 Hz"),
    (r"U_crit = (\S+) m/s  \(wind reaches (\d+)\)", r"U_crit = \1 m/s  (বাতাস ওঠে \2 পর্যন্ত)"),
    (r"tune (\S+), zeta (\S+)", r"টিউনিং \1, zeta \2"),
    (r"(\d+) kN extra load", r"\1 kN বাড়তি ভার"),
    (r"T = (\S+) s  ->  with bearings (\S+) s", r"T = \1 s  ->  বিয়ারিংসহ \2 s"),
    (r"C = (\S+)  \(fixed (\S+), isolated (\S+)\)", r"C = \1  (স্থির \2, বিচ্ছিন্ন \3)"),
    (r"M = (\S+) t, a = (\S+) m/s\^2", r"M = \1 t, a = \2 m/s^2"),
    (r"d = (\S+) m vs joint gap (\S+) m", r"d = \1 m বনাম জোড়ের ফাঁক \2 m"),
    (r"pod (\S+) MW, alloy (\S+) t x 50 kW/t = (\S+) MW", r"পড \1 MW, সংকর \2 t x 50 kW/t = \3 MW"),
    (r"capacity (\S+) MW -> pod gets (\d+)%", r"ক্ষমতা \1 MW -> পড পায় \2%"),
    (r"Wind (\S+) m/s -> f_v = St U / D = (\S+) Hz vs f_n = (\S+) Hz \(U_crit = (\S+) m/s\)",
     r"বাতাস \1 m/s -> f_v = St U / D = \2 Hz বনাম f_n = \3 Hz (U_crit = \4 m/s)"),
    (r"Ground a = (\S+) m/s\^2, C = (\S+), V_base = C M a = (\S+) kN",
     r"ভূমির ত্বরণ a = \1 m/s^2, C = \2, V_base = C M a = \3 kN"),
    (r"drift = C a_g / omega\^2 = (.+) m > joint gap (\S+) m", r"সরণ = C a_g / omega^2 = \1 m > জোড়ের ফাঁক \2 m"),
    (r"Isolation stretched the period to T = (\S+) s, which cut C to (\S+) - but bigger movement needs flexible joints\.",
     r"বিচ্ছিন্নতা পর্যায়কাল T = \1 s পর্যন্ত টেনেছে, তাতে C কমে \2 হয়েছে - কিন্তু বেশি নড়াচড়ার জন্য নমনীয় জোড় লাগে।"),
    (r"POUNDING: the isolated deck slammed into the abutment", r"ধাক্কা: বিচ্ছিন্ন ডেক পাড়ের দেয়ালে আছড়ে পড়েছে"),
    (r"Grid (\S+) MW - alloy (\S+) MW leaves (\S+) MW for a (\S+) MW pod: thrust = P / v",
     r"গ্রিড \1 MW - সংকর \2 MW বাদে \4 MW পডের জন্য থাকে \3 MW: ধাক্কা = P / v"),
    (r"Tuned mass damper \((.+)\)", r"টিউনড মাস ড্যাম্পার (\1)"),
    (r"Aerodynamic fairings \((.+)\)", r"বাতাস-কাটা ফেয়ারিং (\1)"),
    (r"Cross-stay dampers \((.+)\)", r"আড়াআড়ি ড্যাম্পার (\1)"),
    (r"Isolation bearings \((.+)\)", r"আইসোলেশন বিয়ারিং (\1)"),
    (r"Flexible expansion joints \((.+)\)", r"নমনীয় সম্প্রসারণ জোড় (\1)"),
    (r"Banker engine \((.+)\)", r"ব্যাংকার ইঞ্জিন (\1)"),
    (r"Size (\w+)", r"আকার \1"),
    (r"Sag x(\d+)", r"ঝোলা x\1"),
    # --- rail
    (r"Train: (.+?)  -  (\S+) t, (\S+) kW, can climb (\S+) deg",
     lambda m: f"ট্রেন: {_train_name(m.group(1))}  -  {m.group(2)} t, {m.group(3)} kW, উঠতে পারে {m.group(4)} deg"),
    (r"Train: (.+)", lambda m: "ট্রেন: " + _train_name(m.group(1))),
    (r"m = (\S+) t  \(loco (\S+) t drives\)", r"m = \1 t  (ইঞ্জিন \2 t চালায়)"),
    (r"P = (\S+) kW, cargo (\S+) t per trip", r"P = \1 kW, প্রতি ট্রিপে মাল \2 t"),
    (r"theta_max = (\S+) deg dry, (\S+) deg wet; your steepest = (\S+) deg",
     r"theta_max = শুকনোয় \1 deg, ভেজায় \2 deg; তোমার সবচেয়ে খাড়া = \3 deg"),
    (r"(\d+) trip\(s\), time limit (\d+) min", r"\1 ট্রিপ, সময়সীমা \2 মিনিট"),
    (r"track (Rs .+?), cut (\S+) m\^2 = (Rs .+?), fill (\S+) m\^2 = (Rs .+)",
     r"লাইন \1, কাটা \2 m^2 = \3, ভরাট \4 m^2 = \5"),
    (r"loco (Rs .+?), wagons (Rs .+)", r"ইঞ্জিন \1, ওয়াগন \2"),
    (r"v = (\S+) m/s, mu = (\S+), theta = (\S+) deg down", r"v = \1 m/s, mu = \2, theta = \3 deg নিচের দিকে"),
    (r"d = (\S+) m needed;  your marker gives (\S+) m", r"দরকার d = \1 m;  তোমার চিহ্নে আছে \2 m"),
    (r"Track (\d+)-(\d+) m", r"লাইন \1-\2 m"),
    (r"(\S+) kN pulling back", r"\1 kN পিছনে টানছে"),
    (r"N_loco = (\S+) kN", r"N_ইঞ্জিন = \1 kN"),
    (r"grip limit = (\S+) kN \(dry\)", r"আঁকড়ে ধরার সীমা = \1 kN (শুকনো)"),
    (r"Engine pull at (\S+) m/s", r"\1 m/s গতিতে ইঞ্জিনের টান"),
    (r"T = (\S+) kN vs needed (\S+) kN", r"T = \1 kN বনাম দরকার \2 kN"),
    (r"downhill: speeds up", r"উৎরাই: গতি বাড়ে"),
    (r"v = (\S+) m/s \((\d+) km/h\)", r"v = \1 m/s (\2 km/h)"),
    (r"T (\S+), rr (\S+), drag (\S+), brake (\S+), gravity (\S+) kN",
     r"T \1, rr \2, বাতাসের বাধা \3, ব্রেক \4, মাধ্যাকর্ষণ \5 kN"),
    (r"a = (\S+) m/s\^2   WHEEL SLIP", r"a = \1 m/s^2   চাকা পিছলাচ্ছে"),
    (r"engine work (\S+) MJ", r"ইঞ্জিনের কাজ \1 MJ"),
    (r"PE (\S+) MJ, KE (\S+) MJ, heat (\S+) MJ", r"PE \1 MJ, KE \2 MJ, তাপ \3 MJ"),
    (r"v = +([\d.]+) km/h   a = (\S+) m/s\^2   p = (\S+) kN s", r"v = \1 km/h   a = \2 m/s^2   p = \3 kN s"),
    (r"vertical scale x([\d.]+)", r"উল্লম্ব স্কেল x\1"),
    (r"Stall: m g sin\(theta\) = (\S+) kN pulled back harder than the engine's best pull min\(P/v, mu N\) = (\S+) kN",
     r"আটকে গেছে: m g sin(theta) = \1 kN পিছনে টেনেছে, ইঞ্জিনের সেরা টান min(P/v, mu N) = \2 kN-এর চেয়ে বেশি"),
    (r"Max grade this train can climb: (\S+) deg \(tan = mu m_loco / m - C_rr\)",
     r"এই ট্রেনের সর্বোচ্চ ওঠার ঢাল: \1 deg (tan = mu m_ইঞ্জিন / m - C_rr)"),
    (r"Steepest grade on your track: (\S+) deg", r"তোমার লাইনের সবচেয়ে খাড়া ঢাল: \1 deg"),
    (r"HIT THE BUFFERS at (\d+) km/h", r"\1 km/h গতিতে বাফারে ধাক্কা"),
    (r"d_stop = v\^2 / \(2 \(mu g cos - g sin\)\): from (\S+) m/s needed (\S+) m, you allowed (\S+) m",
     r"d_stop = v^2 / (2 (mu g cos - g sin)): \1 m/s থেকে দরকার ছিল \2 m, তুমি দিয়েছ \3 m"),
    (r"g sin\(theta\) = (\S+) > mu g cos\(theta\) = (\S+) m/s\^2 on a (\S+) deg descent",
     r"g sin(theta) = \1 > mu g cos(theta) = \2 m/s^2, \3 deg নামার ঢালে"),
    (r"OVERSPEED: (\d+) km/h on the descent", r"অতিরিক্ত গতি: নামার পথে \1 km/h"),
    (r"Going downhill gravity adds g sin\(theta\) = (\S+) m/s\^2 every second\. The line limit is (\S+) km/h\.",
     r"নামার সময় মাধ্যাকর্ষণ প্রতি সেকেন্ডে g sin(theta) = \1 m/s^2 যোগ করে। লাইনের গতিসীমা \2 km/h।"),
    (r"(\d+) trips x (\S+) s \+ returns = (\S+) s > (\S+) s", r"\1 ট্রিপ x \2 s + ফেরা = \3 s > \4 s"),
    (r"(\S+) s of (\S+) s", r"\1 s (সীমা \2 s)"),
    (r"(\S+) MJ per trip", r"প্রতি ট্রিপে \1 MJ"),
    (r"(\S+) m from the stop line", r"থামার দাগ থেকে \1 m"),
    (r"Wagons: (\d+)", r"ওয়াগন: \1"),
    # --- cantilever
    (r"pier: (.+);  tip: (.+)", r"স্তম্ভ: \1;  ডগা: \2"),
    (r"deep haunch is (\S+)x stiffer than the tip", r"গভীর হঞ্চ ডগার চেয়ে \1 গুণ শক্ত"),
    (r"right arm (\S+), left arm (\S+) MN\*m", r"ডান বাহু \1, বাম বাহু \2 MN*m"),
    (r"unbalance (\S+) of \+/-(\S+) MN\*m(  \(landed on abutment\))?",
     lambda m: f"ভারসাম্যহীনতা {m.group(1)} (সীমা +/-{m.group(2)} MN*m)" + ("  (পাড়ে বসেছে)" if m.group(3) else "")),
    (r"M = (\S+) MN\*m, y = (\S+) m, I = (\S+) m\^4", r"M = \1 MN*m, y = \2 m, I = \3 m^4"),
    (r"sigma = (\S+) MPa \(limit (\S+)\)", r"sigma = \1 MPa (সীমা \2)"),
    (r"level: (\w+) \((.+)\)", lambda m: f"মাত্রা: {v(m.group(1))} ({m.group(2)})"),
    (r"Finish every arm first: (.+)", r"আগে সব বাহু শেষ করো: \1"),
    (r"PIER TILT: unbalanced moment (\S+) MN\*m \(tipping (\w+)\) exceeded the foundation's (\S+) MN\*m",
     lambda m: f"স্তম্ভ হেলে পড়েছে: ভারসাম্যহীন ভ্রামক {m.group(1)} MN*m ({v(m.group(2))} হেলছে), ভিত্তির {m.group(3)} MN*m ছাড়িয়েছে"),
    (r"ROOT CRACK: sigma = M\*y/I = (.+) > (\S+) MPa", r"গোড়ায় ফাটল: sigma = M*y/I = \1 > \2 MPa"),
    (r"Segments cast so far: (\d+)\. Capacity = (\S+) \+ (\d+) tie-down\(s\) x (\S+) MN\*m",
     r"এ পর্যন্ত ঢালাই করা অংশ: \1। ক্ষমতা = \2 + \3টি বাঁধন-তার x \4 MN*m"),
    (r"Temporary high-strength anchor cables: \+(\S+) MN\*m resistance for (.+)",
     r"অস্থায়ী উচ্চ-শক্তির নোঙর-তার: \2 খরচে +\1 MN*m সহ্যক্ষমতা"),
    (r"Balance (\S+) MN\*m of \+/-(\S+); root sigma (\S+) MPa", r"ভারসাম্য \1 MN*m (সীমা +/-\2); গোড়ার sigma \3 MPa"),
    (r"x = (\S+) m: M = (\S+) MN\*m (sagging \(bottom pulled\)|hogging \(top pulled\)), d = (.+?), I = b d\^3/12 = (.+?), sigma = M y / I = (\S+) MPa \(allowed (\S+) MPa\); tau = VQ/\(It\) = (\S+) MPa",
     lambda m: (f"x = {m.group(1)} m: M = {m.group(2)} MN*m "
                f"{'ঝুলে পড়া (নিচে টান)' if m.group(3).startswith('sagging') else 'উঁচু হওয়া (উপরে টান)'}, "
                f"d = {m.group(4)}, I = b d^3/12 = {m.group(5)}, sigma = M y / I = {m.group(6)} MPa "
                f"(অনুমোদিত {m.group(7)} MPa); tau = VQ/(It) = {m.group(8)} MPa")),
    (r"worst (\d+)% at x = (\S+) m", r"সর্বোচ্চ \1%, x = \2 m-এ"),
    (r"max \|M\| = (.+)", r"সর্বোচ্চ |M| = \1"),
    (r"(\d+)% of allowed", r"অনুমোদিত সীমার \1%"),
    # --- signals
    (r"(\d+) trains, (\d+) SPAD, (\d+) s waiting, (\d+) misroutes", r"\1টি ট্রেন, \2 SPAD, \3 s অপেক্ষা, \4টি ভুল পথ"),
    (r"t = +(\d+) s   delivered (\d+)   SPAD (\d+)   waiting (\d+) s", r"t = \1 s   পৌঁছেছে \2   SPAD \3   অপেক্ষা \4 s"),
    (r"t = (\d+) s of (\d+)", r"t = \1 s (মোট \2)"),
    (r"(\d+) m;  short blocks: (.+)",
     lambda m: f"{m.group(1)} m;  ছোট ব্লক: " + ("নেই" if m.group(2) == "none" else m.group(2).replace("m", " m"))),
    (r"(\S+): warning (\d+) m < (\d+) m", r"\1: সতর্কতা \2 m < \3 m"),
    (r"Passenger: (\d+) km/h, (\d+) m   Cargo: (\d+) km/h, (\d+) m", r"যাত্রী ট্রেন: \1 km/h, \2 m   মালগাড়ি: \3 km/h, \4 m"),
    (r"S1: (MAIN|HARBOR|moving)", lambda m: "S1: " + {"MAIN": "মূল লাইন", "HARBOR": "বন্দর", "moving": "সরছে"}[m.group(1)]),
    (r"LEVEL CROSSING UNSAFE: train (\d+) reached the road while the barrier was (up|still lowering)",
     lambda m: f"লেভেল ক্রসিং অনিরাপদ: গেট {'উঠানো' if m.group(2) == 'up' else 'তখনও নামছিল'} অবস্থায় ট্রেন {m.group(1)} রাস্তায় পৌঁছেছে"),
    (r"Barrier needs (\d+) s; at (\d+) m/s a train covers (\d+) m in that time - start lowering (\d+) m out \(XING_APPR\)",
     r"গেট নামতে \1 s লাগে; \2 m/s গতিতে ট্রেন ওই সময়ে \3 m যায় - \4 m দূর থেকে নামানো শুরু করো (XING_APPR)"),
    (r"COLLISION \((head-on|rear)\) on (\w+): trains (\d+) and (\d+)",
     lambda m: f"সংঘর্ষ ({'মুখোমুখি' if m.group(1) == 'head-on' else 'পিছন থেকে'}) {m.group(2)}-এ: ট্রেন {m.group(3)} আর {m.group(4)}"),
    (r"DERAILMENT: switch S1 moved while train (\d+) was on it", r"লাইনচ্যুত: ট্রেন \1 থাকার সময় পয়েন্ট S1 সরে গেছে"),
    (r"DERAILMENT: train (\d+) ran onto switch S1 while it was moving", r"লাইনচ্যুত: পয়েন্ট S1 সরার সময় ট্রেন \1 তার উপর উঠে গেছে"),
    (r"SPAD: train (\d+) passed (\S+) at danger", r"SPAD: ট্রেন \1 লাল অবস্থায় \2 পেরিয়েছে"),
    (r"Misroute: (cargo|passenger) train (\d+) sent to (main|harbor)",
     lambda m: f"ভুল পথ: {v(m.group(1))} ট্রেন {m.group(2)} পাঠানো হয়েছে {v(m.group(3))}-এ"),
    (r"(\d+) TRAIN\(S\) MISROUTED", r"\1টি ট্রেন ভুল পথে গেছে"),
    (r"ONLY (\d+) TRAINS GOT THROUGH", r"মাত্র \1টি ট্রেন পার হয়েছে"),
    (r"Target (\d+): waiting (\d+) train-seconds\. Shorter \(but still safe\) blocks raise capacity\.",
     r"লক্ষ্য \1: অপেক্ষা \2 ট্রেন-সেকেন্ড। ছোট (কিন্তু তবুও নিরাপদ) ব্লক ক্ষমতা বাড়ায়।"),
    (r"(\d+) \(cargo to harbor: (\d+)\)", r"\1 (মালগাড়ি বন্দরে: \2)"),
    (r"(\d+) train-seconds", r"\1 ট্রেন-সেকেন্ড"),
    # --- traffic
    (r"Junction: (\w+) \((.+)\)", lambda m: f"মোড়: {v(m.group(1))} ({m.group(2)})"),
    (r"Rush-hour demand: main (\d+) veh/h, market street (\d+) veh/h", r"ভিড়ের চাহিদা: প্রধান সড়ক \1 veh/h, বাজার রাস্তা \2 veh/h"),
    (r"main (\d+) vs demand (\d+);  cross (\d+) vs demand (\d+) veh/h",
     r"প্রধান সড়ক \1 বনাম চাহিদা \2;  বাজার রাস্তা \3 বনাম চাহিদা \4 veh/h"),
    (r"free: q1 = (\d+) veh/h, k1 = (\d+) veh/km;  jam: q2 = 0, k2 = (\d+)",
     r"মুক্ত: q1 = \1 veh/h, k1 = \2 veh/km;  জ্যাম: q2 = 0, k2 = \3"),
    (r"w = (\S+) km/h \(negative = travels backwards\)", r"w = \1 km/h (ঋণাত্মক = পিছনে যায়)"),
    (r"(\S+) veh/min, trips (\d+) s \(main (\S+)x free-flow\)", r"\1 veh/min, যাত্রা \2 s (প্রধান সড়ক মুক্ত-প্রবাহের \3 গুণ)"),
    (r"idling (\d+) car-s, fuel (\S+) L, queued (\d+)", r"অলস \1 গাড়ি-s, জ্বালানি \2 L, লাইনে \3"),
    (r"GRIDLOCK on (MAIN|CROSS): (\d+) cars queued back past the city edge",
     lambda m: f"{v(m.group(1))}-এ অচল জট: {m.group(2)}টি গাড়ি শহরের সীমানার বাইরে পর্যন্ত লাইনে"),
    (r"Demand (\d+) veh/h > capacity s\*g/C = (.+)", r"চাহিদা \1 veh/h > ক্ষমতা s*g/C = \2"),
    (r"Demand (\d+) veh/h exceeded what the junction could pass; q = k v collapses once k > k_crit",
     r"চাহিদা \1 veh/h মোড়ের পার করার ক্ষমতা ছাড়িয়েছে; k > k_crit হলে q = k v ভেঙে পড়ে"),
    (r"Trips took (\S+)x the free-flow time \(limit (\S+)x\)", r"যাত্রায় মুক্ত-প্রবাহের \1 গুণ সময় লেগেছে (সীমা \2 গুণ)"),
    (r"(\d+)  \((\S+) per min\)", r"\1  (প্রতি মিনিটে \2)"),
    (r"([\d.]+)x", r"\1 গুণ"),
    (r"([\d,]+) car-seconds", r"\1 গাড়ি-সেকেন্ড"),
    (r"\+(\d+) waiting", r"+\1 অপেক্ষায়"),
    # --- logistics
    (r"(\d+) trucks add density; v_max 70 km/h, k_jam 120 veh/km", r"\1টি ট্রাক ঘনত্ব বাড়ায়; v_max 70 km/h, k_jam 120 veh/km"),
    (r"v = (\d+) km/h,  (\d+) truck trips", r"v = \1 km/h,  \2টি ট্রাক-ট্রিপ"),
    (r"grip (\d+) kN vs needed (\d+) kN", r"আঁকড়ে ধরা \1 kN বনাম দরকার \2 kN"),
    (r"(Road|Rail|Barge): (\S+) (t|h)", lambda m: f"{v(m.group(1))}: {m.group(2)} {m.group(3)}"),
    (r"(\d+) trips, round trip (\S+) h", r"\1 ট্রিপ, আসা-যাওয়া \2 h"),
    (r"(\d+) trucks at (\d+) km/h \(Greenshields\)", r"\1টি ট্রাক \2 km/h গতিতে (গ্রিনশিল্ডস)"),
    (r"(\d+) train\(s\) x (\d+) wagons, (\d+) km/h on the grade", r"\1টি ট্রেন x \2 ওয়াগন, ঢালে \3 km/h"),
    (r"(\d+) barge\(s\): (\S+) km/h down, (\S+) km/h back", r"\1টি বার্জ: ভাটিতে \2 km/h, ফেরার পথে \3 km/h"),
    (r"done in (\S+) h, (.+)", r"\1 h-এ শেষ, \2"),
    (r"(\S+) h of (\d+) h, fuel (\S+) L, safety index (\S+)", r"\1 h (সীমা \2 h), জ্বালানি \3 L, নিরাপত্তা সূচক \4"),
    (r"cost (Rs .+?);  toll score (.+)", r"খরচ \1;  টোল স্কোর \2"),
    (r"(\S+) h  \|  (Rs .+?)  \|  safety (\S+)", r"\1 h  |  \2  |  নিরাপত্তা \3"),
    (r"Road share: (\d+) t \(the rest\)", r"সড়কের ভাগ: \1 t (বাকিটা)"),
    (r"hour (\S+)", r"ঘণ্টা \1"),
    (r"Cheapest plan meeting the deadline costs (Rs .+) - can you find it\?",
     r"সময়সীমা মানা সবচেয়ে সস্তা পরিকল্পনার খরচ \1 - খুঁজে পাবে?"),
    (r"STALL: (\d+) wagons weigh (\S+) kt - the 1\.2% grade pulls back m g sin\(theta\) = (\d+) kN but adhesion allows only mu m_loco g = (\d+) kN",
     r"আটকে যাবে: \1টি ওয়াগনের ওজন \2 kt - 1.2% ঢাল পিছনে টানে m g sin(theta) = \3 kN, কিন্তু আঁকড়ে ধরা দেয় মাত্র mu m_ইঞ্জিন g = \4 kN"),
    (r"The slowest mode finishes at (\S+) h > (\d+) h", r"সবচেয়ে ধীর পথ শেষ হয় \1 h-এ > \2 h"),
    (r"(\d+) t in (\S+) h, (.+)", r"\1 t, \2 h-এ, \3"),
    (r"(Road|Rail|Barge)", lambda m: v(m.group(1))),
    # --- generic: a slider/label with a value, and chart titles joined with " / "
    (r"(.+?): (-?[\d.,]+)", lambda m: (f"{LABELS[m.group(1)]}: {m.group(2)}" if m.group(1) in LABELS
                                       else m.group(0))),
    (r"(.+ / .+)", lambda m: " / ".join(EXACT.get(p, p) for p in m.group(1).split(" / "))),
]

PATTERNS = DEMO_PATTERNS + PATTERNS
COMPILED = [(re.compile(p), r) for p, r in PATTERNS]

# Technical words that may stay in Latin letters in Bengali mode (formula symbols, units,
# logic-signal names and brand names).
KEEP = {
    "sigma", "epsilon", "theta", "omega", "zeta", "tau", "sqrt", "atan", "tan", "sin", "cos", "ceil",
    "min", "max", "sum", "mpa", "gpa", "kpa", "kn", "mn", "kw", "mw", "mj", "kj", "km", "cm", "mm",
    "veh", "exp", "rs", "spad", "spads", "tmd", "idm", "lwr", "and", "not", "true", "false",
    "bridge", "occ", "appr", "permit", "xing", "cargo", "switch", "harbor", "barrier", "down",
    "deg", "rr", "drag", "loco", "crit", "jam", "tmd", "pod", "alloy", "base", "eq", "tip", "pier",
    "right", "left", "water", "total", "alloy", "stretch", "modis", "bridgeworks", "english",
    "decay", "pcr", "cr", "dstop", "stop", "brake", "eff", "mu", "pi", "kt", "veh", "ok", "per",
}
