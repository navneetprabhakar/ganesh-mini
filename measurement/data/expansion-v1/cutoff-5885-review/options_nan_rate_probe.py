import unittest
from solution import parse_training_options


class PositiveRateTests(unittest.TestCase):
    def test_nan_is_not_positive(self):
        with self.assertRaises(ValueError):
            parse_training_options(["--learning-rate", "nan"])


if __name__ == "__main__":
    unittest.main()
