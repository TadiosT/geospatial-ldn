import datetime
from typing import List

import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta

from repositories.police_uk_repository import PoliceUKRepository
from services.base_service import BaseService


class PoliceUKService(BaseService):

    def __init__(self):
        self.repository = PoliceUKRepository()

    @staticmethod
    def get_by_borough(raw_crime_result: gpd.GeoDataFrame, borough_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Spatial join between crime and borough gpd.GeoDataFrame objects
        :param raw_crime_result:
        :param borough_gdf: gpd.GeoDataFrame object storing the geometries of each borough in London
        :return: a gpd.GeoDataFrame object storing the crime locations within the bounds of a borough
        """
        filtered_crime_result = gpd.sjoin(raw_crime_result, borough_gdf, predicate="within")
        return filtered_crime_result

    @staticmethod
    def remove_excess_data(borough: str, crimes_by_borough: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Removes excess data from the crimes outside the chosen borough
        :param borough: name of borough
        :param crimes_by_borough: a gpd.GeoDataFrame object storing crime locations in a boroughs bounds(Quadrilateral)
        :return: a gpd.GeoDataFrame object storing the crimes in a chosen borough
        """
        crimes_in_borough = crimes_by_borough.loc[crimes_by_borough["Borough"] == borough]
        return crimes_in_borough

    @staticmethod
    def get_date_range() -> List[str]:
        """Gets a range of dates in the form y1y2y3y4-m1m2 from 2 years and 11 months ago(29 of 30 days do not work)
        until now
        :return: list of dates represented as strings
        """
        today = datetime.date.today()
        end_date = today - relativedelta(months=2)
        start_date = end_date - relativedelta(years=2, months=11)
        dates = pd.date_range(start=start_date, end=end_date, freq="1M").strftime("%Y-%m")
        dates = [str(date) for date in dates]

        return dates

    @staticmethod
    def get_table(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
        """Gets a gpd.GeoDataFrame object storing the crime locations and returns a pd.DataFrame object storing the
        number of offences of each crime type
        :param gdf: gpd.GeoDataFrame object storing the crime locations
        :return: a pd.DataFrame object storing the number of offences of each crime type
        """
        df = gdf[["Borough", "category"]]
        counts = df.groupby(df.columns.tolist(), as_index=False).size()
        counts = counts.rename(columns={"size": "Number of offences"}).set_index("Borough")
        return counts

    @st.cache_data()
    def get_gdf(_self, borough: str, cat_choice: str, dict_of_categories: dict, date: str, bounds: gpd.GeoDataFrame) -> \
            gpd.GeoDataFrame:
        """Gets data from the repository class, cleans the data and returns a gpd.GeoDataFrame object
        :param dict_of_categories: dict storing the category names and their corresponding url inputs
        :param borough: name of borough
        :param cat_choice: choice of crime category
        :param date: date chosen by user
        :param bounds: gpd.GeoDataFrame storing the four boundary points of each London borough in string format
        :return: a gpd.GeoDataFrame object storing the data for crimes in the bounds(QUADRILATERAL) of a chosen
        borough
        """
        data = _self.repository.get_data(borough, cat_choice, dict_of_categories, date, bounds)
        if not data:
            raise RuntimeError("No data for your chosen parameters.")
        crime_df = pd.DataFrame(data)
        locations = crime_df.location.apply(pd.Series)
        crime_gdf = gpd.GeoDataFrame(crime_df, geometry=gpd.points_from_xy(locations.longitude, locations.latitude))
        crime_gdf.drop(["location", "context"], axis=1)
        return crime_gdf

    def extract_from_categories(self, date: str) -> dict:
        """Extracts the category names and urls from the data returned from the repository class.
        :param date: date chosen by a user
        :return: a list of category names and a list of the urls assigned to each of the category names
        """
        crime_categories = self.repository.get_categories(date)
        dict_of_categories = {k["name"]: k["url"] for k in crime_categories}
        return dict_of_categories

    def get_bar_chart(self, gdf: gpd.GeoDataFrame, title: str, xlabel: str, ylabel: str) -> matplotlib.figure.Figure:
        """Uses the table from the get_table method to make a bar chart of the crimes in each crime category
        :param gdf: gpd.GeoDataFrame object storing the crimes in a chosen borough
        :param title: title for the bar chart
        :param xlabel: label for the x-axis
        :param ylabel: label for the y-axis
        :return: a streamlit.delta_generator.DeltaGenerator object which displays the bar chart
        """
        table = self.get_table(gdf).set_index("category")
        fig, ax = plt.subplots()
        table.plot(title=title, xlabel=xlabel, ylabel=ylabel, kind="barh", ax=ax)
        return fig
