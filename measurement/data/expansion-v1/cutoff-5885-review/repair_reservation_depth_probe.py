import unittest
from solution import ReservationBook

class Probe(unittest.TestCase):
    def test_contract(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            ReservationBook({'x': value})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
