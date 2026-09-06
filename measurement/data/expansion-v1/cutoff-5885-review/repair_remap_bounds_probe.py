import unittest
from solution import remap_points

class Probe(unittest.TestCase):
    def test_fraction_beyond_last_pixel(self):
        with self.assertRaises(ValueError):
            remap_points([(2.5, 0)], (3, 3), (3, 3))

if __name__ == '__main__':
    unittest.main()
