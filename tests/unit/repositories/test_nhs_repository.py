from pathlib import Path
from unittest import TestCase
import pandas as pd
from sqlmodel import SQLModel

from config import Config
from main import init_db
from models.nhs_models import Hospital, Pharmacy
from repositories.nhs_repository import NHSRepository
from tests.test_config import TestConfig


class TestNHSRepository(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = TestConfig()
        init_db(config)
        cls.under_test = NHSRepository()

    @classmethod
    def tearDownClass(cls) -> None:
        config = TestConfig()
        Path(config.SQLITE_PATH).unlink()

    def test_get_hospital_data(self):
        actual = self.under_test.get_data("Hospitals")
        expected = [Hospital(OrganisationID="17970", OrganisationCode=Hospital, OrganisationType="Independent Sector",
                             SubType="Visible", Sector=True, OrganisationStatus=None, IsPimsManaged=None,
                             OrganisationName="Walton Community Hospital - Virgin Care Services Ltd", Address1=None,
                             Address2="Rodney Road", Address3=None, City="Walton-on-Thames", County="Surrey",
                             Postcode="KT12 3LD", Latitude=51.379997253417969, Longitude=-0.40604206919670105,
                             ParentODSCode="NDA", ParentName="Virgin Care Services Ltd", Phone="01932 414205",
                             Email=None, Website=None, Fax="01932 253674"),
                    Hospital(OrganisationID="17981", OrganisationCode=Hospital, OrganisationType="Independent Sector",
                             SubType="Visible", Sector=True, OrganisationStatus=None, IsPimsManaged=None,
                             OrganisationName="Woking Community Hospital (Virgin Care)", Address1=None,
                             Address2="Heathside Road", Address3=None, City="Woking", County="Surrey",
                             Postcode="GU22 7HS", Latitude=51.315132141113281, Longitude=-0.55628949403762817,
                             ParentODSCode="NDA", ParentName="Virgin Care Services Ltd", Phone="01483 715911",
                             Email=None, Website=None, Fax=None)]
        expected_pd = pd.Series(expected[0].dict())
        actual_pd = pd.Series(actual[0].dict())
        print(expected[0])
        pd.Series.equals(expected_pd, actual_pd)

    def test_get_pharmacy_data(self):
        actual = self.under_test.get_data("Pharmacies")
        expected = [Pharmacy(OrganisationID=13043, OrganisationCode="FA512", OrganisationType="Pharmacy",
                             SubType="Community Pharmacy",
                             OrganisationStatus="Visible", IsPimsManaged=False, IsEPSEnabled=True,
                             OrganisationName="Lords Pharmacy",
                             Address1="UNIT 61", Address2="THE GUINEAS SHOPPING CTR", Address3="NEWMARKET",
                             City="SUFFOLK",
                             County=None, Postcode="CB8 8EQ", Latitude=52.244796752929688, Longitude=0.4055977463722229,
                             ParentODSCode="QJG", ParentName="Suffolk and North East Essex STP", Phone="01638 428022",
                             Email=None, Website="https://www.lordspharmacynewmarket.co.uk/", Fax="01638 428022"),
                    Pharmacy(OrganisationID=13046, OrganisationCode="FAP38", OrganisationType="Pharmacy",
                             SubType="Community Pharmacy", OrganisationStatus="Visible", IsPimsManaged=False,
                             IsEPSEnabled=True, OrganisationName="LLOYDSPHARMACY", Address1="SAINSBURY'S STORE",
                             Address2="CHURCH STREET", Address3="CARLISLE", City="CUMBRIA", County=None,
                             Postcode="CA2 5TF", Latitude=54.894672393798828, Longitude=-2.9472866058349609,
                             ParentODSCode="QHM", ParentName="Cumbria and North East STP", Phone="01228533915",
                             Email="lp5045@lloydspharmacy.co.uk", Website="http://www.lloydspharmacy.com", Fax=None)]

        expected_series = pd.Series(expected[0].dict())
        actual_series = pd.Series(actual[0].dict())

        pd.Series.equals(expected_series, actual_series)





