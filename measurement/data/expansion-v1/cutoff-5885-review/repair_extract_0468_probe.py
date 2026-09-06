import unittest
from solution import extract_table


class Probe(unittest.TestCase):
    def test_finite_nested_value(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            extract_table([{'x': value}], ['x'])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
