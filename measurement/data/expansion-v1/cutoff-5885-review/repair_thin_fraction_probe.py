import unittest
from fractions import Fraction
from solution import thin_points


class ReviewProbe(unittest.TestCase):
    def test_finite_real_coordinates(self):
        self.assertEqual(thin_points([(Fraction(1, 2), 0)], 0), [(0.5, 0.0)])

    def test_finite_real_minimum(self):
        self.assertEqual(thin_points([(0, 0)], Fraction(1, 2)), [(0.0, 0.0)])


if __name__ == '__main__':
    unittest.main()
