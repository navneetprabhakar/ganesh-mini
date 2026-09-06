import unittest
from solution import evolve

class Probe(unittest.TestCase):
    def test_each_direction_counts_even_when_it_maps_to_self(self):
        # In a 1x2 board the live cell sees itself twice vertically.
        # Its other six offsets land on the dead cell, so it survives.
        self.assertEqual(evolve([[1, 0]], 1, True), [[1, 0]])

if __name__ == '__main__':
    unittest.main()
