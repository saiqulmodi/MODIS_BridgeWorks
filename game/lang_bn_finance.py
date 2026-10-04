"""বাংলা: bank loan and business plan screens (merged into lang_bn)."""

TOLL_NAMES = {"Bridge toll": "সেতুর টোল", "Freight charge": "মালবাহী মাশুল",
              "Track access fee": "লাইন ব্যবহারের ফি", "Congestion charge": "যানজট মাশুল",
              "Highway toll": "মহাসড়কের টোল", "Freight margin": "মালবাহী লাভ",
              "Maglev fare": "ম্যাগলেভ ভাড়া"}
UNITS = {"vehicle": "গাড়ি", "tonne": "টন", "train": "ট্রেন", "car": "গাড়ি", "passenger": "যাত্রী"}

FINANCE_BN = {
    # BridgeWorks Academy: Civil Grants
    "CIVIL GRANT COVERS IT": "সিভিল অনুদানেই হয়ে যায়", "Civil Grant (Academy)": "সিভিল অনুদান (একাডেমি)",
    "Use grant & build": "অনুদান নাও ও নির্মাণ করো",
    "Academy: 75% salvage": "একাডেমি: 75% উদ্ধার",
    "Answer one BridgeWorks Academy question correctly to recover 75% instead of 30%.":
        "একাডেমির একটি প্রশ্নের সঠিক উত্তর দিলে 30%-এর বদলে 75% ফেরত পাবে।",
    "BridgeWorks Academy (A)": "ব্রিজওয়ার্কস একাডেমি (A)",
    "Donation Camps (D)": "দান-শিবির (D)",
    "Give Civil Grants to causes that build opportunities": "সুযোগ তৈরির কাজে সিভিল অনুদান দান করো",
    "Class 1-12 quizzes in 6 subjects: earn Civil Grants for your bridges":
        "শ্রেণি 1-12-এর 6 বিষয়ের কুইজ: তোমার সেতুর জন্য সিভিল অনুদান অর্জন করো",
    "Finance": "অর্থ", "Business plan: tolls, loan, payback.": "ব্যবসার পরিকল্পনা: টোল, ঋণ, খরচ ফেরত।",
    "BANK LOAN NEEDED": "ব্যাংক ঋণ দরকার", "BUSINESS PLAN": "ব্যবসার পরিকল্পনা",
    "Your budget": "তোমার বাজেট", "Shortfall = loans": "ঘাটতি = ঋণ",
    "Loan: 2% a year for 10 years, equal yearly payments": "ঋণ: বছরে 2% সুদ, 10 বছর, প্রতি বছর সমান কিস্তি",
    "Take loan & build": "ঋণ নাও ও নির্মাণ করো", "Go back and cut costs": "ফিরে গিয়ে খরচ কমাও",
    "Close": "বন্ধ করো",
    "The bank approves: tolls cover the loan with a 50% margin.": "ব্যাংক রাজি: টোলের আয় 50% বাড়তি সহ ঋণের কিস্তি মেটায়।",
    "The bank refuses: tolls would not cover the loan with a 50% margin. Cut the cost, or raise the toll.":
        "ব্যাংক রাজি নয়: টোলের আয় 50% বাড়তি সহ ঋণের কিস্তি মেটাবে না। খরচ কমাও, বা টোল বাড়াও।",
    "Higher tolls earn more per user, but some users stay away (users fall as 1 / sqrt(toll)).":
        "বেশি টোলে প্রতি ব্যবহারকারী থেকে বেশি আয়, কিন্তু কিছু মানুষ আর আসে না (ব্যবহারকারী কমে 1 / sqrt(টোল) হারে)।",
    "Your cash (green) and loan still owed (red), Rs lakh, by year": "তোমার নগদ (সবুজ) আর বাকি ঋণ (লাল), লাখ টাকায়, বছর অনুযায়ী",
    "Year-1 toll income": "প্রথম বছরের টোল আয়", "Investment recovered": "বিনিয়োগ ফেরত",
    "Profit after 20 years": "20 বছর পর লাভ", "not within 20 years": "20 বছরের মধ্যে নয়",
    "Bank loan (2%, 10 yr)": "ব্যাংক ঋণ (2%, 10 বছর)",
    "Govt loan (0.5%, 15 yr)": "সরকারি ঋণ (0.5%, 15 বছর)",
    "Govt subsidised loan: ON (0.5%, 15 yr, up to half the budget)":
        "সরকারি ভর্তুকির ঋণ: চালু (0.5%, 15 বছর, বাজেটের অর্ধেক পর্যন্ত)",
    "Govt subsidised loan: OFF - click to apply (0.5%, 15 yr)":
        "সরকারি ভর্তুকির ঋণ: বন্ধ - আবেদন করতে ক্লিক করো (0.5%, 15 বছর)",
    "A = P r / (1 - (1 + r)^-n)   (equal yearly payments)": "A = P r / (1 - (1 + r)^-n)   (প্রতি বছর সমান কিস্তি)",
    "Toll rate (x standard)": "টোলের হার (সাধারণের x গুণ)",
}

FINANCE_PATTERNS = [
    (r"Civil Grant committed: (Rs .+)", r"সিভিল অনুদান নির্ধারিত: "),
    (r"Use Civil Grants: ON \(wallet (.+)\)", r"সিভিল অনুদান ব্যবহার: চালু (তহবিল )"),
    (r"Use Civil Grants: OFF \(wallet (.+)\)", r"সিভিল অনুদান ব্যবহার: বন্ধ (তহবিল )"),
    (r"= (Rs .+?) x 0\.02 / \(1 - 1\.02\^-10\) = (Rs .+?) a year", r"= \1 x 0.02 / (1 - 1.02^-10) = বছরে \2"),
    (r"(.+?): (Rs .+?) per (\w+), about ([\d,]+) a day",
     lambda m: f"{TOLL_NAMES.get(m.group(1), m.group(1))}: প্রতি {UNITS.get(m.group(3), m.group(3))} "
               f"{m.group(2)}, দিনে প্রায় {m.group(4)}"),
    (r"Year-1 income = rate x users x 365 = (Rs .+?); upkeep 3% of cost = (Rs .+?) a year",
     r"প্রথম বছরের আয় = হার x ব্যবহারকারী x 365 = \1; রক্ষণাবেক্ষণ খরচের 3% = বছরে \2"),
    (r"Coverage = \(income - upkeep\) / A = (\S+)   \(the bank needs 1\.50 = a 50% margin\)",
     r"কভারেজ = (আয় - রক্ষণাবেক্ষণ) / A = \1   (ব্যাংকের চাই 1.50 = 50% বাড়তি)"),
    (r"Investment recovered in year (\d+)", r"বিনিয়োগ ফেরত আসে \1 নম্বর বছরে"),
    (r"Not recovered within (\d+) years", r"\1 বছরের মধ্যে ফেরত আসে না"),
    (r"Loan repaid in year (\d+); interest paid (Rs .+)", r"ঋণ শোধ হয় \1 নম্বর বছরে; মোট সুদ \2"),
    (r"Profit after (\d+) years: (-?Rs .+?) - traffic grows 6% a year, so the business keeps growing",
     r"\1 বছর পর লাভ: \2 - যাতায়াত বছরে 6% বাড়ে, তাই ব্যবসা বাড়তেই থাকে"),
    (r"recovered: year (\d+)", r"ফেরত: \1 নম্বর বছর"),
    (r"Govt loan (Rs .+?) at 0\.5% for 15 yr = (Rs .+?) a year", r"সরকারি ঋণ \1, 0.5% সুদে 15 বছর = বছরে \2"),
    (r"Bank loan (Rs .+?) at 2% for 10 yr = (Rs .+?) a year", r"ব্যাংক ঋণ \1, 2% সুদে 10 বছর = বছরে \2"),
    (r"The subsidy saves (Rs .+?) of interest", r"ভর্তুকিতে সুদের \1 বাঁচে"),
    (r"(Rs .+?) \(loans (Rs .+?)\)", r"\1 (ঋণ \2)"),
    (r"year (\d+)", r"\1 নম্বর বছর"),
    (r"(Rs .+?), (Rs .+?) a year", r"\1, বছরে \2"),
]
