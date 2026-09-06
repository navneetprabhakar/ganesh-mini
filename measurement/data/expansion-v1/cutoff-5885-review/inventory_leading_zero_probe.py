import unittest
from solution import parse_inventory

class Probe(unittest.TestCase):
    def test_leading_zero_price(self):
        source = 'sku,price_cents,zone,stock\nx,' + '0'*5000 + '1,z,2\n'
        self.assertEqual(parse_inventory(source), [dict(sku='x', price_cents=1, zone='z', stock=2)])

if __name__ == '__main__':
    unittest.main()
