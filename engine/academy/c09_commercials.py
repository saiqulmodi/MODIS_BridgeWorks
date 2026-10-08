"""Class 9 - Commercials (Bridge Engineer cadet): supply and demand and the equilibrium price,
shifts in curves, price ceilings and floors, comparative advantage, tariffs and exchange rates
for exporters, toll-plaza queues and capacity, earned-value tracking of projects, return on ad
spend, hub-and-spoke networks, and India's highway contract models (EPC, BOT, HAM)."""
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
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    o = _o(r, *alts)
    return mcq(q_en, [pre_en + f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + u_bn for x in o], ex_bn)


def equil(a, b, c, d, item_en, item_bn):
    p = _c((a - c) / (b + d))
    q = _c(a - b * p)
    return _n(f"For {item_en}, demand is Qd = {a} - {b}P and supply is Qs = {c} + {d}P (P in Rs hundreds). What is the equilibrium price P?",
              f"{item_bn}-এর চাহিদা Qd = {a} - {b}P আর জোগান Qs = {c} + {d}P (P শত টাকায়)। ভারসাম্য-দাম P কত?", p,
              f"Set Qd = Qs: {a} - {b}P = {c} + {d}P, so {a - c} = {b + d}P and P = {p:g}. Quantity = {q:g}.",
              f"Qd = Qs ধরো: {a} - {b}P = {c} + {d}P, তাই {a - c} = {b + d}P আর P = {p:g}। পরিমাণ = {q:g}।",
              (q, _c((a + c) / (b + d)), _c(a / b)))


def queue(arrivals, lanes, service):
    r = _c(arrivals * 100 / (lanes * service))
    return _n(f"At a toll plaza, {arrivals:,} vehicles arrive per hour. Each of {lanes} booths can serve {service} vehicles per hour. What is the utilisation of the booths?",
              f"একটা টোল-প্লাজায় ঘণ্টায় {arrivals:,}টি যান আসে। {lanes}টি বুথের প্রত্যেকটা ঘণ্টায় {service}টি যান সামলাতে পারে। বুথের ব্যবহার-হার কত?", r,
              f"Capacity = {lanes} x {service} = {lanes * service:,} per hour; utilisation = {arrivals:,} ÷ {lanes * service:,} x 100 = {r:g}%. Near 100%, queues grow very long.",
              f"ক্ষমতা = {lanes} x {service} = ঘণ্টায় {lanes * service:,}; ব্যবহার = {arrivals:,} ÷ {lanes * service:,} x 100 = {r:g}%। 100%-এর কাছে লাইন খুব লম্বা হয়।",
              (_c(arrivals * 100 / service), _c(lanes * service * 100 / arrivals), _c(r / 2)), "%", "%")


def capu(out, cap, what_en, what_bn):
    r = _c(out * 100 / cap)
    return _n(f"{what_en} can make {cap:,} units a month but made {out:,}. What is its capacity utilisation?",
              f"{what_bn} মাসে {cap:,} একক বানাতে পারে, বানাল {out:,}। ক্ষমতার ব্যবহার কত?", r,
              f"{out:,} ÷ {cap:,} x 100 = {r:g}%. Fixed costs are spread over fewer units when this is low.",
              f"{out:,} ÷ {cap:,} x 100 = {r:g}%। এটা কম হলে স্থির খরচ কম এককে ভাগ হয়।",
              (_c(100 - r), _c(cap * 100 / out), _c(r / 2)), "%", "%")


def cpi(ev, ac):
    r = _c(ev / ac)
    state_en = "under budget" if r > 1 else "over budget" if r < 1 else "on budget"
    state_bn = "বাজেটের নিচে" if r > 1 else "বাজেটের বেশি" if r < 1 else "বাজেট মতো"
    return _n(f"A bridge project has earned value (work done, at budget prices) of Rs {ev} crore and actual cost of Rs {ac} crore. What is its cost performance index (CPI)?",
              f"একটা সেতু-প্রকল্পের অর্জিত মূল্য (বাজেট-দামে করা কাজ) {ev} কোটি টাকা আর আসল খরচ {ac} কোটি টাকা। খরচ-দক্ষতা সূচক (সিপিআই) কত?", r,
              f"CPI = EV ÷ AC = {ev} ÷ {ac} = {r:g}, so the project is {state_en}.",
              f"সিপিআই = অর্জিত ÷ আসল = {ev} ÷ {ac} = {r:g}, তাই প্রকল্প {state_bn}।",
              (_c(ac / ev), ev - ac if ev > ac else ac - ev, _c(r + 0.5)))


def spi(ev, pv):
    r = _c(ev / pv)
    return _n(f"By month 6, a bridge was planned to have Rs {pv} crore of work done, but only Rs {ev} crore worth is complete. What is the schedule performance index (SPI)?",
              f"6 মাসের মধ্যে একটা সেতুতে {pv} কোটি টাকার কাজ হওয়ার কথা ছিল, কিন্তু হয়েছে মাত্র {ev} কোটি টাকার। সময়সূচি-দক্ষতা সূচক (এসপিআই) কত?", r,
              f"SPI = EV ÷ PV = {ev} ÷ {pv} = {r:g}. Below 1 means behind schedule.",
              f"এসপিআই = অর্জিত ÷ পরিকল্পিত = {ev} ÷ {pv} = {r:g}। 1-এর নিচে মানে সময়ের পিছনে।",
              (_c(pv / ev), pv - ev, _c(r + 0.5)))


def roas(rev, spend):
    r = _c(rev / spend)
    return _n(f"A precast-concrete supplier spent Rs {spend:,} on online ads that brought Rs {rev:,} in sales. What is the return on ad spend (ROAS)?",
              f"একজন প্রিকাস্ট-কংক্রিট সরবরাহকারী অনলাইন বিজ্ঞাপনে {spend:,} টাকা খরচ করে {rev:,} টাকার বিক্রি পেলেন। বিজ্ঞাপন-খরচে আয় (আরওএএস) কত?", r,
              f"ROAS = sales ÷ ad spend = {rev:,} ÷ {spend:,} = {r:g} - each rupee of ads brought Rs {r:g} of sales.",
              f"আরওএএস = বিক্রি ÷ বিজ্ঞাপন-খরচ = {rev:,} ÷ {spend:,} = {r:g} - বিজ্ঞাপনের প্রতি টাকায় {r:g} টাকার বিক্রি।",
              (_c(spend / rev), _c((rev - spend) / spend), _c(r * 10)), " : 1", " : 1")


def tariff(price, duty):
    r = price + price * duty // 100
    return _n(f"An imported bridge bearing costs Rs {price:,} at the port. A {duty}% import tariff is charged. What is its cost after the tariff?",
              f"একটা আমদানি-করা সেতু-বিয়ারিংয়ের বন্দরে দাম {price:,} টাকা। {duty}% আমদানি-শুল্ক বসে। শুল্কের পরে দাম কত?", r,
              f"Tariff = {price:,} x {duty}% = {price * duty // 100:,}; total = Rs {r:,}. Tariffs make imports dearer, protecting local makers.",
              f"শুল্ক = {price:,} x {duty}% = {price * duty // 100:,}; মোট = {r:,} টাকা। শুল্ক আমদানি দামি করে স্থানীয় নির্মাতাদের রক্ষা করে।",
              (price * duty // 100, price - price * duty // 100, r + price // 10), "", " টাকা", "Rs ")


def export_usd(rs, rate):
    r = _c(rs / rate)
    o = _o(r, _c(rs * rate / 1000), _c(rs / (rate + 10)), _c(r * 2))
    f = lambda x: f"${x:,}" if isinstance(x, int) else f"${x:,.2f}"
    return mcq(f"An Indian firm sells a steel girder for Rs {rs:,}. At $1 = Rs {rate}, what is the price in US dollars?", [f(x) for x in o], 0,
              f"{rs:,} ÷ {rate} = ${r:g}. If the rupee weakens to more rupees per dollar, the same girder looks cheaper abroad.",
              f"একটা ভারতীয় সংস্থা একটা ইস্পাতের গার্ডার {rs:,} টাকায় বেচে। $1 = {rate} টাকা ধরে মার্কিন ডলারে দাম কত?", [f(x) for x in o],
              f"{rs:,} ÷ {rate} = ${r:g}। টাকা দুর্বল হয়ে ডলারপ্রতি বেশি টাকা লাগলে একই গার্ডার বিদেশে সস্তা দেখায়।")


def routes(n):
    p2p = n * (n - 1) // 2
    return _n(f"A logistics firm links {n} cities. How many direct routes are needed to connect every pair of cities point-to-point?",
              f"একটা পরিবহন-সংস্থা {n}টি শহর যুক্ত করে। প্রতিটা জোড়া শহরকে সরাসরি যুক্ত করতে কতগুলো পথ লাগে?", p2p,
              f"n(n - 1) ÷ 2 = {n} x {n - 1} ÷ 2 = {p2p}. A hub-and-spoke network needs only {n - 1} routes through one hub.",
              f"n(n - 1) ÷ 2 = {n} x {n - 1} ÷ 2 = {p2p}। হাব-আর-স্পোক জালে একটা কেন্দ্র দিয়ে মাত্র {n - 1}টি পথ লাগে।",
              (n - 1, n * n, n * (n - 1)), " routes", "টি পথ")


ITEMS = (
    equil(100, 5, 20, 3, "steel rods", "ইস্পাতের রড"), equil(210, 10, 30, 5, "cement bags", "সিমেন্টের বস্তা"),
    equil(90, 4, 10, 6, "bricks", "ইট"), equil(150, 3, 30, 5, "paint tins", "রঙের টিন"),
    queue(1200, 4, 400), queue(1800, 5, 400), queue(900, 3, 450), queue(2400, 6, 450),
    capu(8000, 10000, "A precast factory", "একটা প্রিকাস্ট-কারখানা"), capu(4500, 6000, "A steel fabrication shop", "একটা ইস্পাত-ফ্যাব্রিকেশন কারখানা"),
    capu(1800, 3000, "A bearing workshop", "একটা বিয়ারিং-কারখানা"),
    cpi(40, 50), cpi(60, 48), cpi(90, 90), cpi(25, 20),
    spi(30, 40), spi(45, 50), spi(18, 24), spi(70, 70),
    roas(500000, 50000), roas(240000, 60000), roas(90000, 30000), roas(1200000, 150000),
    tariff(200000, 10), tariff(50000, 20), tariff(800000, 7), tariff(120000, 15),
    export_usd(85000, 85), export_usd(425000, 85), export_usd(166000, 83),
    routes(5), routes(8), routes(10), routes(12),
    equil(120, 2, 20, 3, "timber planks", "কাঠের তক্তা"), equil(300, 6, 60, 4, "scaffold clamps", "ভারার ক্ল্যাম্প"),
    queue(1500, 5, 500), queue(700, 2, 500), capu(9000, 12000, "A rebar bending yard", "একটা রড-বাঁকানোর উঠান"), capu(350, 500, "A girder casting bed", "একটা গার্ডার-ঢালাইয়ের বেড"),
    cpi(36, 40), cpi(55, 44), spi(52, 65), roas(300000, 75000), roas(640000, 80000),
    tariff(450000, 12), tariff(90000, 25), export_usd(249000, 83), export_usd(340000, 85),
    mcq("What does the law of demand say?", ["As price rises, the quantity demanded usually falls", "As price rises, people buy more", "Demand never changes", "Price and demand are unrelated"], 0,
        "Demand curves slope downwards from left to right.",
        "চাহিদার সূত্র কী বলে?", ["দাম বাড়লে চাহিদার পরিমাণ সাধারণত কমে", "দাম বাড়লে মানুষ বেশি কেনে", "চাহিদা কখনো বদলায় না", "দাম আর চাহিদার সম্পর্ক নেই"],
        "চাহিদা-রেখা বাঁ থেকে ডানে নিচের দিকে ঢালু।"),
    mcq("What does the law of supply say?", ["As price rises, producers are willing to supply more", "As price rises, supply falls", "Supply is always fixed", "Supply depends only on weather"], 0,
        "Higher prices make production more profitable.",
        "জোগানের সূত্র কী বলে?", ["দাম বাড়লে উৎপাদকরা বেশি জোগান দিতে চান", "দাম বাড়লে জোগান কমে", "জোগান সবসময় স্থির", "জোগান শুধু আবহাওয়ার উপর নির্ভর করে"],
        "বেশি দামে উৎপাদন বেশি লাভজনক হয়।"),
    mcq("What is the 'equilibrium price' in a market?", ["The price at which quantity demanded equals quantity supplied", "The highest price ever", "A price set by the government only", "The cost of making one item"], 0,
        "At this price there is no shortage and no surplus.",
        "বাজারে 'ভারসাম্য-দাম' কী?", ["যে দামে চাহিদার পরিমাণ জোগানের পরিমাণের সমান", "সর্বকালের সর্বোচ্চ দাম", "শুধু সরকারের ঠিক করা দাম", "একটা জিনিস বানানোর খরচ"],
        "এই দামে ঘাটতিও নেই, উদ্বৃত্তও নেই।"),
    mcq("A huge new highway programme starts and demand for cement rises. What happens to the price of cement in the short run?", ["It rises, as the demand curve shifts right", "It falls", "It stays the same", "Cement becomes free"], 0,
        "Higher prices then encourage cement makers to expand.",
        "একটা বিশাল নতুন মহাসড়ক-কর্মসূচি শুরু হলো আর সিমেন্টের চাহিদা বাড়ল। স্বল্পমেয়াদে সিমেন্টের দামের কী হয়?", ["বাড়ে, কারণ চাহিদা-রেখা ডানে সরে", "কমে", "একই থাকে", "সিমেন্ট বিনামূল্যে হয়"],
        "বেশি দাম তখন সিমেন্ট-নির্মাতাদের উৎপাদন বাড়াতে উৎসাহ দেয়।"),
    mcq("A new steel plant opens and increases supply. What usually happens to the price of steel bars?", ["It falls, as the supply curve shifts right", "It rises", "It doubles", "Steel stops being sold"], 0,
        "More supply at every price pushes the equilibrium price down.",
        "একটা নতুন ইস্পাত-কারখানা চালু হয়ে জোগান বাড়াল। ইস্পাতের রডের দামের সাধারণত কী হয়?", ["কমে, কারণ জোগান-রেখা ডানে সরে", "বাড়ে", "দ্বিগুণ হয়", "ইস্পাত বিক্রি বন্ধ হয়"],
        "প্রতি দামে বেশি জোগান ভারসাম্য-দামকে নামিয়ে দেয়।"),
    mcq("Heavy monsoon floods close river sand quarries for months. What happens to sand prices?", ["They rise because supply falls", "They fall", "They stay exactly the same", "Sand becomes free"], 0,
        "Builders often stockpile before the monsoon for this reason.",
        "প্রবল বর্ষার বন্যায় কয়েক মাস নদীর বালির খাদান বন্ধ থাকে। বালির দামের কী হয়?", ["জোগান কমায় বাড়ে", "কমে", "হুবহু একই থাকে", "বালি বিনামূল্যে হয়"],
        "তাই নির্মাতারা প্রায়ই বর্ষার আগে মজুত করেন।"),
    mcq("What is a 'price ceiling'?", ["A legal maximum price, often set to protect buyers", "A ceiling made of price tags", "The lowest allowed price", "A tax on roofs"], 0,
        "If set below equilibrium, it can cause shortages.",
        "'দামের ঊর্ধ্বসীমা' কী?", ["আইনি সর্বোচ্চ দাম, প্রায়ই ক্রেতাদের রক্ষায় ঠিক করা", "দামের ট্যাগে তৈরি ছাদ", "অনুমোদিত সর্বনিম্ন দাম", "ছাদের উপর কর"],
        "ভারসাম্যের নিচে ঠিক হলে ঘাটতি তৈরি করতে পারে।"),
    mcq("What is a 'price floor', such as a minimum wage?", ["A legal minimum price, set to protect sellers or workers", "The maximum price allowed", "A wooden floor", "A discount"], 0,
        "A minimum wage protects construction workers from very low pay.",
        "ন্যূনতম মজুরির মতো 'দামের নিম্নসীমা' কী?", ["বিক্রেতা বা কর্মীদের রক্ষায় ঠিক করা আইনি সর্বনিম্ন দাম", "অনুমোদিত সর্বোচ্চ দাম", "কাঠের মেঝে", "ছাড়"],
        "ন্যূনতম মজুরি নির্মাণ-শ্রমিকদের খুব কম বেতন থেকে রক্ষা করে।"),
    mcq("If the government sets a price ceiling on cement well below the market price, what is likely?", ["A shortage, as demand exceeds supply at that price", "A large surplus of cement", "No change at all", "Cement quality improves"], 0,
        "Queues, black markets or rationing often follow.",
        "সরকার সিমেন্টের দামের ঊর্ধ্বসীমা বাজারদামের অনেক নিচে বাঁধলে কী হওয়ার সম্ভাবনা?", ["ঘাটতি, কারণ সেই দামে চাহিদা জোগান ছাড়ায়", "সিমেন্টের বড় উদ্বৃত্ত", "কোনো বদল নেই", "সিমেন্টের মান বাড়ে"],
        "প্রায়ই লাইন, কালোবাজার বা রেশনিং আসে।"),
    mcq("What is 'comparative advantage' in trade?", ["A country gains by specialising in what it gives up least to produce, and trading for the rest", "Making everything yourself", "Having the most money", "Trading only with neighbours"], 0,
        "Even if one country is better at everything, both can gain from trade.",
        "বাণিজ্যে 'তুলনামূলক সুবিধা' কী?", ["যা বানাতে সবচেয়ে কম ছাড়তে হয় তাতে বিশেষজ্ঞ হয়ে বাকিটা বাণিজ্যে নিলে দেশ লাভবান হয়", "সব কিছু নিজে বানানো", "সবচেয়ে বেশি টাকা থাকা", "শুধু প্রতিবেশীর সঙ্গে বাণিজ্য"],
        "একটা দেশ সবকিছুতে ভালো হলেও বাণিজ্যে দুজনেই লাভ করতে পারে।"),
    mcq("Why might a government put a tariff on imported steel?", ["To protect local steelmakers and their jobs, even though builders may pay more", "To make imported steel cheaper", "To stop all building", "Because imported steel is always weaker"], 0,
        "Every tariff has winners (local producers) and losers (local buyers).",
        "সরকার আমদানি-করা ইস্পাতে শুল্ক বসাতে পারে কেন?", ["স্থানীয় ইস্পাত-নির্মাতা আর তাদের কর্মসংস্থান রক্ষা করতে, যদিও নির্মাতাদের বেশি দাম দিতে হতে পারে", "আমদানি-করা ইস্পাত সস্তা করতে", "সব নির্মাণ থামাতে", "কারণ আমদানি-করা ইস্পাত সবসময় দুর্বল"],
        "প্রতিটা শুল্কে লাভবান (স্থানীয় উৎপাদক) আর ক্ষতিগ্রস্ত (স্থানীয় ক্রেতা) দুপক্ষই থাকে।"),
    mcq("What is a 'trade deficit'?", ["When a country imports more goods and services than it exports", "When it exports more than it imports", "A shortage of traders", "A tax on trade"], 0,
        "It must be paid for by borrowing or foreign investment.",
        "'বাণিজ্য-ঘাটতি' কী?", ["যখন একটা দেশ রপ্তানির চেয়ে বেশি পণ্য-পরিষেবা আমদানি করে", "যখন আমদানির চেয়ে বেশি রপ্তানি করে", "ব্যবসায়ীর অভাব", "বাণিজ্যের উপর কর"],
        "এর দাম ঋণ বা বিদেশি বিনিয়োগে মেটাতে হয়।"),
    mcq("What is a 'supply shock'?", ["A sudden event that sharply cuts supply, such as a strike, flood or war, pushing prices up", "A shocking advert", "An electric shock from a supply cable", "A sudden fall in demand"], 0,
        "Firms keep backup suppliers and stock to soften supply shocks.",
        "'জোগান-ধাক্কা' কী?", ["হঠাৎ ঘটনা যা জোগান তীব্রভাবে কমায়, যেমন ধর্মঘট, বন্যা বা যুদ্ধ, আর দাম বাড়ায়", "চমকপ্রদ বিজ্ঞাপন", "সরবরাহ-তারে বৈদ্যুতিক শক", "চাহিদায় হঠাৎ পতন"],
        "সংস্থা বিকল্প সরবরাহকারী আর মজুত রেখে জোগান-ধাক্কা নরম করে।"),
    mcq("Why do steel prices often rise when many countries launch big infrastructure programmes at the same time?", ["Global demand for steel jumps faster than steelmakers can expand supply", "Steel gets heavier", "Bridges use no steel", "Steelmakers close"], 0,
        "Builders often lock in prices early with contracts.",
        "অনেক দেশ একসঙ্গে বড় পরিকাঠামো-কর্মসূচি শুরু করলে ইস্পাতের দাম প্রায়ই বাড়ে কেন?", ["ইস্পাত-নির্মাতারা জোগান যত দ্রুত বাড়াতে পারে, বিশ্বব্যাপী চাহিদা তার চেয়ে দ্রুত লাফায়", "ইস্পাত ভারী হয়", "সেতুতে ইস্পাত লাগে না", "ইস্পাত-নির্মাতারা বন্ধ হয়"],
        "নির্মাতারা প্রায়ই চুক্তিতে আগেভাগে দাম বেঁধে নেন।"),
    mcq("What is a 'tender addendum'?", ["An official change to the tender documents, sent to every bidder before bids close", "A late bid", "A bribe", "The winning bid"], 0,
        "Everyone must bid on the same information to keep the contest fair.",
        "'দরপত্র-সংযোজনী' কী?", ["দর জমার শেষ সময়ের আগে প্রত্যেক দরদাতাকে পাঠানো দরপত্র-নথির আনুষ্ঠানিক বদল", "দেরিতে দেওয়া দর", "ঘুষ", "জয়ী দর"],
        "প্রতিযোগিতা ন্যায্য রাখতে সবাইকে একই তথ্যে দর দিতে হয়।"),
    mcq("What happens at a 'pre-bid meeting' for a bridge tender?", ["Bidders ask the client questions, and the answers are shared with all bidders", "The winner is chosen secretly", "Bids are opened early", "Prices are agreed between bidders"], 0,
        "Agreeing prices between bidders would be illegal bid rigging.",
        "সেতু-দরপত্রের 'প্রাক-দর সভায়' কী হয়?", ["দরদাতারা গ্রাহককে প্রশ্ন করেন, আর উত্তর সব দরদাতাকে জানানো হয়", "গোপনে জয়ী বাছা হয়", "আগেভাগে দর খোলা হয়", "দরদাতারা নিজেদের মধ্যে দাম ঠিক করেন"],
        "দরদাতাদের মধ্যে দাম ঠিক করা বেআইনি দরপত্র-কারসাজি।"),
    mcq("Why might public bridge tenders give some preference to locally made materials?", ["To support domestic industry and jobs, while still meeting quality standards", "Local materials are always cheaper", "Imports are illegal", "To make bridges weaker"], 0,
        "Such rules must be clear and published so all bidders know them.",
        "সরকারি সেতু-দরপত্র স্থানীয়ভাবে তৈরি উপাদানে কিছু অগ্রাধিকার দিতে পারে কেন?", ["মানের শর্ত মেনেই দেশীয় শিল্প আর কর্মসংস্থানকে সমর্থন করতে", "স্থানীয় উপাদান সবসময় সস্তা", "আমদানি বেআইনি", "সেতু দুর্বল করতে"],
        "এমন নিয়ম স্পষ্ট আর প্রকাশিত হতে হবে, যাতে সব দরদাতা জানেন।"),
    mcq("A client changes the deck design after work starts. Which document should record the extra cost and time?", ["A variation order agreed by both sides", "A text message", "Nothing - just start", "The original tender only"], 0,
        "Written, agreed changes protect both the client and the contractor.",
        "কাজ শুরুর পরে গ্রাহক পাটাতনের নকশা বদলালেন। বাড়তি খরচ আর সময় কোন নথিতে লেখা উচিত?", ["দুপক্ষের সম্মত পরিবর্তন-আদেশে", "একটা টেক্সট মেসেজে", "কিছুতে না - শুধু শুরু করো", "শুধু মূল দরপত্রে"],
        "লিখিত, সম্মত বদল গ্রাহক আর ঠিকাদার দুজনকেই রক্ষা করে।"),
    mcq("What does 'utilisation' of a crane fleet tell a hire company?", ["The share of available hours the cranes are actually out on hire earning money", "How tall the cranes are", "The colour of the cranes", "The number of drivers"], 0,
        "Idle cranes still cost money in depreciation, insurance and storage.",
        "ক্রেন-বহরের 'ব্যবহার-হার' একটা ভাড়া-সংস্থাকে কী জানায়?", ["উপলব্ধ ঘণ্টার কত অংশে ক্রেনগুলো সত্যিই ভাড়ায় খেটে টাকা আনছে", "ক্রেন কত উঁচু", "ক্রেনের রং", "চালকের সংখ্যা"],
        "অলস ক্রেনেও অবচয়, বিমা আর রাখার খরচ লাগে।"),
    mcq("What is an 'import quota'?", ["A limit on the quantity of a good that can be imported", "A tax on exports", "A shopping list", "A free-trade deal"], 0,
        "Like tariffs, quotas protect local producers.",
        "'আমদানি-কোটা' কী?", ["কোনো পণ্য কতটা আমদানি করা যাবে তার সীমা", "রপ্তানির উপর কর", "কেনাকাটার তালিকা", "মুক্ত-বাণিজ্য চুক্তি"],
        "শুল্কের মতো কোটাও স্থানীয় উৎপাদকদের রক্ষা করে।"),
    mcq("If the rupee weakens against the dollar, what happens for an Indian firm importing bridge cables?", ["The cables cost more in rupees", "The cables cost less", "Nothing changes", "Imports become free"], 0,
        "A weak rupee helps exporters but hurts importers.",
        "ডলারের বিপরীতে টাকা দুর্বল হলে সেতুর তার আমদানিকারী ভারতীয় সংস্থার কী হয়?", ["টাকায় তারের দাম বাড়ে", "দাম কমে", "কিছু বদলায় না", "আমদানি বিনামূল্যে হয়"],
        "দুর্বল টাকা রপ্তানিকারকদের সাহায্য করে, কিন্তু আমদানিকারকদের ক্ষতি করে।"),
    mcq("What is a 'free trade agreement'?", ["A deal between countries to cut or remove tariffs on each other's goods", "Free goods for everyone", "A ban on trade", "A tax on all imports"], 0,
        "It can lower costs for builders but increase competition for local makers.",
        "'মুক্ত-বাণিজ্য চুক্তি' কী?", ["দেশগুলোর মধ্যে পরস্পরের পণ্যে শুল্ক কমানো বা তুলে দেওয়ার চুক্তি", "সবার জন্য বিনামূল্যের পণ্য", "বাণিজ্য নিষিদ্ধ", "সব আমদানিতে কর"],
        "নির্মাতাদের খরচ কমাতে পারে, কিন্তু স্থানীয় নির্মাতাদের প্রতিযোগিতা বাড়ায়।"),
    mcq("What is 'dumping' in international trade?", ["Selling goods abroad below their cost or home price to grab market share", "Throwing waste in the sea", "Selling at a fair price", "Recycling old goods"], 0,
        "Countries may charge anti-dumping duties on cheap steel imports.",
        "আন্তর্জাতিক বাণিজ্যে 'ডাম্পিং' কী?", ["বাজার দখলে বিদেশে খরচ বা দেশের দামের নিচে মাল বেচা", "সমুদ্রে বর্জ্য ফেলা", "ন্যায্য দামে বেচা", "পুরোনো মাল পুনর্ব্যবহার"],
        "সস্তা ইস্পাত-আমদানিতে দেশগুলো ডাম্পিং-বিরোধী শুল্ক বসাতে পারে।"),
    mcq("Why do long queues form at a toll plaza even when utilisation is 'only' 90%?", ["Vehicles arrive randomly, so short bursts exceed capacity and queues build up", "Booths stop working at 90%", "Drivers drive too slowly", "Queues never form below 100%"], 0,
        "Planners aim well below 100% or use electronic tolling.",
        "ব্যবহার-হার 'মাত্র' 90% হলেও টোল-প্লাজায় লম্বা লাইন হয় কেন?", ["যান এলোমেলোভাবে আসে, তাই হঠাৎ ভিড় ক্ষমতা ছাড়ায় আর লাইন জমে", "90%-এ বুথ কাজ বন্ধ করে", "চালকরা খুব ধীরে চালান", "100%-এর নিচে লাইন হয় না"],
        "পরিকল্পনাকারীরা 100%-এর অনেক নিচে রাখেন বা ইলেকট্রনিক টোল ব্যবহার করেন।"),
    mcq("What is a 'bottleneck' in a supply chain or production line?", ["The slowest step, which limits the output of the whole system", "A broken bottle", "The fastest machine", "A type of warehouse"], 0,
        "Improving anything other than the bottleneck does not raise total output.",
        "সরবরাহ-শৃঙ্খল বা উৎপাদন-লাইনে 'বোতলের গলা' কী?", ["সবচেয়ে ধীর ধাপ, যা পুরো ব্যবস্থার উৎপাদন সীমিত করে", "ভাঙা বোতল", "সবচেয়ে দ্রুত যন্ত্র", "এক রকম গুদাম"],
        "বোতলের গলা ছাড়া অন্য কিছু উন্নত করলে মোট উৎপাদন বাড়ে না।"),
    mcq("What is 'earned value' in project management?", ["The budgeted cost of the work actually completed so far", "The money already spent", "The final profit", "The value of the land"], 0,
        "Comparing it with actual cost and planned value shows if a project is over budget or late.",
        "প্রকল্প-ব্যবস্থাপনায় 'অর্জিত মূল্য' কী?", ["এখন পর্যন্ত আসলে শেষ হওয়া কাজের বাজেট-খরচ", "ইতিমধ্যে খরচ হওয়া টাকা", "শেষ লাভ", "জমির মূল্য"],
        "আসল খরচ আর পরিকল্পিত মূল্যের সঙ্গে তুলনা দেখায় প্রকল্প বাজেট ছাড়িয়েছে বা পিছিয়েছে কিনা।"),
    mcq("A project's CPI is 0.8. What does that mean?", ["It is getting only 80 paise of work for every rupee spent - over budget", "It is under budget", "It is ahead of schedule", "It is finished"], 0,
        "Managers investigate why and try to recover.",
        "একটা প্রকল্পের সিপিআই 0.8। মানে কী?", ["খরচ-করা প্রতি টাকায় মাত্র 80 পয়সার কাজ হচ্ছে - বাজেটের বেশি", "বাজেটের নিচে", "সময়ের আগে", "শেষ হয়ে গেছে"],
        "ম্যানেজাররা কারণ খুঁজে ঘাটতি পূরণের চেষ্টা করেন।"),
    mcq("What is a 'risk register' on a bridge project?", ["A list of possible risks with their likelihood, impact, owner and planned response", "A list of workers' names", "The cash register in the canteen", "A list of completed tasks"], 0,
        "It is reviewed regularly as the project moves on.",
        "সেতু-প্রকল্পে 'ঝুঁকি-তালিকা' কী?", ["সম্ভাব্য ঝুঁকির তালিকা, সঙ্গে সম্ভাবনা, প্রভাব, দায়িত্বপ্রাপ্ত আর পরিকল্পিত পদক্ষেপ", "কর্মীদের নামের তালিকা", "ক্যান্টিনের ক্যাশ-রেজিস্টার", "শেষ হওয়া কাজের তালিকা"],
        "প্রকল্প এগোনোর সঙ্গে নিয়মিত পর্যালোচনা হয়।"),
    mcq("A risk has a 10% chance of causing a Rs 50 lakh delay cost. What is its expected cost for the risk register?", ["Rs 5 lakh", "Rs 50 lakh", "Rs 10 lakh", "Rs 0.5 lakh"], 0,
        "Probability x impact = 0.1 x 50 = 5 lakh - useful for setting a contingency budget.",
        "একটা ঝুঁকির 10% সম্ভাবনায় 50 লাখ টাকার দেরির খরচ হতে পারে। ঝুঁকি-তালিকায় এর প্রত্যাশিত খরচ কত?", ["5 লাখ টাকা", "50 লাখ টাকা", "10 লাখ টাকা", "0.5 লাখ টাকা"],
        "সম্ভাবনা x প্রভাব = 0.1 x 50 = 5 লাখ - আপৎকালীন বাজেট ঠিক করতে কাজের।"),
    mcq("What are the four common ways to respond to a project risk?", ["Avoid, reduce, transfer (e.g. insure) or accept it", "Ignore, hide, deny or blame", "Buy, sell, rent or lend", "Plan, paint, pour or pave"], 0,
        "Insurance transfers a risk; a safety barrier reduces it.",
        "প্রকল্পের ঝুঁকি সামলানোর চারটে সাধারণ উপায় কী?", ["এড়ানো, কমানো, হস্তান্তর (যেমন বিমা) বা মেনে নেওয়া", "উপেক্ষা, লুকোনো, অস্বীকার বা দোষারোপ", "কেনা, বেচা, ভাড়া বা ধার", "পরিকল্পনা, রং, ঢালাই বা বাঁধানো"],
        "বিমা ঝুঁকি হস্তান্তর করে; নিরাপত্তা-বেড়া কমায়।"),
    mcq("What is an EPC contract for a highway bridge?", ["Engineering, procurement and construction: one contractor designs, buys and builds, and the government pays", "A contract for electricity only", "The contractor owns the bridge forever", "A contract for painting only"], 0,
        "The government funds it and collects any tolls itself.",
        "মহাসড়ক-সেতুর জন্য ইপিসি চুক্তি কী?", ["প্রকৌশল, সংগ্রহ আর নির্মাণ: একজন ঠিকাদার নকশা, কেনা আর নির্মাণ করেন, সরকার টাকা দেয়", "শুধু বিদ্যুতের চুক্তি", "ঠিকাদার চিরকাল সেতুর মালিক", "শুধু রঙের চুক্তি"],
        "সরকার অর্থ দেয় আর টোল থাকলে নিজেই তোলে।"),
    mcq("What is a BOT (build-operate-transfer) toll bridge?", ["A private firm builds and runs it, collects tolls for an agreed period, then hands it to the government", "The government builds and keeps it", "Users build it themselves", "A bridge for bots"], 0,
        "The firm carries the traffic risk - if few vehicles come, it earns less.",
        "বিওটি (বানাও-চালাও-হস্তান্তর) টোল-সেতু কী?", ["একটা বেসরকারি সংস্থা বানায় ও চালায়, নির্দিষ্ট সময় টোল তোলে, তারপর সরকারকে দেয়", "সরকার বানিয়ে রেখে দেয়", "ব্যবহারকারীরা নিজেরা বানান", "রোবটদের সেতু"],
        "যানবাহনের ঝুঁকি সংস্থার - কম গাড়ি এলে কম আয়।"),
    mcq("India's Hybrid Annuity Model (HAM) for highways is a mix. How does it share costs?", ["The government pays about 40% during construction, and the developer is repaid the rest with interest in fixed annuities", "The developer pays everything forever", "Users pay everything upfront", "Banks own the road"], 0,
        "It reduces the traffic risk that made many BOT projects struggle.",
        "মহাসড়কের জন্য ভারতের হাইব্রিড অ্যানুইটি মডেল (এইচএএম) একটা মিশ্রণ। এটা খরচ কীভাবে ভাগ করে?", ["নির্মাণের সময় সরকার প্রায় 40% দেয়, বাকিটা সুদসহ নির্দিষ্ট কিস্তিতে নির্মাতাকে ফেরত দেয়", "নির্মাতা চিরকাল সব দেন", "ব্যবহারকারীরা আগেই সব দেন", "ব্যাংক রাস্তার মালিক"],
        "অনেক বিওটি প্রকল্প যে যানবাহন-ঝুঁকিতে ভুগেছিল, তা কমায়।"),
    mcq("What is a 'concession period' in a toll-bridge contract?", ["The years during which the operator may collect tolls before handing the bridge back", "A discount for students", "The time to build the bridge only", "The bridge's paint warranty"], 0,
        "It is set so the operator can recover costs and a fair return.",
        "টোল-সেতুর চুক্তিতে 'ছাড়ের মেয়াদ' কী?", ["যে কয়েক বছর পরিচালক টোল তুলতে পারেন, তারপর সেতু ফেরত দেন", "ছাত্রছাত্রীদের ছাড়", "শুধু সেতু বানানোর সময়", "সেতুর রঙের ওয়ারেন্টি"],
        "এমনভাবে ঠিক হয় যাতে পরিচালক খরচ আর ন্যায্য লাভ তুলতে পারেন।"),
    mcq("What does 'value-based pricing' mean for a specialist bridge-inspection firm?", ["Charging according to the value the client gets, such as avoided closures, not just cost plus a margin", "Charging the lowest price possible", "Charging by weight", "Charging the same as everyone"], 0,
        "Expert knowledge that prevents disasters can command a premium.",
        "একটা বিশেষজ্ঞ সেতু-পরিদর্শন সংস্থার জন্য 'মূল্য-ভিত্তিক দাম' মানে কী?", ["শুধু খরচ যোগ মার্জিন নয়, গ্রাহক যে মূল্য পান, যেমন এড়ানো বন্ধ, সেই অনুযায়ী দাম নেওয়া", "সম্ভাব্য সবচেয়ে কম দাম", "ওজন ধরে দাম", "সবার মতো একই দাম"],
        "বিপর্যয় ঠেকানো বিশেষজ্ঞ জ্ঞান বাড়তি দাম পেতে পারে।"),
    mcq("What is BATNA in negotiation?", ["Your best alternative to a negotiated agreement - what you will do if talks fail", "A type of bat", "The final price", "A bank loan"], 0,
        "A strong BATNA, such as another willing supplier, gives you more bargaining power.",
        "দর-কষাকষিতে ব্যাটনা কী?", ["আলোচনায় সমঝোতা না হলে তোমার সেরা বিকল্প - আলোচনা ভাঙলে কী করবে", "এক রকম বাদুড়", "শেষ দাম", "ব্যাংক-ঋণ"],
        "জোরালো ব্যাটনা, যেমন আরেকজন রাজি সরবরাহকারী, দর-কষাকষির ক্ষমতা বাড়ায়।"),
    mcq("Why is a 'win-win' negotiation better with a long-term supplier?", ["Both sides gain, so the relationship lasts and future deals go smoothly", "One side always loses", "It ends the relationship", "It is always more expensive"], 0,
        "Squeezing suppliers too hard can cost quality and reliability.",
        "দীর্ঘমেয়াদি সরবরাহকারীর সঙ্গে 'দুপক্ষেরই জয়' আলোচনা ভালো কেন?", ["দুপক্ষই লাভ করে, তাই সম্পর্ক টেকে আর পরের চুক্তি সহজ হয়", "একপক্ষ সবসময় হারে", "সম্পর্ক শেষ হয়", "সবসময় বেশি দামি"],
        "সরবরাহকারীকে খুব বেশি চাপলে মান আর ভরসা হারাতে হতে পারে।"),
    mcq("What is 'customer relationship management' (CRM) software used for?", ["Keeping records of contacts, enquiries, orders and follow-ups with customers", "Designing bridges", "Paying taxes", "Running cranes"], 0,
        "It helps a sales team never forget a promised quote or call.",
        "'খদ্দের-সম্পর্ক ব্যবস্থাপনা' (সিআরএম) সফটওয়্যার কীসের জন্য ব্যবহার হয়?", ["খদ্দেরদের যোগাযোগ, জিজ্ঞাসা, অর্ডার আর পরের কাজের নথি রাখতে", "সেতুর নকশা", "কর দেওয়া", "ক্রেন চালানো"],
        "বিক্রয়-দল যাতে কখনো প্রতিশ্রুত উদ্ধৃতি বা ফোন ভুলে না যায়।"),
    mcq("What is 'brand equity'?", ["The extra value a well-known, trusted brand name adds to a product", "The share capital of a company", "The cost of a logo", "A legal case"], 0,
        "Builders may pay more for a cement brand they trust.",
        "'ব্র্যান্ড-মূল্য' কী?", ["পরিচিত, ভরসার ব্র্যান্ড-নাম একটা পণ্যে যে বাড়তি মূল্য যোগ করে", "কোম্পানির শেয়ার-মূলধন", "লোগোর খরচ", "একটা মামলা"],
        "নির্মাতারা ভরসার সিমেন্ট-ব্র্যান্ডে বেশি দিতে পারেন।"),
    mcq("What is a 'hub-and-spoke' distribution network?", ["Goods flow from many origins through a central hub, then out to many destinations", "Every town is connected directly to every other", "A bicycle wheel factory", "A network with no centre"], 0,
        "It needs fewer routes, but a problem at the hub affects everything.",
        "'হাব-আর-স্পোক' বণ্টন-জাল কী?", ["অনেক উৎস থেকে মাল একটা কেন্দ্রীয় হাব দিয়ে অনেক গন্তব্যে যায়", "প্রতিটা শহর প্রতিটার সঙ্গে সরাসরি যুক্ত", "সাইকেলের চাকার কারখানা", "কেন্দ্রহীন জাল"],
        "কম পথ লাগে, কিন্তু হাবে সমস্যা হলে সব প্রভাবিত হয়।"),
    mcq("Why do logistics planners care about a single bridge on a key freight corridor?", ["If it closes, long detours raise costs for every shipment along the corridor", "Bridges cost nothing", "Freight never uses bridges", "Detours are always shorter"], 0,
        "Critical bridges get extra monitoring and backup plans.",
        "পরিবহন-পরিকল্পনাকারীরা প্রধান মালবাহী করিডরের একটা সেতু নিয়ে কেন ভাবেন?", ["বন্ধ হলে লম্বা ঘুরপথে করিডরের প্রতিটা চালানের খরচ বাড়ে", "সেতুতে খরচ নেই", "মাল কখনো সেতু দিয়ে যায় না", "ঘুরপথ সবসময় ছোট"],
        "জরুরি সেতুতে বাড়তি নজরদারি আর বিকল্প পরিকল্পনা থাকে।"),
    mcq("What is 'dedicated freight corridor' (DFC) in India?", ["Rail lines built only for goods trains, so freight moves faster and more cheaply", "A road for cars only", "A corridor in an office", "A pipeline for water"], 0,
        "DFCs need many new rail bridges and viaducts.",
        "ভারতে 'নির্দিষ্ট মালবাহী করিডর' (ডিএফসি) কী?", ["শুধু মালগাড়ির জন্য বানানো রেলপথ, তাই মাল দ্রুত আর সস্তায় যায়", "শুধু গাড়ির রাস্তা", "অফিসের বারান্দা", "জলের পাইপলাইন"],
        "ডিএফসি-তে অনেক নতুন রেলসেতু আর উড়ালপথ লাগে।"),
    mcq("What is 'containerisation' and why did it transform trade?", ["Shipping goods in standard steel boxes that move easily between ships, trains and trucks, cutting handling costs", "Putting goods in plastic bags", "Banning large ships", "Using only small boats"], 0,
        "A container can travel from factory to site without being opened.",
        "'কনটেনারায়ন' কী আর কেন বাণিজ্য বদলে দিল?", ["প্রমিত ইস্পাতের বাক্সে মাল পাঠানো, যা জাহাজ, ট্রেন আর ট্রাকে সহজে বদলায়, নাড়াচাড়ার খরচ কমায়", "প্লাস্টিকের ব্যাগে মাল রাখা", "বড় জাহাজ নিষিদ্ধ", "শুধু ছোট নৌকা"],
        "একটা কনটেনার না খুলেই কারখানা থেকে নির্মাণস্থলে যেতে পারে।"),
    mcq("What is a TEU in shipping?", ["A twenty-foot equivalent unit - the standard measure of container capacity", "A type of truck", "A tax on exports", "A crane"], 0,
        "A 40-foot container counts as 2 TEU.",
        "জাহাজ-পরিবহনে টিইইউ কী?", ["বিশ-ফুট সমতুল্য একক - কনটেনার-ক্ষমতার প্রমিত মাপ", "এক রকম ট্রাক", "রপ্তানির উপর কর", "একটা ক্রেন"],
        "40 ফুটের কনটেনার 2 টিইইউ ধরা হয়।"),
    mcq("What is 'demurrage' at a port?", ["A charge for keeping a container or ship longer than the free time allowed", "A port's opening ceremony", "A type of fish", "A discount for fast unloading"], 0,
        "Slow customs paperwork can add big demurrage bills.",
        "বন্দরে 'বিলম্ব-মাশুল' (ডেমারেজ) কী?", ["অনুমোদিত বিনামূল্যের সময়ের বেশি কনটেনার বা জাহাজ রাখার খরচ", "বন্দরের উদ্বোধন", "এক রকম মাছ", "দ্রুত খালাসের ছাড়"],
        "ধীর শুল্ক-কাগজপত্রে বড় বিলম্ব-মাশুল জুড়তে পারে।"),
    mcq("What is 'opportunity cost' for a contractor who takes on a small, low-margin job?", ["The profit lost by not using the same crew and equipment on a better job", "The fuel cost of the job", "The cost of the bid document", "Nothing"], 0,
        "Every 'yes' to one job is a 'no' to another.",
        "ছোট, কম-মার্জিনের কাজ নেওয়া ঠিকাদারের 'সুযোগ-ব্যয়' কী?", ["একই দল আর যন্ত্র ভালো কাজে না লাগিয়ে হারানো লাভ", "কাজের জ্বালানি-খরচ", "দরপত্র-নথির খরচ", "কিছুই না"],
        "একটা কাজে প্রতিটা 'হ্যাঁ' আরেকটায় 'না'।"),
    mcq("What does 'scope creep' mean on a project?", ["The work slowly growing beyond what was agreed, often without extra time or money", "A creeping insect on site", "Finishing early", "Reducing the work"], 0,
        "Variation orders keep scope changes controlled and paid.",
        "প্রকল্পে 'পরিধি-বিস্তার' মানে কী?", ["কাজ ধীরে ধীরে ঠিক করা সীমা ছাড়িয়ে বাড়ে, প্রায়ই বাড়তি সময় বা টাকা ছাড়া", "নির্মাণস্থলে হামাগুড়ি দেওয়া পোকা", "আগে শেষ করা", "কাজ কমানো"],
        "পরিবর্তন-আদেশ পরিধির বদল নিয়ন্ত্রিত আর অর্থপ্রাপ্ত রাখে।"),
    mcq("What is a 'stakeholder' in a bridge project?", ["Anyone affected by or able to affect the project: users, residents, workers, investors, government", "Only the person holding the survey stake", "Only the contractor", "Only the bank"], 0,
        "Engaging stakeholders early avoids conflict later.",
        "সেতু-প্রকল্পে 'অংশীজন' কে?", ["যে কেউ প্রকল্পে প্রভাবিত বা প্রভাব ফেলতে পারেন: ব্যবহারকারী, বাসিন্দা, কর্মী, বিনিয়োগকারী, সরকার", "শুধু জরিপের খুঁটি ধরা মানুষ", "শুধু ঠিকাদার", "শুধু ব্যাংক"],
        "আগেভাগে অংশীজনদের যুক্ত করলে পরে বিরোধ এড়ানো যায়।"),
    mcq("Why do bridge projects hold public consultations?", ["To hear local concerns about routes, noise, land and access before designs are fixed", "To sell tickets", "To delay work on purpose", "Because nobody uses bridges"], 0,
        "Good consultation can improve the design and build trust.",
        "সেতু-প্রকল্প জনশুনানি করে কেন?", ["নকশা চূড়ান্ত হওয়ার আগে পথ, শব্দ, জমি আর যাতায়াত নিয়ে স্থানীয় উদ্বেগ শুনতে", "টিকিট বেচতে", "ইচ্ছে করে কাজে দেরি করতে", "কারণ কেউ সেতু ব্যবহার করে না"],
        "ভালো শুনানি নকশা উন্নত করে আর আস্থা গড়ে।"),
    mcq("What is 'fair compensation' in land acquisition for a bridge approach road?", ["Paying landowners a just price, plus support for resettlement, as the law requires", "Taking land for free", "Paying only in promises", "Ignoring tenants"], 0,
        "India's land acquisition law sets rules for compensation and rehabilitation.",
        "সেতুর সংযোগ-রাস্তার জমি অধিগ্রহণে 'ন্যায্য ক্ষতিপূরণ' কী?", ["আইন অনুযায়ী জমির মালিকদের ন্যায্য দাম আর পুনর্বাসনের সহায়তা দেওয়া", "বিনামূল্যে জমি নেওয়া", "শুধু প্রতিশ্রুতিতে দাম", "ভাড়াটেদের উপেক্ষা"],
        "ভারতের জমি-অধিগ্রহণ আইন ক্ষতিপূরণ আর পুনর্বাসনের নিয়ম ঠিক করে।"),
    mcq("A local cement shop faces a new rival selling the same brand Rs 10 cheaper. Besides cutting price, what can it compete on?", ["Service: credit for regular builders, fast delivery and advice", "Nothing - it must close", "Selling fake cement", "Refusing to sell"], 0,
        "Non-price competition often wins loyal trade customers.",
        "একটা স্থানীয় সিমেন্ট-দোকানের সামনে নতুন প্রতিদ্বন্দ্বী, একই ব্র্যান্ড 10 টাকা কমে বেচে। দাম কমানো ছাড়া কীসে প্রতিযোগিতা করা যায়?", ["পরিষেবা: নিয়মিত নির্মাতাদের ধার, দ্রুত ডেলিভারি আর পরামর্শ", "কিছুতে না - বন্ধ করতেই হবে", "নকল সিমেন্ট বেচে", "বেচতে অস্বীকার করে"],
        "দাম-ছাড়া প্রতিযোগিতা প্রায়ই অনুগত ব্যবসায়ী খদ্দের জেতে।"),
)
