import unittest
from solution import interval_midpoint

class Probe(unittest.TestCase):
    def test_degenerate_finite_interval(self):
        self.assertEqual(interval_midpoint(1e308, 1e308), 1e308)

if __name__ == '__main__':
    unittest.main()
