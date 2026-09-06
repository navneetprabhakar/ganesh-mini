import unittest
from solution import render_observation


class ObservationIntegerPrecisionTests(unittest.TestCase):
    def test_exact_integer_temperature_to_one_decimal(self):
        value = 2 ** 53 + 1
        text = render_observation('P', dict(temperature_c=value, summary='S', wind_mps=0))
        self.assertIn('Temperature: 9007199254740993.0 C', text)


if __name__ == '__main__':
    unittest.main()
