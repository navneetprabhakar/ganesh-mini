import unittest
from solution import read_ruled_grid


class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(read_ruled_grid([0, 10**400], [0, 1], []), [['']])


if __name__ == '__main__':
    unittest.main()
