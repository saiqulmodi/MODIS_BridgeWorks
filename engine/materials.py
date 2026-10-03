"""Building materials, cross-section shapes, and their real-world properties.

All values are SI units: E and strengths in pascals (Pa), density in kg/m^3.
Cost is in rupees per kg of material placed (used by the economy, Prompt 8).
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
    carbon_per_kg: float = 1.0   # kg CO2 per kg of material
    maintenance_rate: float = 0.1  # yearly upkeep as a fraction of build cost
    cable_only: bool = False     # True = can only pull (rope/cable), never push
    moisture_factor: float = 1.0   # strength multiplier in wet/humid levels
    voltage_stiffening: float = 1.0  # E multiplier when powered (shape-memory alloy)
    fictional: bool = False


TIMBER = Material("Timber", E=11e9, tensile_strength=40e6, compressive_strength=30e6,
                  density=500, cost_per_kg=60, colour=(196, 146, 92),
                  carbon_per_kg=0.4, maintenance_rate=0.25, moisture_factor=0.7)

STEEL = Material("Steel", E=200e9, tensile_strength=250e6, compressive_strength=250e6,
                 density=7850, cost_per_kg=90, colour=(170, 182, 200),
                 carbon_per_kg=1.9, maintenance_rate=0.10)

# Plain concrete is strong when pushed but cracks almost at once when pulled.
CONCRETE = Material("Concrete", E=30e9, tensile_strength=0.0, compressive_strength=30e6,
                    density=2400, cost_per_kg=8, colour=(185, 185, 172),
                    carbon_per_kg=0.15, maintenance_rate=0.05)

STEEL_CABLE = Material("Steel cable", E=190e9, tensile_strength=1500e6, compressive_strength=0.0,
                       density=7850, cost_per_kg=160, colour=(120, 200, 230),
                       carbon_per_kg=2.0, maintenance_rate=0.08, cable_only=True)

CARBON_CABLE = Material("Carbon-fibre cable", E=160e9, tensile_strength=2400e6,
                        compressive_strength=0.0, density=1600, cost_per_kg=2500,
                        colour=(60, 60, 70), carbon_per_kg=25, maintenance_rate=0.02,
                        cable_only=True)

# Fiction layer: "infinite" tensile capacity, zero compressive strength.
NANOTUBE = Material("Nanotube cable", E=1000e9, tensile_strength=1e15, compressive_strength=0.0,
                    density=1300, cost_per_kg=9000, colour=(190, 90, 255),
                    carbon_per_kg=40, maintenance_rate=0.01, cable_only=True, fictional=True)

# Fiction-flavoured: stiffens (E x2) when the smart grid powers it.
SMART_ALLOY = Material("Smart alloy", E=70e9, tensile_strength=700e6, compressive_strength=700e6,
                       density=6500, cost_per_kg=1500, colour=(90, 230, 190),
                       carbon_per_kg=12, maintenance_rate=0.03, voltage_stiffening=2.0,
                       fictional=True)

ALL = {m.name: m for m in (TIMBER, STEEL, CONCRETE, STEEL_CABLE, CARBON_CABLE, NANOTUBE,
                           SMART_ALLOY)}


@dataclass(frozen=True)
class Shape:
    """Cross-section shape. I = factor * A^2, so for the SAME amount of material (A),
    spreading it away from the centre (I-beam, hollow box) gives a much bigger I."""
    name: str
    factor: float          # I / A^2
    fabrication: float     # cost multiplier for making this shape


SOLID = Shape("Solid square", 1 / 12, 1.00)
IBEAM = Shape("I-beam", 0.45, 1.15)
BOX = Shape("Hollow box", 0.80, 1.30)
SHAPES = {s.name: s for s in (SOLID, IBEAM, BOX)}

# Standard sizes the build menu offers (cross-section area, m^2)
BEAM_SIZES = {"S": 0.001, "M": 0.002, "L": 0.004, "XL": 0.008}
CABLE_SIZES = {"S": 0.0005, "M": 0.001, "L": 0.002, "XL": 0.004}
AREA_MIN, AREA_MAX = 0.0003, 0.02


def second_moment(shape, A):
    """I for a member of area A with the given shape."""
    return shape.factor * A * A
