"""Class 9 - Finance (Bridge Engineer cadet): balance sheets and the accounting equation, current
ratio, gearing, return on capital employed, earnings per share and dividends, retained profit,
reducing-balance depreciation, compounding more than once a year, payroll deductions, cash-flow
forecasts, and reading company accounts honestly."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 100, r * 2, r + 10):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def _rs(q_en, q_bn, r, ex_en, ex_bn, alts, unit_en="", unit_bn=""):
    o = _o(r, *alts)
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    return mcq(q_en, [f"Rs {f(x)}{unit_en}" for x in o], 0, ex_en, q_bn, [f"{f(x)}{unit_bn} টাকা" for x in o], ex_bn)


def _num(q_en, q_bn, r, ex_en, ex_bn, alts, u=""):
    o = _o(r, *alts)
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    return mcq(q_en, [f"{f(x)}{u}" for x in o], 0, ex_en, q_bn, [f"{f(x)}{u}" for x in o], ex_bn)


def equity(assets, liab):
    r = assets - liab
    return _rs(f"A bridge contractor has assets of Rs {assets:,} lakh and liabilities of Rs {liab:,} lakh. What is the owners' equity?",
               f"একজন সেতু-ঠিকাদারের সম্পদ {assets:,} লাখ টাকা আর দায় {liab:,} লাখ টাকা। মালিকের মূলধন কত?", r,
               f"Assets = liabilities + equity, so equity = {assets:,} - {liab:,} = Rs {r:,} lakh.",
               f"সম্পদ = দায় + মূলধন, তাই মূলধন = {assets:,} - {liab:,} = {r:,} লাখ টাকা।",
               (assets + liab, liab, _c(assets / liab) if assets // liab != r else r + 7), " lakh", " লাখ")


def current(ca, cl):
    r = _c(ca / cl)
    return _num(f"A firm has current assets of Rs {ca:,} lakh and current liabilities of Rs {cl:,} lakh. What is its current ratio?",
                f"একটা সংস্থার চলতি সম্পদ {ca:,} লাখ টাকা আর চলতি দায় {cl:,} লাখ টাকা। চলতি অনুপাত কত?", r,
                f"Current ratio = current assets ÷ current liabilities = {ca:,} ÷ {cl:,} = {r:g}. Around 1.5-2 is usually comfortable.",
                f"চলতি অনুপাত = চলতি সম্পদ ÷ চলতি দায় = {ca:,} ÷ {cl:,} = {r:g}। সাধারণত 1.5-2-এর আশপাশে স্বচ্ছন্দ।",
                (_c(cl / ca), ca - cl, _c(r * 10)))


def gearing(debt, eq):
    r = _c(debt * 100 / (debt + eq))
    return _num(f"A construction company has long-term loans of Rs {debt:,} crore and shareholders' equity of Rs {eq:,} crore. What is its gearing?",
                f"একটা নির্মাণ-কোম্পানির দীর্ঘমেয়াদি ঋণ {debt:,} কোটি টাকা আর শেয়ারহোল্ডারদের মূলধন {eq:,} কোটি টাকা। এর গিয়ারিং কত?", r,
                f"Gearing = debt ÷ (debt + equity) x 100 = {debt:,} ÷ {debt + eq:,} x 100 = {r:g}%. High gearing means more risk if profits fall.",
                f"গিয়ারিং = ঋণ ÷ (ঋণ + মূলধন) x 100 = {debt:,} ÷ {debt + eq:,} x 100 = {r:g}%। বেশি গিয়ারিং মানে লাভ কমলে বেশি ঝুঁকি।",
                (_c(debt * 100 / eq), _c(eq * 100 / (debt + eq)), _c(r / 2)), "%")


def roce(profit, capital):
    r = _c(profit * 100 / capital)
    return _num(f"A fabrication firm makes an operating profit of Rs {profit:,} lakh using capital of Rs {capital:,} lakh. What is its return on capital employed (ROCE)?",
                f"একটা ফ্যাব্রিকেশন-সংস্থা {capital:,} লাখ টাকা মূলধনে {profit:,} লাখ টাকা পরিচালন-লাভ করে। নিযুক্ত মূলধনে লাভের হার (আরওসিই) কত?", r,
                f"ROCE = {profit:,} ÷ {capital:,} x 100 = {r:g}%. Compare it with the interest a bank would pay.",
                f"আরওসিই = {profit:,} ÷ {capital:,} x 100 = {r:g}%। ব্যাংক যে সুদ দিত তার সঙ্গে তুলনা করো।",
                (_c(capital / profit), _c(profit * 10 / capital), _c(r + 5)), "%")


def eps(profit, shares):
    r = _c(profit / shares)
    return _rs(f"A listed builder earns a profit after tax of Rs {profit:,} crore and has {shares:,} crore shares. What are its earnings per share?",
               f"একটা তালিকাভুক্ত নির্মাতার কর-পরবর্তী লাভ {profit:,} কোটি টাকা আর শেয়ার {shares:,} কোটি। শেয়ারপ্রতি আয় কত?", r,
               f"EPS = profit ÷ number of shares = {profit:,} ÷ {shares:,} = Rs {r:g}.",
               f"শেয়ারপ্রতি আয় = লাভ ÷ শেয়ারের সংখ্যা = {profit:,} ÷ {shares:,} = {r:g} টাকা।",
               (_c(shares / profit * 10), profit * shares, _c(r / 2)))


def retained(profit, div):
    r = profit - div
    return _rs(f"A company makes Rs {profit:,} lakh profit after tax and pays Rs {div:,} lakh in dividends. How much profit is retained in the business?",
               f"একটা কোম্পানি কর-পরবর্তী {profit:,} লাখ টাকা লাভ করে আর {div:,} লাখ টাকা লভ্যাংশ দেয়। কত লাভ ব্যবসায় রেখে দেওয়া হলো?", r,
               f"Retained profit = {profit:,} - {div:,} = Rs {r:,} lakh - often used to buy new equipment.",
               f"রাখা লাভ = {profit:,} - {div:,} = {r:,} লাখ টাকা - প্রায়ই নতুন যন্ত্র কিনতে কাজে লাগে।",
               (profit + div, div, profit), " lakh", " লাখ")


def rbd(cost, pct, years, what_en, what_bn):
    v = cost
    for _ in range(years):
        v = v * (100 - pct) // 100
    sl = cost - cost * pct * years // 100
    return _rs(f"{what_en} costs Rs {cost:,}. It loses {pct}% of its value each year (reducing balance). What is it worth after {years} years?",
               f"{what_bn}-এর দাম {cost:,} টাকা। প্রতি বছর এর মূল্যের {pct}% কমে (হ্রাসমান জের)। {years} বছর পরে মূল্য কত?", v,
               f"Multiply by {(100 - pct) / 100:g} each year, {years} times: Rs {v:,}. (A flat {pct}% of the cost each year would give Rs {sl:,}.)",
               f"প্রতি বছর {(100 - pct) / 100:g} দিয়ে গুণ, {years} বার: {v:,} টাকা। (প্রতি বছর দামের সমান {pct}% কাটলে হতো {sl:,} টাকা।)",
               (sl, cost - v, v + cost * pct // 100))


def halfyear(p, rate, years):
    a = round(p * (1 + rate / 200) ** (2 * years))
    yearly = round(p * (1 + rate / 100) ** years)
    return _rs(f"Rs {p:,} is invested at {rate}% a year, compounded half-yearly. What is it worth after {years} years?",
               f"{p:,} টাকা বছরে {rate}% হারে, ছয় মাস অন্তর চক্রবৃদ্ধিতে বিনিয়োগ করা হলো। {years} বছর পরে মূল্য কত?", a,
               f"{rate / 2:g}% every half-year for {2 * years} half-years: Rs {a:,}. Yearly compounding would give Rs {yearly:,}.",
               f"প্রতি ছয় মাসে {rate / 2:g}%, {2 * years}টি অর্ধবর্ষ: {a:,} টাকা। বার্ষিক চক্রবৃদ্ধিতে হতো {yearly:,} টাকা।",
               (yearly, p + p * rate * years // 100 if p + p * rate * years // 100 != yearly else yearly - 50, a - p))


def payroll(gross, pf_pct, tax):
    pf = gross * pf_pct // 100
    net = gross - pf - tax
    return _rs(f"A site engineer's gross monthly salary is Rs {gross:,}. {pf_pct}% goes to provident fund and Rs {tax:,} is deducted as income tax. What is the take-home pay?",
               f"একজন নির্মাণ-প্রকৌশলীর মাসিক মোট বেতন {gross:,} টাকা। {pf_pct}% ভবিষ্যনিধিতে যায় আর {tax:,} টাকা আয়কর কাটা হয়। হাতে কত পান?", net,
               f"PF = {gross:,} x {pf_pct}% = {pf:,}; net = {gross:,} - {pf:,} - {tax:,} = Rs {net:,}.",
               f"ভবিষ্যনিধি = {gross:,} x {pf_pct}% = {pf:,}; হাতে = {gross:,} - {pf:,} - {tax:,} = {net:,} টাকা।",
               (gross - tax, gross - pf, gross - pf + tax))


def cashflow(opening, inflow, outflow):
    r = opening + inflow - outflow
    return _rs(f"A builder's cash-flow forecast for June: opening balance Rs {opening:,}, money in Rs {inflow:,}, money out Rs {outflow:,}. What is the closing balance?",
               f"জুনের জন্য একজন নির্মাতার নগদপ্রবাহের পূর্বাভাস: শুরুর জের {opening:,} টাকা, আসা টাকা {inflow:,}, যাওয়া টাকা {outflow:,}। শেষের জের কত?", r,
               f"Closing = opening + in - out = {opening:,} + {inflow:,} - {outflow:,} = Rs {r:,}. It becomes July's opening balance.",
               f"শেষের জের = শুরু + আসা - যাওয়া = {opening:,} + {inflow:,} - {outflow:,} = {r:,} টাকা। এটাই জুলাইয়ের শুরুর জের।",
               (inflow - outflow if inflow > outflow else r + 5000, opening + outflow - inflow if opening + outflow > inflow else r + 2000, opening + inflow))


def dps(total_div, shares):
    r = _c(total_div / shares)
    return _rs(f"A company pays out Rs {total_div:,} crore in dividends and has {shares:,} crore shares. What is the dividend per share?",
               f"একটা কোম্পানি {total_div:,} কোটি টাকা লভ্যাংশ দেয় আর শেয়ার {shares:,} কোটি। শেয়ারপ্রতি লভ্যাংশ কত?", r,
               f"{total_div:,} ÷ {shares:,} = Rs {r:g} per share.",
               f"{total_div:,} ÷ {shares:,} = শেয়ারপ্রতি {r:g} টাকা।",
               (total_div * shares, _c(shares / total_div), _c(r * 10)))


ITEMS = (
    equity(500, 320), equity(1200, 450), equity(80, 35), equity(2500, 1900),
    current(300, 150), current(450, 300), current(120, 160), current(600, 240),
    gearing(40, 60), gearing(150, 50), gearing(25, 100), gearing(90, 210),
    roce(30, 200), roce(75, 300), roce(12, 150), roce(90, 450),
    eps(120, 10), eps(45, 5), eps(300, 60), eps(18, 4),
    retained(500, 150), retained(80, 20), retained(1200, 400),
    rbd(1000000, 20, 2, "A crane", "একটা ক্রেন"), rbd(500000, 10, 3, "A site van", "নির্মাণস্থলের একটা ভ্যান"),
    rbd(200000, 25, 2, "A laptop for drawings", "নকশার একটা ল্যাপটপ"), rbd(800000, 15, 2, "A piling rig", "একটা পাইলিং-যন্ত্র"),
    halfyear(10000, 8, 1), halfyear(20000, 10, 2), halfyear(50000, 6, 1), halfyear(40000, 12, 1),
    payroll(50000, 12, 2500), payroll(80000, 12, 6000), payroll(35000, 12, 0), payroll(120000, 12, 15000),
    cashflow(200000, 450000, 520000), cashflow(50000, 300000, 240000), cashflow(150000, 100000, 180000),
    dps(60, 20), dps(25, 10), dps(90, 45),
    current(175, 100), gearing(35, 65), roce(48, 160), eps(75, 25), retained(260, 90),
    rbd(300000, 30, 2, "A hydraulic jack set", "এক সেট হাইড্রলিক জ্যাক"), halfyear(25000, 8, 2), payroll(65000, 12, 4200),
    cashflow(80000, 120000, 160000), dps(33, 12),
    mcq("What is the 'accounting equation'?", ["Assets = liabilities + owners' equity", "Profit = sales x tax", "Cash = profit", "Assets = sales - costs"], 0,
        "Every transaction keeps both sides in balance.",
        "'হিসাবের সমীকরণ' কী?", ["সম্পদ = দায় + মালিকের মূলধন", "লাভ = বিক্রি x কর", "নগদ = লাভ", "সম্পদ = বিক্রি - খরচ"],
        "প্রতিটা লেনদেন দুই দিক সমান রাখে।"),
    mcq("Which is a 'non-current' (fixed) asset for a bridge-building firm?", ["Its cranes and concrete batching plant", "Cash in the bank", "Money owed by clients this month", "This week's cement stock"], 0,
        "Non-current assets are used for more than a year to run the business.",
        "সেতু-নির্মাণ সংস্থার কোনটা 'অচলতি' (স্থায়ী) সম্পদ?", ["এর ক্রেন আর কংক্রিট-মেশানোর কারখানা", "ব্যাংকের নগদ", "এই মাসে গ্রাহকদের বকেয়া", "এই সপ্তাহের সিমেন্ট-মজুত"],
        "অচলতি সম্পদ এক বছরের বেশি ব্যবসা চালাতে ব্যবহার হয়।"),
    mcq("Which of these is a 'current liability'?", ["Money owed to suppliers, due within a year", "A 20-year bank loan", "The firm's land", "Shareholders' capital"], 0,
        "Current liabilities must be paid soon, so cash must be ready.",
        "এদের মধ্যে কোনটা 'চলতি দায়'?", ["সরবরাহকারীদের বকেয়া, এক বছরের মধ্যে দেয়", "20 বছরের ব্যাংক-ঋণ", "সংস্থার জমি", "শেয়ারহোল্ডারদের মূলধন"],
        "চলতি দায় শিগগির মেটাতে হয়, তাই নগদ তৈরি রাখতে হয়।"),
    mcq("What are 'trade receivables' (debtors)?", ["Money owed to the firm by customers for work already done", "Money the firm owes to banks", "The firm's tools", "Gifts received"], 0,
        "Chasing receivables quickly keeps cash flowing.",
        "'বাণিজ্যিক প্রাপ্য' (দেনাদার) কী?", ["আগেই করা কাজের জন্য গ্রাহকদের কাছে সংস্থার পাওনা", "ব্যাংকের কাছে সংস্থার দেনা", "সংস্থার যন্ত্রপাতি", "পাওয়া উপহার"],
        "দ্রুত প্রাপ্য আদায় করলে নগদ চলতে থাকে।"),
    mcq("What does a current ratio below 1 warn about?", ["The firm may not have enough short-term assets to pay its short-term debts", "The firm is very profitable", "The firm has no debt", "The firm owns too much land"], 0,
        "It is a sign to look closely at cash flow.",
        "চলতি অনুপাত 1-এর নিচে হলে কী সতর্ক করে?", ["স্বল্পমেয়াদি দেনা মেটানোর মতো যথেষ্ট স্বল্পমেয়াদি সম্পদ নাও থাকতে পারে", "সংস্থা খুব লাভজনক", "সংস্থার কোনো ঋণ নেই", "সংস্থার অনেক বেশি জমি"],
        "নগদপ্রবাহ খুঁটিয়ে দেখার সংকেত।"),
    mcq("Why is a highly geared company riskier when interest rates rise?", ["More of its profit must go on interest payments, leaving less margin for bad times", "It has no loans", "Interest rates do not affect it", "Shareholders pay the interest"], 0,
        "Gearing amplifies both good and bad results.",
        "সুদের হার বাড়লে উচ্চ-গিয়ারিংয়ের কোম্পানি বেশি ঝুঁকির কেন?", ["লাভের বেশি অংশ সুদ মেটাতে যায়, খারাপ সময়ের জন্য কম ফাঁক থাকে", "এর কোনো ঋণ নেই", "সুদের হার প্রভাব ফেলে না", "শেয়ারহোল্ডাররা সুদ দেন"],
        "গিয়ারিং ভালো আর খারাপ দুই ফলকেই বড় করে।"),
    mcq("What does ROCE tell an investor?", ["How well a firm turns the money invested in it into operating profit", "The firm's total cash", "The share price", "The number of employees"], 0,
        "A ROCE below the bank interest rate suggests the money might do better elsewhere.",
        "আরওসিই বিনিয়োগকারীকে কী জানায়?", ["সংস্থায় খাটানো টাকাকে সংস্থা কতটা ভালোভাবে পরিচালন-লাভে বদলায়", "সংস্থার মোট নগদ", "শেয়ারের দাম", "কর্মীর সংখ্যা"],
        "ব্যাংকের সুদের চেয়ে কম আরওসিই বোঝায় টাকা অন্য কোথাও ভালো করতে পারত।"),
    mcq("What is 'retained profit' used for?", ["Reinvesting in the business, such as new machinery or repaying loans", "Paying all staff bonuses", "It disappears", "Paying taxes twice"], 0,
        "Growing firms often retain more and pay smaller dividends.",
        "'রাখা লাভ' কীসের জন্য ব্যবহার হয়?", ["ব্যবসায় আবার বিনিয়োগ, যেমন নতুন যন্ত্র বা ঋণ শোধ", "সব কর্মীর বোনাস", "মিলিয়ে যায়", "দুবার কর দেওয়া"],
        "বাড়তে-থাকা সংস্থা প্রায়ই বেশি রাখে আর কম লভ্যাংশ দেয়।"),
    mcq("What is the difference between straight-line and reducing-balance depreciation?", ["Straight-line takes the same amount each year; reducing-balance takes the same percentage of the remaining value", "They are identical", "Reducing balance never reaches low values", "Straight-line is only for land"], 0,
        "Reducing balance suits vehicles and computers that lose value fastest when new.",
        "সরলরৈখিক আর হ্রাসমান-জের অবচয়ের পার্থক্য কী?", ["সরলরৈখিকে প্রতি বছর একই অঙ্ক; হ্রাসমানে বাকি মূল্যের একই শতাংশ", "দুটো একই", "হ্রাসমান কখনো কম মানে পৌঁছায় না", "সরলরৈখিক শুধু জমির জন্য"],
        "হ্রাসমান জের গাড়ি আর কম্পিউটারের জন্য মানানসই, যা নতুন অবস্থায় দ্রুত দাম হারায়।"),
    mcq("Why is land usually not depreciated in company accounts?", ["Land does not wear out or get used up", "Land is illegal to own", "Land always loses value", "Accountants forget"], 0,
        "Buildings and machines on the land are depreciated.",
        "কোম্পানির হিসাবে সাধারণত জমির অবচয় ধরা হয় না কেন?", ["জমি ক্ষয়ে যায় না বা ফুরোয় না", "জমির মালিকানা বেআইনি", "জমি সবসময় দাম হারায়", "হিসাবরক্ষকরা ভুলে যান"],
        "জমির উপরের বাড়ি আর যন্ত্রের অবচয় ধরা হয়।"),
    mcq("Why does compounding more often (monthly rather than yearly) give slightly more interest?", ["Interest starts earning interest sooner", "Banks add a fee", "The rate doubles", "It gives less"], 0,
        "The effect is small for one year but adds up over many.",
        "ঘন ঘন চক্রবৃদ্ধি (বার্ষিকের বদলে মাসিক) একটু বেশি সুদ দেয় কেন?", ["সুদ তাড়াতাড়ি নিজেও সুদ পেতে শুরু করে", "ব্যাংক ফি যোগ করে", "হার দ্বিগুণ হয়", "কম দেয়"],
        "এক বছরে প্রভাব ছোট, কিন্তু অনেক বছরে জমে ওঠে।"),
    mcq("What do employers in India contribute to a worker's EPF?", ["An amount matching part of the worker's own contribution, usually 12% of basic pay", "Nothing", "The whole salary", "Only a birthday gift"], 0,
        "It builds retirement savings for both organised and registered construction workers.",
        "ভারতে নিয়োগকর্তা কর্মীর ইপিএফ-এ কী দেন?", ["কর্মীর নিজের জমার অংশের সমান অঙ্ক, সাধারণত মূল বেতনের 12%", "কিছুই না", "পুরো বেতন", "শুধু জন্মদিনের উপহার"],
        "সংগঠিত আর নিবন্ধিত নির্মাণ-শ্রমিক দুজনের জন্যই অবসরের সঞ্চয় গড়ে।"),
    mcq("What is the difference between gross pay and net pay?", ["Gross is before deductions like tax and PF; net is what reaches your account", "They are always equal", "Net is before tax", "Gross includes only overtime"], 0,
        "Always check your payslip each month.",
        "মোট বেতন আর নিট বেতনের পার্থক্য কী?", ["মোট হলো কর আর ভবিষ্যনিধির মতো কাটার আগে; নিট হলো যা অ্যাকাউন্টে পৌঁছায়", "সবসময় সমান", "নিট করের আগে", "মোটে শুধু ওভারটাইম"],
        "প্রতি মাসে বেতনের স্লিপ যাচাই করো।"),
    mcq("What is a 'cash-flow forecast'?", ["A month-by-month prediction of money coming in and going out", "A weather report", "A record of past profits only", "A list of employees"], 0,
        "It warns a firm early if it will run short of cash.",
        "'নগদপ্রবাহের পূর্বাভাস' কী?", ["মাসে মাসে আসা আর যাওয়া টাকার আগাম হিসাব", "আবহাওয়ার খবর", "শুধু আগের লাভের নথি", "কর্মীর তালিকা"],
        "নগদের টান পড়বে কিনা সংস্থাকে আগেভাগে সতর্ক করে।"),
    mcq("A builder's forecast shows negative cash in August. What is the most sensible action now?", ["Arrange an overdraft or chase payments in advance, or delay non-urgent spending", "Ignore it until August", "Stop paying workers", "Close the business"], 0,
        "Forecasts are useful only if you act on them early.",
        "একজন নির্মাতার পূর্বাভাসে আগস্টে নগদ ঋণাত্মক দেখাচ্ছে। এখন সবচেয়ে যুক্তিসঙ্গত পদক্ষেপ কী?", ["আগেভাগে ওভারড্রাফটের ব্যবস্থা বা পাওনা আদায়, বা অ-জরুরি খরচ পিছোনো", "আগস্ট পর্যন্ত উপেক্ষা", "কর্মীদের বেতন বন্ধ", "ব্যবসা বন্ধ"],
        "পূর্বাভাস তখনই কাজের, যখন আগে থেকে ব্যবস্থা নেওয়া হয়।"),
    mcq("What is 'earnings per share' (EPS)?", ["Profit after tax divided by the number of shares", "The share price", "The dividend paid", "Total sales divided by employees"], 0,
        "Rising EPS over several years is a good sign of a growing company.",
        "'শেয়ারপ্রতি আয়' (ইপিএস) কী?", ["কর-পরবর্তী লাভকে শেয়ারের সংখ্যা দিয়ে ভাগ", "শেয়ারের দাম", "দেওয়া লভ্যাংশ", "মোট বিক্রি ÷ কর্মী"],
        "কয়েক বছর ধরে বাড়তে-থাকা ইপিএস বাড়ন্ত কোম্পানির ভালো লক্ষণ।"),
    mcq("Why might a company pay no dividend in a year when it made a profit?", ["It may need the cash to invest in big new projects or to reduce debt", "Dividends are illegal", "Shareholders refuse money", "Profit cannot be shared"], 0,
        "Shareholders hope the investment grows future profits.",
        "লাভ হলেও কোনো বছর কোম্পানি লভ্যাংশ নাও দিতে পারে কেন?", ["বড় নতুন প্রকল্পে বিনিয়োগ বা ঋণ কমাতে নগদ লাগতে পারে", "লভ্যাংশ বেআইনি", "শেয়ারহোল্ডাররা টাকা নেন না", "লাভ ভাগ করা যায় না"],
        "শেয়ারহোল্ডাররা আশা করেন বিনিয়োগ ভবিষ্যৎ লাভ বাড়াবে।"),
    mcq("What is an 'annual report' of a listed company?", ["A yearly document with audited accounts and a review of the business, published for shareholders", "A list of holidays", "A tax bill", "A newspaper advert"], 0,
        "Anyone can read listed companies' annual reports online.",
        "তালিকাভুক্ত কোম্পানির 'বার্ষিক প্রতিবেদন' কী?", ["শেয়ারহোল্ডারদের জন্য প্রকাশিত নিরীক্ষিত হিসাব আর ব্যবসার পর্যালোচনাসহ বার্ষিক নথি", "ছুটির তালিকা", "করের বিল", "খবরের কাগজের বিজ্ঞাপন"],
        "তালিকাভুক্ত কোম্পানির বার্ষিক প্রতিবেদন যে কেউ অনলাইনে পড়তে পারে।"),
    mcq("What does an auditor's 'qualified opinion' warn shareholders about?", ["The auditor disagrees with or could not check something important in the accounts", "The accounts are perfect", "The auditor is qualified to fly", "The firm paid a dividend"], 0,
        "It is a red flag worth investigating.",
        "নিরীক্ষকের 'শর্তযুক্ত মতামত' শেয়ারহোল্ডারদের কী নিয়ে সতর্ক করে?", ["হিসাবের কোনো জরুরি বিষয়ে নিরীক্ষক একমত নন বা যাচাই করতে পারেননি", "হিসাব নিখুঁত", "নিরীক্ষক বিমান চালাতে যোগ্য", "সংস্থা লভ্যাংশ দিয়েছে"],
        "এটা খুঁটিয়ে দেখার মতো বিপদসংকেত।"),
    mcq("What is 'window dressing' of accounts?", ["Making the accounts look better than reality at the year end, for example by delaying payments", "Decorating the office", "Cleaning windows", "Paying taxes early"], 0,
        "It can mislead lenders and investors and may break the law.",
        "হিসাবের 'জানালা-সাজানো' কী?", ["বছরের শেষে হিসাবকে বাস্তবের চেয়ে ভালো দেখানো, যেমন পেমেন্ট পিছিয়ে", "অফিস সাজানো", "জানালা পরিষ্কার", "আগে কর দেওয়া"],
        "এটা ঋণদাতা আর বিনিয়োগকারীদের ভুল বোঝাতে পারে আর আইন ভাঙতে পারে।"),
    mcq("A firm's revenue doubled but its trade receivables tripled. What should a careful analyst ask?", ["Are customers paying slowly or are some sales doubtful?", "Why is the office so big?", "How many cranes are blue?", "Nothing - it is always good news"], 0,
        "Sales that are never paid are not real money.",
        "একটা সংস্থার আয় দ্বিগুণ হলো, কিন্তু বাণিজ্যিক প্রাপ্য তিনগুণ। একজন সতর্ক বিশ্লেষকের কী জিজ্ঞাসা করা উচিত?", ["গ্রাহকরা কি দেরিতে টাকা দিচ্ছেন, নাকি কিছু বিক্রি সন্দেহজনক?", "অফিস এত বড় কেন?", "কটা ক্রেন নীল?", "কিছু না - সবসময় সুখবর"],
        "যে বিক্রির টাকা কখনো আসে না, তা আসল টাকা নয়।"),
    mcq("What is 'bad debt'?", ["Money owed to the firm that will never be paid and is written off", "A loan with high interest", "Debt used to buy tools", "A debt paid early"], 0,
        "Checking a client's credit before starting work reduces bad debts.",
        "'অনাদায়ী দেনা' কী?", ["সংস্থার পাওনা যা কখনো মিলবে না আর বাদ দেওয়া হয়", "চড়া সুদের ঋণ", "যন্ত্র কেনার ঋণ", "আগে শোধ হওয়া দেনা"],
        "কাজ শুরুর আগে গ্রাহকের ঋণযোগ্যতা যাচাই করলে অনাদায়ী দেনা কমে।"),
    mcq("What is a 'bank reconciliation'?", ["Checking the firm's own cash records against the bank statement and explaining any differences", "Making friends with the bank manager", "Closing a bank account", "Applying for a loan"], 0,
        "It catches errors, missing payments and fraud early.",
        "'ব্যাংক-সমন্বয়' কী?", ["সংস্থার নিজের নগদের নথি ব্যাংক-বিবরণীর সঙ্গে মিলিয়ে পার্থক্য ব্যাখ্যা করা", "ব্যাংক-ম্যানেজারের সঙ্গে বন্ধুত্ব", "ব্যাংক-অ্যাকাউন্ট বন্ধ", "ঋণের আবেদন"],
        "ভুল, বাদ-পড়া পেমেন্ট আর প্রতারণা আগেভাগে ধরে।"),
    mcq("What is 'double-entry bookkeeping'?", ["Recording every transaction twice - once as a debit and once as a credit", "Writing everything in two books for safety", "Counting cash twice", "Paying every bill twice"], 0,
        "It keeps the accounting equation balanced and helps spot errors.",
        "'দু-তরফা হিসাবরক্ষণ' কী?", ["প্রতিটা লেনদেন দুবার লেখা - একবার ডেবিট আর একবার ক্রেডিট হিসেবে", "নিরাপত্তার জন্য দুটো খাতায় লেখা", "নগদ দুবার গোনা", "প্রতিটা বিল দুবার দেওয়া"],
        "হিসাবের সমীকরণ সমান রাখে আর ভুল ধরতে সাহায্য করে।"),
    mcq("A contractor buys a Rs 5 lakh mixer on credit. How does the balance sheet change?", ["Assets rise by Rs 5 lakh and liabilities rise by Rs 5 lakh", "Assets fall by Rs 5 lakh", "Equity rises by Rs 5 lakh", "Nothing changes"], 0,
        "Both sides go up equally, so it still balances.",
        "একজন ঠিকাদার ধারে 5 লাখ টাকার মিক্সার কিনলেন। উদ্বৃত্তপত্র কীভাবে বদলায়?", ["সম্পদ 5 লাখ বাড়ে আর দায়ও 5 লাখ বাড়ে", "সম্পদ 5 লাখ কমে", "মূলধন 5 লাখ বাড়ে", "কিছু বদলায় না"],
        "দুই দিক সমান বাড়ে, তাই এখনো মেলে।"),
    mcq("What is 'share capital'?", ["Money raised by a company by selling shares to its owners", "A loan from a bank", "Profit from last year", "The capital city where shares are traded"], 0,
        "It does not have to be repaid like a loan.",
        "'শেয়ার-মূলধন' কী?", ["মালিকদের কাছে শেয়ার বেচে কোম্পানির তোলা টাকা", "ব্যাংকের ঋণ", "গত বছরের লাভ", "যে রাজধানীতে শেয়ার কেনাবেচা হয়"],
        "ঋণের মতো ফেরত দিতে হয় না।"),
    mcq("What is 'limited liability' for shareholders?", ["They can lose only the money they invested, not their personal homes or savings", "They must pay all company debts", "They have no rights", "They cannot sell shares"], 0,
        "It encourages people to invest in big ventures like bridge-building companies.",
        "শেয়ারহোল্ডারদের 'সীমিত দায়' কী?", ["শুধু বিনিয়োগ করা টাকাই হারাতে পারেন, নিজের বাড়ি বা সঞ্চয় নয়", "কোম্পানির সব দেনা দিতে হয়", "কোনো অধিকার নেই", "শেয়ার বেচতে পারেন না"],
        "এটা মানুষকে সেতু-নির্মাণ কোম্পানির মতো বড় উদ্যোগে বিনিয়োগে উৎসাহ দেয়।"),
    mcq("What is the main difference between a sole trader and a private limited company?", ["A company is a separate legal person with limited liability; a sole trader is personally liable for all debts", "There is no difference", "Sole traders cannot have customers", "Companies cannot own equipment"], 0,
        "Many small contractors start as sole traders and later form companies.",
        "একক ব্যবসায়ী আর প্রাইভেট লিমিটেড কোম্পানির প্রধান পার্থক্য কী?", ["কোম্পানি সীমিত দায়সহ আলাদা আইনি ব্যক্তি; একক ব্যবসায়ী সব দেনার জন্য ব্যক্তিগতভাবে দায়ী", "কোনো পার্থক্য নেই", "একক ব্যবসায়ীর খদ্দের থাকতে পারে না", "কোম্পানি যন্ত্রের মালিক হতে পারে না"],
        "অনেক ছোট ঠিকাদার একক ব্যবসায়ী হিসেবে শুরু করে পরে কোম্পানি গড়েন।"),
    mcq("What is a 'partnership' in business?", ["Two or more people owning and running a business together and sharing profits", "A company owned by the government", "One person working alone", "A loan between friends"], 0,
        "A written partnership deed avoids arguments later.",
        "ব্যবসায় 'অংশীদারি' কী?", ["দুই বা বেশি জন একসঙ্গে ব্যবসার মালিক হয়ে চালান আর লাভ ভাগ করেন", "সরকারের মালিকানার কোম্পানি", "একা কাজ করা একজন", "বন্ধুদের মধ্যে ঋণ"],
        "লিখিত অংশীদারি-চুক্তি পরে তর্ক এড়ায়।"),
    mcq("Two partners share profits in the ratio 3 : 2. The firm makes Rs 5 lakh profit. How much does the first partner get?", ["Rs 3 lakh", "Rs 2 lakh", "Rs 2.5 lakh", "Rs 1.5 lakh"], 0,
        "5 lakh ÷ 5 parts = 1 lakh per part; 3 parts = Rs 3 lakh.",
        "দুই অংশীদার 3 : 2 অনুপাতে লাভ ভাগ করেন। সংস্থা 5 লাখ টাকা লাভ করল। প্রথম অংশীদার কত পান?", ["3 লাখ টাকা", "2 লাখ টাকা", "2.5 লাখ টাকা", "1.5 লাখ টাকা"],
        "5 লাখ ÷ 5 ভাগ = ভাগপ্রতি 1 লাখ; 3 ভাগ = 3 লাখ টাকা।"),
    mcq("What is 'capital expenditure' on a bridge project?", ["Spending on long-lasting assets, such as building the bridge itself", "Day-to-day spending like fuel", "Paying salaries", "Buying lunch"], 0,
        "Running and maintenance costs are 'revenue expenditure'.",
        "সেতু-প্রকল্পে 'মূলধনী ব্যয়' কী?", ["দীর্ঘস্থায়ী সম্পদে খরচ, যেমন সেতু নিজেই বানানো", "জ্বালানির মতো দৈনন্দিন খরচ", "বেতন দেওয়া", "দুপুরের খাবার কেনা"],
        "চালানো আর রক্ষণাবেক্ষণের খরচ 'রাজস্ব ব্যয়'।"),
    mcq("Why do governments budget separately for building a bridge and for maintaining it?", ["Construction is a one-off capital cost; maintenance is a regular yearly cost that must be planned for decades", "Maintenance is free", "Bridges never need maintenance", "Both are the same"], 0,
        "Bridges fail when maintenance budgets are cut for too long.",
        "সরকার সেতু বানানো আর রক্ষণাবেক্ষণের জন্য আলাদা বাজেট করে কেন?", ["নির্মাণ একবারের মূলধনী খরচ; রক্ষণাবেক্ষণ নিয়মিত বার্ষিক খরচ, যা কয়েক দশক ধরে পরিকল্পনা করতে হয়", "রক্ষণাবেক্ষণ বিনামূল্যে", "সেতুর রক্ষণাবেক্ষণ লাগে না", "দুটো একই"],
        "রক্ষণাবেক্ষণের বাজেট বেশিদিন ছাঁটলে সেতু ব্যর্থ হয়।"),
    mcq("What is 'inflation-indexed' pay or pension?", ["Payments that rise in line with prices, so their buying power is protected", "Pay that falls every year", "Pay in gold only", "A one-off bonus"], 0,
        "Dearness allowance (DA) in India works this way.",
        "'মূল্যসূচক-যুক্ত' বেতন বা পেনশন কী?", ["দামের সঙ্গে তাল রেখে বাড়ে, তাই ক্রয়ক্ষমতা রক্ষা পায়", "প্রতি বছর কমা বেতন", "শুধু সোনায় বেতন", "একবারের বোনাস"],
        "ভারতে মহার্ঘ ভাতা (ডিএ) এভাবে কাজ করে।"),
    mcq("What is the 'consumer price index' (CPI)?", ["A measure of how the prices of a typical basket of goods and services change over time", "The price of one product", "A list of shops", "The interest rate"], 0,
        "Inflation is usually reported as the yearly change in CPI.",
        "'ভোক্তা মূল্যসূচক' (সিপিআই) কী?", ["সাধারণ পণ্য-পরিষেবার একটা ঝুড়ির দাম সময়ের সঙ্গে কীভাবে বদলায় তার মাপ", "একটা পণ্যের দাম", "দোকানের তালিকা", "সুদের হার"],
        "মুদ্রাস্ফীতি সাধারণত সিপিআই-এর বার্ষিক বদল হিসেবে জানানো হয়।"),
    mcq("Why do long bridge contracts often include a 'price variation clause'?", ["So the price can be adjusted if steel, cement or fuel costs rise or fall sharply", "To let the client never pay", "To fix the price forever", "To change the bridge's design"], 0,
        "It shares the risk of inflation fairly between client and contractor.",
        "দীর্ঘ সেতু-চুক্তিতে প্রায়ই 'দাম-পরিবর্তন ধারা' থাকে কেন?", ["ইস্পাত, সিমেন্ট বা জ্বালানির দাম খুব বাড়লে-কমলে দাম সমন্বয় করা যায়", "গ্রাহক যাতে কখনো টাকা না দেন", "চিরকাল দাম স্থির রাখতে", "সেতুর নকশা বদলাতে"],
        "মুদ্রাস্ফীতির ঝুঁকি গ্রাহক আর ঠিকাদারের মধ্যে ন্যায্যভাবে ভাগ করে।"),
    mcq("What is 'mobilisation advance' on a big bridge contract?", ["An early payment to help the contractor set up the site, repaid from later bills", "A bonus for finishing", "A fine for delay", "A free gift"], 0,
        "It is usually secured by a bank guarantee.",
        "বড় সেতু-চুক্তিতে 'প্রস্তুতি-অগ্রিম' কী?", ["নির্মাণস্থল গোছাতে ঠিকাদারকে আগাম টাকা, পরের বিল থেকে কেটে নেওয়া হয়", "শেষ করার বোনাস", "দেরির জরিমানা", "বিনামূল্যের উপহার"],
        "সাধারণত ব্যাংক-গ্যারান্টিতে সুরক্ষিত থাকে।"),
    mcq("What is a 'running account bill' (RA bill) on a construction project?", ["An interim bill for work done so far, paid in stages as the project progresses", "A bill for running shoes", "The final bill only", "A bill for electricity"], 0,
        "Stage payments keep cash flowing on long projects.",
        "নির্মাণ-প্রকল্পে 'চলতি হিসাব বিল' (আরএ বিল) কী?", ["এখন পর্যন্ত করা কাজের অন্তর্বর্তী বিল, প্রকল্প এগোনোর সঙ্গে ধাপে ধাপে মেটানো হয়", "দৌড়ের জুতোর বিল", "শুধু শেষ বিল", "বিদ্যুতের বিল"],
        "ধাপে ধাপে পেমেন্ট লম্বা প্রকল্পে নগদ চালু রাখে।"),
    mcq("Why should a young worker keep at least some savings in a liquid account even while investing in shares?", ["Shares can fall just when cash is needed for an emergency", "Shares cannot be sold ever", "Liquid accounts pay the most interest", "Banks require it"], 0,
        "Emergency money first, long-term investing second.",
        "শেয়ারে বিনিয়োগের সময়ও একজন তরুণ কর্মীর কিছু সঞ্চয় তরল অ্যাকাউন্টে রাখা উচিত কেন?", ["জরুরি অবস্থায় নগদ দরকার পড়ার মুহূর্তেই শেয়ারের দাম পড়তে পারে", "শেয়ার কখনো বেচা যায় না", "তরল অ্যাকাউন্টে সবচেয়ে বেশি সুদ", "ব্যাংক বাধ্য করে"],
        "আগে জরুরি টাকা, পরে দীর্ঘমেয়াদি বিনিয়োগ।"),
    mcq("What is 'rupee cost averaging' with a monthly SIP?", ["Buying more units when prices are low and fewer when high, smoothing the average cost", "Paying the same price every month", "Buying only when prices peak", "Selling every month"], 0,
        "It removes the need to guess the best day to invest.",
        "মাসিক এসআইপি-তে 'টাকা-খরচের গড়' কী?", ["দাম কম হলে বেশি একক আর বেশি হলে কম একক কেনা, গড় খরচ মসৃণ হয়", "প্রতি মাসে একই দাম দেওয়া", "শুধু দাম চূড়ায় কেনা", "প্রতি মাসে বেচা"],
        "বিনিয়োগের সেরা দিন আন্দাজ করার দরকার থাকে না।"),
    mcq("What is 'goodwill' on a company's balance sheet?", ["The extra value paid when buying a business, for things like its reputation and customer base", "Kindness shown to staff", "A charity donation", "Cash in the bank"], 0,
        "It is an intangible asset - you cannot touch it, but it has value.",
        "কোম্পানির উদ্বৃত্তপত্রে 'সুনাম' (গুডউইল) কী?", ["ব্যবসা কেনার সময় এর সুনাম আর খদ্দের-ভিত্তির মতো জিনিসের জন্য দেওয়া বাড়তি মূল্য", "কর্মীদের প্রতি দয়া", "দাতব্য দান", "ব্যাংকের নগদ"],
        "এটা অদৃশ্য সম্পদ - ছোঁয়া যায় না, কিন্তু মূল্য আছে।"),
    mcq("What is a 'provision' in a builder's accounts?", ["An amount set aside for a likely future cost, such as repairing defects under warranty", "Food for the workers", "A government grant", "A bank deposit that earns interest"], 0,
        "It makes this year's profit reflect costs that this year's work will cause.",
        "একজন নির্মাতার হিসাবে 'সংস্থান' (প্রভিশন) কী?", ["সম্ভাব্য ভবিষ্যৎ খরচের জন্য সরিয়ে রাখা অঙ্ক, যেমন ওয়ারেন্টির মধ্যে ত্রুটি সারানো", "কর্মীদের খাবার", "সরকারি অনুদান", "সুদ-পাওয়া ব্যাংক-জমা"],
        "এ বছরের কাজের জন্য যে খরচ হবে, তা এ বছরের লাভে প্রতিফলিত করে।"),
    mcq("What does 'accrual accounting' mean?", ["Income and costs are recorded when they are earned or incurred, not when cash changes hands", "Recording only cash payments", "Ignoring all bills", "Counting money once a year"], 0,
        "A bridge section finished in March counts as March income even if paid in May.",
        "'উপার্জন-ভিত্তিক হিসাব' মানে কী?", ["আয় আর খরচ যখন অর্জিত বা উদ্ভূত হয় তখনই লেখা হয়, নগদ হাতবদলের সময় নয়", "শুধু নগদ পেমেন্ট লেখা", "সব বিল উপেক্ষা", "বছরে একবার টাকা গোনা"],
        "মার্চে শেষ হওয়া সেতু-খণ্ড মে-তে টাকা পেলেও মার্চের আয় ধরা হয়।"),
    mcq("What does it mean if a company is 'insolvent'?", ["It cannot pay its debts as they fall due", "It is very profitable", "It has no customers but lots of cash", "It has just been formed"], 0,
        "Insolvent firms may be restructured or wound up by a court process.",
        "কোম্পানি 'দেউলিয়া' মানে কী?", ["দেনা মেটানোর সময় হলে তা দিতে পারে না", "খুব লাভজনক", "খদ্দের নেই কিন্তু অনেক নগদ", "সবে তৈরি হয়েছে"],
        "দেউলিয়া সংস্থা আদালতের প্রক্রিয়ায় পুনর্গঠিত বা গুটিয়ে ফেলা হতে পারে।"),
    mcq("Why can a contractor's insolvency be a serious problem for a bridge project?", ["Work stops, suppliers go unpaid, and a new contractor must be found, causing delays and extra cost", "The bridge finishes faster", "The client saves money", "It has no effect"], 0,
        "That is why clients check bidders' finances and ask for performance guarantees.",
        "ঠিকাদারের দেউলিয়া হওয়া সেতু-প্রকল্পের জন্য গুরুতর সমস্যা কেন?", ["কাজ থামে, সরবরাহকারীরা টাকা পান না, নতুন ঠিকাদার খুঁজতে হয়, ফলে দেরি আর বাড়তি খরচ", "সেতু তাড়াতাড়ি শেষ হয়", "গ্রাহকের টাকা বাঁচে", "কোনো প্রভাব নেই"],
        "তাই গ্রাহকরা দরদাতার আর্থিক অবস্থা দেখেন আর কাজ-সম্পাদনের গ্যারান্টি চান।"),
    mcq("What does a bond's 'credit rating', such as AAA or BB, tell investors?", ["How likely the issuer is to repay interest and capital on time", "The bond's colour", "How many bonds exist", "The issuer's age"], 0,
        "Agencies like CRISIL and ICRA rate Indian borrowers.",
        "বন্ডের 'ঋণমান', যেমন AAA বা BB, বিনিয়োগকারীকে কী জানায়?", ["প্রদানকারী সময়মতো সুদ আর আসল ফেরত দেওয়ার সম্ভাবনা কতটা", "বন্ডের রং", "কতগুলো বন্ড আছে", "প্রদানকারীর বয়স"],
        "ক্রিসিল আর ইকরার মতো সংস্থা ভারতীয় ঋণগ্রহীতাদের মান দেয়।"),
    mcq("Why does an AAA-rated infrastructure bond usually pay a lower interest rate than a BB-rated one?", ["Investors accept less return for much lower risk of default", "AAA bonds are smaller", "BB bonds are government-backed", "Ratings do not affect interest"], 0,
        "Higher risk must be rewarded with higher interest.",
        "AAA-মানের পরিকাঠামো-বন্ড সাধারণত BB-মানের চেয়ে কম সুদ দেয় কেন?", ["অনেক কম খেলাপি-ঝুঁকির জন্য বিনিয়োগকারীরা কম লাভ মেনে নেন", "AAA বন্ড ছোট", "BB বন্ড সরকার-সমর্থিত", "মান সুদে প্রভাব ফেলে না"],
        "বেশি ঝুঁকিকে বেশি সুদে পুরস্কৃত করতে হয়।"),
    mcq("A firm makes operating profit of Rs 60 lakh and pays Rs 15 lakh in interest. What is its interest cover?", ["4 times", "0.25 times", "45 times", "75 times"], 0,
        "Interest cover = operating profit ÷ interest = 60 ÷ 15 = 4. Lenders like it well above 2.",
        "একটা সংস্থার পরিচালন-লাভ 60 লাখ টাকা আর সুদ দেয় 15 লাখ টাকা। সুদ-আচ্ছাদন কত?", ["4 গুণ", "0.25 গুণ", "45 গুণ", "75 গুণ"],
        "সুদ-আচ্ছাদন = পরিচালন-লাভ ÷ সুদ = 60 ÷ 15 = 4। ঋণদাতারা এটা 2-এর অনেক উপরে চান।"),
    mcq("What is a 'statutory audit' in India?", ["An audit of a company's accounts that the law requires every year", "A voluntary check by friends", "A police raid", "A tax refund"], 0,
        "It is done by an independent chartered accountant.",
        "ভারতে 'বিধিবদ্ধ নিরীক্ষা' কী?", ["আইনে প্রতি বছর বাধ্যতামূলক কোম্পানির হিসাবের নিরীক্ষা", "বন্ধুদের স্বেচ্ছা যাচাই", "পুলিশের তল্লাশি", "করের ফেরত"],
        "স্বাধীন চার্টার্ড অ্যাকাউন্ট্যান্ট এটা করেন।"),
    mcq("A Rs 10 lakh invoice is raised in March but paid in June. Under accrual accounting, when is the income recorded?", ["In March", "In June", "Half in each month", "Never"], 0,
        "Cash flow and profit can differ because of timing like this.",
        "মার্চে 10 লাখ টাকার চালান হলো কিন্তু জুনে টাকা এল। উপার্জন-ভিত্তিক হিসাবে আয় কখন লেখা হয়?", ["মার্চে", "জুনে", "দুই মাসে অর্ধেক অর্ধেক", "কখনো না"],
        "এমন সময়ের ফারাকে নগদপ্রবাহ আর লাভ আলাদা হতে পারে।"),
)
