import unittest

from solution import parse_telemetry


class EarlyYearTests(unittest.TestCase):
    def test_four_digit_early_year_is_valid(self):
        self.assertEqual(
            parse_telemetry(["dev,0001-01-01,1000,0,1,1000"]),
            [("dev", 1, 1, 1, 1.0, 0.0, 1, 1.0)],
        )


if __name__ == "__main__":
    unittest.main()
