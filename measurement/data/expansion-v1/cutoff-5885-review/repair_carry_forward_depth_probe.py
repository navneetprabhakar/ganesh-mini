import unittest
from solution import carry_forward


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_nonmarker_cell(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            carry_forward([[value], [None]])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
