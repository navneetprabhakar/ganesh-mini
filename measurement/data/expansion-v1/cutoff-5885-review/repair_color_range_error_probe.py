import unittest
from solution import make_color_cube


class ReviewProbe(unittest.TestCase):
    def test_out_of_range_large_integer_channel(self):
        with self.assertRaises(ValueError):
            make_color_cube(1, lambda *args: (10 ** 400, 0, 0))


if __name__ == '__main__':
    unittest.main()
