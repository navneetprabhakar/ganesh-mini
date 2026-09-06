import unittest
from solution import mix_drive


class DriveCancellationTests(unittest.TestCase):
    def test_balanced_finite_signals_have_zero_mean(self):
        commands = mix_drive({"samples": [1e308, 1e308, -1e308, -1e308]}, {"samples": [0]})
        self.assertEqual([c.velocity for c in commands], [0.0] * 4)


if __name__ == "__main__":
    unittest.main()
