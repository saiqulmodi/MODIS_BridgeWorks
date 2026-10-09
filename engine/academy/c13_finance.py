"""NIT level - Finance (engineering economics and corporate finance, entrance and first-year
B.Tech/BBA standard): nominal and effective rates, continuous compounding, annuities and
perpetuities, loan schedules, depreciation methods, valuation of shares and bonds, the cost of
capital, CAPM and portfolios, leverage and ratios, options and forwards, money and banking in India."""
import math

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


# ---------------------------------------------------------------- interest and time value
def ear(r, m, how_en, how_bn):
    e = ((1 + r / 100 / m) ** m - 1) * 100
    return _n(f"A deposit pays {r}% a year compounded {how_en}. What is the effective annual rate?",
              f"একটা আমানতে বছরে {r}% সুদ, {how_bn} চক্রবৃদ্ধি। কার্যকর বার্ষিক হার কত?", e,
              f"EAR = (1 + {r}%/{m})^{m} - 1 = {_f(_c(e))}%. More frequent compounding raises the true yield.",
              f"কার্যকর হার = (1 + {r}%/{m})^{m} - 1 = {_f(_c(e))}%। ঘনঘন চক্রবৃদ্ধিতে প্রকৃত আয় বাড়ে।",
              (r, r / m, e + 0.5), "%")


def continuous(r):
    e = (math.exp(r / 100) - 1) * 100
    return _n(f"What is the effective annual rate of {r}% a year compounded continuously?",
              f"বছরে {r}% সুদ অবিরত চক্রবৃদ্ধিতে কার্যকর বার্ষিক হার কত?", e,
              f"EAR = e^{r / 100:g} - 1 = {_f(_c(e))}% - the upper limit of compounding more and more often.",
              f"কার্যকর হার = e^{r / 100:g} - 1 = {_f(_c(e))}% - ঘনঘন চক্রবৃদ্ধির ঊর্ধ্বসীমা।",
              (r, r * 1.1, e + 1), "%")


def fv(p, r, n):
    v = p * (1 + r / 100) ** n
    return _rs(f"Rs {p:,} is invested at {r}% a year compound interest. What is it worth after {n} years?",
               f"Rs {p:,} বছরে {r}% চক্রবৃদ্ধি সুদে বিনিয়োগ করা হল। {n} বছর পরে এর মূল্য কত?", v,
               f"FV = P(1 + r)ⁿ = {p:,} x {1 + r / 100:g}^{n} = Rs {_f(_c(v))}.",
               f"ভবিষ্যৎ মূল্য = P(1 + r)ⁿ = {p:,} x {1 + r / 100:g}^{n} = Rs {_f(_c(v))}।",
               (p * (1 + r * n / 100), p * (1 + r / 100), v + p))


def pv(f, r, n):
    v = f / (1 + r / 100) ** n
    return _rs(f"How much must be invested today at {r}% compound interest to have Rs {f:,} in {n} years?",
               f"{n} বছরে Rs {f:,} পেতে আজ {r}% চক্রবৃদ্ধি সুদে কত বিনিয়োগ করতে হবে?", v,
               f"PV = F ÷ (1 + r)ⁿ = {f:,} ÷ {1 + r / 100:g}^{n} = Rs {_f(_c(v))}.",
               f"বর্তমান মূল্য = F ÷ (1 + r)ⁿ = {f:,} ÷ {1 + r / 100:g}^{n} = Rs {_f(_c(v))}।",
               (f * (1 - r * n / 100), f / (1 + r / 100), f))


def rule72(r):
    y = 72 / r
    return _n(f"Using the rule of 72, roughly how many years does money take to double at {r}% a year?",
              f"72-এর নিয়মে বছরে {r}% হারে টাকা দ্বিগুণ হতে মোটামুটি কত বছর লাগে?", y,
              f"72 ÷ {r} = {_f(_c(y))} years; the exact answer is ln 2 ÷ ln(1 + r).",
              f"72 ÷ {r} = {_f(_c(y))} বছর; সঠিক উত্তর ln 2 ÷ ln(1 + r)।",
              (100 / r, 72 / r * 2, r), " years", " বছর")


def fv_annuity(a, r, n):
    v = a * ((1 + r / 100) ** n - 1) / (r / 100)
    return _rs(f"Rs {a:,} is deposited at the end of every year for {n} years at {r}% interest. What is the total at the end?",
               f"{n} বছর ধরে প্রতি বছরের শেষে Rs {a:,} করে {r}% সুদে জমা রাখা হয়। শেষে মোট কত হয়?", v,
               f"FV of an ordinary annuity = A[(1 + r)ⁿ - 1] ÷ r = Rs {_f(_c(v))}.",
               f"সাধারণ বার্ষিকীর ভবিষ্যৎ মূল্য = A[(1 + r)ⁿ - 1] ÷ r = Rs {_f(_c(v))}।",
               (a * n, a * n * (1 + r / 100), v * (1 + r / 100)))


def pv_annuity(a, r, n):
    v = a * (1 - (1 + r / 100) ** -n) / (r / 100)
    return _rs(f"What is the present value of Rs {a:,} received at the end of each year for {n} years, at {r}%?",
               f"{r}% হারে, {n} বছর ধরে প্রতি বছরের শেষে পাওয়া Rs {a:,}-এর বর্তমান মূল্য কত?", v,
               f"PV = A[1 - (1 + r)⁻ⁿ] ÷ r = Rs {_f(_c(v))}.",
               f"বর্তমান মূল্য = A[1 - (1 + r)⁻ⁿ] ÷ r = Rs {_f(_c(v))}।",
               (a * n, a * n / (1 + r / 100), v * (1 + r / 100)))


def annuity_due(a, r, n):
    v = a * (1 - (1 + r / 100) ** -n) / (r / 100) * (1 + r / 100)
    return _rs(f"A lease needs Rs {a:,} at the START of each year for {n} years. At {r}%, what is its present value?",
               f"একটা ইজারায় {n} বছর ধরে প্রতি বছরের শুরুতে Rs {a:,} দিতে হয়। {r}% হারে এর বর্তমান মূল্য কত?", v,
               f"An annuity due is an ordinary annuity x (1 + r): Rs {_f(_c(v))}.",
               f"অগ্রিম বার্ষিকী = সাধারণ বার্ষিকী x (1 + r): Rs {_f(_c(v))}।",
               (v / (1 + r / 100), a * n, v * (1 + r / 100)))


def perpetuity(c, r):
    v = c / (r / 100)
    return _rs(f"An endowment pays Rs {c:,} a year forever. At a discount rate of {r}%, what is it worth today?",
               f"একটা অনুদান চিরকাল বছরে Rs {c:,} দেয়। {r}% বাট্টা হারে আজ এর মূল্য কত?", v,
               f"Perpetuity value = C ÷ r = {c:,} ÷ {r / 100:g} = Rs {_f(_c(v))}.",
               f"চিরস্থায়ী আয়ের মূল্য = C ÷ r = {c:,} ÷ {r / 100:g} = Rs {_f(_c(v))}।",
               (c * r, c * 100 / (r + 2), v / 2))


def growing_perp(c, r, g):
    v = c / ((r - g) / 100)
    return _rs(f"A payment of Rs {c:,} next year will grow at {g}% a year forever. At {r}%, what is it worth today?",
               f"আগামী বছর Rs {c:,}-এর একটা প্রদান চিরকাল বছরে {g}% হারে বাড়বে। {r}% হারে আজ এর মূল্য কত?", v,
               f"Growing perpetuity = C ÷ (r - g) = {c:,} ÷ {(r - g) / 100:g} = Rs {_f(_c(v))}.",
               f"বর্ধমান চিরস্থায়ী আয় = C ÷ (r - g) = {c:,} ÷ {(r - g) / 100:g} = Rs {_f(_c(v))}।",
               (c / (r / 100), c / ((r + g) / 100), v / 2))


def emi(p, r, n):
    i = r / 1200
    e = p * i * (1 + i) ** n / ((1 + i) ** n - 1)
    return _rs(f"A loan of Rs {p:,} at {r}% a year is repaid in {n} equal monthly instalments. What is the EMI?",
               f"বছরে {r}% সুদে Rs {p:,} ঋণ {n}টি সমান মাসিক কিস্তিতে শোধ হবে। মাসিক কিস্তি কত?", e,
               f"EMI = P i (1 + i)ⁿ ÷ [(1 + i)ⁿ - 1] with i = {r}%/12: Rs {_f(_c(e))}.",
               f"কিস্তি = P i (1 + i)ⁿ ÷ [(1 + i)ⁿ - 1], i = {r}%/12: Rs {_f(_c(e))}।",
               (p / n, p * (1 + r / 100) / n, e * 1.1))


def first_interest(p, r):
    v = p * r / 1200
    return _rs(f"In the first month of a Rs {p:,} home loan at {r}% a year, how much of the EMI is interest?",
               f"বছরে {r}% সুদে Rs {p:,} গৃহঋণের প্রথম মাসে কিস্তির কতটা সুদ?", v,
               f"Interest = outstanding balance x monthly rate = {p:,} x {r}%/12 = Rs {_f(_c(v))}; the rest of the EMI repays principal.",
               f"সুদ = বকেয়া x মাসিক হার = {p:,} x {r}%/12 = Rs {_f(_c(v))}; কিস্তির বাকিটা আসল শোধ করে।",
               (p * r / 100, v / 2, v * 1.5))


def sinking(f, r, n):
    a = f * (r / 100) / ((1 + r / 100) ** n - 1)
    return _rs(f"A company must have Rs {f:,} in {n} years to replace a machine. With {r}% interest, how much should it set aside each year?",
               f"একটা যন্ত্র বদলাতে একটা কোম্পানির {n} বছরে Rs {f:,} লাগবে। {r}% সুদে প্রতি বছর কত আলাদা রাখা উচিত?", a,
               f"Sinking fund A = F r ÷ [(1 + r)ⁿ - 1] = Rs {_f(_c(a))}.",
               f"নিমজ্জমান তহবিল A = F r ÷ [(1 + r)ⁿ - 1] = Rs {_f(_c(a))}।",
               (f / n, f / n / (1 + r / 100), a * 1.2))


def syd(cost, salv, n):
    d = (cost - salv) * n / (n * (n + 1) / 2)
    return _rs(f"A machine costs Rs {cost:,}, has a salvage value of Rs {salv:,} and a life of {n} years. What is the first year's depreciation by the sum-of-years'-digits method?",
               f"একটা যন্ত্রের দাম Rs {cost:,}, অবশেষ মূল্য Rs {salv:,} আর আয়ু {n} বছর। বছর-অঙ্কের-যোগফল পদ্ধতিতে প্রথম বছরের অবচয় কত?", d,
               f"Digits sum to {n * (n + 1) // 2}; year 1 takes {n}/{n * (n + 1) // 2} of {cost - salv:,} = Rs {_f(_c(d))}.",
               f"অঙ্কের যোগফল {n * (n + 1) // 2}; প্রথম বছর নেয় {cost - salv:,}-এর {n}/{n * (n + 1) // 2} = Rs {_f(_c(d))}।",
               ((cost - salv) / n, cost * 2 / n, d / 2))


def ddb(cost, n):
    d = cost * 2 / n
    return _rs(f"An asset costing Rs {cost:,} with a {n}-year life is depreciated by the double-declining-balance method. What is the first year's charge?",
               f"Rs {cost:,} দামের, {n} বছর আয়ুর একটা সম্পদে দ্বিগুণ-ক্রমহ্রাসমান পদ্ধতিতে অবচয় হয়। প্রথম বছরের অবচয় কত?", d,
               f"Rate = 2 ÷ {n} = {200 / n:g}%; {cost:,} x {200 / n:g}% = Rs {_f(_c(d))}.",
               f"হার = 2 ÷ {n} = {200 / n:g}%; {cost:,} x {200 / n:g}% = Rs {_f(_c(d))}।",
               (cost / n, d * 2, cost - d))


def capitalised(p, a, i):
    v = p + a / (i / 100)
    return _rs(f"A footbridge costs Rs {p:,} to build and Rs {a:,} a year to maintain forever. At {i}%, what is its capitalised cost?",
               f"একটা পায়ে-চলা সেতু বানাতে Rs {p:,} আর চিরকাল রক্ষণাবেক্ষণে বছরে Rs {a:,} লাগে। {i}% হারে এর মূলধনীকৃত খরচ কত?", v,
               f"Capitalised cost = P + A ÷ i = {p:,} + {a:,} ÷ {i / 100:g} = Rs {_f(_c(v))}.",
               f"মূলধনীকৃত খরচ = P + A ÷ i = {p:,} + {a:,} ÷ {i / 100:g} = Rs {_f(_c(v))}।",
               (p + a * i, p + a, a / (i / 100)))


def npv2(c0, c1, c2, r):
    v = -c0 + c1 / (1 + r / 100) + c2 / (1 + r / 100) ** 2
    return _rs(f"A machine costs Rs {c0:,} now and brings Rs {c1:,} after one year and Rs {c2:,} after two. At {r}%, what is the NPV?",
               f"একটা যন্ত্রের দাম এখন Rs {c0:,}, এক বছর পরে Rs {c1:,} আর দুই বছর পরে Rs {c2:,} আনে। {r}% হারে নিট বর্তমান মূল্য কত?", v,
               f"NPV = -{c0:,} + {c1:,}/{1 + r / 100:g} + {c2:,}/{1 + r / 100:g}² = Rs {_f(_c(v))}.",
               f"নিট বর্তমান মূল্য = -{c0:,} + {c1:,}/{1 + r / 100:g} + {c2:,}/{1 + r / 100:g}² = Rs {_f(_c(v))}।",
               (c1 + c2 - c0, v * 2, v + c0 / 10))


# ---------------------------------------------------------------- valuation and cost of capital
def gordon(d1, k, g):
    p = d1 / ((k - g) / 100)
    return _rs(f"A share will pay a dividend of Rs {d1} next year, growing at {g}% a year. Investors want {k}%. What is the share worth?",
               f"একটা শেয়ার আগামী বছর Rs {d1} লভ্যাংশ দেবে, যা বছরে {g}% বাড়বে। বিনিয়োগকারীরা {k}% চান। শেয়ারের মূল্য কত?", p,
               f"Gordon growth model: P = D₁ ÷ (k - g) = {d1} ÷ {(k - g) / 100:g} = Rs {_f(_c(p))}.",
               f"গর্ডন বৃদ্ধি মডেল: P = D₁ ÷ (k - g) = {d1} ÷ {(k - g) / 100:g} = Rs {_f(_c(p))}।",
               (d1 / (k / 100), d1 / ((k + g) / 100), p * 1.5))


def capm(rf, beta, rm):
    r = rf + beta * (rm - rf)
    return _n(f"The risk-free rate is {rf}%, the market return is {rm}% and a share's beta is {beta:g}. What return does CAPM require?",
              f"ঝুঁকিমুক্ত হার {rf}%, বাজারের আয় {rm}% আর একটা শেয়ারের বিটা {beta:g}। সিএপিএম অনুযায়ী প্রত্যাশিত আয় কত?", r,
              f"r = rf + β(rm - rf) = {rf} + {beta:g} x {rm - rf} = {_f(_c(r))}%.",
              f"প্রত্যাশিত আয় = rf + β(rm - rf) = {rf} + {beta:g} x {rm - rf} = {_f(_c(r))}%।",
              (rm * beta, rf + rm * beta, r + 2), "%")


def wacc(e, d, re, rd, t):
    v = e + d
    w = e / v * re + d / v * rd * (1 - t / 100)
    return _n(f"A firm has Rs {e} crore of equity costing {re}% and Rs {d} crore of debt at {rd}%; the tax rate is {t}%. What is its WACC?",
              f"একটা সংস্থার {re}% খরচের Rs {e} কোটি ইক্যুইটি আর {rd}% সুদের Rs {d} কোটি ঋণ আছে; করের হার {t}%। এর ভারযুক্ত গড় মূলধন-খরচ কত?", w,
              f"WACC = {e}/{v} x {re} + {d}/{v} x {rd} x (1 - {t / 100:g}) = {_f(_c(w))}%.",
              f"ভারযুক্ত গড় খরচ = {e}/{v} x {re} + {d}/{v} x {rd} x (1 - {t / 100:g}) = {_f(_c(w))}%।",
              (e / v * re + d / v * rd, (re + rd) / 2, w + 1.5), "%")


def after_tax_debt(rd, t):
    r = rd * (1 - t / 100)
    return _n(f"A company borrows at {rd}% and pays tax at {t}%. What is its after-tax cost of debt?",
              f"একটা কোম্পানি {rd}% সুদে ধার করে আর {t}% কর দেয়। করোত্তর ঋণ-খরচ কত?", r,
              f"Interest is tax-deductible: {rd} x (1 - {t / 100:g}) = {_f(_c(r))}%.",
              f"সুদ কর থেকে বাদ যায়: {rd} x (1 - {t / 100:g}) = {_f(_c(r))}%।",
              (rd, rd * t / 100, r + 1), "%")


def current_yield(coupon, price):
    y = coupon / price * 100
    return _n(f"A bond paying Rs {coupon} a year in coupons trades at Rs {price:,}. What is its current yield?",
              f"বছরে Rs {coupon} কুপন দেওয়া একটা বন্ডের বাজারদর Rs {price:,}। এর চলতি আয়-হার কত?", y,
              f"Current yield = annual coupon ÷ price = {coupon} ÷ {price:,} = {_f(_c(y))}%.",
              f"চলতি আয়-হার = বার্ষিক কুপন ÷ দাম = {coupon} ÷ {price:,} = {_f(_c(y))}%।",
              (coupon / 10, coupon / 1000 * 100, y + 1), "%")


def bond_price(face, c, r, n):
    p = sum(face * c / 100 / (1 + r / 100) ** t for t in range(1, n + 1)) + face / (1 + r / 100) ** n
    return _rs(f"A {n}-year bond of face value Rs {face:,} pays a {c}% annual coupon. If the market yield is {r}%, what is its price?",
               f"Rs {face:,} অভিহিত মূল্যের {n} বছরের একটা বন্ড বছরে {c}% কুপন দেয়। বাজারের আয়-হার {r}% হলে এর দাম কত?", p,
               f"Discount each coupon and the face value at {r}%: Rs {_f(_c(p))} - {'below' if r > c else 'above'} par because the yield is {'above' if r > c else 'below'} the coupon.",
               f"প্রতিটি কুপন আর অভিহিত মূল্য {r}%-এ বাট্টা করো: Rs {_f(_c(p))} - আয়-হার কুপনের {'বেশি' if r > c else 'কম'} বলে দাম অভিহিত মূল্যের {'কম' if r > c else 'বেশি'}।",
               (face, face * (1 + (c - r) / 100), p * 1.1))


# ---------------------------------------------------------------- ratios and leverage
def dol(contrib, ebit):
    v = contrib / ebit
    return _n(f"A company's contribution is Rs {contrib} lakh and its operating profit (EBIT) is Rs {ebit} lakh. What is its degree of operating leverage?",
              f"একটা কোম্পানির অবদান Rs {contrib} লাখ আর পরিচালন মুনাফা (ইবিআইটি) Rs {ebit} লাখ। এর পরিচালন লিভারেজের মাত্রা কত?", v,
              f"DOL = contribution ÷ EBIT = {contrib} ÷ {ebit} = {_f(_c(v))}: a 1% rise in sales lifts EBIT by {_f(_c(v))}%.",
              f"পরিচালন লিভারেজ = অবদান ÷ ইবিআইটি = {contrib} ÷ {ebit} = {_f(_c(v))}: বিক্রি 1% বাড়লে ইবিআইটি {_f(_c(v))}% বাড়ে।",
              (ebit / contrib, contrib - ebit, v + 1))


def dfl(ebit, interest):
    v = ebit / (ebit - interest)
    return _n(f"A firm has EBIT of Rs {ebit} lakh and interest of Rs {interest} lakh. What is its degree of financial leverage?",
              f"একটা সংস্থার ইবিআইটি Rs {ebit} লাখ আর সুদ Rs {interest} লাখ। এর আর্থিক লিভারেজের মাত্রা কত?", v,
              f"DFL = EBIT ÷ (EBIT - interest) = {ebit} ÷ {ebit - interest} = {_f(_c(v))}.",
              f"আর্থিক লিভারেজ = ইবিআইটি ÷ (ইবিআইটি - সুদ) = {ebit} ÷ {ebit - interest} = {_f(_c(v))}।",
              (interest / ebit + 1, ebit / interest, v + 1))


def dupont(margin, turnover, mult):
    r = margin * turnover * mult
    return _n(f"A company has a net profit margin of {margin}%, asset turnover of {turnover:g} and an equity multiplier of {mult:g}. What is its return on equity?",
              f"একটা কোম্পানির নিট মুনাফা-হার {margin}%, সম্পদ-আবর্তন {turnover:g} আর ইক্যুইটি গুণক {mult:g}। ইক্যুইটির উপর আয় কত?", r,
              f"DuPont: ROE = margin x turnover x multiplier = {margin} x {turnover:g} x {mult:g} = {_f(_c(r))}%.",
              f"ডুপন্ট: ইক্যুইটির আয় = মুনাফা-হার x আবর্তন x গুণক = {margin} x {turnover:g} x {mult:g} = {_f(_c(r))}%।",
              (margin * turnover, margin + turnover + mult, r / 2), "%")


def quick_ratio(ca, inv, cl):
    q = (ca - inv) / cl
    return _n(f"A firm has current assets of Rs {ca} lakh (including inventory of Rs {inv} lakh) and current liabilities of Rs {cl} lakh. What is its quick ratio?",
              f"একটা সংস্থার চলতি সম্পদ Rs {ca} লাখ (মজুত Rs {inv} লাখ সহ) আর চলতি দায় Rs {cl} লাখ। এর দ্রুত অনুপাত কত?", q,
              f"Quick ratio = (current assets - inventory) ÷ current liabilities = {ca - inv} ÷ {cl} = {_f(_c(q))}.",
              f"দ্রুত অনুপাত = (চলতি সম্পদ - মজুত) ÷ চলতি দায় = {ca - inv} ÷ {cl} = {_f(_c(q))}।",
              (ca / cl, inv / cl, q + 0.5))


def inventory_days(turnover):
    d = 365 / turnover
    return _n(f"A cement dealer's inventory turns over {turnover:g} times a year. On average, how many days does stock stay in the warehouse?",
              f"একজন সিমেন্ট-বিক্রেতার মজুত বছরে {turnover:g} বার আবর্তিত হয়। গড়ে মাল কত দিন গুদামে থাকে?", d,
              f"Days in inventory = 365 ÷ turnover = 365 ÷ {turnover:g} = {_f(_c(d))} days.",
              f"মজুতের দিন = 365 ÷ আবর্তন = 365 ÷ {turnover:g} = {_f(_c(d))} দিন।",
              (turnover * 30, 365 / turnover / 2, d + 10), " days", " দিন")


def pe_price(eps, pe):
    p = eps * pe
    return _rs(f"A company earns Rs {eps:g} per share and similar firms trade at a P/E ratio of {pe}. What price does that suggest?",
               f"একটা কোম্পানির শেয়ারপ্রতি আয় Rs {eps:g}, আর একই রকম সংস্থাগুলোর দাম-আয় অনুপাত {pe}। এতে কী দাম বোঝায়?", p,
               f"Price = EPS x P/E = {eps:g} x {pe} = Rs {_f(_c(p))}.",
               f"দাম = শেয়ারপ্রতি আয় x দাম-আয় অনুপাত = {eps:g} x {pe} = Rs {_f(_c(p))}।",
               (eps + pe, p / 2, eps * pe * 1.5))


def breakeven(fc, p, vc):
    q = fc / (p - vc)
    return _n(f"A precast-block plant has fixed costs of Rs {fc:,} a month, sells blocks at Rs {p} and spends Rs {vc} on each. How many blocks a month must it sell to break even?",
              f"একটা প্রিকাস্ট-ব্লক কারখানার মাসিক স্থির খরচ Rs {fc:,}, প্রতিটি ব্লক Rs {p}-এ বেচে আর প্রতিটিতে Rs {vc} খরচ করে। লাভ-ক্ষতিহীন হতে মাসে কয়টি ব্লক বেচতে হবে?", q,
              f"Break-even = fixed cost ÷ contribution per unit = {fc:,} ÷ ({p} - {vc}) = {_f(_c(q))} blocks.",
              f"সমচ্ছেদ = স্থির খরচ ÷ এককপ্রতি অবদান = {fc:,} ÷ ({p} - {vc}) = {_f(_c(q))}টি ব্লক।",
              (fc / p, fc / vc, q * 1.5))


def margin_safety(actual, be):
    m = (actual - be) / actual * 100
    return _n(f"A firm sells {actual:,} units a month and breaks even at {be:,} units. What is its margin of safety?",
              f"একটা সংস্থা মাসে {actual:,} একক বেচে আর {be:,} এককে লাভ-ক্ষতিহীন হয়। এর নিরাপত্তা-প্রান্ত কত?", m,
              f"(actual - break-even) ÷ actual = {actual - be:,} ÷ {actual:,} = {_f(_c(m))}%: sales can fall this much before losses start.",
              f"(প্রকৃত - সমচ্ছেদ) ÷ প্রকৃত = {actual - be:,} ÷ {actual:,} = {_f(_c(m))}%: বিক্রি এতটা কমলে তবে লোকসান শুরু।",
              ((actual - be) / be * 100, be / actual * 100, m / 2), "%")


# ---------------------------------------------------------------- portfolios, derivatives, money
def portfolio_return(w, r1, r2):
    r = w / 100 * r1 + (1 - w / 100) * r2
    return _n(f"A portfolio holds {w}% in a fund expected to earn {r1}% and the rest in one expected to earn {r2}%. What is its expected return?",
              f"একটা পোর্টফোলিওর {w}% এমন তহবিলে যার প্রত্যাশিত আয় {r1}%, বাকিটা এমন তহবিলে যার প্রত্যাশিত আয় {r2}%। প্রত্যাশিত আয় কত?", r,
              f"Weighted average: {w / 100:g} x {r1} + {1 - w / 100:g} x {r2} = {_f(_c(r))}%.",
              f"ভারযুক্ত গড়: {w / 100:g} x {r1} + {1 - w / 100:g} x {r2} = {_f(_c(r))}%।",
              ((r1 + r2) / 2, r1 * w / 100, r + 2), "%")


def portfolio_sd(w, s1, s2):
    s = math.sqrt((w / 100 * s1) ** 2 + ((1 - w / 100) * s2) ** 2)
    return _n(f"Two uncorrelated assets have standard deviations of {s1}% and {s2}%. What is the standard deviation of a portfolio with {w}% in the first?",
              f"দুটো সম্পর্কহীন সম্পদের পরিমিত ব্যবধান {s1}% আর {s2}%। প্রথমটায় {w}% রাখা পোর্টফোলিওর পরিমিত ব্যবধান কত?", s,
              f"With zero correlation σp = √(w₁²σ₁² + w₂²σ₂²) = {_f(_c(s))}% - lower than either asset alone: diversification.",
              f"সহগমন শূন্য হলে σp = √(w₁²σ₁² + w₂²σ₂²) = {_f(_c(s))}% - যেকোনো একটার চেয়ে কম: বৈচিত্র্যকরণের সুফল।",
              (w / 100 * s1 + (1 - w / 100) * s2, (s1 + s2) / 2, s + 3), "%")


def sharpe(rp, rf, sd):
    s = (rp - rf) / sd
    return _n(f"A fund returned {rp}% with a standard deviation of {sd}% while the risk-free rate was {rf}%. What is its Sharpe ratio?",
              f"একটা তহবিল {sd}% পরিমিত ব্যবধানে {rp}% আয় দিয়েছে, আর ঝুঁকিমুক্ত হার ছিল {rf}%। এর শার্প অনুপাত কত?", s,
              f"Sharpe = (Rp - Rf) ÷ σ = ({rp} - {rf}) ÷ {sd} = {_f(_c(s))}: excess return per unit of risk.",
              f"শার্প = (Rp - Rf) ÷ σ = ({rp} - {rf}) ÷ {sd} = {_f(_c(s))}: ঝুঁকির এককপ্রতি বাড়তি আয়।",
              (rp / sd, (rp + rf) / sd, s + 0.5))


def put_call(s, k, r, c):
    p = c - s + k / (1 + r / 100)
    return _rs(f"A share trades at Rs {s}; a one-year call with strike Rs {k} costs Rs {c} and the interest rate is {r}%. By put-call parity, what should the matching put cost?",
               f"একটা শেয়ারের দাম Rs {s}; Rs {k} স্ট্রাইকের এক বছরের কল অপশনের দাম Rs {c}, সুদের হার {r}%। পুট-কল সমতা অনুযায়ী মিলিয়ে নেওয়া পুটের দাম কত হওয়া উচিত?", p,
               f"P = C - S + K ÷ (1 + r) = {c} - {s} + {k} ÷ {1 + r / 100:g} = Rs {_f(_c(p))}.",
               f"P = C - S + K ÷ (1 + r) = {c} - {s} + {k} ÷ {1 + r / 100:g} = Rs {_f(_c(p))}।",
               (c, c - s + k, p + 3))


def call_profit(s, k, prem):
    v = max(s - k, 0) - prem
    return _rs(f"An investor buys a call option with strike Rs {k} for a premium of Rs {prem}. At expiry the share is at Rs {s}. What is the profit per share?",
               f"একজন বিনিয়োগকারী Rs {prem} প্রিমিয়ামে Rs {k} স্ট্রাইকের একটা কল অপশন কেনেন। মেয়াদশেষে শেয়ারের দাম Rs {s}। শেয়ারপ্রতি মুনাফা কত?", v,
               f"Payoff = max(S - K, 0) = {max(s - k, 0)}; profit = payoff - premium = Rs {_f(_c(v))}.",
               f"প্রাপ্তি = max(S - K, 0) = {max(s - k, 0)}; মুনাফা = প্রাপ্তি - প্রিমিয়াম = Rs {_f(_c(v))}।",
               (s - k, s - k + prem, prem))


def fisher(n, i):
    r = ((1 + n / 100) / (1 + i / 100) - 1) * 100
    return _n(f"A fixed deposit pays {n}% while inflation is {i}%. What is the exact real rate of return?",
              f"একটা স্থায়ী আমানত {n}% দেয়, মুদ্রাস্ফীতি {i}%। প্রকৃত আয়-হার ঠিক কত?", r,
              f"(1 + {n / 100:g}) ÷ (1 + {i / 100:g}) - 1 = {_f(_c(r))}% - a little below the simple difference {n - i}%.",
              f"(1 + {n / 100:g}) ÷ (1 + {i / 100:g}) - 1 = {_f(_c(r))}% - সরল পার্থক্য {n - i}%-এর একটু কম।",
              (n - i + 0.5, n + i, n / i), "%")


def forward_fx(spot, i_d, i_f):
    fwd = spot * (1 + i_d / 100) / (1 + i_f / 100)
    return _rs(f"The rupee-dollar spot rate is Rs {spot} per $. Rupee interest is {i_d}% and dollar interest is {i_f}%. What should the one-year forward rate be (Rs per $)?",
               f"রুপি-ডলারের তাৎক্ষণিক হার ডলারপ্রতি Rs {spot}। রুপির সুদ {i_d}% আর ডলারের সুদ {i_f}%। এক বছরের অগ্রিম হার (ডলারপ্রতি Rs) কত হওয়া উচিত?", fwd,
               f"Interest rate parity: F = S x (1 + i_INR) ÷ (1 + i_USD) = {spot} x {1 + i_d / 100:g} ÷ {1 + i_f / 100:g} = Rs {_f(_c(fwd))}.",
               f"সুদ-হার সমতা: F = S x (1 + রুপির সুদ) ÷ (1 + ডলারের সুদ) = {spot} x {1 + i_d / 100:g} ÷ {1 + i_f / 100:g} = Rs {_f(_c(fwd))}।",
               (spot, spot * (1 + i_f / 100) / (1 + i_d / 100), spot + i_d - i_f + 1))


def money_multiplier(crr):
    m = 100 / crr
    return _n(f"If banks must keep {crr}% of deposits as reserves and lend all the rest, what is the maximum money multiplier?",
              f"ব্যাংককে আমানতের {crr}% সংরক্ষিত রাখতে হলে আর বাকি সব ধার দিলে সর্বোচ্চ অর্থ-গুণক কত?", m,
              f"Money multiplier = 1 ÷ reserve ratio = 1 ÷ {crr / 100:g} = {_f(_c(m))}.",
              f"অর্থ-গুণক = 1 ÷ সংরক্ষণ-অনুপাত = 1 ÷ {crr / 100:g} = {_f(_c(m))}।",
              (crr, 100 - crr, m / 2))


NUMERIC = [
    ear(12, 12, "monthly", "মাসিক"), ear(10, 4, "quarterly", "ত্রৈমাসিক"), ear(8, 2, "half-yearly", "ষাণ্মাসিক"),
    ear(18, 12, "monthly", "মাসিক"), continuous(10), continuous(6), continuous(12),
    fv(10000, 10, 3), fv(50000, 8, 5), fv(25000, 12, 4), pv(12100, 10, 2), pv(100000, 8, 5), pv(50000, 12, 3),
    rule72(8), rule72(6), rule72(9), rule72(4),
    fv_annuity(1000, 10, 3), fv_annuity(5000, 8, 10), fv_annuity(12000, 12, 5),
    pv_annuity(10000, 10, 2), pv_annuity(20000, 8, 5), pv_annuity(50000, 12, 10),
    annuity_due(10000, 10, 3), annuity_due(25000, 8, 5),
    perpetuity(5000, 8), perpetuity(12000, 6), perpetuity(1500, 5),
    growing_perp(2000, 10, 4), growing_perp(5000, 12, 7), growing_perp(800, 9, 5),
    emi(100000, 12, 12), emi(500000, 9, 60), emi(2500000, 8.5, 240),
    first_interest(3000000, 9), first_interest(1200000, 8),
    sinking(500000, 10, 5), sinking(2000000, 8, 10),
    syd(110000, 10000, 4), syd(500000, 50000, 5), ddb(200000, 5), ddb(90000, 4),
    capitalised(2000000, 50000, 8), capitalised(5000000, 100000, 10),
    npv2(100, 60, 60, 10), npv2(1000, 600, 700, 12), npv2(500, 200, 400, 8),
    gordon(5, 12, 7), gordon(8, 14, 6), gordon(3, 10, 5),
    capm(6, 1.2, 12), capm(7, 0.8, 13), capm(5, 1.5, 11),
    wacc(60, 40, 15, 10, 30), wacc(70, 30, 14, 9, 25), wacc(50, 50, 16, 8, 30),
    after_tax_debt(10, 30), after_tax_debt(12, 25),
    current_yield(80, 950), current_yield(70, 1050), current_yield(90, 1200),
    bond_price(1000, 8, 10, 2), bond_price(1000, 10, 8, 2), bond_price(1000, 6, 9, 3),
    dol(500, 200), dol(900, 300), dfl(200, 50), dfl(400, 160),
    dupont(5, 2, 1.5), dupont(8, 1.2, 2), dupont(12, 0.8, 2.5),
    quick_ratio(500, 200, 250), quick_ratio(800, 300, 400),
    inventory_days(8), inventory_days(12), pe_price(25, 18), pe_price(42.5, 22),
    breakeven(300000, 50, 30), breakeven(450000, 120, 75),
    margin_safety(10000, 8000), margin_safety(25000, 15000),
    portfolio_return(60, 12, 7), portfolio_return(30, 15, 8),
    portfolio_sd(50, 20, 20), portfolio_sd(60, 15, 25),
    sharpe(14, 6, 16), sharpe(11, 5, 10),
    put_call(100, 100, 10, 12), put_call(250, 240, 8, 30),
    call_profit(130, 100, 12), call_profit(120, 100, 8), call_profit(160, 150, 6),
    fisher(10, 4), fisher(7, 5), fisher(12, 6),
    forward_fx(83, 7, 4), forward_fx(80, 6.5, 5),
    money_multiplier(4), money_multiplier(5), money_multiplier(10),
    ear(24, 12, "monthly", "মাসিক"), continuous(8), fv(20000, 9, 2), pv(20000, 10, 3), rule72(12),
    fv_annuity(2000, 6, 4), pv_annuity(15000, 9, 4), annuity_due(5000, 12, 4), perpetuity(10000, 10),
    growing_perp(1200, 11, 5), emi(300000, 10, 36), first_interest(5000000, 8.5), sinking(800000, 12, 6),
    syd(65000, 5000, 3), ddb(150000, 8), capitalised(800000, 20000, 5), npv2(2000, 1200, 1400, 10),
    gordon(12, 15, 9), capm(6.5, 0.9, 12.5), wacc(80, 20, 13, 9, 30), current_yield(60, 800),
    bond_price(1000, 9, 7, 2), dol(600, 150), dfl(300, 60), dupont(6, 1.5, 2), quick_ratio(1200, 500, 500),
    inventory_days(5), pe_price(18, 30), breakeven(600000, 200, 140), margin_safety(40000, 30000),
    portfolio_return(50, 10, 16), sharpe(16, 6, 20), put_call(500, 520, 10, 40), fisher(9, 3), pe_price(12, 25),
    forward_fx(84, 6, 3), money_multiplier(8),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    _q("For the same nominal rate, which compounding gives the largest amount after one year?", ["Continuous compounding", "Yearly compounding", "Half-yearly compounding", "Quarterly compounding"],
       "The more often interest is added, the more interest earns interest; continuous compounding is the limit.",
       "একই নামমাত্র হারে কোন চক্রবৃদ্ধি এক বছর পরে সবচেয়ে বেশি টাকা দেয়?", ["অবিরত চক্রবৃদ্ধি", "বার্ষিক চক্রবৃদ্ধি", "ষাণ্মাসিক চক্রবৃদ্ধি", "ত্রৈমাসিক চক্রবৃদ্ধি"],
       "যত ঘনঘন সুদ যোগ হয়, তত বেশি সুদের উপর সুদ; অবিরত চক্রবৃদ্ধি তার সীমা।"),
    _q("How does an annuity due differ from an ordinary annuity?", ["Payments come at the start of each period, so it is worth (1 + r) times more", "Payments come at the end of each period", "It has no fixed payments", "It never ends"],
       "Rent paid in advance is an annuity due; loan EMIs paid in arrears form an ordinary annuity.",
       "অগ্রিম বার্ষিকী সাধারণ বার্ষিকী থেকে কীভাবে আলাদা?", ["প্রতি পর্বের শুরুতে প্রদান, তাই মূল্য (1 + r) গুণ বেশি", "প্রতি পর্বের শেষে প্রদান", "এর কোনো নির্দিষ্ট প্রদান নেই", "এটা কখনো শেষ হয় না"],
       "অগ্রিম দেওয়া ভাড়া অগ্রিম বার্ষিকী; বকেয়া হিসেবে দেওয়া ঋণের কিস্তি সাধারণ বার্ষিকী।"),
    _q("Over the life of an equal-instalment loan, the interest portion of each EMI…", ["Falls, while the principal portion rises", "Rises steadily", "Stays exactly the same", "Is zero in the first year"],
       "Interest is charged on the outstanding balance, which shrinks with every payment.",
       "সমান কিস্তির ঋণের মেয়াদে প্রতিটি কিস্তির সুদ-অংশ…", ["কমে, আর আসল-অংশ বাড়ে", "ক্রমশ বাড়ে", "ঠিক একই থাকে", "প্রথম বছরে শূন্য"],
       "সুদ ধরা হয় বকেয়ার উপর, যা প্রতিটি প্রদানে কমে।"),
    _q("Why do companies like accelerated depreciation methods for tax purposes?", ["Larger early deductions defer tax, which is worth more today", "They increase total depreciation over the asset's life", "They raise reported profit early on", "They avoid all tax"],
       "Total depreciation is the same, but tax saved sooner has a higher present value.",
       "কোম্পানিগুলো করের জন্য ত্বরিত অবচয় পদ্ধতি পছন্দ করে কেন?", ["শুরুতে বড় ছাড়ে কর পিছিয়ে যায়, যার মূল্য আজ বেশি", "সম্পদের আয়ুতে মোট অবচয় বাড়ায়", "শুরুতে দেখানো মুনাফা বাড়ায়", "সব কর এড়ানো যায়"],
       "মোট অবচয় একই, কিন্তু আগে বাঁচানো করের বর্তমান মূল্য বেশি।"),
    _q("Depreciation itself is a non-cash expense. How does it still affect cash flow?", ["It lowers taxable profit and so lowers tax paid", "It is paid to the bank each year", "It increases sales", "It has no effect at all"],
       "The depreciation tax shield = depreciation x tax rate.",
       "অবচয় নিজে নগদহীন খরচ। তবু তা নগদ প্রবাহকে কীভাবে প্রভাবিত করে?", ["করযোগ্য মুনাফা কমিয়ে দেওয়া কর কমায়", "প্রতি বছর ব্যাংককে দেওয়া হয়", "বিক্রি বাড়ায়", "কোনো প্রভাবই নেই"],
       "অবচয়ের কর-আড়াল = অবচয় x করের হার।"),
    _q("When market interest rates rise, the prices of existing fixed-coupon bonds…", ["Fall", "Rise", "Stay the same", "Double"],
       "New bonds pay more, so old ones must get cheaper to offer the same yield.",
       "বাজারে সুদের হার বাড়লে চালু স্থির-কুপন বন্ডের দাম…", ["কমে", "বাড়ে", "একই থাকে", "দ্বিগুণ হয়"],
       "নতুন বন্ড বেশি দেয়, তাই একই আয় দিতে পুরোনোগুলোকে সস্তা হতে হয়।"),
    _q("A bond's duration measures…", ["How sensitive its price is to interest-rate changes", "Its remaining life only", "Its credit rating", "Its coupon rate"],
       "Longer duration means bigger price swings; zero-coupon bonds have duration equal to maturity.",
       "বন্ডের ডিউরেশন কী মাপে?", ["সুদের হারের পরিবর্তনে তার দাম কতটা সংবেদনশীল", "কেবল বাকি মেয়াদ", "তার ঋণ-মান", "তার কুপন হার"],
       "বেশি ডিউরেশন মানে দামে বড় ওঠানামা; শূন্য-কুপন বন্ডের ডিউরেশন মেয়াদের সমান।"),
    _q("What does an inverted yield curve (short-term rates above long-term rates) often signal?", ["An expected economic slowdown", "Rapid growth ahead", "Very low inflation forever", "Nothing at all"],
       "Markets expect rates to fall later, as they usually do in a downturn.",
       "উল্টানো আয়-রেখা (স্বল্পমেয়াদি হার দীর্ঘমেয়াদির চেয়ে বেশি) প্রায়ই কী ইঙ্গিত দেয়?", ["প্রত্যাশিত অর্থনৈতিক মন্দা", "সামনে দ্রুত বৃদ্ধি", "চিরকাল খুব কম মুদ্রাস্ফীতি", "কিছুই না"],
       "বাজার আশা করে পরে হার কমবে, যেমন মন্দায় সাধারণত হয়।"),
    _q("A share with a beta of 1.5 is expected to…", ["Move about 1.5 times as much as the market", "Move half as much as the market", "Never move", "Move opposite to the market"],
       "Beta measures systematic risk; the market itself has a beta of 1.",
       "1.5 বিটার একটা শেয়ার প্রত্যাশিতভাবে…", ["বাজারের প্রায় 1.5 গুণ ওঠানামা করে", "বাজারের অর্ধেক ওঠানামা করে", "কখনো নড়ে না", "বাজারের উল্টো দিকে চলে"],
       "বিটা ব্যবস্থাগত ঝুঁকি মাপে; বাজারের নিজের বিটা 1।"),
    _q("Which risk can be removed by holding a well-diversified portfolio?", ["Unsystematic (company-specific) risk", "Market-wide recession risk", "Interest-rate changes across the economy", "Inflation across the economy"],
       "A strike at one firm is offset by others; risks that hit the whole market remain.",
       "সুবৈচিত্র্যময় পোর্টফোলিও রাখলে কোন ঝুঁকি দূর করা যায়?", ["অব্যবস্থাগত (কোম্পানি-নির্দিষ্ট) ঝুঁকি", "বাজারব্যাপী মন্দার ঝুঁকি", "অর্থনীতিজুড়ে সুদের হারের পরিবর্তন", "অর্থনীতিজুড়ে মুদ্রাস্ফীতি"],
       "একটা সংস্থার ধর্মঘট অন্যদের দিয়ে পুষিয়ে যায়; পুরো বাজারকে আঘাত করা ঝুঁকি থেকে যায়।"),
    _q("The efficient frontier shows…", ["Portfolios with the highest return for each level of risk", "The cheapest shares", "Only risk-free assets", "The tax on each investment"],
       "Rational investors pick a point on it according to how much risk they can bear.",
       "দক্ষ সীমান্ত (এফিশিয়েন্ট ফ্রন্টিয়ার) কী দেখায়?", ["প্রতিটি ঝুঁকির স্তরে সর্বোচ্চ আয়ের পোর্টফোলিও", "সবচেয়ে সস্তা শেয়ার", "কেবল ঝুঁকিমুক্ত সম্পদ", "প্রতিটি বিনিয়োগের কর"],
       "যুক্তিবাদী বিনিয়োগকারী কতটা ঝুঁকি সইতে পারেন সেই অনুযায়ী এর উপর একটা বিন্দু বাছেন।"),
    _q("The semi-strong form of the efficient market hypothesis says that prices reflect…", ["All publicly available information", "Only past prices", "All information, even private", "Nothing - prices are random"],
       "Then neither chart reading nor studying published accounts can beat the market consistently.",
       "দক্ষ বাজার প্রকল্পের মাঝারি-দৃঢ় রূপ অনুযায়ী দাম প্রতিফলিত করে…", ["সব প্রকাশ্য তথ্য", "কেবল অতীতের দাম", "সব তথ্য, এমনকি গোপনও", "কিছুই না - দাম এলোমেলো"],
       "তাহলে চার্ট পড়া বা প্রকাশিত হিসাব দেখে নিয়মিত বাজারকে হারানো যায় না।"),
    _q("What is arbitrage?", ["A riskless profit from price differences for the same asset", "A long-term investment in shares", "Borrowing to buy property", "Insuring a portfolio"],
       "Buying cheap in one market and selling dear in another quickly removes the gap.",
       "আরবিট্রাজ কী?", ["একই সম্পদের দামের পার্থক্য থেকে ঝুঁকিহীন মুনাফা", "শেয়ারে দীর্ঘমেয়াদি বিনিয়োগ", "ধার করে সম্পত্তি কেনা", "পোর্টফোলিওর বিমা"],
       "এক বাজারে সস্তায় কিনে আরেক বাজারে বেশি দামে বেচলে পার্থক্য দ্রুত মুছে যায়।"),
    _q("The buyer of a put option has…", ["The right, but not the obligation, to sell at the strike price", "The obligation to buy", "The right to buy at the strike price", "No rights at all"],
       "A put gains when the price falls - like insurance on a share you own.",
       "একটা পুট অপশনের ক্রেতার থাকে…", ["স্ট্রাইক দামে বেচার অধিকার, বাধ্যবাধকতা নয়", "কেনার বাধ্যবাধকতা", "স্ট্রাইক দামে কেনার অধিকার", "কোনো অধিকারই নয়"],
       "দাম কমলে পুট লাভ দেয় - নিজের শেয়ারের বিমার মতো।"),
    _q("What is the intrinsic value of a call option with strike Rs 100 when the share is at Rs 90?", ["Zero (it is out of the money)", "Rs 10", "Rs 90", "Rs 100"],
       "Exercising would mean paying 100 for something worth 90; any premium left is pure time value.",
       "শেয়ার Rs 90-এ থাকলে Rs 100 স্ট্রাইকের কল অপশনের অন্তর্নিহিত মূল্য কত?", ["শূন্য (এটা আউট অফ দ্য মানি)", "Rs 10", "Rs 90", "Rs 100"],
       "প্রয়োগ করলে 90 টাকার জিনিসে 100 দিতে হবে; বাকি যা প্রিমিয়াম তা পুরোটাই সময়-মূল্য।"),
    _q("How do futures differ from forward contracts?", ["Futures are standardised, exchange-traded and settled daily (marked to market)", "Futures are private deals with no exchange", "Forwards are settled daily", "There is no difference"],
       "Daily settlement through a clearing house almost removes the risk that the other side defaults.",
       "ফিউচার্স ফরোয়ার্ড চুক্তি থেকে কীভাবে আলাদা?", ["ফিউচার্স মানক, এক্সচেঞ্জে লেনদেন হয় আর রোজ নিষ্পত্তি হয় (মার্কড টু মার্কেট)", "ফিউচার্স এক্সচেঞ্জ ছাড়া ব্যক্তিগত চুক্তি", "ফরোয়ার্ড রোজ নিষ্পত্তি হয়", "কোনো পার্থক্য নেই"],
       "ক্লিয়ারিং হাউসের মাধ্যমে রোজ নিষ্পত্তি অপর পক্ষের খেলাপির ঝুঁকি প্রায় দূর করে।"),
    _q("In an interest-rate swap, two parties typically exchange…", ["Fixed-rate payments for floating-rate payments", "Their loans' principal amounts", "Shares for bonds", "Currencies at a fixed rate only"],
       "A company with a floating loan can swap into fixed payments to make its costs predictable.",
       "সুদ-হার অদলবদলে (সোয়াপ) দুই পক্ষ সাধারণত বিনিময় করে…", ["স্থির-হারের প্রদান আর ভাসমান-হারের প্রদান", "তাদের ঋণের আসল অঙ্ক", "শেয়ারের বদলে বন্ড", "কেবল স্থির হারে মুদ্রা"],
       "ভাসমান ঋণের কোম্পানি সোয়াপ করে স্থির প্রদানে যেতে পারে, যাতে খরচ অনুমানযোগ্য হয়।"),
    _q("What is the repo rate in India?", ["The rate at which the RBI lends short-term money to banks", "The rate banks pay on savings accounts", "The income-tax rate", "The rate on government bonds only"],
       "Raising the repo rate makes borrowing dearer across the economy and helps control inflation.",
       "ভারতে রেপো রেট কী?", ["যে হারে রিজার্ভ ব্যাংক ব্যাংকগুলোকে স্বল্পমেয়াদি ধার দেয়", "সঞ্চয়ী অ্যাকাউন্টে ব্যাংক যে হার দেয়", "আয়করের হার", "কেবল সরকারি বন্ডের হার"],
       "রেপো রেট বাড়ালে অর্থনীতিজুড়ে ধার করা দামি হয় আর মুদ্রাস্ফীতি নিয়ন্ত্রণে আসে।"),
    _q("The Statutory Liquidity Ratio (SLR) requires Indian banks to…", ["Hold a share of deposits in safe liquid assets such as government securities", "Keep all deposits in cash", "Lend only to the government", "Pay a fixed dividend"],
       "The Cash Reserve Ratio (CRR) is the part kept as cash with the RBI itself.",
       "বিধিবদ্ধ তারল্য অনুপাত (এসএলআর) ভারতীয় ব্যাংককে কী করতে বলে?", ["আমানতের একটা অংশ সরকারি সিকিউরিটির মতো নিরাপদ তরল সম্পদে রাখতে", "সব আমানত নগদে রাখতে", "কেবল সরকারকে ধার দিতে", "নির্দিষ্ট লভ্যাংশ দিতে"],
       "নগদ সংরক্ষণ অনুপাত (সিআরআর) হলো রিজার্ভ ব্যাংকের কাছে নগদে রাখা অংশ।"),
    _q("An IPO is…", ["A company's first sale of shares to the public", "A loan from a bank", "A government tax", "A dividend payment"],
       "After listing, the shares trade between investors in the secondary market.",
       "আইপিও কী?", ["জনসাধারণের কাছে কোম্পানির প্রথম শেয়ার বিক্রি", "ব্যাংকের ঋণ", "সরকারি কর", "লভ্যাংশ প্রদান"],
       "তালিকাভুক্তির পর শেয়ারগুলো গৌণ বাজারে বিনিয়োগকারীদের মধ্যে কেনাবেচা হয়।"),
    _q("What is the NAV of a mutual fund?", ["The market value of its assets minus liabilities, per unit", "The price set by SEBI", "The fund manager's salary", "The total number of investors"],
       "Units are bought and redeemed at the NAV, which is worked out every business day.",
       "মিউচুয়াল ফান্ডের নিট সম্পদ মূল্য (এনএভি) কী?", ["এককপ্রতি তার সম্পদের বাজারমূল্য বিয়োগ দায়", "সেবির ঠিক করা দাম", "তহবিল-পরিচালকের বেতন", "মোট বিনিয়োগকারীর সংখ্যা"],
       "একক কেনা আর ফেরত দেওয়া হয় নিট সম্পদ মূল্যে, যা প্রতি কাজের দিনে হিসাব হয়।"),
    _q("Why does investing a fixed sum every month (SIP) lower the average cost per unit?", ["The same rupees buy more units when prices are low", "Units are sold at a discount to SIP investors", "Prices never fall during an SIP", "The fund pays the tax"],
       "This 'rupee-cost averaging' makes the average purchase price below the average market price.",
       "প্রতি মাসে নির্দিষ্ট অঙ্ক বিনিয়োগ (এসআইপি) এককপ্রতি গড় খরচ কমায় কেন?", ["দাম কম থাকলে একই টাকায় বেশি একক কেনা যায়", "এসআইপি বিনিয়োগকারীরা ছাড়ে একক পান", "এসআইপি চলাকালীন দাম কখনো কমে না", "তহবিল কর দেয়"],
       "এই 'রুপি-খরচ গড়করণ' গড় ক্রয়মূল্যকে গড় বাজারদরের নিচে রাখে।"),
    _q("According to Modigliani and Miller (no taxes, perfect markets), a firm's value…", ["Does not depend on how it mixes debt and equity", "Rises with every rupee of debt", "Falls with any debt", "Depends only on its dividend"],
       "With corporate taxes, debt adds value through the tax shield - until distress costs take over.",
       "মোদিগ্লিয়ানি আর মিলারের মতে (কর নেই, নিখুঁত বাজার) একটা সংস্থার মূল্য…", ["ঋণ আর ইক্যুইটি কীভাবে মেশানো হয় তার উপর নির্ভর করে না", "প্রতিটি টাকার ঋণে বাড়ে", "যেকোনো ঋণে কমে", "কেবল তার লভ্যাংশের উপর নির্ভর করে"],
       "কোম্পানি-কর থাকলে কর-আড়ালের জন্য ঋণ মূল্য বাড়ায় - যতক্ষণ না আর্থিক দুর্দশার খরচ ছাপিয়ে যায়।"),
    _q("Free cash flow to the firm is roughly…", ["Operating cash flow minus capital spending", "Net profit plus dividends", "Sales minus tax", "Total assets minus liabilities"],
       "It is the cash available to all investors after the business keeps its assets running and growing.",
       "সংস্থার মুক্ত নগদ প্রবাহ মোটামুটি…", ["পরিচালন নগদ প্রবাহ বিয়োগ মূলধনী ব্যয়", "নিট মুনাফা যোগ লভ্যাংশ", "বিক্রি বিয়োগ কর", "মোট সম্পদ বিয়োগ দায়"],
       "ব্যবসা নিজের সম্পদ চালু রাখার আর বাড়ানোর পরে সব বিনিয়োগকারীর জন্য যে নগদ থাকে।"),
    _q("EBITDA stands for earnings before…", ["Interest, tax, depreciation and amortisation", "Inventory, tax, debt and assets", "Investment, trade, dividends and accounts", "Interest only"],
       "It roughly measures cash profit from operations, before financing and accounting charges.",
       "ইবিআইটিডিএ মানে কোনগুলোর আগের আয়?", ["সুদ, কর, অবচয় আর পরিশোধ", "মজুত, কর, ঋণ আর সম্পদ", "বিনিয়োগ, বাণিজ্য, লভ্যাংশ আর হিসাব", "কেবল সুদ"],
       "এটা অর্থায়ন আর হিসাবি খরচের আগে পরিচালন থেকে মোটামুটি নগদ মুনাফা মাপে।"),
    _q("A company's cash conversion cycle shortens when it…", ["Collects from customers faster and pays suppliers later", "Holds more inventory", "Gives customers longer credit", "Pays suppliers earlier"],
       "Cycle = inventory days + receivable days - payable days; a shorter cycle needs less working capital.",
       "একটা কোম্পানির নগদ রূপান্তর চক্র ছোট হয় যখন সে…", ["গ্রাহকের কাছ থেকে দ্রুত আদায় করে আর সরবরাহকারীকে পরে দেয়", "বেশি মজুত রাখে", "গ্রাহককে বেশি ধার দেয়", "সরবরাহকারীকে আগে দেয়"],
       "চক্র = মজুতের দিন + প্রাপ্যের দিন - প্রদেয়ের দিন; ছোট চক্রে কম চলতি মূলধন লাগে।"),
    _q("What is factoring?", ["Selling receivables to a finance company for cash now", "Buying raw materials in bulk", "Splitting a share into smaller ones", "Paying tax in advance"],
       "A contractor waiting 90 days for a government bill can get most of the money immediately, at a discount.",
       "ফ্যাক্টরিং কী?", ["প্রাপ্য টাকা একটা অর্থ-সংস্থাকে বেচে এখনই নগদ পাওয়া", "একসঙ্গে প্রচুর কাঁচামাল কেনা", "একটা শেয়ারকে ছোট ছোট ভাগ করা", "অগ্রিম কর দেওয়া"],
       "সরকারি বিলের জন্য 90 দিন অপেক্ষারত ঠিকাদার বাট্টায় বেশিরভাগ টাকা সঙ্গে সঙ্গে পেতে পারেন।"),
    _q("A letter of credit protects an exporter because…", ["A bank promises to pay once the shipping documents are presented", "The buyer pays in advance always", "The government insures all exports", "It fixes the exchange rate"],
       "The seller relies on the bank's credit rather than on an unknown foreign buyer.",
       "ঋণপত্র (লেটার অফ ক্রেডিট) রপ্তানিকারককে রক্ষা করে কারণ…", ["জাহাজীকরণের নথি দেখালেই একটা ব্যাংক টাকা দেওয়ার প্রতিশ্রুতি দেয়", "ক্রেতা সবসময় অগ্রিম দেয়", "সরকার সব রপ্তানির বিমা করে", "এটা বিনিময় হার স্থির করে"],
       "বিক্রেতা অচেনা বিদেশি ক্রেতার বদলে ব্যাংকের কৃতিত্বের উপর ভরসা করেন।"),
    _q("A credit rating of 'AAA' on a bond means…", ["The highest safety - the lowest chance of default", "The highest interest rate", "The bond cannot be sold", "It is a government tax bond"],
       "Lower ratings (BB and below are 'junk') must pay higher interest to attract buyers.",
       "বন্ডের 'এএএ' ঋণ-মান মানে…", ["সর্বোচ্চ নিরাপত্তা - খেলাপির সম্ভাবনা সবচেয়ে কম", "সর্বোচ্চ সুদের হার", "বন্ডটা বেচা যায় না", "এটা সরকারি কর-বন্ড"],
       "নিচু মানের বন্ডকে (বিবি আর তার নিচে 'জাঙ্ক') ক্রেতা টানতে বেশি সুদ দিতে হয়।"),
    _q("What does a company's book value per share measure?", ["Shareholders' equity on the balance sheet divided by the number of shares", "The share's market price", "Next year's dividend", "Total sales per share"],
       "A price-to-book ratio above 1 means investors value the business above its accounting net worth.",
       "কোম্পানির শেয়ারপ্রতি বই-মূল্য কী মাপে?", ["স্থিতিপত্রের শেয়ারহোল্ডারদের ইক্যুইটি ভাগ শেয়ারের সংখ্যা", "শেয়ারের বাজারদর", "আগামী বছরের লভ্যাংশ", "শেয়ারপ্রতি মোট বিক্রি"],
       "দাম-বই অনুপাত 1-এর বেশি মানে বিনিয়োগকারীরা ব্যবসাকে তার হিসাবি নিট মূল্যের বেশি দাম দেন।"),
    _q("A bonus issue of shares (1 free share for every 1 held)…", ["Doubles the number of shares but does not change the company's total value", "Doubles each shareholder's wealth", "Raises new cash for the company", "Halves the number of shares"],
       "Reserves are converted into share capital; the share price roughly halves.",
       "বোনাস শেয়ার (প্রতি 1টির জন্য 1টি বিনামূল্যে)…", ["শেয়ারের সংখ্যা দ্বিগুণ করে কিন্তু কোম্পানির মোট মূল্য বদলায় না", "প্রত্যেক শেয়ারহোল্ডারের সম্পদ দ্বিগুণ করে", "কোম্পানির জন্য নতুন নগদ তোলে", "শেয়ারের সংখ্যা অর্ধেক করে"],
       "সঞ্চিতি শেয়ার-মূলধনে রূপান্তরিত হয়; শেয়ারের দাম মোটামুটি অর্ধেক হয়।"),
    _q("A company buys back its own shares. What usually happens to earnings per share?", ["It rises, because profit is shared among fewer shares", "It falls", "It is unchanged", "It becomes zero"],
       "Buybacks return cash to shareholders, like a dividend but with different tax effects.",
       "একটা কোম্পানি নিজের শেয়ার ফেরত কেনে। শেয়ারপ্রতি আয়ের সাধারণত কী হয়?", ["বাড়ে, কারণ মুনাফা কম শেয়ারে ভাগ হয়", "কমে", "একই থাকে", "শূন্য হয়"],
       "শেয়ার ফেরত কেনা শেয়ারহোল্ডারদের নগদ ফেরত দেয়, লভ্যাংশের মতো কিন্তু ভিন্ন কর-প্রভাবে।"),
    _q("Fiscal deficit means…", ["The government's total spending exceeds its total receipts excluding borrowing", "Exports are less than imports", "The RBI prints too little money", "Banks have too few deposits"],
       "It shows how much the government must borrow in the year.",
       "রাজকোষ ঘাটতি মানে…", ["ধার বাদে সরকারের মোট আয়ের চেয়ে মোট ব্যয় বেশি", "রপ্তানি আমদানির চেয়ে কম", "রিজার্ভ ব্যাংক খুব কম টাকা ছাপায়", "ব্যাংকের আমানত খুব কম"],
       "এটা দেখায় বছরে সরকারকে কত ধার করতে হবে।"),
    _q("If the rupee depreciates against the dollar, an Indian firm importing steel will find that…", ["Its imports cost more in rupees", "Its imports cost less in rupees", "Nothing changes", "It no longer needs dollars"],
       "Exporters gain instead, because their dollar earnings convert into more rupees.",
       "রুপির দাম ডলারের তুলনায় কমলে ইস্পাত আমদানিকারী একটা ভারতীয় সংস্থা দেখবে…", ["রুপিতে তার আমদানির খরচ বেড়েছে", "রুপিতে তার আমদানির খরচ কমেছে", "কিছুই বদলায়নি", "তার আর ডলার লাগে না"],
       "রপ্তানিকারকেরা বরং লাভবান হন, কারণ তাঁদের ডলার-আয় বেশি রুপিতে রূপান্তরিত হয়।"),
    _q("Which is an example of a 'hedge' for an Indian company that must pay $1 million in six months?", ["Buying dollars forward today at a fixed rate", "Waiting and buying dollars later", "Selling all its rupees now for gold", "Borrowing more rupees"],
       "The forward locks the cost; the company gives up any gain if the rupee strengthens.",
       "ছয় মাস পরে $1 মিলিয়ন দিতে হবে এমন একটা ভারতীয় কোম্পানির জন্য কোনটা 'হেজ'-এর উদাহরণ?", ["আজই স্থির হারে অগ্রিম ডলার কেনা", "অপেক্ষা করে পরে ডলার কেনা", "এখনই সব রুপি দিয়ে সোনা কেনা", "আরও রুপি ধার করা"],
       "অগ্রিম চুক্তি খরচ বেঁধে দেয়; রুপি শক্তিশালী হলে কোম্পানি সেই লাভ ছেড়ে দেয়।"),
    _q("What is the main purpose of Ind AS / IFRS accounting standards?", ["To make financial statements comparable and transparent across companies", "To set income-tax rates", "To fix share prices", "To control inflation"],
       "Common rules let investors compare firms fairly, including foreign investors.",
       "ইন্ড এএস / আইএফআরএস হিসাবমানের প্রধান উদ্দেশ্য কী?", ["সংস্থাগুলোর আর্থিক বিবরণীকে তুলনীয় আর স্বচ্ছ করা", "আয়করের হার ঠিক করা", "শেয়ারের দাম স্থির করা", "মুদ্রাস্ফীতি নিয়ন্ত্রণ"],
       "একই নিয়ম বিনিয়োগকারীদের, বিদেশিদেরও, সংস্থাগুলোকে ন্যায্যভাবে তুলনা করতে দেয়।"),
    _q("In capital budgeting, mutually exclusive projects are…", ["Alternatives where choosing one rules out the others", "Projects that can all be done together", "Projects with no cash flows", "Projects funded only by debt"],
       "For example, a steel or a concrete design for the same bridge; pick the one with the higher NPV.",
       "মূলধন বাজেটিংয়ে পরস্পর-বর্জনশীল প্রকল্প হলো…", ["এমন বিকল্প যেখানে একটা বাছলে বাকিগুলো বাদ", "যেসব প্রকল্প একসঙ্গে করা যায়", "নগদ প্রবাহহীন প্রকল্প", "কেবল ঋণে অর্থায়িত প্রকল্প"],
       "যেমন একই সেতুর জন্য ইস্পাত বা কংক্রিটের নকশা; বেশি নিট বর্তমান মূল্যেরটা বাছো।"),
    _q("When should a project's cash flows be adjusted for inflation?", ["Always discount nominal cash flows at a nominal rate (or real at real) - never mix them", "Never", "Only for government projects", "Only in the first year"],
       "Mixing a nominal rate with real cash flows understates the project's value, and the reverse overstates it.",
       "কখন একটা প্রকল্পের নগদ প্রবাহ মুদ্রাস্ফীতির জন্য সমন্বয় করা উচিত?", ["সবসময় নামমাত্র প্রবাহ নামমাত্র হারে (বা প্রকৃত প্রবাহ প্রকৃত হারে) বাট্টা করো - কখনো মিশিও না", "কখনো নয়", "কেবল সরকারি প্রকল্পে", "কেবল প্রথম বছরে"],
       "প্রকৃত প্রবাহে নামমাত্র হার মেশালে প্রকল্পের মূল্য কম দেখায়, উল্টোটা বেশি দেখায়।"),
    _q("What does a high debt-to-equity ratio indicate?", ["The company relies heavily on borrowed money and carries more financial risk", "The company has no loans", "The company is very liquid", "The company pays high dividends"],
       "It magnifies returns in good years and losses in bad ones.",
       "উচ্চ ঋণ-ইক্যুইটি অনুপাত কী নির্দেশ করে?", ["কোম্পানি ধার করা টাকার উপর খুব নির্ভরশীল আর বেশি আর্থিক ঝুঁকি বয়", "কোম্পানির কোনো ঋণ নেই", "কোম্পানি খুব তরল", "কোম্পানি বেশি লভ্যাংশ দেয়"],
       "এটা ভালো বছরে আয় আর খারাপ বছরে ক্ষতি দুটোই বাড়িয়ে দেয়।"),
    _q("The interest coverage ratio (EBIT ÷ interest) of 1.2 suggests…", ["The firm barely earns enough to pay its interest", "The firm has no debt", "The firm is extremely safe", "The firm pays no tax"],
       "Lenders usually want 2-3 or more; below 1 means operating profit does not even cover interest.",
       "সুদ-আবরণ অনুপাত (ইবিআইটি ÷ সুদ) 1.2 হলে বোঝায়…", ["সংস্থা কোনোমতে সুদ দেওয়ার মতো আয় করে", "সংস্থার কোনো ঋণ নেই", "সংস্থা অত্যন্ত নিরাপদ", "সংস্থা কোনো কর দেয় না"],
       "ঋণদাতারা সাধারণত 2-3 বা তার বেশি চান; 1-এর নিচে মানে পরিচালন মুনাফা সুদও ঢাকে না।"),
    _q("Why might a profitable company still run out of cash?", ["Its money is tied up in unpaid customer bills and stock", "Profit always equals cash", "Depreciation drains cash", "Taxes are never due"],
       "Fast-growing contractors often fail this way: work is billed, but cash arrives months later.",
       "লাভজনক কোম্পানিরও নগদ ফুরিয়ে যেতে পারে কেন?", ["তার টাকা অনাদায়ী গ্রাহক-বিল আর মজুতে আটকে থাকে", "মুনাফা সবসময় নগদের সমান", "অবচয় নগদ শুষে নেয়", "কর কখনো দিতে হয় না"],
       "দ্রুত বাড়তে থাকা ঠিকাদার প্রায়ই এভাবে ব্যর্থ হন: কাজের বিল হয়, কিন্তু নগদ আসে মাস কয়েক পরে।"),
    _q("A 'stop-loss' order on a share…", ["Sells automatically if the price falls to a set level", "Buys more when the price falls", "Stops all trading in the share", "Guarantees a profit"],
       "It limits the loss on a position, though in a sudden crash it may fill below the set price.",
       "একটা শেয়ারে 'স্টপ-লস' অর্ডার…", ["দাম একটা নির্দিষ্ট স্তরে নামলে স্বয়ংক্রিয়ভাবে বেচে দেয়", "দাম কমলে আরও কেনে", "শেয়ারের সব লেনদেন বন্ধ করে", "মুনাফা নিশ্চিত করে"],
       "এটা অবস্থানের ক্ষতি সীমিত রাখে, যদিও আচমকা পতনে নির্দিষ্ট দামের নিচে বিক্রি হতে পারে।"),
    _q("Which is a feature of a zero-coupon bond?", ["It pays no interest but is sold at a deep discount to face value", "It pays monthly interest", "It has no maturity date", "It always trades above face value"],
       "The investor's return is the difference between the purchase price and the face value at maturity.",
       "শূন্য-কুপন বন্ডের বৈশিষ্ট্য কোনটা?", ["কোনো সুদ দেয় না কিন্তু অভিহিত মূল্যের অনেক কমে বিক্রি হয়", "মাসিক সুদ দেয়", "এর কোনো মেয়াদ নেই", "সবসময় অভিহিত মূল্যের বেশিতে কেনাবেচা হয়"],
       "বিনিয়োগকারীর আয় হলো ক্রয়মূল্য আর মেয়াদশেষে অভিহিত মূল্যের পার্থক্য।"),
    _q("What is the 'time value' part of an option's premium?", ["The extra paid for the chance the option gains value before expiry", "The option's intrinsic value", "The broker's commission", "The tax on the option"],
       "It shrinks as expiry approaches and is zero at expiry.",
       "অপশনের প্রিমিয়ামের 'সময়-মূল্য' অংশ কী?", ["মেয়াদশেষের আগে অপশনের মূল্য বাড়ার সম্ভাবনার জন্য দেওয়া বাড়তি অংশ", "অপশনের অন্তর্নিহিত মূল্য", "দালালের কমিশন", "অপশনের উপর কর"],
       "মেয়াদশেষ যত কাছে আসে এটা তত কমে, মেয়াদশেষে শূন্য।"),
    _q("Which statement about simple and compound interest over several years is true?", ["Compound interest is always more than simple interest at the same rate for more than one year", "Simple interest is always more", "They are always equal", "Compound interest is less after many years"],
       "From the second year compound interest also earns interest on earlier interest.",
       "কয়েক বছরে সরল আর চক্রবৃদ্ধি সুদ সম্পর্কে কোন কথাটা সত্য?", ["একই হারে এক বছরের বেশি হলে চক্রবৃদ্ধি সুদ সবসময় সরল সুদের চেয়ে বেশি", "সরল সুদ সবসময় বেশি", "দুটো সবসময় সমান", "অনেক বছর পরে চক্রবৃদ্ধি সুদ কম"],
       "দ্বিতীয় বছর থেকে চক্রবৃদ্ধি সুদ আগের সুদের উপরও সুদ পায়।"),
    _q("Which is the best measure of a firm's ability to pay its short-term bills without selling stock?", ["The quick (acid-test) ratio", "The debt-to-equity ratio", "The P/E ratio", "Return on equity"],
       "It leaves out inventory, which may be slow to turn into cash.",
       "মজুত না বেচে স্বল্পমেয়াদি বিল মেটানোর ক্ষমতার সবচেয়ে ভালো মাপ কোনটা?", ["দ্রুত (অ্যাসিড-টেস্ট) অনুপাত", "ঋণ-ইক্যুইটি অনুপাত", "দাম-আয় অনুপাত", "ইক্যুইটির উপর আয়"],
       "এতে মজুত বাদ থাকে, যা নগদে বদলাতে দেরি হতে পারে।"),
    _q("A company's shares trade at a very high P/E ratio. This usually means investors…", ["Expect strong future earnings growth", "Think the company will soon close", "Have no information", "Want only dividends"],
       "They pay many years of current earnings now, betting on growth; a high P/E can also mean the share is overpriced.",
       "একটা কোম্পানির শেয়ার খুব বেশি দাম-আয় অনুপাতে কেনাবেচা হয়। এর মানে সাধারণত বিনিয়োগকারীরা…", ["ভবিষ্যতে আয়ের জোরালো বৃদ্ধি আশা করেন", "মনে করেন কোম্পানি শিগগির বন্ধ হবে", "কোনো তথ্য জানেন না", "কেবল লভ্যাংশ চান"],
       "বৃদ্ধির আশায় এখনই অনেক বছরের বর্তমান আয় দাম দেন; বেশি অনুপাত শেয়ার অতিমূল্যায়িত হওয়াও বোঝাতে পারে।"),
    _q("Why does a business keep a cash budget?", ["To foresee shortfalls and arrange finance before bills fall due", "To calculate income tax", "To value its shares", "To set salaries"],
       "It lists expected cash receipts and payments month by month.",
       "একটা ব্যবসা নগদ বাজেট রাখে কেন?", ["ঘাটতি আগে দেখে, বিল দেওয়ার আগেই অর্থের ব্যবস্থা করতে", "আয়কর হিসাব করতে", "শেয়ারের মূল্য নির্ধারণ করতে", "বেতন ঠিক করতে"],
       "এতে মাসে মাসে প্রত্যাশিত নগদ প্রাপ্তি আর প্রদান তালিকাভুক্ত থাকে।"),
    _q("What is a 'callable' bond?", ["One the issuer can repay early, usually when interest rates fall", "One the investor can sell back at any time", "One that pays no coupon", "One issued by a government only"],
       "Investors demand a higher yield for the risk of losing a good coupon early.",
       "'কলযোগ্য' বন্ড কী?", ["যা ইস্যুকারী আগেভাগে শোধ করতে পারে, সাধারণত সুদের হার কমলে", "যা বিনিয়োগকারী যেকোনো সময় ফেরত বেচতে পারেন", "যা কোনো কুপন দেয় না", "যা কেবল সরকার ইস্যু করে"],
       "ভালো কুপন আগেভাগে হারানোর ঝুঁকির জন্য বিনিয়োগকারীরা বেশি আয়-হার চান।"),
    _q("A convertible debenture…", ["Can be exchanged for the company's shares on set terms", "Pays no interest ever", "Is always secured on land", "Cannot be traded"],
       "Because of the conversion option it usually carries a lower interest rate than a plain debenture.",
       "রূপান্তরযোগ্য ডিবেঞ্চার…", ["নির্দিষ্ট শর্তে কোম্পানির শেয়ারের সঙ্গে বদলানো যায়", "কখনো সুদ দেয় না", "সবসময় জমির বিপরীতে সুরক্ষিত", "কেনাবেচা করা যায় না"],
       "রূপান্তরের সুযোগের জন্য এতে সাধারণত সাধারণ ডিবেঞ্চারের চেয়ে কম সুদ থাকে।"),
    _q("What is venture capital?", ["Equity finance for young, high-risk companies with growth potential", "A government grant for farmers", "A bank overdraft", "A type of insurance"],
       "Investors accept many failures in return for a few large successes.",
       "ভেঞ্চার ক্যাপিটাল কী?", ["বৃদ্ধির সম্ভাবনাময়, উচ্চ-ঝুঁকির নতুন কোম্পানির জন্য ইক্যুইটি অর্থায়ন", "কৃষকদের জন্য সরকারি অনুদান", "ব্যাংক ওভারড্রাফট", "এক ধরনের বিমা"],
       "কয়েকটা বড় সাফল্যের বিনিময়ে বিনিয়োগকারীরা অনেক ব্যর্থতা মেনে নেন।"),
    _q("Which statement about the time value of money is correct?", ["A rupee today is worth more than a rupee promised in the future", "Money loses no value over time", "Future money is always worth more", "Interest rates do not matter"],
       "Money today can be invested to earn a return, and the future carries uncertainty and inflation.",
       "অর্থের সময়-মূল্য সম্পর্কে কোন বিবৃতি সঠিক?", ["আজকের এক টাকা ভবিষ্যতে প্রতিশ্রুত এক টাকার চেয়ে বেশি মূল্যবান", "সময়ের সঙ্গে টাকার মূল্য কমে না", "ভবিষ্যতের টাকা সবসময় বেশি মূল্যবান", "সুদের হার কোনো ব্যাপার নয়"],
       "আজকের টাকা বিনিয়োগ করে আয় করা যায়, আর ভবিষ্যতে অনিশ্চয়তা ও মুদ্রাস্ফীতি থাকে।"),
    _q("What does a 'stock split' of 1:5 do?", ["Each share becomes five shares at about one-fifth the price", "The company raises five times more cash", "Shareholders lose 80% of their wealth", "The dividend becomes five times larger"],
       "Total value is unchanged; a lower price can make the share easier for small investors to buy.",
       "1:5 'স্টক স্প্লিট' কী করে?", ["প্রতিটি শেয়ার প্রায় এক-পঞ্চমাংশ দামে পাঁচটা শেয়ার হয়", "কোম্পানি পাঁচ গুণ বেশি নগদ তোলে", "শেয়ারহোল্ডাররা সম্পদের 80% হারান", "লভ্যাংশ পাঁচ গুণ হয়"],
       "মোট মূল্য একই থাকে; কম দাম ছোট বিনিয়োগকারীদের কেনা সহজ করতে পারে।"),
    _q("An index such as the Nifty 50 measures…", ["The combined price movement of a basket of large listed companies", "The price of one company's share", "The RBI's interest rate", "The rupee-dollar exchange rate"],
       "It is weighted by free-float market value, so larger companies move it more.",
       "নিফটি 50-এর মতো সূচক কী মাপে?", ["তালিকাভুক্ত বড় কোম্পানিগুলোর একটা ঝুড়ির মিলিত দামের ওঠানামা", "একটা কোম্পানির শেয়ারের দাম", "রিজার্ভ ব্যাংকের সুদের হার", "রুপি-ডলার বিনিময় হার"],
       "এটা অবাধে কেনাবেচাযোগ্য বাজারমূল্য দিয়ে ভারযুক্ত, তাই বড় কোম্পানিগুলো একে বেশি নাড়ায়।"),
    _q("A company's 'working capital' is…", ["Current assets minus current liabilities", "Total assets", "Fixed assets minus loans", "Annual profit"],
       "It funds day-to-day operations such as stock, wages and customer credit.",
       "কোম্পানির 'চলতি মূলধন' হলো…", ["চলতি সম্পদ বিয়োগ চলতি দায়", "মোট সম্পদ", "স্থায়ী সম্পদ বিয়োগ ঋণ", "বার্ষিক মুনাফা"],
       "এটা মজুত, মজুরি আর গ্রাহককে দেওয়া ধারের মতো দৈনন্দিন কাজের অর্থ জোগায়।"),
    _q("Why do lenders ask for collateral?", ["To recover money by selling the pledged asset if the borrower defaults", "To pay the borrower's tax", "To reduce the loan amount to zero", "To fix the share price"],
       "Secured loans usually carry lower interest rates than unsecured ones.",
       "ঋণদাতারা জামানত চান কেন?", ["ঋণগ্রহীতা খেলাপি হলে বন্ধক রাখা সম্পদ বেচে টাকা আদায় করতে", "ঋণগ্রহীতার কর দিতে", "ঋণের অঙ্ক শূন্যে নামাতে", "শেয়ারের দাম স্থির করতে"],
       "সুরক্ষিত ঋণে সাধারণত অসুরক্ষিত ঋণের চেয়ে কম সুদ থাকে।"),
    _q("A non-performing asset (NPA) for an Indian bank is a loan on which…", ["Interest or principal has been overdue for more than 90 days", "The borrower paid early", "No interest was ever charged", "The government gave a guarantee"],
       "High NPAs force banks to set aside provisions, cutting their profits and lending.",
       "ভারতীয় ব্যাংকের অনুৎপাদক সম্পদ (এনপিএ) এমন ঋণ যার…", ["সুদ বা আসল 90 দিনের বেশি বকেয়া", "ঋণগ্রহীতা আগেভাগে শোধ করেছেন", "কখনো সুদ ধরা হয়নি", "সরকার জামিন দিয়েছে"],
       "বেশি অনুৎপাদক সম্পদ থাকলে ব্যাংককে সংস্থান রাখতে হয়, ফলে মুনাফা আর ঋণদান কমে।"),
    _q("The SEBI rule against insider trading exists to…", ["Keep the market fair by stopping trades on unpublished price-sensitive information", "Ban all share trading", "Fix share prices", "Collect income tax"],
       "Everyone should get important company news at the same time.",
       "অভ্যন্তরীণ লেনদেনের বিরুদ্ধে সেবির নিয়ম আছে যাতে…", ["অপ্রকাশিত দাম-সংবেদনশীল তথ্যে লেনদেন থামিয়ে বাজার ন্যায্য থাকে", "সব শেয়ার-লেনদেন নিষিদ্ধ হয়", "শেয়ারের দাম স্থির হয়", "আয়কর আদায় হয়"],
       "কোম্পানির গুরুত্বপূর্ণ খবর সবাই একই সময়ে পাক।"),
    _q("What does the 'margin of safety' tell a manager?", ["How far sales can fall before the business makes a loss", "The profit on each unit", "The tax rate", "The interest on loans"],
       "A larger margin of safety means the business can survive a bigger drop in demand.",
       "'নিরাপত্তা-প্রান্ত' একজন ম্যানেজারকে কী জানায়?", ["লোকসান শুরুর আগে বিক্রি কতটা কমতে পারে", "প্রতিটি এককের মুনাফা", "করের হার", "ঋণের সুদ"],
       "বড় নিরাপত্তা-প্রান্ত মানে চাহিদা বেশি কমলেও ব্যবসা টিকে থাকতে পারে।"),
    _q("When is a project accepted under the profitability index rule?", ["When the PI is greater than 1", "When the PI is less than 1", "When the PI is exactly 0", "Always"],
       "PI = present value of inflows ÷ initial cost; PI > 1 is the same as NPV > 0.",
       "লাভজনকতা সূচকের নিয়মে কখন একটা প্রকল্প গ্রহণ করা হয়?", ["সূচক 1-এর বেশি হলে", "সূচক 1-এর কম হলে", "সূচক ঠিক 0 হলে", "সবসময়"],
       "সূচক = আগত প্রবাহের বর্তমান মূল্য ÷ প্রাথমিক খরচ; সূচক > 1 মানে নিট বর্তমান মূল্য > 0।"),
    _q("A company pays out all its profit as dividends. What is its sustainable growth rate from retained earnings?", ["Zero", "Equal to its ROE", "Equal to the dividend yield", "Infinite"],
       "Growth from internal funds = retention ratio x ROE, and the retention ratio here is zero.",
       "একটা কোম্পানি সব মুনাফা লভ্যাংশ হিসেবে দিয়ে দেয়। সংরক্ষিত আয় থেকে এর টেকসই বৃদ্ধির হার কত?", ["শূন্য", "ইক্যুইটির উপর আয়ের সমান", "লভ্যাংশ আয়-হারের সমান", "অসীম"],
       "অভ্যন্তরীণ অর্থে বৃদ্ধি = সংরক্ষণ অনুপাত x ইক্যুইটির উপর আয়, আর এখানে সংরক্ষণ অনুপাত শূন্য।"),
    _q("Which financial statement shows a company's position on a single date?", ["The balance sheet", "The profit and loss statement", "The cash flow statement", "The budget"],
       "The profit and loss and cash flow statements cover a period, such as a year.",
       "কোন আর্থিক বিবরণী একটা নির্দিষ্ট তারিখে কোম্পানির অবস্থা দেখায়?", ["স্থিতিপত্র", "লাভ-ক্ষতির বিবরণী", "নগদ প্রবাহ বিবরণী", "বাজেট"],
       "লাভ-ক্ষতি আর নগদ প্রবাহ বিবরণী একটা সময়কাল, যেমন এক বছর, জুড়ে থাকে।"),
    _q("What is the main risk for someone who keeps all savings in a bank's savings account for 20 years?", ["Inflation may grow faster than the interest, cutting real value", "The bank charges for deposits", "The money doubles too fast", "Interest is taxed at 100%"],
       "Real return = nominal return - inflation (roughly); a negative real return shrinks purchasing power.",
       "20 বছর ধরে সব সঞ্চয় ব্যাংকের সঞ্চয়ী অ্যাকাউন্টে রাখলে প্রধান ঝুঁকি কী?", ["মুদ্রাস্ফীতি সুদের চেয়ে দ্রুত বেড়ে প্রকৃত মূল্য কমাতে পারে", "জমার জন্য ব্যাংক টাকা নেয়", "টাকা খুব দ্রুত দ্বিগুণ হয়", "সুদে 100% কর"],
       "প্রকৃত আয় = নামমাত্র আয় - মুদ্রাস্ফীতি (মোটামুটি); ঋণাত্মক প্রকৃত আয় ক্রয়ক্ষমতা কমায়।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
