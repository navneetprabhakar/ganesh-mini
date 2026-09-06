import unittest
from solution import PolicyStore


class PolicyInputTests(unittest.TestCase):
    def test_generator_group_input_is_supported(self):
        store = PolicyStore({"u": {"secret": "x", "groups": (g for g in ["read"])}}, {})
        self.assertEqual(store.groups_for("u"), ("read",))

    def test_unicode_secret_authentication(self):
        store = PolicyStore({"u": {"secret": "é", "groups": []}}, {})
        self.assertTrue(store.authenticate("u", "é"))


if __name__ == "__main__":
    unittest.main()
