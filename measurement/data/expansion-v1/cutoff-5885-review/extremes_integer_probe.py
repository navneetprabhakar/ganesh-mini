import unittest
from solution import locate_signal_extremes

class ExtremeIntegerProbe(unittest.TestCase):
    def test_finite_large_integers_keep_exact_values(self):
        value = 10 ** 400
        self.assertEqual(locate_signal_extremes([value, -value]), {
            'highest': value, 'highest_index': 0, 'lowest': -value, 'lowest_index': 1})

if __name__ == '__main__':
    unittest.main()
