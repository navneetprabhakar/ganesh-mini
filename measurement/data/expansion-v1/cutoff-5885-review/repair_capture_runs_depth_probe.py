import unittest
from solution import capture_runs

class Probe(unittest.TestCase):
    def test_finite_frame(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            capture_runs([value], [True])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
