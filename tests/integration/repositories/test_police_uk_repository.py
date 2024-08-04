from unittest import TestCase

from repositories.police_uk_repository import PoliceUKRepository
from services.geospatial_service import GeospatialService
import datetime
from dateutil.relativedelta import relativedelta


class TestPoliceUKRepository(TestCase):
    under_test = PoliceUKRepository()
    geo_service = GeospatialService()

    @classmethod
    def setUpClass(cls):
        cls.categories_result = cls.under_test.get_categories("2020-12")
        cls.crime_result = cls.under_test.get_data("Newham", "All crime",
                                                   {"All crime": "all-crime",
                                                    "Anti-social behaviour": "anti-social-behaviour",
                                                    "Bicycle theft": "bicycle-theft",
                                                    "Burglary": "burglary",
                                                    "Criminal damage and arson": "criminal-damage-arson",
                                                    "Drugs": "drugs",
                                                    "Other theft": "other-theft",
                                                    "Possession of weapons": "possession-of-weapons",
                                                    "Public order": "public-order",
                                                    "Robbery": "robbery",
                                                    "Shoplifting": "shoplifting",
                                                    "Theft from the person": "theft-from-the-person",
                                                    "Vehicle crime": "vehicle-crime",
                                                    "Violent and sexual offences": "violent-crime",
                                                    "Other crime": "other-crime"},
                                                   str((datetime.date.today() - relativedelta(months=5)).strftime("%Y"
                                                                                                                  "-%m")),
                                                   cls.geo_service.borough_bounds)

    def test_get_categories_returns_list_of_dicts(self):
        count = 0
        if isinstance(self.categories_result, list):
            for category in self.categories_result:
                if isinstance(category, dict):
                    count += 1

        self.assertEqual(count, len(self.categories_result))

    def test_get_categories_returns_url_and_name_pairs(self):
        expected_consistent_keys = {"url", "name"}
        total_keys = [set(categories.keys()) for categories in self.categories_result]
        actual_consistent_keys = set.intersection(*total_keys)

        self.assertEqual(expected_consistent_keys, actual_consistent_keys)

    def test_get_categories_returns_string_values(self):
        expected_consistent_type = {"'str'"}
        total_values = []
        for category in self.categories_result:
            for value in category.values():
                value_type = str(type(value))
                total_values.append(value_type.lstrip('"<class "').rstrip('>"'))
        actual_consistent_types = set.intersection(set(total_values))

        self.assertEqual(expected_consistent_type, actual_consistent_types)

    def test_get_data_returns_less_than_10000_crimes(self):
        maximum_number_of_crimes = 10000
        actual_number_of_crimes = len(self.crime_result)

        self.assertLess(actual_number_of_crimes, maximum_number_of_crimes)
