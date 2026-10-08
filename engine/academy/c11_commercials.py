"""Class 11 - Commercials (Senior Engineer): PERT time estimates, safety stock for a service
level, queue lengths, crashing a project schedule, generalised cost for choosing transport,
empty running and container fill, landed cost, Pareto analysis, break-even tolls, the Kraljic
matrix, FIDIC-style contracts, peak pricing and international freight for bridge projects."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r + 2, r * 2, r + 10):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn="", pre_en=""):
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:,.2f}".rstrip("0").rstrip(".")
    o = _o(r, *alts)
    return mcq(q_en, [pre_en + f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + u_bn for x in o], ex_bn)


def pert(o, m, p, task_en, task_bn):
    t = _c((o + 4 * m + p) / 6)
    return _n(f"Estimates for {task_en}: optimistic {o} days, most likely {m} days, pessimistic {p} days. What is the PERT expected time?",
              f"{task_bn}-এর আন্দাজ: আশাবাদী {o} দিন, সবচেয়ে সম্ভাব্য {m} দিন, নিরাশাবাদী {p} দিন। পার্ট-প্রত্যাশিত সময় কত?", t,
              f"tₑ = (o + 4m + p) ÷ 6 = ({o} + {4 * m} + {p}) ÷ 6 = {t:g} days.",
              f"tₑ = (o + 4m + p) ÷ 6 = ({o} + {4 * m} + {p}) ÷ 6 = {t:g} দিন।",
              (_c((o + m + p) / 3), m, p), " days", " দিন")


def safety(sigma, lead):
    s = round(1.65 * sigma * lead ** 0.5)
    return _n(f"Daily demand for cement bags varies with a standard deviation of {sigma} bags. Lead time is {lead} days. For a 95% service level (z = 1.65), what safety stock is needed? (SS = z x σ x √L)",
              f"সিমেন্টের বস্তার দৈনিক চাহিদার প্রমিত বিচ্যুতি {sigma} বস্তা। সরবরাহ-সময় {lead} দিন। 95% পরিষেবা-স্তরে (z = 1.65) কত নিরাপত্তা-মজুত লাগবে? (SS = z x σ x √L)", s,
              f"SS = 1.65 x {sigma} x √{lead} = 1.65 x {sigma} x {_c(lead ** 0.5):g} ≈ {s:,} bags.",
              f"SS = 1.65 x {sigma} x √{lead} = 1.65 x {sigma} x {_c(lead ** 0.5):g} ≈ {s:,} বস্তা।",
              (round(1.65 * sigma * lead), sigma * lead, round(sigma * lead ** 0.5)), " bags", " বস্তা")


def mm1(arr, serv):
    rho = arr / serv
    l = _c(rho / (1 - rho))
    return _n(f"At a single-lane toll booth, vehicles arrive at {arr} per minute and are served at {serv} per minute (random arrivals and service). What is the average number of vehicles in the system? (L = ρ ÷ (1 - ρ))",
              f"একটা একক-লেনের টোল-বুথে মিনিটে {arr}টি যান আসে আর মিনিটে {serv}টি সামলানো হয় (এলোমেলো আগমন আর পরিষেবা)। ব্যবস্থায় গড়ে কতগুলো যান? (L = ρ ÷ (1 - ρ))", l,
              f"ρ = {arr} ÷ {serv} = {_c(rho):g}; L = {_c(rho):g} ÷ (1 - {_c(rho):g}) = {l:g}. As ρ approaches 1, the queue explodes.",
              f"ρ = {arr} ÷ {serv} = {_c(rho):g}; L = {_c(rho):g} ÷ (1 - {_c(rho):g}) = {l:g}। ρ 1-এর কাছে গেলে লাইন বিস্ফোরিত হয়।",
              (_c(rho), _c(1 / (1 - rho)), _c(l * 2)), " vehicles", "টি যান")


def crash(nc, cc, nt, ct, task_en, task_bn):
    r = (cc - nc) // (nt - ct)
    return _n(f"{task_en} normally takes {nt} days and costs Rs {nc:,}. It can be crashed to {ct} days for Rs {cc:,}. What is the crash cost per day saved?",
              f"{task_bn} সাধারণত {nt} দিনে {nc:,} টাকায় হয়। খরচ বাড়িয়ে {ct} দিনে {cc:,} টাকায় করা যায়। বাঁচানো দিনপ্রতি খরচ কত?", r,
              f"({cc:,} - {nc:,}) ÷ ({nt} - {ct}) = Rs {r:,} per day. Crash the cheapest critical-path tasks first.",
              f"({cc:,} - {nc:,}) ÷ ({nt} - {ct}) = দিনপ্রতি {r:,} টাকা। সংকট-পথের সবচেয়ে সস্তা কাজ আগে দ্রুত করো।",
              (cc // ct, (cc - nc) // nt, cc - nc), "", " টাকা", "Rs ")


def gencost(fare_a, hrs_a, fare_b, hrs_b, vot):
    a = fare_a + hrs_a * vot
    b = fare_b + hrs_b * vot
    win_en, win_bn = ("Rail", "রেল") if a < b else ("Road", "সড়ক")
    lose_en, lose_bn = ("Road", "সড়ক") if a < b else ("Rail", "রেল")
    return mcq(f"Moving a load costs Rs {fare_a:,} by rail taking {hrs_a} hours, or Rs {fare_b:,} by road taking {hrs_b} hours. Time is valued at Rs {vot:,} per hour. Which has the lower generalised cost?",
               [f"{win_en} (Rs {min(a, b):,})", f"{lose_en} (Rs {max(a, b):,})", "They are equal", "Neither can be compared"], 0,
               f"Rail: {fare_a:,} + {hrs_a} x {vot:,} = {a:,}; road: {fare_b:,} + {hrs_b} x {vot:,} = {b:,}.",
               f"একটা বোঝা রেলে নিতে {fare_a:,} টাকা আর {hrs_a} ঘণ্টা, বা সড়কে {fare_b:,} টাকা আর {hrs_b} ঘণ্টা। সময়ের মূল্য ঘণ্টায় {vot:,} টাকা। কোনটার সাধারণীকৃত খরচ কম?",
               [f"{win_bn} ({min(a, b):,} টাকা)", f"{lose_bn} ({max(a, b):,} টাকা)", "দুটো সমান", "তুলনা করা যায় না"],
               f"রেল: {fare_a:,} + {hrs_a} x {vot:,} = {a:,}; সড়ক: {fare_b:,} + {hrs_b} x {vot:,} = {b:,}।")


def empty(empty_km, total_km):
    r = _c(empty_km * 100 / total_km)
    return _n(f"A fleet drove {total_km:,} km last month, of which {empty_km:,} km were empty return trips. What is the empty running percentage?",
              f"একটা বহর গত মাসে {total_km:,} km চলেছে, যার {empty_km:,} km খালি ফেরার যাত্রা। খালি চলার শতাংশ কত?", r,
              f"{empty_km:,} ÷ {total_km:,} x 100 = {r:g}%. Backhauls and load-matching apps cut it.",
              f"{empty_km:,} ÷ {total_km:,} x 100 = {r:g}%। ফিরতি বোঝাই আর বোঝা-মেলানো অ্যাপ এটা কমায়।",
              (_c(100 - r), _c(total_km / empty_km), _c(r / 2)), "%", "%")


def fill(used, cap):
    r = _c(used * 100 / cap)
    return _n(f"A 33 m³ shipping container is loaded with {used:g} m³ of bearings and fixings. What is its fill rate?",
              f"একটা 33 m³-এর জাহাজি কনটেনারে {used:g} m³ বিয়ারিং আর আটকানোর জিনিস ভরা হলো। ভরার হার কত?", r,
              f"{used:g} ÷ {cap} x 100 = {r:g}%. Unused space is still paid for.",
              f"{used:g} ÷ {cap} x 100 = {r:g}%। খালি জায়গার দামও দিতে হয়।",
              (_c(100 - r), _c(cap / used * 10), _c(r + 15)), "%", "%")


def landed(price, freight, ins_pct, duty_pct):
    cif = price + freight + price * ins_pct // 100
    duty = cif * duty_pct // 100
    r = cif + duty
    return _n(f"Steel cables cost Rs {price:,} at the foreign factory. Freight is Rs {freight:,}, insurance {ins_pct}% of the price, and customs duty {duty_pct}% of the CIF value. What is the landed cost?",
              f"ইস্পাতের তারের বিদেশি কারখানায় দাম {price:,} টাকা। ভাড়া {freight:,} টাকা, বিমা দামের {ins_pct}%, আর শুল্ক সিআইএফ মূল্যের {duty_pct}%। পৌঁছানো খরচ কত?", r,
              f"CIF = {price:,} + {freight:,} + {price * ins_pct // 100:,} = {cif:,}; duty = {duty:,}; landed = Rs {r:,}.",
              f"সিআইএফ = {price:,} + {freight:,} + {price * ins_pct // 100:,} = {cif:,}; শুল্ক = {duty:,}; পৌঁছানো = {r:,} টাকা।",
              (cif, price + freight, price + price * duty_pct // 100), "", " টাকা", "Rs ")


def pareto(top, total, what_en, what_bn):
    r = _c(top * 100 / total)
    return _n(f"The top 20% of {what_en} account for Rs {top:,} lakh of a total Rs {total:,} lakh spend. What share is that?",
              f"শীর্ষ 20% {what_bn} মোট {total:,} লাখ টাকা খরচের {top:,} লাখ টাকা। সেটা কত ভাগ?", r,
              f"{top:,} ÷ {total:,} x 100 = {r:g}% - a classic Pareto pattern; focus management effort there.",
              f"{top:,} ÷ {total:,} x 100 = {r:g}% - ধ্রুপদী প্যারেটো নকশা; সেখানে ব্যবস্থাপনার মনোযোগ দাও।",
              (20, _c(100 - r), _c(r / 2)), "%", "%")


def betoll(cost_cr, vehicles, days):
    r = _c(cost_cr * 10_000_000 / (vehicles * days))
    return _n(f"A toll bridge must recover Rs {cost_cr} crore a year (operations and debt). It expects {vehicles:,} vehicles a day for {days} days. What average toll breaks even?",
              f"একটা টোল-সেতুকে বছরে {cost_cr} কোটি টাকা তুলতে হবে (চালনা আর ঋণ)। দিনে {vehicles:,}টি যান আর {days} দিন প্রত্যাশিত। গড়ে কত টোলে লাভ-লোকসান সমান?", r,
              f"{cost_cr} crore = Rs {cost_cr * 10_000_000:,}; ÷ ({vehicles:,} x {days}) = Rs {r:g} per vehicle.",
              f"{cost_cr} কোটি = {cost_cr * 10_000_000:,} টাকা; ÷ ({vehicles:,} x {days}) = যানপ্রতি {r:g} টাকা।",
              (_c(cost_cr * 10_000_000 / vehicles / 100), _c(r * 2), _c(r + 25)), "", " টাকা", "Rs ")


ITEMS = (
    pert(10, 14, 24, "pile driving", "পাইল বসানো"), pert(5, 8, 17, "deck waterproofing", "পাটাতন জলরোধী করা"),
    pert(20, 30, 46, "pier construction", "স্তম্ভ নির্মাণ"), pert(2, 4, 12, "bearing installation", "বিয়ারিং বসানো"),
    safety(20, 4), safety(30, 9), safety(12, 16), safety(50, 1),
    mm1(2, 3), mm1(3, 4), mm1(4, 5), mm1(9, 10),
    crash(200000, 260000, 10, 7, "Casting a pier", "একটা স্তম্ভ ঢালাই"), crash(500000, 620000, 20, 16, "Erecting girders", "গার্ডার খাড়া করা"),
    crash(80000, 104000, 6, 4, "Laying the deck slab", "পাটাতনের স্ল্যাব বসানো"),
    gencost(20000, 30, 32000, 12, 500), gencost(15000, 20, 18000, 10, 200), gencost(40000, 48, 60000, 20, 1000),
    empty(12000, 40000), empty(7000, 28000), empty(5000, 25000), empty(18000, 45000),
    fill(26.4, 33), fill(19.8, 33), fill(29.7, 33),
    landed(1000000, 80000, 1, 10), landed(500000, 40000, 2, 7), landed(2000000, 150000, 1, 5),
    pareto(640, 800, "suppliers", "সরবরাহকারী"), pareto(450, 600, "spare-part lines", "খুচরো যন্ত্রাংশের ধরন"), pareto(350, 500, "customers", "খদ্দের"),
    betoll(20, 10000, 365), betoll(36, 15000, 360), betoll(73, 40000, 365), betoll(45, 25000, 360), betoll(12, 4000, 300),
    pert(3, 6, 15, "scour protection", "ক্ষয়-রোধী সুরক্ষা"), pert(12, 18, 36, "cable spinning", "তার পাকানো"), safety(25, 6), mm1(6, 8),
    crash(150000, 195000, 8, 5, "Installing expansion joints", "প্রসারণ-জোড় বসানো"), crash(300000, 340000, 12, 10, "Painting the girders", "গার্ডারে রং"),
    gencost(25000, 36, 30000, 16, 400), empty(4000, 32000), fill(16.5, 33), landed(800000, 60000, 1, 12),
    pareto(560, 700, "repair jobs", "মেরামতের কাজ"), safety(40, 2),
    mcq("Why does PERT weight the 'most likely' estimate four times?", ["It approximates a realistic spread where the likely value matters most but extremes still count", "Four is a lucky number", "To ignore risks", "To make every task longer"], 0,
        "It also gives a standard deviation: (p - o) ÷ 6.",
        "পার্ট কেন 'সবচেয়ে সম্ভাব্য' আন্দাজকে চারগুণ ওজন দেয়?", ["বাস্তবসম্মত বিস্তারের কাছাকাছি আনে, যেখানে সম্ভাব্য মান সবচেয়ে জরুরি কিন্তু চরম মানও গোনা হয়", "চার শুভ সংখ্যা", "ঝুঁকি উপেক্ষা করতে", "প্রতিটা কাজ লম্বা করতে"],
        "এটা প্রমিত বিচ্যুতিও দেয়: (p - o) ÷ 6।"),
    mcq("What does 'crashing' a project mean?", ["Adding resources to shorten critical tasks, at extra cost, to finish earlier", "Demolishing the bridge", "Stopping the project", "Reducing quality"], 0,
        "Only crashing critical-path tasks shortens the project.",
        "প্রকল্প 'দ্রুতকরণ' (ক্র্যাশিং) মানে কী?", ["বাড়তি খরচে সম্পদ যোগ করে সংকট-পথের কাজ ছোট করা, যাতে আগে শেষ হয়", "সেতু ভেঙে ফেলা", "প্রকল্প থামানো", "মান কমানো"],
        "শুধু সংকট-পথের কাজ দ্রুত করলেই প্রকল্প ছোট হয়।"),
    mcq("Why can crashing one task too much stop helping?", ["Another path may become critical, so further spending on the first task saves no time", "Tasks get longer when crashed", "Crashing always helps", "Money runs out instantly"], 0,
        "Re-check the network after each change.",
        "একটা কাজ খুব বেশি দ্রুত করলে আর সাহায্য হয় না কেন?", ["অন্য একটা পথ সংকট-পথ হয়ে যেতে পারে, তাই প্রথম কাজে আরও খরচে সময় বাঁচে না", "দ্রুত করলে কাজ লম্বা হয়", "দ্রুত করা সবসময় সাহায্য করে", "তখনই টাকা ফুরোয়"],
        "প্রতিটা বদলের পরে জালটা আবার যাচাই করো।"),
    mcq("What is 'resource levelling' in scheduling?", ["Adjusting task timing so demand for crews or equipment is smoother, without unnecessary peaks", "Making the site flat", "Hiring as many workers as possible", "Removing all resources"], 0,
        "It may extend the project slightly but cuts overtime and idle time.",
        "সময়সূচিতে 'সম্পদ-সমতাকরণ' কী?", ["কাজের সময় সমন্বয় করা, যাতে দল বা যন্ত্রের চাহিদা মসৃণ হয়, অকারণ চূড়া ছাড়া", "নির্মাণস্থল সমতল করা", "যত বেশি সম্ভব কর্মী নেওয়া", "সব সম্পদ সরানো"],
        "প্রকল্প একটু লম্বা হতে পারে, কিন্তু ওভারটাইম আর অলস সময় কমে।"),
    mcq("Why is safety stock linked to the square root of lead time?", ["Random daily variations partly cancel out over several days, so uncertainty grows more slowly than lead time", "Lead time does not matter", "It is a coincidence", "Safety stock falls as lead time grows"], 0,
        "Doubling lead time raises safety stock by about 41%, not 100%.",
        "নিরাপত্তা-মজুত সরবরাহ-সময়ের বর্গমূলের সঙ্গে যুক্ত কেন?", ["কয়েক দিনে এলোমেলো দৈনিক ওঠানামা আংশিক কাটাকাটি হয়, তাই অনিশ্চয়তা সরবরাহ-সময়ের চেয়ে ধীরে বাড়ে", "সরবরাহ-সময় গুরুত্বহীন", "কাকতালীয়", "সরবরাহ-সময় বাড়লে মজুত কমে"],
        "সরবরাহ-সময় দ্বিগুণ হলে নিরাপত্তা-মজুত প্রায় 41% বাড়ে, 100% নয়।"),
    mcq("What does raising the service level from 95% to 99% do to safety stock?", ["It increases it a lot - the last few percent of reliability are expensive", "It halves it", "No change", "It removes it"], 0,
        "z rises from about 1.65 to 2.33.",
        "পরিষেবা-স্তর 95% থেকে 99% করলে নিরাপত্তা-মজুতের কী হয়?", ["অনেক বাড়ে - ভরসার শেষ কয়েক শতাংশ দামি", "অর্ধেক হয়", "বদলায় না", "উঠে যায়"],
        "z প্রায় 1.65 থেকে 2.33-এ বাড়ে।"),
    mcq("In queuing, what happens to waiting time as utilisation approaches 100%?", ["It grows very sharply towards infinity", "It falls to zero", "It stays constant", "It halves"], 0,
        "Toll plazas and site gates are designed with spare capacity for this reason.",
        "লাইনে দাঁড়ানোর তত্ত্বে ব্যবহার-হার 100%-এর দিকে গেলে অপেক্ষার সময়ের কী হয়?", ["খুব তীব্রভাবে অসীমের দিকে বাড়ে", "শূন্যে নামে", "স্থির থাকে", "অর্ধেক হয়"],
        "এই কারণে টোল-প্লাজা আর নির্মাণস্থলের ফটক বাড়তি ক্ষমতা রেখে নকশা হয়।"),
    mcq("What is 'generalised cost' in transport planning?", ["Money cost plus the value of time and other inconveniences of a journey", "Only the ticket price", "Only fuel cost", "The cost of building roads"], 0,
        "It explains why people pay more for faster options.",
        "পরিবহন-পরিকল্পনায় 'সাধারণীকৃত খরচ' কী?", ["টাকার খরচ যোগ যাত্রার সময় আর অন্য অসুবিধার মূল্য", "শুধু টিকিটের দাম", "শুধু জ্বালানির খরচ", "রাস্তা বানানোর খরচ"],
        "মানুষ কেন দ্রুত বিকল্পে বেশি দেয়, তা ব্যাখ্যা করে।"),
    mcq("What is 'modal shift' and why do governments encourage it for freight?", ["Moving freight from road to rail or water to cut congestion, emissions and road damage", "Changing fashion models", "Moving offices", "Switching truck brands"], 0,
        "Dedicated freight corridors and river terminals support it.",
        "'পরিবহন-মাধ্যম বদল' কী আর সরকার মালবহনে কেন উৎসাহ দেয়?", ["যানজট, নির্গমন আর রাস্তার ক্ষতি কমাতে মাল সড়ক থেকে রেল বা জলপথে সরানো", "ফ্যাশন-মডেল বদল", "অফিস সরানো", "ট্রাকের ব্র্যান্ড বদল"],
        "নির্দিষ্ট মালবাহী করিডর আর নদী-টার্মিনাল এটা সমর্থন করে।"),
    mcq("What is the 'Kraljic matrix' used for in procurement?", ["Classifying purchases by profit impact and supply risk to choose the right buying strategy", "Designing bridges", "Calculating tax", "Scheduling workers"], 0,
        "Strategic items (high impact, high risk) need close partnerships.",
        "ক্রয়ে 'ক্রালিচ ম্যাট্রিক্স' কীসের জন্য ব্যবহার হয়?", ["লাভে প্রভাব আর জোগান-ঝুঁকি দিয়ে কেনাকাটা শ্রেণিবদ্ধ করে ঠিক ক্রয়-কৌশল বাছা", "সেতুর নকশা", "কর হিসাব", "কর্মীদের সময়সূচি"],
        "কৌশলগত জিনিস (বেশি প্রভাব, বেশি ঝুঁকি) ঘনিষ্ঠ অংশীদারি চায়।"),
    mcq("In the Kraljic matrix, where would specialised cable-stay systems from only two suppliers worldwide fall?", ["Strategic or bottleneck - high supply risk, so secure supply early", "Routine - buy from anyone", "Leverage - push prices down hard", "Not important"], 0,
        "Few suppliers and long lead times make them critical to the schedule.",
        "ক্রালিচ ম্যাট্রিক্সে বিশ্বে মাত্র দুজন সরবরাহকারীর বিশেষ কেবল-স্টে ব্যবস্থা কোথায় পড়বে?", ["কৌশলগত বা বাধা-জিনিস - উচ্চ জোগান-ঝুঁকি, তাই আগেভাগে জোগান নিশ্চিত করো", "সাধারণ - যে কারও থেকে কেনো", "দর-কষাকষির জিনিস - জোর করে দাম নামাও", "গুরুত্বহীন"],
        "কম সরবরাহকারী আর লম্বা সরবরাহ-সময় এগুলোকে সময়সূচির জন্য জরুরি করে।"),
    mcq("What are 'routine' (non-critical) items in procurement, such as nails and gloves?", ["Low value and low risk - buy efficiently with simple processes", "The most strategic items", "Items that need years of negotiation", "Items that cannot be bought"], 0,
        "Framework agreements and e-catalogues save time on them.",
        "ক্রয়ে 'সাধারণ' (অ-জরুরি) জিনিস, যেমন পেরেক আর দস্তানা, কী?", ["কম মূল্য আর কম ঝুঁকি - সরল পদ্ধতিতে দক্ষভাবে কেনো", "সবচেয়ে কৌশলগত জিনিস", "বছরের দর-কষাকষি লাগে এমন জিনিস", "কেনা যায় না এমন জিনিস"],
        "কাঠামো-চুক্তি আর ই-ক্যাটালগ এতে সময় বাঁচায়।"),
    mcq("What are FIDIC contracts?", ["Internationally used standard forms of construction contract, such as the Red, Yellow and Silver Books", "A type of steel", "A bank in Switzerland only", "A traffic rule"], 0,
        "Standard forms make risk allocation familiar to all parties.",
        "ফিডিক চুক্তি কী?", ["আন্তর্জাতিকভাবে ব্যবহৃত নির্মাণ-চুক্তির প্রমিত রূপ, যেমন রেড, ইয়েলো আর সিলভার বুক", "এক রকম ইস্পাত", "শুধু সুইজারল্যান্ডের একটা ব্যাংক", "একটা ট্রাফিক-নিয়ম"],
        "প্রমিত রূপ সব পক্ষের কাছে ঝুঁকি-বণ্টন পরিচিত রাখে।"),
    mcq("Under a 'design and build' contract, who is responsible for the design?", ["The contractor", "The client alone", "The bank", "The public"], 0,
        "It gives the contractor freedom to choose efficient methods - and the design risk.",
        "'নকশা-ও-নির্মাণ' চুক্তিতে নকশার দায়িত্ব কার?", ["ঠিকাদারের", "শুধু গ্রাহকের", "ব্যাংকের", "জনসাধারণের"],
        "ঠিকাদারকে দক্ষ পদ্ধতি বাছার স্বাধীনতা দেয় - আর নকশার ঝুঁকিও।"),
    mcq("What is a 'measurement' (re-measurement) contract?", ["The client pays agreed unit rates for the actual quantities of work done", "A fixed lump sum regardless of work", "Payment only in goods", "No payment until 10 years later"], 0,
        "It suits work like piling where quantities are uncertain at the start.",
        "'পরিমাপ' (পুনঃপরিমাপ) চুক্তি কী?", ["করা কাজের আসল পরিমাণে গ্রাহক ঠিক-করা একক-দর দেন", "কাজ যা-ই হোক নির্দিষ্ট থোক অঙ্ক", "শুধু মালে পেমেন্ট", "10 বছর পরে পর্যন্ত পেমেন্ট নেই"],
        "পাইলিংয়ের মতো কাজে, যেখানে শুরুতে পরিমাণ অনিশ্চিত, মানানসই।"),
    mcq("What is a 'bill of quantities' (BOQ)?", ["A list of items of work with their quantities, which bidders price", "A list of bills already paid", "A shopping receipt", "A bank statement"], 0,
        "It lets bids be compared item by item.",
        "'পরিমাণের তালিকা' (বিওকিউ) কী?", ["কাজের জিনিসগুলোর পরিমাণসহ তালিকা, যাতে দরদাতারা দাম বসান", "আগেই মেটানো বিলের তালিকা", "কেনাকাটার রসিদ", "ব্যাংক-বিবরণী"],
        "জিনিস ধরে ধরে দর তুলনা করতে দেয়।"),
    mcq("What is 'unbalanced bidding'?", ["Pricing some BOQ items high and others low to gain if quantities change, while keeping the total competitive", "Bidding on two projects at once", "A bid with no prices", "A bid in another currency"], 0,
        "Clients check unit rates to spot and manage it.",
        "'ভারসাম্যহীন দর' কী?", ["মোট দর প্রতিযোগিতামূলক রেখে বিওকিউ-এর কিছু জিনিস বেশি আর কিছু কম দামে বসানো, যাতে পরিমাণ বদলালে লাভ হয়", "একসঙ্গে দুটো প্রকল্পে দর", "দামহীন দর", "অন্য মুদ্রায় দর"],
        "গ্রাহকরা একক-দর যাচাই করে এটা ধরেন আর সামলান।"),
    mcq("What is 'peak-load pricing' for a toll bridge?", ["Charging more at busy times and less at quiet times to spread demand", "One price all day", "Free tolls at rush hour", "Charging by vehicle colour"], 0,
        "It uses existing capacity better than building new lanes.",
        "টোল-সেতুর 'ভিড়-সময়ের দাম' কী?", ["ভিড়ের সময় বেশি আর ফাঁকা সময়ে কম নিয়ে চাহিদা ছড়ানো", "সারাদিন একই দাম", "ব্যস্ত সময়ে বিনামূল্যে", "গাড়ির রং ধরে দাম"],
        "নতুন লেন বানানোর চেয়ে বিদ্যমান ক্ষমতা ভালো কাজে লাগায়।"),
    mcq("What is 'price discrimination' in toll setting?", ["Charging different groups different prices, such as discounts for local residents or monthly passes", "Charging illegal prices", "Refusing some vehicles", "Charging only trucks"], 0,
        "It can be fair when it reflects different needs or costs.",
        "টোল ঠিক করায় 'দাম-বৈষম্য' কী?", ["আলাদা দলকে আলাদা দাম, যেমন স্থানীয় বাসিন্দাদের ছাড় বা মাসিক পাস", "বেআইনি দাম", "কিছু গাড়ি ফিরিয়ে দেওয়া", "শুধু ট্রাকের দাম"],
        "আলাদা প্রয়োজন বা খরচ প্রতিফলিত হলে ন্যায্য হতে পারে।"),
    mcq("Why do toll rates usually differ by vehicle class (car, bus, truck)?", ["Heavier vehicles cause much more wear, and toll rules reflect that and their use of space", "Truck drivers earn more", "Cars are not allowed", "It is random"], 0,
        "Road damage rises very steeply with axle load.",
        "গাড়ির ধরন (গাড়ি, বাস, ট্রাক) অনুযায়ী টোলের হার সাধারণত আলাদা কেন?", ["ভারী গাড়ি অনেক বেশি ক্ষয় করে, আর টোল-নিয়ম তা আর তাদের জায়গা-ব্যবহার প্রতিফলিত করে", "ট্রাক-চালকরা বেশি আয় করেন", "গাড়ি নিষিদ্ধ", "এলোমেলো"],
        "অক্ষ-বোঝার সঙ্গে রাস্তার ক্ষতি খুব তীব্রভাবে বাড়ে।"),
    mcq("What is the 'fourth power law' in road and bridge deck wear?", ["Damage rises roughly with the fourth power of axle load - double the load, about 16 times the damage", "Damage is unrelated to load", "Damage halves with heavier trucks", "Four trucks cause no damage"], 0,
        "That is why overloaded trucks are fined heavily.",
        "রাস্তা আর সেতু-পাটাতনের ক্ষয়ে 'চতুর্থ ঘাতের সূত্র' কী?", ["ক্ষতি মোটামুটি অক্ষ-বোঝার চতুর্থ ঘাতে বাড়ে - বোঝা দ্বিগুণ, ক্ষতি প্রায় 16 গুণ", "ক্ষতি বোঝার সঙ্গে সম্পর্কহীন", "ভারী ট্রাকে ক্ষতি অর্ধেক", "চারটে ট্রাকে কোনো ক্ষতি নেই"],
        "তাই অতিরিক্ত বোঝাই ট্রাককে কড়া জরিমানা।"),
    mcq("What is 'weigh-in-motion' (WIM) on a bridge approach?", ["Sensors in the road that weigh vehicles as they drive over, catching overloads", "A scale for workers", "A gym on the bridge", "A toll booth with no staff"], 0,
        "Data also helps engineers understand real bridge loading.",
        "সেতুর সংযোগ-পথে 'চলমান অবস্থায় ওজন' (ডব্লিউআইএম) কী?", ["রাস্তায় বসানো সেন্সর, যা চলতে চলতে গাড়ি ওজন করে অতিরিক্ত বোঝা ধরে", "কর্মীদের দাঁড়িপাল্লা", "সেতুর উপর জিম", "কর্মীহীন টোল-বুথ"],
        "তথ্য প্রকৌশলীদের সেতুর আসল বোঝা বুঝতেও সাহায্য করে।"),
    mcq("What is 'demurrage' versus 'detention' in container shipping?", ["Demurrage is for containers kept too long at the port; detention for keeping them too long outside the port", "They are identical", "Both are discounts", "Detention is a prison"], 0,
        "Both add cost if the site is not ready to receive goods.",
        "কনটেনার-জাহাজিতে 'ডেমারেজ' আর 'ডিটেনশন'-এর পার্থক্য কী?", ["ডেমারেজ বন্দরে বেশিদিন কনটেনার রাখার জন্য; ডিটেনশন বন্দরের বাইরে বেশিদিন রাখার জন্য", "দুটো হুবহু এক", "দুটোই ছাড়", "ডিটেনশন মানে কারাগার"],
        "নির্মাণস্থল মাল নিতে তৈরি না থাকলে দুটোই খরচ বাড়ায়।"),
    mcq("Under a letter of credit, why must the bill of lading's description of the cables match the credit exactly?", ["Banks pay only against documents that strictly comply - a mismatch can delay or block payment", "Banks never read documents", "Any description is accepted", "It only matters for food shipments"], 0,
        "Exporters check every word, date and quantity before presenting documents.",
        "ঋণপত্রে জাহাজি রসিদে তারের বিবরণ ঋণপত্রের সঙ্গে হুবহু মিলতে হবে কেন?", ["ব্যাংক শুধু কড়াভাবে মেলা নথিতে টাকা দেয় - অমিল হলে পেমেন্ট দেরি বা আটকে যেতে পারে", "ব্যাংক কখনো নথি পড়ে না", "যেকোনো বিবরণ চলে", "শুধু খাবারের চালানে গুরুত্বপূর্ণ"],
        "নথি দেওয়ার আগে রপ্তানিকারকরা প্রতিটা শব্দ, তারিখ আর পরিমাণ যাচাই করেন।"),
    mcq("What does a customs broker do for an importer of bridge bearings?", ["Prepares and files customs paperwork, classifies goods and arranges payment of duties", "Builds the bearings", "Drives the delivery truck", "Sets the import tariff"], 0,
        "Correct classification avoids delays and penalties.",
        "সেতু-বিয়ারিংয়ের আমদানিকারকের জন্য একজন শুল্ক-দালাল কী করেন?", ["শুল্কের কাগজপত্র তৈরি আর জমা, মালের শ্রেণিবিভাগ আর শুল্ক-পরিশোধের ব্যবস্থা", "বিয়ারিং বানান", "ডেলিভারি-ট্রাক চালান", "আমদানি-শুল্ক ঠিক করেন"],
        "ঠিক শ্রেণিবিভাগ দেরি আর জরিমানা এড়ায়।"),
    mcq("What is 'transshipment'?", ["Moving cargo from one vessel or vehicle to another at an intermediate point on its journey", "Shipping goods directly with no stops", "Cancelling a shipment", "Painting a ship"], 0,
        "Each transfer adds handling time and damage risk.",
        "'মাঝপথে পরিবহন-বদল' (ট্রানশিপমেন্ট) কী?", ["যাত্রার মাঝের কোনো জায়গায় মাল এক জাহাজ বা গাড়ি থেকে আরেকটায় সরানো", "না থেমে সরাসরি মাল পাঠানো", "চালান বাতিল", "জাহাজ রং করা"],
        "প্রতিটা বদলে নাড়াচাড়ার সময় আর ক্ষতির ঝুঁকি বাড়ে।"),
    mcq("What is a 'bonded warehouse'?", ["A secure store where imported goods can be held without paying duty until they are released", "A warehouse built with bonds", "A free public store", "A warehouse for bank bonds"], 0,
        "It helps importers manage cash flow when goods arrive early.",
        "'শুল্ক-বন্ধক গুদাম' (বন্ডেড ওয়্যারহাউস) কী?", ["নিরাপদ গুদাম, যেখানে আমদানি-করা মাল ছাড়ার আগে পর্যন্ত শুল্ক না দিয়ে রাখা যায়", "বন্ড দিয়ে বানানো গুদাম", "বিনামূল্যের সরকারি গুদাম", "ব্যাংক-বন্ডের গুদাম"],
        "মাল আগে এলে আমদানিকারককে নগদপ্রবাহ সামলাতে সাহায্য করে।"),
    mcq("What is a 'bill of entry' in Indian customs?", ["The importer's declaration to customs describing the goods and their value so duty can be assessed", "A restaurant bill", "A list of workers entering a site", "An exit permit"], 0,
        "Errors in it can lead to fines or held cargo.",
        "ভারতীয় শুল্কে 'প্রবেশপত্র' (বিল অফ এন্ট্রি) কী?", ["আমদানিকারকের শুল্ক-দপ্তরে ঘোষণা, যাতে মাল আর মূল্যের বিবরণ থাকে, যাতে শুল্ক নির্ধারণ হয়", "রেস্তোরাঁর বিল", "নির্মাণস্থলে ঢোকা কর্মীদের তালিকা", "বেরোনোর অনুমতিপত্র"],
        "এতে ভুল থাকলে জরিমানা বা মাল আটকে যেতে পারে।"),
    mcq("What is a 'certificate of origin'?", ["A document stating which country goods were made in, used for customs duties and trade deals", "A birth certificate", "A degree certificate", "A safety certificate"], 0,
        "Trade agreements may lower duty for goods from certain countries.",
        "'উৎস-শংসাপত্র' কী?", ["মাল কোন দেশে তৈরি তা জানানো নথি, শুল্ক আর বাণিজ্য-চুক্তিতে ব্যবহৃত", "জন্ম-শংসাপত্র", "ডিগ্রি-শংসাপত্র", "নিরাপত্তা-শংসাপত্র"],
        "বাণিজ্য-চুক্তি কিছু দেশের মালে শুল্ক কমাতে পারে।"),
    mcq("What is 'DDP' (delivered duty paid) under Incoterms?", ["The seller pays all costs and duties to deliver goods to the buyer's named place", "The buyer pays everything", "Goods are delivered without paperwork", "Duty is never paid"], 0,
        "It is the most convenient - and usually most expensive - option for a buyer.",
        "ইনকোটার্মে 'ডিডিপি' (শুল্ক-পরিশোধিত পৌঁছানো) কী?", ["ক্রেতার বলা জায়গায় মাল পৌঁছাতে বিক্রেতা সব খরচ আর শুল্ক দেন", "ক্রেতা সব দেন", "কাগজপত্র ছাড়া মাল পৌঁছায়", "শুল্ক কখনো দেওয়া হয় না"],
        "ক্রেতার জন্য সবচেয়ে সুবিধার - আর সাধারণত সবচেয়ে দামি - বিকল্প।"),
    mcq("What is 'EXW' (ex works) under Incoterms?", ["The buyer collects from the seller's premises and bears nearly all costs and risks", "The seller delivers to site", "Delivery by air only", "Duty-free delivery"], 0,
        "It suits buyers with strong logistics of their own.",
        "ইনকোটার্মে 'এক্সডব্লিউ' (কারখানা-থেকে) কী?", ["ক্রেতা বিক্রেতার জায়গা থেকে মাল তোলেন আর প্রায় সব খরচ আর ঝুঁকি নেন", "বিক্রেতা নির্মাণস্থলে পৌঁছান", "শুধু বিমানে পৌঁছানো", "শুল্কমুক্ত পৌঁছানো"],
        "নিজস্ব জোরালো পরিবহন-ব্যবস্থার ক্রেতার জন্য মানানসই।"),
    mcq("Why do international bridge projects often price imported items in foreign currency?", ["Suppliers want to avoid exchange-rate risk, so the buyer must manage it", "Rupees cannot be used abroad ever", "Foreign currency is cheaper", "It is required for steel only"], 0,
        "Contracts may include currency adjustment clauses or hedging.",
        "আন্তর্জাতিক সেতু-প্রকল্পে আমদানি-করা জিনিসের দাম প্রায়ই বিদেশি মুদ্রায় ধরা হয় কেন?", ["সরবরাহকারীরা বিনিময়-হারের ঝুঁকি এড়াতে চান, তাই ক্রেতাকে তা সামলাতে হয়", "টাকা বিদেশে কখনো ব্যবহার করা যায় না", "বিদেশি মুদ্রা সস্তা", "শুধু ইস্পাতের জন্য বাধ্যতামূলক"],
        "চুক্তিতে মুদ্রা-সমন্বয় ধারা বা হেজিং থাকতে পারে।"),
    mcq("What is a 'supply chain map'?", ["A diagram of all the tiers of suppliers, routes and facilities behind a product", "A road map", "A map of the bridge site only", "A tourist map"], 0,
        "It reveals hidden single points of failure several tiers back.",
        "'সরবরাহ-শৃঙ্খলের মানচিত্র' কী?", ["একটা পণ্যের পিছনের সব স্তরের সরবরাহকারী, পথ আর কেন্দ্রের চিত্র", "রাস্তার মানচিত্র", "শুধু সেতু-নির্মাণস্থলের মানচিত্র", "পর্যটন-মানচিত্র"],
        "কয়েক স্তর পিছনে লুকোনো একক ব্যর্থতা-বিন্দু প্রকাশ করে।"),
    mcq("What are 'tier 2' suppliers?", ["The suppliers to your direct suppliers", "Your direct suppliers", "Your customers", "Government regulators"], 0,
        "A steel fabricator's tier 2 might be the steel mill and its paint supplier.",
        "'স্তর 2' সরবরাহকারী কারা?", ["তোমার সরাসরি সরবরাহকারীদের সরবরাহকারী", "তোমার সরাসরি সরবরাহকারী", "তোমার খদ্দের", "সরকারি নিয়ন্ত্রক"],
        "একজন ইস্পাত-ফ্যাব্রিকেটরের স্তর 2 হতে পারে ইস্পাত-কারখানা আর তার রঙের সরবরাহকারী।"),
    mcq("What is 'nearshoring' for a construction supplier?", ["Moving production closer to the main market to cut lead times and transport risk", "Building near the sea only", "Closing factories", "Importing from the farthest country"], 0,
        "Shorter supply lines make projects more resilient.",
        "নির্মাণ-সরবরাহকারীর জন্য 'নিকটে-সরানো' (নিয়ারশোরিং) কী?", ["সরবরাহ-সময় আর পরিবহন-ঝুঁকি কমাতে উৎপাদন প্রধান বাজারের কাছে সরানো", "শুধু সমুদ্রের কাছে নির্মাণ", "কারখানা বন্ধ", "সবচেয়ে দূরের দেশ থেকে আমদানি"],
        "ছোট সরবরাহ-পথ প্রকল্পকে বেশি সহনশীল করে।"),
    mcq("What is 'total landed cost' compared with 'unit price' when sourcing abroad?", ["Landed cost adds freight, insurance, duties, handling and delays to the unit price", "They are always equal", "Unit price is always higher", "Landed cost ignores transport"], 0,
        "A cheap foreign price can become expensive once landed.",
        "বিদেশ থেকে সংগ্রহে 'মোট পৌঁছানো খরচ' আর 'একক-দাম'-এর তুলনা কী?", ["পৌঁছানো খরচ একক-দামে ভাড়া, বিমা, শুল্ক, নাড়াচাড়া আর দেরি যোগ করে", "সবসময় সমান", "একক-দাম সবসময় বেশি", "পৌঁছানো খরচ পরিবহন উপেক্ষা করে"],
        "সস্তা বিদেশি দাম পৌঁছানোর পরে দামি হতে পারে।"),
    mcq("What does 'Pareto analysis' help a bridge maintenance manager do?", ["Focus on the few defect types or locations causing most of the cost", "Treat every defect equally", "Ignore costly problems", "Paint the bridge"], 0,
        "Fixing the vital few gives the biggest benefit.",
        "'প্যারেটো বিশ্লেষণ' সেতু-রক্ষণাবেক্ষণ ম্যানেজারকে কী করতে সাহায্য করে?", ["বেশিরভাগ খরচ ঘটানো কয়েকটা ত্রুটির ধরন বা জায়গায় মনোযোগ দিতে", "প্রতিটা ত্রুটিকে সমান দেখতে", "দামি সমস্যা উপেক্ষা করতে", "সেতু রং করতে"],
        "জরুরি কয়েকটা সারালে সবচেয়ে বেশি সুফল।"),
    mcq("What is a 'fishbone' (Ishikawa) diagram used for?", ["Organising the possible causes of a problem into categories like people, methods, materials and machines", "Drawing fish", "Planning a menu", "Mapping rivers"], 0,
        "It is a root-cause analysis tool used after defects or accidents.",
        "'মাছের কাঁটা' (ইশিকাওয়া) চিত্র কীসের জন্য ব্যবহার হয়?", ["সমস্যার সম্ভাব্য কারণকে মানুষ, পদ্ধতি, উপাদান আর যন্ত্রের মতো শ্রেণিতে সাজাতে", "মাছ আঁকতে", "খাবারের তালিকা পরিকল্পনা", "নদীর মানচিত্র"],
        "ত্রুটি বা দুর্ঘটনার পরে মূল কারণ খোঁজার হাতিয়ার।"),
    mcq("What are the 'five whys'?", ["Asking 'why?' repeatedly to dig from a symptom down to a root cause", "Five reasons to quit", "Five steps to build a bridge", "A type of contract"], 0,
        "A late delivery may trace back to a missing purchase-order approval.",
        "'পাঁচটা কেন' কী?", ["উপসর্গ থেকে মূল কারণে পৌঁছাতে বারবার 'কেন?' জিজ্ঞাসা করা", "ছাড়ার পাঁচটা কারণ", "সেতু বানানোর পাঁচ ধাপ", "এক রকম চুক্তি"],
        "দেরির ডেলিভারি হয়তো একটা না-মেলা ক্রয়াদেশ-অনুমোদনে গিয়ে ঠেকে।"),
    mcq("What is 'PDCA' (plan-do-check-act)?", ["A cycle for continuous improvement: plan a change, try it, check results, then standardise or adjust", "A type of crane", "A payment method", "A safety helmet"], 0,
        "It underpins quality systems like ISO 9001.",
        "'পিডিসিএ' (পরিকল্পনা-করো-যাচাই-ব্যবস্থা) কী?", ["নিরন্তর উন্নতির চক্র: বদল পরিকল্পনা, চেষ্টা, ফল যাচাই, তারপর প্রমিত করা বা সমন্বয়", "এক রকম ক্রেন", "পেমেন্টের পদ্ধতি", "নিরাপত্তা-হেলমেট"],
        "আইএসও 9001-এর মতো মান-ব্যবস্থার ভিত্তি।"),
    mcq("What is a 'control chart' used for in production of precast segments?", ["Tracking a measurement over time to spot when a process drifts out of control", "Controlling a crane", "Showing the company's organisation", "Listing customers"], 0,
        "Points outside the limits signal a problem to investigate.",
        "প্রিকাস্ট-খণ্ডের উৎপাদনে 'নিয়ন্ত্রণ-চার্ট' কীসের জন্য ব্যবহার হয়?", ["সময়ের সঙ্গে একটা মাপ নজরে রেখে প্রক্রিয়া কখন নিয়ন্ত্রণের বাইরে সরছে ধরা", "ক্রেন নিয়ন্ত্রণ", "কোম্পানির সংগঠন দেখানো", "খদ্দেরের তালিকা"],
        "সীমার বাইরের বিন্দু খুঁজে দেখার মতো সমস্যার সংকেত।"),
    mcq("What is 'just-in-sequence' delivery for precast bridge segments?", ["Delivering segments in the exact order they will be erected, straight to the crane", "Delivering everything at once", "Delivering in random order", "Delivering after erection"], 0,
        "It saves space and double handling on cramped sites.",
        "প্রিকাস্ট সেতু-খণ্ডের 'ঠিক-ক্রমে' ডেলিভারি কী?", ["যে ক্রমে খাড়া হবে ঠিক সেই ক্রমে খণ্ড সরাসরি ক্রেনের কাছে পৌঁছানো", "সব একসঙ্গে পৌঁছানো", "এলোমেলো ক্রমে পৌঁছানো", "খাড়া করার পরে পৌঁছানো"],
        "ঘিঞ্জি নির্মাণস্থলে জায়গা আর দুবার নাড়াচাড়া বাঁচায়।"),
    mcq("What is 'lean' thinking's idea of 'waste' (muda) in construction logistics?", ["Any activity that adds cost but no value, such as waiting, double handling or excess stock", "Only rubbish in skips", "Profit", "Safety checks"], 0,
        "Removing waste speeds work and cuts cost without cutting quality.",
        "নির্মাণ-পরিবহনে 'লিন' ভাবনার 'অপচয়' (মুদা) কী?", ["যে কাজ খরচ যোগ করে কিন্তু মূল্য নয়, যেমন অপেক্ষা, দুবার নাড়াচাড়া বা বাড়তি মজুত", "শুধু আবর্জনা-পাত্রের ময়লা", "লাভ", "নিরাপত্তা-যাচাই"],
        "অপচয় সরালে মান না কমিয়েই কাজ দ্রুত আর খরচ কম।"),
    mcq("What is 'takt time' in repetitive work like casting identical deck segments?", ["The pace needed to meet demand: available time ÷ number of units required", "The time for a coffee break", "The time to build one bridge", "A clock brand"], 0,
        "If takt is 2 days, each casting bed must produce a segment every 2 days.",
        "অভিন্ন পাটাতন-খণ্ড ঢালাইয়ের মতো পুনরাবৃত্ত কাজে 'টাক্ট-সময়' কী?", ["চাহিদা মেটাতে প্রয়োজনীয় তাল: উপলব্ধ সময় ÷ প্রয়োজনীয় একক", "চা-বিরতির সময়", "একটা সেতু বানানোর সময়", "ঘড়ির ব্র্যান্ড"],
        "টাক্ট 2 দিন হলে প্রতিটা ঢালাই-বেডকে প্রতি 2 দিনে একটা খণ্ড দিতে হবে।"),
    mcq("A precast yard must supply 120 segments in 240 working days. What is the takt time?", ["2 days per segment", "0.5 days", "120 days", "240 days"], 0,
        "240 ÷ 120 = 2 days per segment.",
        "একটা প্রিকাস্ট-উঠানকে 240 কাজের দিনে 120টি খণ্ড দিতে হবে। টাক্ট-সময় কত?", ["খণ্ডপ্রতি 2 দিন", "0.5 দিন", "120 দিন", "240 দিন"],
        "240 ÷ 120 = খণ্ডপ্রতি 2 দিন।"),
    mcq("What is 'reverse logistics' for formwork on a bridge project?", ["Returning reusable formwork and props to the depot for cleaning, repair and reuse", "Throwing formwork away", "Buying new formwork each time", "Sending formwork to customers"], 0,
        "Reuse cuts cost and waste.",
        "সেতু-প্রকল্পে ছাঁচের 'উল্টো পরিবহন' কী?", ["আবার-ব্যবহারযোগ্য ছাঁচ আর ঠেকনা পরিষ্কার, মেরামত আর পুনর্ব্যবহারের জন্য ডিপোতে ফেরানো", "ছাঁচ ফেলে দেওয়া", "প্রতিবার নতুন ছাঁচ কেনা", "খদ্দেরকে ছাঁচ পাঠানো"],
        "পুনর্ব্যবহার খরচ আর বর্জ্য কমায়।"),
    mcq("Why do contractors track 'cost to complete' as well as 'cost so far'?", ["To forecast the final cost and act early if it will exceed the budget", "To pay taxes", "Cost so far is all that matters", "It is not useful"], 0,
        "Estimate at completion = actual cost + estimated cost to complete.",
        "ঠিকাদাররা 'এখন পর্যন্ত খরচ'-এর পাশাপাশি 'শেষ করার খরচ' কেন নজরে রাখেন?", ["শেষ খরচের পূর্বাভাস দিতে আর বাজেট ছাড়াবে মনে হলে আগেই ব্যবস্থা নিতে", "কর দিতে", "শুধু এখন পর্যন্ত খরচই গুরুত্বপূর্ণ", "কাজের নয়"],
        "শেষে আনুমানিক খরচ = আসল খরচ + শেষ করার আনুমানিক খরচ।"),
    mcq("What is a 'change management' process in a bridge contract?", ["A formal way to propose, assess, approve and record changes to scope, cost and time", "Changing workers' shifts", "Giving change at a toll booth", "Replacing the manager"], 0,
        "It stops uncontrolled scope creep.",
        "সেতু-চুক্তিতে 'পরিবর্তন-ব্যবস্থাপনা' প্রক্রিয়া কী?", ["পরিধি, খরচ আর সময়ে বদল প্রস্তাব, মূল্যায়ন, অনুমোদন আর নথিভুক্তির আনুষ্ঠানিক উপায়", "কর্মীদের পালা বদল", "টোল-বুথে খুচরো দেওয়া", "ম্যানেজার বদল"],
        "অনিয়ন্ত্রিত পরিধি-বিস্তার আটকায়।"),
    mcq("What is 'stakeholder mapping' by power and interest?", ["Plotting stakeholders by their influence and concern to decide how closely to engage each", "Drawing stakeholders' houses", "A map of power lines", "Listing interest rates"], 0,
        "High-power, high-interest groups need close management.",
        "ক্ষমতা আর আগ্রহ অনুযায়ী 'অংশীজন-মানচিত্রণ' কী?", ["প্রভাব আর উদ্বেগ অনুযায়ী অংশীজনদের সাজিয়ে কাকে কতটা কাছ থেকে যুক্ত করা হবে ঠিক করা", "অংশীজনদের বাড়ি আঁকা", "বিদ্যুৎ-লাইনের মানচিত্র", "সুদের হারের তালিকা"],
        "উচ্চ-ক্ষমতা, উচ্চ-আগ্রহের দলকে ঘনিষ্ঠভাবে সামলাতে হয়।"),
    mcq("Why do bridge projects publish traffic management plans before closures?", ["So businesses, emergency services and the public can plan, reducing economic disruption", "To advertise the contractor", "Closures need no planning", "To increase tolls"], 0,
        "Clear diversions and timings build trust.",
        "সেতু-প্রকল্প বন্ধের আগে যান-ব্যবস্থাপনার পরিকল্পনা প্রকাশ করে কেন?", ["যাতে ব্যবসা, জরুরি পরিষেবা আর জনসাধারণ পরিকল্পনা করতে পারেন, অর্থনৈতিক ব্যাঘাত কমে", "ঠিকাদারের বিজ্ঞাপন দিতে", "বন্ধে পরিকল্পনা লাগে না", "টোল বাড়াতে"],
        "স্পষ্ট ঘুরপথ আর সময় আস্থা গড়ে।"),
    mcq("What is 'social value' in public procurement?", ["Wider benefits a contract delivers, such as local jobs, apprenticeships and community projects", "The social media following of a firm", "The lowest price only", "Parties for workers"], 0,
        "Some tenders give marks for social value alongside price and quality.",
        "সরকারি ক্রয়ে 'সামাজিক মূল্য' কী?", ["চুক্তির বৃহত্তর সুফল, যেমন স্থানীয় চাকরি, শিক্ষানবিশি আর সামাজিক প্রকল্প", "সংস্থার সামাজিক মাধ্যমের অনুসারী", "শুধু সবচেয়ে কম দাম", "কর্মীদের ভোজ"],
        "কিছু দরপত্রে দাম আর মানের পাশাপাশি সামাজিক মূল্যে নম্বর থাকে।"),
    mcq("What does an 'apprenticeship' requirement in a bridge contract achieve?", ["It trains young local people in construction skills while the project is built", "It replaces skilled engineers", "It lowers safety", "It delays the project on purpose"], 0,
        "Skills stay in the region after the bridge opens.",
        "সেতু-চুক্তিতে 'শিক্ষানবিশি'-র শর্ত কী অর্জন করে?", ["প্রকল্প তৈরির সময় স্থানীয় তরুণদের নির্মাণ-দক্ষতায় প্রশিক্ষণ দেয়", "দক্ষ প্রকৌশলীদের বদলি করে", "নিরাপত্তা কমায়", "ইচ্ছে করে প্রকল্পে দেরি করায়"],
        "সেতু খোলার পরেও দক্ষতা অঞ্চলে থেকে যায়।"),
)
