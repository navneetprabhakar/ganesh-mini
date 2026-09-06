import unittest

from solution import route_length


class IntegerCoordinatesTests(unittest.TestCase):
    def test_unit_segment_at_large_integer_origin(self):
        self.assertEqual(route_length([(2 ** 53, 0), (2 ** 53 + 1, 0)]), 1.0)


if __name__ == "__main__":
    unittest.main()
