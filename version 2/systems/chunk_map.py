class Chunk:
    def __init__(self, x, y, width=20, height=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tiles = [["EMPTY" for _ in range(width)] for _ in range(height)]

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def set_tile(self, x, y, tile_type):
        self.tiles[y][x] = tile_type


class ChunkMap:
    def __init__(self, chunks_x=9, chunks_y=9, chunk_size=20):
        self.chunks_x = chunks_x
        self.chunks_y = chunks_y
        self.chunk_size = chunk_size
        self.chunks = [
            [Chunk(cx, cy, chunk_size, chunk_size) for cx in range(chunks_x)]
            for cy in range(chunks_y)
        ]

    def get_tile(self, global_x, global_y):
        cx, tx = divmod(global_x, self.chunk_size)
        cy, ty = divmod(global_y, self.chunk_size)
        return self.chunks[cy][cx].get_tile(tx, ty)

    def set_tile(self, global_x, global_y, tile_type):
        cx, tx = divmod(global_x, self.chunk_size)
        cy, ty = divmod(global_y, self.chunk_size)
        self.chunks[cy][cx].set_tile(tx, ty, tile_type)

    def all_tiles(self):
        for cy in range(self.chunks_y):
            for cx in range(self.chunks_x):
                chunk = self.chunks[cy][cx]
                for y in range(chunk.height):
                    for x in range(chunk.width):
                        yield (cx * self.chunk_size + x, cy * self.chunk_size + y, chunk.tiles[y][x])
