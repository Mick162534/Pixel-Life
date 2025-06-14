def builder_behavior(creature, world):
    # Find a building under construction
    for site in world.construction_manager.queue:
        if site["tribe_id"] != creature.owner_id or site["complete"]:
            continue

        x, y = site["x"], site["y"]
        # Move toward site
        if abs(x - creature.x) > 1 or abs(y - creature.y) > 1:
            dx = int((x - creature.x)/abs(x - creature.x)) if creature.x != x else 0
            dy = int((y - creature.y)/abs(y - creature.y)) if creature.y != y else 0
            creature.move(dx, dy)
            return

        # If on site, check for resource requirements (basic: 10 wood)
        needed = 10
        for hut in world.buildings:
            if hut.__class__.__name__ == "StorageHut" and hut.owner_id == creature.owner_id:
                if hut.withdraw("wood", needed):
                    site["progress"] += 1
                    print(f"[BUILD] {creature.name} worked on building at ({x},{y})")
                    return
