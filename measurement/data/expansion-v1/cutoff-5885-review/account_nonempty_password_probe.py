import unittest

from solution import AccountRegistry


class PasswordPreservationTests(unittest.TestCase):
    def test_nonempty_whitespace_password_remains_exact(self):
        registry = AccountRegistry()
        registry.register("user", "u@example.com", " ", "First", "Last")
        self.assertIsInstance(registry.login("user", " "), str)
        with self.assertRaises(PermissionError):
            registry.login("user", "")


if __name__ == "__main__":
    unittest.main()
