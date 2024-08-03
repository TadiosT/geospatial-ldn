import functools

import pandas as pd

from config import Config
from repositories.base_repository import BaseRepository


class GeospatialRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self.config = Config()

    @functools.cached_property
    def get_data(self) -> pd.DataFrame:
        """Opens file in resources folder storing the geometries for each borough in London
        :return: pd.DataFrame object which holds the geometries of each borough
        """
        try:
            boroughs_df = pd.read_json(self.config.ldn_path).drop(["type"], axis=1)
            boroughs_df = boroughs_df["features"].apply(pd.Series)
        except TypeError:
            raise RuntimeError("London geospatial data cannot be found.")
        return boroughs_df
