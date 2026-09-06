import unittest
from solution import quantile_positions


class QuantileEndpointTests(unittest.TestCase):
    def test_exact_last_index(self):
        length = 2**53 + 2
        self.assertEqual(quantile_positions(length, 2), [0, length - 1])


if __name__ == "__main__":
    unittest.main()
