import unittest
from solution import numbered_message


class Probe(unittest.TestCase):
    def test_any_integer_start(self):
        self.assertEqual(numbered_message('x', 1, 10**4999), ['1' + '0'*4999 + ': x'])


if __name__ == '__main__':
    unittest.main()
