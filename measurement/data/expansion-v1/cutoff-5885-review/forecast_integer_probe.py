import unittest
from solution import prepare_forecast


class ForecastIntegerTests(unittest.TestCase):
    def test_finite_integer_query_cancels_exactly(self):
        self.assertEqual(prepare_forecast([], None, 10**400, 0, 7), {"records": [], "forecast": 7.0})


if __name__ == "__main__":
    unittest.main()
