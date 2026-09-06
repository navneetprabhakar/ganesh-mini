import unittest
from solution import make_scalers


class ReviewProbe(unittest.TestCase):
    def test_finite_integer_factor(self):
        self.assertEqual(make_scalers([10 ** 400])[0](0), 0)

    def test_finite_integer_argument(self):
        self.assertEqual(make_scalers([0])[0](10 ** 400), 0)


if __name__ == '__main__':
    unittest.main()
