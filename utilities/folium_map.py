import folium
from config import Config
from typing import List
import geopandas as gpd


class FoliumMap:
    config = Config()

    @staticmethod
    def get_folium_map(gdf: gpd.GeoDataFrame, hover_cols: List[str] = ["Borough"],
                       config_lat: int = config.LDN_CENTRE_LAT, config_lng: int = config.LDN_CENTRE_LNG,
                       zoom: int = 10) -> folium.Map():
        gdf.set_crs(epsg=4326, inplace=True)
        m = folium.Map(location=[config_lat, config_lng], zoom_start=zoom, tiles='cartodbdark_matter')

        for i, row in gdf.iterrows():
            folium.CircleMarker(
                location=(row.geometry.y, row.geometry.x),
                radius=5,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
            ).add_to(m)

        return m

