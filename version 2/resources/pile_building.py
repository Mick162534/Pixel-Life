class PileBuilding:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id
        self.storage = {"wood": 0, "food": 0}

    def deposit(self, resource_type, amount):
        if resource_type in self.storage:
            self.storage[resource_type] += amount
        else:
            self.storage[resource_type] = amount
