import unittest
from solution import train_centroids, predict


class CentroidExtremesTests(unittest.TestCase):
    def test_finite_mean_without_intermediate_overflow(self):
        self.assertEqual(train_centroids([("x", [1e308]), ("x", [1e308])]), {"x": (1e308,)})

    def test_nearest_finite_centroid_without_squared_overflow(self):
        self.assertEqual(predict({"far": (2e200,), "near": (1e200,)}, [0.0]), "near")


if __name__ == "__main__":
    unittest.main()
