import unittest
from solution import compressed_estimate


class Probe(unittest.TestCase):
    def test_level_zero_finite_large_integer_radix(self):
        error = None
        try:
            result = compressed_estimate(0, 10**400)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, 0.0)


if __name__ == '__main__':
    unittest.main()
