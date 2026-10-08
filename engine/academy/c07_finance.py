"""Class 7 - Finance (Junior Cadet): monthly interest on loans and cards, how an EMI splits into
interest and principal, dividend yield, bond coupons, real returns after inflation, GST input
credit, savings goals, insurance and expected value, break-even for projects and fair finance."""
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
    return int(x) if x == int(x) else round(x, 1)


def month_int(bal, yearly):
    r = bal * yearly // 1200
    return _rs(f"A loan balance of Rs {bal:,} is charged {yearly}% a year, worked out monthly. What is one month's interest?",
               f"{bal:,} টাকার ঋণ-বকেয়ায় বছরে {yearly}% সুদ, মাসিক হিসাবে। এক মাসের সুদ কত?", r,
               f"Monthly rate = {yearly}% ÷ 12; {bal:,} x {yearly} ÷ 1,200 = Rs {r:,}.",
               f"মাসিক হার = {yearly}% ÷ 12; {bal:,} x {yearly} ÷ 1,200 = {r:,} টাকা।",
               (bal * yearly // 100, r * 12, bal // 12))


def emi_split(bal, yearly, emi):
    i = bal * yearly // 1200
    p = emi - i
    return _rs(f"An EMI of Rs {emi:,} is paid on a Rs {bal:,} loan at {yearly}% a year. In the first month, how much of the EMI reduces the loan?",
               f"{bal:,} টাকার ঋণে বছরে {yearly}% হারে {emi:,} টাকার ইএমআই দেওয়া হলো। প্রথম মাসে ইএমআই-এর কত অংশ ঋণ কমায়?", p,
               f"Interest first: {bal:,} x {yearly} ÷ 1,200 = {i:,}. The rest, {emi:,} - {i:,} = Rs {p:,}, repays principal.",
               f"আগে সুদ: {bal:,} x {yearly} ÷ 1,200 = {i:,}। বাকি {emi:,} - {i:,} = {p:,} টাকা আসল শোধ করে।",
               (i, emi, emi + i))


def card(bal, monthly, months):
    b = bal
    for _ in range(months):
        b = b + b * monthly // 100
    return _rs(f"A credit card bill of Rs {bal:,} is left unpaid. Interest is {monthly}% a month, compounded. What is owed after {months} months?",
               f"{bal:,} টাকার ক্রেডিট-কার্ডের বিল শোধ হলো না। মাসে {monthly}% চক্রবৃদ্ধি সুদ। {months} মাস পরে কত বকেয়া?", b,
               f"Multiply by 1.{monthly:02d} each month: Rs {b:,} - about {(b - bal) * 100 // bal}% more in just {months} months!",
               f"প্রতি মাসে 1.{monthly:02d} দিয়ে গুণ: {b:,} টাকা - মাত্র {months} মাসে প্রায় {(b - bal) * 100 // bal}% বেশি!",
               (bal + bal * monthly * months // 100 - 1 if b != bal + bal * monthly * months // 100 else b + 50, bal, b - bal))


def dy(div, price, co_en, co_bn):
    r = _c(div * 100 / price)
    return _pc(f"A share in {co_en} costs Rs {price:,} and pays a yearly dividend of Rs {div:g}. What is the dividend yield?",
               f"{co_bn}-এর একটা শেয়ারের দাম {price:,} টাকা, বছরে {div:g} টাকা লভ্যাংশ দেয়। লভ্যাংশ-আয় কত?", r,
               f"Yield = dividend ÷ price x 100 = {div:g} ÷ {price:,} x 100 = {r:g}%.",
               f"আয় = লভ্যাংশ ÷ দাম x 100 = {div:g} ÷ {price:,} x 100 = {r:g}%।",
               (_c(price / div), _c(r * 10), _c(r + 2)))


def coupon(face, rate, years):
    r = face * rate * years // 100
    return _rs(f"A Rs {face:,} infrastructure bond pays a {rate}% coupon each year for {years} years. How much interest in total?",
               f"{face:,} টাকার একটা পরিকাঠামো-বন্ড {years} বছর ধরে বছরে {rate}% কুপন দেয়। মোট কত সুদ?", r,
               f"Each year {face:,} x {rate}% = {face * rate // 100:,}; x {years} = Rs {r:,}. The Rs {face:,} is repaid at the end.",
               f"প্রতি বছর {face:,} x {rate}% = {face * rate // 100:,}; x {years} = {r:,} টাকা। শেষে {face:,} টাকা ফেরত দেওয়া হয়।",
               (face * rate // 100, face + r, r // 2))


def real_ret(nom, infl):
    r = nom - infl
    o = []
    for v in (r, nom + infl, nom, -r if r != 0 else 1):
        if v not in o:
            o.append(v)
    o = [f"About {v:g}%" for v in o[:4]]
    o_bn = [s.replace("About ", "প্রায় ") for s in o]
    return mcq(f"Savings earn {nom}% a year while prices rise {infl}% a year. Roughly what is the real return?", o, 0,
               f"Real return ≈ interest - inflation = {nom} - {infl} = {r}%." + (" Your money is losing buying power!" if r < 0 else ""),
               f"সঞ্চয়ে বছরে {nom}% সুদ, আর দাম বাড়ে বছরে {infl}%। প্রকৃত আয় মোটামুটি কত?", o_bn,
               f"প্রকৃত আয় ≈ সুদ - মুদ্রাস্ফীতি = {nom} - {infl} = {r}%।" + (" টাকার ক্রয়ক্ষমতা কমছে!" if r < 0 else ""))


def itc(sales, buys, rate):
    out_tax, in_tax = sales * rate // 100, buys * rate // 100
    r = out_tax - in_tax
    return _rs(f"A fabricator sells steelwork for Rs {sales:,} and bought materials for Rs {buys:,}, both with {rate}% GST. How much GST does it pay the government after input credit?",
               f"একজন ইস্পাত-কারিগর {sales:,} টাকার কাজ বেচলেন আর {buys:,} টাকার উপাদান কিনলেন, দুটোতেই {rate}% জিএসটি। ইনপুট-ক্রেডিটের পরে সরকারকে কত জিএসটি দেবেন?", r,
               f"GST collected {out_tax:,} - GST already paid on inputs {in_tax:,} = Rs {r:,}. Tax is paid only on the value added.",
               f"আদায় করা জিএসটি {out_tax:,} - উপাদানে আগেই দেওয়া {in_tax:,} = {r:,} টাকা। কর দেওয়া হয় শুধু যোগ করা মূল্যের উপর।",
               (out_tax, in_tax, out_tax + in_tax))


def goal(target, have, monthly):
    m = -(-(target - have) // monthly)
    return mcq(f"You need Rs {target:,} for a surveying course, have Rs {have:,} and save Rs {monthly:,} a month. How many months until you can pay?",
               [str(x) for x in _o(m, (target - have) // monthly if (target - have) % monthly else m + 1, target // monthly, m - 1 if m > 1 else m + 3)], 0,
               f"Still needed {target - have:,}; ÷ {monthly:,} = {(target - have) / monthly:.1f}, so round UP to {m} months.",
               f"একটা জরিপ-কোর্সের জন্য {target:,} টাকা লাগবে, আছে {have:,} টাকা আর মাসে {monthly:,} টাকা জমাও। কত মাসে দিতে পারবে?",
               [str(x) for x in _o(m, (target - have) // monthly if (target - have) % monthly else m + 1, target // monthly, m - 1 if m > 1 else m + 3)],
               f"আরও লাগবে {target - have:,}; ÷ {monthly:,} = {(target - have) / monthly:.1f}, তাই উপরে আসন্ন করে {m} মাস।")


def ev(p_pct, loss, premium):
    e = loss * p_pct // 100
    return _rs(f"A site has a {p_pct}% yearly chance of a Rs {loss:,} flood loss. What is the expected yearly loss (useful when judging a Rs {premium:,} premium)?",
               f"একটা নির্মাণস্থলে বছরে {p_pct}% সম্ভাবনায় {loss:,} টাকার বন্যা-ক্ষতি হতে পারে। প্রত্যাশিত বার্ষিক ক্ষতি কত ({premium:,} টাকার প্রিমিয়াম বিচারে কাজের)?", e,
               f"Expected loss = probability x loss = {p_pct}% x {loss:,} = Rs {e:,}. Insurance also protects against the rare huge hit.",
               f"প্রত্যাশিত ক্ষতি = সম্ভাবনা x ক্ষতি = {p_pct}% x {loss:,} = {e:,} টাকা। বিমা বিরল বিশাল আঘাত থেকেও রক্ষা করে।",
               (loss, premium, loss // p_pct if p_pct else e + 7))


ITEMS = (
    month_int(120000, 12), month_int(60000, 10), month_int(240000, 9), month_int(36000, 18), month_int(500000, 6),
    emi_split(100000, 12, 8885), emi_split(60000, 10, 5275), emi_split(240000, 9, 11000), emi_split(300000, 8, 9400),
    card(10000, 3, 2), card(20000, 3, 3), card(5000, 4, 2), card(40000, 2, 3),
    dy(12, 300, "a steel company", "একটা ইস্পাত-কোম্পানি"), dy(5, 125, "a cement firm", "একটা সিমেন্ট-সংস্থা"),
    dy(30, 600, "a toll-road operator", "একটা টোল-সড়ক পরিচালক"), dy(8, 400, "a bridge builder", "একটা সেতু-নির্মাতা"),
    coupon(10000, 7, 5), coupon(50000, 8, 3), coupon(1000, 6, 10), coupon(25000, 9, 4),
    real_ret(7, 5), real_ret(4, 6), real_ret(10, 6), real_ret(6, 6),
    itc(200000, 120000, 18), itc(500000, 300000, 12), itc(80000, 50000, 18),
    goal(15000, 3000, 2000), goal(24000, 5000, 3000), goal(9000, 1000, 1500),
    ev(5, 400000, 25000), ev(2, 1000000, 30000), ev(10, 50000, 4000),
    mcq("Why do lenders work out interest monthly on the remaining balance?", ["As you repay, the balance falls, so later interest is smaller", "To make it confusing", "Interest is fixed forever", "Balances never change"], 0,
        "That is why paying extra early saves a lot of interest.",
        "ঋণদাতারা বাকি অঙ্কের উপর মাসিক সুদ হিসাব করেন কেন?", ["শোধের সঙ্গে বকেয়া কমে, তাই পরের সুদ ছোট হয়", "বিভ্রান্ত করতে", "সুদ চিরকাল স্থির", "বকেয়া কখনো বদলায় না"],
        "তাই আগেভাগে বাড়তি দিলে অনেক সুদ বাঁচে।"),
    mcq("What is the 'principal' of a loan?", ["The original amount borrowed (or still owed), not counting interest", "The interest rate", "The bank manager", "The monthly fee"], 0,
        "EMIs pay interest first, then reduce the principal.",
        "ঋণের 'আসল' কী?", ["মূল ধার করা (বা এখনো বাকি) অঙ্ক, সুদ বাদে", "সুদের হার", "ব্যাংক-ম্যানেজার", "মাসিক ফি"],
        "ইএমআই আগে সুদ দেয়, তারপর আসল কমায়।"),
    mcq("Why should credit card bills be paid in full each month?", ["Card interest of 30-40% a year makes unpaid balances grow very fast", "Banks give prizes", "It lowers your salary", "It is not important"], 0,
        "Paying only the 'minimum due' can trap people in debt for years.",
        "ক্রেডিট-কার্ডের বিল প্রতি মাসে পুরো মেটানো উচিত কেন?", ["বছরে 30-40% কার্ড-সুদে বকেয়া খুব দ্রুত বাড়ে", "ব্যাংক পুরস্কার দেয়", "বেতন কমায়", "জরুরি নয়"],
        "শুধু 'ন্যূনতম বকেয়া' দিলে মানুষ বছরের পর বছর ঋণে আটকে যেতে পারে।"),
    mcq("What is 'dividend yield'?", ["Yearly dividend as a percentage of the share price", "The share price", "Total company profit", "A bank fee"], 0,
        "It shows the income a share gives for its price.",
        "'লভ্যাংশ-আয়' কী?", ["শেয়ারের দামের শতাংশে বার্ষিক লভ্যাংশ", "শেয়ারের দাম", "কোম্পানির মোট লাভ", "ব্যাংকের ফি"],
        "দামের তুলনায় শেয়ার কত আয় দেয় তা দেখায়।"),
    mcq("What is a bond's 'coupon'?", ["The regular interest it pays", "A discount voucher", "The bond's price", "A tax"], 0,
        "Old paper bonds had coupons you cut off to claim each payment.",
        "বন্ডের 'কুপন' কী?", ["এর নিয়মিত সুদ-প্রদান", "ছাড়ের ভাউচার", "বন্ডের দাম", "কর"],
        "পুরোনো কাগজের বন্ডে প্রতি কিস্তি দাবির জন্য কুপন কেটে নেওয়া হতো।"),
    mcq("Why are infrastructure bonds useful for building bridges?", ["They raise large sums from many savers, repaid over years from tolls or taxes", "They print free money", "They avoid all costs", "They are illegal"], 0,
        "Savers earn interest while the nation gets roads and bridges.",
        "সেতু বানাতে পরিকাঠামো-বন্ড কাজের কেন?", ["অনেক সঞ্চয়কারীর থেকে বড় অঙ্ক তোলে, যা টোল বা কর থেকে বছর ধরে শোধ হয়", "বিনামূল্যে টাকা ছাপায়", "সব খরচ এড়ায়", "বেআইনি"],
        "সঞ্চয়কারীরা সুদ পান আর দেশ রাস্তা-সেতু পায়।"),
    mcq("What is the 'real' interest rate?", ["The interest rate minus inflation", "The rate printed on the passbook only", "Interest plus inflation", "Always zero"], 0,
        "It shows how much your buying power really grows.",
        "'প্রকৃত' সুদের হার কী?", ["সুদের হার বিয়োগ মুদ্রাস্ফীতি", "শুধু পাসবইয়ে ছাপা হার", "সুদ যোগ মুদ্রাস্ফীতি", "সবসময় শূন্য"],
        "ক্রয়ক্ষমতা সত্যিই কত বাড়ে তা দেখায়।"),
    mcq("What is 'input tax credit' in GST?", ["Businesses subtract GST already paid on their purchases from GST they collect", "A free loan", "A refund for shoppers only", "A penalty"], 0,
        "It stops tax being charged again and again on the same value.",
        "জিএসটিতে 'ইনপুট-কর ক্রেডিট' কী?", ["ব্যবসা কেনায় আগেই দেওয়া জিএসটি আদায়-করা জিএসটি থেকে বাদ দেয়", "বিনামূল্যের ঋণ", "শুধু ক্রেতাদের ফেরত", "জরিমানা"],
        "একই মূল্যের উপর বারবার কর লাগা আটকায়।"),
    mcq("What is 'expected value' in money decisions?", ["The average result you would expect over many repeats: probability x outcome", "The price tag", "The best possible result", "The worst result"], 0,
        "Insurers use it to set premiums.",
        "টাকার সিদ্ধান্তে 'প্রত্যাশিত মান' কী?", ["বহুবার ঘটলে যে গড় ফল আশা করা যায়: সম্ভাবনা x ফল", "দামের ট্যাগ", "সবচেয়ে ভালো ফল", "সবচেয়ে খারাপ ফল"],
        "বিমাকারী প্রিমিয়াম ঠিক করতে এটা ব্যবহার করে।"),
    mcq("Why do people buy insurance even though premiums usually exceed expected loss?", ["A rare huge loss could ruin them; insurance turns it into a small, certain cost", "Insurance always makes a profit for the buyer", "It is illegal not to buy any", "They like paying"], 0,
        "It is about protection, not profit.",
        "প্রিমিয়াম সাধারণত প্রত্যাশিত ক্ষতির বেশি হলেও মানুষ বিমা কেনে কেন?", ["বিরল বিশাল ক্ষতি সর্বনাশ করতে পারে; বিমা তাকে ছোট, নিশ্চিত খরচে বদলায়", "বিমা ক্রেতার সবসময় লাভ", "না কেনা বেআইনি", "দিতে ভালো লাগে"],
        "এটা সুরক্ষার জন্য, লাভের জন্য নয়।"),
    mcq("What is a 'sinking fund' for a toll bridge's major repairs?", ["Money set aside regularly so big future repairs are already paid for", "A fund that loses money", "A loan", "A tax on boats"], 0,
        "It avoids a sudden crisis when bearings or deck need replacing.",
        "টোল-সেতুর বড় মেরামতের জন্য 'ক্ষয়পূরণ তহবিল' কী?", ["নিয়মিত সরিয়ে রাখা টাকা, যাতে ভবিষ্যতের বড় মেরামতের খরচ তৈরি থাকে", "টাকা হারানো তহবিল", "ঋণ", "নৌকার উপর কর"],
        "বিয়ারিং বা পাটাতন বদলাতে হলে হঠাৎ সংকট এড়ায়।"),
    mcq("A bridge project has fixed costs of Rs 50 lakh and earns Rs 10 per vehicle after running costs. How many vehicles to break even?", ["5 lakh vehicles", "50,000 vehicles", "5 crore vehicles", "500 vehicles"], 0,
        "50,00,000 ÷ 10 = 5,00,000 vehicles.",
        "একটা সেতু-প্রকল্পের স্থির খরচ 50 লাখ টাকা আর চালানোর খরচ বাদে প্রতি যানে 10 টাকা আয়। লাভ-লোকসান সমান হতে কতগুলো যান?", ["5 লাখ যান", "50,000 যান", "5 কোটি যান", "500 যান"],
        "50,00,000 ÷ 10 = 5,00,000 যান।"),
    mcq("What does 'diversified portfolio' mean?", ["Investments spread across different types to reduce risk", "All money in one share", "Only cash", "Only gold"], 0,
        "If one investment falls, others may hold up.",
        "'বৈচিত্র্যময় পোর্টফোলিও' মানে কী?", ["ঝুঁকি কমাতে বিভিন্ন ধরনে ছড়ানো বিনিয়োগ", "সব টাকা একটা শেয়ারে", "শুধু নগদ", "শুধু সোনা"],
        "একটা পড়লে অন্যগুলো টিকে থাকতে পারে।"),
    mcq("What is 'market risk' for a shareholder?", ["Share prices can fall because of economy-wide events", "A shop being robbed", "Rain at a market", "No risk exists"], 0,
        "Only invest money you will not need soon.",
        "শেয়ারহোল্ডারের 'বাজার-ঝুঁকি' কী?", ["গোটা অর্থনীতির ঘটনায় শেয়ারের দাম পড়তে পারে", "দোকানে ডাকাতি", "বাজারে বৃষ্টি", "কোনো ঝুঁকি নেই"],
        "শুধু সেই টাকাই বিনিয়োগ করো যা শিগগির লাগবে না।"),
    mcq("What is a 'Systematic Investment Plan' (SIP)?", ["Investing a fixed amount regularly, such as every month", "A one-time lottery", "A loan scheme", "A tax"], 0,
        "Regular investing smooths out market ups and downs.",
        "'নিয়মিত বিনিয়োগ পরিকল্পনা' (এসআইপি) কী?", ["নিয়মিত, যেমন প্রতি মাসে, একটা নির্দিষ্ট অঙ্ক বিনিয়োগ", "একবারের লটারি", "ঋণ-প্রকল্প", "কর"],
        "নিয়মিত বিনিয়োগ বাজারের ওঠানামা মসৃণ করে।"),
    mcq("What is 'liquidity risk' for a small builder?", ["Running out of cash to pay bills even if the business is profitable", "Water leaking", "Too much cash", "Rain risk"], 0,
        "Late client payments are a common cause.",
        "ছোট নির্মাতার 'তারল্য-ঝুঁকি' কী?", ["ব্যবসা লাভজনক হলেও বিল দেওয়ার নগদ ফুরিয়ে যাওয়া", "জল চুঁইয়ে পড়া", "অনেক বেশি নগদ", "বৃষ্টির ঝুঁকি"],
        "গ্রাহকের দেরিতে পেমেন্ট একটা সাধারণ কারণ।"),
    mcq("What is an 'overdraft'?", ["A bank letting you spend more than is in your account, up to a limit, with interest", "Free money", "A savings bonus", "A cheque book"], 0,
        "Useful short-term, but costly if used for long.",
        "'ওভারড্রাফট' কী?", ["অ্যাকাউন্টে যা আছে তার বেশি, একটা সীমা পর্যন্ত, সুদসহ খরচ করতে দেওয়া", "বিনামূল্যের টাকা", "সঞ্চয়ের বোনাস", "চেকবই"],
        "অল্প সময়ের জন্য কাজের, কিন্তু লম্বা সময় ব্যবহারে দামি।"),
    mcq("What does 'compound annual growth rate' (CAGR) describe?", ["The steady yearly rate that would grow a value from start to end", "The total growth only", "A one-year jump", "The tax rate"], 0,
        "Rs 1,000 -> Rs 1,210 in 2 years is a CAGR of 10%.",
        "'চক্রবৃদ্ধি বার্ষিক বৃদ্ধির হার' (সিএজিআর) কী বোঝায়?", ["যে স্থির বার্ষিক হারে শুরু থেকে শেষ মান পৌঁছায়", "শুধু মোট বৃদ্ধি", "এক বছরের লাফ", "করের হার"],
        "2 বছরে 1,000 থেকে 1,210 টাকা মানে সিএজিআর 10%।"),
    mcq("A town's toll income grew from Rs 10 lakh to Rs 12.1 lakh in 2 years. What is the CAGR?", ["10%", "21%", "10.5%", "12.1%"], 0,
        "10 x 1.1 x 1.1 = 12.1.",
        "একটা শহরের টোল-আয় 2 বছরে 10 লাখ থেকে 12.1 লাখ টাকা হলো। সিএজিআর কত?", ["10%", "21%", "10.5%", "12.1%"],
        "10 x 1.1 x 1.1 = 12.1।"),
    mcq("What is 'financial fraud' warning sign number one?", ["Pressure to act fast with promises of big, guaranteed returns", "A clear written contract", "A registered bank", "Low, steady interest"], 0,
        "Take time, check registration and ask a trusted adult.",
        "'আর্থিক প্রতারণার' এক নম্বর সতর্কসংকেত কী?", ["বড়, নিশ্চিত লাভের প্রতিশ্রুতিসহ দ্রুত সিদ্ধান্তের চাপ", "স্পষ্ট লিখিত চুক্তি", "নিবন্ধিত ব্যাংক", "কম, স্থির সুদ"],
        "সময় নাও, নিবন্ধন দেখো আর বিশ্বস্ত বড়দের জিজ্ঞাসা করো।"),
    mcq("Why should a project's money and a person's own money be kept in separate accounts?", ["It keeps records clear and prevents misuse", "Banks require one account only", "To hide money", "It does not matter"], 0,
        "Mixing funds causes confusion and suspicion.",
        "প্রকল্পের টাকা আর ব্যক্তিগত টাকা আলাদা অ্যাকাউন্টে রাখা উচিত কেন?", ["হিসাব পরিষ্কার থাকে আর অপব্যবহার আটকায়", "ব্যাংক একটাই অ্যাকাউন্ট চায়", "টাকা লুকাতে", "কিছু যায় আসে না"],
        "টাকা মেশালে বিভ্রান্তি আর সন্দেহ হয়।"),
    mcq("What is an 'audit'?", ["An independent check that financial records are true and fair", "A music test", "A bridge load test", "A type of loan"], 0,
        "Public projects are audited to protect taxpayers' money.",
        "'নিরীক্ষা' (অডিট) কী?", ["আর্থিক হিসাব সত্য আর ন্যায্য কিনা তার স্বাধীন যাচাই", "গানের পরীক্ষা", "সেতুর বোঝা-পরীক্ষা", "এক রকম ঋণ"],
        "করদাতাদের টাকা রক্ষায় সরকারি প্রকল্পের নিরীক্ষা হয়।"),
    mcq("What is 'interest rate risk' for a borrower with a floating-rate loan?", ["EMIs can rise if interest rates go up", "Rates never change", "Loans become free", "Only savers are affected"], 0,
        "Fixed-rate loans avoid this but may start higher.",
        "ভাসমান-হারের ঋণগ্রহীতার 'সুদ-হারের ঝুঁকি' কী?", ["সুদের হার বাড়লে ইএমআই বাড়তে পারে", "হার কখনো বদলায় না", "ঋণ বিনামূল্যে হয়", "শুধু সঞ্চয়কারীরা প্রভাবিত"],
        "স্থির-হারের ঋণে এটা নেই, তবে শুরুতে হার বেশি হতে পারে।"),
    mcq("What is 'credit utilisation'?", ["How much of your available credit limit you are using", "Your salary", "Your savings rate", "A shop discount"], 0,
        "Using a small share of your limit helps your credit score.",
        "'ক্রেডিটের ব্যবহার' কী?", ["উপলব্ধ ধার-সীমার কতটা ব্যবহার করছ", "তোমার বেতন", "সঞ্চয়ের হার", "দোকানের ছাড়"],
        "সীমার ছোট অংশ ব্যবহার করলে ক্রেডিট স্কোর ভালো থাকে।"),
    mcq("A card limit is Rs 50,000 and the balance is Rs 15,000. What is the utilisation?", ["30%", "15%", "70%", "3.3%"], 0,
        "15,000 ÷ 50,000 x 100 = 30%.",
        "কার্ডের সীমা 50,000 টাকা আর বকেয়া 15,000 টাকা। ব্যবহার কত?", ["30%", "15%", "70%", "3.3%"],
        "15,000 ÷ 50,000 x 100 = 30%।"),
    mcq("Why do Civil Grants in BridgeWorks beat loans for funding a level?", ["Grants never need repaying and charge no interest", "Loans are free", "Grants cost more", "There is no difference"], 0,
        "Earning grants by learning is the cheapest money in the game.",
        "BridgeWorks-এ একটা লেভেলের অর্থায়নে সিভিল গ্রান্ট ঋণের চেয়ে ভালো কেন?", ["অনুদান শোধ করতে হয় না আর সুদ নেই", "ঋণ বিনামূল্যে", "অনুদানে খরচ বেশি", "কোনো পার্থক্য নেই"],
        "শিখে অনুদান অর্জনই খেলার সবচেয়ে সস্তা টাকা।"),
    mcq("What does 'net present value' greater than zero suggest about a bridge project?", ["Its future benefits, valued in today's money, exceed its cost", "It loses money", "It costs nothing", "It cannot be built"], 0,
        "NPV helps compare projects fairly.",
        "শূন্যের বেশি 'নিট বর্তমান মূল্য' সেতু-প্রকল্প সম্পর্কে কী বোঝায়?", ["আজকের টাকায় মাপা ভবিষ্যৎ উপকার খরচ ছাড়িয়ে যায়", "টাকা হারায়", "খরচ নেই", "বানানো যায় না"],
        "এনপিভি প্রকল্প ন্যায্যভাবে তুলনায় সাহায্য করে।"),
    mcq("What is 'philanthropy'?", ["Giving money or time to help others and society", "Borrowing money", "A type of tax", "Gambling"], 0,
        "Donation Camps in BridgeWorks let players practise giving with in-game grants only.",
        "'জনহিতৈষণা' কী?", ["অন্যদের আর সমাজের সাহায্যে টাকা বা সময় দেওয়া", "টাকা ধার করা", "এক রকম কর", "জুয়া"],
        "BridgeWorks-এর দানশিবির খেলোয়াড়দের শুধু খেলার অনুদানে দান অনুশীলন করতে দেয়।"),
    mcq("Why is a household 'emergency fund' often set at 3-6 months of expenses?", ["It covers job loss or illness without needing high-interest loans", "Banks demand it", "It is a tax rule", "To buy luxuries"], 0,
        "Keep it in a safe, easy-to-reach account.",
        "পরিবারের 'জরুরি তহবিল' প্রায়ই 3-6 মাসের খরচের সমান রাখা হয় কেন?", ["চাকরি হারানো বা অসুখে চড়া সুদের ঋণ ছাড়াই সামলায়", "ব্যাংক চায়", "করের নিয়ম", "বিলাসদ্রব্য কিনতে"],
        "নিরাপদ, সহজে-পাওয়া অ্যাকাউন্টে রাখো।"),
    month_int(80000, 15), month_int(180000, 8),
    emi_split(150000, 10, 7000), emi_split(48000, 12, 4300),
    card(15000, 3, 2), card(8000, 4, 3),
    dy(15, 500, "a port company", "একটা বন্দর-সংস্থা"), dy(9, 180, "a power utility", "একটা বিদ্যুৎ-সংস্থা"),
    coupon(20000, 7, 6), coupon(5000, 8, 5),
    real_ret(8, 5), real_ret(5, 7),
    itc(300000, 200000, 18), itc(150000, 60000, 5),
    goal(30000, 6000, 4000), goal(12000, 2000, 1500),
    ev(4, 250000, 15000), ev(1, 2000000, 30000),
    mcq("Rs 10,000 is deposited at 10% a year, compounded yearly. How much interest is earned in 2 years?", ["Rs 2,100", "Rs 2,000", "Rs 1,000", "Rs 12,100"], 0,
        "Year 1: 10,000 -> 11,000. Year 2: 11,000 -> 12,100. Interest = Rs 2,100 - the extra Rs 100 is interest on interest.",
        "10,000 টাকা বছরে 10% চক্রবৃদ্ধি হারে জমা রাখা হলো। 2 বছরে কত সুদ হয়?", ["2,100 টাকা", "2,000 টাকা", "1,000 টাকা", "12,100 টাকা"],
        "১ম বছর: 10,000 -> 11,000। ২য় বছর: 11,000 -> 12,100। সুদ = 2,100 টাকা - বাড়তি 100 টাকা সুদের উপর সুদ।"),
    mcq("By the 'rule of 72', money growing at 8% a year doubles in roughly how many years?", ["About 9 years", "About 8 years", "About 72 years", "About 4 years"], 0,
        "72 ÷ 8 = 9. A quick way to feel the power of compounding.",
        "'72-এর নিয়ম' অনুযায়ী বছরে 8% হারে বাড়া টাকা মোটামুটি কত বছরে দ্বিগুণ হয়?", ["প্রায় 9 বছর", "প্রায় 8 বছর", "প্রায় 72 বছর", "প্রায় 4 বছর"],
        "72 ÷ 8 = 9। চক্রবৃদ্ধির জোর বোঝার সহজ উপায়।"),
    mcq("A builder pledges a crane to get a loan. What is the crane called in this deal?", ["Collateral", "Dividend", "Coupon", "Premium"], 0,
        "Collateral is something valuable the lender can take if the loan is not repaid - so the lender may offer a lower rate.",
        "একজন নির্মাতা ঋণ পেতে একটা ক্রেন বন্ধক রাখলেন। এই চুক্তিতে ক্রেনটাকে কী বলে?", ["জামানত", "লভ্যাংশ", "কুপন", "প্রিমিয়াম"],
        "জামানত হলো মূল্যবান জিনিস, ঋণ শোধ না হলে ঋণদাতা যা নিতে পারেন - তাই ঋণদাতা কম হার দিতে পারেন।"),
    mcq("What does a good 'credit score' help you get?", ["Loans approved more easily and at lower interest", "Free shopping", "Higher taxes", "A bigger electricity bill"], 0,
        "Paying every EMI and card bill on time builds a good score.",
        "ভালো 'ক্রেডিট-স্কোর' কী পেতে সাহায্য করে?", ["সহজে আর কম সুদে ঋণ মঞ্জুর", "বিনামূল্যে কেনাকাটা", "বেশি কর", "বড় বিদ্যুৎ-বিল"],
        "সময়মতো প্রতিটা ইএমআই আর কার্ড-বিল দিলে ভালো স্কোর তৈরি হয়।"),
    mcq("Two loans both say '10% interest'. One is a 'flat rate', the other on the 'reducing balance'. Which costs more?", ["The flat rate - it charges interest on the full original amount the whole time", "The reducing balance", "They cost exactly the same", "Neither charges interest"], 0,
        "Flat rate ignores what you have already repaid, so its true cost is much higher.",
        "দুটো ঋণেই লেখা '10% সুদ'। একটা 'স্থির হার', অন্যটা 'হ্রাসমান বকেয়ার' উপর। কোনটায় খরচ বেশি?", ["স্থির হার - পুরো সময় মূল অঙ্কের উপরই সুদ নেয়", "হ্রাসমান বকেয়া", "হুবহু সমান খরচ", "কোনোটাই সুদ নেয় না"],
        "স্থির হার আগে শোধ করা অংশ গোনে না, তাই আসল খরচ অনেক বেশি।"),
    mcq("A bank charges a 2% processing fee on a Rs 3,00,000 equipment loan. How much is the fee?", ["Rs 6,000", "Rs 600", "Rs 60,000", "Rs 2,000"], 0,
        "3,00,000 x 2 ÷ 100 = Rs 6,000 - always add fees when comparing loans.",
        "3,00,000 টাকার যন্ত্রপাতি-ঋণে ব্যাংক 2% প্রসেসিং ফি নেয়। ফি কত?", ["6,000 টাকা", "600 টাকা", "60,000 টাকা", "2,000 টাকা"],
        "3,00,000 x 2 ÷ 100 = 6,000 টাকা - ঋণ তুলনার সময় সবসময় ফি যোগ করো।"),
    mcq("Why compare loans using the APR (annual percentage rate)?", ["It includes fees as well as interest, giving the true yearly cost", "It is always the lowest number", "It ignores interest", "Banks are not allowed to show it"], 0,
        "A low headline rate with big fees can cost more than a slightly higher rate with none.",
        "ঋণ তুলনায় এপিআর (বার্ষিক শতাংশ হার) ব্যবহার করা হয় কেন?", ["সুদের সঙ্গে ফি-ও ধরে, তাই আসল বার্ষিক খরচ দেখায়", "সবসময় সবচেয়ে ছোট সংখ্যা", "সুদ বাদ দেয়", "ব্যাংক দেখাতে পারে না"],
        "বড় ফি-সহ কম ঘোষিত হার, ফি-ছাড়া একটু বেশি হারের চেয়ে দামি হতে পারে।"),
    mcq("A caller says they are from your bank and asks for the OTP sent to your phone. What should you do?", ["Never share it - hang up and call the bank's official number", "Read it out quickly", "Share half of it", "Post it online"], 0,
        "Real banks never ask for your OTP or PIN.",
        "একজন ফোন করে বলল সে তোমার ব্যাংক থেকে, আর ফোনে আসা ওটিপি চাইল। কী করবে?", ["কখনো বলবে না - ফোন কেটে ব্যাংকের সরকারি নম্বরে ফোন করো", "তাড়াতাড়ি পড়ে শোনাও", "অর্ধেকটা বলো", "অনলাইনে পোস্ট করো"],
        "আসল ব্যাংক কখনো ওটিপি বা পিন চায় না।"),
    mcq("How does a mutual fund help a small saver invest in many companies at once?", ["It pools many investors' money, and professionals spread it across many investments", "It buys just one share for everyone", "It keeps the money in a locker", "It lends the money to the saver"], 0,
        "Small savers get diversification they could not build alone.",
        "মিউচুয়াল ফান্ড কীভাবে একজন ছোট সঞ্চয়কারীকে একসঙ্গে অনেক কোম্পানিতে বিনিয়োগ করতে দেয়?", ["অনেক বিনিয়োগকারীর টাকা একসঙ্গে করে, পেশাদাররা তা নানা বিনিয়োগে ছড়িয়ে দেন", "সবার জন্য শুধু একটা শেয়ার কেনে", "টাকা লকারে রেখে দেয়", "সঞ্চয়কারীকেই টাকা ধার দেয়"],
        "ছোট সঞ্চয়কারী একা যা পারতেন না, সেই বৈচিত্র্য পান।"),
    mcq("A client keeps 5% 'retention money' from a Rs 20 lakh bridge bill until defects are checked. How much is held back?", ["Rs 1 lakh", "Rs 10 lakh", "Rs 5 lakh", "Rs 10,000"], 0,
        "20,00,000 x 5 ÷ 100 = 1,00,000. It is released once the work proves sound.",
        "ত্রুটি যাচাই না হওয়া পর্যন্ত গ্রাহক 20 লাখ টাকার সেতু-বিল থেকে 5% 'জামানত-টাকা' রেখে দেন। কত আটকে থাকে?", ["1 লাখ টাকা", "10 লাখ টাকা", "5 লাখ টাকা", "10,000 টাকা"],
        "20,00,000 x 5 ÷ 100 = 1,00,000। কাজ মজবুত প্রমাণ হলে ছেড়ে দেওয়া হয়।"),
    mcq("What is a 'performance bank guarantee' on a construction contract?", ["A bank's promise to pay the client if the contractor fails to finish the work", "A bonus for fast work", "A free loan", "An insurance for workers' lunch"], 0,
        "It reassures the client before handing over a big contract.",
        "নির্মাণ-চুক্তিতে 'কাজ-সম্পাদনের ব্যাংক-গ্যারান্টি' কী?", ["ঠিকাদার কাজ শেষ না করলে গ্রাহককে টাকা দেওয়ার ব্যাংকের প্রতিশ্রুতি", "দ্রুত কাজের বোনাস", "বিনামূল্যের ঋণ", "শ্রমিকদের দুপুরের খাবারের বিমা"],
        "বড় চুক্তি দেওয়ার আগে গ্রাহককে ভরসা দেয়।"),
    mcq("A crane costs Rs 10 lakh and is used for 10 years with no scrap value. Using straight-line depreciation, what is the yearly depreciation?", ["Rs 1 lakh", "Rs 10 lakh", "Rs 10,000", "Rs 2 lakh"], 0,
        "10,00,000 ÷ 10 = 1,00,000 a year: the crane's cost spread over its working life.",
        "একটা ক্রেনের দাম 10 লাখ টাকা, 10 বছর চলে, শেষে কোনো মূল্য নেই। সরলরৈখিক অবচয়ে বছরে অবচয় কত?", ["1 লাখ টাকা", "10 লাখ টাকা", "10,000 টাকা", "2 লাখ টাকা"],
        "10,00,000 ÷ 10 = বছরে 1,00,000: ক্রেনের খরচ তার কাজের জীবন জুড়ে ভাগ করা।"),
    mcq("What is a firm's 'working capital'?", ["Money available for day-to-day costs: current assets minus current liabilities", "The office building", "The owner's salary", "Long-term loans only"], 0,
        "Without it, wages and cement bills cannot be paid on time.",
        "একটা সংস্থার 'চলতি মূলধন' কী?", ["দৈনন্দিন খরচের টাকা: চলতি সম্পদ বিয়োগ চলতি দায়", "অফিস-বাড়ি", "মালিকের বেতন", "শুধু দীর্ঘমেয়াদি ঋণ"],
        "এটা না থাকলে মজুরি আর সিমেন্টের বিল সময়ে দেওয়া যায় না।"),
    mcq("A Rs 6 lakh concrete mixer saves Rs 1.5 lakh a year in hire charges. What is its payback period?", ["4 years", "6 years", "1.5 years", "9 years"], 0,
        "6 ÷ 1.5 = 4 years to recover the cost; after that the savings are profit.",
        "6 লাখ টাকার একটা কংক্রিট-মিক্সার বছরে 1.5 লাখ টাকা ভাড়া বাঁচায়। খরচ উঠতে কত সময়?", ["4 বছর", "6 বছর", "1.5 বছর", "9 বছর"],
        "6 ÷ 1.5 = 4 বছরে খরচ উঠে আসে; তারপর সাশ্রয়টাই লাভ।"),
    mcq("What is TDS (tax deducted at source)?", ["Tax taken out by the payer before paying you, and sent to the government", "A shop discount", "Tax paid only by banks", "A penalty for late work"], 0,
        "Clients often deduct TDS from contractor bills; it counts towards the contractor's final tax.",
        "টিডিএস (উৎসে কর কর্তন) কী?", ["যে টাকা দেয়, সে দেওয়ার আগেই কর কেটে সরকারকে পাঠায়", "দোকানের ছাড়", "শুধু ব্যাংকের কর", "দেরির জরিমানা"],
        "গ্রাহকরা প্রায়ই ঠিকাদারের বিল থেকে টিডিএস কাটেন; এটা ঠিকাদারের চূড়ান্ত করে গোনা হয়।"),
    mcq("A bridge was budgeted at Rs 40 lakh but cost Rs 46 lakh. By what percentage did it overrun?", ["15%", "6%", "13%", "46%"], 0,
        "Overrun 6 lakh ÷ budget 40 lakh x 100 = 15%.",
        "একটা সেতুর বাজেট ছিল 40 লাখ টাকা, খরচ হলো 46 লাখ টাকা। কত শতাংশ বেশি খরচ হলো?", ["15%", "6%", "13%", "46%"],
        "বাড়তি 6 লাখ ÷ বাজেট 40 লাখ x 100 = 15%।"),
    mcq("What is a public-private partnership (PPP) for a toll bridge?", ["A company builds and runs it, recovering its money from tolls for an agreed period, then hands it to the government", "The government sells the river", "Citizens build it for free", "A private club bridge"], 0,
        "It lets the public get a bridge sooner without paying the whole cost upfront.",
        "টোল-সেতুর জন্য সরকারি-বেসরকারি অংশীদারি (পিপিপি) কী?", ["একটা সংস্থা বানায় ও চালায়, নির্দিষ্ট সময় টোল থেকে টাকা তোলে, তারপর সরকারকে দেয়", "সরকার নদী বিক্রি করে", "নাগরিকরা বিনামূল্যে বানায়", "বেসরকারি ক্লাবের সেতু"],
        "পুরো খরচ আগে না দিয়েই মানুষ তাড়াতাড়ি সেতু পায়।"),
    mcq("What is a person's or firm's 'net worth'?", ["Everything owned minus everything owed", "Monthly income", "Cash in the wallet only", "Total loans"], 0,
        "Assets Rs 30 lakh with loans Rs 12 lakh means a net worth of Rs 18 lakh.",
        "কোনো ব্যক্তি বা সংস্থার 'নিট সম্পদ' কী?", ["যা কিছু মালিকানায় বিয়োগ যা কিছু দেনা", "মাসিক আয়", "শুধু মানিব্যাগের নগদ", "মোট ঋণ"],
        "সম্পদ 30 লাখ আর ঋণ 12 লাখ মানে নিট সম্পদ 18 লাখ টাকা।"),
    mcq("Rs 1,000 is kept as cash at home for a year while prices rise 6%. What happens?", ["It buys about 6% less than before", "It grows by 6%", "It stays worth exactly the same", "It doubles"], 0,
        "Idle cash loses buying power; a savings account at least fights back.",
        "দাম 6% বাড়ার বছরে 1,000 টাকা ঘরে নগদ রাখা হলো। কী হয়?", ["আগের চেয়ে প্রায় 6% কম কেনা যায়", "6% বাড়ে", "মূল্য হুবহু একই থাকে", "দ্বিগুণ হয়"],
        "অলস নগদ ক্রয়ক্ষমতা হারায়; সঞ্চয়-অ্যাকাউন্ট অন্তত লড়াই করে।"),
)
