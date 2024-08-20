import streamlit as st

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

            crime_map = self.folium_map.get_folium_map(crimes_in_borough,
                                                       popup_cols=self.config.CRIME_POPUPS,
                                                       zoom=11,
                                                       lng=self.geo_service.ldn_centroids[borough].x,
                                                       lat=self.geo_service.ldn_centroids[borough].y)
            crime_map.save("crime_map.html")

            st.subheader(f"Crime data for {borough}")
            if category_choice != "All crime":
                st.write(f"There were {int(table.iloc[0]['Number of offences'])} offences cited in {borough}")
                st.subheader(f"Map of Crime in {borough}")
                self.logger.info("Map of crimes shown to a user")
                st.components.v1.html(open('crime_map.html', 'r').read(), height=500, scrolling=True)
            else:
                st.dataframe(table)
                st.subheader(f"Map of Crime in {borough}")
                st.components.v1.html(open('crime_map.html', 'r').read(), height=500, scrolling=True)
                self.logger.info("Map of crimes shown to a user")
                st.subheader("Bar Chart")
                st.bar_chart(self.crime_service.get_table(crimes_in_borough).set_index("category"))
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
