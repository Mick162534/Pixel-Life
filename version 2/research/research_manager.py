import random

class ResearchManager:
    def __init__(self, tribe_id):
        self.tribe_id = tribe_id
        self.knowledge_points = 0
        self.unlocked = set()
        self.unlock_pool = {
            "logging_camp": {"weight": 5, "requires": []},
            "farm": {"weight": 3, "requires": ["logging_camp"]},
            "taming_pen": {"weight": 2, "requires": ["farm"]},
            "watchtower": {"weight": 2, "requires": ["farm"]},
            "construction_yard": {"weight": 2, "requires": ["watchtower"]},
            "advanced_traits": {"weight": 1, "requires": ["construction_yard"]},
        }

    def tick(self, tribe, world):
        self.knowledge_points += self.count_researchers(tribe, world)

        if self.knowledge_points >= 10:
            self.knowledge_points -= 10
            self.try_unlock(tribe, world)

    def count_researchers(self, tribe, world):
        return sum(1 for c in tribe.members if "scholar" in c.traits and c.alive)

    def try_unlock(self, tribe, world):
        available = [k for k, v in self.unlock_pool.items()
                     if k not in self.unlocked and all(req in self.unlocked for req in v["requires"])]
        if not available:
            return

        weights = []
        for tech in available:
            base = self.unlock_pool[tech]["weight"]
            if tech == "farm":
                base += self._bias_for_farming(tribe, world)
            elif tech == "watchtower":
                base += self._bias_for_predators(tribe, world)
            elif tech == "taming_pen":
                base += self._bias_for_animals(tribe, world)
            elif tech == "construction_yard":
                base += self._bias_for_builders(tribe)
            weights.append(base)

        chosen = random.choices(available, weights=weights, k=1)[0]
        self.unlocked.add(chosen)
        print(f"[RESEARCH] Tribe {tribe.id} unlocked: {chosen}")

    def _bias_for_farming(self, tribe, world):
        return sum(1 for pile in world.piles if pile.owner_id == tribe.id and pile.food > 20)

    def _bias_for_predators(self, tribe, world):
        return sum(1 for c in world.creatures if "carnivore" in c.traits and self._in_territory(c, tribe))

    def _bias_for_animals(self, tribe, world):
        return sum(1 for c in world.creatures if "herbivore" in c.traits and self._in_territory(c, tribe))

    def _bias_for_builders(self, tribe):
        return sum(1 for c in tribe.members if "builder" in c.traits)

    def _in_territory(self, creature, tribe):
        return abs(creature.x - tribe.center_x) <= tribe.territory_radius and abs(creature.y - tribe.center_y) <= tribe.territory_radius
