import unittest

from solution import parse_offset


class DecimalWidthTests(unittest.TestCase):
    def test_three_decimal_components_without_unspecified_width(self):
        self.assertEqual(parse_offset("1:2:3"), 3723)


if __name__ == "__main__":
    unittest.main()
