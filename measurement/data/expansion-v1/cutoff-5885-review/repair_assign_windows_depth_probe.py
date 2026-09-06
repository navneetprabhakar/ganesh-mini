import unittest
from solution import assign_windows

class Probe(unittest.TestCase):
    def test_finite_payload(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            assign_windows([value], 1)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
