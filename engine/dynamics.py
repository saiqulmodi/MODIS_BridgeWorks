"""Dynamic hazards: resonance, wind vortex shedding, tuned mass dampers, earthquakes (Prompt 7).

    natural frequency       f_n = (1 / 2 pi) sqrt(k / m)
    vortex shedding         f_v = St * U / D        (St ~ 0.12 for a bridge deck)
    resonance               when f_v ~ f_n the wind pushes in step with the swing and the
                            amplitude grows until damping (or the steel) stops it.
    seismic ground motion   a_g(t) = A_peak sin(omega t) exp(-decay t)
    base shear              V_base = C * M * a_g
"""
import math
from dataclasses import dataclass, field

G = 9.81
RHO_AIR = 1.225
STROUHAL = 0.12


def natural_frequency(k, m):
    """f_n in Hz."""
    return math.sqrt(k / m) / (2 * math.pi)


def omega_n(k, m):
    return math.sqrt(k / m)


def vortex_frequency(U, D, St=STROUHAL):
    return St * U / D


def critical_wind_speed(f_n, D, St=STROUHAL):
    """Wind speed at which vortex shedding locks onto the bridge: U = f_n D / St."""
    return f_n * D / St


def vortex_force_amplitude(U, D, span, C_L=0.6, rho=RHO_AIR):
    """Peak alternating lift on the deck: F0 = 1/2 rho U^2 D L C_L."""
    return 0.5 * rho * U * U * D * span * C_L


def den_hartog_optimum(mass_ratio):
    """Best TMD tuning for a mass ratio mu: f_tmd/f_n = 1/(1+mu), zeta = sqrt(3 mu / (8 (1+mu)^3))."""
    mu = mass_ratio
    return 1.0 / (1.0 + mu), math.sqrt(3 * mu / (8 * (1 + mu) ** 3))


def ground_acceleration(t, A_peak, f_quake, decay):
    """a_g(t) = A_peak sin(2 pi f t) e^(-decay t)   (m/s^2)."""
    if t < 0:
        return 0.0
    return A_peak * math.sin(2 * math.pi * f_quake * t) * math.exp(-decay * t)


def base_shear(C, mass, a_g):
    return C * mass * a_g


def spectral_coefficient(T):
    """Simplified design response spectrum: how strongly a structure with natural period T
    amplifies ground shaking (stiff short-period structures get the full 2.5x)."""
    if T < 0.1:
        return 1.0 + 15.0 * T
    if T <= 0.5:
        return 2.5
    return 2.5 * 0.5 / T


@dataclass
class TMD:
    mass_ratio: float = 0.02      # TMD mass / structure modal mass
    tuning: float = 1.0           # f_tmd / f_n
    zeta: float = 0.08            # TMD damping ratio


@dataclass
class Oscillator:
    """Structure (1 DOF modal model) with an optional tuned mass damper (2nd DOF)."""
    m: float                      # modal mass, kg
    k: float                      # modal stiffness, N/m
    zeta: float = 0.005           # structural damping ratio (steel bridges ~0.5%)
    tmd: TMD = None
    x: float = 0.0
    v: float = 0.0
    x2: float = 0.0
    v2: float = 0.0
    peak: float = 0.0
    history: list = field(default_factory=list)

    @property
    def c(self):
        return 2 * self.zeta * math.sqrt(self.k * self.m)

    @property
    def f_n(self):
        return natural_frequency(self.k, self.m)

    def _tmd_params(self):
        t = self.tmd
        m2 = t.mass_ratio * self.m
        w2 = 2 * math.pi * self.f_n * t.tuning
        k2 = m2 * w2 * w2
        c2 = 2 * t.zeta * m2 * w2
        return m2, k2, c2

    def _deriv(self, state, F):
        x, v, x2, v2 = state
        a = (F - self.c * v - self.k * x) / self.m
        a2 = 0.0
        if self.tmd is not None:
            m2, k2, c2 = self._tmd_params()
            f_link = k2 * (x2 - x) + c2 * (v2 - v)
            a += f_link / self.m
            a2 = -f_link / m2
        return (v, a, v2, a2)

    def step(self, F, dt):
        """Advance by dt under external force F (RK4, with sub-steps for stiffness)."""
        n = max(1, int(math.ceil(dt * self.f_n * 40)))
        h = dt / n
        s = (self.x, self.v, self.x2, self.v2)
        for _ in range(n):
            k1 = self._deriv(s, F)
            k2 = self._deriv(tuple(s[i] + h / 2 * k1[i] for i in range(4)), F)
            k3 = self._deriv(tuple(s[i] + h / 2 * k2[i] for i in range(4)), F)
            k4 = self._deriv(tuple(s[i] + h * k3[i] for i in range(4)), F)
            s = tuple(s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4))
        self.x, self.v, self.x2, self.v2 = s
        self.peak = max(self.peak, abs(self.x))
        return self.x

    @property
    def equivalent_static_force(self):
        """The spring force k x: what the structure 'feels' at this instant."""
        return self.k * self.x


@dataclass
class WindProfile:
    """Wind speed ramps up steadily so it sweeps through the resonance band."""
    u_start: float = 4.0
    u_end: float = 30.0
    ramp_time: float = 60.0
    gust: float = 0.0             # +/- m/s gusting

    def speed(self, t):
        r = min(max(t / self.ramp_time, 0.0), 1.0)
        u = self.u_start + (self.u_end - self.u_start) * r
        if self.gust:
            u += self.gust * math.sin(0.7 * t) * math.sin(0.23 * t)
        return u


class VortexWind:
    """Drives an Oscillator with vortex-shedding lift. Phase is integrated so the forcing
    frequency can change smoothly as the wind speed changes."""

    def __init__(self, osc, D, span, profile=None, C_L=0.6, fairing=False):
        self.osc = osc
        self.D = D
        self.span = span
        self.profile = profile or WindProfile()
        self.C_L = C_L * (0.25 if fairing else 1.0)
        self.phase = 0.0
        self.t = 0.0

    def step(self, dt):
        U = self.profile.speed(self.t)
        f_v = vortex_frequency(U, self.D)
        F0 = vortex_force_amplitude(U, self.D, self.span, self.C_L)
        # Lock-in: shedding only couples strongly near the natural frequency
        detune = abs(f_v - self.osc.f_n) / self.osc.f_n
        coupling = 1.0 if detune < 0.25 else max(0.15, 1.0 - (detune - 0.25) * 2)
        self.phase += 2 * math.pi * f_v * dt
        F = coupling * F0 * math.sin(self.phase)
        self.osc.step(F, dt)
        self.t += dt
        return U, f_v, F
