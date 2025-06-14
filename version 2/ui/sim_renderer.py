import pygame
import os
from pathlib import Path

class SimRenderer:
    def __init__(self, sim, screen, tile_size=20):
        self.sim = sim
        self.screen = screen
        self.tile_size = tile_size
        self.camera_x = 0
        self.camera_y = 0
        self.view_tiles_x = screen.get_width() // tile_size
        self.view_tiles_y = screen.get_height() // tile_size
        # Load creature sprites (optional)
        self.creature_sprites = {}
        # Load building sprites
        self.building_sprites = {}
        building_types = ['StorageHut', 'LoggingCamp', 'Farm', 'ConstructionYard', 'TamingPen', 'Watchtower', 'ResearchHut', 'Housing', 'CommunalCenter']
        for b in building_types:
            path = Path("assets/buildings") / f"{b}.png"
            if path.exists():
                img = pygame.image.load(str(path))
                self.building_sprites[b] = pygame.transform.scale(img, (tile_size, tile_size))

        # Terrain sprites
        self.terrain_sprites = {}
        for t in ["grass", "water", "tree"]:
            path = Path("assets/terrain") / f"{t}.png"
            if path.exists():
                img = pygame.image.load(str(path))
                self.terrain_sprites[t] = pygame.transform.scale(img, (tile_size, tile_size))

    def render(self):
        self.screen.fill((30, 30, 30))

        # Draw terrain grid
        for x in range(self.view_tiles_x):
            wx = x + self.camera_x
            if wx >= self.sim.width:
                continue
            for y in range(self.view_tiles_y):
                wy = y + self.camera_y
                if wy >= self.sim.height:
                    continue
                tile = self.sim.terrain.get_tile(wx, wy)
                sprite = self.terrain_sprites.get(tile)
                if sprite:
                    self.screen.blit(sprite, (x * self.tile_size, y * self.tile_size))

        # Draw buildings within camera view
        for b in self.sim.buildings:
            sx = (b.x - self.camera_x) * self.tile_size
            sy = (b.y - self.camera_y) * self.tile_size
            if 0 <= sx < self.screen.get_width() and 0 <= sy < self.screen.get_height():
                sprite = self.building_sprites.get(b.__class__.__name__)
                if sprite:
                    self.screen.blit(sprite, (sx, sy))
        # Draw creatures
        for c in self.sim.creatures:
            if not getattr(c, "alive", True):
                continue
            sx = (c.x - self.camera_x) * self.tile_size
            sy = (c.y - self.camera_y) * self.tile_size
            if 0 <= sx < self.screen.get_width() and 0 <= sy < self.screen.get_height():
                trait = c.traits[0] if c.traits else None
                sprite = self.creature_sprites.get(trait)
                if sprite:
                    self.screen.blit(sprite, (sx, sy))
                else:
                    pygame.draw.rect(self.screen, (255,255,0), (sx, sy, self.tile_size, self.tile_size))
        pygame.display.flip()
