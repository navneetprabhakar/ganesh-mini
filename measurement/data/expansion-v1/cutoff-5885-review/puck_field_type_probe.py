import unittest
from solution import PuckState, advance_puck


class PuckFieldTypeTests(unittest.TestCase):
    def test_noninteger_field_has_type_error(self):
        with self.assertRaises(TypeError):
            advance_puck(PuckState(float("nan"), 0, 1), 5)


if __name__ == "__main__":
    unittest.main()
