import unittest
from solution import rank_numeric_fields


class RankFieldIntegerDifferenceTests(unittest.TestCase):
    def test_small_exact_difference_between_large_integer_means(self):
        rows = [{'y': 0, 'x': 2 ** 53}, {'y': 1, 'x': 2 ** 53 + 1}]
        self.assertEqual(rank_numeric_fields(rows, 'y'), [('x', 1)])


if __name__ == '__main__':
    unittest.main()
