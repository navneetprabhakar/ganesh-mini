import unittest
from solution import triangular_total


class ReviewProbe(unittest.TestCase):
    def test_nonnegative_integer_outside_linear_recursion_depth(self):
        error = None
        try:
            result = triangular_total(1100)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, 605550)


if __name__ == '__main__':
    unittest.main()
