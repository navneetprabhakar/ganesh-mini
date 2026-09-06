import unittest
from solution import FrameBuffer

class Probe(unittest.TestCase):
    def test_contract(self):
        buffer = FrameBuffer()
        buffer.feed(b'\x02a')
        view = memoryview(b'b')
        view.release()
        with self.assertRaises(TypeError):
            buffer.feed(view)
        self.assertEqual(buffer.pending, b'\x02a')

if __name__ == '__main__':
    unittest.main()
