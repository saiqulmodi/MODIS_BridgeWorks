"""Class 12 - Commercials (Chief Engineer): earned value (CPI, SPI, estimate at completion), the
economic order quantity, reorder points, Little's law, learning curves, exponential smoothing and
moving averages, transit-mixer fleet sizing, float, quality-and-cost based selection, GST, stock
turnover, containers and freight, liquidated-damage caps, running-bill deductions, and the
contract models (EPC, HAM, TOT) and dispute tools used on India's large bridges."""
import math

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


def cpi(ev, ac, what_en, what_bn):
    r = _c(ev / ac)
    state_en = "under budget" if r > 1 else "over budget"
    state_bn = "বাজেটের নিচে" if r > 1 else "বাজেটের বেশি খরচে"
    return _n(f"On {what_en}, the work done so far is worth Rs {ev} crore of the budget (earned value), but it has actually cost Rs {ac} crore. What is the cost performance index (CPI)?",
              f"{what_bn} এ পর্যন্ত করা কাজের বাজেট-মূল্য (অর্জিত মূল্য) {ev} কোটি টাকা, কিন্তু আসলে খরচ হয়েছে {ac} কোটি টাকা। খরচ-কার্যকারিতা সূচক কত?", r,
              f"CPI = EV ÷ AC = {ev} ÷ {ac} = {_f(r)}, so the job is running {state_en}.",
              f"খরচ-সূচক = অর্জিত মূল্য ÷ আসল খরচ = {ev} ÷ {ac} = {_f(r)}, তাই কাজ চলছে {state_bn}।",
              (_c(ac / ev), ev - ac, _c(r + 0.15)))


def spi(ev, pv, what_en, what_bn):
    r = _c(ev / pv)
    state_en = "ahead of schedule" if r > 1 else "behind schedule"
    state_bn = "সময়সূচির আগে" if r > 1 else "সময়সূচির পিছনে"
    return _n(f"By today {what_en} planned to finish work worth Rs {pv} crore, but has finished work worth Rs {ev} crore. What is the schedule performance index (SPI)?",
              f"আজকের মধ্যে {what_bn} {pv} কোটি টাকার কাজ শেষ করার কথা ছিল, কিন্তু শেষ হয়েছে {ev} কোটি টাকার কাজ। সময়সূচি-কার্যকারিতা সূচক কত?", r,
              f"SPI = EV ÷ PV = {ev} ÷ {pv} = {_f(r)}, so it is {state_en}.",
              f"সময়-সূচক = অর্জিত মূল্য ÷ পরিকল্পিত মূল্য = {ev} ÷ {pv} = {_f(r)}, তাই কাজ {state_bn}।",
              (_c(pv / ev), ev - pv, _c(r + 0.15)))


def eac(bac, ev, ac):
    r = _c(bac * ac / ev)
    return _n(f"A bridge has a total budget of Rs {bac} crore. So far it has earned Rs {ev} crore of value while spending Rs {ac} crore. If this cost efficiency continues, what is the estimate at completion?",
              f"একটা সেতুর মোট বাজেট {bac} কোটি টাকা। এ পর্যন্ত {ac} কোটি টাকা খরচে {ev} কোটি টাকার মূল্য অর্জিত হয়েছে। এই খরচ-দক্ষতা চললে শেষ হওয়ার সময় আনুমানিক মোট খরচ কত?", r,
              f"CPI = {ev} ÷ {ac} = {_f(_c(ev / ac))}; EAC = BAC ÷ CPI = {bac} ÷ {_f(_c(ev / ac))} ≈ Rs {_f(r)} crore.",
              f"খরচ-সূচক = {ev} ÷ {ac} = {_f(_c(ev / ac))}; আনুমানিক মোট = বাজেট ÷ সূচক = {bac} ÷ {_f(_c(ev / ac))} ≈ {_f(r)} কোটি টাকা।",
              (bac, bac + ac - ev, _c(bac * ev / ac)), "Rs ", " crore", " কোটি টাকা")


def eoq(d, s, h, item_en, item_bn):
    r = round(math.sqrt(2 * d * s / h))
    return _n(f"A precast yard uses {d:,} {item_en} a year. Each order costs Rs {s} to place and holding one costs Rs {h} a year. What is the economic order quantity?",
              f"একটা প্রিকাস্ট-চত্বরে বছরে {d:,}টি {item_bn} লাগে। প্রতিটি অর্ডার দিতে খরচ {s} টাকা আর একটি মজুত রাখতে বছরে {h} টাকা। অর্থনৈতিক অর্ডার-পরিমাণ কত?", r,
              f"EOQ = √(2DS ÷ H) = √(2 x {d:,} x {s} ÷ {h}) = {r:,}. Here ordering and holding costs balance.",
              f"অর্থনৈতিক অর্ডার = √(2DS ÷ H) = √(2 x {d:,} x {s} ÷ {h}) = {r:,}। এখানে অর্ডার আর মজুত-খরচ সমান হয়।",
              (round(math.sqrt(d * s / h)), round(r / 2), round(r * 1.5)))


def rop(daily, lead, ss, item_en, item_bn):
    r = daily * lead + ss
    return _n(f"A site uses {daily} {item_en} a day. The supplier takes {lead} days to deliver, and the planner keeps {ss} as safety stock. At what stock level should a new order be placed?",
              f"একটা সাইটে দিনে {daily} {item_bn} লাগে। সরবরাহকারী {lead} দিনে পৌঁছে দেন, আর পরিকল্পক {ss} নিরাপত্তা-মজুত রাখেন। মজুত কত হলে নতুন অর্ডার দেওয়া উচিত?", r,
              f"Reorder point = daily use x lead time + safety stock = {daily} x {lead} + {ss} = {r}.",
              f"পুনঃঅর্ডার-বিন্দু = দৈনিক ব্যবহার x সরবরাহ-সময় + নিরাপত্তা-মজুত = {daily} x {lead} + {ss} = {r}।",
              (daily * lead, daily * lead - ss, ss + lead), "", f" {item_en}", f" {item_bn}")


def little(lam, w, where_en, where_bn):
    r = _c(lam * w / 60)
    return _n(f"Trucks arrive at {where_en} at {lam} an hour and each spends {w} minutes there on average. By Little's law, how many trucks are there at any moment on average?",
              f"{where_bn} ঘণ্টায় {lam}টি ট্রাক আসে আর প্রতিটি গড়ে {w} মিনিট থাকে। লিটলের সূত্রে যেকোনো মুহূর্তে গড়ে কতগুলি ট্রাক সেখানে থাকে?", r,
              f"L = λW = {lam} per hour x {w}/60 hour = {_f(r)} trucks. Halve the time and you halve the crowd.",
              f"L = λW = ঘণ্টায় {lam} x {w}/60 ঘণ্টা = {_f(r)}টি ট্রাক। সময় অর্ধেক করলে ভিড়ও অর্ধেক।",
              (lam * w, _c(lam / w), w))


def learning(t1, rate, n, what_en, what_bn):
    k = int(math.log2(n))
    r = _c(t1 * (rate / 100) ** k)
    return _n(f"The first {what_en} takes {t1} hours. The crew follows {'an' if str(rate).startswith('8') else 'a'} {rate}% learning curve (each doubling of output cuts the time per unit to {rate}%). How long does unit number {n} take?",
              f"প্রথম {what_bn} লাগে {t1} ঘণ্টা। দল {rate}% শেখার রেখা মেনে চলে (উৎপাদন প্রতিবার দ্বিগুণ হলে প্রতি এককের সময় {rate}% হয়)। {n} নম্বর এককে কত সময় লাগে?", r,
              f"Unit {n} is {k} doublings from unit 1: {t1} x {rate / 100:g}^{k} = {_f(r)} hours.",
              f"{n} নম্বর একক প্রথমটি থেকে {k}বার দ্বিগুণ: {t1} x {rate / 100:g}^{k} = {_f(r)} ঘণ্টা।",
              (_c(t1 * rate / 100), _c(t1 * (1 - (1 - rate / 100) * k) * 0.97), t1), "", " hours", " ঘণ্টা")


def smooth(f, a, alpha, item_en, item_bn):
    r = _c(f + alpha * (a - f))
    return _n(f"Last month's forecast for {item_en} was {f:,} but actual use was {a:,}. With exponential smoothing and α = {alpha}, what is the next forecast?",
              f"গত মাসে {item_bn} পূর্বাভাস ছিল {f:,}, কিন্তু আসল ব্যবহার {a:,}। α = {alpha} দিয়ে সূচকীয় মসৃণকরণে পরের পূর্বাভাস কত?", r,
              f"New forecast = F + α(A - F) = {f:,} + {alpha} x ({a:,} - {f:,}) = {_f(r)}.",
              f"নতুন পূর্বাভাস = F + α(A - F) = {f:,} + {alpha} x ({a:,} - {f:,}) = {_f(r)}।",
              (a, f, _c(a - alpha * (a - f))))


def mavg(v, item_en, item_bn):
    r = _c(sum(v) / 3)
    a, b, c = v
    return _n(f"A store used {a}, {b} and {c} {item_en} in the last three months. What is the three-month moving-average forecast for next month?",
              f"একটা গুদামে গত তিন মাসে {a}, {b} আর {c} {item_bn} লেগেছে। পরের মাসের তিন-মাসি চলমান-গড় পূর্বাভাস কত?", r,
              f"({a} + {b} + {c}) ÷ 3 = {_f(r)}.",
              f"({a} + {b} + {c}) ÷ 3 = {_f(r)}।",
              (c, a + b + c, max(v) + 5))


def mixers(rate, cap, cycle):
    per = cap * 60 / cycle
    x = rate / per
    r = math.ceil(x - 1e-9)
    return _n(f"A deck pour needs {rate} m³ of concrete an hour. Each transit mixer carries {cap} m³ and a round trip takes {cycle} minutes. How many mixers are needed?",
              f"পাটাতন ঢালাইয়ে ঘণ্টায় {rate} ঘনমিটার কংক্রিট লাগে। প্রতিটি ট্রানজিট-মিক্সার {cap} ঘনমিটার বয় আর এক চক্কর লাগে {cycle} মিনিট। কতগুলি মিক্সার লাগবে?", r,
              f"One mixer delivers {cap} x 60/{cycle} = {_f(_c(per))} m³ an hour; {rate} ÷ {_f(_c(per))} = {_f(_c(x))}, rounded up to {r} - a pour must never stop for want of a truck.",
              f"একটা মিক্সার ঘণ্টায় {cap} x 60/{cycle} = {_f(_c(per))} ঘনমিটার দেয়; {rate} ÷ {_f(_c(per))} = {_f(_c(x))}, উপরে তুলে {r} — ট্রাকের অভাবে ঢালাই কখনো থামানো চলে না।",
              (math.floor(x), math.ceil(rate / cap), r + 3))


def tfloat(es, dur, lf, task_en, task_bn):
    r = lf - (es + dur)
    return _n(f"The task '{task_en}' can start on day {es} at the earliest, lasts {dur} days, and must finish by day {lf} at the latest. What is its total float?",
              f"'{task_bn}' কাজটি সবচেয়ে আগে {es} নম্বর দিনে শুরু হতে পারে, চলে {dur} দিন, আর সবচেয়ে দেরিতে {lf} নম্বর দিনের মধ্যে শেষ করতে হবে। এর মোট ভাসমান সময় কত?", r,
              f"Float = latest finish - earliest finish = {lf} - ({es} + {dur}) = {r} days." + (" Zero float means it is on the critical path." if r == 0 else ""),
              f"ভাসমান সময় = সবচেয়ে দেরির শেষ - সবচেয়ে আগের শেষ = {lf} - ({es} + {dur}) = {r} দিন।" + (" শূন্য মানে কাজটি জটিল পথে আছে।" if r == 0 else ""),
              (lf - es, dur + 2, lf - dur), "", " days", " দিন")


def qcbs(t, price, low):
    r = _c(0.7 * t + 0.3 * 100 * low / price)
    return _n(f"A bridge-design consultant scores {t}/100 on the technical bid and quotes Rs {price} lakh; the lowest quote is Rs {low} lakh. Under 70:30 QCBS, what is the combined score?",
              f"একজন সেতু-নকশা পরামর্শদাতা প্রযুক্তিগত দরে {t}/100 পান আর {price} লাখ টাকা দর দেন; সর্বনিম্ন দর {low} লাখ টাকা। ৭০:৩০ গুণমান-ও-খরচ ভিত্তিক বাছাইয়ে সম্মিলিত নম্বর কত?", r,
              f"Financial score = 100 x {low}/{price} = {_f(_c(100 * low / price))}; combined = 0.7 x {t} + 0.3 x {_f(_c(100 * low / price))} = {_f(r)}.",
              f"আর্থিক নম্বর = 100 x {low}/{price} = {_f(_c(100 * low / price))}; সম্মিলিত = 0.7 x {t} + 0.3 x {_f(_c(100 * low / price))} = {_f(r)}।",
              (_c((t + 100 * low / price) / 2), _c(0.3 * t + 0.7 * 100 * low / price), t))


def gst(sale, inputs):
    out = _c(sale * 0.18)
    r = _c(out - inputs)
    return _n(f"A fabricator bills Rs {sale} lakh for bridge girders plus 18% GST, and paid Rs {inputs} lakh of GST on the steel and paint it bought. How much GST must it pay the government in cash?",
              f"একজন নির্মাতা সেতুর গার্ডারের জন্য {sale} লাখ টাকা আর তার উপর ১৮% জিএসটি বিল করেন, আর কেনা ইস্পাত-রঙে {inputs} লাখ টাকা জিএসটি দিয়েছেন। সরকারকে নগদে কত জিএসটি দিতে হবে?", r,
              f"Output GST = 18% x {sale} = {_f(out)}; minus input tax credit {inputs} = Rs {_f(r)} lakh.",
              f"বিক্রির জিএসটি = ১৮% x {sale} = {_f(out)}; বাদ উপকরণ-কর ছাড় {inputs} = {_f(r)} লাখ টাকা।",
              (out, _c(out + inputs), sale - inputs), "Rs ", " lakh", " লাখ টাকা")


def turnover(cogs, inv):
    r = _c(cogs / inv)
    return _n(f"A bridge-parts supplier's cost of goods sold is Rs {cogs} crore a year and its average stock is worth Rs {inv} crore. What is its inventory turnover?",
              f"একজন সেতু-যন্ত্রাংশ সরবরাহকারীর বছরে বিক্রীত পণ্যের খরচ {cogs} কোটি টাকা, আর গড় মজুতের মূল্য {inv} কোটি টাকা। মজুত-আবর্তন কত?", r,
              f"Turnover = {cogs} ÷ {inv} = {_f(r)} times a year, so stock is held about {_f(_c(365 / r))} days on average.",
              f"আবর্তন = {cogs} ÷ {inv} = বছরে {_f(r)} বার, তাই মজুত গড়ে প্রায় {_f(_c(365 / r))} দিন থাকে।",
              (_c(inv / cogs), _c(365 / r), cogs - inv), "", " times", " বার")


def containers(t, limit, item_en, item_bn):
    r = math.ceil(t / limit)
    return _n(f"{t} tonnes of {item_en} must be shipped, and each container may legally carry at most {limit} tonnes. How many containers are needed?",
              f"{t} টন {item_bn} পাঠাতে হবে, আর প্রতিটি কন্টেনারে আইনত সর্বোচ্চ {limit} টন বহন করা যায়। কতগুলি কন্টেনার লাগবে?", r,
              f"{t} ÷ {limit} = {_f(_c(t / limit))}, rounded up to {r} - you cannot ship part of a load without a container for it.",
              f"{t} ÷ {limit} = {_f(_c(t / limit))}, উপরে তুলে {r} — বোঝার কিছু অংশও কন্টেনার ছাড়া পাঠানো যায় না।",
              (math.floor(t / limit), math.ceil(t / 20) if math.ceil(t / 20) != r else r + 2, r + 1))


def freight(t, km, rate):
    r = round(t * km * rate)
    return _n(f"Moving {t} tonnes of girders {km} km by rail costs Rs {rate} per tonne-km. What is the freight bill?",
              f"রেলে {t} টন গার্ডার {km} কিলোমিটার নিতে প্রতি টন-কিলোমিটারে {rate} টাকা লাগে। মাশুলের বিল কত?", r,
              f"Freight = tonnes x km x rate = {t} x {km} x {rate} = Rs {r:,}.",
              f"মাশুল = টন x কিলোমিটার x হার = {t} x {km} x {rate} = {r:,} টাকা।",
              (t * km, round(km * rate), round(r / 10)), "Rs ", "", " টাকা")


def ld(value, days):
    raw = _c(value * days * 0.0005)
    cap = _c(value * 0.1)
    r = min(raw, cap)
    capped_en = f" The cap of 10% (Rs {_f(cap)} crore) applies." if raw > cap else f" This is below the 10% cap of Rs {_f(cap)} crore."
    capped_bn = f" ১০% সীমা ({_f(cap)} কোটি টাকা) প্রযোজ্য।" if raw > cap else f" এটি ১০% সীমা {_f(cap)} কোটি টাকার নিচে।"
    return _n(f"A Rs {value} crore bridge is finished {days} days late. Liquidated damages are 0.05% of the contract value per day, capped at 10%. How much does the contractor pay?",
              f"{value} কোটি টাকার একটা সেতু {days} দিন দেরিতে শেষ হল। নির্ধারিত ক্ষতিপূরণ প্রতিদিন চুক্তিমূল্যের ০.০৫%, সর্বোচ্চ ১০%। ঠিকাদার কত দেবেন?", r,
              f"{days} x 0.05% x {value} = Rs {_f(raw)} crore.{capped_en}",
              f"{days} x 0.05% x {value} = {_f(raw)} কোটি টাকা।{capped_bn}",
              (raw if raw != r else _c(r * 1.5), cap if cap != r else _c(r / 2), _c(value * days * 0.005)), "Rs ", " crore", " কোটি টাকা")


def netbill(b):
    r = _c(b * 0.83)
    return _n(f"A contractor's running bill is Rs {b} lakh. The owner deducts 5% retention, 10% to recover the mobilisation advance and 2% TDS. How much is actually paid?",
              f"ঠিকাদারের চলতি বিল {b} লাখ টাকা। মালিক ৫% আটক টাকা, সংগঠন-অগ্রিম ফেরতের জন্য ১০% আর ২% উৎসে কর কাটেন। আসলে কত দেওয়া হয়?", r,
              f"Deductions = 5% + 10% + 2% = 17%; paid = {b} x 0.83 = Rs {_f(r)} lakh. Contractors must plan cash for this gap.",
              f"কাটা = ৫% + ১০% + ২% = ১৭%; দেওয়া = {b} x 0.83 = {_f(r)} লাখ টাকা। এই ফারাকের জন্য ঠিকাদারকে নগদ পরিকল্পনা করতে হয়।",
              (_c(b * 0.95), _c(b * 0.9), _c(b * 0.98)), "Rs ", " lakh", " লাখ টাকা")


ITEMS = (
    cpi(40, 50, "a river bridge", "একটা নদী-সেতুতে"), cpi(90, 75, "a flyover", "একটা উড়ালপুলে"),
    cpi(60, 64, "a rail overbridge", "একটা রেল-উপরি সেতুতে"), cpi(77, 70, "a sea-link package", "একটা সমুদ্র-সংযোগ প্যাকেজে"),
    spi(72, 80, "a viaduct contractor", "একজন উড়ালপথ-ঠিকাদারের"), spi(55, 50, "a footbridge team", "একটা পায়ে-চলা সেতুর দলের"),
    spi(30, 40, "a pier-foundation crew", "একটা স্তম্ভ-ভিত্তি দলের"), spi(84, 70, "a girder-launching gang", "একটা গার্ডার-বসানো দলের"),
    eac(200, 80, 100), eac(300, 90, 100), eac(150, 60, 50), eac(500, 200, 250),
    eoq(12000, 500, 12, "bags of cement", "সিমেন্টের বস্তা"), eoq(7200, 400, 16, "bearing pads", "বিয়ারিং-প্যাড"),
    eoq(4800, 600, 4, "steel couplers", "ইস্পাত-কাপলার"), eoq(20000, 250, 40, "anchor bolts", "অ্যাঙ্কর-বোল্ট"),
    rop(40, 7, 60, "tonnes of rebar", "টন রড"), rop(25, 10, 50, "drums of curing compound", "ড্রাম কিওরিং-যৌগ"),
    rop(120, 3, 100, "bags of grout", "বস্তা গ্রাউট"), rop(8, 14, 30, "elastomeric pads", "রাবার-প্যাড"),
    little(60, 5, "a batching-plant gate", "একটা ব্যাচিং-প্ল্যান্টের ফটকে"), little(36, 20, "a steel-yard weighbridge", "একটা ইস্পাত-চত্বরের ওজন-সেতুতে"),
    little(20, 9, "a toll lane for heavy vehicles", "ভারী যানের একটা টোল-লেনে"), little(30, 12, "a site washing bay", "সাইটের একটা ধোয়ার জায়গায়"),
    learning(100, 80, 4, "precast deck segment", "প্রিকাস্ট পাটাতন-খণ্ডে"), learning(200, 90, 8, "steel box-girder unit", "ইস্পাত বাক্স-গার্ডার এককে"),
    learning(60, 85, 4, "pier-cap cage", "স্তম্ভ-মাথার খাঁচায়"), learning(80, 75, 8, "parapet panel set", "রেলিং-প্যানেলের সেটে"),
    smooth(500, 600, 0.2, "bags of cement", "সিমেন্টের বস্তার"), smooth(80, 60, 0.3, "welding rods (boxes)", "ঝালাই-রডের (বাক্স)"),
    smooth(1200, 1500, 0.4, "litres of diesel", "লিটার ডিজেলের"), smooth(45, 50, 0.5, "safety harnesses", "নিরাপত্তা-বন্ধনীর"),
    mavg((30, 36, 42), "tonnes of cable", "টন কেবল"), mavg((120, 90, 105), "anchor plates", "অ্যাঙ্কর-প্লেট"),
    mavg((14, 18, 25), "expansion joints", "প্রসারণ-জোড়"), mavg((200, 260, 230), "drums of paint", "ড্রাম রং"),
    mixers(60, 6, 45), mixers(90, 8, 60), mixers(40, 7, 90), mixers(120, 9, 40),
    tfloat(10, 6, 20, "lay drainage pipes", "নিকাশি-পাইপ বসানো"), tfloat(25, 10, 35, "cast pier caps", "স্তম্ভ-মাথা ঢালাই"),
    tfloat(4, 3, 12, "paint handrails", "রেলিং রং করা"), tfloat(30, 12, 50, "build approach ramps", "সংযোগ-ঢাল বানানো"),
    qcbs(80, 120, 100), qcbs(90, 150, 120), qcbs(70, 100, 100), qcbs(85, 110, 99),
    gst(50, 5), gst(120, 15), gst(80, 10), gst(200, 22),
    turnover(120, 15), turnover(90, 18), turnover(240, 20), turnover(60, 24),
    containers(130, 26, "bridge bearings", "সেতু-বিয়ারিং"), containers(200, 24, "cable strand coils", "কেবল-তারের কুণ্ডলী"),
    containers(75, 21, "expansion-joint modules", "প্রসারণ-জোড়ের মডিউল"), containers(310, 25, "steel couplers", "ইস্পাত-কাপলার"),
    freight(200, 450, 2.5), freight(80, 1200, 1.8), freight(500, 300, 3), freight(150, 800, 1.2),
    ld(200, 60), ld(100, 250), ld(50, 400), ld(300, 120),
    netbill(100), netbill(240), netbill(75), netbill(180),

    mcq("A bridge project reports CPI 0.85 and SPI 1.05. What does this tell the project manager?", ["It is slightly ahead of schedule but spending more than planned for the work done", "It is behind schedule and under budget", "It is perfectly on track", "It has already finished"], 0,
        "CPI below 1 means overspending; SPI above 1 means faster than planned - perhaps overtime is buying speed.",
        "একটা সেতু-প্রকল্পের খরচ-সূচক ০.৮৫ আর সময়-সূচক ১.০৫। এতে প্রকল্প-ব্যবস্থাপক কী বোঝেন?", ["কাজ সময়সূচির একটু আগে, কিন্তু করা কাজের জন্য পরিকল্পনার চেয়ে বেশি খরচ হচ্ছে", "কাজ পিছিয়ে আর বাজেটের নিচে", "সব একদম ঠিকঠাক", "কাজ শেষ হয়ে গেছে"],
        "খরচ-সূচক ১-এর কম মানে বাড়তি খরচ; সময়-সূচক ১-এর বেশি মানে পরিকল্পনার চেয়ে দ্রুত — হয়তো ওভারটাইম দিয়ে গতি কেনা হচ্ছে।"),
    mcq("Why does a bridge planner watch tasks with zero total float most closely?", ["Any delay to them delays the whole bridge's completion date", "They are the cheapest tasks", "They can be skipped", "They always finish early"], 0,
        "Zero-float tasks form the critical path; a day lost there is a day lost at handover.",
        "সেতু-পরিকল্পক শূন্য ভাসমান-সময়ের কাজগুলিতে সবচেয়ে বেশি নজর রাখেন কেন?", ["এগুলিতে যেকোনো দেরি পুরো সেতুর শেষের তারিখ পিছিয়ে দেয়", "এগুলি সবচেয়ে সস্তা কাজ", "এগুলি বাদ দেওয়া যায়", "এগুলি সবসময় আগে শেষ হয়"],
        "শূন্য-ভাসমান কাজ মিলে জটিল পথ; সেখানে একদিন গেলে হস্তান্তরেও একদিন পিছোয়।"),
    mcq("Why might a contractor order cement in batches much larger than the economic order quantity?", ["A bulk discount or a risk of supply shortages can outweigh the extra holding cost", "EOQ is always wrong", "Larger batches never cost anything to store", "Cement improves with age"], 0,
        "EOQ assumes a fixed price and reliable supply; real decisions also weigh discounts and the cost of running out.",
        "ঠিকাদার অর্থনৈতিক অর্ডার-পরিমাণের চেয়ে অনেক বড় ব্যাচে সিমেন্ট অর্ডার দিতে পারেন কেন?", ["বড় অর্ডারের ছাড় বা জোগানে টান পড়ার ঝুঁকি বাড়তি মজুত-খরচকে ছাপিয়ে যেতে পারে", "অর্থনৈতিক অর্ডার সবসময় ভুল", "বড় ব্যাচ রাখতে কোনো খরচ নেই", "পুরনো হলে সিমেন্ট ভালো হয়"],
        "অর্থনৈতিক অর্ডার স্থির দাম আর নির্ভরযোগ্য জোগান ধরে নেয়; বাস্তব সিদ্ধান্তে ছাড় আর মাল ফুরোনোর খরচও ধরতে হয়।"),
    mcq("How does Little's law help the manager of a congested toll plaza?", ["It links arrival rate, time spent and queue size, so cutting service time shrinks the queue", "It sets the legal toll price", "It counts the toll booths", "It predicts the weather"], 0,
        "L = λW: with arrivals fixed, halving the time each vehicle spends halves the number waiting - hence FASTag lanes.",
        "যানজটে ভরা টোল-প্লাজার ব্যবস্থাপককে লিটলের সূত্র কীভাবে সাহায্য করে?", ["এটি আগমন-হার, ব্যয়িত সময় আর লাইনের আকার জোড়ে, তাই পরিষেবা-সময় কমালে লাইন ছোট হয়", "এটি আইনি টোল-দাম ঠিক করে", "এটি টোল-বুথ গোনে", "এটি আবহাওয়ার পূর্বাভাস দেয়"],
        "L = λW: আগমন স্থির থাকলে প্রতিটি যানের সময় অর্ধেক করলে অপেক্ষমাণ সংখ্যাও অর্ধেক — তাই ফাস্ট্যাগ লেন।"),
    mcq("Why does the eighth identical precast segment take far less time than the first?", ["The crew learns: under a learning curve each doubling of output cuts time per unit by a fixed share", "Later segments are smaller", "The concrete sets faster at night", "Inspectors stop checking"], 0,
        "Practice, better jigs and smoother teamwork all add up - planners use this to price repetitive work.",
        "অষ্টম একই রকম প্রিকাস্ট খণ্ডে প্রথমটির চেয়ে অনেক কম সময় লাগে কেন?", ["দল শেখে: শেখার রেখায় উৎপাদন প্রতিবার দ্বিগুণ হলে প্রতি এককের সময় নির্দিষ্ট ভাগে কমে", "পরের খণ্ডগুলি ছোট", "রাতে কংক্রিট দ্রুত জমে", "পরিদর্শকেরা দেখা বন্ধ করেন"],
        "অনুশীলন, ভালো ছাঁচ আর মসৃণ দলগত কাজ মিলে সময় কমে — পরিকল্পকেরা পুনরাবৃত্ত কাজের দাম ঠিক করতে এটি ব্যবহার করেন।"),
    mcq("Steel demand on a project suddenly starts changing quickly. Why might the planner raise the smoothing constant α?", ["A higher α gives recent data more weight, so the forecast reacts faster", "A higher α ignores recent data", "α only affects the colour of the chart", "Raising α lowers steel prices"], 0,
        "Low α suits stable demand; high α tracks fast change but also follows random noise more.",
        "প্রকল্পে ইস্পাতের চাহিদা হঠাৎ দ্রুত বদলাতে শুরু করেছে। পরিকল্পক মসৃণকরণ-ধ্রুবক α বাড়াতে পারেন কেন?", ["বেশি α সাম্প্রতিক তথ্যকে বেশি গুরুত্ব দেয়, তাই পূর্বাভাস দ্রুত সাড়া দেয়", "বেশি α সাম্প্রতিক তথ্য উপেক্ষা করে", "α শুধু চার্টের রং বদলায়", "α বাড়ালে ইস্পাতের দাম কমে"],
        "কম α স্থির চাহিদায় মানায়; বেশি α দ্রুত বদল ধরে, কিন্তু এলোমেলো ওঠানামাও বেশি অনুসরণ করে।"),
    mcq("What is quality and cost based selection (QCBS) used for in Indian infrastructure?", ["Choosing consultants by combining a weighted technical score with a weighted price score", "Choosing the cheapest steel only", "Ranking bridges by beauty", "Selecting workers by height"], 0,
        "A typical 70:30 or 80:20 weighting stops a weak but cheap design firm from winning.",
        "ভারতের পরিকাঠামোয় গুণমান-ও-খরচ ভিত্তিক বাছাই কীসের জন্য ব্যবহার হয়?", ["প্রযুক্তিগত নম্বর আর দামের নম্বর ওজন দিয়ে মিলিয়ে পরামর্শদাতা বাছাই", "শুধু সবচেয়ে সস্তা ইস্পাত বাছা", "সৌন্দর্য অনুযায়ী সেতু সাজানো", "উচ্চতা দেখে কর্মী বাছা"],
        "সাধারণ ৭০:৩০ বা ৮০:২০ ওজন দুর্বল কিন্তু সস্তা নকশা-সংস্থাকে জিততে দেয় না।"),
    mcq("Why is hiring a bridge design consultant purely on the lowest fee risky?", ["Design quality drives construction and life-cycle costs far more than the design fee itself", "Low fees are illegal", "Cheap consultants work faster", "Design has no effect on cost"], 0,
        "A design fee is often 1-3% of project cost; a poor design can waste far more than that in steel, delays and repairs.",
        "শুধু সবচেয়ে কম ফি দেখে সেতু-নকশা পরামর্শদাতা নিয়োগ ঝুঁকিপূর্ণ কেন?", ["নকশার মানই নির্মাণ আর জীবনচক্র-খরচকে নকশা-ফির চেয়ে অনেক বেশি প্রভাবিত করে", "কম ফি বেআইনি", "সস্তা পরামর্শদাতা দ্রুত কাজ করেন", "নকশার খরচে কোনো প্রভাব নেই"],
        "নকশা-ফি প্রায়ই প্রকল্প-খরচের ১-৩%; খারাপ নকশা ইস্পাত, দেরি আর মেরামতে তার চেয়ে অনেক বেশি নষ্ট করতে পারে।"),
    mcq("What does vendor-managed inventory mean for a ready-mix plant supplying admixtures on a bridge site?", ["The admixture supplier monitors the plant's stock and refills it before it runs low", "The contractor manages the vendor's factory", "Stock is never counted", "The vendor owns the bridge"], 0,
        "The supplier sees real usage, plans production better and the site rarely runs out.",
        "সেতু-সাইটে মিশ্রণ-রাসায়নিক জোগানো রেডি-মিক্স কারখানার জন্য বিক্রেতা-পরিচালিত মজুত মানে কী?", ["রাসায়নিক সরবরাহকারী কারখানার মজুত নজরে রাখেন আর কমার আগেই ভরে দেন", "ঠিকাদার বিক্রেতার কারখানা চালান", "মজুত কখনো গোনা হয় না", "বিক্রেতা সেতুর মালিক"],
        "সরবরাহকারী আসল ব্যবহার দেখেন, উৎপাদন ভালো পরিকল্পনা করেন, আর সাইটে মাল প্রায় কখনো ফুরোয় না।"),
    mcq("Why does a high inventory turnover usually please a bridge-parts supplier's finance team?", ["Less cash is tied up in stock sitting in the warehouse", "It means prices are higher", "It means the warehouse is bigger", "It removes the need for sales"], 0,
        "But too high can mean frequent stock-outs, so the target balances cash against service.",
        "বেশি মজুত-আবর্তন সাধারণত সেতু-যন্ত্রাংশ সরবরাহকারীর অর্থ-দলকে খুশি করে কেন?", ["গুদামে পড়ে থাকা মজুতে কম নগদ আটকে থাকে", "এর মানে দাম বেশি", "এর মানে গুদাম বড়", "এতে বিক্রির দরকার থাকে না"],
        "তবে খুব বেশি হলে ঘনঘন মাল ফুরোতে পারে, তাই লক্ষ্য নগদ আর পরিষেবার মধ্যে ভারসাম্য রাখে।"),
    mcq("Why do bridge contracts usually cap liquidated damages, often at 10% of the contract value?", ["It limits the contractor's delay risk so bids stay reasonable; beyond the cap the owner may terminate", "Delays never cost more than 10%", "The law forbids any damages", "It lets contractors finish whenever they like"], 0,
        "Unlimited damages would make bidders add huge risk premiums or refuse to bid.",
        "সেতু-চুক্তিতে নির্ধারিত ক্ষতিপূরণে সাধারণত সর্বোচ্চ সীমা, প্রায়ই চুক্তিমূল্যের ১০%, রাখা হয় কেন?", ["এতে ঠিকাদারের দেরির ঝুঁকি সীমিত থাকে বলে দর যুক্তিসঙ্গত থাকে; সীমা পেরোলে মালিক চুক্তি বাতিল করতে পারেন", "দেরিতে কখনো ১০%-এর বেশি ক্ষতি হয় না", "আইন কোনো ক্ষতিপূরণ মানে না", "এতে ঠিকাদার যখন খুশি শেষ করতে পারেন"],
        "সীমাহীন ক্ষতিপূরণ থাকলে দরদাতারা বিশাল ঝুঁকি-মাশুল জুড়বেন বা দরই দেবেন না।"),
    mcq("What is an extension of time (EOT) claim on a bridge contract?", ["A contractor's request for more time because of delays it is not responsible for, such as late land handover", "A request to work longer hours each day", "A bonus for finishing early", "A fine for slow work"], 0,
        "If granted, it moves the completion date and protects the contractor from liquidated damages for that period.",
        "সেতু-চুক্তিতে সময়-বৃদ্ধির দাবি কী?", ["ঠিকাদারের দায় নয় এমন দেরির জন্য, যেমন দেরিতে জমি হস্তান্তর, বাড়তি সময়ের আবেদন", "রোজ বেশি ঘণ্টা কাজের আবেদন", "আগে শেষ করার বোনাস", "ধীর কাজের জরিমানা"],
        "মঞ্জুর হলে শেষের তারিখ সরে যায়, আর সেই সময়ের জন্য ঠিকাদার নির্ধারিত ক্ষতিপূরণ থেকে রেহাই পান।"),
    mcq("What is the defects liability period after a bridge is handed over?", ["A set period, often one to five years, during which the contractor must fix defects at its own cost", "The time before construction starts", "The bridge's full design life", "A period when no one may use the bridge"], 0,
        "Retention money and performance guarantees are usually held until it ends.",
        "সেতু হস্তান্তরের পরে ত্রুটি-দায়ের মেয়াদ কী?", ["একটা নির্দিষ্ট সময়, প্রায়ই এক থেকে পাঁচ বছর, যখন ঠিকাদারকে নিজের খরচে ত্রুটি সারাতে হয়", "নির্মাণ শুরুর আগের সময়", "সেতুর পুরো নকশা-আয়ু", "যখন কেউ সেতু ব্যবহার করতে পারে না"],
        "আটক টাকা আর কার্যসম্পাদন-জামানত সাধারণত এটি শেষ হওয়া পর্যন্ত রাখা হয়।"),
    mcq("What is a dispute adjudication board on a large bridge project?", ["A standing panel of independent experts that gives quick decisions on disputes while work continues", "The bridge's ticket counter", "A court that can jail engineers", "A board where workers sign in"], 0,
        "Fast, expert decisions keep the job moving; parties can still go to arbitration later.",
        "বড় সেতু-প্রকল্পে বিরোধ-নিষ্পত্তি বোর্ড কী?", ["স্বাধীন বিশেষজ্ঞদের একটা স্থায়ী দল, যা কাজ চলাকালীন বিরোধে দ্রুত সিদ্ধান্ত দেয়", "সেতুর টিকিট-কাউন্টার", "প্রকৌশলীদের জেলে পাঠাতে পারা আদালত", "কর্মীদের হাজিরা-বোর্ড"],
        "দ্রুত, বিশেষজ্ঞ সিদ্ধান্ত কাজ চালু রাখে; পরে পক্ষগুলি সালিশিতেও যেতে পারে।"),
    mcq("What does PM Gati Shakti aim to do for Indian infrastructure?", ["Plan roads, rail, ports and utilities together on one shared digital map to cut logistics costs", "Make every bridge a toll bridge", "Ban trucks on highways", "Replace all bridges with tunnels"], 0,
        "Joint planning avoids, for example, a new road being dug up months later for a pipeline.",
        "পিএম গতি শক্তি ভারতের পরিকাঠামোর জন্য কী করতে চায়?", ["এক সাধারণ ডিজিটাল মানচিত্রে সড়ক, রেল, বন্দর আর পরিষেবা একসঙ্গে পরিকল্পনা করে পরিবহন-খরচ কমানো", "প্রতিটি সেতুকে টোল-সেতু করা", "মহাসড়কে ট্রাক নিষিদ্ধ করা", "সব সেতুর বদলে সুড়ঙ্গ"],
        "যৌথ পরিকল্পনায় এড়ানো যায়, যেমন নতুন রাস্তা কয়েক মাস পরে পাইপলাইনের জন্য খোঁড়া।"),
    mcq("Trucks deliver steel to a remote bridge site and usually return empty. What is the commercial benefit of arranging backhaul loads?", ["The return trip earns money too, cutting the effective freight cost per tonne", "Trucks drive faster when loaded", "It doubles fuel use for free", "It removes the need for drivers"], 0,
        "Carrying scrap formwork or local produce back to the city turns a wasted journey into revenue.",
        "দূরের সেতু-সাইটে ট্রাক ইস্পাত দিয়ে সাধারণত খালি ফেরে। ফেরার পথে বোঝা জোগাড়ের বাণিজ্যিক লাভ কী?", ["ফেরার যাত্রাতেও আয় হয়, তাই প্রতি টনে কার্যকর মাশুল-খরচ কমে", "বোঝাই ট্রাক দ্রুত চলে", "বিনা পয়সায় জ্বালানি দ্বিগুণ হয়", "চালকের দরকার থাকে না"],
        "পুরনো ফর্মওয়ার্ক বা স্থানীয় ফসল শহরে ফিরিয়ে নিলে নষ্ট যাত্রা আয়ে বদলে যায়।"),
    mcq("Why are 300-tonne bridge girders often moved part of the way by river barge rather than by road?", ["Barges carry huge loads without needing to cross weak bridges or tight bends", "Roads are closed on weekdays", "Barges are always faster than trucks", "Girders float on their own"], 0,
        "Over-dimensional road moves need permits, escorts, and sometimes strengthened culverts - water routes avoid much of that.",
        "৩০০ টনের সেতু-গার্ডার প্রায়ই রাস্তার বদলে আংশিক নদীপথে বজরায় নেওয়া হয় কেন?", ["বজরা দুর্বল সেতু বা সরু বাঁক পেরোনো ছাড়াই বিশাল বোঝা বইতে পারে", "সপ্তাহের দিনে রাস্তা বন্ধ থাকে", "বজরা সবসময় ট্রাকের চেয়ে দ্রুত", "গার্ডার নিজে থেকেই ভাসে"],
        "সড়কে অতিকায় বোঝা নিতে অনুমতি, পাহারা, আর কখনো কালভার্ট মজবুত করাও লাগে — জলপথে তার অনেকটাই এড়ানো যায়।"),
    mcq("What is an over-dimensional cargo (ODC) permit when moving a bridge girder by road?", ["Official permission to move an oversized load on a fixed route and time, often with escorts", "A licence to build bridges", "A customs form for imports", "A discount on tolls"], 0,
        "Authorities check the route's bridges, wires and turns before allowing the move, often at night.",
        "রাস্তায় সেতু-গার্ডার নিতে অতিকায় পণ্যের অনুমতিপত্র কী?", ["নির্দিষ্ট পথে আর সময়ে, প্রায়ই পাহারাসহ, অতিকায় বোঝা নেওয়ার সরকারি অনুমতি", "সেতু বানানোর লাইসেন্স", "আমদানির শুল্ক-ফর্ম", "টোলে ছাড়"],
        "চলাচলের অনুমতির আগে কর্তৃপক্ষ পথের সেতু, তার আর বাঁক পরীক্ষা করে, প্রায়ই রাতে নেওয়া হয়।"),
    mcq("In a bridge alliance contract with target cost and pain/gain share, what happens if the final cost is below target?", ["The savings are shared between the owner and the contractor in agreed proportions", "The contractor must return all its profit", "The owner pays a fine", "The bridge must be rebuilt"], 0,
        "Both sides gain from efficiency and share overruns too, which encourages teamwork instead of claims.",
        "লক্ষ্য-খরচ আর লাভ-ক্ষতি ভাগের সেতু-জোট চুক্তিতে চূড়ান্ত খরচ লক্ষ্যের নিচে হলে কী হয়?", ["সাশ্রয় মালিক আর ঠিকাদারের মধ্যে চুক্তিমতো ভাগে ভাগ হয়", "ঠিকাদারকে সব লাভ ফেরত দিতে হয়", "মালিক জরিমানা দেন", "সেতু আবার বানাতে হয়"],
        "দক্ষতায় দুপক্ষই লাভ করে আর বাড়তি খরচও ভাগ করে, যা দাবি-পাল্টা দাবির বদলে দলগত কাজে উৎসাহ দেয়।"),
    mcq("Why does an EPC (lump-sum turnkey) bridge contract often cost the owner more upfront than an item-rate contract?", ["The contractor prices in the design and quantity risks it now carries", "EPC contractors pay no tax", "EPC bridges are always longer", "Item-rate contracts include free maintenance"], 0,
        "The owner pays a premium for price certainty and a single point of responsibility.",
        "ইপিসি (একমুঠো চাবি-হস্তান্তর) সেতু-চুক্তিতে মালিকের প্রাথমিক খরচ প্রায়ই দফা-দর চুক্তির চেয়ে বেশি হয় কেন?", ["ঠিকাদার এখন যে নকশা আর পরিমাণের ঝুঁকি বহন করেন, তার দাম দরে ধরেন", "ইপিসি ঠিকাদার কর দেন না", "ইপিসি সেতু সবসময় লম্বা", "দফা-দর চুক্তিতে বিনা পয়সায় রক্ষণাবেক্ষণ থাকে"],
        "দামের নিশ্চয়তা আর একক দায়িত্বের জন্য মালিক বাড়তি মূল্য দেন।"),
    mcq("Under India's hybrid annuity model (HAM) for highways and bridges, how is the private partner paid?", ["About 40% of the cost during construction, the rest as fixed annuities over the operating years", "Only from toll collections", "Entirely in advance", "Only if traffic exceeds forecasts"], 0,
        "The government keeps traffic risk; the private partner carries construction and maintenance risk.",
        "মহাসড়ক আর সেতুর জন্য ভারতের মিশ্র বার্ষিকী মডেলে বেসরকারি অংশীদার কীভাবে টাকা পান?", ["নির্মাণকালে খরচের প্রায় ৪০%, বাকিটা চালু থাকার বছরগুলিতে স্থির বার্ষিকী হিসেবে", "শুধু টোল-আদায় থেকে", "পুরোটা আগাম", "যানবাহন পূর্বাভাস ছাড়ালে তবেই"],
        "যানবাহনের ঝুঁকি সরকার রাখে; নির্মাণ আর রক্ষণাবেক্ষণের ঝুঁকি বেসরকারি অংশীদারের।"),
    mcq("What is a toll-operate-transfer (TOT) deal for an existing toll bridge?", ["The government leases the operating bridge to an investor for an upfront payment, and the investor collects tolls for a fixed period", "A contract to build a brand-new bridge", "A free transfer of the bridge to a state", "A scheme to remove tolls"], 0,
        "The upfront cash can fund new projects - a form of asset recycling.",
        "চালু টোল-সেতুর জন্য টোল-পরিচালনা-হস্তান্তর চুক্তি কী?", ["সরকার আগাম টাকার বিনিময়ে চালু সেতু একজন বিনিয়োগকারীকে ইজারা দেয়, আর তিনি নির্দিষ্ট সময় টোল তোলেন", "একদম নতুন সেতু বানানোর চুক্তি", "রাজ্যকে বিনা পয়সায় সেতু হস্তান্তর", "টোল তুলে দেওয়ার প্রকল্প"],
        "আগাম নগদ দিয়ে নতুন প্রকল্পে অর্থ জোগানো যায় — সম্পদ পুনর্ব্যবহারের একটা রূপ।"),
    mcq("Why do bridge owners use two-envelope tendering?", ["Technical bids are opened first, and only qualified bidders' price bids are opened afterwards", "Each bidder must send two copies by post", "It doubles the number of bidders", "Prices are kept secret forever"], 0,
        "Judging competence before seeing prices stops a low price from swaying the technical assessment.",
        "সেতু-মালিকেরা দুই-খামের দরপত্র ব্যবহার করেন কেন?", ["প্রথমে প্রযুক্তিগত দর খোলা হয়, তারপর শুধু যোগ্য দরদাতাদের দামের দর খোলা হয়", "প্রত্যেক দরদাতাকে ডাকে দুটি কপি পাঠাতে হয়", "এতে দরদাতা দ্বিগুণ হয়", "দাম চিরকাল গোপন থাকে"],
        "দাম দেখার আগে যোগ্যতা বিচার করলে কম দাম প্রযুক্তিগত মূল্যায়নকে প্রভাবিত করতে পারে না।"),
    mcq("Several firms secretly agree who will win a bridge tender and at what price. What is this called, and why is it illegal?", ["Bid rigging - it cheats the public out of fair competition and is banned under competition law", "Joint venture - it is always encouraged", "Value engineering - it saves money", "Pre-qualification - it is required"], 0,
        "The Competition Commission of India can impose heavy penalties on cartels.",
        "কয়েকটি সংস্থা গোপনে ঠিক করে নিল কে কোন দামে সেতুর দরপত্র জিতবে। একে কী বলে, আর তা বেআইনি কেন?", ["দর-কারসাজি — এটি জনগণকে ন্যায্য প্রতিযোগিতা থেকে ঠকায় আর প্রতিযোগিতা-আইনে নিষিদ্ধ", "যৌথ উদ্যোগ — সবসময় উৎসাহিত", "মূল্য-প্রকৌশল — টাকা বাঁচায়", "প্রাক-যোগ্যতা — বাধ্যতামূলক"],
        "ভারতের প্রতিযোগিতা কমিশন কার্টেলের উপর বড় জরিমানা চাপাতে পারে।"),
    mcq("Why does a bridge tender hold a pre-bid meeting?", ["To answer every bidder's questions openly so all price the same understanding of the job", "To choose the winner in advance", "To collect bid fees in cash", "To let bidders inspect each other's prices"], 0,
        "Clarifications are issued to all bidders in writing, keeping the contest fair.",
        "সেতুর দরপত্রে দর-পূর্ব সভা হয় কেন?", ["সব দরদাতার প্রশ্নের খোলাখুলি উত্তর দিতে, যাতে সবাই কাজের একই বোঝাপড়ায় দাম দেন", "আগে থেকেই বিজয়ী ঠিক করতে", "নগদে দরপত্র-মাশুল তুলতে", "দরদাতাদের একে অপরের দাম দেখাতে"],
        "সব স্পষ্টীকরণ লিখিতভাবে সব দরদাতাকে দেওয়া হয়, যাতে প্রতিযোগিতা ন্যায্য থাকে।"),
    mcq("Why do lenders study a bridge contractor's cash-flow S-curve?", ["It shows spending over time - slow at the start, fast in the middle, slow at the end - so funding can be lined up", "It shows the shape of the bridge deck", "It measures the river's curve", "It replaces the design drawings"], 0,
        "Drawdowns of loans are scheduled to match the steep middle part of the curve.",
        "ঋণদাতারা সেতু-ঠিকাদারের নগদপ্রবাহের এস-রেখা খুঁটিয়ে দেখেন কেন?", ["এটি সময়ের সঙ্গে খরচ দেখায় — শুরুতে ধীর, মাঝে দ্রুত, শেষে ধীর — তাই অর্থ জোগানের ব্যবস্থা করা যায়", "এটি সেতু-পাটাতনের আকার দেখায়", "এটি নদীর বাঁক মাপে", "এটি নকশা-আঁকার বদলে কাজ করে"],
        "ঋণের কিস্তি তোলা রেখার খাড়া মাঝের অংশের সঙ্গে মিলিয়ে নির্ধারণ করা হয়।"),
    mcq("Why is relying on a single approved maker for a bridge's special bearings a commercial risk?", ["A fire, strike or backlog at that one factory can halt the whole project with no backup", "Single makers are always more expensive", "Bearings from one maker never fit", "It is illegal to have one supplier"], 0,
        "Mitigations include qualifying a second source, ordering early, or holding buffer stock.",
        "সেতুর বিশেষ বিয়ারিং-এর জন্য একটিমাত্র অনুমোদিত নির্মাতার উপর ভরসা করা বাণিজ্যিক ঝুঁকি কেন?", ["সেই একটি কারখানায় আগুন, ধর্মঘট বা কাজের জট হলে বিকল্প ছাড়াই গোটা প্রকল্প থেমে যেতে পারে", "একক নির্মাতা সবসময় বেশি দামি", "এক নির্মাতার বিয়ারিং কখনো মাপে মেলে না", "একজন সরবরাহকারী রাখা বেআইনি"],
        "সমাধান: দ্বিতীয় উৎসকে যোগ্য করা, আগে অর্ডার দেওয়া, বা বাড়তি মজুত রাখা।"),
    mcq("What does the mean absolute percentage error (MAPE) tell a materials planner?", ["The average size of forecast errors as a percentage of actual demand", "The maximum price of a material", "The percentage of trucks that arrive late", "The profit margin on cement"], 0,
        "A MAPE of 8% means forecasts miss by about 8% on average - useful for comparing forecasting methods.",
        "গড় পরম শতাংশ-ত্রুটি একজন উপকরণ-পরিকল্পককে কী জানায়?", ["আসল চাহিদার শতাংশ হিসেবে পূর্বাভাসের ভুলের গড় আকার", "কোনো উপকরণের সর্বোচ্চ দাম", "কত শতাংশ ট্রাক দেরিতে আসে", "সিমেন্টে লাভের হার"],
        "৮% মানে পূর্বাভাস গড়ে প্রায় ৮% ভুল করে — বিভিন্ন পূর্বাভাস-পদ্ধতি তুলনায় কাজে লাগে।"),
)
