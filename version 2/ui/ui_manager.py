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

    def handle_event(self, evt):
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_m:
                # toggle map tab
                self.active_tab = 'Map' if self.active_tab != 'Map' else 'Sim'
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
