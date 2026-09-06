import unittest
from solution import radius_components


class RadiusUnderflowTests(unittest.TestCase):
    def test_zero_radius_does_not_connect_distinct_tiny_points(self):
        self.assertEqual(radius_components([(0.0, 0.0), (1e-200, 0.0)], 0),
                         {"labels": [0, 1], "components": [(0,), (1,)]})


if __name__ == "__main__":
    unittest.main()
