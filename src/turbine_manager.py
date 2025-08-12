import geopandas as gpd
from shapely.geometry import Point
import random

class TurbineManager:
    def __init__(self, config):
        self.config = config

        if self.config["turbine_file"]:
            self.geoms = gpd.read_file(self.config["turbine_file"])
        else:
            self.geoms = self.generate_layout()

        self.sindex = self.geoms.sindex

    def generate_layout(self):
        layout_type = self.config.get("turbine_layout", "grid")
        random.seed(self.config["random_seed"])
        turbines = []

        if layout_type == "grid":
            spacing = self.config.get("grid_spacing", 15)
            width = self.config.get("farm_width", 3)
            height = self.config.get("farm_height", 4)
            for i in range(width):
                for j in range(height):
                    x = i * spacing
                    y = j * spacing
                    turbines.append(Point(x, y))

        elif layout_type == "random":
            for _ in range(self.config.get("num_turbines", 12)):
                x = random.uniform(0, 100)
                y = random.uniform(0, 100)
                turbines.append(Point(x, y))

        return gpd.GeoDataFrame(geometry=turbines, crs="EPSG:4326")
