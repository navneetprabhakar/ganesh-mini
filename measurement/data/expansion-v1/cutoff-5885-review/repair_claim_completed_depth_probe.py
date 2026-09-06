import unittest
from solution import claim_completed


class Probe(unittest.TestCase):
    def test_finite_extra_field(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            claim_completed([{'id': 'x', 'completed': True, 'claimed': False, 'extra': value}])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
