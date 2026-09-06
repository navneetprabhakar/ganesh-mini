import unittest
from solution import build_progression_lines


class ProgressionDecimalLimitTests(unittest.TestCase):
    def test_single_large_integer_line(self):
        decimal = '1' + '0' * 4300
        self.assertEqual(build_progression_lines(10 ** 4300, 0), (decimal + ' + 0 = ' + decimal,))


if __name__ == '__main__':
    unittest.main()
