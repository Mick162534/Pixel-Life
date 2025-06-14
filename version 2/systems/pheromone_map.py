class PheromoneMap:
    def __init__(self, width, height, decay_rate=0.01):
        self.width = width
        self.height = height
        self.decay_rate = decay_rate
        # 2D list for pheromone intensities
        self.map = [[0.0 for _ in range(width)] for _ in range(height)]

    def deposit(self, x, y, amount=1.0):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.map[y][x] += amount

    def evaporate(self):
        for y in range(self.height):
            for x in range(self.width):
                self.map[y][x] = max(0.0, self.map[y][x] * (1 - self.decay_rate))

    def get_intensity(self, x, y, radius=5):
        total = 0.0
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                xx, yy = x + dx, y + dy
                if 0 <= xx < self.width and 0 <= yy < self.height:
                    total += self.map[yy][xx]
        return total
