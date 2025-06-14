class CommunalCenter:
    def __init__(self, x, y, owner_id, radius=5, morale_bonus=1):
        self.x = x
        self.y = y
        self.owner_id = owner_id
        self.radius = radius
        self.morale_bonus = morale_bonus

    @staticmethod
    def meets_prerequisites(world, x, y):
        # Must be built within tribe territory
        for tribe in world.tribes:
            if tribe.id == world.current_tribe_id and (x, y) in tribe.territory_tiles():
                return True
        return False

    def tick(self, world):
        # Increase morale for tribe members near center
        tribe = next((t for t in world.tribes if t.id == self.owner_id), None)
        if not tribe:
            return
        count = sum(1 for m in tribe.members if abs(m.x - self.x) <= self.radius and abs(m.y - self.y) <= self.radius)
        if count >= len(tribe.members) * 0.5:  # at least half present
            tribe.morale = min(100, tribe.morale + self.morale_bonus)
