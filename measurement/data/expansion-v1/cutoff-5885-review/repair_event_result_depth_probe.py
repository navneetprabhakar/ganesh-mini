import unittest
from solution import dispatch_event


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_handler_result(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        calls = []
        def handler(event):
            calls.append(event)
            return value
        error = None
        try:
            dispatch_event({'kind': 'x'}, {'x': handler})
        except Exception as exc:
            error = type(exc).__name__
        self.assertEqual(len(calls), 1)
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
