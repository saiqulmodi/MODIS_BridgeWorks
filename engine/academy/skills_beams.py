"""Game skills, part 2: Help Q51-100 (beams and the balanced cantilever) as multiple-choice
questions.

The question and the explanation are the Help screen's own text in both languages; only the
four options are written here, the right one first (the loader shuffles them)."""
from game.guide.beams import BEAMS

from . import mcq

_OPTS = (
    # Q51 bending moment
    (("A turning effect: force x distance, like your weight times your distance on a see-saw", "The weight of the beam per metre", "The speed at which a beam bends", "A beam's length times its width"),
     ("ঘোরানোর প্রভাব: বল x দূরত্ব, যেমন ঢেঁকিতে তোমার ওজন গুণ মাঝ থেকে দূরত্ব", "প্রতি মিটারে বিমের ওজন", "বিম কত দ্রুত বাঁকে", "বিমের দৈর্ঘ্য গুণ প্রস্থ")),
    # Q52 sagging and hogging
    (("Sagging bends like a smile (bottom pulled); hogging like a frown (top pulled), as over a pier", "Sagging is when the top is pulled", "Both mean the beam is broken", "They are two kinds of concrete"),
     ("ঝোলা মানে হাসির মতো বাঁকা (নিচে টান); কুঁজো মানে ভ্রুকুটির মতো (উপরে টান), যেমন স্তম্ভের উপরে", "ঝোলা মানে উপরে টান", "দুটোরই মানে বিম ভেঙেছে", "এরা দুই রকম কংক্রিট")),
    # Q53 sigma = My/I
    (("Bending stress: zero at the neutral axis and largest at the top and bottom surfaces", "Stress is equal everywhere in the section", "Stress is largest in the middle of the section", "It gives the beam's weight"),
     ("বাঁকানো পীড়ন: নিরপেক্ষ অক্ষে শূন্য, আর উপরের ও নিচের তলে সবচেয়ে বেশি", "প্রস্থচ্ছেদের সব জায়গায় পীড়ন সমান", "প্রস্থচ্ছেদের মাঝখানে পীড়ন সবচেয়ে বেশি", "এটা বিমের ওজন দেয়")),
    # Q54 I = bd³/12
    (("I grows with the cube of depth: double the depth and I becomes 8 times bigger", "Doubling depth doubles I", "Width matters more than depth", "Depth has no effect on I"),
     ("I বাড়ে গভীরতার ঘনফলে: গভীরতা দ্বিগুণ করলে I ৮ গুণ হয়", "গভীরতা দ্বিগুণ করলে I দ্বিগুণ", "গভীরতার চেয়ে প্রস্থ বেশি জরুরি", "গভীরতায় I বদলায় না")),
    # Q55 section modulus
    (("Section modulus S = bd²/6 grows 4 times while the area only doubles", "Deep beams use less concrete in total", "The weight halves when depth doubles", "Strength does not depend on depth"),
     ("প্রস্থচ্ছেদ-গুণাঙ্ক S = bd²/6 চার গুণ বাড়ে, অথচ ক্ষেত্রফল মাত্র দ্বিগুণ", "গভীর বিমে মোট কংক্রিট কম লাগে", "গভীরতা দ্বিগুণ হলে ওজন অর্ধেক হয়", "শক্তি গভীরতার উপর নির্ভর করে না")),
    # Q56 neutral axis
    (("The line in a bent section that is neither stretched nor squeezed", "The strongest line in the beam", "The line where the beam will break", "The road's centre line"),
     ("বাঁকা প্রস্থচ্ছেদের যে রেখা টান বা চাপ কিছুই খায় না", "বিমের সবচেয়ে শক্ত রেখা", "যে রেখায় বিম ভাঙবে", "রাস্তার মাঝের রেখা")),
    # Q57 I-beam flanges and web
    (("Material far from the neutral axis in the flanges gives the most I; the thin web carries shear", "Wide flanges make the beam lighter to paint", "The web carries all the bending", "Flanges stop rain"),
     ("নিরপেক্ষ অক্ষ থেকে দূরে ফ্ল্যাঞ্জে উপাদান রাখলে সবচেয়ে বেশি I; সরু ওয়েব কৃন্তন বয়", "চওড়া ফ্ল্যাঞ্জে রং করা সহজ", "ওয়েবই সব বাঁকানো বয়", "ফ্ল্যাঞ্জ বৃষ্টি আটকায়")),
    # Q58 shear stress
    (("The sliding effect between slices; largest at the neutral axis and near the supports", "Stress caused by cutting with scissors only", "Largest at the top surface at mid-span", "Another name for bending stress"),
     ("পাশাপাশি স্তরের পিছলে যাওয়ার প্রভাব; নিরপেক্ষ অক্ষে আর ভরস্থলের কাছে সবচেয়ে বেশি", "শুধু কাঁচি দিয়ে কাটার পীড়ন", "মাঝ-বিস্তারে উপরের তলে সবচেয়ে বেশি", "বাঁকানো পীড়নের আরেক নাম")),
    # Q59 shear and moment
    (("The moment changes at a rate equal to the shear; where shear passes zero the moment peaks", "They are always equal", "Shear is largest where the moment peaks", "They are unrelated"),
     ("ভ্রামক বদলায় কৃন্তনের সমান হারে; যেখানে কৃন্তন শূন্য পেরোয় সেখানে ভ্রামক সর্বোচ্চ", "এরা সবসময় সমান", "ভ্রামক যেখানে সর্বোচ্চ সেখানে কৃন্তনও সর্বোচ্চ", "এদের কোনো সম্পর্ক নেই")),
    # Q60 standard cases
    (("Central point load PL/4, uniform load wL²/8; cantilever tip load PL, uniform wL²/2", "Every case gives M = PL", "Central point load gives PL/2", "Uniform load gives wL/8"),
     ("মাঝে বিন্দু-ভার PL/4, সুষম ভার wL²/8; ক্যান্টিলিভারের ডগায় ভার PL, সুষম wL²/2", "সব ক্ষেত্রে M = PL", "মাঝে বিন্দু-ভারে PL/2", "সুষম ভারে wL/8")),
    # Q61 hand estimate chord force
    (("Treat the truss as one beam: about 185 kN*m ÷ 3 m depth ≈ 62 kN in each chord", "Chord force equals the van's weight, 34 kN", "Chord force is zero in a truss", "It cannot be estimated by hand"),
     ("ট্রাসকে একটা বিম ধরো: প্রায় ১৮৫ কিলোনিউটন-মিটার ÷ ৩ মিটার গভীরতা ≈ প্রতি কর্ডে ৬২ কিলোনিউটন", "কর্ড-বল ভ্যানের ওজনের সমান, ৩৪ কিলোনিউটন", "ট্রাসে কর্ড-বল শূন্য", "হাতে আন্দাজ করা যায় না")),
    # Q62 deflection
    (("PL³/(48EI): it grows with the cube of the span and falls with stiffness EI", "It is the same for every span", "It grows with the square root of span", "Only the load matters"),
     ("PL³/(48EI): বিস্তারের ঘনফলে বাড়ে আর দৃঢ়তা EI বাড়লে কমে", "সব বিস্তারে সমান", "বিস্তারের বর্গমূলে বাড়ে", "শুধু ভার জরুরি")),
    # Q63 continuous beam
    (("A beam over three or more supports; hogging over inner supports lowers the mid-span moment", "A beam that is never stopped by traffic", "A beam with no supports", "Several separate simple spans"),
     ("তিন বা বেশি ভরস্থলের উপর টানা বিম; ভিতরের ভরস্থলে কুঁজো হওয়া মাঝ-বিস্তারের ভ্রামক কমায়", "যে বিমে যান কখনো থামে না", "ভরস্থলহীন বিম", "কয়েকটা আলাদা সরল বিস্তার")),
    # Q64 balanced cantilever
    (("Built outwards from piers segment by segment on both sides, like a growing see-saw, without scaffolding", "A bridge hung from a single cable", "A bridge built on scaffolding from the riverbed", "A floating pontoon bridge"),
     ("স্তম্ভ থেকে দুদিকে খণ্ড ধরে ধরে বাইরে বানানো, বাড়তে থাকা ঢেঁকির মতো, ভারা ছাড়াই", "একটা কেবলে ঝোলানো সেতু", "নদীর তলা থেকে ভারা বেঁধে বানানো সেতু", "ভাসমান পন্টুন সেতু")),
    # Q65 Level 3 layout
    (("66 m girder, piers at 18 m and 48 m, 3 m segments, 22 segments in total", "100 m girder with one pier", "Two piers at 10 m and 20 m with 50 segments", "No piers - the girder floats"),
     ("৬৬ মিটার গার্ডার, ১৮ আর ৪৮ মিটারে স্তম্ভ, ৩ মিটারের খণ্ড, মোট ২২টি খণ্ড", "এক স্তম্ভের ১০০ মিটার গার্ডার", "১০ আর ২০ মিটারে দুই স্তম্ভ, ৫০টি খণ্ড", "স্তম্ভ নেই — গার্ডার ভাসে")),
    # Q66 see-saw meter
    (("The unbalanced moment on the pier, against 7 MN*m plus 6 per tie-down", "The weight of the traveller only", "The river's speed", "The number of segments cast"),
     ("স্তম্ভের উপর অসম ভ্রামক, যার সীমা ৭ মেগানিউটন-মিটার আর প্রতি নোঙর-দড়িতে ৬ বাড়তি", "শুধু ট্র্যাভেলারের ওজন", "নদীর গতি", "ঢালাই করা খণ্ডের সংখ্যা")),
    # Q67 form traveller
    (("A 400 kN frame at the arm's tip: at 18 m its moment alone is 7.2 MN*m", "A worker who travels between piers", "A light frame with no weight", "A truck that tests the bridge"),
     ("বাহুর ডগায় ৪০০ কিলোনিউটনের কাঠামো: ১৮ মিটারে শুধু এর ভ্রামকই ৭.২ মেগানিউটন-মিটার", "স্তম্ভের মধ্যে যাতায়াতকারী কর্মী", "ওজনহীন হালকা কাঠামো", "সেতু পরীক্ষার ট্রাক")),
    # Q68 segment weight
    (("2400 x 9.81 x b x d per metre - deepest, heaviest segments next to the pier", "Every segment weighs exactly the same", "Segments get heavier towards the tip", "Concrete segments weigh nothing in the game"),
     ("প্রতি মিটারে 2400 x 9.81 x b x d — স্তম্ভের পাশের সবচেয়ে গভীর খণ্ডই সবচেয়ে ভারী", "প্রতিটি খণ্ডের ওজন হুবহু এক", "ডগার দিকে খণ্ড ভারী হয়", "খেলায় কংক্রিট-খণ্ডের ওজন নেই")),
    # Q69 alternate sides
    (("Alternating keeps the unbalance to about one segment, while two or three on one side reach the limit", "It is faster for the crane", "Right-side segments are cheaper", "Alternating is only for decoration"),
     ("পালা করে ঢাললে অসমতা প্রায় এক খণ্ডে থাকে, এক দিকে দুই-তিনটে হলেই সীমায় পৌঁছায়", "ক্রেনের জন্য দ্রুত", "ডান দিকের খণ্ড সস্তা", "পালা করা শুধু সাজানোর জন্য")),
    # Q70 last outer segment
    (("The outer arm has 6 segments but the inner only 5, so nothing balances the sixth - add a tie-down first", "It is the lightest segment", "It is cast with steel instead of concrete", "The traveller is removed before it"),
     ("বাইরের বাহুতে ৬টি খণ্ড কিন্তু ভিতরেরটায় ৫টি, তাই ষষ্ঠটার ভারসাম্য নেই — আগে নোঙর-দড়ি দাও", "এটি সবচেয়ে হালকা খণ্ড", "এটি কংক্রিটের বদলে ইস্পাতে ঢালা হয়", "এর আগে ট্র্যাভেলার সরানো হয়")),
    # Q71 tie-downs
    (("Temporary anchor cables adding 6 MN*m each against tipping, for Rs 5 lakh each", "Permanent cables that hold the road up", "Free ropes for workers", "Cables that pull the bridge sideways"),
     ("অস্থায়ী নোঙর-দড়ি, প্রতিটি উল্টে পড়ার বিরুদ্ধে ৬ মেগানিউটন-মিটার যোগ করে, দাম ৫ লাখ টাকা", "রাস্তা ধরে রাখা স্থায়ী কেবল", "কর্মীদের বিনা পয়সার দড়ি", "সেতুকে পাশে টানা কেবল")),
    # Q72 root crack
    (("Cracking at the top of the girder above the pier when hogging stress passes 8 MPa", "A crack in the river bed", "A crack in the road surface at mid-span", "A crack in a tree root near the bank"),
     ("কুঁজো-পীড়ন ৮ মেগাপাসকাল ছাড়ালে স্তম্ভের ঠিক উপরে গার্ডারের মাথায় ফাটল", "নদীর তলায় ফাটল", "মাঝ-বিস্তারে রাস্তায় ফাটল", "পাড়ের কাছে গাছের শিকড়ে ফাটল")),
    # Q73 d_pier choice
    (("Deeper means lower root stress but heavier, costlier segments; 2.5 m cracks, 3.5 m works", "Always choose the slimmest 2.5 m", "Depth has no effect on root stress", "Always choose 6.5 m - it is free"),
     ("গভীর হলে মূলে পীড়ন কম কিন্তু খণ্ড ভারী আর দামি; ২.৫ মিটারে ফাটে, ৩.৫ মিটারে চলে", "সবসময় সবচেয়ে সরু ২.৫ মিটার নাও", "গভীরতায় মূলের পীড়ন বদলায় না", "সবসময় ৬.৫ মিটার — বিনা পয়সায়")),
    # Q74 d_tip
    (("A thinner tip makes the arms lighter but leaves less I at mid-span for the truck", "A thinner tip always earns three stars", "d_tip has no effect after stitching", "d_tip is the depth of the river"),
     ("সরু ডগায় বাহু হালকা হয়, কিন্তু ট্রাকের জন্য মাঝ-বিস্তারে I কম থাকে", "সরু ডগায় সবসময় তিন তারা", "জোড়ার পরে ডগার গভীরতার প্রভাব নেই", "ডগার গভীরতা মানে নদীর গভীরতা")),
    # Q75 haunch shape
    (("A parabola from d_pier at the pier down to d_tip at the end of the longest arm", "A straight line that gets deeper towards the tip", "A constant depth everywhere", "A zig-zag"),
     ("স্তম্ভে d_pier থেকে সবচেয়ে লম্বা বাহুর শেষে d_tip পর্যন্ত একটা অধিবৃত্ত", "ডগার দিকে গভীর হওয়া সরলরেখা", "সব জায়গায় সমান গভীরতা", "আঁকাবাঁকা")),
    # Q76 starting stiffness
    (("I = 4.29 m⁴ at the pier and 1.56 m⁴ at the tip - about 2.7 times stiffer at the pier", "The same I at pier and tip", "The tip is stiffer than the pier", "I = 1.4 m⁴ everywhere"),
     ("স্তম্ভে I = ৪.২৯ মি⁴ আর ডগায় ১.৫৬ মি⁴ — স্তম্ভে প্রায় ২.৭ গুণ দৃঢ়", "স্তম্ভ আর ডগায় একই I", "ডগা স্তম্ভের চেয়ে দৃঢ়", "সব জায়গায় I = ১.৪ মি⁴")),
    # Q77 deepest at the pier
    (("A cantilever's moment and shear are largest at the root, so depth is needed there", "So the girder looks taller from the river", "Because the tips carry the largest moment", "To make casting slower"),
     ("ক্যান্টিলিভারের ভ্রামক আর কৃন্তন মূলে সবচেয়ে বেশি, তাই গভীরতা সেখানেই দরকার", "যাতে নদী থেকে গার্ডার উঁচু দেখায়", "কারণ ডগা সবচেয়ে বেশি ভ্রামক বয়", "ঢালাই ধীর করার জন্য")),
    # Q78 change depths later
    (("No - the depths fix the formwork, so they can only be set before the first segment", "Yes, at any time for free", "Only after stitching", "Only during the truck test"),
     ("না — গভীরতা ছাঁচ ঠিক করে, তাই প্রথম খণ্ডের আগেই শুধু ঠিক করা যায়", "হ্যাঁ, যেকোনো সময় বিনা খরচে", "শুধু জোড়ার পরে", "শুধু ট্রাক-পরীক্ষার সময়")),
    # Q79 stitch and post-tension
    (("Casts the middle closure and stresses tendons, turning two T-halves into one continuous beam", "Paints the bridge", "Removes all the segments", "Opens the bridge to traffic without testing"),
     ("মাঝের জোড় ঢালাই করে টেন্ডন টানে, দুই টি-আকার অর্ধেক মিলে এক টানা বিম হয়", "সেতু রং করে", "সব খণ্ড সরিয়ে দেয়", "পরীক্ষা ছাড়াই সেতু খুলে দেয়")),
    # Q80 post-tensioning
    (("Tendons squeeze the concrete so it takes more pull; light passes the truck test with FS about 1.6", "Heavy is always the best value", "No post-tensioning gives the best FS", "It makes the concrete heavier only"),
     ("টেন্ডন কংক্রিটকে চেপে রাখে, তাই বেশি টান সয়; হালকা টানে প্রায় ১.৬ গুণকে ট্রাক-পরীক্ষা পাস", "ভারী টান সবসময় সেরা", "টান না দিলেই সবচেয়ে ভালো গুণক", "এতে শুধু কংক্রিট ভারী হয়")),
    # Q81 truck test
    (("A 40 t, two-axle truck crosses; bending tension, compression and shear are checked at every position", "Only the truck's speed is measured", "A van drives across once", "The truck stands still at the left bank"),
     ("৪০ টনের দুই-অক্ষের ট্রাক পার হয়; প্রতিটি অবস্থানে বাঁকানো টান, চাপ আর কৃন্তন যাচাই হয়", "শুধু ট্রাকের গতি মাপা হয়", "একটা ভ্যান একবার পার হয়", "ট্রাক বাঁ পাড়ে দাঁড়িয়ে থাকে")),
    # Q82 truck test failed
    (("Add post-tensioning (usually cheapest), or deepen the tip or the haunch", "Make the truck lighter", "Remove the tie-downs", "Paint the girder"),
     ("পোস্ট-টেনশন বাড়াও (সাধারণত সবচেয়ে সস্তা), বা ডগা কিংবা হঞ্চ গভীর করো", "ট্রাক হালকা করো", "নোঙর-দড়ি সরিয়ে দাও", "গার্ডার রং করো")),
    # Q83 worst stress location
    (("Either mid-span (sagging) or over the piers (hogging) - the chart shows which governs", "Always at the abutments", "Always exactly at the truck's front wheel", "Nowhere - stress is even"),
     ("হয় মাঝ-বিস্তারে (ঝোলা) নয়তো স্তম্ভের উপরে (কুঁজো) — চার্ট দেখায় কোনটা নির্ধারক", "সবসময় প্রান্ত-ভরস্থলে", "সবসময় ঠিক ট্রাকের সামনের চাকায়", "কোথাও না — পীড়ন সমান")),
    # Q84 Level 3 costs
    (("Concrete Rs 8/kg, Rs 60,000 labour per segment, tie-downs Rs 5 L, stitch Rs 3 L; par Rs 76 L", "Everything is free except steel", "Each segment costs Rs 1 crore", "Par is Rs 10 crore"),
     ("কংক্রিট কেজিতে ৮ টাকা, প্রতি খণ্ডে ৬০,০০০ টাকা শ্রম, নোঙর-দড়ি ৫ লাখ, জোড় ৩ লাখ; সমমান ৭৬ লাখ", "ইস্পাত ছাড়া সব বিনা পয়সায়", "প্রতিটি খণ্ড ১ কোটি টাকা", "সমমান ১০ কোটি টাকা")),
    # Q85 three-star plan
    (("Starting depths, one tie-down per pier, alternate casts, light post-tensioning: about Rs 75.7 L, FS 1.6", "Heavy post-tensioning and three tie-downs per pier", "No tie-downs and cast one side first", "Thinnest depths and no post-tensioning"),
     ("শুরুর গভীরতা, প্রতি স্তম্ভে এক নোঙর-দড়ি, পালা করে ঢালাই, হালকা টান: প্রায় ৭৫.৭ লাখ, গুণক ১.৬", "ভারী টান আর প্রতি স্তম্ভে তিন নোঙর-দড়ি", "নোঙর-দড়ি ছাড়া আগে এক দিক ঢালো", "সবচেয়ে সরু গভীরতা আর টান ছাড়া")),
    # Q86 why not heavy PT
    (("It costs Rs 6 L more, pushes the total over par and buys strength the truck never needs", "Heavy post-tensioning cracks the concrete", "It is not allowed in Level 3", "It lowers FS below 1"),
     ("এতে ৬ লাখ বেশি খরচ, মোট সমমান ছাড়ায়, আর এমন শক্তি কেনা হয় যা ট্রাকের লাগে না", "ভারী টানে কংক্রিট ফাটে", "লেভেল ৩-এ এটা নিষেধ", "এতে গুণক ১-এর নিচে নামে")),
    # Q87 concrete not steel
    (("Concrete is very cheap and strong when squeezed, and tendons fix its weakness in tension", "Steel is not available in Level 3", "Concrete is lighter than steel", "Concrete is strongest when pulled"),
     ("কংক্রিট খুব সস্তা আর চাপে শক্ত, আর টেন্ডন টানে তার দুর্বলতা সারায়", "লেভেল ৩-এ ইস্পাত পাওয়া যায় না", "কংক্রিট ইস্পাতের চেয়ে হালকা", "টানে কংক্রিট সবচেয়ে শক্ত")),
    # Q88 moment diagram flip
    (("Before: the whole girder hogs; after: hogging stays over piers but sagging appears at mid-span", "Nothing changes", "All moments become zero", "The girder only sags everywhere before stitching"),
     ("আগে: পুরো গার্ডার কুঁজো; পরে: স্তম্ভের উপরে কুঁজো থাকে কিন্তু মাঝ-বিস্তারে ঝোলা দেখা দেয়", "কিছুই বদলায় না", "সব ভ্রামক শূন্য হয়", "জোড়ার আগে গার্ডার সব জায়গায় শুধু ঝোলে")),
    # Q89 undo
    (("Removes the last segment before stitching; after stitching it un-stitches the middle", "Deletes the whole level", "Undoes the truck test result only", "Changes the river level"),
     ("জোড়ার আগে শেষ খণ্ড সরায়; জোড়ার পরে মাঝের জোড় খুলে দেয়", "পুরো লেভেল মুছে দেয়", "শুধু ট্রাক-পরীক্ষার ফল ফেরায়", "নদীর জলস্তর বদলায়")),
    # Q90 outer arm lands
    (("It props the pier, so the pier can no longer tip - only root stress is checked after that", "The pier must be rebuilt", "The see-saw limit halves", "The traveller falls off"),
     ("এটি স্তম্ভকে ঠেকা দেয়, তাই আর উল্টাতে পারে না — এরপর শুধু মূলের পীড়ন যাচাই হয়", "স্তম্ভ আবার বানাতে হয়", "ঢেঁকির সীমা অর্ধেক হয়", "ট্র্যাভেলার পড়ে যায়")),
    # Q91 alternate route
    (("A steel launch girder finishes the span for 0.7 x the failed cost, with one star and 30 EXP", "A free helicopter lift with three stars", "Skipping the level with no reward", "Building a tunnel instead"),
     ("ইস্পাতের লঞ্চ-গার্ডার ব্যর্থ খরচের ০.৭ গুণে বিস্তার শেষ করে, এক তারা আর ৩০ অভিজ্ঞতা দেয়", "বিনা পয়সায় হেলিকপ্টার আর তিন তারা", "পুরস্কার ছাড়া লেভেল বাদ দেওয়া", "বদলে সুড়ঙ্গ বানানো")),
    # Q92 truss deck pieces bend?
    (("No - every member is pin-jointed and only carries a pull or push along its length", "Yes, they bend like Level 3 girders", "Only in the 3D view", "Only when it rains"),
     ("না — প্রতিটি সদস্য পিন-জোড়ে বাঁধা, শুধু দৈর্ঘ্য বরাবর টান বা ঠেলা বয়", "হ্যাঁ, লেভেল ৩-এর গার্ডারের মতো বাঁকে", "শুধু 3D দৃশ্যে", "শুধু বৃষ্টিতে")),
    # Q93 buckling and bending
    (("Buckling is bending caused by compression, resisted by the same stiffness EI", "Buckling only happens in tension", "They have nothing in common", "Bending only happens in cables"),
     ("বক্রন হল চাপ থেকে হওয়া বাঁকা, যা একই দৃঢ়তা EI রোখে", "বক্রন শুধু টানে হয়", "এদের মধ্যে কোনো মিল নেই", "বাঁকা শুধু কেবলে হয়")),
    # Q94 K factor
    (("It describes end fixity: pinned K = 1, both fixed K = 0.5 (4x stronger), one free K = 2", "K is the cost per kilogram", "K is always 10", "K is the number of joints"),
     ("প্রান্ত কীভাবে আটকানো তা বোঝায়: পিন K = 1, দুই প্রান্ত আটকানো K = 0.5 (৪ গুণ শক্ত), এক প্রান্ত মুক্ত K = 2", "K হল কেজিপ্রতি দাম", "K সবসময় ১০", "K হল জোড়ের সংখ্যা")),
    # Q95 towers
    (("Towers are long, heavily pushed members - use a hollow box, brace them and balance the cable pulls", "Towers carry no force", "Towers should be made of cable", "Towers only need to be painted"),
     ("টাওয়ার লম্বা, প্রবল চাপ-খাওয়া সদস্য — ফাঁপা বাক্স ব্যবহার করো, ঠেকনা দাও আর কেবলের টান সমান রাখো", "টাওয়ার কোনো বল বয় না", "টাওয়ার কেবল দিয়ে বানানো উচিত", "টাওয়ারে শুধু রং লাগে")),
    # Q96 slim tips
    (("Self-weight near the tip has the longest lever arm, so slim tips cut the root moment", "Slim tips look more modern", "Tips carry the most traffic", "Thick tips are not allowed"),
     ("ডগার কাছের নিজ-ওজনের লিভার-বাহু সবচেয়ে লম্বা, তাই সরু ডগা মূলের ভ্রামক কমায়", "সরু ডগা বেশি আধুনিক দেখায়", "ডগা সবচেয়ে বেশি যান বয়", "মোটা ডগা নিষিদ্ধ")),
    # Q97 dead and live load
    (("Dead load is the permanent weight of the structure; live load is traffic that comes and goes", "Dead load is broken parts; live load is new parts", "Both mean the weight of the workers", "Live load is only wind"),
     ("স্থির ভার কাঠামোর স্থায়ী ওজন; চলমান ভার আসা-যাওয়া করা যানবাহন", "স্থির ভার ভাঙা অংশ; চলমান ভার নতুন অংশ", "দুটোরই মানে কর্মীদের ওজন", "চলমান ভার শুধু বাতাস")),
    # Q98 three numbers
    (("Pier balance against capacity, root stress against 8 MPa, and the truck-test ratio after stitching", "Price, colour and speed", "Number of workers, trucks and cranes", "River depth, wind and rain"),
     ("ক্ষমতার তুলনায় স্তম্ভের ভারসাম্য, ৮ মেগাপাসকালের তুলনায় মূলের পীড়ন, আর জোড়ার পরে ট্রাক-পরীক্ষার অনুপাত", "দাম, রং আর গতি", "কর্মী, ট্রাক আর ক্রেনের সংখ্যা", "নদীর গভীরতা, বাতাস আর বৃষ্টি")),
    # Q99 8 MPa vs 3 MPa
    (("Cantilever tendons pre-compress the root during building; afterwards the concrete relies on its own 3 MPa plus post-tensioning", "Concrete gets weaker with age", "It is a mistake in the game", "Trucks are lighter than segments"),
     ("নির্মাণকালে ক্যান্টিলিভার-টেন্ডন মূলকে আগে থেকে চেপে রাখে; পরে কংক্রিট নিজের ৩ মেগাপাসকাল আর পোস্ট-টেনশনের উপর নির্ভর করে", "বয়সে কংক্রিট দুর্বল হয়", "এটা খেলার ভুল", "ট্রাক খণ্ডের চেয়ে হালকা")),
    # Q100 one sentence
    (("Starting depths, one tie-down per pier, alternate every cast, stitch with light post-tensioning", "Deepest haunch, heavy post-tensioning, no tie-downs", "Cast all left segments first, then the right", "Skip the stitch and run the truck"),
     ("শুরুর গভীরতা, প্রতি স্তম্ভে এক নোঙর-দড়ি, প্রতিবার পালা করে ঢালাই, হালকা টানে জোড়া", "সবচেয়ে গভীর হঞ্চ, ভারী টান, নোঙর-দড়ি ছাড়া", "আগে সব বাঁ খণ্ড, তারপর ডান", "জোড় বাদ দিয়ে ট্রাক চালাও")),
)

assert len(_OPTS) == len(BEAMS) == 50

ITEMS = tuple(mcq(it.q_en, en, 0, it.a_en, it.q_bn, bn, it.a_bn) for it, (en, bn) in zip(BEAMS, _OPTS))
