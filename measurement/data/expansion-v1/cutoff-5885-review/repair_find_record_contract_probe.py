import unittest
from solution import find_record

class Probe(unittest.TestCase):
    def test_malformed_record_after_match(self):
        with self.assertRaises((TypeError, ValueError)):
            find_record([{'name': 'x'}, {}], 'x')

    def test_finite_nested_match(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            find_record([{'name': 'x', 'value': value}], 'x')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
