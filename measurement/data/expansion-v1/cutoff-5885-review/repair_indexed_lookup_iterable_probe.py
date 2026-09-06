import unittest
from solution import indexed_lookup


class Keys:
    def __getitem__(self, index):
        if index == 0:
            return 'x'
        raise IndexError


class Probe(unittest.TestCase):
    def test_getitem_iterable(self):
        self.assertEqual(indexed_lookup({'x': 1}, Keys()), [1])


if __name__ == '__main__':
    unittest.main()
