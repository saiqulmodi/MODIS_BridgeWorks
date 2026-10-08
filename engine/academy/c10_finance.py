"""Class 10 - Finance (Bridge Engineer): GST split into CGST and SGST, income tax by slabs,
receivable, inventory and payable days, profit margin and return on equity, quarterly
compounding, loan balances after an EMI, exact real returns, insurance premiums, bond prices
and interest rates, choosing between debt and equity, and fair, transparent finance."""
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


def _rs(q_en, q_bn, r, ex_en, ex_bn, alts):
    o = _o(r, *alts)
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:,.2f}"
    return mcq(q_en, [f"Rs {f(x)}" for x in o], 0, ex_en, q_bn, [f"{f(x)} টাকা" for x in o], ex_bn)


def _num(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    o = _o(r, *alts)
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [f"{f(x)}{u_en}" for x in o], 0, ex_en, q_bn, [f"{f(x)}{ub}" for x in o], ex_bn)


def gst_split(price, rate, item_en, item_bn):
    each = price * rate // 200
    return _rs(f"{item_en} worth Rs {price:,} is sold within one state at {rate}% GST. How much is charged as CGST (the central part)?",
               f"একই রাজ্যের মধ্যে {price:,} টাকার {item_bn} {rate}% জিএসটিতে বিক্রি হলো। সিজিএসটি (কেন্দ্রের অংশ) হিসেবে কত নেওয়া হয়?", each,
               f"Within a state, GST is split equally: CGST {rate / 2:g}% + SGST {rate / 2:g}%. CGST = {price:,} x {rate / 2:g}% = Rs {each:,}.",
               f"একই রাজ্যে জিএসটি সমান ভাগ হয়: সিজিএসটি {rate / 2:g}% + এসজিএসটি {rate / 2:g}%। সিজিএসটি = {price:,} x {rate / 2:g}% = {each:,} টাকা।",
               (each * 2, price + each * 2, each // 2))


def slab_tax(income):
    # simplified illustrative slabs (lakh): 0-3 nil, 3-6 at 5%, 6-9 at 10%, 9-12 at 15%
    bands = [(300000, 0), (300000, 5), (300000, 10), (300000, 15)]
    left, tax, parts = income, 0, []
    for width, rate in bands:
        take = min(left, width)
        if take <= 0:
            break
        t = take * rate // 100
        tax += t
        if rate:
            parts.append(f"{take:,} x {rate}% = {t:,}")
        left -= take
    flat = income * 10 // 100
    return _rs(f"Using these simplified slabs - first Rs 3 lakh tax-free, next Rs 3 lakh at 5%, next Rs 3 lakh at 10%, next Rs 3 lakh at 15% - what tax is due on an income of Rs {income:,}?",
               f"এই সরলীকৃত ধাপে - প্রথম 3 লাখ করমুক্ত, পরের 3 লাখে 5%, পরের 3 লাখে 10%, পরের 3 লাখে 15% - {income:,} টাকা আয়ে কত কর?", tax,
               f"Only each slice is taxed at its own rate: {'; '.join(parts)}; total Rs {tax:,}.",
               f"প্রতিটা ভাগে শুধু তার নিজের হারে কর: {'; '.join(parts)}; মোট {tax:,} টাকা।",
               (flat, income * 15 // 100, tax + 15000))


def recv_days(recv, sales):
    r = _c(recv / sales * 365)
    return _num(f"A builder's annual sales are Rs {sales:,} lakh and clients owe Rs {recv:,} lakh at the year end. On average, how many days do clients take to pay?",
                f"একজন নির্মাতার বার্ষিক বিক্রি {sales:,} লাখ টাকা আর বছরের শেষে গ্রাহকদের বকেয়া {recv:,} লাখ টাকা। গ্রাহকরা গড়ে কত দিনে টাকা দেন?", r,
                f"Receivable days = receivables ÷ sales x 365 = {recv:,} ÷ {sales:,} x 365 = {r:g} days.",
                f"প্রাপ্য-দিন = প্রাপ্য ÷ বিক্রি x 365 = {recv:,} ÷ {sales:,} x 365 = {r:g} দিন।",
                (_c(sales / recv), _c(recv / sales * 100), _c(r * 2)), " days", " দিন")


def inv_days(inv, cogs):
    r = _c(inv / cogs * 365)
    return _num(f"A steel stockist holds Rs {inv:,} lakh of stock and its cost of sales is Rs {cogs:,} lakh a year. How many days of stock does it hold?",
                f"একজন ইস্পাত-মজুতদারের কাছে {inv:,} লাখ টাকার মজুত আর বছরে বিক্রীত মালের খরচ {cogs:,} লাখ টাকা। কত দিনের মজুত আছে?", r,
                f"Inventory days = {inv:,} ÷ {cogs:,} x 365 = {r:g} days.",
                f"মজুত-দিন = {inv:,} ÷ {cogs:,} x 365 = {r:g} দিন।",
                (_c(cogs / inv), _c(inv / cogs * 100), _c(r * 2)), " days", " দিন")


def pay_days(pay, purchases):
    r = _c(pay / purchases * 365)
    return _num(f"A contractor owes suppliers Rs {pay:,} lakh and buys Rs {purchases:,} lakh of materials a year on credit. How many days does it take to pay suppliers?",
                f"একজন ঠিকাদারের সরবরাহকারীদের কাছে দেনা {pay:,} লাখ টাকা আর বছরে ধারে {purchases:,} লাখ টাকার উপাদান কেনেন। সরবরাহকারীদের টাকা দিতে কত দিন নেন?", r,
                f"Payable days = {pay:,} ÷ {purchases:,} x 365 = {r:g} days.",
                f"দেয়-দিন = {pay:,} ÷ {purchases:,} x 365 = {r:g} দিন।",
                (_c(purchases / pay), _c(pay / purchases * 100), _c(r * 2)), " days", " দিন")


def npm(profit, sales):
    r = _c(profit * 100 / sales)
    return _num(f"A firm earns a net profit of Rs {profit:,} lakh on sales of Rs {sales:,} lakh. What is its net profit margin?",
                f"একটা সংস্থা {sales:,} লাখ টাকার বিক্রিতে {profit:,} লাখ টাকা নিট লাভ করে। নিট লাভের মার্জিন কত?", r,
                f"{profit:,} ÷ {sales:,} x 100 = {r:g}%.",
                f"{profit:,} ÷ {sales:,} x 100 = {r:g}%।",
                (_c(sales / profit), _c(profit * 100 / (sales - profit)), _c(r * 2)), "%")


def roe(profit, equity):
    r = _c(profit * 100 / equity)
    return _num(f"A construction company makes Rs {profit:,} crore profit after tax with shareholders' equity of Rs {equity:,} crore. What is its return on equity?",
                f"একটা নির্মাণ-কোম্পানি {equity:,} কোটি টাকা শেয়ারহোল্ডার-মূলধনে কর-পরবর্তী {profit:,} কোটি টাকা লাভ করে। মূলধনে লাভের হার কত?", r,
                f"ROE = {profit:,} ÷ {equity:,} x 100 = {r:g}%.",
                f"মূলধনে লাভ = {profit:,} ÷ {equity:,} x 100 = {r:g}%।",
                (_c(equity / profit), _c(r / 2), _c(r + 10)), "%")


def quarterly(p, rate, years):
    a = round(p * (1 + rate / 400) ** (4 * years))
    yearly = round(p * (1 + rate / 100) ** years)
    return _rs(f"A fixed deposit of Rs {p:,} earns {rate}% a year, compounded quarterly. What is it worth after {years} year{'s' if years > 1 else ''}?",
               f"{p:,} টাকার একটা স্থায়ী আমানতে বছরে {rate}% সুদ, তিন মাস অন্তর চক্রবৃদ্ধি। {years} বছর পরে মূল্য কত?", a,
               f"{rate / 4:g}% each quarter for {4 * years} quarters: Rs {a:,}. Yearly compounding would give Rs {yearly:,}.",
               f"প্রতি ত্রৈমাসিকে {rate / 4:g}%, {4 * years}টি ত্রৈমাসিক: {a:,} টাকা। বার্ষিক চক্রবৃদ্ধিতে হতো {yearly:,} টাকা।",
               (yearly, p + p * rate * years // 100 if p + p * rate * years // 100 != yearly else yearly - 30, a - p))


def balance_after(p, rate, emi):
    i = p * rate // 1200
    r = p - (emi - i)
    return _rs(f"A Rs {p:,} loan at {rate}% a year has a monthly EMI of Rs {emi:,}. What is the balance owed after the first EMI?",
               f"বছরে {rate}% হারে {p:,} টাকার ঋণে মাসিক ইএমআই {emi:,} টাকা। প্রথম ইএমআই-এর পরে বকেয়া কত?", r,
               f"Interest for month 1 = {p:,} x {rate} ÷ 1,200 = {i:,}; principal repaid = {emi:,} - {i:,} = {emi - i:,}; balance = Rs {r:,}.",
               f"প্রথম মাসের সুদ = {p:,} x {rate} ÷ 1,200 = {i:,}; শোধ হওয়া আসল = {emi:,} - {i:,} = {emi - i:,}; বকেয়া = {r:,} টাকা।",
               (p - emi, p + i - emi + i, p - i))


def real_exact(nom, infl):
    r = _c(((1 + nom / 100) / (1 + infl / 100) - 1) * 100)
    return _num(f"An investment earns {nom}% while inflation is {infl}%. What is the exact real return? ((1 + nominal) ÷ (1 + inflation) - 1)",
                f"একটা বিনিয়োগ {nom}% আয় করে আর মুদ্রাস্ফীতি {infl}%। নিখুঁত প্রকৃত আয় কত? ((1 + নামিক) ÷ (1 + মুদ্রাস্ফীতি) - 1)", r,
                f"1.{nom:02d} ÷ 1.{infl:02d} - 1 = {r:g}%. The quick estimate {nom} - {infl} = {nom - infl}% is slightly too high.",
                f"1.{nom:02d} ÷ 1.{infl:02d} - 1 = {r:g}%। দ্রুত আন্দাজ {nom} - {infl} = {nom - infl}% একটু বেশি।",
                (nom - infl, nom + infl, _c(r / 2)), "%")


def premium(sum_assured, per_thousand):
    r = sum_assured // 1000 * per_thousand
    return _rs(f"A term insurance policy charges Rs {per_thousand} a year per Rs 1,000 of cover. What is the yearly premium for Rs {sum_assured:,} of cover?",
               f"একটা মেয়াদি বিমা প্রতি 1,000 টাকা সুরক্ষায় বছরে {per_thousand} টাকা নেয়। {sum_assured:,} টাকা সুরক্ষার বার্ষিক প্রিমিয়াম কত?", r,
               f"{sum_assured:,} ÷ 1,000 = {sum_assured // 1000:,} units; x Rs {per_thousand} = Rs {r:,}.",
               f"{sum_assured:,} ÷ 1,000 = {sum_assured // 1000:,} একক; x {per_thousand} টাকা = {r:,} টাকা।",
               (sum_assured * per_thousand // 100, r // 10, sum_assured // per_thousand))


def be_revenue(fixed, cm_pct):
    r = fixed * 100 // cm_pct
    return _rs(f"A precast yard has fixed costs of Rs {fixed:,} a month and a contribution margin of {cm_pct}% of sales. What sales revenue does it need to break even?",
               f"একটা প্রিকাস্ট-উঠানের মাসিক স্থির খরচ {fixed:,} টাকা আর অবদান-মার্জিন বিক্রির {cm_pct}%। লাভ-লোকসান সমান করতে কত বিক্রি-আয় লাগবে?", r,
               f"Break-even sales = fixed costs ÷ contribution margin = {fixed:,} ÷ {cm_pct}% = Rs {r:,}.",
               f"লাভ-লোকসান-সমান বিক্রি = স্থির খরচ ÷ অবদান-মার্জিন = {fixed:,} ÷ {cm_pct}% = {r:,} টাকা।",
               (fixed * cm_pct // 100, fixed + fixed * cm_pct // 100, r // 2))


ITEMS = (
    gst_split(100000, 18, "Steel brackets", "ইস্পাতের ব্র্যাকেট"), gst_split(50000, 28, "Cement", "সিমেন্ট"),
    gst_split(200000, 12, "Surveying services", "জরিপ-পরিষেবা"), gst_split(80000, 5, "Sand", "বালি"),
    slab_tax(500000), slab_tax(800000), slab_tax(1100000), slab_tax(650000),
    recv_days(60, 365), recv_days(100, 730), recv_days(45, 180), recv_days(30, 365),
    inv_days(40, 365), inv_days(150, 730), inv_days(36, 146),
    pay_days(55, 365), pay_days(35, 365),
    npm(12, 200), npm(45, 300), npm(8, 160), npm(72, 400),
    roe(30, 200), roe(21, 120), roe(50, 250), roe(9, 150),
    quarterly(100000, 8, 1), quarterly(50000, 12, 1), quarterly(200000, 6, 2),
    balance_after(500000, 12, 15000), balance_after(240000, 10, 8000), balance_after(1200000, 9, 25000),
    real_exact(10, 5), real_exact(8, 6), real_exact(12, 4), real_exact(7, 3),
    premium(5000000, 2), premium(2000000, 3), premium(8000000, 1),
    be_revenue(120000, 40), be_revenue(90000, 36), be_revenue(250000, 25), be_revenue(70000, 20),
    gst_split(300000, 18, "Bridge bearings", "সেতুর বিয়ারিং"), slab_tax(950000), recv_days(80, 400), quarterly(80000, 10, 1),
    balance_after(360000, 8, 12000), real_exact(9, 4), premium(3000000, 4),
    mcq("Why is GST split into CGST and SGST for sales within one state?", ["Half the tax goes to the central government and half to the state government", "To charge tax twice", "Because buyers prefer two bills", "It is not split"], 0,
        "For sales between states, IGST is charged instead and shared later.",
        "একই রাজ্যের মধ্যে বিক্রিতে জিএসটি সিজিএসটি আর এসজিএসটি-তে ভাগ হয় কেন?", ["করের অর্ধেক কেন্দ্রীয় সরকার আর অর্ধেক রাজ্য সরকার পায়", "দুবার কর নিতে", "ক্রেতারা দুটো বিল পছন্দ করেন", "ভাগ হয় না"],
        "দুই রাজ্যের মধ্যে বিক্রিতে তার বদলে আইজিএসটি নেওয়া হয় আর পরে ভাগ হয়।"),
    mcq("What is IGST?", ["Integrated GST charged on sales between different states", "A tax on imports of gold only", "An income tax", "A local toll"], 0,
        "It keeps the tax system seamless across state borders.",
        "আইজিএসটি কী?", ["আলাদা রাজ্যের মধ্যে বিক্রিতে নেওয়া সমন্বিত জিএসটি", "শুধু সোনা আমদানিতে কর", "আয়কর", "স্থানীয় টোল"],
        "রাজ্যের সীমানা পেরিয়ে কর-ব্যবস্থা মসৃণ রাখে।"),
    mcq("In a slab tax system, what does a 'marginal tax rate' mean?", ["The rate charged on the next rupee of income", "The average rate on all income", "A tax on margins only", "A fixed fee"], 0,
        "Moving into a higher slab taxes only the extra income at the higher rate.",
        "ধাপভিত্তিক কর-ব্যবস্থায় 'প্রান্তিক করহার' মানে কী?", ["আয়ের পরের টাকায় যে হারে কর", "সব আয়ের গড় হার", "শুধু মার্জিনে কর", "নির্দিষ্ট ফি"],
        "উঁচু ধাপে গেলে শুধু বাড়তি আয়েই উঁচু হারে কর।"),
    mcq("A pay rise moves a worker into a higher tax slab. Will their take-home pay fall?", ["No - only the extra income is taxed at the higher rate, so take-home pay still rises", "Yes - all income is taxed at the higher rate", "Yes - always", "Tax slabs do not exist"], 0,
        "This common myth discourages people from accepting promotions.",
        "বেতন বেড়ে একজন কর্মী উঁচু কর-ধাপে গেলেন। হাতে-পাওয়া বেতন কি কমবে?", ["না - শুধু বাড়তি আয়ে উঁচু হারে কর, তাই হাতে-পাওয়া বেতন তবু বাড়ে", "হ্যাঁ - সব আয়ে উঁচু হারে কর", "হ্যাঁ - সবসময়", "কর-ধাপ বলে কিছু নেই"],
        "এই প্রচলিত ভুল ধারণা মানুষকে পদোন্নতি নিতে নিরুৎসাহিত করে।"),
    mcq("What does a high number of 'receivable days' warn a contractor about?", ["Clients are slow to pay, tying up cash the firm needs", "The firm is very profitable", "Suppliers are paid too early", "Stock is too low"], 0,
        "Chasing payments and agreeing clear terms helps.",
        "বেশি 'প্রাপ্য-দিন' একজন ঠিকাদারকে কী নিয়ে সতর্ক করে?", ["গ্রাহকরা দেরিতে টাকা দিচ্ছেন, সংস্থার দরকারি নগদ আটকে যাচ্ছে", "সংস্থা খুব লাভজনক", "সরবরাহকারীদের খুব আগে টাকা দেওয়া হচ্ছে", "মজুত খুব কম"],
        "পাওনা আদায়ে তাগাদা আর স্পষ্ট শর্ত সাহায্য করে।"),
    mcq("What is the 'cash conversion cycle'?", ["Inventory days + receivable days - payable days: how long cash is tied up in operations", "The time to print money", "A bank's opening hours", "The life of a crane"], 0,
        "A shorter cycle means the business needs less working capital.",
        "'নগদ-রূপান্তর চক্র' কী?", ["মজুত-দিন + প্রাপ্য-দিন - দেয়-দিন: কাজে কতদিন নগদ আটকে থাকে", "টাকা ছাপার সময়", "ব্যাংক খোলার সময়", "ক্রেনের আয়ু"],
        "চক্র ছোট হলে ব্যবসার কম চলতি মূলধন লাগে।"),
    mcq("A firm has 60 inventory days, 75 receivable days and 45 payable days. What is its cash conversion cycle?", ["90 days", "180 days", "30 days", "120 days"], 0,
        "60 + 75 - 45 = 90 days.",
        "একটা সংস্থার মজুত-দিন 60, প্রাপ্য-দিন 75 আর দেয়-দিন 45। নগদ-রূপান্তর চক্র কত?", ["90 দিন", "180 দিন", "30 দিন", "120 দিন"],
        "60 + 75 - 45 = 90 দিন।"),
    mcq("What does 'return on equity' (ROE) measure?", ["How much profit a company makes for each rupee its shareholders have invested", "The share price", "Total debt", "Sales growth"], 0,
        "High ROE from heavy borrowing can hide high risk.",
        "'মূলধনে লাভের হার' (আরওই) কী মাপে?", ["শেয়ারহোল্ডারদের বিনিয়োগ করা প্রতি টাকায় কোম্পানি কত লাভ করে", "শেয়ারের দাম", "মোট ঋণ", "বিক্রির বৃদ্ধি"],
        "অনেক ধার করে পাওয়া বেশি আরওই উচ্চ ঝুঁকি লুকোতে পারে।"),
    mcq("Why does a bond's market price fall when interest rates rise?", ["New bonds pay more interest, so older bonds with lower fixed coupons are worth less", "Bonds become illegal", "The issuer stops paying", "Interest rates do not affect bonds"], 0,
        "Bond prices and interest rates move in opposite directions.",
        "সুদের হার বাড়লে বন্ডের বাজারদাম পড়ে কেন?", ["নতুন বন্ড বেশি সুদ দেয়, তাই কম নির্দিষ্ট কুপনের পুরোনো বন্ডের দাম কমে", "বন্ড বেআইনি হয়", "প্রদানকারী টাকা দেওয়া বন্ধ করে", "সুদের হার বন্ডে প্রভাব ফেলে না"],
        "বন্ডের দাম আর সুদের হার উল্টো দিকে চলে।"),
    mcq("What is a bond's 'yield'?", ["The return an investor actually gets, based on the price paid and the coupons", "The bond's face value", "The issuer's name", "A crop harvest"], 0,
        "Buying a bond below face value raises the yield above the coupon rate.",
        "বন্ডের 'ফলন' (ইল্ড) কী?", ["দেওয়া দাম আর কুপনের ভিত্তিতে বিনিয়োগকারী আসলে যে লাভ পান", "বন্ডের অভিহিত মূল্য", "প্রদানকারীর নাম", "ফসল কাটা"],
        "অভিহিত মূল্যের নিচে বন্ড কিনলে ফলন কুপন-হারের উপরে যায়।"),
    mcq("What is the main difference between raising money by debt and by equity?", ["Debt must be repaid with interest; equity gives investors a share of ownership and profits but need not be repaid", "They are identical", "Equity always has a fixed interest rate", "Debt gives voting rights"], 0,
        "Too much debt adds risk; too much new equity dilutes owners' control.",
        "ঋণ আর মূলধন দিয়ে টাকা তোলার প্রধান পার্থক্য কী?", ["ঋণ সুদসহ শোধ করতে হয়; মূলধন বিনিয়োগকারীকে মালিকানা আর লাভের ভাগ দেয়, শোধ করতে হয় না", "দুটো একই", "মূলধনে সবসময় নির্দিষ্ট সুদ", "ঋণ ভোটাধিকার দেয়"],
        "বেশি ঋণে ঝুঁকি বাড়ে; বেশি নতুন মূলধনে মালিকের নিয়ন্ত্রণ পাতলা হয়।"),
    mcq("Why might a bridge-building company issue new shares instead of borrowing?", ["To fund growth without adding interest payments it might struggle to meet", "Shares must be repaid with interest", "Banks never lend to builders", "Shares are cheaper to print"], 0,
        "Existing owners then hold a smaller percentage of the company.",
        "একটা সেতু-নির্মাণ কোম্পানি ধার না করে নতুন শেয়ার ছাড়তে পারে কেন?", ["এমন সুদের বোঝা না বাড়িয়ে বৃদ্ধির অর্থ জোগাতে, যা মেটাতে অসুবিধা হতে পারে", "শেয়ার সুদসহ শোধ করতে হয়", "ব্যাংক কখনো নির্মাতাদের ধার দেয় না", "শেয়ার ছাপা সস্তা"],
        "তখন পুরোনো মালিকরা কোম্পানির কম শতাংশের মালিক হন।"),
    mcq("What is 'dilution' for existing shareholders?", ["Their percentage ownership falls when a company issues new shares", "Adding water to paint", "Shares doubling in value", "A tax on shares"], 0,
        "Their share of a bigger company can still be worth more.",
        "বর্তমান শেয়ারহোল্ডারদের জন্য 'মালিকানা-তনুকরণ' কী?", ["কোম্পানি নতুন শেয়ার ছাড়লে তাদের মালিকানার শতাংশ কমে", "রঙে জল মেশানো", "শেয়ারের দাম দ্বিগুণ", "শেয়ারে কর"],
        "বড় কোম্পানিতে তাদের ভাগের মূল্য তবু বেশি হতে পারে।"),
    mcq("What is 'venture capital'?", ["Investment in young, high-growth companies in exchange for a share of ownership", "A loan for buying a house", "A type of tax", "Government grant for roads"], 0,
        "Start-ups developing new construction technology often use it.",
        "'উদ্যোগ-পুঁজি' (ভেঞ্চার ক্যাপিটাল) কী?", ["মালিকানার ভাগের বদলে নতুন, দ্রুত-বাড়ন্ত কোম্পানিতে বিনিয়োগ", "বাড়ি কেনার ঋণ", "এক রকম কর", "রাস্তার সরকারি অনুদান"],
        "নতুন নির্মাণ-প্রযুক্তি বানানো স্টার্ট-আপ প্রায়ই এটা নেয়।"),
    mcq("What is a 'recurring deposit' (RD)?", ["Saving a fixed amount every month for a set period, earning interest", "A one-time large deposit", "A loan repaid monthly", "A current account"], 0,
        "It builds the saving habit for goals like buying tools.",
        "'পৌনঃপুনিক আমানত' (আরডি) কী?", ["নির্দিষ্ট সময় ধরে প্রতি মাসে একটা নির্দিষ্ট অঙ্ক জমিয়ে সুদ পাওয়া", "একবারের বড় জমা", "মাসে মাসে শোধ করা ঋণ", "চলতি অ্যাকাউন্ট"],
        "যন্ত্র কেনার মতো লক্ষ্যে সঞ্চয়ের অভ্যাস গড়ে।"),
    mcq("Why is 'sum assured' in life insurance often suggested to be about 10 times yearly income?", ["It aims to replace the family's lost income for many years", "Insurers require exactly 10 times", "It makes premiums zero", "It is a legal rule"], 0,
        "Term insurance makes high cover affordable.",
        "জীবনবিমায় 'বিমাকৃত অঙ্ক' প্রায় বার্ষিক আয়ের 10 গুণ রাখার পরামর্শ দেওয়া হয় কেন?", ["অনেক বছর ধরে পরিবারের হারানো আয় পূরণের লক্ষ্যে", "বিমাকারী ঠিক 10 গুণ চায়", "প্রিমিয়াম শূন্য করে", "এটা আইনি নিয়ম"],
        "মেয়াদি বিমা বেশি সুরক্ষাকে সাধ্যের মধ্যে আনে।"),
    mcq("Why are premiums for life insurance higher for older applicants?", ["The chance of a claim during the policy term is higher", "Older people earn more", "Insurers dislike older people", "Premiums never change with age"], 0,
        "Buying cover young locks in a lower premium.",
        "বয়স্ক আবেদনকারীদের জীবনবিমার প্রিমিয়াম বেশি কেন?", ["পলিসির মেয়াদে দাবির সম্ভাবনা বেশি", "বয়স্করা বেশি আয় করেন", "বিমাকারী বয়স্কদের পছন্দ করে না", "বয়সের সঙ্গে প্রিমিয়াম বদলায় না"],
        "অল্প বয়সে সুরক্ষা কিনলে কম প্রিমিয়াম বাঁধা থাকে।"),
    mcq("What is 'contractor's all-risk' (CAR) insurance on a bridge project?", ["Cover for damage to the works, materials and third parties during construction", "Car insurance for the contractor's car", "Health insurance for workers only", "A tax on contractors"], 0,
        "Floods, fire or collapse during building can be very costly.",
        "সেতু-প্রকল্পে 'ঠিকাদারের সর্বঝুঁকি' (সিএআর) বিমা কী?", ["নির্মাণের সময় কাজ, উপাদান আর তৃতীয় পক্ষের ক্ষতির সুরক্ষা", "ঠিকাদারের গাড়ির বিমা", "শুধু কর্মীদের স্বাস্থ্যবিমা", "ঠিকাদারদের উপর কর"],
        "নির্মাণের সময় বন্যা, আগুন বা ধস খুব দামি হতে পারে।"),
    mcq("What is 'public liability' insurance for a contractor?", ["Cover if the public is injured or their property is damaged by the work", "Insurance for the contractor's health", "A government loan", "A tax on profits"], 0,
        "Falling objects or blocked access can lead to claims.",
        "ঠিকাদারের জন্য 'জনদায়' বিমা কী?", ["কাজের জন্য জনসাধারণ আহত হলে বা তাদের সম্পত্তির ক্ষতি হলে সুরক্ষা", "ঠিকাদারের স্বাস্থ্যবিমা", "সরকারি ঋণ", "লাভের উপর কর"],
        "পড়ে যাওয়া জিনিস বা আটকানো পথ থেকে দাবি আসতে পারে।"),
    mcq("What is 'workmen's compensation' (employees' compensation) insurance?", ["Cover that pays workers or their families if they are injured or killed at work", "Extra pay for overtime", "A pension", "A bonus for safety"], 0,
        "In India, the Employees' Compensation Act sets rules for this.",
        "'শ্রমিক-ক্ষতিপূরণ' (কর্মচারী-ক্ষতিপূরণ) বিমা কী?", ["কাজে আহত বা নিহত হলে কর্মী বা তাঁর পরিবারকে টাকা দেওয়ার সুরক্ষা", "ওভারটাইমের বাড়তি বেতন", "পেনশন", "নিরাপত্তার বোনাস"],
        "ভারতে কর্মচারী-ক্ষতিপূরণ আইন এর নিয়ম ঠিক করে।"),
    mcq("Why do public bridge contracts require performance and payment guarantees from banks?", ["They protect the public if the contractor fails to finish or to pay its subcontractors", "To make banks richer", "To delay payments", "They are optional extras"], 0,
        "The bank pays if the contractor defaults, up to the guarantee amount.",
        "সরকারি সেতু-চুক্তিতে ব্যাংকের কাজ-সম্পাদন আর পেমেন্ট-গ্যারান্টি চাওয়া হয় কেন?", ["ঠিকাদার কাজ শেষ বা উপ-ঠিকাদারদের টাকা দিতে ব্যর্থ হলে জনসাধারণকে রক্ষা করে", "ব্যাংককে ধনী করতে", "পেমেন্টে দেরি করাতে", "ঐচ্ছিক বাড়তি"],
        "ঠিকাদার খেলাপি হলে গ্যারান্টির অঙ্ক পর্যন্ত ব্যাংক টাকা দেয়।"),
    mcq("What does 'escrow account' mean in a toll-bridge project?", ["A special account where toll income is held and paid out in a fixed order, such as lenders first", "A secret account", "A personal savings account", "An account for staff lunches"], 0,
        "It protects lenders and ensures maintenance is funded.",
        "টোল-সেতু প্রকল্পে 'এসক্রো অ্যাকাউন্ট' মানে কী?", ["বিশেষ অ্যাকাউন্ট, যেখানে টোলের আয় রেখে নির্দিষ্ট ক্রমে, যেমন আগে ঋণদাতাদের, দেওয়া হয়", "গোপন অ্যাকাউন্ট", "ব্যক্তিগত সঞ্চয়-অ্যাকাউন্ট", "কর্মীদের দুপুরের খাবারের অ্যাকাউন্ট"],
        "ঋণদাতাদের রক্ষা করে আর রক্ষণাবেক্ষণের টাকা নিশ্চিত করে।"),
    mcq("What is a 'debt service reserve account' (DSRA)?", ["Cash set aside to cover a few months of loan repayments if income dips", "A fund for buying cranes", "A tax refund account", "A shareholder dividend"], 0,
        "It gives a project breathing space in a bad season.",
        "'ঋণ-পরিশোধ সংরক্ষিত অ্যাকাউন্ট' (ডিএসআরএ) কী?", ["আয় কমলে কয়েক মাসের ঋণ-শোধ মেটাতে সরিয়ে রাখা নগদ", "ক্রেন কেনার তহবিল", "করের ফেরত-অ্যাকাউন্ট", "শেয়ারহোল্ডারের লভ্যাংশ"],
        "খারাপ মরসুমে প্রকল্পকে শ্বাস নেওয়ার সময় দেয়।"),
    mcq("What does 'net worth' mean for a family planning a home loan?", ["Total assets minus total debts", "Monthly salary only", "The value of the house only", "The loan amount"], 0,
        "Lenders look at net worth and income together.",
        "গৃহঋণের পরিকল্পনা করা পরিবারের জন্য 'নিট সম্পদ' মানে কী?", ["মোট সম্পদ বিয়োগ মোট দেনা", "শুধু মাসিক বেতন", "শুধু বাড়ির মূল্য", "ঋণের অঙ্ক"],
        "ঋণদাতারা নিট সম্পদ আর আয় একসঙ্গে দেখেন।"),
    mcq("Why do lenders limit EMIs to around 40-50% of a borrower's income?", ["To leave enough for living costs so the borrower can keep repaying", "To make loans bigger", "It is the same for everyone by law", "To charge more interest"], 0,
        "Over-borrowing is a common cause of family financial stress.",
        "ঋণদাতারা ইএমআই ঋণগ্রহীতার আয়ের প্রায় 40-50%-এ সীমিত রাখেন কেন?", ["জীবনযাত্রার খরচের জন্য যথেষ্ট রাখতে, যাতে ঋণগ্রহীতা শোধ চালিয়ে যেতে পারেন", "ঋণ বড় করতে", "আইনে সবার জন্য একই", "বেশি সুদ নিতে"],
        "অতিরিক্ত ধার পারিবারিক আর্থিক চাপের সাধারণ কারণ।"),
    mcq("What happens to total interest paid if a loan's tenure is stretched from 10 to 20 years at the same rate?", ["The EMI falls, but the total interest paid rises a lot", "Total interest falls", "Nothing changes", "The loan becomes free"], 0,
        "Shorter loans cost less overall if you can afford the EMI.",
        "একই হারে ঋণের মেয়াদ 10 থেকে 20 বছর করলে মোট সুদের কী হয়?", ["ইএমআই কমে, কিন্তু মোট সুদ অনেক বাড়ে", "মোট সুদ কমে", "কিছু বদলায় না", "ঋণ বিনামূল্যে হয়"],
        "ইএমআই সামলাতে পারলে ছোট মেয়াদের ঋণে মোট খরচ কম।"),
    mcq("What is a 'prepayment' on a loan?", ["Paying off part of the loan early, reducing future interest", "Paying the EMI late", "Taking a second loan", "A fee for opening an account"], 0,
        "Check whether the loan has prepayment charges.",
        "ঋণে 'আগাম পরিশোধ' কী?", ["ঋণের একটা অংশ আগেভাগে শোধ করা, ভবিষ্যৎ সুদ কমে", "দেরিতে ইএমআই দেওয়া", "দ্বিতীয় ঋণ নেওয়া", "অ্যাকাউন্ট খোলার ফি"],
        "ঋণে আগাম-শোধের চার্জ আছে কিনা দেখে নাও।"),
    mcq("Why is the exact real return slightly less than 'interest minus inflation'?", ["Inflation also erodes the interest earned, not just the original sum", "Banks take a fee", "Inflation is always zero", "It is always more"], 0,
        "For small rates the quick estimate is close enough.",
        "নিখুঁত প্রকৃত আয় 'সুদ বিয়োগ মুদ্রাস্ফীতি'-র চেয়ে একটু কম কেন?", ["মুদ্রাস্ফীতি শুধু মূল টাকা নয়, অর্জিত সুদের মূল্যও কমায়", "ব্যাংক ফি নেয়", "মুদ্রাস্ফীতি সবসময় শূন্য", "সবসময় বেশি"],
        "ছোট হারে দ্রুত আন্দাজ যথেষ্ট কাছাকাছি।"),
    mcq("What is 'stagflation'?", ["High inflation together with slow growth and high unemployment", "Fast growth with no inflation", "Falling prices", "A type of bridge"], 0,
        "It is hard for governments to fix because usual remedies conflict.",
        "'স্ট্যাগফ্লেশন' কী?", ["উচ্চ মুদ্রাস্ফীতির সঙ্গে ধীর বৃদ্ধি আর উচ্চ বেকারত্ব", "মুদ্রাস্ফীতিহীন দ্রুত বৃদ্ধি", "দাম পড়া", "এক রকম সেতু"],
        "সরকারের পক্ষে সারানো কঠিন, কারণ সাধারণ প্রতিকারগুলো পরস্পরবিরোধী।"),
    mcq("What is 'deflation' and why can it hurt the economy?", ["Falling prices; people delay buying, so firms cut jobs and wages", "Rising prices", "A bank's interest rate", "Letting air out of tyres"], 0,
        "Mild, steady inflation is usually considered healthier.",
        "'মূল্যহ্রাস' (ডিফ্লেশন) কী আর কেন অর্থনীতির ক্ষতি করতে পারে?", ["দাম পড়া; মানুষ কেনা পিছোয়, তাই সংস্থা চাকরি আর মজুরি ছাঁটে", "দাম বাড়া", "ব্যাংকের সুদের হার", "টায়ারের হাওয়া ছাড়া"],
        "মৃদু, স্থির মুদ্রাস্ফীতিকে সাধারণত বেশি স্বাস্থ্যকর ধরা হয়।"),
    mcq("What is GDP?", ["Gross domestic product - the total value of goods and services produced in a country in a year", "A type of government bond", "The number of bridges", "Gold deposits"], 0,
        "Infrastructure spending counts towards GDP and helps it grow.",
        "জিডিপি কী?", ["মোট দেশজ উৎপাদন - এক বছরে দেশে উৎপাদিত পণ্য-পরিষেবার মোট মূল্য", "এক রকম সরকারি বন্ড", "সেতুর সংখ্যা", "সোনার মজুত"],
        "পরিকাঠামোর খরচ জিডিপিতে গোনা হয় আর বৃদ্ধিতে সাহায্য করে।"),
    mcq("What is the 'multiplier effect' of building a new bridge?", ["Money spent on wages and materials is spent again by workers and suppliers, boosting the economy more than the original sum", "Bridges multiply themselves", "Taxes double", "Costs multiply"], 0,
        "Local shops, transport and services all benefit.",
        "নতুন সেতু বানানোর 'গুণক প্রভাব' কী?", ["মজুরি আর উপাদানে খরচ হওয়া টাকা কর্মী আর সরবরাহকারীরা আবার খরচ করেন, মূল অঙ্কের চেয়ে বেশি অর্থনীতি চাঙ্গা হয়", "সেতু নিজেরাই বাড়ে", "কর দ্বিগুণ হয়", "খরচ বহুগুণ হয়"],
        "স্থানীয় দোকান, পরিবহন আর পরিষেবা সবাই লাভবান হয়।"),
    mcq("What does 'financial inclusion' mean?", ["Everyone having access to basic banking, credit, insurance and payments", "Only rich people using banks", "Closing small bank branches", "Paying only in cash"], 0,
        "Bank accounts let construction workers receive wages safely.",
        "'আর্থিক অন্তর্ভুক্তি' মানে কী?", ["সবার কাছে মৌলিক ব্যাংকিং, ঋণ, বিমা আর লেনদেনের সুযোগ", "শুধু ধনীদের ব্যাংক ব্যবহার", "ছোট ব্যাংক-শাখা বন্ধ", "শুধু নগদে লেনদেন"],
        "ব্যাংক-অ্যাকাউন্ট নির্মাণ-শ্রমিকদের নিরাপদে মজুরি পেতে দেয়।"),
    mcq("Why is paying wages directly into bank accounts better than in cash on site?", ["It is safer, leaves a record and helps workers build savings and a credit history", "Cash is illegal", "Banks pay extra wages", "It is slower for no reason"], 0,
        "It also reduces the risk of theft and underpayment.",
        "নির্মাণস্থলে নগদের বদলে সরাসরি ব্যাংক-অ্যাকাউন্টে মজুরি দেওয়া ভালো কেন?", ["নিরাপদ, নথি থাকে আর কর্মীদের সঞ্চয় আর ঋণ-ইতিহাস গড়তে সাহায্য করে", "নগদ বেআইনি", "ব্যাংক বাড়তি মজুরি দেয়", "অকারণে ধীর"],
        "চুরি আর কম মজুরি দেওয়ার ঝুঁকিও কমায়।"),
    mcq("What is 'wage theft'?", ["Not paying workers what they are legally owed, such as unpaid overtime or below minimum wage", "Workers stealing tools", "A bank robbery", "Paying wages early"], 0,
        "Workers can complain to the labour department.",
        "'মজুরি-চুরি' কী?", ["কর্মীদের আইনত প্রাপ্য না দেওয়া, যেমন ওভারটাইম না দেওয়া বা ন্যূনতম মজুরির কম দেওয়া", "কর্মীদের যন্ত্র চুরি", "ব্যাংক-ডাকাতি", "আগে মজুরি দেওয়া"],
        "কর্মীরা শ্রম-দপ্তরে অভিযোগ করতে পারেন।"),
    mcq("What is the Building and Other Construction Workers (BOCW) welfare fund in India for?", ["Funded by a cess on construction costs, it provides benefits like pensions, insurance and education help to registered workers", "Paying contractors' profits", "Buying cranes", "A tax refund for builders"], 0,
        "Workers must register to claim the benefits.",
        "ভারতে ভবন ও অন্যান্য নির্মাণ-শ্রমিক (বিওসিডব্লিউ) কল্যাণ-তহবিল কীসের জন্য?", ["নির্মাণ-খরচের উপর সেসে চলে, নিবন্ধিত শ্রমিকদের পেনশন, বিমা আর শিক্ষা-সহায়তার মতো সুবিধা দেয়", "ঠিকাদারদের লাভ দেওয়া", "ক্রেন কেনা", "নির্মাতাদের করের ফেরত"],
        "সুবিধা দাবি করতে শ্রমিকদের নিবন্ধন করতে হয়।"),
    mcq("A cess of 1% is charged on a Rs 50 crore bridge project for the construction workers' welfare fund. How much is collected?", ["Rs 50 lakh", "Rs 5 lakh", "Rs 5 crore", "Rs 50,000"], 0,
        "50,00,00,000 x 1% = 50,00,000.",
        "50 কোটি টাকার সেতু-প্রকল্পে নির্মাণ-শ্রমিক কল্যাণ-তহবিলের জন্য 1% সেস নেওয়া হয়। কত আদায় হয়?", ["50 লাখ টাকা", "5 লাখ টাকা", "5 কোটি টাকা", "50,000 টাকা"],
        "50,00,00,000 x 1% = 50,00,000।"),
    mcq("What is 'transparency' in public finance for a bridge project?", ["Publishing budgets, contracts and spending so citizens can check how money is used", "Hiding the accounts", "Using glass in the bridge", "Paying in cash only"], 0,
        "Open data and social audits discourage corruption.",
        "সেতু-প্রকল্পের সরকারি অর্থে 'স্বচ্ছতা' কী?", ["বাজেট, চুক্তি আর খরচ প্রকাশ করা, যাতে নাগরিকরা টাকা কীভাবে খরচ হয় যাচাই করতে পারেন", "হিসাব লুকোনো", "সেতুতে কাচ ব্যবহার", "শুধু নগদে দেওয়া"],
        "খোলা তথ্য আর সামাজিক নিরীক্ষা দুর্নীতি নিরুৎসাহিত করে।"),
    mcq("What is a 'social audit' of a public works project?", ["Local people review records and visit the site to check that the work and payments were real", "An audit of a social media account", "A party for workers", "A tax inspection only"], 0,
        "It is used in schemes such as MGNREGA in India.",
        "সরকারি কাজের প্রকল্পের 'সামাজিক নিরীক্ষা' কী?", ["স্থানীয় মানুষ নথি দেখে আর নির্মাণস্থলে গিয়ে যাচাই করেন কাজ আর পেমেন্ট সত্যি কিনা", "সামাজিক মাধ্যমের অ্যাকাউন্টের নিরীক্ষা", "কর্মীদের ভোজ", "শুধু কর-পরিদর্শন"],
        "ভারতে মনরেগার মতো প্রকল্পে ব্যবহার হয়।"),
    mcq("A contractor discovers a client overpaid an invoice by Rs 2 lakh. What is the honest action?", ["Tell the client and refund or credit the money", "Keep it quietly", "Spend it quickly", "Blame the bank"], 0,
        "Honesty protects reputation and long-term business.",
        "একজন ঠিকাদার দেখলেন গ্রাহক একটা চালানে 2 লাখ টাকা বেশি দিয়েছেন। সৎ পদক্ষেপ কী?", ["গ্রাহককে জানিয়ে টাকা ফেরত দেওয়া বা জমা করা", "চুপচাপ রেখে দেওয়া", "তাড়াতাড়ি খরচ করা", "ব্যাংককে দোষ দেওয়া"],
        "সততা সুনাম আর দীর্ঘমেয়াদি ব্যবসা রক্ষা করে।"),
    mcq("What is 'insider trading'?", ["Buying or selling shares using important information not yet public", "Trading inside a shop", "Buying shares online", "Selling to friends"], 0,
        "It is illegal because it cheats other investors; SEBI prosecutes it.",
        "'অভ্যন্তরীণ লেনদেন' (ইনসাইডার ট্রেডিং) কী?", ["এখনো প্রকাশিত হয়নি এমন জরুরি তথ্য কাজে লাগিয়ে শেয়ার কেনা-বেচা", "দোকানের ভেতরে কেনাবেচা", "অনলাইনে শেয়ার কেনা", "বন্ধুদের কাছে বেচা"],
        "অন্য বিনিয়োগকারীদের ঠকায় বলে বেআইনি; সেবি এর বিচার করে।"),
    mcq("A worker hears at the office that their company will win a huge bridge contract next week. Should they buy its shares now?", ["No - trading on unpublished price-sensitive information is insider trading and illegal", "Yes - it is a great tip", "Yes - but only a few", "Only if a friend agrees"], 0,
        "Wait until the news is officially public.",
        "একজন কর্মী অফিসে শুনলেন তাঁর কোম্পানি পরের সপ্তাহে একটা বিশাল সেতু-চুক্তি পাবে। এখন কি এর শেয়ার কেনা উচিত?", ["না - অপ্রকাশিত দাম-সংবেদনশীল তথ্যে লেনদেন অভ্যন্তরীণ লেনদেন আর বেআইনি", "হ্যাঁ - দারুণ খবর", "হ্যাঁ - তবে অল্প কয়েকটা", "শুধু বন্ধু রাজি হলে"],
        "খবর সরকারিভাবে প্রকাশ হওয়া পর্যন্ত অপেক্ষা করো।"),
    mcq("What is the role of SEBI?", ["Regulating India's securities markets to protect investors", "Building bridges", "Collecting income tax", "Printing banknotes"], 0,
        "It sets rules for listed companies, brokers and mutual funds.",
        "সেবি-র ভূমিকা কী?", ["বিনিয়োগকারীদের রক্ষায় ভারতের সিকিউরিটিজ-বাজার নিয়ন্ত্রণ", "সেতু বানানো", "আয়কর আদায়", "নোট ছাপানো"],
        "তালিকাভুক্ত কোম্পানি, ব্রোকার আর মিউচুয়াল ফান্ডের নিয়ম ঠিক করে।"),
    mcq("Why is diversifying across many companies safer than putting all savings in one bridge-building company's shares?", ["If that one company fails, you do not lose everything", "One company always grows", "Diversification guarantees profit", "It is not safer"], 0,
        "Even good companies can hit trouble from a single failed project.",
        "সব সঞ্চয় একটা সেতু-নির্মাণ কোম্পানির শেয়ারে না রেখে অনেক কোম্পানিতে ছড়ানো নিরাপদ কেন?", ["সেই একটা কোম্পানি ব্যর্থ হলে সব হারাতে হয় না", "একটা কোম্পানি সবসময় বাড়ে", "বৈচিত্র্য লাভের নিশ্চয়তা দেয়", "নিরাপদ নয়"],
        "ভালো কোম্পানিও একটা ব্যর্থ প্রকল্পে বিপদে পড়তে পারে।"),
    mcq("What is an 'index fund'?", ["A fund that simply holds all the shares in a market index, with low fees", "A fund run by guessing", "A bank fixed deposit", "A fund for one company only"], 0,
        "It gives broad diversification cheaply.",
        "'ইনডেক্স ফান্ড' কী?", ["যে তহবিল কম ফি-তে একটা বাজার-সূচকের সব শেয়ার রাখে", "আন্দাজে চালানো তহবিল", "ব্যাংকের স্থায়ী আমানত", "শুধু একটা কোম্পানির তহবিল"],
        "সস্তায় বিস্তৃত বৈচিত্র্য দেয়।"),
    mcq("Why do mutual fund fees (expense ratios) matter over the long term?", ["Even 1% a year compounds into a large difference in final savings", "Fees are always zero", "Higher fees always mean higher returns", "Fees are paid only once"], 0,
        "Compare costs as carefully as past performance.",
        "দীর্ঘমেয়াদে মিউচুয়াল ফান্ডের ফি (খরচ-অনুপাত) জরুরি কেন?", ["বছরে 1%-ও চক্রবৃদ্ধিতে শেষ সঞ্চয়ে বড় পার্থক্য গড়ে", "ফি সবসময় শূন্য", "বেশি ফি মানে সবসময় বেশি লাভ", "ফি একবারই দিতে হয়"],
        "অতীতের ফলের মতোই খরচও যত্ন করে তুলনা করো।"),
    mcq("What are NEFT and RTGS used for?", ["Transferring money electronically between bank accounts; RTGS is for large, immediate payments", "Paying road tolls only", "Taking out cash", "Buying shares only"], 0,
        "Contractors often receive big stage payments by RTGS.",
        "এনইএফটি আর আরটিজিএস কীসের জন্য ব্যবহার হয়?", ["ব্যাংক-অ্যাকাউন্টের মধ্যে ইলেকট্রনিকভাবে টাকা পাঠাতে; আরটিজিএস বড়, তাৎক্ষণিক পেমেন্টের জন্য", "শুধু রাস্তার টোল দিতে", "নগদ তুলতে", "শুধু শেয়ার কিনতে"],
        "ঠিকাদাররা প্রায়ই আরটিজিএস-এ বড় ধাপের পেমেন্ট পান।"),
    mcq("What is a PAN card used for?", ["A permanent tax ID needed for filing returns, big transactions and opening many accounts", "A driving licence", "A voter card only", "A gas connection"], 0,
        "Keep it safe - misuse of someone's PAN can lead to fraud.",
        "প্যান কার্ড কীসের জন্য ব্যবহার হয়?", ["রিটার্ন জমা, বড় লেনদেন আর অনেক অ্যাকাউন্ট খুলতে লাগা স্থায়ী কর-পরিচয়", "ড্রাইভিং লাইসেন্স", "শুধু ভোটার কার্ড", "গ্যাস-সংযোগ"],
        "নিরাপদে রাখো - কারও প্যানের অপব্যবহারে প্রতারণা হতে পারে।"),
    mcq("Why should a salaried site engineer file an income tax return even if tax was deducted at source?", ["To report income correctly, claim refunds or deductions, and build a record useful for loans and visas", "It is never needed", "To pay double tax", "Only companies file returns"], 0,
        "Form 16 from the employer summarises salary and TDS.",
        "উৎসে কর কাটা হলেও একজন বেতনভোগী নির্মাণ-প্রকৌশলীর আয়কর রিটার্ন জমা দেওয়া উচিত কেন?", ["ঠিকমতো আয় জানাতে, ফেরত বা ছাড় দাবি করতে আর ঋণ ও ভিসার কাজে লাগা নথি গড়তে", "কখনো দরকার হয় না", "দুবার কর দিতে", "শুধু কোম্পানি রিটার্ন জমা দেয়"],
        "নিয়োগকর্তার ফর্ম 16 বেতন আর টিডিএস-এর সারাংশ দেয়।"),
    mcq("Why should a worker add a 'nominee' to their bank account and provident fund?", ["So the money can be passed quickly to the chosen person if the worker dies", "To share the PIN", "To double the interest", "It is not allowed"], 0,
        "It saves families long legal delays at a hard time.",
        "একজন কর্মীর ব্যাংক-অ্যাকাউন্ট আর ভবিষ্যনিধিতে 'মনোনীত ব্যক্তি' যোগ করা উচিত কেন?", ["কর্মী মারা গেলে টাকা যাতে দ্রুত বাছাই-করা মানুষের কাছে যায়", "পিন ভাগ করতে", "সুদ দ্বিগুণ করতে", "অনুমোদিত নয়"],
        "কঠিন সময়ে পরিবারকে দীর্ঘ আইনি দেরি থেকে বাঁচায়।"),
    mcq("What is 'compounding' of returns in a long-term SIP?", ["Earnings are reinvested and themselves earn returns, growing faster over time", "Paying fees twice", "Returns staying flat", "A one-time deposit"], 0,
        "Starting early gives compounding the most time to work.",
        "দীর্ঘমেয়াদি এসআইপি-তে আয়ের 'চক্রবৃদ্ধি' কী?", ["আয় আবার বিনিয়োগ হয়ে নিজেও আয় করে, সময়ের সঙ্গে দ্রুত বাড়ে", "দুবার ফি দেওয়া", "আয় একই থাকা", "একবারের জমা"],
        "আগে শুরু করলে চক্রবৃদ্ধি সবচেয়ে বেশি সময় পায়।"),
)
