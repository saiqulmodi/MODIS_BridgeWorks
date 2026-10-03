"""Building materials and their real-world properties.

All values are SI units: E and strengths in pascals (Pa), density in kg/m^3.
Cost is in rupees per kg of material placed (used by the economy in Prompt 8).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    name: str
    E: float                     # Young's modulus (stiffness), Pa
    tensile_strength: float      # stress at which it fails when pulled, Pa
    compressive_strength: float  # stress at which it crushes when pushed, Pa
    density: float               # kg/m^3
    cost_per_kg: float           # Rs per kg
    colour: tuple = (200, 200, 200)


TIMBER = Material("Timber", E=11e9, tensile_strength=40e6, compressive_strength=30e6,
                  density=500, cost_per_kg=60, colour=(181, 134, 84))

STEEL = Material("Steel", E=200e9, tensile_strength=250e6, compressive_strength=250e6,
                 density=7850, cost_per_kg=90, colour=(150, 160, 175))

# Plain concrete is strong when pushed but cracks almost at once when pulled.
CONCRETE = Material("Concrete", E=30e9, tensile_strength=0.0, compressive_strength=30e6,
                    density=2400, cost_per_kg=8, colour=(175, 175, 165))

ALL = {m.name: m for m in (TIMBER, STEEL, CONCRETE)}
