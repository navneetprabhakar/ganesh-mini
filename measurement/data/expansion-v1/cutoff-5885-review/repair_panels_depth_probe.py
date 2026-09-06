import unittest
from solution import retitle_panels


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_metadata(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            retitle_panels([{'id': 1, 'title': 'old', 'meta': value}], 1, 'new')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
