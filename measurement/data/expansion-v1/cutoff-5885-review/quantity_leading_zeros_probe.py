import unittest
from solution import aggregate_label

class QuantityZerosProbe(unittest.TestCase):
    def test_in_range_quantity_with_many_leading_zeroes(self):
        self.assertEqual(aggregate_label('x,c,' + '0' * 5000 + '1', 'x'), 1)

if __name__ == '__main__':
    unittest.main()
