import unittest
from solution import merge_identity


class SharedAccountTests(unittest.TestCase):
    def test_only_selected_account_email_changes(self):
        account = {"username": "u", "email": "old", "password": "p"}
        result, selected = merge_identity({"a": account, "b": account},
                                          {"external_key": "a", "email": "new", "secret": "s"})
        self.assertIs(selected, result["a"])
        self.assertEqual(result["b"]["email"], "old")


if __name__ == "__main__":
    unittest.main()
