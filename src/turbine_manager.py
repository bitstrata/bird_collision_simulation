import os
import warnings
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from math import cos, sin, radians

class TurbineManager:
    def __init__(self, config: dict):
        self.config = config  # Preserve full config
        self.gdf = None
        self.sindex = None
        self.geoms = None

        np.random.seed(self.config.get("random_seed", 42))

        turbine_file = self.config.get("turbine_file")
        if turbine_file and os.path.exists(turbine_file):
            self._load_from_file(turbine_file)
        else:
            self._generate_turbines()  # Will call GA if layout=optimized

        # Ensure projected CRS before buffering
        if self.gdf.crs is None or self.gdf.crs.is_geographic:
            warnings.warn(
                "Input geometries are in geographic coordinates; "
                "reprojecting to EPSG:3857 for buffer operations."
            )
            self.gdf = self.gdf.set_crs(epsg=4326, allow_override=True).to_crs(epsg=3857)

        # Create collision zones
        buffer_distance = float(self.config.get("collision_zone_buffer", 5.0))
        self.gdf["collision_zone"] = self.gdf.geometry.buffer(buffer_distance)
        self.gdf = self.gdf.set_geometry("collision_zone", inplace=False)

        # Spatial index
        self.sindex = self.gdf.sindex
        self.geoms = list(self.gdf.geometry.values)

    # ---------- Load / Generate ----------
    def _load_from_file(self, file_path: str):
        gdf = gpd.read_file(file_path)
        if gdf.empty:
            raise ValueError(f"No turbine features found in {file_path}")
        if not all(gdf.geometry.geom_type == "Point"):
            gdf = gdf.set_geometry(gdf.geometry.centroid, inplace=False)
        self.gdf = gdf
        print(f"Loaded {len(self.gdf)} turbines from {file_path}")

    def _generate_turbines(self):
        num_turbines = int(self.config.get("num_turbines", 12))
        layout = self.config.get("turbine_layout", "grid").lower()

        if layout == "grid":
            points = self._generate_grid(num_turbines)
        elif layout == "random":
            points = self._generate_random(num_turbines)
        elif layout == "optimized":
            points = self._optimize_layout_ga(num_turbines)
        else:
            raise ValueError(f"Unknown turbine layout: {layout}")

        self.gdf = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")
        print(f"Generated {num_turbines} turbines using '{layout}' layout.")

    # ---------- Grid / Random ----------
    def _generate_grid(self, num_turbines):
        spacing = float(self.config.get("grid_spacing", 10))
        grid_size = int(np.ceil(np.sqrt(num_turbines)))
        pts = []
        for i in range(grid_size):
            for j in range(grid_size):
                if len(pts) >= num_turbines:
                    break
                pts.append(Point(i * spacing, j * spacing))
            if len(pts) >= num_turbines:
                break
        return pts

    def _generate_random(self, num_turbines):
        x_min, x_max = self._get_bounds("x_range", 0, 100)
        y_min, y_max = self._get_bounds("y_range", 0, 100)
        return [Point(np.random.uniform(x_min, x_max), np.random.uniform(y_min, y_max))
                for _ in range(num_turbines)]

    # ---------- GA Optimizer ----------
    def _optimize_layout_ga(self, num_turbines):
        # Simple GA placeholder returning random layout (full GA from previous code can be inserted)
        print("GA optimization complete (placeholder).")
        return self._generate_random(num_turbines)

    # ---------- Helpers ----------
    def _get_bounds(self, key, default_min, default_max):
        rng = self.config.get(key, [default_min, default_max])
        if not isinstance(rng, (list, tuple)) or len(rng) != 2:
            rng = [default_min, default_max]
        return float(rng[0]), float(rng[1])
