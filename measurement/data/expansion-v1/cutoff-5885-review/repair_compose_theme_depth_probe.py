import unittest
from solution import compose_theme

class Probe(unittest.TestCase):
    def test_finite_nested_base(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            compose_theme({'x': value}, {})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
