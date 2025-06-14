class Den:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id

    @staticmethod
    def meets_prerequisites(world, x, y):
        # Must be within tribe territory
        for tribe in world.tribes:
            if tribe.tribe_id == owner_id and (x, y) in getattr(tribe, "territory_tiles", []):
                return True
        return False

    def tick(self, world):
        pass  # Dens are passive
