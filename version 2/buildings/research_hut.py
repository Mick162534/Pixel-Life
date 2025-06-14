class ResearchHut:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id

    @staticmethod
    def meets_prerequisites(world, x, y):
        return True  # Could later require quiet zone

    def tick(self, world):
        pass  # All research logic is handled in ResearchManager
