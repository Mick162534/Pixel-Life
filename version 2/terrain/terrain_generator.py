import random

class TerrainGenerator:
    """Generate simple terrain tiles for the world."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [["grass" for _ in range(height)] for _ in range(width)]
        self.generate()

    def generate(self):
        # sprinkle a few ponds with shallow edges and deep centers

        for _ in range(max(1, (self.width * self.height) // 50)):
            wx, wy = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    x, y = wx + dx, wy + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        dist = max(abs(dx), abs(dy))
                        self.tiles[x][y] = "deep_water" if dist <= 1 else "shallow_water"

        for _ in range(max(1, (self.width * self.height) // 40)):
            tx, ty = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self.tiles[tx][ty] = "tree"

    def get_tile(self, x, y):
        return self.tiles[x][y]
