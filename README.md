# MODIS BridgeWorks

A hard-physics infrastructure sandbox: **Calculate, Construct, Route.**
Every result comes from real formulas, and a built-in scientific calculator shows them with
your numbers plugged in. Built from the 10-prompt design brief in `docs/PROMPTS_10_PHASES.md`.

## Run it

```
venv\Scripts\python.exe main.py
```

Esc returns to the level menu. C toggles the calculator. F1 re-opens the briefing.
**F2 switches between English and Bengali (বাংলা)** - also the button on the menu and in every level's top bar. The choice is remembered.

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
  `reference.py` (known good/bad designs used by the tests)
- `tests/` - textbook checks for every formula, and end-to-end tests proving each level can
  be won within budget and that bad designs fail for the right reason

```
venv\Scripts\python.exe -m pytest -q
```
