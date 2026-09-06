import unittest
from solution import extract_epoch_series


class EpochIntegerTests(unittest.TestCase):
    def test_nonnegative_integer_with_leading_zero(self):
        result = extract_epoch_series("epoch=01;validation_score=1;validation_error=2;learning_score=3;learning_error=4")
        self.assertEqual([r["epochs"] for r in result], [[1]])


if __name__ == "__main__":
    unittest.main()
