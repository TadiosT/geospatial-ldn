from typing import List

import geopandas as gpd
import requests
from requests import ConnectionError

from repositories.base_repository import BaseRepository


class PoliceUKRepository(BaseRepository):

    def __init__(self):
        super().__init__()

    def get_categories(self, date: str) -> List[dict]:
        """Gets crime categories available at a particular date and returns a json
        :param date: date object that is selected by a user
        :return: a list of dictionaries storing the name and url assigned to each crime category
        """
        try:
            categories_url = f"{self.config.CRIME_BASE_URL}crime-categories?date={date}"
            categories = self.request_session.get(categories_url).json()
            return categories
        except ConnectionError:
            raise RuntimeError("There is a connection error. Crime categories cannot be retrieved.")

    def get_data(self, borough: str, cat_choice: str, dict_of_categorise: dict, date: str, bounds: gpd.GeoDataFrame) \
            -> dict:
        """Gets crime data from a chosen borough, date and category and returns a pandas DataFrame
        :param borough: name of borough selected by a user
        :param cat_choice: name of crime category chosen by a user
        :param dict_of_categorise: list of category urls for the date chosen
        :param date: date selected by a user
        :param bounds: a pd.DataFrame object storing the bounds of each borough in a string format
        :return: a pd.DataFrame object holding crime data based on the selected parameters
        """
        url = f"{self.config.CRIME_BASE_URL}/crimes-street/{dict_of_categorise[cat_choice]}?poly=" \
              f"{bounds.loc[borough]['coordinates_url']}&date={date}"
        try:
            crime_data = self.request_session.get(url).json()
        except ValueError:
            raise RuntimeError("There seems to be no data available for your chosen parameters.")
        except ConnectionError:
            raise RuntimeError("There is a connection error. Crime data cannot be retrieved.")

        return crime_data
