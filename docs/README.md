Bird Collision Simulation Documentation
Overview
This project simulates bird collisions with wind turbines using Mesa for agent-based modeling. Birds move randomly in a continuous 2D space, and turbines are fixed with collision radii. Bayesian updates adjust collision risks, and parallel execution supports multiple runs.
Setup Instructions

Clone the repository: git clone https://github.com/<your-username>/bird_collision_simulation.git
Create virtual environment: python3 -m venv .venv
Activate: source .venv/bin/activate
Install dependencies: pip install -r requirements.txt
Run simulation:
Static mode: python run_simulation.py --mode static --runs 4
Dynamic mode: python run_simulation.py --mode dynamic



Configuration

data/config.json: Set grid_width, grid_height, num_birds.
data/turbines.geojson: Turbine locations (GeoJSON format).

Output

Static: Generates collision_results.png.
Dynamic: Web interface at http://127.0.0.1:8521 with grid and collision chart.
