import unittest
from solution import select_rows

class Probe(unittest.TestCase):
    def test_finite_nested_row(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            select_rows([{'x': value}], {})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
