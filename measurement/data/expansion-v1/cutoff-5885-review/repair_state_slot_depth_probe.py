import unittest
from solution import StateSlot


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_initial_value(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            StateSlot(value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
