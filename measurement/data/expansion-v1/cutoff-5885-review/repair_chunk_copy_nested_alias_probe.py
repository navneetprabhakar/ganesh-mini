import unittest
from solution import chunk_copy


class Probe(unittest.TestCase):
    def test_nested_mutation_isolated(self):
        value = []
        values = [value, value]
        result = chunk_copy(values, 1)
        result[0][0].append(1)
        self.assertEqual(result[1], [[]])
        self.assertEqual(values, [[], []])


if __name__ == '__main__':
    unittest.main()
