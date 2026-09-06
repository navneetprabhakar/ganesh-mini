import unittest
from solution import render_breakdowns

class Probe(unittest.TestCase):
    def test_large_integer_render(self):
        value = 10**4300
        digits = '1' + '0'*4300
        self.assertEqual(render_breakdowns({value: (value,)}), digits + ': ' + digits)

if __name__ == '__main__':
    unittest.main()
