import math

def compute_flock_direction(creature, world,
                            neighbor_radius=5,
                            separation_radius=2,
                            weight_cohesion=1.0,
                            weight_separation=1.5,
                            weight_pheromone=1.0):
    """Compute a movement vector based on flocking and pheromones."""
    neighbors = []
    for other in world.creatures:
        if other.id == creature.id:
            continue
        dx = other.x - creature.x
        dy = other.y - creature.y
        dist = math.hypot(dx, dy)
        if dist <= neighbor_radius:
            neighbors.append((other, dx, dy, dist))

    vec_x, vec_y = 0.0, 0.0

    # Cohesion: move toward average position of neighbors
    if neighbors:
        avg_dx = sum(dx for _, dx, _, _ in neighbors) / len(neighbors)
        avg_dy = sum(dy for _, _, dy, _ in neighbors) / len(neighbors)
        length = math.hypot(avg_dx, avg_dy)
        if length:
            vec_x += weight_cohesion * (avg_dx / length)
            vec_y += weight_cohesion * (avg_dy / length)

    # Separation: move away from too-close neighbors
    sep_x, sep_y = 0.0, 0.0
    for other, dx, dy, dist in neighbors:
        if dist < separation_radius and dist > 0:
            sep_x -= dx / dist
            sep_y -= dy / dist
    length = math.hypot(sep_x, sep_y)
    if length:
        vec_x += weight_separation * (sep_x / length)
        vec_y += weight_separation * (sep_y / length)

    # Pheromone attraction: move toward highest pheromone area
    best_intensity = world.pheromone_map.get_intensity(creature.x, creature.y, radius=neighbor_radius)
    pher_dx, pher_dy = 0.0, 0.0
    for dy in range(-neighbor_radius, neighbor_radius+1):
        for dx in range(-neighbor_radius, neighbor_radius+1):
            xx, yy = creature.x + dx, creature.y + dy
            if 0 <= xx < world.width and 0 <= yy < world.height:
                intensity = world.pheromone_map.map[yy][xx]
                if intensity > best_intensity:
                    best_intensity = intensity
                    pher_dx, pher_dy = dx, dy
    length = math.hypot(pher_dx, pher_dy)
    if length:
        vec_x += weight_pheromone * (pher_dx / length)
        vec_y += weight_pheromone * (pher_dy / length)

    # No movement if zero vector
    if vec_x == 0 and vec_y == 0:
        return 0, 0

    # Normalize and convert to step of size 1
    step_x = 1 if vec_x > 0 else -1 if vec_x < 0 else 0
    step_y = 1 if vec_y > 0 else -1 if vec_y < 0 else 0
    return step_x, step_y
