import unittest
from solution import largest_value_window


class LargeIntegerTests(unittest.TestCase):
    def test_finite_integers_need_not_fit_float(self):
        value = 10 ** 400
        self.assertEqual(largest_value_window([value, value + 1], 1), 2)


if __name__ == "__main__":
    unittest.main()
