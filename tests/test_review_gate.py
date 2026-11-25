import unittest
from scripts.check_review_gate import check

class ReviewGateTests(unittest.TestCase):
    def test_cases(self):
        pr = dict(headRefOid="head", baseRefOid="base", mergeStateStatus="CLEAN")
        receipt = dict(author={"login":"chatgpt-codex-connector"}, state="COMMENTED", commit={"oid":"head"}, body="<!-- codex-review-receipt:v1 -->")
        self.assertIsNone(check(pr,[receipt],[],"base"))
        self.assertIsNotNone(check(pr,[],[],"base"))
        self.assertIsNotNone(check(pr,[dict(receipt,commit={"oid":"old"})],[],"base"))
        self.assertIsNotNone(check(pr,[dict(receipt,author={"login":"other"})],[],"base"))
        self.assertIsNotNone(check(pr,[receipt],[{"isResolved":False}],"base"))
        self.assertIsNotNone(check(pr,[receipt],[],"newbase"))

if __name__ == "__main__":
    unittest.main()
