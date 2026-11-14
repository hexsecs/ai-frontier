import tempfile
from pathlib import Path
import unittest
from check_briefing_mining import validate


class KnowledgeIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.wiki = Path(self.tmp.name)
        (self.wiki / 'projects').mkdir()
        (self.wiki / 'projects/example.md').touch()

    def test_links_must_belong_to_each_finding(self):
        text = '## 1. First\n[[projects/example]]\n## 2. Second\nNo link.\n## Synthesis\n[[projects/example]]'
        self.assertEqual(len(validate(text, self.wiki)), 1)

    def test_nested_findings_and_aliased_links(self):
        self.assertEqual(validate('## Findings\n### 1. Example\nSee [[projects/example|Example]].', self.wiki), [])

    def test_footer_cannot_satisfy_ingestion(self):
        errors = validate('## 1. Example\nNo link.\n## Knowledge mining\n[[projects/example]]', self.wiki)
        self.assertEqual(len(errors), 2)

    def test_missing_target(self):
        self.assertTrue(validate('## 1. Example\n[[projects/missing]]', self.wiki))

    def test_fenced_links_do_not_count(self):
        self.assertTrue(validate('## 1. Example\n```text\n[[projects/example]]\n```', self.wiki))


if __name__ == '__main__':
    unittest.main()
