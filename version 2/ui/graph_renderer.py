import matplotlib.pyplot as plt
import pygame
import io

class GraphRenderer:
    def __init__(self, metrics, width, height):
        self.metrics = metrics
        self.width = width
        self.height = height

    def render(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        ticks = self.metrics.get_all_ticks()
        trait_keys = self.metrics.get_all_trait_keys()

        # Plot total counts
        ax.plot(ticks, self.metrics.get_series("creature_count"), label="Creatures")
        ax.plot(ticks, self.metrics.get_series("grass_count"), label="Grass")
        ax.plot(ticks, self.metrics.get_series("corpse_count"), label="Corpses")
        ax.plot(ticks, self.metrics.get_series("avg_energy"), label="Avg Energy")

        # Plot traits dynamically
        for trait in trait_keys:
            ax.plot(ticks, self.metrics.get_series(trait), label=trait.title())

        ax.set_title("Simulation Metrics Over Time")
        ax.set_xlabel("Ticks")
        ax.set_ylabel("Value")
        ax.legend()
        buf = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        image = pygame.image.load(buf, 'png')
        surface = pygame.Surface((self.width, self.height))
        surface.blit(pygame.transform.scale(image, (self.width, self.height)), (0, 0))
        return surface
