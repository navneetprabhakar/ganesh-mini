import unittest
from solution import bracketed_zero


class Probe(unittest.TestCase):
    def test_nonzero_constant_not_bracketed(self):
        with self.assertRaises(ValueError):
            bracketed_zero([1e-200], 0, 1, 1)


if __name__ == '__main__':
    unittest.main()
