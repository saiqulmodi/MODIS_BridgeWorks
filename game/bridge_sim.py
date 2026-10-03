"""Bridge levels (1, 7, 8, 10): the design model and the live simulation, with no drawing.

Kept separate from the screen code so tests can build a design and run it headless.
"""
import math
from dataclasses import dataclass, field

from engine import economy
from engine.dynamics import (TMD, Oscillator, VortexWind, WindProfile, critical_wind_speed,
                             den_hartog_optimum, ground_acceleration, spectral_coefficient)
from engine.failure import FailureReport
from engine.materials import ALL as MATERIALS, SHAPES, second_moment
from engine.truss import (FAILED, G, Member, Node, TrussSolver, UnstableStructure,
                          member_length, self_weight_loads)
from engine.vehicles import TrackPath, VehicleEngine, VehicleSpec

EXTRA_COSTS = dict(tmd=350000.0, fairing=250000.0, dampers=200000.0, isolation=300000.0,
                   joints=150000.0, grid_mw=400000.0)


@dataclass
class Beam:
    a: int
    b: int
    material: str
    A: float
    shape: str = "I-beam"
    kind: str = "beam"        # beam / deck / cable


@dataclass
class Design:
    joints: list = field(default_factory=list)     # [(x, y)]
    beams: list = field(default_factory=list)      # [Beam]
    anchors: dict = field(default_factory=dict)    # joint index -> "pin" / "roller"
    # hazard countermeasures
    tmd: bool = False
    tmd_mass_ratio: float = 0.02
    tmd_tuning: float = 0.98
    tmd_zeta: float = 0.08
    fairing: bool = False
    dampers: bool = False
    isolation: bool = False
    flex_joints: bool = False
    grid_mw: float = 4.0
    power_alloy: bool = False

    def copy(self):
        d = Design(list(self.joints), [Beam(**vars(b)) for b in self.beams], dict(self.anchors))
        for k in ("tmd", "tmd_mass_ratio", "tmd_tuning", "tmd_zeta", "fairing", "dampers",
                  "isolation", "flex_joints", "grid_mw", "power_alloy"):
            setattr(d, k, getattr(self, k))
        return d

    def joint_at(self, x, y, tol=1e-6):
        for k, (jx, jy) in enumerate(self.joints):
            if abs(jx - x) < tol and abs(jy - y) < tol:
                return k
        return None

    def add_joint(self, x, y):
        k = self.joint_at(x, y)
        if k is None:
            self.joints.append((x, y))
            k = len(self.joints) - 1
        return k

    def add_beam(self, p, q, material, A, shape="I-beam", kind="beam"):
        a, b = self.add_joint(*p), self.add_joint(*q)
        if a == b:
            return None
        for bm in self.beams:
            if {bm.a, bm.b} == {a, b}:
                bm.material, bm.A, bm.shape, bm.kind = material, A, shape, kind
                return bm
        bm = Beam(a, b, material, A, shape, kind)
        self.beams.append(bm)
        return bm

    def remove_beam(self, idx):
        self.beams.pop(idx)
        self.prune()

    def remove_joint(self, k):
        if k in self.anchors:
            return
        self.beams = [b for b in self.beams if k not in (b.a, b.b)]
        self.prune()

    def prune(self):
        """Drop joints no beam uses (anchors always stay) and renumber."""
        used = {b.a for b in self.beams} | {b.b for b in self.beams} | set(self.anchors)
        mapping, joints = {}, []
        for k, p in enumerate(self.joints):
            if k in used:
                mapping[k] = len(joints)
                joints.append(p)
        self.joints = joints
        self.anchors = {mapping[k]: v for k, v in self.anchors.items()}
        for b in self.beams:
            b.a, b.b = mapping[b.a], mapping[b.b]

    def length(self, bm):
        (x0, y0), (x1, y1) = self.joints[bm.a], self.joints[bm.b]
        return math.hypot(x1 - x0, y1 - y0)


def new_design(cfg):
    d = Design()
    for x, y, kind in cfg["anchors"]:
        d.anchors[d.add_joint(float(x), float(y))] = kind
    for x in cfg.get("extra_anchor_xs", []):
        d.anchors[d.add_joint(float(x), float(cfg.get("extra_anchor_y", cfg["ground_y"])))] = "pin"
    return d


def deck_path(design, cfg):
    """Joint indices of the road from the left bank to the right bank along deck beams."""
    start = design.joint_at(cfg["left_x"], cfg["deck_y"])
    goal = design.joint_at(cfg["right_x"], cfg["deck_y"])
    if start is None or goal is None:
        return None
    adj = {}
    for bm in design.beams:
        if bm.kind == "deck":
            adj.setdefault(bm.a, []).append(bm.b)
            adj.setdefault(bm.b, []).append(bm.a)
    prev, frontier = {start: None}, [start]
    while frontier:
        nxt = []
        for k in frontier:
            for n in sorted(adj.get(k, []), key=lambda j: design.joints[j][0]):
                if n not in prev:
                    prev[n] = k
                    nxt.append(n)
        frontier = nxt
    if goal not in prev:
        return None
    path, k = [], goal
    while k is not None:
        path.append(k)
        k = prev[k]
    path.reverse()
    return path


def build_truss(design, cfg, powered_alloy=False):
    nodes = []
    used = {b.a for b in design.beams} | {b.b for b in design.beams}
    for k, (x, y) in enumerate(design.joints):
        kind = design.anchors.get(k)
        if kind == "pin" or k not in used:      # unused anchors are simply held still
            nodes.append(Node.pinned(x, y))
        elif kind == "pin":
            nodes.append(Node.pinned(x, y))
        elif kind == "roller":
            nodes.append(Node.roller(x, y))
        else:
            nodes.append(Node(x, y))
    members = []
    humid = cfg.get("humid", False)
    for bm in design.beams:
        mat = MATERIALS[bm.material]
        shape = SHAPES.get(bm.shape, SHAPES["I-beam"])
        I = second_moment(shape, bm.A) if not mat.cable_only else 1e-12
        members.append(Member(bm.a, bm.b, mat, bm.A, I, kind=bm.kind,
                              E_factor=mat.voltage_stiffening if powered_alloy else 1.0,
                              strength_factor=mat.moisture_factor if humid else 1.0))
    return nodes, members


def alloy_tonnes(design):
    t = 0.0
    for bm in design.beams:
        mat = MATERIALS[bm.material]
        if mat.voltage_stiffening > 1:
            t += mat.density * bm.A * design.length(bm) / 1000
    return t


def design_cost(design, cfg):
    nodes, members = build_truss(design, cfg)
    extras = 0.0
    if design.tmd:
        extras += EXTRA_COSTS["tmd"] * (design.tmd_mass_ratio / 0.02)
    if design.fairing:
        extras += EXTRA_COSTS["fairing"]
    if design.dampers:
        extras += EXTRA_COSTS["dampers"]
    if design.isolation:
        extras += EXTRA_COSTS["isolation"]
    if design.flex_joints:
        extras += EXTRA_COSTS["joints"]
    if cfg.get("grid_power"):
        extras += EXTRA_COSTS["grid_mw"] * design.grid_mw
        extras += cfg.get("maglev_rs_m", 0.0) * (cfg["right_x"] - cfg["left_x"])
    # build members via index so the fabrication lookup is safe
    cb = economy.CostBreakdown(extras=extras)
    used = set()
    for bm, m in zip(design.beams, members):
        L = member_length(nodes, m)
        fab = 1.0 if m.material.cable_only else SHAPES.get(bm.shape, SHAPES["I-beam"]).fabrication
        c, mass = economy.member_material_cost(m.material, m.A, L, fab)
        cb.materials += c
        cb.carbon_kg += mass * m.material.carbon_per_kg
        cb.maintenance += c * m.material.maintenance_rate
        cb.labour += economy.LABOUR_PER_MEMBER
        h = max(0.0, (nodes[m.i].y + nodes[m.j].y) / 2 - cfg["ground_y"])
        cb.labour += economy.SCAFFOLD_PER_METRE_HEIGHT * h * 0.2
        used.update((m.i, m.j))
    cb.labour += economy.LABOUR_PER_JOINT * len(used - set(design.anchors))
    return cb


def vehicle_spec(vcfg):
    kind = vcfg["kind"]
    return VehicleSpec(kind.title(), mass=vcfg["mass"], power=vcfg["power"],
                       driven_mass=vcfg["mass"] * (0.5 if kind != "maglev" else 1.0),
                       length=vcfg["length"], axles=vcfg["axles"], C_rr=vcfg.get("C_rr", 0.0),
                       C_d=0.8, frontal_area=7.0, mu_dry=vcfg.get("mu", 0.7),
                       mu_wet=vcfg.get("mu", 0.7) * 0.6, max_speed=vcfg["speed"],
                       maglev=vcfg.get("maglev", False), max_thrust=vcfg.get("max_thrust", 0.0))


class BridgeSim:
    """Runs vehicles over a design with wind / earthquake hazards. step(dt) until done/failure."""

    APPROACH = 22.0
    EXIT = 26.0

    def __init__(self, design, cfg, level_title=""):
        self.design = design
        self.cfg = cfg
        self.path_joints = deck_path(design, cfg)
        if self.path_joints is None:
            raise ValueError("The road is not connected: build DECK beams from the left bank to "
                             "the right bank.")
        self.grid_power = cfg.get("grid_power", False)
        self.alloy_t = alloy_tonnes(design)
        self.alloy_demand = 0.05e6 * self.alloy_t if design.power_alloy else 0.0   # W
        powered = design.power_alloy and (not self.grid_power or design.grid_mw * 1e6 >= self.alloy_demand)
        self.nodes, self.members = build_truss(design, cfg, powered_alloy=powered)
        self.solver = TrussSolver(self.nodes, self.members)
        deck_load = cfg.get("deck_load", 0.0)
        self.dead = self_weight_loads(self.nodes, self.members,
                                      lambda m: deck_load if m.kind == "deck" else 0.0)
        # Throws UnstableStructure straight away if the frame is a mechanism
        self.result = self.solver.solve(self.dead)
        self.node_mass = {k: -fy / G for k, (fx, fy) in self.dead.items()}
        # Road path
        pts = [(cfg["left_x"] - self.APPROACH, cfg["deck_y"])]
        pts += [design.joints[k] for k in self.path_joints]
        pts += [(cfg["right_x"] + self.EXIT, cfg["deck_y"])]
        self.path = TrackPath(pts)
        self.deck_s0 = self.path.cum[1]
        self.deck_s1 = self.path.cum[-2]
        # Vehicles
        vcfg = cfg["vehicle"]
        self.spec = vehicle_spec(vcfg)
        self.vehicles = []
        spacing = vcfg.get("spacing", 0.0) * vcfg["speed"]
        for k in range(vcfg.get("count", 1)):
            v = VehicleEngine(self.spec, self.path, s=self.spec.length - k * max(spacing, 0.0),
                              v=0.0 if vcfg.get("maglev") else vcfg["speed"] * 0.8,
                              speed_limit=vcfg["speed"])
            self.vehicles.append(v)
        self.power_factor = 1.0
        if self.grid_power:
            avail = design.grid_mw * 1e6 - self.alloy_demand
            self.power_factor = max(0.0, min(1.0, avail / self.spec.power))
            for v in self.vehicles:
                v.power_factor = self.power_factor
        self.time = 0.0
        self.max_ratio = self.result.max_ratio
        self.history = {"max load %": []}
        self.deck_enter = None      # (time, engine work) when the first vehicle's front enters
        self.deck_exit = None
        self.failure = None
        self.done = False
        self.red_members = set()
        self.events = []        # sounds etc for the UI: ("creak", member) ...
        self._setup_wind()
        self._setup_quake()

    # --- dynamic setup -----------------------------------------------------------------
    def _deck_interior(self):
        return self.path_joints[1:-1] if len(self.path_joints) > 2 else []

    def _setup_wind(self):
        w = self.cfg.get("wind")
        self.wind = None
        if not w:
            return
        L0, L1 = self.cfg["left_x"], self.cfg["right_x"]
        span = L1 - L0
        interior = self._deck_interior()
        if not interior:
            interior = self.path_joints
        p = {}
        for k in interior:
            x = self.nodes[k].x
            p[k] = math.sin(math.pi * (x - L0) / span)
        total = sum(p.values()) or 1.0
        self.pattern = {k: v / total for k, v in p.items()}          # sums to 1 N (down)
        res = self.solver.solve({k: (0.0, -v) for k, v in self.pattern.items()})
        u = {k: -res.displacements[k][1] for k in range(len(self.nodes))}
        self.u_ref_node = max(self.pattern, key=lambda k: u[k])
        self.u_ref = max(u[self.u_ref_node], 1e-12)
        K_star = sum(self.pattern[k] * u[k] for k in self.pattern) / self.u_ref ** 2
        M_star = sum(self.node_mass.get(k, 0.0) * (u[k] / self.u_ref) ** 2 for k in range(len(self.nodes)))
        M_star = max(M_star, 100.0)
        zeta = 0.02 if self.design.dampers else 0.005
        tmd = None
        if self.design.tmd:
            tmd = TMD(self.design.tmd_mass_ratio, self.design.tmd_tuning, self.design.tmd_zeta)
        self.osc = Oscillator(M_star, K_star, zeta, tmd)
        self.deck_depth = self.cfg.get("deck_depth", 1.2)
        prof = WindProfile(w["u_start"], w["u_end"], w["ramp"], w.get("gust", 0.0))
        self.wind = VortexWind(self.osc, self.deck_depth, span, prof, fairing=self.design.fairing)
        self.wind_duration = w.get("duration", w["ramp"])
        self.f_n = self.osc.f_n
        self.U_crit = critical_wind_speed(self.f_n, self.deck_depth)
        self.history["wind m/s"] = []
        self.wind_U = prof.u_start
        self.wind_fv = 0.0
        self.mode_shape = {k: u[k] / self.u_ref for k in range(len(self.nodes))}

    def _setup_quake(self):
        q = self.cfg.get("quake")
        self.quake = q
        self.quake_t0 = None
        self.ground_x = 0.0
        if not q:
            return
        # Rayleigh estimate of the lateral period: T = 2 pi sqrt(sum m u^2 / sum F u), F = m g
        loads = {k: (m * G, 0.0) for k, m in self.node_mass.items()
                 if not self.nodes[k].fix_x}
        res = self.solver.solve(loads)
        num = sum(self.node_mass[k] * res.displacements[k][0] ** 2 for k in loads)
        den = sum(loads[k][0] * res.displacements[k][0] for k in loads)
        self.T_struct = 2 * math.pi * math.sqrt(num / den) if den > 0 else 0.05
        self.T = q["T_iso"] if self.design.isolation else self.T_struct
        self.C = spectral_coefficient(self.T)
        self.total_mass = sum(self.node_mass.values())
        self.gap = q["joint_gap"] if self.design.flex_joints else q["gap"]
        self.history["ground a (m/s2)"] = []
        self.a_g = 0.0
        self.deck_drift = 0.0

    # --- helpers -----------------------------------------------------------------------
    def axle_loads(self):
        loads = {}
        for veh in self.vehicles:
            P = veh.axle_load()
            for a in veh.axle_positions():
                if not (self.deck_s0 <= a <= self.deck_s1):
                    continue
                # path segment k joins path points k and k+1; deck segments are 1 .. n-1
                k = min(max(self.path.segment_at(a), 1), len(self.path_joints) - 1)
                seg0, seg1 = self.path.cum[k], self.path.cum[k + 1]
                t = (a - seg0) / (seg1 - seg0) if seg1 > seg0 else 0.0
                j0 = self.path_joints[k - 1]
                j1 = self.path_joints[k]
                for j, share in ((j0, 1 - t), (j1, t)):
                    fx, fy = loads.get(j, (0.0, 0.0))
                    loads[j] = (fx, fy - P * share)
        return loads

    def total_loads(self, vehicle_loads=None):
        loads = dict(self.dead)
        for src in (vehicle_loads or {},):
            for k, (fx, fy) in src.items():
                ox, oy = loads.get(k, (0.0, 0.0))
                loads[k] = (ox + fx, oy + fy)
        return loads

    def preview(self, frac=0.5):
        """Static check with one vehicle centred at `frac` of the deck (editor 'Test' mode)."""
        saved = [v.s for v in self.vehicles]
        mid = self.deck_s0 + frac * (self.deck_s1 - self.deck_s0) + self.spec.length / 2
        for k, v in enumerate(self.vehicles):
            v.s = mid if k == 0 else -1e6
        res = self.solver.solve(self.total_loads(self.axle_loads()))
        for v, s in zip(self.vehicles, saved):
            v.s = s
        return res

    def worst_preview(self, steps=9):
        worst = None
        for i in range(steps):
            r = self.preview(i / (steps - 1))
            if worst is None or r.max_ratio > worst.max_ratio:
                worst = r
        return worst

    @property
    def span_done(self):
        return all(v.finished for v in self.vehicles)

    # --- main step ------------------------------------------------------------------------
    def step(self, dt):
        if self.failure or self.done:
            return
        self.time += dt
        for v in self.vehicles:
            v.step(dt)
            if v.runaway:
                self._fail_vehicle(v)
                return
        lead = self.vehicles[0]
        if self.deck_enter is None and lead.s >= self.deck_s0:
            self.deck_enter = (self.time, lead.engine_work)
        if self.deck_exit is None and lead.s - lead.spec.length >= self.deck_s1:
            self.deck_exit = (self.time, lead.engine_work)
        loads = self.total_loads(self.axle_loads())
        if self.wind:
            U, f_v, _ = self.wind.step(dt)
            self.wind_U, self.wind_fv = U, f_v
            q = self.osc.x
            scale = q / self.u_ref
            for k, p in self.pattern.items():
                fx, fy = loads.get(k, (0.0, 0.0))
                loads[k] = (fx, fy - p * scale)
            self._hist("wind m/s", U)
        if self.quake:
            self._quake_loads(loads, dt)
            if self.failure:
                return
        try:
            self.result = self.solver.solve(loads)
        except UnstableStructure as e:
            self.failure = FailureReport("unstable", "STRUCTURE FOLDED UP", str(e), time=self.time,
                                         history=self.history)
            return
        r = self.result.max_ratio
        self.max_ratio = max(self.max_ratio, r)
        self._hist("max load %", 100 * r)
        for k, mr in enumerate(self.result.members):
            if mr.status in ("red", FAILED) and k not in self.red_members:
                self.red_members.add(k)
                self.events.append(("groan" if self.members[k].material.name != "Timber" else "creak", k))
            elif mr.status not in ("red", FAILED):
                self.red_members.discard(k)
        failed = self.result.failed_members
        if failed:
            k = max(failed, key=lambda i: self.result.members[i].ratio)
            mr = self.result.members[k]
            kind = mr.failure_mode or "yield"
            if self.wind and self.dynamic_load() > 0.5 * self.spec.mass * G:
                kind = "resonance"
            if self.quake and self.quake_t0 is not None and abs(self.a_g) > 0.5:
                kind = "seismic" if kind == "yield" else kind
            details = [f"Member {k}: {self.members[k].material.name}, L = {mr.length:.1f} m, "
                       f"A = {self.members[k].A*1e4:.0f} cm^2"]
            if self.wind:
                details.append(f"Wind {self.wind_U:.1f} m/s -> f_v = St U / D = {self.wind_fv:.2f} Hz "
                               f"vs f_n = {self.f_n:.2f} Hz (U_crit = {self.U_crit:.1f} m/s)")
            if self.quake:
                details.append(f"Ground a = {self.a_g:.2f} m/s^2, C = {self.C:.2f}, "
                               f"V_base = C M a = {self.C*self.total_mass*abs(self.a_g)/1e3:.0f} kN")
            self.failure = FailureReport(kind, mr.explanation.split(":")[0] + f" - member {k}",
                                         mr.explanation, details, self.time, k, self.history)
            return
        if self.grid_power and self.cfg.get("time_limit") and self.time > self.cfg["time_limit"] \
                and not self.span_done:
            kind = "brownout" if self.power_factor < 0.5 else "timeout"
            self.failure = FailureReport(kind, "TOO SLOW: the pod train missed its slot",
                                         f"Grid {self.design.grid_mw:.1f} MW - alloy "
                                         f"{self.alloy_demand/1e6:.2f} MW leaves "
                                         f"{max(0.0, self.design.grid_mw - self.alloy_demand/1e6):.2f} MW "
                                         f"for a {self.spec.power/1e6:.1f} MW pod: thrust = P / v",
                                         time=self.time, history=self.history)
            return
        finished = self.span_done
        if self.wind and self.time < self.wind_duration:
            finished = False
        if self.quake and (self.quake_t0 is None or self.time < self.quake_t0 + self.quake["duration"]):
            finished = False
        if finished:
            self.done = True

    def dynamic_load(self):
        """Equivalent static load (N) from the wind-driven swing right now: k* q."""
        return abs(self.osc.x) / self.u_ref if self.wind else 0.0

    def _hist(self, name, value):
        h = self.history.setdefault(name, [])
        if not h or self.time - h[-1][0] >= 0.1:
            h.append((self.time, value))

    def _quake_loads(self, loads, dt):
        q = self.quake
        if self.quake_t0 is None:
            front = max(v.s for v in self.vehicles)
            if front >= self.deck_s0 + q["start_frac"] * (self.deck_s1 - self.deck_s0):
                self.quake_t0 = self.time
                self.events.append(("quake", None))
        if self.quake_t0 is None:
            self.a_g = 0.0
            self._hist("ground a (m/s2)", 0.0)
            return
        t = self.time - self.quake_t0
        self.a_g = ground_acceleration(t, q["A_peak"], q["f"], q["decay"]) if t < q["duration"] else 0.0
        self.ground_x = self.a_g * 0.02
        self._hist("ground a (m/s2)", self.a_g)
        for k, m in self.node_mass.items():
            if self.nodes[k].fix_x:
                continue
            fx, fy = loads.get(k, (0.0, 0.0))
            loads[k] = (fx - m * self.C * self.a_g, fy)
        if self.design.isolation:
            w = 2 * math.pi / self.T
            self.deck_drift = self.C * self.a_g / (w * w)
            if abs(self.deck_drift) > self.gap:
                self.failure = FailureReport(
                    "pounding", "POUNDING: the isolated deck slammed into the abutment",
                    f"drift = C a_g / omega^2 = {self.C:.2f} x {abs(self.a_g):.2f} / "
                    f"{w*w:.2f} = {abs(self.deck_drift):.2f} m > joint gap {self.gap:.2f} m",
                    [f"Isolation stretched the period to T = {self.T:.1f} s, which cut C to "
                     f"{self.C:.2f} - but bigger movement needs flexible joints."],
                    self.time, None, self.history)

    def _fail_vehicle(self, v):
        self.failure = FailureReport("stall", "VEHICLE ROLLED BACK", v.stall_explanation(),
                                     time=self.time, history=self.history)

    # --- results ---------------------------------------------------------------------
    @property
    def factor_of_safety(self):
        return economy.factor_of_safety(self.max_ratio)

    def toll_numbers(self):
        """Toll = (t x km) / (h x L) for the first vehicle's crossing of the deck, compared with
        an ideal crossing at the speed limit on a flat road. Returns (actual, ideal)."""
        sp = self.spec
        dist = (self.deck_s1 - self.deck_s0) + sp.length
        tons, km = sp.mass / 1000, dist / 1000
        ideal_h = dist / sp.max_speed / 3600
        ideal_work = (sp.C_rr * sp.mass * G + 0.5 * 1.225 * sp.C_d * sp.frontal_area * sp.max_speed ** 2) * dist
        ideal_l = max(ideal_work, 1.0) / (3.6e7 * 0.35)            # diesel: 36 MJ/L at 35%
        if self.deck_enter and self.deck_exit:
            h = max(self.deck_exit[0] - self.deck_enter[0], 1e-6) / 3600
            litres = max(self.deck_exit[1] - self.deck_enter[1], ideal_work) / (3.6e7 * 0.35)
        else:
            h, litres = ideal_h, ideal_l
        return economy.toll(tons, km, h, litres), economy.toll(tons, km, ideal_h, ideal_l)

    def toll_ratio(self):
        actual, ideal = self.toll_numbers()
        return min(1.2, actual / ideal) if ideal else 1.0

    def wind_summary(self):
        if not self.wind:
            return None
        mu = self.design.tmd_mass_ratio
        best_tune, best_zeta = den_hartog_optimum(mu)
        return dict(f_n=self.f_n, U_crit=self.U_crit, M=self.osc.m, K=self.osc.k,
                    best_tune=best_tune, best_zeta=best_zeta)
