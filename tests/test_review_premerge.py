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

class CheckCoverageTests(unittest.TestCase):
    def test_coverage(self):
        from scripts.premerge_authorize import verify_checks
        h="a"*40
        req=[("lint",1),("mining-audit",1)]
        runs=[dict(name=n,app={"id":1},head_sha=h,id=i,status="completed",conclusion="success") for i,(n,_) in enumerate(req)]
        verify_checks(req,runs,h)
        for bad in [runs[:1], [runs[0],dict(runs[1],conclusion="cancelled")], [runs[0],dict(runs[1],app={"id":2})], [runs[0],dict(runs[1],head_sha="b"*40)]]:
            with self.assertRaises(RuntimeError):
                verify_checks(req,bad,h)
