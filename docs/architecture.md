Code Architecture

src/config_loader.py: Loads simulation parameters from data/config.json.
src/agent.py: Defines BirdAgent with movement and collision logic.
src/turbine.py: Defines TurbineAgent and loads turbine data from GeoJSON.
src/simulation.py: Core BirdCollisionSimulation model using Mesa.
src/bayesian.py: Bayesian updates for collision probabilities.
src/parallel.py: Parallel execution of simulation runs.
src/utils.py: Plotting and utility functions.
run_simulation.py: Entry point with static and dynamic modes.
