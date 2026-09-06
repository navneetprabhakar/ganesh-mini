import unittest
from solution import compile_record

class KindValidationProbe(unittest.TestCase):
    def test_unhashable_kind_is_malformed_specification(self):
        with self.assertRaises(ValueError):
            compile_record([{'name': 'x', 'kind': []}], {})

if __name__ == '__main__':
    unittest.main()
