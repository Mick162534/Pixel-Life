class ConstructionYard:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id

    @staticmethod
    def meets_prerequisites(world, x, y):
        return True  # No special requirement

    def tick(self, world):
        for site in world.construction_manager.queue:
            if site["tribe_id"] == self.owner_id:
                site["progress"] += 1  # Bonus build speed from nearby yard
