import unittest

from solution import render_parcel_manifest


class ManifestLineTests(unittest.TestCase):
    def test_text_newline_cannot_break_fixed_width_lines(self):
        result = render_parcel_manifest([
            {"tracking": "A\nB", "zone": "z", "weight": 1, "note": "n"}
        ], 60)
        self.assertTrue(all(len(line) == 60 for line in result.split("\n")), repr(result))


if __name__ == "__main__":
    unittest.main()
