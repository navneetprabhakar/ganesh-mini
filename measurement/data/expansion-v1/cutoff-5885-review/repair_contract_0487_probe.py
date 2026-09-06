import unittest
from solution import attach_entries


class Probe(unittest.TestCase):
    def test_contract(self):
        amount = 2**53 + 1
        result = attach_entries([{'id': 1, 'name': 'x'}], [{'account_id': 1, 'amount': amount}])
        self.assertEqual(result[0]['entries'][0]['amount'], amount)


if __name__ == '__main__':
    unittest.main()
