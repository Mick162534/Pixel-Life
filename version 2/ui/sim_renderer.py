import pygame
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
        # Placeholder surfaces for creatures, buildings and terrain
        # If image assets exist locally they will override these colors
        self.creature_sprites = {}
        self.building_sprites = {}
        building_colors = {
            'StorageHut': (139, 69, 19),
            'LoggingCamp': (160, 82, 45),
            'Farm': (218, 165, 32),
            'ConstructionYard': (105, 105, 105),
            'TamingPen': (205, 133, 63),
            'Watchtower': (184, 134, 11),
            'ResearchHut': (70, 130, 180),
            'Housing': (210, 180, 140),
            'CommunalCenter': (128, 0, 128),
        }
        for b, color in building_colors.items():
            surface = pygame.Surface((tile_size, tile_size))
            surface.fill(color)
            self.building_sprites[b] = surface
            path = Path("assets/buildings") / f"{b}.png"
            if path.exists():
                img = pygame.image.load(str(path))
                self.building_sprites[b] = pygame.transform.scale(img, (tile_size, tile_size))

        # Terrain sprites
        self.terrain_sprites = {}
        terrain_colors = {
            "grass": (34, 139, 34),
            "water": (0, 0, 255),
            "tree": (0, 100, 0),
        }
        for t, color in terrain_colors.items():
            surface = pygame.Surface((tile_size, tile_size))
            surface.fill(color)
            self.terrain_sprites[t] = surface
            path = Path("assets/terrain") / f"{t}.png"
            if path.exists():
                img = pygame.image.load(str(path))
                self.terrain_sprites[t] = pygame.transform.scale(img, (tile_size, tile_size))

        # creature colors
        trait_colors = {
            "builder": (255, 215, 0),
            "gatherer": (30, 144, 255),
            "herbivore": (124, 252, 0),
        }
        for trait, color in trait_colors.items():
            surf = pygame.Surface((tile_size, tile_size))
            surf.fill(color)
            self.creature_sprites[trait] = surf

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

