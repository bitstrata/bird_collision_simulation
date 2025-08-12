from .agent import Agent
from .turbine_manager import TurbineManager
from .parallel import step_parallel
from .bayesian import bayesian_update

class Simulation:
    def __init__(self, config):
        self.wind_direction = config.get("wind_direction")
        self.prior_prob = config.get("prior_collision_probability")
        self.num_agents = config.get("num_agents")
        self.initial_energy = config.get("initial_energy")

        self.turbines = TurbineManager(
            config.get("turbine_file"),
            config.get("collision_zone_buffer")
        )
        self.agents = [Agent((0, 0), self.initial_energy) for _ in range(self.num_agents)]

    def step(self):
        self.agents, self.prior_prob = step_parallel(
            self.agents,
            self.turbines,
            self.wind_direction,
            self.prior_prob,
            bayesian_update
        )

    def run(self, steps=10):
        for _ in range(steps):
            self.step()
        return self.prior_prob
