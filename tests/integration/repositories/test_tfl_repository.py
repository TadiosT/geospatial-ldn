from unittest import TestCase

from repositories.tfl_repository import TfLRepository


class TestTfLRepository(TestCase):
    under_test = TfLRepository()

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = cls.under_test.get_data()

    def test_data_returns_expected_consistent_key(self):
        expected_consistent_keys = {"Name", "mode", "line", "geometry"}
        total_keys = [set(mode.keys()) for mode in self.result]
        actual_consistent_keys = set.intersection(*total_keys)

        self.assertEqual(expected_consistent_keys, actual_consistent_keys)

    def test_data_returns_expected_modes(self):
        expected_consistent_keys = {"cable-car", "dlr", "national-rail", "overground", "replacement-bus", "river-bus",
                                    "river-tour", "tflrail", "tram", "tube"}
        actual_consistent_keys = {mode["mode"] for mode in self.result}

        self.assertTrue(actual_consistent_keys.issubset(expected_consistent_keys))

    def test_data_returns_expected_tfl_lines(self):
        expected_lines = {"Bakerloo", "Central", "Circle", "District", "Hammersmith & City", "Jubilee", "Metropolitan",
                          "Northern", "Piccadilly", "Victoria", "Waterloo & City"}
        actual_lines = {line["line"] for line in self.result}

        self.assertTrue(expected_lines.issubset(actual_lines))

    def test_data_returns_expected_number_of_stops(self):
        expected_minimum_number_of_stops = 4000
        actual_number_of_stops = len(self.result)

        self.assertGreater(actual_number_of_stops, expected_minimum_number_of_stops)
