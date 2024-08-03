from abc import abstractmethod, ABC

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from config import Config
from utilities.logging import setup_logger


class BaseRepository(ABC):

    def __init__(self):
        self.config = Config()
        self.request_session = requests.Session()
        self.retry_policy = Retry(total=5, backoff_factor=1, status_forcelist=[429])
        self.request_session.mount(self.config.URL_SCHEME, HTTPAdapter(max_retries=self.retry_policy))
        self.logger = setup_logger(__name__)

    @abstractmethod
    def get_data(self, *args):
        """
        Gets raw data from either an API using HTTP Get requests or from a database using SQL queries
        :param args: parameters required to filter for specific data e.g. borough
        :return: raw data of a range of types
        """
        pass
