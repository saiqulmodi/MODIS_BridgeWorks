"""IIT level - Mathematics (JEE Advanced standard): combinatorics (derangements, onto functions,
distributions, dictionary rank, divisors), number theory and remainders, binomial and multinomial
coefficients, series and telescoping sums, roots of unity, theory of equations, determinants and
adjoints, limits, definite integrals (Wallis, Beta, Gamma, greatest integer), areas, differential
equations, conics, circles, 3-D geometry and vectors, probability and statistics, trigonometric
equations and inverse functions."""
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
    return f"{x:,}" if isinstance(x, int) else f"{x:g}"


def _n(q_en, q_bn, r, ex_en, ex_bn, alts):
    o = _o(_c(r), *alts)
    return mcq(q_en, [_f(x) for x in o], 0, ex_en, q_bn, [_f(x) for x in o], ex_bn)


def _k(c, var):
    """A coefficient written the usual way: x, not 1x."""
    return var if c == 1 else f"{c}{var}"


def _fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def _fr(q_en, q_bn, r, alts, ex_en, ex_bn):
    """A fraction answer such as 5/36, with distinct fraction distractors."""
    out = []
    for x in (r, *alts, r * 2, r / 2, r + F(1, 6), r * 3):
        x = F(x)
        if x > 0 and x not in out:
            out.append(x)
    opts = [_fs(x) for x in out[:4]]
    return mcq(q_en, opts, 0, ex_en, q_bn, opts, ex_bn)


# ---------------------------------------------------------------- combinatorics
def k_binom_sum(n):
    s = n * 2 ** (n - 1)
    return _n(f"What is the value of 1·ⁿC₁ + 2·ⁿC₂ + 3·ⁿC₃ + ... + n·ⁿCₙ for n = {n}?",
              f"n = {n} হলে 1·ⁿC₁ + 2·ⁿC₂ + 3·ⁿC₃ + ... + n·ⁿCₙ-এর মান কত?", s,
              f"k·ⁿCₖ = n·ⁿ⁻¹Cₖ₋₁, so the sum is n·2ⁿ⁻¹ = {n} x {2 ** (n - 1)} = {s}.",
              f"k·ⁿCₖ = n·ⁿ⁻¹Cₖ₋₁, তাই যোগফল n·2ⁿ⁻¹ = {n} x {2 ** (n - 1)} = {s}।",
              (2 ** n, n * 2 ** n, s - n))


def derangement(n):
    d = round(math.factorial(n) * sum((-1) ** k / math.factorial(k) for k in range(n + 1)))
    return _n(f"{n} letters are put into their {n} addressed envelopes at random. In how many ways can every letter go into a wrong envelope?",
              f"{n}টি চিঠি এলোমেলোভাবে তাদের ঠিকানা-লেখা {n}টি খামে ভরা হল। কত উপায়ে প্রতিটি চিঠি ভুল খামে যেতে পারে?", d,
              f"Derangements: Dₙ = n!(1 - 1/1! + 1/2! - ... ± 1/n!) = {d} for n = {n}.",
              f"বিন্যাস-বিচ্যুতি: Dₙ = n!(1 - 1/1! + 1/2! - ... ± 1/n!), n = {n} হলে {d}।",
              (math.factorial(n) - 1, math.factorial(n - 1), d + n))


def distribute(n, k, nonempty):
    if nonempty:
        r = math.comb(n - 1, k - 1)
        en, bn = "each box getting at least one", "প্রতিটি বাক্সে অন্তত একটি"
        ex = f"Stars and bars with no empty box: ⁿ⁻¹Cₖ₋₁ = {n - 1}C{k - 1} = {r}."
        exb = f"কোনো বাক্স খালি নয়, তারা-আর-দণ্ড পদ্ধতি: ⁿ⁻¹Cₖ₋₁ = {n - 1}C{k - 1} = {r}।"
        alts = (math.comb(n + k - 1, k - 1), k ** n if k ** n < 10 ** 6 else r + 7, math.comb(n, k))
    else:
        r = math.comb(n + k - 1, k - 1)
        en, bn = "boxes may be empty", "বাক্স খালি থাকতে পারে"
        ex = f"Stars and bars: ⁿ⁺ᵏ⁻¹Cₖ₋₁ = {n + k - 1}C{k - 1} = {r}."
        exb = f"তারা-আর-দণ্ড পদ্ধতি: ⁿ⁺ᵏ⁻¹Cₖ₋₁ = {n + k - 1}C{k - 1} = {r}।"
        alts = (math.comb(n - 1, k - 1), math.comb(n + k, k), r + k)
    return _n(f"In how many ways can {n} identical steel bolts be shared among {k} different crates ({en})?",
              f"{n}টি একই রকম ইস্পাতের বল্টু {k}টি আলাদা বাক্সে কত উপায়ে ভাগ করা যায় ({bn})?", r, ex, exb, alts)


def _divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def num_divisors(n):
    d = len(_divisors(n))
    return _n(f"How many positive divisors does {n:,} have?", f"{n:,}-এর কয়টি ধনাত্মক উৎপাদক আছে?", d,
              f"Write {n:,} as a product of prime powers p^a q^b ...; the count is (a + 1)(b + 1)... = {d}.",
              f"{n:,}-কে মৌলিক ঘাতের গুণফল p^a q^b ... হিসেবে লেখো; সংখ্যা = (a + 1)(b + 1)... = {d}।",
              (d - 2, d + 4, d // 2))


def sum_divisors(n):
    s = sum(_divisors(n))
    return _n(f"What is the sum of all positive divisors of {n}?", f"{n}-এর সব ধনাত্মক উৎপাদকের যোগফল কত?", s,
              f"σ(n) is multiplicative: for p^a it is (p^(a+1) - 1) ÷ (p - 1); multiplying over the prime powers of {n} gives {s}.",
              f"σ(n) গুণনীয়: p^a-এর জন্য (p^(a+1) - 1) ÷ (p - 1); {n}-এর মৌলিক ঘাতগুলোর জন্য গুণ করলে {s}।",
              (s - n, 2 * n, s + 1))


def remainder(a, n, m):
    r = pow(a, n, m)
    return _n(f"What is the remainder when {a}^{n} is divided by {m}?", f"{a}^{n}-কে {m} দিয়ে ভাগ করলে ভাগশেষ কত?", r,
              f"Find the cycle of {a}^k mod {m} (or use Fermat/Euler), reduce the exponent {n} within the cycle: remainder {r}.",
              f"{m} দিয়ে ভাগে {a}^k-এর ভাগশেষের চক্র খোঁজো (বা ফার্মা/অয়লার), ঘাত {n}-কে চক্রে নামাও: ভাগশেষ {r}।",
              (r + 1 if r + 1 < m else r - 1, (r * a) % m or m - 1, m - r if m - r != r else r + 2))


def coeff_power(n, r, a, b):
    c = math.comb(n, r) * a ** r * b ** (n - r)
    return _n(f"What is the coefficient of x^{r} in the expansion of ({_k(a, 'x')} + {b})^{n}?",
              f"({_k(a, 'x')} + {b})^{n}-এর বিস্তারে x^{r}-এর সহগ কত?", c,
              f"T = ⁿCᵣ (ax)^r b^(n-r): {math.comb(n, r)} x {a}^{r} x {b}^{n - r} = {c:,}.",
              f"পদ = ⁿCᵣ (ax)^r b^(n-r): {math.comb(n, r)} x {a}^{r} x {b}^{n - r} = {c:,}।",
              (math.comb(n, r) * a ** (n - r) * b ** r, math.comb(n, r) * a * b, c // a))


def coeff_total(a, b, n):
    s = (a + b) ** n
    sign = "+" if b >= 0 else "-"
    return _n(f"What is the sum of all the coefficients in the expansion of ({_k(a, 'x')} {sign} {abs(b)})^{n}?",
              f"({_k(a, 'x')} {sign} {abs(b)})^{n}-এর বিস্তারে সব সহগের যোগফল কত?", s,
              f"Put x = 1: ({a} {sign} {abs(b)})^{n} = {s}.", f"x = 1 বসাও: ({a} {sign} {abs(b)})^{n} = {s}।",
              (abs(a) ** n + abs(b) ** n, (abs(a) + abs(b)) ** n if b < 0 else s + n, 2 ** n))


def dict_rank(word):
    letters = sorted(word)
    rank = 1
    rest = list(word)
    for ch in word:
        smaller = sorted(set(x for x in rest if x < ch))
        for s_ in smaller:
            rest2 = list(rest)
            rest2.remove(s_)
            rank += len(set(permutations(rest2)))
        rest.remove(ch)
    total = len(set(permutations(letters)))
    return _n(f"All arrangements of the letters of {word} are listed in dictionary order. What is the rank of {word} itself?",
              f"{word}-এর অক্ষরগুলোর সব বিন্যাস অভিধানের ক্রমে সাজানো হল। {word} নিজে কত নম্বরে আসে?", rank,
              f"Count the words that start with a smaller letter at each position (fixing the earlier letters), then add 1: rank {rank} of {total}.",
              f"প্রতিটি অবস্থানে আগের অক্ষর স্থির রেখে ছোট অক্ষর দিয়ে শুরু শব্দ গোনো, তারপর 1 যোগ করো: {total}-এর মধ্যে {rank} নম্বর।",
              (rank - 1 if rank > 2 else rank + 3, total - rank + 1, rank + 120))


def onto(m, n):
    r = sum((-1) ** k * math.comb(n, k) * (n - k) ** m for k in range(n + 1))
    return _n(f"How many onto (surjective) functions are there from a set of {m} elements to a set of {n} elements?",
              f"{m} সদস্যের সেট থেকে {n} সদস্যের সেটে কয়টি উপরিচিত্রণ (সার্বিক অপেক্ষক) আছে?", r,
              f"Inclusion-exclusion: Σ (-1)^k ⁿCₖ (n - k)^m = {r}.", f"অন্তর্ভুক্তি-বর্জন: Σ (-1)^k ⁿCₖ (n - k)^m = {r}।",
              (n ** m, math.perm(m, n) if m >= n else r + 2, r + n))


def chessboard(n, squares):
    if squares:
        r = sum(k * k for k in range(1, n + 1))
        return _n(f"How many squares of all sizes are there on an {n} x {n} grid board?",
                  f"{n} x {n} ছকের বোর্ডে সব মাপের মোট কয়টি বর্গ আছে?", r,
                  f"k x k squares number (n - k + 1)²; summing gives 1² + 2² + ... + {n}² = {r}.",
                  f"k x k বর্গ আছে (n - k + 1)²টি; যোগ করলে 1² + 2² + ... + {n}² = {r}।",
                  (n * n, math.comb(n + 1, 2) ** 2, r + n))
    r = math.comb(n + 1, 2) ** 2
    return _n(f"How many rectangles (squares included) are there on an {n} x {n} grid board?",
              f"{n} x {n} ছকের বোর্ডে মোট কয়টি আয়তক্ষেত্র (বর্গসহ) আছে?", r,
              f"Choose 2 of the {n + 1} vertical and 2 of the {n + 1} horizontal lines: ({n + 1}C2)² = {r}.",
              f"{n + 1}টি খাড়া রেখার 2টি আর {n + 1}টি আনুভূমিক রেখার 2টি বাছো: ({n + 1}C2)² = {r}।",
              (sum(k * k for k in range(1, n + 1)), math.comb(n + 1, 2) * 2, r - n))


def triangles(n, k):
    r = math.comb(n, 3) - math.comb(k, 3)
    return _n(f"{n} points lie in a plane, and exactly {k} of them are collinear. How many triangles have their corners among these points?",
              f"একটা সমতলে {n}টি বিন্দু আছে, যার ঠিক {k}টি সমরেখ। এই বিন্দুগুলো শীর্ষ করে কয়টি ত্রিভুজ হয়?", r,
              f"ⁿC₃ - ᵏC₃ = {math.comb(n, 3)} - {math.comb(k, 3)} = {r}: collinear triples make no triangle.",
              f"ⁿC₃ - ᵏC₃ = {math.comb(n, 3)} - {math.comb(k, 3)} = {r}: সমরেখ তিনটি বিন্দু ত্রিভুজ গড়ে না।",
              (math.comb(n, 3), r - k, math.comb(n, 3) - k))


# ---------------------------------------------------------------- series
def agp_inf(den):
    x = F(1, den)
    s = x / (1 - x) ** 2
    return _fr(f"What is the sum of the infinite series 1·x + 2·x² + 3·x³ + ... when x = 1/{den}?",
               f"x = 1/{den} হলে অসীম শ্রেণি 1·x + 2·x² + 3·x³ + ...-এর যোগফল কত?", s,
               (x / (1 - x), 1 / (1 - x) ** 2, s + 1),
               f"Σ k xᵏ = x ÷ (1 - x)² = {_fs(x)} ÷ {_fs((1 - x) ** 2)} = {_fs(s)}.",
               f"Σ k xᵏ = x ÷ (1 - x)² = {_fs(x)} ÷ {_fs((1 - x) ** 2)} = {_fs(s)}।")


def telescoping(n):
    s = F(n, n + 1)
    return _fr(f"What is 1/(1·2) + 1/(2·3) + 1/(3·4) + ... + 1/({n}·{n + 1})?",
               f"1/(1·2) + 1/(2·3) + 1/(3·4) + ... + 1/({n}·{n + 1})-এর মান কত?", s,
               (F(n - 1, n), F(1, n + 1), F(n + 1, n + 2)),
               f"1/(k(k + 1)) = 1/k - 1/(k + 1), so the sum telescopes to 1 - 1/{n + 1} = {_fs(s)}.",
               f"1/(k(k + 1)) = 1/k - 1/(k + 1), তাই মাঝের পদগুলো কেটে যায়: 1 - 1/{n + 1} = {_fs(s)}।")


def ap_divisible(d):
    first = -(-100 // d) * d
    last = 999 // d * d
    n = (last - first) // d + 1
    s = n * (first + last) // 2
    return _n(f"What is the sum of all three-digit numbers that are divisible by {d}?",
              f"{d} দিয়ে বিভাজ্য সব তিন-অঙ্কের সংখ্যার যোগফল কত?", s,
              f"AP from {first} to {last} with {n} terms: S = {n}/2 x ({first} + {last}) = {s:,}.",
              f"{first} থেকে {last} পর্যন্ত {n}টি পদের সমান্তর প্রগতি: যোগফল = {n}/2 x ({first} + {last}) = {s:,}।",
              (s - last, n * last, s + first))


# ---------------------------------------------------------------- algebra
def adj_det(n, d, twice):
    if twice:
        r = d ** ((n - 1) ** 2)
        return _n(f"A is a {n} x {n} matrix with |A| = {d}. What is |adj(adj A)|?",
                  f"A একটা {n} x {n} ম্যাট্রিক্স, |A| = {d}। |adj(adj A)| কত?", r,
                  f"|adj A| = |A|^(n-1), applied twice: |A|^((n-1)²) = {d}^{(n - 1) ** 2} = {r}.",
                  f"|adj A| = |A|^(n-1), দুবার প্রয়োগে: |A|^((n-1)²) = {d}^{(n - 1) ** 2} = {r}।",
                  (d ** (n - 1), d ** (2 * (n - 1)) if d ** (2 * (n - 1)) != r else r + d, d ** n))
    r = d ** (n - 1)
    return _n(f"A is a {n} x {n} matrix with determinant {d}. What is the determinant of its adjoint?",
              f"A একটা {n} x {n} ম্যাট্রিক্স, নির্ণায়ক {d}। এর অ্যাডজয়েন্টের নির্ণায়ক কত?", r,
              f"A·adj A = |A| I gives |A|·|adj A| = |A|ⁿ, so |adj A| = |A|^(n-1) = {d}^{n - 1} = {r}.",
              f"A·adj A = |A| I থেকে |A|·|adj A| = |A|ⁿ, তাই |adj A| = |A|^(n-1) = {d}^{n - 1} = {r}।",
              (d ** n, d * n, d))


def conj_power(n):
    r = n + 2
    return _n(f"How many complex numbers z satisfy z^{n} = z̄ (the conjugate of z)?",
              f"কয়টি জটিল সংখ্যা z-এর জন্য z^{n} = z̄ (z-এর অনুবন্ধী) সত্য?", r,
              f"|z|^{n} = |z| gives z = 0 or |z| = 1; then z^{n + 1} = z z̄ = 1 has {n + 1} roots. Total {r}.",
              f"|z|^{n} = |z| থেকে z = 0 বা |z| = 1; তখন z^{n + 1} = z z̄ = 1-এর {n + 1}টি বীজ। মোট {r}টি।",
              (n + 1, n, 2 * n))


def cubic_sq(a, b, c):
    r = a * a - 2 * b
    return _n(f"α, β, γ are the roots of x³ - {a}x² + {b}x - {c} = 0. What is α² + β² + γ²?",
              f"x³ - {a}x² + {b}x - {c} = 0-এর বীজ α, β, γ। α² + β² + γ² কত?", r,
              f"Σα = {a}, Σαβ = {b}; Σα² = (Σα)² - 2Σαβ = {a * a} - {2 * b} = {r}.",
              f"Σα = {a}, Σαβ = {b}; Σα² = (Σα)² - 2Σαβ = {a * a} - {2 * b} = {r}।",
              (a * a + 2 * b, a * a - b, a * a))


def am_gm_min(k):
    r = 2 * math.sqrt(k)
    return _n(f"What is the least value of x + {k}/x for x > 0?",
              f"x > 0 হলে x + {k}/x-এর ন্যূনতম মান কত?", r,
              f"AM ≥ GM: x + {k}/x ≥ 2√{k} = {_f(_c(r))}, with equality at x = {_f(_c(math.sqrt(k)))}.",
              f"সমান্তর গড় ≥ গুণোত্তর গড়: x + {k}/x ≥ 2√{k} = {_f(_c(r))}, সমতা x = {_f(_c(math.sqrt(k)))}-এ।",
              (k, math.sqrt(k), k + 1))


# ---------------------------------------------------------------- calculus
def lim_cos(k):
    r = F(k * k, 2)
    return _fr(f"What is the limit of (1 - cos {k}x) ÷ x² as x → 0?",
               f"x → 0 হলে (1 - cos {k}x) ÷ x²-এর সীমা কত?", r,
               (F(k * k), F(k, 2), F(k)),
               f"1 - cos {k}x = 2 sin²({_fs(F(k, 2))}x) ≈ {k * k}x²/2, so the limit is {_fs(r)}.",
               f"1 - cos {k}x = 2 sin²({_fs(F(k, 2))}x) ≈ {k * k}x²/2, তাই সীমা {_fs(r)}।")


def lim_tan_sin(k):
    r = F(k ** 3, 2)
    kx = _k(k, "x")
    return _fr(f"What is the limit of (tan {kx} - sin {kx}) ÷ x³ as x → 0?",
               f"x → 0 হলে (tan {kx} - sin {kx}) ÷ x³-এর সীমা কত?", r,
               (F(k ** 3, 6), F(k ** 3), F(k, 2)),
               f"tan u - sin u = tan u (1 - cos u) ≈ u·u²/2 with u = {kx}: limit {_fs(r)}.",
               f"tan u - sin u = tan u (1 - cos u) ≈ u·u²/2, u = {kx}: সীমা {_fs(r)}।")


def _wallis(n):
    num = math.prod(range(n - 1, 0, -2)) or 1
    den = math.prod(range(n, 0, -2))
    return F(num, den), n % 2 == 0


def _pi_str(fr, with_pi):
    if not with_pi:
        return _fs(fr)
    top = "π" if fr.numerator == 1 else f"{fr.numerator}π"
    return top if fr.denominator == 1 else f"{top}/{fr.denominator}"


def wallis(n):
    k, even = _wallis(n)
    val = k / 2 if even else k
    opts = []
    for fr, pi in ((val, even), (val, not even), (_wallis(n - 1)[0] / (2 if _wallis(n - 1)[1] else 1), _wallis(n - 1)[1]),
                   (val * 2, even), (val / 2, even)):
        s = _pi_str(fr, pi)
        if s not in opts:
            opts.append(s)
    opts = opts[:4]
    return mcq(f"What is the integral of sin^{n} x from 0 to π/2?", opts, 0,
               f"Wallis: ∫ sinⁿx = (n-1)/n x (n-3)/(n-2) x ... {'x π/2 for even n' if even else 'ending in 2/3 for odd n'} = {opts[0]}.",
               f"0 থেকে π/2 পর্যন্ত sin^{n} x-এর সমাকলের মান কত?", opts,
               f"ওয়ালিসের সূত্র: (n-1)/n x (n-3)/(n-2) x ... {'জোড় n-এ x π/2' if even else 'বিজোড় n-এ শেষে 2/3'} = {opts[0]}।")


def beta(m, n):
    r = F(math.factorial(m) * math.factorial(n), math.factorial(m + n + 1))
    return _fr(f"What is the integral of x^{m}(1 - x)^{n} from 0 to 1?",
               f"0 থেকে 1 পর্যন্ত x^{m}(1 - x)^{n}-এর সমাকলের মান কত?", r,
               (F(1, m + n + 1), F(1, (m + 1) * (n + 1)), r * 2),
               f"Beta integral: m! n! ÷ (m + n + 1)! = {math.factorial(m)} x {math.factorial(n)} ÷ {math.factorial(m + n + 1)} = {_fs(r)}.",
               f"বিটা সমাকল: m! n! ÷ (m + n + 1)! = {math.factorial(m)} x {math.factorial(n)} ÷ {math.factorial(m + n + 1)} = {_fs(r)}।")


def gamma(n):
    r = math.factorial(n)
    return _n(f"What is the integral of x^{n} e^(-x) from 0 to ∞?",
              f"0 থেকে ∞ পর্যন্ত x^{n} e^(-x)-এর সমাকলের মান কত?", r,
              f"Integrating by parts {n} times (the Gamma function) gives {n}! = {r}.",
              f"{n} বার খণ্ডশ সমাকলনে (গামা অপেক্ষক) পাওয়া যায় {n}! = {r}।",
              (math.factorial(n - 1), n, math.factorial(n + 1)))


def floor_int(k):
    r = k * (k - 1) // 2
    return _n(f"What is the integral of [x] (the greatest integer not exceeding x) from 0 to {k}?",
              f"0 থেকে {k} পর্যন্ত [x]-এর (x-এর চেয়ে বড় নয় এমন বৃহত্তম পূর্ণসংখ্যা) সমাকল কত?", r,
              f"[x] = j on [j, j + 1): the area is 0 + 1 + ... + {k - 1} = {r}.",
              f"[j, j + 1) ব্যবধিতে [x] = j: ক্ষেত্রফল 0 + 1 + ... + {k - 1} = {r}।",
              (k * (k + 1) // 2, k * k // 2, r + k))


def area_parabola_lr(a):
    r = F(8 * a * a, 3)
    return _fr(f"What is the area enclosed by the parabola y² = {4 * a}x and its latus rectum x = {a}?",
               f"অধিবৃত্ত y² = {4 * a}x আর তার নাভিলম্ব x = {a} দিয়ে ঘেরা ক্ষেত্রফল কত?", r,
               (F(4 * a * a, 3), F(2 * a * a), F(16 * a * a, 3)),
               f"2∫₀^{a} 2√({a}x) dx = (8/3)a² = {_fs(r)}.", f"2∫₀^{a} 2√({a}x) dx = (8/3)a² = {_fs(r)}।")


def area_parabola_line(c):
    r = F(4, 3) * F(int(round(math.sqrt(c)))) ** 3
    return _fr(f"What is the area between the parabola y = x² and the line y = {c}?",
               f"অধিবৃত্ত y = x² আর রেখা y = {c}-এর মাঝের ক্ষেত্রফল কত?", r,
               (F(2, 3) * F(int(round(math.sqrt(c)))) ** 3, F(2 * c), r + F(c)),
               f"The curves meet at x = ±{int(round(math.sqrt(c)))}; area = ∫({c} - x²) dx = (4/3) x {int(round(math.sqrt(c)))}³ = {_fs(r)}.",
               f"বক্ররেখা দুটো x = ±{int(round(math.sqrt(c)))}-এ মেলে; ক্ষেত্রফল = ∫({c} - x²) dx = (4/3) x {int(round(math.sqrt(c)))}³ = {_fs(r)}।")


def de_value(y0, m):
    r = y0 * m
    return _n(f"y satisfies dy/dx = y with y(0) = {y0}. What is y when x = ln {m}?",
              f"dy/dx = y আর y(0) = {y0}। x = ln {m} হলে y কত?", r,
              f"y = {y0}eˣ, so y(ln {m}) = {y0} x {m} = {r}.", f"y = {y0}eˣ, তাই y(ln {m}) = {y0} x {m} = {r}।",
              (y0 + m, m, y0 * m * m))


# ---------------------------------------------------------------- coordinate and 3-D geometry
def ellipse_lr(a, b):
    r = 2 * b * b / a
    return _n(f"What is the length of the latus rectum of the ellipse x²/{a * a} + y²/{b * b} = 1?",
              f"উপবৃত্ত x²/{a * a} + y²/{b * b} = 1-এর নাভিলম্বের দৈর্ঘ্য কত?", r,
              f"Latus rectum = 2b²/a = 2 x {b * b} ÷ {a} = {_f(_c(r))}.",
              f"নাভিলম্ব = 2b²/a = 2 x {b * b} ÷ {a} = {_f(_c(r))}।",
              (2 * a * a / b, b * b / a, 2 * b))


def directrix_gap(a, b):
    e = math.sqrt(1 - b * b / (a * a))
    r = 2 * a / e
    return _n(f"How far apart are the two directrices of the ellipse x²/{a * a} + y²/{b * b} = 1?",
              f"উপবৃত্ত x²/{a * a} + y²/{b * b} = 1-এর দুটি নিয়ামকের মধ্যে দূরত্ব কত?", r,
              f"e = √(1 - b²/a²) = {_f(_c(e))}; the directrices are x = ±a/e, so the gap is 2a/e = {_f(_c(r))}.",
              f"উৎকেন্দ্রতা = √(1 - b²/a²) = {_f(_c(e))}; নিয়ামক x = ±a/e, তাই দূরত্ব 2a/e = {_f(_c(r))}।",
              (2 * a * e, 2 * a, a / e))


def conjugate_e(e1):
    e2 = e1 / math.sqrt(e1 * e1 - 1)
    return _n(f"A hyperbola has eccentricity {e1}. What is the eccentricity of its conjugate hyperbola?",
              f"একটা পরাবৃত্তের উৎকেন্দ্রতা {e1}। এর অনুবন্ধী পরাবৃত্তের উৎকেন্দ্রতা কত?", e2,
              f"1/e₁² + 1/e₂² = 1, so e₂ = e₁ ÷ √(e₁² - 1) = {_f(_c(e2))}.",
              f"1/e₁² + 1/e₂² = 1, তাই e₂ = e₁ ÷ √(e₁² - 1) = {_f(_c(e2))}।",
              (1 / e1 + 1, math.sqrt(e1 * e1 - 1), e1))


def tangent_length(x, y, r):
    t = math.sqrt(x * x + y * y - r * r)
    return _n(f"What is the length of the tangent from the point ({x}, {y}) to the circle x² + y² = {r * r}?",
              f"বিন্দু ({x}, {y}) থেকে বৃত্ত x² + y² = {r * r}-এ টানা স্পর্শকের দৈর্ঘ্য কত?", t,
              f"√(S₁) = √({x}² + {y}² - {r * r}) = {_f(_c(t))}.", f"√(S₁) = √({x}² + {y}² - {r * r}) = {_f(_c(t))}।",
              (math.hypot(x, y), math.hypot(x, y) - r, t + r))


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def tetra(a, b, c):
    v = F(abs(_dot(a, _cross(b, c))), 6)
    return _fr(f"A tetrahedron has one corner at the origin and edges along the vectors {a}, {b} and {c}. What is its volume?",
               f"একটা চতুস্তলকের এক শীর্ষ মূলবিন্দুতে আর ধারগুলো ভেক্টর {a}, {b} আর {c} বরাবর। এর আয়তন কত?", v,
               (v * 6, v * 3, v * 2),
               f"V = |[a b c]| ÷ 6 = {abs(_dot(a, _cross(b, c)))} ÷ 6 = {_fs(v)}.",
               f"আয়তন = |[a b c]| ÷ 6 = {abs(_dot(a, _cross(b, c)))} ÷ 6 = {_fs(v)}।")


def skew_distance(a1, b1, a2, b2):
    n = _cross(b1, b2)
    d = abs(_dot(_sub(a2, a1), n)) / math.sqrt(_dot(n, n))
    return _n(f"What is the shortest distance between the lines r = {a1} + t{b1} and r = {a2} + s{b2}?",
              f"রেখা r = {a1} + t{b1} আর r = {a2} + s{b2}-এর মধ্যে ন্যূনতম দূরত্ব কত?", d,
              f"d = |(a₂ - a₁)·(b₁ x b₂)| ÷ |b₁ x b₂| with b₁ x b₂ = {n}: d = {_f(_c(d))}.",
              f"দূরত্ব = |(a₂ - a₁)·(b₁ x b₂)| ÷ |b₁ x b₂|, যেখানে b₁ x b₂ = {n}: {_f(_c(d))}।",
              (abs(_dot(_sub(a2, a1), n)), math.sqrt(_dot(_sub(a2, a1), _sub(a2, a1))), d + 1))


def point_plane(p, a, b, c, d):
    r = abs(a * p[0] + b * p[1] + c * p[2] + d) / math.sqrt(a * a + b * b + c * c)
    plane = (f"{_k(a, 'x')} {'+' if b >= 0 else '-'} {_k(abs(b), 'y')} {'+' if c >= 0 else '-'} {_k(abs(c), 'z')} "
             f"{'+' if d >= 0 else '-'} {abs(d)} = 0")
    return _n(f"What is the distance of the point {p} from the plane {plane}?",
              f"বিন্দু {p}-এর সমতল {plane} থেকে দূরত্ব কত?", r,
              f"|ax₀ + by₀ + cz₀ + d| ÷ √(a² + b² + c²) = {abs(a * p[0] + b * p[1] + c * p[2] + d)} ÷ {_f(_c(math.sqrt(a * a + b * b + c * c)))} = {_f(_c(r))}.",
              f"|ax₀ + by₀ + cz₀ + d| ÷ √(a² + b² + c²) = {abs(a * p[0] + b * p[1] + c * p[2] + d)} ÷ {_f(_c(math.sqrt(a * a + b * b + c * c)))} = {_f(_c(r))}।",
              (abs(a * p[0] + b * p[1] + c * p[2] + d), r * 3, r + 2))


# ---------------------------------------------------------------- probability, statistics, trigonometry
def three_dice(s):
    ways = sum(1 for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) if a + b + c == s)
    r = F(ways, 216)
    return _fr(f"Three fair dice are thrown. What is the probability that the total is {s}?",
               f"তিনটি নিরপেক্ষ ছক্কা ছোড়া হল। মোট {s} হওয়ার সম্ভাবনা কত?", r,
               (F(ways, 36) if ways < 36 else r + F(1, 216), F(ways + 3, 216), F(1, 18)),
               f"{ways} of the 216 equally likely outcomes give {s}, so P = {ways}/216 = {_fs(r)}.",
               f"216টি সমসম্ভব ফলাফলের {ways}টিতে মোট {s}, তাই সম্ভাবনা = {ways}/216 = {_fs(r)}।")


def exact_heads(n, k):
    r = F(math.comb(n, k), 2 ** n)
    return _fr(f"A fair coin is tossed {n} times. What is the probability of exactly {k} heads?",
               f"একটা নিরপেক্ষ মুদ্রা {n} বার ছোড়া হল। ঠিক {k}টি হেড পড়ার সম্ভাবনা কত?", r,
               (F(1, 2 ** n), F(k, n), F(math.comb(n, k), 2 ** (n + 1))),
               f"ⁿCₖ ÷ 2ⁿ = {math.comb(n, k)} ÷ {2 ** n} = {_fs(r)}.", f"ⁿCₖ ÷ 2ⁿ = {math.comb(n, k)} ÷ {2 ** n} = {_fs(r)}।")


def var_naturals(n):
    r = F(n * n - 1, 12)
    return _fr(f"What is the variance of the first {n} natural numbers 1, 2, ..., {n}?",
               f"প্রথম {n}টি স্বাভাবিক সংখ্যা 1, 2, ..., {n}-এর ভেদাঙ্ক কত?", r,
               (F(n * n + 1, 12), F(n + 1, 2), F(n * n - 1, 6)),
               f"Variance = (n² - 1) ÷ 12 = {n * n - 1} ÷ 12 = {_fs(r)}.", f"ভেদাঙ্ক = (n² - 1) ÷ 12 = {n * n - 1} ÷ 12 = {_fs(r)}।")


def trig_zeros(k):
    r = 2 * k + 1
    return _n(f"How many solutions does sin({k}x) = 0 have in the closed interval [0, 2π]?",
              f"বদ্ধ ব্যবধি [0, 2π]-এ sin({k}x) = 0-এর কয়টি সমাধান আছে?", r,
              f"{k}x = mπ gives x = mπ/{k} for m = 0, 1, ..., {2 * k}: {r} solutions.",
              f"{k}x = mπ থেকে x = mπ/{k}, m = 0, 1, ..., {2 * k}: {r}টি সমাধান।",
              (2 * k, k + 1, 2 * k - 1))


NUMERIC = [
    k_binom_sum(6), k_binom_sum(7), k_binom_sum(8), k_binom_sum(9), k_binom_sum(10), k_binom_sum(12),
    derangement(4), derangement(5), derangement(6),
    distribute(10, 3, False), distribute(10, 3, True), distribute(12, 4, False), distribute(12, 4, True),
    distribute(8, 5, False), distribute(15, 5, True),
    num_divisors(360), num_divisors(720), num_divisors(1000), num_divisors(2520), num_divisors(1260),
    sum_divisors(360), sum_divisors(100), sum_divisors(72),
    remainder(2, 100, 7), remainder(5, 30, 13), remainder(7, 77, 10), remainder(3, 41, 11), remainder(2, 50, 9),
    coeff_power(6, 2, 2, 3), coeff_power(7, 3, 1, 2), coeff_power(8, 5, 2, 1), coeff_power(5, 2, 3, 2),
    coeff_total(2, 1, 5), coeff_total(3, -1, 4), coeff_total(1, 2, 6),
    dict_rank("MOTHER"), dict_rank("BRIDGE"), dict_rank("CRANE"),
    onto(4, 2), onto(4, 3), onto(5, 3),
    chessboard(8, False), chessboard(8, True), chessboard(5, False), chessboard(5, True),
    triangles(10, 4), triangles(12, 5), triangles(15, 6),
    agp_inf(2), agp_inf(3), agp_inf(4),
    telescoping(10), telescoping(20), telescoping(99),
    ap_divisible(7), ap_divisible(9), ap_divisible(11),
    adj_det(3, 4, False), adj_det(3, 5, False), adj_det(4, 2, False), adj_det(3, 2, True), adj_det(3, 3, True),
    conj_power(3), conj_power(4), conj_power(5),
    cubic_sq(6, 11, 6), cubic_sq(7, 14, 8), cubic_sq(9, 26, 24),
    am_gm_min(9), am_gm_min(16), am_gm_min(25),
    lim_cos(2), lim_cos(3), lim_cos(4), lim_cos(6),
    lim_tan_sin(1), lim_tan_sin(2),
    wallis(3), wallis(4), wallis(5), wallis(6),
    beta(1, 1), beta(2, 1), beta(2, 2), beta(3, 1),
    gamma(3), gamma(4), gamma(5),
    floor_int(5), floor_int(7), floor_int(10),
    area_parabola_lr(1), area_parabola_lr(2), area_parabola_lr(3),
    area_parabola_line(1), area_parabola_line(4), area_parabola_line(9),
    de_value(2, 5), de_value(3, 4), de_value(5, 3),
    ellipse_lr(5, 3), ellipse_lr(4, 2), ellipse_lr(13, 12),
    directrix_gap(5, 4), directrix_gap(5, 3),
    conjugate_e(2), conjugate_e(1.25),
    tangent_length(5, 12, 5), tangent_length(7, 1, 5), tangent_length(6, 8, 6),
    tetra((1, 0, 0), (0, 2, 0), (0, 0, 3)), tetra((1, 2, 3), (0, 1, 1), (2, 0, 1)), tetra((2, 1, 0), (1, 3, 1), (0, 1, 4)),
    skew_distance((0, 0, 0), (1, 0, 0), (0, 0, 3), (0, 1, 0)),
    skew_distance((1, 2, 3), (1, -1, 1), (2, 4, 5), (2, 1, 1)),
    skew_distance((0, 0, 0), (1, 1, 0), (1, 0, 2), (0, 1, 1)),
    point_plane((1, 2, 3), 2, -1, 2, 6), point_plane((3, 1, -1), 1, 2, 2, -4), point_plane((0, 0, 0), 2, 3, 6, -14),
    three_dice(10), three_dice(9), three_dice(4),
    exact_heads(6, 3), exact_heads(5, 2), exact_heads(8, 4),
    var_naturals(5), var_naturals(7), var_naturals(11),
    trig_zeros(2), trig_zeros(3), trig_zeros(4),
]


def _q(en, opts_en, ex_en, bn, opts_bn, ex_bn):
    return mcq(en, opts_en, 0, ex_en, bn, opts_bn, ex_bn)


CONCEPTS = [
    # ---------------------------------------------------------------- functions and calculus
    _q("If f(x) = |x - 1| + |x - 2|, what is the least value of f?", ["1", "0", "2", "3"],
       "For 1 ≤ x ≤ 2 the two distances add up to the gap between 1 and 2, which is 1; outside that interval f grows.",
       "f(x) = |x - 1| + |x - 2| হলে f-এর ন্যূনতম মান কত?", ["1", "0", "2", "3"],
       "1 ≤ x ≤ 2 হলে দুটো দূরত্ব মিলে 1 আর 2-এর ব্যবধান, অর্থাৎ 1; ব্যবধির বাইরে f বাড়ে।"),
    _q("At how many points is f(x) = |x² - 4| not differentiable?", ["2", "0", "1", "4"],
       "The graph has sharp corners where x² - 4 changes sign, at x = -2 and x = 2.",
       "f(x) = |x² - 4| কয়টি বিন্দুতে অবকলনযোগ্য নয়?", ["2", "0", "1", "4"],
       "x² - 4 যেখানে চিহ্ন বদলায়, x = -2 আর x = 2-এ, লেখচিত্রে তীক্ষ্ণ কোণ হয়।"),
    _q("Where is the greatest integer function [x] discontinuous?", ["At every integer", "Nowhere", "Only at x = 0", "At every rational number"],
       "[x] jumps by 1 at each integer and is constant in between.",
       "বৃহত্তম পূর্ণসংখ্যা অপেক্ষক [x] কোথায় অসন্তত?", ["প্রতিটি পূর্ণসংখ্যায়", "কোথাও নয়", "কেবল x = 0-এ", "প্রতিটি মূলদ সংখ্যায়"],
       "প্রতিটি পূর্ণসংখ্যায় [x] 1 লাফ দেয়, মাঝখানে ধ্রুবক থাকে।"),
    _q("The function f(x) = x sin(1/x) for x ≠ 0, with f(0) = 0, is at x = 0…", ["Continuous but not differentiable", "Differentiable", "Discontinuous", "Not defined"],
       "|x sin(1/x)| ≤ |x| → 0 gives continuity, but (f(h) - f(0))/h = sin(1/h) has no limit.",
       "x ≠ 0-এ f(x) = x sin(1/x) আর f(0) = 0 হলে x = 0-এ অপেক্ষকটি…", ["সন্তত কিন্তু অবকলনযোগ্য নয়", "অবকলনযোগ্য", "অসন্তত", "সংজ্ঞাহীন"],
       "|x sin(1/x)| ≤ |x| → 0, তাই সন্তত; কিন্তু (f(h) - f(0))/h = sin(1/h)-এর কোনো সীমা নেই।"),
    _q("By the King's rule, ∫₀^(π/2) √(sin x) ÷ (√(sin x) + √(cos x)) dx equals…", ["π/4", "π/2", "1", "0"],
       "Replacing x by π/2 - x swaps sin and cos; adding the two forms gives 2I = π/2.",
       "রাজার নিয়মে ∫₀^(π/2) √(sin x) ÷ (√(sin x) + √(cos x)) dx-এর মান…", ["π/4", "π/2", "1", "0"],
       "x-এর জায়গায় π/2 - x বসালে sin আর cos বদলে যায়; দুটো রূপ যোগ করলে 2I = π/2।"),
    _q("If f is continuous and f(x) = f(a - x), then ∫₀^a x f(x) dx equals…", ["(a/2) ∫₀^a f(x) dx", "a ∫₀^a f(x) dx", "0", "∫₀^a f(x) dx"],
       "Substituting x → a - x gives I = ∫(a - x) f(x) dx, so 2I = a ∫ f(x) dx.",
       "f সন্তত আর f(x) = f(a - x) হলে ∫₀^a x f(x) dx-এর মান…", ["(a/2) ∫₀^a f(x) dx", "a ∫₀^a f(x) dx", "0", "∫₀^a f(x) dx"],
       "x → a - x বসালে I = ∫(a - x) f(x) dx, তাই 2I = a ∫ f(x) dx।"),
    _q("What does the Leibniz rule give for d/dx ∫₀^(x²) sin t dt?", ["2x sin(x²)", "sin(x²)", "cos(x²)", "2x cos(x²)"],
       "d/dx ∫ₐ^(g(x)) f(t) dt = f(g(x)) g'(x) = sin(x²) x 2x.",
       "লাইবনিৎস নিয়মে d/dx ∫₀^(x²) sin t dt কত?", ["2x sin(x²) রাশি", "sin(x²) রাশি", "cos(x²) রাশি", "2x cos(x²) রাশি"],
       "নিয়ম: d/dx ∫ₐ^(g(x)) f(t) dt = f(g(x)) g'(x) = sin(x²) x 2x।"),
    _q("What is the integrating factor of dy/dx + (1/x) y = x² (for x > 0)?", ["x", "eˣ", "1/x", "ln x"],
       "IF = e^(∫ P dx) = e^(ln x) = x; then d(xy)/dx = x³.",
       "dy/dx + (1/x) y = x² (x > 0)-এর সমাকল-গুণক কী?", ["x", "eˣ", "1/x", "ln x"],
       "সমাকল-গুণক = e^(∫ P dx) = e^(ln x) = x; তখন d(xy)/dx = x³।"),
    _q("dy/dx = (x + y)/(x - y) is which type of differential equation?", ["Homogeneous - solve with y = vx", "Linear in y", "Exact with separable variables", "Bernoulli of order 2"],
       "Numerator and denominator are both degree 1 in x and y, so the right side depends only on y/x.",
       "dy/dx = (x + y)/(x - y) কোন ধরনের অবকল সমীকরণ?", ["সমমাত্রিক - y = vx বসিয়ে সমাধান", "y-তে রৈখিক", "পৃথকযোগ্য চলের যথাযথ", "দ্বিতীয় মাত্রার বার্নুলি"],
       "লব আর হর দুটোই x আর y-তে মাত্রা 1, তাই ডান দিক কেবল y/x-এর ওপর নির্ভর করে।"),
    _q("A family of curves y = A eˣ + B e⁻ˣ has two arbitrary constants. Its differential equation is…", ["d²y/dx² = y", "dy/dx = y", "d²y/dx² = -y", "dy/dx = -y"],
       "Differentiating twice gives A eˣ + B e⁻ˣ back; the order equals the number of constants.",
       "বক্ররেখা-পরিবার y = A eˣ + B e⁻ˣ-এ দুটি যথেচ্ছ ধ্রুবক আছে। এর অবকল সমীকরণ…", ["d²y/dx² = y", "dy/dx = y", "d²y/dx² = -y", "dy/dx = -y"],
       "দুবার অবকলন করলে আবার A eˣ + B e⁻ˣ পাওয়া যায়; ক্রম ধ্রুবকের সংখ্যার সমান।"),
    _q("If f''(x) > 0 on an interval, the graph of f there is…", ["Concave up (bending upwards)", "Concave down", "A straight line", "Decreasing"],
       "The slope keeps increasing, so the curve lies above its tangents; f'' = 0 with a sign change marks an inflection.",
       "কোনো ব্যবধিতে f''(x) > 0 হলে সেখানে f-এর লেখচিত্র…", ["ঊর্ধ্ব-অবতল (ওপরের দিকে বাঁকা)", "নিম্ন-অবতল", "সরলরেখা", "হ্রাসমান"],
       "নতি বাড়তে থাকে, তাই বক্ররেখা স্পর্শকের ওপরে থাকে; চিহ্ন বদলানো f'' = 0 নতিপরিবর্তন বিন্দু।"),
    _q("For x > 0, which is larger: eˣ or 1 + x?", ["eˣ, always", "1 + x, always", "They are equal for all x", "It depends on x"],
       "g(x) = eˣ - 1 - x has g(0) = 0 and g'(x) = eˣ - 1 > 0 for x > 0, so g > 0.",
       "x > 0 হলে কোনটি বড়: eˣ না 1 + x?", ["সবসময় eˣ", "সবসময় 1 + x", "সব x-এ সমান", "x-এর ওপর নির্ভর করে"],
       "g(x) = eˣ - 1 - x-এ g(0) = 0 আর x > 0-এ g'(x) = eˣ - 1 > 0, তাই g > 0।"),
    _q("lim (x → ∞) (1 + 1/x)^x equals…", ["e", "1", "∞", "0"],
       "This is a definition of e ≈ 2.718; it is the 1^∞ form, solved by e^(lim x·(1/x)).",
       "x → ∞ হলে (1 + 1/x)^x-এর সীমা…", ["e", "1", "∞", "0"],
       "এটা e ≈ 2.718-এর একটা সংজ্ঞা; 1^∞ আকার, সমাধান e^(lim x·(1/x))।"),
    _q("Which of these functions is periodic?", ["sin x + cos 2x", "x sin x", "sin(x²)", "eˣ sin x"],
       "sin x has period 2π and cos 2x has period π; their sum repeats every 2π. The others grow or stretch.",
       "এদের মধ্যে কোন অপেক্ষক পর্যাবৃত্ত?", ["sin x + cos 2x অপেক্ষক", "x sin x অপেক্ষক", "sin(x²) অপেক্ষক", "eˣ sin x অপেক্ষক"],
       "sin x-এর পর্যায় 2π আর cos 2x-এর π; যোগফল প্রতি 2π-তে পুনরাবৃত্ত হয়। বাকিগুলো বাড়ে বা প্রসারিত হয়।"),
    _q("If f(x) = x³ + x, then f is…", ["One-one and onto from ℝ to ℝ", "Neither one-one nor onto", "Onto but not one-one", "One-one but not onto"],
       "f'(x) = 3x² + 1 > 0, so f strictly increases; it runs from -∞ to ∞, covering all of ℝ.",
       "f(x) = x³ + x হলে ℝ থেকে ℝ-এ f…", ["এক-এক আর উপরিচিত্রণ", "এক-এক বা উপরিচিত্রণ কোনোটাই নয়", "উপরিচিত্রণ কিন্তু এক-এক নয়", "এক-এক কিন্তু উপরিচিত্রণ নয়"],
       "f'(x) = 3x² + 1 > 0, তাই f কঠোরভাবে বর্ধমান; -∞ থেকে ∞ পর্যন্ত যায়, পুরো ℝ ঢাকে।"),
    _q("The graph of y = f⁻¹(x) is the reflection of y = f(x) in…", ["The line y = x", "The x-axis", "The y-axis", "The origin"],
       "Swapping x and y reflects every point (a, b) to (b, a).",
       "y = f⁻¹(x)-এর লেখচিত্র y = f(x)-এর প্রতিফলন…", ["y = x রেখায়", "x-অক্ষে", "y-অক্ষে", "মূলবিন্দুতে"],
       "x আর y বদলালে প্রতিটি বিন্দু (a, b) হয় (b, a)।"),
    _q("If f(x) + 2f(1/x) = 3x for x ≠ 0, what is f(1)?", ["1", "3", "2", "0"],
       "Put x = 1: f(1) + 2f(1) = 3, so f(1) = 1.",
       "x ≠ 0-এ f(x) + 2f(1/x) = 3x হলে f(1) কত?", ["1", "3", "2", "0"],
       "x = 1 বসাও: f(1) + 2f(1) = 3, তাই f(1) = 1।"),
    # ---------------------------------------------------------------- algebra and complex numbers
    _q("If 1, ω, ω² are the cube roots of unity, what is (1 - ω + ω²)(1 + ω - ω²)?", ["4", "0", "1", "2"],
       "1 + ω² = -ω and 1 + ω = -ω², so the product is (-2ω)(-2ω²) = 4ω³ = 4.",
       "1, ω, ω² এককের ঘনমূল হলে (1 - ω + ω²)(1 + ω - ω²) কত?", ["4", "0", "1", "2"],
       "1 + ω² = -ω আর 1 + ω = -ω², তাই গুণফল (-2ω)(-2ω²) = 4ω³ = 4।"),
    _q("What is the sum of the n-th roots of unity for n ≥ 2?", ["0", "1", "n", "-1"],
       "They are the roots of zⁿ - 1 = 0, whose zⁿ⁻¹ coefficient is 0; geometrically they balance around the origin.",
       "n ≥ 2 হলে এককের n-তম মূলগুলোর যোগফল কত?", ["0", "1", "n", "-1"],
       "এরা zⁿ - 1 = 0-এর বীজ, যার zⁿ⁻¹-এর সহগ 0; জ্যামিতিকভাবে মূলবিন্দুর চারপাশে ভারসাম্যে থাকে।"),
    _q("The locus of z with |z - 1| = |z + 1| is…", ["The imaginary axis", "The real axis", "A circle of radius 1", "The line y = x"],
       "Points equidistant from 1 and -1 lie on their perpendicular bisector, Re z = 0.",
       "|z - 1| = |z + 1| হলে z-এর সঞ্চারপথ…", ["কাল্পনিক অক্ষ", "বাস্তব অক্ষ", "1 ব্যাসার্ধের বৃত্ত", "y = x রেখা"],
       "1 আর -1 থেকে সমদূরবর্তী বিন্দুগুলো তাদের লম্বদ্বিখণ্ডকে থাকে, Re z = 0।"),
    _q("If |z| = 1 and z ≠ -1, then (z - 1)/(z + 1) is…", ["Purely imaginary", "Purely real", "Always zero", "Of modulus 2"],
       "With z = e^(iθ), (z - 1)/(z + 1) = i tan(θ/2).",
       "|z| = 1 আর z ≠ -1 হলে (z - 1)/(z + 1)…", ["বিশুদ্ধ কাল্পনিক", "বিশুদ্ধ বাস্তব", "সবসময় শূন্য", "মডুলাস 2"],
       "z = e^(iθ) হলে (z - 1)/(z + 1) = i tan(θ/2)।"),
    _q("For which values of k does x² + kx + 9 = 0 have equal roots?", ["k = 6 or k = -6", "k = 9 only", "k = 3 only", "k = 0"],
       "Discriminant k² - 36 = 0 gives k = ±6.",
       "k-এর কোন মানে x² + kx + 9 = 0-এর বীজ দুটি সমান?", ["k = 6 বা k = -6", "কেবল k = 9", "কেবল k = 3", "k = 0"],
       "নিরূপক k² - 36 = 0 থেকে k = ±6।"),
    _q("If a quadratic f(x) = ax² + bx + c with a > 0 has f(p) < 0, then…", ["p lies strictly between the two real roots", "f has no real roots", "p is a root", "p is less than both roots"],
       "An upward parabola is negative only between its roots, so f(p) < 0 forces two real roots on either side of p.",
       "a > 0 সহ দ্বিঘাত f(x) = ax² + bx + c-এ f(p) < 0 হলে…", ["p দুটি বাস্তব বীজের ঠিক মাঝে", "f-এর বাস্তব বীজ নেই", "p একটা বীজ", "p দুটি বীজেরই চেয়ে ছোট"],
       "ঊর্ধ্বমুখী অধিবৃত্ত কেবল বীজদুটির মাঝে ঋণাত্মক, তাই f(p) < 0 মানে p-এর দুই পাশে দুটি বাস্তব বীজ।"),
    _q("For positive a, b, c, what is the least value of (a + b + c)(1/a + 1/b + 1/c)?", ["9", "3", "1", "6"],
       "AM ≥ HM (or Cauchy-Schwarz): the product is at least 3² = 9, equal when a = b = c.",
       "ধনাত্মক a, b, c-এর জন্য (a + b + c)(1/a + 1/b + 1/c)-এর ন্যূনতম মান কত?", ["9", "3", "1", "6"],
       "সমান্তর গড় ≥ বিপরীত গড় (বা কশি-শোয়ার্জ): গুণফল অন্তত 3² = 9, সমতা a = b = c-তে।"),
    _q("A matrix A satisfies A² = A. Such a matrix is called…", ["Idempotent", "Nilpotent", "Involutory", "Orthogonal"],
       "Nilpotent means Aᵏ = 0, involutory A² = I, orthogonal AAᵀ = I.",
       "যে ম্যাট্রিক্স A² = A মানে তাকে বলে…", ["সমঘাতী", "শূন্যঘাতী", "আত্ম-বিপরীত", "লম্ব-ম্যাট্রিক্স"],
       "শূন্যঘাতী মানে Aᵏ = 0, আত্ম-বিপরীত A² = I, লম্ব-ম্যাট্রিক্স AAᵀ = I।"),
    _q("If A is an orthogonal matrix, then |A| is…", ["1 or -1", "0", "Any real number", "Always 2"],
       "AAᵀ = I gives |A|² = 1.",
       "A লম্ব-ম্যাট্রিক্স হলে |A|…", ["1 বা -1", "0", "যেকোনো বাস্তব সংখ্যা", "সবসময় 2"],
       "AAᵀ = I থেকে |A|² = 1।"),
    _q("A homogeneous system AX = 0 has non-trivial solutions exactly when…", ["|A| = 0", "|A| ≠ 0", "A is the identity", "A is symmetric"],
       "If |A| ≠ 0, X = A⁻¹·0 = 0 is the only solution; a zero determinant leaves a free variable.",
       "সমমাত্রিক তন্ত্র AX = 0-এর অশূন্য সমাধান থাকে ঠিক তখনই যখন…", ["|A| = 0", "|A| ≠ 0", "A একক ম্যাট্রিক্স", "A প্রতিসম"],
       "|A| ≠ 0 হলে X = A⁻¹·0 = 0 একমাত্র সমাধান; নির্ণায়ক শূন্য হলে একটা মুক্ত চল থাকে।"),
    _q("Every square matrix can be written uniquely as the sum of…", ["A symmetric and a skew-symmetric matrix", "Two diagonal matrices", "Two orthogonal matrices", "An identity and a zero matrix"],
       "A = ½(A + Aᵀ) + ½(A - Aᵀ).",
       "প্রতিটি বর্গ ম্যাট্রিক্সকে অনন্যভাবে লেখা যায় যোগফল হিসেবে…", ["একটা প্রতিসম আর একটা বিপ্রতিসম ম্যাট্রিক্সের", "দুটো কর্ণ-ম্যাট্রিক্সের", "দুটো লম্ব-ম্যাট্রিক্সের", "একক আর শূন্য ম্যাট্রিক্সের"],
       "A = ½(A + Aᵀ) + ½(A - Aᵀ)।"),
    _q("What are the eigenvalues of a 2 x 2 matrix with trace 5 and determinant 6?", ["2 and 3", "1 and 6", "5 and 6", "-2 and -3"],
       "They solve λ² - 5λ + 6 = 0 (sum = trace, product = determinant).",
       "ট্রেস 5 আর নির্ণায়ক 6-এর একটা 2 x 2 ম্যাট্রিক্সের আইগেন মান কী কী?", ["2 আর 3", "1 আর 6", "5 আর 6", "-2 আর -3"],
       "এরা λ² - 5λ + 6 = 0-এর সমাধান (যোগফল = ট্রেস, গুণফল = নির্ণায়ক)।"),
    _q("If a, b, c are in AP, then 2b equals…", ["a + c", "ac", "a - c", "√(ac)"],
       "Equal common difference: b - a = c - b. For a GP the condition is b² = ac, for an HP 2/b = 1/a + 1/c.",
       "a, b, c সমান্তর প্রগতিতে থাকলে 2b সমান…", ["a + c", "ac", "a - c", "√(ac)"],
       "সাধারণ অন্তর সমান: b - a = c - b। গুণোত্তরে শর্ত b² = ac, বিপরীত প্রগতিতে 2/b = 1/a + 1/c।"),
    _q("For two positive numbers, which ordering of the means is always true?", ["AM ≥ GM ≥ HM", "HM ≥ GM ≥ AM", "GM ≥ AM ≥ HM", "All three are always equal"],
       "Equality holds only when the numbers are equal; also GM² = AM x HM for two numbers.",
       "দুটি ধনাত্মক সংখ্যার গড়গুলোর কোন ক্রম সবসময় সত্য?", ["সমান্তর ≥ গুণোত্তর ≥ বিপরীত গড়", "বিপরীত ≥ গুণোত্তর ≥ সমান্তর গড়", "গুণোত্তর ≥ সমান্তর ≥ বিপরীত গড়", "তিনটি সবসময় সমান"],
       "কেবল সংখ্যাদুটো সমান হলে সমতা; আর দুটি সংখ্যার জন্য গুণোত্তর² = সমান্তর x বিপরীত গড়।"),
    _q("What is the number of terms in the expansion of (a + b + c)⁶?", ["28", "21", "7", "36"],
       "Terms aᵖbᵠcʳ with p + q + r = 6: ⁶⁺²C₂ = 28.",
       "(a + b + c)⁶-এর বিস্তারে কয়টি পদ আছে?", ["28", "21", "7", "36"],
       "aᵖbᵠcʳ পদ, যেখানে p + q + r = 6: ⁶⁺²C₂ = 28।"),
    _q("Which binomial coefficient is the largest in the expansion of (1 + x)¹⁰?", ["¹⁰C₅", "¹⁰C₁₀", "¹⁰C₁", "¹⁰C₉"],
       "For even n the middle coefficient ⁿC_(n/2) is the greatest: ¹⁰C₅ = 252.",
       "(1 + x)¹⁰-এর বিস্তারে কোন দ্বিপদ সহগ সবচেয়ে বড়?", ["¹⁰C₅", "¹⁰C₁₀", "¹⁰C₁", "¹⁰C₉"],
       "জোড় n-এ মাঝের সহগ ⁿC_(n/2) সবচেয়ে বড়: ¹⁰C₅ = 252।"),
    # ---------------------------------------------------------------- combinatorics and probability
    _q("By the pigeonhole principle, among 13 people at least two must share…", ["A birth month", "A birthday", "A first name", "A height"],
       "13 people into 12 months: some month holds at least two of them.",
       "পায়রার খোপ নীতিতে 13 জনের মধ্যে অন্তত দুজনের মিল থাকবেই…", ["জন্মমাসে", "জন্মদিনে", "প্রথম নামে", "উচ্চতায়"],
       "13 জন 12 মাসে: কোনো এক মাসে অন্তত দুজন থাকবে।"),
    _q("A family has two children and at least one is a boy. What is the probability that both are boys?", ["1/3", "1/2", "1/4", "2/3"],
       "The equally likely cases BB, BG, GB remain; only BB has two boys.",
       "একটা পরিবারে দুটি সন্তান, অন্তত একজন ছেলে। দুজনেই ছেলে হওয়ার সম্ভাবনা কত?", ["1/3", "1/2", "1/4", "2/3"],
       "সমসম্ভব ক্ষেত্র ছেলে-ছেলে, ছেলে-মেয়ে, মেয়ে-ছেলে থাকে; কেবল প্রথমটিতে দুজন ছেলে।"),
    _q("For a binomial distribution B(n, p), what is the variance?", ["np(1 - p)", "np", "n²p", "√(np)"],
       "Each trial contributes p(1 - p); n independent trials add up.",
       "দ্বিপদ বিন্যাস B(n, p)-এর ভেদাঙ্ক কত?", ["np(1 - p)", "np", "n²p", "√(np)"],
       "প্রতিটি পরীক্ষা p(1 - p) দেয়; n টি স্বাধীন পরীক্ষা যোগ হয়।"),
    _q("If P(A) = 0.5, P(B) = 0.4 and A, B are independent, what is P(A ∪ B)?", ["0.7", "0.9", "0.2", "0.5"],
       "P(A ∩ B) = 0.5 x 0.4 = 0.2, so P(A ∪ B) = 0.5 + 0.4 - 0.2 = 0.7.",
       "P(A) = 0.5, P(B) = 0.4 আর A, B স্বাধীন হলে P(A ∪ B) কত?", ["0.7", "0.9", "0.2", "0.5"],
       "P(A ∩ B) = 0.5 x 0.4 = 0.2, তাই P(A ∪ B) = 0.5 + 0.4 - 0.2 = 0.7।"),
    _q("A random variable X takes values 0, 1, 2 with probabilities 1/4, 1/2, 1/4. What is E(X)?", ["1", "1/2", "3/4", "2"],
       "E(X) = 0·¼ + 1·½ + 2·¼ = 1 - the centre of a symmetric distribution.",
       "একটা যদৃচ্ছ চল X 0, 1, 2 মান নেয় সম্ভাবনা 1/4, 1/2, 1/4-এ। E(X) কত?", ["1", "1/2", "3/4", "2"],
       "E(X) = 0·¼ + 1·½ + 2·¼ = 1 - প্রতিসম বিন্যাসের কেন্দ্র।"),
    _q("In how many ways can 6 people sit at a round table if two particular people refuse to sit together?", ["72", "120", "48", "24"],
       "All arrangements (6 - 1)! = 120; together: treat the pair as one, 4! x 2 = 48; so 120 - 48 = 72.",
       "দুজন বিশেষ ব্যক্তি পাশাপাশি বসতে না চাইলে 6 জন গোল টেবিলে কত উপায়ে বসতে পারে?", ["72", "120", "48", "24"],
       "মোট (6 - 1)! = 120; পাশাপাশি: দুজনকে এক ধরে 4! x 2 = 48; তাই 120 - 48 = 72।"),
    _q("How many diagonals does a convex polygon with 20 sides have?", ["170", "190", "180", "200"],
       "n(n - 3)/2 = 20 x 17 ÷ 2 = 170.",
       "20 বাহুর একটা উত্তল বহুভুজের কয়টি কর্ণ আছে?", ["170", "190", "180", "200"],
       "n(n - 3)/2 = 20 x 17 ÷ 2 = 170।"),
    _q("A 5-digit number is formed from 0, 1, 2, 3, 4 without repetition. How many such numbers are there?", ["96", "120", "24", "100"],
       "5! = 120 arrangements, minus the 4! = 24 that start with 0.",
       "0, 1, 2, 3, 4 থেকে পুনরাবৃত্তি ছাড়া 5-অঙ্কের সংখ্যা তৈরি হয়। এমন কয়টি সংখ্যা আছে?", ["96", "120", "24", "100"],
       "5! = 120 বিন্যাস, তার থেকে 0 দিয়ে শুরু 4! = 24টি বাদ।"),
    # ---------------------------------------------------------------- coordinate geometry
    _q("The condition for y = mx + c to touch the parabola y² = 4ax is…", ["c = a/m", "c = am", "c = -am²", "c² = a²m² + b²"],
       "Substituting gives a quadratic in x whose discriminant vanishes when c = a/m.",
       "y = mx + c রেখা অধিবৃত্ত y² = 4ax-কে স্পর্শ করার শর্ত…", ["c = a/m", "c = am", "c = -am²", "c² = a²m² + b²"],
       "বসালে x-এ একটা দ্বিঘাত পাওয়া যায়, যার নিরূপক c = a/m হলে শূন্য।"),
    _q("The condition for y = mx + c to touch the ellipse x²/a² + y²/b² = 1 is…", ["c² = a²m² + b²", "c² = a²m² - b²", "c = a/m", "c = 0"],
       "The tangent of slope m to the ellipse is y = mx ± √(a²m² + b²); for a hyperbola it is c² = a²m² - b².",
       "y = mx + c রেখা উপবৃত্ত x²/a² + y²/b² = 1-কে স্পর্শ করার শর্ত…", ["c² = a²m² + b²", "c² = a²m² - b²", "c = a/m", "c = 0"],
       "উপবৃত্তে নতি m-এর স্পর্শক y = mx ± √(a²m² + b²); পরাবৃত্তে শর্ত c² = a²m² - b²।"),
    _q("What is the eccentricity of a rectangular hyperbola?", ["√2", "1", "2", "1/√2"],
       "a = b gives e² = 1 + b²/a² = 2.",
       "সমপরাবৃত্তের উৎকেন্দ্রতা কত?", ["√2", "1", "2", "1/√2"],
       "a = b হলে e² = 1 + b²/a² = 2।"),
    _q("The tangents drawn at the ends of a focal chord of a parabola meet…", ["At right angles on the directrix", "At the focus", "At the vertex", "On the axis, parallel to each other"],
       "With ends t₁ and t₂, t₁t₂ = -1 makes the slopes' product -1 and the meeting point lies on x = -a.",
       "অধিবৃত্তের একটা নাভিগামী জ্যা-র দুই প্রান্তের স্পর্শক মেলে…", ["নিয়ামকের ওপর সমকোণে", "নাভিতে", "শীর্ষবিন্দুতে", "অক্ষের ওপর, পরস্পর সমান্তরালে"],
       "প্রান্ত t₁ আর t₂ হলে t₁t₂ = -1, তাই নতির গুণফল -1 আর মিলনবিন্দু x = -a রেখায়।"),
    _q("Light from one focus of an elliptical mirror reflects to…", ["The other focus", "The centre", "Infinity, parallel to the axis", "The nearer vertex"],
       "The normal bisects the angle between the focal radii - the reason whispering galleries carry sound across a room.",
       "উপবৃত্তাকার দর্পণের এক নাভি থেকে আসা আলো প্রতিফলিত হয়ে যায়…", ["অন্য নাভিতে", "কেন্দ্রে", "অসীমে, অক্ষের সমান্তরালে", "নিকটতর শীর্ষবিন্দুতে"],
       "অভিলম্ব নাভি-ব্যাসার্ধদুটির মাঝের কোণকে সমদ্বিখণ্ডিত করে - তাই ফিসফিস-গ্যালারিতে শব্দ ঘরের ওপারে পৌঁছয়।"),
    _q("Two circles with centres C₁, C₂ and radii r₁, r₂ touch externally when…", ["C₁C₂ = r₁ + r₂", "C₁C₂ = |r₁ - r₂|", "C₁C₂ < |r₁ - r₂|", "C₁C₂ = 0"],
       "Equal to the difference means internal touching; between the difference and the sum, they cut at two points.",
       "কেন্দ্র C₁, C₂ আর ব্যাসার্ধ r₁, r₂-এর দুটি বৃত্ত বহিঃস্থভাবে স্পর্শ করে যখন…", ["C₁C₂ = r₁ + r₂", "C₁C₂ = |r₁ - r₂|", "C₁C₂ < |r₁ - r₂|", "C₁C₂ = 0"],
       "পার্থক্যের সমান হলে অন্তঃস্থ স্পর্শ; পার্থক্য আর যোগফলের মাঝে হলে দুটি বিন্দুতে ছেদ।"),
    _q("The locus of a point from which the two tangents to a circle x² + y² = a² are perpendicular is…", ["The director circle x² + y² = 2a²", "The circle itself", "A straight line", "The circle x² + y² = a²/2"],
       "Perpendicular tangents meet at distance a√2 from the centre.",
       "যে বিন্দু থেকে বৃত্ত x² + y² = a²-এ টানা দুটি স্পর্শক পরস্পর লম্ব, তার সঞ্চারপথ…", ["নিয়ামক বৃত্ত x² + y² = 2a²", "বৃত্তটি নিজেই", "একটা সরলরেখা", "বৃত্ত x² + y² = a²/2"],
       "পরস্পর লম্ব স্পর্শকগুলো কেন্দ্র থেকে a√2 দূরত্বে মেলে।"),
    _q("The pair of lines ax² + 2hxy + by² = 0 are perpendicular when…", ["a + b = 0", "h² = ab", "h = 0", "a = b"],
       "The product of slopes is a/b; it equals -1 when a + b = 0. h² = ab makes the lines coincide.",
       "রেখাযুগল ax² + 2hxy + by² = 0 পরস্পর লম্ব হয় যখন…", ["a + b = 0", "h² = ab", "h = 0", "a = b"],
       "নতির গুণফল a/b; a + b = 0 হলে তা -1। h² = ab হলে রেখাদুটো মিলে যায়।"),
    # ---------------------------------------------------------------- vectors and 3-D
    _q("If |a + b| = |a - b| for non-zero vectors a and b, then…", ["a and b are perpendicular", "a and b are parallel", "a = b", "|a| = |b|"],
       "Squaring: 2a·b = -2a·b, so a·b = 0 - the diagonals of the parallelogram are equal, making it a rectangle.",
       "অশূন্য ভেক্টর a আর b-এর জন্য |a + b| = |a - b| হলে…", ["a আর b পরস্পর লম্ব", "a আর b সমান্তরাল", "a = b", "|a| = |b|"],
       "বর্গ করলে 2a·b = -2a·b, তাই a·b = 0 - সামান্তরিকের কর্ণ দুটো সমান, অর্থাৎ আয়তক্ষেত্র।"),
    _q("What is a x (b x c) equal to?", ["(a·c)b - (a·b)c", "(a·b)c - (a·c)b", "(a x b) x c", "0 always"],
       "The vector triple product lies in the plane of b and c; the cross product is not associative.",
       "a x (b x c) কীসের সমান?", ["(a·c)b - (a·b)c", "(a·b)c - (a·c)b", "(a x b) x c", "সবসময় 0"],
       "ভেক্টর ত্রয়ী গুণফল b আর c-এর সমতলে থাকে; ক্রস গুণফল সংযোগ-নিয়ম মানে না।"),
    _q("A line with direction ratios 1, 1, 1 makes equal angles with the axes. What is the cosine of each angle?", ["1/√3", "1", "1/3", "1/√2"],
       "Direction cosines are 1/√(1 + 1 + 1) each, and l² + m² + n² = 1.",
       "দিক-অনুপাত 1, 1, 1-এর রেখা অক্ষগুলোর সঙ্গে সমান কোণ করে। প্রতিটি কোণের কোসাইন কত?", ["1/√3", "1", "1/3", "1/√2"],
       "প্রতিটি দিক-কোসাইন 1/√(1 + 1 + 1), আর l² + m² + n² = 1।"),
    _q("The line r = a + t b is parallel to the plane r·n = d when…", ["b·n = 0", "b x n = 0", "a·n = d", "b = n"],
       "A direction perpendicular to the plane's normal lies along the plane; if also a·n = d, the line lies in it.",
       "রেখা r = a + t b সমতল r·n = d-এর সমান্তরাল হয় যখন…", ["b·n = 0", "b x n = 0", "a·n = d", "b = n"],
       "সমতলের অভিলম্বের সঙ্গে লম্ব দিক সমতল বরাবর থাকে; a·n = d-ও হলে রেখা সমতলের মধ্যেই থাকে।"),
    _q("What is the angle between the planes x + y = 3 and y + z = 5?", ["60°", "45°", "90°", "30°"],
       "Normals (1, 1, 0) and (0, 1, 1): cos θ = 1 ÷ (√2 x √2) = 1/2.",
       "সমতল x + y = 3 আর y + z = 5-এর মাঝের কোণ কত?", ["60°", "45°", "90°", "30°"],
       "অভিলম্ব (1, 1, 0) আর (0, 1, 1): cos θ = 1 ÷ (√2 x √2) = 1/2।"),
    _q("Which point divides the line joining (1, 2, 3) and (4, 5, 6) internally in the ratio 1 : 2?", ["(2, 3, 4)", "(3, 4, 5)", "(2.5, 3.5, 4.5)", "(5, 7, 9)"],
       "Section formula: (2 x (1, 2, 3) + 1 x (4, 5, 6)) ÷ 3 = (2, 3, 4).",
       "(1, 2, 3) আর (4, 5, 6) সংযোগকারী রেখাকে কোন বিন্দু অন্তঃস্থভাবে 1 : 2 অনুপাতে ভাগ করে?", ["(2, 3, 4)", "(3, 4, 5)", "(2.5, 3.5, 4.5)", "(5, 7, 9)"],
       "বিভাজন সূত্র: (2 x (1, 2, 3) + 1 x (4, 5, 6)) ÷ 3 = (2, 3, 4)।"),
    # ---------------------------------------------------------------- trigonometry
    _q("What is tan⁻¹(1/2) + tan⁻¹(1/3)?", ["π/4", "π/3", "π/6", "π/2"],
       "tan⁻¹a + tan⁻¹b = tan⁻¹((a + b)/(1 - ab)) = tan⁻¹((5/6) ÷ (5/6)) = tan⁻¹ 1.",
       "tan⁻¹(1/2) + tan⁻¹(1/3)-এর মান কত?", ["π/4", "π/3", "π/6", "π/2"],
       "সূত্র: tan⁻¹a + tan⁻¹b = tan⁻¹((a + b)/(1 - ab)) = tan⁻¹((5/6) ÷ (5/6)) = tan⁻¹ 1, তাই উত্তর π/4।"),
    _q("What is sin⁻¹x + cos⁻¹x for -1 ≤ x ≤ 1?", ["π/2", "π", "0", "π/4"],
       "If sin θ = x then cos(π/2 - θ) = x, so the two angles add to π/2.",
       "-1 ≤ x ≤ 1 হলে sin⁻¹x + cos⁻¹x কত?", ["π/2", "π", "0", "π/4"],
       "sin θ = x হলে cos(π/2 - θ) = x, তাই দুটো কোণ মিলে π/2।"),
    _q("What is the maximum value of sin x · cos x?", ["1/2", "1", "√2", "2"],
       "sin x cos x = ½ sin 2x, which peaks at ½.",
       "sin x · cos x-এর সর্বোচ্চ মান কত?", ["1/2", "1", "√2", "2"],
       "sin x cos x = ½ sin 2x, যার সর্বোচ্চ ½।"),
    _q("What is the value of cos 20° cos 40° cos 80°?", ["1/8", "1/4", "1/2", "√3/8"],
       "cos θ cos(60° - θ) cos(60° + θ) = ¼ cos 3θ; with θ = 20° that is ¼ cos 60° = 1/8.",
       "cos 20° cos 40° cos 80°-এর মান কত?", ["1/8", "1/4", "1/2", "√3/8"],
       "cos θ cos(60° - θ) cos(60° + θ) = ¼ cos 3θ; θ = 20° হলে ¼ cos 60° = 1/8।"),
    _q("In a triangle ABC, if a² + b² = c², then angle C is…", ["90°", "60°", "45°", "120°"],
       "The cosine rule c² = a² + b² - 2ab cos C forces cos C = 0.",
       "ত্রিভুজ ABC-তে a² + b² = c² হলে কোণ C…", ["90°", "60°", "45°", "120°"],
       "কোসাইন সূত্র c² = a² + b² - 2ab cos C থেকে cos C = 0।"),
    _q("What is the general solution of tan x = tan α?", ["x = nπ + α, n an integer", "x = 2nπ ± α", "x = nπ + (-1)ⁿα", "x = α only"],
       "tan has period π; sin uses nπ + (-1)ⁿα and cos uses 2nπ ± α.",
       "tan x = tan α-এর সাধারণ সমাধান কী?", ["x = nπ + α, n পূর্ণসংখ্যা", "x = 2nπ ± α", "x = nπ + (-1)ⁿα", "কেবল x = α"],
       "tan-এর পর্যায় π; sin-এ nπ + (-1)ⁿα আর cos-এ 2nπ ± α।"),
    _q("In any triangle, what is tan A + tan B + tan C equal to?", ["tan A · tan B · tan C", "1", "0", "π"],
       "A + B = π - C gives tan(A + B) = -tan C; clearing the fraction gives the identity.",
       "যেকোনো ত্রিভুজে tan A + tan B + tan C কীসের সমান?", ["tan A · tan B · tan C গুণফলের", "1", "0", "π"],
       "A + B = π - C থেকে tan(A + B) = -tan C; ভগ্নাংশ সরালে অভেদটি পাওয়া যায়।"),
    _q("What is the radius of the circumcircle of a triangle with sides a, b, c and area Δ?", ["a·b·c ÷ 4Δ", "Δ ÷ s", "a·b·c ÷ 2Δ", "(a + b + c) ÷ 2"],
       "R = abc/4Δ = a/(2 sin A); the inradius is r = Δ/s.",
       "a, b, c বাহু আর ক্ষেত্রফল Δ-এর ত্রিভুজের পরিবৃত্তের ব্যাসার্ধ কত?", ["a·b·c ÷ 4Δ", "Δ ÷ s", "a·b·c ÷ 2Δ", "(a + b + c) ÷ 2"],
       "R = abc/4Δ = a/(2 sin A); অন্তর্বৃত্তের ব্যাসার্ধ r = Δ/s।"),
    _q("Which statement about the function y = sin⁻¹(sin x) is true?", ["It equals x only for x in [-π/2, π/2]", "It equals x for every real x", "It is never equal to x", "It equals -x for every x"],
       "sin⁻¹ returns angles in [-π/2, π/2]; outside that range the graph zig-zags.",
       "অপেক্ষক y = sin⁻¹(sin x) সম্পর্কে কোন বিবৃতি সত্য?", ["কেবল [-π/2, π/2]-এ এটা x-এর সমান", "সব বাস্তব x-এ এটা x-এর সমান", "কখনোই x-এর সমান নয়", "সব x-এ এটা -x-এর সমান"],
       "sin⁻¹ কেবল [-π/2, π/2]-এর কোণ ফেরায়; তার বাইরে লেখচিত্র আঁকাবাঁকা হয়।"),
    # ---------------------------------------------------------------- statistics and reasoning
    _q("If every value in a data set is multiplied by 3, the variance is…", ["Multiplied by 9", "Multiplied by 3", "Unchanged", "Increased by 3"],
       "Var(aX) = a² Var(X); the standard deviation is multiplied by |a|.",
       "একটা তথ্যের প্রতিটি মানকে 3 দিয়ে গুণ করলে ভেদাঙ্ক…", ["9 গুণ হয়", "3 গুণ হয়", "অপরিবর্তিত থাকে", "3 বাড়ে"],
       "Var(aX) = a² Var(X); সমক বিচ্যুতি |a| গুণ হয়।"),
    _q("For a moderately skewed distribution, which empirical relation holds?", ["Mode = 3 Median - 2 Mean", "Mean = 3 Median - 2 Mode", "Median = Mean + Mode", "Mode = Mean"],
       "Karl Pearson's empirical relation links the three averages when the skew is mild.",
       "মাঝারি বঙ্কিম বিন্যাসে কোন অভিজ্ঞতালব্ধ সম্পর্ক খাটে?", ["সংখ্যাগুরুমান = 3 মধ্যমা - 2 গড়", "গড় = 3 মধ্যমা - 2 সংখ্যাগুরুমান", "মধ্যমা = গড় + সংখ্যাগুরুমান", "সংখ্যাগুরুমান = গড়"],
       "বঙ্কিমতা অল্প হলে কার্ল পিয়ারসনের সম্পর্ক তিনটি গড়কে যুক্ত করে।"),
    _q("What is the remainder when 1! + 2! + 3! + ... + 100! is divided by 5?", ["3", "0", "1", "4"],
       "From 5! on every term is a multiple of 5, so only 1 + 2 + 6 + 24 = 33 matters: remainder 3.",
       "1! + 2! + 3! + ... + 100!-কে 5 দিয়ে ভাগ করলে ভাগশেষ কত?", ["3", "0", "1", "4"],
       "5! থেকে প্রতিটি পদ 5-এর গুণিতক, তাই কেবল 1 + 2 + 6 + 24 = 33 গোনে: ভাগশেষ 3।"),
    _q("How many real solutions does the equation eˣ = x have?", ["None", "Exactly one", "Exactly two", "Infinitely many"],
       "eˣ ≥ 1 + x > x for every real x, so the curves y = eˣ and y = x never meet.",
       "eˣ = x সমীকরণের কয়টি বাস্তব সমাধান আছে?", ["একটিও নেই", "ঠিক একটি", "ঠিক দুটি", "অসংখ্য"],
       "প্রতিটি বাস্তব x-এর জন্য eˣ ≥ 1 + x > x, তাই y = eˣ আর y = x বক্ররেখা কখনো মেলে না।"),
    _q("Which statement is logically equivalent to 'p → q'?", ["¬p ∨ q", "p ∨ ¬q", "q → p", "¬p → ¬q"],
       "An implication fails only when p is true and q false; '¬q → ¬p' (the contrapositive) is also equivalent.",
       "'p → q'-এর সঙ্গে যুক্তিগতভাবে সমতুল্য কোন বিবৃতি?", ["¬p ∨ q", "p ∨ ¬q", "q → p", "¬p → ¬q"],
       "শর্তবাক্য কেবল p সত্য আর q মিথ্যা হলে মিথ্যা; '¬q → ¬p' (বিপরীতধর্মী) রূপটিও সমতুল্য।"),
    _q("The function f(x) = x³ − 3x has local maximum and minimum at:", ["Local max at x = −1 (f = 2); local min at x = 1 (f = −2)", "Local max at x = 1; min at x = −1", "No local extrema", "Local max at x = 0"],
       "f'(x) = 3x² − 3 = 0 → x = ±1. f''(x) = 6x; f''(−1) = −6 < 0 (max); f''(1) = 6 > 0 (min).",
       "f(x) = x³ − 3x-এর স্থানীয় সর্বোচ্চ ও সর্বনিম্ন:", ["x = −1-এ স্থানীয় সর্বোচ্চ (f = 2); x = 1-এ সর্বনিম্ন (f = −2)", "x = 1-এ সর্বোচ্চ; x = −1-এ সর্বনিম্ন", "কোনো স্থানীয় চরম নেই", "x = 0-এ সর্বোচ্চ"],
       "f'(x) = 3x² − 3 = 0 → x = ±1। f''(−1) < 0 (সর্বোচ্চ); f''(1) > 0 (সর্বনিম্ন)।"),
    _q("The number of real solutions of |x² − 5x + 6| = 0 is:", ["2 (x = 2 and x = 3; the quadratic x² − 5x + 6 = (x−2)(x−3) has two real roots where |f| = 0)", "0", "4", "1"],
       "|f(x)| = 0 iff f(x) = 0. Roots of x² − 5x + 6 = 0: x = 2, 3.",
       "|x² − 5x + 6| = 0-এর বাস্তব সমাধান সংখ্যা:", ["2 (x = 2 ও x = 3; দ্বিঘাত (x−2)(x−3) এর দুটো বাস্তব মূল)", "0", "4", "1"],
       "|f(x)| = 0 তখনই যখন f(x) = 0। x² − 5x + 6 = 0-এর মূল: x = 2, 3।"),
    _q("If α and β are roots of 2x² − 5x + 3 = 0, then α² + β² = ?", ["19/4 (α+β = 5/2; αβ = 3/2; α²+β² = (α+β)² − 2αβ = 25/4 − 3 = 13/4? No: 25/4 − 6/2 = 25/4 − 12/4 = 13/4)", "25/4", "9/4", "7/4"],
       "By Vieta: α+β = 5/2, αβ = 3/2. α²+β² = (5/2)² − 2(3/2) = 25/4 − 3 = 13/4.",
       "2x² − 5x + 3 = 0-এর মূল α ও β হলে α² + β² = ?", ["13/4 (α+β = 5/2; αβ = 3/2; α²+β² = 25/4 − 3 = 13/4)", "25/4", "9/4", "7/4"],
       "ভিয়েটা: α+β = 5/2, αβ = 3/2। α²+β² = 25/4 − 3 = 13/4।"),
    _q("The area enclosed between the curves y = x² and y = √x (for x from 0 to 1) is:", ["1/3 (∫₀¹(√x − x²)dx = [⅔x^(3/2) − x³/3]₀¹ = 2/3 − 1/3 = 1/3)", "1/2", "2/3", "1/6"],
       "Upper curve: y = √x; lower curve: y = x² on [0, 1]. They intersect at (0,0) and (1,1).",
       "y = x² ও y = √x বক্ররেখার মধ্যবর্তী ক্ষেত্রফল (x: 0 থেকে 1):", ["1/3 (∫₀¹(√x − x²)dx = 2/3 − 1/3 = 1/3)", "1/2", "2/3", "1/6"],
       "উপরের বক্ররেখা: y = √x; নিচের: y = x²। ছেদ (0,0) ও (1,1)-এ।"),
    _q("The value of ∫₀^(π) x sin x dx is:", ["π (integrate by parts: u = x, dv = sin x dx → [−x cos x + sin x]₀^π = π)", "0", "2π", "π/2"],
       "IBP: ∫x sin x dx = −x cos x + sin x + C. At π: −π(−1) + 0 = π. At 0: 0 + 0 = 0.",
       "∫₀^(π) x sin x dx-এর মান:", ["π (আংশিক ইন্টিগ্রেশন: u = x, dv = sin x → [−x cos x + sin x]₀^π = π)", "0", "2π", "π/2"],
       "IBP: ∫x sin x dx = −x cos x + sin x + C। π-তে: π(+1) = π।"),
    _q("The differential equation dy/dx = ky has the general solution:", ["y = Ceᵏˣ where C is an arbitrary constant", "y = kx + C", "y = k ln x + C", "y = C sin(kx)"],
       "Separable: dy/y = k dx → ln|y| = kx + C₁ → y = Ce^(kx). Models population growth, radioactive decay.",
       "dy/dx = ky অবকল সমীকরণের সাধারণ সমাধান:", ["y = Ceᵏˣ যেখানে C স্বেচ্ছা ধ্রুবক", "y = kx + C", "y = k ln x + C", "y = C sin(kx)"],
       "বিভাজনযোগ্য: dy/y = k dx → y = Ceᵏˣ। জনসংখ্যা বৃদ্ধি, তেজস্ক্রিয় ক্ষয় মডেল।"),
    _q("If |z| = 1 and z ≠ ±1, then (z − 1)/(z + 1) is:", ["Purely imaginary (the real part of (z−1)/(z+1) is zero when |z| = 1)", "Purely real", "Has modulus 1", "Zero"],
       "Let z = cosθ + i sinθ. Then (z−1)/(z+1) = i tan(θ/2), which is purely imaginary.",
       "|z| = 1 ও z ≠ ±1 হলে (z − 1)/(z + 1):", ["বিশুদ্ধ কাল্পনিক (|z| = 1 হলে (z−1)/(z+1)-এর বাস্তব অংশ শূন্য)", "বিশুদ্ধ বাস্তব", "মডুলাস 1", "শূন্য"],
       "z = cosθ + i sinθ ধরলে (z−1)/(z+1) = i tan(θ/2) — বিশুদ্ধ কাল্পনিক।"),
    _q("The number of ways to choose a committee of 3 men and 2 women from 6 men and 4 women is:", ["120 (C(6,3) × C(4,2) = 20 × 6 = 120)", "240", "60", "360"],
       "C(6,3) = 20; C(4,2) = 6; total = 120. Multiplication principle: independent choices multiply.",
       "6 জন পুরুষ ও 4 জন মহিলার মধ্য থেকে 3 পুরুষ ও 2 মহিলার কমিটি গঠনের উপায়:", ["120 (C(6,3) × C(4,2) = 20 × 6 = 120)", "240", "60", "360"],
       "C(6,3) = 20; C(4,2) = 6; মোট = 120।"),
    _q("The coefficient of x³ in the expansion of (1 + x)⁵(1 + x²)³ is:", ["10 + 3×5 + 3 = ? Let me compute: (1+x)⁵ coefficients: 1,5,10,10,5,1; (1+x²)³: 1,3,3,1 (powers 0,2,4,6); x³ from (1+x)⁵ needs 1,3,5 terms × (1+x²)³ terms: C(5,3)×1 + C(5,1)×C(3,1) = 10 + 15 = 25", "10", "15", "30"],
       "Coefficient of x³: take x³ from (1+x)⁵ with (1+x²)³ at x⁰ → C(5,3)=10; take x¹ from (1+x)⁵ with x² from (1+x²)³ → C(5,1)×C(3,1)=15. Total = 25.",
       "(1 + x)⁵(1 + x²)³ প্রসারণে x³-এর সহগ:", ["25 (C(5,3)×1 + C(5,1)×C(3,1) = 10 + 15 = 25)", "10", "15", "30"],
       "x³-এর সহগ: (1+x)⁵ থেকে x³ × (1+x²)³ থেকে x⁰ → 10; (1+x)⁵ থেকে x¹ × (1+x²)³ থেকে x² → 15। মোট 25।"),
    _q("If a₁, a₂, a₃, … is an AP with first term a and common difference d, then Σ_{k=1}^{n} aₖ = ?", ["n/2 × (2a + (n−1)d) = n(first + last)/2", "(a + d)ⁿ", "n × a × d", "an + d"],
       "AP sum = n/2 × [2a + (n−1)d]. Alternative: Sn = n × (a + l)/2 where l is the last term.",
       "প্রথম পদ a ও সাধারণ পার্থক্য d সহ সমান্তর ধারার n পদের সমষ্টি:", ["n/2 × (2a + (n−1)d) = n(প্রথম + শেষ)/2", "(a + d)ⁿ", "n × a × d", "an + d"],
       "সমান্তর ধারার সমষ্টি = n/2 × [2a + (n−1)d]।"),
    _q("The slope of the tangent to the curve y = x³ − 2x at the point (1, −1) is:", ["1 (dy/dx = 3x² − 2; at x = 1: slope = 3 − 2 = 1)", "−1", "3", "2"],
       "Normal to curve at (1,−1) has slope −1 (negative reciprocal). Tangent-normal pair is common in bridge geometry.",
       "বিন্দু (1, −1)-তে y = x³ − 2x বক্ররেখার স্পর্শকের ঢাল:", ["1 (dy/dx = 3x² − 2; x = 1-এ ঢাল = 1)", "−1", "3", "2"],
       "বক্ররেখায় (1,−1)-তে অভিলম্বের ঢাল = −1।"),
    _q("A continuous random variable X has PDF f(x) = kx² for 0 ≤ x ≤ 1, zero elsewhere. The value of k is:", ["3 (∫₀¹ kx² dx = k/3 = 1 → k = 3)", "2", "1", "1/3"],
       "∫₋∞^∞ f(x)dx = 1. k∫₀¹ x² dx = k × [x³/3]₀¹ = k/3 = 1 → k = 3.",
       "সতত চলক X-এর PDF f(x) = kx² (0 ≤ x ≤ 1, অন্যত্র শূন্য)। k-এর মান:", ["3 (∫₀¹ kx² dx = k/3 = 1 → k = 3)", "2", "1", "1/3"],
       "∫₋∞^∞ f(x)dx = 1। k/3 = 1 → k = 3।"),
    _q("The eccentricity of the hyperbola x²/9 − y²/16 = 1 is:", ["5/3 (c² = a² + b² = 9 + 16 = 25 → c = 5; e = c/a = 5/3)", "√(25/9)", "4/3", "3/5"],
       "Hyperbola: e > 1. Here e = 5/3 ≈ 1.67. Compare: ellipse e < 1; parabola e = 1.",
       "x²/9 − y²/16 = 1 পরাবৃত্তের উৎকেন্দ্রতা:", ["5/3 (c² = 9 + 16 = 25 → c = 5; e = 5/3)", "√(25/9)", "4/3", "3/5"],
       "পরাবৃত্ত: e > 1। এখানে e = 5/3 ≈ 1.67।"),
    _q("The equation of the normal to the parabola y² = 4ax at the point (at², 2at) is:", ["y = −tx + 2at + at³ (slope of tangent = 1/t; normal slope = −t)", "y = tx + a/t", "y = t(x − a)", "y = x/t + a"],
       "Tangent to y² = 4ax at (at², 2at): ty = x + at². Normal: slope = −t, passes through (at², 2at).",
       "y² = 4ax পরাবৃত্তে বিন্দু (at², 2at)-তে অভিলম্বের সমীকরণ:", ["y = −tx + 2at + at³ (স্পর্শকের ঢাল = 1/t; অভিলম্বের ঢাল = −t)", "y = tx + a/t", "y = t(x − a)", "y = x/t + a"],
       "y² = 4ax-এ স্পর্শক: ty = x + at²। অভিলম্বের ঢাল = −t।"),
    _q("The sum of an infinite geometric series a/(1 − r) converges when:", ["|r| < 1 (common ratio must have absolute value less than one)", "|r| > 1", "r = 0 only", "|r| ≤ 1"],
       "For |r| ≥ 1 (r ≠ 0), terms don't go to zero and the series diverges.",
       "অসীম গুণোত্তর ধারা a/(1 − r) অভিসারী যখন:", ["|r| < 1 (সাধারণ অনুপাতের পরম মান এক-এর কম)", "|r| > 1", "শুধু r = 0", "|r| ≤ 1"],
       "|r| ≥ 1 (r ≠ 0) হলে পদগুলো শূন্যে যায় না এবং ধারা অপসারী।"),
    _q("If A is a 3×3 matrix with det(A) = 5, then det(3A) = ?", ["135 (det(kA) = k³ det(A) for a 3×3 matrix; 3³ × 5 = 27 × 5 = 135)", "15", "45", "27"],
       "For n×n matrix: det(kA) = kⁿ det(A). In 3D: scaling by k scales volume by k³.",
       "3×3 ম্যাট্রিক্স A-এর det(A) = 5 হলে det(3A) = ?", ["135 (det(kA) = k³ det(A); 27 × 5 = 135)", "15", "45", "27"],
       "n×n ম্যাট্রিক্সে: det(kA) = kⁿ det(A)।"),
    _q("The angle between the vectors a = i + j and b = i − j is:", ["90° (a·b = 1×1 + 1×(−1) = 0; perpendicular vectors)", "45°", "60°", "180°"],
       "a·b = |a||b|cosθ = 0 → cosθ = 0 → θ = 90°. They are orthogonal.",
       "ভেক্টর a = i + j ও b = i − j-এর মধ্যবর্তী কোণ:", ["90° (a·b = 1×1 + 1×(−1) = 0; লম্ব ভেক্টর)", "45°", "60°", "180°"],
       "a·b = 0 → cosθ = 0 → θ = 90°। তারা পরস্পর লম্ব।"),
    _q("The volume of the tetrahedron with vertices at the origin and points a, b, c is:", ["(1/6)|a · (b × c)| — one-sixth the absolute value of the scalar triple product", "(1/3)|a · (b × c)|", "|a × b|", "(1/2)|a · (b × c)|"],
       "Parallelepiped volume = |a · (b × c)|. Tetrahedron = 1/6 of parallelepiped.",
       "মূলবিন্দু এবং a, b, c বিন্দু শীর্ষবিশিষ্ট চতুর্মুখীর আয়তন:", ["(1/6)|a · (b × c)| — স্কেলার ট্রিপল প্রোডাক্টের পরম মানের এক-ষষ্ঠাংশ", "(1/3)|a · (b × c)|", "|a × b|", "(1/2)|a · (b × c)|"],
       "সমান্তরষষ্ঠতলকের আয়তন = |a · (b × c)|। চতুর্মুখী = 1/6।"),
    _q("The general solution of sin x = 1/2 is:", ["x = nπ + (−1)ⁿ π/6, n ∈ ℤ (covers both π/6 and 5π/6 in each period)", "x = π/6 + 2nπ only", "x = nπ + π/6", "x = π/6"],
       "Principal value: x = π/6. General: x = nπ + (−1)ⁿα where α = π/6.",
       "sin x = 1/2-এর সাধারণ সমাধান:", ["x = nπ + (−1)ⁿ π/6, n ∈ ℤ (প্রতিটি পর্যায়ে π/6 ও 5π/6 উভয় ধরে)", "শুধু x = π/6 + 2nπ", "x = nπ + π/6", "x = π/6"],
       "মূল মান: x = π/6। সাধারণ: x = nπ + (−1)ⁿα যেখানে α = π/6।"),
    _q("The mean of a binomial distribution B(n, p) is np. If n = 20 and p = 0.3, the variance is:", ["4.2 (variance = np(1−p) = 20 × 0.3 × 0.7 = 4.2)", "6", "3", "np = 6"],
       "Variance = npq where q = 1 − p. Standard deviation = √(npq) = √4.2 ≈ 2.05.",
       "B(n, p) বিনোমিয়াল বিতরণে n = 20, p = 0.3 হলে ভেরিয়েন্স:", ["4.2 (np(1−p) = 20 × 0.3 × 0.7 = 4.2)", "6", "3", "np = 6"],
       "ভেরিয়েন্স = npq। প্রমাণ বিচ্যুতি = √(npq) ≈ 2.05।"),
    _q("By Rolle's theorem, if f is continuous on [a, b], differentiable on (a, b), and f(a) = f(b), then:", ["There exists c ∈ (a, b) such that f'(c) = 0", "f is constant", "f'(a) = 0", "f has no extremum"],
       "Rolle's is a special case of MVT. It guarantees at least one stationary point between a and b.",
       "রোলের উপপাদ্যে f [a, b]-এ সতত, (a, b)-এ অবকলনযোগ্য এবং f(a) = f(b) হলে:", ["c ∈ (a, b) আছে যাতে f'(c) = 0", "f ধ্রুবক", "f'(a) = 0", "f-এর কোনো চরম নেই"],
       "রোলের উপপাদ্য MVT-এর বিশেষ ক্ষেত্র। a ও b-এর মধ্যে অন্তত একটি স্থির বিন্দু নিশ্চিত করে।"),
    _q("The Cauchy-Schwarz inequality for vectors states: (a · b)² ≤ ?", ["|a|² |b|² (with equality when a and b are parallel)", "|a|² + |b|²", "|a||b|", "|a + b|²"],
       "Equivalent to |cosθ| ≤ 1. Used in probability, statistics, and analysis.",
       "ভেক্টরের জন্য কশি-শোয়ার্জ অসমতা: (a · b)² ≤ ?", ["|a|² |b|² (a ও b সমান্তরাল হলে সমতা)", "|a|² + |b|²", "|a||b|", "|a + b|²"],
       "|cosθ| ≤ 1-এর সমতুল্য। সম্ভাবনা, পরিসংখ্যান ও বিশ্লেষণে ব্যবহার।"),
    _q("The Taylor series expansion of eˣ around x = 0 is:", ["1 + x + x²/2! + x³/3! + … (converges for all x)", "1 + x + x² + x³ + …", "Σ xⁿ", "1 + x²/2! + x⁴/4! + …"],
       "MacLaurin series (Taylor at 0). Radius of convergence = ∞. Used in bridge load calculations and numerical methods.",
       "x = 0 এর চারপাশে eˣ-এর টেলর ধারা:", ["1 + x + x²/2! + x³/3! + … (সব x-এর জন্য অভিসারী)", "1 + x + x² + x³ + …", "Σ xⁿ", "1 + x²/2! + x⁴/4! + …"],
       "ম্যাকলরিন ধারা। অভিসরণ ব্যাসার্ধ = ∞।"),
    _q("The condition for three planes to have exactly one common point (unique solution) is:", ["det of coefficient matrix ≠ 0 (Cramer's rule applies; unique intersection at one point)", "det = 0", "All planes are parallel", "Two planes are identical"],
       "If det ≠ 0: unique solution. det = 0: either no solution (inconsistent) or infinitely many solutions.",
       "তিনটি সমতলের ঠিক একটি সাধারণ বিন্দু থাকার শর্ত:", ["সহগ ম্যাট্রিক্সের det ≠ 0 (ক্রেমারের নিয়ম প্রযোজ্য)", "det = 0", "সব সমতল সমান্তরাল", "দুটো সমতল একই"],
       "det ≠ 0: অনন্য সমাধান। det = 0: কোনো সমাধান নেই বা অসীম সমাধান।"),
    _q("The principal argument of the complex number −1 − i√3 is:", ["−2π/3 (lies in third quadrant; arctan(√3/1) = π/3 below −x axis → −π + π/3 = −2π/3)", "2π/3", "4π/3", "π/3"],
       "Principal arg ∈ (−π, π]. Modulus = 2. Point at 240° from positive x-axis → principal arg = −2π/3.",
       "জটিল সংখ্যা −1 − i√3-এর মুখ্য আর্গুমেন্ট:", ["−2π/3 (তৃতীয় চতুর্ভাগে; −x অক্ষের নিচে π/3 → −π + π/3 = −2π/3)", "2π/3", "4π/3", "π/3"],
       "মুখ্য আর্গুমেন্ট ∈ (−π, π]। মডুলাস = 2।"),
    _q("The line x = 3 is the directrix of a parabola with vertex at the origin opening left. The equation of the parabola is:", ["y² = −12x (focus at (−3, 0); p = 3; y² = −4px = −12x)", "y² = 12x", "x² = 12y", "y² = 6x"],
       "Directrix x = a means focus at (−a, 0) for leftward parabola. 4p = 12.",
       "x = 3 হল মূলবিন্দুতে শীর্ষ ও বামদিকে খোলা পরাবৃত্তের নিয়ামক রেখা। পরাবৃত্তের সমীকরণ:", ["y² = −12x (ফোকাস (−3, 0); y² = −12x)", "y² = 12x", "x² = 12y", "y² = 6x"],
       "নিয়ামক x = a মানে বাম-পরাবৃত্তে ফোকাস (−a, 0)।"),
    _q("If f(x) = |x|, then f is:", ["Continuous everywhere but not differentiable at x = 0 (left derivative = −1, right = +1)", "Differentiable everywhere", "Not continuous at x = 0", "Differentiable at x = 0 with f'(0) = 0"],
       "Continuity: lim f(x) = 0 = f(0) ✓. Differentiability: left/right derivatives differ at 0 ✗.",
       "f(x) = |x| হলে f:", ["সর্বত্র সতত কিন্তু x = 0-এ অবকলনযোগ্য নয় (বাম অবকল = −1, ডান = +1)", "সর্বত্র অবকলনযোগ্য", "x = 0-এ সতত নয়", "x = 0-এ অবকলনযোগ্য f'(0) = 0 সহ"],
       "সাতত্য: lim f(x) = 0 = f(0) ✓। অবকলনীয়তা: বাম/ডান অবকল ভিন্ন ✗।"),
    _q("The maximum value of the function f(x, y) = x + y subject to x² + y² = 1 (by Lagrange multipliers) is:", ["√2 (optimal at x = y = 1/√2 → f = 2/√2 = √2)", "1", "2", "1/2"],
       "Lagrange: ∇f = λ∇g → (1,1) = λ(2x,2y) → x = y. On circle: x² + x² = 1 → x = 1/√2.",
       "লাগ্রঞ্জ গুণনীয়ক দিয়ে x² + y² = 1 সাপেক্ষে f(x, y) = x + y-এর সর্বোচ্চ মান:", ["√2 (x = y = 1/√2-এ সর্বোচ্চ → f = √2)", "1", "2", "1/2"],
       "লাগ্রঞ্জ: ∇f = λ∇g → x = y। বৃত্তে: x = 1/√2।"),
    _q("The number of real cube roots of −8 is:", ["1 (only −2 is a real cube root; the other two are complex)", "3", "2", "0"],
       "(−2)³ = −8. The other two cube roots are complex: 2e^(iπ/3) and 2e^(i5π/3).",
       "−8-এর বাস্তব ঘনমূলের সংখ্যা:", ["1 (শুধু −2 বাস্তব ঘনমূল; অন্য দুটো জটিল)", "3", "2", "0"],
       "(−2)³ = −8। অন্য দুটো মূল জটিল।"),
    _q("If P(A) = 0.6, P(B) = 0.4, and A and B are mutually exclusive, then P(A ∪ B) = ?", ["1.0 (P(A ∪ B) = P(A) + P(B) = 0.6 + 0.4 = 1.0 for mutually exclusive events)", "0.24", "0.76", "0.4"],
       "Mutually exclusive: P(A ∩ B) = 0. Addition rule: P(A ∪ B) = P(A) + P(B) − P(A ∩ B).",
       "P(A) = 0.6, P(B) = 0.4 এবং A ও B পরস্পর বিচ্ছিন্ন হলে P(A ∪ B) = ?", ["1.0 (0.6 + 0.4 = 1.0)", "0.24", "0.76", "0.4"],
       "পরস্পর বিচ্ছিন্ন: P(A ∩ B) = 0।"),
    _q("For a matrix A, if A² = A, then A is called:", ["Idempotent matrix (satisfies A² = A; projection matrices are idempotent)", "Nilpotent", "Orthogonal", "Skew-symmetric"],
       "Idempotent eigenvalues: 0 or 1 only. Trace = rank. Used in linear regression projection.",
       "A² = A হলে ম্যাট্রিক্স A-কে বলে:", ["অভেদ্য ম্যাট্রিক্স (A² = A; প্রজেকশন ম্যাট্রিক্স অভেদ্য)", "নিলপোটেন্ট", "অর্থোগোনাল", "তির্যক-সিমেট্রিক"],
       "অভেদ্য eigenvalue: শুধু 0 বা 1। Trace = rank।"),
    _q("The shortest distance between two skew lines r = a + λb and r = c + μd is:", ["|（c − a)·(b × d)| / |b × d|", "|(c − a) × (b × d)|", "|(b × d)|", "|(a − c) · b|"],
       "b × d gives a vector perpendicular to both lines. Project (c−a) onto this direction.",
       "দুটো তির্যক রেখা r = a + λb ও r = c + μd-এর মধ্যে সর্বনিম্ন দূরত্ব:", ["|（c − a)·(b × d)| / |b × d|", "|(c − a) × (b × d)|", "|(b × d)|", "|(a − c) · b|"],
       "b × d উভয় রেখার লম্বভাবে ভেক্টর দেয়। এই দিকে (c−a) প্রজেক্ট করুন।"),
    _q("For a differentiable function f, the Mean Value Theorem guarantees a c ∈ (a, b) such that:", ["f'(c) = (f(b) − f(a))/(b − a) (the instantaneous rate equals the average rate over [a, b])", "f'(c) = 0", "f(c) = (f(a) + f(b))/2", "f'(a) = f'(b)"],
       "MVT: the tangent line at some point c has the same slope as the secant from a to b.",
       "অবকলনযোগ্য f-এর জন্য মধ্যমান উপপাদ্য নিশ্চিত করে c ∈ (a, b) যাতে:", ["f'(c) = (f(b) − f(a))/(b − a) (তাৎক্ষণিক হার = [a, b]-এ গড় হার)", "f'(c) = 0", "f(c) = (f(a) + f(b))/2", "f'(a) = f'(b)"],
       "MVT: c বিন্দুতে স্পর্শরেখার ঢাল a থেকে b পর্যন্ত ছেদকের সমান।"),
    _q("The directional derivative of f(x, y) = x² + y² at (1, 1) in the direction of (1, 0) is:", ["2 (∂f/∂x = 2x; at (1,1): gradient = (2, 2); dot with unit vector (1,0) = 2)", "2√2", "4", "1"],
       "Directional derivative = ∇f · û. Gradient at (1,1): (2x, 2y) = (2, 2).",
       "f(x, y) = x² + y² বিন্দু (1, 1)-তে (1, 0) দিকে দিকমুখী অবকল:", ["2 (∂f/∂x = 2x; ঢাল = (2, 2); (1,0) দিয়ে ডট = 2)", "2√2", "4", "1"],
       "দিকমুখী অবকল = ∇f · û।"),
    _q("The equation of the plane through (1, 2, 3) with normal vector (2, −1, 4) is:", ["2(x−1) − (y−2) + 4(z−3) = 0 → 2x − y + 4z = 12", "2x − y + 4z = 0", "x + 2y + 3z = 12", "2x − y + 4z = 1"],
       "Plane: n·(r − r₀) = 0. Expanding: 2x − y + 4z = 2(1) − (2) + 4(3) = 12.",
       "(1, 2, 3) বিন্দু ও (2, −1, 4) অভিলম্ব ভেক্টর সহ সমতলের সমীকরণ:", ["2(x−1) − (y−2) + 4(z−3) = 0 → 2x − y + 4z = 12", "2x − y + 4z = 0", "x + 2y + 3z = 12", "2x − y + 4z = 1"],
       "সমতল: n·(r − r₀) = 0। প্রসারণ: 2x − y + 4z = 12।"),
    _q("The number of distinct permutations of the letters of MISSISSIPPI is:", ["34650 (11!/(4!×4!×2!×1!) = 39916800/24/24/2 = 34650)", "11!", "11!/4!", "7920"],
       "MISSISSIPPI: 11 letters; M=1, I=4, S=4, P=2. Formula: n!/∏(nᵢ!).",
       "MISSISSIPPI-এর অক্ষরের স্বতন্ত্র বিন্যাসের সংখ্যা:", ["34650 (11!/(4!×4!×2!×1!) = 34650)", "11!", "11!/4!", "7920"],
       "MISSISSIPPI: 11 অক্ষর; I=4, S=4, P=2। 11!/(4!×4!×2!) = 34650।"),
    _q("Which of the following series converges by the ratio test?", ["Σ n!/nⁿ (limit of |a_{n+1}/aₙ| = 1/e < 1)", "Σ 1/n (harmonic — diverges)", "Σ 1/√n (p=1/2 < 1 — diverges)", "Σ n (obviously diverges)"],
       "Ratio test: if lim |a_{n+1}/aₙ| < 1, series converges. Σn!/nⁿ: ratio → 1/e ≈ 0.368 < 1.",
       "অনুপাত পরীক্ষায় কোন ধারাটি অভিসারী?", ["Σ n!/nⁿ (|a_{n+1}/aₙ|-এর সীমা = 1/e < 1)", "Σ 1/n (হারমোনিক — অপসারী)", "Σ 1/√n (p=1/2 < 1 — অপসারী)", "Σ n (স্পষ্ট অপসারী)"],
       "অনুপাত পরীক্ষা: lim |a_{n+1}/aₙ| < 1 হলে অভিসারী।"),
    _q("The gradient ∇f of a scalar field f points in the direction of:", ["Maximum rate of increase of f (steepest ascent direction)", "Zero change", "Minimum value of f", "The tangent to a level curve"],
       "∇f is perpendicular to level curves/surfaces. |∇f| gives the magnitude of the maximum rate of change.",
       "স্কেলার ক্ষেত্র f-এর গ্রেডিয়েন্ট ∇f নির্দেশ করে:", ["f-এর সর্বোচ্চ পরিবর্তনের হারের দিক (সবচেয়ে খাড়া আরোহণ)", "শূন্য পরিবর্তন", "f-এর সর্বনিম্ন মানের দিক", "স্তর বক্ররেখার স্পর্শক"],
       "∇f স্তর বক্ররেখার লম্ব। |∇f| সর্বোচ্চ পরিবর্তনের মাত্রা।"),
    _q("The Bayes' theorem formula is:", ["P(A|B) = P(B|A)P(A)/P(B)", "P(A|B) = P(A)/P(B)", "P(A|B) = P(A)P(B)", "P(A|B) = P(A∩B)/P(A)"],
       "P(B) = Σ P(B|Aᵢ)P(Aᵢ) — law of total probability. Bayes updates prior P(A) to posterior P(A|B).",
       "বেইজের উপপাদ্যের সূত্র:", ["P(A|B) = P(B|A)P(A)/P(B)", "P(A|B) = P(A)/P(B)", "P(A|B) = P(A)P(B)", "P(A|B) = P(A∩B)/P(A)"],
       "P(B) = Σ P(B|Aᵢ)P(Aᵢ)। বেইজ পূর্ব-সম্ভাবনাকে পরবর্তী সম্ভাবনায় আপডেট করে।"),
    _q("The value of ∫₀^∞ e^(−x²) dx is:", ["√π/2 (Gaussian integral; ∫₋∞^∞ e^(−x²) dx = √π)", "1", "π/2", "√π"],
       "Proof uses polar coordinates in 2D. Critical in probability (normal distribution) and bridge load statistics.",
       "∫₀^∞ e^(−x²) dx-এর মান:", ["√π/2 (গাউসিয়ান ইন্টিগ্রাল; ∫₋∞^∞ e^(−x²) dx = √π)", "1", "π/2", "√π"],
       "প্রমাণ 2D মেরু স্থানাঙ্ক ব্যবহার করে। সম্ভাবনায় (স্বাভাবিক বিতরণ) গুরুত্বপূর্ণ।"),
    _q("The number of solutions of x² ≡ 1 (mod 8) in {0, 1, 2, …, 7} is:", ["4 (x = 1, 3, 5, 7; each gives x² ≡ 1 mod 8)", "2", "1", "8"],
       "1² = 1 ✓; 3² = 9 ≡ 1 ✓; 5² = 25 ≡ 1 ✓; 7² = 49 ≡ 1 ✓. 0,2,4,6 give 0,4,0,4.",
       "{0,…,7}-এ x² ≡ 1 (mod 8)-এর সমাধানের সংখ্যা:", ["4 (x = 1, 3, 5, 7)", "2", "1", "8"],
       "1² = 1; 3² = 9 ≡ 1; 5² = 25 ≡ 1; 7² = 49 ≡ 1 (mod 8)।"),
    _q("If f(x) = sin x, the Maclaurin series is:", ["x − x³/3! + x⁵/5! − … = Σ (−1)ⁿx^(2n+1)/(2n+1)!", "x + x³/3! + x⁵/5! + …", "1 − x²/2! + x⁴/4! − …", "x + x²/2! + x³/3! + …"],
       "sin x: odd function, only odd powers. cos x: even powers. Both series converge for all x.",
       "f(x) = sin x-এর ম্যাকলরিন ধারা:", ["x − x³/3! + x⁵/5! − … = Σ (−1)ⁿx^(2n+1)/(2n+1)!", "x + x³/3! + x⁵/5! + …", "1 − x²/2! + x⁴/4! − …", "x + x²/2! + x³/3! + …"],
       "sin x: বিজোড় ফাংশন, শুধু বিজোড় ঘাত।"),
    _q("The residue of f(z) = 1/(z² + 1) at z = i is:", ["1/(2i) = −i/2 (simple pole; residue = lim_{z→i} (z−i)f(z) = 1/(z+i)|_{z=i} = 1/(2i))", "1/2", "i/2", "−1/2"],
       "1/(z²+1) = 1/((z−i)(z+i)). Residue at z = i: 1/(i+i) = 1/(2i) = −i/2.",
       "f(z) = 1/(z² + 1)-এর z = i-তে অবশিষ্ট:", ["1/(2i) = −i/2", "1/2", "i/2", "−1/2"],
       "1/(z²+1) = 1/((z−i)(z+i))। z = i-তে অবশিষ্ট = 1/(2i) = −i/2।"),
    _q("Stokes' theorem relates:", ["A surface integral of the curl to a line integral around the boundary: ∬(∇×F)·dS = ∮F·dr", "Two volume integrals", "Gradient and divergence", "Scalar and vector potentials"],
       "Stokes generalises Green's theorem to 3D surfaces. Used in fluid dynamics and electromagnetic field theory.",
       "স্টোকসের উপপাদ্য সম্পর্কিত:", ["কার্লের পৃষ্ঠ ইন্টিগ্রাল ও সীমানার চারপাশে রেখা ইন্টিগ্রাল: ∬(∇×F)·dS = ∮F·dr", "দুটো আয়তন ইন্টিগ্রাল", "গ্রেডিয়েন্ট ও ডাইভার্জেন্স", "স্কেলার ও ভেক্টর পোটেনশিয়াল"],
       "স্টোকস গ্রিনের উপপাদ্যকে 3D পৃষ্ঠে সাধারণীকরণ করে।"),
    _q("The Laplace transform of f(t) = t is:", ["1/s² (L{tⁿ} = n!/s^(n+1); n = 1 → 1/s²)", "1/s", "s", "2/s³"],
       "L{1} = 1/s. L{t} = 1/s². L{t²} = 2/s³. L{eᵃᵗ} = 1/(s−a) for s > a.",
       "f(t) = t-এর ল্যাপ্লাস রূপান্তর:", ["1/s² (L{tⁿ} = n!/s^(n+1); n = 1 → 1/s²)", "1/s", "s", "2/s³"],
       "L{1} = 1/s। L{t} = 1/s²। L{t²} = 2/s³।"),
    _q("The characteristic equation of a 2×2 matrix A is det(A − λI) = 0. If A = [[1,2],[3,4]], the eigenvalues are:", ["λ = (5 ± √33)/2 ≈ −0.37 and 5.37 (char poly: λ² − 5λ − 2 = 0)", "1 and 4", "2 and 3", "5 and −1"],
       "det([[1−λ,2],[3,4−λ]]) = (1−λ)(4−λ) − 6 = λ² − 5λ + 4 − 6 = λ² − 5λ − 2 = 0.",
       "A = [[1,2],[3,4]]-এর আইগেনমান:", ["λ = (5 ± √33)/2 ≈ −0.37 ও 5.37 (λ² − 5λ − 2 = 0)", "1 ও 4", "2 ও 3", "5 ও −1"],
       "det([[1−λ,2],[3,4−λ]]) = λ² − 5λ − 2 = 0।"),
]

ITEMS = tuple(NUMERIC + CONCEPTS)
