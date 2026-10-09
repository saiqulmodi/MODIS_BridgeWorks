"""NIT level - Commercials (accountancy, cost accounting, operations and business management at
entrance and first-year B.Tech/BBA standard): accounting concepts and statements, depreciation,
partnership and company accounts, cost and variance analysis, marginal costing, PERT/CPM scheduling,
inventory and quality control, productivity, marketing, management principles and commercial law."""
from . import mcq


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def _o(r, *alts):
    out = []
    for x in (r, *alts, r * 2, r + 1, r * 3, r + 10):
        x = _c(x)
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _f(x):
    return f"{x:,}" if isinstance(x, int) else f"{x:,.2f}".rstrip("0").rstrip(".")


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None, pre=""):
    r = _c(r)
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [pre + _f(x) + u_en for x in o], 0, ex_en, q_bn, [pre + _f(x) + ub for x in o], ex_bn)


def _rs(q_en, q_bn, r, ex_en, ex_bn, alts):
    return _n(q_en, q_bn, r, ex_en, ex_bn, alts, pre="Rs ")


# ---------------------------------------------------------------- financial accounting
def equation(assets, liab):
    cap = assets - liab
    return _rs(f"A contractor's business has assets of Rs {assets:,} and outside liabilities of Rs {liab:,}. What is the owner's capital?",
               f"একজন ঠিকাদারের ব্যবসার সম্পদ Rs {assets:,} আর বাইরের দায় Rs {liab:,}। মালিকের মূলধন কত?", cap,
               f"Accounting equation: Assets = Liabilities + Capital, so Capital = {assets:,} - {liab:,} = Rs {cap:,}.",
               f"হিসাব-সমীকরণ: সম্পদ = দায় + মূলধন, তাই মূলধন = {assets:,} - {liab:,} = Rs {cap:,}।",
               (assets + liab, liab, assets))


def slm(cost, salv, life):
    d = (cost - salv) / life
    return _rs(f"A concrete mixer costs Rs {cost:,}, will be sold for Rs {salv:,} after {life} years. What is the yearly depreciation by the straight-line method?",
               f"একটা কংক্রিট মিক্সারের দাম Rs {cost:,}, {life} বছর পরে Rs {salv:,}-এ বিক্রি হবে। সরলরৈখিক পদ্ধতিতে বার্ষিক অবচয় কত?", d,
               f"(cost - salvage) ÷ life = ({cost:,} - {salv:,}) ÷ {life} = Rs {_f(_c(d))} every year.",
               f"(দাম - অবশেষ মূল্য) ÷ আয়ু = ({cost:,} - {salv:,}) ÷ {life} = প্রতি বছর Rs {_f(_c(d))}।",
               (cost / life, (cost + salv) / life, d * 1.5))


def wdv(cost, rate, n):
    v = cost * (1 - rate / 100) ** n
    return _rs(f"A truck bought for Rs {cost:,} is depreciated at {rate}% a year on the written-down value. What is its book value after {n} years?",
               f"Rs {cost:,}-এ কেনা একটা ট্রাকের হ্রাসমান মূল্যে বছরে {rate}% অবচয় হয়। {n} বছর পরে এর বই-মূল্য কত?", v,
               f"Book value = cost x (1 - rate)ⁿ = {cost:,} x {1 - rate / 100:g}^{n} = Rs {_f(_c(v))}.",
               f"বই-মূল্য = দাম x (1 - হার)ⁿ = {cost:,} x {1 - rate / 100:g}^{n} = Rs {_f(_c(v))}।",
               (cost * (1 - rate * n / 100), cost * (1 - rate / 100), v * 0.9))


def cogs(opening, purchases, closing):
    c = opening + purchases - closing
    return _rs(f"A hardware shop had opening stock of Rs {opening:,}, bought goods for Rs {purchases:,} and has closing stock of Rs {closing:,}. What is the cost of goods sold?",
               f"একটা হার্ডওয়্যার দোকানের প্রারম্ভিক মজুত Rs {opening:,}, ক্রয় Rs {purchases:,} আর সমাপনী মজুত Rs {closing:,}। বিক্রীত পণ্যের ব্যয় কত?", c,
               f"COGS = opening stock + purchases - closing stock = {opening:,} + {purchases:,} - {closing:,} = Rs {c:,}.",
               f"বিক্রীত পণ্যের ব্যয় = প্রারম্ভিক মজুত + ক্রয় - সমাপনী মজুত = {opening:,} + {purchases:,} - {closing:,} = Rs {c:,}।",
               (opening + purchases + closing, purchases, purchases - closing))


def gross_margin(sales, cost):
    g = (sales - cost) / sales * 100
    return _n(f"Sales are Rs {sales:,} and the cost of goods sold is Rs {cost:,}. What is the gross profit margin?",
              f"বিক্রি Rs {sales:,} আর বিক্রীত পণ্যের ব্যয় Rs {cost:,}। মোট মুনাফার হার কত?", g,
              f"(sales - COGS) ÷ sales = {sales - cost:,} ÷ {sales:,} = {_f(_c(g))}%.",
              f"(বিক্রি - ব্যয়) ÷ বিক্রি = {sales - cost:,} ÷ {sales:,} = {_f(_c(g))}%।",
              ((sales - cost) / cost * 100, cost / sales * 100, g / 2), "%")


def goodwill_avg(profits, years):
    avg = sum(profits) / len(profits)
    g = avg * years
    txt = ", ".join(f"Rs {p:,}" for p in profits)
    return _rs(f"A firm's profits over the last {len(profits)} years were {txt}. What is goodwill at {years} years' purchase of the average profit?",
               f"একটা ফার্মের গত {len(profits)} বছরের মুনাফা {txt}। গড় মুনাফার {years} বছরের ক্রয়-মূল্যে সুনাম কত?", g,
               f"Average profit = Rs {_f(_c(avg))}; goodwill = {_f(_c(avg))} x {years} = Rs {_f(_c(g))}.",
               f"গড় মুনাফা = Rs {_f(_c(avg))}; সুনাম = {_f(_c(avg))} x {years} = Rs {_f(_c(g))}।",
               (sum(profits), avg, sum(profits) * years))


def super_profit(avg, capital, rate, years):
    sp = avg - capital * rate / 100
    g = sp * years
    return _rs(f"A firm earns an average profit of Rs {avg:,} on capital of Rs {capital:,}; the normal return is {rate}%. What is goodwill at {years} years' purchase of super profit?",
               f"একটা ফার্ম Rs {capital:,} মূলধনে গড়ে Rs {avg:,} মুনাফা করে; স্বাভাবিক আয় {rate}%। অতি-মুনাফার {years} বছরের ক্রয়-মূল্যে সুনাম কত?", g,
               f"Normal profit = {capital:,} x {rate}% = Rs {_f(_c(capital * rate / 100))}; super profit = Rs {_f(_c(sp))}; goodwill = {_f(_c(sp))} x {years} = Rs {_f(_c(g))}.",
               f"স্বাভাবিক মুনাফা = {capital:,} x {rate}% = Rs {_f(_c(capital * rate / 100))}; অতি-মুনাফা = Rs {_f(_c(sp))}; সুনাম = {_f(_c(sp))} x {years} = Rs {_f(_c(g))}।",
               (avg * years, sp, capital * rate / 100 * years))


def capital_interest(cap, rate, months):
    i = cap * rate / 100 * months / 12
    return _rs(f"A partner's capital is Rs {cap:,} and the deed allows {rate}% a year interest on capital. How much interest is credited for {months} months?",
               f"একজন অংশীদারের মূলধন Rs {cap:,}, আর চুক্তিপত্রে মূলধনের উপর বছরে {rate}% সুদ দেওয়ার কথা। {months} মাসের জন্য কত সুদ জমা হয়?", i,
               f"{cap:,} x {rate}% x {months}/12 = Rs {_f(_c(i))}.",
               f"সুদ = {cap:,} x {rate}% x {months}/12 = Rs {_f(_c(i))}।",
               (cap * rate / 100, i / 2, i + cap / 100))


def premium(n, face, prem):
    v = n * prem
    return _rs(f"A company issues {n:,} shares of Rs {face} each at a premium of Rs {prem}. How much is credited to the Securities Premium account?",
               f"একটা কোম্পানি Rs {face} মূল্যের {n:,}টি শেয়ার Rs {prem} প্রিমিয়ামে ইস্যু করে। সিকিউরিটিজ প্রিমিয়াম খাতে কত জমা হয়?", v,
               f"Only the premium part goes there: {n:,} x Rs {prem} = Rs {v:,}; {n:,} x Rs {face} goes to share capital.",
               f"কেবল প্রিমিয়াম অংশ সেখানে যায়: {n:,} x Rs {prem} = Rs {v:,}; {n:,} x Rs {face} যায় শেয়ার-মূলধনে।",
               (n * (face + prem), n * face, v * 2))


def roi(profit, inv):
    r = profit / inv * 100
    return _n(f"A new batching plant cost Rs {inv:,} and earns a profit of Rs {profit:,} a year. What is its return on investment?",
              f"একটা নতুন ব্যাচিং প্ল্যান্টের খরচ Rs {inv:,} আর বছরে মুনাফা Rs {profit:,}। বিনিয়োগের উপর আয় কত?", r,
              f"ROI = profit ÷ investment = {profit:,} ÷ {inv:,} = {_f(_c(r))}%.",
              f"বিনিয়োগের উপর আয় = মুনাফা ÷ বিনিয়োগ = {profit:,} ÷ {inv:,} = {_f(_c(r))}%।",
              (inv / profit, r * 2, r + 5), "%")


# ---------------------------------------------------------------- cost accounting
def pv_ratio(sales, vc):
    r = (sales - vc) / sales * 100
    return _n(f"Sales are Rs {sales:,} and variable costs are Rs {vc:,}. What is the profit-volume (P/V) ratio?",
              f"বিক্রি Rs {sales:,} আর পরিবর্তনশীল খরচ Rs {vc:,}। মুনাফা-আয়তন (পি/ভি) অনুপাত কত?", r,
              f"P/V ratio = contribution ÷ sales = {sales - vc:,} ÷ {sales:,} = {_f(_c(r))}%.",
              f"পি/ভি অনুপাত = অবদান ÷ বিক্রি = {sales - vc:,} ÷ {sales:,} = {_f(_c(r))}%।",
              (vc / sales * 100, (sales - vc) / vc * 100, r / 2), "%")


def bep_sales(fc, pv):
    s = fc / (pv / 100)
    return _rs(f"Fixed costs are Rs {fc:,} and the P/V ratio is {pv}%. What sales value is needed to break even?",
               f"স্থির খরচ Rs {fc:,} আর পি/ভি অনুপাত {pv}%। লাভ-ক্ষতিহীন হতে কত টাকার বিক্রি লাগে?", s,
               f"Break-even sales = fixed cost ÷ P/V ratio = {fc:,} ÷ {pv / 100:g} = Rs {_f(_c(s))}.",
               f"সমচ্ছেদ বিক্রি = স্থির খরচ ÷ পি/ভি অনুপাত = {fc:,} ÷ {pv / 100:g} = Rs {_f(_c(s))}।",
               (fc * pv / 100, fc / (1 - pv / 100), s * 1.2))


def target_sales(fc, profit, pv):
    s = (fc + profit) / (pv / 100)
    return _rs(f"Fixed costs are Rs {fc:,}, the P/V ratio is {pv}% and the firm wants a profit of Rs {profit:,}. What sales are required?",
               f"স্থির খরচ Rs {fc:,}, পি/ভি অনুপাত {pv}% আর সংস্থা Rs {profit:,} মুনাফা চায়। কত বিক্রি লাগবে?", s,
               f"Required sales = (fixed cost + target profit) ÷ P/V = {fc + profit:,} ÷ {pv / 100:g} = Rs {_f(_c(s))}.",
               f"প্রয়োজনীয় বিক্রি = (স্থির খরচ + লক্ষ্য মুনাফা) ÷ পি/ভি = {fc + profit:,} ÷ {pv / 100:g} = Rs {_f(_c(s))}।",
               (fc / (pv / 100), (fc + profit) * pv / 100, s * 1.1))


def mpv(sp, ap, aq):
    v = (sp - ap) * aq
    word_en = "favourable" if v > 0 else "adverse"
    word_bn = "অনুকূল" if v > 0 else "প্রতিকূল"
    return _rs(f"Cement has a standard price of Rs {sp} a bag but was bought at Rs {ap} a bag; {aq:,} bags were bought. What is the size of the material price variance?",
               f"সিমেন্টের প্রমাণ দাম বস্তাপ্রতি Rs {sp}, কিন্তু কেনা হয়েছে বস্তাপ্রতি Rs {ap}-এ; {aq:,} বস্তা কেনা হয়েছে। মাল-দাম ভেদাঙ্কের পরিমাণ কত?", abs(v),
               f"(standard price - actual price) x actual quantity = ({sp} - {ap}) x {aq:,} = Rs {abs(v):,} {word_en}.",
               f"(প্রমাণ দাম - প্রকৃত দাম) x প্রকৃত পরিমাণ = ({sp} - {ap}) x {aq:,} = Rs {abs(v):,} {word_bn}।",
               (abs(v) / 2, abs(v) * 2, sp * aq / 10))


def muv(sq, aq, sp):
    v = (sq - aq) * sp
    return _rs(f"A slab should use {sq} tonnes of steel at a standard Rs {sp:,} a tonne but used {aq} tonnes. What is the size of the material usage variance?",
               f"একটা স্ল্যাবে প্রমাণ দাম টনপ্রতি Rs {sp:,}-এ {sq} টন ইস্পাত লাগার কথা, কিন্তু লেগেছে {aq} টন। মাল-ব্যবহার ভেদাঙ্কের পরিমাণ কত?", abs(v),
               f"(standard quantity - actual quantity) x standard price = ({sq} - {aq}) x {sp:,} = Rs {abs(v):,} {'adverse' if v < 0 else 'favourable'}.",
               f"(প্রমাণ পরিমাণ - প্রকৃত পরিমাণ) x প্রমাণ দাম = ({sq} - {aq}) x {sp:,} = Rs {abs(v):,} {'প্রতিকূল' if v < 0 else 'অনুকূল'}।",
               (aq * sp, sq * sp, abs(v) * 2))


def lrv(sr, ar, hours):
    v = (sr - ar) * hours
    return _rs(f"Masons are paid Rs {ar} an hour against a standard rate of Rs {sr}; they worked {hours:,} hours. What is the size of the labour rate variance?",
               f"রাজমিস্ত্রিদের প্রমাণ হার ঘণ্টায় Rs {sr}, কিন্তু দেওয়া হয়েছে Rs {ar}; তাঁরা {hours:,} ঘণ্টা কাজ করেছেন। শ্রম-হার ভেদাঙ্কের পরিমাণ কত?", abs(v),
               f"(standard rate - actual rate) x actual hours = ({sr} - {ar}) x {hours:,} = Rs {abs(v):,} {'adverse' if v < 0 else 'favourable'}.",
               f"(প্রমাণ হার - প্রকৃত হার) x প্রকৃত ঘণ্টা = ({sr} - {ar}) x {hours:,} = Rs {abs(v):,} {'প্রতিকূল' if v < 0 else 'অনুকূল'}।",
               (ar * hours, sr * hours, abs(v) * 2))


def oar(overhead, hours):
    r = overhead / hours
    return _rs(f"A workshop's budgeted overheads are Rs {overhead:,} for {hours:,} machine hours. What is the overhead absorption rate per machine hour?",
               f"একটা কর্মশালার বাজেটকৃত উপরিখরচ {hours:,} যন্ত্র-ঘণ্টার জন্য Rs {overhead:,}। যন্ত্র-ঘণ্টাপ্রতি উপরিখরচ শোষণ-হার কত?", r,
               f"Rate = budgeted overheads ÷ budgeted hours = {overhead:,} ÷ {hours:,} = Rs {_f(_c(r))} per hour.",
               f"হার = বাজেটকৃত উপরিখরচ ÷ বাজেটকৃত ঘণ্টা = {overhead:,} ÷ {hours:,} = ঘণ্টাপ্রতি Rs {_f(_c(r))}।",
               (hours / overhead * 100, r * 2, r + 5))


def markup_margin(m):
    g = m / (100 + m) * 100
    return _n(f"A dealer adds a {m}% mark-up on cost. What is the profit as a percentage of the selling price (the margin)?",
              f"একজন বিক্রেতা খরচের উপর {m}% লাভ যোগ করেন। বিক্রয়মূল্যের শতাংশ হিসেবে মুনাফা (মার্জিন) কত?", g,
              f"Margin = mark-up ÷ (100 + mark-up) = {m} ÷ {100 + m} = {_f(_c(g))}%.",
              f"মার্জিন = মার্ক-আপ ÷ (100 + মার্ক-আপ) = {m} ÷ {100 + m} = {_f(_c(g))}%।",
              (m, m / 100 * m, 100 - m if m < 100 else g + 5), "%")


def net_price(lp, td, cd):
    v = lp * (1 - td / 100) * (1 - cd / 100)
    return _rs(f"An item listed at Rs {lp:,} gets a {td}% trade discount and then a {cd}% cash discount for prompt payment. What is paid?",
               f"Rs {lp:,} তালিকামূল্যের একটা জিনিসে {td}% বাণিজ্যিক ছাড় আর তারপর দ্রুত প্রদানের জন্য {cd}% নগদ ছাড়। কত দিতে হয়?", v,
               f"{lp:,} x {1 - td / 100:g} x {1 - cd / 100:g} = Rs {_f(_c(v))} - discounts in a chain do not simply add.",
               f"{lp:,} x {1 - td / 100:g} x {1 - cd / 100:g} = Rs {_f(_c(v))} - ধারাবাহিক ছাড় সরলভাবে যোগ হয় না।",
               (lp * (1 - (td + cd) / 100), lp * (1 - td / 100), v * 1.05))


def gst_base(price, rate):
    b = price / (1 + rate / 100)
    return _rs(f"A tool sells for Rs {price:,} including {rate}% GST. What is its price before GST?",
               f"জিএসটি {rate}% সহ একটা যন্ত্রের দাম Rs {price:,}। জিএসটি-র আগে এর দাম কত?", b,
               f"Base = inclusive price ÷ (1 + rate) = {price:,} ÷ {1 + rate / 100:g} = Rs {_f(_c(b))}.",
               f"মূল দাম = জিএসটি-সহ দাম ÷ (1 + হার) = {price:,} ÷ {1 + rate / 100:g} = Rs {_f(_c(b))}।",
               (price * (1 - rate / 100), price, b * 1.1))


# ---------------------------------------------------------------- operations and quality
def pert_te(to, tm, tp):
    te = (to + 4 * tm + tp) / 6
    return _n(f"A bridge-deck activity has optimistic, most likely and pessimistic times of {to}, {tm} and {tp} days. What is its PERT expected time?",
              f"সেতু-পাটাতনের একটা কাজের আশাবাদী, সম্ভাব্যতম আর নৈরাশ্যবাদী সময় {to}, {tm} আর {tp} দিন। এর পার্ট প্রত্যাশিত সময় কত?", te,
              f"tₑ = (a + 4m + b) ÷ 6 = ({to} + {4 * tm} + {tp}) ÷ 6 = {_f(_c(te))} days.",
              f"প্রত্যাশিত সময় = (a + 4m + b) ÷ 6 = ({to} + {4 * tm} + {tp}) ÷ 6 = {_f(_c(te))} দিন।",
              ((to + tm + tp) / 3, tm, tp - to), " days", " দিন")


def pert_sd(to, tp):
    s = (tp - to) / 6
    return _n(f"An activity's optimistic time is {to} days and pessimistic time is {tp} days. What is its PERT standard deviation?",
              f"একটা কাজের আশাবাদী সময় {to} দিন আর নৈরাশ্যবাদী সময় {tp} দিন। এর পার্ট পরিমিত ব্যবধান কত?", s,
              f"σ = (b - a) ÷ 6 = ({tp} - {to}) ÷ 6 = {_f(_c(s))} days.",
              f"পরিমিত ব্যবধান = (b - a) ÷ 6 = ({tp} - {to}) ÷ 6 = {_f(_c(s))} দিন।",
              ((tp - to) / 3, s * s, tp - to), " days", " দিন")


def project_length(paths):
    best = max(sum(p) for _, p in paths)
    txt_en = "; ".join(f"{name}: {' + '.join(map(str, p))} days" for name, p in paths)
    return _n(f"A project network has these paths - {txt_en}. What is the minimum time to finish the project?",
              f"একটা প্রকল্প-জালে এই পথগুলো আছে - {txt_en.replace('days', 'দিন')}। প্রকল্প শেষ করতে ন্যূনতম কত সময় লাগে?", best,
              f"The longest path is critical: {best} days. Any delay on it delays the whole project.",
              f"দীর্ঘতম পথটাই সংকট-পথ: {best} দিন। এর উপর যেকোনো দেরি পুরো প্রকল্প পিছিয়ে দেয়।",
              (min(sum(p) for _, p in paths), sum(sum(p) for _, p in paths), best - 2), " days", " দিন")


def total_float(lf, es, dur):
    f = lf - es - dur
    return _n(f"An activity lasting {dur} days can start at the earliest on day {es} and must finish by day {lf} at the latest. What is its total float?",
              f"{dur} দিনের একটা কাজ সবচেয়ে আগে {es} নম্বর দিনে শুরু হতে পারে আর সবচেয়ে দেরিতে {lf} নম্বর দিনে শেষ হতে হবে। এর মোট ফ্লোট কত?", f,
              f"Total float = LF - ES - duration = {lf} - {es} - {dur} = {f} days.",
              f"মোট ফ্লোট = সর্বশেষ সমাপ্তি - আগাম শুরু - সময়কাল = {lf} - {es} - {dur} = {f} দিন।",
              (lf - es, lf - dur, f + dur), " days", " দিন")


def reorder(max_use, max_lead):
    r = max_use * max_lead
    return _n(f"A site uses at most {max_use} bags of cement a day and delivery takes at most {max_lead} days. What reorder level avoids running out?",
              f"একটা সাইটে দিনে সর্বোচ্চ {max_use} বস্তা সিমেন্ট লাগে আর সরবরাহে সর্বোচ্চ {max_lead} দিন লাগে। কোন পুনঃক্রয়-স্তরে মাল ফুরোবে না?", r,
              f"Reorder level = maximum usage x maximum lead time = {max_use} x {max_lead} = {r} bags.",
              f"পুনঃক্রয়-স্তর = সর্বোচ্চ ব্যবহার x সর্বোচ্চ সরবরাহ-সময় = {max_use} x {max_lead} = {r} বস্তা।",
              (max_use + max_lead, r // 2, r + max_use), " bags", " বস্তা")


def safety_stock(max_use, avg_use, lead):
    s = (max_use - avg_use) * lead
    return _n(f"Daily usage averages {avg_use} units but can reach {max_use}; lead time is {lead} days. What safety stock covers the peak?",
              f"দৈনিক গড় ব্যবহার {avg_use} একক, কিন্তু {max_use} পর্যন্ত হতে পারে; সরবরাহ-সময় {lead} দিন। কত নিরাপত্তা-মজুত শীর্ষ চাহিদা সামলায়?", s,
              f"(maximum - average usage) x lead time = ({max_use} - {avg_use}) x {lead} = {s} units.",
              f"(সর্বোচ্চ - গড় ব্যবহার) x সরবরাহ-সময় = ({max_use} - {avg_use}) x {lead} = {s} একক।",
              (max_use * lead, avg_use * lead, s + lead), " units", " একক")


def control_limits(mean, sd):
    u = mean + 3 * sd
    return _n(f"A cube-strength test has a process mean of {mean} MPa and a standard deviation of {sd} MPa. What is the upper control limit (3-sigma)?",
              f"কিউব-শক্তি পরীক্ষার প্রক্রিয়া-গড় {mean} MPa আর পরিমিত ব্যবধান {sd} MPa। ঊর্ধ্ব নিয়ন্ত্রণ-সীমা (3-সিগমা) কত?", u,
              f"UCL = mean + 3σ = {mean} + 3 x {sd} = {_f(_c(u))} MPa; the LCL is {_f(_c(mean - 3 * sd))} MPa.",
              f"ঊর্ধ্ব সীমা = গড় + 3σ = {mean} + 3 x {sd} = {_f(_c(u))} MPa; নিম্ন সীমা {_f(_c(mean - 3 * sd))} MPa।",
              (mean + sd, mean + 2 * sd, mean * 1.5), " MPa", " মেগাপাস্কাল")


def cp(usl, lsl, sd):
    c = (usl - lsl) / (6 * sd)
    return _n(f"A rebar diameter must lie between {lsl} and {usl} mm; the process standard deviation is {sd} mm. What is the process capability index Cp?",
              f"একটা রডের ব্যাস {lsl} থেকে {usl} mm-এর মধ্যে থাকতে হবে; প্রক্রিয়ার পরিমিত ব্যবধান {sd} mm। প্রক্রিয়া-সক্ষমতা সূচক Cp কত?", c,
              f"Cp = (USL - LSL) ÷ 6σ = {_f(_c(usl - lsl))} ÷ {_f(_c(6 * sd))} = {_f(_c(c))}; above 1.33 is usually considered capable.",
              f"Cp = (ঊর্ধ্ব - নিম্ন সীমা) ÷ 6σ = {_f(_c(usl - lsl))} ÷ {_f(_c(6 * sd))} = {_f(_c(c))}; 1.33-এর বেশি হলে সাধারণত সক্ষম ধরা হয়।",
              ((usl - lsl) / (3 * sd), (usl - lsl) / sd, c + 0.5))


def oee(a, p, q):
    v = a * p * q / 10000
    return _n(f"A crushing plant has {a}% availability, {p}% performance and {q}% quality rate. What is its overall equipment effectiveness (OEE)?",
              f"একটা পাথর-ভাঙা প্ল্যান্টের প্রাপ্যতা {a}%, কর্মক্ষমতা {p}% আর গুণমান-হার {q}%। এর সামগ্রিক যন্ত্র-কার্যকারিতা (ওইই) কত?", v,
              f"OEE = availability x performance x quality = {a / 100:g} x {p / 100:g} x {q / 100:g} = {_f(_c(v))}%.",
              f"ওইই = প্রাপ্যতা x কর্মক্ষমতা x গুণমান = {a / 100:g} x {p / 100:g} x {q / 100:g} = {_f(_c(v))}%।",
              ((a + p + q) / 3, min(a, p, q), v + 10), "%")


def productivity(out, workers, hours):
    p = out / (workers * hours)
    return _n(f"A crew of {workers} workers lays {out:,} paver blocks in a {hours}-hour shift. What is the labour productivity per worker-hour?",
              f"{workers} জন কর্মীর একটা দল {hours} ঘণ্টার শিফটে {out:,}টি পেভার ব্লক বসায়। কর্মী-ঘণ্টাপ্রতি শ্রম-উৎপাদনশীলতা কত?", p,
              f"Output ÷ input = {out:,} ÷ ({workers} x {hours}) = {_f(_c(p))} blocks per worker-hour.",
              f"উৎপাদন ÷ উপকরণ = {out:,} ÷ ({workers} x {hours}) = কর্মী-ঘণ্টাপ্রতি {_f(_c(p))}টি ব্লক।",
              (out / workers, out / hours, p * 2), "")


def elasticity(dq, dp):
    e = dq / dp
    return _n(f"When the price of a road-toll pass rises by {dp}%, the number of passes sold falls by {dq}%. What is the size of the price elasticity of demand?",
              f"রোড-টোল পাসের দাম {dp}% বাড়লে বিক্রি হওয়া পাসের সংখ্যা {dq}% কমে। চাহিদার দাম-স্থিতিস্থাপকতার মান কত?", e,
              f"|%ΔQ ÷ %ΔP| = {dq} ÷ {dp} = {_f(_c(e))}; {'elastic (above 1): raising the price lowers revenue' if e > 1 else 'inelastic (below 1): raising the price raises revenue'}.",
              f"|%ΔQ ÷ %ΔP| = {dq} ÷ {dp} = {_f(_c(e))}; {'স্থিতিস্থাপক (1-এর বেশি): দাম বাড়ালে আয় কমে' if e > 1 else 'অস্থিতিস্থাপক (1-এর কম): দাম বাড়ালে আয় বাড়ে'}।",
              (dp / dq, dq * dp / 100, e + 1))


def attrition(left, start, end):
    r = left / ((start + end) / 2) * 100
    return _n(f"A construction firm started the year with {start} engineers and ended with {end}; {left} left during the year. What is the attrition rate?",
              f"একটা নির্মাণ-সংস্থা বছর শুরু করেছিল {start} জন প্রকৌশলী নিয়ে আর শেষ করেছে {end} জনে; বছরে {left} জন চলে গেছেন। কর্মী-ক্ষয়ের হার কত?", r,
              f"Leavers ÷ average headcount = {left} ÷ {_f(_c((start + end) / 2))} = {_f(_c(r))}%.",
              f"চলে যাওয়া ÷ গড় কর্মীসংখ্যা = {left} ÷ {_f(_c((start + end) / 2))} = {_f(_c(r))}%।",
              (left / start * 100, left / end * 100, r + 5), "%")


NUMERIC = [
    equation(2500000, 900000), equation(780000, 310000), equation(1450000, 625000),
    slm(500000, 50000, 5), slm(1200000, 200000, 10), slm(84000, 4000, 8),
    wdv(1000000, 20, 2), wdv(500000, 15, 3), wdv(800000, 25, 2),
    cogs(50000, 300000, 70000), cogs(120000, 850000, 95000), cogs(30000, 210000, 45000),
    gross_margin(500000, 350000), gross_margin(1200000, 900000), gross_margin(80000, 50000),
    goodwill_avg([40000, 50000, 60000], 2), goodwill_avg([120000, 150000, 90000, 140000], 3),
    super_profit(90000, 500000, 12, 3), super_profit(150000, 1000000, 10, 2),
    capital_interest(200000, 6, 12), capital_interest(150000, 8, 9), capital_interest(400000, 5, 6),
    premium(10000, 10, 5), premium(50000, 10, 15), premium(25000, 100, 20),
    roi(180000, 1200000), roi(60000, 250000),
    pv_ratio(1000000, 600000), pv_ratio(500000, 350000), pv_ratio(800000, 520000),
    bep_sales(300000, 40), bep_sales(450000, 30), bep_sales(120000, 25),
    target_sales(300000, 100000, 40), target_sales(200000, 50000, 25),
    mpv(350, 365, 2000), mpv(400, 380, 1500), mpv(60, 64, 5000),
    muv(20, 22, 60000), muv(50, 48, 55000),
    lrv(120, 130, 800), lrv(90, 85, 1200),
    oar(600000, 12000), oar(280000, 3500), oar(900000, 15000),
    markup_margin(25), markup_margin(50), markup_margin(100), markup_margin(20),
    net_price(10000, 20, 5), net_price(50000, 10, 2), net_price(2400, 25, 4),
    gst_base(1180, 18), gst_base(11200, 12), gst_base(2800, 28),
    pert_te(4, 6, 14), pert_te(10, 12, 20), pert_te(3, 5, 13),
    pert_sd(4, 16), pert_sd(6, 24), pert_sd(12, 27),
    project_length([("A-B-D", (4, 6, 5)), ("A-C-D", (4, 9, 5)), ("A-E", (4, 12))]),
    project_length([("piling-pier-deck", (20, 15, 30)), ("piling-abutment-deck", (20, 25, 30)), ("approach road", (40, 35))]),
    total_float(30, 10, 12), total_float(45, 20, 18), total_float(60, 25, 30),
    reorder(40, 6), reorder(25, 8), reorder(120, 3),
    safety_stock(50, 35, 6), safety_stock(80, 60, 5), safety_stock(30, 20, 9),
    control_limits(30, 2), control_limits(40, 2.5), control_limits(25, 1.8),
    cp(12.2, 11.8, 0.05), cp(25.5, 24.5, 0.1), cp(10.6, 9.4, 0.15),
    oee(90, 95, 99), oee(85, 90, 98), oee(80, 85, 95),
    productivity(1800, 6, 8), productivity(2400, 8, 10), productivity(960, 4, 8),
    elasticity(30, 10), elasticity(5, 10), elasticity(24, 12),
    attrition(12, 80, 88), attrition(30, 140, 160),
    equation(960000, 410000), slm(250000, 10000, 6), wdv(1500000, 10, 3), cogs(80000, 640000, 60000),
    gross_margin(250000, 190000), goodwill_avg([60000, 75000, 90000], 3), super_profit(200000, 1500000, 8, 4),
    capital_interest(300000, 7, 8), premium(20000, 10, 8), roi(90000, 450000), pv_ratio(600000, 420000),
    bep_sales(240000, 20), target_sales(150000, 60000, 30), mpv(120, 115, 3000), muv(30, 33, 45000),
    lrv(100, 110, 1500), oar(360000, 8000), markup_margin(40), net_price(8000, 15, 3), gst_base(5900, 18),
    pert_te(6, 9, 18), pert_sd(10, 22), total_float(50, 15, 25), reorder(60, 5), safety_stock(45, 30, 4),
    control_limits(35, 3), cp(50.6, 49.4, 0.2), oee(95, 92, 97), productivity(3600, 12, 6), elasticity(8, 16),
    attrition(18, 60, 72), markup_margin(60),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    _q("The going-concern concept assumes that a business…", ["Will continue operating for the foreseeable future", "Will close at the end of the year", "Has no liabilities", "Records assets at sale value"],
       "That is why fixed assets are shown at cost less depreciation rather than at forced-sale value.",
       "চলমান প্রতিষ্ঠান ধারণা ধরে নেয় যে একটা ব্যবসা…", ["অদূর ভবিষ্যতে চালু থাকবে", "বছরের শেষে বন্ধ হবে", "কোনো দায় নেই", "সম্পদ বিক্রয়মূল্যে লেখে"],
       "সেই জন্যই স্থায়ী সম্পদ বাধ্যতামূলক বিক্রয়মূল্যে নয়, খরচ বিয়োগ অবচয়ে দেখানো হয়।"),
    _q("Which principle says expenses should be recorded in the same period as the revenue they help earn?", ["The matching principle", "The going-concern concept", "The money-measurement concept", "The entity concept"],
       "So wages for March's work belong to March's profit even if they are paid in April.",
       "কোন নীতি বলে যে খরচ সেই সময়কালেই লেখা উচিত যে সময়ের আয়ে তা সাহায্য করে?", ["মিলকরণ নীতি", "চলমান প্রতিষ্ঠান ধারণা", "অর্থ-পরিমাপ ধারণা", "সত্তা ধারণা"],
       "তাই মার্চের কাজের মজুরি এপ্রিলে দিলেও মার্চের মুনাফায় ধরা হয়।"),
    _q("The prudence (conservatism) concept means…", ["Anticipate no profits but provide for all likely losses", "Record all expected profits now", "Ignore possible losses", "Value stock at selling price"],
       "Stock is valued at the lower of cost and net realisable value for this reason.",
       "বিচক্ষণতা (রক্ষণশীলতা) ধারণা মানে…", ["কোনো মুনাফা আগাম ধরো না, কিন্তু সম্ভাব্য সব ক্ষতির সংস্থান রাখো", "সব প্রত্যাশিত মুনাফা এখনই লেখো", "সম্ভাব্য ক্ষতি উপেক্ষা করো", "মজুত বিক্রয়মূল্যে ধরো"],
       "এই কারণেই মজুত খরচ আর নিট আদায়যোগ্য মূল্যের মধ্যে যেটা কম, তাতে ধরা হয়।"),
    _q("Under the dual-aspect concept, every transaction…", ["Has two equal effects, so the accounting equation always balances", "Affects only one account", "Is recorded twice in the same account", "Must involve cash"],
       "This is the basis of double-entry book-keeping: total debits always equal total credits.",
       "দ্বৈত সত্তা ধারণা অনুযায়ী প্রতিটি লেনদেন…", ["দুটো সমান প্রভাব ফেলে, তাই হিসাব-সমীকরণ সবসময় মেলে", "কেবল একটা খাতকে প্রভাবিত করে", "একই খাতে দুবার লেখা হয়", "নগদ জড়িত থাকতেই হবে"],
       "এটাই দু-তরফা দাখিলার ভিত্তি: মোট ডেবিট সবসময় মোট ক্রেডিটের সমান।"),
    _q("Buying a new crane for a construction company is…", ["Capital expenditure", "Revenue expenditure", "Deferred revenue expenditure", "A liability"],
       "It brings benefit over many years, so it is shown as an asset and depreciated; its fuel is revenue expenditure.",
       "একটা নির্মাণ-কোম্পানির নতুন ক্রেন কেনা হলো…", ["মূলধনী ব্যয়", "মুনাফাজাতীয় ব্যয়", "বিলম্বিত মুনাফাজাতীয় ব্যয়", "একটা দায়"],
       "এটা বহু বছর সুফল দেয়, তাই সম্পদ হিসেবে দেখিয়ে অবচয় করা হয়; এর জ্বালানি মুনাফাজাতীয় ব্যয়।"),
    _q("Which error will NOT be revealed by a trial balance?", ["An error of complete omission", "Posting a debit to the credit side", "A wrong total in a ledger account", "Posting only one side of an entry"],
       "If a transaction is left out entirely, debits and credits still match; errors of principle and compensating errors also hide.",
       "কোন ভুল রেওয়ামিলে ধরা পড়বে না?", ["সম্পূর্ণ বাদ পড়ার ভুল", "ডেবিটকে ক্রেডিট দিকে খতিয়ানে তোলা", "খতিয়ানে ভুল যোগফল", "দাখিলার কেবল এক দিক খতিয়ানে তোলা"],
       "পুরো লেনদেন বাদ পড়লে ডেবিট আর ক্রেডিট তবু মেলে; নীতিগত ভুল আর পরিপূরক ভুলও লুকিয়ে থাকে।"),
    _q("Why does a bank reconciliation statement need to be prepared?", ["The cash book and bank passbook balances differ because of timing and errors", "To calculate income tax", "To value fixed assets", "To pay salaries"],
       "Cheques issued but not yet presented, or bank charges not yet recorded, are common reasons.",
       "ব্যাংক সমন্বয় বিবরণী তৈরি করতে হয় কেন?", ["সময়ের ব্যবধান আর ভুলের জন্য নগদান বই আর ব্যাংক পাসবইয়ের জের আলাদা হয়", "আয়কর হিসাব করতে", "স্থায়ী সম্পদের মূল্য নির্ধারণে", "বেতন দিতে"],
       "ইস্যু করা কিন্তু এখনো উপস্থাপিত না হওয়া চেক, বা এখনো না লেখা ব্যাংক-চার্জ সাধারণ কারণ।"),
    _q("How does a provision differ from a reserve?", ["A provision covers a known liability or loss; a reserve is profit set aside", "They are exactly the same", "A reserve is a charge against profit", "A provision increases capital"],
       "Provision for doubtful debts is charged against profit; a general reserve is an appropriation of profit.",
       "সংস্থান আর সঞ্চিতির পার্থক্য কী?", ["সংস্থান একটা জানা দায় বা ক্ষতি ঢাকে; সঞ্চিতি হলো আলাদা রাখা মুনাফা", "দুটো হুবহু এক", "সঞ্চিতি মুনাফার উপর চার্জ", "সংস্থান মূলধন বাড়ায়"],
       "অনাদায়ী পাওনার সংস্থান মুনাফার উপর চার্জ; সাধারণ সঞ্চিতি মুনাফার বণ্টন।"),
    _q("If a partnership deed is silent, how are profits shared under the Indian Partnership Act?", ["Equally among the partners", "In the ratio of capital", "By age", "Only to the managing partner"],
       "Without a deed there is also no interest on capital and no salary for partners; loans from partners earn 6% a year.",
       "অংশীদারি চুক্তিপত্রে কিছু না বলা থাকলে ভারতীয় অংশীদারি আইনে মুনাফা কীভাবে ভাগ হয়?", ["অংশীদারদের মধ্যে সমানভাবে", "মূলধনের অনুপাতে", "বয়স অনুযায়ী", "কেবল পরিচালক অংশীদারকে"],
       "চুক্তি না থাকলে মূলধনে সুদ বা অংশীদারের বেতনও নেই; অংশীদারের ঋণে বছরে 6% সুদ।"),
    _q("When a new partner joins and brings goodwill in cash, the old partners share it in…", ["Their sacrificing ratio", "The new profit ratio", "Their capital ratio", "Equal shares always"],
       "Sacrificing ratio = old share - new share for each old partner.",
       "নতুন অংশীদার যোগ দিয়ে নগদে সুনাম আনলে পুরোনো অংশীদাররা তা ভাগ করেন…", ["তাঁদের ত্যাগের অনুপাতে", "নতুন মুনাফা-অনুপাতে", "তাঁদের মূলধন-অনুপাতে", "সবসময় সমানভাগে"],
       "ত্যাগের অনুপাত = প্রত্যেক পুরোনো অংশীদারের পুরোনো ভাগ - নতুন ভাগ।"),
    _q("Preference shareholders differ from equity shareholders because they…", ["Get a fixed dividend first and are repaid before equity on winding up", "Always control the company by voting", "Never receive dividends", "Own the company's debt"],
       "Equity holders bear the most risk but keep all remaining profits and normally hold the votes.",
       "অগ্রাধিকার শেয়ারহোল্ডাররা ইক্যুইটি শেয়ারহোল্ডারদের থেকে আলাদা কারণ তাঁরা…", ["আগে নির্দিষ্ট লভ্যাংশ পান আর অবসায়নে ইক্যুইটির আগে টাকা ফেরত পান", "সবসময় ভোট দিয়ে কোম্পানি নিয়ন্ত্রণ করেন", "কখনো লভ্যাংশ পান না", "কোম্পানির ঋণের মালিক"],
       "ইক্যুইটি হোল্ডাররা সবচেয়ে বেশি ঝুঁকি নেন কিন্তু বাকি সব মুনাফা পান আর সাধারণত ভোটাধিকার রাখেন।"),
    _q("Debenture holders of a company are its…", ["Creditors, entitled to interest whether or not there is profit", "Owners, entitled to dividends", "Employees", "Auditors"],
       "Debenture interest is a charge against profit; dividends are paid out of profit.",
       "একটা কোম্পানির ডিবেঞ্চার-হোল্ডাররা তার…", ["পাওনাদার, মুনাফা হোক বা না হোক সুদ পাওয়ার অধিকারী", "মালিক, লভ্যাংশ পাওয়ার অধিকারী", "কর্মচারী", "নিরীক্ষক"],
       "ডিবেঞ্চারের সুদ মুনাফার উপর চার্জ; লভ্যাংশ দেওয়া হয় মুনাফা থেকে।"),
    _q("In a cash flow statement, buying a new machine is shown under…", ["Investing activities", "Operating activities", "Financing activities", "It is not shown"],
       "Operating covers day-to-day trading; financing covers loans, share issues and dividends.",
       "নগদ প্রবাহ বিবরণীতে নতুন যন্ত্র কেনা কোন অংশে দেখানো হয়?", ["বিনিয়োগ কার্যক্রম", "পরিচালন কার্যক্রম", "অর্থায়ন কার্যক্রম", "দেখানো হয় না"],
       "পরিচালনে দৈনন্দিন ব্যবসা; অর্থায়নে ঋণ, শেয়ার ইস্যু আর লভ্যাংশ।"),
    _q("Which cost stays the same in total when output rises (within a range)?", ["Fixed cost, such as site office rent", "Variable cost, such as cement per cubic metre", "Direct material cost", "Piece-rate wages"],
       "Fixed cost per unit falls as output rises; variable cost per unit stays constant.",
       "উৎপাদন বাড়লেও (একটা সীমার মধ্যে) মোট কোন খরচ একই থাকে?", ["স্থির খরচ, যেমন সাইট অফিসের ভাড়া", "পরিবর্তনশীল খরচ, যেমন ঘনমিটারপ্রতি সিমেন্ট", "প্রত্যক্ষ মালের খরচ", "ঠিকা-হারের মজুরি"],
       "উৎপাদন বাড়লে এককপ্রতি স্থির খরচ কমে; এককপ্রতি পরিবর্তনশীল খরচ একই থাকে।"),
    _q("In marginal costing, which costs are charged to products?", ["Only variable costs; fixed costs are written off in the period", "Only fixed costs", "All costs including selling expenses", "None"],
       "This makes short-term decisions such as accepting a special order clearer.",
       "প্রান্তিক ব্যয়করণে পণ্যের উপর কোন খরচ চাপানো হয়?", ["কেবল পরিবর্তনশীল খরচ; স্থির খরচ সেই সময়কালেই বাদ যায়", "কেবল স্থির খরচ", "বিক্রয়-ব্যয়সহ সব খরচ", "কোনোটাই নয়"],
       "এতে বিশেষ অর্ডার নেওয়ার মতো স্বল্পমেয়াদি সিদ্ধান্ত স্পষ্ট হয়।"),
    _q("A firm with spare capacity gets a special order below its normal price. It should usually accept if…", ["The price is above the variable cost per unit", "The price covers full cost including fixed overheads", "The price is below variable cost", "Never"],
       "Fixed costs are paid anyway, so any contribution adds to profit - provided normal sales are not harmed.",
       "অব্যবহৃত ক্ষমতার একটা সংস্থা স্বাভাবিকের চেয়ে কম দামে একটা বিশেষ অর্ডার পায়। সাধারণত তা নেওয়া উচিত যদি…", ["দাম এককপ্রতি পরিবর্তনশীল খরচের বেশি হয়", "দাম স্থির উপরিখরচসহ পুরো খরচ ঢাকে", "দাম পরিবর্তনশীল খরচের কম হয়", "কখনো নয়"],
       "স্থির খরচ এমনিতেই দিতে হয়, তাই যেকোনো অবদান মুনাফা বাড়ায় - যদি স্বাভাবিক বিক্রি ক্ষতিগ্রস্ত না হয়।"),
    _q("What is standard costing mainly used for?", ["Comparing actual costs with predetermined standards to find variances", "Paying taxes", "Valuing shares", "Recording sales"],
       "Analysing price and usage variances shows managers where to act.",
       "প্রমাণ ব্যয়করণ প্রধানত কী কাজে লাগে?", ["প্রকৃত খরচকে পূর্বনির্ধারিত মানের সঙ্গে তুলনা করে ভেদাঙ্ক খুঁজতে", "কর দিতে", "শেয়ারের মূল্য নির্ধারণে", "বিক্রি লিখতে"],
       "দাম আর ব্যবহার ভেদাঙ্ক বিশ্লেষণ ম্যানেজারদের দেখায় কোথায় ব্যবস্থা নিতে হবে।"),
    _q("In ABC inventory analysis, 'A' items are…", ["A few items that make up most of the total value", "Many cheap items", "Items that are never used", "Items sorted alphabetically"],
       "A items (about 10-20% of items, 70-80% of value) get the tightest control; C items the least.",
       "এবিসি মজুত-বিশ্লেষণে 'এ' আইটেম হলো…", ["অল্প কয়েকটা আইটেম যা মোট মূল্যের বেশিরভাগ", "অনেক সস্তা আইটেম", "কখনো ব্যবহার না হওয়া আইটেম", "বর্ণানুক্রমে সাজানো আইটেম"],
       "এ আইটেম (প্রায় 10-20% আইটেম, 70-80% মূল্য) সবচেয়ে কড়া নিয়ন্ত্রণ পায়; সি আইটেম সবচেয়ে কম।"),
    _q("The just-in-time (JIT) approach aims to…", ["Receive materials exactly when needed, keeping inventory minimal", "Store large stocks for emergencies", "Produce as much as possible regardless of demand", "Delay all deliveries"],
       "It cuts storage cost and waste but needs very reliable suppliers.",
       "জাস্ট-ইন-টাইম (জেআইটি) পদ্ধতির লক্ষ্য…", ["ঠিক প্রয়োজনের সময় মাল আনা, মজুত ন্যূনতম রাখা", "জরুরি অবস্থার জন্য বড় মজুত রাখা", "চাহিদা না দেখে যত পারা যায় উৎপাদন", "সব সরবরাহ পিছিয়ে দেওয়া"],
       "এতে মজুত-খরচ আর অপচয় কমে কিন্তু খুব নির্ভরযোগ্য সরবরাহকারী লাগে।"),
    _q("Kaizen means…", ["Continuous small improvements by everyone", "A one-time large investment", "Laying off workers", "Outsourcing all production"],
       "The Japanese idea builds quality and productivity step by step from the shop floor up.",
       "কাইজেন মানে…", ["সবার দ্বারা নিরন্তর ছোট ছোট উন্নতি", "একবারের বড় বিনিয়োগ", "কর্মী ছাঁটাই", "সব উৎপাদন বাইরে করানো"],
       "জাপানি এই ধারণা কারখানার মেঝে থেকে ধাপে ধাপে গুণমান আর উৎপাদনশীলতা গড়ে।"),
    _q("A Six Sigma process aims for about how many defects per million opportunities?", ["3.4", "340", "34,000", "0 exactly"],
       "It allows for a 1.5σ drift of the mean; the method uses the DMAIC cycle.",
       "সিক্স সিগমা প্রক্রিয়ার লক্ষ্য প্রতি দশ লক্ষ সুযোগে প্রায় কয়টি ত্রুটি?", ["3.4", "340", "34,000", "ঠিক 0"],
       "এতে গড়ের 1.5σ সরণ ধরা হয়; পদ্ধতিটা ডিএমএআইসি চক্র ব্যবহার করে।"),
    _q("A point outside the 3-sigma limits of a control chart usually signals…", ["An assignable (special) cause that should be investigated", "Normal random variation", "That the limits are wrong", "Perfect quality"],
       "Random variation alone puts only about 3 points in 1,000 outside the limits.",
       "নিয়ন্ত্রণ-চার্টের 3-সিগমা সীমার বাইরে একটা বিন্দু সাধারণত কী নির্দেশ করে?", ["নির্দিষ্টযোগ্য (বিশেষ) কারণ, যা তদন্ত করা উচিত", "স্বাভাবিক এলোমেলো তারতম্য", "সীমাগুলো ভুল", "নিখুঁত গুণমান"],
       "কেবল এলোমেলো তারতম্যে 1,000-এ প্রায় 3টি বিন্দু সীমার বাইরে যায়।"),
    _q("The critical path in a project network is…", ["The longest path, with zero total float", "The shortest path", "The cheapest path", "Any path with a milestone"],
       "Shortening the project means shortening (crashing) activities on this path.",
       "প্রকল্প-জালের সংকট-পথ হলো…", ["দীর্ঘতম পথ, যার মোট ফ্লোট শূন্য", "সবচেয়ে ছোট পথ", "সবচেয়ে সস্তা পথ", "মাইলফলকসহ যেকোনো পথ"],
       "প্রকল্প ছোট করতে হলে এই পথের কাজগুলো ছোট (ক্র্যাশ) করতে হয়।"),
    _q("'Crashing' an activity in project scheduling means…", ["Shortening its duration by adding resources, at extra cost", "Cancelling it", "Delaying it", "Doing it after the project ends"],
       "Crash the critical activity with the lowest cost per day saved first.",
       "প্রকল্প-সূচিতে একটা কাজ 'ক্র্যাশ' করা মানে…", ["বাড়তি খরচে সম্পদ যোগ করে তার সময়কাল কমানো", "বাতিল করা", "পিছিয়ে দেওয়া", "প্রকল্প শেষের পরে করা"],
       "দিনপ্রতি বাঁচানো খরচ সবচেয়ে কম এমন সংকট-কাজ আগে ক্র্যাশ করো।"),
    _q("How does PERT differ from CPM?", ["PERT uses three time estimates for uncertain activities; CPM uses one fixed time", "PERT ignores time", "CPM is only for research projects", "They are identical"],
       "PERT suits new, uncertain work such as research; CPM suits repetitive construction where times are well known.",
       "পার্ট সিপিএম থেকে কীভাবে আলাদা?", ["অনিশ্চিত কাজের জন্য পার্ট তিনটি সময়-অনুমান নেয়; সিপিএম একটা নির্দিষ্ট সময়", "পার্ট সময় উপেক্ষা করে", "সিপিএম কেবল গবেষণা প্রকল্পের জন্য", "দুটো হুবহু এক"],
       "নতুন, অনিশ্চিত কাজে (যেমন গবেষণা) পার্ট মানানসই; সময় জানা পুনরাবৃত্ত নির্মাণে সিপিএম।"),
    _q("A Gantt chart shows…", ["Activities as bars against a time scale", "Profit against sales", "An organisation's hierarchy", "Cash flows"],
       "It is easy to read but does not show dependencies as clearly as a network diagram.",
       "গ্যান্ট চার্ট কী দেখায়?", ["সময়-স্কেলের বিপরীতে কাজগুলোকে দণ্ড হিসেবে", "বিক্রির বিপরীতে মুনাফা", "প্রতিষ্ঠানের ক্রমবিন্যাস", "নগদ প্রবাহ"],
       "এটা পড়া সহজ, কিন্তু নির্ভরতা জাল-চিত্রের মতো স্পষ্ট দেখায় না।"),
    _q("Fayol's principle of 'unity of command' says that…", ["Each employee should receive orders from only one superior", "All managers share every decision", "Workers should choose their bosses", "Orders should come from many managers"],
       "Two bosses giving conflicting orders cause confusion on site.",
       "ফেয়লের 'আদেশের ঐক্য' নীতি বলে যে…", ["প্রত্যেক কর্মী কেবল একজন ঊর্ধ্বতনের কাছ থেকে আদেশ পাবেন", "সব ম্যানেজার প্রতিটি সিদ্ধান্ত ভাগ করবেন", "কর্মীরা নিজেদের বস বাছবেন", "অনেক ম্যানেজার থেকে আদেশ আসবে"],
       "দুজন বস পরস্পরবিরোধী আদেশ দিলে সাইটে বিভ্রান্তি হয়।"),
    _q("F. W. Taylor is known as the father of…", ["Scientific management", "Human relations theory", "Marketing", "Double-entry book-keeping"],
       "He used time and motion studies to find the 'one best way' of doing each task.",
       "এফ. ডব্লিউ. টেলর কীসের জনক হিসেবে পরিচিত?", ["বৈজ্ঞানিক ব্যবস্থাপনা", "মানবিক সম্পর্ক তত্ত্ব", "বিপণন", "দু-তরফা দাখিলা"],
       "প্রতিটি কাজের 'একমাত্র সেরা উপায়' খুঁজতে তিনি সময় ও গতি অধ্যয়ন ব্যবহার করেছিলেন।"),
    _q("Which management function compares actual performance with plans and corrects deviations?", ["Controlling", "Planning", "Organising", "Staffing"],
       "Planning sets the targets; controlling checks progress against them and closes the loop.",
       "ব্যবস্থাপনার কোন কাজ প্রকৃত কর্মক্ষমতাকে পরিকল্পনার সঙ্গে তুলনা করে বিচ্যুতি সংশোধন করে?", ["নিয়ন্ত্রণ", "পরিকল্পনা", "সংগঠন", "কর্মী-নিয়োগ"],
       "পরিকল্পনা লক্ষ্য ঠিক করে; নিয়ন্ত্রণ সেই অনুযায়ী অগ্রগতি যাচাই করে চক্র পূর্ণ করে।"),
    _q("In Maslow's hierarchy of needs, which level comes right after physiological needs?", ["Safety and security", "Esteem", "Self-actualisation", "Social belonging"],
       "Order: physiological → safety → social → esteem → self-actualisation.",
       "মাসলোর চাহিদা-স্তরক্রমে শারীরিক চাহিদার ঠিক পরে কোন স্তর?", ["নিরাপত্তা আর সুরক্ষা", "সম্মান", "আত্মোপলব্ধি", "সামাজিক মেলামেশা"],
       "ক্রম: শারীরিক → নিরাপত্তা → সামাজিক → সম্মান → আত্মোপলব্ধি।"),
    _q("McGregor's Theory Y assumes that workers…", ["Like responsibility and can direct themselves", "Dislike work and must be closely supervised", "Want only money", "Cannot be trusted"],
       "Theory X managers rely on control; Theory Y managers rely on participation and trust.",
       "ম্যাকগ্রেগরের থিওরি ওয়াই ধরে নেয় যে কর্মীরা…", ["দায়িত্ব পছন্দ করেন আর নিজেদের চালাতে পারেন", "কাজ অপছন্দ করেন আর কড়া তত্ত্বাবধান লাগে", "কেবল টাকা চান", "বিশ্বাসযোগ্য নন"],
       "থিওরি এক্স ম্যানেজাররা নিয়ন্ত্রণে ভরসা করেন; থিওরি ওয়াই ম্যানেজাররা অংশগ্রহণ আর আস্থায়।"),
    _q("The four Ps of the marketing mix are…", ["Product, price, place and promotion", "People, profit, planning and power", "Purchase, payment, packing and post", "Price, profit, plant and production"],
       "Services add people, process and physical evidence to make seven Ps.",
       "বিপণন-মিশ্রণের চারটি 'পি' হলো…", ["পণ্য, দাম, স্থান আর প্রচার", "মানুষ, মুনাফা, পরিকল্পনা আর ক্ষমতা", "ক্রয়, প্রদান, মোড়ক আর ডাক", "দাম, মুনাফা, কারখানা আর উৎপাদন"],
       "সেবার ক্ষেত্রে মানুষ, প্রক্রিয়া আর বাস্তব প্রমাণ যোগ হয়ে সাতটি পি।"),
    _q("In which stage of the product life cycle are sales highest and competition fiercest?", ["Maturity", "Introduction", "Growth", "Decline"],
       "Firms then compete on price and features and look for new uses or markets.",
       "পণ্যের জীবনচক্রের কোন পর্যায়ে বিক্রি সবচেয়ে বেশি আর প্রতিযোগিতা সবচেয়ে তীব্র?", ["পরিণতি", "প্রবর্তন", "বৃদ্ধি", "পতন"],
       "তখন সংস্থাগুলো দাম আর বৈশিষ্ট্যে প্রতিযোগিতা করে আর নতুন ব্যবহার বা বাজার খোঁজে।"),
    _q("Under GST, input tax credit allows a business to…", ["Deduct the GST it paid on purchases from the GST it collects on sales", "Avoid all tax", "Charge double tax", "Pay tax only once a decade"],
       "Tax is then paid only on the value added at each stage, removing the 'tax on tax' cascade.",
       "জিএসটি-তে ইনপুট ট্যাক্স ক্রেডিট একটা ব্যবসাকে কী করতে দেয়?", ["ক্রয়ে দেওয়া জিএসটি বিক্রিতে আদায় করা জিএসটি থেকে বাদ দিতে", "সব কর এড়াতে", "দ্বিগুণ কর নিতে", "দশকে একবার কর দিতে"],
       "তখন প্রতিটি ধাপে কেবল সংযোজিত মূল্যের উপর কর দিতে হয়, 'করের উপর কর' দূর হয়।"),
    _q("Which GST applies when goods move from one Indian state to another?", ["IGST", "CGST and SGST", "No GST", "Customs duty"],
       "For sales within one state, CGST and SGST are charged in equal halves.",
       "এক ভারতীয় রাজ্য থেকে আরেক রাজ্যে মাল গেলে কোন জিএসটি প্রযোজ্য?", ["আইজিএসটি", "সিজিএসটি আর এসজিএসটি", "কোনো জিএসটি নয়", "আমদানি শুল্ক"],
       "একই রাজ্যের মধ্যে বিক্রিতে সিজিএসটি আর এসজিএসটি সমান অর্ধেক করে নেওয়া হয়।"),
    _q("For a contract to be valid under the Indian Contract Act, which is essential?", ["Free consent of competent parties and lawful consideration", "It must be written on stamp paper always", "Only one party must agree", "It must involve a government department"],
       "An agreement without consideration is generally void, with a few exceptions such as gifts made in writing out of natural love.",
       "ভারতীয় চুক্তি আইনে একটা চুক্তি বৈধ হতে কোনটা অপরিহার্য?", ["যোগ্য পক্ষগুলোর স্বাধীন সম্মতি আর বৈধ প্রতিদান", "সবসময় স্ট্যাম্প পেপারে লিখতে হবে", "কেবল এক পক্ষের সম্মতি", "সরকারি বিভাগ জড়িত থাকতে হবে"],
       "প্রতিদান ছাড়া চুক্তি সাধারণত বাতিল, কয়েকটা ব্যতিক্রম ছাড়া, যেমন স্বাভাবিক ভালোবাসায় লিখিত দান।"),
    _q("A contract signed because one party was threatened is…", ["Voidable at the option of the threatened party", "Valid and binding on both", "Automatically void from the start", "Illegal for both parties"],
       "Coercion, undue influence and fraud make a contract voidable; the affected party may choose to cancel it.",
       "এক পক্ষকে হুমকি দিয়ে সই করানো চুক্তি…", ["হুমকিপ্রাপ্ত পক্ষের ইচ্ছায় বাতিলযোগ্য", "বৈধ আর দুই পক্ষের জন্য বাধ্যতামূলক", "শুরু থেকেই স্বয়ংক্রিয়ভাবে বাতিল", "দুই পক্ষের জন্যই বেআইনি"],
       "বলপ্রয়োগ, অনুচিত প্রভাব আর প্রতারণা চুক্তিকে বাতিলযোগ্য করে; ক্ষতিগ্রস্ত পক্ষ তা বাতিল করতে পারেন।"),
    _q("What is a 'crossed' cheque?", ["One that can only be paid into a bank account, not cashed over the counter", "One with no amount written", "One that has expired", "One signed by two people"],
       "Two parallel lines across the cheque protect against theft, since the money must go to an account.",
       "'রেখাঙ্কিত' চেক কী?", ["যা কেবল ব্যাংক অ্যাকাউন্টে জমা হয়, কাউন্টারে নগদ দেওয়া হয় না", "যাতে কোনো অঙ্ক লেখা নেই", "যার মেয়াদ শেষ", "যা দুজন সই করেছেন"],
       "চেকের উপর দুটো সমান্তরাল রেখা চুরি থেকে রক্ষা করে, কারণ টাকা অ্যাকাউন্টেই যেতে হবে।"),
    _q("How does a private limited company differ from a public limited company in India?", ["It cannot invite the public to buy its shares", "It has unlimited liability", "It needs no directors", "It cannot own property"],
       "A private company can have at most 200 members; a One Person Company has a single member.",
       "ভারতে প্রাইভেট লিমিটেড কোম্পানি পাবলিক লিমিটেড থেকে কীভাবে আলাদা?", ["এটা জনসাধারণকে শেয়ার কিনতে আহ্বান করতে পারে না", "এর দায় অসীম", "এর পরিচালক লাগে না", "এটা সম্পত্তির মালিক হতে পারে না"],
       "প্রাইভেট কোম্পানিতে সর্বোচ্চ 200 জন সদস্য; ওয়ান পার্সন কোম্পানিতে একজন সদস্য।"),
    _q("What is the main advantage of a limited liability partnership (LLP) over an ordinary partnership?", ["Partners' personal assets are protected beyond their agreed contribution", "It pays no tax", "It needs no registration", "Partners cannot leave"],
       "An LLP is a separate legal entity; one partner is not liable for another's misconduct.",
       "সাধারণ অংশীদারির তুলনায় সীমিত দায় অংশীদারির (এলএলপি) প্রধান সুবিধা কী?", ["চুক্তিবদ্ধ অবদানের বাইরে অংশীদারদের ব্যক্তিগত সম্পদ সুরক্ষিত", "এটা কোনো কর দেয় না", "নিবন্ধন লাগে না", "অংশীদাররা ছাড়তে পারেন না"],
       "এলএলপি একটা পৃথক আইনি সত্তা; এক অংশীদার আরেকজনের অসদাচরণের জন্য দায়ী নন।"),
    _q("A PESTLE analysis of the business environment examines…", ["Political, economic, social, technological, legal and environmental factors", "Only competitors' prices", "Employee salaries", "The cash book"],
       "For a bridge contractor, new safety laws (legal) and steel prices (economic) are typical items.",
       "ব্যবসায়িক পরিবেশের পিইএসটিএলই বিশ্লেষণ কী পরীক্ষা করে?", ["রাজনৈতিক, অর্থনৈতিক, সামাজিক, প্রযুক্তিগত, আইনি আর পরিবেশগত বিষয়", "কেবল প্রতিযোগীর দাম", "কর্মীদের বেতন", "নগদান বই"],
       "একজন সেতু-ঠিকাদারের ক্ষেত্রে নতুন নিরাপত্তা আইন (আইনি) আর ইস্পাতের দাম (অর্থনৈতিক) সাধারণ উদাহরণ।"),
    _q("In a SWOT analysis, 'opportunities' and 'threats' refer to…", ["External factors outside the firm", "Internal strengths and weaknesses", "The firm's balance sheet", "Employee skills only"],
       "Strengths and weaknesses are internal; opportunities and threats come from the environment.",
       "সোয়াট বিশ্লেষণে 'সুযোগ' আর 'হুমকি' বলতে বোঝায়…", ["সংস্থার বাইরের বিষয়", "ভেতরের শক্তি আর দুর্বলতা", "সংস্থার স্থিতিপত্র", "কেবল কর্মীদের দক্ষতা"],
       "শক্তি আর দুর্বলতা ভেতরের; সুযোগ আর হুমকি আসে পরিবেশ থেকে।"),
    _q("Under the Consumer Protection Act, 2019, a consumer can complain about…", ["Defective goods, deficient services and unfair trade practices", "Only government services", "Only goods bought abroad", "Nothing after purchase"],
       "Complaints go to district, state or national commissions depending on the value involved; e-commerce is also covered.",
       "ভোক্তা সুরক্ষা আইন, 2019 অনুযায়ী একজন ভোক্তা কী নিয়ে অভিযোগ করতে পারেন?", ["ত্রুটিপূর্ণ পণ্য, ঘাটতিপূর্ণ সেবা আর অন্যায্য বাণিজ্য-রীতি", "কেবল সরকারি সেবা", "কেবল বিদেশে কেনা পণ্য", "কেনার পরে কিছুই না"],
       "জড়িত মূল্য অনুযায়ী অভিযোগ যায় জেলা, রাজ্য বা জাতীয় কমিশনে; ই-কমার্সও এর আওতায়।"),
    _q("Which communication barrier is caused by using technical jargon with site workers?", ["A semantic (language) barrier", "A physical barrier", "An organisational barrier", "A personal barrier"],
       "The message is sent but not understood; plain words and demonstrations help.",
       "সাইট-কর্মীদের সঙ্গে কারিগরি পরিভাষা ব্যবহারে কোন যোগাযোগ-বাধা তৈরি হয়?", ["শব্দার্থগত (ভাষাগত) বাধা", "ভৌত বাধা", "সাংগঠনিক বাধা", "ব্যক্তিগত বাধা"],
       "বার্তা পাঠানো হয় কিন্তু বোঝা যায় না; সহজ ভাষা আর হাতে-কলমে দেখানো সাহায্য করে।"),
    _q("A leader who makes decisions alone and expects obedience follows which style?", ["Autocratic", "Democratic", "Laissez-faire", "Participative"],
       "It can work in emergencies on site but often lowers morale in the long run.",
       "যে নেতা একাই সিদ্ধান্ত নেন আর আনুগত্য আশা করেন, তিনি কোন রীতি মানেন?", ["স্বৈরতান্ত্রিক", "গণতান্ত্রিক", "অবাধ (লেসে-ফেয়ার)", "অংশগ্রহণমূলক"],
       "সাইটে জরুরি অবস্থায় এটা কাজ করতে পারে কিন্তু দীর্ঘমেয়াদে প্রায়ই মনোবল কমায়।"),
    _q("Delegation of authority means…", ["Giving a subordinate the power to act, while the manager remains accountable", "Passing all responsibility and accountability downwards", "Taking power away from staff", "Firing employees"],
       "Authority can be delegated; ultimate accountability cannot.",
       "কর্তৃত্ব অর্পণ মানে…", ["অধস্তনকে কাজ করার ক্ষমতা দেওয়া, যদিও জবাবদিহি ম্যানেজারেরই থাকে", "সব দায়িত্ব আর জবাবদিহি নিচে পাঠানো", "কর্মীদের ক্ষমতা কেড়ে নেওয়া", "কর্মী বরখাস্ত করা"],
       "কর্তৃত্ব অর্পণ করা যায়; চূড়ান্ত জবাবদিহি করা যায় না।"),
    _q("Which of these is an example of a non-financial incentive?", ["Recognition and a chance of promotion", "A cash bonus", "Profit sharing", "A pay rise"],
       "Status, job security and challenging work also motivate, often as much as money.",
       "এগুলোর মধ্যে কোনটা অ-আর্থিক প্রণোদনার উদাহরণ?", ["স্বীকৃতি আর পদোন্নতির সুযোগ", "নগদ বোনাস", "মুনাফার ভাগ", "বেতন বৃদ্ধি"],
       "মর্যাদা, চাকরির নিরাপত্তা আর চ্যালেঞ্জিং কাজও অনুপ্রাণিত করে, প্রায়ই টাকার মতোই।"),
    _q("What does 'span of control' mean?", ["The number of subordinates a manager directly supervises", "The length of a bridge span", "The total budget of a department", "The working hours of a manager"],
       "A narrow span means more layers of management; a wide span means a flatter organisation.",
       "'নিয়ন্ত্রণের পরিসর' মানে কী?", ["একজন ম্যানেজার সরাসরি কতজন অধস্তনকে তত্ত্বাবধান করেন", "সেতুর একটা স্প্যানের দৈর্ঘ্য", "একটা বিভাগের মোট বাজেট", "ম্যানেজারের কাজের সময়"],
       "সরু পরিসর মানে ব্যবস্থাপনার বেশি স্তর; চওড়া পরিসর মানে চ্যাপ্টা প্রতিষ্ঠান।"),
    _q("A matrix organisation is common in engineering firms because…", ["Staff report to both a functional head and a project manager", "There are no managers", "Each worker reports only to the owner", "It has one department only"],
       "It shares specialists across projects but can create conflicts between two bosses.",
       "প্রকৌশল-সংস্থায় ম্যাট্রিক্স সংগঠন প্রচলিত কারণ…", ["কর্মীরা একজন বিভাগীয় প্রধান আর একজন প্রকল্প-ম্যানেজার দুজনের কাছেই রিপোর্ট করেন", "কোনো ম্যানেজার নেই", "প্রত্যেক কর্মী কেবল মালিকের কাছে রিপোর্ট করেন", "এর কেবল একটা বিভাগ"],
       "এটা প্রকল্পগুলোর মধ্যে বিশেষজ্ঞ ভাগ করে, কিন্তু দুই বসের মধ্যে দ্বন্দ্ব তৈরি করতে পারে।"),
    _q("Why do companies prepare a budget?", ["To plan, coordinate and control activities against targets", "To record past transactions only", "To calculate share prices", "To replace accounting"],
       "Budgets turn plans into numbers; comparing actuals with them shows where action is needed.",
       "কোম্পানিগুলো বাজেট তৈরি করে কেন?", ["লক্ষ্যের বিপরীতে কাজ পরিকল্পনা, সমন্বয় আর নিয়ন্ত্রণ করতে", "কেবল অতীতের লেনদেন লিখতে", "শেয়ারের দাম হিসাব করতে", "হিসাবরক্ষণের বদলে"],
       "বাজেট পরিকল্পনাকে সংখ্যায় রূপ দেয়; প্রকৃতের সঙ্গে তুলনা দেখায় কোথায় ব্যবস্থা লাগবে।"),
    _q("What is a flexible budget?", ["One adjusted to the actual level of activity achieved", "One that never changes", "One for a single day", "One without any costs"],
       "It separates fixed and variable costs so that performance is judged at the real output level.",
       "নমনীয় বাজেট কী?", ["প্রকৃত কাজের স্তর অনুযায়ী সমন্বয় করা বাজেট", "যা কখনো বদলায় না", "এক দিনের বাজেট", "কোনো খরচ ছাড়া বাজেট"],
       "এটা স্থির আর পরিবর্তনশীল খরচ আলাদা করে, যাতে প্রকৃত উৎপাদন-স্তরে কর্মক্ষমতা বিচার হয়।"),
    _q("Under the FIFO method, closing stock is valued at…", ["The most recent purchase prices", "The oldest purchase prices", "The average of all prices", "The selling price"],
       "Goods bought first are assumed to be used first, so what is left is the latest stock.",
       "এফআইএফও পদ্ধতিতে সমাপনী মজুতের মূল্য ধরা হয়…", ["সাম্প্রতিকতম ক্রয়মূল্যে", "সবচেয়ে পুরোনো ক্রয়মূল্যে", "সব দামের গড়ে", "বিক্রয়মূল্যে"],
       "প্রথমে কেনা মাল প্রথমে ব্যবহৃত ধরা হয়, তাই বাকি থাকে সর্বশেষ মজুত।"),
    _q("Which of these is an intangible asset?", ["A patent or trademark", "A building", "Cash in hand", "Stock of cement"],
       "Intangible assets have value without physical form; most are amortised over their useful life.",
       "এগুলোর মধ্যে কোনটা অস্পৃশ্য সম্পদ?", ["পেটেন্ট বা ট্রেডমার্ক", "একটা ভবন", "হাতে নগদ", "সিমেন্টের মজুত"],
       "অস্পৃশ্য সম্পদের বাস্তব রূপ ছাড়াই মূল্য থাকে; বেশিরভাগের উপযোগী আয়ু জুড়ে পরিশোধ হয়।"),
    _q("A contingent liability, such as a pending court case, is shown…", ["As a note to the accounts, not in the balance sheet total", "As a fixed asset", "As income", "Not at all"],
       "It may or may not turn into a real liability; if it becomes probable, a provision is made.",
       "বিচারাধীন মামলার মতো সম্ভাব্য দায় দেখানো হয়…", ["হিসাবের টীকায়, স্থিতিপত্রের মোট অঙ্কে নয়", "স্থায়ী সম্পদ হিসেবে", "আয় হিসেবে", "একদমই নয়"],
       "এটা প্রকৃত দায়ে পরিণত হতেও পারে, না-ও পারে; সম্ভাব্য হয়ে উঠলে সংস্থান রাখা হয়।"),
    _q("Which statement about outsourcing is correct?", ["Contracting work to outside specialists so the firm can focus on its core activities", "Doing every task in-house", "Selling the whole company", "Hiring only temporary staff"],
       "A bridge builder may outsource piling to a specialist subcontractor.",
       "আউটসোর্সিং সম্পর্কে কোন বিবৃতি সঠিক?", ["বাইরের বিশেষজ্ঞদের কাজ দিয়ে সংস্থা নিজের মূল কাজে মন দেয়", "সব কাজ নিজেরাই করা", "পুরো কোম্পানি বেচে দেওয়া", "কেবল অস্থায়ী কর্মী নিয়োগ"],
       "একজন সেতু-নির্মাতা পাইলিংয়ের কাজ একজন বিশেষজ্ঞ উপ-ঠিকাদারকে দিতে পারেন।"),
    _q("Which statement best describes an MSME in India?", ["A micro, small or medium enterprise classified by investment and turnover", "Any multinational company", "A government ministry", "A stock exchange"],
       "MSMEs get priority-sector lending and other support, and employ a large share of India's workforce.",
       "ভারতে এমএসএমই-কে কোন বিবৃতি সবচেয়ে ভালো বর্ণনা করে?", ["বিনিয়োগ আর লেনদেন অনুযায়ী শ্রেণিভুক্ত অতি-ক্ষুদ্র, ক্ষুদ্র বা মাঝারি উদ্যোগ", "যেকোনো বহুজাতিক কোম্পানি", "একটা সরকারি মন্ত্রক", "একটা শেয়ারবাজার"],
       "এমএসএমই অগ্রাধিকার-খাতের ঋণ আর অন্যান্য সহায়তা পায়, আর ভারতের কর্মশক্তির বড় অংশকে কাজ দেয়।"),
    _q("A tender is awarded on the L1 basis. What does L1 mean?", ["The lowest technically qualified bid", "The first bid received", "The bid with the most pages", "The highest bid"],
       "Only bids that pass the technical evaluation are compared on price.",
       "একটা দরপত্র এল1 ভিত্তিতে দেওয়া হয়। এল1 মানে কী?", ["কারিগরিভাবে যোগ্য সর্বনিম্ন দর", "প্রথম জমা পড়া দর", "সবচেয়ে বেশি পাতার দর", "সর্বোচ্চ দর"],
       "কেবল কারিগরি মূল্যায়নে উত্তীর্ণ দরগুলোই দামের ভিত্তিতে তুলনা হয়।"),
    _q("What does a 'bill of quantities' in a construction tender list?", ["The items of work with their quantities, to be priced by bidders", "The contractor's bank balance", "The project's final accounts only", "The workers' names"],
       "Bidders fill in rates; the totals give comparable prices and later the basis for measured payments.",
       "নির্মাণ-দরপত্রের 'পরিমাণ-তালিকা' কী তালিকাভুক্ত করে?", ["কাজের আইটেম আর তাদের পরিমাণ, দরদাতারা যার দাম বসান", "ঠিকাদারের ব্যাংক-জের", "কেবল প্রকল্পের চূড়ান্ত হিসাব", "কর্মীদের নাম"],
       "দরদাতারা হার বসান; মোট অঙ্কে তুলনীয় দাম পাওয়া যায়, আর পরে মাপা কাজের অর্থপ্রদানের ভিত্তি হয়।"),
    _q("Why is internal audit useful to a company?", ["It independently checks that controls work and records are reliable", "It replaces the statutory auditor", "It sets the share price", "It collects taxes"],
       "Internal auditors report to management or the audit committee throughout the year.",
       "অভ্যন্তরীণ নিরীক্ষা একটা কোম্পানির কাছে উপকারী কেন?", ["নিয়ন্ত্রণ কাজ করছে আর নথি নির্ভরযোগ্য কিনা তা স্বাধীনভাবে যাচাই করে", "এটা বিধিবদ্ধ নিরীক্ষকের জায়গা নেয়", "শেয়ারের দাম ঠিক করে", "কর আদায় করে"],
       "অভ্যন্তরীণ নিরীক্ষকেরা সারা বছর পরিচালনা বা নিরীক্ষা কমিটির কাছে রিপোর্ট করেন।"),
    _q("Which type of cost should be ignored when choosing between two future options?", ["A cost already incurred that cannot be recovered", "Future cash costs that differ between the options", "Opportunity costs", "Incremental costs"],
       "Only relevant costs - future and different between the options - should drive the decision.",
       "ভবিষ্যতের দুটো বিকল্পের মধ্যে বাছার সময় কোন ধরনের খরচ উপেক্ষা করা উচিত?", ["ইতিমধ্যে হয়ে যাওয়া খরচ যা আর ফেরত পাওয়া যাবে না", "ভবিষ্যতের নগদ খরচ যা বিকল্পভেদে আলাদা", "সুযোগ-খরচ", "বর্ধিত খরচ"],
       "কেবল প্রাসঙ্গিক খরচ - ভবিষ্যতের আর বিকল্পভেদে আলাদা - সিদ্ধান্ত চালাবে।"),
    _q("What is a 'make or buy' decision about?", ["Whether to produce a part in-house or purchase it from a supplier", "Whether to hire or fire staff", "Whether to issue shares or debentures", "Whether to pay tax now or later"],
       "Compare the relevant in-house cost with the purchase price, and weigh quality and control too.",
       "'তৈরি না কেনা' সিদ্ধান্ত কী নিয়ে?", ["একটা যন্ত্রাংশ নিজেরা তৈরি করা হবে নাকি সরবরাহকারীর কাছ থেকে কেনা হবে", "কর্মী নিয়োগ নাকি ছাঁটাই", "শেয়ার নাকি ডিবেঞ্চার ইস্যু", "কর এখন নাকি পরে"],
       "নিজে তৈরির প্রাসঙ্গিক খরচকে ক্রয়মূল্যের সঙ্গে তুলনা করো, আর গুণমান ও নিয়ন্ত্রণও বিবেচনা করো।"),
    _q("A company holds too little inventory. Which cost rises?", ["Stock-out (shortage) costs such as idle crews and lost sales", "Storage costs", "Insurance on stock", "Deterioration of stock"],
       "Holding costs rise with more stock; ordering and shortage costs rise with less. The EOQ balances them.",
       "একটা কোম্পানি খুব কম মজুত রাখে। কোন খরচ বাড়ে?", ["মজুত-শূন্যতার (ঘাটতির) খরচ, যেমন অলস দল আর হারানো বিক্রি", "গুদামজাতকরণ খরচ", "মজুতের বিমা", "মজুতের নষ্ট হওয়া"],
       "বেশি মজুতে রক্ষণ-খরচ বাড়ে; কম মজুতে অর্ডার আর ঘাটতির খরচ বাড়ে। মিতব্যয়ী অর্ডার-পরিমাণ এদের ভারসাম্য করে।"),
    _q("Which document is the formal request from a buyer to a supplier to supply goods?", ["A purchase order", "An invoice", "A receipt", "A delivery challan"],
       "The supplier then sends goods with a delivery challan and bills with an invoice.",
       "কোন নথি সরবরাহকারীর কাছে মাল সরবরাহের জন্য ক্রেতার আনুষ্ঠানিক অনুরোধ?", ["ক্রয়াদেশ (পারচেজ অর্ডার)", "চালান (ইনভয়েস)", "রসিদ", "সরবরাহ-চালান"],
       "সরবরাহকারী তারপর সরবরাহ-চালানসহ মাল পাঠান আর ইনভয়েস দিয়ে বিল করেন।"),
    _q("Which account is credited when a business receives cash from a customer who owed it money?", ["The debtor's (customer's) account", "The cash account", "The capital account", "The sales account"],
       "Cash (an asset) increases and is debited; the debtor's balance falls and is credited.",
       "পাওনাদার গ্রাহকের কাছ থেকে নগদ পেলে কোন খাত ক্রেডিট হয়?", ["দেনাদারের (গ্রাহকের) খাত", "নগদ খাত", "মূলধন খাত", "বিক্রয় খাত"],
       "নগদ (সম্পদ) বাড়ে, তাই ডেবিট; দেনাদারের জের কমে, তাই ক্রেডিট।"),
    _q("Goods withdrawn by the owner for personal use are recorded as…", ["Drawings, reducing capital", "Sales", "An expense of the business", "A new asset"],
       "Drawings account is debited and purchases (or stock) is credited at cost.",
       "মালিক ব্যক্তিগত ব্যবহারের জন্য মাল তুলে নিলে তা লেখা হয়…", ["উত্তোলন হিসেবে, যা মূলধন কমায়", "বিক্রি হিসেবে", "ব্যবসার খরচ হিসেবে", "নতুন সম্পদ হিসেবে"],
       "উত্তোলন খাত ডেবিট আর ক্রয় (বা মজুত) খাত খরচ-মূল্যে ক্রেডিট হয়।"),
    _q("Accrued (outstanding) wages at year end are shown in the balance sheet as…", ["A current liability", "A current asset", "Income", "Capital"],
       "The work was done this year, so the cost belongs to this year even though it is paid next year.",
       "বছরশেষে বকেয়া মজুরি স্থিতিপত্রে দেখানো হয়…", ["চলতি দায় হিসেবে", "চলতি সম্পদ হিসেবে", "আয় হিসেবে", "মূলধন হিসেবে"],
       "কাজ এই বছর হয়েছে, তাই পরের বছর দেওয়া হলেও খরচটা এই বছরের।"),
    _q("Rent paid in advance for next year is shown as…", ["A prepaid expense, a current asset", "A liability", "This year's expense", "Capital"],
       "The benefit has not yet been received, so it is carried forward as an asset.",
       "পরের বছরের অগ্রিম দেওয়া ভাড়া দেখানো হয়…", ["অগ্রিম প্রদত্ত খরচ, একটা চলতি সম্পদ হিসেবে", "দায় হিসেবে", "এই বছরের খরচ হিসেবে", "মূলধন হিসেবে"],
       "সুবিধা এখনো পাওয়া যায়নি, তাই সম্পদ হিসেবে পরের বছরে নেওয়া হয়।"),
    _q("A provision for doubtful debts is created because of which concept?", ["Prudence (conservatism)", "Going concern", "Money measurement", "Separate entity"],
       "Some customers may not pay; recognising the likely loss now avoids overstating profit and assets.",
       "কোন ধারণার কারণে অনাদায়ী পাওনার সংস্থান তৈরি করা হয়?", ["বিচক্ষণতা (রক্ষণশীলতা)", "চলমান প্রতিষ্ঠান", "অর্থ-পরিমাপ", "পৃথক সত্তা"],
       "কিছু গ্রাহক টাকা নাও দিতে পারেন; সম্ভাব্য ক্ষতি এখনই স্বীকার করলে মুনাফা আর সম্পদ বাড়িয়ে দেখানো হয় না।"),
    _q("When a partner retires, the remaining partners acquire his share in…", ["Their gaining ratio", "The old profit ratio", "Equal shares always", "Their capital ratio"],
       "Gaining ratio = new share - old share; they compensate the retiring partner for goodwill in this ratio.",
       "একজন অংশীদার অবসর নিলে বাকি অংশীদাররা তাঁর অংশ নেন…", ["তাঁদের লাভের অনুপাতে", "পুরোনো মুনাফা-অনুপাতে", "সবসময় সমানভাগে", "তাঁদের মূলধন-অনুপাতে"],
       "লাভের অনুপাত = নতুন ভাগ - পুরোনো ভাগ; অবসরপ্রাপ্ত অংশীদারকে সুনামের ক্ষতিপূরণ এই অনুপাতে দেওয়া হয়।"),
    _q("Forfeiture of shares happens when…", ["A shareholder fails to pay calls due on the shares", "The company makes a profit", "Shares are split", "A dividend is declared"],
       "The amount already received is kept in a forfeited shares account; the shares can be reissued.",
       "শেয়ার বাজেয়াপ্ত হয় যখন…", ["শেয়ারহোল্ডার শেয়ারের বকেয়া তলবি টাকা দেন না", "কোম্পানি মুনাফা করে", "শেয়ার বিভাজিত হয়", "লভ্যাংশ ঘোষিত হয়"],
       "ইতিমধ্যে পাওয়া টাকা বাজেয়াপ্ত শেয়ার খাতে থাকে; শেয়ারগুলো আবার ইস্যু করা যায়।"),
    _q("What is the purpose of a 'suspense account' when a trial balance does not agree?", ["To hold the difference temporarily until the errors are found", "To record sales", "To pay suppliers", "To store goodwill"],
       "As each error is found and corrected, the suspense account is cleared to zero.",
       "রেওয়ামিল না মিললে 'অনিশ্চিত খাত'-এর উদ্দেশ্য কী?", ["ভুল খুঁজে না পাওয়া পর্যন্ত পার্থক্যটা সাময়িকভাবে রাখা", "বিক্রি লেখা", "সরবরাহকারীকে টাকা দেওয়া", "সুনাম রাখা"],
       "প্রতিটি ভুল খুঁজে সংশোধন করলে অনিশ্চিত খাত শূন্যে নেমে আসে।"),
    _q("Which of these is an example of a fictitious asset?", ["Preliminary expenses not yet written off", "Land", "Stock", "Cash at bank"],
       "It has no real value; modern standards require such costs to be expensed rather than carried as assets.",
       "এগুলোর মধ্যে কোনটা কাল্পনিক সম্পদের উদাহরণ?", ["এখনো অবলোপন না হওয়া প্রাথমিক ব্যয়", "জমি", "মজুত", "ব্যাংকে নগদ"],
       "এর কোনো প্রকৃত মূল্য নেই; আধুনিক হিসাবমান এমন খরচকে সম্পদ না রেখে খরচ হিসেবে লিখতে বলে।"),
    _q("What does a 'contribution' in marginal costing cover?", ["Fixed costs first, then profit", "Only variable costs", "Only taxes", "Only selling expenses"],
       "Contribution = sales - variable cost; once fixed costs are covered, every extra rupee of contribution is profit.",
       "প্রান্তিক ব্যয়করণে 'অবদান' কী ঢাকে?", ["প্রথমে স্থির খরচ, তারপর মুনাফা", "কেবল পরিবর্তনশীল খরচ", "কেবল কর", "কেবল বিক্রয়-ব্যয়"],
       "অবদান = বিক্রি - পরিবর্তনশীল খরচ; স্থির খরচ ঢাকা হয়ে গেলে অবদানের প্রতিটি বাড়তি টাকাই মুনাফা।"),
    _q("A 'key factor' (limiting factor) in production planning is…", ["The scarce resource that restricts output, such as machine hours", "The cheapest raw material", "The sales tax rate", "The company's name"],
       "When a factor is scarce, rank products by contribution per unit of that factor.",
       "উৎপাদন-পরিকল্পনায় 'মূল উপাদান' (সীমাবদ্ধকারী উপাদান) হলো…", ["যে দুষ্প্রাপ্য সম্পদ উৎপাদন সীমিত করে, যেমন যন্ত্র-ঘণ্টা", "সবচেয়ে সস্তা কাঁচামাল", "বিক্রয়-করের হার", "কোম্পানির নাম"],
       "কোনো উপাদান দুষ্প্রাপ্য হলে সেই উপাদানের এককপ্রতি অবদান অনুযায়ী পণ্যগুলোর ক্রম ঠিক করো।"),
    _q("Which statement about economies of scale is correct?", ["Average cost per unit falls as output grows, up to a point", "Costs always rise with output", "Small firms always have lower costs", "Output does not affect cost"],
       "Bulk buying and specialised machinery spread fixed costs; too large a scale can bring diseconomies.",
       "মাপের সাশ্রয় সম্পর্কে কোন বিবৃতি সঠিক?", ["একটা সীমা পর্যন্ত উৎপাদন বাড়লে এককপ্রতি গড় খরচ কমে", "উৎপাদনের সঙ্গে খরচ সবসময় বাড়ে", "ছোট সংস্থার খরচ সবসময় কম", "উৎপাদন খরচকে প্রভাবিত করে না"],
       "একসঙ্গে প্রচুর কেনা আর বিশেষ যন্ত্র স্থির খরচ ছড়িয়ে দেয়; খুব বড় মাপে আবার অসাশ্রয় আসতে পারে।"),
    _q("A 5S programme on a site aims to…", ["Organise the workplace: sort, set in order, shine, standardise, sustain", "Increase prices by 5%", "Hire five supervisors", "Work five shifts a day"],
       "A tidy, well-organised site is safer and wastes less time searching for tools.",
       "সাইটে 5এস কর্মসূচির লক্ষ্য…", ["কর্মস্থল গোছানো: বাছাই, সাজানো, পরিষ্কার, মানক করা, বজায় রাখা", "দাম 5% বাড়ানো", "পাঁচজন সুপারভাইজার নিয়োগ", "দিনে পাঁচ শিফটে কাজ"],
       "পরিপাটি, সুসংগঠিত সাইট বেশি নিরাপদ আর যন্ত্র খুঁজতে কম সময় নষ্ট হয়।"),
    _q("Which statement about a sole proprietorship is correct?", ["The owner has unlimited personal liability for business debts", "It must have at least seven members", "It is a separate legal entity", "It cannot be closed"],
       "It is the simplest form of business, but the owner's personal assets are at risk.",
       "একমালিকানা ব্যবসা সম্পর্কে কোন বিবৃতি সঠিক?", ["ব্যবসার দেনার জন্য মালিকের ব্যক্তিগত দায় অসীম", "অন্তত সাতজন সদস্য লাগে", "এটা পৃথক আইনি সত্তা", "এটা বন্ধ করা যায় না"],
       "এটা সবচেয়ে সহজ ব্যবসার রূপ, কিন্তু মালিকের ব্যক্তিগত সম্পদ ঝুঁকিতে থাকে।"),
    _q("What is 'e-procurement' in public works?", ["Buying goods and services through online tendering platforms", "Paying workers in cash", "Ordering by post only", "Selling scrap at auction"],
       "India's Central Public Procurement Portal and GeM make bidding more transparent and competitive.",
       "সরকারি কাজে 'ই-প্রকিউরমেন্ট' কী?", ["অনলাইন দরপত্র-প্ল্যাটফর্মের মাধ্যমে পণ্য আর সেবা কেনা", "কর্মীদের নগদে মজুরি দেওয়া", "কেবল ডাকে অর্ডার দেওয়া", "নিলামে ভাঙাচোরা বেচা"],
       "ভারতের কেন্দ্রীয় সরকারি ক্রয় পোর্টাল আর জেম দরপত্রকে আরও স্বচ্ছ আর প্রতিযোগিতামূলক করে।"),
    _q("What does 'quality assurance' focus on, compared with 'quality control'?", ["Preventing defects through good processes, rather than finding them after production", "Only inspecting finished goods", "Reducing prices", "Marketing the product"],
       "QA designs the system right; QC inspects the output. Both are needed on a bridge site.",
       "'গুণমান নিশ্চিতকরণ' 'গুণমান নিয়ন্ত্রণের' তুলনায় কীসে জোর দেয়?", ["উৎপাদনের পরে ত্রুটি খোঁজার বদলে ভালো প্রক্রিয়ায় ত্রুটি প্রতিরোধ", "কেবল তৈরি পণ্য পরিদর্শন", "দাম কমানো", "পণ্যের বিপণন"],
       "গুণমান নিশ্চিতকরণ ব্যবস্থাটা ঠিকঠাক গড়ে; গুণমান নিয়ন্ত্রণ ফলাফল পরিদর্শন করে। সেতুর সাইটে দুটোই লাগে।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
