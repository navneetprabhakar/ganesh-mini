import unittest
from solution import decode_table


class ReviewProbe(unittest.TestCase):
    def test_carriage_return_record_separator(self):
        self.assertEqual(decode_table('a,b\r1,2'), [['a', 'b'], ['1', '2']])

    def test_valid_field_beyond_default_csv_limit(self):
        field = 'a' * 131073
        error = None
        try:
            rows = decode_table(field)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(rows, [[field]])


if __name__ == '__main__':
    unittest.main()
