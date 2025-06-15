import matplotlib.pyplot as plt
import pygame
import io

class GraphRenderer:
    def __init__(self, metrics, width, height):
        self.metrics = metrics
        self.width = width
        self.height = height

    def render(self, series_keys=None):
        """Return a pygame Surface with the requested metric series plotted."""
        fig, ax = plt.subplots(figsize=(6, 4))
        ticks = self.metrics.get_all_ticks()
        if series_keys is None:
            series_keys = ["creature_count"]

        for key in series_keys:
            ax.plot(ticks, self.metrics.get_series(key), label=key.replace("_", " ").title())

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
