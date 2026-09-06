import unittest
from types import MappingProxyType
from solution import select_route


class ReviewProbe(unittest.TestCase):
    def test_standard_readonly_mapping_record(self):
        record = MappingProxyType({'address': '8.8.8.8', 'priority': 0})
        result = select_route([record])
        self.assertIs(type(result), dict)
        self.assertEqual(result, dict(record))


if __name__ == '__main__':
    unittest.main()
