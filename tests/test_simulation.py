import pytest
from src.simulation import Simulation

@pytest.fixture
def config(tmp_path):
    turbine_file = tmp_path / "turbines.geojson"
    turbine_file.write_text('{"type": "FeatureCollection", "features": []}')
    return {
        "wind_direction": [1, 0],
        "num_agents": 5,
        "initial_prob": 0.5,
        "turbine_file": str(turbine_file)
    }

def test_simulation_runs(config):
    sim = Simulation(config)
    result = sim.run(steps=2)
    assert 0 <= result <= 1
