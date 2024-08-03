from typing import List

import geopandas as gpd
import pandas as pd
from sqlmodel import SQLModel

from repositories.nhs_repository import NHSRepository
from services.base_service import BaseService


class NHSService(BaseService):

    def __init__(self):
        self.repository = NHSRepository()

    @staticmethod
    def _sqlmodel_to_df(objs: List[SQLModel]) -> pd.DataFrame:
        """Converts a list of SQLModel objects into a pd.DataFrame object.
        :param objs: a list of SQLModel objects
        :return: a pd.DataFrame object
        """
        records = [model.dict() for model in objs]
        df = pd.DataFrame.from_records(records)
        return df

    def _get_df(self, table_name: str) -> pd.DataFrame:
        """Gets a list of SQLModel objects for the chosen organisation and converts it to a pd.DataFrame object.
        :param table_name: name of table in database
        :return: pd.DataFrame object
        """
        results = self.repository.get_data(table_name)
        df = self._sqlmodel_to_df(results)
        return df

    def _get_service_df(self, organisation: str) -> pd.DataFrame:
        """
        Converts the service data from a list of SQLModel objects to a pd.DataFrame object
        :param organisation: name of organisation
        :return: pd.DataFrame object storing a list of services for each organisation
        """
        service = self.repository.get_services(organisation)
        service_df = self._sqlmodel_to_df(service)
        service_series = service_df.groupby("OrganisationID").apply(lambda x: ", ".join(x["ServiceName"]))
        service_df = service_series.rename("Services").to_frame().reset_index()

        return service_df

    def get_by_borough(self, borough: str, organisation: str, boroughs_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Gets data on a chosen nhs organisation and filters it by borough
        :param borough: name of chosen borough
        :param organisation: name of organisation
        :param boroughs_gdf: gpd.GeoDataFrame object storing the geometries of each borough in London
        :return: a gpd.GeoDataFrame object storing nhs organisation data for a chosen borough
        """

        df = self._get_df(organisation)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude)).drop(
            columns=["Longitude", "Latitude"])
        org_in_borough = gpd.sjoin(gdf, boroughs_gdf[boroughs_gdf["Borough"] == borough], predicate="within")
        org_in_borough = org_in_borough.set_crs(4326, allow_override=True)

        return org_in_borough

    def join_services(self, borough: str, organisation: str, boroughs_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
        """
        Joins the service dataframe with a dataframe storing the organisation data of a chosen borough
        :param borough: name of chosen borough
        :param organisation: name of organisation
        :param boroughs_gdf: gpd.GeoDataFrame object storing the geometries of each borough in London
        :return: a pd.DataFrame object storing service data as well as relevant organisation data
        """
        org_in_borough = self.get_by_borough(borough, organisation, boroughs_gdf)
        service_df = self._get_service_df(organisation)
        joined_df = pd.merge(org_in_borough, service_df, left_index=True, right_index=True)

        return joined_df
