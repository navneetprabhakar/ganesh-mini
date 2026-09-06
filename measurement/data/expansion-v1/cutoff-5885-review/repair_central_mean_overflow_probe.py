import unittest
from solution import central_measure


class ReviewProbe(unittest.TestCase):
    def test_finite_representable_mean(self):
        self.assertEqual(central_measure([1e308, 1e308]), 1e308)


if __name__ == '__main__':
    unittest.main()
