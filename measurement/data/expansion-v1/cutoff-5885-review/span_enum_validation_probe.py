import unittest
from solution import summarize_spans

class SpanEnumProbe(unittest.TestCase):
    def test_unhashable_kind_and_level_raise_value_error(self):
        for field in ['kind', 'level']:
            event = {'name': 'x', 'kind': 'begin', 'tick': 0, 'level': 'info'}
            event[field] = []
            with self.subTest(field=field), self.assertRaises(ValueError):
                summarize_spans([event])

if __name__ == '__main__':
    unittest.main()
