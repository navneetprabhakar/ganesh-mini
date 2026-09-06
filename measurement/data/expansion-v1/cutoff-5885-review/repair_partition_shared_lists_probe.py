import unittest
from solution import append_partitioned


class ReviewProbe(unittest.TestCase):
    def test_append_affects_only_named_partition(self):
        records = [1]
        storage = {'a': records, 'b': records}
        result = append_partitioned(storage, {'a': [2]})
        self.assertEqual(result, {'a': [1, 2], 'b': [1]})
        self.assertEqual(records, [1])


if __name__ == '__main__':
    unittest.main()
