#!/usr/bin/env python3
"""Check in-context canonical references; factual quality still requires review."""
from datetime import date
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CUTOFF = date(2026, 11, 7)
PROCESS_HEADING = re.compile(
    r'^#{2,4}\s+(?:Knowledge mining|Canonical updates|Relations and evidence|Mining audit|'
    r'(?:Research|Preference|Quality|Search)(?: and (?:preference|novelty|search))? audit|'
    r'Traceable seven-briefing audit.*|Cross-briefing audit and selection adjustments|'
    r'What I learned about your interests)\s*$', re.M | re.I)
CANONICAL = re.compile(r'\[\[((?:projects|benchmarks|case-studies|workflows|domains|concepts|techniques|signals|evaluations|experiments)/[^\]|]+)(?:\|[^\]]+)?\]\]')


def validate(text, wiki):
    # Ignore fenced examples and comments when checking visible article structure.
    text = re.sub(r'(?ms)^```.*?^```[^\n]*', '', text)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    errors = [f'process heading belongs in the PR: {m.group(0)}' for m in PROCESS_HEADING.finditer(text)]
    discoveries = list(re.finditer(r'^#{2,3}\s+\d+[.)]\s+.+$', text, re.M))
    if not discoveries:
        errors.append('no numbered discovery sections; use ## 1. Title')
    for m in discoveries:
        following = re.search(r'^#{2,3}\s+', text[m.end():], re.M)
        end = m.end() + following.start() if following else len(text)
        targets = CANONICAL.findall(text[m.end():end])
        if not targets:
            errors.append(f'{m.group(0)}: missing canonical link in the discovery text')
        for target in targets:
            if not (wiki / (target + '.md')).is_file():
                errors.append(f'{m.group(0)}: missing canonical target {target}')
    return errors


def main():
    errors = []
    for path in sorted((ROOT / 'wiki/briefings').glob('*/*/*.md')):
        try:
            day = date.fromisoformat(path.stem)
        except ValueError:
            continue
        if day >= CUTOFF:
            errors.extend(f'{path.relative_to(ROOT)}: {e}' for e in validate(path.read_text(), ROOT / 'wiki'))
    for error in errors:
        print('ERROR:', error)
    print(f'Briefing knowledge integration: {len(errors)} errors')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
