class Watchtower:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id

    @staticmethod
    def meets_prerequisites(world, x, y):
        return True  # No special terrain needed

    def tick(self, world):
        for c in world.creatures:
            if c.owner_id != self.owner_id and abs(c.x - self.x) <= 5 and abs(c.y - self.y) <= 5:
                if "revealed" not in c.traits:
                    c.traits.append("revealed")  # Could be used by combat AI later
