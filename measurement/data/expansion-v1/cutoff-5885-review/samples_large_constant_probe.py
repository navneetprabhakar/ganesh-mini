import unittest
from solution import summarize_samples

class Probe(unittest.TestCase):
    def test_constant_large_sample(self):
        result = summarize_samples([[1e308, 1e308]])[0]
        self.assertEqual(result['mean'], 1e308)
        self.assertEqual(result['variance'], 0)
        self.assertEqual(result['z_scores'], [0.0, 0.0])

if __name__ == '__main__':
    unittest.main()
