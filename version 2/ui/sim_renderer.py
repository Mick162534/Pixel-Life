import pygame
import os
from pathlib import Path

class SimRenderer:
    def __init__(self, sim, screen, tile_size=20):
        self.sim = sim
        self.screen = screen
        self.tile_size = tile_size
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

    def render(self):
        self.screen.fill((30, 30, 30))
        # Draw buildings
        for b in self.sim.buildings:
            sprite = self.building_sprites.get(b.__class__.__name__)
            if sprite:
                self.screen.blit(sprite, (b.x*self.tile_size, b.y*self.tile_size))
        # Draw creatures
        for c in self.sim.creatures:
            if not getattr(c, "alive", True):
                continue
            trait = c.traits[0] if c.traits else None
            sprite = self.creature_sprites.get(trait)
            if sprite:
                self.screen.blit(sprite, (c.x*self.tile_size, c.y*self.tile_size))
            else:
                pygame.draw.rect(self.screen, (255,255,0), (c.x*self.tile_size, c.y*self.tile_size, self.tile_size, self.tile_size))
        pygame.display.flip()
