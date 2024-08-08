from typing import List

import pandas as pd
import streamlit as st
from streamlit_keplergl import keplergl_static

from controllers.base_controller import BaseController
from services.air_quality_service import AirQualityService


class AirQualityController(BaseController):

    def __init__(self):
        super().__init__()
        self.service = AirQualityService()

    def run(self, borough: str) -> None:
        try:
            st.title("Air Quality")
            self.logger.info("Air quality data retrieved from the API")
            air_quality_borough_gdf = self.service.get_by_borough(borough)
            st.subheader(f"Map of sensors in {borough}")
            air_quality_map = self.map.get_kepler_map(air_quality_borough_gdf,
                                                      "Air Quality Sensors",
                                                      hover_cols=("Borough", "SiteName"),
                                                      config_lat=self.geo_service.ldn_centroids[borough].y,
                                                      config_lng=self.geo_service.ldn_centroids[borough].x,
                                                      zoom=10)
            keplergl_static(air_quality_map)
            self.logger.info("Map of sensors shown to the user")
            sensor_input = st.selectbox("Select a sensor", pd.Series.to_list(air_quality_borough_gdf["SiteName"]))
            sensor_data = self.service.extract_sensor_data(air_quality_borough_gdf, sensor_input)
            self.return_sensor_metrics(sensor_data)
            self.logger.info("Metrics for the user's chosen sensor has been shown")
        except RuntimeError as e:
            st.error(e)

    @staticmethod
    @st.cache_data()
    def return_sensor_metrics(data_dict: List[dict]):
        """
        Iterates of a dictionary storing the air quality data at each sensor in the borough chosen and returns it to
        the user
        :param data_dict: a list of dictionaries storing air quality data at each sensor in the borough
        :return: a streamlit metric displaying air quality data
        """

        for data in data_dict:
            st.metric(label=data["SpeciesCode"], value=data["AirQualityBand"])
