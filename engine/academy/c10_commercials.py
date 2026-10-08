"""Class 10 - Commercials (Bridge Engineer): exponential smoothing and seasonal forecasts, freight
emissions per tonne-km, cheapest routes through a network, total cost of ownership, market
sizing, bundles and series discounts, fleet sizing, fuel costs, logistics payback, contract
claims and dispute resolution, and sustainable, ethical supply chains for bridge projects."""
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


def smooth(f_old, actual, alpha, item_en, item_bn):
    r = _c(f_old + alpha * (actual - f_old))
    return _n(f"Last month's forecast for {item_en} was {f_old:,}; actual sales were {actual:,}. Using exponential smoothing with α = {alpha:g}, what is the new forecast?",
              f"গত মাসে {item_bn}-এর পূর্বাভাস ছিল {f_old:,}; আসল বিক্রি {actual:,}। α = {alpha:g} দিয়ে সূচকীয় মসৃণকরণে নতুন পূর্বাভাস কত?", r,
              f"New = old + α(actual - old) = {f_old:,} + {alpha:g} x ({actual:,} - {f_old:,}) = {r:,}.",
              f"নতুন = পুরোনো + α(আসল - পুরোনো) = {f_old:,} + {alpha:g} x ({actual:,} - {f_old:,}) = {r:,}।",
              (actual, _c((f_old + actual) / 2) if _c((f_old + actual) / 2) != r else r + 5, _c(f_old + alpha * actual)))


def seasonal(base, index, season_en, season_bn):
    r = _c(base * index)
    return _n(f"Average monthly cement demand is {base:,} bags. The seasonal index for {season_en} is {index:g}. What is the forecast for {season_en}?",
              f"সিমেন্টের গড় মাসিক চাহিদা {base:,} বস্তা। {season_bn}-এর মরসুমি সূচক {index:g}। {season_bn}-এর পূর্বাভাস কত?", r,
              f"Forecast = average x seasonal index = {base:,} x {index:g} = {r:,} bags.",
              f"পূর্বাভাস = গড় x মরসুমি সূচক = {base:,} x {index:g} = {r:,} বস্তা।",
              (base, _c(base / index), _c(base + index * 100)), " bags", " বস্তা")


def emissions(t, km, g_per_tkm, mode_en, mode_bn):
    r = _c(t * km * g_per_tkm / 1000)
    return _n(f"Moving {t} tonnes of steel {km} km by {mode_en} emits about {g_per_tkm} g of CO2 per tonne-km. What are the total emissions?",
              f"{mode_bn} {t} টন ইস্পাত {km} km নিতে টন-কিমিপ্রতি প্রায় {g_per_tkm} g CO2 বেরোয়। মোট নির্গমন কত?", r,
              f"{t} x {km} = {t * km:,} tonne-km; x {g_per_tkm} g = {t * km * g_per_tkm:,} g = {r:g} kg of CO2.",
              f"{t} x {km} = {t * km:,} টন-কিমি; x {g_per_tkm} g = {t * km * g_per_tkm:,} g = {r:g} kg CO2।",
              (_c(r * 10), _c(km * g_per_tkm / 1000), _c(r / t)), " kg", " kg")


def route(ab, bd, ac, cd):
    p1, p2 = ab + bd, ac + cd
    best_en, best_bn = ("A-B-D", "A-B-D") if p1 < p2 else ("A-C-D", "A-C-D")
    o = [f"{best_en} (Rs {min(p1, p2):,})", f"{'A-C-D' if best_en == 'A-B-D' else 'A-B-D'} (Rs {max(p1, p2):,})", f"{best_en} (Rs {abs(p1 - p2):,})", "Both cost the same"]
    o_bn = [f"{best_bn} ({min(p1, p2):,} টাকা)", f"{'A-C-D' if best_bn == 'A-B-D' else 'A-B-D'} ({max(p1, p2):,} টাকা)", f"{best_bn} ({abs(p1 - p2):,} টাকা)", "দুটোর খরচ সমান"]
    return mcq(f"Truck costs between depots: A-B Rs {ab:,}, B-D Rs {bd:,}, A-C Rs {ac:,}, C-D Rs {cd:,}. There is no direct A-D road. Which route from A to D is cheapest?",
               o, 0,
               f"A-B-D = {ab:,} + {bd:,} = {p1:,}; A-C-D = {ac:,} + {cd:,} = {p2:,}. Choose {best_en}.",
               f"ডিপোগুলোর মধ্যে ট্রাকের খরচ: A-B {ab:,} টাকা, B-D {bd:,} টাকা, A-C {ac:,} টাকা, C-D {cd:,} টাকা। A-D সরাসরি রাস্তা নেই। A থেকে D-তে কোন পথ সবচেয়ে সস্তা?",
               o_bn,
               f"A-B-D = {ab:,} + {bd:,} = {p1:,}; A-C-D = {ac:,} + {cd:,} = {p2:,}। {best_bn} বাছো।")


def tco(price, running, years, resale, what_en, what_bn):
    r = price + running * years - resale
    return _n(f"{what_en} costs Rs {price:,} lakh, Rs {running:,} lakh a year to run for {years} years, and sells for Rs {resale:,} lakh at the end. What is its total cost of ownership?",
              f"{what_bn}-এর দাম {price:,} লাখ টাকা, {years} বছর চালাতে বছরে {running:,} লাখ টাকা, আর শেষে {resale:,} লাখ টাকায় বেচা যায়। মালিকানার মোট খরচ কত?", r,
              f"TCO = price + running costs - resale = {price:,} + {running:,} x {years} - {resale:,} = Rs {r:,} lakh.",
              f"মোট খরচ = দাম + চালানোর খরচ - বিক্রয়মূল্য = {price:,} + {running:,} x {years} - {resale:,} = {r:,} লাখ টাকা।",
              (price, price + running * years, r + resale * 2), " lakh", " লাখ টাকা", "Rs ")


def market(households, pct, spend, item_en, item_bn):
    buyers = households * pct // 100
    r = _c(buyers * spend / 10_000_000)
    return _n(f"A district has {households:,} households. About {pct}% plan {item_en} this year, spending Rs {spend:,} each on materials. What is the market size?",
              f"একটা জেলায় {households:,} পরিবার। প্রায় {pct}% এ বছর {item_bn} পরিকল্পনা করছে, প্রত্যেকে উপাদানে {spend:,} টাকা খরচ করবে। বাজারের আকার কত?", r,
              f"{households:,} x {pct}% = {buyers:,} buyers; x Rs {spend:,} = Rs {buyers * spend:,} = Rs {r:g} crore.",
              f"{households:,} x {pct}% = {buyers:,} ক্রেতা; x {spend:,} টাকা = {buyers * spend:,} টাকা = {r:g} কোটি টাকা।",
              (_c(households * spend / 10_000_000), _c(r / 10), _c(r * 10)), " crore", " কোটি টাকা", "Rs ")


def series(listp, d1, d2):
    r = listp * (100 - d1) * (100 - d2) // 10000
    single = listp * (100 - d1 - d2) // 100
    return _n(f"A pump has a list price of Rs {listp:,}. A builder gets a {d1}% trade discount and then a {d2}% cash discount on the reduced price. What does the builder pay?",
              f"একটা পাম্পের তালিকা-দাম {listp:,} টাকা। একজন নির্মাতা {d1}% ব্যবসায়িক ছাড় আর তারপর কমা দামে {d2}% নগদ-ছাড় পান। নির্মাতা কত দেন?", r,
              f"{listp:,} x {(100 - d1) / 100:g} = {listp * (100 - d1) // 100:,}; x {(100 - d2) / 100:g} = Rs {r:,}. (Not the same as a single {d1 + d2}% off, which gives Rs {single:,}.)",
              f"{listp:,} x {(100 - d1) / 100:g} = {listp * (100 - d1) // 100:,}; x {(100 - d2) / 100:g} = {r:,} টাকা। (একবারে {d1 + d2}% ছাড়ে হতো {single:,} টাকা - এক নয়।)",
              (single, listp * d1 // 100, r + listp * d2 // 100), "", " টাকা", "Rs ")


def fleet(demand, cap, trips):
    r = -(-demand // (cap * trips))
    return _n(f"A site needs {demand:,} tonnes of aggregate a day. Each truck carries {cap} tonnes and can make {trips} trips a day. How many trucks are needed?",
              f"একটা নির্মাণস্থলে দিনে {demand:,} টন খোয়া লাগে। প্রতিটা ট্রাক {cap} টন বয় আর দিনে {trips}বার যেতে পারে। কতগুলো ট্রাক লাগবে?", r,
              f"One truck moves {cap} x {trips} = {cap * trips} tonnes a day; {demand:,} ÷ {cap * trips} = {demand / (cap * trips):.2f}, rounded UP to {r}.",
              f"একটা ট্রাক দিনে {cap} x {trips} = {cap * trips} টন নেয়; {demand:,} ÷ {cap * trips} = {demand / (cap * trips):.2f}, উপরে আসন্ন করে {r}।",
              (demand // (cap * trips) if demand // (cap * trips) != r else r + 2, demand // cap, r * trips), " trucks", "টি ট্রাক")


def fuel(km, kmpl, price):
    r = _c(km / kmpl * price)
    return _n(f"A truck travels {km:,} km on a round trip and does {kmpl:g} km per litre. Diesel costs Rs {price} a litre. What is the fuel cost?",
              f"একটা ট্রাক আসা-যাওয়ায় {km:,} km যায় আর লিটারে {kmpl:g} km চলে। ডিজেল লিটারে {price} টাকা। জ্বালানি-খরচ কত?", r,
              f"Litres = {km:,} ÷ {kmpl:g} = {_c(km / kmpl):g}; x Rs {price} = Rs {r:,}.",
              f"লিটার = {km:,} ÷ {kmpl:g} = {_c(km / kmpl):g}; x {price} টাকা = {r:,} টাকা।",
              (_c(km * price / 10), _c(km * kmpl), _c(r / 2)), "", " টাকা", "Rs ")


def payback(cost, saving, what_en, what_bn):
    r = _c(cost / saving)
    return _n(f"A firm spends Rs {cost:,} lakh on {what_en}, saving Rs {saving:,} lakh a year. What is the payback period?",
              f"একটা সংস্থা {what_bn}-এ {cost:,} লাখ টাকা খরচ করে, বছরে {saving:,} লাখ টাকা বাঁচে। খরচ উঠে আসার সময় কত?", r,
              f"{cost:,} ÷ {saving:,} = {r:g} years.",
              f"{cost:,} ÷ {saving:,} = {r:g} বছর।",
              (_c(saving / cost * 10), cost - saving, _c(r * 2)), " years", " বছর")


ITEMS = (
    smooth(500, 600, 0.2, "steel couplers", "ইস্পাতের কাপলার"), smooth(1200, 1000, 0.3, "cement bags", "সিমেন্টের বস্তা"),
    smooth(80, 120, 0.5, "scaffold hires", "ভারা-ভাড়া"), smooth(300, 330, 0.1, "bolt boxes", "বল্টুর বাক্স"),
    seasonal(10000, 1.3, "the dry season", "শুকনো মরসুম"), seasonal(10000, 0.6, "the monsoon", "বর্ষাকাল"),
    seasonal(8000, 1.15, "the festive season", "উৎসবের মরসুম"), seasonal(12000, 0.85, "early winter", "শীতের শুরু"),
    emissions(20, 500, 80, "road", "সড়কপথে"), emissions(20, 500, 25, "rail", "রেলপথে"),
    emissions(100, 300, 15, "inland waterway", "অভ্যন্তরীণ জলপথে"), emissions(40, 250, 60, "road", "সড়কপথে"),
    route(4000, 3000, 2500, 5000), route(6000, 2000, 3000, 4000), route(1500, 4500, 3500, 3000),
    tco(80, 10, 6, 20, "A diesel excavator", "একটা ডিজেল খননযন্ত্র"), tco(100, 6, 6, 30, "An electric excavator", "একটা বৈদ্যুতিক খননযন্ত্র"),
    tco(40, 5, 8, 8, "A concrete pump", "একটা কংক্রিট-পাম্প"),
    market(200000, 5, 150000, "a home extension", "বাড়ির সম্প্রসারণ"), market(50000, 10, 40000, "a new roof", "নতুন ছাদ"),
    market(120000, 3, 250000, "a new house", "নতুন বাড়ি"),
    series(100000, 20, 5), series(60000, 10, 2), series(250000, 15, 3),
    fleet(600, 20, 4), fleet(1300, 25, 5), fleet(400, 12, 3), fleet(1500, 30, 6),
    fuel(600, 4, 95), fuel(450, 5, 92), fuel(1200, 3.5, 90), fuel(300, 6, 95),
    payback(60, 15, "a GPS fleet-tracking system", "একটা জিপিএস বহর-নজরদারি ব্যবস্থা"), payback(200, 40, "a rail siding at the precast yard", "প্রিকাস্ট-উঠানে একটা রেল-সাইডিং"),
    payback(25, 10, "LED site lighting", "নির্মাণস্থলে এলইডি আলো"), payback(90, 12, "an automated rebar-bending machine", "একটা স্বয়ংক্রিয় রড-বাঁকানোর যন্ত্র"),
    smooth(2000, 2400, 0.25, "ready-mix loads", "রেডি-মিক্স বোঝাই"), smooth(150, 110, 0.4, "pallet deliveries", "প্যালেট-ডেলিভারি"),
    seasonal(6000, 1.45, "the pre-monsoon rush", "বর্ষার আগের ভিড়"), emissions(500, 150, 15, "inland waterway", "অভ্যন্তরীণ জলপথে"),
    emissions(30, 800, 25, "rail", "রেলপথে"), route(3500, 2500, 2000, 3500), tco(60, 8, 5, 15, "A tower crane", "একটা টাওয়ার-ক্রেন"),
    market(80000, 8, 120000, "a shop renovation", "দোকান-সংস্কার"), series(40000, 25, 4), fleet(720, 18, 4), fuel(800, 4.5, 94),
    mcq("What does the smoothing constant α control in exponential smoothing?", ["How strongly the forecast reacts to the latest actual figure", "The colour of the graph", "The number of products", "The tax rate"], 0,
        "A high α reacts fast to change; a low α smooths out random noise.",
        "সূচকীয় মসৃণকরণে মসৃণকরণ-ধ্রুবক α কী নিয়ন্ত্রণ করে?", ["সাম্প্রতিক আসল সংখ্যায় পূর্বাভাস কতটা জোরে সাড়া দেয়", "লেখচিত্রের রং", "পণ্যের সংখ্যা", "করের হার"],
        "বেশি α দ্রুত বদলে সাড়া দেয়; কম α এলোমেলো ওঠানামা মসৃণ করে।"),
    mcq("What does a seasonal index of 1.3 for the dry season mean?", ["Demand in that season is typically 30% above the average month", "Demand is 1.3% lower", "Demand never changes", "Prices rise 1.3 times"], 0,
        "Builders do much more concreting when it is dry.",
        "শুকনো মরসুমের মরসুমি সূচক 1.3 মানে কী?", ["সেই মরসুমে চাহিদা সাধারণত গড় মাসের চেয়ে 30% বেশি", "চাহিদা 1.3% কম", "চাহিদা কখনো বদলায় না", "দাম 1.3 গুণ বাড়ে"],
        "শুকনো সময়ে নির্মাতারা অনেক বেশি ঢালাই করেন।"),
    mcq("Why is shifting freight from road to rail one of the biggest ways to cut a bridge project's transport emissions?", ["Rail emits far less CO2 per tonne-km than trucks", "Trains are always faster", "Rail is always cheaper for every trip", "Trucks cannot carry steel"], 0,
        "Rail-to-site combined with short truck hops is often the greenest option.",
        "সেতু-প্রকল্পের পরিবহন-নির্গমন কমানোর সবচেয়ে বড় উপায়গুলোর একটা কেন সড়ক থেকে রেলে মাল সরানো?", ["টন-কিমিপ্রতি রেল ট্রাকের চেয়ে অনেক কম CO2 ছাড়ে", "ট্রেন সবসময় দ্রুত", "প্রতিটা যাত্রায় রেল সবসময় সস্তা", "ট্রাক ইস্পাত বইতে পারে না"],
        "রেলে নির্মাণস্থলের কাছে এনে ছোট ট্রাক-যাত্রা প্রায়ই সবচেয়ে সবুজ বিকল্প।"),
    mcq("What is 'Scope 3' in carbon accounting for a construction company?", ["Indirect emissions in its supply chain, such as making the steel and cement it buys", "Emissions from its own trucks only", "Emissions from its office lights only", "A type of telescope"], 0,
        "For builders, Scope 3 is usually by far the largest share.",
        "নির্মাণ-কোম্পানির কার্বন-হিসাবে 'স্কোপ 3' কী?", ["সরবরাহ-শৃঙ্খলের পরোক্ষ নির্গমন, যেমন কেনা ইস্পাত আর সিমেন্ট তৈরিতে", "শুধু নিজের ট্রাকের নির্গমন", "শুধু অফিসের আলোর নির্গমন", "এক রকম দূরবিন"],
        "নির্মাতাদের জন্য স্কোপ 3 সাধারণত সবচেয়ে বড় অংশ।"),
    mcq("What is 'total cost of ownership' (TCO)?", ["The full cost over an item's life: purchase, running, maintenance and disposal, minus resale", "The purchase price only", "The cost of insurance only", "The cost of one repair"], 0,
        "An electric machine may cost more to buy but less to own.",
        "'মালিকানার মোট খরচ' (টিসিও) কী?", ["জিনিসের জীবনভর পুরো খরচ: কেনা, চালানো, রক্ষণাবেক্ষণ আর নিষ্পত্তি, বিক্রয়মূল্য বাদে", "শুধু কেনার দাম", "শুধু বিমার খরচ", "একবার মেরামতের খরচ"],
        "বৈদ্যুতিক যন্ত্র কিনতে দামি, কিন্তু মালিকানায় সস্তা হতে পারে।"),
    mcq("What is the 'total addressable market' (TAM)?", ["The total sales possible if a product reached every potential customer", "The firm's current sales", "The number of competitors", "A market's address"], 0,
        "Firms then estimate the share they can realistically win.",
        "'মোট সম্ভাব্য বাজার' (ট্যাম) কী?", ["পণ্যটা প্রত্যেক সম্ভাব্য খদ্দেরের কাছে পৌঁছালে মোট যত বিক্রি সম্ভব", "সংস্থার বর্তমান বিক্রি", "প্রতিদ্বন্দ্বীর সংখ্যা", "বাজারের ঠিকানা"],
        "তারপর সংস্থা বাস্তবে কত ভাগ জিততে পারে তা আন্দাজ করে।"),
    mcq("Why is a 10% then 5% discount not the same as a single 15% discount?", ["The second discount applies to the already-reduced price, so the total is 14.5%", "It is exactly the same", "The second discount is added to the list price", "Discounts cannot be combined"], 0,
        "0.9 x 0.95 = 0.855 of the list price.",
        "আগে 10% তারপর 5% ছাড় একবারে 15% ছাড়ের সমান নয় কেন?", ["দ্বিতীয় ছাড় আগেই-কমা দামে খাটে, তাই মোট 14.5%", "হুবহু একই", "দ্বিতীয় ছাড় তালিকা-দামে যোগ হয়", "ছাড় মেশানো যায় না"],
        "তালিকা-দামের 0.9 x 0.95 = 0.855।"),
    mcq("What is 'bundle pricing'?", ["Selling several products together for less than buying them separately", "Charging extra for packaging", "Tying products with string", "Selling only one item"], 0,
        "A scaffold-hire bundle might include towers, boards and delivery.",
        "'গুচ্ছ-মূল্য' কী?", ["আলাদা কেনার চেয়ে কম দামে কয়েকটা পণ্য একসঙ্গে বেচা", "প্যাকেটের জন্য বাড়তি দাম", "দড়ি দিয়ে পণ্য বাঁধা", "শুধু একটা জিনিস বেচা"],
        "ভারা-ভাড়ার গুচ্ছে মিনার, তক্তা আর ডেলিভারি থাকতে পারে।"),
    mcq("Why must the number of trucks always be rounded UP?", ["A part of a truck cannot run - rounding down would leave material undelivered", "Trucks are cheap", "Rounding up saves fuel", "It does not matter"], 0,
        "The same applies to cranes, crews and pallets.",
        "ট্রাকের সংখ্যা সবসময় উপরে আসন্ন করতে হয় কেন?", ["ট্রাকের একটা অংশ চলতে পারে না - নিচে আসন্ন করলে মাল পৌঁছানো বাকি থাকবে", "ট্রাক সস্তা", "উপরে আসন্ন করলে জ্বালানি বাঁচে", "কিছু যায় আসে না"],
        "ক্রেন, দল আর প্যালেটের ক্ষেত্রেও একই।"),
    mcq("What is 'fleet utilisation' and why does it matter?", ["The share of time trucks are working; idle trucks still cost money", "The number of trucks owned", "The truck colour", "Fuel economy only"], 0,
        "Good scheduling raises utilisation and cuts cost per tonne.",
        "'বহর-ব্যবহার' কী আর কেন জরুরি?", ["ট্রাক কত সময় কাজ করছে তার অংশ; অলস ট্রাকেও খরচ লাগে", "মালিকানার ট্রাকের সংখ্যা", "ট্রাকের রং", "শুধু জ্বালানি-দক্ষতা"],
        "ভালো সময়সূচি ব্যবহার বাড়ায় আর টনপ্রতি খরচ কমায়।"),
    mcq("What is 'telematics' in fleet management?", ["Devices that send data on vehicle location, speed, fuel use and driver behaviour", "Television in trucks", "A type of road sign", "Truck painting"], 0,
        "It helps reduce speeding, idling and fuel theft.",
        "বহর-ব্যবস্থাপনায় 'টেলিম্যাটিক্স' কী?", ["যে যন্ত্র গাড়ির অবস্থান, গতি, জ্বালানি-ব্যবহার আর চালকের আচরণের তথ্য পাঠায়", "ট্রাকে টেলিভিশন", "এক রকম রাস্তার চিহ্ন", "ট্রাক রং করা"],
        "গতি-লঙ্ঘন, অলস দাঁড়ানো আর জ্বালানি-চুরি কমাতে সাহায্য করে।"),
    mcq("Why do logistics managers plan 'routes' with the help of software for many deliveries?", ["The number of possible routes grows very fast, so computers find good ones much quicker", "Drivers cannot read maps", "Software makes roads shorter", "It is required by law"], 0,
        "Even 10 stops have millions of possible orders.",
        "অনেক ডেলিভারির জন্য পরিবহন-ম্যানেজাররা সফটওয়্যারের সাহায্যে 'পথ' পরিকল্পনা করেন কেন?", ["সম্ভাব্য পথের সংখ্যা খুব দ্রুত বাড়ে, তাই কম্পিউটার অনেক দ্রুত ভালো পথ খোঁজে", "চালকরা মানচিত্র পড়তে পারেন না", "সফটওয়্যার রাস্তা ছোট করে", "আইনে বাধ্যতামূলক"],
        "মাত্র 10টা থামাতেও লক্ষ লক্ষ সম্ভাব্য ক্রম।"),
    mcq("What is a 'claim' in a construction contract?", ["A formal request by the contractor for extra time or money, usually because of events beyond its control", "A complaint about lunch", "A tax refund", "A warranty card"], 0,
        "Good records like site diaries and photos support a fair claim.",
        "নির্মাণ-চুক্তিতে 'দাবি' কী?", ["সাধারণত নিয়ন্ত্রণের বাইরের ঘটনার জন্য ঠিকাদারের বাড়তি সময় বা টাকার আনুষ্ঠানিক অনুরোধ", "দুপুরের খাবার নিয়ে অভিযোগ", "করের ফেরত", "ওয়ারেন্টি-কার্ড"],
        "নির্মাণস্থলের ডায়েরি আর ছবির মতো ভালো নথি ন্যায্য দাবির সমর্থন করে।"),
    mcq("What is 'arbitration' in a contract dispute?", ["A private process where an independent arbitrator hears both sides and makes a binding decision", "A street protest", "Going to the police", "Ignoring the dispute"], 0,
        "It is usually faster than going to court.",
        "চুক্তি-বিরোধে 'সালিশ' কী?", ["ব্যক্তিগত প্রক্রিয়া, যেখানে একজন স্বাধীন সালিশকারী দুপক্ষের কথা শুনে বাধ্যতামূলক সিদ্ধান্ত দেন", "রাস্তার প্রতিবাদ", "পুলিশের কাছে যাওয়া", "বিরোধ উপেক্ষা"],
        "সাধারণত আদালতে যাওয়ার চেয়ে দ্রুত।"),
    mcq("What is 'mediation'?", ["A neutral person helps both sides talk and reach their own agreement", "A judge imposes a decision", "A type of meditation", "A bank loan"], 0,
        "It keeps business relationships intact more often than court.",
        "'মধ্যস্থতা' কী?", ["একজন নিরপেক্ষ মানুষ দুপক্ষকে কথা বলে নিজেদের সমঝোতায় পৌঁছাতে সাহায্য করেন", "বিচারক সিদ্ধান্ত চাপান", "এক রকম ধ্যান", "ব্যাংক-ঋণ"],
        "আদালতের চেয়ে বেশিবার ব্যবসায়িক সম্পর্ক অটুট রাখে।"),
    mcq("What is a 'dispute resolution board' on a big bridge project?", ["A standing panel of experts who visit regularly and help settle disagreements early", "A notice board for complaints", "A court room", "A board game"], 0,
        "Settling problems early stops them growing into costly disputes.",
        "বড় সেতু-প্রকল্পে 'বিরোধ-নিষ্পত্তি পর্ষদ' কী?", ["বিশেষজ্ঞদের স্থায়ী প্যানেল, যাঁরা নিয়মিত আসেন আর মতভেদ আগেভাগে মেটাতে সাহায্য করেন", "অভিযোগের নোটিস-বোর্ড", "আদালত-কক্ষ", "বোর্ড-খেলা"],
        "সমস্যা আগেভাগে মেটালে তা দামি বিরোধে বাড়ে না।"),
    mcq("What is 'force majeure' used to cover in a contract?", ["Extraordinary events beyond anyone's control, like major floods or war, that may excuse delays", "Normal rain", "A late delivery from carelessness", "A contractor's mistake"], 0,
        "It usually gives extra time but not always extra money.",
        "চুক্তিতে 'দৈব-দুর্বিপাক' (ফোর্স মেজিওর) কী ঢাকতে ব্যবহার হয়?", ["কারও নিয়ন্ত্রণের বাইরের অসাধারণ ঘটনা, যেমন বড় বন্যা বা যুদ্ধ, যা দেরি মাফ করতে পারে", "সাধারণ বৃষ্টি", "অসাবধানতায় দেরিতে ডেলিভারি", "ঠিকাদারের ভুল"],
        "সাধারণত বাড়তি সময় দেয়, তবে সবসময় বাড়তি টাকা নয়।"),
    mcq("What is a 'site diary' and why is it valuable in a dispute?", ["A daily record of weather, labour, deliveries and events, made at the time", "A worker's personal journal", "A holiday calendar", "A list of phone numbers"], 0,
        "Records made at the time are strong evidence.",
        "'নির্মাণস্থলের ডায়েরি' কী আর বিরোধে কেন মূল্যবান?", ["আবহাওয়া, শ্রমিক, ডেলিভারি আর ঘটনার দৈনিক নথি, সেই সময়েই লেখা", "কর্মীর ব্যক্তিগত ডায়েরি", "ছুটির ক্যালেন্ডার", "ফোন-নম্বরের তালিকা"],
        "সেই সময়ে লেখা নথি জোরালো প্রমাণ।"),
    mcq("What is a 'subcontractor'?", ["A firm hired by the main contractor to do part of the work, such as piling or painting", "The client", "A government inspector", "A bank"], 0,
        "The main contractor remains responsible to the client for the whole job.",
        "'উপ-ঠিকাদার' কী?", ["মূল ঠিকাদারের ভাড়া করা সংস্থা, যা কাজের একটা অংশ করে, যেমন পাইলিং বা রং", "গ্রাহক", "সরকারি পরিদর্শক", "ব্যাংক"],
        "পুরো কাজের জন্য গ্রাহকের কাছে মূল ঠিকাদারই দায়ী থাকেন।"),
    mcq("Why should a main contractor pay subcontractors promptly?", ["Late payment can bankrupt small firms, stop work and damage trust", "Subcontractors prefer waiting", "It is illegal to pay on time", "It saves the main contractor nothing"], 0,
        "Fair payment practices are increasingly written into public contracts.",
        "মূল ঠিকাদারের উপ-ঠিকাদারদের তাড়াতাড়ি টাকা দেওয়া উচিত কেন?", ["দেরিতে পেমেন্ট ছোট সংস্থাকে দেউলিয়া করতে, কাজ থামাতে আর আস্থা নষ্ট করতে পারে", "উপ-ঠিকাদাররা অপেক্ষা পছন্দ করেন", "সময়ে দেওয়া বেআইনি", "মূল ঠিকাদারের কিছু বাঁচে না"],
        "ন্যায্য পেমেন্টের নিয়ম ক্রমশ সরকারি চুক্তিতে লেখা হচ্ছে।"),
    mcq("What is a 'pay-when-paid' clause, and why is it often restricted?", ["The main contractor pays subcontractors only after the client pays it - unfair because the risk is passed down", "Paying everyone in advance", "Paying only in cash", "A discount for early payment"], 0,
        "Many countries limit such clauses to protect small firms.",
        "'পেলে-তবে-দেব' ধারা কী, আর কেন প্রায়ই সীমিত করা হয়?", ["গ্রাহক মূল ঠিকাদারকে টাকা দেওয়ার পরেই তিনি উপ-ঠিকাদারদের দেন - অন্যায্য, কারণ ঝুঁকি নিচে চাপানো হয়", "সবাইকে আগাম দেওয়া", "শুধু নগদে দেওয়া", "আগে দিলে ছাড়"],
        "ছোট সংস্থাদের রক্ষায় অনেক দেশ এমন ধারা সীমিত করে।"),
    mcq("What is 'value engineering' on a bridge project?", ["Finding ways to deliver the same function and quality at lower whole-life cost", "Making the bridge as cheap as possible regardless of quality", "Adding expensive decoration", "Increasing the price"], 0,
        "A different foundation design might save months and money without losing safety.",
        "সেতু-প্রকল্পে 'মূল্য-প্রকৌশল' কী?", ["একই কাজ আর মান কম পূর্ণ-জীবন খরচে দেওয়ার উপায় খোঁজা", "মান যা-ই হোক সেতু যত সস্তা সম্ভব করা", "দামি সাজসজ্জা যোগ করা", "দাম বাড়ানো"],
        "আলাদা ভিতের নকশা নিরাপত্তা না হারিয়ে কয়েক মাস আর টাকা বাঁচাতে পারে।"),
    mcq("What is 'modern slavery' risk in construction supply chains?", ["Forced or bonded labour hidden in suppliers, such as in brick kilns or quarries", "Using old machines", "Paying fair wages", "Working short hours"], 0,
        "Responsible firms audit suppliers and support workers to speak up.",
        "নির্মাণের সরবরাহ-শৃঙ্খলে 'আধুনিক দাসত্বের' ঝুঁকি কী?", ["সরবরাহকারীদের মধ্যে লুকোনো জোর করে বা ঋণ-বন্ধকে কাজ, যেমন ইটভাটা বা খাদানে", "পুরোনো যন্ত্র ব্যবহার", "ন্যায্য মজুরি দেওয়া", "কম ঘণ্টা কাজ"],
        "দায়িত্বশীল সংস্থা সরবরাহকারীদের নিরীক্ষা করে আর কর্মীদের মুখ খুলতে সমর্থন করে।"),
    mcq("What is a 'supplier code of conduct'?", ["Rules a buyer sets for suppliers on safety, labour rights, environment and honesty", "A secret password", "A price list", "A delivery timetable"], 0,
        "Breaking it can lead to losing the contract.",
        "'সরবরাহকারী আচরণবিধি' কী?", ["নিরাপত্তা, শ্রম-অধিকার, পরিবেশ আর সততা নিয়ে ক্রেতার ঠিক করা নিয়ম", "গোপন পাসওয়ার্ড", "দামের তালিকা", "ডেলিভারির সময়সূচি"],
        "ভাঙলে চুক্তি হারাতে পারে।"),
    mcq("What does 'circular economy' mean for bridge materials?", ["Designing so materials can be reused or recycled instead of thrown away", "Building round bridges", "Buying new materials every year", "Burning old materials"], 0,
        "Steel girders can be reused; crushed concrete can become new aggregate.",
        "সেতুর উপাদানের ক্ষেত্রে 'বৃত্তাকার অর্থনীতি' মানে কী?", ["এমনভাবে নকশা যাতে উপাদান ফেলে না দিয়ে আবার ব্যবহার বা পুনর্ব্যবহার করা যায়", "গোল সেতু বানানো", "প্রতি বছর নতুন উপাদান কেনা", "পুরোনো উপাদান পোড়ানো"],
        "ইস্পাতের গার্ডার আবার ব্যবহার করা যায়; গুঁড়ো কংক্রিট নতুন খোয়া হতে পারে।"),
    mcq("What is 'reverse auction' risk if used carelessly for safety-critical bridge parts?", ["Suppliers may cut corners on quality to win on price", "Prices always rise", "It always improves safety", "No suppliers take part"], 0,
        "Quality checks must be strict before price competition starts.",
        "নিরাপত্তা-জরুরি সেতুর অংশে অসাবধানে উল্টো নিলাম ব্যবহারের ঝুঁকি কী?", ["দামে জিততে সরবরাহকারীরা মানে কাটছাঁট করতে পারেন", "দাম সবসময় বাড়ে", "সবসময় নিরাপত্তা বাড়ায়", "কোনো সরবরাহকারী অংশ নেয় না"],
        "দামের প্রতিযোগিতার আগে মানের যাচাই কড়া হতে হবে।"),
    mcq("What is a 'key performance indicator' (KPI) for a logistics team?", ["A measurable target, such as on-time deliveries or cost per tonne", "A key to the warehouse", "A truck's number plate", "A secret plan"], 0,
        "Good KPIs focus attention on what matters most.",
        "পরিবহন-দলের জন্য 'প্রধান কর্মদক্ষতা সূচক' (কেপিআই) কী?", ["মাপা যায় এমন লক্ষ্য, যেমন সময়মতো ডেলিভারি বা টনপ্রতি খরচ", "গুদামের চাবি", "ট্রাকের নম্বর-প্লেট", "গোপন পরিকল্পনা"],
        "ভালো কেপিআই সবচেয়ে জরুরি বিষয়ে মনোযোগ রাখে।"),
    mcq("Why can a single KPI, such as 'lowest cost', lead to bad decisions?", ["Teams may sacrifice safety, quality or reliability to hit one number", "One KPI is always enough", "Costs never matter", "KPIs are illegal"], 0,
        "A balanced scorecard mixes cost, quality, safety and time.",
        "'সবচেয়ে কম খরচ'-এর মতো একটা কেপিআই কেন খারাপ সিদ্ধান্তে নিতে পারে?", ["একটা সংখ্যা ছুঁতে দল নিরাপত্তা, মান বা ভরসা ত্যাগ করতে পারে", "একটা কেপিআই সবসময় যথেষ্ট", "খরচ কখনো গুরুত্বপূর্ণ নয়", "কেপিআই বেআইনি"],
        "ভারসাম্যপূর্ণ মূল্যায়নে খরচ, মান, নিরাপত্তা আর সময় মেশানো থাকে।"),
    mcq("What is 'demand planning' for a ready-mix concrete plant?", ["Matching production and trucks to the pours customers have booked", "Making concrete at random", "Selling only on Sundays", "Stopping production in summer"], 0,
        "Concrete must be placed within a couple of hours, so timing is critical.",
        "রেডি-মিক্স কংক্রিট-কারখানার 'চাহিদা-পরিকল্পনা' কী?", ["খদ্দেরদের বুক-করা ঢালাইয়ের সঙ্গে উৎপাদন আর ট্রাক মেলানো", "এলোমেলো কংক্রিট বানানো", "শুধু রবিবারে বেচা", "গ্রীষ্মে উৎপাদন বন্ধ"],
        "কংক্রিট কয়েক ঘণ্টার মধ্যে বসাতে হয়, তাই সময় খুব জরুরি।"),
    mcq("Why is ready-mix concrete a 'perishable' product for logistics?", ["It starts to set within hours, so it must be delivered and placed quickly", "It melts in the sun", "It is eaten by insects", "It has an expiry date of years"], 0,
        "Retarders can extend the time a little for long journeys.",
        "পরিবহনের দিক থেকে রেডি-মিক্স কংক্রিট 'পচনশীল' পণ্য কেন?", ["কয়েক ঘণ্টার মধ্যে জমতে শুরু করে, তাই দ্রুত পৌঁছে বসাতে হয়", "রোদে গলে", "পোকা খায়", "মেয়াদ কয়েক বছর"],
        "লম্বা যাত্রায় মন্দক একটু সময় বাড়াতে পারে।"),
    mcq("What is a 'transit mixer'?", ["A truck with a rotating drum that keeps concrete mixed on the way to site", "A bus for workers", "A type of crane", "A traffic light"], 0,
        "The drum turns slowly while driving to stop the concrete separating.",
        "'ট্রানজিট মিক্সার' কী?", ["ঘোরা ড্রামওয়ালা ট্রাক, যা নির্মাণস্থলে যাওয়ার পথে কংক্রিট মিশিয়ে রাখে", "কর্মীদের বাস", "এক রকম ক্রেন", "ট্রাফিক-বাতি"],
        "যাওয়ার সময় ড্রাম ধীরে ঘোরে, যাতে কংক্রিট আলাদা না হয়।"),
    mcq("What is 'cold chain' style planning needed for in bridge logistics?", ["Time- and temperature-sensitive materials like concrete, some adhesives and epoxy resins", "Only frozen food for the canteen", "Steel girders", "Sand"], 0,
        "Storing resins too hot or too cold can ruin them.",
        "সেতুর পরিবহনে 'শীতল-শৃঙ্খল' ধাঁচের পরিকল্পনা কীসের জন্য লাগে?", ["সময় আর তাপমাত্রা-সংবেদনশীল উপাদান, যেমন কংক্রিট, কিছু আঠা আর ইপক্সি রজন", "শুধু ক্যান্টিনের জমানো খাবার", "ইস্পাতের গার্ডার", "বালি"],
        "রজন খুব গরমে বা ঠান্ডায় রাখলে নষ্ট হতে পারে।"),
    mcq("What is an 'abnormal load' permit for moving a huge bridge girder by road?", ["Official permission with a set route and times because the load exceeds normal size or weight limits", "A permit to drive fast", "A parking ticket", "A toll exemption only"], 0,
        "Police escorts and route checks for low bridges and weak culverts are often needed.",
        "বিশাল সেতু-গার্ডার সড়কপথে নিতে 'অস্বাভাবিক বোঝা' অনুমতিপত্র কী?", ["বোঝা স্বাভাবিক মাপ বা ওজনের সীমা ছাড়ায় বলে নির্দিষ্ট পথ আর সময়সহ সরকারি অনুমতি", "দ্রুত চালানোর অনুমতি", "পার্কিংয়ের টিকিট", "শুধু টোল-ছাড়"],
        "প্রায়ই পুলিশ-পাহারা আর নিচু সেতু ও দুর্বল কালভার্টের পথ-যাচাই লাগে।"),
    mcq("Why are very long girders sometimes delivered at night?", ["Roads are quieter, so the slow, wide load causes less disruption and risk", "Girders shrink at night", "Night tolls are higher", "Drivers see better at night"], 0,
        "Careful planning avoids blocking hospitals and schools at busy times.",
        "খুব লম্বা গার্ডার কখনো রাতে পৌঁছানো হয় কেন?", ["রাস্তা ফাঁকা, তাই ধীর, চওড়া বোঝা কম ব্যাঘাত আর ঝুঁকি ঘটায়", "রাতে গার্ডার ছোট হয়", "রাতে টোল বেশি", "রাতে চালকরা ভালো দেখেন"],
        "যত্নশীল পরিকল্পনা ব্যস্ত সময়ে হাসপাতাল আর স্কুলের পথ আটকানো এড়ায়।"),
    mcq("What does 'incremental launching' of a bridge deck save in logistics?", ["Deck segments are cast behind the abutment and pushed out, so no huge cranes or river access are needed", "It saves paint", "It saves the bridge's name", "Nothing"], 0,
        "It suits long viaducts over valleys or rivers.",
        "সেতুর পাটাতনের 'ধাপে ধাপে ঠেলে বসানো' পরিবহনে কী বাঁচায়?", ["প্রান্ত-ঠেকনার পিছনে খণ্ড ঢালাই করে সামনে ঠেলা হয়, তাই বিশাল ক্রেন বা নদীতে পৌঁছানো লাগে না", "রং বাঁচায়", "সেতুর নাম বাঁচায়", "কিছুই না"],
        "উপত্যকা বা নদীর উপর লম্বা উড়ালপথে মানানসই।"),
    mcq("What is 'prefabrication' and why does it suit busy city bridges?", ["Making parts in a factory and assembling them quickly on site, reducing road closures", "Building everything on site by hand", "Painting before building", "Using no materials"], 0,
        "Factory quality is also easier to control.",
        "'আগাম-নির্মাণ' কী আর ব্যস্ত শহুরে সেতুতে কেন মানানসই?", ["কারখানায় অংশ বানিয়ে নির্মাণস্থলে দ্রুত জোড়া, রাস্তা কম বন্ধ থাকে", "সব হাতে নির্মাণস্থলে বানানো", "বানানোর আগে রং করা", "কোনো উপাদান না ব্যবহার"],
        "কারখানার মান নিয়ন্ত্রণ করাও সহজ।"),
    mcq("What is a 'logistics hub' near a big bridge project?", ["A staging area where materials are received, checked, stored and sent to site just in time", "The bridge's centre", "A wheel hub", "A shopping mall"], 0,
        "It keeps a cramped site clear and deliveries flowing.",
        "বড় সেতু-প্রকল্পের কাছে 'পরিবহন-হাব' কী?", ["মঞ্চায়নের জায়গা, যেখানে মাল এসে যাচাই, মজুত আর ঠিক সময়ে নির্মাণস্থলে পাঠানো হয়", "সেতুর কেন্দ্র", "চাকার হাব", "শপিং-মল"],
        "ঘিঞ্জি নির্মাণস্থল ফাঁকা আর ডেলিভারি চালু রাখে।"),
    mcq("What is 'consolidation' of deliveries?", ["Combining several part-loads into fewer, fuller trucks", "Making concrete solid", "Cancelling orders", "Splitting a load into many trucks"], 0,
        "Fewer trucks means less traffic, cost and emissions.",
        "ডেলিভারির 'একত্রীকরণ' কী?", ["কয়েকটা আংশিক বোঝা মিলিয়ে কম, বেশি ভরা ট্রাক", "কংক্রিট শক্ত করা", "অর্ডার বাতিল", "এক বোঝা অনেক ট্রাকে ভাগ"],
        "কম ট্রাক মানে কম যানজট, খরচ আর নির্গমন।"),
    mcq("What is an 'inventory audit' (stock-take) for?", ["Checking that physical stock matches the records, finding loss, theft or errors", "Ordering new stock only", "Painting the warehouse", "Paying suppliers"], 0,
        "Cycle counts check a few items every day instead of everything at once.",
        "'মজুত-নিরীক্ষা' (মাল-গণনা) কীসের জন্য?", ["আসল মজুত নথির সঙ্গে মেলে কিনা যাচাই, হারানো, চুরি বা ভুল খোঁজা", "শুধু নতুন মজুত অর্ডার", "গুদাম রং করা", "সরবরাহকারীকে টাকা দেওয়া"],
        "চক্র-গণনায় একসঙ্গে সব না গুনে রোজ কয়েকটা জিনিস যাচাই হয়।"),
    mcq("What does 'shrinkage' mean in inventory?", ["Stock lost through theft, damage or errors", "Steel shrinking in cold", "Smaller boxes", "A sales discount"], 0,
        "Secure storage and good records reduce it.",
        "মজুতে 'ক্ষয়' (শ্রিংকেজ) মানে কী?", ["চুরি, ক্ষতি বা ভুলে হারানো মজুত", "ঠান্ডায় ইস্পাত ছোট হওয়া", "ছোট বাক্স", "বিক্রির ছাড়"],
        "নিরাপদ মজুত আর ভালো নথি এটা কমায়।"),
    mcq("What is 'cyber security' risk for a logistics company?", ["Hackers could steal data, divert payments or shut down tracking and booking systems", "Trucks rusting", "Rain on the warehouse", "Drivers getting lost"], 0,
        "Strong passwords, updates and staff training are basic defences.",
        "একটা পরিবহন-সংস্থার 'সাইবার-নিরাপত্তা' ঝুঁকি কী?", ["হ্যাকাররা তথ্য চুরি, পেমেন্ট ঘুরিয়ে দেওয়া বা নজরদারি আর বুকিং-ব্যবস্থা বন্ধ করতে পারে", "ট্রাকে মরচে", "গুদামে বৃষ্টি", "চালকদের পথ হারানো"],
        "শক্ত পাসওয়ার্ড, হালনাগাদ আর কর্মী-প্রশিক্ষণ মৌলিক প্রতিরক্ষা।"),
    mcq("A supplier emails new bank details asking for the next payment there. What should the accounts team do?", ["Phone the supplier on a known number to confirm before paying", "Pay immediately", "Reply to the email to check", "Ignore all supplier emails"], 0,
        "Fake 'change of bank details' emails are a common fraud.",
        "একজন সরবরাহকারী ইমেলে নতুন ব্যাংক-তথ্য দিয়ে পরের পেমেন্ট সেখানে চাইলেন। হিসাব-দলের কী করা উচিত?", ["টাকা দেওয়ার আগে জানা নম্বরে সরবরাহকারীকে ফোন করে নিশ্চিত হওয়া", "তখনই টাকা দেওয়া", "যাচাইয়ে সেই ইমেলেই উত্তর দেওয়া", "সব সরবরাহকারীর ইমেল উপেক্ষা"],
        "ভুয়ো 'ব্যাংক-তথ্য বদল' ইমেল এক সাধারণ প্রতারণা।"),
    mcq("What is 'business continuity planning' for a bridge contractor?", ["Preparing to keep working through disruptions like floods, IT failures or supplier collapse", "Planning holidays", "Planning the bridge's paint colour", "Closing the business"], 0,
        "Backup suppliers, data backups and alternative routes are typical measures.",
        "একজন সেতু-ঠিকাদারের 'ব্যবসা-ধারাবাহিকতা পরিকল্পনা' কী?", ["বন্যা, আইটি-বিপর্যয় বা সরবরাহকারীর পতনের মতো ব্যাঘাতেও কাজ চালিয়ে যাওয়ার প্রস্তুতি", "ছুটির পরিকল্পনা", "সেতুর রঙের পরিকল্পনা", "ব্যবসা বন্ধ"],
        "বিকল্প সরবরাহকারী, তথ্যের ব্যাকআপ আর বিকল্প পথ সাধারণ ব্যবস্থা।"),
    mcq("What does 'GeM' (Government e-Marketplace) do in India?", ["Lets government departments buy goods and services online from registered sellers transparently", "Sells gemstones", "Builds bridges", "Collects tolls"], 0,
        "Small firms can register and compete for government orders.",
        "ভারতে 'জেম' (সরকারি ই-বাজার) কী করে?", ["সরকারি দপ্তরকে নিবন্ধিত বিক্রেতাদের কাছ থেকে স্বচ্ছভাবে অনলাইনে পণ্য-পরিষেবা কিনতে দেয়", "রত্ন বেচে", "সেতু বানায়", "টোল তোলে"],
        "ছোট সংস্থা নিবন্ধন করে সরকারি অর্ডারের জন্য প্রতিযোগিতা করতে পারে।"),
    mcq("What is an 'MSME' and why do public tenders sometimes give them preference?", ["A micro, small or medium enterprise; preference helps small local firms grow and create jobs", "A large multinational", "A government ministry", "A type of cement"], 0,
        "Many bridge subcontractors are MSMEs.",
        "'এমএসএমই' কী আর সরকারি দরপত্র কখনো তাদের অগ্রাধিকার দেয় কেন?", ["অতি-ক্ষুদ্র, ক্ষুদ্র বা মাঝারি উদ্যোগ; অগ্রাধিকার ছোট স্থানীয় সংস্থাকে বাড়তে আর কাজ তৈরি করতে সাহায্য করে", "বড় বহুজাতিক", "একটা সরকারি মন্ত্রক", "এক রকম সিমেন্ট"],
        "অনেক সেতু-উপঠিকাদার এমএসএমই।"),
    mcq("Why do engineers and buyers keep good relationships with quarry owners near a bridge project?", ["Reliable local aggregate supply avoids long hauls, delays and price spikes", "Quarries give free gifts", "To avoid paying for stone", "It does not matter"], 0,
        "Local sourcing also cuts transport emissions.",
        "প্রকৌশলী আর ক্রেতারা সেতু-প্রকল্পের কাছের খাদান-মালিকদের সঙ্গে ভালো সম্পর্ক রাখেন কেন?", ["ভরসার স্থানীয় খোয়া-জোগান লম্বা পরিবহন, দেরি আর দামের লাফ এড়ায়", "খাদান বিনামূল্যে উপহার দেয়", "পাথরের দাম না দিতে", "কিছু যায় আসে না"],
        "স্থানীয় সংগ্রহ পরিবহন-নির্গমনও কমায়।"),
    mcq("What is 'lead time variability' and why does it matter?", ["How much delivery times vary; the more they vary, the more safety stock is needed", "The colour of lead", "The speed of trucks", "A fixed delivery date"], 0,
        "Reliable suppliers allow lower stock and less cash tied up.",
        "'সরবরাহ-সময়ের পরিবর্তনশীলতা' কী আর কেন জরুরি?", ["ডেলিভারির সময় কতটা ওঠানামা করে; যত বেশি ওঠানামা, তত বেশি নিরাপত্তা-মজুত লাগে", "সিসার রং", "ট্রাকের গতি", "নির্দিষ্ট ডেলিভারির তারিখ"],
        "ভরসার সরবরাহকারী কম মজুত আর কম আটকে-থাকা নগদে চলতে দেয়।"),
    mcq("A supplier is 10% cheaper but delivers late 30% of the time; another is on time 98% of the time. For a bridge with costly delays, which is usually better?", ["The reliable supplier - delay costs can far exceed the price saving", "The cheaper supplier always", "Neither", "It cannot be judged"], 0,
        "Total cost includes the cost of disruption, not just the invoice.",
        "একজন সরবরাহকারী 10% সস্তা কিন্তু 30% সময় দেরিতে দেন; আরেকজন 98% সময় ঠিক সময়ে দেন। দামি দেরির সেতুর জন্য সাধারণত কে ভালো?", ["ভরসার সরবরাহকারী - দেরির খরচ দামের সাশ্রয়ের চেয়ে অনেক বেশি হতে পারে", "সবসময় সস্তাজন", "কেউই না", "বিচার করা যায় না"],
        "মোট খরচে শুধু চালান নয়, ব্যাঘাতের খরচও ধরা থাকে।"),
    mcq("What does RFID tagging do for precast bridge segments?", ["Radio tags let each segment be identified and tracked automatically from factory to its exact place in the bridge", "It paints the segments", "It makes them lighter", "It replaces the steel inside"], 0,
        "Scanning confirms the right segment goes in the right position.",
        "প্রিকাস্ট সেতু-খণ্ডে আরএফআইডি ট্যাগ কী করে?", ["রেডিও-ট্যাগ প্রতিটা খণ্ডকে কারখানা থেকে সেতুর ঠিক জায়গা পর্যন্ত নিজে থেকে চিনতে আর অনুসরণ করতে দেয়", "খণ্ডে রং করে", "হালকা করে", "ভেতরের ইস্পাতের বদলি"],
        "স্ক্যান করে নিশ্চিত হওয়া যায় ঠিক খণ্ড ঠিক জায়গায় যাচ্ছে।"),
    mcq("What is BIM (building information modelling) used for on bridge projects?", ["A shared 3D digital model holding design, quantities, schedule and cost information", "A type of crane", "A bank loan", "A road sign"], 0,
        "Clashes between parts can be found on screen before building starts.",
        "সেতু-প্রকল্পে বিআইএম (বিল্ডিং ইনফরমেশন মডেলিং) কীসের জন্য ব্যবহার হয়?", ["নকশা, পরিমাণ, সময়সূচি আর খরচের তথ্যসহ একটা ভাগ-করা ত্রিমাত্রিক ডিজিটাল মডেল", "এক রকম ক্রেন", "ব্যাংক-ঋণ", "রাস্তার চিহ্ন"],
        "নির্মাণ শুরুর আগেই পর্দায় অংশগুলোর সংঘাত ধরা যায়।"),
    mcq("What is a 'digital twin' of a bridge?", ["A live computer model fed by sensors on the real bridge, used to predict maintenance needs", "A second identical bridge", "A photo album", "A twin-span bridge"], 0,
        "It helps owners fix problems before they become dangerous or costly.",
        "সেতুর 'ডিজিটাল যমজ' কী?", ["আসল সেতুর সেন্সর থেকে তথ্য পাওয়া জীবন্ত কম্পিউটার-মডেল, রক্ষণাবেক্ষণের প্রয়োজন আগাম বুঝতে ব্যবহৃত", "হুবহু আরেকটা সেতু", "ছবির অ্যালবাম", "জোড়া-স্প্যানের সেতু"],
        "মালিকদের বিপজ্জনক বা দামি হওয়ার আগে সমস্যা সারাতে সাহায্য করে।"),
    mcq("How do drones help bridge inspection teams commercially?", ["They inspect high or hard-to-reach parts quickly without closing lanes or hiring access platforms", "They carry the bridge", "They replace all engineers", "They collect tolls"], 0,
        "Engineers still check the images and confirm defects by hand where needed.",
        "ব্যবসার দিক থেকে ড্রোন সেতু-পরিদর্শক দলকে কীভাবে সাহায্য করে?", ["লেন বন্ধ বা নাগাল-মঞ্চ ভাড়া না করেই উঁচু বা দুর্গম অংশ দ্রুত পরিদর্শন করে", "সেতু বয়ে নেয়", "সব প্রকৌশলীর বদলি", "টোল তোলে"],
        "দরকারে প্রকৌশলীরা ছবি দেখে হাতে-কলমে ত্রুটি নিশ্চিত করেন।"),
    mcq("What is a 'warehouse management system' (WMS)?", ["Software that tracks where every item is stored and guides picking, packing and stock levels", "A security guard", "A forklift", "A delivery van"], 0,
        "It reduces errors and speeds up order picking.",
        "'গুদাম-ব্যবস্থাপনা ব্যবস্থা' (ডব্লিউএমএস) কী?", ["যে সফটওয়্যার প্রতিটা জিনিস কোথায় রাখা আছে নজরে রাখে আর তোলা, প্যাক আর মজুতের মাত্রা পরিচালনা করে", "নিরাপত্তারক্ষী", "ফর্কলিফট", "ডেলিভারি-ভ্যান"],
        "ভুল কমায় আর অর্ডার তোলা দ্রুত করে।"),
)
