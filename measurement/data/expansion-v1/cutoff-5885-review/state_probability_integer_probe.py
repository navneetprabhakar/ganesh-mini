import unittest
from solution import DiscreteStateModel


class ProbabilityProbe(unittest.TestCase):
    def test_out_of_range_integer_probability_raises_value_error(self):
        with self.assertRaises(ValueError):
            DiscreteStateModel(['s'], ['x'], [[10 ** 400]], [[1]], [1])


if __name__ == '__main__':
    unittest.main()
