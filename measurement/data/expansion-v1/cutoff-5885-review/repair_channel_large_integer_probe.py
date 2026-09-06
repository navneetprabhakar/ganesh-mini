import unittest
from solution import select_channel

class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(select_channel([[[10**400]]], 0), [[10**400]])

if __name__ == '__main__':
    unittest.main()
