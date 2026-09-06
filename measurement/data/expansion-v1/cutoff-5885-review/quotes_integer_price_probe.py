import unittest
from solution import prepare_quotes


class QuoteIntegerPriceTests(unittest.TestCase):
    def test_large_equal_finite_prices_have_zero_changes_and_ranges(self):
        n = 10**400
        rows = [{"day": "2024-01-01", "open": n, "close": n}, {"day": "2024-01-02", "open": n, "close": n}]
        result = prepare_quotes(rows, "2024-01-01")
        self.assertEqual(result["train"][0]["open"], 0.0)
        self.assertEqual(result["train"][0]["fractional_change"], 0.0)


if __name__ == "__main__":
    unittest.main()
