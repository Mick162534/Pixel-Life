class TamingPen:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id

    @staticmethod
    def meets_prerequisites(world, x, y):
        nearby_creatures = [c for c in world.creatures if abs(c.x - x) <= 3 and abs(c.y - y) <= 3 and c.owner_id is None]
        return len(nearby_creatures) > 0

    def tick(self, world):
        for c in world.creatures:
            if abs(c.x - self.x) <= 2 and abs(c.y - self.y) <= 2 and c.owner_id is None:
                c.owner_id = self.owner_id
                print(f"[TAMED] Creature at ({c.x},{c.y}) now belongs to tribe {self.owner_id}")
                break
