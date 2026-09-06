import unittest
from solution import progressive_bands


class Probe(unittest.TestCase):
    def test_finite_large_integer(self):
        error = None
        value = 10**400
        try:
            result = progressive_bands([[value], [-value]])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, [[value], [0]])


if __name__ == '__main__':
    unittest.main()
