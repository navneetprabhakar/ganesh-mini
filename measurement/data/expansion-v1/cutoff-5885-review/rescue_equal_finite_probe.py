import unittest
from solution import plan_rescue


class RescueFiniteTests(unittest.TestCase):
    def test_equal_finite_halves_have_zero_turn(self):
        self.assertEqual(plan_rescue(True, [[1e308] * 4])[0], ("TURN", 0.0))


if __name__ == "__main__":
    unittest.main()
