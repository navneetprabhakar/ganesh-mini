import unittest
from solution import run_pipeline

class Probe(unittest.TestCase):
    def test_finite_payload(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            run_pipeline([{'value': value}], [])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
