import unittest
from solution import stream_totals


class Probe(unittest.TestCase):
    def test_finite_large_integer(self):
        error = None
        value = 10**400
        try:
            result = stream_totals(iter([('x', value), ('x', -value)]))
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, [('x', 0)])


if __name__ == '__main__':
    unittest.main()
