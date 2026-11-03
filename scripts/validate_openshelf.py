#!/usr/bin/env python3
"""Run OpenShelf lint while acknowledging explicitly justified L2 size warnings.

All OpenShelf errors remain fatal. Only the advisory L2 budget warning can be
acknowledged, using a Markdown comment in the affected page.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OVERRIDE = re.compile(r'<!--\s*openshelf:budget-override\s+reason="([^"\n]{12,300})"\s*-->', re.I)
WARNING = re.compile(r'^(.*?): warning: (wiki/[^:]+\.md): page is ~\d+ tokens, over the L2 budget of \d+; consider splitting\s*$')

def main():
    proc = subprocess.run(["openshelf", "lint", "."], cwd=ROOT, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    for line in proc.stdout.splitlines():
        match = WARNING.match(line)
        if match:
            target = (ROOT / match.group(2)).resolve()
            if target.is_relative_to(ROOT / "wiki") and target.is_file():
                source = target.read_text(encoding="utf-8")
                found = OVERRIDE.search(source)
                if found:
                    print(f"{match.group(2)}: L2 token budget acknowledged: {found.group(1)}")
                    continue
        print(line)
    return proc.returncode

if __name__ == "__main__":
    sys.exit(main())
