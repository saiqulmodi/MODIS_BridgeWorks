"""Help, Q151-200: money, loans and business plans, and how to optimise every level."""
from . import qa

MONEY = (
    # --- budget, par, stars --------------------------------------------------------------
    qa("What is the difference between budget, par cost and cost?",
       "Cost is what your current design costs, shown live in the top bar. The budget is the money "
       "you have; going over it needs a loan. The par cost is the target an expert would hit: stay "
       "at or under it for the second star. The cost turns green at or under par, yellow under "
       "budget and red over budget.",
       "বাজেট, প্যার খরচ আর খরচের পার্থক্য কী?",
       "খরচ হলো তোমার এখনকার নকশার দাম, উপরের বারে সরাসরি দেখায়। বাজেট হলো তোমার কাছে থাকা টাকা; তার বেশি গেলে "
       "ঋণ লাগে। প্যার খরচ হলো একজন দক্ষ প্রকৌশলীর লক্ষ্য: দ্বিতীয় তারার জন্য এর সমান বা নিচে থাকো। খরচ প্যারের সমান "
       "বা নিচে সবুজ, বাজেটের নিচে হলুদ আর বাজেটের উপরে লাল হয়।"),
    qa("What makes up a bridge's cost?",
       "Four lines: Materials (density x area x length x price per kg x shape factor), Labour & "
       "scaffolding (Rs 2,500 per member, Rs 4,000 per non-anchor joint, about Rs 300 per metre of "
       "height per member), Maintenance (5 yr) (a share of the material cost) and Equipment & "
       "extras (dampers, bearings, grid power, the maglev guideway). The top bar shows the sum, "
       "updated with every beam you draw.",
       "একটি সেতুর খরচ কী দিয়ে তৈরি?",
       "চারটি লাইন: উপাদান (ঘনত্ব x ক্ষেত্রফল x দৈর্ঘ্য x প্রতি kg দাম x গড়নের গুণক), শ্রম ও ভারা (প্রতি সদস্যে Rs 2,500, "
       "নোঙর নয় এমন প্রতি জোড়ে Rs 4,000, প্রতি সদস্যে প্রতি মিটার উচ্চতায় প্রায় Rs 300), রক্ষণাবেক্ষণ (5 বছর) "
       "(উপাদানের খরচের একটি ভাগ) আর সরঞ্জাম ও বাড়তি (ড্যাম্পার, বিয়ারিং, গ্রিডের শক্তি, ম্যাগলেভের পথ)। উপরের বার "
       "এদের যোগফল দেখায়, প্রতিটি বিম আঁকার সঙ্গে সঙ্গে হালনাগাদ হয়।"),
    qa("In Level 1, why is labour bigger than materials?",
       "Timber is so cheap that the work dominates. The Level 1 demo bridge costs Rs 61,960: "
       "materials only Rs 13,728, labour Rs 44,800 (72%), maintenance Rs 3,432. A steel Warren "
       "with four panels costs about Rs 1.50 L - over the Rs 1.00 L par - mostly because it has "
       "twice as many members and joints. Fewer, bigger timber members win.",
       "লেভেল 1-এ উপাদানের চেয়ে শ্রমের খরচ বেশি কেন?",
       "কাঠ এত সস্তা যে কাজের খরচই প্রধান। লেভেল 1-এর প্রদর্শনী-সেতুর খরচ Rs 61,960: উপাদান মাত্র Rs 13,728, শ্রম "
       "Rs 44,800 (72%), রক্ষণাবেক্ষণ Rs 3,432। চার ঘরের ইস্পাতের ওয়ারেনের খরচ প্রায় Rs 1.50 L - Rs 1.00 L প্যারের "
       "উপরে - মূলত কারণ এতে দ্বিগুণ সদস্য আর জোড়। কম কিন্তু বড় কাঠের সদস্যই জেতে।"),
    qa("Exactly when do I get 1, 2 or 3 stars?",
       "1 star: success and cost within your funds (budget plus any approved loan). 2 stars: also "
       "cost at or under par - a loan does not move the par. 3 stars: also the extra goal (FS 1.5-4 "
       "for structures, or the level's bonus such as zero SPADs, idling under 4000 car-seconds, a "
       "safety index of 95, or stopping within 15 m). Your best result per level is kept.",
       "ঠিক কখন 1, 2 বা 3 তারা পাব?",
       "1 তারা: সাফল্য আর তহবিলের (বাজেট আর অনুমোদিত ঋণ) মধ্যে খরচ। 2 তারা: খরচ প্যারের সমান বা নিচেও - ঋণ প্যার "
       "সরায় না। 3 তারা: বাড়তি লক্ষ্যও (কাঠামোর জন্য FS 1.5-4, অথবা লেভেলের বোনাস, যেমন শূন্য SPAD, 4000 গাড়ি-সেকেন্ডের "
       "কম দাঁড়ানো, 95 নিরাপত্তা সূচক, বা 15 m-এর মধ্যে থামা)। প্রতিটি লেভেলে তোমার সেরা ফল রাখা হয়।"),
    qa("How do I earn EXP?",
       "A success gives 100 + 50 x stars (up to 250). Opening the Black Box after a failure gives "
       "10, a correct diagnosis on the first try 50 more, and finishing by the alternate route 30. "
       "Demonstrations give nothing. So a failure you learn from is worth 60 EXP - failing "
       "smartly is part of the game.",
       "EXP কীভাবে অর্জন করব?",
       "একটি সাফল্যে 100 + 50 x তারা (সর্বোচ্চ 250)। ব্যর্থতার পর ব্ল্যাক বক্স খুললে 10, প্রথম চেষ্টায় সঠিক নির্ণয়ে আরও "
       "50, আর বিকল্প পথে শেষ করলে 30। প্রদর্শনী কিছুই দেয় না। তাই যে ব্যর্থতা থেকে শেখো তার দাম 60 EXP - বুদ্ধি করে "
       "ব্যর্থ হওয়াও খেলার অংশ।"),
    qa("What is salvage?",
       "When a design fails, 30% of its build cost is recovered as salvage and added to that "
       "level's budget for good - the top bar shows '+salvage'. It adds up over several failures. "
       "So a bold, cheap experiment that fails still leaves you with more money for the next try.",
       "উদ্ধার-মূল্য (salvage) কী?",
       "কোনো নকশা ব্যর্থ হলে তার খরচের 30% উদ্ধার-মূল্য হিসেবে ফেরত আসে আর ওই লেভেলের বাজেটে স্থায়ীভাবে যোগ হয় - "
       "উপরের বারে '+উদ্ধার' দেখায়। কয়েকটি ব্যর্থতায় এটি জমতে থাকে। তাই সাহসী, সস্তা কোনো পরীক্ষা ব্যর্থ হলেও পরের "
       "চেষ্টার জন্য তোমার হাতে বেশি টাকা থাকে।"),
    qa("How much does a demo cost in each level?",
       "0.5% of the level's base budget, once: Level 1 Rs 1,250; Level 2 Rs 6,000; Level 3 Rs 47,500; "
       "Level 4 Rs 20,000; Level 5 Rs 15,000; Level 6 Rs 25,000; Level 7 Rs 17,500; Level 8 Rs 15,000; "
       "Level 9 Rs 9,000; Level 10 Rs 50,000. It comes out of that level's budget permanently (the "
       "top bar shows 'demo -...'), so it can matter when you aim for a tight budget.",
       "প্রতিটি লেভেলে ডেমোর দাম কত?",
       "লেভেলের মূল বাজেটের 0.5%, একবারই: লেভেল 1 Rs 1,250; লেভেল 2 Rs 6,000; লেভেল 3 Rs 47,500; লেভেল 4 Rs 20,000; "
       "লেভেল 5 Rs 15,000; লেভেল 6 Rs 25,000; লেভেল 7 Rs 17,500; লেভেল 8 Rs 15,000; লেভেল 9 Rs 9,000; লেভেল 10 "
       "Rs 50,000। এটি ওই লেভেলের বাজেট থেকে চিরতরে কাটা যায় (উপরের বারে 'ডেমো -...' দেখায়), তাই টানাটানির বাজেটে "
       "গুরুত্বপূর্ণ হতে পারে।"),
    qa("What is the over-engineering penalty?",
       "If a structure finishes with a factor of safety above 4, the results subtract 5% of the "
       "budget for every point above 4, up to 30%. Example: FS 6 in Level 7 (budget Rs 35 L) costs "
       "2 x 5% x 35 L = Rs 3.5 L of profit. The game is telling you that strength nobody needs is "
       "money thrown away.",
       "অতিরিক্ত-মজবুতের জরিমানা কী?",
       "কোনো কাঠামো 4-এর বেশি নিরাপত্তা গুণক নিয়ে শেষ হলে ফলাফল থেকে 4-এর উপরের প্রতিটি পয়েন্টে বাজেটের 5% কাটা হয়, "
       "সর্বোচ্চ 30%। উদাহরণ: লেভেল 7-এ (বাজেট Rs 35 L) FS 6 হলে লাভ থেকে 2 x 5% x 35 L = Rs 3.5 L যায়। খেলাটি "
       "বলছে, যে শক্তি কারো দরকার নেই তা ফেলে দেওয়া টাকা।"),
    qa("What does an alternate route cost?",
       "After a failure, the Black Box may offer the level's alternate route (debris ford, cable "
       "winch, cable car...). It costs the level's cost factor (0.4 to 0.8) x your failed build "
       "cost, or x half the par if that is more. It always finishes the level with one star and 30 "
       "EXP - a way forward, never a dead end.",
       "বিকল্প পথের খরচ কত?",
       "ব্যর্থতার পরে ব্ল্যাক বক্স লেভেলের বিকল্প পথ দিতে পারে (ধ্বংসাবশেষের পারাপার, তারের উইঞ্চ, কেবল কার...)। এর "
       "খরচ লেভেলের খরচ-গুণক (0.4 থেকে 0.8) x তোমার ব্যর্থ নকশার খরচ, অথবা তা বেশি হলে x প্যারের অর্ধেক। এটি সবসময় "
       "এক তারা আর 30 EXP দিয়ে লেভেল শেষ করে - এগোনোর পথ, কখনো কানা গলি নয়।"),
    # --- tolls, loans and the business plan ------------------------------------------------
    qa("What does each level earn from tolls?",
       "Level 1 bridge toll Rs 10 per vehicle; 2 freight Rs 150 per tonne; 3 bridge toll Rs 60 per "
       "vehicle; 4 freight Rs 120 per tonne; 5 track access Rs 1,500 per train; 6 congestion "
       "charge Rs 2 per car; 7 bridge toll Rs 40 per vehicle; 8 highway toll Rs 50 per vehicle; 9 "
       "freight margin Rs 25 per tonne; 10 maglev fare Rs 200 per passenger. The business plan "
       "turns these into yearly income.",
       "প্রতিটি লেভেল টোল থেকে কত আয় করে?",
       "লেভেল 1 সেতুর টোল প্রতি গাড়ি Rs 10; 2 মাল-ভাড়া প্রতি টন Rs 150; 3 সেতুর টোল প্রতি গাড়ি Rs 60; 4 মাল-ভাড়া প্রতি "
       "টন Rs 120; 5 লাইন ব্যবহার প্রতি ট্রেন Rs 1,500; 6 যানজট-মাশুল প্রতি গাড়ি Rs 2; 7 সেতুর টোল প্রতি গাড়ি Rs 40; "
       "8 মহাসড়কের টোল প্রতি গাড়ি Rs 50; 9 মাল-মুনাফা প্রতি টন Rs 25; 10 ম্যাগলেভ ভাড়া প্রতি যাত্রী Rs 200। ব্যবসার "
       "পরিকল্পনা এগুলোকে বছরের আয়ে বদলায়।"),
    qa("How big is the first-year income?",
       "At the standard toll the first year earns 45% of the level's budget: Rs 1.13 L in Level 1, "
       "Rs 15.75 L in Level 7, Rs 45 L in Level 10. The number of users per day follows from that "
       "and the toll rate. Traffic then grows 6% every year, so income grows too.",
       "প্রথম বছরের আয় কত বড়?",
       "সাধারণ টোলে প্রথম বছরে লেভেলের বাজেটের 45% আয় হয়: লেভেল 1-এ Rs 1.13 L, লেভেল 7-এ Rs 15.75 L, লেভেল 10-এ "
       "Rs 45 L। প্রতিদিনের ব্যবহারকারীর সংখ্যা এ থেকে আর টোলের হার থেকে আসে। তারপর যান চলাচল প্রতি বছর 6% বাড়ে, "
       "তাই আয়ও বাড়ে।"),
    qa("Should I raise the toll rate?",
       "The toll can be set from 0.5 to 1.5 x the standard rate. Higher tolls keep some users away: "
       "users = base x (1 / factor)^0.5. Income = users x toll, so it grows only with the square "
       "root of the factor: 1.5 x the toll loses about 18% of users but brings about 22% more "
       "income. That extra income can be what gets a loan approved.",
       "টোলের হার কি বাড়াব?",
       "টোল সাধারণ হারের 0.5 থেকে 1.5 গুণ পর্যন্ত রাখা যায়। বেশি টোলে কিছু ব্যবহারকারী দূরে থাকে: ব্যবহারকারী = মূল x "
       "(1 / গুণক)^0.5। আয় = ব্যবহারকারী x টোল, তাই এটি গুণকের বর্গমূল অনুপাতে বাড়ে: 1.5 গুণ টোলে প্রায় 18% "
       "ব্যবহারকারী কমে কিন্তু প্রায় 22% বেশি আয় হয়। এই বাড়তি আয়ই ঋণ মঞ্জুর করাতে পারে।"),
    qa("How is the yearly loan payment calculated?",
       "Equal yearly payments (an annuity): A = P r / (1 - (1 + r)^-n). For the bank loan (r = 2%, "
       "n = 10 years) every Rs 1 L borrowed costs about Rs 11,133 a year. For the government loan "
       "(r = 0.5%, n = 15 years) only about Rs 6,936 a year. The Finance screen shows the full "
       "year-by-year table.",
       "বছরের ঋণ-কিস্তি কীভাবে হিসাব হয়?",
       "সমান বার্ষিক কিস্তি (অ্যানুইটি): A = P r / (1 - (1 + r)^-n)। ব্যাংক ঋণে (r = 2%, n = 10 বছর) প্রতি Rs 1 L "
       "ধারে বছরে প্রায় Rs 11,133। সরকারি ঋণে (r = 0.5%, n = 15 বছর) বছরে মাত্র প্রায় Rs 6,936। 'অর্থ' পর্দা বছর-বছর "
       "পুরো তালিকা দেখায়।"),
    qa("What is the 1.5 coverage rule (DSCR)?",
       "The debt-service coverage ratio is DSCR = (first-year toll income - upkeep) / yearly loan "
       "payments. The bank lends only if DSCR >= 1.5 - the toll business must earn its loan "
       "payment with a 50% safety margin. If high material spending pushes the loan above that "
       "line, the plan is rejected however safe the structure is.",
       "1.5 কভারেজ নিয়ম (DSCR) কী?",
       "ঋণ-পরিশোধ কভারেজ অনুপাত DSCR = (প্রথম বছরের টোল আয় - রক্ষণাবেক্ষণ) / বছরের ঋণ-কিস্তি। DSCR >= 1.5 হলে তবেই "
       "ব্যাংক ধার দেয় - টোলের ব্যবসাকে 50% নিরাপত্তা-ফাঁকসহ কিস্তি আয় করতে হবে। বেশি উপাদান-খরচে ঋণ এই সীমার উপরে "
       "গেলে কাঠামো যত নিরাপদই হোক, পরিকল্পনা বাতিল হয়।"),
    qa("What are upkeep and traffic growth in the plan?",
       "Upkeep (operation and maintenance) is 3% of the build cost every year, so expensive designs "
       "cost more to run for ever. Traffic and income grow 6% a year. The plan runs 20 years and "
       "shows, each year, income, upkeep, loan payment, interest, what is still owed and your "
       "running cash position.",
       "পরিকল্পনায় রক্ষণাবেক্ষণ আর যান-বৃদ্ধি কী?",
       "রক্ষণাবেক্ষণ (চালানো ও মেরামত) প্রতি বছর নির্মাণ-খরচের 3%, তাই দামি নকশা চিরকাল চালাতে বেশি খরচ। যান চলাচল আর "
       "আয় বছরে 6% বাড়ে। পরিকল্পনা 20 বছর চলে আর প্রতি বছরের আয়, রক্ষণাবেক্ষণ, ঋণ-কিস্তি, সুদ, এখনো কত বাকি আর তোমার "
       "চলতি নগদ অবস্থা দেখায়।"),
    qa("What do 'Investment recovered' and 'Profit after 20 years' mean?",
       "Your own money spent (up to the budget) starts as a minus. Each year's net cash (income - "
       "upkeep - loan payments) is added. 'Investment recovered' is the first year that total "
       "turns positive; 'Profit after 20 years' is where it ends, minus any over-engineering "
       "penalty. A cheap design inside the budget usually recovers in the first year or two.",
       "'বিনিয়োগ ফেরত' আর '20 বছর পরে লাভ' মানে কী?",
       "তোমার খরচ করা নিজের টাকা (বাজেট পর্যন্ত) শুরুতে বিয়োগ হিসেবে থাকে। প্রতি বছরের নিট নগদ (আয় - রক্ষণাবেক্ষণ - "
       "ঋণ-কিস্তি) যোগ হয়। 'বিনিয়োগ ফেরত' হলো যে বছর প্রথম মোট ধনাত্মক হয়; '20 বছর পরে লাভ' হলো শেষে যা দাঁড়ায়, "
       "অতিরিক্ত-মজবুতের জরিমানা বাদে। বাজেটের মধ্যে সস্তা নকশা সাধারণত প্রথম এক-দুই বছরেই ফেরত আসে।"),
    qa("Bank loan or government loan?",
       "Take the government subsidised loan first whenever you need a loan: 0.5% over 15 years "
       "against the bank's 2% over 10 years - about 38% lower yearly payments and far less "
       "interest. It covers up to half the level's budget; the bank lends the rest. The plan shows "
       "the interest you saved. It never changes the par, so loans help you finish, not to earn "
       "the par star.",
       "ব্যাংক ঋণ নাকি সরকারি ঋণ?",
       "ঋণ লাগলেই আগে সরকারি ভর্তুকির ঋণ নাও: বছরে 0.5%, 15 বছর, যেখানে ব্যাংকের 2%, 10 বছর - প্রায় 38% কম বার্ষিক "
       "কিস্তি আর অনেক কম সুদ। এটি লেভেলের বাজেটের অর্ধেক পর্যন্ত দেয়; বাকিটা ব্যাংক দেয়। পরিকল্পনা দেখায় কত সুদ "
       "বাঁচল। এটি কখনো প্যার বদলায় না, তাই ঋণ শেষ করতে সাহায্য করে, প্যারের তারা পেতে নয়।"),
    qa("How big a loan will the bank approve?",
       "The largest bank loan with DSCR exactly 1.5 is P = (income - 3% of the budget) / (1.5 x "
       "payment per rupee + 3%). At the standard toll that is about Rs 5.3 L in Level 1, Rs 74.6 L "
       "in Level 7 and Rs 2.13 Cr in Level 10. A higher toll or a government loan for the first "
       "part raises the limit.",
       "ব্যাংক কত বড় ঋণ মঞ্জুর করবে?",
       "DSCR ঠিক 1.5 রেখে সবচেয়ে বড় ব্যাংক ঋণ P = (আয় - বাজেটের 3%) / (1.5 x প্রতি টাকার কিস্তি + 3%)। সাধারণ টোলে তা "
       "লেভেল 1-এ প্রায় Rs 5.3 L, লেভেল 7-এ Rs 74.6 L আর লেভেল 10-এ Rs 2.13 Cr। বেশি টোল বা প্রথম অংশে সরকারি ঋণ সীমা "
       "বাড়ায়।"),
    qa("Can you show a loan example?",
       "Level 1, a design costing Rs 3.00 L with a Rs 2.50 L budget: the shortfall is Rs 50,000. "
       "From the bank that is about Rs 5,566 a year for 10 years; first-year income is Rs 1.13 L "
       "and upkeep Rs 9,000, so DSCR is about 18.6 - easily approved. With the government loan the "
       "payment drops to about Rs 3,468 a year. Either way the investment is recovered in year 3 - "
       "but the cost is over par, so at most one star.",
       "একটি ঋণের উদাহরণ দেখাবে?",
       "লেভেল 1, Rs 2.50 L বাজেটে Rs 3.00 L খরচের নকশা: ঘাটতি Rs 50,000। ব্যাংক থেকে তা 10 বছর ধরে বছরে প্রায় Rs 5,566; "
       "প্রথম বছরের আয় Rs 1.13 L আর রক্ষণাবেক্ষণ Rs 9,000, তাই DSCR প্রায় 18.6 - সহজেই মঞ্জুর। সরকারি ঋণে কিস্তি নেমে "
       "বছরে প্রায় Rs 3,468। যেভাবেই হোক বিনিয়োগ ফেরত আসে 3য় বছরে - কিন্তু খরচ প্যারের উপরে, তাই বড়জোর এক তারা।"),
    qa("When does the loan screen appear, and can I see it without a loan?",
       "The Business Plan opens by itself when you start a design that costs more than the "
       "budget; you choose the loans and the toll there, then accept or go back and cut costs. The "
       "Finance button at the top shows the same plan at any time, even inside the budget, so you "
       "can check the payback before you build.",
       "ঋণের পর্দা কখন আসে, আর ঋণ ছাড়া কি দেখা যায়?",
       "বাজেটের বেশি খরচের নকশা শুরু করলে ব্যবসার পরিকল্পনা নিজেই খোলে; সেখানে ঋণ আর টোল বেছে নাও, তারপর মেনে নাও বা "
       "ফিরে গিয়ে খরচ কমাও। উপরের 'অর্থ' বোতাম বাজেটের মধ্যেও যেকোনো সময় একই পরিকল্পনা দেখায়, তাই বানানোর আগেই "
       "খরচ ফেরতের হিসাব দেখে নিতে পারো।"),
    # --- per-level optimisation: bridges ---------------------------------------------------
    qa("What do the bridge demos cost, and are they three-star designs?",
       "Played through the real simulation: Level 1 demo Rs 61,960, FS 1.79, 3 stars. Level 7 demo "
       "Rs 21.4 L (par Rs 22 L), FS 1.83, 3 stars. Level 8 demo Rs 13.4 L (par Rs 15 L), FS 2.11, "
       "3 stars. Level 10 demo Rs 73.4 L, FS 2.90 - over the Rs 70 L par, so only 2 stars. Beat "
       "them with your own designs.",
       "সেতুর প্রদর্শনীগুলোর খরচ কত, আর এগুলো কি তিন-তারার নকশা?",
       "আসল সিমুলেশনে চালিয়ে: লেভেল 1-এর প্রদর্শনী Rs 61,960, FS 1.79, 3 তারা। লেভেল 7 Rs 21.4 L (প্যার Rs 22 L), "
       "FS 1.83, 3 তারা। লেভেল 8 Rs 13.4 L (প্যার Rs 15 L), FS 2.11, 3 তারা। লেভেল 10 Rs 73.4 L, FS 2.90 - Rs 70 L "
       "প্যারের উপরে, তাই মাত্র 2 তারা। নিজের নকশা দিয়ে এগুলোকে হারাও।"),
    qa("How do I get the Level 10 demo design under par?",
       "Its extras are big: the maglev guideway costs Rs 50,000 per metre x 64 m = Rs 32 L whatever "
       "you build, and the grid costs Rs 4 L per MW. The demo buys 4 MW. With the same bridge and "
       "only 3 MW the pod still crosses in time, the cost drops to Rs 69.4 L - under the Rs 70 L "
       "par - and the result is 3 stars. Do not pay for power you do not use.",
       "লেভেল 10-এর প্রদর্শনী-নকশা প্যারের নিচে কীভাবে আনব?",
       "এর বাড়তি খরচ বড়: যা-ই বানাও, ম্যাগলেভের পথের খরচ প্রতি মিটারে Rs 50,000 x 64 m = Rs 32 L, আর গ্রিডের খরচ প্রতি "
       "MW-এ Rs 4 L। প্রদর্শনী 4 MW কেনে। একই সেতু আর মাত্র 3 MW-তে পড তবুও সময়মতো পার হয়, খরচ নেমে Rs 69.4 L - "
       "Rs 70 L প্যারের নিচে - আর ফল 3 তারা। যে শক্তি ব্যবহার করো না তার দাম দিয়ো না।"),
    qa("How do I keep Level 7 under its Rs 22 L par?",
       "Budget Rs 35 L, par Rs 22 L. The buses and 12 kN/m road make it heavy, so steel is right, "
       "but every extra panel adds labour and steel. One wind fix is usually enough - fairings "
       "(Rs 2.5 L) work at every wind speed. The demo (deep steel Warren, 8 panels, hollow box XL, "
       "fairings) is Rs 21.4 L: right at the edge, so shrink green members where you can.",
       "লেভেল 7-কে Rs 22 L প্যারের নিচে কীভাবে রাখব?",
       "বাজেট Rs 35 L, প্যার Rs 22 L। বাস আর 12 kN/m রাস্তা একে ভারী করে, তাই ইস্পাতই ঠিক, কিন্তু প্রতিটি বাড়তি ঘর শ্রম "
       "আর ইস্পাত যোগ করে। সাধারণত একটি বাতাস-প্রতিকারই যথেষ্ট - ফেয়ারিং (Rs 2.5 L) সব বাতাসের গতিতে কাজ করে। প্রদর্শনী "
       "(গভীর ইস্পাতের ওয়ারেন, 8 ঘর, ফাঁপা বাক্স XL, ফেয়ারিং) Rs 21.4 L: একেবারে সীমায়, তাই যেখানে পারো সবুজ সদস্য "
       "ছোট করো।"),
    qa("How do I keep Level 8 under its Rs 15 L par?",
       "Budget Rs 30 L, par Rs 15 L. Isolation (Rs 3 L) plus flexible joints (Rs 1.5 L) cut the "
       "earthquake force five times, so the columns and braces can be slim. The demo - steel "
       "columns every 4 m, one diagonal per bay, isolation and joints - costs Rs 13.4 L with FS "
       "2.11. Heavy X-braced piers without isolation need far more steel.",
       "লেভেল 8-কে Rs 15 L প্যারের নিচে কীভাবে রাখব?",
       "বাজেট Rs 30 L, প্যার Rs 15 L। আইসোলেশন (Rs 3 L) আর নমনীয় জোড় (Rs 1.5 L) ভূমিকম্পের বল পাঁচ গুণ কমায়, তাই "
       "স্তম্ভ আর ঠেকনা সরু হতে পারে। প্রদর্শনী - প্রতি 4 m-এ ইস্পাতের স্তম্ভ, প্রতি খোপে একটি কর্ণ, আইসোলেশন আর জোড় - "
       "খরচ Rs 13.4 L, FS 2.11। আইসোলেশন ছাড়া ভারী X-ঠেকনা স্তম্ভে অনেক বেশি ইস্পাত লাগে।"),
    # --- rail levels ---------------------------------------------------------------------
    qa("Where does the money go in Levels 2 and 4?",
       "Track (Rs 3,000 per metre), earthworks (cuttings and embankments), the locomotive (Rs 1.5 L "
       "to Rs 18 L) and wagon hire (Rs 20,000 or Rs 50,000 each). Level 2: budget Rs 12 L, par "
       "Rs 8 L. Level 4: budget Rs 40 L, par Rs 30 L. The cheapest engine whose grip copes with "
       "your steepest grade, plus only the earthworks you really need, is the winning recipe.",
       "লেভেল 2 আর 4-এ টাকা কোথায় যায়?",
       "লাইন (প্রতি মিটারে Rs 3,000), মাটির কাজ (কাটা আর বাঁধ), ইঞ্জিন (Rs 1.5 L থেকে Rs 18 L) আর ওয়াগন ভাড়া (প্রতিটি "
       "Rs 20,000 বা Rs 50,000)। লেভেল 2: বাজেট Rs 12 L, প্যার Rs 8 L। লেভেল 4: বাজেট Rs 40 L, প্যার Rs 30 L। জেতার "
       "রেসিপি: যে সবচেয়ে সস্তা ইঞ্জিনের আঁকড়ে ধরা তোমার সবচেয়ে খাড়া ঢাল সামলায়, আর শুধু সত্যিই দরকারি মাটির কাজ।"),
    qa("Mainline diesel or double-header in Level 4?",
       "The double-header has twice the power and grip but costs Rs 18 L against Rs 10 L - and the "
       "par is Rs 30 L. A single mainline diesel with 5 wagons (300 t per trip, two trips) "
       "handles the pass if the grades are sensible. Spend the saved money on smoothing the worst "
       "grade, not on a second engine.",
       "লেভেল 4-এ মেইনলাইন ডিজেল নাকি জোড়া ইঞ্জিন?",
       "জোড়া ইঞ্জিনের দ্বিগুণ শক্তি আর আঁকড়ে ধরা, কিন্তু দাম Rs 18 L, যেখানে মেইনলাইন Rs 10 L - আর প্যার Rs 30 L। ঢাল "
       "যুক্তিসঙ্গত হলে 5 ওয়াগনসহ একটি মেইনলাইন ডিজেল (প্রতি যাত্রায় 300 t, দুই যাত্রা) গিরিপথ সামলায়। বাঁচানো টাকা "
       "দ্বিতীয় ইঞ্জিনে নয়, সবচেয়ে খারাপ ঢাল সমান করতে খরচ করো।"),
    # --- Level 5 signals -------------------------------------------------------------------
    qa("How is Level 5 priced?",
       "Cost = signal price x (signals you place + the 2 fixed ones) + Rs 50,000 for every term in "
       "your interlocking logic. A 3-aspect signal is Rs 3 L, a 4-aspect one Rs 4.5 L. Budget "
       "Rs 30 L, par Rs 15 L. The demo (one extra signal 400 m out on each side, 8 logic terms) "
       "costs 4 x Rs 3 L + 8 x Rs 0.5 L = Rs 16 L - just over par.",
       "লেভেল 5-এর দাম কীভাবে হয়?",
       "খরচ = সিগন্যালের দাম x (তোমার বসানো সিগন্যাল + 2টি স্থির) + তোমার ইন্টারলকিং লজিকের প্রতিটি পদে Rs 50,000। "
       "3-অ্যাসপেক্ট সিগন্যাল Rs 3 L, 4-অ্যাসপেক্ট Rs 4.5 L। বাজেট Rs 30 L, প্যার Rs 15 L। প্রদর্শনী (প্রতিটি দিকে 400 m "
       "দূরে একটি বাড়তি সিগন্যাল, 8টি লজিক-পদ) খরচ 4 x Rs 3 L + 8 x Rs 0.5 L = Rs 16 L - প্যারের সামান্য উপরে।"),
    qa("What is the cheapest three-star plan for Level 5?",
       "Fix the three logic bugs and place no extra signals at all. Tested in the real simulation: "
       "11 trains delivered, every cargo train to the harbor, 0 SPADs and about 764 train-seconds "
       "of waiting (bonus needs 1000 or less), for 2 x Rs 3 L + 8 x Rs 0.5 L = Rs 10 L. Adding the "
       "400 m signals raises the waiting to about 1095 train-seconds and loses the bonus.",
       "লেভেল 5-এ সবচেয়ে সস্তা তিন-তারার পরিকল্পনা কী?",
       "লজিকের তিনটি ভুল ঠিক করো আর কোনো বাড়তি সিগন্যাল বসিয়ো না। আসল সিমুলেশনে পরীক্ষিত: 11টি ট্রেন পৌঁছায়, প্রতিটি "
       "মালগাড়ি বন্দরে, 0 SPAD আর প্রায় 764 ট্রেন-সেকেন্ড অপেক্ষা (বোনাসে 1000 বা কম লাগে), খরচ 2 x Rs 3 L + 8 x "
       "Rs 0.5 L = Rs 10 L। 400 m-এর সিগন্যাল যোগ করলে অপেক্ষা প্রায় 1095 ট্রেন-সেকেন্ডে ওঠে আর বোনাস হারায়।"),
    qa("What are the three bugs in the starter interlocking?",
       "1) PERMIT_EB = APPR_EB AND NOT BRIDGE_OCC is missing AND NOT PERMIT_WB (and the same for "
       "PERMIT_WB) - both directions can be given the single-track bridge at once: head-on danger. "
       "2) SWITCH_HARBOR follows CARGO_APPR_JE, so the switch can move early, under the train ahead "
       "- use CARGO_AT_JE. 3) BARRIER_DOWN is empty, so the crossing barrier never falls - use "
       "XING_APPR.",
       "শুরুর ইন্টারলকিংয়ে তিনটি ভুল কী?",
       "1) PERMIT_EB = APPR_EB AND NOT BRIDGE_OCC-এ AND NOT PERMIT_WB নেই (PERMIT_WB-তেও একই) - একসঙ্গে দুই দিককেই "
       "এক-লাইনের সেতু দেওয়া যায়: মুখোমুখি বিপদ। 2) SWITCH_HARBOR চলে CARGO_APPR_JE মেনে, তাই পয়েন্ট আগেভাগে, সামনের "
       "ট্রেনের নিচেই সরে যেতে পারে - CARGO_AT_JE ব্যবহার করো। 3) BARRIER_DOWN ফাঁকা, তাই লেভেল-ক্রসিংয়ের গেট কখনো "
       "নামে না - XING_APPR ব্যবহার করো।"),
    qa("How do I edit the interlocking rows?",
       "Each output = [NOT] A AND/OR [NOT] B AND/OR [NOT] C, and the rows are worked out top to "
       "bottom. Click an input box to cycle through the inputs (or '-' for none), click NOT to "
       "invert that input, and click AND/OR to switch the joining word. 'Starter logic' puts back "
       "the original rows with their bugs. The 'Live' column shows each value during a run.",
       "ইন্টারলকিংয়ের সারিগুলো কীভাবে বদলাব?",
       "প্রতিটি আউটপুট = [NOT] A AND/OR [NOT] B AND/OR [NOT] C, আর সারিগুলো উপর থেকে নিচে হিসাব হয়। ইনপুটের ঘরে ক্লিক "
       "করে ইনপুটগুলো একে একে বদলাও (বা কিছু না চাইলে '-'), সেই ইনপুট উল্টাতে NOT-এ ক্লিক করো, আর যোগের শব্দ বদলাতে "
       "AND/OR-এ ক্লিক করো। 'শুরুর লজিক' ভুলসহ আসল সারিগুলো ফিরিয়ে আনে। 'সরাসরি' কলাম চালানোর সময় প্রতিটি মান দেখায়।"),
    qa("What do the interlocking inputs mean?",
       "BRIDGE_OCC: a train is on the single-track bridge. APPR_EB / APPR_WB: a train is "
       "approaching from the west (eastbound) or the east (westbound). PERMIT_EB / PERMIT_WB: the "
       "bridge is currently given to that direction. XING_APPR: a train is approaching the level "
       "crossing. CARGO_APPR_JE: a cargo train is approaching the harbor junction; CARGO_AT_JE: one "
       "is at it; JE_OCC: the junction track is occupied. TRUE: always on.",
       "ইন্টারলকিংয়ের ইনপুটগুলোর মানে কী?",
       "BRIDGE_OCC: এক-লাইনের সেতুতে একটি ট্রেন আছে। APPR_EB / APPR_WB: পশ্চিম থেকে (পূর্বমুখী) বা পূর্ব থেকে (পশ্চিমমুখী) "
       "একটি ট্রেন আসছে। PERMIT_EB / PERMIT_WB: সেতু এখন ওই দিককে দেওয়া। XING_APPR: একটি ট্রেন লেভেল-ক্রসিংয়ের দিকে "
       "আসছে। CARGO_APPR_JE: একটি মালগাড়ি বন্দরের জংশনের দিকে আসছে; CARGO_AT_JE: জংশনে আছে; JE_OCC: জংশনের লাইন দখল। "
       "TRUE: সবসময় চালু।"),
    qa("Why did a signal at 350 m cause a crash when 400 m was fine?",
       "Each placed signal splits the approach into blocks. A signal at 350 m makes the block up to "
       "the bridge entrance too short for a train to stop in after seeing YELLOW, so a following "
       "train passed a red (a SPAD) and ran into the one ahead. At 400 m and beyond the blocks are "
       "long enough. Remember: about 354 m for passenger trains and 330 m for cargo, plus margin.",
       "350 m-এ সিগন্যাল সংঘর্ষ ঘটাল, অথচ 400 m ঠিক ছিল কেন?",
       "প্রতিটি বসানো সিগন্যাল আসার পথকে ব্লকে ভাগ করে। 350 m-এর সিগন্যাল সেতুর প্রবেশ পর্যন্ত ব্লককে এত ছোট করে যে হলুদ "
       "দেখার পর ট্রেন থামতে পারে না, তাই পেছনের ট্রেন লাল পেরিয়ে (SPAD) সামনেরটিকে ধাক্কা দিল। 400 m বা তার বেশিতে ব্লক "
       "যথেষ্ট লম্বা। মনে রেখো: যাত্রীবাহী ট্রেনের প্রায় 354 m আর মালগাড়ির 330 m, সঙ্গে কিছু বাড়তি।"),
    qa("What is the Level 5 bonus star, and why can more signals hurt it?",
       "Zero SPADs and total waiting (idle + queued) of 1000 train-seconds or less in the 12 "
       "minutes. More signals mean more places where a train may be held at a red before the "
       "bridge; with this single track the bridge itself is the bottleneck, so extra blocks add "
       "waiting without adding capacity. Fewer, well-placed signals are better here.",
       "লেভেল 5-এর বোনাস তারা কী, আর বেশি সিগন্যাল কেন ক্ষতি করতে পারে?",
       "12 মিনিটে শূন্য SPAD আর মোট অপেক্ষা (দাঁড়ানো + লাইনে থাকা) 1000 ট্রেন-সেকেন্ড বা কম। বেশি সিগন্যাল মানে সেতুর "
       "আগে ট্রেনকে লালে আটকে রাখার বেশি জায়গা; এই এক-লাইনে সেতুটাই বাধা, তাই বাড়তি ব্লক ক্ষমতা না বাড়িয়ে অপেক্ষা "
       "বাড়ায়। এখানে কম কিন্তু ঠিক জায়গায় বসানো সিগন্যালই ভালো।"),
    # --- Level 6 traffic -------------------------------------------------------------------
    qa("What is the fundamental diagram, q = k v?",
       "Flow q (cars per hour) = density k (cars per km) x speed v. With the Greenshields model "
       "v = v_max (1 - k / k_jam), flow rises with density until k_crit = k_jam / 2, where it "
       "peaks at q_max = v_max k_jam / 4. Push more cars in than that and speed collapses, flow "
       "falls and a jam is born. The Level 6 chart plots every detector reading live.",
       "মৌলিক চিত্র, q = k v কী?",
       "প্রবাহ q (প্রতি ঘণ্টায় গাড়ি) = ঘনত্ব k (প্রতি km-এ গাড়ি) x গতি v। গ্রিনশিল্ডস মডেলে v = v_max (1 - k / k_jam), "
       "ঘনত্ব বাড়লে প্রবাহ বাড়ে k_crit = k_jam / 2 পর্যন্ত, যেখানে তা চূড়ায় q_max = v_max k_jam / 4। এর বেশি গাড়ি "
       "ঢোকালে গতি ভেঙে পড়ে, প্রবাহ কমে আর যানজট জন্মায়। লেভেল 6-এর চার্ট প্রতিটি ডিটেক্টরের পাঠ সরাসরি আঁকে।"),
    qa("Why do traffic jams travel backwards?",
       "Where a fast, thin stream meets a slow, dense queue, the boundary moves at "
       "w = (q2 - q1) / (k2 - k1). Because the queue is denser but carries less flow, w is "
       "negative: the back of the jam creeps upstream even though every car moves forward. Watch "
       "the red bands crawl backwards in the speed-coloured heat map.",
       "যানজট পেছনের দিকে চলে কেন?",
       "যেখানে দ্রুত, পাতলা স্রোত ধীর, ঘন লাইনের সঙ্গে মেলে, সীমানা চলে w = (q2 - q1) / (k2 - k1) গতিতে। লাইন ঘন কিন্তু "
       "কম প্রবাহ বয় বলে w ঋণাত্মক: প্রতিটি গাড়ি সামনে এগোলেও যানজটের পেছনটা উজানের দিকে হামাগুড়ি দেয়। গতি-রঙা তাপ-মানচিত্রে "
       "লাল ফিতেগুলো পেছনে সরতে দেখো।"),
    qa("How do I tune the traffic signals in Level 6?",
       "Each road passes about s x g / C cars per hour: s = 1800 cars per hour of green, g the "
       "green time, C the cycle; every phase change loses 5 s. At peak the main road brings 1100 "
       "cars per hour and the market street 400. The default 60 s cycle with a 0.5 split gives "
       "the main road only about 750 - gridlock. A 90 s cycle with 0.7 to the main road passes "
       "(trips 1.62 x free flow), but idling is about 5800 car-seconds, so no bonus.",
       "লেভেল 6-এ ট্রাফিক সিগন্যাল কীভাবে টিউন করব?",
       "প্রতিটি রাস্তা ঘণ্টায় প্রায় s x g / C গাড়ি পার করে: s = প্রতি ঘণ্টা সবুজে 1800 গাড়ি, g সবুজের সময়, C চক্র; প্রতিটি "
       "পর্যায় বদলে 5 s নষ্ট হয়। ভিড়ের চূড়ায় প্রধান সড়কে ঘণ্টায় 1100 আর বাজার রাস্তায় 400 গাড়ি আসে। শুরুর 60 s চক্র আর "
       "0.5 ভাগে প্রধান সড়ক মাত্র প্রায় 750 পায় - যানজট। 90 s চক্র আর প্রধান সড়কে 0.7 পাস করে (যাত্রা ফাঁকা রাস্তার "
       "1.62 গুণ), কিন্তু প্রায় 5800 গাড়ি-সেকেন্ড দাঁড়ানো, তাই বোনাস নেই।"),
    qa("Roundabout or overpass in Level 6?",
       "Tested in the real simulation. Roundabout (Rs 12 L): no gridlock, main-road trips 1.56 x "
       "free flow, idling about 3700 car-seconds - under the 4000 bonus limit and under the Rs 15 L "
       "par: three stars. Overpass (Rs 45 L): trips 1.05 x free flow and zero idling, but far over "
       "par. Signals are cheapest (Rs 4 L) but hard to get under the idling limit.",
       "লেভেল 6-এ গোলচত্বর নাকি উড়ালসেতু?",
       "আসল সিমুলেশনে পরীক্ষিত। গোলচত্বর (Rs 12 L): যানজট নেই, প্রধান সড়কের যাত্রা ফাঁকা রাস্তার 1.56 গুণ, প্রায় 3700 "
       "গাড়ি-সেকেন্ড দাঁড়ানো - 4000 বোনাস-সীমা আর Rs 15 L প্যার দুটোরই নিচে: তিন তারা। উড়ালসেতু (Rs 45 L): যাত্রা ফাঁকা "
       "রাস্তার 1.05 গুণ আর শূন্য দাঁড়ানো, কিন্তু প্যারের অনেক উপরে। সিগন্যাল সবচেয়ে সস্তা (Rs 4 L), তবে দাঁড়ানোর সীমার "
       "নিচে আনা কঠিন।"),
    qa("How do cars follow each other in Level 6 (IDM)?",
       "Each car uses the Intelligent Driver Model: it accelerates towards the speed limit but "
       "keeps a safe time gap of T = 1.2 s to the car ahead and brakes smoothly when the gap "
       "shrinks. At the roundabout cars merge only into gaps of at least 2 s and slow to 8 m/s. "
       "Small hesitations ripple back through the queue - which is how stop-and-go waves form.",
       "লেভেল 6-এ গাড়িগুলো একে অপরকে কীভাবে অনুসরণ করে (IDM)?",
       "প্রতিটি গাড়ি ইন্টেলিজেন্ট ড্রাইভার মডেল ব্যবহার করে: গতিসীমার দিকে গতি বাড়ায়, কিন্তু সামনের গাড়ি থেকে T = 1.2 s "
       "নিরাপদ সময়-ফাঁক রাখে আর ফাঁক কমলে মসৃণভাবে ব্রেক করে। গোলচত্বরে গাড়ি শুধু অন্তত 2 s ফাঁকে মেশে আর 8 m/s-এ ধীর হয়। "
       "ছোট দ্বিধাগুলো লাইন ধরে পেছনে ছড়ায় - এভাবেই থামা-চলার ঢেউ তৈরি হয়।"),
    # --- Level 9 logistics -----------------------------------------------------------------
    qa("What are the three transport modes in Level 9?",
       "Road: 25 t trucks at Rs 9,000 a day, 80 km, up to 70 km/h - but more trucks crowd the road "
       "and slow each other (Greenshields). Rail: trains of 60 t wagons at Rs 1.2 L per train per "
       "day, 95 km over a 1.2% grade, Rs 60 per tonne to transfer and 3 h at the terminals. Barge: "
       "1000 t each at Rs 60,000 a day, 120 km on the river at 3 m/s plus a 1 m/s current, Rs 100 "
       "per tonne to transfer and 6 h at the terminals. Diesel costs Rs 100 per litre.",
       "লেভেল 9-এ তিনটি পরিবহন-পথ কী?",
       "সড়ক: দিনে Rs 9,000-এ 25 t-এর ট্রাক, 80 km, সর্বোচ্চ 70 km/h - কিন্তু বেশি ট্রাক রাস্তা ভরিয়ে একে অপরকে ধীর করে "
       "(গ্রিনশিল্ডস)। রেল: প্রতি ট্রেন দিনে Rs 1.2 L-এ 60 t-এর ওয়াগনের ট্রেন, 1.2% ঢালে 95 km, প্রতি টন স্থানান্তরে Rs 60 "
       "আর টার্মিনালে 3 ঘণ্টা। বার্জ: প্রতিটি 1000 t, দিনে Rs 60,000, নদীতে 120 km, 3 m/s আর 1 m/s স্রোত, প্রতি টন "
       "স্থানান্তরে Rs 100 আর টার্মিনালে 6 ঘণ্টা। ডিজেল প্রতি লিটার Rs 100।"),
    qa("How is the Level 9 safety index worked out?",
       "Risk grows with every vehicle trip and every kilometre: each round trip adds a small risk "
       "per km for its mode. Hundreds of truck trips add up fast, while a few trains or barges add "
       "little. All 6000 t by 60 trucks scores about 84.6 - below the 95 needed for the bonus - "
       "while rail and barge plans score about 99.6.",
       "লেভেল 9-এর নিরাপত্তা সূচক কীভাবে হিসাব হয়?",
       "প্রতিটি যাত্রা আর প্রতিটি কিলোমিটারে ঝুঁকি বাড়ে: প্রতিটি আসা-যাওয়া তার পথের জন্য প্রতি km-এ সামান্য ঝুঁকি যোগ করে। "
       "শত শত ট্রাক-যাত্রা দ্রুত জমে যায়, আর কয়েকটি ট্রেন বা বার্জ সামান্যই যোগ করে। 60টি ট্রাকে পুরো 6000 t-এ সূচক প্রায় "
       "84.6 - বোনাসের 95-এর নিচে - আর রেল ও বার্জের পরিকল্পনায় প্রায় 99.6।"),
    qa("Which Level 9 plans actually work?",
       "Tested with the game's own model (budget Rs 18 L, par Rs 13 L, deadline 24 h): 5000 t by "
       "one 30-wagon train + 1000 t by one barge: 22.9 h, Rs 11.2 L, safety 99.6 - three stars. "
       "All by rail with 2 trains: 13.7 h, Rs 12.3 L - three stars. All by rail with 1 train: 32 h "
       "- too slow. All by 6 barges: 14.3 h, Rs 13.6 L - over par. All by 60 trucks: 13.2 h, "
       "Rs 16.9 L, safety 84.6 - one star.",
       "লেভেল 9-এর কোন পরিকল্পনাগুলো সত্যিই কাজ করে?",
       "খেলার নিজের মডেলে পরীক্ষিত (বাজেট Rs 18 L, প্যার Rs 13 L, সময়সীমা 24 ঘণ্টা): 30 ওয়াগনের একটি ট্রেনে 5000 t + একটি "
       "বার্জে 1000 t: 22.9 ঘণ্টা, Rs 11.2 L, নিরাপত্তা 99.6 - তিন তারা। 2টি ট্রেনে সবটা রেলে: 13.7 ঘণ্টা, Rs 12.3 L - তিন "
       "তারা। 1টি ট্রেনে সবটা রেলে: 32 ঘণ্টা - খুব ধীর। 6টি বার্জে সবটা: 14.3 ঘণ্টা, Rs 13.6 L - প্যারের উপরে। 60টি ট্রাকে "
       "সবটা: 13.2 ঘণ্টা, Rs 16.9 L, নিরাপত্তা 84.6 - এক তারা।"),
    qa("Why can one freight locomotive pull only about 30 wagons?",
       "The loco weighs 130 t, so its grip is 0.30 x 130 t x g = about 383 kN. Each loaded wagon "
       "weighs 82 t (60 t ore + 22 t wagon). With 30 wagons the 2590 t train needs about 356 kN on "
       "the 1.2% grade - just inside. At 33 wagons it needs about 389 kN and the wheels slip. For "
       "more tonnes per hour, add a second train, not more wagons.",
       "একটি মালবাহী ইঞ্জিন মাত্র প্রায় 30টি ওয়াগন টানতে পারে কেন?",
       "ইঞ্জিনের ওজন 130 t, তাই তার আঁকড়ে ধরা 0.30 x 130 t x g = প্রায় 383 kN। প্রতিটি ভরা ওয়াগনের ওজন 82 t (60 t আকরিক + "
       "22 t ওয়াগন)। 30 ওয়াগনে 2590 t-এর ট্রেনের 1.2% ঢালে লাগে প্রায় 356 kN - সীমার ঠিক ভেতরে। 33 ওয়াগনে লাগে প্রায় "
       "389 kN আর চাকা পিছলায়। ঘণ্টায় বেশি টনের জন্য বেশি ওয়াগন নয়, দ্বিতীয় ট্রেন যোগ করো।"),
    qa("What is the Pareto frontier in Level 9?",
       "Every plan has a cost, a time and a safety score. A plan is on the Pareto frontier if no "
       "other plan beats it on all three at once. Plans off the frontier are simply wasteful - "
       "something else is cheaper, faster and safer. 'Optimizer: show all plans' plots every "
       "feasible plan so you can choose your favourite trade-off from the frontier.",
       "লেভেল 9-এ প্যারেটো সীমান্ত কী?",
       "প্রতিটি পরিকল্পনার একটি খরচ, একটি সময় আর একটি নিরাপত্তা-মান আছে। কোনো পরিকল্পনা প্যারেটো সীমান্তে থাকে যদি অন্য "
       "কোনো পরিকল্পনা তিনটিতেই একসঙ্গে তাকে না হারায়। সীমান্তের বাইরের পরিকল্পনা স্রেফ অপচয় - অন্য কিছু আরও সস্তা, দ্রুত "
       "আর নিরাপদ। 'অপ্টিমাইজার: সব পরিকল্পনা দেখাও' প্রতিটি সম্ভব পরিকল্পনা আঁকে, যাতে সীমান্ত থেকে তোমার পছন্দের "
       "আপস বেছে নিতে পারো।"),
    qa("What is the Level 9 toll formula?",
       "Toll = (tonnes x km) / (hours x litres of fuel), times a payout scale. It rewards moving "
       "lots of cargo far, quickly and with little fuel. Trucks burn about 0.35 litres per km "
       "loaded; rail and barge only about 0.004 litres per tonne-km - which is why they earn a "
       "better payout and a better business plan.",
       "লেভেল 9-এর টোলের সূত্র কী?",
       "টোল = (টন x km) / (ঘণ্টা x লিটার জ্বালানি), গুণ একটি পরিশোধ-মাপ। এটি অনেক মাল দূরে, দ্রুত আর কম জ্বালানিতে নেওয়াকে "
       "পুরস্কার দেয়। ভরা ট্রাক প্রতি km-এ প্রায় 0.35 লিটার পোড়ায়; রেল আর বার্জ প্রতি টন-km-এ মাত্র প্রায় 0.004 লিটার - "
       "এজন্যই তারা ভালো পরিশোধ আর ভালো ব্যবসার পরিকল্পনা পায়।"),
    # --- general strategy ----------------------------------------------------------------
    qa("What are the budget and par of every level?",
       "Level 1: Rs 2.50 L / Rs 1.00 L. Level 2: Rs 12 L / Rs 8 L. Level 3: Rs 95 L / Rs 76 L. "
       "Level 4: Rs 40 L / Rs 30 L. Level 5: Rs 30 L / Rs 15 L. Level 6: Rs 50 L / Rs 15 L. "
       "Level 7: Rs 35 L / Rs 22 L. Level 8: Rs 30 L / Rs 15 L. Level 9: Rs 18 L / Rs 13 L. "
       "Level 10: Rs 1.00 Cr / Rs 70 L. (L = lakh = 100,000; Cr = crore = 10,000,000.)",
       "প্রতিটি লেভেলের বাজেট আর প্যার কত?",
       "লেভেল 1: Rs 2.50 L / Rs 1.00 L। লেভেল 2: Rs 12 L / Rs 8 L। লেভেল 3: Rs 95 L / Rs 76 L। লেভেল 4: Rs 40 L / "
       "Rs 30 L। লেভেল 5: Rs 30 L / Rs 15 L। লেভেল 6: Rs 50 L / Rs 15 L। লেভেল 7: Rs 35 L / Rs 22 L। লেভেল 8: Rs 30 L / "
       "Rs 15 L। লেভেল 9: Rs 18 L / Rs 13 L। লেভেল 10: Rs 1.00 Cr / Rs 70 L। (L = লাখ = 100,000; Cr = কোটি = "
       "10,000,000।)"),
    qa("What are the 'two paths forward' in every briefing?",
       "Each level can be solved in two styles. 'Low cost, high skill': a lean design that uses "
       "the physics cleverly - it reaches par but needs care. 'High cost, robust': more material, "
       "bigger engines or extra equipment - safer to get through but harder to keep under par. "
       "Try the robust path first if you are stuck, then trim it towards the skilful one.",
       "প্রতিটি নির্দেশনায় 'এগোনোর দুই পথ' কী?",
       "প্রতিটি লেভেল দুই ধরনে সমাধান করা যায়। 'কম খরচ, বেশি দক্ষতা': পদার্থবিজ্ঞান চতুরভাবে ব্যবহার করা একটি হালকা নকশা - "
       "প্যারে পৌঁছায় কিন্তু যত্ন লাগে। 'বেশি খরচ, নিশ্চিত': বেশি উপাদান, বড় ইঞ্জিন বা বাড়তি সরঞ্জাম - পার হওয়া নিরাপদ, কিন্তু "
       "প্যারের নিচে রাখা কঠিন। আটকে গেলে আগে নিশ্চিত পথে চেষ্টা করো, তারপর ছেঁটে দক্ষতার পথের দিকে আনো।"),
    qa("I am stuck on a level. What should I do?",
       "1) Read the Black Box: the failing formula tells you exactly which number to change. "
       "2) Open the calculator on the part that failed. 3) Read this Help's walkthrough for the "
       "level (Start here). 4) Try the robust path first, then trim. 5) If you are still stuck, "
       "the Demo shows a working solution for 0.5% of the budget, and replays are free.",
       "একটি লেভেলে আটকে গেছি। কী করব?",
       "1) ব্ল্যাক বক্স পড়ো: ব্যর্থ সূত্রটি ঠিক বলে দেয় কোন সংখ্যা বদলাতে হবে। 2) যে অংশ ব্যর্থ হয়েছে তার উপর ক্যালকুলেটর "
       "খোলো। 3) এই সাহায্যে লেভেলের পথনির্দেশ পড়ো ('এখান থেকে শুরু')। 4) আগে নিশ্চিত পথে চেষ্টা করো, তারপর ছাঁটো। 5) তবুও "
       "আটকে থাকলে ডেমো বাজেটের 0.5%-এ একটি কার্যকর সমাধান দেখায়, আর আবার দেখা বিনামূল্যে।"),
    qa("Does failing cost me anything?",
       "Very little - failure is part of the design loop. You keep your design, earn 10 EXP for "
       "the Black Box (60 with a correct diagnosis) and 30% of the build cost back as salvage. "
       "Each attempt is also recorded for the Pareto chart. The only things that cost you for "
       "good are a demonstration and taking the alternate route instead of a full solution.",
       "ব্যর্থ হলে কি আমার কিছু খরচ হয়?",
       "খুব সামান্য - ব্যর্থতা নকশার চক্রেরই অংশ। তোমার নকশা থাকে, ব্ল্যাক বক্সে 10 EXP (সঠিক নির্ণয়ে 60) আর নির্মাণ-খরচের "
       "30% উদ্ধার-মূল্য হিসেবে ফেরত পাও। প্রতিটি চেষ্টা প্যারেটো চার্টের জন্যও লেখা থাকে। স্থায়ীভাবে খরচ হয় শুধু প্রদর্শনী, "
       "আর পূর্ণ সমাধানের বদলে বিকল্প পথ নেওয়া।"),
    qa("Can I play in the browser or on a phone?",
       "Yes. The browser version at https://saiqulmodi.github.io/MODIS_BridgeWorks/ is the same "
       "game. Click once to start (browsers need a click before sound); the first load downloads "
       "about 15 MB and takes 10-20 seconds. Use the full-screen button at the bottom right or F11. "
       "On the desktop, run main.py.",
       "ব্রাউজারে বা ফোনে কি খেলা যায়?",
       "হ্যাঁ। https://saiqulmodi.github.io/MODIS_BridgeWorks/-এর ব্রাউজার সংস্করণ একই খেলা। শুরু করতে একবার ক্লিক করো "
       "(শব্দের আগে ব্রাউজার একটি ক্লিক চায়); প্রথমবার প্রায় 15 MB নামে আর 10-20 সেকেন্ড লাগে। নিচে ডানের পূর্ণ-পর্দা বোতাম বা "
       "F11 ব্যবহার করো। ডেস্কটপে main.py চালাও।"),
    qa("What is the one rule a real engineer would give me?",
       "Make it safe, then make it lean. First get a design that works with no red. Then remove "
       "waste until the factor of safety is about 1.5-2 and the cost is under par. Safe and cheap "
       "together is what engineering is - and what the three stars reward.",
       "একজন আসল প্রকৌশলী আমাকে কোন একটি নিয়ম দিতেন?",
       "আগে নিরাপদ করো, তারপর হালকা করো। প্রথমে এমন নকশা বানাও যা কোনো লাল ছাড়াই কাজ করে। তারপর অপচয় সরাও, যতক্ষণ না "
       "নিরাপত্তা গুণক প্রায় 1.5-2 আর খরচ প্যারের নিচে হয়। নিরাপদ আর সস্তা একসঙ্গে - এটাই প্রকৌশল, আর তিনটি তারা এটাকেই "
       "পুরস্কার দেয়।"),
)
