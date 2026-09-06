import unittest
from solution import validate_mounts


class Hostile:
    def __eq__(self, other):
        raise RuntimeError("field comparison escaped")


class MountFieldTests(unittest.TestCase):
    def test_wrong_type_field_never_raises(self):
        mounts = [
            {"prefix": Hostile(), "module": "control.urls"},
            {"prefix": "/", "module": "records.urls"},
            {"prefix": "/session/", "module": "accounts.urls"},
        ]
        self.assertIs(validate_mounts(mounts), False)


if __name__ == "__main__":
    unittest.main()
