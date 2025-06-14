class Farm:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id
        self.food_stored = 0

    @staticmethod
    def meets_prerequisites(world, x, y):
        nearby_grass = sum(1 for row in world.map[max(0, y-2):y+3] for tile in row[max(0, x-2):x+3] if tile == "grass")
        return nearby_grass >= 3

    def tick(self, world):
        nearby_grass = sum(1 for row in world.map[max(0, self.y-2):self.y+3] for tile in row[max(0, self.x-2):self.x+3] if tile == "grass")
        self.food_stored += 1 + (nearby_grass // 4)
