import unittest

from solution import upgrade_rows


class DistinctRowIdTests(unittest.TestCase):
    def test_repeated_input_record_receives_distinct_position_ids(self):
        shared = {"name": "same"}
        result = upgrade_rows([shared, shared])
        self.assertEqual([row["unique_id"] for row in result], ["I" + "0" * 31, "I" + "0" * 30 + "1"])
        self.assertEqual(shared, {"name": "same"})


if __name__ == "__main__":
    unittest.main()
