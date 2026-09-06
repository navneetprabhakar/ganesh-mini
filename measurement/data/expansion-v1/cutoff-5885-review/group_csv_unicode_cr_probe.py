import csv
import io
import unittest
from solution import render_group_csv


class GroupCsvTests(unittest.TestCase):
    def test_lowercase_precedes_ascii_replacement(self):
        self.assertEqual(list(render_group_csv([{"name": "\u212a", "enabled": True, "rows": []}])), ["k.csv"])

    def test_carriage_return_field_roundtrips(self):
        rows = [["a\rb", "1", "2", "z"]]
        text = render_group_csv([{"name": "g", "enabled": True, "rows": rows}])["g.csv"]
        self.assertEqual(list(csv.reader(io.StringIO(text, newline="")))[1:], rows)


if __name__ == "__main__":
    unittest.main()
