import unittest
from solution import project_to_box_edge

class BoxFiniteProbe(unittest.TestCase):
    def test_representable_boundary_and_parameter_with_large_finite_inputs(self):
        found = project_to_box_edge((-1e308, 0.0), (1e308, 0.0), (-1.5e308, -1.0, 1e308, 1.0))
        self.assertEqual(found, (1e308, 0.0, 2.0))

if __name__ == '__main__':
    unittest.main()
