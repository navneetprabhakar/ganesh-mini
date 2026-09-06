import unittest
from solution import AllocationLedger


class AllocationLargeStartTests(unittest.TestCase):
    def test_positive_integer_start(self):
        ledger = AllocationLedger(10 ** 4300)
        self.assertEqual(ledger.reserve('desk', 'member')['id'], 'A1' + '0' * 4300)


if __name__ == '__main__':
    unittest.main()
