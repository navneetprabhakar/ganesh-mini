import unittest
from solution import grade_responses

class Probe(unittest.TestCase):
    def test_finite_payload(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            grade_responses([{'prompt': 'x', 'expected': None}], [value])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
