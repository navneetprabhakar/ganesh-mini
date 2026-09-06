import unittest
from solution import evaluate_formula


class FormulaDepthBoundedTraceTests(unittest.TestCase):
    def test_nested_parentheses_without_recursion_error(self):
        recursion_failed = False
        try:
            value = evaluate_formula('(' * 400 + '1' + ')' * 400)
        except RecursionError:
            recursion_failed = True
        self.assertFalse(recursion_failed, 'RecursionError on 400 valid nested parentheses')
        self.assertEqual(value, 1)


if __name__ == '__main__':
    unittest.main()
