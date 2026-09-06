import unittest
from solution import is_schema_supported


class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertTrue(is_schema_supported('0' * 5000 + '2.7.3'))


if __name__ == '__main__':
    unittest.main()
