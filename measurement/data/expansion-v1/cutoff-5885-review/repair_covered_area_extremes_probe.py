import unittest
from solution import compute_covered_area


class Probe(unittest.TestCase):
    def test_zero_coverage_finite_dimensions(self):
        self.assertEqual(compute_covered_area(1e308, 1e308, 0), 0.0)

    def test_finite_huge_integer_zero_coverage(self):
        self.assertEqual(compute_covered_area(10**400, 1, 0), 0.0)


if __name__ == '__main__':
    unittest.main()
