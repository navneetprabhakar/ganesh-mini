import unittest
from solution import turning_points


class Probe(unittest.TestCase):
    def test_small_finite_sign_change(self):
        self.assertEqual(turning_points([0.0, 1e-200, 0.0], 0), [1])


if __name__ == '__main__':
    unittest.main()
