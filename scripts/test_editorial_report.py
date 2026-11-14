import unittest

from editorial_report import suggestions


class EditorialReportTests(unittest.TestCase):
    def test_shared_source_is_advisory_and_versions_are_deduplicated(self):
        pages = {
            'projects/a': {'front': {'type': 'benchmark', 'sources': ['https://arxiv.org/abs/2611.12345', 'https://arxiv.org/html/2611.12345v1']}, 'body': '', 'outgoing': set()},
            'projects/b': {'front': {'type': 'project', 'sources': ['https://arxiv.org/abs/2611.12345v2']}, 'body': '', 'outgoing': set()},
        }
        shared = [r for r in suggestions(pages) if r['kind'] == 'shared_source_review_not_duplicate_verdict']
        self.assertEqual(len(shared), 1)
        self.assertEqual(shared[0]['pages'], ['projects/a', 'projects/b'])

    def test_concept_navigation_and_topic_membership_are_separate(self):
        pages = {
            'topics/a': {'front': {'type': 'index'}, 'body': '', 'outgoing': {'concepts/a'}},
            'concepts/a': {'front': {'type': 'concept'}, 'body': '', 'outgoing': set()},
        }
        self.assertEqual(suggestions(pages), [{'kind': 'concept_without_concept_link', 'page': 'concepts/a'}])
