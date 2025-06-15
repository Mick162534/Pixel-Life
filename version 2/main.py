import pygame, sys
from world import World
from ui.sim_renderer import SimRenderer
from ui.map_renderer import MapRenderer
from ui.ui_manager import UIManager
from ui.metrics_collector import MetricsCollector
from ui.graph_renderer import GraphRenderer

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # initialize a reasonably sized world so environment generation succeeds
    sim = World(50, 50)
    renderer = SimRenderer(sim, screen)
    map_renderer = MapRenderer(sim, renderer, screen)
    metrics = MetricsCollector()
    graph_renderer = GraphRenderer(metrics, WIDTH, HEIGHT - 30)
    ui = UIManager(sim, renderer, map_renderer, metrics, graph_renderer)
    tick = 0

    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            ui.handle_event(evt)

        if not ui.paused:
            for _ in range(ui.speed):
                sim.tick()
                metrics.record(tick, sim)
                tick += 1

        renderer.render()
        if ui.show_map:
            map_renderer.render()
        ui.draw(screen)
        pygame.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    main()
