import unittest
from solution import coerce_optional_int


class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(coerce_optional_int('0' * 5000 + '1'), 1)


if __name__ == '__main__':
    unittest.main()
