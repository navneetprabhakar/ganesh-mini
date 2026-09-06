import unittest
from solution import snapshot_layers


class Probe(unittest.TestCase):
    def test_finite_payload(self):
        value = {}
        for _ in range(600):
            value = {'x': value}
        error = None
        try:
            snapshot_layers([{'name': 'x', 'settings': value}])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
