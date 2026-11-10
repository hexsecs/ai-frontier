import unittest
import bleach
import markdown
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

    def test_bare_briefing_sources_are_clickable(self):
        source = "**Source:** https://arxiv.org/abs/2611.07372. **Implementation:** https://github.com/TracyTeam/tracybot."
        rendered = bleach.linkify(markdown.markdown(source), skip_tags=["pre", "code"])
        self.assertIn('href="https://arxiv.org/abs/2611.07372"', rendered)
        self.assertIn('href="https://github.com/TracyTeam/tracybot"', rendered)

    def test_existing_links_are_not_nested(self):
        rendered = bleach.linkify('<a href="#/page/projects/envopt">EnvOpt</a> and <a href="https://example.org">paper</a>', skip_tags=["pre", "code"])
        self.assertEqual(rendered.count("<a "), 2)

    def test_code_urls_remain_literal(self):
        rendered = bleach.linkify("<code>https://example.org</code><pre>https://example.org</pre>", skip_tags=["pre", "code"])
        self.assertNotIn("<a ", rendered)

    def test_traversal_rejected(self):
        self.assertEqual(expand_wikilinks('[[../secret]]'), '[[../secret]]')


if __name__ == "__main__":
    unittest.main()
