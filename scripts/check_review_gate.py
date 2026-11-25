"""Fail closed on missing, stale or unresolved Codex review evidence."""
import re
import sys
import json

TRUSTED = "chatgpt-codex-connector"

def trusted(author):
    author = author or {}
    return author.get("__typename") == "Bot" and author.get("login", "").removesuffix("[bot]") == TRUSTED

def check(pr, reviews, threads, main_sha, comments=()):
    head = pr["headRefOid"]
    if pr["baseRefOid"] != main_sha or pr["mergeStateStatus"] in ("BEHIND", "DIRTY", "UNKNOWN"):
        return "Synchronize with current main before review"
    receipts = []
    for review in reviews:
        if not trusted(review.get("author")):
            continue
        if review.get("state") not in ("COMMENTED", "APPROVED"):
            continue
        if review.get("commit", {}).get("oid") != head:
            continue
        if "<!-- codex-review-receipt:v1 -->" not in review.get("body", ""):
            continue
        receipts.append(review)
    for comment in comments:
        if not trusted(comment.get("author")):
            continue
        body = comment.get("body", "")
        if "<!-- codex-review-receipt:v1 -->" not in body:
            continue
        matches = re.findall(r"(?m)^\s*\*\*Reviewed commit:\*\*\s*`([0-9a-f]{10,40})`\s*$", body)
        if len(matches) == 1 and matches[0] == head:
            receipts.append(comment)
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
    error = check(data["pr"], data["reviews"], data["threads"], data["main_sha"], data["comments"])
    if error:
        sys.exit(error)
    print("Current-head review gate passed")
