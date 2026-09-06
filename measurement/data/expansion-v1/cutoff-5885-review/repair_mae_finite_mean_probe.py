import unittest
from solution import mean_absolute_error


class ReviewProbe(unittest.TestCase):
    def test_finite_representable_mean(self):
        self.assertEqual(mean_absolute_error([1e308, 1e308], [0, 0]), 1e308)


if __name__ == '__main__':
    unittest.main()
