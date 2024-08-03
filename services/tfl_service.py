from typing import List

import geopandas as gpd
import pandas as pd
import streamlit as st

from repositories.tfl_repository import TfLRepository
from services.base_service import BaseService


class TfLService(BaseService):

    def __init__(self):
        self.repository = TfLRepository()

    @staticmethod
    def _seconds_to_minutes(num: int) -> str:
        mins = num // 60
        if mins == 0:
            return "Due"
        else:
            return f"{mins} min"

    @st.cache
    def _get_gdf(self) -> gpd.GeoDataFrame:
        """Gets list of dictionaries storing data for each stop point
        :return: a gpd.GeoDataFrame object storing the stop points
        """
        stops = self.repository.get_data()
        stations = gpd.GeoDataFrame(stops, geometry="geometry")
        stations["line"] = stations.groupby("Name")["line"].transform(", ".join)
        stations = stations.drop_duplicates()

        return stations

    def _clean_arrival_data(self, station_name: str) -> List[dict]:
        """Cleans arrival data from the repository
        :param station_name: Name of station chosen by the user
        :return: a list of dictionaries storing arrival data
        """
        arrival_data = self.repository.get_arrival_data(station_name)
        if not arrival_data:
            raise RuntimeError("No TfL arrival data.")
        required_keys = ["stationName",	"platformName", "direction", "destinationName", "timeToStation"]
        cleaned_stop_data = [
            {stop_key: stop_value for stop_key, stop_value in stop.items() if stop_key in required_keys}
            for stop in arrival_data]
        return cleaned_stop_data

    def get_by_borough(self, borough: str, borough_gdf: pd.DataFrame) -> gpd.GeoDataFrame:
        """Spatial join of two gpd.GeoDataFrame objects which store all the tfl stops and all the geometries for
        boroughs in London
        :param borough: borough name
        :param borough_gdf: gdf storing geometries for all boroughs in London
        :return: a gpd.GeoDataFrame object storing the tfl stop points in the requested borough
        """
        stations_in_borough = gpd.sjoin(self._get_gdf(), borough_gdf[borough_gdf["Borough"] == borough])
        if stations_in_borough.empty:
            raise RuntimeError("No data available currently for your chosen borough.")
        return stations_in_borough

    def get_arrival_times(self, station_name: str) -> pd.DataFrame:
        """Gets arrival data times for each platform and in a pd.Dataframe ready to be displayed to the user
        :param station_name: Name of station chosen by a user
        :return: a pd.DataFrame object storing arrival data
        """
        arrival_data = self._clean_arrival_data(station_name)
        arrival_df = pd.DataFrame(arrival_data)
        arrival_df["timeToStation"] = arrival_df["timeToStation"].apply(self._seconds_to_minutes)
        arrival_df = arrival_df.set_index("stationName")
        arrival_df = arrival_df.rename(columns={"platformName": "Platform",
                                                "direction": "Direction",
                                                "destinationName": "Destination",
                                                "timeToStation": "Time Remaining"
                                                }).sort_values("Platform")

        return arrival_df
