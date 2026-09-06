import unittest
from solution import dispatch_primary


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_payload(self):
        payload = []
        cursor = payload
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        error = None
        try:
            result = dispatch_primary([{'channel': 'p', 'payload': payload}],
                                      {'p': [lambda value: len(value)]}, 'p')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, [1])


if __name__ == '__main__':
    unittest.main()
