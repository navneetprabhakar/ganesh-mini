import unittest
from solution import select_records


class LegacyIterable:
    def __getitem__(self, index):
        if index == 0:
            return {'rank': 1}
        raise IndexError


class Probe(unittest.TestCase):
    def test_getitem_iterable(self):
        self.assertEqual(select_records(LegacyIterable(), False), [{'rank': 1}])

    def test_finite_payload(self):
        value = {}
        for _ in range(600):
            value = {'x': value}
        error = None
        try:
            select_records([{'rank': 1, 'extra': value}], False)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
