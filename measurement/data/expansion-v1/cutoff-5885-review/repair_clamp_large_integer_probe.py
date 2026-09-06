import unittest
from solution import clamp_scaled


class ReviewProbe(unittest.TestCase):
    def test_finite_integer_with_representable_clamped_result(self):
        self.assertEqual(clamp_scaled(10 ** 400, 1, 1), 1.0)


if __name__ == '__main__':
    unittest.main()
