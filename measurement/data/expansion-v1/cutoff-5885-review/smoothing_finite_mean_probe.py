import unittest
from solution import smooth_series


class FiniteMeanTests(unittest.TestCase):
    def test_constant_finite_series_all_schemes(self):
        for scheme in ("mean", "linear", "exponential"):
            with self.subTest(scheme=scheme):
                self.assertEqual(smooth_series([1e308, 1e308], 2, scheme), [None, 1e308])


if __name__ == "__main__":
    unittest.main()
