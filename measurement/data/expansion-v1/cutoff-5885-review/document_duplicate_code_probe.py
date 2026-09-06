import unittest
from solution import DocumentIndex


class DocumentDuplicateCodeTests(unittest.TestCase):
    def test_identical_title_does_not_relax_unique_codes(self):
        index = DocumentIndex()
        index.add('Title', 'CODE', {'version': 1})
        with self.assertRaises((ValueError, TypeError)):
            index.add('Title', 'CODE', {'version': 2})


if __name__ == '__main__':
    unittest.main()
