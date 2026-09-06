import unittest
from solution import evaluate_formula


class FormulaDepthDecimalTests(unittest.TestCase):
    def test_valid_nested_parentheses(self):
        self.assertEqual(evaluate_formula('(' * 400 + '1' + ')' * 400), 1)

    def test_decimal_with_leading_zeroes(self):
        self.assertEqual(evaluate_formula('0' * 5000 + '1'), 1)


if __name__ == '__main__':
    unittest.main()
