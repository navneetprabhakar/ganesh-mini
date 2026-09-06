import unittest
from solution import version_at_least


class Probe(unittest.TestCase):
    def test_long_decimal_component(self):
        self.assertTrue(version_at_least('1' + '0'*4999, '1'))


if __name__ == '__main__':
    unittest.main()
