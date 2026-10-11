"""IIT level - Commercials (MBA / IIT-management depth): Ind AS financial reporting (revenue, leases,
deferred tax, impairment, consolidation, diluted EPS), strategic cost management (ABC, target and
transfer pricing, multi-product break-even, variances), operations research and operations
management (linear programming, assignment, transportation, queues, line balancing, learning curves,
forecasting, EPQ, process capability, Taguchi loss), project control by earned value, strategy,
marketing, organisational behaviour and Indian business law."""
import math
from fractions import Fraction as F
from itertools import permutations

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


def _fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


# ---------------------------------------------------------------- queues and flow
def little(lam, w):
    r = lam * w
    return _n(f"Trucks arrive at a batching plant at {lam} per hour and each spends {w} hours on site on average. On average, how many trucks are on site?",
              f"একটা ব্যাচিং প্ল্যান্টে ঘণ্টায় {lam}টি ট্রাক আসে আর প্রতিটি গড়ে {w} ঘণ্টা থাকে। গড়ে কয়টি ট্রাক সাইটে থাকে?", r,
              f"Little's law: L = λW = {lam} x {w} = {_f(_c(r))} - true for any stable system.",
              f"লিটলের সূত্র: L = λW = {lam} x {w} = {_f(_c(r))} - যেকোনো স্থিতিশীল ব্যবস্থায় সত্য।",
              (lam / w, lam + w, r + 2))


def mm1_lq(lam, mu):
    rho = lam / mu
    lq = rho * rho / (1 - rho)
    return _n(f"A single toll booth serves {mu} vehicles an hour; vehicles arrive at random at {lam} an hour (M/M/1). How many vehicles wait in the queue on average?",
              f"একটা টোল-বুথ ঘণ্টায় {mu}টি গাড়ি সামলায়; গাড়ি এলোমেলোভাবে ঘণ্টায় {lam}টি আসে (এম/এম/1)। গড়ে কয়টি গাড়ি সারিতে অপেক্ষা করে?", lq,
              f"ρ = λ/μ = {_f(_c(rho))}; Lq = ρ² ÷ (1 - ρ) = {_f(_c(lq))}. Queues explode as ρ approaches 1.",
              f"ρ = λ/μ = {_f(_c(rho))}; Lq = ρ² ÷ (1 - ρ) = {_f(_c(lq))}। ρ 1-এর কাছে গেলে সারি বিস্ফোরিত হয়।",
              (rho / (1 - rho), rho, lq * 2 + 0.5))


def mm1_wq(lam, mu):
    rho = lam / mu
    wq = rho / (mu - lam) * 60
    return _n(f"A single crane unloads {mu} trucks an hour; trucks arrive at random at {lam} an hour (M/M/1). How long does a truck wait before unloading starts, on average?",
              f"একটা ক্রেন ঘণ্টায় {mu}টি ট্রাক খালি করে; ট্রাক এলোমেলোভাবে ঘণ্টায় {lam}টি আসে (এম/এম/1)। খালি শুরুর আগে একটা ট্রাক গড়ে কতক্ষণ অপেক্ষা করে?", wq,
              f"Wq = λ ÷ [μ(μ - λ)] = {lam} ÷ [{mu} x {mu - lam}] hours = {_f(_c(wq))} minutes.",
              f"Wq = λ ÷ [μ(μ - λ)] = {lam} ÷ [{mu} x {mu - lam}] ঘণ্টা = {_f(_c(wq))} মিনিট।",
              (60 / (mu - lam), 60 / mu, wq + 5), " min", " মিনিট")


def takt(minutes, demand):
    r = minutes * 60 / demand
    return _n(f"A precast factory works {minutes} minutes a day and must make {demand} panels a day. What is the takt time?",
              f"একটা প্রিকাস্ট কারখানা দিনে {minutes} মিনিট কাজ করে আর দিনে {demand}টি প্যানেল বানাতে হয়। টাক্ট সময় কত?", r,
              f"Takt = available time ÷ demand = {minutes * 60:,} s ÷ {demand} = {_f(_c(r))} seconds per panel: the pace the line must keep.",
              f"টাক্ট = প্রাপ্য সময় ÷ চাহিদা = {minutes * 60:,} সেকেন্ড ÷ {demand} = প্রতি প্যানেলে {_f(_c(r))} সেকেন্ড: লাইনকে এই গতি রাখতে হবে।",
              (demand / minutes * 60, minutes / demand, r * 1.5), " s", " সেকেন্ড")


def stations(total, takt_s):
    r = math.ceil(total / takt_s)
    return _n(f"The tasks on an assembly line add up to {total} seconds and the takt time is {takt_s} seconds. What is the minimum number of workstations?",
              f"একটা অ্যাসেম্বলি লাইনের কাজ মিলিয়ে {total} সেকেন্ড আর টাক্ট সময় {takt_s} সেকেন্ড। ন্যূনতম কয়টি কর্মস্থল লাগে?", r,
              f"Nmin = ⌈total work ÷ takt⌉ = ⌈{total} ÷ {takt_s}⌉ = ⌈{_f(_c(total / takt_s))}⌉ = {r}; precedence may force more.",
              f"ন্যূনতম = ⌈মোট কাজ ÷ টাক্ট⌉ = ⌈{total} ÷ {takt_s}⌉ = ⌈{_f(_c(total / takt_s))}⌉ = {r}; ক্রম-বাধ্যবাধকতায় বেশি লাগতে পারে।",
              (r - 1 if r > 1 else r + 2, r + 2, math.floor(total / takt_s) + 3))


def learning(t1, rate, n):
    r = t1 * (rate / 100) ** math.log2(n)
    return _n(f"The first steel girder takes {t1} hours to fabricate and the work follows an {rate}% learning curve. How long does the {n}th girder take?",
              f"প্রথম ইস্পাতের গার্ডার তৈরিতে {t1} ঘণ্টা লাগে আর কাজ {rate}% শিখন-বক্ররেখা মানে। {n}-তম গার্ডারে কত সময় লাগে?", r,
              f"Each doubling of output multiplies unit time by {rate / 100:g}: {t1} x {rate / 100:g}^{int(math.log2(n))} = {_f(_c(r))} hours.",
              f"উৎপাদন প্রতিবার দ্বিগুণ হলে একক-সময় {rate / 100:g} গুণ হয়: {t1} x {rate / 100:g}^{int(math.log2(n))} = {_f(_c(r))} ঘণ্টা।",
              (t1 * rate / 100, t1 / n, r + 10), " hours", " ঘণ্টা")


def smoothing(f, a, alpha):
    r = f + alpha * (a - f)
    return _n(f"Last month's forecast for cement demand was {f} tonnes and actual demand was {a} tonnes. With exponential smoothing (α = {alpha}), what is this month's forecast?",
              f"গত মাসে সিমেন্টের চাহিদার পূর্বাভাস ছিল {f} টন আর প্রকৃত চাহিদা {a} টন। সূচকীয় মসৃণকরণে (α = {alpha}) এই মাসের পূর্বাভাস কত?", r,
              f"Fₜ₊₁ = Fₜ + α(Aₜ - Fₜ) = {f} + {alpha} x ({a} - {f}) = {_f(_c(r))} tonnes.",
              f"Fₜ₊₁ = Fₜ + α(Aₜ - Fₜ) = {f} + {alpha} x ({a} - {f}) = {_f(_c(r))} টন।",
              ((f + a) / 2, a, f + (1 - alpha) * (a - f)), " t", " টন")


def mad(actual, forecast):
    errs = [abs(a - f) for a, f in zip(actual, forecast)]
    r = sum(errs) / len(errs)
    return _n(f"Actual demand was {actual} and the forecasts were {forecast}. What is the mean absolute deviation (MAD) of the forecast?",
              f"প্রকৃত চাহিদা ছিল {actual} আর পূর্বাভাস {forecast}। পূর্বাভাসের গড় পরম বিচ্যুতি (এমএডি) কত?", r,
              f"Absolute errors {errs}; MAD = {sum(errs)} ÷ {len(errs)} = {_f(_c(r))}. Signs are dropped so errors cannot cancel.",
              f"পরম ত্রুটি {errs}; এমএডি = {sum(errs)} ÷ {len(errs)} = {_f(_c(r))}। চিহ্ন বাদ দেওয়া হয় যাতে ত্রুটি কাটাকাটি না হয়।",
              (abs(sum(a - f for a, f in zip(actual, forecast))) / len(errs) + 0.5, max(errs), r * 1.5))


def epq(d, s, h, p_rate, d_rate):
    q = math.sqrt(2 * d * s / (h * (1 - d_rate / p_rate)))
    return _n(f"A plant uses {d:,} blocks a year. It makes them itself at {p_rate} a day while using {d_rate} a day; each set-up costs Rs {s} and holding a block costs Rs {h} a year. What is the economic production quantity?",
              f"একটা প্ল্যান্ট বছরে {d:,}টি ব্লক ব্যবহার করে। নিজে দিনে {p_rate}টি বানায় আর দিনে {d_rate}টি ব্যবহার করে; প্রতি প্রস্তুতিতে খরচ Rs {s}, আর একটা ব্লক রাখার খরচ বছরে Rs {h}। অর্থনৈতিক উৎপাদন-পরিমাণ কত?", q,
              f"EPQ = √[2DS ÷ (H(1 - d/p))] = √[2 x {d:,} x {s} ÷ ({h} x {_f(_c(1 - d_rate / p_rate))})] = {_f(_c(q))} blocks - larger than EOQ, as stock builds up gradually.",
              f"উৎপাদন-পরিমাণ = √[2DS ÷ (H(1 - d/p))] = √[2 x {d:,} x {s} ÷ ({h} x {_f(_c(1 - d_rate / p_rate))})] = {_f(_c(q))}টি ব্লক - ইওকিউ-এর চেয়ে বড়, কারণ মজুত ধীরে জমে।",
              (math.sqrt(2 * d * s / h), q / 2, q * 1.4), " blocks", "টি ব্লক")


# ---------------------------------------------------------------- project control and quality
def cpi(ev, ac):
    r = ev / ac
    return _n(f"A bridge project has earned value Rs {ev} lakh against an actual cost of Rs {ac} lakh. What is its cost performance index (CPI)?",
              f"একটা সেতু-প্রকল্পের অর্জিত মূল্য Rs {ev} লক্ষ, প্রকৃত খরচ Rs {ac} লক্ষ। এর খরচ-কৃতি সূচক (সিপিআই) কত?", r,
              f"CPI = EV ÷ AC = {ev} ÷ {ac} = {_f(_c(r))}: {'over' if r < 1 else 'under'} budget for the work done.",
              f"সিপিআই = অর্জিত মূল্য ÷ প্রকৃত খরচ = {ev} ÷ {ac} = {_f(_c(r))}: করা কাজের তুলনায় বাজেট {'ছাড়িয়েছে' if r < 1 else 'কম লেগেছে'}।",
              (ac / ev, (ev - ac) / ac + 1.2, r + 0.3))


def spi(ev, pv):
    r = ev / pv
    return _n(f"By month 6 a project planned to finish work worth Rs {pv} lakh but completed work worth Rs {ev} lakh. What is its schedule performance index (SPI)?",
              f"6 মাসের মধ্যে একটা প্রকল্পের Rs {pv} লক্ষের কাজ শেষ করার পরিকল্পনা ছিল, কিন্তু শেষ হয়েছে Rs {ev} লক্ষের। এর সময়সূচি-কৃতি সূচক (এসপিআই) কত?", r,
              f"SPI = EV ÷ PV = {ev} ÷ {pv} = {_f(_c(r))}: {'behind' if r < 1 else 'ahead of'} schedule.",
              f"এসপিআই = অর্জিত মূল্য ÷ পরিকল্পিত মূল্য = {ev} ÷ {pv} = {_f(_c(r))}: সময়সূচির {'পেছনে' if r < 1 else 'আগে'}।",
              (pv / ev, r + 0.25, (pv - ev) / pv + 0.5))


def eac(bac, cpi_v):
    r = bac / cpi_v
    return _n(f"A project's budget at completion is Rs {bac} lakh and its CPI so far is {cpi_v}. If performance continues, what is the estimate at completion (Rs lakh)?",
              f"একটা প্রকল্পের সমাপ্তি-বাজেট Rs {bac} লক্ষ আর এখন পর্যন্ত সিপিআই {cpi_v}। কৃতি একই থাকলে সমাপ্তির আনুমানিক খরচ (Rs লক্ষ) কত?", r,
              f"EAC = BAC ÷ CPI = {bac} ÷ {cpi_v} = {_f(_c(r))}; the overrun would be {_f(_c(r - bac))}.",
              f"সমাপ্তির অনুমান = বাজেট ÷ সিপিআই = {bac} ÷ {cpi_v} = {_f(_c(r))}; বাড়তি খরচ হবে {_f(_c(r - bac))}।",
              (bac * cpi_v, bac, r + 20))


def cpk(usl, lsl, mean, sd):
    r = min(usl - mean, mean - lsl) / (3 * sd)
    return _n(f"Rebar diameters must lie between {lsl} and {usl} mm. The process mean is {mean} mm with a standard deviation of {sd} mm. What is Cpk?",
              f"রডের ব্যাস {lsl} থেকে {usl} mm-এর মধ্যে হতে হবে। প্রক্রিয়ার গড় {mean} mm, সমক বিচ্যুতি {sd} mm। Cpk কত?", r,
              f"Cpk = min(USL - μ, μ - LSL) ÷ 3σ = min({_f(_c(usl - mean))}, {_f(_c(mean - lsl))}) ÷ {_f(_c(3 * sd))} = {_f(_c(r))}. Cp ignores centring; Cpk does not.",
              f"Cpk = min(USL - μ, μ - LSL) ÷ 3σ = min({_f(_c(usl - mean))}, {_f(_c(mean - lsl))}) ÷ {_f(_c(3 * sd))} = {_f(_c(r))}। Cp কেন্দ্রীকরণ উপেক্ষা করে, Cpk করে না।",
              ((usl - lsl) / (6 * sd), (usl - lsl) / (3 * sd), r + 0.4))


def taguchi(k, y, t):
    r = k * (y - t) ** 2
    return _rs(f"A beam's target depth is {t} mm. Taguchi's loss constant is k = Rs {k} per mm². What is the quality loss for a beam {y} mm deep?",
               f"একটা বিমের লক্ষ্য-গভীরতা {t} mm। তাগুচির ক্ষতি-ধ্রুবক k = Rs {k} প্রতি mm²। {y} mm গভীর বিমের গুণমান-ক্ষতি কত?", r,
               f"L = k(y - T)² = {k} x ({_f(_c(y - t))})² = Rs {_f(_c(r))}: loss grows with the square of the deviation, even inside the tolerance.",
               f"L = k(y - T)² = {k} x ({_f(_c(y - t))})² = Rs {_f(_c(r))}: সহনসীমার ভেতরেও বিচ্যুতির বর্গের সঙ্গে ক্ষতি বাড়ে।",
               (k * abs(y - t), k * (y - t) ** 2 / 2, r + k))


# ---------------------------------------------------------------- operations research
def lp(c1, c2, a1, b1, r1, a2, b2, r2):
    pts = [(0, 0), (r1 / a1, 0), (r2 / a2, 0), (0, r1 / b1), (0, r2 / b2)]
    det = a1 * b2 - a2 * b1
    if det:
        pts.append(((r1 * b2 - r2 * b1) / det, (a1 * r2 - a2 * r1) / det))
    feas = [(x, y) for x, y in pts if x >= -1e-9 and y >= -1e-9 and a1 * x + b1 * y <= r1 + 1e-9 and a2 * x + b2 * y <= r2 + 1e-9]
    best = max(feas, key=lambda p: c1 * p[0] + c2 * p[1])
    z = c1 * best[0] + c2 * best[1]
    worst_corner = sorted(c1 * x + c2 * y for x, y in feas)
    return _rs(f"Maximise profit {c1}x + {c2}y subject to {a1}x + {b1}y ≤ {r1}, {a2}x + {b2}y ≤ {r2}, x, y ≥ 0. What is the maximum profit?",
               f"শর্ত {a1}x + {b1}y ≤ {r1}, {a2}x + {b2}y ≤ {r2}, x, y ≥ 0 মেনে মুনাফা {c1}x + {c2}y সর্বোচ্চ করো। সর্বোচ্চ মুনাফা কত?", z,
               f"The optimum of a linear programme lies at a corner of the feasible region; checking the corners gives x = {_f(_c(best[0]))}, y = {_f(_c(best[1]))}, profit Rs {_f(_c(z))}.",
               f"রৈখিক প্রোগ্রামের সর্বোত্তম সমাধান সম্ভাব্য অঞ্চলের কোণে থাকে; কোণগুলো যাচাই করলে x = {_f(_c(best[0]))}, y = {_f(_c(best[1]))}, মুনাফা Rs {_f(_c(z))}।",
               (worst_corner[-2] if len(worst_corner) > 1 and worst_corner[-2] > 0 else z * 0.8, max(c1 * r1 / a1, c2 * r1 / b1) * 1.3, z * 0.75))


def assignment(m):
    best = min(permutations(range(3)), key=lambda p: sum(m[i][p[i]] for i in range(3)))
    r = sum(m[i][best[i]] for i in range(3))
    worst = max(sum(m[i][p[i]] for i in range(3)) for p in permutations(range(3)))
    diag = sum(m[i][i] for i in range(3))
    rows = "; ".join(" ".join(str(x) for x in row) for row in m)
    return _n(f"Three crews must be assigned to three sites, one each. The cost matrix (crews in rows, Rs thousand) is [{rows}]. What is the minimum total cost?",
              f"তিনটি দলকে তিনটি সাইটে একটা করে দিতে হবে। খরচের ম্যাট্রিক্স (সারিতে দল, Rs হাজার) [{rows}]। ন্যূনতম মোট খরচ কত?", r,
              f"Hungarian method (or checking all 6 assignments): crew → site {[(i + 1, best[i] + 1) for i in range(3)]}, total {r}.",
              f"হাঙ্গেরীয় পদ্ধতি (বা 6টি বণ্টনই যাচাই): দল → সাইট {[(i + 1, best[i] + 1) for i in range(3)]}, মোট {r}।",
              (diag if diag != r else r + 3, worst, r + 2))


def nw_corner(supply, demand, cost):
    s, d = list(supply), list(demand)
    i = j = 0
    total = 0
    while i < len(s) and j < len(d):
        q = min(s[i], d[j])
        total += q * cost[i][j]
        s[i] -= q
        d[j] -= q
        if s[i] == 0:
            i += 1
        else:
            j += 1
    rows = "; ".join(" ".join(str(x) for x in row) for row in cost)
    return _n(f"Two quarries with supplies {supply} tonnes feed three sites needing {demand} tonnes. Unit costs (quarries in rows) are [{rows}]. What is the cost of the north-west corner starting solution?",
              f"{supply} টন জোগানের দুটি খাদান {demand} টন চাহিদার তিনটি সাইটে পাঠায়। একক খরচ (সারিতে খাদান) [{rows}]। উত্তর-পশ্চিম কোণ পদ্ধতির প্রারম্ভিক সমাধানের খরচ কত?", total,
              f"Fill cells from the top-left, using up each supply or demand in turn: total cost {total:,}. MODI or stepping-stone then improves it.",
              f"বাঁ-ওপরের ঘর থেকে ভরো, পালা করে প্রতিটি জোগান বা চাহিদা শেষ করে: মোট খরচ {total:,}। তারপর মোদি বা স্টেপিং-স্টোন পদ্ধতি একে উন্নত করে।",
              (total - 200, sum(supply) * min(min(r) for r in cost), total + 300))


# ---------------------------------------------------------------- marketing and cost management
def clv(margin, retention, disc):
    r = margin * (retention / 100) / (1 + disc / 100 - retention / 100)
    return _rs(f"A cement dealer earns Rs {margin:,} a year from a builder, keeps {retention}% of builders each year, and uses a {disc}% discount rate. What is the customer lifetime value?",
               f"একজন সিমেন্ট-বিক্রেতা একজন নির্মাতার থেকে বছরে Rs {margin:,} আয় করেন, প্রতি বছর {retention}% নির্মাতাকে ধরে রাখেন, আর {disc}% বাট্টা হার নেন। গ্রাহকের আজীবন মূল্য কত?", r,
               f"CLV = m x r ÷ (1 + i - r) = {margin:,} x {retention / 100:g} ÷ {_f(_c(1 + disc / 100 - retention / 100))} = Rs {_f(_c(r))}.",
               f"আজীবন মূল্য = m x r ÷ (1 + i - r) = {margin:,} x {retention / 100:g} ÷ {_f(_c(1 + disc / 100 - retention / 100))} = Rs {_f(_c(r))}।",
               (margin / (1 - retention / 100), margin * retention / 100, r * 1.3))


def arc_elasticity(p1, q1, p2, q2):
    r = abs(((q2 - q1) / ((q1 + q2) / 2)) / ((p2 - p1) / ((p1 + p2) / 2)))
    return _n(f"When the price of a bag of cement rose from Rs {p1} to Rs {p2}, monthly sales fell from {q1:,} to {q2:,} bags. What is the arc (midpoint) price elasticity, in absolute terms?",
              f"এক বস্তা সিমেন্টের দাম Rs {p1} থেকে Rs {p2} হলে মাসিক বিক্রি {q1:,} থেকে {q2:,} বস্তায় নামে। চাপ (মধ্যবিন্দু) দাম-স্থিতিস্থাপকতা পরম মানে কত?", r,
              f"%ΔQ = {_f(_c((q2 - q1) / ((q1 + q2) / 2) * 100))}%, %ΔP = {_f(_c((p2 - p1) / ((p1 + p2) / 2) * 100))}% (on midpoints): |E| = {_f(_c(r))}{' - elastic, so revenue moves opposite to price' if r > 1 else ' - inelastic, so revenue moves with price'}.",
              f"মধ্যবিন্দুতে %ΔQ = {_f(_c((q2 - q1) / ((q1 + q2) / 2) * 100))}%, %ΔP = {_f(_c((p2 - p1) / ((p1 + p2) / 2) * 100))}%: |E| = {_f(_c(r))}{' - স্থিতিস্থাপক, তাই আয় দামের উল্টো দিকে যায়' if r > 1 else ' - অস্থিতিস্থাপক, তাই আয় দামের সঙ্গে একই দিকে যায়'}।",
              (abs((q2 - q1) / q1 / ((p2 - p1) / p1)) + 0.2, r * 2, r + 0.5))


def multi_bep(fc, cm_a, cm_b, mix_a, mix_b):
    wcm = (cm_a * mix_a + cm_b * mix_b) / (mix_a + mix_b)
    r = fc / wcm
    return _n(f"A plant sells pipes and poles in the ratio {mix_a} : {mix_b}, with contributions of Rs {cm_a} and Rs {cm_b} per unit. Fixed costs are Rs {fc:,}. How many units in total must it sell to break even?",
              f"একটা কারখানা পাইপ আর খুঁটি {mix_a} : {mix_b} অনুপাতে বেচে, প্রতি এককে অবদান Rs {cm_a} আর Rs {cm_b}। স্থির খরচ Rs {fc:,}। লাভ-ক্ষতিহীন হতে মোট কত একক বেচতে হবে?", r,
              f"Weighted contribution = ({cm_a} x {mix_a} + {cm_b} x {mix_b}) ÷ {mix_a + mix_b} = {_f(_c(wcm))}; break-even = {fc:,} ÷ {_f(_c(wcm))} = {_f(_c(r))} units.",
              f"ভারযুক্ত অবদান = ({cm_a} x {mix_a} + {cm_b} x {mix_b}) ÷ {mix_a + mix_b} = {_f(_c(wcm))}; লাভ-ক্ষতিহীন বিন্দু = {fc:,} ÷ {_f(_c(wcm))} = {_f(_c(r))} একক।",
              (fc / ((cm_a + cm_b) / 2), fc / max(cm_a, cm_b), r * 1.25), " units", " একক")


def transfer_min(vc, sp, ext_vc, full):
    r = vc + ((sp - ext_vc) if full else 0)
    how = "the division is at full capacity, so add the contribution lost on outside sales" if full else "the division has spare capacity, so only variable cost matters"
    how_bn = "বিভাগ পূর্ণ ক্ষমতায়, তাই বাইরের বিক্রিতে হারানো অবদান যোগ করো" if full else "বিভাগের অতিরিক্ত ক্ষমতা আছে, তাই কেবল পরিবর্তনশীল খরচ গোনে"
    return _rs(f"A cement division's variable cost is Rs {vc} a bag; it sells outside at Rs {sp} with Rs {ext_vc} variable cost per outside sale. It is {'working at full capacity' if full else 'working below capacity'}. What is the minimum transfer price to the group's construction division?",
               f"একটা সিমেন্ট-বিভাগের পরিবর্তনশীল খরচ বস্তাপ্রতি Rs {vc}; বাইরে Rs {sp}-এ বেচে, বাইরের প্রতি বিক্রিতে পরিবর্তনশীল খরচ Rs {ext_vc}। এটা {'পূর্ণ ক্ষমতায় চলছে' if full else 'ক্ষমতার নিচে চলছে'}। গোষ্ঠীর নির্মাণ-বিভাগে ন্যূনতম স্থানান্তর-মূল্য কত?", r,
               f"Minimum transfer price = variable cost + opportunity cost; {how}: Rs {r}.",
               f"ন্যূনতম স্থানান্তর-মূল্য = পরিবর্তনশীল খরচ + সুযোগ-ব্যয়; {how_bn}: Rs {r}।",
               (sp, vc + (0 if full else sp - ext_vc), r + 20))


def abc_cost(pool, driver_total, used, driver_en, driver_bn):
    rate = pool / driver_total
    r = rate * used
    return _rs(f"Overheads of Rs {pool:,} are driven by {driver_total:,} {driver_en}. A product uses {used:,} of them. How much overhead does activity-based costing charge to it?",
               f"Rs {pool:,} উপরিব্যয়ের চালক {driver_total:,}টি {driver_bn}। একটা পণ্য তার {used:,}টি ব্যবহার করে। কার্যভিত্তিক খরচ-নিরূপণে এতে কত উপরিব্যয় চাপে?", r,
               f"Driver rate = {pool:,} ÷ {driver_total:,} = Rs {_f(_c(rate))}; charge = {_f(_c(rate))} x {used:,} = Rs {_f(_c(r))}.",
               f"চালক-হার = {pool:,} ÷ {driver_total:,} = Rs {_f(_c(rate))}; চাপানো = {_f(_c(rate))} x {used:,} = Rs {_f(_c(r))}।",
               (pool / 2, pool * used / (driver_total * 2), r * 1.4))


def target_cost(price, margin):
    r = price * (1 - margin / 100)
    return _rs(f"Market research says a prefabricated toilet unit can sell for Rs {price:,}. The firm wants a {margin}% profit margin on price. What is the target cost?",
               f"বাজার-গবেষণা বলে একটা প্রি-ফ্যাব শৌচাগার Rs {price:,}-এ বিক্রি হতে পারে। প্রতিষ্ঠান দামের ওপর {margin}% মুনাফা চায়। লক্ষ্য-খরচ কত?", r,
               f"Target cost = target price - target profit = {price:,} x {1 - margin / 100:g} = Rs {_f(_c(r))}; design must hit it, not the other way round.",
               f"লক্ষ্য-খরচ = লক্ষ্য-দাম - লক্ষ্য-মুনাফা = {price:,} x {1 - margin / 100:g} = Rs {_f(_c(r))}; নকশাকেই একে ছুঁতে হবে, উল্টোটা নয়।",
               (price / (1 + margin / 100), price * margin / 100, r * 1.1))


def lab_eff(sr, sh, ah):
    r = abs(sr * (sh - ah))
    fav = sh >= ah
    return _rs(f"Standard time for a batch of slabs is {sh:,} hours at Rs {sr} an hour, but {ah:,} hours were actually worked. What is the labour efficiency variance, and is it favourable?",
               f"একগুচ্ছ স্ল্যাবের মানক সময় {sh:,} ঘণ্টা, ঘণ্টাপ্রতি Rs {sr}, কিন্তু প্রকৃত কাজ হয়েছে {ah:,} ঘণ্টা। শ্রম-দক্ষতা বিচ্যুতি কত, আর তা অনুকূল কি?", r,
               f"LEV = SR x (SH - AH) = {sr} x ({sh:,} - {ah:,}) = Rs {_f(_c(r))} {'favourable' if fav else 'adverse'}.",
               f"শ্রম-দক্ষতা বিচ্যুতি = SR x (SH - AH) = {sr} x ({sh:,} - {ah:,}) = Rs {_f(_c(r))} {'অনুকূল' if fav else 'প্রতিকূল'}।",
               (sr * ah, sr * sh, r * 2))


# ---------------------------------------------------------------- financial reporting
def deferred_tax(book_dep, tax_dep, rate):
    r = abs(tax_dep - book_dep) * rate / 100
    return _n(f"In year 1 a company charges depreciation of Rs {book_dep} lakh in its books but claims Rs {tax_dep} lakh for tax. The tax rate is {rate}%. What deferred tax liability arises (Rs lakh)?",
              f"প্রথম বছরে একটা কোম্পানি খাতায় Rs {book_dep} লক্ষ অবচয় ধরে কিন্তু করের জন্য Rs {tax_dep} লক্ষ দাবি করে। করহার {rate}%। কত বিলম্বিত কর-দায় তৈরি হয় (Rs লক্ষ)?", r,
              f"Temporary difference {tax_dep - book_dep} x {rate}% = {_f(_c(r))}: lower tax now, higher tax later when the difference reverses.",
              f"অস্থায়ী পার্থক্য {tax_dep - book_dep} x {rate}% = {_f(_c(r))}: এখন কম কর, পার্থক্য উল্টে গেলে পরে বেশি কর।",
              (tax_dep * rate / 100, tax_dep - book_dep, r * 2))


def diluted_eps(ni, shares, conv_int, tax, new_shares):
    r = (ni + conv_int * (1 - tax / 100)) / (shares + new_shares)
    return _rs(f"Net profit is Rs {ni} lakh on {shares} lakh shares. Convertible debentures carrying Rs {conv_int} lakh interest a year would convert into {new_shares} lakh shares; tax is {tax}%. What is diluted EPS?",
               f"নিট মুনাফা Rs {ni} লক্ষ, শেয়ার {shares} লক্ষ। বছরে Rs {conv_int} লক্ষ সুদের রূপান্তরযোগ্য ডিবেঞ্চার {new_shares} লক্ষ শেয়ারে বদলাবে; কর {tax}%। মিশ্রিত ইপিএস কত?", r,
               f"Add back after-tax interest: ({ni} + {conv_int} x {1 - tax / 100:g}) ÷ ({shares} + {new_shares}) = Rs {_f(_c(r))} (basic EPS Rs {_f(_c(ni / shares))}).",
               f"করোত্তর সুদ ফেরত যোগ করো: ({ni} + {conv_int} x {1 - tax / 100:g}) ÷ ({shares} + {new_shares}) = Rs {_f(_c(r))} (মূল ইপিএস Rs {_f(_c(ni / shares))})।",
               (ni / shares, ni / (shares + new_shares), (ni + conv_int) / (shares + new_shares) + 0.5))


def lease_liability(pay, rate, n):
    r = pay * (1 - (1 + rate / 100) ** -n) / (rate / 100)
    return _n(f"Under Ind AS 116, a company leases a crane for {n} years, paying Rs {pay} lakh at the end of each year. The incremental borrowing rate is {rate}%. What lease liability is recognised at the start (Rs lakh)?",
              f"Ind AS 116 অনুযায়ী একটা কোম্পানি {n} বছরের জন্য একটা ক্রেন লিজ নেয়, প্রতি বছরের শেষে Rs {pay} লক্ষ দেয়। বাড়তি ধারের হার {rate}%। শুরুতে কত লিজ-দায় স্বীকৃত হয় (Rs লক্ষ)?", r,
              f"Present value of the payments: {pay} x [1 - {1 + rate / 100:g}^-{n}] ÷ {rate / 100:g} = {_f(_c(r))}; a matching right-of-use asset is recorded.",
              f"কিস্তিগুলোর বর্তমান মূল্য: {pay} x [1 - {1 + rate / 100:g}^-{n}] ÷ {rate / 100:g} = {_f(_c(r))}; সমান ব্যবহারের-অধিকার সম্পদও লেখা হয়।",
              (pay * n, pay * n / (1 + rate / 100), r * 0.9))


def goodwill(cost, net_assets, pct):
    r = cost - net_assets * pct / 100
    return _n(f"A company pays Rs {cost} crore for {pct}% of a firm whose net assets are worth Rs {net_assets} crore at fair value. What goodwill arises on consolidation (proportionate method, Rs crore)?",
              f"একটা কোম্পানি ন্যায্যমূল্যে Rs {net_assets} কোটি নিট সম্পদের একটা প্রতিষ্ঠানের {pct}%-এর জন্য Rs {cost} কোটি দেয়। একত্রীকরণে কত সুনাম তৈরি হয় (আনুপাতিক পদ্ধতি, Rs কোটি)?", r,
              f"Goodwill = cost - share of net assets = {cost} - {pct / 100:g} x {net_assets} = {_f(_c(r))}.",
              f"সুনাম = খরচ - নিট সম্পদের অংশ = {cost} - {pct / 100:g} x {net_assets} = {_f(_c(r))}।",
              (cost - net_assets if cost > net_assets else r + 15, net_assets * pct / 100, r * 1.5))


def nci(net_assets, pct):
    r = net_assets * (100 - pct) / 100
    return _n(f"A parent owns {pct}% of a subsidiary with net assets of Rs {net_assets} crore. What non-controlling interest appears in the consolidated balance sheet (proportionate method, Rs crore)?",
              f"একটা মূল কোম্পানির Rs {net_assets} কোটি নিট সম্পদের সহায়ক কোম্পানিতে {pct}% মালিকানা। একত্রিত উদ্বৃত্তপত্রে কত অ-নিয়ন্ত্রক স্বার্থ দেখানো হয় (আনুপাতিক পদ্ধতি, Rs কোটি)?", r,
              f"NCI = {100 - pct}% x {net_assets} = {_f(_c(r))}: the subsidiary is consolidated 100%, and the outside share is shown separately.",
              f"অ-নিয়ন্ত্রক স্বার্থ = {100 - pct}% x {net_assets} = {_f(_c(r))}: সহায়ককে 100% একত্রিত করা হয়, বাইরের অংশ আলাদা দেখানো হয়।",
              (net_assets * pct / 100, net_assets, r / 2))


def impairment(carrying, fv_less_cost, viu):
    rec = max(fv_less_cost, viu)
    r = max(0, carrying - rec)
    return _n(f"A machine is carried at Rs {carrying} lakh. Its fair value less costs to sell is Rs {fv_less_cost} lakh and its value in use is Rs {viu} lakh. What impairment loss is recognised (Rs lakh)?",
              f"একটা যন্ত্রের বহন-মূল্য Rs {carrying} লক্ষ। বিক্রয়-খরচ বাদে ন্যায্যমূল্য Rs {fv_less_cost} লক্ষ আর ব্যবহার-মূল্য Rs {viu} লক্ষ। কত ক্ষতিগ্রস্ততা-লোকসান স্বীকৃত হয় (Rs লক্ষ)?", r,
              f"Recoverable amount = higher of {fv_less_cost} and {viu} = {rec}; loss = {carrying} - {rec} = {_f(_c(r))}.",
              f"পুনরুদ্ধারযোগ্য অঙ্ক = {fv_less_cost} আর {viu}-এর বড়টি = {rec}; লোকসান = {carrying} - {rec} = {_f(_c(r))}।",
              (carrying - min(fv_less_cost, viu), abs(fv_less_cost - viu), r + 5))


def weighted_avg(o_q, o_r, p_q, p_r, issue):
    rate = (o_q * o_r + p_q * p_r) / (o_q + p_q)
    r = (o_q + p_q - issue) * rate
    return _rs(f"Opening stock is {o_q} bags at Rs {o_r}; {p_q} bags are bought at Rs {p_r}; then {issue} bags are issued. Using the weighted-average method, what is the value of closing stock?",
               f"প্রারম্ভিক মজুত {o_q} বস্তা Rs {o_r}-এ; {p_q} বস্তা কেনা হল Rs {p_r}-এ; তারপর {issue} বস্তা দেওয়া হল। ভারযুক্ত গড় পদ্ধতিতে সমাপনী মজুতের মূল্য কত?", r,
               f"Average rate = ({o_q} x {o_r} + {p_q} x {p_r}) ÷ {o_q + p_q} = Rs {_f(_c(rate))}; closing {o_q + p_q - issue} bags x {_f(_c(rate))} = Rs {_f(_c(r))}.",
               f"গড় হার = ({o_q} x {o_r} + {p_q} x {p_r}) ÷ {o_q + p_q} = Rs {_f(_c(rate))}; সমাপনী {o_q + p_q - issue} বস্তা x {_f(_c(rate))} = Rs {_f(_c(r))}।",
               ((o_q + p_q - issue) * p_r, (o_q + p_q - issue) * o_r, r + 500))


def sacrifice(old, new):
    r = F(old) - F(new)
    opts = []
    for x in (r, F(new), F(old), r * 2, r + F(1, 10)):
        s = _fs(x)
        if x > 0 and s not in opts:
            opts.append(s)
    opts = opts[:4]
    return mcq(f"Partner A's share falls from {_fs(old)} to {_fs(new)} when a new partner is admitted. What is A's sacrificing share?",
               opts, 0,
               f"Sacrifice = old share - new share = {_fs(old)} - {_fs(new)} = {_fs(r)}; the new partner compensates A for it through goodwill.",
               f"নতুন অংশীদার এলে অংশীদার A-এর অংশ {_fs(old)} থেকে কমে {_fs(new)} হয়। A-এর ত্যাগের অংশ কত?",
               opts,
               f"ত্যাগ = পুরোনো অংশ - নতুন অংশ = {_fs(old)} - {_fs(new)} = {_fs(r)}; নতুন অংশীদার সুনামের মাধ্যমে A-কে তা পূরণ করেন।")


def dso(recv, sales):
    r = recv / sales * 365
    return _n(f"A contractor's trade receivables are Rs {recv} lakh and annual credit sales Rs {sales} lakh. What is the average collection period?",
              f"একজন ঠিকাদারের বাণিজ্যিক পাওনা Rs {recv} লক্ষ আর বার্ষিক ধারে বিক্রি Rs {sales} লক্ষ। গড় আদায়কাল কত?", r,
              f"DSO = receivables ÷ credit sales x 365 = {recv} ÷ {sales} x 365 = {_f(_c(r))} days.",
              f"আদায়কাল = পাওনা ÷ ধারে বিক্রি x 365 = {recv} ÷ {sales} x 365 = {_f(_c(r))} দিন।",
              (sales / recv, r / 2, r + 15), " days", " দিন")


def roce(ebit, equity, ltd):
    r = ebit / (equity + ltd) * 100
    return _n(f"A company has EBIT of Rs {ebit} crore, equity of Rs {equity} crore and long-term debt of Rs {ltd} crore. What is its return on capital employed?",
              f"একটা কোম্পানির ইবিআইটি Rs {ebit} কোটি, ইকুইটি Rs {equity} কোটি আর দীর্ঘমেয়াদি ঋণ Rs {ltd} কোটি। নিয়োজিত মূলধনের ওপর আয় কত?", r,
              f"ROCE = EBIT ÷ (equity + long-term debt) = {ebit} ÷ {equity + ltd} = {_f(_c(r))}%; it judges how well all long-term capital is used.",
              f"আরওসিই = ইবিআইটি ÷ (ইকুইটি + দীর্ঘমেয়াদি ঋণ) = {ebit} ÷ {equity + ltd} = {_f(_c(r))}%; সব দীর্ঘমেয়াদি মূলধন কতটা ভালো ব্যবহার হয়, তা বিচার করে।",
              (ebit / equity * 100, ebit / ltd * 100, r + 5), "%")


def gst_payable(sales, out_rate, purchases, in_rate):
    r = sales * out_rate / 100 - purchases * in_rate / 100
    return _rs(f"A contractor bills Rs {sales:,} plus {out_rate}% GST and buys inputs of Rs {purchases:,} plus {in_rate}% GST, all eligible for credit. How much GST must be paid in cash?",
               f"একজন ঠিকাদার Rs {sales:,} আর {out_rate}% জিএসটি বিল করেন, আর Rs {purchases:,} আর {in_rate}% জিএসটি-র উপকরণ কেনেন, যার সবটাই ক্রেডিটযোগ্য। নগদে কত জিএসটি দিতে হবে?", r,
               f"Output tax {_f(_c(sales * out_rate / 100))} - input tax credit {_f(_c(purchases * in_rate / 100))} = Rs {_f(_c(r))}: tax only on value added.",
               f"বিক্রয়-কর {_f(_c(sales * out_rate / 100))} - উপকরণ-কর ক্রেডিট {_f(_c(purchases * in_rate / 100))} = Rs {_f(_c(r))}: কেবল যুক্ত মূল্যে কর।",
               (sales * out_rate / 100, (sales - purchases) * in_rate / 100, r + purchases * in_rate / 200))


NUMERIC = [
    little(6, 1.5), little(12, 0.75), little(20, 0.4),
    mm1_lq(40, 50), mm1_lq(15, 20), mm1_lq(7, 10),
    mm1_wq(4, 6), mm1_wq(8, 10), mm1_wq(3, 5),
    takt(480, 96), takt(450, 150), takt(900, 120),
    stations(330, 60), stations(470, 90), stations(1000, 150),
    learning(100, 80, 8), learning(200, 90, 4), learning(60, 85, 16),
    smoothing(500, 560, 0.2), smoothing(1200, 1050, 0.3), smoothing(800, 900, 0.5),
    mad([100, 120, 110, 130], [105, 115, 120, 125]), mad([50, 60, 55], [52, 57, 60]), mad([200, 180, 220, 210], [190, 195, 205, 215]),
    epq(12000, 400, 6, 100, 40), epq(24000, 600, 8, 200, 80), epq(9000, 250, 5, 60, 30),
    cpi(90, 100), cpi(150, 120), cpi(400, 500),
    spi(80, 100), spi(120, 110), spi(45, 60),
    eac(1000, 0.8), eac(500, 1.25), eac(240, 0.9),
    cpk(12.6, 11.4, 12.1, 0.1), cpk(25.5, 24.5, 25.0, 0.1), cpk(8.2, 7.8, 7.95, 0.05),
    taguchi(50, 302, 300), taguchi(20, 497, 500), taguchi(100, 151.5, 150),
    lp(30, 40, 1, 2, 40, 3, 2, 60), lp(5, 4, 6, 4, 24, 1, 2, 6), lp(20, 30, 2, 1, 100, 1, 3, 90),
    assignment(((9, 2, 7), (6, 4, 3), (5, 8, 1))), assignment(((4, 8, 6), (7, 3, 5), (6, 9, 2))), assignment(((12, 7, 9), (8, 9, 6), (7, 11, 10))),
    nw_corner((50, 70), (30, 40, 50), ((4, 6, 8), (5, 3, 7))), nw_corner((60, 40), (20, 50, 30), ((2, 5, 7), (6, 4, 3))),
    clv(50000, 80, 10), clv(20000, 70, 12), clv(100000, 90, 10),
    arc_elasticity(300, 10000, 330, 9000), arc_elasticity(400, 5000, 440, 4800), arc_elasticity(100, 2000, 90, 2600),
    multi_bep(300000, 50, 20, 2, 3), multi_bep(240000, 40, 80, 3, 1), multi_bep(500000, 25, 75, 1, 1),
    transfer_min(250, 400, 20, False), transfer_min(250, 400, 20, True), transfer_min(180, 300, 30, True),
    abc_cost(500000, 250, 40, "machine set-ups", "যন্ত্র-প্রস্তুতি"), abc_cost(120000, 600, 90, "purchase orders", "ক্রয়-আদেশ"),
    abc_cost(900000, 3000, 450, "inspection hours", "পরিদর্শন-ঘণ্টা"),
    target_cost(60000, 20), target_cost(150000, 15), target_cost(8000, 25),
    lab_eff(150, 1200, 1300), lab_eff(200, 800, 750), lab_eff(120, 2500, 2700),
    deferred_tax(40, 60, 30), deferred_tax(100, 150, 25), deferred_tax(75, 90, 35),
    diluted_eps(100, 10, 12, 30, 2), diluted_eps(240, 40, 20, 25, 5), diluted_eps(500, 50, 30, 30, 10),
    lease_liability(10, 10, 5), lease_liability(25, 8, 4), lease_liability(6, 12, 3),
    goodwill(90, 100, 80), goodwill(300, 400, 60), goodwill(55, 50, 100),
    nci(200, 80), nci(500, 60), nci(150, 75),
    impairment(100, 70, 85), impairment(250, 230, 210), impairment(60, 42, 39),
    weighted_avg(100, 300, 200, 330, 150), weighted_avg(500, 40, 300, 48, 600), weighted_avg(50, 1000, 150, 1200, 120),
    sacrifice(F(3, 5), F(1, 2)), sacrifice(F(1, 2), F(3, 8)), sacrifice(F(2, 3), F(1, 2)),
    dso(60, 365), dso(90, 540), dso(45, 300),
    roce(30, 150, 50), roce(80, 300, 100), roce(12, 60, 40),
    gst_payable(1000000, 18, 600000, 18), gst_payable(500000, 12, 300000, 18), gst_payable(2000000, 18, 1500000, 12),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    # ---------------------------------------------------------------- financial reporting (Ind AS)
    _q("Ind AS 115 recognises revenue using a five-step model. Which step comes right after identifying the contract?", ["Identify the performance obligations", "Recognise revenue", "Determine the transaction price", "Allocate the price"],
       "Contract → performance obligations → transaction price → allocation → recognise revenue as each obligation is satisfied.",
       "Ind AS 115 পাঁচ-ধাপের মডেলে আয় স্বীকার করে। চুক্তি শনাক্তের ঠিক পরের ধাপ কোনটি?", ["কার্য-দায়িত্ব শনাক্ত করা", "আয় স্বীকার করা", "লেনদেন-মূল্য নির্ধারণ", "মূল্য বণ্টন"],
       "চুক্তি → কার্য-দায়িত্ব → লেনদেন-মূল্য → বণ্টন → প্রতিটি দায়িত্ব পূরণ হলে আয় স্বীকার।"),
    _q("A contractor builds a flyover on the client's land over three years. Under Ind AS 115, revenue is usually recognised…", ["Over time, as progress is made (e.g. costs incurred ÷ total expected costs)", "Only when the flyover is handed over", "When the contract is signed", "When cash is received"],
       "The client controls the asset as it is built, so the obligation is satisfied over time; an expected loss is recognised at once.",
       "একজন ঠিকাদার তিন বছর ধরে ক্লায়েন্টের জমিতে একটা উড়ালপুল বানান। Ind AS 115 অনুযায়ী আয় সাধারণত স্বীকৃত হয়…", ["সময়ের সঙ্গে, অগ্রগতি অনুযায়ী (যেমন খরচ হয়েছে ÷ মোট প্রত্যাশিত খরচ)", "কেবল উড়ালপুল হস্তান্তরের সময়", "চুক্তি সইয়ের সময়", "নগদ পাওয়ার সময়"],
       "নির্মাণের সঙ্গে সঙ্গে সম্পদ ক্লায়েন্টের নিয়ন্ত্রণে, তাই দায়িত্ব সময়ের সঙ্গে পূরণ হয়; প্রত্যাশিত লোকসান সঙ্গে সঙ্গে স্বীকৃত হয়।"),
    _q("Under Ind AS 116, how does a lessee account for most leases?", ["It records a right-of-use asset and a lease liability on the balance sheet", "It only expenses the rent each year", "It ignores the lease", "It records the asset at the lessor's cost"],
       "The old operating-lease 'off balance sheet' treatment is gone for lessees, except short-term and low-value leases.",
       "Ind AS 116 অনুযায়ী ইজারাগ্রহীতা বেশির ভাগ লিজের হিসাব রাখে কীভাবে?", ["উদ্বৃত্তপত্রে ব্যবহারের-অধিকার সম্পদ আর লিজ-দায় লিখে", "প্রতি বছর কেবল ভাড়া খরচ ধরে", "লিজ উপেক্ষা করে", "ইজারাদাতার খরচে সম্পদ লিখে"],
       "ইজারাগ্রহীতার পুরোনো 'উদ্বৃত্তপত্রের বাইরে' পরিচালন-লিজ নেই, স্বল্পমেয়াদি আর কমমূল্যের লিজ ছাড়া।"),
    _q("A deferred tax asset for carried-forward losses may be recognised only when…", ["It is probable that future taxable profits will be available to use it", "The company made a loss this year", "The auditor agrees verbally", "The tax rate is zero"],
       "Without probable future profits the asset could never be realised, so prudence forbids recognising it.",
       "বহন-করা লোকসানের জন্য বিলম্বিত কর-সম্পদ স্বীকার করা যায় কেবল যখন…", ["এটা কাজে লাগানোর মতো ভবিষ্যৎ করযোগ্য মুনাফা পাওয়া সম্ভাব্য", "কোম্পানি এ বছর লোকসান করেছে", "নিরীক্ষক মুখে রাজি", "করহার শূন্য"],
       "সম্ভাব্য ভবিষ্যৎ মুনাফা না থাকলে সম্পদটি কখনো আদায় হবে না, তাই বিচক্ষণতা স্বীকৃতি নিষেধ করে।"),
    _q("How is goodwill from an acquisition treated under Ind AS?", ["Not amortised, but tested for impairment at least every year", "Written off immediately", "Amortised over 40 years", "Added to equity"],
       "It is allocated to cash-generating units, and an impairment of goodwill can never be reversed.",
       "অধিগ্রহণ থেকে পাওয়া সুনাম Ind AS-এ কীভাবে দেখানো হয়?", ["অবচয় হয় না, তবে অন্তত প্রতি বছর ক্ষতিগ্রস্ততা পরীক্ষা হয়", "সঙ্গে সঙ্গে বাদ দেওয়া হয়", "40 বছরে অবচয় হয়", "ইকুইটিতে যোগ হয়"],
       "এটা নগদ-সৃষ্টিকারী এককে বণ্টিত হয়, আর সুনামের ক্ষতিগ্রস্ততা কখনো উল্টানো যায় না।"),
    _q("An investor holding 30% of a company with significant influence (not control) accounts for it using…", ["The equity method", "Full consolidation", "Proportionate consolidation", "Fair value only, through the profit and loss"],
       "The investment is adjusted for the investor's share of the associate's profits; 20-50% voting power usually indicates significant influence.",
       "একজন বিনিয়োগকারী উল্লেখযোগ্য প্রভাবসহ (নিয়ন্ত্রণ নয়) একটা কোম্পানির 30% রাখলে হিসাব রাখেন…", ["ইকুইটি পদ্ধতিতে", "পূর্ণ একত্রীকরণে", "আনুপাতিক একত্রীকরণে", "কেবল লাভ-ক্ষতি দিয়ে ন্যায্যমূল্যে"],
       "সহযোগীর মুনাফায় বিনিয়োগকারীর অংশ অনুযায়ী বিনিয়োগ সমন্বিত হয়; সাধারণত 20-50% ভোটাধিকার উল্লেখযোগ্য প্রভাব বোঝায়।"),
    _q("Under Ind AS 110, an investor controls an investee when it has…", ["Power over it, exposure to variable returns, and the ability to use that power to affect those returns", "More than 10% of its shares", "A seat on its board only", "A long-term supply contract"],
       "Control, not just share percentage, decides consolidation - sometimes under 50% is enough.",
       "Ind AS 110 অনুযায়ী বিনিয়োগকারী বিনিয়োজিত প্রতিষ্ঠানকে নিয়ন্ত্রণ করেন যখন তাঁর আছে…", ["এর ওপর ক্ষমতা, পরিবর্তনশীল আয়ের ঝুঁকি, আর সেই আয়ে প্রভাব ফেলতে ক্ষমতা ব্যবহারের সামর্থ্য", "এর 10%-এর বেশি শেয়ার", "কেবল পর্ষদে একটা আসন", "দীর্ঘমেয়াদি সরবরাহ-চুক্তি"],
       "কেবল শেয়ারের শতাংশ নয়, নিয়ন্ত্রণই একত্রীকরণ ঠিক করে - কখনো 50%-এর কমেও যথেষ্ট।"),
    _q("A provision under Ind AS 37 is recognised when there is a present obligation from a past event, an outflow is probable, and…", ["A reliable estimate of the amount can be made", "The auditor signs a cheque", "The obligation is only possible, not probable", "Cash has already been paid"],
       "If the outflow is only possible, it is disclosed as a contingent liability; contingent assets are not recognised.",
       "Ind AS 37-এ সংস্থান স্বীকৃত হয় যখন অতীত ঘটনা থেকে বর্তমান দায় আছে, বহিঃপ্রবাহ সম্ভাব্য, আর…", ["অঙ্কটির নির্ভরযোগ্য অনুমান করা যায়", "নিরীক্ষক চেক সই করেন", "দায়টি কেবল সম্ভব, সম্ভাব্য নয়", "নগদ আগেই দেওয়া হয়েছে"],
       "বহিঃপ্রবাহ কেবল সম্ভব হলে সম্ভাব্য দায় হিসেবে প্রকাশ করা হয়; সম্ভাব্য সম্পদ স্বীকৃত হয় না।"),
    _q("A customer's bankruptcy after the year end confirms that a receivable was already doubtful at the year end. This is…", ["An adjusting event after the reporting period", "A non-adjusting event", "Irrelevant to the accounts", "A change in accounting policy"],
       "Adjusting events give evidence of conditions at the balance sheet date; a fire after year end is non-adjusting (disclosed only).",
       "বছর শেষের পরে একজন ক্রেতার দেউলিয়া হওয়া নিশ্চিত করে যে পাওনাটি বছর শেষেই সন্দেহজনক ছিল। এটা…", ["প্রতিবেদন-কালের পরের সমন্বয়ী ঘটনা", "অসমন্বয়ী ঘটনা", "হিসাবে অপ্রাসঙ্গিক", "হিসাব-নীতির পরিবর্তন"],
       "সমন্বয়ী ঘটনা উদ্বৃত্তপত্রের তারিখের অবস্থার প্রমাণ দেয়; বছর শেষের পরের আগুন অসমন্বয়ী (কেবল প্রকাশ)।"),
    _q("Fair value measured from quoted prices for identical assets in active markets is in which level of the fair value hierarchy?", ["Level 1", "Level 2", "Level 3", "Level 4"],
       "Level 2 uses other observable inputs; Level 3 relies on unobservable inputs such as the firm's own models.",
       "সক্রিয় বাজারে অভিন্ন সম্পদের উদ্ধৃত দাম থেকে মাপা ন্যায্যমূল্য ন্যায্যমূল্য-স্তরবিন্যাসের কোন স্তরে?", ["স্তর 1", "স্তর 2", "স্তর 3", "স্তর 4"],
       "স্তর 2 অন্য পর্যবেক্ষণযোগ্য উপাদান ব্যবহার করে; স্তর 3 প্রতিষ্ঠানের নিজস্ব মডেলের মতো অপর্যবেক্ষণযোগ্য উপাদানে নির্ভর করে।"),
    _q("An auditor who finds the financial statements materially and pervasively misstated issues…", ["An adverse opinion", "An unmodified (clean) opinion", "A qualified opinion only for minor issues", "No report at all"],
       "A qualified opinion is for material but not pervasive issues; a disclaimer is given when the auditor cannot obtain enough evidence.",
       "আর্থিক বিবরণে গুরুতর আর সর্বব্যাপী ভুল পেলে নিরীক্ষক দেন…", ["প্রতিকূল মতামত", "অপরিবর্তিত (পরিষ্কার) মতামত", "কেবল ছোট বিষয়ে শর্তযুক্ত মতামত", "কোনো প্রতিবেদনই নয়"],
       "গুরুতর কিন্তু সর্বব্যাপী নয় এমন বিষয়ে শর্তযুক্ত মতামত; যথেষ্ট প্রমাণ না পেলে নিরীক্ষক মতামত দিতে অস্বীকার করেন।"),
    _q("Window dressing in financial statements means…", ["Making the year-end position look better than it really is, e.g. by delaying payments", "Decorating the annual report", "Revaluing land upwards honestly", "Paying dividends"],
       "Ratios like the current ratio can be inflated temporarily; analysts compare year-end figures with averages.",
       "আর্থিক বিবরণে উইন্ডো ড্রেসিং মানে…", ["বছর শেষের অবস্থাকে আসলের চেয়ে ভালো দেখানো, যেমন পরিশোধ পিছিয়ে", "বার্ষিক প্রতিবেদন সাজানো", "সৎভাবে জমির পুনর্মূল্যায়ন", "লভ্যাংশ দেওয়া"],
       "চলতি অনুপাতের মতো অনুপাত সাময়িকভাবে ফুলিয়ে দেখানো যায়; বিশ্লেষকরা বছর শেষের সংখ্যা গড়ের সঙ্গে তুলনা করেন।"),
    # ---------------------------------------------------------------- strategic cost management and control
    _q("Activity-based costing gives more accurate product costs than a single plant-wide rate because…", ["It charges overheads by the activities that actually cause them", "It ignores overheads", "It uses only direct labour hours", "It values stock at selling price"],
       "Low-volume, complex products often turn out to be under-costed by traditional absorption costing.",
       "একক কারখানা-ব্যাপী হারের চেয়ে কার্যভিত্তিক খরচ-নিরূপণ পণ্যের খরচ বেশি নির্ভুল দেয় কারণ…", ["যে কাজগুলো আসলে উপরিব্যয় ঘটায়, সেই অনুযায়ী তা চাপায়", "উপরিব্যয় উপেক্ষা করে", "কেবল প্রত্যক্ষ শ্রম-ঘণ্টা ব্যবহার করে", "বিক্রয়মূল্যে মজুত মূল্যায়ন করে"],
       "কম পরিমাণের জটিল পণ্য প্রায়ই প্রথাগত শোষণ-খরচে কম খরচের দেখায়।"),
    _q("Throughput accounting, from the theory of constraints, focuses on…", ["Maximising throughput (sales minus totally variable costs) per unit of the bottleneck resource", "Cutting labour costs first", "Building high inventory", "Allocating all overheads"],
       "Only the bottleneck limits output, so time lost there is lost for the whole plant.",
       "সীমাবদ্ধতা-তত্ত্ব থেকে আসা থ্রুপুট হিসাব মনোযোগ দেয়…", ["বাধা-সম্পদের প্রতি এককে থ্রুপুট (বিক্রি বাদ সম্পূর্ণ পরিবর্তনশীল খরচ) সর্বোচ্চ করায়", "আগে শ্রম-খরচ কমানোয়", "বেশি মজুত গড়ায়", "সব উপরিব্যয় বণ্টনে"],
       "কেবল বাধাটিই উৎপাদন সীমিত করে, তাই সেখানে হারানো সময় গোটা কারখানার জন্য হারানো।"),
    _q("A division manager judged on ROI rejects a project earning 15% because the division already earns 20%, though the company's cost of capital is 12%. This shows…", ["Dysfunctional behaviour that residual income can avoid", "Good goal congruence", "Correct decision making", "Over-capitalisation"],
       "Residual income = profit - cost of capital x investment, so any project beating 12% raises it.",
       "আরওআই দিয়ে বিচার হওয়া একজন বিভাগ-ব্যবস্থাপক 15% আয়ের প্রকল্প বাতিল করেন কারণ বিভাগ ইতিমধ্যে 20% আয় করে, যদিও কোম্পানির মূলধন-ব্যয় 12%। এটা দেখায়…", ["অবাঞ্ছিত আচরণ, যা অবশিষ্ট আয় দিয়ে এড়ানো যায়", "ভালো লক্ষ্য-সামঞ্জস্য", "সঠিক সিদ্ধান্ত", "অতি-মূলধনায়ন"],
       "অবশিষ্ট আয় = মুনাফা - মূলধন-ব্যয় x বিনিয়োগ, তাই 12% ছাড়ানো যেকোনো প্রকল্প এটা বাড়ায়।"),
    _q("A division whose manager controls revenues, costs and the assets invested is a…", ["Investment centre", "Cost centre", "Revenue centre", "Expense centre"],
       "Profit centres control revenue and costs but not investment; investment centres are judged by ROI, RI or EVA.",
       "যে বিভাগের ব্যবস্থাপক আয়, খরচ আর বিনিয়োজিত সম্পদ নিয়ন্ত্রণ করেন, তা হল…", ["বিনিয়োগ কেন্দ্র", "খরচ কেন্দ্র", "আয় কেন্দ্র", "ব্যয় কেন্দ্র"],
       "মুনাফা কেন্দ্র আয় আর খরচ নিয়ন্ত্রণ করে কিন্তু বিনিয়োগ নয়; বিনিয়োগ কেন্দ্রের বিচার আরওআই, অবশিষ্ট আয় বা ইভিএ দিয়ে।"),
    _q("The balanced scorecard measures performance from which four perspectives?", ["Financial, customer, internal business process, and learning and growth", "Sales, cost, profit and tax", "Past, present, future and risk", "Land, labour, capital and enterprise"],
       "Kaplan and Norton linked non-financial drivers to long-term financial results.",
       "ব্যালান্সড স্কোরকার্ড কোন চারটি দৃষ্টিকোণ থেকে কৃতি মাপে?", ["আর্থিক, গ্রাহক, অভ্যন্তরীণ ব্যবসা-প্রক্রিয়া, আর শিক্ষা ও বৃদ্ধি", "বিক্রি, খরচ, মুনাফা আর কর", "অতীত, বর্তমান, ভবিষ্যৎ আর ঝুঁকি", "জমি, শ্রম, মূলধন আর উদ্যোগ"],
       "ক্যাপলান আর নর্টন অ-আর্থিক চালকদের দীর্ঘমেয়াদি আর্থিক ফলের সঙ্গে যুক্ত করেন।"),
    _q("Zero-based budgeting means…", ["Every activity must justify its budget from zero each year", "Next year's budget is last year's plus inflation", "No budget is prepared", "Only capital spending is budgeted"],
       "It cuts waste but takes much more time than incremental budgeting.",
       "শূন্য-ভিত্তিক বাজেট মানে…", ["প্রতি বছর প্রতিটি কাজকে শূন্য থেকে তার বাজেটের যৌক্তিকতা দেখাতে হয়", "আগামী বছরের বাজেট = গত বছরের + মুদ্রাস্ফীতি", "কোনো বাজেট তৈরি হয় না", "কেবল মূলধনী ব্যয়ের বাজেট"],
       "এটা অপচয় কমায় কিন্তু ক্রমবর্ধিষ্ণু বাজেটের চেয়ে অনেক বেশি সময় নেয়।"),
    _q("Life-cycle costing of a bridge considers…", ["All costs from design and construction through maintenance to demolition", "Only the construction cost", "Only the first year's maintenance", "Only the land cost"],
       "A cheaper design with costly upkeep can lose to a dearer but durable one when whole-life costs are discounted.",
       "একটা সেতুর জীবনচক্র-খরচ বিবেচনা করে…", ["নকশা আর নির্মাণ থেকে রক্ষণাবেক্ষণ হয়ে ভেঙে ফেলা পর্যন্ত সব খরচ", "কেবল নির্মাণ-খরচ", "কেবল প্রথম বছরের রক্ষণাবেক্ষণ", "কেবল জমির খরচ"],
       "পুরো জীবনের খরচ বাট্টা করলে ব্যয়বহুল রক্ষণাবেক্ষণের সস্তা নকশা দামি কিন্তু টেকসই নকশার কাছে হারতে পারে।"),
    _q("Value engineering in construction aims to…", ["Deliver the required function at the lowest whole-life cost", "Use the most expensive materials", "Add features the client did not ask for", "Cut quality to save money"],
       "It questions each element: what does it do, what else could do it, and what would that cost?",
       "নির্মাণে মূল্য-প্রকৌশলের লক্ষ্য…", ["প্রয়োজনীয় কাজটি সর্বনিম্ন আজীবন খরচে দেওয়া", "সবচেয়ে দামি উপকরণ ব্যবহার", "ক্লায়েন্ট চাননি এমন বৈশিষ্ট্য যোগ", "টাকা বাঁচাতে গুণমান কমানো"],
       "এটা প্রতিটি অংশকে প্রশ্ন করে: এটা কী করে, আর কী তা করতে পারত, আর তাতে কত খরচ হত?"),
    _q("Kaizen costing differs from target costing because it…", ["Seeks small, continuous cost cuts during production rather than at the design stage", "Sets the selling price", "Ignores costs", "Is used only for services"],
       "Target costing works before launch; kaizen costing keeps improving afterwards.",
       "কাইজেন খরচ-নিরূপণ লক্ষ্য-খরচ থেকে আলাদা কারণ এটা…", ["নকশা-পর্যায়ে নয়, উৎপাদনের সময় ছোট ছোট অবিরাম খরচ-ছাঁটাই খোঁজে", "বিক্রয়মূল্য ঠিক করে", "খরচ উপেক্ষা করে", "কেবল পরিষেবায় ব্যবহৃত হয়"],
       "লক্ষ্য-খরচ চালুর আগে কাজ করে; কাইজেন খরচ পরে উন্নতি চালিয়ে যায়।"),
    _q("A material yield variance arises when…", ["The output obtained from a given input differs from the standard", "The purchase price differs from standard", "Workers are paid more", "Overheads are under-absorbed"],
       "The material usage variance splits into mix (proportions of inputs) and yield (output from the inputs).",
       "উপকরণ-ফলন বিচ্যুতি হয় যখন…", ["নির্দিষ্ট উপকরণ থেকে পাওয়া উৎপাদন মানক থেকে আলাদা হয়", "ক্রয়মূল্য মানক থেকে আলাদা হয়", "শ্রমিকরা বেশি বেতন পান", "উপরিব্যয় কম শোষিত হয়"],
       "উপকরণ-ব্যবহার বিচ্যুতি ভাগ হয় মিশ্রণ (উপকরণের অনুপাত) আর ফলনে (উপকরণ থেকে উৎপাদন)।"),
    # ---------------------------------------------------------------- operations and supply chain
    _q("Small changes in customer demand causing ever larger swings in orders further up the supply chain is called…", ["The bullwhip effect", "The Hawthorne effect", "Economies of scale", "The learning curve"],
       "Sharing point-of-sale data, smaller batches and vendor-managed inventory reduce it.",
       "গ্রাহক-চাহিদার ছোট পরিবর্তন সরবরাহ-শৃঙ্খলের উজানে ক্রমশ বড় অর্ডার-দোলা ঘটালে তাকে বলে…", ["চাবুক-প্রভাব (বুলহুইপ)", "হথর্ন প্রভাব", "বৃহদায়তনের সুবিধা", "শিখন-বক্ররেখা"],
       "বিক্রয়-বিন্দুর তথ্য ভাগ করা, ছোট ব্যাচ আর বিক্রেতা-পরিচালিত মজুত এটা কমায়।"),
    _q("In the theory of constraints, 'drum-buffer-rope' scheduling means…", ["The bottleneck sets the pace, a buffer protects it, and material release is tied to it", "Every machine runs at full speed", "Inventory is kept at zero everywhere", "Workers are paid by piece"],
       "Goldratt's five focusing steps: identify, exploit, subordinate, elevate, and repeat.",
       "সীমাবদ্ধতা-তত্ত্বে 'ড্রাম-বাফার-রোপ' সময়সূচি মানে…", ["বাধাটি গতি ঠিক করে, একটা বাফার তাকে রক্ষা করে, আর উপকরণ ছাড়া তার সঙ্গে বাঁধা", "প্রতিটি যন্ত্র পূর্ণ গতিতে চলে", "সর্বত্র মজুত শূন্য", "শ্রমিক টুকরোপ্রতি মজুরি পান"],
       "গোল্ডর‍্যাটের পাঁচ ধাপ: শনাক্ত, সদ্ব্যবহার, অধীনস্থ করা, উন্নীত করা, আবার করা।"),
    _q("Material requirements planning (MRP) uses which inputs to schedule purchases and production?", ["The master production schedule, the bill of materials and inventory records", "Only last year's sales", "Only the share price", "Only workers' attendance"],
       "It 'explodes' end-item demand into dependent demand for parts, offset by lead times.",
       "উপকরণ-চাহিদা পরিকল্পনা (এমআরপি) ক্রয় আর উৎপাদনের সময়সূচিতে কোন তথ্য ব্যবহার করে?", ["প্রধান উৎপাদন-সূচি, উপকরণ-তালিকা আর মজুতের নথি", "কেবল গত বছরের বিক্রি", "কেবল শেয়ারদর", "কেবল শ্রমিকদের হাজিরা"],
       "এটা চূড়ান্ত পণ্যের চাহিদাকে যন্ত্রাংশের নির্ভরশীল চাহিদায় 'বিস্ফোরিত' করে, সরবরাহ-সময় অনুযায়ী আগে-পিছে করে।"),
    _q("In aggregate planning, a 'chase' strategy means…", ["Changing output (hiring, overtime) to match demand each period", "Keeping output constant and using inventory", "Refusing extra orders", "Outsourcing everything permanently"],
       "A level strategy keeps the workforce steady and lets inventory or backorders absorb the swings.",
       "সামগ্রিক পরিকল্পনায় 'অনুসরণ' কৌশল মানে…", ["প্রতি পর্বে চাহিদার সঙ্গে মিলিয়ে উৎপাদন বদলানো (নিয়োগ, ওভারটাইম)", "উৎপাদন স্থির রেখে মজুত ব্যবহার", "বাড়তি অর্ডার প্রত্যাখ্যান", "স্থায়ীভাবে সব কিছু বাইরে করানো"],
       "সমতল কৌশল কর্মীসংখ্যা স্থির রাখে আর মজুত বা বকেয়া অর্ডার দোলা সামলায়।"),
    _q("A forecast's tracking signal stays well above +4 for months. This suggests…", ["The forecast is biased - it keeps under-forecasting demand", "The forecast is perfect", "Demand is random noise", "Inventory is too high"],
       "Tracking signal = running sum of errors ÷ MAD; a persistent sign means systematic bias.",
       "একটা পূর্বাভাসের ট্র্যাকিং সিগন্যাল মাসের পর মাস +4-এর অনেক ওপরে থাকে। এটা ইঙ্গিত করে…", ["পূর্বাভাসটি পক্ষপাতদুষ্ট - বারবার চাহিদা কম ধরছে", "পূর্বাভাস নিখুঁত", "চাহিদা এলোমেলো গোলমাল", "মজুত খুব বেশি"],
       "ট্র্যাকিং সিগন্যাল = ত্রুটির চলমান যোগফল ÷ এমএডি; চিহ্ন একই থাকলে নিয়মিত পক্ষপাত।"),
    _q("The Delphi method of forecasting…", ["Gathers expert opinions anonymously over several rounds until they converge", "Uses only past sales data", "Is a type of regression", "Asks customers to vote"],
       "Anonymity avoids dominant personalities; useful for new technologies with no history.",
       "পূর্বাভাসের ডেলফি পদ্ধতি…", ["কয়েক দফায় বেনামে বিশেষজ্ঞ-মত সংগ্রহ করে, যতক্ষণ না তা কাছাকাছি আসে", "কেবল অতীত বিক্রির তথ্য ব্যবহার করে", "এক ধরনের নির্ভরণ", "ক্রেতাদের ভোট নেয়"],
       "বেনামিতা প্রভাবশালী ব্যক্তিত্বের প্রভাব এড়ায়; ইতিহাসহীন নতুন প্রযুক্তিতে কার্যকর।"),
    _q("A process layout (functional layout) suits…", ["Low-volume, high-variety work such as a repair workshop", "High-volume production of one product", "A continuous chemical plant", "A single-product assembly line"],
       "Product (line) layouts suit high volume and low variety; cellular layouts group machines for part families.",
       "প্রক্রিয়া-বিন্যাস (কার্যভিত্তিক বিন্যাস) উপযুক্ত…", ["কম পরিমাণ আর বেশি বৈচিত্র্যের কাজে, যেমন মেরামতি কারখানা", "একটা পণ্যের বিপুল উৎপাদনে", "অবিরাম রাসায়নিক কারখানায়", "এক-পণ্যের অ্যাসেম্বলি লাইনে"],
       "পণ্য (লাইন) বিন্যাস বেশি পরিমাণ আর কম বৈচিত্র্যে উপযুক্ত; কোষ-বিন্যাস যন্ত্রাংশ-পরিবারের জন্য যন্ত্র একত্র করে।"),
    _q("In lean thinking, which of these is NOT one of the seven classic wastes (muda)?", ["Value-adding assembly work", "Overproduction", "Waiting", "Excess inventory"],
       "The seven wastes: transport, inventory, motion, waiting, overproduction, over-processing and defects (TIMWOOD).",
       "লিন-চিন্তায় এর কোনটি সাতটি চিরাচরিত অপচয়ের (মুডা) একটি নয়?", ["মূল্য-যোগকারী সংযোজন-কাজ", "অতি-উৎপাদন", "অপেক্ষা", "বাড়তি মজুত"],
       "সাতটি অপচয়: পরিবহন, মজুত, অঙ্গচালনা, অপেক্ষা, অতি-উৎপাদন, অতি-প্রক্রিয়াকরণ আর ত্রুটি।"),
    _q("A poka-yoke device on a production line…", ["Makes a mistake impossible or immediately obvious (mistake-proofing)", "Speeds up the conveyor", "Counts the workers", "Measures profit"],
       "Example: a jig into which a part fits only the right way round.",
       "উৎপাদন-লাইনে পোকা-ইয়োকে যন্ত্র…", ["ভুল অসম্ভব বা সঙ্গে সঙ্গে স্পষ্ট করে (ভুল-প্রতিরোধ)", "কনভেয়ার দ্রুত করে", "শ্রমিক গোনে", "মুনাফা মাপে"],
       "উদাহরণ: এমন জিগ যাতে যন্ত্রাংশ কেবল সঠিক দিকেই ঢোকে।"),
    _q("SMED (single-minute exchange of dies) aims to…", ["Cut set-up and changeover times sharply, making small batches economical", "Increase batch sizes", "Hire more workers", "Store more dies"],
       "Shingo separated internal set-up (machine stopped) from external set-up (done while running).",
       "এসএমইডি-র (এক-মিনিটে ডাই বদল) লক্ষ্য…", ["প্রস্তুতি আর বদলের সময় খুব কমানো, যাতে ছোট ব্যাচ লাভজনক হয়", "ব্যাচের আকার বাড়ানো", "বেশি শ্রমিক নিয়োগ", "বেশি ডাই মজুত রাখা"],
       "শিঙ্গো অভ্যন্তরীণ প্রস্তুতি (যন্ত্র বন্ধ) আর বাহ্যিক প্রস্তুতি (চলার সময়) আলাদা করেন।"),
    _q("A Kanban system is a…", ["Pull system where cards or signals authorise production only when downstream uses parts", "Push system driven by forecasts", "Type of accounting ledger", "Quality inspection report"],
       "Limiting the number of kanbans caps work-in-progress and exposes problems.",
       "কানবান ব্যবস্থা হল…", ["টান-ব্যবস্থা, যেখানে ভাটিতে যন্ত্রাংশ ব্যবহার হলে তবেই কার্ড বা সংকেত উৎপাদনের অনুমতি দেয়", "পূর্বাভাস-চালিত ঠেলা-ব্যবস্থা", "এক ধরনের হিসাবের খাতা", "গুণমান-পরিদর্শনের প্রতিবেদন"],
       "কানবানের সংখ্যা সীমিত রাখলে চলতি কাজ সীমিত থাকে আর সমস্যা প্রকাশ পায়।"),
    _q("An Ishikawa (fishbone) diagram helps a team to…", ["List possible causes of a problem under categories such as man, machine, method and material", "Track project costs", "Draw an organisation chart", "Plan a marketing budget"],
       "Combined with '5 Whys', it digs past symptoms to root causes.",
       "ইশিকাওয়া (মাছের কাঁটা) চিত্র একটা দলকে সাহায্য করে…", ["মানুষ, যন্ত্র, পদ্ধতি আর উপকরণের মতো শ্রেণিতে সমস্যার সম্ভাব্য কারণ তালিকা করতে", "প্রকল্পের খরচ অনুসরণ করতে", "সংগঠন-চিত্র আঁকতে", "বিপণন-বাজেট পরিকল্পনায়"],
       "'পাঁচবার কেন'-র সঙ্গে মিলিয়ে এটা লক্ষণ পেরিয়ে মূল কারণে পৌঁছয়।"),
    _q("In acceptance sampling, the producer's risk (α) is the chance of…", ["Rejecting a good lot", "Accepting a bad lot", "Never inspecting", "Shipping late"],
       "Consumer's risk (β) is accepting a bad lot; the operating characteristic curve shows both for a sampling plan.",
       "গ্রহণ-নমুনায়নে উৎপাদকের ঝুঁকি (α) হল সম্ভাবনা…", ["একটা ভালো লট বাতিলের", "একটা খারাপ লট গ্রহণের", "কখনো পরিদর্শন না করার", "দেরিতে পাঠানোর"],
       "ভোক্তার ঝুঁকি (β) খারাপ লট গ্রহণের; চালনা-বৈশিষ্ট্য বক্ররেখা একটা নমুনা-পরিকল্পনার দুটোই দেখায়।"),
    _q("Taguchi's idea of 'robust design' means…", ["Designing products that perform well even when conditions and inputs vary", "Making products as heavy as possible", "Inspecting every item twice", "Using only imported parts"],
       "His loss function says any deviation from target costs society something, not only defects outside limits.",
       "তাগুচির 'দৃঢ় নকশা' ধারণা মানে…", ["এমন পণ্যের নকশা, যা অবস্থা আর উপকরণ বদলালেও ভালো কাজ করে", "পণ্য যত সম্ভব ভারী করা", "প্রতিটি জিনিস দুবার পরিদর্শন", "কেবল আমদানি-করা যন্ত্রাংশ ব্যবহার"],
       "তাঁর ক্ষতি-অপেক্ষক বলে লক্ষ্য থেকে যেকোনো বিচ্যুতি সমাজের কিছু খরচ ঘটায়, কেবল সীমার বাইরের ত্রুটি নয়।"),
    _q("Deming's PDCA cycle stands for…", ["Plan, Do, Check (Study), Act", "Price, Demand, Cost, Access", "Prepare, Deliver, Close, Audit", "Product, Design, Control, Assure"],
       "It is the basic engine of continuous improvement in TQM and ISO 9001 quality systems.",
       "ডেমিংয়ের পিডিসিএ চক্র মানে…", ["পরিকল্পনা, কাজ, যাচাই (অধ্যয়ন), পদক্ষেপ", "দাম, চাহিদা, খরচ, প্রবেশ", "প্রস্তুতি, সরবরাহ, সমাপ্তি, নিরীক্ষা", "পণ্য, নকশা, নিয়ন্ত্রণ, নিশ্চয়তা"],
       "এটা টিকিউএম আর আইএসও 9001 গুণমান-ব্যবস্থায় অবিরাম উন্নতির মূল চালক।"),
    _q("What is generally considered 'world-class' overall equipment effectiveness (OEE)?", ["About 85%", "About 15%", "About 40%", "Exactly 100% every day"],
       "OEE = availability x performance x quality; many plants run at 40-60%.",
       "সাধারণভাবে 'বিশ্বমানের' সামগ্রিক যন্ত্র-কার্যকারিতা (ওইই) কত ধরা হয়?", ["প্রায় 85%", "প্রায় 15%", "প্রায় 40%", "প্রতিদিন ঠিক 100%"],
       "ওইই = প্রাপ্যতা x কৃতি x গুণমান; অনেক কারখানা 40-60%-এ চলে।"),
    _q("Vendor-managed inventory (VMI) means…", ["The supplier monitors the buyer's stock and decides when to replenish it", "The buyer keeps no records", "Inventory is owned by the government", "Stock is counted once a year"],
       "Sharing data this way reduces stock-outs and the bullwhip effect; cement and FMCG companies use it with dealers.",
       "বিক্রেতা-পরিচালিত মজুত (ভিএমআই) মানে…", ["সরবরাহকারী ক্রেতার মজুত নজরে রাখেন আর কখন পূরণ করবেন ঠিক করেন", "ক্রেতা কোনো নথি রাখেন না", "মজুতের মালিক সরকার", "বছরে একবার মজুত গোনা হয়"],
       "এভাবে তথ্য ভাগ করলে মজুত-শূন্যতা আর চাবুক-প্রভাব কমে; সিমেন্ট আর এফএমসিজি কোম্পানি বিক্রেতাদের সঙ্গে এটা ব্যবহার করে।"),
    # ---------------------------------------------------------------- project management
    _q("A project shows CPI = 0.85 and SPI = 1.1. What does this mean?", ["It is over budget but ahead of schedule", "It is under budget and behind schedule", "It is on budget and on schedule", "It has been cancelled"],
       "CPI < 1 means each rupee spent earns less than a rupee of planned work; SPI > 1 means more work is done than planned.",
       "একটা প্রকল্পে সিপিআই = 0.85 আর এসপিআই = 1.1। এর মানে কী?", ["বাজেট ছাড়িয়েছে কিন্তু সময়সূচির আগে", "বাজেটের নিচে আর সময়সূচির পেছনে", "বাজেট আর সময়সূচি দুটোই ঠিক", "প্রকল্প বাতিল"],
       "সিপিআই < 1 মানে খরচ হওয়া প্রতি টাকায় এক টাকার কম পরিকল্পিত কাজ; এসপিআই > 1 মানে পরিকল্পনার চেয়ে বেশি কাজ।"),
    _q("'Fast-tracking' a project schedule means…", ["Doing activities in parallel that were planned in sequence, at extra risk", "Adding resources to shorten activities", "Removing scope", "Delaying the start"],
       "Crashing adds cost to shorten critical activities; fast-tracking overlaps them and risks rework.",
       "প্রকল্প-সূচি 'ফাস্ট-ট্র্যাক' করা মানে…", ["ক্রমানুসারে পরিকল্পিত কাজগুলো বাড়তি ঝুঁকিতে সমান্তরালে করা", "কাজ ছোট করতে সম্পদ যোগ করা", "পরিধি কমানো", "শুরু পিছিয়ে দেওয়া"],
       "ক্র্যাশিং খরচ বাড়িয়ে জরুরি কাজ ছোট করে; ফাস্ট-ট্র্যাকিং কাজগুলো একসঙ্গে চালায়, পুনরায় কাজের ঝুঁকি থাকে।"),
    _q("Free float of an activity is…", ["The delay it can take without delaying the early start of any following activity", "The delay it can take without delaying the whole project", "Its duration", "Always equal to total float"],
       "Total float protects the project end date; free float protects the next activity's earliest start.",
       "একটা কাজের মুক্ত ফ্লোট হল…", ["পরের কোনো কাজের আদি-শুরু না পিছিয়ে যতটা দেরি নেওয়া যায়", "পুরো প্রকল্প না পিছিয়ে যতটা দেরি নেওয়া যায়", "এর স্থায়িত্বকাল", "সবসময় মোট ফ্লোটের সমান"],
       "মোট ফ্লোট প্রকল্পের শেষ তারিখ রক্ষা করে; মুক্ত ফ্লোট পরের কাজের আদি-শুরু রক্ষা করে।"),
    _q("A work breakdown structure (WBS) is…", ["A hierarchical breakdown of the project scope into deliverables and work packages", "A list of employees", "A budget for one month", "A risk register"],
       "Work packages at the lowest level are estimated, scheduled and assigned; nothing outside the WBS is in scope.",
       "কাজ-বিভাজন কাঠামো (ডব্লিউবিএস) হল…", ["প্রকল্পের পরিধিকে প্রদেয় আর কাজের প্যাকেজে স্তরভিত্তিক বিভাজন", "কর্মীদের তালিকা", "এক মাসের বাজেট", "ঝুঁকির খাতা"],
       "সবচেয়ে নিচের স্তরের কাজের প্যাকেজের অনুমান, সূচি আর দায়িত্ব ঠিক হয়; ডব্লিউবিএস-এর বাইরে কিছুই পরিধিতে নেই।"),
    _q("Resource levelling in project scheduling…", ["Shifts activities within their float to smooth resource use, possibly extending the project", "Always shortens the project", "Removes the critical path", "Adds new activities"],
       "If resources are limited, the project end date may have to move.",
       "প্রকল্প-সূচিতে সম্পদ-সমতলীকরণ…", ["সম্পদ-ব্যবহার মসৃণ করতে কাজগুলোকে তাদের ফ্লোটের মধ্যে সরায়, তাতে প্রকল্প লম্বা হতে পারে", "সবসময় প্রকল্প ছোট করে", "জরুরি পথ সরিয়ে দেয়", "নতুন কাজ যোগ করে"],
       "সম্পদ সীমিত হলে প্রকল্পের শেষ তারিখ সরাতে হতে পারে।"),
    _q("A RACI chart clarifies, for each task, who is…", ["Responsible, Accountable, Consulted and Informed", "Rich, Active, Careful and Idle", "Recruited, Appraised, Coached and Insured", "Reporting, Auditing, Costing and Invoicing"],
       "Only one person should be Accountable for each task.",
       "আরএসিআই চার্ট প্রতিটি কাজের জন্য স্পষ্ট করে কে…", ["দায়িত্বপ্রাপ্ত, জবাবদিহিকারী, পরামর্শদাতা আর অবহিত", "ধনী, সক্রিয়, সতর্ক আর অলস", "নিযুক্ত, মূল্যায়িত, প্রশিক্ষিত আর বিমাকৃত", "প্রতিবেদক, নিরীক্ষক, খরচ-নির্ধারক আর চালান-প্রস্তুতকারী"],
       "প্রতিটি কাজে কেবল একজন জবাবদিহিকারী থাকা উচিত।"),
]
CONCEPTS += [
    # ---------------------------------------------------------------- strategy
    _q("Which is one of Porter's five competitive forces?", ["The bargaining power of suppliers", "The interest rate", "The company's mission statement", "Employee turnover"],
       "The five: rivalry, threat of new entrants, threat of substitutes, buyer power and supplier power.",
       "পোর্টারের পাঁচটি প্রতিযোগিতামূলক শক্তির একটি কোনটি?", ["সরবরাহকারীর দর-কষাকষির ক্ষমতা", "সুদের হার", "কোম্পানির লক্ষ্য-বিবৃতি", "কর্মী-বদলের হার"],
       "পাঁচটি: প্রতিদ্বন্দ্বিতা, নতুন প্রবেশকারীর হুমকি, বিকল্পের হুমকি, ক্রেতার ক্ষমতা আর সরবরাহকারীর ক্ষমতা।"),
    _q("In the BCG matrix, a product with high market share in a slow-growing market is a…", ["Cash cow", "Star", "Question mark", "Dog"],
       "Cash cows fund stars (high share, high growth) and question marks (low share, high growth); dogs are candidates for exit.",
       "বিসিজি ম্যাট্রিক্সে ধীরগতির বাজারে বেশি বাজার-অংশের পণ্য হল…", ["নগদ গাভী", "তারকা", "প্রশ্নচিহ্ন", "কুকুর"],
       "নগদ গাভী তারকা (বেশি অংশ, বেশি বৃদ্ধি) আর প্রশ্নচিহ্নকে (কম অংশ, বেশি বৃদ্ধি) অর্থ জোগায়; কুকুর সরে যাওয়ার প্রার্থী।"),
    _q("In Ansoff's matrix, selling new products in new markets is…", ["Diversification - the riskiest growth option", "Market penetration", "Product development", "Market development"],
       "Penetration = existing products, existing markets; development strategies change one of the two.",
       "আনসফের ম্যাট্রিক্সে নতুন বাজারে নতুন পণ্য বেচা হল…", ["বৈচিত্র্যকরণ - সবচেয়ে ঝুঁকিপূর্ণ বৃদ্ধির পথ", "বাজার-প্রবেশ", "পণ্য-উন্নয়ন", "বাজার-উন্নয়ন"],
       "প্রবেশ = বর্তমান পণ্য, বর্তমান বাজার; উন্নয়ন-কৌশল দুটির একটিকে বদলায়।"),
    _q("Porter's generic strategies are cost leadership, differentiation and…", ["Focus (on a narrow segment)", "Diversification", "Vertical integration", "Downsizing"],
       "Firms 'stuck in the middle' without a clear strategy tend to earn below-average returns.",
       "পোর্টারের সাধারণ কৌশলগুলো হল খরচ-নেতৃত্ব, পার্থক্যকরণ আর…", ["কেন্দ্রীকরণ (একটা সরু অংশে)", "বৈচিত্র্যকরণ", "উল্লম্ব সংযুক্তি", "আকার ছোট করা"],
       "স্পষ্ট কৌশলহীন 'মাঝে আটকে থাকা' প্রতিষ্ঠান সাধারণত গড়ের নিচে আয় করে।"),
    _q("In Porter's value chain, which is a primary activity?", ["Inbound logistics", "Human resource management", "Technology development", "Procurement"],
       "Primary: inbound logistics, operations, outbound logistics, marketing and sales, service; the rest are support activities.",
       "পোর্টারের মূল্য-শৃঙ্খলে কোনটি প্রাথমিক কাজ?", ["অন্তর্মুখী সরবরাহ-ব্যবস্থা", "মানবসম্পদ ব্যবস্থাপনা", "প্রযুক্তি-উন্নয়ন", "সংগ্রহ"],
       "প্রাথমিক: অন্তর্মুখী সরবরাহ, পরিচালন, বহির্মুখী সরবরাহ, বিপণন ও বিক্রি, পরিষেবা; বাকিগুলো সহায়ক।"),
    _q("According to Prahalad and Hamel, a core competence…", ["Gives access to many markets, adds real customer value, and is hard to imitate", "Is any product the firm sells", "Is the company's head office", "Is a short-term cost saving"],
       "Honda's engine know-how across cars, bikes and generators is the classic example.",
       "প্রহ্লাদ আর হ্যামেলের মতে মূল দক্ষতা…", ["অনেক বাজারে প্রবেশ দেয়, গ্রাহককে প্রকৃত মূল্য দেয়, আর নকল করা কঠিন", "প্রতিষ্ঠানের বেচা যেকোনো পণ্য", "কোম্পানির প্রধান কার্যালয়", "স্বল্পমেয়াদি খরচ-সাশ্রয়"],
       "গাড়ি, মোটরবাইক আর জেনারেটরে হোন্ডার ইঞ্জিন-দক্ষতা চিরাচরিত উদাহরণ।"),
    _q("A blue ocean strategy aims to…", ["Create uncontested market space by offering new value, making competition irrelevant", "Fight rivals on price in a crowded market", "Sell only sea food", "Merge with the market leader"],
       "Red oceans are existing, bloody markets; Kim and Mauborgne's examples include Cirque du Soleil.",
       "ব্লু ওশান কৌশলের লক্ষ্য…", ["নতুন মূল্য দিয়ে প্রতিদ্বন্দ্বিতাহীন বাজার-পরিসর তৈরি, যাতে প্রতিযোগিতা অপ্রাসঙ্গিক হয়", "ভিড়ের বাজারে দামে প্রতিদ্বন্দ্বীর সঙ্গে লড়া", "কেবল সামুদ্রিক খাবার বেচা", "বাজার-নেতার সঙ্গে মিশে যাওয়া"],
       "রেড ওশান হল বিদ্যমান, রক্তাক্ত বাজার; কিম আর মবোর্নের উদাহরণে সার্ক দ্যু সোলেই।"),
    _q("In the VRIO framework, a resource gives sustained competitive advantage when it is…", ["Valuable, rare, costly to imitate, and the organisation is set up to exploit it", "Cheap and common", "Owned by the government", "Recorded in the balance sheet"],
       "Missing any one gives only parity or a temporary advantage.",
       "ভিআরআইও কাঠামোয় একটা সম্পদ টেকসই প্রতিযোগিতামূলক সুবিধা দেয় যখন তা…", ["মূল্যবান, বিরল, নকল করা ব্যয়বহুল, আর সংগঠন তা কাজে লাগাতে প্রস্তুত", "সস্তা আর সাধারণ", "সরকারের মালিকানাধীন", "উদ্বৃত্তপত্রে লেখা"],
       "যেকোনো একটা না থাকলে কেবল সমতা বা সাময়িক সুবিধা মেলে।"),
    _q("Christensen's 'disruptive innovation' typically…", ["Starts with simpler, cheaper products for overlooked customers and later moves up-market", "Means improving products for the most demanding customers", "Is any very expensive new technology", "Happens only in government"],
       "Incumbents ignore it because the first customers look unprofitable - until it is too late.",
       "ক্রিস্টেনসেনের 'বিঘ্নকারী উদ্ভাবন' সাধারণত…", ["উপেক্ষিত ক্রেতাদের জন্য সরল, সস্তা পণ্যে শুরু হয়ে পরে উঁচু বাজারে ওঠে", "সবচেয়ে চাহিদাসম্পন্ন ক্রেতার জন্য পণ্যের উন্নতি", "যেকোনো খুব দামি নতুন প্রযুক্তি", "কেবল সরকারে ঘটে"],
       "প্রথম ক্রেতারা অলাভজনক মনে হয় বলে প্রতিষ্ঠিত প্রতিষ্ঠান উপেক্ষা করে - যতক্ষণ না অনেক দেরি হয়।"),
    _q("The McKinsey 7S framework links strategy, structure and systems with…", ["Shared values, style, staff and skills", "Sales, stock, supply and service", "Shares, salaries, savings and spending", "Seven subsidiaries"],
       "The 'soft' S's are as important as the 'hard' ones for successful change.",
       "ম্যাককিনজি 7S কাঠামো কৌশল, কাঠামো আর ব্যবস্থাকে যুক্ত করে…", ["অভিন্ন মূল্যবোধ, শৈলী, কর্মী আর দক্ষতার সঙ্গে", "বিক্রি, মজুত, সরবরাহ আর পরিষেবার সঙ্গে", "শেয়ার, বেতন, সঞ্চয় আর ব্যয়ের সঙ্গে", "সাতটি সহায়ক কোম্পানির সঙ্গে"],
       "সফল পরিবর্তনে 'নরম' দিকগুলো 'শক্ত' দিকের মতোই গুরুত্বপূর্ণ।"),
    # ---------------------------------------------------------------- marketing
    _q("STP in marketing stands for…", ["Segmentation, targeting and positioning", "Sales, transport and pricing", "Strategy, tactics and planning", "Supply, trade and profit"],
       "Divide the market, choose the segments to serve, then build a clear place in customers' minds.",
       "বিপণনে এসটিপি মানে…", ["বিভাজন, লক্ষ্য-নির্ধারণ আর অবস্থান-নির্ধারণ", "বিক্রি, পরিবহন আর দাম", "কৌশল, কৌশলগত পদক্ষেপ আর পরিকল্পনা", "সরবরাহ, বাণিজ্য আর মুনাফা"],
       "বাজার ভাগ করো, কোন অংশে কাজ করবে বাছো, তারপর ক্রেতার মনে স্পষ্ট জায়গা গড়ো।"),
    _q("Launching a new product at a high price to recover development costs from early adopters is…", ["Price skimming", "Penetration pricing", "Cost-plus pricing", "Predatory pricing"],
       "Penetration pricing starts low to win share quickly; skimming suits innovative products with little competition.",
       "আগ্রহী প্রথম ক্রেতাদের থেকে উন্নয়ন-খরচ তুলতে নতুন পণ্য বেশি দামে ছাড়া হল…", ["স্কিমিং দাম (মাখন-তোলা দাম)", "প্রবেশ-দাম", "খরচ-যোগ দাম", "শিকারি দাম"],
       "প্রবেশ-দাম দ্রুত অংশ পেতে কম দামে শুরু করে; কম প্রতিযোগিতার উদ্ভাবনী পণ্যে স্কিমিং উপযুক্ত।"),
    _q("The Net Promoter Score (NPS) is calculated from customers' likelihood to recommend as…", ["% promoters (9-10) minus % detractors (0-6)", "Average score out of 10", "% of customers who complain", "Sales growth"],
       "It ranges from -100 to +100; passives (7-8) are not counted.",
       "নেট প্রোমোটার স্কোর (এনপিএস) ক্রেতার সুপারিশের সম্ভাবনা থেকে হিসাব হয়…", ["প্রবর্তকের % (9-10) বাদ বিরোধীর % (0-6)", "10-এর মধ্যে গড় নম্বর", "অভিযোগকারী ক্রেতার %", "বিক্রি-বৃদ্ধি"],
       "এটা -100 থেকে +100; নিষ্ক্রিয়রা (7-8) গোনা হয় না।"),
    _q("In Kotler's levels of a product, after-sales service, warranty and installation form the…", ["Augmented product", "Core benefit", "Actual product", "Generic product"],
       "Core = the basic benefit (shelter); actual = the designed product (the house); augmented = extra services.",
       "কোটলারের পণ্য-স্তরে বিক্রয়োত্তর পরিষেবা, ওয়ারেন্টি আর স্থাপন গড়ে…", ["বর্ধিত পণ্য", "মূল সুবিধা", "প্রকৃত পণ্য", "সাধারণ পণ্য"],
       "মূল = প্রাথমিক সুবিধা (আশ্রয়); প্রকৃত = নকশা-করা পণ্য (বাড়ি); বর্ধিত = বাড়তি পরিষেবা।"),
    _q("The AIDA model describes a buyer moving through…", ["Attention, interest, desire and action", "Analysis, investment, delivery and audit", "Advertising, inventory, demand and accounts", "Awareness, invoice, discount and approval"],
       "Advertising messages are designed to move customers step by step towards purchase.",
       "এআইডিএ মডেল ক্রেতার যাত্রা বর্ণনা করে…", ["মনোযোগ, আগ্রহ, আকাঙ্ক্ষা আর পদক্ষেপ", "বিশ্লেষণ, বিনিয়োগ, সরবরাহ আর নিরীক্ষা", "বিজ্ঞাপন, মজুত, চাহিদা আর হিসাব", "সচেতনতা, চালান, ছাড় আর অনুমোদন"],
       "বিজ্ঞাপনের বার্তা ক্রেতাকে ধাপে ধাপে কেনার দিকে নিয়ে যেতে নকশা করা হয়।"),
    _q("In business-to-business buying, the 'buying centre' is…", ["Everyone involved in a purchase decision - users, influencers, buyers, deciders and gatekeepers", "The purchase department's office", "A shopping mall", "The supplier's warehouse"],
       "Selling steel to a builder may mean convincing engineers, finance and the site manager, not just the purchase officer.",
       "প্রতিষ্ঠান-থেকে-প্রতিষ্ঠান কেনাকাটায় 'ক্রয়-কেন্দ্র' হল…", ["ক্রয়-সিদ্ধান্তে জড়িত সবাই - ব্যবহারকারী, প্রভাবক, ক্রেতা, সিদ্ধান্তকারী আর দ্বাররক্ষী", "ক্রয় বিভাগের অফিস", "একটা শপিং মল", "সরবরাহকারীর গুদাম"],
       "নির্মাতাকে ইস্পাত বেচতে কেবল ক্রয়-কর্মকর্তা নয়, প্রকৌশলী, অর্থবিভাগ আর সাইট-ম্যানেজারকেও রাজি করাতে হতে পারে।"),
    _q("The SERVQUAL model measures service quality as the gap between…", ["Customers' expectations and their perceptions of the service received", "Price and cost", "Sales and profit", "Staff salaries and output"],
       "Its five dimensions: reliability, assurance, tangibles, empathy and responsiveness (RATER).",
       "সার্ভকোয়াল মডেল পরিষেবার গুণমান মাপে কীসের ফারাক হিসেবে?", ["ক্রেতার প্রত্যাশা আর পাওয়া পরিষেবা সম্পর্কে তাঁর উপলব্ধির", "দাম আর খরচের", "বিক্রি আর মুনাফার", "কর্মী-বেতন আর উৎপাদনের"],
       "এর পাঁচটি মাত্রা: নির্ভরযোগ্যতা, আশ্বাস, দৃশ্যমান দিক, সহমর্মিতা আর তৎপরতা।"),
    _q("Brand equity is…", ["The extra value a brand name adds to a product beyond its functional benefits", "The share capital of a company", "The cost of advertising", "The number of products sold"],
       "It lets firms charge premiums and launch extensions; it can be measured by price premium or customer loyalty.",
       "ব্র্যান্ড ইকুইটি হল…", ["কার্যকর সুবিধার বাইরে ব্র্যান্ড-নাম পণ্যে যে বাড়তি মূল্য যোগ করে", "কোম্পানির শেয়ার-মূলধন", "বিজ্ঞাপনের খরচ", "বিক্রি হওয়া পণ্যের সংখ্যা"],
       "এতে প্রতিষ্ঠান বেশি দাম নিতে আর সম্প্রসারিত পণ্য ছাড়তে পারে; দামের প্রিমিয়াম বা ক্রেতা-আনুগত্য দিয়ে মাপা যায়।"),
    _q("Channel conflict happens when…", ["Different sales channels (e.g. dealers and the company's own online store) compete for the same customers", "Television channels change", "Two departments share an office", "A product has two colours"],
       "Clear territories, pricing rules and dealer margins reduce it.",
       "বিক্রয়-মাধ্যমের দ্বন্দ্ব হয় যখন…", ["আলাদা বিক্রয়-মাধ্যম (যেমন ডিলার আর কোম্পানির নিজস্ব অনলাইন দোকান) একই ক্রেতার জন্য প্রতিযোগিতা করে", "টেলিভিশন চ্যানেল বদলায়", "দুটি বিভাগ একটা অফিস ভাগ করে", "একটা পণ্যের দুটি রং"],
       "স্পষ্ট এলাকা, দামের নিয়ম আর ডিলার-মার্জিন এটা কমায়।"),
    # ---------------------------------------------------------------- organisational behaviour
    _q("According to Herzberg, salary and working conditions are…", ["Hygiene factors - their absence causes dissatisfaction, but they do not motivate by themselves", "The strongest motivators", "Irrelevant to work", "Self-actualisation needs"],
       "Motivators are achievement, recognition, the work itself, responsibility and growth.",
       "হার্জবার্গের মতে বেতন আর কাজের পরিবেশ হল…", ["স্বাস্থ্যবিধান উপাদান - না থাকলে অসন্তোষ হয়, কিন্তু নিজে থেকে প্রেরণা দেয় না", "সবচেয়ে শক্তিশালী প্রেরক", "কাজে অপ্রাসঙ্গিক", "আত্মোপলব্ধির চাহিদা"],
       "প্রেরক হল সাফল্য, স্বীকৃতি, কাজটি নিজে, দায়িত্ব আর বৃদ্ধি।"),
    _q("Vroom's expectancy theory says motivation depends on…", ["Expectancy x instrumentality x valence", "Salary alone", "The number of holidays", "Age and experience only"],
       "If any of the three is zero - effort will not lead to performance, performance will not be rewarded, or the reward is not valued - motivation collapses.",
       "ভ্রুমের প্রত্যাশা-তত্ত্ব বলে প্রেরণা নির্ভর করে…", ["প্রত্যাশা x সহায়কতা x আকর্ষণ-মূল্যের ওপর", "কেবল বেতনের ওপর", "ছুটির সংখ্যার ওপর", "কেবল বয়স আর অভিজ্ঞতার ওপর"],
       "তিনটির যেকোনো একটা শূন্য হলে - চেষ্টায় কৃতি হবে না, কৃতির পুরস্কার নেই, বা পুরস্কারের মূল্য নেই - প্রেরণা ভেঙে পড়ে।"),
    _q("McClelland's acquired-needs theory identifies the needs for achievement, power and…", ["Affiliation", "Food", "Security", "Esteem"],
       "High achievers like moderate-risk goals with clear feedback; effective managers often have a high need for institutional power.",
       "ম্যাকক্লেল্যান্ডের অর্জিত-চাহিদা তত্ত্ব সাফল্য, ক্ষমতা আর কোন চাহিদা চিহ্নিত করে?", ["সংযোগ (অন্তর্ভুক্তি)", "খাদ্য", "নিরাপত্তা", "আত্মসম্মান"],
       "উচ্চ-সাফল্যকামীরা স্পষ্ট প্রতিক্রিয়াসহ মাঝারি ঝুঁকির লক্ষ্য পছন্দ করেন; কার্যকর ব্যবস্থাপকের প্রায়ই প্রাতিষ্ঠানিক ক্ষমতার চাহিদা বেশি।"),
    _q("Tuckman's stages of team development, in order, are…", ["Forming, storming, norming, performing (and adjourning)", "Norming, forming, performing, storming", "Planning, doing, checking, acting", "Hiring, training, appraising, firing"],
       "Conflict in 'storming' is normal; teams that work through it agree norms and then perform.",
       "টাকম্যানের দল-বিকাশের পর্যায়গুলো ক্রমানুসারে…", ["গঠন, ঝড়, নিয়ম-স্থাপন, কৃতি (আর বিদায়)", "নিয়ম-স্থাপন, গঠন, কৃতি, ঝড়", "পরিকল্পনা, কাজ, যাচাই, পদক্ষেপ", "নিয়োগ, প্রশিক্ষণ, মূল্যায়ন, বরখাস্ত"],
       "'ঝড়'-পর্যায়ে দ্বন্দ্ব স্বাভাবিক; যে দল তা পেরোয়, তারা নিয়মে একমত হয়ে তারপর কৃতি দেখায়।"),
    _q("A leader who inspires followers with a vision and encourages them to look beyond self-interest is…", ["Transformational", "Transactional", "Laissez-faire", "Autocratic"],
       "Transactional leaders exchange rewards for performance; both styles have their place.",
       "যে নেতা দৃষ্টিভঙ্গি দিয়ে অনুসারীদের অনুপ্রাণিত করেন আর নিজস্বার্থের বাইরে দেখতে উৎসাহ দেন, তিনি…", ["রূপান্তরমূলক", "লেনদেনমূলক", "অবাধ (লেসে-ফেয়ার)", "স্বৈরাচারী"],
       "লেনদেনমূলক নেতা কৃতির বিনিময়ে পুরস্কার দেন; দুটি শৈলীরই নিজস্ব জায়গা আছে।"),
    _q("Hersey and Blanchard's situational leadership says the best style depends on…", ["The followers' readiness (competence and commitment)", "The leader's age", "The size of the office", "The company's profit"],
       "Styles move from telling, to selling, to participating, to delegating as followers develop.",
       "হার্সি আর ব্ল্যানচার্ডের পরিস্থিতিগত নেতৃত্ব বলে সেরা শৈলী নির্ভর করে…", ["অনুসারীদের প্রস্তুতির (দক্ষতা আর অঙ্গীকার) ওপর", "নেতার বয়সের ওপর", "অফিসের আকারের ওপর", "কোম্পানির মুনাফার ওপর"],
       "অনুসারীরা বিকশিত হলে শৈলী বলে দেওয়া থেকে বোঝানো, অংশগ্রহণ আর অর্পণে সরে।"),
    _q("A cohesive group that suppresses dissent and makes a poor decision to preserve harmony shows…", ["Groupthink", "Synergy", "Brainstorming", "Delegation"],
       "Remedies include a devil's advocate, outside experts and leaders who speak last.",
       "একটা ঐক্যবদ্ধ দল মতানৈক্য চেপে রেখে সম্প্রীতি বজায় রাখতে খারাপ সিদ্ধান্ত নিলে তা দেখায়…", ["গোষ্ঠী-চিন্তা (গ্রুপথিংক)", "সমন্বয়", "মস্তিষ্ক-ঝড়", "অর্পণ"],
       "প্রতিকার: শয়তানের উকিল, বাইরের বিশেষজ্ঞ আর শেষে কথা বলা নেতা।"),
    _q("The Hawthorne studies found that workers' productivity rose mainly because…", ["They felt observed and valued - social factors mattered", "Lighting was always brighter", "Wages were doubled", "Machines were replaced"],
       "This launched the human relations movement in management.",
       "হথর্ন গবেষণায় দেখা যায় শ্রমিকদের উৎপাদনশীলতা বেড়েছিল মূলত কারণ…", ["তাঁরা নিজেদের পর্যবেক্ষিত আর মূল্যবান মনে করেছিলেন - সামাজিক উপাদান গুরুত্বপূর্ণ", "আলো সবসময় উজ্জ্বল ছিল", "মজুরি দ্বিগুণ হয়েছিল", "যন্ত্র বদলানো হয়েছিল"],
       "এটা ব্যবস্থাপনায় মানব-সম্পর্ক আন্দোলনের সূচনা করে।"),
    _q("Job enrichment differs from job enlargement because it…", ["Adds responsibility and control (vertical loading), not just more tasks of the same level", "Simply adds more similar tasks", "Reduces pay", "Removes all decisions"],
       "Hackman and Oldham's job characteristics model links autonomy and feedback to motivation.",
       "কাজ-সমৃদ্ধকরণ কাজ-সম্প্রসারণ থেকে আলাদা কারণ এটা…", ["একই স্তরের আরও কাজ নয়, দায়িত্ব আর নিয়ন্ত্রণ যোগ করে (উল্লম্ব ভার)", "কেবল আরও একই রকম কাজ যোগ করে", "বেতন কমায়", "সব সিদ্ধান্ত সরিয়ে নেয়"],
       "হ্যাকম্যান আর ওল্ডহ্যামের কাজ-বৈশিষ্ট্য মডেল স্বাধীনতা আর প্রতিক্রিয়াকে প্রেরণার সঙ্গে যুক্ত করে।"),
    _q("A 360-degree appraisal collects feedback from…", ["Supervisors, peers, subordinates and sometimes customers and the employee", "Only the immediate boss", "Only the HR department", "Only customers"],
       "It gives a rounder picture but must be handled carefully to stay honest and constructive.",
       "360-ডিগ্রি মূল্যায়ন প্রতিক্রিয়া সংগ্রহ করে…", ["তত্ত্বাবধায়ক, সহকর্মী, অধস্তন আর কখনো ক্রেতা ও কর্মীর নিজের থেকে", "কেবল সরাসরি ঊর্ধ্বতনের থেকে", "কেবল মানবসম্পদ বিভাগ থেকে", "কেবল ক্রেতাদের থেকে"],
       "এটা পূর্ণাঙ্গ ছবি দেয়, তবে সৎ আর গঠনমূলক রাখতে সাবধানে সামলাতে হয়।"),
    _q("Mintzberg grouped a manager's ten roles into…", ["Interpersonal, informational and decisional roles", "Planning, organising and controlling", "Technical, human and conceptual skills", "Line and staff roles"],
       "For example: figurehead and leader (interpersonal), monitor and spokesperson (informational), entrepreneur and negotiator (decisional).",
       "মিন্টজবার্গ একজন ব্যবস্থাপকের দশটি ভূমিকাকে ভাগ করেন…", ["আন্তঃব্যক্তিক, তথ্যগত আর সিদ্ধান্তমূলক ভূমিকায়", "পরিকল্পনা, সংগঠন আর নিয়ন্ত্রণে", "প্রযুক্তিগত, মানবিক আর ধারণাগত দক্ষতায়", "লাইন আর স্টাফ ভূমিকায়"],
       "যেমন: প্রতীক আর নেতা (আন্তঃব্যক্তিক), নজরদার আর মুখপাত্র (তথ্যগত), উদ্যোক্তা আর আলোচক (সিদ্ধান্তমূলক)।"),
    # ---------------------------------------------------------------- business law (India)
    _q("Under the Indian Contract Act, how does a contract of guarantee differ from a contract of indemnity?", ["Guarantee has three parties (creditor, debtor, surety) and a secondary liability; indemnity has two parties", "They are exactly the same", "Indemnity always needs three parties", "A guarantee need not be enforceable"],
       "Section 124 defines indemnity and Section 126 guarantee; the surety pays only if the principal debtor fails.",
       "ভারতীয় চুক্তি আইনে নিশ্চয়তা-চুক্তি ক্ষতিপূরণ-চুক্তি থেকে কীভাবে আলাদা?", ["নিশ্চয়তায় তিন পক্ষ (পাওনাদার, দেনাদার, জামিনদার) আর গৌণ দায়; ক্ষতিপূরণে দুই পক্ষ", "এরা হুবহু এক", "ক্ষতিপূরণে সবসময় তিন পক্ষ লাগে", "নিশ্চয়তা বলবৎযোগ্য হতে হয় না"],
       "ধারা 124 ক্ষতিপূরণ আর ধারা 126 নিশ্চয়তার সংজ্ঞা দেয়; মূল দেনাদার ব্যর্থ হলে তবেই জামিনদার দেন।"),
    _q("Handing over goods to someone for a purpose, to be returned afterwards (such as a car left for repair), is…", ["Bailment", "Sale", "Gift", "Mortgage"],
       "A pledge is a bailment of goods as security for a loan; the bailee must take reasonable care of the goods.",
       "কোনো উদ্দেশ্যে কাউকে জিনিস দেওয়া, যা পরে ফেরত দিতে হবে (যেমন মেরামতে রাখা গাড়ি), হল…", ["গচ্ছিত (বেইলমেন্ট)", "বিক্রি", "দান", "বন্ধক"],
       "ঋণের জামানত হিসেবে জিনিস গচ্ছিত রাখা হল প্লেজ; গচ্ছিত-গ্রহীতাকে জিনিসের যথাযথ যত্ন নিতে হয়।"),
    _q("An agreement with a minor in India is…", ["Void from the beginning (void ab initio)", "Valid", "Voidable at the minor's option", "Valid only if written"],
       "Settled in Mohori Bibee v Dharmodas Ghose (1903); necessaries supplied to a minor can be recovered from the minor's property.",
       "ভারতে নাবালকের সঙ্গে চুক্তি…", ["শুরু থেকেই বাতিল", "বৈধ", "নাবালকের ইচ্ছায় বাতিলযোগ্য", "লিখিত হলে তবেই বৈধ"],
       "মোহরি বিবি বনাম ধর্মদাস ঘোষ (1903) মামলায় নিষ্পত্তি; নাবালককে দেওয়া প্রয়োজনীয় জিনিসের দাম তার সম্পত্তি থেকে আদায় করা যায়।"),
    _q("Under the Sale of Goods Act, a 'condition' differs from a 'warranty' because…", ["Breach of a condition lets the buyer reject the goods; breach of a warranty gives only a claim for damages", "They mean the same", "A warranty is more important", "Conditions apply only to services"],
       "Whether a term is a condition depends on whether it goes to the root of the contract.",
       "পণ্য বিক্রয় আইনে 'শর্ত' 'ওয়ারেন্টি' থেকে আলাদা কারণ…", ["শর্ত ভাঙলে ক্রেতা পণ্য প্রত্যাখ্যান করতে পারেন; ওয়ারেন্টি ভাঙলে কেবল ক্ষতিপূরণ দাবি", "দুটির মানে একই", "ওয়ারেন্টি বেশি গুরুত্বপূর্ণ", "শর্ত কেবল পরিষেবায় প্রযোজ্য"],
       "একটা শর্ত কিনা তা নির্ভর করে চুক্তির মূলে তা যায় কিনা তার ওপর।"),
    _q("Section 138 of the Negotiable Instruments Act makes it a criminal offence when…", ["A cheque issued to pay a debt bounces for insufficient funds and is not paid within 15 days of notice", "A cheque is crossed", "A bank closes early", "A cheque is written in pencil"],
       "The payee must send a notice within 30 days of the bounce; the drawer then has 15 days to pay.",
       "নিগোশিয়েবল ইনস্ট্রুমেন্টস আইনের ধারা 138 ফৌজদারি অপরাধ ধরে যখন…", ["দেনা শোধে দেওয়া চেক অপর্যাপ্ত তহবিলে ফেরত আসে আর নোটিসের 15 দিনের মধ্যে টাকা দেওয়া হয় না", "চেক ক্রস করা হয়", "ব্যাংক আগে বন্ধ হয়", "পেনসিলে চেক লেখা হয়"],
       "চেক ফেরতের 30 দিনের মধ্যে প্রাপককে নোটিস পাঠাতে হয়; তারপর প্রদানকারী 15 দিন পান।"),
    _q("Which body enforces the Competition Act, 2002 against cartels and abuse of dominance in India?", ["The Competition Commission of India (CCI)", "SEBI", "The RBI", "The Election Commission"],
       "The CCI has fined cement makers for cartelisation and also reviews large mergers.",
       "ভারতে কার্টেল আর আধিপত্যের অপব্যবহারের বিরুদ্ধে প্রতিযোগিতা আইন, 2002 কোন সংস্থা প্রয়োগ করে?", ["ভারতের প্রতিযোগিতা কমিশন (সিসিআই)", "সেবি", "রিজার্ভ ব্যাংক", "নির্বাচন কমিশন"],
       "সিসিআই কার্টেল গড়ার জন্য সিমেন্ট-প্রস্তুতকারকদের জরিমানা করেছে আর বড় সংযুক্তিও পর্যালোচনা করে।"),
    _q("In construction contracts, disputes are often settled under the Arbitration and Conciliation Act because arbitration…", ["Is private, faster than courts and decided by experts the parties choose", "Is always free", "Cannot be enforced", "Requires a jury"],
       "An arbitral award is binding and enforceable like a court decree, with limited grounds for challenge.",
       "নির্মাণ-চুক্তিতে বিবাদ প্রায়ই সালিশি ও মীমাংসা আইনে নিষ্পত্তি হয় কারণ সালিশি…", ["গোপনীয়, আদালতের চেয়ে দ্রুত আর পক্ষদের বাছাই করা বিশেষজ্ঞরা সিদ্ধান্ত নেন", "সবসময় বিনামূল্যে", "বলবৎ করা যায় না", "জুরি লাগে"],
       "সালিশি রোয় আদালতের ডিক্রির মতোই বাধ্যতামূলক আর বলবৎযোগ্য, চ্যালেঞ্জের সুযোগ সীমিত।"),
    _q("The Real Estate (Regulation and Development) Act, 2016 (RERA) requires developers to…", ["Register projects and keep 70% of buyers' money in a separate account for that project", "Build only government housing", "Sell flats only for cash", "Avoid giving possession dates"],
       "It aims at timely delivery and transparency; buyers can complain to the state RERA authority.",
       "রিয়েল এস্টেট (নিয়ন্ত্রণ ও উন্নয়ন) আইন, 2016 (রেরা) নির্মাতাদের বাধ্য করে…", ["প্রকল্প নিবন্ধন করতে আর ক্রেতাদের টাকার 70% সেই প্রকল্পের আলাদা অ্যাকাউন্টে রাখতে", "কেবল সরকারি আবাসন বানাতে", "কেবল নগদে ফ্ল্যাট বেচতে", "দখলের তারিখ না দিতে"],
       "লক্ষ্য সময়মতো হস্তান্তর আর স্বচ্ছতা; ক্রেতারা রাজ্যের রেরা কর্তৃপক্ষের কাছে অভিযোগ করতে পারেন।"),
    _q("Under GST's reverse charge mechanism…", ["The buyer, not the supplier, pays the GST to the government on notified supplies", "The government pays tax to the buyer", "No tax is paid", "The supplier pays double tax"],
       "It applies to items like services from goods transport agencies and purchases from certain unregistered suppliers.",
       "জিএসটি-র বিপরীত আদায় ব্যবস্থায়…", ["বিজ্ঞাপিত সরবরাহে সরবরাহকারী নয়, ক্রেতা সরকারকে জিএসটি দেন", "সরকার ক্রেতাকে কর দেয়", "কোনো কর দেওয়া হয় না", "সরবরাহকারী দ্বিগুণ কর দেন"],
       "পণ্য-পরিবহন সংস্থার পরিষেবা আর কিছু অনিবন্ধিত সরবরাহকারী থেকে কেনার মতো ক্ষেত্রে প্রযোজ্য।"),
    _q("An e-way bill under GST is needed when…", ["Goods worth more than Rs 50,000 are moved by vehicle", "Any service is provided", "A shop sells food over the counter", "Money is transferred by UPI"],
       "Generated online before movement, it lets tax officers track consignments and reduces evasion.",
       "জিএসটি-তে ই-ওয়ে বিল লাগে যখন…", ["Rs 50,000-এর বেশি মূল্যের পণ্য গাড়িতে সরানো হয়", "যেকোনো পরিষেবা দেওয়া হয়", "দোকানে কাউন্টারে খাবার বিক্রি হয়", "ইউপিআই-তে টাকা পাঠানো হয়"],
       "চলাচলের আগে অনলাইনে তৈরি হয়, কর-কর্মকর্তাদের চালান অনুসরণ করতে দেয় আর ফাঁকি কমায়।"),
    _q("The GST composition scheme suits small businesses because it…", ["Lets them pay tax at a low flat rate on turnover with simpler returns, but without input tax credit", "Removes all tax", "Lets them charge GST to customers at double rates", "Applies to all exporters"],
       "Composition dealers cannot collect GST on invoices or make inter-state supplies of goods.",
       "জিএসটি-র সংমিশ্রণ প্রকল্প ছোট ব্যবসার জন্য উপযুক্ত কারণ এটা…", ["সহজ রিটার্নে লেনদেনের ওপর কম সমান হারে কর দিতে দেয়, তবে উপকরণ-কর ক্রেডিট ছাড়া", "সব কর তুলে দেয়", "ক্রেতার কাছে দ্বিগুণ হারে জিএসটি নিতে দেয়", "সব রপ্তানিকারকের জন্য প্রযোজ্য"],
       "সংমিশ্রণ-ব্যবসায়ী চালানে জিএসটি নিতে বা আন্তঃরাজ্য পণ্য সরবরাহ করতে পারেন না।"),
    _q("A one person company (OPC) under the Companies Act 2013 allows…", ["A single individual to form a company with limited liability", "One company to own all others", "Only one share to be issued", "Unlimited liability for the owner"],
       "It gives sole entrepreneurs the benefits of a corporate form; a nominee is named for continuity.",
       "কোম্পানি আইন 2013-এর এক-ব্যক্তি কোম্পানি (ওপিসি) অনুমতি দেয়…", ["একজন ব্যক্তিকে সীমিত দায়সহ কোম্পানি গড়তে", "একটা কোম্পানিকে বাকি সব মালিকানায় রাখতে", "কেবল একটা শেয়ার ছাড়তে", "মালিকের অসীম দায়"],
       "একক উদ্যোক্তাকে কোম্পানি-রূপের সুবিধা দেয়; ধারাবাহিকতার জন্য একজন মনোনীত ব্যক্তির নাম থাকে।"),
    _q("The Sexual Harassment of Women at Workplace Act, 2013 (POSH) requires employers with 10 or more workers to…", ["Set up an Internal Committee to receive and inquire into complaints", "Ban women from night shifts", "Report to SEBI", "Close the office on weekends"],
       "Employers must also run awareness programmes; non-compliance attracts penalties.",
       "কর্মক্ষেত্রে নারীদের যৌন হয়রানি আইন, 2013 (পশ) 10 বা তার বেশি কর্মীর নিয়োগকর্তাকে বাধ্য করে…", ["অভিযোগ গ্রহণ আর তদন্তের জন্য একটা অভ্যন্তরীণ কমিটি গড়তে", "নারীদের রাতের শিফট নিষেধ করতে", "সেবিকে জানাতে", "সপ্তাহান্তে অফিস বন্ধ রাখতে"],
       "নিয়োগকর্তাকে সচেতনতা কর্মসূচিও চালাতে হয়; না মানলে জরিমানা।"),
    _q("Under the Foreign Exchange Management Act (FEMA), contraventions are treated as…", ["Civil offences, settled mainly by penalties", "Always criminal offences with jail", "Matters for the CCI", "Tax offences under GST"],
       "FEMA (1999) replaced the stricter FERA, reflecting liberalisation; the Enforcement Directorate administers it.",
       "বিদেশি মুদ্রা ব্যবস্থাপনা আইনে (ফেমা) লঙ্ঘনকে ধরা হয়…", ["দেওয়ানি অপরাধ হিসেবে, মূলত জরিমানায় নিষ্পত্তি", "সবসময় কারাদণ্ডসহ ফৌজদারি অপরাধ", "সিসিআই-এর বিষয়", "জিএসটি-র কর-অপরাধ"],
       "উদারীকরণের প্রতিফলনে ফেমা (1999) কঠোরতর ফেরার জায়গা নেয়; এনফোর্সমেন্ট ডিরেক্টরেট এটা পরিচালনা করে।"),
    _q("The Johari window helps people understand themselves by dividing awareness into which four areas?", ["Open, blind, hidden and unknown", "Past, present, future and never", "Strengths, weaknesses, opportunities and threats", "Plan, do, check and act"],
       "Feedback shrinks the blind area and self-disclosure shrinks the hidden area, enlarging the open area and trust in teams.",
       "জোহারি জানালা সচেতনতাকে কোন চারটি অঞ্চলে ভাগ করে মানুষকে নিজেকে বুঝতে সাহায্য করে?", ["খোলা, অন্ধ, লুকোনো আর অজানা", "অতীত, বর্তমান, ভবিষ্যৎ আর কখনো না", "শক্তি, দুর্বলতা, সুযোগ আর হুমকি", "পরিকল্পনা, কাজ, যাচাই আর পদক্ষেপ"],
       "প্রতিক্রিয়া অন্ধ অঞ্চল আর আত্মপ্রকাশ লুকোনো অঞ্চল ছোট করে, খোলা অঞ্চল আর দলে আস্থা বাড়ায়।"),
    _q("The GE-McKinsey nine-cell matrix judges business units on…", ["Industry attractiveness and business-unit strength", "Market share and market growth only", "Price and quality", "Assets and liabilities"],
       "It uses several factors on each axis, unlike the simpler two-variable BCG matrix.",
       "জিই-ম্যাককিনজি নয়-ঘরের ম্যাট্রিক্স ব্যবসা-এককের বিচার করে…", ["শিল্পের আকর্ষণ আর ব্যবসা-এককের শক্তি দিয়ে", "কেবল বাজার-অংশ আর বাজার-বৃদ্ধি দিয়ে", "দাম আর গুণমান দিয়ে", "সম্পদ আর দায় দিয়ে"],
       "সরল দুই-চলের বিসিজি ম্যাট্রিক্সের মতো নয়, এটা প্রতিটি অক্ষে কয়েকটি উপাদান ব্যবহার করে।"),
    _q("Critical chain project management protects the finish date mainly by…", ["Removing padding from individual tasks and pooling it into project and feeding buffers", "Adding extra time to every task", "Ignoring resources", "Starting every task as late as possible without buffers"],
       "Goldratt argued that safety hidden in each task is wasted by Parkinson's law and student syndrome.",
       "ক্রিটিক্যাল চেইন প্রকল্প-ব্যবস্থাপনা শেষ তারিখ রক্ষা করে মূলত…", ["প্রতিটি কাজ থেকে বাড়তি সময় সরিয়ে প্রকল্প আর সংযোগ-বাফারে জমিয়ে", "প্রতিটি কাজে বাড়তি সময় যোগ করে", "সম্পদ উপেক্ষা করে", "বাফার ছাড়াই প্রতিটি কাজ যত দেরিতে সম্ভব শুরু করে"],
       "গোল্ডর‍্যাট যুক্তি দেন, প্রতিটি কাজে লুকোনো নিরাপত্তা-সময় পার্কিনসনের সূত্র আর 'ছাত্র-লক্ষণে' নষ্ট হয়।"),
    _q("The main benefit of an enterprise resource planning (ERP) system is…", ["One integrated database linking finance, purchasing, inventory, production and HR", "Faster internet", "Replacing all managers", "Avoiding taxes"],
       "Data entered once is visible everywhere; implementation is costly and needs process redesign.",
       "এন্টারপ্রাইজ রিসোর্স প্ল্যানিং (ইআরপি) ব্যবস্থার মূল সুবিধা…", ["অর্থ, ক্রয়, মজুত, উৎপাদন আর মানবসম্পদকে যুক্ত করা একটা সমন্বিত তথ্যভান্ডার", "দ্রুত ইন্টারনেট", "সব ব্যবস্থাপকের প্রতিস্থাপন", "কর এড়ানো"],
       "একবার দেওয়া তথ্য সর্বত্র দেখা যায়; চালু করা ব্যয়বহুল আর প্রক্রিয়ার নতুন নকশা লাগে।"),
    _q("A person who receives goods delivered to them by mistake and uses them must pay for them, even without a contract. This is a…", ["Quasi-contract (Sections 68-72 of the Indian Contract Act)", "Void agreement", "Contract of guarantee", "Wagering agreement"],
       "The law imposes the obligation to prevent unjust enrichment.",
       "ভুল করে পাঠানো জিনিস পেয়ে কেউ ব্যবহার করলে চুক্তি না থাকলেও তার দাম দিতে হয়। এটা…", ["আধা-চুক্তি (ভারতীয় চুক্তি আইনের ধারা 68-72)", "বাতিল চুক্তি", "নিশ্চয়তা-চুক্তি", "বাজি-চুক্তি"],
       "অন্যায্য লাভ ঠেকাতে আইন এই দায় চাপায়।"),
    _q("The rule of caveat emptor in the sale of goods means…", ["Let the buyer beware - the buyer must check the goods, subject to exceptions such as fitness for a disclosed purpose", "The seller must always refund", "The government inspects all goods", "Goods can never be returned"],
       "Exceptions include sale by description, sale by sample and fraud by the seller.",
       "পণ্য বিক্রয়ে কেভিয়েট এম্পটর নিয়মের মানে…", ["ক্রেতা সাবধান - ক্রেতাকেই পণ্য যাচাই করতে হবে, জানানো উদ্দেশ্যে উপযুক্ততার মতো ব্যতিক্রম বাদে", "বিক্রেতাকে সবসময় টাকা ফেরত দিতে হবে", "সরকার সব পণ্য পরিদর্শন করে", "পণ্য কখনো ফেরত দেওয়া যায় না"],
       "ব্যতিক্রম: বর্ণনা অনুযায়ী বিক্রি, নমুনা অনুযায়ী বিক্রি আর বিক্রেতার প্রতারণা।"),
    _q("A whistle-blower policy in a listed Indian company exists so that…", ["Employees can report fraud or unethical conduct safely, without retaliation", "Managers can blow whistles during fire drills", "Shareholders get extra dividends", "Auditors can skip their checks"],
       "SEBI's listing rules require a vigil mechanism with direct access to the audit committee chair.",
       "তালিকাভুক্ত ভারতীয় কোম্পানিতে হুইসল-ব্লোয়ার নীতি থাকে যাতে…", ["কর্মীরা প্রতিশোধের ভয় ছাড়াই নিরাপদে প্রতারণা বা অনৈতিক আচরণ জানাতে পারেন", "অগ্নি-মহড়ায় ব্যবস্থাপকরা বাঁশি বাজাতে পারেন", "শেয়ারহোল্ডাররা বাড়তি লভ্যাংশ পান", "নিরীক্ষকরা যাচাই এড়াতে পারেন"],
       "সেবির তালিকাভুক্তি-নিয়মে নিরীক্ষা কমিটির সভাপতির কাছে সরাসরি পৌঁছনোর সতর্কতা-ব্যবস্থা বাধ্যতামূলক।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
