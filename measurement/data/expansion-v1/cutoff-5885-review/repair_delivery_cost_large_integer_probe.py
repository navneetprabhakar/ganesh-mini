import unittest
from solution import extract_delivery_cost

class Probe(unittest.TestCase):
    def test_finite_integer_cost(self):
        self.assertEqual(extract_delivery_cost({'ok': True, 'result': {'cost': 10**400}}), 10**400)

if __name__ == '__main__':
    unittest.main()
