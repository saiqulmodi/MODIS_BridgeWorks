"""Bank loans and the business plan (tolls pay the project back).

    Loan instalment (equal yearly payments):   A = P r / (1 - (1 + r)^-n)
    Net operating income (year y):             NOI = toll income - upkeep
    Debt-service coverage ratio:               DSCR = NOI / A
    The bank lends only if DSCR >= 1.5 - toll income must beat the loan payment
    with a 50% margin. Traffic grows every year, so the business grows too.
    A government subsidised loan (0.5%, 15 years, up to half the budget) can take the
    first part of the shortfall; the bank lends the rest.
"""
import math
from dataclasses import dataclass, field

LOAN_RATE = 0.02           # 2% a year
LOAN_YEARS = 10
GOVT_RATE = 0.005          # government subsidised loan: 0.5% a year ...
GOVT_YEARS = 15            # ... over 15 years ...
GOVT_CAP_SHARE = 0.5       # ... for up to 50% of the level's budget
MIN_COVERAGE = 1.5         # = 50% margin over the yearly loan payment
TRAFFIC_GROWTH = 0.06      # users grow 6% a year
UPKEEP_RATE = 0.03         # yearly operation & maintenance, share of build cost
HORIZON = 20               # years shown in the business plan
TOLL_RANGE = (0.5, 1.5)    # toll can be set between half and 1.5x the standard rate
REVENUE_SHARE = 0.45       # year-1 income at the standard toll = 45% of the level budget

# What each level charges for, the standard rate, and the unit it is charged per
TOLLS = {
    1: ("Bridge toll", 10.0, "vehicle"),
    2: ("Freight charge", 150.0, "tonne"),
    3: ("Bridge toll", 60.0, "vehicle"),
    4: ("Freight charge", 120.0, "tonne"),
    5: ("Track access fee", 1500.0, "train"),
    6: ("Congestion charge", 2.0, "car"),
    7: ("Bridge toll", 40.0, "vehicle"),
    8: ("Highway toll", 50.0, "vehicle"),
    9: ("Freight margin", 25.0, "tonne"),
    10: ("Maglev fare", 200.0, "passenger"),
}


def annuity_payment(P, r=LOAN_RATE, n=LOAN_YEARS):
    """Equal yearly payment that repays P with interest r over n years."""
    if P <= 0:
        return 0.0
    if r == 0:
        return P / n
    return P * r / (1 - (1 + r) ** -n)


def users_per_day(level_num, budget, toll_factor=1.0):
    """Daily users at the standard toll are set by the level; a higher toll keeps some away:
    users = base x (1 / toll_factor)^0.5   (price elasticity -0.5)."""
    name, rate, unit = TOLLS[level_num]
    base = REVENUE_SHARE * budget / 365.0 / rate
    return base / math.sqrt(toll_factor)


def first_year_income(level_num, budget, toll_factor=1.0, efficiency=1.0):
    name, rate, unit = TOLLS[level_num]
    return users_per_day(level_num, budget, toll_factor) * rate * toll_factor * 365.0 * efficiency


@dataclass
class YearRow:
    year: int
    income: float
    upkeep: float
    payment: float
    interest: float
    balance: float          # loan still owed at the end of the year
    net: float              # cash to the owner this year
    cumulative: float       # owner's position, starting at minus their own funds spent


@dataclass
class Plan:
    build_cost: float
    own_funds: float
    loan: float
    payment: float
    income1: float
    upkeep1: float
    coverage: float         # DSCR in year 1 (inf when there is no loan)
    viable: bool
    payback_year: int       # first year the owner has recovered their own funds (0 = never)
    loan_repaid_year: int
    profit_horizon: float   # owner's cumulative cash after HORIZON years
    total_interest: float
    rows: list = field(default_factory=list)
    users_day: float = 0.0
    toll_factor: float = 1.0


def business_plan(level_num, budget, build_cost, toll_factor=1.0, efficiency=1.0,
                  rate=LOAN_RATE, years=LOAN_YEARS, horizon=HORIZON, govt=False):
    """Cash-flow plan for a project: own funds first, then loans for anything above the budget.
    govt=True: a subsidised government loan covers up to GOVT_CAP_SHARE of the budget first,
    and the bank lends the rest."""
    own = min(build_cost, budget)
    loan = max(0.0, build_cost - budget)
    govt_loan = min(loan, GOVT_CAP_SHARE * budget) if govt else 0.0
    bank_loan = loan - govt_loan
    loans = [(bank_loan, rate, years), (govt_loan, GOVT_RATE, GOVT_YEARS)]
    pays = [annuity_payment(P, r, n) for P, r, n in loans]
    A = sum(pays)                                   # total payment in year 1
    income1 = first_year_income(level_num, budget, toll_factor, efficiency)
    upkeep = UPKEEP_RATE * build_cost
    noi1 = income1 - upkeep
    coverage = math.inf if A == 0 else noi1 / A
    balances = [P for P, _, _ in loans]
    rows, cum = [], -own
    payback = repaid = 0
    total_interest = 0.0
    for y in range(1, horizon + 1):
        income = income1 * (1 + TRAFFIC_GROWTH) ** (y - 1)
        pay = interest = 0.0
        for k, (P, r, n) in enumerate(loans):
            if y <= n and balances[k] > 0:
                i = balances[k] * r
                balances[k] = max(0.0, balances[k] + i - pays[k])
                interest += i
                pay += pays[k]
        balance = sum(balances)
        total_interest += interest
        net = income - upkeep - pay
        cum += net
        if not payback and cum >= 0:
            payback = y
        if loan and not repaid and balance <= 1e-6:
            repaid = y
        rows.append(YearRow(y, income, upkeep, pay, interest, balance, net, cum))
    viable = loan == 0 or coverage >= MIN_COVERAGE
    plan = Plan(build_cost, own, loan, A, income1, upkeep, coverage, viable, payback, repaid,
                cum, total_interest, rows, users_per_day(level_num, budget, toll_factor), toll_factor)
    plan.govt_loan, plan.bank_loan = govt_loan, bank_loan
    plan.govt_payment, plan.bank_payment = pays[1], pays[0]
    # what the same money would have cost entirely from the bank
    bank_only_interest = annuity_payment(loan, rate, years) * years - loan
    plan.subsidy_saving = bank_only_interest - total_interest if govt else 0.0
    return plan


def max_viable_loan(level_num, budget, toll_factor=1.0, efficiency=1.0):
    """Largest loan the bank would approve (DSCR exactly 1.5)."""
    income1 = first_year_income(level_num, budget, toll_factor, efficiency)
    a = annuity_payment(1.0)            # payment per rupee borrowed
    # income - UPKEEP (budget + P) >= 1.5 a P
    return max(0.0, (income1 - UPKEEP_RATE * budget) / (MIN_COVERAGE * a + UPKEEP_RATE))
