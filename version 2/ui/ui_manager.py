import pygame
from ui.tab_manager import TabManager

class UIManager:
    def __init__(self, sim, renderer, map_renderer, metrics, graph_renderer):
        self.sim = sim
        self.renderer = renderer
        self.map_renderer = map_renderer
        self.metrics = metrics
        self.graph_renderer = graph_renderer
        self.tab_manager = TabManager()
        self.show_map = False
        self.show_spawn_menu = False
        self.spawn_index = 0
        self.species_options = ['gatherer', 'builder', 'deer', 'boar', 'goat', 'bear', 'fish']
        self.metric_menu = False
        self.metric_index = 0
        self.selected_metric = 'creature_count'
        self.font = pygame.font.SysFont(None, 18)
        self.dragging = False
        self.drag_start = (0, 0)
        self.cam_start = (0, 0)
        self.paused = False
        self.speed = 1

    @property
    def active_tab(self):
        return self.tab_manager.active_tab

    def handle_event(self, evt):
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_TAB:
                self.tab_manager.toggle()
            elif evt.key == pygame.K_m:
                self.show_map = not self.show_map
            elif evt.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif evt.key in (pygame.K_EQUALS, pygame.K_PLUS):
                self.speed = min(5, self.speed + 1)
            elif evt.key == pygame.K_MINUS:
                self.speed = max(1, self.speed - 1)
            elif evt.key == pygame.K_n and self.active_tab == 'SIM':
                self.show_spawn_menu = not self.show_spawn_menu
                self.spawn_index = 0
            elif self.show_spawn_menu:
                if evt.key == pygame.K_UP:
                    self.spawn_index = (self.spawn_index - 1) % len(self.species_options)
                elif evt.key == pygame.K_DOWN:
                    self.spawn_index = (self.spawn_index + 1) % len(self.species_options)
                elif evt.key == pygame.K_RETURN:
                    mods = pygame.key.get_mods()
                    count = 5 if mods & pygame.KMOD_SHIFT else 1
                    species = self.species_options[self.spawn_index]

                    for _ in range(count):
                        cx = self.renderer.camera_x + self.renderer.view_tiles_x // 2
                        cy = self.renderer.camera_y + self.renderer.view_tiles_y // 2
                        self.sim.spawn_creature(species, cx, cy)
                    self.show_spawn_menu = False
                elif evt.key == pygame.K_ESCAPE:
                    self.show_spawn_menu = False
            elif self.active_tab == 'GRAPH' and evt.key == pygame.K_d:
                self.metric_menu = not self.metric_menu
                self.metric_index = 0
            elif self.metric_menu:
                metrics = self.available_metrics()
                if evt.key == pygame.K_UP:
                    self.metric_index = (self.metric_index - 1) % len(metrics)
                elif evt.key == pygame.K_DOWN:
                    self.metric_index = (self.metric_index + 1) % len(metrics)
                elif evt.key == pygame.K_RETURN:
                    self.selected_metric = metrics[self.metric_index]
                    self.metric_menu = False
                elif evt.key == pygame.K_ESCAPE:
                    self.metric_menu = False

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

    def available_metrics(self):
        base = ['creature_count', 'resource_nodes', 'bush_nodes', 'avg_energy']
        return base + self.metrics.get_all_trait_keys()

    def draw(self, screen):
        # draw tab headers
        sim_color = (255, 255, 0) if self.active_tab == 'SIM' else (200, 200, 200)
        graph_color = (255, 255, 0) if self.active_tab == 'GRAPH' else (200, 200, 200)
        sim_text = self.font.render('SIM', True, sim_color)
        graph_text = self.font.render('GRAPH', True, graph_color)
        screen.blit(sim_text, (10, 5))
        screen.blit(graph_text, (60, 5))

        # status info
        status = f'Speed: {self.speed}x'
        if self.paused:
            status += ' (Paused)'
        status_surf = self.font.render(status, True, (255, 255, 255))
        screen.blit(status_surf, (150, 5))

        if self.show_map:
            self.map_renderer.render()

        if self.active_tab == 'GRAPH':
            graph = self.graph_renderer.render([self.selected_metric])
            screen.blit(graph, (0, 30))
            if self.metric_menu:
                opts = self.available_metrics()
                menu_w = 150
                menu_h = 20 * len(opts) + 10
                x = screen.get_width() - menu_w - 10
                y = 40
                pygame.draw.rect(screen, (0, 0, 0), (x, y, menu_w, menu_h))
                pygame.draw.rect(screen, (255, 255, 255), (x, y, menu_w, menu_h), 1)
                for i, opt in enumerate(opts):
                    color = (255, 255, 0) if i == self.metric_index else (255, 255, 255)
                    text = self.font.render(opt, True, color)
                    screen.blit(text, (x + 5, y + 5 + i * 20))
        elif self.show_spawn_menu:
            menu_w = 150
            menu_h = 20 * len(self.species_options) + 10
            x, y = 10, 30
            pygame.draw.rect(screen, (0, 0, 0), (x, y, menu_w, menu_h))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, menu_w, menu_h), 1)
            for i, sp in enumerate(self.species_options):
                color = (255, 255, 0) if i == self.spawn_index else (255, 255, 255)

                text = self.font.render(sp, True, color)
                screen.blit(text, (x + 5, y + 5 + i * 20))
