import unittest
from solution import RoutePlan

class RouteIntegerProbe(unittest.TestCase):
    def test_large_integer_coordinates_with_small_representable_distance(self):
        x = 10 ** 400
        plan = RoutePlan([(x, 0), (x + 3, 4)])
        self.assertEqual(plan.total_manhattan_distance(), 7.0)

if __name__ == '__main__':
    unittest.main()
