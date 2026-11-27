import unittest
from scripts.briefing_checkpoint import advance

class CheckpointTests(unittest.TestCase):
    def test_missing_predecessor(self):
        with self.assertRaises(ValueError):
            advance({}, "merge", {"head":"a","commit":"b"})
    def test_stale_head(self):
        state = {"research":{}, "briefing":{}, "ingestion":{}, "pr":{"head":"a"}}
        with self.assertRaises(ValueError):
            advance(state, "validation", {"head":"b","checks":{"lint":"success"}})
    def test_rewind(self):
        self.assertEqual(advance({"research":{"sources":["old"]},"briefing":{}}, "research", {"sources":["new"]}), {"research":{"sources":["new"]}})
