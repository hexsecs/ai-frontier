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

class RulesetTests(unittest.TestCase):
    def test_ruleset_only(self):
        from scripts.premerge_authorize import required_contexts
        rule={"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":True,"required_status_checks":[{"context":"lint","integration_id":15368}]}}
        self.assertEqual(required_contexts([rule]),[("lint",15368)])
        with self.assertRaises(RuntimeError):
            required_contexts([])
        rule["parameters"]["strict_required_status_checks_policy"]=False
        with self.assertRaises(RuntimeError):
            required_contexts([rule])

    def test_snapshot_requires_checks_from_every_rules_page(self):
        from unittest.mock import patch
        from scripts.premerge_authorize import snapshot
        h = "a"*40
        base = "b"*40
        def rule(*names):
            return {"type":"required_status_checks","parameters":{
                "strict_required_status_checks_policy":True,
                "required_status_checks":[{"context":n,"integration_id":1} for n in names]}}
        def run(n,i):
            return dict(name=n,app={"id":1},head_sha=h,id=i,status="completed",conclusion="success")
        def api(*args):
            if args[0] == "pr":
                return dict(headRefOid=h,baseRefOid=base,baseRefName="main",
                            mergeStateStatus="CLEAN",state="OPEN",isDraft=False)
            if "git/ref/heads/main" in args[-1]:
                return {"object":{"sha":base}}
            if args[1] == "graphql":
                return [{"data":{"repository":{"pullRequest":{
                    n:{"nodes":[]} for n in ("reviews","reviewThreads","comments")}}}}]
            if args[-1].endswith("/branches/main"):
                return {"protection":{"enabled":False}}
            if "/rules/branches/main" in args[-1]:
                self.assertIn("--paginate",args)
                self.assertIn("--slurp",args)
                return [[rule("lint","mining-audit")],[rule("extra")]]
            if "/check-runs?" in args[-1]:
                return [{"check_runs":[run("lint",1),run("mining-audit",2)]}]
            raise AssertionError(args)
        with patch("scripts.premerge_authorize.gh",side_effect=api), patch("scripts.premerge_authorize.check",return_value=None):
            with self.assertRaisesRegex(RuntimeError,"Missing required check: extra"):
                snapshot("o/r",1)
