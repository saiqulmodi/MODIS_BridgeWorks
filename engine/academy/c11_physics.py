"""Class 11 - Physics (Senior Engineer): second moment of area, bending stress σ = My/I, Euler
buckling of struts, forces in truss joints, resolving forces, simple harmonic motion of springs
and pendulums, wind drag on bridges, flow continuity, thermal stress in restrained steel,
damping and resonance, and measurement uncertainty - the physics behind real bridge design."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r * 2, r + 10, r + 2):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _c(x):
    x = round(x, 3)
    return int(x) if x == int(x) else x


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + ub for x in o], ex_bn)


def i_rect(b, d):
    i = round(b * d ** 3 / 12)
    return _n(f"A rectangular timber beam is {b} cm wide and {d} cm deep. What is its second moment of area about the bending axis? (I = bd³ ÷ 12)",
              f"একটা আয়তাকার কাঠের কড়ি {b} cm চওড়া আর {d} cm গভীর। বাঁকার অক্ষের সাপেক্ষে দ্বিতীয় ক্ষেত্র-ভ্রামক কত? (I = bd³ ÷ 12)", i,
              f"I = {b} x {d}³ ÷ 12 = {b} x {d ** 3:,} ÷ 12 = {i:,} cm⁴. Depth is cubed, so deep beams are far stiffer.",
              f"I = {b} x {d}³ ÷ 12 = {b} x {d ** 3:,} ÷ 12 = {i:,} cm⁴। গভীরতার ঘন হয়, তাই গভীর কড়ি অনেক বেশি দৃঢ়।",
              (round(d * b ** 3 / 12), round(b * d * d / 12), round(b * d ** 3 / 6)), " cm⁴")


def bend(m_knm, y_mm, i_e6):
    s = _c(m_knm * 1e6 * y_mm / (i_e6 * 1e6))
    return _n(f"A steel beam carries a bending moment of {m_knm} kN·m. Its second moment of area is {i_e6:g} x 10⁶ mm⁴ and the extreme fibre is {y_mm} mm from the neutral axis. What is the maximum bending stress? (σ = My ÷ I)",
              f"একটা ইস্পাতের কড়ি {m_knm} kN·m বাঁকানো ভ্রামক বয়। দ্বিতীয় ক্ষেত্র-ভ্রামক {i_e6:g} x 10⁶ mm⁴ আর প্রান্তের তন্তু নিরপেক্ষ অক্ষ থেকে {y_mm} mm দূরে। সর্বোচ্চ বাঁকানো পীড়ন কত? (σ = My ÷ I)", s,
              f"σ = My ÷ I = ({m_knm} x 10⁶ N·mm x {y_mm} mm) ÷ ({i_e6:g} x 10⁶ mm⁴) = {s:g} N/mm².",
              f"σ = My ÷ I = ({m_knm} x 10⁶ N·mm x {y_mm} mm) ÷ ({i_e6:g} x 10⁶ mm⁴) = {s:g} N/mm²।",
              (_c(m_knm * y_mm / i_e6 / 10), _c(m_knm / i_e6), _c(s * 2)), " N/mm²")


def euler(e_gpa, i_e6, l_m):
    # P = π² E I / L², using π² ≈ 9.87
    p = round(9.87 * e_gpa * 1e3 * i_e6 * 1e6 / (l_m * 1000) ** 2 / 1000)
    return _n(f"A pin-ended steel strut is {l_m} m long with E = {e_gpa} GPa and I = {i_e6:g} x 10⁶ mm⁴. What is its Euler buckling load? (P = π²EI ÷ L², π² ≈ 9.87)",
              f"দুই প্রান্তে কব্জা-আটকানো একটা ইস্পাতের ঠেকনা {l_m} m লম্বা, E = {e_gpa} GPa আর I = {i_e6:g} x 10⁶ mm⁴। এর অয়লার-বাঁকন বোঝা কত? (P = π²EI ÷ L², π² ≈ 9.87)", p,
              f"P = 9.87 x {e_gpa * 1000:,} N/mm² x {i_e6:g} x 10⁶ mm⁴ ÷ ({l_m * 1000:,} mm)² ≈ {p:,} kN. Doubling the length cuts it to a quarter!",
              f"P = 9.87 x {e_gpa * 1000:,} N/mm² x {i_e6:g} x 10⁶ mm⁴ ÷ ({l_m * 1000:,} mm)² ≈ {p:,} kN। দৈর্ঘ্য দ্বিগুণ হলে এটা এক-চতুর্থাংশ!",
              (p * 2, round(p / 2), p * 4), " kN")


def joint(w, ang, s):
    f = _c(w / (2 * s))
    return _n(f"Two equal truss members meet at the top of a symmetric A-frame, each at {ang}° to the horizontal (sin {ang}° = {s:g}). A load of {w} kN hangs from the apex. What force is in each member?",
              f"একটা প্রতিসম A-কাঠামোর চূড়ায় দুটো সমান ট্রাস-অংশ মেশে, প্রত্যেকটা অনুভূমিকের সঙ্গে {ang}° (sin {ang}° = {s:g})। চূড়া থেকে {w} kN বোঝা ঝোলে। প্রতিটা অংশে কত বল?", f,
              f"Vertical balance: 2F sin {ang}° = {w}, so F = {w} ÷ (2 x {s:g}) = {f:g} kN (compression). Flatter members carry more force.",
              f"উল্লম্ব সাম্য: 2F sin {ang}° = {w}, তাই F = {w} ÷ (2 x {s:g}) = {f:g} kN (সংনমন)। চ্যাপ্টা অংশে বেশি বল।",
              (_c(w / 2), _c(w * s), _c(w / s)), " kN")


def resolve(f, ang, c, s, which):
    r = _c(f * (c if which == "h" else s))
    w_en, w_bn = ("horizontal", "অনুভূমিক") if which == "h" else ("vertical", "উল্লম্ব")
    return _n(f"A stay cable pulls on a deck anchor with {f:,} kN at {ang}° to the horizontal (cos {ang}° = {c:g}, sin {ang}° = {s:g}). What is the {w_en} component?",
              f"একটা টানা-তার পাটাতনের নোঙরে অনুভূমিকের সঙ্গে {ang}°-এ {f:,} kN বলে টানে (cos {ang}° = {c:g}, sin {ang}° = {s:g})। {w_bn} উপাংশ কত?", r,
              f"{w_en.capitalize()} component = {f:,} x {'cos' if which == 'h' else 'sin'} {ang}° = {r:g} kN.",
              f"{w_bn} উপাংশ = {f:,} x {'cos' if which == 'h' else 'sin'} {ang}° = {r:g} kN।",
              (_c(f * (s if which == "h" else c)), f, _c(r / 2)), " kN")


def spring_t(m, k):
    t = _c(2 * 3.14 * (m / k) ** 0.5)
    return _n(f"A {m:,} kg mass on a spring of stiffness {k:,} N/m oscillates freely. What is its period? (T = 2π√(m/k), π ≈ 3.14)",
              f"{k:,} N/m দৃঢ়তার স্প্রিংয়ে {m:,} kg ভর মুক্তভাবে দোলে। পর্যায়কাল কত? (T = 2π√(m/k), π ≈ 3.14)", t,
              f"T = 2 x 3.14 x √({m:,} ÷ {k:,}) = 6.28 x {_c((m / k) ** 0.5):g} = {t:g} s.",
              f"T = 2 x 3.14 x √({m:,} ÷ {k:,}) = 6.28 x {_c((m / k) ** 0.5):g} = {t:g} s।",
              (_c(2 * 3.14 * m / k), _c((m / k) ** 0.5), _c(t * 2)), " s")


def pend(l):
    t = _c(2 * l ** 0.5)
    return _n(f"A plumb bob hangs on a {l:g} m line and swings gently. What is its period? (T = 2π√(L/g), taking g ≈ π² so T ≈ 2√L)",
              f"একটা ওলন {l:g} m সুতোয় ঝুলে আলতো দোলে। পর্যায়কাল কত? (T = 2π√(L/g), g ≈ π² ধরে T ≈ 2√L)", t,
              f"T ≈ 2√{l:g} = {t:g} s. The period depends on length, not on the mass of the bob.",
              f"T ≈ 2√{l:g} = {t:g} s। পর্যায়কাল দৈর্ঘ্যের উপর নির্ভর করে, ওলনের ভরের উপর নয়।",
              (_c(2 * l), _c(l ** 0.5), _c(t * 2)), " s")


def drag(v, cd, area):
    f = _c(0.5 * 1.2 * v * v * cd * area / 1000)
    return _n(f"Wind at {v} m/s blows on a bridge sign of area {area} m² with drag coefficient {cd:g}. What is the wind force? (F = ½ρv²C_dA, ρ = 1.2 kg/m³)",
              f"{v} m/s বেগের হাওয়া {area} m² ক্ষেত্রফলের একটা সেতু-বোর্ডে লাগে, বাধা-গুণাঙ্ক {cd:g}। হাওয়ার বল কত? (F = ½ρv²C_dA, ρ = 1.2 kg/m³)", f,
              f"F = 0.5 x 1.2 x {v}² x {cd:g} x {area} = {_c(f * 1000):,} N = {f:g} kN. Double the wind speed and the force is four times as big.",
              f"F = 0.5 x 1.2 x {v}² x {cd:g} x {area} = {_c(f * 1000):,} N = {f:g} kN। হাওয়ার বেগ দ্বিগুণ হলে বল চারগুণ।",
              (_c(f * 2), _c(0.6 * v * cd * area / 1000), _c(f / 2)), " kN")


def contin(a1, v1, a2):
    v2 = _c(a1 * v1 / a2)
    return _n(f"A river {a1} m² in cross-section flows at {v1:g} m/s. Under a bridge the channel narrows to {a2} m². How fast does the water flow there?",
              f"{a1} m² প্রস্থচ্ছেদের একটা নদী {v1:g} m/s বেগে বয়। সেতুর নিচে খাত সরু হয়ে {a2} m²। সেখানে জল কত দ্রুত বয়?", v2,
              f"Continuity: A1v1 = A2v2, so v2 = {a1} x {v1:g} ÷ {a2} = {v2:g} m/s - faster water means more scour.",
              f"নিরবচ্ছিন্নতা: A1v1 = A2v2, তাই v2 = {a1} x {v1:g} ÷ {a2} = {v2:g} m/s - দ্রুত জল মানে বেশি ক্ষয়-খনন।",
              (_c(a2 * v1 / a1), _c(v1 + a1 - a2) if v1 + a1 - a2 > 0 else _c(v2 + 1), _c(v2 * 2)), " m/s")


def tstress(dt):
    s = _c(200000 * 12e-6 * dt)
    return _n(f"A steel rail (E = 200,000 N/mm², α = 12 x 10⁻⁶ /°C) is fixed so it cannot expand. It warms by {dt}°C. What thermal stress builds up?",
              f"একটা ইস্পাতের রেল (E = 200,000 N/mm², α = 12 x 10⁻⁶ /°C) এমনভাবে আটকানো যে প্রসারিত হতে পারে না। এটা {dt}°C গরম হলো। কত তাপীয় পীড়ন জমে?", s,
              f"σ = EαΔT = 200,000 x 12 x 10⁻⁶ x {dt} = {s:g} N/mm². This is why rails and decks need expansion joints or careful stressing.",
              f"σ = EαΔT = 200,000 x 12 x 10⁻⁶ x {dt} = {s:g} N/mm²। তাই রেল আর পাটাতনে প্রসারণ-জোড় বা সাবধানী টান লাগে।",
              (_c(12 * dt / 10), _c(s * 10), _c(200 * dt)), " N/mm²")


def uncert(val, err, what_en, what_bn):
    p = _c(err * 100 / val)
    return _n(f"{what_en} is measured as {val:g} ± {err:g}. What is the percentage uncertainty?",
              f"{what_bn} মাপা হলো {val:g} ± {err:g}। শতাংশ অনিশ্চয়তা কত?", p,
              f"{err:g} ÷ {val:g} x 100 = {p:g}%.",
              f"{err:g} ÷ {val:g} x 100 = {p:g}%।",
              (_c(err * 10), _c(val / err), _c(p * 2)), "%")


ITEMS = (
    i_rect(10, 30), i_rect(20, 40), i_rect(5, 20), i_rect(15, 60),
    bend(100, 150, 300), bend(240, 200, 400), bend(90, 100, 50), bend(500, 250, 1000),
    euler(200, 5, 4), euler(200, 2, 2), euler(200, 10, 5), euler(70, 4, 2),
    joint(100, 30, 0.5), joint(60, 45, 0.71), joint(200, 60, 0.87), joint(40, 10, 0.17),
    resolve(500, 30, 0.87, 0.5, "h"), resolve(500, 30, 0.87, 0.5, "v"), resolve(800, 60, 0.5, 0.87, "h"), resolve(1200, 45, 0.71, 0.71, "v"),
    spring_t(100, 10000), spring_t(16, 400), spring_t(2000, 20000), spring_t(9, 100),
    pend(1), pend(4), pend(0.25), pend(2.25),
    drag(20, 1.2, 5), drag(30, 1.5, 10), drag(40, 1.0, 2), drag(25, 2.0, 8),
    contin(200, 1.5, 120), contin(150, 2, 100), contin(400, 1, 250),
    tstress(20), tstress(35), tstress(50), tstress(10),
    uncert(50, 0.5, "A cable length (m)", "একটা তারের দৈর্ঘ্য (m)"), uncert(2.5, 0.05, "A beam deflection (mm)", "একটা কড়ির বিক্ষেপ (mm)"),
    uncert(400, 6, "A load-cell reading (kN)", "একটা লোড-সেলের পাঠ (kN)"),
    i_rect(30, 90), bend(320, 300, 800), euler(200, 8, 6), joint(150, 20, 0.34), drag(35, 1.3, 6), contin(300, 1.2, 180),
    tstress(28), pend(9),
    mcq("What does the 'second moment of area' (I) of a beam's cross-section measure?", ["How the material is spread about the bending axis - its resistance to bending", "The beam's weight", "The beam's length", "The beam's temperature"], 0,
        "Material far from the neutral axis adds most to I.",
        "কড়ির প্রস্থচ্ছেদের 'দ্বিতীয় ক্ষেত্র-ভ্রামক' (I) কী মাপে?", ["বাঁকার অক্ষের চারপাশে উপাদান কীভাবে ছড়ানো - বাঁকার বিরুদ্ধে এর প্রতিরোধ", "কড়ির ওজন", "কড়ির দৈর্ঘ্য", "কড়ির তাপমাত্রা"],
        "নিরপেক্ষ অক্ষ থেকে দূরের উপাদান I-তে সবচেয়ে বেশি যোগ করে।"),
    mcq("What is the 'neutral axis' of a bent beam?", ["The line through the section where there is no bending stress - neither tension nor compression", "The top edge", "The bottom edge", "The beam's centre of mass only in length"], 0,
        "Stress grows linearly with distance from it: σ = My/I.",
        "বাঁকা কড়ির 'নিরপেক্ষ অক্ষ' কী?", ["প্রস্থচ্ছেদের যে রেখায় বাঁকানো পীড়ন নেই - টানও না, সংনমনও না", "উপরের ধার", "নিচের ধার", "দৈর্ঘ্যে শুধু ভরকেন্দ্র"],
        "এর থেকে দূরত্বের সঙ্গে পীড়ন সরলরৈখিকভাবে বাড়ে: σ = My/I।"),
    mcq("Why are steel I-beams turned so the tall web is vertical when carrying deck loads?", ["That orientation gives a much larger I about the bending axis, so stress and deflection are smaller", "It looks neater", "It is easier to paint", "It uses less steel to make"], 0,
        "The same beam laid flat would bend far more under load.",
        "পাটাতনের বোঝা বইতে ইস্পাতের I-কড়ির লম্বা ওয়েব খাড়া রাখা হয় কেন?", ["এই অবস্থানে বাঁকার অক্ষের সাপেক্ষে I অনেক বড়, তাই পীড়ন আর বিক্ষেপ কম", "দেখতে পরিপাটি", "রং করা সহজ", "বানাতে কম ইস্পাত লাগে"],
        "একই কড়ি শোয়ানো থাকলে বোঝায় অনেক বেশি বাঁকত।"),
    mcq("What is 'buckling' of a strut?", ["A sudden sideways bending failure of a slender member under compression", "Stretching under tension", "Corrosion of steel", "Melting in a fire"], 0,
        "Slender struts can buckle at stresses well below the material's yield stress.",
        "ঠেকনার 'বাঁকন' (বাকলিং) কী?", ["সংনমনে সরু অংশের হঠাৎ পাশের দিকে বেঁকে ব্যর্থ হওয়া", "টানে লম্বা হওয়া", "ইস্পাতের ক্ষয়", "আগুনে গলে যাওয়া"],
        "সরু ঠেকনা উপাদানের নতি-পীড়নের অনেক নিচেই বেঁকে যেতে পারে।"),
    mcq("According to Euler's formula, what happens to a strut's buckling load if its length is doubled?", ["It falls to one quarter", "It halves", "It doubles", "It stays the same"], 0,
        "P is proportional to 1/L², so 1/2² = 1/4.",
        "অয়লারের সূত্র অনুযায়ী ঠেকনার দৈর্ঘ্য দ্বিগুণ করলে বাঁকন-বোঝার কী হয়?", ["এক-চতুর্থাংশে নামে", "অর্ধেক হয়", "দ্বিগুণ হয়", "একই থাকে"],
        "P হলো 1/L²-এর সমানুপাতিক, তাই 1/2² = 1/4।"),
    mcq("How can engineers stop a long compression member in a truss from buckling?", ["Add bracing to shorten its effective length, or use a section with a larger I", "Paint it", "Make it thinner", "Heat it"], 0,
        "Tubes and boxes give high I for little weight.",
        "ট্রাসের লম্বা সংনমন-অংশকে বেঁকে যাওয়া থেকে প্রকৌশলীরা কীভাবে আটকান?", ["কার্যকর দৈর্ঘ্য কমাতে ব্রেসিং যোগ করে, বা বেশি I-এর প্রস্থচ্ছেদ ব্যবহার করে", "রং করে", "সরু করে", "গরম করে"],
        "নল আর বাক্স অল্প ওজনে বেশি I দেয়।"),
    mcq("Why do tension members in a truss not have a buckling problem?", ["Tension pulls a member straight, so any small bend is removed rather than growing", "They are always thicker", "Steel cannot buckle", "They carry no force"], 0,
        "That is why ties can be slender rods or cables.",
        "ট্রাসের টান-অংশে বাঁকনের সমস্যা হয় না কেন?", ["টান অংশকে সোজা করে টানে, তাই ছোট বাঁক বাড়ে না, বরং মুছে যায়", "এগুলো সবসময় মোটা", "ইস্পাত বাঁকতে পারে না", "এরা কোনো বল বয় না"],
        "তাই টানা-অংশ সরু রড বা তার হতে পারে।"),
    mcq("In the 'method of joints' for a truss, what do you apply at each joint?", ["Equilibrium: the sum of horizontal forces and the sum of vertical forces are both zero", "Only the moments", "The material's density", "The joint's temperature"], 0,
        "Work joint by joint, starting where only two forces are unknown.",
        "ট্রাসের 'জোড়-পদ্ধতিতে' প্রতিটা জোড়ে কী প্রয়োগ করা হয়?", ["সাম্য: অনুভূমিক বলের যোগফল আর উল্লম্ব বলের যোগফল দুটোই শূন্য", "শুধু ভ্রামক", "উপাদানের ঘনত্ব", "জোড়ের তাপমাত্রা"],
        "জোড় ধরে ধরে এগোও, যেখানে মাত্র দুটো বল অজানা সেখান থেকে শুরু করে।"),
    mcq("What is a 'zero-force member' in a truss?", ["A member that carries no load under a particular loading, often there for stability or other load cases", "A broken member", "A member made of plastic", "A member carrying infinite force"], 0,
        "Removing it may make the truss unstable under different loads.",
        "ট্রাসে 'শূন্য-বল অংশ' কী?", ["নির্দিষ্ট বোঝায় যে অংশ কোনো বল বয় না, প্রায়ই স্থিতি বা অন্য বোঝার জন্য রাখা", "ভাঙা অংশ", "প্লাস্টিকের অংশ", "অসীম বল বওয়া অংশ"],
        "সরালে অন্য বোঝায় ট্রাস অস্থির হতে পারে।"),
    mcq("What is 'simple harmonic motion'?", ["Oscillation where the restoring force is proportional to the displacement and directed towards the centre", "Motion in a straight line at constant speed", "Random shaking", "Circular motion only"], 0,
        "Springs and pendulums (for small swings) move this way.",
        "'সরল দোলগতি' কী?", ["দোলন, যেখানে ফেরানোর বল সরণের সমানুপাতিক আর কেন্দ্রের দিকে", "স্থির দ্রুতিতে সরলরেখায় গতি", "এলোমেলো ঝাঁকুনি", "শুধু বৃত্তাকার গতি"],
        "স্প্রিং আর (ছোট দোলায়) দোলক এভাবে চলে।"),
    mcq("A footbridge is made stiffer without changing its mass. What happens to its natural frequency?", ["It rises", "It falls", "It stays the same", "It becomes zero"], 0,
        "f is proportional to √(k/m) - higher stiffness, higher frequency.",
        "একটা পায়ে-চলা সেতুর ভর না বদলে দৃঢ় করা হলো। স্বাভাবিক কম্পাঙ্কের কী হয়?", ["বাড়ে", "কমে", "একই থাকে", "শূন্য হয়"],
        "f হলো √(k/m)-এর সমানুপাতিক - বেশি দৃঢ়তা, বেশি কম্পাঙ্ক।"),
    mcq("Why do footbridge designers aim to keep the vertical natural frequency above about 5 Hz?", ["Walking pace is about 2 Hz, so staying well above it avoids resonance from footsteps", "5 Hz is a lucky number", "Higher frequency means less steel", "It makes the bridge quieter only"], 0,
        "If that is not possible, dampers are added.",
        "পায়ে-চলা সেতুর নকশাকাররা উল্লম্ব স্বাভাবিক কম্পাঙ্ক প্রায় 5 Hz-এর উপরে রাখতে চান কেন?", ["হাঁটার তাল প্রায় 2 Hz, তাই অনেক উপরে থাকলে পায়ের ধাপে অনুনাদ এড়ানো যায়", "5 Hz শুভ সংখ্যা", "বেশি কম্পাঙ্ক মানে কম ইস্পাত", "শুধু সেতু শান্ত করে"],
        "সেটা সম্ভব না হলে ড্যাম্পার বসানো হয়।"),
    mcq("What does 'damping' do to an oscillating bridge?", ["Removes energy from the vibration so its amplitude dies away", "Makes it vibrate forever", "Increases the amplitude", "Changes the bridge's colour"], 0,
        "Tuned mass dampers are heavy weights on springs tuned to the bridge's frequency.",
        "দোলনরত সেতুতে 'অবমন্দন' (ড্যাম্পিং) কী করে?", ["কম্পন থেকে শক্তি সরিয়ে নেয়, তাই বিস্তার মিলিয়ে যায়", "চিরকাল কাঁপায়", "বিস্তার বাড়ায়", "সেতুর রং বদলায়"],
        "টিউনড-মাস ড্যাম্পার হলো সেতুর কম্পাঙ্কে টিউন-করা স্প্রিংয়ে বসানো ভারী ওজন।"),
    mcq("What is a 'tuned mass damper'?", ["A heavy mass on springs and dampers, tuned to move against the structure's vibration and absorb it", "A musical instrument", "A heavy truck", "A type of bearing"], 0,
        "Taipei 101 and many footbridges use them.",
        "'টিউনড-মাস ড্যাম্পার' কী?", ["স্প্রিং আর ড্যাম্পারে বসানো ভারী ভর, কাঠামোর কম্পনের উল্টো দিকে চলতে টিউন করা, কম্পন শুষে নেয়", "একটা বাদ্যযন্ত্র", "একটা ভারী ট্রাক", "এক রকম বিয়ারিং"],
        "তাইপেই 101 আর অনেক পায়ে-চলা সেতু এটা ব্যবহার করে।"),
    mcq("Why does a pendulum's period not depend on the mass of the bob?", ["Gravity's pull and the bob's inertia both scale with mass, so mass cancels out", "Heavy bobs swing faster", "Light bobs swing faster", "It does depend on mass"], 0,
        "Only length and g matter (for small swings).",
        "দোলকের পর্যায়কাল ওলনের ভরের উপর নির্ভর করে না কেন?", ["মাধ্যাকর্ষণের টান আর ওলনের জড়তা দুটোই ভরের সঙ্গে বাড়ে, তাই ভর কেটে যায়", "ভারী ওলন দ্রুত দোলে", "হালকা ওলন দ্রুত দোলে", "ভরের উপর নির্ভর করে"],
        "(ছোট দোলায়) শুধু দৈর্ঘ্য আর g গুরুত্বপূর্ণ।"),
    mcq("What is 'vortex shedding' around a bridge cable or deck?", ["Wind leaves alternating swirls behind the object, giving a rhythmic side force", "Water entering a drain", "Paint peeling in wind", "Cables shedding their coating"], 0,
        "If the shedding frequency matches the natural frequency, large vibrations can build up.",
        "সেতুর তার বা পাটাতনের চারপাশে 'ঘূর্ণি-নিক্ষেপ' কী?", ["হাওয়া বস্তুর পিছনে পালা করে ঘূর্ণি রেখে যায়, ছন্দোময় পাশের বল দেয়", "নালায় জল ঢোকা", "হাওয়ায় রং ওঠা", "তারের আবরণ খসা"],
        "নিক্ষেপের কম্পাঙ্ক স্বাভাবিক কম্পাঙ্কের সঙ্গে মিললে বড় কম্পন জমতে পারে।"),
    mcq("How do helical strakes or dimpled surfaces on tall structures reduce wind vibration?", ["They break up regular vortex shedding so no rhythmic force builds", "They make the structure heavier", "They attract birds", "They reflect sunlight"], 0,
        "You see spiral fins on tall chimneys for this reason.",
        "উঁচু কাঠামোয় পেঁচানো পাখনা বা খাঁজকাটা তল কীভাবে হাওয়ার কম্পন কমায়?", ["নিয়মিত ঘূর্ণি-নিক্ষেপ ভেঙে দেয়, তাই ছন্দোময় বল জমে না", "কাঠামো ভারী করে", "পাখি টানে", "সূর্যালোক প্রতিফলিত করে"],
        "এই কারণেই উঁচু চিমনিতে পেঁচানো পাখনা দেখা যায়।"),
    mcq("What does Bernoulli's principle say about moving air?", ["Where the speed of a fluid increases, its pressure decreases", "Faster air has higher pressure", "Pressure never changes", "Air cannot move"], 0,
        "Air speeding over a deck can create lift forces engineers must check.",
        "চলমান বাতাস নিয়ে বার্নুলির নীতি কী বলে?", ["যেখানে প্রবাহীর গতি বাড়ে, সেখানে চাপ কমে", "দ্রুত বাতাসে চাপ বেশি", "চাপ কখনো বদলায় না", "বাতাস চলতে পারে না"],
        "পাটাতনের উপর দিয়ে দ্রুত বাতাস উত্তোলন-বল তৈরি করতে পারে, যা প্রকৌশলীদের যাচাই করতে হয়।"),
    mcq("Why must lightweight bridge decks and roofs be tied down against wind uplift?", ["Fast wind over the top lowers pressure there, so the higher pressure below can lift them", "Wind always pushes down", "Gravity switches off in storms", "Uplift only happens indoors"], 0,
        "Holding-down bolts resist the uplift.",
        "হালকা সেতু-পাটাতন আর ছাদ হাওয়ার উত্তোলনের বিরুদ্ধে বেঁধে রাখতে হয় কেন?", ["উপরের দ্রুত হাওয়া সেখানে চাপ কমায়, তাই নিচের বেশি চাপ তুলে দিতে পারে", "হাওয়া সবসময় নিচে ঠেলে", "ঝড়ে মাধ্যাকর্ষণ বন্ধ হয়", "উত্তোলন শুধু ঘরের ভেতরে হয়"],
        "আটকানো-বল্টু উত্তোলন রোধ করে।"),
    mcq("What is the 'continuity equation' for a liquid?", ["The flow rate (area x speed) stays the same along a pipe or channel", "Pressure is always constant", "Speed is always constant", "Area never changes"], 0,
        "Narrow sections mean faster flow.",
        "তরলের 'নিরবচ্ছিন্নতার সমীকরণ' কী?", ["পাইপ বা খাত বরাবর প্রবাহের হার (ক্ষেত্রফল x বেগ) একই থাকে", "চাপ সবসময় স্থির", "বেগ সবসময় স্থির", "ক্ষেত্রফল কখনো বদলায় না"],
        "সরু অংশ মানে দ্রুত প্রবাহ।"),
    mcq("Why do bridges over rivers often have wide spans and slender piers?", ["To avoid narrowing the river, which would speed up flow, raise flood levels and cause scour", "To save paint", "To look modern only", "Piers must always be thin"], 0,
        "Hydraulic engineers model the flow before the design is fixed.",
        "নদীর উপরের সেতুতে প্রায়ই চওড়া স্প্যান আর সরু স্তম্ভ থাকে কেন?", ["নদী সরু না করতে, যা প্রবাহ দ্রুত করত, বন্যার জল বাড়াত আর ক্ষয়-খনন ঘটাত", "রং বাঁচাতে", "শুধু আধুনিক দেখাতে", "স্তম্ভ সবসময় সরু হতেই হবে"],
        "নকশা চূড়ান্তের আগে জলবিদ্যার প্রকৌশলীরা প্রবাহের মডেল বানান।"),
    mcq("What is 'thermal stress'?", ["Stress that builds up when a material is prevented from expanding or contracting with temperature", "Stress caused by workers in hot weather", "Stress from heavy trucks", "Stress in a thermometer"], 0,
        "σ = EαΔT for a fully restrained member.",
        "'তাপীয় পীড়ন' কী?", ["তাপমাত্রায় উপাদান প্রসারিত বা সংকুচিত হতে না পারলে যে পীড়ন জমে", "গরমে কর্মীদের চাপ", "ভারী ট্রাকের পীড়ন", "থার্মোমিটারের পীড়ন"],
        "পুরো আটকানো অংশে σ = EαΔT।"),
    mcq("Why are continuous welded railway rails 'stressed' (pre-tensioned) when laid?", ["So they are neither too compressed in summer (risking buckling) nor too stretched in winter (risking breaking)", "To make them shine", "To bend them into curves", "Stressing makes them lighter"], 0,
        "They are fixed at a 'stress-free temperature' near the local average high.",
        "একটানা ঝালাই-করা রেললাইন বসানোর সময় 'টান দেওয়া' হয় কেন?", ["যাতে গ্রীষ্মে খুব বেশি চাপে না পড়ে (বাঁকার ঝুঁকি) আর শীতে খুব বেশি টানে না পড়ে (ভাঙার ঝুঁকি)", "চকচকে করতে", "বাঁকে বাঁকাতে", "টানে হালকা হয়"],
        "স্থানীয় গড় উচ্চ তাপমাত্রার কাছের 'পীড়নহীন তাপমাত্রায়' আটকানো হয়।"),
    mcq("What is the 'absolute uncertainty' in a measurement?", ["The range either side of the reading within which the true value probably lies, e.g. ± 0.5 mm", "The reading itself", "The percentage error only", "The number of readings"], 0,
        "Percentage uncertainty = absolute ÷ reading x 100.",
        "মাপে 'পরম অনিশ্চয়তা' কী?", ["পাঠের দুপাশের যে পরিসরে আসল মান সম্ভবত থাকে, যেমন ± 0.5 mm", "পাঠ নিজেই", "শুধু শতাংশ ভুল", "পাঠের সংখ্যা"],
        "শতাংশ অনিশ্চয়তা = পরম ÷ পাঠ x 100।"),
    mcq("When two measured quantities are multiplied, how do their percentage uncertainties combine (simply)?", ["They are added", "They are multiplied", "They cancel", "Only the bigger one counts"], 0,
        "Area = length x width: 1% + 2% gives about 3% uncertainty in the area.",
        "দুটো মাপা রাশি গুণ করলে তাদের শতাংশ অনিশ্চয়তা (সরলভাবে) কীভাবে মেশে?", ["যোগ হয়", "গুণ হয়", "কাটাকাটি হয়", "শুধু বড়টা গোনা হয়"],
        "ক্ষেত্রফল = দৈর্ঘ্য x প্রস্থ: 1% + 2% মানে ক্ষেত্রফলে প্রায় 3% অনিশ্চয়তা।"),
    mcq("If a length L has 2% uncertainty, what is the uncertainty in L³?", ["6%", "2%", "8%", "4%"], 0,
        "Raising to a power multiplies the percentage uncertainty by the power.",
        "দৈর্ঘ্য L-এ 2% অনিশ্চয়তা থাকলে L³-এ কত অনিশ্চয়তা?", ["6%", "2%", "8%", "4%"],
        "ঘাতে তুললে শতাংশ অনিশ্চয়তা ঘাত দিয়ে গুণ হয়।"),
    mcq("What is a 'systematic error'?", ["An error that shifts every reading the same way, such as a zero error on a gauge", "A random scatter of readings", "A mistake in writing down", "An error that cancels by averaging"], 0,
        "Repeating readings does not remove systematic errors - calibration does.",
        "'নিয়মিত ভুল' (সিস্টেম্যাটিক এরর) কী?", ["যে ভুল প্রতিটা পাঠকে একই দিকে সরায়, যেমন মাপকযন্ত্রের শূন্য-ভুল", "পাঠের এলোমেলো ছড়ানো", "লিখতে ভুল", "গড় করলে কেটে যাওয়া ভুল"],
        "পাঠ বারবার নিলে নিয়মিত ভুল যায় না - ক্রমাঙ্কন যায়।"),
    mcq("Why are load cells and strain gauges on bridges calibrated regularly?", ["Calibration against known standards removes drift and systematic error", "To make them heavier", "Calibration changes the bridge", "It is never needed"], 0,
        "Wrong readings could hide real overload.",
        "সেতুর লোড-সেল আর বিকৃতি-মাপক নিয়মিত ক্রমাঙ্কন করা হয় কেন?", ["জানা মানের সঙ্গে ক্রমাঙ্কন সরণ আর নিয়মিত ভুল দূর করে", "ভারী করতে", "ক্রমাঙ্কন সেতু বদলায়", "কখনো দরকার নেই"],
        "ভুল পাঠ আসল অতিরিক্ত বোঝা লুকোতে পারে।"),
    mcq("What does 'dimensional analysis' let an engineer check?", ["That both sides of an equation have the same units, catching many mistakes", "The bridge's colour", "The weather", "The cost of steel"], 0,
        "σ = My/I: (N·mm x mm) ÷ mm⁴ = N/mm² - the units match a stress.",
        "'মাত্রিক বিশ্লেষণ' প্রকৌশলীকে কী যাচাই করতে দেয়?", ["সমীকরণের দুদিকের একক একই কিনা, অনেক ভুল ধরা পড়ে", "সেতুর রং", "আবহাওয়া", "ইস্পাতের দাম"],
        "σ = My/I: (N·mm x mm) ÷ mm⁴ = N/mm² - একক পীড়নের সঙ্গে মেলে।"),
    mcq("What is the SI base unit of mass?", ["Kilogram", "Gram", "Newton", "Tonne"], 0,
        "The newton is a derived unit: kg m/s².",
        "ভরের এসআই মৌলিক একক কী?", ["কিলোগ্রাম", "গ্রাম", "নিউটন", "টন"],
        "নিউটন একটা লব্ধ একক: kg m/s²।"),
    mcq("What is 1 N/mm² equal to?", ["1 MPa (megapascal)", "1 Pa", "1 kPa", "1 GPa"], 0,
        "1 N/mm² = 10⁶ N/m² = 1 MPa - the usual unit for steel and concrete stresses.",
        "1 N/mm² কীসের সমান?", ["1 মেগাপ্যাসকেল", "1 প্যাসকেল", "1 কিলোপ্যাসকেল", "1 গিগাপ্যাসকেল"],
        "1 N/mm² = 10⁶ N/m² = 1 মেগাপ্যাসকেল - ইস্পাত আর কংক্রিটের পীড়নের সাধারণ একক।"),
    mcq("What is the moment of a 50 kN force acting 4 m from a pivot?", ["200 kN·m", "12.5 kN·m", "54 kN·m", "46 kN·m"], 0,
        "Moment = force x perpendicular distance = 50 x 4.",
        "পিভট থেকে 4 m দূরে কাজ করা 50 kN বলের ভ্রামক কত?", ["200 kN·m", "12.5 kN·m", "54 kN·m", "46 kN·m"],
        "ভ্রামক = বল x লম্ব দূরত্ব = 50 x 4।"),
    mcq("What is a 'couple' in statics?", ["Two equal, opposite, parallel forces that cause rotation but no overall movement", "Two people working together", "A single force", "A type of joint"], 0,
        "Turning a spanner with two hands applies a couple.",
        "স্থিতিবিদ্যায় 'যুগ্ম বল' (কাপল) কী?", ["দুটো সমান, বিপরীত, সমান্তরাল বল যা ঘোরায় কিন্তু সামগ্রিক সরণ ঘটায় না", "একসঙ্গে কাজ করা দুজন", "একটা বল", "এক রকম জোড়"],
        "দুই হাতে স্প্যানার ঘোরানো একটা যুগ্ম বল প্রয়োগ করে।"),
    mcq("What are the three conditions for a rigid body to be in equilibrium in two dimensions?", ["Sum of horizontal forces = 0, sum of vertical forces = 0, sum of moments = 0", "Only the forces must balance", "Only the moments must balance", "It must be stationary and painted"], 0,
        "These three equations let engineers find three unknown reactions.",
        "দ্বিমাত্রায় একটা দৃঢ় বস্তু সাম্যে থাকার তিনটে শর্ত কী?", ["অনুভূমিক বলের যোগফল = 0, উল্লম্ব বলের যোগফল = 0, ভ্রামকের যোগফল = 0", "শুধু বল সমান", "শুধু ভ্রামক সমান", "স্থির আর রং-করা হতে হবে"],
        "এই তিনটে সমীকরণ দিয়ে প্রকৌশলীরা তিনটে অজানা প্রতিক্রিয়া বের করেন।"),
    mcq("What is a 'statically determinate' structure?", ["One whose support reactions and member forces can be found from equilibrium alone", "One that cannot move at all", "One made of concrete", "One with no supports"], 0,
        "Indeterminate structures need extra information about stiffness.",
        "'স্থিতিগতভাবে নির্ণেয়' কাঠামো কী?", ["যার ঠেকনা-প্রতিক্রিয়া আর অংশের বল শুধু সাম্য থেকে বের করা যায়", "যা মোটেই নড়তে পারে না", "কংক্রিটে তৈরি", "ঠেকনাহীন"],
        "অনির্ণেয় কাঠামোয় দৃঢ়তা নিয়ে বাড়তি তথ্য লাগে।"),
    mcq("Why are many modern bridges built as continuous beams over several supports?", ["Continuity spreads bending moments, reducing the maximum moment and deflection", "They are easier to calculate by hand", "They need no bearings", "They are always cheaper to build"], 0,
        "They are statically indeterminate and need more careful analysis.",
        "অনেক আধুনিক সেতু কয়েকটা ঠেকনার উপর একটানা কড়ি হিসেবে বানানো হয় কেন?", ["একটানা হওয়ায় বাঁকানো ভ্রামক ছড়িয়ে যায়, সর্বোচ্চ ভ্রামক আর বিক্ষেপ কমে", "হাতে হিসাব করা সহজ", "বিয়ারিং লাগে না", "বানাতে সবসময় সস্তা"],
        "এরা স্থিতিগতভাবে অনির্ণেয় আর বেশি যত্নের বিশ্লেষণ লাগে।"),
    mcq("What is 'shear stress'?", ["Force per unit area acting parallel to a surface, trying to slide layers past each other", "Force per unit area at right angles to a surface", "Stress from heat", "Stress in a cable only"], 0,
        "Bolts in a lap joint are mainly in shear.",
        "'কর্তন-পীড়ন' কী?", ["তলের সমান্তরালে কাজ করা একক ক্ষেত্রফলে বল, স্তরগুলোকে পরস্পরের পাশ দিয়ে পিছলে দিতে চায়", "তলের লম্বভাবে একক ক্ষেত্রফলে বল", "তাপের পীড়ন", "শুধু তারের পীড়ন"],
        "ওভারল্যাপ-জোড়ের বল্টু প্রধানত কর্তনে থাকে।"),
    mcq("A bolt of cross-section 300 mm² carries a shear force of 30 kN. What is the average shear stress?", ["100 N/mm²", "10 N/mm²", "9,000 N/mm²", "0.01 N/mm²"], 0,
        "30,000 N ÷ 300 mm² = 100 N/mm².",
        "300 mm² প্রস্থচ্ছেদের একটা বল্টু 30 kN কর্তন-বল বয়। গড় কর্তন-পীড়ন কত?", ["100 N/mm²", "10 N/mm²", "9,000 N/mm²", "0.01 N/mm²"],
        "30,000 N ÷ 300 mm² = 100 N/mm²।"),
    mcq("What is 'Poisson's ratio'?", ["The ratio of sideways contraction to lengthwise extension when a material is stretched", "The ratio of stress to strain", "A fish-based measure", "The ratio of mass to volume"], 0,
        "For steel it is about 0.3.",
        "'পয়সনের অনুপাত' কী?", ["উপাদান টানলে পাশের দিকে সংকোচন আর লম্বা দিকের প্রসারণের অনুপাত", "পীড়ন আর বিকৃতির অনুপাত", "মাছ-ভিত্তিক মাপ", "ভর আর আয়তনের অনুপাত"],
        "ইস্পাতের ক্ষেত্রে প্রায় 0.3।"),
    mcq("What is 'strain energy'?", ["Energy stored in a material when it is elastically deformed", "Energy in a battery", "Heat energy only", "The energy of a moving truck"], 0,
        "For a spring it is ½kx²; bridge bearings and cables store it under load.",
        "'বিকৃতি-শক্তি' কী?", ["উপাদান স্থিতিস্থাপকভাবে বিকৃত হলে তাতে জমা শক্তি", "ব্যাটারির শক্তি", "শুধু তাপশক্তি", "চলন্ত ট্রাকের শক্তি"],
        "স্প্রিংয়ে এটা ½kx²; বোঝায় সেতুর বিয়ারিং আর তার এটা জমায়।"),
    mcq("What does 'toughness' of a material mean?", ["Its ability to absorb energy and resist cracking before it breaks", "Its hardness only", "Its weight", "Its colour"], 0,
        "Bridge steels are tested for toughness at low temperatures (the Charpy test).",
        "উপাদানের 'দৃঢ়তা-সহনশীলতা' (টাফনেস) মানে কী?", ["ভাঙার আগে শক্তি শোষে আর ফাটল রোধ করার ক্ষমতা", "শুধু কাঠিন্য", "এর ওজন", "এর রং"],
        "সেতুর ইস্পাত কম তাপমাত্রায় দৃঢ়তা-সহনশীলতার জন্য পরীক্ষা হয় (চার্পি পরীক্ষা)।"),
    mcq("Why can some steels become brittle in very cold weather?", ["Below a transition temperature they absorb much less energy before cracking", "Cold makes steel softer", "Steel melts in cold", "It never happens"], 0,
        "Ships and bridges have failed suddenly in freezing conditions for this reason.",
        "খুব ঠান্ডা আবহাওয়ায় কিছু ইস্পাত ভঙ্গুর হয়ে যেতে পারে কেন?", ["একটা রূপান্তর-তাপমাত্রার নিচে ফাটার আগে অনেক কম শক্তি শোষে", "ঠান্ডায় ইস্পাত নরম হয়", "ঠান্ডায় ইস্পাত গলে", "কখনো হয় না"],
        "এই কারণে জাহাজ আর সেতু হিমশীতল অবস্থায় হঠাৎ ব্যর্থ হয়েছে।"),
    mcq("What is the purpose of a 'pre-stressed' concrete beam?", ["Steel tendons squeeze the concrete in advance so it stays in compression under load, avoiding cracks", "To make concrete heavier", "To paint the beam", "To let it crack freely"], 0,
        "Concrete is strong in compression but weak in tension.",
        "'আগাম-পীড়িত' কংক্রিট-কড়ির উদ্দেশ্য কী?", ["ইস্পাতের তার আগে থেকেই কংক্রিটকে চেপে রাখে, যাতে বোঝাতেও সংনমনে থাকে আর ফাটল না ধরে", "কংক্রিট ভারী করতে", "কড়িতে রং করতে", "মুক্তভাবে ফাটতে দিতে"],
        "কংক্রিট সংনমনে শক্ত, কিন্তু টানে দুর্বল।"),
    mcq("What is the difference between 'pre-tensioning' and 'post-tensioning'?", ["Pre-tensioned tendons are stressed before the concrete is cast; post-tensioned ones are stressed after it hardens", "They are the same", "Post-tensioning uses no steel", "Pre-tensioning is done on site only"], 0,
        "Long bridge girders are usually post-tensioned in ducts.",
        "'আগাম-টান' আর 'পরে-টান'-এর পার্থক্য কী?", ["আগাম-টানের তার কংক্রিট ঢালার আগে টানা হয়; পরে-টানের তার কংক্রিট শক্ত হওয়ার পরে", "দুটো একই", "পরে-টানে ইস্পাত লাগে না", "আগাম-টান শুধু নির্মাণস্থলে হয়"],
        "লম্বা সেতু-গার্ডার সাধারণত নালির ভেতরে পরে-টান দেওয়া হয়।"),
    mcq("Why does a cable-stayed bridge's tower carry mostly compression?", ["The cables pull down on it from both sides, and the balanced pull squeezes it into the foundations", "Towers are in tension", "The tower carries no load", "Wind holds it up"], 0,
        "Concrete towers suit this because concrete is strong in compression.",
        "কেবল-স্টেড সেতুর মিনার প্রধানত সংনমন বয় কেন?", ["দুদিক থেকে তার একে নিচে টানে, আর ভারসাম্যপূর্ণ টান একে ভিতের দিকে চাপে", "মিনার টানে থাকে", "মিনার কোনো বোঝা বয় না", "হাওয়া একে ধরে রাখে"],
        "কংক্রিট সংনমনে শক্ত বলে কংক্রিটের মিনার এতে মানানসই।"),
    mcq("What is 'gravitational potential energy' gained by a 2,000 kg girder lifted 15 m? (g = 10 N/kg)", ["300,000 J", "30,000 J", "150,000 J", "3,000 J"], 0,
        "Ep = mgh = 2,000 x 10 x 15.",
        "2,000 kg-এর একটা গার্ডার 15 m তুললে কত মহাকর্ষীয় স্থিতিশক্তি পায়? (g = 10 N/kg)", ["300,000 J", "30,000 J", "150,000 J", "3,000 J"],
        "স্থিতিশক্তি Ep = mgh = 2,000 x 10 x 15।"),
    mcq("A crane lifts that girder in 50 s. What is the minimum power needed?", ["6,000 W", "300,000 W", "600 W", "15,000 W"], 0,
        "P = 300,000 J ÷ 50 s = 6,000 W; real cranes need more because of losses.",
        "একটা ক্রেন সেই গার্ডার 50 s-এ তোলে। ন্যূনতম কত ক্ষমতা লাগে?", ["6,000 W", "300,000 W", "600 W", "15,000 W"],
        "P = 300,000 J ÷ 50 s = 6,000 W; ক্ষয়ের জন্য আসল ক্রেনে আরও বেশি লাগে।"),
    mcq("What is 'specific stiffness' and why is it useful in long-span design?", ["Stiffness divided by density - high values give stiff structures that are also light", "The stiffness of a specific bolt", "The density of steel", "The cost of stiffness"], 0,
        "Carbon fibre has very high specific stiffness.",
        "'আপেক্ষিক দৃঢ়তা' কী আর লম্বা-স্প্যানের নকশায় কেন কাজের?", ["দৃঢ়তা ÷ ঘনত্ব - বেশি মান মানে দৃঢ় অথচ হালকা কাঠামো", "নির্দিষ্ট বল্টুর দৃঢ়তা", "ইস্পাতের ঘনত্ব", "দৃঢ়তার দাম"],
        "কার্বন-তন্তুর আপেক্ষিক দৃঢ়তা খুব বেশি।"),
    mcq("How does fixing both ends of a strut (instead of pinning them) change its buckling load?", ["It rises about four times, because the effective length halves", "It halves", "It stays the same", "It falls to zero"], 0,
        "Effective length = 0.5L for fixed-fixed; P depends on 1/(effective length)².",
        "ঠেকনার দুই প্রান্ত কব্জার বদলে শক্ত করে আটকালে বাঁকন-বোঝা কীভাবে বদলায়?", ["প্রায় চারগুণ বাড়ে, কারণ কার্যকর দৈর্ঘ্য অর্ধেক হয়", "অর্ধেক হয়", "একই থাকে", "শূন্যে নামে"],
        "দুই প্রান্ত আটকানোয় কার্যকর দৈর্ঘ্য = 0.5L; P নির্ভর করে 1/(কার্যকর দৈর্ঘ্য)²-এর উপর।"),
    mcq("What is the 'slenderness ratio' of a column?", ["Its effective length divided by its radius of gyration - a high value means it buckles easily", "Its weight divided by its length", "Its cost divided by its strength", "Its height divided by its colour"], 0,
        "Stocky columns crush; slender columns buckle.",
        "থামের 'সরুত্ব-অনুপাত' কী?", ["কার্যকর দৈর্ঘ্য ÷ ঘূর্ণন-ব্যাসার্ধ - বেশি মান মানে সহজে বেঁকে যায়", "ওজন ÷ দৈর্ঘ্য", "দাম ÷ শক্তি", "উচ্চতা ÷ রং"],
        "মোটা-বেঁটে থাম চূর্ণ হয়; সরু থাম বেঁকে যায়।"),
)
