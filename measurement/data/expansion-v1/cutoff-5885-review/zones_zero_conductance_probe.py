import unittest
from solution import simulate_zones


class ZeroConductionTests(unittest.TestCase):
    def test_zero_conductance_preserves_finite_extremes(self):
        zones = [{"name": "a", "temperature": -1e308, "capacity": 1},
                 {"name": "b", "temperature": 1e308, "capacity": 1}]
        targets = {"a": (-1e308, -1e308), "b": (1e308, 1e308)}
        self.assertEqual(simulate_zones(zones, [("a", "b", 0)], targets, 1),
                         [{"name": "a", "temperature": -1e308},
                          {"name": "b", "temperature": 1e308}])


if __name__ == "__main__":
    unittest.main()
