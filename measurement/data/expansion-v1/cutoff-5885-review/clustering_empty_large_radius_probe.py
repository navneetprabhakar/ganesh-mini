import unittest
from solution import cluster_points


class ClusteringEmptyLargeRadiusTests(unittest.TestCase):
    def test_empty_input_with_finite_positive_radius(self):
        self.assertEqual(cluster_points([], radius=1e200, min_size=1), {'clusters': [], 'noise': []})


if __name__ == '__main__':
    unittest.main()
