"""Donation Camps: players and students give part of their Civil Grants to nation-building
causes - a school footbridge, a flood shelter, a road to the market - and watch each
camp's collection grow towards its target.

Everything here is in-game money (Civil Grants earned in the BridgeWorks Academy). No real
money is collected anywhere in the game. REAL_DONATIONS_ENABLED is the hook for a later
version: real gifts must go through a registered charity's own verified payment page (never
card or bank details typed into the game), with a parent's consent for children.
"""
from dataclasses import dataclass

REAL_DONATIONS_ENABLED = False       # flip only with a registered charity partner, see above
GIVE_STEPS = (500.0, 1000.0, 5000.0)
EXP_PER_1000 = 5                     # EXP for every Rs 1,000 given
EXP_CAMP_COMPLETE = 100              # EXP when your gifts complete a camp


@dataclass(frozen=True)
class Camp:
    key: str
    name_en: str
    name_bn: str
    cause_en: str
    cause_bn: str
    target: float            # Civil Grants needed to complete the camp, Rs
    badge_en: str
    badge_bn: str

    def name(self, lang):
        return self.name_bn if lang == "bn" else self.name_en

    def cause(self, lang):
        return self.cause_bn if lang == "bn" else self.cause_en

    def badge(self, lang):
        return self.badge_bn if lang == "bn" else self.badge_en


CAMPS = (
    Camp("school_bridge", "Village school footbridge", "গ্রামের স্কুলের হাঁটার সেতু",
         "Children in Char Kalia wade across a stream to school every monsoon. A small steel "
         "truss footbridge keeps them dry and safe all year.",
         "চর কালিয়ার শিশুরা প্রতি বর্ষায় নালা হেঁটে পেরিয়ে স্কুলে যায়। একটা ছোট ইস্পাতের ট্রাস "
         "হাঁটার সেতু সারা বছর তাদের শুকনো আর নিরাপদ রাখবে।",
         20000.0, "School Bridge Builder", "স্কুল-সেতু নির্মাতা"),
    Camp("flood_shelter", "Flood shelter on stilts", "খুঁটির উপর বন্যা-আশ্রয়",
         "A raised concrete shelter where 300 families and their cattle can wait out a flood. "
         "Its columns are braced like a viaduct so the water cannot push it over.",
         "উঁচু কংক্রিটের আশ্রয়, যেখানে 300টি পরিবার আর তাদের গবাদি পশু বন্যা কাটাতে পারবে। এর "
         "স্তম্ভগুলো উঁচু সেতুর মতো ঠেকনা দেওয়া, যাতে জলের ঠেলায় উল্টে না যায়।",
         50000.0, "Flood Guardian", "বন্যা-রক্ষী"),
    Camp("market_road", "Road to the market", "বাজারে যাওয়ার রাস্তা",
         "Farmers carry vegetables 12 km on foot. An all-weather road and a culvert bridge let "
         "a truck reach the town market in 20 minutes, so food arrives fresh.",
         "চাষিরা 12 km পায়ে হেঁটে সবজি বয়ে নেন। সব ঋতুর রাস্তা আর একটা কালভার্ট সেতু হলে ট্রাক "
         "20 মিনিটে শহরের বাজারে পৌঁছাবে, খাবার টাটকা থাকবে।",
         40000.0, "Market Maker", "বাজার-গড়িয়ে"),
    Camp("water_pipe", "Clean water pipe bridge", "বিশুদ্ধ জলের পাইপ-সেতু",
         "A light cable-stayed pipe bridge carries clean drinking water across the river to a "
         "village of 2,000 people.",
         "একটা হালকা তার-ঝোলানো পাইপ-সেতু নদী পেরিয়ে 2,000 মানুষের গ্রামে বিশুদ্ধ খাবার জল "
         "পৌঁছে দেবে।",
         30000.0, "Water Hero", "জল-নায়ক"),
    Camp("girls_engineering", "Scholarships for future engineers", "ভবিষ্যৎ প্রকৌশলীদের বৃত্তি",
         "Pays for books, a laptop and travel so that bright students from poor families - "
         "especially girls - can study engineering.",
         "বই, ল্যাপটপ আর যাতায়াতের খরচ, যাতে দরিদ্র পরিবারের মেধাবী শিক্ষার্থীরা - বিশেষ করে "
         "মেয়েরা - প্রকৌশল পড়তে পারে।",
         60000.0, "Opportunity Maker", "সুযোগ-সৃষ্টিকারী"),
    Camp("relief_bridge", "Emergency relief bridge kit", "জরুরি ত্রাণ-সেতুর কিট",
         "A ready-to-bolt steel panel bridge stored for disasters. When a flood or quake breaks "
         "a road, it can be put up in two days to bring help through.",
         "দুর্যোগের জন্য রাখা জোড়া-লাগানোর-জন্য-তৈরি ইস্পাতের প্যানেল-সেতু। বন্যা বা ভূমিকম্পে "
         "রাস্তা ভাঙলে দুই দিনে বসিয়ে সাহায্য পৌঁছানো যায়।",
         80000.0, "First Responder", "প্রথম উদ্ধারকারী"),
    Camp("riverbank_trees", "Trees for the riverbanks", "নদীর পাড়ে গাছ",
         "5,000 saplings whose roots hold the riverbanks together, protecting bridge "
         "foundations and farms from erosion.",
         "5,000টি চারাগাছ, যাদের শিকড় নদীর পাড় ধরে রাখবে, সেতুর ভিত আর খেত-খামারকে ভাঙন থেকে "
         "বাঁচাবে।",
         15000.0, "Green Engineer", "সবুজ প্রকৌশলী"),
    Camp("library_boat", "Floating library boat", "ভাসমান লাইব্রেরি-নৌকা",
         "A boat full of books and a solar-powered classroom that visits river islands with no "
         "school nearby.",
         "বই আর সৌরশক্তির ক্লাসরুমে ভরা একটা নৌকা, যা কাছে স্কুল নেই এমন নদীর চরে যায়।",
         25000.0, "Knowledge Carrier", "জ্ঞান-বাহক"),
)

# Giver titles by total Civil Grants given
TITLES = ((0.0, "Friend of the Nation", "দেশের বন্ধু"),
          (5000.0, "Community Builder", "সমাজ-গড়িয়ে"),
          (25000.0, "Citizen Engineer", "নাগরিক প্রকৌশলী"),
          (100000.0, "Nation Builder", "দেশ-গড়িয়ে"))


def camp(key):
    return next(c for c in CAMPS if c.key == key)


def title(total_given, lang):
    t = TITLES[0]
    for row in TITLES:
        if total_given >= row[0]:
            t = row
    return t[2] if lang == "bn" else t[1]
