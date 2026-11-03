#!/usr/bin/env python3
"""AI Frontier metadata policy (stricter than OpenShelf 1.7 core contract)."""
from datetime import date
from pathlib import Path
import uuid
import yaml

ROOT = Path(__file__).resolve().parents[1]
seen = {}
errors = []
for path in sorted((ROOT / "wiki").rglob("*.md")):
    rel = path.relative_to(ROOT / "wiki")
    if any(part.startswith(("_", ".")) for part in rel.parts):
        continue
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---" not in text[4:]:
        errors.append(f"{rel}: missing YAML frontmatter")
        continue
    front = yaml.safe_load(text[4:].split("\n---", 1)[0]) or {}
    if front.get("type") == "index":
        if not front.get("title"):
            errors.append(f"{rel}: index missing title")
        continue
    for field in ("uid", "title", "summary", "type", "created", "updated", "depth", "sources"):
        if field not in front:
            errors.append(f"{rel}: missing {field}")
    if not isinstance(front.get("title"), str) or not front.get("title", "").strip():
        errors.append(f"{rel}: invalid title")
    summary = front.get("summary")
    if not isinstance(summary, str) or not 0 < len(summary) <= 160:
        errors.append(f"{rel}: summary must be 1-160 characters")
    if front.get("depth") not in ("stub", "brief", "full", "deep"):
        errors.append(f"{rel}: invalid depth")
    if not isinstance(front.get("sources"), list):
        errors.append(f"{rel}: sources must be a list")
    try:
        identity = str(uuid.UUID(str(front.get("uid"))))
        if identity in seen:
            errors.append(f"{rel}: duplicate uid also in {seen[identity]}")
        seen[identity] = rel
    except (ValueError, TypeError, AttributeError):
        errors.append(f"{rel}: invalid UUID")
    for field in ("created", "updated"):
        value = front.get(field)
        if not isinstance(value, date):
            try:
                date.fromisoformat(str(value))
            except ValueError:
                errors.append(f"{rel}: invalid {field} date")
for error in errors:
    print("ERROR:", error)
print(f"Validated {len(seen)} content page identities; {len(errors)} errors")
raise SystemExit(bool(errors))
