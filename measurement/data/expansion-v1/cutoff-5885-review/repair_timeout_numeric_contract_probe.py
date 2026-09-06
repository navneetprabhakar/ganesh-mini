import unittest
from fractions import Fraction
from solution import normalize_timeout


class Probe(unittest.TestCase):
    def test_non_int_float_rejected(self):
        with self.assertRaises(TypeError):
            normalize_timeout(Fraction(1, 2))

    def test_negative_integer_value_error(self):
        with self.assertRaises(ValueError):
            normalize_timeout(-(10**400))


if __name__ == '__main__':
    unittest.main()
