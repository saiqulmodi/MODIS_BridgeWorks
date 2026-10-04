"""Help, part 1: a step-by-step guide for new players and a walkthrough for every level."""
from . import qa

START = (
    qa("What is MODIS BridgeWorks and how do I win?",
       "It is an engineering game with 10 levels: bridges, railways, a concrete cantilever, "
       "train signals, a city junction and a freight plan. Every result comes from real physics "
       "formulas. To finish a level, meet its SUCCESS goal without spending more than the budget. "
       "Nothing is ever 'game over': if something breaks, the Black Box shows you exactly why and "
       "you try again.",
       "MODIS BridgeWorks কী, আর কীভাবে জিতব?",
       "এটি 10টি লেভেলের একটি প্রকৌশল খেলা: সেতু, রেললাইন, কংক্রিটের ক্যান্টিলিভার, ট্রেনের সিগন্যাল, "
       "শহরের মোড় আর মালবহনের পরিকল্পনা। প্রতিটি ফল আসল পদার্থবিজ্ঞানের সূত্র থেকে আসে। লেভেল শেষ "
       "করতে বাজেটের বেশি খরচ না করে তার 'সাফল্য' লক্ষ্য পূরণ করো। এখানে কখনো 'গেম ওভার' নেই: কিছু "
       "ভাঙলে ব্ল্যাক বক্স ঠিক কেন ভেঙেছে দেখায়, তারপর আবার চেষ্টা করো।"),
    qa("How do I start a level?",
       "On the menu, click a level card (or press 1-9, and 0 for Level 10). All levels are open, "
       "so you can play in any order, but Levels 1, 2 and 3 are the best start. The Briefing "
       "opens first: it shows the mission, the budget, the par cost, the two paths forward and "
       "the maths you will discover. Press Enter or 'Start building' to begin. F1 opens the "
       "Briefing again at any time.",
       "লেভেল কীভাবে শুরু করব?",
       "মেনুতে একটি লেভেলের কার্ডে ক্লিক করো (অথবা 1-9 চাপো, লেভেল 10-এর জন্য 0)। সব লেভেল খোলা, "
       "তাই যেকোনো ক্রমে খেলা যায়, তবে লেভেল 1, 2 আর 3 দিয়ে শুরু করা সবচেয়ে ভালো। প্রথমে 'নির্দেশনা' "
       "খোলে: সেখানে মিশন, বাজেট, প্যার খরচ, এগোনোর দুই পথ আর যে গণিত শিখবে তা দেখায়। শুরু করতে Enter "
       "বা 'নির্মাণ শুরু করো' চাপো। F1 চাপলে যেকোনো সময় নির্দেশনা আবার খোলে।"),
    qa("What does the top bar show?",
       "Left: the level name and 'Cost / budget'. The cost is green while it is at or below the "
       "par cost (bonus star), yellow while it is within the budget, and red when it is over "
       "budget. Right: the '?' Help button (H), Finance (business plan and loans), Demo (a paid "
       "working solution), the language button (F2), Briefing (F1) and Menu (Esc). Bridge levels "
       "with wind or earthquakes also have a lab button (L).",
       "উপরের বারে কী দেখায়?",
       "বাঁ দিকে: লেভেলের নাম আর 'খরচ / বাজেট'। খরচ প্যার খরচের সমান বা কম থাকলে সবুজ (বোনাস তারা), "
       "বাজেটের মধ্যে থাকলে হলুদ, আর বাজেট ছাড়ালে লাল। ডান দিকে: '?' সাহায্য বোতাম (H), অর্থ "
       "(ব্যবসার পরিকল্পনা ও ঋণ), ডেমো (টাকা দিয়ে একটি কার্যকর সমাধান দেখা), ভাষার বোতাম (F2), "
       "নির্দেশনা (F1) আর মেনু (Esc)। বাতাস বা ভূমিকম্পের সেতু-লেভেলে একটি ল্যাব বোতামও (L) থাকে।"),
    qa("How do I draw a bridge (Levels 1, 7, 8 and 10)?",
       "1) Pick the Deck tool (D) and draw the road from one bank to the other: click a start "
       "point, then an end point (or drag). Hold Shift while clicking to keep drawing from the "
       "last point. 2) Pick the Beam tool (B) and add beams above or below the deck so that "
       "every panel is a triangle. 3) Choose material (M), size S / M / L / XL and shape on the "
       "bottom bar before you draw. 4) Right-click (or the Delete tool, X) removes a beam; "
       "Ctrl+Z undoes. 5) Press SPACE or RUN to send the vehicles across.",
       "সেতু কীভাবে আঁকব (লেভেল 1, 7, 8 ও 10)?",
       "1) 'ডেক' টুল (D) নিয়ে এক পাড় থেকে অন্য পাড় পর্যন্ত রাস্তা আঁকো: একটি শুরুর বিন্দুতে, তারপর "
       "শেষের বিন্দুতে ক্লিক করো (অথবা টেনে আনো)। Shift চেপে ক্লিক করলে শেষ বিন্দু থেকে আঁকা চলতে থাকে। "
       "2) 'বিম' টুল (B) নিয়ে ডেকের উপরে বা নিচে বিম যোগ করো, যাতে প্রতিটি ঘর ত্রিভুজ হয়। 3) আঁকার "
       "আগে নিচের বারে উপাদান (M), আকার S / M / L / XL আর গড়ন বেছে নাও। 4) ডান-ক্লিক (বা 'মুছো' টুল, X) "
       "বিম সরায়; Ctrl+Z ফেরায়। 5) গাড়ি পার করাতে SPACE বা 'চালাও' চাপো।"),
    qa("What do the colours mean while I build?",
       "With TEST on (T), every beam is coloured by its load ratio = force / the force it can "
       "carry, with the vehicle parked at its worst spot. Green: under 50%. Yellow: 50-80%. "
       "Red: 80-100%, close to breaking. Over 100% the beam fails. Aim for green and yellow: a "
       "bridge that is all dark green is wasting money, and red beams need more area, a better "
       "shape or a shorter length.",
       "বানানোর সময় রংগুলোর মানে কী?",
       "'পরীক্ষা' (T) চালু থাকলে প্রতিটি বিম তার ভার-অনুপাত = বল / যে বল সে বইতে পারে, সেই অনুযায়ী রং "
       "পায়, আর গাড়িটি থাকে সবচেয়ে কঠিন জায়গায়। সবুজ: 50%-এর কম। হলুদ: 50-80%। লাল: 80-100%, ভাঙার "
       "কাছাকাছি। 100% পেরোলে বিম ভেঙে যায়। সবুজ আর হলুদ লক্ষ্য রাখো: পুরো সেতু গাঢ় সবুজ মানে টাকা "
       "নষ্ট, আর লাল বিমের দরকার বেশি ক্ষেত্রফল, ভালো গড়ন বা কম দৈর্ঘ্য।"),
    qa("How do I see the maths behind a beam?",
       "Pick the Select tool (S) and click any beam, joint or vehicle. The scientific calculator "
       "on the right (C opens and closes it) shows the formula, your numbers plugged in, and the "
       "answer: N, sigma = N / A, the buckling load P_cr and the factor of safety. For a beam you "
       "can slide its cross-section area A and watch the stress change at once. Vectors (V) draws "
       "the force arrows; Sag (F) exaggerates how far the bridge bends.",
       "একটি বিমের পেছনের গণিত কীভাবে দেখব?",
       "'বাছাই' টুল (S) নিয়ে যেকোনো বিম, জোড় বা গাড়িতে ক্লিক করো। ডানের বৈজ্ঞানিক ক্যালকুলেটর "
       "(C চাপলে খোলে ও বন্ধ হয়) সূত্র, তাতে বসানো তোমার সংখ্যা আর উত্তর দেখায়: N, sigma = N / A, "
       "বাকলিং ভার P_cr আর নিরাপত্তা গুণক। কোনো বিমের প্রস্থচ্ছেদের ক্ষেত্রফল A স্লাইড করে সঙ্গে সঙ্গে "
       "পীড়নের পরিবর্তন দেখতে পারো। 'বল-তীর' (V) বলের তীর আঁকে; 'ঝোলা' (F) সেতু কতটা বাঁকে তা বাড়িয়ে দেখায়।"),
    qa("What happens when I press RUN?",
       "The real simulation plays: vehicles drive across (or trains run, traffic flows, ships "
       "sail) and every force is recalculated many times a second. The speed button (x1, x2...) "
       "makes it faster. If everything survives and the goal is met, the Results screen gives "
       "stars, EXP, the factor of safety and the business plan. If anything breaks, the run "
       "freezes at the first failure and the Black Box opens.",
       "'চালাও' চাপলে কী হয়?",
       "আসল সিমুলেশন চলে: গাড়ি পার হয় (অথবা ট্রেন চলে, যানবাহন চলে, জাহাজ ভাসে) আর প্রতি সেকেন্ডে "
       "বহুবার প্রতিটি বল নতুন করে হিসাব হয়। গতির বোতাম (x1, x2...) দিয়ে দ্রুত করা যায়। সব টিকে "
       "থাকলে আর লক্ষ্য পূরণ হলে ফলাফলের পর্দায় তারা, EXP, নিরাপত্তা গুণক আর ব্যবসার পরিকল্পনা দেখায়। "
       "কিছু ভাঙলে প্রথম ব্যর্থতার মুহূর্তে সব থেমে যায় আর ব্ল্যাক বক্স খোলে।"),
    qa("Something broke. What is the Black Box?",
       "The Black Box Investigation shows the exact formula that failed with your numbers, a "
       "history chart, and a quiz: pick the real cause. Opening it gives 10 EXP and a correct "
       "first answer gives 50 EXP more. You also get salvage: 30% of the failed build cost is "
       "added to that level's budget. 'Edit & retry' (R) takes you back to your design. Some "
       "levels offer an Alternate route that finishes the level another way (1 star, 30 EXP).",
       "কিছু ভেঙে গেছে। ব্ল্যাক বক্স কী?",
       "ব্ল্যাক বক্স তদন্ত তোমার সংখ্যা বসিয়ে ঠিক কোন সূত্রটি ব্যর্থ হয়েছে, একটি ইতিহাসের চার্ট, আর "
       "একটি কুইজ দেখায়: আসল কারণটি বেছে নাও। খুললেই 10 EXP, আর প্রথমবারেই সঠিক উত্তর দিলে আরও 50 EXP। "
       "উদ্ধার-মূল্যও পাও: ভাঙা নকশার খরচের 30% ওই লেভেলের বাজেটে যোগ হয়। 'আবার চেষ্টা করো' (R) "
       "তোমাকে নকশায় ফেরায়। কিছু লেভেলে 'বিকল্প পথ' থাকে, যা অন্যভাবে লেভেল শেষ করে (1 তারা, 30 EXP)।"),
    qa("How do stars and EXP work?",
       "1 star: the mission succeeded within your funds (budget plus any approved loan). "
       "2 stars: the cost was also at or below the par cost. 3 stars: the extra goal was also "
       "met - for bridges and the cantilever a factor of safety between 1.5 and 4, for other "
       "levels the level's own bonus goal. Each success gives 100 + 50 x stars EXP.",
       "তারা আর EXP কীভাবে কাজ করে?",
       "1 তারা: তোমার তহবিলের (বাজেট আর অনুমোদিত ঋণ) মধ্যে মিশন সফল। 2 তারা: খরচও প্যার খরচের সমান "
       "বা কম। 3 তারা: বাড়তি লক্ষ্যও পূরণ - সেতু ও ক্যান্টিলিভারে নিরাপত্তা গুণক 1.5 থেকে 4-এর মধ্যে, "
       "অন্য লেভেলে সেই লেভেলের নিজের বোনাস লক্ষ্য। প্রতিটি সাফল্যে 100 + 50 x তারা EXP পাও।"),
    qa("What is the Demo button?",
       "Demo plays a working solution and explains why it works. It costs 0.5% of that level's "
       "budget, taken from the budget for good. A warning shows the old and new budget before "
       "anything is charged, and 'No, keep my budget' cancels. Once paid, replays are free. A "
       "demo never earns stars or EXP, and 'Back to my design' returns your own design.",
       "'ডেমো' বোতাম কী?",
       "ডেমো বোতাম একটি কার্যকর সমাধান চালিয়ে দেখায় আর বোঝায় কেন সেটি কাজ করে। এর দাম ওই লেভেলের "
       "বাজেটের 0.5%, যা বাজেট থেকে চিরতরে কাটা যায়। কিছু কাটার আগে একটি সতর্কবার্তা পুরোনো আর নতুন বাজেট "
       "দেখায়, আর 'না, আমার বাজেট রাখো' চাপলে বাতিল হয়। একবার টাকা দিলে আবার দেখা বিনামূল্যে। প্রদর্শনীতে "
       "কখনো তারা বা EXP মেলে না, আর 'আমার নকশায় ফেরো' তোমার নিজের নকশা ফিরিয়ে দেয়।"),
    qa("My design costs more than the budget. Can I still build it?",
       "Yes, with a loan. When you press RUN over budget, a Business Plan opens first. A bank loan "
       "(2% a year, 10 years) covers the shortfall; a government subsidised loan (0.5% a year, "
       "15 years, up to half the budget) can take the first part. The loan is approved only if "
       "first-year toll income minus upkeep is at least 1.5 x the yearly loan payments. The "
       "Finance button shows the plan at any time.",
       "আমার নকশার খরচ বাজেটের বেশি। তবুও কি বানাতে পারি?",
       "হ্যাঁ, ঋণ নিয়ে। বাজেটের বেশি খরচে 'চালাও' চাপলে আগে একটি ব্যবসার পরিকল্পনা খোলে। ব্যাংক ঋণ "
       "(বছরে 2%, 10 বছর) ঘাটতি মেটায়; সরকারি ভর্তুকির ঋণ (বছরে 0.5%, 15 বছর, বাজেটের অর্ধেক পর্যন্ত) "
       "প্রথম অংশটা নিতে পারে। ঋণ মঞ্জুর হয় শুধু তখনই, যখন প্রথম বছরের টোল আয় থেকে রক্ষণাবেক্ষণ বাদ দিয়ে "
       "বছরের ঋণ-কিস্তির অন্তত 1.5 গুণ থাকে। 'অর্থ' বোতাম যেকোনো সময় পরিকল্পনাটি দেখায়।"),
    qa("Which keys and buttons work everywhere?",
       "H or '?': this Help. F1: Briefing. F2: English / Bengali (remembered). F11: full screen. "
       "C: calculator. Esc: back to the menu (in Help, Esc closes Help). SPACE: run (bridge and "
       "rail levels). Ctrl+Z: undo. In bridge levels, 3 switches the 3D view; in 3D, turn the "
       "view with the arrow keys, middle-drag or Alt + drag, zoom with the mouse wheel or + / -, "
       "and Home resets the view. Hover over any bottom-bar button for its IDEA tip.",
       "কোন চাবি আর বোতাম সব জায়গায় কাজ করে?",
       "H বা '?': এই সাহায্য। F1: নির্দেশনা। F2: ইংরেজি / বাংলা (মনে রাখা হয়)। F11: পূর্ণ পর্দা। "
       "C: ক্যালকুলেটর। Esc: মেনুতে ফেরা (সাহায্যের ভেতরে Esc সাহায্য বন্ধ করে)। SPACE: চালাও (সেতু আর "
       "রেলের লেভেলে)। Ctrl+Z: ফেরাও। সেতুর লেভেলে 3 চাবি 3D দৃশ্য বদলায়; 3D-তে তীর-চাবি, মাঝের বোতাম "
       "বা Alt চেপে টেনে দৃশ্য ঘোরাও, মাউসের চাকা বা + / - দিয়ে কাছে-দূরে নাও, Home দৃশ্য আগের মতো করে। "
       "নিচের বারের যেকোনো বোতামে মাউস রাখলে তার 'আইডিয়া' টিপস দেখায়।"),
    qa("Is my progress saved, and can I replay a level?",
       "Yes. Stars, EXP, salvage, demo purchases, your attempts and the language are saved "
       "automatically. You can replay any level at any time; your best stars are kept, and a new "
       "success adds EXP again. All levels are unlocked, so you may play them in any order.",
       "আমার অগ্রগতি কি সংরক্ষিত হয়, আর লেভেল কি আবার খেলা যায়?",
       "হ্যাঁ। তারা, EXP, উদ্ধার-মূল্য, কেনা প্রদর্শনী, তোমার চেষ্টাগুলো আর ভাষা নিজে থেকেই সংরক্ষিত হয়। যেকোনো লেভেল যেকোনো "
       "সময় আবার খেলতে পারো; তোমার সেরা তারা রাখা হয়, আর নতুন সাফল্যে আবার EXP যোগ হয়। সব লেভেল খোলা, তাই যেকোনো ক্রমে "
       "খেলতে পারো।"),
    qa("How do I win Level 1, The Creek Crossing?",
       "Goal: the 3.5 t bakery van crosses the 16 m gap (x = 12 to 28 m). Budget Rs 2.50 L, par "
       "Rs 1.00 L. Draw the deck along y = 0 from bank to bank in pieces of 8 m or less (beams "
       "are limited to 8 m here). Add triangles above it, e.g. a Warren truss 3 m high, and tie "
       "the truss to the lower anchors at y = -3 if you build below. Timber is cheap; use a "
       "hollow box or I-beam shape so the top chord does not buckle. Check that TEST shows no "
       "red, then press SPACE.",
       "লেভেল 1, খাঁড়ির সেতু কীভাবে জিতব?",
       "লক্ষ্য: 3.5 t-এর বেকারির ভ্যান 16 m ফাঁক (x = 12 থেকে 28 m) পার হবে। বাজেট Rs 2.50 L, প্যার "
       "Rs 1.00 L। y = 0 বরাবর এক পাড় থেকে অন্য পাড় পর্যন্ত 8 m বা তার ছোট টুকরোয় ডেক আঁকো (এখানে বিম "
       "সর্বোচ্চ 8 m)। তার উপরে ত্রিভুজ যোগ করো, যেমন 3 m উঁচু একটি ওয়ারেন ট্রাস; নিচে বানালে ট্রাসকে "
       "y = -3-এর নিচের নোঙরে বাঁধো। কাঠ সস্তা; উপরের কর্ড যাতে বাকল না করে সেজন্য ফাঁপা বাক্স বা আই-বিম "
       "গড়ন নাও। 'পরীক্ষা'-তে কোনো লাল নেই দেখে SPACE চাপো।", level=1),
    qa("How do I win Level 2, The Timber Incline?",
       "Goal: haul 120 t of logs up to the ridge within 2 minutes without stalling. Drag the round "
       "track handles to shape the slope ('Even grade' makes one steady 8% slope between the "
       "stations). Each wagon carries 30 t. The engine can only pull mu x its own weight on dry "
       "rails (mu = 0.30). The Diesel shunter (60 t) grips about 177 kN; with 2 wagons the 150 t "
       "train needs about 120 kN on 8%, so it climbs - with 4 wagons it slips. So: shunter, 2 "
       "wagons, two quick trips. A banker engine is the costly, robust path.",
       "লেভেল 2, কাঠের ঢাল কীভাবে জিতব?",
       "লক্ষ্য: আটকে না গিয়ে 2 মিনিটের মধ্যে 120 t কাঠ শৈলশিরায় তোলা। গোল হাতলগুলো টেনে লাইনের ঢাল "
       "বানাও ('সমান ঢাল' স্টেশনগুলোর মধ্যে একটানা 8% ঢাল করে)। প্রতিটি ওয়াগন 30 t নেয়। শুকনো লাইনে "
       "ইঞ্জিন নিজের ওজনের mu গুণের (mu = 0.30) বেশি টানতে পারে না। ডিজেল শান্টার (60 t) প্রায় 177 kN "
       "আঁকড়ে ধরে; 2 ওয়াগনসহ 150 t-এর ট্রেনের 8% ঢালে লাগে প্রায় 120 kN, তাই সে ওঠে - 4 ওয়াগনে চাকা "
       "পিছলায়। তাই: শান্টার, 2 ওয়াগন, দুটি দ্রুত যাত্রা। ব্যাংকার ইঞ্জিন হলো দামি কিন্তু নিশ্চিত পথ।",
       level=2),
    qa("How do I win Level 3, The Deep Canyon Pier?",
       "Goal: build a 66 m concrete girder outward from two piers (at 18 m and 48 m), stitch the "
       "middle, and let a 40 t truck cross. First set the haunch depths in the calculator (only "
       "possible before the first cast). Then cast 3 m segments with the four CAST buttons, "
       "alternating left and right so each pier's see-saw meter stays inside its limit. Add a "
       "tie-down on a pier if the meter gets close. When all four arms are complete press STITCH "
       "& POST-TENSION, then TRUCK TEST.",
       "লেভেল 3, গভীর গিরিখাতের স্তম্ভ কীভাবে জিতব?",
       "লক্ষ্য: দুটি স্তম্ভ (18 m আর 48 m-এ) থেকে বাইরের দিকে 66 m কংক্রিটের গার্ডার বানানো, মাঝখান "
       "জোড়া দেওয়া, আর 40 t-এর ট্রাক পার করানো। প্রথমে ক্যালকুলেটরে হঞ্চের গভীরতা ঠিক করো (প্রথম ঢালাইয়ের "
       "আগেই শুধু সম্ভব)। তারপর চারটি CAST বোতামে 3 m-এর অংশ ঢালো, বাঁ আর ডান পালা করে, যাতে প্রতিটি "
       "স্তম্ভের ঢেঁকি-মিটার সীমার মধ্যে থাকে। মিটার সীমার কাছে গেলে স্তম্ভে একটি বাঁধন-তার দাও। চারটি "
       "বাহু শেষ হলে 'জোড়া দাও ও পোস্ট-টেনশন', তারপর 'ট্রাক পরীক্ষা' চাপো।", level=3),
    qa("How do I win Level 4, Freight Mountain Pass?",
       "Goal: move 600 t over the pass to the terminal within 8 minutes and stop before the "
       "buffers. Rain makes the far side wet: grip falls from mu = 0.30 to 0.18. Each wagon "
       "carries 60 t. A Mainline diesel with 5 wagons does it in two trips. The key is the brake "
       "marker: on the wet descent the train needs a longer stopping distance, so move the marker "
       "earlier (the demo brakes 80 m before the stop line). Keep the descent gentle - if "
       "g sin(theta) > mu g cos(theta) no brake can hold the train.",
       "লেভেল 4, মালবাহী পাহাড়ি গিরিপথ কীভাবে জিতব?",
       "লক্ষ্য: 8 মিনিটের মধ্যে 600 t গিরিপথ পেরিয়ে টার্মিনালে নেওয়া আর বাফারের আগে থামা। বৃষ্টিতে ওপারের "
       "লাইন ভেজা: আঁকড়ে ধরা mu = 0.30 থেকে 0.18-এ নামে। প্রতিটি ওয়াগন 60 t নেয়। 5 ওয়াগনসহ একটি মেইনলাইন "
       "ডিজেল দুই যাত্রায় কাজটা করে। আসল চাবিকাঠি ব্রেকের চিহ্ন: ভেজা নামায় ট্রেনের থামতে বেশি পথ লাগে, তাই "
       "চিহ্নটা আগে সরাও (প্রদর্শনী থামার দাগের 80 m আগে ব্রেক করে)। নামা ঢাল কম রাখো - g sin(theta) > "
       "mu g cos(theta) হলে কোনো ব্রেকই ট্রেন ধরে রাখতে পারে না।", level=4),
    qa("How do I win Level 5, The Harbor Switchyard?",
       "Goal: 12 minutes with no collision, derailment or crossing incident, at least 10 trains "
       "delivered, and every cargo train sent to the harbor. Click the dots beside the tracks to "
       "place signals (100-750 m out). The starter interlocking has three bugs: 1) each PERMIT "
       "must also have NOT the other direction's PERMIT, 2) SWITCH_HARBOR should use CARGO_AT_JE, "
       "3) BARRIER_DOWN needs XING_APPR. The demo uses one signal 400 m out on each side.",
       "লেভেল 5, বন্দরের সুইচইয়ার্ড কীভাবে জিতব?",
       "লক্ষ্য: 12 মিনিট কোনো সংঘর্ষ, লাইনচ্যুতি বা লেভেল-ক্রসিং দুর্ঘটনা ছাড়া, অন্তত 10টি ট্রেন পৌঁছানো, "
       "আর প্রতিটি মালগাড়ি বন্দরে পাঠানো। লাইনের পাশের বিন্দুতে ক্লিক করে সিগন্যাল বসাও (100-750 m দূরে)। "
       "শুরুর ইন্টারলকিংয়ে তিনটি ভুল আছে: 1) প্রতিটি PERMIT-এ অন্য দিকের PERMIT-এর NOT-ও লাগবে, "
       "2) SWITCH_HARBOR-এ CARGO_AT_JE ব্যবহার করো, 3) BARRIER_DOWN-এ XING_APPR লাগবে। প্রদর্শনী প্রতিটি "
       "দিকে 400 m দূরে একটি করে সিগন্যাল ব্যবহার করে।", level=5),
    qa("How do I win Level 6, Urban Bottleneck?",
       "Goal: 12 minutes of rush hour without gridlock, with main-road trips no more than 1.8 x "
       "the free-flow time; bonus for idling under 4000 car-seconds. Choose the junction at the "
       "bottom left: signals (Rs 4 L) are cheapest but need a good cycle and green split; a "
       "roundabout (Rs 12 L) is under the par of Rs 15 L and keeps cars moving; an overpass "
       "(Rs 45 L) never jams but misses the par star. The demo uses the roundabout.",
       "লেভেল 6, শহরের যানজট-মোড় কীভাবে জিতব?",
       "লক্ষ্য: যানজটে আটকে না গিয়ে 12 মিনিটের ভিড়, আর প্রধান সড়কের যাত্রা ফাঁকা রাস্তার সময়ের 1.8 গুণের "
       "বেশি নয়; 4000 গাড়ি-সেকেন্ডের কম দাঁড়িয়ে থাকলে বোনাস। নিচে বাঁ দিকে মোড়ের ধরন বাছো: ট্রাফিক "
       "সিগন্যাল (Rs 4 L) সবচেয়ে সস্তা, কিন্তু ভালো চক্র আর সবুজের ভাগ লাগে; গোলচত্বর (Rs 12 L) Rs 15 L "
       "প্যারের নিচে আর গাড়ি চলমান রাখে; উড়ালসেতু (Rs 45 L) কখনো আটকায় না, কিন্তু প্যার তারা পায় না। "
       "প্রদর্শনী গোলচত্বর ব্যবহার করে।", level=6),
    qa("How do I win Level 7, Gale-Force Gorge?",
       "Goal: four 12 t buses cross a 48 m gorge while the wind rises from 4 to 36 m/s. The danger "
       "is resonance: vortices shed at f_v = St U / D (St = 0.12, deck depth D = 1.2 m), so they "
       "match the bridge's natural frequency f_n at U_crit = f_n x 1.2 / 0.12 = 10 f_n, and they lock "
       "on from about 75% of U_crit. Either build a stiff truss with f_n above about 4.8 Hz (so "
       "even 36 m/s stays below the lock-in band), or open the Wind lab (L) and add fairings, "
       "dampers or a tuned mass damper. The demo uses a deep steel "
       "Warren truss with fairings.",
       "লেভেল 7, ঝড়ো হাওয়ার খাদ কীভাবে জিতব?",
       "লক্ষ্য: বাতাস 4 থেকে 36 m/s-এ ওঠার সময় 12 t-এর চারটি বাস 48 m খাদ পার হবে। বিপদ হলো অনুনাদ: "
       "ঘূর্ণি ঝরে f_v = St U / D হারে (St = 0.12, ডেকের গভীরতা D = 1.2 m), তাই সেতুর স্বাভাবিক কম্পাঙ্ক "
       "f_n-এর সঙ্গে মেলে U_crit = f_n x 1.2 / 0.12 = 10 f_n বাতাসে, আর U_crit-এর প্রায় 75% থেকেই আটকে যায়। হয় "
       "f_n প্রায় 4.8 Hz-এর বেশি রেখে শক্ত ট্রাস বানাও (তাহলে 36 m/s-ও আটকে যাওয়ার সীমার নিচে থাকে), নয়তো 'বাতাসের ল্যাব' (L) খুলে ফেয়ারিং, ড্যাম্পার বা টিউনড মাস "
       "ড্যাম্পার দাও। প্রদর্শনী ফেয়ারিংসহ একটি গভীর ইস্পাতের ওয়ারেন ট্রাস ব্যবহার করে।", level=7),
    qa("How do I win Level 8, Earthquake Fault Viaduct?",
       "Goal: a 20 t truck crosses during a strong earthquake (peak ground acceleration 0.35 g). "
       "Build the deck on columns standing on the footings at the valley floor (every 4 m from "
       "x = 10 to 42), with a diagonal in every bay. Beams are limited to 8 m here, so build each "
       "12 m column from two 6 m pieces. Base shear is V = C M a_g: a stiff bridge "
       "gets C = 2.5. Isolation bearings (Quake lab, L) stretch the period to 2.5 s so C drops to "
       "0.5 - but the deck then moves more, so add flexible joints too (gap 0.40 m instead of "
       "0.05 m).",
       "লেভেল 8, ভূমিকম্প-ফাটলের উঁচু সেতু কীভাবে জিতব?",
       "লক্ষ্য: জোরালো ভূমিকম্পের (মাটির সর্বোচ্চ ত্বরণ 0.35 g) মধ্যে 20 t-এর ট্রাক পার হবে। উপত্যকার "
       "তলায় পাদভিত্তির (x = 10 থেকে 42, প্রতি 4 m-এ) উপর দাঁড়ানো স্তম্ভে ডেক বানাও, প্রতিটি খোপে একটি "
       "কর্ণ দিয়ে। এখানে বিম সর্বোচ্চ 8 m, তাই প্রতিটি 12 m স্তম্ভ দুটি 6 m টুকরোয় বানাও। ভিত্তির কর্তন-বল V = C M a_g: শক্ত সেতুর C = 2.5। আইসোলেশন বিয়ারিং (ভূমিকম্পের ল্যাব, "
       "L) পর্যায়কাল 2.5 s করে, তাতে C নেমে 0.5 হয় - কিন্তু তখন ডেক বেশি নড়ে, তাই নমনীয় জোড়ও দাও (ফাঁক "
       "0.05 m-এর বদলে 0.40 m)।", level=8),
    qa("How do I win Level 9, Heavy Industrial Corridor?",
       "Goal: ship 6000 t to the port within 24 hours and within the Rs 18 L budget; bonus for a "
       "safety index of 95 or more. Use the sliders to split the tonnes between road, rail and "
       "barge and to hire fleets. One freight loco can pull at most about 30 wagons (60 t each) "
       "up the 1.2% grade before its wheels slip. 'Optimizer' plots every plan so you can pick "
       "one on the Pareto frontier. The demo sends 5000 t by one 30-wagon train and 1000 t by "
       "barge.",
       "লেভেল 9, ভারী শিল্প করিডর কীভাবে জিতব?",
       "লক্ষ্য: 24 ঘণ্টার মধ্যে আর Rs 18 L বাজেটের মধ্যে 6000 t বন্দরে পাঠানো; নিরাপত্তা সূচক 95 বা বেশি "
       "হলে বোনাস। স্লাইডার দিয়ে টন সড়ক, রেল আর বার্জে ভাগ করো আর বাহন ভাড়া করো। একটি মালবাহী ইঞ্জিন "
       "1.2% ঢালে চাকা পিছলানোর আগে প্রায় 30টি ওয়াগন (প্রতিটি 60 t) পর্যন্ত টানতে পারে। 'অপ্টিমাইজার' সব "
       "পরিকল্পনা আঁকে, যাতে প্যারেটো সীমান্তের একটি বেছে নিতে পারো। প্রদর্শনী 30 ওয়াগনের একটি ট্রেনে "
       "5000 t আর বার্জে 1000 t পাঠায়।", level=9),
    qa("How do I win Level 10, The Continental Megastructure?",
       "Goal: the maglev pod train crosses the 64 m strait (x = 8 to 72) in under 9.5 s while the "
       "wind rises to 22 m/s. Beams may be up to 12 m and cables up to 80 m. Two rock islands "
       "(x = 22-32 and 48-58) have footings at x = 26, 28, 52 and 54: prop the deck there with "
       "V-shaped piers. Give the smart grid enough MW (Grid & wind lab, L) - the pod needs power "
       "for thrust, and powered smart alloy also draws 50 kW per tonne. The demo is a steel deck "
       "truss on V-piers.",
       "লেভেল 10, মহাদেশ-জোড়া মহাসেতু কীভাবে জিতব?",
       "লক্ষ্য: বাতাস 22 m/s-এ ওঠার সময় ম্যাগলেভ পড-ট্রেন 9.5 s-এর কমে 64 m প্রণালী (x = 8 থেকে 72) পার "
       "হবে। বিম সর্বোচ্চ 12 m আর তার সর্বোচ্চ 80 m। দুটি পাথুরে দ্বীপে (x = 22-32 আর 48-58) x = 26, 28, "
       "52 ও 54-এ পাদভিত্তি আছে: সেখানে V-আকৃতির স্তম্ভ দিয়ে ডেককে ঠেকনা দাও। স্মার্ট গ্রিডকে যথেষ্ট MW দাও "
       "('গ্রিড ও বাতাসের ল্যাব', L) - পডের ঠেলার জন্য বিদ্যুৎ লাগে, আর চালু স্মার্ট সংকর ধাতুও প্রতি টনে "
       "50 kW নেয়। প্রদর্শনী V-স্তম্ভের উপর একটি ইস্পাতের ডেক ট্রাস।", level=10),
)
