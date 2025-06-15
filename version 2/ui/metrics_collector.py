from collections import defaultdict

class MetricsCollector:
    def __init__(self):
        self.tick_data = []

    def record(self, tick, world):
        """Collect simple metrics from the world each tick."""
        count_by_trait = defaultdict(int)
        total_energy = 0
        resource_count = 0
        bush_count = 0

        for node in getattr(world.resource_manager, "nodes", []):
            if not getattr(node, "is_depleted", False):
                resource_count += 1

        for bush in getattr(world, "bushes", []):
            if not bush.is_depleted:
                bush_count += 1

        living = [c for c in world.creatures if getattr(c, "alive", True)]
        for c in living:
            total_energy += c.energy
            for trait in c.traits:
                count_by_trait[trait] += 1

        avg_energy = total_energy / len(living) if living else 0

        data = {
            "tick": tick,
            "creature_count": len(living),
            "resource_nodes": resource_count,
            "bush_nodes": bush_count,
            "avg_energy": avg_energy,
        }
        data.update(count_by_trait)
        self.tick_data.append(data)

    def get_series(self, key):
        return [tick.get(key, 0) for tick in self.tick_data]

    def get_all_ticks(self):
        return [tick["tick"] for tick in self.tick_data]

    def get_all_trait_keys(self):
        trait_keys = set()
        ignore = ["tick", "creature_count", "resource_nodes", "bush_nodes", "avg_energy"]
        for tick in self.tick_data:
            for key in tick:
                if key not in ignore:
                    trait_keys.add(key)
        return sorted(trait_keys)
