# BridgeWorks: the Python version and its data

The game now runs as a web page (`web/`, JavaScript). This file records the Python version,
which is kept unchanged. It is the source of all the game data and still runs on the desktop.

## Run it (desktop)

```
venv\Scripts\python.exe main.py
```

The game opens on the **Campus World**: a road with one building per level, in this order:
Class 1-12, BE, NIT, IIT, Expert Engineer. Click a building to enter that class.

| Inside a class | What it does |
|---|---|
| Subject chips | Filter that class's own questions (each class has only its own bank) |
| Question card | Keys 1-4 or click; Space skips. Right: +₹10,000, +4 points, + parts. Wrong: -₹1,000, -1 point |
| Bridge build | Click two joints to place a member; right-click removes; T tests; U undoes |
| Q&A Bank | Q or the button: 5 questions per page, answer highlighted, explanation |
| Top bar | Score, Treasury, Govt Subsidies (score x ₹2,500), Vehicles |

## The 5 bridge projects (`game/projects.py`)

| Project | Levels | Bridge | Test vehicle |
|---|---|---|---|
| 1 Tension Fibers | Class 1-7 | 3 cables from two masts, 20 m | Car 1.2 t |
| 2 Coplanar Trusses | Class 8-10 | Truss, 30 m | Minibus 6 t |
| 3 Parabolic Thrust | Class 11-12 | Arch with hangers and braces, 40 m | Truck 12 t |
| 4 Stay Dynamics | BE, NIT | Cable-stayed, one pylon, 60 m | Heavy-haul trailer 70 t x 1.15 |
| 5 Matrix Dissipation | IIT, Expert | Two pylons, 80 m | Freight convoy 160 t x 1.3 |

Every test uses the stiffness-method truss solver in `engine/truss.py` (tension, crushing, Euler buckling,
slack cables). `tests/test_projects.py` proves each project can be won and that weak designs fail.

## Question data

| Source | Where | Questions |
|---|---|---|
| School MCQ bank | `banks/school/*.json` (keys q/o/a/e, class from file name) | 22,412 |
| Academy | `engine/academy/*.py` (Class 1-12, NIT = 13, IIT = 14) | 10,532 |
| Generated core bank | `banks/core/*.json`, built by `python -m game.qgen` | 20,419 |
| **In the game** (repeats removed) | `data/questions.json` (short keys l/s/q/o/a/e) | **53,356** |

Level codes: 1-12 = Class 1-12, 13 = NIT (JEE Main), 14 = IIT (JEE Advanced / Olympiad), 15 = BE, 16 = Expert Engineer.

### The generated core bank (`game/qgen/`)

Numerical questions are templates: numbers are drawn with a fixed seed and the answer is computed, so it is
always right. Concept questions are written out by hand, each placed in ONE class (easier ones lower).

| Module | Subject | Levels |
|---|---|---|
| `computer.py` | Computer: exactly 120 per level, rising from robot moves to algorithms and systems | 1-16 |
| `economics.py` | Money basics, NCERT Economics 9-12, engineering economics (NPV, EMI, depreciation) | 1-16 |
| `physics.py` | Class 11 and 12 NCERT numericals | 11, 12, BE, NIT, IIT, Expert |
| `chemistry.py` | Mole concept to electrochemistry, hybridisation, oxidation states | 11, 12, BE, NIT, IIT, Expert |
| `maths.py` | Algebra to calculus, vectors, matrices; BE maths (eigenvalues, ODEs, numerical methods) | 11, 12, BE, NIT, IIT, Expert |
| `engineering.py` | Strength of materials, beams, buckling, fluids, thermal, electrical, civil | BE, Expert |
| `expert.py` | Commerce/accountancy numericals; Expert Engineer integration questions | 11 up |
| `bridge.py` | Bridge quiz for each class's own project (463-847 per project) | 1-16 |

### Rebuilding

```
venv\Scripts\python.exe -m game.qgen          # banks/core/ + data/questions.json + questions.txt
venv\Scripts\python.exe -m game.question_bank # data/questions.json + questions.txt only
venv\Scripts\python.exe tools\export_web.py   # web/data/ for the web version
```

`questions.txt` keeps the readable layout `{"1".."5": [...]}` that `quiz_console.py` reads
(Phase 1 = Class 1-3, 2 = 4-7, 3 = 8-10, 4 = 11-12, 5 = NIT/IIT/BE/Expert).

## How the web version gets its data

`tools/export_web.py` writes `web/data/`: one question file per level (`q/<level>.json`), `levels.json`,
`projects.json` (projects, materials and the guided-build steps, each checked with the Python solver) and
`handbook.json` (the 200-question Engineering Handbook from `game/guide/`). `web/tests/truss.test.js`
checks that the JavaScript solver gives the same results as Python for every guided design.
