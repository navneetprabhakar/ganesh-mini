import unittest
from solution import expand_grid


class Probe(unittest.TestCase):
    def test_finite_payload(self):
        value = {}
        for _ in range(600):
            value = {'x': value}
        error = None
        try:
            expand_grid([value], [0], [[0]])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
