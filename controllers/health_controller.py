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
            popup_cols = ["OrganisationName", "Borough", "Address1", "Address2", "Address3", "City", "County",
                          "Postcode", "Phone", "Email", "Website"]
            match organisation_options:
                case "Pharmacies":
                    # TODO: Fix GP services csv issue
                    organisation = self.nhs_service.join_services(borough,
                                                                  organisation_options,
                                                                  self.geo_service.get_by_borough)
                    popup_cols.insert(2, "Services")
                case _:
                    organisation = self.nhs_service.get_by_borough(borough,
                                                                   organisation_options,
                                                                   self.geo_service.get_by_borough)
            self.logger.info("Data received from database.db")
            if organisation_options == "Pharmacy":
                st.subheader(f"Pharmacies in {borough}")
            else:
                st.subheader(f"{organisation_options} in {borough}")

            nhs_map = self.folium_map.get_folium_map(organisation,
                                                     popup_cols=popup_cols,
                                                     config_lat=self.geo_service.ldn_centroids[borough].y,
                                                     config_lng=self.geo_service.ldn_centroids[borough].x,
                                                     zoom=11)
            nhs_map.save("nhs_map.html")
            st.components.v1.html(open('nhs_map.html', 'r').read(), height=500, scrolling=True)
            self.logger.info("Map of organisations shown to the user")
        except RuntimeError as e:
            st.error(e)
