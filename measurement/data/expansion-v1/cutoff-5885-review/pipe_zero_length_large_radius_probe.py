import unittest
from solution import pipe_metrics

class Probe(unittest.TestCase):
    def test_zero_length_finite_radius(self):
        self.assertEqual(pipe_metrics(1e200, 0, 0), (0.0, 0.0))

if __name__ == '__main__':
    unittest.main()
