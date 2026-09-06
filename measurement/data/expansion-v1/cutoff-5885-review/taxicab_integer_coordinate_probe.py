import unittest
from solution import taxicab_distance


class IntegerCoordinateTests(unittest.TestCase):
    def test_large_finite_coordinates_have_small_exact_distance(self):
        x = 10**400
        self.assertEqual(taxicab_distance((x, 0), (x + 3, 4)), 7.0)


if __name__ == "__main__":
    unittest.main()
