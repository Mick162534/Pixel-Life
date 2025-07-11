import pygame

class MapRenderer:
    def __init__(self, sim, renderer, screen, map_rect=(10,10,200,200)):
        self.sim = sim
        self.renderer = renderer
        self.screen = screen
        self.map_rect = pygame.Rect(map_rect)

    def render(self):
        # semi-transparent overlay
        s = pygame.Surface((self.map_rect.width, self.map_rect.height), pygame.SRCALPHA)
        s.fill((0,0,0,180))
        self.screen.blit(s, (self.map_rect.x, self.map_rect.y))
        # simple mini-map of creature positions
        cw = self.map_rect.width / self.sim.width
        ch = self.map_rect.height / self.sim.height
        # draw simple terrain colors
        for x in range(self.sim.width):
            for y in range(self.sim.height):
                tile = self.sim.terrain.get_tile(x, y)
                if tile == "grass":
                    color = (34, 139, 34)
                elif tile == "shallow_water":
                    color = (173, 216, 230)
                elif tile == "deep_water":
                    color = (0, 0, 139)
                else:
                    color = (139, 69, 19)

                pygame.draw.rect(
                    self.screen,
                    color,
                    (self.map_rect.x + x * cw, self.map_rect.y + y * ch, cw, ch)
                )

        for c in self.sim.creatures:
            if not getattr(c, "alive", True):
                continue
            trait = c.traits[0] if c.traits else "herbivore"
            color = self.renderer.creature_sprites.get(trait)
            if isinstance(color, pygame.Surface):
                color = color.get_at((0, 0))
            else:
                color = (255, 255, 0)
            pygame.draw.rect(
                self.screen,
                color,
                (self.map_rect.x + c.x * cw, self.map_rect.y + c.y * ch, cw, ch),
            )
        # show camera viewport
        rect_w = self.renderer.view_tiles_x * cw
        rect_h = self.renderer.view_tiles_y * ch
        cam_rect = pygame.Rect(
            self.map_rect.x + self.renderer.camera_x * cw,
            self.map_rect.y + self.renderer.camera_y * ch,
            rect_w,
            rect_h,
        )
        pygame.draw.rect(self.screen, (255,255,0), cam_rect, 1)
