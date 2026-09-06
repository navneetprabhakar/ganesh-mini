import unittest
from solution import format_stride

class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(format_stride(10**4999 + 1, 10**4999), '0, 1' + '0'*4999)

if __name__ == '__main__':
    unittest.main()
