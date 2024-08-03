from requests import ConnectionError

from repositories.base_repository import BaseRepository


class AirQualityRepository(BaseRepository):

    def __init__(self):
        super().__init__()

    def get_data(self) -> dict:
        """Gets daily air quality data for london returning a json.
        :return: JSON storing air quality data.
        """
        request_url = f"{self.config.AIR_BASE_URL}/Daily/MonitoringIndex/Latest/GroupName=London/Json"
        try:
            air_quality_data = self.request_session.get(request_url).json()["DailyAirQualityIndex"]["LocalAuthority"]
        except ConnectionError:
            raise RuntimeError("There is a connection error. Air quality data cannot be retrieved")
        except KeyError:
            raise RuntimeError("Data has unexpected keys.")
        return air_quality_data

