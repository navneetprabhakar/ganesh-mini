import unittest

from solution import LinearFit


class SmallDistinctInputTests(unittest.TestCase):
    def test_distinct_finite_x_values_fit_unit_slope(self):
        fitted = LinearFit.fit([0.0, 1e-200], [0.0, 1e-200])
        self.assertAlmostEqual(fitted.slope, 1.0)
        self.assertEqual(fitted.intercept, 0.0)


if __name__ == "__main__":
    unittest.main()
