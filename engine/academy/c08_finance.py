"""Class 8 - Finance (Junior Cadet): compound interest over several years, the total cost of an
EMI loan, return on investment, present value (discounting), prices after inflation,
straight-line depreciation with scrap value, profit and loss statements, break-even units,
debt-to-income ratios, the repo rate, shares and the P/E ratio, taxes, home loans, microfinance,
pensions and honest money."""
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
    return mcq(q_en, [f"{x:g}%" for x in o], 0, ex_en, q_bn, [f"{x:g}%" for x in o], ex_bn)


def _c(x):
    x = round(x, 1)
    return int(x) if x == int(x) else x


def compound(p, rate, years):
    a = round(p * (1 + rate / 100) ** years)
    si = p + p * rate * years // 100
    return _rs(f"Rs {p:,} is invested at {rate}% a year, compounded yearly. What is it worth after {years} years?",
               f"{p:,} টাকা বছরে {rate}% চক্রবৃদ্ধি হারে বিনিয়োগ করা হলো। {years} বছর পরে মূল্য কত?", a,
               f"Multiply by 1.{rate:02d} each year, {years} times: Rs {a:,}. Simple interest would give only Rs {si:,}.",
               f"প্রতি বছর 1.{rate:02d} দিয়ে গুণ, {years} বার: {a:,} টাকা। সরল সুদে হতো মাত্র {si:,} টাকা।",
               (si, a - p, a + a * rate // 100))


def emi_total(p, emi, months):
    tot = emi * months
    i = tot - p
    return _rs(f"A Rs {p:,} equipment loan is repaid with {months} EMIs of Rs {emi:,}. How much interest is paid in total?",
               f"{p:,} টাকার যন্ত্রপাতি-ঋণ {emi:,} টাকার {months}টি ইএমআই-তে শোধ হয়। মোট কত সুদ দিতে হয়?", i,
               f"Total paid = {emi:,} x {months} = {tot:,}; interest = {tot:,} - {p:,} = Rs {i:,}.",
               f"মোট দেওয়া = {emi:,} x {months} = {tot:,}; সুদ = {tot:,} - {p:,} = {i:,} টাকা।",
               (tot, emi * 12 - p if emi * 12 > p and emi * 12 - p != i else i + 500, i // months))


def roi(cost, gain, what_en, what_bn):
    r = _c((gain - cost) * 100 / cost)
    return _pc(f"A firm spends Rs {cost:,} on {what_en} and it brings back Rs {gain:,}. What is the return on investment?",
               f"একটা সংস্থা {what_bn}-এ {cost:,} টাকা খরচ করে আর তা থেকে {gain:,} টাকা ফেরত আসে। বিনিয়োগে লাভের হার কত?", r,
               f"ROI = (gain - cost) ÷ cost x 100 = ({gain:,} - {cost:,}) ÷ {cost:,} x 100 = {r:g}%.",
               f"লাভের হার = (ফেরত - খরচ) ÷ খরচ x 100 = ({gain:,} - {cost:,}) ÷ {cost:,} x 100 = {r:g}%।",
               (_c(gain * 100 / cost), _c((gain - cost) * 100 / gain), _c(r / 2)))


def pv(future, rate):
    r = future * 100 // (100 + rate)
    return _rs(f"A client promises Rs {future:,} in one year. If money can earn {rate}% a year, what is that promise worth today?",
               f"একজন গ্রাহক এক বছর পরে {future:,} টাকা দেওয়ার প্রতিশ্রুতি দিলেন। টাকা বছরে {rate}% আয় করতে পারলে প্রতিশ্রুতিটার আজকের মূল্য কত?", r,
               f"Present value = {future:,} ÷ 1.{rate:02d} = Rs {r:,}. Money today is worth more than the same money later.",
               f"বর্তমান মূল্য = {future:,} ÷ 1.{rate:02d} = {r:,} টাকা। আজকের টাকা পরের একই টাকার চেয়ে দামি।",
               (future, future - future * rate // 100, future * (100 + rate) // 100))


def inflate(price, rate, years, item_en, item_bn):
    p = round(price * (1 + rate / 100) ** years)
    return _rs(f"{item_en} costs Rs {price:,} today. If prices rise {rate}% a year, roughly what will it cost in {years} years?",
               f"{item_bn}-এর দাম আজ {price:,} টাকা। দাম বছরে {rate}% বাড়লে {years} বছরে মোটামুটি কত হবে?", p,
               f"Compound the rise: {price:,} x 1.{rate:02d}^{years} ≈ Rs {p:,}.",
               f"বৃদ্ধি চক্রবৃদ্ধিতে ধরো: {price:,} x 1.{rate:02d}^{years} ≈ {p:,} টাকা।",
               (price + price * rate * years // 100, price * rate * years // 100, price))


def slde(cost, scrap, years, what_en, what_bn):
    d = (cost - scrap) // years
    return _rs(f"{what_en} costs Rs {cost:,}, lasts {years} years and can be sold for Rs {scrap:,} at the end. What is the yearly straight-line depreciation?",
               f"{what_bn}-এর দাম {cost:,} টাকা, {years} বছর চলে আর শেষে {scrap:,} টাকায় বেচা যায়। বছরে সরলরৈখিক অবচয় কত?", d,
               f"(cost - scrap value) ÷ life = ({cost:,} - {scrap:,}) ÷ {years} = Rs {d:,} a year.",
               f"(দাম - শেষ মূল্য) ÷ আয়ু = ({cost:,} - {scrap:,}) ÷ {years} = বছরে {d:,} টাকা।",
               (cost // years, scrap // years if scrap // years != d else d + 1000, (cost + scrap) // years))


def netprofit(rev, cogs, exp):
    gp = rev - cogs
    np = gp - exp
    return _rs(f"A fabrication firm's year: sales Rs {rev:,}, cost of materials and labour Rs {cogs:,}, office and other expenses Rs {exp:,}. What is the net profit?",
               f"একটা ফ্যাব্রিকেশন-সংস্থার বছর: বিক্রি {rev:,} টাকা, উপাদান আর শ্রমের খরচ {cogs:,} টাকা, অফিস আর অন্য খরচ {exp:,} টাকা। নিট লাভ কত?", np,
               f"Gross profit = {rev:,} - {cogs:,} = {gp:,}; net profit = {gp:,} - {exp:,} = Rs {np:,}.",
               f"মোট লাভ = {rev:,} - {cogs:,} = {gp:,}; নিট লাভ = {gp:,} - {exp:,} = {np:,} টাকা।",
               (gp, rev - exp, rev - cogs - exp // 2))


def breakeven(fixed, price, var, item_en, item_bn):
    n = -(-fixed // (price - var))
    return mcq(f"A workshop has fixed costs of Rs {fixed:,} a month. It sells {item_en} at Rs {price:,} each; each costs Rs {var:,} to make. How many must it sell to break even?",
               [f"{x:,}" for x in _o(n, fixed // price, fixed // var if fixed // var != n else n + 7, n * 2)], 0,
               f"Contribution per unit = {price:,} - {var:,} = {price - var:,}; {fixed:,} ÷ {price - var:,} = {n:,} units.",
               f"একটা কারখানার মাসিক স্থির খরচ {fixed:,} টাকা। এটা {item_bn} প্রতিটা {price:,} টাকায় বেচে; প্রতিটা বানাতে {var:,} টাকা লাগে। লাভ-লোকসান সমান করতে কতগুলো বেচতে হবে?",
               [f"{x:,}" for x in _o(n, fixed // price, fixed // var if fixed // var != n else n + 7, n * 2)],
               f"প্রতি এককে অবদান = {price:,} - {var:,} = {price - var:,}; {fixed:,} ÷ {price - var:,} = {n:,}টি।")


def dti(emis, income):
    r = _c(emis * 100 / income)
    return _pc(f"A site engineer earns Rs {income:,} a month and pays Rs {emis:,} a month in loan EMIs. What is their debt-to-income ratio?",
               f"একজন নির্মাণ-প্রকৌশলী মাসে {income:,} টাকা আয় করেন আর মাসে {emis:,} টাকা ঋণের ইএমআই দেন। ঋণ-আয় অনুপাত কত?", r,
               f"{emis:,} ÷ {income:,} x 100 = {r:g}%. Lenders worry when this goes much above 40-50%.",
               f"{emis:,} ÷ {income:,} x 100 = {r:g}%। এটা 40-50%-এর অনেক উপরে গেলে ঋণদাতারা চিন্তিত হন।",
               (_c(income / emis), _c(100 - r), _c(r + 10)))


def pe(price, eps, co_en, co_bn):
    r = _c(price / eps)
    return mcq(f"A share in {co_en} costs Rs {price:,} and the company earns Rs {eps:g} per share. What is its price-to-earnings (P/E) ratio?",
               [f"{x:g}" for x in _o(r, _c(eps / price * 100), _c(price - eps), _c(r * 2))], 0,
               f"P/E = price ÷ earnings per share = {price:,} ÷ {eps:g} = {r:g}. Buyers are paying {r:g} years of today's earnings.",
               f"{co_bn}-এর একটা শেয়ারের দাম {price:,} টাকা আর কোম্পানি শেয়ারপ্রতি {eps:g} টাকা আয় করে। দাম-আয় (পি/ই) অনুপাত কত?",
               [f"{x:g}" for x in _o(r, _c(eps / price * 100), _c(price - eps), _c(r * 2))],
               f"পি/ই = দাম ÷ শেয়ারপ্রতি আয় = {price:,} ÷ {eps:g} = {r:g}। ক্রেতারা আজকের আয়ের {r:g} বছরের সমান দাম দিচ্ছেন।")


ITEMS = (
    compound(10000, 10, 3), compound(50000, 8, 2), compound(20000, 5, 3), compound(100000, 12, 2),
    emi_total(100000, 9000, 12), emi_total(250000, 12000, 24), emi_total(60000, 5400, 12), emi_total(500000, 11000, 60),
    roi(50000, 65000, "a new welding machine", "একটা নতুন ঝালাই-যন্ত্র"), roi(200000, 250000, "a training course for crane drivers", "ক্রেন-চালকদের প্রশিক্ষণ"),
    roi(80000, 96000, "solar panels for the site office", "নির্মাণস্থলের অফিসের সৌর প্যানেল"), roi(150000, 210000, "a second-hand excavator", "একটা পুরোনো খননযন্ত্র"),
    pv(110000, 10), pv(54000, 8), pv(212000, 6), pv(105000, 5),
    inflate(1000, 10, 2, "A bag of special cement", "এক বস্তা বিশেষ সিমেন্ট"), inflate(50000, 6, 3, "A steel girder", "একটা ইস্পাতের গার্ডার"),
    inflate(2000, 5, 2, "A safety harness", "একটা নিরাপত্তা-জোতা"), inflate(400, 8, 3, "A day's site meals", "নির্মাণস্থলে এক দিনের খাবার"),
    slde(1000000, 100000, 10, "A crane", "একটা ক্রেন"), slde(450000, 50000, 5, "A concrete pump", "একটা কংক্রিট-পাম্প"),
    slde(240000, 40000, 8, "A site van", "নির্মাণস্থলের একটা ভ্যান"), slde(90000, 10000, 4, "A laser level", "একটা লেজার-লেভেল"),
    netprofit(2000000, 1300000, 400000), netprofit(900000, 500000, 250000), netprofit(5000000, 3600000, 900000),
    breakeven(60000, 500, 300, "steel brackets", "ইস্পাতের ব্র্যাকেট"), breakeven(90000, 1200, 900, "railing panels", "রেলিং-প্যানেল"),
    breakeven(40000, 250, 150, "concrete blocks", "কংক্রিটের ব্লক"),
    dti(12000, 40000), dti(25000, 50000), dti(9000, 60000),
    pe(500, 25, "a cement company", "একটা সিমেন্ট-কোম্পানি"), pe(1200, 40, "a construction firm", "একটা নির্মাণ-সংস্থা"), pe(300, 30, "a steel maker", "একটা ইস্পাত-নির্মাতা"),
    mcq("Why does compound interest grow faster than simple interest?", ["Interest is earned on earlier interest as well as on the original sum", "Banks add a bonus each year", "The rate rises every year", "It does not grow faster"], 0,
        "Over long periods the difference becomes huge - in savings and in debts.",
        "চক্রবৃদ্ধি সুদ সরল সুদের চেয়ে দ্রুত বাড়ে কেন?", ["মূল টাকার সঙ্গে আগের সুদের উপরেও সুদ হয়", "ব্যাংক প্রতি বছর বোনাস দেয়", "হার প্রতি বছর বাড়ে", "দ্রুত বাড়ে না"],
        "লম্বা সময়ে পার্থক্য বিশাল হয় - সঞ্চয়ে আর ঋণে দুটোতেই।"),
    mcq("Why does starting to save early matter so much?", ["Compounding has more years to work, so small amounts grow very large", "Banks only accept young savers", "Interest rates are higher for children", "It does not matter"], 0,
        "Rs 1,000 a month from age 20 can beat Rs 2,000 a month from age 35.",
        "আগে থেকে সঞ্চয় শুরু করা এত জরুরি কেন?", ["চক্রবৃদ্ধি বেশি বছর কাজ করে, তাই ছোট অঙ্কও অনেক বড় হয়", "ব্যাংক শুধু অল্পবয়সীদের সঞ্চয় নেয়", "শিশুদের সুদের হার বেশি", "জরুরি নয়"],
        "20 বছর বয়স থেকে মাসে 1,000 টাকা, 35 থেকে মাসে 2,000 টাকাকে হারাতে পারে।"),
    mcq("Interest paid monthly at 1% a month is a little more than 12% a year. Why?", ["Each month's interest itself earns interest, giving about 12.7% a year", "Banks round up", "There are 13 months in a banking year", "It is exactly 12%"], 0,
        "This 'effective annual rate' is what really matters when comparing.",
        "মাসে 1% হারে মাসিক সুদ বছরে 12%-এর একটু বেশি হয়। কেন?", ["প্রতি মাসের সুদ নিজেও সুদ পায়, তাই বছরে প্রায় 12.7%", "ব্যাংক উপরে আসন্ন করে", "ব্যাংকের বছরে 13 মাস", "ঠিক 12%"],
        "তুলনার সময় এই 'কার্যকর বার্ষিক হার'-ই আসল।"),
    mcq("What is 'present value'?", ["What a future amount of money is worth today, after allowing for interest it could earn", "The price of a present", "The value of cash in your pocket only", "Next year's salary"], 0,
        "It lets engineers compare projects with costs and benefits at different times.",
        "'বর্তমান মূল্য' কী?", ["ভবিষ্যতের টাকার আজকের মূল্য, যে সুদ আয় করতে পারত তা বাদ দিয়ে", "উপহারের দাম", "শুধু পকেটের নগদের মূল্য", "পরের বছরের বেতন"],
        "এতে প্রকৌশলীরা আলাদা সময়ের খরচ আর লাভসহ প্রকল্প তুলনা করতে পারেন।"),
    mcq("Why is Rs 1 lakh received today worth more than Rs 1 lakh received in 3 years?", ["Today's money can be invested to earn interest, and prices may rise meanwhile", "Old notes are worth more", "Banks close after 3 years", "It is worth exactly the same"], 0,
        "This idea is called the time value of money.",
        "3 বছর পরে পাওয়া 1 লাখ টাকার চেয়ে আজ পাওয়া 1 লাখ টাকার দাম বেশি কেন?", ["আজকের টাকা বিনিয়োগ করে সুদ পাওয়া যায়, আর এর মধ্যে দাম বাড়তে পারে", "পুরোনো নোটের দাম বেশি", "3 বছর পরে ব্যাংক বন্ধ হয়", "হুবহু একই দাম"],
        "এই ভাবনাকে টাকার সময়-মূল্য বলে।"),
    mcq("What is 'scrap value' (residual value) of a machine?", ["What it can be sold for at the end of its useful life", "The cost of throwing it away", "Its price when new", "The cost of repairs"], 0,
        "Depreciation spreads cost minus scrap value over the years of use.",
        "যন্ত্রের 'শেষ মূল্য' (অবশিষ্ট মূল্য) কী?", ["কাজের জীবন শেষে যে দামে বেচা যায়", "ফেলে দেওয়ার খরচ", "নতুন অবস্থায় দাম", "মেরামতের খরচ"],
        "অবচয় দাম বিয়োগ শেষ মূল্যকে ব্যবহারের বছরগুলোয় ছড়িয়ে দেয়।"),
    mcq("Why do firms record depreciation even though no cash leaves the business that year?", ["It shows the true cost of wearing out equipment, so profits are not overstated", "To pay less salary", "Because cash is stolen", "It is a fine from the government"], 0,
        "It also reminds owners to save for replacements.",
        "সে বছর কোনো নগদ না বেরোলেও সংস্থা অবচয় লিখে রাখে কেন?", ["যন্ত্রপাতি ক্ষয়ে যাওয়ার আসল খরচ দেখায়, তাই লাভ বাড়িয়ে দেখানো হয় না", "কম বেতন দিতে", "নগদ চুরি হয় বলে", "সরকারের জরিমানা"],
        "মালিকদের বদলের জন্য সঞ্চয়ের কথাও মনে করায়।"),
    mcq("What is the difference between gross profit and net profit?", ["Gross profit is sales minus direct costs; net profit also takes off all other expenses", "They are the same", "Net profit is always bigger", "Gross profit includes taxes only"], 0,
        "A firm can have good gross profit but still lose money overall.",
        "মোট লাভ আর নিট লাভের পার্থক্য কী?", ["মোট লাভ = বিক্রি বিয়োগ প্রত্যক্ষ খরচ; নিট লাভে বাকি সব খরচও বাদ যায়", "দুটো একই", "নিট লাভ সবসময় বড়", "মোট লাভে শুধু কর ধরা থাকে"],
        "একটা সংস্থার মোট লাভ ভালো হলেও সামগ্রিকভাবে লোকসান হতে পারে।"),
    mcq("What is a 'profit and loss statement'?", ["A summary of a firm's income and expenses over a period, showing its profit or loss", "A list of the firm's buildings", "A bank's interest table", "A tax receipt"], 0,
        "Also called an income statement.",
        "'লাভ-ক্ষতির হিসাব' কী?", ["একটা সময়ে সংস্থার আয় আর খরচের সারাংশ, যা লাভ বা ক্ষতি দেখায়", "সংস্থার বাড়ির তালিকা", "ব্যাংকের সুদের তালিকা", "করের রসিদ"],
        "একে আয়-বিবরণীও বলে।"),
    mcq("What is a 'balance sheet'?", ["A snapshot of what a firm owns (assets) and owes (liabilities) on one date", "A list of daily sales", "A sheet for balancing beams", "A salary slip"], 0,
        "Assets = liabilities + owners' equity - it always balances.",
        "'উদ্বৃত্তপত্র' (ব্যালান্স শিট) কী?", ["একটা নির্দিষ্ট তারিখে সংস্থার কী আছে (সম্পদ) আর কী দেনা (দায়) তার ছবি", "দৈনিক বিক্রির তালিকা", "কড়ি সাম্যে রাখার কাগজ", "বেতনের স্লিপ"],
        "সম্পদ = দায় + মালিকের মূলধন - সবসময় মেলে।"),
    mcq("Why can a profitable construction firm still go bust?", ["It can run out of cash if clients pay late while wages and suppliers must be paid now", "Profit always means plenty of cash", "Banks close profitable firms", "Profit is illegal"], 0,
        "Cash flow, not just profit, keeps a business alive.",
        "লাভজনক নির্মাণ-সংস্থাও দেউলিয়া হতে পারে কেন?", ["গ্রাহক দেরিতে টাকা দিলে আর মজুরি ও সরবরাহকারীকে এখনই দিতে হলে নগদ ফুরিয়ে যেতে পারে", "লাভ মানেই প্রচুর নগদ", "ব্যাংক লাভজনক সংস্থা বন্ধ করে", "লাভ বেআইনি"],
        "শুধু লাভ নয়, নগদপ্রবাহই ব্যবসা বাঁচিয়ে রাখে।"),
    mcq("What is the 'contribution' of each product sold?", ["Selling price minus variable cost - the amount that goes towards fixed costs and then profit", "The total sales", "The tax paid", "A donation"], 0,
        "Break-even units = fixed costs ÷ contribution per unit.",
        "বিক্রি হওয়া প্রতিটা পণ্যের 'অবদান' কী?", ["বিক্রয়মূল্য বিয়োগ পরিবর্তনশীল খরচ - যা স্থির খরচ আর পরে লাভে যায়", "মোট বিক্রি", "দেওয়া কর", "দান"],
        "লাভ-লোকসান-সমান একক = স্থির খরচ ÷ এককপ্রতি অবদান।"),
    mcq("What is the 'margin of safety' in business?", ["How far sales can fall before the firm reaches break-even", "The safety rail on a bridge", "Extra stock in the warehouse", "Insurance cover"], 0,
        "Selling 1,500 units when break-even is 1,000 gives a margin of safety of 500 units.",
        "ব্যবসায় 'নিরাপত্তার ব্যবধান' কী?", ["লাভ-লোকসান সমান বিন্দুতে পৌঁছানোর আগে বিক্রি কতটা কমতে পারে", "সেতুর নিরাপত্তা-রেলিং", "গুদামের বাড়তি মজুত", "বিমার সুরক্ষা"],
        "লাভ-লোকসান-সমান 1,000 হলে 1,500 একক বেচলে ব্যবধান 500 একক।"),
    mcq("What does the RBI's 'repo rate' affect?", ["The rate at which banks borrow from the RBI, which pushes loan and deposit rates up or down", "The price of onions directly", "The number of bank branches", "Only foreign currency"], 0,
        "Raising it usually makes loans dearer and helps control inflation.",
        "আরবিআই-এর 'রেপো রেট' কীসে প্রভাব ফেলে?", ["যে হারে ব্যাংক আরবিআই-এর থেকে ধার নেয়, যা ঋণ আর আমানতের সুদ ওঠায়-নামায়", "সরাসরি পেঁয়াজের দাম", "ব্যাংক-শাখার সংখ্যা", "শুধু বিদেশি মুদ্রা"],
        "এটা বাড়ালে সাধারণত ঋণ দামি হয় আর মুদ্রাস্ফীতি নিয়ন্ত্রণে আসে।"),
    mcq("If interest rates rise, what usually happens to a builder's floating-rate loan EMI?", ["It goes up", "It goes down", "It disappears", "It never changes"], 0,
        "Fixed-rate loans protect against this, at a cost.",
        "সুদের হার বাড়লে একজন নির্মাতার ভাসমান-হারের ঋণের ইএমআই-এর সাধারণত কী হয়?", ["বাড়ে", "কমে", "মুছে যায়", "কখনো বদলায় না"],
        "স্থির-হারের ঋণ কিছু খরচে এর থেকে রক্ষা করে।"),
    mcq("What does a stock market index such as the Sensex or Nifty show?", ["The average movement of a group of large companies' share prices", "The price of one share", "The interest rate", "The number of investors"], 0,
        "It is a quick way to see how the market as a whole is doing.",
        "সেনসেক্স বা নিফটির মতো শেয়ার-বাজার সূচক কী দেখায়?", ["একদল বড় কোম্পানির শেয়ারের দামের গড় ওঠানামা", "একটা শেয়ারের দাম", "সুদের হার", "বিনিয়োগকারীর সংখ্যা"],
        "গোটা বাজার কেমন চলছে, দ্রুত দেখার উপায়।"),
    mcq("What is an IPO?", ["An initial public offering - when a company first sells shares to the public", "An international post office", "A type of loan", "A government tax"], 0,
        "Firms use IPOs to raise money for growth, such as building new plants.",
        "আইপিও কী?", ["প্রাথমিক গণ-প্রস্তাব - যখন একটা কোম্পানি প্রথমবার জনসাধারণকে শেয়ার বেচে", "আন্তর্জাতিক ডাকঘর", "এক রকম ঋণ", "সরকারি কর"],
        "নতুন কারখানা বানানোর মতো বৃদ্ধির জন্য সংস্থা আইপিও-তে টাকা তোলে।"),
    mcq("What is a 'bull market'?", ["A period when share prices are generally rising", "A cattle fair", "A period of falling prices", "A market that is closed"], 0,
        "A 'bear market' is the opposite - prices generally falling.",
        "'বুল মার্কেট' কী?", ["যে সময়ে শেয়ারের দাম সাধারণত বাড়ছে", "গবাদি পশুর মেলা", "দাম পড়ার সময়", "বন্ধ বাজার"],
        "'বেয়ার মার্কেট' উল্টো - দাম সাধারণত পড়ছে।"),
    mcq("What does a high P/E ratio usually suggest?", ["Investors expect strong future growth in the company's earnings", "The company is losing money", "The share is certainly cheap", "The company has no shareholders"], 0,
        "A high P/E can also mean the share is overpriced - it is a clue, not a guarantee.",
        "পি/ই অনুপাত বেশি হলে সাধারণত কী বোঝায়?", ["বিনিয়োগকারীরা কোম্পানির আয়ে ভবিষ্যতে জোরালো বৃদ্ধি আশা করেন", "কোম্পানি লোকসান করছে", "শেয়ারটা নিশ্চয়ই সস্তা", "কোম্পানির শেয়ারহোল্ডার নেই"],
        "বেশি পি/ই মানে শেয়ার অতিমূল্যায়িতও হতে পারে - এটা ইঙ্গিত, নিশ্চয়তা নয়।"),
    mcq("What is 'asset allocation'?", ["Dividing investments between types such as shares, bonds, gold and cash to balance risk and return", "Selling all assets", "Buying one share", "Counting tools in a store"], 0,
        "Younger savers often hold more shares; those near retirement more bonds.",
        "'সম্পদ বণ্টন' কী?", ["ঝুঁকি আর লাভের ভারসাম্যে বিনিয়োগকে শেয়ার, বন্ড, সোনা আর নগদের মতো ধরনে ভাগ করা", "সব সম্পদ বেচে দেওয়া", "একটা শেয়ার কেনা", "গুদামের যন্ত্র গোনা"],
        "অল্পবয়সী সঞ্চয়কারীরা প্রায়ই বেশি শেয়ার রাখেন; অবসরের কাছের মানুষ বেশি বন্ড।"),
    mcq("What is the difference between a direct tax and an indirect tax?", ["Direct tax is paid on income or wealth by the person; indirect tax is added to the price of goods and services", "They are the same", "Indirect tax is paid only by companies", "Direct tax is added at shops"], 0,
        "Income tax is direct; GST is indirect.",
        "প্রত্যক্ষ কর আর পরোক্ষ করের পার্থক্য কী?", ["প্রত্যক্ষ কর ব্যক্তি নিজের আয় বা সম্পদের উপর দেন; পরোক্ষ কর পণ্য-পরিষেবার দামে যোগ হয়", "দুটো একই", "পরোক্ষ কর শুধু কোম্পানি দেয়", "প্রত্যক্ষ কর দোকানে যোগ হয়"],
        "আয়কর প্রত্যক্ষ; জিএসটি পরোক্ষ।"),
    mcq("What does a 'progressive' income tax mean?", ["Higher slices of income are taxed at higher rates", "Everyone pays the same amount", "Poorer people pay more", "Tax falls as income rises"], 0,
        "It asks those who earn more to contribute a larger share.",
        "'প্রগতিশীল' আয়কর মানে কী?", ["আয়ের উঁচু ভাগে বেশি হারে কর", "সবাই সমান অঙ্ক দেন", "গরিবরা বেশি দেন", "আয় বাড়লে কর কমে"],
        "যাঁরা বেশি আয় করেন, তাঁদের বড় ভাগ দিতে বলে।"),
    mcq("What do taxes pay for that helps the building trade?", ["Public roads, bridges, schools and hospitals that firms build and use", "Only politicians' salaries", "Nothing useful", "Private holidays"], 0,
        "Honest tax payment keeps public works funded.",
        "কর থেকে কী খরচ হয় যা নির্মাণ-ব্যবসাকে সাহায্য করে?", ["সরকারি রাস্তা, সেতু, স্কুল আর হাসপাতাল, যা সংস্থাগুলো বানায় আর ব্যবহার করে", "শুধু রাজনীতিকদের বেতন", "কাজের কিছু না", "ব্যক্তিগত ছুটি"],
        "সৎভাবে কর দিলে সরকারি কাজের টাকা জোটে।"),
    mcq("What is 'tax evasion'?", ["Illegally hiding income or sales to avoid paying tax", "Legally claiming allowances", "Paying tax early", "Asking an accountant for advice"], 0,
        "It is a crime and shifts the burden onto honest taxpayers.",
        "'কর ফাঁকি' কী?", ["কর এড়াতে বেআইনিভাবে আয় বা বিক্রি লুকোনো", "আইনসম্মতভাবে ছাড় দাবি", "আগেভাগে কর দেওয়া", "হিসাবরক্ষকের পরামর্শ নেওয়া"],
        "এটা অপরাধ, আর বোঝা সৎ করদাতাদের উপর চাপায়।"),
    mcq("What is a home loan (mortgage)?", ["A long-term loan to buy property, secured on that property", "A loan for groceries", "Rent paid to a landlord", "A government grant"], 0,
        "If repayments stop, the lender can take the house.",
        "গৃহঋণ (বন্ধকী ঋণ) কী?", ["সম্পত্তি কিনতে দীর্ঘমেয়াদি ঋণ, সেই সম্পত্তিকেই জামানত রেখে", "মুদিখানার ঋণ", "বাড়িওয়ালাকে দেওয়া ভাড়া", "সরকারি অনুদান"],
        "কিস্তি বন্ধ হলে ঋণদাতা বাড়ি নিয়ে নিতে পারেন।"),
    mcq("What is the difference between a secured and an unsecured loan?", ["A secured loan is backed by an asset the lender can take; an unsecured one is not, so it usually costs more", "Unsecured loans are always free", "Secured loans have no interest", "There is no difference"], 0,
        "Personal loans and credit cards are unsecured; home and vehicle loans are secured.",
        "জামানতযুক্ত আর জামানতহীন ঋণের পার্থক্য কী?", ["জামানতযুক্ত ঋণের পিছনে এমন সম্পদ থাকে যা ঋণদাতা নিতে পারেন; জামানতহীনে থাকে না, তাই সাধারণত দামি", "জামানতহীন ঋণ সবসময় বিনামূল্যে", "জামানতযুক্ত ঋণে সুদ নেই", "কোনো পার্থক্য নেই"],
        "ব্যক্তিগত ঋণ আর ক্রেডিট-কার্ড জামানতহীন; গৃহ আর গাড়ির ঋণ জামানতযুক্ত।"),
    mcq("What is 'loan-to-value' (LTV) on a home loan?", ["The loan as a percentage of the property's value", "The interest rate", "The length of the loan", "The house's size"], 0,
        "A Rs 40 lakh loan on a Rs 50 lakh home is an LTV of 80%.",
        "গৃহঋণে 'ঋণ-মূল্য অনুপাত' (এলটিভি) কী?", ["সম্পত্তির মূল্যের শতাংশে ঋণ", "সুদের হার", "ঋণের মেয়াদ", "বাড়ির মাপ"],
        "50 লাখ টাকার বাড়িতে 40 লাখের ঋণ মানে এলটিভি 80%।"),
    mcq("What is 'microfinance'?", ["Small loans and savings services for people with low incomes, often through self-help groups", "Very tiny banknotes", "Loans for microchips only", "A bank for children"], 0,
        "It helps small traders and artisans start or grow a business.",
        "'ক্ষুদ্রঋণ' কী?", ["কম আয়ের মানুষের জন্য ছোট ঋণ আর সঞ্চয়-পরিষেবা, প্রায়ই স্বনির্ভর দলের মাধ্যমে", "খুব ছোট নোট", "শুধু মাইক্রোচিপের ঋণ", "শিশুদের ব্যাংক"],
        "ছোট ব্যবসায়ী আর কারিগরদের ব্যবসা শুরু বা বাড়াতে সাহায্য করে।"),
    mcq("How does a self-help group (SHG) usually work?", ["Members save small amounts together and lend to each other, building trust and credit", "One member keeps all the money", "The government pays every member's bills", "Members only meet to play games"], 0,
        "Many SHGs later get bank loans as a group.",
        "স্বনির্ভর দল (এসএইচজি) সাধারণত কীভাবে চলে?", ["সদস্যরা একসঙ্গে অল্প অল্প জমান আর পরস্পরকে ধার দেন, আস্থা আর ঋণযোগ্যতা গড়েন", "একজন সব টাকা রাখেন", "সরকার প্রত্যেকের বিল দেয়", "সদস্যরা শুধু খেলতে মিলিত হন"],
        "অনেক দল পরে দল হিসেবে ব্যাংক-ঋণ পায়।"),
    mcq("What is the Public Provident Fund (PPF)?", ["A long-term government-backed savings scheme with tax benefits", "A loan for public works", "A share in a company", "A fund for buying bridges"], 0,
        "It has a 15-year lock-in, so it suits long-term goals.",
        "পাবলিক প্রভিডেন্ট ফান্ড (পিপিএফ) কী?", ["করছাড়সহ সরকার-সমর্থিত দীর্ঘমেয়াদি সঞ্চয়-প্রকল্প", "সরকারি কাজের ঋণ", "কোম্পানির শেয়ার", "সেতু কেনার তহবিল"],
        "15 বছরের আটকানো মেয়াদ, তাই দীর্ঘমেয়াদি লক্ষ্যে মানানসই।"),
    mcq("Why should workers think about a pension early in their career?", ["Small regular contributions grow for decades and provide income in old age", "Pensions are only for the rich", "Old age never comes", "It is illegal to save for later"], 0,
        "Schemes like the NPS and EPF help build retirement savings.",
        "কর্মজীবনের শুরুতেই কর্মীদের পেনশন নিয়ে ভাবা উচিত কেন?", ["ছোট নিয়মিত জমা কয়েক দশক ধরে বেড়ে বৃদ্ধ বয়সে আয় দেয়", "পেনশন শুধু ধনীদের", "বৃদ্ধ বয়স আসে না", "পরে জন্য জমানো বেআইনি"],
        "এনপিএস আর ইপিএফ-এর মতো প্রকল্প অবসরের সঞ্চয় গড়তে সাহায্য করে।"),
    mcq("What is the Employees' Provident Fund (EPF)?", ["A savings fund where both the worker and employer contribute part of the salary each month", "A loan from a shop", "A bonus paid once", "A bank fee"], 0,
        "Registered construction workers can benefit from it.",
        "কর্মচারী ভবিষ্যনিধি (ইপিএফ) কী?", ["সঞ্চয়-তহবিল, যেখানে কর্মী আর নিয়োগকর্তা দুজনেই প্রতি মাসে বেতনের একটা অংশ জমা দেন", "দোকানের ঋণ", "একবারের বোনাস", "ব্যাংকের ফি"],
        "নিবন্ধিত নির্মাণ-শ্রমিকরা এর সুবিধা পেতে পারেন।"),
    mcq("What are Sovereign Gold Bonds?", ["Government bonds linked to the gold price that also pay interest", "Gold coins sold in shops", "A gold mine", "A tax on gold"], 0,
        "They avoid the worry of storing physical gold safely.",
        "সার্বভৌম স্বর্ণ-বন্ড কী?", ["সোনার দামের সঙ্গে যুক্ত সরকারি বন্ড, যা সুদও দেয়", "দোকানে বিক্রি হওয়া সোনার মুদ্রা", "সোনার খনি", "সোনার উপর কর"],
        "আসল সোনা নিরাপদে রাখার চিন্তা থাকে না।"),
    mcq("A village crowdfunds Rs 6 lakh for a footbridge from 1,200 online donors. What is the average gift?", ["Rs 500", "Rs 5,000", "Rs 50", "Rs 200"], 0,
        "6,00,000 ÷ 1,200 = Rs 500. Many small gifts can build something big.",
        "একটা গ্রাম পায়ে-চলা সেতুর জন্য 1,200 জন অনলাইন দাতার থেকে 6 লাখ টাকা গণ-অর্থায়নে তুলল। গড় দান কত?", ["500 টাকা", "5,000 টাকা", "50 টাকা", "200 টাকা"],
        "6,00,000 ÷ 1,200 = 500 টাকা। অনেক ছোট দানে বড় কিছু গড়া যায়।"),
    mcq("What is 'term life insurance'?", ["Cover that pays the family a fixed sum if the insured person dies within the term, with no savings part", "Insurance for a school term", "A savings account", "Insurance for tools only"], 0,
        "It is the cheapest way for a worker to protect their family.",
        "'মেয়াদি জীবনবিমা' কী?", ["মেয়াদের মধ্যে বিমাকৃত ব্যক্তি মারা গেলে পরিবার নির্দিষ্ট অঙ্ক পায়, সঞ্চয়ের অংশ নেই", "স্কুলের এক পর্বের বিমা", "সঞ্চয়-অ্যাকাউন্ট", "শুধু যন্ত্রের বিমা"],
        "একজন কর্মীর পরিবারকে রক্ষার এটাই সবচেয়ে সস্তা উপায়।"),
    mcq("Why should a self-employed welder have health insurance?", ["A hospital stay could wipe out years of savings; insurance covers most of the bill", "Hospitals are free for welders", "Welders never get ill", "It increases their wages"], 0,
        "Schemes like Ayushman Bharat help families with low incomes.",
        "একজন স্বনিযুক্ত ঝালাইকারের স্বাস্থ্যবিমা থাকা উচিত কেন?", ["হাসপাতালে থাকলে বছরের সঞ্চয় শেষ হতে পারে; বিমা বিলের বেশিরভাগ মেটায়", "ঝালাইকারদের জন্য হাসপাতাল বিনামূল্যে", "ঝালাইকাররা অসুস্থ হন না", "মজুরি বাড়ায়"],
        "আয়ুষ্মান ভারতের মতো প্রকল্প কম আয়ের পরিবারকে সাহায্য করে।"),
    mcq("What is a 'no-claim bonus' on vehicle insurance?", ["A discount on next year's premium for not making a claim", "A prize for crashing", "A refund of all premiums", "A fine for late payment"], 0,
        "Careful driving of site vans saves money year after year.",
        "গাড়ির বিমায় 'দাবিহীন বোনাস' কী?", ["দাবি না করলে পরের বছরের প্রিমিয়ামে ছাড়", "ধাক্কা লাগানোর পুরস্কার", "সব প্রিমিয়াম ফেরত", "দেরিতে দেওয়ার জরিমানা"],
        "সাবধানে নির্মাণস্থলের ভ্যান চালালে বছরের পর বছর টাকা বাঁচে।"),
    mcq("A warehouse worth Rs 50 lakh is insured for only Rs 25 lakh. A fire causes Rs 10 lakh of damage. Why might the insurer pay only about Rs 5 lakh?", ["It is underinsured by half, so claims are often cut in the same proportion", "Insurers never pay for fire", "Rs 5 lakh is the maximum for any claim", "Fire damage is always halved"], 0,
        "Insure for the full replacement value.",
        "50 লাখ টাকার একটা গুদাম মাত্র 25 লাখ টাকায় বিমা করা। আগুনে 10 লাখ টাকার ক্ষতি হলো। বিমাকারী মাত্র প্রায় 5 লাখ টাকা দিতে পারেন কেন?", ["অর্ধেক কম বিমা, তাই দাবিও প্রায়ই একই অনুপাতে কমে", "বিমাকারী আগুনের জন্য দেন না", "যেকোনো দাবির সর্বোচ্চ 5 লাখ", "আগুনের ক্ষতি সবসময় অর্ধেক হয়"],
        "পুরো প্রতিস্থাপন-মূল্যে বিমা করো।"),
    mcq("A builder pays suppliers after 30 days but clients pay the builder after 90 days. For how many days must the builder finance the gap?", ["60 days", "120 days", "30 days", "90 days"], 0,
        "90 - 30 = 60 days of cash must come from savings or a loan.",
        "একজন নির্মাতা সরবরাহকারীদের 30 দিন পরে টাকা দেন, কিন্তু গ্রাহকরা তাঁকে দেন 90 দিন পরে। কত দিনের ফাঁক নির্মাতাকে অর্থায়ন করতে হবে?", ["60 দিন", "120 দিন", "30 দিন", "90 দিন"],
        "90 - 30 = 60 দিনের নগদ সঞ্চয় বা ঋণ থেকে আসতে হবে।"),
    mcq("What is 'invoice discounting' (factoring)?", ["Getting cash now from a finance firm against unpaid invoices, for a fee", "Giving customers a discount", "Tearing up old invoices", "A tax on invoices"], 0,
        "It eases cash flow when clients pay slowly.",
        "'চালান-বাট্টা' (ফ্যাক্টরিং) কী?", ["না-মেটানো চালানের বদলে ফি দিয়ে অর্থ-সংস্থা থেকে এখনই নগদ পাওয়া", "গ্রাহককে ছাড় দেওয়া", "পুরোনো চালান ছিঁড়ে ফেলা", "চালানের উপর কর"],
        "গ্রাহক ধীরে টাকা দিলে নগদপ্রবাহ সহজ করে।"),
    mcq("What does a 'letter of credit' from a bank do in international trade?", ["The bank promises to pay the seller once the agreed shipping documents are presented", "It is a thank-you letter", "It gives the buyer free goods", "It replaces customs duty"], 0,
        "It builds trust between buyers and sellers who have never met.",
        "আন্তর্জাতিক বাণিজ্যে ব্যাংকের 'ঋণপত্র' (লেটার অফ ক্রেডিট) কী করে?", ["ঠিক করা জাহাজি নথি দেখালে বিক্রেতাকে টাকা দেওয়ার ব্যাংকের প্রতিশ্রুতি", "ধন্যবাদের চিঠি", "ক্রেতাকে বিনামূল্যে মাল দেয়", "শুল্কের বদলি"],
        "কখনো দেখা হয়নি এমন ক্রেতা-বিক্রেতার মধ্যে আস্থা গড়ে।"),
    mcq("An importer of bridge bearings agrees today to buy dollars at a fixed rate in 3 months. Why?", ["To protect against the rupee weakening and the bearings costing more", "To make the bearings arrive faster", "Because dollars are free in 3 months", "To avoid paying the supplier"], 0,
        "This is called hedging - it trades possible gains for certainty.",
        "সেতু-বিয়ারিংয়ের একজন আমদানিকারক আজই 3 মাস পরের জন্য নির্দিষ্ট হারে ডলার কেনার চুক্তি করলেন। কেন?", ["টাকা দুর্বল হয়ে বিয়ারিংয়ের দাম বেড়ে যাওয়া থেকে রক্ষা পেতে", "বিয়ারিং তাড়াতাড়ি আনতে", "কারণ 3 মাস পরে ডলার বিনামূল্যে", "সরবরাহকারীকে টাকা না দিতে"],
        "একে হেজিং বলে - সম্ভাব্য লাভের বদলে নিশ্চয়তা কেনা।"),
    mcq("Which of these can be turned into cash most quickly without losing value?", ["Money in a savings account", "A plot of land", "A used crane", "A 15-year PPF account"], 0,
        "Keep emergency money in liquid forms like this.",
        "এদের মধ্যে কোনটা মূল্য না হারিয়ে সবচেয়ে দ্রুত নগদে বদলানো যায়?", ["সঞ্চয়-অ্যাকাউন্টের টাকা", "এক টুকরো জমি", "পুরোনো ক্রেন", "15 বছরের পিপিএফ অ্যাকাউন্ট"],
        "জরুরি টাকা এমন তরল রূপে রাখো।"),
    mcq("A Rs 2 lakh fixed deposit earns 7% interest in a year. The bank deducts 10% TDS on the interest. How much TDS is deducted?", ["Rs 1,400", "Rs 14,000", "Rs 20,000", "Rs 700"], 0,
        "Interest = 2,00,000 x 7% = 14,000; TDS = 10% of 14,000 = Rs 1,400.",
        "2 লাখ টাকার স্থায়ী আমানতে বছরে 7% সুদ। ব্যাংক সুদের উপর 10% টিডিএস কাটে। কত টিডিএস কাটা হয়?", ["1,400 টাকা", "14,000 টাকা", "20,000 টাকা", "700 টাকা"],
        "সুদ = 2,00,000 x 7% = 14,000; টিডিএস = 14,000-এর 10% = 1,400 টাকা।"),
    mcq("What happens when a cheque 'bounces'?", ["The bank refuses to pay it, usually because the account lacks funds - and penalties can follow", "It is paid twice", "It is paid in coins", "It turns into cash automatically"], 0,
        "In India a bounced cheque can even lead to a court case.",
        "চেক 'বাউন্স' করলে কী হয়?", ["ব্যাংক টাকা দিতে অস্বীকার করে, সাধারণত অ্যাকাউন্টে টাকা না থাকায় - আর জরিমানা হতে পারে", "দুবার টাকা মেলে", "খুচরো পয়সায় মেলে", "নিজে থেকে নগদ হয়ে যায়"],
        "ভারতে চেক বাউন্স থেকে মামলাও হতে পারে।"),
    mcq("Why are UPI and bank transfers useful for a small contractor's record-keeping?", ["Each payment leaves an automatic digital record with date and amount", "They hide payments from the tax office", "They never need receipts for anything", "They are only for shopping"], 0,
        "Good records make tax returns, loans and disputes much easier.",
        "ছোট ঠিকাদারের হিসাব রাখায় ইউপিআই আর ব্যাংক-স্থানান্তর কাজের কেন?", ["প্রতিটা লেনদেন তারিখ আর অঙ্কসহ নিজে থেকে ডিজিটাল নথি রেখে যায়", "কর-দপ্তর থেকে লেনদেন লুকোয়", "কিছুতেই রসিদ লাগে না", "শুধু কেনাকাটার জন্য"],
        "ভালো নথি কর-রিটার্ন, ঋণ আর বিবাদ অনেক সহজ করে।"),
    mcq("What is an 'audit trail'?", ["A chain of records showing each step of a transaction, from order to payment", "A walking path for auditors", "A list of trees", "A bridge inspection route"], 0,
        "It lets anyone check that public money was spent properly.",
        "'নিরীক্ষা-সূত্র' (অডিট ট্রেল) কী?", ["অর্ডার থেকে পেমেন্ট পর্যন্ত লেনদেনের প্রতি ধাপের নথির শৃঙ্খল", "নিরীক্ষকদের হাঁটার পথ", "গাছের তালিকা", "সেতু-পরিদর্শনের পথ"],
        "এতে যে কেউ যাচাই করতে পারে সরকারি টাকা ঠিকভাবে খরচ হয়েছে কিনা।"),
    mcq("Why does a bank ask to see a construction firm's last three years of accounts before lending?", ["To judge whether the firm earns steadily enough to repay", "To copy its designs", "To count its workers' birthdays", "Banks never ask for accounts"], 0,
        "Steady, well-kept accounts make borrowing easier and cheaper.",
        "ঋণ দেওয়ার আগে ব্যাংক একটা নির্মাণ-সংস্থার শেষ তিন বছরের হিসাব দেখতে চায় কেন?", ["সংস্থা শোধ করার মতো স্থিরভাবে আয় করে কিনা বিচার করতে", "নকশা নকল করতে", "কর্মীদের জন্মদিন গুনতে", "ব্যাংক কখনো হিসাব চায় না"],
        "স্থির, যত্নে রাখা হিসাব ঋণ নেওয়া সহজ আর সস্তা করে।"),
    mcq("What is 'ESG' or ethical investing?", ["Choosing investments by how companies treat the environment, people and governance, not only profit", "Investing only in the cheapest shares", "Investing in one country", "Avoiding all investment"], 0,
        "Many investors now check a builder's safety and pollution record.",
        "'ইএসজি' বা নৈতিক বিনিয়োগ কী?", ["শুধু লাভ নয়, কোম্পানি পরিবেশ, মানুষ আর পরিচালনার সঙ্গে কেমন আচরণ করে দেখে বিনিয়োগ বাছা", "শুধু সবচেয়ে সস্তা শেয়ারে বিনিয়োগ", "এক দেশে বিনিয়োগ", "সব বিনিয়োগ এড়ানো"],
        "অনেক বিনিয়োগকারী এখন নির্মাতার নিরাপত্তা আর দূষণের রেকর্ড দেখেন।"),
    mcq("In India, why do some donors give to registered charities under section 80G?", ["Part of the donation can be deducted from taxable income", "It doubles the donation automatically", "It makes the donor a government official", "It is required by law for everyone"], 0,
        "Always check a charity is registered before giving real money.",
        "ভারতে কিছু দাতা 80G ধারায় নিবন্ধিত দাতব্য-সংস্থাকে দান করেন কেন?", ["দানের একটা অংশ করযোগ্য আয় থেকে বাদ দেওয়া যায়", "দান নিজে থেকে দ্বিগুণ হয়", "দাতা সরকারি কর্মকর্তা হয়ে যান", "আইনে সবার জন্য বাধ্যতামূলক"],
        "আসল টাকা দেওয়ার আগে সবসময় দেখো দাতব্য-সংস্থা নিবন্ধিত কিনা।"),
    mcq("What makes a financial goal 'SMART'?", ["Specific, measurable, achievable, relevant and time-bound", "Secret, magic, automatic, random and tiny", "Spending more and returning tomorrow", "Saving money at random times"], 0,
        "'Save Rs 30,000 for a welding course by next June' is SMART.",
        "আর্থিক লক্ষ্যকে কী 'স্মার্ট' করে?", ["নির্দিষ্ট, মাপা যায়, অর্জনযোগ্য, প্রাসঙ্গিক আর সময়-বাঁধা", "গোপন, জাদুকরী, স্বয়ংক্রিয়, এলোমেলো আর খুদে", "বেশি খরচ করে কাল ফেরত", "এলোমেলো সময়ে টাকা জমানো"],
        "'পরের জুনের মধ্যে ঝালাই-কোর্সের জন্য 30,000 টাকা জমাও' স্মার্ট লক্ষ্য।"),
    mcq("What is a 'budget deficit' for a government?", ["Spending more than it collects in revenue in a year", "Collecting more than it spends", "A balanced budget", "A list of bridges"], 0,
        "Deficits are covered by borrowing, which must be repaid with interest.",
        "সরকারের 'বাজেট ঘাটতি' কী?", ["এক বছরে যত আয় তার চেয়ে বেশি খরচ", "খরচের চেয়ে বেশি আয়", "সুষম বাজেট", "সেতুর তালিকা"],
        "ঘাটতি ঋণে মেটে, যা সুদসহ শোধ করতে হয়।"),
    mcq("Why might a government spend more on bridges and roads during a slowdown?", ["It creates jobs and orders for firms, boosting the economy, while leaving useful assets", "To use up all its money", "Because bridges are cheaper in slowdowns only", "To raise unemployment"], 0,
        "This is one tool of fiscal policy.",
        "মন্দার সময় সরকার সেতু আর রাস্তায় বেশি খরচ করতে পারে কেন?", ["কাজ আর সংস্থার অর্ডার তৈরি হয়, অর্থনীতি চাঙ্গা হয়, আবার কাজের সম্পদও থাকে", "সব টাকা খরচ করে ফেলতে", "কারণ মন্দাতেই শুধু সেতু সস্তা", "বেকারত্ব বাড়াতে"],
        "এটা রাজস্ব-নীতির একটা হাতিয়ার।"),
    mcq("What is a 'municipal bond'?", ["A bond issued by a city to raise money for local projects like water supply or flyovers", "A bond between two cities", "A type of glue", "A bank account for children"], 0,
        "Investors earn interest; the city repays from its revenues.",
        "'পৌর-বন্ড' কী?", ["জল-সরবরাহ বা উড়ালপুলের মতো স্থানীয় প্রকল্পের টাকা তুলতে শহরের ছাড়া বন্ড", "দুই শহরের বন্ধন", "এক রকম আঠা", "শিশুদের ব্যাংক-অ্যাকাউন্ট"],
        "বিনিয়োগকারীরা সুদ পান; শহর তার আয় থেকে শোধ করে।"),
    mcq("A toll bridge earns Rs 2 crore a year. Its loan needs Rs 1.6 crore a year in repayments. What is the debt service coverage ratio (DSCR)?", ["1.25", "0.8", "3.6", "0.4"], 0,
        "DSCR = income available ÷ debt payments = 2 ÷ 1.6 = 1.25. Lenders like it comfortably above 1.",
        "একটা টোল-সেতু বছরে 2 কোটি টাকা আয় করে। এর ঋণে বছরে 1.6 কোটি টাকা শোধ লাগে। ঋণ-পরিশোধ আচ্ছাদন অনুপাত (ডিএসসিআর) কত?", ["1.25", "0.8", "3.6", "0.4"],
        "ডিএসসিআর = উপলব্ধ আয় ÷ ঋণ-শোধ = 2 ÷ 1.6 = 1.25। ঋণদাতারা এটা স্বচ্ছন্দে 1-এর উপরে চান।"),
    mcq("What does it mean if a project's DSCR is below 1?", ["Its income does not cover its loan repayments", "It is very profitable", "It has no debt", "It has too much cash"], 0,
        "The owners would have to find extra money or renegotiate the loan.",
        "একটা প্রকল্পের ডিএসসিআর 1-এর নিচে হলে মানে কী?", ["আয় দিয়ে ঋণ-শোধ মেটে না", "খুব লাভজনক", "কোনো ঋণ নেই", "অনেক বেশি নগদ"],
        "মালিকদের বাড়তি টাকা জোগাড় বা ঋণের শর্ত বদলাতে হবে।"),
    mcq("Why should a young worker read the terms before signing a loan agreement?", ["Hidden fees, penalties and variable rates can make a loan far more expensive than it looks", "Reading slows the bank down", "Loans have no terms", "Signing first is always safer"], 0,
        "Ask questions and get a copy of everything you sign.",
        "ঋণ-চুক্তিতে সই করার আগে একজন তরুণ কর্মীর শর্ত পড়া উচিত কেন?", ["লুকোনো ফি, জরিমানা আর পরিবর্তনশীল হার ঋণকে দেখতে যা মনে হয় তার চেয়ে অনেক দামি করতে পারে", "পড়লে ব্যাংকের দেরি হয়", "ঋণের কোনো শর্ত নেই", "আগে সই করা সবসময় নিরাপদ"],
        "প্রশ্ন করো আর সই করা সবকিছুর কপি রাখো।"),
    mcq("A friend offers to 'double your money in 30 days' through a new app. What should you suspect?", ["A scam - genuine investments cannot promise such huge, quick, guaranteed returns", "A great bank deal", "A government scheme", "A normal savings rate"], 0,
        "Check whether the firm is registered with SEBI or the RBI before investing anything.",
        "একজন বন্ধু নতুন অ্যাপে '30 দিনে টাকা দ্বিগুণ' করার প্রস্তাব দিলেন। কী সন্দেহ করা উচিত?", ["প্রতারণা - আসল বিনিয়োগ এত বড়, দ্রুত, নিশ্চিত লাভের প্রতিশ্রুতি দিতে পারে না", "ব্যাংকের দারুণ চুক্তি", "সরকারি প্রকল্প", "সাধারণ সঞ্চয়ের হার"],
        "কিছু বিনিয়োগের আগে দেখো সংস্থাটা সেবি বা আরবিআই-তে নিবন্ধিত কিনা।"),
    mcq("What is 'identity theft'?", ["Someone using your personal details to borrow money or buy things in your name", "Losing your ID card at home", "Changing your name legally", "Forgetting your password"], 0,
        "Keep Aadhaar, PAN and bank details private and shred old documents.",
        "'পরিচয় চুরি' কী?", ["কেউ তোমার ব্যক্তিগত তথ্য দিয়ে তোমার নামে ধার নেয় বা জিনিস কেনে", "বাড়িতে পরিচয়পত্র হারানো", "আইনত নাম বদলানো", "পাসওয়ার্ড ভুলে যাওয়া"],
        "আধার, প্যান আর ব্যাংকের তথ্য গোপন রাখো আর পুরোনো কাগজ কুচিয়ে ফেলো।"),
    mcq("Why is it wise to check your bank statement every month?", ["To spot mistakes or unknown payments quickly and report them", "Banks charge for not reading it", "To make the balance grow", "It is not useful"], 0,
        "Fraud reported fast is far easier to reverse.",
        "প্রতি মাসে ব্যাংকের বিবরণী দেখা বুদ্ধিমানের কাজ কেন?", ["ভুল বা অচেনা লেনদেন তাড়াতাড়ি ধরে জানাতে", "না পড়লে ব্যাংক টাকা কাটে", "জমা বাড়াতে", "কাজের নয়"],
        "তাড়াতাড়ি জানালে প্রতারণা ফেরানো অনেক সহজ।"),
    mcq("A contractor offers a discount if paid in cash 'without a bill'. Why is this a bad idea?", ["It helps evade tax, leaves you no proof of payment and no warranty", "Cash is illegal", "Bills are always wrong", "Discounts are never real"], 0,
        "Always get a proper GST invoice for building work.",
        "একজন ঠিকাদার 'বিল ছাড়া' নগদে দিলে ছাড় দিতে চাইলেন। এটা খারাপ ভাবনা কেন?", ["কর ফাঁকিতে সাহায্য করে, তোমার কাছে দেওয়ার প্রমাণ বা ওয়ারেন্টি থাকে না", "নগদ বেআইনি", "বিল সবসময় ভুল", "ছাড় কখনো সত্যি নয়"],
        "নির্মাণ-কাজে সবসময় সঠিক জিএসটি চালান নাও।"),
    mcq("A small firm's bank offers an overdraft at 15% and a supplier offers 60 days' interest-free credit. Which is cheaper for buying steel?", ["The supplier's interest-free credit, if paid within 60 days", "The overdraft", "They cost the same", "Neither can be used"], 0,
        "Free credit used wisely is the cheapest finance - but missing the deadline may bring penalties.",
        "একটা ছোট সংস্থার ব্যাংক 15%-এ ওভারড্রাফট দেয় আর সরবরাহকারী 60 দিনের সুদহীন ধার দেন। ইস্পাত কিনতে কোনটা সস্তা?", ["সরবরাহকারীর সুদহীন ধার, যদি 60 দিনের মধ্যে শোধ হয়", "ওভারড্রাফট", "দুটোর খরচ সমান", "কোনোটাই ব্যবহার করা যায় না"],
        "বুদ্ধি করে ব্যবহার করলে বিনা সুদের ধারই সবচেয়ে সস্তা অর্থায়ন - তবে সময়সীমা পেরোলে জরিমানা লাগতে পারে।"),
    mcq("What is a 'performance bonus' on a bridge contract?", ["Extra payment for finishing early or exceeding agreed quality targets", "A fine for late work", "A loan from the client", "A tax refund"], 0,
        "It rewards good work, just as penalties discourage delays.",
        "সেতু-চুক্তিতে 'কাজ-সম্পাদনের বোনাস' কী?", ["আগে শেষ করা বা ঠিক করা মানের লক্ষ্য ছাড়ানোর জন্য বাড়তি টাকা", "দেরির জরিমানা", "গ্রাহকের ঋণ", "করের ফেরত"],
        "জরিমানা যেমন দেরি ঠেকায়, বোনাস তেমনি ভালো কাজের পুরস্কার দেয়।"),
    mcq("In BridgeWorks, a Class 8 correct first answer earns Rs 8,000 as a Civil Grant. How many such answers fund a Rs 40,000 shortfall?", ["5", "8", "4", "40"], 0,
        "40,000 ÷ 8,000 = 5 - learning really does build bridges here.",
        "BridgeWorks-এ ক্লাস 8-এর প্রথম চেষ্টায় সঠিক উত্তরে 8,000 টাকার সিভিল গ্রান্ট মেলে। 40,000 টাকার ঘাটতি মেটাতে এমন কটা উত্তর লাগবে?", ["5", "8", "4", "40"],
        "40,000 ÷ 8,000 = 5 - এখানে শেখা সত্যিই সেতু গড়ে।"),
)
