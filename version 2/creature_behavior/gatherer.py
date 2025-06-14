def gatherer_behavior(creature, world):
    if creature.carrying:
        # Try to deliver to nearest storage hut
        huts = [b for b in world.buildings if b.__class__.__name__ == "StorageHut" and b.owner_id == creature.owner_id]
        if huts:
            closest = min(huts, key=lambda h: abs(h.x - creature.x) + abs(h.y - creature.y))
            if abs(closest.x - creature.x) <= 1 and abs(closest.y - creature.y) <= 1:
                success = closest.store(creature.carrying_type, creature.carrying)
                if success:
                    print(f"[DELIVER] {creature.name} stored {creature.carrying} {creature.carrying_type} at hut ({closest.x},{closest.y})")
                    creature.carrying = 0
                    creature.carrying_type = None
                return
            else:
                dx = int((closest.x - creature.x)/abs(closest.x - creature.x)) if creature.x != closest.x else 0
                dy = int((closest.y - creature.y)/abs(closest.y - creature.y)) if creature.y != closest.y else 0
                creature.move(dx, dy)
                return
    else:
        # Search for resource to gather
        resource_nodes = [n for n in world.resource_manager.nodes if n.resource_type in ["wood", "food"]]
        if resource_nodes:
            closest = min(resource_nodes, key=lambda n: abs(n.x - creature.x) + abs(n.y - creature.y))
            if abs(closest.x - creature.x) <= 1 and abs(closest.y - creature.y) <= 1:
                harvested = closest.harvest(5)
                if harvested > 0:
                    creature.carrying = harvested
                    creature.carrying_type = closest.resource_type
            else:
                dx = int((closest.x - creature.x)/abs(closest.x - creature.x)) if creature.x != closest.x else 0
                dy = int((closest.y - creature.y)/abs(closest.y - creature.y)) if creature.y != closest.y else 0
                creature.move(dx, dy)
