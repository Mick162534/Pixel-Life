import math

def calculate_affinity(creature_a, creature_b):
    if creature_a.id == creature_b.id:
        return 0
    shared_traits = set(creature_a.traits).intersection(set(creature_b.traits))
    trait_bonus = len(shared_traits) * 5
    charisma_bonus = (creature_a.stats.get("charisma", 10) + creature_b.stats.get("charisma", 10)) / 2
    distance = math.sqrt((creature_a.x - creature_b.x) ** 2 + (creature_a.y - creature_b.y) ** 2)
    if distance > 10:
        return 0
    distance_penalty = max(0, 10 - distance)
    return trait_bonus + charisma_bonus + distance_penalty
