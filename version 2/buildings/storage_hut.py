class StorageHut:
    def __init__(self, x, y, owner_id):
        self.x = x
        self.y = y
        self.owner_id = owner_id
        self.contents = {"wood": 0, "food": 0}
        self.capacity = 200

    @staticmethod
    def meets_prerequisites(world, x, y):
        return True  # No terrain or resource requirements

    def tick(self, world):
        pass  # Storage behavior is passive; handled by gatherers and builders

    def store(self, resource_type, amount):
        if sum(self.contents.values()) + amount <= self.capacity:
            self.contents[resource_type] = self.contents.get(resource_type, 0) + amount
            return True
        return False

    def withdraw(self, resource_type, amount):
        if self.contents.get(resource_type, 0) >= amount:
            self.contents[resource_type] -= amount
            return True
        return False
