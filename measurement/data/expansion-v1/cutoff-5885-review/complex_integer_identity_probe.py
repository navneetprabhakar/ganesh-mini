import unittest
from solution import LinearComplexSystem


class ComplexIntegerIdentityTests(unittest.TestCase):
    def test_allowed_integer_system_has_representable_solution(self):
        value = 10 ** 400
        system = LinearComplexSystem([[value]], [value])
        self.assertEqual(system.solve(), [1 + 0j])


if __name__ == '__main__':
    unittest.main()
