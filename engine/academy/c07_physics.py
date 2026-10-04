"""Class 7 - Physics (Junior Cadet): Newton's second law, stress in members (N/mm²), hydraulic
jacks, kinetic and potential energy, the wave equation, resistors in series and parallel,
electricity costs, stopping distances, centre of mass and stability - with bridge examples."""
from . import mcq


def _o(r, *alts):
    out = []
    for x in (r, *alts, r + 1, r * 2, r + 10, r + 2):
        if x not in out and x > 0:
            out.append(x)
    return out[:4]


def _n(q_en, q_bn, r, ex_en, ex_bn, alts, u_en="", u_bn=None):
    f = lambda x: f"{x:,}" if isinstance(x, int) else f"{x:g}"
    o = _o(r, *alts)
    ub = u_en if u_bn is None else u_bn
    return mcq(q_en, [f(x) + u_en for x in o], 0, ex_en, q_bn, [f(x) + ub for x in o], ex_bn)


def fma(m, a, what_en, what_bn):
    f = m * a
    return _n(f"{what_en} of mass {m:,} kg accelerates at {a} m/s². What resultant force acts on it?",
              f"{m:,} kg ভরের {what_bn} {a} m/s² ত্বরণে চলে। তার উপর লব্ধি বল কত?", f,
              f"F = ma = {m:,} x {a} = {f:,} N.",
              f"F = ma = {m:,} x {a} = {f:,} N।",
              (m + a, m // a if m % a == 0 else f + 5, f * 10), " N")


def stress(kn, area, what_en, what_bn):
    s = kn * 1000 // area
    return _n(f"{what_en} carries {kn} kN over a cross-section of {area:,} mm². What is the stress?",
              f"{what_bn} {area:,} mm² প্রস্থচ্ছেদে {kn} kN বয়। পীড়ন কত?", s,
              f"Stress = force ÷ area = {kn * 1000:,} N ÷ {area:,} mm² = {s} N/mm² (MPa).",
              f"পীড়ন = বল ÷ ক্ষেত্রফল = {kn * 1000:,} N ÷ {area:,} mm² = {s} N/mm² (মেগাপ্যাসকেল)।",
              (kn * area // 1000 if kn * area >= 1000 else s + 7, s * 10, kn), " N/mm²", " N/mm²")


def hyd(f1, a1, a2):
    f2 = f1 * a2 // a1
    return _n(f"A hydraulic jack: {f1} N pushes on a {a1} cm² piston. The lifting piston is {a2:,} cm². What force does it give?",
              f"একটা হাইড্রলিক জ্যাক: {a1} cm² পিস্টনে {f1} N ঠেলা। তোলার পিস্টন {a2:,} cm²। কত বল দেয়?", f2,
              f"Same pressure everywhere: F2 = F1 x A2 ÷ A1 = {f1} x {a2:,} ÷ {a1} = {f2:,} N.",
              f"সব জায়গায় চাপ সমান: F2 = F1 x A2 ÷ A1 = {f1} x {a2:,} ÷ {a1} = {f2:,} N।",
              (f1 * a1 // a2 if f1 * a1 >= a2 else f2 + 50, f1 + a2, f2 // 10), " N")


def ke(m, v, what_en, what_bn):
    e = m * v * v // 2
    return _n(f"{what_en} of mass {m:,} kg moves at {v} m/s. What is its kinetic energy?",
              f"{m:,} kg ভরের {what_bn} {v} m/s বেগে চলে। তার গতিশক্তি কত?", e,
              f"KE = ½mv² = ½ x {m:,} x {v}² = {e:,} J.",
              f"গতিশক্তি = ½mv² = ½ x {m:,} x {v}² = {e:,} J।",
              (m * v, m * v * v, m * v // 2), " J")


def wave(f, lam, what_en, what_bn):
    v = f * lam
    v = int(v) if v == int(v) else round(v, 2)
    return _n(f"{what_en} has frequency {f:g} Hz and wavelength {lam:g} m. What is its speed?",
              f"{what_bn}-এর কম্পাঙ্ক {f:g} Hz আর তরঙ্গদৈর্ঘ্য {lam:g} m। গতি কত?", v,
              f"v = fλ = {f:g} x {lam:g} = {v:g} m/s.",
              f"v = fλ = {f:g} x {lam:g} = {v:g} m/s।",
              (round(f / lam, 2), round(f + lam, 2), round(v * 10, 2)), " m/s")


def series(r1, r2, r3):
    r = r1 + r2 + r3
    return _n(f"Resistors of {r1} Ω, {r2} Ω and {r3} Ω are joined in series. What is the total resistance?",
              f"{r1} Ω, {r2} Ω আর {r3} Ω রোধ শ্রেণিতে জোড়া। মোট রোধ কত?", r,
              f"In series, resistances add: {r1} + {r2} + {r3} = {r} Ω.",
              f"শ্রেণিতে রোধ যোগ হয়: {r1} + {r2} + {r3} = {r} Ω।",
              (r1 * r2 * r3, max(r1, r2, r3), r // 3 if r % 3 == 0 else r - 1), " Ω")


def parallel2(r1, r2):
    r = r1 * r2 / (r1 + r2)
    r = int(r) if r == int(r) else round(r, 2)
    return _n(f"Two resistors of {r1} Ω and {r2} Ω are joined in parallel. What is the total resistance?",
              f"{r1} Ω আর {r2} Ω-এর দুটি রোধ সমান্তরালে জোড়া। মোট রোধ কত?", r,
              f"1/R = 1/{r1} + 1/{r2}, so R = ({r1} x {r2}) ÷ ({r1} + {r2}) = {r:g} Ω - less than either one.",
              f"1/R = 1/{r1} + 1/{r2}, তাই R = ({r1} x {r2}) ÷ ({r1} + {r2}) = {r:g} Ω - যেকোনোটার চেয়ে কম।",
              (r1 + r2, round((r1 + r2) / 2, 2), min(r1, r2)), " Ω")


def ecost(kw, hours, days, rate):
    units = kw * hours * days
    units = int(units) if units == int(units) else round(units, 1)
    c = int(units * rate)
    return _n(f"Site lights use {kw:g} kW for {hours} hours a night for {days} nights. Electricity costs Rs {rate} per kWh. What is the bill in rupees?",
              f"নির্মাণস্থলের বাতি {days} রাত ধরে রাতে {hours} ঘণ্টা {kw:g} kW খরচ করে। বিদ্যুৎ ইউনিটপ্রতি {rate} টাকা। বিল কত?", c,
              f"Energy = {kw:g} x {hours} x {days} = {units:g} kWh; cost = {units:g} x {rate} = Rs {c:,}.",
              f"শক্তি = {kw:g} x {hours} x {days} = {units:g} ইউনিট; খরচ = {units:g} x {rate} = {c:,} টাকা।",
              (int(units), c // days, c + rate * 10), "", " টাকা")


ITEMS = (
    fma(1200, 3, "A car", "একটা গাড়ি"), fma(20000, 1, "A loaded truck", "একটা বোঝাই ট্রাক"),
    fma(60, 4, "A sprinter", "একজন দৌড়বিদ"), fma(500, 2, "A crane hook load", "ক্রেনের আংটার বোঝা"),
    fma(50000, 2, "A freight locomotive", "একটা মালগাড়ির ইঞ্জিন"),
    stress(100, 2000, "A steel tie bar", "একটা ইস্পাতের টান-দণ্ড"), stress(250, 1000, "A bridge hanger rod", "সেতুর একটা ঝোলানো রড"),
    stress(600, 4000, "A truss member", "একটা ট্রাস-অংশ"), stress(45, 500, "A bolt", "একটা বল্টু"),
    stress(1200, 6000, "A column", "একটা স্তম্ভ"),
    hyd(100, 2, 200), hyd(250, 5, 500), hyd(50, 1, 300), hyd(400, 4, 1000),
    ke(1000, 20, "A car", "একটা গাড়ি"), ke(80, 5, "A cyclist with bike", "সাইকেলসহ একজন আরোহী"),
    ke(20000, 10, "A truck", "একটা ট্রাক"), ke(2, 30, "A falling bolt", "একটা পড়ন্ত বল্টু"),
    wave(340, 1, "A sound", "একটা শব্দ"), wave(0.5, 4, "A water wave on a river", "নদীর একটা জলের ঢেউ"),
    wave(1000, 0.34, "A whistle", "একটা বাঁশি"), wave(2, 1.5, "A ripple", "একটা ছোট ঢেউ"),
    series(10, 20, 30), series(4, 6, 2), series(100, 220, 330),
    parallel2(6, 3), parallel2(10, 10), parallel2(12, 4), parallel2(20, 30),
    ecost(2, 10, 30, 8), ecost(1.5, 12, 20, 7), ecost(5, 8, 25, 9),
    mcq("What is Newton's second law?", ["Resultant force = mass x acceleration", "Every action has an equal reaction", "Objects stay still unless pushed", "Energy is conserved"], 0,
        "A bigger force or a smaller mass gives a bigger acceleration.",
        "নিউটনের দ্বিতীয় সূত্র কী?", ["লব্ধি বল = ভর x ত্বরণ", "প্রতিটি ক্রিয়ার সমান প্রতিক্রিয়া", "ঠেলা না দিলে বস্তু স্থির থাকে", "শক্তি সংরক্ষিত"],
        "বড় বল বা ছোট ভরে বড় ত্বরণ।"),
    mcq("A 1,000 kg car brakes with a 5,000 N force. What is its deceleration?", ["5 m/s²", "0.2 m/s²", "5,000 m/s²", "50 m/s²"], 0,
        "a = F ÷ m = 5,000 ÷ 1,000 = 5 m/s².",
        "1,000 kg-এর একটা গাড়ি 5,000 N বলে ব্রেক কষে। মন্দন কত?", ["5 m/s²", "0.2 m/s²", "5,000 m/s²", "50 m/s²"],
        "a = F ÷ m = 5,000 ÷ 1,000 = 5 m/s²।"),
    mcq("What is 'stress' in a structural member?", ["Force per unit area inside the material", "How worried the engineer is", "The member's length", "Its colour"], 0,
        "Too much stress and the material yields or breaks.",
        "কাঠামোর অংশে 'পীড়ন' কী?", ["উপাদানের ভেতরে একক ক্ষেত্রফলে বল", "প্রকৌশলীর দুশ্চিন্তা", "অংশের দৈর্ঘ্য", "তার রং"],
        "বেশি পীড়নে উপাদান নতিস্বীকার করে বা ভাঙে।"),
    mcq("Structural steel typically yields at about 250-350 N/mm². A member is at 300 N/mm² under design load. Is that a concern?", ["Yes - it is at or near yield with no safety margin", "No, it is very low", "Steel cannot yield", "Stress does not matter"], 0,
        "Designers keep working stress well below yield.",
        "কাঠামোর ইস্পাত সাধারণত 250-350 N/mm²-এ নতিস্বীকার করে। নকশার বোঝায় একটা অংশে 300 N/mm²। এটা কি চিন্তার?", ["হ্যাঁ - নতিস্বীকারের কাছে, নিরাপত্তা-মার্জিন নেই", "না, খুব কম", "ইস্পাত নতিস্বীকার করে না", "পীড়ন জরুরি নয়"],
        "নকশাকারীরা কার্যকর পীড়ন নতিস্বীকারের অনেক নিচে রাখেন।"),
    mcq("What is 'strain'?", ["Change in length ÷ original length", "Force ÷ area", "Mass ÷ volume", "Energy ÷ time"], 0,
        "A 1 m bar stretching 1 mm has a strain of 0.001.",
        "'বিকৃতি' (স্ট্রেন) কী?", ["দৈর্ঘ্যের পরিবর্তন ÷ আদি দৈর্ঘ্য", "বল ÷ ক্ষেত্রফল", "ভর ÷ আয়তন", "শক্তি ÷ সময়"],
        "1 m দণ্ড 1 mm লম্বা হলে বিকৃতি 0.001।"),
    mcq("What does Young's modulus measure?", ["How stiff a material is: stress ÷ strain", "How heavy it is", "How hot it gets", "Its price"], 0,
        "Steel (about 200,000 N/mm²) is about 7 times stiffer than concrete.",
        "ইয়ং-এর গুণাঙ্ক কী মাপে?", ["উপাদান কতটা দৃঢ়: পীড়ন ÷ বিকৃতি", "কত ভারী", "কত গরম হয়", "তার দাম"],
        "ইস্পাত (প্রায় 2,00,000 N/mm²) কংক্রিটের প্রায় 7 গুণ দৃঢ়।"),
    mcq("What does Hooke's law say?", ["Extension is proportional to force, up to the limit of proportionality", "Force is always zero", "Springs never stretch", "Heavier things fall faster"], 0,
        "F = kx for springs and elastic members.",
        "হুকের সূত্র কী বলে?", ["সমানুপাতিক সীমা পর্যন্ত প্রসারণ বলের সমানুপাতিক", "বল সবসময় শূন্য", "স্প্রিং কখনো লম্বা হয় না", "ভারী জিনিস দ্রুত পড়ে"],
        "স্প্রিং আর স্থিতিস্থাপক অংশের জন্য F = kx।"),
    mcq("A spring has stiffness k = 200 N/m. How far does it stretch under 50 N?", ["0.25 m", "4 m", "10,000 m", "250 m"], 0,
        "x = F ÷ k = 50 ÷ 200 = 0.25 m.",
        "একটা স্প্রিংয়ের দৃঢ়তা k = 200 N/m। 50 N-এ কত লম্বা হয়?", ["0.25 m", "4 m", "10,000 m", "250 m"],
        "x = F ÷ k = 50 ÷ 200 = 0.25 m।"),
    mcq("Why can a hydraulic jack lift a bridge deck?", ["Pressure is passed through the oil, so a small force on a small piston makes a big force on a big piston", "Oil is lighter than air", "Hydraulics remove gravity", "The deck floats"], 0,
        "Pressure = force ÷ area is the same everywhere in the fluid.",
        "হাইড্রলিক জ্যাক সেতুর পাটাতন তুলতে পারে কেন?", ["তেলের মধ্য দিয়ে চাপ যায়, তাই ছোট পিস্টনে ছোট বল বড় পিস্টনে বড় বল তৈরি করে", "তেল বাতাসের চেয়ে হালকা", "হাইড্রলিক মাধ্যাকর্ষণ সরায়", "পাটাতন ভাসে"],
        "তরলের সর্বত্র চাপ = বল ÷ ক্ষেত্রফল সমান।"),
    mcq("If a car's speed doubles, what happens to its kinetic energy?", ["It becomes 4 times bigger", "It doubles", "It halves", "It stays the same"], 0,
        "KE depends on v² - that is why speed limits on bridges matter so much.",
        "গাড়ির গতি দ্বিগুণ হলে গতিশক্তির কী হয়?", ["4 গুণ হয়", "দ্বিগুণ হয়", "অর্ধেক হয়", "একই থাকে"],
        "গতিশক্তি v²-এর উপর নির্ভর করে - তাই সেতুতে গতিসীমা এত জরুরি।"),
    mcq("A 10 kg tool falls 20 m (g = 10 N/kg). Ignoring air resistance, about how fast is it moving at the bottom?", ["20 m/s", "200 m/s", "10 m/s", "2 m/s"], 0,
        "mgh = ½mv²: 10 x 10 x 20 = 2,000 J = ½ x 10 x v², so v² = 400 and v = 20 m/s.",
        "একটা 10 kg যন্ত্র 20 m পড়ল (g = 10 N/kg)। বায়ুর বাধা বাদে নিচে মোটামুটি কত বেগ?", ["20 m/s", "200 m/s", "10 m/s", "2 m/s"],
        "mgh = ½mv²: 10 x 10 x 20 = 2,000 J = ½ x 10 x v², তাই v² = 400 আর v = 20 m/s।"),
    mcq("What is the 'principle of conservation of energy'?", ["Energy cannot be created or destroyed, only transferred or changed", "Energy is always lost", "Energy grows by itself", "Energy only exists in batteries"], 0,
        "A dropped hammer's potential energy becomes kinetic energy, then heat and sound.",
        "'শক্তির সংরক্ষণ নীতি' কী?", ["শক্তি সৃষ্টি বা ধ্বংস হয় না, শুধু স্থানান্তরিত বা রূপান্তরিত হয়", "শক্তি সবসময় হারায়", "শক্তি নিজে থেকে বাড়ে", "শক্তি শুধু ব্যাটারিতে থাকে"],
        "পড়ন্ত হাতুড়ির স্থিতিশক্তি গতিশক্তি, তারপর তাপ আর শব্দ হয়।"),
    mcq("What is 'thinking distance' in a car's stopping distance?", ["The distance travelled before the driver reacts and brakes", "The distance while braking", "The length of the car", "The distance to home"], 0,
        "Tiredness, phones and alcohol make it longer.",
        "গাড়ির থামার দূরত্বে 'ভাবার দূরত্ব' কী?", ["চালক সাড়া দিয়ে ব্রেক কষার আগে যতটা যায়", "ব্রেক কষার সময়ের দূরত্ব", "গাড়ির দৈর্ঘ্য", "বাড়ির দূরত্ব"],
        "ক্লান্তি, ফোন আর মদ এটা বাড়ায়।"),
    mcq("A driver's reaction time is 0.7 s at 20 m/s. What is the thinking distance?", ["14 m", "28 m", "2.9 m", "0.7 m"], 0,
        "20 x 0.7 = 14 m - travelled before even touching the brake.",
        "20 m/s বেগে চালকের প্রতিক্রিয়ার সময় 0.7 s। ভাবার দূরত্ব কত?", ["14 m", "28 m", "2.9 m", "0.7 m"],
        "20 x 0.7 = 14 m - ব্রেক ছোঁয়ার আগেই যাওয়া।"),
    mcq("Why are stopping distances longer on a wet bridge deck?", ["Less friction between tyres and road means weaker braking", "Water pushes cars forward", "Bridges are slippery only when dry", "They are shorter"], 0,
        "Slow down in rain.",
        "ভেজা সেতুর পাটাতনে থামার দূরত্ব বেশি কেন?", ["টায়ার আর রাস্তার কম ঘর্ষণে ব্রেক দুর্বল", "জল গাড়ি সামনে ঠেলে", "শুকনো হলেই সেতু পিছল", "কম হয়"],
        "বৃষ্টিতে ধীরে চালাও।"),
    mcq("What is a 'transverse wave'?", ["A wave whose vibrations are at right angles to its direction of travel", "A wave that vibrates along its direction", "A wave that does not move", "A sound wave in air"], 0,
        "Light and ripples on water are transverse; sound in air is longitudinal.",
        "'অনুপ্রস্থ তরঙ্গ' কী?", ["যে তরঙ্গের কম্পন চলার দিকের সঙ্গে সমকোণে", "চলার দিক বরাবর কম্পিত তরঙ্গ", "যে তরঙ্গ চলে না", "বাতাসে শব্দতরঙ্গ"],
        "আলো আর জলের ঢেউ অনুপ্রস্থ; বাতাসে শব্দ অনুদৈর্ঘ্য।"),
    mcq("What is the 'amplitude' of a wave?", ["Its maximum displacement from the rest position", "Its speed", "Its wavelength", "Its frequency"], 0,
        "Bigger amplitude = louder sound or bigger sway.",
        "তরঙ্গের 'বিস্তার' (অ্যাম্পলিটিউড) কী?", ["স্থির অবস্থান থেকে সর্বোচ্চ সরণ", "তার গতি", "তার তরঙ্গদৈর্ঘ্য", "তার কম্পাঙ্ক"],
        "বড় বিস্তার = জোরালো শব্দ বা বড় দোলা।"),
    mcq("What is the 'period' of a vibration with frequency 2 Hz?", ["0.5 s", "2 s", "4 s", "20 s"], 0,
        "Period = 1 ÷ frequency.",
        "2 Hz কম্পাঙ্কের কম্পনের 'পর্যায়কাল' কত?", ["0.5 s", "2 s", "4 s", "20 s"],
        "পর্যায়কাল = 1 ÷ কম্পাঙ্ক।"),
    mcq("What happens to total resistance when you add more resistors in parallel?", ["It decreases", "It increases", "It stays the same", "It becomes infinite"], 0,
        "More paths make it easier for current to flow.",
        "সমান্তরালে আরও রোধ যোগ করলে মোট রোধের কী হয়?", ["কমে", "বাড়ে", "একই থাকে", "অসীম হয়"],
        "বেশি পথে বিদ্যুৎ সহজে বয়।"),
    mcq("In a series circuit, how is the current at different points?", ["The same everywhere", "Bigger near the battery", "Zero after each bulb", "Different in each bulb"], 0,
        "There is only one path, so the same current flows through each part.",
        "শ্রেণি-বর্তনীতে বিভিন্ন বিন্দুতে বিদ্যুৎ-প্রবাহ কেমন?", ["সব জায়গায় সমান", "ব্যাটারির কাছে বেশি", "প্রতি বাল্বের পরে শূন্য", "প্রতি বাল্বে আলাদা"],
        "একটাই পথ, তাই প্রতিটি অংশে একই প্রবাহ।"),
    mcq("In a parallel circuit, how is the voltage across each branch?", ["The same as the supply voltage", "Shared out equally", "Zero", "Double"], 0,
        "That is why every lamp on a parallel circuit is equally bright.",
        "সমান্তরাল বর্তনীতে প্রতিটি শাখায় ভোল্টেজ কেমন?", ["সরবরাহ-ভোল্টেজের সমান", "সমান ভাগ হয়", "শূন্য", "দ্বিগুণ"],
        "তাই সমান্তরাল বর্তনীর প্রতিটি বাতি সমান উজ্জ্বল।"),
    mcq("What does an earth wire do in a plug?", ["Provides a safe path for current if a metal case becomes live", "Makes the device work faster", "Stores electricity", "Cools the plug"], 0,
        "With a fuse, it protects people from shocks.",
        "প্লাগে আর্থ-তার কী করে?", ["ধাতুর খোল বিদ্যুতায়িত হলে বিদ্যুৎকে নিরাপদ পথ দেয়", "যন্ত্র দ্রুত চালায়", "বিদ্যুৎ জমায়", "প্লাগ ঠান্ডা রাখে"],
        "ফিউজের সঙ্গে মিলে মানুষকে শক থেকে রক্ষা করে।"),
    mcq("What does an RCD (residual current device) on a building site do?", ["Cuts power in milliseconds if current leaks to earth, preventing deadly shocks", "Measures rain", "Charges phones", "Lights the site"], 0,
        "Every outdoor site tool should be protected by an RCD.",
        "নির্মাণস্থলে আরসিডি (অবশিষ্ট-বিদ্যুৎ যন্ত্র) কী করে?", ["বিদ্যুৎ মাটিতে চুঁইয়ে গেলে মিলিসেকেন্ডে লাইন কেটে প্রাণঘাতী শক ঠেকায়", "বৃষ্টি মাপে", "ফোন চার্জ করে", "নির্মাণস্থল আলোকিত করে"],
        "বাইরের প্রতিটি যন্ত্র আরসিডি-সুরক্ষিত হওয়া উচিত।"),
    mcq("What is the 'centre of mass' of a crane plus its load?", ["The single point where all the weight seems to act", "The top of the jib", "The driver's seat", "The hook only"], 0,
        "If it moves outside the base, the crane tips over.",
        "ভারসহ ক্রেনের 'ভরকেন্দ্র' কী?", ["যে একক বিন্দুতে সব ওজন কাজ করছে বলে মনে হয়", "বাহুর ডগা", "চালকের আসন", "শুধু আংটা"],
        "এটা ভিত্তির বাইরে গেলে ক্রেন উল্টে যায়।"),
    mcq("Why do mobile cranes put out wide 'outriggers' before lifting?", ["A wider base keeps the centre of mass inside it, so the crane is stable", "To look bigger", "To slow traffic", "To save fuel"], 0,
        "Stability depends on base width and centre-of-mass position.",
        "চলমান ক্রেন তোলার আগে চওড়া 'আউটরিগার' ছড়ায় কেন?", ["চওড়া ভিত্তি ভরকেন্দ্রকে ভেতরে রাখে, তাই ক্রেন স্থির", "বড় দেখাতে", "যানবাহন ধীর করতে", "জ্বালানি বাঁচাতে"],
        "স্থিতি নির্ভর করে ভিত্তির প্রস্থ আর ভরকেন্দ্রের অবস্থানে।"),
    mcq("What is 'terminal velocity'?", ["The steady top speed reached when air resistance equals weight", "The speed of a bus at a terminal", "Zero speed", "The speed of light"], 0,
        "A skydiver stops accelerating at about 55 m/s.",
        "'প্রান্তীয় বেগ' কী?", ["বায়ুর বাধা ওজনের সমান হলে যে স্থির সর্বোচ্চ গতি", "টার্মিনালে বাসের গতি", "শূন্য গতি", "আলোর গতি"],
        "একজন স্কাইডাইভার প্রায় 55 m/s-এ ত্বরণ থামান।"),
    mcq("What is 'thermal conductivity'?", ["How easily heat passes through a material", "How hot a material is", "Its electrical charge", "Its weight"], 0,
        "Metals have high conductivity; insulation foam has very low.",
        "'তাপ-পরিবাহিতা' কী?", ["উপাদানের মধ্য দিয়ে তাপ কত সহজে যায়", "উপাদান কত গরম", "তার বৈদ্যুতিক আধান", "তার ওজন"],
        "ধাতুর পরিবাহিতা বেশি; অন্তরক ফোমের খুব কম।"),
    mcq("What is 'specific heat capacity'?", ["Energy needed to raise 1 kg of a material by 1 °C", "The size of a heater", "The boiling point", "The density"], 0,
        "Water's is high, so rivers warm and cool slowly.",
        "'আপেক্ষিক তাপ' কী?", ["1 kg উপাদানের তাপমাত্রা 1 °C বাড়াতে প্রয়োজনীয় শক্তি", "হিটারের মাপ", "স্ফুটনাঙ্ক", "ঘনত্ব"],
        "জলের বেশি, তাই নদী ধীরে গরম আর ঠান্ডা হয়।"),
    mcq("Water's specific heat capacity is 4,200 J/kg°C. How much energy heats 2 kg by 10 °C?", ["84,000 J", "8,400 J", "4,212 J", "420 J"], 0,
        "E = mcΔT = 2 x 4,200 x 10 = 84,000 J.",
        "জলের আপেক্ষিক তাপ 4,200 J/kg°C। 2 kg জলকে 10 °C গরম করতে কত শক্তি?", ["84,000 J", "8,400 J", "4,212 J", "420 J"],
        "E = mcΔT = 2 x 4,200 x 10 = 84,000 J।"),
    fma(1500, 2, "A van", "একটা ভ্যান"), fma(300, 5, "A loaded wheelbarrow and worker", "বোঝাই ঠেলাগাড়িসহ একজন কর্মী"),
    fma(4000, 3, "A small bus", "একটা ছোট বাস"), fma(250, 6, "A motorbike with rider", "আরোহীসহ একটা মোটরসাইকেল"),
    stress(80, 400, "A hanger cable strand", "ঝোলানো তারের একটা গোছা"), stress(500, 2500, "A diagonal brace", "একটা কর্ণ-ঠেকনা"),
    stress(30, 300, "A small tie rod", "একটা ছোট টান-রড"), stress(900, 3000, "A bottom chord", "একটা নিচের দণ্ড"),
    hyd(150, 3, 600), hyd(80, 2, 400), hyd(200, 5, 1500),
    ke(1500, 10, "A pickup truck", "একটা পিকআপ ট্রাক"), ke(50, 4, "A running child", "দৌড়ানো এক শিশু"), ke(40000, 5, "A slow freight train", "একটা ধীর মালগাড়ি"),
    wave(50, 6.8, "A low hum", "একটা নিচু গুঞ্জন"), wave(4, 2.5, "A rope wave", "একটা দড়ির ঢেউ"), wave(5, 0.2, "A pond ripple", "পুকুরের একটা ছোট ঢেউ"),
    series(5, 15, 25), series(47, 33, 20),
    parallel2(4, 4), parallel2(30, 60), parallel2(8, 24),
    ecost(3, 6, 30, 8), ecost(0.5, 12, 30, 10), ecost(4, 10, 15, 7),
    mcq("What is 'impulse'?", ["Force x time, equal to the change in momentum", "A sudden idea", "Speed x mass only", "Pressure x area"], 0,
        "Airbags and crumple zones increase the time, so the force is smaller.",
        "'ঘাত' (ইমপালস) কী?", ["বল x সময়, যা ভরবেগের পরিবর্তনের সমান", "হঠাৎ একটা ধারণা", "শুধু গতি x ভর", "চাপ x ক্ষেত্রফল"],
        "এয়ারব্যাগ আর দোমড়ানো-অঞ্চল সময় বাড়ায়, তাই বল কমে।"),
    mcq("A 1,000 kg car at 15 m/s stops in 3 s. What average force acts on it?", ["5,000 N", "45,000 N", "15,000 N", "3,000 N"], 0,
        "Change in momentum = 1,000 x 15 = 15,000; ÷ 3 s = 5,000 N.",
        "15 m/s বেগের 1,000 kg গাড়ি 3 s-এ থামল। গড়ে কত বল কাজ করল?", ["5,000 N", "45,000 N", "15,000 N", "3,000 N"],
        "ভরবেগের পরিবর্তন = 1,000 x 15 = 15,000; ÷ 3 s = 5,000 N।"),
    mcq("What is 'gravitational field strength' on Earth?", ["About 9.8 N/kg (often rounded to 10)", "About 1 N/kg", "About 100 N/kg", "Zero"], 0,
        "It is the pull of gravity on each kilogram.",
        "পৃথিবীতে 'মাধ্যাকর্ষণ ক্ষেত্রের প্রাবল্য' কত?", ["প্রায় 9.8 N/kg (প্রায়ই 10 ধরা হয়)", "প্রায় 1 N/kg", "প্রায় 100 N/kg", "শূন্য"],
        "প্রতি কিলোগ্রামের উপর মাধ্যাকর্ষণের টান।"),
    mcq("What is 'work done' when a crane lifts a 2,000 N beam 15 m?", ["30,000 J", "2,015 J", "133 J", "300 J"], 0,
        "W = F x d = 2,000 x 15 = 30,000 J.",
        "একটা ক্রেন 2,000 N-এর বিম 15 m তুললে 'কৃতকার্য' কত?", ["30,000 J", "2,015 J", "133 J", "300 J"],
        "W = F x d = 2,000 x 15 = 30,000 J।"),
    mcq("If that 30,000 J lift takes 60 s, what is the crane's useful power?", ["500 W", "1,800,000 W", "60 W", "30 W"], 0,
        "P = W ÷ t = 30,000 ÷ 60 = 500 W.",
        "সেই 30,000 J তোলায় 60 s লাগলে ক্রেনের দরকারি ক্ষমতা কত?", ["500 W", "18,00,000 W", "60 W", "30 W"],
        "P = W ÷ t = 30,000 ÷ 60 = 500 W।"),
    mcq("Why do long-span bridges use high-strength steel?", ["It carries more stress, so members can be lighter for the same load", "It is cheaper per kg", "It never rusts", "It is magnetic"], 0,
        "Lighter members mean less dead load to carry.",
        "লম্বা স্প্যানের সেতুতে উচ্চ-শক্তির ইস্পাত ব্যবহার হয় কেন?", ["বেশি পীড়ন বইতে পারে, তাই একই বোঝায় অংশ হালকা হয়", "কেজিপ্রতি সস্তা", "কখনো মরচে ধরে না", "চুম্বকীয়"],
        "হালকা অংশ মানে কম স্থির বোঝা।"),
    mcq("What is the 'ultimate tensile strength' of a material?", ["The maximum stress it can take in tension before breaking", "Its weight", "Its stiffness only", "Its melting point"], 0,
        "Design stresses stay far below it.",
        "উপাদানের 'চূড়ান্ত টান-শক্তি' কী?", ["ভাঙার আগে টানে সর্বোচ্চ যে পীড়ন সইতে পারে", "তার ওজন", "শুধু দৃঢ়তা", "গলনাঙ্ক"],
        "নকশার পীড়ন এর অনেক নিচে থাকে।"),
    mcq("What is 'fatigue' in metals?", ["Weakening from many repeated loads, even small ones, leading to cracks", "Tiredness of workers", "Rust only", "Melting"], 0,
        "Every truck crossing is one load cycle - bridges see millions.",
        "ধাতুর 'ক্লান্তি' (ফ্যাটিগ) কী?", ["বারবার বোঝায়, ছোট হলেও, দুর্বল হয়ে ফাটল ধরা", "কর্মীদের ক্লান্তি", "শুধু মরচে", "গলে যাওয়া"],
        "প্রতিটি ট্রাক পার হওয়া একটা বোঝা-চক্র - সেতু লক্ষ লক্ষ দেখে।"),
    mcq("What is 'creep' in concrete?", ["Slow, continuing deformation under a constant load over years", "Insects crawling", "Instant cracking", "Freezing"], 0,
        "Engineers allow for creep so decks do not sag too much.",
        "কংক্রিটে 'ক্রিপ' কী?", ["স্থির বোঝায় বছরের পর বছর ধীরে চলতে থাকা বিকৃতি", "পোকার হামাগুড়ি", "তাৎক্ষণিক ফাটল", "জমে যাওয়া"],
        "পাটাতন যাতে বেশি না ঝোলে তাই প্রকৌশলীরা ক্রিপ ধরে রাখেন।"),
    mcq("A 3 kW heater runs for 2 hours. How many kWh does it use?", ["6 kWh", "1.5 kWh", "5 kWh", "3,000 kWh"], 0,
        "3 x 2 = 6 kWh.",
        "একটা 3 kW হিটার 2 ঘণ্টা চলে। কত কিলোওয়াট-ঘণ্টা খরচ হয়?", ["6 কিলোওয়াট-ঘণ্টা", "1.5 কিলোওয়াট-ঘণ্টা", "5 কিলোওয়াট-ঘণ্টা", "3,000 কিলোওয়াট-ঘণ্টা"],
        "3 x 2 = 6 কিলোওয়াট-ঘণ্টা।"),
    mcq("What is 'electromagnetic induction'?", ["Making a voltage by moving a wire through a magnetic field (or changing the field)", "Magnetising iron with heat", "Lighting a bulb with a battery", "Static electricity"], 0,
        "Generators and transformers depend on it.",
        "'তড়িৎচুম্বকীয় আবেশ' কী?", ["চৌম্বক ক্ষেত্রে তার সরিয়ে (বা ক্ষেত্র বদলে) ভোল্টেজ তৈরি", "তাপে লোহা চুম্বক করা", "ব্যাটারিতে বাল্ব জ্বালানো", "স্থির বিদ্যুৎ"],
        "জেনারেটর আর ট্রান্সফর্মার এর উপর নির্ভর করে।"),
    mcq("A step-down transformer has 1,000 turns on the primary and 50 on the secondary. 230 V goes in. What comes out?", ["11.5 V", "4,600 V", "230 V", "50 V"], 0,
        "Vs = Vp x Ns ÷ Np = 230 x 50 ÷ 1,000 = 11.5 V.",
        "একটা অবনমন ট্রান্সফর্মারের মুখ্য কুণ্ডলীতে 1,000 পাক আর গৌণে 50। 230 V ঢোকে। কত বেরোয়?", ["11.5 V", "4,600 V", "230 V", "50 V"],
        "Vs = Vp x Ns ÷ Np = 230 x 50 ÷ 1,000 = 11.5 V।"),
    mcq("Why are building-site hand tools often run at 110 V instead of 230 V?", ["Lower voltage makes shocks far less dangerous in wet, rough conditions", "110 V is more powerful", "It is cheaper electricity", "No reason"], 0,
        "Many sites use transformers to step down for safety.",
        "নির্মাণস্থলের হাত-যন্ত্র প্রায়ই 230 V-এর বদলে 110 V-এ চলে কেন?", ["কম ভোল্টেজে ভেজা, রুক্ষ পরিবেশে শক অনেক কম বিপজ্জনক", "110 V বেশি শক্তিশালী", "বিদ্যুৎ সস্তা", "কোনো কারণ নেই"],
        "অনেক নির্মাণস্থল নিরাপত্তার জন্য ট্রান্সফর্মারে ভোল্টেজ কমায়।"),
    mcq("What is 'static electricity'?", ["A build-up of charge on an insulator, often from rubbing", "Electricity in wires", "Lightning only", "Battery current"], 0,
        "A spark from static can ignite fuel vapour - fuel tankers are earthed.",
        "'স্থির বিদ্যুৎ' কী?", ["অন্তরকে আধান জমা, প্রায়ই ঘষা থেকে", "তারের বিদ্যুৎ", "শুধু বজ্র", "ব্যাটারির প্রবাহ"],
        "স্থির বিদ্যুতের স্ফুলিঙ্গ জ্বালানির বাষ্পে আগুন ধরাতে পারে - তেলের ট্যাংকার মাটির সঙ্গে জোড়া থাকে।"),
)
