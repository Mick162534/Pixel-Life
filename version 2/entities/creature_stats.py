import random

STAT_KEYS = ["strength", "charisma", "intelligence", "agility", "endurance", "social_drive"]

def generate_stats(base=10, variance=5):
    stats = {stat: base + random.randint(-variance, variance) for stat in STAT_KEYS}
    # Clamp intelligence and social_drive between 5 and 15
    stats["intelligence"] = max(5, min(15, stats["intelligence"]))
    stats["social_drive"] = max(5, min(15, stats["social_drive"]))
    return stats
