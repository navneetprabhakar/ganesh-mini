import unittest
from solution import dispatch_fifo

class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(dispatch_fifo([], 10**100), [])

if __name__ == '__main__':
    unittest.main()
