import unittest
from solution import reads_same


class PalindromeRecursionTests(unittest.TestCase):
    def test_moderate_symmetric_string(self):
        self.assertTrue(reads_same('a' * 3000))


if __name__ == '__main__':
    unittest.main()
