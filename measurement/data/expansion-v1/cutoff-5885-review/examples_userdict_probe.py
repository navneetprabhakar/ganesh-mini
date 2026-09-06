import unittest
from collections import UserDict
from solution import prepare_examples


class MappingRecordTests(unittest.TestCase):
    def test_standard_mapping_record(self):
        result = prepare_examples([UserDict(pixels=[[0]], sector="s", distance="d")], 2)
        self.assertEqual(result["sector"]["train"], [{"pixels": [[0]], "label": "s"}])


if __name__ == "__main__":
    unittest.main()
