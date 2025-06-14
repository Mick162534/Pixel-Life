import pygame, sys
from world import World
from ui.sim_renderer import SimRenderer
from ui.map_renderer import MapRenderer
from ui.ui_manager import UIManager

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # initialize a reasonably sized world so environment generation succeeds
    sim = World(50, 50)
    renderer = SimRenderer(sim, screen)
    map_renderer = MapRenderer(sim, screen)
    ui = UIManager(sim, renderer, map_renderer)

    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            ui.handle_event(evt)

        if ui.active_tab != 'Map':
            sim.tick()
        renderer.render()
        if ui.active_tab == 'Map':
            map_renderer.render()

        clock.tick(30)

if __name__ == "__main__":
    main()
