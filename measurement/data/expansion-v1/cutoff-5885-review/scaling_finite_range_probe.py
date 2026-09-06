import unittest
from solution import scale_readings


class ReviewProbe(unittest.TestCase):
    def test_finite_extreme_endpoints(self):
        self.assertEqual(scale_readings([-1e308, 1e308]), [0.0, 1.0])


if __name__ == '__main__':
    unittest.main()
