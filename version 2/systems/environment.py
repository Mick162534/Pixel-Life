class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [["EMPTY" for _ in range(width)] for _ in range(height)]

    def get_tile(self, x, y):
        return self.grid[y][x]

    def set_tile(self, x, y, tile_type):
        self.grid[y][x] = tile_type
