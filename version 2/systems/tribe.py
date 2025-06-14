import uuid
import random

class Tribe:
    def __init__(self, members):
        self.id = uuid.uuid4()
        self.members = set(m.id for m in members)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.leader_id = max(members, key=lambda m: m.stats.get("charisma", 10)).id

    def add_member(self, creature):
        self.members.add(creature.id)

    def remove_member(self, creature):
        self.members.discard(creature.id)

    def update(self, all_creatures):
        # Optional: update leader or shared goals
        pass
