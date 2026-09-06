import unittest
from solution import build_record


class Probe(unittest.TestCase):
    def test_finite_fields(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            build_record('title', {'value': value})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
