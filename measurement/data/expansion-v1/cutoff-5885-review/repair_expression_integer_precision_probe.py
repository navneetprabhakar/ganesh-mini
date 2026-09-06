import unittest
from solution import evaluate_expression


class ReviewProbe(unittest.TestCase):
    def test_integer_difference_with_exact_float_result(self):
        self.assertEqual(evaluate_expression([2 ** 53 + 1, 2 ** 53, '-'], {}), 1.0)


if __name__ == '__main__':
    unittest.main()
