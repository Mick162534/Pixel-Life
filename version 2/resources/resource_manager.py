class ResourceManager:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_nearby_nodes(self, x, y, radius, resource_type=None):
        result = []
        for node in self.nodes:
            if node.is_depleted:
                continue
            if resource_type and node.resource_type != resource_type:
                continue
            dx = node.x - x
            dy = node.y - y
            if dx * dx + dy * dy <= radius * radius:
                result.append(node)
        return result

    def tick(self):
        for node in self.nodes:
            node.tick()
