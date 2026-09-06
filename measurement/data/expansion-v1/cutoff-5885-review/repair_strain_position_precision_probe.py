import unittest
from solution import strain_energy


class Probe(unittest.TestCase):
    def test_adjacent_integer_positions(self):
        # Exact interval is one, constant squared strain is one, modulus is two.
        error = None
        try:
            result = strain_energy([(2**53, 1), (2**53 + 1, 1)], 2)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, 1.0)


if __name__ == '__main__':
    unittest.main()
