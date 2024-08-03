from unittest import TestCase
from unittest.mock import patch

from requests import Session

from repositories.tfl_repository import TfLRepository
from tests.fixtures.TFLRepositoryFixture import TFLRepositoryFixture


@patch.object(Session, "get")
@patch.object(TfLRepository, "_clean_mode_names")
class TestTFLRepository(TestCase):
    under_test = TfLRepository()
    fixture = TFLRepositoryFixture()

    def test_data_returns_expected_error_on_bad_response_to_mode_get(self, mock_clean_mode_names, mock_request_get):
        mock_clean_mode_names.return_value = self.fixture.mode_response
        mock_request_get.return_value = self.fixture.empty_404_response
        expected_msg = f"Could not query TFL API for available modes. {self.fixture.empty_404_response.status_code}" \
                       f" Response."
        with self.assertRaisesRegex(RuntimeError, expected_regex=expected_msg):
            self.under_test.get_data()

    def test_data_returns_expected_error_on_bad_response_to_mode_status(self, mock_clean_mode_names, mock_request_get):
        mock_clean_mode_names.return_value = [self.fixture.mode]
        mock_request_get.side_effect = [self.fixture.mode_status_response, self.fixture.empty_404_response]
        expected_msg = f"Could not connect to TFL API for {self.fixture.mode} transport mode. " \
                       f"{self.fixture.empty_404_response.status_code} Response."
        with self.assertRaisesRegex(RuntimeError, expected_regex=expected_msg):
            self.under_test.get_data()

    def test_data_returns_expected_error_on_bad_response_to_lines_info(self, mock_clean_mode_names, mock_request_get):
        mock_clean_mode_names.return_value = self.fixture.mode_response
        mock_request_get.side_effect = [self.fixture.empty_200_response, self.fixture.mode_status_response,
                                        self.fixture.empty_404_response]
        expected_msg = f"Could not get stop point data from TFL API. {self.fixture.empty_404_response.status_code}" \
                       f" Response"
        with self.assertRaisesRegex(RuntimeError, expected_regex=expected_msg):
            self.under_test.get_data()
