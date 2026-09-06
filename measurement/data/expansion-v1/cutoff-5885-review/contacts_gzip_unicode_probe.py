import gzip
import json
import unittest
from solution import decode_contacts


class ContactsGzipUnicodeTests(unittest.TestCase):
    def test_malformed_deflate_counts_one_error(self):
        bad = bytes.fromhex('1f8b08000000000000ff07') + b'\x00' * 8
        self.assertEqual(decode_contacts([bad]), {'anchors': [], 'errors': 1})

    def test_unicode_separator_inside_json_string_is_not_ndjson_delimiter(self):
        raw = json.dumps({'label': 'a\u2028b', 'target': '/x'}, ensure_ascii=False)
        packed = gzip.compress(raw.encode('utf-8'), mtime=0)
        self.assertEqual(decode_contacts([packed]), {'anchors': ['<a href="/x">a\u2028b</a>'], 'errors': 0})


if __name__ == '__main__':
    unittest.main()
