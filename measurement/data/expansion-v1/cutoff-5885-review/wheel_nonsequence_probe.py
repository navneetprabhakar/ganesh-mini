import unittest
from solution import correct_wheel_speeds


class WheelSequenceTests(unittest.TestCase):
    def test_set_is_not_an_encoder_sequence(self):
        with self.assertRaises(TypeError):
            correct_wheel_speeds(set(), set(), 10)


if __name__ == "__main__":
    unittest.main()
