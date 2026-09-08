import unittest
from solution import logical_right_shift


class TinyResultTests(unittest.TestCase):
    def test_controls(self):
        self.assertEqual(logical_right_shift(1, 0, 32), 1)
        self.assertEqual(logical_right_shift(-1, 10**100, 10**100), 0)

    def test_tiny_result_does_not_require_width_sized_mask(self):
        self.assertEqual(logical_right_shift(1, 0, 10**100), 1)


if __name__ == '__main__':
    unittest.main()
