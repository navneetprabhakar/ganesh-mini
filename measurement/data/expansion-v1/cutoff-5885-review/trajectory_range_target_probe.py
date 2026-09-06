import unittest
from solution import analyze_trajectory


class TrajectorySequenceTests(unittest.TestCase):
    def test_range_target_pair(self):
        self.assertEqual(analyze_trajectory([(0, 1)], range(2), 0)["first_reached"], 0)


if __name__ == "__main__":
    unittest.main()
