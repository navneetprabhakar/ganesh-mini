import unittest
from solution import self_power_suffix


class WideSuffixTests(unittest.TestCase):
    def test_supported_width_above_integer_conversion_limit(self):
        result = self_power_suffix(1500, 5000)
        self.assertEqual(len(result), 5000)
        self.assertTrue(result.isascii() and result.isdigit())
        self.assertEqual(result[-10:], self_power_suffix(1500, 10))


if __name__ == "__main__":
    unittest.main()
