import unittest
from solution import needs_upgrade


class Probe(unittest.TestCase):
    def test_allowed_leading_zeroes(self):
        self.assertTrue(needs_upgrade('0'*4999 + '1', '2'))


if __name__ == '__main__':
    unittest.main()
