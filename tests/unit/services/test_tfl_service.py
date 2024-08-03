from unittest import TestCase
from unittest.mock import patch

from geopandas import GeoDataFrame

from services.geospatial_service import GeospatialService
from services.tfl_service import TfLService


class TestTfLService(TestCase):
    under_test = TfLService()
    geospatial_service = GeospatialService()

    @patch.object(GeoDataFrame, "empty")
    def test_get_by_borough_raises_correct_exception_when_gdf_empty(self, mock_gpd_empty):
        mock_gpd_empty.return_value = True
        expected_msg = "No data available currently for your chosen borough."
        with self.assertRaisesRegex(RuntimeError, expected_regex=expected_msg):
            self.under_test.get_by_borough("Newham", self.geospatial_service.get_by_borough)
