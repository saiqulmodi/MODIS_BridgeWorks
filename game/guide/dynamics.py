"""Help, Q101-150: wind and resonance, earthquakes, rail grades and braking, maglev power."""
from . import qa

DYNAMICS = (
    # --- wind and resonance (Levels 7 and 10) ----------------------------------------------
    qa("What is a bridge's natural frequency f_n?",
       "Every structure has a speed at which it likes to swing, like a child's swing. For a "
       "spring-and-mass system f_n = (1 / 2 pi) sqrt(k / m): stiffness k makes it faster, mass m "
       "makes it slower. The game works out k and m from your actual truss (its sag shape and the "
       "weight of every joint) and shows f_n in the Wind lab.",
       "সেতুর স্বাভাবিক কম্পাঙ্ক f_n কী?",
       "প্রতিটি কাঠামোর একটি নিজস্ব দোলার গতি আছে, দোলনার মতো। স্প্রিং-আর-ভরের ব্যবস্থায় f_n = (1 / 2 pi) "
       "sqrt(k / m): দৃঢ়তা k একে দ্রুত করে, ভর m ধীর করে। খেলাটি তোমার আসল ট্রাস (তার ঝোলার আকার আর প্রতিটি "
       "জোড়ের ওজন) থেকে k আর m বের করে, আর বাতাসের ল্যাবে f_n দেখায়।"),
    qa("How do I raise the natural frequency?",
       "Make the bridge stiffer or lighter. Stiffer: a deeper truss, steel instead of timber "
       "(18 times higher E), more triangles, bigger chord areas. Lighter: remove unneeded members "
       "and avoid heavy materials. Because f_n depends on sqrt(k / m), doubling the stiffness "
       "raises f_n by only about 41% - deep trusses are the most effective way.",
       "স্বাভাবিক কম্পাঙ্ক কীভাবে বাড়াব?",
       "সেতুকে আরও দৃঢ় বা হালকা করো। দৃঢ়: গভীর ট্রাস, কাঠের বদলে ইস্পাত (18 গুণ বেশি E), বেশি ত্রিভুজ, বড় "
       "কর্ডের ক্ষেত্রফল। হালকা: অপ্রয়োজনীয় সদস্য সরাও আর ভারী উপাদান এড়াও। যেহেতু f_n নির্ভর করে sqrt(k / m)-এর "
       "উপর, দৃঢ়তা দ্বিগুণ করলে f_n মাত্র প্রায় 41% বাড়ে - গভীর ট্রাসই সবচেয়ে কার্যকর উপায়।"),
    qa("What is resonance and why is it so dangerous?",
       "If a force pushes a structure in time with its own natural swing, every push adds to the "
       "last one and the swing grows and grows - like pushing a swing at exactly the right moment. "
       "In 1940 the Tacoma Narrows Bridge tore itself apart in a wind of only 19 m/s this way. A "
       "small force at the wrong rhythm can break a bridge that a much bigger steady force cannot.",
       "অনুনাদ কী, আর এটি এত বিপজ্জনক কেন?",
       "কোনো বল যদি কাঠামোকে তার নিজের স্বাভাবিক দোলার তালে তালে ঠেলে, প্রতিটি ঠেলা আগেরটির সঙ্গে যোগ হয় আর দোলা "
       "বাড়তেই থাকে - যেমন ঠিক সময়ে দোলনা ঠেলা। 1940 সালে ট্যাকোমা ন্যারোস সেতু মাত্র 19 m/s বাতাসে এভাবেই "
       "নিজেকে ছিঁড়ে ফেলেছিল। ভুল তালে ছোট একটি বলও এমন সেতু ভাঙতে পারে, যা অনেক বড় স্থির বলেও ভাঙে না।"),
    qa("What is vortex shedding, f_v = St U / D?",
       "Wind flowing past the deck peels off swirls (vortices) alternately from the top and the "
       "bottom edge, giving the deck a rhythmic up-and-down push. Its frequency is f_v = St U / D: "
       "St is the Strouhal number (0.12 for a bridge deck), U the wind speed and D the deck depth "
       "(1.2 m in Level 7, 1.0 m in Level 10). As the wind grows, the rhythm gets faster.",
       "ঘূর্ণি ঝরা (vortex shedding), f_v = St U / D কী?",
       "ডেকের পাশ দিয়ে বয়ে যাওয়া বাতাস পালা করে উপরের আর নিচের কিনারা থেকে ঘূর্ণি ছাড়ে, যা ডেককে তালে তালে "
       "উপরে-নিচে ঠেলে। এর কম্পাঙ্ক f_v = St U / D: St হলো স্ট্রুহাল সংখ্যা (সেতুর ডেকের জন্য 0.12), U বাতাসের "
       "গতি আর D ডেকের গভীরতা (লেভেল 7-এ 1.2 m, লেভেল 10-এ 1.0 m)। বাতাস বাড়লে তাল দ্রুত হয়।"),
    qa("What is U_crit?",
       "The wind speed at which the vortex rhythm equals the bridge's natural frequency: "
       "U_crit = f_n D / St. In Level 7 that is f_n x 1.2 / 0.12 = 10 x f_n; in Level 10 it is "
       "f_n x 1.0 / 0.12 = 8.3 x f_n. A bridge with f_n = 2 Hz in Level 7 meets its critical wind "
       "at 20 m/s - well inside the afternoon gale. The Wind lab shows your U_crit before you run.",
       "U_crit কী?",
       "যে বাতাসের গতিতে ঘূর্ণির তাল সেতুর স্বাভাবিক কম্পাঙ্কের সমান হয়: U_crit = f_n D / St। লেভেল 7-এ তা "
       "f_n x 1.2 / 0.12 = 10 x f_n; লেভেল 10-এ f_n x 1.0 / 0.12 = 8.3 x f_n। লেভেল 7-এ f_n = 2 Hz-এর সেতু তার "
       "সংকট-বাতাস পায় 20 m/s-এ - বিকেলের ঝড়ের একেবারে মাঝে। চালানোর আগেই বাতাসের ল্যাব তোমার U_crit দেখায়।"),
    qa("Does the wind have to match f_n exactly?",
       "No. The vortices 'lock in' to the bridge whenever f_v is within 25% of f_n - that is, for "
       "wind speeds from about 0.75 to 1.25 x U_crit - and push with full strength there. Further "
       "away the push gets weaker but never below 15%. So in Level 7, to keep the whole 4-36 m/s "
       "gale out of the lock-in band, you need 0.75 x U_crit above 36 m/s: f_n above about 4.8 Hz.",
       "বাতাসকে কি ঠিক f_n-এর সমান হতে হবে?",
       "না। f_v যখনই f_n-এর 25%-এর মধ্যে থাকে, অর্থাৎ বাতাসের গতি প্রায় 0.75 থেকে 1.25 x U_crit হলে, ঘূর্ণি সেতুর "
       "সঙ্গে 'আটকে' যায় আর পুরো জোরে ঠেলে। এর বাইরে ঠেলা দুর্বল হয়, তবে কখনো 15%-এর নিচে নয়। তাই লেভেল 7-এ "
       "পুরো 4-36 m/s ঝড়কে আটকে যাওয়ার সীমার বাইরে রাখতে 0.75 x U_crit-কে 36 m/s-এর বেশি হতে হবে: f_n প্রায় "
       "4.8 Hz-এর বেশি।"),
    qa("Why is resonance at high wind worse than at low wind?",
       "The size of the vortex push is F = 1/2 rho U^2 D x span x C_L (C_L = 0.6). It grows with "
       "the square of the wind speed: at 30 m/s it is 9 times bigger than at 10 m/s. A floppy "
       "bridge that resonates in a gentle breeze is pushed softly; a medium bridge that resonates "
       "in the full gale is pushed hard, in rhythm, right when it hurts.",
       "কম বাতাসের চেয়ে জোরালো বাতাসে অনুনাদ বেশি খারাপ কেন?",
       "ঘূর্ণির ঠেলার মাপ F = 1/2 rho U^2 D x স্প্যান x C_L (C_L = 0.6)। এটি বাতাসের গতির বর্গ অনুপাতে বাড়ে: "
       "30 m/s-এ তা 10 m/s-এর চেয়ে 9 গুণ বড়। নরম সেতু মৃদু বাতাসে অনুনাদ করলে আলতো ঠেলা খায়; মাঝারি সেতু পুরো "
       "ঝড়ে অনুনাদ করলে জোরে, তালে তালে, ঠিক যখন সবচেয়ে ক্ষতি তখনই ঠেলা খায়।"),
    qa("What do aerodynamic fairings do?",
       "Streamlined edges on the deck break up the vortices: the lift coefficient C_L drops by 75% "
       "(from 0.6 to 0.15), so the rhythmic push is four times weaker at every wind speed. They "
       "cost Rs 2.5 L and do not change f_n. The Level 7 demo combines a deep steel truss with "
       "fairings.",
       "অ্যারোডাইনামিক ফেয়ারিং কী করে?",
       "ডেকের মসৃণ কিনারা ঘূর্ণি ভেঙে দেয়: উত্থান-গুণক C_L 75% কমে (0.6 থেকে 0.15), তাই প্রতিটি বাতাসের গতিতে "
       "তালের ঠেলা চার গুণ দুর্বল হয়। দাম Rs 2.5 L, আর এটি f_n বদলায় না। লেভেল 7-এর প্রদর্শনী একটি গভীর ইস্পাতের "
       "ট্রাসের সঙ্গে ফেয়ারিং মিলিয়ে ব্যবহার করে।"),
    qa("What do the cross-stay dampers do?",
       "They raise the structure's damping ratio from 0.5% (normal for steel bridges) to 2%. At "
       "resonance the swing size is roughly proportional to 1 / (2 x damping), so four times more "
       "damping makes the resonant swing about four times smaller. They cost Rs 2 L.",
       "ক্রস-স্টে ড্যাম্পার কী করে?",
       "এরা কাঠামোর অবমন্দন অনুপাত 0.5% (ইস্পাতের সেতুর জন্য স্বাভাবিক) থেকে 2%-এ তোলে। অনুনাদে দোলার মাপ মোটামুটি "
       "1 / (2 x অবমন্দন)-এর সমানুপাতিক, তাই চার গুণ বেশি অবমন্দনে অনুনাদের দোলা প্রায় চার গুণ ছোট হয়। দাম "
       "Rs 2 L।"),
    qa("What is a tuned mass damper (TMD)?",
       "A heavy mass hung under the deck on springs and dampers, tuned to the bridge's own "
       "frequency. When the bridge starts to swing, the mass swings the opposite way and soaks up "
       "the energy. Tall towers and long bridges really use them. In the game it costs Rs 3.5 L "
       "at a mass ratio of 0.02, and more for a heavier mass.",
       "টিউনড মাস ড্যাম্পার (TMD) কী?",
       "ডেকের নিচে স্প্রিং আর ড্যাম্পারে ঝোলানো একটি ভারী ভর, যা সেতুর নিজের কম্পাঙ্কে টিউন করা। সেতু দুলতে শুরু "
       "করলে ভরটি উল্টো দিকে দোলে আর শক্তি শুষে নেয়। উঁচু টাওয়ার আর লম্বা সেতুতে সত্যিই এটি ব্যবহার হয়। খেলায় "
       "0.02 ভর-অনুপাতে দাম Rs 3.5 L, আর ভারী ভরে বেশি।"),
    qa("How do I tune the TMD sliders?",
       "Use Den Hartog's rule for a mass ratio mu: tuning f_tmd / f_n = 1 / (1 + mu) and damping "
       "zeta = sqrt(3 mu / (8 (1 + mu)^3)). For mu = 0.02 that gives tuning 0.98 and zeta about "
       "0.08 - exactly the starting values. If you change mu, re-tune: mu = 0.04 needs about 0.96 "
       "and 0.12. A mistuned damper does little.",
       "TMD-এর স্লাইডারগুলো কীভাবে টিউন করব?",
       "ভর-অনুপাত mu-এর জন্য ডেন হার্টগের নিয়ম ব্যবহার করো: টিউনিং f_tmd / f_n = 1 / (1 + mu) আর অবমন্দন "
       "zeta = sqrt(3 mu / (8 (1 + mu)^3))। mu = 0.02-এ তা দেয় টিউনিং 0.98 আর zeta প্রায় 0.08 - ঠিক শুরুর মানগুলো। "
       "mu বদলালে আবার টিউন করো: mu = 0.04-এ লাগে প্রায় 0.96 আর 0.12। ভুল টিউনের ড্যাম্পার সামান্যই কাজ করে।"),
    qa("Is a heavier TMD better?",
       "A bigger mass ratio works over a wider band of frequencies and is more forgiving, but its "
       "cost grows in proportion (Rs 3.5 L x mu / 0.02, so mu = 0.04 costs Rs 7 L) and it adds "
       "weight to the deck. Usually the default 0.02, correctly tuned, is the best value.",
       "ভারী TMD কি ভালো?",
       "বড় ভর-অনুপাত কম্পাঙ্কের চওড়া পরিসরে কাজ করে আর ভুল কম সহ্য করে, কিন্তু দাম সমানুপাতে বাড়ে (Rs 3.5 L x "
       "mu / 0.02, তাই mu = 0.04-এর দাম Rs 7 L) আর ডেকে ওজন যোগ হয়। সাধারণত ঠিকমতো টিউন করা শুরুর 0.02-ই সবচেয়ে "
       "লাভজনক।"),
    qa("Which wind fix should I pick in Level 7?",
       "Cheapest first: dampers Rs 2 L, fairings Rs 2.5 L, TMD Rs 3.5 L. Fairings weaken the push "
       "at every wind speed; dampers and the TMD shrink the swing once it starts; stiffening the "
       "truss moves the resonance out of the gale altogether. Check the Wind lab card - f_n, "
       "U_crit and the live wind - and combine one fix with a reasonably stiff truss.",
       "লেভেল 7-এ কোন বাতাস-প্রতিকার বাছব?",
       "সবচেয়ে সস্তা আগে: ড্যাম্পার Rs 2 L, ফেয়ারিং Rs 2.5 L, TMD Rs 3.5 L। ফেয়ারিং প্রতিটি বাতাসের গতিতে ঠেলা "
       "দুর্বল করে; ড্যাম্পার আর TMD দোলা শুরু হলে তা ছোট করে; ট্রাস দৃঢ় করলে অনুনাদ পুরোপুরি ঝড়ের বাইরে সরে যায়। "
       "বাতাসের ল্যাবের কার্ড - f_n, U_crit আর চলতি বাতাস - দেখো, আর মোটামুটি দৃঢ় ট্রাসের সঙ্গে একটি প্রতিকার মেলাও।"),
    qa("How does the wind swing turn into forces in my beams?",
       "The game models the bridge's first swing mode: a sine-shaped bending along the span. The "
       "wind drives that mode, and at every instant its swing is turned into an equivalent set of "
       "loads on the deck joints, added to the buses' weight. The full truss solver then checks "
       "every member. If a member breaks while the swing load is large, the Black Box names "
       "resonance as the cause.",
       "বাতাসের দোলা আমার বিমে বল হয় কীভাবে?",
       "খেলাটি সেতুর প্রথম দোলার ধরন মডেল করে: স্প্যান বরাবর সাইন-আকৃতির বাঁক। বাতাস সেই ধরনটিকে চালায়, আর প্রতিটি "
       "মুহূর্তে তার দোলা ডেকের জোড়গুলোতে সমতুল্য ভারে বদলে বাসের ওজনের সঙ্গে যোগ হয়। তারপর পুরো ট্রাস সমাধানকারী "
       "প্রতিটি সদস্য যাচাই করে। দোলার ভার বড় থাকার সময় কোনো সদস্য ভাঙলে ব্ল্যাক বক্স কারণ হিসেবে অনুনাদের নাম দেয়।"),
    qa("Why can Level 7 fail even when TEST shows no red?",
       "TEST checks one bus standing still with no wind. The real run sends four 12 t buses across "
       "and keeps the wind rising from 4 to 36 m/s for 70 seconds, with gusts of about 1.5 m/s. "
       "The bridge must survive until the gale has passed, not just until the buses are across. "
       "Keep extra margin - FS around 2 in TEST - or fix the resonance first.",
       "'পরীক্ষা'-তে কোনো লাল না থাকলেও লেভেল 7 ব্যর্থ হয় কেন?",
       "'পরীক্ষা' বাতাস ছাড়া দাঁড়িয়ে থাকা একটি বাস যাচাই করে। আসল চালানোয় 12 t-এর চারটি বাস পার হয়, আর 70 "
       "সেকেন্ড ধরে বাতাস 4 থেকে 36 m/s-এ উঠতে থাকে, প্রায় 1.5 m/s দমকাসহ। শুধু বাস পার হওয়া পর্যন্ত নয়, ঝড় শেষ "
       "হওয়া পর্যন্ত সেতুকে টিকতে হবে। বাড়তি নিরাপত্তা রাখো - 'পরীক্ষা'-তে FS প্রায় 2 - অথবা আগে অনুনাদ ঠিক করো।"),
    # --- earthquakes (Level 8) --------------------------------------------------------------
    qa("What does the Wind lab show before I run?",
       "Open it with the lab button (L). Cards show: the natural frequency f_n from your truss "
       "(k* and m*), the vortex rhythm f_v = St U / D for the current wind, the danger wind speed "
       "U_crit compared with the strongest wind of the level, Den Hartog's best TMD tuning for your "
       "mass ratio, and during a run the extra load from the swing right now. If U_crit sits inside "
       "the wind range, fix it before pressing RUN.",
       "চালানোর আগে বাতাসের ল্যাব কী দেখায়?",
       "ল্যাব বোতাম (L) দিয়ে খোলো। কার্ডগুলো দেখায়: তোমার ট্রাস থেকে স্বাভাবিক কম্পাঙ্ক f_n (k* আর m*), এখনকার "
       "বাতাসে ঘূর্ণির তাল f_v = St U / D, লেভেলের সবচেয়ে জোরালো বাতাসের সঙ্গে তুলনা করে বিপদের বাতাস U_crit, তোমার "
       "ভর-অনুপাতের জন্য ডেন হার্টগের সেরা TMD টিউনিং, আর চালানোর সময় এই মুহূর্তে দোলার বাড়তি ভার। U_crit বাতাসের "
       "পরিসরের ভেতরে থাকলে 'চালাও' চাপার আগে ঠিক করো।"),
    qa("How is the Level 8 earthquake modelled?",
       "The ground shakes with a_g(t) = A sin(omega t) e^(-decay t): a peak of 0.35 g (3.43 m/s^2) "
       "at 1.5 Hz that dies away (decay 0.35 per second) over 12 seconds. It starts when the 20 t "
       "truck is 35% of the way across, so the truck is on the bridge during the strongest shaking. "
       "The seismograph trace shows the pulse.",
       "লেভেল 8-এর ভূমিকম্প কীভাবে মডেল করা হয়েছে?",
       "মাটি কাঁপে a_g(t) = A sin(omega t) e^(-decay t) অনুযায়ী: 1.5 Hz-এ 0.35 g (3.43 m/s^2) চূড়া, যা 12 সেকেন্ডে "
       "মিলিয়ে যায় (প্রতি সেকেন্ডে ক্ষয় 0.35)। 20 t-এর ট্রাক 35% পথ পেরোলে এটি শুরু হয়, তাই সবচেয়ে জোরালো কাঁপুনির "
       "সময় ট্রাক সেতুর উপরেই থাকে। সিসমোগ্রাফের রেখা কম্পনটি দেখায়।"),
    qa("What is base shear, V = C M a_g?",
       "The total sideways force the shaking puts on a structure: its mass M times the ground "
       "acceleration a_g, multiplied by the response factor C (how much the structure amplifies "
       "the shaking). In the game every joint feels a sideways force of its mass x C x a_g, and the "
       "truss must carry all of it down to the footings.",
       "ভিত্তির কর্তন-বল, V = C M a_g কী?",
       "কাঁপুনি একটি কাঠামোর উপর যে মোট পাশের বল দেয়: তার ভর M গুণ মাটির ত্বরণ a_g, গুণ সাড়া-গুণক C (কাঠামো "
       "কাঁপুনিকে কতটা বাড়ায়)। খেলায় প্রতিটি জোড় তার ভর x C x a_g পরিমাণ পাশের বল অনুভব করে, আর ট্রাসকে সবটা "
       "পাদভিত্তি পর্যন্ত নামিয়ে নিতে হয়।"),
    qa("What is the natural period T?",
       "The time of one full sideways sway: T = 2 pi sqrt(M / k) = 1 / f. A stiff, light bridge "
       "sways quickly (short T); a soft or heavy one sways slowly (long T). The game calculates T "
       "for your own viaduct from its real stiffness and mass, and the Quake lab card shows it with "
       "the resulting C.",
       "স্বাভাবিক পর্যায়কাল T কী?",
       "পাশের দিকে একবার পুরো দোল খেতে যে সময় লাগে: T = 2 pi sqrt(M / k) = 1 / f। দৃঢ় আর হালকা সেতু দ্রুত দোলে "
       "(ছোট T); নরম বা ভারী সেতু ধীরে দোলে (লম্বা T)। খেলাটি তোমার উঁচু সেতুর আসল দৃঢ়তা আর ভর থেকে T হিসাব করে, "
       "আর ভূমিকম্পের ল্যাবের কার্ড তা আর তার ফলে আসা C দেখায়।"),
    qa("How does the response factor C depend on T?",
       "The game uses a simplified design spectrum: T below 0.1 s gives C = 1 + 15 T; T from 0.1 to "
       "0.5 s gives the plateau C = 2.5 (the shaking is amplified 2.5 times); above 0.5 s, "
       "C = 2.5 x 0.5 / T, so it falls as the period grows. At T = 2.5 s, C = 0.5 - five times less "
       "force than on the plateau.",
       "সাড়া-গুণক C কীভাবে T-এর উপর নির্ভর করে?",
       "খেলাটি একটি সরলীকৃত নকশা-বর্ণালী ব্যবহার করে: T 0.1 s-এর কম হলে C = 1 + 15 T; T 0.1 থেকে 0.5 s হলে সমতল "
       "C = 2.5 (কাঁপুনি 2.5 গুণ বাড়ে); 0.5 s-এর উপরে C = 2.5 x 0.5 / T, তাই পর্যায়কাল বাড়লে কমে। T = 2.5 s-এ "
       "C = 0.5 - সমতলের চেয়ে পাঁচ গুণ কম বল।"),
    qa("Why can making the viaduct stiffer make it worse in an earthquake?",
       "A stiffer viaduct has a shorter period, and most stiff bridges land on the 2.5 plateau "
       "where the shaking is amplified the most. You also often add mass when you stiffen. So the "
       "force V = C M a_g goes up, and the members must be bigger again. Real seismic design "
       "either makes the structure strong enough for the full force or lets it move (isolation) "
       "so the force drops.",
       "উঁচু সেতু বেশি দৃঢ় করলে ভূমিকম্পে তা খারাপ হতে পারে কেন?",
       "বেশি দৃঢ় সেতুর পর্যায়কাল ছোট, আর বেশিরভাগ দৃঢ় সেতু 2.5-এর সমতলে পড়ে, যেখানে কাঁপুনি সবচেয়ে বেশি বাড়ে। "
       "দৃঢ় করতে গিয়ে প্রায়ই ভরও যোগ হয়। ফলে বল V = C M a_g বাড়ে, আর সদস্যদের আবার বড় করতে হয়। আসল ভূমিকম্প-নকশা "
       "হয় কাঠামোকে পুরো বলের জন্য যথেষ্ট শক্ত করে, নয়তো তাকে নড়তে দেয় (আইসোলেশন), যাতে বল কমে।"),
    qa("Why does a heavier viaduct feel more earthquake force?",
       "Because the force is mass x acceleration: every extra tonne becomes about C x 3.4 kN of "
       "sideways force at the peak, which the columns and braces must carry. Concrete is cheap but "
       "heavy; light steel members often win in Level 8 even though steel costs more per kg.",
       "ভারী উঁচু সেতু ভূমিকম্পে বেশি বল অনুভব করে কেন?",
       "কারণ বল = ভর x ত্বরণ: চূড়ায় প্রতিটি বাড়তি টন প্রায় C x 3.4 kN পাশের বল হয়ে যায়, যা স্তম্ভ আর ঠেকনাকে বইতে "
       "হয়। কংক্রিট সস্তা কিন্তু ভারী; লেভেল 8-এ হালকা ইস্পাতের সদস্য প্রায়ই জেতে, যদিও প্রতি kg ইস্পাত বেশি দামি।"),
    qa("What do isolation bearings do?",
       "Rubber-and-lead bearings let the ground move underneath while the deck glides. They "
       "stretch the period to 2.5 s, which drops C from 2.5 to 0.5 - five times less force in every "
       "member. They cost Rs 3 L in the Quake lab. The catch: the deck now moves much further "
       "sideways.",
       "আইসোলেশন বিয়ারিং কী করে?",
       "রাবার-আর-সীসার বিয়ারিং নিচে মাটিকে নড়তে দেয়, আর ডেক পিছলে চলে। এরা পর্যায়কাল 2.5 s করে, যাতে C 2.5 থেকে "
       "0.5-এ নামে - প্রতিটি সদস্যে পাঁচ গুণ কম বল। ভূমিকম্পের ল্যাবে দাম Rs 3 L। শর্ত হলো: ডেক এখন পাশে অনেক "
       "বেশি সরে।"),
    qa("Why did my isolated viaduct fail by 'pounding'?",
       "With isolation the deck drifts by C x a_g / omega^2 with omega = 2 pi / T. At the peak that "
       "is 0.5 x 3.43 / (2 pi / 2.5)^2 = about 0.27 m - but a normal joint only leaves 0.05 m of "
       "gap, so the deck slams into the abutment. Flexible expansion joints (Rs 1.5 L) give 0.40 m. "
       "Isolation without flexible joints always fails; buy them together.",
       "আমার আইসোলেটেড উঁচু সেতু 'ধাক্কা' (pounding) খেয়ে ব্যর্থ হলো কেন?",
       "আইসোলেশনে ডেক সরে C x a_g / omega^2, যেখানে omega = 2 pi / T। চূড়ায় তা 0.5 x 3.43 / (2 pi / 2.5)^2 = "
       "প্রায় 0.27 m - কিন্তু সাধারণ জোড়ে মাত্র 0.05 m ফাঁক থাকে, তাই ডেক অ্যাবাটমেন্টে আছড়ে পড়ে। নমনীয় "
       "সম্প্রসারণ-জোড় (Rs 1.5 L) 0.40 m দেয়। নমনীয় জোড় ছাড়া আইসোলেশন সবসময় ব্যর্থ; দুটি একসঙ্গে কেনো।"),
    qa("Why does every bay of the viaduct need a diagonal?",
       "In Level 8 the bank anchors are rollers: they hold the deck up but cannot take a sideways "
       "push. So the whole sideways earthquake force must travel down through your columns to the "
       "pinned footings on the valley floor. A column bay without a diagonal is a square - it "
       "sways like a parallelogram and folds. Diagonals (or an X) turn each bay into triangles.",
       "উঁচু সেতুর প্রতিটি খোপে একটি কর্ণ লাগে কেন?",
       "লেভেল 8-এ পাড়ের নোঙরগুলো রোলার: এরা ডেককে উপরে ধরে রাখে কিন্তু পাশের ঠেলা নিতে পারে না। তাই ভূমিকম্পের পুরো "
       "পাশের বল তোমার স্তম্ভ দিয়ে উপত্যকার তলার পিন-করা পাদভিত্তি পর্যন্ত নামতে হয়। কর্ণ ছাড়া স্তম্ভের খোপ একটি "
       "বর্গ - সমান্তরিকের মতো দুলে ভাঁজ হয়ে যায়। কর্ণ (বা X) প্রতিটি খোপকে ত্রিভুজে বদলায়।"),
    qa("Can I use concrete for the Level 8 braces?",
       "Not for diagonals. Shaking reverses direction about three times a second, so a brace that "
       "is pushed now is pulled a moment later - and plain concrete fails the instant it is "
       "pulled. Concrete can work for columns that stay squeezed by the deck's weight, but use "
       "steel (or timber) for every brace.",
       "লেভেল 8-এর ঠেকনায় কি কংক্রিট ব্যবহার করা যায়?",
       "কর্ণে নয়। কাঁপুনি সেকেন্ডে প্রায় তিনবার দিক বদলায়, তাই যে ঠেকনা এখন ঠেলা খাচ্ছে পরমুহূর্তে সেটি টানা খায় - আর "
       "সাধারণ কংক্রিট টানা পড়লেই সঙ্গে সঙ্গে ভাঙে। ডেকের ওজনে চাপে থাকা স্তম্ভে কংক্রিট চলতে পারে, কিন্তু প্রতিটি "
       "ঠেকনায় ইস্পাত (বা কাঠ) ব্যবহার করো।"),
    qa("What is the 'robust' way through Level 8?",
       "Massive X-braced steel piers that resist the full shaking with C = 2.5: no isolation, no "
       "joints, just strength. It works, but all that extra steel makes it hard to stay under the Rs 15 L par. "
       "The 'clever' way is slender braced piers on isolation bearings plus flexible joints, which "
       "cut the force five times for Rs 4.5 L of extras.",
       "লেভেল 8 পার হওয়ার 'মজবুত' উপায় কী?",
       "বিশাল X-ঠেকনা দেওয়া ইস্পাতের স্তম্ভ, যা C = 2.5-এ পুরো কাঁপুনি সয়: আইসোলেশন নেই, জোড় নেই, শুধু শক্তি। "
       "এটি কাজ করে, কিন্তু এত বাড়তি ইস্পাতে Rs 15 L প্যারের নিচে থাকা কঠিন। 'চতুর' উপায় হলো আইসোলেশন বিয়ারিং "
       "আর নমনীয় জোড়ের উপর সরু ঠেকনা-দেওয়া স্তম্ভ, যা Rs 4.5 L বাড়তি খরচে বল পাঁচ গুণ কমায়।"),
    # --- rail grades (Levels 2 and 4) --------------------------------------------------------
    qa("What does the Quake lab show?",
       "Your viaduct's lateral period T (and 2.5 s with bearings), the factor C for both cases, the "
       "base shear at the peak V = C M a_g with your bridge's mass, and how far an isolated deck "
       "would drift compared with the joint gap. Read it before you buy anything: if the drift is "
       "bigger than the gap, isolation needs flexible joints too.",
       "ভূমিকম্পের ল্যাব কী দেখায়?",
       "তোমার উঁচু সেতুর পাশের পর্যায়কাল T (আর বিয়ারিংসহ 2.5 s), দুই ক্ষেত্রের গুণক C, তোমার সেতুর ভর দিয়ে চূড়ায় "
       "ভিত্তির কর্তন-বল V = C M a_g, আর আইসোলেটেড ডেক জোড়ের ফাঁকের তুলনায় কতটা সরবে। কিছু কেনার আগে পড়ো: সরণ "
       "ফাঁকের চেয়ে বড় হলে আইসোলেশনের সঙ্গে নমনীয় জোড়ও লাগবে।"),
    qa("How much does a slope pull a train back?",
       "Gravity along the slope is F = m g sin(theta). For gentle slopes sin(theta) is almost the "
       "grade: a 1% grade (1 m up per 100 m) pulls back about 1% of the train's weight. A 150 t "
       "train on an 8% grade is pulled back by about 117 kN. Drag a track handle steeper and "
       "the red gravity arrow grows.",
       "ঢাল একটি ট্রেনকে কতটা পিছনে টানে?",
       "ঢাল বরাবর মাধ্যাকর্ষণ F = m g sin(theta)। মৃদু ঢালে sin(theta) প্রায় ঢালের মানই: 1% ঢাল (প্রতি 100 m-এ 1 m "
       "ওঠা) ট্রেনের ওজনের প্রায় 1% পিছনে টানে। 8% ঢালে 150 t-এর ট্রেনকে প্রায় 117 kN পিছনে টানে। লাইনের হাতল খাড়া "
       "করে টানো, লাল মাধ্যাকর্ষণের তীর বড় হবে।"),
    qa("What is adhesion, F_grip = mu N?",
       "Steel wheels on steel rails grip only a fraction of the weight pressing on the driving "
       "wheels: mu = 0.30 on dry rails and 0.18 on wet rails. Only the locomotive's own weight "
       "counts - wagons are not driven. So a 60 t shunter can pull at most 0.30 x 60 t x g = about "
       "177 kN, however powerful its engine. Ask for more and the wheels slip.",
       "আঁকড়ে ধরা (adhesion), F_grip = mu N কী?",
       "ইস্পাতের লাইনে ইস্পাতের চাকা চালক-চাকার উপর চাপ দেওয়া ওজনের শুধু একটি ভগ্নাংশ আঁকড়ে ধরে: শুকনো লাইনে "
       "mu = 0.30, ভেজায় 0.18। শুধু ইঞ্জিনের নিজের ওজন গোনা হয় - ওয়াগন চালিত নয়। তাই 60 t-এর শান্টার যত শক্তিশালীই "
       "হোক, সর্বোচ্চ 0.30 x 60 t x g = প্রায় 177 kN টানতে পারে। বেশি চাইলে চাকা পিছলায়।"),
    qa("What is tractive effort T = min(P / v, mu N)?",
       "The engine's pull. At low speed it is limited by grip (mu N); at higher speed by power, "
       "because power = force x speed, so pull = P / v falls as you go faster. A 500 kW shunter "
       "can pull 177 kN only below about 2.8 m/s; at 10 m/s its power allows just 50 kN. That is "
       "why trains slow down on long climbs.",
       "টানার বল T = min(P / v, mu N) কী?",
       "ইঞ্জিনের টান। কম গতিতে এটি আঁকড়ে ধরা (mu N) দিয়ে সীমিত; বেশি গতিতে শক্তি দিয়ে, কারণ শক্তি = বল x গতি, "
       "তাই টান = P / v গতি বাড়লে কমে। 500 kW-এর শান্টার শুধু প্রায় 2.8 m/s-এর নিচে 177 kN টানতে পারে; 10 m/s-এ "
       "তার শক্তি মাত্র 50 kN দেয়। এজন্যই লম্বা চড়াইয়ে ট্রেন ধীর হয়।"),
    qa("How steep a grade can my train climb?",
       "At crawling speed it can hold tan(theta) = mu x m_loco / m_train - C_rr, with C_rr = 0.002. "
       "Diesel shunter (60 t) with 2 wagons of 45 t (150 t): 0.30 x 60 / 150 - 0.002 = 11.8%. With "
       "4 wagons (240 t): only 7.3%. The track labels show this: red = too steep for this train, "
       "yellow = close, blue = downhill.",
       "আমার ট্রেন কতটা খাড়া ঢাল উঠতে পারে?",
       "হামাগুড়ির গতিতে সে ধরে রাখতে পারে tan(theta) = mu x m_ইঞ্জিন / m_ট্রেন - C_rr, যেখানে C_rr = 0.002। ডিজেল "
       "শান্টার (60 t) আর 45 t-এর 2 ওয়াগন (150 t): 0.30 x 60 / 150 - 0.002 = 11.8%। 4 ওয়াগনে (240 t): মাত্র 7.3%। "
       "লাইনের লেবেল এটি দেখায়: লাল = এই ট্রেনের জন্য খুব খাড়া, হলুদ = কাছাকাছি, নীল = উৎরাই।"),
    qa("'Even grade' or 'Follow hill' in Level 2?",
       "Follow hill lays the track on the ground: no earthworks, but the hill between x = 20 and "
       "80 m rises 8 m in 60 m - a 13.3% stretch that stalls almost any train. Even grade reshapes "
       "the track into one steady 8% slope between the stations (8 m over 100 m) for the cost of "
       "the cuttings and embankments. The steepest bit is what stalls a train, so smoothing it "
       "usually pays.",
       "লেভেল 2-এ 'সমান ঢাল' নাকি 'পাহাড় বরাবর'?",
       "'পাহাড় বরাবর' লাইন মাটির উপর বসায়: মাটির কাজ নেই, কিন্তু x = 20 থেকে 80 m-এর পাহাড় 60 m-এ 8 m ওঠে - "
       "13.3%-এর একটি অংশ, যা প্রায় যেকোনো ট্রেনকে আটকে দেয়। 'সমান ঢাল' কাটা আর বাঁধের খরচে স্টেশনগুলোর মধ্যে "
       "লাইনকে একটানা 8% ঢালে (100 m-এ 8 m) বদলায়। সবচেয়ে খাড়া অংশই ট্রেন আটকায়, তাই সমান করা সাধারণত লাভজনক।"),
    qa("What do track and earthworks cost?",
       "Track costs Rs 3,000 per metre. Digging a cutting costs Rs 2,500 per m^2 of cross-section "
       "drawn and building an embankment Rs 2,000 per m^2 in Level 2; on the rocky Eagle Pass "
       "(Level 4) Rs 9,000 and Rs 7,000. So small changes to the handles near the ground are cheap, "
       "and big cuts through the summit are expensive.",
       "লাইন আর মাটির কাজের খরচ কত?",
       "লাইনের খরচ প্রতি মিটারে Rs 3,000। লেভেল 2-এ কাটা খুঁড়তে আঁকা প্রস্থচ্ছেদের প্রতি m^2-এ Rs 2,500 আর বাঁধ "
       "বানাতে Rs 2,000; পাথুরে ঈগল গিরিপথে (লেভেল 4) Rs 9,000 আর Rs 7,000। তাই মাটির কাছে হাতলের ছোট পরিবর্তন "
       "সস্তা, আর চূড়ার ভেতর দিয়ে বড় কাটা দামি।"),
    qa("Which locomotive should I choose?",
       "Tank engine: 250 kW, 30 t, Rs 1.5 L, up to 12 m/s. Diesel shunter: 500 kW, 60 t, Rs 3.5 L, "
       "14 m/s. Mainline diesel: 2.2 MW, 120 t, Rs 10 L, 20 m/s. Double-header: two mainline "
       "engines, 4.4 MW, 240 t, Rs 18 L. Weight is grip: a heavier engine can pull more before "
       "slipping. Pick the cheapest one whose grip limit covers your train on the steepest bit.",
       "কোন ইঞ্জিন বাছব?",
       "ট্যাংক ইঞ্জিন: 250 kW, 30 t, Rs 1.5 L, সর্বোচ্চ 12 m/s। ডিজেল শান্টার: 500 kW, 60 t, Rs 3.5 L, 14 m/s। "
       "মেইনলাইন ডিজেল: 2.2 MW, 120 t, Rs 10 L, 20 m/s। জোড়া ইঞ্জিন: দুটি মেইনলাইন ইঞ্জিন, 4.4 MW, 240 t, Rs 18 L। "
       "ওজনই আঁকড়ে ধরা: ভারী ইঞ্জিন পিছলানোর আগে বেশি টানতে পারে। সবচেয়ে খাড়া অংশে যার আঁকড়ে ধরার সীমা তোমার "
       "ট্রেন সামলায়, তার মধ্যে সবচেয়ে সস্তাটি বাছো।"),
    qa("What does the banker engine add (Level 2)?",
       "A pusher at the back: +400 kW of power and +50 t of driven weight, so +0.30 x 50 t x g = "
       "about 147 kN more grip. It costs Rs 2.5 L. It is the 'high cost, robust' path - haul more "
       "wagons per trip without slipping - while the clever path is fewer wagons and more trips.",
       "ব্যাংকার ইঞ্জিন কী যোগ করে (লেভেল 2)?",
       "পেছনে একটি ঠেলা-ইঞ্জিন: +400 kW শক্তি আর +50 t চালিত ওজন, তাই +0.30 x 50 t x g = প্রায় 147 kN বেশি আঁকড়ে "
       "ধরা। দাম Rs 2.5 L। এটি 'বেশি খরচ, নিশ্চিত' পথ - না পিছলে প্রতি যাত্রায় বেশি ওয়াগন - আর চতুর পথ হলো কম "
       "ওয়াগন আর বেশি যাত্রা।"),
    qa("How heavy are the wagons and what do they cost?",
       "Level 2 log wagons carry 30 t and weigh 15 t empty; up to 6 per train; Rs 20,000 each. "
       "Level 4 ore wagons carry 60 t and weigh 22 t empty; up to 12 per train; Rs 50,000 each. "
       "Remember the engine must pull the empty weight too: a full Level 2 wagon is 45 t.",
       "ওয়াগন কতটা ভারী আর দাম কত?",
       "লেভেল 2-এর কাঠের ওয়াগন 30 t বয় আর খালি অবস্থায় 15 t; প্রতি ট্রেনে সর্বোচ্চ 6টি; প্রতিটি Rs 20,000। লেভেল "
       "4-এর আকরিকের ওয়াগন 60 t বয় আর খালি 22 t; প্রতি ট্রেনে সর্বোচ্চ 12টি; প্রতিটি Rs 50,000। মনে রেখো ইঞ্জিনকে "
       "খালি ওজনও টানতে হয়: লেভেল 2-এর একটি ভরা ওয়াগন 45 t।"),
    qa("How is the total job time worked out?",
       "Trips = cargo target / cargo per train, rounded up. The game runs one loaded trip and then "
       "counts: total time = trips x trip time + the empty runs back. Level 2 needs 120 t in 2 "
       "minutes; Level 4 needs 600 t in 8 minutes. More wagons mean fewer trips but a heavier, "
       "slower train - find the balance.",
       "মোট কাজের সময় কীভাবে হিসাব হয়?",
       "যাত্রা = মালের লক্ষ্য / প্রতি ট্রেনের মাল, উপরের দিকে পূর্ণসংখ্যা। খেলাটি একটি ভরা যাত্রা চালায়, তারপর গোনে: "
       "মোট সময় = যাত্রা x যাত্রার সময় + খালি ফেরার পথ। লেভেল 2-এ 2 মিনিটে 120 t; লেভেল 4-এ 8 মিনিটে 600 t। বেশি "
       "ওয়াগন মানে কম যাত্রা, কিন্তু ভারী আর ধীর ট্রেন - ভারসাম্য খুঁজে নাও।"),
    qa("The train shows WHEEL SLIP. What should I do?",
       "The engine is asking for more pull than its grip allows (P / v is above mu N). The train "
       "will slow and may stall on the steepest part. Fix it by carrying fewer wagons, flattening "
       "the steepest stretch, choosing a heavier engine (more weight = more grip) or adding the "
       "banker in Level 2. More power alone does not help when the wheels are already slipping.",
       "ট্রেনে 'চাকা পিছলাচ্ছে' দেখাচ্ছে। কী করব?",
       "ইঞ্জিন তার আঁকড়ে ধরার সীমার চেয়ে বেশি টান চাইছে (P / v, mu N-এর উপরে)। ট্রেন ধীর হবে আর সবচেয়ে খাড়া "
       "অংশে আটকে যেতে পারে। সমাধান: কম ওয়াগন নাও, সবচেয়ে খাড়া অংশ সমান করো, ভারী ইঞ্জিন বাছো (বেশি ওজন = বেশি "
       "আঁকড়ে ধরা), অথবা লেভেল 2-এ ব্যাংকার যোগ করো। চাকা আগে থেকেই পিছলালে শুধু বেশি শক্তিতে লাভ নেই।"),
    qa("Can the cheap tank engine finish Level 2?",
       "On the even 8% grade a 30 t tank engine can lift one wagon (75 t train: limit 11.8%) but "
       "not two (120 t: limit 7.3%). One wagon carries 30 t, so 120 t needs four loaded trips, "
       "with only 250 kW and 12 m/s. Check the job time against the 2-minute limit in the "
       "calculator. The diesel shunter with 2 wagons and two trips is the safer cheap plan.",
       "সস্তা ট্যাংক ইঞ্জিন কি লেভেল 2 শেষ করতে পারে?",
       "সমান 8% ঢালে 30 t-এর ট্যাংক ইঞ্জিন একটি ওয়াগন তুলতে পারে (75 t ট্রেন: সীমা 11.8%), কিন্তু দুটি নয় (120 t: "
       "সীমা 7.3%)। একটি ওয়াগন 30 t নেয়, তাই 120 t-এর জন্য চারটি ভরা যাত্রা লাগে, মাত্র 250 kW আর 12 m/s নিয়ে। "
       "ক্যালকুলেটরে কাজের সময় 2 মিনিটের সীমার সঙ্গে মিলিয়ে দেখো। 2 ওয়াগন আর দুই যাত্রাসহ ডিজেল শান্টারই বেশি "
       "নিরাপদ সস্তা পরিকল্পনা।"),
    qa("How does momentum p = m v help a train?",
       "A heavy moving train carries a lot of momentum. On a short steep crest it can coast over "
       "even where its engine alone could not climb at crawling speed, because it spends its "
       "kinetic energy on the way up. But on a long climb the speed is used up, so the grip limit "
       "still decides.",
       "ভরবেগ p = m v ট্রেনকে কীভাবে সাহায্য করে?",
       "চলমান ভারী ট্রেন অনেক ভরবেগ বয়। ছোট খাড়া চূড়ায় সে গড়িয়ে পার হয়ে যেতে পারে, এমনকি যেখানে শুধু ইঞ্জিন দিয়ে "
       "হামাগুড়ির গতিতে উঠতে পারত না, কারণ ওঠার পথে সে গতিশক্তি খরচ করে। কিন্তু লম্বা চড়াইয়ে গতি ফুরিয়ে যায়, তাই "
       "তখনও আঁকড়ে ধরার সীমাই ঠিক করে।"),
    qa("What do the energy bars (KE, PE) show?",
       "Kinetic energy KE = 1/2 m v^2 and potential energy PE = m g h. Climbing turns the engine's "
       "work into height (PE); descending turns height back into speed (KE), and the brakes must "
       "turn that energy into heat. A 600 t train dropping 12 m releases about 70 MJ that the "
       "brakes have to absorb.",
       "শক্তির বার (KE, PE) কী দেখায়?",
       "গতিশক্তি KE = 1/2 m v^2 আর স্থিতিশক্তি PE = m g h। চড়াইয়ে ইঞ্জিনের কাজ উচ্চতায় (PE) বদলায়; উৎরাইয়ে "
       "উচ্চতা আবার গতিতে (KE) বদলায়, আর ব্রেককে সেই শক্তি তাপে বদলাতে হয়। 600 t-এর ট্রেন 12 m নামলে প্রায় 70 MJ "
       "বেরোয়, যা ব্রেককে শুষতে হয়।"),
    qa("How far does a train need to stop?",
       "d_stop = v^2 / (2 (mu g cos(theta) - g sin(theta))) going downhill. On level dry rails "
       "(mu = 0.30) a train at 20 m/s needs about 68 m; on level wet rails (mu = 0.18) about 113 m; "
       "on a wet 8% descent the slope eats most of the grip and it needs more than 200 m. Speed "
       "counts twice: double the speed and the distance becomes four times longer.",
       "একটি ট্রেনের থামতে কতটা পথ লাগে?",
       "উৎরাইয়ে d_stop = v^2 / (2 (mu g cos(theta) - g sin(theta)))। সমতল শুকনো লাইনে (mu = 0.30) 20 m/s-এর ট্রেনের "
       "লাগে প্রায় 68 m; সমতল ভেজা লাইনে (mu = 0.18) প্রায় 113 m; ভেজা 8% উৎরাইয়ে ঢাল আঁকড়ে ধরার বেশিরভাগ খেয়ে "
       "ফেলে, তখন 200 m-এর বেশি লাগে। গতি দুবার গোনা হয়: গতি দ্বিগুণ হলে দূরত্ব চার গুণ হয়।"),
    qa("When can no brake stop a train?",
       "When g sin(theta) > mu g cos(theta), that is when the grade (tan theta) is bigger than mu: "
       "steeper than 30% on dry rails, or steeper than 18% (about 10 degrees) on wet rails. Then "
       "gravity beats the brakes and the train runs away. Long before that, a steep wet descent "
       "can also make the train too fast (OVERSPEED). Keep descents gentle, especially where it "
       "rains.",
       "কখন কোনো ব্রেকই ট্রেন থামাতে পারে না?",
       "যখন g sin(theta) > mu g cos(theta), অর্থাৎ ঢাল (tan theta) mu-এর চেয়ে বড়: শুকনো লাইনে 30%-এর বেশি খাড়া, "
       "বা ভেজা লাইনে 18%-এর (প্রায় 10 ডিগ্রি) বেশি খাড়া। তখন মাধ্যাকর্ষণ ব্রেককে হারায় আর ট্রেন নিয়ন্ত্রণ হারায়। তার "
       "অনেক আগেই খাড়া ভেজা উৎরাই ট্রেনকে অতিরিক্ত দ্রুত (OVERSPEED) করে দিতে পারে। উৎরাই মৃদু রাখো, বিশেষ করে "
       "যেখানে বৃষ্টি হয়।"),
    qa("How do I place the brake marker in Level 4?",
       "The train brakes fully from the marker, so the distance you allow is stop line - marker. "
       "Too late and it hits the buffers ('HIT THE BUFFERS': the Black Box shows the distance it "
       "needed and the distance you gave). Too early is safe - the train stops short and crawls to "
       "the line - but slower. For the bonus star stop within 15 m of the stop line. The demo "
       "brakes 80 m before it.",
       "লেভেল 4-এ ব্রেকের চিহ্ন কোথায় রাখব?",
       "চিহ্ন থেকে ট্রেন পুরো ব্রেক করে, তাই তুমি যে দূরত্ব দাও তা হলো থামার দাগ - চিহ্ন। দেরি হলে বাফারে ধাক্কা "
       "('বাফারে ধাক্কা': ব্ল্যাক বক্স দেখায় কত দূরত্ব লাগত আর তুমি কত দিয়েছিলে)। আগে হলে নিরাপদ - ট্রেন আগে থেমে "
       "হামাগুড়ি দিয়ে দাগ পর্যন্ত যায় - তবে ধীর। বোনাস তারার জন্য থামার দাগের 15 m-এর মধ্যে থামো। প্রদর্শনী দাগের "
       "80 m আগে ব্রেক করে।"),
    # --- signals braking (Level 5) ------------------------------------------------------------
    qa("Why must signals be spaced at least a braking distance apart?",
       "A train passing a YELLOW must be able to stop before the next RED. A passenger train at "
       "25 m/s brakes at 0.09 g: d_stop = 25^2 / (2 x 0.09 x 9.81) = about 354 m. A cargo train at "
       "18 m/s brakes at only 0.05 g: about 330 m. Put a signal closer than that to the one ahead "
       "and a train sails past the red - a SPAD (signal passed at danger).",
       "সিগন্যালগুলো অন্তত একটি ব্রেক-দূরত্ব দূরে রাখতে হবে কেন?",
       "হলুদ পেরোনো ট্রেনকে পরের লালের আগে থামতে পারতে হবে। 25 m/s-এর যাত্রীবাহী ট্রেন 0.09 g-তে ব্রেক করে: "
       "d_stop = 25^2 / (2 x 0.09 x 9.81) = প্রায় 354 m। 18 m/s-এর মালগাড়ি মাত্র 0.05 g-তে ব্রেক করে: প্রায় 330 m। "
       "সামনেরটির এর চেয়ে কাছে সিগন্যাল বসালে ট্রেন লাল পেরিয়ে চলে যায় - একটি SPAD (বিপদে সিগন্যাল পার)।"),
    qa("3-aspect or 4-aspect signals?",
       "3-aspect: RED (stop), YELLOW (the next signal is red - start braking), GREEN. 4-aspect adds "
       "DOUBLE YELLOW (the signal after next is red), so the warning spans two blocks and each block "
       "only needs half the braking distance. More, shorter blocks let trains follow closer. But a "
       "4-aspect signal costs Rs 4.5 L against Rs 3 L.",
       "3-অ্যাসপেক্ট নাকি 4-অ্যাসপেক্ট সিগন্যাল?",
       "3-অ্যাসপেক্ট: লাল (থামো), হলুদ (পরের সিগন্যাল লাল - ব্রেক শুরু করো), সবুজ। 4-অ্যাসপেক্ট যোগ করে জোড়া হলুদ "
       "(পরেরটির পরের সিগন্যাল লাল), তাই সতর্কতা দুটি ব্লক জুড়ে থাকে আর প্রতিটি ব্লকে শুধু অর্ধেক ব্রেক-দূরত্ব লাগে। "
       "বেশি আর ছোট ব্লকে ট্রেন কাছাকাছি চলতে পারে। কিন্তু 4-অ্যাসপেক্ট সিগন্যালের দাম Rs 4.5 L, যেখানে 3-অ্যাসপেক্ট "
       "Rs 3 L।"),
    # --- maglev and the smart grid (Level 10) ----------------------------------------------------
    qa("How does the maglev pod accelerate, P = F v?",
       "The linear motor gives at most 220 kN of thrust and 3 MW of power. Below about 13.6 m/s the "
       "thrust limit rules (220 kN pushes the 60 t pod at about 3.7 m/s^2); above it the power "
       "rules, F = P / v, so at 40 m/s only 75 kN is left. There are no wheels, so there is no grip "
       "limit and no rolling resistance.",
       "ম্যাগলেভ পড কীভাবে গতি বাড়ায়, P = F v?",
       "লিনিয়ার মোটর সর্বোচ্চ 220 kN ঠেলা আর 3 MW শক্তি দেয়। প্রায় 13.6 m/s-এর নিচে ঠেলার সীমা নিয়ন্ত্রণ করে (220 kN "
       "60 t-এর পডকে প্রায় 3.7 m/s^2-এ ঠেলে); এর উপরে শক্তি নিয়ন্ত্রণ করে, F = P / v, তাই 40 m/s-এ মাত্র 75 kN বাকি "
       "থাকে। চাকা নেই, তাই আঁকড়ে ধরার সীমা বা গড়ানোর বাধা নেই।"),
    qa("How many MW should the smart grid have in Level 10?",
       "The pod needs its full 3 MW to reach speed in time, and powered smart alloy draws 50 kW per "
       "tonne from the same grid. Power left for the pod = grid MW - alloy MW; if it is only part "
       "of 3 MW, thrust is scaled down and the crossing may take longer than 9.5 s. Below half power "
       "the Black Box reports a brownout. Each MW costs Rs 4 L, so buy about 3 MW plus the alloy's "
       "share, not 8.",
       "লেভেল 10-এ স্মার্ট গ্রিডে কত MW রাখব?",
       "সময়মতো গতি পেতে পডের পুরো 3 MW লাগে, আর চালু স্মার্ট সংকর ধাতু একই গ্রিড থেকে প্রতি টনে 50 kW নেয়। পডের জন্য "
       "বাকি শক্তি = গ্রিড MW - সংকর ধাতুর MW; তা 3 MW-এর শুধু একটি অংশ হলে ঠেলা কমে যায় আর পার হতে 9.5 s-এর বেশি "
       "লাগতে পারে। অর্ধেক শক্তির নিচে ব্ল্যাক বক্স বিদ্যুৎ-ঘাটতি (brownout) জানায়। প্রতি MW-এর দাম Rs 4 L, তাই 8 নয়, "
       "প্রায় 3 MW আর সংকর ধাতুর ভাগটুকু কেনো।"),
    qa("Should I power the smart alloy?",
       "Powering doubles the alloy's stiffness E, which raises the bridge's natural frequency (by up "
       "to about 41% if the whole bridge were alloy) and reduces sag - useful against the rising "
       "wind. But it draws 50 kW per tonne of alloy from the grid that also drives the pod. Power "
       "it only if the wind is the problem, and add that load to your grid MW.",
       "স্মার্ট সংকর ধাতু কি চালু করব?",
       "চালু করলে সংকর ধাতুর দৃঢ়তা E দ্বিগুণ হয়, যা সেতুর স্বাভাবিক কম্পাঙ্ক বাড়ায় (পুরো সেতু সংকর ধাতুর হলে প্রায় 41% "
       "পর্যন্ত) আর ঝোলা কমায় - বাড়তে থাকা বাতাসের বিরুদ্ধে কাজের। কিন্তু এটি সেই গ্রিড থেকে প্রতি টন ধাতুতে 50 kW "
       "নেয়, যা পডকেও চালায়। শুধু বাতাসই সমস্যা হলে চালু করো, আর সেই ভার তোমার গ্রিড MW-এ যোগ করো।"),
)
