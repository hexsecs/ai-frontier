"""Derive navigation from explicit links, without inferring evidence relationships."""
from html.parser import HTMLParser
from urllib.parse import unquote


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for key, value in attrs:
                if key == "href" and value and value.startswith("#/page/"):
                    self.targets.add(unquote(value[7:].split("?", 1)[0].split("#", 1)[0]))


def explicit_targets(rendered):
    parser = PageLinks()
    parser.feed(rendered)
    return parser.targets


def reachable_from(start, adjacency):
    seen, pending = set(), [start]
    while pending:
        page = pending.pop()
        if page not in seen:
            seen.add(page)
            pending.extend(adjacency.get(page, ()))
    return seen


def resolve_related(values, ids):
    """Accept full IDs and uniquely resolvable legacy slugs; never guess ambiguity."""
    resolved, unresolved = set(), []
    for value in values if isinstance(values, list) else []:
        if not isinstance(value, str):
            unresolved.append(str(value))
            continue
        value = value.removesuffix(".md")
        candidates = [p for p in ids if p == value or ("/" not in value and p.rsplit("/", 1)[-1] == value)]
        if len(candidates) == 1:
            resolved.add(candidates[0])
        else:
            unresolved.append(value)
    return sorted(resolved), sorted(unresolved)


def attach_navigation(pages):
    ids = {p["id"] for p in pages}
    inbound = {p: set() for p in ids}
    for page in pages:
        outgoing = explicit_targets(page["html"]) & ids - {page["id"]}
        page["outgoing"] = sorted(outgoing)
        for target in outgoing:
            inbound[target].add(page["id"])
        page["related"], page["unresolved_related"] = resolve_related(page.pop("related_raw", []), ids)
        page["related"] = [p for p in page["related"] if p != page["id"]]
    for page in pages:
        page["backlinks"] = sorted(inbound[page["id"]])
