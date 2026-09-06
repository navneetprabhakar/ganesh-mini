import math
import unittest

from solution import solve_chain


class ConvergenceTests(unittest.TestCase):
    def test_finite_chain_does_not_report_nan_as_converged(self):
        try:
            result = solve_chain([1e308, 1e308], [0], 2, 2)
        except ValueError:
            # Explicit inability to converge is an allowed failure outcome.
            return
        self.assertTrue(all(math.isfinite(value) for value in result), repr(result))
        self.assertAlmostEqual(result[1], 2.0)


if __name__ == "__main__":
    unittest.main()
