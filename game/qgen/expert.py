"""Commerce / accountancy numericals (Class 11 up) and Expert Engineer integration questions."""
from . import facts, fmt, template, unit

C = "commercials"
LEVELS = (11, 12, 15, 13, 14, 16)
N = 40


@template(LEVELS, C, N)
def accounting_equation(rng, level):
    a = rng.randrange(100, 2000, 10) * 1000
    l = rng.randrange(10, a // 1000 - 10, 5) * 1000
    if rng.random() < 0.5:
        return (f"Total assets are ₹{a:,} and liabilities are ₹{l:,}. What is the capital?", f"₹{a - l:,}",
                [f"₹{a + l:,}", f"₹{l:,}", f"₹{(a - l) // 2:,}", f"₹{a:,}"], "Assets = Liabilities + Capital.")
    return (f"Capital is ₹{a - l:,} and liabilities are ₹{l:,}. What are the total assets?", f"₹{a:,}",
            [f"₹{a - 2 * l:,}" if a > 2 * l else f"₹{a + 1000:,}", f"₹{l:,}", f"₹{a + l:,}", f"₹{a - l:,}"], "Assets = Liabilities + Capital.")


@template(LEVELS, C, N)
def ratios(rng, level):
    kind = rng.randrange(4)
    if kind == 0:
        ca, cl = rng.randrange(100, 900, 10), rng.randrange(50, 500, 10)
        return (f"Current assets ₹{ca}k, current liabilities ₹{cl}k. What is the current ratio?", f"{fmt(ca / cl)} : 1",
                [f"{fmt(cl / ca)} : 1", f"{fmt((ca - cl) / cl)} : 1", f"{fmt(ca / cl * 2)} : 1", f"{fmt(ca / (ca + cl))} : 1"],
                f"Current ratio = CA / CL = {fmt(ca / cl)} : 1 (ideal about 2 : 1).")
    if kind == 1:
        ca, inv, cl = rng.randrange(300, 900, 10), rng.randrange(50, 250, 10), rng.randrange(100, 400, 10)
        q = (ca - inv) / cl
        return (f"Current assets ₹{ca}k include inventory of ₹{inv}k; current liabilities are ₹{cl}k. What is the quick ratio?", f"{fmt(q)} : 1",
                [f"{fmt(ca / cl)} : 1", f"{fmt((ca + inv) / cl)} : 1", f"{fmt(inv / cl)} : 1", f"{fmt(q * 2)} : 1"], f"Quick ratio = (CA - inventory)/CL = {fmt(q)} : 1.")
    if kind == 2:
        sales, cogs = rng.randrange(500, 3000, 50), None
        gp = rng.choice([10, 15, 20, 25, 30, 40])
        cogs = sales * (100 - gp) / 100
        return (f"Net sales are ₹{sales}k and cost of goods sold is ₹{fmt(cogs)}k. What is the gross profit ratio?", f"{gp}%",
                [f"{100 - gp}%", f"{fmt(gp * 1.5)}%", f"{fmt(sales / cogs * 10)}%", f"{gp // 2}%"], f"GP ratio = (sales - COGS)/sales x 100 = {gp}%.")
    np_, ce = rng.randrange(50, 500, 10), rng.randrange(500, 3000, 100)
    roi = np_ / ce * 100
    return (f"Profit before interest and tax is ₹{np_}k on capital employed of ₹{ce}k. What is the return on investment?", f"{fmt(roi)}%",
            [f"{fmt(ce / np_)}%", f"{fmt(roi * 2)}%", f"{fmt(roi / 2)}%", f"{fmt(np_ / (ce + np_) * 100)}%"], f"ROI = PBIT / capital employed x 100 = {fmt(roi)}%.")


@template(LEVELS, C, N)
def partnership(rng, level):
    kind = rng.randrange(2)
    if kind == 0:
        a, b = rng.randrange(1, 6), rng.randrange(1, 6)
        P = (a + b) * rng.randrange(5, 50) * 1000
        return (f"A and B share profits in the ratio {a} : {b}. The profit is ₹{P:,}. What is A's share?", f"₹{P * a // (a + b):,}",
                [f"₹{P * b // (a + b):,}" if a != b else f"₹{P:,}", f"₹{P // 2:,}" if a != b else f"₹{P // 3:,}", f"₹{P * a // b:,}" if a != b else f"₹{P // 4:,}", f"₹{P * a // (a + b) + 1000:,}"],
                f"A gets {a}/{a + b} of ₹{P:,}.")
    cap, r = rng.randrange(1, 20) * 50000, rng.choice([5, 6, 8, 10, 12])
    return (f"A partner's capital is ₹{cap:,} and interest on capital is allowed at {r}% p.a. What is the interest for a full year?",
            f"₹{cap * r // 100:,}", [f"₹{cap * r // 1000:,}", f"₹{cap * r // 50:,}", f"₹{cap * r // 200:,}", f"₹{cap * (r + 1) // 100:,}"],
            f"{cap:,} x {r}/100 = ₹{cap * r // 100:,}.")


@template(LEVELS, C, 20)
def goodwill(rng, level):
    profits = [rng.randrange(20, 120) * 1000 for _ in range(3)]
    yrs = rng.choice([2, 3, 4])
    avg = sum(profits) / 3
    gw = avg * yrs
    return (f"Profits for 3 years were ₹{profits[0]:,}, ₹{profits[1]:,} and ₹{profits[2]:,}. Goodwill is {yrs} years' purchase of average profit. Goodwill?",
            f"₹{fmt(gw)}", [f"₹{fmt(sum(profits) * yrs)}", f"₹{fmt(avg)}", f"₹{fmt(avg * (yrs + 1))}", f"₹{fmt(sum(profits))}"],
            f"Average profit = ₹{fmt(avg)}; goodwill = {fmt(avg)} x {yrs} = ₹{fmt(gw)}.")


facts((11, 12, 15, 13, 14, 16), C, [
    ("The golden rule for a real account is:", "Debit what comes in, credit what goes out", ["Debit the receiver, credit the giver",
     "Debit expenses, credit incomes", "Debit all, credit none"], "Personal: receiver/giver; nominal: expenses/incomes."),
    ("A trial balance checks the:", "Arithmetical accuracy of ledger postings", ["Profit of the firm", "Cash in hand", "Tax payable"],
     "Total debits must equal total credits."),
    ("Depreciation is a:", "Non-cash expense", ["Cash income", "Liability", "Capital receipt"], "It spreads an asset's cost over its life."),
    ("Which is a current liability?", "Bills payable", ["Machinery", "Goodwill", "Debentures due in 10 years"], "Due within one year."),
    ("Under the Partnership Act 1932, without an agreement, profits are shared:", "Equally", ["In capital ratio", "By age",
     "Not at all"], "And no interest on capital is allowed."),
    ("Shares issued above face value are issued at a:", "Premium", ["Discount", "Par", "Loss"], "The extra goes to the Securities Premium account."),
    ("Debenture holders are the company's:", "Creditors", ["Owners", "Employees", "Customers"], "They earn fixed interest, not dividends."),
    ("Management by objectives (MBO) was popularised by:", "Peter Drucker", ["Henri Fayol", "F. W. Taylor", "Adam Smith"],
     "Goals set jointly by managers and staff."),
    ("Fayol's 'unity of command' means:", "An employee gets orders from one boss only", ["One plan for the whole firm",
     "All share profits", "Managers work alone"], "Two bosses cause confusion."),
    ("SEBI was set up to:", "Regulate the securities market and protect investors", ["Collect income tax", "Print currency",
     "Fix railway fares"], "Securities and Exchange Board of India, statutory since 1992."),
    ("The 4 Ps of marketing are Product, Price, Place and:", "Promotion", ["Profit", "People only", "Planning"], "The marketing mix."),
    ("Working capital equals:", "Current assets - current liabilities", ["Fixed assets - loans", "Capital + reserves",
     "Sales - purchases"], "It funds day-to-day operations."),
])

# ---------- Expert Engineer: everything together ----------
facts((16,), "engineering", [
    ("A bridge project has NPV > 0 at the cost of capital but its IRR is below the bank rate. The bank rate is:", "Higher than the cost of capital used",
     ["Lower than the cost of capital", "Irrelevant", "Equal to the IRR"], "NPV > 0 means IRR > the discount rate used; a higher bank rate changes the decision."),
    ("Doubling a cable's cross-section area changes its tensile capacity by:", "x 2", ["x 4", "x √2", "No change"], "Capacity = strength x area."),
    ("Doubling the depth of a rectangular beam multiplies its bending stiffness EI by:", "8", ["2", "4", "16"], "I = bd³/12."),
    ("Halving a column's effective length multiplies its Euler load by:", "4", ["2", "0.5", "8"], "P_cr ∝ 1/L²."),
    ("Concrete is weak in:", "Tension", ["Compression", "Weight", "Durability"], "Steel reinforcement carries the tension."),
    ("Chloride attack on reinforced concrete mainly causes:", "Corrosion of the steel bars", ["Freezing", "Shrinkage of cement only",
     "Higher strength"], "Corrosion products expand and crack the cover."),
    ("Galvanising protects steel by:", "A sacrificial zinc coating", ["Making it heavier", "Adding carbon", "Painting it red"],
     "Zinc is more reactive (lower E°) and corrodes first."),
    ("A finite element model splits a structure into elements and solves:", "[K]{u} = {F}", ["E = mc²", "PV = nRT", "V = IR only"],
     "The same stiffness method as the BridgeWorks truss solver."),
    ("Monte Carlo simulation estimates risk by:", "Running many random trials", ["One exact formula", "Ignoring uncertainty",
     "Using only the worst case"], "The spread of outcomes shows the risk."),
    ("Critical path in project scheduling is the:", "Longest chain of dependent tasks", ["Shortest chain", "Cheapest task",
     "First task"], "Any delay on it delays the whole project."),
    ("Life-cycle cost of a bridge includes:", "Construction, maintenance and disposal over its life", ["Only construction",
     "Only land", "Only tolls"], "Cheap to build can be costly to keep."),
    ("Carbon footprint of a design is cut most by:", "Using less material and lower-carbon materials", ["Painting it green",
     "Building it faster only", "Using more cement"], "Cement and steel production emit most CO2."),
    ("A sensor network on a bridge (structural health monitoring) mostly tracks:", "Strain, vibration and deflection",
     ["Traffic music", "Paint colour", "Toll prices"], "Changes warn of damage early."),
    ("If inflation is 6% and a loan's nominal rate is 9%, the real rate is about:", "3%", ["15%", "9%", "1.5%"], "Real ≈ nominal - inflation."),
    ("An engineer's first duty under most professional codes is to:", "Public safety, health and welfare", ["The lowest cost", "The client's speed only",
     "Personal profit"], "Safety comes before cost and schedule."),
    ("Machine learning on sensor data can be used for:", "Predictive maintenance", ["Pouring concrete", "Replacing all inspections by law",
     "Making steel stronger"], "Models flag unusual vibration before failure."),
])
