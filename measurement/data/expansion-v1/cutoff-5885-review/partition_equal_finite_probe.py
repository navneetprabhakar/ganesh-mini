import unittest
from solution import exact_partition_report


class PartitionFiniteTests(unittest.TestCase):
    def test_equal_finite_groups_have_zero_differences(self):
        self.assertEqual(exact_partition_report([1e308, 1e308], [1e308, 1e308]), {"observed": 0.0, "differences": (0.0,) * 6, "extreme_fraction": 1.0})


if __name__ == "__main__":
    unittest.main()
