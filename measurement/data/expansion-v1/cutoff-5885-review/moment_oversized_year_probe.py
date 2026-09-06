import unittest
from solution import build_moment_context


class InvalidYearTests(unittest.TestCase):
    def test_out_of_range_integer_year_raises_value_error(self):
        with self.assertRaises(ValueError):
            build_moment_context((10 ** 100, 1, 1, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
