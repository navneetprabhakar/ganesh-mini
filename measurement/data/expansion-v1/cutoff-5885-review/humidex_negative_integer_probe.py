import math
import unittest
from solution import humidex_celsius


class HumidexNegativeIntegerTests(unittest.TestCase):
    def test_finite_integer_below_valid_temperature(self):
        self.assertTrue(math.isnan(humidex_celsius(-(10 ** 400), 0)))


if __name__ == '__main__':
    unittest.main()
