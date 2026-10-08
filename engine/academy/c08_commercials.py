"""Class 8 - Commercials (Junior Cadet): economic order quantity, cost per tonne-kilometre, price
elasticity, moving-average forecasts, online click-through and customer acquisition cost,
defects per million, holding costs, whole-life tender evaluation, earnest money and bid
security, the bullwhip effect, dual sourcing, quality systems and fair competition."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r + 2, r * 2, r + 10):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn="", pre_en=""):
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    o = _o(r, *alts)
    return mcq(q_en, [pre_en + f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + u_bn for x in o], ex_bn)


def _c(x):
    x = round(x, 2)
    return int(x) if x == int(x) else x


def eoq(d, s, h, item_en, item_bn):
    q = int(round((2 * d * s / h) ** 0.5))
    return _n(f"A depot uses {d:,} {item_en} a year. Each order costs Rs {s} to place and holding one for a year costs Rs {h}. What is the economic order quantity? (EOQ = √(2DS/H))",
              f"একটা ডিপোতে বছরে {d:,}টি {item_bn} লাগে। প্রতিবার অর্ডারে {s} টাকা খরচ আর একটা এক বছর রাখতে {h} টাকা। অর্থনৈতিক অর্ডার-পরিমাণ কত? (EOQ = √(2DS/H))", q,
              f"EOQ = √(2 x {d:,} x {s} ÷ {h}) = √{2 * d * s // h:,} = {q:,}. It balances ordering costs against storage costs.",
              f"EOQ = √(2 x {d:,} x {s} ÷ {h}) = √{2 * d * s // h:,} = {q:,}। এটা অর্ডারের খরচ আর মজুত রাখার খরচের ভারসাম্য করে।",
              (2 * d * s // h, d // 12, q // 2))


def tkm(cost, t, km):
    r = _c(cost / (t * km))
    return _n(f"Moving {t} tonnes of steel {km} km costs Rs {cost:,}. What is the cost per tonne-kilometre?",
              f"{t} টন ইস্পাত {km} km নিতে {cost:,} টাকা খরচ। টন-কিলোমিটারপ্রতি খরচ কত?", r,
              f"Tonne-km = {t} x {km} = {t * km:,}; {cost:,} ÷ {t * km:,} = Rs {r:g} per tonne-km - handy for comparing road, rail and river.",
              f"টন-কিমি = {t} x {km} = {t * km:,}; {cost:,} ÷ {t * km:,} = টন-কিমিপ্রতি {r:g} টাকা - সড়ক, রেল আর নদীপথ তুলনায় কাজের।",
              (_c(cost / km), _c(cost / t), _c(r * 10)), "", " টাকা", "Rs ")


def elastic(dq, dp, item_en, item_bn):
    e = _c(dq / dp)
    kind_en = "elastic" if e > 1 else "inelastic" if e < 1 else "unit elastic"
    kind_bn = "স্থিতিস্থাপক" if e > 1 else "অস্থিতিস্থাপক" if e < 1 else "একক স্থিতিস্থাপক"
    o = []
    for v in (e, _c(dp / dq), _c(dq + dp), _c(dq * dp / 10)):
        if v not in o:
            o.append(v)
    while len(o) < 4:
        o.append(_c(o[-1] + 0.5))
    return mcq(f"When the price of {item_en} rises {dp}%, sales fall {dq}%. What is the price elasticity of demand (ignoring the minus sign)?",
               [f"{v:g}" for v in o], 0,
               f"Elasticity = % change in quantity ÷ % change in price = {dq} ÷ {dp} = {e:g}, so demand is {kind_en}.",
               f"{item_bn}-এর দাম {dp}% বাড়লে বিক্রি {dq}% কমে। চাহিদার দাম-স্থিতিস্থাপকতা কত (ঋণচিহ্ন বাদ দিয়ে)?",
               [f"{v:g}" for v in o],
               f"স্থিতিস্থাপকতা = পরিমাণের % বদল ÷ দামের % বদল = {dq} ÷ {dp} = {e:g}, তাই চাহিদা {kind_bn}।")


def mavg(a, b, c, item_en, item_bn):
    r = _c((a + b + c) / 3)
    return _n(f"A supplier sold {a}, {b} and {c} {item_en} in the last three months. Using a 3-month moving average, what is the forecast for next month?",
              f"একজন সরবরাহকারী গত তিন মাসে {a}, {b} আর {c}টি {item_bn} বেচলেন। 3-মাসের চলমান গড় ধরে পরের মাসের পূর্বাভাস কত?", r,
              f"({a} + {b} + {c}) ÷ 3 = {r:g}.",
              f"({a} + {b} + {c}) ÷ 3 = {r:g}।",
              (a + b + c, c, _c((a + c) / 2) if _c((a + c) / 2) != r else r + 5))


def ctr(clicks, views):
    r = _c(clicks * 100 / views)
    return _n(f"An online advert for scaffolding hire was shown {views:,} times and clicked {clicks:,} times. What is the click-through rate?",
              f"ভারা-ভাড়ার একটা অনলাইন বিজ্ঞাপন {views:,} বার দেখানো হলো আর {clicks:,} বার ক্লিক হলো। ক্লিক-হার কত?", r,
              f"CTR = clicks ÷ views x 100 = {clicks:,} ÷ {views:,} x 100 = {r:g}%.",
              f"ক্লিক-হার = ক্লিক ÷ দেখা x 100 = {clicks:,} ÷ {views:,} x 100 = {r:g}%।",
              (_c(views / clicks), _c(r * 10), _c(r / 2)), "%", "%")


def cac(spend, new):
    r = spend // new
    return _n(f"A tool-hire firm spent Rs {spend:,} on marketing and won {new} new trade customers. What is the customer acquisition cost?",
              f"একটা যন্ত্র-ভাড়ার সংস্থা বিপণনে {spend:,} টাকা খরচ করে {new} জন নতুন ব্যবসায়ী খদ্দের পেল। খদ্দের-অর্জনের খরচ কত?", r,
              f"CAC = marketing spend ÷ new customers = {spend:,} ÷ {new} = Rs {r:,} each.",
              f"অর্জনের খরচ = বিপণন-খরচ ÷ নতুন খদ্দের = {spend:,} ÷ {new} = প্রত্যেকে {r:,} টাকা।",
              (spend * new // 100, spend // 10, r + new), "", " টাকা", "Rs ")


def ppm(defects, units, item_en, item_bn):
    r = defects * 1_000_000 // units
    return _n(f"A factory made {units:,} {item_en} and found {defects} faulty. What is the defect rate in parts per million (ppm)?",
              f"একটা কারখানা {units:,}টি {item_bn} বানাল আর {defects}টি ত্রুটিপূর্ণ পেল। প্রতি দশ লক্ষে (পিপিএম) ত্রুটির হার কত?", r,
              f"{defects} ÷ {units:,} x 1,000,000 = {r:,} ppm.",
              f"{defects} ÷ {units:,} x 1,000,000 = {r:,} পিপিএম।",
              (r // 10, r * 10, defects * 100), " ppm", " পিপিএম")


def holding(avg_value, pct):
    r = avg_value * pct // 100
    return _n(f"A store holds stock worth Rs {avg_value:,} on average. Storage, insurance and capital cost {pct}% of stock value a year. What is the yearly holding cost?",
              f"একটা ভাঁড়ারে গড়ে {avg_value:,} টাকার মজুত থাকে। গুদাম, বিমা আর মূলধনের খরচ বছরে মজুত-মূল্যের {pct}%। বার্ষিক মজুত রাখার খরচ কত?", r,
              f"{avg_value:,} x {pct}% = Rs {r:,} a year - cash tied up in stock is not free.",
              f"{avg_value:,} x {pct}% = বছরে {r:,} টাকা - মজুতে আটকানো নগদ বিনামূল্যের নয়।",
              (avg_value * pct // 1000, avg_value - r, r * 12), "", " টাকা", "Rs ")


def wholelife(a_bid, a_maint, b_bid, b_maint, years):
    a = a_bid + a_maint * years
    b = b_bid + b_maint * years
    win_en, win_bn = ("Firm A", "সংস্থা A") if a < b else ("Firm B", "সংস্থা B")
    lose_en, lose_bn = ("Firm B", "সংস্থা B") if a < b else ("Firm A", "সংস্থা A")
    return mcq(f"Firm A bids Rs {a_bid} lakh with maintenance of Rs {a_maint} lakh a year; firm B bids Rs {b_bid} lakh with Rs {b_maint} lakh a year. Over {years} years, which is cheaper?",
               [f"{win_en} (Rs {min(a, b)} lakh)", f"{lose_en} (Rs {max(a, b)} lakh)", "They cost the same", "Neither - both are free"], 0,
               f"A: {a_bid} + {a_maint} x {years} = {a}; B: {b_bid} + {b_maint} x {years} = {b}. The lowest bid is not always the cheapest bridge to own.",
               f"সংস্থা A {a_bid} লাখ টাকার দর দেয়, রক্ষণাবেক্ষণ বছরে {a_maint} লাখ; সংস্থা B {b_bid} লাখ, বছরে {b_maint} লাখ। {years} বছরে কোনটা সস্তা?",
               [f"{win_bn} ({min(a, b)} লাখ টাকা)", f"{lose_bn} ({max(a, b)} লাখ টাকা)", "দুটোর খরচ সমান", "কোনোটাই না - দুটোই বিনামূল্যে"],
               f"A: {a_bid} + {a_maint} x {years} = {a}; B: {b_bid} + {b_maint} x {years} = {b}। সবচেয়ে কম দরই সবসময় মালিকানার সবচেয়ে সস্তা সেতু নয়।")


def tiered(qty, p1, cut, p2, item_en, item_bn):
    r = qty * (p2 if qty >= cut else p1)
    return _n(f"{item_en} cost Rs {p1} each, or Rs {p2} each for orders of {cut:,} or more. What does an order of {qty:,} cost?",
              f"{item_bn} প্রতিটা {p1} টাকা, বা {cut:,}টি বা বেশি অর্ডারে প্রতিটা {p2} টাকা। {qty:,}টির অর্ডারে খরচ কত?", r,
              f"{qty:,} ≥ {cut:,}, so every unit is Rs {p2}: {qty:,} x {p2} = Rs {r:,}." if qty >= cut else f"{qty:,} is below {cut:,}, so Rs {p1} each: Rs {r:,}.",
              f"{qty:,} ≥ {cut:,}, তাই প্রতিটা {p2} টাকা: {qty:,} x {p2} = {r:,} টাকা।" if qty >= cut else f"{qty:,} হলো {cut:,}-এর কম, তাই প্রতিটা {p1} টাকা: {r:,} টাকা।",
              (qty * p1 if qty >= cut else qty * p2, cut * p2, r + qty), "", " টাকা", "Rs ")


ITEMS = (
    eoq(1200, 50, 3, "bags of grout", "বস্তা গ্রাউট"), eoq(4500, 100, 10, "steel couplers", "ইস্পাতের কাপলার"),
    eoq(3200, 100, 4, "anchor bolts", "নোঙর-বল্টু"), eoq(12500, 40, 4, "bricks", "ইট"),
    tkm(36000, 20, 300), tkm(15000, 10, 250), tkm(90000, 40, 500), tkm(8000, 5, 400),
    elastic(30, 10, "branded paint", "ব্র্যান্ডেড রং"), elastic(5, 10, "cement", "সিমেন্ট"),
    elastic(20, 10, "decorative tiles", "নকশাদার টালি"), elastic(4, 20, "drinking water", "খাবার জল"),
    mavg(120, 150, 180, "pallets of blocks", "প্যালেট ব্লক"), mavg(40, 46, 52, "scaffold towers", "ভারা-মিনার"),
    mavg(300, 270, 330, "bags of lime", "বস্তা চুন"), mavg(15, 21, 18, "concrete mixers", "কংক্রিট-মিক্সার"),
    ctr(150, 10000), ctr(90, 3000), ctr(400, 20000), ctr(48, 1200),
    cac(60000, 40), cac(150000, 75), cac(24000, 16), cac(90000, 45),
    ppm(3, 10000, "bridge bolts", "সেতুর বল্টু"), ppm(12, 200000, "rivets", "রিভেট"),
    ppm(5, 50000, "cable clamps", "তারের ক্ল্যাম্প"), ppm(2, 400000, "weld studs", "ঝালাই-স্টাড"),
    holding(400000, 20), holding(1500000, 15), holding(250000, 24), holding(800000, 25),
    wholelife(50, 3, 44, 5, 10), wholelife(120, 2, 110, 4, 8), wholelife(80, 6, 95, 2, 15), wholelife(60, 1, 52, 2, 5),
    tiered(500, 40, 400, 35, "Steel brackets", "ইস্পাতের ব্র্যাকেট"), tiered(300, 40, 400, 35, "Bearing pads", "বিয়ারিং-প্যাড"),
    tiered(1000, 12, 1000, 10, "Wall plugs", "দেয়ালের প্লাগ"), tiered(250, 90, 200, 80, "Packs of cable ties", "প্যাকেট তারের বাঁধন"),
    tkm(24000, 12, 200), tkm(5000, 25, 100), elastic(12, 8, "imported tiles", "আমদানি-করা টালি"), mavg(60, 66, 75, "site toilets hired", "ভাড়া-করা নির্মাণস্থলের শৌচাগার"),
    cac(200000, 80), ppm(8, 160000, "anchor plates", "নোঙর-পাত"), holding(600000, 18), wholelife(200, 5, 180, 8, 10), eoq(800, 25, 1, "drums of curing compound", "ড্রাম কিউরিং-যৌগ"),
    mcq("What does the economic order quantity try to balance?", ["The cost of placing many small orders against the cost of storing large stocks", "Price against quality", "Sales against advertising", "Wages against tax"], 0,
        "Order too often and paperwork costs pile up; order too much and storage costs do.",
        "অর্থনৈতিক অর্ডার-পরিমাণ কীসের ভারসাম্য করতে চায়?", ["অনেক ছোট অর্ডারের খরচ বনাম বড় মজুত রাখার খরচ", "দাম বনাম মান", "বিক্রি বনাম বিজ্ঞাপন", "মজুরি বনাম কর"],
        "খুব ঘন ঘন অর্ডারে কাগজপত্রের খরচ জমে; খুব বেশিতে গুদামের খরচ।"),
    mcq("What is a 'tonne-kilometre'?", ["Moving one tonne of goods a distance of one kilometre", "A tonne of goods sold per kilometre of road", "A kilometre of road weighing a tonne", "A speed limit"], 0,
        "It is the standard way to compare freight costs and emissions.",
        "'টন-কিলোমিটার' কী?", ["এক টন মাল এক কিলোমিটার দূরে নেওয়া", "রাস্তার কিলোমিটারপ্রতি বেচা এক টন মাল", "এক টন ওজনের এক কিলোমিটার রাস্তা", "গতিসীমা"],
        "মালবহনের খরচ আর নির্গমন তুলনার প্রচলিত উপায়।"),
    mcq("Why is inland waterway transport often cheapest per tonne-km for heavy cargo?", ["A barge carries huge loads using little fuel because water supports the weight", "Rivers are always straight", "Boats need no crew", "Barges are faster than trains"], 0,
        "Bridges over navigable rivers must leave enough headroom for barges.",
        "ভারী মালের জন্য অভ্যন্তরীণ জলপথ প্রায়ই টন-কিমিপ্রতি সবচেয়ে সস্তা কেন?", ["জল ওজন বয় বলে বজরা অল্প জ্বালানিতে বিশাল বোঝা নেয়", "নদী সবসময় সোজা", "নৌকায় নাবিক লাগে না", "বজরা ট্রেনের চেয়ে দ্রুত"],
        "নৌচলাচলের নদীর উপর সেতুতে বজরার জন্য যথেষ্ট উঁচু ফাঁক রাখতে হয়।"),
    mcq("A bridge's navigation span must give 12 m clearance above high water. Why does this matter commercially?", ["Too low a span would block ships and cut off trade upriver", "It makes the bridge cheaper to paint", "Taller spans attract tourists only", "It does not matter"], 0,
        "Ports and river trade depend on agreed clearances.",
        "সেতুর নৌচলাচল-স্প্যানকে জোয়ারের জলের উপরে 12 m ফাঁক দিতে হবে। ব্যবসার দিক থেকে এটা জরুরি কেন?", ["স্প্যান খুব নিচু হলে জাহাজ আটকাবে আর উজানের বাণিজ্য বন্ধ হবে", "সেতু রং করা সস্তা হয়", "উঁচু স্প্যান শুধু পর্যটক টানে", "জরুরি নয়"],
        "বন্দর আর নদী-বাণিজ্য ঠিক করা ফাঁকের উপর নির্ভর করে।"),
    mcq("If demand for a product is 'elastic', what happens if the firm raises its price?", ["Total revenue usually falls because sales drop a lot", "Revenue always rises", "Sales stay exactly the same", "The product becomes free"], 0,
        "Firms selling elastic goods compete hard on price.",
        "কোনো পণ্যের চাহিদা 'স্থিতিস্থাপক' হলে সংস্থা দাম বাড়ালে কী হয়?", ["বিক্রি অনেক কমায় মোট আয় সাধারণত কমে", "আয় সবসময় বাড়ে", "বিক্রি হুবহু একই থাকে", "পণ্য বিনামূল্যে হয়"],
        "স্থিতিস্থাপক পণ্যের বিক্রেতারা দামে তীব্র প্রতিযোগিতা করে।"),
    mcq("Why do brands with loyal customers often face less elastic demand?", ["Loyal buyers keep buying even when the price rises a little", "Loyal buyers never pay", "Brands are illegal to change", "Elasticity only applies to food"], 0,
        "Building trust and quality gives a firm some pricing power.",
        "অনুগত খদ্দেরওয়ালা ব্র্যান্ডের চাহিদা প্রায়ই কম স্থিতিস্থাপক কেন?", ["দাম একটু বাড়লেও অনুগত ক্রেতারা কিনতে থাকেন", "অনুগত ক্রেতারা টাকা দেন না", "ব্র্যান্ড বদলানো বেআইনি", "স্থিতিস্থাপকতা শুধু খাদ্যে খাটে"],
        "আস্থা আর মান গড়লে সংস্থা দাম ঠিক করার কিছু ক্ষমতা পায়।"),
    mcq("What is a 'moving average' forecast?", ["The average of the most recent few periods, updated each period", "The average speed of trucks", "A forecast that never changes", "The highest sales ever"], 0,
        "It smooths out random ups and downs.",
        "'চলমান গড়' পূর্বাভাস কী?", ["সাম্প্রতিক কয়েকটা সময়কালের গড়, প্রতি সময়কালে হালনাগাদ", "ট্রাকের গড় গতি", "যে পূর্বাভাস কখনো বদলায় না", "সর্বকালের সর্বোচ্চ বিক্রি"],
        "এলোমেলো ওঠানামা মসৃণ করে।"),
    mcq("What is the main weakness of a simple moving average when sales are rising steadily?", ["It lags behind the trend, so forecasts are too low", "It is always too high", "It cannot be calculated", "It uses too much data"], 0,
        "Trend-adjusted methods fix this.",
        "বিক্রি স্থিরভাবে বাড়তে থাকলে সরল চলমান গড়ের প্রধান দুর্বলতা কী?", ["প্রবণতার পিছনে পড়ে থাকে, তাই পূর্বাভাস খুব কম হয়", "সবসময় খুব বেশি", "হিসাব করা যায় না", "খুব বেশি তথ্য লাগে"],
        "প্রবণতা-সমন্বিত পদ্ধতি এটা ঠিক করে।"),
    mcq("What does 'click-through rate' measure?", ["The share of people who saw an online ad and clicked it", "The speed of a website", "The number of products sold", "The price of advertising"], 0,
        "A low CTR suggests the ad is not reaching or interesting the right people.",
        "'ক্লিক-হার' কী মাপে?", ["অনলাইন বিজ্ঞাপন যাঁরা দেখলেন, তাঁদের কত অংশ ক্লিক করলেন", "ওয়েবসাইটের গতি", "বিক্রি হওয়া পণ্যের সংখ্যা", "বিজ্ঞাপনের দাম"],
        "কম ক্লিক-হার বোঝায় বিজ্ঞাপন ঠিক মানুষের কাছে পৌঁছোচ্ছে না বা আগ্রহ জাগাচ্ছে না।"),
    mcq("A customer brings Rs 30,000 profit over their lifetime. Is a customer acquisition cost of Rs 2,000 worth it?", ["Yes - the customer is worth far more than it costs to win them", "No - any cost is too much", "Only if the customer is a relative", "It cannot be judged"], 0,
        "Firms compare lifetime value with acquisition cost.",
        "একজন খদ্দের জীবনভর 30,000 টাকা লাভ আনেন। 2,000 টাকার খদ্দের-অর্জনের খরচ কি সার্থক?", ["হ্যাঁ - খদ্দেরকে পাওয়ার খরচের চেয়ে তাঁর মূল্য অনেক বেশি", "না - যেকোনো খরচই বেশি", "শুধু খদ্দের আত্মীয় হলে", "বিচার করা যায় না"],
        "সংস্থা জীবনকালীন মূল্যকে অর্জনের খরচের সঙ্গে তুলনা করে।"),
    mcq("A paint firm sells a tough marine coating to bridge builders and a cheaper washable paint to homeowners. What is it doing?", ["Serving different market segments with products suited to each", "Selling the same product to everyone", "Breaking competition law", "Price fixing"], 0,
        "Different buyers value different things - durability for bridges, price and colour for homes.",
        "একটা রং-সংস্থা সেতু-নির্মাতাদের মজবুত সামুদ্রিক আবরণ আর বাড়ির মালিকদের সস্তা ধোয়া-যায় এমন রং বেচে। এটা কী করছে?", ["প্রতিটার উপযোগী পণ্য দিয়ে আলাদা বাজার-অংশের সেবা করছে", "সবাইকে একই পণ্য বেচছে", "প্রতিযোগিতা-আইন ভাঙছে", "দাম বাঁধছে"],
        "আলাদা ক্রেতা আলাদা জিনিসকে মূল্য দেন - সেতুর জন্য টেকসই, বাড়ির জন্য দাম আর রং।"),
    mcq("What is 'positioning' in marketing?", ["How a firm wants customers to see its product compared with rivals", "Where the shop is located only", "Putting goods on shelves", "Parking trucks"], 0,
        "A paint might be positioned as 'the longest-lasting' or 'the best value'.",
        "বিপণনে 'অবস্থান-নির্ধারণ' কী?", ["প্রতিদ্বন্দ্বীদের তুলনায় খদ্দেররা পণ্যটাকে কীভাবে দেখুক, সংস্থা যা চায়", "শুধু দোকানের ঠিকানা", "তাকে মাল সাজানো", "ট্রাক রাখা"],
        "একটা রং 'সবচেয়ে টেকসই' বা 'সবচেয়ে সাশ্রয়ী' হিসেবে অবস্থান নিতে পারে।"),
    mcq("What is B2B selling?", ["Business-to-business: selling to other firms, such as cement to contractors", "Back-to-back selling", "Selling to babies", "Buying two, getting two"], 0,
        "B2B deals are usually larger, slower and built on relationships.",
        "বিটুবি বিক্রি কী?", ["ব্যবসা-থেকে-ব্যবসা: অন্য সংস্থাকে বেচা, যেমন ঠিকাদারকে সিমেন্ট", "পিঠোপিঠি বিক্রি", "শিশুদের কাছে বিক্রি", "দুটো কিনলে দুটো"],
        "বিটুবি চুক্তি সাধারণত বড়, ধীর আর সম্পর্কের উপর দাঁড়ানো।"),
    mcq("What does 'parts per million' (ppm) express in quality control?", ["How many faulty items there are in every million made", "The price per million items", "The speed of a machine", "The number of workers"], 0,
        "Top suppliers aim for very low ppm on safety-critical parts like bridge bolts.",
        "মান-নিয়ন্ত্রণে 'প্রতি দশ লক্ষে অংশ' (পিপিএম) কী প্রকাশ করে?", ["প্রতি দশ লক্ষ তৈরিতে কতগুলো ত্রুটিপূর্ণ", "প্রতি দশ লক্ষ জিনিসের দাম", "যন্ত্রের গতি", "কর্মীর সংখ্যা"],
        "সেরা সরবরাহকারীরা সেতুর বল্টুর মতো নিরাপত্তা-জরুরি অংশে খুব কম পিপিএম চান।"),
    mcq("What is 'Six Sigma'?", ["A quality method aiming for no more than about 3.4 defects per million opportunities", "Six managers in a team", "A sixth-grade exam", "A type of crane"], 0,
        "It uses data to find and remove the causes of defects.",
        "'সিক্স সিগমা' কী?", ["প্রতি দশ লক্ষ সুযোগে প্রায় 3.4টির বেশি ত্রুটি না রাখার মান-পদ্ধতি", "একটা দলে ছয়জন ম্যানেজার", "ষষ্ঠ শ্রেণির পরীক্ষা", "এক রকম ক্রেন"],
        "তথ্য দিয়ে ত্রুটির কারণ খুঁজে দূর করে।"),
    mcq("What does ISO 9001 certification tell a client about a steel fabricator?", ["It runs a checked quality management system with written procedures and audits", "Its steel is free", "It has 9,001 workers", "It never makes mistakes"], 0,
        "Certification shows a system for catching and fixing problems.",
        "আইএসও 9001 শংসাপত্র একজন গ্রাহককে ইস্পাত-ফ্যাব্রিকেটর সম্পর্কে কী জানায়?", ["এটা লিখিত পদ্ধতি আর নিরীক্ষাসহ যাচাই-করা মান-ব্যবস্থাপনা চালায়", "এর ইস্পাত বিনামূল্যে", "এর 9,001 জন কর্মী", "এটা কখনো ভুল করে না"],
        "শংসাপত্র সমস্যা ধরা আর সারানোর একটা ব্যবস্থা দেখায়।"),
    mcq("What is a 'mill test certificate' that comes with steel?", ["A document from the steel mill showing the steel's tested chemistry and strength", "A receipt for the truck", "A certificate for mill workers' training", "A flour quality label"], 0,
        "Bridge engineers check it before steel is used.",
        "ইস্পাতের সঙ্গে আসা 'কারখানা-পরীক্ষার শংসাপত্র' কী?", ["ইস্পাত-কারখানার নথি, যাতে ইস্পাতের পরীক্ষিত রাসায়নিক গঠন আর শক্তি থাকে", "ট্রাকের রসিদ", "কারখানা-কর্মীদের প্রশিক্ষণের শংসাপত্র", "আটার মানের লেবেল"],
        "ব্যবহারের আগে সেতু-প্রকৌশলীরা এটা যাচাই করেন।"),
    mcq("What is 'traceability' for bridge materials?", ["Being able to trace each batch back to where and when it was made and tested", "Drawing tracing-paper plans", "Following trucks with a camera", "Keeping no records"], 0,
        "If a fault is found, all parts from the same batch can be checked quickly.",
        "সেতু-সামগ্রীর 'উৎস-অনুসরণযোগ্যতা' কী?", ["প্রতিটা ব্যাচ কোথায়, কবে তৈরি আর পরীক্ষা হয়েছিল তা খুঁজে বের করতে পারা", "ট্রেসিং-কাগজে নকশা আঁকা", "ক্যামেরা নিয়ে ট্রাকের পিছু নেওয়া", "কোনো নথি না রাখা"],
        "ত্রুটি মিললে একই ব্যাচের সব অংশ দ্রুত পরীক্ষা করা যায়।"),
    mcq("What is the 'holding cost' of stock?", ["The yearly cost of keeping stock: storage, insurance, damage and the cash tied up", "The price paid to the supplier", "A cost for holding a meeting", "Delivery charges"], 0,
        "It is often 15-30% of the stock's value per year.",
        "মজুতের 'ধারণ-খরচ' কী?", ["মজুত রাখার বার্ষিক খরচ: গুদাম, বিমা, ক্ষতি আর আটকে থাকা নগদ", "সরবরাহকারীকে দেওয়া দাম", "সভা করার খরচ", "ডেলিভারির খরচ"],
        "প্রায়ই বছরে মজুত-মূল্যের 15-30%।"),
    mcq("What is 'whole-life costing' for a bridge?", ["Adding up the cost to build, run, maintain and finally remove it over its life", "Only the construction price", "The cost of one day's traffic", "The designer's fee"], 0,
        "A cheaper bridge needing constant repairs can cost more in the end.",
        "সেতুর 'পূর্ণ-জীবন খরচ' কী?", ["বানানো, চালানো, রক্ষণাবেক্ষণ আর শেষে সরানোর খরচ জীবনভর যোগ করা", "শুধু নির্মাণের দাম", "এক দিনের যানবাহনের খরচ", "নকশাকারের ফি"],
        "সস্তা সেতুতে সারাক্ষণ মেরামত লাগলে শেষে বেশি খরচ হতে পারে।"),
    mcq("What is an 'earnest money deposit' (EMD) in a public tender?", ["A small deposit bidders pay to show they are serious; it is returned or kept if they back out", "The full contract price", "A bribe", "A fee for reading the tender"], 0,
        "It discourages time-wasting bids.",
        "সরকারি দরপত্রে 'বায়না-জমা' (ইএমডি) কী?", ["দরদাতারা আন্তরিকতা দেখাতে যে ছোট জমা দেন; ফেরত হয়, বা পিছিয়ে গেলে রেখে দেওয়া হয়", "চুক্তির পুরো দাম", "ঘুষ", "দরপত্র পড়ার ফি"],
        "সময় নষ্ট করা দর ঠেকায়।"),
    mcq("A tender requires an EMD of 2% of the estimated Rs 5 crore value. How much must each bidder deposit?", ["Rs 10 lakh", "Rs 1 lakh", "Rs 1 crore", "Rs 2 lakh"], 0,
        "5,00,00,000 x 2% = 10,00,000.",
        "একটা দরপত্রে আনুমানিক 5 কোটি টাকার 2% বায়না-জমা লাগে। প্রত্যেক দরদাতাকে কত জমা দিতে হবে?", ["10 লাখ টাকা", "1 লাখ টাকা", "1 কোটি টাকা", "2 লাখ টাকা"],
        "5,00,00,000 x 2% = 10,00,000।"),
    mcq("What does 'L1' mean in Indian public tenders?", ["The lowest technically qualified bidder", "The first bidder to arrive", "Level 1 of a building", "The largest firm"], 0,
        "Bids must first pass the technical check before price is compared.",
        "ভারতের সরকারি দরপত্রে 'এল1' মানে কী?", ["কারিগরি যোগ্যতা পাওয়া সবচেয়ে কম দরদাতা", "প্রথম পৌঁছানো দরদাতা", "বাড়ির প্রথম তলা", "সবচেয়ে বড় সংস্থা"],
        "দাম তুলনার আগে দরকে কারিগরি যাচাই পেরোতে হয়।"),
    mcq("Why do tenders for big bridges often have a technical stage before price is opened?", ["To make sure only firms able to build safely are compared on price", "To delay the project", "Because price does not matter", "To choose the most expensive firm"], 0,
        "A cheap bid from an inexperienced firm can be the most costly mistake.",
        "বড় সেতুর দরপত্রে দাম খোলার আগে প্রায়ই কারিগরি পর্যায় থাকে কেন?", ["নিশ্চিত করতে যে শুধু নিরাপদে বানাতে সক্ষম সংস্থাগুলোই দামে তুলনা হয়", "প্রকল্পে দেরি করাতে", "কারণ দাম গুরুত্বহীন", "সবচেয়ে দামি সংস্থা বাছতে"],
        "অনভিজ্ঞ সংস্থার সস্তা দর সবচেয়ে দামি ভুল হতে পারে।"),
    mcq("What is the 'bullwhip effect' in a supply chain?", ["Small changes in customer demand grow into big swings in orders further up the chain", "Trucks cracking whips", "Prices always falling", "Warehouses shaking"], 0,
        "Sharing real sales data along the chain calms the whip.",
        "সরবরাহ-শৃঙ্খলে 'চাবুক-প্রভাব' কী?", ["খদ্দেরের চাহিদার ছোট বদল শৃঙ্খলের উপরের দিকে অর্ডারে বড় দোলায় পরিণত হয়", "ট্রাকে চাবুক হাঁকানো", "দাম সবসময় পড়া", "গুদাম কাঁপা"],
        "শৃঙ্খল জুড়ে আসল বিক্রির তথ্য ভাগ করলে চাবুক শান্ত হয়।"),
    mcq("Why might a bridge contractor use two suppliers for bearings instead of one?", ["If one supplier fails or is late, the other can still deliver (dual sourcing)", "Two suppliers are always cheaper", "Bearings must be mixed", "One supplier is illegal"], 0,
        "Single sourcing can be cheaper but is riskier.",
        "একজন সেতু-ঠিকাদার বিয়ারিংয়ের জন্য একজনের বদলে দুজন সরবরাহকারী রাখতে পারেন কেন?", ["একজন ব্যর্থ হলে বা দেরি করলে অন্যজন এখনো দিতে পারেন (দ্বৈত-উৎস)", "দুজন সবসময় সস্তা", "বিয়ারিং মিশিয়ে লাগাতে হয়", "একজন সরবরাহকারী বেআইনি"],
        "একক-উৎস সস্তা হতে পারে, কিন্তু বেশি ঝুঁকির।"),
    mcq("What is a 'single point of failure' in a supply chain?", ["One supplier, route or machine whose failure stops everything", "A broken pencil", "The best supplier", "A spare part"], 0,
        "A single bridge on the only road to a quarry is a classic example.",
        "সরবরাহ-শৃঙ্খলে 'একক ব্যর্থতা-বিন্দু' কী?", ["এমন একজন সরবরাহকারী, পথ বা যন্ত্র যা বিকল হলে সব থেমে যায়", "ভাঙা পেনসিল", "সেরা সরবরাহকারী", "খুচরো যন্ত্রাংশ"],
        "খাদানের একমাত্র রাস্তায় একটা সেতু ধ্রুপদী উদাহরণ।"),
    mcq("What is a 'cartel'?", ["Firms secretly agreeing to fix prices or share markets instead of competing", "A large truck", "A trade fair", "A shopping cart"], 0,
        "Cement and steel cartels have been fined by competition regulators.",
        "'কার্টেল' কী?", ["প্রতিযোগিতা না করে সংস্থাগুলোর গোপনে দাম বাঁধা বা বাজার ভাগের চুক্তি", "বড় ট্রাক", "বাণিজ্যমেলা", "কেনাকাটার গাড়ি"],
        "প্রতিযোগিতা-নিয়ন্ত্রক সিমেন্ট আর ইস্পাতের কার্টেলকে জরিমানা করেছে।"),
    mcq("Which body in India investigates cartels and unfair competition?", ["The Competition Commission of India (CCI)", "The Indian Railways", "The Election Commission", "A city council"], 0,
        "Fair competition keeps prices honest for public projects.",
        "ভারতে কোন সংস্থা কার্টেল আর অন্যায্য প্রতিযোগিতার তদন্ত করে?", ["ভারতীয় প্রতিযোগিতা কমিশন (সিসিআই)", "ভারতীয় রেল", "নির্বাচন কমিশন", "পৌরসভা"],
        "ন্যায্য প্রতিযোগিতা সরকারি প্রকল্পে দাম সৎ রাখে।"),
    mcq("What is 'predatory pricing'?", ["A big firm selling below cost to drive smaller rivals out, then raising prices", "Pricing animals at a zoo", "A normal sale", "Charging a fair price"], 0,
        "Competition law can forbid it.",
        "'শিকারি মূল্যনির্ধারণ' কী?", ["ছোট প্রতিদ্বন্দ্বীদের তাড়াতে বড় সংস্থার খরচের নিচে বেচা, পরে দাম বাড়ানো", "চিড়িয়াখানায় প্রাণীর দাম", "সাধারণ বিক্রি", "ন্যায্য দাম নেওয়া"],
        "প্রতিযোগিতা-আইন এটা নিষিদ্ধ করতে পারে।"),
    mcq("A market dominated by a few large sellers, such as cement or steel, is called…", ["An oligopoly", "A monopoly", "Perfect competition", "A cooperative"], 0,
        "With few sellers, each watches the others closely - and regulators watch for cartels.",
        "সিমেন্ট বা ইস্পাতের মতো কয়েকজন বড় বিক্রেতার দখলে থাকা বাজারকে বলে…", ["অল্প-বিক্রেতার বাজার (অলিগোপলি)", "একচেটিয়া বাজার", "পূর্ণ প্রতিযোগিতা", "সমবায়"],
        "বিক্রেতা কম হলে প্রত্যেকে অন্যদের কড়া নজরে রাখে - আর নিয়ন্ত্রকরা কার্টেলে নজর রাখেন।"),
    mcq("What is 'lean construction'?", ["Planning and working so as to cut waste of materials, time and effort", "Building very thin bridges", "Using no workers", "Leaning walls"], 0,
        "Ordering only what is needed and avoiding waiting time are lean ideas.",
        "'লিন নির্মাণ' কী?", ["উপাদান, সময় আর শ্রমের অপচয় কমাতে পরিকল্পনা আর কাজ", "খুব সরু সেতু বানানো", "কর্মী ছাড়া কাজ", "হেলানো দেয়াল"],
        "শুধু যা দরকার তা অর্ডার আর অপেক্ষার সময় এড়ানো লিন ভাবনা।"),
    mcq("What is 'kaizen'?", ["A habit of making many small, continuous improvements", "A Japanese bridge", "A one-time big change", "A type of cement"], 0,
        "Every worker is encouraged to suggest better ways of working.",
        "'কাইজেন' কী?", ["অনেক ছোট, ক্রমাগত উন্নতি করার অভ্যাস", "জাপানি সেতু", "একবারের বড় বদল", "এক রকম সিমেন্ট"],
        "প্রতিটা কর্মীকে কাজের ভালো উপায় সুপারিশ করতে উৎসাহ দেওয়া হয়।"),
    mcq("What is 'vendor rating'?", ["Scoring suppliers regularly on quality, delivery and price to decide whom to keep using", "Rating street vendors' food", "A supplier's advert", "A tax on vendors"], 0,
        "It rewards reliable suppliers with more business.",
        "'বিক্রেতা-মূল্যায়ন' কী?", ["কাকে রাখা হবে ঠিক করতে নিয়মিত মান, ডেলিভারি আর দামে সরবরাহকারীদের নম্বর দেওয়া", "ফেরিওয়ালার খাবারের মূল্যায়ন", "সরবরাহকারীর বিজ্ঞাপন", "বিক্রেতার উপর কর"],
        "ভরসার সরবরাহকারীরা বেশি কাজ পান।"),
    mcq("Why is a price quoted 'ex-works' usually lower than one quoted 'delivered to site'?", ["Ex-works means the buyer collects from the factory and pays for transport", "Ex-works goods are second-hand", "Delivered goods are better quality", "Ex-works prices exclude the goods"], 0,
        "Always compare prices on the same delivery basis.",
        "'কারখানা-থেকে' (এক্স-ওয়ার্কস) দাম সাধারণত 'নির্মাণস্থলে পৌঁছে' দামের চেয়ে কম কেন?", ["এক্স-ওয়ার্কস মানে ক্রেতা কারখানা থেকে নিজে আনেন আর পরিবহনের খরচ দেন", "এক্স-ওয়ার্কস মাল পুরোনো", "পৌঁছে-দেওয়া মালের মান ভালো", "এক্স-ওয়ার্কস দামে মাল ধরা নেই"],
        "সবসময় একই ডেলিভারি-ভিত্তিতে দাম তুলনা করো।"),
    mcq("What is 'dead stock'?", ["Stock that has not been sold or used for a long time and may never be", "Stock that has been delivered", "Animals on a farm", "Stock counted twice"], 0,
        "It wastes space and cash; firms clear it with discounts or recycling.",
        "'অচল মজুত' কী?", ["যে মজুত অনেকদিন বিক্রি বা ব্যবহার হয়নি আর হয়তো কখনো হবে না", "পৌঁছে যাওয়া মজুত", "খামারের পশু", "দুবার গোনা মজুত"],
        "জায়গা আর নগদ নষ্ট করে; সংস্থা ছাড় দিয়ে বা পুনর্ব্যবহারে সরায়।"),
    mcq("Why might a precast-beam factory make a short 'pilot run' before full production?", ["To find and fix problems in the process before making hundreds of beams", "To waste materials", "Because pilots buy beams", "To delay the client"], 0,
        "Mistakes are cheapest to fix early.",
        "একটা প্রিকাস্ট-কড়ির কারখানা পুরো উৎপাদনের আগে ছোট 'পরীক্ষামূলক উৎপাদন' করতে পারে কেন?", ["শত শত কড়ি বানানোর আগে প্রক্রিয়ার সমস্যা খুঁজে সারাতে", "উপাদান নষ্ট করতে", "কারণ বিমানচালকরা কড়ি কেনেন", "গ্রাহককে দেরি করাতে"],
        "ভুল আগেভাগে সারানোই সবচেয়ে সস্তা।"),
    mcq("Why are bridge tolls often set or approved by a government body?", ["Drivers may have no other route, so tolls could otherwise be unfairly high", "Toll operators cannot count", "Tolls are always free", "To make queues longer"], 0,
        "Regulation protects users while letting operators recover their costs.",
        "সেতুর টোল প্রায়ই সরকারি সংস্থা ঠিক বা অনুমোদন করে কেন?", ["চালকদের অন্য পথ নাও থাকতে পারে, নইলে টোল অন্যায্যভাবে বেশি হতে পারত", "টোল-পরিচালকরা গুনতে পারেন না", "টোল সবসময় বিনামূল্যে", "লাইন লম্বা করতে"],
        "নিয়ন্ত্রণ ব্যবহারকারীদের রক্ষা করে, আবার পরিচালককে খরচ তুলতেও দেয়।"),
    mcq("What is a 'trade mark'?", ["A legally protected name, logo or symbol that identifies a firm's products", "A mark left by trucks", "A school grade", "A price tag"], 0,
        "Copying another firm's trade mark on fake goods is illegal.",
        "'ট্রেডমার্ক' কী?", ["আইনত সুরক্ষিত নাম, লোগো বা প্রতীক যা একটা সংস্থার পণ্য চেনায়", "ট্রাকের রেখে যাওয়া দাগ", "স্কুলের নম্বর", "দামের ট্যাগ"],
        "নকল মালে অন্য সংস্থার ট্রেডমার্ক বসানো বেআইনি।"),
    mcq("Why are counterfeit (fake) bolts dangerous on a bridge project?", ["They may look identical but be weaker, so joints could fail under load", "They are always too strong", "They rust less", "They cost more"], 0,
        "Buy from trusted suppliers and check certificates and markings.",
        "সেতু-প্রকল্পে নকল বল্টু বিপজ্জনক কেন?", ["দেখতে হুবহু এক হলেও দুর্বল হতে পারে, তাই বোঝায় জোড় ভেঙে যেতে পারে", "সবসময় বেশি শক্ত", "কম মরচে ধরে", "দাম বেশি"],
        "ভরসার সরবরাহকারীর কাছে কেনো আর শংসাপত্র ও চিহ্ন যাচাই করো।"),
    mcq("What is a 'patent'?", ["A legal right for an inventor to stop others copying an invention for a number of years", "A shiny leather", "A doctor's patient", "A tax on ideas"], 0,
        "New bridge-bearing designs and cable systems are often patented.",
        "'পেটেন্ট' কী?", ["উদ্ভাবকের আইনি অধিকার, যাতে কয়েক বছর অন্যরা উদ্ভাবন নকল করতে না পারে", "চকচকে চামড়া", "ডাক্তারের রোগী", "ভাবনার উপর কর"],
        "নতুন সেতু-বিয়ারিংয়ের নকশা আর তারের ব্যবস্থা প্রায়ই পেটেন্ট করা হয়।"),
    mcq("What is 'export promotion' through a new bridge or port link?", ["Lower transport costs make local products cheaper to sell abroad", "Banning exports", "Taxing every export heavily", "Closing the border"], 0,
        "Good infrastructure helps farmers and factories reach world markets.",
        "নতুন সেতু বা বন্দর-সংযোগের মাধ্যমে 'রপ্তানি-প্রসার' কী?", ["পরিবহন-খরচ কমায় স্থানীয় পণ্য বিদেশে বেচা সস্তা হয়", "রপ্তানি নিষিদ্ধ", "প্রতিটা রপ্তানিতে চড়া কর", "সীমান্ত বন্ধ"],
        "ভালো পরিকাঠামো চাষি আর কারখানাকে বিশ্ববাজারে পৌঁছাতে সাহায্য করে।"),
    mcq("Why are exports of goods often 'zero-rated' for GST in India?", ["So that Indian goods are not made more expensive abroad by Indian tax", "Because exports are illegal", "To raise more tax", "Because exports have no value"], 0,
        "Exporters can usually claim back GST paid on their inputs.",
        "ভারতে পণ্য রপ্তানি প্রায়ই জিএসটিতে 'শূন্য-হারযুক্ত' কেন?", ["যাতে ভারতীয় কর বিদেশে ভারতীয় পণ্যকে দামি না করে", "কারণ রপ্তানি বেআইনি", "বেশি কর তুলতে", "কারণ রপ্তানির মূল্য নেই"],
        "রপ্তানিকারকরা সাধারণত উপাদানে দেওয়া জিএসটি ফেরত দাবি করতে পারেন।"),
    mcq("What is a 'consignment'?", ["A batch of goods sent together from a seller to a buyer", "A signed letter", "A type of loan", "A truck driver's licence"], 0,
        "Each consignment travels with its own documents.",
        "'চালান' (কনসাইনমেন্ট) কী?", ["বিক্রেতা থেকে ক্রেতাকে একসঙ্গে পাঠানো মালের দল", "সই-করা চিঠি", "এক রকম ঋণ", "ট্রাক-চালকের লাইসেন্স"],
        "প্রতিটা চালান নিজের নথিসহ যায়।"),
    mcq("What is an 'e-way bill' in India?", ["An electronic document needed to move goods above a set value by road", "An electricity bill", "A toll receipt", "A train ticket"], 0,
        "It helps tax authorities track goods in transit.",
        "ভারতে 'ই-ওয়ে বিল' কী?", ["নির্দিষ্ট মূল্যের বেশি মাল সড়কপথে নিতে লাগা ইলেকট্রনিক নথি", "বিদ্যুতের বিল", "টোলের রসিদ", "ট্রেনের টিকিট"],
        "কর-কর্তৃপক্ষকে চলমান মাল নজরে রাখতে সাহায্য করে।"),
    mcq("What does a 'GPS tracker' on a fleet of delivery trucks help a logistics manager do?", ["See where trucks are, plan routes and give customers accurate arrival times", "Make trucks faster", "Avoid paying drivers", "Fill fuel tanks"], 0,
        "It also helps spot idling that wastes fuel.",
        "ডেলিভারি-ট্রাকের বহরে 'জিপিএস-ট্র্যাকার' পরিবহন-ম্যানেজারকে কী করতে সাহায্য করে?", ["ট্রাক কোথায় দেখতে, পথ ঠিক করতে আর খদ্দেরকে সঠিক পৌঁছানোর সময় জানাতে", "ট্রাক দ্রুত করতে", "চালকদের বেতন না দিতে", "জ্বালানি ভরতে"],
        "অলস দাঁড়িয়ে জ্বালানি পোড়ানোও ধরা পড়ে।"),
    mcq("A detour adds 40 km to each of 25 trucks a day while a bridge is closed. Fuel and driver cost Rs 30 per km. What is the extra daily cost?", ["Rs 30,000", "Rs 1,000", "Rs 3,000", "Rs 12,000"], 0,
        "40 x 25 = 1,000 extra km; x Rs 30 = Rs 30,000 a day - why bridge closures are planned carefully.",
        "সেতু বন্ধ থাকায় ঘুরপথে দিনে 25টি ট্রাকের প্রত্যেকটার 40 km বাড়ে। জ্বালানি আর চালকের খরচ km-প্রতি 30 টাকা। দৈনিক বাড়তি খরচ কত?", ["30,000 টাকা", "1,000 টাকা", "3,000 টাকা", "12,000 টাকা"],
        "40 x 25 = 1,000 বাড়তি km; x 30 টাকা = দিনে 30,000 টাকা - তাই সেতু বন্ধ যত্ন করে পরিকল্পনা হয়।"),
    mcq("Why do contractors often repair bridges at night or at weekends?", ["Fewer road users are delayed, so the economic cost of disruption is lower", "Concrete only sets at night", "Workers prefer darkness", "Night work is always cheaper"], 0,
        "Night work costs more in wages, but saves the public far more in delays.",
        "ঠিকাদাররা প্রায়ই রাতে বা সপ্তাহান্তে সেতু মেরামত করেন কেন?", ["কম যাত্রী দেরিতে পড়েন, তাই ব্যাঘাতের অর্থনৈতিক খরচ কম", "কংক্রিট শুধু রাতে জমে", "কর্মীরা অন্ধকার পছন্দ করেন", "রাতের কাজ সবসময় সস্তা"],
        "রাতের কাজে মজুরি বেশি, কিন্তু জনসাধারণের দেরির খরচ অনেক বেশি বাঁচে।"),
    mcq("What does a 'service level' of 98% mean for a supplier's stock?", ["98 out of 100 orders can be filled straight from stock", "98% of workers are present", "Prices are 98% of list", "98% of trucks are new"], 0,
        "Higher service levels need more safety stock.",
        "সরবরাহকারীর মজুতে '98% পরিষেবা-স্তর' মানে কী?", ["100টা অর্ডারের 98টা সরাসরি মজুত থেকে মেটানো যায়", "98% কর্মী উপস্থিত", "দাম তালিকার 98%", "98% ট্রাক নতুন"],
        "বেশি পরিষেবা-স্তরে বেশি নিরাপত্তা-মজুত লাগে।"),
    mcq("What is a 'framework agreement' with a supplier?", ["A long-term agreement on prices and terms, with individual orders placed as needed", "A wooden frame", "A single one-off purchase", "An agreement to never buy again"], 0,
        "It saves re-tendering for every small order.",
        "সরবরাহকারীর সঙ্গে 'কাঠামো-চুক্তি' কী?", ["দাম আর শর্তে দীর্ঘমেয়াদি চুক্তি, দরকার মতো আলাদা আলাদা অর্ডার", "কাঠের ফ্রেম", "একবারের কেনা", "আর কখনো না কেনার চুক্তি"],
        "প্রতিটা ছোট অর্ডারে নতুন দরপত্র এড়ায়।"),
    mcq("A bridge builder's reputation suffers after a widely shared video of unsafe work. What is the best commercial response?", ["Fix the safety problem openly, explain the changes and let results rebuild trust", "Delete all comments and deny it", "Blame the workers publicly", "Lower prices and say nothing"], 0,
        "Honesty and real improvement are the only lasting repair for reputation.",
        "অনিরাপদ কাজের একটা ভিডিও ছড়িয়ে পড়ায় একজন সেতু-নির্মাতার সুনাম ক্ষতিগ্রস্ত হলো। সবচেয়ে ভালো ব্যবসায়িক জবাব কী?", ["খোলাখুলি নিরাপত্তার সমস্যা সারাও, বদলগুলো বুঝিয়ে বলো আর ফলাফলকে আস্থা ফেরাতে দাও", "সব মন্তব্য মুছে অস্বীকার করো", "প্রকাশ্যে কর্মীদের দোষ দাও", "দাম কমিয়ে চুপ থাকো"],
        "সততা আর আসল উন্নতিই সুনামের একমাত্র স্থায়ী মেরামত।"),
)
