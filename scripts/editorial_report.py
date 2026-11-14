#!/usr/bin/env python3
"""Nonblocking editorial suggestions; no inferred scientific relationships."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re


from build_site import split_frontmatter, expand_wikilinks, rewrite_links
from page_navigation import explicit_targets, resolve_related
import markdown

ROOT = Path(__file__).resolve().parents[1]


def collect(wiki):
    pages = {}
    for path in sorted(wiki.rglob('*.md')):
        if path.name.startswith('_'):
            continue
        front, body = split_frontmatter(path.read_text())
        page_id = path.relative_to(wiki).as_posix()[:-3]
        # Literal examples do not establish article relationships.
        visible = re.sub(r'(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1\s*$', '', body)
        rendered = rewrite_links(markdown.markdown(expand_wikilinks(visible), extensions=['fenced_code']), page_id)
        pages[page_id] = {'front': front, 'body': visible, 'outgoing': explicit_targets(rendered)}
    return pages


def suggestions(pages):
    results = []
    ids = set(pages)
    topic_members = set().union(*(p['outgoing'] for pid, p in pages.items() if pid.startswith('topics/')))
    sources = defaultdict(list)
    titles = defaultdict(list)
    for pid, page in pages.items():
        front, outgoing = page['front'], page['outgoing']
        if front.get('type') == 'index':
            continue
        if front.get('type') == 'concept' and not any(t.startswith('concepts/') for t in outgoing):
            results.append({'kind': 'concept_without_concept_link', 'page': pid})
        if front.get('type') not in {'briefing', 'experiment'} and pid not in topic_members:
            results.append({'kind': 'review_reading_path_membership', 'page': pid})
        _, unresolved = resolve_related(front.get('related', []), ids)
        for value in unresolved:
            results.append({'kind': 'unresolved_related_navigation', 'page': pid, 'target': value})
        # Flag explicit canonical identifiers written as unlinked prose/code.
        for target in sorted(ids - outgoing - {pid}):
            if pages[target]['front'].get('type') == 'index':
                continue
            title = str(pages[target]['front'].get('title', ''))
            named = len(title) >= 8 and re.search(r'(?<!\w)' + re.escape(title) + r'(?!\w)', page['body'], re.I)
            if target in page['body'] or named:
                results.append({'kind': 'unlinked_canonical_mention', 'page': pid, 'target': target})
        if front.get('type') in {'project', 'benchmark', 'workflow', 'case-study', 'experiment'}:
            titles[re.sub(r'[^a-z0-9]', '', str(front.get('title', '')).lower())].append(pid)
            for source in front.get('sources', []):
                value = source.get('url', '') if isinstance(source, dict) else str(source)
                arxiv = re.search(r'arxiv.org/(?:abs|html|pdf)/(\d{4}\.\d{4,5})', value)
                key = 'arxiv:' + arxiv[1] if arxiv else value.rstrip('/')
                if key:
                    sources[key].append(pid)
    for identity, members in sorted(sources.items()):
        members = sorted(set(members))
        if len(members) > 1:
            results.append({'kind': 'shared_source_review_not_duplicate_verdict', 'source': identity, 'pages': members})
    for title, members in sorted(titles.items()):
        if title and len(members) > 1:
            results.append({'kind': 'overlapping_title_review', 'pages': members})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    results = suggestions(collect(ROOT / 'wiki'))
    if args.json:
        print(json.dumps({'status': 'advisory', 'suggestions': results}, indent=2))
    else:
        print(f'Editorial suggestions: {len(results)} (advisory; shared sources do not establish duplicates)')
        for result in results:
            print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
