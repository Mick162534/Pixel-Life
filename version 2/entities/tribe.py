import random
from collections import defaultdict

class Tribe:
    def __init__(self, leader, members):
        self.id = f"tribe-{random.randint(10000, 99999)}"
        self.leader = leader
        self.members = members
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.state = "tribe"
        self.ticks_stationary = 0
        self.last_center = (leader.x, leader.y)
        self.growth_check_timer = 0

    def update_leader(self):
        self.leader = max(self.members, key=lambda c: c.stats["charisma"] + c.stats["intelligence"])

    def is_stationary(self):
        center_x = sum(c.x for c in self.members) / len(self.members)
        center_y = sum(c.y for c in self.members) / len(self.members)
        dx = abs(center_x - self.last_center[0])
        dy = abs(center_y - self.last_center[1])
        self.last_center = (center_x, center_y)
        return dx <= 2 and dy <= 2

    def average_affinity(self):
        total = 0
        count = 0
        for c in self.members:
            for other in self.members:
                if c != other and other.id in c.affinities:
                    total += c.affinities[other.id]
                    count += 1
        return total / count if count else 0

    def trait_distribution(self):
        trait_count = defaultdict(int)
        for c in self.members:
            for t in c.traits:
                trait_count[t] += 1
        return trait_count

    def tick(self):
        if self.state == "city":
            return

        if self.is_stationary():
            self.ticks_stationary += 1
        else:
            self.ticks_stationary = 0

        self.growth_check_timer += 1
        if self.growth_check_timer >= 50:
            self.growth_check_timer = 0
            if self.check_city_growth():
                self.state = "city"
                print(f"{self.id} has evolved into a city!")

    def check_city_growth(self):
        if len(self.members) < 10:
            return False
        if self.leader.stats["intelligence"] < 15:
            return False
        if self.ticks_stationary < 300:
            return False
        if self.average_affinity() < 12:
            return False
        trait_count = self.trait_distribution()
        economic_traits = ["builder", "trader", "gatherer"]
        econ_total = sum(trait_count[t] for t in economic_traits if t in trait_count)
        return econ_total >= len(self.members) * 0.3
