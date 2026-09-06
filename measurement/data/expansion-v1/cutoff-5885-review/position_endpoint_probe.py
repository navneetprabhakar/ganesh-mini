import unittest
from solution import position_to_value


class PositionEndpointTests(unittest.TestCase):
    def test_exact_integer_endpoint_is_preserved(self):
        maximum = 2**53 + 1
        self.assertEqual(position_to_value(1, 1, 0, maximum), maximum)


if __name__ == "__main__":
    unittest.main()
