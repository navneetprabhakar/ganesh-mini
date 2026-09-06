import unittest
from collections import UserList
from solution import clear_region

class Probe(unittest.TestCase):
    def test_standard_sequence(self):
        self.assertEqual(clear_region(UserList(['x']), 0, 0, 0, 0), [' '])

if __name__ == '__main__':
    unittest.main()
