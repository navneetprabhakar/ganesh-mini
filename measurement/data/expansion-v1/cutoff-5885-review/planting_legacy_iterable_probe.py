import unittest
from solution import PlantingLedger


class Records:
    def __getitem__(self, index):
        if index == 0:
            return {"field": "f", "crop": "c", "planting_date": "date"}
        raise IndexError


class PlantingIterableTests(unittest.TestCase):
    def test_sequence_protocol_is_iterable(self):
        self.assertEqual(PlantingLedger().import_records(Records())[0]["id"], 1)


if __name__ == "__main__":
    unittest.main()
