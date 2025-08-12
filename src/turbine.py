import geopandas as gpd
import pyproj

class TurbineManager:
    def __init__(self, turbine_file, buffer_distance=50):
        self.gdf = gpd.read_file(turbine_file)

        if self.gdf.crs is None:
            raise ValueError("Turbine file has no CRS. Please define it before loading.")

        if self.gdf.crs.is_geographic:
            centroid = self.gdf.unary_union.centroid
            utm_zone = int((centroid.x + 180) / 6) + 1
            utm_crs = pyproj.CRS.from_string(f"EPSG:{32600 + utm_zone}")
            self.gdf = self.gdf.to_crs(utm_crs)

        self.gdf["collision_zone"] = self.gdf.geometry.buffer(buffer_distance)
        self.sindex = self.gdf.sindex

