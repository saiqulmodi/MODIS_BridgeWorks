"""Class 11 - Finance (Senior Engineer): the EMI formula and amortisation, debt service coverage
(DSCR), present value of single sums and annuities, perpetuities, the weighted average cost of
capital, interest tax shields, lease versus buy, toll-revenue forecasting, sensitivity analysis,
and how project finance shares risk in public-private bridge projects."""
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


def _rs(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=""):
    o = _o(r, *alts)
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:,.2f}"
    return mcq(q_en, [f"Rs {f(x)}{u_en}" for x in o], 0, ex_en, q_bn, [f"{f(x)}{u_bn} টাকা" for x in o], ex_bn)


def _num(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    o = _o(r, *alts)
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [f"{f(x)}{u_en}" for x in o], 0, ex_en, q_bn, [f"{f(x)}{ub}" for x in o], ex_bn)


def emi(p, annual, years):
    r = annual / 1200
    n = years * 12
    e = round(p * r * (1 + r) ** n / ((1 + r) ** n - 1))
    flat = round(p * (1 + annual * years / 100) / n)
    return _rs(f"What is the monthly EMI on a Rs {p:,} loan at {annual}% a year over {years} years? (EMI = P r (1 + r)ⁿ ÷ ((1 + r)ⁿ - 1), r monthly)",
               f"বছরে {annual}% হারে {years} বছরে {p:,} টাকার ঋণের মাসিক ইএমআই কত? (ইএমআই = P r (1 + r)ⁿ ÷ ((1 + r)ⁿ - 1), r মাসিক)", e,
               f"r = {annual}/1,200 = {r:.5f}, n = {n}; EMI ≈ Rs {e:,}. Total paid ≈ Rs {e * n:,}, so interest ≈ Rs {e * n - p:,}.",
               f"r = {annual}/1,200 = {r:.5f}, n = {n}; ইএমআই ≈ {e:,} টাকা। মোট দেওয়া ≈ {e * n:,} টাকা, তাই সুদ ≈ {e * n - p:,} টাকা।",
               (flat, round(p / n), round(p * r)))


def dscr(cfads, service, what_en, what_bn):
    r = _c(cfads / service)
    return _num(f"{what_en} generates Rs {cfads:,} crore a year of cash available for debt service. Its loan repayments are Rs {service:,} crore a year. What is the DSCR?",
                f"{what_bn} বছরে {cfads:,} কোটি টাকা ঋণ-পরিশোধে উপলব্ধ নগদ দেয়। ঋণ-শোধ বছরে {service:,} কোটি টাকা। ডিএসসিআর কত?", r,
                f"DSCR = {cfads:,} ÷ {service:,} = {r:g}. Lenders on toll projects often want at least 1.3-1.5.",
                f"ডিএসসিআর = {cfads:,} ÷ {service:,} = {r:g}। টোল-প্রকল্পে ঋণদাতারা প্রায়ই অন্তত 1.3-1.5 চান।",
                (_c(service / cfads), cfads - service, _c(r + 0.5)))


def pv1(fv, rate, years):
    r = round(fv / (1 + rate / 100) ** years)
    return _rs(f"A bridge repair worth Rs {fv:,} will be needed in {years} years. At a discount rate of {rate}%, what is its present value?",
               f"{years} বছর পরে {fv:,} টাকার একটা সেতু-মেরামত লাগবে। {rate}% বাট্টা-হারে এর বর্তমান মূল্য কত?", r,
               f"PV = {fv:,} ÷ 1.{rate:02d}^{years} ≈ Rs {r:,}.",
               f"বর্তমান মূল্য = {fv:,} ÷ 1.{rate:02d}^{years} ≈ {r:,} টাকা।",
               (fv - fv * rate * years // 100, round(fv * (1 + rate / 100) ** years), round(fv / (1 + rate * years / 100)) if round(fv / (1 + rate * years / 100)) != r else r + 500))


def pva(a, rate, years):
    r = round(a * (1 - (1 + rate / 100) ** -years) / (rate / 100))
    return _rs(f"A toll concession pays Rs {a:,} lakh at the end of each year for {years} years. At {rate}%, what is the present value of these payments?",
               f"একটা টোল-ছাড় {years} বছর ধরে প্রতি বছরের শেষে {a:,} লাখ টাকা দেয়। {rate}%-এ এই পেমেন্টের বর্তমান মূল্য কত?", r,
               f"Annuity PV = A x (1 - 1.{rate:02d}^-{years}) ÷ {rate / 100:g} ≈ Rs {r:,} lakh - less than the simple total of Rs {a * years:,} lakh.",
               f"বার্ষিকীর বর্তমান মূল্য = A x (1 - 1.{rate:02d}^-{years}) ÷ {rate / 100:g} ≈ {r:,} লাখ টাকা - সরল মোট {a * years:,} লাখের চেয়ে কম।",
               (a * years, round(a * years / (1 + rate / 100)), round(a / (rate / 100))), " lakh", " লাখ")


def perp(a, rate):
    r = round(a * 100 / rate)
    return _rs(f"A bridge endowment must pay Rs {a:,} lakh a year for maintenance forever. If it earns {rate}% a year, how large must the fund be?",
               f"একটা সেতু-তহবিলকে চিরকাল রক্ষণাবেক্ষণে বছরে {a:,} লাখ টাকা দিতে হবে। বছরে {rate}% আয় করলে তহবিল কত বড় হতে হবে?", r,
               f"Perpetuity PV = payment ÷ rate = {a:,} ÷ {rate / 100:g} = Rs {r:,} lakh.",
               f"চিরস্থায়ী বার্ষিকীর বর্তমান মূল্য = পেমেন্ট ÷ হার = {a:,} ÷ {rate / 100:g} = {r:,} লাখ টাকা।",
               (a * rate, a * 100, r // 2), " lakh", " লাখ")


def wacc(e, d, re, rd, t):
    v = e + d
    w = _c(e / v * re + d / v * rd * (1 - t / 100))
    return _num(f"A bridge company is funded {e}% by equity costing {re}% and {d}% by debt costing {rd}% before tax. The tax rate is {t}%. What is its WACC?",
                f"একটা সেতু-কোম্পানির অর্থের {e}% মূলধন ({re}% খরচ) আর {d}% ঋণ (করের আগে {rd}% খরচ)। করহার {t}%। এর ডব্লিউএসিসি কত?", w,
                f"WACC = {e / 100:g} x {re} + {d / 100:g} x {rd} x (1 - {t / 100:g}) = {w:g}%. Projects must earn more than this to create value.",
                f"ডব্লিউএসিসি = {e / 100:g} x {re} + {d / 100:g} x {rd} x (1 - {t / 100:g}) = {w:g}%। মূল্য তৈরি করতে প্রকল্পকে এর বেশি আয় করতে হবে।",
                (_c((re + rd) / 2), _c(e / v * re + d / v * rd), _c(w + 2)), "%")


def shield(interest, tax):
    r = interest * tax // 100
    return _rs(f"A contractor pays Rs {interest:,} of interest on business loans in a year. Interest is tax-deductible and the tax rate is {tax}%. How much tax does the interest save?",
               f"একজন ঠিকাদার বছরে ব্যবসায়িক ঋণে {interest:,} টাকা সুদ দেন। সুদ করে বাদ যায় আর করহার {tax}%। সুদের জন্য কত কর বাঁচে?", r,
               f"Tax shield = interest x tax rate = {interest:,} x {tax}% = Rs {r:,} - one reason debt can be cheaper than equity.",
               f"কর-আড়াল = সুদ x করহার = {interest:,} x {tax}% = {r:,} টাকা - ঋণ মূলধনের চেয়ে সস্তা হতে পারার একটা কারণ।",
               (interest - r, interest, r // 2))


def lease_buy(price, resale, lease, years):
    buy = price - resale
    total_lease = lease * years
    cheaper_en, cheaper_bn = ("Buying", "কেনা") if buy < total_lease else ("Leasing", "ভাড়া")
    other_en, other_bn = ("Leasing", "ভাড়া") if cheaper_en == "Buying" else ("Buying", "কেনা")
    return mcq(f"A crane costs Rs {price} lakh to buy and resells for Rs {resale} lakh after {years} years, or it can be leased for Rs {lease} lakh a year. Ignoring interest, which is cheaper?",
               [f"{cheaper_en} (Rs {min(buy, total_lease)} lakh)", f"{other_en} (Rs {max(buy, total_lease)} lakh)", "They cost the same", "Neither has any cost"], 0,
               f"Buying: {price} - {resale} = {buy}; leasing: {lease} x {years} = {total_lease}. A full comparison would also discount the cash flows.",
               f"একটা ক্রেন কিনতে {price} লাখ টাকা, {years} বছর পরে {resale} লাখে বেচা যায়, বা বছরে {lease} লাখে ভাড়া নেওয়া যায়। সুদ বাদে কোনটা সস্তা?",
               [f"{cheaper_bn} ({min(buy, total_lease)} লাখ টাকা)", f"{other_bn} ({max(buy, total_lease)} লাখ টাকা)", "দুটোর খরচ সমান", "কোনোটারই খরচ নেই"],
               f"কেনা: {price} - {resale} = {buy}; ভাড়া: {lease} x {years} = {total_lease}। পুরো তুলনায় নগদপ্রবাহের বাট্টাও ধরতে হয়।")


def _cr(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=""):
    o = _o(r, *alts)
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:,.2f}".rstrip("0").rstrip(".")
    return mcq(q_en, [f"Rs {f(x)} crore" for x in o], 0, ex_en, q_bn, [f"{f(x)} কোটি টাকা" for x in o], ex_bn)


def tollrev(vehicles, toll, days):
    r = _c(vehicles * toll * days / 10_000_000)
    return _cr(f"A toll bridge carries {vehicles:,} vehicles a day at an average toll of Rs {toll}. What is the yearly toll revenue ({days} days)?",
                f"একটা টোল-সেতু দিয়ে দিনে {vehicles:,}টি যান চলে, গড় টোল {toll} টাকা। বার্ষিক টোল-আয় ({days} দিন) কত?", r,
                f"{vehicles:,} x {toll} x {days} = Rs {vehicles * toll * days:,} = Rs {r:g} crore.",
                f"{vehicles:,} x {toll} x {days} = {vehicles * toll * days:,} টাকা = {r:g} কোটি টাকা।",
                (_c(vehicles * toll / 100000), _c(r * 10), _c(r / 2)), " crore", " কোটি টাকা")


def sens(cfads, service, drop):
    new = _c(cfads * (100 - drop) / 100 / service)
    return _num(f"A toll project has cash available for debt service of Rs {cfads} crore and debt service of Rs {service} crore. If traffic income falls {drop}%, what does the DSCR become?",
                f"একটা টোল-প্রকল্পে ঋণ-পরিশোধে উপলব্ধ নগদ {cfads} কোটি টাকা আর ঋণ-শোধ {service} কোটি টাকা। যানবাহনের আয় {drop}% কমলে ডিএসসিআর কত হয়?", new,
                f"New cash = {cfads} x {(100 - drop) / 100:g} = {_c(cfads * (100 - drop) / 100):g}; DSCR = {_c(cfads * (100 - drop) / 100):g} ÷ {service} = {new:g} (it was {_c(cfads / service):g}).",
                f"নতুন নগদ = {cfads} x {(100 - drop) / 100:g} = {_c(cfads * (100 - drop) / 100):g}; ডিএসসিআর = {_c(cfads * (100 - drop) / 100):g} ÷ {service} = {new:g} (আগে ছিল {_c(cfads / service):g})।",
                (_c(cfads / service), _c(new - 0.3) if new > 0.3 else _c(new + 0.4), _c(cfads / service - drop / 100)))


ITEMS = (
    emi(1000000, 12, 5), emi(500000, 10, 3), emi(2000000, 9, 10), emi(300000, 15, 2),
    dscr(30, 20, "A toll bridge", "একটা টোল-সেতু"), dscr(45, 25, "A ring-road project", "একটা বলয়-সড়ক প্রকল্প"),
    dscr(18, 15, "A river-crossing PPP", "একটা নদী-পারাপার পিপিপি"), dscr(66, 40, "An expressway", "একটা এক্সপ্রেসওয়ে"),
    pv1(1000000, 10, 2), pv1(500000, 8, 3), pv1(2000000, 6, 5), pv1(800000, 12, 4),
    pva(100, 10, 5), pva(50, 8, 10), pva(200, 12, 3),
    perp(20, 5), perp(36, 8), perp(15, 6),
    wacc(60, 40, 14, 10, 30), wacc(40, 60, 16, 9, 25), wacc(50, 50, 12, 8, 30), wacc(70, 30, 15, 10, 20),
    shield(500000, 30), shield(1200000, 25), shield(80000, 20),
    lease_buy(120, 40, 18, 5), lease_buy(80, 30, 9, 5), lease_buy(200, 50, 40, 4),
    tollrev(20000, 100, 365), tollrev(8000, 60, 360), tollrev(50000, 150, 365),
    sens(30, 20, 20), sens(45, 30, 10), sens(24, 16, 25), sens(52, 32, 15),
    emi(800000, 11, 4), dscr(28, 16, "A metro viaduct", "একটা মেট্রো-উড়ালপথ"), pv1(1500000, 9, 3), pva(80, 9, 6), perp(24, 4),
    wacc(55, 45, 13, 9, 25), shield(900000, 30), lease_buy(150, 60, 20, 5), tollrev(30000, 80, 365),
    mcq("What does an amortisation schedule show?", ["For each payment, how much goes to interest, how much to principal, and the balance left", "Only the total loan", "The bank's opening hours", "The tax rate"], 0,
        "Early payments are mostly interest; later ones mostly principal.",
        "পরিশোধ-সূচি (অ্যামর্টাইজেশন শিডিউল) কী দেখায়?", ["প্রতিটা কিস্তিতে কত সুদে, কত আসলে যায়, আর কত বাকি থাকে", "শুধু মোট ঋণ", "ব্যাংক খোলার সময়", "করের হার"],
        "শুরুর কিস্তি বেশিরভাগ সুদ; পরেরগুলো বেশিরভাগ আসল।"),
    mcq("Why does more of each EMI go to principal as a loan gets older?", ["Interest is charged on a falling balance, so the interest part shrinks while the EMI stays the same", "Banks lower the rate each month", "EMIs rise every year", "Principal disappears"], 0,
        "That is why prepaying early saves the most interest.",
        "ঋণ পুরোনো হলে প্রতিটা ইএমআই-এর বেশি অংশ আসলে যায় কেন?", ["সুদ কমতে-থাকা বকেয়ার উপর, তাই ইএমআই একই থাকলেও সুদের অংশ ছোট হয়", "ব্যাংক প্রতি মাসে হার কমায়", "প্রতি বছর ইএমআই বাড়ে", "আসল মিলিয়ে যায়"],
        "তাই আগেভাগে শোধ করলে সবচেয়ে বেশি সুদ বাঁচে।"),
    mcq("What does a DSCR of 1.5 mean?", ["Cash available is 1.5 times the debt payments due - a 50% cushion", "The loan is 1.5 times the project", "Profit is 1.5%", "The project loses money"], 0,
        "Lenders want a cushion in case traffic or revenue falls.",
        "1.5-এর ডিএসসিআর মানে কী?", ["উপলব্ধ নগদ প্রাপ্য ঋণ-শোধের 1.5 গুণ - 50% গদি", "ঋণ প্রকল্পের 1.5 গুণ", "লাভ 1.5%", "প্রকল্প লোকসানে"],
        "যান বা আয় কমলে যাতে গদি থাকে, ঋণদাতারা তা চান।"),
    mcq("What is 'project finance'?", ["Funding a project through a separate company whose loans are repaid from that project's own cash flows", "A personal loan for an engineer", "A government grant only", "Paying cash from the owner's pocket"], 0,
        "The project company is often called a special purpose vehicle (SPV).",
        "'প্রকল্প-অর্থায়ন' কী?", ["আলাদা কোম্পানির মাধ্যমে প্রকল্পের অর্থায়ন, যার ঋণ সেই প্রকল্পের নিজের নগদপ্রবাহ থেকে শোধ হয়", "প্রকৌশলীর ব্যক্তিগত ঋণ", "শুধু সরকারি অনুদান", "মালিকের পকেট থেকে নগদ"],
        "প্রকল্প-কোম্পানিকে প্রায়ই বিশেষ উদ্দেশ্য সংস্থা (এসপিভি) বলে।"),
    mcq("What is a 'special purpose vehicle' (SPV) in a toll-bridge deal?", ["A company created just to own, build and run that one project", "A truck for special loads", "A government ministry", "A bank account"], 0,
        "It keeps the project's risks and finances separate from the sponsors' other businesses.",
        "টোল-সেতুর চুক্তিতে 'বিশেষ উদ্দেশ্য সংস্থা' (এসপিভি) কী?", ["শুধু সেই একটা প্রকল্পের মালিকানা, নির্মাণ আর চালনার জন্য তৈরি কোম্পানি", "বিশেষ বোঝার ট্রাক", "সরকারি মন্ত্রক", "ব্যাংক-অ্যাকাউন্ট"],
        "প্রকল্পের ঝুঁকি আর অর্থ উদ্যোক্তাদের অন্য ব্যবসা থেকে আলাদা রাখে।"),
    mcq("What does 'non-recourse' debt mean?", ["Lenders can only claim the project's assets and cash, not the sponsors' other assets", "The loan never has to be repaid", "Lenders can take the sponsors' homes", "Interest is zero"], 0,
        "So lenders study the project's cash flows very carefully.",
        "'আশ্রয়হীন' (নন-রিকোর্স) ঋণ মানে কী?", ["ঋণদাতারা শুধু প্রকল্পের সম্পদ আর নগদ দাবি করতে পারেন, উদ্যোক্তাদের অন্য সম্পদ নয়", "ঋণ কখনো শোধ করতে হয় না", "ঋণদাতারা উদ্যোক্তাদের বাড়ি নিতে পারেন", "সুদ শূন্য"],
        "তাই ঋণদাতারা প্রকল্পের নগদপ্রবাহ খুব যত্নে দেখেন।"),
    mcq("What is the 'discount rate' in present value calculations?", ["The rate used to convert future money into today's value, reflecting interest and risk", "A shop discount", "A tax rate", "The inflation rate always"], 0,
        "Riskier projects use higher discount rates.",
        "বর্তমান মূল্যের হিসাবে 'বাট্টা-হার' কী?", ["ভবিষ্যতের টাকাকে আজকের মূল্যে বদলাতে ব্যবহৃত হার, যা সুদ আর ঝুঁকি প্রতিফলিত করে", "দোকানের ছাড়", "করের হার", "সবসময় মুদ্রাস্ফীতির হার"],
        "বেশি ঝুঁকির প্রকল্পে বেশি বাট্টা-হার ব্যবহার হয়।"),
    mcq("Why is the present value of a payment smaller the further in the future it is?", ["It must be discounted for more years, because money today could earn interest meanwhile", "Future money is fake", "Inflation is always zero", "It is not smaller"], 0,
        "A payment 30 years away is worth much less today.",
        "কোনো পেমেন্ট ভবিষ্যতে যত দূরে, তার বর্তমান মূল্য তত ছোট কেন?", ["বেশি বছর ধরে বাট্টা দিতে হয়, কারণ আজকের টাকা এর মধ্যে সুদ আয় করতে পারত", "ভবিষ্যতের টাকা নকল", "মুদ্রাস্ফীতি সবসময় শূন্য", "ছোট নয়"],
        "30 বছর দূরের পেমেন্টের দাম আজ অনেক কম।"),
    mcq("What is an 'annuity'?", ["A series of equal payments made at regular intervals for a set time", "A one-off payment", "A type of insurance claim only", "A yearly holiday"], 0,
        "EMIs, pensions and fixed toll concessions are annuities.",
        "'বার্ষিকী' (অ্যানুইটি) কী?", ["নির্দিষ্ট সময় ধরে নিয়মিত অন্তরে সমান পেমেন্টের সারি", "একবারের পেমেন্ট", "শুধু এক রকম বিমা-দাবি", "বার্ষিক ছুটি"],
        "ইএমআই, পেনশন আর নির্দিষ্ট টোল-ছাড় বার্ষিকী।"),
    mcq("What is a 'perpetuity'?", ["An annuity that continues forever", "A loan with no interest", "A very short loan", "A tax-free bond only"], 0,
        "Its present value is simply payment ÷ interest rate.",
        "'চিরস্থায়ী বার্ষিকী' (পারপেচুইটি) কী?", ["যে বার্ষিকী চিরকাল চলে", "সুদহীন ঋণ", "খুব ছোট ঋণ", "শুধু করমুক্ত বন্ড"],
        "এর বর্তমান মূল্য সোজা পেমেন্ট ÷ সুদের হার।"),
    mcq("What does WACC represent for a company?", ["The average return it must pay its investors and lenders, weighted by how it is funded", "Its total wages", "Its tax bill", "The price of its shares"], 0,
        "It is often used as the discount rate for new projects.",
        "কোম্পানির জন্য ডব্লিউএসিসি কী বোঝায়?", ["অর্থায়নের ভাগ অনুযায়ী ভারযুক্ত, বিনিয়োগকারী আর ঋণদাতাদের যে গড় লাভ দিতে হয়", "মোট মজুরি", "করের বিল", "শেয়ারের দাম"],
        "নতুন প্রকল্পের বাট্টা-হার হিসেবে প্রায়ই ব্যবহার হয়।"),
    mcq("Why is equity usually more expensive than debt for a company?", ["Shareholders take more risk - they are paid last - so they expect higher returns", "Shares have no risk", "Debt has no interest", "Equity is always cheaper"], 0,
        "Debt interest is also tax-deductible, lowering its cost further.",
        "কোম্পানির জন্য মূলধন সাধারণত ঋণের চেয়ে দামি কেন?", ["শেয়ারহোল্ডাররা বেশি ঝুঁকি নেন - তাঁরা সবার শেষে পান - তাই বেশি লাভ আশা করেন", "শেয়ারে ঝুঁকি নেই", "ঋণে সুদ নেই", "মূলধন সবসময় সস্তা"],
        "ঋণের সুদ করে বাদও যায়, খরচ আরও কমে।"),
    mcq("What is an 'interest tax shield'?", ["The tax saved because interest payments reduce taxable profit", "A shield against high interest rates", "Insurance for loans", "A tax on interest earned"], 0,
        "It is worth interest x tax rate each year.",
        "'সুদের কর-আড়াল' কী?", ["সুদ করযোগ্য লাভ কমায় বলে যে কর বাঁচে", "উচ্চ সুদের হারের বিরুদ্ধে ঢাল", "ঋণের বিমা", "অর্জিত সুদে কর"],
        "প্রতি বছর এর মূল্য সুদ x করহার।"),
    mcq("Why can too much debt be dangerous even with a tax shield?", ["Fixed repayments must be met even in bad years, raising the risk of default", "Debt has no repayments", "Tax shields grow forever", "Banks forgive all debts"], 0,
        "Companies balance tax benefits against financial distress risk.",
        "কর-আড়াল থাকলেও বেশি ঋণ বিপজ্জনক হতে পারে কেন?", ["খারাপ বছরেও নির্দিষ্ট শোধ মেটাতে হয়, খেলাপির ঝুঁকি বাড়ে", "ঋণে শোধ নেই", "কর-আড়াল চিরকাল বাড়ে", "ব্যাংক সব ঋণ মাফ করে"],
        "কোম্পানি কর-সুবিধা আর আর্থিক বিপদের ঝুঁকির ভারসাম্য রাখে।"),
    mcq("What is 'operating leverage'?", ["A high share of fixed costs, so profits swing sharply when sales change", "Using a lever to lift loads", "Borrowing money", "Paying staff more"], 0,
        "Toll bridges have high fixed costs and low running costs - strong operating leverage.",
        "'পরিচালন-লিভারেজ' কী?", ["স্থির খরচের বড় ভাগ, তাই বিক্রি বদলালে লাভ তীব্রভাবে দোলে", "বোঝা তুলতে লিভার ব্যবহার", "টাকা ধার করা", "কর্মীদের বেশি বেতন"],
        "টোল-সেতুর স্থির খরচ বেশি আর চালানোর খরচ কম - জোরালো পরিচালন-লিভারেজ।"),
    mcq("What does 'sensitivity analysis' test in a bridge project's financial model?", ["How results change when one key input, like traffic or interest rate, is changed", "The bridge's sensitivity to touch", "The colour scheme", "Workers' feelings only"], 0,
        "It shows which assumptions matter most.",
        "সেতু-প্রকল্পের আর্থিক মডেলে 'সংবেদনশীলতা-বিশ্লেষণ' কী পরীক্ষা করে?", ["যান বা সুদের হারের মতো একটা মূল ইনপুট বদলালে ফল কীভাবে বদলায়", "স্পর্শে সেতুর সংবেদনশীলতা", "রঙের পরিকল্পনা", "শুধু কর্মীদের অনুভূতি"],
        "কোন অনুমান সবচেয়ে গুরুত্বপূর্ণ তা দেখায়।"),
    mcq("What is 'scenario analysis'?", ["Testing the model under several combined situations, such as a recession with high interest rates", "Drawing scenery", "A single best guess", "Ignoring risks"], 0,
        "Lenders often ask for a 'downside case'.",
        "'পরিস্থিতি-বিশ্লেষণ' কী?", ["কয়েকটা সম্মিলিত পরিস্থিতিতে মডেল পরীক্ষা, যেমন উচ্চ সুদের সঙ্গে মন্দা", "দৃশ্য আঁকা", "একটা সেরা আন্দাজ", "ঝুঁকি উপেক্ষা"],
        "ঋণদাতারা প্রায়ই একটা 'খারাপ পরিস্থিতি' চান।"),
    mcq("Why do traffic forecasts for new toll bridges often turn out too optimistic?", ["Sponsors may overestimate demand to make projects look viable, and drivers may avoid tolls", "Traffic always grows faster than expected", "Forecasts are always exact", "Tolls attract more traffic"], 0,
        "Independent traffic studies and conservative cases protect lenders and the public.",
        "নতুন টোল-সেতুর যান-পূর্বাভাস প্রায়ই অতি-আশাবাদী হয় কেন?", ["প্রকল্প লাভজনক দেখাতে উদ্যোক্তারা চাহিদা বেশি ধরতে পারেন, আর চালকরা টোল এড়াতে পারেন", "যান সবসময় প্রত্যাশার চেয়ে দ্রুত বাড়ে", "পূর্বাভাস সবসময় নিখুঁত", "টোল বেশি যান টানে"],
        "স্বাধীন যান-সমীক্ষা আর সাবধানী পরিস্থিতি ঋণদাতা আর জনসাধারণকে রক্ষা করে।"),
    mcq("What is 'traffic risk' in a toll-bridge PPP?", ["The risk that fewer vehicles use the bridge than forecast, reducing income", "The risk of traffic accidents only", "Noise from traffic", "The risk of potholes"], 0,
        "Annuity and hybrid models move some of this risk back to the government.",
        "টোল-সেতু পিপিপি-তে 'যান-ঝুঁকি' কী?", ["পূর্বাভাসের চেয়ে কম যান সেতু ব্যবহার করে আয় কমার ঝুঁকি", "শুধু পথ-দুর্ঘটনার ঝুঁকি", "যানবাহনের শব্দ", "গর্তের ঝুঁকি"],
        "বার্ষিকী আর হাইব্রিড মডেল এই ঝুঁকির কিছুটা সরকারের দিকে ফেরায়।"),
    mcq("What is the principle of 'risk allocation' in PPP contracts?", ["Each risk should be carried by the party best able to manage it", "All risks go to the government", "All risks go to the contractor", "Risks are ignored"], 0,
        "Construction risk usually sits with the builder; land acquisition risk with the government.",
        "পিপিপি চুক্তিতে 'ঝুঁকি-বণ্টন'-এর নীতি কী?", ["যে পক্ষ সবচেয়ে ভালো সামলাতে পারে, প্রতিটা ঝুঁকি তার কাঁধে", "সব ঝুঁকি সরকারের", "সব ঝুঁকি ঠিকাদারের", "ঝুঁকি উপেক্ষা"],
        "নির্মাণ-ঝুঁকি সাধারণত নির্মাতার; জমি-অধিগ্রহণের ঝুঁকি সরকারের।"),
    mcq("What is 'refinancing' a project loan?", ["Replacing an existing loan with a new one, often on better terms once construction risk has passed", "Paying the loan twice", "Cancelling the project", "Increasing the interest rate on purpose"], 0,
        "Lower interest after completion can improve returns.",
        "প্রকল্প-ঋণের 'পুনঃঅর্থায়ন' কী?", ["পুরোনো ঋণের বদলে নতুন ঋণ নেওয়া, প্রায়ই নির্মাণ-ঝুঁকি পেরোনোর পরে ভালো শর্তে", "দুবার ঋণ শোধ", "প্রকল্প বাতিল", "ইচ্ছে করে সুদ বাড়ানো"],
        "শেষ হওয়ার পরে কম সুদ লাভ বাড়াতে পারে।"),
    mcq("What is 'construction risk' and why do lenders charge more during building?", ["The chance of delays, cost overruns or failure before the bridge earns income", "The risk of traffic jams after opening", "The colour risk", "There is no risk during construction"], 0,
        "Once the bridge is open and earning, the project is usually safer to lend to.",
        "'নির্মাণ-ঝুঁকি' কী আর নির্মাণের সময় ঋণদাতারা বেশি নেন কেন?", ["সেতু আয় করার আগে দেরি, খরচ বৃদ্ধি বা ব্যর্থতার সম্ভাবনা", "খোলার পরে যানজটের ঝুঁকি", "রঙের ঝুঁকি", "নির্মাণের সময় ঝুঁকি নেই"],
        "সেতু খুলে আয় শুরু হলে প্রকল্পে ধার দেওয়া সাধারণত নিরাপদ।"),
    mcq("What is a 'moratorium' on a project loan?", ["An initial period, often during construction, when no repayments are due", "A penalty for late payment", "A permanent cancellation", "A type of bond"], 0,
        "Interest may still build up during this period.",
        "প্রকল্প-ঋণে 'স্থগিতাদেশ' (মোরাটোরিয়াম) কী?", ["প্রথম দিকের সময়, প্রায়ই নির্মাণের সময়, যখন কোনো শোধ দিতে হয় না", "দেরির জরিমানা", "চিরস্থায়ী বাতিল", "এক রকম বন্ড"],
        "এই সময়েও সুদ জমতে পারে।"),
    mcq("What does 'capitalised interest' mean during construction?", ["Interest that is added to the loan balance instead of being paid in cash", "Interest paid in gold", "Interest written in capital letters", "Interest that is forgiven"], 0,
        "It raises the amount to be repaid once the bridge opens.",
        "নির্মাণের সময় 'মূলধনীকৃত সুদ' মানে কী?", ["নগদে না দিয়ে ঋণের বকেয়ায় যোগ করা সুদ", "সোনায় দেওয়া সুদ", "বড় হাতের অক্ষরে লেখা সুদ", "মাফ করা সুদ"],
        "সেতু খোলার পরে শোধের অঙ্ক বাড়ায়।"),
    mcq("What is 'inflation-indexed' toll pricing?", ["Tolls that rise each year in line with an inflation index, keeping real revenue steady", "Tolls that never change", "Tolls set by drivers", "Tolls that fall each year"], 0,
        "Many Indian toll rules link increases to the wholesale price index.",
        "'মূল্যসূচক-যুক্ত' টোল-দাম কী?", ["মুদ্রাস্ফীতি-সূচকের সঙ্গে তাল রেখে প্রতি বছর বাড়া টোল, প্রকৃত আয় স্থির রাখে", "কখনো না বদলানো টোল", "চালকদের ঠিক করা টোল", "প্রতি বছর কমা টোল"],
        "ভারতের অনেক টোল-নিয়ম বৃদ্ধিকে পাইকারি মূল্যসূচকের সঙ্গে জোড়ে।"),
    mcq("What is 'leasing' equipment?", ["Paying regularly to use an asset owned by someone else", "Buying with cash", "Borrowing from a friend for free", "Selling equipment"], 0,
        "It saves upfront cash and may include maintenance.",
        "যন্ত্রপাতি 'লিজ' নেওয়া কী?", ["অন্যের মালিকানার সম্পদ ব্যবহারের জন্য নিয়মিত টাকা দেওয়া", "নগদে কেনা", "বন্ধুর থেকে বিনামূল্যে ধার", "যন্ত্রপাতি বেচা"],
        "আগাম নগদ বাঁচায় আর রক্ষণাবেক্ষণও থাকতে পারে।"),
    mcq("Why might a contractor lease a special crane instead of buying it?", ["It is needed only for one project, so owning it would leave it idle afterwards", "Leasing is always cheaper in every case", "Buying is illegal", "Leased cranes are stronger"], 0,
        "Buying makes sense when equipment will be used often for years.",
        "একজন ঠিকাদার একটা বিশেষ ক্রেন কেনার বদলে লিজ নিতে পারেন কেন?", ["শুধু একটা প্রকল্পে লাগবে, তাই মালিক হলে পরে অলস পড়ে থাকবে", "লিজ সব ক্ষেত্রে সবসময় সস্তা", "কেনা বেআইনি", "লিজের ক্রেন বেশি শক্ত"],
        "বছরের পর বছর ঘন ঘন ব্যবহার হলে কেনা যুক্তিসঙ্গত।"),
    mcq("What is the 'internal rate of return' (IRR) of a project?", ["The discount rate at which the project's net present value is zero", "The bank's interest rate", "The tax rate", "The inflation rate"], 0,
        "If IRR exceeds the cost of capital, the project adds value.",
        "প্রকল্পের 'অভ্যন্তরীণ লাভের হার' (আইআরআর) কী?", ["যে বাট্টা-হারে প্রকল্পের নিট বর্তমান মূল্য শূন্য", "ব্যাংকের সুদের হার", "করের হার", "মুদ্রাস্ফীতির হার"],
        "আইআরআর মূলধনের খরচ ছাড়ালে প্রকল্প মূল্য যোগ করে।"),
    mcq("A project has an IRR of 14% and the company's WACC is 10%. What does this suggest?", ["The project is expected to earn more than its cost of funds, so it adds value", "It will lose money", "It breaks even exactly", "IRR and WACC cannot be compared"], 0,
        "Risks and assumptions still need checking.",
        "একটা প্রকল্পের আইআরআর 14% আর কোম্পানির ডব্লিউএসিসি 10%। এতে কী বোঝা যায়?", ["প্রকল্প তহবিলের খরচের চেয়ে বেশি আয় করবে বলে আশা, তাই মূল্য যোগ করে", "লোকসান হবে", "ঠিক লাভ-লোকসান সমান", "আইআরআর আর ডব্লিউএসিসি তুলনা করা যায় না"],
        "ঝুঁকি আর অনুমান তবু যাচাই করতে হয়।"),
    mcq("What is 'equity IRR' versus 'project IRR'?", ["Equity IRR is the return to shareholders after debt; project IRR is the return on the whole investment", "They are always identical", "Equity IRR ignores shareholders", "Project IRR is only for banks"], 0,
        "Debt can raise equity IRR - and its risk.",
        "'মূলধন-আইআরআর' আর 'প্রকল্প-আইআরআর'-এর পার্থক্য কী?", ["মূলধন-আইআরআর ঋণের পরে শেয়ারহোল্ডারদের লাভ; প্রকল্প-আইআরআর পুরো বিনিয়োগের লাভ", "সবসময় হুবহু এক", "মূলধন-আইআরআর শেয়ারহোল্ডারদের উপেক্ষা করে", "প্রকল্প-আইআরআর শুধু ব্যাংকের জন্য"],
        "ঋণ মূলধন-আইআরআর বাড়াতে পারে - আর তার ঝুঁকিও।"),
    mcq("What is 'credit enhancement' for an infrastructure bond?", ["Extra support, like a guarantee, that lowers the bond's risk and so its interest rate", "Painting the bond certificate", "Raising the interest rate", "Cancelling the bond"], 0,
        "It helps projects borrow from pension and insurance funds.",
        "পরিকাঠামো-বন্ডের 'ঋণমান-উন্নয়ন' কী?", ["গ্যারান্টির মতো বাড়তি সমর্থন, যা বন্ডের ঝুঁকি আর তাই সুদের হার কমায়", "বন্ডের শংসাপত্রে রং", "সুদের হার বাড়ানো", "বন্ড বাতিল"],
        "প্রকল্পকে পেনশন আর বিমা-তহবিল থেকে ধার নিতে সাহায্য করে।"),
    mcq("What is an 'InvIT' (infrastructure investment trust) in India?", ["A trust that owns income-producing infrastructure like toll roads and pays investors most of the cash", "A government tax", "A bank loan", "A construction company"], 0,
        "It lets ordinary investors share in toll income.",
        "ভারতে 'ইনভিআইটি' (পরিকাঠামো বিনিয়োগ ট্রাস্ট) কী?", ["টোল-সড়কের মতো আয়কারী পরিকাঠামোর মালিক ট্রাস্ট, যা বিনিয়োগকারীদের নগদের বেশিরভাগ দেয়", "সরকারি কর", "ব্যাংক-ঋণ", "নির্মাণ-কোম্পানি"],
        "সাধারণ বিনিয়োগকারীদের টোল-আয়ের ভাগ নিতে দেয়।"),
    mcq("What is 'asset recycling' (monetisation) of public bridges?", ["Leasing finished, revenue-earning assets to investors and using the money to build new ones", "Melting down old bridges", "Painting bridges again", "Closing toll roads"], 0,
        "India's National Monetisation Pipeline uses this idea.",
        "সরকারি সেতুর 'সম্পদ-পুনর্ব্যবহার' (মুদ্রায়ন) কী?", ["শেষ হওয়া, আয়কারী সম্পদ বিনিয়োগকারীদের লিজ দিয়ে সেই টাকায় নতুন বানানো", "পুরোনো সেতু গলানো", "আবার সেতু রং করা", "টোল-সড়ক বন্ধ"],
        "ভারতের জাতীয় মুদ্রায়ন পাইপলাইন এই ভাবনা ব্যবহার করে।"),
    mcq("What is a 'financial model' for a bridge project?", ["A spreadsheet that forecasts costs, revenues, financing and returns year by year", "A plastic model of the bridge", "A fashion model", "A bank's logo"], 0,
        "Good models are clear, checked and test many assumptions.",
        "সেতু-প্রকল্পের 'আর্থিক মডেল' কী?", ["যে স্প্রেডশিট বছরে বছরে খরচ, আয়, অর্থায়ন আর লাভের পূর্বাভাস দেয়", "সেতুর প্লাস্টিক-মডেল", "ফ্যাশন-মডেল", "ব্যাংকের লোগো"],
        "ভালো মডেল স্পষ্ট, যাচাই-করা আর অনেক অনুমান পরীক্ষা করে।"),
    mcq("Why should a financial model's assumptions be listed separately and clearly?", ["So others can check them, change them easily and see how results depend on them", "To hide them", "To make the file larger", "Assumptions do not matter"], 0,
        "Hidden assumptions are a common source of costly errors.",
        "আর্থিক মডেলের অনুমান আলাদা আর স্পষ্ট করে লেখা উচিত কেন?", ["যাতে অন্যরা যাচাই করতে, সহজে বদলাতে আর ফল কীভাবে নির্ভর করে দেখতে পারে", "লুকোতে", "ফাইল বড় করতে", "অনুমান গুরুত্বহীন"],
        "লুকোনো অনুমান দামি ভুলের সাধারণ উৎস।"),
    mcq("What is 'viability gap funding' (VGF) in Indian PPPs?", ["A government grant that covers part of the cost so a socially useful but not fully profitable project can attract private investors", "A loan to the government", "A tax on tolls", "A penalty for late completion"], 0,
        "It can be up to a set share of the project cost.",
        "ভারতীয় পিপিপি-তে 'লাভজনকতা-ঘাটতি অর্থায়ন' (ভিজিএফ) কী?", ["সরকারি অনুদান, যা খরচের একটা অংশ মেটায়, যাতে সামাজিকভাবে কাজের কিন্তু পুরো লাভজনক নয় এমন প্রকল্প বেসরকারি বিনিয়োগ টানে", "সরকারকে ঋণ", "টোলের উপর কর", "দেরিতে শেষ করার জরিমানা"],
        "প্রকল্প-খরচের একটা নির্দিষ্ট ভাগ পর্যন্ত হতে পারে।"),
    mcq("What is 'termination payment' in a concession agreement?", ["Compensation set in advance if the contract ends early, depending on who caused it", "A bonus for finishing", "A final toll", "A worker's salary"], 0,
        "It protects lenders and gives both sides certainty.",
        "ছাড়-চুক্তিতে 'সমাপ্তি-পেমেন্ট' কী?", ["চুক্তি আগে শেষ হলে আগেই ঠিক করা ক্ষতিপূরণ, কে কারণ তার উপর নির্ভর করে", "শেষ করার বোনাস", "শেষ টোল", "কর্মীর বেতন"],
        "ঋণদাতাদের রক্ষা করে আর দুপক্ষকে নিশ্চয়তা দেয়।"),
    mcq("What is 'hand-back condition' at the end of a toll concession?", ["The required state of the bridge when it is returned to the government, checked by inspection", "The bridge is given away free to anyone", "The tolls are returned to drivers", "A handshake ceremony"], 0,
        "It stops operators from skipping maintenance near the end.",
        "টোল-ছাড়ের শেষে 'ফেরত-দেওয়ার শর্ত' কী?", ["সরকারকে ফেরত দেওয়ার সময় সেতুর প্রয়োজনীয় অবস্থা, পরিদর্শনে যাচাই হয়", "যে কাউকে বিনামূল্যে সেতু দেওয়া", "চালকদের টোল ফেরত", "করমর্দন-অনুষ্ঠান"],
        "শেষের দিকে পরিচালককে রক্ষণাবেক্ষণ এড়াতে দেয় না।"),
    mcq("Why do toll concessions often require a 'major maintenance reserve'?", ["Cash is set aside regularly so big resurfacing and bearing replacement can be paid for when due", "To pay bonuses", "To lower tolls", "It is not required"], 0,
        "Without it, large repairs could leave the project short of cash.",
        "টোল-ছাড়ে প্রায়ই 'বড় রক্ষণাবেক্ষণ-সংরক্ষণ' লাগে কেন?", ["নিয়মিত নগদ সরিয়ে রাখা হয়, যাতে সময়মতো বড় পুনর্বাঁধানো আর বিয়ারিং বদলের খরচ মেটানো যায়", "বোনাস দিতে", "টোল কমাতে", "লাগে না"],
        "এটা না থাকলে বড় মেরামতে প্রকল্পের নগদ কম পড়তে পারে।"),
    mcq("What is 'currency mismatch' risk for a project borrowing in dollars?", ["Tolls are earned in rupees but debt is owed in dollars, so a falling rupee raises repayments", "Using two currencies in a shop", "Printing money", "There is no such risk"], 0,
        "Hedging or borrowing in rupees reduces it.",
        "ডলারে ধার নেওয়া প্রকল্পের 'মুদ্রা-অসামঞ্জস্য' ঝুঁকি কী?", ["টোল আয় টাকায়, কিন্তু ঋণ ডলারে, তাই টাকা পড়লে শোধ বাড়ে", "দোকানে দুটো মুদ্রা ব্যবহার", "টাকা ছাপানো", "এমন ঝুঁকি নেই"],
        "হেজিং বা টাকায় ধার নেওয়া এটা কমায়।"),
    mcq("What is a 'cash waterfall' in project finance?", ["The fixed order in which project cash is used: operating costs, debt service, reserves, then shareholders", "A waterfall near the bridge", "Random spending", "Paying shareholders first"], 0,
        "Shareholders are paid only after lenders and reserves are covered.",
        "প্রকল্প-অর্থায়নে 'নগদ-জলপ্রপাত' কী?", ["প্রকল্পের নগদ ব্যবহারের নির্দিষ্ট ক্রম: পরিচালন-খরচ, ঋণ-শোধ, সংরক্ষণ, তারপর শেয়ারহোল্ডার", "সেতুর কাছে জলপ্রপাত", "এলোমেলো খরচ", "আগে শেয়ারহোল্ডারদের দেওয়া"],
        "ঋণদাতা আর সংরক্ষণ মেটার পরেই শেয়ারহোল্ডাররা পান।"),
    mcq("What is a 'lock-up' covenant in a loan agreement?", ["If DSCR falls below a set level, dividends to shareholders are blocked until it recovers", "A padlock for the site", "A ban on all spending", "A rule to close the bridge at night"], 0,
        "It keeps cash in the project when it is under stress.",
        "ঋণ-চুক্তিতে 'আটক-শর্ত' (লক-আপ কভেন্যান্ট) কী?", ["ডিএসসিআর নির্দিষ্ট মাত্রার নিচে নামলে সেরে না ওঠা পর্যন্ত শেয়ারহোল্ডারদের লভ্যাংশ বন্ধ", "নির্মাণস্থলের তালা", "সব খরচে নিষেধ", "রাতে সেতু বন্ধের নিয়ম"],
        "চাপের সময় নগদ প্রকল্পে রাখে।"),
    mcq("Why do lenders appoint an 'independent engineer' on big bridge loans?", ["To check designs, progress and costs objectively before money is released", "To design the logo", "To collect tolls", "To replace the contractor"], 0,
        "Draw-downs are often tied to certified progress.",
        "বড় সেতু-ঋণে ঋণদাতারা 'স্বাধীন প্রকৌশলী' নিয়োগ করেন কেন?", ["টাকা ছাড়ার আগে নকশা, অগ্রগতি আর খরচ নিরপেক্ষভাবে যাচাই করতে", "লোগো বানাতে", "টোল তুলতে", "ঠিকাদারের বদলি হতে"],
        "টাকা তোলা প্রায়ই প্রত্যয়িত অগ্রগতির সঙ্গে বাঁধা।"),
    mcq("What does 'cost overrun' mean, and how is it usually funded?", ["Spending more than budget; covered by contingency, sponsor support or standby loans agreed in advance", "Spending less than budget", "A bonus for workers", "A fine for drivers"], 0,
        "Good projects agree who pays for overruns before work begins.",
        "'খরচ-বৃদ্ধি' মানে কী, আর সাধারণত কীভাবে অর্থায়ন হয়?", ["বাজেটের বেশি খরচ; আপৎকালীন তহবিল, উদ্যোক্তার সমর্থন বা আগেই ঠিক-করা অপেক্ষমাণ ঋণে মেটানো হয়", "বাজেটের কম খরচ", "কর্মীদের বোনাস", "চালকদের জরিমানা"],
        "ভালো প্রকল্পে কাজ শুরুর আগেই ঠিক হয় বাড়তি খরচ কে দেবে।"),
    mcq("What is 'optimism bias' in project estimates?", ["The tendency to underestimate costs and timescales and overestimate benefits", "Being cheerful at work", "A bias in measuring tools", "Overestimating costs"], 0,
        "Reference-class forecasting, using data from similar projects, corrects for it.",
        "প্রকল্পের হিসাবে 'আশাবাদী পক্ষপাত' কী?", ["খরচ আর সময় কম আর সুফল বেশি ধরার ঝোঁক", "কাজে হাসিখুশি থাকা", "মাপকযন্ত্রের পক্ষপাত", "খরচ বেশি ধরা"],
        "একই রকম প্রকল্পের তথ্য দিয়ে 'তুলনা-শ্রেণি পূর্বাভাস' এটা সংশোধন করে।"),
    mcq("What is a 'benefit-cost ratio' (BCR) for a public bridge?", ["The present value of benefits divided by the present value of costs", "Cost minus benefit", "The toll rate", "The number of lanes"], 0,
        "A BCR above 1 means benefits exceed costs.",
        "সরকারি সেতুর 'সুফল-খরচ অনুপাত' (বিসিআর) কী?", ["সুফলের বর্তমান মূল্য ÷ খরচের বর্তমান মূল্য", "খরচ বিয়োগ সুফল", "টোলের হার", "লেনের সংখ্যা"],
        "বিসিআর 1-এর উপরে মানে সুফল খরচ ছাড়ায়।"),
    mcq("Which benefits are counted in a public bridge's economic appraisal?", ["Travel time saved, lower vehicle costs, fewer accidents and wider economic gains", "Only toll income", "Only construction jobs", "Only the view"], 0,
        "Economic appraisal looks at society as a whole, not just the operator.",
        "সরকারি সেতুর অর্থনৈতিক মূল্যায়নে কোন সুফল গোনা হয়?", ["বাঁচা যাত্রা-সময়, কম গাড়ি-খরচ, কম দুর্ঘটনা আর বৃহত্তর অর্থনৈতিক লাভ", "শুধু টোল-আয়", "শুধু নির্মাণের চাকরি", "শুধু দৃশ্য"],
        "অর্থনৈতিক মূল্যায়ন শুধু পরিচালক নয়, গোটা সমাজকে দেখে।"),
    mcq("What is 'value of time' in transport appraisal?", ["A money value given to time saved by travellers, used to compare benefits with costs", "The price of a watch", "A worker's overtime rate only", "The time a bridge lasts"], 0,
        "Freight and business trips usually have higher values than leisure trips.",
        "পরিবহন-মূল্যায়নে 'সময়ের মূল্য' কী?", ["যাত্রীদের বাঁচা সময়ের টাকার মূল্য, সুফলকে খরচের সঙ্গে তুলনায় ব্যবহার হয়", "ঘড়ির দাম", "শুধু কর্মীর ওভারটাইমের হার", "সেতু কত সময় টেকে"],
        "মাল আর ব্যবসায়িক যাত্রার মূল্য সাধারণত অবসর-যাত্রার চেয়ে বেশি।"),
    mcq("Why is the 'social discount rate' used for public projects often lower than private rates?", ["Society values long-lasting benefits to future generations more than a private investor might", "Governments ignore the future", "It is always higher", "Public projects have no costs"], 0,
        "A lower rate gives more weight to benefits far in the future.",
        "সরকারি প্রকল্পে 'সামাজিক বাট্টা-হার' প্রায়ই বেসরকারি হারের চেয়ে কম হয় কেন?", ["ভবিষ্যৎ প্রজন্মের দীর্ঘস্থায়ী সুফলকে সমাজ একজন বেসরকারি বিনিয়োগকারীর চেয়ে বেশি মূল্য দেয়", "সরকার ভবিষ্যৎ উপেক্ষা করে", "সবসময় বেশি", "সরকারি প্রকল্পে খরচ নেই"],
        "কম হার অনেক দূর ভবিষ্যতের সুফলকে বেশি গুরুত্ব দেয়।"),
    mcq("What is the danger of 'creative accounting' in a toll company?", ["Misleading figures can hide losses, cheat investors and lead to sudden collapse", "It makes accounts more accurate", "It is required by law", "It only affects colours in reports"], 0,
        "Audits, regulators and honest management protect against it.",
        "টোল-কোম্পানিতে 'সৃজনশীল হিসাব'-এর বিপদ কী?", ["বিভ্রান্তিকর সংখ্যা লোকসান লুকোতে, বিনিয়োগকারীদের ঠকাতে আর হঠাৎ পতন ঘটাতে পারে", "হিসাব বেশি সঠিক করে", "আইনে বাধ্যতামূলক", "শুধু প্রতিবেদনের রঙে প্রভাব"],
        "নিরীক্ষা, নিয়ন্ত্রক আর সৎ পরিচালনা এর বিরুদ্ধে রক্ষা করে।"),
    mcq("What is 'whistleblowing' in a construction finance context?", ["Reporting wrongdoing, such as fraud or unsafe cost-cutting, through proper channels", "Blowing a whistle at the site", "Starting the work day", "Calling a lunch break"], 0,
        "Laws protect genuine whistleblowers from retaliation.",
        "নির্মাণ-অর্থের প্রসঙ্গে 'হুইসেল-ব্লোয়িং' কী?", ["প্রতারণা বা অনিরাপদ খরচ-ছাঁটাইয়ের মতো অন্যায় সঠিক পথে জানানো", "নির্মাণস্থলে বাঁশি বাজানো", "কাজের দিন শুরু", "দুপুরের বিরতি ডাকা"],
        "আসল হুইসেল-ব্লোয়ারদের প্রতিশোধ থেকে আইন রক্ষা করে।"),
    mcq("Why is the 'time value of money' central to choosing between two bridge designs?", ["A cheaper-to-build design may cost more over its life once future maintenance is discounted and compared", "Only the building price matters", "Future costs are always zero", "Designs cannot be compared"], 0,
        "Whole-life cost uses present values of all future costs.",
        "দুটো সেতু-নকশার মধ্যে বাছাইয়ে 'টাকার সময়-মূল্য' কেন কেন্দ্রীয়?", ["বানাতে সস্তা নকশাও ভবিষ্যৎ রক্ষণাবেক্ষণের বাট্টা ধরে তুলনা করলে জীবনভর দামি হতে পারে", "শুধু নির্মাণের দাম গুরুত্বপূর্ণ", "ভবিষ্যৎ খরচ সবসময় শূন্য", "নকশা তুলনা করা যায় না"],
        "পূর্ণ-জীবন খরচ সব ভবিষ্যৎ খরচের বর্তমান মূল্য ব্যবহার করে।"),
    mcq("What is 'depreciation' used for in a toll company's tax calculation?", ["It is a non-cash expense that reduces taxable profit, lowering tax", "It increases tax", "It is paid in cash to the government", "It has no effect on tax"], 0,
        "So depreciation affects cash flow through tax, even though no cash leaves.",
        "টোল-কোম্পানির কর-হিসাবে 'অবচয়' কীসের জন্য ব্যবহার হয়?", ["নগদহীন খরচ, যা করযোগ্য লাভ কমিয়ে কর কমায়", "কর বাড়ায়", "সরকারকে নগদে দেওয়া হয়", "করে প্রভাব নেই"],
        "তাই নগদ না বেরোলেও অবচয় করের মাধ্যমে নগদপ্রবাহে প্রভাব ফেলে।"),
    mcq("What is a 'green bond'?", ["A bond whose money must be spent on environmentally beneficial projects, such as low-carbon transport", "A bond printed on green paper", "A bond with no interest", "A loan for buying plants only"], 0,
        "Rail bridges and electrified transit often qualify.",
        "'সবুজ বন্ড' কী?", ["যে বন্ডের টাকা পরিবেশ-উপকারী প্রকল্পে, যেমন কম-কার্বন পরিবহনে, খরচ করতেই হবে", "সবুজ কাগজে ছাপা বন্ড", "সুদহীন বন্ড", "শুধু গাছ কেনার ঋণ"],
        "রেলসেতু আর বিদ্যুৎচালিত গণপরিবহন প্রায়ই যোগ্য হয়।"),
    mcq("What is 'mezzanine finance' in a big project?", ["A layer of funding between senior debt and equity - riskier than loans, so it pays more", "A loan for building a mezzanine floor", "Government grant money", "The safest form of debt"], 0,
        "It is repaid after senior lenders but before shareholders.",
        "বড় প্রকল্পে 'মেজানাইন অর্থায়ন' কী?", ["প্রধান ঋণ আর মূলধনের মাঝের তহবিল-স্তর - ঋণের চেয়ে ঝুঁকিপূর্ণ, তাই বেশি দেয়", "মেজানাইন তলা বানানোর ঋণ", "সরকারি অনুদানের টাকা", "সবচেয়ে নিরাপদ ঋণ"],
        "প্রধান ঋণদাতাদের পরে কিন্তু শেয়ারহোল্ডারদের আগে শোধ হয়।"),
    mcq("Why do multilateral banks such as the World Bank or ADB fund some large bridges?", ["They offer long-term, lower-cost loans and technical expertise for projects with big public benefits", "They own all bridges", "They only give gifts", "They charge the highest interest"], 0,
        "Their involvement also encourages good procurement and environmental standards.",
        "বিশ্বব্যাংক বা এডিবি-র মতো বহুপাক্ষিক ব্যাংক কিছু বড় সেতুতে অর্থ দেয় কেন?", ["বড় জনকল্যাণের প্রকল্পে দীর্ঘমেয়াদি, কম খরচের ঋণ আর কারিগরি দক্ষতা দেয়", "এরা সব সেতুর মালিক", "শুধু উপহার দেয়", "সবচেয়ে বেশি সুদ নেয়"],
        "তাদের যুক্ত থাকা ভালো ক্রয়-পদ্ধতি আর পরিবেশ-মানকেও উৎসাহ দেয়।"),
)
