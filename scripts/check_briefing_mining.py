#!/usr/bin/env python3
"""Require a traceable knowledge-mining audit in new AI Frontier briefings.

Historical briefings before 2026-11-07 are intentionally grandfathered.
This is a structural gate, not a substitute for reviewing source evidence.
"""
from datetime import date
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
cutoff = date(2026, 11, 7)
for path in sorted((root / "wiki/briefings").glob("*/*/*.md")):
    try:
        day = date.fromisoformat(path.stem)
    except ValueError:
        continue
    if day < cutoff:
        continue
    text = path.read_text(encoding="utf-8")
    required = (
        "## Knowledge mining",
        "### Canonical updates",
        "### Relations and evidence",
        "### Mining audit",
    )
    for heading in required:
        if not re.search(r"^" + re.escape(heading) + r"\s*$", text, re.M):
            errors.append(f"{path.relative_to(root)}: missing {heading}")
    # A heading with no content is not an audit.
    for i, heading in enumerate(required[1:]):
        match = re.search(r"^" + re.escape(heading) + r"\s*$", text, re.M)
        if not match:
            continue
        following = text[match.end():]
        body = re.split(r"^#{2,3}\s+", following, maxsplit=1, flags=re.M)[0]
        if len(body.strip()) < 35:
            errors.append(f"{path.relative_to(root)}: {heading} requires a substantive audit")
    if not re.search(r"wiki/(?:projects|concepts|techniques|signals|evaluations|experiments)/|\[\[", text):
        errors.append(f"{path.relative_to(root)}: no canonical wiki references found")
for err in errors:
    print("ERROR:", err)
print(f"Briefing mining audit: {len(errors)} errors")
sys.exit(bool(errors))
