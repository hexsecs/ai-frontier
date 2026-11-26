"""Fresh PR-specific authorization. No cached check can authorize a merge."""
import json
import os
import re
import subprocess
import sys
from scripts.check_review_gate import check, resolve_commit

def gh(*args):
    return json.loads(subprocess.check_output(["gh", *args], text=True))

def verify_checks(requirements, runs, head):
    if not requirements or not {"lint","mining-audit"}.issubset({n for n,_ in requirements}):
        raise RuntimeError("Required validation contexts missing")
    for name, app in set(requirements):
        if not isinstance(app,int) or app <= 0:
            raise RuntimeError("Unbound required check source")
        matching = [r for r in runs if r["name"] == name and r["app"]["id"] == app
                    and r["head_sha"] == head]
        if not matching:
            raise RuntimeError("Missing required check: "+name)
        latest = max(matching,key=lambda r:r["id"])
        if latest["status"] != "completed" or latest["conclusion"] != "success":
            raise RuntimeError("Nonpassing required check: "+name)

def required_contexts(rules, protection=None):
    requirements = []
    if protection is not None:
        requirements = [(c["context"], c["app_id"]) for c in protection["checks"]]
        if not protection["strict"] or set(protection["contexts"]) != {n for n,_ in requirements}:
            raise RuntimeError("Strict source-bound classic protection required")
    for rule in rules:
        if rule["type"] == "required_status_checks":
            params = rule["parameters"]
            if not params["strict_required_status_checks_policy"]:
                raise RuntimeError("Non-strict ruleset")
            requirements.extend((c["context"],c.get("integration_id")) for c in
                                params["required_status_checks"])
    if not requirements:
        raise RuntimeError("No effective required checks")
    return requirements

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
    # Effective branch rules are authoritative for ruleset-only deployments.
    # Classic protection, when enabled, is additive; never ignore read errors.
    branch = gh("api", f"repos/{repo}/branches/main")
    rule_pages = gh("api", "--paginate", "--slurp",
                    f"repos/{repo}/rules/branches/main?per_page=100")
    if not isinstance(rule_pages, list) or not rule_pages or any(not isinstance(page, list) for page in rule_pages):
        raise RuntimeError("Invalid effective branch rules response")
    rules = [rule for page in rule_pages for rule in page]
    protection = None
    if branch["protection"]["enabled"]:
        protection = gh("api", f"repos/{repo}/branches/main/protection/required_status_checks")
    requirements = required_contexts(rules, protection)
    pages = gh("api","--paginate","--slurp",
               f"repos/{repo}/commits/{pr['headRefOid']}/check-runs?filter=all&per_page=100")
    verify_checks(requirements, [c for page in pages for c in page["check_runs"]],
                  pr["headRefOid"])
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
