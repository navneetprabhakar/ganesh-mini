import unittest
from collections import UserDict
from solution import clean_catalog


class CatalogMappingTests(unittest.TestCase):
    def test_scoped_suffixes_accepts_mapping(self):
        entry = {"path": ("src", "a.tmp"), "kind": "file", "metadata": {}}
        self.assertEqual(clean_catalog([entry], (), (), UserDict({("src",): (".tmp",)}), False), {"removed": [entry], "remaining": []})


if __name__ == "__main__":
    unittest.main()
