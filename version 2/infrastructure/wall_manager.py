from infrastructure.wall_tile import WallTile


class WallManager:
    def __init__(self):
        self.wall_tiles = []

    def add_wall(self, x, y, owner_id):
        if not self.get_wall(x, y):
            self.wall_tiles.append(WallTile(x, y, owner_id))

    def get_wall(self, x, y):
        for wall in self.wall_tiles:
            if wall.x == x and wall.y == y:
                return wall
        return None

    def is_inside_walls(self, x, y, owner_id):
        owned_walls = [w for w in self.wall_tiles if w.owner_id == owner_id]
        if not owned_walls:
            return True  # no walls yet, everything is allowed
        xs = [w.x for w in owned_walls]
        ys = [w.y for w in owned_walls]
        return min(xs) < x < max(xs) and min(ys) < y < max(ys)
