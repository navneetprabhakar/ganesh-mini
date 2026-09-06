import unittest
from types import MappingProxyType
from solution import migrate_schema


class ReviewProbe(unittest.TestCase):
    def test_readonly_mapping(self):
        source = MappingProxyType({'fields': {'blob': {'kind': 'old'}}})
        result = migrate_schema(source)
        self.assertEqual(result['fields']['blob']['kind'], 'upload')
        self.assertEqual(source['fields']['blob']['kind'], 'old')


if __name__ == '__main__':
    unittest.main()
