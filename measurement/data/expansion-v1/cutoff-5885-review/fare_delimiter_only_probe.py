import unittest

from solution import parse_fare_table


class NonblankRowTests(unittest.TestCase):
    def test_delimiter_only_row_is_not_blank(self):
        for text in (";", " ; ", ";;"):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_fare_table(text)


if __name__ == "__main__":
    unittest.main()
