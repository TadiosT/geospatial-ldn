from pathlib import Path

from config import Config


class TestConfig(Config):
    def __init__(self):
        super(TestConfig, self).__init__()
        self.ROOT_PATH = Path(__file__).parent
        self.RESOURCES_PATH = self.ROOT_PATH.joinpath("resources")
        self.SQLITE_PATH = "test_database.db"
        self.SQLITE_URI = f"sqlite:///{self.SQLITE_PATH}"
