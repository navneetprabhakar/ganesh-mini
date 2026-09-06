import unittest
from solution import expand_ranges

class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(expand_ranges('1'+'0'*4999), [10**4999])

if __name__ == '__main__':
    unittest.main()
