import unittest
from decimal import Decimal, localcontext
from solution import sum_measurements


class ReviewProbe(unittest.TestCase):
    def test_opposite_exponent_span(self):
        expected = Decimal('1' + '0' * 99 + '.' + '0' * 99 + '1')
        self.assertEqual(sum_measurements(['1e99', '1e-100']), expected)

    def test_invalid_text_does_not_change_caller_flags(self):
        with localcontext() as context:
            context.clear_flags()
            before = dict(context.flags)
            with self.assertRaises(ValueError):
                sum_measurements(['not-a-number'])
            self.assertEqual(dict(context.flags), before)


if __name__ == '__main__':
    unittest.main()
