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
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_m:
            # toggle map tab
            self.active_tab = 'Map' if self.active_tab != 'Map' else 'Sim'
