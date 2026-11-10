#!/usr/bin/env python3
"""Validate OpenShelf wiki references and generated site routes."""
import argparse
from html.parser import HTMLParser
import html
import json
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
WIKILINK = re.compile(r'\[\[([^\]\n]+)\]\]')
MDLINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def body_only(text):
    if text.startswith("---\n"):
        text = text.split("\n---", 1)[-1]
    text = re.sub(r'(?ms)^ {0,3}(?:\x60{3,}|~{3,}).*?^ {0,3}(?:\x60{3,}|~{3,})\s*$', '', text)
    return re.sub(r'\x60[^\x60\n]+\x60', '', text)


def check_source():
    ids = {p.relative_to(WIKI).as_posix()[:-3] for p in WIKI.rglob("*.md") if not p.name.startswith("_")}
    errors, inbound = [], set()
    for path in sorted(WIKI.rglob("*.md")):
        if path.name.startswith("_"):
            continue
        page = path.relative_to(WIKI).as_posix()[:-3]
        body = body_only(path.read_text(encoding="utf-8"))
        for match in WIKILINK.finditer(body):
            target = match.group(1).split("|", 1)[0].strip().removesuffix(".md")
            if target not in ids:
                errors.append(f"{page}: missing wiki target [[{target}]]")
            else:
                inbound.add(target)
        for match in MDLINK.finditer(body):
            raw = unquote(html.unescape(match.group(1))).split("#", 1)[0].split("?", 1)[0]
            if not raw.endswith(".md") or raw.startswith(("/", "//")):
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(page), raw))[:-3]
            if target not in ids:
                errors.append(f"{page}: missing Markdown target {raw}")
            else:
                inbound.add(target)
    orphans = sorted(ids - inbound)
    print(f"Source: {len(ids)} pages, {len(errors)} broken links, {len(orphans)} orphan candidates")
    for orphan in orphans[:30]:
        print("WARNING orphan candidate:", orphan)
    for error in errors:
        print("ERROR:", error)
    return errors


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(v for k, v in attrs if k == "href" and v is not None)


def check_rendered():
    path = ROOT / "docs" / "data.json"
    if not path.exists():
        return ["docs/data.json missing; build site first"]
    pages = json.loads(path.read_text(encoding="utf-8"))["pages"]
    ids = {p["id"] for p in pages}
    errors = []
    for page in pages:
        parser = Links()
        parser.feed(page["html"])
        for link in parser.hrefs:
            if link.startswith("#/page/"):
                target = unquote(link[len("#/page/"):].split("?", 1)[0].split("#", 1)[0])
                if target not in ids:
                    errors.append(f"{page['id']}: broken rendered route {link}")
        if re.search(r'\[\[[^\]\n]+\]\]', page["html"]):
            errors.append(f"{page['id']}: unrendered wiki reference")
    print(f"Rendered: {len(pages)} pages, {len(errors)} link errors")
    for error in errors:
        print("ERROR:", error)
    return errors


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rendered", action="store_true")
    args = ap.parse_args()
    sys.exit(bool(check_rendered() if args.rendered else check_source()))
