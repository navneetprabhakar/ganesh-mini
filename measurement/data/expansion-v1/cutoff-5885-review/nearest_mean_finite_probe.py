import unittest
from solution import NearestMean


class FiniteMeanProbe(unittest.TestCase):
    def test_representable_mean_of_large_finite_values(self):
        model = NearestMean()
        model.fit([[1e308], [1e308]], ['x', 'x'])
        self.assertEqual(model.model_snapshot()['centroids']['x'], [1e308])

    def test_large_finite_distances_still_select_nearest_label(self):
        model = NearestMean()
        model.fit([[1e200], [2e200]], ['near', 'far'])
        self.assertEqual(model.predict([[0.0]]), ['near'])


if __name__ == '__main__':
    unittest.main()
