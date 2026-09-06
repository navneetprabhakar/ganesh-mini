import unittest
from solution import decode_packet

class Probe(unittest.TestCase):
    def test_valid_unique_direct_fields_in_other_order(self):
        xml = '<packet><topic>b</topic><sender>a</sender><message>c</message></packet>'
        self.assertEqual(decode_packet(xml, 'application/vnd.packet+xml'), {'sender': 'a', 'topic': 'b', 'message': 'c'})

if __name__ == '__main__':
    unittest.main()
