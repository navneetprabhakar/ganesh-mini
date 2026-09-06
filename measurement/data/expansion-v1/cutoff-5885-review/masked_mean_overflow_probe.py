import unittest

from solution import masked_row_means


class FiniteMeanTests(unittest.TestCase):
    def test_representable_mean_of_large_finite_values(self):
        self.assertEqual(masked_row_means([[1e308, 1e308]], [[True, True]]), (1e308,))


if __name__ == "__main__":
    unittest.main()
