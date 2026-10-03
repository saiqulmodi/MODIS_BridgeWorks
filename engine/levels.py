"""The 10-level campaign (Prompt 9). Pure data - each scene reads its own `cfg`."""
from dataclasses import dataclass, field


@dataclass
class Level:
    num: int
    title: str
    tier: str
    scene: str                  # bridge / rail / cantilever / signals / traffic / logistics
    mission: str
    context: str
    budget: float
    par_cost: float
    materials: list
    formulas: list              # [(formula, how you discover it while playing)]
    paths: list                 # [(name, description)]  - the "two paths forward"
    success: str
    bonus: str
    alternate: dict = None      # Prompt 6 alternate route: name, text, cost_factor
    cfg: dict = field(default_factory=dict)


LEVELS = [
    Level(
        1, "The Creek Crossing", "Tier 1: Foundations", "bridge",
        "The bakery van must reach the village across Pebble Creek every morning. Build a "
        "road bridge across the 16 m gap.",
        "Truss bridges like the old railway crossings of the 1800s use triangles because a "
        "triangle cannot change shape without changing the length of a side.",
        budget=250000, par_cost=100000, materials=["Timber", "Steel"],
        formulas=[
            ("Sum Fx = 0, Sum Fy = 0", "Click any joint: all the arrows pulling on it always add "
                                       "up to zero, or it would move."),
            ("sigma = N / A", "Click a beam and slide its area A: the stress drops as A grows."),
            ("Tension vs compression", "Top chords go blue-ish (pushed), bottom chords pull. "
                                       "Swap them and watch which ones buckle."),
            ("Centre of mass", "The van's weight moves along the deck - the worst moment is when "
                               "it is in the middle."),
        ],
        paths=[("Low cost, high skill", "A light timber Warren truss of perfect triangles."),
               ("High cost, robust", "Chunky steel members everywhere - safe but pricey.")],
        success="The van (3.5 t) crosses and the bridge stands.",
        bonus="Factor of safety between 1.5 and 4 (not wasteful).",
        alternate=dict(name="Debris ford", cost_factor=0.5,
                       text="Pile the fallen pieces into a low ford across the creek. Vans "
                            "splash across slowly - half price, but it floods in the rains."),
        cfg=dict(left_x=12, right_x=28, deck_y=0.0, ground_y=-6.0, water_y=-4.0,
                 anchors=[(12, 0, "pin"), (12, -3, "pin"), (28, 0, "pin"), (28, -3, "pin")],
                 extra_anchor_xs=[], grid=1.0, view=(0, -9, 40, 14),
                 vehicle=dict(kind="van", mass=3500, power=60e3, length=5, axles=2,
                              speed=12.0, count=1, C_rr=0.012, mu=0.7),
                 deck_load=1500.0, wind=None, quake=None, humid=False,
                 max_beam=8.0, max_cable=0.0, time_limit=None),
    ),
    Level(
        2, "The Timber Incline", "Tier 2: Rail & Gradients", "rail",
        "Haul 120 t of logs from the valley sawmill up to the ridge-top timber yard on a "
        "narrow-gauge railway.",
        "Mountain railways are limited by adhesion: steel wheels on steel rails grip only "
        "about 30% of the weight resting on the driving wheels.",
        budget=1200000, par_cost=800000, materials=["Timber"],
        formulas=[
            ("F = m g sin(theta)", "Drag a track handle steeper: the red gravity arrow grows."),
            ("N = m g cos(theta)", "The grip (adhesion) depends on the weight pressing down."),
            ("F_grip = mu N", "Too many wagons and the wheels spin: the engine cannot pull more "
                              "than mu times its own weight."),
            ("Tractive effort T = min(P/v, mu N)", "Watch the engine's pull fall as speed rises."),
        ],
        paths=[("Low cost, high skill", "Small engine, fewer wagons per trip, more trips."),
               ("High cost, robust", "Hire a banker (pusher) engine and haul everything at once.")],
        success="Deliver 120 t to the ridge yard within 2 minutes without stalling.",
        bonus="Spend less than the par cost.",
        alternate=dict(name="Cable winch", cost_factor=0.6,
                       text="Rig a winch at the top and drag wagons up the slope one at a time - "
                            "slow, but it never stalls."),
        cfg=dict(ground=[(0, 0), (20, 0), (80, 8), (120, 8)], x_end=120,
                 stations=list(range(0, 121, 10)), fixed_ends=((0, 10), (110, 120)),
                 start_x=10, end_x=110, cargo_target=120.0, time_limit=120.0, wet=False,
                 locos=["Tank engine", "Diesel shunter"], banker=True, brake_marker=False,
                 wagon_load=30000.0, wagon_tare=15000.0, max_wagons=6, track_rs_m=3000.0,
                 cut_rs_m2=2500.0, fill_rs_m2=2000.0, view=(-5, -10, 125, 25)),
    ),
    Level(
        3, "The Deep Canyon Pier", "Tier 2: Rail & Gradients", "cantilever",
        "Span the 66 m Raven Canyon with a concrete girder built outward from two tall piers - "
        "no scaffolding can reach the canyon floor.",
        "Balanced-cantilever bridges grow like a see-saw: a segment on one side must be "
        "matched on the other, or the pier tips over.",
        budget=9500000, par_cost=7600000, materials=["Concrete"],
        formulas=[
            ("Sum M_pier = Sum W_right x - Sum W_left x", "The see-saw meter swings each time you "
                                                         "cast a segment."),
            ("sigma = M y / I", "The pier root feels the biggest bending moment."),
            ("I = b d^3 / 12", "Double the haunch depth d and the girder gets 8x stiffer."),
            ("tau = V Q / (I t)", "Shear is largest next to the supports."),
            ("Continuous beam", "Stitching the middle changes cantilevers into one beam: watch "
                                "the moment diagram flip."),
        ],
        paths=[("Low cost, high skill", "Perfectly alternate segments, slim haunch, light post-tensioning."),
               ("High cost, robust", "Deep haunch, tie-downs on both piers, heavy post-tensioning.")],
        success="Both piers stand, the stitch is closed, and a 40 t truck crosses.",
        bonus="Girder factor of safety between 1.5 and 4 under the truck.",
        alternate=dict(name="Steel launch girder", cost_factor=0.7,
                       text="Re-use the formwork travellers as a temporary steel launching truss "
                            "to finish the span the slow way."),
        cfg=dict(view=(-4, -30, 70, 6)),
    ),
    Level(
        4, "Freight Mountain Pass", "Tier 2: Rail & Gradients", "rail",
        "Move 600 t of copper ore over Eagle Pass to the smelter terminal. Rain is forecast "
        "on the far side of the summit.",
        "Heavy trains carry enormous momentum p = m v. Climbing turns it into height; "
        "descending, the brakes must turn it all into heat.",
        budget=4000000, par_cost=3000000, materials=["Steel"],
        formulas=[
            ("p = m v", "Momentum carries the train over a short steep crest."),
            ("KE = 1/2 m v^2, PE = m g h", "The energy bars swap as the train climbs and descends."),
            ("d_stop = v^2 / (2 (mu g cos(theta) - g sin(theta)))", "Move the brake marker: "
                "too late on wet rails and you hit the buffers."),
            ("Runaway when g sin(theta) > mu g cos(theta)", "Make a descent too steep and no "
                                                             "brake can hold the train."),
        ],
        paths=[("Low cost, high skill", "One locomotive, smart grades, careful braking point."),
               ("High cost, robust", "Double-header locomotives and expensive gentle earthworks.")],
        success="Deliver 600 t to the terminal within 8 minutes and stop before the buffers.",
        bonus="Stop within 15 m of the stop line.",
        alternate=dict(name="Bypass spur", cost_factor=0.5,
                       text="Lay a short spur at the bottom of the descent so a runaway train "
                            "can coast safely uphill to a stop."),
        cfg=dict(ground=[(0, 0), (30, 0), (220, 12), (250, 12), (390, 0), (460, 0)], x_end=460,
                 stations=list(range(0, 461, 20)), fixed_ends=((0, 20), (400, 460)),
                 start_x=20, end_x=430, stop_x=420, buffer_x=445, cargo_target=600.0,
                 time_limit=480.0, wet_after_x=240, locos=["Mainline diesel", "Double-header"],
                 banker=False, brake_marker=True, wagon_load=60000.0, wagon_tare=22000.0,
                 max_wagons=12, track_rs_m=3000.0, cut_rs_m2=9000.0, fill_rs_m2=7000.0,
                 view=(-10, -15, 470, 30)),
    ),
    Level(
        5, "The Harbor Switchyard", "Tier 3: Flow & Signalling", "signals",
        "Passenger and cargo trains share one single-track bridge into Port Kavi. Cargo must "
        "go to the harbor siding, passengers to the main line - and nobody may meet head-on.",
        "Real railways divide track into blocks with signals; interlocking logic stops two "
        "trains ever being given conflicting routes.",
        budget=3000000, par_cost=1500000, materials=[],
        formulas=[
            ("d_stop = v^2 / (2 mu g)", "Place a signal too close to the next one and a fast "
                                        "train sails past the red (SPAD)."),
            ("3-aspect: RED / YELLOW / GREEN", "Watch aspects ripple back behind every train."),
            ("Logic gates AND / OR / NOT", "Wire PERMIT_EB = APPR_EB AND NOT BRIDGE_OCC AND NOT "
                                           "PERMIT_WB to lock out head-on moves."),
            ("Headway", "More, shorter blocks let trains follow closer - if they can still stop."),
        ],
        paths=[("Low cost, high skill", "Few, well-spaced 3-aspect signals and tight logic."),
               ("High cost, robust", "Many 4-aspect signals for short blocks and high capacity.")],
        success="Run 12 minutes with no collision, derailment or crossing incident, deliver at "
                "least 10 trains and send every cargo train to the harbor.",
        bonus="Zero SPADs and total waiting under 1000 train-seconds.",
        alternate=dict(name="Cable ferry", cost_factor=0.4,
                       text="Run cargo wagons across the bay on a cable ferry instead of the "
                            "bridge - slower, but it frees the single track for passengers."),
        cfg=dict(signal_cost=300000, signal_cost_4=450000, term_cost=50000, target=10),
    ),
    Level(
        6, "Urban Bottleneck", "Tier 3: Flow & Signalling", "traffic",
        "Rush hour at Gandhi Chowk: the main road and the market street cross at one "
        "junction. Keep the city moving.",
        "Traffic behaves like a fluid: flow q = k v rises with density k until a critical "
        "point, then collapses into a jam that travels backwards.",
        budget=5000000, par_cost=1500000, materials=[],
        formulas=[
            ("q = k v", "The fundamental diagram plots every detector reading live."),
            ("v = v_max (1 - k / k_jam)", "Greenshields: speed falls as cars pack closer."),
            ("k_crit = k_jam / 2, q_max = v_max k_jam / 4", "Push demand past q_max and a queue "
                                                           "is born."),
            ("w = (q2 - q1) / (k2 - k1)", "Watch the red shockwave crawl backwards in the heat map."),
            ("IDM car-following", "Each car keeps a safe time gap T = 1.2 s to the one ahead."),
        ],
        paths=[("Low cost, high skill", "Tune signal cycle and green split, or merge with a roundabout."),
               ("High cost, robust", "Build a grade-separated overpass: no conflict at all.")],
        success="12 minutes of rush hour without gridlock, main-road trips no more than 1.8x "
                "the free-flow time.",
        bonus="Idling under 4000 car-seconds (less pollution).",
        alternate=dict(name="Bypass lane", cost_factor=0.5,
                       text="Open a temporary bypass through the bus depot to drain the queue."),
        cfg=dict(cost=dict(signals=400000, roundabout=1200000, overpass=4500000),
                 max_delay=1.8, idle_bonus=4000.0),
    ),
    Level(
        7, "Gale-Force Gorge", "Tier 4: Dynamic Systems", "bridge",
        "Build a 48 m bus bridge across Whistling Gorge, where the wind builds from a breeze "
        "to a 36 m/s gale every afternoon.",
        "In 1940 the Tacoma Narrows Bridge twisted itself apart in a 19 m/s wind because "
        "the wind pushed it in time with its own natural swing.",
        budget=3500000, par_cost=2200000, materials=["Timber", "Steel", "Steel cable"],
        formulas=[
            ("f_n = (1/2 pi) sqrt(k / m)", "Stiffer (bigger k) or lighter (smaller m) raises the "
                                           "natural frequency."),
            ("f_v = St U / D", "Vortices peel off the deck faster as the wind speeds up."),
            ("U_crit = f_n D / St", "The calculator predicts the wind speed where they match."),
            ("Tuned mass damper", "Slide its mass and tuning until the swing dies away."),
        ],
        paths=[("Low cost, high skill", "A light bridge plus a well-tuned mass damper or fairings."),
               ("High cost, robust", "A deep, stiff truss whose natural frequency stays above "
                                     "anything the wind can excite.")],
        success="Four buses cross while the wind sweeps from 4 to 36 m/s, and the bridge survives.",
        bonus="Factor of safety between 1.5 and 4.",
        alternate=dict(name="Cable car", cost_factor=0.5,
                       text="String a cable car across the gorge from the surviving towers."),
        cfg=dict(left_x=6, right_x=54, deck_y=0.0, ground_y=-14.0, water_y=-12.0,
                 anchors=[(6, 0, "pin"), (6, -4, "pin"), (54, 0, "pin"), (54, -4, "pin")],
                 extra_anchor_xs=[], grid=2.0, view=(0, -16, 60, 16),
                 vehicle=dict(kind="bus", mass=12000, power=200e3, length=11, axles=2,
                              speed=14.0, count=4, spacing=16.0, C_rr=0.012, mu=0.7),
                 deck_load=12000.0, deck_depth=1.2, humid=False,
                 wind=dict(u_start=4.0, u_end=36.0, ramp=60.0, gust=1.5, duration=70.0),
                 quake=None, max_beam=10.0, max_cable=60.0, time_limit=None),
    ),
    Level(
        8, "Earthquake Fault Viaduct", "Tier 4: Dynamic Systems", "bridge",
        "A highway viaduct must cross the Kutch fault valley. A magnitude-7 tremor is "
        "expected while traffic is on the bridge.",
        "Modern bridges in earthquake zones often sit on rubber-and-lead isolation bearings "
        "that let the ground move underneath while the deck glides.",
        budget=3000000, par_cost=1500000, materials=["Timber", "Steel", "Concrete"],
        formulas=[
            ("a_g(t) = A sin(omega t) e^(-decay t)", "The seismograph trace shows the pulse."),
            ("V_base = C M a_g", "Heavier bridges and stiff (short-period) bridges feel more force."),
            ("T = 2 pi sqrt(M / k)", "Isolation bearings lengthen T and drop C from 2.5 to 0.5."),
            ("Displacement = C a / omega^2", "...but the deck now swings further - add flexible joints."),
        ],
        paths=[("Low cost, high skill", "Slender piers on isolation bearings with flexible joints."),
               ("High cost, robust", "Massive X-braced steel piers that resist the full shaking.")],
        success="A 20 t truck crosses during the earthquake and the viaduct stands.",
        bonus="Factor of safety between 1.5 and 4.",
        alternate=dict(name="Ground-level road", cost_factor=0.5,
                       text="Grade a winding road down into the valley across the debris."),
        cfg=dict(left_x=6, right_x=46, deck_y=0.0, ground_y=-12.0, water_y=None,
                 anchors=[(6, 0, "roller"), (6, -3, "roller"), (46, 0, "roller"), (46, -3, "roller")],
                 extra_anchor_xs=list(range(10, 43, 4)), extra_anchor_y=-12.0,
                 grid=2.0, view=(0, -15, 52, 10),
                 vehicle=dict(kind="truck", mass=20000, power=250e3, length=10, axles=3,
                              speed=10.0, count=1, C_rr=0.012, mu=0.7),
                 deck_load=3000.0, humid=False, wind=None,
                 quake=dict(A_peak=0.35 * 9.81, f=1.5, decay=0.35, start_frac=0.35,
                            duration=12.0, gap=0.05, joint_gap=0.40, T_iso=2.5),
                 max_beam=8.0, max_cable=0.0, time_limit=None),
    ),
    Level(
        9, "Heavy Industrial Corridor", "Tier 4: Dynamic Systems", "logistics",
        "The Bhilwara mine must ship 6000 t of ore to Kandla port within 24 hours. Road, "
        "rail and river barge are all available - choose the mix.",
        "Real logistics planners solve exactly this with linear programming: the cheapest "
        "mix that still meets the deadline and the safety target.",
        budget=1800000, par_cost=1300000, materials=[],
        formulas=[
            ("v = v_max (1 - k / k_jam)", "Hire too many trucks and they slow each other down."),
            ("P / v = m g (sin(theta) + C_rr)", "The train's speed on the 1.2% grade."),
            ("mu m_loco g >= m g sin(theta)", "Over 30 wagons and one loco stalls on the grade."),
            ("Toll = (t x km) / (h x L)", "Fast, fuel-light deliveries earn the best payout."),
            ("Pareto frontier", "No plan on the frontier can be beaten on cost, time and safety "
                                "all at once."),
        ],
        paths=[("Low cost, high skill", "A rail-and-barge mix tuned to the deadline."),
               ("High cost, robust", "Flood the road with trucks - fast but costly and less safe.")],
        success="All 6000 t delivered within 24 h and within budget.",
        bonus="Safety index of 95 or more.",
        alternate=dict(name="Split shipment", cost_factor=0.8,
                       text="Ship the urgent half now and the rest next week at a penalty."),
        cfg=dict(total=6000.0, deadline=24.0, safety_bonus=95.0),
    ),
    Level(
        10, "The Continental Megastructure", "Tier 4: Dynamic Systems", "bridge",
        "Link two continents across the 64 m Sapphire Strait with a maglev crossing powered by "
        "the new smart grid - in a rising wind.",
        "Everything you have learned at once: cables, towers, resonance, power budgets and "
        "materials from the future.",
        budget=10000000, par_cost=7000000,
        materials=["Steel", "Steel cable", "Carbon-fibre cable", "Nanotube cable", "Smart alloy"],
        formulas=[
            ("Cables: tension only", "Cables go slack (grey) if you ask them to push."),
            ("Cable-stayed towers", "Tall towers turn the deck load into cable tension and tower "
                                    "compression."),
            ("P = F v", "The maglev pod's thrust needs power from the smart grid."),
            ("Smart alloy: E x 2 when powered", "Stiffen the bridge by spending grid power."),
            ("f_n vs f_v", "The wind still wants to make it dance."),
        ],
        paths=[("Low cost, high skill", "Steel deck truss with a few carbon stays and a TMD."),
               ("High cost, robust", "Nanotube cables, smart-alloy towers and a big grid.")],
        success="The maglev pod train crosses in under 9.5 s while the wind rises to 22 m/s.",
        bonus="Factor of safety between 1.5 and 4.",
        alternate=dict(name="Hyperloop ferry", cost_factor=0.6,
                       text="Float the maglev pods across in a sealed ferry tube."),
        cfg=dict(left_x=8, right_x=72, deck_y=0.0, ground_y=-14.0, water_y=-12.0,
                 anchors=[(8, 0, "pin"), (8, -4, "pin"), (72, 0, "pin"), (72, -4, "pin")],
                 extra_anchor_xs=[26, 28, 52, 54], extra_anchor_y=-12.0, islands=[(22, 32), (48, 58)],
                 grid=2.0, view=(0, -16, 80, 26),
                 vehicle=dict(kind="maglev", mass=60000, power=3.0e6, length=36, axles=6,
                              speed=40.0, count=1, maglev=True, max_thrust=220e3),
                 deck_load=3000.0, deck_depth=1.0, humid=False,
                 wind=dict(u_start=4.0, u_end=22.0, ramp=30.0, gust=1.0, duration=36.0),
                 quake=None, grid_power=True, maglev_rs_m=50000.0, max_beam=12.0,
                 max_cable=80.0, time_limit=9.5),
    ),
]


def get(num):
    return LEVELS[num - 1]
