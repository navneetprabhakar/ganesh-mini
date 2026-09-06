import unittest
from solution import summarize_activity


class ActivityYearTests(unittest.TestCase):
    def test_four_digit_early_year_is_valid(self):
        row = {"asset": "a", "location": "L", "timestamp": "0001-01-01 00:00"}
        self.assertEqual(summarize_activity([row], []), ("Asset a checked in at L on 0001-01-01 00:00", None))


if __name__ == "__main__":
    unittest.main()
