import unittest
from solution import dequeue_snapshot


class Probe(unittest.TestCase):
    def test_finite_payload(self):
        value = {}
        for _ in range(600):
            value = {'x': value}
        error = None
        try:
            dequeue_snapshot([value])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
