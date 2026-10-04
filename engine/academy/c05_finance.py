"""Class 5 - Finance (Junior Cadet): simple and compound interest, percentage change, profit and
loss percent, prices with GST, successive discounts, exchange rates, opportunity cost, risk and
return, monthly cash flow, project funding (grants, loans, shortfalls) and honest money habits."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 10, r * 2, r + 1):
        if x not in out and x >= 0:
            out.append(x)
    return out[:4]


def _rs(o):
    return [f"Rs {x:,}" for x in o], [f"{x:,} টাকা" for x in o]


def si(P, r, t):
    i = P * r * t // 100
    en, bn = _rs(_o(i, P * r // 100, P + i, i + P * r // 100))
    return mcq(f"What simple interest does Rs {P:,} earn at {r}% a year for {t} years?", en, 0,
               f"SI = P x R x T ÷ 100 = {P:,} x {r} x {t} ÷ 100 = Rs {i:,}.",
               f"{P:,} টাকায় বছরে {r}% হারে {t} বছরে কত সরল সুদ হয়?", bn,
               f"সরল সুদ = আসল x হার x সময় ÷ 100 = {P:,} x {r} x {t} ÷ 100 = {i:,} টাকা।")


def ci2(P, r):
    a1 = P + P * r // 100
    a2 = a1 + a1 * r // 100
    simple = P + 2 * P * r // 100
    en, bn = _rs(_o(a2, simple, a1, P))
    return mcq(f"Rs {P:,} is saved at {r}% compound interest, added once a year. What is it worth after 2 years?", en, 0,
               f"Year 1: {P:,} + {r}% = {a1:,}. Year 2: {a1:,} + {r}% = {a2:,}. Interest earns interest - more than simple interest's {simple:,}.",
               f"{P:,} টাকা বছরে একবার যোগ হওয়া {r}% চক্রবৃদ্ধি সুদে জমানো হলো। 2 বছর পরে কত হবে?", bn,
               f"বছর 1: {P:,} + {r}% = {a1:,}। বছর 2: {a1:,} + {r}% = {a2:,}। সুদের উপরও সুদ - সরল সুদের {simple:,}-এর চেয়ে বেশি।")


def change(old, new, what_en, what_bn):
    d = new - old
    p = abs(d) * 100 // old
    word_en, word_bn = ("increase", "বৃদ্ধি") if d > 0 else ("decrease", "হ্রাস")
    o = _o(p, abs(d) * 100 // new, abs(d), p + 5)
    return mcq(f"{what_en} changed from Rs {old:,} to Rs {new:,}. What is the percentage {word_en}?",
               [f"{x}%" for x in o], 0,
               f"Change = {abs(d):,}; {abs(d):,} ÷ {old:,} x 100 = {p}%. Always divide by the ORIGINAL value.",
               f"{what_bn} {old:,} টাকা থেকে {new:,} টাকা হলো। শতাংশ {word_bn} কত?",
               [f"{x}%" for x in o],
               f"পরিবর্তন = {abs(d):,}; {abs(d):,} ÷ {old:,} x 100 = {p}%। সবসময় আদি মান দিয়ে ভাগ করো।")


def gst(price, rate, item_en, item_bn):
    tax = price * rate // 100
    r = price + tax
    en, bn = _rs(_o(r, tax, price, price + rate))
    return mcq(f"{item_en} costs Rs {price:,} before tax. GST is {rate}%. What is the final price?", en, 0,
               f"GST = {rate}% of {price:,} = Rs {tax:,}; total = Rs {r:,}.",
               f"করের আগে {item_bn}-এর দাম {price:,} টাকা। জিএসটি {rate}%। শেষ দাম কত?", bn,
               f"জিএসটি = {price:,}-এর {rate}% = {tax:,} টাকা; মোট = {r:,} টাকা।")


def twodisc(price, a, b):
    p1 = price - price * a // 100
    p2 = p1 - p1 * b // 100
    wrong = price - price * (a + b) // 100
    en, bn = _rs(_o(p2, wrong, p1, price))
    return mcq(f"A Rs {price:,} drill gets {a}% off, then a further {b}% off the new price. What is the final price?", en, 0,
               f"After {a}%: {p1:,}. Then {b}% off {p1:,} = {p2:,}. Two discounts are NOT the same as adding them ({a + b}% off would give {wrong:,}).",
               f"{price:,} টাকার একটা ড্রিলে {a}% ছাড়, তারপর নতুন দামে আরও {b}% ছাড়। শেষ দাম কত?", bn,
               f"{a}% পরে: {p1:,}। তারপর {p1:,}-এ {b}% ছাড় = {p2:,}। দুটো ছাড় যোগ করার সমান নয় ({a + b}% ছাড়ে হতো {wrong:,})।")


def fx(usd, rate):
    r = usd * rate
    en, bn = _rs(_o(r, usd + rate, r // 10, usd))
    return mcq(f"An imported bridge bearing costs ${usd:,}. If $1 = Rs {rate}, what does it cost in rupees?", en, 0,
               f"{usd:,} x {rate} = Rs {r:,}. If the rupee weakens, imports cost more.",
               f"একটা আমদানি করা সেতু-বিয়ারিংয়ের দাম ${usd:,}। $1 = {rate} টাকা হলে টাকায় দাম কত?", bn,
               f"{usd:,} x {rate} = {r:,} টাকা। টাকার দাম কমলে আমদানির খরচ বাড়ে।")


def shortfall(cost, grant, saved):
    r = max(cost - grant - saved, 0)
    en, bn = _rs(_o(r, cost - grant, cost - saved, grant + saved))
    return mcq(f"A bridge costs Rs {cost:,}. You have Rs {saved:,} saved and a Rs {grant:,} Civil Grant. How much must be borrowed?", en, 0,
               f"{cost:,} - {grant:,} - {saved:,} = Rs {r:,}. Grants and savings shrink the loan - and the interest.",
               f"একটা সেতুর খরচ {cost:,} টাকা। তোমার {saved:,} টাকা জমানো আর {grant:,} টাকার সিভিল গ্রান্ট আছে। কত ধার করতে হবে?", bn,
               f"{cost:,} - {grant:,} - {saved:,} = {r:,} টাকা। অনুদান আর সঞ্চয় ঋণ - আর সুদ - কমায়।")


ITEMS = (
    si(4000, 5, 3), si(12000, 8, 2), si(7500, 6, 4), si(20000, 7, 5), si(2500, 12, 2),
    ci2(10000, 10), ci2(5000, 20), ci2(20000, 5), ci2(8000, 10), ci2(1000, 10),
    change(800, 1000, "A bag of cement", "এক বস্তা সিমেন্ট"),
    change(500, 400, "A train ticket", "একটা ট্রেনের টিকিট"),
    change(1200, 1500, "A worker's weekly wage", "একজন কর্মীর সাপ্তাহিক মজুরি"),
    change(2000, 1700, "A tonne of gravel", "এক টন পাথরকুচি"),
    change(250, 300, "A bridge toll", "একটা সেতুর টোল"),
    change(60000, 45000, "A used truck's value", "একটা পুরোনো ট্রাকের দাম"),
    gst(500, 18, "A safety helmet", "একটা নিরাপত্তা-হেলমেট"),
    gst(2000, 12, "A pair of work boots", "এক জোড়া কাজের বুট"),
    gst(10000, 28, "A small cement mixer", "একটা ছোট সিমেন্ট-মিক্সার"),
    gst(800, 5, "A box of packaged food", "এক বাক্স প্যাকেট-খাবার"),
    twodisc(5000, 20, 10), twodisc(2000, 10, 10), twodisc(8000, 25, 20),
    fx(100, 83), fx(250, 80), fx(1200, 85),
    shortfall(100000, 40000, 25000), shortfall(250000, 120000, 50000), shortfall(60000, 45000, 20000),
    mcq("How is compound interest different from simple interest?", ["Compound interest also earns interest on past interest", "It is always lower", "It never changes", "They are the same"], 0,
        "Over many years, compounding makes savings - and debts - grow much faster.",
        "চক্রবৃদ্ধি সুদ সরল সুদ থেকে কীভাবে আলাদা?", ["চক্রবৃদ্ধিতে আগের সুদের উপরও সুদ হয়", "সবসময় কম", "কখনো বদলায় না", "দুটো একই"],
        "বহু বছরে চক্রবৃদ্ধি সঞ্চয় - আর ঋণ - অনেক দ্রুত বাড়ায়।"),
    mcq("Why can an unpaid credit card balance grow scarily fast?", ["High compound interest is charged on the growing balance", "Cards shrink money", "Banks forget", "It never grows"], 0,
        "Rates of 36%+ a year can double a debt in about 2 years.",
        "না-মেটানো ক্রেডিট কার্ডের বকেয়া ভয়ংকর দ্রুত বাড়ে কেন?", ["বাড়তে থাকা বকেয়ার উপর উঁচু চক্রবৃদ্ধি সুদ লাগে", "কার্ড টাকা ছোট করে", "ব্যাংক ভুলে যায়", "কখনো বাড়ে না"],
        "বছরে 36%+ হারে প্রায় 2 বছরে ঋণ দ্বিগুণ হতে পারে।"),
    mcq("What does the 'Rule of 72' estimate?", ["How many years money takes to double: 72 ÷ interest rate", "The number of bank holidays", "Tax on 72 items", "The price of 72 bricks"], 0,
        "At 8%, money doubles in about 72 ÷ 8 = 9 years.",
        "'72-এর নিয়ম' কী আন্দাজ করে?", ["টাকা দ্বিগুণ হতে কত বছর: 72 ÷ সুদের হার", "ব্যাংকের ছুটির সংখ্যা", "72টি জিনিসে কর", "72টি ইটের দাম"],
        "8%-এ টাকা প্রায় 72 ÷ 8 = 9 বছরে দ্বিগুণ হয়।"),
    mcq("Using the Rule of 72, how long to double money at 6% a year?", ["About 12 years", "About 6 years", "About 72 years", "About 2 years"], 0,
        "72 ÷ 6 = 12.",
        "72-এর নিয়মে বছরে 6% হারে টাকা দ্বিগুণ হতে কত সময়?", ["প্রায় 12 বছর", "প্রায় 6 বছর", "প্রায় 72 বছর", "প্রায় 2 বছর"],
        "72 ÷ 6 = 12।"),
    mcq("Why is starting to save early so powerful?", ["Compounding has more years to work", "Banks pay children double", "Money is heavier when young", "It is not"], 0,
        "Time is the secret ingredient of compound growth.",
        "আগে থেকে সঞ্চয় শুরু করা এত শক্তিশালী কেন?", ["চক্রবৃদ্ধি কাজ করার জন্য বেশি বছর পায়", "ব্যাংক শিশুদের দ্বিগুণ দেয়", "ছোটবেলায় টাকা ভারী", "নয়"],
        "সময়ই চক্রবৃদ্ধির গোপন উপাদান।"),
    mcq("A price rises 10% and then falls 10%. Is it back to the original?", ["No - it ends 1% lower", "Yes, exactly", "It ends 10% higher", "It doubles"], 0,
        "Rs 100 -> 110 -> 99. The 10% fall is taken from a bigger number.",
        "একটা দাম 10% বেড়ে তারপর 10% কমল। কি আগের দামে ফিরল?", ["না - 1% কমে শেষ হয়", "হ্যাঁ, ঠিক আগের মতো", "10% বেশিতে শেষ হয়", "দ্বিগুণ হয়"],
        "100 টাকা -> 110 -> 99। 10% কমা হয় বড় সংখ্যা থেকে।"),
    mcq("A shop buys a fan for Rs 1,600 and sells it for Rs 2,000. What is the profit percent on cost?", ["25%", "20%", "40%", "400%"], 0,
        "Profit 400 ÷ cost 1,600 x 100 = 25%.",
        "একটা দোকান 1,600 টাকায় পাখা কিনে 2,000 টাকায় বেচল। খরচের উপর লাভ কত শতাংশ?", ["25%", "20%", "40%", "400%"],
        "লাভ 400 ÷ খরচ 1,600 x 100 = 25%।"),
    mcq("A trader buys goods for Rs 5,000 and sells them for Rs 4,000. What is the loss percent?", ["20%", "25%", "10%", "80%"], 0,
        "Loss 1,000 ÷ 5,000 x 100 = 20%.",
        "একজন ব্যবসায়ী 5,000 টাকায় মাল কিনে 4,000 টাকায় বেচলেন। ক্ষতি কত শতাংশ?", ["20%", "25%", "10%", "80%"],
        "ক্ষতি 1,000 ÷ 5,000 x 100 = 20%।"),
    mcq("A price including 18% GST is Rs 1,180. What was the price before GST?", ["Rs 1,000", "Rs 968", "Rs 1,162", "Rs 212"], 0,
        "1,180 ÷ 1.18 = 1,000. Do not just subtract 18% of 1,180!",
        "18% জিএসটিসহ দাম 1,180 টাকা। জিএসটির আগে দাম কত ছিল?", ["1,000 টাকা", "968 টাকা", "1,162 টাকা", "212 টাকা"],
        "1,180 ÷ 1.18 = 1,000। শুধু 1,180-এর 18% বিয়োগ কোরো না!"),
    mcq("What is 'opportunity cost'?", ["What you give up when you choose one option over another", "The price tag only", "A free chance", "A bank fee"], 0,
        "Spending Rs 500 on a game means not having that Rs 500 for a book.",
        "'সুযোগ-ব্যয়' কী?", ["একটা বিকল্প বাছলে অন্যটায় যা ছেড়ে দিতে হয়", "শুধু দামের ট্যাগ", "বিনামূল্যের সুযোগ", "ব্যাংকের ফি"],
        "500 টাকা খেলায় খরচ মানে সেই 500 টাকা বইয়ের জন্য থাকছে না।"),
    mcq("A town can spend Rs 1 crore on a bridge OR a new school wing. What is the opportunity cost of the bridge?", ["The school wing it could not build", "Nothing", "The bridge itself", "The tax"], 0,
        "Public money has many uses - choices need careful thought.",
        "একটা শহর 1 কোটি টাকা সেতুতে বা স্কুলের নতুন অংশে খরচ করতে পারে। সেতুর সুযোগ-ব্যয় কী?", ["যে স্কুল-অংশ বানানো গেল না", "কিছুই না", "সেতু নিজে", "কর"],
        "জনগণের টাকার নানা ব্যবহার - বাছাইয়ে যত্ন করে ভাবতে হয়।"),
    mcq("What is the usual link between risk and return in investing?", ["Higher possible returns usually come with higher risk", "High return always means no risk", "Risk and return are unrelated", "Low risk always pays most"], 0,
        "Be wary of anyone promising high returns with no risk.",
        "বিনিয়োগে ঝুঁকি আর লাভের সাধারণ সম্পর্ক কী?", ["বেশি সম্ভাব্য লাভে সাধারণত বেশি ঝুঁকি", "বেশি লাভে কখনো ঝুঁকি নেই", "ঝুঁকি আর লাভের সম্পর্ক নেই", "কম ঝুঁকিতে সবসময় সবচেয়ে বেশি লাভ"],
        "ঝুঁকি ছাড়া বেশি লাভের প্রতিশ্রুতি যে দেয়, তার থেকে সাবধান।"),
    mcq("What does 'diversification' mean?", ["Spreading money across different investments to lower risk", "Putting all money in one place", "Spending everything", "Borrowing more"], 0,
        "Don't put all your eggs in one basket.",
        "'বৈচিত্র্যকরণ' মানে কী?", ["ঝুঁকি কমাতে টাকা বিভিন্ন বিনিয়োগে ছড়ানো", "সব টাকা এক জায়গায় রাখা", "সব খরচ করা", "আরও ধার করা"],
        "সব ডিম এক ঝুড়িতে রেখো না।"),
    mcq("What is a 'share' in a company?", ["A small part of ownership in the company", "A loan to the company", "A free gift", "A type of tax"], 0,
        "Shareholders may get dividends and their shares can rise or fall in value.",
        "কোম্পানির 'শেয়ার' কী?", ["কোম্পানির মালিকানার একটা ছোট অংশ", "কোম্পানিকে ঋণ", "বিনামূল্যের উপহার", "এক রকম কর"],
        "শেয়ারহোল্ডার লভ্যাংশ পেতে পারেন আর শেয়ারের দাম ওঠানামা করে।"),
    mcq("What is a 'dividend'?", ["Part of a company's profit paid to its shareholders", "A loan repayment", "A tax", "A discount"], 0,
        "Profitable companies often share some profit this way.",
        "'লভ্যাংশ' কী?", ["কোম্পানির লাভের যে অংশ শেয়ারহোল্ডারদের দেওয়া হয়", "ঋণ শোধ", "কর", "ছাড়"],
        "লাভজনক কোম্পানি প্রায়ই এভাবে লাভের কিছু ভাগ করে।"),
    mcq("What is a 'bond'?", ["A loan you give to a government or company that pays interest", "A share of ownership", "A free gift", "A sticky glue"], 0,
        "Governments sell bonds to raise money for roads and bridges.",
        "'বন্ড' কী?", ["সরকার বা কোম্পানিকে দেওয়া ঋণ, যা সুদ দেয়", "মালিকানার অংশ", "বিনামূল্যের উপহার", "আঠালো আঠা"],
        "রাস্তা আর সেতুর টাকা তুলতে সরকার বন্ড বেচে।"),
    mcq("What is 'cash flow' for a bridge company each month?", ["Money received minus money paid out", "Only profit", "Only loans", "Water flowing under the bridge"], 0,
        "A firm can be profitable on paper but fail if cash runs out.",
        "সেতু-কোম্পানির মাসিক 'নগদ প্রবাহ' কী?", ["পাওয়া টাকা বিয়োগ দেওয়া টাকা", "শুধু লাভ", "শুধু ঋণ", "সেতুর নিচে বয়ে যাওয়া জল"],
        "কাগজে লাভজনক সংস্থাও নগদ ফুরোলে ব্যর্থ হতে পারে।"),
    mcq("A builder starts the month with Rs 50,000, receives Rs 30,000 and pays out Rs 65,000. What is left?", ["Rs 15,000", "Rs 45,000", "Rs 145,000", "Rs -15,000"], 0,
        "50,000 + 30,000 - 65,000 = 15,000.",
        "একজন নির্মাতা মাস শুরু করলেন 50,000 টাকা নিয়ে, পেলেন 30,000 আর দিলেন 65,000। কত বাকি?", ["15,000 টাকা", "45,000 টাকা", "1,45,000 টাকা", "-15,000 টাকা"],
        "50,000 + 30,000 - 65,000 = 15,000।"),
    mcq("Why do construction contracts often pay in stages (milestones)?", ["The builder gets cash as work is completed, and the client pays only for finished work", "To confuse the builder", "Stages are cheaper", "It is illegal to pay at once"], 0,
        "Stage payments keep cash flowing and reduce risk for both sides.",
        "নির্মাণ-চুক্তিতে প্রায়ই ধাপে ধাপে (মাইলফলকে) টাকা দেওয়া হয় কেন?", ["কাজ শেষ হওয়ার সঙ্গে নির্মাতা টাকা পান, আর গ্রাহক শুধু শেষ হওয়া কাজের দাম দেন", "নির্মাতাকে বিভ্রান্ত করতে", "ধাপে সস্তা", "একসঙ্গে দেওয়া বেআইনি"],
        "ধাপে টাকা নগদ প্রবাহ সচল রাখে আর দুই পক্ষের ঝুঁকি কমায়।"),
    mcq("What is 'retention money' in a building contract?", ["A small part of payment held back until defects are fixed", "A tip for workers", "A tax refund", "Money kept in a piggy bank"], 0,
        "Often 5% is kept until the end of the defects period.",
        "নির্মাণ-চুক্তিতে 'জামানত-টাকা' (রিটেনশন) কী?", ["ত্রুটি সারানো পর্যন্ত আটকে রাখা পেমেন্টের ছোট অংশ", "কর্মীদের বকশিশ", "করের ফেরত", "মাটির ভাঁড়ে রাখা টাকা"],
        "ত্রুটি-সময়কাল শেষ না হওয়া পর্যন্ত প্রায়ই 5% রাখা হয়।"),
    mcq("A Rs 2,00,000 contract keeps 5% retention. How much is held back?", ["Rs 10,000", "Rs 1,000", "Rs 20,000", "Rs 5,000"], 0,
        "5% of 2,00,000 = 10,000.",
        "2,00,000 টাকার চুক্তিতে 5% জামানত রাখা হয়। কত আটকে রাখা হয়?", ["10,000 টাকা", "1,000 টাকা", "20,000 টাকা", "5,000 টাকা"],
        "2,00,000-এর 5% = 10,000।"),
    mcq("Why do banks ask for a 'down payment' on loans?", ["Borrowers put in their own money, reducing the bank's risk", "To make loans bigger", "It is a gift to the bank", "No reason"], 0,
        "Your own stake shows commitment.",
        "ব্যাংক ঋণে 'অগ্রিম পেমেন্ট' চায় কেন?", ["ঋণগ্রহীতা নিজের টাকা দেন, ব্যাংকের ঝুঁকি কমে", "ঋণ বড় করতে", "ব্যাংককে উপহার", "কোনো কারণ নেই"],
        "নিজের অংশ প্রতিশ্রুতি দেখায়।"),
    mcq("What is 'collateral' for a loan?", ["Something valuable promised to the lender if the loan is not repaid", "A free extra loan", "A type of interest", "A bank holiday"], 0,
        "Land or equipment is often used as collateral.",
        "ঋণের 'জামানত' (কোল্যাটারাল) কী?", ["ঋণ শোধ না হলে ঋণদাতাকে দেওয়ার প্রতিশ্রুত মূল্যবান জিনিস", "বিনামূল্যের বাড়তি ঋণ", "এক রকম সুদ", "ব্যাংকের ছুটি"],
        "জমি বা যন্ত্রপাতি প্রায়ই জামানত হিসেবে ব্যবহার হয়।"),
    mcq("What is a 'credit score'?", ["A number showing how reliably someone has repaid debts", "A cricket score", "A school grade", "A bank's profit"], 0,
        "Good scores mean cheaper, easier loans.",
        "'ক্রেডিট স্কোর' কী?", ["কেউ কতটা নির্ভরযোগ্যভাবে ঋণ শোধ করেছেন তার সংখ্যা", "ক্রিকেটের স্কোর", "স্কুলের গ্রেড", "ব্যাংকের লাভ"],
        "ভালো স্কোর মানে সস্তা, সহজ ঋণ।"),
    mcq("Two loans of Rs 50,000: one at 10% for 2 years, one at 8% for 3 years (simple interest). Which costs less interest?", ["10% for 2 years (Rs 10,000 vs Rs 12,000)", "8% for 3 years", "They are equal", "Neither charges interest"], 0,
        "50,000 x 10 x 2 ÷ 100 = 10,000; 50,000 x 8 x 3 ÷ 100 = 12,000. A lower rate is not always cheaper overall.",
        "50,000 টাকার দুটো ঋণ: একটা 10%-এ 2 বছর, আরেকটা 8%-এ 3 বছর (সরল সুদ)। কোনটায় সুদ কম?", ["10%-এ 2 বছর (10,000 বনাম 12,000 টাকা)", "8%-এ 3 বছর", "দুটো সমান", "কোনোটাতেই সুদ নেই"],
        "50,000 x 10 x 2 ÷ 100 = 10,000; 50,000 x 8 x 3 ÷ 100 = 12,000। কম হার সবসময় মোটে সস্তা নয়।"),
    mcq("Why does the Black Box challenge in BridgeWorks reward study with salvage money?", ["Understanding why a bridge failed is worth real value - learning reduces future losses", "It is random", "To punish players", "Salvage is always zero"], 0,
        "Passing the academic challenge recovers 75% salvage instead of the normal amount.",
        "BridgeWorks-এর ব্ল্যাক বক্স চ্যালেঞ্জ পড়াশোনার জন্য উদ্ধার-টাকা দেয় কেন?", ["সেতু কেন ভাঙল তা বোঝার আসল মূল্য আছে - শেখা ভবিষ্যতের ক্ষতি কমায়", "এলোমেলো", "খেলোয়াড়দের শাস্তি দিতে", "উদ্ধার-টাকা সবসময় শূন্য"],
        "অ্যাকাডেমিক চ্যালেঞ্জে পাস করলে স্বাভাবিকের বদলে 75% উদ্ধার-টাকা ফেরত মেলে।"),
    mcq("A failed bridge cost Rs 80,000. Black Box salvage returns 75%. How much is recovered?", ["Rs 60,000", "Rs 20,000", "Rs 75,000", "Rs 8,000"], 0,
        "75% of 80,000 = 60,000.",
        "একটা ভাঙা সেতুর খরচ ছিল 80,000 টাকা। ব্ল্যাক বক্স উদ্ধারে 75% ফেরত। কত উদ্ধার হলো?", ["60,000 টাকা", "20,000 টাকা", "75,000 টাকা", "8,000 টাকা"],
        "80,000-এর 75% = 60,000।"),
    mcq("What does 'insurance excess' (deductible) mean?", ["The part of a claim you pay yourself before insurance pays the rest", "Extra insurance for free", "A bonus", "The premium"], 0,
        "A higher excess usually means a lower premium.",
        "বিমায় 'নিজস্ব অংশ' (ডিডাক্টিবল) মানে কী?", ["দাবির যে অংশ বিমা বাকিটা দেওয়ার আগে নিজে দিতে হয়", "বিনামূল্যের বাড়তি বিমা", "বোনাস", "প্রিমিয়াম"],
        "বেশি নিজস্ব অংশে সাধারণত প্রিমিয়াম কম।"),
    mcq("Flood damages a site: repair costs Rs 40,000 and the excess is Rs 5,000. How much does insurance pay?", ["Rs 35,000", "Rs 40,000", "Rs 45,000", "Rs 5,000"], 0,
        "40,000 - 5,000 = 35,000.",
        "বন্যায় নির্মাণস্থলের ক্ষতি: মেরামতে 40,000 টাকা আর নিজস্ব অংশ 5,000 টাকা। বিমা কত দেয়?", ["35,000 টাকা", "40,000 টাকা", "45,000 টাকা", "5,000 টাকা"],
        "40,000 - 5,000 = 35,000।"),
    mcq("What is an 'exchange rate'?", ["The price of one currency in another currency", "A bank's opening hours", "Swapping toys", "Interest on a loan"], 0,
        "Exchange rates matter when buying steel or machines from abroad.",
        "'বিনিময় হার' কী?", ["এক মুদ্রার দাম অন্য মুদ্রায়", "ব্যাংক খোলার সময়", "খেলনা অদলবদল", "ঋণের সুদ"],
        "বিদেশ থেকে ইস্পাত বা যন্ত্র কেনার সময় বিনিময় হার জরুরি।"),
    mcq("If $1 changes from Rs 80 to Rs 85, what happens to the cost of imported machines?", ["It rises", "It falls", "It stays the same", "It becomes free"], 0,
        "Each dollar now costs more rupees.",
        "$1 যদি 80 টাকা থেকে 85 টাকা হয়, আমদানি করা যন্ত্রের খরচের কী হয়?", ["বাড়ে", "কমে", "একই থাকে", "বিনামূল্যে হয়"],
        "এখন প্রতিটি ডলারে বেশি টাকা লাগে।"),
    mcq("What is a 'budget surplus'?", ["When income is more than spending", "When spending is more than income", "A type of loan", "A broken budget"], 0,
        "A surplus can be saved or used to pay off debts.",
        "'বাজেট-উদ্বৃত্ত' কী?", ["যখন আয় খরচের চেয়ে বেশি", "যখন খরচ আয়ের চেয়ে বেশি", "এক রকম ঋণ", "ভাঙা বাজেট"],
        "উদ্বৃত্ত জমানো বা ঋণ শোধে ব্যবহার করা যায়।"),
    mcq("What is a 'budget deficit'?", ["When spending is more than income", "When income is more than spending", "A savings account", "A bonus"], 0,
        "Deficits must be covered by savings or borrowing.",
        "'বাজেট-ঘাটতি' কী?", ["যখন খরচ আয়ের চেয়ে বেশি", "যখন আয় খরচের চেয়ে বেশি", "সঞ্চয়ী অ্যাকাউন্ট", "বোনাস"],
        "ঘাটতি সঞ্চয় বা ধার দিয়ে মেটাতে হয়।"),
    mcq("Why might a government borrow to build a big bridge?", ["The bridge brings benefits for decades, so the cost is spread over the years it is used", "Borrowing is always free", "To avoid building it", "Bridges cost nothing"], 0,
        "Tolls and economic growth help repay the loan.",
        "সরকার বড় সেতু বানাতে ধার করতে পারে কেন?", ["সেতু দশকের পর দশক উপকার দেয়, তাই খরচ ব্যবহারের বছরগুলোতে ছড়ানো যায়", "ধার সবসময় বিনামূল্যে", "না বানাতে", "সেতুর খরচ নেই"],
        "টোল আর অর্থনৈতিক বৃদ্ধি ঋণ শোধে সাহায্য করে।"),
    mcq("What is 'net worth'?", ["What you own minus what you owe", "Your salary", "Your savings only", "Your debts only"], 0,
        "Assets - liabilities = net worth.",
        "'নিট সম্পদ' কী?", ["যা তোমার আছে বিয়োগ যা তুমি ধারো", "তোমার বেতন", "শুধু সঞ্চয়", "শুধু ঋণ"],
        "সম্পদ - দায় = নিট সম্পদ।"),
    mcq("A firm owns equipment worth Rs 5 lakh and cash of Rs 1 lakh, and owes Rs 2 lakh. What is its net worth?", ["Rs 4 lakh", "Rs 8 lakh", "Rs 6 lakh", "Rs 2 lakh"], 0,
        "5 + 1 - 2 = 4 lakh.",
        "একটা সংস্থার 5 লাখ টাকার যন্ত্রপাতি আর 1 লাখ নগদ আছে, আর 2 লাখ ধার। নিট সম্পদ কত?", ["4 লাখ টাকা", "8 লাখ টাকা", "6 লাখ টাকা", "2 লাখ টাকা"],
        "5 + 1 - 2 = 4 লাখ।"),
    mcq("What is an 'asset'?", ["Something owned that has value", "A debt", "A bill", "A fine"], 0,
        "Cranes, trucks, cash and land are assets for a builder.",
        "'সম্পদ' (অ্যাসেট) কী?", ["মালিকানাধীন মূল্যবান জিনিস", "ঋণ", "বিল", "জরিমানা"],
        "ক্রেন, ট্রাক, নগদ আর জমি নির্মাতার সম্পদ।"),
    mcq("What is a 'liability'?", ["Something owed, like a loan", "A thing you own", "Cash in hand", "A profit"], 0,
        "Loans and unpaid bills are liabilities.",
        "'দায়' কী?", ["যা ধারা আছে, যেমন ঋণ", "যে জিনিস তোমার", "হাতে নগদ", "লাভ"],
        "ঋণ আর না-মেটানো বিল দায়।"),
    mcq("A machine costs Rs 1,00,000 and loses 20% of its value each year. What is it worth after 1 year?", ["Rs 80,000", "Rs 20,000", "Rs 1,20,000", "Rs 98,000"], 0,
        "1,00,000 - 20% = 80,000.",
        "একটা যন্ত্রের দাম 1,00,000 টাকা আর প্রতি বছর 20% মূল্য হারায়। 1 বছর পরে দাম কত?", ["80,000 টাকা", "20,000 টাকা", "1,20,000 টাকা", "98,000 টাকা"],
        "1,00,000 - 20% = 80,000।"),
    mcq("A household spends 40% of Rs 25,000 income on rent. How much is rent?", ["Rs 10,000", "Rs 4,000", "Rs 15,000", "Rs 40,000"], 0,
        "40% of 25,000 = 10,000.",
        "একটা পরিবার 25,000 টাকা আয়ের 40% ভাড়ায় খরচ করে। ভাড়া কত?", ["10,000 টাকা", "4,000 টাকা", "15,000 টাকা", "40,000 টাকা"],
        "25,000-এর 40% = 10,000।"),
    mcq("The 50/30/20 budget rule suggests what share of income for savings?", ["20%", "50%", "30%", "80%"], 0,
        "50% needs, 30% wants, 20% savings - a simple starting guide.",
        "50/30/20 বাজেট-নিয়ম সঞ্চয়ের জন্য আয়ের কত অংশ রাখতে বলে?", ["20%", "50%", "30%", "80%"],
        "50% প্রয়োজন, 30% ইচ্ছা, 20% সঞ্চয় - শুরু করার সহজ নির্দেশিকা।"),
    mcq("With Rs 30,000 income and the 50/30/20 rule, how much goes to savings?", ["Rs 6,000", "Rs 9,000", "Rs 15,000", "Rs 3,000"], 0,
        "20% of 30,000 = 6,000.",
        "30,000 টাকা আয়ে 50/30/20 নিয়মে সঞ্চয়ে কত যায়?", ["6,000 টাকা", "9,000 টাকা", "15,000 টাকা", "3,000 টাকা"],
        "30,000-এর 20% = 6,000।"),
    mcq("What is a 'Ponzi scheme'?", ["A scam paying old investors with new investors' money until it collapses", "A safe bank deposit", "A government bond", "A school fund"], 0,
        "No real profit is made - it always collapses, and most people lose.",
        "'পঞ্জি স্কিম' কী?", ["নতুন বিনিয়োগকারীর টাকা দিয়ে পুরোনোদের টাকা দেওয়া প্রতারণা, যা শেষে ভেঙে পড়ে", "নিরাপদ ব্যাংক-আমানত", "সরকারি বন্ড", "স্কুলের তহবিল"],
        "কোনো আসল লাভ হয় না - সবসময় ভেঙে পড়ে আর বেশিরভাগ মানুষ হারায়।"),
    mcq("A 'chit fund' promoter says 'bring 5 friends and double your money'. What should you suspect?", ["A pyramid or Ponzi scam", "A great safe deal", "A government grant", "A bank account"], 0,
        "Returns that depend on recruiting others are a red flag.",
        "একজন 'চিট ফান্ড' প্রচারক বলছেন '5 জন বন্ধু আনো আর টাকা দ্বিগুণ করো'। কী সন্দেহ করবে?", ["পিরামিড বা পঞ্জি প্রতারণা", "দারুণ নিরাপদ চুক্তি", "সরকারি অনুদান", "ব্যাংক-অ্যাকাউন্ট"],
        "অন্যদের আনার উপর নির্ভর করা লাভ একটা লাল সংকেত।"),
    mcq("Who regulates banks in India?", ["The Reserve Bank of India (RBI)", "The Railway Board", "A private club", "Nobody"], 0,
        "Use only RBI-regulated banks and SEBI-registered investment firms.",
        "ভারতে ব্যাংক কে নিয়ন্ত্রণ করে?", ["ভারতীয় রিজার্ভ ব্যাংক (আরবিআই)", "রেলওয়ে বোর্ড", "একটা ব্যক্তিগত ক্লাব", "কেউ না"],
        "শুধু আরবিআই-নিয়ন্ত্রিত ব্যাংক আর সেবি-নিবন্ধিত বিনিয়োগ-সংস্থা ব্যবহার করো।"),
    mcq("Why should you check a bank statement every month?", ["To spot mistakes or payments you did not make", "To waste paper", "Banks require it daily", "It is not useful"], 0,
        "Report unknown payments to the bank immediately.",
        "প্রতি মাসে ব্যাংক-বিবরণী দেখা উচিত কেন?", ["ভুল বা তুমি করোনি এমন পেমেন্ট ধরতে", "কাগজ নষ্ট করতে", "ব্যাংক রোজ চায়", "কাজের নয়"],
        "অচেনা পেমেন্ট সঙ্গে সঙ্গে ব্যাংককে জানাও।"),
    mcq("A donation camp in BridgeWorks uses Civil Grants. What real money does the game collect from players?", ["None - real payments are switched off", "All of it", "Half of it", "Only on weekends"], 0,
        "Real-money giving would only ever go through a registered charity with a parent's consent.",
        "BridgeWorks-এর দানশিবির সিভিল গ্রান্ট ব্যবহার করে। খেলা খেলোয়াড়দের থেকে কত আসল টাকা নেয়?", ["কিছুই না - আসল পেমেন্ট বন্ধ", "সবটা", "অর্ধেক", "শুধু সপ্তাহান্তে"],
        "আসল টাকার দান কেবল নিবন্ধিত দাতব্য সংস্থার মাধ্যমে, অভিভাবকের সম্মতি নিয়েই হতে পারে।"),
    si(9000, 4, 3), si(15000, 9, 2), si(6400, 5, 5),
    ci2(4000, 10), ci2(25000, 4), ci2(12000, 5),
    change(40, 50, "A kilo of onions", "এক কিলো পেঁয়াজ"),
    change(900, 720, "A monthly phone bill", "মাসিক ফোনের বিল"),
    change(3500, 4200, "A steel railing panel", "ইস্পাতের রেলিংয়ের একটা প্যানেল"),
    gst(1500, 18, "A tool belt with tools", "যন্ত্রসহ একটা যন্ত্র-বেল্ট"),
    gst(40000, 12, "A survey instrument", "একটা জরিপ-যন্ত্র"),
    twodisc(10000, 30, 10), twodisc(4000, 15, 20),
    fx(50, 84), fx(600, 82),
    shortfall(180000, 90000, 30000), shortfall(75000, 50000, 10000),
    mcq("Your money earns 6% interest but prices rise 8% a year. What is happening to your savings' buying power?", ["It is shrinking by about 2% a year", "It is growing by 14%", "It is unchanged", "It doubles"], 0,
        "The 'real' return is about interest rate minus inflation: 6 - 8 = -2%.",
        "তোমার টাকায় 6% সুদ হয় কিন্তু দাম বছরে 8% বাড়ে। সঞ্চয়ের ক্রয়ক্ষমতার কী হচ্ছে?", ["বছরে প্রায় 2% কমছে", "14% বাড়ছে", "অপরিবর্তিত", "দ্বিগুণ হয়"],
        "'প্রকৃত' লাভ প্রায় সুদের হার বিয়োগ মুদ্রাস্ফীতি: 6 - 8 = -2%।"),
    mcq("What is an 'EMI'?", ["Equated Monthly Instalment - the same loan payment every month", "An extra monthly income", "An emergency fund", "A type of tax"], 0,
        "EMIs include both interest and part of the loan.",
        "'ইএমআই' কী?", ["সমান মাসিক কিস্তি - প্রতি মাসে একই ঋণ-পেমেন্ট", "বাড়তি মাসিক আয়", "জরুরি তহবিল", "এক রকম কর"],
        "ইএমআই-তে সুদ আর ঋণের একটা অংশ দুটোই থাকে।"),
    mcq("Why do early EMIs mostly pay interest and later ones mostly repay the loan?", ["Interest is charged on the remaining balance, which is biggest at the start", "Banks change their minds", "Later EMIs are bigger", "It is random"], 0,
        "As the balance shrinks, more of each EMI goes to the principal.",
        "প্রথম দিকের ইএমআই-তে বেশিরভাগ সুদ আর পরেরগুলোয় বেশিরভাগ ঋণ শোধ হয় কেন?", ["বাকি অঙ্কের উপর সুদ লাগে, যা শুরুতে সবচেয়ে বড়", "ব্যাংক মত বদলায়", "পরের ইএমআই বড়", "এলোমেলো"],
        "বাকি অঙ্ক কমলে প্রতিটি ইএমআই-এর বেশি অংশ আসলে যায়।"),
    mcq("What does 'paying off a loan early' usually do?", ["Saves interest you would otherwise pay", "Always costs double", "Increases the loan", "Nothing"], 0,
        "Check for any prepayment fee first.",
        "'আগেভাগে ঋণ শোধ' সাধারণত কী করে?", ["যে সুদ দিতে হতো তা বাঁচায়", "সবসময় দ্বিগুণ খরচ", "ঋণ বাড়ায়", "কিছুই না"],
        "আগে দেখে নাও কোনো আগাম-শোধের ফি আছে কিনা।"),
    mcq("A Rs 1,000 investment grows to Rs 1,331 in 3 years. What yearly compound rate is that?", ["10%", "33%", "11%", "3%"], 0,
        "1,000 x 1.1 x 1.1 x 1.1 = 1,331.",
        "1,000 টাকার বিনিয়োগ 3 বছরে 1,331 টাকা হলো। বছরে কত চক্রবৃদ্ধি হার?", ["10%", "33%", "11%", "3%"],
        "1,000 x 1.1 x 1.1 x 1.1 = 1,331।"),
    mcq("What is a 'mutual fund'?", ["A pool of many people's money invested by professionals in many shares or bonds", "A bank loan", "A government tax", "A charity"], 0,
        "It spreads risk, but its value can still go down.",
        "'মিউচুয়াল ফান্ড' কী?", ["অনেক মানুষের টাকার একটা ভান্ডার, যা পেশাদাররা বহু শেয়ার বা বন্ডে বিনিয়োগ করেন", "ব্যাংক-ঋণ", "সরকারি কর", "দাতব্য সংস্থা"],
        "ঝুঁকি ছড়ায়, তবে দাম কমতেও পারে।"),
    mcq("A grant pays 30% of a Rs 5 lakh footbridge. How much does the grant cover?", ["Rs 1.5 lakh", "Rs 3.5 lakh", "Rs 30,000", "Rs 15 lakh"], 0,
        "30% of 5 lakh = 1.5 lakh.",
        "5 লাখ টাকার হাঁটার সেতুর 30% একটা অনুদান দেয়। অনুদান কত মেটায়?", ["1.5 লাখ টাকা", "3.5 লাখ টাকা", "30,000 টাকা", "15 লাখ টাকা"],
        "5 লাখের 30% = 1.5 লাখ।"),
)
