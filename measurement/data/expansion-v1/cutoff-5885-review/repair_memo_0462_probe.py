import unittest
from solution import MemoTable


class Probe(unittest.TestCase):
    def test_finite_nested_value(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            MemoTable().get_or_compute('x', lambda: value)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
