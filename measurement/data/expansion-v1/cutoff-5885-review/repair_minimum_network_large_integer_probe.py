import unittest
from solution import minimum_network

class Probe(unittest.TestCase):
    def test_finite_integer_cost(self):
        self.assertEqual(minimum_network(2, [(0, 1, 10**400)])[2], 10**400)

if __name__ == '__main__':
    unittest.main()
