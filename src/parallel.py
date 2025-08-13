from joblib import Parallel, delayed
import multiprocessing
from shapely.geometry import Point

def agent_worker(agent, turbine_geoms, turbine_sindex, wind_direction):
    agent.move(wind_direction)
    pt = Point(agent.pos)
    hit = False
    for idx in turbine_sindex.intersection(pt.bounds):
        if turbine_geoms[idx].contains(pt):
            hit = True
            agent.alive = False
            break
    agent.energy -= 1
    return agent, hit

def step_parallel(agents, turbine_manager, wind_direction, prior_prob, bayesian_func):
    n_jobs = max(1, multiprocessing.cpu_count() - 1)
    results = Parallel(n_jobs=n_jobs, backend="loky")(
        delayed(agent_worker)(
            agent,
            turbine_manager.geoms,
            turbine_manager.sindex,
            wind_direction
        )
        for agent in agents
    )
    updated_agents, hits = zip(*results)
    posterior = bayesian_func(prior_prob, sum(hits), len(hits))
    return list(updated_agents), posterior
