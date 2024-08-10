import streamlit as st
from streamlit_keplergl import keplergl_static

from controllers.base_controller import BaseController
from services.nhs_service import NHSService


class HealthController(BaseController):

    def __init__(self):
        super().__init__()
        self.nhs_service = NHSService()

    def run(self, borough: str) -> None:
        try:
            st.title("Health")
            organisation_options = st.selectbox("Choose an NHS organisation: ", ["Hospitals", "Pharmacies", "GP",
                                                                                 "Dentists"])
            match organisation_options:
                case "Pharmacies":
                    # TODO: Fix GP services csv issue
                    organisation = self.nhs_service.join_services(borough,
                                                                  organisation_options,
                                                                  self.geo_service.get_by_borough)
                case _:
                    organisation = self.nhs_service.get_by_borough(borough,
                                                                   organisation_options,
                                                                   self.geo_service.get_by_borough)
            self.logger.info("Data received from database.db")
            if organisation_options == "Pharmacy":
                st.subheader(f"Pharmacies in {borough}")
            else:
                st.subheader(f"{organisation_options} in {borough}")

            nhs_map = self.map.get_kepler_map(organisation, f"{organisation_options}",
                                              hover_cols=(
                                                  "OrganisationName", "Borough", "Services", "Address1", "Address2",
                                                  "Address3", "City", "County", "Postcode", "Phone", "Email",
                                                  "Website"),
                                              config_lat=self.geo_service.ldn_centroids[borough].y,
                                              config_lng=self.geo_service.ldn_centroids[borough].x,
                                              zoom=10)
            keplergl_static(nhs_map)
            self.logger.info("Map of organisations shown to the user")
        except RuntimeError as e:
            st.error(e)
