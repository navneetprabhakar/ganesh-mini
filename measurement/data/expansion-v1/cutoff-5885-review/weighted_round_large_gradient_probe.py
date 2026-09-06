import unittest
from solution import run_weighted_round

class Probe(unittest.TestCase):
    def test_finite_gradient_clips_to_one(self):
        self.assertEqual(run_weighted_round([0], [[[1e200]]], 1, 1, 1), [-1.0])

if __name__ == '__main__':
    unittest.main()
