import random

class RaidFSM:
    def __init__(self, target_tribe_id):
        self.state = "Traveling"
        self.target_tribe_id = target_tribe_id

    def tick(self, band, world):
        if self.state == "Traveling":
            if band.is_near_target(world):
                self.state = "Attacking"
        elif self.state == "Attacking":
            enemies = band.find_enemies(world)
            if not enemies:
                self.state = "Returning"
            else:
                band.attack(enemies)
        elif self.state == "Returning":
            if band.is_home():
                self.state = "Idle"

class Band:
    def __init__(self, members, home_chunk, target_tribe_id):
        self.members = members
        self.home_chunk = home_chunk
        self.target_tribe_id = target_tribe_id
        self.fsm = RaidFSM(target_tribe_id)

    def tick(self, world):
        self.fsm.tick(self, world)

    def is_near_target(self, world):
        for m in self.members:
            for tribe in world.tribes:
                if tribe.tribe_id == self.fsm.target_tribe_id:
                    for cx, cy in tribe.territory_chunks:
                        if abs(m.chunk_x - cx) + abs(m.chunk_y - cy) <= 1:
                            return True
        return False

    def is_home(self):
        for m in self.members:
            if (m.chunk_x, m.chunk_y) == self.home_chunk:
                return True
        return False

    def find_enemies(self, world):
        enemies = []
        for m in self.members:
            visible = world.get_creatures_in_range(m.x, m.y, radius=5)
            for other in visible:
                if other.owner_id != m.owner_id:
                    enemies.append(other)
        return enemies

    def attack(self, enemies):
        for m in self.members:
            if enemies:
                target = random.choice(enemies)
                m.attack(target)
