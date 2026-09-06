import unittest
from solution import TaskRunner


class Probe(unittest.TestCase):
    def test_finite_result(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            TaskRunner(True).execute('one', lambda: value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
