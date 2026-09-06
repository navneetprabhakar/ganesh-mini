import unittest
from solution import parse_measurements

class Probe(unittest.TestCase):
    def test_cr_record_separator(self):
        self.assertEqual(parse_measurements('a,b\rc,d\r'), [('a', 'b'), ('c', 'd')])

    def test_valid_large_field(self):
        text = 'x' * 140000
        self.assertEqual(parse_measurements(text), [(text,)])

if __name__ == '__main__':
    unittest.main()
