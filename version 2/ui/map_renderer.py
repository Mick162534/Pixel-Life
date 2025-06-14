import pygame

class MapRenderer:
    def __init__(self, sim, screen, map_rect=(10,10,200,200)):
        self.sim = sim
        self.screen = screen
        self.map_rect = pygame.Rect(map_rect)

    def render(self):
        # semi-transparent overlay
        s = pygame.Surface((self.map_rect.width, self.map_rect.height), pygame.SRCALPHA)
        s.fill((0,0,0,180))
        self.screen.blit(s, (self.map_rect.x, self.map_rect.y))
        # draw chunks
        cw = self.map_rect.width / self.sim.chunk_manager.max_chunks_x
        ch = self.map_rect.height / self.sim.chunk_manager.max_chunks_y
        for (cx, cy), chunk in self.sim.chunk_manager.loaded.items():
            color = (34,139,34)  # default
            # pick color by biome of first tile
            tile = chunk['tiles'][0][0]
            if tile == 'water': color = (0,0,255)
            elif tile == 'forest': color = (34,139,34)
            pygame.draw.rect(self.screen, color,
                (self.map_rect.x + cx*cw, self.map_rect.y + cy*ch, cw, ch))
        # highlight camera
        cam_cx, cam_cy = self.sim.camera_chunk
        pygame.draw.rect(self.screen, (255,255,0),
                         (self.map_rect.x + cam_cx*cw, self.map_rect.y + cam_cy*ch, cw, ch), 2)
