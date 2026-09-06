import unittest
from solution import RegionAccumulator


class RegionSingleCellPrecisionTests(unittest.TestCase):
    def test_small_cell_not_lost_to_unrelated_prefix(self):
        accumulator = RegionAccumulator([[1e16, 1.0]])
        self.assertEqual(accumulator.rectangle_total(0, 1, 1, 2), 1.0)


if __name__ == '__main__':
    unittest.main()
