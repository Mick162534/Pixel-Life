try:
    import matplotlib
    matplotlib.use("Agg")  # ensure headless environments work
    import matplotlib.pyplot as plt
    MATPLOTLIB = True
except Exception:  # matplotlib not available in minimal env
    MATPLOTLIB = False
import pygame
import io

class GraphRenderer:
    def __init__(self, metrics, width, height):
        self.metrics = metrics
        self.width = width
        self.height = height

    def render(self, series_keys=None):
        """Return a pygame Surface with the requested metric series plotted."""
        surface = pygame.Surface((self.width, self.height))
        if not MATPLOTLIB:
            surface.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 24)
            txt = font.render("matplotlib not available", True, (255, 0, 0))
            rect = txt.get_rect(center=(self.width // 2, self.height // 2))
            surface.blit(txt, rect)
            return surface


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
        surface.blit(pygame.transform.scale(image, (self.width, self.height)), (0, 0))
        return surface
