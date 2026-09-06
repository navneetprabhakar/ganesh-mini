import unittest
from solution import assemble_bundle


class Probe(unittest.TestCase):
    def test_finite_bundle(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            assemble_bundle({'value': value})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
