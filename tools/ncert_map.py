"""NCERT chapter map for the question banks (used by tools/export_web.py).

Every question of Class 1-12 is filed under a chapter of ITS OWN class's NCERT book, or it is not filed as NCERT at all.
NIT = JEE Main and IIT = JEE Advanced use the Class 11 + 12 chapters of Physics, Chemistry and Maths (the JEE syllabus).
BE and Expert have no NCERT book, so they keep their own subjects with no chapters.

How a question is matched:
  - School bank questions carry a topic: only the topic is tested, so a sum dressed up as biology ("a seedling grows
    2 cm a week") stays out of the Biology chapters.
  - Other questions have no topic: the question and explanation text are tested.
Questions that match no chapter are kept, under a separate "not NCERT" subject chip.
"""
import re


def _ch(*pairs):
    return [(name, re.compile(rx)) for name, rx in pairs]


EVS = _ch(
    ("Family and Friends: People", r"family|people who help|helpers?\b|festival|games? we play|games:|kabaddi|dances?|arts and crafts|famous indians|armed forces|monuments?|national symbols|stories from|walls tell|farmers, forests|up you go|mountaineer|like father|inherited"),
    ("Family and Friends: Animals", r"animal|birds?\b|insects?|honeybee|snakes?|super senses|sounds|young ones|\bpets?\b|\bwild\b|butterfl"),
    ("Family and Friends: Plants", r"plants?\b|trees?\b|roots? of|seeds?\b|germinat|leaves|leaf\b|flowers?\b|forests?\b"),
    ("Food", r"food|fruits?|vegetable|spices?|tasting|digest|mangoes|nutrient|cooking|hygiene|good habits|my body|sense organs|bones|teeth"),
    ("Shelter", r"\bhouses?\b|shelter|ladakh|neighbourhood|igloo|\btents?\b|\bhuts?\b"),
    ("Water", r"water|\brain|every drop|\brivers?\b|\bponds?\b|float|\bsink"),
    ("Travel", r"transport|train|journey|communication|travel|maps?\b|directions?|sun, moon|earth from space|the earth|seasons?|weather|rainbow|natural resources|pollution|fuels?"),
    ("Things We Make and Do", r"materials?|groups of|tools?\b|made of|natural and man-made|clay|paper\b|cloth"),
)

MATH_1_5 = {
    1: _ch(("Shapes and Space", r"shape|circle|square|triangle|rectangle"), ("Numbers", r"comparing|before, after|between|number name|place value|ordinal|numbers?\b|count"),
           ("Addition", r"addition|\badd\b|plus"), ("Subtraction", r"subtract|minus|word problems"), ("Time", r"days, months|time\b|clock|o'clock"),
           ("Measurement", r"measure|length|longer|heavier|taller"), ("Patterns", r"pattern|skip"), ("Money", r"money|coin|note|rupee")),
    2: _ch(("What is Long, What is Round?", r"shape|circle|square|triangle"), ("Counting in Groups", r"skip|pattern|even and odd"), ("How Much Can You Carry?", r"weight|heavier"),
           ("Counting in Tens", r"comparing|before, after|between|number name|place value|ordinal|numbers?\b"), ("Add Our Points / Give and Take", r"addition|subtract|word problems"),
           ("Long and Short", r"length|measure"), ("Birds Come, Birds Go (Tables)", r"multiplication|tables?\b"), ("Lines and Lines", r"\blines?\b"), ("Tens and Ones", r"tens and ones"),
           ("My Funday (Time)", r"days, months|time\b|clock"), ("Rupees and Paise", r"money|coin|rupee"), ("Sharing", r"sharing|division")),
    3: _ch(("Shapes and Designs", r"shape|design"), ("Fun with Numbers", r"number name|place value|large numbers"), ("Give and Take", r"addition|subtraction"),
           ("Long and Short", r"length|perimeter"), ("Time Goes On", r"time\b|clock|calendar"), ("Who is Heavier?", r"weight|heavier|measurement"), ("How Many Times?", r"multiplication|tables?\b"),
           ("Can We Share?", r"sharing|division"), ("Rupees and Paise", r"money|rupees|paise|buying|change\b"), ("Jugs and Mugs", r"capacity|litre"), ("Play with Patterns", r"pattern")),
    4: _ch(("Long and Short", r"\blength|\bmetres?\b"), ("Tick-Tick-Tick", r"time\b|clock"), ("The Junk Seller", r"money|buying|rupees|paise|decimal"), ("Halves and Quarters", r"fraction|half|quarter"),
           ("Tables and Shares", r"multiplication|division|multipl|factors? and"), ("Fields and Fences", r"perimeter|area"), ("Carts and Wheels", r"circle|radius|centre"), ("Play with Patterns", r"pattern"),
           ("How Heavy? How Light?", r"weight|gram\b|kilogram"), ("Jugs and Mugs", r"capacity|litre"), ("Building with Bricks", r"addition and subtraction of large|large numbers")),
    5: _ch(("Shapes and Angles", r"angle"), ("Parts and Wholes", r"fraction"), ("Be My Multiple, I'll Be Your Factor", r"factor|hcf|lcm|multiple|prime"), ("Tenths and Hundredths", r"decimal"),
           ("Area and its Boundary", r"\barea\b|perimeter"), ("Ways to Multiply and Divide", r"multiplication|division|unitary|bills"), ("How Big? How Heavy?", r"volume|cuboid"),
           ("The Fish Tale", r"large numbers|place value|money|buying|profit"), ("Can You See the Pattern?", r"pattern"), ("Smart Charts", r"chart|graph|data")),
}

CH = {
    1: {"evs": EVS, "math": MATH_1_5[1]}, 2: {"evs": EVS, "math": MATH_1_5[2]}, 3: {"evs": EVS, "math": MATH_1_5[3]},
    4: {"evs": EVS, "math": MATH_1_5[4]}, 5: {"evs": EVS, "math": MATH_1_5[5]},
    6: {
        "math": _ch(("Knowing Our Numbers", r"large numbers|place value|roman"), ("Playing with Numbers", r"hcf|lcm|prime|factor|multiple|divisib"), ("Integers", r"integer"), ("Fractions", r"fraction"),
                    ("Decimals", r"decimal"), ("Data Handling", r"average|mean\b|data|bar graph"), ("Mensuration", r"\barea\b|perimeter|volume"), ("Algebra", r"equation|algebra|variable"),
                    ("Ratio and Proportion", r"ratio|proportion|unitary"), ("Understanding Elementary Shapes", r"angle|triangle")),
        "physics": _ch(("Motion and Measurement of Distances", r"measure|unit conversion|si unit|instrument|ruler|motion"), ("Light, Shadows and Reflections", r"light|shadow|reflect|mirror|opaque|transparent"),
                       ("Electricity and Circuits", r"electric|circuit|conductor|insulator|battery|bulb"), ("Fun with Magnets", r"magnet|compass|pole")),
        "chemistry": _ch(("Fibre to Fabric", r"fibre|fabric|cotton|jute|yarn"), ("Sorting Materials into Groups", r"sorting|solubil|lustre|materials"), ("Separation of Substances", r"separation|filtrat|sieving|evaporat|decant|winnow|solutions and dissolving"),
                         ("Changes Around Us", r"physical and chemical changes|changes?\b|reversible"), ("Air Around Us", r"\bair\b|oxygen|nitrogen|atmosphere"), ("Water", r"\bwater\b|water cycle")),
        "biology": _ch(("Components of Food", r"components of food|nutrient|vitamin|protein|carbohydrate|deficien|balanced diet"), ("Food: Where Does It Come From?", r"food|herbivore|carnivore|omnivore"),
                       ("Getting to Know Plants", r"getting to know plants|flowers and pollination|\bplants?\b|leaf|leaves|root|stem|flower|petal"), ("Body Movements", r"body movements|bone|joint|skeleton|muscle|gait"),
                       ("Living Organisms and Their Surroundings", r"living organisms|habitat|adaptation|surroundings")),
        "geography": _ch(("The Earth in Our Solar System", r"solar system|planet|stars?\b"), ("Globe: Latitudes and Longitudes", r"latitude|longitude|globe|time and"), ("Maps", r"maps?\b|scale"),
                         ("Major Domains of the Earth", r"continents|oceans?\b|biosphere"), ("Major Landforms of the Earth", r"mountains|landform|plateau|plains?\b|deserts"), ("Our Country: India", r"india: physical|neighbours of india|states and capitals|india")),
    },
    7: {
        "math": _ch(("Integers", r"integer"), ("Fractions and Decimals", r"fraction|decimal"), ("Data Handling", r"average|mean|median|mode\b|data"), ("Simple Equations", r"equation"),
                    ("The Triangle and its Properties", r"triangle|pythagoras"), ("Comparing Quantities", r"percent|profit|interest|ratio|proportion|unitary|discount|gst|shopping|banking"),
                    ("Rational Numbers", r"rational"), ("Perimeter and Area", r"\barea\b|perimeter|circumference|circle"), ("Exponents and Powers", r"exponent|power"), ("Algebraic Expressions", r"algebraic")),
        "physics": _ch(("Heat", r"temperature|heat|thermometer|celsius|fahrenheit|kelvin|conduct"), ("Motion and Time", r"speed|distance and time|motion|measur|pendulum"), ("Electric Current and its Effects", r"electric|fuse|circuit"),
                       ("Light", r"light|mirror|lens|reflect")),
        "chemistry": _ch(("Fibre to Fabric", r"fibre|wool|silk"), ("Acids, Bases and Salts", r"acid|base|salts|indicator|litmus|neutrali"), ("Physical and Chemical Changes", r"physical and chemical|rusting|crystalli|changes"),
                         ("Water: A Precious Resource / Wastewater Story", r"water|sewage")),
        "biology": _ch(("Nutrition in Plants", r"nutrition in plants|photosynth|parasit|chlorophyll"), ("Nutrition in Animals", r"nutrition in animals|ruminant|amoeba|digest"), ("Weather, Climate and Adaptations", r"weather, climate|adaptation|polar|rainforest"),
                       ("Respiration in Organisms", r"respiration|breathing rate|anaerobic"), ("Transportation in Animals and Plants", r"transportation|excretion|blood|heart\b|xylem|phloem|kidney"), ("Reproduction in Plants", r"reproduction in plants|flowers and pollination|pollinat|seed dispersal|vegetative"),
                       ("Forests: Our Lifeline", r"forests?\b")),
        "geography": _ch(("Inside Our Earth / Air", r"interior of the earth|atmosphere|temperature and altitude|lapse"), ("Our Changing Earth", r"landforms|erosion"), ("Natural Vegetation and Wildlife", r"natural vegetation|wildlife"),
                         ("Life in the Deserts / Temperate Grasslands", r"deserts|grassland|mountains")),
    },
    8: {
        "math": _ch(("Rational Numbers", r"rational"), ("Linear Equations in One Variable", r"equation"), ("Data Handling", r"probability|mean|median|mode\b|data"), ("Squares and Square Roots", r"square"), ("Cubes and Cube Roots", r"cube root|cubes and"),
                    ("Comparing Quantities", r"interest|profit|discount|gst|shopping|banking|percent"), ("Algebraic Expressions and Identities", r"algebraic|identit"), ("Mensuration", r"surface area|volume|cylinder"), ("Exponents and Powers", r"exponent|power"),
                    ("Direct and Inverse Proportions", r"proportion"), ("Factorisation", r"factoris")),
        "physics": _ch(("Force and Pressure", r"force|pressure"), ("Friction", r"friction|lubric"), ("Sound", r"sound|vibrat|pitch|decibel"), ("Light", r"light|eye\b|reflection"), ("Stars and the Solar System", r"star|planet|solar")),
        "chemistry": _ch(("Synthetic Fibres and Plastics", r"synthetic|plastic|nylon|polyester|rayon"), ("Materials: Metals and Non-Metals", r"metals|displacement|reactivity|oxide"), ("Coal and Petroleum", r"coal|petroleum|kerosene"),
                         ("Combustion and Flame", r"combustion|fuels?|flame|calorific"), ("Chemical Effects of Electric Current", r"chemical effects|electroplat|electrolysis")),
        "biology": _ch(("Crop Production and Management", r"crop|kharif|rabi|irrigat|fertili"), ("Microorganisms: Friend and Foe", r"microorganism|bacteria|virus|fungi|microbe"), ("Conservation of Plants and Animals", r"conservation|deforest|endemic|sanctuar"),
                       ("Cell: Structure and Functions", r"\bcell\b|nucleus|chloroplast"), ("Reproduction in Animals", r"reproduction in animals|fertilis|embryo|metamorphosis"), ("Reaching the Age of Adolescence", r"adolescence|puberty|hormone")),
        "geography": _ch(("Resources", r"resources|soils?\b|minerals?|agriculture"), ("Land, Soil, Water, Vegetation and Wildlife", r"natural vegetation|landforms|wildlife"), ("Human Resources", r"population|density|sex ratio")),
    },
    9: {
        "math": _ch(("Number Systems", r"number system|irrational|rational"), ("Polynomials", r"polynomial|algebraic identit|identit"), ("Coordinate Geometry", r"coordinate"), ("Linear Equations in Two Variables", r"linear equation"),
                    ("Triangles and Lines", r"triangle|pythagoras|angle|parallel"), ("Quadrilaterals and Circles", r"quadrilateral|parallelogram|circle"), ("Heron's Formula", r"heron"), ("Surface Areas and Volumes", r"surface area|volume"), ("Statistics", r"statistic|mean|median|mode\b"), ("Probability", r"probabil")),
        "physics": _ch(("Motion", r"equations of motion|speed|velocity|acceleration|motion"), ("Force and Laws of Motion", r"newton|momentum|force|inertia"), ("Gravitation", r"gravit|density|pressure|buoyan|upthrust|archimedes|weight of|weighs"), ("Work and Energy", r"work, energy|work\b|energy|power"), ("Sound", r"sound|echo|wavelength")),
        "chemistry": _ch(("Matter in Our Surroundings", r"matter and|states|evaporat|melting|boiling"), ("Is Matter Around Us Pure?", r"concentration|solution|mixture|pure|colloid"), ("Atoms and Molecules", r"mole concept|atoms, molecules|molecular mass|formula|avogadro|\bmoles?\b"), ("Structure of the Atom", r"structure of the atom|electron|proton|neutron|isotope|valency")),
        "biology": _ch(("The Fundamental Unit of Life", r"\bcell\b|cell:|cell division|mitochond|nucleus"), ("Tissues", r"tissue|xylem|phloem|epithel"), ("Diversity in Living Organisms", r"diversity|phylum|kingdom|classif"), ("Why Do We Fall Ill?", r"fall ill|disease|immun|vaccin|infect"), ("Improvement in Food Resources", r"food resources|crop|manure|fertili|poultry|fisher")),
        "geography": _ch(("India: Size and Location", r"size and location|latitude"), ("Physical Features of India", r"physical features|himalaya|plateau"), ("Drainage", r"rivers?|drainage"), ("Climate", r"climate|monsoon|temperature|winds"), ("Natural Vegetation and Wildlife", r"natural vegetation|wildlife"), ("Population", r"population|density|sex ratio")),
        "economics": _ch(("People as Resource", r"human capital|education|people as|unemploy"), ("Poverty as a Challenge", r"poverty"), ("Food Security in India", r"food security|buffer|ration"), ("The Story of Village Palampur", r"palampur|factors of production")),
    },
    10: {
        "math": _ch(("Real Numbers", r"real numbers|hcf|lcm|irrational"), ("Polynomials", r"polynomial"), ("Pair of Linear Equations", r"pair of linear|linear equation"), ("Quadratic Equations", r"quadratic"), ("Arithmetic Progressions", r"arithmetic progression|\bap\b"),
                    ("Triangles", r"similar|triangle"), ("Coordinate Geometry", r"coordinate"), ("Introduction to Trigonometry", r"trigonometric|sin\b|cos\b|tan\b"), ("Some Applications of Trigonometry", r"heights and distances|angle of elevation"), ("Circles", r"tangent"), ("Areas Related to Circles", r"areas related|sector"), ("Surface Areas and Volumes", r"surface area|volume"), ("Statistics", r"statistic|mean|median|mode\b"), ("Probability", r"probabil")),
        "physics": _ch(("Light: Reflection and Refraction", r"mirror|lens|refract|reflect"), ("The Human Eye and the Colourful World", r"human eye|myopia|hypermetropia|prism|dispersion"), ("Electricity", r"ohm|resist|electric power|electric|current|voltage"), ("Magnetic Effects of Electric Current", r"magnetic|solenoid|motor"), ("Sources of Energy", r"sources of energy|solar|biogas|nuclear energy")),
        "chemistry": _ch(("Chemical Reactions and Equations", r"chemical reactions|balanc|displacement|redox|tests? for gases"), ("Acids, Bases and Salts", r"acid|base|salts?|\bph\b"), ("Metals and Non-metals", r"metals|reactivity|extraction|corrosion|ionic"), ("Carbon and its Compounds", r"carbon|homologous|alkane|ethanol"), ("Periodic Classification of Elements", r"periodic|mendeleev|modern periodic")),
        "biology": _ch(("Life Processes", r"life processes|digest|respirat|heart|kidney|photosynth"), ("Control and Coordination", r"control and coordination|neuron|reflex|hormone|auxin"), ("How Do Organisms Reproduce?", r"reproduce|reproduction|cell division|budding|pollen"), ("Heredity and Evolution", r"heredity|mendel|evolution|sex determination|chromosome"), ("Our Environment", r"our environment|food chain|ecosystem|ozone|trophic")),
        "geography": _ch(("Resources and Development", r"resources|soils?\b"), ("Forest and Wildlife Resources", r"natural vegetation|wildlife|forest"), ("Water Resources", r"\bdams?\b|water resources"), ("Agriculture", r"agricultur|crops?\b|kharif|rabi"), ("Minerals and Energy Resources", r"minerals?|energy resources"), ("Manufacturing Industries", r"human geography|industr|economic activities"), ("Lifelines of National Economy", r"transport|ports")),
        "economics": _ch(("Development", r"per capita|development|human development|average income|income"), ("Sectors of the Indian Economy", r"sectors?|primary|secondary|tertiary"), ("Money and Credit", r"\bmoney\b|\bcredit\b|\bbarter\b|self-help|reserve bank"), ("Globalisation and the Indian Economy", r"globalis|foreign|\bmnc"), ("Consumer Rights", r"consumer")),
    },
}

PH11 = _ch(("Units and Measurement", r"units?\b and|dimension|significant figure|least count|vernier|screw gauge|si unit"), ("Motion in a Plane", r"projectile|vectors? and|circular motion|centripetal|range of|relative velocity|resultant"),
           ("Motion in a Straight Line", r"accelerat|decelerat|brak|stopping distance|straight line|free fall|uniformly"), ("Laws of Motion", r"friction|newton|momentum|impulse|tension in|inclined|banking|lift\b|recoil"),
           ("Work, Energy and Power", r"collision|kinetic energy|potential energy|work done|(?<!electric )\bpower\b|\benergy\b|spring constant"), ("System of Particles and Rotational Motion", r"rotational|moment of inertia|torque|angular|centre of mass|rolling"),
           ("Gravitation", r"gravit|orbit|escape|satellite|kepler"), ("Mechanical Properties of Solids", r"young|stress|strain|modulus|stretch|elongat"), ("Mechanical Properties of Fluids", r"fluid|bernoulli|viscos|surface tension|pascal|hydraulic|buoyan|pressure at|solids and fluids"),
           ("Thermal Properties of Matter", r"thermal|expansion|specific heat|latent|conduction|calorimet|radiation|heat "), ("Thermodynamics", r"thermodynamic|carnot|isothermal|adiabatic|heat engine"), ("Kinetic Theory", r"kinetic theory|\brms\b|ideal gas|mean free|mol of"),
           ("Oscillations", r"oscillat|pendulum|shm|simple harmonic"), ("Waves", r"\bwaves?\b|string|sound|beat|organ pipe|doppler"))
PH12 = _ch(("Electric Charges and Fields", r"electric charges|coulomb|electric field|gauss|dipole|charges? of"), ("Electrostatic Potential and Capacitance", r"capacitor|capacitance|parallel-plate|electrostatic potential|potential energy of charges"), ("Current Electricity", r"current electricity|\bemf\b|internal resistance|\bohm|resist|kirchhoff|wheatstone|potentiometer|drift|electric power"),
           ("Moving Charges and Magnetism", r"moving charges|ampere|biot|cyclotron|lorentz|solenoid|galvanometer"), ("Magnetism and Matter", r"magnetism and matter|magnetic dipole|bar magnet|diamagnet|paramagnet|ferromagnet"), ("Alternating Current", r"alternating|\bac\b|transformer|reactance|impedance|lc circuit|\brms\b.*(current|voltage)"),
           ("Electromagnetic Induction", r"electromagnetic induction|faraday|lenz|induced|flux|inductance"), ("Electromagnetic Waves", r"electromagnetic waves?|displacement current|em wave"), ("Wave Optics", r"wave optics|young's|fringe|diffract|polari|interfer|huygens|slit"),
           ("Ray Optics and Optical Instruments", r"ray and|ray optics|lens|mirror|refract|prism|microscope|telescope"), ("Dual Nature of Radiation and Matter", r"dual nature|photoelectric|de broglie|work function|photon"), ("Atoms", r"bohr|rydberg|spectral|hydrogen atom"), ("Nuclei", r"atoms and nuclei|nucle|half-life|radioactiv|binding energy|mass defect"),
           ("Semiconductor Electronics", r"semiconductor|diode|transistor|logic gate|p-n"))
CH11 = _ch(("Some Basic Concepts of Chemistry", r"mole concept|molarity|empirical|percentage composition|stoichiometr|\bmoles?\b|molar mass|gas laws|avogadro|limiting"), ("Structure of Atom", r"structure of atom|quantum|orbital|bohr|electronic configuration"), ("Classification of Elements and Periodicity", r"periodic|s-block|ionisation|electronegativ|alkali"),
           ("Chemical Bonding and Molecular Structure", r"bonding|hybridi|vsepr|bond order|molecular orbital|dipole"), ("Thermodynamics", r"thermodynamic|enthalp|entropy|gibbs|hess"), ("Equilibrium", r"equilibri|\bph\b|buffer|solubility product|le chatelier|\bkc\b|\bkp\b"), ("Redox Reactions", r"redox|oxidation number|oxidation state"),
           ("Organic Chemistry: Basic Principles", r"carbon compounds|iupac|homologous|isomer|inductive|carbocation"), ("Hydrocarbons", r"alkane|alkene|alkyne|benzene|hydrocarbon"))
CH12 = _ch(("Solutions", r"solutions? |raoult|colligative|molality|osmotic|henry"), ("Electrochemistry", r"electrochem|nernst|faraday|conductiv|cell potential|electrolys|e°"), ("Chemical Kinetics", r"kinetics|rate constant|rate law|half-life|order of reaction|arrhenius|activation energy"),
           ("The p-Block Elements", r"p-block|noble gas|halogen"), ("The d- and f-Block Elements", r"d- and f|transition|lanthan|actin"), ("Coordination Compounds", r"coordination|ligand|crystal field|werner"), ("Haloalkanes and Haloarenes", r"haloalk|haloaren|alkyl halide|sn1|sn2|chloroform"),
           ("Alcohols, Phenols and Ethers", r"alcohol|phenol|ether\b|lucas"), ("Aldehydes, Ketones and Carboxylic Acids", r"aldehyde|ketone|carboxyl|cannizzaro|aldol|fehling|tollens"), ("Amines", r"\bamines?\b|aniline|diazo|hinsberg|gabriel"), ("Biomolecules", r"biomolecule|protein|carbohydrate|polysaccharide|cellulose|starch|vitamin|nucleic|polymers?\b"))
BI11 = _ch(("The Living World / Classification", r"diversity|classif|kingdom|taxonom"), ("Plant Kingdom", r"bryophyt|pteridophyt|gymnosperm|angiosperm|alga"), ("Animal Kingdom", r"phylum|chordat|arthropod|mollus|annelid"), ("Cell: The Unit of Life", r"\bcell organ|mitochond|ribosome|golgi|cell wall"), ("Cell Cycle and Cell Division", r"cell cycle|cell division|chromosome numbers|mitosis|meiosis"),
           ("Photosynthesis and Respiration in Plants", r"photosynth|respiration in plants|glycoly|krebs|calvin"), ("Human Physiology", r"human physiology|breath|lung|heart|blood|kidney|nephron|muscle|neuron|nerve"), ("Chemical Coordination and Integration", r"hormone|gland|thyroid|insulin"))
BI12 = _ch(("Reproduction", r"reproduction|pollinat|embryo|contracept|menstru"), ("Principles of Inheritance and Variation", r"heredity|mendel|inheritance and variation|sex determination|linkage"), ("Molecular Basis of Inheritance", r"molecular basis|dna|rna|transcription|translation|genetic code"), ("Evolution", r"evolution|hardy|darwin"),
           ("Human Health and Disease", r"human health|disease|immun|malaria|cancer|aids"), ("Microbes in Human Welfare", r"microbes|fermentation|antibiotic|biogas"), ("Biotechnology", r"biotech|restriction|pcr|transgenic|bt "), ("Organisms and Populations", r"organisms and populations|population|mutualism|competition"), ("Ecosystem and Biodiversity", r"our environment|ecosystem|food chain|biodiversity|trophic"))
MA11 = _ch(("Sets", r"(?<!data )\bsets?\b|subset|venn"), ("Relations and Functions", r"relations and"), ("Trigonometric Functions", r"trigonometric|radian|sin\b|cos\b"), ("Complex Numbers and Quadratic Equations", r"complex|quadratic|\biota\b"), ("Linear Inequalities", r"inequal"), ("Permutations and Combinations", r"permutation|combination|arrange"), ("Binomial Theorem", r"binomial theorem|binomial expansion"),
           ("Sequences and Series", r"sequence|series|arithmetic progression|geometric progression|\bgp\b|\bap\b"), ("Straight Lines", r"straight line|slope"), ("Conic Sections", r"conic|parabola|ellipse|hyperbola|circle"), ("Three Dimensional Geometry (Intro)", r"three dimensional|3d|octant"), ("Limits and Derivatives", r"\blimit|\blim\(|derivative"), ("Statistics", r"statistic|variance|standard deviation"), ("Probability", r"probabil"))
MA12 = _ch(("Relations and Functions", r"relations and|one-one|\bonto\b|bijective|composite function"), ("Inverse Trigonometric Functions", r"inverse trig|sin⁻|tan⁻|cos⁻"), ("Matrices", r"matri"), ("Determinants", r"determinant"), ("Continuity and Differentiability", r"continuity|differentiab|chain rule|mean value|rolle"), ("Application of Integrals", r"application of integrals|area under"), ("Integrals", r"integral|∫"),
           ("Application of Derivatives", r"application of derivatives|maxima|minima|rate of change|tangent"), ("Differential Equations", r"differential equation"), ("Vector Algebra", r"\bvectors?\b|dot product|cross product|\d?i\s*[-+]\s*\d*j"), ("Three Dimensional Geometry", r"three dimensional|direction cosine"), ("Linear Programming", r"linear programming|lpp"), ("Probability", r"probabil|bayes"))
CH[11] = {"physics": PH11, "chemistry": CH11, "biology": BI11, "math": MA11,
          "accountancy": _ch(("Accounting Equation and Recording", r"accounting equation|debit|credit|journal|ledger|terms and concepts|trial balance|accountancy: terms"), ("Depreciation", r"depreciation"), ("Financial Statements", r"financial statement|balance sheet")),
          "business": _ch(("Forms of Business Organisation", r"forms of business|sole|partnership firm|company|cooperative"), ("Nature and Purpose of Business", r"business")),
          "economics": _ch(("Statistics for Economics", r"statistic|mean|median|index number|correlation"), ("Indian Economic Development", r"indian econom|reform|liberalis|poverty|employment|infrastructure|sustainable")),
          "geography": _ch(("Fundamentals of Physical Geography", r"atmosphere|interior|landform|climate|temperature|rainfall|ocean"), ("India: Physical Environment", r"india: physical|monsoon")),
          "computer": _ch(("Computer System", r"hardware|software|cpu|memory|operating system|ram\b|rom\b"), ("Encoding and Number Systems", r"binary|hexadecimal|octal|ascii|unicode|bit\b|byte"), ("Getting Started with Python", r"python|list\b|tuple|dictionar|loop|string"), ("Problem Solving", r"algorithm|flowchart|pseudocode"), ("Societal Impact", r"cyber|phishing|malware|privacy|plagiar"))}
CH[12] = {"physics": PH12, "chemistry": CH12, "biology": BI12, "math": MA12,
          "accountancy": _ch(("Partnership Accounts", r"partnership|goodwill|partner|profit-sharing"), ("Company Accounts: Shares and Debentures", r"share|debenture"), ("Analysis of Financial Statements", r"ratio|financial statement|cash flow|terms and concepts")),
          "business": _ch(("Management, Marketing and Finance", r"management|marketing|financial market|planning|staffing|business studies")),
          "economics": _ch(("Introductory Macroeconomics", r"national income|multiplier|macro|gdp|money supply|aggregate|budget|balance of payments"), ("Introductory Microeconomics", r"elasticity|demand|supply|utility|marginal|cost|revenue|market")),
          "geography": _ch(("Fundamentals of Human Geography", r"population|density|sex ratio|migration"), ("India: People and Economy", r"india")),
          "computer": _ch(("Exception and File Handling", r"exception|file\b"), ("Stack and Queue", r"stack|queue"), ("Sorting and Searching", r"sort|search"), ("Database Concepts and SQL", r"database|sql|primary key|table"), ("Computer Networks", r"network|\blan\b|protocol|ip address|http|modem"), ("Security Aspects", r"security|firewall|encrypt|malware"))}
# Rules run in the order that avoids false hits; the chapter list a player sees stays in NCERT book order.
DISPLAY = {"physics11": [n for n, _ in PH11], "chemistry11": [n for n, _ in CH11], "chemistry12": [n for n, _ in CH12], "math11": [n for n, _ in MA11]}


def _first(chapters, *names):
    """Same chapters, with these names tried first."""
    head = [c for n in names for c in chapters if c[0] == n]
    return head + [c for c in chapters if c not in head]


CH[11]["physics"] = _first(PH11, "Units and Measurement", "Oscillations", "Waves", "Thermodynamics", "Kinetic Theory", "Thermal Properties of Matter",
                           "Mechanical Properties of Solids", "Mechanical Properties of Fluids", "Gravitation", "System of Particles and Rotational Motion",
                           "Work, Energy and Power", "Laws of Motion")
CH[11]["chemistry"] = _first(CH11, "Chemical Bonding and Molecular Structure", "Thermodynamics", "Equilibrium", "Redox Reactions")
CH[11]["math"] = _first(MA11, "Limits and Derivatives", "Statistics", "Probability")
CH[12]["chemistry"] = _first(CH12, "Electrochemistry", "Chemical Kinetics", "Coordination Compounds", "Haloalkanes and Haloarenes")
DISPLAY["physics8"] = [n for n, _ in CH[8]["physics"]]
CH[8]["physics"] = _first(CH[8]["physics"], "Friction")
# JEE: Class 12 rules are tried first because they are the more specific ones ("photon energy" is not Work and Energy);
# the chapters are still listed Class 11 first.
CH[13] = {s: CH[12][s] + CH[11][s] for s in ("physics", "chemistry", "math")}
CH[14] = CH[13]
JEE_ORDER = {"physics": list(dict.fromkeys(DISPLAY["physics11"] + [n for n, _ in PH12])),
             "chemistry": DISPLAY["chemistry11"] + DISPLAY["chemistry12"],
             "math": list(dict.fromkeys(DISPLAY["math11"] + [n for n, _ in MA12]))}

JEE_LABEL = {13: "JEE Main", 14: "JEE Advanced"}
# subjects that have an NCERT book in the class; BE (15) and Expert (16) have none
NCERT_SUBJECTS = {level: list(CH[level]) for level in CH}


# topics too wide to name one chapter: their question text decides
BROAD_TOPICS = ("Economics: sectors", "Economics: concepts", "Business Studies", "Accountancy: terms")


def _targets(level, raw, topic):
    """NCERT subjects of this class a question of subject `raw` may belong to."""
    if level <= 5:
        return {"math": ["math"], "commercials": ["math"], "evs": ["evs"], "biology": ["evs"], "chemistry": ["evs"],
                "physics": ["evs"], "geography": ["evs"]}.get(raw, [])
    if level <= 10 and raw == "commercials":
        return ["economics"] if level >= 9 else ["math"]
    if level in (11, 12) and raw == "commercials":
        t = topic.lower()
        return (["accountancy"] if t.startswith("accountancy") else ["business"] if t.startswith("business") else
                ["economics"] if "econom" in t else ["accountancy", "economics", "business"])
    return [raw] if raw in CH[level] else []


def classify(level, raw, topic, question, explanation):
    """-> (subject, chapter name or None, is_ncert)."""
    if raw == "bridge" or level not in CH:
        return raw, None, False
    if topic and not topic.startswith(BROAD_TOPICS):
        tries = [topic.lower()]
    else:           # the question itself first: an explanation often names a neighbouring idea
        tries = [question.lower(), f"{question} {explanation}".lower()]
    for text in tries:
        for subject in _targets(level, raw, topic):
            for name, rx in CH[level][subject]:
                if rx.search(text):
                    return subject, name, True
    # kept, on its own chip: "physics_x" when the class has an NCERT Physics book, plain "finance" when it has no such book
    return (raw + "_x" if raw in CH[level] else raw), None, False


def chapter_order(level, subject):
    if level in (13, 14):
        return JEE_ORDER.get(subject, [])
    if f"{subject}{level}" in DISPLAY:
        return DISPLAY[f"{subject}{level}"]
    return [name for name, _ in CH[level][subject]] if level in CH and subject in CH[level] else []
