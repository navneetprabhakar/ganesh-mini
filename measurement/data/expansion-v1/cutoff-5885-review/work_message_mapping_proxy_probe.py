import unittest
from types import MappingProxyType
from solution import WorkMessage


class MappingProxyTests(unittest.TestCase):
    def test_standard_readonly_mapping_is_accepted_and_detached(self):
        raw = {"id": "r", "accepted": True}
        message = WorkMessage("reply", MappingProxyType(raw))
        raw["accepted"] = False
        self.assertEqual(message.fields, {"id": "r", "accepted": True})


if __name__ == "__main__":
    unittest.main()
