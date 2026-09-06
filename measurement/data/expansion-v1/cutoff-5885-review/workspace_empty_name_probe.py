import unittest
from solution import MemoryWorkspace


class WorkspaceNameTests(unittest.TestCase):
    def test_empty_append_name_is_invalid_not_unknown(self):
        with self.assertRaises(ValueError):
            MemoryWorkspace().append("   ", {})


if __name__ == "__main__":
    unittest.main()
