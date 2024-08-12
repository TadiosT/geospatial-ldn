from abc import abstractmethod, ABC

from services.geospatial_service import GeospatialService
from utilities.kepler_map import Map
from utilities.folium_map import FoliumMap
from utilities.logging import setup_logger


class BaseController(ABC):

    def __init__(self):
        self.geo_service = GeospatialService()
        self.map = Map()
        self.folium_map = FoliumMap()
        self.logger = setup_logger(__name__)

    @abstractmethod
    def run(self, borough: str) -> None:
        """
        Procedural method that gets transformed data from the service level and presents it to the user using streamlit
        methods
        :param borough: name of borough selected by the user
        :return: None
        """
        pass
