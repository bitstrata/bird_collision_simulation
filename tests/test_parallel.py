import geopandas as gpd
from shapely.geometry import Point
from src.agents import Agent
from src.parallel import step_parallel
from src.bayesian import bayesian_update

def test_step_parallel_runs():
    agents = [Agent((0,0)) for _ in range(5)]
    turbine_gdf = gpd.GeoDataFrame({"collision_zone": [Point(5,5).buffer(1)]})
    wind_direction = (1,0)
    updated_agents, posterior = step_parallel(
        agents, turbine_gdf, wind_direction, 0.5, bayesian_update
    )
    assert len(updated_agents) == 5
    assert 0 <= posterior <= 1
