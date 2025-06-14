import random
from creature_behavior.guard import guard_behavior
from systems.flocking import compute_flock_direction
from systems.memory import Memory

class Creature:
    def __init__(self, id, x, y, traits, stats):
        self.id = id
        self.x = x
        self.y = y
        self.traits = traits
        self.stats = stats
        self.memory = Memory(capacity=10) if "has_memory" in self.traits else None
        self.world_context = None  # Will be set each tick
        self.energy = 100
        self.hunger = 100
        self.alive = True
        self.carrying = None
        self.target_node = None
        self.target_pile = None
        self.build_target = None
        self.build_timer = 0
        self.eating = False

    def tick(self, world):
        # Guard behavior
        if 'guard' in self.traits:
            if guard_behavior(self, world):
                return

        # record presence and deposit pheromone
        if self.memory is not None:
            self.memory.add('presence', (self.x, self.y))
        if "pheromone_emitter" in self.traits:
            world.pheromone_map.deposit(self.x, self.y, amount=0.1)
        
        if not self.alive:
            return
        self.hunger -= 0.5
        self.energy -= 0.2
        if self.hunger <= 0 or self.energy <= 0:
            self.alive = False
            return

        if self.hunger < 50:
            self.eat_logic(world)
        elif "gatherer" in self.traits:
            self.gather_logic(world)
        elif "builder" in self.traits:
            self.builder_logic(world)

    def eat_logic(self, world):
        if self.target_node:
            if abs(self.target_node.x - self.x) <= 1 and abs(self.target_node.y - self.y) <= 1:
                eaten = self.target_node.harvest(10)
                if eaten > 0:
                    self.hunger = min(100, self.hunger + eaten * 2)
                    self.energy = min(100, self.energy + eaten)
                    self.target_node = None
            else:
                self.move_towards(self.target_node.x, self.target_node.y)
        else:
            bushes = world.get_bushes_nearby(self.x, self.y)
            if bushes:
                self.target_node = random.choice(bushes)

    def gather_logic(self, world):
        if self.carrying:
            if not self.target_pile:
                self.target_pile = min(world.piles, key=lambda p: (p.x - self.x)**2 + (p.y - self.y)**2, default=None)
            if self.target_pile:
                if abs(self.target_pile.x - self.x) <= 1 and abs(self.target_pile.y - self.y) <= 1:
                    self.target_pile.deposit(self.carrying[0], self.carrying[1])
                    self.carrying = None
                    self.target_pile = None
                else:
                    self.move_towards(self.target_pile.x, self.target_pile.y)
        else:
            if not self.target_node:
                nearby = world.resource_manager.get_nearby_nodes(self.x, self.y, radius=5, resource_type="wood")
                if nearby:
                    self.target_node = random.choice(nearby)
            if self.target_node:
                if abs(self.target_node.x - self.x) <= 1 and abs(self.target_node.y - self.y) <= 1:
                    harvested = self.target_node.harvest(10)
                    if harvested > 0:
                        self.carrying = ("wood", harvested)
                        self.target_node = None
                else:
                    self.move_towards(self.target_node.x, self.target_node.y)

    def builder_logic(self, world):
        if self.build_target:
            bx, by = self.build_target
            if self.x == bx and self.y == by:
                if self.build_timer <= 0:
                    world.wall_manager.add_wall(bx, by, owner_id="test_tribe")
                    self.build_target = None
                    self.build_timer = 10
                else:
                    self.build_timer -= 1
            else:
                self.move_towards(bx, by)
        else:
            target = world.get_wall_construction_site()
            if target:
                self.build_target = target

    def move_towards(self, tx, ty):
        dx = tx - self.x
        dy = ty - self.y
        self.x += 1 if dx > 0 else -1 if dx < 0 else 0
        self.y += 1 if dy > 0 else -1 if dy < 0 else 0
