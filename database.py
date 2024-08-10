from sqlmodel import create_engine, SQLModel, Session, engine
import pandas as pd
from models import nhs_models


def model_paths(config) -> dict:
    """Creates a dictionary storing the nhs organisation paths assigned to each ORM
    :param config: object storing required file paths
    :return: a dictionary storing the nhs organisation paths assigned to each ORM
    """
    _model_paths = {
        nhs_models.Hospital: config.nhs_path.joinpath("hospitals", "hospitals.csv"),
        nhs_models.Pharmacy: config.nhs_path.joinpath("pharmacies", "pharmacies.csv"),
        nhs_models.PharmacyService: config.nhs_path.joinpath("pharmacies", "services.csv"),
        nhs_models.GP: config.nhs_path.joinpath("gp", "gp.csv"),
        # nhs_models.GPService: config.nhs_path.joinpath("gp", "services.csv"),
        nhs_models.Dentist: config.nhs_path.joinpath("dentists", "dentists.csv")
    }
    return _model_paths


def create_db_engine(config) -> engine:
    """Creates a network connection to the database
    :param config: object storing required file paths
    :return: Engine object holding the network connection
    """
    db_engine = create_engine(config.SQLITE_URI, echo=True)
    return db_engine


def create_db_and_tables(config) -> None:
    """Creates the database and tables
    :param config: object storing required file paths
    :return: None
    """
    db_engine = create_db_engine(config)
    SQLModel.metadata.create_all(db_engine)


def insert_objects(config) -> None:
    """Inserts data into tables in the database
    :param config: object storing required file paths
    :return: None
    """
    db_engine = create_db_engine(config)
    for model, nhs_file_path in model_paths(config).items():
        df = pd.read_csv(nhs_file_path, sep='|', encoding='ISO-8859-1', on_bad_lines='skip')
        sql_models = [model(**row) for row in df.to_dict("records")]
        with Session(db_engine) as session:
            session.bulk_save_objects(sql_models)
            session.commit()
