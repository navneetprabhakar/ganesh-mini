import unittest
from solution import cumulative_total


class ReviewProbe(unittest.TestCase):
    def test_nonnegative_integer_beyond_linear_recursion_limit(self):
        error = None
        try:
            result = cumulative_total(1100)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, 605550)


if __name__ == '__main__':
    unittest.main()
