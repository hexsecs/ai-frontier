"""Fresh PR-specific authorization. No cached check can authorize a merge."""
import json
import os
import re
import subprocess
import sys
from scripts.check_review_gate import check, resolve_commit

def gh(*args):
    return json.loads(subprocess.check_output(["gh", *args], text=True))

def snapshot(repo, number):
    owner, name = repo.split("/")
    pr = gh("pr", "view", str(number), "--repo", repo, "--json",
            "headRefOid,baseRefOid,baseRefName,mergeStateStatus,state,isDraft")
    if pr["state"] != "OPEN" or pr["isDraft"] or pr["baseRefName"] != "main":
        raise RuntimeError("Not an open, ready main-target PR")
    main = gh("api", f"repos/{repo}/git/ref/heads/main")["object"]["sha"]
    def collect(field, selection):
        query = ("query($owner:String!,$repo:String!,$pr:Int!,$endCursor:String)"
                 "{repository(owner:$owner,name:$repo){pullRequest(number:$pr){"
                 + field + "(first:100,after:$endCursor){nodes{" + selection
                 + "} pageInfo{hasNextPage endCursor}}}}}")
        pages = gh("api", "graphql", "--paginate", "--slurp", "-f", "query="+query,
                   "-f", "owner="+owner, "-f", "repo="+name, "-F", "pr="+str(number))
        return [node for page in pages for node in
                page["data"]["repository"]["pullRequest"][field]["nodes"]]
    reviews = collect("reviews", "author{login __typename} state body commit{oid}")
    threads = collect("reviewThreads", "isResolved")
    comments = collect("comments", "author{login __typename} body")
    error = check(pr, reviews, threads, main, comments, resolve_commit)
    if error:
        raise RuntimeError(error)
    # Native required checks must also be green. gh exits nonzero on pending,
    # failed or unavailable required checks.
    subprocess.run(["gh","pr","checks",str(number),"--repo",repo,"--required"],
                   check=True)
    return pr["headRefOid"], main

def authorize(repo, number, expected, read=snapshot):
    if not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise RuntimeError("Expected full head SHA required")
    first = read(repo, number)
    second = read(repo, number)
    if first != second or second[0] != expected:
        raise RuntimeError("Head or base changed during authorization")
    return second

if __name__ == "__main__":
    repo = os.environ["GITHUB_REPOSITORY"]
    number = int(sys.argv[1])
    expected = sys.argv[2]
    head, base = authorize(repo, number, expected)
    print(json.dumps({"pr":number,"head":head,"base":base,"authorized_snapshot":True}))
    # Advisory only: intentionally no merge operation until native protection,
    # required check configuration and live failure tests are verified.
