import streamlit as st

from controllers.base_controller import BaseController
from services.tfl_service import TfLService


class TfLController(BaseController):

    def __init__(self):
        super().__init__()
        self.tfl_service = TfLService()

    def run(self, borough: str) -> None:
        try:
            st.title("TfL")
            borough_stations = self.tfl_service.get_by_borough(borough, self.geo_service.get_by_borough)
            self.logger.info("Data received from the TfL API")

            tfl_map = self.folium_map.get_folium_map(borough_stations,
                                                     popup_cols=self.config.TFL_POPUPS,
                                                     lat=self.geo_service.ldn_centroids[borough].y,
                                                     lng=self.geo_service.ldn_centroids[borough].x,
                                                     zoom=11)

            tfl_map.save("tfl_map.html")
            st.subheader(f"Map of stations in {borough}")
            st.components.v1.html(open('tfl_map.html', 'r').read(), height=500, scrolling=True)
            self.logger.info("Map of stations shown to the user")
            station_names = list(dict.fromkeys(borough_stations["Name"]))

            arrival_time_choice = st.selectbox("Select a station you would like to see arrival times for: ",
                                               station_names)

            arrival_times = self.tfl_service.get_arrival_times(arrival_time_choice)
            st.dataframe(arrival_times)
        except RuntimeError as e:
            st.error(e)
