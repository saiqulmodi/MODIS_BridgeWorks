"""IIT level - Finance (MBA / IIT-management depth): capital budgeting (IRR, MIRR, discounted
payback), fixed income (yield to maturity, duration, spot and forward rates, T-bills), working
capital (EOQ, reorder level, cash conversion cycle), capital structure (EBIT-EPS indifference,
leverage, Hamada beta, Modigliani-Miller with taxes), valuation (FCFF, EVA, two-stage dividends,
justified P/E, rights issues), derivatives (binomial pricing, put-call parity, straddles), risk
(VaR, Treynor, Jensen's alpha, correlated portfolios), international finance and Indian markets."""
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


def _pc(q_en, q_bn, r, ex_en, ex_bn, alts):
    return _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="%")


# ---------------------------------------------------------------- capital budgeting
def irr2(c0, c1, c2):
    x = (-c1 + math.sqrt(c1 * c1 + 4 * c2 * c0)) / (2 * c2)
    r = (1 / x - 1) * 100
    return _pc(f"A project costs Rs {c0:,} today and returns Rs {c1:,} after one year and Rs {c2:,} after two. What is its IRR?",
               f"একটা প্রকল্পে আজ Rs {c0:,} খরচ, এক বছর পরে Rs {c1:,} আর দুই বছর পরে Rs {c2:,} ফেরত। এর আইআরআর কত?", r,
               f"Solve {c0:,} = {c1:,}/(1 + r) + {c2:,}/(1 + r)² (a quadratic in 1/(1 + r)): r = {_f(_c(r))}%.",
               f"{c0:,} = {c1:,}/(1 + r) + {c2:,}/(1 + r)² সমাধান করো (1/(1 + r)-এ দ্বিঘাত): r = {_f(_c(r))}%।",
               ((c1 + c2 - c0) / c0 * 100, (c1 + c2 - c0) / c0 * 50, r + 5))


def mirr(c0, flows, reinvest):
    n = len(flows)
    fv = sum(cf * (1 + reinvest / 100) ** (n - 1 - t) for t, cf in enumerate(flows))
    r = ((fv / c0) ** (1 / n) - 1) * 100
    txt = ", ".join(f"Rs {cf:,}" for cf in flows)
    return _pc(f"A project costs Rs {c0:,} and returns {txt} over the next {n} years. If inflows are reinvested at {reinvest}%, what is its MIRR?",
               f"একটা প্রকল্পে Rs {c0:,} খরচ, পরের {n} বছরে ফেরত {txt}। প্রবাহ {reinvest}%-এ পুনর্বিনিয়োগ হলে এর এমআইআরআর কত?", r,
               f"Compound the inflows to year {n} at {reinvest}%: Rs {_f(_c(fv))}; MIRR = ({_f(_c(fv))} ÷ {c0:,})^(1/{n}) - 1 = {_f(_c(r))}%.",
               f"প্রবাহগুলোকে {reinvest}%-এ {n} বছর পর্যন্ত চক্রবৃদ্ধি করো: Rs {_f(_c(fv))}; এমআইআরআর = ({_f(_c(fv))} ÷ {c0:,})^(1/{n}) - 1 = {_f(_c(r))}%।",
               ((sum(flows) / c0 - 1) / n * 100, reinvest, r + 4))


def disc_payback(c0, cf, rate, years):
    cum, t = 0.0, 0
    pvs = [cf / (1 + rate / 100) ** k for k in range(1, years + 1)]
    for k, pv in enumerate(pvs, 1):
        if cum + pv >= c0:
            t = k - 1 + (c0 - cum) / pv
            break
        cum += pv
    return _n(f"A project costs Rs {c0:,} and brings Rs {cf:,} a year. At a {rate}% discount rate, what is its discounted payback period?",
              f"একটা প্রকল্পে Rs {c0:,} খরচ, প্রতি বছর Rs {cf:,} আয়। {rate}% বাট্টা হারে এর বাট্টাকৃত পরিশোধকাল কত?", t,
              f"Add the present values Rs {_f(_c(pvs[0]))}, Rs {_f(_c(pvs[1]))}, ... until they reach Rs {c0:,}: about {_f(_c(t))} years (simple payback: {_f(_c(c0 / cf))}).",
              f"বর্তমান মূল্য Rs {_f(_c(pvs[0]))}, Rs {_f(_c(pvs[1]))}, ... যোগ করো যতক্ষণ না Rs {c0:,} হয়: প্রায় {_f(_c(t))} বছর (সাধারণ পরিশোধকাল: {_f(_c(c0 / cf))})।",
              (c0 / cf, t + 1.5, t - 1 if t > 2 else t + 3), " years", " বছর")


# ---------------------------------------------------------------- fixed income
def ytm_approx(face, coupon, price, n):
    r = (coupon + (face - price) / n) / ((face + price) / 2) * 100
    return _pc(f"A {n}-year bond with face value Rs {face:,} pays Rs {coupon} a year and trades at Rs {price:,}. What is its approximate yield to maturity?",
               f"Rs {face:,} অভিহিত মূল্যের {n} বছরের একটা বন্ড বছরে Rs {coupon} দেয় আর Rs {price:,}-এ কেনাবেচা হয়। এর আনুমানিক পরিপক্বতা-আয় কত?", r,
               f"YTM ≈ [C + (F - P)/n] ÷ [(F + P)/2] = [{coupon} + {_f(_c((face - price) / n))}] ÷ {_f(_c((face + price) / 2))} = {_f(_c(r))}%.",
               f"পরিপক্বতা-আয় ≈ [C + (F - P)/n] ÷ [(F + P)/2] = [{coupon} + {_f(_c((face - price) / n))}] ÷ {_f(_c((face + price) / 2))} = {_f(_c(r))}%।",
               (coupon / price * 100, coupon / face * 100, r + 2))


def macaulay(face, c, y, n):
    flows = [face * c / 100] * (n - 1) + [face * c / 100 + face]
    pvs = [cf / (1 + y / 100) ** t for t, cf in enumerate(flows, 1)]
    d = sum(t * pv for t, pv in enumerate(pvs, 1)) / sum(pvs)
    return _n(f"A {n}-year bond pays a {c}% annual coupon and is priced to yield {y}%. What is its Macaulay duration?",
              f"{n} বছরের একটা বন্ড বছরে {c}% কুপন দেয়, দাম {y}% আয় হিসেবে। এর ম্যাকলে স্থিতিকাল কত?", d,
              f"Weight each year by the share of price it delivers: D = Σ t·PV(CFₜ) ÷ price = {_f(_c(d))} years - a bit under the {n}-year maturity.",
              f"প্রতিটি বছরকে দামের যে অংশ দেয় তা দিয়ে ভার দাও: D = Σ t·PV(CFₜ) ÷ দাম = {_f(_c(d))} বছর - {n} বছরের মেয়াদের সামান্য কম।",
              (n, (n + 1) / 2, d + 0.5), " years", " বছর")


def mod_duration(d, y, dy):
    dm = d / (1 + y / 100)
    r = dm * dy
    return _pc(f"A bond has a Macaulay duration of {d} years and yields {y}%. Roughly how much does its price fall if yields rise by {dy} percentage point?",
               f"একটা বন্ডের ম্যাকলে স্থিতিকাল {d} বছর, আয় {y}%। আয় {dy} শতাংশ-বিন্দু বাড়লে এর দাম প্রায় কত কমে?", r,
               f"Modified duration = {d} ÷ {1 + y / 100:g} = {_f(_c(dm))}; price change ≈ -{_f(_c(dm))} x {dy}% = -{_f(_c(r))}%.",
               f"সংশোধিত স্থিতিকাল = {d} ÷ {1 + y / 100:g} = {_f(_c(dm))}; দামের পরিবর্তন ≈ -{_f(_c(dm))} x {dy}% = -{_f(_c(r))}%।",
               (d * dy, dm * dy / 2, r + 1))


def zero_coupon(face, y, n):
    p = face / (1 + y / 100) ** n
    return _rs(f"A zero-coupon bond pays Rs {face:,} in {n} years. If the market yield is {y}%, what is its price today?",
               f"একটা শূন্য-কুপন বন্ড {n} বছর পরে Rs {face:,} দেবে। বাজার-আয় {y}% হলে আজ এর দাম কত?", p,
               f"P = F ÷ (1 + y)ⁿ = {face:,} ÷ {1 + y / 100:g}^{n} = Rs {_f(_c(p))}.",
               f"দাম = F ÷ (1 + y)ⁿ = {face:,} ÷ {1 + y / 100:g}^{n} = Rs {_f(_c(p))}।",
               (face * (1 - y / 100 * n), face / (1 + y / 100), p * 1.1))


def forward_rate(s1, s2):
    f = ((1 + s2 / 100) ** 2 / (1 + s1 / 100) - 1) * 100
    return _pc(f"The one-year spot rate is {s1}% and the two-year spot rate is {s2}%. What one-year rate, starting a year from now, is implied?",
               f"এক বছরের স্পট হার {s1}% আর দুই বছরের স্পট হার {s2}%। এক বছর পরে শুরু হওয়া এক বছরের কোন হার নিহিত?", f,
               f"(1 + s₂)² = (1 + s₁)(1 + f): f = {1 + s2 / 100:g}² ÷ {1 + s1 / 100:g} - 1 = {_f(_c(f))}%.",
               f"(1 + s₂)² = (1 + s₁)(1 + f): f = {1 + s2 / 100:g}² ÷ {1 + s1 / 100:g} - 1 = {_f(_c(f))}%।",
               ((s1 + s2) / 2, s2, f + 1))


def tbill_yield(face, price, days):
    r = (face - price) / price * 365 / days * 100
    return _pc(f"A {days}-day Treasury bill with face value Rs {face:,} is bought for Rs {price:,}. What is its annualised yield?",
               f"Rs {face:,} অভিহিত মূল্যের {days} দিনের একটা ট্রেজারি বিল Rs {price:,}-এ কেনা হল। এর বার্ষিক আয় কত?", r,
               f"Gain {face - price} on {price:,} for {days} days: ({face - price} ÷ {price:,}) x 365/{days} = {_f(_c(r))}%.",
               f"{days} দিনে {price:,}-এ {face - price} লাভ: ({face - price} ÷ {price:,}) x 365/{days} = {_f(_c(r))}%।",
               ((face - price) / face * 365 / days * 100, (face - price) / price * 100, r + 2))


# ---------------------------------------------------------------- working capital
def eoq(d, s, h):
    q = math.sqrt(2 * d * s / h)
    return _n(f"A contractor uses {d:,} bags of cement a year. Each order costs Rs {s} to place and holding one bag costs Rs {h} a year. What is the economic order quantity?",
              f"একজন ঠিকাদার বছরে {d:,} বস্তা সিমেন্ট ব্যবহার করেন। প্রতি অর্ডারে খরচ Rs {s}, আর এক বস্তা রাখার খরচ বছরে Rs {h}। অর্থনৈতিক অর্ডার-পরিমাণ কত?", q,
              f"EOQ = √(2DS/H) = √(2 x {d:,} x {s} ÷ {h}) = {_f(_c(q))} bags, where ordering and holding costs balance.",
              f"অর্থনৈতিক অর্ডার = √(2DS/H) = √(2 x {d:,} x {s} ÷ {h}) = {_f(_c(q))} বস্তা, যেখানে অর্ডার আর রাখার খরচ সমান।",
              (math.sqrt(d * s / h), d * s / h / 100, q * 1.5), " bags", " বস্তা")


def reorder(daily, lead, safety):
    r = daily * lead + safety
    return _n(f"A site uses {daily} steel rods a day, a delivery takes {lead} days and the safety stock is {safety} rods. At what stock level should a new order be placed?",
              f"একটা সাইটে দিনে {daily}টি ইস্পাতের রড লাগে, সরবরাহে {lead} দিন লাগে আর নিরাপত্তা-মজুত {safety}টি। মজুত কত হলে নতুন অর্ডার দেওয়া উচিত?", r,
              f"Reorder level = daily use x lead time + safety stock = {daily} x {lead} + {safety} = {r:,} rods.",
              f"পুনঃঅর্ডার স্তর = দৈনিক ব্যবহার x সরবরাহ-সময় + নিরাপত্তা-মজুত = {daily} x {lead} + {safety} = {r:,}টি রড।",
              (daily * lead, r + safety, daily + lead + safety), " rods", "টি রড")


def ccc(dio, dso, dpo):
    r = dio + dso - dpo
    return _n(f"A firm holds inventory for {dio} days, collects from customers in {dso} days and pays suppliers in {dpo} days. What is its cash conversion cycle?",
              f"একটা প্রতিষ্ঠান {dio} দিন মজুত রাখে, {dso} দিনে ক্রেতার থেকে টাকা পায় আর {dpo} দিনে সরবরাহকারীকে দেয়। এর নগদ রূপান্তর-চক্র কত?", r,
              f"CCC = DIO + DSO - DPO = {dio} + {dso} - {dpo} = {r} days of cash tied up.",
              f"নগদ চক্র = মজুত-দিন + আদায়-দিন - পরিশোধ-দিন = {dio} + {dso} - {dpo} = {r} দিন টাকা আটকে থাকে।",
              (dio + dso + dpo, dio + dso, r + 10), " days", " দিন")


# ---------------------------------------------------------------- capital structure and valuation
def sgr(roe, payout):
    r = roe * (1 - payout / 100)
    return _pc(f"A company earns a return on equity of {roe}% and pays out {payout}% of its profit as dividends. What is its sustainable growth rate?",
               f"একটা কোম্পানির ইকুইটির ওপর আয় {roe}%, আর মুনাফার {payout}% লভ্যাংশ দেয়। এর টেকসই বৃদ্ধির হার কত?", r,
               f"g = ROE x retention = {roe}% x {1 - payout / 100:g} = {_f(_c(r))}%: growth funded without new equity or more leverage.",
               f"বৃদ্ধি = ইকুইটি-আয় x ধরে রাখা অংশ = {roe}% x {1 - payout / 100:g} = {_f(_c(r))}%: নতুন ইকুইটি বা বাড়তি ঋণ ছাড়া।",
               (roe * payout / 100, roe, r + 3))


def indifference(i1, n1, i2, n2):
    e = (i2 * n1 - i1 * n2) / (n1 - n2)
    return _n(f"Plan A has interest of Rs {i1} lakh and {n1} lakh shares; plan B has interest of Rs {i2} lakh and {n2} lakh shares. At what EBIT (Rs lakh) is EPS the same for both?",
              f"পরিকল্পনা A-তে সুদ Rs {i1} লক্ষ আর {n1} লক্ষ শেয়ার; B-তে সুদ Rs {i2} লক্ষ আর {n2} লক্ষ শেয়ার। কোন ইবিআইটি-তে (Rs লক্ষ) দুটির ইপিএস সমান?", e,
              f"(EBIT - {i1}) ÷ {n1} = (EBIT - {i2}) ÷ {n2} (tax cancels): EBIT = ({i2} x {n1} - {i1} x {n2}) ÷ ({n1} - {n2}) = {_f(_c(e))}. Above it, the debt-heavy plan gives higher EPS.",
              f"(ইবিআইটি - {i1}) ÷ {n1} = (ইবিআইটি - {i2}) ÷ {n2} (কর কেটে যায়): ইবিআইটি = ({i2} x {n1} - {i1} x {n2}) ÷ ({n1} - {n2}) = {_f(_c(e))}। এর ওপরে বেশি-ঋণের পরিকল্পনায় ইপিএস বেশি।",
              (i1 + i2, (i2 - i1) * 2, e + i2))


def dtl(dol, dfl):
    r = dol * dfl
    return _n(f"A firm's degree of operating leverage is {dol} and its degree of financial leverage is {dfl}. If sales rise by 10%, by how much does EPS rise?",
              f"একটা প্রতিষ্ঠানের পরিচালন-লিভারেজ {dol} আর আর্থিক-লিভারেজ {dfl}। বিক্রি 10% বাড়লে ইপিএস কত বাড়ে?", r * 10,
              f"Degree of total leverage = DOL x DFL = {dol} x {dfl} = {_f(_c(r))}, so EPS rises {_f(_c(r))} x 10% = {_f(_c(r * 10))}%.",
              f"মোট লিভারেজ = পরিচালন x আর্থিক = {dol} x {dfl} = {_f(_c(r))}, তাই ইপিএস বাড়ে {_f(_c(r))} x 10% = {_f(_c(r * 10))}%।",
              ((dol + dfl) * 10, dol * 10, dfl * 10), "%")


def hamada(bu, de, t):
    bl = bu * (1 + (1 - t / 100) * de)
    return _n(f"A firm's unlevered (asset) beta is {bu}. It adopts a debt-to-equity ratio of {de} with a {t}% tax rate. What is its levered beta?",
              f"একটা প্রতিষ্ঠানের ঋণহীন (সম্পদ) বিটা {bu}। এটা {t}% করহারে ঋণ-ইকুইটি অনুপাত {de} নেয়। এর ঋণযুক্ত বিটা কত?", bl,
              f"Hamada: βL = βU[1 + (1 - t)D/E] = {bu} x [1 + {1 - t / 100:g} x {de}] = {_f(_c(bl))}. Debt makes equity riskier.",
              f"হামাদা: βL = βU[1 + (1 - t)D/E] = {bu} x [1 + {1 - t / 100:g} x {de}] = {_f(_c(bl))}। ঋণ ইকুইটিকে বেশি ঝুঁকিপূর্ণ করে।",
              (bu * (1 + de), bu, bl + 0.3))


def mm_tax(vu, debt, t):
    vl = vu + t / 100 * debt
    return _n(f"An all-equity firm is worth Rs {vu} crore. It borrows Rs {debt} crore permanently; the corporate tax rate is {t}%. Under Modigliani-Miller with taxes, what is it worth now (Rs crore)?",
              f"সম্পূর্ণ-ইকুইটির একটা প্রতিষ্ঠানের মূল্য Rs {vu} কোটি। এটা স্থায়ীভাবে Rs {debt} কোটি ধার নেয়; কর্পোরেট কর {t}%। করসহ মোদিগ্লিয়ানি-মিলার অনুযায়ী এখন মূল্য (Rs কোটি) কত?", vl,
              f"V_L = V_U + tD = {vu} + {t / 100:g} x {debt} = {_f(_c(vl))}: the interest tax shield adds value.",
              f"V_L = V_U + tD = {vu} + {t / 100:g} x {debt} = {_f(_c(vl))}: সুদের কর-ঢাল মূল্য যোগ করে।",
              (vu, vu + debt, vu - t / 100 * debt))


def fcff(ebit, t, dep, capex, dwc):
    r = ebit * (1 - t / 100) + dep - capex - dwc
    return _n(f"A company has EBIT of Rs {ebit} crore, a {t}% tax rate, depreciation of Rs {dep} crore, capital spending of Rs {capex} crore and a rise in working capital of Rs {dwc} crore. What is its free cash flow to the firm (Rs crore)?",
              f"একটা কোম্পানির ইবিআইটি Rs {ebit} কোটি, কর {t}%, অবচয় Rs {dep} কোটি, মূলধনী ব্যয় Rs {capex} কোটি আর কার্যকর মূলধন বৃদ্ধি Rs {dwc} কোটি। প্রতিষ্ঠানের মুক্ত নগদ প্রবাহ (Rs কোটি) কত?", r,
              f"FCFF = EBIT(1 - t) + depreciation - capex - ΔWC = {_f(_c(ebit * (1 - t / 100)))} + {dep} - {capex} - {dwc} = {_f(_c(r))}.",
              f"মুক্ত নগদ প্রবাহ = ইবিআইটি(1 - t) + অবচয় - মূলধনী ব্যয় - কার্যকর মূলধন বৃদ্ধি = {_f(_c(ebit * (1 - t / 100)))} + {dep} - {capex} - {dwc} = {_f(_c(r))}।",
              (ebit * (1 - t / 100), ebit + dep - capex - dwc, r + dwc + capex / 2))


def eva(nopat, wacc, capital):
    r = nopat - wacc / 100 * capital
    return _n(f"A division earns NOPAT of Rs {nopat} crore on capital of Rs {capital} crore; its WACC is {wacc}%. What is its economic value added (Rs crore)?",
              f"একটা বিভাগ Rs {capital} কোটি মূলধনে Rs {nopat} কোটি করোত্তর পরিচালন মুনাফা করে; মূলধন-ব্যয় {wacc}%। এর অর্থনৈতিক মূল্য সংযোজন (Rs কোটি) কত?", r,
              f"EVA = NOPAT - WACC x capital = {nopat} - {wacc / 100:g} x {capital} = {_f(_c(r))}: profit beyond the cost of all capital.",
              f"ইভিএ = করোত্তর পরিচালন মুনাফা - মূলধন-ব্যয় x মূলধন = {nopat} - {wacc / 100:g} x {capital} = {_f(_c(r))}: সব মূলধনের খরচের বাইরের মুনাফা।",
              (nopat, wacc / 100 * capital, r + 10))


def two_stage(d0, g1, k, g2):
    d1 = d0 * (1 + g1 / 100)
    d2 = d1 * (1 + g1 / 100)
    p2 = d2 * (1 + g2 / 100) / (k / 100 - g2 / 100)
    v = d1 / (1 + k / 100) + (d2 + p2) / (1 + k / 100) ** 2
    return _rs(f"A share just paid Rs {d0}. Dividends grow {g1}% a year for two years, then {g2}% forever. Investors want {k}%. What is the share worth?",
               f"একটা শেয়ার সদ্য Rs {d0} দিয়েছে। লভ্যাংশ দুই বছর {g1}% হারে, তারপর চিরকাল {g2}% হারে বাড়বে। বিনিয়োগকারী {k}% চান। শেয়ারের মূল্য কত?", v,
               f"D₁ = {_f(_c(d1))}, D₂ = {_f(_c(d2))}, P₂ = D₃/(k - g) = {_f(_c(p2))}; value = D₁/{1 + k / 100:g} + (D₂ + P₂)/{1 + k / 100:g}² = Rs {_f(_c(v))}.",
               f"D₁ = {_f(_c(d1))}, D₂ = {_f(_c(d2))}, P₂ = D₃/(k - g) = {_f(_c(p2))}; মূল্য = D₁/{1 + k / 100:g} + (D₂ + P₂)/{1 + k / 100:g}² = Rs {_f(_c(v))}।",
               (d0 * (1 + g2 / 100) / (k / 100 - g2 / 100), p2, v * 1.2))


def justified_pe(payout, k, g):
    r = (payout / 100) / (k / 100 - g / 100)
    return _n(f"A firm pays out {payout}% of earnings, its dividends grow at {g}% a year and investors want {k}%. What forward P/E ratio is justified?",
              f"একটা প্রতিষ্ঠান আয়ের {payout}% লভ্যাংশ দেয়, লভ্যাংশ বছরে {g}% বাড়ে আর বিনিয়োগকারী {k}% চান। কোন অগ্রিম পি/ই অনুপাত যুক্তিসংগত?", r,
              f"From Gordon: P₀/E₁ = payout ÷ (k - g) = {payout / 100:g} ÷ {(k - g) / 100:g} = {_f(_c(r))}.",
              f"গর্ডন সূত্র থেকে: P₀/E₁ = বিতরণ-অনুপাত ÷ (k - g) = {payout / 100:g} ÷ {(k - g) / 100:g} = {_f(_c(r))}।",
              (1 / (k / 100), payout / k, r + 4))


def terp(n_old, price, n_new, sub):
    r = (n_old * price + n_new * sub) / (n_old + n_new)
    return _rs(f"A share trades at Rs {price}. The company offers {n_new} new share for every {n_old} held at Rs {sub}. What is the theoretical ex-rights price?",
               f"একটা শেয়ারের দাম Rs {price}। কোম্পানি প্রতি {n_old}টি শেয়ারে {n_new}টি নতুন শেয়ার Rs {sub}-এ দিচ্ছে। তাত্ত্বিক অধিকার-পরবর্তী দাম কত?", r,
               f"({n_old} x {price} + {n_new} x {sub}) ÷ {n_old + n_new} = Rs {_f(_c(r))}; the right itself is worth Rs {_f(_c(r - sub))}.",
               f"({n_old} x {price} + {n_new} x {sub}) ÷ {n_old + n_new} = Rs {_f(_c(r))}; অধিকারটির নিজের মূল্য Rs {_f(_c(r - sub))}।",
               ((price + sub) / 2, price - sub, r + 15))


def roe_from(roa, de):
    r = roa * (1 + de)
    return _pc(f"A firm earns a {roa}% return on assets and has a debt-to-equity ratio of {de}. Ignoring interest effects on profit, what is its return on equity?",
               f"একটা প্রতিষ্ঠানের সম্পদের ওপর আয় {roa}% আর ঋণ-ইকুইটি অনুপাত {de}। মুনাফায় সুদের প্রভাব বাদ দিলে ইকুইটির ওপর আয় কত?", r,
               f"Assets = equity x (1 + D/E), so ROE = ROA x (1 + D/E) = {roa} x {1 + de:g} = {_f(_c(r))}%.",
               f"সম্পদ = ইকুইটি x (1 + D/E), তাই ইকুইটি-আয় = সম্পদ-আয় x (1 + D/E) = {roa} x {1 + de:g} = {_f(_c(r))}%।",
               (roa * de, roa + de, r + 5))


def loan_balance(p, r, n, k):
    i = r / 1200
    emi = p * i * (1 + i) ** n / ((1 + i) ** n - 1)
    bal = emi * (1 - (1 + i) ** -(n - k)) / i
    return _rs(f"A Rs {p:,} loan at {r}% a year is repaid by {n} monthly EMIs. How much is still owed just after the {k}th EMI?",
               f"Rs {p:,} ঋণ বছরে {r}% সুদে {n}টি মাসিক কিস্তিতে শোধ হয়। {k}-তম কিস্তির ঠিক পরে কত বাকি থাকে?", bal,
               f"EMI = Rs {_f(_c(emi))}; the balance is the present value of the {n - k} EMIs left = Rs {_f(_c(bal))} (early EMIs are mostly interest).",
               f"কিস্তি = Rs {_f(_c(emi))}; বাকি = অবশিষ্ট {n - k}টি কিস্তির বর্তমান মূল্য = Rs {_f(_c(bal))} (প্রথম দিকের কিস্তি বেশির ভাগই সুদ)।",
               (p * (n - k) / n, emi * (n - k), bal * 0.9))


# ---------------------------------------------------------------- derivatives
def binomial(s, u, d, k, r):
    p = (1 + r / 100 - d) / (u - d)
    cu, cd = max(s * u - k, 0), max(s * d - k, 0)
    c = (p * cu + (1 - p) * cd) / (1 + r / 100)
    return _rs(f"A share at Rs {s} will move to Rs {_f(_c(s * u))} or Rs {_f(_c(s * d))} in one year; the risk-free rate is {r}%. What is a one-year call with strike Rs {k} worth (one-step binomial)?",
               f"Rs {s}-এর একটা শেয়ার এক বছরে Rs {_f(_c(s * u))} বা Rs {_f(_c(s * d))} হবে; ঝুঁকিহীন হার {r}%। স্ট্রাইক Rs {k}-এর এক বছরের কল অপশনের মূল্য কত (এক-ধাপ দ্বিপদ)?", c,
               f"Risk-neutral p = (1 + r - d)/(u - d) = {_f(_c(p))}; payoffs {_f(_c(cu))} and {_f(_c(cd))}; C = [p x {_f(_c(cu))} + (1 - p) x {_f(_c(cd))}] ÷ {1 + r / 100:g} = Rs {_f(_c(c))}.",
               f"ঝুঁকি-নিরপেক্ষ p = (1 + r - d)/(u - d) = {_f(_c(p))}; প্রাপ্তি {_f(_c(cu))} আর {_f(_c(cd))}; C = [p x {_f(_c(cu))} + (1 - p) x {_f(_c(cd))}] ÷ {1 + r / 100:g} = Rs {_f(_c(c))}।",
               (0.5 * cu / (1 + r / 100), cu, c * 1.5))


def call_from_put(s, k, r, put):
    c = put + s - k / (1 + r / 100)
    return _rs(f"A share trades at Rs {s}; a one-year European put with strike Rs {k} costs Rs {put} and the risk-free rate is {r}%. What should the matching call cost?",
               f"একটা শেয়ারের দাম Rs {s}; স্ট্রাইক Rs {k}-এর এক বছরের ইউরোপীয় পুট Rs {put}, আর ঝুঁকিহীন হার {r}%। একই রকম কলের দাম কত হওয়া উচিত?", c,
               f"Put-call parity: C = P + S - K/(1 + r) = {put} + {s} - {_f(_c(k / (1 + r / 100)))} = Rs {_f(_c(c))}.",
               f"পুট-কল সমতা: C = P + S - K/(1 + r) = {put} + {s} - {_f(_c(k / (1 + r / 100)))} = Rs {_f(_c(c))}।",
               (put + s - k, put, c + 5))


def straddle(k, call, put, st):
    r = abs(st - k) - call - put
    return _rs(f"An investor buys a straddle: a call and a put, both with strike Rs {k}, costing Rs {call} and Rs {put}. At expiry the share is at Rs {st}. What is the profit?",
               f"একজন বিনিয়োগকারী একটা স্ট্র্যাডল কেনেন: স্ট্রাইক Rs {k}-এর একটা কল আর একটা পুট, দাম Rs {call} আর Rs {put}। মেয়াদশেষে শেয়ারের দাম Rs {st}। মুনাফা কত?", r,
               f"Payoff |S - K| = {abs(st - k)}, minus premiums {call + put}: Rs {_f(_c(r))}. Straddles gain from big moves either way.",
               f"প্রাপ্তি |S - K| = {abs(st - k)}, বাদ প্রিমিয়াম {call + put}: Rs {_f(_c(r))}। স্ট্র্যাডল যেকোনো দিকে বড় নড়াচড়ায় লাভ করে।",
               (abs(st - k), abs(st - k) - call, r + put))


# ---------------------------------------------------------------- risk, portfolios and international
def ppp(spot, inf_d, inf_f):
    e = spot * (1 + inf_d / 100) / (1 + inf_f / 100)
    return _rs(f"The rupee is at Rs {spot} per dollar. Indian inflation is expected at {inf_d}% and US inflation at {inf_f}%. By relative PPP, what rate is expected in one year?",
               f"রুপি ডলারপ্রতি Rs {spot}। ভারতে মুদ্রাস্ফীতি {inf_d}% আর আমেরিকায় {inf_f}% আশা করা হচ্ছে। আপেক্ষিক ক্রয়ক্ষমতা সমতা অনুযায়ী এক বছর পরে কত হারের আশা?", e,
               f"E₁ = E₀ x (1 + π_India) ÷ (1 + π_US) = {spot} x {1 + inf_d / 100:g} ÷ {1 + inf_f / 100:g} = Rs {_f(_c(e))}: higher inflation weakens a currency.",
               f"E₁ = E₀ x (1 + ভারতের স্ফীতি) ÷ (1 + আমেরিকার স্ফীতি) = {spot} x {1 + inf_d / 100:g} ÷ {1 + inf_f / 100:g} = Rs {_f(_c(e))}: বেশি স্ফীতি মুদ্রাকে দুর্বল করে।",
               (spot * (1 + inf_f / 100) / (1 + inf_d / 100), spot + inf_d - inf_f + 3, spot))


def var95(value, sd):
    r = 1.65 * sd / 100 * value
    return _n(f"A portfolio worth Rs {value} lakh has a daily return standard deviation of {sd}%. What is its one-day 95% Value-at-Risk (normal returns), in Rs lakh?",
              f"Rs {value} লক্ষের একটা পোর্টফোলিওর দৈনিক আয়ের সমক বিচ্যুতি {sd}%। এর এক দিনের 95% ঝুঁকি-মূল্য (স্বাভাবিক বিন্যাস) Rs লক্ষে কত?", r,
              f"VaR = 1.65 x σ x value = 1.65 x {sd / 100:g} x {value} = {_f(_c(r))}: on 19 days out of 20 the loss should be smaller.",
              f"ঝুঁকি-মূল্য = 1.65 x σ x মূল্য = 1.65 x {sd / 100:g} x {value} = {_f(_c(r))}: 20 দিনের 19 দিন ক্ষতি এর চেয়ে কম হওয়ার কথা।",
              (sd / 100 * value, 2.33 * sd / 100 * value, r * 1.5))


def treynor(rp, rf, beta):
    r = (rp - rf) / beta
    return _n(f"A fund earned {rp}% with a beta of {beta} while the risk-free rate was {rf}%. What is its Treynor ratio?",
              f"একটা ফান্ড {beta} বিটায় {rp}% আয় করেছে, ঝুঁকিহীন হার ছিল {rf}%। এর ট্রেনর অনুপাত কত?", r,
              f"Treynor = (Rp - Rf) ÷ β = ({rp} - {rf}) ÷ {beta} = {_f(_c(r))}: excess return per unit of market risk.",
              f"ট্রেনর = (Rp - Rf) ÷ β = ({rp} - {rf}) ÷ {beta} = {_f(_c(r))}: বাজার-ঝুঁকির প্রতি এককে বাড়তি আয়।",
              ((rp - rf) * beta, rp / beta, r + 2))


def jensen(rp, rf, beta, rm):
    a = rp - (rf + beta * (rm - rf))
    return _pc(f"A fund returned {rp}% with a beta of {beta}. The risk-free rate was {rf}% and the market returned {rm}%. What is its Jensen's alpha?",
               f"একটা ফান্ড {beta} বিটায় {rp}% আয় দিয়েছে। ঝুঁকিহীন হার {rf}% আর বাজার-আয় {rm}%। এর জেনসেন আলফা কত?", a,
               f"Alpha = Rp - [Rf + β(Rm - Rf)] = {rp} - [{rf} + {beta} x {rm - rf}] = {_f(_c(a))}%: return beyond what CAPM predicts.",
               f"আলফা = Rp - [Rf + β(Rm - Rf)] = {rp} - [{rf} + {beta} x {rm - rf}] = {_f(_c(a))}%: সিএপিএম-এর অনুমানের বাইরের আয়।",
               (rp - rm, rp - rf, a + 2))


def port_beta(w, b1, b2):
    r = w / 100 * b1 + (1 - w / 100) * b2
    return _n(f"A portfolio puts {w}% in a share with beta {b1} and the rest in one with beta {b2}. What is the portfolio beta?",
              f"একটা পোর্টফোলিও {w}% রাখে বিটা {b1}-এর শেয়ারে, বাকিটা বিটা {b2}-এর শেয়ারে। পোর্টফোলিওর বিটা কত?", r,
              f"β_p = Σ wᵢβᵢ = {w / 100:g} x {b1} + {1 - w / 100:g} x {b2} = {_f(_c(r))}.",
              f"β_p = Σ wᵢβᵢ = {w / 100:g} x {b1} + {1 - w / 100:g} x {b2} = {_f(_c(r))}।",
              ((b1 + b2) / 2 + 0.15, b1 * b2, r + 0.4))


def corr_sd(s1, s2, rho):
    v = 0.25 * s1 * s1 + 0.25 * s2 * s2 + 2 * 0.25 * rho * s1 * s2
    r = math.sqrt(v)
    return _pc(f"Two assets with standard deviations {s1}% and {s2}% have a correlation of {rho}. What is the standard deviation of a 50:50 portfolio?",
               f"{s1}% আর {s2}% সমক বিচ্যুতির দুটি সম্পদের সহসম্বন্ধ {rho}। 50:50 পোর্টফোলিওর সমক বিচ্যুতি কত?", r,
               f"σ² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂ = {_f(_c(v))}; σ = {_f(_c(r))}% - less than the average {_f(_c((s1 + s2) / 2))}% unless ρ = 1.",
               f"σ² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂ = {_f(_c(v))}; σ = {_f(_c(r))}% - ρ = 1 না হলে গড় {_f(_c((s1 + s2) / 2))}%-এর চেয়ে কম।",
               ((s1 + s2) / 2, math.sqrt(0.25 * s1 * s1 + 0.25 * s2 * s2), r + 3))


def min_var(s1, s2):
    w = s2 * s2 / (s1 * s1 + s2 * s2) * 100
    return _pc(f"Two uncorrelated assets have standard deviations of {s1}% and {s2}%. What share of the money should go into the first asset to minimise portfolio risk?",
               f"দুটি অসম্বন্ধ সম্পদের সমক বিচ্যুতি {s1}% আর {s2}%। পোর্টফোলিওর ঝুঁকি ন্যূনতম করতে টাকার কত অংশ প্রথম সম্পদে রাখা উচিত?", w,
               f"With ρ = 0, w₁ = σ₂² ÷ (σ₁² + σ₂²) = {s2 * s2} ÷ {s1 * s1 + s2 * s2} = {_f(_c(w))}%: more goes into the safer asset.",
               f"ρ = 0 হলে w₁ = σ₂² ÷ (σ₁² + σ₂²) = {s2 * s2} ÷ {s1 * s1 + s2 * s2} = {_f(_c(w))}%: নিরাপদ সম্পদে বেশি যায়।",
               (s2 / (s1 + s2) * 100, 50 if abs(w - 50) > 1 else 40, 100 - w))


NUMERIC = [
    irr2(1000, 600, 600), irr2(1000, 500, 700), irr2(2000, 1000, 1500),
    mirr(1000, [500, 600, 400], 10), mirr(5000, [2000, 2500, 3000], 12), mirr(2000, [800, 900, 1000], 8),
    disc_payback(10000, 4000, 10, 5), disc_payback(50000, 15000, 12, 8), disc_payback(20000, 6000, 8, 6),
    ytm_approx(1000, 80, 950, 5), ytm_approx(1000, 100, 1080, 4), ytm_approx(1000, 60, 900, 10),
    macaulay(1000, 10, 10, 2), macaulay(1000, 8, 10, 3), macaulay(1000, 12, 8, 2),
    mod_duration(5, 8, 1), mod_duration(7.5, 10, 0.5), mod_duration(3, 6, 2),
    zero_coupon(100000, 8, 5), zero_coupon(1000, 10, 3), zero_coupon(500000, 7, 10),
    forward_rate(6, 7), forward_rate(5, 6.5), forward_rate(8, 7.5),
    tbill_yield(100, 98, 91), tbill_yield(100, 96.5, 182), tbill_yield(100, 93, 364),
    eoq(10000, 200, 4), eoq(36000, 500, 10), eoq(5000, 300, 12),
    reorder(40, 7, 100), reorder(25, 12, 60), reorder(120, 5, 300),
    ccc(60, 45, 30), ccc(90, 60, 75), ccc(30, 20, 40),
    sgr(18, 40), sgr(24, 25), sgr(15, 60),
    indifference(20, 10, 60, 6), indifference(10, 8, 40, 5), indifference(30, 20, 90, 12),
    dtl(2, 1.5), dtl(3, 1.25), dtl(1.8, 2),
    hamada(0.8, 1, 30), hamada(1.1, 0.5, 25), hamada(0.6, 2, 30),
    mm_tax(500, 200, 30), mm_tax(1000, 400, 25), mm_tax(250, 100, 35),
    fcff(100, 30, 20, 40, 10), fcff(250, 25, 50, 90, 25), fcff(60, 30, 15, 20, 5),
    eva(30, 12, 200), eva(80, 10, 500), eva(45, 14, 250),
    two_stage(4, 20, 14, 6), two_stage(10, 15, 12, 5), two_stage(2, 25, 15, 6),
    justified_pe(40, 12, 8), justified_pe(60, 14, 10), justified_pe(30, 11, 7),
    terp(4, 200, 1, 150), terp(5, 120, 2, 85), terp(3, 500, 1, 380),
    roe_from(8, 1), roe_from(6, 1.5), roe_from(10, 0.5),
    loan_balance(1000000, 9, 120, 60), loan_balance(500000, 12, 60, 24),
    binomial(100, 1.2, 0.8, 100, 5), binomial(50, 1.3, 0.9, 55, 6), binomial(200, 1.25, 0.8, 190, 10),
    call_from_put(100, 100, 10, 5), call_from_put(250, 240, 8, 12), call_from_put(500, 520, 10, 30),
    straddle(100, 8, 6, 125), straddle(500, 25, 20, 430), straddle(200, 10, 9, 230),
    ppp(83, 6, 3), ppp(80, 5, 2), ppp(85, 4.5, 2.5),
    var95(100, 1.2), var95(500, 2), var95(250, 0.8),
    treynor(15, 6, 1.2), treynor(12, 5, 0.8), treynor(20, 7, 1.5),
    jensen(16, 6, 1.2, 12), jensen(13, 5, 0.9, 11), jensen(18, 7, 1.4, 13),
    port_beta(60, 1.4, 0.8), port_beta(30, 1.8, 1.0), port_beta(75, 0.6, 1.2),
    corr_sd(20, 30, 0.5), corr_sd(15, 25, -0.4), corr_sd(10, 20, 0.2),
    min_var(20, 10), min_var(30, 15), min_var(25, 20),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    # ---------------------------------------------------------------- capital budgeting
    _q("When NPV and IRR rank two mutually exclusive projects differently, which should usually decide?", ["NPV, because it measures the value added in rupees", "IRR, because a percentage is easier to compare", "Payback period", "Whichever project is cheaper"],
       "Conflicts come from differences in scale or timing; NPV assumes reinvestment at the cost of capital, which is more realistic than at the IRR.",
       "দুটি পরস্পর-বর্জনীয় প্রকল্পকে এনপিভি আর আইআরআর আলাদা ক্রমে সাজালে সাধারণত কোনটি সিদ্ধান্ত নেবে?", ["এনপিভি, কারণ এটা টাকায় যোগ হওয়া মূল্য মাপে", "আইআরআর, কারণ শতাংশ তুলনা করা সহজ", "পরিশোধকাল", "যে প্রকল্প সস্তা"],
       "আকার বা সময়ের পার্থক্যে বিরোধ হয়; এনপিভি মূলধন-ব্যয়ে পুনর্বিনিয়োগ ধরে, যা আইআরআর-এ পুনর্বিনিয়োগের চেয়ে বাস্তবসম্মত।"),
    _q("A project's cash flows change sign more than once (-, +, -). What problem can arise?", ["It can have more than one IRR", "Its NPV cannot be calculated", "Its payback is always infinite", "It must be rejected"],
       "Each sign change can add a root (Descartes' rule); NPV still gives a clear answer at the cost of capital.",
       "একটা প্রকল্পের নগদ প্রবাহের চিহ্ন একাধিকবার বদলায় (-, +, -)। কোন সমস্যা হতে পারে?", ["এর একাধিক আইআরআর থাকতে পারে", "এর এনপিভি গণনা করা যায় না", "এর পরিশোধকাল সবসময় অসীম", "এটা বাতিল করতেই হবে"],
       "প্রতিটি চিহ্ন-পরিবর্তন একটা বীজ যোগ করতে পারে (দেকার্তের নিয়ম); মূলধন-ব্যয়ে এনপিভি তখনো স্পষ্ট উত্তর দেয়।"),
    _q("Money already spent on a feasibility study last year should be treated in a capital budgeting decision as…", ["A sunk cost, ignored because it cannot be recovered", "An outflow of the project", "An inflow of the project", "Part of working capital"],
       "Only incremental future cash flows matter; opportunity costs (like the rent a site could earn) must be included.",
       "গত বছর সম্ভাব্যতা-সমীক্ষায় খরচ হওয়া টাকাকে মূলধন-বাজেট সিদ্ধান্তে ধরা উচিত…", ["নিমজ্জিত ব্যয় হিসেবে, যা ফেরত আসে না বলে উপেক্ষা করা হয়", "প্রকল্পের বহিঃপ্রবাহ হিসেবে", "প্রকল্পের অন্তঃপ্রবাহ হিসেবে", "কার্যকর মূলধনের অংশ হিসেবে"],
       "কেবল বাড়তি ভবিষ্যৎ নগদ প্রবাহ গোনে; সুযোগ-ব্যয় (যেমন জমিটি যে ভাড়া পেত) ধরতেই হবে।"),
    _q("A new product steals some sales from the company's existing product. In project evaluation this is…", ["Cannibalisation - the lost profit is a cost of the new project", "Irrelevant", "A sunk cost", "Extra revenue for the new project"],
       "Side effects on other parts of the firm (externalities) belong in the incremental cash flows.",
       "নতুন একটা পণ্য কোম্পানির পুরোনো পণ্যের কিছু বিক্রি কেড়ে নেয়। প্রকল্প মূল্যায়নে এটা…", ["স্বজাতিভক্ষণ - হারানো মুনাফা নতুন প্রকল্পের খরচ", "অপ্রাসঙ্গিক", "নিমজ্জিত ব্যয়", "নতুন প্রকল্পের বাড়তি আয়"],
       "প্রতিষ্ঠানের অন্য অংশে পার্শ্বপ্রতিক্রিয়া (বাহ্যিকতা) বাড়তি নগদ প্রবাহের মধ্যে ধরতে হয়।"),
    _q("Two machines with different lives (3 years and 5 years) do the same job. How should they be compared?", ["By equivalent annual annuity (or a common replacement horizon)", "By total NPV only", "By purchase price only", "By IRR only"],
       "EAA spreads each NPV into an equal yearly amount, so a short-lived cheap machine can be fairly compared with a long-lived one.",
       "আলাদা আয়ুর (3 বছর আর 5 বছর) দুটি যন্ত্র একই কাজ করে। কীভাবে তুলনা করা উচিত?", ["সমতুল্য বার্ষিক বার্ষিকী দিয়ে (বা সাধারণ প্রতিস্থাপন-সময় ধরে)", "কেবল মোট এনপিভি দিয়ে", "কেবল ক্রয়মূল্য দিয়ে", "কেবল আইআরআর দিয়ে"],
       "সমতুল্য বার্ষিকী প্রতিটি এনপিভিকে সমান বার্ষিক অঙ্কে ছড়ায়, তাই স্বল্পায়ু সস্তা যন্ত্রকে দীর্ঘায়ুর সঙ্গে ন্যায্যভাবে তুলনা করা যায়।"),
    _q("The right to wait a year before building a toll bridge, until traffic is clearer, is an example of…", ["A real option (option to delay)", "A sunk cost", "A financial lease", "Working capital"],
       "Real options - to delay, expand or abandon - add value that a static NPV misses, especially when uncertainty is high.",
       "যান চলাচল আরও স্পষ্ট হওয়া পর্যন্ত টোল-সেতু তৈরির আগে এক বছর অপেক্ষার অধিকার কীসের উদাহরণ?", ["বাস্তব অপশন (দেরি করার অপশন)", "নিমজ্জিত ব্যয়", "আর্থিক লিজ", "কার্যকর মূলধন"],
       "বাস্তব অপশন - দেরি, সম্প্রসারণ বা পরিত্যাগের - এমন মূল্য যোগ করে যা স্থির এনপিভি ধরে না, বিশেষত অনিশ্চয়তা বেশি হলে।"),
    _q("A company evaluating a project much riskier than its usual business should discount it at…", ["A rate reflecting the project's own risk, e.g. from the beta of a pure-play firm", "The company's overall WACC", "The risk-free rate", "The bank's savings rate"],
       "Using one WACC for everything accepts too many risky projects and rejects safe ones.",
       "স্বাভাবিক ব্যবসার চেয়ে অনেক বেশি ঝুঁকির একটা প্রকল্প মূল্যায়নে কোম্পানির বাট্টা দেওয়া উচিত…", ["প্রকল্পের নিজস্ব ঝুঁকি-প্রতিফলিত হারে, যেমন একই ব্যবসার প্রতিষ্ঠানের বিটা থেকে", "কোম্পানির সামগ্রিক মূলধন-ব্যয়ে", "ঝুঁকিহীন হারে", "ব্যাংকের সঞ্চয় হারে"],
       "সব কিছুতে একটা মূলধন-ব্যয় ব্যবহার করলে বেশি ঝুঁকির প্রকল্প বেশি গৃহীত হয় আর নিরাপদ প্রকল্প বাতিল হয়।"),
    _q("Sensitivity analysis in capital budgeting shows…", ["How NPV changes when one input (such as sales or cost) changes, others held constant", "The exact future cash flows", "The tax rate", "The project's legal risks"],
       "Scenario analysis changes several inputs together; Monte Carlo simulation samples many combinations.",
       "মূলধন-বাজেটে সংবেদনশীলতা বিশ্লেষণ দেখায়…", ["বাকিগুলো স্থির রেখে একটা উপাদান (যেমন বিক্রি বা খরচ) বদলালে এনপিভি কীভাবে বদলায়", "সঠিক ভবিষ্যৎ নগদ প্রবাহ", "করহার", "প্রকল্পের আইনি ঝুঁকি"],
       "পরিস্থিতি বিশ্লেষণ একসঙ্গে কয়েকটি উপাদান বদলায়; মন্টে কার্লো সিমুলেশন অনেক সংমিশ্রণ পরীক্ষা করে।"),
    _q("Under capital rationing (a fixed budget), projects are best chosen by…", ["Ranking on the profitability index and picking the highest within the budget", "Choosing the single largest project", "Ranking by payback only", "Choosing at random"],
       "PI = PV of inflows ÷ investment shows value per rupee invested; with indivisible projects, check combinations.",
       "মূলধন-রেশনিংয়ে (নির্দিষ্ট বাজেটে) প্রকল্প সবচেয়ে ভালো বাছা যায়…", ["লাভজনকতা সূচকে ক্রম সাজিয়ে বাজেটের মধ্যে সর্বোচ্চগুলো নিয়ে", "একক সবচেয়ে বড় প্রকল্প বেছে", "কেবল পরিশোধকালে ক্রম সাজিয়ে", "এলোমেলোভাবে বেছে"],
       "লাভজনকতা সূচক = অন্তঃপ্রবাহের বর্তমান মূল্য ÷ বিনিয়োগ, প্রতি টাকার মূল্য দেখায়; অবিভাজ্য প্রকল্পে সংমিশ্রণ যাচাই করো।"),
    _q("In a DCF valuation, why must the perpetual growth rate in the terminal value stay below the economy's long-run growth?", ["No firm can grow faster than the whole economy forever", "Taxes forbid it", "It makes the NPV negative", "Accounting rules require it"],
       "A growth rate above the discount rate would also give an infinite value; terminal value often makes up most of a DCF.",
       "ডিসিএফ মূল্যায়নে অন্তিম মূল্যের চিরস্থায়ী বৃদ্ধির হার কেন অর্থনীতির দীর্ঘমেয়াদি বৃদ্ধির নিচে রাখতে হয়?", ["কোনো প্রতিষ্ঠান চিরকাল গোটা অর্থনীতির চেয়ে দ্রুত বাড়তে পারে না", "কর তা নিষেধ করে", "এতে এনপিভি ঋণাত্মক হয়", "হিসাবের নিয়মে বাধ্যতামূলক"],
       "বাট্টা হারের চেয়ে বেশি বৃদ্ধি অসীম মূল্যও দিত; প্রায়ই ডিসিএফ-এর বেশির ভাগ অন্তিম মূল্য থেকে আসে।"),
    # ---------------------------------------------------------------- capital structure and dividends
    _q("According to Modigliani-Miller proposition II (no taxes), as a firm borrows more, its cost of equity…", ["Rises, exactly offsetting the cheaper debt so WACC stays constant", "Falls", "Stays the same", "Becomes equal to the cost of debt"],
       "rₑ = r₀ + (r₀ - r_d)D/E: shareholders demand more for the extra financial risk.",
       "মোদিগ্লিয়ানি-মিলারের দ্বিতীয় প্রস্তাব (কর ছাড়া) অনুযায়ী প্রতিষ্ঠান বেশি ধার নিলে তার ইকুইটি-ব্যয়…", ["বাড়ে, সস্তা ঋণকে ঠিক পুষিয়ে দেয়, তাই মূলধন-ব্যয় স্থির থাকে", "কমে", "একই থাকে", "ঋণ-ব্যয়ের সমান হয়"],
       "rₑ = r₀ + (r₀ - r_d)D/E: বাড়তি আর্থিক ঝুঁকির জন্য শেয়ারহোল্ডাররা বেশি চান।"),
    _q("The trade-off theory says the best capital structure balances…", ["The tax benefit of debt against the costs of financial distress", "Dividends against buybacks", "Assets against liabilities", "Inflation against interest"],
       "Firms with stable cash flows and tangible assets can carry more debt; risky, intangible-heavy firms carry less.",
       "বিনিময় তত্ত্ব বলে সেরা মূলধন-কাঠামো ভারসাম্য রাখে…", ["ঋণের কর-সুবিধা আর আর্থিক সংকটের খরচের মধ্যে", "লভ্যাংশ আর বাইব্যাকের মধ্যে", "সম্পদ আর দায়ের মধ্যে", "মুদ্রাস্ফীতি আর সুদের মধ্যে"],
       "স্থিতিশীল নগদ প্রবাহ আর বাস্তব সম্পদের প্রতিষ্ঠান বেশি ঋণ বইতে পারে; ঝুঁকিপূর্ণ, অবাস্তব সম্পদনির্ভর প্রতিষ্ঠান কম।"),
    _q("The pecking-order theory says firms prefer to finance in which order?", ["Retained earnings, then debt, then new equity last", "New equity, then debt, then retained earnings", "Debt only", "Equity only"],
       "Managers know more than investors, so issuing shares signals overvaluation; internal funds avoid that signal.",
       "পেকিং-অর্ডার তত্ত্ব বলে প্রতিষ্ঠান কোন ক্রমে অর্থ জোগাড় পছন্দ করে?", ["সঞ্চিত মুনাফা, তারপর ঋণ, শেষে নতুন ইকুইটি", "নতুন ইকুইটি, তারপর ঋণ, তারপর সঞ্চিত মুনাফা", "কেবল ঋণ", "কেবল ইকুইটি"],
       "ব্যবস্থাপক বিনিয়োগকারীর চেয়ে বেশি জানেন, তাই শেয়ার ছাড়া অতিমূল্যায়নের সংকেত দেয়; নিজস্ব তহবিল সেই সংকেত এড়ায়।"),
    _q("Shareholders of a nearly bankrupt firm pushing it into very risky projects, at lenders' expense, is…", ["The asset-substitution (risk-shifting) agency cost of debt", "The clientele effect", "The bird-in-hand theory", "A rights issue"],
       "Shareholders keep the upside but lenders bear most of the downside, so lenders add covenants to loans.",
       "প্রায় দেউলিয়া প্রতিষ্ঠানের শেয়ারহোল্ডাররা ঋণদাতার খরচে খুব ঝুঁকিপূর্ণ প্রকল্পে ঠেলে দেওয়া হল…", ["ঋণের সম্পদ-প্রতিস্থাপন (ঝুঁকি-স্থানান্তর) এজেন্সি খরচ", "ক্লায়েন্টেল প্রভাব", "হাতে-থাকা-পাখি তত্ত্ব", "রাইটস ইস্যু"],
       "লাভের দিক শেয়ারহোল্ডারের, ক্ষতির বেশির ভাগ ঋণদাতার, তাই ঋণদাতা ঋণে শর্ত জুড়ে দেন।"),
    _q("Jensen's free cash flow hypothesis suggests that debt can add value because…", ["Interest payments stop managers wasting surplus cash on poor projects", "Debt is always cheaper than equity", "Debt raises the share price automatically", "Debt removes taxes"],
       "Committed payouts discipline managers of cash-rich firms with few good investments.",
       "জেনসেনের মুক্ত নগদ প্রবাহ প্রকল্প বলে ঋণ মূল্য যোগ করতে পারে কারণ…", ["সুদ দিতে হয় বলে ব্যবস্থাপক বাড়তি নগদ বাজে প্রকল্পে নষ্ট করতে পারেন না", "ঋণ সবসময় ইকুইটির চেয়ে সস্তা", "ঋণ নিজে থেকে শেয়ারদর বাড়ায়", "ঋণ কর তুলে দেয়"],
       "নির্ধারিত পরিশোধ নগদ-সমৃদ্ধ কিন্তু ভালো বিনিয়োগহীন প্রতিষ্ঠানের ব্যবস্থাপককে শৃঙ্খলায় রাখে।"),
    _q("Modigliani and Miller's dividend irrelevance theory holds that, in perfect markets…", ["Dividend policy does not change firm value; investors can create 'home-made' dividends", "High dividends always raise value", "Low dividends always raise value", "Firms must pay all earnings out"],
       "The 'bird-in-hand' view and tax, signalling and clientele effects explain why policy may matter in practice.",
       "মোদিগ্লিয়ানি-মিলারের লভ্যাংশ-অপ্রাসঙ্গিকতা তত্ত্ব বলে, নিখুঁত বাজারে…", ["লভ্যাংশ নীতি প্রতিষ্ঠানের মূল্য বদলায় না; বিনিয়োগকারী 'ঘরে-তৈরি' লভ্যাংশ বানাতে পারেন", "বেশি লভ্যাংশ সবসময় মূল্য বাড়ায়", "কম লভ্যাংশ সবসময় মূল্য বাড়ায়", "প্রতিষ্ঠানকে সব আয় বিতরণ করতেই হবে"],
       "'হাতে-থাকা-পাখি' মত আর কর, সংকেত ও ক্লায়েন্টেল প্রভাব ব্যাখ্যা করে কেন বাস্তবে নীতি গুরুত্বপূর্ণ হতে পারে।"),
    _q("Lintner's study found that managers set dividends by…", ["Smoothing them - changing slowly towards a target payout and avoiding cuts", "Paying a fixed percentage of each year's profit", "Paying nothing in good years", "Changing them randomly"],
       "Because cuts are punished by the market, dividend increases signal confidence in lasting earnings.",
       "লিন্টনারের গবেষণায় দেখা যায় ব্যবস্থাপকরা লভ্যাংশ ঠিক করেন…", ["মসৃণ করে - লক্ষ্য-বিতরণের দিকে ধীরে বদলান আর কমানো এড়ান", "প্রতি বছরের মুনাফার নির্দিষ্ট শতাংশ দিয়ে", "ভালো বছরে কিছু না দিয়ে", "এলোমেলোভাবে বদলে"],
       "কমালে বাজার শাস্তি দেয়, তাই লভ্যাংশ বৃদ্ধি স্থায়ী আয়ের প্রতি আস্থার সংকেত দেয়।"),
    _q("Since April 2020, how are dividends from Indian companies taxed?", ["In the hands of shareholders at their slab rates (Dividend Distribution Tax was abolished)", "Only through Dividend Distribution Tax paid by the company", "They are fully tax-free", "At a flat 50%"],
       "Companies deduct TDS above a threshold; this changed the payout-versus-buyback choice for many firms.",
       "এপ্রিল 2020 থেকে ভারতীয় কোম্পানির লভ্যাংশে কীভাবে কর বসে?", ["শেয়ারহোল্ডারের হাতে তাঁদের স্ল্যাব হারে (লভ্যাংশ বণ্টন কর তুলে দেওয়া হয়েছে)", "কেবল কোম্পানির দেওয়া লভ্যাংশ বণ্টন করে", "সম্পূর্ণ করমুক্ত", "সমান 50% হারে"],
       "একটা সীমার ওপরে কোম্পানি উৎসে কর কাটে; এতে অনেক প্রতিষ্ঠানের লভ্যাংশ-বনাম-বাইব্যাক পছন্দ বদলেছে।"),
    _q("A firm's enterprise value equals…", ["Market value of equity + debt - cash", "Book value of equity only", "Sales x P/E ratio", "Total assets - total liabilities"],
       "EV is what an acquirer pays for the whole business; EV/EBITDA compares firms regardless of capital structure.",
       "একটা প্রতিষ্ঠানের এন্টারপ্রাইজ মূল্য সমান…", ["ইকুইটির বাজারমূল্য + ঋণ - নগদ", "কেবল ইকুইটির বইমূল্য", "বিক্রি x পি/ই অনুপাত", "মোট সম্পদ - মোট দায়"],
       "অধিগ্রহণকারী গোটা ব্যবসার জন্য যা দেন, তাই এন্টারপ্রাইজ মূল্য; ইভি/ইবিআইটিডিএ মূলধন-কাঠামো নির্বিশেষে প্রতিষ্ঠান তুলনা করে।"),
    _q("A company with a return on equity higher than its cost of equity should trade at…", ["A price-to-book ratio above 1", "A price-to-book ratio below 1", "Exactly its book value", "Zero"],
       "P/B = (ROE - g)/(rₑ - g) in a simple growth model: value is created only when ROE beats the required return.",
       "যে কোম্পানির ইকুইটি-আয় তার ইকুইটি-ব্যয়ের চেয়ে বেশি, তার দাম হওয়া উচিত…", ["দাম-বইমূল্য অনুপাত 1-এর ওপরে", "দাম-বইমূল্য অনুপাত 1-এর নিচে", "ঠিক বইমূল্যে", "শূন্য"],
       "সরল বৃদ্ধি-মডেলে P/B = (ROE - g)/(rₑ - g): ইকুইটি-আয় প্রত্যাশিত আয়কে ছাড়ালে তবেই মূল্য সৃষ্টি হয়।"),
    # ---------------------------------------------------------------- mergers and corporate actions
    _q("A cement maker buying a limestone mine is an example of…", ["Vertical integration (backward)", "Horizontal merger", "Conglomerate merger", "Demerger"],
       "Horizontal joins competitors; conglomerate joins unrelated businesses.",
       "একটা সিমেন্ট-প্রস্তুতকারক চুনাপাথরের খনি কিনলে তা কীসের উদাহরণ?", ["উল্লম্ব সংযুক্তি (পশ্চাৎমুখী)", "আনুভূমিক সংযুক্তি", "বহুমুখী সংযুক্তি", "বিভাজন"],
       "আনুভূমিক মানে প্রতিদ্বন্দ্বীদের মিলন; বহুমুখী মানে সম্পর্কহীন ব্যবসার মিলন।"),
    _q("In a leveraged buyout (LBO), the purchase of a company is financed mainly by…", ["Borrowed money secured on the target's own assets and cash flows", "Government grants", "Issuing new shares to the public", "The target's customers"],
       "High debt forces efficiency; private equity firms use LBOs and later sell or list the company.",
       "লিভারেজড বাইআউটে একটা কোম্পানি কেনার অর্থ মূলত আসে…", ["লক্ষ্য কোম্পানির নিজের সম্পদ আর নগদ প্রবাহের জামানতে ধার করা টাকা থেকে", "সরকারি অনুদান থেকে", "জনসাধারণকে নতুন শেয়ার দিয়ে", "লক্ষ্য কোম্পানির ক্রেতাদের থেকে"],
       "বেশি ঋণ দক্ষতা বাড়াতে বাধ্য করে; প্রাইভেট ইকুইটি প্রতিষ্ঠান এলবিও করে, পরে বিক্রি বা তালিকাভুক্ত করে।"),
    _q("A 'poison pill' is used by a company to…", ["Make a hostile takeover very expensive, e.g. by letting existing holders buy cheap new shares", "Reduce its taxes", "Pay a special dividend", "Merge with a competitor"],
       "Other defences include a 'white knight' (a friendly buyer) and staggered boards.",
       "কোম্পানি 'পয়জন পিল' ব্যবহার করে…", ["শত্রুতামূলক অধিগ্রহণকে খুব ব্যয়বহুল করতে, যেমন বর্তমান মালিকদের সস্তায় নতুন শেয়ার কিনতে দিয়ে", "কর কমাতে", "বিশেষ লভ্যাংশ দিতে", "প্রতিদ্বন্দ্বীর সঙ্গে মিশে যেতে"],
       "অন্য প্রতিরক্ষা: 'হোয়াইট নাইট' (বন্ধুভাবাপন্ন ক্রেতা) আর ধাপে ধাপে পরিচালক-নির্বাচন।"),
    _q("The swap ratio in a share-for-share merger tells…", ["How many acquirer shares each target shareholder gets per target share", "The interest rate on merger loans", "The tax rate after the merger", "How many employees are swapped"],
       "It is usually based on relative values (EPS, market price, book value or DCF) of the two companies.",
       "শেয়ার-বদলে-শেয়ার সংযুক্তিতে বিনিময় অনুপাত জানায়…", ["লক্ষ্য কোম্পানির প্রতি শেয়ারে সেখানকার শেয়ারহোল্ডার অধিগ্রহণকারীর কয়টি শেয়ার পান", "সংযুক্তি-ঋণের সুদের হার", "সংযুক্তির পরের করহার", "কতজন কর্মী বদল হয়"],
       "সাধারণত দুই কোম্পানির আপেক্ষিক মূল্যের (ইপিএস, বাজারদর, বইমূল্য বা ডিসিএফ) ওপর ভিত্তি করে।"),
    _q("In an Indian IPO, the 'green shoe' option lets the issuer…", ["Allot extra shares (up to 15%) to stabilise the price after listing", "Cancel the issue", "Pay dividends early", "Avoid SEBI rules"],
       "The stabilising agent buys back shares in the market if the price falls below the issue price.",
       "ভারতীয় আইপিও-তে 'গ্রিন শু' অপশন ইস্যুকারীকে দেয়…", ["তালিকাভুক্তির পরে দাম স্থির রাখতে বাড়তি শেয়ার (15% পর্যন্ত) বণ্টনের সুযোগ", "ইস্যু বাতিলের সুযোগ", "আগে লভ্যাংশ দেওয়ার সুযোগ", "সেবির নিয়ম এড়ানোর সুযোগ"],
       "দাম ইস্যু-দামের নিচে নামলে স্থিতিশীলকারী এজেন্ট বাজার থেকে শেয়ার কিনে নেয়।"),
    _q("Book building in an IPO means…", ["The price is discovered from bids received within a price band", "The company prints a book about itself", "Shares are sold only to employees", "The price is fixed by the government"],
       "ASBA lets the applicant's money stay blocked in their bank account until shares are allotted.",
       "আইপিও-তে বুক বিল্ডিং মানে…", ["একটা দামের পরিসরে পাওয়া দরপ্রস্তাব থেকে দাম নির্ধারিত হয়", "কোম্পানি নিজের সম্পর্কে বই ছাপায়", "কেবল কর্মীদের শেয়ার বিক্রি হয়", "সরকার দাম ঠিক করে"],
       "এএসবিএ-তে বণ্টন না হওয়া পর্যন্ত আবেদনকারীর টাকা তাঁর ব্যাংক অ্যাকাউন্টেই আটকে থাকে।"),
    _q("Before an IPO, a company files a detailed disclosure document with SEBI for public comments. It is the…", ["Draft red herring prospectus (DRHP)", "Annual report", "Balance sheet only", "Credit rating letter"],
       "It describes the business, risks, financials and use of funds; the final prospectus adds the price after book building.",
       "আইপিও-র আগে একটা কোম্পানি জনমতের জন্য সেবির কাছে বিশদ প্রকাশ-নথি জমা দেয়। এটা হল…", ["খসড়া রেড হেরিং প্রসপেক্টাস (ডিআরএইচপি)", "বার্ষিক প্রতিবেদন", "কেবল উদ্বৃত্তপত্র", "ক্রেডিট রেটিংয়ের চিঠি"],
       "এতে ব্যবসা, ঝুঁকি, আর্থিক বিবরণ আর অর্থের ব্যবহার থাকে; চূড়ান্ত প্রসপেক্টাসে বুক বিল্ডিংয়ের পরে দাম যোগ হয়।"),
    _q("When promoters delist a company from Indian exchanges, the exit price for public shareholders is found by…", ["Reverse book building, where shareholders bid the price at which they will sell", "A fixed price set by the promoter alone", "The RBI", "A lottery"],
       "The delisting succeeds only if enough shares are tendered at the discovered price (or a counter-offer is accepted).",
       "প্রোমোটাররা ভারতীয় এক্সচেঞ্জ থেকে কোম্পানির তালিকা সরালে সাধারণ শেয়ারহোল্ডারদের প্রস্থান-দাম ঠিক হয়…", ["বিপরীত বুক বিল্ডিংয়ে, যেখানে শেয়ারহোল্ডাররা যে দামে বেচবেন তার দর দেন", "কেবল প্রোমোটারের ঠিক করা স্থির দামে", "রিজার্ভ ব্যাংকের দ্বারা", "লটারিতে"],
       "নির্ধারিত দামে (বা পাল্টা প্রস্তাব গৃহীত হলে) যথেষ্ট শেয়ার জমা পড়লে তবেই তালিকা-প্রত্যাহার সফল হয়।"),
    _q("A qualified institutional placement (QIP) lets a listed Indian company…", ["Raise equity quickly by selling shares only to qualified institutional buyers", "Borrow from the RBI", "Delist its shares", "Issue bonus shares"],
       "It avoids the lengthy process of a public offer; pricing follows a SEBI formula based on recent market prices.",
       "যোগ্য প্রাতিষ্ঠানিক স্থাপন (কিউআইপি) একটা তালিকাভুক্ত ভারতীয় কোম্পানিকে দেয়…", ["কেবল যোগ্য প্রাতিষ্ঠানিক ক্রেতাদের শেয়ার বেচে দ্রুত ইকুইটি তোলার সুযোগ", "রিজার্ভ ব্যাংক থেকে ধারের সুযোগ", "শেয়ার তালিকা থেকে সরানোর সুযোগ", "বোনাস শেয়ার দেওয়ার সুযোগ"],
       "এতে গণপ্রস্তাবের দীর্ঘ প্রক্রিয়া এড়ানো যায়; সাম্প্রতিক বাজারদর-ভিত্তিক সেবির সূত্রে দাম ঠিক হয়।"),
    _q("Infrastructure investment trusts (InvITs) in India allow investors to…", ["Own units of completed infrastructure assets such as roads and power lines and receive most of their cash flows", "Lend directly to the government", "Trade commodity futures", "Buy gold in electronic form"],
       "They must distribute at least 90% of net distributable cash; REITs do the same for rent-earning real estate.",
       "ভারতে ইনফ্রাস্ট্রাকচার ইনভেস্টমেন্ট ট্রাস্ট (ইনভিট) বিনিয়োগকারীকে দেয়…", ["রাস্তা আর বিদ্যুৎ-লাইনের মতো সম্পূর্ণ পরিকাঠামো সম্পদের ইউনিট আর তার নগদ প্রবাহের বেশির ভাগ পাওয়ার সুযোগ", "সরাসরি সরকারকে ধার দেওয়ার সুযোগ", "পণ্য ফিউচার কেনাবেচার সুযোগ", "বৈদ্যুতিক রূপে সোনা কেনার সুযোগ"],
       "নিট বণ্টনযোগ্য নগদের অন্তত 90% বিতরণ করতে হয়; ভাড়া-আয়ের রিয়েল এস্টেটের জন্য রিট একই কাজ করে।"),
    # ---------------------------------------------------------------- fixed income
    _q("Bond convexity means that for a plain bond…", ["Prices rise more when yields fall than they drop when yields rise by the same amount", "Prices move in a straight line with yields", "Prices rise when yields rise", "Duration never changes"],
       "Duration is a linear estimate; convexity corrects it and is valuable to the holder.",
       "সাধারণ বন্ডে উত্তলতা মানে…", ["একই পরিমাণ আয় কমলে দাম যতটা বাড়ে, বাড়লে ততটা কমে না", "আয়ের সঙ্গে দাম সরলরেখায় চলে", "আয় বাড়লে দাম বাড়ে", "স্থিতিকাল কখনো বদলায় না"],
       "স্থিতিকাল একটা রৈখিক অনুমান; উত্তলতা তা সংশোধন করে আর মালিকের পক্ষে মূল্যবান।"),
    _q("What is the Macaulay duration of a zero-coupon bond?", ["Equal to its maturity", "Zero", "Half its maturity", "Always one year"],
       "All its cash comes at the end, so the weighted-average time of payment is the maturity itself.",
       "শূন্য-কুপন বন্ডের ম্যাকলে স্থিতিকাল কত?", ["এর মেয়াদের সমান", "শূন্য", "মেয়াদের অর্ধেক", "সবসময় এক বছর"],
       "সব টাকা শেষে আসে, তাই পরিশোধের ভারযুক্ত গড় সময় মেয়াদই।"),
    _q("A pension fund matches the duration of its bonds to the duration of its liabilities. This is…", ["Immunisation against interest-rate changes", "Speculation", "Arbitrage", "Diversification across countries"],
       "Price and reinvestment effects then offset each other for small parallel rate shifts.",
       "একটা পেনশন ফান্ড বন্ডের স্থিতিকালকে দায়ের স্থিতিকালের সঙ্গে মেলায়। এটা…", ["সুদের হার পরিবর্তনের বিরুদ্ধে প্রতিরোধীকরণ", "ফাটকা", "আর্বিট্রাজ", "দেশজুড়ে বৈচিত্র্যকরণ"],
       "তখন ছোট সমান্তরাল হার-পরিবর্তনে দাম আর পুনর্বিনিয়োগের প্রভাব পরস্পরকে বাতিল করে।"),
    _q("The liquidity preference theory explains why the yield curve usually slopes upward:", ["Investors want extra return (a term premium) for tying money up longer", "Long bonds are always safer", "The RBI fixes long rates higher", "Short bonds pay no interest"],
       "Pure expectations theory says long rates only reflect expected short rates; segmentation theory treats maturities as separate markets.",
       "তারল্য-পছন্দ তত্ত্ব ব্যাখ্যা করে কেন আয়-বক্ররেখা সাধারণত ঊর্ধ্বমুখী:", ["বেশি দিন টাকা আটকে রাখার জন্য বিনিয়োগকারী বাড়তি আয় (মেয়াদ-প্রিমিয়াম) চান", "দীর্ঘ বন্ড সবসময় বেশি নিরাপদ", "রিজার্ভ ব্যাংক দীর্ঘ হার বেশি ঠিক করে", "স্বল্প বন্ড সুদ দেয় না"],
       "বিশুদ্ধ প্রত্যাশা তত্ত্ব বলে দীর্ঘ হার কেবল প্রত্যাশিত স্বল্প হার প্রতিফলিত করে; বিভাজন তত্ত্ব মেয়াদগুলোকে আলাদা বাজার ধরে।"),
    _q("A floating-rate bond's price stays close to par because…", ["Its coupon resets to market rates at each reset date", "It has no credit risk", "It never matures", "It pays no interest"],
       "Its duration is only about the time to the next reset, so rate risk is small.",
       "ভাসমান-হারের বন্ডের দাম অভিহিত মূল্যের কাছাকাছি থাকে কারণ…", ["প্রতিটি পুনর্নির্ধারণ-তারিখে এর কুপন বাজার-হারে বদলায়", "এতে ঋণ-ঝুঁকি নেই", "এটা কখনো পরিপক্ব হয় না", "এটা সুদ দেয় না"],
       "এর স্থিতিকাল কেবল পরের পুনর্নির্ধারণ পর্যন্ত, তাই হার-ঝুঁকি কম।"),
    _q("Why does a callable bond show 'negative convexity' when yields fall low?", ["The issuer is likely to call it, capping how high its price can rise", "Its coupon falls", "It defaults", "Its maturity extends"],
       "Investors demand a higher yield for this call risk than on an otherwise identical straight bond.",
       "আয় অনেক কমলে কলযোগ্য বন্ডে 'ঋণাত্মক উত্তলতা' দেখা যায় কেন?", ["ইস্যুকারী সম্ভবত এটা ফেরত ডাকবেন, তাই দাম কতটা উঠতে পারে তার সীমা থাকে", "এর কুপন কমে", "এটা খেলাপি হয়", "এর মেয়াদ বাড়ে"],
       "এই কল-ঝুঁকির জন্য বিনিয়োগকারী একই রকম সাধারণ বন্ডের চেয়ে বেশি আয় চান।"),
    _q("The yield to maturity of a bond is the true return only if…", ["It is held to maturity, does not default, and coupons are reinvested at the same yield", "It is sold the next day", "Interest rates rise", "It is a zero-coupon bond held for one day"],
       "Reinvestment risk means realised returns often differ from the quoted YTM.",
       "একটা বন্ডের পরিপক্বতা-আয় প্রকৃত আয় হয় কেবল যদি…", ["মেয়াদ পর্যন্ত রাখা হয়, খেলাপি না হয়, আর কুপন একই আয়ে পুনর্বিনিয়োগ হয়", "পরের দিনই বিক্রি হয়", "সুদের হার বাড়ে", "এক দিনের জন্য রাখা শূন্য-কুপন বন্ড হয়"],
       "পুনর্বিনিয়োগ-ঝুঁকির কারণে বাস্তব আয় প্রায়ই ঘোষিত পরিপক্বতা-আয় থেকে আলাদা হয়।"),
    _q("Additional Tier-1 (AT1) bonds issued by banks carry high yields because…", ["They can be written down or converted to equity if the bank's capital falls too low", "They are guaranteed by the government", "They mature in one month", "They pay no coupon"],
       "Their perpetual, loss-absorbing nature was seen in the 2020 write-off of Yes Bank's AT1 bonds.",
       "ব্যাংকের অতিরিক্ত টিয়ার-1 (এটি1) বন্ডে আয় বেশি কারণ…", ["ব্যাংকের মূলধন খুব কমলে এগুলো মুছে ফেলা বা ইকুইটিতে বদলানো যায়", "সরকার এগুলোর জামিন", "এক মাসে পরিপক্ব হয়", "কোনো কুপন দেয় না"],
       "এদের চিরস্থায়ী, ক্ষতি-শোষী চরিত্র 2020-তে ইয়েস ব্যাংকের এটি1 বন্ড মুছে ফেলায় দেখা যায়।"),
    _q("A widening credit spread on a company's bonds over government securities signals…", ["The market sees higher default risk for that company", "Lower inflation", "The bond has become risk-free", "A stock split"],
       "Spreads also widen across the market in recessions, as investors flee to safe government paper.",
       "সরকারি ঋণপত্রের তুলনায় একটা কোম্পানির বন্ডে ঋণ-ব্যবধান বাড়লে সংকেত দেয়…", ["বাজার ওই কোম্পানির খেলাপি-ঝুঁকি বেশি দেখছে", "কম মুদ্রাস্ফীতি", "বন্ডটি ঝুঁকিহীন হয়েছে", "শেয়ার বিভাজন"],
       "মন্দায় পুরো বাজারেই ব্যবধান বাড়ে, কারণ বিনিয়োগকারী নিরাপদ সরকারি কাগজের দিকে ছোটেন।"),
    # ---------------------------------------------------------------- derivatives
    _q("The delta of a long call option always lies between…", ["0 and 1", "-1 and 0", "1 and 2", "-2 and -1"],
       "Delta is the change in option price per rupee change in the share; a deep in-the-money call has delta near 1, a put has delta between -1 and 0.",
       "লং কল অপশনের ডেল্টা সবসময় থাকে…", ["0 আর 1-এর মধ্যে", "-1 আর 0-এর মধ্যে", "1 আর 2-এর মধ্যে", "-2 আর -1-এর মধ্যে"],
       "শেয়ারের দাম এক টাকা বদলালে অপশনের দামের পরিবর্তন হল ডেল্টা; গভীর ইন-দ্য-মানি কলে প্রায় 1, পুটে -1 আর 0-এর মধ্যে।"),
    _q("For someone holding an option, theta (time decay) is usually…", ["Negative - the option loses value as expiry approaches, other things equal", "Positive", "Always zero", "Equal to delta"],
       "Time value shrinks to zero at expiry; option sellers collect this decay.",
       "অপশন-মালিকের জন্য থিটা (সময়-ক্ষয়) সাধারণত…", ["ঋণাত্মক - অন্য সব একই থাকলে মেয়াদ এগোলে অপশনের মূল্য কমে", "ধনাত্মক", "সবসময় শূন্য", "ডেল্টার সমান"],
       "মেয়াদশেষে সময়-মূল্য শূন্য হয়; অপশন বিক্রেতা এই ক্ষয় সংগ্রহ করেন।"),
    _q("When expected volatility of the share rises, the prices of both calls and puts…", ["Rise", "Fall", "Stay the same", "Become zero"],
       "Options gain from big moves but their losses are limited; this sensitivity is vega. India VIX reflects implied volatility of Nifty options.",
       "শেয়ারের প্রত্যাশিত অস্থিরতা বাড়লে কল আর পুট দুটোরই দাম…", ["বাড়ে", "কমে", "একই থাকে", "শূন্য হয়"],
       "বড় নড়াচড়ায় অপশন লাভ করে কিন্তু ক্ষতি সীমিত; এই সংবেদনশীলতাই ভেগা। ইন্ডিয়া ভিক্স নিফটি অপশনের নিহিত অস্থিরতা দেখায়।"),
    _q("Why is it never optimal to exercise an American call on a non-dividend-paying share before expiry?", ["Selling the call is worth more than exercising, because it keeps its time value", "Exercise is illegal before expiry", "The strike rises over time", "Dividends are paid to call holders"],
       "So its value equals the European call; early exercise of puts or of calls before a large dividend can be optimal.",
       "লভ্যাংশহীন শেয়ারে আমেরিকান কল মেয়াদের আগে প্রয়োগ করা কখনো সর্বোত্তম নয় কেন?", ["প্রয়োগের চেয়ে কল বিক্রি বেশি মূল্যবান, কারণ তাতে সময়-মূল্য থাকে", "মেয়াদের আগে প্রয়োগ বেআইনি", "সময়ের সঙ্গে স্ট্রাইক বাড়ে", "কল-মালিক লভ্যাংশ পান"],
       "তাই এর মূল্য ইউরোপীয় কলের সমান; পুটে বা বড় লভ্যাংশের আগে কলে আগাম প্রয়োগ সর্বোত্তম হতে পারে।"),
    _q("Holding a share and buying a put option on it creates…", ["A protective put - a floor under the value, like insurance", "A covered call", "A short straddle", "A naked call"],
       "A covered call (share + sold call) earns premium but caps the upside; a collar combines both.",
       "একটা শেয়ার রেখে তার ওপর পুট অপশন কিনলে তৈরি হয়…", ["সুরক্ষামূলক পুট - বিমার মতো মূল্যের নিচে একটা মেঝে", "কভার্ড কল", "শর্ট স্ট্র্যাডল", "নগ্ন কল"],
       "কভার্ড কল (শেয়ার + বিক্রি করা কল) প্রিমিয়াম আনে কিন্তু লাভের সীমা টানে; কলার দুটোকে মেলায়।"),
    _q("A bull call spread is built by…", ["Buying a call at a lower strike and selling a call at a higher strike", "Buying two puts", "Selling a call and a put at the same strike", "Buying a share and selling it short"],
       "It costs less than a single call but limits the maximum gain to the gap between strikes minus the net premium.",
       "বুল কল স্প্রেড তৈরি হয়…", ["কম স্ট্রাইকে একটা কল কিনে আর বেশি স্ট্রাইকে একটা কল বিক্রি করে", "দুটি পুট কিনে", "একই স্ট্রাইকে কল আর পুট বিক্রি করে", "শেয়ার কিনে আবার শর্ট বিক্রি করে"],
       "একটা কলের চেয়ে কম খরচ, কিন্তু সর্বোচ্চ লাভ স্ট্রাইকের ব্যবধান বাদ নিট প্রিমিয়ামে সীমিত।"),
    _q("Futures positions are 'marked to market' daily, which means…", ["Gains and losses are settled into the margin account every day", "The contract price is fixed and never compared with the market", "Only the final day matters", "The exchange buys the contract back daily"],
       "This, with initial margin, removes counterparty risk; a margin call follows when the balance falls below maintenance margin.",
       "ফিউচার অবস্থান প্রতিদিন 'বাজারদরে হিসাব' হয়, মানে…", ["প্রতিদিন লাভ-ক্ষতি মার্জিন অ্যাকাউন্টে মিটিয়ে দেওয়া হয়", "চুক্তির দাম স্থির থাকে, বাজারের সঙ্গে কখনো তুলনা হয় না", "কেবল শেষ দিন গোনে", "এক্সচেঞ্জ প্রতিদিন চুক্তি কিনে নেয়"],
       "প্রাথমিক মার্জিনের সঙ্গে এটা প্রতিপক্ষ-ঝুঁকি দূর করে; রক্ষণ-মার্জিনের নিচে নামলে মার্জিন কল আসে।"),
    _q("As a futures contract approaches expiry, its basis (spot price - futures price)…", ["Converges to zero", "Grows without limit", "Doubles", "Stays fixed"],
       "At expiry the futures must equal the spot price, or arbitrageurs would profit.",
       "ফিউচার চুক্তির মেয়াদ এগোলে এর ভিত্তি (স্পট দাম - ফিউচার দাম)…", ["শূন্যের দিকে মিলে যায়", "সীমাহীন বাড়ে", "দ্বিগুণ হয়", "স্থির থাকে"],
       "মেয়াদশেষে ফিউচারকে স্পট দামের সমান হতেই হয়, নইলে আর্বিট্রাজকারী লাভ করতেন।"),
    _q("For a non-dividend asset, the cost-of-carry model gives the futures price as…", ["F = S x e^(rT) - the spot price grown at the risk-free rate", "F = S - rT", "F = S ÷ (1 + r)", "F = S x T"],
       "If F is higher, sell futures and buy spot (cash-and-carry arbitrage); storage costs and dividends adjust the formula.",
       "লভ্যাংশহীন সম্পদের জন্য বহন-ব্যয় মডেল ফিউচার দাম দেয়…", ["F = S x e^(rT) - ঝুঁকিহীন হারে বাড়া স্পট দাম", "F = S - rT", "F = S ÷ (1 + r)", "F = S x T"],
       "F বেশি হলে ফিউচার বেচে স্পট কেনো (নগদ-ও-বহন আর্বিট্রাজ); মজুত খরচ আর লভ্যাংশ সূত্রটি সংশোধন করে।"),
    _q("A credit default swap (CDS) lets the buyer…", ["Pay a regular premium in return for compensation if a named borrower defaults", "Swap fixed interest for floating interest", "Exchange currencies", "Buy shares at a fixed price"],
       "CDS prices show the market's view of credit risk; they played a big part in the 2008 crisis.",
       "ক্রেডিট ডিফল্ট সোয়াপ (সিডিএস) ক্রেতাকে দেয়…", ["নিয়মিত প্রিমিয়ামের বিনিময়ে একজন নির্দিষ্ট ঋণগ্রহীতা খেলাপি হলে ক্ষতিপূরণ পাওয়ার সুযোগ", "স্থির সুদের বদলে ভাসমান সুদ", "মুদ্রা বিনিময়", "নির্দিষ্ট দামে শেয়ার কেনা"],
       "সিডিএস-এর দাম ঋণ-ঝুঁকি নিয়ে বাজারের মত দেখায়; 2008 সালের সংকটে এদের বড় ভূমিকা ছিল।"),
    _q("Which is a key assumption of the Black-Scholes model?", ["Share prices follow a lognormal path with constant volatility", "Volatility changes every day in a known way", "The share pays a large dividend each month", "Interest rates are zero"],
       "Real markets show a volatility 'smile', so traders quote implied volatilities that vary with strike.",
       "ব্ল্যাক-স্কোলস মডেলের একটা মূল অনুমান কোনটি?", ["শেয়ারদর স্থির অস্থিরতায় লগনর্মাল পথে চলে", "অস্থিরতা প্রতিদিন জানা উপায়ে বদলায়", "শেয়ার প্রতি মাসে বড় লভ্যাংশ দেয়", "সুদের হার শূন্য"],
       "বাস্তব বাজারে অস্থিরতার 'হাসি' দেখা যায়, তাই ব্যবসায়ীরা স্ট্রাইক অনুযায়ী আলাদা নিহিত অস্থিরতা দেন।"),
    _q("In a currency swap between an Indian and a US company, the parties exchange…", ["Principal and interest payments in two different currencies", "Only shares", "Commodities", "Credit ratings"],
       "Each borrows where it has an advantage and swaps, lowering costs and hedging long-term currency exposure.",
       "একটা ভারতীয় আর একটা আমেরিকান কোম্পানির মুদ্রা-সোয়াপে পক্ষেরা বিনিময় করে…", ["দুটি আলাদা মুদ্রায় আসল আর সুদের কিস্তি", "কেবল শেয়ার", "পণ্যদ্রব্য", "ক্রেডিট রেটিং"],
       "প্রত্যেকে যেখানে সুবিধা সেখানে ধার করে বদলে নেয়, খরচ কমে আর দীর্ঘমেয়াদি মুদ্রা-ঝুঁকি আড়াল হয়।"),
    # ---------------------------------------------------------------- portfolio theory and behaviour
    _q("The Security Market Line (SML) plots expected return against…", ["Beta (systematic risk)", "Total standard deviation", "Company size", "Dividend yield"],
       "The Capital Market Line uses total risk but only for efficient portfolios; shares above the SML are undervalued.",
       "সিকিউরিটি মার্কেট লাইন (এসএমএল) প্রত্যাশিত আয়কে কীসের সাপেক্ষে আঁকে?", ["বিটা (ব্যবস্থাগত ঝুঁকি)", "মোট সমক বিচ্যুতি", "কোম্পানির আকার", "লভ্যাংশ-আয়"],
       "ক্যাপিটাল মার্কেট লাইন মোট ঝুঁকি ব্যবহার করে কিন্তু কেবল দক্ষ পোর্টফোলিওর জন্য; এসএমএল-এর ওপরের শেয়ার অবমূল্যায়িত।"),
    _q("When is the Treynor ratio a better measure than the Sharpe ratio?", ["For a fund that is only one part of a well-diversified portfolio", "For an investor's entire wealth", "For a single bond", "Never"],
       "Treynor uses beta, which matters when unsystematic risk is diversified away elsewhere; Sharpe uses total risk.",
       "কখন ট্রেনর অনুপাত শার্প অনুপাতের চেয়ে ভালো মাপকাঠি?", ["যে ফান্ড একটা সুবৈচিত্র্যময় পোর্টফোলিওর কেবল একটা অংশ", "বিনিয়োগকারীর সমগ্র সম্পদের জন্য", "একটা একক বন্ডের জন্য", "কখনো নয়"],
       "ট্রেনর বিটা ব্যবহার করে, যা গুরুত্বপূর্ণ যখন অব্যবস্থাগত ঝুঁকি অন্যত্র বৈচিত্র্যে দূর হয়েছে; শার্প মোট ঝুঁকি ব্যবহার করে।"),
    _q("The Fama-French three-factor model adds which factors to the market factor?", ["Size (small minus big) and value (high minus low book-to-market)", "Inflation and GDP", "Momentum and liquidity", "Dividends and taxes"],
       "Small firms and value firms historically earned more than CAPM predicts; a four-factor version adds momentum.",
       "ফামা-ফ্রেঞ্চ তিন-উপাদান মডেল বাজার-উপাদানের সঙ্গে কোন উপাদান যোগ করে?", ["আকার (ছোট বাদ বড়) আর মূল্য (বেশি বাদ কম বই-বাজার অনুপাত)", "মুদ্রাস্ফীতি আর জিডিপি", "গতিবেগ আর তারল্য", "লভ্যাংশ আর কর"],
       "ছোট আর মূল্য-ধরনের প্রতিষ্ঠান ইতিহাসে সিএপিএম-এর অনুমানের চেয়ে বেশি আয় দিয়েছে; চার-উপাদান রূপে গতিবেগ যোগ হয়।"),
    _q("Arbitrage pricing theory (APT) differs from CAPM because it…", ["Allows several systematic risk factors instead of a single market factor", "Ignores risk", "Uses only the risk-free rate", "Requires options"],
       "Factors might include inflation, industrial output and interest-rate surprises.",
       "আর্বিট্রাজ প্রাইসিং তত্ত্ব (এপিটি) সিএপিএম থেকে আলাদা কারণ এটা…", ["একটা বাজার-উপাদানের বদলে কয়েকটি ব্যবস্থাগত ঝুঁকি-উপাদান মানে", "ঝুঁকি উপেক্ষা করে", "কেবল ঝুঁকিহীন হার ব্যবহার করে", "অপশন দাবি করে"],
       "উপাদান হতে পারে মুদ্রাস্ফীতি, শিল্প-উৎপাদন আর সুদের হারের আকস্মিক পরিবর্তন।"),
    _q("Two assets with a correlation of exactly -1 can be combined to…", ["Eliminate portfolio risk completely with the right weights", "Double the risk", "Remove all return", "Make beta equal to 2"],
       "Perfectly negative co-movement lets one asset's gains cancel the other's losses at every moment.",
       "ঠিক -1 সহসম্বন্ধের দুটি সম্পদ মিলিয়ে করা যায়…", ["সঠিক ভারে পোর্টফোলিওর ঝুঁকি সম্পূর্ণ দূর", "ঝুঁকি দ্বিগুণ", "সব আয় দূর", "বিটা 2 করা"],
       "পুরোপুরি বিপরীত চলাচলে প্রতি মুহূর্তে একটার লাভ অন্যটার ক্ষতি বাতিল করে।"),
    _q("Investors feeling the pain of a loss about twice as strongly as the joy of an equal gain is called…", ["Loss aversion (prospect theory)", "Overconfidence", "Anchoring", "Herding"],
       "Kahneman and Tversky's work also explains the disposition effect - selling winners too early and holding losers too long.",
       "সমান লাভের আনন্দের চেয়ে ক্ষতির কষ্ট প্রায় দ্বিগুণ তীব্র অনুভব করাকে বলে…", ["ক্ষতি-বিমুখতা (প্রসপেক্ট তত্ত্ব)", "অতি-আত্মবিশ্বাস", "নোঙর-প্রভাব", "পালের মনোভাব"],
       "কানেম্যান আর টভারস্কির কাজ নিষ্পত্তি-প্রভাবও ব্যাখ্যা করে - জেতাগুলো আগে বেচা আর হারাগুলো বেশি দিন রাখা।"),
    _q("Relying too heavily on a first number seen, such as a share's past high price, is…", ["Anchoring bias", "Diversification", "Arbitrage", "Hedging"],
       "Other common biases: confirmation bias (seeking agreeing news) and recency bias (overweighting recent events).",
       "প্রথম দেখা কোনো সংখ্যার ওপর বেশি নির্ভর করা, যেমন শেয়ারের অতীত উচ্চ দাম, হল…", ["নোঙর-পক্ষপাত", "বৈচিত্র্যকরণ", "আর্বিট্রাজ", "হেজিং"],
       "অন্য সাধারণ পক্ষপাত: নিশ্চিতকরণ-পক্ষপাত (সমর্থক খবর খোঁজা) আর সাম্প্রতিকতা-পক্ষপাত (সাম্প্রতিক ঘটনায় বেশি গুরুত্ব)।"),
    _q("A fund manager's information ratio measures…", ["Active return over the benchmark divided by tracking error", "Total return divided by beta", "Dividend yield", "Expense ratio"],
       "It shows how consistently a manager beats the index per unit of deviation from it.",
       "একজন ফান্ড-ব্যবস্থাপকের তথ্য অনুপাত মাপে…", ["মানদণ্ডের ওপর সক্রিয় আয় ভাগ ট্র্যাকিং ত্রুটি", "মোট আয় ভাগ বিটা", "লভ্যাংশ-আয়", "ব্যয়-অনুপাত"],
       "সূচক থেকে বিচ্যুতির প্রতি এককে ব্যবস্থাপক কতটা ধারাবাহিকভাবে সূচককে হারান, তা দেখায়।"),
    _q("Shares that did well over the past 3-12 months tend to keep doing well for a while. This anomaly is…", ["Momentum", "Mean reversion over decades", "The January effect only", "The risk-free rate"],
       "It challenges the weak-form efficient market hypothesis, which says past prices cannot predict future returns.",
       "গত 3-12 মাসে ভালো করা শেয়ার কিছু দিন ভালো করতে থাকে। এই ব্যতিক্রমকে বলে…", ["গতিবেগ (মোমেন্টাম)", "দশকজুড়ে গড়ে ফেরা", "কেবল জানুয়ারি প্রভাব", "ঝুঁকিহীন হার"],
       "এটা দুর্বল-রূপ দক্ষ বাজার প্রকল্পকে চ্যালেঞ্জ করে, যা বলে অতীত দাম ভবিষ্যৎ আয় বলতে পারে না।"),
    _q("A risk-free asset has a beta of…", ["0", "1", "-1", "Infinity"],
       "Its return does not move with the market; the market portfolio itself has a beta of exactly 1.",
       "ঝুঁকিহীন সম্পদের বিটা কত?", ["0", "1", "-1", "অসীম"],
       "এর আয় বাজারের সঙ্গে নড়ে না; বাজার-পোর্টফোলিওর নিজের বিটা ঠিক 1।"),
    # ---------------------------------------------------------------- risk management and banking
    _q("A major weakness of Value-at-Risk is that it…", ["Says nothing about how large losses can be beyond the VaR level", "Cannot be calculated", "Always overstates risk", "Ignores time"],
       "Expected shortfall (CVaR) averages the losses in the tail; stress tests examine extreme scenarios.",
       "ঝুঁকি-মূল্যের (ভিএআর) একটা বড় দুর্বলতা হল এটা…", ["ভিএআর স্তরের বাইরে ক্ষতি কত বড় হতে পারে, তা কিছুই বলে না", "গণনা করা যায় না", "সবসময় ঝুঁকি বাড়িয়ে দেখায়", "সময় উপেক্ষা করে"],
       "প্রত্যাশিত ঘাটতি (সিভিএআর) লেজের ক্ষতিগুলোর গড় নেয়; চাপ-পরীক্ষা চরম পরিস্থিতি দেখে।"),
    _q("Under Basel III as applied in India, banks must keep a minimum capital to risk-weighted assets ratio (CRAR) of about…", ["9% (11.5% including the capital conservation buffer)", "1%", "50%", "100%"],
       "RBI's minimum is higher than Basel's 8%; riskier loans carry higher risk weights and need more capital.",
       "ভারতে প্রযোজ্য ব্যাসেল III-এ ব্যাংককে ঝুঁকি-ভারযুক্ত সম্পদের তুলনায় ন্যূনতম মূলধন (সিআরএআর) রাখতে হয় প্রায়…", ["9% (মূলধন-সংরক্ষণ বাফারসহ 11.5%)", "1%", "50%", "100%"],
       "রিজার্ভ ব্যাংকের ন্যূনতম ব্যাসেলের 8%-এর চেয়ে বেশি; বেশি ঝুঁকির ঋণে ঝুঁকি-ভার বেশি, মূলধনও বেশি লাগে।"),
    _q("The liquidity coverage ratio (LCR) requires banks to hold enough high-quality liquid assets to survive…", ["30 days of stressed cash outflows", "One hour of withdrawals", "Ten years of losses", "One year of salaries only"],
       "The net stable funding ratio (NSFR) looks at funding stability over one year.",
       "তারল্য-আচ্ছাদন অনুপাত (এলসিআর) ব্যাংককে এত উচ্চমানের তরল সম্পদ রাখতে বলে যাতে টিকে থাকে…", ["চাপের সময়ে 30 দিনের নগদ বহিঃপ্রবাহে", "এক ঘণ্টার উত্তোলনে", "দশ বছরের ক্ষতিতে", "কেবল এক বছরের বেতনে"],
       "নিট স্থিতিশীল তহবিল অনুপাত (এনএসএফআর) এক বছরের তহবিল-স্থিতিশীলতা দেখে।"),
    _q("A bank funding long-term fixed-rate home loans with short-term deposits mainly faces…", ["Interest-rate (maturity mismatch) risk", "Currency risk", "Commodity risk", "No risk"],
       "If rates rise, deposit costs reset up quickly while loan income stays fixed - the asset-liability management problem.",
       "স্বল্পমেয়াদি আমানত দিয়ে দীর্ঘমেয়াদি স্থির-হারের গৃহঋণ দেওয়া ব্যাংক মূলত সম্মুখীন হয়…", ["সুদের হার (মেয়াদ-অমিল) ঝুঁকির", "মুদ্রা-ঝুঁকির", "পণ্য-ঝুঁকির", "কোনো ঝুঁকির নয়"],
       "হার বাড়লে আমানতের খরচ দ্রুত বাড়ে কিন্তু ঋণের আয় স্থির থাকে - সম্পদ-দায় ব্যবস্থাপনার সমস্যা।"),
    _q("India's Insolvency and Bankruptcy Code (2016) mainly aims to…", ["Resolve stressed companies in a time-bound way through the NCLT, maximising value for creditors", "Nationalise all companies", "Write off all bank loans", "Ban foreign investment"],
       "A committee of creditors runs the resolution process; liquidation follows if no plan is approved in time.",
       "ভারতের দেউলিয়া ও ঋণখেলাপি বিধির (2016) মূল লক্ষ্য…", ["এনসিএলটি-র মাধ্যমে সময়বদ্ধভাবে সংকটগ্রস্ত কোম্পানির সমাধান, ঋণদাতার জন্য সর্বোচ্চ মূল্য", "সব কোম্পানি জাতীয়করণ", "সব ব্যাংক-ঋণ মকুব", "বিদেশি বিনিয়োগ নিষেধ"],
       "ঋণদাতাদের কমিটি সমাধান-প্রক্রিয়া চালায়; সময়ে পরিকল্পনা অনুমোদিত না হলে অবসায়ন।"),
    _q("The SARFAESI Act allows Indian banks to…", ["Take possession of and sell secured assets of defaulters without going to court first", "Print money", "Set the repo rate", "List on stock exchanges"],
       "It also created asset reconstruction companies (ARCs) that buy bad loans from banks.",
       "সারফেসি আইন ভারতীয় ব্যাংককে দেয়…", ["আগে আদালতে না গিয়েই খেলাপির জামানত-সম্পদ দখল আর বিক্রির অধিকার", "টাকা ছাপানোর অধিকার", "রেপো হার ঠিক করার অধিকার", "শেয়ারবাজারে তালিকাভুক্তির অধিকার"],
       "এটা সম্পদ-পুনর্গঠন কোম্পানিও (এআরসি) তৈরি করে, যারা ব্যাংক থেকে খারাপ ঋণ কেনে।"),
    _q("Since 2019, most new floating-rate retail loans in India are linked to…", ["An external benchmark such as the RBI repo rate", "The bank's MCLR only", "The gold price", "The US Fed rate"],
       "External benchmarking passes policy-rate changes to borrowers faster than the internal MCLR system did.",
       "2019 থেকে ভারতে বেশির ভাগ নতুন ভাসমান-হারের খুচরো ঋণ কীসের সঙ্গে যুক্ত?", ["রিজার্ভ ব্যাংকের রেপো হারের মতো একটা বাহ্যিক মানদণ্ডের সঙ্গে", "কেবল ব্যাংকের এমসিএলআর-এর সঙ্গে", "সোনার দামের সঙ্গে", "আমেরিকার ফেড হারের সঙ্গে"],
       "বাহ্যিক মানদণ্ড অভ্যন্তরীণ এমসিএলআর ব্যবস্থার চেয়ে নীতি-হারের পরিবর্তন দ্রুত ঋণগ্রহীতার কাছে পৌঁছয়।"),
    _q("In the RBI's liquidity corridor, the floor and ceiling rates are…", ["The Standing Deposit Facility rate and the Marginal Standing Facility rate", "The CRR and SLR", "Inflation and GDP growth", "The bank rate and the savings rate"],
       "The repo rate sits in the middle; overnight market rates are kept inside this corridor.",
       "রিজার্ভ ব্যাংকের তারল্য-করিডরে মেঝে আর ছাদের হার হল…", ["স্থায়ী আমানত সুবিধা হার আর প্রান্তিক স্থায়ী সুবিধা হার", "সিআরআর আর এসএলআর", "মুদ্রাস্ফীতি আর জিডিপি বৃদ্ধি", "ব্যাংক হার আর সঞ্চয় হার"],
       "রেপো হার মাঝখানে থাকে; রাতারাতি বাজার-হার এই করিডরের মধ্যে রাখা হয়।"),
    _q("When the RBI buys government securities in open market operations, it…", ["Injects liquidity (money) into the banking system", "Withdraws liquidity", "Raises the CRR", "Devalues the rupee by decree"],
       "Selling securities does the opposite; OMOs are a key tool besides the repo rate.",
       "খোলা বাজার কার্যক্রমে রিজার্ভ ব্যাংক সরকারি ঋণপত্র কিনলে…", ["ব্যাংক-ব্যবস্থায় তারল্য (টাকা) ঢোকায়", "তারল্য তুলে নেয়", "সিআরআর বাড়ায়", "আদেশে রুপির অবমূল্যায়ন করে"],
       "ঋণপত্র বিক্রি উল্টো কাজ করে; রেপো হারের পাশাপাশি খোলা বাজার কার্যক্রম একটা প্রধান হাতিয়ার।"),
    _q("Under priority sector lending rules, Indian scheduled commercial banks must direct what share of adjusted net bank credit to sectors such as agriculture and small businesses?", ["40%", "4%", "75%", "100%"],
       "Sub-targets exist for agriculture and weaker sections; shortfalls go into funds such as RIDF.",
       "অগ্রাধিকার খাত ঋণের নিয়মে ভারতীয় তফসিলি বাণিজ্যিক ব্যাংককে সমন্বিত নিট ব্যাংক-ঋণের কত অংশ কৃষি আর ক্ষুদ্র ব্যবসার মতো খাতে দিতে হয়?", ["40%", "4%", "75%", "100%"],
       "কৃষি আর দুর্বল শ্রেণির জন্য উপ-লক্ষ্য আছে; ঘাটতি আরআইডিএফ-এর মতো তহবিলে যায়।"),
    # ---------------------------------------------------------------- international finance
    _q("Covered interest rate parity says the forward premium on a currency equals…", ["The interest-rate difference between the two countries", "The inflation rate in one country", "The trade deficit", "Zero always"],
       "If not, borrowing in one currency and investing in the other with a forward cover gives riskless profit.",
       "আচ্ছাদিত সুদের হার সমতা বলে একটা মুদ্রার অগ্রিম প্রিমিয়াম সমান…", ["দুই দেশের সুদের হারের পার্থক্য", "এক দেশের মুদ্রাস্ফীতি", "বাণিজ্য-ঘাটতি", "সবসময় শূন্য"],
       "না হলে এক মুদ্রায় ধার করে অন্যটায় অগ্রিম আচ্ছাদনসহ বিনিয়োগে ঝুঁকিহীন লাভ হত।"),
    _q("A change in the rupee's value that alters the rupee worth of a firm's future competitive cash flows is…", ["Economic (operating) exposure", "Translation exposure", "Transaction exposure", "Credit exposure"],
       "Transaction exposure covers specific contracted payments; translation exposure affects consolidated accounts of foreign subsidiaries.",
       "রুপির মূল্যের পরিবর্তন যখন প্রতিষ্ঠানের ভবিষ্যৎ প্রতিযোগিতামূলক নগদ প্রবাহের রুপি-মূল্য বদলায়, তা হল…", ["অর্থনৈতিক (পরিচালন) ঝুঁকি", "রূপান্তর ঝুঁকি", "লেনদেন ঝুঁকি", "ঋণ ঝুঁকি"],
       "লেনদেন ঝুঁকি নির্দিষ্ট চুক্তিবদ্ধ পরিশোধে; রূপান্তর ঝুঁকি বিদেশি সহায়ক কোম্পানির একত্রিত হিসাবে প্রভাব ফেলে।"),
    _q("An Indian IT company earning dollars borrows in dollars too. This is…", ["A natural hedge", "Speculation", "Transfer pricing", "Dumping"],
       "Dollar revenues service dollar debt, so exchange-rate moves largely cancel out.",
       "ডলার আয় করা একটা ভারতীয় আইটি কোম্পানি ডলারেই ধার নেয়। এটা…", ["স্বাভাবিক হেজ", "ফাটকা", "স্থানান্তর-মূল্য নির্ধারণ", "ডাম্পিং"],
       "ডলার আয় দিয়ে ডলার ঋণ শোধ হয়, তাই বিনিময় হারের ওঠানামা মোটামুটি কাটাকাটি হয়।"),
    _q("Masala bonds are…", ["Rupee-denominated bonds issued by Indian entities to overseas investors", "Bonds issued by spice companies only", "Dollar bonds issued in India", "Gold-backed bonds"],
       "The foreign investor, not the Indian issuer, bears the currency risk.",
       "মশলা বন্ড হল…", ["বিদেশি বিনিয়োগকারীদের কাছে ভারতীয় প্রতিষ্ঠানের ইস্যু করা রুপি-মূল্যের বন্ড", "কেবল মশলা কোম্পানির ইস্যু করা বন্ড", "ভারতে ইস্যু করা ডলার বন্ড", "সোনা-সমর্থিত বন্ড"],
       "মুদ্রা-ঝুঁকি বহন করেন বিদেশি বিনিয়োগকারী, ভারতীয় ইস্যুকারী নন।"),
    _q("How does foreign direct investment (FDI) differ from foreign portfolio investment (FPI)?", ["FDI brings a lasting stake with management influence (usually 10% or more); FPI is a smaller, easily sold holding", "FDI is only in bonds", "FPI is always larger", "There is no difference"],
       "FPI flows are 'hot money' that can leave quickly, making markets and the rupee volatile.",
       "প্রত্যক্ষ বিদেশি বিনিয়োগ (এফডিআই) আর বিদেশি পোর্টফোলিও বিনিয়োগের (এফপিআই) পার্থক্য কী?", ["এফডিআই ব্যবস্থাপনায় প্রভাবসহ দীর্ঘস্থায়ী অংশীদারি আনে (সাধারণত 10% বা বেশি); এফপিআই ছোট, সহজে বিক্রয়যোগ্য অংশ", "এফডিআই কেবল বন্ডে", "এফপিআই সবসময় বড়", "কোনো পার্থক্য নেই"],
       "এফপিআই প্রবাহ 'গরম টাকা', দ্রুত চলে যেতে পারে, বাজার আর রুপিকে অস্থির করে।"),
    _q("The Indian rupee is currently…", ["Fully convertible on the current account but only partly on the capital account", "Fully convertible on both accounts", "Not convertible at all", "Pegged to gold"],
       "Trade and travel payments are free; capital flows face limits such as the Liberalised Remittance Scheme cap.",
       "ভারতীয় রুপি বর্তমানে…", ["চলতি খাতে পুরোপুরি রূপান্তরযোগ্য কিন্তু মূলধনী খাতে আংশিক", "দুই খাতেই পুরোপুরি রূপান্তরযোগ্য", "একেবারেই রূপান্তরযোগ্য নয়", "সোনার সঙ্গে বাঁধা"],
       "বাণিজ্য আর ভ্রমণের পরিশোধ মুক্ত; মূলধনী প্রবাহে উদারীকৃত প্রেরণ প্রকল্পের সীমার মতো বাধা আছে।"),
    _q("External commercial borrowings (ECBs) allow Indian firms to…", ["Borrow from foreign lenders within RBI rules on purpose, maturity and cost", "Borrow only from Indian banks", "Avoid all currency risk", "Issue shares abroad without approval"],
       "Unhedged foreign-currency debt can become very costly if the rupee weakens sharply.",
       "বাহ্যিক বাণিজ্যিক ঋণ (ইসিবি) ভারতীয় প্রতিষ্ঠানকে দেয়…", ["উদ্দেশ্য, মেয়াদ আর খরচ নিয়ে রিজার্ভ ব্যাংকের নিয়মের মধ্যে বিদেশি ঋণদাতা থেকে ধারের সুযোগ", "কেবল ভারতীয় ব্যাংক থেকে ধারের সুযোগ", "সব মুদ্রা-ঝুঁকি এড়ানোর সুযোগ", "অনুমোদন ছাড়া বিদেশে শেয়ার ছাড়ার সুযোগ"],
       "রুপি খুব দুর্বল হলে আড়ালহীন বিদেশি-মুদ্রার ঋণ খুব ব্যয়বহুল হতে পারে।"),
    _q("GIFT City's International Financial Services Centre (IFSC) in Gujarat was set up to…", ["Offer global financial services from Indian soil, under a single regulator (IFSCA)", "Grow cotton", "Host the RBI headquarters", "Mint coins"],
       "It aims to bring back offshore business in rupee derivatives, aircraft leasing, banking and fund management.",
       "গুজরাটের গিফট সিটির আন্তর্জাতিক আর্থিক পরিষেবা কেন্দ্র (আইএফএসসি) তৈরি হয়…", ["এক নিয়ন্ত্রকের (আইএফএসসিএ) অধীনে ভারতের মাটি থেকে বিশ্ব-আর্থিক পরিষেবা দিতে", "তুলো চাষ করতে", "রিজার্ভ ব্যাংকের সদর দপ্তর রাখতে", "মুদ্রা ছাপাতে"],
       "রুপি ডেরিভেটিভ, বিমান লিজ, ব্যাংকিং আর তহবিল-ব্যবস্থাপনার বিদেশি ব্যবসা দেশে ফেরানো এর লক্ষ্য।"),
    # ---------------------------------------------------------------- Indian markets and governance
    _q("India moved its equity market settlement cycle to T+1 in 2023. This means…", ["Trades are settled (shares and money exchanged) one working day after the trade", "Trades settle one year later", "Only one trade a day is allowed", "Prices change once a day"],
       "Faster settlement reduces counterparty risk and frees up capital; India was among the first major markets to do so.",
       "2023-এ ভারত শেয়ারবাজারের নিষ্পত্তি-চক্র T+1 করে। এর মানে…", ["লেনদেনের এক কার্যদিবস পরে নিষ্পত্তি হয় (শেয়ার আর টাকা হাতবদল)", "এক বছর পরে নিষ্পত্তি", "দিনে কেবল একটা লেনদেন", "দিনে একবার দাম বদলায়"],
       "দ্রুত নিষ্পত্তি প্রতিপক্ষ-ঝুঁকি কমায় আর মূলধন মুক্ত করে; প্রধান বাজারগুলোর মধ্যে ভারত প্রথম দিকে এটা করে।"),
    _q("Market-wide circuit breakers on Indian exchanges…", ["Halt trading for a while when the index falls by 10%, 15% or 20%", "Stop trading on holidays only", "Fix share prices permanently", "Control electricity at the exchange"],
       "They give investors time to absorb information during panic; individual shares also have price bands.",
       "ভারতীয় এক্সচেঞ্জের বাজার-ব্যাপী সার্কিট ব্রেকার…", ["সূচক 10%, 15% বা 20% পড়লে কিছুক্ষণ লেনদেন থামায়", "কেবল ছুটির দিনে লেনদেন থামায়", "শেয়ারদর স্থায়ীভাবে বেঁধে দেয়", "এক্সচেঞ্জের বিদ্যুৎ নিয়ন্ত্রণ করে"],
       "আতঙ্কের সময় বিনিয়োগকারী তথ্য বুঝে নেওয়ার সময় পান; আলাদা শেয়ারেরও দামের সীমা থাকে।"),
    _q("Under the Companies Act 2013, profitable companies above a size threshold must spend at least what share of average net profit on CSR?", ["2%", "0.2%", "20%", "50%"],
       "Section 135 applies to companies meeting net worth, turnover or profit thresholds; unspent amounts go to specified funds.",
       "কোম্পানি আইন 2013 অনুযায়ী একটা সীমার ওপরের লাভজনক কোম্পানিকে গড় নিট মুনাফার অন্তত কত অংশ সিএসআর-এ খরচ করতে হয়?", ["2%", "0.2%", "20%", "50%"],
       "ধারা 135 নিট মূল্য, লেনদেন বা মুনাফার সীমা পেরোনো কোম্পানির ক্ষেত্রে প্রযোজ্য; খরচ না হওয়া অর্থ নির্দিষ্ট তহবিলে যায়।"),
    _q("Independent directors on a company board mainly exist to…", ["Protect minority shareholders by giving unbiased oversight of management", "Run daily operations", "Sell the company's products", "Audit the accounts themselves"],
       "Listed Indian companies must have audit committees with a majority of independent directors.",
       "কোম্পানির পরিচালক-পর্ষদে স্বাধীন পরিচালক মূলত থাকেন…", ["ব্যবস্থাপনার নিরপেক্ষ তদারকি করে সংখ্যালঘু শেয়ারহোল্ডারদের রক্ষা করতে", "দৈনন্দিন কাজ চালাতে", "কোম্পানির পণ্য বিক্রি করতে", "নিজেরাই হিসাব নিরীক্ষা করতে"],
       "তালিকাভুক্ত ভারতীয় কোম্পানির নিরীক্ষা কমিটিতে সংখ্যাগরিষ্ঠ স্বাধীন পরিচালক থাকতে হয়।"),
    _q("Equity-linked savings schemes (ELSS) mutual funds in India are popular because they…", ["Give a tax deduction under Section 80C with the shortest lock-in (3 years) among such options", "Guarantee returns", "Invest only in gold", "Have no market risk"],
       "Their returns depend on the share market; PPF and tax-saving FDs have longer lock-ins.",
       "ভারতে ইকুইটি-যুক্ত সঞ্চয় প্রকল্প (ইএলএসএস) মিউচুয়াল ফান্ড জনপ্রিয় কারণ এরা…", ["ধারা 80C-তে কর-ছাড় দেয়, এমন বিকল্পের মধ্যে সবচেয়ে কম লক-ইনে (3 বছর)", "নিশ্চিত আয় দেয়", "কেবল সোনায় বিনিয়োগ করে", "বাজার-ঝুঁকিহীন"],
       "আয় শেয়ারবাজারের ওপর নির্ভর করে; পিপিএফ আর কর-সাশ্রয়ী এফডি-র লক-ইন বেশি।"),
    _q("A mutual fund's expense ratio matters to long-term investors because…", ["It is deducted every year and compounds into a large gap in final wealth", "It is paid only once", "It increases returns", "It is refunded at the end"],
       "Direct plans have lower expense ratios than regular plans because no distributor commission is paid.",
       "দীর্ঘমেয়াদি বিনিয়োগকারীর কাছে মিউচুয়াল ফান্ডের ব্যয়-অনুপাত গুরুত্বপূর্ণ কারণ…", ["এটা প্রতি বছর কাটা হয় আর চক্রবৃদ্ধিতে শেষ সম্পদে বড় ফারাক তৈরি করে", "এটা কেবল একবার দিতে হয়", "এটা আয় বাড়ায়", "শেষে এটা ফেরত দেওয়া হয়"],
       "ডিরেক্ট প্ল্যানে বিতরণকারীর কমিশন নেই, তাই রেগুলার প্ল্যানের চেয়ে ব্যয়-অনুপাত কম।"),
    _q("UPI transformed Indian payments mainly because it…", ["Allows instant, low-cost bank-to-bank transfers through a mobile app using a simple address", "Requires a credit card", "Works only in banks", "Charges high fees on every payment"],
       "Run by NPCI, it handles billions of transactions a month and supports small merchants through QR codes.",
       "ইউপিআই ভারতের লেনদেনে বিপ্লব এনেছে মূলত কারণ এটা…", ["সরল ঠিকানা দিয়ে মোবাইল অ্যাপে তাৎক্ষণিক, কম খরচের ব্যাংক-থেকে-ব্যাংক স্থানান্তর দেয়", "ক্রেডিট কার্ড দাবি করে", "কেবল ব্যাংকে কাজ করে", "প্রতিটি লেনদেনে বেশি মাশুল নেয়"],
       "এনপিসিআই পরিচালিত এই ব্যবস্থা মাসে শত শত কোটি লেনদেন সামলায় আর কিউআর কোডে ছোট ব্যবসায়ীদের সাহায্য করে।"),
    _q("A credit score such as CIBIL's mainly reflects…", ["A borrower's record of repaying loans and credit cards on time", "Their salary only", "Their age", "The value of their house"],
       "Missed payments and very high use of credit limits lower the score; lenders use it to price and approve loans.",
       "সিবিল-এর মতো ক্রেডিট স্কোর মূলত প্রতিফলিত করে…", ["ঋণগ্রহীতার সময়মতো ঋণ আর ক্রেডিট কার্ড শোধের রেকর্ড", "কেবল তাঁর বেতন", "তাঁর বয়স", "তাঁর বাড়ির মূল্য"],
       "কিস্তি বাদ পড়া আর ঋণসীমার খুব বেশি ব্যবহার স্কোর কমায়; ঋণদাতা এটা দিয়ে ঋণের দাম আর অনুমোদন ঠিক করেন।"),
    # ---------------------------------------------------------------- working capital and treasury
    _q("Financing permanent working capital with short-term loans is a working-capital policy that is…", ["Aggressive - cheaper but riskier because loans must be rolled over", "Conservative", "Risk-free", "Illegal"],
       "A conservative policy uses long-term funds even for some temporary needs: safer but costlier.",
       "স্থায়ী কার্যকর মূলধনে স্বল্পমেয়াদি ঋণ দিয়ে অর্থ জোগানো কার্যকর-মূলধন নীতি হল…", ["আক্রমণাত্মক - সস্তা কিন্তু বেশি ঝুঁকিপূর্ণ, কারণ ঋণ বারবার নবীকরণ করতে হয়", "রক্ষণশীল", "ঝুঁকিহীন", "বেআইনি"],
       "রক্ষণশীল নীতি কিছু অস্থায়ী প্রয়োজনেও দীর্ঘমেয়াদি তহবিল ব্যবহার করে: নিরাপদ কিন্তু ব্যয়বহুল।"),
    _q("A supplier offers terms of '2/10 net 30'. Skipping the discount and paying on day 30 costs roughly…", ["About 37% a year", "2% a year", "10% a year", "Nothing"],
       "Paying 2% more to keep money 20 extra days: (2/98) x (365/20) ≈ 37.2% - usually cheaper to borrow and take the discount.",
       "একজন সরবরাহকারী '2/10 নেট 30' শর্ত দেন। ছাড় না নিয়ে 30 দিনে দিলে খরচ মোটামুটি…", ["বছরে প্রায় 37%", "বছরে 2%", "বছরে 10%", "কিছুই নয়"],
       "বাড়তি 20 দিন টাকা রাখতে 2% বেশি দেওয়া: (2/98) x (365/20) ≈ 37.2% - সাধারণত ধার করে ছাড় নেওয়াই সস্তা।"),
    _q("Commercial paper in India is…", ["A short-term unsecured promissory note issued by highly rated companies", "A long-term secured bond", "A type of share", "A government currency note"],
       "Maturities run from 7 days to a year; it is usually cheaper than bank loans for top-rated firms.",
       "ভারতে কমার্শিয়াল পেপার হল…", ["উচ্চ রেটিংয়ের কোম্পানির ইস্যু করা স্বল্পমেয়াদি জামানতহীন প্রতিশ্রুতিপত্র", "দীর্ঘমেয়াদি জামানতযুক্ত বন্ড", "এক ধরনের শেয়ার", "সরকারি কাগুজে মুদ্রা"],
       "মেয়াদ 7 দিন থেকে এক বছর; সেরা রেটিংয়ের প্রতিষ্ঠানের জন্য সাধারণত ব্যাংক-ঋণের চেয়ে সস্তা।"),
    _q("ABC analysis in inventory management means…", ["Controlling the few high-value items (A) most tightly and the many low-value items (C) loosely", "Ordering items alphabetically", "Buying only from three suppliers", "Counting stock once a year"],
       "Often about 10-20% of items make up 70-80% of inventory value - a Pareto pattern.",
       "মজুত-ব্যবস্থাপনায় এবিসি বিশ্লেষণ মানে…", ["অল্প কয়েকটি উচ্চমূল্যের সামগ্রী (A) সবচেয়ে কড়াভাবে আর অনেক কমমূল্যের (C) শিথিলভাবে নিয়ন্ত্রণ", "বর্ণানুক্রমে সামগ্রী অর্ডার", "কেবল তিনজন সরবরাহকারী থেকে কেনা", "বছরে একবার মজুত গোনা"],
       "প্রায়ই 10-20% সামগ্রী মজুতের মূল্যের 70-80% - এক প্যারেটো ধরন।"),
    _q("The Miller-Orr cash management model sets…", ["Upper and lower cash limits with a return point, reacting only when cash hits a limit", "A fixed daily cash balance", "Zero cash at all times", "Cash equal to sales"],
       "It suits firms with random cash flows; the Baumol model treats cash like inventory with steady use.",
       "মিলার-অর নগদ-ব্যবস্থাপনা মডেল ঠিক করে…", ["ফেরার বিন্দুসহ নগদের ঊর্ধ্ব আর নিম্ন সীমা, নগদ সীমা ছুঁলে তবেই পদক্ষেপ", "দৈনিক নির্দিষ্ট নগদ", "সবসময় শূন্য নগদ", "বিক্রির সমান নগদ"],
       "এলোমেলো নগদ প্রবাহের প্রতিষ্ঠানের জন্য উপযুক্ত; বাউমল মডেল নগদকে স্থির ব্যবহারের মজুতের মতো ধরে।"),
    _q("Just-in-time (JIT) inventory reduces working capital by…", ["Receiving materials only as production needs them", "Buying a year's stock at once", "Holding extra safety stock", "Selling on long credit"],
       "It needs reliable suppliers; disruptions (as in 2020-21) showed its risks.",
       "জাস্ট-ইন-টাইম (জেআইটি) মজুত কার্যকর মূলধন কমায়…", ["উৎপাদনের যখন যা দরকার কেবল তখনই উপকরণ এনে", "একবারে এক বছরের মজুত কিনে", "বাড়তি নিরাপত্তা-মজুত রেখে", "দীর্ঘ ধারে বিক্রি করে"],
       "নির্ভরযোগ্য সরবরাহকারী লাগে; ব্যাঘাত (যেমন 2020-21-এ) এর ঝুঁকি দেখিয়েছে।"),
    _q("Why does a company with high operating leverage feel a recession more sharply?", ["Its large fixed costs stay while revenue falls, so profit drops faster than sales", "Its variable costs rise", "It pays no interest", "Its taxes double"],
       "The same fixed-cost structure makes profits rise faster than sales in good times.",
       "বেশি পরিচালন-লিভারেজের কোম্পানি মন্দা বেশি তীব্রভাবে টের পায় কেন?", ["আয় কমলেও বড় স্থির খরচ থেকে যায়, তাই মুনাফা বিক্রির চেয়ে দ্রুত পড়ে", "এর পরিবর্তনশীল খরচ বাড়ে", "এটা সুদ দেয় না", "এর কর দ্বিগুণ হয়"],
       "একই স্থির-খরচ কাঠামো ভালো সময়ে মুনাফাকে বিক্রির চেয়ে দ্রুত বাড়ায়।"),
    _q("A company reports rising profits but negative operating cash flow for several years. An analyst should…", ["Check for aggressive revenue recognition or ballooning receivables and inventory", "Ignore it, since profit is what matters", "Assume taxes are wrong", "Buy more shares immediately"],
       "Quality of earnings: cash flow is harder to manipulate than accounting profit.",
       "একটা কোম্পানি কয়েক বছর ধরে বাড়তি মুনাফা দেখায় কিন্তু পরিচালন নগদ প্রবাহ ঋণাত্মক। বিশ্লেষকের উচিত…", ["আক্রমণাত্মক আয়-স্বীকৃতি বা ফুলে ওঠা পাওনা আর মজুত খতিয়ে দেখা", "উপেক্ষা করা, মুনাফাই আসল", "ধরে নেওয়া কর ভুল", "তখনই আরও শেয়ার কেনা"],
       "আয়ের গুণমান: হিসাবের মুনাফার চেয়ে নগদ প্রবাহ কারসাজি করা কঠিন।"),
    _q("Interest coverage and debt-to-EBITDA are typical loan covenants. If a borrower breaches them, the lender can usually…", ["Demand early repayment, raise the rate or impose new conditions", "Do nothing at all", "Take over the government", "Cancel the borrower's taxes"],
       "Covenants protect lenders against the agency costs of debt by giving early warning and control rights.",
       "সুদ-আচ্ছাদন আর ঋণ-ইবিআইটিডিএ সাধারণ ঋণ-শর্ত। ঋণগ্রহীতা তা ভাঙলে ঋণদাতা সাধারণত পারেন…", ["আগাম পরিশোধ দাবি, হার বাড়ানো বা নতুন শর্ত চাপাতে", "কিছুই না করতে", "সরকার দখল করতে", "ঋণগ্রহীতার কর বাতিল করতে"],
       "শর্তগুলো আগাম সতর্কতা আর নিয়ন্ত্রণের অধিকার দিয়ে ঋণদাতাকে ঋণের এজেন্সি খরচ থেকে রক্ষা করে।"),
    _q("Which statement about stock dividends (bonus shares) is correct?", ["They move reserves into share capital without changing total shareholder value", "They pay cash to shareholders", "They increase the company's assets", "They double the firm's value"],
       "The share price adjusts down in proportion; they can signal confidence and improve liquidity.",
       "শেয়ার-লভ্যাংশ (বোনাস শেয়ার) সম্পর্কে কোন বিবৃতি সঠিক?", ["মোট শেয়ারহোল্ডার-মূল্য না বদলে সঞ্চিতি থেকে শেয়ার-মূলধনে সরায়", "শেয়ারহোল্ডারকে নগদ দেয়", "কোম্পানির সম্পদ বাড়ায়", "প্রতিষ্ঠানের মূল্য দ্বিগুণ করে"],
       "শেয়ারদর আনুপাতিক হারে কমে; এগুলো আস্থার সংকেত দিতে আর তারল্য বাড়াতে পারে।"),
    _q("Which is the main advantage of an index fund over an actively managed fund?", ["Very low costs, with returns that closely match the market", "Guaranteed higher returns", "No market risk", "Daily dividends"],
       "Most active funds fail to beat their benchmark after fees over long periods.",
       "সক্রিয়ভাবে পরিচালিত ফান্ডের তুলনায় ইনডেক্স ফান্ডের মূল সুবিধা কী?", ["খুব কম খরচ, আর আয় বাজারের সঙ্গে প্রায় মেলে", "নিশ্চিত বেশি আয়", "বাজার-ঝুঁকিহীন", "দৈনিক লভ্যাংশ"],
       "দীর্ঘ সময়ে মাশুল বাদ দিয়ে বেশির ভাগ সক্রিয় ফান্ড মানদণ্ডকে হারাতে পারে না।"),
    _q("The National Pension System (NPS) is described as 'market-linked' because…", ["Contributions are invested in equity, corporate bonds and government securities chosen by the subscriber", "It pays a fixed government pension", "It invests only in bank deposits", "It cannot be withdrawn"],
       "At retirement part can be withdrawn and part must buy an annuity; costs are among the lowest in India.",
       "জাতীয় পেনশন ব্যবস্থাকে (এনপিএস) 'বাজার-যুক্ত' বলা হয় কারণ…", ["অবদান গ্রাহকের বাছাই করা ইকুইটি, কর্পোরেট বন্ড আর সরকারি ঋণপত্রে বিনিয়োগ হয়", "এটা সরকারের স্থির পেনশন দেয়", "কেবল ব্যাংক-আমানতে বিনিয়োগ করে", "কখনো তোলা যায় না"],
       "অবসরে কিছু অংশ তোলা যায় আর কিছু দিয়ে বার্ষিকী কিনতে হয়; খরচ ভারতে সবচেয়ে কমগুলোর মধ্যে।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
