from systems.affinity_system import calculate_affinity

def accumulate_family_affinity(creatures):
    """Update each creature's affinity dictionary using calculate_affinity."""
    for c in creatures:
        if not hasattr(c, "affinities"):
            c.affinities = {}
    for i, a in enumerate(creatures):
        for b in creatures[i+1:]:
            aff = calculate_affinity(a, b)
            if aff > 0:
                a.affinities[b.id] = aff
                b.affinities[a.id] = aff
