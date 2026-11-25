import unittest
from scripts.premerge_authorize import authorize

class AuthorizationTests(unittest.TestCase):
    def test_stable(self):
        h="a"*40
        self.assertEqual(authorize("o/r",1,h,lambda *_:(h,"base")),(h,"base"))
    def test_changed(self):
        h="a"*40
        values=iter([(h,"base"),(h,"newbase")])
        with self.assertRaises(RuntimeError):
            authorize("o/r",1,h,lambda *_:next(values))
    def test_outage(self):
        def unavailable(*_):
            raise OSError("API unavailable")
        with self.assertRaises(OSError):
            authorize("o/r",1,"a"*40,unavailable)
    def test_wrong_head(self):
        with self.assertRaises(RuntimeError):
            authorize("o/r",1,"a"*40,lambda *_:("b"*40,"base"))
