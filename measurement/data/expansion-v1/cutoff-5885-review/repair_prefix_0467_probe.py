import unittest
from solution import smallest_prefix_for_share


class Probe(unittest.TestCase):
    def test_zero_share_with_finite_large_values(self):
        self.assertEqual(smallest_prefix_for_share([1e308, 1e308], 0), [])


if __name__ == '__main__':
    unittest.main()
