import unittest
from collections import UserString
from solution import resolve_panel


class AuthenticationTypeTests(unittest.TestCase):
    def test_non_string_equal_value_does_not_authenticate(self):
        result = resolve_panel({"signed_in": UserString("yes"), "user": "u"}, ["home"])
        self.assertEqual(result, {"screen": "sign_in", "user": None, "menu": []})


if __name__ == "__main__":
    unittest.main()
