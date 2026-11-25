"""Fail closed on missing, stale or unresolved Codex review evidence."""
import re
import sys
import json

TRUSTED = "chatgpt-codex-connector"

def check(pr, reviews, threads, main_sha):
    head = pr["headRefOid"]
    if pr["baseRefOid"] != main_sha or pr["mergeStateStatus"] in ("BEHIND", "DIRTY", "UNKNOWN"):
        return "Synchronize with current main before review"
    receipts = []
    for review in reviews:
        if (review.get("author") or {}).get("login") != TRUSTED:
            continue
        if review.get("state") not in ("COMMENTED", "APPROVED"):
            continue
        if review.get("commit", {}).get("oid") != head:
            continue
        if "<!-- codex-review-receipt:v1 -->" not in review.get("body", ""):
            continue
        receipts.append(review)
    if not receipts:
        return "No trusted review receipt for current head"
    for thread in threads:
        if not thread["isResolved"]:
            return "Unresolved review thread"
    if any(r.get("state") == "CHANGES_REQUESTED" for r in reviews):
        return "Changes requested; dismiss superseded review or obtain resolution"
    return None

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = json.load(f)
    error = check(data["pr"], data["reviews"], data["threads"], data["main_sha"])
    if error:
        sys.exit(error)
    print("Current-head review gate passed")
