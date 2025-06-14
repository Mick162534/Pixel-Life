class LoggingCamp:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id
        self.wood_stored = 0

    @staticmethod
    def meets_prerequisites(world, x, y):
        nearby_trees = [n for n in world.resource_manager.nodes if n.resource_type == "wood" and abs(n.x - x) <= 3 and abs(n.y - y) <= 3]
        return len(nearby_trees) >= 1

    def tick(self, world):
        trees = [n for n in world.resource_manager.nodes if n.resource_type == "wood" and abs(n.x - self.x) <= 4 and abs(n.y - self.y) <= 4]
        if trees:
            harvested = trees[0].harvest(5)
            self.wood_stored += harvested
