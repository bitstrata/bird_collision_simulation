def bayesian_update(prior, hits, total):
    if total == 0:
        return prior
    likelihood_collision = hits / total
    likelihood_no_collision = 1 - likelihood_collision
    return (likelihood_collision * prior) / (
        likelihood_collision * prior +
        likelihood_no_collision * (1 - prior)
    )
