from abc import abstractmethod, ABC

import geopandas as gpd


class BaseService(ABC):

    @abstractmethod
    def get_by_borough(self, *args) -> gpd.GeoDataFrame:
        """
        Should call a get_data method from the repository level that gets data for a borough chosen by the user and
        convert it to gpd.GeoDataFrame object that stores the geometries for a point on a map
        :param args: parameters required to filter for chosen data e.g borough
        :return: a gpd.GeoDataFrame storing the data for the requested borough
        """
        pass
