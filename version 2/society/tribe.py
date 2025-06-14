from research.research_manager import ResearchManager
from random import randint

class Tribe:
    def __init__(self, id, center_x, center_y):
        self.morale = 50  # 0-100

        self.id = id
        self.center_x = center_x
        self.center_y = center_y
        self.members = []
        # Track tiles making up the tribe's claimed territory
        self.territory_chunks = set()
        self.territory_radius = 6
        self.known_resources = []
        self.known_piles = []
        self.research = ResearchManager(self.id)
        self.building_cooldown = 0
        # Initial territory centered on the tribe location
        self.expand_territory_placeholder()

    def expand_territory_placeholder(self):
        """Seed territory with the center tile so other checks don't fail."""
        self.territory_chunks.add((self.center_x, self.center_y))

    def add_member(self, creature):
        self.members.append(creature)

    def tick(self, world):
        # Morale decay
        self.morale = max(0, self.morale - 0.1)

        if len(self.members) > self.territory_radius * 2:
            self.territory_radius += 1
            self.expand_territory(world)

        self.known_resources = world.resource_manager.nodes
        self.known_piles = world.piles

        self.research.tick(self, world)

        if self.building_cooldown > 0:
            self.building_cooldown -= 1

        # Attempt to request a new building every 50 ticks
        if self.building_cooldown == 0 and self.research.unlocked:
            options = list(self.research.unlocked)
            if options:
                choice = options[randint(0, len(options)-1)]
                tx, ty = self.center_x + randint(-5, 5), self.center_y + randint(-5, 5)
                world.construction_manager.request_construction(tx, ty, choice, self.id)
                print(f"[QUEUE] Tribe {self.id} queued: {choice} at ({tx},{ty})")
                self.building_cooldown = 50

        for member in self.members:
            if not member.alive:
                continue
            if "builder" in member.traits:
                # Builder role: will help with construction
                continue
            if "gatherer" in member.traits and not member.carrying:
                continue

    def expand_territory(self, world):
        cx, cy = self.center_x, self.center_y
        r = self.territory_radius
        self.territory_chunks.add((cx, cy))
        for dx in range(-r, r+1):
            for dy in [-r, r]:
                world.wall_targets.append((cx + dx, cy + dy))
        for dy in range(-r+1, r):
            for dx in [-r, r]:
                world.wall_targets.append((cx + dx, cy + dy))

    def territory_tiles(self):
        tiles = []
        for cx, cy in self.territory_chunks:
            tiles.extend([(x, y) for x in range(cx*20, cx*20+20) for y in range(cy*20, cy*20+20)])
        return tiles
