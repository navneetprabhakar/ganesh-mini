import unittest
from solution import sort_assets


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
            sort_assets([{'rank': 1, 'meta': value}], 'rank')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
