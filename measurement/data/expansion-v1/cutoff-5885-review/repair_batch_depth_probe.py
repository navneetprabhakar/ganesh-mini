import unittest
from solution import TaskBatch


class ReviewProbe(unittest.TestCase):
    def test_finite_nested_payload_while_open(self):
        value = []
        cursor = value
        for _ in range(600):
            child = []
            cursor.append(child)
            cursor = child
        batch = TaskBatch()
        error = None
        try:
            batch.add(value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(len(batch), 1)


if __name__ == '__main__':
    unittest.main()
