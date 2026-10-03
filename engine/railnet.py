r"""Harbor Switchyard network simulation (Prompt 4, Level 5).

Layout (x in metres, west -> east):

  EB_W  ====(crossing 560-640)=======[EB entry 780]\                  /==== EB_E (main) ===> 2200
                                                     ===== BRIDGE =====  S1
  WB_W  <===(crossing)=======[WB exit 750]========/  800        1400  \==== HARBOR (siding) => 2000
                                                     [WB entry 1420] ======= WB_E <=== 2200

Eastbound (EB) trains run west->east and use switch S1 at 1400 to go to the harbor (cargo)
or the main line (passenger). Westbound (WB) trains run east->west. Both directions share
the single-track bridge 800-1400, so the interlocking logic must never let them meet.
"""
import math
from dataclasses import dataclass, field

from .signals import (DOUBLE_YELLOW, GREEN, RED, YELLOW, LogicRow, aspect_for,
                      evaluate_logic, min_block_length)

G = 9.81
X_END = 2200.0
BRIDGE = (800.0, 1400.0)
CROSSING = (560.0, 640.0)
JE_ZONE = (1380.0, 1440.0)
HARBOR_END = 2000.0
EB_ENTRY_X, WB_ENTRY_X = 780.0, 1420.0
EB_EXIT_X, WB_EXIT_X = 1450.0, 750.0
SIGHT = 200.0
FRINGE_S = 1.0      # map-edge signal; trains appear just behind it
APPROACH = 450.0
XING_WARN = 350.0
BARRIER_TIME = 8.0
SWITCH_TIME = 3.0

INPUTS = ["BRIDGE_OCC", "APPR_EB", "APPR_WB", "PERMIT_EB", "PERMIT_WB", "XING_APPR",
          "CARGO_APPR_JE", "CARGO_AT_JE", "JE_OCC", "TRUE"]
OUTPUTS = ["PERMIT_EB", "PERMIT_WB", "SWITCH_HARBOR", "BARRIER_DOWN"]

# Player-placeable signal slots (route distance s from each direction's start)
SIGNAL_SLOTS = [float(s) for s in range(100, 751, 50)]


@dataclass(frozen=True)
class TrainType:
    kind: str           # "cargo" or "passenger"
    length: float
    max_speed: float
    accel: float
    brake_mu: float     # effective braking friction -> deceleration = mu * g

    @property
    def decel(self):
        return self.brake_mu * G


PASSENGER = TrainType("passenger", 120.0, 25.0, 0.6, 0.09)
CARGO = TrainType("cargo", 200.0, 18.0, 0.3, 0.05)


def default_logic():
    """The starting interlocking - it has three deliberate bugs for the player to find."""
    return [
        LogicRow("PERMIT_EB", ["APPR_EB", "BRIDGE_OCC", None], [False, True, False]),
        LogicRow("PERMIT_WB", ["APPR_WB", "BRIDGE_OCC", None], [False, True, False]),
        LogicRow("SWITCH_HARBOR", ["CARGO_APPR_JE", None, None]),
        LogicRow("BARRIER_DOWN", [None, None, None]),
    ]


def reference_logic():
    return [
        LogicRow("PERMIT_EB", ["APPR_EB", "BRIDGE_OCC", "PERMIT_WB"], [False, True, True]),
        LogicRow("PERMIT_WB", ["APPR_WB", "BRIDGE_OCC", "PERMIT_EB"], [False, True, True]),
        LogicRow("SWITCH_HARBOR", ["CARGO_AT_JE", None, None]),
        LogicRow("BARRIER_DOWN", ["XING_APPR", None, None]),
    ]


@dataclass
class Signal:
    name: str
    direction: str      # "EB" or "WB"
    s: float            # route distance where it stands
    block_end: float = 0.0
    fixed: bool = False
    aspect: str = GREEN


@dataclass
class Train:
    tid: int
    direction: str
    ttype: TrainType
    s: float = 0.0          # route distance of the FRONT
    v: float = 0.0
    branch: str = ""        # "main" / "harbor" once past S1 (EB only)
    last_aspect: str = GREEN
    next_signal_idx: int = 0
    idle: float = 0.0
    spad: bool = False
    emergency: bool = False
    done: bool = False
    spawn_time: float = 0.0

    def x_of(self, s):
        return s if self.direction == "EB" else X_END - s

    @property
    def front_x(self):
        return self.x_of(self.s)

    @property
    def rear_x(self):
        return self.x_of(self.s - self.ttype.length)

    def x_span(self):
        a, b = self.front_x, self.rear_x
        return min(a, b), max(a, b)

    def pieces(self):
        """Physical track pieces this train covers: [(track, x0, x1)]."""
        x0, x1 = self.x_span()
        out = []
        b0, b1 = BRIDGE
        if self.direction == "EB":
            approach, exit_track = "EB_W", ("HARBOR" if self.branch == "harbor" else "EB_E")
        else:
            approach, exit_track = "WB_E", "WB_W"
        lo_track = approach if self.direction == "EB" else exit_track
        hi_track = exit_track if self.direction == "EB" else approach
        if x0 < b0:
            out.append((lo_track, x0, min(x1, b0)))
        if x1 > b0 and x0 < b1:
            out.append(("BRIDGE", max(x0, b0), min(x1, b1)))
        if x1 > b1:
            out.append((hi_track, max(x0, b1), x1))
        return out

    def overlaps_x(self, a, b):
        x0, x1 = self.x_span()
        return x0 < b and x1 > a


@dataclass
class Failure:
    kind: str
    message: str
    formula: str
    time: float
    trains: tuple = ()


@dataclass
class RailNetConfig:
    duration: float = 720.0
    headway: float = 80.0          # seconds between trains in each direction
    wb_offset: float = 40.0
    target_delivered: int = 10


class RailNet:
    def __init__(self, signal_slots_eb=(), signal_slots_wb=(), four_aspect=False,
                 logic=None, cfg=None):
        self.cfg = cfg or RailNetConfig()
        self.four_aspect = four_aspect
        self.logic = logic if logic is not None else default_logic()
        self.signals = {"EB": [], "WB": []}
        for s in sorted(signal_slots_eb):
            self.signals["EB"].append(Signal(f"E{int(s)}", "EB", float(s)))
        for s in sorted(signal_slots_wb):
            self.signals["WB"].append(Signal(f"W{int(s)}", "WB", float(s)))
        self.signals["EB"].append(Signal("EB_ENTRY", "EB", EB_ENTRY_X, fixed=True))
        self.signals["WB"].append(Signal("WB_ENTRY", "WB", X_END - WB_ENTRY_X, fixed=True))
        # Fringe signals at the map edge: trains arrive having already read them
        self.signals["EB"].append(Signal("EB_FRINGE", "EB", FRINGE_S, fixed=True))
        self.signals["WB"].append(Signal("WB_FRINGE", "WB", FRINGE_S, fixed=True))
        for d in ("EB", "WB"):
            sig = self.signals[d]
            sig.sort(key=lambda g: g.s)
            for k, g in enumerate(sig):
                if k + 1 < len(sig):
                    g.block_end = sig[k + 1].s
                else:  # entry signal protects the bridge up to the far exit point
                    g.block_end = EB_EXIT_X if d == "EB" else X_END - WB_EXIT_X
        self.time = 0.0
        self.trains = []
        self.next_id = 1
        self.schedule = self._make_schedule()
        self.outputs = {o: False for o in OUTPUTS}
        self.barrier = 0.0          # 0 = up, 1 = fully down
        self.switch_pos = 0.0       # 0 = main, 1 = harbor
        self.failure = None
        self.delivered = 0
        self.delivered_cargo_harbor = 0
        self.misroutes = 0
        self.spads = 0
        self.idle_time = 0.0
        self.queue_time = 0.0
        self.barrier_down_time = 0.0
        self.events = []
        self.inputs = {}

    # --- setup -----------------------------------------------------------------------
    def _make_schedule(self):
        out = []
        kinds = [CARGO, PASSENGER]
        t, k = 5.0, 0
        while t < self.cfg.duration - 120:
            out.append((t, "EB", kinds[k % 2]))
            out.append((t + self.cfg.wb_offset, "WB", kinds[(k + 1) % 2]))
            t += self.cfg.headway
            k += 1
        out.sort(key=lambda e: e[0])
        return out

    # --- helpers ---------------------------------------------------------------------
    def trains_dir(self, d):
        return [t for t in self.trains if t.direction == d]

    def block_occupied(self, sig):
        if sig.name in ("EB_ENTRY", "WB_ENTRY"):
            # The bridge itself (either direction) plus this direction's own track beyond it
            lo, hi = (EB_ENTRY_X, EB_EXIT_X) if sig.name == "EB_ENTRY" else (WB_EXIT_X, WB_ENTRY_X)
            for t in self.trains:
                for track, a, b in t.pieces():
                    if track == "BRIDGE" or (t.direction == sig.direction and a < hi and b > lo):
                        return True
            return False
        for t in self.trains_dir(sig.direction):
            if t.s > sig.s and t.s - t.ttype.length < sig.block_end:
                return True
        return False

    def update_aspects(self):
        for d in ("EB", "WB"):
            sig = self.signals[d]
            nxt = None
            for g in reversed(sig):
                permitted = True
                if g.name == "EB_ENTRY":
                    permitted = self.outputs["PERMIT_EB"]
                elif g.name == "WB_ENTRY":
                    permitted = self.outputs["PERMIT_WB"]
                g.aspect = aspect_for(self.block_occupied(g), nxt, self.four_aspect, permitted)
                nxt = g.aspect

    def compute_inputs(self):
        inp = {"TRUE": True}
        inp["BRIDGE_OCC"] = any(t.overlaps_x(EB_ENTRY_X, WB_ENTRY_X) for t in self.trains)
        inp["APPR_EB"] = any(EB_ENTRY_X - APPROACH <= t.s < EB_ENTRY_X for t in self.trains_dir("EB"))
        wb_entry_s = X_END - WB_ENTRY_X
        inp["APPR_WB"] = any(wb_entry_s - APPROACH <= t.s < wb_entry_s for t in self.trains_dir("WB"))
        inp["PERMIT_EB"] = self.outputs["PERMIT_EB"]
        inp["PERMIT_WB"] = self.outputs["PERMIT_WB"]
        xing = False
        for t in self.trains:
            if t.overlaps_x(*CROSSING):
                xing = True
            dist = (CROSSING[0] - t.front_x) if t.direction == "EB" else (t.front_x - CROSSING[1])
            if 0 <= dist <= XING_WARN:
                xing = True
        inp["XING_APPR"] = xing
        je_occ = any(t.overlaps_x(*JE_ZONE) for t in self.trains_dir("EB"))
        inp["JE_OCC"] = je_occ
        approaching = sorted((t for t in self.trains_dir("EB")
                              if 1000 <= t.front_x < JE_ZONE[0]), key=lambda t: -t.s)
        inp["CARGO_APPR_JE"] = bool(approaching) and approaching[0].ttype.kind == "cargo"
        at = [t for t in self.trains_dir("EB") if t.overlaps_x(*JE_ZONE)] or approaching
        inp["CARGO_AT_JE"] = bool(at) and at[0].ttype.kind == "cargo"
        self.inputs = inp
        return inp

    def fail(self, kind, message, formula, trains=()):
        if not self.failure:
            self.failure = Failure(kind, message, formula, self.time, tuple(trains))

    # --- main step -----------------------------------------------------------------------
    def step(self, dt):
        if self.failure:
            return
        self.time += dt
        # spawn
        while self.schedule and self.schedule[0][0] <= self.time:
            t0, d, ttype = self.schedule[0]
            fringe = self.signals[d][0]
            clear = (fringe.aspect != RED
                     and all(t.s - t.ttype.length > 30 for t in self.trains_dir(d)))
            if not clear:
                self.queue_time += dt
                break
            self.schedule.pop(0)
            self.trains.append(Train(self.next_id, d, ttype, s=0.0, v=ttype.max_speed,
                                     spawn_time=self.time))
            self.next_id += 1

        self.compute_inputs()
        self.outputs = evaluate_logic(self.logic, self.inputs)
        self.update_aspects()

        # physical barrier and switch
        target = 1.0 if self.outputs["BARRIER_DOWN"] else 0.0
        self.barrier += max(-dt / BARRIER_TIME, min(dt / BARRIER_TIME, target - self.barrier))
        if self.barrier > 0.5:
            self.barrier_down_time += dt
        sw_target = 1.0 if self.outputs["SWITCH_HARBOR"] else 0.0
        if sw_target != self.switch_pos:
            if self.inputs["JE_OCC"]:
                t = next(t for t in self.trains_dir("EB") if t.overlaps_x(*JE_ZONE))
                self.fail("derail", f"DERAILMENT: switch S1 moved while train {t.tid} was on it",
                          "Interlocking rule: a switch may only move when its track circuit is "
                          "clear -> add 'AND NOT JE_OCC' style locking (use CARGO_AT_JE)", [t.tid])
                return
            self.switch_pos += max(-dt / SWITCH_TIME, min(dt / SWITCH_TIME, sw_target - self.switch_pos))

        for t in list(self.trains):
            self._drive(t, dt)
        self._check_hazards()

    def _signal_ahead(self, t, offset=0):
        sig = self.signals[t.direction]
        idx = t.next_signal_idx + offset
        return sig[idx] if idx < len(sig) else None

    def _drive(self, t, dt):
        tt = t.ttype
        nxt = self._signal_ahead(t)
        target = None
        if nxt is not None:
            if nxt.s - t.s <= SIGHT:
                a = nxt.aspect
                if a == RED:
                    target = nxt.s
                elif a == YELLOW:
                    after = self._signal_ahead(t, 1)
                    target = after.s if after else None
                elif a == DOUBLE_YELLOW:
                    after = self._signal_ahead(t, 2)
                    target = after.s if after else None
            else:
                if t.last_aspect == YELLOW:
                    target = nxt.s
                elif t.last_aspect == DOUBLE_YELLOW:
                    after = self._signal_ahead(t, 1)
                    target = after.s if after else None
        # line-of-sight automatic running behind a leader beyond the bridge
        leader_gap = None
        for o in self.trains_dir(t.direction):
            if o is not t and o.s > t.s:
                rear = o.s - o.ttype.length
                if leader_gap is None or rear - t.s < leader_gap:
                    leader_gap = rear - t.s
        v_allowed = tt.max_speed
        if target is not None:
            v_allowed = min(v_allowed, math.sqrt(2 * tt.decel * max(target - t.s - 10.0, 0.0)))
        if leader_gap is not None and t.s > (EB_EXIT_X if t.direction == "EB" else X_END - WB_EXIT_X):
            v_allowed = min(v_allowed, math.sqrt(2 * tt.decel * max(leader_gap - 60.0, 0.0)))
        if t.emergency:
            a = -1.5 * tt.decel
            if t.v + a * dt <= 0:
                t.emergency = False
        else:
            a = max(-tt.decel, min(tt.accel, (v_allowed - t.v) / dt))
        t.v = max(0.0, t.v + a * dt)
        old_s = t.s
        t.s += t.v * dt
        if t.v < 0.5:
            t.idle += dt
            self.idle_time += dt
        # passing signals
        while nxt is not None and old_s < nxt.s <= t.s:
            if nxt.aspect == RED:
                self.spads += 1
                t.spad = True
                t.emergency = True
                self.events.append((self.time, f"SPAD: train {t.tid} passed {nxt.name} at danger"))
            t.last_aspect = nxt.aspect
            t.next_signal_idx += 1
            nxt = self._signal_ahead(t)
        # switch S1 decides the branch when the front reaches 1400
        if t.direction == "EB" and not t.branch and t.front_x >= BRIDGE[1]:
            if 0.0 < self.switch_pos < 1.0:
                self.fail("derail", f"DERAILMENT: train {t.tid} ran onto switch S1 while it was moving",
                          "Set the switch early and hold it while JE is occupied", [t.tid])
                return
            t.branch = "harbor" if self.switch_pos >= 1.0 else "main"
            wrong = (t.branch == "harbor") != (t.ttype.kind == "cargo")
            if wrong:
                self.misroutes += 1
                self.events.append((self.time, f"Misroute: {t.ttype.kind} train {t.tid} sent to "
                                               f"{t.branch}"))
        # leaving the map
        if t.direction == "EB" and t.branch == "harbor" and t.front_x >= HARBOR_END - 10:
            t.done = True
        elif (t.rear_x >= X_END) if t.direction == "EB" else (t.rear_x <= 0):
            t.done = True
        if t.done:
            self.trains.remove(t)
            self.delivered += 1
            if t.branch == "harbor" and t.ttype.kind == "cargo":
                self.delivered_cargo_harbor += 1

    def _check_hazards(self):
        # crossing
        for t in self.trains:
            if t.overlaps_x(*CROSSING) and self.barrier < 0.99:
                self.fail("crossing", f"LEVEL CROSSING UNSAFE: train {t.tid} reached the road "
                                      f"while the barrier was {'up' if self.barrier < 0.5 else 'still lowering'}",
                          f"Barrier needs {BARRIER_TIME:.0f} s; at {t.ttype.max_speed:.0f} m/s a train covers "
                          f"{t.ttype.max_speed*BARRIER_TIME:.0f} m in that time - start lowering "
                          f"{XING_WARN:.0f} m out (XING_APPR)", [t.tid])
                return
        # collisions
        for a in range(len(self.trains)):
            for b in range(a + 1, len(self.trains)):
                ta, tb = self.trains[a], self.trains[b]
                for (tr1, a0, a1) in ta.pieces():
                    for (tr2, b0, b1) in tb.pieces():
                        if tr1 == tr2 and a0 < b1 and b0 < a1:
                            head_on = ta.direction != tb.direction
                            kind = "head-on" if head_on else "rear"
                            self.fail("collision",
                                      f"COLLISION ({kind}) on {tr1}: trains {ta.tid} and {tb.tid}",
                                      "d_stop = v^2 / (2 mu g) - every red must be warned at least "
                                      "d_stop earlier, and the bridge must only be given to one "
                                      "direction at a time (PERMIT_EB / PERMIT_WB interlock)",
                                      [ta.tid, tb.tid])
                            return

    # --- analysis ---------------------------------------------------------------------
    def block_warnings(self):
        """Blocks too short for the trains' braking distance: [(signal name, length, needed)]."""
        need = max(min_block_length(PASSENGER.max_speed, PASSENGER.brake_mu, self.four_aspect),
                   min_block_length(CARGO.max_speed, CARGO.brake_mu, self.four_aspect))
        out = []
        for d in ("EB", "WB"):
            sig = self.signals[d]
            # A red signal is warned by the caution aspect of the signal before it.
            for prev, g in zip(sig, sig[1:]):
                warning = g.s - prev.s
                if warning < need:
                    out.append((g.name, warning, need))
        return out

    @property
    def finished(self):
        return self.failure is not None or self.time >= self.cfg.duration

    def run(self, dt=0.2, until=None):
        until = until or self.cfg.duration
        while not self.failure and self.time < until:
            self.step(dt)
        return self
