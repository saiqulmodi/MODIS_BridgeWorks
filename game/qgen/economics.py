"""Economics: money basics (Class 1-8), NCERT Economics (Class 9-12), engineering economics and finance (BE+)."""
from . import facts, fmt, near, template

S = "economics"

facts(range(1, 4), S, [
    ("Things we must have to live, like food and water, are called:", "Needs", ["Wants", "Toys", "Gifts"],
     "Needs keep us alive and safe: food, water, clothes, a home."),
    ("A toy car is a:", "Want", ["Need", "Tax", "Bank"], "Wants are nice to have but we can live without them."),
    ("We keep money safely in a:", "Bank or piggy bank", ["Dustbin", "River", "Shoe"], "Banks keep money safe and even pay interest."),
    ("The person who sells things in a shop is the:", "Seller (shopkeeper)", ["Buyer", "Doctor", "Pilot"],
     "The shopkeeper sells; the customer buys."),
    ("Money we keep aside for later is called:", "Savings", ["Spending", "Borrowing", "Price"], "Saving means not spending all money now."),
    ("Indian money is called the:", "Rupee", ["Dollar", "Pound", "Yen"], "India's currency is the Indian Rupee (₹)."),
    ("A farmer who grows rice and sells it is a:", "Producer", ["Consumer", "Banker", "Teacher"],
     "Producers make or grow goods; consumers use them."),
    ("When we buy and use things, we are:", "Consumers", ["Producers", "Sellers", "Bankers"], "A consumer buys goods and services to use."),
    ("Going to a doctor is buying a:", "Service", ["Good", "Tax", "Saving"], "Services are work done for us; goods are things we can touch."),
    ("Before money, people exchanged goods for goods. This is called:", "Barter", ["Banking", "Saving", "Tax"],
     "Barter: e.g. rice for cloth, with no money."),
    ("Which of these is a good, not a service?", "A pencil", ["A haircut", "Teaching", "A bus ride"],
     "A pencil is a thing; the others are work done for us."),
    ("If we spend less than we earn, we can:", "Save money", ["Get into debt", "Lose all money", "Never buy anything"],
     "Income minus spending = saving."),
])

facts(range(4, 9), S, [
    ("The money paid to workers for their work is called:", "Wages / salary", ["Rent", "Interest", "Profit"],
     "Labour earns wages; land earns rent; capital earns interest."),
    ("Selling price more than cost price gives a:", "Profit", ["Loss", "Discount", "Tax"], "Profit = SP - CP when SP > CP."),
    ("Money charged by a bank on a loan is called:", "Interest", ["Principal", "Discount", "Wage"],
     "The borrower pays interest on the principal."),
    ("The money the government collects from people and businesses is:", "Tax", ["Salary", "Loan", "Profit"],
     "Taxes pay for roads, schools, hospitals and defence."),
    ("GST in India stands for:", "Goods and Services Tax", ["General Sales Tax", "Government Savings Tax",
     "Goods Supply Total"], "GST is one tax on most goods and services since 2017."),
    ("A market where farmers sell vegetables every week is a:", "Weekly market (haat)", ["Stock market",
     "Shopping mall", "Online shop"], "Weekly markets sell cheaply as they have no shop rent."),
    ("When many people want a thing but there is little of it, its price usually:", "Rises", ["Falls",
     "Stays zero", "Disappears"], "High demand and low supply push prices up."),
    ("A family's plan of income and spending is called a:", "Budget", ["Bill", "Receipt", "Invoice"],
     "A budget plans how to spend and save."),
    ("Factories, machines and tools used to make goods are called:", "Capital", ["Labour", "Land", "Rent"],
     "Physical capital helps produce more goods."),
    ("A Self-Help Group (SHG) mainly helps:", "Poor women save and get small loans", ["Big companies list shares",
     "Banks print money", "Government collect tax"], "SHGs pool savings and lend to members."),
    ("The central bank of India is the:", "Reserve Bank of India", ["State Bank of India", "World Bank",
     "Punjab National Bank"], "RBI issues currency and controls credit."),
    ("Money kept in a bank that can be taken out any time is in a:", "Savings / current account (demand deposit)",
     ["Fixed deposit only", "Locker", "Tax account"], "Demand deposits can be withdrawn on demand."),
    ("A person who starts a business and takes its risk is an:", "Entrepreneur", ["Employee", "Consumer", "Landlord"],
     "Entrepreneurs organise land, labour and capital."),
    ("When prices of most things keep rising over time, it is called:", "Inflation", ["Deflation", "Saving", "Barter"],
     "Inflation reduces what each rupee can buy."),
])

facts(range(9, 11), S, [
    ("In the story of Palampur village, the main production activity is:", "Farming", ["Mining", "Fishing", "IT services"],
     "Palampur (NCERT Class 9) shows farming as the main activity, with small non-farm work."),
    ("The four factors of production are land, labour, physical capital and:", "Human capital (enterprise)",
     ["Money only", "Taxes", "Rainfall"], "Knowledge and enterprise put the other factors together."),
    ("Growing more than one crop on the same land in a year is called:", "Multiple cropping", ["Mixed farming",
     "Shifting cultivation", "Monoculture"], "It is the most common way to raise farm output."),
    ("Investment in education and health that makes people more productive is:", "Human capital formation",
     ["Physical capital", "Disguised unemployment", "Barter"], "Educated, healthy people are a resource (Class 9, People as Resource)."),
    ("More people working on a farm than needed, so some add nothing to output, is:", "Disguised unemployment",
     ["Seasonal unemployment", "Frictional unemployment", "Full employment"], "Their marginal product is zero."),
    ("The Public Distribution System (PDS) supplies food through:", "Ration (fair price) shops",
     ["Stock markets", "Hotels", "Export houses"], "Food Corporation of India buys grain; PDS sells it cheaply."),
    ("Buffer stock of food grains is kept by the:", "Food Corporation of India", ["RBI", "SEBI", "NABARD only"],
     "FCI buys at the minimum support price and stores grain."),
    ("Average income (total income / population) is also called:", "Per capita income", ["National debt",
     "Gross margin", "Fiscal deficit"], "The World Bank uses per capita income to rank countries."),
    ("The Human Development Index (HDI) combines income with:", "Health and education", ["Only military power",
     "Only exports", "Only population"], "UNDP's HDI uses life expectancy, schooling and income."),
    ("The primary sector includes:", "Agriculture, fishing and mining", ["Banking and transport",
     "Factories only", "Software"], "Primary: natural products; secondary: manufacturing; tertiary: services."),
    ("Banks and transport belong to the:", "Tertiary sector", ["Primary sector", "Secondary sector",
     "Quaternary only"], "They are services that support the other sectors."),
    ("MGNREGA 2005 guarantees rural households:", "100 days of paid work a year", ["Free land", "A government job",
     "Free electricity only"], "It is a right-to-work law for unskilled manual work."),
    ("Something a borrower pledges until a loan is repaid is called:", "Collateral", ["Interest", "Principal", "Dividend"],
     "Land, gold or a building are common collateral (Money and Credit)."),
    ("Formal sources of credit include:", "Banks and cooperatives", ["Moneylenders", "Traders", "Relatives"],
     "Formal lenders are supervised by the RBI; informal ones are not."),
    ("Removing barriers on foreign trade and investment is called:", "Liberalisation", ["Nationalisation",
     "Protectionism", "Barter"], "India's 1991 reforms liberalised trade and investment."),
    ("A company that owns or controls production in more than one country is an:", "MNC", ["SHG", "PSU", "NGO"],
     "Multinational corporations spread production across countries."),
    ("The 'right to seek redressal' lets a consumer:", "Get compensation for unfair trade", ["Avoid taxes",
     "Get free goods", "Fix prices"], "Consumer courts (Consumer Protection Act) handle complaints."),
    ("The ISI and Agmark logos tell consumers about:", "Quality standards", ["Price", "Tax", "Country of origin only"],
     "Certified products meet set quality standards."),
])

facts(range(11, 13), S, [
    ("Statistics for Economics: the most frequent value in data is the:", "Mode", ["Mean", "Median", "Range"],
     "Mode = most common; median = middle; mean = average."),
    ("A measure of central tendency NOT affected by extreme values is the:", "Median", ["Mean", "Range", "Sum"],
     "The median depends only on the middle position."),
    ("India's planning era started its First Five-Year Plan in:", "1951", ["1947", "1961", "1991"],
     "Plans ran 1951-2017; NITI Aayog replaced the Planning Commission in 2015."),
    ("The Green Revolution mainly raised the output of:", "Wheat and rice", ["Cotton and jute", "Tea and coffee", "Fish"],
     "High-yielding seeds, fertiliser and irrigation from the mid-1960s."),
    ("LPG reforms of 1991 stand for Liberalisation, Privatisation and:", "Globalisation", ["Growth", "Gold", "Licensing"],
     "The New Economic Policy of 1991."),
    ("Microeconomics studies:", "Individual markets, consumers and firms", ["The whole economy only",
     "Only government budgets", "Only international trade"], "Macroeconomics studies aggregates like GDP and inflation."),
    ("The law of demand says, other things equal, when price rises quantity demanded:", "Falls", ["Rises",
     "Stays the same", "Becomes zero"], "Demand curves slope downward."),
    ("A good whose demand rises when income rises is a:", "Normal good", ["Inferior good", "Giffen good", "Free good"],
     "Inferior goods' demand falls as income rises."),
    ("Goods used together, like car and petrol, are:", "Complements", ["Substitutes", "Inferior goods", "Giffen goods"],
     "If petrol gets costlier, demand for cars falls."),
    ("Under perfect competition, a firm is a:", "Price taker", ["Price maker", "Monopolist", "Cartel"],
     "Many sellers of an identical product: no single firm can set the price."),
    ("Marginal cost is the change in total cost when output rises by:", "One unit", ["Ten units", "Its maximum",
     "Zero"], "MC = change in TC / change in Q."),
    ("GDP measures the value of final goods and services produced:", "Within a country's borders in a year",
     ["By citizens anywhere", "Including intermediate goods", "Only by the government"], "GNP adds net factor income from abroad."),
    ("The Reserve Bank's main tool to control credit by changing the rate it lends to banks is the:", "Repo rate",
     ["GST rate", "Income tax", "Exchange rate"], "Higher repo rate -> costlier loans -> less spending."),
    ("A fiscal deficit means the government's:", "Total spending exceeds receipts (other than borrowing)",
     ["Exports exceed imports", "Bank has extra cash", "Taxes exceed spending"], "It is met by borrowing."),
    ("Under a flexible exchange rate, the rupee's value is set by:", "Demand and supply of foreign exchange",
     ["RBI alone every day", "The World Bank", "Gold weight"], "The RBI may step in only to smooth swings."),
    ("The balance of payments has two main accounts: current account and:", "Capital account", ["Savings account",
     "Fiscal account", "Revenue account"], "Current: trade and transfers; capital: investment and loans."),
])

facts((15, 13, 14, 16), S, [
    ("Net present value (NPV) of a project is positive when:", "Discounted inflows exceed the investment",
     ["The payback is under a year", "Inflation is zero", "Interest rate is zero"], "Accept projects with NPV > 0."),
    ("The internal rate of return (IRR) is the discount rate at which:", "NPV = 0", ["NPV is maximum",
     "Payback = 1 year", "Profit = revenue"], "Accept if IRR > cost of capital."),
    ("Straight-line depreciation charges each year:", "(Cost - salvage) / life", ["Cost x rate on book value",
     "Salvage / life", "Cost / salvage"], "The same amount every year."),
    ("Opportunity cost is:", "The value of the next best alternative given up", ["The money price paid",
     "A sunk cost", "A tax"], "Choosing one option means giving up the best other one."),
    ("A cost already incurred that cannot be recovered is a:", "Sunk cost", ["Marginal cost", "Variable cost",
     "Opportunity cost"], "Sunk costs should not affect future decisions."),
    ("Break-even point is where:", "Total revenue = total cost", ["Profit is maximum", "Price = 0",
     "Fixed cost = 0"], "Q_BE = Fixed cost / (price - variable cost per unit)."),
    ("Real interest rate is approximately:", "Nominal rate - inflation rate", ["Nominal + inflation",
     "Nominal x inflation", "Inflation - nominal"], "Fisher relation: (1 + r)(1 + pi) = 1 + i."),
    ("WACC is used as the:", "Discount rate for a firm's projects", ["Tax rate", "Depreciation rate", "Inflation index"],
     "Weighted average cost of capital blends debt and equity costs."),
    ("Price elasticity of demand above 1 (in size) means demand is:", "Elastic", ["Inelastic", "Unit elastic",
     "Perfectly inelastic"], "Quantity changes more than price in percentage terms."),
    ("In a monopoly, profit is maximised where:", "MR = MC", ["P = MC", "AR = AC", "TR is maximum"],
     "Every firm maximises profit where marginal revenue equals marginal cost."),
    ("The Phillips curve shows a short-run trade-off between:", "Inflation and unemployment",
     ["GDP and exports", "Savings and taxes", "Interest and wages"], "Lower unemployment tends to come with higher inflation (short run)."),
    ("Crowding out happens when government borrowing:", "Raises interest rates and lowers private investment",
     ["Lowers all prices", "Raises exports", "Cuts taxes"], "Public demand for loans competes with firms."),
])

# ---------- calculated ----------

@template(range(1, 5), S, 25)
def shop_total(rng, level):
    p = rng.randrange(2, 6 + level * 5)
    n = rng.randrange(2, 3 + level * 2)
    return (f"One pencil costs ₹{p}. How much do {n} pencils cost?", f"₹{p * n}",
            [f"₹{p + n}", f"₹{p * n + p}", f"₹{p * (n - 1)}", f"₹{p * n * 2}"], f"₹{p} x {n} = ₹{p * n}.")


@template(range(1, 6), S, 25)
def change_back(rng, level):
    note = rng.choice([10, 20, 50] if level <= 2 else [50, 100, 200, 500])
    cost = rng.randrange(1, note)
    return (f"You pay with a ₹{note} note for a toy costing ₹{cost}. How much change do you get?", f"₹{note - cost}",
            [f"₹{note + cost}", f"₹{note - cost + 1}", f"₹{cost}", f"₹{note - cost - 1}"], f"₹{note} - ₹{cost} = ₹{note - cost}.")


@template(range(3, 9), S, 20)
def saving_months(rng, level):
    s = rng.randrange(5, 20 + level * 10)
    m = rng.randrange(3, 13)
    return (f"Arjun saves ₹{s} every month. How much does he save in {m} months?", f"₹{s * m}",
            [f"₹{s + m}", f"₹{s * (m + 1)}", f"₹{s * m - s}", f"₹{s * 12}" if m != 12 else f"₹{s * 10}"], f"₹{s} x {m} = ₹{s * m}.")


@template(range(5, 11), S, 20)
def profit_loss(rng, level):
    cp = rng.randrange(40, 200 + level * 100, 10)
    pct = rng.choice([5, 10, 12, 15, 20, 25, 30])
    gain = rng.random() < 0.6
    sp = cp * (100 + pct) / 100 if gain else cp * (100 - pct) / 100
    word = "profit" if gain else "loss"
    return (f"A shopkeeper buys an item for ₹{cp} and sells it for ₹{fmt(sp)}. What is the {word} per cent?",
            f"{pct}%", [f"{pct + 5}%", f"{abs(pct - 5) or 1}%", f"{fmt(abs(sp - cp))}%", f"{fmt(abs(sp - cp) / sp * 100)}%"],
            f"{word.title()} = ₹{fmt(abs(sp - cp))}; {word} % = {fmt(abs(sp - cp))} / {cp} x 100 = {pct}% (always on cost price).")


@template(range(6, 11), S, 20)
def simple_interest(rng, level):
    p = rng.randrange(1000, 20000, 500)
    r = rng.choice([4, 5, 6, 7.5, 8, 9, 10, 12])
    t = rng.randrange(2, 6)
    si = p * r * t / 100
    return (f"Find the simple interest on ₹{p:,} at {fmt(r)}% per year for {t} years.", f"₹{fmt(si)}",
            [f"₹{fmt(p * r / 100)}", f"₹{fmt(si + p)}", f"₹{fmt(si * 2)}", f"₹{fmt(p * r * (t - 1) / 100)}"],
            f"SI = P x R x T / 100 = {p:,} x {fmt(r)} x {t} / 100 = ₹{fmt(si)}.")


@template(range(9, 11), S, 20)
def per_capita(rng, level):
    pop = rng.choice([2, 4, 5, 8, 10, 20, 25, 40])
    inc = pop * rng.randrange(20, 200) * 1000
    pci = inc / pop
    return (f"A country of {pop} lakh people has a total income of ₹{inc:,} lakh. What is its per capita income?",
            f"₹{fmt(pci)}", [f"₹{fmt(pci * 10)}", f"₹{fmt(pci / 2)}", f"₹{fmt(inc)}", f"₹{fmt(pci + pop)}"],
            f"Per capita income = total income / population = {inc:,} / {pop} = ₹{fmt(pci)}.")


@template(range(9, 13), S, 20)
def literacy_rate(rng, level):
    pop = rng.randrange(500, 5000, 50)
    lit = rng.randrange(pop // 3, pop)
    rate = lit / pop * 100
    return (f"In a district, {lit:,} of {pop:,} people aged 7+ can read and write. What is the literacy rate?",
            f"{fmt(rate)}%", near(rate, rng, "%", (0.8, 1.15, 0.5, 0.9)), f"Literacy rate = {lit:,} / {pop:,} x 100 = {fmt(rate)}%.")


@template((11, 12, 13), S, 20)
def mean_median(rng, level):
    n = rng.choice([5, 7, 9])
    data = sorted(rng.sample(range(10, 99), n))
    mean = sum(data) / n
    med = data[n // 2]
    shown = data[:]
    rng.shuffle(shown)
    if rng.random() < 0.5:
        return (f"Find the median of: {', '.join(map(str, shown))}", str(med),
                [fmt(mean), str(data[n // 2 - 1]), str(data[n // 2 + 1]), str(shown[n // 2])],
                f"Sorted: {', '.join(map(str, data))}; the middle ({n // 2 + 1}th) value is {med}.")
    return (f"Find the arithmetic mean of: {', '.join(map(str, shown))}", fmt(mean),
            [str(med), fmt(sum(data) / (n - 1)), fmt(mean + 1), str(sum(data))], f"Mean = {sum(data)} / {n} = {fmt(mean)}.")


@template((11, 12, 13), S, 20)
def pct_change(rng, level):
    a = rng.randrange(100, 900, 5)
    b = a + rng.randrange(-a // 3, a // 2, 5)
    if b == a:
        b += 25
    ch = (b - a) / a * 100
    return (f"A price index rose from {a} to {b}. What is the percentage change?" if b > a else
            f"A price index changed from {a} to {b}. What is the percentage change?", f"{fmt(ch)}%",
            [f"{fmt((b - a) / b * 100)}%", f"{fmt(-ch)}%", f"{b - a}%", f"{fmt(ch * 2)}%"],
            f"% change = ({b} - {a}) / {a} x 100 = {fmt(ch)}%.")


@template((12, 13, 14, 15, 16), S, 20)
def elasticity(rng, level):
    p0 = rng.randrange(10, 60)
    q0 = rng.randrange(100, 1000, 10)
    dp = rng.choice([10, 20, 25, 50]) / 100
    e = rng.choice([0.4, 0.5, 0.8, 1, 1.5, 2, 2.5])
    q1 = q0 * (1 - e * dp)
    return (f"When price rises from ₹{p0} to ₹{fmt(p0 * (1 + dp))}, quantity demanded falls from {q0} to {fmt(q1)} units. "
            f"What is the price elasticity of demand (percentage method, in size)?", fmt(e),
            [fmt(1 / e), fmt(e * 2), fmt(e / 2), fmt(e + 1)],
            f"%dQ = {fmt(e * dp * 100)}%, %dP = {fmt(dp * 100)}%; e = {fmt(e * dp * 100)} / {fmt(dp * 100)} = {fmt(e)}.")


@template((12, 13, 14, 15, 16), S, 20)
def multiplier(rng, level):
    mpc = rng.choice([0.5, 0.6, 0.75, 0.8, 0.9])
    di = rng.choice([100, 200, 500, 1000, 2500])
    k = 1 / (1 - mpc)
    return (f"If MPC = {mpc}, by how much does national income rise when investment rises by ₹{di} crore?",
            f"₹{fmt(di * k)} crore", [f"₹{fmt(di * mpc)} crore", f"₹{fmt(di / mpc)} crore", f"₹{fmt(di)} crore",
                                      f"₹{fmt(di * (k + 1))} crore"],
            f"Multiplier k = 1 / (1 - MPC) = {fmt(k)}; dY = {fmt(k)} x {di} = ₹{fmt(di * k)} crore.")


@template((12, 13, 14), S, 20)
def national_income(rng, level):
    c, i, g, x, m = (rng.randrange(a, b, 10) for a, b in ((400, 900), (100, 300), (100, 300), (50, 200), (50, 200)))
    dep = rng.randrange(20, 90, 5)
    if rng.random() < 0.5:
        gdp = c + i + g + x - m
        return (f"C = {c}, I = {i}, G = {g}, exports = {x}, imports = {m} (₹ crore). Find GDP at market price.",
                f"₹{gdp} crore", [f"₹{c + i + g + x + m} crore", f"₹{c + i + g} crore", f"₹{gdp - dep} crore", f"₹{gdp + m} crore"],
                f"GDP = C + I + G + (X - M) = {gdp}.")
    gdp = c + i + g + x - m
    return (f"GDP at market price is ₹{gdp} crore and depreciation is ₹{dep} crore. Find NDP at market price.",
            f"₹{gdp - dep} crore", [f"₹{gdp + dep} crore", f"₹{gdp} crore", f"₹{dep} crore", f"₹{gdp - 2 * dep} crore"],
            f"NDP = GDP - depreciation = {gdp} - {dep} = {gdp - dep}.")


@template((12, 13, 14), S, 15)
def money_multiplier(rng, level):
    lrr = rng.choice([5, 8, 10, 12.5, 20, 25])
    dep = rng.choice([100, 500, 1000, 2000])
    m = 100 / lrr
    return (f"With a legal reserve ratio of {fmt(lrr)}%, how much total credit can banks create from new deposits of ₹{dep} crore?",
            f"₹{fmt(dep * m)} crore", [f"₹{fmt(dep * lrr / 100)} crore", f"₹{fmt(dep * (m - 1))} crore", f"₹{dep} crore",
                                       f"₹{fmt(dep * m * 2)} crore"],
            f"Money multiplier = 1 / LRR = {fmt(m)}; credit = {fmt(m)} x {dep} = ₹{fmt(dep * m)} crore.")


@template((15, 13, 14, 16), S, 20)
def npv(rng, level):
    inv = rng.randrange(50, 300, 10)
    cf = rng.randrange(20, 120, 5)
    n = rng.randrange(2, 6)
    r = rng.choice([0.05, 0.08, 0.1, 0.12, 0.15])
    pv = sum(cf / (1 + r) ** t for t in range(1, n + 1))
    val = pv - inv
    return (f"A project costs ₹{inv} lakh now and returns ₹{cf} lakh at the end of each of the next {n} years. "
            f"At a {r:.0%} discount rate, what is its NPV?", f"₹{fmt(val)} lakh",
            [f"₹{fmt(cf * n - inv)} lakh", f"₹{fmt(pv)} lakh", f"₹{fmt(val * (1 + r))} lakh", f"₹{fmt(-val)} lakh"],
            f"PV of inflows = sum of {cf}/(1+{r})^t for t = 1..{n} = {fmt(pv)}; NPV = {fmt(pv)} - {inv} = {fmt(val)}.")


@template((15, 16), S, 20)
def depreciation(rng, level):
    cost = rng.randrange(100, 1000, 20) * 1000
    salvage = cost * rng.choice([0, 0.05, 0.1, 0.2])
    life = rng.randrange(4, 16)
    d = (cost - salvage) / life
    return (f"A machine costs ₹{cost:,}, lasts {life} years and has a salvage value of ₹{fmt(salvage)}. "
            f"What is the yearly straight-line depreciation?", f"₹{fmt(d)}",
            [f"₹{fmt(cost / life)}", f"₹{fmt((cost + salvage) / life)}", f"₹{fmt(d * 2)}", f"₹{fmt(salvage / life)}"],
            f"D = (cost - salvage) / life = ({cost:,} - {fmt(salvage)}) / {life} = ₹{fmt(d)}.")


@template((15, 16), S, 20)
def emi(rng, level):
    p = rng.randrange(5, 100) * 100000
    annual = rng.choice([7, 8, 8.5, 9, 10, 12])
    yrs = rng.choice([5, 10, 15, 20])
    i = annual / 1200
    n = yrs * 12
    e = p * i * (1 + i) ** n / ((1 + i) ** n - 1)
    return (f"What is the monthly EMI on a loan of ₹{p:,} at {annual}% a year for {yrs} years (monthly reducing balance)?",
            f"₹{fmt(e, 4)}", [f"₹{fmt(p / n, 4)}", f"₹{fmt(p * (1 + annual / 100 * yrs) / n, 4)}", f"₹{fmt(e * 1.1, 4)}", f"₹{fmt(e * 0.9, 4)}"],
            f"EMI = P i (1+i)^n / ((1+i)^n - 1) with i = {annual}/1200, n = {n}: ₹{fmt(e, 4)}.")


@template((15, 13, 14, 16), S, 20)
def break_even(rng, level):
    fc = rng.randrange(50, 500, 10) * 1000
    p = rng.randrange(50, 300, 5)
    v = rng.randrange(10, p - 10, 5)
    q = fc / (p - v)
    return (f"Fixed costs are ₹{fc:,}, price is ₹{p} per unit and variable cost is ₹{v} per unit. Find the break-even quantity.",
            f"{fmt(q, 4)} units", [f"{fmt(fc / p, 4)} units", f"{fmt(fc / v, 4)} units", f"{fmt(fc / (p + v), 4)} units",
                                   f"{fmt(q * 2, 4)} units"], f"Q = FC / (P - V) = {fc:,} / ({p} - {v}) = {fmt(q, 4)} units.")


@template((14, 16), S, 15)
def cagr(rng, level):
    a = rng.randrange(100, 500, 10)
    yrs = rng.randrange(3, 11)
    g = rng.choice([0.04, 0.06, 0.08, 0.1, 0.12, 0.15])
    b = a * (1 + g) ** yrs
    return (f"Revenue grew from ₹{a} crore to ₹{fmt(b, 4)} crore in {yrs} years. What is the compound annual growth rate?",
            f"{g:.0%}", [f"{(b / a - 1) / yrs:.1%}", f"{g + 0.02:.0%}", f"{g - 0.02:.0%}", f"{(b / a - 1):.0%}"],
            f"CAGR = (end / start)^(1/{yrs}) - 1 = {g:.0%}; simple averaging overstates it.")
