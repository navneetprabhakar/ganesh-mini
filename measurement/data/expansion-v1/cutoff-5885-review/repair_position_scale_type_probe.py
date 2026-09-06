import unittest
from solution import select_position


class ReviewProbe(unittest.TestCase):
    def test_invalid_unhashable_scale(self):
        with self.assertRaises(ValueError):
            select_position([1, 2], 0, [])


if __name__ == '__main__':
    unittest.main()
