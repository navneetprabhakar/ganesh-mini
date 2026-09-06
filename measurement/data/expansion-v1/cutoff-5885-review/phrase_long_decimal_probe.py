import unittest
from solution import analyze_phrase


class PhraseLongDecimalTests(unittest.TestCase):
    def test_digit_run_with_leading_zeroes(self):
        self.assertEqual(analyze_phrase('0' * 5000 + '7')['quantities'], [7])


if __name__ == '__main__':
    unittest.main()
