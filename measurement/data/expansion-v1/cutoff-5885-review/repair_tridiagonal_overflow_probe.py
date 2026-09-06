import unittest
from solution import solve_tridiagonal


class ReviewProbe(unittest.TestCase):
    def test_representable_solution_with_large_elimination_intermediate(self):
        actual = solve_tridiagonal([1e308], [1.0, 1e308], [2.0], [3.0, 1e308])
        self.assertEqual(actual, [-1.0, 2.0])


if __name__ == '__main__':
    unittest.main()
