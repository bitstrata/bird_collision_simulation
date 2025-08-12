Usage Guide
Running the Simulation

Static mode: python run_simulation.py --mode static --runs 4
Runs 4 parallel simulations and generates collision_results.png.


Dynamic mode: python run_simulation.py --mode dynamic
Launches visualization at http://127.0.0.1:8521.



Testing

Run tests: python -m unittest discover -s tests

Configuration
Edit data/config.json to adjust grid size and number of birds.