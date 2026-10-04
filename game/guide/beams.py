"""Help, Q51-100: bending, beams and the balanced cantilever (Level 3)."""
from . import qa

BEAMS = (
    # --- bending basics -----------------------------------------------------------------
    qa("What is a bending moment?",
       "A turning effect: force x distance (N*m). Sit at the end of a see-saw and your weight "
       "times your distance from the middle is the moment. In a beam, the moment at any point is "
       "the sum of every load times its distance from that point. The bigger the moment, the "
       "harder the beam is bent there.",
       "বাঁকানো ভ্রামক কী?",
       "একটি ঘোরানোর প্রভাব: বল x দূরত্ব (N*m)। ঢেঁকির এক প্রান্তে বসলে তোমার ওজন গুণ মাঝখান থেকে দূরত্ব হলো "
       "ভ্রামক। বিমের যেকোনো বিন্দুতে ভ্রামক হলো প্রতিটি ভার গুণ সেই বিন্দু থেকে তার দূরত্বের যোগফল। ভ্রামক "
       "যত বড়, বিম সেখানে তত জোরে বাঁকে।"),
    qa("What are sagging and hogging?",
       "Sagging: the beam bends like a smile - the bottom is pulled and the top is squeezed, as in "
       "the middle of a span. Hogging: it bends like a frown - the top is pulled and the bottom is "
       "squeezed, as over a pier or at the root of a cantilever. Concrete cracks where it is "
       "pulled, so it matters which side is in tension. The Level 3 calculator names which one "
       "is critical.",
       "স্যাগিং আর হগিং কী?",
       "স্যাগিং: বিম হাসির মতো বাঁকে - নিচের দিক টানে আর উপরের দিক চাপে থাকে, যেমন স্প্যানের মাঝখানে। হগিং: "
       "ভ্রূকুটির মতো বাঁকে - উপরের দিক টানে আর নিচের দিক চাপে থাকে, যেমন স্তম্ভের উপরে বা ক্যান্টিলিভারের "
       "গোড়ায়। কংক্রিট যেখানে টানা পড়ে সেখানে ফাটে, তাই কোন দিক টানে আছে তা গুরুত্বপূর্ণ। লেভেল 3-এর "
       "ক্যালকুলেটর বলে দেয় কোনটি সংকটজনক।"),
    qa("What does sigma = M y / I mean?",
       "It is the flexural (bending) stress. M is the bending moment, y the distance from the "
       "middle of the section (the neutral axis) to the point you check, and I the second moment "
       "of area. Stress is zero in the middle and largest at the top and bottom surfaces, where "
       "y = d / 2. A deeper section has a much bigger I, so the same moment gives less stress.",
       "sigma = M y / I মানে কী?",
       "এটি বাঁকানোর পীড়ন। M হলো বাঁকানো ভ্রামক, y হলো প্রস্থচ্ছেদের মাঝখান (নিরপেক্ষ অক্ষ) থেকে যে বিন্দু "
       "দেখছ তার দূরত্ব, আর I ক্ষেত্রফলের দ্বিতীয় ভ্রামক। মাঝখানে পীড়ন শূন্য, আর উপর ও নিচের তলে, যেখানে "
       "y = d / 2, সবচেয়ে বেশি। গভীর প্রস্থচ্ছেদের I অনেক বড়, তাই একই ভ্রামকে পীড়ন কম হয়।"),
    qa("Why does I = b d^3 / 12 make depth so important?",
       "For a rectangle of width b and depth d, I grows with the cube of the depth. Double the "
       "width and I doubles; double the depth and I becomes 8 times bigger. That is why beams are "
       "tall and thin, and why the Level 3 girder is deepest where the moment is largest.",
       "I = b d^3 / 12 গভীরতাকে এত গুরুত্বপূর্ণ করে কেন?",
       "প্রস্থ b আর গভীরতা d-এর আয়তক্ষেত্রে I বাড়ে গভীরতার ঘনফল অনুপাতে। প্রস্থ দ্বিগুণ করলে I দ্বিগুণ; "
       "গভীরতা দ্বিগুণ করলে I 8 গুণ। এজন্যই বিম উঁচু আর সরু হয়, আর লেভেল 3-এর গার্ডার সেখানেই সবচেয়ে গভীর "
       "যেখানে ভ্রামক সবচেয়ে বড়।"),
    qa("Why does doubling the depth cut the material per unit of strength?",
       "Bending strength depends on the section modulus S = I / y = b d^2 / 6. Doubling the depth "
       "makes S 4 times bigger while the area (and weight and cost) only doubles. So per kilogram "
       "of material a deep section carries about twice the moment of a shallow one. The limit is "
       "that very deep, thin sections need enough web to carry shear.",
       "গভীরতা দ্বিগুণ করলে শক্তির প্রতি একক উপাদান কমে কেন?",
       "বাঁকানোর শক্তি নির্ভর করে সেকশন মডুলাস S = I / y = b d^2 / 6-এর উপর। গভীরতা দ্বিগুণ করলে S 4 গুণ "
       "হয়, অথচ ক্ষেত্রফল (আর ওজন ও খরচ) শুধু দ্বিগুণ। তাই প্রতি কিলোগ্রাম উপাদানে গভীর প্রস্থচ্ছেদ অগভীরের "
       "প্রায় দ্বিগুণ ভ্রামক বয়। সীমা হলো, খুব গভীর আর সরু প্রস্থচ্ছেদে কর্তন বইতে যথেষ্ট ওয়েব লাগে।"),
    qa("What is the neutral axis?",
       "The line through a bent section where the material is neither stretched nor squeezed. "
       "Above it (in sagging) the material is squeezed, below it stretched, and the stress grows "
       "with the distance from it. Material close to the neutral axis does almost no work in "
       "bending - which is why hollow and I-shaped sections save so much material.",
       "নিরপেক্ষ অক্ষ কী?",
       "বাঁকা প্রস্থচ্ছেদের ভেতর দিয়ে যাওয়া সেই রেখা, যেখানে উপাদান টানাও হয় না, চাপাও হয় না। (স্যাগিংয়ে) এর "
       "উপরে উপাদান চাপে, নিচে টানে, আর এর থেকে দূরত্বের সঙ্গে পীড়ন বাড়ে। নিরপেক্ষ অক্ষের কাছের উপাদান "
       "বাঁকানোয় প্রায় কোনো কাজ করে না - এজন্যই ফাঁপা আর I-আকৃতির প্রস্থচ্ছেদ এত উপাদান বাঁচায়।"),
    qa("Why do I-beams have wide flanges and a thin web?",
       "Bending stress sigma = M y / I is biggest at the outer fibres, so putting material far "
       "from the neutral axis - in the flanges - gives the largest I for the least mass. The web "
       "in the middle mainly carries the shear force V and keeps the flanges apart, so it can be "
       "thin. In this game an I-beam has I = 0.45 A^2 against 0.083 A^2 for a solid square.",
       "আই-বিমে চওড়া ফ্ল্যাঞ্জ আর পাতলা ওয়েব কেন?",
       "বাঁকানোর পীড়ন sigma = M y / I বাইরের তন্তুতে সবচেয়ে বেশি, তাই নিরপেক্ষ অক্ষ থেকে দূরে - ফ্ল্যাঞ্জে - "
       "উপাদান রাখলে সবচেয়ে কম ভরে সবচেয়ে বড় I পাওয়া যায়। মাঝের ওয়েব মূলত কর্তন-বল V বয় আর ফ্ল্যাঞ্জ দুটিকে "
       "দূরে রাখে, তাই পাতলা হতে পারে। এই খেলায় আই-বিমের I = 0.45 A^2, যেখানে নিরেট বর্গের 0.083 A^2।"),
    qa("What is shear stress tau = V Q / (I t)?",
       "Shear is the sliding effect between neighbouring slices of a beam. V is the shear force, Q "
       "the first moment of the area above the point, I the second moment of area and t the width "
       "there. It is largest at the neutral axis and largest near the supports, where V is big. "
       "The Level 3 girder may carry at most 2.5 MPa of shear.",
       "কর্তন পীড়ন tau = V Q / (I t) কী?",
       "কর্তন হলো বিমের পাশাপাশি দুই স্তরের মধ্যে পিছলে যাওয়ার প্রভাব। V কর্তন-বল, Q বিন্দুর উপরের "
       "ক্ষেত্রফলের প্রথম ভ্রামক, I দ্বিতীয় ভ্রামক আর t সেখানকার প্রস্থ। এটি নিরপেক্ষ অক্ষে আর সাপোর্টের কাছে, "
       "যেখানে V বড়, সবচেয়ে বেশি। লেভেল 3-এর গার্ডার সর্বোচ্চ 2.5 MPa কর্তন বইতে পারে।"),
    qa("How are shear force and bending moment related?",
       "The bending moment changes along a beam at a rate equal to the shear force: where V is "
       "large the moment climbs quickly, and where V passes through zero the moment is at a peak. "
       "So shear is biggest next to the supports and the moment is biggest at mid-span or over a "
       "pier - which is why a deep haunch at the pier helps against both.",
       "কর্তন-বল আর বাঁকানো ভ্রামকের সম্পর্ক কী?",
       "বিম বরাবর বাঁকানো ভ্রামক কর্তন-বলের সমান হারে বদলায়: যেখানে V বড় সেখানে ভ্রামক দ্রুত বাড়ে, আর যেখানে "
       "V শূন্য পেরোয় সেখানে ভ্রামক চূড়ায়। তাই কর্তন সাপোর্টের পাশে সবচেয়ে বেশি আর ভ্রামক স্প্যানের মাঝে বা "
       "স্তম্ভের উপরে সবচেয়ে বেশি - এজন্যই স্তম্ভে গভীর হঞ্চ দুটির বিরুদ্ধেই সাহায্য করে।"),
    qa("What moments do the standard simple cases give?",
       "Simply supported beam of span L: a point load P in the middle gives M = P L / 4; a uniform "
       "load w per metre gives M = w L^2 / 8 at mid-span. Cantilever of length L: a point load at "
       "the tip gives M = P L at the root; a uniform load gives M = w L^2 / 2. These four formulas "
       "let you estimate almost any member before you build it.",
       "সাধারণ সহজ ক্ষেত্রগুলোতে ভ্রামক কত হয়?",
       "L স্প্যানের সরলভাবে বসানো বিম: মাঝখানে বিন্দু-ভার P দিলে M = P L / 4; প্রতি মিটারে সমান ভার w দিলে "
       "মাঝখানে M = w L^2 / 8। L দৈর্ঘ্যের ক্যান্টিলিভার: ডগায় বিন্দু-ভার দিলে গোড়ায় M = P L; সমান ভারে "
       "M = w L^2 / 2। এই চারটি সূত্রে প্রায় যেকোনো সদস্যের মান বানানোর আগেই আন্দাজ করা যায়।"),
    qa("Can I estimate the chord force of my Level 1 truss by hand?",
       "Yes - treat the whole truss as one beam. The 3.5 t van (about 34 kN) in the middle of the "
       "16 m span gives M = 34 x 16 / 4 = 137 kN*m; the road surface (1.5 kN/m) adds "
       "1.5 x 16^2 / 8 = 48 kN*m. Total about 185 kN*m. With a 3 m deep truss each chord carries "
       "about 185 / 3 = 62 kN, plus a little for the truss's own weight. Compare that with what "
       "your chord members can carry.",
       "লেভেল 1-এর ট্রাসের কর্ড-বল কি হাতে আন্দাজ করা যায়?",
       "হ্যাঁ - পুরো ট্রাসকে একটি বিম ধরো। 16 m স্প্যানের মাঝে 3.5 t ভ্যান (প্রায় 34 kN) দেয় M = 34 x 16 / 4 = "
       "137 kN*m; রাস্তার আস্তরণ (1.5 kN/m) যোগ করে 1.5 x 16^2 / 8 = 48 kN*m। মোট প্রায় 185 kN*m। 3 m গভীর "
       "ট্রাসে প্রতিটি কর্ড প্রায় 185 / 3 = 62 kN বয়, সঙ্গে ট্রাসের নিজের ওজনের জন্য একটু বেশি। তোমার কর্ড "
       "সদস্য কতটা বইতে পারে তার সঙ্গে তুলনা করো।"),
    qa("How much does a beam bend (deflect)?",
       "For a simply supported beam with a central load, deflection = P L^3 / (48 E I). It grows "
       "with the cube of the span: double the span and the beam bends 8 times more. Stiffness EI "
       "fights it - a stiffer material (bigger E) or a deeper section (bigger I) both help. "
       "Bridges are usually limited by deflection and vibration as much as by strength.",
       "একটি বিম কতটা বাঁকে (বিচ্যুত হয়)?",
       "মাঝখানে ভারসহ সরলভাবে বসানো বিমে বিচ্যুতি = P L^3 / (48 E I)। এটি স্প্যানের ঘনফল অনুপাতে বাড়ে: স্প্যান "
       "দ্বিগুণ করলে বিম 8 গুণ বেশি বাঁকে। দৃঢ়তা EI এর বিরুদ্ধে লড়ে - বেশি দৃঢ় উপাদান (বড় E) বা গভীর প্রস্থচ্ছেদ "
       "(বড় I) দুটোই সাহায্য করে। সেতু সাধারণত শক্তির মতোই বিচ্যুতি আর কম্পন দিয়েও সীমিত হয়।"),
    qa("What is a continuous beam and why is it better?",
       "A beam that runs over three or more supports without a break. Over each inner support it "
       "hogs, which pulls the moment at mid-span down. Compared with separate simple spans, the "
       "biggest moment is smaller and the beam is stiffer. In Level 3, stitching the middle turns "
       "the two T-shaped cantilevers into one continuous beam over four supports.",
       "অবিচ্ছিন্ন বিম কী, আর এটি ভালো কেন?",
       "যে বিম কোনো বিরতি ছাড়া তিন বা তার বেশি সাপোর্টের উপর দিয়ে চলে। প্রতিটি ভেতরের সাপোর্টের উপরে সে হগ "
       "করে, যা স্প্যানের মাঝের ভ্রামক নামিয়ে আনে। আলাদা আলাদা সরল স্প্যানের তুলনায় সবচেয়ে বড় ভ্রামক ছোট হয় "
       "আর বিম বেশি দৃঢ় হয়। লেভেল 3-এ মাঝখান জোড়া দিলে T-আকৃতির দুটি ক্যান্টিলিভার চারটি সাপোর্টের উপর একটি "
       "অবিচ্ছিন্ন বিম হয়ে যায়।"),
    # --- Level 3: the balanced cantilever --------------------------------------------------
    qa("What is a balanced-cantilever bridge?",
       "A bridge built outwards from tall piers without any scaffolding from the ground: concrete "
       "segments are cast one at a time on both sides of each pier, like a see-saw growing both "
       "ways. When the arms meet in the middle they are stitched together. It is used for deep "
       "valleys and rivers where nothing can stand underneath during construction.",
       "ব্যালান্সড-ক্যান্টিলিভার সেতু কী?",
       "নিচের মাটি থেকে কোনো ভারা ছাড়াই উঁচু স্তম্ভ থেকে বাইরের দিকে বানানো সেতু: প্রতিটি স্তম্ভের দুই পাশে "
       "একটি একটি করে কংক্রিটের অংশ ঢালা হয়, যেন একটি ঢেঁকি দুই দিকে বাড়ছে। বাহুগুলো মাঝখানে মিললে জোড়া দেওয়া "
       "হয়। গভীর উপত্যকা আর নদীতে এটি ব্যবহার হয়, যেখানে নির্মাণের সময় নিচে কিছু দাঁড় করানো যায় না।"),
    qa("What is the layout of Level 3?",
       "The girder runs 66 m from abutment to abutment (x = 0 to 66). Pier A stands at 18 m and "
       "pier B at 48 m. Every segment is 3 m long. Each pier has an outer arm of 6 segments (18 m, "
       "landing on the abutment) and an inner arm of 5 segments (15 m, meeting the other pier's "
       "arm at mid-span, x = 33 m). That is 22 segments in total.",
       "লেভেল 3-এর বিন্যাস কেমন?",
       "গার্ডারটি এক অ্যাবাটমেন্ট থেকে অন্যটি পর্যন্ত 66 m (x = 0 থেকে 66)। স্তম্ভ A 18 m-এ আর স্তম্ভ B 48 m-এ "
       "দাঁড়িয়ে। প্রতিটি অংশ 3 m লম্বা। প্রতিটি স্তম্ভের একটি বাইরের বাহু 6 অংশের (18 m, অ্যাবাটমেন্টে গিয়ে "
       "নামে) আর একটি ভেতরের বাহু 5 অংশের (15 m, স্প্যানের মাঝে x = 33 m-এ অন্য স্তম্ভের বাহুর সঙ্গে মেলে)। "
       "মোট 22টি অংশ।"),
    qa("What does the see-saw meter measure?",
       "The unbalanced moment on the pier: the sum of weight x distance on the right minus the "
       "same on the left. The foundation can resist 7 MN*m without help, plus 6 MN*m for each "
       "tie-down. If the unbalance passes that, the pier tips over and the Black Box reports 'The "
       "pier tipped: the see-saw was out of balance'.",
       "ঢেঁকি-মিটার কী মাপে?",
       "স্তম্ভের উপর অসাম্য ভ্রামক: ডানের ওজন x দূরত্বের যোগফল বিয়োগ বাঁয়ের একই যোগফল। ভিত্তি কোনো সাহায্য "
       "ছাড়া 7 MN*m সইতে পারে, আর প্রতিটি বাঁধন-তারে আরও 6 MN*m। অসাম্য এর বেশি হলে স্তম্ভ উল্টে যায় আর "
       "ব্ল্যাক বক্স জানায় 'স্তম্ভ উল্টে গেছে: ঢেঁকির ভারসাম্য ছিল না'।"),
    qa("What is the form traveller, and why does it matter so much?",
       "The traveller is the 400 kN steel frame that holds the formwork at the tip of the arm "
       "being built. It stands at the very end of the arm, so its moment is 400 kN x tip distance "
       "- at 18 m that is 7.2 MN*m, more than the bare foundation allows by itself. It moves off "
       "once an arm is complete.",
       "ফর্ম ট্রাভেলার কী, আর এটি এত গুরুত্বপূর্ণ কেন?",
       "ট্রাভেলার হলো 400 kN-এর একটি ইস্পাতের কাঠামো, যা তৈরি হতে থাকা বাহুর ডগায় ছাঁচ ধরে রাখে। এটি বাহুর "
       "একেবারে শেষে থাকে, তাই এর ভ্রামক 400 kN x ডগার দূরত্ব - 18 m-এ তা 7.2 MN*m, যা খালি ভিত্তি একা যতটা "
       "সইতে পারে তার চেয়ে বেশি। বাহু শেষ হলে এটি সরে যায়।"),
    qa("How heavy is each concrete segment?",
       "Weight per metre = 2400 kg/m^3 x 9.81 x b x d, with web width b = 1.2 m and depth d. At "
       "d = 3.5 m that is about 99 kN per metre; at d = 2.5 m about 71 kN per metre. A 3 m segment "
       "next to the pier is the heaviest because the girder is deepest there; segments get lighter "
       "towards the tip.",
       "প্রতিটি কংক্রিটের অংশ কতটা ভারী?",
       "প্রতি মিটারে ওজন = 2400 kg/m^3 x 9.81 x b x d, যেখানে ওয়েবের প্রস্থ b = 1.2 m আর গভীরতা d। d = 3.5 m-এ "
       "তা প্রতি মিটারে প্রায় 99 kN; d = 2.5 m-এ প্রায় 71 kN। স্তম্ভের পাশের 3 m অংশটি সবচেয়ে ভারী, কারণ সেখানে "
       "গার্ডার সবচেয়ে গভীর; ডগার দিকে অংশগুলো হালকা হয়।"),
    qa("Why must I alternate left and right when casting?",
       "Each segment adds its weight x its distance to one side of the see-saw. Only two or three "
       "segments on one side are enough to reach the 7 MN*m limit. Casting left, then right, then "
       "left keeps the unbalance to about one segment at a time. The demo casts both piers this "
       "way, segment by segment.",
       "ঢালাইয়ের সময় বাঁ-ডান পালা করতে হবে কেন?",
       "প্রতিটি অংশ ঢেঁকির এক দিকে তার ওজন x দূরত্ব যোগ করে। এক দিকে মাত্র দুই বা তিনটি অংশেই 7 MN*m সীমায় "
       "পৌঁছানো যায়। বাঁয়ে, তারপর ডানে, তারপর বাঁয়ে ঢাললে অসাম্য একবারে প্রায় একটি অংশের সমান থাকে। প্রদর্শনী "
       "দুটি স্তম্ভই এভাবে অংশে অংশে ঢালে।"),
    qa("Why is the last outer segment the most dangerous cast?",
       "Each outer arm has 6 segments but each inner arm only 5, so the sixth outer segment has "
       "nothing on the other side to balance it - and the traveller is then 18 m out. With the "
       "starting depths the unbalance reaches about 10-11 MN*m, far above 7 MN*m. Add a tie-down on "
       "that pier before this cast (capacity 13 MN*m). Once that arm lands on the abutment, the "
       "pier is propped and cannot tip any more.",
       "শেষ বাইরের অংশটি ঢালা সবচেয়ে বিপজ্জনক কেন?",
       "প্রতিটি বাইরের বাহুতে 6টি অংশ কিন্তু প্রতিটি ভেতরের বাহুতে মাত্র 5টি, তাই ষষ্ঠ বাইরের অংশের অন্য পাশে "
       "ভারসাম্য রাখার কিছু নেই - আর ট্রাভেলার তখন 18 m দূরে। শুরুর গভীরতায় অসাম্য প্রায় 10-11 MN*m-এ পৌঁছায়, "
       "যা 7 MN*m-এর অনেক উপরে। এই ঢালাইয়ের আগে ওই স্তম্ভে একটি বাঁধন-তার দাও (ক্ষমতা 13 MN*m)। ওই বাহু "
       "অ্যাবাটমেন্টে নামলে স্তম্ভ ঠেকনা পায় আর আর উল্টাতে পারে না।"),
    qa("What do the tie-downs do and what do they cost?",
       "A tie-down is a set of temporary anchor cables at the pier. Each one adds 6 MN*m of "
       "resistance against tipping and costs Rs 5 L. Press 'Tie-down A' or 'Tie-down B' before a "
       "risky cast. One per pier is usually enough when you alternate sides; more only costs "
       "money.",
       "বাঁধন-তার কী করে আর এর দাম কত?",
       "বাঁধন-তার হলো স্তম্ভে অস্থায়ী নোঙর-তারের একটি সেট। প্রতিটি উল্টানোর বিরুদ্ধে 6 MN*m প্রতিরোধ যোগ করে "
       "আর দাম Rs 5 L। ঝুঁকির ঢালাইয়ের আগে 'বাঁধন-তার A' বা 'বাঁধন-তার B' চাপো। পালা করে ঢাললে প্রতি স্তম্ভে "
       "একটিই সাধারণত যথেষ্ট; বেশি দিলে শুধু টাকা খরচ।"),
    qa("What is a 'root crack'?",
       "While the arms grow, each pier's root (the top of the girder right above the pier) hogs: "
       "its top is pulled. The built-in tendons allow up to 8 MPa there. The calculator checks "
       "sigma = M y / I with y = d_pier / 2 and I = b d_pier^3 / 12. If the haunch is too slim the "
       "Black Box reports 'The girder cracked at the pier: bending stress too high'.",
       "'গোড়ায় ফাটল' কী?",
       "বাহু বাড়ার সময় প্রতিটি স্তম্ভের গোড়া (স্তম্ভের ঠিক উপরে গার্ডারের উপরিভাগ) হগ করে: এর উপরের দিক "
       "টানা পড়ে। ভেতরে বসানো টেন্ডন সেখানে 8 MPa পর্যন্ত সইতে দেয়। ক্যালকুলেটর sigma = M y / I যাচাই করে, "
       "যেখানে y = d_pier / 2 আর I = b d_pier^3 / 12। হঞ্চ খুব সরু হলে ব্ল্যাক বক্স জানায় 'স্তম্ভের কাছে গার্ডার "
       "ফেটে গেছে: বাঁকানোর পীড়ন খুব বেশি'।"),
    qa("How do I choose the haunch depth at the piers (d_pier)?",
       "The slider goes from 2.5 to 6.5 m and the level starts at 3.5 m. Deeper means a much "
       "bigger I (d^3) so lower root stress - but also heavier segments, more concrete and more "
       "cost. Too slim fails: with 2.5 m the root reaches about 9 MPa and cracks. 3.5 m works with "
       "the starting tip depth; 5 m is very safe but costs about Rs 8 L more.",
       "স্তম্ভের কাছে হঞ্চের গভীরতা (d_pier) কীভাবে বাছব?",
       "স্লাইডার 2.5 থেকে 6.5 m, আর লেভেল শুরু হয় 3.5 m-এ। বেশি গভীর মানে অনেক বড় I (d^3), তাই গোড়ায় কম "
       "পীড়ন - কিন্তু ভারী অংশ, বেশি কংক্রিট আর বেশি খরচও। খুব সরু হলে ব্যর্থ: 2.5 m-এ গোড়া প্রায় 9 MPa-এ পৌঁছে "
       "ফেটে যায়। শুরুর ডগার গভীরতার সঙ্গে 3.5 m কাজ করে; 5 m খুব নিরাপদ, কিন্তু প্রায় Rs 8 L বেশি খরচ।"),
    qa("And the depth at the tips and mid-span (d_tip)?",
       "d_tip (1.5 to 3.5 m, starting at 2.5 m) is the depth at the ends of the arms, which become "
       "mid-span after stitching. A thinner tip makes the arms lighter, but mid-span then has a "
       "smaller I when the truck drives over it. With d_pier 3.5 m, light post-tensioning and "
       "d_tip 2.0 m the girder still passes, but only with FS about 1.3 - no third star.",
       "আর ডগা ও স্প্যানের মাঝের গভীরতা (d_tip)?",
       "d_tip (1.5 থেকে 3.5 m, শুরু 2.5 m) হলো বাহুগুলোর প্রান্তে গভীরতা, যা জোড়া দেওয়ার পর স্প্যানের মাঝ হয়ে "
       "যায়। সরু ডগায় বাহু হালকা হয়, কিন্তু ট্রাক যখন উপর দিয়ে যায় তখন মাঝখানের I ছোট থাকে। d_pier 3.5 m, "
       "হালকা পোস্ট-টেনশনিং আর d_tip 2.0 m হলে গার্ডার তবুও পাস করে, তবে FS মাত্র প্রায় 1.3 - তৃতীয় তারা নেই।"),
    qa("What shape is the haunch?",
       "The depth follows a parabola: d_pier right at the pier, falling smoothly to d_tip at the "
       "end of the longest arm (18 m away). Most of the extra depth stays close to the pier, where "
       "the moment is largest, and little is wasted further out. This is how real balanced "
       "cantilevers are shaped.",
       "হঞ্চের আকার কেমন?",
       "গভীরতা একটি অধিবৃত্ত মেনে চলে: স্তম্ভে ঠিক d_pier, তারপর মসৃণভাবে কমে সবচেয়ে লম্বা বাহুর প্রান্তে (18 m "
       "দূরে) d_tip। বাড়তি গভীরতার বেশিরভাগ স্তম্ভের কাছে থাকে, যেখানে ভ্রামক সবচেয়ে বড়, আর দূরে সামান্যই নষ্ট "
       "হয়। আসল ব্যালান্সড ক্যান্টিলিভারের আকার এভাবেই হয়।"),
    qa("How stiff is the starting Level 3 girder?",
       "With web width b = 1.2 m: at the pier d = 3.5 m gives I = 1.2 x 3.5^3 / 12 = 4.29 m^4; at the "
       "tip d = 2.5 m gives I = 1.2 x 2.5^3 / 12 = 1.56 m^4. So the section over the pier is about "
       "2.7 times stiffer than the tip, although it is only 1.4 times deeper - the d^3 rule at work.",
       "শুরুর লেভেল 3-এর গার্ডার কতটা দৃঢ়?",
       "ওয়েবের প্রস্থ b = 1.2 m ধরে: স্তম্ভে d = 3.5 m দেয় I = 1.2 x 3.5^3 / 12 = 4.29 m^4; ডগায় d = 2.5 m দেয় "
       "I = 1.2 x 2.5^3 / 12 = 1.56 m^4। তাই স্তম্ভের উপরের প্রস্থচ্ছেদ ডগার চেয়ে প্রায় 2.7 গুণ দৃঢ়, যদিও মাত্র "
       "1.4 গুণ গভীর - d^3 নিয়মের ফল।"),
    qa("Why should the girder be deepest at the pier?",
       "A cantilever's moment grows towards its root (for a uniform load M = w L^2 / 2), so the "
       "pier root carries the biggest moment and the biggest shear. Depth there gives I and "
       "section modulus exactly where they are needed. At the tips the moment is almost zero, so "
       "depth there would only add dead weight - which itself adds moment at the root.",
       "গার্ডার স্তম্ভের কাছে সবচেয়ে গভীর হওয়া উচিত কেন?",
       "ক্যান্টিলিভারের ভ্রামক তার গোড়ার দিকে বাড়ে (সমান ভারে M = w L^2 / 2), তাই স্তম্ভের গোড়া সবচেয়ে বড় "
       "ভ্রামক আর সবচেয়ে বড় কর্তন বয়। সেখানে গভীরতা ঠিক যেখানে দরকার সেখানে I আর সেকশন মডুলাস দেয়। ডগায় "
       "ভ্রামক প্রায় শূন্য, তাই সেখানে গভীরতা শুধু মৃত ওজন বাড়াত - যা নিজেই গোড়ায় ভ্রামক বাড়ায়।"),
    qa("Can I change the depths after I start casting?",
       "No. The haunch depths can only be set before the first segment is cast, because they fix "
       "the shape of the formwork. Undo all your segments if you want to change them. Plan the "
       "depths first with the calculator, then cast.",
       "ঢালাই শুরুর পর কি গভীরতা বদলাতে পারি?",
       "না। হঞ্চের গভীরতা শুধু প্রথম অংশ ঢালার আগেই ঠিক করা যায়, কারণ এটি ছাঁচের আকার ঠিক করে দেয়। বদলাতে "
       "চাইলে সব অংশ 'ফেরাও' করো। আগে ক্যালকুলেটর দিয়ে গভীরতা পরিকল্পনা করো, তারপর ঢালো।"),
    qa("What does 'STITCH & POST-TENSION' do?",
       "When all four arms are complete, it casts the closure in the middle (Rs 3 L) and stresses "
       "the tendons. The two T-shaped halves become one continuous beam over four supports, and "
       "the moments redistribute: the middle now sags under load instead of the arms hanging free. "
       "You must stitch before the truck test.",
       "'জোড়া দাও ও পোস্ট-টেনশন' কী করে?",
       "চারটি বাহু শেষ হলে এটি মাঝখানের জোড়ের অংশ ঢালে (Rs 3 L) আর টেন্ডনে টান দেয়। T-আকৃতির দুই অর্ধেক "
       "চারটি সাপোর্টের উপর একটি অবিচ্ছিন্ন বিম হয়ে যায়, আর ভ্রামক নতুন করে ভাগ হয়: বাহুগুলো মুক্তভাবে ঝোলার "
       "বদলে এখন ভার পড়লে মাঝখান স্যাগ করে। ট্রাক পরীক্ষার আগে জোড়া দিতেই হবে।"),
    qa("What is post-tensioning and which level should I choose?",
       "Steel tendons inside the girder are pulled tight after the concrete hardens, squeezing it. "
       "That pre-compression lets the concrete take more pull before it cracks: plain concrete 3 "
       "MPa, light post-tensioning +3 MPa (Rs 6 L), heavy +6 MPa (Rs 12 L). With the starting "
       "depths: none fails the truck test (FS about 0.8), light passes with FS about 1.6, heavy "
       "gives FS about 2.4 but pushes the cost over par.",
       "পোস্ট-টেনশনিং কী, আর কোন মাত্রা বাছব?",
       "কংক্রিট শক্ত হওয়ার পর গার্ডারের ভেতরের ইস্পাতের টেন্ডন টেনে টানটান করা হয়, যা কংক্রিটকে চেপে ধরে। এই "
       "আগাম চাপ কংক্রিটকে ফাটার আগে বেশি টান সইতে দেয়: সাধারণ কংক্রিট 3 MPa, হালকা পোস্ট-টেনশনিং +3 MPa "
       "(Rs 6 L), ভারী +6 MPa (Rs 12 L)। শুরুর গভীরতায়: কিছু না দিলে ট্রাক পরীক্ষায় ব্যর্থ (FS প্রায় 0.8), "
       "হালকায় FS প্রায় 1.6-এ পাস, ভারীতে FS প্রায় 2.4 কিন্তু খরচ প্যারের উপরে যায়।"),
    qa("What exactly does the truck test check?",
       "A 40 t truck - two axles of 196 kN, 4 m apart - drives across the stitched girder, which "
       "also carries 20 kN per metre of road surfacing. At every position the continuous-beam "
       "solver finds M and V along the girder and checks bending tension against the allowed "
       "value, compression against 20 MPa and shear against 2.5 MPa. The worst ratio gives the FS.",
       "ট্রাক পরীক্ষা ঠিক কী যাচাই করে?",
       "একটি 40 t ট্রাক - 4 m দূরে দূরে 196 kN-এর দুটি অ্যাক্সেল - জোড়া দেওয়া গার্ডারের উপর দিয়ে চলে, যা প্রতি "
       "মিটারে 20 kN রাস্তার আস্তরণও বয়। প্রতিটি অবস্থানে অবিচ্ছিন্ন-বিম সমাধানকারী গার্ডার বরাবর M আর V বের করে, "
       "আর বাঁকানোর টান অনুমোদিত মানের সঙ্গে, চাপ 20 MPa-এর সঙ্গে আর কর্তন 2.5 MPa-এর সঙ্গে মেলায়। সবচেয়ে খারাপ "
       "অনুপাত থেকে FS আসে।"),
    qa("The truck test failed. What do I change?",
       "The Black Box says 'The finished girder was over-stressed by the truck' and the calculator "
       "shows where: x, M, whether it is sagging (bottom pulled) or hogging (top pulled), and the "
       "stress. Options: more post-tensioning (raises the allowed tension), a deeper tip d_tip "
       "(more I at mid-span) or a deeper haunch (more I over the piers). Post-tensioning is "
       "usually the cheapest fix.",
       "ট্রাক পরীক্ষা ব্যর্থ হয়েছে। কী বদলাব?",
       "ব্ল্যাক বক্স বলে 'তৈরি গার্ডার ট্রাকের ভারে অতিরিক্ত পীড়িত হয়েছে' আর ক্যালকুলেটর দেখায় কোথায়: x, M, "
       "সেটি স্যাগিং (নিচ টানা) নাকি হগিং (উপর টানা), আর পীড়ন। উপায়: বেশি পোস্ট-টেনশনিং (অনুমোদিত টান বাড়ায়), "
       "গভীর ডগা d_tip (মাঝখানে বেশি I) বা গভীর হঞ্চ (স্তম্ভের উপরে বেশি I)। সাধারণত পোস্ট-টেনশনিংই সবচেয়ে "
       "সস্তা সমাধান।"),
    qa("Where along the girder does the truck cause the worst stress?",
       "Two places compete: mid-span between the piers (sagging, bottom pulled, worst when the "
       "truck is near the middle) and the girder over the piers (hogging, top pulled, worst when "
       "the truck is in a neighbouring span). The chart 'girder % vs truck x' plots the worst ratio "
       "for every truck position, so you can see which one governs.",
       "ট্রাক গার্ডারের কোথায় সবচেয়ে বেশি পীড়ন ঘটায়?",
       "দুটি জায়গা প্রতিযোগিতা করে: স্তম্ভ দুটির মাঝের স্প্যান (স্যাগিং, নিচ টানা, ট্রাক মাঝখানের কাছে থাকলে "
       "সবচেয়ে খারাপ) আর স্তম্ভের উপরের গার্ডার (হগিং, উপর টানা, ট্রাক পাশের স্প্যানে থাকলে সবচেয়ে খারাপ)। "
       "'গার্ডার % বনাম ট্রাকের অবস্থান x' চার্ট প্রতিটি অবস্থানের সবচেয়ে খারাপ অনুপাত আঁকে, তাই কোনটি নিয়ন্ত্রণ "
       "করছে দেখতে পাও।"),
    qa("What does Level 3 cost, item by item?",
       "Concrete Rs 8 per kg, so Rs 19,200 per cubic metre. Each segment also costs Rs 60,000 of "
       "labour to move the traveller and cast it - 22 segments make Rs 13.2 L. Tie-downs Rs 5 L "
       "each, the stitch Rs 3 L, post-tensioning Rs 6 L (light) or Rs 12 L (heavy). Budget "
       "Rs 95 L, par Rs 76 L.",
       "লেভেল 3-এর খরচ খাতে খাতে কত?",
       "কংক্রিট প্রতি kg Rs 8, অর্থাৎ প্রতি ঘনমিটার Rs 19,200। প্রতিটি অংশে ট্রাভেলার সরাতে আর ঢালতে আরও "
       "Rs 60,000 শ্রম - 22টি অংশে Rs 13.2 L। বাঁধন-তার প্রতিটি Rs 5 L, জোড়া Rs 3 L, পোস্ট-টেনশনিং Rs 6 L "
       "(হালকা) বা Rs 12 L (ভারী)। বাজেট Rs 95 L, প্যার Rs 76 L।"),
    qa("What is a proven three-star plan for Level 3?",
       "Keep the starting depths (d_pier 3.5 m, d_tip 2.5 m). Add one tie-down on each pier. Cast "
       "each pier's arms alternately, outer and inner. Stitch with light post-tensioning, then run "
       "the truck test. That costs about Rs 75.7 L (just under the Rs 76 L par) with FS about 1.6 - "
       "all three stars.",
       "লেভেল 3-এ তিন তারার একটি প্রমাণিত পরিকল্পনা কী?",
       "শুরুর গভীরতা রাখো (d_pier 3.5 m, d_tip 2.5 m)। প্রতিটি স্তম্ভে একটি করে বাঁধন-তার দাও। প্রতিটি স্তম্ভের "
       "বাহু পালা করে, বাইরে আর ভেতরে, ঢালো। হালকা পোস্ট-টেনশনিংসহ জোড়া দাও, তারপর ট্রাক পরীক্ষা চালাও। খরচ "
       "প্রায় Rs 75.7 L (Rs 76 L প্যারের ঠিক নিচে), FS প্রায় 1.6 - তিনটি তারাই।"),
    qa("Why not take heavy post-tensioning just to be safe?",
       "It costs Rs 6 L more than light. With the starting depths that lifts the total to about "
       "Rs 81.7 L - over the Rs 76 L par - so you lose the par star while FS rises to about 2.4, "
       "strength the truck never needs. Light post-tensioning already gives FS about 1.6, inside "
       "the 1.5-4 band.",
       "নিরাপদ থাকতে ভারী পোস্ট-টেনশনিং নিই না কেন?",
       "এটি হালকার চেয়ে Rs 6 L বেশি দামি। শুরুর গভীরতায় মোট খরচ প্রায় Rs 81.7 L হয় - Rs 76 L প্যারের উপরে - "
       "তাই প্যারের তারা হারাও, অথচ FS প্রায় 2.4-এ ওঠে, যে শক্তি ট্রাকের কখনো লাগে না। হালকা পোস্ট-টেনশনিংই "
       "FS প্রায় 1.6 দেয়, যা 1.5-4-এর মধ্যে।"),
    qa("Why is concrete used for this bridge and not steel?",
       "Concrete is very cheap (Rs 8 per kg against Rs 90 for steel) and strong when squeezed. Its "
       "weakness - almost no strength when pulled - is solved by tendons: built-in ones while the "
       "arms grow (8 MPa at the root) and post-tensioning after the stitch. Its large weight is "
       "the price, which is why balance and depth matter so much.",
       "এই সেতুতে ইস্পাত নয়, কংক্রিট কেন?",
       "কংক্রিট খুব সস্তা (প্রতি kg Rs 8, যেখানে ইস্পাত Rs 90) আর চাপে শক্ত। এর দুর্বলতা - টানলে প্রায় কোনো শক্তি "
       "নেই - টেন্ডন দিয়ে মেটানো হয়: বাহু বাড়ার সময় ভেতরে বসানো টেন্ডন (গোড়ায় 8 MPa) আর জোড়ার পরে "
       "পোস্ট-টেনশনিং। এর বড় ওজনই দাম, এজন্যই ভারসাম্য আর গভীরতা এত গুরুত্বপূর্ণ।"),
    qa("How does the moment diagram change when I stitch?",
       "Before stitching each pier carries a T-shaped cantilever: the whole girder hogs, with the "
       "largest moment at the pier roots and zero at the free tips. After stitching the girder is "
       "continuous: hogging remains over the piers, but sagging now appears at mid-span and near "
       "the abutments under the truck. The calculator chart shows the flip.",
       "জোড়া দিলে ভ্রামক-চিত্র কীভাবে বদলায়?",
       "জোড়ার আগে প্রতিটি স্তম্ভ একটি T-আকৃতির ক্যান্টিলিভার বয়: পুরো গার্ডার হগ করে, স্তম্ভের গোড়ায় সবচেয়ে বড় "
       "ভ্রামক আর মুক্ত ডগায় শূন্য। জোড়ার পরে গার্ডার অবিচ্ছিন্ন: স্তম্ভের উপরে হগিং থাকে, কিন্তু ট্রাকের ভারে "
       "এখন স্প্যানের মাঝে আর অ্যাবাটমেন্টের কাছে স্যাগিং দেখা দেয়। ক্যালকুলেটরের চার্ট এই উল্টে যাওয়া দেখায়।"),
    qa("What does Undo do in Level 3?",
       "Before stitching it removes the last segment you cast (one at a time, in reverse order). "
       "After stitching, before the truck test, it un-stitches the middle so you can change the "
       "post-tensioning. Removing segments is how you go back to change the haunch depths.",
       "লেভেল 3-এ 'ফেরাও' কী করে?",
       "জোড়ার আগে এটি শেষ ঢালা অংশটি সরায় (একবারে একটি, উল্টো ক্রমে)। জোড়ার পরে, ট্রাক পরীক্ষার আগে, এটি মাঝের "
       "জোড়া খুলে দেয় যাতে পোস্ট-টেনশনিং বদলাতে পারো। অংশ সরিয়েই হঞ্চের গভীরতা বদলাতে আগের অবস্থায় ফেরা যায়।"),
    qa("What happens when an outer arm reaches the abutment?",
       "It lands on the abutment and props the pier from that side. From then on the pier can no "
       "longer tip over, so later casts on the inner arm are only checked for root stress. That "
       "is why a smart order finishes the outer arm early - but its last segment still needs the "
       "tie-down while it is being cast.",
       "বাইরের বাহু অ্যাবাটমেন্টে পৌঁছালে কী হয়?",
       "এটি অ্যাবাটমেন্টে নামে আর সেই দিক থেকে স্তম্ভকে ঠেকনা দেয়। তারপর থেকে স্তম্ভ আর উল্টাতে পারে না, তাই ভেতরের "
       "বাহুর পরের ঢালাইগুলো শুধু গোড়ার পীড়নের জন্য যাচাই হয়। এজন্যই বুদ্ধিমান ক্রম বাইরের বাহু আগে শেষ করে - "
       "তবে তার শেষ অংশ ঢালার সময় তবুও বাঁধন-তার লাগে।"),
    qa("What is the Level 3 alternate route?",
       "If something fails you may choose 'Steel launch girder': the formwork travellers are "
       "re-used as a temporary steel launching truss to finish the span the slow way. It costs 0.7 "
       "x your failed build cost (at least 0.7 x half the par) and completes the level with one "
       "star and 30 EXP.",
       "লেভেল 3-এর বিকল্প পথ কী?",
       "কিছু ব্যর্থ হলে 'ইস্পাতের লঞ্চ গার্ডার' বাছতে পারো: ফর্ম ট্রাভেলারগুলো আবার অস্থায়ী ইস্পাতের লঞ্চিং ট্রাস "
       "হিসেবে ব্যবহার করে ধীরে ধীরে স্প্যান শেষ করা হয়। এর দাম তোমার ব্যর্থ নকশার খরচের 0.7 গুণ (অন্তত প্যারের "
       "অর্ধেকের 0.7 গুণ), আর এক তারা ও 30 EXP দিয়ে লেভেল শেষ হয়।"),
    # --- bending in the other levels ------------------------------------------------------
    qa("Do the deck pieces in the truss levels bend?",
       "No. In Levels 1, 7, 8 and 10 every member is pin-jointed, so it only carries a pull or a "
       "push along its length. A wheel standing between two joints is shared between them like a "
       "plank on two bricks. That is why short deck pieces and well-placed joints matter: the "
       "truss, not a single bending beam, carries the load.",
       "ট্রাসের লেভেলে ডেকের টুকরো কি বাঁকে?",
       "না। লেভেল 1, 7, 8 আর 10-এ প্রতিটি সদস্য পিন-জোড়া, তাই সে শুধু তার দৈর্ঘ্য বরাবর টান বা ঠেলা বয়। দুটি "
       "জোড়ের মাঝে দাঁড়ানো চাকা দুই ইটের উপর রাখা তক্তার মতো দুটির মধ্যে ভাগ হয়। এজন্যই ছোট ডেক টুকরো আর ঠিক "
       "জায়গায় জোড় গুরুত্বপূর্ণ: একটি বাঁকা বিম নয়, পুরো ট্রাসই ভার বয়।"),
    qa("How is buckling related to bending?",
       "Buckling is bending caused by compression. Once a pushed member bows a little, the push "
       "acts at an offset and creates a bending moment that bows it more. Its resistance comes "
       "from the same bending stiffness E I - which is why the shapes with a large I (I-beam, "
       "hollow box) are also the best struts.",
       "বাকলিং আর বাঁকানোর সম্পর্ক কী?",
       "বাকলিং হলো চাপের কারণে বাঁকানো। ঠেলা সদস্য একটু বাঁকলেই ঠেলা একটু সরে গিয়ে কাজ করে আর একটি বাঁকানো "
       "ভ্রামক তৈরি করে, যা তাকে আরও বাঁকায়। এর প্রতিরোধ আসে সেই একই বাঁকানোর দৃঢ়তা E I থেকে - এজন্যই বড় I-এর "
       "গড়ন (আই-বিম, ফাঁপা বাক্স) সবচেয়ে ভালো ঠেকনাও।"),
    qa("What is the effective-length factor K?",
       "It describes how the ends of a strut are held: P_cr = pi^2 E I / (K L)^2. Pinned at both ends "
       "K = 1 (that is what the game uses for every member); both ends fixed K = 0.5 (4 times "
       "stronger); one end fixed and one free K = 2 (4 times weaker). Bracing a strut at its "
       "middle has the same effect as halving L.",
       "কার্যকর-দৈর্ঘ্য গুণক K কী?",
       "এটি বলে ঠেকনার প্রান্তগুলো কীভাবে ধরা আছে: P_cr = pi^2 E I / (K L)^2। দুই প্রান্তে পিন হলে K = 1 (খেলায় "
       "প্রতিটি সদস্যে এটিই ব্যবহার হয়); দুই প্রান্ত স্থির হলে K = 0.5 (4 গুণ শক্ত); এক প্রান্ত স্থির আর অন্যটি "
       "মুক্ত হলে K = 2 (4 গুণ দুর্বল)। মাঝখানে ঠেকনাকে আটকে দেওয়া L অর্ধেক করার সমান কাজ করে।"),
    qa("Why do the towers in Levels 7 and 10 need special care?",
       "A tower holding cable stays is a long, heavily pushed member: the stays pull its top down "
       "on both sides. Long and pushed means buckling. Use a hollow box (largest I), make it "
       "shorter by adding joints with bracing, and keep the cable pulls on both sides balanced so "
       "the tower is pushed straight down rather than bent.",
       "লেভেল 7 আর 10-এর টাওয়ারে বিশেষ যত্ন লাগে কেন?",
       "তার ধরে রাখা টাওয়ার একটি লম্বা, জোরে ঠেলা খাওয়া সদস্য: তারগুলো দুই দিক থেকে এর মাথা নিচে টানে। লম্বা আর "
       "ঠেলা মানেই বাকলিং। ফাঁপা বাক্স (সবচেয়ে বড় I) ব্যবহার করো, ঠেকনাসহ জোড় যোগ করে একে ছোট করো, আর দুই দিকের "
       "তারের টান সমান রাখো, যাতে টাওয়ার বাঁকে না গিয়ে সোজা নিচে ঠেলা খায়।"),
    qa("Why are long cantilevers slim at the tips?",
       "Self-weight. A cantilever's own weight produces a root moment w L^2 / 2 that grows with the "
       "square of the length. Every extra kilogram near the tip is multiplied by the longest lever "
       "arm. Slim tips keep that dead-load moment down, so the root can be smaller and the whole "
       "structure lighter.",
       "লম্বা ক্যান্টিলিভারের ডগা সরু কেন?",
       "নিজের ওজনের জন্য। ক্যান্টিলিভারের নিজের ওজন গোড়ায় w L^2 / 2 ভ্রামক তৈরি করে, যা দৈর্ঘ্যের বর্গ অনুপাতে "
       "বাড়ে। ডগার কাছের প্রতিটি বাড়তি কিলোগ্রাম সবচেয়ে লম্বা লিভার-বাহু দিয়ে গুণ হয়। সরু ডগা সেই মৃত-ভারের "
       "ভ্রামক কম রাখে, তাই গোড়া ছোট হতে পারে আর পুরো কাঠামো হালকা হয়।"),
    qa("What does 'dead load' and 'live load' mean?",
       "Dead load is the structure's own weight and everything permanent on it - concrete, deck, "
       "road surfacing. Live load is what comes and goes - vans, buses, trucks, trains. Engineers "
       "check both together. In Level 3 the dead load during construction decides the balance, "
       "and the live load (the truck) decides the final check.",
       "'মৃত ভার' আর 'চলমান ভার' মানে কী?",
       "মৃত ভার হলো কাঠামোর নিজের ওজন আর তার উপরের সব স্থায়ী জিনিস - কংক্রিট, ডেক, রাস্তার আস্তরণ। চলমান ভার "
       "হলো যা আসে আর যায় - ভ্যান, বাস, ট্রাক, ট্রেন। প্রকৌশলীরা দুটি একসঙ্গে যাচাই করেন। লেভেল 3-এ নির্মাণের "
       "সময়ের মৃত ভার ভারসাম্য ঠিক করে, আর চলমান ভার (ট্রাক) শেষ পরীক্ষা ঠিক করে।"),
    qa("What are the three numbers to watch in Level 3?",
       "1) The see-saw balance of each pier against its capacity (7 MN*m, plus 6 per tie-down). "
       "2) The root stress against 8 MPa while casting. 3) After stitching, the girder ratio under "
       "the truck (FS = 1 / ratio, aim 1.5-4). The calculator shows all three, and the history chart "
       "plots each pier's balance as you cast.",
       "লেভেল 3-এ কোন তিনটি সংখ্যা খেয়াল রাখব?",
       "1) প্রতিটি স্তম্ভের ঢেঁকি-ভারসাম্য বনাম তার ক্ষমতা (7 MN*m, আর প্রতি বাঁধন-তারে 6)। 2) ঢালাইয়ের সময় গোড়ার "
       "পীড়ন বনাম 8 MPa। 3) জোড়ার পরে ট্রাকের ভারে গার্ডারের অনুপাত (FS = 1 / অনুপাত, লক্ষ্য 1.5-4)। ক্যালকুলেটর "
       "তিনটিই দেখায়, আর ইতিহাসের চার্ট ঢালাইয়ের সঙ্গে সঙ্গে প্রতিটি স্তম্ভের ভারসাম্য আঁকে।"),
    qa("Why does the game allow 8 MPa at the root while building but only 3 MPa later?",
       "During construction the girder contains cantilever tendons stressed as each segment is "
       "added; they pre-compress the top of the root, so it can take up to 8 MPa of hogging pull. "
       "The continuous girder after stitching relies on the concrete's own 3 MPa plus whatever "
       "post-tensioning you buy. Real bridges use exactly this two-stage tendon layout.",
       "নির্মাণের সময় গোড়ায় 8 MPa অনুমোদিত, কিন্তু পরে মাত্র 3 MPa কেন?",
       "নির্মাণের সময় গার্ডারে ক্যান্টিলিভার-টেন্ডন থাকে, প্রতিটি অংশ যোগের সঙ্গে সঙ্গে যাতে টান দেওয়া হয়; এরা গোড়ার "
       "উপরিভাগে আগাম চাপ দেয়, তাই সেখানে 8 MPa পর্যন্ত হগিংয়ের টান সইতে পারে। জোড়ার পরে অবিচ্ছিন্ন গার্ডার নির্ভর "
       "করে কংক্রিটের নিজের 3 MPa আর তুমি যতটা পোস্ট-টেনশনিং কেনো তার উপর। আসল সেতুও ঠিক এই দুই ধাপের টেন্ডন "
       "বিন্যাস ব্যবহার করে।"),
    qa("How do I get all three stars in Level 3 in one sentence?",
       "Starting depths, one tie-down per pier, alternate every cast, stitch with light "
       "post-tensioning: cost about Rs 75.7 L (par Rs 76 L) and FS about 1.6 (inside 1.5-4).",
       "এক বাক্যে লেভেল 3-এ তিনটি তারা কীভাবে পাব?",
       "শুরুর গভীরতা, প্রতি স্তম্ভে একটি বাঁধন-তার, প্রতিটি ঢালাই পালা করে, হালকা পোস্ট-টেনশনিংসহ জোড়া: খরচ প্রায় "
       "Rs 75.7 L (প্যার Rs 76 L) আর FS প্রায় 1.6 (1.5-4-এর মধ্যে)।"),
)
