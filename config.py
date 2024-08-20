from pathlib import Path


class Config:
    def __init__(self):
        # BASE URLs
        self.URL_SCHEME = "https://"
        self.AIR_BASE_URL = f"{self.URL_SCHEME}api.erg.ic.ac.uk/AirQuality"
        self.TFL_BASE_URL = f"{self.URL_SCHEME}api.tfl.gov.uk"
        self.CRIME_BASE_URL = f"{self.URL_SCHEME}data.police.uk/api/"

        # SQL LITE
        self.SQLITE_PATH = "database.db"
        self.SQLITE_URI = f"sqlite:///{self.SQLITE_PATH}"

        # BASE FILE PATHS
        self.ROOT_PATH = Path(__file__).parent

        # MAP CONFIG
        self.LDN_CENTRE_LAT = 51.490097
        self.LDN_CENTRE_LNG = -0.127794
        self.DEFAULT_ZOOM = 8.5
        self.NUMBER_OF_BOROUGHS = 33

        # POPUP COLUMNS
        self.CRIME_POPUPS = ["Borough", "category"]
        self.TFL_POPUPS = ["Borough", "Name", "mode", "line"]
        self.HEALTH_POPUPS = ["OrganisationName", "Borough", "Address1", "Address2", "Address3", "City", "County",
                              "Postcode", "Phone", "Email", "Website"]
        self.AIR_POPUPS = ["Borough", "SiteName"]

    @property
    def resources_path(self) -> Path:
        return self.ROOT_PATH.joinpath("resources")

    @property
    def db_path(self) -> Path:
        return self.ROOT_PATH.joinpath(self.SQLITE_PATH)

    @property
    def nhs_path(self) -> Path:
        return self.resources_path.joinpath("nhs_data")

    @property
    def ldn_path(self) -> Path:
        return self.resources_path.joinpath("ldn_data", "ldn.json")
