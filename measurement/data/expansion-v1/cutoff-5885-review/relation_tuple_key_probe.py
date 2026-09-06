import unittest
from solution import RelationBuckets


class TupleKeyTests(unittest.TestCase):
    def test_tuple_scalar_does_not_read_list_key_bucket(self):
        buckets = RelationBuckets()
        buckets.add(["a", "b"], 1)
        self.assertEqual(buckets.get(("a", "b")), frozenset())


if __name__ == "__main__":
    unittest.main()
