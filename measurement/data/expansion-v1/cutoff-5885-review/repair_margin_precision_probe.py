import unittest
from solution import labels_from_margins

class Probe(unittest.TestCase):
    def test_distinct_integers_not_rounded_together(self):
        self.assertEqual(labels_from_margins([2**53], 2**53+1), [-1])

    def test_finite_huge_integer(self):
        self.assertEqual(labels_from_margins([10**400], 0), [1])

if __name__ == '__main__':
    unittest.main()
