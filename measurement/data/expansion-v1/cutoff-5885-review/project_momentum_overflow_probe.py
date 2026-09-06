import unittest
from solution import project_state


class MomentumTests(unittest.TestCase):
    def test_finite_representable_adjusted_velocity(self):
        bodies = [
            {"name": "a", "mass": 1e308, "position": [0, 0, 0], "velocity": [0, 0, 0]},
            {"name": "b", "mass": 1e308, "position": [0, 0, 0], "velocity": [2, 0, 0]},
        ]
        self.assertEqual(project_state(bodies)[0]["velocity"][0], -2.0)


if __name__ == "__main__":
    unittest.main()
