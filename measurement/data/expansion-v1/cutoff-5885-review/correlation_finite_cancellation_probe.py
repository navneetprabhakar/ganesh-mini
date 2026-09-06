import unittest
from solution import classify_grids


class CorrelationFiniteCancellationTests(unittest.TestCase):
    def test_representable_correlation_after_cancellation(self):
        result = classify_grids([[[1e308, 1e308, 1]]], [[[2, -2, 1]]], [0])
        self.assertEqual(result, {'indices': [0], 'scores': [[1.0]]})


if __name__ == '__main__':
    unittest.main()
