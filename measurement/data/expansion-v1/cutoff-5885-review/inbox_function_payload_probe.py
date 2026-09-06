import unittest
from solution import CommandInbox

class Probe(unittest.TestCase):
    def test_accepted_function_payload_is_not_isolated(self):
        def payload():
            return None
        payload.items = [1]
        inbox = CommandInbox(['u'])
        result = inbox.submit('u', {'action': 'store', 'payload': payload})
        result['result'].items.append(2)
        self.assertEqual(inbox.stored()[0].items, [1])

if __name__ == '__main__':
    unittest.main()
