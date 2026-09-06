import unittest
from solution import join_tiles

class Probe(unittest.TestCase):
    def test_finite_nested_cell(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            join_tiles([[[value]]])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
