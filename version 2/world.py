import random
from buildings.communal_center import CommunalCenter
from society.tribe_creator import form_tribes
from society.affinity_system import accumulate_family_affinity
from construction.construction_manager import ConstructionManager
from resources.resource_manager import ResourceManager
from resources.resource_node import ResourceNode
from resources.bush_node import BushNode
from resources.pile_building import PileBuilding
from infrastructure.wall_manager import WallManager
from infrastructure.wall_tile import WallTile
from entities.creature import Creature
from society.tribe import Tribe
from systems.pheromone_map import PheromoneMap
from terrain import TerrainGenerator
from entities.creature_stats import generate_stats

class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.creatures = []
        self.construction_manager = ConstructionManager()
        self.piles = []
        self.bushes = []
        self.resource_manager = ResourceManager()
        self.pheromone_map = PheromoneMap(self.width, self.height)
        self.terrain = TerrainGenerator(self.width, self.height)
        self.wall_manager = WallManager()
        self.wall_targets = []
        self.tribes = []
        self.buildings = []
        self.initialize_environment()

    def initialize_environment(self):
        for _ in range(10):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            tree = ResourceNode(x, y, "wood", amount=100)
            self.resource_manager.add_node(tree)

        for _ in range(6):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            self.bushes.append(BushNode(x, y))

        pile = PileBuilding(self.width//2, self.height//2, owner_id="test_tribe")
        self.piles.append(pile)

        gatherer = Creature("gatherer_1", self.width//2 + 2, self.height//2 + 2,
                            ["gatherer"], generate_stats())
        builder = Creature("builder_1", self.width//2 + 4, self.height//2 + 4,
                           ["builder"], generate_stats())
        deer = Creature("deer_1", self.width//2 - 3, self.height//2 - 3,
                        ["deer", "herbivore"], generate_stats())
        boar = Creature("boar_1", random.randint(0, self.width-1), random.randint(0, self.height-1),
                        ["boar", "herbivore"], generate_stats())
        goat = Creature("goat_1", random.randint(0, self.width-1), random.randint(0, self.height-1),
                        ["goat", "herbivore"], generate_stats())
        bear = Creature("bear_1", random.randint(0, self.width-1), random.randint(0, self.height-1),
                        ["bear", "carnivore"], generate_stats())
        # spawn fish in a random water tile if available
        fx, fy = 0, 0
        water_tiles = [(x, y) for x in range(self.width) for y in range(self.height)
                       if self.terrain.get_tile(x, y) == "water"]
        if water_tiles:
            fx, fy = random.choice(water_tiles)
        fish = Creature("fish_1", fx, fy, ["fish", "herbivore"], generate_stats())
        self.creatures.extend([gatherer, builder, deer, boar, goat, bear, fish])

        tribe = Tribe("tribe_alpha", self.width//2, self.height//2)
        tribe.add_member(gatherer)
        tribe.add_member(builder)
        tribe.add_member(deer)
        self.tribes.append(tribe)

        self.initiate_wall_ring(cx=self.width//2, cy=self.height//2, radius=6)

    def initiate_wall_ring(self, cx, cy, radius):
        for dx in range(-radius, radius+1):
            for dy in [-radius, radius]:
                self.wall_targets.append((cx + dx, cy + dy))
        for dy in range(-radius+1, radius):
            for dx in [-radius, radius]:
                self.wall_targets.append((cx + dx, cy + dy))

    def get_wall_construction_site(self):
        while self.wall_targets:
            x, y = self.wall_targets.pop(0)
            if not self.wall_manager.get_wall(x, y):
                return (x, y)
        return None

    def get_bushes_nearby(self, x, y, radius=5):
        return [b for b in self.bushes if not b.is_depleted and abs(b.x - x) <= radius and abs(b.y - y) <= radius]

    def cleanup_unused_walls(self):
        valid_area = set()
        cx, cy = self.width//2, self.height//2
        radius = 6
        for dx in range(-radius, radius+1):
            for dy in [-radius, radius]:
                valid_area.add((cx + dx, cy + dy))
        for dy in range(-radius+1, radius):
            for dx in [-radius, radius]:
                valid_area.add((cx + dx, cy + dy))

        self.wall_manager.wall_tiles = [w for w in self.wall_manager.wall_tiles if (w.x, w.y) in valid_area]

    def get_creatures_in_range(self, x, y, radius=5):
        """Return all living creatures within the given Manhattan radius."""
        found = []
        for c in self.creatures:
            if not getattr(c, "alive", True):
                continue
            if abs(c.x - x) <= radius and abs(c.y - y) <= radius:
                found.append(c)
        return found

    def spawn_creature(self, species, x, y):
        """Create a new creature with basic stats and the given species trait."""
        species_traits = {
            'gatherer': ['gatherer'],
            'builder': ['builder'],
            'deer': ['deer', 'herbivore'],
            'boar': ['boar', 'herbivore'],
            'goat': ['goat', 'herbivore'],
            'bear': ['bear', 'carnivore'],
            'fish': ['fish', 'herbivore'],
        }
        traits = species_traits.get(species, ['herbivore'])
        cid = f"{species}_{len(self.creatures)+1}"
        stats = generate_stats()
        creature = Creature(cid, x, y, traits, stats)
        self.creatures.append(creature)
        if self.tribes:
            self.tribes[0].add_member(creature)
        return creature

    def spawn_raid_band(self, attacking_tribe, target_tribe):
        """Placeholder for raid band creation used by older tribe logic."""
        pass

    def tick(self):
        # Dynamic tribe formation
        new_tribes = form_tribes(self.creatures, self.tribes)
        accumulate_family_affinity(self.creatures)
        if new_tribes:
            self.tribes.extend(new_tribes)

        self.resource_manager.tick()
        for bush in self.bushes:
            bush.tick()
        for tribe in self.tribes:
            tribe.tick(self)
        for building in self.buildings:
            if isinstance(building, CommunalCenter):
                building.tick(self)
        self.construction_manager.tick(self)
        self.pheromone_map.evaporate()
        for creature in self.creatures:
            creature.tick(self)
        self.cleanup_unused_walls()
