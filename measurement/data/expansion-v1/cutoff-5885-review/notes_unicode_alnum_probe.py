import unittest
from solution import prepare_notes


class UnicodeNoteTests(unittest.TestCase):
    def test_unicode_letters_and_digits_are_alphanumeric(self):
        rows = [{"group": "g", "channel": "c", "priority": "p", "text": "CAFÉ १२"}]
        self.assertEqual(prepare_notes(rows)[0]["tokens"], ["café", "१२"])


if __name__ == "__main__":
    unittest.main()
