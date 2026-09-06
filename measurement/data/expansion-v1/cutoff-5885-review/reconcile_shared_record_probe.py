import unittest
from solution import reconcile_records

class Probe(unittest.TestCase):
    def test_independent_digest_replacements(self):
        shared = {'digest': 'a'*64}
        expected = {'first': {'digest': 'b'*64}, 'second': {'digest': 'c'*64}}
        result = reconcile_records(expected, {'first': shared, 'second': shared})
        self.assertEqual(result['records']['first']['digest'], 'b'*64)
        self.assertEqual(result['records']['second']['digest'], 'c'*64)

if __name__ == '__main__':
    unittest.main()
