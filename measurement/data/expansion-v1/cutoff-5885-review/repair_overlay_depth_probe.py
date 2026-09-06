import unittest
from solution import overlay_rows


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_row(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            overlay_rows([{'id': 'a', 'data': value}], [], 'merge')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
