import unittest
from solution import Observation, Expectation


class AuditorNaNDurationTests(unittest.TestCase):
    def test_nan_is_not_nonnegative(self):
        with self.assertRaises(ValueError):
            Observation((), float('nan'))
        with self.assertRaises(ValueError):
            Expectation((), 0, float('nan'))


if __name__ == '__main__':
    unittest.main()
