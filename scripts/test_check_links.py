import unittest

from check_links import visible_html


class VisibleHtmlTests(unittest.TestCase):
    def test_wikilink_example_in_code_is_documentation(self):
        page_html = '<p>Syntax: <code>[[&lt;kb-id&gt;:&lt;page-id&gt;]]</code> shorthand.</p>'
        self.assertNotIn('[[', visible_html(page_html))

    def test_wikilink_example_in_pre_is_documentation(self):
        page_html = '<pre><code>[[projects/example]]</code></pre>'
        self.assertNotIn('[[', visible_html(page_html))

    def test_unrendered_reference_in_prose_still_visible(self):
        page_html = '<p>See [[projects/missing]] for details.</p>'
        self.assertIn('[[projects/missing]]', visible_html(page_html))

    def test_prose_around_code_is_kept(self):
        page_html = '<p>Before <code>[[x]]</code> after [[projects/missing]].</p>'
        visible = visible_html(page_html)
        self.assertIn('Before', visible)
        self.assertIn('[[projects/missing]]', visible)
        self.assertNotIn('[[x]]', visible)


if __name__ == '__main__':
    unittest.main()
