"""Balanced cantilever construction (Prompt 3).

Two tall piers stand in a canyon. Concrete segments are cast one at a time outward from
each pier, like a see-saw growing both ways. Every new segment (and the heavy form
traveller machine sitting at the tip) adds a turning moment about the pier:

    sum(M_pier) = sum(W_right * x_right) - sum(W_left * x_left)

If that unbalance is bigger than what the foundation (plus any temporary tie-down
cables) can resist, the pier tilts over. The girder root also has to survive the
hogging moment M = sum(W * x): sigma = M * y / I with I = b d^3 / 12.

When the two inner arms meet in the middle, "Stitch & Post-Tension" joins everything
into one continuous beam resting on abutments and piers, and the moments redistribute.
"""
import math
from dataclasses import dataclass, field

from .beams import BeamSolver, bending_stress, haunch_depth, rect_I, rect_Q_max, shear_stress

G = 9.81
CONCRETE_DENSITY = 2400.0


@dataclass
class CantileverConfig:
    abutments: tuple = (0.0, 66.0)
    piers: tuple = (18.0, 48.0)
    seg_len: float = 3.0
    width: float = 1.2                 # effective web width b, m
    traveller_weight: float = 400e3    # N, form traveller at each growing tip
    base_capacity: float = 7e6        # N*m the foundation resists without help
    tie_down_capacity: float = 6e6     # N*m added per temporary tie-down
    allow_tension_build: float = 8e6   # Pa, root tension allowed while cantilevering (built-in tendons)
    allow_compression: float = 20e6    # Pa
    concrete_tension: float = 3e6      # Pa, continuous girder before post-tensioning
    pt_levels: tuple = (0.0, 3e6, 6e6) # extra allowable tension from post-tensioning
    road_load: float = 20e3            # N/m superimposed dead load after stitching
    truck_axles: tuple = (196e3, 196e3)
    truck_axle_gap: float = 4.0
    depth_range: tuple = (1.5, 6.5)


@dataclass
class StageCheck:
    ok: bool
    overturning: float      # N*m, signed (+ tips right)
    capacity: float         # N*m
    root_stress: float      # Pa (worst arm of this pier)
    root_moment: float      # N*m
    message: str
    failure: str = ""       # "", "overturn", "root"


@dataclass
class CantileverBridge:
    cfg: CantileverConfig = field(default_factory=CantileverConfig)
    d_pier: float = 4.0
    d_tip: float = 2.0
    segments: dict = field(default_factory=dict)   # (pier, side) -> count; side -1 left, +1 right
    tie_downs: list = field(default_factory=lambda: [0, 0])
    stitched: bool = False
    pt_level: int = 0

    def __post_init__(self):
        for p in range(len(self.cfg.piers)):
            for side in (-1, 1):
                self.segments.setdefault((p, side), 0)

    # --- geometry -------------------------------------------------------------
    def arm_target(self, pier, side):
        """Length (m) this arm must reach: to the abutment (outer) or to midspan (inner)."""
        x = self.cfg.piers[pier]
        a0, a1 = self.cfg.abutments
        mid = (self.cfg.piers[0] + self.cfg.piers[-1]) / 2
        if side == -1:
            end = a0 if pier == 0 else mid
        else:
            end = a1 if pier == len(self.cfg.piers) - 1 else mid
        return abs(end - x)

    def arm_segments_needed(self, pier, side):
        return int(round(self.arm_target(pier, side) / self.cfg.seg_len))

    def arm_complete(self, pier, side):
        return self.segments[(pier, side)] >= self.arm_segments_needed(pier, side)

    def haunch_length(self, pier):
        return max(self.arm_target(pier, -1), self.arm_target(pier, 1))

    def depth_at(self, x):
        """Girder depth at position x (nearest pier's haunch)."""
        pier = min(range(len(self.cfg.piers)), key=lambda p: abs(x - self.cfg.piers[p]))
        return haunch_depth(x, self.cfg.piers[pier], self.haunch_length(pier),
                            self.d_pier, self.d_tip)

    def I_at(self, x):
        return rect_I(self.cfg.width, self.depth_at(x))

    def weight_per_m(self, x):
        return CONCRETE_DENSITY * G * self.cfg.width * self.depth_at(x)

    def segment_span(self, pier, side, k):
        """(x_start, x_end) of segment k (0 = next to pier) on an arm."""
        x0 = self.cfg.piers[pier]
        a = x0 + side * k * self.cfg.seg_len
        b = x0 + side * (k + 1) * self.cfg.seg_len
        return (min(a, b), max(a, b))

    def segment_weight(self, pier, side, k):
        a, b = self.segment_span(pier, side, k)
        n = 6
        return sum(self.weight_per_m(a + (b - a) * (i + 0.5) / n) for i in range(n)) * (b - a) / n

    def tip_distance(self, pier, side):
        return self.segments[(pier, side)] * self.cfg.seg_len

    def can_change_haunch(self):
        return all(c == 0 for c in self.segments.values())

    # --- construction-stage mechanics ----------------------------------------------
    def arm_moment(self, pier, side, with_traveller=True):
        """Hogging moment at the pier root from one arm (positive number), N*m."""
        M = 0.0
        for k in range(self.segments[(pier, side)]):
            M += self.segment_weight(pier, side, k) * (k + 0.5) * self.cfg.seg_len
        if with_traveller and not self.arm_complete(pier, side):
            M += self.cfg.traveller_weight * self.tip_distance(pier, side)
        return M

    def propped(self, pier):
        """An outer arm that has landed on its abutment props the pier against tipping."""
        outer = -1 if pier == 0 else 1
        return self.arm_complete(pier, outer)

    def capacity(self, pier):
        return self.cfg.base_capacity + self.tie_downs[pier] * self.cfg.tie_down_capacity

    def check_pier(self, pier, casting_side=None):
        """Check overturning and root stress of one pier.

        casting_side: the side whose newest segment was just cast. While it is being cast its
        traveller still stands at the new tip, so it counts even if the arm is now complete.
        """
        def arm(side):
            M = self.arm_moment(pier, side, with_traveller=False)
            if self.segments[(pier, side)] and (not self.arm_complete(pier, side)
                                                or side == casting_side):
                M += self.cfg.traveller_weight * self.tip_distance(pier, side)
            return M

        right, left = arm(1), arm(-1)
        overturning = right - left
        landed = self.propped(pier) and casting_side != (-1 if pier == 0 else 1)
        cap = math.inf if landed else self.capacity(pier)
        root_M = max(right, left)
        I = rect_I(self.cfg.width, self.d_pier)
        root_stress = bending_stress(root_M, I, self.d_pier / 2)
        if abs(overturning) > cap:
            direction = "right" if overturning > 0 else "left"
            return StageCheck(False, overturning, cap, root_stress, root_M,
                              f"PIER TILT: unbalanced moment {abs(overturning)/1e6:.1f} MN*m "
                              f"(tipping {direction}) exceeded the foundation's "
                              f"{cap/1e6:.1f} MN*m", "overturn")
        if root_stress > self.cfg.allow_tension_build:
            return StageCheck(False, overturning, cap, root_stress, root_M,
                              f"ROOT CRACK: sigma = M*y/I = {root_M/1e6:.1f} MN*m x "
                              f"{self.d_pier/2:.2f} m / {I:.2f} m^4 = {root_stress/1e6:.1f} MPa "
                              f"> {self.cfg.allow_tension_build/1e6:.0f} MPa", "root")
        return StageCheck(True, overturning, cap if not landed else self.capacity(pier),
                          root_stress, root_M,
                          f"Balance {overturning/1e6:+.1f} MN*m of +/-{self.capacity(pier)/1e6:.1f};"
                          f" root sigma {root_stress/1e6:.1f} MPa")

    def add_segment(self, pier, side):
        """Cast the next segment on an arm. Returns the StageCheck (ok=False means failure)."""
        if self.stitched:
            raise ValueError("Already stitched")
        if self.arm_complete(pier, side):
            raise ValueError("That arm is already complete")
        self.segments[(pier, side)] += 1
        return self.check_pier(pier, casting_side=side)

    def ready_to_stitch(self):
        return all(self.arm_complete(p, s) for p in range(len(self.cfg.piers)) for s in (-1, 1))

    # --- continuous girder after stitching ---------------------------------------------
    def beam_model(self, step=1.5):
        a0, a1 = self.cfg.abutments
        n = int(round((a1 - a0) / step))
        xs = [a0 + i * (a1 - a0) / n for i in range(n + 1)]
        mids = [(xs[i] + xs[i + 1]) / 2 for i in range(n)]
        E = 30e9
        EI = [E * self.I_at(x) for x in mids]
        supports = {0: "pin", n: "pin"}
        for p in self.cfg.piers:
            supports[min(range(n + 1), key=lambda i: abs(xs[i] - p))] = "pin"
        solver = BeamSolver(xs, EI, supports)
        w = [self.weight_per_m(x) + self.cfg.road_load for x in mids]
        return solver, xs, mids, w

    def allowable_tension(self):
        return self.cfg.concrete_tension + self.cfg.pt_levels[self.pt_level]

    def girder_check(self, truck_front=None, solver_bundle=None):
        """Continuous-beam check with an optional truck. Returns (ratio, worst_x, result, info)."""
        solver, xs, mids, w = solver_bundle or self.beam_model()
        point = {}
        if truck_front is not None:
            for k, P in enumerate(self.cfg.truck_axles):
                x = truck_front - k * self.cfg.truck_axle_gap
                if xs[0] <= x <= xs[-1]:
                    # share the axle between the two nearest joints
                    i = max(0, min(len(xs) - 2, int((x - xs[0]) / (xs[1] - xs[0]))))
                    t = (x - xs[i]) / (xs[i + 1] - xs[i])
                    point[i] = point.get(i, 0.0) + P * (1 - t)
                    point[i + 1] = point.get(i + 1, 0.0) + P * t
        res = solver.solve(w=w, point_loads=point)
        worst, worst_x, info = 0.0, xs[0], ""
        allow_t = self.allowable_tension()
        for k, x in enumerate(res.x):
            d = self.depth_at(x)
            I = rect_I(self.cfg.width, d)
            sigma = abs(bending_stress(res.M[k], I, d / 2))
            ratio = max(sigma / allow_t, sigma / self.cfg.allow_compression)
            tau = shear_stress(abs(res.V[k]), rect_Q_max(self.cfg.width, d), I, self.cfg.width)
            ratio = max(ratio, tau / 2.5e6)
            if ratio > worst:
                worst, worst_x = ratio, x
                kind = "sagging (bottom pulled)" if res.M[k] > 0 else "hogging (top pulled)"
                info = (f"x = {x:.1f} m: M = {res.M[k]/1e6:.2f} MN*m {kind}, d = {d:.2f} m, "
                        f"I = b d^3/12 = {I:.2f} m^4, sigma = M y / I = {sigma/1e6:.2f} MPa "
                        f"(allowed {allow_t/1e6:.0f} MPa); tau = VQ/(It) = {tau/1e6:.2f} MPa")
        return worst, worst_x, res, info

    # --- cost ----------------------------------------------------------------------
    def concrete_volume(self):
        vol = 0.0
        for (p, side), count in self.segments.items():
            for k in range(count):
                a, b = self.segment_span(p, side, k)
                n = 6
                vol += sum(self.depth_at(a + (b - a) * (i + 0.5) / n) for i in range(n)) \
                    * (b - a) / n * self.cfg.width
        return vol


# --- cost (Rs) ------------------------------------------------------------------------------
CONCRETE_RS_M3 = CONCRETE_DENSITY * 8.0      # Rs 8 per kg
SEGMENT_LABOUR = 60000.0                     # moving the traveller and casting one segment
TIE_DOWN_RS = 500000.0
PT_RS = (0.0, 600000.0, 1200000.0)
STITCH_RS = 300000.0


def construction_cost(b):
    segs = sum(b.segments.values())
    return (b.concrete_volume() * CONCRETE_RS_M3 + segs * SEGMENT_LABOUR
            + sum(b.tie_downs) * TIE_DOWN_RS + PT_RS[b.pt_level] + (STITCH_RS if b.stitched else 0.0))
