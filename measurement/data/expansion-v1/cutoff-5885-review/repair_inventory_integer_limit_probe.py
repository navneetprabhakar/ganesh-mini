import unittest
from solution import decode_inventory

class Probe(unittest.TestCase):
    def test_valid_large_quantity(self):
        xml = '<inventory><item code="x" quantity="1' + '0'*4999 + '">x</item></inventory>'
        self.assertEqual(decode_inventory(xml)[0]['quantity'], 10**4999)

if __name__ == '__main__':
    unittest.main()
