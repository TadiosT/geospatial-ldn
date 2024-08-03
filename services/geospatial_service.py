import ast
import functools
from typing import List

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

from config import Config
from repositories.geospatial_repository import GeospatialRepository
from services.base_service import BaseService


class GeospatialService(BaseService):
    def __init__(self):
        self.repository = GeospatialRepository()
        self.config = Config()

    @functools.cached_property
    def _ldn_geo_df(self) -> pd.DataFrame:
        """Returns a pd.DataFrame object that stores the boundary coordinates which define each borough in London.
        :return: a pd.DataFrame object storing the boundaries of each borough
        """
        boroughs_df = self.repository.get_data
        ldn_boroughs_geo = boroughs_df.geometry.apply(pd.Series)

        return ldn_boroughs_geo

    @functools.cached_property
    def get_by_borough(self) -> gpd.GeoDataFrame:
        """
        Converts borough boundaries from the repository class to a shapely.geometry.Polygon object and makes it the
        geometry column of GeoDataFrame object storing the data for each borough in London while removing redundant
        columns
        :return: a gpd.GeoDataFrame object storing geospatial data on each borough in London
        """
        boroughs_df = self.repository.get_data
        ldn_boroughs_NM = boroughs_df.properties.apply(pd.Series)
        ldn_boroughs_geo = self._ldn_geo_df

        poly_ldn = [Polygon(ast.literal_eval(str(ldn_boroughs_geo.coordinates.iloc[i]))[0]) for i in
                    range(len(ldn_boroughs_geo))]

        ldn_boroughs_NM["geometry"] = gpd.GeoSeries(poly_ldn)
        boroughs_gdf = gpd.GeoDataFrame(ldn_boroughs_NM)

        boroughs_gdf = boroughs_gdf.drop(["LAD20CD", "LAT", "LONG", "OBJECTID", "BNG_E", "BNG_N"], axis=1)

        return boroughs_gdf

    @functools.cached_property
    def borough_bounds(self) -> gpd.GeoDataFrame:
        """
        Gets the bounds of each borough in London and stores them in string format to be used in a URL (Only used in crime)
        :return: a pd.DataFrame object which stores the 4 min and max points that cover every borough in a URL format
        """
        bounds = self.get_by_borough.geometry.bounds
        bounds["Borough"] = self._ldn_dict.keys()
        bounds = bounds.set_index("Borough")
        bounds["coordinates_url"] = [f"{bounds.iloc[i]['miny']},{bounds.iloc[i]['minx']}:"
                                     f"{bounds.iloc[i]['miny']},{bounds.iloc[i]['maxx']}:"
                                     f"{bounds.iloc[i]['maxy']},{bounds.iloc[i]['maxx']}:"
                                     f"{bounds.iloc[i]['maxy']},{bounds.iloc[i]['minx']}"
                                     for i in range(self.config.NUMBER_OF_BOROUGHS)]
        return bounds

    @functools.cached_property
    def _ldn_dict(self) -> dict:
        """Creates a dictionary to store the geometries of each borough
        :return: a dictionary storing the geometries of each borough
        """
        ldn_dict = self.get_by_borough[["Borough", "geometry"]].set_index("Borough").T.to_dict()
        return ldn_dict

    @functools.cached_property
    def ldn_centroids(self) -> gpd.GeoDataFrame:
        """Gets the centre points of each borough in London and returns a gpd.GeoDataFrame object
        :return: a geopandas.GeoDataFrame object which stores the centre points of all the boroughs in London
        """
        for borough in self._ldn_dict.keys():
            list_of_coords = self._ldn_geo_df.coordinates.to_list()[list(self._ldn_dict.keys()).index(borough)][0]
            self._ldn_dict[borough]["geometry"] = "".join(
                [f"{list_of_coords[i][1]},{list_of_coords[i][0]}:" for i in range(self.config.NUMBER_OF_BOROUGHS)])[:-1]

        centroids = self.get_by_borough[["Borough", "geometry"]].set_index("Borough").centroid

        return centroids

    @functools.cached_property
    def borough_list(self) -> List[str]:
        """Gets a list of the boroughs in London
        :return: a list of boroughs in London
        """
        borough_list = list(self.ldn_centroids.index)

        return borough_list
