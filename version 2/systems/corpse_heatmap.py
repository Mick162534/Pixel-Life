class CorpseHeatmap:
    def __init__(self, width, height):
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def add_heat(self, x, y, amount):
        self.grid[y][x] = min(100, self.grid[y][x] + amount)

    def get(self, x, y):
        return self.grid[y][x]

    def update(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] > 0:
                    self.grid[y][x] -= 2
