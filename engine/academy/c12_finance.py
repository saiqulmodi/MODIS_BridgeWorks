"""Class 12 - Finance (Chief Engineer): net present value, payback, benefit-cost ratio and the
profitability index, real versus nominal rates, straight-line and written-down depreciation,
sinking funds, bond pricing, CAPM, equivalent annual cost, the principal and interest in an EMI,
cost escalation, currency risk, break-even traffic, IRR, and the contract and risk tools used to
finance large bridges."""
from . import mcq


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def _o(r, *alts):
    out = []
    for x in (r, *alts, _c(r + 1), _c(r * 2), _c(r + 10), _c(r + 20)):
        x = _c(x)
        if x not in out:
            out.append(x)
    return out[:4]


def _f(x):
    return f"{x:,}" if isinstance(x, int) else f"{x:,.2f}".rstrip("0").rstrip(".")


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, pre_en="", u_en="", u_bn=""):
    o = _o(r, *alts)
    return mcq(q_en, [f"{pre_en}{_f(x)}{u_en}" for x in o], 0, ex_en, q_bn, [f"{_f(x)}{u_bn}" for x in o], ex_bn)


def _crore(q_en, q_bn, r, ex_en, ex_bn, alts):
    return _n(q_en, q_bn, r, ex_en, ex_bn, alts, "Rs ", " crore", " কোটি টাকা")


def _lakh(q_en, q_bn, r, ex_en, ex_bn, alts):
    return _n(q_en, q_bn, r, ex_en, ex_bn, alts, "Rs ", " lakh", " লাখ টাকা")


def npv(c0, cfs, rate, what_en, what_bn):
    pv = sum(cf / (1 + rate / 100) ** t for t, cf in enumerate(cfs, 1))
    r = _c(pv - c0)
    a, b, c = cfs
    verdict_en = "positive, so it adds value" if r > 0 else "negative, so it should be rejected at this rate"
    verdict_bn = "ধনাত্মক, তাই এটি মূল্য যোগ করে" if r > 0 else "ঋণাত্মক, তাই এই হারে এটি বাতিল করা উচিত"
    return _crore(f"{what_en} costs Rs {c0} crore now and returns Rs {a}, {b} and {c} crore at the end of years 1, 2 and 3. At a {rate}% discount rate, what is its NPV?",
                  f"{what_bn} এখন {c0} কোটি টাকা খরচ করে, আর ১, ২ ও ৩ নম্বর বছরের শেষে {a}, {b} ও {c} কোটি টাকা ফেরত দেয়। {rate}% বাট্টা-হারে এর নিট বর্তমান মূল্য কত?", r,
                  f"PV of returns = {a}/1.{rate:02d} + {b}/1.{rate:02d}² + {c}/1.{rate:02d}³ ≈ {pv:.2f}; NPV = {pv:.2f} - {c0} ≈ Rs {_f(r)} crore - {verdict_en}.",
                  f"ফেরতের বর্তমান মূল্য = {a}/1.{rate:02d} + {b}/1.{rate:02d}² + {c}/1.{rate:02d}³ ≈ {pv:.2f}; নিট বর্তমান মূল্য = {pv:.2f} - {c0} ≈ {_f(r)} কোটি টাকা — {verdict_bn}।",
                  (a + b + c - c0, _c(pv), _c(sum(cf / (1 + 2 * rate / 100) ** t for t, cf in enumerate(cfs, 1)) - c0)))


def payback(c0, annual, what_en, what_bn):
    r = _c(c0 / annual)
    return _n(f"{what_en} costs Rs {c0} crore and earns a steady Rs {annual} crore a year. What is its simple payback period?",
              f"{what_bn} খরচ {c0} কোটি টাকা আর বছরে স্থির {annual} কোটি টাকা আয় করে। এর সরল পরিশোধকাল কত?", r,
              f"Payback = cost ÷ yearly cash = {c0} ÷ {annual} = {_f(r)} years. It ignores everything after that point.",
              f"পরিশোধকাল = খরচ ÷ বার্ষিক নগদ = {c0} ÷ {annual} = {_f(r)} বছর। এর পরের সব আয় এটি উপেক্ষা করে।",
              (_c(r + 2), _c(r / 2), _c(annual / c0 * 100)), u_en=" years", u_bn=" বছর")


def bcr(b, c, what_en, what_bn):
    r = _c(b / c)
    ok_en = "above 1, so benefits exceed costs" if r > 1 else "below 1, so society loses on it"
    ok_bn = "১-এর বেশি, তাই লাভ খরচের চেয়ে বেশি" if r > 1 else "১-এর কম, তাই সমাজের এতে ক্ষতি"
    return _n(f"{what_en} has discounted benefits of Rs {b} crore (time saved, fewer crashes) and discounted costs of Rs {c} crore. What is its benefit-cost ratio?",
              f"{what_bn} বাট্টা-করা লাভ {b} কোটি টাকা (সময় বাঁচা, কম দুর্ঘটনা) আর বাট্টা-করা খরচ {c} কোটি টাকা। এর লাভ-খরচ অনুপাত কত?", r,
              f"BCR = {b} ÷ {c} = {_f(r)}, which is {ok_en}.",
              f"লাভ-খরচ অনুপাত = {b} ÷ {c} = {_f(r)}, যা {ok_bn}।",
              (_c(c / b), b - c, _c(r + 0.5)))


def pindex(pv, c0, what_en, what_bn):
    r = _c(pv / c0)
    return _n(f"{what_en} needs Rs {c0} crore now, and its future cash flows are worth Rs {pv} crore in today's money. What is its profitability index?",
              f"{what_bn} এখন {c0} কোটি টাকা লাগে, আর এর ভবিষ্যৎ নগদপ্রবাহের আজকের মূল্য {pv} কোটি টাকা। এর লাভযোগ্যতা সূচক কত?", r,
              f"PI = PV of future cash ÷ initial cost = {pv} ÷ {c0} = {_f(r)}. Above 1 means a positive NPV.",
              f"লাভযোগ্যতা সূচক = ভবিষ্যৎ নগদের বর্তমান মূল্য ÷ প্রাথমিক খরচ = {pv} ÷ {c0} = {_f(r)}। ১-এর বেশি মানে নিট বর্তমান মূল্য ধনাত্মক।",
              (pv - c0, _c(c0 / pv), _c(r + 0.25)))


def fisher(nom, infl):
    r = _c(((1 + nom / 100) / (1 + infl / 100) - 1) * 100)
    return _n(f"A bridge bond pays {nom}% a year while inflation runs at {infl}%. Using the exact Fisher relation, what is the real rate of return?",
              f"একটা সেতু-বন্ড বছরে {nom}% দেয়, আর মূল্যস্ফীতি {infl}%। সঠিক ফিশার সম্পর্কে প্রকৃত আয়ের হার কত?", r,
              f"Real = (1.{nom:02d} ÷ 1.{infl:02d}) - 1 ≈ {_f(r)}%. The quick 'nominal minus inflation' gives {nom - infl}%, slightly too high.",
              f"প্রকৃত হার = (1.{nom:02d} ÷ 1.{infl:02d}) - 1 ≈ {_f(r)}%। চটজলদি 'নামমাত্র বিয়োগ মূল্যস্ফীতি' দেয় {nom - infl}%, যা একটু বেশি।",
              (nom - infl, nom + infl, _c(nom / infl)), u_en="%", u_bn="%")


def slm(cost, salvage, life, what_en, what_bn):
    r = _c((cost - salvage) / life)
    return _lakh(f"{what_en} costs Rs {cost} lakh, lasts {life} years and will be sold for Rs {salvage} lakh as scrap. What is its yearly straight-line depreciation?",
                 f"{what_bn} দাম {cost} লাখ টাকা, চলে {life} বছর, আর শেষে {salvage} লাখ টাকায় ভাঙা হিসেবে বিক্রি হবে। সরলরৈখিক পদ্ধতিতে বার্ষিক অবচয় কত?", r,
                 f"Depreciation = (cost - scrap) ÷ life = ({cost} - {salvage}) ÷ {life} = Rs {_f(r)} lakh a year.",
                 f"অবচয় = (দাম - ভাঙা-মূল্য) ÷ আয়ু = ({cost} - {salvage}) ÷ {life} = বছরে {_f(r)} লাখ টাকা।",
                 (_c(cost / life), _c((cost + salvage) / life), _c(r * 2)))


def wdv(cost, rate, n, what_en, what_bn):
    r = _c(cost * (1 - rate / 100) ** n)
    return _lakh(f"{what_en[:1].upper()}{what_en[1:]} bought for Rs {cost} lakh is depreciated at {rate}% a year on the written-down value. What is its book value after {n} years?",
                 f"{cost} লাখ টাকায় কেনা {what_bn} হ্রাসমান মূল্যে বছরে {rate}% হারে অবচয় হয়। {n} বছর পরে এর খাতা-মূল্য কত?", r,
                 f"Book value = {cost} x (1 - {rate / 100:g})^{n} = Rs {_f(r)} lakh. Each year's {rate}% is taken from a smaller balance.",
                 f"খাতা-মূল্য = {cost} x (1 - {rate / 100:g})^{n} = {_f(r)} লাখ টাকা। প্রতি বছরের {rate}% ছোট হতে থাকা অঙ্ক থেকে কাটা হয়।",
                 (_c(cost * (1 - rate * n / 100)), _c(cost * (1 - rate / 100) ** (n - 1)), _c(cost * (1 - rate / 100) ** (n + 1))))


def sinking(fv, rate, n):
    i = rate / 100
    r = _c(fv * i / ((1 + i) ** n - 1))
    return _lakh(f"A city must replace a bridge's expansion joints for Rs {fv} lakh in {n} years. How much should it put into a sinking fund at the end of each year if the fund earns {rate}%?",
                 f"একটা শহরকে {n} বছর পরে {fv} লাখ টাকায় সেতুর প্রসারণ-জোড় বদলাতে হবে। তহবিল {rate}% আয় করলে প্রতি বছরের শেষে কত জমানো উচিত?", r,
                 f"A = FV x i ÷ ((1 + i)ⁿ - 1) = {fv} x {i:g} ÷ (1.{rate:02d}^{n} - 1) ≈ Rs {_f(r)} lakh - less than {fv}/{n} because interest helps.",
                 f"বার্ষিক জমা = FV x i ÷ ((1 + i)ⁿ - 1) = {fv} x {i:g} ÷ (1.{rate:02d}^{n} - 1) ≈ {_f(r)} লাখ টাকা — সুদ সাহায্য করে বলে {fv}/{n}-এর চেয়ে কম।",
                 (_c(fv / n), _c(fv * i), _c(fv / (1 + i) ** n)))


def bond(coupon, y, n):
    c = 1000 * coupon / 100
    r = round(sum(c / (1 + y / 100) ** t for t in range(1, n + 1)) + 1000 / (1 + y / 100) ** n)
    side_en = "below" if r < 1000 else "above"
    side_bn = "কম" if r < 1000 else "বেশি"
    return _n(f"A Rs 1,000 infrastructure bond pays a {coupon}% coupon yearly and is repaid in {n} years. If investors now want a {y}% yield, what is its price?",
              f"১,০০০ টাকার একটা পরিকাঠামো-বন্ড বছরে {coupon}% কুপন দেয় আর {n} বছরে শোধ হয়। বিনিয়োগকারীরা এখন {y}% আয় চাইলে এর দাম কত?", r,
              f"Price = PV of {n} coupons of Rs {c:g} + PV of Rs 1,000 at {y}% ≈ Rs {r:,}, {side_en} face value because the coupon is {'lower' if coupon < y else 'higher'} than the yield.",
              f"দাম = {c:g} টাকার {n}টি কুপনের বর্তমান মূল্য + {y}%-এ ১,০০০ টাকার বর্তমান মূল্য ≈ {r:,} টাকা — কুপন আয়ের চেয়ে {'কম' if coupon < y else 'বেশি'} বলে অভিহিত মূল্যের চেয়ে {side_bn}।",
              (1000, round(1000 + c * n), round(1000 / (1 + y / 100) ** n)), "Rs ", "", " টাকা")


def capm(rf, beta, rm, what_en, what_bn):
    r = _c(rf + beta * (rm - rf))
    return _n(f"{what_en} has a beta of {beta}. The risk-free rate is {rf}% and the market return is {rm}%. Using CAPM, what return should shareholders expect?",
              f"{what_bn} বিটা {beta}। ঝুঁকিহীন হার {rf}% আর বাজারের আয় {rm}%। মূলধনী সম্পদ মূল্যায়ন মডেলে শেয়ারহোল্ডাররা কত আয় আশা করবেন?", r,
              f"Expected return = rf + β(rm - rf) = {rf} + {beta} x ({rm} - {rf}) = {_f(r)}%.",
              f"প্রত্যাশিত আয় = rf + β(rm - rf) = {rf} + {beta} x ({rm} - {rf}) = {_f(r)}%।",
              (_c(beta * rm), rm, _c(rf + beta * rm)), u_en="%", u_bn="%")


def eac(cost, rate, n, what_en, what_bn):
    i = rate / 100
    r = _c(cost * i / (1 - (1 + i) ** -n))
    return _lakh(f"{what_en} costs Rs {cost} lakh and lasts {n} years. At {rate}%, what is its equivalent annual cost?",
                 f"{what_bn} দাম {cost} লাখ টাকা আর চলে {n} বছর। {rate}%-এ এর সমতুল্য বার্ষিক খরচ কত?", r,
                 f"EAC = cost x i ÷ (1 - (1 + i)^-n) = {cost} x {i:g} ÷ (1 - 1.{rate:02d}^-{n}) ≈ Rs {_f(r)} lakh a year.",
                 f"সমতুল্য বার্ষিক খরচ = দাম x i ÷ (1 - (1 + i)^-n) = {cost} x {i:g} ÷ (1 - 1.{rate:02d}^-{n}) ≈ বছরে {_f(r)} লাখ টাকা।",
                 (_c(cost / n), _c(cost * i), _c(cost / n + cost * i)))


def emi_split(p, annual, years):
    i = annual / 1200
    n = years * 12
    e = round(p * i * (1 + i) ** n / ((1 + i) ** n - 1))
    interest = round(p * i)
    r = e - interest
    return _n(f"A contractor's Rs {p:,} equipment loan at {annual}% a year over {years} years has an EMI of Rs {e:,}. How much of the very first EMI repays principal?",
              f"ঠিকাদারের {p:,} টাকার যন্ত্র-ঋণ, বছরে {annual}% হারে {years} বছরে, ইএমআই {e:,} টাকা। একেবারে প্রথম ইএমআই-এর কত অংশ আসল শোধ করে?", r,
              f"First month's interest = {p:,} x {annual}/1,200 ≈ Rs {interest:,}; principal = {e:,} - {interest:,} = Rs {r:,}. The principal share grows every month.",
              f"প্রথম মাসের সুদ = {p:,} x {annual}/1,200 ≈ {interest:,} টাকা; আসল = {e:,} - {interest:,} = {r:,} টাকা। প্রতি মাসে আসলের ভাগ বাড়ে।",
              (interest, e, round(p / n)), "Rs ", "", " টাকা")


def escalate(cost, infl, n, what_en, what_bn):
    r = _c(cost * (1 + infl / 100) ** n)
    return _crore(f"{what_en} is estimated at Rs {cost} crore in today's prices. If construction costs rise {infl}% a year, what will it cost if building starts in {n} years?",
                  f"{what_bn} আজকের দামে আনুমানিক {cost} কোটি টাকা। নির্মাণ-খরচ বছরে {infl}% বাড়লে {n} বছর পরে কাজ শুরু হলে খরচ কত হবে?", r,
                  f"Future cost = {cost} x 1.{infl:02d}^{n} ≈ Rs {_f(r)} crore. Delay is expensive!",
                  f"ভবিষ্যৎ খরচ = {cost} x 1.{infl:02d}^{n} ≈ {_f(r)} কোটি টাকা। দেরির দাম অনেক!",
                  (_c(cost * (1 + infl * n / 100)), cost + infl, _c(cost * (1 + infl / 100) ** (n - 1))))


def forex(usd, r0, r1):
    r = _c(usd * (r1 - r0) / 10)
    return _crore(f"A contractor must pay USD {usd} million for imported cable strands. The rupee weakens from Rs {r0} to Rs {_f(r1)} per dollar before payment. How much extra does the order cost?",
                  f"আমদানি করা কেবল-তারের জন্য ঠিকাদারকে {usd} মিলিয়ন ডলার দিতে হবে। পেমেন্টের আগে টাকা প্রতি ডলারে {r0} থেকে দুর্বল হয়ে {_f(r1)} টাকা হল। অর্ডারে কত বাড়তি খরচ?", r,
                  f"Extra = {usd} million x Rs {_f(_c(r1 - r0))} = Rs {_f(_c(usd * (r1 - r0)))} million = Rs {_f(r)} crore. A forward contract could have locked the rate.",
                  f"বাড়তি = {usd} মিলিয়ন x {_f(_c(r1 - r0))} টাকা = {_f(_c(usd * (r1 - r0)))} মিলিয়ন টাকা = {_f(r)} কোটি টাকা। ফরোয়ার্ড চুক্তি হার আগেই বেঁধে দিতে পারত।",
                  (_c(usd * r1 / 10), _c(usd * (r1 - r0)), _c(r / 2)))


def breakeven(fixed, toll, var):
    r = round(fixed * 100000 / (toll - var))
    return _n(f"A toll bridge has fixed costs of Rs {fixed} lakh a year. Each vehicle pays Rs {toll} and adds Rs {var} of variable cost. How many vehicles a year are needed to break even?",
              f"একটা টোল-সেতুর স্থির খরচ বছরে {fixed} লাখ টাকা। প্রতিটি যান {toll} টাকা দেয় আর {var} টাকা পরিবর্তনশীল খরচ যোগ করে। সমান-সমান হতে বছরে কতগুলি যান লাগবে?", r,
              f"Break-even = fixed ÷ (toll - variable) = Rs {fixed * 100000:,} ÷ {toll - var} = {r:,} vehicles.",
              f"সমচ্ছেদ = স্থির খরচ ÷ (টোল - পরিবর্তনশীল) = {fixed * 100000:,} টাকা ÷ {toll - var} = {r:,}টি যান।",
              (round(fixed * 100000 / toll), round(r / 365), r * 2))


def irr(c, x, n, what_en, what_bn):
    r = _c(((x / c) ** (1 / n) - 1) * 100)
    simple = _c((x / c - 1) * 100 / n)
    alts = (simple if simple != r else _c(r + 3), _c((x / c - 1) * 100), _c(r + 2))
    return _n(f"{what_en} costs Rs {c} crore today and returns a single Rs {_f(x)} crore after {n} year{'s' if n > 1 else ''}. What is its IRR?",
              f"{what_bn} আজ {c} কোটি টাকা খরচ করে, আর {n} বছর পরে একবারে {_f(x)} কোটি টাকা ফেরত দেয়। এর অভ্যন্তরীণ আয়-হার কত?", r,
              f"IRR solves {c} x (1 + IRR)^{n} = {_f(x)}, so IRR = ({_f(x)}/{c})^(1/{n}) - 1 ≈ {_f(r)}%.",
              f"অভ্যন্তরীণ আয়-হার এমন যে {c} x (1 + হার)^{n} = {_f(x)}, তাই হার = ({_f(x)}/{c})^(1/{n}) - 1 ≈ {_f(r)}%।",
              alts, u_en="%", u_bn="%")


ITEMS = (
    npv(100, (40, 40, 40), 10, "A river-ferry replacement bridge", "একটা নদী-খেয়ার বদলি সেতু"),
    npv(50, (20, 25, 30), 8, "A footbridge with shop rents", "দোকান-ভাড়াসহ একটা পায়ে-চলা সেতু"),
    npv(200, (80, 80, 80), 12, "A toll flyover", "একটা টোল-উড়ালপুল"),
    npv(120, (50, 50, 50), 9, "A rail-over-bridge with freight fees", "মাল-মাশুলসহ একটা রেল-উপরি সেতু"),
    npv(80, (30, 35, 40), 10, "A port access bridge", "একটা বন্দর-সংযোগ সেতু"),
    npv(150, (60, 60, 60), 15, "A private estuary crossing", "একটা বেসরকারি মোহনা-পারাপার"),
    payback(60, 15, "A bypass toll plaza upgrade", "একটা বাইপাস টোল-প্লাজার উন্নয়ন"),
    payback(90, 12, "A canal-crossing toll bridge", "একটা খাল-পারাপারের টোল-সেতু"),
    payback(45, 10, "A bridge-deck solar panel scheme", "সেতু-পাটাতনে সৌর প্যানেলের প্রকল্প"),
    payback(100, 8, "A riverfront bridge with parking fees", "পার্কিং-মাশুলসহ নদীতীরের একটা সেতু"),
    bcr(300, 200, "A village-to-market bridge", "গ্রাম-থেকে-বাজার একটা সেতু"),
    bcr(450, 500, "A low-traffic island link", "কম-যানবাহনের একটা দ্বীপ-সংযোগ"),
    bcr(840, 600, "A city ring-road bridge", "শহরের বলয়-সড়কের একটা সেতু"),
    bcr(250, 100, "A school-route footbridge", "স্কুল-পথের একটা পায়ে-চলা সেতু"),
    pindex(130, 100, "A truss-bridge widening", "একটা ট্রাস-সেতু চওড়া করার কাজ"),
    pindex(90, 120, "A decorative arch makeover", "একটা শোভাবর্ধক খিলান-সংস্কার"),
    pindex(275, 250, "A container-yard overbridge", "একটা কন্টেনার-চত্বরের উপরি সেতু"),
    fisher(9, 4), fisher(12, 6), fisher(7, 5), fisher(10, 7),
    slm(50, 5, 9, "A concrete pump", "একটা কংক্রিট-পাম্প"),
    slm(120, 20, 10, "A piling rig", "একটা পাইলিং-যন্ত্র"),
    slm(36, 6, 5, "A site generator", "একটা সাইট-জেনারেটর"),
    slm(80, 8, 12, "A launching girder", "একটা লঞ্চিং-গার্ডার"),
    wdv(100, 20, 2, "a tower crane", "একটা টাওয়ার-ক্রেন"),
    wdv(50, 15, 3, "a batching plant", "একটা ব্যাচিং-প্ল্যান্ট"),
    wdv(200, 25, 2, "a floating barge crane", "একটা ভাসমান বজরা-ক্রেন"),
    wdv(80, 10, 3, "a bridge inspection vehicle", "একটা সেতু-পরিদর্শন গাড়ি"),
    sinking(100, 8, 5), sinking(50, 6, 10), sinking(200, 10, 4), sinking(60, 7, 6),
    bond(8, 10, 3), bond(9, 7, 2), bond(10, 12, 4), bond(7, 5, 3),
    capm(7, 1.2, 12, "A bridge-building company's share", "একটা সেতু-নির্মাণ কোম্পানির শেয়ারের"),
    capm(6, 0.8, 11, "A toll-road operator's share", "একটা টোল-সড়ক পরিচালকের শেয়ারের"),
    capm(6.5, 1.5, 12, "A steel-fabricator's share", "একটা ইস্পাত-নির্মাতার শেয়ারের"),
    capm(7, 0.6, 13, "A bridge-maintenance utility's share", "একটা সেতু-রক্ষণাবেক্ষণ সংস্থার শেয়ারের"),
    eac(100, 10, 10, "A bridge bearing set", "একসেট সেতু-বিয়ারিং-এর"),
    eac(60, 8, 5, "A road-marking machine", "একটা রাস্তা-দাগানোর যন্ত্রের"),
    eac(150, 9, 20, "A cathodic-protection system", "একটা ক্যাথোডিক-সুরক্ষা ব্যবস্থার"),
    eac(40, 12, 8, "A deck-drainage pump set", "একসেট পাটাতন-নিকাশি পাম্পের"),
    emi_split(1200000, 9, 10), emi_split(600000, 12, 5), emi_split(2500000, 8.5, 15), emi_split(400000, 10, 3),
    escalate(100, 6, 3, "A cable-stayed bridge", "একটা কেবল-ধৃত সেতু"),
    escalate(250, 5, 4, "A sea-link viaduct", "একটা সমুদ্র-সংযোগ উড়ালপথ"),
    escalate(80, 8, 2, "A hill-road arch bridge", "পাহাড়ি রাস্তার একটা খিলান-সেতু"),
    escalate(40, 7, 5, "A railway foot-overbridge", "রেলের একটা পায়ে-চলা উপরি সেতু"),
    forex(5, 83, 86), forex(12, 82, 85), forex(8, 84, 88), forex(20, 83, 84.5),
    breakeven(365, 60, 10), breakeven(219, 80, 20), breakeven(180, 100, 25), breakeven(146, 50, 10),
    irr(100, 121, 2, "A bridge-lighting upgrade", "একটা সেতু-আলো উন্নয়ন"),
    irr(50, 60, 1, "A one-year bridge-repair contract", "এক বছরের একটা সেতু-মেরামত চুক্তি"),
    irr(80, 100, 2, "A ferry-terminal footbridge", "একটা খেয়াঘাটের পায়ে-চলা সেতু"),
    irr(64, 100, 2, "A land parcel beside a new bridge", "নতুন সেতুর পাশের একখণ্ড জমি"),

    mcq("Two bridge designs are mutually exclusive: design A has the higher NPV, design B the higher IRR. Which should a value-maximising owner choose?", ["A, because NPV measures the actual rupees of value added", "B, because a higher percentage is always better", "Neither, because the methods disagree", "Whichever is cheaper to build"], 0,
        "IRR is a percentage and can favour small projects; NPV shows how much wealth each option really creates.",
        "দুটি সেতু-নকশার মধ্যে একটিই বাছতে হবে: নকশা ক-এর নিট বর্তমান মূল্য বেশি, নকশা খ-এর অভ্যন্তরীণ আয়-হার বেশি। মূল্য সর্বাধিক করতে চাওয়া মালিক কোনটি বাছবেন?", ["ক, কারণ নিট বর্তমান মূল্য আসল কত টাকা মূল্য যোগ হল তা মাপে", "খ, কারণ বেশি শতাংশ সবসময় ভালো", "কোনোটিই নয়, কারণ পদ্ধতি দুটি মেলে না", "যেটা বানাতে সস্তা"],
        "অভ্যন্তরীণ আয়-হার একটা শতাংশ, যা ছোট প্রকল্পকে সুবিধা দিতে পারে; নিট বর্তমান মূল্য দেখায় প্রতিটি বিকল্প সত্যিই কত সম্পদ তৈরি করে।"),
    mcq("Why is the simple payback period a weak test for a bridge designed to last 100 years?", ["It ignores all cash flows after payback and the time value of money", "It is too hard to calculate", "It always gives a negative answer", "It counts only maintenance costs"], 0,
        "A bridge that pays back in 12 years and then earns for 88 more looks no better than one that dies at year 13.",
        "১০০ বছর টেকার জন্য নকশা করা সেতুর ক্ষেত্রে সরল পরিশোধকাল দুর্বল পরীক্ষা কেন?", ["পরিশোধের পরের সব নগদপ্রবাহ আর টাকার সময়-মূল্য এটি উপেক্ষা করে", "এটি হিসাব করা খুব কঠিন", "এটি সবসময় ঋণাত্মক উত্তর দেয়", "এটি শুধু রক্ষণাবেক্ষণ-খরচ গোনে"],
        "যে সেতু ১২ বছরে খরচ তুলে আরও ৮৮ বছর আয় করে, তাকে ১৩ বছরে ভেঙে পড়া সেতুর চেয়ে ভালো দেখায় না।"),
    mcq("What is the 'discounted payback period' of a project?", ["The time until the discounted cash flows add up to the initial investment", "The payback period after a supplier's price discount", "Half the ordinary payback period", "The time until the loan interest rate is cut"], 0,
        "It fixes one flaw of simple payback by valuing later rupees less, though it still ignores cash after that point.",
        "কোনো প্রকল্পের 'বাট্টা-করা পরিশোধকাল' কী?", ["বাট্টা-করা নগদপ্রবাহ যোগ হয়ে প্রাথমিক বিনিয়োগের সমান হতে যত সময় লাগে", "সরবরাহকারীর ছাড়ের পরের পরিশোধকাল", "সাধারণ পরিশোধকালের অর্ধেক", "ঋণের সুদ কমা পর্যন্ত সময়"],
        "পরের টাকাকে কম মূল্য দিয়ে এটি সরল পরিশোধকালের একটা ত্রুটি সারায়, যদিও তার পরের নগদ এখনও উপেক্ষা করে।"),
    mcq("Why can a bridge project whose cash flows switch between negative and positive several times have more than one IRR?", ["Its NPV curve can cross zero at several different discount rates", "IRR is always calculated twice", "Banks set two interest rates", "Each pier has its own IRR"], 0,
        "With a big repair outlay in the middle of its life, the NPV equation can have multiple roots, so use NPV instead.",
        "যে সেতু-প্রকল্পের নগদপ্রবাহ কয়েকবার ঋণাত্মক-ধনাত্মক বদলায়, তার একাধিক অভ্যন্তরীণ আয়-হার থাকতে পারে কেন?", ["এর নিট বর্তমান মূল্যের রেখা কয়েকটি আলাদা বাট্টা-হারে শূন্য পার হতে পারে", "অভ্যন্তরীণ আয়-হার সবসময় দুবার হিসাব হয়", "ব্যাংক দুটি সুদের হার ঠিক করে", "প্রতিটি স্তম্ভের নিজস্ব হার থাকে"],
        "জীবনের মাঝপথে বড় মেরামত-খরচ থাকলে সমীকরণের একাধিক মূল হতে পারে, তাই তখন নিট বর্তমান মূল্য ব্যবহার করো।"),
    mcq("Why must a bridge cash-flow forecast use nominal cash flows with a nominal discount rate, or real cash flows with a real rate?", ["Mixing them counts inflation twice or not at all, distorting the NPV", "Real rates are illegal in India", "Nominal cash flows are always zero", "It makes the spreadsheet shorter"], 0,
        "Inflated tolls discounted at a real rate look far too good; today's-price tolls discounted at a nominal rate look far too bad.",
        "সেতুর নগদপ্রবাহ-পূর্বাভাসে নামমাত্র নগদের সঙ্গে নামমাত্র বাট্টা-হার, বা প্রকৃত নগদের সঙ্গে প্রকৃত হার ব্যবহার করতেই হবে কেন?", ["মিশিয়ে ফেললে মূল্যস্ফীতি দুবার গোনা হয় বা একবারও নয়, তাতে নিট বর্তমান মূল্য বিকৃত হয়", "ভারতে প্রকৃত হার বেআইনি", "নামমাত্র নগদ সবসময় শূন্য", "এতে হিসাবের পাতা ছোট হয়"],
        "মূল্যস্ফীতি-যুক্ত টোলকে প্রকৃত হারে বাট্টা করলে অতিরিক্ত ভালো দেখায়; আজকের দামের টোলকে নামমাত্র হারে বাট্টা করলে অতিরিক্ত খারাপ দেখায়।"),
    mcq("Why does written-down-value depreciation give a crane larger tax deductions in its early years?", ["A fixed percentage is applied to a book value that shrinks each year", "Cranes are taxed more when new", "The law doubles deductions in year 1 only", "Old cranes have no value at all"], 0,
        "20% of 100 is 20, but 20% of 64 is only 12.8 - deductions fall as the balance falls.",
        "হ্রাসমান-মূল্য অবচয়ে প্রথম দিকের বছরগুলিতে ক্রেনের জন্য করছাড় বেশি হয় কেন?", ["প্রতি বছর ছোট হতে থাকা খাতা-মূল্যের উপর একটা স্থির শতাংশ ধরা হয়", "নতুন ক্রেনে বেশি কর লাগে", "আইন শুধু প্রথম বছরে ছাড় দ্বিগুণ করে", "পুরনো ক্রেনের কোনো মূল্যই নেই"],
        "১০০-র ২০% হল ২০, কিন্তু ৬৪-র ২০% মাত্র ১২.৮ — অঙ্ক কমলে ছাড়ও কমে।"),
    mcq("What is a 'sinking fund' in a bridge authority's accounts?", ["Regular deposits that grow with interest to pay a known large future cost, like a deck replacement", "Money lost when a pier sinks", "A fund for underwater bridges only", "Cash kept to pay fines"], 0,
        "Saving steadily avoids a sudden shock to the budget or an emergency loan.",
        "সেতু-কর্তৃপক্ষের হিসাবে 'নিমজ্জন তহবিল' কী?", ["নিয়মিত জমা, যা সুদে বেড়ে পাটাতন বদলের মতো জানা বড় ভবিষ্যৎ খরচ মেটায়", "স্তম্ভ ডুবে গেলে হারানো টাকা", "শুধু জলের নিচের সেতুর তহবিল", "জরিমানা দেওয়ার জন্য রাখা নগদ"],
        "নিয়মিত সঞ্চয়ে বাজেটে হঠাৎ ধাক্কা বা জরুরি ঋণ এড়ানো যায়।"),
    mcq("Why does the price of an existing infrastructure bond fall when market interest rates rise?", ["Its fixed coupons now look poor beside new bonds paying more, so buyers will only pay less for it", "The bridge becomes older", "The government cancels the coupons", "Bond prices never change"], 0,
        "Price and yield move in opposite directions; the lower price lifts the buyer's return up to the new market rate.",
        "বাজারে সুদের হার বাড়লে পুরনো পরিকাঠামো-বন্ডের দাম পড়ে কেন?", ["বেশি দেওয়া নতুন বন্ডের পাশে এর স্থির কুপন কম আকর্ষণীয়, তাই ক্রেতা কম দামই দেবেন", "সেতু পুরনো হয়ে যায়", "সরকার কুপন বাতিল করে", "বন্ডের দাম কখনো বদলায় না"],
        "দাম আর আয় উল্টো দিকে চলে; কম দামে কিনলে ক্রেতার আয় বেড়ে নতুন বাজার-হারে পৌঁছায়।"),
    mcq("What does a bond's 'yield to maturity' represent?", ["The overall yearly return if it is bought at today's price and held until it is repaid", "The coupon rate printed on it", "The number of years left", "The bank's service fee"], 0,
        "It combines the coupons with any gain or loss between today's price and the face value.",
        "বন্ডের 'পরিপক্বতা পর্যন্ত আয়' কী বোঝায়?", ["আজকের দামে কিনে শোধ হওয়া পর্যন্ত রাখলে মোট বার্ষিক আয়", "এতে ছাপা কুপন-হার", "বাকি বছরের সংখ্যা", "ব্যাংকের পরিষেবা-মাশুল"],
        "এতে কুপনের সঙ্গে আজকের দাম আর অভিহিত মূল্যের ফারাকের লাভ-ক্ষতিও ধরা হয়।"),
    mcq("What does a beta of 1.5 for a construction company's shares mean?", ["The share tends to rise or fall about 1.5 times as much as the overall market", "The company has 1.5 bridges", "The share price is Rs 1.5", "The company pays a 1.5% dividend"], 0,
        "Builders are cyclical: in booms they soar, in slowdowns they slump harder than the market.",
        "একটা নির্মাণ-কোম্পানির শেয়ারের বিটা ১.৫ মানে কী?", ["শেয়ারটি সামগ্রিক বাজারের প্রায় ১.৫ গুণ ওঠানামা করে", "কোম্পানির ১.৫টি সেতু আছে", "শেয়ারের দাম ১.৫ টাকা", "কোম্পানি ১.৫% লভ্যাংশ দেয়"],
        "নির্মাণ-ব্যবসা চক্রাকার: সুসময়ে লাফিয়ে ওঠে, মন্দায় বাজারের চেয়ে বেশি পড়ে।"),
    mcq("What is 'systematic risk' for an investor in bridge-building shares?", ["Market-wide risk, such as a recession or rising interest rates, that diversification cannot remove", "The risk that one site crane breaks", "Risk from a single bad contract", "Risk that only affects one engineer"], 0,
        "Only systematic risk earns a premium in CAPM, because firm-specific risk can be diversified away.",
        "সেতু-নির্মাণের শেয়ারে বিনিয়োগকারীর 'ব্যবস্থাগত ঝুঁকি' কী?", ["মন্দা বা সুদ বাড়ার মতো গোটা বাজারের ঝুঁকি, যা বৈচিত্র্যকরণে দূর হয় না", "সাইটের একটা ক্রেন ভাঙার ঝুঁকি", "একটা খারাপ চুক্তির ঝুঁকি", "শুধু একজন প্রকৌশলীর ঝুঁকি"],
        "মূলধনী সম্পদ মূল্যায়ন মডেলে শুধু ব্যবস্থাগত ঝুঁকিই বাড়তি আয় পায়, কারণ কোম্পানি-নির্দিষ্ট ঝুঁকি বৈচিত্র্যে কাটানো যায়।"),
    mcq("Why does an investor holding shares in twenty different companies face less risk than one holding shares only in a single contractor?", ["Problems at one firm are offset by others, cancelling out much firm-specific risk", "Twenty shares are guaranteed by law", "Brokers charge less", "Contractor shares cannot fall"], 0,
        "Diversification: a collapsed tender at one company barely dents a broad portfolio.",
        "একজন ঠিকাদারের শেয়ার একা রাখার চেয়ে কুড়িটি আলাদা কোম্পানির শেয়ার রাখলে ঝুঁকি কম কেন?", ["এক কোম্পানির সমস্যা অন্যগুলি পুষিয়ে দেয়, কোম্পানি-নির্দিষ্ট ঝুঁকির অনেকটা কেটে যায়", "কুড়িটি শেয়ার আইনে নিশ্চিত", "দালাল কম মাশুল নেয়", "ঠিকাদারের শেয়ার পড়তে পারে না"],
        "বৈচিত্র্যকরণ: এক কোম্পানির দরপত্র ভেস্তে গেলে বড় পোর্টফোলিওতে সামান্যই আঁচ লাগে।"),
    mcq("Why compare two bridge-bearing options with different lifespans using equivalent annual cost rather than total price?", ["It puts options lasting different numbers of years on a fair cost-per-year basis", "Total price is always secret", "It ignores interest completely", "Bearings with longer lives are banned"], 0,
        "A Rs 60 lakh bearing lasting 30 years can beat a Rs 40 lakh one lasting 12 years once costs are spread per year.",
        "আলাদা আয়ুর দুটি সেতু-বিয়ারিং বিকল্প মোট দামে না দেখে সমতুল্য বার্ষিক খরচে তুলনা করা হয় কেন?", ["এতে আলাদা বছর টেকা বিকল্পগুলিকে বছরপ্রতি খরচের ন্যায্য ভিত্তিতে আনা যায়", "মোট দাম সবসময় গোপন থাকে", "এটি সুদ পুরো উপেক্ষা করে", "বেশি আয়ুর বিয়ারিং নিষিদ্ধ"],
        "৩০ বছর টেকা ৬০ লাখের বিয়ারিং বছরে ভাগ করলে ১২ বছর টেকা ৪০ লাখেরটাকে হারাতে পারে।"),
    mcq("Why might a weathering-steel bridge win on life-cycle cost even though it costs more to build?", ["Savings on repainting and maintenance over decades can outweigh the higher upfront price", "Weathering steel never needs inspection", "It is cheaper to buy than ordinary steel", "Rust makes it stronger every year"], 0,
        "Its stable rust layer protects it, so the bridge skips several expensive repaint cycles - though it still needs inspection.",
        "নির্মাণ-খরচ বেশি হলেও আবহ-সহ ইস্পাতের সেতু জীবনচক্র-খরচে জিততে পারে কেন?", ["দশকের পর দশক রং আর রক্ষণাবেক্ষণের সাশ্রয় বেশি প্রাথমিক দামকে ছাপিয়ে যেতে পারে", "এই ইস্পাতের কখনো পরিদর্শন লাগে না", "এটি সাধারণ ইস্পাতের চেয়ে সস্তা", "মরচে একে প্রতি বছর মজবুত করে"],
        "এর স্থিতিশীল মরচে-স্তর সুরক্ষা দেয়, তাই কয়েকটা দামি রং-চক্র বাঁচে — তবে পরিদর্শন তবুও লাগে।"),
    mcq("What does a 'price variation clause' in a four-year bridge contract do?", ["Adjusts payments in line with published indices for steel, cement, fuel and labour", "Lets the contractor charge any price", "Fixes every price for ever", "Changes the bridge's length"], 0,
        "It shares inflation risk fairly, so bidders need not pad their prices with huge safety margins.",
        "চার বছরের সেতু-চুক্তিতে 'মূল্য-পরিবর্তন ধারা' কী করে?", ["ইস্পাত, সিমেন্ট, জ্বালানি আর শ্রমের প্রকাশিত সূচক অনুযায়ী পেমেন্ট সমন্বয় করে", "ঠিকাদারকে যেকোনো দাম নিতে দেয়", "সব দাম চিরকালের মতো বেঁধে দেয়", "সেতুর দৈর্ঘ্য বদলায়"],
        "এটি মূল্যস্ফীতির ঝুঁকি ন্যায্যভাবে ভাগ করে, তাই দরদাতাদের দামে বিশাল নিরাপত্তা-মার্জিন জুড়তে হয় না।"),
    mcq("What is a currency 'forward contract' for a contractor importing bridge cables?", ["An agreement today to buy dollars at a fixed rate on a future payment date", "A contract to deliver cables early", "A loan in a foreign currency", "A promise to pay in gold"], 0,
        "It removes the risk of the rupee weakening before the invoice is due, at the cost of missing any gain if it strengthens.",
        "সেতুর কেবল আমদানিকারী ঠিকাদারের জন্য মুদ্রার 'ফরোয়ার্ড চুক্তি' কী?", ["ভবিষ্যতের পেমেন্টের দিনে স্থির হারে ডলার কেনার আজকের চুক্তি", "আগেভাগে কেবল সরবরাহের চুক্তি", "বিদেশি মুদ্রায় ঋণ", "সোনায় দেওয়ার প্রতিশ্রুতি"],
        "চালান মেটানোর আগে টাকা দুর্বল হওয়ার ঝুঁকি এতে দূর হয়, যদিও টাকা মজবুত হলে লাভটাও হাতছাড়া হয়।"),
    mcq("What is a 'natural hedge' against currency risk on a bridge project?", ["Earning revenue in the same currency as the costs or debt, so rate swings cancel out", "Planting hedges along the approach road", "Keeping cash under a mattress", "Buying only local sand"], 0,
        "A port bridge charging shipping lines in dollars can safely repay a dollar loan.",
        "সেতু-প্রকল্পে মুদ্রা-ঝুঁকির বিরুদ্ধে 'স্বাভাবিক আড়াল' কী?", ["খরচ বা ঋণ যে মুদ্রায়, আয়ও সেই মুদ্রায় করা, যাতে হারের ওঠানামা কাটাকাটি হয়", "সংযোগ-সড়কের ধারে ঝোপ লাগানো", "নগদ তোশকের নিচে রাখা", "শুধু স্থানীয় বালি কেনা"],
        "জাহাজ-সংস্থাকে ডলারে মাশুল নেওয়া বন্দর-সেতু নিরাপদে ডলার-ঋণ শোধ করতে পারে।"),
    mcq("What does a Monte Carlo simulation add to a bridge cost estimate?", ["It runs thousands of random combinations of uncertain costs to show the probability of each total", "It adds casino profits to the budget", "It removes all risk", "It gives one exact final cost"], 0,
        "Instead of a single number, the client sees a range, such as a 50% and a 90% confidence cost.",
        "সেতুর খরচ-আন্দাজে মন্টে কার্লো অনুকরণ কী যোগ করে?", ["অনিশ্চিত খরচের হাজার হাজার এলোমেলো মিশ্রণ চালিয়ে প্রতিটি মোটের সম্ভাবনা দেখায়", "বাজেটে জুয়াখানার লাভ যোগ করে", "সব ঝুঁকি দূর করে", "একটা নির্ভুল চূড়ান্ত খরচ দেয়"],
        "একটা সংখ্যার বদলে গ্রাহক একটা পরিসর দেখেন, যেমন ৫০% আর ৯০% আস্থার খরচ।"),
    mcq("What is a 'P90' cost estimate for a large bridge?", ["A cost that has a 90% chance of not being exceeded", "The cost of 90 piers", "90% of the cheapest bid", "The cost after 90 days"], 0,
        "Lenders and governments often budget at P90 to avoid running out of money.",
        "বড় সেতুর 'পি৯০' খরচ-আন্দাজ কী?", ["এমন খরচ যা ছাড়িয়ে না যাওয়ার সম্ভাবনা ৯০%", "৯০টি স্তম্ভের খরচ", "সবচেয়ে সস্তা দরের ৯০%", "৯০ দিন পরের খরচ"],
        "টাকা ফুরিয়ে যাওয়া এড়াতে ঋণদাতা আর সরকার প্রায়ই পি৯০-তে বাজেট করে।"),
    mcq("A river-flood risk has a 20% chance of costing Rs 5 crore and an 80% chance of costing nothing. What is its expected monetary value?", ["Rs 1 crore", "Rs 5 crore", "Rs 4 crore", "Rs 0.2 crore"], 0,
        "EMV = 0.2 x 5 + 0.8 x 0 = Rs 1 crore - the amount a large risk register would reserve on average.",
        "নদী-বন্যার একটা ঝুঁকিতে ২০% সম্ভাবনায় ৫ কোটি টাকা খরচ আর ৮০% সম্ভাবনায় কিছুই না। এর প্রত্যাশিত আর্থিক মূল্য কত?", ["১ কোটি টাকা", "৫ কোটি টাকা", "৪ কোটি টাকা", "০.২ কোটি টাকা"],
        "প্রত্যাশিত মূল্য = ০.২ x ৫ + ০.৮ x ০ = ১ কোটি টাকা — বড় ঝুঁকি-তালিকা গড়ে এতটাই সংরক্ষণ রাখে।"),
    mcq("What is a 'real option' in bridge planning?", ["A right, not an obligation, to act later, such as building piers strong enough for a future second deck", "An option to buy shares in the contractor", "A choice of paint colours", "A legal duty to widen the bridge"], 0,
        "Paying a little now for flexibility can be worth far more than its cost if traffic grows.",
        "সেতু-পরিকল্পনায় 'বাস্তব বিকল্প' কী?", ["পরে কাজ করার অধিকার, বাধ্যতা নয় — যেমন ভবিষ্যতে দ্বিতীয় পাটাতন বসানোর মতো মজবুত স্তম্ভ বানানো", "ঠিকাদারের শেয়ার কেনার বিকল্প", "রঙের পছন্দ", "সেতু চওড়া করার আইনি দায়"],
        "নমনীয়তার জন্য এখন একটু খরচ করলে যানবাহন বাড়লে তার মূল্য খরচের চেয়ে অনেক বেশি হতে পারে।"),
    mcq("What is the 'sunk cost fallacy' on a troubled bridge project?", ["Continuing because of money already spent, instead of judging only future costs and benefits", "Counting the cost of sunken piers", "Refusing to pay for divers", "Writing off old bridges for tax"], 0,
        "Money already spent cannot be recovered either way; only the choices ahead should drive the decision.",
        "সমস্যায় পড়া সেতু-প্রকল্পে 'ডুবে-যাওয়া খরচের ভ্রান্তি' কী?", ["শুধু ভবিষ্যতের খরচ-লাভ না দেখে, আগে খরচ হয়ে গেছে বলে চালিয়ে যাওয়া", "ডুবে যাওয়া স্তম্ভের খরচ গোনা", "ডুবুরির টাকা দিতে অস্বীকার", "করের জন্য পুরনো সেতু বাদ দেওয়া"],
        "খরচ হয়ে যাওয়া টাকা কোনোভাবেই ফেরে না; শুধু সামনের বিকল্পগুলি দিয়েই সিদ্ধান্ত নেওয়া উচিত।"),
    mcq("What is the 'opportunity cost of capital' for a bridge investor?", ["The return given up on the best alternative investment of similar risk", "The cost of printing share certificates", "The interest on a savings account only", "The price of the land"], 0,
        "It is why the discount rate is not zero, even when a government uses its own cash.",
        "সেতু-বিনিয়োগকারীর 'মূলধনের সুযোগ-খরচ' কী?", ["একই রকম ঝুঁকির সেরা বিকল্প বিনিয়োগে যে আয় ছেড়ে দিতে হয়", "শেয়ার-সার্টিফিকেট ছাপার খরচ", "শুধু সঞ্চয়-খাতার সুদ", "জমির দাম"],
        "এজন্যই সরকার নিজের নগদ খরচ করলেও বাট্টা-হার শূন্য হয় না।"),
    mcq("What is 'retention money' in a bridge construction contract?", ["A share of each payment, often 5%, held back until the defects period ends", "Money paid to retain staff", "A bonus for finishing early", "The contractor's profit"], 0,
        "It gives the owner leverage to get defects fixed, but it squeezes the contractor's cash flow.",
        "সেতু-নির্মাণ চুক্তিতে 'আটক টাকা' কী?", ["প্রতিটি পেমেন্টের একটা ভাগ, প্রায়ই ৫%, ত্রুটি-সারাইয়ের মেয়াদ শেষ হওয়া পর্যন্ত রেখে দেওয়া", "কর্মী ধরে রাখার জন্য দেওয়া টাকা", "আগে শেষ করার বোনাস", "ঠিকাদারের লাভ"],
        "এতে ত্রুটি সারাতে মালিকের হাতে চাপ থাকে, কিন্তু ঠিকাদারের নগদপ্রবাহ টানাটানিতে পড়ে।"),
    mcq("What is a 'mobilisation advance' on a bridge contract?", ["An advance paid at the start to set up the site, recovered from later bills", "A fee for moving traffic", "A fine for late mobile phone bills", "Payment for the final inspection"], 0,
        "It is usually secured by a bank guarantee, because the work has not yet been done.",
        "সেতু-চুক্তিতে 'সংগঠন-অগ্রিম' কী?", ["সাইট গোছাতে শুরুতে দেওয়া অগ্রিম, যা পরের বিল থেকে কেটে নেওয়া হয়", "যানবাহন সরানোর মাশুল", "দেরিতে ফোন-বিলের জরিমানা", "শেষ পরিদর্শনের পেমেন্ট"],
        "কাজ তখনও হয়নি বলে সাধারণত ব্যাংক-জামানত দিয়ে এটি সুরক্ষিত রাখা হয়।"),
    mcq("What is a 'performance bank guarantee' in a bridge contract?", ["A bank's promise to pay the owner a set sum if the contractor fails to perform", "A guarantee that the bridge will never fall", "A bank's loan to the owner", "A certificate of good painting"], 0,
        "Typically 5-10% of the contract value, it protects the owner without tying up all the contractor's cash.",
        "সেতু-চুক্তিতে 'কার্যসম্পাদন ব্যাংক-জামানত' কী?", ["ঠিকাদার কাজ না করলে মালিককে নির্দিষ্ট অঙ্ক দেওয়ার ব্যাংকের প্রতিশ্রুতি", "সেতু কখনো পড়বে না তার নিশ্চয়তা", "মালিককে ব্যাংকের ঋণ", "ভালো রঙের সার্টিফিকেট"],
        "সাধারণত চুক্তিমূল্যের ৫-১০%, এটি ঠিকাদারের সব নগদ আটকে না রেখে মালিককে সুরক্ষা দেয়।"),
    mcq("What are 'liquidated damages' in a bridge contract?", ["A pre-agreed sum per day or week that the contractor pays for late completion", "Damage caused by water", "The cost of melted steel", "A refund for unused cement"], 0,
        "Fixing the amount in advance avoids long court battles about how much a delay really cost.",
        "সেতু-চুক্তিতে 'নির্ধারিত ক্ষতিপূরণ' কী?", ["দেরিতে কাজ শেষ করলে ঠিকাদার প্রতিদিন বা সপ্তাহে যে আগে-ঠিক-করা অঙ্ক দেন", "জলে হওয়া ক্ষতি", "গলে যাওয়া ইস্পাতের খরচ", "অব্যবহৃত সিমেন্টের ফেরত"],
        "অঙ্ক আগে ঠিক থাকলে দেরির আসল ক্ষতি কত তা নিয়ে লম্বা মামলা এড়ানো যায়।"),
    mcq("A Rs 50 toll is never raised for 20 years while inflation averages 5% a year. About what is it worth in today's money by year 20?", ["About Rs 19", "Still Rs 50", "About Rs 45", "About Rs 133"], 0,
        "50 ÷ 1.05²⁰ ≈ 50 ÷ 2.65 ≈ Rs 19. That is why concessions index tolls to inflation.",
        "৫০ টাকার টোল ২০ বছর একবারও বাড়ানো হল না, আর মূল্যস্ফীতি গড়ে বছরে ৫%। ২০ নম্বর বছরে আজকের টাকায় এর মূল্য প্রায় কত?", ["প্রায় ১৯ টাকা", "এখনও ৫০ টাকা", "প্রায় ৪৫ টাকা", "প্রায় ১৩৩ টাকা"],
        "৫০ ÷ ১.০৫²⁰ ≈ ৫০ ÷ ২.৬৫ ≈ ১৯ টাকা। তাই ছাড়-চুক্তিতে টোলকে মূল্যস্ফীতির সঙ্গে বাঁধা হয়।"),
    mcq("How does a toll company's credit rating affect a new bridge it wants to build?", ["A better rating lowers the interest it pays on loans and bonds", "It sets the bridge's maximum span", "It decides the toll price by law", "It has no effect at all"], 0,
        "Agencies judge the chance of default; lower risk means cheaper money and a more viable project.",
        "একটা টোল-কোম্পানির ঋণমান তার নতুন সেতু বানানোর পরিকল্পনাকে কীভাবে প্রভাবিত করে?", ["ভালো ঋণমানে ঋণ আর বন্ডে কম সুদ লাগে", "এটি সেতুর সর্বোচ্চ বিস্তার ঠিক করে", "এটি আইনে টোলের দাম ঠিক করে", "এর কোনো প্রভাবই নেই"],
        "সংস্থাগুলি খেলাপির সম্ভাবনা বিচার করে; কম ঝুঁকি মানে সস্তা টাকা আর বেশি টেকসই প্রকল্প।"),
    mcq("What does the 'loan life coverage ratio' (LLCR) measure for a toll bridge?", ["Present value of cash available for debt service over the loan's life, divided by the debt outstanding", "The number of years left on the loan", "The bridge's design life divided by its age", "Toll income divided by staff count"], 0,
        "Unlike a single year's DSCR, LLCR looks across the whole remaining loan.",
        "টোল-সেতুর ক্ষেত্রে 'ঋণ-জীবন আচ্ছাদন অনুপাত' কী মাপে?", ["ঋণের মেয়াদ জুড়ে ঋণ-পরিশোধে উপলব্ধ নগদের বর্তমান মূল্য ভাগ বাকি ঋণ", "ঋণের বাকি বছরের সংখ্যা", "সেতুর নকশা-আয়ু ভাগ তার বয়স", "টোল-আয় ভাগ কর্মী-সংখ্যা"],
        "এক বছরের ঋণ-পরিশোধ আচ্ছাদন অনুপাতের বদলে এটি গোটা বাকি ঋণকাল দেখে।"),
    mcq("What is a 'hurdle rate' for a bridge company's investments?", ["The minimum expected return a project must beat to be approved", "The speed limit on the bridge", "The height of a crash barrier", "The rate at which workers are hired"], 0,
        "It is usually the cost of capital plus a margin for the project's extra risk.",
        "সেতু-কোম্পানির বিনিয়োগে 'বাধা-হার' কী?", ["অনুমোদন পেতে কোনো প্রকল্পকে যে ন্যূনতম প্রত্যাশিত আয় ছাড়াতে হয়", "সেতুর গতিসীমা", "দুর্ঘটনা-রোধক বেড়ার উচ্চতা", "কর্মী নিয়োগের হার"],
        "সাধারণত এটি মূলধনের খরচ আর প্রকল্পের বাড়তি ঝুঁকির একটা মার্জিন মিলিয়ে।"),
    mcq("When a state has only a fixed budget for many possible bridges, why rank them by profitability index?", ["It picks the projects giving the most NPV per rupee invested", "It always picks the biggest bridge", "It ignores costs", "It ranks by alphabetical order"], 0,
        "Under capital rationing, value per rupee matters more than total value of any single project.",
        "রাজ্যের হাতে অনেক সম্ভাব্য সেতুর জন্য নির্দিষ্ট বাজেট থাকলে লাভযোগ্যতা সূচকে সাজানো হয় কেন?", ["এতে বিনিয়োগের প্রতি টাকায় সবচেয়ে বেশি নিট বর্তমান মূল্য দেওয়া প্রকল্প বাছা হয়", "এতে সবসময় সবচেয়ে বড় সেতু বাছা হয়", "এটি খরচ উপেক্ষা করে", "এটি বর্ণানুক্রমে সাজায়"],
        "মূলধন সীমিত হলে কোনো এক প্রকল্পের মোট মূল্যের চেয়ে টাকাপ্রতি মূল্য বেশি গুরুত্বপূর্ণ।"),
    mcq("Why can a profitable bridge contractor still go bankrupt?", ["It can run out of cash when payments are delayed while wages and suppliers must be paid now", "Profit is illegal for contractors", "Bankruptcy only depends on the weather", "Profitable firms never pay tax"], 0,
        "Profit is on paper; cash pays the bills. Working capital management keeps a firm alive.",
        "লাভজনক সেতু-ঠিকাদারও দেউলিয়া হতে পারে কেন?", ["পেমেন্ট আটকে থাকলে নগদ ফুরিয়ে যেতে পারে, অথচ মজুরি আর সরবরাহকারীর টাকা এখনই দিতে হয়", "ঠিকাদারের লাভ বেআইনি", "দেউলিয়া হওয়া শুধু আবহাওয়ার উপর নির্ভর করে", "লাভজনক সংস্থা কখনো কর দেয় না"],
        "লাভ খাতায়-কলমে; বিল মেটায় নগদ। চলতি মূলধনের ব্যবস্থাপনাই সংস্থাকে বাঁচিয়ে রাখে।"),
    mcq("What is 'terminal value' when valuing a toll-bridge company?", ["A single figure for the value of all cash flows beyond the detailed forecast years", "The value of the bus terminal", "The scrap value of the toll booths", "The final day's toll takings"], 0,
        "For long-lived assets it is often the largest part of the valuation, so its assumptions deserve careful checking.",
        "টোল-সেতু কোম্পানির মূল্যায়নে 'অন্তিম মূল্য' কী?", ["বিস্তারিত পূর্বাভাসের বছরগুলির পরের সব নগদপ্রবাহের মূল্য, একটা সংখ্যায়", "বাস-টার্মিনালের মূল্য", "টোল-বুথের ভাঙা-মূল্য", "শেষ দিনের টোল-আদায়"],
        "দীর্ঘজীবী সম্পদের ক্ষেত্রে এটিই প্রায়ই মূল্যায়নের সবচেয়ে বড় অংশ, তাই এর অনুমান সাবধানে যাচাই করা দরকার।"),
    mcq("In a bridge budget, how does a 'contingency' differ from an 'escalation' allowance?", ["Contingency covers unknown risks and surprises; escalation covers expected price rises over the building period", "They are two names for the same thing", "Contingency is the contractor's profit; escalation is tax", "Escalation pays for lifts on the bridge"], 0,
        "One money pot is for things that might go wrong, the other for inflation we already expect - mixing them hides how much risk is really covered.",
        "সেতুর বাজেটে 'আকস্মিক-ব্যয় সংস্থান' আর 'মূল্যবৃদ্ধি সংস্থান'-এর তফাত কী?", ["আকস্মিক সংস্থান অজানা ঝুঁকি আর অপ্রত্যাশিত ঘটনা ঢাকে; মূল্যবৃদ্ধি সংস্থান নির্মাণকালে প্রত্যাশিত দাম-বৃদ্ধি ঢাকে", "দুটো একই জিনিসের দুই নাম", "আকস্মিক সংস্থান ঠিকাদারের লাভ; মূল্যবৃদ্ধি হল কর", "মূল্যবৃদ্ধি সংস্থানে সেতুর লিফটের খরচ মেটে"],
        "একটা তহবিল যা ভুল হতে পারে তার জন্য, অন্যটা আগে থেকেই প্রত্যাশিত মূল্যস্ফীতির জন্য — মিশিয়ে ফেললে আসলে কতটা ঝুঁকি ঢাকা আছে তা লুকিয়ে যায়।"),
)
