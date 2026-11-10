#!/usr/bin/env python3
"""Build the AI Frontier GitHub Pages search index from OpenShelf Markdown."""
import html
import base64
import shutil
import urllib.parse
import json
import pathlib
import posixpath
import re
import sys
from chatgpt_charts import convert as convert_chatgpt_charts

try:
    import markdown
    import yaml
    import bleach
except ImportError as exc:
    raise SystemExit("Install dependencies: pip install markdown PyYAML") from exc

ROOT = pathlib.Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
OUT = ROOT / "docs" / "data.json"


WIKILINK = re.compile(r'\[\[([A-Za-z0-9_./-]+)(?:\|([^\]\n]+))?\]\]')

def expand_wikilinks(body):
    """Convert OpenShelf wiki references before Markdown rendering."""
    def replace(match):
        target, label = match.group(1), match.group(2)
        if target.startswith("/") or ".." in target.split("/"):
            return match.group(0)
        target = target.removesuffix(".md")
        label = label or target.split("/")[-1].replace("-", " ")
        # Escape label to prevent Markdown/HTML injection from wiki titles.
        return '<a href="#/page/' + urllib.parse.quote(target, safe="/-_.") + '">' + html.escape(label) + '</a>'
    return WIKILINK.sub(replace, body)

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

def enhance_media(rendered, file):
    def replace_image(match):
        attrs = match.group(1)
        src_match = re.search(r'src="([^"]+)"', attrs)
        if not src_match:
            return match.group(0)
        src = html.unescape(src_match.group(1))
        parsed = urllib.parse.urlsplit(src)
        if not parsed.scheme and not src.startswith(("//", "#", "data:")):
            source = (file.parent / urllib.parse.unquote(parsed.path)).resolve()
            if source.is_file() and source.is_relative_to(ROOT) and source.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}:
                dest = ROOT / "docs" / "assets" / source.relative_to(ROOT)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                url = "./assets/" + urllib.parse.quote(source.relative_to(ROOT).as_posix())
                attrs = attrs.replace(src_match.group(0), 'src="' + html.escape(url, quote=True) + '"')
        alt_match = re.search(r'alt="([^"]*)"', attrs)
        caption = alt_match.group(1) if alt_match else ""
        return ('<figure class="briefing-figure"><a href="' +
                html.escape(re.search(r'src="([^"]+)"', attrs).group(1), quote=True) +
                '" target="_blank" rel="noopener noreferrer" aria-label="Open full-size image">' +
                '<img' + attrs + ' loading="lazy" decoding="async"></a>' +
                ('<figcaption>' + caption + '</figcaption>' if caption else '') + '</figure>')
    return re.sub(r'<img\\b([^>]*?)/?>', replace_image, rendered)



def embed_visualizations(body):
    """Compile supported fenced Markdown into inert, validated visualization specs."""
    pattern = re.compile(r'^```(chart|vega-lite|mermaid|graph)\s*\n(.*?)^```\s*$', re.M | re.S)
    def replace(match):
        kind, raw = match.group(1), match.group(2).strip()
        if len(raw) > 100_000:
            raise ValueError("Visualization specification exceeds 100 KB")
        if kind != "mermaid":
            try:
                spec = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid {kind} JSON: {exc}") from exc
            if not isinstance(spec, dict):
                raise ValueError(f"{kind} must contain a JSON object")
            if kind == "graph" and (not isinstance(spec.get("nodes"), list) or not isinstance(spec.get("edges"), list)):
                raise ValueError("graph requires nodes and edges arrays")
            if kind == "chart" and (spec.get("type") not in {"bar", "line", "scatter", "pie", "doughnut", "radar"} or not isinstance(spec.get("labels"), list) or not isinstance(spec.get("datasets"), list)):
                raise ValueError("chart requires a supported type, labels and datasets")
            if kind == "vega-lite" and not isinstance(spec.get("mark"), (str, dict)) and not isinstance(spec.get("layer"), list):
                raise ValueError("vega-lite requires mark or layer")
            raw = json.dumps(spec, separators=(",", ":"))
        encoded = base64.b64encode(raw.encode("utf-8")).decode("ascii")
        return ('\n<div class="interactive-figure" data-visual="' + kind +
                '" data-spec="' + encoded + '"><p>Interactive figure loads on the website.</p></div>\n')
    return pattern.sub(replace, body)


def main():
    pages = []
    for file in sorted(WIKI.rglob("*.md")):
        if file.name.startswith("_"):
            continue
        page_id = file.relative_to(WIKI).as_posix()[:-3]
        front, body = split_frontmatter(file.read_text(encoding="utf-8"))
        body = convert_chatgpt_charts(body)
        category = page_id.split("/", 1)[0]
        if category not in {"projects", "concepts", "techniques", "briefings", "signals", "experiments", "evaluations", "benchmarks", "case-studies", "workflows", "domains"}:
            continue
        title = str(front.get("title") or re.search(r"^# (.+)$", body, re.M).group(1) if re.search(r"^# (.+)$", body, re.M) else page_id)
        summary = str(front.get("summary") or "")
        if re.search(r"<(?:Chart|grid|grid-item|box|row|caption|title|text)\\b", body):
            raise ValueError(f"{file.relative_to(ROOT)}: unconverted ChatGPT layout component in Markdown")
        compiled = embed_visualizations(body)
        if re.search(r"(?m)^\\s{0,3}```(?:chart|vega-lite|mermaid|graph)\\b", compiled):
            raise ValueError(f"{file.relative_to(ROOT)}: visualization fence was not compiled")
        rendered = markdown.markdown(expand_wikilinks(compiled), extensions=["tables", "fenced_code", "sane_lists"])
        rendered = rewrite_links(rendered, page_id)
        rendered = bleach.clean(rendered,
            tags=set(bleach.sanitizer.ALLOWED_TAGS) | {"h1","h2","h3","h4","h5","h6","p","pre","code","img","figure","figcaption","div","span","table","thead","tbody","tr","th","td","hr","br","del","sup","sub"},
            attributes={"a":["href","title","target","rel","aria-label"],"img":["src","alt","title","loading","decoding","width","height"],"*":["class","id","data-visual","data-spec","role","aria-label"]},
            protocols={"http","https","mailto","data"}, strip=True)
        rendered = enhance_media(rendered, file)
        body_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", rendered))[:12000]
        pages.append({"id": page_id, "title": title, "summary": summary, "category": category,
                      "created": str(front.get("created") or ""), "updated": str(front.get("updated") or ""),
                      "depth": str(front.get("depth") or "full"), "type": str(front.get("type") or category.rstrip("s")),
                      "body_text": html.unescape(body_text), "html": rendered})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"pages": pages}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Indexed {len(pages)} pages into {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
