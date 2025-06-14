def guard_behavior(creature, world):
    # Guard creatures protect their home den
    if not hasattr(creature, "home_den"):
        return False
    den_x, den_y = creature.home_den
    # Detect enemy creatures near the den
    enemies = [
        c for c in world.creatures
        if getattr(c, "tribe_id", None) and c.tribe_id != creature.tribe_id
        and abs(c.x - den_x) <= 5 and abs(c.y - den_y) <= 5
    ]
    if not enemies:
        return False
    # Choose nearest enemy
    target = min(enemies, key=lambda c: abs(c.x - creature.x) + abs(c.y - creature.y))
    # Move to or attack the target
    if abs(target.x - creature.x) > 1 or abs(target.y - creature.y) > 1:
        # move_towards should be defined on Creature
        creature.move_towards(target.x, target.y)
    else:
        # attack method on Creature
        creature.attack(target)
    return True
