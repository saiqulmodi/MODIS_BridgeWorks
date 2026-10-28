"""
National Infrastructure Economy & Policy Engine.
Handles Treasury grants, Q/A-driven Green Subsidies, Toll Revenue, and Civic Approval.
"""

class CivicEconomy:
    def __init__(self, project_name="Bandra-Worli Sea Link", initial_grant=50000000):
        self.project_name = project_name
        self.treasury = initial_grant  # INR
        self.subsidies_earned = 0
        self.toll_rate = 85.0          # INR per vehicle
        self.daily_traffic = 0
        self.social_approval = 100.0   # Approval rating percentage
        self.penalties = 0

    def deduct_material_cost(self, material_type, length_m):
        costs = {
            "timber": 1500,
            "structural_steel": 12000,
            "prestressed_concrete": 28000,
            "stay_cable_strand": 45000,
        }
        cost = costs.get(material_type, 10000) * length_m
        if self.treasury >= cost:
            self.treasury -= cost
            return True, cost
        return False, cost

    def apply_academic_subsidy(self, question_class, is_correct):
        """
        Class 10-12 and JEE correct answers unlock substantial green/research subsidies.
        Incorrect answers trigger regulatory audit penalties.
        """
        if is_correct:
            tier_multiplier = 1.6 ** (max(1, question_class - 6))
            grant = int(50000 * tier_multiplier)
            self.treasury += grant
            self.subsidies_earned += grant
            self.social_approval = min(100.0, self.social_approval + 1.5)
            return True, grant
        else:
            penalty = 25000
            self.treasury -= penalty
            self.penalties += penalty
            self.social_approval = max(0.0, self.social_approval - 3.0)
            return False, penalty

    def collect_toll_revenue(self, vehicle_count):
        revenue = vehicle_count * self.toll_rate
        self.daily_traffic += vehicle_count
        self.treasury += revenue
        return revenue

    def get_status(self):
        return {
            "Treasury": f"₹{self.treasury:,.2f}",
            "Subsidies": f"₹{self.subsidies_earned:,.2f}",
            "Approval": f"{self.social_approval:.1f}%",
            "Vehicles Passed": self.daily_traffic
        }
