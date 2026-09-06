import unittest
from solution import normalize_charge


class Probe(unittest.TestCase):
    def test_leading_zeroes_are_allowed(self):
        result = normalize_charge({'description': 'x', 'minor_units': '0'*4999 + '1'})
        self.assertEqual(result['minor_units'], 1)


if __name__ == '__main__':
    unittest.main()
