import unittest
from solution import dispatch_zone_jobs


class DispatchCopyTests(unittest.TestCase):
    def test_submit_cannot_mutate_nested_identifier(self):
        entries = [{"identifier": ["id"], "location": {"zone": "z"}}]
        dispatch_zone_jobs(entries, "z", lambda value: value.append("changed"))
        self.assertEqual(entries[0]["identifier"], ["id"])


if __name__ == "__main__":
    unittest.main()
