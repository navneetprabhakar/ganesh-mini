import unittest
from solution import render_label

class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(render_label('x', {'n': 10**4999}), 'x [n=1' + '0'*4999 + ']')

if __name__ == '__main__':
    unittest.main()
