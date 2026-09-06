import unittest
from solution import apply_revisions

class Probe(unittest.TestCase):
    def test_finite_nested_snapshot(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            apply_revisions({'a': {'x': value}}, [])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
