import unittest
from solution import notes_to_markup

class Probe(unittest.TestCase):
    def test_single_empty_line_is_not_a_paragraph(self):
        self.assertEqual(notes_to_markup('\n'), '')

if __name__ == '__main__':
    unittest.main()
