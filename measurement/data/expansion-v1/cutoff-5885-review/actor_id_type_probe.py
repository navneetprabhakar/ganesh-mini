import unittest

from solution import advance_actors


class ActorIdTypeTests(unittest.TestCase):
    def test_nonstring_id_raises_type_error(self):
        with self.assertRaises(TypeError):
            advance_actors(2, 2, [{"id": 1, "x": 0, "y": 0}], {})


if __name__ == "__main__":
    unittest.main()
