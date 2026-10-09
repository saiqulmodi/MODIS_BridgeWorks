# MODIS BridgeWorks

A hard-physics infrastructure sandbox: **Calculate, Construct, Route.**
Every result comes from real formulas, and a built-in scientific calculator shows them with
your numbers plugged in. Built from the 10-prompt design brief in `docs/PROMPTS_10_PHASES.md`.

## Play in the browser

https://saiqulmodi.github.io/MODIS_BridgeWorks/ - click once to start (browsers need a click before a game may play sound). The first load downloads about 15 MB (Python + numpy) and takes 10-20 seconds. Use the full-screen button at the bottom right, or F11.

## Run it

```
venv\Scripts\python.exe main.py
```

Esc returns to the level menu. C toggles the calculator. F1 re-opens the briefing. **F11** (or the menu's Full screen button) toggles full screen.

**3D view (bridge levels 1, 7, 8, 10):** the "3D view" button (or key **3**) shows the real bridge: your truss on both sides of the road, the deck and cross beams between them. You can build in 3D too: clicks land on the side truss facing you, and every beam appears on both sides. Turn the view by dragging on empty space with Select, middle-drag, Alt + drag, the arrow keys or the on-screen arrows. Zoom with the mouse wheel or + / -. Home or Reset goes back to the starting view. The physics is unchanged: the two side trusses share the load equally.
**F2 switches between English and Bengali (বাংলা)** - also the button on the menu and in every level's top bar. The choice is remembered.
**Help (H, the '?' button in a level, or 'Help: how to play' on the menu):** a step-by-step guide for new players with a walkthrough for every level, plus 200 questions & answers in four parts - Q1-50 trusses & materials, Q51-100 beams & the cantilever, Q101-150 wind, earthquakes, rail and maglev, Q151-200 money, loans and how to optimise every level. All of it is in English and Bengali and uses the game's real numbers. Inside a level it opens on that level's walkthrough. Type to search both languages (or a number such as Q37); Esc clears the search, then closes Help. The text lives in `game/guide/`.
**BridgeWorks Academy (A on the menu):** multiple-choice quizzes for Class 1-12 in Physics, Chemistry, Math, Biology, Finance and Commercials, in English and Bengali (the bank grows towards 100 questions per subject per class; `python -m engine.academy_data out.json` exports it). A right first answer earns Rs 1,000 x class in Civil Grants, reading an explanation Rs 200, reading a Help answer to the end Rs 500. Grants cover an over-budget shortfall before any loan, and one Academy question in the Black Box raises salvage from 30% to 75%. A Daily 5 mixes subjects. The Scholarship Pass hook (`engine/academy_pass.py`) is free for now - no payments are collected.
**Donation Camps (D on the menu):** give Civil Grants to nation-building causes (a school footbridge, a flood shelter, a road to the market, scholarships...) and earn badges and titles. In-game money only; `engine/donations.py` describes how real gifts could later go through a registered charity.
**IDEA hints:** hover over or click any button on the bottom bar and an IDEA box explains what it does, with a tip.
**Demo:** the Demo button at the top of each level plays a working solution. It costs 0.5% of that level's budget - a warning shows the old and new budget before anything is charged. Replays are free; demos earn no stars or EXP.
**Bank loan & government subsidised loan:** if a design costs more than the budget, a Business Plan appears before building. A bank loan (2%, 10 years) covers the shortfall; a government subsidised loan (0.5%, 15 years, up to half the budget) can take the first part. Loans are approved only if first-year toll income (after upkeep) is at least 1.5x the yearly payments - a 50% margin. Traffic grows 6% a year; the plan shows the payback year and 20-year profit. The Finance button shows the plan any time.

## The 10 levels

| # | Level | You do | Physics |
|---|---|---|---|
| 1 | The Creek Crossing | Draw a truss bridge | Stiffness-method truss, sigma = N/A, Euler buckling, sum F = 0 |
| 2 | The Timber Incline | Shape a railway, pick a train | m g sin(theta), mu N grip, T = min(P/v, mu N) |
| 3 | The Deep Canyon Pier | Cast a balanced cantilever | See-saw moments, sigma = M y / I, I = b d^3/12, continuous beam |
| 4 | Freight Mountain Pass | Heavy train over a pass in the rain | p = m v, PE/KE, braking distance on wet descents |
| 5 | The Harbor Switchyard | Place signals, wire interlocking logic | d_stop, 3/4-aspect blocks, AND/OR/NOT |
| 6 | Urban Bottleneck | Signals vs roundabout vs overpass | q = k v, Greenshields, shockwaves, IDM car-following |
| 7 | Gale-Force Gorge | Bridge that survives a 36 m/s gale | f_n, vortex shedding f_v = St U / D, tuned mass damper |
| 8 | Earthquake Fault Viaduct | Viaduct through an earthquake | a_g(t), V = C M a, isolation and flexible joints |
| 9 | Heavy Industrial Corridor | Split freight across road/rail/barge | Greenshields, train grade speed, Pareto frontier |
| 10 | The Continental Megastructure | Cable bridge + maglev + smart grid | Everything together |

Every level has two paths forward (cheap and clever, or costly and robust), a budget and
par cost, star ratings, EXP, and a **Black Box investigation** when something fails: the
exact formula that broke, a history chart, a diagnosis quiz, a salvage refund and an
alternate route. All levels are unlocked for review (`UNLOCK_ALL` in `game/save.py`).

## Project layout

- `engine/` - pure physics and maths, no drawing (truss, vehicles, beams, cantilever,
  signals, railnet, traffic, dynamics, economy, logistics, failure, levels)
- `game/` - pygame screens: `app.py`, `common.py` (calculator, black box, results, briefing),
  `scenes/` (one per level type), `bridge_sim.py` and `rail_sim.py` (headless simulations),
  `reference.py` (known good/bad designs used by the tests), `help_screen.py` and `guide/`
  (the Help screen and its English/Bengali guide and 200 Q&A)
- `tests/` - textbook checks for every formula, and end-to-end tests proving each level can
  be won within budget and that bad designs fail for the right reason

```
venv\Scripts\python.exe -m pytest -q\
# MODIS BridgeWorks

**MODIS BridgeWorks** is an educational engineering and commerce foundation platform designed to build national capability through a gamified "learn and earn" system.

## Features
- **5 Progressive Phases:** Ranging from early foundational concepts (Classes 1–3) to elite engineering & business preparation (IIT/NIT level).
- **Core Disciplines:** Mathematics, Physics, Chemistry, Biology, Geography, and Commerce.
- **Earn-While-You-Learn Wallet:** 
  - **₹10** rewarded per question attempt.
  - **+₹90 bonus (Total ₹100)** for every correct answer.
- **Automated Progression:** Dynamic question randomization, session persistence (`save.json`), and automatic phase promotion.

## Getting Started
1. Install dependencies (if applicable): `pip install -r requirements.txt`
2. Run the bridge game (also what the website runs):
   ```bash
   python main.py
   ```
3. Run the text-based question game (Phases 1-5, wallet):
   ```bash
   python quiz_console.py
```

## Big question banks
Very large MCQ collections (JEE Main/Advanced, NIT/IIT, international olympiads, school banks) plug in
without changing the game code. `tools/build_bank.py` turns a SQLite, CSV or JSON file into `banks/<id>/`
(small JSON pieces by level and subject); the game reads only the piece a student opens, on desktop and
in the browser. Banks can add new levels (e.g. `--new-level "15=International Olympiad|আন্তর্জাতিক অলিম্পিয়াড"`)
and new subjects (EVS, Geography, ...), which appear as Academy buttons. Rewards, the wallet and the
25-answers-per-login limit work the same for every question.
```bash
python tools/build_bank.py --id school --title "School MCQ Bank" --sqlite ../School_MCQ_Bank/output/mcq_bank.db --publish
python tools/build_bank.py --remove school --publish
```
`--publish` copies `banks/` to `docs/banks/` for the website. The Stratos hub box stays without banks
(20 MB limit).
