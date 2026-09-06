import unittest
from solution import canvas_pixels


class ReviewProbe(unittest.TestCase):
    def test_exact_integer_product_is_not_changed_by_rounding(self):
        value = 2 ** 52 + 1
        self.assertEqual(canvas_pixels(value, 1, 1), (value, 1))


if __name__ == '__main__':
    unittest.main()
