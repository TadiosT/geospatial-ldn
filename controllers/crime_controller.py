import streamlit as st
from streamlit_keplergl import keplergl_static

from controllers.base_controller import BaseController
from services.police_uk_service import PoliceUKService


class CrimeController(BaseController):

    def __init__(self):
        super().__init__()
        self.crime_service = PoliceUKService()

    def run(self, borough: str) -> None:
        try:
            st.title("Crime")
            self.logger.info("Getting date slider.")
            date = self._get_date_slider()
            self.logger.debug("Extracting from categories.")
            dict_of_categories = self.crime_service.extract_from_categories(date)
            category_choice = st.selectbox("Pick a crime category:", dict_of_categories.keys())
            crime_gdf = self.crime_service.get_gdf(borough, category_choice, dict_of_categories,
                                                   date, self.geo_service.borough_bounds)

            filtered_crime_result = self.crime_service.get_by_borough(crime_gdf, self.geo_service.get_by_borough)
            crimes_in_borough = self.crime_service.remove_excess_data(borough, filtered_crime_result)

            crimes_in_borough = crimes_in_borough.drop(["location_subtype", "context"], axis=1)

            table = self.crime_service.get_table(crimes_in_borough)
            crime_map = self.map.get_kepler_map(crimes_in_borough,
                                                "Crime",
                                                hover_cols=("Borough", "category"),
                                                zoom=10,
                                                config_lng=self.geo_service.ldn_centroids[borough].x,
                                                config_lat=self.geo_service.ldn_centroids[borough].y)

            st.subheader(f"Crime data for {borough}")
            if category_choice != "All crime":
                st.write(f"There were {int(table.iloc[0]['Number of offences'])} offences cited in {borough}")
                st.subheader(f"Map of Crime in {borough}")
                self.logger.info("Map of crimes shown to a user")
                keplergl_static(crime_map)
            else:
                st.dataframe(table)
                st.subheader(f"Map of Crime in {borough}")
                keplergl_static(crime_map)
                self.logger.info("Map of crimes shown to a user")
                st.subheader("Bar Chart")
                st.pyplot(self.crime_service.get_bar_chart(crimes_in_borough, f"{borough}", "Crime Categories",
                                                           "Frequency"))
                self.logger.info("Bar chart displayed to the user")

        except RuntimeError as e:
            st.error(e)

    def _get_date_slider(self) -> str:
        """
        Creates a date slider based on a list of dates
        :return: a streamlit date slider
        """
        dates = self.crime_service.get_date_range()
        slider_args = ["Choose a month", dates]
        dates_slider = st.select_slider(*slider_args)

        return dates_slider
