import unittest

from solution import apply_membership_commands


class TagPreservationTests(unittest.TestCase):
    def test_only_names_are_specified_to_be_stripped(self):
        result = apply_membership_commands([
            {"op": "add", "name": " Ada ", "tags": [" red ", "red"]}
        ])
        self.assertEqual(result[0]["member"]["name"], "Ada")
        self.assertEqual(result[0]["member"]["tags"], [" red ", "red"])


if __name__ == "__main__":
    unittest.main()
