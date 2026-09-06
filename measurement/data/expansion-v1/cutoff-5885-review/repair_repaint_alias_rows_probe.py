import unittest
from solution import repaint_exterior

class Probe(unittest.TestCase):
    def test_independent_replacements_shared_input_rows(self):
        row = [1]
        result = repaint_exterior([row, row], 1, {'items': []})
        self.assertIsNot(result[0][0], result[1][0])

    def test_finite_deep_cell(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            repaint_exterior([[value]], 1, 2)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
