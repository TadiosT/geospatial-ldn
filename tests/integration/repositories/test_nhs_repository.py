from unittest import TestCase

from sqlmodel import SQLModel

from repositories.nhs_repository import NHSRepository


class TestNHSRepository(TestCase):
    under_test = NHSRepository()

    @classmethod
    def setUpClass(cls):
        cls.organisations = ["Hospitals", "Pharmacy", "GP", "Dentists"]
        cls.result = cls.under_test.get_data

    def test_get_data_returns_list_of_SQLModel_objects(self):
        #TODO: Fix this test
        bool_list = []
        expected_value = SQLModel
        for org in self.organisations:
            if isinstance(self.result(org)[0], SQLModel):
                bool_list.append(True)

        actual_value = set(bool_list)

        self.assertEqual(expected_value, actual_value)
