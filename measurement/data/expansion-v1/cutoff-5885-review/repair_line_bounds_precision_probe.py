import unittest
from solution import line_bounds

class Probe(unittest.TestCase):
    def test_reversed_integer_bounds_not_rounded_together(self):
        word = {'line': 0, 'text': 'x', 'x0': 2**53+1, 'y0': 0, 'x1': 2**53, 'y1': 0}
        with self.assertRaises(ValueError):
            line_bounds([word])

    def test_finite_integer_coordinate(self):
        word = {'line': 0, 'text': 'x', 'x0': 0, 'y0': 0, 'x1': 10**400, 'y1': 0}
        self.assertEqual(line_bounds([word])[0]['x1'], 10**400)

if __name__ == '__main__':
    unittest.main()
