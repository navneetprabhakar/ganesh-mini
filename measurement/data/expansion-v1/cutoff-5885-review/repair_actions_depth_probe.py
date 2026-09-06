import unittest
from solution import normalize_actions


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_payload(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            normalize_actions([{'at': 1, 'kind': 'x', 'payload': {'data': value}}])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
