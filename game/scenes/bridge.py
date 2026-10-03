"""Bridge levels (1, 7, 8, 10): draw beams, run vehicles, watch the forces."""
import math

import pygame

from engine import economy
from engine.dynamics import den_hartog_optimum, spectral_coefficient
from engine.failure import FailureReport
from engine.materials import ALL as MATERIALS, BEAM_SIZES, CABLE_SIZES, SHAPES, second_moment
from engine.truss import FAILED, UnstableStructure, euler_buckling_load

from .. import sound
from ..bridge_sim import BridgeSim, deck_path, design_cost, new_design
from ..common import Card, LevelScene
from ..ui import (ACCENT, BAD, BG_DARK, BOTTOM_BAR, CYAN, DRAWER_W, GOOD, HEIGHT, LINE, MUTED,
                  PANEL_EDGE, STATUS, TEXT, TOP_BAR, WARN, WIDTH, Button, Cycler, Slider,
                  WidgetGroup, arrow, blueprint_background, mini_chart, panel, text)

ROCK = (40, 58, 84)
ROCK_EDGE = (120, 150, 190)
WATER = (30, 90, 160)


class Camera:
    def __init__(self, view):
        x0, y0, x1, y1 = view
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        area = pygame.Rect(10, TOP_BAR + 10, WIDTH - DRAWER_W - 46, HEIGHT - TOP_BAR - BOTTOM_BAR - 20)
        self.scale = min(area.w / (x1 - x0), area.h / (y1 - y0))
        self.ox = area.x + (area.w - (x1 - x0) * self.scale) / 2
        self.oy = area.y + (area.h - (y1 - y0) * self.scale) / 2
        self.shake = 0.0

    def to_screen(self, x, y):
        return (int(self.ox + (x - self.x0) * self.scale + self.shake),
                int(self.oy + (self.y1 - y) * self.scale))

    def to_world(self, px, py):
        return ((px - self.ox) / self.scale + self.x0, self.y1 - (py - self.oy) / self.scale)


def seg_dist(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


class BridgeScene(LevelScene):
    CONTROLS = ("Pick a tool, then click a start point and an end point (or drag). Deck = road "
                "the vehicle drives on. Right-click deletes. Ctrl+Z undo. Select tool + click a "
                "beam/joint/vehicle shows its maths. SPACE runs the test.")

    def __init__(self, app, level):
        super().__init__(app, level)
        self.cfg = level.cfg
        self.cam = Camera(self.cfg["view"])
        self.design = new_design(self.cfg)
        self.undo_stack = []
        self.tool = "deck"
        self.pending = None
        self.mouse_world = None
        self.mode = "edit"
        self.sim = None
        self.preview = None
        self._preview_sim = None
        self.preview_on = True
        self.preview_error = ""
        self.vectors = False
        self.deflect = 1
        self.speed = 1
        self.selected = None
        self.dirty = True
        self.tick = 0
        self.debris = None
        self.lab_open = False
        self.lab = WidgetGroup()
        self.run_under_overlay = False
        self._build_toolbar()
        self._build_lab()
        self.drawer.show("Calculator", [], hint="Build with the tools below. Turn on TEST to "
                                                  "see live stress colours while you draw.")

    # --- toolbar -----------------------------------------------------------------------
    def _materials_for(self, tool):
        names = [n for n in self.level.materials if n in MATERIALS]
        if tool == "cable":
            return [n for n in names if MATERIALS[n].cable_only] or ["Steel cable"]
        return [n for n in names if not MATERIALS[n].cable_only] or ["Steel"]

    def _build_toolbar(self):
        y = HEIGHT - BOTTOM_BAR + 9
        x = 10
        self.tool_buttons = {}
        tools = [("select", "Select", pygame.K_s), ("deck", "Deck", pygame.K_d),
                 ("beam", "Beam", pygame.K_b)]
        if self.cfg.get("max_cable"):
            tools.append(("cable", "Cable", pygame.K_k))
        tools.append(("delete", "Delete", pygame.K_x))
        for key, label, hk in tools:
            b = self.widgets.add(Button((x, y, 72, 40), label, lambda k=key: self.set_tool(k),
                                        hotkey=hk, size=15))
            self.tool_buttons[key] = b
            x += 76
        x += 6
        self.mat_cycler = self.widgets.add(Cycler((x, y, 150, 40), "", self._materials_for("deck"),
                                                  on_change=self._apply_style, size=14,
                                                  hotkey=pygame.K_m))
        x += 154
        self.size_cycler = self.widgets.add(Cycler((x, y, 66, 40), "Size ", list(BEAM_SIZES), 1,
                                                   on_change=self._apply_style, size=14))
        x += 70
        self.shape_cycler = self.widgets.add(Cycler((x, y, 118, 40), "", list(SHAPES), 1,
                                                    on_change=self._apply_style, size=14))
        x += 128
        self.widgets.add(Button((x, y, 60, 40), "Undo", self.undo, size=14))
        x += 64
        self.widgets.add(Button((x, y, 60, 40), "Clear", self.clear, size=14))
        x += 70
        self.test_btn = self.widgets.add(Button((x, y, 64, 40), "TEST", self.toggle_preview,
                                                toggle=True, active=True, hotkey=pygame.K_t, size=14,
                                                tooltip="Live stress colours with the vehicle at "
                                                        "its worst position."))
        x += 68
        self.vec_btn = self.widgets.add(Button((x, y, 76, 40), "Vectors", self.toggle_vectors,
                                               toggle=True, hotkey=pygame.K_v, size=14,
                                               tooltip="Show force arrows (length = kN)."))
        x += 80
        self.def_btn = self.widgets.add(Button((x, y, 74, 40), "Sag x1", self.cycle_deflect,
                                               hotkey=pygame.K_f, size=14,
                                               tooltip="Exaggerate deflection 10x / 50x so you can "
                                                       "see the sag and bulge."))
        x += 78
        self.speed_btn = self.widgets.add(Button((x, y, 52, 40), "x1", self.cycle_speed, size=14))
        x += 56
        self.run_btn = self.widgets.add(Button((x, y, WIDTH - x - 10, 40), "RUN", self.toggle_run,
                                               hotkey=pygame.K_SPACE, colour=(40, 110, 70)))
        self.set_tool("deck")
        hazard = None
        if self.cfg.get("wind"):
            hazard = "Wind lab"
        if self.cfg.get("quake"):
            hazard = "Quake lab"
        if self.cfg.get("grid_power"):
            hazard = "Grid & wind lab"
        if hazard:
            self.top_buttons.add(Button((WIDTH - 380, 6, 160, 32), hazard, self.toggle_lab, size=14,
                                        hotkey=pygame.K_l))

    def _build_lab(self):
        """Hazard countermeasures: toggles and sliders shown at the top of the calculator."""
        d = self.design
        self.lab.clear()
        x, y = 0, 0
        def toggle(label, attr, tip):
            b = Button((x, y, 230, 32), label, lambda a=attr: self._toggle_attr(a), toggle=True,
                       active=getattr(self.design, attr), size=14, tooltip=tip)
            self.lab.add(b)
            return b
        if self.cfg.get("wind"):
            toggle(f"Tuned mass damper (+{economy.format_rs(350000)})", "tmd",
                   "A heavy pendulum mass under the deck, tuned to swing against the bridge.")
            self.lab.add(Slider((x, y, 230, 40), "TMD mass ratio mu", 0.005, 0.06, d.tmd_mass_ratio,
                                lambda v: self._set_attr("tmd_mass_ratio", v), "{:.3f}", 0.005))
            self.lab.add(Slider((x, y, 230, 40), "TMD tuning f_tmd/f_n", 0.7, 1.3, d.tmd_tuning,
                                lambda v: self._set_attr("tmd_tuning", v), "{:.2f}", 0.01))
            self.lab.add(Slider((x, y, 230, 40), "TMD damping zeta", 0.01, 0.25, d.tmd_zeta,
                                lambda v: self._set_attr("tmd_zeta", v), "{:.2f}", 0.01))
            toggle(f"Aerodynamic fairings (+{economy.format_rs(250000)})", "fairing",
                   "Streamlined edges break up the vortices: lift coefficient drops by 75%.")
            toggle(f"Cross-stay dampers (+{economy.format_rs(200000)})", "dampers",
                   "Raise structural damping from 0.5% to 2%.")
        if self.cfg.get("quake"):
            toggle(f"Isolation bearings (+{economy.format_rs(300000)})", "isolation",
                   "Rubber-lead bearings stretch the period to 2.5 s: C drops to 0.5.")
            toggle(f"Flexible expansion joints (+{economy.format_rs(150000)})", "flex_joints",
                   "Let the deck move 0.40 m instead of 0.05 m before it hits the abutment.")
        if self.cfg.get("grid_power"):
            self.lab.add(Slider((x, y, 230, 40), "Smart grid capacity (MW)", 0.5, 8.0, d.grid_mw,
                                lambda v: self._set_attr("grid_mw", v), "{:.1f}", 0.1))
            toggle("Power the smart alloy (E x2)", "power_alloy",
                   "Smart-alloy members double their stiffness but draw 50 kW per tonne.")

    def toggle_lab(self):
        self.lab_open = True
        self.drawer.open = True
        self.select(("lab", None))

    def _toggle_attr(self, attr):
        if self.mode != "edit":
            self.say("Stop the run to change the bridge")
            self.select(("lab", None))
            return
        self.push_undo()
        setattr(self.design, attr, not getattr(self.design, attr))
        self.dirty = True
        self.select(("lab", None))

    def _set_attr(self, attr, v):
        if self.mode != "edit":
            return
        setattr(self.design, attr, v)
        self.dirty = True

    def set_tool(self, key):
        self.tool = key
        self.pending = None
        for k, b in self.tool_buttons.items():
            b.active = k == key
        if key in ("deck", "beam", "cable"):
            mats = self._materials_for(key)
            if self.mat_cycler.options != mats:
                self.mat_cycler.options = mats
                self.mat_cycler.index = 0
                self.mat_cycler.label = self.mat_cycler._label()
            sizes = list(CABLE_SIZES if key == "cable" else BEAM_SIZES)
            self.size_cycler.options = sizes

    def _style(self):
        mat = self.mat_cycler.value
        sizes = CABLE_SIZES if MATERIALS[mat].cable_only else BEAM_SIZES
        return mat, sizes[self.size_cycler.value], self.shape_cycler.value

    def _apply_style(self, _value):
        """Changing material/size/shape also restyles the selected beam."""
        if self.mode == "edit" and self.selected and self.selected[0] == "beam":
            bm = self.design.beams[self.selected[1]]
            mat, A, shape = self._style()
            if MATERIALS[mat].cable_only == (bm.kind == "cable"):
                self.push_undo()
                bm.material, bm.A, bm.shape = mat, A, shape
                self.dirty = True
                self.select(self.selected)

    def toggle_preview(self):
        self.preview_on = self.test_btn.active
        self.dirty = True

    def toggle_vectors(self):
        self.vectors = self.vec_btn.active

    def cycle_deflect(self):
        self.deflect = {1: 10, 10: 50, 50: 1}[self.deflect]
        self.def_btn.label = f"Sag x{self.deflect}"

    def cycle_speed(self):
        self.speed = {1: 2, 2: 4, 4: 1}[self.speed]
        self.speed_btn.label = f"x{self.speed}"

    # --- editing --------------------------------------------------------------------------
    def push_undo(self):
        self.undo_stack.append(self.design.copy())
        self.undo_stack = self.undo_stack[-60:]

    def undo(self):
        if self.mode == "edit" and self.undo_stack:
            self.design = self.undo_stack.pop()
            self.selected = None
            self.dirty = True
            self._build_lab()

    def clear(self):
        if self.mode == "edit":
            self.push_undo()
            d = new_design(self.cfg)
            for attr in ("tmd", "fairing", "dampers", "isolation", "flex_joints", "grid_mw"):
                setattr(d, attr, getattr(self.design, attr))
            self.design = d
            self.selected = None
            self.dirty = True

    def cost(self):
        return design_cost(self.design, self.cfg).total

    def snap(self, wx, wy):
        g = self.cfg["grid"]
        sx, sy = round(wx / g) * g, round(wy / g) * g
        # prefer an existing joint near the cursor
        best, bd = None, 14 / self.cam.scale
        for (jx, jy) in self.design.joints:
            d = math.hypot(jx - wx, jy - wy)
            if d < bd:
                best, bd = (jx, jy), d
        return best or (float(sx), float(sy))

    def solid(self, x, y):
        c = self.cfg
        eps = 1e-6
        if y < c["deck_y"] - eps and (x < c["left_x"] - eps or x > c["right_x"] + eps):
            return True
        if y < c["ground_y"] - eps:
            return True
        for a, b in c.get("islands", []):
            if a + eps < x < b - eps and y < c.get("extra_anchor_y", c["ground_y"]) - eps:
                return True
        v = c["view"]
        return not (v[0] <= x <= v[2] and v[1] <= y <= v[3])

    def try_add(self, p, q):
        if p == q:
            return
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        kind = self.tool
        limit = self.cfg.get("max_cable", 0) if kind == "cable" else self.cfg.get("max_beam", 8)
        if L > limit + 1e-6:
            self.say(f"Too long: {L:.1f} m (max {limit:.0f} m for this tool)")
            return
        for pt in (p, q):
            if self.solid(*pt):
                self.say("You can't build inside the rock")
                return
        mat, A, shape = self._style()
        self.push_undo()
        self.design.add_beam(p, q, mat, A, shape, kind)
        self.dirty = True
        sound.play("click")

    def beam_at(self, pos):
        best, bd = None, 9
        for k, bm in enumerate(self.design.beams):
            a = self.cam.to_screen(*self.design.joints[bm.a])
            b = self.cam.to_screen(*self.design.joints[bm.b])
            d = seg_dist(pos, a, b)
            if d < bd:
                best, bd = k, d
        return best

    def joint_at(self, pos):
        for k, (x, y) in enumerate(self.design.joints):
            sx, sy = self.cam.to_screen(x, y)
            if math.hypot(sx - pos[0], sy - pos[1]) < 10:
                return k
        return None

    def vehicle_at(self, pos):
        if not self.sim:
            return None
        for k, v in enumerate(self.sim.vehicles):
            for p in v.axle_points():
                sx, sy = self.cam.to_screen(*p)
                if math.hypot(sx - pos[0], sy - pos[1]) < 30:
                    return k
        return None

    def handle_world(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL):
            self.undo()
            return
        if event.type == pygame.MOUSEMOTION:
            self.mouse_world = self.cam.to_world(*event.pos)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and self.mode == "edit":
            self.pending = None
            k = self.beam_at(event.pos)
            if k is not None:
                self.push_undo()
                self.design.remove_beam(k)
            else:
                j = self.joint_at(event.pos)
                if j is not None and j not in self.design.anchors:
                    self.push_undo()
                    self.design.remove_joint(j)
            self.selected = None
            self.dirty = True
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.mode != "edit" or self.tool == "select":
                self._select_at(event.pos)
                return
            if self.tool == "delete":
                k = self.beam_at(event.pos)
                if k is not None:
                    self.push_undo()
                    self.design.remove_beam(k)
                    self.selected = None
                    self.dirty = True
                return
            p = self.snap(*self.cam.to_world(*event.pos))
            if self.pending is None:
                self.pending = p
            else:
                self.try_add(self.pending, p)
                self.pending = p if pygame.key.get_mods() & pygame.KMOD_SHIFT else None
            return
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.pending is not None \
                and self.mode == "edit" and self.tool in ("deck", "beam", "cable"):
            q = self.snap(*self.cam.to_world(*event.pos))
            if q != self.pending:
                self.try_add(self.pending, q)
                self.pending = None

    def _select_at(self, pos):
        v = self.vehicle_at(pos)
        if v is not None:
            self.select(("vehicle", v))
            return
        j = self.joint_at(pos)
        if j is not None:
            self.select(("joint", j))
            return
        k = self.beam_at(pos)
        if k is not None:
            self.select(("beam", k))
            bm = self.design.beams[k]
            if self.mode == "edit":
                self.mat_cycler.options = self._materials_for(bm.kind)
                self.mat_cycler.set(bm.material)
                self.shape_cycler.set(bm.shape)
            return
        self.select(None)

    # --- selection -> calculator -----------------------------------------------------------
    def select(self, sel):
        self.selected = sel
        sliders = []
        if sel and sel[0] == "lab":
            self._build_lab()
            sliders = list(self.lab.items)
        if sel and sel[0] == "beam" and self.mode == "edit":
            bm = self.design.beams[sel[1]]

            def set_area(v, bm=bm):
                bm.A = v / 1e4
                self.dirty = True
            sliders.append(Slider((0, 0, 10, 40), "Cross-section area A (cm^2)", 3, 200, bm.A * 1e4,
                                  set_area, "{:.0f}", log=True))
        title = {None: "Calculator", "beam": "Beam", "joint": "Joint", "vehicle": "Vehicle",
                 "lab": "Hazard lab"}[sel[0] if sel else None]
        if sel and sel[0] in ("beam", "joint"):
            title += f" #{sel[1]}"
        self.drawer.show(title, self.cards(), sliders, tape=self.tape_line())

    def current_result(self):
        if self.mode in ("run", "frozen") and self.sim:
            return self.sim.result
        return self.preview

    def tape_line(self):
        res = self.current_result()
        if not self.selected or res is None:
            return None
        kind, k = self.selected
        if kind == "beam" and k < len(res.members):
            m = res.members[k]
            return f"#{k}: N={m.N/1e3:+.1f}kN s={m.stress/1e6:.1f}MPa {m.ratio*100:.0f}%"
        return None

    def cards(self):
        sel = self.selected
        res = self.current_result()
        if not sel:
            return []
        kind, k = sel
        if kind == "lab":
            return self.lab_cards()
        if kind == "beam":
            if k >= len(self.design.beams):
                return []
            bm = self.design.beams[k]
            mat = MATERIALS[bm.material]
            L = self.design.length(bm)
            I = second_moment(SHAPES.get(bm.shape, SHAPES["I-beam"]), bm.A)
            cards = [Card("Member", f"{bm.material} {bm.kind}, {bm.shape}",
                          f"L = {L:.2f} m, A = {bm.A*1e4:.1f} cm^2, E = {mat.E/1e9:.0f} GPa")]
            if res is None or k >= len(res.members):
                cards.append(Card("Forces", "Turn on TEST or RUN to see forces"))
                return cards
            m = res.members[k]
            state = "TENSION (pulled)" if m.N > 0 else ("COMPRESSION (pushed)" if m.N < 0 else "no load")
            if m.slack:
                state = "SLACK (cable cannot push)"
            cards.append(Card("Axial force from the stiffness solve", "N = (E A / L) x stretch",
                              f"stretch = {m.strain * L * 1000:+.3f} mm",
                              f"N = {m.N/1e3:+.1f} kN  {state}", STATUS[m.status]))
            cards.append(Card("Axial stress", "sigma = N / A",
                              f"= {m.N/1e3:.1f} kN / {bm.A*1e4:.1f} cm^2",
                              f"sigma = {m.stress/1e6:+.1f} MPa"))
            cards.append(Card("Strain", "epsilon = sigma / E", "",
                              f"epsilon = {m.strain*1e6:+.0f} microstrain"))
            if not mat.cable_only:
                cards.append(Card("Euler buckling (only matters when pushed)",
                                  "P_cr = pi^2 E I / (K L)^2",
                                  f"I = {SHAPES.get(bm.shape, SHAPES['I-beam']).factor:.3f} A^2 = "
                                  f"{I*1e8:.0f} cm^4",
                                  f"P_cr = {euler_buckling_load(mat.E, I, 1.0, L)/1e3:.0f} kN"))
            fs = economy.factor_of_safety(m.ratio)
            cards.append(Card("Load ratio", "ratio = |N| / N_limit", m.explanation,
                              f"{m.ratio*100:.0f}% of limit  ->  FS = {fs:.2f}" if m.ratio else "unloaded",
                              STATUS[m.status]))
            return cards
        if kind == "joint":
            if res is None or k >= len(res.loads):
                return [Card("Joint", "Turn on TEST or RUN to see forces")]
            fx = fy = 0.0
            lines = []
            for (n, mi, f_x, f_y) in res.node_forces:
                if n == k:
                    lines.append(f"beam {mi}: ({f_x/1e3:+.1f}, {f_y/1e3:+.1f}) kN")
                    fx += f_x
                    fy += f_y
            lx, ly = res.loads[k]
            rx, ry = res.reactions[k]
            lines.append(f"loads: ({lx/1e3:+.1f}, {ly/1e3:+.1f}) kN")
            if rx or ry:
                lines.append(f"support: ({rx/1e3:+.1f}, {ry/1e3:+.1f}) kN")
            sx, sy = fx + lx + rx, fy + ly + ry
            return [Card("Method of joints", "Sum Fx = 0,  Sum Fy = 0", "\n".join(lines[:9]),
                         f"Sum Fx = {sx/1e3:+.2f} kN, Sum Fy = {sy/1e3:+.2f} kN", GOOD),
                    Card("Why it balances", "Newton's 3rd law",
                         "Each beam pulls/pushes this joint exactly as hard as the joint pulls/pushes "
                         "the beam. If the sum were not zero the joint would accelerate.")]
        if kind == "vehicle" and self.sim:
            v = self.sim.vehicles[k]
            f = v.forces
            return [Card("Motion", "F_net = m a", f"m = {v.spec.mass/1e3:.1f} t",
                         f"v = {v.v:.1f} m/s ({v.v*3.6:.0f} km/h), a = {v.acceleration:+.2f} m/s^2"),
                    Card("Forces along the road", "F = T - F_rr - F_drag - m g sin(theta)",
                         f"T = {f.traction/1e3:.1f} kN, F_rr = {-f.rolling/1e3:.2f} kN, "
                         f"drag = {-f.drag/1e3:.2f} kN, gravity = {f.gravity/1e3:+.2f} kN"),
                    Card("Momentum & energy", "p = m v,  KE = 1/2 m v^2",
                         f"p = {v.momentum/1e3:.0f} kN s", f"KE = {v.kinetic_energy/1e3:.0f} kJ"),
                    Card("Axle loads on the deck", "P = m g / axles", "",
                         f"{v.axle_load()/1e3:.1f} kN on each of {v.spec.axles} axles")]
        return []

    def lab_cards(self):
        d = self.design
        cards = []
        sim = self.sim or self._preview_sim
        if sim is None:
            return [Card("Hazard lab", "Finish a connected, stable bridge first",
                         self.preview_error or "Build a deck from bank to bank with triangles.")]
        if sim.wind:
            w = sim.wind_summary()
            tune, zeta = den_hartog_optimum(d.tmd_mass_ratio)
            cards += [
                Card("Natural frequency (Rayleigh)", "f_n = (1/2 pi) sqrt(k / m)",
                     f"k* = {w['K']/1e6:.2f} MN/m, m* = {w['M']/1e3:.1f} t", f"f_n = {w['f_n']:.2f} Hz"),
                Card("Vortex shedding", "f_v = St U / D", f"St = 0.12, D = {sim.deck_depth:.1f} m (deck)",
                     f"now: U = {sim.wind_U:.1f} m/s -> f_v = {sim.wind_fv:.2f} Hz"),
                Card("Danger wind speed", "U_crit = f_n D / St", "",
                     f"U_crit = {w['U_crit']:.1f} m/s  (wind reaches {self.cfg['wind']['u_end']:.0f})",
                     BAD if w['U_crit'] < self.cfg['wind']['u_end'] * 1.25 else GOOD),
                Card("Best TMD tuning (Den Hartog)", "f_tmd/f_n = 1/(1+mu), zeta = sqrt(3mu/8(1+mu)^3)",
                     f"mu = {d.tmd_mass_ratio:.3f}", f"tune {tune:.2f}, zeta {zeta:.2f}"),
            ]
            if self.sim:
                cards.append(Card("Swing right now", "F_eq = k* x", "",
                                  f"{sim.dynamic_load()/1e3:.0f} kN extra load"))
        if sim.quake:
            q = self.cfg["quake"]
            cards += [
                Card("Lateral period (Rayleigh)", "T = 2 pi sqrt(sum m u^2 / sum F u)", "",
                     f"T = {sim.T_struct:.2f} s  ->  with bearings {q['T_iso']:.1f} s"),
                Card("Spectral coefficient", "C(T): 2.5 for stiff, 2.5 x 0.5/T for long periods", "",
                     f"C = {sim.C:.2f}  (fixed {spectral_coefficient(sim.T_struct):.2f}, isolated "
                     f"{spectral_coefficient(q['T_iso']):.2f})"),
                Card("Base shear at peak", "V_base = C M a_g",
                     f"M = {sim.total_mass/1e3:.0f} t, a = {q['A_peak']:.2f} m/s^2",
                     f"V = {sim.C*sim.total_mass*q['A_peak']/1e3:.0f} kN"),
                Card("Deck drift if isolated", "d = C a / omega^2",
                     f"omega = 2 pi / {q['T_iso']:.1f} s",
                     f"d = {spectral_coefficient(q['T_iso'])*q['A_peak']/(2*math.pi/q['T_iso'])**2:.2f} m "
                     f"vs joint gap {q['joint_gap'] if d.flex_joints else q['gap']:.2f} m"),
            ]
        if sim.grid_power:
            cards += [
                Card("Smart grid budget", "P_total = P_pod + P_alloy",
                     f"pod {sim.spec.power/1e6:.1f} MW, alloy {sim.alloy_t:.1f} t x 50 kW/t = "
                     f"{sim.alloy_demand/1e6:.2f} MW",
                     f"capacity {d.grid_mw:.1f} MW -> pod gets {sim.power_factor*100:.0f}%",
                     GOOD if sim.power_factor >= 1 else WARN),
                Card("Maglev thrust", "T = min(P / v, T_max)", "no wheels: no rolling resistance",
                     f"T_max = {sim.spec.max_thrust/1e3:.0f} kN"),
            ]
        return cards

    # --- running ---------------------------------------------------------------------------
    def toggle_run(self):
        if self.overlay is not None:
            return
        if self.mode == "edit":
            self.start_run()
        else:
            self.stop_run()

    def start_run(self):
        try:
            self.sim = BridgeSim(self.design, self.cfg)
        except UnstableStructure as e:
            self.fail(FailureReport("unstable", "THE FRAME FOLDS UP", str(e),
                                    ["A pin-jointed square can lean over like a parallelogram. "
                                     "Triangles cannot."], 0.0))
            return
        except ValueError as e:
            self.say(str(e), 4)
            return
        self.mode = "run"
        self.run_btn.label = "STOP"
        self.pending = None
        sound.play("whoosh")
        if self.selected:
            self.select(self.selected)

    def stop_run(self):
        self.mode = "edit"
        self.sim = None
        self.run_btn.label = "RUN"
        self.cam.shake = 0
        self.dirty = True

    def reset_after_failure(self):
        self.stop_run()
        self.debris = None

    def take_alternate(self, report):
        # The wreckage settles in the valley and becomes the base of a low route
        self.debris = []
        for bm in self.design.beams:
            (x0, y0), (x1, y1) = self.design.joints[bm.a], self.design.joints[bm.b]
            mx = (x0 + x1) / 2
            if self.cfg["left_x"] < mx < self.cfg["right_x"]:
                L = min(math.hypot(x1 - x0, y1 - y0), 6) / 2
                gy = self.cfg["ground_y"] + 0.3
                self.debris.append(((mx - L, gy), (mx + L, gy + 0.4)))
        super().take_alternate(report)

    def update_world(self, dt):
        self.tick += 1
        if self.mode == "edit" and self.dirty:
            self.dirty = False
            self._refresh_preview()
        if self.mode == "run" and self.sim:
            for _ in range(self.speed):
                self.sim.step(min(dt, 1 / 30))
                if self.sim.failure or self.sim.done:
                    break
            for name, _ in self.sim.events:
                sound.play({"creak": "creak", "groan": "groan", "quake": "whoosh"}.get(name, name))
            self.sim.events.clear()
            self.cam.shake = self.sim.ground_x * self.cam.scale * 6 if self.sim.quake else 0
            if self.sim.failure:
                self.mode = "frozen"
                self.run_btn.label = "EDIT"
                rep = self.sim.failure
                rep.build_cost = self.cost()
                self.fail(rep)
            elif self.sim.done:
                self.mode = "frozen"
                self.run_btn.label = "EDIT"
                self._finish()
        if self.selected:
            self.drawer.update_cards(self.cards())

    def _refresh_preview(self):
        self.preview = None
        self.preview_error = ""
        self._preview_sim = None
        if not self.design.beams:
            return
        if deck_path(self.design, self.cfg) is None:
            self.preview_error = "Road not connected yet (build DECK from bank to bank)"
            return
        try:
            sim = BridgeSim(self.design, self.cfg)
            self._preview_sim = sim
            if self.preview_on:
                self.preview = sim.worst_preview()
        except UnstableStructure:
            self.preview_error = "Wobbly! Add triangles (diagonals) so it cannot fold"
        except ValueError as e:
            self.preview_error = str(e)

    def _finish(self):
        sim = self.sim
        cost = self.cost()
        fs = sim.factor_of_safety
        revenue = 1.6 * self.level.par_cost * sim.toll_ratio()
        cb = design_cost(self.design, self.cfg)
        actual, ideal = sim.toll_numbers()
        lines = [("Toll = (t x km)/(h x L)", f"{100 * actual / ideal:.0f}% of an ideal flat, full-speed crossing", None),
                 ("Carbon footprint", f"{cb.carbon_kg/1000:.1f} t CO2", None),
                 ("Worst member load", f"{sim.max_ratio*100:.0f}%", None),
                 ("Time", f"{sim.time:.1f} s", None)]
        if sim.wind:
            lines.append(("Wind: f_n / U_crit", f"{sim.f_n:.2f} Hz / {sim.U_crit:.1f} m/s", None))
        if sim.quake:
            lines.append(("Quake: T / C", f"{sim.T:.2f} s / {sim.C:.2f}", None))
        self.succeed(cost, min(100.0, 50 * fs), sim.time, fs=fs, lines=lines, revenue=revenue)

    # --- drawing ---------------------------------------------------------------------------
    def joint_pos(self, k, result=None):
        x, y = self.design.joints[k]
        if result is not None and self.deflect and k < len(result.displacements):
            ux, uy = result.displacements[k]
            x += ux * self.deflect
            y += uy * self.deflect
        return self.cam.to_screen(x, y)

    def draw_terrain(self, s):
        c, cam = self.cfg, self.cam
        v = c["view"]
        def rect(x0, y0, x1, y1, col, edge=True):
            a = cam.to_screen(x0, y1)
            b = cam.to_screen(x1, y0)
            r = pygame.Rect(a, (b[0] - a[0], b[1] - a[1]))
            pygame.draw.rect(s, col, r)
            if edge:
                pygame.draw.rect(s, ROCK_EDGE, r, 1)
        if c.get("water_y") is not None:
            rect(c["left_x"], c["ground_y"], c["right_x"], c["water_y"], WATER, False)
            for k in range(int(c["left_x"]), int(c["right_x"]), 3):
                off = ((self.tick // 6) + k) % 3 * 0.4
                p = cam.to_screen(k + off, c["water_y"] - 0.4)
                q = cam.to_screen(k + off + 1.2, c["water_y"] - 0.4)
                pygame.draw.line(s, (120, 180, 240), p, q, 2)
        rect(v[0], v[1], c["left_x"], c["deck_y"], ROCK)
        rect(c["right_x"], v[1], v[2], c["deck_y"], ROCK)
        rect(c["left_x"], v[1], c["right_x"], c["ground_y"], ROCK)
        for a, b in c.get("islands", []):
            rect(a, c["ground_y"], b, c["extra_anchor_y"], ROCK)
        # approach roads
        for x0, x1 in ((v[0], c["left_x"]), (c["right_x"], v[2])):
            pygame.draw.line(s, (60, 64, 72), cam.to_screen(x0, c["deck_y"]), cam.to_screen(x1, c["deck_y"]), 6)
        if self.debris:
            pts = [cam.to_screen(c["left_x"], c["ground_y"]), cam.to_screen(c["left_x"] + 3, c["ground_y"] + 2.2),
                   cam.to_screen(c["right_x"] - 3, c["ground_y"] + 2.2), cam.to_screen(c["right_x"], c["ground_y"])]
            pygame.draw.polygon(s, (120, 96, 64), pts)
            for (a, b) in self.debris:
                pygame.draw.line(s, (150, 150, 150), cam.to_screen(*a), cam.to_screen(*b), 4)

    def draw_world(self, s):
        blueprint_background(s, (0, TOP_BAR, WIDTH, HEIGHT - TOP_BAR - BOTTOM_BAR),
                             step=max(8, int(self.cfg["grid"] * self.cam.scale)))
        self.draw_terrain(s)
        cam = self.cam
        res = self.current_result()
        if self.mode == "edit":
            g = self.cfg["grid"]
            v = self.cfg["view"]
            x = v[0]
            while x <= v[2] + 1e-6:
                y = v[1]
                while y <= v[3] + 1e-6:
                    if not self.solid(x, y):
                        pygame.draw.circle(s, (70, 100, 150), cam.to_screen(x, y), 1)
                    y += g
                x += g
        # anchors
        for k, kind in self.design.anchors.items():
            p = self.joint_pos(k)
            pygame.draw.polygon(s, ACCENT, [p, (p[0] - 9, p[1] + 14), (p[0] + 9, p[1] + 14)], 0 if kind == "pin" else 2)
            if kind == "roller":
                pygame.draw.circle(s, ACCENT, (p[0] - 5, p[1] + 18), 3)
                pygame.draw.circle(s, ACCENT, (p[0] + 5, p[1] + 18), 3)
        # beams
        flash = (self.tick // 8) % 2
        for k, bm in enumerate(self.design.beams):
            a = self.joint_pos(bm.a, res)
            b = self.joint_pos(bm.b, res)
            mat = MATERIALS[bm.material]
            w = max(2, min(11, int(3 + 2 * math.log2(max(bm.A, 1e-4) / 0.001))))
            if bm.kind == "cable":
                w = max(2, w - 2)
            col = mat.colour
            if res is not None and k < len(res.members):
                mr = res.members[k]
                col = STATUS[mr.status]
                if mr.slack:
                    col = (110, 120, 135)
                if mr.status == FAILED and flash:
                    col = (255, 255, 255)
            if bm.kind == "deck":
                pygame.draw.line(s, (25, 25, 30), a, b, w + 6)
            if self.selected == ("beam", k):
                pygame.draw.line(s, ACCENT, a, b, w + 8)
            pygame.draw.line(s, col, a, b, w)
        for k in range(len(self.design.joints)):
            if k in self.design.anchors and not any(k in (b.a, b.b) for b in self.design.beams):
                continue
            p = self.joint_pos(k, res)
            pygame.draw.circle(s, (235, 240, 250), p, 4)
            if self.selected == ("joint", k):
                pygame.draw.circle(s, ACCENT, p, 9, 2)
        # pending beam
        if self.mode == "edit" and self.pending and self.mouse_world:
            q = self.snap(*self.mouse_world)
            a, b = cam.to_screen(*self.pending), cam.to_screen(*q)
            L = math.hypot(q[0] - self.pending[0], q[1] - self.pending[1])
            limit = self.cfg.get("max_cable", 0) if self.tool == "cable" else self.cfg.get("max_beam", 8)
            ok = L <= limit + 1e-6 and not self.solid(*q)
            pygame.draw.line(s, ACCENT if ok else BAD, a, b, 3)
            mat, A, shape = self._style()
            c, _ = economy.member_material_cost(MATERIALS[mat], A, L)
            ang = math.degrees(math.atan2(q[1] - self.pending[1], q[0] - self.pending[0]))
            text(s, f"{L:.1f} m  {ang:+.0f} deg  ~{economy.format_rs(c + 6500)}", (b[0] + 12, b[1] - 22),
                 14, ACCENT if ok else BAD)
        if self.sim and self.mode in ("run", "frozen"):
            self.draw_vehicles(s)
            self.draw_hazards(s)
        if self.vectors and res is not None:
            self.draw_vectors(s, res)
        self.draw_hud(s, res)

    def draw_vehicles(self, s):
        for veh in self.sim.vehicles:
            pts = veh.axle_points()
            front = self.cam.to_screen(*veh.path.point_at(veh.s))
            rear = self.cam.to_screen(*veh.path.point_at(veh.s - veh.spec.length))
            dx, dy = front[0] - rear[0], front[1] - rear[1]
            L = math.hypot(dx, dy) or 1
            nx, ny = dy / L, -dx / L
            h = 1.8 * self.cam.scale if veh.spec.maglev else 2.4 * self.cam.scale
            lift = 0.5 * self.cam.scale if veh.spec.maglev else 0.6 * self.cam.scale
            body = [(rear[0] + nx * lift, rear[1] + ny * lift), (front[0] + nx * lift, front[1] + ny * lift),
                    (front[0] + nx * (lift + h), front[1] + ny * (lift + h)),
                    (rear[0] + nx * (lift + h), rear[1] + ny * (lift + h))]
            colour = {"van": (240, 140, 60), "bus": (240, 200, 60), "truck": (200, 90, 70),
                      "maglev": (230, 240, 255)}.get(self.cfg["vehicle"]["kind"], ACCENT)
            pygame.draw.polygon(s, colour, body)
            pygame.draw.polygon(s, (20, 20, 30), body, 2)
            if not veh.spec.maglev:
                for p in pts:
                    pygame.draw.circle(s, (20, 20, 25), self.cam.to_screen(*p), max(3, int(0.45 * self.cam.scale)))
            if self.vectors:
                c = self.cam.to_screen(*veh.path.point_at(veh.centre_s()))
                arrow(s, GOOD, c, (c[0] + veh.v * 3, c[1]), 3)

    def draw_hazards(self, s):
        sim = self.sim
        if sim.wind:
            n = 18
            for k in range(n):
                y = self.cfg["view"][1] + (k + 0.5) * (self.cfg["view"][3] - self.cfg["view"][1]) / n
                x = (self.tick * sim.wind_U * 0.05 + k * 7.3) % (self.cfg["view"][2] - self.cfg["view"][0])
                a = self.cam.to_screen(self.cfg["view"][0] + x, y)
                pygame.draw.line(s, (150, 190, 230), a, (a[0] + int(sim.wind_U * 1.5), a[1]), 1)
            if self.design.tmd:
                k = sim.u_ref_node
                p = self.joint_pos(k, sim.result)
                off = int((sim.osc.x2 - sim.osc.x) * self.cam.scale * 20)
                pygame.draw.line(s, MUTED, p, (p[0], p[1] + 30 + off), 2)
                pygame.draw.rect(s, CYAN, (p[0] - 10, p[1] + 30 + off, 20, 14))
        if sim.quake and sim.design.isolation:
            text(s, f"deck drift {sim.deck_drift*100:+.0f} cm", self.cam.to_screen(self.cfg["left_x"], 3),
                 14, WARN)

    def draw_vectors(self, s, res):
        scale = 30 / max(1.0, max((abs(r) for r in res.reactions.flatten()), default=1.0))
        for k in range(len(self.design.joints)):
            rx, ry = res.reactions[k]
            if rx or ry:
                p = self.joint_pos(k, res)
                arrow(s, CYAN, p, (p[0] + rx * scale * 2, p[1] - ry * scale * 2), 3)
                text(s, f"{math.hypot(rx, ry)/1e3:.0f} kN", (p[0] + 6, p[1] + 16), 13, CYAN)
            lx, ly = res.loads[k]
            if self.sim and (abs(ly) > 1 or abs(lx) > 1) and k not in self.design.anchors:
                p = self.joint_pos(k, res)
                arrow(s, BAD, p, (p[0] + lx * scale * 2, p[1] - ly * scale * 2), 2, 7)
        if self.selected and self.selected[0] == "joint":
            j = self.selected[1]
            p = self.joint_pos(j, res)
            for (n, mi, fx, fy) in res.node_forces:
                if n == j:
                    arrow(s, ACCENT, p, (p[0] + fx * scale * 2, p[1] - fy * scale * 2), 3)
        if self.selected and self.selected[0] == "beam" and self.selected[1] < len(res.members):
            mi = self.selected[1]
            for (n, m2, fx, fy) in res.node_forces:
                if m2 == mi:
                    p = self.joint_pos(n, res)
                    arrow(s, ACCENT, p, (p[0] + fx * scale * 2, p[1] - fy * scale * 2), 3)

    def draw_hud(self, s, res):
        x, y = 16, TOP_BAR + 10
        lines = []
        if self.mode == "edit":
            if self.preview_error:
                lines.append((self.preview_error, WARN))
            elif res is not None:
                fs = economy.factor_of_safety(res.max_ratio)
                g, _ = economy.fs_grade(fs)
                lines.append((f"TEST: worst member {res.max_ratio*100:.0f}% -> FS {fs:.2f} ({g})",
                              GOOD if res.max_ratio < 0.67 else (WARN if res.max_ratio <= 1 else BAD)))
            else:
                lines.append(("Build DECK across the gap, then add triangles above or below.", MUTED))
        elif self.sim:
            sim = self.sim
            lines.append((f"t = {sim.time:5.1f} s   worst member now {res.max_ratio*100:3.0f}%   "
                          f"max so far {sim.max_ratio*100:.0f}%", TEXT))
            if sim.wind:
                lines.append((f"wind U = {sim.wind_U:4.1f} m/s   f_v = {sim.wind_fv:.2f} Hz   "
                              f"f_n = {sim.f_n:.2f} Hz   swing load {sim.dynamic_load()/1e3:.0f} kN",
                              BAD if abs(sim.wind_fv - sim.f_n) / sim.f_n < 0.25 else CYAN))
            if sim.quake:
                lines.append((f"ground a = {sim.a_g:+.2f} m/s^2   C = {sim.C:.2f}   "
                              f"V_base = {abs(sim.C*sim.total_mass*sim.a_g)/1e3:.0f} kN", WARN))
            if sim.grid_power:
                lines.append((f"grid {self.design.grid_mw:.1f} MW: pod power {sim.power_factor*100:.0f}%   "
                              f"limit {self.cfg['time_limit']:.1f} s", CYAN))
        for k, (t, c) in enumerate(lines):
            text(s, t, (x, y + k * 20), 15, c)
        if self.sim and self.mode in ("run", "frozen"):
            hist = self.sim.history
            series = [hist["max load %"]]
            cols = [BAD]
            for name in ("wind m/s", "ground a (m/s2)"):
                if name in hist:
                    series.append(hist[name])
                    cols.append(CYAN)
            mini_chart(s, (16, TOP_BAR + 80, 300, 110), series, cols, "load % (red) over time",
                       limit=100)
