import folium
from config import Config
from typing import List
import geopandas as gpd
import pandas as pd


class FoliumMap:
    config = Config()

    def get_folium_map(self, gdf: gpd.GeoDataFrame, popup_cols: List[str] = ["Borough"],
                       config_lat: int = config.LDN_CENTRE_LAT, config_lng: int = config.LDN_CENTRE_LNG,
                       zoom: int = 10) -> folium.Map():
        gdf.set_crs(epsg=4326, inplace=True)
        m = folium.Map(location=[config_lat, config_lng], zoom_start=zoom, tiles='cartodbdark_matter')

        for i, row in gdf.iterrows():
            folium.CircleMarker(
                location=(row.geometry.y, row.geometry.x),
                radius=2,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
                popup=self.build_popup_text(row, popup_cols)
            ).add_to(m)

        return m

    @staticmethod
    def build_popup_text(row: pd.Series, popup_cols: List[str]) -> str:
        s = ""
        for popup in popup_cols:
            s += f"{popup.capitalize()}: {row[popup]}, "

        return s.rstrip(", ")
