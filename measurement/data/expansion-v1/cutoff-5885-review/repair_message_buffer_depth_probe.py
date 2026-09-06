import unittest
from solution import MessageBuffer


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_payload(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        buffer = MessageBuffer()
        error = None
        try:
            buffer.add('id', value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(buffer.pending_count(), 1)


if __name__ == '__main__':
    unittest.main()
