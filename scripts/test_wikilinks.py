import unittest
from build_site import expand_wikilinks, rewrite_links


class WikiLinkTests(unittest.TestCase):
    def test_basic_reference(self):
        self.assertEqual(expand_wikilinks("[[projects/strategist]]"), '<a href="#/page/projects/strategist">strategist</a>')

    def test_label(self):
        self.assertEqual(expand_wikilinks("[[concepts/capability-locus|Capability locus]]"), '<a href="#/page/concepts/capability-locus">Capability locus</a>')

    def test_nested_briefing(self):
        self.assertIn('#/page/briefings/2026/11/2026-11-03', expand_wikilinks('[[briefings/2026/11/2026-11-03]]'))

    def test_legacy_markdown(self):
        self.assertIn('#/page/projects/strategist', rewrite_links('<a href="../projects/strategist.md">X</a>', 'concepts/preservation-aware-agent-improvement'))

    def test_escape_label(self):
        self.assertIn('&lt;script&gt;', expand_wikilinks('[[projects/strategist|<script>]]'))

    def test_traversal_rejected(self):
        self.assertEqual(expand_wikilinks('[[../secret]]'), '[[../secret]]')


if __name__ == "__main__":
    unittest.main()
