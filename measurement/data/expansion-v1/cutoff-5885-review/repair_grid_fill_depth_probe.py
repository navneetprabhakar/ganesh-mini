import unittest
from solution import make_grid


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_fill(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            make_grid(1, 1, value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
