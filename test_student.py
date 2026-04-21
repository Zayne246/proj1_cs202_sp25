import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade. 
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_holder(self):

        pass
    
    def test_emissions_per_capita(self):
        self.assertAlmostEqual(emissions_per_capita(sf_condition), 4120000.0 / 827500, places=4)
        self.assertAlmostEqual(emissions_per_capita(cs_condition), 0.0, places=4)
    
    def test_area(self):
        expected = 6378.1**2 * math.radians(0.17) * abs(math.sin(math.radians(37.81)) - math.sin(math.radians(37.70)))
        self.assertAlmostEqual(area(sf_rect), expected, places=4)
        wrap_rect = GlobeRect(0.0, 10.0, 170.0, -170.0)
        self.assertGreater(area(wrap_rect), 0.0)
        self.assertLess(area(wrap_rect), 10_000_000)

    def test_emissions_per_square_km(self):
        expected = sf_condition.ghg_rate / area(sf_rect)
        self.assertAlmostEqual(emissions_per_square_km(sf_condition), expected, places=4)
        self.assertEqual(emissions_per_square_km(cs_condition), 0.0)
    def test_densest_rc(self):
        self.assertEqual(densest_rc([sf_condition]).region.name, "San Francisco")
        self.assertEqual(densest_rc([cs_condition]).region.name, "Caribbean Sea")
        self.assertEqual(densest_rc(region_conditions).region.name, "San Francisco")

    def test_densest(self):
        self.assertEqual(densest([sf_condition]), "San Francisco")
        self.assertEqual(densest([cs_condition]), "Caribbean Sea")

    def test_growth_rate(self):
        self.assertAlmostEqual(growth_rate("ocean"), 0.0001, places=4)
        self.assertAlmostEqual(growth_rate("mountains"), 0.0005, places=4)
        self.assertAlmostEqual(growth_rate("forest"), -0.00001, places=4)
        self.assertAlmostEqual(growth_rate("other"), 0.0003, places=4)

    def test_project_condition(self):
        years = 10
        rate = growth_rate(sf_condition.region.terrain) # Get the actual rate
        projected = project_condition(sf_condition, years)
        new_pop = sf_condition.pop * (1 + rate) ** years
        expected_pop = int(new_pop)
        expected_ghg = sf_condition.ghg_rate * (new_pop / sf_condition.pop)
        self.assertEqual(projected.year, sf_condition.year + years)
        self.assertEqual(projected.pop, expected_pop)
        self.assertAlmostEqual(projected.ghg_rate, expected_ghg, places=2)

if __name__ == '__main__':
    unittest.main()
