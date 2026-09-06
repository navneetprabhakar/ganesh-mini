import unittest
from solution import decode_grid

class Probe(unittest.TestCase):
    def test_cr_rows(self):
        self.assertEqual(decode_grid('a;b\rc;d'), [('a', 'b'), ('c', 'd')])

if __name__ == '__main__':
    unittest.main()
