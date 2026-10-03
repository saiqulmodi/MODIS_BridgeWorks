"""Textbook checks for the physics modules (Prompts 2-8)."""
import math

import pytest

from engine import economy
from engine.beams import BeamSolver, bending_stress, rect_I, rect_Q_max, shear_stress
from engine.cantilever import CantileverBridge
from engine.dynamics import (TMD, Oscillator, critical_wind_speed, den_hartog_optimum,
                             ground_acceleration, natural_frequency, spectral_coefficient,
                             vortex_frequency)
from engine.failure import CAUSES, FailureReport
from engine.materials import STEEL, STEEL_CABLE
from engine.signals import (GREEN, RED, YELLOW, DOUBLE_YELLOW, LogicRow, aspect_for,
                            evaluate_logic, min_block_length)
from engine.traffic import (critical_density, ctm_step, greenshields_flow, greenshields_speed,
                            idm_accel, IDMParams, max_flow, shockwave_speed)
from engine.truss import Member, Node, TrussSolver, UnstableStructure
from engine.vehicles import (G, TrackPath, VehicleEngine, VehicleSpec, braking_distance,
                             max_climbable_grade, tractive_effort)

REL = 1e-6


# --- cables (tension-only members) ---------------------------------------------------------
def test_hanging_load_on_two_cables():
    P = 10e3
    nodes = [Node.pinned(-1, 1), Node.pinned(1, 1), Node(0, 0, fy=-P)]
    cab = [Member(0, 2, STEEL_CABLE, 1e-4, 1e-12), Member(1, 2, STEEL_CABLE, 1e-4, 1e-12)]
    res = TrussSolver(nodes, cab).solve()
    # each cable at 45 deg carries P / (2 sin 45)
    for m in res.members:
        assert m.N == pytest.approx(P / (2 * math.sin(math.radians(45))), rel=1e-6)


def test_cable_cannot_push():
    nodes = [Node.pinned(-1, 1), Node.pinned(1, 1), Node(0, 0, fy=+10e3)]
    cab = [Member(0, 2, STEEL_CABLE, 1e-4, 1e-12), Member(1, 2, STEEL_CABLE, 1e-4, 1e-12)]
    with pytest.raises(UnstableStructure):
        TrussSolver(nodes, cab).solve()


def test_x_braced_square_uses_only_the_tight_cable():
    P = 5e3
    nodes = [Node.pinned(0, 0), Node.pinned(1, 0), Node(1, 1, fx=P), Node(0, 1)]
    beams = [Member(0, 3, STEEL, 1e-3, 1e-6), Member(1, 2, STEEL, 1e-3, 1e-6), Member(2, 3, STEEL, 1e-3, 1e-6)]
    cables = [Member(0, 2, STEEL_CABLE, 1e-4, 1e-12), Member(1, 3, STEEL_CABLE, 1e-4, 1e-12)]
    res = TrussSolver(nodes, beams + cables).solve()
    tight, slack = res.members[3], res.members[4]
    assert slack.slack and slack.N == 0
    assert tight.N > 0


# --- vehicles (Prompt 2) ---------------------------------------------------------------------
def test_incline_force_components():
    th = math.radians(10)
    path = TrackPath([(0, 0), (100 * math.cos(th), 100 * math.sin(th))])
    spec = VehicleSpec("t", mass=1000, power=0, driven_mass=1000, length=1, axles=1, C_rr=0, C_d=0)
    v = VehicleEngine(spec, path, s=50, v=0, throttle=0)
    f = v.compute_forces()
    assert f.normal == pytest.approx(1000 * G * math.cos(th), rel=REL)
    # stands still on the slope only if friction can hold; here C_rr = 0 so it slides back
    v.step(0.1)
    assert v.v < 0


def test_tractive_effort_is_min_of_power_and_grip():
    assert tractive_effort(1e6, 10.0, 0.3, 1e6) == pytest.approx(1e5)       # P/v = 100 kN < 300 kN
    assert tractive_effort(1e6, 1.0, 0.3, 1e6) == pytest.approx(3e5)        # grip-limited


def test_braking_distance_formula():
    assert braking_distance(20, 0.3) == pytest.approx(400 / (2 * 0.3 * G))
    th = math.radians(3)
    assert braking_distance(20, 0.3, th) == pytest.approx(
        400 / (2 * (0.3 * G * math.cos(th) - G * math.sin(th))))
    assert braking_distance(20, 0.05, math.radians(10)) == math.inf


def test_max_climbable_grade():
    spec = VehicleSpec("t", mass=200e3, power=1e6, driven_mass=50e3, length=10, C_rr=0.002, mu_dry=0.3)
    assert math.tan(max_climbable_grade(spec)) == pytest.approx(0.3 * 50 / 200 - 0.002)


def test_energy_is_conserved_on_a_frictionless_slope():
    path = TrackPath([(0, 0), (1000, 50)])
    spec = VehicleSpec("t", mass=1e4, power=2e5, driven_mass=1e4, length=1, axles=1, C_rr=0, C_d=0,
                       mu_dry=1.0, max_speed=1e9)
    v = VehicleEngine(spec, path, s=1, v=5)
    ke0 = v.kinetic_energy
    for _ in range(2000):
        v.step(0.01)
    assert v.engine_work == pytest.approx(v.kinetic_energy - ke0 + v.potential_energy, rel=2e-3)


def test_weak_engine_stalls_and_rolls_back():
    path = TrackPath([(0, 0), (100, 0), (300, 40)])
    spec = VehicleSpec("t", mass=300e3, power=200e3, driven_mass=30e3, length=10, C_rr=0.002)
    v = VehicleEngine(spec, path, s=100, v=3)
    for _ in range(3000):
        v.step(0.02)
    assert v.runaway or v.stalled


# --- beams (Prompt 3) --------------------------------------------------------------------------
def test_simply_supported_uniform_load():
    L, w, EI, n = 10.0, 5e3, 2e7, 20
    xs = [L * i / n for i in range(n + 1)]
    res = BeamSolver(xs, [EI] * n, {0: "pin", n: "pin"}).solve(w=w)
    assert max(res.M) == pytest.approx(w * L * L / 8, rel=1e-3)
    assert min(res.deflection) == pytest.approx(-5 * w * L ** 4 / (384 * EI), rel=1e-3)
    assert res.reactions[0][0] == pytest.approx(w * L / 2, rel=1e-6)


def test_cantilever_point_load():
    L, P, EI, n = 4.0, 10e3, 1e7, 8
    xs = [L * i / n for i in range(n + 1)]
    res = BeamSolver(xs, [EI] * n, {0: "fixed"}).solve(point_loads={n: P})
    assert min(res.M) == pytest.approx(-P * L, rel=1e-6)                 # hogging at the wall
    assert res.deflection[-1] == pytest.approx(-P * L ** 3 / (3 * EI), rel=1e-6)


def test_two_span_continuous_beam():
    L, w, EI, n = 8.0, 2e3, 1e7, 16
    xs = [2 * L * i / (2 * n) for i in range(2 * n + 1)]
    res = BeamSolver(xs, [EI] * (2 * n), {0: "pin", n: "pin", 2 * n: "pin"}).solve(w=w)
    mid = list(res.x).index(L)
    assert res.M[mid] == pytest.approx(-w * L * L / 8, rel=1e-3)        # hogging over the middle
    assert res.reactions[n][0] == pytest.approx(1.25 * w * L, rel=1e-3)


def test_section_formulas():
    b, d = 0.3, 0.6
    assert rect_I(b, d) == pytest.approx(b * d ** 3 / 12)
    I = rect_I(b, d)
    assert bending_stress(1e5, I, d / 2) == pytest.approx(1e5 * 0.3 / I)
    assert shear_stress(1e5, rect_Q_max(b, d), I, b) == pytest.approx(1.5 * 1e5 / (b * d))


def test_cantilever_overturning_and_tie_downs():
    b = CantileverBridge()
    for _ in range(4):
        chk = b.add_segment(0, -1)          # four segments on one side only
    assert not chk.ok and chk.failure == "overturn"
    b2 = CantileverBridge()
    b2.tie_downs[0] = 2
    for _ in range(4):
        chk = b2.add_segment(0, -1)
    assert chk.ok


# --- signals (Prompt 4) -----------------------------------------------------------------------
def test_three_and_four_aspect_sequences():
    assert aspect_for(True, None) == RED
    assert aspect_for(False, RED) == YELLOW
    assert aspect_for(False, YELLOW) == GREEN
    assert aspect_for(False, YELLOW, four_aspect=True) == DOUBLE_YELLOW
    assert aspect_for(False, GREEN, permitted=False) == RED


def test_four_aspect_halves_block_length():
    assert min_block_length(25, 0.09, True) == pytest.approx(min_block_length(25, 0.09, False) / 2)


def test_logic_rows_lock_each_other_out():
    rows = [LogicRow("PERMIT_EB", ["APPR_EB", "BRIDGE_OCC", "PERMIT_WB"], [False, True, True]),
            LogicRow("PERMIT_WB", ["APPR_WB", "BRIDGE_OCC", "PERMIT_EB"], [False, True, True])]
    out = evaluate_logic(rows, {"APPR_EB": True, "APPR_WB": True, "BRIDGE_OCC": False, "PERMIT_WB": False})
    assert out == {"PERMIT_EB": True, "PERMIT_WB": False}


# --- traffic (Prompt 5) -----------------------------------------------------------------------
def test_greenshields():
    assert critical_density(140) == 70
    assert max_flow(50, 140) == pytest.approx(greenshields_flow(70, 50, 140))
    assert greenshields_speed(140, 50, 140) == 0
    assert shockwave_speed(1000, 20, 0, 140) == pytest.approx(-1000 / 120)


def test_ctm_conserves_vehicles_and_jams_spread_backwards():
    k = [0.02] * 20
    total0 = sum(k) * 10
    inflow_total = outflow_total = 0.0
    for _ in range(200):
        k, fin, fout = ctm_step(k, 10.0, 0.5, 14.0, 0.14, inflow=0.3, out_capacity=0.1)
        inflow_total += fin * 0.5
        outflow_total += fout * 0.5
    assert sum(k) * 10 == pytest.approx(total0 + inflow_total - outflow_total, rel=1e-6)
    assert k[-1] > 0.07 and k[10] > 0.07          # the jam grew backwards from the exit


def test_idm_free_road_and_braking():
    p = IDMParams()
    assert idm_accel(0, math.inf, 0, p) == pytest.approx(p.a_max)
    assert idm_accel(10, 5, 5, p) < -p.b               # closing fast on a near car -> hard braking


# --- dynamics (Prompt 7) ----------------------------------------------------------------------
def test_frequency_formulas():
    assert natural_frequency(4 * math.pi ** 2, 1) == pytest.approx(1.0)
    assert vortex_frequency(10, 1.2) == pytest.approx(1.0)
    assert critical_wind_speed(1.0, 1.2) == pytest.approx(10.0)


def test_resonance_peak_and_tmd_reduction():
    def peak(f_drive, tmd=None):
        o = Oscillator(m=1000.0, k=1000.0 * (2 * math.pi) ** 2, zeta=0.01, tmd=tmd)
        for i in range(6000):
            t = i * 0.01
            o.step(100 * math.sin(2 * math.pi * f_drive * t), 0.01)
        return o.peak
    at_res = peak(1.0)
    off_res = peak(1.6)
    assert at_res > 10 * off_res
    tune, zeta = den_hartog_optimum(0.03)
    assert peak(1.0, TMD(0.03, tune, zeta)) < 0.3 * at_res


def test_seismic_helpers():
    assert ground_acceleration(0, 3, 1.5, 0.3) == 0
    assert abs(ground_acceleration(10, 3, 1.5, 0.3)) < 3 * math.exp(-3) + 1e-9
    assert spectral_coefficient(0.3) == 2.5
    assert spectral_coefficient(2.5) == pytest.approx(0.5)


# --- economy (Prompt 8) -----------------------------------------------------------------------
def test_fs_grades_and_stars():
    assert economy.fs_grade(0.9)[0] == "FAILED"
    assert economy.fs_grade(1.7)[0] == "OPTIMAL"
    assert economy.fs_grade(5)[0] == "OVER-ENGINEERED"
    assert economy.star_rating(True, 90, 100, 200, fs=1.8) == 3
    assert economy.star_rating(True, 150, 100, 200, fs=6) == 1
    assert economy.star_rating(True, 250, 100, 200) == 0


def test_toll_formula_and_pareto():
    assert economy.toll(10, 5, 2, 25, scale=1) == pytest.approx(1.0)
    pts = [dict(safety=90, cost=10, time=5), dict(safety=95, cost=12, time=5),
           dict(safety=80, cost=15, time=6)]
    assert economy.pareto_front(pts) == [0, 1]


def test_rupee_format():
    assert economy.format_rs(250000) == "Rs 2.50 L"
    assert economy.format_rs(1.2e7) == "Rs 1.20 Cr"


# --- failure (Prompt 6) -----------------------------------------------------------------------
def test_diagnosis_rewards_first_correct_answer_once():
    r = FailureReport("buckling", "BUCKLED", "P > P_cr")
    opts = r.diagnosis_options()
    assert r.correct_cause in opts and len(set(opts)) == 3
    assert r.diagnose(r.correct_cause) == 50
    assert r.diagnose(r.correct_cause) == 0
    wrong = FailureReport("yield", "X", "y")
    bad = next(o for o in wrong.diagnosis_options() if o != wrong.correct_cause)
    assert wrong.diagnose(bad) == 0
    assert wrong.diagnose(wrong.correct_cause) == 0      # bonus only on the first try
    assert all(len(v) == 2 for v in CAUSES.values())
