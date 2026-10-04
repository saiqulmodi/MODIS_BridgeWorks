"""'IDEA' help shown when a bottom-bar button is hovered or clicked: what it does + a tip."""

HELP = {
    # --- bridge levels
    "select": "Click any beam, joint or vehicle to open its maths in the calculator. "
              "Idea: with TEST on, click the top chord and watch sigma = N / A change.",
    "deck": "Draws road beams that vehicles drive on. Build them from bank to bank first. "
            "Idea: shorter deck pieces spread the load over more joints.",
    "beam": "Draws structural beams that hold the deck up. "
            "Idea: make triangles - a square can fold over, a triangle cannot.",
    "cable": "Draws cables: very strong when pulled, useless when pushed. "
             "Idea: hang the deck from a tall tower with cables.",
    "delete": "Click a beam to remove it (right-click does the same with any tool). "
              "Idea: delete one diagonal and watch the frame turn wobbly.",
    "size": "Cross-section size S / M / L / XL. A bigger area A means lower stress "
            "(sigma = N / A) but more weight and cost.",
    "undo": "Takes back your last change (Ctrl+Z).",
    "clear": "Removes every beam so you can start fresh (Undo brings it back).",
    "test": "Shows live stress colours with the vehicle at its worst spot while you build. "
            "Idea: aim for green and yellow - all dark green wastes money, red is close to breaking.",
    "vectors": "Shows force arrows: support reactions in blue, loads in red, and the forces on "
               "the selected joint. Arrow length = kN.",
    "sag": "Exaggerates how far the bridge bends (x1, x10, x50) so you can see it sag and bulge.",
    "speed": "Changes how fast the simulation plays.",
    "run_bridge": "Sends the vehicles across. If something breaks, the Black Box shows exactly why.",
    # --- rail levels
    "wagon_minus": "Removes a wagon: less cargo per trip, but the engine climbs more easily.",
    "wagon_plus": "Adds a wagon: more cargo per trip, but the engine can only pull mu x its own "
                  "weight before the wheels slip.",
    "banker": "Hires a pusher engine at the back of the train: more power and more grip on "
              "steep slopes.",
    "even_grade": "Re-shapes the track into one steady slope between the stations (costs "
                  "earthworks). Idea: the steepest bit is what stalls a train.",
    "follow_hill": "Lays the track straight on the ground: no earthworks, but every bump of the "
                   "hill stays in the track.",
    "run_rail": "Runs one loaded trip. Total job time = trips x trip time + the empty runs back.",
    # --- cantilever
    "cast": "Casts the next concrete segment on this arm. "
            "Idea: alternate sides to keep the see-saw balanced.",
    "tie": "Temporary anchor cables at the pier: more resistance against tipping over, for a cost.",
    "undo_cast": "Removes the last segment you cast (or un-stitches the middle).",
    "stitch": "Joins the two halves in the middle and post-tensions the girder: it becomes one "
              "continuous beam and the moments redistribute.",
    "truck_test": "Drives a 40 t truck across the finished girder and checks every section.",
    # --- signals
    "aspect": "Switches between 3-aspect and 4-aspect signals. 4-aspect adds DOUBLE YELLOW, so "
              "each block only needs half the braking distance - but each signal costs more.",
    "starter_logic": "Resets the interlocking rows to the starting version (it has bugs to find).",
    "run_signals": "Plays 12 minutes of train traffic with your signals and logic.",
    # --- traffic
    "run_traffic": "Plays 12 minutes of rush hour. Watch the road colours: red bands are jams "
                   "moving backwards.",
    # --- logistics
    "optimizer": "Plots every possible plan (a brute-force stand-in for linear programming), so "
                 "you can see the Pareto frontier of cost, time and safety.",
    "ship": "Ships all 6000 t with your plan and checks the 24-hour deadline.",
}

MATERIAL = {
    "Timber": "Timber: cheap and light but weaker (40 MPa). Good for short spans; gets weaker when wet.",
    "Steel": "Steel: strong when pulled and pushed (250 MPa), but heavy and costly.",
    "Concrete": "Concrete: very cheap and strong when pushed, but it cracks if pulled - use it "
                "only where members are squeezed.",
    "Steel cable": "Steel cable: 1500 MPa when pulled, but it cannot push at all.",
    "Carbon-fibre cable": "Carbon-fibre cable: super strong and light, but very expensive.",
    "Nanotube cable": "Nanotube cable (future material): practically unbreakable when pulled; "
                      "cannot push.",
    "Smart alloy": "Smart alloy (future material): doubles its stiffness when the smart grid "
                   "powers it.",
}

SHAPE = {
    "Solid square": "Solid square: the same material packed in the middle - smallest I, so it "
                    "buckles first.",
    "I-beam": "I-beam: material moved to the flanges, I = 0.45 A^2 - about 5x stiffer than a "
              "solid square of the same weight.",
    "Hollow box": "Hollow box: I = 0.8 A^2 - the best against buckling, but a little dearer to make.",
}

LOCO = {
    "Tank engine": "Tank engine: 250 kW, 30 t. Cheap, but light engines have little grip.",
    "Diesel shunter": "Diesel shunter: 500 kW, 60 t. Twice the power and grip of the tank engine.",
    "Mainline diesel": "Mainline diesel: 2.2 MW, 120 t. Strong, but heavy trains need gentle grades.",
    "Double-header": "Double-header: two mainline engines, 4.4 MW and 240 t of grip. Expensive.",
}

JUNCTION = {
    "signals": "Traffic signals: cheapest. Tune the cycle and green split in the calculator, or "
               "the queues grow.",
    "roundabout": "Roundabout: cars merge in turn without stopping for red lights, but must slow "
                  "to 8 m/s.",
    "overpass": "Overpass: the roads never meet, so nobody waits - but it costs the most.",
}


def all_texts():
    """Every help string (for the translation coverage test)."""
    out = list(HELP.values())
    for d in (MATERIAL, SHAPE, LOCO, JUNCTION):
        out += list(d.values())
    return out
