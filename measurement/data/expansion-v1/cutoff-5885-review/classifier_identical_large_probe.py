import unittest
from solution import fit_centroid_classifier

class Probe(unittest.TestCase):
    def test_identical_finite_points_tie_zero(self):
        predict = fit_centroid_classifier([[1e308, 0], [1e308, 0]], [0, 1])
        self.assertEqual(predict([[1e308, 0]]), [0])

if __name__ == '__main__':
    unittest.main()
