#!/usr/bin/env python3
"""Reject known KB-maintenance prose, without treating citations as violations.

This is a narrow editorial guard, not a source-truth or completeness verifier.
Scientific processes, proposed ingestion experiments and source caveats are valid.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
RULES = (
    (r'\b(?:mining pass(?:es)?\s+\d|depth pass|depth campaign)\b', 'KB maintenance campaign'),
    (r'\bthis (?:page|article) (?:was|has been) (?:updated|created|expanded|rewritten|promoted)\b', 'article change report'),
    (r'\b(?:previous revision of this page|revision of this page|correction to this page|imported stub|the stub this page replaces)\b', 'article revision history'),
    (r'^#{2,4}\s+(?:Knowledge mining|Canonical updates|Mining audit|What I learned about your interests)\s*$', 'maintenance appendix'),
)


def check(text):
    if text.startswith('---\n'):
        text = text.split('\n---\n', 1)[-1]
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    # Exclude fenced literal examples, including tilde fences and longer fences.
    text = re.sub(r'(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1\s*$', '', text)
    errors = []
    for pattern, label in RULES:
        for match in re.finditer(pattern, text, re.I | re.M):
            errors.append(f'{label}: {match.group(0)}')
    return errors


def main():
    errors = []
    for path in sorted((ROOT / 'wiki').rglob('*.md')):
        if path.name.startswith('_'):
            continue
        errors.extend(f'{path.relative_to(ROOT)}: {e}' for e in check(path.read_text()))
    for error in errors:
        print('ERROR:', error)
    print(f'Article prose: {len(errors)} errors (known maintenance phrases only)')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
