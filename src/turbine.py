import json
import geopandas as gpd
from shapely.geometry import Point
from shapely.strtree import STRtree

class TurbineManager:
    def __init__(self, config):
        self.config = config
        self.turbines = []

        turbine_file = config.get("turbine_file")
        if turbine_file:
            try:
                self._load_from_file(turbine_file)
            except Exception as e:
                print(f"⚠️ Could not load turbine file ({e}), falling back to generated layout.")
                self._generate_turbines()
        else:
            self._generate_turbines()

        self._build_geoms()

    def _load_from_file(self, filepath):
        gdf = gpd.read_file(filepath)
        for geom in gdf.geometry:
            if geom.geom_type == "Point":
                self.turbines.append({"x": geom.x, "y": geom.y, "radius": self.config["turbines"].get("radius", 40)})
        print(f"✅ Loaded {len(self.turbines)} turbines from {filepath}")

    def _generate_turbines(self):
        settings = self.config.get("turbines", {})
        count = settings.get("count", 12)
        spacing = settings.get("spacing", 200)
        radius = settings.get("radius", 40)
        rows = settings.get("grid_rows", 3)
        cols = settings.get("grid_cols", 4)

        for r in range(rows):
            for c in range(cols):
                if len(self.turbines) >= count:
                    return
                x = c * spacing
                y = r * spacing
                self.turbines.append({"x": x, "y": y, "radius": radius})

        print(f"✅ Generated {len(self.turbines)} turbines in grid layout.")

    def _build_geoms(self):
        self.geoms = [Point(t["x"], t["y"]).buffer(t["radius"]) for t in self.turbines]
        self.sindex = STRtree(self.geoms)
