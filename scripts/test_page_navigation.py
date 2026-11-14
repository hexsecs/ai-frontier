import unittest

from page_navigation import attach_navigation, resolve_related, reachable_from


class PageNavigationTests(unittest.TestCase):
    def test_root_reachability_handles_cycles_and_disconnected_pages(self):
        graph = {'root': {'hub'}, 'hub': {'a'}, 'a': {'hub'}, 'unreachable': set()}
        self.assertEqual(reachable_from('root', graph), {'root', 'hub', 'a'})

    def test_explicit_links_only_and_direction_preserved(self):
        pages = [
            {'id': 'projects/a', 'html': '<p>mentions b</p><a href="#/page/concepts/b">B</a><code>projects/c</code>', 'related_raw': ['projects/c']},
            {'id': 'concepts/b', 'html': '<a href="https://example.org">source</a>'},
            {'id': 'projects/c', 'html': '<p>a</p>'},
        ]
        attach_navigation(pages)
        self.assertEqual(pages[0]['outgoing'], ['concepts/b'])
        self.assertEqual(pages[1]['backlinks'], ['projects/a'])
        self.assertEqual(pages[1]['outgoing'], [])
        self.assertEqual(pages[2]['backlinks'], [])
        self.assertEqual(pages[0]['related'], ['projects/c'])

    def test_legacy_slug_only_when_unambiguous(self):
        resolved, unresolved = resolve_related(['unique', 'same', '../private', 'projects/missing'], {'projects/unique', 'projects/same', 'concepts/same'})
        self.assertEqual(resolved, ['projects/unique'])
        self.assertEqual(unresolved, ['../private', 'projects/missing', 'same'])

    def test_invalid_targets_and_self_links_do_not_create_backlinks(self):
        pages = [{'id': 'projects/a', 'html': '<a href="#/page/missing">?</a><a href="#/page/projects/a">self</a>'}]
        attach_navigation(pages)
        self.assertEqual(pages[0]['outgoing'], [])
        self.assertEqual(pages[0]['backlinks'], [])

    def test_encoded_targets_are_normalized(self):
        pages = [{'id': 'projects/a', 'html': '<a href="#/page/concepts%2Fb">B</a>'}, {'id': 'concepts/b', 'html': ''}]
        attach_navigation(pages)
        self.assertEqual(pages[1]['backlinks'], ['projects/a'])
