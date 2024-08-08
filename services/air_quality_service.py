import ast
from typing import Dict, List

import geopandas as gpd
import pandas as pd
import streamlit as st

from repositories.air_quality_repository import AirQualityRepository
from services.base_service import BaseService


class AirQualityService(BaseService):

    def __init__(self):
        self.repository = AirQualityRepository()

    @staticmethod
    @st.cache_data()
    def _parse_data_from_sites(result: dict, site: Dict[str, str], species: dict, local_authority: dict) -> dict:
        """Creates a nested dictionary by cleaning data requested by the repository
        :param result: a dictionary storing running air quality data
        :param site: a dictionary storing data about the site
        :param species: a dictionary storing data about the type of pollutant
        :param local_authority: a dictionary storing data on the local authority area
        :return: a dictionary storing air quality data
        """
        site_name = f"{site['@SiteCode']}{species['@SpeciesCode']}"
        result[site_name] = dict(
            SiteName=site["@SiteName"],
            LocalAuthorityName=local_authority["@LocalAuthorityName"],
            Latitude=site["@Latitude"],
            Longitude=site["@Longitude"],
            Species=str(
                dict(SpeciesCode=species["@SpeciesCode"],
                     SpeciesDescription=species["@SpeciesDescription"],
                     AirQualityIndex=species["@AirQualityIndex"],
                     AirQualityBand=species["@AirQualityBand"])
            )
        )

        return result

    @staticmethod
    @st.cache()
    def extract_sensor_data(gdf: gpd.GeoDataFrame, sensor_name: str) -> List[dict]:
        """Extracts sensor data based on a sensor chosen by a user
        :param gdf: a gpd.GeoDataFrame object storing the air quality data for London
        :param sensor_name: name of the sensor chosen by the user
        :return: a list of dictionaries storing
        """
        data = gdf[gdf["SiteName"] == sensor_name]
        species = data["Species"].iloc[0].split("}")
        list_of_dicts = []

        for i in range(len(species)):
            list_of_dicts.append(species[i] + "}")
        list_of_dicts = [ast.literal_eval(char) for char in list_of_dicts[0:-1]]

        return list_of_dicts

    @st.cache_data()
    def _parse_data_from_site(_self, result: dict, site: dict, local_authority: dict) -> dict:
        
        species = site["Species"]
        parse_kwargs = dict(site=site, local_authority=local_authority)
        if isinstance(species, list):
            for single_species in species:
                result = _self._parse_data_from_sites(species=single_species, result=result, **parse_kwargs)
        elif isinstance(species, dict):
            result = _self._parse_data_from_sites(species=species, result=result, **parse_kwargs)
        else:
            raise RuntimeError("Type of species is not in expected types (list, dict)")

        return result

    @st.cache_data()
    def get_parsed_data(_self) -> dict:
        """Extracts required data from the air quality API
        :return: Air Quality data
        """
        local_authority_air_quality = _self.repository.get_data()
        result_dict = dict()
        for local_authority_data in local_authority_air_quality:
            if "Site" in local_authority_data:
                sites_data = local_authority_data["Site"]
                if isinstance(sites_data, list):
                    for site_data in sites_data:
                        _self._parse_data_from_site(result_dict, site_data, local_authority_data)
                elif isinstance(sites_data, dict):
                    _self._parse_data_from_site(result_dict, sites_data, local_authority_data)

        return result_dict

    def get_by_borough(self, borough: str) -> gpd.GeoDataFrame:
        """Filters a dictionary storing air quality data by borough
        :param borough: name of borough
        :return: a gpd.GeoDataFrame object storing the air quality data in a chosen borough
        """
        air_quality_data = self.get_parsed_data()
        air_quality_df = pd.DataFrame.from_dict(air_quality_data).T

        air_quality_df["Species"] = air_quality_df.groupby("SiteName")["Species"].transform(" ".join)
        air_quality_df = air_quality_df.groupby("SiteName").first().reset_index(level=0)
        air_quality_in_borough = air_quality_df.loc[air_quality_df["LocalAuthorityName"] == borough]
        air_quality_gdf = gpd.GeoDataFrame(air_quality_in_borough, crs="EPSG:4326",
                                           geometry=gpd.points_from_xy(
                                               air_quality_in_borough["Longitude"],
                                               air_quality_in_borough["Latitude"]))
        air_quality_gdf = air_quality_gdf.rename({"LocalAuthorityName": "Borough"}, axis=1)

        sensor_names = list(air_quality_gdf["SiteName"])
        sensor_names = list(map(lambda x: x.split("-")[-1][1:], sensor_names))
        air_quality_gdf = air_quality_gdf.replace(pd.Series.to_list(air_quality_gdf["SiteName"]), sensor_names)

        return air_quality_gdf
