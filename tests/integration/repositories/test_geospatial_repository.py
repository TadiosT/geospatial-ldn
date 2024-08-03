from unittest import TestCase
from unittest.mock import patch

import pandas as pd

from repositories.geospatial_repository import GeospatialRepository
from config import Config


class TestGeospatialRepository(TestCase):
    under_test = GeospatialRepository()

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = cls.under_test.get_data

    def test_get_data_returns_correct_type(self):
        actual = type(self.result)
        if isinstance(actual, pd.DataFrame):
            return True
        else:
            return False
