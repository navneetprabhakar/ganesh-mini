import unittest
from solution import build_histogram_grid


class HistogramSubnormalTests(unittest.TestCase):
    def test_finite_distinct_endpoints(self):
        plot = build_histogram_grid({'c': ['p']}, {'p': [0.0, 5e-324]}, bins=2)[0]['plots'][0]
        self.assertEqual(plot['counts'], [1, 1])


if __name__ == '__main__':
    unittest.main()
