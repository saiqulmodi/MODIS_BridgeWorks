"""Game skills, part 1: Help Q1-50 (trusses and materials) as multiple-choice questions.

The question and the explanation are the Help screen's own text in both languages; only the
four options are written here, the right one first (the loader shuffles them)."""
from game.guide.truss import TRUSS

from . import mcq

_OPTS = (
    # Q1 triangles
    (("A triangle cannot change shape unless a side changes length, so it locks the frame", "Triangles use less paint", "Squares are not allowed by the game", "Triangles look better from a distance"),
     ("একটা পাশের দৈর্ঘ্য না বদলালে ত্রিভুজের আকার বদলায় না, তাই কাঠামো আটকে যায়", "ত্রিভুজে কম রং লাগে", "খেলায় বর্গ বানানো নিষেধ", "দূর থেকে ত্রিভুজ বেশি সুন্দর দেখায়")),
    # Q2 deck / beam / cable
    (("Deck is the road, beams hold it up (pull or push), cables can only be pulled", "All three are road pieces", "Cables can be pushed and pulled, beams only pulled", "Deck pieces carry no force at all"),
     ("ডেক হল রাস্তা, বিম তাকে ধরে রাখে (টান বা ঠেলা), কেবল শুধু টান নিতে পারে", "তিনটিই রাস্তার টুকরো", "কেবল ঠেলা-টান দুটোই নেয়, বিম শুধু টান", "ডেকের টুকরো কোনো বল বয় না")),
    # Q3 anchors, pin, roller
    (("A pin holds a joint still in every direction; a roller holds it up but lets it slide sideways", "A pin lets the joint slide; a roller holds it still", "Pins and rollers are the same", "Anchors can be placed anywhere in the air"),
     ("পিন জোড়কে সব দিকে স্থির রাখে; রোলার তাকে ধরে রাখে কিন্তু পাশে সরতে দেয়", "পিন জোড়কে সরতে দেয়; রোলার স্থির রাখে", "পিন আর রোলার একই", "নোঙর বাতাসে যেকোনো জায়গায় বসানো যায়")),
    # Q4 joints and grid
    (("Clicks snap to the grid or a nearby joint, and beams ending at the same point share one joint", "Joints can be placed anywhere, even inside rock", "Each beam has its own separate joints", "Anchors disappear when no beam uses them"),
     ("ক্লিক গ্রিডে বা কাছের জোড়ে আটকে যায়, আর একই বিন্দুতে শেষ হওয়া বিম একটা জোড় ভাগ করে", "জোড় যেকোনো জায়গায়, পাথরের ভিতরেও বসানো যায়", "প্রতিটি বিমের নিজস্ব আলাদা জোড়", "কোনো বিম না থাকলে নোঙর মুছে যায়")),
    # Q5 beam length limit
    (("Each level limits member length; add a braced joint in the middle and use two pieces", "Longer beams cost nothing extra but are hidden", "Holding Shift lets you draw any length", "The game has a bug with long beams"),
     ("প্রতিটি লেভেলে সদস্যের দৈর্ঘ্য সীমিত; মাঝে একটা মজবুত জোড় দিয়ে দুই টুকরো ব্যবহার করো", "লম্বা বিমের বাড়তি খরচ নেই কিন্তু লুকানো", "শিফট চেপে যেকোনো দৈর্ঘ্য আঁকা যায়", "লম্বা বিমে খেলার ত্রুটি আছে")),
    # Q6 direct stiffness method
    (("The Direct Stiffness Method: members act as springs k = EA/L and [K][U] = [F] is solved", "It guesses forces from the colours", "It weighs the bridge and divides by the beams", "It copies forces from a table of old bridges"),
     ("সরাসরি দৃঢ়তা পদ্ধতি: সদস্যরা স্প্রিং k = EA/L-এর মতো, আর [K][U] = [F] সমাধান হয়", "রং দেখে বল আন্দাজ করে", "সেতুর ওজনকে বিমের সংখ্যায় ভাগ করে", "পুরনো সেতুর তালিকা থেকে বল নকল করে")),
    # Q7 tension or compression
    (("Click it with Select: the calculator says TENSION (N > 0) or COMPRESSION (N < 0)", "Tension beams are always longer", "Compression beams are always blue", "You cannot find out before the bridge breaks"),
     ("'বাছাই' দিয়ে ক্লিক করো: ক্যালকুলেটর বলে টান (N > 0) না চাপ (N < 0)", "টানের বিম সবসময় লম্বা", "চাপের বিম সবসময় নীল", "সেতু না ভাঙা পর্যন্ত জানা যায় না")),
    # Q8 sigma = N / A
    (("Stress is the force shared over the cross-section area, so a bigger area means lower stress", "Stress is force times area", "Sigma is the length of the beam", "A bigger area raises the stress"),
     ("পীড়ন হল প্রস্থচ্ছেদের ক্ষেত্রফলে ভাগ হওয়া বল, তাই বড় ক্ষেত্রফলে পীড়ন কম", "পীড়ন হল বল গুণ ক্ষেত্রফল", "সিগমা হল বিমের দৈর্ঘ্য", "বড় ক্ষেত্রফলে পীড়ন বাড়ে")),
    # Q9 strain and E
    (("Strain = sigma / E is stretch per metre; E is the material's stiffness (steel 200 GPa)", "Strain is the price per metre", "E is the bridge's height", "A stiffer material stretches more"),
     ("বিকৃতি = sigma / E, প্রতি মিটারে কতটা লম্বা হয়; E উপাদানের দৃঢ়তা (ইস্পাত 200 GPa)", "বিকৃতি হল প্রতি মিটারের দাম", "E হল সেতুর উচ্চতা", "বেশি দৃঢ় উপাদান বেশি লম্বা হয়")),
    # Q10 strengths
    (("Steel 250 MPa both ways, but concrete 0 MPa when pulled and 30 MPa when pushed", "Concrete is strongest when pulled", "Timber is stronger than steel", "Cables are strongest when pushed"),
     ("ইস্পাত দুদিকেই 250 MPa, কিন্তু কংক্রিট টানে 0 আর চাপে 30 MPa", "কংক্রিট টানে সবচেয়ে শক্ত", "কাঠ ইস্পাতের চেয়ে শক্ত", "কেবল চাপে সবচেয়ে শক্ত")),
    # Q11 density and price
    (("Cost = density x A x L x price x shape factor; 1 m of steel I-beam M is about Rs 1,625", "Every material costs Rs 100 per kg", "Concrete is the most expensive per kg", "Timber is heavier than steel"),
     ("খরচ = ঘনত্ব x A x L x দাম x আকৃতি-গুণক; ১ মিটার ইস্পাত আই-বিম M প্রায় ১,৬২৫ টাকা", "সব উপাদানের দাম কেজিতে ১০০ টাকা", "কেজিপ্রতি কংক্রিট সবচেয়ে দামি", "কাঠ ইস্পাতের চেয়ে ভারী")),
    # Q12 pushed members fail earlier
    (("They can buckle - bow sideways - at the Euler load, often far below the crushing load", "Pushed members are made of weaker steel", "The game doubles their load", "Pulled members never fail"),
     ("এরা বেঁকে যেতে পারে — পাশে বেঁকে — অয়লার ভারে, যা প্রায়ই চূর্ণ-ভারের অনেক নিচে", "চাপের সদস্য দুর্বল ইস্পাতে তৈরি", "খেলা এদের ভার দ্বিগুণ করে", "টানের সদস্য কখনো ভাঙে না")),
    # Q13 shortening
    (("P_cr grows with 1 / L²: halve the length and the buckling load becomes 4 times bigger", "Shorter members are always cheaper to paint", "Halving the length halves the buckling load", "Length has no effect on buckling"),
     ("P_cr বাড়ে 1 / L² অনুপাতে: দৈর্ঘ্য অর্ধেক করলে বক্রন-ভার ৪ গুণ হয়", "ছোট সদস্যে রং সবসময় সস্তা", "দৈর্ঘ্য অর্ধেক করলে বক্রন-ভার অর্ধেক হয়", "দৈর্ঘ্যের বক্রনে কোনো প্রভাব নেই")),
    # Q14 I and shape
    (("I measures how far material sits from the centre; a hollow box is about 9.6 times stiffer than a solid square", "I is the beam's colour index", "A solid square is the stiffest shape", "Shape matters only for cables"),
     ("I মাপে উপাদান কেন্দ্র থেকে কত দূরে; ফাঁপা বাক্স নিরেট বর্গের চেয়ে প্রায় ৯.৬ গুণ দৃঢ়", "I হল বিমের রঙের সূচক", "নিরেট বর্গই সবচেয়ে দৃঢ় আকার", "আকার শুধু কেবলের জন্য জরুরি")),
    # Q15 bigger area vs buckling
    (("Yes: doubling A makes I four times bigger, so P_cr rises 4 times", "No, area never affects buckling", "Doubling A halves P_cr", "Only the colour of the beam matters"),
     ("হ্যাঁ: A দ্বিগুণ করলে I চার গুণ হয়, তাই P_cr ৪ গুণ বাড়ে", "না, ক্ষেত্রফল কখনো বক্রনে প্রভাব ফেলে না", "A দ্বিগুণ করলে P_cr অর্ধেক হয়", "শুধু বিমের রং জরুরি")),
    # Q16 buckling or crushing
    (("Compare crushing (strength x A) with P_cr - the smaller limit wins", "Buckling always happens first", "Crushing always happens first", "Toss a coin"),
     ("চূর্ণন (শক্তি x A) আর P_cr তুলনা করো — যেটা ছোট, সেটাই আগে ঘটে", "বক্রন সবসময় আগে হয়", "চূর্ণন সবসময় আগে হয়", "মুদ্রা টস করো")),
    # Q17 sizes
    (("Cross-section areas: beams S 10, M 20, L 40, XL 80 cm², each step doubling area and cost", "Lengths: S 1 m up to XL 8 m", "Colours of the beams", "Small, Medium, Large and Extra-Large vehicles"),
     ("প্রস্থচ্ছেদের ক্ষেত্রফল: বিম S 10, M 20, L 40, XL 80 বর্গসেমি, প্রতি ধাপে ক্ষেত্রফল আর খরচ দ্বিগুণ", "দৈর্ঘ্য: S ১ মিটার থেকে XL ৮ মিটার", "বিমের রং", "ছোট, মাঝারি, বড় আর খুব বড় গাড়ি")),
    # Q18 sizing a pulled member
    (("A_min = FS x N / sigma_t; any extra area only adds weight and cost", "Always use size XL for ties", "A_min = N x sigma_t", "Use the hollow box shape for every tie"),
     ("A_min = FS x N / sigma_t; বাড়তি ক্ষেত্রফল শুধু ওজন আর খরচ বাড়ায়", "টানা সদস্যে সবসময় XL ব্যবহার করো", "ন্যূনতম ক্ষেত্রফল = N x sigma_t", "প্রতিটি টানা সদস্যে ফাঁপা বাক্স ব্যবহার করো")),
    # Q19 sizing a pushed member
    (("Check both crushing and buckling, and take the bigger area needed", "Check only crushing", "Check only the colour", "Use the smallest size and hope"),
     ("চূর্ণন আর বক্রন দুটোই যাচাই করো, যেটায় বেশি ক্ষেত্রফল লাগে সেটা নাও", "শুধু চূর্ণন যাচাই করো", "শুধু রং দেখো", "সবচেয়ে ছোট আকার নিয়ে আশা করো")),
    # Q20 Pratt truss
    (("Diagonals are pulled and verticals pushed, so the short verticals act as struts", "Every member is pushed", "Diagonals are pushed, verticals pulled", "The top chord is pulled"),
     ("কর্ণ টান খায় আর খাড়া সদস্য চাপ, তাই ছোট খাড়া সদস্যরাই ঠেকনা", "সব সদস্য চাপ খায়", "কর্ণ চাপ খায়, খাড়া সদস্য টান", "উপরের কর্ড টান খায়")),
    # Q21 Warren truss
    (("Equal triangles with no verticals - few members and joints keep labour low", "A truss made only of verticals", "A truss that needs cables", "A truss that cannot carry vehicles"),
     ("খাড়া সদস্য ছাড়া সমান ত্রিভুজের সারি — কম সদস্য আর জোড়ে শ্রম-খরচ কম", "শুধু খাড়া সদস্যের ট্রাস", "কেবল লাগে এমন ট্রাস", "গাড়ি বইতে পারে না এমন ট্রাস")),
    # Q22 Howe truss
    (("The mirror of a Pratt: long diagonals are pushed, so they need more size to resist buckling", "Identical to a Warren truss", "A truss with no diagonals", "A truss where nothing is pushed"),
     ("প্র্যাটের উল্টো: লম্বা কর্ণ চাপ খায়, তাই বক্রন ঠেকাতে বড় আকার লাগে", "ওয়ারেন ট্রাসের হুবহু এক", "কর্ণহীন ট্রাস", "যে ট্রাসে কিছুই চাপ খায় না")),
    # Q23 truss depth
    (("Chord force is about M / h, so deeper halves chord forces; about 1/5 to 1/8 of the span is a good start", "As shallow as possible always", "Exactly equal to the span", "Depth does not change chord forces"),
     ("কর্ড-বল প্রায় M / h, তাই গভীরতা বাড়ালে বল কমে; বিস্তারের ১/৫ থেকে ১/৮ ভালো শুরু", "সবসময় যত কম গভীর সম্ভব", "ঠিক বিস্তারের সমান", "গভীরতায় কর্ড-বল বদলায় না")),
    # Q24 number of panels
    (("Few big panels for short, light spans; more panels for heavy loads or long spans, since each member and joint costs labour", "Always as many as possible", "Always exactly one panel", "Panels have no cost"),
     ("ছোট, হালকা বিস্তারে কয়েকটা বড় প্যানেল; ভারী বোঝা বা লম্বা বিস্তারে বেশি — প্রতিটি সদস্য আর জোড়ে শ্রম-খরচ আছে", "সবসময় যত বেশি সম্ভব", "সবসময় ঠিক একটা প্যানেল", "প্যানেলের কোনো খরচ নেই")),
    # Q25 above or below deck
    (("Above works everywhere; below keeps the road clear but must rest on lower anchors", "Below is impossible in every level", "Above needs anchors under the river", "It makes no difference to supports"),
     ("উপরে সব জায়গায় চলে; নিচে রাস্তা খোলা রাখে কিন্তু নিচের নোঙরে বসাতে হয়", "নিচে বানানো সব লেভেলে অসম্ভব", "উপরে বানাতে নদীর নিচে নোঙর লাগে", "ভরস্থলে কোনো তফাত নেই")),
    # Q26 zero-force member
    (("It carries no force in this test but may still keep the frame stable - delete only if TEST stays fine", "Always delete it immediately", "It is a broken member", "It carries the most force"),
     ("এই পরীক্ষায় বল বয় না, তবু কাঠামো স্থির রাখতে পারে — 'পরীক্ষা' ঠিক থাকলে তবেই মুছো", "সঙ্গে সঙ্গে মুছে ফেলো", "এটি ভাঙা সদস্য", "এটি সবচেয়ে বেশি বল বয়")),
    # Q27 stability count
    (("A 2D truss needs at least m + r ≥ 2j, and the members must also form triangles", "Count the vehicles instead", "Any frame with 10 members is stable", "m must equal j exactly"),
     ("২ডি ট্রাসে অন্তত m + r ≥ 2j লাগে, আর সদস্যদের ত্রিভুজও গড়তে হয়", "বরং গাড়ি গোনো", "১০টি সদস্যের যেকোনো কাঠামো স্থির", "m আর j ঠিক সমান হতে হবে")),
    # Q28 self weight
    (("Yes: each member's weight is shared to its end joints, and deck pieces carry the road surface too", "No, the bridge is weightless", "Only cables have weight", "Only the vehicle's weight counts"),
     ("হ্যাঁ: প্রতিটি সদস্যের ওজন দুই প্রান্তের জোড়ে ভাগ হয়, আর ডেক রাস্তার আস্তরণও বয়", "না, সেতু ওজনহীন", "শুধু কেবলের ওজন আছে", "শুধু গাড়ির ওজন ধরা হয়")),
    # Q29 TEST positions
    (("At 9 positions along the deck, showing the worst one", "Only in the exact middle", "Only at the left bank", "Nowhere - TEST ignores vehicles"),
     ("ডেক বরাবর ৯টি জায়গায়, আর সবচেয়ে খারাপটা দেখায়", "শুধু ঠিক মাঝখানে", "শুধু বাঁ পাড়ে", "কোথাও না — পরীক্ষা গাড়ি উপেক্ষা করে")),
    # Q30 wheel load path
    (("Each axle's load is split between its deck piece's two end joints, by how close it is to each", "Wheels push directly on the cables", "The whole weight goes to the left anchor", "Loads spread evenly to every joint"),
     ("প্রতিটি অক্ষের ভার তার ডেক-টুকরোর দুই প্রান্তের জোড়ে, কাছাকাছি অনুযায়ী ভাগ হয়", "চাকা সরাসরি কেবলে চাপ দেয়", "পুরো ওজন বাঁ নোঙরে যায়", "ভার সব জোড়ে সমানভাবে ছড়ায়")),
    # Q31 factor of safety
    (("FS = capacity / demand; 1.5-2 is OPTIMAL and the third star needs FS between 1.5 and 4", "FS is the bridge's price", "Any FS above 1 earns three stars", "FS below 1 is the best grade"),
     ("নিরাপত্তা-গুণক = ক্ষমতা / চাহিদা; ১.৫-২ সেরা, আর তৃতীয় তারার জন্য ১.৫ থেকে ৪ লাগে", "নিরাপত্তা-গুণক হল সেতুর দাম", "১-এর বেশি হলেই তিন তারা", "১-এর নিচে সবচেয়ে ভালো গ্রেড")),
    # Q32 TEST summary line
    (("The worst member is at 63% of its limit, so FS = 1 / 0.63 = 1.59 (OPTIMAL)", "63% of the bridge is built", "The bridge will fail 63% of the time", "63% of the budget is spent"),
     ("সবচেয়ে চাপে থাকা সদস্য তার সীমার ৬৩%-এ, তাই নিরাপত্তা-গুণক = ১ / ০.৬৩ = ১.৫৯ (সেরা)", "সেতুর ৬৩% বানানো হয়েছে", "সেতু ৬৩% সময় ভাঙবে", "বাজেটের ৬৩% খরচ হয়েছে")),
    # Q33 why not FS 10
    (("Unused strength costs money, and above FS 4 the business plan charges an over-engineering penalty", "FS above 4 is impossible", "Higher FS makes the bridge weaker", "There is no downside"),
     ("অব্যবহৃত শক্তির দাম আছে, আর ৪-এর বেশি হলে ব্যবসা-পরিকল্পনা অতি-প্রকৌশলের জরিমানা নেয়", "৪-এর বেশি নিরাপত্তা-গুণক অসম্ভব", "বেশি গুণকে সেতু দুর্বল হয়", "কোনো অসুবিধা নেই")),
    # Q34 timber or steel Level 1
    (("Timber: its material is so cheap that labour is most of the cost, and the van is light", "Steel, because it is always better", "Concrete cables", "Carbon fibre for everything"),
     ("কাঠ: উপাদান এত সস্তা যে খরচের বেশিটাই শ্রম, আর ভ্যানটা হালকা", "ইস্পাত, কারণ সবসময় ভালো", "কংক্রিটের কেবল", "সবকিছুতে কার্বন-ফাইবার")),
    # Q35 saving labour
    (("Use fewer, better members: each member costs Rs 2,500 and each new joint Rs 4,000", "Build at night", "Use only cables", "Add decorative members"),
     ("কম কিন্তু ভালো সদস্য ব্যবহার করো: প্রতিটি সদস্যে ২,৫০০ টাকা আর প্রতিটি নতুন জোড়ে ৪,০০০ টাকা", "রাতে বানাও", "শুধু কেবল ব্যবহার করো", "শোভাবর্ধক সদস্য যোগ করো")),
    # Q36 when steel is worth it
    (("Where forces are large - heavy buses, earthquakes, the maglev - since steel is much stronger and stiffer", "Always, in every level", "Never, timber always wins", "Only for decoration"),
     ("যেখানে বল বড় — ভারী বাস, ভূমিকম্প, ম্যাগলেভ — কারণ ইস্পাত অনেক বেশি শক্ত আর দৃঢ়", "সবসময়, প্রতিটি লেভেলে", "কখনো না, কাঠ সবসময় জেতে", "শুধু সাজানোর জন্য")),
    # Q37 concrete
    (("Only in members that are always pushed - it cracks the moment it is pulled", "In cables", "In members that are always pulled", "Everywhere, because it is cheap"),
     ("শুধু যে সদস্য সবসময় চাপ খায় — টান পড়লেই কংক্রিট ফাটে", "কেবলে", "যে সদস্য সবসময় টান খায়", "সব জায়গায়, কারণ সস্তা")),
    # Q38 cables
    (("Only where the force is a pull, such as hangers and stays from a tall tower", "As struts that are pushed", "As deck pieces", "Anywhere - cables carry both ways"),
     ("শুধু যেখানে বল টান, যেমন উঁচু টাওয়ার থেকে ঝোলানো দড়ি আর স্টে", "চাপ-খাওয়া ঠেকনা হিসেবে", "ডেকের টুকরো হিসেবে", "যেকোনো জায়গায় — কেবল দুদিকেই বয়")),
    # Q39 carbon fibre
    (("Only where saving weight really matters, because per newton it is still several times dearer than steel cable", "Always - it is cheaper than steel", "Never - it is weaker than steel", "Only for pushed members"),
     ("শুধু যেখানে ওজন বাঁচানো সত্যিই জরুরি, কারণ প্রতি নিউটনে এটি এখনও ইস্পাত-কেবলের কয়েক গুণ দামি", "সবসময় — এটি ইস্পাতের চেয়ে সস্তা", "কখনো না — এটি ইস্পাতের চেয়ে দুর্বল", "শুধু চাপের সদস্যে")),
    # Q40 nanotube and smart alloy
    (("Future materials: near-unbreakable nanotube cable, and smart alloy whose stiffness doubles when powered", "Cheap materials for Level 1", "Two kinds of timber", "Paints that stop rust"),
     ("ভবিষ্যতের উপাদান: প্রায় অভঙ্গুর ন্যানোটিউব কেবল, আর বিদ্যুৎ পেলে দৃঢ়তা দ্বিগুণ হওয়া স্মার্ট সংকর", "লেভেল ১-এর সস্তা উপাদান", "দুই রকম কাঠ", "মরচে রোখার রং")),
    # Q41 wet timber
    (("Yes - in wet levels timber keeps only 70% of its strength", "No, water makes timber stronger", "Only steel gets weaker when wet", "Timber dissolves completely"),
     ("হ্যাঁ — ভেজা লেভেলে কাঠ তার শক্তির মাত্র ৭০% রাখে", "না, জলে কাঠ আরও শক্ত হয়", "শুধু ইস্পাত ভিজলে দুর্বল হয়", "কাঠ পুরো গলে যায়")),
    # Q42 maintenance cost
    (("It includes five years of maintenance, such as 25% for timber and 10% for steel", "It includes a tip for the workers", "It is a game error", "It pays for the vehicles"),
     ("এতে পাঁচ বছরের রক্ষণাবেক্ষণ ধরা থাকে, যেমন কাঠে ২৫% আর ইস্পাতে ১০%", "এতে কর্মীদের বকশিশ ধরা থাকে", "এটি খেলার ভুল", "এটি গাড়ির দাম মেটায়")),
    # Q43 carbon footprint
    (("The tonnes of CO2 released making your materials - it shows the hidden cost of heavy designs", "The weight of the cars", "A penalty that removes stars", "The amount of paint used"),
     ("তোমার উপাদান বানাতে যত টন কার্বন-ডাই-অক্সাইড বেরোয় — ভারী নকশার লুকানো খরচ দেখায়", "গাড়িগুলির ওজন", "তারা কেটে নেওয়ার জরিমানা", "ব্যবহৃত রঙের পরিমাণ")),
    # Q44 I-beam and box worth it
    (("In compression almost always, since they are far stiffer against buckling; in tension use a solid square", "Never - they cost more", "Only in tension", "Only for deck pieces"),
     ("চাপে প্রায় সবসময়, কারণ বক্রনের বিরুদ্ধে অনেক দৃঢ়; টানে নিরেট বর্গ ব্যবহার করো", "কখনো না — দাম বেশি", "শুধু টানে", "শুধু ডেকের টুকরোয়")),
    # Q45 same size everywhere
    (("No - shrink the dark-green members and grow the red ones until all are yellow-green", "Yes, always use the same size", "Make every member XL", "Make every member S"),
     ("না — গাঢ় সবুজগুলো ছোট আর লালগুলো বড় করো, যতক্ষণ না সব হলুদ-সবুজ হয়", "হ্যাঁ, সবসময় একই আকার", "সব সদস্য XL করো", "সব সদস্য S করো")),
    # Q46 vectors
    (("Blue support reactions, red loads, and member forces at a selected joint - they add up to zero", "Wind directions only", "The route of the vehicles", "Where the paint is thickest"),
     ("নীল ভর-প্রতিক্রিয়া, লাল ভার, আর বাছা জোড়ে সদস্যদের বল — সব যোগ করলে শূন্য", "শুধু বাতাসের দিক", "গাড়ির যাত্রাপথ", "কোথায় রং সবচেয়ে পুরু")),
    # Q47 sag exaggeration
    (("Real deflections are millimetres, so magnifying them shows where the bridge bends most", "It makes the bridge weaker", "It adds extra load", "It is only for decoration"),
     ("আসল বাঁক মাত্র মিলিমিটার, তাই বড় করে দেখালে বোঝা যায় সেতু কোথায় সবচেয়ে বাঁকে", "এতে সেতু দুর্বল হয়", "এতে বাড়তি ভার যোগ হয়", "এটা শুধু সাজানোর জন্য")),
    # Q48 calculator
    (("Material, shape, L, A, E, force N, stress, strain, P_cr and the load ratio, card by card", "Only the price", "Only the colour", "The weather forecast"),
     ("উপাদান, আকার, L, A, E, বল N, পীড়ন, বিকৃতি, P_cr আর ভার-অনুপাত — কার্ড ধরে ধরে", "শুধু দাম", "শুধু রং", "আবহাওয়ার পূর্বাভাস")),
    # Q49 vehicle will not start
    (("The road is not connected: deck pieces must form one chain from bank to bank", "The vehicle has no fuel", "The bridge is too strong", "You must press undo first"),
     ("রাস্তা জোড়া নেই: ডেকের টুকরো এক পাড় থেকে অন্য পাড় পর্যন্ত এক শিকল হতে হবে", "গাড়িতে জ্বালানি নেই", "সেতু খুব বেশি শক্ত", "আগে পূর্বাবস্থা চাপতে হবে")),
    # Q50 optimising
    (("Get a stable no-red design, RUN it, shrink and reshape members, remove unloaded ones, stop at FS about 1.5-2", "Make everything XL steel", "Delete members at random", "Copy the cheapest-looking shape"),
     ("লাল-ছাড়া স্থির নকশা বানাও, চালাও, সদস্য ছোট আর আকার বদলাও, ভারহীন সরাও, গুণক ১.৫-২ হলে থামো", "সব XL ইস্পাত করো", "এলোমেলোভাবে সদস্য মুছো", "সবচেয়ে সস্তা-দেখতে আকার নকল করো")),
)

assert len(_OPTS) == len(TRUSS) == 50

ITEMS = tuple(mcq(it.q_en, en, 0, it.a_en, it.q_bn, bn, it.a_bn) for it, (en, bn) in zip(TRUSS, _OPTS))
