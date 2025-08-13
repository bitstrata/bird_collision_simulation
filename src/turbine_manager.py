# src/turbine_manager.py

import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import os
import warnings


class TurbineManager:
    def __init__(self, config):
        """
        Initialize the turbine manager.

        Args:
            config (dict): Simulation configuration dictionary.
        """
        self.config = config
        self.gdf = None
        self.sindex = None
        self.geoms = None

        np.random.seed(self.config.get("random_seed", 42))

        if self.config.get("turbine_file") and os.path.exists(self.config["turbine_file"]):
            self._load_from_file(self.config["turbine_file"])
        else:
            self._generate_turbines()

        # Ensure projected CRS before buffering
        if self.gdf.crs is None or self.gdf.crs.is_geographic:
            warnings.warn(
                "Input geometries are in geographic coordinates; "
                "reprojecting to EPSG:3857 for buffer operations."
            )
            self.gdf = self.gdf.set_crs(epsg=4326, allow_override=True).to_crs(epsg=3857)

        # Create collision zone
        buffer_distance = self.config.get("collision_zone_buffer", 5.0)
        self.gdf["collision_zone"] = self.gdf.geometry.buffer(buffer_distance)

        # Spatial index for collision checks
        self.sindex = self.gdf.sindex
        self.geoms = self.gdf.geometry.values

    def _load_from_file(self, file_path):
        """Load turbines from a GeoJSON or Shapefile."""
        self.gdf = gpd.read_file(file_path)
        print(f"Loaded {len(self.gdf)} turbines from {file_path}")

    def _generate_turbines(self):
        """Generate turbines based on config parameters."""
        num_turbines = self.config.get("num_turbines", 12)
        layout = self.config.get("turbine_layout", "grid")  # grid | random | optimized

        if layout == "grid":
            points = self._generate_grid(num_turbines)
        elif layout == "random":
            points = self._generate_random(num_turbines)
        elif layout == "optimized":
            points = self._optimize_layout(num_turbines)
        else:
            raise ValueError(f"Unknown turbine layout: {layout}")

        self.gdf = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")
        print(f"Generated {num_turbines} turbines using '{layout}' layout.")

    def _generate_grid(self, num_turbines):
        """Generate turbines in a simple square grid."""
        grid_size = int(np.ceil(np.sqrt(num_turbines)))
        spacing = self.config.get("turbine_spacing", 10)
        points = []
        for i in range(grid_size):
            for j in range(grid_size):
                if len(points) < num_turbines:
                    points.append(Point(i * spacing, j * spacing))
        return points

    def _generate_random(self, num_turbines):
        """Generate turbines at random positions."""
        x_range = self.config.get("x_range", [0, 100])
        y_range = self.config.get("y_range", [0, 100])
        points = [
            Point(
                np.random.uniform(*x_range),
                np.random.uniform(*y_range)
            )
            for _ in range(num_turbines)
        ]
        return points

    def _optimize_layout(self, num_turbines):
        """
        Placeholder for optimization-based turbine placement.

        In the future, this will:
        - Maximize power output based on wind direction & speed distribution
        - Minimize bird collision probability
        """
        print("Optimizing turbine layout... (placeholder)")
        # For now, just fall back to grid
        return self._generate_grid(num_turbines)
