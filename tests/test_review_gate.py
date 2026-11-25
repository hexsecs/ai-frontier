import unittest
from scripts.check_review_gate import check

class ReviewGateTests(unittest.TestCase):
    def test_cases(self):
        pr = dict(headRefOid="head", baseRefOid="base", mergeStateStatus="CLEAN")
        receipt = dict(author={"login":"chatgpt-codex-connector[bot]","__typename":"Bot"}, state="COMMENTED", commit={"oid":"head"}, body="<!-- codex-review-receipt:v1 -->")
        self.assertIsNone(check(pr,[receipt],[],"base"))
        self.assertIsNotNone(check(pr,[],[],"base"))
        self.assertIsNotNone(check(pr,[dict(receipt,state="DISMISSED")],[],"base"))
        self.assertIsNotNone(check(pr,[receipt,dict(receipt,state="CHANGES_REQUESTED")],[],"base"))
        self.assertIsNone(check(pr,[dict(receipt,author={"login":"chatgpt-codex-connector","__typename":"Bot"})],[],"base"))
        self.assertIsNotNone(check(pr,[dict(receipt,author={"login":"chatgpt-codex-connector","__typename":"User"})],[],"base"))
        self.assertIsNotNone(check(pr,[dict(receipt,commit={"oid":"old"})],[],"base"))
        self.assertIsNotNone(check(pr,[dict(receipt,author={"login":"other"})],[],"base"))
        self.assertIsNotNone(check(pr,[receipt],[{"isResolved":False}],"base"))
        self.assertIsNotNone(check(pr,[receipt],[],"newbase"))

    def test_comment_receipt(self):
        head = "a" * 40
        pr = dict(headRefOid=head, baseRefOid="base", mergeStateStatus="CLEAN")
        comment = dict(author={"login":"chatgpt-codex-connector","__typename":"Bot"}, body="<!-- codex-review-receipt:v1 -->\n**Reviewed commit:** `"+head+"`")
        self.assertIsNone(check(pr,[],[],"base",[comment]))
        self.assertIsNotNone(check(pr,[],[],"base",[dict(comment,body=comment["body"].replace(head,head[:10]))]))
        self.assertIsNotNone(check(pr,[],[],"base",[dict(comment,author={"login":"chatgpt-codex-connector","__typename":"User"})]))

if __name__ == "__main__":
    unittest.main()
