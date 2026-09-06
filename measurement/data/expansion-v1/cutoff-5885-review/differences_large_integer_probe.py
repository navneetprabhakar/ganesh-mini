import unittest
from solution import format_differences


class ReviewProbe(unittest.TestCase):
    def test_arbitrarily_large_integer(self):
        digits = '1' + '0' * 5000
        self.assertEqual(format_differences([[10 ** 5000, 0]]),
                         ['Entry 1: ' + digits + ' - 0 = ' + digits])


if __name__ == '__main__':
    unittest.main()
