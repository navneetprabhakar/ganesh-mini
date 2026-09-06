import unittest
from solution import CentroidIndex

class Probe(unittest.TestCase):
    def test_large_finite_distance(self):
        model = CentroidIndex(1, max_iterations=1).fit([[0], [1e200]])
        self.assertEqual(model.centers, [[5e199]])

    def test_repeated_large_point_mean(self):
        model = CentroidIndex(1, max_iterations=1).fit([[1e308], [1e308]])
        self.assertEqual(model.centers, [[1e308]])

if __name__ == '__main__':
    unittest.main()
