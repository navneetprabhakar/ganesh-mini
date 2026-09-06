import unittest
from solution import first_lucas_term_with_digits


class LucasDigitLimitTests(unittest.TestCase):
    def test_exact_threshold_beyond_decimal_conversion_limit(self):
        threshold = 10 ** 4300
        previous, current, index = 2, 1, 1
        while current < threshold:
            previous, current = current, previous + current
            index += 1
        self.assertEqual(first_lucas_term_with_digits(4301), index)


if __name__ == '__main__':
    unittest.main()
