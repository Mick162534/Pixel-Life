import random

class Tribe:
    def __init__(self, tribe_id, name):
        self.tribe_id = tribe_id
        self.name = name
        self.members = []
        self.territory_chunks = set()
        self.relationships = {}  # tribe_id -> 'neutral', 'hostile', 'allied'
        self.warrior_cache = []
        self.last_raid_tick = -1000  # delay between raids

    def tick(self, world, current_tick):
        # Recalculate warrior list
        self.warrior_cache = [c for c in self.members if 'warrior' in c.traits]
        if len(self.warrior_cache) < 3 or current_tick - self.last_raid_tick < 300:
            return  # Not enough warriors or too soon to raid again

        # Evaluate nearby tribes
        possible_targets = []
        for other in world.tribes:
            if other.tribe_id == self.tribe_id:
                continue
            relation = self.relationships.get(other.tribe_id, "neutral")
            if relation == "allied":
                continue

            if self.is_in_raid_range(other):
                possible_targets.append((other, relation))

        if not possible_targets:
            return

        # Sort by hostility and proximity
        target, status = sorted(possible_targets, key=lambda t: (t[1] != "hostile", self.distance_to(t[0])))[0]

        # Decide to raid
        if random.random() < 0.5:  # 50% chance to commit to raid
            print(f"[TRIBE AI] {self.name} plans raid on {target.name} ({status})")
            self.last_raid_tick = current_tick
            world.spawn_raid_band(self, target)

    def is_in_raid_range(self, other):
        for chunk in self.territory_chunks:
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    if (chunk[0] + dx, chunk[1] + dy) in other.territory_chunks:
                        return True
        return False

    def distance_to(self, other):
        if not self.territory_chunks or not other.territory_chunks:
            return 99
        return min(
            abs(x1 - x2) + abs(y1 - y2)
            for (x1, y1) in self.territory_chunks
            for (x2, y2) in other.territory_chunks
        )
