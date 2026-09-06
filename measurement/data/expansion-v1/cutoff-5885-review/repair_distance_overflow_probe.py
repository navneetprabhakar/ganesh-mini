import unittest
from solution import shortest_distance_km

class Probe(unittest.TestCase):
    def test_reachable_finite_kilometers(self):
        graph = {'a': {'b': 1e308}, 'b': {'c': 1e308}, 'c': {}}
        result = shortest_distance_km(graph, 'a', 'c')
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result / 2e305, 1.0)

    def test_same_endpoint_with_finite_integer_edge(self):
        graph = {'a': {'b': 10**400}, 'b': {}}
        self.assertEqual(shortest_distance_km(graph, 'a', 'a'), 0.0)

if __name__ == '__main__':
    unittest.main()
