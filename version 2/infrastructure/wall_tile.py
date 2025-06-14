class WallTile:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id
        self.durability = 100  # could decay over time or be attacked in the future
