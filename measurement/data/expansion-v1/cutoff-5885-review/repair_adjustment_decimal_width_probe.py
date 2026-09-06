import unittest
from solution import aggregate_adjustments


class ReviewProbe(unittest.TestCase):
    def test_valid_large_decimal_quantity_with_zero_adjustment(self):
        line = 'AB12 ' + '1' * 4301 + ' +0'
        error = None
        try:
            result = aggregate_adjustments([line])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, {'AB12': 0})


if __name__ == '__main__':
    unittest.main()
