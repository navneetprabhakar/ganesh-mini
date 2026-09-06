import unittest
from solution import scale_axes

class Probe(unittest.TestCase):
    def test_finite_opposite_extremes(self):
        self.assertEqual(scale_axes([[-1e308], [0.0], [1e308]]), [[0.0], [0.5], [1.0]])

    def test_finite_huge_integer_constant(self):
        self.assertEqual(scale_axes([[10**400]]), [[0.0]])

if __name__ == '__main__':
    unittest.main()
