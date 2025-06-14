class ConstructionManager:
    def __init__(self):
        self.queue = []  # Each item: (x, y, building_type, tribe_id, progress)

    def request_construction(self, x, y, building_type, tribe_id):
        self.queue.append({"x": x, "y": y, "type": building_type, "tribe_id": tribe_id, "progress": 0})

    def tick(self, world):
        completed = []
        for site in self.queue:
            builders = [c for c in world.creatures if c.alive and "builder" in c.traits and c.owner_id == site["tribe_id"]]
            if not builders:
                continue

            site["progress"] += len(builders)  # Each builder adds 1 point
            if site["progress"] >= 10:
                completed.append(site)

        for site in completed:
            self.queue.remove(site)
            self.place_building(world, site)

    def place_building(self, world, site):
        x, y, tribe_id, b_type = site["x"], site["y"], site["tribe_id"], site["type"]
        from buildings.logging_camp import LoggingCamp
        from buildings.farm import Farm
        from buildings.construction_yard import ConstructionYard
        from buildings.taming_pen import TamingPen
        from buildings.watchtower import Watchtower
        from buildings.research_hut import ResearchHut

        new_building = None
        if b_type == "logging_camp":
            new_building = LoggingCamp(x, y, tribe_id)
        elif b_type == "farm":
            new_building = Farm(x, y, tribe_id)
        elif b_type == "construction_yard":
            new_building = ConstructionYard(x, y, tribe_id)
        elif b_type == "taming_pen":
            new_building = TamingPen(x, y, tribe_id)
        elif b_type == "watchtower":
            new_building = Watchtower(x, y, tribe_id)
                elif b_type == "den":
            from buildings.den import Den
            new_building = Den(x, y, tribe_id)
        elif b_type == "research_hut":
            new_building = ResearchHut(x, y, tribe_id)

        if new_building:
            world.buildings.append(new_building)
            print(f"[BUILD] Tribe {tribe_id} completed: {b_type} at ({x}, {y})")
