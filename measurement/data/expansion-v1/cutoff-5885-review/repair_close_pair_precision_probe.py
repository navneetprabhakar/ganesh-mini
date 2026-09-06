import unittest
from solution import has_close_pair


class Probe(unittest.TestCase):
    def test_distinct_integer_precision(self):
        self.assertFalse(has_close_pair([2**53, 2**53 + 1], 0.5))

    def test_finite_large_integer(self):
        self.assertFalse(has_close_pair([10**400], 1))


if __name__ == '__main__':
    unittest.main()
