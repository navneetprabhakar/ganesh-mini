import unittest
from solution import chunk_records

class Probe(unittest.TestCase):
    def test_contract(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            chunk_records([value], 1)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
