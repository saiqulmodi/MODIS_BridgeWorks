"""বাংলা: paid demonstration screens (merged into lang_bn)."""
import re

DEMO_BN = {
    "Demo": "ডেমো",
    "Watch a working solution (costs part of this level's budget).": "একটি কার্যকর সমাধান দেখো (এই লেভেলের বাজেটের একটু অংশ খরচ হয়)।",
    "WATCH A DEMONSTRATION?": "একটি প্রদর্শনী দেখবে?",
    "A demonstration shows one design that solves this level.": "প্রদর্শনী এমন একটি নকশা দেখায় যা এই লেভেল সমাধান করে।",
    "After paying, you can replay the demonstration for free. A demonstration earns no stars or EXP.":
        "টাকা দেওয়ার পর প্রদর্শনী বিনামূল্যে আবার দেখতে পারবে। প্রদর্শনী থেকে কোনো তারা বা EXP পাওয়া যায় না।",
    "No, keep my budget": "না, আমার বাজেট রাখো",
    "DEMONSTRATION": "প্রদর্শনী", "DEMONSTRATION FINISHED": "প্রদর্শনী শেষ",
    "Back to my design": "আমার নকশায় ফেরো", "Start from this design": "এই নকশা থেকে শুরু করো",
    "Demonstrations earn no stars or EXP - now build your own version and try to beat its cost!":
        "প্রদর্শনী থেকে কোনো তারা বা EXP পাওয়া যায় না - এবার নিজের সংস্করণ বানাও আর এর খরচকে হারানোর চেষ্টা করো!",
    "Demonstration already paid for - replaying free": "প্রদর্শনীর দাম আগেই দেওয়া হয়েছে - বিনামূল্যে আবার দেখাচ্ছি",
    # why each demonstration works
    "A light timber Warren truss: two big triangles of hollow-box timber. Hollow boxes resist buckling, and triangles cannot fold.":
        "হালকা কাঠের ওয়ারেন ট্রাস: ফাঁপা-বাক্স কাঠের দুটি বড় ত্রিভুজ। ফাঁপা বাক্স বেঁকে যাওয়া ঠেকায়, আর ত্রিভুজ ভাঁজ হতে পারে না।",
    "The diesel shunter with only 2 wagons stays under its grip limit on the hill, so it makes two quick trips instead of stalling with four wagons.":
        "মাত্র 2টি ওয়াগনসহ ডিজেল শান্টার পাহাড়ে তার আঁকড়ে ধরার সীমার নিচে থাকে, তাই চারটি ওয়াগন নিয়ে আটকে না গিয়ে দুটি দ্রুত ট্রিপ দেয়।",
    "Slim haunch, tie-downs on both piers, segments cast left-right in turn, light post-tensioning after the stitch.":
        "সরু হঞ্চ, দুই স্তম্ভে বাঁধন-তার, পালা করে বাঁয়ে-ডানে অংশ ঢালাই, জোড়ার পরে হালকা পোস্ট-টেনশনিং।",
    "One mainline diesel with 5 wagons (two trips), braking 80 m before the stop line so the wet descent still leaves enough stopping distance.":
        "5টি ওয়াগনসহ একটি মেইনলাইন ডিজেল (দুই ট্রিপ), থামার দাগের 80 m আগে ব্রেক, যাতে ভেজা ঢালেও থামার যথেষ্ট দূরত্ব থাকে।",
    "A distant signal 400 m out on each side, the bridge locked to one direction at a time, the switch following CARGO_AT_JE and the barrier triggered by XING_APPR.":
        "দুই পাশে 400 m দূরে একটি করে আগাম সিগন্যাল, সেতু একবারে এক দিকেই তালাবদ্ধ, পয়েন্ট CARGO_AT_JE মেনে চলে, আর গেট নামে XING_APPR দিয়ে।",
    "A roundabout: cars merge in turn, so nobody waits for a red light and the queue never reaches the city edge.":
        "গোলচত্বর: গাড়ি পালা করে মেশে, তাই কেউ লাল বাতির জন্য অপেক্ষা করে না আর লাইন কখনো শহরের সীমানা পর্যন্ত পৌঁছায় না।",
    "A deep steel Warren truss with aerodynamic fairings: the fairings weaken the vortices so the swing never builds up when the wind matches f_n.":
        "বাতাস-কাটা ফেয়ারিংসহ গভীর ইস্পাতের ওয়ারেন ট্রাস: ফেয়ারিং ঘূর্ণি দুর্বল করে, তাই বাতাস f_n-এর সমান হলেও দোলন বাড়ে না।",
    "Slender braced piers on isolation bearings plus flexible joints: forces drop to C = 0.5 and the joints leave room for the bigger movement.":
        "আইসোলেশন বিয়ারিংয়ের উপর সরু বন্ধনী-দেওয়া স্তম্ভ আর নমনীয় জোড়: বল কমে C = 0.5 হয়, আর জোড় বড় নড়াচড়ার জায়গা দেয়।",
    "5000 t by rail (one 30-wagon train, under the grip limit) and 1000 t by barge: cheap, safe and inside 24 hours.":
        "রেলে 5000 t (30 ওয়াগনের একটি ট্রেন, আঁকড়ে ধরার সীমার নিচে) আর বার্জে 1000 t: সস্তা, নিরাপদ আর 24 ঘণ্টার মধ্যে।",
    "A steel deck truss propped by V-piers on both rock islands, with enough grid power for the maglev pod to cross in time.":
        "দুই পাথুরে দ্বীপে V-স্তম্ভের উপর ভর দেওয়া ইস্পাতের ডেক ট্রাস, আর ম্যাগলেভ পড সময়মতো পার হওয়ার মতো যথেষ্ট গ্রিড বিদ্যুৎ।",
}

DEMO_PATTERNS = [
    (r"Yes, pay (Rs .+)", r"হ্যাঁ, \1 দাও"),
    (r"It costs (Rs .+) \((\d+)% of this level's budget\)\.", r"এর দাম \1 (এই লেভেলের বাজেটের \2%)।"),
    (r"WARNING: your total budget for this level will drop from (Rs .+?) to (Rs .+?)\. This cannot be undone\.",
     r"সতর্কতা: এই লেভেলে তোমার মোট বাজেট \1 থেকে কমে \2 হয়ে যাবে। এটি আর ফেরানো যাবে না।"),
]
