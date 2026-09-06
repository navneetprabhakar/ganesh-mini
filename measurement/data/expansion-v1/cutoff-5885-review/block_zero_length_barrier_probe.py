import unittest

from solution import BlockCompactor


class ZeroLengthBarrierTests(unittest.TestCase):
    def test_zero_length_block_does_not_hide_overlapping_interval(self):
        block = BlockCompactor.Block
        result = BlockCompactor.merge([block(0, 10), block(5, 5), block(6, 12)])
        pairs = [(item.start, item.end) for item in result]
        self.assertCountEqual(pairs, [(0, 12), (5, 5)])


if __name__ == "__main__":
    unittest.main()
