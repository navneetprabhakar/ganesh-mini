import unittest
from solution import pack_rows

class Probe(unittest.TestCase):
    def test_finite_nested_row(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            pack_rows([{'x': value}], 1)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
