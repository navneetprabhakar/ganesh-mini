import unittest
from solution import DistributionController, ReplayBuffer

class Probe(unittest.TestCase):
    def test_zero_selects_first_positive_weight(self):
        controller = DistributionController(lambda state: [5e-324, 1e308], ReplayBuffer(1))
        self.assertEqual(controller.act(None, 0.0), 0)

if __name__ == '__main__':
    unittest.main()
