import unittest
from solution import LinearTrainer

class Probe(unittest.TestCase):
    def test_post_epoch_binary_cross_entropy(self):
        trainer = LinearTrainer('binary', 1, 1, 100, 1).fit([[0], [0]], [1, 0])
        self.assertEqual(trainer.parameters()['bias'], -50.0)
        # Mean of softplus(50) and softplus(-50), equal to 25 to
        # ordinary floating precision. Probability clipping changes the loss.
        self.assertAlmostEqual(trainer.history()[0], 25.0, places=10)

if __name__ == '__main__':
    unittest.main()
