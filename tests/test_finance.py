"""Loan and business-plan maths."""
import math

import pytest

from engine import finance as F


def test_annuity_matches_textbook():
    # 1,00,000 at 2% over 10 years -> 11,132.65 a year
    assert F.annuity_payment(100000, 0.02, 10) == pytest.approx(11132.65, abs=0.01)
    assert F.annuity_payment(0) == 0


def test_loan_is_fully_repaid_after_the_term():
    p = F.business_plan(1, 250000, 400000)
    assert p.loan == pytest.approx(150000)
    assert p.rows[F.LOAN_YEARS - 1].balance == pytest.approx(0, abs=1e-6)
    assert p.loan_repaid_year == F.LOAN_YEARS
    assert p.total_interest == pytest.approx(p.payment * F.LOAN_YEARS - p.loan)


def test_no_loan_inside_budget():
    p = F.business_plan(1, 250000, 200000)
    assert p.loan == 0 and p.payment == 0 and p.viable and math.isinf(p.coverage)
    assert p.payback_year >= 1


def test_coverage_rule_is_a_50_percent_margin():
    budget = 250000
    P = F.max_viable_loan(1, budget)
    ok = F.business_plan(1, budget, budget + P * 0.99)
    bad = F.business_plan(1, budget, budget + P * 1.05)
    assert ok.viable and ok.coverage >= 1.5
    assert not bad.viable and bad.coverage < 1.5
    assert F.business_plan(1, budget, budget + P).coverage == pytest.approx(1.5, rel=1e-6)


def test_business_grows_and_profit_jumps_after_the_loan():
    p = F.business_plan(3, 9.5e6, 12e6)
    assert p.rows[5].income > p.rows[0].income * 1.3          # 6% growth a year
    y9, y10 = p.rows[F.LOAN_YEARS - 1], p.rows[F.LOAN_YEARS]
    # payments stop -> the owner keeps the whole instalment, plus that year's traffic growth
    assert y10.net - y9.net == pytest.approx(p.payment + (y10.income - y9.income), rel=1e-6)


def test_higher_toll_earns_more_but_users_fall():
    lo = F.business_plan(1, 250000, 300000, toll_factor=1.0)
    hi = F.business_plan(1, 250000, 300000, toll_factor=1.5)
    assert hi.users_day < lo.users_day
    assert hi.income1 > lo.income1                # elasticity -0.5: revenue ~ sqrt(toll)
    assert hi.coverage > lo.coverage


def test_government_loan_is_capped_and_cheaper():
    budget = 250000
    bank = F.business_plan(1, budget, 700000)
    govt = F.business_plan(1, budget, 700000, govt=True)
    assert govt.loan == bank.loan == pytest.approx(450000)
    assert govt.govt_loan == pytest.approx(F.GOVT_CAP_SHARE * budget)     # capped at half the budget
    assert govt.bank_loan == pytest.approx(450000 - 125000)
    assert govt.payment < bank.payment                                     # cheaper per year
    assert govt.coverage > bank.coverage
    assert govt.subsidy_saving > 0
    assert govt.govt_payment == pytest.approx(F.annuity_payment(125000, 0.005, 15))


def test_government_loan_runs_15_years():
    p = F.business_plan(1, 250000, 300000, govt=True)          # small shortfall: all government
    assert p.bank_loan == 0 and p.govt_loan == pytest.approx(50000)
    assert p.loan_repaid_year == F.GOVT_YEARS
    assert p.rows[F.GOVT_YEARS - 1].balance == pytest.approx(0, abs=1e-6)


def test_subsidy_can_make_a_refused_project_viable():
    budget = 250000
    P = F.max_viable_loan(1, budget)
    cost = budget + P * 1.04      # just misses the bank's 1.5x rule
    assert not F.business_plan(1, budget, cost).viable
    assert F.business_plan(1, budget, cost, govt=True).viable


def test_every_level_has_a_toll():
    for n in range(1, 11):
        name, rate, unit = F.TOLLS[n]
        assert rate > 0 and F.first_year_income(n, 1e6) == pytest.approx(F.REVENUE_SHARE * 1e6)
