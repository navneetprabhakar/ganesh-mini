import unittest

from solution import select_values


class DecimalIndexTests(unittest.TestCase):
    def test_long_zero_index_selects_first_value(self):
        self.assertEqual(select_values(["first"], "0" * 5000), ["first"])


if __name__ == "__main__":
    unittest.main()
