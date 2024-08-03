from typing import List

from sqlmodel import Session, select, SQLModel

from database import create_db_engine
from models.nhs_models import GP, Hospital, Pharmacy, Dentist, PharmacyService, GPService
from repositories.base_repository import BaseRepository


class NHSRepository(BaseRepository):

    def __init__(self):
        super().__init__()

    def get_data(self, organisation: str) -> List[SQLModel]:
        """Uses switch case statements to generate a list of SQLModel objects based on a user input
        :param organisation: name of the nhs organisation which has been selected by a user (Hospital, Pharmacy etc.)
        :return: a list of SQLModel objects
        """
        match organisation:
            case "Hospitals":
                model = Hospital
            case "Pharmacies":
                model = Pharmacy
            case "GP":
                model = GP
            case "Dentists":
                model = Dentist
            case _:
                raise RuntimeError("This NHS Service does not exist")

        engine = create_db_engine(self.config)
        with Session(engine) as session:
            data = session.exec(select(model)).all()

        return data

    def get_services(self, organisation: str) -> List[SQLModel]:
        match organisation:
            case "Pharmacies":
                model = PharmacyService
            case "GP":
                model = GPService
            case _:
                raise RuntimeError("This NHS Service does not exist")

        engine = create_db_engine(self.config)
        with Session(engine) as session:
            data = session.exec(select(model)).all()

        return data
