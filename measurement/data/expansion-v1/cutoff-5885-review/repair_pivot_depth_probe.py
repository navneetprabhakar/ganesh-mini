import unittest
from solution import pivot_rows


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_cell(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            pivot_rows([[value]])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
