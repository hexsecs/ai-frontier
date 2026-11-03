#!/usr/bin/env python3
"""One-time OpenShelf 1.7 adoption: mint missing stable page UUIDs, preserve dates."""
from pathlib import Path
import uuid
import yaml

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "wiki"

def main():
    count = 0
    for path in sorted(PAGES.rglob("*.md")):
        if any(part.startswith(("_", ".")) for part in path.relative_to(PAGES).parts):
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            raise ValueError(f"{path}: missing frontmatter")
        head, sep, body = text[4:].partition("\n---")
        if not sep:
            raise ValueError(f"{path}: unclosed frontmatter")
        metadata = yaml.safe_load(head) or {}
        if metadata.get("type") == "index":
            continue
        additions = []
        if not metadata.get("uid"):
            additions.append(f"uid: {uuid.uuid4()}")
        if not metadata.get("depth"):
            additions.append("depth: deep" if "/briefings/" in path.as_posix() else "depth: brief")
        if additions:
            path.write_text("---\n" + "\n".join(additions) + "\n" + head + "\n---" + body, encoding="utf-8")
            count += 1
    print(f"Updated {count} content pages; existing identities and creation dates preserved")

if __name__ == "__main__":
    main()
