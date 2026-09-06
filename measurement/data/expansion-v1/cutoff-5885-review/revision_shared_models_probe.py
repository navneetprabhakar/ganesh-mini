import unittest
from solution import apply_revision, rollback_revision


class RevisionSharedModelsTests(unittest.TestCase):
    def test_apply_preserves_unrelated_model_sharing_source_list(self):
        fields = [{'name': 'title', 'kind': 'text'}]
        result = apply_revision({'Article': fields, 'Other': fields})
        self.assertEqual(result['Other'], fields)

    def test_rollback_preserves_unrelated_model_sharing_source_list(self):
        fields = [{'name': 'reviewers', 'kind': 'references', 'optional': True}]
        result = rollback_revision({'Article': fields, 'Other': fields})
        self.assertEqual(result['Other'], fields)


if __name__ == '__main__':
    unittest.main()
