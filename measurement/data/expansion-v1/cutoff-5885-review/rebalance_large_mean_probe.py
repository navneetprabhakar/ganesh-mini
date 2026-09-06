import unittest
from solution import rebalance_table

class Probe(unittest.TestCase):
    def test_identical_finite_column(self):
        self.assertEqual(rebalance_table([[1e308], [1e308]], 1e308), [[5e307], [5e307]])

if __name__ == '__main__':
    unittest.main()
