import unittest
from solution import parse_canvas_size


class ReviewProbe(unittest.TestCase):
    def test_in_range_dimension_with_leading_zeroes(self):
        error = None
        try:
            dimensions = parse_canvas_size('0' * 4300 + '1x2')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(dimensions, (1, 2))


if __name__ == '__main__':
    unittest.main()
