#!/usr/bin/env python3
"""Report external source URL availability; network errors never fail CI."""
import concurrent.futures
from pathlib import Path
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1] / "wiki"
urls = set()
for path in ROOT.rglob("*.md"):
    if path.name.startswith("_"):
        continue
    urls.update(u.rstrip(".,;)") for u in re.findall(r'https?://[^\s<>"\]]+', path.read_text(encoding="utf-8")))
urls = sorted(urls)
print(f"Checking {len(urls)} unique external URLs (advisory only)", flush=True)


def check(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "AI-Frontier-Link-Audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return url, resp.status, ""
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405, 429):
            return url, exc.code, "access restricted or rate limited"
        return url, exc.code, "HTTP error"
    except Exception as exc:
        return url, "unknown", type(exc).__name__


with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(check, urls))
bad = [(url, status, note) for url, status, note in results if status != 200 and status != 204 and status != 301 and status != 302]
for url, status, note in bad:
    print(f"WARNING [{status}] {url} ({note})")
print(f"External audit: {len(urls) - len(bad)} healthy, {len(bad)} warnings; advisory, no failure")
