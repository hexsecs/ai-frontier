#!/usr/bin/env python3
"""Build the AI Frontier GitHub Pages search index from OpenShelf Markdown."""
import html
import json
import pathlib
import posixpath
import re
import sys

try:
    import markdown
    import yaml
except ImportError as exc:
    raise SystemExit("Install dependencies: pip install markdown PyYAML") from exc

ROOT = pathlib.Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
OUT = ROOT / "docs" / "data.json"

def split_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body.lstrip("\n")

def rewrite_links(rendered, page_id):
    def change(match):
        url = html.unescape(match.group(2))
        if url.startswith(("http:", "https:", "mailto:", "#", "data:")):
            return match.group(0)
        path = url.split("#", 1)[0]
        if not path.endswith(".md"):
            return match.group(0)
        target = posixpath.normpath(posixpath.join(posixpath.dirname(page_id), path))
        if target.startswith("../"):
            return match.group(0)
        suffix = target[:-3]
        return match.group(1) + "#/page/" + suffix + match.group(3)
    return re.sub(r'(href=")([^"]+)(")', change, rendered)

def main():
    pages = []
    for file in sorted(WIKI.rglob("*.md")):
        if file.name.startswith("_"):
            continue
        page_id = file.relative_to(WIKI).as_posix()[:-3]
        front, body = split_frontmatter(file.read_text(encoding="utf-8"))
        category = page_id.split("/", 1)[0]
        if category not in {"projects", "techniques", "briefings", "signals", "experiments", "evaluations"}:
            continue
        title = str(front.get("title") or re.search(r"^# (.+)$", body, re.M).group(1) if re.search(r"^# (.+)$", body, re.M) else page_id)
        summary = str(front.get("summary") or "")
        rendered = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
        rendered = rewrite_links(rendered, page_id)
        body_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", rendered))[:12000]
        pages.append({"id": page_id, "title": title, "summary": summary, "category": category,
                      "created": str(front.get("created") or ""), "updated": str(front.get("updated") or ""),
                      "body_text": html.unescape(body_text), "html": rendered})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"pages": pages}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Indexed {len(pages)} pages into {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
