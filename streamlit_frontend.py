import streamlit as st

from controllers.air_quality_controller import AirQualityController
from controllers.crime_controller import CrimeController
from controllers.health_controller import HealthController
from controllers.tfl_controller import TfLController
from services.geospatial_service import GeospatialService


class StreamlitFrontend:
    def __init__(self):
        self.crime = CrimeController()
        self.health = HealthController()
        self.tfl = TfLController()
        self.air_quality = AirQualityController()
        self.geo_service = GeospatialService()

    @staticmethod
    def start_up() -> tuple[str, str]:
        st.sidebar.title("A Geospatial Analysis of London")
        st.sidebar.write("In this project I will be using Open data to allow the citizens of London to\n"
                         "have a deeper understanding of their borough")

        st.sidebar.subheader("How to use the site!")
        st.sidebar.write(
            "In this sidebar you will be able to select the borough that you'd like to analyse.\nOnce you have "
            "selected the borough you may decide which aspect of the borough you wish to inspect")
        borough_list = GeospatialService().borough_list
        category = st.sidebar.selectbox("Choose a category", ("Crime", "Health", "TfL", "Air Quality"))
        borough_options = st.sidebar.selectbox("Choose a borough", borough_list)

        return borough_options, category

    def run(self, borough: str, category_choice: str) -> None:
        dict_of_categories = {
            "Crime": self.crime,
            "Health": self.health,
            "TfL": self.tfl,
            "Air Quality": self.air_quality
        }

        dict_of_categories[category_choice].run(borough)
