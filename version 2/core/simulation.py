import pygame
from systems.environment import Environment
from systems.corpse_heatmap import CorpseHeatmap
from systems.grass_regenerator import GrassRegenerator
from entities.creature import Creature
from ui.metrics_collector import MetricsCollector
from ui.tab_manager import TabManager
from ui.graph_renderer import GraphRenderer
from systems.affinity_system import calculate_affinity
from systems.tribe import Tribe

class Simulation:
    def __init__(self, width=180, height=180):
        self.width = width
        self.height = height
        self.env = Environment(width, height)
        self.heatmap = CorpseHeatmap(width, height)
        self.regenerator = GrassRegenerator(width, height, tree_coords=[(5, 5), (25, 25), (50, 50)])
        self.metrics = MetricsCollector()
        self.tab_manager = TabManager()
        self.graph_renderer = GraphRenderer(self.metrics, width, height)
        self.creatures = []
        self.tribes = []

        for _ in range(20):
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            traits = random.choices(["herbivore", "predator", "wanderer", "curious", "leader"], k=2)
            self.creatures.append(Creature(x, y, traits=traits))

    def step(self):
        self.heatmap.update()
        self.regenerator.update(self.env, self.heatmap)
        new_creatures = []

        for c in self.creatures:
            c.tick(self.env, self.creatures)
            c.move(self.env)
            nearby = [o for o in self.creatures if abs(o.x - c.x) <= 2 and abs(o.y - c.y) <= 2 and o.id != c.id]
            c.reproduce(self.env, new_creatures, nearby)

        self.creatures.extend(new_creatures)

        # Update affinities
        for a in self.creatures:
            for b in self.creatures:
                if a.id != b.id:
                    aff = calculate_affinity(a, b)
                    if aff > 0:
                        a.affinities[b.id] = aff

        # Form tribes from unassigned creatures with strong mutual affinity
        untribed = [c for c in self.creatures if not c.tribe_id]
        random.shuffle(untribed)
        for i in range(len(untribed)):
            if untribed[i].stats["intelligence"] < 13 or untribed[i].stats["social_drive"] < 12:
                continue
            c1 = untribed[i]
            compatible = []
            for c2 in untribed:
                if c2.id != c1.id and c1.affinities.get(c2.id, 0) > 15 and c2.affinities.get(c1.id, 0) > 15:
                    compatible.append(c2)
            if len(compatible) >= 2:
                group = [c1] + compatible[:3]
                new_tribe = Tribe(group)
                for m in group:
                    m.tribe_id = new_tribe.id
                self.tribes.append(new_tribe)

        for tribe in self.tribes:
            tribe.update(self.creatures)

        self.metrics.record(len(self.metrics.tick_data), self.creatures, self.env, self.heatmap)
