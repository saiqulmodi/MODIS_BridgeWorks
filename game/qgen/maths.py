"""Maths high-yield: Class 11/12 NCERT and JEE topics, plus BE engineering maths."""
import math
from fractions import Fraction

from . import facts, fmt, template

S = "math"
C11 = (11, 15, 13, 14, 16)
C12 = (12, 15, 13, 14, 16)
BE = (15, 16)
N = 60


def frac(x):
    f = Fraction(x).limit_denominator(1000)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


@template(C11, S, N)
def quadratic(rng, level):
    r1, r2 = rng.randrange(-9, 10), rng.randrange(-9, 10)
    a = rng.choice([1, 1, 2, 3])
    b, c = -a * (r1 + r2), a * r1 * r2
    eq = f"{a if a != 1 else ''}x² {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0"
    kind = rng.randrange(3)
    if kind == 0:
        return (f"What is the sum of the roots of {eq}?", str(r1 + r2), [str(-(r1 + r2)), str(r1 * r2), frac(b / a) if b else "1", str(r1 + r2 + 1)],
                f"Sum = -b/a = {frac(-b / a)}.")
    if kind == 1:
        return (f"What is the product of the roots of {eq}?", str(r1 * r2), [str(-r1 * r2) if r1 * r2 else "1", str(r1 + r2), str(c), str(r1 * r2 + 1)],
                f"Product = c/a = {frac(c / a)}.")
    roots = sorted({r1, r2})
    ans = ", ".join(map(str, roots))
    return (f"Solve {eq}.", ans, [", ".join(str(-r) for r in roots), f"{roots[0] + 1}, {roots[-1] + 1}", f"{roots[0]}, {-roots[-1]}" if roots[-1] else "1, 2",
                                  f"{roots[0] * 2}, {roots[-1] * 2}" if any(roots) else "2, 3"],
            f"It factors as {a if a != 1 else ''}(x - ({r1}))(x - ({r2})) = 0.")


@template(C11, S, N)
def sequences(rng, level):
    kind = rng.randrange(3)
    a, d, n = rng.randrange(-10, 20), rng.randrange(1, 9), rng.randrange(8, 40)
    if kind == 0:
        t = a + (n - 1) * d
        return (f"The AP {a}, {a + d}, {a + 2 * d}, ... What is its {n}th term?", str(t), [str(a + n * d), str(t - d + 1), str(a * n), str(t + d)],
                f"aₙ = a + (n - 1)d = {a} + {n - 1} x {d} = {t}.")
    if kind == 1:
        s = n * (2 * a + (n - 1) * d) // 2 if (n * (2 * a + (n - 1) * d)) % 2 == 0 else n * (2 * a + (n - 1) * d) / 2
        return (f"Find the sum of the first {n} terms of the AP {a}, {a + d}, {a + 2 * d}, ...", fmt(s),
                [fmt(n * (a + (n - 1) * d)), fmt(s + a), fmt(n * (2 * a + n * d) / 2), fmt(s * 2)], f"Sₙ = n/2 (2a + (n - 1)d) = {fmt(s)}.")
    a, r = rng.randrange(1, 10), rng.choice([Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4)])
    s = Fraction(a) / (1 - r)
    return (f"Find the sum to infinity of the GP {a}, {frac(a * r)}, {frac(a * r * r)}, ...", frac(s),
            [frac(a / (1 + r)), frac(a * r / (1 - r)), frac(s * 2), frac(a / r)], f"S∞ = a/(1 - r) = {a}/(1 - {frac(r)}) = {frac(s)}.")


@template(C11, S, N)
def perm_comb(rng, level):
    kind = rng.randrange(3)
    n = rng.randrange(5, 13)
    r = rng.randrange(2, min(6, n))
    if kind == 0:
        v = math.comb(n, r)
        return (f"In how many ways can a committee of {r} be chosen from {n} people?", f"{v:,}",
                [f"{math.perm(n, r):,}", f"{math.comb(n, r - 1):,}", f"{n * r:,}", f"{math.comb(n + 1, r):,}"], f"ⁿCᵣ = {n}C{r} = {v:,}.")
    if kind == 1:
        v = math.perm(n, r)
        return (f"In how many ways can {r} different prizes be given to {n} students (one prize each at most)?", f"{v:,}",
                [f"{math.comb(n, r):,}", f"{n ** r:,}", f"{r ** n:,}" if r ** n < 10 ** 9 else "1", f"{math.perm(n, r - 1):,}"], f"ⁿPᵣ = {n}!/({n}-{r})! = {v:,}.")
    word = rng.choice(["BANANA", "LETTER", "COMMITTEE", "STATISTICS", "ENGINEER", "BRIDGE", "MISSISSIPPI", "PHYSICS", "CALCULUS"])
    v = math.factorial(len(word))
    for ch in set(word):
        v //= math.factorial(word.count(ch))
    return (f"How many different arrangements are there of the letters of '{word}'?", f"{v:,}",
            [f"{math.factorial(len(word)):,}", f"{v * 2:,}", f"{v // 2:,}", f"{math.factorial(len(set(word))):,}"],
            f"{len(word)}! divided by the factorials of the repeated letters = {v:,}.")


@template(C11, S, N)
def binomial(rng, level):
    n = rng.randrange(4, 11)
    r = rng.randrange(1, n)
    a, b = rng.randrange(1, 4), rng.randrange(1, 4)
    coef = math.comb(n, r) * a ** (n - r) * b ** r
    return (f"What is the coefficient of x^{r} in ({a} + {b}x)^{n}?", f"{coef:,}",
            [f"{math.comb(n, r):,}", f"{math.comb(n, r) * a ** r * b ** (n - r):,}", f"{coef * 2:,}", f"{math.comb(n, r + 1) * a ** (n - r - 1) * b ** (r + 1):,}"],
            f"T(r+1) = ⁿCᵣ a^(n-r) (bx)^r: {n}C{r} x {a}^{n - r} x {b}^{r} = {coef:,}.")


@template(C11, S, N)
def probability(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        s = rng.randrange(2, 13)
        ways = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s)
        return (f"Two fair dice are thrown. What is the probability that the sum is {s}?", frac(Fraction(ways, 36)),
                [frac(Fraction(ways + 1, 36)), frac(Fraction(1, s)), frac(Fraction(ways, 12)), frac(Fraction(max(ways - 1, 2), 36))],
                f"{ways} favourable outcomes out of 36.")
    if kind == 1:
        n = rng.randrange(2, 7)
        return (f"A fair coin is tossed {n} times. What is the probability of at least one head?", frac(1 - Fraction(1, 2 ** n)),
                [frac(Fraction(1, 2 ** n)), frac(Fraction(1, 2)), frac(Fraction(n, 2 ** n)), frac(1 - Fraction(1, 2 ** (n - 1)))],
                f"1 - P(no head) = 1 - (½)^{n} = {frac(1 - Fraction(1, 2 ** n))}.")
    pa, pb = rng.choice([Fraction(1, 2), Fraction(1, 3), Fraction(2, 5), Fraction(1, 4)]), rng.choice([Fraction(1, 3), Fraction(1, 5), Fraction(3, 4), Fraction(2, 3)])
    p = pa + pb - pa * pb
    return (f"Independent events A and B have P(A) = {frac(pa)} and P(B) = {frac(pb)}. What is P(A or B)?", frac(p),
            [frac(pa + pb) if pa + pb <= 1 else frac(pa * pb + Fraction(1, 10)), frac(pa * pb), frac(1 - pa * pb), frac(p / 2)],
            f"P(A ∪ B) = P(A) + P(B) - P(A)P(B) = {frac(p)}.")


@template(C11, S, N)
def coordinate(rng, level):
    kind = rng.randrange(3)
    x1, y1, x2, y2 = (rng.randrange(-9, 10) for _ in range(4))
    if kind == 0:
        dx, dy = x2 - x1, y2 - y1
        d2 = dx * dx + dy * dy or 1
        d = math.sqrt(d2)
        ans = str(int(d)) if d == int(d) else f"√{d2}"
        return (f"What is the distance between ({x1}, {y1}) and ({x2}, {y2})?", ans,
                [f"√{d2 + 2}", f"√{abs(dx) + abs(dy)}" if abs(dx) + abs(dy) != d2 else f"√{d2 * 2}", str(abs(dx) + abs(dy)), f"√{d2 - 1}" if d2 > 2 else "3"],
                f"d = √(Δx² + Δy²) = √({dx}² + {dy}²) = {ans}.")
    if kind == 1:
        a, b, c = rng.randrange(1, 6), rng.randrange(-6, 7) or 1, rng.randrange(-10, 11)
        px, py = rng.randrange(-5, 6), rng.randrange(-5, 6)
        num = abs(a * px + b * py + c)
        den2 = a * a + b * b
        d = num / math.sqrt(den2)
        return (f"What is the distance of the point ({px}, {py}) from the line {a}x {'+' if b >= 0 else '-'} {abs(b)}y {'+' if c >= 0 else '-'} {abs(c)} = 0?",
                fmt(d), [fmt(num / den2), fmt(num), fmt(d * 2) if d else "1", fmt((num + 1) / math.sqrt(den2))], f"|ax + by + c| / √(a² + b²) = {num}/√{den2} = {fmt(d)}.")
    h, k, r = rng.randrange(-6, 7), rng.randrange(-6, 7), rng.randrange(1, 9)
    c = h * h + k * k - r * r
    return (f"What is the radius of the circle x² + y² {'-' if h >= 0 else '+'} {abs(2 * h)}x {'-' if k >= 0 else '+'} {abs(2 * k)}y {'+' if c >= 0 else '-'} {abs(c)} = 0?",
            str(r), [str(r * r), str(r + 1), str(abs(c)) if abs(c) != r else str(r + 2), str(h + k) if h + k != r else str(r - 1)],
            f"Centre ({h}, {k}); r = √(g² + f² - c) = √({h * h} + {k * k} - ({c})) = {r}.")


@template(C11, S, 20)
def conics(rng, level):
    kind = rng.randrange(2)
    if kind == 0:
        a = rng.randrange(1, 10)
        return (f"What is the focus of the parabola y² = {4 * a}x?", f"({a}, 0)", [f"(0, {a})", f"({4 * a}, 0)", f"({-a}, 0)", f"({2 * a}, 0)"],
                f"y² = 4ax with a = {a}: focus ({a}, 0), directrix x = -{a}.")
    a, b = sorted(rng.sample(range(2, 11), 2), reverse=True)
    e = math.sqrt(1 - b * b / (a * a))
    return (f"What is the eccentricity of the ellipse x²/{a * a} + y²/{b * b} = 1?", fmt(e),
            [fmt(b / a), fmt(math.sqrt(1 + b * b / (a * a))), fmt(1 - b / a), fmt(e * e)], f"e = √(1 - b²/a²) = √(1 - {b * b}/{a * a}) = {fmt(e)}.")


@template(C11, S, 20)
def complex_numbers(rng, level):
    if rng.random() < 0.5:
        a, b = rng.choice([(3, 4), (5, 12), (6, 8), (8, 15), (1, 1), (2, 3), (1, 2)])
        a, b = a * rng.choice([1, -1]), b * rng.choice([1, -1])
        m2 = a * a + b * b
        m = math.sqrt(m2)
        ans = str(int(m)) if m == int(m) else f"√{m2}"
        return (f"What is the modulus of {a} {'+' if b >= 0 else '-'} {abs(b)}i?", ans, [str(abs(a) + abs(b)), f"√{m2 + 1}", str(m2), f"√{abs(a * b)}"],
                f"|z| = √(a² + b²) = √{m2} = {ans}.")
    n = rng.randrange(5, 200)
    vals = {0: "1", 1: "i", 2: "-1", 3: "-i"}
    return (f"What is i^{n}?", vals[n % 4], [v for k, v in vals.items() if k != n % 4], f"Powers of i repeat every 4; {n} mod 4 = {n % 4}.")


@template(C12, S, N)
def determinants(rng, level):
    if rng.random() < 0.5 or level == 12:
        a, b, c, d = (rng.randrange(-9, 10) for _ in range(4))
        det = a * d - b * c
        return (f"Find the determinant of the matrix [[{a}, {b}], [{c}, {d}]].", str(det), [str(a * d + b * c), str(a * b - c * d), str(-det) if det else "1", str(a + d)],
                f"|A| = ad - bc = {a}x{d} - {b}x{c} = {det}.")
    m = [[rng.randrange(-4, 5) for _ in range(3)] for _ in range(3)]
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
           + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    k = rng.choice([2, 3])
    if rng.random() < 0.5:
        return (f"If |A| = {det or 5} for a 3x3 matrix A, what is |{k}A|?", str((det or 5) * k ** 3),
                [str((det or 5) * k), str((det or 5) * k * k), str((det or 5) + k ** 3), str((det or 5) * k ** 4)], f"|kA| = k³|A| for a 3x3 matrix.")
    return (f"Find the determinant of [[{m[0][0]}, {m[0][1]}, {m[0][2]}], [{m[1][0]}, {m[1][1]}, {m[1][2]}], [{m[2][0]}, {m[2][1]}, {m[2][2]}]].",
            str(det), [str(-det) if det else "1", str(det + 2), str(det - 2), str(det * 2) if det else "4"], "Expand along the first row.")


@template(C12, S, N)
def derivatives(rng, level):
    kind = rng.randrange(3)
    if kind == 0:
        a, n, b, x0 = rng.randrange(1, 7), rng.randrange(2, 6), rng.randrange(-9, 10), rng.randrange(-3, 4)
        val = a * n * x0 ** (n - 1) + b
        return (f"If f(x) = {a}x^{n} + {b}x, what is f'({x0})?", str(val), [str(a * x0 ** n + b * x0), str(a * n * x0 ** n + b), str(val + a), str(a * (n - 1) * x0 ** (n - 2) + b) if x0 else str(val + 2)],
                f"f'(x) = {a * n}x^{n - 1} + {b}; at x = {x0}: {val}.")
    if kind == 1:
        a = rng.randrange(2, 9)
        b = rng.randrange(2, 9)
        return (f"Evaluate lim(x->0) sin({a}x) / ({b}x).", frac(Fraction(a, b)), [frac(Fraction(b, a)), "1", "0", str(a * b)],
                f"sin({a}x)/({a}x) -> 1, so the limit is {a}/{b}.")
    a, n = rng.randrange(1, 5), rng.randrange(2, 8)
    v = n * a ** (n - 1)
    return (f"Evaluate lim(x->{a}) (x^{n} - {a ** n}) / (x - {a}).", str(v), [str(a ** n), str(n * a ** n), str((n - 1) * a ** (n - 1)), str(v + n)],
            f"lim (xⁿ - aⁿ)/(x - a) = n a^(n-1) = {n} x {a}^{n - 1} = {v}.")


@template(C12, S, N)
def integrals(rng, level):
    a, n = rng.randrange(1, 7), rng.randrange(1, 5)
    lo, hi = rng.randrange(0, 2), rng.randrange(2, 5)
    v = Fraction(a, n + 1) * (hi ** (n + 1) - lo ** (n + 1))
    if rng.random() < 0.7:
        term = ("" if a == 1 else str(a)) + ("x" if n == 1 else f"x^{n}")
        return (f"Evaluate ∫ from {lo} to {hi} of {term} dx.", frac(v),
                [frac(a * (hi ** n - lo ** n)), frac(Fraction(a, n) * (hi ** n - lo ** n)), frac(v * 2), frac(a * n * (hi ** (n - 1) - lo ** (n - 1))) if n > 1 else frac(v + 1)],
                f"∫{term} dx = ({frac(Fraction(a, n + 1))})x^{n + 1}; evaluate from {lo} to {hi}: {frac(v)}.")
    k = rng.randrange(1, 6)
    return (f"Evaluate ∫ from 0 to π/2 of {k} sin x dx.", str(k), [str(2 * k), "0", f"{k}π/2", str(-k)], f"{k}[-cos x] from 0 to π/2 = {k}(0 + 1) = {k}.")


@template(C12, S, N)
def vectors(rng, level):
    a = [rng.randrange(-5, 6) for _ in range(3)]
    b = [rng.randrange(-5, 6) for _ in range(3)]
    va = f"{a[0]}i {'+' if a[1] >= 0 else '-'} {abs(a[1])}j {'+' if a[2] >= 0 else '-'} {abs(a[2])}k"
    vb = f"{b[0]}i {'+' if b[1] >= 0 else '-'} {abs(b[1])}j {'+' if b[2] >= 0 else '-'} {abs(b[2])}k"
    kind = rng.randrange(3)
    if kind == 0:
        d = sum(x * y for x, y in zip(a, b))
        return (f"Find a·b for a = {va} and b = {vb}.", str(d), [str(d + 1), str(-d) if d else "2", str(sum(x + y for x, y in zip(a, b))), str(a[0] * b[0])],
                f"a·b = a1b1 + a2b2 + a3b3 = {d}.")
    if kind == 1:
        c = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
        ans = f"{c[0]}i {'+' if c[1] >= 0 else '-'} {abs(c[1])}j {'+' if c[2] >= 0 else '-'} {abs(c[2])}k"
        neg = f"{-c[0]}i {'+' if -c[1] >= 0 else '-'} {abs(c[1])}j {'+' if -c[2] >= 0 else '-'} {abs(c[2])}k"
        alt = f"{c[0]}i {'+' if -c[1] >= 0 else '-'} {abs(c[1])}j {'+' if c[2] >= 0 else '-'} {abs(c[2])}k"
        alt2 = f"{c[2]}i {'+' if c[1] >= 0 else '-'} {abs(c[1])}j {'+' if c[0] >= 0 else '-'} {abs(c[0])}k"
        return (f"Find a x b for a = {va} and b = {vb}.", ans, [neg, alt, alt2, f"{c[0] + 1}i + {abs(c[1])}j + {abs(c[2])}k"],
                "Use the determinant with rows (i, j, k), a and b.")
    m2 = sum(x * x for x in a) or 1
    m = math.sqrt(m2)
    ans = str(int(m)) if m == int(m) else f"√{m2}"
    return (f"What is the magnitude of a = {va}?", ans, [str(sum(abs(x) for x in a)), f"√{m2 + 1}", str(m2), f"√{m2 - 1}" if m2 > 2 else "3"],
            f"|a| = √(sum of squares) = √{m2}.")


@template(BE, S, N)
def eigenvalues(rng, level):
    l1, l2 = rng.randrange(-5, 8), rng.randrange(-5, 8)
    b = rng.randrange(-4, 5)
    a, d = l1, l2
    c = 0
    if rng.random() < 0.5:
        return (f"What are the eigenvalues of the triangular matrix [[{a}, {b}], [{c}, {d}]]?", ", ".join(map(str, sorted({a, d}))) if a != d else f"{a}, {a}",
                [f"{a + b}, {d}", f"{a}, {b}" if b not in (a, d) else f"{a + 1}, {d + 1}", f"{-a}, {-d}" if a or d else "1, 2", f"{a * d}, {a + d}"],
                "A triangular matrix has its diagonal entries as eigenvalues.")
    tr, det = l1 + l2, l1 * l2
    return (f"A 2x2 matrix has trace {tr} and determinant {det}. What are its eigenvalues?", ", ".join(map(str, sorted({l1, l2}))) if l1 != l2 else f"{l1}, {l1}",
            [f"{tr}, {det}", f"{-l1}, {-l2}" if l1 or l2 else "1, -1", f"{l1 + 1}, {l2 - 1}", f"{tr // 2}, {tr - tr // 2}" if tr // 2 not in (l1, l2) else f"{l1 + 2}, {l2}"],
            f"λ² - {tr}λ + {det} = 0  ->  λ = {l1}, {l2}.")


@template(BE, S, N)
def ode_growth(rng, level):
    y0, k, t = rng.randrange(10, 500, 10), rng.choice([0.05, 0.1, 0.2, -0.1, -0.05, 0.3]), rng.randrange(2, 15)
    y = y0 * math.exp(k * t)
    return (f"dy/dt = {k}y with y(0) = {y0}. What is y at t = {t}?", fmt(y, 4),
            [fmt(y0 * (1 + k * t), 4), fmt(y0 * math.exp(-k * t), 4), fmt(y0 * k * t, 4), fmt(y0 * math.exp(k), 4)], f"y = y0 e^(kt) = {y0} e^({fmt(k * t)}) = {fmt(y, 4)}.")


@template(BE, S, 20)
def newton_raphson(rng, level):
    c = rng.choice([2, 3, 5, 7, 10, 20])
    x0 = rng.choice([1, 2, 3, 4])
    x1 = x0 - (x0 * x0 - c) / (2 * x0)
    return (f"Using Newton-Raphson on f(x) = x² - {c} from x0 = {x0}, what is x1?", fmt(x1, 4),
            [fmt(x0 + (x0 * x0 - c) / (2 * x0), 4), fmt(math.sqrt(c), 4), fmt(x0 - (x0 * x0 - c) / x0, 4), fmt(x1 + 0.5, 4)],
            f"x1 = x0 - f(x0)/f'(x0) = {x0} - ({x0 * x0 - c})/({2 * x0}) = {fmt(x1, 4)}.")


@template(BE, S, 20)
def binomial_dist(rng, level):
    n, p, k = rng.randrange(3, 9), rng.choice([0.1, 0.2, 0.25, 0.3, 0.5]), rng.randrange(0, 4)
    pr = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    return (f"A component fails with probability {p}. Out of {n} independent components, what is the probability exactly {k} fail?",
            fmt(pr, 3), [fmt(p ** k, 3), fmt(math.comb(n, k) * p ** k, 3), fmt(1 - pr, 3), fmt(pr * 2, 3)],
            f"P = ⁿCₖ pᵏ (1-p)^(n-k) = {fmt(pr, 3)}.")


facts((11, 12, 15, 13, 14, 16), S, [
    ("The derivative of sin x is:", "cos x", ["-cos x", "sin x", "-sin x"], "d/dx sin x = cos x; d/dx cos x = -sin x."),
    ("∫ (1/x) dx equals:", "ln|x| + C", ["x² / 2 + C", "-1/x² + C", "e^x + C"], "The natural log is the antiderivative of 1/x."),
    ("The derivative of e^(2x) is:", "2e^(2x)", ["e^(2x)", "e^(2x)/2", "2x e^(2x)"], "Chain rule."),
    ("sin² x + cos² x equals:", "1", ["0", "2", "tan x"], "The Pythagorean identity."),
    ("The value of sin 30° is:", "1/2", ["√3/2", "1", "1/√2"], "sin 30° = cos 60° = 1/2."),
    ("A matrix A with A^T = A is:", "Symmetric", ["Skew-symmetric", "Singular", "Orthogonal"], "Skew-symmetric: A^T = -A."),
    ("If |A| = 0, the matrix A is:", "Singular (no inverse)", ["Invertible", "Identity", "Orthogonal"], "A⁻¹ = adj A / |A| needs |A| ≠ 0."),
    ("The number of subsets of a set with n elements is:", "2^n", ["n²", "n!", "2n"], "Each element is in or out."),
    ("log_a(xy) equals:", "log_a x + log_a y", ["log_a x x log_a y", "log_a x - log_a y", "(log_a x)/(log_a y)"], "Product rule of logarithms."),
    ("The slope of a line perpendicular to one with slope m is:", "-1/m", ["m", "1/m", "-m"], "m1 m2 = -1."),
    ("e^(iπ) + 1 equals:", "0", ["1", "-1", "i"], "Euler's identity."),
    ("A function that has a derivative at a point is always ___ there.", "Continuous", ["Discontinuous", "Zero", "Increasing"],
     "Differentiable implies continuous (not the reverse)."),
    ("The order of the differential equation y'' + 3y' + 2y = 0 is:", "2", ["1", "3", "0"], "Highest derivative present."),
    ("The mean of a binomial distribution B(n, p) is:", "np", ["npq", "n/p", "p/n"], "Variance is npq."),
    ("The angle between two vectors with zero dot product is:", "90°", ["0°", "180°", "45°"], "a·b = |a||b|cos θ = 0."),
    ("Rank of an n x n invertible matrix is:", "n", ["0", "1", "n - 1"], "Full rank means invertible."),
    ("Laplace transform of 1 is:", "1/s", ["s", "1", "e^(-s)"], "L{1} = ∫ e^(-st) dt = 1/s (s > 0)."),
    ("The Fourier series represents a periodic function as a sum of:", "Sines and cosines", ["Polynomials only",
     "Exponential growth terms", "Logarithms"], "Each harmonic has its own coefficient."),
])


@template(C12, S, N)
def matrix_product(rng, level):
    A = [[rng.randrange(-4, 5) for _ in range(2)] for _ in range(2)]
    B = [[rng.randrange(-4, 5) for _ in range(2)] for _ in range(2)]
    i, j = rng.randrange(2), rng.randrange(2)
    v = A[i][0] * B[0][j] + A[i][1] * B[1][j]
    return (f"A = [[{A[0][0]}, {A[0][1]}], [{A[1][0]}, {A[1][1]}]], B = [[{B[0][0]}, {B[0][1]}], [{B[1][0]}, {B[1][1]}]]. "
            f"What is the entry in row {i + 1}, column {j + 1} of AB?", str(v),
            [str(A[i][j] * B[i][j]), str(A[0][i] * B[j][0] + A[1][i] * B[j][1]), str(v + 1), str(-v) if v else "2"],
            f"(AB)ij = row {i + 1} of A · column {j + 1} of B = {v}.")


@template(C12, S, N)
def bayes(rng, level):
    p1 = rng.choice([Fraction(1, 2), Fraction(2, 5), Fraction(3, 5), Fraction(1, 3), Fraction(2, 3)])
    d1, d2 = rng.choice([Fraction(1, 20), Fraction(1, 10), Fraction(1, 25)]), rng.choice([Fraction(1, 50), Fraction(1, 20), Fraction(3, 100)])
    pd = p1 * d1 + (1 - p1) * d2
    post = p1 * d1 / pd
    return (f"Machine A makes {frac(p1)} of the bolts and machine B the rest. A's defect rate is {frac(d1)} and B's is {frac(d2)}. "
            f"A bolt is defective. What is the probability it came from A?", frac(post),
            [frac(p1), frac(d1), frac(1 - post), frac(p1 * d1)], f"Bayes: P(A|D) = P(A)P(D|A) / P(D) = {frac(p1 * d1)} / {frac(pd)} = {frac(post)}.")
