import unittest
from solution import NearestLabelPlanner


class PlannerUnselectedSensorTests(unittest.TestCase):
    def test_rows_must_contain_real_sensor_values(self):
        planner = NearestLabelPlanner([0], 1, 2, 2)
        with self.assertRaises(TypeError):
            planner.fit([[[0, 'invalid'], [1, 2]]], [[0, 1]])


if __name__ == '__main__':
    unittest.main()
