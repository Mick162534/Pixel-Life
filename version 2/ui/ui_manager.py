import pygame

class UIManager:
    def __init__(self, sim, renderer, map_renderer):
        self.sim = sim
        self.renderer = renderer
        self.map_renderer = map_renderer
        self.active_tab = 'Sim'
        self.dragging = False
        self.drag_start = (0, 0)
        self.cam_start = (0, 0)
        self.show_spawn_menu = False
        self.menu_index = 0
        self.species_options = ['gatherer', 'builder', 'herbivore']
        self.font = pygame.font.SysFont(None, 18)

    def handle_event(self, evt):
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_m:
                # toggle map tab
                self.active_tab = 'Map' if self.active_tab != 'Map' else 'Sim'
            elif evt.key == pygame.K_n:
                self.show_spawn_menu = not self.show_spawn_menu
                self.menu_index = 0
            elif self.show_spawn_menu:
                if evt.key == pygame.K_UP:
                    self.menu_index = (self.menu_index - 1) % len(self.species_options)
                elif evt.key == pygame.K_DOWN:
                    self.menu_index = (self.menu_index + 1) % len(self.species_options)
                elif evt.key == pygame.K_RETURN:
                    mods = pygame.key.get_mods()
                    count = 5 if mods & pygame.KMOD_SHIFT else 1
                    species = self.species_options[self.menu_index]
                    for _ in range(count):
                        cx = self.renderer.camera_x + self.renderer.view_tiles_x // 2
                        cy = self.renderer.camera_y + self.renderer.view_tiles_y // 2
                        self.sim.spawn_creature(species, cx, cy)
                    self.show_spawn_menu = False
                elif evt.key == pygame.K_ESCAPE:
                    self.show_spawn_menu = False
            elif evt.key == pygame.K_LEFT:
                self.renderer.camera_x = max(0, self.renderer.camera_x - 1)
            elif evt.key == pygame.K_RIGHT:
                max_x = max(0, self.sim.width - self.renderer.view_tiles_x)
                self.renderer.camera_x = min(max_x, self.renderer.camera_x + 1)
            elif evt.key == pygame.K_UP:
                self.renderer.camera_y = max(0, self.renderer.camera_y - 1)
            elif evt.key == pygame.K_DOWN:
                max_y = max(0, self.sim.height - self.renderer.view_tiles_y)
                self.renderer.camera_y = min(max_y, self.renderer.camera_y + 1)
        elif evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
            self.dragging = True
            self.drag_start = evt.pos
            self.cam_start = (self.renderer.camera_x, self.renderer.camera_y)
        elif evt.type == pygame.MOUSEBUTTONUP and evt.button == 1:
            self.dragging = False
        elif evt.type == pygame.MOUSEMOTION and self.dragging:
            dx = (evt.pos[0] - self.drag_start[0]) // self.renderer.tile_size
            dy = (evt.pos[1] - self.drag_start[1]) // self.renderer.tile_size
            max_x = max(0, self.sim.width - self.renderer.view_tiles_x)
            max_y = max(0, self.sim.height - self.renderer.view_tiles_y)
            self.renderer.camera_x = max(0, min(max_x, self.cam_start[0] - dx))
            self.renderer.camera_y = max(0, min(max_y, self.cam_start[1] - dy))
    def draw(self, screen):
        if self.show_spawn_menu:
            menu_w = 150
            menu_h = 20 * len(self.species_options) + 10
            x, y = 10, 10
            pygame.draw.rect(screen, (0, 0, 0), (x, y, menu_w, menu_h))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, menu_w, menu_h), 1)
            for i, sp in enumerate(self.species_options):
                color = (255, 255, 0) if i == self.menu_index else (255, 255, 255)
                text = self.font.render(sp, True, color)
                screen.blit(text, (x + 5, y + 5 + i * 20))

