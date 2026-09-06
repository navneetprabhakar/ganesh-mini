import unittest
from solution import make_batches


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_item(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            make_batches([value], 1)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
