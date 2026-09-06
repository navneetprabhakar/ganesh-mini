import unittest

from solution import expand_layouts


class PositiveScaleTests(unittest.TestCase):
    def test_nan_is_not_positive(self):
        with self.assertRaises(ValueError):
            expand_layouts({"x": {"scale": float("nan"), "box": [1, 1, 1], "points": []}}, {})


if __name__ == "__main__":
    unittest.main()
