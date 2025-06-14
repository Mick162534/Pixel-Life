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
            cx, cy = self.renderer.camera_chunk_x, self.renderer.camera_chunk_y
            if evt.key == pygame.K_LEFT and cx > 0:
                cx -= 1
            elif evt.key == pygame.K_RIGHT and cx < self.sim.chunk_manager.max_chunks_x - 1:
                cx += 1
            elif evt.key == pygame.K_UP and cy > 0:
                cy -= 1
            elif evt.key == pygame.K_DOWN and cy < self.sim.chunk_manager.max_chunks_y - 1:
                cy += 1
            self.renderer.camera_chunk_x, self.renderer.camera_chunk_y = cx, cy
            self.sim.camera_chunk = (cx, cy)

        elif evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
            self.dragging = True
            self.drag_start = evt.pos
            self.cam_start = (self.renderer.camera_chunk_x, self.renderer.camera_chunk_y)
        elif evt.type == pygame.MOUSEBUTTONUP and evt.button == 1:
            self.dragging = False
        elif evt.type == pygame.MOUSEMOTION and self.dragging:
            dx = (evt.pos[0] - self.drag_start[0]) // (self.renderer.tile_size * self.renderer.chunk_size)
            dy = (evt.pos[1] - self.drag_start[1]) // (self.renderer.tile_size * self.renderer.chunk_size)
            cx = max(0, min(self.sim.chunk_manager.max_chunks_x-1, self.cam_start[0] - dx))
            cy = max(0, min(self.sim.chunk_manager.max_chunks_y-1, self.cam_start[1] - dy))
            self.renderer.camera_chunk_x, self.renderer.camera_chunk_y = cx, cy
            self.sim.camera_chunk = (cx, cy)
