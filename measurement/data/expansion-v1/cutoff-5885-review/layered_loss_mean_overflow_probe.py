import math
import unittest

from solution import LayeredTextPlan


class FiniteLossTests(unittest.TestCase):
    def test_representable_mean_squared_error(self):
        plan = LayeredTextPlan(2, "pre", "forward")
        result = plan.loss([1e154, 1e154], [0, 0])
        self.assertTrue(math.isfinite(result), repr(result))
        self.assertAlmostEqual(result / 1e308, 1.0)


if __name__ == "__main__":
    unittest.main()
