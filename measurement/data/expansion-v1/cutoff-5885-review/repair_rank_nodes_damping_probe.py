import unittest
from solution import rank_nodes


class Probe(unittest.TestCase):
    def test_out_of_range_integer(self):
        with self.assertRaises(ValueError):
            rank_nodes([], damping=10**400)


if __name__ == '__main__':
    unittest.main()
