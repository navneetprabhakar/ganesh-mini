import unittest
from solution import continuous_headings


class Probe(unittest.TestCase):
    def test_declared_interval(self):
        # No integer number of full turns can make 100 fall in [-30, 30].
        # This exposes a prompt feasibility gap, not an invented error policy.
        result = continuous_headings([0, 100], 30)
        self.assertLessEqual(abs(result[1] - result[0]), 30)


if __name__ == '__main__':
    unittest.main()
