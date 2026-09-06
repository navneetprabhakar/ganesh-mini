import unittest

from solution import transform_detection


class BoxOrderingTests(unittest.TestCase):
    def test_nan_does_not_satisfy_endpoint_order(self):
        with self.assertRaises(ValueError):
            transform_detection({"image": [[1]], "annotations": [{"bbox": [float("nan"), 0, 1, 1]}]}, 1, 1)


if __name__ == "__main__":
    unittest.main()
