import unittest
from solution import reshape_values


class ReviewProbe(unittest.TestCase):
    def test_finite_rank_with_one_scalar(self):
        error = None
        try:
            result = reshape_values([1], (1,) * 600)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        for _ in range(600):
            result = result[0]
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
