import unittest
from solution import compute_thumbnail_box


class ThumbnailIdentityTests(unittest.TestCase):
    def test_already_fitting_integer_dimensions_remain_exact(self):
        n = 2**53 + 1
        self.assertEqual(compute_thumbnail_box(n, 1, n, 1), (n, 1, 1.0))


if __name__ == "__main__":
    unittest.main()
