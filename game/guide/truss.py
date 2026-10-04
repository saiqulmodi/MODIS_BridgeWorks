"""Help, Q1-50: truss mechanics and material sizing (bridge levels 1, 7, 8 and 10)."""
from . import qa

TRUSS = (
    # --- how a truss works ------------------------------------------------------------
    qa("Why does every bridge need triangles?",
       "A triangle cannot change shape unless one of its sides changes length, and beams resist "
       "changing length very strongly. A square can fold into a diamond while every side keeps "
       "its length, so a frame of squares collapses. Put a diagonal in every panel and the whole "
       "bridge locks into shape. If you forget, the Black Box reports 'The frame was a mechanism - "
       "not enough triangles'.",
       "প্রতিটি সেতুতে ত্রিভুজ লাগে কেন?",
       "কোনো বাহুর দৈর্ঘ্য না বদলালে ত্রিভুজের আকার বদলাতে পারে না, আর বিম দৈর্ঘ্য বদলাতে খুব জোরে বাধা "
       "দেয়। বর্গ প্রতিটি বাহুর দৈর্ঘ্য ঠিক রেখেও ভাঁজ হয়ে রম্বস হয়ে যেতে পারে, তাই বর্গের কাঠামো ভেঙে পড়ে। "
       "প্রতিটি ঘরে একটি কর্ণ দাও, পুরো সেতু নিজের আকারে আটকে যাবে। ভুলে গেলে ব্ল্যাক বক্স জানায় 'কাঠামোটি "
       "একটি যন্ত্রকৌশল ছিল - যথেষ্ট ত্রিভুজ নেই'।"),
    qa("What is the difference between Deck, Beam and Cable?",
       "Deck pieces are the road: vehicles drive only on deck pieces, and the road must join the "
       "left bank to the right bank. Beams are the structure that holds the deck up; they can be "
       "pulled or pushed. Cables can only be pulled - push one and it goes slack (grey) and "
       "carries nothing. All three are truss members with the same maths: a force N along "
       "their length.",
       "ডেক, বিম আর তারের পার্থক্য কী?",
       "ডেকের টুকরো হলো রাস্তা: গাড়ি শুধু ডেকের উপরেই চলে, আর রাস্তাকে বাঁ পাড় থেকে ডান পাড় পর্যন্ত "
       "জুড়তে হবে। বিম হলো সেই কাঠামো যা ডেককে ধরে রাখে; বিমকে টানা বা ঠেলা দুই-ই যায়। তারকে শুধু টানা "
       "যায় - ঠেললে তা ঢিলা (ধূসর) হয়ে যায় আর কোনো ভার নেয় না। তিনটিই ট্রাসের সদস্য, গণিতও এক: দৈর্ঘ্য "
       "বরাবর একটি বল N।"),
    qa("What are the anchors, and what is a pin or a roller?",
       "Anchors are the fixed joints in the rock where your bridge can rest. A pin holds a joint "
       "still in every direction. A roller holds it up but lets it slide sideways, so it cannot "
       "take a sideways push. Level 1 has pins at both banks at y = 0 and y = -3; Level 7 at y = 0 "
       "and y = -4. Level 8 has rollers at the banks plus pinned footings on the valley floor, and "
       "Level 10 has extra footings on the two islands.",
       "নোঙর কী, আর পিন বা রোলার কী?",
       "নোঙর হলো পাথরের মধ্যে স্থির জোড়, যার উপর তোমার সেতু ভর দেয়। পিন একটি জোড়কে সব দিকে স্থির রাখে। "
       "রোলার জোড়কে উপরে ধরে রাখে কিন্তু পাশে সরতে দেয়, তাই পাশের ঠেলা নিতে পারে না। লেভেল 1-এ দুই পাড়ে "
       "y = 0 আর y = -3-এ পিন আছে; লেভেল 7-এ y = 0 আর y = -4-এ। লেভেল 8-এ পাড়ে রোলার আর উপত্যকার তলায় "
       "পিন-করা পাদভিত্তি, আর লেভেল 10-এ দুই দ্বীপে বাড়তি পাদভিত্তি আছে।"),
    qa("How do joints and the grid work?",
       "Every click snaps to the grid (1 m in Level 1, 2 m in Levels 7, 8 and 10) or to a nearby "
       "existing joint. Two beams that end at the same point share one joint - that is how forces "
       "pass from member to member. You cannot build inside the rock. Joints with no beam "
       "disappear by themselves; anchors always stay.",
       "জোড় আর গ্রিড কীভাবে কাজ করে?",
       "প্রতিটি ক্লিক গ্রিডে (লেভেল 1-এ 1 m, লেভেল 7, 8 ও 10-এ 2 m) অথবা কাছের কোনো পুরোনো জোড়ে বসে যায়। "
       "একই বিন্দুতে শেষ হওয়া দুটি বিম একটি জোড় ভাগ করে - এভাবেই বল এক সদস্য থেকে আরেকটিতে যায়। পাথরের "
       "ভেতরে বানানো যায় না। কোনো বিম না থাকলে জোড় নিজেই মুছে যায়; নোঙর সবসময় থাকে।"),
    qa("Why can't I draw a longer beam?",
       "Each level limits member length: beams up to 8 m in Levels 1 and 8, 10 m in Level 7 and "
       "12 m in Level 10; cables up to 60 m (Level 7) and 80 m (Level 10). Real members are "
       "delivered in limited lengths, and long struts buckle easily anyway. To span further, add a "
       "joint in the middle and use two pieces - and brace that middle joint so it cannot bow.",
       "আরও লম্বা বিম আঁকতে পারি না কেন?",
       "প্রতিটি লেভেল সদস্যের দৈর্ঘ্য সীমিত রাখে: বিম লেভেল 1 ও 8-এ 8 m পর্যন্ত, লেভেল 7-এ 10 m আর লেভেল "
       "10-এ 12 m; তার 60 m (লেভেল 7) আর 80 m (লেভেল 10) পর্যন্ত। আসল সদস্য সীমিত দৈর্ঘ্যেই আসে, আর লম্বা "
       "ঠেকনা এমনিতেই সহজে বাকল করে। আরও দূরে যেতে মাঝখানে একটি জোড় দিয়ে দুটি টুকরো ব্যবহার করো - আর "
       "সেই মাঝের জোড়কে আটকে দাও যাতে তা বাঁকতে না পারে।"),
    qa("How does the game calculate the force in every beam?",
       "With the Direct Stiffness Method, the same method engineers' software uses. Each member "
       "acts like a stiff spring along its length with stiffness k = E A / L. All springs are added "
       "into one big matrix K, the supports are held still, and [K][U] = [F] is solved for how far "
       "every joint moves (U). Each member's stretch then gives its force N, its stress "
       "sigma = N / A and its strain epsilon = sigma / E.",
       "খেলাটি প্রতিটি বিমের বল কীভাবে হিসাব করে?",
       "ডাইরেক্ট স্টিফনেস মেথড দিয়ে - প্রকৌশলীদের সফটওয়্যারও এটিই ব্যবহার করে। প্রতিটি সদস্য তার দৈর্ঘ্য "
       "বরাবর একটি শক্ত স্প্রিংয়ের মতো, যার দৃঢ়তা k = E A / L। সব স্প্রিং যোগ করে একটি বড় ম্যাট্রিক্স K "
       "বানানো হয়, সাপোর্টগুলো স্থির রাখা হয়, আর [K][U] = [F] সমাধান করে বের হয় প্রতিটি জোড় কতটা সরে (U)। "
       "তারপর প্রতিটি সদস্যের প্রসারণ থেকে আসে তার বল N, পীড়ন sigma = N / A আর বিকৃতি epsilon = sigma / E।"),
    qa("How do I know if a beam is pulled (tension) or pushed (compression)?",
       "Click it with Select: the calculator says TENSION (pulled, N > 0) or COMPRESSION (pushed, "
       "N < 0). For a truss sitting above the deck and loaded from above, the top chord is "
       "squeezed and the bottom chord (the deck) is stretched - the bridge bends like a plank "
       "with its top side shortening. Diagonals alternate depending on their slope.",
       "কোন বিম টানা হচ্ছে (টান) আর কোনটি ঠেলা হচ্ছে (চাপ) কীভাবে বুঝব?",
       "'বাছাই' দিয়ে বিমে ক্লিক করো: ক্যালকুলেটর বলবে টান (টানা হচ্ছে, N > 0) নাকি চাপ (ঠেলা হচ্ছে, "
       "N < 0)। ডেকের উপরে থাকা ট্রাসে উপর থেকে ভার পড়লে উপরের কর্ড চাপে থাকে আর নিচের কর্ড (ডেক) টানে "
       "থাকে - সেতু একটি তক্তার মতো বাঁকে, যার উপরের দিক ছোট হয়। কর্ণগুলোর অবস্থা তাদের ঢাল অনুযায়ী "
       "পালাক্রমে বদলায়।"),
    qa("What does sigma = N / A mean?",
       "Stress sigma is the force N shared over the cross-section area A. The same 100 kN in a "
       "beam of 10 cm^2 (0.001 m^2) gives 100 MPa; in 40 cm^2 it gives only 25 MPa. A member "
       "fails by yielding or crushing when its stress passes the material's strength. That is why "
       "making A bigger makes a beam safer - but also heavier and more expensive.",
       "sigma = N / A মানে কী?",
       "পীড়ন sigma হলো প্রস্থচ্ছেদের ক্ষেত্রফল A জুড়ে ভাগ হওয়া বল N। একই 100 kN বল 10 cm^2 (0.001 m^2) "
       "বিমে 100 MPa পীড়ন দেয়; 40 cm^2-এ মাত্র 25 MPa। পীড়ন উপাদানের শক্তি পেরোলে সদস্যটি ছিঁড়ে বা চূর্ণ "
       "হয়ে যায়। তাই A বড় করলে বিম নিরাপদ হয় - তবে ভারী আর দামিও হয়।"),
    qa("What are strain and Young's modulus E?",
       "Strain epsilon = sigma / E is how much a member stretches or shortens per metre of length. "
       "E is the material's stiffness: steel 200 GPa, cables 190 GPa, concrete 30 GPa, timber "
       "11 GPa. A stiffer material stretches less for the same stress, so the bridge sags less "
       "(press Sag to see it) and its natural frequency is higher.",
       "বিকৃতি আর ইয়াং গুণাঙ্ক E কী?",
       "বিকৃতি epsilon = sigma / E হলো প্রতি মিটার দৈর্ঘ্যে সদস্য কতটা লম্বা বা ছোট হয়। E হলো উপাদানের "
       "দৃঢ়তা: ইস্পাত 200 GPa, তার 190 GPa, কংক্রিট 30 GPa, কাঠ 11 GPa। বেশি দৃঢ় উপাদান একই পীড়নে কম "
       "লম্বা হয়, তাই সেতু কম ঝোলে ('ঝোলা' চেপে দেখো) আর তার স্বাভাবিক কম্পাঙ্ক বেশি হয়।"),
    qa("How strong is each material?",
       "Pull / push strength: Timber 40 / 30 MPa. Steel 250 / 250 MPa. Concrete 0 / 30 MPa "
       "(it cracks if pulled). Steel cable 1500 MPa when pulled, nothing when pushed. Carbon-fibre "
       "cable 2400 MPa pulled. Nanotube cable practically unbreakable when pulled. Smart alloy "
       "700 / 700 MPa. Pushed members can buckle long before reaching these numbers.",
       "কোন উপাদান কতটা শক্ত?",
       "টানা / ঠেলার শক্তি: কাঠ 40 / 30 MPa। ইস্পাত 250 / 250 MPa। কংক্রিট 0 / 30 MPa (টানলে ফেটে যায়)। "
       "ইস্পাতের তার টানলে 1500 MPa, ঠেললে কিছুই না। কার্বন-ফাইবার তার টানলে 2400 MPa। ন্যানোটিউব তার টানলে "
       "কার্যত অভঙ্গুর। স্মার্ট সংকর ধাতু 700 / 700 MPa। ঠেলা সদস্য এই সংখ্যায় পৌঁছানোর অনেক আগেই বাকল "
       "করতে পারে।"),
    qa("How heavy and how expensive is each material?",
       "Density and price per kg: Timber 500 kg/m^3, Rs 60. Steel 7850 kg/m^3, Rs 90. Concrete "
       "2400 kg/m^3, Rs 8. Steel cable 7850 kg/m^3, Rs 160. Carbon fibre 1600 kg/m^3, Rs 2500. "
       "Nanotube 1300 kg/m^3, Rs 9000. Smart alloy 6500 kg/m^3, Rs 1500. Member cost = density x "
       "A x L x price x shape factor. Example: 1 m of steel I-beam size M costs about Rs 1,625; "
       "1 m of timber I-beam M only about Rs 69.",
       "কোন উপাদান কতটা ভারী আর কতটা দামি?",
       "ঘনত্ব আর প্রতি kg দাম: কাঠ 500 kg/m^3, Rs 60। ইস্পাত 7850 kg/m^3, Rs 90। কংক্রিট 2400 kg/m^3, Rs 8। "
       "ইস্পাতের তার 7850 kg/m^3, Rs 160। কার্বন ফাইবার 1600 kg/m^3, Rs 2500। ন্যানোটিউব 1300 kg/m^3, "
       "Rs 9000। স্মার্ট সংকর ধাতু 6500 kg/m^3, Rs 1500। সদস্যের দাম = ঘনত্ব x A x L x দাম x গড়নের গুণক। "
       "উদাহরণ: সাইজ M ইস্পাতের আই-বিমের 1 m প্রায় Rs 1,625; কাঠের আই-বিম M-এর 1 m মাত্র প্রায় Rs 69।"),
    # --- buckling ---------------------------------------------------------------------
    qa("Why do pushed members fail earlier than pulled ones?",
       "A pulled member only fails when its stress reaches the material strength (sigma = N / A). "
       "A pushed member can also bow sideways and fold - buckling - at the Euler load "
       "P_cr = pi^2 E I / (K L)^2, which for long thin members is far below the crushing load. "
       "Each pushed member's limit is the smaller of the two: crushing (strength x A) or P_cr. In "
       "this game K = 1 (pinned at both ends).",
       "ঠেলা সদস্য টানা সদস্যের আগে ভাঙে কেন?",
       "টানা সদস্য ভাঙে শুধু তখন, যখন তার পীড়ন উপাদানের শক্তিতে পৌঁছায় (sigma = N / A)। ঠেলা সদস্য পাশে "
       "বেঁকে ভাঁজও হয়ে যেতে পারে - বাকলিং - অয়লারের ভার P_cr = pi^2 E I / (K L)^2-এ, যা লম্বা সরু সদস্যের "
       "জন্য চূর্ণ হওয়ার ভারের চেয়ে অনেক কম। প্রতিটি ঠেলা সদস্যের সীমা দুটির মধ্যে ছোটটি: চূর্ণ হওয়া "
       "(শক্তি x A) অথবা P_cr। এই খেলায় K = 1 (দুই প্রান্তে পিন)।"),
    qa("Why is shortening a pushed member so powerful?",
       "Because P_cr grows with 1 / L^2. Halve the length and the buckling load becomes 4 times "
       "bigger; cut it to a third and it becomes 9 times bigger. Example: a steel I-beam size M "
       "buckles at about 56 kN when 8 m long but about 222 kN when 4 m long. Add a joint in the "
       "middle of a long strut and brace it, or use more, smaller panels.",
       "ঠেলা সদস্য ছোট করা এত কাজের কেন?",
       "কারণ P_cr বাড়ে 1 / L^2 অনুপাতে। দৈর্ঘ্য অর্ধেক করলে বাকলিং ভার 4 গুণ হয়; এক-তৃতীয়াংশ করলে 9 গুণ। "
       "উদাহরণ: সাইজ M ইস্পাতের আই-বিম 8 m লম্বা হলে প্রায় 56 kN-এ বাকল করে, কিন্তু 4 m লম্বা হলে প্রায় "
       "222 kN-এ। লম্বা ঠেকনার মাঝে একটি জোড় দিয়ে তাকে আটকে দাও, অথবা বেশি সংখ্যক ছোট ঘর ব্যবহার করো।"),
    qa("What is I, and why does the shape matter?",
       "I (second moment of area) measures how far the material sits from the centre of the "
       "section; the further out, the harder the member is to bend or buckle. In this game "
       "I = factor x A^2: Solid square 1/12, I-beam 0.45, Hollow box 0.8. For the same amount of "
       "material an I-beam is about 5.4 times and a hollow box about 9.6 times stiffer against "
       "buckling than a solid square.",
       "I কী, আর গড়ন গুরুত্বপূর্ণ কেন?",
       "I (ক্ষেত্রফলের দ্বিতীয় ভ্রামক) মাপে উপাদান প্রস্থচ্ছেদের কেন্দ্র থেকে কত দূরে আছে; যত দূরে, সদস্যকে "
       "বাঁকানো বা বাকল করানো তত কঠিন। এই খেলায় I = গুণক x A^2: নিরেট বর্গ 1/12, আই-বিম 0.45, ফাঁপা বাক্স "
       "0.8। একই পরিমাণ উপাদানে আই-বিম নিরেট বর্গের চেয়ে প্রায় 5.4 গুণ আর ফাঁপা বাক্স প্রায় 9.6 গুণ বেশি "
       "বাকলিং ঠেকায়।"),
    qa("Does a bigger area help against buckling?",
       "Yes, a lot. Because I = factor x A^2 here, doubling A makes I four times bigger, so P_cr "
       "rises 4 times - while the crushing and pulling strength (strength x A) only doubles. "
       "Example: a timber hollow box 4 m long buckles at about 22 kN in size M but about 347 kN in "
       "size XL. But doubling A also doubles the weight and material cost, so try a better shape "
       "or a shorter length first.",
       "বড় ক্ষেত্রফল কি বাকলিং ঠেকাতে সাহায্য করে?",
       "হ্যাঁ, অনেক। এখানে I = গুণক x A^2, তাই A দ্বিগুণ করলে I চার গুণ হয়, ফলে P_cr 4 গুণ বাড়ে - যেখানে "
       "চূর্ণ হওয়া আর টানার শক্তি (শক্তি x A) শুধু দ্বিগুণ হয়। উদাহরণ: 4 m লম্বা কাঠের ফাঁপা বাক্স সাইজ M-এ "
       "প্রায় 22 kN-এ বাকল করে, কিন্তু সাইজ XL-এ প্রায় 347 kN-এ। তবে A দ্বিগুণ করলে ওজন আর উপাদানের "
       "খরচও দ্বিগুণ হয়, তাই আগে ভালো গড়ন বা ছোট দৈর্ঘ্য চেষ্টা করো।"),
    qa("How do I tell whether buckling or crushing will break a pushed member?",
       "Compare the two limits. Crushing: compressive strength x A. Buckling: P_cr. The smaller "
       "one wins. A steel I-beam size M crushes at 500 kN; at 4 m long it buckles first at "
       "222 kN, but at 2 m long P_cr is about 888 kN, so it would crush first. The calculator "
       "shows both numbers for the beam you select.",
       "ঠেলা সদস্যকে বাকলিং ভাঙবে নাকি চূর্ণ হওয়া - কীভাবে বুঝব?",
       "দুটি সীমা তুলনা করো। চূর্ণ: চাপ-শক্তি x A। বাকলিং: P_cr। যেটি ছোট সেটিই আগে ঘটে। সাইজ M ইস্পাতের "
       "আই-বিম 500 kN-এ চূর্ণ হয়; 4 m লম্বা হলে আগে 222 kN-এ বাকল করে, কিন্তু 2 m লম্বা হলে P_cr প্রায় "
       "888 kN, তাই আগে চূর্ণ হবে। বাছাই করা বিমের জন্য ক্যালকুলেটর দুটি সংখ্যাই দেখায়।"),
    # --- sizing -----------------------------------------------------------------------
    qa("What do the sizes S, M, L and XL mean?",
       "They are cross-section areas. Beams: S = 10 cm^2, M = 20 cm^2, L = 40 cm^2, XL = 80 cm^2. "
       "Cables: S = 5, M = 10, L = 20, XL = 40 cm^2. Each step doubles the area, the weight and the "
       "material cost. With the Select tool you can also slide any single beam's area anywhere "
       "from 3 to 200 cm^2 in the calculator.",
       "S, M, L আর XL সাইজের মানে কী?",
       "এগুলো প্রস্থচ্ছেদের ক্ষেত্রফল। বিম: S = 10 cm^2, M = 20 cm^2, L = 40 cm^2, XL = 80 cm^2। তার: S = 5, "
       "M = 10, L = 20, XL = 40 cm^2। প্রতিটি ধাপে ক্ষেত্রফল, ওজন আর উপাদানের খরচ দ্বিগুণ হয়। 'বাছাই' টুল "
       "দিয়ে ক্যালকুলেটরে যেকোনো একটি বিমের ক্ষেত্রফল 3 থেকে 200 cm^2-এর মধ্যে স্লাইড করেও বদলাতে পারো।"),
    qa("How do I size a pulled member with no waste?",
       "Use A_min = FS x N / sigma_t, where FS is the factor of safety you want (1.5-2 is the sweet "
       "spot). Example: a steel tie pulling 100 kN with FS = 1.75 needs 1.75 x 100,000 / 250e6 = "
       "0.0007 m^2 = 7 cm^2, so size S (10 cm^2) is enough. Area above A_min only adds weight and "
       "cost. Shape does not matter in tension, so the cheapest solid square is fine for ties.",
       "টানা সদস্যের মাপ অপচয় ছাড়া কীভাবে ঠিক করব?",
       "A_min = FS x N / sigma_t ব্যবহার করো, যেখানে FS তোমার চাওয়া নিরাপত্তা গুণক (1.5-2 সবচেয়ে ভালো)। "
       "উদাহরণ: 100 kN টানা একটি ইস্পাতের টাই-এ FS = 1.75 হলে লাগে 1.75 x 100,000 / 250e6 = 0.0007 m^2 = "
       "7 cm^2, তাই সাইজ S (10 cm^2) যথেষ্ট। A_min-এর বেশি ক্ষেত্রফল শুধু ওজন আর খরচ বাড়ায়। টানে গড়নের "
       "কোনো ভূমিকা নেই, তাই টাই-এর জন্য সবচেয়ে সস্তা নিরেট বর্গই ঠিক।"),
    qa("How do I size a pushed member?",
       "It must pass two checks. Crushing: A >= FS x N / sigma_c. Buckling: I >= FS x N x L^2 / "
       "(pi^2 E), and since I = factor x A^2, A >= sqrt(I / factor). Take the bigger A. Example: "
       "a 4 m steel strut pushed by 100 kN with FS = 1.75 needs I >= 1.42e-6 m^4; as an I-beam "
       "that is A >= sqrt(1.42e-6 / 0.45) = 17.7 cm^2, so size M (20 cm^2).",
       "ঠেলা সদস্যের মাপ কীভাবে ঠিক করব?",
       "দুটি পরীক্ষায় পাস করতে হবে। চূর্ণ: A >= FS x N / sigma_c। বাকলিং: I >= FS x N x L^2 / (pi^2 E), আর "
       "যেহেতু I = গুণক x A^2, তাই A >= sqrt(I / গুণক)। বড় A-টি নাও। উদাহরণ: 100 kN ঠেলা খাওয়া 4 m ইস্পাতের "
       "ঠেকনায় FS = 1.75 হলে লাগে I >= 1.42e-6 m^4; আই-বিম হলে A >= sqrt(1.42e-6 / 0.45) = 17.7 cm^2, তাই "
       "সাইজ M (20 cm^2)।"),
    # --- truss types -------------------------------------------------------------------
    qa("Which members of a Pratt truss are pulled and which are pushed?",
       "In a Pratt truss the diagonals slope down towards the middle of the span. Under downward "
       "loads those diagonals are pulled (tension), the verticals are pushed (compression), the "
       "top chord is pushed and the bottom chord is pulled. That is efficient: the long diagonals "
       "only need tension area, while the short verticals are the struts - and short struts "
       "resist buckling well.",
       "প্র্যাট ট্রাসের কোন সদস্য টানা আর কোনটি ঠেলা হয়?",
       "প্র্যাট ট্রাসে কর্ণগুলো স্প্যানের মাঝের দিকে নিচে নামে। নিচের দিকে ভার পড়লে এই কর্ণগুলো টানে "
       "থাকে, খাড়া সদস্যগুলো চাপে, উপরের কর্ড চাপে আর নিচের কর্ড টানে। এটি দক্ষ: লম্বা কর্ণগুলোর শুধু টানের "
       "ক্ষেত্রফল লাগে, আর ছোট খাড়া সদস্যগুলো ঠেকনা - ছোট ঠেকনা বাকলিং ভালোভাবে ঠেকায়।"),
    qa("What is a Warren truss and why does the Level 1 demo use it?",
       "A Warren truss is a row of equal triangles with no verticals: the diagonals take turns "
       "being pulled and pushed. It needs few members and few joints, which keeps labour low. The "
       "Level 1 demo is just two big triangles of timber hollow box, 3 m high: few joints, short "
       "enough struts and a shape that resists buckling.",
       "ওয়ারেন ট্রাস কী, আর লেভেল 1-এর প্রদর্শনী এটি কেন ব্যবহার করে?",
       "ওয়ারেন ট্রাস হলো খাড়া সদস্য ছাড়া সমান ত্রিভুজের একটি সারি: কর্ণগুলো পালা করে টানা আর ঠেলা হয়। "
       "এতে কম সদস্য আর কম জোড় লাগে, তাই শ্রমের খরচ কম থাকে। লেভেল 1-এর প্রদর্শনী হলো কাঠের ফাঁপা বাক্সের "
       "মাত্র দুটি বড় ত্রিভুজ, 3 m উঁচু: কম জোড়, যথেষ্ট ছোট ঠেকনা আর বাকলিং-ঠেকানো গড়ন।"),
    qa("What about a Howe truss?",
       "A Howe truss is the mirror of a Pratt: its diagonals slope up towards the middle, so under "
       "downward loads the long diagonals are pushed and the verticals are pulled. Long pushed "
       "diagonals buckle easily, so in steel a Howe usually needs bigger diagonals than a Pratt. "
       "Try both in the game and compare the colours and the cost.",
       "হাউ ট্রাস কেমন?",
       "হাউ ট্রাস প্র্যাটের আয়নার প্রতিচ্ছবি: এর কর্ণগুলো মাঝের দিকে উপরে ওঠে, তাই নিচের দিকে ভার পড়লে "
       "লম্বা কর্ণগুলো চাপে আর খাড়া সদস্যগুলো টানে থাকে। লম্বা ঠেলা কর্ণ সহজে বাকল করে, তাই ইস্পাতে হাউ "
       "ট্রাসে সাধারণত প্র্যাটের চেয়ে বড় কর্ণ লাগে। খেলায় দুটিই বানিয়ে রং আর খরচ তুলনা করো।"),
    qa("How deep (tall) should my truss be?",
       "The chords work like the top and bottom of a giant beam: chord force is about M / h, where "
       "M is the bending moment of the whole span and h the truss depth. Double the depth and the "
       "chord forces halve. But deeper means longer diagonals (which may buckle), more material "
       "and more scaffolding cost. A depth of about 1/5 to 1/8 of the span is a good start (3 m for "
       "the 16 m creek).",
       "আমার ট্রাস কতটা গভীর (উঁচু) হওয়া উচিত?",
       "কর্ডগুলো একটি বিশাল বিমের উপর আর নিচের অংশের মতো কাজ করে: কর্ডের বল প্রায় M / h, যেখানে M পুরো "
       "স্প্যানের বাঁকানো ভ্রামক আর h ট্রাসের গভীরতা। গভীরতা দ্বিগুণ করলে কর্ডের বল অর্ধেক হয়। কিন্তু বেশি "
       "গভীর মানে লম্বা কর্ণ (বাকল করতে পারে), বেশি উপাদান আর বেশি ভারা-খরচ। স্প্যানের প্রায় 1/5 থেকে 1/8 "
       "গভীরতা দিয়ে শুরু করা ভালো (16 m খাঁড়ির জন্য 3 m)।"),
    qa("How many panels (triangles) should I use?",
       "More panels mean shorter members, which buckle much less (P_cr ~ 1 / L^2), and shorter deck "
       "pieces that spread the wheel loads. But every member costs Rs 2,500 of labour and every "
       "new joint Rs 4,000. For short spans and light loads (Level 1) a few big panels are "
       "cheapest; for heavy buses (Level 7) or long spans use more panels.",
       "কতগুলো ঘর (ত্রিভুজ) ব্যবহার করব?",
       "বেশি ঘর মানে ছোট সদস্য, যারা অনেক কম বাকল করে (P_cr ~ 1 / L^2), আর ছোট ডেক টুকরো, যারা চাকার ভার "
       "ছড়িয়ে দেয়। কিন্তু প্রতিটি সদস্যে Rs 2,500 শ্রম আর প্রতিটি নতুন জোড়ে Rs 4,000 খরচ। ছোট স্প্যান আর "
       "হালকা ভারে (লেভেল 1) কয়েকটি বড় ঘরই সবচেয়ে সস্তা; ভারী বাস (লেভেল 7) বা লম্বা স্প্যানে বেশি ঘর "
       "ব্যবহার করো।"),
    qa("Should I build the truss above or below the deck?",
       "Above (a 'through' truss) works everywhere and only needs the bank anchors at deck level. "
       "Below (a 'deck' truss) keeps the space above the road clear, but it must rest on anchors "
       "below the deck: y = -3 in Level 1 and y = -4 in Level 7. In Levels 8 and 10 the deck "
       "stands on columns or V-piers from footings far below.",
       "ট্রাস ডেকের উপরে বানাব নাকি নিচে?",
       "উপরে ('থ্রু' ট্রাস) সব জায়গায় চলে, আর শুধু ডেকের উচ্চতায় পাড়ের নোঙর লাগে। নিচে ('ডেক' ট্রাস) রাস্তার "
       "উপরের জায়গা ফাঁকা রাখে, কিন্তু তাকে ডেকের নিচের নোঙরে ভর দিতে হয়: লেভেল 1-এ y = -3 আর লেভেল 7-এ "
       "y = -4। লেভেল 8 আর 10-এ ডেক দাঁড়ায় অনেক নিচের পাদভিত্তি থেকে ওঠা স্তম্ভ বা V-স্তম্ভের উপর।"),
    qa("What is a zero-force member? Can I delete it?",
       "A member that carries no force for the loads in the test shows 'Unloaded (zero-force "
       "member)'. It may still be needed: it can keep the frame from becoming a mechanism, or carry "
       "load when the vehicle stands somewhere else. Delete it, run TEST again, and keep the "
       "change only if nothing turns red and the frame stays stable - each member removed saves "
       "its material plus Rs 2,500 of labour.",
       "শূন্য-বল সদস্য কী? আমি কি মুছে দিতে পারি?",
       "পরীক্ষার ভারে যে সদস্য কোনো বল বয় না, সেটি দেখায় 'ভারহীন (শূন্য-বল সদস্য)'। তবুও তার দরকার থাকতে "
       "পারে: সে কাঠামোকে যন্ত্রকৌশল হয়ে যাওয়া থেকে বাঁচাতে পারে, বা গাড়ি অন্য জায়গায় থাকলে ভার নিতে পারে। "
       "মুছে দাও, আবার 'পরীক্ষা' চালাও, আর কিছু লাল না হলে ও কাঠামো স্থির থাকলে তবেই পরিবর্তন রাখো - প্রতিটি "
       "সদস্য সরালে তার উপাদান আর Rs 2,500 শ্রম বাঁচে।"),
    qa("Is there a quick way to check that my frame is stable?",
       "Count: members m, joints j, support restraints r (a pin gives 2, a roller 1). A 2D truss "
       "needs at least m + r >= 2 j to be stable. If it has fewer, some joint can move freely and "
       "the solver reports a mechanism. Enough members is necessary but not sufficient - they must "
       "also form triangles, not just squares with an extra diagonal somewhere else.",
       "কাঠামো স্থির কিনা দ্রুত বোঝার উপায় আছে?",
       "গুনে দেখো: সদস্য m, জোড় j, সাপোর্টের বাঁধন r (পিন দেয় 2, রোলার 1)। স্থির হতে 2D ট্রাসের অন্তত "
       "m + r >= 2 j লাগে। এর কম হলে কোনো জোড় মুক্তভাবে সরতে পারে আর সমাধানকারী যন্ত্রকৌশলের খবর দেয়। "
       "যথেষ্ট সদস্য থাকা জরুরি কিন্তু যথেষ্ট নয় - তাদের ত্রিভুজও গড়তে হবে, অন্য কোথাও একটি বাড়তি কর্ণসহ "
       "শুধু বর্গ নয়।"),
    # --- loads ------------------------------------------------------------------------
    qa("Does the bridge's own weight count?",
       "Yes. Every member's weight W = rho A L g is shared half to each of its end joints, and "
       "every deck piece also carries the road surface: 1500 N per metre in Level 1, 12,000 N/m in "
       "Level 7, and 3000 N/m in Levels 8 and 10. Heavy members add load that other members must "
       "carry, so oversizing everything can make forces grow - a reason steel is not always "
       "better than timber.",
       "সেতুর নিজের ওজন কি হিসাবে ধরা হয়?",
       "হ্যাঁ। প্রতিটি সদস্যের ওজন W = rho A L g তার দুই প্রান্তের জোড়ে অর্ধেক অর্ধেক ভাগ হয়, আর প্রতিটি "
       "ডেক টুকরো রাস্তার আস্তরণও বয়: লেভেল 1-এ প্রতি মিটারে 1500 N, লেভেল 7-এ 12,000 N/m, আর লেভেল 8 ও "
       "10-এ 3000 N/m। ভারী সদস্য এমন ভার যোগ করে যা অন্য সদস্যদের বইতে হয়, তাই সবকিছু বড় করলে বল বাড়তে "
       "পারে - এজন্যই ইস্পাত সবসময় কাঠের চেয়ে ভালো নয়।"),
    qa("Where is the vehicle when TEST checks my bridge?",
       "TEST places one vehicle at 9 positions along the deck and shows the worst one. The middle "
       "of the span is usually worst for the chords; positions near the banks are often worst for "
       "the end diagonals. During RUN everything really moves - several buses in Level 7, wind and "
       "earthquakes - so the real run can be harder than TEST. Keep some margin.",
       "'পরীক্ষা' যখন সেতু যাচাই করে, গাড়ি তখন কোথায় থাকে?",
       "'পরীক্ষা' একটি গাড়িকে ডেক বরাবর 9টি জায়গায় রেখে সবচেয়ে খারাপটি দেখায়। কর্ডের জন্য সাধারণত স্প্যানের "
       "মাঝখান সবচেয়ে খারাপ; পাড়ের কাছের জায়গা প্রায়ই প্রান্তের কর্ণের জন্য খারাপ। 'চালাও'-তে সত্যিই সব "
       "চলে - লেভেল 7-এ কয়েকটি বাস, বাতাস আর ভূমিকম্প - তাই আসল চালানো 'পরীক্ষা'-র চেয়ে কঠিন হতে পারে। "
       "কিছুটা বাড়তি নিরাপত্তা রাখো।"),
    qa("How does a wheel's weight reach the truss?",
       "The vehicle's weight is shared between its axles. Each axle stands on one deck piece, and "
       "its load is split between that piece's two end joints in proportion to how close it is "
       "to each. So the deck only passes loads to joints - shorter deck pieces mean more joints to "
       "share the load and smaller forces in each member below.",
       "চাকার ওজন ট্রাসে কীভাবে পৌঁছায়?",
       "গাড়ির ওজন তার অ্যাক্সেলগুলোর মধ্যে ভাগ হয়। প্রতিটি অ্যাক্সেল একটি ডেক টুকরোর উপর থাকে, আর তার ভার "
       "সেই টুকরোর দুই প্রান্তের জোড়ে ভাগ হয় - যে জোড়ের যত কাছে, তার ভাগ তত বেশি। তাই ডেক শুধু জোড়েই ভার "
       "পাঠায় - ছোট ডেক টুকরো মানে ভার ভাগ করার জন্য বেশি জোড়, আর নিচের প্রতিটি সদস্যে কম বল।"),
    # --- safety factor ----------------------------------------------------------------
    qa("What is the factor of safety (FS)?",
       "FS = capacity / demand = 1 / (worst load ratio). If the most loaded member is at 50% of "
       "its limit, FS = 2. Grades: below 1 FAILED; 1-1.5 RISKY; 1.5-2 OPTIMAL (safe without waste); "
       "2-4 CONSERVATIVE; above 4 OVER-ENGINEERED. The third star needs FS between 1.5 and 4.",
       "নিরাপত্তা গুণক (FS) কী?",
       "FS = ক্ষমতা / চাহিদা = 1 / (সবচেয়ে বেশি ভার-অনুপাত)। সবচেয়ে ভারী সদস্য তার সীমার 50%-এ থাকলে "
       "FS = 2। মান: 1-এর নিচে ব্যর্থ; 1-1.5 ঝুঁকিপূর্ণ; 1.5-2 সর্বোত্তম (অপচয় ছাড়া নিরাপদ); 2-4 বেশি "
       "সাবধানী; 4-এর উপরে অতিরিক্ত মজবুত। তৃতীয় তারার জন্য FS 1.5 থেকে 4-এর মধ্যে লাগে।"),
    qa("What does the line 'TEST: worst member 63% -> FS 1.59' mean?",
       "It is the live summary of TEST. The most heavily loaded member is at 63% of what it can "
       "carry, so the factor of safety of the whole bridge is 1 / 0.63 = 1.59, and the grade in "
       "brackets (here OPTIMAL) tells you whether that is risky, just right or wasteful. Watch it "
       "change as you resize members - it is the fastest way to tune a design.",
       "'পরীক্ষা: সবচেয়ে বেশি ভারের সদস্য 63% -> FS 1.59' লাইনের মানে কী?",
       "এটি 'পরীক্ষা'-র সরাসরি সারাংশ। সবচেয়ে বেশি ভার পাওয়া সদস্যটি যতটা বইতে পারে তার 63%-এ আছে, তাই পুরো "
       "সেতুর নিরাপত্তা গুণক 1 / 0.63 = 1.59, আর বন্ধনীর মান (এখানে সর্বোত্তম) বলে সেটা ঝুঁকিপূর্ণ, ঠিকঠাক নাকি "
       "অপচয়। সদস্যের মাপ বদলানোর সঙ্গে সঙ্গে এটি বদলাতে দেখো - নকশা ঠিক করার এটাই সবচেয়ে দ্রুত উপায়।"),
    qa("Why not just make the FS 5 or 10 to be safe?",
       "Because strength costs money. A bridge with FS 5 carries 5 times the load it will ever "
       "see, so you paid for strength you never use - and it can push the cost over par or even "
       "over budget. Above FS 4 the business plan also charges an over-engineering penalty of 5% "
       "of the budget for each point above 4 (up to 30%). Engineers aim for 1.5-2.",
       "নিরাপদ থাকতে FS 5 বা 10 করলেই তো হয়?",
       "কারণ শক্তির দাম আছে। FS 5-এর সেতু যত ভার কখনো দেখবে তার 5 গুণ বইতে পারে, অর্থাৎ যে শক্তি কখনো কাজে "
       "লাগবে না তার দাম দিয়েছ - আর তাতে খরচ প্যারের উপরে, এমনকি বাজেটের উপরেও যেতে পারে। FS 4-এর উপরে "
       "ব্যবসার পরিকল্পনা প্রতিটি অতিরিক্ত পয়েন্টে বাজেটের 5% (সর্বোচ্চ 30%) অতিরিক্ত-মজবুতের জরিমানাও কাটে। "
       "প্রকৌশলীরা 1.5-2 লক্ষ্য রাখেন।"),
    # --- materials in practice -----------------------------------------------------------
    qa("Timber or steel for Level 1?",
       "Timber. Its material is so cheap (about Rs 30-310 per metre depending on size and shape) "
       "that labour - Rs 2,500 per member and Rs 4,000 per new joint - is most of the cost. The van "
       "is light, so a few large timber members with a hollow-box or I-beam shape pass easily. "
       "Steel costs about Rs 700-7,300 per metre and makes sense only where forces are high.",
       "লেভেল 1-এ কাঠ নাকি ইস্পাত?",
       "কাঠ। এর উপাদান এত সস্তা (আকার আর গড়ন অনুযায়ী প্রতি মিটারে প্রায় Rs 30-310) যে খরচের বেশিরভাগই "
       "শ্রম - প্রতি সদস্যে Rs 2,500 আর প্রতি নতুন জোড়ে Rs 4,000। ভ্যানটি হালকা, তাই ফাঁপা বাক্স বা আই-বিম "
       "গড়নের কয়েকটি বড় কাঠের সদস্য সহজেই পাস করে। ইস্পাতের খরচ প্রতি মিটারে প্রায় Rs 700-7,300, তাই "
       "শুধু যেখানে বল বেশি সেখানেই এটি যুক্তিসঙ্গত।"),
    qa("Since labour is so expensive, how do I save on it?",
       "Use fewer, better members. Every member costs Rs 2,500 to place and every joint that is "
       "not an anchor costs Rs 4,000 to bolt or weld. Big triangles, members ending on the anchors, "
       "and no decorative extras keep labour down. Members high above the ground also pay "
       "scaffolding: about Rs 300 per metre of height.",
       "শ্রম যেহেতু এত দামি, কীভাবে বাঁচাব?",
       "কম কিন্তু ভালো সদস্য ব্যবহার করো। প্রতিটি সদস্য বসাতে Rs 2,500 আর নোঙর নয় এমন প্রতিটি জোড় বল্টু বা "
       "ঝালাই করতে Rs 4,000 খরচ। বড় ত্রিভুজ, নোঙরে শেষ হওয়া সদস্য আর বাড়তি সাজসজ্জা না থাকলে শ্রমের খরচ "
       "কম থাকে। মাটি থেকে অনেক উঁচুতে থাকা সদস্যের ভারার খরচও লাগে: প্রতি মিটার উচ্চতায় প্রায় Rs 300।"),
    qa("When is steel worth its price?",
       "Where forces are large: heavy buses (Level 7), trucks during an earthquake (Level 8) and "
       "the maglev (Level 10). Steel is 6-8 times stronger than timber and 18 times stiffer, so a "
       "steel member can be much smaller - and stiffness also raises the natural frequency that "
       "keeps a bridge safe from wind.",
       "ইস্পাত কখন তার দামের যোগ্য?",
       "যেখানে বল বড়: ভারী বাস (লেভেল 7), ভূমিকম্পের মধ্যে ট্রাক (লেভেল 8) আর ম্যাগলেভ (লেভেল 10)। ইস্পাত "
       "কাঠের চেয়ে 6-8 গুণ শক্ত আর 18 গুণ দৃঢ়, তাই ইস্পাতের সদস্য অনেক ছোট হতে পারে - আর দৃঢ়তা সেই স্বাভাবিক "
       "কম্পাঙ্কও বাড়ায় যা সেতুকে বাতাস থেকে নিরাপদ রাখে।"),
    qa("Where should I use concrete?",
       "Only in members that are always pushed - columns and struts. Plain concrete has zero "
       "tensile strength: the moment it is pulled it cracks and fails. It is very cheap (Rs 8 per "
       "kg) and strong when squeezed (30 MPa). Careful in Level 8: an earthquake shakes the bridge "
       "both ways, so a brace that is pushed now may be pulled a moment later.",
       "কংক্রিট কোথায় ব্যবহার করব?",
       "শুধু সেই সদস্যে যা সবসময় ঠেলা খায় - স্তম্ভ আর ঠেকনা। সাধারণ কংক্রিটের টানার শক্তি শূন্য: টানা পড়লেই "
       "ফেটে ভেঙে যায়। এটি খুব সস্তা (প্রতি kg Rs 8) আর চাপে শক্ত (30 MPa)। লেভেল 8-এ সাবধান: ভূমিকম্প সেতুকে "
       "দুই দিকেই ঝাঁকায়, তাই যে ঠেকনা এখন ঠেলা খাচ্ছে, পরমুহূর্তে সেটি টানা খেতে পারে।"),
    qa("How should I use cables?",
       "Only where the force is a pull: hangers and stays from a tall tower to the deck (Levels 7 "
       "and 10). A steel cable carries 1500 MPa - six times steel beams - so it can be thin. If a "
       "cable would be pushed it goes slack (grey) and does nothing, so the rest of the frame must "
       "still be stable. Towers that hold the cables are pushed and must resist buckling.",
       "তার কীভাবে ব্যবহার করব?",
       "শুধু যেখানে বল টান: উঁচু টাওয়ার থেকে ডেকে ঝোলানো তার (লেভেল 7 ও 10)। ইস্পাতের তার 1500 MPa বয় - "
       "ইস্পাতের বিমের ছয় গুণ - তাই সরু হতে পারে। কোনো তার ঠেলা খেলে তা ঢিলা (ধূসর) হয়ে কোনো কাজ করে না, "
       "তাই বাকি কাঠামোকে তবুও স্থির থাকতে হবে। যে টাওয়ার তারগুলো ধরে রাখে সেগুলো ঠেলা খায়, তাই বাকলিং "
       "ঠেকাতে হবে।"),
    qa("Is carbon-fibre cable worth it?",
       "It is stronger (2400 MPa) and much lighter (1600 kg/m^3) than steel cable, but it costs "
       "Rs 2,500 per kg against Rs 160. Per newton of pull it is still several times dearer than "
       "steel cable. Use it only where saving weight really matters, for example long stays in "
       "Level 10 where the cable's own weight adds up.",
       "কার্বন-ফাইবার তার কি দামের যোগ্য?",
       "এটি ইস্পাতের তারের চেয়ে বেশি শক্ত (2400 MPa) আর অনেক হালকা (1600 kg/m^3), কিন্তু দাম প্রতি kg "
       "Rs 2,500, যেখানে ইস্পাতের তার Rs 160। প্রতি নিউটন টানে এটি এখনো ইস্পাতের তারের চেয়ে কয়েক গুণ দামি। "
       "শুধু যেখানে ওজন কমানো সত্যিই জরুরি সেখানে ব্যবহার করো, যেমন লেভেল 10-এর লম্বা তার, যেখানে তারের "
       "নিজের ওজনই অনেক।"),
    qa("What are nanotube cable and smart alloy (Level 10)?",
       "Future materials. Nanotube cable is practically unbreakable when pulled (but cannot push) "
       "and costs Rs 9,000 per kg. Smart alloy is a 700 MPa metal whose stiffness E doubles (70 to "
       "140 GPa) when the smart grid powers it - 'Power the smart alloy' in the lab - drawing 50 kW "
       "for each tonne of alloy. Both are expensive: use them only where they solve a real problem.",
       "ন্যানোটিউব তার আর স্মার্ট সংকর ধাতু কী (লেভেল 10)?",
       "ভবিষ্যতের উপাদান। ন্যানোটিউব তার টানলে কার্যত অভঙ্গুর (কিন্তু ঠেলতে পারে না), দাম প্রতি kg Rs 9,000। "
       "স্মার্ট সংকর ধাতু 700 MPa শক্তির একটি ধাতু, যার দৃঢ়তা E স্মার্ট গ্রিড চালু করলে দ্বিগুণ হয় (70 থেকে "
       "140 GPa) - ল্যাবে 'স্মার্ট সংকর ধাতু চালু করো' - আর প্রতি টন ধাতুর জন্য 50 kW নেয়। দুটিই দামি: শুধু "
       "যেখানে সত্যিকারের সমস্যা মেটায় সেখানেই ব্যবহার করো।"),
    qa("Does timber get weaker when wet?",
       "Yes. In a wet or humid level timber keeps only 70% of its strength (moisture factor 0.7). "
       "Steel and concrete are not affected in the game. If a level is wet, size timber members "
       "with that in mind or switch the most loaded ones to steel.",
       "ভেজা হলে কি কাঠ দুর্বল হয়?",
       "হ্যাঁ। ভেজা বা আর্দ্র লেভেলে কাঠ তার শক্তির মাত্র 70% রাখে (আর্দ্রতা গুণক 0.7)। খেলায় ইস্পাত আর "
       "কংক্রিটের উপর এর প্রভাব নেই। কোনো লেভেল ভেজা হলে সেটা মাথায় রেখে কাঠের সদস্যের মাপ ঠিক করো, অথবা "
       "সবচেয়ে ভারী সদস্যগুলো ইস্পাতে বদলাও।"),
    qa("Why does a member cost more than its material and labour?",
       "The cost also includes five years of maintenance: real bridges must be painted, treated "
       "and repaired. Each material adds a share of its own "
       "material cost: timber 25% (it rots), steel 10% (it rusts), steel cable 8%, concrete 5%, "
       "smart alloy 3%, carbon fibre 2% and nanotube 1%. This is another reason timber is not "
       "free - and why cheap material is not always the cheapest bridge.",
       "একটি সদস্যের খরচ তার উপাদান আর শ্রমের চেয়ে বেশি কেন?",
       "খরচে পাঁচ বছরের রক্ষণাবেক্ষণও ধরা আছে: আসল সেতু রং করতে, রক্ষা করতে আর মেরামত করতে হয়। প্রতিটি উপাদান তার নিজের উপাদান-খরচের একটি ভাগ "
       "যোগ করে: কাঠ 25% (পচে যায়), ইস্পাত 10% (মরচে ধরে), ইস্পাতের তার 8%, কংক্রিট 5%, স্মার্ট সংকর ধাতু "
       "3%, কার্বন ফাইবার 2% আর ন্যানোটিউব 1%। এজন্যই কাঠ বিনামূল্যে নয় - আর সস্তা উপাদান সবসময় সবচেয়ে "
       "সস্তা সেতু নয়।"),
    qa("What is the carbon footprint on the results screen?",
       "The tonnes of CO2 released to make your materials: about 0.4 kg per kg of timber, 1.9 for "
       "steel, 0.15 for concrete, 2 for steel cable, 25 for carbon fibre, 40 for nanotube and 12 for "
       "smart alloy. It does not change your stars, but it shows the hidden cost of heavy, "
       "high-tech designs - a lean bridge is also a greener bridge.",
       "ফলাফলের পর্দায় কার্বন পদচিহ্ন কী?",
       "তোমার উপাদান তৈরিতে যত টন CO2 বেরোয়: প্রতি kg কাঠে প্রায় 0.4 kg, ইস্পাতে 1.9, কংক্রিটে 0.15, "
       "ইস্পাতের তারে 2, কার্বন ফাইবারে 25, ন্যানোটিউবে 40 আর স্মার্ট সংকর ধাতুতে 12। এটি তোমার তারা "
       "বদলায় না, কিন্তু ভারী আর উচ্চ-প্রযুক্তির নকশার লুকোনো খরচ দেখায় - হালকা সেতু পরিবেশের জন্যও ভালো।"),
    qa("I-beam and hollow box cost more to make. Are they worth it?",
       "In compression, almost always. An I-beam costs 15% more to fabricate and a hollow box 30% "
       "more, but they are 5.4 and 9.6 times stiffer against buckling than a solid square with the "
       "same material. To get the same P_cr from a solid square you would need about 2.3 to 3.1 "
       "times the area. In tension, shape does not help - use the cheaper solid square.",
       "আই-বিম আর ফাঁপা বাক্স বানাতে বেশি খরচ। তবু কি লাভ?",
       "চাপে প্রায় সবসময়ই। আই-বিম বানাতে 15% আর ফাঁপা বাক্সে 30% বেশি খরচ, কিন্তু একই উপাদানের নিরেট "
       "বর্গের চেয়ে এরা বাকলিংয়ে 5.4 আর 9.6 গুণ দৃঢ়। নিরেট বর্গ দিয়ে একই P_cr পেতে প্রায় 2.3 থেকে 3.1 গুণ "
       "ক্ষেত্রফল লাগত। টানে গড়ন কোনো সাহায্য করে না - সস্তা নিরেট বর্গ ব্যবহার করো।"),
    qa("Should every beam have the same size?",
       "No - that wastes money. After TEST, click each member with Select and slide its area: "
       "shrink the dark-green ones, grow the red ones. Typically the top chord and end diagonals "
       "need the most, while the middle diagonals and the hangers need little. A design where "
       "every member is yellow-green is close to the cheapest safe design.",
       "সব বিম কি একই মাপের হওয়া উচিত?",
       "না - তাতে টাকা নষ্ট। 'পরীক্ষা'-র পরে 'বাছাই' দিয়ে প্রতিটি সদস্যে ক্লিক করে তার ক্ষেত্রফল স্লাইড করো: "
       "গাঢ় সবুজগুলো ছোট করো, লালগুলো বড় করো। সাধারণত উপরের কর্ড আর প্রান্তের কর্ণে সবচেয়ে বেশি লাগে, আর "
       "মাঝের কর্ণ ও ঝোলানো তারে কম। যে নকশায় প্রতিটি সদস্য হলুদ-সবুজ, সেটি সবচেয়ে সস্তা নিরাপদ নকশার "
       "কাছাকাছি।"),
    # --- tools ------------------------------------------------------------------------
    qa("What do the force arrows (Vectors) show?",
       "Blue arrows are the support reactions pushing up on the bridge; red arrows are the loads "
       "(weights and vehicles); when you select a joint, the arrows of every member on it are "
       "drawn. Arrow length is proportional to kN. At every joint the arrows add up to zero - "
       "Sum Fx = 0 and Sum Fy = 0 - otherwise the joint would move.",
       "বলের তীর ('বল-তীর') কী দেখায়?",
       "নীল তীর হলো সাপোর্টের প্রতিক্রিয়া, যা সেতুকে উপরে ঠেলে; লাল তীর হলো ভার (ওজন আর গাড়ি); কোনো জোড় "
       "বাছাই করলে তার উপরের প্রতিটি সদস্যের তীর আঁকা হয়। তীরের দৈর্ঘ্য kN-এর সমানুপাতিক। প্রতিটি জোড়ে "
       "তীরগুলোর যোগফল শূন্য - Sum Fx = 0 আর Sum Fy = 0 - নইলে জোড়টি সরে যেত।"),
    qa("Why exaggerate the sag (x1, x10, x50)?",
       "Real deflections are millimetres - too small to see. Sag x10 or x50 multiplies them so you "
       "can see where the bridge bends most, which way each joint moves, and which part is "
       "too flexible. A floppy bridge is also a low-frequency bridge, which matters for wind "
       "in Levels 7 and 10.",
       "ঝোলা বাড়িয়ে দেখানো (x1, x10, x50) কেন?",
       "আসল বাঁক কয়েক মিলিমিটার - দেখার পক্ষে খুব ছোট। 'ঝোলা' x10 বা x50 সেটাকে গুণ করে, যাতে দেখতে পাও "
       "সেতু কোথায় সবচেয়ে বেশি বাঁকে, প্রতিটি জোড় কোন দিকে সরে, আর কোন অংশ বেশি নরম। নরম সেতু মানে কম "
       "কম্পাঙ্কের সেতুও, যা লেভেল 7 আর 10-এর বাতাসে গুরুত্বপূর্ণ।"),
    qa("How do I read the calculator for one beam?",
       "It shows, card by card: material, shape, length L, area A and stiffness E; the force N and "
       "whether it is TENSION or COMPRESSION; the stress sigma = N / A with the material limit; the "
       "strain; P_cr = pi^2 E I / (K L)^2 with your numbers; and the load ratio. The "
       "failing formula is the same one the Black Box will show if this beam breaks.",
       "একটি বিমের জন্য ক্যালকুলেটর কীভাবে পড়ব?",
       "কার্ডে কার্ডে দেখায়: উপাদান, গড়ন, দৈর্ঘ্য L, ক্ষেত্রফল A আর দৃঢ়তা E; বল N আর সেটি টান নাকি চাপ; "
       "উপাদানের সীমাসহ পীড়ন sigma = N / A; বিকৃতি; তোমার সংখ্যা বসানো P_cr = pi^2 E I / (K L)^2; আর ভার-অনুপাত। এই বিম ভাঙলে "
       "ব্ল্যাক বক্স ঠিক এই সূত্রটিই দেখাবে।"),
    qa("The vehicle will not start - what is wrong?",
       "Usually the road is not connected: the deck pieces must form one chain from the left bank "
       "joint to the right bank joint (the TEST panel says 'Road not connected yet'). Check that "
       "the deck ends exactly on the bank anchors and that no deck piece was drawn with the Beam "
       "tool by mistake - beams are not road.",
       "গাড়ি চলতে শুরু করছে না - সমস্যা কী?",
       "সাধারণত রাস্তা জোড়া হয়নি: ডেকের টুকরোগুলোকে বাঁ পাড়ের জোড় থেকে ডান পাড়ের জোড় পর্যন্ত একটি শিকল "
       "বানাতে হবে ('পরীক্ষা' প্যানেল বলে 'রাস্তা এখনো জোড়া হয়নি')। দেখো ডেক ঠিক পাড়ের নোঙরে শেষ হয়েছে কিনা, "
       "আর কোনো ডেক টুকরো ভুল করে 'বিম' টুলে আঁকা হয়নি তো - বিম রাস্তা নয়।"),
    qa("What is a good step-by-step way to optimise any bridge?",
       "1) Build a simple stable shape and get TEST to show no red. 2) Press RUN to make sure it "
       "really works. 3) Shrink dark-green members one by one and change shapes of pushed "
       "members to I-beam or box. 4) Remove members that carry nothing. 5) Stop when the FS is "
       "about 1.5-2 and the cost is under par. Every failure along the way gives salvage and EXP, "
       "so experimenting is cheap.",
       "যেকোনো সেতু ধাপে ধাপে উন্নত করার ভালো উপায় কী?",
       "1) একটি সহজ স্থির আকার বানাও, 'পরীক্ষা'-তে যেন কোনো লাল না থাকে। 2) সত্যিই কাজ করে কিনা দেখতে "
       "'চালাও' চাপো। 3) গাঢ় সবুজ সদস্যগুলো একে একে ছোট করো, আর ঠেলা সদস্যের গড়ন আই-বিম বা বাক্সে বদলাও। "
       "4) যে সদস্য কোনো ভার নেয় না তা সরাও। 5) FS প্রায় 1.5-2 আর খরচ প্যারের নিচে হলে থামো। পথে প্রতিটি "
       "ব্যর্থতা উদ্ধার-মূল্য আর EXP দেয়, তাই পরীক্ষা-নিরীক্ষা সস্তা।"),
)
