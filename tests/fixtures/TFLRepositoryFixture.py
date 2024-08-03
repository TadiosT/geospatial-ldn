import json
from unittest.mock import Mock
from requests import Response

from tests.test_config import TestConfig

config = TestConfig()


class TFLRepositoryFixture:
    mode = "cable-car"
    mode_response = [mode]

    @property
    def empty_404_response(self):
        empty_404_response = Response()
        empty_404_response.status_code = 404
        return empty_404_response

    @property
    def empty_200_response(self):
        empty_200_response = Response()
        empty_200_response.status_code = 200
        return empty_200_response

    @property
    def mode_status_response(self):
        mode_status_response = Response()
        mode_status_response.status_code = 200
        mode_status_response.json = Mock()
        mode_status_response_path = config.RESOURCES_PATH.joinpath("mode_status_response.json")
        mode_status_response.json.return_value = json.loads(mode_status_response_path.read_bytes())
        return mode_status_response
