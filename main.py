from sqlmodel import SQLModel

from config import Config
from database import create_db_and_tables, insert_objects
from streamlit_frontend import StreamlitFrontend

config = Config()


def init_db(configuration: Config) -> None:
    """Creates a database if the database doesn't already exist and clears the metadata if it does
    :param configuration: Config object storing required file paths
    :return: None
    """
    if not config.db_path.exists():
        create_db_and_tables(configuration)
        insert_objects(configuration)
    else:
        SQLModel.metadata.clear()


def main() -> None:
    """Runs the frontend software
    :return: None
    """
    frontend = StreamlitFrontend()
    user_input = frontend.start_up()
    frontend.run(user_input[0], user_input[1])


if __name__ == "__main__":
    init_db(config)
    main()
