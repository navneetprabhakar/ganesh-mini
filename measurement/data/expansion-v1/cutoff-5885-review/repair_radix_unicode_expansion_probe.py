import unittest
from solution import compare_radix_literals


class ReviewProbe(unittest.TestCase):
    def test_unicode_letter_outside_digit_alphabet(self):
        with self.assertRaises(ValueError):
            compare_radix_literals([('invalid', 'ß', 36)])


if __name__ == '__main__':
    unittest.main()
