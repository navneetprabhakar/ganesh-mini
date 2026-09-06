import unittest
from solution import minimum_tour


class Probe(unittest.TestCase):
    def test_finite_singleton_diagonal(self):
        self.assertEqual(minimum_tour([[10**400]]), ([0, 0], 0.0))

    def test_overflow_does_not_change_best_route(self):
        costs = [[0, 1e308, 9e307], [9e307, 0, 1e308], [1e308, 9e307, 0]]
        self.assertEqual(minimum_tour(costs)[0], [0, 2, 1, 0])


if __name__ == '__main__':
    unittest.main()
