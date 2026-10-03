Here is a comprehensive, production-grade Game Architecture Prompt Suite. It is broken into 10 progressive development phases (Prompts 1 to 10).
Each prompt is built to instruct an advanced AI coding assistant or lead game architect to build a standalone, modular component of the system in Python (using Pygame-CE / Pymunk or Godot/WebAssembly). They enforce real classical mechanics, financial optimization ("Funds & Fun"), and intuitive discovery learning so students learn the math through mechanics without opening a textbook.
Phase 1: Mathematical Engine & The "Smart Calculator" Core
> Focus: 2D Direct Stiffness Method (FEM) truss solver, axial stress/strain, Euler buckling, and real-time visual vectors.
> 
PROMPT 1:
You are an expert Structural Engineering Software Architect and Game Developer.
Build the foundational structural calculation engine for a 2D engineering physics sandbox game using Python (with NumPy for vectorized math).

Requirements:
1. Core FEM / Truss Mechanics:
   - Implement a 2D Direct Stiffness Matrix solver for pin-jointed planar trusses.
   - For every member connecting nodes (i, j): calculate length L, angle theta, local-to-global transformation matrix, and element stiffness matrix k = (E*A/L).
   - Assemble the global stiffness matrix K, apply boundary conditions (fixed pinned supports, rolling supports), and solve for nodal displacements U: [K][U] = [F].
   - Calculate internal axial force N, axial stress sigma = N/A, and strain epsilon = sigma/E.

2. Physical Failure & Euler Buckling:
   - Distinguish strictly between Tension (sigma > 0) and Compression (sigma < 0).
   - Implement Euler's critical buckling load for compressive members: P_cr = (pi^2 * E * I) / (K_eff * L)^2.
   - If tensile stress exceeds Yield Strength (sigma_yield) OR compressive load exceeds P_cr, flag the member for plastic deformation or catastrophic rupture.

3. "Invisible Math Made Visible" HUD Data Feed:
   - Return clean structural metrics for the UI: normalized load ratio (|N| / N_limit from 0.0 to 1.0), vector arrows at nodes showing Newton's third law reaction pairs, and color-coded member status (Green = stable < 50%, Yellow = 50-80%, Red = 80-100%, Flashing Red = failure).
   - Write cleanly documented, standalone Python classes: Node, Member, Material, and TrussSolver with unit tests validating against standard textbook cantilever and Warren truss benchmarks.

Phase 2: Incline Kinematics, Rail Dynamics & Momentum
> Focus: Newtonian motion on ramps, friction coefficients, engine tractive effort, and kinetic vs. potential energy balance.
> 
PROMPT 2:
You are an expert Mechanical Engineer and Game Physics Programmer.
Develop the vehicle kinematics and railway track physics module that runs on top of the structural engine from Phase 1.

Requirements:
1. Dynamic Wheel-Rail Contact Mechanics:
   - Implement vehicle motion along continuous spline/linear track segments with varying incline angle theta.
   - Calculate instantaneous forces: Gravity components F_parallel = m * g * sin(theta) and Normal force N = m * g * cos(theta).
   - Model rolling resistance (F_rr = C_rr * N) and static/kinetic rail adhesion limits (F_friction_max = mu * N).
   - Implement aerodynamic drag: F_drag = 0.5 * rho * C_d * A_frontal * v^2.

2. Train Engine Power & Energy Conversion:
   - Implement Tractive Effort (T_e = min(P_engine / v, F_adhesion_limit)).
   - Model the work-energy theorem dynamically: delta_KE = Work_net, tracking Potential Energy (m*g*h) and Kinetic Energy (0.5*m*v^2).
   - If a train attempts to climb a grade steeper than the tractive effort can sustain, compute the stall condition and backward runaway slide.

3. Interactive Kinetic HUD:
   - Provide an active output stream displaying instantaneous velocity (v), acceleration (a), energy bar breakdown (Joules of PE vs. KE vs. Thermal Heat Lost to Friction).
   - Package this as a modular VehicleEngine and TrackPath system that can pass live dynamic axle loads onto the bridge nodes solved in Phase 1.

Phase 3: Cantilever Mechanics & Variable Depth Box Girders
> Focus: Balanced cantilever construction, bending moments (M), shear forces (V), and counterweight balancing.
> 
PROMPT 3:
You are an expert Civil Infrastructure and Game Engine Developer.
Create the Balanced Cantilever bridge-building subsystem where players advance segment-by-segment outward from central piers.

Requirements:
1. Beam Bending & Moment Dynamics:
   - For flexural members, implement Euler-Bernoulli beam theory: sigma_bending = (M * y) / I, and shear stress tau = (V * Q) / (I * t).
   - Compute bending moment M(x) and shear force V(x) distributions along the cantilever arms.
   - Model variable-depth haunched girder geometry: depth d(x) is largest at the pier table and tapers toward mid-span. Update Moment of Inertia I(x) = (b * d(x)^3) / 12 dynamically.

2. Seesaw Balance & Unbalance Torque Mechanics:
   - Track overturning moment about the pier support: sum(M_pier) = sum(Weight_left * distance_left) - sum(Weight_right * distance_right).
   - If |sum(M_pier)| exceeds the pier foundation's overturning resistance threshold (anchor tie-down capacity), trigger catastrophic pier tilt/rotation.
   - Implement temporary prestressing tie-downs: players can buy temporary high-strength anchor cables to stabilize asymmetric construction phases.

3. Mid-Span Closure Stitch:
   - When opposing cantilevers meet at center, provide a "Stitch & Post-Tension" function that switches the boundary conditions from dual statically determinate cantilevers into an indeterminate continuous beam, updating the moment distribution in real time.

Phase 4: Railway Signaling, Logic Gates & Safe Headway
> Focus: Signal logic (Block & Interlocking), braking distance equations, and crash prevention.
> 
PROMPT 4:
You are a Railway Systems & Automation Control Engineer and Game Designer.
Design an automated railway signaling, interlocking, and block control system for multi-train traffic networks.

Requirements:
1. Physics-Based Safe Braking Distance & Headway:
   - Compute required emergency braking distance based on current speed and track slope: d_stop = (v^2) / (2 * (mu * g * cos(theta) - g * sin(theta))).
   - Enforce dynamic signal spacing: yellow/amber cautions must be placed at a distance >= d_stop to prevent overruns.

2. Track Circuit & Block Signaling Logic:
   - Divide track networks into discrete electrical blocks. If any wheelset is inside Block N, the block status is OCCUPIED.
   - Implement 3-aspect and 4-aspect signal transitions:
     - RED (Stop): Block immediately ahead is occupied.
     - YELLOW (Caution, slow to approach speed): Next block is occupied.
     - GREEN (Clear): Two or more blocks ahead are clear.

3. Player Automation & Logic Circuits:
   - Allow players to wire basic logic components (AND, OR, NOT, Directional Triggers) to switches and crossing barriers.
   - Reward the player when automated timing eliminates train idling without triggering safety stops.

Phase 5: Macroscopic Traffic Flow & Fluid-Density Analytics
> Focus: Lighthill-Whitham-Richards (LWR) traffic model, fundamental traffic equation (q = k \cdot v), and shockwave jams.
> 
PROMPT 5:
You are a Traffic Flow Mathematician and Game Systems Architect.
Build a real-time macroscopic and microscopic road traffic simulation engine.

Requirements:
1. Fundamental Traffic Flow Equation:
   - Implement Greenshields or Greenberg traffic flow relations: Velocity v(k) = v_max * (1 - k / k_jam), where k is vehicle density (cars/km).
   - Calculate traffic throughput flow: q = k * v.
   - Calculate critical density k_crit where maximum flow capacity (q_max) occurs. If density exceeds k_crit, simulate congestion collapse and negative kinematic shockwaves propagating backward.

2. Microscopic Car-Following Model:
   - Implement the Intelligent Driver Model (IDM) for individual vehicles: calculate desired acceleration as a function of current velocity, gap distance to lead vehicle s, and velocity difference delta_v.
   - Vehicles must realistically brake, merge, and yield based on sightlines and speed deltas.

3. Real-Time Heatmap Analytics HUD:
   - Render a live velocity/density heatmap over the road network.
   - Output statistical graphs: Average Travel Time, Throughput (vehicles/min), and Fuel Consumption / Idle Emissions penalty.

Phase 6: Dual-Outcome Branching Mechanics ("Two Steps Forward")
> Focus: Non-punitive game design where structural failure or traffic rerouting opens alternative strategic paths.
> 
PROMPT 6:
You are an innovative Systems Game Designer specializing in constructive education mechanics.
Design the "Two Steps Forward" progression and failure-recovery architecture for an infrastructure engineering game.

Requirements:
1. Constructive Failure State Machine:
   - Eliminate binary "Game Over" screen. When a bridge collapses, train derails, or gridlock occurs, the game triggers a "Black Box Investigation Mode".
   - The physics simulation freezes at the exact frame of initial fracture or collision, rendering high-contrast stress vectors and showing the exact formula that caused failure (e.g., "Buckling: Compressive force 420 kN exceeded P_cr 310 kN").

2. Adaptive Alternate Routing:
   - If a bridge collapses into a gorge, the fallen debris automatically settles as rigid body rubble that can be reinforced into a low-level causeway, ford, or embankment at half the normal foundation cost.
   - If a rail mainline jams, unlock a "Bypass Spur Line" or "Cable Ferry" challenge branch, granting the player alternative points for exploring emergency logistics.

3. Educational Rewards for Autopsy:
   - Give players "Engineering Experience Points" (EXP) and salvage refunds for diagnosing why their structure failed using the integrated stress chart, ensuring that experimenting with extreme physics is financially rewarded.

Phase 7: Dynamic Environmental Hazards & Resonant Oscillations
> Focus: Harmonic frequency (f = \frac{1}{2\pi}\sqrt{\frac{k}{m}}), vortex shedding, wind aerodynamic flutter, and seismic ground acceleration.
> 
PROMPT 7:
You are an Aeroelasticity and Structural Dynamics Specialist.
Build the dynamic environmental hazard module that tests bridges and tall buildings against dynamic oscillatory forces.

Requirements:
1. Harmonic Resonance & Wind Aerodynamics:
   - Calculate the natural frequency of the structure: omega_n = sqrt(k_effective / m_effective).
   - Implement vortex shedding frequency using the Strouhal number: f_vortex = (St * U_wind) / D, where D is deck depth and U_wind is wind velocity.
   - If wind shedding frequency matches natural structural frequency (f_vortex ~= f_n), induce resonant sinusoidal oscillations with growing amplitude until damping forces or material limits are reached (the Tacoma Narrows effect).

2. Seismic Shockwaves:
   - Implement ground acceleration pulses: a_ground(t) = A_peak * sin(omega_quake * t) * exp(-decay * t).
   - Simulate base shear force: V_base = C_seismic * Total_Mass * a_ground.

3. Engineering Countermeasures:
   - Provide deployable damping components: Tuned Mass Dampers (pendulum masses with dashpots), cross-stay wind dampers, and aerodynamic fairings to break vortex formation.
   - Let children adjust the mass and spring stiffness sliders on a Tuned Mass Damper until the vibrating structure stabilizes in real time.

Phase 8: Resource Economics, Optimization & Budgeting Engine ("Funds & Fun")
> Focus: Linear programming cost optimization, material unit rates, carbon footprint tradeoffs, and revenue collection.
> 
PROMPT 8:
You are an Economy Systems Designer and Operations Research Specialist.
Build the economic and resource optimization engine for the engineering sandbox.

Requirements:
1. Multi-Objective Cost & Material Matrix:
   - Every placed component has a volumetric mass and price:
     - Timber: Low cost, high sustainability, low tensile strength, vulnerable to moisture/fire.
     - Concrete: Low cost, high compressive capacity, zero tensile capacity (unless steel-reinforced).
     - Structural Steel: High cost, high bidirectional strength, high carbon weight.
     - Advanced Carbon Fiber / Smart Alloys: Extreme cost, ultralight, near-infinite tensile capacity.
   - Calculate Total Construction Cost = sum(Material_cost) + sum(Labor_scaffolding_time) + Maintenance_overhead.

2. Dynamic Revenue Generation:
   - When freight or traffic successfully navigates the network, players earn tolls based on: Toll = (Tons_Delivered * Distance) / (Time_Taken * Fuel_Burned).
   - High speed and zero congestion multiply the payout; structural over-engineering (massive safety factors > 4.0) depletes profit margins.

3. Optimization Challenge Benchmarking:
   - Rank completed designs on a Pareto-efficiency frontier:
     - Safety Index vs. Capital Expense vs. Time-to-Complete.
   - Teach players the concept of "Optimal Factor of Safety" (FS = 1.5 - 2.0)—neither under-designed (collapse) nor over-designed (bankruptcy).

Phase 9: Ten Progressive Educational Campaign Levels (Level 1 to 10)
> Focus: Full progression design mapping mechanics, math concepts, constraints, and learning outcomes without textbooks.
> 
PROMPT 9:
You are a Principal Curriculum Game Designer.
Design the complete 10-level campaign progression for this infrastructure physics game. Each level must introduce a distinct scientific principle, budget constraint, fun narrative objective, and explicit formula learned through hands-on gameplay.

Format each level as follows:
- Level Number & Title
- Narrative Mission & Real-World Context
- Budget ("Funds") & Material Unlocks
- Engineering & Physics Formulas Explored (Explain how the player learns it intuitively)
- The "Two Paths Forward" (Low-cost/high-skill vs. high-cost/robust)
- Level Success Metric

Level Outline to implement:
- Level 1: "The Creek Crossing" -> Triangulation, Vectors, Tension vs Compression.
- Level 2: "The Timber Incline" -> Ramps, Friction (mu), Gravity components (mg*sin(theta)).
- Level 3: "The Deep Canyon Pier" -> Cantilevers, Haunched Girders, Center of Gravity.
- Level 4: "Freight Mountain Pass" -> Engine Power, Momentum (p=mv), Braking Distance.
- Level 5: "The Harbor Switchyard" -> Block Signaling, Safe Headways, Intersection Logic.
- Level 6: "Urban Bottleneck" -> Traffic Density, LWR Flow model, Roundabouts vs Overpasses.
- Level 7: "Gale-Force Gorge" -> Aerodynamic Wind Drag, Harmonic Resonance, Tuned Mass Dampers.
- Level 8: "Earthquake Fault Viaduct" -> Base Shear, Seismic Isolation, Flexible Joints.
- Level 9: "Heavy Industrial Corridor" -> Multi-modal optimization (Rail + Road + Barge transfer).
- Level 10: "The Continental Megastructure" -> Ultimate synthesis (Maglev + Suspension + Smart Grid).

Phase 10: User Interface, Scientific Calculator Overlay & Gamified Feedback
> Focus: Modern HUD, interactive scientific calculator tape, vector visualizations, and instant replay diagnostics.
> 
PROMPT 10:
You are a Lead UI/UX Engineer for educational simulation games.
Build the graphical user interface, vector rendering layer, and interactive scientific calculator HUD for the engineering game.

Requirements:
1. The "Under-the-Hood" Scientific Calculator Drawer:
   - Design an expandable, interactive side-panel calculator that automatically populates with active variables when a user clicks on any beam, joint, track, or vehicle.
   - Example: Clicking a bridge member displays the equation sigma = N/A with live values plugged in, showing the slider to tweak cross-sectional area A and watching stress sigma update immediately.

2. Visual Stress & Vector Overlays:
   - Toggleable HUD layers:
     - Vector Mode: Displays live force vectors (arrows whose length reflects magnitude in kN).
     - Deflection Exaggeration: Magnifies structural deformation by 10x-50x so students can visually understand tension sag and compression bulge.
     - Velocity & Friction vectors on rail vehicles.

3. Kid-Friendly "Discovery" Sound & Visual FX:
   - Creaking wood and groaning steel sound effects as stresses cross 80%.
   - Satisfying "Ka-Ching" and confetti particle effects when an efficient design beats the budget target.
   - Clean, high-contrast, modern technical blueprint or stylized vector art style suitable for both desktop and tablet touchscreens.

Recommended Implementation Roadmap
 * Sprint 1 (Physics Core): Run Prompt 1 and Prompt 2 in your local IDE with Python/Pygame to get rigid truss members and a train running across a simple bridge with stress colors.
 * Sprint 2 (Mechanics & Signals): Run Prompt 3 and Prompt 4 to add cantilever segments and train signal lights.
 * Sprint 3 (Economics & Levels): Run Prompt 8 and Prompt 9 to establish the coin/budget economy and populate the 10 game levels.
 * Sprint 4 (UI & Polish): Run Prompt 6 and Prompt 10 to implement the failure autopsy mode and the live formula calculator overlay.