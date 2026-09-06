import unittest
from solution import select_context


class Probe(unittest.TestCase):
    def test_zero_limit_with_finite_valid_metadata(self):
        value = []
        for _ in range(600):
            value = [value]
        records = [{'id': 'one', 'text': 'match', 'metadata': {'value': value}}]
        error = None
        try:
            result = select_context(records, 'match', 0)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
