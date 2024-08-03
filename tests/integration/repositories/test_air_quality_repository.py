from unittest import TestCase

from repositories.air_quality_repository import AirQualityRepository


class TestAirQualityRepository(TestCase):
    under_test = AirQualityRepository()

    @classmethod
    def setUpClass(cls) -> None:
        cls.result = cls.under_test.get_data()

    def test_get_data_returns_expected_consistent_key(self):
        expected_consistent_key = "@LocalAuthorityName"
        total_keys = [set(borough.keys()) for borough in self.result]
        actual_consistent_keys = set.intersection(*total_keys)

        self.assertIn(expected_consistent_key, actual_consistent_keys)

    def test_get_data_returns_expected_consistent_keys_in_site(self):
        expected_consistent_site_keys = ["@SiteCode", "@SiteName", "@Latitude", "@Longitude"]
        site_keys = []
        for borough in self.result:
            if "Site" in borough:
                site = borough["Site"]
                if isinstance(site, dict):
                    site = [site]
                for site in site:
                    site_keys.append(set(site.keys()))
        actual_consistent_site_keys = set.intersection(*site_keys)

        self.assertTrue(set(expected_consistent_site_keys).issubset(set(actual_consistent_site_keys)))

    def test_get_data_returns_expected_consistent_keys_in_species(self):
        expected_consistent_species_keys = ["@SpeciesCode", "@SpeciesDescription", "@AirQualityIndex", "@AirQualityBand"
                                            ]
        species_keys = []
        for borough in self.result:
            if "Site" in borough:
                sites = borough["Site"]
                if isinstance(sites, dict):
                    sites = [sites]
                for site in sites:
                    if "Species" in site:
                        species = site["Species"]
                        if isinstance(species, dict):
                            species = [species]
                        for species in species:
                            species_keys.append(set(species.keys()))
        actual_consistent_species_keys = set.intersection(*species_keys)

        self.assertTrue(set(expected_consistent_species_keys).issubset(set(actual_consistent_species_keys)))
