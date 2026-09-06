import unittest
from solution import merge_directory

class Probe(unittest.TestCase):
    def test_finite_nested_data(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            merge_directory(['x'], {'x': {'value': value}})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
