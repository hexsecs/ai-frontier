import unittest
from check_article_prose import check


class ArticleProseTests(unittest.TestCase):
    def test_rejects_revision_diary(self):
        self.assertTrue(check('This page was updated with two sources.'))
        self.assertTrue(check('Mining pass 2 promoted this concept.'))
        self.assertTrue(check('## Canonical updates\nCreated five pages.'))

    def test_accepts_evidence_and_citations(self):
        self.assertEqual(check('The authors report 30 trials [source](https://example.org/paper). '
                               'Compare [[projects/example]]. No independent replication is cited.'), [])

    def test_accepts_process_as_subject(self):
        self.assertEqual(check('The ingestion pipeline validates evidence before accepting changes. '
                               'A proposed experiment compares two mining methods.'), [])

    def test_ignores_literal_examples_and_metadata(self):
        self.assertEqual(check('---\nupdated: 2026-11-14\n---\n~~~text\nThis page was updated.\n~~~\n'), [])


if __name__ == '__main__':
    unittest.main()
