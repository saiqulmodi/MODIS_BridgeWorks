"""Class 6 - Finance (Junior Cadet): compound growth over several years, reverse percentages,
return on investment, payback periods, commission, reducing-balance depreciation, total cost of
a loan, income tax slabs in simple form, currency both ways, budgets for projects and fairness."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 100, r * 2, r + 10):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _rs(q_en, q_bn, r, ex_en, ex_bn, alts):
    o = _o(r, *alts)
    return mcq(q_en, [f"Rs {x:,}" for x in o], 0, ex_en, q_bn, [f"{x:,} টাকা" for x in o], ex_bn)


def _pc(q_en, q_bn, r, ex_en, ex_bn, alts):
    o = _o(r, *alts)
    f = lambda x: f"{x:g}%"
    return mcq(q_en, [f(x) for x in o], 0, ex_en, q_bn, [f(x) for x in o], ex_bn)


def ci(P, r, n):
    a = P
    steps = []
    for _ in range(n):
        a = a + a * r // 100
        steps.append(f"{a:,}")
    simple = P + P * r * n // 100
    return _rs(f"Rs {P:,} grows at {r}% compound interest a year. What is it worth after {n} years?",
               f"{P:,} টাকা বছরে {r}% চক্রবৃদ্ধি সুদে বাড়ে। {n} বছর পরে কত হবে?", a,
               f"Each year multiply by 1.{r:02d}: " + " -> ".join(steps) + f". (Simple interest would give only {simple:,}.)",
               f"প্রতি বছর 1.{r:02d} দিয়ে গুণ: " + " -> ".join(steps) + f"। (সরল সুদে হতো মাত্র {simple:,}।)",
               (simple, P * r * n // 100, a - P))


def reverse(final, p, item_en, item_bn):
    orig = final * 100 // (100 + p)
    wrong = final - final * p // 100
    return _rs(f"After a {p}% price rise, {item_en} costs Rs {final:,}. What did it cost before?",
               f"{p}% দাম বাড়ার পর {item_bn}-এর দাম {final:,} টাকা। আগে কত ছিল?", orig,
               f"New = old x {100 + p}%, so old = {final:,} ÷ {(100 + p) / 100:g} = Rs {orig:,}. (Taking {p}% off {final:,} gives the wrong {wrong:,}.)",
               f"নতুন = পুরোনো x {100 + p}%, তাই পুরোনো = {final:,} ÷ {(100 + p) / 100:g} = {orig:,} টাকা। ({final:,}-এর {p}% বাদ দিলে ভুল {wrong:,} হয়।)",
               (wrong, final - p, final))


def roi(cost, gain, what_en, what_bn):
    r = (gain - cost) * 100 // cost
    return _pc(f"{what_en} cost Rs {cost:,} and brought back Rs {gain:,}. What is the return on investment (ROI)?",
               f"{what_bn}-এ {cost:,} টাকা খরচ হয়ে {gain:,} টাকা ফেরত এল। বিনিয়োগে রিটার্ন (আরওআই) কত?", r,
               f"ROI = (gain - cost) ÷ cost x 100 = ({gain:,} - {cost:,}) ÷ {cost:,} x 100 = {r}%.",
               f"আরওআই = (ফেরত - খরচ) ÷ খরচ x 100 = ({gain:,} - {cost:,}) ÷ {cost:,} x 100 = {r}%।",
               ((gain - cost) * 100 // gain, gain * 100 // cost, r + 5))


def payback(cost, yearly, what_en, what_bn):
    r = cost / yearly
    r = int(r) if r == int(r) else round(r, 1)
    o = _o(r, round(yearly / cost * 100, 1), r * 2, r + 1)
    f = lambda x: f"{x:g}"
    return mcq(f"{what_en} costs Rs {cost:,} and saves Rs {yearly:,} a year. What is the payback period?",
               [f(x) + " years" for x in o], 0,
               f"Payback = cost ÷ yearly saving = {cost:,} ÷ {yearly:,} = {r:g} years.",
               f"{what_bn}-এর খরচ {cost:,} টাকা আর বছরে {yearly:,} টাকা বাঁচায়। খরচ ফেরতের সময় কত?",
               [f(x) + " বছর" for x in o],
               f"খরচ ফেরতের সময় = খরচ ÷ বার্ষিক সাশ্রয় = {cost:,} ÷ {yearly:,} = {r:g} বছর।")


def commission(sales, rate, base):
    c = sales * rate // 100
    return _rs(f"A salesperson earns Rs {base:,} a month plus {rate}% commission. This month they sold Rs {sales:,} of steel. What is their total pay?",
               f"একজন বিক্রয়কর্মী মাসে {base:,} টাকা আর {rate}% কমিশন পান। এ মাসে {sales:,} টাকার ইস্পাত বেচলেন। মোট বেতন কত?", base + c,
               f"Commission = {rate}% of {sales:,} = {c:,}; total = {base:,} + {c:,} = Rs {base + c:,}.",
               f"কমিশন = {sales:,}-এর {rate}% = {c:,}; মোট = {base:,} + {c:,} = {base + c:,} টাকা।",
               (c, base, sales * rate))


def reducing(cost, p, years):
    v = cost
    for _ in range(years):
        v = v - v * p // 100
    straight = cost - cost * p * years // 100
    return _rs(f"A crane costs Rs {cost:,} and loses {p}% of its value each year (reducing balance). What is it worth after {years} years?",
               f"একটা ক্রেনের দাম {cost:,} টাকা আর প্রতি বছর তার মূল্যের {p}% কমে (হ্রাসমান জের)। {years} বছর পরে দাম কত?", v,
               f"Multiply by {(100 - p) / 100:g} each year: {cost:,} x {(100 - p) / 100:g}^{years} = Rs {v:,}. (Straight-line would give {straight:,}.)",
               f"প্রতি বছর {(100 - p) / 100:g} দিয়ে গুণ: {cost:,} x {(100 - p) / 100:g}^{years} = {v:,} টাকা। (সরলরেখা পদ্ধতিতে হতো {straight:,}।)",
               (straight, cost * p // 100, cost - v))


def loan_total(P, emi, months):
    total = emi * months
    return _rs(f"A Rs {P:,} loan is repaid at Rs {emi:,} a month for {months} months. How much interest is paid in total?",
               f"{P:,} টাকার ঋণ মাসে {emi:,} টাকা করে {months} মাসে শোধ হলো। মোট কত সুদ দেওয়া হলো?", total - P,
               f"Total repaid = {emi:,} x {months} = {total:,}; interest = {total:,} - {P:,} = Rs {total - P:,}.",
               f"মোট শোধ = {emi:,} x {months} = {total:,}; সুদ = {total:,} - {P:,} = {total - P:,} টাকা।",
               (total, emi, P // months))


ITEMS = (
    ci(10000, 10, 3), ci(20000, 5, 3), ci(5000, 20, 3), ci(1000, 10, 4), ci(8000, 25, 2),
    reverse(1100, 10, "a bag of bolts", "এক ব্যাগ বল্টু"), reverse(1200, 20, "a helmet", "একটা হেলমেট"),
    reverse(5750, 15, "a tonne of cement", "এক টন সিমেন্ট"), reverse(2625, 5, "a train pass", "একটা ট্রেন-পাস"),
    reverse(3240, 8, "a generator rental", "জেনারেটর ভাড়া"),
    roi(10000, 12500, "A new mixer", "একটা নতুন মিক্সার"), roi(50000, 65000, "A training course for welders", "ঝালাইকারীদের প্রশিক্ষণ"),
    roi(200000, 260000, "A delivery truck", "একটা ডেলিভারি ট্রাক"), roi(8000, 10000, "Solar lights for a site", "নির্মাণস্থলের সৌরবাতি"),
    payback(60000, 20000, "Solar panels for a site office", "নির্মাণস্থলের অফিসের সৌর প্যানেল"),
    payback(500000, 125000, "A new bridge's toll booth system", "নতুন সেতুর টোল-ব্যবস্থা"),
    payback(90000, 36000, "LED bridge lighting", "সেতুর এলইডি আলো"),
    payback(1200000, 150000, "A ferry replaced by a footbridge", "খেয়ার বদলে হাঁটার সেতু"),
    commission(200000, 2, 15000), commission(500000, 3, 12000), commission(80000, 5, 10000),
    reducing(1000000, 20, 2), reducing(500000, 10, 3), reducing(200000, 25, 2),
    loan_total(100000, 9000, 12), loan_total(50000, 4500, 12), loan_total(240000, 11000, 24),
    mcq("Why does a 'reverse percentage' need division, not subtraction?", ["The percentage was taken of the ORIGINAL, not the new amount", "Subtraction is illegal", "Division is faster", "It does not"], 0,
        "If Rs 100 rises 10% to 110, taking 10% off 110 gives 99, not 100.",
        "'উল্টো শতাংশে' বিয়োগ নয়, ভাগ লাগে কেন?", ["শতাংশ নেওয়া হয়েছিল আদি অঙ্কের, নতুনের নয়", "বিয়োগ বেআইনি", "ভাগ দ্রুত", "লাগে না"],
        "100 টাকা 10% বেড়ে 110 হলে 110-এর 10% বাদ দিলে 99 হয়, 100 নয়।"),
    mcq("What is 'APR' on a loan?", ["Annual Percentage Rate - the yearly cost of borrowing including fees", "A type of bank", "A monthly bonus", "Average Price Rise"], 0,
        "Compare APRs to find the cheapest loan.",
        "ঋণে 'এপিআর' কী?", ["বার্ষিক শতাংশ হার - ফি-সহ ধারের বার্ষিক খরচ", "এক রকম ব্যাংক", "মাসিক বোনাস", "গড় দামবৃদ্ধি"],
        "সবচেয়ে সস্তা ঋণ খুঁজতে এপিআর তুলনা করো।"),
    mcq("Two loans: A at 12% APR, B at 9% APR plus a big upfront fee. How should you compare them?", ["Work out the total cost of each over the full term", "Always pick the lower rate", "Always pick A", "Pick randomly"], 0,
        "Fees can make a 'cheaper' rate more expensive overall.",
        "দুটো ঋণ: A 12% এপিআর-এ, B 9% এপিআর-এ সঙ্গে বড় অগ্রিম ফি। কীভাবে তুলনা করবে?", ["পুরো মেয়াদে প্রতিটির মোট খরচ হিসাব করো", "সবসময় কম হারটা বাছো", "সবসময় A বাছো", "এলোমেলো বাছো"],
        "ফি 'সস্তা' হারকেও মোটে দামি করতে পারে।"),
    mcq("What is 'return on investment' (ROI)?", ["Profit from an investment as a percentage of its cost", "The cost of a loan", "A tax", "Total sales"], 0,
        "Higher ROI means money was used more effectively.",
        "'বিনিয়োগে রিটার্ন' (আরওআই) কী?", ["খরচের শতাংশে বিনিয়োগের লাভ", "ঋণের খরচ", "কর", "মোট বিক্রি"],
        "বেশি আরওআই মানে টাকা বেশি কার্যকরভাবে ব্যবহার হয়েছে।"),
    mcq("What is a 'payback period'?", ["How long an investment takes to earn back its cost", "A loan holiday", "A refund window in a shop", "A tax return"], 0,
        "Shorter payback usually means less risk.",
        "'খরচ ফেরতের সময়' কী?", ["বিনিয়োগ তার খরচ তুলতে কত সময় নেয়", "ঋণের ছুটি", "দোকানে ফেরতের সময়", "করের রিটার্ন"],
        "কম সময়ে ফেরত মানে সাধারণত কম ঝুঁকি।"),
    mcq("What is 'commission'?", ["Pay based on a percentage of sales made", "A fixed salary", "A tax", "A loan"], 0,
        "It rewards salespeople for selling more.",
        "'কমিশন' কী?", ["বিক্রির শতাংশের ভিত্তিতে বেতন", "স্থির বেতন", "কর", "ঋণ"],
        "বেশি বেচার জন্য বিক্রয়কর্মীদের পুরস্কৃত করে।"),
    mcq("What is 'reducing balance' depreciation?", ["Losing the same PERCENTAGE of the remaining value each year", "Losing the same amount every year", "Gaining value", "No change"], 0,
        "Machines lose most value in their early years.",
        "'হ্রাসমান জের' অবচয় কী?", ["প্রতি বছর বাকি মূল্যের একই শতাংশ কমা", "প্রতি বছর একই অঙ্ক কমা", "মূল্য বাড়া", "পরিবর্তন নেই"],
        "যন্ত্র প্রথম বছরগুলোতে বেশিরভাগ মূল্য হারায়।"),
    mcq("What is 'income tax'?", ["Tax paid on what people earn above a set amount", "Tax on goods in shops", "A road toll", "A bank fee"], 0,
        "In India, income below a threshold is not taxed; higher income is taxed at higher rates.",
        "'আয়কর' কী?", ["নির্দিষ্ট অঙ্কের বেশি আয়ের উপর দেওয়া কর", "দোকানের মালের উপর কর", "রাস্তার টোল", "ব্যাংকের ফি"],
        "ভারতে একটা সীমার নিচের আয়ে কর নেই; বেশি আয়ে বেশি হারে কর।"),
    mcq("A simple tax rule: no tax on the first Rs 3 lakh, then 5% on the rest. Tax on Rs 5 lakh income?", ["Rs 10,000", "Rs 25,000", "Rs 15,000", "Rs 5,000"], 0,
        "Taxable = 5 - 3 = 2 lakh; 5% of 2 lakh = 10,000.",
        "একটা সহজ কর-নিয়ম: প্রথম 3 লাখে কর নেই, বাকিটায় 5%। 5 লাখ আয়ে কর কত?", ["10,000 টাকা", "25,000 টাকা", "15,000 টাকা", "5,000 টাকা"],
        "করযোগ্য = 5 - 3 = 2 লাখ; 2 লাখের 5% = 10,000।"),
    mcq("What is a 'progressive' tax?", ["Higher earners pay a higher percentage", "Everyone pays the same amount", "Poorer people pay more", "Tax that grows every day"], 0,
        "It aims to share the cost of public services fairly.",
        "'প্রগতিশীল' কর কী?", ["বেশি আয়ের মানুষ বেশি শতাংশ দেন", "সবাই একই অঙ্ক দেন", "গরিবেরা বেশি দেন", "রোজ বাড়া কর"],
        "জনপরিষেবার খরচ ন্যায্যভাবে ভাগ করার লক্ষ্য।"),
    mcq("What is 'TDS' (tax deducted at source)?", ["Tax taken by the payer before you receive your money", "A shop discount", "A bank loan", "A toll"], 0,
        "Contractors' payments often have TDS deducted.",
        "'টিডিএস' (উৎসে কর কর্তন) কী?", ["টাকা পাওয়ার আগেই প্রদানকারী যে কর কেটে রাখেন", "দোকানের ছাড়", "ব্যাংক-ঋণ", "টোল"],
        "ঠিকাদারদের পেমেন্টে প্রায়ই টিডিএস কাটা হয়।"),
    mcq("A contractor bills Rs 1,00,000 and 2% TDS is deducted. How much is received?", ["Rs 98,000", "Rs 1,02,000", "Rs 2,000", "Rs 80,000"], 0,
        "2% of 1,00,000 = 2,000; 1,00,000 - 2,000 = 98,000.",
        "একজন ঠিকাদার 1,00,000 টাকার বিল দিলেন আর 2% টিডিএস কাটা হলো। কত পেলেন?", ["98,000 টাকা", "1,02,000 টাকা", "2,000 টাকা", "80,000 টাকা"],
        "1,00,000-এর 2% = 2,000; 1,00,000 - 2,000 = 98,000।"),
    mcq("$1 = Rs 84. A German machine costs €2,000 and €1 = Rs 90. Which costs more: the machine or a $2,000 one?", ["The €2,000 machine (Rs 1,80,000 vs Rs 1,68,000)", "The $2,000 machine", "They cost the same", "Cannot tell"], 0,
        "2,000 x 90 = 1,80,000; 2,000 x 84 = 1,68,000.",
        "$1 = 84 টাকা। একটা জার্মান যন্ত্রের দাম €2,000 আর €1 = 90 টাকা। কোনটা দামি: সেটা না $2,000-এর যন্ত্র?", ["€2,000-এর যন্ত্র (1,80,000 বনাম 1,68,000 টাকা)", "$2,000-এর যন্ত্র", "দুটোর দাম সমান", "বলা যায় না"],
        "2,000 x 90 = 1,80,000; 2,000 x 84 = 1,68,000।"),
    mcq("You have Rs 8,400 and $1 = Rs 84. How many dollars can you get (ignoring fees)?", ["$100", "$1,000", "$84", "$10"], 0,
        "8,400 ÷ 84 = 100.",
        "তোমার কাছে 8,400 টাকা আর $1 = 84 টাকা। (ফি বাদে) কত ডলার পাবে?", ["$100", "$1,000", "$84", "$10"],
        "8,400 ÷ 84 = 100।"),
    mcq("A footbridge budget: materials Rs 2.4 lakh, labour Rs 1.6 lakh, 10% contingency on both. Total?", ["Rs 4.4 lakh", "Rs 4 lakh", "Rs 4.1 lakh", "Rs 5 lakh"], 0,
        "2.4 + 1.6 = 4.0; plus 10% = 4.4 lakh.",
        "হাঁটার সেতুর বাজেট: উপাদান 2.4 লাখ, শ্রম 1.6 লাখ, দুটোর উপর 10% আকস্মিক-তহবিল। মোট?", ["4.4 লাখ টাকা", "4 লাখ টাকা", "4.1 লাখ টাকা", "5 লাখ টাকা"],
        "2.4 + 1.6 = 4.0; 10% যোগে 4.4 লাখ।"),
    mcq("A crew of 6 workers earns Rs 600 a day each. A job takes 15 days. What is the labour cost?", ["Rs 54,000", "Rs 9,000", "Rs 3,600", "Rs 90,000"], 0,
        "6 x 600 x 15 = 54,000.",
        "6 জনের একটা দল জনপ্রতি দিনে 600 টাকা পায়। কাজে 15 দিন লাগে। শ্রম-খরচ কত?", ["54,000 টাকা", "9,000 টাকা", "3,600 টাকা", "90,000 টাকা"],
        "6 x 600 x 15 = 54,000।"),
    mcq("What is 'person-days' in project planning?", ["Number of workers x number of days", "Days off for workers", "Workers' birthdays", "Hours slept"], 0,
        "A 60 person-day job could be 6 people for 10 days or 10 people for 6.",
        "প্রকল্প-পরিকল্পনায় 'মানব-দিবস' কী?", ["কর্মী-সংখ্যা x দিন-সংখ্যা", "কর্মীদের ছুটির দিন", "কর্মীদের জন্মদিন", "ঘুমের ঘণ্টা"],
        "60 মানব-দিবসের কাজ 6 জনে 10 দিন বা 10 জনে 6 দিন হতে পারে।"),
    mcq("A job needs 120 person-days. With 8 workers, how many days?", ["15", "960", "128", "12"], 0,
        "120 ÷ 8 = 15.",
        "একটা কাজে 120 মানব-দিবস লাগে। 8 জন কর্মীতে কত দিন?", ["15", "960", "128", "12"],
        "120 ÷ 8 = 15।"),
    mcq("What is a 'cost overrun'?", ["When a project ends up costing more than its budget", "Saving money", "A running race", "A bank bonus"], 0,
        "Good estimates and contingency reduce overruns.",
        "'খরচ-ছাড়ানো' (কস্ট ওভাররান) কী?", ["যখন প্রকল্পের খরচ বাজেট ছাড়িয়ে যায়", "টাকা বাঁচানো", "দৌড় প্রতিযোগিতা", "ব্যাংকের বোনাস"],
        "ভালো আন্দাজ আর আকস্মিক-তহবিল খরচ-ছাড়ানো কমায়।"),
    mcq("A bridge was budgeted at Rs 80 lakh but cost Rs 92 lakh. What was the overrun percentage?", ["15%", "12%", "13%", "92%"], 0,
        "Overrun 12 ÷ 80 x 100 = 15%.",
        "একটা সেতুর বাজেট ছিল 80 লাখ, খরচ হলো 92 লাখ। খরচ-ছাড়ানোর শতাংশ কত?", ["15%", "12%", "13%", "92%"],
        "ছাড়ানো 12 ÷ 80 x 100 = 15%।"),
    mcq("What is a 'sinking fund'?", ["Money saved regularly to pay for a known future cost", "Money that sinks in water", "A bad investment", "A tax"], 0,
        "Bridge owners save for repainting and bearing replacement years ahead.",
        "'ক্ষয়পূরণ তহবিল' (সিঙ্কিং ফান্ড) কী?", ["ভবিষ্যতের জানা খরচ মেটাতে নিয়মিত জমানো টাকা", "জলে ডোবা টাকা", "খারাপ বিনিয়োগ", "কর"],
        "সেতুর মালিকরা বছর আগে থেকে রং আর বিয়ারিং বদলের জন্য জমান।"),
    mcq("A bridge needs repainting in 5 years at Rs 10 lakh. How much should be saved each year (no interest)?", ["Rs 2 lakh", "Rs 50 lakh", "Rs 10 lakh", "Rs 5 lakh"], 0,
        "10 ÷ 5 = 2 lakh a year.",
        "একটা সেতু 5 বছর পরে 10 লাখ টাকায় রং করতে হবে। বছরে কত জমানো উচিত (সুদ ছাড়া)?", ["2 লাখ টাকা", "50 লাখ টাকা", "10 লাখ টাকা", "5 লাখ টাকা"],
        "10 ÷ 5 = বছরে 2 লাখ।"),
    mcq("What is 'whole-life cost' of a bridge?", ["Building cost plus all maintenance and running costs over its life", "Only the building cost", "Only the paint", "The toll price"], 0,
        "A cheaper bridge needing lots of repairs can cost more overall.",
        "সেতুর 'আজীবন খরচ' কী?", ["নির্মাণ-খরচ আর আয়ুষ্কালের সব রক্ষণাবেক্ষণ ও চালানোর খরচ", "শুধু নির্মাণ-খরচ", "শুধু রং", "টোলের দাম"],
        "অনেক মেরামত লাগা সস্তা সেতু মোটে বেশি দামি হতে পারে।"),
    mcq("Bridge A costs Rs 50 lakh + Rs 2 lakh/year upkeep. Bridge B costs Rs 60 lakh + Rs 1 lakh/year. Over 20 years, which is cheaper?", ["B (Rs 80 lakh vs Rs 90 lakh)", "A", "They are equal", "Neither"], 0,
        "A: 50 + 40 = 90; B: 60 + 20 = 80.",
        "সেতু A: 50 লাখ + বছরে 2 লাখ রক্ষণাবেক্ষণ। সেতু B: 60 লাখ + বছরে 1 লাখ। 20 বছরে কোনটা সস্তা?", ["B (80 লাখ বনাম 90 লাখ)", "A", "দুটো সমান", "কোনোটাই না"],
        "A: 50 + 40 = 90; B: 60 + 20 = 80।"),
    mcq("What does 'liquidity' mean?", ["How quickly something can be turned into cash without loss", "How wet it is", "How much it weighs", "A type of tax"], 0,
        "Cash is fully liquid; land and cranes are not.",
        "'তারল্য' মানে কী?", ["ক্ষতি ছাড়া কত দ্রুত কোনো কিছুকে নগদে বদলানো যায়", "কত ভেজা", "কত ভারী", "এক রকম কর"],
        "নগদ পুরো তরল; জমি আর ক্রেন নয়।"),
    mcq("Why can a firm with lots of cranes still go bust?", ["It may not have enough cash to pay bills when they are due", "Cranes are worthless", "Firms never go bust", "Cranes pay wages"], 0,
        "Assets are not the same as cash in hand.",
        "অনেক ক্রেন থাকা সংস্থাও কেন দেউলিয়া হতে পারে?", ["বিল দেওয়ার সময় যথেষ্ট নগদ না থাকতে পারে", "ক্রেন মূল্যহীন", "সংস্থা কখনো দেউলিয়া হয় না", "ক্রেন বেতন দেয়"],
        "সম্পদ আর হাতে নগদ এক নয়।"),
    mcq("What is 'working capital'?", ["Money available for day-to-day running costs", "A city where people work", "The value of buildings only", "A type of loan only"], 0,
        "Current assets minus current liabilities.",
        "'চলতি মূলধন' কী?", ["দৈনন্দিন চালানোর খরচের জন্য উপলব্ধ টাকা", "যে শহরে মানুষ কাজ করে", "শুধু ভবনের মূল্য", "শুধু এক রকম ঋণ"],
        "চলতি সম্পদ বিয়োগ চলতি দায়।"),
    mcq("What is 'crowdfunding'?", ["Raising money from many people, often online, for a project", "Paying a crowd to watch", "A bank loan", "A government tax"], 0,
        "In real life it needs legal checks - BridgeWorks donation camps use only in-game Civil Grants.",
        "'গণ-অর্থায়ন' (ক্রাউডফান্ডিং) কী?", ["প্রকল্পের জন্য অনেক মানুষের থেকে, প্রায়ই অনলাইনে, টাকা তোলা", "ভিড়কে দেখার জন্য টাকা দেওয়া", "ব্যাংক-ঋণ", "সরকারি কর"],
        "বাস্তবে আইনি যাচাই লাগে - BridgeWorks-এর দানশিবির শুধু খেলার সিভিল গ্রান্ট ব্যবহার করে।"),
    mcq("Why is it important that donation money is used for the stated cause?", ["Donors trusted it would be; misuse is dishonest and can be illegal", "It does not matter", "Charities can spend it on anything", "Donors forget"], 0,
        "Accountability keeps giving alive.",
        "দানের টাকা ঘোষিত কাজেই ব্যবহার করা জরুরি কেন?", ["দাতারা সেই বিশ্বাসে দিয়েছেন; অপব্যবহার অসৎ আর বেআইনি হতে পারে", "কিছু যায় আসে না", "দাতব্য সংস্থা যা খুশি খরচ করতে পারে", "দাতারা ভুলে যান"],
        "জবাবদিহি দানকে বাঁচিয়ে রাখে।"),
    mcq("A village footbridge saves 500 people 1 hour each per day. If their time is worth Rs 50 an hour, what is the daily benefit?", ["Rs 25,000", "Rs 550", "Rs 2,500", "Rs 50,000"], 0,
        "500 x 1 x 50 = 25,000 - time saved is real economic value.",
        "একটা গ্রামের হাঁটার সেতু 500 জনের প্রত্যেকের দিনে 1 ঘণ্টা বাঁচায়। তাঁদের সময়ের মূল্য ঘণ্টায় 50 টাকা হলে দৈনিক উপকার কত?", ["25,000 টাকা", "550 টাকা", "2,500 টাকা", "50,000 টাকা"],
        "500 x 1 x 50 = 25,000 - বাঁচানো সময় আসল অর্থনৈতিক মূল্য।"),
    mcq("What is a 'cost-benefit analysis'?", ["Comparing all the costs of a project with all its benefits in money terms", "Listing only costs", "A bank statement", "A tax return"], 0,
        "Governments use it to choose which bridges to build first.",
        "'খরচ-উপকার বিশ্লেষণ' কী?", ["প্রকল্পের সব খরচকে টাকার হিসেবে সব উপকারের সঙ্গে তুলনা", "শুধু খরচের তালিকা", "ব্যাংক-বিবরণী", "করের রিটার্ন"],
        "কোন সেতু আগে বানানো হবে তা বাছতে সরকার এটা ব্যবহার করে।"),
    mcq("A project costs Rs 2 crore and gives benefits worth Rs 5 crore. What is the benefit-cost ratio?", ["2.5", "0.4", "3", "7"], 0,
        "5 ÷ 2 = 2.5. Above 1 means benefits exceed costs.",
        "একটা প্রকল্পের খরচ 2 কোটি আর উপকারের মূল্য 5 কোটি। উপকার-খরচ অনুপাত কত?", ["2.5", "0.4", "3", "7"],
        "5 ÷ 2 = 2.5। 1-এর বেশি মানে উপকার খরচ ছাড়িয়ে যায়।"),
    mcq("Why can 'buy now, pay later' offers be risky for young people?", ["Missed payments add fees and debt can build up quickly", "They are always free", "Shops lose money", "There is no risk"], 0,
        "Only buy what you can afford to repay on time.",
        "'এখন কেনো, পরে দাও' প্রস্তাব তরুণদের জন্য ঝুঁকির কেন?", ["কিস্তি বাদ গেলে ফি যোগ হয় আর দ্রুত ঋণ জমে", "সবসময় বিনামূল্যে", "দোকান টাকা হারায়", "ঝুঁকি নেই"],
        "সময়মতো শোধ করতে পারবে শুধু এমন জিনিসই কেনো।"),
    mcq("What is a 'financial goal' that is SMART?", ["Specific, Measurable, Achievable, Relevant and Time-bound", "Spend More And Regret Today", "Simple Money Accounts Return Tax", "Save Minimal Amounts Randomly"], 0,
        "'Save Rs 3,600 for a bicycle in 12 months' is SMART.",
        "'স্মার্ট' আর্থিক লক্ষ্য কী?", ["নির্দিষ্ট, পরিমাপযোগ্য, অর্জনযোগ্য, প্রাসঙ্গিক আর সময়বদ্ধ", "আজ বেশি খরচ করে অনুশোচনা", "সহজ টাকার হিসাবে কর ফেরত", "এলোমেলো অল্প সঞ্চয়"],
        "'12 মাসে সাইকেলের জন্য 3,600 টাকা জমানো' স্মার্ট।"),
    ci(50000, 10, 2), ci(4000, 5, 2), ci(16000, 25, 2), ci(30000, 10, 3),
    reverse(4400, 10, "a bridge model kit", "একটা সেতু-মডেল কিট"), reverse(690, 15, "a pair of gloves", "এক জোড়া দস্তানা"),
    reverse(13000, 30, "a welding machine", "একটা ঝালাই-যন্ত্র"), reverse(840, 12, "a box of paint", "এক বাক্স রং"),
    roi(40000, 50000, "A small workshop machine", "কারখানার একটা ছোট যন্ত্র"), roi(25000, 35000, "A survey drone", "একটা জরিপ-ড্রোন"),
    roi(120000, 150000, "A portable cabin office", "একটা বহনযোগ্য কেবিন-অফিস"), roi(5000, 6000, "Safety training videos", "নিরাপত্তা-প্রশিক্ষণের ভিডিও"),
    payback(40000, 10000, "A rainwater tank for a site", "নির্মাণস্থলের বৃষ্টির জলের ট্যাংক"),
    payback(300000, 60000, "An electric site vehicle", "নির্মাণস্থলের বৈদ্যুতিক গাড়ি"),
    payback(75000, 30000, "A concrete recycling crusher hire plan", "কংক্রিট-পুনর্ব্যবহারের পেষক-ভাড়ার পরিকল্পনা"),
    payback(2000000, 400000, "A toll bridge upgrade", "একটা টোল-সেতুর উন্নয়ন"),
    commission(150000, 4, 9000), commission(320000, 2, 14000), commission(60000, 10, 8000),
    reducing(400000, 10, 2), reducing(800000, 25, 2), reducing(250000, 20, 3),
    loan_total(60000, 5500, 12), loan_total(150000, 7000, 24), loan_total(30000, 2700, 12),
    mcq("What is 'gross pay' versus 'net pay'?", ["Gross is before deductions; net is what you actually receive", "They are the same", "Net is before tax", "Gross is after tax"], 0,
        "Net = gross - tax - other deductions.",
        "'মোট বেতন' আর 'নিট বেতন'-এর পার্থক্য কী?", ["মোট কাটার আগে; নিট হাতে যা আসে", "দুটো একই", "নিট করের আগে", "মোট করের পরে"],
        "নিট = মোট - কর - অন্য কাটা।"),
    mcq("What is the 'Provident Fund' (PF) in India?", ["A retirement savings fund that worker and employer both pay into", "A loan", "A tax", "A lottery"], 0,
        "It builds savings for old age.",
        "ভারতে 'ভবিষ্যনিধি' (পিএফ) কী?", ["অবসরের সঞ্চয়-তহবিল, যাতে কর্মী আর নিয়োগকর্তা দুজনেই দেন", "ঋণ", "কর", "লটারি"],
        "বার্ধক্যের জন্য সঞ্চয় গড়ে।"),
    mcq("Why is compound interest called 'interest on interest'?", ["Each year's interest is added and then earns interest too", "Banks charge twice", "Interest is paid daily in cash", "It is a type of tax"], 0,
        "Over decades, this snowball effect is huge.",
        "চক্রবৃদ্ধি সুদকে 'সুদের উপর সুদ' বলে কেন?", ["প্রতি বছরের সুদ যোগ হয়ে তারও সুদ হয়", "ব্যাংক দুবার নেয়", "রোজ নগদে সুদ দেওয়া হয়", "এক রকম কর"],
        "দশকের পর দশক এই তুষারগোলক-প্রভাব বিশাল।"),
    mcq("Money doubles at 9% compound interest in about how many years (Rule of 72)?", ["8 years", "9 years", "72 years", "4 years"], 0,
        "72 ÷ 9 = 8.",
        "9% চক্রবৃদ্ধি সুদে টাকা মোটামুটি কত বছরে দ্বিগুণ হয় (72-এর নিয়ম)?", ["8 বছর", "9 বছর", "72 বছর", "4 বছর"],
        "72 ÷ 9 = 8।"),
    mcq("What is 'net present value' in simple words?", ["Future money is worth less today, so future benefits are reduced to today's value", "The price tag", "A tax", "Money in your pocket only"], 0,
        "Rs 100 next year is worth less than Rs 100 today - it could earn interest meanwhile.",
        "সহজ কথায় 'নিট বর্তমান মূল্য' কী?", ["ভবিষ্যতের টাকার আজকের মূল্য কম, তাই ভবিষ্যৎ উপকারকে আজকের মূল্যে কমিয়ে ধরা হয়", "দামের ট্যাগ", "কর", "শুধু পকেটের টাকা"],
        "আগামী বছরের 100 টাকার মূল্য আজকের 100 টাকার চেয়ে কম - মাঝে সুদ পেতে পারত।"),
    mcq("Would you rather have Rs 1,000 today or Rs 1,000 in 2 years?", ["Today - you could save or invest it meanwhile", "In 2 years", "No difference", "Neither"], 0,
        "This is the 'time value of money'.",
        "আজ 1,000 টাকা না 2 বছর পরে 1,000 টাকা - কোনটা চাইবে?", ["আজ - মাঝে জমিয়ে বা খাটিয়ে বাড়াতে পারবে", "2 বছর পরে", "পার্থক্য নেই", "কোনোটাই না"],
        "একে বলে 'টাকার সময়-মূল্য'।"),
    mcq("What is a 'guarantor' on a loan?", ["Someone who promises to repay if the borrower cannot", "The bank manager", "A tax officer", "A shopkeeper"], 0,
        "Only agree to be a guarantor if you can truly afford to pay.",
        "ঋণের 'জামিনদার' কে?", ["ঋণগ্রহীতা না পারলে যিনি শোধের প্রতিশ্রুতি দেন", "ব্যাংক-ম্যানেজার", "কর-আধিকারিক", "দোকানদার"],
        "সত্যিই দিতে পারলে তবেই জামিনদার হতে রাজি হও।"),
    mcq("What is a 'microfinance' loan?", ["A small loan to people or tiny businesses that banks often ignore", "A huge company loan", "A free grant", "A tax refund"], 0,
        "Self-help groups in Bengal use microfinance to start small businesses.",
        "'ক্ষুদ্রঋণ' (মাইক্রোফিনান্স) কী?", ["যাঁদের ব্যাংক প্রায়ই উপেক্ষা করে সেই মানুষ বা ছোট ব্যবসাকে ছোট ঋণ", "বড় কোম্পানির ঋণ", "বিনামূল্যের অনুদান", "করের ফেরত"],
        "বাংলার স্বনির্ভর গোষ্ঠী ছোট ব্যবসা শুরু করতে ক্ষুদ্রঋণ ব্যবহার করে।"),
    mcq("What is a 'self-help group' (SHG)?", ["A small group, often of women, who save together and lend to members", "A gym", "A bank branch", "A government office"], 0,
        "SHGs have helped millions of families build savings and businesses.",
        "'স্বনির্ভর গোষ্ঠী' (এসএইচজি) কী?", ["ছোট দল, প্রায়ই মহিলাদের, যাঁরা একসঙ্গে জমান আর সদস্যদের ধার দেন", "ব্যায়ামাগার", "ব্যাংকের শাখা", "সরকারি দপ্তর"],
        "এসএইচজি লক্ষ লক্ষ পরিবারকে সঞ্চয় আর ব্যবসা গড়তে সাহায্য করেছে।"),
    mcq("A village SHG of 12 members each saves Rs 200 a month. How much after 1 year?", ["Rs 28,800", "Rs 2,400", "Rs 14,400", "Rs 24,000"], 0,
        "12 x 200 x 12 = 28,800.",
        "একটা গ্রামের এসএইচজি-র 12 জন সদস্য মাসে 200 টাকা করে জমান। 1 বছরে কত?", ["28,800 টাকা", "2,400 টাকা", "14,400 টাকা", "24,000 টাকা"],
        "12 x 200 x 12 = 28,800।"),
    mcq("What is 'financial inclusion'?", ["Making sure everyone can use banks, savings, credit and insurance", "Only rich people banking", "Closing banks", "Charging high fees"], 0,
        "Schemes like Jan Dhan accounts brought millions into banking.",
        "'আর্থিক অন্তর্ভুক্তি' কী?", ["সবাই যাতে ব্যাংক, সঞ্চয়, ঋণ আর বিমা ব্যবহার করতে পারেন তা নিশ্চিত করা", "শুধু ধনীদের ব্যাংকিং", "ব্যাংক বন্ধ", "চড়া ফি নেওয়া"],
        "জন ধন অ্যাকাউন্টের মতো প্রকল্প লক্ষ লক্ষ মানুষকে ব্যাংকিংয়ে এনেছে।"),
    mcq("Why do bridges help financial inclusion in remote villages?", ["People can reach banks, markets and jobs more easily", "Bridges print money", "Banks are built on bridges", "They do not"], 0,
        "Access is the first step to opportunity.",
        "প্রত্যন্ত গ্রামে সেতু আর্থিক অন্তর্ভুক্তিতে সাহায্য করে কেন?", ["মানুষ সহজে ব্যাংক, বাজার আর কাজে পৌঁছাতে পারেন", "সেতু টাকা ছাপায়", "সেতুর উপর ব্যাংক বানানো হয়", "করে না"],
        "পৌঁছানোই সুযোগের প্রথম ধাপ।"),
    mcq("What is a 'warranty' worth when choosing between two similar machines?", ["It can save repair costs, so it adds value", "Nothing", "It doubles the price", "It reduces quality"], 0,
        "Compare total value, not just the sticker price.",
        "দুটো একই রকম যন্ত্রের মধ্যে বাছতে ওয়ারেন্টির মূল্য কী?", ["মেরামতের খরচ বাঁচাতে পারে, তাই মূল্য যোগ করে", "কিছুই না", "দাম দ্বিগুণ করে", "মান কমায়"],
        "শুধু দামের ট্যাগ নয়, মোট মূল্য তুলনা করো।"),
    mcq("What does 'pay yourself first' mean?", ["Put savings aside as soon as you are paid, before spending", "Spend everything first", "Pay your boss", "Take a loan first"], 0,
        "Automatic savings make the habit easy.",
        "'আগে নিজেকে দাও' মানে কী?", ["বেতন পাওয়া মাত্র খরচের আগে সঞ্চয় সরিয়ে রাখা", "আগে সব খরচ করা", "মালিককে দেওয়া", "আগে ঋণ নেওয়া"],
        "স্বয়ংক্রিয় সঞ্চয় অভ্যাসটা সহজ করে।"),
)
