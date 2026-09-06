import unittest
from solution import stamp_matrix


class SharedRowTests(unittest.TestCase):
    def test_overlay_changes_only_target_row(self):
        row = [0]
        self.assertEqual(stamp_matrix([row, row], [[1]], 0, 0), [[1], [0]])


if __name__ == "__main__":
    unittest.main()
