import unittest
from solution import parse_tag_table


class ReviewProbe(unittest.TestCase):
    def test_valid_identifier_with_leading_zeroes(self):
        error = None
        try:
            rows = parse_tag_table('0' * 4300 + '1 tag')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(rows, [{'id': 1, 'tags': ['tag']}])


if __name__ == '__main__':
    unittest.main()
