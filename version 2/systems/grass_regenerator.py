import random

class GrassRegenerator:
    def __init__(self, width, height, tree_coords=None):
        self.width = width
        self.height = height
        self.tree_coords = tree_coords or []

    def is_near_tree(self, x, y, radius=5):
        return any(abs(x - tx) <= radius and abs(y - ty) <= radius for tx, ty in self.tree_coords)

    def count_adjacent_grass(self, env, x, y):
        count = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if env.get_tile(nx, ny) == "GRASS":
                    count += 1
        return count

    def update(self, env, corpse_heatmap):
        for y in range(self.height):
            for x in range(self.width):
                if env.get_tile(x, y) != "EMPTY":
                    continue
                chance = 0.05
                count = self.count_adjacent_grass(env, x, y)
                chance += 0.1 * count
                if self.is_near_tree(x, y):
                    chance += 0.2
                corpse_heat = corpse_heatmap.get(x, y)
                chance -= 0.2 * (corpse_heat / 100)
                if random.random() < chance:
                    env.set_tile(x, y, "GRASS")
