from collections import defaultdict

class MetricsCollector:
    def __init__(self):
        self.tick_data = []

    def record(self, tick, creatures, env, corpse_heatmap):
        count_by_trait = defaultdict(int)
        total_energy = 0
        grass_count = 0
        corpse_count = 0

        for row in env.grid:
            for tile in row:
                if tile == "GRASS":
                    grass_count += 1

        for row in corpse_heatmap.grid:
            for val in row:
                if val > 0:
                    corpse_count += 1

        for c in creatures:
            total_energy += c.energy
            for trait in c.traits:
                count_by_trait[trait] += 1

        avg_energy = total_energy / len(creatures) if creatures else 0

        data = {
            "tick": tick,
            "creature_count": len(creatures),
            "grass_count": grass_count,
            "corpse_count": corpse_count,
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
        for tick in self.tick_data:
            for key in tick:
                if key not in ["tick", "creature_count", "grass_count", "corpse_count", "avg_energy"]:
                    trait_keys.add(key)
        return sorted(trait_keys)
