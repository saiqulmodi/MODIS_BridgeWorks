"""'Two Steps Forward' failure handling (Prompt 6).

There is no Game Over. When something breaks, the simulation freezes on the first
fracture/collision and a Black Box Investigation opens: the exact formula that failed,
a stress/speed history chart, a diagnosis quiz (EXP for a correct answer), a salvage
refund, and - where the level offers one - an alternate route that turns the failure
into a new path forward.
"""
import random
from dataclasses import dataclass, field

EXP_AUTOPSY = 10          # for opening the investigation and reading it
EXP_DIAGNOSIS = 50        # correct diagnosis on the first try
EXP_ALTERNATE = 30        # completing a level by its alternate route
SALVAGE_FRACTION = 0.30   # share of the failed build cost refunded as salvage credit
ACADEMY_SALVAGE_FRACTION = 0.75   # ... after a correct BridgeWorks Academy challenge answer

# kind -> (correct diagnosis, short lesson)
CAUSES = {
    "buckling": ("A member in compression buckled (P > P_cr)",
                 "Long thin struts bow sideways. Shorten them, brace them, or use a shape with a "
                 "bigger I (I-beam, hollow box): P_cr = pi^2 E I / (K L)^2."),
    "yield": ("A member was over-stressed (sigma = N/A too big)",
              "Give the member more area A, a stronger material, or share the load with more triangles."),
    "unstable": ("The frame was a mechanism - not enough triangles",
                 "Squares fold up. Every panel needs a diagonal so the joints cannot slide."),
    "stall": ("The slope pulled back harder than the engine could pull",
              "m g sin(theta) grows with steepness. Flatten the grade, add power, or carry less."),
    "overrun": ("The train could not stop in the distance it had",
                "d_stop = v^2 / (2 (mu g cos(theta) - g sin(theta))). Brake earlier or approach slower."),
    "runaway": ("Gravity beat the brakes on the descent",
                "If g sin(theta) > mu g cos(theta) no brake can stop you. Make the descent gentler."),
    "collision": ("Two trains were allowed into the same block",
                  "Signals must warn at least d_stop ahead, and the single track needs an interlock."),
    "derail": ("A switch moved under (or just before) a train",
               "Lock switches while their track circuit is occupied."),
    "misroute": ("Trains were sent down the wrong route",
                 "Switches must follow the train type: cargo to the harbor, passengers to the main line."),
    "crossing": ("The level-crossing barrier was not down in time",
                 "Barriers take seconds to fall; trigger them from far enough out."),
    "gridlock": ("Demand was higher than the junction's capacity",
                 "q = k v peaks at k_crit. Above it, queues grow and shockwaves travel backwards."),
    "overturn": ("The pier tipped: the see-saw was out of balance",
                 "sum(W x) on one side must stay within the foundation's resistance. Alternate sides "
                 "or add tie-downs."),
    "root": ("The girder cracked at the pier: bending stress too high",
             "sigma = M y / I and I = b d^3 / 12: a deeper haunch at the pier helps a lot."),
    "girder": ("The finished girder was over-stressed by the truck",
               "Post-tensioning adds pre-compression; a deeper mid-span section raises I."),
    "resonance": ("Wind vortices pushed in step with the bridge's natural swing",
                  "When f_v = St U / D matches f_n the swing grows. Detune (stiffen), add damping, "
                  "a tuned mass damper, or fairings."),
    "pounding": ("The isolated deck swung into the abutment",
                 "Seismic isolation lowers forces but increases movement: add flexible joints."),
    "seismic": ("Earthquake base shear broke the supports",
                "V = C M a_g. Brace the piers, or isolate the deck to lengthen the period and cut C."),
    "timeout": ("The job took longer than the deadline",
                "Speed comes from power, gentle grades and fewer bottlenecks."),
    "brownout": ("The smart grid ran out of power",
                 "Maglev thrust and smart-alloy stiffening share one power budget."),
    "budget": ("The design cost more than the budget",
               "Use the calculator: aim for FS 1.5-2.0, not 5."),
}


@dataclass
class FailureReport:
    kind: str
    title: str
    formula: str
    details: list = field(default_factory=list)
    time: float = 0.0
    element: object = None            # what to highlight (member index, train id, ...)
    history: dict = field(default_factory=dict)   # series name -> [(t, value)]
    build_cost: float = 0.0
    diagnosed: bool = False
    diagnosis_attempts: int = 0
    options: list = None
    academy_bonus: bool = False       # Academy challenge answered correctly

    @property
    def salvage(self):
        return (ACADEMY_SALVAGE_FRACTION if self.academy_bonus else SALVAGE_FRACTION) * self.build_cost

    @property
    def correct_cause(self):
        return CAUSES.get(self.kind, (self.title, ""))[0]

    @property
    def lesson(self):
        return CAUSES.get(self.kind, ("", ""))[1]

    def diagnosis_options(self, seed=None):
        """Three answers: the real cause plus two plausible wrong ones (stable per report)."""
        if self.options is None:
            rng = random.Random(seed if seed is not None else hash(self.title) & 0xFFFF)
            wrong = [c[0] for k, c in CAUSES.items() if k != self.kind]
            picks = rng.sample(wrong, 2) + [self.correct_cause]
            rng.shuffle(picks)
            self.options = picks
        return self.options

    def diagnose(self, answer):
        """Returns EXP earned for this answer (only the first attempt can earn the bonus)."""
        self.diagnosis_attempts += 1
        if answer == self.correct_cause:
            first = not self.diagnosed and self.diagnosis_attempts == 1
            self.diagnosed = True
            return EXP_DIAGNOSIS if first else 0
        return 0
