import unittest
from solution import axis_sums

class Probe(unittest.TestCase):
    def test_contract(self):
        with self.assertRaises((TypeError, ValueError)):
            axis_sums([[b'a']], 0)

    def test_finite_integer(self):
        self.assertEqual(axis_sums([[[10**400]]], 0), [[10**400]])

if __name__ == '__main__':
    unittest.main()
