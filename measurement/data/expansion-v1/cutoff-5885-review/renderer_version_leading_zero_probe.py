import unittest
from solution import make_renderer

class Probe(unittest.TestCase):
    def test_valid_leading_zero_version(self):
        self.assertEqual(make_renderer('p', '0'*5000 + '2.5')(7), '[p] 7')

if __name__ == '__main__':
    unittest.main()
