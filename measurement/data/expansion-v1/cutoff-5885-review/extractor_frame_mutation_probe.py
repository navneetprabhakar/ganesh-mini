import unittest

from solution import extract_dataset


class FrameIsolationTests(unittest.TestCase):
    def test_extractor_cannot_mutate_caller_frame_through_argument(self):
        frame = {"values": [1]}

        def extractor(value):
            value["values"].append(2)
            return value

        extract_dataset([("x", [frame])], extractor)
        self.assertEqual(frame, {"values": [1]})


if __name__ == "__main__":
    unittest.main()
